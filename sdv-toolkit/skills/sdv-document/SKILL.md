---
name: sdv-document
description: Use when producing or back-filling documentation surface in a SportsDataverse repo. Phases — (1) generate a col_name/type/description returns table as a Python schema YAML from a sample payload or a live DataFrame schema, writing descriptions to manual_column_descriptions.yaml and NEVER to schemas/**.yaml which is clobbered on re-capture, (2) generate or back-fill the equivalent roxygen @return markdown table for an SDV R function, (3) scaffold a per-sport intro Jupyter notebook at examples/notebooks/0X_<sport>_intro.ipynb, (4) apply the bespoke SportsDataverse pkgdown theming and fix the shared extra.css Bootstrap-5 bugs (dark-mode-invisible text, dead .navbar-dark selectors). Invoke for "generate a returns table", "generate the returns schema", "add column descriptions", "back-fill the return table", "add a roxygen return table", "add an example notebook", "scaffold a notebook for this sport", "apply the pkgdown theme", or "fix the pkgdown dark mode".
---

# Document — returns schema, notebook, pkgdown

Covers the documentation surface across the sdv-py + R-package ecosystem:
Python returns-schema YAML, the matching R roxygen `@return` table, per-sport
intro notebooks, and R pkgdown theming (including two recurring Bootstrap 5
bugs). Four independent phases — jump to the one that matches the ask.

## Phase menu

| Entry phrase | Start at |
|---|---|
| "generate a returns table", "generate the returns schema", "add column descriptions" | Phase 1 (returns-schema-py) |
| "add a roxygen return table", "back-fill the return table" | Phase 2 (returns-table-r) |
| "add an example notebook", "scaffold a notebook for this sport" | Phase 3 (notebook) |
| "apply the pkgdown theme", "fix the pkgdown dark mode" | Phase 4 (pkgdown) |

### Review (mandatory)

- `sdv-docs-reviewer` — always, for returns-table coverage and quality.
- `sdv-r-reviewer` — additionally when the target is an R package.

---

## Phase 1 — Python: returns schema YAML (`returns-schema-py`)

Produce a `tools/codegen/schemas/<name>.yaml` from a live polars DataFrame or
a raw JSON payload. Also used to back-fill empty `description: ''` entries in
existing schema files.

**Binding rule:** column descriptions live in `manual_column_descriptions.yaml`
(schema-keyed), **NEVER** in `schemas/**.yaml` directly — that tree is
clobbered on re-capture. Author descriptions in the manual file; the schema
YAML's `description: ''` placeholder stays empty and gets merged at build
time.

### Dtype → R-type mapping

| Polars dtype | R-style type |
|---|---|
| `Int8/16/32/64`, `UInt8/16/32/64` | `integer` |
| `Utf8`, `String`, `Categorical` | `character` |
| `Float32`, `Float64` | `double` |
| `Boolean` | `logical` |
| `Date`, `Datetime`, `Duration` | `character` |
| `List(*)`, `Struct(*)`, `Array(*)` | `character` (stringified) |
| `Null` | `character` |

### Emit the schema YAML

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

Save output to `tools/codegen/schemas/<name>.yaml`. Then write the
`description:` values into `manual_column_descriptions.yaml` (schema-keyed —
never inline in the schema file) by inspecting column contents:

```python
print(df.select(pl.all().describe()))  # summary stats for numerics
print(df.head(3))                      # sample values for character cols
```

For multi-league schemas (e.g. `schemas/scoreboard/nba.yaml`), run per-league
and diff against a base schema.

### Back-filling existing schemas

Find schema files with empty descriptions:

```bash
grep -rl "description: ''" tools/codegen/schemas/
```

Open a fixture or call the live endpoint, inspect values, and fill in
plain-English descriptions (e.g. `'ESPN athlete identifier'`, `'Team win
percentage as a decimal'`) into `manual_column_descriptions.yaml`.

---

## Phase 2 — R: roxygen `@return` markdown table (`returns-table-r`)

Adds or updates the `@return` block in an SDV roxygen2 docstring so it matches
the `| col_name | type | description |` convention used in the Python codegen
schemas.

### Prerequisites — enable markdown in roxygen

Check `DESCRIPTION` for:

```
Roxygen: list(markdown = TRUE)
```

If absent, add it before the `RoxygenNote:` line. Without this flag pkgdown
will render the pipe table as plain text.

### Step 1 — Derive the column list

Run the function in a live R session (or read an existing data artifact) to
get the real schema:

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

Or generate the table programmatically from a live tibble `df`:

```r
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

### Step 2 — Write the `@return` block

Place the table immediately after the `@return` tag. Every column that a
caller can reliably expect should appear. Unknown / internal columns go in an
"additional columns" prose note below the table.

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

### Step 3 — Regenerate `man/` pages

```r
devtools::document()   # rewrites man/<fn>.Rd from roxygen comments
```

Spot-check the rendered output:

```r
?cfbd_play_by_play_data   # should show the markdown table in the Value section
```

### Step 4 — Rebuild the pkgdown site

```r
pkgdown::build_reference_index()   # fast: just the reference page
# or full rebuild:
pkgdown::build_site()
```

Verify the HTML table renders on the reference page (requires deploy; see
Phase 4 for theming gotchas).

### Parity note — Python ↔ R

When a Python function (e.g. `load_nfl_pbp` in sdv-py) and an R function
(e.g. `nflfastR::load_pbp`) document the same dataset, use identical
`col_name` values and aligned descriptions. The Python side stores
descriptions in `manual_column_descriptions.yaml`; the R side in the
`@return` roxygen block. Update both when adding a new column.

---

## Phase 3 — Scaffold a per-sport intro notebook (`notebook`)

Add a new per-sport intro notebook at
`examples/notebooks/0X_<sport>_intro.ipynb` that parallels the existing set,
demonstrating the canonical surface for one sport in a consistent order.

### Numbering convention

Notebooks use zero-padded two-digit prefixes so they sort correctly:

```
examples/notebooks/
  01_nfl_intro.ipynb
  02_cfb_intro.ipynb
  03_nba_intro.ipynb
  04_wnba_intro.ipynb
  05_mbb_intro.ipynb
  06_wbb_intro.ipynb
  07_nhl_intro.ipynb
  08_mlb_intro.ipynb
  09_<new_sport>_intro.ipynb   ← your file
```

Pick the next available number. The set must stay parallel — every sport
gets exactly one intro notebook.

### Cell outline

#### Cell 1 — Markdown header

```markdown
# <Sport Full Name> — sportsdataverse-py intro

Short one-paragraph description of the sport module and what data it provides.
Links: package docs, companion R package (e.g. hoopR / wehoop / cfbfastR).
```

#### Cell 2 — Imports + version pin

```python
import polars as pl
import sportsdataverse.<sport> as <abbr>

print(pl.__version__)
print(<abbr>.__version__ if hasattr(<abbr>, "__version__") else "ok")
```

#### Cell 3 — Schedule

```python
schedule = <abbr>.espn_<sport>_schedule(season=2024, return_parsed=True)
print(schedule.shape)
schedule.head(5)
```

One markdown cell before it explaining what the schedule endpoint returns
(columns to highlight: `game_id`, `date`, `home_team`, `away_team`,
`home_score`, `away_score`).

#### Cell 4 — Play-by-play (if available)

```python
# Pick a recent completed game_id from schedule above
game_id = int(schedule.filter(pl.col("home_score").is_not_null())["game_id"][0])
pbp = <abbr>.espn_<sport>_pbp(event_id=game_id, return_parsed=True)
print(pbp.shape)
pbp.select(["clock_display_value", "type_text", "text", "score_value"]).head(10)
```

#### Cell 5 — Teams

```python
teams = <abbr>.espn_<sport>_teams(return_parsed=True)
print(teams.shape)
teams.head(5)
```

#### Cell 6 — Season stats / standings

```python
standings = <abbr>.espn_<sport>_standings(season=2024, return_parsed=True)
standings.head(10)
```

Adapt to whatever the sport's canonical season-level endpoint is
(`scoreboard`, `standings`, `statistics`).

#### Cell 7 — Cache + config (NFL or any cached loader)

Include only when the sport uses the NFL-style cache layer:

```python
from sportsdataverse.nfl import get_config, update_config, clear_cache
print(get_config())
update_config(cache_mode="memory", cache_duration=3600)
# ... call a loader ...
clear_cache()
```

#### Cell 8 — Markdown closing

```markdown
## Next steps
- PBP deep-dive: see `examples/notebooks/0X_<sport>_pbp_deep_dive.ipynb` (if it exists)
- R parity: [<companion R package>](<url>)
- Full API reference: [sportsdataverse docs](https://py.sportsdataverse.org)
```

### Output hygiene

If the repo has `nbstripout` configured (check `.gitattributes` for
`*.ipynb filter=nbstripout`), all cell outputs are stripped automatically on
`git add`. If not configured, strip outputs manually before committing:

```bash
uv run jupyter nbconvert --ClearOutputPreprocessor.enabled=True \
    --to notebook --inplace examples/notebooks/09_<sport>_intro.ipynb
```

Never commit notebooks with large embedded outputs (images, full
DataFrames) — they bloat the repo and produce noisy diffs.

### Checklist before committing

- [ ] File named `0X_<sport>_intro.ipynb` with the correct next number.
- [ ] All cells execute top-to-bottom without errors against a live API (run
      `SDV_PY_LIVE_TESTS=1 uv run jupyter nbconvert --to notebook --execute ...`).
- [ ] Outputs stripped.
- [ ] Markdown cells use plain English, no internal jargon.
- [ ] `See Also` cross-links point to the correct companion R package URL
      from the CLAUDE.md table.

---

## Phase 4 — pkgdown theming — preserve brand + fix BS5 bugs (`pkgdown`)

The SDV R pkgdown sites share a bespoke look (custom fonts, glow effect). Two
Bootstrap 5 bugs are present in the shared `extra.css` across all sites.
Apply the fixes below WITHOUT flattening the brand.

### Ground rules

- **Do NOT apply a blanket bootswatch template** (e.g.
  `template: bootswatch: flatly` in `_pkgdown.yml`). This strips custom
  fonts, glow CSS, and color overrides.
- **Light theme: do not touch.** All visual regressions reported so far are
  dark-mode.
- **Dark mode: keep + fix on-brand.** The goal is legibility, not redesign.
- **Preview is not available locally** (bespoke fonts + Vercel CDN refs).
  Verify on deploy.

### `_pkgdown.yml` — settings to preserve

When editing `_pkgdown.yml`, keep these blocks unchanged:

```yaml
template:
  bslib:
    # keep any custom variable overrides already present, e.g.:
    # primary: "#...", font_scale: ..., etc.
  # Do NOT add: bootswatch: <theme>
```

If `bslib:` variables are absent and need to be added, only add explicit
overrides — never replace the block with a bootswatch name.

### Bug 1 — Dark-mode-invisible hardcoded text color

Any `color: #0f0f0f` (or similar near-black hex, e.g. `#111`, `#1a1a1a`,
`#0d0d0d`) in `pkgdown/extra.css` is invisible against dark-mode backgrounds.

**Before:**
```css
.some-selector {
  color: #0f0f0f;
}
```

**After:**
```css
.some-selector {
  color: var(--bs-body-color);
}
```

`--bs-body-color` is the Bootstrap 5 semantic token: `#212529` in light
mode, `#dee2e6` (or theme override) in dark mode. It tracks the active
theme automatically without a media query.

Search the file for all near-black hex literals before committing:

```bash
grep -nE 'color:\s*#(0[0-9a-f]{5}|1[0-3][0-9a-f]{4})' pkgdown/extra.css
```

### Bug 2 — Dead `.navbar-dark` selectors (Bootstrap 4 → 5 rename)

Bootstrap 5 removed the `.navbar-dark` utility class. SDV `extra.css` files
still target it, so those rules are silently ignored in dark mode.

**Before (BS4 / dead in BS5):**
```css
.navbar-dark .navbar-brand,
.navbar-dark .navbar-nav .nav-link {
  color: #ffffff;
}
```

**After (BS5):**
```css
[data-bs-theme="dark"] .navbar .navbar-brand,
[data-bs-theme="dark"] .navbar .navbar-nav .nav-link {
  color: #ffffff;
}
```

Also verify the navbar HTML in the rendered site uses `data-bs-theme="dark"`
on the `<nav>` element (pkgdown 1.6+ sets this automatically when `bslib`
dark mode is active). If you see `class="navbar navbar-dark"` in the
source, the pkgdown version is old — upgrade pkgdown first.

```r
remotes::install_github("r-lib/pkgdown")
```

### Checklist before pushing

- [ ] `grep -n 'navbar-dark' pkgdown/extra.css` returns zero results.
- [ ] `grep -nE 'color:\s*#[0-1][0-9a-f]' pkgdown/extra.css` returns zero results.
- [ ] `_pkgdown.yml` has no `bootswatch:` key.
- [ ] `bslib:` variable overrides are preserved (not replaced).
- [ ] `devtools::document()` runs clean (no roxygen warnings).
- [ ] Commit, push to `main` (or PR branch), verify on Vercel deploy.

### Regenerating the site locally (limited fidelity)

```r
pkgdown::build_site(preview = FALSE)
# Open docs/index.html in browser — fonts / glow may differ from deploy
```

Full fidelity only on Vercel. For a quick CSS-only sanity check, open the
built `docs/` HTML directly and inspect element with DevTools dark-mode
emulation (`Rendering > Emulate CSS media feature prefers-color-scheme: dark`).
