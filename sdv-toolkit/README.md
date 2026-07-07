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
| sdd-namespacing-guard | PreToolUse(Edit/Write) | **Blocks** flat `.superpowers/sdd/task-*.md` writes — task artifacts must be namespaced under `.superpowers/sdd/<plan-slug>/` (flat names clobber across plans; `progress.md` stays at the root). |
| uv-lock-relock-guard | PreToolUse(Bash) | **Warns** on `git commit` when `uv.lock` is staged without `pyproject.toml` — the silent `uv run mypy/pytest` re-lock riding into an unrelated commit. |
| recipe-dep-sync-guard | PreToolUse(Bash) | **Warns** on `git commit` when `pyproject.toml` is staged but `recipe/meta.yaml` (present in the repo) is not — runtime deps must be mirrored into the conda recipe (the rapidfuzz lesson). |

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
| `pandas-to-polars` | Convert pandas DataFrame/Series code → idiomatic **polars 1.2+** (idiom map, `null`≠`NaN`, no-index model, SDV 1.x conventions) — incl. the `0.36-live` pandas→polars reconciliation. |
| `port-r-to-python` | Port R logic (nflfastR/cfbfastR/baseballr/hoopR…) → sdv-py polars, parity-test-first. |
| `port-python-to-r` | Reverse: port sdv-py Python logic → an SDV R package (tidyverse/data.table idiom map), parity-test-first. |
| `preflight` | Fast scoped local sweep (ruff + mypy ratchet + tests on changed files only) before commit/PR. |
| `ship` | Gated end-to-end PR flow: regen codegen docs → lint → full pytest → commit → push → wait for CI green → confirm merge. |
| `release` | Cut a sdv-py PyPI release: bump version, CHANGELOG entry, docs snapshot, tag a GitHub Release (triggers the publish workflow). |
| `address-bot-reviews` | Triage + resolve CodeRabbit/Copilot review threads on a PR (fix the valid, reply/decline the rest, resolve each). |
| `stack` | Land stacked PRs bottom-up: map the stack, merge, retarget + `rebase --onto` after each squash-merge, re-run the codegen drift gate at every new head; depth cap ~4. |
| `scrape-job` | Generate a user-executable runbook for any >3-min scraping/backfill job: unbuffered timestamped logging, live watch command, resumable checkpoint, env-only rate tuning, per-site gotchas (NBA TLS-hang, NCAA proxy, ESPN 403). Raw-repo aware: output saves into the owning `-raw` repo's canonical committed tree (`nfl/raw/{season}/{game_id}.json`, `cfb/json/…`), launcher in its `scripts/`, `*_schedule_master.parquet` flag upsert. |
| `build-data` | The `-data` repo pipeline: ingest the sibling `-raw` tree → builder module per dataset (`<x>_data_build/`) → validation-harness + parity-vs-prior-release checks → publish (git commit + per-file `gh release upload --clobber`, release-map aware) → wire `daily_*_processor.sh`. |

### 🤖 Agents (`agents/`) — specialized reviewers/auditors

| Agent | Reviews |
|---|---|
| `returns-table-auditor` | Functions/endpoints missing `col_name|type|description` returns tables or with empty descriptions (Python + R). |
| `docstring-auditor` | Google-style napoleon docstrings (`Args/Returns/Raises/Example`, `See Also`, no raw `>>>`). |
| `provider-shape-mapper` | Maps a captured provider payload → top-level-key table + returns table + divergence notes. |
| `http-layer-reviewer` | `dl_utils.download()` + capture/crawl code against the retry/pooling/backoff/bound-to-attempts rules. |
| `polars-1x-reviewer` | Flags outdated polars in 3 tiers vs the installed 1.x (lockfile 1.42): removed pre-1.0 API (runtime errors), within-1.x deprecations (`melt`/`pivot(columns=)`/`collect(streaming=True)`/`map_dict`/`min_periods`/`take`/`clip_min`/`json_extract`/…), and perf/modernize advisories (`map_elements` UDFs, eager-read) — plus the bool-mask + lookaround-regex conventions. |
| `espn-parser-contract-reviewer` | Parser contract (polars default, zero-row-on-empty/never-raise, snake_case, `return_as_pandas`) + `ENDPOINT_PARSERS` coverage. |
| `roxygen-doc-reviewer` | R roxygen completeness (`@param`/`@return` table/`@examples`) + `_pkgdown.yml` reference coverage. |
| `extraction-semantics-reviewer` | (sdv-py Tier-2 validation) Triages an `extraction` WARN — judges from the null-row `cleaned_text` samples whether the parser missed a named participant or the field is legitimately null for that play type. |
| `anomaly-triage-reviewer` | (sdv-py Tier-2 validation) Triages a `sweep` WARN (null-rate spike / mean-shift vs prior release) — real regression vs expected data change (rule/era, sparse new column, schedule mix). |
| `parity-divergence-reviewer` | (sdv-py Tier-2 validation) Triages a `numeric_parity` WARN (corr < oracle floor) — real model/producer regression vs documented acceptable divergence (WPA SNR, kickoff/PAT feature-substitution, NFL raw-vs-model-domain). |
| `leakage-reviewer` | (sdv-py Tier-2 validation) Triages a `leakage_lint` (Python/R ungrouped lag/cum) or `boundary_leakage` (cumulative non-reset) WARN — real cross-game leak vs already-grouped / single-game / intentional, accounting for the linters' documented heuristic limits. |

### 🔌 MCP (`.mcp.json`)

- **context7** — live library docs (polars 1.x / pandas / Jinja2 / Docusaurus). The 0.18→1.x churn is exactly its sweet spot.

## Conventions encoded

- Codegen is the source of truth; never hand-edit `# GENERATED` files.
- Returns tables are `col_name | type | description` with **R-style types** (`integer`/`character`/`double`/`logical`) — shared Python ⇄ R so paired functions document identically.
- Parser contract: polars default, pandas via `return_as_pandas=True`, empty → zero-row frame (never raise), snake_case columns.
- polars 1.x only (no 0.18 API); Rust regex has no lookaround.
- No AI attribution on commits/PRs.
