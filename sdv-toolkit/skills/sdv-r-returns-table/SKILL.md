---
name: sdv-r-returns-table
description: Generate or back-fill a roxygen @return markdown table (col_name|type|description) for an SDV R function, matching the Python returns convention.
disable-model-invocation: true
---

# SDV R — @return Markdown Table

Adds or updates the `@return` block in an SDV roxygen2 docstring so it matches the
`| col_name | type | description |` convention used in the Python codegen schemas.

---

## Prerequisites — enable markdown in roxygen

Check `DESCRIPTION` for:

```
Roxygen: list(markdown = TRUE)
```

If absent, add it before the `RoxygenNote:` line. Without this flag pkgdown will
render the pipe table as plain text.

---

## Step 1 — Derive the column list

Run the function in a live R session (or read an existing data artifact) to get the
real schema:

```r
library(cfbfastR)  # or wehoop / hoopR / etc.
df <- cfbd_play_by_play_data(season = 2023, week = 1)
dplyr::glimpse(df)
# Use the Name + type columns from glimpse output
```

Map R class → table type token:

| R class | Table token |
|---|---|
| `integer` / `int` | `integer` |
| `numeric` / `dbl` | `double` |
| `character` / `chr` | `character` |
| `logical` / `lgl` | `logical` |
| `list` | `list` |
| `POSIXct` / `Date` | `character` (document format in description) |

---

## Step 2 — Write the @return block

Place the table immediately after the `@return` tag. Every column that a caller
can reliably expect should appear. Unknown / internal columns go in an "additional
columns" prose note below the table.

```r
#' @return A [tibble][tibble::tibble-package] with one row per play and columns:
#'
#' | col_name | type | description |
#' |---|---|---|
#' | game_id | integer | ESPN game identifier |
#' | play_id | character | Unique play identifier within the game |
#' | period | integer | Game period (1–4; 5+ for OT) |
#' | clock | character | Game clock at snap, formatted `MM:SS` |
#' | pos_team | character | Abbreviation of the team with possession |
#' | yards_gained | integer | Net yards on the play (negative for losses) |
#' | score_differential | double | Home score minus away score at snap |
#' | wp | double | Pre-play win probability for the possession team (0–1) |
```

---

## Step 3 — Regenerate man/ pages

```r
devtools::document()   # rewrites man/<fn>.Rd from roxygen comments
```

Spot-check the rendered output:

```r
?cfbd_play_by_play_data   # should show the markdown table in the Value section
```

---

## Step 4 — Rebuild the pkgdown site

```r
pkgdown::build_reference_index()   # fast: just the reference page
# or full rebuild:
pkgdown::build_site()
```

Verify the HTML table renders on the reference page (requires deploy; see
`sdv-pkgdown-personalize` skill for theming gotchas).

---

## Parity note — Python ↔ R

When a Python function (e.g. `load_nfl_pbp` in sdv-py) and an R function
(e.g. `nflfastR::load_pbp`) document the same dataset, use identical
`col_name` values and aligned descriptions. The Python side stores the
table in `tools/codegen/schemas/loader_schemas.yaml`; the R side in the
`@return` roxygen block. Update both when adding a new column.
