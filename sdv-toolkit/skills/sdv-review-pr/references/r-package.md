# r-package — cfbfastR, hoopR, wehoop, baseballr, fastRhockey, oddsapiR, cfbseedR, softballR, sportsdataverse-R, cfbplotR, sportsdataverse-data

CRAN / r-universe packages wrapping live APIs, plus `load_*` loaders over
sportsdataverse-data release assets. Recognise from `DESCRIPTION` + `NAMESPACE` +
`R/` + `man/` (Python `-data`/`-raw` repos also carry `DESCRIPTION` + `R/` but no
`NAMESPACE`/`man/`).

CI: `R-CMD-check` runs on PRs; **`pkgdown` runs on push to `main` only** (every SDV R
package except sportyR); every package `.Rbuildignore`s `^vignettes`, so vignette code
runs only after merge. softballR has no CI. A green PR is not evidence `main` will be
green — list the post-merge pkgdown run in the report's watch list.

**Routed, not restated:** roxygen `@param`/`@return` table/`@examples`, `_pkgdown.yml`
reference coverage, tidy idiom, style, CRAN, performance → `sdv-r-reviewer` (by lens);
R↔Python parity → `sdv-parity-reviewer`. Maintainer-owned packages (sportyR, cfb4th,
baseballr, mlbplotR) → `other-repos.md` third-party mode.

## Rules

- **R-1** `[blocker]` A PR touching `vignettes/*.Rmd`, `_pkgdown.yml`, `NAMESPACE`
  exports, or any function a vignette calls includes `pkgdown::check_pkgdown()` and
  `pkgdown::build_article()` output from the installed dev build. Nothing pre-merge
  renders them; failures surface as a red `main` blamed on the next merge. —
  (cfbfastR#153 "Note on visibility")
- **R-2** `[blocker]` A new `@name <family>` / `@rdname` topic is its own pkgdown
  topic: `_pkgdown.yml` needs `starts_with("<family>")` (listing only member functions
  errors on the unindexed topic). — (cfbfastR#130)
- **R-3** `[blocker]` Vignette setup chunks never install the package itself
  (`pak::pak(c(..., "cfbfastR"))` overwrote the dev build mid-render; every function
  newer than CRAN became "could not find function"). — (cfbfastR#154)
- **R-4** `[major]` The pkgdown workflow does an unconditional source install of the
  package; pak's `local::.` is treated as satisfied from a cache holding the same
  `Version` (dev `3.0.0.9000` across all commits), so docs render against a stale
  build. Bumping `cache-version` re-breaks on the next function. — (cfbfastR#153)
- **R-5** `[major]` Every key-dependent example/vignette/test chunk is gated —
  `GITHUB_PAT`/`gh::` (`nzchar(Sys.getenv(...))`), `CFBD_API_KEY` (`has_cfbd_key()`),
  `ODDS_API_KEY` (`has_toa_key()`) — or `eval = FALSE` / `@examplesIf` +
  `\donttest{}`. The r-universe sandbox has no valid PAT: `validate_gh_pat()` killed
  hoopR/wehoop/fastRhockey source builds. Confirm on the r-universe builds page before
  claiming fixed.
- **R-6** `[major]` Joins over API frames in vignettes and functions survive upstream
  columns: explicit `by=` and `suffix=`, `select(any_of())`, assert population (rows,
  NA counts) not column presence. — (CFBD added `conference` → `conference.x/.y`;
  pkgdown red for weeks)
- **R-7** `[blocker]` An empty CFBD frame is not evidence of no data — wrappers
  collapse HTTP 204 and 5xx into the same empty frame + message. Any `data-raw/` probe
  or documented `@param year` minimum derived from `nrow() == 0` retries on zero,
  trusts positive counts, reads the message, and is sanity-checked against a
  real-world fact. — (cfbfastR#148; `min_year_map_df.R` wrote wrong minimums into docs)
- **R-8** `[major]` Live-test hygiene: guard every live block on the key plus
  `skip_on_cran()`; guard **every** fetch in a test, not only the first; assert class
  or message in `expect_error()`. **Do not** request `skip_on_ci()` on cfbfastR
  `cfbd_*`/artifact tests — CI sets `NOT_CRAN` and `CFBD_API_KEY` deliberately
  (declined twice: cfbfastR#129, #142).
- **R-9** `[major]` Review `DESCRIPTION` hunks one by one: new tidyverse verbs raise
  Imports floors (`join_by()`/`relationship=` need dplyr ≥ 1.1.1); a
  `git checkout -- DESCRIPTION` to discard `RoxygenNote` churn silently reverted a
  floor bump (cfbfastR#129). New `pkg::` calls need an Imports entry.
- **R-10** `[major]` API-surface changes update the triad `NEWS.md` +
  `cran-comments.md` + `_pkgdown.yml`; new NEWS bullets go under the current
  development heading (never open a version section before release). Decline bot
  suggestions citing nonexistent headings or re-levelling NEWS headings.
- **R-11** `[blocker]` Loaders are a contract with producer asset names and formats:
  one loader per release tag, stem == asset prefix, `.rds` via `rds_from_url()` /
  `.parquet` via `parquet_from_url()`. `wehoop::load_wnba_stats_*` read the
  `wnba_stats_*` tags live; hoopR has no `load_nba_stats_*`. A loader PR cites the real
  asset listing (`gh release view <tag> -R sportsdataverse/sportsdataverse-data`).
- **R-12** `[major]` Model scoring: `df[["season"]]` never `df$season` (`$`
  partial-matches `season_type`); class order through `.ep_predict()`'s permutation;
  resolve the booster before reading its card (the card cache keys on booster mtime);
  never restate `ERA_BOUNDS` — read them from the card. — (cfbfastR#152, #150)
- **R-13** `[major]` Articles quoting EP/EPA numbers say which build produced them
  (CRAN 3.0.0 scores with the previous model generation; dev scores with the XGBoost
  `cfb_model_artifacts` bundle); a "model is broken" claim sweeps inside the trainer's
  feature support. — (cfbfastR#149 retraction)
- **R-14** `[major]` Wrappers never error with "object not found": initialise the
  return (`data.frame()`) before `tryCatch` and return it unconditionally; API errors
  surface the API message rather than reading as "no data"; empty-but-valid responses
  return a **typed** empty tibble; HTTP goes through the package's call helper
  (oddsapiR `toa_api_call()` — never `httr2` directly in a wrapper).
- **R-15** `[minor]` Package contracts: sportsdataverse-R's roster lives in three
  places (`R/core.R`, DESCRIPTION `>=` floors, `_pkgdown.yml` menu — members must be on
  CRAN); cfbplotR's `ggpath::element_path` is S7 (construct, never
  `structure(list(), class=)`), `R/sysdata.rda`/`data/*.rda` are regenerated from
  `data-raw/` never hand-edited, and vdiffr is skipped on CI so geom/element PRs include
  locally accepted `_snaps/**/*.svg`; `inst/CITATION` year is pinned, not `Sys.Date()`;
  baseballr never renames Statcast columns by position.
- **R-16** `[major]` R CMD check tests the **installed** package — tests that
  `readLines("R/...")` fail there (guard with `file.exists()` or don't); no time-bomb
  date arithmetic (`Sys.Date() - months(3)` also drags in an undeclared `lubridate`).

## Verify

```sh
git diff --name-only origin/main...HEAD | grep -E '^(vignettes/|_pkgdown.yml|NAMESPACE|DESCRIPTION)'
git diff origin/main...HEAD -- DESCRIPTION                        # R-9
grep -n 'pak::pak(' vignettes/*.Rmd                               # R-3
Rscript -e 'devtools::document()' && git status --porcelain man NAMESPACE   # generated docs current
Rscript -e 'pkgdown::check_pkgdown()'                             # R-1/R-2
R CMD INSTALL --library="$SCRATCH/Rlib" . && Rscript -e '.libPaths(c("'"$SCRATCH"'/Rlib", .libPaths())); pkgdown::build_article("<article>")'
Rscript -e 'devtools::check(document = FALSE)'
gh run list -R sportsdataverse/<pkg> --workflow pkgdown --branch main -L 5   # post-merge watch
```

Several R installs exist (`Rscript --version`); keys load from `~/.Renviron` only for R.
