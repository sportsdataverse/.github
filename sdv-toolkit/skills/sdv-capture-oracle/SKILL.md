---
name: sdv-capture-oracle
description: Use when capturing an external oracle/validation corpus into committed test fixtures — Torvik/KenPom ratings, ESPN BPI/predictor/odds, market closing lines, MoneyPuck, published RAPM/EPM, or any third-party reference a model gate will assert against. Covers column contracts, Utf8-id discipline, the team/player name-crosswalk recipe (contracting normalizer + candidate keys + alias table + match-rate reporting), rate-limit-aware sampling, and the mandatory provenance README. Invoke for "capture the oracle corpus", "commit the <source> fixtures", or any Task-0-style fixture capture in a model plan.
---

# Capture an oracle corpus to committed fixtures (SDV)

Oracle fixtures are the ground truth every model gate asserts against — a wrong
or undocumented fixture silently corrupts every downstream gate. This is the
Task-0.1 pattern from the prediction-stack builds.

## 1. Contracts before code

- Write the **column contract per fixture file first** (names, dtypes, one line
  of meaning) — usually already in the plan. The capture script conforms to the
  contract, never the reverse.
- **Every id is `Utf8`, cast from the raw integer**:
  `pl.col("id").cast(pl.Int64).cast(pl.Utf8)` — never stringify a float
  (`"123.0"`). Columns snake_case. Fixtures are parquet under
  `tests/fixtures/<domain>/`.

## 2. Probe the real shapes before writing the capture script

Run a throwaway probe (scratchpad, not committed) that prints each source's
actual columns/sample rows and each remote endpoint's **content type + first
lines**. Real incidents this catches:

- An endpoint that returns HTML where you expected CSV (barttorvik `trank.php`
  is bot-blocked; the static `<year>_team_results.csv` works).
- Loader column names that differ from the plan's sketch (`home_id` vs
  `home_team_id`, string `date` + proper `game_date`).
- Savant-style content-type heterogeneity (JSON vs CSV vs HTML-embedded blobs).

The capture script itself lives in `dev/<domain>/capture_oracle.py`
(gitignored), rerunnable end-to-end, printing per-file row counts.

## 3. The name-crosswalk recipe (oracle keyed on names, not ids)

External sources key on team/player NAMES; your fixtures key on provider ids.
The proven two-tier matcher:

1. **Contracting normalizer**: lowercase, strip everything but `[a-z0-9]`.
   Build the provider key set from every name variant you have (location,
   display name, slug minus mascot).
2. **Candidate-key expansions** for the source's systematic shorthands — try
   the identity form PLUS each expansion, match if any hits. College example:
   trailing `St.` → both `X State` and bare `X` (Grambling, McNeese); mid
   `Cal St. X` → `Cal State X`; leading `St.` stays (St. John's). One-way
   expansion regressed real matches — always candidate sets.
3. **Explicit alias table** for the true one-offs (`connecticut→uconn`,
   `mississippi→olemiss`, `umkc→kansascity`). Seed it from the first run's
   unmatched report; keep it in the capture script, commented.
4. **Report the match rate + the full unmatched list every run.** Iterate until
   the unmatched tail is only one-off irregulars, then STOP — a 96%+ match is
   statistically immaterial to a rank-correlation gate; chasing 100% via fuzzy
   matching risks silent wrong matches, which are worse than drops. Record the
   final rate + the dropped names in the README.

## 4. Rate limits — sample, don't sweep

- Per-game oracle samples (ESPN predictor/odds) are a rate-limited scrape:
  capture a **stratified sample** (a few hundred games across the season), not
  the full slate — the Brier/MAE gates need representativeness, not coverage.
  ESPN Core v2 403s under aggressive parallelism; keep it low, bound attempts.
- **Defer expensive captures to the phase that consumes them** and say so in
  the README ("Not yet captured" section) — don't block Phase 1 on Phase 2's
  oracle. Design the corpus-loading test fixture with optional entries.

## 5. Provenance README (mandatory, committed with the fixtures)

Per file: source (URL or wrapper name), capture date, season, row count, and
the id-dtype note. Plus: the crosswalk match rate + unmatched list, any known
gaps (e.g. "adj_tempo null — tempo endpoint bot-blocked; no gate depends on
it"), and the regeneration command. The doctoc pre-commit hook will inject a
TOC and abort the first commit — re-add and re-commit.

## Stop conditions

- A fixture whose schema can't meet the plan's column contract — surface the
  divergence, don't silently reshape the contract.
- Match rate below ~90% after expansions + aliases — the normalizer is missing
  a systematic pattern; report the unmatched list instead of force-matching.

## Boundaries (which capture skill governs)

- **Single API payload for a parser fixture / returns schema** → `/sdv-capture-endpoint`
  (structured id-walk, error-envelope skip, atomic writes).
- **Long-running scrape (>3 min) or a `-raw` repo's committed tree** → `/sdv-scrape-job`
  (user-executable runbook, resumable checkpoint, env-only rate tuning).
- **This skill** owns model-gate oracle corpora: external reference values committed as
  test fixtures with contracts, crosswalks, and provenance.
