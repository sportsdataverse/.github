---
name: sdv-model-spine
description: Use when executing a model-spine implementation plan (the ClaudeCowork specs/plans backlog — prediction stacks, ratings engines, projection/impact models) or building any oracle-gated analytics module in an SDV repo. Covers the full loop — isolated worktree + baseline, Phase-0 oracle harness (metrics/constants/leakage split/fixtures), per-task TDD with verified commits, oracle gates with the never-lower rule, league-shim parity, mypy/codegen close-out, reviewer pass, and the session restart prompt. Invoke for "implement T<x>", "start the <sport> model spine", "continue the prediction stack", or any multi-phase model build.
---

# Execute a model spine (SDV)

The repeatable loop for building oracle-validated model stacks in sdv-py (and
siblings). Distilled from the MBB/WBB prediction-stack build — every rule below
paid for itself in a real session. Create one todo per phase/task and keep the
plan's task order unless dependencies force otherwise.

## 0. Setup — isolated worktree + clean baseline

- Plans/specs live in `ClaudeCowork/{plans,specs}/` (see
  `ClaudeCowork/notes/model-build-roadmap.md` for the backlog + dependency notes).
  Read the plan's Global Constraints once; they bind every task.
- **Never build on the user's open checkout** (it usually has an open-PR branch).
  Create a worktree: `git worktree add .claude/worktrees/<slug> -b feat/<slug> origin/main`
  (fetch first; `.claude/worktrees` is gitignored).
- `uv sync --all-extras --dev` in the worktree, then run the relevant suite(s)
  and **record the baseline count**. A dirty baseline is a stop — report it.
- Check the SDD ledger (`.superpowers/sdd/progress.md`) and `git log` before
  starting: tasks already marked complete are DONE — never re-execute them.

## 1. Phase 0 — harness before models

Every spine starts with the validation substrate, not the model:

- **Metrics + constants module** (`<sport>_prediction_constants.py` pattern):
  Brier/log-loss/Spearman/MAE/calibration-table helpers; a frozen
  `LeagueConstants` dataclass + `LEAGUE_CONSTANTS` table + `get_constants()`.
  **League-agnostic algorithms, league-specific constants** — no league number
  is ever hard-coded inside an algorithm function. Seed constants from
  published references and mark which fitting task overwrites them.
- **Leakage split**: an `as_of_*_split(frame, cutoff)` helper returning strictly
  `date < cutoff`. Every predictive backtest rates event G using only data
  before G — this is the line the oracle-gate-reviewer checks hardest.
  **The trap that hit two independent Tier-3/5 spines:** a rating/rate fit
  over the FULL season, then reused inside the per-game as-of walk — the
  public `as_of` param filtered the box scores but NOT the ratings, giving
  false leakage safety while the docstrings claimed "as-of". Recompute every
  rating/rate as-of the event's date; if a per-date recompute is intractable
  at fixture scale, DROP the "as-of" claim and document the full-season
  snapshot caveat — never label as-of anything that isn't.
- **Oracle fixtures**: capture via `/sdv-capture-oracle` (column contracts,
  Utf8 ids, name crosswalk, provenance README). Defer expensive per-game
  oracle samples to the phase that consumes them — don't block Phase 1 on a
  rate-limited scrape. If a high-volume oracle capture throttles on
  stats.nba.com / stats.ncaa.org, route it through the ProxyBonanza pool
  (proven transport `dev/ncaa_proxy.py`: curl_cffi `impersonate="chrome"` +
  rotating proxies) rather than just slowing down — reach for it the moment a
  capture throttles, not after.

## 2. Per-task TDD loop (one commit per task)

1. Write the failing test (plan code verbatim where given).
2. Run it — confirm it fails for the RIGHT reason.
3. Implement minimally. **Add an import in the SAME edit as the code that first
   uses it** — the format-on-save hook strips not-yet-used imports (F401).
4. Run to green + `ruff check`/`format --check` on the touched files.
5. Commit explicit paths (Conventional Commits, no AI trailer) and **verify it
   landed** (`git log -1`; doctoc/ruff can silently abort).

Task-loop gotchas that recur:

- **Name-shadowing check before naming a new module**: if the module and its
  public function share a name, the package `import *` rebinds the attribute
  to the function (three real incidents). Grep the package `__init__` exports
  first; tests that monkeypatch module attrs need
  `importlib.import_module("pkg.mod")`, not `from pkg import mod`.
- **Preview the oracle gate early.** After the core algorithm task, run the
  real-data oracle correlation as a sanity check even though the gate task
  comes later — an algorithm bug is cheapest to find before three more tasks
  stack on it (the AdjEM engine previewed Spearman 0.952 the moment it worked).
- ID dtype discipline: one dtype per id (`Utf8` via `.cast(pl.Int64).cast(pl.Utf8)`),
  assert `left.schema[k] == right.schema[k]` before every join.
- Empty inputs return the documented zero-row schema; `return_as_pandas: bool = False`
  on every public function.

## 3. Oracle gates — the correctness contract

- Set gate floors **from observed values** (rounded with margin), document the
  observed number in the test docstring, and record the rule in the test:
  **never lower a gate to make it pass** — debug the model (possession formula,
  HFA sign, convergence, join direction) instead.
- Match the metric to the model: Brier/log-loss + calibration table for
  probabilities; MAE vs closing market line for spreads/totals; Spearman +
  MAE vs the external oracle for ratings; per-bucket calibration for in-game
  WP; calibration slope for simulators.
- **Every oracle join carries a min-size + dtype guard.** Assert
  `left.schema[k] == right.schema[k]` before the join AND
  `assert joined.height >= <observed N>` after it. A bare `assert height > 0`,
  or an `if height >= N:` with no `else`, lets a shrunken / re-captured fixture
  pass a top-K or Spearman check on a handful of rows (`spearman_corr(n=1)` is
  `nan`; a partial shrink to a few correlated rows passes vacuously). This guard
  was missing on nearly every Tier-3/5 spine's oracle join — write it WITH the
  gate, not at review.
- Fitted constants (σ, HFA, coefficients) come from a committed `dev/` fitting
  script whose output values are pasted into the constants table with a comment
  citing the script + fit sample — never presented as magic numbers.

## 4. Sibling-league parity

Shim the sibling league by reference (`wbb_rapm` pattern): re-export the core
functions, default `league="<sibling>"`, supply the sibling's constants row.
Re-run the same oracle gates on the sibling's fixtures at identical thresholds.

## 5. Close-out (per phase or per session)

1. mypy: type the new modules cleanly, append them to the `[tool.mypy] files`
   ratchet; `git checkout uv.lock` after any `uv run`.
2. Codegen: new public functions (`__all__`) must land in `parsed/` + reference
   docs — `uv run python tools/codegen/generate.py` then `--check` clean.
3. Reviewer pass: `polars-1x-reviewer` + `oracle-gate-reviewer` (+
   `returns-table-auditor` if schemas were added; `port-parity-reviewer` if the
   spine ports external source code).
4. **Publish operability** (if the spine publishes artifacts): add/update the
   owning repo's CLAUDE.md **Model registry row** (model | artifact(s) | release
   tag | training data | fitting script | gates at publish | last retrain |
   cadence — `frozen` valid but explicit; unknown cells `TODO`, never
   fabricated). The retrain path must pass the orphan test — wired into a
   workflow (dispatch-only is fine) or the runbook, never a stranded script
   (`retrain_xg_models.R` failure class). Verify artifact
   `feature_names == *_FEATURES` at package time; consumers re-verify on load.
5. Append the SDD ledger / session note (what shipped, gate results, follow-ups).
6. **Write the restart prompt** so the next session resumes cold:

   ```text
   Continue <spine> in <repo> — <next phase>, inline execution (executing-plans, TDD).
   ## Where things stand
   - Worktree: <path>, branch <name>, N commits ahead of origin/main (<base sha>), UNPUSHED.
   - Plan: <ClaudeCowork plan path>  Spec: <spec path>
   - DONE (do not redo): <modules/tasks + gate results, fixture inventory, suite counts>.
   ## Next up (in order)
   <the next 2-3 tasks with their gates and data dependencies>
   ## Session gotchas (avoid)
   <F401 import-strip, name shadowing, doctoc recommit, uv.lock checkout, codegen regen, ...>
   Start with the ledger check (git log --oneline origin/main..HEAD), then the
   baseline suite, then proceed.
   ```

   Contents are mandatory: ledger-check-first, exact worktree/branch state, a
   DO-NOT-REDO list with gate numbers, and the gotchas that cost time this
   session. Hand it to the user at the stopping point.

7. When merging: hand off to `/sdv-ship` (it owns the PR/CI/bot-review/merge flow).

## Stop conditions (report, don't push through)

- Baseline suite red before any change.
- An oracle gate below its floor after debugging — surface the numbers and the
  hypotheses tried; do not lower the gate or skip it.
- The plan contradicts a repo convention (CLAUDE.md governs — flag, don't guess).
