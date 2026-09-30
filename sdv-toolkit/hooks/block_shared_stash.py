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
    "import",
}
WRAPPERS = {"sudo", "command", "exec", "env", "time", "nohup"}
PUNCT = set("();<>|&")
ASSIGN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
SHELLS = {"bash", "sh", "zsh", "dash"}
SHELL_C = re.compile(r"-[a-z]*c[a-z]*$")  # bash -c / -lc / -ec
REPO_OPTS = ("-C", "--git-dir", "--work-tree")


def segments(command):
    """Split a shell command into simple-command token lists (quote-aware).

    Subshell parens come through as "(" / ")" markers so a `cd` inside one
    does not leak into the commands after it.
    """
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    items, cur, skip = [], [], False
    for tok in lex:
        if skip:
            skip = False
        elif tok and set(tok) <= PUNCT:
            if "<" in tok or ">" in tok:  # redirect: drop its fd and its target
                if cur and cur[-1].isdigit():
                    cur.pop()
                skip = True
            else:
                items.append(cur)
                cur = []
                items.extend(c for c in tok if c in "()")
        else:
            cur.append(tok)
    items.append(cur)
    return [s for s in items if s]


def stash_targets(command, cwd):
    """Yield (dir, repo-selecting git options, env) per mutating `git stash`."""
    here, saved = cwd, []
    for seg in segments(command):
        if seg == "(":
            saved.append(here)
            continue
        if seg == ")":
            here = saved.pop() if saved else here
            continue
        i = 0
        while i < len(seg) and (
            ASSIGN.match(seg[i])
            or os.path.basename(seg[i]) in WRAPPERS
            or (i and seg[i].startswith("-"))
        ):
            i += 1
        env = dict(t.split("=", 1) for t in seg[:i] if ASSIGN.match(t))
        seg = seg[i:]
        if not seg:
            continue
        name = os.path.basename(seg[0])
        if name in ("cd", "pushd"):
            if len(seg) > 1 and seg[1] != "-":
                here = os.path.join(here, os.path.expanduser(seg[1]))
            continue
        if name in SHELLS:
            flag = next((j for j, t in enumerate(seg) if SHELL_C.match(t)), None)
            if flag is not None and flag + 1 < len(seg):
                yield from stash_targets(seg[flag + 1], here)
            continue
        if name not in ("git", "git.exe"):
            continue
        opts, i = [], 1
        while i < len(seg) and seg[i].startswith("-"):
            if seg[i] in REPO_OPTS and i + 1 < len(seg):
                opts += [seg[i], os.path.expanduser(seg[i + 1])]
                i += 2
            elif seg[i].split("=")[0] in REPO_OPTS:
                opts.append(seg[i])
                i += 1
            elif seg[i] in ("-c", "--namespace"):
                i += 2
            else:
                i += 1
        if i >= len(seg) or seg[i] != "stash":
            continue
        rest = seg[i + 1 :]
        if not rest or rest[0].startswith("-") or rest[0] in MUTATING:
            yield here, opts, env


def worktrees(here, opts, env):
    out = subprocess.run(
        ["git", *opts, "worktree", "list", "--porcelain"],
        cwd=here,
        env={**os.environ, **env},
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
    for target in stash_targets(command, cwd):
        trees = worktrees(*target)
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
