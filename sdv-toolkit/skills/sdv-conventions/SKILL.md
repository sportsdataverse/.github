---
name: sdv-conventions
description: Use when working in any SportsDataverse repo to load that repo archetype's binding conventions — the rules that differ between sdv-py, a -raw producer, a -data producer, and an R package, and that are the usual source of drift when moving between repos. Loaded automatically by the SessionStart router; invoke directly for "what are the conventions here", "what applies in this repo", "repo rules", or when a convention question arises mid-task. Reference files: sdv-py (polars 1.x surface, codegen is never hand-edited, manual_column_descriptions.yaml is the only place returns descriptions live, ID/join-key dtype discipline, mypy ratchet), raw (scraping-only, committed per-game JSON, rate discipline), data (NN_ stage numbering is intended build order not run order, idempotent re-runs, scripts earn scripts/ only via runbook wiring, models need registry rows), r-package (roxygen completeness, pkgdown reference coverage, tibble returns, snake_case). Also carries a UNIVERSAL rule that applies in every archetype — validate the instrument, not just the result: a measurement that drives an action must carry a control, a reconciliation, or a negative case before it is reported, and a selector that narrows silently is worse than no selector.
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

## Universal — validate the instrument, not just the result

Applies in every archetype. **A measurement that drives an action carries one
of these three before it is reported or acted on:**

- **A control** — run the instrument where the answer is already known. A
  sibling repo that is already correct, or the published artifact, is usually
  sitting right there.
- **A reconciliation** — decompose the number and check the parts sum. If a
  total cannot be broken into parts that add up, it is not yet a fact.
- **A negative case** — confirm the glob/regex/filter EXCLUDES what it should
  and INCLUDES what it should. Exclusion is the side nobody checks, and it is
  where these fail.

This is the same discipline the gates already demand (guard-the-guard, mutation
proof, vacuous-pass floors) turned on your own ad-hoc greps. Real failures it
would have caught, all from one 2026-08-07 session:

| Claim | Why it was wrong |
|---|---|
| "38,900 surplus manifest rows" | the glob counted a 31k-row × 78-col DATASET that merely shared the filename suffix; real figure 1,929 |
| "these duplicate rows are corruption" | they were an intentional append LOG; `publish` collapses to one row per season. The published asset — a perfect control — was clean the whole time |
| "`tools.validation` is importable here" | `find_spec` succeeded; the actual import failed on a dev-only dep |
| "the R files are dead code" | read correctly, intent inverted — git showed a commit *restoring* them |
| a `\bnba\b` sed | silently left `nba_*` untouched (`_` is a word char) |

Corollary: **a check that narrows silently is worse than no check.** A filter
that quietly stops matching leaves every downstream assertion passing
vacuously, which reads greener than before while testing less. Whenever you
add a selector, add the assertion that fails when it selects nothing — or
selects too little.

For the full producer lifecycle (not just the differing rules), see
`sdv-data-pipeline`. For documentation surface, see `sdv-document`.
