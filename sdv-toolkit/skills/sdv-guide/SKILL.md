---
name: sdv-guide
description: Use to find out what the sdv-toolkit contains and which part to reach for, without needing to remember any of it. Renders the catalog as a runbook — every skill and agent with a one-line "when to reach for it", its phase menu, which reviewers it dispatches, and what it hands off to — plus the hook inventory, the archetype routing matrix, the upstream skill routing tables for R and ML/DS, and the 0.3.x to 0.4.0 rename map. Accepts an optional filter, for example modeling, R, shipping, data, or porting. Invoke for "what skills are available", "what should I use for X", "which agent reviews Y", "what does the toolkit have", "sdv help", "what was <old-skill-name> renamed to", or when unsure which skill applies.
---

# sdv-guide — callable index

Everything on this page except the rename map is generated live from the
files already on disk — don't hand-maintain a second copy of any of it.

## Rendering the index

1. Read `catalog.json`. If an argument was given (e.g. `modeling`, `R`,
   `shipping`, `data`, `porting`), split each entry's `name`, `purpose`,
   `archetypes`, and `phases` into words on non-alphanumeric characters
   (hyphens, slashes, spaces), and keep only entries with a matching
   word. A word matches the argument, case-insensitively, if: it equals
   the argument; it equals the argument with a trailing `ing` removed
   (and, when that leaves the stem ending in a doubled consonant, drop
   one — `shipping`→`ship`, `porting`→`port`, `modeling`→`model`); or it
   *starts with* the argument or that stem (`sdv-port` still matches
   `porting`). **Exception:** arguments of 2 characters or fewer (e.g.
   `R`) match a whole word only, exactly and case-sensitively, with no
   stemming or prefix matching — a case-insensitive substring match on a
   single letter would hit nearly every entry, so `R` intentionally
   surfaces only entries whose text carries a standalone capital `R`
   (the language), not every entry that happens to contain the letter.
   With no argument, keep every entry.
2. Render the filtered entries the way `tools/render.py`'s
   `render_readme(catalog)` does (skills table, then agents table) — call
   that function rather than re-deriving the table. For each skill also
   surface its `phases` (phase menu), `dispatches` (reviewers it calls),
   and `hands_off_to`, when the entry has them — those aren't in the
   plain README table.
3. **Hook inventory.** Read `hooks/hooks.json`; list each hook by its
   trigger event (`SessionStart` / `PreToolUse` / `PostToolUse`) plus
   matcher, and a one-line purpose drawn from the command's own
   `echo`/message text.
4. **Archetype routing matrix.** Read `ARCHETYPE_BINDINGS` and
   `ARCHETYPE_GATES` in `hooks/sdv_router.py`; render one row per
   archetype (binding rule + gate command) — this is what the
   SessionStart router already emits per-repo, shown here for every
   archetype at once.
5. **Upstream skill routing tables.** Any catalog entry with a `pulls`
   field routes its general (non-SDV-specific) concerns to an external
   skill; render one table per such entry, `lens/lane -> upstream skill`.
   Today that's `sdv-r-reviewer` (R: `r-skills:*`, `r-lib:*`). No catalog
   entry currently declares an ML/DS `pulls` list — say that plainly
   rather than fabricating one.
6. Always print the rename map below verbatim and in full, regardless of
   any filter — it is the one thing on this page not derivable from
   `catalog.json` (the old names no longer exist anywhere on disk), and
   someone reaching for a retired name won't know to ask for it under a
   new-world filter term.

## Rename map (0.3.7 → 0.4.0)

| Old | New |
|---|---|
| `sdv-preflight`, `sdv-address-bot-reviews`, `sdv-stack`, `sdv-release` | `/sdv-ship` (phase menu) |
| `sdv-port-r-to-python`, `sdv-port-python-to-r`, `sdv-pandas-to-polars` | `/sdv-port` (direction) |
| `sdv-pipeline-layout`, `sdv-scrape-job`, `sdv-build-data`, `sdv-standardize-repo` | `/sdv-data-pipeline` |
| `sdv-capture-oracle` | `/sdv-model-spine` phase 0 |
| the six `sdv-add-*`, `sdv-capture-endpoint` | `/sdv-add-source` |
| `sdv-gen-returns-schema`, `sdv-r-returns-table`, `sdv-new-example-notebook`, `sdv-pkgdown-personalize` | `/sdv-document` |
| `polars-1x-reviewer`, `http-layer-reviewer`, `espn-parser-contract-reviewer`, `docstring-auditor` | `sdv-python-reviewer` (lens) |
| `roxygen-doc-reviewer` | `sdv-r-reviewer` (lens) |
| `oracle-gate-reviewer`, `leakage-reviewer` (design-time) | `sdv-model-reviewer` (lens) |
| `anomaly-triage-reviewer`, `extraction-semantics-reviewer`, `parity-divergence-reviewer`, `leakage-reviewer` (harness) | `sdv-harness-triage` (finding_type) |
| `port-parity-reviewer` | `sdv-parity-reviewer` |
| `returns-table-auditor`, `provider-shape-mapper` | `sdv-docs-reviewer` (mode) |
