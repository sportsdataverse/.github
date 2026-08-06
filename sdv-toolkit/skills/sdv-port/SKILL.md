---
name: sdv-port
description: Use when porting logic between R, Python, and dataframe engines in the SportsDataverse ecosystem, in any direction. Directions — r-to-python (nflfastR / cfbfastR / cfbscrapR / baseballr / hoopR / bigballR into sdv-py), python-to-r (sdv-py into cfbfastR / hoopR / wehoop / baseballr / fastRhockey / softballR), and pandas-to-polars (converting df.loc / np.select / df.assign / groupby().transform / merge blocks, or reconciling a pandas fix from the sdv-py 0.36-live branch into polars main). Enforces a parity-test-first workflow — golden fixture captured from the source-language output on REAL data, then a failing parity test, then the port, then green — plus the polars-1x, ID-dtype, and no-lookaround conventions, R numeric fidelity when output must match bit-for-bit, and oracle integrity when the captured reference is itself suspect. Invoke for "port this R function to polars", "port from nflfastR", "port from bigballR", "port this to cfbfastR", "translate this dplyr to polars", "translate this np.select to polars", "convert this pandas code to polars", "reconcile 0.36-live into main", "re-implement the R model recipe in Python", "bring this Python fix back to the R package", or when a parity test fails on a handful of rounding-boundary cells.
---

# Port between R, Python, and dataframe engines, parity-test-first

The failure this prevents is the recurring one: a port *looks* right, lands, and the
divergence only surfaces downstream (a model rebuild, a join, a season compile, a pkgdown
example) as a wrong/empty result — then a `fix` → `fail` → `revert` cycle. The fix is the
same regardless of direction: make the divergence a **failing test before the port**, not
a surprise after it.

**Create one todo per numbered step below.**

## 0. Pick your direction

| Direction | Source → target | Reference |
|---|---|---|
| `r-to-python` | R package (nflfastR / cfbfastR / cfbscrapR / baseballr / hoopR / bigballR) → sdv-py (polars) | `references/r-to-python.md` |
| `python-to-r` | sdv-py (polars) → an SDV R package (cfbfastR / hoopR / wehoop / baseballr / fastRhockey / softballR) | `references/python-to-r.md` |
| `pandas-to-polars` | pandas/numpy (incl. the sdv-py `0.36-live` branch) → polars 1.x `main` | `references/pandas-to-polars.md` |

Read the matching reference file now — it has the canonical source locations, the idiom
map, and the bug-class table for your direction. Steps 1–6 below are the spine that's
identical across all three; the reference file is where the direction-specific mechanics
live.

## 1. Pin the canonical source

Identify the exact thing you are porting and read it directly — don't port from memory of
how it "should" work. Quote the source function + line range in the parity test / roxygen
provenance so it's durable. Your reference file lists canonical source repo paths for this
direction.

## 2. Capture a golden fixture from the source-language output — real data, never synthetic

Run the source function on a small, representative **real** input and persist its output as
the parity oracle (CSV/parquet under `tests/fixtures/`, or `dev/` for a one-off
reconciliation). Capture the columns you'll assert on plus the join keys, and note the
source version + inputs in a sibling `README.md` or the fixture header.

**The capture path itself can corrupt the oracle — verify it before you trust it.** This
applies in every direction: an R browser/rvest capture can mangle a payload, a stale sdv-py
cache can hold last season's data, a pandas index misalignment can silently reorder rows
before the fixture is written. When a captured column is provably wrong-by-construction,
**do not port the bug to match it** — fix it, and if you can't fix the capture, partition
the oracle columns (strict / promoted / invariant-covered) and say so in the test docstring.
Your reference file has the direction-specific version of this failure mode.

## 3. Write the failing parity test FIRST

Before porting, add a test that loads the golden fixture and asserts the (not-yet-written)
output matches — `pytest` for a Python target, `testthat::test_that()` for an R target. Use
correlation/closeness thresholds for float model columns (state the threshold and *why*) and
exact equality for categorical/id columns. Run it; confirm it fails for the right reason —
not an import error or a fixture-loading bug.

## 4. Translate idioms

Use the idiom map in your direction's reference file, and apply its bug-class table as you
go (ID-dtype discipline, regex semantics, indexing base, null/NA handling, and — when the
target must match bit-for-bit — R numeric fidelity). These are the highest-frequency port
bugs in this ecosystem; treat every one of them as a checklist item, not background reading.

## 5. Respect single-owner invariants (when porting into sdv-py)

For `r-to-python` and `pandas-to-polars` (both land in sdv-py), some logic must live in
exactly one place — don't re-add it inline during a port:

- **EPA/WPA derivation** lives only in `nfl/ep_wp.py` (`calculate_epa` / `calculate_wpa`).
  Construction modules emit a frame; `ep_wp` applies the models.
- **CFB player-name/id extraction** lives in `cfb_play_participants.py`; extend it rather
  than adding new regex in `cfb_pbp.__add_player_cols`.

For `python-to-r`, check whether the target R package has an equivalent single-owner module
before adding parallel logic.

## 6. Go green, then run the gate and dispatch review

Implement until the parity test passes. Then run the target's fast inner loop.

Python target (`r-to-python`, `pandas-to-polars`):

```sh
uv run ruff format <changed.py> && uv run ruff check <changed.py>
uv run mypy                                   # if the file is in the [tool.mypy] ratchet
uv run pytest tests/<sport>/ tests/test_id_conventions.py -q
```

New modules must be fully typed and appended to the `[tool.mypy] files` ratchet.

R target (`python-to-r`):

```r
devtools::document()
devtools::test()                 # parity test + package tests
devtools::check()                # R CMD check (or the package's CI-parity target)
```

**Review, mandatory:**

- **`sdv-parity-reviewer`** — always, on the ported module(s). It's the comprehensive
  post-port audit (ID-join dtypes, regex divergence, indexing base, NA/null/NaN drift,
  golden-master-test adequacy) and works in every direction.
- **`sdv-python-reviewer`** with the `polars` lens — always, when the change lands Python
  code (`r-to-python`, `pandas-to-polars`).
- For `python-to-r`, also run the target package's R-side reviewers
  (`roxygen-doc-reviewer` / `returns-table-auditor`) per `references/python-to-r.md`.

Fix MUST-FIX findings before escalating to `/sdv-preflight` (Python target) or the
package's own CI-parity check (R target), then `/sdv-ship`.

## 7. Record 0.36-live reconciliations (when applicable)

If this was a `0.36-live` → `main` port (`r-to-python` or `pandas-to-polars`), note the
function + commit in `dev/` so the function-by-function reconciliation map stays current.
Don't merge `0.36-live` wholesale — it's pandas-flavored and would undo the polars
migration; port semantic fixes by translation.

## Fan-out mode (multi-module ports)

For a package-scale port (many independent modules), parallelize steps 1–6 with one
implementer subagent per module instead of porting serially:

- **Cap concurrency at ~6–8** — more trips a server-side rate limit. If completion
  notifications look throttled, the on-disk outputs are ground truth, not the
  notifications.
- **Per-module gate**: a module is DONE only when its golden-master parity test
  (steps 2–3) passes — an agent's "done" report without a green parity test is not done.
  Each agent's brief carries: the pinned source path, the fixture contract, the idiom
  hard-rules for the direction, and its report-file path.
- **Ledger checkpoint**: track per-module status in the SDD ledger, namespaced under
  `.superpowers/sdd/<plan-slug>/` (flat `task-N-*` names clobber across plans). On any
  interruption (rate limit, compaction, session end) resume from the ledger + `git log` —
  never re-dispatch a module the ledger marks complete.
- **Review wave**: after each module goes green (not at the very end), dispatch
  `sdv-parity-reviewer` on it — findings are cheapest before dependent modules stack on top.

## See also

- `references/r-to-python.md`, `references/python-to-r.md`, `references/pandas-to-polars.md`
  — the idiom map + bug-class table for each direction.
- `sdv-parity-reviewer` (agent) — the comprehensive post-port audit; dispatch it in step 6.
- `sdv-python-reviewer` (agent, `polars` lens) — polars-1x currency check for Python-target ports.
- `/sdv-build-data` — for the heavy sweep that re-runs a ported pipeline over a corpus in a `-data` repo.
- sdv-py `CLAUDE.md` "Polars version" + "ID column types" sections are the authoritative
  idiom/dtype reference for the Python side.
