---
name: sdv-data-pipeline
description: Use for the full producer lifecycle in an SDV -raw / -data / -db repo. Phases — (1) standardize the repo onto the template (root pyproject/uv.lock, python/ + tests/ split, bash-only scripts/, CI, R-chain retirement), (2) decide placement BEFORE creating any script — the placement-decides-lifecycle rules, canonical NN_ stage numbering (numbers are intended build order, not run order), idempotency contract, and model-registry requirements, (3) set up a scraping or backfill job expected to run more than ~3 minutes with a user-executable runbook, unbuffered timestamped logging, a live watch command, resumable checkpoints, and env-only rate tuning, (4) build — read the sibling -raw tree and write tidy parquet, (5) validate, (6) publish via git commit plus per-file gh release upload. Invoke for "standardize this repo", "bring this repo onto the template", "where does this script go", "add a script to the raw repo", "new pipeline stage", "one-off driver", "set up a scrape", "backfill season X", "long scraping job", "scraper runbook", "build the dataset", "add a data-repo builder", "publish to the release", "reshape raw to data", or "daily processor".
---

# Data pipeline — the producer lifecycle for `-raw` / `-data` / `-db` repos

SDV splits producer repos: `-raw` repos scrape and commit raw JSON
(scraping-only — never reintroduce ML/model deps there); `-data` repos own
reshaping, modeling, reports, and publishing. This skill covers the whole
lifecycle across both: standardizing a repo onto the template, deciding
where a new script lives, running a long scrape, building a dataset,
validating it, and publishing it.

## Phase menu — jump to the phase that matches the ask

| Entry phrase | Start at |
|---|---|
| "standardize this repo", "bring this onto the template" | Phase 1 |
| "where does this script go", "new pipeline stage" | Phase 2 |
| "set up a scrape", "backfill season X" | Phase 3 |
| "build the dataset", "reshape raw to data" | Phase 4 |
| "publish to the release" | Phase 6 |

### Review (mandatory, before Phase 6)

- `sdv-python-reviewer` with lens `polars` for any dataframe code, `http`
  for any fetch/retry code.
- `sdv-harness-triage` for **any** validation WARN, passing `finding_type`
  as one of `sweep | extraction | leakage_lint | boundary_leakage | numeric_parity`.

Do not substitute `general-purpose`.

---

## Phase 1 — Standardize the repo onto the template

Authoritative spec: `ClaudeCowork/specs/2026-08-01-data-raw-repo-standardization-design.md`
(decisions D1–D43 + lessons §12.5–12.7). This phase is the executed ORDER with
the traps inlined, from pilots 1–10 (wehoop-wbb pair, hoopR-nba-stats pair,
wehoop-wnba-stats pair, the NCAA campaign pilots) plus the ESPN `-data`
fan-out. A multi-repo standardization needs an **execution ledger** — one
roadmap doc listing every repo × every decision with its verified state;
`ClaudeCowork/plans/2026-08-07-standardization-completion-roadmap.md` is the
worked example. Work on `main` via small verified commits (or PRs per
repo protection); the pilots proved 20-file PRs get real bot reviews and
2,000-file ones get silently skipped — split accordingly.

### Sequence (each step = one commit, verified before the next)

1. **Survey first, trust nothing written.** `git status` (other sessions leave
   WIP — never clobber; fold in only self-consistent 2-line cleanups, with
   attribution in the message). Diff `CLAUDE.md`/`copilot-instructions.md`
   claims against `ls` — pilots found files calling live repos "empty
   placeholders" and instructing agents to revert the standardization.
   Correcting actively-false directives belongs in the FIRST commit.
2. **Packaging to root**: `pyproject.toml` + `uv.lock` at root (merge any
   nested `python/pyproject.toml`); package-dir stays `python/`; `tests/` to
   root; kill `requirements.txt`; pinned ruff rule set (`E4 E7 E9 F I`,
   ignore `E712`); pytest `testpaths`/`pythonpath` + an `archive` marker;
   `sportsdataverse` pinned to git main via `[tool.uv.sources]`; `.Rproj`
   beside `DESCRIPTION`; template gitignore block (bare AND `**/` nested).
   Annotate any deliberately-tracked dir that looks like build output
   (`.bundles/`) IN the gitignore, or someone will "fix" it.
3. **Moves**: `scripts/*.py` → `python/`; tests out of `scripts/`; update every
   reference (`grep -rn "scripts/[a-z_]*\.py"` over sh/yml/md). Interpreter
   resolution via a sourced `scripts/_venv.sh` (this repo's `.venv`, env
   override, loud failure) — pilots found three scripts hardcoding a SIBLING
   repo's venv. Never `uv run` inside long-running scrape entry points (it
   re-syncs mid-sweep); reserve it for tests/lint.
4. **Gates**: `uv lock && uv sync --dev`, full pytest, `ruff check --fix`,
   `bash -n scripts/*.sh`. Wiring pytest for the first time WILL surface dead
   tests and stale paths — fix them here, they are why this step exists.
5. **CI** (`tests.yml`): sparse checkout (`python tests scripts pyproject.toml
   uv.lock` — a 500k-file archive checkout never finishes), `uv sync --frozen`,
   `pytest -m "not archive"`, ruff, `bash -n`. ~30s on a 490k-file repo.
6. **Purges** (own commit, HEAD-only, never rewrite history): committed raw
   JSON superseded by the `-raw` sibling — but "superseded" is a PER-FILE
   claim: diff game-id sets first and copy anything only-here into the raw
   store (pilot 4 found 85 preseason games per family that the sweep's
   season-type scope never captures). `.qs` + `.csv.gz` per D30.
7. **R/Python dual-pipeline parity** (`-data`) — **DO NOT retire the R chain.**
   Python is the PRIMARY pipeline and gets the work; R is maintained
   alongside it as a methodological/language equivalent. Two R chains were
   retired on 2026-08-02 under the old rule and had to be restored
   (`hoopR-nba-stats-data` 645 lines, `nfl-data` 251) — if a repo has no R
   twin, that is a gap to fill, not a state to preserve. See Phase 5 for the
   full dataset-level parity policy (what counts as parity, who's
   authoritative, the `cfb-data` exception) — this step is only about NOT
   deleting the R side while standardizing. Workflows may still be
   Python-only — restoring the twin preserves the METHOD in a second
   language, it does not re-schedule R. When rewriting a workflow: uv, raw
   store over `raw.githubusercontent.com`, season default computed in bash
   (NBA rolls over in OCTOBER; WNBA is calendar-year — never copy one
   league's rule to the other). Keep an annual job if the daily cron windows
   miss an event (WNBA draft is mid-April; daily runs May–Oct).
8. **Docs/close-out**: update the repo's own agent-facing docs to the new
   layout; record lessons in the spec (§12.x); memory topic update.

### Traps that cost real time in pilots (verify, don't assume)

- **Verification must name the ref it verifies.** `ahead=$(git rev-list
  origin/main..main)` says nothing while on a feature branch — this masked an
  unmerged fix TWICE. Print `HEAD=$(rev-parse --short HEAD)
  origin/main=$(rev-parse --short origin/main)` instead. Same rule for a
  brief's "known broken" claim: check it against git BEFORE fixing it — one
  fan-out repo's CI fix was already landed and a stale brief nearly caused
  duplicate work.
- **Check `git status` AFTER committing.** A failed pathspec inside
  `git add -A -- a b c` silently drops the rest; a pilot shipped a workflow
  invoking a script deleted in the same "commit".
- **Pre-commit hooks mutate**: ruff-format strips not-yet-used imports (add
  imports in the same edit as first use); a hook-modified file aborts the
  commit — re-add and re-commit; ALWAYS confirm with `git log -1`.
- **Windows process checks lie**: `pgrep -f` cannot see native `python.exe`
  command lines, and a `CommandLine -match` filter matches the checking shell
  itself. Judge liveness by log growth or an explicit watched PID
  (`commit_loop.sh <pid>` pattern), never by process-name counts.
- **GATE-0 quiescence is TWO-channel** (before standardizing a repo another
  session may be capturing into): a process filter on the COMMAND LINE, AND
  capture-tree mtimes compared across two snapshots ~30s apart. Either channel
  alone reports a busy repo idle.
- **Read `docs/SCRAPING_NOTES.md` in full before touching a stats.ncaa repo** —
  it is normative for that family (transport, pacing, solve-proof), not
  background reading.
- **A guard's refusal rc MUST be distinguishable from a capture-failure rc.**
  A stale `MAX_SEASON=2025` refused season 2026 with rc=2, the range driver
  read that as a capture hard-stop, and an entire WBB pbp campaign captured
  ZERO bundles while discovery looked healthy. Bump the season guard in the
  same commit as the crosswalk-season bump.
- **Census by rows, not by counts.** A full-tree deep parse (99,240 bundles:
  0 corrupt, 0 bm-verify artifacts persisted as captures) is the only honest
  completion claim; the residual 797 contests vs discovery resolved to
  documented skips + pageless games, which a count-only check would have
  reported as loss.
- **Diff-port byte-sibling twins** (MBB→WBB) instead of re-deriving the change
  — see Phase 2's twin-repo rule.
- **A cross-repo rename (D33) goes reader-side-WITH-FALLBACK first** when the
  writer lives in another repo: accept both names on read now, land the writer
  rename + fallback drop as a tracked follow-up.
- **CRLF in `.sh` files fails GitHub runners' syntax gate** — one repo's tests
  were red on `main` for days from this alone. `bash -n` locally on Git Bash
  will not catch it.
- **`uv sync --frozen` in CI, and nothing after it that re-resolves** — an
  `--upgrade-package` step defeats the lock the gate exists to enforce.
- **Kill by CIM + command-line filter, never by process name** — blanket
  `Stop-Process python` would have killed another session's 25-worker
  campaign.
- **Backfills must commit as they run**: launcher starts
  `scripts/commit_loop.sh $$` and flushes once at exit; presence-based resume
  makes stranded-uncommitted work invisible.
- **Bot review economics**: CodeRabbit skips >100 files, Sourcery >300 and
  has a weekly diff budget a purge PR can exhaust for the whole org. Put the
  reviewable logic in the small PR; note the skip in the bulk one.
- **A rate-limited review bot reports a GREEN check while performing no
  review.** CodeRabbit ("Review rate limited" / "you've reached your PR review
  limit") and Sourcery ("weekly rate limit of 500000 diff characters") both did
  this repeatedly on 2026-08-13; several PRs merged bot-unreviewed behind a
  passing tick. Read the check's status DESCRIPTION, not its conclusion.
- For `-raw` capture semantics (write guards, zero-row vs `{}`, floors,
  measure domains, poisoned defaults), defer to
  `sdv-internal-refs/nba/API_NOTES.md` + `ENDPOINT_DECISIONS.md` — those are
  provider-specific and normative there.

### Step 9 — the fan-out phase (docs, schemas, models)

Numbered thin builders, `docs.py` + column-description stores, pydantic
models, schedule-master artifacts (D34). Still **don't scope-creep these into
step 2** — they are gated on a tested build package existing. Executed
2026-08-07 across the ESPN `-data` fan-out; the dominant bug class was
**drift gates that pass locally and would red every PR**.

- **Verify a docs `--check` drift gate with the data payload ABSENT** —
  physically move the payload dir aside to simulate CI's sparse checkout,
  then run the gate. Two repos shipped gates that would have reddened every
  PR: one's sparse checkout omitted `docs`/`README.md`/`CLAUDE.md` so the
  generated files did not exist on the runner; the other's coverage tables
  derive from `*_in_data_repo.csv` manifests deliberately outside the
  checkout, so a CI-side regen always diverged. Fix = add the doc paths to
  the sparse checkout AND exclude payload-derived sections (seasons-built
  line, coverage table) from the drift comparison.
- **When the sparse checkout genuinely cannot see the data the docs derive
  from, do NOT wire `--check` into CI** — document why in the module
  docstring. A permanently-red gate is worse than no gate.
- **The sections `--check` excludes are the ones an offline regen destroys.**
  A `--no-live` docs regen blanked 14 real "Last published" dates to em dashes,
  and because the status block is deliberately outside the drift comparison the
  gate would have passed over the wipe. Offline regen is a read-only debugging
  mode: `git diff` the excluded sections and restore them before staging, or
  don't commit an offline run at all.
- **Column descriptions: leave EMPTY when no description store exists.** An
  empty cell is an honest TODO; an invented or cross-league-borrowed sentence
  is a defect. (Never borrow by column name across leagues.)
- **Preserve each file's existing line-ending convention** when regenerating
  marker blocks — a naive LF rewrite turned a ~20-line diff into 144.
- **Pydantic dataset models are generated from the LATEST PUBLISHED or
  COMMITTED parquet** — never invented, never borrowed from the twin league.
  An unpublished release tag gets NO model until first publish.
- **Loader-schema cross-check fixtures are VENDORED** into the repo with a
  documented refresh command; never read a sibling checkout at CI time.
- **A repo with no dataset registry skips D40/D43** — state the reason in the
  ledger rather than inventing a registry to satisfy the decision.

---

## Phase 2 — Placement: where scripts live and what they must promise

Read this BEFORE creating any new script. Distilled from the 2026-08-02
30-repo audit (`ClaudeCowork/notes/2026-08-02-raw-data-repo-script-audit.md`):
703 scripts, 85 orphans, ~55% of recent adds twin-repo copy-paste. The
disease is **indistinguishability** — load-bearing stages that look like
one-offs, and one-offs that live forever beside package code. Placement +
naming carry the lifecycle so a reader (or CI) can tell without archaeology.
This is also the section Task 15's `sdv-conventions` `raw`/`data` archetype
packs reference.

### Placement decides lifecycle (the load-bearing rule)

| Location | Meaning | Contract |
|---|---|---|
| `python/<pkg>/`, `R/` | durable stage logic | importable, tested, invoked by numbered shims / `python -m` |
| `scripts/` | drivers + launchers ONLY | **every file referenced by README run-order, a workflow, or another driver** — the orphan test (CI gate: `sportsdataverse/.github` reusable workflow `orphan-scripts.yml`) |
| `ops/` | recurring operational tools that aren't stages (autocommit, publish bundles, supervise, backup) | one README line each |
| `ops/init/` | one-time bootstraps (the old `0000_`/`0001_` release-init scripts) | 3-line README; never in the stage-numbered namespace |
| `ops/oneoff/` | dated one-shots that must be repo-resident: `YYYYMMDD_<what>.py` | delete or header-mark `DONE` after the run; date = run date |
| gitignored `dev/` or session scratchpad | experiments, probes, session drivers | the DEFAULT birthplace of every new script |

**A script is born in `dev/`/scratchpad; it earns `scripts/` only by being
wired into the runbook/driver/workflow in the same commit.** If a one-off is
actively driving real repo work, commit it to `ops/oneoff/` — never leave it
untracked (the highest-value incident tooling repeatedly had the weakest
provenance).

Hard bans: session-phase names (`fanout_p2.py`, `p7_drop_csvgz.py` — plan-phase
numbers are meaningless outside the session); new siblings for incident recovery
(add a mode/flag to the existing stage script at the chokepoint instead — the
cfb `72b835e0a` hardcoded-True bug was a one-off edit to a durable pipeline);
experiments inside shipped packages.

**The `-raw`/`-data` boundary is one-way**: data repos read raw trees; raw
repos never import from data repos and never grow modeling deps.

### Canonical stage numbering

`-raw` (ESPN family, identical across nba/mbb/wnba/wbb):
`espn_{lg}_NN_{name}_scrape.py` — 01 schedules, 02 pbp, 03 standings,
04 game_rosters, 05 draft, 06 player_stats, 07 team_stats, 08 team_rosters,
09 player_core; 10+ league extras; 99 master. **A missing dataset leaves a
HOLE — never compact.** Cross-repo number semantics beat dense numbering.
`-data`: `espn_{lg}_NN_*_creation` / `{lg}_NN_*` stage files as thin shims over
the tested build package ("the directory listing IS the pipeline"); the daily
driver's ordered array is the single source of sequence truth. Cadence in the
name when not daily: `annual_*`, `weekly_*`. The sh driver is the `00` role.

**The `NN_` numbers are intended build order, not run order** — a stage's
number reflects where it sits in the pipeline's dependency chain, not the
order the daily driver happens to invoke stages in (drivers may parallelize
or reorder independent stages).

### Idempotency contract (every stage)

1. Season/date as CLI args (`-s/-e`), defaults derived (`most_recent_*_season()`).
2. Resume = skip-already-captured **with a validity check** (non-empty,
   parseable) — bare `path.exists` let 3,347 empty `{}` payloads block
   refetch. Presence is not validity: a "captured" flag or file existing on
   disk must still be rejected if it's empty/unparseable. Never persist an
   empty payload. (This applies to scrape checkpoints in Phase 3 too — same
   rule, same failure mode.)
3. Atomic writes (tmp+rename); never overwrite a complete artifact with a
   partial; masters upsert by game_id, never wholesale clobber.
4. Boolean flags: the tolerant house `str2bool` (unknown → False, never raises —
   a cron typo must not trigger a full re-scrape). `argparse type=bool` is a
   BUG (truthy-string, `bool('false') is True`), and thread the parsed flag
   all the way to dispatch — a one-off hardcoded `True` in a dispatch tuple
   severed `-r` for months (cfb `72b835e0a`). Same rule applies to scraper
   CLI flags in Phase 3.
5. Rate/pace env-only, ONE naming convention per repo family — see Phase 3
   for the concrete env-var names and per-site tuning.
6. Publish: `--dry-run`/`--publish` mutually exclusive; per-file `--clobber`;
   `.done_<season>` sentinels written only on rc 0.
7. Wholesale re-runs always safe; drivers log per-stage elapsed seconds into the
   run summary (pipelines are benchmarkable run-over-run).
8. Driver failure ledger: one dead stage doesn't stop siblings, partials still
   commit, the run exits RED at the end.

### Models are pipelines too

Stage order: ingest → features → train → evaluate/gate → package → publish →
integrate. Every published artifact gets a **Model registry row** in CLAUDE.md
(model | artifact(s) | release tag | training data | fitting script | gates at
publish | last retrain | cadence — `frozen` is valid but must be explicit;
unknown cells are `TODO`, never fabricated). A retrain recipe referenced by
nothing is the `retrain_xg_models.R` stranding failure. Gates sit upstream of
publish and are never lowered; `feature_names` verified at package AND consume
time. Training experiments are born in `dev/` like any other one-off.

### Twin repos

NBA↔WNBA stats-raw and MBB↔WBB share near-identical stacks. Until the shared
league-parameterized engine package lands: a fix in one twin ports to the other
**in the same session, verified** — drifted twins have already shipped a crash
one side didn't have.

---

## Phase 3 — Scrape: a user-executable runbook for long jobs

Any scrape/backfill expected to run more than ~3 minutes (ESPN,
stats.nba.com/wnba.com, stats.ncaa.org, Savant) must be **runnable and
watchable by the user directly**, not babysat through the assistant: the
user copy-pastes one command, sees real-time timestamped output, can Ctrl-C
safely, and can resume from a checkpoint. The assistant may additionally
watch in the background, but the user never waits on the assistant to learn
a job's status.

### Step 0 — find the owning `-raw` repo (before writing anything)

Scraped output belongs in the SDV `-raw` repo for that provider family, in
its **canonical committed tree** — raw per-game JSON is committed directly
to git (the chosen pattern, at scale; do NOT warn about repo bloat and do
NOT stage output in scratch/`dev/` dirs). If a `-raw` repo exists for the
family, the job runs THERE, extending its existing scraper — not as a new
standalone script elsewhere.

| Family | Repo | Data tree | Scraper entry |
|---|---|---|---|
| NFL | `nflverse-dev/nfl-raw` | `nfl/raw/{season}/{game_id}.json` | `python/scrape_nfl_json.py -s/-e` |
| CFB | `cfbfastR-dev/cfbfastR-cfb-raw` | `cfb/{json,game_rosters,play_participants,schedules,betting,power_index,qbr}/…` | `python/scrape_cfb_json.py` (+ per-dataset `scrape_cfb_*.py`) |
| MBB | `hoopR-dev/hoopR-mbb-raw` | `mbb/{json,game_rosters,schedules,standings,team_rosters,team_stats,player_season_stats}/…` | `python/` scrapers + `scripts/daily_mbb_scraper.sh` |
| NBA / NBA-stats | `hoopR-dev/hoopR-nba-raw`, `hoopR-nba-stats-raw` | mirrors the mbb shape | family scrapers |
| WBB / WNBA | `wehoop-dev/wehoop-{wbb,wnba,wnba-stats}-raw` | mirrors the mbb shape | family scrapers |
| NHL / PWHL | `hockey-dev/fastRhockey-{nhl,pwhl}-raw` | `nhl/…` | `python/` + `scripts/` |

Before writing: `ls <family-dir>/` + read the repo's `CLAUDE.md` — the
existing tree IS the spec (per-dataset subdir names, season partitioning,
id scheme e.g. nflverse ids for NFL). New dataset for the family → new
sibling subdir following the same shape, never a new top-level layout.

**Repo placement conventions:**

- Launcher script → the repo's `scripts/` (next to `daily_*_scraper.sh` /
  `backfill_*.sh`); logs → the repo's `logs/`. Follow Phase 2's placement
  rules (stage-numbered scrapers, `ops/oneoff/` for dated one-shots, the
  orphan test on `scripts/`).
- **Inventory/checkpoint**: most families keep a
  `*_schedule_master.parquet` with per-game boolean flags for which
  artifacts exist. Upsert flags after a run; on first run of a NEW flag
  column, the master's schema predates it — add the column with a default
  before joining, and mind polars join-suffix naming on the upsert (see
  Phase 4's gotchas for the fuller version of this failure — it has hit
  both scrape checkpoints and build joins).
- **Commit cadence**: batch (per-day or per-season chunk), not per-game;
  conventional message e.g. `feat(raw): 2025 wk14 games`.
- Wire the job into the repo's daily cron script if it should recur.

### Deliverables (all three, every time)

1. **A launcher script** (`scripts/run_<job>.sh` in the owning repo — or
   `dev/` only when no `-raw` repo owns the family) the user runs in their
   own terminal.
2. **A live watch command** handed back verbatim, e.g.
   `tail -f <log>` or
   `powershell -Command "Get-Content -Path <log> -Tail 5 -Wait"`.
3. **A resume story**: the job skips already-captured work on restart, so
   Ctrl-C + rerun is always safe.

### Launcher script requirements

```sh
#!/usr/bin/env bash
export PYTHONUNBUFFERED=1        # real-time lines, no 4KB buffering lag
export PYTHONIOENCODING=utf-8    # cp1252 chokes on unicode/emoji in piped output
LOG=logs/<job>_$(date +%Y%m%d_%H%M%S).log   # the owning repo's logs/ dir
mkdir -p logs
python <scraper>.py "$@" 2>&1 | tee -a "$LOG"   # append (>>-style), never truncate
echo "EXIT=$?" | tee -a "$LOG"   # grep-able completion marker; do NOT trust a
                                 # 'COMPLETED' print the script may emit early
```

- **Timestamps on every log line** (scraper-side `logging` format with
  `%(asctime)s`) so hangs are visible as a stalled clock, not a mystery.
- **Rate limits are env-only — never hardcoded.** Expose
  `STATS_RATE_HITS` / `STATS_RATE_MAX` / `STATS_RATE_WINDOW` (or the job's
  equivalents) so the user can re-tune pace without a code change or a
  round-trip through the assistant.
- **Graceful Ctrl-C**: catch `KeyboardInterrupt`, flush the checkpoint,
  exit non-zero.
- **Resumable checkpoint**: derive done-ness from what's on disk
  (per-game JSON present ⇒ skip) rather than a separate state file when
  possible — the data IS the checkpoint. Apply Phase 2's idempotency-contract
  validity check (item 2): presence is not validity, reject
  empty/unparseable payloads too.
- **Boolean CLI flags**: apply Phase 2's idempotency-contract rule (item 4)
  — tolerant `str2bool`, never `argparse type=bool`, flag threaded all the
  way to dispatch.
- **Season-scoped sentinels** (multi-season campaigns): write
  `.done_<season>` only on exit 0, never on an output file's existence.
- **Per-stage timing**: the driver logs elapsed seconds per stage into the
  run summary so pace regressions are visible run-over-run.

### Per-site gotchas (check before writing the script)

| Site | Constraint |
|---|---|
| `stats.nba.com` / `stats.wnba.com` | TLS/JA3-blocks plain `requests` (silent HANG, not an error) → `curl_cffi` `impersonate="chrome"`. Datacenter/cloud IPs also hang — run from a residential IP only. Gate live tests with `SDV_PY_NBA_STATS_LIVE=1`, not the generic live gate. |
| `stats.ncaa.org` | Unfriendly to direct traffic — route through the proven proxy client; keep parallelism at 1–2. |
| ESPN Core v2 | 403s under aggressive parallelism; Site v2 is more forgiving. Keep workers low and never re-scrape already-captured games. |
| ESPN Site v2 | **Soft-throttles as HTTP 200 with the payload array absent** — no exception, so a per-item `except` logs nothing and the run reports success. An instrumented sweep returned 239/362 rosters empty with zero errors; paced, 0. Assert the expected array is PRESENT per response, count the misses, and treat a nonzero count as throttling — not as a roster gap. |
| All | Bound ATTEMPTS, not saves — an id-walk without an attempt cap can 404-flood (the CBS incident: 8,400+ wasted requests). |

### Assistant-side conduct while the job runs

- Launch **the user's script, not an inline command**, and hand back the
  watch command in the same message.
- If also monitoring: use a background task and report on completion — no
  foreground sleep-polling, and never paste the log into the reply
  (summarize + give `cat <log>`).

---

## Phase 4 — Build: read raw, write tidy parquet

| Data repo | Reads from | Package layout | Publishes to |
|---|---|---|---|
| `nflverse-dev/nfl-data` | `nfl-raw` `nfl/raw/{season}/{game_id}.json` | `python/{nfl_data_ingest, native_pbp, nfl_model_publish, model_training}` | `sportsdataverse-data` releases (`nfl_model_pbp`, `nfl_model_artifacts`, `nfl_4th_down_models`) |
| `cfbfastR-dev/cfbfastR-cfb-data` | `cfbfastR-cfb-raw` `cfb/{json,…}` | `python/{cfb_data_ingest, cfb_data_build, cfb_model_pbp, cfb_model_publish, cfb_model_reports}` + R producer | `espn_cfb_*` releases (14 public datasets; R is the released producer — python builders must parity-match) |
| `hoopR-dev/hoopR-nba-stats-data` | `hoopR-nba-stats-raw` | `python/nba_data_build` | git commit + `sportsdataverse-data` release tags (e.g. `nba_stats_pbp`, `nba_stats_possessions`, `nba_stats_game_lineups`) |
| `hoopR-dev/hoopR-{mbb,nba}-data`, `wehoop-dev/wehoop-*-data`, `hockey-dev/fastRhockey-*-data` | family `-raw` mirror | family-shaped | family releases |

Cron entry point: `scripts/daily_<family>_processor.sh` (data side) mirrors
the raw side's `daily_<family>_scraper.sh`. The target repo's `CLAUDE.md` +
existing package layout govern over this table — read them first.

1. **Ingest** — read the sibling `-raw` checkout directly from disk (it's a
   sibling under `GitHub-Data/`; never re-scrape or clone). Path via the
   repo's config/env (e.g. `SDV_VALIDATION_*_DATA_ROOT` patterns), not
   hardcoded absolute paths. Put reading logic in `<x>_data_ingest/`.
2. **Build** — a builder module per dataset in `<x>_data_build/` (mirror the
   existing builders' signature/CLI), following Phase 2's stage-numbering and
   idempotency contract. polars 1.x; snake_case columns; one canonical dtype
   per id at the boundary; empty frames carry the documented schema;
   partition output like the released dataset (per-season parquet is the
   norm).

Validation is Phase 5; publishing is Phase 6 — don't skip either on the way
from a built frame to a release.

### Gotchas

- **Raw/data boundary is one-way** — see Phase 2; data repos read raw trees,
  raw repos never import from data repos.
- **Loader handoff**: if sdv-py (or an R package) should load the new
  dataset, that's a separate consumer-side PR (cached loader + returns
  schema) — note it as follow-up, don't bundle it into the producer change.
- **New master-flag columns**: upserting a new boolean flag into a
  `*_schedule_master.parquet` whose schema predates it crashes on first
  run — add the column with a default before the join. This is the same
  master-parquet file Phase 3's scrape checkpoints upsert into, so the fix
  applies on both the scrape and the build side.

---

## Phase 5 — Validate before publish

Run the validation-harness checks the repo wires (constant-column,
extraction coverage, parity vs the PRIOR release for overlapping seasons).
The harness has caught real producer bugs — do not skip.

**R/Python parity (standing policy, 2026-08-03):** `-data` repos carry BOTH
pipelines — Python primary, R maintained as the methodological equivalent,
both moving together (Phase 1 covers not retiring the R chain while
standardizing; this is the ongoing gate). Parity is keyed on the DATASET,
not the file: R is dataset-per-file (`espn_{lg}_NN_{dataset}_creation.R`),
Python is layer-per-module (`{lg}_data_build/{ingest,reshapers,build,
publish}.py`) with datasets as `config.REGISTRY` rows. Before publishing a
dataset, confirm the other language still produces it; a dataset that
exists on only one side is a parity gap to close, not a simplification.
**Neither side is automatically authoritative** — a divergence is a review
item, decided on which is methodologically right. The one codified
exception is `cfb-data`, where R is the released producer and python
builders must parity-match its parquet.

Dispatch the mandatory Review agents (top of this file) before moving to
Phase 6 — `sdv-python-reviewer` on any dataframe/HTTP code touched during
the build, `sdv-harness-triage` on any WARN the validation run surfaces.

---

## Phase 6 — Publish

> **Before running ANY R stage, read the publish + manifest rules in
> `sdv-conventions` → `references/data.md`.** Two things there are
> incident-grade, not style: an `R/espn_<lg>_*_creation.R` stage publishes to
> the LIVE release with no dry-run gate (running one locally overwrote three
> WNBA tags on 2026-08-07), and the in-tree manifests are append LOGS that
> `publish` collapses — deduplicating them destroys intended history.

Two mirrors, both required when the repo uses both:

- **git commit** of the data tree (batch, conventional message);
- **release assets**: `gh release upload <tag> <one-file> --clobber` —
  **per-file loop, never a multi-file glob** (multi-asset uploads
  silently drop large files). Respect the repo's release map — e.g.
  nfl `nfl_model_publish` has `DECISION_MODELS_RELEASE_MAP` (fd →
  `nfl_4th_down_models`, rest → `nfl_model_artifacts`) that the generic
  subcommand ignores; check where each artifact belongs before uploading.
- **Piggyback releases**: several families publish onto an EXISTING release
  tag (`espn_cfb_*`, `sportsdataverse-data`) rather than cutting new ones —
  find the tag the released dataset already lives under.

**Wire the cron** — add/extend `scripts/daily_<family>_processor.sh` so the
daily run picks the new dataset up; log to `logs/` with Phase 3's scrape-job
logging conventions (unbuffered, timestamped, `EXIT=$?`).

**Loader handoff** — if sdv-py (or an R package) should load the new
dataset, that's a separate consumer-side PR (cached loader + returns
schema); note it as follow-up rather than bundling it into the producer
change.

### Gotchas

- **Publishing the data and publishing the artifact that DESCRIBES the data
  are separate steps — usually only the first is wired.** Three instances in
  one night (2026-08-13): per-tag release `README.md` assets stayed stale after
  the docs PR merged (needed a cutover re-run); sdv-db's API surface is
  generated from a committed DB snapshot, so it lags its catalog; and per-tag
  `<tag>_in_data_repo.csv` manifests were never written by the Python publish
  path at all — the R→Python port dropped the step, leaving manifests declaring
  1 season while 30 were published. The fix that worked: a read-only `check`
  that compares the tag's ACTUAL asset seasons against the manifest and exits
  non-zero on disagreement — **compare the SET, not the count** (a count-only
  check passes while the seasons are wrong).
- **Don't cut a parallel `_v3`-style tag — widen the production one.** A
  parallel tag accumulates consumers and becomes hard to retire.
  `nba_stats_pbpv3` / `possessions_v3` / `lineups_v3` ran beside production
  until the pipeline was widened to admit every NBA season type, which made
  them a strict subset (`v3_not_in_prod = 0`); they were deleted 2026-08-13,
  but only after a consumer-repoint sweep. If a parallel tag is unavoidable,
  name its retirement condition when you cut it.

Hand off to `/sdv-ship` for the PR/merge flow once the dataset is committed
and published.
