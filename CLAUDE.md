# CLAUDE.md — sportsdataverse-org

The GitHub **org-profile + Claude Code plugin marketplace** repo for the
SportsDataverse org. `origin` is `github.com/sportsdataverse/.github`, so its
`profile/README.md` renders as the org landing page; `.claude-plugin/marketplace.json`
publishes the marketplace and the bundled `sdv-toolkit` plugin.

## Structure

- `.claude-plugin/marketplace.json` — marketplace manifest (`name: sportsdataverse`,
  one plugin entry pointing at `./sdv-toolkit`). Its plugin description is
  **rendered** by `sdv-toolkit/tools/render.py`.
- `README.md` — repo/marketplace README (install instructions).
- `profile/README.md` + `profile/*.{png,svg}` — the org GitHub profile page and its logos.
- `status/` — `ecosystem.{json,md}`, a nightly org snapshot written by the
  `ecosystem-status.yml` bot. Never edit by hand.
- `sdv-toolkit/` — the bundled Claude Code plugin (shared across the ~40 SDV Python + R repos):
  - `catalog.json` — **source of truth** for the skill and agent inventory.
  - `.claude-plugin/plugin.json` — plugin manifest (version, `hooks`, `mcpServers`);
    its description is rendered from the catalog.
  - `README.md` — skill/agent tables, **rendered** from the catalog (do not hand-edit).
  - `skills/<name>/SKILL.md` (+ `references/`, `scripts/`) and `agents/*.md` — see
    `catalog.json` or `README.md` for the current list; counts are not repeated here
    because they drift.
  - `hooks/hooks.json` + `hooks/sdv_router.py` — guard hooks and the SessionStart
    archetype router (`hooks/test_sdv_router.py`).
  - `tools/` — `check_catalog.py`, `render.py`, the README renderers, and their
    `test_*.py` (including `test_pr_context.py` for `skills/sdv-review-pr/scripts/`).
  - `.mcp.json` — MCP servers (`context7`, HTTP).

## CI

`.github/workflows/`:
- `sdv-toolkit-catalog.yml` — on changes under `sdv-toolkit/**` or `.claude-plugin/**`:
  `python -m unittest discover -s tools -p 'test_*.py'`, `python tools/check_catalog.py .`,
  and `python tools/render.py --check` (run from `sdv-toolkit/`).
- `ecosystem-status.yml` — scheduled `status/` snapshot (`[skip ci]` commits).
- `orphan-scripts.yml` — reusable `workflow_call` gate used by the `-raw`/`-data` repos.

Run the same three catalog commands locally before pushing a toolkit change, plus
`python -m unittest discover -s hooks -p 'test_*.py'` for router changes.

## Conventions

- Toolkit changes land here **first** (branch + PR), then are mirrored to
  `saiemgilani/dotfiles:claude/plugins/sdv-toolkit/` in a follow-up PR. Compare the
  mirror with `diff -r --strip-trailing-cr`.
- A skill/agent/hook change bumps `sdv-toolkit/.claude-plugin/plugin.json` `version`,
  adds or updates its `catalog.json` row, and re-renders with `python tools/render.py`.
  A new skill without a catalog row fails CI.
- `sdv-toolkit/hooks/hooks.json` encodes SDV house rules: block edits to
  codegen-generated files (`*_espn_ext.py`, `tools/codegen/_generated/*`,
  `docs/docs/*/reference/*`); **block AI co-author / "generated with AI" trailers**;
  warn on unbounded capture/crawl loops; remind to regenerate after codegen-source
  edits, to add a `returns_schema` when an endpoint declares a `parser`, and to
  `devtools::document()` after R edits.
- Two `README.md` files with distinct roles: the **root** one is the repo/marketplace
  page; **`profile/README.md`** is the rendered org profile. Edit the right one.

## Gotchas

- `sdv-toolkit/README.md` and `.claude-plugin/marketplace.json` are committed with
  **CRLF** line endings. `render.py` writes LF on Linux, so restore CRLF after
  rendering or the diff rewrites every line.
- The Bash PreToolUse guard blocks any command whose *text* contains the AI-trailer
  pattern — edit code that mentions it with a file editor, not a shell heredoc.
- Changes reach sessions only after `claude plugin update sdv-toolkit` and a restart;
  the installed cache is version-pinned.
- Never add AI co-author trailers (the plugin's own hook blocks them repo-wide).

## Reference

- Org: <https://github.com/sportsdataverse> · Site: <https://sportsdataverse.org>
- Install: `claude plugin marketplace add sportsdataverse/.github` then
  `claude plugin install sdv-toolkit@sportsdataverse`.
