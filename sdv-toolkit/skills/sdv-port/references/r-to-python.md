# Direction: R → Python (polars)

Source is an R package function; target is sdv-py (polars 1.x). This is the classic
"port an nflfastR/cfbfastR/bigballR recipe" or "reconcile `0.36-live` into `main`" case.

## Canonical R sources in the workspace

- `nflverse-dev/nflfastR/R/*.R` (e.g. `helper_add_ep_wp.R`, `helper_add_fixed_drives.R`,
  `helper_add_series_data.R`) — the EP/WP/series/drives recipes.
- `cfbfastR-dev/cfbfastR/R/*.R` and the `0.36-live` branch of sdv-py (pandas-flavored CFB
  pbp fixes not yet in polars `main`; reconciliation notes live in `dev/`).
- `baseball-dev/baseballr`, `hoopR-dev/hoopR`, `wehoop-dev/wehoop`, `hockey-dev/fastRhockey`.

**If the R source has a sibling package for another league (bigballR/wbigballR,
hoopR/wehoop), diff them before you trust either.** The sibling is often a *stale fork*,
not an independent implementation: it inherits the parent's assumptions and silently
mis-handles its own league. (Real incident: `wbigballR` applies `bigballR`'s two-halves
clock math to quarter-format WBB pages, so regulation reads as double-overtime.) Port ONE
parameterized core + thin per-league bindings, and treat a fork-inherited bug as a
**deliberate fix** — documented in-module, with the fixed behavior proven by an independent
invariant, never by matching the oracle's bug.

## Oracle integrity — the R capture path can corrupt the oracle

An R-captured golden fixture is only as good as how it was captured. R's HTML/browser
readers mangle real payloads: `rvest::html_table` (and any chromote/rendered-DOM path)
expands a *nested* table's cells into the parent row — so a column can hold a completely
different stat than its name claims — and a rendered DataTable re-sorts rows, so oracle row
order ≠ source row order. Prefer a **static, offline capture over the exact bytes the
Python test will parse** (`XML::readHTMLTable`, or the R package's own `use_file=TRUE` path
against the committed fixture) so both sides see identical input.

When a column is provably wrong-by-construction, **do not port the bug to match it.**
Partition the oracle columns and say so in the test docstring:

- **strict** — asserted cell-for-cell,
- **promoted** — empirically verified to agree despite being suspect (check before assuming
  divergence; a constant offset often cancels inside the algorithm),
- **invariant-covered** — the oracle is wrong here; assert independent invariants instead
  (bounds, monotonicity, totals) and prove the correction with a check the buggy version
  could not pass (e.g. a 100% join-match rate that only holds under the fixed clock math).

If the R can't be run locally, hand-derive a few rows from the R logic by inspection and
mark them `# derived-by-inspection` — still better than no oracle.

## Idiom map — R (base/dplyr/np) → polars 1.x

| R / pandas idiom | polars 1.x |
|---|---|
| `dplyr::mutate(x = ...)` / `df.assign(...)` | `df.with_columns((...).alias("x"))` |
| `dplyr::case_when(...)` / `np.select(conds, choices, default)` | `pl.when(c1).then(v1).when(c2).then(v2).otherwise(default)` |
| `dplyr::group_by(g) %>% summarise(...)` / `df.groupby(...)` | `df.group_by("g").agg(...)` |
| `dplyr::lag(x)` / `dplyr::lead(x)` / `df.shift()` | `pl.col("x").shift(1)` / `.shift(-1)` — **always `.over("game_id")`** to avoid cross-game leak when frames are concatenated |
| `cumsum(x)` | `pl.col("x").cum_sum()` |
| `ifelse(cond, a, b)` | `pl.when(cond).then(a).otherwise(b)` |
| `df.loc[mask, col] = v` | `with_columns(pl.when(mask).then(v).otherwise(pl.col(col)).alias(col))` |
| `nrow()` / `dplyr::n()` | `pl.len()` |
| `df[order(x), ]` | `df.sort("x")` |
| `tidyr::pivot_wider` | `df.pivot(...)` |
| `stringr::str_extract(s, re)` | `pl.col("s").str.extract(re, group)` |
| `x[i]` (R is **1-indexed**) | `x[i - 1]` (Python/polars are **0-indexed**) — see the bug-class entry below |

## Bug-class table (the high-frequency port bugs, R → Python)

- **ID dtype discipline / int-vs-str mismatches at join boundaries.** Pick one canonical
  dtype per id at the boundary and keep it. Never `cast(Utf8)` a float-origin id (`123.0` ≠
  `"123"`); cast the raw integer. Assert `left.schema[key] == right.schema[key]` before any
  join.
- **NaN ids surviving an `is not None` filter.** An R `NA` numeric id, once round-tripped
  through a CSV/pandas capture, becomes a float `NaN` — not `None`/`null` — so a Python
  guard written as `if id is not None` (or a pandas `.notnull()` applied loosely) lets it
  through as a "real" id. Filter with `pl.col("id").is_not_null() & pl.col("id").is_not_nan()`
  (or `pd.isna()` if the intermediate is pandas), not an identity/`is not None` check.
- **No regex lookaround.** Rust/polars regex rejects `(?=)`/`(?!)`/`(?<=)`/`(?<!)` — R's
  ICU/PCRE regex supports it, so a straight port of an R lookaround pattern raises
  `ComputeError`. To stop a capture at a stopword, use the inline case toggle
  `(?i)prefix(?-i: NAMES)` instead. Also watch case-sensitivity defaults: R regex functions
  are case-sensitive by default same as polars, but a port that relied on R's `perl=TRUE`
  ignore-case flag needs the explicit `(?i)` toggle carried over.
- **1-based → 0-based indexing.** R vectors/data frames are 1-indexed; polars/Python are
  0-indexed. A literal port of `x[i]`, `head(x, n)[n]`, or a row-number comparison off by a
  constant is the classic silent off-by-one — check every hard-coded index and every
  `row_number()`/`seq_along()` translation.
- **polars 1.x surface only.** No `groupby` / `with_row_count` / `apply` / `pl.count` /
  `cumsum` / `set_at_idx` / `how="outer"` / `str.strip`. If you wrote a 0.18-era call, it's
  a bug (the review step catches these).
- **Explicit boolean masks.** `pl.col("c") == True`, not bare `pl.col("c")`.
- **Float64 model outputs.** Models emit float32; cast public columns explicitly so a
  `pl.Series(numpy_f32)` can't silently downcast.

### R numeric fidelity (when the port must match R bit-for-bit)

**Signature: the parity test passes on 99% of cells and fails on a handful — almost all of
them `.xx5` rounding boundaries, or a group sum that's off in the last ulp.** That is not a
logic bug; it is R's arithmetic differing from Python's. Four sources, all real:

- **`round()` is not scale-and-round.** R ≥4.0 (`src/nmath/fround.c`) takes the two
  *back-converted doubles* `floor(x·10^d)/10^d` and `ceil(x·10^d)/10^d`, picks whichever is
  nearer to `x`, and breaks an exact tie to the even scaled digit. So `round(0.475,2)=0.48`
  **but** `round(22.755,2)=22.75` — no single polars `round` mode (`half_away_from_zero` *or*
  `half_to_even`) reproduces both, and neither does any decimal-repr rule. Port it as an
  explicit `_fround(x, digits)` UDF (`map_elements(..., return_dtype=pl.Float64)`) and
  **fuzz-verify a boundary grid against local `Rscript`** before trusting it.
- **`sum()` accumulates in 80-bit long double.** A plain float64 fold diverges at boundary
  values (e.g. 42.765) and then flips the rounded output. Use `math.fsum` for any group sum
  that feeds a rounded/reported column.
- **Non-`na.rm` aggregations NULL-POISON.** In R, `sum(x)` / `max(x)` without `na.rm=TRUE`
  return `NA` if *any* element is NA — but polars aggregations **skip nulls** and happily
  return a number. When the R call omits `na.rm`, add an explicit any-null-poisons guard;
  don't let polars invent a value where R produced NA.
- **dplyr group order = C-locale byte sort, NA groups last.** If row order is part of the
  contract, `.sort(keys, nulls_last=True)` — and beware sorting a Utf8 id where R sorted a
  numeric one (differs the moment ids have mixed digit-width).

These only matter for outputs that must match R exactly (rounded stats, published tables).
Don't reach for them on a model column governed by a correlation threshold.
