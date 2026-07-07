---
name: build-data
description: Use when building or extending a dataset in an SDV `-data` repo (nfl-data, cfb-data, hoopR-*-data, wehoop-*-data, fastRhockey-*-data) — the ingest → build → validate → publish pipeline that reads the sibling `-raw` repo tree, writes tidy parquet, and publishes via git commit + per-file gh release upload. Invoke for "build the dataset", "add a data-repo builder", "publish to the release", "reshape raw to data", or "daily processor".
---

# Build-data — the `-raw` → `-data` → release pipeline

SDV splits producer repos: `-raw` repos scrape and commit raw JSON
(scraping-only — never reintroduce ML/model deps there); `-data` repos own
reshaping, modeling, reports, and publishing. This skill encodes the data
side: read the sibling raw tree, build tidy frames, validate, publish.

## Repo map (data repo ← raw source ← publish target)

| Data repo | Reads from | Package layout | Publishes to |
|---|---|---|---|
| `nflverse-dev/nfl-data` | `nfl-raw` `nfl/raw/{season}/{game_id}.json` | `python/{nfl_data_ingest, native_pbp, nfl_model_publish, model_training}` | `sportsdataverse-data` releases (`nfl_model_pbp`, `nfl_model_artifacts`, `nfl_4th_down_models`) |
| `cfbfastR-dev/cfbfastR-cfb-data` | `cfbfastR-cfb-raw` `cfb/{json,…}` | `python/{cfb_data_ingest, cfb_data_build, cfb_model_pbp, cfb_model_publish, cfb_model_reports}` + R producer | `espn_cfb_*` releases (14 public datasets; R is the released producer — python builders must parity-match) |
| `hoopR-dev/hoopR-nba-stats-data` | `hoopR-nba-stats-raw` | `python/nba_data_build` | git commit + `sportsdataverse-data` release tags (e.g. `nba_stats_pbpv3`, `possessions_v3`, `lineups_v3`) |
| `hoopR-dev/hoopR-{mbb,nba}-data`, `wehoop-dev/wehoop-*-data`, `hockey-dev/fastRhockey-*-data` | family `-raw` mirror | family-shaped | family releases |

Cron entry point: `scripts/daily_<family>_processor.sh` (data side) mirrors
the raw side's `daily_<family>_scraper.sh`. The target repo's `CLAUDE.md` +
existing package layout govern over this table — read them first.

## Pipeline steps

1. **Ingest** — read the sibling `-raw` checkout directly from disk (it's a
   sibling under `GitHub-Data/`; never re-scrape or clone). Path via the
   repo's config/env (e.g. `SDV_VALIDATION_*_DATA_ROOT` patterns), not
   hardcoded absolute paths. Put reading logic in `<x>_data_ingest/`.
2. **Build** — a builder module per dataset in `<x>_data_build/` (mirror the
   existing builders' signature/CLI). polars 1.x; snake_case columns; one
   canonical dtype per id at the boundary; empty frames carry the documented
   schema; partition output like the released dataset (per-season parquet is
   the norm).
3. **Validate before publish** — run the validation-harness checks the repo
   wires (constant-column, extraction coverage, parity vs the PRIOR release
   for overlapping seasons). Where an R producer released the dataset
   (cfb-data), the python build must parity-match the R-released parquet
   before it ships. The harness has caught real producer bugs — do not skip.
4. **Publish** — two mirrors, both required when the repo uses both:
   - **git commit** of the data tree (batch, conventional message);
   - **release assets**: `gh release upload <tag> <one-file> --clobber` —
     **per-file loop, never a multi-file glob** (multi-asset uploads
     silently drop large files). Respect the repo's release map — e.g.
     nfl `nfl_model_publish` has `DECISION_MODELS_RELEASE_MAP` (fd →
     `nfl_4th_down_models`, rest → `nfl_model_artifacts`) that the generic
     subcommand ignores; check where each artifact belongs before uploading.
5. **Wire the cron** — add/extend `scripts/daily_<family>_processor.sh` so
   the daily run picks the new dataset up; log to `logs/` with the
   scrape-job conventions (unbuffered, timestamped, `EXIT=$?`).

## Gotchas

- **Raw/data boundary is one-way**: data repos read raw trees; raw repos
  never import from data repos and never grow modeling deps.
- **Loader handoff**: if sdv-py (or an R package) should load the new
  dataset, that's a separate consumer-side PR (cached loader + returns
  schema) — note it as follow-up, don't bundle it into the producer change.
- **New master-flag columns**: upserting a new boolean flag into a
  `*_schedule_master.parquet` whose schema predates it crashes on first
  run — add the column with a default before the join.
- **Piggyback releases**: several families publish onto an EXISTING release
  tag (`espn_cfb_*`, `sportsdataverse-data`) rather than cutting new ones —
  find the tag the released dataset already lives under.
