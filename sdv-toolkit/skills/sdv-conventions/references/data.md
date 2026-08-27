# `-data` producer conventions

- Reads the sibling `-raw` repo directly via HTTP GH `-raw` repo — never re-scrape or clone.
- `NN_` stage numbering is intended build order, not run order — a stage's
  number reflects its place in the dependency chain, not the sequence the
  daily driver happens to invoke it in (drivers may parallelize/reorder).
- Idempotent re-runs: same contract as `-raw` — season/date CLI args,
  atomic writes (tmp+rename, masters upsert by id, never wholesale
  clobber), resume with a validity check (presence ≠ validity).
- Scripts earn `scripts/` only via runbook/driver wiring in the same
  commit; durable build logic lives in `<pkg>_data_build/` modules mirroring
  existing builders' signature/CLI, not in `scripts/`.
- New master-flag columns: add the column with a default BEFORE the upsert
  join — a schema-predates-column join crashes on first run.
- Models are pipelines too: every published artifact needs a **registry
  row** (model | artifact(s) | release tag | training data | fitting
  script | gates at publish | last retrain | cadence) in the repo's
  CLAUDE.md. Gates sit upstream of publish and are never lowered;
  `feature_names` verified at package AND consume time.
- R/Python parity is a standing policy: `-data` repos carry BOTH pipelines
  (Python primary, R maintained as the methodological equivalent); neither
  side is automatically authoritative — the one exception is `cfb-data`,
  where R is the released producer and Python must parity-match it.
- **DANGER — running an `R/espn_<lg>_*_creation.R` stage PUBLISHES to the
  live release.** There is no dry-run flag: the stage writes locally and then
  calls `sportsdataversedata::sportsdataverse_save(..., .token =
  Sys.getenv("GITHUB_PAT"))` unconditionally. Running one "just to see its
  output" overwrote three WNBA 2025 tags on 2026-08-07 (and regressed the pbp
  `id` from Int64 to Float64 in published data). Blanking `GITHUB_PAT` is NOT
  a workaround — the save is wrapped in `insistently(pause_min = 60,
  max_times = 10)`, so it retries ~10 minutes per dataset and only then
  fails. Neutralize the publisher instead: `assignInNamespace()` a no-op over
  `sportsdataverse_save` and assert the swap took before sourcing the stage
  (see `wehoop-wnba-data/ops/_r_no_publish.R`). That fails closed.
- **Manifests are two-tier — do not "fix" the duplicates.** The in-tree
  `<lg>/<dataset>/<lg>_<dataset>_in_data_repo.csv` is an append LOG, one row
  per RUN; `publish` collapses it to one row per season for the release asset
  (`.unique(subset=["season"], keep="last").sort("season")`). Duplicate season
  rows in the TREE are intentional history. Deduplicating them destroyed
  ~1,929 rows of run history across 37 files before the two-tier design was
  noticed. NOTE an unresolved conflict: some R stages upsert to one row per
  season in the tree while the Python builders append — both conventions are
  live in the same family. Establish which one a repo follows before changing
  either side.
- Publish: git commit of the data tree PLUS `gh release upload <tag>
  <file> --clobber` as a per-file loop — never a multi-file glob (silently
  drops large assets). Several families piggyback onto an existing release
  tag rather than cutting a new one.
- Loader handoff (sdv-py or an R package consuming the new dataset) is a
  separate consumer-side PR — note it as follow-up, don't bundle it in.
- **Join keys are MEASURED per league, never carried over.** For
  `player_box`, `(game_id, athlete_id)` is unique in WNBA but NOT in MBB or
  WBB — both need `team_id` too. Copying a sibling's keys silently fans a
  comparison join into a cross product and produces confident nonsense. Prove
  `df.select(keys).unique().height == df.height` on a real season before
  using a key, and make the tool REFUSE an unmeasured dataset rather than
  guess. (The MBB/WBB non-uniqueness is itself an ESPN defect: the same
  athlete appears under both teams' box scores in one game — identical stats,
  only attribution flips — so naive per-athlete aggregation double-counts.)
- **Proving a gate bites on shared-engine code: mutate site-packages, not
  your checkout.** Each `-raw`/`-data` repo pins `sportsdataverse` as a git
  dependency into its OWN `.venv`. Editing the local sdv-py checkout changes
  nothing for that repo — mutate
  `{repo}/.venv/Lib/site-packages/sportsdataverse/...` instead, then restore.
- polars 1.x; snake_case columns; one canonical dtype per id at the
  boundary; empty frames carry the documented schema.
