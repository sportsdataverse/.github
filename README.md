# SportsDataverse

The [SportsDataverse](https://sportsdataverse.org) is a family of open-source sports-data
packages across Python and R — `sportsdataverse-py`, `hoopR`, `wehoop`, `cfbfastR`,
`baseballr`, `fastRhockey`, and more.

This repository also serves as the **SportsDataverse Claude Code plugin marketplace**.

## 🧩 Claude Code plugins

### Install

The `sdv-docs` MCP server runs through `uvx`, so install [uv](https://docs.astral.sh/uv/getting-started/installation/) first and make sure `uvx` is on your `PATH`. The other MCP server, `context7`, is remote and needs nothing local.

```sh
claude plugin marketplace add sportsdataverse/sportsdataverse
claude plugin install sdv-toolkit@sportsdataverse
```

Update
```sh
claude plugin update sdv-toolkit@sportsdataverse
```


### `sdv-toolkit`

Engineering tooling shared across the SportsDataverse Python + R repos — install once,
get identical automation everywhere.

- **Router** — a `SessionStart` hook detects the repo archetype (sdv-py, `-raw` / `-data`
  producer, R package, …) and loads that archetype's conventions on arrival.
- **Hooks** — block edits to codegen-generated (`# GENERATED`) files; block AI
  co-author/attribution trailers on commits; warn on unbounded capture/crawl loops;
  remind to regenerate after codegen-source edits, add a `returns_schema`, or
  `devtools::document()` after R edits; note a `tryCatch(warning = )` added to an R
  package (it unwinds and silently empties results); block mutating `git stash` in a
  repo with more than one worktree (the stash stack is shared, so parallel sessions pop
  each other's work).
- **Skills** (`/sdv-<name>`) — sources and endpoints (`/sdv-add-source`,
  `/sdv-api-sync`), producers and datasets (`/sdv-data-pipeline`,
  `/sdv-dataset-lifecycle`), docs (`/sdv-document`, `/sdv-regen-docs`), repo health
  (`/sdv-repo-audit`, `/sdv-review-pr`, `/sdv-triage`, `/sdv-ship`), R test coverage
  (`/sdv-r-coverage`), modeling and research (`/sdv-modeling`, `/sdv-model-build`,
  `/sdv-research-paper`), and the conventions packs (`/sdv-conventions`, including the
  README standard). `/sdv-guide` is the full index.
- **Agents** — lens-dispatched reviewers (`sdv-python-reviewer`, `sdv-r-reviewer`,
  `sdv-parity-reviewer`, `sdv-docs-reviewer`, `sdv-model-reviewer`,
  `sdv-paper-reviewer`) and auditors (`sdv-repo-auditor`, `sdv-dataset-coverage-auditor`,
  `sdv-harness-triage`, `sdv-issue-triage`).
- **MCP** — `context7` (live library docs for polars / pandas / Jinja2 / Docusaurus) and
  `sdv-docs` (exact sdv-py / R-package functions, Returns-table columns, provider endpoints
  and released datasets, served by `uvx` from `sportsdataverse[mcp]>=0.2.0b1`).

See [`sdv-toolkit/README.md`](sdv-toolkit/README.md) (rendered from `catalog.json`) for
the full, current inventory; this page names families, not counts, so it doesn't drift.

## Links

- Website: <https://sportsdataverse.org>
- Org: <https://github.com/sportsdataverse>
