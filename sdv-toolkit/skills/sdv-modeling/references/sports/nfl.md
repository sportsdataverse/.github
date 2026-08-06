# NFL — models, data, gotchas, oracle

`methods.md` explicitly does not cover NFL rating systems, EP/WP/CP/xYAC, or simulation ("Not covered" / "The corpus does not cover this family") — this file is the only place those three method families are documented. Ported from the shipped T4.2 ratings/market spine (`plan.md`/`design.md`) and verified against the code that shipped, which now exceeds both.

| Shorthand | Path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `plan.md` | `ClaudeCowork/plans/2026-07-07-nfl-ratings-market.md` |
| `design.md` | `ClaudeCowork/specs/2026-07-07-nfl-ratings-market-design.md` |
| `CLAUDE.md` | `sdv-py/CLAUDE.md` ("ep_wp model application" section) |
| `ratings-oracle.py` | `sdv-py/tests/nfl/test_nfl_ratings_oracle.py` |
| `backtest.py` | `sdv-py/tests/nfl/test_nfl_prediction_backtest.py` |

## 1. Models + mechanism

**Ratings** (`nfl_ratings.py`) — `efficiency_ratings`/`special_teams_ratings` fit `opponent_adjusted_ridge` (offense + defense team indicators + intercept + HFA, penalize only team coords) on `load_nfl_pbp`'s already-computed `epa`, filtered to competitive plays (`special/qb_kneel/qb_spike != 1`, naive `wp` in `[0.05, 0.95]` — never `vegas_wp`). `adj_net = adj_off_epa - adj_def_epa`; ST teams with no ST plays get neutral `0.0`. The solver now lives in shared `sportsdataverse/_common/ratings.py`, imported by NFL — the T7.2 cross-league extraction `design.md` flagged as future work already happened (`nfl_ratings.py:8-11,26`). Fitted `ridge_lambda = 25.0`, the min of the searched grid `{25,50,100,200,400,800}` (`nfl_prediction_constants.py:35-38`).

**EP/WP/CP/xYAC** — single owner `ep_wp.py`; `enrich_nfl_pbp(method="lead_diff")` is the only implemented method (`method="snapshot"` still raises `ValueError`, `ep_wp.py:3803-3805`). Era cuts verified in code: `ERA_SEASON_CUTS = (2001, 2005, 2013, 2017)` (`model_vars.py:40`, matches `CLAUDE.md`). Kickoff/PAT feature substitution — `down`→1, `ydstogo`→10, touchback yardline `TOUCHBACK_YARDLINE_PRE_2016=80` / `_POST_2016=75` (`model_vars.py:45,54`) — is the parity lever; the 2016 value is *lower* because the 2016 rule moved the touchback spot from the 20 to the 25 — farther from the receiving team's own goal line (better field position), so `yardline_100` (distance to the opponent's goal) drops from 80 to 75. Parity vs nflfastR: ep 0.996, epa 0.994, wp 0.997, vegas_wp 0.998; wpa ≈0.89 is a first-differencing SNR ceiling, not a derivation bug (`CLAUDE.md`).

**Decision surfaces** (`nfl_fourth_down.py`) — an nfl4th port: `get_go_wp`/`get_fg_wp`/`get_punt_wp` (punt uses a bundled `punt_data.parquet` landing distribution, prob-weighted over the receiving team's ensuing-drive WP); `fourth_down_recommendation` is the max-WP choice among go/punt/field-goal, `wp_added = 100*(go_wp - max(fg_wp, punt_wp))` in points.

**QBR** — `qbr_model.ubj` is bundled but ships **no `.card.json`**, unlike all 7 of CFB's model artifacts (`sportsdataverse/cfb/models/*.card.json` exist; the same glob under `nfl/models/` is empty). Combined with "training window unknown, no script found anywhere" (`data-sources.md` §1c), QBR has no recorded provenance at all.

**Simulation** (`nfl_simulations.py`) — a faithful vectorized port of `nflseedR::nfl_simulations()` + `nflseedR_compute_results` (MIT), full NFL tiebreakers, round-by-round playoffs with reseeding, draft order; seeded via a `numpy` RNG (`seed` param), one vectorized pass instead of nflseedR's `furrr`-chunked parallelism.

**Market ②** (`nfl_market.py`) — closed-form: `predict_margin`, `win_prob_from_margin = Φ(margin/σ)`, `predict_total`; `market_edge = exp_margin - close_spread_home` is display-only, asserted never to feed back into ①/②/③ (`nfl_market.py:6,149`). **Props ③** (`nfl_player_props.py`) — empirical-Bayes usage×efficiency×matchup×game-script, shrunk toward position priors.

## 2. Data

Ratings/market/props all read `load_nfl_pbp` (`nfl_model_pbp`, 1999–2025 per `data-sources.md` §1c/§2 — not a fresh scrape) + `load_nfl_schedule`; props also reads `load_nfl_player_stats`. The oracle corpus is a single season, `tests/fixtures/nfl_prediction/` (fpi/results/pbp/player_stats/espn_predictor/espn_odds/espn_propbets/team_stats, **2023 only** — the plan's Phase-0 scope, `plan.md` Task 0.1).

## 3. Gotchas

- **`backtest.py`'s own docstring calls its floors "in-sample regression pins"** (`backtest.py:8`) — constants were fit AND gated on the same 2023 walk-forward, not a held-out season; treat the MAE/Brier floors below as regression guards, not out-of-sample validation.
- QBR has zero provenance (no card, no fitting script) — flag before trusting `qbr_model.ubj` for anything training-window-sensitive.
- The non-market boundary (① never reads `spread_line`/`vegas_wp`) is grep-gated in CI, not just documented (`plan.md` Task 4.2).

## 4. Oracle / gates

**Not in `data-sources.md` §4's oracle catalog at all** — that table covers CFB/MBB/NHL/NBA oracles but has no NFL row despite `tests/fixtures/nfl_prediction/` existing; a cataloging gap, not a missing oracle. Observed/floor pairs, all 2023, all "never lower" per the binding rule: ratings `spearman(adj_net, fpi) = 0.8904` (floor 0.85), `spearman(adj_off_epa, raw) = 0.9652` (floor 0.90) — `ratings-oracle.py`. Market: `mae(exp_margin, close_spread_home) = 2.961` (floor 3.5), `mae(exp_total, close_total) = 3.235` (floor 4.0), Brier tolerance 0.01 (mine 0.2318 vs ESPN 0.2294) — `backtest.py`. Props: MAE floors passing 75 / rushing 23 / receiving 23 yards; calibration ceiling 0.12 (observed 0.0954) — `backtest.py`.
