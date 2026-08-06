# Data sources — what feeds this model?

Distilled from a season-coverage audit (a 32 KB training-data audit + a 15 KB
publication plan, both prose) and its two machine-readable companions (a
155-entry loader inventory + a per-dataset season-coverage JSON), plus source
code read directly where those four documents turned out not to cover a
question the brief asked for (the CFB recruiting-family floors, the oracle
column contracts). Every rule below cites the file it came from — an
uncited claim in this file should be treated as invented.

Shorthand used in citations:

| Shorthand | Full path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `audit.md` | `sdv-py/dev/model-training-data-audit-2026-07-28.md` |
| `pub-plan.md` | `ClaudeCowork/notes/2026-07-12-model-dataset-publication-plan.md` |
| `loader_map.json` | `ClaudeCowork/notes/2026-07-11-release-dataset-season-audit/out/loader_map.json` (155 entries) |
| `release_coverage.json` | `ClaudeCowork/notes/2026-07-11-release-dataset-season-audit/out/release_coverage.json` (`releases` + `trees` top-level keys) |
| `recruiting.py` | `cfbfastR-cfb-data/python/cfb_data_build/recruiting.py` |
| `scrape_cfb_recruits.py` | `cfbfastR-cfb-raw/python/scrape_cfb_recruits.py` |
| `cfb_prediction/README.md` | `sdv-py/tests/fixtures/cfb_prediction/README.md` |
| `mbb_prediction/README.md` | `sdv-py/tests/fixtures/mbb_prediction/README.md` |
| `nhl_player_impact/README.md` | `sdv-py/tests/fixtures/nhl_player_impact/README.md` |
| `nba_oracle/README.md` | `sdv-py/tests/fixtures/nba_oracle/README.md` |

---

## 1. Season-coverage floors — two different axes, don't conflate them

**A model trained across a floor silently trains on absent data — no error,
just a wrong model.** This corpus actually documents two distinct floors that
answer two different questions, and treating them as one is itself a bug
class:

- **Dataset floor** (`loader_map.json`'s `floor` field): the earliest season
  a `load_*` call returns *any* rows. Two behaviors coexist **inside the same
  loader**, keyed on how far below the documented floor the caller asks:
  `load_cfb_betting` and `load_cfb_fpi_weekly` both raise `SeasonNotFoundError`
  outright for a season below their hard floor (2004 / 2005 respectively —
  `sportsdataverse/cfb/cfb_loaders.py:1553-1566` raises at `:1555-1556`,
  `:1647-1650` raises at `:1649-1650`), but for an individual missing asset
  *at or above* that floor the same function degrades gracefully instead —
  `_read_release_parquet` returns `None`, the season is added to a `missing`
  list, and `cli_warn()` fires (`cfb_loaders.py:1557-1565`). Either way this
  floor is at least observable if you're watching for it.
- **Model-training window** (`audit.md`): what season range a *specific
  shipped artifact* was actually fit on — which is frequently narrower than
  the dataset floor above, and that gap is the genuinely silent failure mode.
  Example: WNBA ESPN pbp is published 2002–2026 (`loader_map.json`:
  `load_wnba_pbp` floor 2002) but `wnba_in_game_wp.ubj` was trained on **one**
  season out of those 25, with the exact season "not recorded anywhere"
  (`audit.md` §WNBA). Nothing about calling `load_wnba_pbp([2010])` today
  tells you the deployed model never saw 2010.

### 1a. Interior gaps — a floor is necessary, not sufficient

`release_coverage.json`'s `interior_gaps` field catches missing seasons
*inside* the covered range, which a single min/max floor check will not
surface:

| Dataset | Covered range | `interior_gaps` |
|---|---|---|
| `espn_cfb_pbp` | 2004–2024 | `[2011, 2020, 2023]` |
| `espn_cfb_model_pbp` | 2004–2024 (only 5 of 21 possible assets) | `[2005..2023]` minus the 5 published |
| `espn_mens_college_basketball_pbp` | 2003–2026 | `[2004, 2005]` |
| `espn_womens_college_basketball_player_boxscores` / `_team_boxscores` | 2004–2026 | `[2005]` |
| `fastRhockey-data` `phf/pbp/parquet` | 2016–2023 | `[2017, 2018, 2019]` |

(`release_coverage.json`, `trees`/`releases` → per-dataset `interior_gaps`
arrays.) A `season >= floor` check alone would silently include these
missing years as an *absence* the caller never sees — the loader returns
whatever seasons exist and moves on with no count assertion.

### 1b. CFB recruiting family (recruits 2002; team_talent / returning_production 2005)

**Not present in `release_coverage.json` at all** — grepping both its
`releases` and `trees` sections for `recruit`, `talent`, and `return`
returns zero matches. These three datasets are new enough (the
`cfbfastR-cfb-data` recruiting producer) that the 2026-07-11 coverage audit
predates them; their floors have to be derived from the producer source
directly:

- **`cfb_recruits` floor = 2002.** The raw 247 scrape's own floor is
  `FIRST_CLASS_YEAR = 2000` (`scrape_cfb_recruits.py:55`), but the earliest
  *complete* manifest on disk is class year 2002
  (`cfbfastR-cfb-raw/cfb/recruits/json/2002/_manifest.json` present; 2000/2001
  absent) — `available_years()` only offers years with a checked-complete
  manifest (`recruiting.py:66-87`), so 2002 is the practical floor even
  though the scraper would in principle accept 2000.
- **`cfb_team_talent` floor = 2005.** Talent for season *S* is a composite
  over classes *S-3..S* (`TALENT_WINDOW = 4`, `recruiting.py:183`) — a
  season needs its full 4-class window present in the raw store, so the
  earliest season with a complete window given a 2002 raw floor is
  `2002 + 3 = 2005`. `recruiting.py:230-245` enforces this at build time,
  raising `FileNotFoundError` rather than publishing a season with a
  silently-thinner composite. (The same file's inline comment flags the
  earlier bug this fixed: applying the 4-class window requirement to
  `cfb_recruits` too made 2002-2004 recruit-class *pulls* fail on classes
  that predate the floor and "were never going to exist" — `recruits` was
  fixed to need only its own single class, `recruiting.py:229-234`.)
- **`cfb_returning_production` floor = 2005.** This dataset is built from
  ESPN's player box for season *S-1* plus the season-*S* roster
  (`recruiting.py:167-174` — "Not built from the recruit store at all... it
  lives here because it is the same roster-continuity family"), not from
  the 247 recruit store. CFB's empirical ESPN pbp/box usable floor is 2004
  (missing-game cliff: 771 games missing pbp in 2002, 287 in 2003, 261 in
  2004, then single digits by 2011 — `audit.md` §CFB "Why the 2004 floor").
  A season-*S* returning-production row needs season *S-1*'s box, so the
  earliest usable target season is `2004 + 1 = 2005`.

### 1c. Model-training-window floors by league (from `audit.md`)

This is the *narrower* axis from §1 above — what a shipped artifact was
actually fit on, independent of what the underlying dataset now covers:

| League | Regime | Floor / window | Note |
|---|---|---|---|
| CFB | full-history + era one-hots | 2004–2025 (all 12 `sportsdataverse/cfb/models/*` artifacts) | no season-floor constant in code — `--seasons=None` defaults to everything on disk; **as of the 0.0.75 retrain (2026-08-02), all 7 `.card.json` cards read `training_seasons: [2004, 2025]`, `trained_date: "2026-08-02"` — no longer prose-only provenance. See `sports/cfb.md` §1 for the supersession note and the two boosters (`fd_model.ubj`/`cfb_cp_model.ubj`) that still ship with no card at all.** |
| NFL | full-history + era one-hots | 1999–2025 | departs from upstream nflfastR/nfl4th narrower windows on purpose; `qbr_model.ubj`'s training window is **unknown, no script found anywhere** |
| NHL xG (`xg_model_5v5`/`_st`) | full-history + era one-hots | 2009-10–2025-26 (partial) | coordinate floor ~2007-08; a stale R docstring still says "2010–2024" |
| MBB/WBB in-game WP | oracle-season fit | 2023 only | leakage separation from the 2024 gate season; could train 2006–2026 (MBB) / 2008–2026 (WBB) today |
| NBA impact family (RAPM→adj-RAPM→SPM→BPM→WAR→DARKO) | full league history | 1997–2026 (30 seasons) | run complete but **unpublished** — `load_nba_player_impact` points at a release tag that does not exist yet |
| WNBA draft/aging/availability | full league history | 1997–2025 (29 classes) | contrasts with WNBA in-game WP's 1-of-25-seasons fit above — same league, two very different regimes |
| PWHL (everything) | ceiling-bound | 2024–2026 (3 seasons total) | every window here is a ceiling, not a choice — the league has only played 3 seasons |
| MLB Stuff+/Command+ | ceiling-bound but under-used | 2023 only, ~30 pitchers, vs Statcast 2015+ available | disclosed corpus-size deviation from the original 2021-2023 full-league plan |

(`audit.md` "Cross-league synthesis" §"The four window-setting regimes" and
per-league sections — table above condenses the full per-league detail;
read the source for row counts, era-cut rationale, and the 10-item ranked
provenance-gap list.)

---

## 2. Dataset → loader → feature family map

The full `load_*` inventory (155 entries) grouped by league, from
`loader_map.json`. `host` is `sdv-release` (GitHub Release asset, keyed by
`release_tag`), `sdv-git-tree` (raw parquet on a repo's default branch,
keyed by `git_tree_path`), or an upstream mirror (`nflverse`/`ffverse`, keyed
by a `config.py` URL constant). `floor` is `null` where the source script
didn't resolve one (mostly `nflverse`/`ffverse` mirrors with no per-season
partitioning to probe).

### CFB (6 loaders)

| Loader | Host | Floor | Source |
|---|---|---|---|
| `load_cfb_pbp` | sdv-git-tree | 2003 | `cfbfastR-data/main/pbp/parquet/play_by_play_{season}.parquet` |
| `load_cfb_rosters` | sdv-git-tree | 2003 | `cfbfastR-data/main/rosters/parquet/cfb_rosters_{season}.parquet` |
| `load_cfb_schedule` | sdv-git-tree | 2003 | `cfbfastR-data/main/schedules/parquet/cfb_schedules_{season}.parquet` |
| `load_cfb_team_info` | sdv-git-tree | 2003 | `cfbfastR-data/main/team_info/parquet/cfb_team_info_{season}.parquet` |
| `load_cfb_teams_crosswalk` | sdv-release | 2014 | `cfb_crosswalk` |
| `load_cfb_schedule_crosswalk` | sdv-release | 2014 | `cfb_crosswalk` |

Feeds: the ratings/EP/WP/QBR/decision-model family reads `load_cfb_pbp`
directly (CFB models train on the full 2004–2025 corpus per §1c, not this
loader's nominal 2003 floor — the models' own ingest additionally filters
missing-pbp seasons per `audit.md`). `cfb_recruits`/`cfb_team_talent`/
`cfb_returning_production` (§1b) are **not yet in this loader inventory** —
they're published by the newer `cfbfastR-cfb-data` recruiting producer and
have no `load_cfb_*` counterpart captured by this JSON.

### MBB (11 loaders) — all `sdv-release`, `espn_mens_college_basketball_*` tags

| Loader | Floor | | Loader | Floor |
|---|---|---|---|---|
| `load_mbb_pbp` | 2002 | | `load_mbb_schedule` | 2002 |
| `load_mbb_player_boxscore` | 2002 | | `load_mbb_team_boxscore` | 2002 |
| `load_mbb_standings` | 2003 | | `load_mbb_team_season_stats` | 2003 |
| `load_mbb_game_rosters` | 2025 | | `load_mbb_officials` | 2025 |
| `load_mbb_player_season_stats` | 2025 | | `load_mbb_rosters` | 2025 |
| `load_mbb_shots` | 2025 | | | |

Feeds: T1.0 prediction stack (pregame/in-game WP, ratings) reads
`load_mbb_schedule` + `load_mbb_pbp`; T1.1/T1.2 player-value spine additionally
needs `load_mbb_player_boxscore`/`load_mbb_shots`, which floor at 2025 —
a hard structural ceiling for that spine, not a choice (`audit.md` §MBB/WBB).
WBB uses the same 11 loader names against `espn_womens_college_basketball_*`
tags but is not a 1:1 floor mirror: `load_wbb_pbp`/`_player_boxscore`/
`_team_boxscore`/`_schedule` floor 2002, matching MBB — but
`load_wbb_standings`/`_team_season_stats` floor at **2026**, where MBB's
equivalents floor at 2003, and `load_wbb_game_rosters`/`_officials`/
`_player_season_stats`/`_rosters`/`_shots` floor at 2026 versus MBB's 2025
(`loader_map.json`).

### MLB (5 loaders — all stubs)

`load_mlb_pbp`, `load_mlb_player_boxscore`, `load_mlb_rosters`,
`load_mlb_schedule`, `load_mlb_team_boxscore` all resolve to `host=null`,
`floor=null` in `loader_map.json` — **MLB has zero release datasets; every
`load_mlb_*` is a `NotImplementedError` stub** (`audit.md` §MLB: "MLB has
zero release datasets... every model self-collects from the wire"). Model
inputs for Stuff+/Command+/RE24/etc. come from live `mlb_statcast_*`
wrappers, not a `load_*` loader.

### NBA (13 loaders) — all `sdv-release`

| Loader | Floor | Tag |
|---|---|---|
| `load_nba_pbp` / `_shots` / `_officials` / `_game_rosters` / `_player_boxscore` / `_player_season_stats` / `_schedule` / `_standings` / `_team_boxscore` / `_team_season_stats` | 2002 | `espn_nba_*` |
| `load_nba_draft` | 2003 | `espn_nba_draft` |
| `load_nba_rosters` | 2025 | `espn_nba_rosters` (current-roster only, not historical) |
| `load_nba_stats_schedules` | 2025 | `nba_stats_schedules` (stats.nba.com, distinct floor from the ESPN family) |

Feeds: the NBA impact family (§1c) does **not** read any of these — RAPM/
adj-RAPM/SPM/WAR/DARKO/BPM all go through `compile_nba_season` /
`nba_possessions.py`, which requires live stats.nba.com access with no ESPN
fallback (`pub-plan.md` "CORRECTION (verified in code 2026-07-12): the ENTIRE
NBA model surface is stats.nba.com-sourced, not just tracking"). ESPN `pbp`/
`shots` here feed the sdv-engine ESPN-sim path instead (`audit.md` §NBA data
span table).

### NFL (35 loaders — the most heterogeneous host mix)

| Loader | Host | Floor | Source |
|---|---|---|---|
| `load_nfl_combine` | nflverse | – | `config.NFL_COMBINE_URL` |
| `load_nfl_contracts` | nflverse | – | `config.NFL_CONTRACTS_URL` |
| `load_nfl_depth_charts` | nflverse | – | `depth_charts` |
| `load_nfl_draft_picks` | nflverse | – | `config.NFL_DRAFT_PICKS_URL` |
| `load_nfl_espn_qbr` | sdv-release | – | `nfl_espn_qbr` |
| `load_nfl_ff_opportunity` | ffverse | – | `config.NFL_FF_OPPORTUNITY_URL` |
| `load_nfl_ff_playerids` | sdv-git-tree | – | `config.NFL_FF_PLAYERIDS_URL` |
| `load_nfl_ff_rankings` | sdv-git-tree | – | `config.NFL_FF_RANKINGS_DRAFT_URL` |
| `load_nfl_ftn_charting` | nflverse | – | `ftn_charting` |
| `load_nfl_injuries` | nflverse | – | `injuries` |
| `load_nfl_nextgen_stats` | – | – | dispatches per-type at call time (unified loader) |
| `load_nfl_ngs_passing` | nflverse | – | `config.NFL_NGS_PASSING_URL` |
| `load_nfl_ngs_receiving` | nflverse | – | `config.NFL_NGS_RECEIVING_URL` |
| `load_nfl_ngs_rushing` | nflverse | – | `config.NFL_NGS_RUSHING_URL` |
| `load_nfl_officials` | nflverse | – | `config.NFL_OFFICIALS_URL` |
| `load_nfl_pbp` | sdv-release | – | `nfl_model_pbp` (1999–2025 per `audit.md`; `floor=null` in this JSON) |
| `load_nfl_pbp_participation` | nflverse | – | `pbp_participation` |
| `load_nfl_pfr_advstats` | – | – | dispatches per-type/summary at call time (unified loader) |
| `load_nfl_pfr_def` | nflverse | – | `config.NFL_PFR_SEASON_DEF_URL` |
| `load_nfl_pfr_pass` | nflverse | – | `config.NFL_PFR_SEASON_PASS_URL` |
| `load_nfl_pfr_rec` | nflverse | – | `config.NFL_PFR_SEASON_REC_URL` |
| `load_nfl_pfr_rush` | nflverse | – | `config.NFL_PFR_SEASON_RUSH_URL` |
| `load_nfl_pfr_weekly_def` | – | – | – |
| `load_nfl_pfr_weekly_pass` | – | – | – |
| `load_nfl_pfr_weekly_rec` | – | – | – |
| `load_nfl_pfr_weekly_rush` | – | – | – |
| `load_nfl_player_stats` | sdv-release | – | `nfl_player_stats` |
| `load_nfl_players` | sdv-release | – | `nfl_players` |
| `load_nfl_rosters` | sdv-release | – | `nfl_rosters` |
| `load_nfl_schedule` | nflverse | – | `config.NFL_TEAM_SCHEDULE_URL` |
| `load_nfl_snap_counts` | nflverse | – | `snap_counts` |
| `load_nfl_team_stats` | sdv-release | – | `nfl_team_stats` |
| `load_nfl_teams` | nflverse | – | `config.NFL_TEAM_LOGO_URL` |
| `load_nfl_trades` | nflverse | – | `config.NFL_TRADES_URL` |
| `load_nfl_weekly_rosters` | nflverse | – | `weekly_rosters` |

Every loader in this league shows `floor=null` in `loader_map.json` — none
of NFL's sources are partitioned in a way the audit script could probe a
per-season floor from (`nflverse`/`ffverse` mirrors ship one combined file;
the `sdv-release` subset's real span is documented separately in `audit.md`'s
model-training table, e.g. `nfl_model_pbp` 1999–2025). `load_nfl_nextgen_stats`
and `load_nfl_pfr_advstats` are the two unified loaders (see the sdv-py
`CLAUDE.md` "don't add new per-type wrappers" rule) — they show `host=null`
because they dispatch to per-type URLs at call time rather than owning one
fixed path.

### NHL (28 loaders) + PWHL (21 loaders) — same shape, `nhl_*`/`pwhl_*` tags

| Loader | Host | Floor | Source |
|---|---|---|---|
| `load_nhl_game_info` | sdv-release | 2024 | `nhl_game_info` |
| `load_nhl_game_rosters` | sdv-release | 2024 | `nhl_game_rosters` |
| `load_nhl_games` | sdv-release | – | `nhl_schedules` |
| `load_nhl_goalie_box` | – | – | – (dispatch shim over `load_nhl_goalie_boxscores`) |
| `load_nhl_goalie_boxscores` | sdv-release | 2024 | `nhl_goalie_boxscores` |
| `load_nhl_linescore` | sdv-release | 2024 | `nhl_linescore` |
| `load_nhl_officials` | sdv-release | 2025 | `nhl_officials` |
| `load_nhl_pbp` | sdv-release | 2010 | `nhl_pbp_full` |
| `load_nhl_pbp_full` | sdv-release | 2010 | `nhl_pbp_full` |
| `load_nhl_pbp_lite` | sdv-release | 2010 | `nhl_pbp_lite` |
| `load_nhl_penalties` | sdv-release | 2024 | `nhl_penalties` |
| `load_nhl_player_box` | – | – | – (dispatch shim over `load_nhl_player_boxscores`) |
| `load_nhl_player_boxscore` | sdv-release | 2010 | `nhl_player_boxscores` |
| `load_nhl_player_boxscores` | sdv-release | 2010 | `nhl_player_boxscores` |
| `load_nhl_rosters` | sdv-release | 2010 | `nhl_rosters` |
| `load_nhl_schedule` | sdv-release | 2010 | `nhl_schedules` |
| `load_nhl_schedules` | sdv-release | 2010 | `nhl_schedules` |
| `load_nhl_scoring` | sdv-release | 2024 | `nhl_scoring` |
| `load_nhl_scratches` | sdv-release | 2024 | `nhl_scratches` |
| `load_nhl_shifts` | sdv-release | 2025 | `nhl_shifts` |
| `load_nhl_shootout` | sdv-release | 2025 | `nhl_shootout` |
| `load_nhl_shots_by_period` | sdv-release | 2025 | `nhl_shots_by_period` |
| `load_nhl_skater_box` | – | – | – (dispatch shim over `load_nhl_skater_boxscores`) |
| `load_nhl_skater_boxscores` | sdv-release | 2024 | `nhl_skater_boxscores` |
| `load_nhl_team_box` | – | – | – (dispatch shim over `load_nhl_team_boxscores`) |
| `load_nhl_team_boxscore` | sdv-release | 2010 | `nhl_team_boxscores` |
| `load_nhl_team_boxscores` | sdv-release | 2010 | `nhl_team_boxscores` |
| `load_nhl_three_stars` | sdv-release | 2024 | `nhl_three_stars` |

NHL floors group into three bands: pbp/box/rosters/schedule at **2010**,
the per-game detail family (`game_info`, `linescore`, `penalties`, `scoring`,
`scratches`, `skater_boxscores`, `three_stars`) at **2024**, and `shifts`/
`shootout`/`shots_by_period`/`officials` at **2025**.

| Loader | Host | Floor | Source |
|---|---|---|---|
| `load_pwhl_game_info` | sdv-release | 2024 | `pwhl_game_info` |
| `load_pwhl_game_rosters` | sdv-release | 2024 | `pwhl_game_rosters` |
| `load_pwhl_games` | sdv-release | – | `pwhl_schedules` |
| `load_pwhl_goalie_box` | – | – | – |
| `load_pwhl_goalie_boxscores` | sdv-release | 2024 | `pwhl_goalie_boxscores` |
| `load_pwhl_officials` | sdv-release | 2024 | `pwhl_officials` |
| `load_pwhl_pbp` | sdv-release | 2024 | `pwhl_pbp` |
| `load_pwhl_penalty_summary` | sdv-release | 2024 | `pwhl_penalty_summary` |
| `load_pwhl_player_box` | – | – | – |
| `load_pwhl_player_boxscores` | sdv-release | 2024 | `pwhl_player_boxscores` |
| `load_pwhl_rosters` | sdv-release | 2024 | `pwhl_rosters` |
| `load_pwhl_schedule` | – | – | – |
| `load_pwhl_schedules` | sdv-release | 2024 | `pwhl_schedules` |
| `load_pwhl_scoring_summary` | sdv-release | 2024 | `pwhl_scoring_summary` |
| `load_pwhl_shootout` | sdv-release | 2026 | `pwhl_shootout` |
| `load_pwhl_shots_by_period` | sdv-release | 2024 | `pwhl_shots_by_period` |
| `load_pwhl_skater_box` | – | – | – |
| `load_pwhl_skater_boxscores` | sdv-release | 2024 | `pwhl_skater_boxscores` |
| `load_pwhl_team_box` | – | – | – |
| `load_pwhl_team_boxscores` | sdv-release | 2024 | `pwhl_team_boxscores` |
| `load_pwhl_three_stars` | sdv-release | 2024 | `pwhl_three_stars` |

PWHL mirrors NHL's shape (same `*_box` dispatch-shim pattern) but every
floor is 2024 except `shootout` (2026) — **the whole league is only 3
seasons old**, so these floors are the same ceiling `audit.md` §PWHL
documents, not an independent finding.

### WNBA (25 loaders — the widest single-league set, two source families)

| Loader | Host | Floor | Source |
|---|---|---|---|
| `load_wnba_draft` | sdv-release | 2026 | `espn_wnba_draft` |
| `load_wnba_game_rosters` | sdv-release | 2024 | `espn_wnba_game_rosters` |
| `load_wnba_officials` | sdv-release | 2024 | `espn_wnba_officials` |
| `load_wnba_pbp` | sdv-release | 2002 | `espn_wnba_pbp` |
| `load_wnba_player_boxscore` | sdv-release | 2002 | `espn_wnba_player_boxscores` |
| `load_wnba_player_season_stats` | sdv-release | 2024 | `espn_wnba_player_season_stats` |
| `load_wnba_rosters` | sdv-release | 2024 | `espn_wnba_rosters` |
| `load_wnba_schedule` | sdv-release | 2002 | `espn_wnba_schedules` |
| `load_wnba_shots` | sdv-release | 2024 | `espn_wnba_shots` |
| `load_wnba_standings` | sdv-release | 2024 | `espn_wnba_standings` |
| `load_wnba_team_boxscore` | sdv-release | 2002 | `espn_wnba_team_boxscores` |
| `load_wnba_team_season_stats` | sdv-release | 2024 | `espn_wnba_team_season_stats` |
| `load_wnba_stats_coaches` | sdv-release | 2026 | `wnba_stats_coaches` |
| `load_wnba_stats_draft` | sdv-release | 2025 | `wnba_stats_draft` |
| `load_wnba_stats_game_rosters` | sdv-release | 2026 | `wnba_stats_game_rosters` |
| `load_wnba_stats_lineups` | sdv-release | 2026 | `wnba_stats_lineups` |
| `load_wnba_stats_officials` | sdv-release | 2026 | `wnba_stats_officials` |
| `load_wnba_stats_pbp` | sdv-release | 2026 | `wnba_stats_pbp` |
| `load_wnba_stats_player_game_logs` | sdv-release | 2025 | `wnba_stats_player_game_logs` |
| `load_wnba_stats_player_season_stats` | sdv-release | 2026 | `wnba_stats_player_season_stats` |
| `load_wnba_stats_rosters` | sdv-release | 2026 | `wnba_stats_rosters` |
| `load_wnba_stats_schedules` | sdv-release | 2025 | `wnba_stats_schedules` |
| `load_wnba_stats_shots` | sdv-release | 2026 | `wnba_stats_shots` |
| `load_wnba_stats_standings` | sdv-release | 2026 | `wnba_stats_standings` |
| `load_wnba_stats_team_season_stats` | sdv-release | 2026 | `wnba_stats_team_season_stats` |

Two source families, radically different depth: `espn_wnba_*` (ESPN) goes
back to 2002 for pbp/schedule/boxscores; `wnba_stats_*` (stats.wnba.com)
floors at 2025 or 2026 across the board. This mirrors `audit.md`'s WNBA
§finding that the ESPN pbp family spans 25 seasons (2002–2026) while the
possession-sim glue is locked to stats.wnba.com's single 2026 season.

---

## 3. Raw-store and validation env vars

Not a release loader at all — a read-through cache for per-endpoint JSON
payloads (mostly stats.nba.com/stats.wnba.com, which hang rather than error
on cloud IPs) plus the offline oracle/validation directories:

| Env var | Effect | Source |
|---|---|---|
| `SDV_PY_NBA_RAW_JSON_DIR` | Generic raw-JSON-store root for NBA stats.nba.com fetches; per-endpoint override is `SDV_PY_NBA_RAW_JSON_DIR_{ENDPOINT}` (e.g. `_PLAYBYPLAYV3`) | `sportsdataverse/nba/nba_possessions.py` |
| `SDV_PY_NBA_RAW_JSON_READONLY` | `1` disables writes to the store (read-only replay) | `sportsdataverse/nba/nba_possessions.py` |
| `SDV_PY_NBA_RAW_JSON_HTTP_TIMEOUT` | Per-request timeout override for the store's live fallback | `sportsdataverse/nba/nba_possessions.py` |
| `SDV_PY_WNBA_RAW_JSON_DIR` / `SDV_PY_WNBA_RAW_JSON_READONLY` | Same pattern, WNBA (`nba_season_compile`-equivalent path) | `sportsdataverse/wnba/wnba_engine.py` |
| `SDV_PY_NBA_ORACLE_DIR` | Points the gated real-CSV NBA oracle smoke tests at the full (non-3-row-sample) RAPM/EPM/DARKO/LEBRON CSVs | `sportsdataverse/nba/nba_oracle_data.py`; `nba_oracle/README.md` |
| `SDV_PBPSTATS_ROOT` | Gates the `pbpstats`-live start-type oracle test for `nba_play_context` | `tests/nba/test_nba_play_context_oracle.py` |
| `SDV_VALIDATION_DATA_ROOT` / `SDV_VALIDATION_NFL_DATA_ROOT` | Root(s) the validation-harness CLI reads real release data from | `tools/validation/oracles.py`, `tools/validation/registry.py` |

None of these are release-dataset loaders — they gate *offline replay* of
otherwise-live or paywalled sources. `SDV_PY_NBA_RAW_JSON_DIR`/
`SDV_PY_WNBA_RAW_JSON_DIR` are the mechanism that makes the entire NBA/WNBA
model surface (§2's NBA table above) reproducible without hitting
stats.nba.com/stats.wnba.com per run.

---

## 4. Oracle catalog

External validation corpora, keyed by where the *committed test fixture*
lives (not the live URL — re-derive from the fixture's README when
refreshing). **ID dtype is NOT universal across this table — verify per
row before joining.** The ESPN-derived basketball/football fixtures (Torvik,
Torvik BPM, ESPN FPI/BPI/predictor/odds) are `Utf8`, cast from the raw ESPN
integer, so they join against `load_*` output without a cast. The NHL
MoneyPuck/EvolvingHockey fixtures do **not** follow that convention:
`mp_gsax.parquet`'s `player_id`, `mp_shots_sample.parquet`'s `game_id`/
`shooter_id`, and `eh_skaters.parquet`'s `player_id` are all `Int64`
(verified via `polars.read_parquet(...).schema`), and
`moneypuck_teams_2023.parquet` has **no id column at all** — it's keyed on
`team` (a name string), same as `eh_skaters.parquet`'s name-based crosswalk.
Joining an `Int64` MoneyPuck id straight into a `Utf8` loader column is
exactly the silent-zero-match id-dtype bug class the ecosystem's `CLAUDE.md`
warns about — cast one side first and assert the join actually matched rows.

| Oracle | Fixture path | Columns (verified) | Coverage | Use |
|---|---|---|---|---|
| Torvik/Barttorvik (CFB-analog ratings) | `tests/fixtures/mbb_prediction/torvik_2024.parquet` | `team_id, team, adj_o, adj_d, adj_em, adj_tempo, rank` (`adj_tempo` is null — source CSV has no tempo column) | 2024 only, 350 teams | Phase-1 ratings gate, Spearman(`adj_em`) ≥0.95 (observed 0.990) — `mbb_prediction/README.md` |
| Torvik BPM (player-value) | `tests/fixtures/mbb_player_value/barttorvik_bpm_{2025,2026}.parquet` | `player_id, player, team, team_id, season, bpm, obpm, dbpm, gp, min_per, role` (`player_id`/`team_id` are `Utf8`; `bpm == obpm+dbpm` by construction) | 2025, 2026 | primary player-BPM oracle, ~97.3% name-matched to `team_id` (`mbb_player_value/README.md:33` — 4,922/5,059) |
| KenPom | **not captured — paywalled, no flat endpoint.** Referenced only as a methodology descriptor in docstrings | — | — | `sportsdataverse/mbb/mbb_ncaa_strength.py:1,16,621`, `sportsdataverse/cfb/cfb_opponent_adjust.py:297` ("KenPom-style fixed-point solver"); Torvik/GameOnPaper substitute as the free-tier oracle |
| ESPN FPI (CFB's BPI-equivalent) | `tests/fixtures/cfb_prediction/fpi_2023.parquet` + `fpi_resume_2023.parquet` | `team_id, team, fpi, fpi_rank`; resume adds `fpi_sos_rank, fpi_sor_rank, fpi_gc_rank` | 2023 only, 133 teams | corresponds to the `load_cfb_fpi_weekly` release loader (floor 2005, §1) |
| ESPN BPI (MBB/WBB) | `tests/fixtures/mbb_prediction/espn_bpi_2024.parquet` | `team_id, team, bpi, bpi_rank, bpi_offense, bpi_defense, sos, sos_rank, sor, sor_rank, wins, losses` | 2024 only, 362 teams | Phase-4 SoS Spearman gate |
| ESPN predictor (win-prob) — **schema differs per league, do not assume one contract** | `tests/fixtures/{cfb,mbb,nhl}_prediction/espn_predictor_sample.parquet` | CFB (5 cols): `game_id, home_team_id, away_team_id, home_win_prob, predicted_margin`. MBB (**4** cols, no `predicted_margin`): `game_id, home_team_id, away_team_id, home_win_prob` — `home_win_prob` here is ESPN's own `gameProjection`/100, the same derivation CFB already ships as a column, not an addition. NHL (**team-name keyed, not `_team_id`**): `game_id, home_team, away_team, home_win_prob` | per-league sample, one season | Win-prob Brier gate vs ESPN BPI/predictor |
| Market closing lines — **schema differs per league** | `tests/fixtures/{cfb,mbb,nhl}_prediction/espn_odds_sample.parquet`, CFB also `market_odds_2024.parquet` | CFB/MBB: `game_id, close_spread_home, close_total` (home spread, negative = home favored). NHL: `game_id, close_puck_line_home, close_total` — a puck line, not a point spread | per-league sample | Spread/total MAE gate; CFB corr(`predicted_margin`, `-close_spread_home`) = −0.95 |
| MoneyPuck (NHL team xG) | `tests/fixtures/nhl_prediction/moneypuck_teams_2023.parquet` | `team, xgf, xga, xg_diff, gf, ga` | 2023, 32 teams | team-level xG concurrent-validity |
| MoneyPuck (NHL goalie GSAx) | `tests/fixtures/nhl_player_impact/mp_gsax.parquet` | `player_id, goalie, gsax` (`gsax = xGoals - goals`) | 2024-25 regular season, 103 goalies | Spearman vs internal GSAx, floor 0.65 (`nhl_player_impact/README.md`) |
| MoneyPuck (per-shot xG) | `tests/fixtures/nhl_player_impact/mp_shots_sample.parquet` | `game_id, period, shooter_id, game_seconds, mp_xgoal, mp_goal` | 3 games, 266 shots | NHL-booster-vs-MoneyPuck agreement gate (corr 0.66, 97% match) |
| EvolvingHockey RAPM/WAR (secondary NHL oracle) | `tests/fixtures/nhl_player_impact/eh_skaters.parquet` | `player_id, player, xg_rapm, war` (name-keyed crosswalk, not a real id join) | 2024-25, 72 skaters | needs `EVOLVING_HOCKEY_USER`/`EVOLVING_HOCKEY_PASS` (`~/.Renviron`) to re-capture; Pro-Subscriber paywall |
| Published RAPM (Ryan Davis) | `tests/fixtures/nba_oracle/rapm_ryan_davis_sample.csv` | 3-row byte-quoted sample only | 2009-10 season | full file in `ClaudeCowork/nba_data/data_metrics/rapm_ryan_davis.csv` (gitignored, no other copy) |
| Published EPM (Dunks & Threes) | `tests/fixtures/nba_oracle/epm_sample.csv`, `dunks_threes_sample.csv` | 3-row samples | 2025 season | full files `2025_EPM_data.csv`, `2025_Dunks_&_Threes_Stats.csv` in the same `ClaudeCowork` dir |
| Published DARKO DPM | `tests/fixtures/nba_oracle/darko_dpm_sample.csv` | 3-row sample, sign-prefixed int columns, UTF-8 BOM header preserved | 2026 | full file `2026-darko-dpm-leaderboard.csv` |
| Published LEBRON | `tests/fixtures/nba_oracle/lebron_season_sample.csv`, `lebron_daily_sample.csv` | 3-row samples | 2026 season / one daily snapshot | full files `lebron-data-2026.csv`, `lebron_daily_2026-07-02.csv` |

All six NBA oracle fixtures share one gotcha worth restating (it already
burned this ecosystem once): the *committed* sample rows are real
byte-quoted captures now, but an earlier revision had round-number
placeholder rows that were never real data — read `nba_oracle/README.md`'s
"Honesty note" before trusting a value from the sample files instead of the
full CSVs behind `SDV_PY_NBA_ORACLE_DIR`.

---

## 5. Honest gaps

- **KenPom has no captured corpus anywhere in this ecosystem** — it's
  paywalled with no flat CSV endpoint, unlike Torvik. Every "KenPom-style"
  reference in the codebase is a methodology descriptor for a fixed-point
  SoS solver, not a data source.
- **The CFB recruiting-family floors (§1b) are not in `release_coverage.json`**
  — that audit predates the `cfbfastR-cfb-data` recruiting producer. If a
  future re-run of the season-coverage audit picks these up, prefer its
  numbers over the source-code derivation here; until then, this file's
  §1b derivation is the only record of *why* 2005 and not some other year.
  There is also no `load_cfb_recruits`/`load_cfb_team_talent` in
  `loader_map.json` (or in `sdv-py/sportsdataverse/cfb/cfb_loaders.py`) —
  today these are compute-on-demand (`cfb_roster_talent()`,
  `cfb_returning_production()`), not release-backed loaders.
- **MLB has zero release datasets** (§2) — no season floor to report because
  there is no `load_mlb_*` to floor. `pub-plan.md` Phase 4 proposes a
  Statcast-era (2015+) floor for a not-yet-built `mlb-data` producer.
- **`audit.md` and `loader_map.json`/`release_coverage.json` measure
  different things and neither source reconciles them.** The audit's
  per-league "Data span (the ceilings)" tables (e.g. NBA's SportVU 2013-14+,
  Synergy 2015-16+) are the modeler-relevant ceiling; `loader_map.json`'s
  `floor` field is the loader-relevant floor. Where they disagree (e.g. NFL
  `sdv-release` loaders show `floor=null` in the JSON but `audit.md` states
  1999–2025), this file cites `audit.md` for the training-relevant number
  and flags the JSON's `null` rather than silently picking one.
