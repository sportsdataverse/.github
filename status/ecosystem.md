# SportsDataverse ecosystem status

_80 public repos · generated 2026-11-02T19:40Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

384 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 109.2 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 107.3 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 107.3 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 103.7 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 88.5 | 2025 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 82.5 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 82.5 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 82.5 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 82.5 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 82.5 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 82.5 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 76.3 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 76.3 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 76.3 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 76.3 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 76.3 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 76.2 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 74.8 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 74.8 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 74.7 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 74.7 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 74.7 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 74.7 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 70.7 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 70.7 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 70.5 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 70.5 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 67.4 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 67.4 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 62.0 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 62.0 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 61.0 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 61.0 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 61.0 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 61.0 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 61.0 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 61.0 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 61.0 | 2023 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 54.6 | 2026 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 36.7 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 36.7 | 2025 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 36.6 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 33.9 | 2026 |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 33.6 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 33.6 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 33.6 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 33.6 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 33.2 |  |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 25.3 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 25.3 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 25.3 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 25.3 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 25.3 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 25.3 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 25.3 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 25.3 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 25.3 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 25.3 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 25.3 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 25.3 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 25.3 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 25.3 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-11T10:41 | 22.4 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-11T10:41 | 22.4 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 22.3 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 22.3 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 22.3 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 22.3 | 2026 |
| mlb_groups | sdv-reference-data | 260 | 2026-10-11T15:00 | 22.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 22.2 |  |
| nfl_groups | sdv-reference-data | 122 | 2026-10-11T15:01 | 22.2 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 21.8 | 2025 |
| mbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 21.6 | 2027 |
| wbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 21.6 | 2027 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 21.5 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-10-12T06:59 | 21.5 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 55 | 2026-10-12T07:08 | 21.5 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-10-12T07:11 | 21.5 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-10-12T07:55 | 21.5 |  |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 21.4 |  |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-10-18T14:16 | 15.2 | 2027 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-10-20T18:14 | 13.1 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 151 | 2026-10-26T12:57 | 7.3 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 109 | 2026-10-26T13:05 | 7.3 | 2026 |
| nhl_groups | sdv-reference-data | 226 | 2026-10-26T13:34 | 7.3 | 2027 |
| nfl_players | nfl-data | 5 | 2026-10-26T16:03 | 7.2 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-10-26T16:08 | 7.1 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-10-26T19:43 | 7.0 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-10-26T23:57 | 6.8 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-27T13:13 | 6.3 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 6.1 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 6.1 | 2026 |
| nfl_model_pbp_backup_rev7_20261027 | nfl-data | 14 | 2026-10-27T18:09 | 6.1 |  |
| espn_nfl_pbp | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-10-29T03:56 | 4.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-10-29T03:57 | 4.7 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-10-29T03:58 | 4.7 | 2026 |
| nfl_paper_index_games | nfl-data | 29 | 2026-10-29T03:58 | 4.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-10-29T04:01 | 4.7 |  |
| nfl_team_summaries | nfl-data | 30 | 2026-10-29T05:21 | 4.6 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-29T05:21 | 4.6 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-29T05:21 | 4.6 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-29T05:21 | 4.6 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-29T05:22 | 4.6 | 2026 |
| nfl_model_pbp | nfl-data | 33 | 2026-10-29T05:22 | 4.6 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-10-29T05:24 | 4.6 |  |
| nfl_team_stats | nfl-data | 5 | 2026-10-29T05:24 | 4.6 |  |
| mlb_pbp | baseballr-data | 121 | 2026-10-29T12:33 | 4.3 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-29T12:34 | 4.3 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-29T12:35 | 4.3 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-29T12:35 | 4.3 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-30T03:28 | 3.7 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-30T10:42 | 3.4 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-30T10:42 | 3.4 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-30T10:42 | 3.4 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-30T10:43 | 3.4 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-30T10:44 | 3.4 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-30T10:45 | 3.4 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-30T10:45 | 3.4 | 2026 |
| mlb_statcast | baseballr-data | 40 | 2026-10-30T12:37 | 3.3 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-31T11:05 | 2.4 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 94 | 2026-10-31T11:05 | 2.4 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 97 | 2026-10-31T12:49 | 2.3 | 2027 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-10-31T12:49 | 2.3 | 2027 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-31T13:13 | 2.3 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-31T13:13 | 2.3 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-31T13:13 | 2.3 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 2.3 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-31T13:14 | 2.3 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 2.3 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-31T13:14 | 2.3 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 2.3 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 2.3 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:15 | 2.3 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:16 | 2.3 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-31T14:01 | 2.2 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-31T14:01 | 2.2 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-31T14:01 | 2.2 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-31T14:01 | 2.2 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-31T14:06 | 2.2 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-31T14:32 | 2.2 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-31T14:55 | 2.2 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-31T14:55 | 2.2 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-31T14:55 | 2.2 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-31T14:55 | 2.2 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-31T14:56 | 2.2 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-31T14:56 | 2.2 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-31T14:56 | 2.2 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-31T15:15 | 2.2 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-31T16:11 | 2.1 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-31T17:11 | 2.1 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-31T17:12 | 2.1 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-31T17:12 | 2.1 | 2026 |
| ncaa_baseball_teams | baseballr-data | 22 | 2026-10-31T17:18 | 2.1 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 61 | 2026-10-31T17:18 | 2.1 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 22 | 2026-10-31T17:18 | 2.1 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 44 | 2026-10-31T17:30 | 2.1 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 22 | 2026-10-31T17:30 | 2.1 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 22 | 2026-10-31T17:30 | 2.1 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 22 | 2026-10-31T17:30 | 2.1 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 22 | 2026-10-31T17:31 | 2.1 | 2026 |
| ncaa_baseball_games | baseballr-data | 37 | 2026-10-31T17:31 | 2.1 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-01T02:21 | 1.7 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-01T02:49 | 1.7 | 2026 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-11-01T09:04 | 1.4 | 2027 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-11-01T09:39 | 1.4 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-11-01T10:58 | 1.4 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-01T11:05 | 1.4 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-11-01T12:10 | 1.3 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-11-01T12:11 | 1.3 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-11-01T12:22 | 1.3 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-11-01T12:24 | 1.3 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-11-01T12:24 | 1.3 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-11-01T12:25 | 1.3 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-11-01T12:26 | 1.3 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-11-01T12:28 | 1.3 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-11-01T12:43 | 1.3 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-11-01T12:46 | 1.3 |  |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 58 | 2026-11-01T12:46 | 1.3 | 2027 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-11-01T13:59 | 1.2 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-11-01T18:18 | 1.1 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-11-01T18:22 | 1.1 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-11-01T18:22 | 1.1 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-11-01T18:22 | 1.1 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-11-01T18:22 | 1.1 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-11-01T18:22 | 1.1 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-11-01T18:23 | 1.1 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-01T18:25 | 1.1 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-01T18:25 | 1.1 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-01T18:25 | 1.1 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-11-01T18:45 | 1.0 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-11-01T18:46 | 1.0 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-11-01T18:46 | 1.0 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-11-02T01:54 | 0.7 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-11-02T01:54 | 0.7 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-11-02T01:54 | 0.7 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-11-02T01:56 | 0.7 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-11-02T05:17 | 0.6 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-11-02T08:02 | 0.5 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-11-02T08:02 | 0.5 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-11-02T08:02 | 0.5 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-11-02T08:03 | 0.5 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 109 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-11-02T08:04 | 0.5 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-11-02T08:05 | 0.5 | 2027 |
| nba_player_impact | hoopR-nba-stats-data | 99 | 2026-11-02T09:00 | 0.4 | 2027 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-11-02T09:28 | 0.4 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-11-02T09:30 | 0.4 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-11-02T09:31 | 0.4 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-11-02T09:32 | 0.4 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-11-02T09:32 | 0.4 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-11-02T09:34 | 0.4 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-11-02T09:35 | 0.4 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-11-02T09:36 | 0.4 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-11-02T09:37 | 0.4 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-11-02T09:38 | 0.4 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-11-02T09:39 | 0.4 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-11-02T09:40 | 0.4 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-11-02T09:41 | 0.4 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-11-02T09:42 | 0.4 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-11-02T09:43 | 0.4 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-11-02T09:44 | 0.4 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-11-02T09:45 | 0.4 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-11-02T09:46 | 0.4 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-11-02T09:47 | 0.4 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-11-02T09:53 | 0.4 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-11-02T09:59 | 0.4 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-11-02T10:05 | 0.4 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-02T10:10 | 0.4 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-11-02T10:16 | 0.4 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-02T10:21 | 0.4 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-11-02T10:27 | 0.4 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-11-02T10:32 | 0.4 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-11-02T10:38 | 0.4 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-02T10:44 | 0.4 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-02T11:02 | 0.4 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-11-02T11:08 | 0.4 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-11-02T11:21 | 0.3 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 79 | 2026-11-02T11:28 | 0.3 | 2027 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 79 | 2026-11-02T11:28 | 0.3 | 2027 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 79 | 2026-11-02T11:28 | 0.3 | 2027 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-11-02T11:29 | 0.3 | 2027 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 74 | 2026-11-02T11:29 | 0.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-11-02T11:30 | 0.3 | 2027 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 81 | 2026-11-02T11:31 | 0.3 | 2027 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 62 | 2026-11-02T11:31 | 0.3 | 2027 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-11-02T11:32 | 0.3 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 57 | 2026-11-02T11:32 | 0.3 | 2027 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 73 | 2026-11-02T11:33 | 0.3 | 2027 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-02T11:37 | 0.3 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-11-02T11:43 | 0.3 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-11-02T11:48 | 0.3 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-11-02T11:59 | 0.3 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-11-02T11:59 | 0.3 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-11-02T12:00 | 0.3 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-11-02T12:08 | 0.3 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-11-02T12:09 | 0.3 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-11-02T12:12 | 0.3 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-11-02T12:12 | 0.3 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-11-02T12:12 | 0.3 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-11-02T12:12 | 0.3 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-11-02T12:12 | 0.3 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-11-02T12:13 | 0.3 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-11-02T12:14 | 0.3 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-11-02T12:20 | 0.3 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-11-02T12:30 | 0.3 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-11-02T12:30 | 0.3 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-11-02T12:30 | 0.3 | 2026 |
| cfb_crosswalk | cfbfastR-cfb-data | 50 | 2026-11-02T12:31 | 0.3 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 82 | 2026-11-02T12:39 | 0.3 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 106 | 2026-11-02T12:39 | 0.3 | 2027 |
| espn_nba_player_boxscores | hoopR-nba-data | 106 | 2026-11-02T12:39 | 0.3 | 2027 |
| espn_nba_player_core | hoopR-nba-data | 106 | 2026-11-02T12:40 | 0.3 | 2027 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-11-02T12:41 | 0.3 | 2027 |
| espn_nba_shots | hoopR-nba-data | 83 | 2026-11-02T12:41 | 0.3 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-11-02T12:41 | 0.3 | 2027 |
| espn_nba_player_season_stats | hoopR-nba-data | 107 | 2026-11-02T12:42 | 0.3 | 2027 |
| espn_nba_team_season_stats | hoopR-nba-data | 83 | 2026-11-02T12:42 | 0.3 | 2027 |
| espn_nba_game_rosters | hoopR-nba-data | 83 | 2026-11-02T12:42 | 0.3 | 2027 |
| espn_nba_officials | hoopR-nba-data | 83 | 2026-11-02T12:43 | 0.3 | 2027 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 58 | 2026-11-02T12:50 | 0.3 | 2027 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-11-02T12:50 | 0.3 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-11-02T12:50 | 0.3 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-11-02T12:51 | 0.3 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-11-02T12:51 | 0.3 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-11-02T12:51 | 0.3 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-11-02T12:52 | 0.3 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-11-02T12:52 | 0.3 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-11-02T12:53 | 0.3 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-11-02T12:53 | 0.3 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-11-02T12:53 | 0.3 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-11-02T12:54 | 0.3 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-11-02T12:54 | 0.3 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-11-02T12:57 | 0.3 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-11-02T13:01 | 0.3 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-11-02T13:02 | 0.3 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 98 | 2026-11-02T15:15 | 0.2 | 2027 |
| nba_stats_pbp | hoopR-nba-stats-data | 94 | 2026-11-02T15:15 | 0.2 | 2027 |
| nba_stats_possessions | hoopR-nba-stats-data | 94 | 2026-11-02T15:15 | 0.2 | 2027 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 94 | 2026-11-02T15:16 | 0.2 | 2027 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 871 | 2026-11-02T15:19 | 0.2 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 830 | 2026-11-02T15:20 | 0.2 | 2027 |
| nba_stats_matchups | hoopR-nba-stats-data | 58 | 2026-11-02T15:20 | 0.2 | 2027 |
| nba_stats_hustle | hoopR-nba-stats-data | 94 | 2026-11-02T15:21 | 0.2 | 2027 |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-11-02T16:32 | 0.1 | 2027 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 34 | 2026-11-02T16:51 | 0.1 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 97 | 2026-11-02T16:51 | 0.1 | 2027 |
| nba_stats_injury_report | hoopR-nba-stats-data | 29 | 2026-11-02T16:51 | 0.1 | 2027 |
| nba_stats_lineups | hoopR-nba-stats-data | 64 | 2026-11-02T16:51 | 0.1 | 2027 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 95 | 2026-11-02T16:51 | 0.1 | 2027 |
| nba_stats_officials | hoopR-nba-stats-data | 97 | 2026-11-02T16:52 | 0.1 | 2027 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 97 | 2026-11-02T16:52 | 0.1 | 2027 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 97 | 2026-11-02T16:52 | 0.1 | 2027 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 97 | 2026-11-02T16:52 | 0.1 | 2027 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 95 | 2026-11-02T16:53 | 0.1 | 2027 |
| nba_stats_rosters | hoopR-nba-stats-data | 97 | 2026-11-02T16:53 | 0.1 | 2027 |
| nba_stats_shots | hoopR-nba-stats-data | 97 | 2026-11-02T16:54 | 0.1 | 2027 |
| nba_stats_standings | hoopR-nba-stats-data | 97 | 2026-11-02T16:55 | 0.1 | 2027 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 97 | 2026-11-02T16:55 | 0.1 | 2027 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 97 | 2026-11-02T16:55 | 0.1 | 2027 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-11-02T17:14 | 0.1 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-11-02T17:15 | 0.1 | 2026 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 75 | 2026-11-02T17:53 | 0.1 | 2027 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 75 | 2026-11-02T17:53 | 0.1 | 2027 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 73 | 2026-11-02T17:53 | 0.1 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 91 | 2026-11-02T17:54 | 0.1 | 2027 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 77 | 2026-11-02T17:54 | 0.1 | 2027 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-11-02T17:54 | 0.1 | 2027 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 52 | 2026-11-02T17:55 | 0.1 | 2027 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 71 | 2026-11-02T17:55 | 0.1 | 2027 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 74 | 2026-11-02T17:55 | 0.1 | 2027 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 40 | 2026-11-02T17:56 | 0.1 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 76 | 2026-11-02T17:57 | 0.1 | 2027 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-11-02T18:04 | 0.1 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-11-02T18:04 | 0.1 | 2026 |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-11-01<br>`cfb_fpi_weekly.yml` success 2026-11-01<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-11-01 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2026 | `daily_cfb.yml` success 2026-11-02 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-31 | 2026-11-02 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-11-02 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-10-29 | 2026-11-02 | 2026 | `espn_nfl_cron.yml` disabled 2026-10-26<br>`nfl_pbp_cron.yml` disabled 2026-10-26<br>`nfl_ratings_weekly.yml` disabled 2026-10-20<br>`nfl_rosters_players_cron.yml` disabled 2026-10-26<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2026 | `daily_ngs.yml` success 2026-11-02 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-11-02 | 2026-11-02 | 2027 | `daily_mbb.yml` success 2026-11-02<br>`mbb_models_cron.yml` failure 2026-11-01 |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-11-01 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2027 | `daily_nba.yml` success 2026-11-02 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2027 | `daily_nba_stats.yml` success 2026-11-02<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-11-02 | 2026-11-02 | 2027 | `daily_wbb.yml` success 2026-11-02<br>`weekly_wbb.yml` success 2026-11-01<br>`wbb_models_cron.yml` failure 2026-11-01 |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-11-02 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | idle | no | 2026-10-30 | 2026-11-01 | 2026 | `daily_wnba.yml` success 2026-11-02<br>`weekly_wnba.yml` success 2026-11-01<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | idle | no | 2026-10-31 | 2026-10-31 | 2026 | `daily_wnba_stats.yml` success 2026-10-31<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-11-02 | 2026-11-02 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-10-08 | 2026-11-01 | 2026 | `daily_pwhl_python.yml` success 2026-11-02<br>`pwhl_xg_cron.yml` success 2026-11-01 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | fresh | yes | 2026-10-31 | 2026-10-31 | 2026 | `mlb_models_cron.yml` success 2026-10-31<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-10-26 | 2026-10-26 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| BillPetti/baseballr | R-CMD-check | failure | [run](https://github.com/BillPetti/baseballr/actions/runs/41104260277) | 3.1 |
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 93.3 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 70.3 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 89.2 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 65.2 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/41354640849) | 0.9 |
| sportsdataverse/hoopR-mbb-data | MBB Model Datasets | failure | [run](https://github.com/sportsdataverse/hoopR-mbb-data/actions/runs/41335178888) | 1.1 |
| sportsdataverse/hoopR-nba-stats-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-raw/actions/runs/40973301004) | 3.8 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/39549673868) | 12.6 |
| sportsdataverse/sdvplotR | R-hub | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/41117062689) | 3.0 |
| sportsdataverse/sdvplotR | automation-example | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/40387157239) | 7.0 |
| sportsdataverse/sportsdataverse-baseball-data | Update Statcast PBP | failure | [run](https://github.com/sportsdataverse/sportsdataverse-baseball-data/actions/runs/41485357557) | 0.1 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 67.2 |
| sportsdataverse/wehoop-wbb-data | WBB Model Datasets | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-data/actions/runs/41335294376) | 1.1 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 57.5 | 57.5 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 50.2 | 28.4 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 526.6 | 11.5 |  |
| sportsdataverse/sportsdataverse-js | [#129](https://github.com/sportsdataverse/sportsdataverse-js/pull/129) chore(vendor): sync sdv-py codegen YAML to c2031afbc7 | github-actions[bot] | 7.0 | 7.0 |  |
| sportsdataverse/nfl-data | [#88](https://github.com/sportsdataverse/nfl-data/pull/88) fix(models): train CP from 2009; document the team-summary play set | saiemgilani | 3.7 | 3.7 |  |
| sportsdataverse/sdvplot-js | [#101](https://github.com/sportsdataverse/sdvplot-js/pull/101) chore(release): version packages | github-actions[bot] | 3.6 | 3.3 |  |
| sportsdataverse/sportypy | [#39](https://github.com/sportsdataverse/sportypy/pull/39) build(deps-dev): bump the python-deps group with 2 updates | dependabot[bot] | 1.4 | 1.4 |  |
| sportsdataverse/sportypy | [#38](https://github.com/sportsdataverse/sportypy/pull/38) build(deps): bump the actions group with 3 updates | dependabot[bot] | 1.4 | 1.4 |  |
| saiemgilani/game-on-paper-app | [#364](https://github.com/saiemgilani/game-on-paper-app/pull/364) feat(game): quarter filter on each player section (G9) | saiemgilani | 0.8 | 0.8 |  |
| saiemgilani/game-on-paper-app | [#362](https://github.com/saiemgilani/game-on-paper-app/pull/362) feat(panels): method notes on advanced panels behind the method-notes  | saiemgilani | 0.8 | 0.8 |  |
| saiemgilani/game-on-paper-app | [#367](https://github.com/saiemgilani/game-on-paper-app/pull/367) fix(players): time out stalled player reads after 10 s | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#366](https://github.com/saiemgilani/game-on-paper-app/pull/366) fix(espn): time out stalled ESPN and relay requests after 10 s per att | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#365](https://github.com/saiemgilani/game-on-paper-app/pull/365) feat(game): 'first time' final-score chip, span-stated (IF-6) | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#363](https://github.com/saiemgilani/game-on-paper-app/pull/363) feat(admin): durable per-game source override (L-sources) | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#361](https://github.com/saiemgilani/game-on-paper-app/pull/361) feat(leaderboards): all-time player leaderboards behind a preview flag | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#360](https://github.com/saiemgilani/game-on-paper-app/pull/360) feat(scoreboard): spice borders get words, behind the spice-cues previ | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#359](https://github.com/saiemgilani/game-on-paper-app/pull/359) feat(players): player compare page, cards side by side (preview) | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#358](https://github.com/saiemgilani/game-on-paper-app/pull/358) feat(seo): sitemap index with paginated player sitemaps | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#357](https://github.com/saiemgilani/game-on-paper-app/pull/357) feat(leaderboards): metric help on tap behind the metric-help preview  | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#356](https://github.com/saiemgilani/game-on-paper-app/pull/356) fix(scoreboard): compact row possession dot beside the logo on the row | saiemgilani | 0.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#344](https://github.com/saiemgilani/game-on-paper-app/pull/344) feat(wbb): women's college basketball shooting dashboards behind the w | saiemgilani | 14.4 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#343](https://github.com/saiemgilani/game-on-paper-app/pull/343) feat(wbb): women's college basketball scoreboard and game page behind  | saiemgilani | 14.5 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#342](https://github.com/saiemgilani/game-on-paper-app/pull/342) feat(mbb): men's college basketball shooting dashboards behind the mbb | saiemgilani | 14.5 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#341](https://github.com/saiemgilani/game-on-paper-app/pull/341) feat(mbb): men's college basketball scoreboard and game page behind th | saiemgilani | 14.6 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#340](https://github.com/saiemgilani/game-on-paper-app/pull/340) feat(wnba): WNBA shooting dashboards and the teams-index landing behin | saiemgilani | 14.7 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#332](https://github.com/saiemgilani/game-on-paper-app/pull/332) feat(wnba): WNBA scoreboard and game pages behind the wnba preview fla | saiemgilani | 14.8 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#324](https://github.com/saiemgilani/game-on-paper-app/pull/324) refactor(basketball): league-parameterized basketball code, NBA byte-i | saiemgilani | 15.0 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#374](https://github.com/saiemgilani/game-on-paper-app/pull/374) feat(charts): sized logo/headshot sources and a sprite-atlas helper (F | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#373](https://github.com/saiemgilani/game-on-paper-app/pull/373) feat(metrics): consume the sdv-py metric registry on the chart builder | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#372](https://github.com/saiemgilani/game-on-paper-app/pull/372) feat(team): game-set filter for the season team page's Team Stats (pre | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#371](https://github.com/saiemgilani/game-on-paper-app/pull/371) feat(coaches): Situations board behind 'coach-situations' (IF-5) | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#370](https://github.com/saiemgilani/game-on-paper-app/pull/370) feat(team): team profile as a history hub (S12, preview) | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#369](https://github.com/saiemgilani/game-on-paper-app/pull/369) feat(search): stat-threshold season search behind a preview flag (S15) | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#368](https://github.com/saiemgilani/game-on-paper-app/pull/368) feat(data-sources): public data-status table behind 'data-status' (N4) | saiemgilani | 0.6 | 0.6 | y |
| saiemgilani/game-on-paper-app | [#355](https://github.com/saiemgilani/game-on-paper-app/pull/355) fix(cache): purge the summary pages once per Data API ingest | saiemgilani | 1.1 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#377](https://github.com/saiemgilani/game-on-paper-app/pull/377) feat(playoff): CFP projection page with a simulated bracket (preview) | saiemgilani | 0.1 | 0.1 |  |
| saiemgilani/game-on-paper-app | [#376](https://github.com/saiemgilani/game-on-paper-app/pull/376) feat(about): About page with the team's bios (preview) | saiemgilani | 0.1 | 0.1 | y |
| saiemgilani/game-on-paper-app | [#375](https://github.com/saiemgilani/game-on-paper-app/pull/375) fix(coaches): read every head coach, not the first 400 | saiemgilani | 0.6 | 0.1 |  |
| sportsdataverse/sportsdataverse-py | [#1058](https://github.com/sportsdataverse/sportsdataverse-py/pull/1058) feat(cfb): 2026 CFP selection, fixed bracket, cfbseedR 0.2.0 tiebreake | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/sdvplotR | [#91](https://github.com/sportsdataverse/sdvplotR/pull/91) fix(resolve): fold team names as sdvplot does; record the sdvplot comm | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sdv-assets | [#16](https://github.com/sportsdataverse/sdv-assets/pull/16) feat(sources): junior/minor HockeyTech leagues, ESPN NBL + pooled fiba | saiemgilani | 0.0 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 8 | 8 |
| BillPetti/baseballr | 8 | 8 |
| sportsdataverse/hoopR-nba-data | 7 | 6 |
| sportsdataverse/sportyR | 5 | 5 |
| sportsdataverse/sportsdataverse-py | 6 | 5 |
| sportsdataverse/wehoop-wnba-data | 6 | 5 |
| sportsdataverse/wehoop-wbb-data | 4 | 4 |
| sportsdataverse/sdvplot | 4 | 4 |
| sportsdataverse/sportsdataverse-data | 6 | 3 |
| sportsdataverse/hoopR-mbb-data | 3 | 3 |
| sportsdataverse/fastRhockey-nhl-data | 4 | 3 |
| sportsdataverse/wehoop | 2 | 2 |
| sportsdataverse/sportypy | 2 | 2 |
| sportsdataverse/softballR | 2 | 2 |
| sportsdataverse/hoopR-nba-stats-raw | 3 | 2 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/sdvplotR | 1 | 1 |
| sportsdataverse/hoopR-nba-stats-data | 2 | 1 |
| sportsdataverse/wehoop-wnba-stats-data | 2 | 1 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 1 |
| sportsdataverse/nfl-data | 1 | 1 |
| sportsdataverse/ncaa-wbb-hoops-data | 2 | 1 |
| sportsdataverse/ncaa-mbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mfb-football-data | 1 | 1 |
| sportsdataverse/baseballr-data | 1 | 0 |
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/sdv-reference-data | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/sportsdataverse-data | nba_stats_injury_report | 384 | 2026-11-02T18:04 | 0.1 | 3.1 |
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 22.2 | 0.3 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 95.9 | 2.3 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 714.5 | 21.4 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.3 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 24.6 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.2 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.2 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.2 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.2 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.2 |
| sportsdataverse/sdvplot | v0.1.1 | 2026-10-26 | 0.2 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.2.0 | 2026-10-30 | 0.2 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.0 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.2 |
| sportsdataverse/sportsdataverse-py | v0.2.0b1 | 2026-10-26 | 0.0 |
| sportsdataverse/sportyR | v2.4.5 | 2026-10-27 | 0.2 |
| sportsdataverse/sportypy | v1.2.5 | 2026-10-30 | 0.2 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.2 |

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
