---
name: sdv-ship
description: Use when landing any change in a SportsDataverse Python repo — the full ship lifecycle, enterable at any phase. Phases: (1) regenerate codegen docs, (2) preflight — ruff, the mypy ratchet, and tests scoped to changed files, (3) commit and verify it landed, (4) push, (5) triage automated review comments from CodeRabbit, Copilot, and Sourcery in parallel with CI rather than after it — starting by PROVING a review happened at all, since six distinct green bot signals (zero unresolved threads, a `pass` check that means rate-limited, a `skipping` Sourcery budget exhaustion, a review predating the head, an empty review shell, an unreviewed draft) each read as reviewed while nothing was; the surviving test is `review.commit_id == head.sha` AND a non-empty body AND zero unresolved threads, then reading the body for the Outside-diff-range findings that never became threads, (6) confirm the codegen drift gate is green — CI-green means the codegen gate only; remote test jobs are observed and reported, never waited on, (7) merge and confirm state is MERGED before any branch cleanup, (8) retarget and rebase stacked children after a squash-merge, (9) cut a release — version bump, CHANGELOG entry, docs snapshot, GitHub Release tag. Invoke for "ship this", "preflight", "quick check before commit", "lint+type+test my changes", "open the PR", "merge the PR", "land this change", "address the coderabbit comments", "resolve the bot reviews", "handle the copilot review", "merge the stack", "land these stacked PRs", "retarget after merge", "stacked PRs", "cut a release", "release 0.0.x", "ship a new version", "publish to PyPI", "bump the version and release".
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

   **The CI job is `--check` PLUS the codegen tests.** `tests/codegen/` runs
   inside that same gate, so it travels with the regen even when Phase 2 is
   otherwise scoping tests to changed files — a hardcoded wrapper-count
   assertion in `tests/codegen/` reddened CI after a perfectly clean `--check`:

   ```sh
   uv run pytest tests/codegen/ -q
   ```

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
`run_in_background` and confirm the remote head afterwards. **A backgrounded
push's own stdout is not evidence — and neither is the mere existence of the
remote ref.** `git ls-remote` proves a ref exists, which a prior or concurrent
push also satisfies; compare its SHA against the commit you meant to push:

```sh
expected=$(git rev-parse HEAD)
remote=$(git ls-remote origin "refs/heads/<branch>" | awk 'NR==1{print $1}')
test "$remote" = "$expected" && echo "PUSHED $expected" || echo "NOT YOURS: $remote"
``` With many worktrees sharing one
`.git`, concurrent background pushes interleave stdout into each other's logs:
two 2026-09-01 push logs reported *another session's* branch name at exit 0
while the branch under push was still absent. Nothing was damaged, but the log
described someone else's fast-forward. Relatedly, a
`fatal: full write to remote helper failed: Broken pipe` can mean the push
**succeeded** server-side — check `ls-remote` before retrying, or you pay
another 5-10 min hook run and get a `reference already exists` error that
invites exactly the wrong conclusion.

**`gh pr create` / `gh pr edit --body-file` can fail on the projects-classic
GraphQL deprecation / rate limit** while REST is fine — and piping their output
through `grep` hides it, costing a silently-unapplied PR body (three times in
two days). Use REST and read the body back:

```sh
# create — build the JSON first; --rawfile keeps markdown intact
jq -n --rawfile b body.md '{title:"...",head:"...",base:"main",body:$b}' > pr.json
gh api -X POST repos/{owner}/{repo}/pulls --input pr.json --jq '{number,url:.html_url}'

# edit — same shape, then READ IT BACK; a silent no-op is the failure mode
jq -n --rawfile b body.md '{body:$b}' > patch.json
gh api -X PATCH repos/{owner}/{repo}/pulls/<N> --input patch.json >/dev/null
diff <(gh api repos/{owner}/{repo}/pulls/<N> --jq '.body') body.md && echo "body OK"
```

**"files were modified by this hook" push failures (2026-09-01, both shipped):**
the pre-push hooks run `uv run …`, so anything that makes `uv run` rewrite a
file fails the push even when the check itself passes. Two real causes:
(a) a release bumped `pyproject.toml`'s version WITHOUT committing the
re-locked `uv.lock` — every later `uv run` re-wrote the lock's own `version`
line until someone committed it; (b) a stray pull-merge polluted the branch so
the hook's regen produced drift. Diagnose by reading which hook says
"files were modified", `git diff` the file it touched, and commit the
legitimate change (a 1-line lock sync is a fix, not noise) — never bypass with
`--no-verify`. The tree must be CLEAN immediately after commit for the push to
survive the hooks.

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

### Step 0 — prove a review actually happened

**"Reviewed" is a claim, and every cheap signal for it lies.** On 2026-09-02 six
distinct green signals each read as reviewed while nothing had been reviewed:

| Green signal | What it actually meant |
|---|---|
| 0 unresolved review threads | CodeRabbit's **"Outside diff range comments"** live in the PR-level review *body* and create no thread — cfb-data #59 carried a MAJOR data-integrity finding there while `reviewThreads` returned 0 |
| A `pass` check from CodeRabbit | body read **"Review rate limited"** — zero reviews on the PR |
| A green Sourcery check | conclusion `skipping`: the **weekly 250,000-diff-character budget** was exhausted fleet-wide. Not red, not a pass |
| A review object exists | it **predates the head** — #59's newest review was 18:23Z against a 18:59Z head, so "0 unresolved" meant "not re-reviewed" |
| A review object exists, at head | an **empty shell** — a COMMENTED review with a zero-length body, posted next to the rate-limit notice |
| Every bot check green/neutral on a draft | CodeRabbit says **"Draft PR not reviewed"** in a collapsed comment, not in a check. Un-draft first, then expect a review |

**The one test that survives all six** — run it before triaging anything, and
again before merge:

```sh
gh pr view <N> --json headRefOid,isDraft \
  --jq '{head:.headRefOid, draft:.isDraft}'
gh api repos/{owner}/{repo}/pulls/<N>/reviews \
  --jq '.[] | select(.user.login|test("(?i)coderabbit|copilot|sourcery"))
       | {by:.user.login, state, at:.submitted_at, sha:.commit_id, body_len:(.body|length)}'
```

…and the unresolved-thread count, which those two calls do NOT return — run the
paginated `reviewThreads` query from step 2 below and count
`isResolved == false`. A PR can pass everything above with a live finding still
open.

A PR is **reviewed** only when, for at least one bot:
`review.commit_id == head.sha` **AND** `body_len > 0` **AND** unresolved
threads == 0. Anything short of all three is **unreviewed** — say so, don't let
a green board stand in for it.

Then read the body of every qualifying review for the findings that never
became threads:

```sh
gh api repos/{owner}/{repo}/pulls/<N>/reviews --jq '.[].body' \
  | grep -nE 'Outside diff range|Nitpick comments|Additional comments|Duplicate comments'
```

The headline count undercounts: a 2026-09-02 review said *"Actionable comments
posted: 1"* and carried 2 — the hidden one was the Major.

**When no real review can be obtained** (both bots were down most of
2026-09-02): review the diff by hand, and **record that rationale as a PR
comment** naming what you checked. Do not merge on a green board alone; do not
block a small, tested fix indefinitely either.

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

3. **Enumerate the findings INSIDE each thread body before replying.** GitHub
   renders a multi-finding comment as one thread, so a single reply plus a
   resolve closes the *thread*, not every finding in it. hoopR-nba-stats-data
   #35's thread on `nba_stats_synergyplaytypes.R:68` held two Majors; the
   second stayed live in the code after the thread was resolved. **Resolving is
   a claim about the whole thread** — answer each finding explicitly.

   Two corollaries: a bot's stated *mechanism* can be wrong while its *finding*
   is right (reproduce the shape before editing — one 2026-09-02 finding named
   the wrong cause and the real one was live at five sites), and a bot's
   "verified by static analysis" block is evidence of a script it ran, not of
   its conclusion. Verify the finding against the **current head**, then grep
   for siblings that share the pattern — a refactor landing mid-review
   relocates and multiplies the defect.

4. **Triage each thread comment** into one of:
   - **Valid** → fix in code.
   - **Convention conflict / false positive** → do NOT change; reply citing the
     CLAUDE.md rule (see Guardrails).
   - **Question** → answer in a reply.
   - **Nit** → judgment call; apply if cheap and correct.

5. **Apply the valid fixes**, grouped by file, then re-run Phase 2 (ruff + mypy
   ratchet + targeted tests) so a fix doesn't introduce a regression.

6. **Commit + push.** Conventional-Commit subject, **no AI co-author trailer**
   (the `commit-msg` hook enforces both). Pushing flips the addressed threads to
   `isOutdated`.

   ```sh
   git commit -m "fix(<scope>): address review feedback on <area>"
   git push
   ```

7. **Reply to, then resolve, each thread.** Reply first; resolve only after the
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

8. **Re-request review** if the changes were substantial: `@coderabbitai review`
   (comment) for CodeRabbit, or `request_copilot_review` (github MCP) for Copilot.

9. **Report** a table: `thread | by | path:line | verdict (fixed/declined/answered) | resolved?`.
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
3. **Three watcher gotchas** carried over from prior incidents: a check run
   started before a re-push can reflect the OLD head (re-fetch after any
   push); after any merge the PR-branch run is superseded — the definitive
   signal is **main's post-merge run** (`gh run list --branch main`); and a
   settle condition of `gh pr checks | grep -qv pending` fires when ANY line
   is non-pending (a `skipping` live-test row settles it instantly, 2026-09-01)
   — loop until the count of `pending` rows is ZERO instead:
   `pend=$(gh pr checks N | grep -c $'\tpending\t'); [ "$pend" -eq 0 ] && break`.

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

3. **A merge can land between a review being requested and it arriving, and a
   squash can drop a conflict resolution.** Three of four PRs in one
   2026-09-02 batch were squash-merged mid-flight; one review with a real bug
   arrived four minutes after its merge. Two consequences:

   - **Re-check `.merged` and `.headRefOid` immediately before pushing any
     review fix.** Pushing to a branch GitHub deleted on merge silently
     *recreates* the ref and the fix goes nowhere. If you see `* [new branch]`
     for a branch you believed existed, the PR merged underneath you — branch
     off fresh `main` and open a successor PR. (A deleted base branch also
     auto-closes its stacked child, and a force-push to the child makes that
     close permanent — GitHub refuses `state=open` afterwards. Rebuild and
     cross-link; do not expect to reopen.)
   - **Re-run the suite against `origin/main` after the merge.** That is the
     only check that covers what actually shipped — a conflict resolution is a
     code change and a squash can silently drop it.

4. **Write a session note.** Capture what shipped while the context is fresh, so
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

   **Then immediately `uv lock` and commit `uv.lock` WITH the bump.** The
   lockfile records the package's own version; 0.1.4 shipped without the
   re-lock, and for the next day every `uv run` rewrote `uv.lock`'s version
   line — which made every pre-push hook fail with "files were modified by
   this hook" (2026-09-01). The bump and its lock travel in one commit.

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
