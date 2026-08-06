# Direction: Python (polars) → R

Source is an sdv-py function (polars); target is an SDV R package. R uses snake_case
function names (`cfbfastR::cfbd_*`, `espn_cfb_*`) and returns **tibbles**.

## Canonical target R packages in the workspace

- `cfbfastR-dev/cfbfastR`, `hoopR-dev/hoopR`, `wehoop-dev/wehoop`,
  `baseball-dev/baseballr`, `hockey-dev/fastRhockey`, `softballR-dev/softballR`.

Read the sdv-py function directly (`sportsdataverse/<sport>/...`); quote its path + line
range in the test/roxygen provenance.

## Oracle integrity — the Python fixture can itself be wrong

Don't assume the captured sdv-py output is ground truth just because it's the newer
implementation. A stale cache, a wrong season/game id, or an upstream ESPN payload that
changed shape between capture and port can all make the "golden" fixture wrong. If the R
port disagrees with the fixture in a way that looks more correct than the fixture, verify
against the raw source before porting the divergence away — **fix the bug, don't match it**
(the same rule as the reverse direction).

## Idiom map — polars/pandas → tidyverse (or data.table)

| polars / pandas idiom | tidyverse R |
|---|---|
| `df.with_columns((...).alias("x"))` | `dplyr::mutate(x = ...)` |
| `pl.when(c1).then(v1)...otherwise(d)` | `dplyr::case_when(c1 ~ v1, ..., TRUE ~ d)` |
| `df.group_by("g").agg(...)` | `dplyr::group_by(g) %>% dplyr::summarise(...)` |
| `pl.col("x").shift(1).over("game_id")` | `dplyr::group_by(game_id) %>% dplyr::mutate(dplyr::lag(x))` |
| `pl.col("x").cum_sum().over("g")` | `dplyr::group_by(g) %>% dplyr::mutate(cumsum(x))` |
| `df.filter(pl.col("c") == True)` | `dplyr::filter(c)` |
| `df.join(o, on="k", how="left")` | `dplyr::left_join(o, by = "k")` |
| `df.join(o, how="full", coalesce=True)` | `dplyr::full_join(o, by="k")` then coalesce |
| `pl.col("s").str.extract(re, g)` | `stringr::str_match(s, re)[, g+1]` |
| `df.pivot(...)` | `tidyr::pivot_wider(...)` |
| `df.melt(...)` / `unpivot` | `tidyr::pivot_longer(...)` |
| `df.with_row_index("i")` (0-based) | `dplyr::mutate(i = dplyr::row_number() - 1)` (R's `row_number()` is 1-based) |

## Bug-class table (the high-frequency port bugs, Python → R)

- **Join-key dtype discipline carries over.** Ids must match type on both sides; an integer
  id stringified as `"123.0"` is the same foot-gun in R — coerce the raw integer, don't
  `as.character()` a float-origin id. Match player names case-insensitively
  (`stringr::regex(..., ignore_case = TRUE)`).
- **0-based → 1-based indexing.** polars is 0-indexed; R vectors/`row_number()` are
  1-indexed. A literal transcription of a polars row-index expression (`with_row_index`,
  a `.slice(i, n)`) needs a `+ 1` somewhere, or a translated loop bound is off by one —
  check every index the polars side computed.
- **`NA` vs polars null.** polars null → R `NA` of the right type; watch `NA_real_` vs
  `NA_character_` in `case_when` branches (all branches must share a type).
- **Regex flavor differs the other way.** R's ICU/PCRE regex *does* support lookaround
  (unlike polars, which rejects it) — a polars-side workaround pattern (the `(?i)prefix(?-i:
  NAMES)` toggle) doesn't need to survive the port verbatim; a cleaner native R lookaround
  is fine, but re-test extraction on the fixture rather than assuming the polars pattern is
  portable as-is.
- **The null-poisoning inversion runs backwards here.** polars aggregations skip nulls; if
  you write the R side as `sum(x)` / `max(x)` **without** `na.rm = TRUE`, R will return `NA`
  the moment any input has one — a case the polars source may have handled silently. Decide
  deliberately whether the R output should propagate `NA` or skip it, and set `na.rm`
  accordingly; don't let the base-R default surprise you into a return-type change.
- **R numeric fidelity is now working *for* you, not against you** — but only if you use
  base R's own `round()`/`sum()` rather than hand-rolling scale-and-round or a naive
  accumulator. R ≥4.0's `round()` (`fround.c`) and `sum()` (80-bit long double) already match
  R's own historical outputs; the risk is a contributor "optimizing" with
  `sprintf("%.2f", x)` or a Rcpp accumulator that quietly stops matching the rest of the
  ecosystem's R output.

## Return-shape conventions

- **Return a tibble**, snake_case columns, stable column set even on empty input
  (`tibble::tibble(col = character())`), matching the sibling functions in the package.
- **Vectorize, don't loop.** `case_when`/`if_else` over rowwise loops; mirror the polars
  expression structure rather than transcribing an imperative pass.

## Document + wire pkgdown

Every exported R function needs a complete roxygen block: `@param` for each arg, an
`@return` describing the tibble (ideally a column table), and runnable `@examples`. Then:

- `devtools::document()` to regenerate `man/*.Rd` + `NAMESPACE`.
- Add the function to `_pkgdown.yml` reference so it appears on the site.
- Run `sdv-r-reviewer` (roxygen lens) and `sdv-docs-reviewer` (`mode: audit`) to check
  completeness.

Match the package's existing lint/style (most SDV R packages follow tidyverse style;
`styler::style_pkg()` if configured). Commit with the package's Conventional-Commit scope
(`feat(cfb): ...`) and **no AI co-author trailer** (SDV ecosystem rule).
