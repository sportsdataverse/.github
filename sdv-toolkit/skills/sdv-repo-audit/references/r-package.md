# R package lenses (cfbfastR, hoopR, wehoop, baseballr, fastRhockey, oddsapiR, cfbplotR, sdvplotR, …)

Run R read-only in the audit tree: `Rscript -e 'pkgload::load_all("<W>", quiet = TRUE); …'`.
Several R installs exist; pick the version the repo's CI uses (`Rscript --version`).
Anything that writes (`devtools::document()`, `pkgdown::build_site()`) runs only in a
throwaway copy (`git -C <W> archive HEAD | tar -x -C <tmp>`), never in the main checkout.
General R concerns route to `sdv-r-reviewer`'s upstream skills; this audit owns the
claims, coverage and currency.

## 01 contributor-docs

**Files:** `NEWS.md`, `README.Rmd` + `README.md`, `CONTRIBUTING.md` / `.github/CONTRIBUTING.md`,
`CLAUDE.md`, `AGENTS.md`, `DESCRIPTION`, `cran-comments.md`, `.github/ISSUE_TEMPLATE/*`,
`.github/pull_request_template.md`, `.github/workflows/*.yml`, `_pkgdown.yml`, `vignettes/*.Rmd`.

| Claim kind | How to verify |
|---|---|
| `README.md` rendered from `README.Rmd` | the two agree (a stale knit is the usual drift); a code chunk's output matches the current function |
| Function names, arguments in prose and examples | exported? (`NAMESPACE`); argument exists (`formals(pkg::fn)`) |
| Counts ("N functions", "seasons 2002-2025") | `length(getNamespaceExports("pkg"))`; season floors against the loader's own check |
| `NEWS.md` | top heading `# pkg (development version)` between releases; released headings match CRAN/tags; bullets name the function and the PR/issue |
| `DESCRIPTION` | `Version`, `URL`/`BugReports` resolve, `Depends: R (>= x)` matches CI matrix, `Imports`/`Suggests` used (`grep -rn "pkg::"`) |
| Commands in CONTRIBUTING | `devtools::check()`, `pkgdown::build_site()`, test env vars (`NOT_CRAN`, live toggles) are the ones CI uses |
| Templates | `packageVersion("pkg")` asked for (not a field that does not exist); dropdowns list real sports/functions |
| `cran-comments.md` | current submission, not the last one |
| Contradictions / jargon | same fact twice with two values; internal ids, private repos, local paths |

## 02 companions

Plotting and surface companions: **cfbplotR** (cfbfastR), **nflplotR** (nflfastR family),
**sportyR** (surfaces for every sport), **sdvplotR** (SDV-wide theme/colors); data
companions: the matching `*-data` release repos and `sportsdataverse-py` for parity.

**Files:** `DESCRIPTION` `Suggests`, `vignettes/*`, `_pkgdown.yml` articles + navbar,
`README.Rmd` companion section, roxygen `@seealso`, the companion's sibling checkout.

| Check | How |
|---|---|
| Declared | companion in `Suggests` (not `Imports` unless used at runtime), with a version floor that exists on CRAN |
| Guarded | every use behind `rlang::check_installed()` / `requireNamespace()` |
| Vignette coverage matrix | one row per vignette/article: companion used? plot? coordinates or team colors shown only as a table? |
| Links both directions | this package's site links the companion; the companion's README/site links back and calls functions that exist in this package's **CRAN** version |
| Python parity | the sdv-py twin of each headline function exists and is named consistently (`load_cfb_pbp` ↔ `load_cfb_pbp`) |

## 03 coverage

**Files:** `_pkgdown.yml` (reference index, articles, navbar), `NAMESPACE`, `man/*.Rd`,
`README.Rmd`, `pkgdown/index.md` (if the home page is not the README), `vignettes/`.

| Check | How |
|---|---|
| Reference index complete | `pkgdown::check_pkgdown("<copy>")` (read-only check); exported functions missing from `_pkgdown.yml`, entries naming unexported or removed topics |
| Articles listed | every vignette appears under `articles:`; no dead entry |
| README function tables vs exports | set difference; hard-coded counts (`counts` probe) |
| Naming | section titles consistent with the sibling packages (hoopR ↔ wehoop mirror each other) |
| Dead links | `urlchecker::url_check("<copy>")`, plus a live sample of the site's navbar |
| Old names | renamed/deprecated functions still shown in README or articles (`lifecycle::deprecate_*` calls tell you which) |

## 04 currency

**Files:** `DESCRIPTION`, `NEWS.md`, `renv.lock` (if present), `.github/workflows/*`.

| Area | Commands |
|---|---|
| Release | `release` probe (`--cran <pkg>`); dev version `x.y.z.9000` between releases is normal, so weigh commits since the tag |
| CRAN health | WebFetch `https://cran.r-project.org/web/checks/check_results_<pkg>.html`: any ERROR/WARN flavor, a deadline notice |
| Outdated deps | `Rscript -e 'remotes::package_deps("<W>")'`; floors in `DESCRIPTION` far below what CI installs mean the floor is untested |
| Advisories | `osv` probe on `renv.lock` when one exists; otherwise say "no lock, n/a" |
| CI on main | R-CMD-check, test-coverage, pkgdown workflows at the SHA; pkgdown deploys only on push to main, so check its last run and the gh-pages head |
| Crons | every `schedule:` workflow's last 5 runs |
| Site freshness | gh-pages head commit vs the SHA; reference page for the newest export exists live |

## 05 polish

Rank: GitHub landing → CRAN page → pkgdown home → reference index → a reference page →
articles → news → 404.

| Check | How |
|---|---|
| README header | hex logo, CRAN/lifecycle/R-CMD-check badges resolve and agree; no dev-only install as the first line when it is on CRAN |
| `DESCRIPTION` Title/Description | title case, no "R package for", the description reads as a sentence; this is the CRAN page |
| Repo About box | `gh repo view o/r --json description,repositoryTopics,homepageUrl` (homepage = pkgdown URL) |
| pkgdown theme | SDV dark on-brand theme, shared CSS, favicon set (`pkgdown/favicon/`), no Bootstrap 5 regressions |
| Leaked internals | `leaks` probe over `man/`, `vignettes/`, `README*`, `NEWS.md`; roxygen comments render, so they count |
| Examples | `\dontrun{}` vs `\donttest{}` used deliberately; examples that error on the live site |
| Root clutter | `.Rbuildignore` covers dev files; tracked scratch (`*.Rproj.user`, `inst/doc` duplicates, data dumps) |
