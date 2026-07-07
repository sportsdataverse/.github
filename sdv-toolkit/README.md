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
| ruff-format-on-edit | PostToolUse(Edit/Write) | Auto-runs `ruff format` on any just-edited `.py` file (venv exe `.venv/Scripts/ruff.exe` → `.venv/bin/ruff` → PATH; silent no-op when absent). **Format-only by design** — never `check --fix` (the F401 autofix strips a just-added not-yet-used import) and never `uv run` (which can silently re-lock `uv.lock`). |
| codegen-regen-reminder | PostToolUse(Edit/Write) | Nudges `generate.py` + `--check` after editing codegen sources (`endpoints/*.yaml`, templates, parsers, `generate.py`, `spec.py`). |
| returns-schema-reminder | PostToolUse(Edit/Write) | Flags an endpoint YAML that declares `parser:` but no `returns_schema:`. |
| r-document-reminder | PostToolUse(Edit/Write) | Nudges `devtools::document()` after editing `R/*.R`. |
| sdd-namespacing-guard | PreToolUse(Edit/Write) | **Blocks** flat `.superpowers/sdd/task-*.md` writes — task artifacts must be namespaced under `.superpowers/sdd/<plan-slug>/` (flat names clobber across plans; `progress.md` stays at the root). |
| uv-lock-relock-guard | PreToolUse(Bash) | **Warns** on `git commit` when `uv.lock` is staged without `pyproject.toml` — the silent `uv run mypy/pytest` re-lock riding into an unrelated commit. |
| recipe-dep-sync-guard | PreToolUse(Bash) | **Warns** on `git commit` when `pyproject.toml` is staged but `recipe/meta.yaml` (present in the repo) is not — runtime deps must be mirrored into the conda recipe (the rapidfuzz lesson). |
| codegen-push-drift-guard | PreToolUse(Bash) | **Warns** on `git push` when the push range touches Python/codegen sources but contains no regenerated outputs (`docs/docs/`, `sportsdataverse/parsed/`) — run the drift gate at the branch head first (CI fails on drift). |
| post-commit-verify | PostToolUse(Bash) | After any `git commit`: prints HEAD + the leftover modified-file count, so a silently-aborted commit (ruff-format / doctoc rewrote staged files) is caught immediately instead of assumed successful. |
| fixture-provenance-guard | PreToolUse(Bash) | **Warns** on `git commit` when staged adds include `tests/fixtures/**/*.parquet\|json\|csv` in a directory with no README.md (present or staged) — committed fixtures need a provenance README (source, capture date, row counts, id dtypes). |
| main-commit-guard | PreToolUse(Bash) | **Warns** on `git commit` while on `main`/`master` in a repo whose origin is `sportsdataverse/*` — the convention is branch + PR. Scoped by remote, so dotfiles/config repos stay exempt. |

### 🎯 Skills (`skills/`) — every skill is `sdv-`-prefixed; invoke with `/sdv-<name>` (or fully qualified: `/sdv-toolkit:sdv-<name>`)

| Skill | Purpose |
|---|---|
| `sdv-add-provider-source` | Meta-skill: add a league/source for any provider (ESPN/Fox/CBS/Yahoo/247/Torvik) — capture → returns doc → catalog → wrapper. |
| `sdv-add-espn-league` | Register a new ESPN league family (leagues.yaml row, pre-create dir+`__init__`, regenerate, gated live test, drift gate). |
| `sdv-add-sport-parser` | Scaffold a sport-specific parser module + `_SPORT_PARSER_OVERRIDES` routing + fixtures (the soccer/cricket pattern). |
| `sdv-add-fox-league` | Fox Bifrost API (`apikey`+`api-version`, `{sport}` path param). |
| `sdv-add-cbs-league` | CBS NAPI (auth-free data-backed resources). |
| `sdv-add-yahoo-source` | Yahoo scraper source. |
| `sdv-gen-returns-schema` | Generate a `col_name|type|description` returns table (Python schema YAML or R roxygen) from a payload / DataFrame. |
| `sdv-capture-endpoint` | Hardened, provider-agnostic single-body capture (structured id-walk, error-envelope skip). |
| `sdv-regen-docs` | `generate.py --docs` → Docusaurus build check → release snapshot. |
| `sdv-new-example-notebook` | Scaffold a per-sport `examples/notebooks/0X_<sport>_intro.ipynb`. |
| `sdv-r-returns-table` | Generate roxygen `@return` markdown tables matching the Python returns convention. |
| `sdv-pkgdown-personalize` | Apply the bespoke SDV pkgdown theming + fix the shared `extra.css` BS5 bugs. |
| `sdv-pandas-to-polars` | Convert pandas DataFrame/Series code → idiomatic **polars 1.2+** (idiom map, `null`≠`NaN`, no-index model, SDV 1.x conventions) — incl. the `0.36-live` pandas→polars reconciliation. |
| `sdv-port-r-to-python` | Port R logic (nflfastR/cfbfastR/baseballr/hoopR…) → sdv-py polars, parity-test-first. |
| `sdv-port-python-to-r` | Reverse: port sdv-py Python logic → an SDV R package (tidyverse/data.table idiom map), parity-test-first. |
| `sdv-preflight` | Fast scoped local sweep (ruff + mypy ratchet + tests on changed files only) before commit/PR. |
| `sdv-ship` | Gated end-to-end PR flow: regen codegen docs → update changelog/docs/tutorials → lint → full pytest → commit + verify it landed → push → CI green → triage bot reviews (CodeRabbit/Sourcery/Copilot) → confirm merge → session note. |
| `sdv-release` | Cut a sdv-py PyPI release: bump version, CHANGELOG entry, docs snapshot, tag a GitHub Release (triggers the publish workflow). |
| `sdv-address-bot-reviews` | Triage + resolve CodeRabbit/Sourcery/Copilot review threads on a PR (fix the valid, reply/decline the rest, resolve each). |
| `sdv-stack` | Land stacked PRs bottom-up: map the stack, merge, retarget + `rebase --onto` after each squash-merge, re-run the codegen drift gate at every new head; depth cap ~4. |
| `sdv-model-spine` | Execute a model-spine plan (the ClaudeCowork backlog) end-to-end: isolated worktree + baseline → Phase-0 oracle harness (metrics/constants/leakage split) → per-task TDD with verified commits → oracle gates (never-lower rule, early gate preview) → sibling-league shims → mypy/codegen close-out → reviewer pass → session restart prompt. |
| `sdv-capture-oracle` | Capture an external oracle corpus to committed fixtures: column contracts, Utf8-id discipline, probe-before-code, the name-crosswalk recipe (contracting normalizer + candidate keys + alias table + match-rate reporting), sample-don't-sweep rate-limit rules, mandatory provenance README. |
| `sdv-scrape-job` | Generate a user-executable runbook for any >3-min scraping/backfill job: unbuffered timestamped logging, live watch command, resumable checkpoint, env-only rate tuning, per-site gotchas (NBA TLS-hang, NCAA proxy, ESPN 403). Raw-repo aware: output saves into the owning `-raw` repo's canonical committed tree (`nfl/raw/{season}/{game_id}.json`, `cfb/json/…`), launcher in its `scripts/`, `*_schedule_master.parquet` flag upsert. |
| `sdv-build-data` | The `-data` repo pipeline: ingest the sibling `-raw` tree → builder module per dataset (`<x>_data_build/`) → validation-harness + parity-vs-prior-release checks → publish (git commit + per-file `gh release upload --clobber`, release-map aware) → wire `daily_*_processor.sh`. |

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
| `port-parity-reviewer` | Audits a cross-language port (R↔Python, TS/Scala→Python) for the recurring bug classes — int-vs-str ID joins, `"123.0"` float-id stringification, regex case/lookaround divergence, 1-based indexing, NA/null/NaN drift, silent recycling — and verifies parity tests assert against REAL source-language fixtures (golden-master), not synthetic only. |
| `oracle-gate-reviewer` | Audits NEW model/validation code before merge (vs the Tier-2 agents, which triage harness findings): as-of-date leakage actually enforced, gates derived from observed values + never lowered, oracle-join dtype/match-rate hygiene, metric-model fit (Brier+calibration / MAE-vs-market / Spearman / sim slope), fitted-constant + fixture provenance, train/holdout separation. |
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
