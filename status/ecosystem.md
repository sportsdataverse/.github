# SportsDataverse ecosystem status

_80 public repos · generated 2026-11-26T19:12Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

388 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 131.3 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 131.3 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 112.5 | 2025 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 94.7 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 94.7 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 94.4 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 94.4 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 91.3 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 91.3 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 85.0 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 85.0 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 85.0 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 85.0 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 85.0 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 85.0 | 2023 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 57.2 |  |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 49.2 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 49.2 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 49.2 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 49.2 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 49.2 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 49.2 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 49.2 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 49.2 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 49.2 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 49.2 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 49.2 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 49.2 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 49.2 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 49.2 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 46.3 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 46.3 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 46.3 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 46.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 46.2 |  |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 45.8 | 2025 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 45.5 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 45.4 |  |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-10-18T14:16 | 39.2 | 2027 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-27T13:13 | 30.2 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 30.1 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 30.1 | 2026 |
| nfl_model_pbp_backup_rev7_20261027 | nfl-data | 14 | 2026-10-27T18:09 | 30.0 |  |
| mlb_pbp | baseballr-data | 121 | 2026-10-29T12:33 | 28.3 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-29T12:34 | 28.3 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-29T12:35 | 28.3 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-29T12:35 | 28.3 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-31T13:13 | 26.2 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-31T13:13 | 26.2 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-31T13:13 | 26.2 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 26.2 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-31T13:14 | 26.2 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 26.2 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-31T13:14 | 26.2 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 26.2 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 26.2 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:15 | 26.2 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:16 | 26.2 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-31T14:01 | 26.2 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-31T14:01 | 26.2 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-31T14:01 | 26.2 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-31T14:06 | 26.2 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-31T15:15 | 26.2 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-31T16:11 | 26.1 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-31T17:11 | 26.1 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-31T17:12 | 26.1 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-31T17:12 | 26.1 | 2026 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 58 | 2026-11-01T12:46 | 25.3 | 2027 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 58 | 2026-11-02T12:50 | 24.3 | 2027 |
| ncaa_mhockey_groups |  | 66 | 2026-11-03T00:16 | 23.8 | 2027 |
| ncaa_whockey_groups |  | 66 | 2026-11-03T00:16 | 23.8 | 2027 |
| mlb_groups | sdv-reference-data | 263 | 2026-11-03T11:20 | 23.3 | 2026 |
| wnba_groups | sdv-reference-data | 75 | 2026-11-03T11:38 | 23.3 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-04T02:47 | 22.7 | 2027 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-04T02:49 | 22.7 | 2027 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-11-08T14:06 | 18.2 | 2027 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-11-09T06:50 | 17.5 | 2026 |
| mlb_statcast | baseballr-data | 40 | 2026-11-09T13:37 | 17.2 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 186 | 2026-11-09T19:26 | 17.0 | 2026 |
| nba_current_impact | hoopR-nba-stats-data | 62 | 2026-11-12T05:10 | 14.6 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 97 | 2026-11-12T15:46 | 14.1 | 2027 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-11-13T05:58 | 13.6 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-11-13T10:13 | 13.4 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-11-13T10:17 | 13.4 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 100 | 2026-11-13T10:18 | 13.4 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-11-13T10:18 | 13.4 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 13.4 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 13.4 | 2026 |
| espn_wnba_draft | wehoop-wnba-data | 32 | 2026-11-13T11:16 | 13.3 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 95 | 2026-11-13T12:56 | 13.3 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 79 | 2026-11-13T13:16 | 13.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 95 | 2026-11-13T16:22 | 13.1 | 2026 |
| nhl_xg_models |  | 7 | 2026-11-13T18:11 | 13.0 |  |
| wnba_stats_matchups | wehoop-wnba-stats-data | 45 | 2026-11-21T06:29 | 5.5 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-11-22T03:42 | 4.6 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-11-22T15:02 | 4.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 77 | 2026-11-22T15:03 | 4.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-11-23T18:35 | 3.0 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-11-23T19:31 | 3.0 | 2026 |
| nfl_players | nfl-data | 5 | 2026-11-23T20:43 | 2.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-11-23T20:48 | 2.9 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-11-24T01:28 | 2.7 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-11-24T13:27 | 2.2 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-11-24T23:42 | 1.8 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-25T03:39 | 1.6 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-25T04:26 | 1.6 | 2026 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-11-25T09:28 | 1.4 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-11-25T09:29 | 1.4 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-11-25T09:30 | 1.4 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-11-25T09:31 | 1.4 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-11-25T09:32 | 1.4 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-11-25T09:34 | 1.4 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-11-25T09:35 | 1.4 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-11-25T09:36 | 1.4 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-11-25T09:37 | 1.4 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-11-25T09:39 | 1.4 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-11-25T09:40 | 1.4 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-11-25T09:41 | 1.4 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-11-25T09:42 | 1.4 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-11-25T09:43 | 1.4 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-11-25T09:44 | 1.4 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-11-25T09:45 | 1.4 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-11-25T09:46 | 1.4 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-11-25T09:47 | 1.4 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-11-25T09:48 | 1.4 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-11-25T09:55 | 1.4 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-11-25T10:06 | 1.4 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-11-25T10:16 | 1.4 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-25T10:23 | 1.4 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-11-25T10:31 | 1.4 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-25T10:38 | 1.4 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-11-25T10:47 | 1.4 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-11-25T10:55 | 1.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-11-25T11:04 | 1.3 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-25T11:12 | 1.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-11-25T11:20 | 1.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-25T11:27 | 1.3 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-25T11:35 | 1.3 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-11-25T11:44 | 1.3 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-11-25T11:52 | 1.3 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-11-25T12:06 | 1.3 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-25T12:13 | 1.3 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-11-25T12:20 | 1.3 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-11-25T12:26 | 1.3 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-11-25T12:41 | 1.3 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-11-25T12:41 | 1.3 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-11-25T12:41 | 1.3 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-11-25T12:41 | 1.3 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-11-25T12:49 | 1.3 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-11-25T12:52 | 1.3 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-11-25T12:54 | 1.3 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-11-25T12:56 | 1.3 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-11-25T12:56 | 1.3 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-11-25T12:58 | 1.3 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-11-25T13:01 | 1.3 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-11-25T13:17 | 1.2 |  |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-11-25T16:49 | 1.1 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-11-25T16:49 | 1.1 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-11-25T16:49 | 1.1 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-11-25T16:49 | 1.1 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-11-25T16:50 | 1.1 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-11-25T16:50 | 1.1 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-11-25T16:50 | 1.1 | 2026 |
| cfb_groups | sdv-reference-data | 329 | 2026-11-25T19:57 | 1.0 | 2026 |
| mbb_groups | sdv-reference-data | 67 | 2026-11-25T19:57 | 1.0 | 2027 |
| nba_groups | sdv-reference-data | 129 | 2026-11-25T19:57 | 1.0 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-11-25T19:57 | 1.0 |  |
| ncaa_softball_crosswalk |  | 5 | 2026-11-25T19:57 | 1.0 |  |
| nfl_groups | sdv-reference-data | 129 | 2026-11-25T19:57 | 1.0 | 2026 |
| nhl_groups | sdv-reference-data | 229 | 2026-11-25T19:57 | 1.0 | 2027 |
| wbb_groups | sdv-reference-data | 67 | 2026-11-25T19:57 | 1.0 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-11-25T19:57 | 1.0 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 98 | 2026-11-25T19:57 | 1.0 | 2026 |
| mbb_ratings | hoopR-mbb-data | 27 | 2026-11-25T22:02 | 0.9 | 2027 |
| mbb_player_value | hoopR-mbb-data | 28 | 2026-11-25T22:02 | 0.9 | 2027 |
| wbb_ratings | wehoop-wbb-data | 24 | 2026-11-25T22:04 | 0.9 | 2027 |
| wbb_player_value | wehoop-wbb-data | 20 | 2026-11-25T22:04 | 0.9 | 2027 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-11-25T22:11 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-11-25T22:11 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-11-25T22:11 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-11-25T22:12 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-11-25T22:12 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-11-25T22:12 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-25T22:14 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-25T22:15 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-25T22:15 | 0.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-11-25T22:56 | 0.8 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-11-25T22:56 | 0.8 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-11-25T23:05 | 0.8 | 2026 |
| nfl_model_pbp | nfl-data | 33 | 2026-11-26T02:38 | 0.7 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-11-26T02:38 | 0.7 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-11-26T02:38 | 0.7 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-11-26T02:38 | 0.7 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-11-26T02:38 | 0.7 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-11-26T02:39 | 0.7 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-11-26T02:39 | 0.7 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-11-26T02:39 | 0.7 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-11-26T02:39 | 0.7 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-11-26T02:39 | 0.7 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-11-26T02:39 | 0.7 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-11-26T02:41 | 0.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-11-26T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-11-26T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-11-26T02:44 | 0.7 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-11-26T02:44 | 0.7 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-11-26T02:44 | 0.7 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-11-26T02:44 | 0.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-11-26T02:44 | 0.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-11-26T02:44 | 0.7 |  |
| nfl_paper_index_games | nfl-data | 29 | 2026-11-26T02:44 | 0.7 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-11-26T02:57 | 0.7 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-11-26T02:58 | 0.7 |  |
| nfl_team_stats | nfl-data | 5 | 2026-11-26T02:58 | 0.7 |  |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-11-26T08:03 | 0.5 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 0.5 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 0.5 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 0.5 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 0.5 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 109 | 2026-11-26T08:06 | 0.5 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 0.5 | 2027 |
| nhl_rosters | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 0.5 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-11-26T08:06 | 0.5 | 2027 |
| nba_player_impact | hoopR-nba-stats-data | 192 | 2026-11-26T09:00 | 0.4 | 2027 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-11-26T09:33 | 0.4 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-11-26T09:37 | 0.4 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-11-26T10:11 | 0.4 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 79 | 2026-11-26T11:34 | 0.3 | 2027 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 79 | 2026-11-26T11:34 | 0.3 | 2027 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 79 | 2026-11-26T11:46 | 0.3 | 2027 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-11-26T11:46 | 0.3 | 2027 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 74 | 2026-11-26T11:47 | 0.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 14 | 2026-11-26T11:48 | 0.3 | 2027 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 80 | 2026-11-26T12:00 | 0.3 | 2027 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 80 | 2026-11-26T12:01 | 0.3 | 2027 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 80 | 2026-11-26T12:01 | 0.3 | 2027 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 83 | 2026-11-26T12:03 | 0.3 | 2027 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 77 | 2026-11-26T12:04 | 0.3 | 2027 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 73 | 2026-11-26T12:09 | 0.3 | 2027 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-11-26T12:20 | 0.3 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:31 | 0.3 | 2027 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-11-26T12:31 | 0.3 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:32 | 0.3 | 2027 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:34 | 0.3 | 2027 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:35 | 0.3 | 2027 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-11-26T12:35 | 0.3 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-11-26T12:35 | 0.3 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-11-26T12:36 | 0.3 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:36 | 0.3 | 2027 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-11-26T12:36 | 0.3 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-11-26T12:36 | 0.3 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:37 | 0.3 | 2027 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-11-26T12:37 | 0.3 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:38 | 0.3 | 2027 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-11-26T12:39 | 0.3 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 82 | 2026-11-26T12:39 | 0.3 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 106 | 2026-11-26T12:39 | 0.3 | 2027 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 58 | 2026-11-26T12:40 | 0.3 | 2027 |
| espn_nba_player_boxscores | hoopR-nba-data | 106 | 2026-11-26T12:40 | 0.3 | 2027 |
| espn_nba_player_core | hoopR-nba-data | 106 | 2026-11-26T12:40 | 0.3 | 2027 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 31 | 2026-11-26T12:41 | 0.3 | 2027 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-11-26T12:41 | 0.3 | 2027 |
| espn_nba_shots | hoopR-nba-data | 83 | 2026-11-26T12:41 | 0.3 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-11-26T12:41 | 0.3 | 2027 |
| espn_nba_player_season_stats | hoopR-nba-data | 107 | 2026-11-26T12:41 | 0.3 | 2027 |
| espn_nba_team_season_stats | hoopR-nba-data | 107 | 2026-11-26T12:42 | 0.3 | 2027 |
| espn_nba_standings | hoopR-nba-data | 83 | 2026-11-26T12:42 | 0.3 | 2027 |
| espn_nba_game_rosters | hoopR-nba-data | 107 | 2026-11-26T12:42 | 0.3 | 2027 |
| espn_nba_officials | hoopR-nba-data | 107 | 2026-11-26T12:43 | 0.3 | 2027 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-11-26T12:48 | 0.3 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-11-26T12:49 | 0.3 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-11-26T12:49 | 0.3 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-11-26T12:49 | 0.3 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-11-26T12:50 | 0.3 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-11-26T12:51 | 0.3 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-11-26T12:51 | 0.3 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:51 | 0.3 | 2027 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-11-26T12:51 | 0.3 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-11-26T12:52 | 0.3 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-11-26T12:52 | 0.3 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-11-26T12:52 | 0.3 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-11-26T12:52 | 0.3 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 25 | 2026-11-26T12:52 | 0.3 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:52 | 0.3 | 2027 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-11-26T12:53 | 0.3 | 2026 |
| cfb_crosswalk | cfbfastR-cfb-data | 57 | 2026-11-26T12:53 | 0.3 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:54 | 0.3 | 2027 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:55 | 0.3 | 2027 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:56 | 0.3 | 2027 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:57 | 0.3 | 2027 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-11-26T12:57 | 0.3 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:58 | 0.3 | 2027 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 58 | 2026-11-26T12:59 | 0.3 | 2027 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 31 | 2026-11-26T13:00 | 0.3 | 2027 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-11-26T13:03 | 0.3 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-11-26T13:04 | 0.3 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 98 | 2026-11-26T15:16 | 0.2 | 2027 |
| nba_stats_pbp | hoopR-nba-stats-data | 94 | 2026-11-26T15:16 | 0.2 | 2027 |
| nba_stats_possessions | hoopR-nba-stats-data | 94 | 2026-11-26T15:16 | 0.2 | 2027 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 94 | 2026-11-26T15:16 | 0.2 | 2027 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 871 | 2026-11-26T15:18 | 0.2 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 830 | 2026-11-26T15:20 | 0.2 | 2027 |
| nba_stats_matchups | hoopR-nba-stats-data | 78 | 2026-11-26T15:20 | 0.2 | 2027 |
| nba_stats_hustle | hoopR-nba-stats-data | 94 | 2026-11-26T15:20 | 0.2 | 2027 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-11-26T15:46 | 0.1 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-11-26T15:46 | 0.1 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 34 | 2026-11-26T17:33 | 0.1 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 97 | 2026-11-26T17:33 | 0.1 | 2027 |
| nba_stats_injury_report | hoopR-nba-stats-data | 29 | 2026-11-26T17:33 | 0.1 | 2027 |
| nba_stats_lineups | hoopR-nba-stats-data | 64 | 2026-11-26T17:33 | 0.1 | 2027 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 95 | 2026-11-26T17:33 | 0.1 | 2027 |
| nba_stats_officials | hoopR-nba-stats-data | 97 | 2026-11-26T17:34 | 0.1 | 2027 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 106 | 2026-11-26T17:34 | 0.1 | 2027 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 97 | 2026-11-26T17:34 | 0.1 | 2027 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 97 | 2026-11-26T17:34 | 0.1 | 2027 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 95 | 2026-11-26T17:34 | 0.1 | 2027 |
| nba_stats_rosters | hoopR-nba-stats-data | 97 | 2026-11-26T17:35 | 0.1 | 2027 |
| nba_stats_shots | hoopR-nba-stats-data | 97 | 2026-11-26T17:35 | 0.1 | 2027 |
| nba_stats_standings | hoopR-nba-stats-data | 97 | 2026-11-26T17:35 | 0.1 | 2027 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 106 | 2026-11-26T17:35 | 0.1 | 2027 |
| nba_stats_team_game_logs | hoopR-nba-stats-data | 97 | 2026-11-26T17:36 | 0.1 | 2027 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 97 | 2026-11-26T17:36 | 0.1 | 2027 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 76 | 2026-11-26T17:40 | 0.1 | 2027 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 76 | 2026-11-26T17:41 | 0.1 | 2027 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 76 | 2026-11-26T17:42 | 0.1 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 91 | 2026-11-26T17:43 | 0.1 | 2027 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 77 | 2026-11-26T17:43 | 0.1 | 2027 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-11-26T17:44 | 0.1 | 2027 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 59 | 2026-11-26T17:45 | 0.1 | 2027 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 58 | 2026-11-26T17:45 | 0.1 | 2027 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 86 | 2026-11-26T17:46 | 0.1 | 2027 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 77 | 2026-11-26T17:46 | 0.1 | 2027 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 47 | 2026-11-26T17:47 | 0.1 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 76 | 2026-11-26T17:51 | 0.1 | 2027 |
| mbb_crosswalk | hoopR-mbb-data | 223 | 2026-11-26T18:00 | 0.1 | 2027 |
| wbb_crosswalk | wehoop-wbb-data | 175 | 2026-11-26T18:01 | 0.0 | 2027 |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-11-26T18:02 | 0.0 | 2027 |
| ncaa_baseball_teams | baseballr-data | 52 | 2026-11-26T18:52 | 0.0 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 64 | 2026-11-26T18:53 | 0.0 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 52 | 2026-11-26T18:53 | 0.0 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 56 | 2026-11-26T19:04 | 0.0 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 49 | 2026-11-26T19:04 | 0.0 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 49 | 2026-11-26T19:05 | 0.0 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 49 | 2026-11-26T19:05 | 0.0 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 49 | 2026-11-26T19:05 | 0.0 | 2026 |
| ncaa_baseball_games | baseballr-data | 49 | 2026-11-26T19:05 | 0.0 | 2026 |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-11-25 | 2026-11-26 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-11-25<br>`cfb_fpi_weekly.yml` success 2026-11-25<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` success 2026-11-04<br>`espn_daily_snapshots.yml` success 2026-11-25 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-11-23 | 2026-11-23 | 2026 | `daily_cfb.yml` success 2026-11-23 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-11-25 | 2026-11-26 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-11-26 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2026 | `espn_nfl_cron.yml` success 2026-11-26<br>`nfl_pbp_cron.yml` success 2026-11-26<br>`nfl_ratings_weekly.yml` success 2026-11-24<br>`nfl_rosters_players_cron.yml` success 2026-11-26<br>`nfl_model_pipeline.yml` success 2026-11-04 |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2026 | `daily_ngs.yml` success 2026-11-26 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `daily_mbb.yml` success 2026-11-26<br>`mbb_models_cron.yml` success 2026-11-25 |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `ncaa_mbb_models.yml` success 2026-11-04 |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `daily_nba.yml` success 2026-11-26 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `daily_nba_stats.yml` success 2026-11-26<br>`nba_models.yml` failure 2026-11-04<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `daily_wbb.yml` success 2026-11-26<br>`weekly_wbb.yml` success 2026-11-22<br>`wbb_models_cron.yml` success 2026-11-25 |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | idle | no | 2026-11-13 | 2026-11-22 | 2026 | `daily_wnba.yml` success 2026-11-26<br>`weekly_wnba.yml` success 2026-11-22<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | idle | no | 2026-10-31 | 2026-11-21 | 2026 | `daily_wnba_stats.yml` success 2026-11-20<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-11-26 | 2026-11-26 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` failure 2026-11-12 |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | fresh | yes | 2026-10-08 | 2026-11-25 | 2026 | `daily_pwhl_python.yml` success 2026-11-26<br>`pwhl_xg_cron.yml` success 2026-11-25 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | idle | no | 2026-11-26 | 2026-11-26 | 2026 | `mlb_models_cron.yml` success 2026-10-31<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-11-25 | 2026-11-25 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 117.3 |
| sportsdataverse/cfb4th | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485962) | 1.8 |
| sportsdataverse/cfb4th | pkgdown | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485900) | 1.8 |
| sportsdataverse/cfb4th | test-coverage | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485968) | 1.8 |
| sportsdataverse/cfbfastR | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/45522397467) | 1.8 |
| sportsdataverse/cfbfastR | pkgdown | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/45522337880) | 1.8 |
| sportsdataverse/cfbfastR | test-coverage | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/45522337688) | 1.8 |
| sportsdataverse/cfbfastR | url-check | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/45522337759) | 1.8 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 113.2 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 89.2 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/45415359666) | 2.2 |
| sportsdataverse/cfbplotR | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498606) | 1.8 |
| sportsdataverse/cfbplotR | pkgdown | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498961) | 1.8 |
| sportsdataverse/cfbplotR | test-coverage | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498686) | 1.8 |
| sportsdataverse/fastRhockey-nhl-data | NHL xG Model Pipeline | failure | [run](https://github.com/sportsdataverse/fastRhockey-nhl-data/actions/runs/43147042866) | 14.7 |
| sportsdataverse/hoopR-nba-raw | tests | failure | [run](https://github.com/sportsdataverse/hoopR-nba-raw/actions/runs/45818540917) | 0.3 |
| sportsdataverse/hoopR-nba-stats-data | NBA Model Datasets | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/41791350576) | 22.5 |
| sportsdataverse/hoopR-nba-stats-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/45835682844) | 0.2 |
| sportsdataverse/hoopR-nba-stats-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-raw/actions/runs/43557893472) | 12.6 |
| sportsdataverse/ncaa-mbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-mbb-hoops-raw/actions/runs/43314603538) | 13.9 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/42785104475) | 16.4 |
| sportsdataverse/ncaa-wbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/43314623437) | 13.9 |
| sportsdataverse/sdvmodels | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522579211) | 1.8 |
| sportsdataverse/sdvmodels | pkgdown | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522579185) | 1.8 |
| sportsdataverse/sdvmodels | test-coverage | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522578899) | 1.8 |
| sportsdataverse/sportsdataverse-R | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610197) | 1.8 |
| sportsdataverse/sportsdataverse-R | pkgdown | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610199) | 1.8 |
| sportsdataverse/sportsdataverse-R | test-coverage | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610121) | 1.8 |
| sportsdataverse/sportsdataverse-js | Vendor sync (sdv-py) | failure | [run](https://github.com/sportsdataverse/sportsdataverse-js/actions/runs/45305067695) | 2.7 |
| sportsdataverse/sportsdataverse-py | codegen | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45863854720) | 0.1 |
| sportsdataverse/sportsdataverse-py | live tests | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45850927595) | 0.1 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45297142863) | 2.8 |
| sportsdataverse/sportsdataverse-py | quality | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45863854329) | 0.1 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45863854266) | 0.1 |
| sportsdataverse/sportsdataverse-py | tutorials-refresh | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45298703925) | 2.8 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 91.2 |
| sportsdataverse/sportypy | docs-deploy | cancelled | [run](https://github.com/sportsdataverse/sportypy/actions/runs/43576181613) | 12.4 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 74.2 | 52.4 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 550.6 | 35.5 |  |
| sportsdataverse/sportsdataverse-js | [#136](https://github.com/sportsdataverse/sportsdataverse-js/pull/136) chore(vendor): sync sdv-py codegen YAML to 39e9f0e77c | github-actions[bot] | 9.8 | 9.8 |  |
| sportsdataverse/sportypy | [#44](https://github.com/sportsdataverse/sportypy/pull/44) build(deps): bump the actions group with 2 updates | dependabot[bot] | 4.4 | 4.4 |  |
| sportsdataverse/sportypy | [#43](https://github.com/sportsdataverse/sportypy/pull/43) build(deps-dev): bump ruff from 0.17.3 to 0.17.4 in the python-deps gr | dependabot[bot] | 11.4 | 4.4 |  |
| sportsdataverse/sdvplot | [#174](https://github.com/sportsdataverse/sdvplot/pull/174) build(deps): bump astral-sh/setup-uv from 10.3.3 to 10.4.0 in the acti | dependabot[bot] | 3.0 | 3.0 |  |
| sportsdataverse/sdvplot | [#173](https://github.com/sportsdataverse/sdvplot/pull/173) docs(tutorials): weekly refresh of executed notebook pages and home fi | github-actions[bot] | 9.8 | 2.8 |  |
| sportsdataverse/sportsdataverse-py | [#1252](https://github.com/sportsdataverse/sportsdataverse-py/pull/1252) docs(tutorials): weekly refresh of executed notebook pages | github-actions[bot] | 2.8 | 2.7 |  |
| sportsdataverse/sdvplot | [#182](https://github.com/sportsdataverse/sdvplot/pull/182) build(deps): bump the python-deps group across 1 directory with 8 upda | dependabot[bot] | 1.4 | 1.4 |  |
| sportsdataverse/sdvplot-js | [#101](https://github.com/sportsdataverse/sdvplot-js/pull/101) chore(release): version packages | github-actions[bot] | 27.6 | 0.7 |  |
| sportsdataverse/sportsdataverse-py | [#1330](https://github.com/sportsdataverse/sportsdataverse-py/pull/1330) chore(codegen): refresh R export lists and parity aliases | saiemgilani | 0.3 | 0.1 |  |
| sportsdataverse/cfbfastR-cfb-data | [#164](https://github.com/sportsdataverse/cfbfastR-cfb-data/pull/164) fix(higher_models): hierarchical gate beats the served formula; floor  | saiemgilani | 0.1 | 0.1 |  |
| sportsdataverse/wehoop | [#134](https://github.com/sportsdataverse/wehoop/pull/134) docs(load_models): complete the returns tables of the three model load | saiemgilani | 0.3 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#1329](https://github.com/sportsdataverse/sportsdataverse-py/pull/1329) fix(cfb): award the 2026 Group-of-6 bid to the highest-ranked team, ch | saiemgilani | 0.3 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#512](https://github.com/saiemgilani/game-on-paper-app/pull/512) feat(cfb): a market-aware / score-only lens switch on the game page WP | saiemgilani | 0.0 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| sportsdataverse/sportsdataverse-py | 11 | 8 |
| BillPetti/baseballr | 8 | 8 |
| sportsdataverse/hoopR-nba-data | 6 | 6 |
| sportsdataverse/sportyR | 5 | 5 |
| sportsdataverse/wehoop-wnba-data | 5 | 5 |
| saiemgilani/game-on-paper-app | 5 | 5 |
| sportsdataverse/sportsdataverse-data | 6 | 4 |
| sportsdataverse/wehoop-wbb-data | 4 | 4 |
| sportsdataverse/fastRhockey-nhl-data | 4 | 4 |
| sportsdataverse/hoopR-mbb-data | 3 | 3 |
| sportsdataverse/hoopR-nba-stats-data | 4 | 3 |
| sportsdataverse/cfbfastR-cfb-data | 4 | 3 |
| sportsdataverse/hoopR | 2 | 2 |
| sportsdataverse/.github | 4 | 2 |
| sportsdataverse/softballR | 2 | 2 |
| sportsdataverse/wehoop-wnba-stats-data | 2 | 2 |
| sportsdataverse/nfl-data | 2 | 2 |
| sportsdataverse/sportsdataverse-js | 2 | 1 |
| sportsdataverse/wehoop | 1 | 1 |
| sportsdataverse/cfbfastR | 1 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/cfb4th | 1 | 1 |
| sportsdataverse/sportypy | 1 | 1 |
| sportsdataverse/softballR-data | 1 | 1 |
| sportsdataverse/sdvmodels | 1 | 1 |
| sportsdataverse/hoopR-nba-stats-raw | 2 | 1 |
| sportsdataverse/ncaa-wbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mfb-football-data | 1 | 1 |
| sportsdataverse/baseballr-data | 1 | 0 |
| sportsdataverse/sdvplot | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 46.1 | 0.2 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 119.9 | 0.3 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 738.5 | 45.4 |
| sportsdataverse/sportsdataverse-data | wnba_stats_matchups | 388 | 2026-11-26T19:05 | 0.0 | 0.2 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.1 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 0.2 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.1 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.1 |
| sportsdataverse/sdvplot | v0.1.1 | 2026-10-26 | 0.1 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.2.0 | 2026-10-30 | 0.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.1 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.1 |
| sportsdataverse/sportsdataverse-py | v0.2.0b1 | 2026-10-26 | 0.0 |
| sportsdataverse/sportyR | v2.4.5 | 2026-10-27 | 0.1 |
| sportsdataverse/sportypy | v1.2.6 | 2026-11-14 | 0.1 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.0 |

## Unmapped release tags

8 `sportsdataverse/sportsdataverse-data` tags have no producer in `producers.json` (unattributed on purpose until the publishing code is found; never guessed).

- `phf_pbp`
- `phf_player_boxscores`
- `phf_schedules`
- `phf_team_boxscores`
- `ncaa_mhockey_groups`
- `ncaa_whockey_groups`
- `nhl_xg_models`
- `ncaa_softball_crosswalk`

## Warnings

Config and collection problems found by this run.

- none
