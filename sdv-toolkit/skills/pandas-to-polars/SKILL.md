---
name: pandas-to-polars
description: Use when converting pandas DataFrame/Series code to polars 1.2+ in a SportsDataverse repo — translating a `df.loc`/`np.select`/`df.assign`/`groupby().transform`/`merge` block, reconciling a pandas fix from the sdv-py `0.36-live` branch into polars `main`, or modernizing a pandas-flavored parser/loader. Invoke for "convert this pandas to polars", "rewrite with polars", "translate pandas df.loc/np.where to polars", "port the 0.36-live pandas code", or "make this use polars instead of pandas".
---

# Convert pandas → polars 1.2+

Translate pandas code into **idiomatic, correct polars 1.2+** that already satisfies the
SportsDataverse conventions (1.x surface only, no regex lookaround, ID-dtype discipline).
The recurring failure this prevents: a translation that *looks* right but diverges
downstream — a null where pandas had `NaN`, a row dropped by an index misalignment, an
unordered `group_by` — surfacing only at a join, a model rebuild, or a season compile.

> **Sibling skills — don't reach for this one if:** the source is **R** (use
> `port-r-to-python`), or the code is already polars but on the **0.18 API** (that's a
> version migration — run the `polars-1x-reviewer` agent, not a pandas conversion).

## The three mental-model shifts (most bugs live here)

1. **No index.** polars has no row index and no automatic index alignment. `set_index` /
   `reset_index` / `.loc[label]` have no equivalent — promote the would-be index to a real
   column and join/sort/filter on it. Two frames line up by an explicit `join`, never by
   "same index".
2. **Expressions, not in-place mutation.** You never assign into a frame
   (`df["c"] = ...`). You build a new frame with `df.with_columns((expr).alias("c"))`.
   A conditional write (`df.loc[mask, "c"] = v`) becomes
   `with_columns(pl.when(mask).then(v).otherwise(pl.col("c")).alias("c"))`.
3. **null ≠ NaN.** pandas conflates missing and NaN; polars separates **null** (missing)
   from **NaN** (a float value). `fillna`/`isna`/`dropna` split into `fill_null`/`is_null`/
   `drop_nulls` **and** `fill_nan`/`is_nan`. Translating only the null half is the single
   most common silent bug.

## Translation reference (pandas → polars 1.x)

### Select / filter / sort
| pandas | polars 1.x |
|---|---|
| `df[df.x > 0]` | `df.filter(pl.col("x") > 0)` |
| `df.loc[mask, "c"]` | `df.filter(mask).select("c")` |
| `df[["a", "b"]]` | `df.select("a", "b")` |
| `df.sort_values("x", ascending=False)` | `df.sort("x", descending=True)` |
| `df.drop_duplicates(subset=["k"])` | `df.unique(subset=["k"], keep="first")` |
| `df.set_index(...)` / `df.reset_index()` | (no index) promote to a real column / `with_row_index` |
| `df.nlargest(k, "x")` | `df.top_k(k, by="x")` |

### Create / mutate columns
| pandas | polars 1.x |
|---|---|
| `df["c"] = expr` | `df = df.with_columns(expr.alias("c"))` |
| `df.assign(c=..., d=...)` | `df.with_columns(c=..., d=...)` |
| `df.loc[mask, "c"] = v` | `df.with_columns(pl.when(mask).then(v).otherwise(pl.col("c")).alias("c"))` |
| `df.rename(columns={"a": "b"})` | `df.rename({"a": "b"})` |
| `df.drop(columns=["a"])` | `df.drop("a")` |
| `df.astype({"a": "int64"})` | `df.with_columns(pl.col("a").cast(pl.Int64))` |
| `df["c"].map(mapping)` (full remap) | `pl.col("c").replace_strict(mapping, default=None)` |
| `df["c"].replace(old, new)` (patch some) | `pl.col("c").replace(old, new)` |
| `df.apply(fn, axis=1)` | prefer a vectorized expr; last resort `pl.struct(...).map_elements(fn, return_dtype=...)` |

### Conditionals
| pandas / numpy | polars 1.x |
|---|---|
| `np.where(cond, a, b)` | `pl.when(cond).then(a).otherwise(b)` |
| `np.select(conds, choices, default)` | chained `pl.when(c1).then(v1).when(c2).then(v2)...otherwise(default)` |
| `df["x"].clip(lo, hi)` | `pl.col("x").clip(lo, hi)` |

### Group-by / window
| pandas | polars 1.x |
|---|---|
| `df.groupby("g").agg({"x": "sum"})` | `df.group_by("g").agg(pl.col("x").sum())` |
| `df.groupby("g")["x"].transform("sum")` | `pl.col("x").sum().over("g")` (keeps row count) |
| `df.groupby("g")["x"].shift(1)` | `pl.col("x").shift(1).over("g")` — **always `.over(group)`** so a concat can't leak across groups |
| `df.groupby("g").cumsum()` | `pl.col("x").cum_sum().over("g")` |
| `df.groupby("g", sort=False)` | `df.group_by("g", maintain_order=True)` — polars `group_by` is **unordered by default** (pandas sorts) |
| `df["x"].rolling(3).mean()` | `pl.col("x").rolling_mean(window_size=3)` |

### Join / concat
| pandas | polars 1.x |
|---|---|
| `df.merge(o, on="k", how="left")` | `df.join(o, on="k", how="left")` |
| `pd.merge(a, b, how="outer")` | `a.join(b, on="k", how="full", coalesce=True)` |
| `df.merge(o, left_on=, right_on=)` | `df.join(o, left_on=, right_on=)` |
| `pd.concat([a, b])` (stack rows) | `pl.concat([a, b])` — use `how="diagonal_relaxed"` when schemas differ |
| `pd.concat([a, b], axis=1)` (cols) | `pl.concat([a, b], how="horizontal")` |

### Missing data (null vs NaN — read shift #3)
| pandas | polars 1.x |
|---|---|
| `df.fillna(0)` | `df.fill_null(0)` — and `.fill_nan(0)` if floats carry NaN |
| `df.dropna()` | `df.drop_nulls()` |
| `df["x"].isna()` | `pl.col("x").is_null()` (`.is_nan()` for float NaN) |
| `df.isnull().sum()` | `df.null_count()` |
| `df["x"].ffill()` | `pl.col("x").forward_fill()` |

### Strings (Rust regex — **no lookaround**)
| pandas | polars 1.x |
|---|---|
| `s.str.contains(pat)` | `pl.col("s").str.contains(pat)` |
| `s.str.replace(a, b)` / `replace(..., regex=True)` | `.str.replace(a, b)` (first) / `.str.replace_all(a, b)` |
| `s.str.extract(pat, expand=False)` | `pl.col("s").str.extract(pat, group_index)` |
| `s.str.lower()` / `s.str.strip()` | `.str.to_lowercase()` / `.str.strip_chars()` |
| `s.str.len()` | `pl.col("s").str.len_chars()` |
| `a + " " + b` (concat) | `pl.concat_str(["a", "b"], separator=" ")` |

### Dates
| pandas | polars 1.x |
|---|---|
| `pd.to_datetime(s, format=f)` | `pl.col("s").str.to_datetime(f)` (or `.str.to_date(f)`) |
| `s.dt.year` (attribute) | `pl.col("s").dt.year()` (**method call**) |
| `s.dt.strftime(f)` | `pl.col("s").dt.strftime(f)` |

### Reshape / interop
| pandas | polars 1.x |
|---|---|
| `df.pivot_table(index=, columns=, values=, aggfunc=)` | `df.pivot(on=, index=, values=, aggregate_function=)` — first arg is **`on=`** (was `columns=` pre-1.0) |
| `df.melt(id_vars=, value_vars=)` | `df.unpivot(index=, on=, variable_name=, value_name=)` — `melt` **deprecated at 1.0** |
| `df.T` | `df.transpose()` |
| `pd.read_csv(path, dtype=...)` | `pl.read_csv(path, schema_overrides=...)` |
| `len(df)` / `df.shape[0]` | `df.height` / `len(df)` |
| `df["x"].sum()` (scalar) | `df.select(pl.col("x").sum()).item()` (or `df["x"].sum()` on a Series) |
| `df.to_pandas()` / `pl.from_pandas(pdf)` | interop both directions |

## SDV conventions the polars output MUST satisfy

These are the project rules from sdv-py `CLAUDE.md` — a conversion that ignores them is a
bug even if it runs. After converting, **run the `polars-1x-reviewer` agent** to catch them
mechanically.

- **1.x surface only.** No `groupby` / `with_row_count` / `.apply(` / `pl.count()` /
  `cumsum` / `set_at_idx` / `how="outer"` / `str.strip` / `shift_and_fill`. (Full table:
  the `polars-1x-reviewer` agent.)
- **No regex lookaround.** `(?=)` `(?!)` `(?<=)` `(?<!)` raise `ComputeError`. Stop a
  capture at a stopword with the inline case toggle: `(?i)prefix(?-i: NAMES)`.
- **Explicit boolean masks.** `pl.col("c") == True`, never bare `pl.col("c")` / `~pl.col(...)`.
- **ID-dtype discipline.** Pick one canonical dtype per join key at the boundary and keep
  it. Never `cast(Utf8)` a float-origin id (`123.0` ≠ `"123"`) — cast the raw integer.
  Assert `left.schema[key] == right.schema[key]` before a join.
- **Float64 model outputs.** Cast explicitly; a `pl.Series(numpy_f32)` silently downcasts.
- **Scalar from numpy** is `pl.lit(np_array).first()`, not `pl.lit(np_array)` (1.x no longer
  auto-broadcasts).
- **snake_case output columns** via `sportsdataverse.dl_utils.underscore`.

## Converting a real pipeline function (not a greenfield snippet)

When the pandas code is live pipeline logic (e.g. a `0.36-live` → `main` reconciliation),
the divergence-surfaces-downstream failure is real — make it a **failing parity test before
the conversion**, mirroring `port-r-to-python`:

1. Run the pandas function on a small representative input; persist its output (the columns
   you'll assert on + the join keys) as a golden fixture under `tests/fixtures/` (or `dev/`
   for a one-off reconciliation).
2. Write a parity test that loads the fixture and asserts the not-yet-written polars output
   matches — exact equality for id/categorical columns, a closeness threshold (state it +
   why) for float model columns. Run it; confirm it fails for the right reason.
3. Translate using the tables above; go green.
4. Gate: `uv run ruff format <f> && uv run ruff check <f>`, the `polars-1x-reviewer` agent,
   then `/preflight` (scoped) before `/ship`.

Don't merge `0.36-live` wholesale — it's pandas-flavored and would undo the polars
migration. Port semantic fixes by translation and record the reconciliation in `dev/`.

## Common mistakes

- Translating `fillna`/`isna` only as `fill_null`/`is_null` and missing the **NaN** half.
- A `shift`/`cumsum`/`transform` left un-`.over(group)` — leaks across games on concat.
- `group_by` without `maintain_order=True` when a downstream step assumes pandas' sorted
  order.
- `df.pivot(columns=...)` (pre-1.0) or `df.melt(...)` instead of `pivot(on=...)` /
  `unpivot(...)`.
- `pd.merge(how="outer")` → `how="outer"` (a 0.18 token) instead of `how="full", coalesce=True`.
- A row-wise `df.apply(fn, axis=1)` ported to `map_elements` when a vectorized `pl.when` /
  arithmetic expression exists — keep it vectorized; `map_elements` is the slow last resort.

## See also

- `port-r-to-python` — the R→polars sibling (parity-test-first; shares the gate).
- `polars-1x-reviewer` agent — the post-conversion mechanical check for 0.18-era API.
- sdv-py `CLAUDE.md` "Polars version" + "ID column types" — the authoritative idiom/dtype reference.
