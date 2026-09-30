# SportsDataverse ecosystem status

_80 public repos · generated 2026-09-30T08:22Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [sportsdataverse-data release tags — freshness](#sportsdataverse-data-release-tags--freshness)
- [Producers](#producers)
- [Red default-branch workflows](#red-default-branch-workflows)
- [Open PRs (most idle first)](#open-prs-most-idle-first)
- [Open issues](#open-issues)
- [Release-asset freshness (data producers)](#release-asset-freshness-data-producers)
- [Package repos — latest release](#package-repos--latest-release)
- [Unmapped release tags](#unmapped-release-tags)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## sportsdataverse-data release tags — freshness

367 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest standalone year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| cfb_crosswalk | cfbfastR-cfb-data | 26 | 2026-06-13T08:31 | 109.0 | 2025 |
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 75.7 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 73.8 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 73.8 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 70.3 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-07-22T21:39 | 69.4 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 69.4 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 55 | 2026-07-23T00:02 | 69.3 | 2026 |
| nhl_team_boxscores | fastRhockey-nhl-data | 55 | 2026-07-23T00:03 | 69.3 | 2026 |
| nhl_pbp_lite | fastRhockey-nhl-data | 64 | 2026-07-23T00:03 | 69.3 | 2026 |
| nhl_player_boxscores | fastRhockey-nhl-data | 55 | 2026-07-23T00:03 | 69.3 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 55.0 | 2025 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-08-12T05:47 | 49.1 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-08-12T05:47 | 49.1 | 2026 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 49.0 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 49.0 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 49.0 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 49.0 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 49.0 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 49.0 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:05 | 49.0 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 49.0 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 48.1 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 181 | 2026-08-13T05:19 | 48.1 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 48.1 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 188 | 2026-08-13T05:20 | 48.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 769 | 2026-08-13T08:38 | 48.0 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 47.6 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 47.6 | 2026 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 47.6 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 47.6 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 47.6 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 47.6 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 47.6 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 47.6 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 47.6 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 47.6 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 90 | 2026-08-13T17:44 | 47.6 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 47.6 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 90 | 2026-08-13T18:11 | 47.6 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 47.5 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 42.8 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 42.8 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 42.8 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 42.8 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 42.8 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 42.8 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 42.8 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 42.8 | 2026 |
| nba_crosswalk | hoopR-nba-data | 25 | 2026-08-19T01:34 | 42.3 | 2027 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 41.3 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 41.3 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 41.3 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 41.3 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 41.3 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 41.3 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 37.3 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 37.3 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 37.0 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 37.0 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 33.9 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 33.9 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 33.5 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 33.5 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 33.5 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 33.5 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 33.5 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 33.5 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 33.5 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 33.5 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 33.5 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 28.5 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 28.5 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 28.5 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 28.5 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 28.5 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 28.5 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 28.5 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 56 | 2026-09-01T20:26 | 28.5 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 28.5 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 48 | 2026-09-02T18:05 | 27.6 | 2025 |
| nba_player_impact | hoopR-nba-stats-data | 95 | 2026-09-02T18:27 | 27.6 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 27.6 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 27.6 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 27.6 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 27.6 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 27.6 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 27.6 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 27.6 | 2023 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-09-02T19:02 | 27.6 | 2026 |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-09-02T19:52 | 27.5 | 2025 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-02T19:55 | 27.5 | 2025 |
| nba_stats_hustle | hoopR-nba-stats-data | 86 | 2026-09-02T19:55 | 27.5 | 2025 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-02T19:57 | 27.5 | 2026 |
| nhl_game_rosters | fastRhockey-nhl-data | 55 | 2026-09-07T09:08 | 23.0 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 28 | 2026-09-07T23:12 | 22.4 |  |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 21.2 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 21.2 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 21.2 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 21.2 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 21.2 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 21.2 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-09-09T04:42 | 21.2 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 21.2 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 21.1 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-09-09T05:16 | 21.1 | 2026 |
| espn_nba_team_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 21.1 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 21.1 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 79 | 2026-09-09T05:18 | 21.1 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 21.1 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 21.1 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 21.1 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 21.1 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 21.1 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 21.1 | 2026 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-09-09T05:43 | 21.1 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 61 | 2026-09-09T06:28 | 21.1 | 2026 |
| nhl_game_info | fastRhockey-nhl-data | 55 | 2026-09-09T07:56 | 21.0 | 2026 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_linescore | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_penalties | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_scoring | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_scratches | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_three_stars | fastRhockey-nhl-data | 55 | 2026-09-09T07:57 | 21.0 | 2026 |
| nhl_officials | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 20.9 | 2026 |
| nhl_shootout | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 20.9 | 2026 |
| nhl_shots_by_period | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 20.9 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 25 | 2026-09-09T14:13 | 20.8 |  |
| nhl_shifts | fastRhockey-nhl-data | 55 | 2026-09-09T22:14 | 20.4 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-09-10T04:38 | 20.2 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-09-10T04:58 | 20.1 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-09-10T14:28 | 19.7 | 2026 |
| espn_nba_schedules | hoopR-nba-data | 88 | 2026-09-15T07:57 | 15.0 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-09-15T07:57 | 15.0 | 2027 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-09-15T07:57 | 15.0 | 2027 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-09-15T08:21 | 15.0 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-09-15T08:22 | 15.0 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-09-19T00:45 | 11.3 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-09-19T01:46 | 11.3 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 3.2 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 3.2 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 3.2 | 2025 |
| nfl_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 3.2 | 2026 |
| nhl_groups | sdv-reference-data | 224 | 2026-09-27T03:32 | 3.2 | 2026 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 3.2 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 94 | 2026-09-27T10:25 | 2.9 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 82 | 2026-09-27T10:26 | 2.9 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-09-27T11:40 | 2.9 | 2027 |
| mlb_parks | sdv-reference-data | 2 | 2026-09-27T19:55 | 2.5 |  |
| mbb_groups | sdv-reference-data | 60 | 2026-09-28T13:33 | 1.8 | 2027 |
| mlb_groups | sdv-reference-data | 260 | 2026-09-28T13:34 | 1.8 | 2026 |
| wbb_groups | sdv-reference-data | 60 | 2026-09-28T13:34 | 1.8 | 2027 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-09-28T14:41 | 1.7 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-09-28T17:32 | 1.6 | 2026 |
| nfl_players | nfl-data | 5 | 2026-09-28T17:33 | 1.6 |  |
| nfl_player_stats | nfl-data | 5 | 2026-09-28T17:33 | 1.6 |  |
| nfl_team_stats | nfl-data | 5 | 2026-09-28T17:34 | 1.6 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-09-28T17:39 | 1.6 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-09-28T20:22 | 1.5 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-09-29T10:39 | 0.9 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-09-29T10:39 | 0.9 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-09-29T10:39 | 0.9 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-09-29T10:40 | 0.9 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 85 | 2026-09-29T10:40 | 0.9 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-09-29T10:40 | 0.9 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-09-29T10:41 | 0.9 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-09-29T10:41 | 0.9 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-09-29T10:41 | 0.9 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-09-29T10:42 | 0.9 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-09-29T10:42 | 0.9 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-09-29T10:42 | 0.9 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 16 | 2026-09-29T10:43 | 0.9 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-09-29T14:31 | 0.7 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-09-29T15:33 | 0.7 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-09-29T15:33 | 0.7 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-09-29T15:33 | 0.7 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-09-29T15:34 | 0.7 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-09-29T15:34 | 0.7 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-09-29T15:34 | 0.7 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-09-29T15:34 | 0.7 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-09-29T15:35 | 0.7 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-09-29T15:35 | 0.7 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-09-29T15:35 | 0.7 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 8 | 2026-09-29T15:35 | 0.7 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-09-29T17:10 | 0.6 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-09-29T18:00 | 0.6 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-09-29T18:01 | 0.6 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-09-29T18:03 | 0.6 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-09-29T18:15 | 0.6 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-09-29T18:15 | 0.6 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-09-29T18:15 | 0.6 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-09-29T18:16 | 0.6 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-09-29T18:16 | 0.6 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-09-29T18:16 | 0.6 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-09-29T18:17 | 0.6 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-09-29T18:17 | 0.6 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-09-29T18:17 | 0.6 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-09-29T18:17 | 0.6 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-09-29T18:18 | 0.6 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-09-29T18:18 | 0.6 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-09-29T18:18 | 0.6 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-09-29T18:20 | 0.6 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-09-29T18:22 | 0.6 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-09-29T18:23 | 0.6 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-09-29T18:30 | 0.6 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-09-29T18:30 | 0.6 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-09-29T18:30 | 0.6 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-09-29T18:30 | 0.6 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-09-29T18:30 | 0.6 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-09-29T18:30 | 0.6 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-09-29T18:30 | 0.6 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-29T18:33 | 0.6 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-29T18:33 | 0.6 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-29T18:33 | 0.6 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-09-29T19:03 | 0.6 | 2026 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-09-29T19:14 | 0.5 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-09-29T19:14 | 0.5 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-09-29T19:14 | 0.5 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-09-29T19:14 | 0.5 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-09-29T19:15 | 0.5 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-09-29T19:15 | 0.5 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-09-29T19:15 | 0.5 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-09-29T19:15 | 0.5 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-09-29T19:15 | 0.5 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-09-29T19:16 | 0.5 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-09-29T19:16 | 0.5 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-09-29T19:16 | 0.5 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-09-29T19:16 | 0.5 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-09-29T19:16 | 0.5 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-09-29T19:17 | 0.5 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 0.4 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-09-29T23:32 | 0.4 | 2026 |
| espn_nfl_qa | nfl-data | 3 | 2026-09-29T23:32 | 0.4 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-09-29T23:32 | 0.4 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 23 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-09-29T23:33 | 0.4 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 23 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 23 | 2026-09-29T23:34 | 0.4 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-09-29T23:35 | 0.4 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-09-29T23:35 | 0.4 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-09-29T23:35 | 0.4 |  |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-09-30T01:33 | 0.3 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-09-30T01:34 | 0.3 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-09-30T01:34 | 0.3 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-09-30T01:35 | 0.3 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-09-30T01:35 | 0.3 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-09-30T01:36 | 0.3 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-09-30T01:37 | 0.3 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-09-30T01:37 | 0.3 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-09-30T01:38 | 0.3 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-09-30T01:38 | 0.3 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-09-30T01:39 | 0.3 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-09-30T01:39 | 0.3 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-09-30T01:40 | 0.3 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-09-30T01:40 | 0.3 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-09-30T01:41 | 0.3 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-09-30T01:41 | 0.3 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-09-30T01:41 | 0.3 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-09-30T01:42 | 0.3 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-09-30T01:42 | 0.3 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-09-30T01:43 | 0.3 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-09-30T01:46 | 0.3 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-09-30T01:50 | 0.3 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T01:53 | 0.3 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T01:56 | 0.3 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-09-30T01:59 | 0.3 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-09-30T02:03 | 0.3 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-09-30T02:07 | 0.3 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-09-30T02:11 | 0.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T02:14 | 0.3 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T02:17 | 0.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-09-30T02:20 | 0.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-09-30T02:23 | 0.2 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-09-30T02:27 | 0.2 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-09-30T02:30 | 0.2 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-09-30T02:33 | 0.2 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-09-30T02:36 | 0.2 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-09-30T02:39 | 0.2 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-09-30T02:43 | 0.2 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-09-30T02:47 | 0.2 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-09-30T02:51 | 0.2 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-09-30T02:55 | 0.2 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-09-30T02:58 | 0.2 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-09-30T02:59 | 0.2 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-09-30T02:59 | 0.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-09-30T03:04 | 0.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-09-30T03:04 | 0.2 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-09-30T03:05 | 0.2 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-09-30T03:06 | 0.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-09-30T03:06 | 0.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-09-30T03:08 | 0.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-09-30T03:08 | 0.2 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-09-30T03:13 | 0.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-09-30T03:23 | 0.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-09-30T03:23 | 0.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-09-30T03:23 | 0.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-09-30T03:23 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-09-30T03:24 | 0.2 |  |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 0.2 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 0.1 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 0.1 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 0.1 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-09-30T05:27 | 0.1 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-09-30T07:12 | 0.0 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-09-30T07:12 | 0.0 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-09-30T07:13 | 0.0 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-09-30T07:14 | 0.0 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-09-30T07:14 | 0.0 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-09-30T07:15 | 0.0 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-09-30T07:16 | 0.0 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-09-30T07:17 | 0.0 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-09-30T08:18 | 0.0 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-09-30T08:23 | -0.0 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-09-30T08:24 | -0.0 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-09-30T08:24 | -0.0 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-09-30T08:24 | -0.0 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-09-30T08:24 | -0.0 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-09-30T08:25 | -0.0 | 2026 |
| espn_cfb_player_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_cfb_team_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `idle` = out of season, never an alarm.

| repo | state | in season | data updated | through season | update workflows |
|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-09-30 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-09-29<br>`cfb_fpi_weekly.yml` success 2026-09-29<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-09-29 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-09-28 | 2026 | `daily_cfb.yml` success 2026-09-28 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-09-29 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-09-29 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-09-30 | 2026 | `espn_nfl_cron.yml` success 2026-09-29<br>`nfl_pbp_cron.yml` success 2026-09-30<br>`nfl_ratings_weekly.yml` success 2026-09-29<br>`nfl_rosters_players_cron.yml` success 2026-09-28<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-09-29 | 2026 | `daily_ngs.yml` success 2026-09-29 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-09-30 | 2026 | `daily_mbb.yml` success 2026-08-07<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-24 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-09-15 | 2026 | `daily_nba.yml` cancelled 2026-09-09 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-09-02 | 2026 | `daily_nba_stats.yml` success 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` no runs |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-09-30 | 2026 | `daily_wbb.yml` success 2026-09-09<br>`weekly_wbb.yml` success 2026-09-27<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-24 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-09-29 | 2026 | `daily_wnba.yml` success 2026-09-29<br>`weekly_wnba.yml` success 2026-09-27<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-09-29 | 2026 | `daily_wnba_stats.yml` success 2026-09-13<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | idle | no | 2026-09-09 | 2026 | `daily_nhl.yml` success 2026-07-22<br>`daily_nhl_python.yml` no runs<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-09-02 | 2026 | `daily_pwhl.yml` success 2026-07-18<br>`daily_pwhl_python.yml` no runs<br>`pwhl_xg_cron.yml` no runs |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | fresh | yes | 2026-09-29 | 2026 | `mlb_models_cron.yml` success 2026-09-29<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-09-29 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 59.9 |
| sportsdataverse/baseballr-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/36263141819) | 3.6 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 36.8 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 55.7 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 31.8 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 113.0 |
| sportsdataverse/hoopR-nba-data | Update NBA Data | cancelled | [run](https://github.com/sportsdataverse/hoopR-nba-data/actions/runs/34314472849) | 21.1 |
| sportsdataverse/hoopR-nba-data | tests | failure | [run](https://github.com/sportsdataverse/hoopR-nba-data/actions/runs/31059833392) | 55.3 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/34331662340) | 21.0 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/36672953834) | 0.1 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 33.7 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/25519402950) | 145.5 |
| sportsdataverse/wehoop-wnba-raw | tests | failure | [run](https://github.com/sportsdataverse/wehoop-wnba-raw/actions/runs/36556464017) | 0.9 |
| sportsdataverse/wehoop-wnba-stats-raw | tests | failure | [run](https://github.com/sportsdataverse/wehoop-wnba-stats-raw/actions/runs/36573019473) | 0.8 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 24.0 | 24.0 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 16.7 | 16.7 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 493.2 | 14.4 |  |
| sportsdataverse/sportsdataverse-py | [#617](https://github.com/sportsdataverse/sportsdataverse-py/pull/617) docs(tutorials): weekly refresh of executed notebook pages | github-actions[bot] | 1.4 | 1.4 |  |
| sportsdataverse/sportyR | [#52](https://github.com/sportsdataverse/sportyR/pull/52) Add NCAA softball field via geom_softball() | billyfryer | 0.7 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#290](https://github.com/saiemgilani/game-on-paper-app/pull/290) fix(players): the game log's Live and QA badges in #270's Performance  | saiemgilani | 0.4 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#270](https://github.com/saiemgilani/game-on-paper-app/pull/270) Fixing design issues + Team Stats SSR + splitting Situational Metrics | akeaswaran | 10.3 | 0.3 | y |
| saiemgilani/game-on-paper-app | [#264](https://github.com/saiemgilani/game-on-paper-app/pull/264) test(tables): render-level contract tests, twin parity and aggregation | saiemgilani | 11.2 | 0.2 |  |
| sportsdataverse/sportsdataverse-data | [#20](https://github.com/sportsdataverse/sportsdataverse-data/pull/20) docs(notes): wbb_ratings 2009-2012 correction and 2008 withdrawal | saiemgilani | 0.1 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#292](https://github.com/saiemgilani/game-on-paper-app/pull/292) fix(glossary): fourth-down, pace, finishing, third-down and neutral pa | saiemgilani | 0.1 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#280](https://github.com/saiemgilani/game-on-paper-app/pull/280) fix(game): fit the drive chart to the screen instead of scrolling it | saiemgilani | 3.6 | 0.1 |  |
| sportsdataverse/cfbfastR | [#166](https://github.com/sportsdataverse/cfbfastR/pull/166) docs(cfbd): SDV return tables for recent cfbd_* wrappers + box_advance | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#632](https://github.com/sportsdataverse/sportsdataverse-py/pull/632) feat(football)!: tackle share counts only the defense's own scrimmage  | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#631](https://github.com/sportsdataverse/sportsdataverse-py/pull/631) fix(cfb): a completion whose text states no gain takes ESPN's statYard | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#630](https://github.com/sportsdataverse/sportsdataverse-py/pull/630) feat(football)!: CFB situation-neutral reads the score-and-clock win p | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#629](https://github.com/sportsdataverse/sportsdataverse-py/pull/629) fix(football): pace counts regulation drives once, for the drive's own | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#628](https://github.com/sportsdataverse/sportsdataverse-py/pull/628) fix(football): a season usage table keeps one row per player | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#627](https://github.com/sportsdataverse/sportsdataverse-py/pull/627) fix(football): credit a tackle to the tackler's own team | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#626](https://github.com/sportsdataverse/sportsdataverse-py/pull/626) fix(cfb): overtime-aware win probability, decided end-of-regulation st | saiemgilani | 0.0 | 0.0 | y |
| sportsdataverse/sportsdataverse-py | [#625](https://github.com/sportsdataverse/sportsdataverse-py/pull/625) feat(cfb): ship the gated xQBR retrain (served features, no spread) | saiemgilani | 0.0 | 0.0 | y |
| sportsdataverse/sportsdataverse-py | [#624](https://github.com/sportsdataverse/sportsdataverse-py/pull/624) fix(football): a pick-six or fumble-return touchdown is not the offens | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/cfbfastR-cfb-data | [#116](https://github.com/sportsdataverse/cfbfastR-cfb-data/pull/116) feat(models): gated xQBR retrain on the served box score, committed ES | saiemgilani | 0.1 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#293](https://github.com/saiemgilani/game-on-paper-app/pull/293) fix(game): turnover model to two decimals, Pass Breakups from the payl | saiemgilani | 0.1 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#291](https://github.com/saiemgilani/game-on-paper-app/pull/291) fix(coaches): name split-season teams, rate third downs over expected, | saiemgilani | 0.1 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#286](https://github.com/saiemgilani/game-on-paper-app/pull/286) fix(sdv): key the Data API cache by each table's ingest stamp | saiemgilani | 2.4 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#284](https://github.com/saiemgilani/game-on-paper-app/pull/284) feat(team): Five Factors table on the season team page (preview) | saiemgilani | 2.5 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 8 | 7 |
| BillPetti/baseballr | 7 | 7 |
| sportsdataverse/sportyR | 6 | 6 |
| sportsdataverse/sportsdataverse-py | 6 | 4 |
| sportsdataverse/wehoop-wnba-data | 2 | 2 |
| sportsdataverse/hoopR | 1 | 1 |
| sportsdataverse/cfbfastR | 1 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/sportypy | 1 | 1 |
| sportsdataverse/softballR | 1 | 1 |
| sportsdataverse/sportsdataverse-data | 1 | 1 |
| sportsdataverse/hoopR-nba-stats-data | 1 | 1 |
| sportsdataverse/wehoop-wbb-data | 1 | 1 |
| sportsdataverse/nfl-data | 1 | 1 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 62.4 | 0.3 |
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-07-28T06:34 | 64.1 | 0.3 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 681.0 | 911.6 |
| sportsdataverse/sportsdataverse-data | nfl_team_opponent_splits | 367 | 2026-09-30T08:25 | -0.0 | 0.1 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.0 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 2.5 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.0 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 4.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 3.2 |
| sportsdataverse/hoopR | v1.0.4 | 2021-05-21 | 0.1 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 4.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.3 |
| sportsdataverse/sportsdataverse-js | v3.0.0 | 2026-06-17 | 4.1 |
| sportsdataverse/sportsdataverse-py | v0.1.4 | 2026-09-01 | 0.0 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 4.1 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 4.1 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.3 |

## Unmapped release tags

5 `sportsdataverse/sportsdataverse-data` tags have no producer in `producers.json` (unattributed on purpose until the publishing code is found; never guessed).

- `nhl_xg_models`
- `phf_pbp`
- `phf_player_boxscores`
- `phf_schedules`
- `phf_team_boxscores`
