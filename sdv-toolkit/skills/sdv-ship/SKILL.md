---
name: sdv-ship
description: Use when shipping a change in sportsdataverse-py (sdv-py) — opening, pushing, or merging a PR. Runs the steps in the correct order (regenerate codegen docs, update changelog/docs/tutorials, lint, full pytest, commit + verify it landed, push, wait for CI green, triage bot reviews CodeRabbit/Sourcery/Copilot, confirm merge, write a session note) and never cleans up a branch before the merge is confirmed. Invoke for "ship this", "open/merge the PR", "land this change", or any end-of-change release flow.
---

# Ship a change (sdv-py)

A gated checklist for landing a change in `sportsdataverse-py`. The ordering is
load-bearing: each gate caught a real failure in past sessions (stale generated
docs failing CI, a silently-aborted ruff commit, a branch deleted before merge
was confirmed). **Do not reorder, and do not skip a gate because a step "looks
clean."** Create one todo per numbered step and check them off as you go.

## Preconditions

- Run from the repo root (any checkout; do not hard-code a path — use
  `git rev-parse --show-toplevel` if you need it).
- This repo uses **uv**. Prefix Python tooling with `uv run`.
- **Never branch-ship from `main`.** If `git branch --show-current` is `main`,
  create a feature branch first (`git switch -c <type>/<slug>`) before committing.
- Commit convention: **Conventional Commits** (`feat(nfl): ...`, `fix(cfb): ...`).
  **Never add an AI `Co-Authored-By` trailer** (Claude/Copilot/etc.) — the human
  author is the sole attributable contributor. See CLAUDE.md.

## Steps

1. **Regenerate generated docs (codegen drift gate).** If the change touched any
   endpoint YAML (`tools/codegen/endpoints/*`), schemas, docstrings, loaders, or
   wrappers, the generated reference subtree is probably stale and **CI will fail
   on it**. Regenerate, then check:

   ```sh
   uv run python tools/codegen/generate.py          # regenerate wrappers + docs
   uv run python tools/codegen/generate.py --check   # must exit 0 (drift gate)
   ```

   If `--check` is non-zero, the generated tree drifted — regenerate and stage
   the result. The same gate runs in CI and the `sdv-codegen` pre-commit hook.

   **Branch head, not per-task.** On a multi-commit / multi-task branch, re-run
   the gate at the FINAL branch head even if it passed mid-branch — later
   commits that add exports or docstrings silently invalidate an earlier
   regeneration (per-task green does not compose; this failed a real
   whole-branch review).

   **Shadow check before regenerating.** If the branch added a new module under
   a package with generated wrappers, first confirm the filename doesn't shadow
   a wrapper function (see `/sdv-preflight`'s new-module check). Regenerating WITH
   a shadow in place silently DROPS the shadowed wrapper from the generated
   `parsed/` module — fix the name first, then regenerate.

2. **Update changelog / docs / tutorials (conditional — skip only if truly N/A).**
   - **User-facing change** (new function, renamed/removed surface, behavior or
     dependency change)? Add a `CHANGELOG.md` entry under the unreleased heading
     (the `sync-docs-changelog` pre-commit hook mirrors it into the docs site).
   - **New/changed public surface**? Check whether the relevant example notebook
     (`examples/notebooks/0X_<sport>_intro.ipynb`) or a hand-authored conceptual
     doc page mentions the old surface — update it. Generated reference pages are
     already handled by step 1; never hand-edit those.
   - Internal-only refactor with zero user-visible effect → note "changelog N/A"
     in the todo and move on. Don't invent an entry for noise.

3. **Lint + format.** The PostToolUse ruff hook formats files as they're edited,
   but run the suite-wide pass before committing so nothing slips through:

   ```sh
   uv run ruff format sportsdataverse/ tools/ .claude/
   uv run ruff check sportsdataverse/ tools/ .claude/
   ```

   A ruff-format hook can **silently abort a commit** — if `git commit` reports
   nothing committed, suspect the pre-commit ruff hook rewrote files; re-`git add`
   and re-commit. Confirm the commit actually landed (`git log -1 --oneline`).

4. **Run the full test suite.** Not a subset — the whole thing must be green
   before declaring done.

   ```sh
   uv run pytest
   ```

   Live-API tests are gated behind `SDV_PY_LIVE_TESTS=1` and skip by default;
   that's expected. A red suite is a stop-ship — fix before continuing.

5. **Commit — then VERIFY it landed.** Conventional Commits subject, scoped where
   useful. No AI co-author trailer. Split unrelated work into separate commits.
   After every `git commit`, confirm with `git log -1 --oneline` + `git status`
   that HEAD is your new commit and nothing is left half-staged. Two hooks
   silently abort commits while printing mostly-green output: the ruff-format
   hook (rewrites files) and **doctoc** (rewrites any staged README/markdown
   with a TOC). In both cases: re-`git add` the hook-modified files and
   re-commit — never `--no-verify`.

6. **Push** the feature branch and **open the PR** (or update it):

   ```sh
   git push -u origin HEAD
   gh pr create --fill        # or: gh pr view --web  to edit
   ```

7. **Wait for CI to go green.** Do not merge on a yellow/pending or red run.

   ```sh
   gh pr checks --watch
   ```

   If CI fails, read the failing job, fix, and loop back to the relevant step
   (often step 1 for docs drift or step 4 for tests). Report the failure — do
   not silently retry.

8. **Address automated reviews (CodeRabbit / Sourcery / Copilot).** They post a
   few minutes after CI. Triage + resolve the unresolved bot threads before
   merging — run `/sdv-address-bot-reviews` (fix the valid ones, decline
   convention-conflicts with a CLAUDE.md citation, then reply + resolve each
   thread). Skip only if no bot review landed.

9. **Merge — only after CI is green and bot threads are resolved.**

   ```sh
   gh pr merge --squash        # or the project's preferred strategy
   ```

10. **Confirm the merge landed, THEN clean up.** Verify before deleting anything:

    ```sh
    gh pr view --json state,mergedAt   # state must be MERGED
    ```

    Only once `state == MERGED`: delete the branch and `git switch main && git pull`.
    **Never delete the branch before this confirmation** — a premature cleanup
    stranded work in a past session.

11. **Write a session note.** Capture what shipped while the context is fresh, so
    the next session (or a compaction recovery) doesn't re-derive it:
    - If the repo has an SDD ledger (`.superpowers/sdd/progress.md`), append one
      entry there: date, branch, PR # + URL, the commit range, gates passed
      (tests/mypy/drift), and any deferred follow-ups.
    - Otherwise write `dev/session-notes/YYYY-MM-DD-<slug>.md` (`dev/` is
      gitignored — working notes, not repo docs).
    - If the ship changed durable cross-session state (a program milestone, a new
      convention, a gotcha worth remembering), also update the memory topic file
      for that program.

## Stop conditions (report, don't push through)

- Drift gate (`generate.py --check`) non-zero after regeneration.
- Any test failure in the full suite.
- CI red or still pending.
- PR `state` not `MERGED` at cleanup time.

In each case: stop, surface the exact output, and wait — do not delete branches,
force-push, or skip hooks (`--no-verify`) to get unstuck.
