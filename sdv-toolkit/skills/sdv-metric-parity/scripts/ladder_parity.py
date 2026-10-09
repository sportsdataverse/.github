"""Check that a metric shown against a percentile ladder means the same thing as that ladder.

The core test is "mean shown": rank every value computed with the DISPLAY's definition against the ladder it is
displayed with. A ladder built from the same definition and population averages ~49.5; the 2026-10-08 audit found
the CFB Def Run Stuff Rate (rushes only) ranked against an all-plays ladder averaging 13.4, so a 13% stuff rate
showed 1st instead of ~34th. Two more checks catch the other classes the audit found: a home/away gap in mean
shown (a home-relative yard line made home red-zone plays invisible) and parts that sum to the whole (pass and
rush rates divided by all plays).

    ladder_parity.py --values V --ladder L --map display=key[,display=key...]
                     [--season 2025] [--tol 4] [--side-col home] [--side-tol 25] [--split overall=part1+part2]

V: one row per unit (team-game, player-game), a `season` column, one column per display metric computed with the
display's own definition, the same population the ladder was built on (e.g. FBS-vs-FBS team-games).
L: wide ladder, `season` (or `year`) plus one column per ladder key, one row per percentile breakpoint.
CSV or parquet (parquet needs polars). Exit 0 all OK/WATCH, 1 any MISMATCH / SIDE-ASYMMETRY / SPLIT-SUMS,
2 usage or data error.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import math
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

MATCHED = 49.5  # mean percentile a matched ladder shows under midrank ranking of 99 breakpoints


def _num(v):
    """A float, or None for blank / null / NaN / non-numeric cells."""
    if v is None or v == "":
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


def percentile_of(value: float, breakpoints: list[float]) -> float:
    """Midrank percentile of ``value`` against sorted ``breakpoints``: ties count half, so a matched sample averages 50."""
    below = bisect.bisect_left(breakpoints, value)
    equal = bisect.bisect_right(breakpoints, value) - below
    return 100.0 * (below + 0.5 * equal) / len(breakpoints)


def mean_shown(values, breakpoints) -> tuple[float, float, int]:
    """(mean, median, n) of the percentiles ``values`` would display against ``breakpoints``; nulls skipped."""
    bps = sorted(b for b in (_num(x) for x in breakpoints) if b is not None)
    shown = [percentile_of(v, bps) for v in (_num(x) for x in values) if v is not None]
    if not shown or not bps:
        return math.nan, math.nan, len(shown)
    return statistics.fmean(shown), statistics.median(shown), len(shown)


@dataclass
class Result:
    season: object
    metric: str
    key: str
    n: int
    value_p50: float
    ladder_p50: float
    mean_shown: float
    median_shown: float
    verdict: str
    note: str = ""


def _season(row: dict):
    s = row.get("season", row.get("year"))
    f = _num(s)
    return int(f) if f is not None and f == int(f) else s


def check(
    values: list[dict],
    ladder: list[dict],
    mapping: dict,
    *,
    season=None,
    tol: float = 4.0,
    side_col: str | None = None,
    side_tol: float = 25.0,
) -> list[Result]:
    """One Result per (season, display metric) for seasons present in both inputs."""
    if not ladder:
        raise ValueError("ladder is empty")
    for metric, key in mapping.items():
        if key not in ladder[0]:
            raise ValueError(f"ladder has no column {key!r}")
        if values and metric not in values[0]:
            raise ValueError(f"values have no column {metric!r}")
    if not any("season" in r or "year" in r for r in ladder[:1]):
        # A per-season ladder file (cfb_percentiles_2025.csv) carries no season column.
        if season is None:
            raise ValueError("ladder has no season/year column: pass --season for a per-season ladder file")
        ladder = [{**r, "season": season} for r in ladder]
    seasons = sorted({_season(r) for r in values} & {_season(r) for r in ladder}, key=str)
    if season is not None:
        seasons = [s for s in seasons if str(s) == str(season)]
    if not seasons:
        # Checking nothing must never read as "ok".
        raise ValueError(
            f"no season in both inputs (values: {sorted({str(_season(r)) for r in values})[:5]}, "
            f"ladder: {sorted({str(_season(r)) for r in ladder})[:5]})"
        )
    out = []
    for s in seasons:
        vrows = [r for r in values if _season(r) == s]
        lrows = [r for r in ladder if _season(r) == s]
        for metric, key in mapping.items():
            bps = [r[key] for r in lrows]
            vals = [r[metric] for r in vrows]
            mean, median, n = mean_shown(vals, bps)
            nums = [v for v in (_num(x) for x in vals) if v is not None]
            lnums = [v for v in (_num(x) for x in bps) if v is not None]
            vp50 = statistics.median(nums) if nums else math.nan
            lp50 = statistics.median(lnums) if lnums else math.nan
            if n == 0 or not lnums:
                out.append(
                    Result(s, metric, key, n, vp50, lp50, mean, median, "NO-DATA")
                )
                continue
            gap = abs(mean - MATCHED)
            verdict = "MISMATCH" if gap > tol else ("WATCH" if gap > tol / 2 else "OK")
            note = ""
            if side_col:  # more specific than MISMATCH: it names the orientation class
                sides = {}
                for flag in (0, 1):
                    sv = [r[metric] for r in vrows if _num(r.get(side_col)) == flag]
                    sides[flag] = mean_shown(sv, bps)[0]
                if (
                    not any(math.isnan(x) for x in sides.values())
                    and abs(sides[1] - sides[0]) > side_tol
                ):
                    verdict = "SIDE-ASYMMETRY"
                    note = f"{side_col}=1 shows {sides[1]:.1f}, {side_col}=0 shows {sides[0]:.1f}"
            out.append(
                Result(s, metric, key, n, vp50, lp50, mean, median, verdict, note)
            )
    return out


@dataclass
class SplitResult:
    overall: str
    parts: list
    n: int
    share_summing: float
    verdict: str


def split_sums(
    rows: list[dict], overall: str, parts: list[str], *, eps: float = 1e-6
) -> SplitResult:
    """Flag parts that add up to the overall rate on most rows: each part was divided by the WHOLE population.

    Rates on their own denominators combine as a weighted mean, which lies between the parts, never at their sum.
    """
    n = hits = 0
    for r in rows:
        o = _num(r.get(overall))
        ps = [_num(r.get(p)) for p in parts]
        if o is None or any(p is None for p in ps) or o == 0:
            continue
        n += 1
        hits += abs(sum(ps) - o) <= eps * max(1.0, abs(o))
    share = hits / n if n else math.nan
    verdict = "NO-DATA" if n == 0 else ("SPLIT-SUMS" if share > 0.5 else "OK")
    return SplitResult(overall, parts, n, share, verdict)


def _read(path: str) -> list[dict]:
    p = Path(path)
    if p.suffix.lower() in (".parquet", ".pq"):
        try:
            import polars as pl
        except ImportError:
            raise SystemExit(
                f"{path}: reading parquet needs polars (uv run --with polars ...) or pass a CSV"
            ) from None
        return pl.read_parquet(p).to_dicts()
    with p.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _pairs(spec: str) -> dict:
    out = {}
    for item in spec.replace("\n", ",").split(","):
        item = item.strip()
        if item:
            a, sep, b = item.partition("=")
            if not sep:
                raise ValueError(f"--map item {item!r} is not display=key")
            out[a.strip()] = b.strip()
    return out


def _fmt(x) -> str:
    return (
        "nan"
        if isinstance(x, float) and math.isnan(x)
        else (f"{x:.4g}" if isinstance(x, float) else str(x))
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--values", required=True)
    ap.add_argument("--ladder", required=True)
    ap.add_argument(
        "--map",
        required=True,
        help="display=key pairs, comma-separated, or @file with one per line",
    )
    ap.add_argument("--season")
    ap.add_argument(
        "--tol",
        type=float,
        default=4.0,
        help="MISMATCH when mean shown is further than this from 49.5",
    )
    ap.add_argument(
        "--side-tol",
        type=float,
        default=25.0,
        help="SIDE-ASYMMETRY when the two sides' mean shown differ by more than this; home-field advantage alone moves "
        "them ~10-15 apart (CFB 2025 yards/play: 55 vs 40), an orientation bug pins one side near 0 or 100",
    )
    ap.add_argument(
        "--side-col",
        help="0/1 column (e.g. home): flag a gap in mean shown between the two sides",
    )
    ap.add_argument(
        "--split", action="append", default=[], help="overall=part1+part2 (repeatable)"
    )
    a = ap.parse_args(argv)
    try:
        spec = (
            Path(a.map[1:]).read_text(encoding="utf-8")
            if a.map.startswith("@")
            else a.map
        )
        mapping = _pairs(spec)
        values, ladder = _read(a.values), _read(a.ladder)
        results = check(
            values, ladder, mapping, season=a.season, tol=a.tol, side_col=a.side_col, side_tol=a.side_tol
        )
        splits = []
        for s in a.split:
            overall, _, rest = s.partition("=")
            splits.append(
                split_sums(
                    values, overall.strip(), [p.strip() for p in rest.split("+")]
                )
            )
    except (ValueError, OSError) as e:  # a bad map, a missing column or an unreadable file: exit 2, no traceback
        print(f"ladder_parity: {e}", file=sys.stderr)
        return 2
    print(
        "season\tdisplay\tladder_key\tn\tvalue_p50\tladder_p50\tmean_shown\tmedian_shown\tverdict\tnote"
    )
    for r in results:
        print(
            "\t".join(
                _fmt(x)
                for x in (
                    r.season,
                    r.metric,
                    r.key,
                    r.n,
                    r.value_p50,
                    r.ladder_p50,
                    r.mean_shown,
                    r.median_shown,
                    r.verdict,
                    r.note,
                )
            )
        )
    for s in splits:
        print(
            f"split {s.overall} = {' + '.join(s.parts)}: {s.verdict} (parts sum to the whole on "
            f"{_fmt(100 * s.share_summing)}% of {s.n} rows)"
        )
    bad = [r for r in results if r.verdict in ("MISMATCH", "SIDE-ASYMMETRY")] + [
        s for s in splits if s.verdict == "SPLIT-SUMS"
    ]
    print(f"VERDICT: {'mismatch' if bad else 'ok'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
