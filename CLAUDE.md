# CLAUDE.md — sportsdataverse-org

The GitHub **org-profile + Claude Code plugin marketplace** repo for the
SportsDataverse org. `origin` is `github.com/sportsdataverse/.github`, so its
`profile/README.md` renders as the org landing page; `.claude-plugin/marketplace.json`
publishes the marketplace and the bundled `sdv-toolkit` plugin. Content-only — no build,
no CI, no package manifest.

## Structure

- `.claude-plugin/marketplace.json` — marketplace manifest (`name: sportsdataverse`,
  one plugin entry pointing at `./sdv-toolkit`).
- `README.md` — repo/marketplace README (install instructions, plugin inventory).
- `profile/README.md` + `profile/*.{png,svg}` — the org GitHub profile page and its logos.
- `sdv-toolkit/` — the bundled Claude Code plugin (shared across the ~40 SDV Python + R repos):
  - `.claude-plugin/plugin.json` — plugin manifest (wires `hooks` + `mcpServers`).
  - `.mcp.json` — MCP servers (`context7`, HTTP).
  - `hooks/hooks.json` — Pre/PostToolUse guards (see Conventions).
  - `agents/*.md` — 7 review agents (returns-table-auditor, docstring-auditor,
    provider-shape-mapper, polars-1x-reviewer, espn-parser-contract-reviewer,
    http-layer-reviewer, roxygen-doc-reviewer).
  - `skills/<name>/SKILL.md` — 12 skills (add-provider-source, add-espn-league,
    add-sport-parser, add-fox-league, add-cbs-league, add-yahoo-source,
    gen-returns-schema, capture-endpoint, regen-docs, new-example-notebook,
    sdv-r-returns-table, sdv-pkgdown-personalize).

## Conventions

- Two `README.md` files with distinct roles: the **root** one is the repo/marketplace
  page; **`profile/README.md`** is the rendered org profile. Edit the right one.
- `sdv-toolkit/hooks/hooks.json` encodes SDV house rules and is the canonical source for
  them: block edits to codegen-generated files (`*_espn_ext.py`, `tools/codegen/_generated/*`,
  `docs/docs/*/reference/*`); **block AI co-author / "generated with AI" trailers on
  commits**; warn on unbounded capture/crawl loops; remind to regenerate after codegen-source
  edits, to add a `returns_schema` when an endpoint declares a `parser`, and to
  `devtools::document()` after R edits.
- Plugin/marketplace manifests must stay in sync: a new plugin needs both a `plugins[]`
  entry in `marketplace.json` and its own `<plugin>/.claude-plugin/plugin.json`.
- Bump `sdv-toolkit/.claude-plugin/plugin.json` `version` when changing the plugin's
  hooks/agents/skills.

## Gotchas

- Adding a skill/agent is not enough to surface it — skills auto-discover from
  `skills/<name>/SKILL.md`, but the README inventory and (for top-level changes) the
  marketplace description are hand-maintained; update them too.
- No automation in this repo: no `.github/workflows`, no `package.json`, no deploy config.
  Don't invent a build/test command — there is none.
- Never add AI co-author trailers (the plugin's own hook blocks them repo-wide).

## Reference

- Org: <https://github.com/sportsdataverse> · Site: <https://sportsdataverse.org>
- Install: `claude plugin marketplace add sportsdataverse/sportsdataverse` then
  `claude plugin install sdv-toolkit@sportsdataverse`.
