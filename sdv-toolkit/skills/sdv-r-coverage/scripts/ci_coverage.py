#!/usr/bin/env python3
"""Per-file coverage from a test-coverage CI run, grouped by function family.

    python ci_coverage.py --repo owner/name --run <run-id> --src <local checkout> [--out cov.csv]

covr's print() lists `R/<file>: <pct>%` lines in the "Test coverage" step log. This
reads them through `gh run view --log`, weights each file by its non-blank,
non-comment line count from the checkout, and prints the zero-coverage weight per
family (the prefix before the first underscore: espn_, mlb_, ncaa_, ...). Rank work by
the lines in that table, not by file count -- one 6,500-line family beats twenty
30-line files.
"""

import argparse
import csv
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

LINE = re.compile(r"\s(R/[\w.\-]+\.R): ([0-9.]+)%")


def code_lines(path):
    n = 0
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if s and not s.startswith("#"):
            n += 1
    return n


def family(file):
    stem = pathlib.Path(file).stem
    return stem.split("_")[0] if "_" in stem else stem


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--repo", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--src", required=True, type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    a = ap.parse_args(argv)

    log = subprocess.run(
        ["gh", "run", "view", a.run, "-R", a.repo, "--log"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    total = re.search(r"Coverage: ([0-9.]+)%", log)
    rows = {}
    for m in LINE.finditer(log):
        rows[m.group(1)] = float(m.group(2))
    if not rows:
        print("no per-file coverage lines found in the run log", file=sys.stderr)
        return 1

    table, fam_zero, fam_all = [], defaultdict(int), defaultdict(int)
    for f, pct in sorted(rows.items()):
        p = a.src / f
        n = code_lines(p) if p.exists() else 0
        table.append((f, pct, n))
        fam_all[family(f)] += n
        if pct == 0:
            fam_zero[family(f)] += n
    if a.out:
        with a.out.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["file", "pct", "lines"])
            w.writerows(table)

    print(
        f"overall: {total.group(1) if total else '?'}%   files: {len(rows)}   "
        f"at 0%: {sum(1 for _, p, _ in table if p == 0)}"
    )
    print(f"{'family':<20}{'0% lines':>10}{'all lines':>11}")
    for fam, z in sorted(fam_zero.items(), key=lambda kv: -kv[1])[:15]:
        print(f"{fam:<20}{z:>10}{fam_all[fam]:>11}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
