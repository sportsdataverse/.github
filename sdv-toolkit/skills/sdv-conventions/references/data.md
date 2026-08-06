# `-data` producer conventions

- Reads the sibling `-raw` repo directly off disk (sibling checkout under
  `GitHub-Data/`) — never re-scrape or clone it.
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
- Publish: git commit of the data tree PLUS `gh release upload <tag>
  <file> --clobber` as a per-file loop — never a multi-file glob (silently
  drops large assets). Several families piggyback onto an existing release
  tag rather than cutting a new one.
- Loader handoff (sdv-py or an R package consuming the new dataset) is a
  separate consumer-side PR — note it as follow-up, don't bundle it in.
- polars 1.x; snake_case columns; one canonical dtype per id at the
  boundary; empty frames carry the documented schema.
