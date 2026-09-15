# Universal review rules — every SDV pull request

Load this for every review. Archetype files add to it; they never relax it.

Format: **ID** `[severity]` rule — *diff signal* — (evidence). Evidence is a PR
(`repo#N`), a commit, or a memory note, so a finding can cite the incident rather
than the rule id. Sections are ordered by how often the class shipped a defect
across 810 merged PRs (May–Sep 2026), not by how often bots mention it.

Specialist rules already owned by an SDV agent are **routed, not restated**:
polars API / http layer / ESPN parser contract / docstrings → `sdv-python-reviewer`;
roxygen / pkgdown / R style → `sdv-r-reviewer`; cross-language ports →
`sdv-parity-reviewer`; model gates, leakage, silent no-ops → `sdv-model-reviewer`;
returns tables → `sdv-docs-reviewer`; new release tags across surfaces →
`sdv-dataset-coverage-auditor`.

---

## U-FAIL — the failure path (green-but-empty: the #1 shipped class)

For every new fetch, parse, stage, upload, or commit, ask: **what does the
failure branch return, and does the exit code reach the caller?**

- **U-FAIL-1** `[blocker]` A failed fetch/parse/stage/upload must not become an
  empty frame, a zero, a "skip: no rows", or `EXIT=0`. Only 404/410 mean absent;
  5xx, 403 and timeouts retry, then raise. — *broad `except` returning
  `pl.DataFrame()`/`{}`/`None`; `git push … || true`, `git commit || echo`;
  `set -uo pipefail` without `-e`; rc read through `| tee`/`| tail` with no
  `PIPESTATUS`; a trailing `echo EXIT=$?` as the step's status; `continue` after a
  failure while an artifact is still written; `[ -z "$TOKEN" ]` as the only
  credential check* — (wehoop-wnba-stats-data#14 published nothing for 30 days
  while green; sportsdataverse-py#464, #347→#348/#349; cfbfastR-data#20;
  sportsdataverse-py#482 failed 60/60 silently)
- **U-FAIL-2** `[blocker]` Never persist an empty or falsy payload into a
  read-through cache or as a "done" marker; finality comes from provider status
  (`status.type.completed`, every `FINAL*` spelling), never from a file existing.
  — *un-guarded `json.dump(payload)`; `if path.exists(): skip`; `== "FINAL"`* —
  (2,735 `{}` NBA cache files became permanent hits; cfbfastR-cfb-raw#8/#16 banked
  940 pre-game shells; NGS `FINAL_OVERTIME` dropped 24 OT games)
- **U-FAIL-3** `[major]` Absent ≠ zero ≠ null. Null-check, don't truthiness-check;
  never `fill_null(0)` / `?? 0` / `or 0` on a signal whose absence means unknown. —
  (game-on-paper-app `807c287`: `period=None` → 0 marked every final regressed;
  Sourcery on game-on-paper-app#198 minted a Q0 split)
- **U-FAIL-4** `[major]` A builder or publisher PR shows non-zero output on a
  known-populated season (a positive control). "skip X: no rows" for every dataset
  means the reader resolved nothing, not an empty season. — (wehoop-wnba-stats-data#14)
- **U-FAIL-5** `[major]` Fail-open is for optional enrichment only, per unit (one
  window, one feature), and it logs what was skipped. A column that ships in a
  **published** asset is not optional: a failure that silently publishes it all-null is
  **U-FAIL-1**. A failed fetch cached for the run (`lru_cache` around a function that
  returns empty on error) turns one blip into every season. — (sportsdataverse-py#464
  "silently never worked in production"; game-on-paper-app#220/#221/#244)
- **U-FAIL-6** `[major]` Bounded, classified external calls: `timeout=` on
  `subprocess`/`requests`, `--max-time` on curl; retries classify status (no backoff
  on permanent 4xx; never retry a non-idempotent `gh release create`); retry counts
  from env/config are validated `>= 1` and exhaustion **raises**. — *`range(1,
  ATTEMPTS + 1)`; retry wrapper returning `None`* — (cfbfastR-cfb-data#75 spent 55
  min/run retrying uploads into a tag that never existed; #76 attempts=0 published
  nothing while counting uploads)

## U-DATA — data semantics

- **U-DATA-1** `[blocker]` Season keys follow each surface's convention and are
  re-keyed **exactly once** at the documented boundary; an asset's filename year
  equals its rows' `season`. Verify a convention with a real-world fact per table
  family (Wembanyama `1641705` first season = 2024 under END keying; 66-game max in
  2012; CFP first season 2014), never a column/dtype audit. — *`season ± 1`,
  `$((i + 1))`, `{season + 1}` in a URL template (never evaluates), unanchored
  `nba_stats_` patterns (also match `wnba_stats_`)* — (1,931 nba_stats assets
  re-keyed 2026-08-13; hoopR-nba-stats-data#29 double shift; sportsdataverse-py#367
  shifted 8 WNBA URLs; an ncaa_mfb `_2026` asset holding 2025 rows ingested 0 rows)

  | Convention | Surfaces (verify against `sdv-db/python/src/sdv_db/catalog.py` `SEASON_END_YEAR_OFFSET` — this is a snapshot) |
  |---|---|
  | START year | cfb, nfl, ncaa_mfb, pff_cfb, pff_nfl |
  | END year | nba, nba_stats, nhl, mbb, wbb |
  | single calendar year | wnba, wnba_stats, mlb, ncaa_baseball, pwhl, pff_ufl, pff_aaf |
  | commence-time year | odds |
  | academic year (`season + 1`) | **only** inside ncaa-mfb-football-raw; `-data` stamps START |

- **U-DATA-2** `[blocker]` One dtype per id, fixed at the boundary; assert
  `left.schema[k] == right.schema[k]` before a join; no float→string ids (`"123.0"`),
  no `strict=False` casts on ids (malformed ids become nulls that inner joins drop).
  — (sportsdataverse-py#350 "highest-value finding", #353, #245 breaking Int64 play
  id; port-specific classes → `sdv-parity-reviewer`)
- **U-DATA-3** `[major]` Joins on row keys, never position; enrichment joins are
  LEFT; the right side is unique (dedupe before joining and check fan-out); compare
  key sets, not row counts. — (sportsdataverse-py#408 inner join to QBR deleted every
  passer while fixtures ran `join_participants=False`; #341 duplicate keys fanned into
  a cross product; traded players fanned out `nba_player_positions`)
- **U-DATA-4** `[major]` Anything rendered, compared, snapshotted or published is
  sorted on a full key with a tiebreak after `group_by`/`join`. — (sportsdataverse-py#494
  box-score rows reordered every run, caught only by GOP's evidence diff; #247)
- **U-DATA-5** `[major]` `pl.col("x") == True` is house style — the real question is
  **can the column be null?** Tri-state predicates need `fill_null(False)` on the
  combined predicate; no `drop_nulls()` after feature construction; NaN-aware float
  comparisons. — (sportsdataverse-py#358 `penalty_negated_play` tri-state, #413;
  fastRhockey-nhl-data#1)
- **U-DATA-6** `[major]` Aggregation scope matches the concept (game vs period vs
  OT vs window vs drive); era/season cut-offs come from the shared bounds, not
  literals. Football specifics: drive-level answers come from the drives grouping
  (`drive.team`), never plays grouped by `drive.id` (ESPN files post-turnover plays
  under the ended drive); dedupe `drives.current` against `drives.previous`;
  field-position flags use possession-relative `yardsToEndzone`, not `yardLine`;
  administrative rows (Timeout, Two-minute warning, End Period) are excluded from
  scrimmage/EPA sums and skipped by lag/lead logic. — (sportsdataverse-py#435 OT
  scope, #493 + game-on-paper-app#247 live drive double-counted, #463 + cfbfastR#150
  hard-coded `<= 2017` era, #495 + nfl-data#39 `scoring_opp` flagged 2/3 of drives;
  NFL week-1 audit: Timeout rows moved team EPA by up to −18)
- **U-DATA-7** `[major]` Empty input keeps the documented schema (no early
  `return df` before `with_columns`); sometimes-absent provider fields use
  `.get()` / optional chaining. — (sportsdataverse-py#468 TBD competitor `KeyError`;
  game-on-paper-app#183/#227 empty 200s)
- **U-DATA-8** `[major]` A new or renamed filter/param must show that it changes
  row counts — providers silently ignore unknown keys. — (CFBD `division` →
  `classification` returned all divisions; sdv-py codegen silently ignores
  `query_params:`; `site.api.espn.com` 403s explicit User-Agents)

## U-DEP — cross-repo dependencies and deploy order

- **U-DEP-1** `[blocker]` When a consumer (a `-raw`/`-data` repo, GOP, sdv-db) uses
  a new sdv-py symbol, kwarg or behaviour, the lock **in this diff** must resolve to a
  commit that has it — check `git show <locked-sha>:<path>`; don't trust lock text
  or a sibling PR's green CI. Plain `uv lock` keeps the old git SHA; it needs
  `uv lock --upgrade-package sportsdataverse`. Same for R `DESCRIPTION` Imports and
  Python package-data. — (ncaa-mbb-hoops-data#20 Critical; nfl-data#38/#39;
  wehoop-wbb-data#36 + hoopR-mbb-data#29: the republish "had never taken" because
  main pinned a pre-fix sdv-py)
- **U-DEP-2** `[major]` A library fix is not shipped until consumers move. The PR
  says how it reaches users: seasons to republish, the consumer's `SCHEMA_REV`/stamp
  bump, pin bumps, deploy. — (cfb-raw `processing_version` did not move on a
  git-main lock bump, so reprocess skipped every game; GOP builds sdv-py `main` at
  image build time)
- **U-DEP-3** `[major]` A change spanning repos states its merge/deploy order
  (producer → sdv-db ingest → API restart → GOP `select`). — (game-on-paper-app
  `f0c0505`/#233: a column union 400'd every college team profile for ~2 h)
- **U-DEP-4** `[major]` Lockfiles are tracked, CI installs frozen (`uv sync
  --frozen`, `npm ci`), and lock changes are deliberate. `--frozen` does **not**
  check the lock matches `pyproject.toml` — ask for `uv lock --check`. No `uv.lock`
  hunks riding along from `uv run pytest`. — (sportsdataverse-py#454 added an extra
  without re-locking, the delta rode into #466; game-on-paper-app#203/#204 untracked
  `package-lock.json` turned main red with no repo change)

## U-CI — CI and GitHub Actions

No repo in scope has required status checks and admins bypass reviews, so a green
board is not a gate. Read the checks, then ask what they could not see.

- **U-CI-1** `[major]` CI actually exercises the changed surface. The sparse
  checkout lists every path the new code/tests read; the test job covers the
  language touched; path filters include the new tree. Known blind spots: R
  `pkgdown` runs on push to `main` only (vignettes too); sdv-py live tests skip PRs;
  cfbplotR skips vdiffr on CI; no CI at all in sdv-orch, sdv-swagger, softballR,
  dotfiles, bin/ — require pasted local output there. — (fastRhockey-pwhl-raw#3: 22
  parity tests "never actually ran"; game-on-paper-app#240 vitest-only CI deployed
  conflict markers; nfl-data#27; cfbfastR#153)
- **U-CI-2** `[blocker]` No untrusted expression expanded inside `run:` —
  `github.event.inputs.*`, `inputs.*`, `client_payload.*`, PR title/body/head ref,
  comment bodies. Pass through `env:` and quote. — (game-on-paper-app#176 CWE-78;
  hoopR-nba-data / baseballr-data / fastRhockey-nhl-data / cfbfastR-data daily
  workflows echo the dispatch commit message into `run:`)
- **U-CI-3** `[blocker]` Secrets never inlined in shell/ssh/heredoc or echoed; no
  `secrets.X || secrets.GITHUB_TOKEN` fallback (it 403s cross-repo *after* the whole
  build); a missing required secret fails before the build. — (game-on-paper-app#167;
  nfl-data#24)
- **U-CI-4** `[blocker]` Token scope matches the endpoint: `repository_dispatch`
  and cross-repo release upload are **write** (fine-grained `Contents: write` or
  classic `repo`); repo secrets silently shadow org secrets; branch on the API
  response body, not on `-z`. Comments that prescribe a scope are claims to verify.
  — (sportsdataverse-py#467/#482: the comment said `Contents: read`)
- **U-CI-5** `[blocker]` A workflow on the self-hosted production runner
  (`sdv-droplet`: Postgres, the Data API, Prefect, `/etc/sdv-db/sdv-db.env`) never
  gains a fork-triggerable event (`pull_request`, `pull_request_target`,
  `issue_comment`, fork `workflow_run`) — public repos already target it. Flag any
  new `pull_request_target` anywhere.
- **U-CI-6** `[blocker]` Workflows that commit to a data repo use a **repo-wide**
  concurrency group (`${{ github.repository }}-commit`, `cancel-in-progress: false`
  — cancelling mid-upload half-updates a tag), stage and commit before reconciling,
  reconcile with `git rebase --merge origin/main` (the am backend stalls on parquet),
  and fail the run on a rejected push. — (hoopR-nba-data run green-but-rejected)
- **U-CI-7** `[major]` Trigger topology: one producer per tree/tag; trigger
  workflows guard `github.ref == 'refs/heads/main'`; `repository_dispatch` keeps only
  the newest pending run, so N per-season pushes cannot drive N builds; load-bearing
  commit subjects (`<Sport> Raw Update (Start: YYYY End: YYYY)`) are preserved. —
  (cfbfastR-cfb-raw#10: three production builds fired from PR branches; racing WNBA
  compilers)
- **U-CI-8** `[minor]` Actions on node24 majors (checkout v5, setup-python v6,
  setup-uv v8.1.0, setup-node v5, upload-artifact v7, cache v5); tag pins are the org
  convention; `persist-credentials: false` when a later step pushes with a PAT.
- **U-CI-9** `[major]` Merge automation treats an empty conclusion as pending;
  `gh pr merge --admin` in a script or a PR merged before its review landed is
  called out. — (sportsdataverse-py#417 merged before CI finished; nfl-data#29
  merged 7 min before a re-review that found 3 defects)

## U-TEST — tests

- **U-TEST-1** `[major]` **Would the test fail with the fix reverted?** Red flags:
  the expectation recomputed with the code's own expression; `raising=False`;
  synthetic dicts standing in for an upstream return; `skip` when a committed artifact
  is missing; `expect_error()` with no class/message; a skip guard on only the first
  of several fetches; float `==`; CWD-relative fixture paths; expiring fixtures (week
  counts, `Sys.Date()`); `toContain(regex)`; `<= 1` where an exact count is known;
  regex over source text instead of calling the function. Bug-fix PRs should show
  the test seen red (4% of PR bodies do). Model and gate code → `sdv-model-reviewer`
  silent-no-op lens. — (cfbfastR-cfb-data#76/#77; cfbfastR#151/#152/#153;
  sportsdataverse-py#336/#453; game-on-paper-app#186/#243)
- **U-TEST-2** `[major]` Tests run the production condition: flags production
  enables, oracle columns removed, the snapshot actually consumed. —
  (sportsdataverse-py#408, #335)
- **U-TEST-3** `[major]` Fixtures are byte-faithful real captures with a provenance
  README (source, capture date, row counts, id dtypes); never reformatted (a parity
  CSV's trailing space is load-bearing); parity asserts against real source-language
  output. — (three Statcast parsers shipped wrong on hand-written fixtures)
- **U-TEST-4** `[major]` Gates fail closed on NaN, inf, empty, a missing card, a
  missing season, or a wrong dtype — route depth to `sdv-model-reviewer`
  gate-integrity. — (wehoop-wnba-stats-data#15: `pl.corr` NaN on a constant column
  skipped the gate)

## U-SEC — security

- **U-SEC-1** `[blocker]` No tokens, cookies, DSNs, `.Renviron`/`.env` contents, or
  account-bound values in code, fixtures, OpenAPI `example:`s, logs, or PR text. Most
  repos in scope are **public** (GOP, sdv-swagger, Sports-Research-Papers, the
  packages). Key material stays in `~/.Renviron`, `/etc/sdv-db/sdv-db.env`,
  `/root/.sdv-*-key`.
- **U-SEC-2** `[blocker]` SQL: caller-supplied identifiers are whitelisted then
  quoted; values are bound parameters; no f-string SQL over request input.
- **U-SEC-3** `[blocker]` AuthN/Z: the gate runs before any env/key access; identity
  comes from vetted middleware state, never a raw `Authorization` header; a path
  rewrite never carries a request past a gate that checked the original path; a
  cacheable response never varies by viewer. — (game-on-paper-app#229 Critical
  `/nfl/admin` bypass, #217, #219 actor spoof; sportsdataverse-web#34)
- **U-SEC-4** `[major]` Redirect targets are validated (reject `//` and `\`, check
  origin); bearer tokens go only over https; identifiers from requests are
  regex-validated before proxying. — (game-on-paper-app#213 open redirect, #222;
  sportsdataverse-web#36)
- **U-SEC-5** `[major]` Exposure of licensed data (PFF, paywalled PDFs, secured
  provider specs) is an explicit owner decision recorded in the PR, never
  incidental to another change.

## U-GIT — merge and commit hygiene

- **U-GIT-1** `[blocker]` No conflict markers; when the PR is a merge or a rebase of
  a stacked branch, parse the changed files (`python -c "import ast; ast.parse(...)"`,
  `node --check`). — (game-on-paper-app#224 → #239: markers in `python/app.py`
  reached a deploy; fastRhockey#64 merged 17 min after a force-push, no re-review)
- **U-GIT-2** `[blocker]` Every deleted file is announced in the title or body. —
  (sportsdataverse-py#322 swept in staged `git rm`s of the `nbagl` package; #323
  restored them)
- **U-GIT-3** `[major]` No silent revert of recent `main` logic —
  `git log -S '<removed line>' origin/main` on suspicious removals. —
  (sportsdataverse-py#358 stale editor buffer reverted the `yds_penalty` extraction)
- **U-GIT-4** `[blocker]` No AI co-author trailers or "Generated with" footers in
  commits or the PR body, in any repo.
- **U-GIT-5** `[major]` No unrelated churn: whole-file CRLF↔LF flips, mode-only
  hunks, roxygen version drift rewriting `man/`, reformatting of untouched code,
  drive-by lint fixes. Code and data go in separate PRs; mass data changes land per
  season. — (cfbfastR-cfb-raw#7: 949 files, both bots skipped it)
- **U-GIT-6** `[major]` A force-push after a Critical/Major finding needs a
  re-review at the new head before merge. "Pre-existing" does not apply to code the
  PR **moved** — moved code is new surface. — (game-on-paper-app#229 deferred 4
  Majors as "moved verbatim"; #233 was the production regression)
- **U-GIT-7** `[minor]` No agent state or scratch committed: `.omc/`,
  `.claude/state`, flat `.superpowers/sdd/task-*`, `.playwright-mcp/`, `*-check*.png`,
  root-level `probe_*.py`/`spike.py`. New `scripts/`/`ops/` files are referenced from
  README/RUNBOOK/a workflow (orphan-scripts gate). — (game-on-paper-app#177)
- **U-PATH** `[major]` No machine paths (`C:/Users/…`, `/Users/…`, `~/Documents/…`)
  and no `Path()` around a URL (`https://h` collapses to `https:/h`). —
  (sportsdataverse-py#314; wehoop-wnba-stats-data#14)

## U-CLAIM — claims versus code

- **U-CLAIM-1** `[major]` Every "verified", "offline", "parity", "no behaviour
  change", or number in the PR body, docs, help text, or a status/log line has code
  or a committed script behind it in the diff; a status line never prints success on
  a branch that skipped the check. — (hoopR-nba-stats-raw#14 printed "proxy pool
  verified" in `--no-proxy` mode; cfbfastR#149 and sportsdataverse-py#479
  retractions; nfl-data#29)
- **U-CLAIM-2** `[major]` "Passed locally" names the head SHA and a
  production-equivalent environment: `env -i` for anything systemd/cron runs, the
  installed package for `R CMD check`, Docker workerd for `astro build`. The
  droplet's `git_pull` cron moves HEAD at :40 of 1,5,9,13,17,21. — (sportsdataverse-py#475)
- **U-CLAIM-3** `[minor]` Root causes quoted from bots, audits, or grepped Actions
  logs are hypotheses — Actions logs echo `run:` source, so a grepped "failed" line
  may be code that never ran. Compare against the prior commit's run before blaming
  the PR.

---

## General engineering (apply with judgement — SDV rules above win)

**Python.** Specific exception types; no mutable defaults; context managers for
files/connections; `timeout=` on I/O; `logging` not `print` in library code; typed
public API; no network or heavy work at import; `pathlib`; `multiprocessing` spawn
context when polars is loaded; validation via `raise`, not `assert` (stripped by
`-O`).

**R.** `pkg::fn` plus a DESCRIPTION Imports entry (never `library()` in package
code); `.data$` in tidy eval; `df[["col"]]` (not `$`, which partial-matches);
typed empty returns; classed conditions via `cli::cli_abort`; no `Sys.Date()` in
tests or CITATION; key-dependent examples/vignettes gated.

**TypeScript / JavaScript / Svelte.** `null` vs `0` handled explicitly; no `any`
escaping into public types; no floating promises; `AbortSignal.timeout` on fetch;
never serialize large objects into client props; `set:html` / `{@html}` only on
trusted content; typed event targets; ESM imports carry `.js`.

**SQL / Postgres.** Parameterized; migrations idempotent and transactional per
table (bound ACCESS EXCLUSIVE locks); indexes for new filter columns; partition-aware
DDL; no `trust` or `0.0.0.0/0` in `pg_hba`.

**API design.** Additive changes; stable error shape; pagination clamped
(`1 <= limit <= max`); caller errors are 4xx, never 500; auth on everything except
health; idempotent writes; frozen external contracts named in code.

**Architecture.** One source of truth per fact (codegen, catalog, registry) with a
drift gate; shared domain logic lives in the library (sdv-py), not the app; staged
rollout behind a flag whose promotion deletes the old path; cache keys carry the
producing code's version; fail loudly at boundaries; background jobs are observable
(exit code, log, freshness); least-privilege tokens; config via env with a documented
`.env.example`.
