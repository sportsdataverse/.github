# Python package lenses (sportsdataverse-py and other PyPI packages)

Rows tagged **[sdv-py]** apply only where `tools/codegen/generate.py` exists. Measure
counts by importing the package **from the audit tree**, never the editable install in
the main checkout:

```sh
cd <W> && PYTHONPATH=<W> uv run --frozen --no-sync python -c "import sportsdataverse as s, pathlib; assert pathlib.Path(s.__file__).resolve().is_relative_to(pathlib.Path('<W>').resolve()); ..."
```

`uv run` without `--no-sync` can re-lock or strip extras; check `git status` in the main
checkout afterwards.

## 01 contributor-docs

**Files:** `CHANGELOG.md`, `changelog.d/*` (+ its `README.md` contract), `CONTRIBUTING.md`,
`README.md`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`,
`.github/ISSUE_TEMPLATE/*`, `.github/pull_request_template.md`, `pyproject.toml`,
`.pre-commit-config.yaml`, `.github/workflows/*.yml`, `recipe/meta.yaml`.

Check every concrete claim; list the ones that held under "Verified accurate".

| Claim kind | How to verify |
|---|---|
| Counts (wrappers, loaders, families, parsers, leagues) | import + `len(__all__)` / `dir()` / registry parse; quote the command |
| Module paths, scripts, workflows, test files, private helpers named in prose | `test -e` / `git ls-files` at the SHA; grep the symbol |
| Commands (`uv run …`, `python tools/…`, `--check`) | run them read-only (`--help`, `--check`, dry-run) in the audit tree |
| Env vars | grep the code for the exact name (`SDV_PY_*`); a documented var nothing reads is wrong |
| Version, `requires-python`, classifiers, extras, dependency floors | `pyproject.toml`; extras vs the docs' extras list; `[all]` composition |
| "Newest release", "since X", "removed in X" | against the `release` probe; deprecation windows against the stated policy (sdv-py: two minors) and `removed_in=` in code |
| Links | relative links resolve; external links sampled (WebFetch) |
| Template dropdowns / required fields | against the registry (`docs/src/data/leagues.json`) and the code (a field asking for `pkg.__version__` must exist: `python -c "import pkg; pkg.__version__"`) |
| doctoc TOCs | match the headings |
| Fragments **[sdv-py]** | `fragments` probe: PR number per bullet, ≤ 3 lines, `**Area:**` lead, no internal ids; group counts |
| Contradictions | the same fact in two files with two values (CLAUDE.md vs copilot-instructions is the usual pair) |
| Internal jargon | ids (`B-M31`, `C-L3`, `Task 3.1`), private repos, vendor names, internal run names in public files |
| conda recipe **[sdv-py]** | `python tools/check_recipe_mirror.py` |

Trap: a body or doc written before the last refactor (sdv-py #1020 moved `providers/`,
`analytics/`, `basketball/*`) is the likeliest stale claim; grep old paths.

## 02 companions

sdv-py companions: **sdvplot** (charts, team colors/logos, themes) and **sportypy**
(GPL-3.0 surface drawing, deliberately its own extra). Other Python packages: whatever
their README calls a companion.

**Files:** `pyproject.toml` extras, `uv.lock` entries for each companion, `examples/notebooks/*.ipynb`,
`docs/docs/**` mentions, docstring `See Also` blocks, `CLAUDE.md` companion table,
`docs/src/data/companions.yaml` (if present); the companion's own checkout (sibling under
`GitHub-Data/sdv-dev/`, read it, don't clone) for the reverse direction.

| Check | How |
|---|---|
| Pins vs latest released | extra floor vs PyPI JSON for the companion; lock version |
| What each extra actually installs | the companion's own base deps vs what notebooks import (sdv-py's `[sdvplot]` brought no matplotlib or sportypy, so every plotting notebook's first import failed) |
| Extras on the *published* version | `git show v<registry>:pyproject.toml`: an extra that exists only on main installs nothing for `pip install pkg[extra]` |
| Code integration | `grep -rn "import <companion>"`; lazy-import + install-hint pattern, or none (acceptable for a companion: say so) |
| Notebook coverage matrix | one row per notebook: companion used? plots? coordinates shown only as a table (a missed chart)? install line correct for its imports? |
| Docs links both directions | sdv-py → companion URLs consistent (docs site vs GitHub); companion → sdv-py module paths exist on main **and** on the companion's pinned sdv-py version |

Trap: a companion cookbook importing a module that exists on main but not in the
latest release (sdvplot's `sportsdataverse.euroleague` against a `>=0.1.4` pin).

## 03 coverage

**Files:** registries — `docs/src/data/leagues.json`, `tools/codegen/sources.yaml`,
`tools/codegen/endpoints/leagues.yaml` **[sdv-py]**; front pages — `README.md`,
`docs/docs/intro.md`, `docs/src/pages/index.*`, `docs/sidebars.ts`, `docs/docusaurus.config.ts`
(navbar/footer), `docs/docs/ecosystem.md`, `docs/docs/quality-of-life.md`; discovery helpers
(`discover.py`, `function_count()`, `list_functions()`).

| Check | How |
|---|---|
| Ground truth first | a measured table (registry size by group, provider count, public function count) with the command for each |
| Every registry entry on each front page | set difference per page: missing, extra, prose-only |
| Hand-written vs generated | name which pages are generated (complete by construction) and which lag |
| Hard-coded counts | `counts` probe; each number against the measured table |
| Naming | page titles / H1 / sidebar labels vs the registry's display names (raw slugs such as `NBASL_LV`, `EUROLEAGUE` leak through) |
| Order and grouping | home grid and tables follow the registry's sport/group order |
| Dead links | live-site sample (WebFetch) of nav, footer, hero buttons; `onBrokenLinks` setting |
| Old paths | grep pre-refactor import paths in README, docs, notebooks |
| Code that hard-codes a registry | a helper listing 45 of 105 leagues is a code bug: batch it with a test |

## 04 currency

**Files:** `pyproject.toml`, `uv.lock`, `changelog.d/`, `CHANGELOG.md`, `.github/workflows/*`,
`.github/dependabot.yml`, `sdv_docs/schema.py` + `.github/workflows/docs-index.yml` **[sdv-py]**,
`docs/docusaurus.config.ts` (search, llms plugin), `context7.json`.

| Area | Commands |
|---|---|
| Release | `release` probe (`--pypi <dist>`); `gh api repos/o/r/releases?per_page=10`; publish workflow trigger (`python-publish.yml` on `release: published`) and its last run |
| Unreleased | fragment counts by group (breaking count → migration notes needed); commits since the registry tag |
| Outdated deps | `uv tree --outdated --depth 1` (in the audit tree, `--frozen`); direct deps only unless a transitive one has an advisory |
| Advisories | `osv` probe on `uv.lock`; for each hit `uv tree --invert --package <pkg>` → runtime, extra, or dev; Dependabot alerts on? (`gh api repos/o/r/vulnerability-alerts -i` → 204 on, 404 off) |
| Docs MCP index **[sdv-py]** | `gh release view docs-index --json assets` asset `updatedAt` vs the merge time; download `manifest_v1.json`, compare `sdv_py_commit` to the SHA; `SCHEMA_VERSION` vs the hard-coded names in `docs-index.yml` |
| Site search / llms.txt | search plugin version vs npm latest; built at deploy? gh-pages head commit vs the SHA; live `Last-Modified`; `llms.txt` contains a recently added module |
| CI on main | `gh run list --branch main --limit 30 --json name,conclusion,headSha,event`; anything not success at the SHA |
| Crons | `gh run list --workflow <cron>.yml --limit 5` for every `schedule:` workflow; three reds in a row is a finding even when a fix merged ("not yet proven by a green run") |
| Drift issues | `gh issue list --label live-tests:drift --state open` |
| Workflow registry | `gh workflow list --all`: registered workflows whose file is gone, `disabled_manually` ones (deliberate?) |

## 05 polish

Rank by visibility: GitHub landing → PyPI page → docs home → getting started → league
index → a reference page → tutorials → changelog → 404.

**Files / pages:** `README.md` header, `gh repo view o/r --json description,repositoryTopics,homepageUrl`,
PyPI JSON `info.summary`, live pages (WebFetch), `docs/docs/**` front matter,
`docs/docusaurus.config.ts` (title, tagline, social card), `git ls-files` at the root.

| Check | How |
|---|---|
| README header | badges resolve and agree (two coverage badges with different numbers), logo URL not on a `master` branch or 1 MB+, no HTML in the TOC, no orphan sentences |
| Repo About box | description says what it is in one line; topics present; homepage set |
| Home page | install line, a code sample, a value statement above the fold, not just a wall of links |
| Rendering bugs | admonitions printed literally (`:::caution Deprecated` needs `:::caution[Deprecated]` in Docusaurus 3) |
| Leaked internals | `leaks` probe over tracked public files; **also** the rendered reference pages (docstrings), since that is where `ponytail:`, `Task 3.1`, `sdv-internal-refs` reached the site |
| Reference pages | type names match the language (R `character/numeric` in a Python package's returns tables); summaries that are only `GET /path` |
| Tutorials | executed notebooks publishing tracebacks, HTML dumps, auth errors |
| Metadata/SEO | `description:` front matter on hand-written pages; page title and tagline; og:image; the search snippet is not badge alt text |
| Root clutter | `git ls-files` top level: duplicate logos, dead configs (`.flake8` under ruff), tracked files under ignored dirs (`git ls-files -ci --exclude-standard`), stray result/baseline files, agent state dirs |
