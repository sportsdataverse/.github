"""Offline tests for ecosystem_status.py (stdlib unittest, no network).

Run: python -m unittest discover -s .github/scripts/tests
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ecosystem_status as es  # noqa: E402

PRODUCERS = HERE.parents[2] / "status" / "producers.json"
NOW = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)


def wf(name, file, conclusion=None, created_at=None):
    return {
        "name": name,
        "file": f".github/workflows/{file}",
        "conclusion": conclusion,
        "created_at": created_at,
        "age_days": None,
        "url": f"https://github.com/x/actions/workflows/{file}",
        "event": "schedule" if conclusion else None,
        "state": "active",
    }


def fake_snap():
    """Two producers, one package, a hub with mapped / unmapped / snapshot tags."""
    rel = lambda newest, season, n=1: {  # noqa: E731
        "published_at": "2025-01-01T00:00:00Z",
        "assets": n,
        "asset_bytes": 1,
        "newest_asset_at": newest,
        "max_season": season,
    }
    repo = lambda full, wfs, releases=None: {  # noqa: E731
        "full_name": full,
        "private": False,
        "open_prs": [],
        "open_issues": 0,
        "stale_unassigned_issues": [],
        "workflows": {w["name"]: w for w in wfs},
        "red_workflows": [w["name"] for w in wfs if w["conclusion"] == "failure"],
        "releases": releases or {},
        "latest_release_tag": next(iter(releases or {}), None),
        "newest_asset_at": None,
        "newest_asset_age_days": None,
        "pushed_age_days": 1.0,
    }
    return {
        "generated_at": NOW.isoformat(),
        "totals": {"repos": 4},
        "repos": {
            "sportsdataverse/sportsdataverse-data": repo(
                "sportsdataverse/sportsdataverse-data",
                [],
                {
                    "espn_wnba_pbp": rel("2026-09-29T00:00:00Z", 2026),
                    "espn_wnba_schedules": rel("2026-09-28T00:00:00Z", 2027),  # pre-season file
                    "espn_wnba_injuries": rel("2026-09-30T00:00:00Z", 2027),
                    "espn_nba_pbp": rel("2026-06-20T00:00:00Z", 2026),
                    "phf_pbp": rel("2023-03-01T00:00:00Z", 2023),
                    "zzz_new": rel(None, None, 0),
                },
            ),
            "sportsdataverse/wehoop-wnba-data": repo(
                "sportsdataverse/wehoop-wnba-data",
                [wf("Update WNBA Data", "daily_wnba.yml", "success", "2026-09-29T07:00:00Z")],
            ),
            "sportsdataverse/cfbfastR-cfb-data": repo(
                "sportsdataverse/cfbfastR-cfb-data",
                [wf("ESPN Daily Snapshots", "espn_daily_snapshots.yml", "success", "2026-09-30T13:00:00Z")],
            ),
            "sportsdataverse/hoopR": repo(
                "sportsdataverse/hoopR",
                [
                    wf("R-CMD-check", "R-CMD-check.yaml", "failure", "2026-09-20T00:00:00Z"),
                    wf("pkgdown", "pkgdown.yaml"),
                ],
                {"v3.0.0": rel(None, None, 0)},
            ),
        },
    }


def fake_cfg():
    return {
        "package_repos": ["sportsdataverse/hoopR"],
        "rules": [
            {"prefix": "espn_wnba_injuries", "repo": "sportsdataverse/cfbfastR-cfb-data", "freshness": False},
            {"prefix": "phf_", "repo": None},
            {"prefix": "espn_wnba_", "repo": "sportsdataverse/wehoop-wnba-data"},
        ],
        "producers": [
            {
                "repo": "sportsdataverse/wehoop-wnba-data",
                "label": "WNBA (ESPN)",
                "sport": "basketball",
                "packages": ["hoopR"],
                "raw_repo": None,
                "schedule": "Daily",
                "season": {"start": "05-01", "end": "10-25"},
                "stale_after_days": 5,
                "update_workflows": ["daily_wnba.yml"],
                "through_tags": ["espn_wnba_pbp"],
            },
            {
                "repo": "sportsdataverse/cfbfastR-cfb-data",
                "label": "CFB",
                "sport": "football",
                "packages": [],
                "raw_repo": None,
                "schedule": "Daily",
                "season": {"start": "08-20", "end": "01-25"},
                "stale_after_days": 10,
                "update_workflows": ["espn_daily_snapshots.yml"],
            },
        ],
    }


class SeasonWindow(unittest.TestCase):
    WRAP = {"start": "10-18", "end": "04-15"}
    PLAIN = {"start": "05-01", "end": "10-25"}

    def test_wrapping_window_both_boundaries(self):
        f = lambda m, d: es.in_season(self.WRAP, date(2026, m, d))  # noqa: E731
        self.assertFalse(f(10, 17))
        self.assertTrue(f(10, 18))
        self.assertTrue(f(12, 31))
        self.assertTrue(f(1, 1))
        self.assertTrue(f(4, 15))
        self.assertFalse(f(4, 16))
        self.assertFalse(f(7, 1))

    def test_plain_window_both_boundaries(self):
        f = lambda m, d: es.in_season(self.PLAIN, date(2026, m, d))  # noqa: E731
        self.assertFalse(f(4, 30))
        self.assertTrue(f(5, 1))
        self.assertTrue(f(10, 25))
        self.assertFalse(f(10, 26))

    def test_full_year_and_leap_day(self):
        full = {"start": "01-01", "end": "12-31"}
        self.assertTrue(es.in_season(full, date(2028, 2, 29)))
        self.assertTrue(es.in_season({"start": "02-14", "end": "10-31"}, date(2028, 2, 29)))


class MaxSeason(unittest.TestCase):
    def test_accepts_standalone_year(self):
        self.assertEqual(es.max_season(["play_by_play_2026.parquet"]), 2026)
        self.assertEqual(es.max_season(["a_2019.rds", "b_2025.csv.gz", "timestamp.json"]), 2025)

    def test_rejects_dates_and_long_digit_runs(self):
        self.assertIsNone(es.max_season(["pbp_20260929.parquet"]))
        self.assertIsNone(es.max_season(["game_120255.json", "id_401520281.parquet"]))
        self.assertIsNone(es.max_season(["x_1066.rds", "y_2099.rds"]))  # outside 1950-2049
        self.assertIsNone(es.max_season([]))

    def test_year_next_to_letters_counts(self):
        self.assertEqual(es.max_season(["nhl_pbp2024.rds", "shots_2023-24.csv"]), 2024)


class Rules(unittest.TestCase):
    cfg = es.load_producers(PRODUCERS)

    def owner(self, tag):
        r = es.match_rule(tag, self.cfg["rules"])
        return r and r["repo"]

    def test_specific_prefix_wins(self):
        self.assertEqual(self.owner("nba_stats_pbp"), "sportsdataverse/hoopR-nba-stats-data")
        self.assertEqual(self.owner("nba_player_impact"), "sportsdataverse/hoopR-nba-stats-data")
        self.assertEqual(self.owner("nba_crosswalk"), "sportsdataverse/hoopR-nba-data")
        self.assertEqual(self.owner("cfbfastR_cfb_pbp"), "sportsdataverse/cfbfastR-data")
        self.assertEqual(self.owner("cfb_ratings"), "sportsdataverse/cfbfastR-cfb-data")
        self.assertEqual(self.owner("cfb_groups"), "sportsdataverse/sdv-reference-data")
        self.assertEqual(self.owner("espn_nba_injuries"), "sportsdataverse/cfbfastR-cfb-data")
        self.assertEqual(self.owner("espn_nba_pbp"), "sportsdataverse/hoopR-nba-data")
        self.assertEqual(self.owner("nfl_ngs_passing"), "sportsdataverse/nfl-ngs-data")
        self.assertEqual(self.owner("nfl_pbp"), "sportsdataverse/nfl-data")
        self.assertEqual(self.owner("wnba_stats_pbp"), "sportsdataverse/wehoop-wnba-stats-data")
        self.assertEqual(self.owner("wnba_crosswalk"), "sportsdataverse/wehoop-wnba-data")

    def test_unattributed_and_unknown_stay_unmapped(self):
        self.assertIsNone(self.owner("phf_pbp"))
        self.assertIsNone(self.owner("nhl_xg_models"))
        self.assertIsNone(self.owner("brand_new_family_2027"))

    def test_shadowed_rule_is_refused(self):
        bad = {
            "package_repos": [],
            "rules": [{"prefix": "nba_", "repo": "a/b"}, {"prefix": "nba_stats_", "repo": "a/c"}],
            "producers": [],
        }
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "producers.json"
            p.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(SystemExit):
                es.load_producers(p)

    def test_through_tags_belong_to_their_producer(self):
        for p in self.cfg["producers"]:
            for t in p.get("through_tags", []):
                self.assertEqual(self.owner(t), p["repo"], t)

    def test_every_producer_entry_is_complete(self):
        keys = {
            "repo",
            "label",
            "sport",
            "packages",
            "raw_repo",
            "schedule",
            "season",
            "stale_after_days",
            "update_workflows",
        }
        for p in self.cfg["producers"]:
            self.assertLessEqual(keys, set(p), p["repo"])
            for k in ("start", "end"):
                self.assertRegex(p["season"][k], r"^\d\d-\d\d$")


class StateMachine(unittest.TestCase):
    season = {"start": "05-01", "end": "10-25"}

    def ds(self, updated_at, today):
        return es.data_state(updated_at, self.season, 5, today, NOW)[0]

    def test_data_states(self):
        self.assertEqual(self.ds("2026-09-29T00:00:00Z", date(2026, 9, 30)), "fresh")
        self.assertEqual(self.ds("2026-09-01T00:00:00Z", date(2026, 9, 30)), "stale")
        self.assertEqual(self.ds("2026-09-01T00:00:00Z", date(2026, 12, 1)), "idle")
        self.assertEqual(self.ds(None, date(2026, 9, 30)), "unknown")

    DATA = "2026-09-20T00:00:00Z"  # newest counted asset

    @staticmethod
    def wf_run(conclusion, created_at="2026-09-25T00:00:00Z"):
        return {"conclusion": conclusion, "created_at": created_at}

    def test_failing_beats_stale_beats_idle(self):
        r = self.wf_run
        self.assertEqual(es.producer_state("stale", [r("success"), r("failure")], self.DATA), "failing")
        self.assertEqual(es.producer_state("stale", [r("success"), r(None, None), r("cancelled")], self.DATA), "stale")
        self.assertEqual(es.producer_state("idle", [r("success")], self.DATA), "idle")
        self.assertEqual(es.producer_state("unknown", [], None), "unknown")

    def test_failure_older_than_last_data_is_not_failing(self):
        old = self.wf_run("failure", "2026-08-05T00:00:00Z")
        self.assertEqual(es.producer_state("fresh", [old], self.DATA), "fresh")
        self.assertEqual(es.producer_state("stale", [old], self.DATA), "stale")

    def test_failure_newer_than_last_data_is_failing_even_off_season(self):
        self.assertEqual(es.producer_state("idle", [self.wf_run("timed_out")], self.DATA), "failing")
        self.assertEqual(es.producer_state("fresh", [self.wf_run("startup_failure")], self.DATA), "failing")

    def test_failed_run_and_no_data_is_failing(self):
        self.assertEqual(es.producer_state("unknown", [self.wf_run("failure")], None), "failing")

    def test_cancelled_is_never_failing(self):
        self.assertEqual(es.producer_state("fresh", [self.wf_run("cancelled")], self.DATA), "fresh")

    def test_idle_is_never_red(self):
        p = {
            "state": "idle",
            "data_state": "idle",
            "updated_at": "2026-06-01T00:00:00Z",
            "age_days": 120.0,
            "through_season": 2026,
        }
        for b in es.producer_badges(p).values():
            self.assertNotEqual(b["color"], "red")
        self.assertEqual(es.producer_badges(p)["status"]["message"], "idle (off-season)")
        self.assertEqual(es.producer_badges(p)["status"]["color"], "blue")


class Badges(unittest.TestCase):
    SHAPE = {"schemaVersion", "label", "message", "color", "namedLogo"}

    def check(self, b, label, message, color):
        self.assertEqual(set(b), self.SHAPE)
        self.assertEqual(b["schemaVersion"], 1)
        self.assertEqual(b["namedLogo"], "github")
        self.assertEqual((b["label"], b["message"], b["color"]), (label, message, color))

    def test_workflow_badges(self):
        ok = wf("Update WBB Data", "daily_wbb.yml", "success", "2026-09-09T07:00:00Z")
        self.check(es.wf_badge(ok), "Update WBB Data", "passing · 2026-09-09", "brightgreen")
        bad = wf("R-CMD-check", "R-CMD-check.yaml", "failure", "2026-09-20T00:00:00Z")
        self.check(es.wf_badge(bad), "R-CMD-check", "failing · 2026-09-20", "red")
        cx = wf("x", "x.yml", "cancelled", "2026-09-21T00:00:00Z")
        self.check(es.wf_badge(cx), "x", "cancelled · 2026-09-21", "yellow")
        self.check(es.wf_badge(wf("pkgdown", "pkgdown.yaml")), "pkgdown", "no runs", "lightgrey")

    def test_producer_badges(self):
        p = {
            "state": "stale",
            "data_state": "stale",
            "updated_at": "2026-09-01T10:00:00Z",
            "age_days": 29.1,
            "through_season": 2026,
        }
        b = es.producer_badges(p)
        self.check(b["updated"], "data updated", "2026-09-01", "orange")
        self.check(b["through"], "through", "2026 season", "blue")
        self.check(b["status"], "pipeline", "stale 29d", "orange")
        p = {
            "state": "failing",
            "data_state": "fresh",
            "updated_at": "2026-09-29T10:00:00Z",
            "age_days": 1.0,
            "through_season": None,
        }
        b = es.producer_badges(p)
        self.check(b["updated"], "data updated", "2026-09-29", "brightgreen")
        self.check(b["through"], "through", "unknown", "lightgrey")
        self.check(b["status"], "pipeline", "failing", "red")
        p = {"state": "unknown", "data_state": "unknown", "updated_at": None, "age_days": None, "through_season": None}
        self.check(es.producer_badges(p)["status"], "pipeline", "unknown", "lightgrey")

    def test_write_json_is_utf8_lf_sorted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "b" / "x.json"
            es.write_json(p, {"b": "passing · 2026-09-09", "a": 1})
            raw = p.read_bytes()
        self.assertIn("·".encode("utf-8"), raw)
        self.assertNotIn(b"\r\n", raw)
        self.assertTrue(raw.endswith(b"}\n"))
        self.assertLess(raw.index(b'"a"'), raw.index(b'"b"'))

    def test_badge_files_cover_every_workflow_and_producer(self):
        snap = fake_snap()
        files = es.badge_files(snap, es.build_summary(snap, fake_cfg(), NOW))
        for key in (
            "hoopR/wf-R-CMD-check.json",
            "hoopR/wf-pkgdown.json",
            "wehoop-wnba-data/wf-daily_wnba.json",
            "wehoop-wnba-data/updated.json",
            "wehoop-wnba-data/through.json",
            "wehoop-wnba-data/status.json",
            "cfbfastR-cfb-data/status.json",
        ):
            self.assertIn(key, files)
        self.assertEqual(files["hoopR/wf-pkgdown.json"]["message"], "no runs")

    def test_duplicate_workflow_stem_fails_loudly(self):
        snap = fake_snap()
        wfs = snap["repos"]["sportsdataverse/hoopR"]["workflows"]
        wfs["dup"] = {**wfs["pkgdown"], "name": "dup", "file": ".github/workflows/pkgdown.yml"}
        with self.assertRaises(SystemExit):
            es.badge_files(snap, es.build_summary(snap, fake_cfg(), NOW))


class RepoFilters(unittest.TestCase):
    def test_private_repos_are_dropped(self):
        repos = [
            {"full_name": "sportsdataverse/a", "private": False},
            {"full_name": "sportsdataverse/secret", "private": True},
            {"full_name": "sportsdataverse/old", "private": False, "archived": True},
        ]
        self.assertEqual([r["full_name"] for r in es.drop_private(repos)], ["sportsdataverse/a"])

    def test_bare_name_collision_fails_loudly(self):
        es.check_bare_names(["sportsdataverse/hoopR", "BillPetti/baseballr"])
        with self.assertRaises(SystemExit):
            es.check_bare_names(["sportsdataverse/baseballr", "BillPetti/baseballr"])

    def test_dynamic_workflows(self):
        self.assertTrue(es.is_dynamic("dynamic/dependabot/dependabot-updates"))
        self.assertTrue(es.is_dynamic(None))
        self.assertFalse(es.is_dynamic(".github/workflows/daily_wbb.yml"))


class Summary(unittest.TestCase):
    def setUp(self):
        self.snap = fake_snap()
        self.summary = es.build_summary(self.snap, fake_cfg(), NOW)

    def test_release_tags_stalest_first_empty_last(self):
        rt = self.summary["release_tags"]
        self.assertEqual(
            [t["tag"] for t in rt],
            ["phf_pbp", "espn_nba_pbp", "espn_wnba_schedules", "espn_wnba_pbp", "espn_wnba_injuries", "zzz_new"],
        )
        self.assertEqual(set(rt[0]), {"tag", "producer", "assets", "newest_asset_at", "max_season"})
        self.assertIsNone(rt[0]["producer"])
        self.assertEqual(rt[3]["producer"], "sportsdataverse/wehoop-wnba-data")
        self.assertEqual(rt[2]["max_season"], 2027)  # per-tag max_season stays raw
        self.assertEqual(self.summary["unmapped_tags"], ["phf_pbp", "espn_nba_pbp", "zzz_new"])

    def test_through_tags_limit_through_season(self):
        wnba = next(p for p in self.summary["producers"] if p["repo"].endswith("wehoop-wnba-data"))
        self.assertEqual(wnba["through_season"], 2026)  # pbp only, not the 2027 schedule
        cfg = fake_cfg()
        del cfg["producers"][0]["through_tags"]
        s = es.build_summary(fake_snap(), cfg, NOW)
        wnba = next(p for p in s["producers"] if p["repo"].endswith("wehoop-wnba-data"))
        self.assertEqual(wnba["through_season"], 2027)  # default: every counted tag

    def test_tags_is_a_count_with_names_beside_it(self):
        wnba = next(p for p in self.summary["producers"] if p["repo"].endswith("wehoop-wnba-data"))
        self.assertEqual(wnba["tags"], 2)
        self.assertEqual(wnba["tag_names"], ["espn_wnba_pbp", "espn_wnba_schedules"])

    def test_freshness_false_tags_do_not_count(self):
        cfb = next(p for p in self.summary["producers"] if p["repo"].endswith("cfbfastR-cfb-data"))
        self.assertEqual(cfb["tag_names"], ["espn_wnba_injuries"])
        self.assertIsNone(cfb["updated_at"])
        self.assertEqual(cfb["state"], "unknown")
        wnba = next(p for p in self.summary["producers"] if p["repo"].endswith("wehoop-wnba-data"))
        self.assertEqual(wnba["updated_at"], "2026-09-29T00:00:00Z")
        self.assertEqual(wnba["through_season"], 2026)
        self.assertEqual(wnba["state"], "fresh")
        self.assertEqual(wnba["workflows"][0]["file"], ".github/workflows/daily_wnba.yml")

    def test_packages_and_red(self):
        self.assertEqual(self.summary["packages"][0]["repo"], "sportsdataverse/hoopR")
        self.assertEqual([r["file"] for r in self.summary["red_workflows"]], [".github/workflows/R-CMD-check.yaml"])


class Markdown(unittest.TestCase):
    def setUp(self):
        snap = fake_snap()
        self.md = es.render_md(snap, es.build_summary(snap, fake_cfg(), NOW))

    def test_empty_tags_print_empty_and_sort_last(self):
        rows = [l for l in self.md.splitlines() if l.startswith("| ") and "|---" not in l]
        tag_rows = rows[1:7]  # header, then the six release tags
        self.assertTrue(tag_rows[-1].startswith("| zzz_new |"))
        self.assertIn("| empty |", tag_rows[-1])

    def test_doctoc_markers_exactly_once(self):
        self.assertEqual(self.md.count(es.TOC_START), 1)
        self.assertEqual(self.md.count(es.TOC_END), 1)
        self.assertLess(self.md.index(es.TOC_START), self.md.index("\n## "))

    def test_release_tags_section_comes_first(self):
        heads = [l for l in self.md.splitlines() if l.startswith("## ")]
        self.assertEqual(heads[0], es.RELEASE_TAGS_HEADING)
        self.assertEqual(heads[1], "## Producers")
        self.assertEqual(heads[-1], "## Unmapped release tags")

    def test_headings_hold_no_counts_or_dates(self):
        for l in self.md.splitlines():
            if l.startswith("#"):
                self.assertIsNone(re.search(r"\d", l), l)


if __name__ == "__main__":
    unittest.main()
