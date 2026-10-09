"""Tests for skills/sdv-metric-parity/scripts/ladder_parity.py.

Run: python -m unittest discover -s tools -p 'test_*.py'

Each check is tested on the defect it exists to catch (2026-10-08 percentile audit) and on a
matched pair it must leave alone: a check that cannot fail is worse than none.
"""

import csv
import io
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(
    0,
    str(
        pathlib.Path(__file__).resolve().parent.parent
        / "skills"
        / "sdv-metric-parity"
        / "scripts"
    ),
)

import ladder_parity as lp  # noqa: E402


def _ladder(lo: float, hi: float) -> list[float]:
    """99 breakpoints of a uniform distribution on [lo, hi], like a pctile 1..99 ladder column."""
    return [lo + (hi - lo) * p / 100 for p in range(1, 100)]


def _uniform(lo: float, hi: float, n: int = 1000) -> list[float]:
    return [lo + (hi - lo) * (i + 0.5) / n for i in range(n)]


class PercentileOf(unittest.TestCase):
    def test_midrank_counts_ties_half(self):
        self.assertEqual(lp.percentile_of(2.5, [1, 2, 3, 4]), 50.0)
        self.assertEqual(lp.percentile_of(2, [1, 2, 3, 4]), 37.5)

    def test_outside_the_ladder_is_0_or_100(self):
        self.assertEqual(lp.percentile_of(-1, [1, 2, 3]), 0.0)
        self.assertEqual(lp.percentile_of(9, [1, 2, 3]), 100.0)


class MeanShown(unittest.TestCase):
    def test_matched_definition_shows_about_the_50th(self):
        mean, median, n = lp.mean_shown(_uniform(0.0, 0.3), _ladder(0.0, 0.3))
        self.assertEqual(n, 1000)
        self.assertAlmostEqual(mean, 50.0, delta=1.0)
        self.assertAlmostEqual(median, 50.0, delta=1.5)

    def test_nulls_and_nans_are_skipped(self):
        _, _, n = lp.mean_shown([0.1, None, float("nan"), 0.2], _ladder(0.0, 0.3))
        self.assertEqual(n, 2)


def _rows(
    metric_values: dict, season: int = 2025, extra: dict | None = None
) -> list[dict]:
    n = len(next(iter(metric_values.values())))
    rows = []
    for i in range(n):
        r = {"season": season}
        r.update({k: v[i] for k, v in metric_values.items()})
        for k, v in (extra or {}).items():
            r[k] = v[i]
        rows.append(r)
    return rows


def _ladder_rows(keys: dict, season: int = 2025) -> list[dict]:
    return [
        {"season": season, "pctile": p, **{k: v[p - 1] for k, v in keys.items()}}
        for p in range(1, 100)
    ]


class Check(unittest.TestCase):
    def test_stuff_rate_against_an_all_plays_ladder_is_a_mismatch(self):
        # F1: the box counts stuffs over rushes (p50 .161); the ladder over all plays (p50 .300).
        values = _rows({"rushing_stuff_rate": _uniform(0.0, 0.32)})
        ladder = _ladder_rows({"play_stuffed": _ladder(0.10, 0.50)})
        [res] = lp.check(values, ladder, {"rushing_stuff_rate": "play_stuffed"})
        self.assertEqual(res.verdict, "MISMATCH")
        self.assertLess(res.mean_shown, 30)

    def test_a_matched_pair_is_ok(self):
        values = _rows({"epa_per_play": _uniform(-0.4, 0.6)})
        ladder = _ladder_rows({"EPAplay": _ladder(-0.4, 0.6)})
        [res] = lp.check(values, ladder, {"epa_per_play": "EPAplay"})
        self.assertEqual(res.verdict, "OK")

    def test_small_drift_is_watch_not_mismatch(self):
        # A2-sized drift (mean shown ~54): worth a look, not a failure.
        values = _rows({"yards_per_dropback": _uniform(1.3, 11.3)})
        ladder = _ladder_rows({"yardsdropback": _ladder(1.0, 11.0)})
        [res] = lp.check(
            values, ladder, {"yards_per_dropback": "yardsdropback"}, tol=4.0
        )
        self.assertEqual(res.verdict, "WATCH")

    def test_home_relative_yardline_shows_as_side_asymmetry(self):
        # B2: home red-zone plays were never detected, so home rows sit at 0.
        n = 1000
        side = [1 if i % 2 else 0 for i in range(n)]
        rz = [0.0 if s else v for s, v in zip(side, _uniform(0.0, 0.4, n))]
        values = _rows({"red_zone_rate": rz}, extra={"home": side})
        ladder = _ladder_rows({"rz_rate": _ladder(0.0, 0.4)})
        [res] = lp.check(values, ladder, {"red_zone_rate": "rz_rate"}, side_col="home")
        self.assertEqual(res.verdict, "SIDE-ASYMMETRY")

    def test_home_field_advantage_is_not_side_asymmetry(self):
        # Real CFB 2025 yards/play: home shows ~55, away ~40 (home teams also host the weak
        # non-conference opponents). Only a side pinned near 0 or 100 is an orientation bug.
        n = 1000
        side = [1 if i % 2 else 0 for i in range(n)]
        ypp = [v + (0.4 if s else -0.4) for s, v in zip(side, _uniform(2.0, 9.0, n))]
        values = _rows({"yards_per_play": ypp}, extra={"home": side})
        ladder = _ladder_rows({"yardsplay": _ladder(2.0, 9.0)})
        [res] = lp.check(
            values, ladder, {"yards_per_play": "yardsplay"}, side_col="home"
        )
        self.assertNotEqual(res.verdict, "SIDE-ASYMMETRY")

    def test_no_values_is_reported_not_crashed(self):
        values = _rows({"rate": [None, None]})
        ladder = _ladder_rows({"key": _ladder(0, 1)})
        [res] = lp.check(values, ladder, {"rate": "key"})
        self.assertEqual(res.verdict, "NO-DATA")

    def test_only_seasons_in_both_inputs_are_checked(self):
        values = _rows({"m": _uniform(0, 1)}, season=2024) + _rows(
            {"m": _uniform(0, 1)}, season=2025
        )
        ladder = _ladder_rows({"k": _ladder(0, 1)}, season=2025)
        results = lp.check(values, ladder, {"m": "k"})
        self.assertEqual([r.season for r in results], [2025])

    def test_checking_nothing_is_an_error_not_an_ok(self):
        # A per-season ladder file has no season column: zero overlapping seasons must not read as "ok".
        values = _rows({"m": _uniform(0, 1)}, season=2025)
        ladder = [
            {k: v for k, v in r.items() if k != "season"}
            for r in _ladder_rows({"k": _ladder(0, 1)})
        ]
        with self.assertRaisesRegex(ValueError, "no season"):
            lp.check(values, ladder, {"m": "k"})

    def test_a_ladder_without_a_season_column_takes_season_from_the_argument(self):
        values = _rows({"m": _uniform(0.0, 0.32)}, season=2025)
        ladder = [
            {k: v for k, v in r.items() if k != "season"}
            for r in _ladder_rows({"k": _ladder(0.1, 0.5)})
        ]
        [res] = lp.check(values, ladder, {"m": "k"}, season=2025)
        self.assertEqual((res.season, res.verdict), (2025, "MISMATCH"))

    def test_an_unknown_ladder_key_is_a_usage_error(self):
        values = _rows({"m": _uniform(0, 1)})
        ladder = _ladder_rows({"k": _ladder(0, 1)})
        with self.assertRaisesRegex(ValueError, "ladder has no column 'nope'"):
            lp.check(values, ladder, {"m": "nope"})


class SplitSums(unittest.TestCase):
    def test_parts_divided_by_all_plays_sum_to_the_overall_rate(self):
        # E1: late-down pass and rush success rates were means over every late-down play.
        rows = [
            {"late_sr": 0.5, "late_pass_sr": 0.3, "late_rush_sr": 0.2}
            for _ in range(10)
        ]
        res = lp.split_sums(rows, "late_sr", ["late_pass_sr", "late_rush_sr"])
        self.assertEqual(res.verdict, "SPLIT-SUMS")

    def test_parts_on_their_own_denominators_do_not(self):
        rows = [
            {"late_sr": 0.5, "late_pass_sr": 0.55, "late_rush_sr": 0.44}
            for _ in range(10)
        ]
        res = lp.split_sums(rows, "late_sr", ["late_pass_sr", "late_rush_sr"])
        self.assertEqual(res.verdict, "OK")


class Main(unittest.TestCase):
    def _write(self, path: pathlib.Path, rows: list[dict]) -> None:
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    def test_csv_round_trip_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            self._write(
                d / "v.csv",
                _rows(
                    {"stuff": _uniform(0.0, 0.32, 200), "epa": _uniform(-0.4, 0.6, 200)}
                ),
            )
            self._write(
                d / "l.csv",
                _ladder_rows(
                    {"play_stuffed": _ladder(0.1, 0.5), "EPAplay": _ladder(-0.4, 0.6)}
                ),
            )
            args = ["--values", str(d / "v.csv"), "--ladder", str(d / "l.csv")]
            out = io.StringIO()
            with redirect_stdout(out):
                ok = lp.main([*args, "--map", "epa=EPAplay"])
            self.assertEqual(ok, 0, out.getvalue())
            self.assertIn("VERDICT: ok", out.getvalue())
            out = io.StringIO()
            with redirect_stdout(out):
                bad = lp.main([*args, "--map", "epa=EPAplay,stuff=play_stuffed"])
            self.assertEqual(bad, 1)
            self.assertIn("MISMATCH", out.getvalue())
            self.assertIn("VERDICT: mismatch", out.getvalue())

    def test_a_missing_input_file_is_exit_2_not_a_traceback(self):
        with tempfile.TemporaryDirectory() as d:
            err = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(err):
                code = lp.main(
                    [
                        "--values",
                        f"{d}/nope.csv",
                        "--ladder",
                        f"{d}/nope2.csv",
                        "--map",
                        "a=b",
                    ]
                )
            self.assertEqual(code, 2)
            self.assertIn("nope.csv", err.getvalue())

    def test_a_missing_values_column_is_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            self._write(d / "v.csv", _rows({"epa": _uniform(0, 1, 10)}))
            self._write(d / "l.csv", _ladder_rows({"EPAplay": _ladder(0, 1)}))
            with redirect_stdout(io.StringIO()):
                code = lp.main(
                    [
                        "--values",
                        str(d / "v.csv"),
                        "--ladder",
                        str(d / "l.csv"),
                        "--map",
                        "nope=EPAplay",
                    ]
                )
            self.assertEqual(code, 2)


class ReviewFixes(unittest.TestCase):
    """2026-10-09 review: every way the script could report ok while checking nothing."""

    def _main(self, values, ladder, *args):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            for name, rows in (("v.csv", values), ("l.csv", ladder)):
                with (d / name).open("w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
                    w.writeheader()
                    w.writerows(rows)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = lp.main(["--values", str(d / "v.csv"), "--ladder", str(d / "l.csv"), *args])
            return code, out.getvalue(), err.getvalue()

    def test_no_data_fails_the_run(self):
        code, out, _ = self._main(_rows({"m": [None] * 5}), _ladder_rows({"k": _ladder(0, 1)}), "--map", "m=k")
        self.assertEqual(code, 1)
        self.assertIn("NO-DATA", out)
        self.assertNotIn("VERDICT: ok", out)

    def test_a_split_naming_a_missing_column_is_exit_2(self):
        code, _, err = self._main(
            _rows({"m": _uniform(0, 1, 10)}), _ladder_rows({"k": _ladder(0, 1)}), "--map", "m=k", "--split", "m=m+typo"
        )
        self.assertEqual(code, 2)
        self.assertIn("typo", err)

    def test_a_split_without_equals_is_exit_2(self):
        code, _, _ = self._main(_rows({"m": _uniform(0, 1, 10)}), _ladder_rows({"k": _ladder(0, 1)}), "--map", "m=k",
                                "--split", "m+m")
        self.assertEqual(code, 2)

    def test_psql_t_f_booleans_drive_the_side_check(self):
        # psql \copy writes booleans as t/f; without ::int the side check must still run, not silently skip.
        n = 1000
        side = ["t" if i % 2 else "f" for i in range(n)]
        rz = [0.0 if s == "t" else v for s, v in zip(side, _uniform(0.0, 0.4, n))]
        [res] = lp.check(_rows({"rz": rz}, extra={"home": side}), _ladder_rows({"k": _ladder(0.0, 0.4)}),
                         {"rz": "k"}, side_col="home")
        self.assertEqual(res.verdict, "SIDE-ASYMMETRY")

    def test_a_side_column_with_one_side_empty_is_an_error(self):
        values = _rows({"m": _uniform(0, 1, 10)}, extra={"home": ["yes"] * 10})
        with self.assertRaisesRegex(ValueError, "home"):
            lp.check(values, _ladder_rows({"k": _ladder(0, 1)}), {"m": "k"}, side_col="home")

    def test_a_non_positive_or_nan_tolerance_is_exit_2(self):
        for bad in ("-1", "nan", "0"):
            code, _, _ = self._main(_rows({"m": _uniform(0, 1, 10)}), _ladder_rows({"k": _ladder(0, 1)}),
                                    "--map", "m=k", "--tol", bad)
            self.assertEqual(code, 2, bad)

    def test_a_matched_ladder_centres_on_50(self):
        self.assertEqual(lp.MATCHED, 50.0)

    def test_rounded_parts_still_sum_to_the_whole(self):
        # Stored at 4 dp, parts divided by the whole population miss the overall rate by ~1e-4.
        rows = [{"o": 0.3333, "a": 0.1111, "b": 0.2223} for _ in range(10)]
        self.assertEqual(lp.split_sums(rows, "o", ["a", "b"]).verdict, "SPLIT-SUMS")

    def test_a_pooled_ladder_warns(self):
        ladder = _ladder_rows({"k": _ladder(0, 1)}) + _ladder_rows({"k": _ladder(0, 1)})  # 198 rows in one season
        code, out, err = self._main(_rows({"m": _uniform(0, 1, 50)}), ladder, "--map", "m=k")
        self.assertIn("198 ladder rows", err)


class BotThreadFixes(unittest.TestCase):
    """PR #50 review threads."""

    def test_an_all_null_ladder_column_is_no_data_not_a_crash(self):
        values = _rows({"m": _uniform(0, 1, 10)})
        ladder = _ladder_rows({"k": [None] * 99})
        [res] = lp.check(values, ladder, {"m": "k"})
        self.assertEqual(res.verdict, "NO-DATA")

    def test_an_empty_map_is_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            (d / "v.csv").write_text("season,m\n2025,0.1\n", encoding="utf-8")
            (d / "l.csv").write_text("season,pctile,k\n2025,1,0.1\n", encoding="utf-8")
            (d / "empty.map").write_text("\n", encoding="utf-8")
            for spec in ("", " , ", f"@{d / 'empty.map'}"):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    code = lp.main(["--values", str(d / "v.csv"), "--ladder", str(d / "l.csv"), "--map", spec])
                self.assertEqual(code, 2, repr(spec))


if __name__ == "__main__":
    unittest.main()
