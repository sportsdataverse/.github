---
name: sdv-conventions
description: Use when working in any SportsDataverse repo to load that repo archetype's binding conventions — the rules that differ between sdv-py, a -raw producer, a -data producer, and an R package, and that are the usual source of drift when moving between repos. Loaded automatically by the SessionStart router; invoke directly for "what are the conventions here", "what applies in this repo", "repo rules", or when a convention question arises mid-task. Reference files: sdv-py (polars 1.x surface, codegen is never hand-edited, manual_column_descriptions.yaml is the only place returns descriptions live, ID/join-key dtype discipline, mypy ratchet), raw (scraping-only, committed per-game JSON, rate discipline), data (NN_ stage numbering is intended build order not run order, idempotent re-runs, scripts earn scripts/ only via runbook wiring, models need registry rows), r-package (roxygen completeness, pkgdown reference coverage, tibble returns, snake_case).
---

# SDV conventions — archetype packs

One reference file per repo archetype. Load only the one that matches the
repo you're in — these are the rules that DIFFER between archetypes, not a
full style guide.

| Archetype | File |
|---|---|
| sdv-py (the Python package) | `references/sdv-py.md` |
| `-raw` producer (scrape → commit JSON) | `references/raw.md` |
| `-data` producer (build → publish parquet) | `references/data.md` |
| R package (cfbfastR, hoopR, wehoop, …) | `references/r-package.md` |

For the full producer lifecycle (not just the differing rules), see
`sdv-data-pipeline`. For documentation surface, see `sdv-document`.
