# sdv-toolkit

A Claude Code plugin packaging the engineering conventions of the **SportsDataverse** repos
(the polars/codegen Python packages + the ~10 roxygen/pkgdown R packages) into reusable
skills, agents, hooks, and an MCP server. Install once, get identical automation across all
~40 SDV repos instead of copy-pasting `.claude/` dirs.

## Install

From this dotfiles repo (local marketplace):

```sh
# add the local marketplace (the directory that holds .claude-plugin/marketplace.json)
claude plugin marketplace add ~/Documents/GitHub-Data/sdv-dev/dotfiles_saiemgilani/claude/plugins
# install the plugin
claude plugin install sdv-toolkit@sdv-plugins
```

Or, if you publish `claude/plugins/` as its own git repo:

```sh
claude plugin marketplace add saiemgilani/sdv-plugins
claude plugin install sdv-toolkit@sdv-plugins
```

Verify: `claude plugin list` should show `sdv-toolkit` and its skills/agents/hooks.

## What's inside

### ⚡ Hooks (`hooks/hooks.json`) — fire on tool events, before/after edits

| Hook | Event | Effect |
|---|---|---|
| block-generated-files | PreToolUse(Edit/Write) | **Blocks** edits to `*_espn_ext.py`, `tools/codegen/_generated/*`, generated `docs/docs/*/reference/*` (they carry `# GENERATED -- DO NOT EDIT`). Tells you to edit the YAML/template + regenerate. |
| no-ai-attribution | PreToolUse(Bash) | **Blocks** `git commit`/`gh` with `Co-Authored-By:` AI trailers or "generated with Claude" — enforces the SDV sole-human-attribution rule. |
| crawl-runaway-guard | PreToolUse(Bash) | **Warns** when a capture/crawl runs without a visible attempt bound (the CBS 404-flood lesson). |
| codegen-regen-reminder | PostToolUse(Edit/Write) | Nudges `generate.py` + `--check` after editing codegen sources (`endpoints/*.yaml`, templates, parsers, `generate.py`, `spec.py`). |
| returns-schema-reminder | PostToolUse(Edit/Write) | Flags an endpoint YAML that declares `parser:` but no `returns_schema:`. |
| r-document-reminder | PostToolUse(Edit/Write) | Nudges `devtools::document()` after editing `R/*.R`. |

### 🎯 Skills (`skills/`) — invoke with `/sdv-toolkit:<name>`

| Skill | Purpose |
|---|---|
| `add-provider-source` | Meta-skill: add a league/source for any provider (ESPN/Fox/CBS/Yahoo/247/Torvik) — capture → returns doc → catalog → wrapper. |
| `add-espn-league` | Register a new ESPN league family (leagues.yaml row, pre-create dir+`__init__`, regenerate, gated live test, drift gate). |
| `add-sport-parser` | Scaffold a sport-specific parser module + `_SPORT_PARSER_OVERRIDES` routing + fixtures (the soccer/cricket pattern). |
| `add-fox-league` | Fox Bifrost API (`apikey`+`api-version`, `{sport}` path param). |
| `add-cbs-league` | CBS NAPI (auth-free data-backed resources). |
| `add-yahoo-source` | Yahoo scraper source. |
| `gen-returns-schema` | Generate a `col_name|type|description` returns table (Python schema YAML or R roxygen) from a payload / DataFrame. |
| `capture-endpoint` | Hardened, provider-agnostic single-body capture (structured id-walk, error-envelope skip). |
| `regen-docs` | `generate.py --docs` → Docusaurus build check → release snapshot. |
| `new-example-notebook` | Scaffold a per-sport `examples/notebooks/0X_<sport>_intro.ipynb`. |
| `sdv-r-returns-table` | Generate roxygen `@return` markdown tables matching the Python returns convention. |
| `sdv-pkgdown-personalize` | Apply the bespoke SDV pkgdown theming + fix the shared `extra.css` BS5 bugs. |

### 🤖 Agents (`agents/`) — specialized reviewers/auditors

| Agent | Reviews |
|---|---|
| `returns-table-auditor` | Functions/endpoints missing `col_name|type|description` returns tables or with empty descriptions (Python + R). |
| `docstring-auditor` | Google-style napoleon docstrings (`Args/Returns/Raises/Example`, `See Also`, no raw `>>>`). |
| `provider-shape-mapper` | Maps a captured provider payload → top-level-key table + returns table + divergence notes. |
| `http-layer-reviewer` | `dl_utils.download()` + capture/crawl code against the retry/pooling/backoff/bound-to-attempts rules. |
| `polars-1x-reviewer` | Flags 0.18-era polars API (`groupby`/`with_row_count`/`.apply(`/`pl.count()`/`cumsum`/`set_at_idx`/`how="outer"`/lookaround regex). |
| `espn-parser-contract-reviewer` | Parser contract (polars default, zero-row-on-empty/never-raise, snake_case, `return_as_pandas`) + `ENDPOINT_PARSERS` coverage. |
| `roxygen-doc-reviewer` | R roxygen completeness (`@param`/`@return` table/`@examples`) + `_pkgdown.yml` reference coverage. |

### 🔌 MCP (`.mcp.json`)

- **context7** — live library docs (polars 1.x / pandas / Jinja2 / Docusaurus). The 0.18→1.x churn is exactly its sweet spot.

## Conventions encoded

- Codegen is the source of truth; never hand-edit `# GENERATED` files.
- Returns tables are `col_name | type | description` with **R-style types** (`integer`/`character`/`double`/`logical`) — shared Python ⇄ R so paired functions document identically.
- Parser contract: polars default, pandas via `return_as_pandas=True`, empty → zero-row frame (never raise), snake_case columns.
- polars 1.x only (no 0.18 API); Rust regex has no lookaround.
- No AI attribution on commits/PRs.
