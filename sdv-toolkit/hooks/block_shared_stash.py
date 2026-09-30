#!/usr/bin/env python3
"""PreToolUse(Bash) guard: block mutating `git stash` in a repo with >1 worktree.

`git stash` is ONE stack per repository, shared by every worktree. Parallel
sessions popped each other's stashes three times (GOP 2026-09-28, sdv-py
2026-09-30) and silently cross-contaminated worktrees. `list`/`show` are
read-only and allowed. Fails open (exit 0) on any parse or git error.
"""

import json
import os
import re
import shlex
import subprocess
import sys

MUTATING = {
    "push",
    "save",
    "pop",
    "apply",
    "drop",
    "clear",
    "branch",
    "store",
    "create",
}
WRAPPERS = {"sudo", "command", "exec", "env", "time", "nohup"}
PUNCT = set("();<>|&")
ASSIGN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


def segments(command):
    """Split a shell command into simple-command token lists (quote-aware)."""
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    segs, cur, skip = [], [], False
    for tok in lex:
        if skip:
            skip = False
        elif tok and set(tok) <= PUNCT:
            if "<" in tok or ">" in tok:  # redirect: drop its fd and its target
                if cur and cur[-1].isdigit():
                    cur.pop()
                skip = True
            else:
                segs.append(cur)
                cur = []
        else:
            cur.append(tok)
    segs.append(cur)
    return [s for s in segs if s]


def stash_targets(command, cwd):
    """Yield the repo dir of every mutating `git stash` invocation."""
    here = cwd
    for seg in segments(command):
        i = 0
        while i < len(seg) and (ASSIGN.match(seg[i]) or seg[i] in WRAPPERS):
            i += 1
        seg = seg[i:]
        if not seg:
            continue
        if seg[0] in ("cd", "pushd"):
            if len(seg) > 1 and seg[1] != "-":
                here = os.path.join(here, os.path.expanduser(seg[1]))
            continue
        if os.path.basename(seg[0]) not in ("git", "git.exe"):
            continue
        repo, i = here, 1
        while i < len(seg) and seg[i].startswith("-"):
            if seg[i] == "-C" and i + 1 < len(seg):
                repo = os.path.join(repo, os.path.expanduser(seg[i + 1]))
                i += 2
            elif seg[i] in ("-c", "--git-dir", "--work-tree", "--namespace"):
                i += 2
            else:
                i += 1
        if i >= len(seg) or seg[i] != "stash":
            continue
        rest = seg[i + 1 :]
        if not rest or rest[0].startswith("-") or rest[0] in MUTATING:
            yield repo


def worktrees(repo):
    out = subprocess.run(
        ["git", "-C", repo, "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if out.returncode != 0:
        return []
    return [
        line[9:] for line in out.stdout.splitlines() if line.startswith("worktree ")
    ]


def main():
    data = json.loads(sys.stdin.read())
    command = (data.get("tool_input") or {}).get("command") or ""
    if "stash" not in command:
        return 0
    cwd = data.get("cwd") or os.getcwd()
    for repo in stash_targets(command, cwd):
        trees = worktrees(repo)
        if len(trees) > 1:
            sys.stderr.write(
                "BLOCKED: `git stash` is shared by all %d worktrees of %s — parallel "
                "sessions can pop each other's changes. Set work aside with a WIP commit "
                "on your branch (git commit -m 'wip') or a scratch worktree instead.\n"
                % (len(trees), trees[0])
            )
            return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # fail open: never break an unrelated command
        sys.exit(0)
