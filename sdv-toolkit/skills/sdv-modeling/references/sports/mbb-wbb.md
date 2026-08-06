# MBB / WBB

25-spine roadmap Tier 1 (`roadmap.md` L20-26): T1.0 Prediction & Tournament,
T1.1 Player-Value & Projection, T1.2 Shot Quality — all **specced** at
compile time (`roadmap.md` L12 status legend, ✅ = "spec+plan written"; L14
"all 25 spines... have a spec+plan pair on disk... **Nothing committed to
any repo**"). What's actually shipped is verified below against the code,
not against this roadmap's ✅ marks.

## 1. Models and where they live

- **Rating engine (T1.0, model ①):** `mbb_team_ratings.py:25` imports `_common/ratings.py::iterative_opponent_adjust` — a **KenPom-style fixed-point solver**; `roadmap.md` L129 says it's shared with NBA and *mathematically distinct* from the CFB/NFL ridge family (`opponent_adjusted_ridge`), "don't force-unify." Produces AdjO/AdjD/AdjEM.
- **Bracketology + season sim (T1.0 phase 5/6, also shipped):** `mbb_bracketology.py` (resume-score seeding + at-large selection, blending ① with SoS/WAB) and `mbb_season_sim.py` (Monte Carlo sampling `margin ~ Normal(exp_margin, margin_sd)` off the Phase-2 closed form, seeded `numpy.random.default_rng`); `wbb_bracketology.py`/`wbb_season_sim.py` mirror both.
- **A second, different KenPom-style solver** feeds player-value: `mbb_ncaa_strength.py::run_iterative_adjustment_with_hca` (`:611-637`, ported from hoop-explorer) is a Jacobi iteration — `adj_game = raw_game * (league / (opp_adj ± hca))`, re-estimating HCA from home/away possession-imbalance residuals each sweep, over per-game shooting rates — not the same code as the team-efficiency solver above. `data-sources.md` §4 cites this file (`:1,16,621`) as the ecosystem's fixed-point-solver reference since real KenPom has no captured corpus (paywalled).
- **Prediction stack (T1.0 phase 2):** `mbb_game_predict.py` — closed-form pregame margin/win-prob/total from the ratings above, plus a bundled xgboost/logistic in-game WP artifact (`:1-39`). League-agnostic; HFA/sigma/tempo come from `mbb_prediction_constants.py`'s `LeagueConstants` table.
- **Player-value spine (T1.1):** `mbb_rapm.py`/`mbb_box_bpm.py` + `mbb_ratings.py`'s individual O/D rating (Dean-Oliver ORtg/DRtg, ported from hoop-explorer, `:1-16`) feed the RAPM prior — see `methods.md`'s Possession-engines section for the schedule-strength anchoring + freshman-prior mechanism (cross-ref, not re-derived here).
- **Shot quality (T1.2):** `mbb_shot_quality.py` + `mbb_shots_adapter.py`.

WBB is not a separate port: it's a **thin shim over the MBB engine** — the algorithms are league-agnostic, so `wbb_team_ratings.py` (65 lines) re-exports `mbb_team_ratings.py`'s (405 lines) functions **by reference** and just calls them with `league="womens"` (`wbb_team_ratings.py:1-8,42-65`); same pattern for `wbb_ratings.py`/`wbb_rapm.py`/`wbb_game_predict.py` (`mbb_prediction_constants.py:41-47`).

## 2. Data feeding these models

`data-sources.md` §2 MBB table (11 loaders, `sdv-release`,
`espn_mens_college_basketball_*`) — cross-ref, don't duplicate. `mbb_team_ratings.py`
imports `load_mbb_schedule`+`load_mbb_team_boxscore` directly (`:26`, floor 2002/2002
each) — note this diverges from `data-sources.md` §2's prose, which names
`load_mbb_pbp` for T1.0 instead; trust the import line over the prose here.
T1.1/T1.2 additionally need `load_mbb_player_boxscore`/`load_mbb_shots`, floor
**2025** — a structural ceiling, not a choice (`data-sources.md` §2, `audit.md`
§MBB/WBB). WBB is not a floor mirror: `load_wbb_standings`/
`_team_season_stats` floor **2026** vs MBB's 2003; `_game_rosters`/
`_officials`/`_player_season_stats`/`_rosters`/`_shots` floor 2026 vs MBB's
2025 (`data-sources.md` §2).

## 3. Gotchas

- **NCAA shot-coordinate axis swap.** NCAA `ShotLocation` is
  `(x=up-court, y=lateral)` — opposite the canonical ESPN schema
  (`shot_x=lateral, shot_y=up-court`); `mbb_shots_adapter.py:172-177` swaps
  at ingestion. Feeds T1.2.
- **In-game WP's training window is far narrower than its data floor.**
  `load_mbb_pbp`/`load_wbb_pbp` floor 2002, but the shipped artifact was fit
  on **2023 only** — could train 2006-2026 (MBB)/2008-2026 (WBB) today but
  doesn't (`data-sources.md` §1c).
- **College small-sample constraint on RAPM priors** — cross-ref
  `methods.md` Possession-engines: ~1,500 poss/season for a high-minute
  starter vs >5,000 NBA, so ridge alone often can't separate players who
  rarely play apart. Don't re-derive here.
- Floor divergence (§2) is a structural ceiling, not a producer defect.

## 4. Oracle

Cross-ref, don't re-derive: `data-sources.md` §4 — Torvik/Barttorvik ratings
(Spearman(`adj_em`) ≥0.95, observed 0.990), Torvik BPM (player-value,
~97.3% name-matched to `team_id`), ESPN BPI (SoS Spearman gate). `metrics-and-gates.md` §1 —
`mbb-prediction-backtest.py` gates win-prob **calibration slope** (not the
general per-time-bucket rule) to `[0.9, 1.1]` on neutral courts; §4 —
`ncaa-crosswalk-test.py` match-rate floors (0.97 recent / 0.95 overall).
