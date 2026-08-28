#!/usr/bin/env python3
"""Render the ``## Automation & status`` block of an SDV data-repo README.

WHY THIS EXISTS
---------------
A 2026-08-28 survey of all 42 ``*-raw``/``*-data`` repos found that NOT ONE shows
whether its automation is alive. The only generated block anywhere is a datasets
table. A reader cannot tell, from any README in the org, whether the pipeline ran
last night or died in March.

Everything in this block is derivable -- workflow schedules from the ``cron:``
lines, last-run from the Actions API, release tags and publish dates and asset
counts from the Releases API. Hand-maintaining it across 20 repos guarantees it
goes stale; that is what this script prevents.

THE TWO RULES THIS SCRIPT ENFORCES
----------------------------------
1. **The status block is LIVE DATA and must stay outside the ``--check`` drift
   comparison.** Every successful publish changes it. A repo that gates on it
   reddens CI on its own success. ``--check`` here therefore verifies only that
   the MARKERS exist and the block parses -- never that its contents match.

2. **An offline run must preserve the committed block or refuse -- never blank
   it.** Because of rule 1, a wipe is invisible to the drift gate: a regen
   without API access would replace real dates with em dashes, ``--check`` would
   pass, and the damaged README would commit clean. This already happened once in
   this org (an offline docs regen blanked 14 real "Last published" dates). So
   when the API is unreachable this script exits non-zero with an explanation and
   writes nothing, unless ``--keep-on-offline`` is passed, which carries the
   committed block forward verbatim.

USAGE
-----
    python render_readme_status.py --repo sportsdataverse/nfl-raw          # stdout
    python render_readme_status.py --repo <r> --readme README.md --write   # in place
    python render_readme_status.py --repo <r> --readme README.md --check   # markers only

VENDORING
---------
Source of truth is ``sdv-toolkit/tools/`` in the ``sportsdataverse/.github``
repo. Vendor it per repo (never read a sibling checkout at CI time) and record
the refresh command in the repo's CLAUDE.md, matching the convention already used
for loader-schema fixtures.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

BEGIN = "<!-- BEGIN GENERATED: status -->"
END = "<!-- END GENERATED: status -->"

#: Month numbers for rendering a cron month field in words.
_MONTHS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


class OfflineError(RuntimeError):
    """The GitHub API was unreachable, so live fields cannot be refreshed."""


def gh_api(path: str) -> Any:
    """Call the GitHub REST API via the ``gh`` CLI.

    REST deliberately, not GraphQL: the GraphQL quota is metered separately and
    is routinely exhausted in this org, which takes `gh pr`/`gh release` down
    while REST still works.

    Args:
        path: API path, e.g. ``repos/<owner>/<name>/releases``.

    Returns:
        The decoded JSON body.

    Raises:
        OfflineError: When the call fails for any reason. The caller decides
            whether that is fatal; this function never fabricates a result.
    """
    proc = subprocess.run(
        ["gh", "api", path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise OfflineError(f"gh api {path} failed: {proc.stderr.strip()[:200]}")
    try:
        # No --paginate anywhere here: every endpoint used returns a SINGLE
        # object (`releases/tags/<t>`, `workflows/<f>/runs?per_page=1`).
        # --paginate concatenates responses, which for objects yields `}{` --
        # unparseable, and it surfaced as a misleading "offline" error.
        return json.loads(proc.stdout.strip())
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise OfflineError(f"gh api {path} returned unparseable JSON: {exc}") from exc


def describe_cron(expr: str) -> str:
    """Render a cron expression in words.

    ``0 9 * 8 *`` reads as "daily 09:00 UTC in Aug" -- which is the point. A
    schedule nobody can read is a schedule nobody audits, and the month field is
    exactly where season windows hide (a December range that stops on the 20th
    silently drops the bowls).

    Args:
        expr: A five-field cron expression.

    Returns:
        A human-readable description, or the raw expression if it does not parse.
    """
    parts = expr.split()
    if len(parts) != 5:
        return f"`{expr}`"
    minute, hour, dom, month, dow = parts

    when = f"{int(hour):02d}:{int(minute):02d} UTC" if hour.isdigit() and minute.isdigit() else f"`{expr}`"

    if month == "*":
        months = "year-round"
    else:
        nums: list[int] = []
        for piece in month.split(","):
            # Cron permits step values (`1-12/2`, `*/6`); ignoring the step
            # silently rendered "Jan-Dec" for a schedule that fires every other
            # month, which is a worse lie than printing the raw expression.
            step = 1
            if "/" in piece:
                piece, _, raw_step = piece.partition("/")
                step = int(raw_step) if raw_step.isdigit() and int(raw_step) > 0 else 1
            if piece == "*":
                nums.extend(range(1, 13)[::step])
            elif "-" in piece:
                lo, hi = piece.split("-")
                nums.extend(range(int(lo), int(hi) + 1)[::step])
            elif piece.isdigit():
                nums.append(int(piece))
        if not nums:
            return f"`{expr}`"
        # Only abbreviate to a RANGE when the set is actually contiguous. A
        # stepped schedule (`1-12/2`) rendered as "Jan-Nov" reads as every month
        # from January to November when it really fires six times, every other
        # month -- a readable lie, which is worse than the raw expression.
        nums = sorted(set(nums))
        contiguous = len(nums) > 1 and nums == list(range(nums[0], nums[-1] + 1))
        if len(nums) == 1:
            months = _MONTHS.get(nums[0], month)
        elif contiguous:
            months = f"{_MONTHS[nums[0]]}-{_MONTHS[nums[-1]]}"
        else:
            months = ", ".join(_MONTHS[n] for n in nums)

    if dom == "*":
        days = "daily"
    elif "-" in dom:
        days = f"days {dom}"
    else:
        days = f"day {dom}"

    tail = "" if dow == "*" else f", dow {dow}"
    return f"{days} {when} in {months}{tail}"


def workflow_rows(repo: str, wf_dir: Path) -> list[str]:
    """One table row per workflow: badge, schedule in words, last run.

    Reads schedules from the local workflow files rather than the API, because
    the ``cron:`` line is the authority on intent; the API only knows what fired.

    Args:
        repo: ``owner/name``.
        wf_dir: Path to ``.github/workflows``.

    Returns:
        Rendered markdown table rows.
    """
    rows: list[str] = []
    for wf in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
        text = wf.read_text(encoding="utf-8")
        crons = re.findall(r"^\s*-\s*cron:\s*['\"]?([^'\"#\n]+)", text, re.M)
        schedule = "; ".join(describe_cron(c.strip()) for c in crons) if crons else "on push / PR / dispatch"

        badge = f"[![{wf.name}](https://github.com/{repo}/actions/workflows/{wf.name}/badge.svg)](https://github.com/{repo}/actions/workflows/{wf.name})"
        try:
            runs = gh_api(f"repos/{repo}/actions/workflows/{wf.name}/runs?per_page=1")
            items = runs.get("workflow_runs", []) if isinstance(runs, dict) else []
            last = items[0]["updated_at"][:10] if items else "never run"
        except OfflineError:
            raise
        rows.append(f"| {badge} | {schedule} | {last} |")
    return rows


def release_rows(release_repo: str, tags: list[str]) -> list[str]:
    """One row per release tag: asset count, total size, last publish.

    Asset count is not decoration. A badge proves a workflow RAN; only the asset
    count proves it PUBLISHED. The "GREEN job that published nothing" failure
    mode is precisely what a badge alone hides.

    Args:
        release_repo: ``owner/name`` hosting the releases.
        tags: Release tags this repo is responsible for.

    Returns:
        Rendered markdown table rows.
    """
    rows: list[str] = []
    for tag in tags:
        try:
            rel = gh_api(f"repos/{release_repo}/releases/tags/{tag}")
        except OfflineError as exc:
            # A tag that does not exist is a FACT about this repo, not an outage.
            # Treating it as one made a single typo abort the whole render and
            # report "offline", which is both wrong and unactionable.
            if "404" in str(exc) or "Not Found" in str(exc):
                url = f"https://github.com/{release_repo}/releases/tag/{tag}"
                rows.append(f"| [`{tag}`]({url}) | **no release** | — | — |")
                continue
            raise
        assets = rel.get("assets", []) if isinstance(rel, dict) else []
        size_mb = sum(a.get("size", 0) for a in assets) / 1048576
        # The newest ASSET timestamp, not the release's `published_at`. These tags
        # are long-lived and rolling: assets are replaced in place, so
        # `published_at` reports when the tag was first created and is wildly
        # misleading. `espn_cfb_pbp` reads 2023-05-04 by that field while its
        # assets were re-uploaded 2026-08-03 -- a three-year error on exactly the
        # number this table exists to show.
        stamps = [a.get("updated_at") or a.get("created_at") or "" for a in assets]
        newest = max((t for t in stamps if t), default="")
        # No assets means nothing was published, whatever the release says. Falling
        # back to `published_at` here would print a confident date for a tag that
        # shipped nothing -- the "GREEN job that published nothing" mode this table
        # exists to expose.
        published = newest[:10] if newest else "—"
        url = f"https://github.com/{release_repo}/releases/tag/{tag}"
        rows.append(f"| [`{tag}`]({url}) | {len(assets)} | {size_mb:,.1f} MB | {published} |")
    return rows


def render(repo: str, wf_dir: Path, release_repo: str, tags: list[str]) -> str:
    """Render the full marker-delimited status block."""
    out = [BEGIN, "", "| workflow | schedule | last run |", "|---|---|---|"]
    out += workflow_rows(repo, wf_dir) or ["| _none_ | — | — |"]
    if tags:
        out += ["", "| release tag | assets | size | last publish |", "|---|---:|---:|---|"]
        out += release_rows(release_repo, tags)
    out += ["", END]
    return "\n".join(out)


def splice(readme: str, block: str) -> str:
    """Replace the marker block, or append it when the markers are absent."""
    if BEGIN in readme and END in readme:
        head = readme[: readme.index(BEGIN)]
        tail = readme[readme.index(END) + len(END) :]
        return head + block + tail
    sep = "" if readme.endswith("\n\n") else ("\n" if readme.endswith("\n") else "\n\n")
    return f"{readme}{sep}## Automation & status\n\n{block}\n"


def committed_block(readme: str) -> str | None:
    """The block currently in the file, or ``None`` when the markers are absent."""
    if BEGIN in readme and END in readme:
        return readme[readme.index(BEGIN) : readme.index(END) + len(END)]
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", required=True, help="owner/name of the repo being documented")
    ap.add_argument("--readme", type=Path, help="README to update (omit to print to stdout)")
    ap.add_argument("--workflows", type=Path, default=Path(".github/workflows"))
    ap.add_argument("--release-repo", default="sportsdataverse/sportsdataverse-data")
    ap.add_argument("--tags", nargs="*", default=[], help="release tags this repo publishes")
    ap.add_argument("--write", action="store_true", help="write the block back into --readme")
    ap.add_argument(
        "--check",
        action="store_true",
        help="verify the markers exist and the block parses. Deliberately does NOT "
        "compare contents: this block is live data and every publish changes it.",
    )
    ap.add_argument(
        "--keep-on-offline",
        action="store_true",
        help="when the API is unreachable, carry the committed block forward instead "
        "of failing. Without this the script refuses rather than blanking it.",
    )
    args = ap.parse_args(argv)

    if args.check:
        if not args.readme:
            print("--check needs --readme", file=sys.stderr)
            return 2
        text = args.readme.read_text(encoding="utf-8")
        block = committed_block(text)
        if block is None:
            print(f"{args.readme}: missing {BEGIN} / {END} markers", file=sys.stderr)
            return 1
        # Structure, not just "contains a pipe": a block holding `| arbitrary |`
        # would otherwise pass and the gate would certify a table that is not one.
        if "| workflow | schedule | last run |" not in block:
            print(
                f"{args.readme}: status block is missing the workflow table header "
                "(| workflow | schedule | last run |)",
                file=sys.stderr,
            )
            return 1
        if "|---|" not in block.replace(" ", ""):
            print(f"{args.readme}: status block has no table delimiter row", file=sys.stderr)
            return 1
        if re.search(r"\|\s*—\s*\|\s*—\s*\|", block):
            print(
                f"{args.readme}: status block looks BLANKED (em-dash placeholders). "
                "An offline regen probably wiped live values; restore from git.",
                file=sys.stderr,
            )
            return 1
        print(f"{args.readme}: status block present and parseable")
        return 0

    try:
        block = render(args.repo, args.workflows, args.release_repo, args.tags)
    except OfflineError as exc:
        if not (args.keep_on_offline and args.readme and args.readme.exists()):
            print(
                f"cannot refresh status offline: {exc}\n"
                "Refusing to write placeholders -- the drift gate excludes this block "
                "by design, so a blanked table would commit clean. Re-run with API "
                "access, or pass --keep-on-offline to carry the committed block forward.",
                file=sys.stderr,
            )
            return 1
        kept = committed_block(args.readme.read_text(encoding="utf-8"))
        if kept is None:
            print(f"--keep-on-offline: no committed block in {args.readme} to keep", file=sys.stderr)
            return 1
        print(f"offline: kept the committed status block in {args.readme}", file=sys.stderr)
        return 0

    if args.write and args.readme:
        original = args.readme.read_text(encoding="utf-8") if args.readme.exists() else ""
        args.readme.write_text(splice(original, block), encoding="utf-8", newline="\n")
        print(f"wrote status block to {args.readme}")
    else:
        print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
