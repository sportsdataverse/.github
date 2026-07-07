---
name: sdv-port-r-to-python
description: Use when porting R logic into the Python SportsDataverse package (sdv-py) — e.g. translating an nflfastR / cfbfastR / cfbscrapR / baseballr / hoopR R function, reconciling a fix from the pandas `0.36-live` branch into polars `main`, or re-implementing a modeling recipe (EP/WP/QBR/CPOE) from R. Enforces a parity-test-first workflow (golden fixture from the R output → failing parity test → port → green) and the polars-1x + ID-dtype + no-lookaround conventions. Invoke for "port this R function to polars", "port from nflfastR", "reconcile 0.36-live into main", "translate this dplyr/np.select to polars", or "re-implement the R model recipe in Python".
---

# Port R → Python (polars), parity-test-first

The failure this prevents is the recurring one: a port *looks* right, lands, and the
divergence only surfaces downstream (a model rebuild, a join, a season compile) as a
wrong/empty result — then a `fix` → `fail` → `revert` cycle. The fix is to make the
R↔Python divergence a **failing test before the port**, not a surprise after it.

**Create one todo per numbered step below.**

## 1. Pin the canonical R source

Identify the exact upstream R you are porting and read it directly — don't port from
memory of how it "should" work. Canonical sources in the workspace:

- `nflverse-dev/nflfastR/R/*.R` (e.g. `helper_add_ep_wp.R`, `helper_add_fixed_drives.R`,
  `helper_add_series_data.R`) — the EP/WP/series/drives recipes.
- `cfbfastR-dev/cfbfastR/R/*.R` and the `0.36-live` branch of sdv-py (pandas-flavored
  CFB pbp fixes not yet in polars `main`; reconciliation notes live in `dev/`).
- `baseball-dev/baseballr`, `hoopR-dev/hoopR`, `wehoop-dev/wehoop`, `hockey-dev/fastRhockey`.

Quote the specific function + line range you are porting in the parity test docstring so
the provenance is durable.

## 2. Capture a golden fixture (the R output)

Run the R function on a small, representative input and persist its output as the parity
oracle — CSV/parquet under `tests/fixtures/` (or `dev/` if it's a one-off reconciliation).
Capture the *columns you will assert on* plus the join keys. Note the R version + inputs
in a sibling `README.md` or the fixture header, matching the existing fixture provenance
convention.

If the R can't be run locally, hand-derive a few rows from the R logic by inspection and
mark them `# derived-by-inspection` — still better than no oracle.

## 3. Write the failing parity test FIRST

Before porting, add a test that loads the golden fixture and asserts the (not-yet-written)
Python output matches. Use correlation/closeness thresholds for float model columns and
exact equality for categorical/id columns. The nflfastR port's accepted bar is the
template: `ep` 0.996, `epa` 0.994, `wp` 0.997, `vegas_wp` 0.998 on the model domain; a
lower `wpa` ≈0.89 is an SNR ceiling, not a bug (it's exact when fed nflverse's own `wp`).
State the threshold and *why* in the test. Run it; confirm it fails for the right reason.

## 4. Translate idioms — pandas/dplyr/np → polars 1.x

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

Hard rules (from sdv-py CLAUDE.md — these are the high-frequency port bugs):

- **polars 1.x surface only.** No `groupby` / `with_row_count` / `apply` / `pl.count` /
  `cumsum` / `set_at_idx` / `how="outer"` / `str.strip`. If you wrote a 0.18-era call,
  it's a bug (the step-6 review pass catches these).
- **No regex lookaround.** Rust/polars regex rejects `(?=)`/`(?!)`/`(?<=)`/`(?<!)`. To
  stop a capture at a stopword, use the inline case toggle `(?i)prefix(?-i: NAMES)`.
- **ID dtype discipline.** Pick one canonical dtype per id at the boundary and keep it.
  Never `cast(Utf8)` a float-origin id (`123.0` ≠ `"123"`); cast the raw integer. Assert
  `left.schema[key] == right.schema[key]` before any join.
- **Explicit boolean masks.** `pl.col("c") == True`, not bare `pl.col("c")`.
- **Float64 model outputs.** Models emit float32; cast public columns explicitly so a
  `pl.Series(numpy_f32)` can't silently downcast.

## 5. Respect single-owner invariants

Some logic must live in exactly one place — don't re-add it inline during a port:

- **EPA/WPA derivation** lives only in `nfl/ep_wp.py` (`calculate_epa` / `calculate_wpa`).
  Construction modules emit a frame; `ep_wp` applies the models. Don't re-add EPA/WPA in a
  pbp constructor.
- **Player-name/id extraction** for CFB lives in `cfb_play_participants.py`; extend it
  rather than adding new regex in `cfb_pbp.__add_player_cols`.

## 6. Go green, then run the gate

Implement until the parity test passes. Then run the fast inner loop:

```sh
uv run ruff format <changed.py> && uv run ruff check <changed.py>
uv run mypy                                   # if the file is in the [tool.mypy] ratchet
uv run pytest tests/<sport>/ tests/test_id_conventions.py -q
```

New modules must be fully typed and appended to the `[tool.mypy] files` ratchet. Then
**dispatch the `port-parity-reviewer` agent on the ported module(s)** — it is the
comprehensive post-port audit (ID-join dtypes, regex divergence, 1-based indexing,
NA/null/NaN drift, silent recycling, golden-master-test adequacy, module-name shadowing)
and hands polars currency to `polars-1x-reviewer`. Fix its MUST-FIX findings before
escalating to `/sdv-preflight` (scoped sweep) then `/sdv-ship` (full gate).

## 7. Record the reconciliation

If this was a `0.36-live` → `main` port, note the function + commit in `dev/` so the
function-by-function reconciliation map stays current. Don't merge `0.36-live` wholesale —
it's pandas-flavored and would undo the polars migration; port semantic fixes by translation.

## Fan-out mode (multi-module ports)

For a package-scale port (many independent R modules), parallelize steps 1–6 with
one implementer subagent per module instead of porting serially:

- **Cap concurrency at ~6–8** — more trips a server-side rate limit. If completion
  notifications look throttled, the on-disk outputs are ground truth, not the
  notifications.
- **Per-module gate**: a module is DONE only when its golden-master parity test
  (steps 2–3) passes — an agent's "done" report without a green parity test is
  not done. Each agent's brief carries: the pinned R source path, the fixture
  contract, the idiom hard-rules, and its report-file path.
- **Ledger checkpoint**: track per-module status in the SDD ledger, namespaced
  under `.superpowers/sdd/<plan-slug>/` (flat `task-N-*` names clobber across
  plans). On any interruption (rate limit, compaction, session end) resume from
  the ledger + `git log` — never re-dispatch a module the ledger marks complete.
- **Review wave**: after each module goes green (not at the very end), dispatch
  `port-parity-reviewer` on it — findings are cheapest before dependent modules
  stack on top.

## See also

- `port-parity-reviewer` (agent) — the comprehensive post-port audit; dispatch it in step 6.
- `/sdv-build-data` — for the heavy sweep that re-runs a ported pipeline over a corpus in a `-data` repo.
- `sdv-port-python-to-r` — the reverse direction (sdv-py → the SDV R packages).
- sdv-py `CLAUDE.md` "Polars version" + "ID column types" sections are the authoritative idiom/dtype reference.
