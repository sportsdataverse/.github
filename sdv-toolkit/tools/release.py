#!/usr/bin/env python3
"""Release and mirror helper for the sdv-toolkit plugin.

Line-ending rules: files the org repo's index stores as CRLF (README.md,
plugin.json, marketplace.json, ...) stay CRLF after a render; the dotfiles
mirror is LF (its .gitattributes forces eol=lf). A file is text when it
decodes as UTF-8 and has no NUL byte; binaries are copied as-is. The mirror
source is the git-tracked files under sdv-toolkit/; it deletes only files the
dest checkout tracks. Tool state (.git/, .venv/, .omc/, __pycache__/,
.pytest_cache/, .ruff_cache/, *.pyc) is never mirrored, and the same paths in
the mirror are never touched.

Subcommands (run from sdv-toolkit/):
  bump (patch|minor|major|X.Y.Z)   rewrite plugin.json's version only
  render                           tools/render.py, then restore CRLF
  check                            catalog, render --check, tools + hooks tests
  mirror --dest DIR [--dry-run] [--allow-non-git]
                                   make DIR an LF copy of sdv-toolkit/
  verify --dest DIR                diff sdv-toolkit/ vs DIR ignoring CR
  next-steps [--dotfiles DIR]      print the commit/PR/plugin-update commands
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

TOOLKIT = Path(__file__).resolve().parents[1]
REPO = TOOLKIT.parent
PLUGIN_JSON = TOOLKIT / ".claude-plugin" / "plugin.json"
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".omc",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}

_VERSION = re.compile(rb'("version"\s*:\s*")(\d+\.\d+\.\d+)(")')
_BARE_LF = re.compile(rb"(?<!\r)\n")


# -- bump --------------------------------------------------------------------


def next_version(old: str, spec: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", spec):
        return spec
    major, minor, patch = (int(x) for x in old.split("."))
    if spec == "major":
        return "%d.0.0" % (major + 1)
    if spec == "minor":
        return "%d.%d.0" % (major, minor + 1)
    if spec == "patch":
        return "%d.%d.%d" % (major, minor, patch + 1)
    raise ValueError("bump wants patch|minor|major|X.Y.Z, got %r" % spec)


def bump(path: Path, spec: str) -> str:
    data = path.read_bytes()
    m = _VERSION.search(data)
    old = m.group(2).decode() if m else None
    if old is None or json.loads(data)["version"] != old:
        raise ValueError("no top-level x.y.z version found in %s" % path)
    new = next_version(old, spec)
    path.write_bytes(data[: m.start(2)] + new.encode() + data[m.end(2) :])
    print("%s -> %s" % (old, new))
    return new


# -- render ------------------------------------------------------------------


def _is_text(data: bytes) -> bool:
    """UTF-8 decodable and no NUL byte."""
    if b"\0" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def crlf_paths(repo: Path) -> list[str]:
    """Repo-relative paths whose index copy has CRLF line endings."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--eol"],
        cwd=repo,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    paths = []
    for entry in filter(None, out.split("\0")):
        info, _, rel = entry.partition("\t")
        if info.split()[0] == "i/crlf":
            paths.append(rel)
    return paths


def restore_crlf(repo: Path, render_step: Callable[[], object]) -> list[str]:
    """Run render_step, then put CRLF back on CRLF-indexed files it left LF."""
    targets = crlf_paths(repo)
    restored = []
    try:
        render_step()
    finally:  # a render that writes LF and then fails must not leave LF behind
        for rel in targets:
            path = repo / rel
            if not path.is_file():
                continue
            data = path.read_bytes()
            if not _BARE_LF.search(data):
                continue
            if not _is_text(data):
                print("skipped CRLF restore (binary): %s" % rel)
            else:
                path.write_bytes(data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
                restored.append(rel)
    return restored


def _run_render() -> None:
    r = subprocess.run(
        [sys.executable, "tools/render.py"],
        cwd=TOOLKIT,
        capture_output=True,
        text=True,
        check=True,
    )
    sys.stdout.write(r.stdout)


# -- check -------------------------------------------------------------------

CHECK_STEPS = [
    ("check_catalog", ["tools/check_catalog.py", "."]),
    ("render --check", ["tools/render.py", "--check"]),
    ("tools tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
    ("hooks tests", ["-m", "unittest", "discover", "-s", "hooks", "-p", "test_*.py"]),
]


def check() -> int:
    failed = 0
    for name, args in CHECK_STEPS:
        r = subprocess.run(
            [sys.executable, *args], cwd=TOOLKIT, capture_output=True, text=True
        )
        print("%s  %s" % ("ok  " if r.returncode == 0 else "FAIL", name))
        if r.returncode:
            failed += 1
            sys.stderr.write(r.stdout + r.stderr)
    return 1 if failed else 0


# -- mirror / verify ---------------------------------------------------------


def _is_excluded(rel: str) -> bool:
    parts = rel.split("/")
    return rel.endswith(".pyc") or any(p in EXCLUDED_DIRS for p in parts)


def _git(cwd: Path, *args: str) -> str | None:
    """stdout of `git <args>` run in cwd (or its nearest existing parent)."""
    while not cwd.exists():
        cwd = cwd.parent
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def _zlist(out: str | None) -> list[str]:
    return [p for p in (out or "").split("\0") if p and not _is_excluded(p)]


def _toplevel(path: Path) -> Path | None:
    out = _git(path, "rev-parse", "--show-toplevel")
    return Path(out.strip()).resolve() if out else None


def _files(root: Path) -> dict[str, Path]:
    """{posix relpath: path} for every non-excluded file on disk under root."""
    found = {}
    if not root.is_dir():
        return found
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix()
            if not _is_excluded(rel):
                found[rel] = path
    return found


def _source_files(src: Path) -> dict[str, Path]:
    """The git-tracked, non-excluded files under src."""
    out = _git(src, "ls-files", "-z")
    if out is None:
        raise ValueError("mirror source %s is not a git checkout" % src)
    rels = _zlist(out)
    # is_file() follows a symlink, so a tracked link would copy a file from outside src
    links = [rel for rel in rels if (src / rel).is_symlink()]
    if links:
        raise ValueError("mirror source tracks symlinks: %s" % ", ".join(links))
    return {rel: src / rel for rel in rels if (src / rel).is_file()}


def _owned(dest: Path) -> dict[str, Path]:
    """Dest files the mirror may delete: the tracked ones, if dest is in git."""
    files = _files(dest)
    if files and _toplevel(dest) is not None:
        tracked = set(_zlist(_git(dest, "ls-files", "-z")))
        files = {rel: p for rel, p in files.items() if rel in tracked}
    return files


def _warn_uncommitted(src: Path) -> None:
    untracked = _zlist(_git(src, "ls-files", "-z", "--others", "--exclude-standard"))
    changed = _zlist(_git(src, "diff", "--name-only", "-z", "--relative", "HEAD"))
    if not (untracked or changed):
        return
    sys.stderr.write(
        "warning: %s is not a clean checkout; untracked files are NOT mirrored, "
        "uncommitted edits ARE (working-tree content):\n" % src
    )
    for label, rels in (("untracked", untracked), ("modified ", changed)):
        for rel in rels:
            sys.stderr.write("  %s  %s\n" % (label, rel))


def _lf(data: bytes) -> bytes:
    """CRLF -> LF for text (UTF-8, no NUL); binaries unchanged."""
    return data.replace(b"\r\n", b"\n") if _is_text(data) else data


def _exec_bits(path: Path) -> int:
    return path.stat().st_mode & 0o111


def _roots(path: Path) -> set[str]:
    return set((_git(path, "rev-list", "--max-parents=0", "HEAD") or "").split())


def _guard(src: Path, dest: Path, allow_non_git: bool) -> None:
    # resolving a symlinked dest would pass every check below while writing into its target
    if dest.is_symlink():
        raise ValueError("--dest %s is a symlink; pass the real directory" % dest)
    s, d = src.resolve(), dest.resolve()
    if d.name != s.name:
        raise ValueError("--dest must end in /%s, got %s" % (s.name, dest))
    if d == s or s in d.parents or d in s.parents:
        raise ValueError("--dest %s overlaps the source %s" % (dest, src))
    dest_top = _toplevel(d)
    if dest_top is None:
        if not allow_non_git:
            raise ValueError(
                "--dest %s is not inside a git work tree (pass --allow-non-git)" % dest
            )
        return
    # Same toplevel = the org checkout itself; shared root commits = another
    # worktree or clone of the org repo. Neither is the dotfiles mirror.
    if dest_top == _toplevel(s) or _roots(s) & _roots(d):
        raise ValueError("--dest %s is a checkout of the source repo" % dest)


def _no_symlinks(dest: Path, rels) -> None:
    """Refuse a path whose file or any parent below dest is a symlink: following it would write outside dest."""
    for rel in rels:
        p = dest
        for part in Path(rel).parts:
            p = p / part
            if p.is_symlink():
                raise ValueError(
                    "--dest %s is a symlink; refusing to follow it outside %s"
                    % (p, dest)
                )


def mirror(
    src: Path, dest: Path, dry_run: bool = False, allow_non_git: bool = False
) -> tuple[list[str], list[str], list[str]]:
    _guard(src, dest, allow_non_git)
    want = _source_files(src)
    _no_symlinks(dest, set(want) | set(_owned(dest)))
    _warn_uncommitted(src)
    added, updated = [], []
    for rel, path in sorted(want.items()):
        out = dest / rel
        if not out.is_file():
            added.append(rel)
        elif out.read_bytes() != _lf(path.read_bytes()) or _exec_bits(
            out
        ) != _exec_bits(path):
            updated.append(rel)
    owned = _owned(dest)
    deleted = sorted(set(owned) - set(want))

    verb = "would " if dry_run else ""
    for label, rels in (("add", added), ("update", updated), ("delete", deleted)):
        for rel in rels:
            print("%s%s %s" % (verb, label, rel))
    print(
        "%sadded %d, updated %d, deleted %d%s"
        % (
            "" if dry_run else "mirror: ",
            len(added),
            len(updated),
            len(deleted),
            " (dry run)" if dry_run else "",
        )
    )
    if dry_run:
        return added, updated, deleted

    for rel in deleted:
        owned[rel].unlink()
    for dirpath, _, _ in sorted(os.walk(dest), key=lambda w: -len(w[0])):
        d = Path(dirpath)
        rel = d.relative_to(dest).as_posix()
        if d != dest and not _is_excluded(rel) and not any(d.iterdir()):
            d.rmdir()
    for rel in added + updated:
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(_lf(want[rel].read_bytes()))
        shutil.copymode(want[rel], out)
    return added, updated, deleted


def verify(src: Path, dest: Path) -> int:
    """Report every path mirror() would add, update or delete."""
    if dest.is_symlink():
        raise ValueError("--dest %s is a symlink; pass the real directory" % dest)
    want, owned = _source_files(src), _owned(dest)
    # a tree mirror() refuses must not verify clean
    _no_symlinks(dest, set(want) | set(owned))
    problems = []
    for rel in sorted(set(want) | set(owned)):
        out = dest / rel
        if rel not in want:
            problems.append("extra    %s" % rel)
        elif not out.is_file():
            problems.append("missing  %s" % rel)
        elif _lf(want[rel].read_bytes()) != _lf(out.read_bytes()):
            problems.append("differs  %s" % rel)
        elif _exec_bits(want[rel]) != _exec_bits(out):
            problems.append("mode     %s" % rel)
    for line in problems:
        print(line)
    return 1 if problems else 0


# -- next-steps --------------------------------------------------------------


def next_steps(dotfiles: str) -> str:
    version = json.loads(PLUGIN_JSON.read_bytes())["version"]
    claude = "/root/.local/bin/claude"
    win = '"$(cygpath -u "$LOCALAPPDATA")/Programs/claude/claude.exe"'
    return "\n".join(
        [
            "# 1. org repo (sportsdataverse/.github) -- stage explicit paths only",
            "git -C %s status --short" % REPO,
            "git -C %s add <paths>" % REPO,
            'git -C %s commit -m "chore(sdv-toolkit): release %s"' % (REPO, version),
            "git -C %s push -u origin HEAD" % REPO,
            "gh pr create --repo sportsdataverse/.github --fill",
            "",
            "# 2. dotfiles mirror (saiemgilani/dotfiles)",
            "python %s mirror --dest %s/claude/plugins/sdv-toolkit"
            % (Path(__file__).resolve(), dotfiles),
            "python %s verify --dest %s/claude/plugins/sdv-toolkit"
            % (Path(__file__).resolve(), dotfiles),
            "git -C %s switch -c sdv-toolkit-%s" % (dotfiles, version),
            "git -C %s add claude/plugins/sdv-toolkit" % dotfiles,
            'git -C %s commit -m "chore(sdv-toolkit): mirror %s '
            '(sportsdataverse/.github#<PR>)"' % (dotfiles, version),
            "git -C %s push -u origin HEAD" % dotfiles,
            "gh pr create --repo saiemgilani/dotfiles --fill",
            "",
            "# 3. plugin update, after both PRs merge",
            "# droplet:",
            "%s plugin marketplace update sportsdataverse && "
            "%s plugin update sdv-toolkit@sportsdataverse" % (claude, claude),
            "# Windows (Git Bash):",
            "%s plugin update sdv-toolkit" % win,
            "# then restart the session",
        ]
    )


# -- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="release.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bump").add_argument("spec", help="patch|minor|major|X.Y.Z")
    sub.add_parser("render")
    sub.add_parser("check")
    m = sub.add_parser("mirror")
    m.add_argument("--dest", required=True, type=Path)
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--allow-non-git", action="store_true")
    sub.add_parser("verify").add_argument("--dest", required=True, type=Path)
    sub.add_parser("next-steps").add_argument("--dotfiles", default="<dotfiles>")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "bump":
            bump(PLUGIN_JSON, args.spec)
        elif args.cmd == "render":
            for rel in restore_crlf(REPO, _run_render):
                print("restored CRLF: %s" % rel)
        elif args.cmd == "check":
            return check()
        elif args.cmd == "mirror":
            mirror(TOOLKIT, args.dest, args.dry_run, args.allow_non_git)
        elif args.cmd == "verify":
            return verify(TOOLKIT, args.dest)
        else:
            print(next_steps(args.dotfiles))
    except ValueError as e:
        sys.stderr.write("release.py: %s\n" % e)
        return 2
    except subprocess.CalledProcessError as e:
        sys.stderr.write("release.py: %s failed (exit %d)\n" % (e.cmd, e.returncode))
        for stream in (e.stdout, e.stderr):
            if stream:
                sys.stderr.write(stream if isinstance(stream, str) else stream.decode())
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
