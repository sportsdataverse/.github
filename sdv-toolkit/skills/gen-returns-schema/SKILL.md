---
name: gen-returns-schema
description: Generate a col_name|type|description returns table (Python schema YAML or R roxygen @return) from a sample payload or a live DataFrame's schema.
disable-model-invocation: true
---

## Purpose

Produce a `tools/codegen/schemas/<name>.yaml` (Python) or a roxygen `@return` block (R) from either a live polars DataFrame or a raw JSON payload. Also used to back-fill empty `description: ''` entries in existing schema files.

---

## Dtype → R-type mapping

| Polars dtype | R-style type |
|---|---|
| `Int8/16/32/64`, `UInt8/16/32/64` | `integer` |
| `Utf8`, `String`, `Categorical` | `character` |
| `Float32`, `Float64` | `double` |
| `Boolean` | `logical` |
| `Date`, `Datetime`, `Duration` | `character` |
| `List(*)`, `Struct(*)`, `Array(*)` | `character` (stringified) |
| `Null` | `character` |

---

## Mode A — Python: emit schema YAML

Given a function call or an existing `pl.DataFrame`, run this snippet:

```python
import polars as pl
from sportsdataverse.<sport> import espn_<sport>_<endpoint>

df = espn_<sport>_<endpoint>(<args>, return_parsed=True)

DTYPE_MAP = {
    pl.Int8: "integer", pl.Int16: "integer", pl.Int32: "integer", pl.Int64: "integer",
    pl.UInt8: "integer", pl.UInt16: "integer", pl.UInt32: "integer", pl.UInt64: "integer",
    pl.Float32: "double", pl.Float64: "double",
    pl.Boolean: "logical",
    pl.Utf8: "character", pl.String: "character", pl.Categorical: "character",
    pl.Date: "character", pl.Datetime: "character", pl.Duration: "character",
    pl.Null: "character",
}

def to_r_type(dtype):
    base = dtype.base_type() if hasattr(dtype, "base_type") else type(dtype)
    return DTYPE_MAP.get(base, "character")

lines = ["schema: <name>", "kind: dataframe", "columns:"]
for col_name, dtype in df.schema.items():
    lines.append(f"  - {{name: {col_name}, type: {to_r_type(dtype)}, description: ''}}")

print("\n".join(lines))
```

Save output to `tools/codegen/schemas/<name>.yaml`. Then fill in `description:` values by inspecting column contents:

```python
print(df.select(pl.all().describe()))  # summary stats for numerics
print(df.head(3))                      # sample values for character cols
```

For multi-league schemas (e.g. `schemas/scoreboard/nba.yaml`), run per-league and diff against a base schema.

---

## Mode B — R: emit roxygen `@return`

Emit a markdown table usable directly in a roxygen block:

```r
# In R, given a tibble `df`:
cat("@return A tibble with", nrow(df), "rows and the following columns:\n\n")
cat("| col_name | type | description |\n|---|---|---|\n")
for (nm in names(df)) {
  rtype <- dplyr::case_when(
    is.integer(df[[nm]])   ~ "integer",
    is.double(df[[nm]])    ~ "double",
    is.logical(df[[nm]])   ~ "logical",
    TRUE                   ~ "character"
  )
  cat(sprintf("| `%s` | %s |  |\n", nm, rtype))
}
```

Paste the table into the `@return` section and fill descriptions.

---

## Back-filling existing schemas

Find schema files with empty descriptions:

```bash
grep -rl "description: ''" tools/codegen/schemas/
```

Open a fixture or call the live endpoint, inspect values, and fill in plain-English descriptions (e.g. `'ESPN athlete identifier'`, `'Team win percentage as a decimal'`).
