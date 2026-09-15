---
name: sdv-review-pr
description: Use when asked to review a pull request, branch, or diff in a SportsDataverse org repo or a saiemgilani repo (game-on-paper-app, sdv-swagger, Sports-Research-Papers, dotfiles), including the data platform (sdv-db, sdv-orch, sportsdataverse-web) and outside-contributor PRs — before merge, before approving, or to audit a merged PR after a regression. Invoke for "review PR #N", "review this PR", "code review <PR url>", "is this safe to merge", "second opinion on this diff", "check akeaswaran's PR", "what did this PR break". Not for triaging bot comments on your own PR (use sdv-ship Phase 5) or sweeping the whole org queue (use sdv-triage).
---

# sdv-review-pr — review a pull request the way this org actually breaks

The expensive SDV defects are not style. They are a publish job that goes green
having published nothing, a season key shifted twice, a fix that misses the public
twin page, a lock that doesn't contain the symbol the code calls, a test that cannot
fail, and a claim nobody measured. A review is a set of **verified findings at the PR
head, each with a failure scenario** — not an impression of the diff.

This review is often the only real gate: no repo in scope has required status checks,
admins bypass required reviews, and bot reviews are frequently rate-limited, stale, or
empty (72 PRs merged with an unresolved Major/Critical bot thread; 113 got their bot
review only after merging).

## Authorization

| Tier | Action | Authorization |
|---|---|---|
| 0 | Read the PR, export the head to a scratch tree, run local gates with outward paths cut (Phase 5), write the report | Autonomous |
| 1 | Post a review or inline comments, request changes, approve, label, push a fix, merge | **Explicit confirmation, per PR** |

Never approve your own PR (post a COMMENT review). Never push to a contributor's
branch. Posted text carries no AI attribution footer or trailer.

## Phase 0 — Context

```sh
python3 <this-skill-dir>/scripts/pr_context.py <N | owner/repo#N | URL> [-R owner/repo] --out "$SCRATCH/reviews"
```

It writes `context.md` (state, head SHA, checks, bot-review proof, archetypes → which
references to load, file-level and line-level **signals**), `context.json`, and
`diff.patch`. Signals are leads tied to rule ids, never findings.

If `gh` is unavailable, gather by hand: `gh pr view N -R o/r --json …`, `gh pr diff`,
`gh api repos/o/r/pulls/N/{files,reviews}`, and the `reviewThreads` GraphQL query.

Branch on state:
- **Merged/closed** → post-merge audit: review the merged head, then check `main`
  since (`git log <merge>..origin/main -- <paths>`) for follow-up fixes.
- **Draft** → review, and say bots skip drafts.
- **Fork, out-of-scope owner, or maintainer-owned repo** → `other-repos.md`
  third-party mode.

## Phase 1 — Materialize the head

Read the code at the head, not just the hunks — the twin page, the caller, the lock,
and the workflow are outside the diff. Export a read-only tree; it changes no git state
in the shared checkout:

```sh
T=/mnt/sdv_repos/tmp/pr-review/<repo>-<N>   # same device as the uv cache; not a git repo, so the puller ignores it
git -C /mnt/sdv_repos/<repo> cat-file -e <headRefOid> 2>/dev/null \
  || git -C /mnt/sdv_repos/<repo> fetch origin pull/<N>/head    # objects + FETCH_HEAD only; HEAD never moves
mkdir -p "$T" && git -C /mnt/sdv_repos/<repo> archive <headRefOid> [<paths>] | tar -x -C "$T"

# no local checkout, or the fetch is unwanted: export code paths over the API
gh api "repos/<o>/<r>/git/trees/<headRefOid>?recursive=1" --jq '.tree[]|select(.type=="blob").path' \
  | grep -E '^(python|tests|scripts|models|R|ops|\.github)/|^(pyproject\.toml|uv\.lock|DESCRIPTION)$' \
  | xargs -P8 -I{} sh -c 'mkdir -p "$(dirname "'"$T"'/{}")" && gh api "repos/<o>/<r>/contents/{}?ref=<headRefOid>" -H "Accept: application/vnd.github.raw" > "'"$T"'/{}"'
```

Reports and `context.md` stay in the scratchpad; only trees that need a venv go under
`/mnt/sdv_repos/tmp/pr-review/` (the root filesystem is nearly full and a venv built
across devices copies ~1.5 GB). Remove the tree when the review is done.

Never check out a PR branch in a canonical `/mnt/sdv_repos` checkout — the `git_pull`
cron moves HEAD at :40 of 1,5,9,13,17,21 and other sessions share those trees. In
`-raw`/`-data` repos pass `<paths>` — copy the `sparse-checkout:` list from the repo's
`tests.yml` (leaving `models/` or `R/` out fakes test failures). To run gates in the exported tree,
install its dependencies there (`uv sync --frozen`, `npm ci`) — never symlink a
canonical `node_modules` (lockfiles pick up `../` paths).

## Phase 2 — Intent and claims

1. Read the title, body, linked issues, commit messages, and the repo's instruction
   files **at the head**: `CLAUDE.md` → `AGENTS.md` → `CONTRIBUTING.md` → PR template →
   `.github/copilot-instructions.md`. A repo instruction that conflicts with a reference
   file wins for that repo; note the conflict.
   A reference that cites **this** PR as an incident is context, not a finding — the
   defect may have been fixed by a later commit inside the PR; verify at the head.
   A companion PR in another repo (the sdv-py change this PR depends on) is read at its
   own head; record whether it is merged and whether this PR's lock already includes it.
2. Build the **claims ledger**: every "verified", "tests pass", "no behaviour change",
   "parity", "pre-existing", number, or checked box → what evidence the PR carries.
   Skip the bot-generated "Summary by Sourcery/CodeRabbit" blocks — they are not the
   author's claims. A body written before later fix commits goes stale — compare it
   against the newest commit messages.

## Phase 3 — Load references

Always `references/universal.md`, plus the files `context.md` lists:

| Archetype | Reference |
|---|---|
| sportsdataverse-py | `references/python-package.md` |
| R packages (cfbfastR, hoopR, wehoop, oddsapiR, cfbplotR, …) | `references/r-package.md` |
| `*-raw`, `*-data`, models in them | `references/producers.md` |
| sdv-db, sdv-orch, sportsdataverse-web, sdv-swagger, bin/, sportsdataverse-data, universe | `references/platform.md` |
| game-on-paper-app | `references/web-gop.md` |
| sportsdataverse-js, plotting libs, papers, toolkit/dotfiles, maintainer-owned | `references/other-repos.md` |

Mixed PRs load the union. Load `references/false-positives.md` before Phase 6.
Verify blocks in the references write the PR diff as `git diff origin/main...HEAD`; in
an exported tree use `diff.patch` or `gh pr diff <N> -R <o/r> --name-only`. Run tests
with the repo's own CI command (copy it from `tests.yml`, including markers such as
`-m "not archive"`), prefixed `env -u VIRTUAL_ENV` so a global venv isn't picked up.

## Phase 4 — Review passes (in this order; each fills a report section)

The first three passes are the ones capable reviewers skip — they go deep on domain
logic and miss the failure branch, the vacuous test, and the environment assumption.
Do them first, exhaustively, for every item in the diff:

1. **Failure-path pass (U-FAIL).** Enumerate every new or changed fetch, parse, stage,
   upload, commit, push, retry, cache write, and `except`/`tryCatch`/`|| …` branch. For
   each, record what the failure branch returns and whether the exit code reaches the
   caller. → *Failure-path ledger*.
2. **Test pass (U-TEST).** For every new or changed test: would it fail with the fix
   reverted? Does it skip when an artifact, key, or network is missing? Does it run the
   production condition? → *Test ledger*.
3. **Environment pass (U-PATH, U-CI, PLAT-ORCH-1).** CWD-relative paths, machine paths,
   systemd/cron PATH, runner, secrets and token scopes, sparse checkout and path
   filters, what CI cannot see (push-to-main-only pkgdown, live tests skipped on PRs,
   repos with no CI). For every changed script, CLI flag, or function signature, list
   **every caller** (`context.md` lists workflow, sdv-orch registry, and script callers
   it can find; also check crontab and sibling repos) and the convention each one
   passes — a callee changed to match one caller breaks the others. Resolve each
   caller's **interpreter and venv** (the droplet runs `python/.venv`, CI builds from
   the lock) and import any newly used symbol with that interpreter — a lock bump that
   never reaches the droplet venv is an `ImportError` on the next cron run. → *Environment ledger*.

A ledger with nothing to enumerate says `n/a — <what was checked>` (e.g. "n/a — no
fetch, parse, upload, or except in the 3 changed files"), never a bare "none".

Then:

4. **Contracts and data semantics** — season keys, id dtypes, joins, ordering, empty
   schemas, loader/tag/API/codegen contracts, deploy order (U-DATA, U-DEP, archetype
   rules).
5. **Security** (U-SEC; the web and platform rules).
6. **Domain depth** — the most productive pass once the ledgers are done. Replay the
   old and new logic over **real** data and diff the outputs: committed fixtures
   (`astro/test/fixtures/`, `tests/fixtures/`), and season files on the droplet
   (`cfbfastR-cfb-data/cfb/pbp/parquet/play_by_play_<yr>.parquet`,
   `nfl-data/out/espn_nfl/pbp/play_by_play_<yr>.parquet` — local, gitignored). Check a
   season convention with a real-world fact: open one raw payload and compare its
   season id and game dates to the directory and asset year, or find one known player's
   first season. Local data trees reflect current `main` and may already contain this
   PR's output — strip the new columns (or use the published asset from before the PR)
   before replaying. Trace callers across sibling repos; check the public twin.
7. **Claims** — close out the claims ledger (U-CLAIM).
8. **Hygiene** — deletions, conflict markers, reverts of recent `main` logic, churn,
   agent state (U-GIT).

**Specialists, dispatched in parallel** with an explicit lens and file list — never a
`general-purpose` agent for a lens an SDV agent owns:

| Diff contains | Dispatch |
|---|---|
| `.py` in sdv-py | `sdv-python-reviewer` — lens `polars` (dataframe code), `http` (`dl_utils` network code), `parser-contract` (ESPN parsers), `docstring` (new public callables) |
| `.py` in a producer | `sdv-python-reviewer` lens `polars`; producer network code is reviewed against U-FAIL here (the `http` lens covers sdv-py's `dl_utils` only) |
| `R/`, `man/`, `_pkgdown.yml`, roxygen | `sdv-r-reviewer` with the matching lens |
| A port between R/Python/TS | `sdv-parity-reviewer` |
| Model, gate, backtest, or validation code | `sdv-model-reviewer` with the matching lens |
| sdv-py returns tables / codegen schemas, R `@return` tables | `sdv-docs-reviewer` (audit mode); a producer's own `column_descriptions.yaml` is reviewed inline |
| A new or renamed release tag | `sdv-dataset-coverage-auditor` |

When subagents are unavailable, read the agent's definition at
`<this-skill-dir>/../../agents/<agent>.md` and apply the lens inline.

**REVIEW-SIZE** — above ~40 files or ~3k changed lines, fan out one subagent per
archetype or pass (cap 6), each given its reference file, its file subset, the head SHA,
and the report sections it owns; merge and dedupe their findings yourself. Bots skip
very large PRs, so nothing else will have read them.

## Phase 5 — Verify every finding

**Before running any PR code — tests, mutations, replays, CLIs — cut its outward
paths.** The droplet's `gh` is logged in and `.Renviron` holds real tokens; a
publisher test with its fix reverted can upload to a production release tag.

```sh
export GH_CONFIG_DIR="$(mktemp -d)" GH_TOKEN= GITHUB_TOKEN= GITHUB_PAT= SDV_GH_TOKEN=
mkdir -p "$T/.shim" && printf '#!/bin/sh\necho "BLOCKED during review: gh $*" >&2; exit 97\n' > "$T/.shim/gh" \
  && chmod +x "$T/.shim/gh" && export PATH="$T/.shim:$PATH"
```

Never invoke publish, upload, push, deploy, purge, or ingest entry points, never
source `.Renviron`, and keep live-test toggles (`SDV_PY_LIVE_TESTS`, …) unset. A test
that fails with exit 97 or `BLOCKED` touched an outward path — that is a finding
(U-TEST-1: tests must mock it), not a reason to lift the block.

For each candidate:
1. Re-read the lines at the head SHA (a finding against already-fixed code is the most
   common bot false positive).
2. Write the concrete **failure scenario**: input or state → wrong output, crash, or
   exposure. No scenario → drop it.
3. Prove it when cheap: run the test, replay a fixture, grep the caller, reproduce with
   `env -i`, or `git show <locked-sha>:<path>` for a symbol.
4. Label it **CONFIRMED** (reproduced, or unambiguous from the code) or **PLAUSIBLE**
   (needs the author's knowledge).

Then:
- Run the archetype's local gates at the head (commands in each reference). Order: the
  tests the PR adds or touches, then a mutation check (revert the fix in the exported
  tree, confirm red), then the full suite in the background with a time cap — an
  unrelated slow or hanging suite is reported, not waited on. Environment traps: a
  repo venv with an editable sdv-py is not the locked commit (use a fresh
  `uv sync --frozen` in the exported tree); `uv lock --check` on `branch = "main"` git
  sources can report stale for reasons unrelated to the PR. Anything you couldn't run
  is listed as unverifiable, never implied passed.
- Checks at the head SHA (`gh pr checks` takes no SHA):
  `gh api repos/<o>/<r>/commits/<head>/check-runs --jq '.check_runs[]|[.name,.status,.conclusion]|@tsv'`
  plus `gh api repos/<o>/<r>/commits/<head>/status`; name red, pending, and structurally
  blind checks.
- Bot state: a bot review counts only when `commit_id == head` **and** its body is
  non-empty **and** zero threads are unresolved (`context.md` computes it). Unresolved
  Major/Critical bot threads are findings — cite the link, don't restate.
- Drop or reframe anything on `references/false-positives.md`.

## Phase 6 — Report

Write `$SCRATCH/reviews/<repo>-<N>/review.md` (a path the caller names wins) with
exactly these sections, in order. Every section appears; an empty one says
`n/a — <what was checked>`.

1. **Header** — `repo#N · title · head <sha> · base <branch> · reviewed <date>`.
2. **Verdict** — one of `BLOCK` (an unresolved blocker) · `CHANGES REQUESTED` (majors)
   · `COMMENTS` (minors only) · `LGTM (advisory)` — plus one sentence why.
3. **Findings** — a summary table sorted by severity, then one numbered block per
   finding with the full failure scenario, evidence (command + output), and fix:

   | # | Sev | Rule | Location | One-line problem | Status |
   |---|---|---|---|---|---|

4. **Failure-path ledger** — `item | failure branch returns | exit propagates? | finding #`.
5. **Test ledger** — `test | fails if fix reverted? | skips when? | finding #`.
6. **Environment ledger** — `assumption | holds in CI/cron/systemd/deploy? | finding #`.
7. **Claims ledger** — `claim | evidence in PR | verified? | finding #`.
8. **Gates** — local commands run → result; CI at head; bot-review proof; blind spots.
9. **Post-merge watch list** — what only `main` or a deploy reveals (pkgdown run,
   classic-page smoke, `systemctl restart`, reprocess/republish, `SCHEMA_REV` bump).
10. **Observations outside the diff** — brief, never blocking.

Severity:

| Severity | Means |
|---|---|
| blocker | Silently wrong or missing published data; data loss; secret exposure or auth bypass; production outage or broken deploy; a public/loader/tag/API contract broken without migration; a green-but-empty path; conflict markers or unexplained deletions |
| major | Wrong result under realistic input; required evidence missing (twin, regen, lock, pkgdown, local gates where CI is blind); a test that cannot fail for the changed behaviour; a convention whose violation caused a logged incident |
| minor | Maintainability, consistency, or docs drift with no behaviour impact |
| nit | Omitted unless the user asks |

Severity comes from the failure scenario, not from a rule's default tag — the `[blocker]`
/ `[major]` tags in the references are starting points. Rate by what the merged PR makes
reachable: a PR that writes a wrong assumption about an **untouched** caller into a
touched file owns that consequence. A pre-existing defect that makes the PR's **stated
goal** unreachable (the stage the PR fixes is never invoked) is a finding rated by that
goal failing. Code the PR rewrote or moved owns the defects it carries over. A test
that cannot fail takes the severity of the behaviour it fails to guard. A green-but-empty
path is a blocker when it can publish, commit, or ingest, and major when it only builds
locally. Any other defect that exists identically with or without the PR is an
Observation.

In the terminal: verdict, finding counts by severity, the top three findings, and the
report path.

## Phase 7 — Post (tier 1, only after an explicit yes)

Show the exact text first. Post as one review at the head SHA:

```sh
gh api repos/<o>/<r>/pulls/<N>/reviews -X POST --input "$SCRATCH/reviews/<repo>-<N>/review.json"
# {"commit_id": "<head>", "event": "COMMENT", "body": "...", "comments": [{"path": "...", "line": 42, "side": "RIGHT", "body": "..."}]}
```

Findings are written finding-first: failure scenario, then fix, then the incident it
echoes (a PR link, not an internal rule id). Read the review back after posting.

## Red flags — stop and do the pass you're skipping

| Thought | Reality |
|---|---|
| "The diff looks right" | The twin page, the caller, the lock, and the workflow are outside the hunks. Read at the head. |
| "CI is green" | No required checks; pkgdown and live tests don't run on PRs; sparse checkouts omit directories. |
| "CodeRabbit already reviewed it" | Rate-limited, stale-head, or empty reviews all look green. Check the proof. |
| "The happy path is correct, so it's fine" | Green-but-empty is the most-shipped defect class. Walk every failure branch. |
| "There are tests" | Would they fail with the fix reverted? Do they skip when the artifact is missing? |
| "Pre-existing — it was just moved" | Moved code is new surface (game-on-paper-app#229 → #233). |
| "It's a data repo, it's mostly data" | Season keys and publish paths have the highest blast radius in the ecosystem. |
| "I'll list everything I noticed" | Thirty nits bury the blocker. Omit nits; put untouched code in Observations. |
| "The bot suggested it, so it's probably right" | Check `false-positives.md` — house style is not a defect. |
| "I couldn't run the gate, but it's probably fine" | Write "unverifiable here" in Gates. |

## Keeping this skill sharp

A defect that shipped past a review that used this skill is a rule this skill is
missing: capture it with `sdv-learn` (rule + incident + diff signal), and add a
`pr_context.py` signal with a positive and a negative test in
`tools/test_pr_context.py` when the pattern is mechanically matchable.
