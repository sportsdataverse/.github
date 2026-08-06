---
name: sdv-dataset-lifecycle
description: Use when a new or updated release tag needs to reach every downstream surface it touches — a fresh dataset, new assets on an existing tag, or a schema change (new column/season/dtype) on a dataset that already ships. Drives the 12-surface propagation checklist across five repo targets (the `<league>-data` release repos, `sdv-py`, the R sibling packages, `sdv-db`, `sdv-web`) and produces a per-dataset ledger that records which surfaces applied, which were done, and which were deliberately skipped — an unrecorded skip is how the season-coverage audit found 90 of ~140 surfaces silently missing. Invoke for "propagate this release", "wire up the new dataset", "did this reach the API/docs/DB", "a column got added, what needs updating", or "audit dataset coverage" (dispatches the read-only `sdv-dataset-coverage-auditor` first). Hands off to `sdv-ship` for the sdv-py-side commit/PR once its surfaces are done.
---

# Propagate a dataset release across the platform (sdv-dataset-lifecycle)

A dataset is not done when the release asset uploads. It has to reach up to
twelve downstream surfaces across five repo targets, and today that fan-out
is manual and memory-dependent — the single highest-value instance of drift
in the whole toolkit. The season-coverage audit found **90 of ~140 surfaces**
needing backfill; that is what an unmanaged fan-out looks like after a year.

This is a **checklist skill**, not a reference — it drives the propagation to
completion and produces a ledger. For "which loader feeds which dataset",
cross-reference `sdv-modeling/references/data-sources.md` §2 (the 155-loader
dataset→loader map) rather than re-deriving it here.

## Phase menu

| Entry phrase | Start at |
|---|---|
| "propagate this release", "wire up the new dataset" | Phase 1 — Detect |
| "did this reach the API/docs/DB", "audit dataset coverage" | Phase 2, after dispatching `sdv-dataset-coverage-auditor` |
| "a column got added, what needs updating" | Phase 1, schema-delta trigger |
| "write the ledger", "what did we skip and why" | Phase 4 |

## Phase 1 — Detect the trigger

Two shapes of trigger, and they are **not equally dangerous**:

1. **A new release tag, or new assets on an existing tag.** Loud — you (or
   `sdv-data-pipeline`) just made it. You know propagation is needed because
   you know you shipped something.
2. **A schema delta on a dataset that already ships** — a new column, a new
   season added to an existing parquet, or a changed dtype. **This is the
   dangerous one, and the precise mechanism matters — it is not uniform
   across surfaces, so don't wave at "everything goes stale":**

   - **Genuinely blind** (hand-maintained or a static snapshot; nothing
     forces an update): the loader schema (surface 3,
     `loader_schemas.yaml`), the returns table (surface 4,
     `manual_column_descriptions.yaml`), the generated docs (surface 5,
     derivative of 3+4), and the API response schema (surface 9,
     `sdv-db`'s `api/gen/schema_snapshot.json` is a **committed static
     file read at mount time**, not a live schema query).
   - **Self-healing — verified in `sdv_db/load.py`'s `_reconcile_columns`**:
     the Postgres ETL (surface 8) runs `ALTER TABLE ... ADD COLUMN IF NOT
     EXISTS` and widens a column's type automatically on every load. A new
     column reaches the DB without anyone touching surface 8 — don't spend
     effort "fixing" it.
   - **Self-detecting, but only if already registered**: the sdv-py loader
     itself (surface 2) does a columns-passthrough read
     (`pl.read_parquet(..., columns=None)`), so the new column is live and
     visible to any Python caller immediately — it is not the loader that
     hides it. And the validation harness (surface 11)'s
     `schema_contract.py` check emits an **ERROR finding for an unexpected
     column** — but only for a dataset that already has a `DatasetSpec`
     registered. An unregistered dataset gets no such error; a registered
     one turns every future schema delta loud. That asymmetry is the
     argument for registering surface 11 once, up front.
   - **Not applicable to column-level deltas**: the `sdv-db` catalog row
     (surface 7) carries `league`/`name`/`loader`/`module`/`partition_col`
     — no column list — so a new column doesn't require editing it at all.

   A new tag announces itself; a schema delta does not, and the surfaces
   that actually stay quiet are narrower than "everything downstream." Fix
   the genuinely-blind four (3, 4, 5, 9); don't burn effort on 8 (heals
   itself) or 7 (not applicable); lean on 11 if it's already registered,
   and register it if it isn't.

Identify which trigger fired, and for a schema delta, name the exact column
/ season / dtype that changed — Phase 2 needs it to scope which surfaces
actually require an edit (surface 4's returns table only needs the *new*
column's row, not a rewrite).

## Phase 2 — Select surfaces

Not every dataset needs all twelve surfaces, and deciding is the point of
this phase — **selection, not completeness, is the job.** Walk the table
below in order; for each row, decide `apply` or `skip` and write down why
either way (Phase 4 makes this durable).

**Counter-check — read this before proposing anything:** if your selection
proposes all twelve surfaces for a routine, same-schema season refresh (a
new season of an existing dataset, no new columns, no new consumer), **that
selection is wrong, not thorough.** A same-schema refresh typically only
touches surface 1 (new release asset) and, if the loader takes an explicit
season list rather than discovering seasons dynamically, surface 2. Surfaces
3–5, 7, 9, 11 are schema/registration surfaces — they don't change when the
shape of the data doesn't change. Proposing all twelve on every refresh
isn't caution, it's noise that will get the checklist ignored the next time
it's actually needed.

### The 12 surfaces

Verified against the live repos on 2026-08-06 (commands in the report). Two
corrections from the original design draft are folded in below — surface 9
is not a separate "sdv-data" repo (it lives inside `sdv-db`), and surface 11
has no literal `min_season` field (the harness expresses floors as named
thresholds, not a season cutoff).

| # | Surface | Repo | Location | Checkable condition |
|---|---|---|---|---|
| 1 | Release asset published | `<league>-data` (e.g. `cfbfastR-data`, `nflverse-data`, `hoopR-nba-data`, `wehoop-wnba-data`) | git commit + per-file `gh release upload`; owned by `sdv-data-pipeline` phase 6 | `gh release view <tag> --json assets` lists the file |
| 2 | Python loader | `sdv-py` | `sportsdataverse/config.py` (URL constant) + `sportsdataverse/<league>/<league>_loaders.py` (`load_*` function) | both grep as present: `grep '<DATASET>_URL' config.py`, `grep 'def load_<dataset>' <league>_loaders.py` |
| 3 | Loader schema | `sdv-py` | `tools/codegen/schemas/loader_schemas.yaml` — a **hand-edited source**; never hand-edit what it generates | a `load_<dataset>:` top-level key exists with a column list |
| 4 | Returns-table descriptions | `sdv-py` | `tools/codegen/manual_column_descriptions.yaml` — **never** `schemas/**.yaml` (clobbered on re-capture) | every column from the surface-3 row has a non-empty description here |
| 5 | Reference docs | `sdv-py` | generated `docs/docs/<sport>/reference/*` via `tools/codegen/generate.py` | `uv run python tools/codegen/generate.py --check` exits 0 |
| 6 | R parity loader | `cfbfastR` / `hoopR` / `wehoop` / `fastRhockey` — **only if that sibling package carries the surface** | `R/cfbd_*.R` (cfbfastR), `R/load_*.R` (hoopR, wehoop); fastRhockey has no `load_*` convention (per-endpoint `R/nhl_*.R` only) — usually a legitimate skip for hockey | a same-named or documented-equivalent R function exists, or the skip is recorded |
| 7 | Catalog row | `sdv-db` | `python/src/sdv_db/catalog.py` — a `Dataset` entry in `REGISTRY` | the `(league, name)` pair is present in `REGISTRY` |
| 8 | Postgres ETL | `sdv-db` | `python/src/sdv_db/load.py` (ingest) + `infra/postgresql/*.sql` (schema) + `systemd/sdv-db-ingest.service`/`.timer` (cron) | the table exists in the schema SQL and matches the surface-7 row's `name` |
| 9 | API exposure | `sdv-db` — **not a separate "sdv-data" repo; the API lives inside sdv-db** | `python/src/sdv_db/api/generated/endpoints.py` (read) + `api/ingest_routes.py` (write) + `api/gen/curation.yaml` / `api/gen/schema_snapshot.json` (schema) | a generated endpoint resolves the dataset's table |
| 10 | Platform freshness | `sdv-db` (push) + `sdv-web` (display) — a two-repo wire, not a single-repo surface | `sdv-db/python/src/sdv_db/heartbeat.py` (per-table freshness collector, POSTs to `/api/platform/db-status`) + `sdv-web/frontend/lib/platform/dbStatus.ts` + `app/api/platform/db-status/route.ts` | the table resolves under `heartbeat.py`'s `_TS_CANDIDATES`/`_ID_CANDIDATES` and appears in the platform DB tab |
| 11 | Validation registration | `sdv-py` harness | `tools/validation/registry.py` — a `DatasetSpec` entry — plus the coverage/correlation floors it uses from `tools/validation/thresholds.yaml` and `oracles.py` | a `DatasetSpec` with this dataset's `parquet_glob` exists in `registry.py` |
| 12 | Model registry | `<league>-data` — **only if the dataset is a model's output** | a lineage doc (e.g. `docs/models/<model>.md`, citing the training script) + a scheduled retrain workflow (`.github/workflows/*.yml` with a `schedule:` trigger, not manual-only) | the lineage doc exists and the workflow has a cron trigger |

**Repo count note:** "five repos" means five *targets*, not five checkouts —
target 1 (`<league>-data`) and target 3 (the R packages) are each a family
of several sibling repos; pick the specific one(s) the dataset actually has.

## Phase 3 — Propagate

For each surface marked `apply` in Phase 2, do the edit at its Location, then
verify against its Checkable condition before moving to the next surface.
Dispatch rather than hand-roll where a reviewer already owns the check:

- **Surface 4/5** (returns table, reference docs) → after editing, dispatch
  `sdv-docs-reviewer` in `audit` mode to confirm no other function/endpoint
  in the same family is now inconsistently documented.
- **Surface 6** (R parity loader) → after editing (or deciding to skip),
  dispatch `sdv-r-reviewer` with `lens: parity` (or `lens: all` for a new
  loader) against the touched R file.
- **Before starting, or when asked to "audit coverage"** → dispatch the
  read-only `sdv-dataset-coverage-auditor` (Task 11) either for this one
  dataset or as a full-inventory sweep; treat its report as the Phase 2
  starting point rather than re-deriving selection from scratch.

Surfaces 2–5 and 11 are `sdv-py`-internal; once they're done, **hand off to
`sdv-ship`** for the preflight → commit → PR → CI → merge sequence rather
than reimplementing that lifecycle here.

## Phase 4 — Ledger

Write one row per surface considered (not just the ones done) — the ledger's
value is making the *decision* visible, not just the work:

```
dataset: <name>
trigger: <new-tag | new-assets | schema-delta: col=<x> season=<y> dtype=<z>>

| # | Surface | Decision | Evidence |
|---|---|---|---|
| 1 | Release asset | apply — done | commit <sha>, `gh release view <tag>` |
| 2 | Python loader | apply — done | sportsdataverse/nfl/nfl_loaders.py:60 |
| 3 | Loader schema | apply — done | loader_schemas.yaml:<line> |
| 4 | Returns table | apply — done | manual_column_descriptions.yaml:<line> |
| 5 | Reference docs | apply — done | generate.py --check exit 0 |
| 6 | R parity loader | skip — hockey dataset, fastRhockey has no load_* convention | n/a |
| 7 | Catalog row | apply — done | sdv_db/catalog.py:<line> |
| 8 | Postgres ETL | skip — table unchanged, ETL already covers it | n/a |
| 9 | API exposure | apply — done | api/generated/endpoints.py:<line> |
| 10 | Platform freshness | apply — done | heartbeat.py picks up updated_at |
| 11 | Validation registration | apply — done | registry.py:<line> |
| 12 | Model registry | skip — not a model output | n/a |
```

**A row with no `skip — <reason>` and no `done` evidence is not a valid
ledger entry** — an omitted row is exactly the ambiguity this skill exists
to remove. If a surface is genuinely ambiguous, write `skip — undecided,
follow-up: <what would resolve it>` rather than leaving it out.

## Stop conditions

- A schema-delta trigger where you cannot name the specific column/season/
  dtype that changed — go find that first; "something changed" doesn't scope
  Phase 2.
- Surface 3 or 4 edited without the corresponding docs regeneration
  (surface 5) — `generate.py --check` will fail downstream in `sdv-ship`
  Phase 1 if you skip this.
- A ledger with unrecorded rows — incomplete, not "good enough."
