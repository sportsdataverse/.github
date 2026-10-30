# SportsDataverse ecosystem status

_80 public repos · generated 2026-10-30T16:08Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

383 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 106.0 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 104.1 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 104.1 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 100.6 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 85.3 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 79.3 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 79.3 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 79.3 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 79.3 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 79.3 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 79.3 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 79.3 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 77.9 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 77.9 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 77.9 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 77.9 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 77.9 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 77.9 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 77.9 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 73.1 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 73.1 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 73.1 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 73.1 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 73.1 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 73.1 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 73.1 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 71.6 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 71.6 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 71.6 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 71.6 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 71.6 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 71.6 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 67.6 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 67.6 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 67.3 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 67.3 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 64.2 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 64.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 63.9 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 63.9 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 63.9 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 63.9 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 63.9 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 63.9 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 63.8 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 63.8 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 63.8 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 58.8 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 58.8 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 58.8 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 58.8 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 58.8 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 58.8 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 58.8 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 58.8 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 57.9 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 57.9 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 57.9 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 57.9 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 57.9 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 57.9 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 57.9 | 2023 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 51.5 | 2026 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 33.5 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 33.5 | 2025 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 33.5 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 30.7 | 2026 |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 30.5 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 30.5 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 30.5 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 30.5 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 30.1 |  |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 29.7 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 29.7 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 29.7 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 29.7 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 29.6 | 2026 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 92 | 2026-10-01T22:01 | 28.8 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T22:33 | 28.7 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 22.1 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 22.1 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 22.1 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 22.1 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 22.1 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 22.1 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 22.1 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 22.1 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 22.1 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 22.1 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 22.1 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 22.1 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 22.1 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 22.1 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:37 | 22.1 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-09T05:35 | 21.4 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-11T10:41 | 19.2 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-11T10:41 | 19.2 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 19.2 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 19.1 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 19.1 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 19.1 | 2026 |
| mlb_groups | sdv-reference-data | 260 | 2026-10-11T15:00 | 19.0 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 19.0 |  |
| nfl_groups | sdv-reference-data | 122 | 2026-10-11T15:01 | 19.0 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 18.7 | 2025 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-10-12T03:05 | 18.5 | 2027 |
| mbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 18.4 | 2027 |
| wbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 18.4 | 2027 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 18.4 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-10-12T06:59 | 18.4 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 55 | 2026-10-12T07:08 | 18.4 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-10-12T07:11 | 18.4 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-10-12T07:55 | 18.3 |  |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 18.3 |  |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 59 | 2026-10-12T23:30 | 17.7 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-10-18T12:35 | 12.1 | 2027 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-10-18T14:16 | 12.1 | 2027 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-10-18T15:30 | 12.0 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-10-20T18:14 | 9.9 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 151 | 2026-10-26T12:57 | 4.1 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 109 | 2026-10-26T13:05 | 4.1 | 2026 |
| nhl_groups | sdv-reference-data | 226 | 2026-10-26T13:34 | 4.1 | 2027 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-10-26T14:15 | 4.1 | 2026 |
| nfl_players | nfl-data | 5 | 2026-10-26T16:03 | 4.0 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-10-26T16:08 | 4.0 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-10-26T19:43 | 3.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-10-26T19:43 | 3.9 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-10-26T19:44 | 3.9 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-10-26T23:57 | 3.7 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-27T13:13 | 3.1 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-27T13:14 | 3.1 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-27T13:14 | 3.1 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-27T13:15 | 3.1 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-27T13:15 | 3.1 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-27T13:16 | 3.1 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-27T13:16 | 3.1 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-27T13:16 | 3.1 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-27T15:20 | 3.0 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 3.0 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 3.0 | 2026 |
| nfl_model_pbp_backup_rev7_20261027 | nfl-data | 14 | 2026-10-27T18:09 | 2.9 |  |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-10-28T08:05 | 2.3 | 2027 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-28T13:11 | 2.1 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-28T13:11 | 2.1 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-10-29T03:56 | 1.5 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-10-29T03:57 | 1.5 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-10-29T03:58 | 1.5 | 2026 |
| nfl_paper_index_games | nfl-data | 29 | 2026-10-29T03:58 | 1.5 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-10-29T04:01 | 1.5 |  |
| nfl_team_summaries | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-10-29T05:21 | 1.4 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-29T05:22 | 1.4 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-10-29T05:22 | 1.4 | 2026 |
| nfl_model_pbp | nfl-data | 33 | 2026-10-29T05:22 | 1.4 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-10-29T05:24 | 1.4 |  |
| nfl_team_stats | nfl-data | 5 | 2026-10-29T05:24 | 1.4 |  |
| mlb_pbp | baseballr-data | 121 | 2026-10-29T12:33 | 1.1 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-29T12:34 | 1.1 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-29T12:35 | 1.1 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-29T12:35 | 1.1 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-29T13:17 | 1.1 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-29T13:17 | 1.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-29T14:04 | 1.1 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 871 | 2026-10-29T14:19 | 1.1 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 828 | 2026-10-29T14:20 | 1.1 | 2027 |
| nba_stats_matchups | hoopR-nba-stats-data | 58 | 2026-10-29T14:20 | 1.1 | 2027 |
| nba_stats_hustle | hoopR-nba-stats-data | 94 | 2026-10-29T14:20 | 1.1 | 2027 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-29T14:32 | 1.1 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-29T17:28 | 0.9 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-29T18:15 | 0.9 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-29T18:16 | 0.9 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-29T18:17 | 0.9 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-10-29T18:49 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-10-29T18:50 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-10-29T18:50 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-10-29T18:51 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-10-29T18:51 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-10-29T18:51 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-10-29T18:51 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-29T18:53 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-29T18:54 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-29T18:54 | 0.9 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-10-30T03:21 | 0.5 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-30T03:28 | 0.5 | 2026 |
| nba_player_impact | hoopR-nba-stats-data | 99 | 2026-10-30T08:01 | 0.3 | 2027 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-30T08:03 | 0.3 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-30T08:04 | 0.3 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-30T08:05 | 0.3 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 109 | 2026-10-30T08:05 | 0.3 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-30T08:05 | 0.3 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-30T08:05 | 0.3 | 2027 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-10-30T08:28 | 0.3 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-30T08:29 | 0.3 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-30T08:30 | 0.3 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-30T08:31 | 0.3 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-30T08:32 | 0.3 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-30T08:33 | 0.3 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-30T08:34 | 0.3 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-30T08:35 | 0.3 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-30T08:36 | 0.3 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-30T08:36 | 0.3 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-30T08:37 | 0.3 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-30T08:38 | 0.3 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-30T08:39 | 0.3 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-30T08:40 | 0.3 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-30T08:40 | 0.3 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-30T08:41 | 0.3 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-30T08:42 | 0.3 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-30T08:43 | 0.3 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-30T08:43 | 0.3 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-30T08:44 | 0.3 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-30T08:49 | 0.3 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-30T08:54 | 0.3 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-30T08:59 | 0.3 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-30T09:04 | 0.3 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-10-30T09:10 | 0.3 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-30T09:15 | 0.3 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-10-30T09:20 | 0.3 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-10-30T09:26 | 0.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-10-30T09:31 | 0.3 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-30T09:36 | 0.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-10-30T09:42 | 0.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-30T09:47 | 0.3 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-30T09:54 | 0.3 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-10-30T10:01 | 0.3 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-10-30T10:09 | 0.2 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-30T10:15 | 0.2 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-10-30T10:22 | 0.2 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-30T10:28 | 0.2 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-10-30T10:35 | 0.2 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-10-30T10:40 | 0.2 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-30T10:42 | 0.2 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-30T10:42 | 0.2 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-30T10:42 | 0.2 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-30T10:43 | 0.2 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 94 | 2026-10-30T10:43 | 0.2 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-30T10:43 | 0.2 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-30T10:44 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-30T10:44 | 0.2 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-30T10:45 | 0.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-30T10:45 | 0.2 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-30T10:45 | 0.2 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-10-30T10:51 | 0.2 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-10-30T10:51 | 0.2 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-10-30T10:51 | 0.2 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-30T10:51 | 0.2 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-10-30T10:52 | 0.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-10-30T11:00 | 0.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-10-30T11:01 | 0.2 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-10-30T11:02 | 0.2 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-10-30T11:03 | 0.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-10-30T11:04 | 0.2 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-10-30T11:04 | 0.2 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-10-30T11:04 | 0.2 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-10-30T11:04 | 0.2 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-10-30T11:05 | 0.2 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-10-30T11:05 | 0.2 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-10-30T11:05 | 0.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-10-30T11:05 | 0.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-10-30T11:06 | 0.2 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-10-30T11:07 | 0.2 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-10-30T11:07 | 0.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-10-30T11:21 | 0.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-10-30T11:21 | 0.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-10-30T11:21 | 0.2 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-10-30T11:21 | 0.2 | 2026 |
| cfb_crosswalk | cfbfastR-cfb-data | 50 | 2026-10-30T11:22 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-10-30T11:22 | 0.2 |  |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-30T11:48 | 0.2 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-30T11:48 | 0.2 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-30T11:48 | 0.2 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-30T11:48 | 0.2 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-30T11:49 | 0.2 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-30T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-30T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-30T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-30T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-30T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-30T11:51 | 0.2 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-30T11:51 | 0.2 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-30T11:53 | 0.2 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-30T11:55 | 0.2 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-30T11:56 | 0.2 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 82 | 2026-10-30T12:03 | 0.2 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 106 | 2026-10-30T12:03 | 0.2 | 2027 |
| espn_nba_player_boxscores | hoopR-nba-data | 106 | 2026-10-30T12:03 | 0.2 | 2027 |
| espn_nba_player_core | hoopR-nba-data | 106 | 2026-10-30T12:04 | 0.2 | 2027 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-10-30T12:04 | 0.2 | 2027 |
| espn_nba_shots | hoopR-nba-data | 83 | 2026-10-30T12:05 | 0.2 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-30T12:05 | 0.2 | 2027 |
| espn_nba_player_season_stats | hoopR-nba-data | 107 | 2026-10-30T12:05 | 0.2 | 2027 |
| espn_nba_team_season_stats | hoopR-nba-data | 83 | 2026-10-30T12:06 | 0.2 | 2027 |
| espn_nba_game_rosters | hoopR-nba-data | 83 | 2026-10-30T12:06 | 0.2 | 2027 |
| espn_nba_officials | hoopR-nba-data | 83 | 2026-10-30T12:06 | 0.2 | 2027 |
| mlb_statcast | baseballr-data | 40 | 2026-10-30T12:37 | 0.1 | 2026 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-10-30T13:56 | 0.1 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-10-30T13:58 | 0.1 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-10-30T14:00 | 0.1 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-30T14:01 | 0.1 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-30T14:01 | 0.1 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-30T14:01 | 0.1 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-30T14:01 | 0.1 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-10-30T14:02 | 0.1 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-10-30T14:03 | 0.1 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-10-30T14:03 | 0.1 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-10-30T14:04 | 0.1 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-10-30T14:06 | 0.1 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-10-30T14:07 | 0.1 | 2026 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-10-30T14:14 | 0.1 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 98 | 2026-10-30T14:15 | 0.1 | 2027 |
| nba_stats_pbp | hoopR-nba-stats-data | 94 | 2026-10-30T14:15 | 0.1 | 2027 |
| nba_stats_possessions | hoopR-nba-stats-data | 94 | 2026-10-30T14:15 | 0.1 | 2027 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 94 | 2026-10-30T14:15 | 0.1 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-10-30T14:21 | 0.1 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 91 | 2026-10-30T14:31 | 0.1 | 2027 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-10-30T14:32 | 0.1 | 2027 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-30T14:50 | 0.1 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-30T14:51 | 0.1 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-30T14:51 | 0.1 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-30T14:51 | 0.1 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-30T14:52 | 0.1 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-30T14:52 | 0.1 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-30T14:52 | 0.1 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-30T14:52 | 0.1 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-10-30T14:53 | 0.1 | 2026 |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-10-30T15:30 | 0.0 | 2027 |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-10-29<br>`cfb_fpi_weekly.yml` success 2026-10-29<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-10-29 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-10-26 | 2026-10-26 | 2026 | `daily_cfb.yml` success 2026-10-26 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-30 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-10-29 | 2026-10-29 | 2026 | `espn_nfl_cron.yml` disabled 2026-10-26<br>`nfl_pbp_cron.yml` disabled 2026-10-26<br>`nfl_ratings_weekly.yml` disabled 2026-10-20<br>`nfl_rosters_players_cron.yml` disabled 2026-10-26<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2026 | `daily_ngs.yml` success 2026-10-30 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | failing | no | 2026-10-18 | 2026-10-30 | 2026 | `daily_mbb.yml` failure 2026-10-30<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-10-12 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2027 | `daily_nba.yml` success 2026-10-30 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2027 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-10-30 | 2026-10-30 | 2026 | `daily_wbb.yml` success 2026-10-30<br>`weekly_wbb.yml` success 2026-10-25<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-10-12 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | idle | no | 2026-10-30 | 2026-10-30 | 2026 | `daily_wnba.yml` success 2026-10-30<br>`weekly_wnba.yml` success 2026-10-25<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | idle | no | 2026-10-30 | 2026-10-30 | 2026 | `daily_wnba_stats.yml` success 2026-10-29<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-10-30 | 2026-10-30 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-10-08 | 2026-10-08 | 2026 | `daily_pwhl_python.yml` success 2026-10-08<br>`pwhl_xg_cron.yml` success 2026-10-08 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | fresh | yes | 2026-10-29 | 2026-10-30 | 2026 | `mlb_models_cron.yml` success 2026-10-29<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-10-26 | 2026-10-26 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| BillPetti/baseballr | R-CMD-check | failure | [run](https://github.com/BillPetti/baseballr/actions/runs/39994452180) | 6.9 |
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 90.2 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 67.2 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 86.1 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 62.1 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/40467159993) | 3.4 |
| sportsdataverse/fastRhockey | R-CMD-check | failure | [run](https://github.com/sportsdataverse/fastRhockey/actions/runs/40977247300) | 0.7 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 143.3 |
| sportsdataverse/hoopR-mbb-data | Update MBB Data | failure | [run](https://github.com/sportsdataverse/hoopR-mbb-data/actions/runs/41066149446) | 0.1 |
| sportsdataverse/hoopR-nba-stats-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-raw/actions/runs/40973301004) | 0.7 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/39549673868) | 9.4 |
| sportsdataverse/sdvplotR | R-hub | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/39070634243) | 12.8 |
| sportsdataverse/sdvplotR | automation-example | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/40387157239) | 3.9 |
| sportsdataverse/sportsdataverse-py | live tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/41034648172) | 0.3 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 64.1 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 54.4 | 54.4 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 47.0 | 25.2 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 523.5 | 8.4 |  |
| sportsdataverse/sportsdataverse-js | [#129](https://github.com/sportsdataverse/sportsdataverse-js/pull/129) chore(vendor): sync sdv-py codegen YAML to c2031afbc7 | github-actions[bot] | 3.8 | 3.8 |  |
| sportsdataverse/nfl-data | [#88](https://github.com/sportsdataverse/nfl-data/pull/88) fix(models): train CP from 2009; document the team-summary play set | saiemgilani | 0.5 | 0.5 |  |
| sportsdataverse/sdvplot-js | [#101](https://github.com/sportsdataverse/sdvplot-js/pull/101) chore(release): version packages | github-actions[bot] | 0.5 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#344](https://github.com/saiemgilani/game-on-paper-app/pull/344) feat(wbb): women's college basketball shooting dashboards behind the w | saiemgilani | 11.3 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#343](https://github.com/saiemgilani/game-on-paper-app/pull/343) feat(wbb): women's college basketball scoreboard and game page behind  | saiemgilani | 11.3 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#342](https://github.com/saiemgilani/game-on-paper-app/pull/342) feat(mbb): men's college basketball shooting dashboards behind the mbb | saiemgilani | 11.4 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#341](https://github.com/saiemgilani/game-on-paper-app/pull/341) feat(mbb): men's college basketball scoreboard and game page behind th | saiemgilani | 11.5 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#340](https://github.com/saiemgilani/game-on-paper-app/pull/340) feat(wnba): WNBA shooting dashboards and the teams-index landing behin | saiemgilani | 11.5 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#332](https://github.com/saiemgilani/game-on-paper-app/pull/332) feat(wnba): WNBA scoreboard and game pages behind the wnba preview fla | saiemgilani | 11.7 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#324](https://github.com/saiemgilani/game-on-paper-app/pull/324) refactor(basketball): league-parameterized basketball code, NBA byte-i | saiemgilani | 11.9 | 0.1 |  |
| sportsdataverse/sportsdataverse-web | [#137](https://github.com/sportsdataverse/sportsdataverse-web/pull/137) docs(cheatsheets): refresh eleven package cheat sheets to current main | saiemgilani | 0.2 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#354](https://github.com/saiemgilani/game-on-paper-app/pull/354) fix(game): the passer to watch is the team's dropback leader | saiemgilani | 0.0 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 8 | 8 |
| BillPetti/baseballr | 8 | 7 |
| sportsdataverse/sportyR | 5 | 5 |
| sportsdataverse/hoopR-nba-data | 7 | 5 |
| sportsdataverse/wehoop-wnba-data | 6 | 5 |
| sportsdataverse/sportsdataverse-py | 6 | 4 |
| sportsdataverse/wehoop-wbb-data | 4 | 4 |
| sportsdataverse/sportsdataverse-data | 6 | 3 |
| sportsdataverse/hoopR-mbb-data | 3 | 3 |
| sportsdataverse/fastRhockey-nhl-data | 4 | 3 |
| sportsdataverse/sdvplot | 4 | 3 |
| sportsdataverse/hoopR | 2 | 2 |
| sportsdataverse/wehoop | 2 | 2 |
| sportsdataverse/sportypy | 2 | 2 |
| sportsdataverse/softballR | 2 | 2 |
| sportsdataverse/cfbfastR | 3 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/sdvplotR | 1 | 1 |
| sportsdataverse/hoopR-nba-stats-data | 2 | 1 |
| sportsdataverse/wehoop-wnba-stats-data | 2 | 1 |
| sportsdataverse/hoopR-nba-stats-raw | 3 | 1 |
| sportsdataverse/nfl-data | 1 | 1 |
| sportsdataverse/ncaa-wbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mfb-football-data | 1 | 1 |
| sportsdataverse/baseballr-data | 1 | 0 |
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 19.0 | 0.7 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 92.8 | 1.1 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 711.3 | 18.3 |
| sportsdataverse/sportsdataverse-data | nfl_model_pbp_backup_rev7_20261027 | 383 | 2026-10-30T15:30 | 0.0 | 2.9 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.2 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 21.5 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.5 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.1 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.1 |
| sportsdataverse/sdvplot | v0.1.1 | 2026-10-26 | 0.1 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.2.0 | 2026-10-30 | 0.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.1 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.1 |
| sportsdataverse/sportsdataverse-py | v0.2.0b1 | 2026-10-26 | 0.0 |
| sportsdataverse/sportyR | v2.4.5 | 2026-10-27 | 0.1 |
| sportsdataverse/sportypy | v1.2.5 | 2026-10-30 | 0.1 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.1 |

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
