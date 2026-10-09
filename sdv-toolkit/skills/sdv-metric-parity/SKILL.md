---
name: sdv-metric-parity
description: Use when a metric is shown against a percentile ladder, rank or league average built by another code path — GOP box/percentile cells, sdv-db percentiles, -data summary ladders, team/player ranks — and before merging any change to a metric's definition (numerator, denominator, filter, population, orientation) or to a display-to-ladder mapping. Triggers on "percentile looks wrong", "1st percentile but the value is normal", "mean shown", "ladder", "definition parity", "stuff rate", "red zone rate", and on PRs touching box-score rates, summaries, percentiles or BinionBoxScore mappings. Runs the mean-shown, side-asymmetry and split-sum checks on real data and walks the six defect classes.
---

# Metric-definition parity

A displayed value and the ladder it is ranked against usually come from different code paths that share a column
name, not a definition: sdv-py computes the box value, a `-data` repo builds the ladder, sdv-db stores both, GOP maps
one onto the other. Nothing errors when they drift. The 2026-10-08 audit found 14 such defects across five repos; the
worst showed a normal 13% run-stuff rate as the 1st percentile (it is the ~34th), because the ladder counted
incompletions as stuffs. Read [`references/defect-classes.md`](references/defect-classes.md) before you change a
definition: it lists the six classes with the test that catches each.

## 1. Trace the metric through every layer

For the metric you are touching or checking, find each place it is defined or consumed, and write down the
numerator, denominator, row filter and population at each one:

| Layer | Where to look |
|---|---|
| Producer (box value, per play / per game) | sdv-py `sportsdataverse/<league>/<lg>_pbp.py` flags and the `*_rate` aggregations; `sportsdataverse/registry/` |
| Ladder / summary builder | `cfbfastR-cfb-data` / `nfl-data` summary + percentile stages (`_quantiles`, `input.py` filters) |
| Storage | sdv-db `cfb.percentiles`, `nfl.percentiles`, `*.adv_team_gamelog`, `*_pct` / `_rank` columns |
| Display mapping | GOP `BinionBoxScore.{astro,svelte}` metric → ladder key maps, `misc.ts`, `constants.ts` (`PERCENTILE_YEAR`) |

`rg -n '<metric_or_key>'` in each checkout finds the four sites. If two layers disagree on any of the four
properties, you have a finding before running anything.

## 2. Run the checks on real data

Build two inputs for one season: **values** (one row per unit, computed with the DISPLAY's definition, the same
population as the ladder, e.g. FBS-vs-FBS regular-season team-games, plus a 0/1 `home` column) and the **ladder**
(the wide percentile table the display reads). Then:

```sh
S=<scratch dir>
psql "$SDV_DB_DSN" -c "\copy (select season, game_id, team, is_home::int as home, rushing_stuff_rate,
  yards_per_play from cfb.adv_team_gamelog where season=2025 and season_type=2) to '$S/values.csv' csv header"
psql "$SDV_DB_DSN" -c "\copy (select * from cfb.percentiles where season=2025) to '$S/ladder.csv' csv header"
python <toolkit>/skills/sdv-metric-parity/scripts/ladder_parity.py --values $S/values.csv --ladder $S/ladder.csv \
  --map rushing_stuff_rate=play_stuffed,yards_per_play=yardsplay --side-col home \
  [--split late_sr=late_pass_sr+late_rush_sr] [--season 2025 for a per-season ladder file]
```

Use a read-only session (`PGOPTIONS='-c default_transaction_read_only=on'`): the shell's `SDV_DB_*` point at
production. Parquet inputs work with `uv run --with polars`. Exit 0 = OK/WATCH only, 1 = a failure verdict,
2 = usage or data error (including "no season in both inputs": checking nothing is never OK).

| Verdict | Meaning | Usual class |
|---|---|---|
| `OK` | mean shown within `--tol` (4) of 49.5 | matched |
| `WATCH` | within 2-4 points | small definition drift (sack yards, INT returns, kneels) |
| `MISMATCH` | further than 4 | population or definition mismatch |
| `SIDE-ASYMMETRY` | home and away mean shown differ by > `--side-tol` (25) | orientation (home-relative yard line) |
| `SPLIT-SUMS` | parts add to the whole on most rows | parts divided by the whole population |
| `NO-DATA` | no non-null values for the season | a stage that produced nothing |

Worked example (sdv-db, 2026-10-09, before the cfb-data #139 ladder was republished) — the audit's findings,
reproduced in one command:

```
display                   ladder_p50  mean_shown  verdict
rushing_stuff_rate        0.3         12.14       MISMATCH   (F1: ladder over all plays)
rushing_opportunity_rate  0.2364      95.2        MISMATCH   (C1)
yards_per_play            5.866       47.21       WATCH      (A3: INT-return yards)
yards_per_rush            4.825       49.76       OK
```

Home-field advantage alone moves the sides about 10-15 points apart (CFB 2025 yards/play: home 55, away 40); only a
side pinned near 0 or 100 is a bug, which is why `--side-tol` defaults to 25.

## 3. Check what the data cannot show

The script sees values, not code. Read the display layer for the classes in the reference that live in code:
the ladder season (a constant like `PERCENTILE_YEAR = 2025` ranks every game against one year), era shifts in the
ladder itself (PBU coverage moved havoc medians from 0.10 to 0.145 between 2024 and 2026), null rendered as `0%`
with a percentile, ties ranked at the top of the tie run instead of midrank, and partial spans (a quarter or half)
ranked against a full-game ladder.

## 4. Fix at the definition, then prove it

- Fix the layer that disagrees with the display's definition, usually the ladder. Change the definition in one
  place per repo and keep the column name honest (rename an all-plays column rather than redefining it silently).
- Re-run step 2 on the rebuilt ladder. `OK` with mean shown near 49.5 is the acceptance test; paste the table into
  the PR. A changed definition also means a republish: see `/sdv-reprocess` and `/sdv-dataset-lifecycle`, and note
  that sdv-db's nightly ingest reloads only the current and prior season.
- A definition change that alters published numbers needs a changelog entry in each package repo.
