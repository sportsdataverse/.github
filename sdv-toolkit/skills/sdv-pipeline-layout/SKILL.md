---
name: sdv-pipeline-layout
description: Use BEFORE creating any new script in an SDV `-raw`/`-data`/`-db` repo, and when naming/placing pipeline stages, ops tools, one-offs, or model training/publish code — the placement-decides-lifecycle rules, canonical stage numbering, idempotency contract, and model-registry requirements from the 2026-08-02 pipeline audit. Invoke for "where does this script go", "add a script to <raw/data repo>", "new pipeline stage", "one-off driver", or before an incident-recovery script.
---

# Pipeline layout — where scripts live and what they must promise

Distilled from the 2026-08-02 30-repo audit
(`ClaudeCowork/notes/2026-08-02-raw-data-repo-script-audit.md`): 703 scripts,
85 orphans, ~55% of recent adds twin-repo copy-paste. The disease is
**indistinguishability** — load-bearing stages that look like one-offs, and
one-offs that live forever beside package code. Placement + naming carry the
lifecycle so a reader (or CI) can tell without archaeology.

## Placement decides lifecycle (the load-bearing rule)

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

## Canonical stage numbering

`-raw` (ESPN family, identical across nba/mbb/wnba/wbb):
`espn_{lg}_NN_{name}_scrape.py` — 01 schedules, 02 pbp, 03 standings,
04 game_rosters, 05 draft, 06 player_stats, 07 team_stats, 08 team_rosters,
09 player_core; 10+ league extras; 99 master. **A missing dataset leaves a
HOLE — never compact.** Cross-repo number semantics beat dense numbering.
`-data`: `espn_{lg}_NN_*_creation` / `{lg}_NN_*` stage files as thin shims over
the tested build package ("the directory listing IS the pipeline"); the daily
driver's ordered array is the single source of sequence truth. Cadence in the
name when not daily: `annual_*`, `weekly_*`. The sh driver is the `00` role.

## Idempotency contract (every stage)

1. Season/date as CLI args (`-s/-e`), defaults derived (`most_recent_*_season()`).
2. Resume = skip-already-captured **with a validity check** (non-empty,
   parseable) — bare `path.exists` let 3,347 empty `{}` payloads block refetch.
3. Atomic writes (tmp+rename); never overwrite a complete artifact with a
   partial; masters upsert by game_id, never wholesale clobber.
4. Boolean flags: the tolerant house `str2bool` (unknown → False, never raises —
   a cron typo must not trigger a full re-scrape). `argparse type=bool` is a
   BUG (truthy-string), and thread the parsed flag all the way to dispatch.
5. Rate/pace env-only, ONE naming convention per repo family.
6. Publish: `--dry-run`/`--publish` mutually exclusive; per-file `--clobber`;
   `.done_<season>` sentinels written only on rc 0.
7. Wholesale re-runs always safe; drivers log per-stage elapsed seconds into the
   run summary (pipelines are benchmarkable run-over-run).
8. Driver failure ledger: one dead stage doesn't stop siblings, partials still
   commit, the run exits RED at the end.

## Models are pipelines too

Stage order: ingest → features → train → evaluate/gate → package → publish →
integrate. Every published artifact gets a **Model registry row** in CLAUDE.md
(model | artifact(s) | release tag | training data | fitting script | gates at
publish | last retrain | cadence — `frozen` is valid but must be explicit;
unknown cells are `TODO`, never fabricated). A retrain recipe referenced by
nothing is the `retrain_xg_models.R` stranding failure. Gates sit upstream of
publish and are never lowered; `feature_names` verified at package AND consume
time. Training experiments are born in `dev/` like any other one-off.

## Twin repos

NBA↔WNBA stats-raw and MBB↔WBB share near-identical stacks. Until the shared
league-parameterized engine package lands: a fix in one twin ports to the other
**in the same session, verified** — drifted twins have already shipped a crash
one side didn't have.
