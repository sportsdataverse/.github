# NBA / WNBA

Harvested from the T3.3 prediction-market plan/design (`plan.md` = `ClaudeCowork/plans/2026-07-07-nba-prediction-market.md`; `design.md` = `.../specs/2026-07-07-nba-prediction-market-design.md`), the possession-engine design (`poss-design.md` = `ClaudeCowork/nba_data/specs/2026-06-29-nba-possession-engine-foundation-design.md`), and shipped `sdv-py` code/fixtures. RAPM/adj-RAPM/DARKO + possession methodology are already in `methods.md` — not repeated here.

## 1. Models

**Impact family** (`nba_rapm.py`/`nba_adj_rapm.py`/`nba_darko.py`) — mechanism lives in `methods.md`; module names only confirmed here.

**Prediction-market family** (T3.3, shipped): `nba/` core + `wnba/` shims (`league_id="10"`); G-League = `league_id="20"` on the same core, no new module (`design.md` §3.1, §8 D5):

- ① `nba_team_ratings.py` — opponent-adjusted net rating + pace, iterative KenPom-style fixed-point *(T7.2-shared w/ MBB/CFB)*. This **is** a ratings-family model — `methods.md` states CFB/NFL/MBB/WBB ratings are uncovered by the APM corpus; NBA/WNBA is the one league here with real ratings mechanism (`design.md` §3.3).
- ②③ `nba_game_predict.py` — `exp_margin=(adj_net_home−adj_net_away)·exp_poss/100+HFA`, `home_win_prob=Φ(exp_margin/σ)`, `exp_total` from pace × blended off/def (`design.md` §3.4).
- ④ same module, `nba_in_game_win_prob` — logistic/xgboost on `[score_diff, sqrt(sec_left), pregame_logit, home_has_ball]`, bundled per league as `.ubj` (`nba/models/nba_in_game_wp.ubj`, `wnba/models/wnba_in_game_wp.ubj`) — plan specified one JSON keyed by `league_id`; shipped code escalated to xgboost `.ubj` per league instead (`plan.md` Task 3.2's fallback clause).
- ⑤ `nba_clutch.py` — clutch-delta vs full-game AdjNet, empirical-Bayes shrinkage toward zero, gated **out-of-sample only** (in-sample is circular — the clutch endpoint *is* the fit data) (`design.md` §3.6, §8 D7).
- ⑥ `nba_player_props.py` — rate × projected poss → NegBin(counts)/Normal(pts) → `P(over)`.
- **Not carried:** EP/WP/CP/xYAC (football-only), xG (hockey/soccer-only), simulation (bracketology is an explicit T3.3 non-goal, `design.md` §1).

## 2. Data

Impact family bypasses ESPN loaders for stats.nba.com (`data-sources.md` §2) — prediction-market ① mirrors that split: the model reads ESPN `load_nba_schedule`/`load_nba_team_boxscore` (id `Int64`), but its *oracle* is stats.nba.com `leaguedashteamstats`/`leaguedashteamclutch` (10-digit franchise id) crosswalked to ESPN by **team name**, not id — the two id spaces don't overlap (`nba_prediction/README.md` = `sdv-py/tests/fixtures/nba_prediction/README.md`). ④'s planned concurrent oracle `winprobabilitypbp` is a **dead endpoint** (HTTP 500 on every well-formed request; hoopR's own wrapper is `deprecate_stop()`-ed) — fixture ships zero-row, gate (b) dropped, only gate (a) calibration remains (`nba_prediction/README.md`; `tests/nba/test_nba_in_game_wp.py:3-6,120-124`).

## 3. Gotchas

- v3 pbp sort key `period asc → sec_remaining desc → action_number asc → payload_position asc` has **no event-type tiebreak — adding one was tried and disproved** pbpstats agreement (`nba_enhanced_pbp.py:178-190`).
- Box-derived possessions are the **default** for team ratings; the event-level `nba_possessions` engine is the escalation only if the oracle MAE floor fails, not the baseline (`design.md` §3.3, "escalate to the event engine only if the oracle floor fails").
- **WNBA pre-2005 team-log repair** — not in sdv-py; lives in the `wehoop-wnba-stats-data` producer that consumes this engine, `_repair_team_logs` (`wehoop-dev/wehoop-wnba-stats-data/python/wnba_model_publish/builders.py:262-296`): early team logs are corrupt (`min`=8.0/2000, 0.9/2002, string/1997+2003; `tov`≈0 pre-2001) while **player** logs are pristine every era — `min` is unconditionally replaced by the player-sum (not maxed, the column is simply wrong whenever it's wrong), `tov := max(team_col, player-sum)` because team TOV legitimately includes team-attributed turnovers (shot-clock/8-second) player rows lack, so the sane column is never smaller than the player sum.
- `failure-modes.md` #12 (`group_by` w/o `maintain_order`, `nba_player_identity`) lives in this same tree — cross-referenced, not re-derived.
- Clutch cross-season Spearman ≈0.10 sitting **inside** the null band is the *correct* gate outcome, not a weak result — the gate accepts `rho>0` OR `|rho|<0.1`, and the model keeps heavy shrinkage rather than inventing a signal (`nba_clutch.py:24-27`; `test_nba_clutch.py:108-111`).

## 4. Oracle

Six-fixture NBA RAPM/EPM/DARKO/LEBRON oracle + its placeholder-row honesty note is covered in `data-sources.md` §4. Prediction-market has its own fixture family, `tests/fixtures/nba_prediction/` (captured 2026-07-08, season 2024 + prior 2023 for the clutch gate) — WNBA fixtures fold into that same directory (`wnba_results_2024.parquet` etc.); **no separate `wnba_prediction/` exists**. Observed floor `spearman(adj_net_rtg, NET_RATING) >= 0.95` (`test_nba_team_ratings_oracle.py:48`) is tighter than `design.md`'s 0.90 target, per the never-lower rule (`metrics-and-gates.md` §2).
