# R package conventions

- Every exported function needs a complete roxygen2 block: title +
  description before the first `@param`, `@param` for every argument,
  `@examples` present with live network calls wrapped in `\dontrun{}`.
- New dependencies are to be avoided whenever possible; if a new dependency is unavoidable, it must be justified in
  the PR and added to `DESCRIPTION` and `NAMESPACE`. Also consider opportunities to refactor existing code to avoid new dependencies/remove existing dependencies.
- `@param` description should indicate required vs optional and the default value if applicable. For example, `@param` season (required) The season to retrieve data for. or `@param` season (optional, default = 2023) The season to retrieve data for.
- `@return` description should indicate the type of object returned. For example, `@return` A tibble containing the requested data (<- perhaps a bit more descriptive than this).
- `@return` must include a `| col_name | type | description |` markdown
  table (R-style types: `character`, `integer`, `double`, `logical`,
  `list`, `data.frame`, `tibble`) — a one-liner without a table is a gap.
- `DESCRIPTION` needs `Roxygen: list(markdown = TRUE)` or the `@return`
  table renders as plain text in pkgdown instead of a table.
- Use {rlang}, {dplyr}, {tidyr} and {purrr} for tidy evaluation, data manipulation, and functional programming.
  Avoid base R functions when a tidyverse equivalent exists. Also use defensive tidyselections and tidy evaluation to avoid NSE issues.
  For example, use `dplyr::filter(df, {{ col_name }} == value)` instead of `df[df$col_name == value, ]`.
  Also follow data masking conventions and use `dplyr::select()` to select columns instead of base R subsetting.
  Be defensive about these selections and make ample use of `dplyr::any_of()`.
  We want to avoid NSE issues and make sure that the code is robust to changes in column names.
- Functions return tibbles; output columns are snake_case.
- For any new functions, consider adding unit tests to the `tests/testthat/` directory. Use the {testthat} package for testing and follow the existing test structure.
  If the function is a wrapper around an existing function, consider testing the wrapper's behavior and edge cases.
  Also if the function calls an external API, make sure to put skip_on_cran() in the test file to avoid running the tests on CRAN.
  Make sure to test edge cases and error handling as well.
- Follow the CRAN guidelines for package development and submission.
  This includes adhering to the R package structure, using proper documentation, and following best practices for package development. [Guide](https://r-pkgs.org/release.html)
- Ensure no files/directories are included in the package that are not needed for the package to function. This includes removing any temporary files, test data, or other files that are not necessary for the package to work. If committed and necessary, they should be in `.Rbuildignore`
  to avoid being included in the package build.
- `_pkgdown.yml`'s `reference:` section must list every export — no orphan
  exports (exported, not listed) and no phantom references (listed, not
  exported).
- Python ↔ R documentation parity: when the same dataset is documented on
  both sides, use identical `col_name` values and aligned descriptions —
  Python's live in `manual_column_descriptions.yaml`, R's in the `@return`
  roxygen block; update both when a column changes.
- R numeric fidelity for cross-language parity: R>=4.0 `fround` semantics,
  80-bit long-double sum, non-`na.rm` null-poisoning (R's sum/max return
  `NA`, polars skips nulls), dplyr C-locale group order.
- pkgdown theming: never apply a blanket bootswatch template — it strips
  the bespoke fonts/glow. Light theme stays untouched; fix dark mode only.
  Hardcoded near-black text (`#0f0f0f` etc.) → `var(--bs-body-color)`.
  Dead BS4 `.navbar-dark` selectors → `[data-bs-theme="dark"] .navbar`.
- Install packages with `pak::pak()` or `remotes::install_github()`, not `devtools::`.
  A README `remotes::` fallback installs `remotes` first.
- README: follow `readme.md` (bold headings, every badge whose backing exists, hand-written
  authors, full footer); check it with `sdv-repo-audit/scripts/check_r_readme.py`.
- **Never give `tryCatch()` a `warning =` handler around a parse.** The handler unwinds,
  so any harmless warning returns the empty default with no error
  (`espn_mlb_team_current_roster()` returned 0 rows for every team). Report warnings with a
  calling handler: `withCallingHandlers(..., warning = function(w) { report(w);
  invokeRestart("muffleWarning") })`, or baseballr's `.try_catch()` (same signature as
  `tryCatch`). Exception: code that uses the warning as a fallback signal on purpose.
- Coverage: house `test-coverage.yaml` (covr, `NOT_CRAN=true`, the same test env vars as
  `R-CMD-check.yaml`, non-fatal Codecov upload with the org `CODECOV_TOKEN`, fork-PR guard
  when secrets are used); outside the org without a token, the self-hosted shields-endpoint
  badge. Wrapper tests replay recorded httr2 responses so they run on CI — see
  `/sdv-r-coverage` for both.
- Conventional Commits, no AI co-author trailer.
