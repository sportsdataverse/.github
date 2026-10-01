# SportsDataverse ecosystem status

_81 public repos · generated 2026-10-01T16:37Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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
- [Warnings](#warnings)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## sportsdataverse-data release tags — freshness

374 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| cfb_crosswalk | cfbfastR-cfb-data | 26 | 2026-06-13T08:31 | 110.3 | 2025 |
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 77.0 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 75.2 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 75.2 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 71.6 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-07-22T21:39 | 70.8 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 70.8 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 56.4 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 50.4 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 50.4 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 50.4 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 50.4 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 50.4 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 50.4 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:05 | 50.4 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 50.4 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 49.5 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 49.5 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 49.5 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 95 | 2026-08-13T05:20 | 49.5 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 49.0 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 49.0 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 49.0 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 49.0 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 49.0 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 49.0 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 49.0 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 49.0 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 48.8 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 44.2 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 44.2 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 44.2 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 44.2 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 44.2 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 44.2 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 44.1 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 44.1 | 2026 |
| nba_crosswalk | hoopR-nba-data | 25 | 2026-08-19T01:34 | 43.6 | 2027 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 42.6 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 42.6 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 42.6 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 42.6 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 42.6 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 42.6 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 38.6 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 38.6 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 38.3 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 38.3 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 35.2 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 35.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 34.9 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 34.9 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 34.9 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 34.9 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 34.9 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 34.9 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 34.9 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 34.9 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 34.9 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 29.9 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 29.9 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 29.9 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 29.9 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 29.8 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 29.8 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 29.8 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 56 | 2026-09-01T20:26 | 29.8 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 29.8 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 48 | 2026-09-02T18:05 | 28.9 | 2025 |
| nba_player_impact | hoopR-nba-stats-data | 95 | 2026-09-02T18:27 | 28.9 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 28.9 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 28.9 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 28.9 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 28.9 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 28.9 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 28.9 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 28.9 | 2023 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-09-02T19:02 | 28.9 | 2026 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 22.5 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 22.5 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 22.5 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 22.5 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 22.5 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 22.5 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-09-09T04:42 | 22.5 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 22.5 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 22.5 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-09-09T05:16 | 22.5 | 2026 |
| espn_nba_team_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 22.5 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 22.5 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 79 | 2026-09-09T05:18 | 22.5 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 22.5 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 22.5 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 22.5 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 22.5 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 22.5 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 22.5 | 2026 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-09-09T05:43 | 22.5 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 22.2 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 25 | 2026-09-09T14:13 | 22.1 |  |
| mlb_pitches | baseballr-data | 121 | 2026-09-10T04:38 | 21.5 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-09-10T04:58 | 21.5 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-09-10T14:28 | 21.1 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-09-15T08:21 | 16.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-09-15T08:22 | 16.3 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-09-19T00:45 | 12.7 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-09-19T01:46 | 12.6 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 4.5 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 4.5 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 4.5 | 2025 |
| nfl_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 4.5 | 2026 |
| nhl_groups | sdv-reference-data | 224 | 2026-09-27T03:32 | 4.5 | 2026 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 4.5 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 94 | 2026-09-27T10:25 | 4.3 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 82 | 2026-09-27T10:26 | 4.3 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-09-27T11:40 | 4.2 | 2027 |
| mlb_parks | sdv-reference-data | 2 | 2026-09-27T19:55 | 3.9 |  |
| mbb_groups | sdv-reference-data | 60 | 2026-09-28T13:33 | 3.1 | 2027 |
| mlb_groups | sdv-reference-data | 260 | 2026-09-28T13:34 | 3.1 | 2026 |
| wbb_groups | sdv-reference-data | 60 | 2026-09-28T13:34 | 3.1 | 2027 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-09-28T14:41 | 3.1 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-09-28T17:32 | 3.0 | 2026 |
| nfl_players | nfl-data | 5 | 2026-09-28T17:33 | 3.0 |  |
| nfl_player_stats | nfl-data | 5 | 2026-09-28T17:33 | 3.0 |  |
| nfl_team_stats | nfl-data | 5 | 2026-09-28T17:34 | 3.0 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-09-28T17:39 | 3.0 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-09-28T20:22 | 2.8 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 16 | 2026-09-29T10:43 | 2.2 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-09-29T19:03 | 1.9 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 1.8 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-09-29T23:32 | 1.7 | 2026 |
| espn_nfl_qa | nfl-data | 3 | 2026-09-29T23:32 | 1.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-09-29T23:32 | 1.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 23 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-09-29T23:33 | 1.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-09-29T23:33 | 1.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-09-29T23:35 | 1.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-09-29T23:35 | 1.7 |  |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 1.5 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 1.5 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 1.5 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 1.5 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-09-30T05:27 | 1.5 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-09-30T07:12 | 1.4 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-09-30T07:12 | 1.4 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-09-30T07:13 | 1.4 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-09-30T07:14 | 1.4 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-09-30T07:14 | 1.4 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-09-30T07:15 | 1.4 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-09-30T07:16 | 1.4 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-09-30T07:17 | 1.4 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T09:32 | 1.3 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-09-30T09:48 | 1.3 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-09-30T10:04 | 1.3 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-09-30T10:18 | 1.3 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-09-30T10:28 | 1.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T10:39 | 1.2 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-09-30T10:44 | 1.2 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-09-30T10:52 | 1.2 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-09-30T11:00 | 1.2 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-09-30T11:08 | 1.2 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-09-30T11:13 | 1.2 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-09-30T11:18 | 1.2 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-09-30T11:24 | 1.2 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-09-30T11:29 | 1.2 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-09-30T11:35 | 1.2 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-09-30T11:43 | 1.2 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-09-30T11:49 | 1.2 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-09-30T11:56 | 1.2 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-09-30T12:04 | 1.2 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-09-30T12:04 | 1.2 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-09-30T12:04 | 1.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-09-30T12:16 | 1.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-09-30T12:16 | 1.2 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-09-30T12:18 | 1.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-09-30T12:19 | 1.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-09-30T12:20 | 1.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-09-30T12:21 | 1.2 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-09-30T12:28 | 1.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-09-30T12:49 | 1.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-09-30T12:50 | 1.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-09-30T12:50 | 1.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-09-30T12:51 | 1.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-09-30T12:51 | 1.2 |  |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-09-30T13:07 | 1.1 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-09-30T13:07 | 1.1 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-09-30T13:07 | 1.1 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-09-30T13:08 | 1.1 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-09-30T13:08 | 1.1 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-09-30T13:08 | 1.1 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-09-30T13:09 | 1.1 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-09-30T13:12 | 1.1 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 1.1 |  |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-09-30T14:05 | 1.1 | 2026 |
| nba_stats_hustle | hoopR-nba-stats-data | 90 | 2026-09-30T14:24 | 1.1 | 2026 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-30T14:28 | 1.1 | 2026 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-30T14:36 | 1.1 | 2027 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 23 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-09-30T14:50 | 1.1 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 23 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-09-30T14:52 | 1.1 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 1.1 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 1.1 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-09-30T16:48 | 1.0 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-09-30T17:48 | 1.0 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-09-30T17:49 | 1.0 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-09-30T17:50 | 0.9 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-09-30T18:18 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-09-30T18:19 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-09-30T18:19 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-09-30T18:19 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-09-30T18:19 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-09-30T18:19 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-09-30T18:19 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-30T18:22 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-30T18:22 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-09-30T18:22 | 0.9 | 2026 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 0.7 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 0.7 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 0.7 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 0.7 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 0.7 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 0.6 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-01T08:01 | 0.4 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-01T08:01 | 0.4 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-01T08:01 | 0.4 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-01T08:01 | 0.4 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-01T08:02 | 0.4 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-01T08:03 | 0.4 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-01T08:03 | 0.4 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 67 | 2026-10-01T08:03 | 0.4 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-01T08:03 | 0.4 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-01T08:03 | 0.4 | 2027 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-10-01T08:28 | 0.3 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-01T08:29 | 0.3 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-01T08:30 | 0.3 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-01T08:31 | 0.3 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-01T08:31 | 0.3 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-01T08:32 | 0.3 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-01T08:33 | 0.3 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-01T08:34 | 0.3 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-01T08:34 | 0.3 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-01T08:35 | 0.3 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-01T08:36 | 0.3 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-01T08:36 | 0.3 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-01T08:37 | 0.3 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-01T08:38 | 0.3 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-01T08:38 | 0.3 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-01T08:39 | 0.3 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-01T08:40 | 0.3 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-01T08:40 | 0.3 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-01T08:41 | 0.3 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-01T08:42 | 0.3 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-01T08:53 | 0.3 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-01T09:05 | 0.3 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-01T09:16 | 0.3 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-01T10:39 | 0.2 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-01T10:39 | 0.2 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-01T10:39 | 0.2 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-01T10:40 | 0.2 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 85 | 2026-10-01T10:40 | 0.2 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-01T10:40 | 0.2 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-01T10:41 | 0.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-01T10:41 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-01T10:41 | 0.2 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-01T10:41 | 0.2 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-01T10:42 | 0.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-01T10:42 | 0.2 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-01T11:45 | 0.2 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-01T11:47 | 0.2 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-01T11:47 | 0.2 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-01T11:47 | 0.2 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-01T11:48 | 0.2 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-01T11:48 | 0.2 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-01T11:48 | 0.2 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-01T11:48 | 0.2 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-01T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-01T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-01T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-01T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-01T11:49 | 0.2 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-01T11:50 | 0.2 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-01T11:51 | 0.2 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-01T11:53 | 0.2 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-01T11:53 | 0.2 | 2026 |
| espn_nba_schedules | hoopR-nba-data | 88 | 2026-10-01T11:59 | 0.2 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-01T11:59 | 0.2 | 2027 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-01T12:00 | 0.2 | 2027 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-01T12:07 | 0.2 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T12:45 | 0.2 | 2026 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-01T13:19 | 0.1 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-01T13:20 | 0.1 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-01T13:20 | 0.1 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-01T13:20 | 0.1 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-01T13:20 | 0.1 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-01T13:21 | 0.1 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-01T13:21 | 0.1 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-01T13:21 | 0.1 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-01T13:21 | 0.1 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 70 | 2026-10-01T14:01 | 0.1 | 2025 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 70 | 2026-10-01T14:01 | 0.1 | 2025 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-01T14:01 | 0.1 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-01T14:01 | 0.1 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-01T14:01 | 0.1 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-01T14:01 | 0.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-01T14:09 | 0.1 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 95 | 2026-10-01T14:31 | 0.1 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-01T15:55 | 0.0 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-01T15:56 | 0.0 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-01T15:56 | 0.0 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-01T15:56 | 0.0 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-01T15:56 | 0.0 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-01T15:56 | 0.0 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-01T15:57 | 0.0 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-01T15:57 | 0.0 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-01T15:57 | 0.0 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-01T15:57 | 0.0 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 8 | 2026-10-01T15:57 | 0.0 | 2026 |
| espn_cfb_player_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_cfb_team_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-01 | 2026-10-01 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-09-30<br>`cfb_fpi_weekly.yml` success 2026-09-30<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-09-30 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-09-28 | 2026-09-28 | 2026 | `daily_cfb.yml` success 2026-09-28 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-01 | 2026-10-01 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-01 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-09-29 | 2026-10-01 | 2026 | `espn_nfl_cron.yml` success 2026-09-29<br>`nfl_pbp_cron.yml` success 2026-09-30<br>`nfl_ratings_weekly.yml` success 2026-09-29<br>`nfl_rosters_players_cron.yml` success 2026-09-28<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-01 | 2026-10-01 | 2026 | `daily_ngs.yml` success 2026-10-01 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-09-19 | 2026-09-30 | 2026 | `daily_mbb.yml` success 2026-09-09<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-08-24 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-09-09 | 2026-10-01 | 2026 | `daily_nba.yml` cancelled 2026-09-09 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-08-13 | 2026-10-01 | 2026 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` no runs |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-09-19 | 2026-09-30 | 2026 | `daily_wbb.yml` success 2026-09-09<br>`weekly_wbb.yml` success 2026-09-27<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-08-24 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-10-01 | 2026-10-01 | 2026 | `daily_wnba.yml` success 2026-10-01<br>`weekly_wnba.yml` success 2026-09-27<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-10-01 | 2026-10-01 | 2026 | `daily_wnba_stats.yml` success 2026-10-01<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | idle | no | 2026-10-01 | 2026-10-01 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-07-22 | 2026-09-02 | 2026 | `daily_pwhl_python.yml` no runs<br>`pwhl_xg_cron.yml` no runs |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | stale | yes | 2026-09-10 | 2026-09-30 | 2026 | `mlb_models_cron.yml` success 2026-09-30<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-09-29 | 2026-09-29 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| BillPetti/baseballr | R-CMD-check | cancelled | [run](https://github.com/BillPetti/baseballr/actions/runs/36727692437) | 1.1 |
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 61.2 |
| sportsdataverse/baseballr-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/36722219995) | 1.1 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 38.2 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 57.1 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 33.1 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 114.4 |
| sportsdataverse/hoopR-nba-data | Update NBA Data | cancelled | [run](https://github.com/sportsdataverse/hoopR-nba-data/actions/runs/34314472849) | 22.5 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/34331662340) | 22.3 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/36854890964) | 0.2 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 35.1 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/25519402950) | 146.9 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 25.4 | 25.4 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 18.1 | 18.0 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 494.5 | 15.8 |  |
| saiemgilani/game-on-paper-app | [#280](https://github.com/saiemgilani/game-on-paper-app/pull/280) fix(game): fit the drive chart to the screen instead of scrolling it | saiemgilani | 5.0 | 1.4 |  |
| saiemgilani/game-on-paper-app | [#294](https://github.com/saiemgilani/game-on-paper-app/pull/294) chore(processor): bump sportsdataverse to 01d3c1ad6 (wave-2 fixes, xQB | saiemgilani | 1.1 | 1.0 |  |
| saiemgilani/game-on-paper-app | [#292](https://github.com/saiemgilani/game-on-paper-app/pull/292) fix(glossary): fourth-down, pace, finishing, third-down and neutral pa | saiemgilani | 1.5 | 1.0 |  |
| saiemgilani/game-on-paper-app | [#286](https://github.com/saiemgilani/game-on-paper-app/pull/286) fix(sdv): key the Data API cache by each table's ingest stamp | saiemgilani | 3.8 | 1.0 |  |
| saiemgilani/game-on-paper-app | [#293](https://github.com/saiemgilani/game-on-paper-app/pull/293) fix(game): turnover model to two decimals, Pass Breakups from the payl | saiemgilani | 1.5 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#291](https://github.com/saiemgilani/game-on-paper-app/pull/291) fix(coaches): name split-season teams, rate third downs over expected, | saiemgilani | 1.5 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#284](https://github.com/saiemgilani/game-on-paper-app/pull/284) feat(team): Five Factors table on the season team page (preview) | saiemgilani | 3.9 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#270](https://github.com/saiemgilani/game-on-paper-app/pull/270) Fixing design issues + Team Stats SSR + splitting Situational Metrics | akeaswaran | 11.7 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#264](https://github.com/saiemgilani/game-on-paper-app/pull/264) test(tables): render-level contract tests, twin parity and aggregation | saiemgilani | 12.5 | 0.6 |  |
| sportsdataverse/sportyR | [#52](https://github.com/sportsdataverse/sportyR/pull/52) Add NCAA softball field via geom_softball() | billyfryer | 2.0 | 0.4 |  |
| sportsdataverse/sdv-assets | [#11](https://github.com/sportsdataverse/sdv-assets/pull/11) data: monthly capture 2026-10-01 | saiemgilani | 0.4 | 0.4 |  |
| sportsdataverse/sportsdataverse-py | [#654](https://github.com/sportsdataverse/sportsdataverse-py/pull/654) chore: repo hygiene fixes found while porting sdv-py's tooling to sdvp | saiemgilani | 0.1 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 8 | 7 |
| BillPetti/baseballr | 7 | 7 |
| sportsdataverse/sportyR | 6 | 6 |
| sportsdataverse/sportsdataverse-py | 8 | 4 |
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
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/fastRhockey-nhl-data | 1 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-01T01:33 | 0.6 | 0.2 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 63.8 | 0.1 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 682.3 | 912.9 |
| sportsdataverse/sportsdataverse-data | wnba_stats_metric_curves | 374 | 2026-10-01T15:57 | 0.0 | 0.1 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.1 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 1.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.3 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 1.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 1.1 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 1.1 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 1.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.0 |
| sportsdataverse/sportsdataverse-js | v3.0.0 | 2026-06-17 | 1.1 |
| sportsdataverse/sportsdataverse-py | v0.1.4 | 2026-09-01 | 0.0 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 5.4 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 5.4 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 1.1 |

## Unmapped release tags

5 `sportsdataverse/sportsdataverse-data` tags have no producer in `producers.json` (unattributed on purpose until the publishing code is found; never guessed).

- `nhl_xg_models`
- `phf_pbp`
- `phf_player_boxscores`
- `phf_schedules`
- `phf_team_boxscores`

## Warnings

Config and collection problems found by this run.

- none
