---
name: sdv-standardize-repo
description: Use when bringing an SDV `-raw` or `-data` repo onto the standard template (root pyproject/uv.lock, python/ + tests/ split, bash-only scripts/, CI, purges, R/Python dual-pipeline parity) — the executed sequence from pilots 1–6 (wehoop-wbb pair, hoopR-nba-stats pair, wehoop-wnba-stats pair) with every landmine those pilots hit. Invoke for "standardize <repo>", "bring <repo> onto the template", "repo standardization pilot", or the fan-out to the remaining -raw/-data repos.
---

# Standardize an SDV `-raw`/`-data` repo

Authoritative spec: `ClaudeCowork/specs/2026-08-01-data-raw-repo-standardization-design.md`
(decisions D1–D43 + lessons §12.5–12.7). This skill is the executed ORDER with
the traps inlined. Work on `main` via small verified commits (or PRs per repo
protection); the pilots proved 20-file PRs get real bot reviews and 2,000-file
ones get silently skipped — split accordingly.

## Sequence (each step = one commit, verified before the next)

1. **Survey first, trust nothing written.** `git status` (other sessions leave
   WIP — never clobber; fold in only self-consistent 2-line cleanups, with
   attribution in the message). Diff `CLAUDE.md`/`copilot-instructions.md`
   claims against `ls` — pilots found files calling live repos "empty
   placeholders" and instructing agents to revert the standardization.
   Correcting actively-false directives belongs in the FIRST commit.
2. **Packaging to root**: `pyproject.toml` + `uv.lock` at root (merge any
   nested `python/pyproject.toml`); package-dir stays `python/`; `tests/` to
   root; kill `requirements.txt`; pinned ruff rule set (`E4 E7 E9 F I`,
   ignore `E712`); pytest `testpaths`/`pythonpath` + an `archive` marker;
   `sportsdataverse` pinned to git main via `[tool.uv.sources]`; `.Rproj`
   beside `DESCRIPTION`; template gitignore block (bare AND `**/` nested).
   Annotate any deliberately-tracked dir that looks like build output
   (`.bundles/`) IN the gitignore, or someone will "fix" it.
3. **Moves**: `scripts/*.py` → `python/`; tests out of `scripts/`; update every
   reference (`grep -rn "scripts/[a-z_]*\.py"` over sh/yml/md). Interpreter
   resolution via a sourced `scripts/_venv.sh` (this repo's `.venv`, env
   override, loud failure) — pilots found three scripts hardcoding a SIBLING
   repo's venv. Never `uv run` inside long-running scrape entry points (it
   re-syncs mid-sweep); reserve it for tests/lint.
4. **Gates**: `uv lock && uv sync --dev`, full pytest, `ruff check --fix`,
   `bash -n scripts/*.sh`. Wiring pytest for the first time WILL surface dead
   tests and stale paths — fix them here, they are why this step exists.
5. **CI** (`tests.yml`): sparse checkout (`python tests scripts pyproject.toml
   uv.lock` — a 500k-file archive checkout never finishes), `uv sync --frozen`,
   `pytest -m "not archive"`, ruff, `bash -n`. ~30s on a 490k-file repo.
6. **Purges** (own commit, HEAD-only, never rewrite history): committed raw
   JSON superseded by the `-raw` sibling — but "superseded" is a PER-FILE
   claim: diff game-id sets first and copy anything only-here into the raw
   store (pilot 4 found 85 preseason games per family that the sweep's
   season-type scope never captures). `.qs` + `.csv.gz` per D30.
7. **R/Python dual-pipeline parity** (`-data`) — **DO NOT retire the R chain.**
   Standing policy (2026-08-03): Python is the PRIMARY pipeline and gets the
   work; R is maintained alongside it as a methodological/language equivalent;
   **both sides move together when either changes**. Two R chains were retired
   on 2026-08-02 under the old rule and had to be restored
   (`hoopR-nba-stats-data` 645 lines, `nfl-data` 251) — if a repo has no R
   twin, that is a gap to fill, not a state to preserve.
   - **Parity is DATASET-level, not file-level.** The two sides decompose
     differently on purpose: R is dataset-per-file
     (`espn_{lg}_NN_{dataset}_creation.R`), Python is layer-per-module
     (`{lg}_data_build/{ingest,reshapers,build,publish}.py`) with datasets as
     registry rows. There is no `01_pbp.R` ↔ `01_pbp.py` pair to couple; the
     shared key is the dataset name, which `config.REGISTRY` already carries
     ("Mirrors each `espn_{lg}_NN_*_creation.R` script").
   - **Neither side is automatically authoritative.** A divergence is a review
     item — do not "fix" R to match Python or vice versa without deciding which
     is methodologically right. (`cfb-data` is the exception with an explicit
     rule: R is the released producer there, so python builders parity-match.)
   - Workflows may still be Python-only — restoring the twin preserves the
     METHOD in a second language, it does not re-schedule R. When rewriting a
     workflow: uv, raw store over `raw.githubusercontent.com`, season default
     computed in bash (NBA rolls over in OCTOBER; WNBA is calendar-year — never
     copy one league's rule to the other). Keep an annual job if the daily cron
     windows miss an event (WNBA draft is mid-April; daily runs May–Oct).
8. **Docs/close-out**: update the repo's own agent-facing docs to the new
   layout; record lessons in the spec (§12.x); memory topic update.

## Traps that cost real time in pilots (verify, don't assume)

- **Verification must name the ref it verifies.** `ahead=$(git rev-list
  origin/main..main)` says nothing while on a feature branch — this masked an
  unmerged fix TWICE. Print `HEAD=$(rev-parse --short HEAD)
  origin/main=$(rev-parse --short origin/main)` instead.
- **Check `git status` AFTER committing.** A failed pathspec inside
  `git add -A -- a b c` silently drops the rest; a pilot shipped a workflow
  invoking a script deleted in the same "commit".
- **Pre-commit hooks mutate**: ruff-format strips not-yet-used imports (add
  imports in the same edit as first use); a hook-modified file aborts the
  commit — re-add and re-commit; ALWAYS confirm with `git log -1`.
- **Windows process checks lie**: `pgrep -f` cannot see native `python.exe`
  command lines, and a `CommandLine -match` filter matches the checking shell
  itself. Judge liveness by log growth or an explicit watched PID
  (`commit_loop.sh <pid>` pattern), never by process-name counts.
- **Kill by CIM + command-line filter, never by process name** — blanket
  `Stop-Process python` would have killed another session's 25-worker
  campaign.
- **Backfills must commit as they run**: launcher starts
  `scripts/commit_loop.sh $$` and flushes once at exit; presence-based resume
  makes stranded-uncommitted work invisible.
- **Bot review economics**: CodeRabbit skips >100 files, Sourcery >300 and
  has a weekly diff budget a purge PR can exhaust for the whole org. Put the
  reviewable logic in the small PR; note the skip in the bulk one.
- For `-raw` capture semantics (write guards, zero-row vs `{}`, floors,
  measure domains, poisoned defaults), defer to
  `sdv-internal-refs/nba/API_NOTES.md` + `ENDPOINT_DECISIONS.md` — those are
  provider-specific and normative there.

## Deferred-by-design (don't scope-creep into step 2)

Numbered thin builders, docs.py + column-description stores (author per
league, NEVER borrow by column name), pydantic models from built parquets,
schedule-master artifacts (D34). These are their own phase, gated on a tested
build package existing; the stats pair's phase is tracked in the plan
close-out.
