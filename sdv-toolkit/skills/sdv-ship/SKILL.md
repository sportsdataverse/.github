---
name: sdv-ship
description: Use when landing any change in a SportsDataverse Python repo — the full ship lifecycle, enterable at any phase. Phases: (1) regenerate codegen docs, (2) preflight — ruff, the mypy ratchet, and tests scoped to changed files, (3) commit and verify it landed, (4) push, (5) triage automated review comments from CodeRabbit, Copilot, and Sourcery in parallel with CI rather than after it, (6) confirm the codegen drift gate is green — CI-green means the codegen gate only; remote test jobs are observed and reported, never waited on, (7) merge and confirm state is MERGED before any branch cleanup, (8) retarget and rebase stacked children after a squash-merge, (9) cut a release — version bump, CHANGELOG entry, docs snapshot, GitHub Release tag. Invoke for "ship this", "preflight", "quick check before commit", "lint+type+test my changes", "open the PR", "merge the PR", "land this change", "address the coderabbit comments", "resolve the bot reviews", "handle the copilot review", "merge the stack", "land these stacked PRs", "retarget after merge", "stacked PRs", "cut a release", "release 0.0.x", "ship a new version", "publish to PyPI", "bump the version and release".
---

# Ship a change (sdv-py)

A gated checklist for the full lifecycle of landing a change in
`sportsdataverse-py` — from regenerating docs through a PyPI release. The
ordering is load-bearing: each gate caught a real failure in past sessions
(stale generated docs failing CI, a silently-aborted ruff commit, a branch
deleted before merge was confirmed). **Do not reorder, and do not skip a gate
because a step "looks clean."** Create one todo per phase step and check them
off as you go.

## Phase menu — jump to the phase that matches the ask

| Entry phrase | Start at |
|---|---|
| "preflight", "quick check before commit" | Phase 2 |
| "ship this", "open the PR", "land this change" | Phase 1 |
| "address the coderabbit comments", "resolve the bot reviews" | Phase 5 |
| "merge the stack", "retarget after merge" | Phase 8 |
| "cut a release", "publish to PyPI" | Phase 9 |

Do NOT replay earlier phases when entering mid-flow. State which phase you
are starting at, then proceed forward from there.

## Preconditions

- Run from the repo root (any checkout; do not hard-code a path — use
  `git rev-parse --show-toplevel` if you need it).
- This repo uses **uv**. Prefix Python tooling with `uv run`.
- **Never branch-ship from `main`.** If `git branch --show-current` is `main`,
  create a feature branch first (`git switch -c <type>/<slug>`) before committing.
- Commit convention: **Conventional Commits** (`feat(nfl): ...`, `fix(cfb): ...`).
  **Never add an AI `Co-Authored-By` trailer** (Claude/Copilot/etc.) — the human
  author is the sole attributable contributor. See CLAUDE.md.

## Phase 1 — Regenerate docs

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
   a wrapper function (see Phase 2's new-module check). Regenerating WITH a
   shadow in place silently DROPS the shadowed wrapper from the generated
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

## Phase 2 — Preflight

A quick, scoped sweep that mirrors what CI will check, but only over what you
changed — seconds, not a full `pytest`. Use this for fast inner-loop feedback
before a commit; Phase 3 still runs the full suite as the final gate.

1. **Find changed Python files** (staged + unstaged + untracked):

   ```sh
   # all changed .py (handles renames "old -> new" and space-containing paths)
   git status --porcelain | sed 's/^...//; s/.* -> //' | grep -E '\.py$'
   ```

   **New module? Shadow check first.** If the change ADDS a new
   `sportsdataverse/**/<name>.py`, confirm the filename doesn't collide with an
   existing symbol in the target package (star-imported wrapper, generated
   function, loader). A module that shares a name with a released function
   rebinds the package attribute — existing callers get
   `TypeError: 'module' object is not callable`. This has shipped twice
   (`nba_possessions`, `nfl_standings`):

   ```sh
   grep -rn "\b<name>\b" sportsdataverse/<pkg>/__init__.py
   uv run python -c "import sportsdataverse.<pkg> as p; print(type(getattr(p, '<name>', None)))"
   ```

   If it collides, rename the module file (e.g. `<name>_calc.py`) — the public
   function inside can keep its name; only the filename collides.

2. **Ruff** — format + lint the changed files (the PostToolUse hook already
   formats on edit; this catches anything edited outside Claude):

   ```sh
   uv run ruff format <changed.py ...>
   uv run ruff check <changed.py ...>
   ```

3. **mypy ratchet** — only if a changed file is in the `[tool.mypy] files`
   ratchet in `pyproject.toml`. mypy with no args checks the curated list
   (`follow_imports = "skip"` → sub-second):

   ```sh
   uv run mypy
   ```

4. **Targeted tests** — map each changed module to its test dir and run only
   those, rather than the whole suite. For a changed
   `sportsdataverse/<sport>/<mod>.py`, run `tests/<sport>/`:

   ```sh
   uv run pytest tests/<sport>/ -q
   ```

   If the change is cross-cutting (e.g. `dl_utils.py`, `_common_espn*.py`,
   `config.py`) or the mapping is unclear, fall back to the full suite
   (`uv run pytest -q`) and say so. Live-API tests stay skipped unless
   `SDV_PY_LIVE_TESTS=1`.

   **Always also run the ID / name-matching contract** — a sub-second offline guard
   for the recurring int-vs-str / `id→Utf8` / case-sensitive-regex bug class:

   ```sh
   uv run pytest tests/test_id_conventions.py -q
   ```

5. **Report** a one-line verdict per stage (ruff / mypy / tests: pass|fail) and,
   on any failure, the specific file:line. This is a sanity sweep — surface
   problems, don't auto-fix beyond ruff's own `--fix`.

When preflight is green, proceed to Phase 3 for the full-suite gate and commit.

## Phase 3 — Commit

1. **Run the full test suite.** Not a subset — the whole thing must be green
   before declaring done, even though Phase 2 already ran a scoped pass.

   ```sh
   uv run pytest
   ```

   Live-API tests are gated behind `SDV_PY_LIVE_TESTS=1` and skip by default;
   that's expected. A red suite is a stop-ship — fix before continuing.

2. **Commit — then VERIFY it landed.** Conventional Commits subject, scoped where
   useful. No AI co-author trailer. Split unrelated work into separate commits.
   After every `git commit`, confirm with `git log -1 --oneline` + `git status`
   that HEAD is your new commit and nothing is left half-staged. Two hooks
   silently abort commits while printing mostly-green output: the ruff-format
   hook (rewrites files) and **doctoc** (rewrites any staged README/markdown
   with a TOC). In both cases: re-`git add` the hook-modified files and
   re-commit — never `--no-verify`.

### Phase 3b — Review (mandatory, not optional)

Dispatch, by archetype:

- `sdv-python-reviewer` — always, for any changed `.py`. Pass the lens:
  `polars` for dataframe code, `http` for network code, `parser-contract`
  for an ESPN parser, `docstring` for new public callables.
- `sdv-r-reviewer` — for any changed `.R` / `man/` / `_pkgdown.yml`.
- `sdv-docs-reviewer` — when a returns table or schema changed.

Do not substitute `general-purpose`. If a reviewer reports a finding, fix or
explicitly decline it with a rationale before Phase 4.

## Phase 4 — Push

Push the feature branch and open the PR (or update it):

```sh
git push -u origin HEAD
gh pr create --fill        # or: gh pr view --web  to edit
```

The pre-push hook re-runs the codegen drift gate (~3-5 min), so a push
regularly outlives a 2-minute foreground tool timeout — run it
`run_in_background` and confirm the remote head afterwards
(`git ls-remote origin <branch>`).

## Phase 5 — Bot triage

CodeRabbit (login `coderabbitai` / `coderabbitai[bot]`) and Copilot
(`copilot-pull-request-reviewer[bot]`) post reviews a few minutes after a push /
CI run — **triage them in parallel with Phase 6, not after it**, so review
fixes and the remote CI run overlap instead of serializing. Fetch the
**unresolved** threads, address each, and resolve it. Run this after the PR is
open, before merge.

**Evaluate — do not auto-apply.** Both bots produce false positives, especially
against this repo's *documented* choices. A suggestion that contradicts CLAUDE.md
is a decline-with-citation, not a fix (see Guardrails).

1. **Resolve the PR + repo coordinates.**

   ```sh
   gh pr view --json number,url,headRefName
   gh repo view --json owner,name -q '.owner.login+"/"+.name'   # sportsdataverse/sportsdataverse-py
   ```

2. **List unresolved bot review threads** (verified query — returns thread id +
   the comment's `databaseId` for replies):

   ```sh
   gh api graphql -f query='
   query($owner:String!,$repo:String!,$pr:Int!){
     repository(owner:$owner,name:$repo){
       pullRequest(number:$pr){
         reviewThreads(first:100){ nodes{
           id isResolved isOutdated
           comments(first:10){ nodes{ databaseId author{login} body path line } }
         }}
       }
     }
   }' -F owner=sportsdataverse -F repo=sportsdataverse-py -F pr=<N> \
     --jq '.data.repository.pullRequest.reviewThreads.nodes
           | map(select(.isResolved==false and (.comments.nodes[0].author.login|test("(?i)coderabbit|copilot"))))'
   ```

   For a PR with >100 threads, paginate: add `pageInfo{ hasNextPage endCursor }`
   to `reviewThreads` and loop with `after: <endCursor>` until `hasNextPage` is
   false (a hard-coded `first:100` silently drops the tail).

   Also read the PR-level summary review (CodeRabbit's walkthrough / Copilot's
   overview), which often holds suggestions not attached to a line:

   ```sh
   gh pr view <N> --json reviews \
     --jq '.reviews[] | select(.author.login|test("(?i)coderabbit|copilot")) | {by:.author.login,state,body}'
   ```

3. **Triage each thread comment** into one of:
   - **Valid** → fix in code.
   - **Convention conflict / false positive** → do NOT change; reply citing the
     CLAUDE.md rule (see Guardrails).
   - **Question** → answer in a reply.
   - **Nit** → judgment call; apply if cheap and correct.

4. **Apply the valid fixes**, grouped by file, then re-run Phase 2 (ruff + mypy
   ratchet + targeted tests) so a fix doesn't introduce a regression.

5. **Commit + push.** Conventional-Commit subject, **no AI co-author trailer**
   (the `commit-msg` hook enforces both). Pushing flips the addressed threads to
   `isOutdated`.

   ```sh
   git commit -m "fix(<scope>): address review feedback on <area>"
   git push
   ```

6. **Reply to, then resolve, each thread.** Reply first; resolve only after the
   fix is pushed or the decline is justified.

   - Reply (github MCP `add_reply_to_pull_request_comment`, or REST):

     ```sh
     gh api -X POST repos/sportsdataverse/sportsdataverse-py/pulls/<N>/comments \
       -F in_reply_to=<databaseId> -f body='Fixed in <sha>.'      # or the decline rationale
     ```

   - Resolve the thread (GraphQL mutation, verified shape):

     ```sh
     gh api graphql -f query='mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread{ isResolved } } }' -F id=<threadNodeId>
     ```

   - **CodeRabbit shortcuts** (post as a top-level PR comment):
     `@coderabbitai resolve` resolves all of its own comments at once;
     `@coderabbitai review` triggers a re-review after you push fixes. Use these
     for CodeRabbit-wide actions; use the per-thread GraphQL mutation for Copilot
     or for selective resolution.

7. **Re-request review** if the changes were substantial: `@coderabbitai review`
   (comment) for CodeRabbit, or `request_copilot_review` (github MCP) for Copilot.

8. **Report** a table: `thread | by | path:line | verdict (fixed/declined/answered) | resolved?`.
   Leave genuinely contentious threads unresolved and flag them for a human call.

### Guardrails — decline suggestions that fight CLAUDE.md

When a bot suggestion contradicts a documented repo convention, **decline with a
one-line citation** instead of "fixing" into a regression. Common false positives
here:

- `pl.col(...) == True` / `== False` — intentional for polars boolean masks
  (E712 is suppressed in `pyproject.toml`); do not rewrite to `pl.col(...)` / `~`.
- Polars **1.x** idioms — don't accept reverts to 0.18 API
  (`group_by`/`with_row_index`/`pl.len()`/`how="full"`, etc.).
- Regex with the inline case toggle `(?i)...(?-i:...)` — polars/Rust has **no
  lookaround**; a "use a lookbehind" suggestion is wrong.
- ID-dtype discipline — don't accept an `id -> Utf8` "paper-over" cast.
- Packaging — no `setup.py` / `requirements*.txt` (PEP 621 + uv only).
- Don't resolve a thread you didn't actually address; don't add an AI
  co-author trailer to fix commits (hook-enforced anyway).

## Phase 6 — CI gate

**CI-green means the codegen gate only.** The remote pytest matrix is observed
and reported, never waited on — Phase 3 already ran the full suite locally, so
blocking on a slow/flaky remote matrix just serializes work that Phase 5
should be running in parallel.

```sh
gh pr checks
```

1. **Confirm the codegen drift gate job is green.** This is the required
   signal to proceed to merge. If it's red, read the failing job, fix, and
   loop back to Phase 1.
2. **Observe and report the remaining jobs** (test matrix, docs build, etc.)
   without blocking on them. Distinguish real failures from known repo flakes
   (0-second Vercel previews; live-test timeout races) — call out a flake
   explicitly rather than silently ignoring it.
3. **Two watcher gotchas** carried over from prior incidents: a check run
   started before a re-push can reflect the OLD head (re-fetch after any
   push), and after any merge the PR-branch run is superseded — the
   definitive signal is **main's post-merge run** (`gh run list --branch main`).

If the codegen gate fails, report the failure and stop — do not silently
retry or merge past a red gate.

## Phase 7 — Merge

1. **Merge — only after the codegen drift gate (Phase 6) is green and bot
   threads (Phase 5) are resolved.**

   ```sh
   gh pr merge --squash        # or the project's preferred strategy
   ```

   If the human directs an early merge (`--admin`) past pending/red checks:
   only override a failure you have READ and verified as infra flake (Vercel
   preview deploy, runner DNS), never an unread one — admin merges silently
   accept red required checks (a red codegen gate rode onto main exactly this
   way) — and afterwards confirm main's post-merge run goes green.

2. **Confirm the merge landed, THEN clean up.** Verify before deleting anything:

   ```sh
   gh pr view --json state,mergedAt   # state must be MERGED
   ```

   Only once `state == MERGED`: delete the branch and `git switch main && git pull`.
   **Never delete the branch before this confirmation** — a premature cleanup
   stranded work in a past session.

3. **Write a session note.** Capture what shipped while the context is fresh, so
   the next session (or a compaction recovery) doesn't re-derive it:
   - If the repo has an SDD ledger (`.superpowers/sdd/progress.md`), append one
     entry there: date, branch, PR # + URL, the commit range, gates passed
     (tests/mypy/drift), and any deferred follow-ups.
   - Otherwise write `dev/session-notes/YYYY-MM-DD-<slug>.md` (`dev/` is
     gitignored — working notes, not repo docs).
   - If the ship changed durable cross-session state (a program milestone, a new
     convention, a gotcha worth remembering), also update the memory topic file
     for that program.

## Phase 8 — Stack retarget

Stacked PRs (each branch based on the previous) let phased work ship
reviewably, but every landed parent invalidates its children: SDV repos
squash-merge, so a child branch still carries the parent's now-duplicate
commits and must be rebased, and the codegen drift gate must re-pass at the
child's NEW head. This phase encodes the sequence that avoids the three
failure modes that have actually happened: stale-base drift failures,
hand-merged docs conflicts, and premature branch deletion stranding work.

**Depth cap: ~4.** Beyond that, one bottom-of-stack change costs N rebases +
N drift re-checks. If the stack is deeper, land the bottom before opening
the next PR.

### 1. Map the stack

```sh
gh pr list --state open --json number,title,headRefName,baseRefName \
  --template '{{range .}}{{.number}}\t{{.baseRefName}} <- {{.headRefName}}\t{{.title}}\n{{end}}'
```

Draw the parent graph (base ← head). The **bottom** PR is the one whose base
is `main`. Everything else merges only after its parent.

### 2. Land the bottom PR

Run Phase 6 (ci-gate) then Phase 7 (merge) for the bottom PR. **Do NOT delete
the head branch until `gh pr view <n> --json state` says `MERGED`** —
premature cleanup has stranded work before.

### 3. Retarget + rebase the next child

GitHub auto-retargets children to `main` when the merged head branch is
deleted, but the child branch still CONTAINS the parent's pre-squash
commits. Rebase them away — never merge them forward:

```sh
git fetch origin
git checkout <child-branch>
git rebase --onto origin/main <old-parent-branch> <child-branch>
git push --force-with-lease origin <child-branch>
```

`--force-with-lease` only; never plain `--force`. If the PR didn't
auto-retarget, `gh pr edit <n> --base main` first.

**Conflict rule for generated files:** never hand-merge codegen output or
generated docs. Take either side, finish the rebase, then regenerate —
the regeneration in step 4 makes the tree correct regardless.

### 4. Re-verify at the new head

The drift gate passing at the old head means nothing at the new one:

```sh
uv run python tools/codegen/generate.py && uv run python tools/codegen/generate.py --check
uv run pytest -q   # or Phase 2's scoped preflight
```

Commit any regen delta as its own `chore(docs): regenerate reference docs`
commit. Check `git status` for a silent `uv.lock` re-lock before committing.

### 5. Repeat

The child is now the bottom. Loop steps 2–4 until the stack is flat.

### Quick reference — the three past incidents this prevents

| Incident | Guard |
|---|---|
| Drift gate red after retarget (regenerated at old head) | Step 4 always re-runs `generate.py --check` at the new head |
| Docs merge-conflict hand-resolved wrong | Step 3 conflict rule: take either side, regenerate |
| Branch deleted while PR still open → stranded work | Step 2: verify `state == MERGED` before any cleanup |

## Phase 9 — Release

End-to-end pre-tag sequence for a PyPI release. The actual PyPI publish is
automated by `.github/workflows/python-publish.yml` on the **GitHub Release
`published`** event — so this phase's job is everything *up to and including*
creating that release. Create one todo per numbered step; the ordering matters.

**Preconditions:** work on a branch, not `main` (`git switch -c release/0.0.x`).
The version + CHANGELOG + docs-snapshot land in one PR, then the tag is cut
after merge. Decide the new version by semver bump from the current
`pyproject.toml` `[project] version` (check it — releases have been rapid,
e.g. 0.0.66 → 0.0.69).

1. **Run Phases 1–6 first.** A release must be green: regenerate codegen
   docs (Phase 1), preflight + the full `uv run pytest` (Phases 2–3), push
   and bot-triage (Phases 4–5), and the codegen drift gate (Phase 6). Do not
   proceed on a red suite.

2. **Bump the version** in `pyproject.toml`:

   ```toml
   [project]
   version = "0.0.X"
   ```

   (There is no `setup.py` / `__version__` duplicate — `pyproject.toml` is the
   single source of truth.)

3. **Write the CHANGELOG entry.** Add a new section at the **top** of
   `CHANGELOG.md` (immediately below the doctoc TOC comment block), matching the
   existing shape exactly:

   ```markdown
   ## 0.0.X Release: <Month DD, YYYY>

   ### <SPORT/AREA> — <short title>

   <prose summary of the change, mirroring prior entries>
   ```

   Derive the subsections from the Conventional-Commit subjects since the last
   tag:

   ```sh
   git describe --tags --abbrev=0          # last tag (note the v-prefix convention)
   git log <last-tag>..HEAD --pretty=format:'%s'
   ```

   Do **not** hand-edit the TOC — the `doctoc` pre-commit hook regenerates it,
   and the `sync-docs-changelog` local hook copies `CHANGELOG.md` →
   `docs/src/pages/CHANGELOG.md` automatically on commit.

4. **Freeze the docs snapshot.** Snapshot the live `docs/docs/` tree into a
   frozen per-release archive:

   ```sh
   (cd docs && yarn version:docs 0.0.X)    # subshell: stays at repo root after
   ```

   This writes `docs/versioned_docs/version-0.0.X/`. **Keep `lastVersion:
   'current'` in `docusaurus.config` — never bump it away from `current`**, so
   the live docs always track `main`. (Gotcha: a docs snapshot has triggered a
   **Vercel build heap-OOM** before; if the Vercel deploy fails after this,
   that's the suspect — drop/trim the snapshot rather than loosening anything.)

5. **Commit** everything in one release commit:

   ```sh
   git add pyproject.toml CHANGELOG.md docs/
   git commit -m "chore(release): 0.0.X"
   ```

   (The `commit-msg` hook enforces the Conventional-Commit subject + no AI
   co-author trailer.)

6. **Push, open the PR, confirm the gates, merge** — i.e. finish via Phases
   4–7 (push → bot-triage → ci-gate → confirm `state == MERGED` → cleanup).

7. **Tag the GitHub Release** (this is what triggers PyPI). Match the existing
   tag convention from step 3:

   ```sh
   gh release create v0.0.X --title "0.0.X" \
     --notes "<paste the new CHANGELOG section>"
   ```

   The `publish` workflow builds the sdist+wheel with `uv build` and publishes
   via **PyPI Trusted Publishing (OIDC)** — no token needed.

8. **Verify the publish landed.**

   ```sh
   gh run watch                            # follow the `publish` workflow
   ```

   Confirm the new version appears on <https://pypi.org/project/sportsdataverse/>.
   `workflow_dispatch` is a build-only dry-run; only the Release event publishes.

9. **Downstream pins (if relevant).** If a consumer repo pins a minimum
   sportsdataverse version (e.g. the cfb-raw / nfl-data pipelines), bump the
   pin to `>=0.0.X` in a follow-up.

## Stop conditions (report, don't push through)

- Drift gate (`generate.py --check`) non-zero after regeneration (Phase 1) or
  still red in the codegen gate job (Phase 6).
- Any test failure in the full suite (Phase 3).
- PR `state` not `MERGED` at cleanup time (Phase 7).
- Vercel docs build OOM after a docs snapshot (Phase 9 step 4) — investigate
  the snapshot.
- `publish` workflow failure (Phase 9 step 8) — read the job; do not re-cut a
  tag over a partially-published version (the action's `skip-existing: true`
  protects against dup-file errors, but a wrong version is a wrong version).

In each case: stop, surface the exact output, and wait — do not delete branches,
force-push, or skip hooks (`--no-verify`) to get unstuck.
