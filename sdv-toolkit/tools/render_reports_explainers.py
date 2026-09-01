#!/usr/bin/env python3
"""Render the ``## Reports & explainers`` block of an SDV data-repo README.

WHY THIS EXISTS

Measured 2026-08-28 across all 42 ``*-raw``/``*-data`` repos: **no repo had a
Reports & explainers section** (0/42), while several generate exactly the
artifacts it should surface — ``cfbfastR-cfb-data`` regenerates ``docs/models/``
on every run and nothing links to it; six repos carry 15-23 generated
``docs/datasets/*.md`` files reachable only by browsing the tree. The section
is what makes those directories discoverable from the front page.

CONTRACT (mirrors ``render_readme_status.py``)

1. The block lives between ``<!-- BEGIN GENERATED: reports -->`` /
   ``<!-- END GENERATED: reports -->`` markers and is rewritten wholesale.
2. ``--check`` verifies the MARKERS exist and the block parses -- it does NOT
   compare contents. The listing derives from docs trees that a CI sparse
   checkout may not include, and a gate that regenerates against an absent
   payload reds every PR (the drift-gate-absent-payload trap, sdv-data-pipeline
   Step 9).
3. Nothing here is invented: titles come from each file's first ``#`` heading,
   dates from ``git log`` (``uncommitted`` for untracked files), and a repo
   with no artifacts renders an explicit ``_none yet_`` row rather than an
   aspirational table.

WHAT GETS A ROW

- ``models/REGISTRY.md`` -- one row (the model registry).
- ``docs/models/*.md`` / ``docs/datasets/*.md`` / ``docs/validation/*.md`` --
  ONE collapsed row per directory family (link + file count + newest git
  date). These are generated, one-file-per-model/dataset trees; itemizing 20
  rows buries the hand-written material.
- ``docs/*.md`` (top level, non-recursive) -- one row each. These are
  hand-written explainers (``SCRAPING_NOTES.md`` and friends) and deserve
  their own titles.

USAGE

    python render_reports_explainers.py --repo-root .                      # stdout
    python render_reports_explainers.py --repo-root . --readme README.md --write
    python render_reports_explainers.py --repo-root . --readme README.md --check
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED: reports -->"
END = "<!-- END GENERATED: reports -->"

#: Directory families collapsed to a single row: (relative dir, label).
DIR_FAMILIES = [
    ("docs/models", "Model reports & cards"),
    ("docs/datasets", "Dataset docs (column-level, generated)"),
    ("docs/validation", "Validation reports"),
]


def git_date(repo_root: Path, path: Path) -> str:
    """Last commit date (YYYY-MM-DD) for ``path``, or ``uncommitted``.

    ``git log`` rather than mtime: a fresh clone resets every mtime, and the
    question a reader asks is "when did this last change", which is commit
    history. An untracked file is honestly labelled rather than dated.
    """
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "log", "-1", "--format=%as", "--", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    date = proc.stdout.strip()
    return date if proc.returncode == 0 and date else "uncommitted"


def first_heading(path: Path) -> str:
    """The file's own first ``#`` heading, else its stem.

    The file names itself; inventing a description here would violate the
    leave-empty-when-no-store-exists rule the docs pipeline already follows.
    """
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"#+\s+(.*\S)", line)
            if m:
                # Verbatim: stripping emphasis/backtick characters mangles a
                # heading that legitimately STARTS with code (`-raw` -> ...).
                # Inline backticks render fine inside a markdown link label.
                return m.group(1)
    except OSError:
        pass
    return path.stem


def rows(repo_root: Path) -> list[str]:
    """Assemble the table rows for one repo, in a stable order."""
    out: list[str] = []

    registry = repo_root / "models" / "REGISTRY.md"
    if registry.is_file():
        out.append(
            f"| [Model registry](models/REGISTRY.md) | model | artifact | gates | retrain, one row per published model | {git_date(repo_root, registry)} |"
        )

    for rel, label in DIR_FAMILIES:
        d = repo_root / rel
        files = sorted(d.glob("*.md")) if d.is_dir() else []
        files = [f for f in files if f.name.lower() != "readme.md"] or files
        if not files:
            continue
        newest = max((git_date(repo_root, f) for f in files), default="uncommitted")
        out.append(
            f"| [{label}]({rel}/) | {len(files)} files, one per item | {newest} |"
        )

    docs = repo_root / "docs"
    if docs.is_dir():
        for f in sorted(docs.glob("*.md")):
            out.append(
                f"| [{first_heading(f)}](docs/{f.name}) | explainer | {git_date(repo_root, f)} |"
            )

    return out


def render(repo_root: Path) -> str:
    """The full generated block, markers included."""
    body = rows(repo_root)
    lines = [BEGIN, "", "| Report | What it is | Last updated |", "|---|---|---|"]
    if body:
        lines += body
    else:
        lines.append("| _none yet_ | — | — |")
    lines += ["", END]
    return "\n".join(lines)


def committed_block(text: str) -> str | None:
    """The current between-markers block, or None when markers are absent."""
    i, j = text.find(BEGIN), text.find(END)
    if i == -1 or j == -1 or j < i:
        return None
    return text[i : j + len(END)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--repo-root", type=Path, default=Path("."), help="repo working tree to scan"
    )
    ap.add_argument(
        "--readme", type=Path, help="README to update (omit to print to stdout)"
    )
    ap.add_argument(
        "--write", action="store_true", help="write the block back into --readme"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="verify the markers exist and the block parses; contents are NOT compared "
        "(the listing derives from docs trees a sparse checkout may omit)",
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
        if "| Report | What it is | Last updated |" not in block:
            print(
                f"{args.readme}: reports block is missing its table header",
                file=sys.stderr,
            )
            return 1
        print(f"{args.readme}: reports block present and parseable")
        return 0

    block = render(args.repo_root)

    if not args.write or not args.readme:
        print(block)
        return 0

    text = args.readme.read_text(encoding="utf-8")
    old = committed_block(text)
    if old is None:
        print(
            f"{args.readme}: missing {BEGIN} / {END} markers — add them first",
            file=sys.stderr,
        )
        return 1
    args.readme.write_text(text.replace(old, block), encoding="utf-8", newline="")
    print(f"wrote reports block to {args.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
