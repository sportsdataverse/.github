# SportsDataverse

The [SportsDataverse](https://sportsdataverse.org) is a family of open-source sports-data
packages across Python and R — `sportsdataverse-py`, `hoopR`, `wehoop`, `cfbfastR`,
`baseballr`, `fastRhockey`, and more.

This repository also serves as the **SportsDataverse Claude Code plugin marketplace**.

## 🧩 Claude Code plugins

### Install

```sh
claude plugin marketplace add sportsdataverse/sportsdataverse
claude plugin install sdv-toolkit@sportsdataverse
```

### `sdv-toolkit`

Engineering tooling shared across the SportsDataverse Python + R repos — install once,
get identical automation everywhere.

- **Hooks** — block edits to codegen-generated (`# GENERATED`) files; block AI
  co-author/attribution trailers on commits; warn on unbounded capture/crawl loops;
  remind to regenerate after codegen-source edits, add a `returns_schema`, or
  `devtools::document()` after R edits.
- **Skills** (`/sdv-toolkit:<name>`) — `add-provider-source`, `add-espn-league`,
  `add-sport-parser`, `add-fox-league`, `add-cbs-league`, `add-yahoo-source`,
  `gen-returns-schema`, `capture-endpoint`, `regen-docs`, `new-example-notebook`,
  `sdv-r-returns-table`, `sdv-pkgdown-personalize`.
- **Agents** — `returns-table-auditor`, `docstring-auditor`, `provider-shape-mapper`,
  `polars-1x-reviewer`, `espn-parser-contract-reviewer`, `http-layer-reviewer`,
  `roxygen-doc-reviewer`.
- **MCP** — `context7` (live library docs for polars / pandas / Jinja2 / Docusaurus).

See [`sdv-toolkit/README.md`](sdv-toolkit/README.md) for the full inventory and the
conventions it encodes.

## Links

- Website: <https://sportsdataverse.org>
- Org: <https://github.com/sportsdataverse>
