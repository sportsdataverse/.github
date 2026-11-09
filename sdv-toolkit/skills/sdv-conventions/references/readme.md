# README standard (every archetype)

Owner decisions (2026-11-09): the standard is **inclusive** — every badge whose backing
exists goes in (no cap), `#` / `##` headings are **bold**, the authors list is
**hand-written**, every archetype carries the **full** ecosystem footer, and lifecycle follows
the version (`experimental` below 1.0, `stable` from 1.0). All 16 SDV R packages were brought
to this standard and pass `sdv-repo-audit/scripts/check_r_readme.py`; use it, not memory.

## Rules for every archetype

- Order is fixed; optional sections may be omitted, never reordered:
  H1 + logo → one-line tagline → badge block → body (archetype-specific) → ecosystem footer.
- H1: `# **<name>** <a href='<site>'><img alt="<name> hex logo" src='<logo>' align="right" .../></a>`.
  The `alt` is required: the link has no other accessible name.
- Bold every `#` and `##` heading (`## **Installation**`); one style per file.
- Badges live inside `<!-- badges: start -->` … `<!-- badges: end -->`, one per line, grouped
  registry → CI/quality → docs → community, `style=for-the-badge`.
- **A badge goes in only when its backing exists** (workflow file, registry listing,
  service). A badge for a missing workflow, or a CRAN badge on a package that is not on CRAN,
  is a defect.
- Links: `x.com`, never `twitter.com`; never "on Twitter". The GitHub-stars badge links the
  repo root, not `/stargazers` (that page 404s for logged-out readers).
- Never invent a URL, handle or function. Check every link you add returns 200
  (`curl -s -o /dev/null -w '%{http_code}' -L <url>`); an X handle that 404s (the account is
  gone) is dropped, keeping the person's GitHub link. Never in a README: internal repo names,
  local paths, task/rule ids, plan/ledger links, secret values, AI-tooling notes.
- Ecosystem footer, in order: `## **The SportsDataverse**` (ecosystem table) →
  `## **Follow the [SportsDataverse](https://x.com/SportsDataverse) on X and star this repo**`
  (X follow, stars, star-history picture when `star-history.yml` exists) →
  `## **Our Authors**` (hand-written: every `aut` in DESCRIPTION / pyproject, name link + X and
  GitHub badges; optional Contributors / Authors Emeritus / Special Thanks) →
  `## **Cheat sheet**` (only when `sportsdataverse.org/cheatsheets/<name>.pdf` — or a repo-named
  or combined sheet such as `cfbplotR-cfb4th-cfbseedR.pdf` — returns 200) →
  `## **Code of Conduct**` (when `CODE_OF_CONDUCT.md` / `CODE-OF-CONDUCT.md` exists) →
  `## **Citations**` → `## **License**`.

## Badge list (union of what the best-badged repos carry)

| Group | Badge | Backing | r-pkg | py | js | producer | app/service |
|---|---|---|---|---|---|---|---|
| Registry | CRAN version, CRAN downloads | on CRAN | ✓ | | | | |
| | R-universe | listed in `sportsdataverse.r-universe.dev` | ✓ | | | | |
| | Dev version (`Version-Number`) | — | ✓ | ✓ | ✓ | | |
| | PyPI version · Python versions · pepy downloads | on PyPI | | ✓ | | | |
| | npm version · downloads per member · Node engines | on npm | | | ✓ | | |
| CI/quality | R-CMD-check / tests / ci | the workflow file | ✓ | ✓ | ✓ | ✓ | ✓ |
| | Codecov — or a self-hosted `Coverage` badge (see r-package.md) | coverage workflow + upload | ✓ | ✓ | ✓ | | |
| | scrape / trigger / pipeline / orphan-scripts workflows | the workflow files | | | | ✓ | |
| Docs | pkgdown / Docusaurus deploy | the deploy workflow | ✓ | ✓ | ✓ | | opt |
| | Lifecycle (`experimental` < 1.0, `stable` ≥ 1.0) | — | ✓ | ✓ | ✓ | | |
| | License | LICENSE file | ✓ | ✓ | ✓ | ✓ | ✓ |
| Deploy | deploy status | deploy workflow | | | | | ✓ |
| Community | Contributors · GitHub stars · X Follow `@SportsDataverse` | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data | per-dataset freshness (status endpoint badges) | the `-data` repo workflows | data-backed | sdv-py | | generated | |

## Body per archetype

- **r-package** — `README.Rmd` is the source; `README.md` carries the same markdown (edit
  both identically when not re-knitting; new example code in plain ```` ```r ```` fences so the
  two stay equal). Installation: CRAN → R-universe → `pak::pak("<slug>")` with a commented
  fallback that installs `remotes` first. Then Quick start (2–4 calls to real exports, checked
  against NAMESPACE) → Data status (data-backed) → package-specific sections (kept) →
  Documentation (site, reference, every vignette, NEWS) → Breaking Changes (opt, link NEWS)
  → Companion packages → footer. Citations from `inst/CITATION`, else built from DESCRIPTION.
- **sdv-py** — doctoc TOC (pre-commit owns it); generated leagues/sources section; Data status
  table; Installation (pip, `uv add`, extras table); polars-first Quick start; AI agents / MCP;
  Companion packages (sdvplot, sportypy); footer + `CITATION.cff`.
- **python-package** — Installation (pip/uv, extras, JS twin); Usage with an image per
  example; Documentation (site, gallery, env-var table); Logos, trademarks and data (same text
  everywhere marks ship); footer.
- **js-package** — Packages table for monorepos (per-member npm badges live there);
  Installation (npm/pnpm, ESM import, engines); TS Usage; Documentation (site + typedoc);
  Development; trademarks if marks ship; footer. Each published member has a short README
  linking the root.
- **-raw / -data producer** — tagline says what is published, from where, how often, for
  whom. Pipeline diagram → What it produces / Data releases (tag · datasets · through · R and
  Python loader) → Usage (`scripts/NN_*` run order, reprocess vs recreate) → the three
  GENERATED blocks (`tools/render_readme_layout.py`, `render_reports_explainers.py`,
  `render_readme_status.py`) → Consumers → Stage inventory → Maintainer setup (secret
  *names* only) → full footer. No analysis write-ups in a producer README — they go to
  `docs/models/` and surface through the generated Reports block.
- **web-app** — tagline + live URL first; deploy/CI badges; current screenshot; Features;
  Stack; Run locally (env-var table: name · purpose · required); Deploy; data credits; footer.
- **db-service** — tagline (what it serves, who consumes it); architecture diagram;
  schema/catalog list (from migrations where possible); Run locally; Operations (backups,
  migrations, runbooks); Consumers; footer.

## Checking a README

`python <sdv-repo-audit>/scripts/check_r_readme.py --repo-dir <clone> --slug <owner/repo>`
(R packages; `--pending-coverage` while the coverage workflow is still in an open PR). It
resolves every badge's backing live (CRAN, R-universe, workflows, cheat sheet, CoC) and
checks heading boldness and order, the badge set in both directions, install lines, authors
vs DESCRIPTION, `twitter.com`, `/stargazers`, logo alt text, and Rmd/md heading parity.
Run it from a fresh clone of the pushed branch before merging; do not trust an agent's
"PASS".
