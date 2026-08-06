---
name: sdv-learn
description: Use when a durable finding surfaces mid-session that should outlive the session — a gotcha with a reproducible detection test, a convention that differs by repo, a failure mode, a method insight, or a routing correction. Triages whether it belongs in the toolkit at all (durable org knowledge), in the memory system (personal preference, program state), or nowhere (session-specific, or already recorded in the repo). Then picks the surface — an agent lens, a skill reference file, sdv-conventions plus its override table, or a hook when the violation is mechanically pattern-matchable — writes the finding WITH its detection test, updates catalog.json, and hands back the mirror-and-publish sequence. Invoke for "remember this for next time", "capture this gotcha", "add this to the toolkit", "this should be a rule", "we keep hitting this", or "update the skill with what we just learned".
---

# sdv-learn — promote a session finding into the toolkit

## Step 1 — Triage (this is the whole value; over-capture is the failure mode)

| The finding is | Goes to |
|---|---|
| durable org knowledge — a rule that will apply again in another repo | the toolkit (continue to Step 2) |
| a personal/workflow preference, or program state | the memory system, NOT the toolkit |
| already recorded in code, git history, or a CLAUDE.md | nowhere — say so and stop |
| specific to this session's task | nowhere — say so and stop |

Declining is a correct outcome. A toolkit that absorbs every observation
becomes unreadable, which recreates the discovery problem it exists to solve.

Worked decline: "the cfb_ratings module lives in sportsdataverse/cfb/" is a
fact already recorded by the repo's own directory structure — no reproducible
gotcha, no cross-repo rule, nothing that survives a `grep`. Decline it.

## Step 2 — Pick the surface

| Kind of finding | Surface |
|---|---|
| a gotcha with a detection test | an agent lens, or a skill's failure-modes reference |
| a method or data-source insight | the relevant skill's `references/` |
| a repo rule | `sdv-conventions` (+ `hooks/sdv-overrides.tsv` if repo-specific) |
| a mechanically pattern-matchable violation | a **hook**, not prose |
| general R / ML / library guidance | a routing-table row pointing upstream, NOT restated prose |

## Step 3 — Write it with its test

Every failure-mode entry ships the assertion that would have caught it, not
just a description. "Watch out for X" is not a finding; "assert Y changed"
is.

Worked examples (all three surfaced during this consolidation and would have
been re-derived next time without a landing spot):

1. **`git mv` stages the destination with the SOURCE's bytes.** A post-move
   edit not re-`git add`ed commits stale content and shows as a pure rename.
   Detection: `git show --stat HEAD` must not show `| 0` for a file you also
   edited.
2. **`git commit -- <pathspec>` scopes OUT `git mv`-staged deletions**,
   leaving the old file alive alongside the new one.
   Detection: after a pathspec-scoped commit that included a move, `git
   status` must show no leftover staged deletion for the old path.
3. **A merge can preserve every *concept* while dropping every runnable
   artifact.** A line-count delta looks healthy while the actual code is
   gone. Detection: grep for identifiers that only exist in code (`def
   parse_`, `test_*`) — never trust a line-count delta alone.

## Step 4 — Update catalog.json

Every skill or agent directory needs a matching `catalog.json` row —
`tools/check_catalog.py` fails the build otherwise. Append a row, don't
hand-format the whole file:

```bash
cd /c/Users/saiem/Documents/GitHub-Data/sdv-dev/sportsdataverse-org/sdv-toolkit
python - <<'PY'
import json, pathlib
p = pathlib.Path("catalog.json")
c = json.loads(p.read_text(encoding="utf-8"))
c["entries"].append({
    "name": "<name>", "kind": "skill",  # or "agent" / "hook"
    "purpose": "<one line>",
    "archetypes": ["all"],
})
p.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")
PY
python tools/check_catalog.py .
```

If the finding is a hook instead of a skill/agent, add it to `hooks.json`
and the catalog row's `kind` is `"hook"` — there is no on-disk directory
check for hooks, only the catalog row.

## Guardrails

- Never write to the plugin cache (`~/.claude/plugins/cache/...`). Primary
  checkout and mirror only.
- Never add a skill or agent without a `catalog.json` row — CI rejects it.
- Never restate upstream guidance; add a routing row instead.

## Step 5 — Hand back the sync sequence

Changes do not take effect until the plugin is republished and the session
restarts. Output these commands for the user to run:

    cd /c/Users/saiem/Documents/GitHub-Data/sdv-dev/sportsdataverse-org
    # bump sdv-toolkit/.claude-plugin/plugin.json "version", then:
    python sdv-toolkit/tools/render.py
    git add -- sdv-toolkit .claude-plugin && git commit -m "feat(toolkit): <finding>"
    git push
    # mirror (separate repository):
    cp -r sdv-toolkit/* /c/Users/saiem/Documents/GitHub-Data/sdv-dev/dotfiles_saiemgilani/claude/plugins/sdv-toolkit/
    cd /c/Users/saiem/Documents/GitHub-Data/sdv-dev/dotfiles_saiemgilani && git add -- claude/plugins/sdv-toolkit && git commit -m "chore(plugins): sync sdv-toolkit" && git push
    # then, by full path (claude is not on PATH in the VSCode-extension shell):
    "$(cygpath -u "$LOCALAPPDATA")/Programs/claude/claude.exe" plugin update sdv-toolkit
    # then restart the session
