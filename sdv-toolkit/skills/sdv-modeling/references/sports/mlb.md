# MLB — pitching, hitting, fielding, game-state

**Correction to this file's own brief:** it describes MLB as "design-only,
never built." That's wrong — `sportsdataverse/mlb/` holds 42 `.py` files, 20
of them the T6.1–T6.4 model modules in the table below (16 carry an explicit
`T6.x` docstring tag), two committed xgboost artifacts, and a publish-scoping
pass naming exact tag composition + live gate values (`mlb-scoping.md`);
`soccer.md` is actually design-only, don't conflate the two. Shorthand:
`pitching-design.md` = `ClaudeCowork/specs/2026-07-07-mlb-pitching-design.md`;
`mlb-scoping.md` = `ClaudeCowork/notes/2026-07-17-mlb-model-publish-scoping.md`.

## Models and where they live

| Program | Models | Module(s) |
|---|---|---|
| T6.1 pitching | Stuff+/Command+ (bundled xgboost RV), xERA (parametric) + SIERA-like (fitted OLS, **unpublished**), TTO/fatigue, pitch reclass (GMM), tunneling (geometry), injury-risk (z-score) | `mlb_stuff_plus.py`, `mlb_command_plus.py`, `mlb_pitch_era.py`, `mlb_pitch_fatigue.py`, `mlb_pitch_classify.py`, `mlb_pitch_sequencing.py`, `mlb_pitch_injury.py` |
| T6.2 hitting | expected stats (xwOBA/xBA/xSLG, EV×LA grid), expected HR, batter aging + Marcel projection | `mlb_expected_stats.py`, `mlb_expected_home_runs.py`, `mlb_batter_projection.py` |
| T6.3 fielding/catching/baserunning | OAA (per-position logistic), catcher framing, catcher blocking+throwing, SB value, baserunning value | `mlb_fielding_oaa.py`, `mlb_catcher_framing.py`, `mlb_catcher_defense.py`, `mlb_stolen_base.py`, `mlb_baserunning.py`, shared engine `mlb_run_values.py` |
| T6.4 game-state | RE24, win expectancy/WPA/leverage, umpire zone bias, team projection (pythagenpat+Elo), team-runs/K props | `mlb_run_expectancy.py`, `mlb_win_expectancy.py`, `mlb_umpire_zone.py`, `mlb_team_projection.py`, `mlb_prop_projection.py` |

**Stuff+/Command+ mechanism** (the only two needing a bundled artifact):
xgboost regresses per-pitch `delta_run_exp` on standardized physics +
fastball-relative deltas (Stuff+) or location+count/handedness (Command+);
both map to a `100=avg` `+`-scale via a shared `_to_plus` sign-inverted
z-score. Command+ ships as **Location+** in substance — no catcher-target
field in Statcast, so "aimed here, missed" ≡ "aimed here, hit it"
(`mlb_command_plus.py:1-17`; `pitching-design.md` §3.4). Every other model
is parametric/compute-on-demand by policy (`pitching-design.md` §3.2).

## Data feed

**Correction (2026-09-01):** MLB now HAS release datasets — `baseballr-data`
publishes four model tags (`mlb_game_state`, `mlb_hitting_models`,
`mlb_pitching_models`, `mlb_fielding_models`; per-season parquet + csv + rds,
see its `models/REGISTRY.md`) and sdv-py ships real loaders
(`load_mlb_expected_stats`, `load_mlb_expected_hr`, `load_mlb_batter_projection`,
`load_mlb_stuff_plus`, `load_mlb_command_plus`, `load_mlb_oaa`,
`load_mlb_catcher_framing`, `load_mlb_re`). The TRAINING substrate is still
self-collected live via `mlb_statcast_search` into per-season caches
(`SDV_MLB_STATCAST_CACHE`); `mlb_pitch_features.py` is the single Savant
consumer for the pitching family so every model reads one shared per-pitch
frame (`pitching-design.md` §3.3).

## Gotchas

- **Three-way input-contract split drives the publish CLI**: only RE24 +
  hitting self-load by season; pitching/fielding need a pre-fetched Savant
  frame — publish does one season pull, fans it into all three ("the NBA
  'one possession pass, many models' lesson again," `mlb-scoping.md`).
- **SIERA-like is placeholder-coefficient, do-not-publish**; catcher
  throwing/blocking, baserunning, SB value are **data-ceiling-limited**
  (live floors 0.03–0.073 vs 0.80–0.85 targets) — scope exclusions, not
  bugs (`mlb-scoping.md`).
- **Ceiling-bound corpus**: Stuff+/Command+ fit on 2023 only, ~30 pitchers,
  vs Statcast's 2015+ availability (`data-sources.md` §1c). RE288 lives in
  game-state (`mlb_run_values.py`), not fielding — a scope correction the
  plan itself had wrong (`mlb-scoping.md`). As-of-date leakage is enforced
  via `as_of_seasons_split`/`as_of_split` — season *Y* only sees `season <
  Y` (`mlb_batter_projection.py:1-8`).

- **PA-ender discipline (2026-09-01, `sportsdataverse-py#421`).** Every
  hitter count is gated by `events` non-null/non-empty: `pa` = PA-ending rows,
  `ab` excludes walks/HBP/sacrifices/catcher's interference, the wOBA
  denominator excludes intentional walks, sac bunts and catcher's interference,
  and walk/HBP wOBA values default to `.69`/`.72` when the cache vintage lacks
  `woba_value`. The bug that motivated it counted raw PITCH rows as PA and
  published league-mean "xwOBA" of .44–.73 (`failure-modes.md` §21).
- **Cache vintages are heterogeneous.** Seasons under `SDV_MLB_STATCAST_CACHE`
  were captured at different times; `woba_denom`/`woba_value` and other derived
  columns are null in older vintages. Derive denominators from `events`; never
  trust a cached derived column across seasons without a null-rate check.
- **Rank gates are scale-blind here too.** The publish gates were Spearman vs
  Savant leaderboards and stayed green through a 2x scale error; the level band
  (`pa >= 100`, `n >= 50`, xwOBA `[.26, .38]`, xBA `[.18, .30]`) in
  `baseballr-data python/mlb_model_publish/computes.py` is publish-blocking and
  must stay beside the rank gate (`metrics-and-gates.md` §6).
- **xERA ≡ x_wOBA is BY DESIGN** — `mlb_pitch_era` is a documented affine
  wOBA→runs conversion; a render-time identity check guards the recipe, it is
  not a bug. Differentiating xERA (batted-ball mix, park) is a new model.

## Oracle

No committed sdv-py fixture like CFB/MBB/NHL have in `data-sources.md` §4 — MLB gates against **live** Savant leaderboards (xERA MAE, Stuff+ rank, RE24 vs. Tango/Lichtman/Dolphin) plus internal calibration: hitting "≥0.95 offline/≥0.90 live," OAA "live 0.55/obs .605," framing "live 0.40/obs .468," Command+ "≥0.04 directional only" (`mlb-scoping.md`) — a real gap, not an oversight.
