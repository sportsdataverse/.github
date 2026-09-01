#!/usr/bin/env python3
"""Render the ``## Repository layout`` tree for an SDV ``-raw`` / ``-data`` repo.

Answers "where do I look?" without cloning: a two-level directory tree derived
from the working copy, annotated from a shared vocabulary so the same directory
name reads the same way in all 34 repos.

Contract, matching the sibling renderers in this directory:

1. The block lives between ``<!-- BEGIN GENERATED: layout -->`` /
   ``<!-- END GENERATED: layout -->`` markers and is rewritten wholesale.
2. ``--check`` verifies the MARKERS exist and the block parses -- it does NOT
   compare contents. A sparse or blobless checkout legitimately omits
   directories, and a gate that failed on that would make every partial clone
   red. Contents are refreshed by re-running with ``--write``.
3. Output is deterministic: entries are sorted, nothing is timestamped, and a
   directory with more children than the cap is summarised rather than dumped
   (a season tree holds thousands of files and would bury the README).

Usage::

    python render_readme_layout.py --repo-root .
    python render_readme_layout.py --repo-root . --readme README.md --write
    python render_readme_layout.py --repo-root . --readme README.md --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED: layout -->"
END = "<!-- END GENERATED: layout -->"

# Children shown per directory before the remainder is summarised.
# Children shown before the remainder is summarised. Code directories get a
# larger budget on purpose: the numbered stage scripts ARE the documentation
# here, and hiding stage 09 behind a summary line defeats the section.
MAX_CHILDREN_DATA = 8
MAX_CHILDREN_CODE = 16

# Never descend into or list these -- tooling caches and local agent state.
SKIP_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "node_modules",
    "renv",
    "packrat",
    ".Rproj.user",
    ".git",
    ".omc",
    ".claude",
    ".understand-anything",
    ".cache",
    ".ipynb_checkpoints",
}

# Directories whose FILES carry the meaning (the numbered stage scripts). For
# every other directory only child directories are listed -- a data tree's files
# are thousands of per-game payloads, and naming eight of them tells you nothing.
CODE_DIRS = {"python", "R", "scripts", "tools", "src", "tests", "ops"}

# One vocabulary so `logs/` means the same thing in all 34 repos.
GLOSSARY = {
    "python": "Python pipeline stages, numbered in build order",
    "R": "R pipeline stages and publish toolchain",
    "scripts": "bash drivers (the daily/weekly entry points)",
    "tests": "test suite",
    "tools": "repo-local helper scripts",
    "docs": "explainers, model reports and dataset docs",
    "logs": "per-run logs (gitignored where large)",
    "ops": "cron definitions and runbooks",
    "models": "model artifacts, cards and the registry",
    "dev": "working notes, not part of the pipeline",
    "data": "committed datasets",
    "figures": "generated figures",
    "themes": "plot themes",
    "man": "generated R documentation",
    "features": "feature-set definitions",
}


def is_visible_dir(p: Path) -> bool:
    return p.is_dir() and not p.name.startswith(".") and p.name not in SKIP_NAMES


def is_visible_file(p: Path) -> bool:
    return p.is_file() and not p.name.startswith(".")


def annotate(name: str) -> str:
    """The shared-vocabulary comment for a directory name, or ''."""
    return GLOSSARY.get(name, "")


def children_of(d: Path) -> tuple[list[Path], int]:
    """Level-2 entries for ``d`` plus the count elided by the cap."""
    subdirs = sorted(
        (p for p in d.iterdir() if is_visible_dir(p)), key=lambda p: p.name
    )
    entries: list[Path] = list(subdirs)
    if d.name in CODE_DIRS:
        files = sorted(
            (
                p
                for p in d.iterdir()
                if is_visible_file(p) and p.suffix in {".py", ".R", ".sh"}
            ),
            key=lambda p: p.name,
        )
        entries += files
    cap = MAX_CHILDREN_CODE if d.name in CODE_DIRS else MAX_CHILDREN_DATA
    # Eliding a single entry costs the same line as showing it, and a reader
    # who sees "… 1 more" has to clone to learn what it was. Never hide one.
    if len(entries) == cap + 1:
        return entries, 0
    shown = entries[:cap]
    return shown, len(entries) - len(shown)


def tree_lines(repo_root: Path) -> list[str]:
    """The fenced tree body, root line included."""
    root_name = repo_root.resolve().name
    lines = [f"{root_name}/"]
    tops = sorted(
        (p for p in repo_root.iterdir() if is_visible_dir(p)), key=lambda p: p.name
    )
    for i, top in enumerate(tops):
        last_top = i == len(tops) - 1
        elbow, spine = ("└── ", "    ") if last_top else ("├── ", "│   ")
        note = annotate(top.name)
        lines.append(f"{elbow}{top.name}/{f'   # {note}' if note else ''}")
        try:
            shown, elided = children_of(top)
        except OSError:  # unreadable directory -- report the parent, not a crash
            continue
        for j, child in enumerate(shown):
            last_child = j == len(shown) - 1 and elided == 0
            c_elbow = "└── " if last_child else "├── "
            suffix = "/" if child.is_dir() else ""
            lines.append(f"{spine}{c_elbow}{child.name}{suffix}")
        if elided:
            lines.append(f"{spine}└── … {elided} more")
    return lines


def render(repo_root: Path) -> str:
    """The full generated block, markers included."""
    body = tree_lines(repo_root)
    return "\n".join([BEGIN, "", "```", *body, "```", "", END])


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
        "(a sparse checkout legitimately omits directories)",
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
        if "```" not in block:
            print(
                f"{args.readme}: layout block is missing its fenced tree",
                file=sys.stderr,
            )
            return 1
        print(f"{args.readme}: layout block present and parseable")
        return 0

    block = render(args.repo_root)

    if not args.write or not args.readme:
        print(block)
        return 0

    # Refuse rather than commit a tree asserting the repo has no directories. A
    # sparse or blobless checkout produces exactly that, and it would read as
    # fact -- the same failure the status block's offline-regen rule guards
    # against. Printing to stdout stays allowed; only writing is refused.
    if len(tree_lines(args.repo_root)) <= 1:
        print(
            f"{args.repo_root}: no directories visible — refusing to write an "
            "empty tree (sparse checkout? run from a full clone)",
            file=sys.stderr,
        )
        return 1

    # Preserve the file's existing newline convention. Reading with universal
    # newlines and writing back with newline="" silently converts a CRLF README
    # end-to-end, turning a one-section edit into a whole-file diff nobody can
    # review.
    # Path.read_text() only grew a newline= parameter in 3.13; the workflow runs
    # 3.12, so go through Path.open(), which has accepted it all along.
    with args.readme.open(encoding="utf-8", newline="") as fh:
        raw = fh.read()
    eol = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")

    old = committed_block(text)
    if old is None:
        print(
            f"{args.readme}: missing {BEGIN} / {END} markers — add them first",
            file=sys.stderr,
        )
        return 1
    updated = text.replace(old, block).replace("\n", eol)
    args.readme.write_text(updated, encoding="utf-8", newline="")
    print(f"wrote layout block to {args.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
