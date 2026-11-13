# SportsDataverse ecosystem status

_80 public repos · generated 2026-11-13T17:18Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

387 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 118.2 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 118.2 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 99.4 | 2025 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 81.6 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 81.6 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 81.4 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 81.4 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 78.3 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 78.3 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 72.0 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 72.0 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 72.0 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 72.0 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 72.0 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 72.0 | 2023 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 44.1 |  |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 36.2 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 36.2 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 36.2 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 36.2 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 36.2 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 36.2 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 36.2 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 36.2 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 36.2 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 36.2 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 36.2 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 36.2 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 36.2 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 36.2 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 33.2 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 33.2 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 33.2 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 33.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 33.1 |  |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 32.7 | 2025 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 32.4 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 32.3 |  |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-10-18T14:16 | 26.1 | 2027 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-27T13:13 | 17.2 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 17.0 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 17.0 | 2026 |
| nfl_model_pbp_backup_rev7_20261027 | nfl-data | 14 | 2026-10-27T18:09 | 17.0 |  |
| mlb_pbp | baseballr-data | 121 | 2026-10-29T12:33 | 15.2 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-29T12:34 | 15.2 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-29T12:35 | 15.2 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-29T12:35 | 15.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-30T03:28 | 14.6 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-31T13:13 | 13.2 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-31T13:13 | 13.2 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-31T13:13 | 13.2 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 13.2 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-31T13:14 | 13.2 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 13.2 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-31T13:14 | 13.2 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 13.2 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 13.2 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:15 | 13.2 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:16 | 13.2 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-31T14:01 | 13.1 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-31T14:01 | 13.1 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-31T14:01 | 13.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-31T14:06 | 13.1 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-31T15:15 | 13.1 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-31T16:11 | 13.0 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-31T17:11 | 13.0 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-31T17:12 | 13.0 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-31T17:12 | 13.0 | 2026 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 58 | 2026-11-01T12:46 | 12.2 | 2027 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 58 | 2026-11-02T12:50 | 11.2 | 2027 |
| ncaa_mhockey_groups |  | 66 | 2026-11-03T00:16 | 10.7 | 2027 |
| ncaa_whockey_groups |  | 66 | 2026-11-03T00:16 | 10.7 | 2027 |
| mlb_groups | sdv-reference-data | 263 | 2026-11-03T11:20 | 10.2 | 2026 |
| nhl_groups | sdv-reference-data | 229 | 2026-11-03T11:20 | 10.2 | 2027 |
| nfl_groups | sdv-reference-data | 129 | 2026-11-03T11:37 | 10.2 | 2026 |
| wnba_groups | sdv-reference-data | 75 | 2026-11-03T11:38 | 10.2 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-04T02:47 | 9.6 | 2027 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-04T02:49 | 9.6 | 2027 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-11-08T14:02 | 5.1 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-11-08T14:06 | 5.1 | 2027 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-11-08T19:23 | 4.9 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-11-08T19:23 | 4.9 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-11-09T06:50 | 4.4 | 2026 |
| mlb_statcast | baseballr-data | 40 | 2026-11-09T13:37 | 4.2 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-11-09T18:20 | 4.0 | 2026 |
| nfl_players | nfl-data | 5 | 2026-11-09T19:20 | 3.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-11-09T19:25 | 3.9 |  |
| wnba_player_impact | wehoop-wnba-stats-data | 186 | 2026-11-09T19:26 | 3.9 | 2026 |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-11-09T23:16 | 3.8 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-11-10T20:39 | 2.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-11-11T21:03 | 1.8 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-11-11T21:03 | 1.8 | 2026 |
| nba_current_impact | hoopR-nba-stats-data | 62 | 2026-11-12T05:10 | 1.5 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 98 | 2026-11-12T15:15 | 1.1 | 2027 |
| nba_stats_pbp | hoopR-nba-stats-data | 94 | 2026-11-12T15:16 | 1.1 | 2027 |
| nba_stats_possessions | hoopR-nba-stats-data | 94 | 2026-11-12T15:16 | 1.1 | 2027 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 94 | 2026-11-12T15:16 | 1.1 | 2027 |
| nba_stats_coaches | hoopR-nba-stats-data | 97 | 2026-11-12T15:46 | 1.1 | 2027 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 34 | 2026-11-12T15:46 | 1.1 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 97 | 2026-11-12T15:46 | 1.1 | 2027 |
| nba_stats_injury_report | hoopR-nba-stats-data | 29 | 2026-11-12T15:47 | 1.1 | 2027 |
| nba_stats_lineups | hoopR-nba-stats-data | 64 | 2026-11-12T15:47 | 1.1 | 2027 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 95 | 2026-11-12T15:47 | 1.1 | 2027 |
| nba_stats_officials | hoopR-nba-stats-data | 97 | 2026-11-12T15:47 | 1.1 | 2027 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 97 | 2026-11-12T15:48 | 1.1 | 2027 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 95 | 2026-11-12T15:48 | 1.1 | 2027 |
| nba_stats_rosters | hoopR-nba-stats-data | 97 | 2026-11-12T15:48 | 1.1 | 2027 |
| nba_stats_shots | hoopR-nba-stats-data | 97 | 2026-11-12T15:49 | 1.1 | 2027 |
| nba_stats_standings | hoopR-nba-stats-data | 97 | 2026-11-12T15:49 | 1.1 | 2027 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 97 | 2026-11-12T15:49 | 1.1 | 2027 |
| mbb_ratings | hoopR-mbb-data | 27 | 2026-11-12T20:32 | 0.9 | 2027 |
| mbb_player_value | hoopR-mbb-data | 28 | 2026-11-12T20:32 | 0.9 | 2027 |
| wbb_ratings | wehoop-wbb-data | 24 | 2026-11-12T20:33 | 0.9 | 2027 |
| wbb_player_value | wehoop-wbb-data | 20 | 2026-11-12T20:33 | 0.9 | 2027 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-11-12T20:41 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-11-12T20:41 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-11-12T20:41 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-11-12T20:42 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-11-12T20:42 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-11-12T20:42 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-11-12T20:42 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-12T20:44 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-12T20:44 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-12T20:44 | 0.9 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-11-12T21:15 | 0.8 | 2026 |
| cfb_groups | sdv-reference-data | 329 | 2026-11-12T22:08 | 0.8 | 2026 |
| mbb_groups | sdv-reference-data | 67 | 2026-11-12T22:08 | 0.8 | 2027 |
| nba_groups | sdv-reference-data | 129 | 2026-11-12T22:08 | 0.8 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-11-12T22:08 | 0.8 |  |
| ncaa_softball_crosswalk |  | 5 | 2026-11-12T22:08 | 0.8 |  |
| wbb_groups | sdv-reference-data | 67 | 2026-11-12T22:08 | 0.8 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-11-12T22:08 | 0.8 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 98 | 2026-11-12T22:08 | 0.8 | 2026 |
| nfl_model_pbp | nfl-data | 33 | 2026-11-13T00:53 | 0.7 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-11-13T00:53 | 0.7 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-11-13T00:53 | 0.7 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-11-13T00:54 | 0.7 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-11-13T00:55 | 0.7 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-11-13T00:56 | 0.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-11-13T00:57 | 0.7 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-11-13T00:58 | 0.7 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-11-13T00:58 | 0.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-11-13T00:59 | 0.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-11-13T00:59 | 0.7 |  |
| nfl_paper_index_games | nfl-data | 29 | 2026-11-13T00:59 | 0.7 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-11-13T01:17 | 0.7 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-11-13T01:18 | 0.7 |  |
| nfl_team_stats | nfl-data | 5 | 2026-11-13T01:18 | 0.7 |  |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-11-13T05:58 | 0.5 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 77 | 2026-11-13T08:23 | 0.4 | 2026 |
| nba_player_impact | hoopR-nba-stats-data | 192 | 2026-11-13T09:00 | 0.3 | 2027 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-11-13T09:27 | 0.3 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-11-13T09:29 | 0.3 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-11-13T09:30 | 0.3 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-11-13T09:31 | 0.3 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-11-13T09:32 | 0.3 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-11-13T09:33 | 0.3 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-11-13T09:34 | 0.3 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-11-13T09:35 | 0.3 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-11-13T09:36 | 0.3 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-11-13T09:36 | 0.3 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-11-13T09:38 | 0.3 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-11-13T09:39 | 0.3 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-11-13T09:40 | 0.3 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-11-13T09:41 | 0.3 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-11-13T09:42 | 0.3 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-11-13T09:43 | 0.3 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 106 | 2026-11-13T09:43 | 0.3 | 2027 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-11-13T09:44 | 0.3 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 106 | 2026-11-13T09:44 | 0.3 | 2027 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-11-13T09:44 | 0.3 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-11-13T09:45 | 0.3 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-11-13T09:46 | 0.3 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-11-13T09:53 | 0.3 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-11-13T10:00 | 0.3 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-11-13T10:06 | 0.3 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-13T10:13 | 0.3 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-11-13T10:13 | 0.3 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-11-13T10:17 | 0.3 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 100 | 2026-11-13T10:18 | 0.3 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-11-13T10:18 | 0.3 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 0.3 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-11-13T10:19 | 0.3 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 0.3 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-13T10:25 | 0.3 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-11-13T10:32 | 0.3 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-11-13T10:39 | 0.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-11-13T10:46 | 0.3 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-13T10:54 | 0.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-11-13T11:01 | 0.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-13T11:07 | 0.3 | 2026 |
| nhl_xg_models |  | 7 | 2026-11-13T11:13 | 0.3 |  |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-13T11:14 | 0.3 | 2026 |
| espn_wnba_draft | wehoop-wnba-data | 32 | 2026-11-13T11:16 | 0.3 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-11-13T11:20 | 0.2 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-11-13T11:26 | 0.2 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-13T11:34 | 0.2 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-11-13T11:42 | 0.2 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-13T11:50 | 0.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 25 | 2026-11-13T11:50 | 0.2 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 61 | 2026-11-13T11:50 | 0.2 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 25 | 2026-11-13T11:51 | 0.2 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-11-13T11:57 | 0.2 | 2026 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 14 | 2026-11-13T11:59 | 0.2 | 2027 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-11-13T12:03 | 0.2 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 44 | 2026-11-13T12:04 | 0.2 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 25 | 2026-11-13T12:04 | 0.2 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 25 | 2026-11-13T12:05 | 0.2 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 25 | 2026-11-13T12:05 | 0.2 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-11-13T12:06 | 0.2 | 2027 |
| ncaa_baseball_situational_stats | baseballr-data | 25 | 2026-11-13T12:06 | 0.2 | 2026 |
| ncaa_baseball_games | baseballr-data | 37 | 2026-11-13T12:06 | 0.2 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-13T12:10 | 0.2 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 83 | 2026-11-13T12:14 | 0.2 | 2027 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 77 | 2026-11-13T12:15 | 0.2 | 2027 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-11-13T12:16 | 0.2 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-11-13T12:16 | 0.2 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-11-13T12:17 | 0.2 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-11-13T12:17 | 0.2 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-11-13T12:17 | 0.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-11-13T12:27 | 0.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-11-13T12:27 | 0.2 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-11-13T12:28 | 0.2 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-11-13T12:30 | 0.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-11-13T12:30 | 0.2 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:31 | 0.2 | 2027 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-11-13T12:31 | 0.2 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-11-13T12:31 | 0.2 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-11-13T12:31 | 0.2 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-11-13T12:31 | 0.2 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:31 | 0.2 | 2027 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-11-13T12:31 | 0.2 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-11-13T12:32 | 0.2 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 82 | 2026-11-13T12:32 | 0.2 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 106 | 2026-11-13T12:32 | 0.2 | 2027 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-11-13T12:32 | 0.2 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 106 | 2026-11-13T12:32 | 0.2 | 2027 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:33 | 0.2 | 2027 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-11-13T12:33 | 0.2 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:33 | 0.2 | 2027 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-11-13T12:33 | 0.2 | 2027 |
| espn_nba_shots | hoopR-nba-data | 83 | 2026-11-13T12:34 | 0.2 | 2027 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:34 | 0.2 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-11-13T12:34 | 0.2 | 2027 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-11-13T12:34 | 0.2 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-11-13T12:34 | 0.2 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:35 | 0.2 | 2027 |
| espn_nba_standings | hoopR-nba-data | 83 | 2026-11-13T12:35 | 0.2 | 2027 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:35 | 0.2 | 2027 |
| espn_nba_game_rosters | hoopR-nba-data | 107 | 2026-11-13T12:35 | 0.2 | 2027 |
| espn_nba_officials | hoopR-nba-data | 107 | 2026-11-13T12:36 | 0.2 | 2027 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 58 | 2026-11-13T12:36 | 0.2 | 2027 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 31 | 2026-11-13T12:37 | 0.2 | 2027 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-11-13T12:39 | 0.2 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-11-13T12:48 | 0.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-11-13T12:48 | 0.2 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-11-13T12:48 | 0.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-11-13T12:48 | 0.2 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-11-13T12:48 | 0.2 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-11-13T12:48 | 0.2 | 2026 |
| cfb_crosswalk | cfbfastR-cfb-data | 50 | 2026-11-13T12:49 | 0.2 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-11-13T12:49 | 0.2 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-11-13T12:49 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-11-13T12:49 | 0.2 |  |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-11-13T12:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-11-13T12:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-11-13T12:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-11-13T12:50 | 0.2 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:50 | 0.2 | 2027 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-11-13T12:51 | 0.2 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-11-13T12:51 | 0.2 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:51 | 0.2 | 2027 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:52 | 0.2 | 2027 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:53 | 0.2 | 2027 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-11-13T12:53 | 0.2 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:53 | 0.2 | 2027 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:54 | 0.2 | 2027 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:55 | 0.2 | 2027 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 58 | 2026-11-13T12:55 | 0.2 | 2027 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-11-13T12:56 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 95 | 2026-11-13T12:56 | 0.2 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 31 | 2026-11-13T12:56 | 0.2 | 2027 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-11-13T12:56 | 0.2 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 107 | 2026-11-13T13:00 | 0.2 | 2027 |
| espn_nba_player_core | hoopR-nba-data | 106 | 2026-11-13T13:16 | 0.2 | 2027 |
| espn_wnba_player_core | wehoop-wnba-data | 79 | 2026-11-13T13:16 | 0.2 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 97 | 2026-11-13T14:26 | 0.1 | 2027 |
| nba_stats_team_game_logs | hoopR-nba-stats-data | 97 | 2026-11-13T14:26 | 0.1 | 2027 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 80 | 2026-11-13T15:05 | 0.1 | 2027 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 871 | 2026-11-13T15:18 | 0.1 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 830 | 2026-11-13T15:20 | 0.1 | 2027 |
| nba_stats_matchups | hoopR-nba-stats-data | 58 | 2026-11-13T15:20 | 0.1 | 2027 |
| nba_stats_hustle | hoopR-nba-stats-data | 94 | 2026-11-13T15:20 | 0.1 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-11-13T15:43 | 0.1 | 2027 |
| nhl_rosters | fastRhockey-nhl-data | 58 | 2026-11-13T15:44 | 0.1 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-11-13T15:44 | 0.1 | 2027 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-11-13T15:54 | 0.1 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-11-13T15:54 | 0.1 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-11-13T15:55 | 0.1 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-11-13T15:55 | 0.1 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-11-13T15:55 | 0.1 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-11-13T15:56 | 0.1 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-11-13T15:56 | 0.1 | 2027 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-11-13T15:56 | 0.1 | 2026 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-11-13T15:56 | 0.1 | 2027 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-11-13T15:56 | 0.1 | 2026 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-11-13T15:56 | 0.1 | 2027 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-11-13T15:56 | 0.1 | 2026 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-11-13T15:56 | 0.1 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-11-13T15:57 | 0.1 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-11-13T15:57 | 0.1 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-11-13T15:57 | 0.1 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-11-13T15:58 | 0.1 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-11-13T15:58 | 0.1 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-11-13T15:58 | 0.1 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-11-13T15:58 | 0.1 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-11-13T15:59 | 0.1 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-11-13T15:59 | 0.1 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-11-13T15:59 | 0.1 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-11-13T15:59 | 0.1 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 108 | 2026-11-13T16:00 | 0.1 | 2027 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 95 | 2026-11-13T16:22 | 0.0 | 2026 |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-11-13T16:31 | 0.0 | 2027 |
| espn_nba_player_season_stats | hoopR-nba-data | 107 | 2026-11-13T16:55 | 0.0 | 2027 |
| mbb_crosswalk | hoopR-mbb-data | 178 | 2026-11-13T16:57 | 0.0 | 2027 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 73 | 2026-11-13T16:58 | 0.0 | 2027 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 76 | 2026-11-13T17:06 | 0.0 | 2027 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 76 | 2026-11-13T17:07 | 0.0 | 2027 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 79 | 2026-11-13T17:08 | 0.0 | 2027 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 76 | 2026-11-13T17:09 | 0.0 | 2027 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 79 | 2026-11-13T17:09 | 0.0 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 91 | 2026-11-13T17:09 | 0.0 | 2027 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 77 | 2026-11-13T17:10 | 0.0 | 2027 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 59 | 2026-11-13T17:12 | 0.0 | 2027 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 79 | 2026-11-13T17:12 | 0.0 | 2027 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 58 | 2026-11-13T17:12 | 0.0 | 2027 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-11-13T17:12 | 0.0 | 2027 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 86 | 2026-11-13T17:13 | 0.0 | 2027 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 74 | 2026-11-13T17:13 | 0.0 | 2027 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 77 | 2026-11-13T17:14 | 0.0 | 2027 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 47 | 2026-11-13T17:16 | 0.0 | 2027 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 80 | 2026-11-13T17:17 | 0.0 | 2027 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 80 | 2026-11-13T17:17 | 0.0 | 2027 |
| wbb_crosswalk | wehoop-wbb-data | 172 | 2026-11-13T17:18 | 0.0 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 76 | 2026-11-13T17:21 | 0.0 | 2027 |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-11-12<br>`cfb_fpi_weekly.yml` success 2026-11-12<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` success 2026-11-04<br>`espn_daily_snapshots.yml` success 2026-11-12 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-11-09 | 2026-11-09 | 2026 | `daily_cfb.yml` success 2026-11-09 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-11-13 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2026 | `espn_nfl_cron.yml` success 2026-11-13<br>`nfl_pbp_cron.yml` success 2026-11-13<br>`nfl_ratings_weekly.yml` success 2026-11-10<br>`nfl_rosters_players_cron.yml` success 2026-11-13<br>`nfl_model_pipeline.yml` success 2026-11-04 |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2026 | `daily_ngs.yml` success 2026-11-13 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `daily_mbb.yml` failure 2026-11-13<br>`mbb_models_cron.yml` success 2026-11-12 |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `ncaa_mbb_models.yml` success 2026-11-04 |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `daily_nba.yml` success 2026-11-13 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | failing | yes | 2026-11-12 | 2026-11-13 | 2027 | `daily_nba_stats.yml` failure 2026-11-13<br>`nba_models.yml` failure 2026-11-04<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `daily_wbb.yml` cancelled 2026-11-13<br>`weekly_wbb.yml` success 2026-11-08<br>`wbb_models_cron.yml` success 2026-11-12 |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | idle | no | 2026-11-13 | 2026-11-13 | 2026 | `daily_wnba.yml` success 2026-11-13<br>`weekly_wnba.yml` success 2026-11-08<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | idle | no | 2026-10-31 | 2026-11-09 | 2026 | `daily_wnba_stats.yml` success 2026-10-31<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-11-13 | 2026-11-13 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` failure 2026-11-12 |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-10-08 | 2026-11-12 | 2026 | `daily_pwhl_python.yml` success 2026-11-13<br>`pwhl_xg_cron.yml` success 2026-11-12 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | idle | no | 2026-11-13 | 2026-11-13 | 2026 | `mlb_models_cron.yml` success 2026-10-31<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-11-12 | 2026-11-12 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 104.2 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 100.1 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 76.1 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/41788852698) | 9.4 |
| sportsdataverse/fastRhockey-nhl-data | NHL xG Model Pipeline | failure | [run](https://github.com/sportsdataverse/fastRhockey-nhl-data/actions/runs/43147042866) | 1.6 |
| sportsdataverse/fastRhockey-nhl-raw | Scrape NHL Player Bio | failure | [run](https://github.com/sportsdataverse/fastRhockey-nhl-raw/actions/runs/42684942487) | 3.9 |
| sportsdataverse/hoopR-mbb-data | Update MBB Data | failure | [run](https://github.com/sportsdataverse/hoopR-mbb-data/actions/runs/43413106607) | 0.3 |
| sportsdataverse/hoopR-nba-stats-data | NBA Model Datasets | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/41791350576) | 9.4 |
| sportsdataverse/hoopR-nba-stats-data | Update NBA Stats Data | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/43448033359) | 0.1 |
| sportsdataverse/hoopR-nba-stats-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/43440140018) | 0.1 |
| sportsdataverse/hoopR-nba-stats-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-raw/actions/runs/43438543515) | 0.1 |
| sportsdataverse/ncaa-mbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-mbb-hoops-raw/actions/runs/43314603538) | 0.8 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/42785104475) | 3.4 |
| sportsdataverse/ncaa-wbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/43314623437) | 0.8 |
| sportsdataverse/sdvplot | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sdvplot/actions/runs/42715798019) | 3.8 |
| sportsdataverse/sportsdataverse-py | live tests | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/43445169556) | 0.1 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/42714671125) | 3.8 |
| sportsdataverse/sportsdataverse-py | quality | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/43452533888) | 0.1 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/43452531599) | 0.1 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 78.1 |
| sportsdataverse/wehoop-wbb-data | Update WBB Data | cancelled | [run](https://github.com/sportsdataverse/wehoop-wbb-data/actions/runs/43430626689) | 0.2 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 61.1 | 39.3 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 537.5 | 22.4 |  |
| saiemgilani/game-on-paper-app | [#394](https://github.com/saiemgilani/game-on-paper-app/pull/394) feat(basketball): college standings and bracketology page behind 'bbal | saiemgilani | 9.6 | 9.6 |  |
| saiemgilani/game-on-paper-app | [#391](https://github.com/saiemgilani/game-on-paper-app/pull/391) feat(basketball): game excitement index beside the WP chart (preview ' | saiemgilani | 9.7 | 9.6 |  |
| saiemgilani/game-on-paper-app | [#395](https://github.com/saiemgilani/game-on-paper-app/pull/395) feat(basketball): NBA and WNBA standings and playoff picture behind 'b | saiemgilani | 9.5 | 9.4 |  |
| saiemgilani/game-on-paper-app | [#405](https://github.com/saiemgilani/game-on-paper-app/pull/405) test: vitest network guard, and mocks for the 144 Data API reads it ca | saiemgilani | 8.3 | 8.3 |  |
| saiemgilani/game-on-paper-app | [#433](https://github.com/saiemgilani/game-on-paper-app/pull/433) feat(basketball): the NBA player page's Play types and Defense panels  | saiemgilani | 4.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#376](https://github.com/saiemgilani/game-on-paper-app/pull/376) feat(about): About page with the team's bios (preview) | saiemgilani | 11.0 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#375](https://github.com/saiemgilani/game-on-paper-app/pull/375) fix(coaches): read every head coach, not the first 400 | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#373](https://github.com/saiemgilani/game-on-paper-app/pull/373) feat(metrics): consume the sdv-py metric registry on the chart builder | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#372](https://github.com/saiemgilani/game-on-paper-app/pull/372) feat(team): game-set filter for the season team page's Team Stats (pre | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#371](https://github.com/saiemgilani/game-on-paper-app/pull/371) feat(coaches): Situations board behind 'coach-situations' (IF-5) | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#370](https://github.com/saiemgilani/game-on-paper-app/pull/370) feat(team): team profile as a history hub (S12, preview) | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#369](https://github.com/saiemgilani/game-on-paper-app/pull/369) feat(search): stat-threshold season search behind a preview flag (S15) | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#368](https://github.com/saiemgilani/game-on-paper-app/pull/368) feat(data-sources): public data-status table behind 'data-status' (N4) | saiemgilani | 11.5 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#367](https://github.com/saiemgilani/game-on-paper-app/pull/367) fix(players): time out stalled player reads after 10 s | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#366](https://github.com/saiemgilani/game-on-paper-app/pull/366) fix(espn): time out stalled ESPN and relay requests after 10 s per att | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#364](https://github.com/saiemgilani/game-on-paper-app/pull/364) feat(game): quarter filter on each player section (G9) | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#363](https://github.com/saiemgilani/game-on-paper-app/pull/363) feat(admin): durable per-game source override (L-sources) | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#362](https://github.com/saiemgilani/game-on-paper-app/pull/362) feat(panels): method notes on advanced panels behind the method-notes  | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#360](https://github.com/saiemgilani/game-on-paper-app/pull/360) feat(scoreboard): spice borders get words, behind the spice-cues previ | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#358](https://github.com/saiemgilani/game-on-paper-app/pull/358) feat(seo): sitemap index with paginated player sitemaps | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#356](https://github.com/saiemgilani/game-on-paper-app/pull/356) fix(scoreboard): compact row possession dot inside the abbreviation, o | saiemgilani | 11.7 | 4.5 |  |
| saiemgilani/game-on-paper-app | [#436](https://github.com/saiemgilani/game-on-paper-app/pull/436) test(astro): fail any vitest test that reaches the network | saiemgilani | 4.4 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#374](https://github.com/saiemgilani/game-on-paper-app/pull/374) feat(charts): sized logo/headshot sources and a sprite-atlas helper (F | saiemgilani | 11.5 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#365](https://github.com/saiemgilani/game-on-paper-app/pull/365) feat(game): 'first time' final-score chip, span-stated (IF-6) | saiemgilani | 11.7 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#361](https://github.com/saiemgilani/game-on-paper-app/pull/361) feat(leaderboards): all-time player leaderboards behind a preview flag | saiemgilani | 11.7 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#359](https://github.com/saiemgilani/game-on-paper-app/pull/359) feat(players): player compare page, cards side by side (preview) | saiemgilani | 11.7 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#357](https://github.com/saiemgilani/game-on-paper-app/pull/357) feat(leaderboards): metric help on tap behind the metric-help preview  | saiemgilani | 11.7 | 4.4 |  |
| saiemgilani/game-on-paper-app | [#355](https://github.com/saiemgilani/game-on-paper-app/pull/355) fix(cache): purge the summary pages once per Data API ingest | saiemgilani | 12.0 | 4.4 |  |
| sportsdataverse/sportypy | [#39](https://github.com/sportsdataverse/sportypy/pull/39) build(deps-dev): bump the python-deps group with 2 updates | dependabot[bot] | 12.3 | 3.9 |  |
| sportsdataverse/sportypy | [#38](https://github.com/sportsdataverse/sportypy/pull/38) build(deps): bump the actions group across 1 directory with 3 updates | dependabot[bot] | 12.3 | 3.9 |  |
| saiemgilani/game-on-paper-app | [#437](https://github.com/saiemgilani/game-on-paper-app/pull/437) fix(pro): re-land the Scout Pack pages (#430) on main | saiemgilani | 4.3 | 3.7 |  |
| sportsdataverse/sdvplot-js | [#101](https://github.com/sportsdataverse/sdvplot-js/pull/101) chore(release): version packages | github-actions[bot] | 14.5 | 3.6 |  |
| saiemgilani/game-on-paper-app | [#441](https://github.com/saiemgilani/game-on-paper-app/pull/441) feat(basketball): the player page's Career table with ranks and percen | saiemgilani | 3.5 | 3.5 |  |
| saiemgilani/game-on-paper-app | [#449](https://github.com/saiemgilani/game-on-paper-app/pull/449) feat(basketball): shot profile and scoring composition behind 'bball-s | saiemgilani | 3.3 | 3.3 |  |
| saiemgilani/game-on-paper-app | [#443](https://github.com/saiemgilani/game-on-paper-app/pull/443) feat(basketball): advanced player and team game logs behind 'bball-gam | saiemgilani | 3.5 | 3.3 |  |
| saiemgilani/game-on-paper-app | [#452](https://github.com/saiemgilani/game-on-paper-app/pull/452) feat(basketball): player page Situations section behind 'bball-player- | saiemgilani | 3.2 | 3.2 |  |
| saiemgilani/game-on-paper-app | [#460](https://github.com/saiemgilani/game-on-paper-app/pull/460) feat(basketball): hub standouts by game score and a WP sparkline on ea | saiemgilani | 2.9 | 2.9 |  |
| saiemgilani/game-on-paper-app | [#457](https://github.com/saiemgilani/game-on-paper-app/pull/457) feat(basketball): team schedule context and rotation behind 'bball-sch | saiemgilani | 2.9 | 2.9 |  |
| saiemgilani/game-on-paper-app | [#461](https://github.com/saiemgilani/game-on-paper-app/pull/461) feat(basketball): hub WAR leaders and a browser-kept follow-a-team car | saiemgilani | 2.9 | 2.8 |  |
| saiemgilani/game-on-paper-app | [#463](https://github.com/saiemgilani/game-on-paper-app/pull/463) feat(basketball): Season vs Current impact on the NBA player page behi | saiemgilani | 1.5 | 1.5 |  |
| saiemgilani/game-on-paper-app | [#464](https://github.com/saiemgilani/game-on-paper-app/pull/464) feat(basketball): roll the college dashboards to 2026-27 (BB-D29) | saiemgilani | 1.4 | 1.4 |  |
| saiemgilani/game-on-paper-app | [#385](https://github.com/saiemgilani/game-on-paper-app/pull/385) feat(basketball): admin source tool and source compare on the game pag | saiemgilani | 9.9 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#384](https://github.com/saiemgilani/game-on-paper-app/pull/384) feat(python): ?source= and /<league>/<id>/sources for basketball (BB-G | saiemgilani | 10.1 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#403](https://github.com/saiemgilani/game-on-paper-app/pull/403) feat(basketball): game page Impact box and Lineups used behind 'bball- | saiemgilani | 8.5 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#401](https://github.com/saiemgilani/game-on-paper-app/pull/401) feat(basketball): NBA and WNBA head-coach boards behind 'bball-coaches | saiemgilani | 8.5 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#400](https://github.com/saiemgilani/game-on-paper-app/pull/400) feat(basketball): team season block on the team pages behind 'bball-te | saiemgilani | 8.7 | 0.6 |  |
| saiemgilani/game-on-paper-app | [#414](https://github.com/saiemgilani/game-on-paper-app/pull/414) feat(basketball): impact and team views on the scatter (BB-G10, previe | saiemgilani | 8.3 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#410](https://github.com/saiemgilani/game-on-paper-app/pull/410) feat(basketball): game flow panel behind 'bball-game-flow' (BB-G28) | saiemgilani | 8.3 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#408](https://github.com/saiemgilani/game-on-paper-app/pull/408) feat(basketball): the player page's Impact panel behind 'bball-impact' | saiemgilani | 8.3 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#406](https://github.com/saiemgilani/game-on-paper-app/pull/406) feat(basketball): team strength in the team season block behind 'bball | saiemgilani | 8.3 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#404](https://github.com/saiemgilani/game-on-paper-app/pull/404) feat(basketball): points over expected on the game, team and player pa | saiemgilani | 8.4 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#399](https://github.com/saiemgilani/game-on-paper-app/pull/399) feat(basketball): rolling leaders' improvers and decliners behind 'bba | saiemgilani | 8.8 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#398](https://github.com/saiemgilani/game-on-paper-app/pull/398) feat(basketball): NBA Cup page, groups, wild cards, knockout and odds  | saiemgilani | 9.2 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#466](https://github.com/saiemgilani/game-on-paper-app/pull/466) fix(evidence): keep a clipped shot when a page is too tall to encode | saiemgilani | 0.4 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#465](https://github.com/saiemgilani/game-on-paper-app/pull/465) feat(basketball): team season shot chart with a lineup ON/OFF filter b | saiemgilani | 1.3 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#458](https://github.com/saiemgilani/game-on-paper-app/pull/458) feat(basketball): league hub with today's games, market lines and a pa | saiemgilani | 2.9 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#439](https://github.com/saiemgilani/game-on-paper-app/pull/439) fix(header): list the basketball leagues in the football league switch | saiemgilani | 3.5 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#438](https://github.com/saiemgilani/game-on-paper-app/pull/438) feat(nba): drop the Nets entry from the NBA header menu | saiemgilani | 3.6 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#417](https://github.com/saiemgilani/game-on-paper-app/pull/417) feat(basketball): play-style archetype chips on the player and team pa | saiemgilani | 8.1 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#415](https://github.com/saiemgilani/game-on-paper-app/pull/415) feat(basketball): nearby ranks on the team and player pages (BB-G12, p | saiemgilani | 8.3 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#413](https://github.com/saiemgilani/game-on-paper-app/pull/413) feat(basketball): Impact, Teams and Lineups leaderboards behind 'bball | saiemgilani | 8.3 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#411](https://github.com/saiemgilani/game-on-paper-app/pull/411) feat(basketball): player page On/Off and top WOWY partners behind 'bba | saiemgilani | 8.3 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#409](https://github.com/saiemgilani/game-on-paper-app/pull/409) feat(basketball): league small-multiples shot page behind 'bball-leagu | saiemgilani | 8.3 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#402](https://github.com/saiemgilani/game-on-paper-app/pull/402) feat(basketball): team page Lineups tab behind 'bball-lineups' (BB-G3) | saiemgilani | 8.5 | 0.4 |  |
| saiemgilani/game-on-paper-app | [#397](https://github.com/saiemgilani/game-on-paper-app/pull/397) feat(basketball): Best Games board by game excitement behind 'bball-ge | saiemgilani | 9.2 | 0.4 |  |
| sportsdataverse/sportsdataverse-py | [#1179](https://github.com/sportsdataverse/sportsdataverse-py/pull/1179) docs(nfl): clean_pbp player columns in load_nfl_model_pbp's returns ta | saiemgilani | 0.4 | 0.3 | y |
| saiemgilani/game-on-paper-app | [#432](https://github.com/saiemgilani/game-on-paper-app/pull/432) feat(basketball): player compare for the four leagues behind 'bball-co | saiemgilani | 4.7 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#423](https://github.com/saiemgilani/game-on-paper-app/pull/423) feat(basketball): WAR and VORP, and points over expected leaderboards  | saiemgilani | 7.7 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#422](https://github.com/saiemgilani/game-on-paper-app/pull/422) feat(basketball): the player page's Value panel (WAR with its interval | saiemgilani | 7.7 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#418](https://github.com/saiemgilani/game-on-paper-app/pull/418) feat(basketball): NBA game page EPV box behind 'bball-epv' (BB-G26) | saiemgilani | 7.7 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#412](https://github.com/saiemgilani/game-on-paper-app/pull/412) feat(basketball): game-set filter and last-X games on team and player  | saiemgilani | 8.3 | 0.3 |  |
| saiemgilani/game-on-paper-app | [#407](https://github.com/saiemgilani/game-on-paper-app/pull/407) feat(basketball): team page On/Off and WOWY section behind 'bball-on-o | saiemgilani | 8.3 | 0.3 |  |
| sportsdataverse/sportsdataverse-py | [#1181](https://github.com/sportsdataverse/sportsdataverse-py/pull/1181) fix(nhl): check cached xG boosters against the nhl_xg_models release m | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/fastRhockey | [#102](https://github.com/sportsdataverse/fastRhockey/pull/102) feat(xg): check cached xG models against the release manifest, not pin | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/sportsdataverse-data | [#33](https://github.com/sportsdataverse/sportsdataverse-data/pull/33) docs(notes): nhl_xg_models publisher and manifest | saiemgilani | 0.2 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#462](https://github.com/saiemgilani/game-on-paper-app/pull/462) feat(basketball): WP lenses, margin overlay and game-flow extras behin | saiemgilani | 2.8 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#459](https://github.com/saiemgilani/game-on-paper-app/pull/459) feat(basketball): lines and markets panel and the live 'at this pace'  | saiemgilani | 2.9 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#456](https://github.com/saiemgilani/game-on-paper-app/pull/456) feat(basketball): game page player props panel behind 'bball-props' (B | saiemgilani | 2.9 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#455](https://github.com/saiemgilani/game-on-paper-app/pull/455) feat(basketball): game page shift chart behind 'bball-shift-chart' (BB | saiemgilani | 3.2 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#454](https://github.com/saiemgilani/game-on-paper-app/pull/454) feat(basketball): game info, officials and availability behind 'bball- | saiemgilani | 3.2 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#453](https://github.com/saiemgilani/game-on-paper-app/pull/453) feat(basketball): EPV box for the WNBA and college behind 'bball-epv'  | saiemgilani | 3.2 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#451](https://github.com/saiemgilani/game-on-paper-app/pull/451) feat(basketball): filterable game shot charts behind 'bball-shot-filte | saiemgilani | 3.2 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#450](https://github.com/saiemgilani/game-on-paper-app/pull/450) feat(basketball): in-game 1- to 5-man lineups, on/off and an on/off pi | saiemgilani | 3.3 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#448](https://github.com/saiemgilani/game-on-paper-app/pull/448) feat(basketball): player box views and visual QA behind 'bball-player- | saiemgilani | 3.4 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#447](https://github.com/saiemgilani/game-on-paper-app/pull/447) feat(basketball): game page possession factors behind 'bball-situation | saiemgilani | 3.4 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#446](https://github.com/saiemgilani/game-on-paper-app/pull/446) feat(basketball): team stats grid with counted possessions, season con | saiemgilani | 3.4 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#445](https://github.com/saiemgilani/game-on-paper-app/pull/445) feat(basketball): Latest strip on live games behind 'bball-latest-stri | saiemgilani | 3.4 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#444](https://github.com/saiemgilani/game-on-paper-app/pull/444) feat(basketball): game page shooting signature and distance bars behin | saiemgilani | 3.4 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#442](https://github.com/saiemgilani/game-on-paper-app/pull/442) feat(basketball): game page leaders and assist web behind 'bball-game- | saiemgilani | 3.5 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#440](https://github.com/saiemgilani/game-on-paper-app/pull/440) feat(basketball): play-by-play controls behind 'bball-pbp-controls' (B | saiemgilani | 3.5 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#435](https://github.com/saiemgilani/game-on-paper-app/pull/435) feat(basketball): game page garbage-time toggle behind 'bball-garbage- | saiemgilani | 4.6 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#434](https://github.com/saiemgilani/game-on-paper-app/pull/434) feat(basketball): pregame projection and the bracket's game odds behin | saiemgilani | 4.7 | 0.2 |  |
| saiemgilani/game-on-paper-app | [#416](https://github.com/saiemgilani/game-on-paper-app/pull/416) feat(basketball): team page Situations section behind 'bball-situation | saiemgilani | 8.1 | 0.2 |  |
| sportsdataverse/fastRhockey | [#103](https://github.com/sportsdataverse/fastRhockey/pull/103) fix(nhl): rotate the rink by homeTeamDefendingSide instead of abs(x) | saiemgilani | 0.1 | 0.1 |  |
| sportsdataverse/hoopR | [#271](https://github.com/sportsdataverse/hoopR/pull/271) fix(loaders): integer NBA Stats ids in the NBA crosswalks; link every  | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/hoopR | [#270](https://github.com/sportsdataverse/hoopR/pull/270) feat(loaders): add the stats.ncaa.org to ESPN MBB crosswalk loaders | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/hoopR | [#269](https://github.com/sportsdataverse/hoopR/pull/269) feat(loaders): load the ten NBA release tags that had no hoopR loader | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/wehoop | [#126](https://github.com/sportsdataverse/wehoop/pull/126) docs(loaders): link each release loader's sportsdataverse-data tag in  | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/wehoop | [#125](https://github.com/sportsdataverse/wehoop/pull/125) feat(loaders): NCAA-ESPN WBB crosswalk loaders; integer ids on load_nc | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/wehoop | [#124](https://github.com/sportsdataverse/wehoop/pull/124) feat(loaders): add the five missing WNBA Stats release loaders | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#1187](https://github.com/sportsdataverse/sportsdataverse-py/pull/1187) docs(basketball): link release loaders to their producer dataset pages | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#1186](https://github.com/sportsdataverse/sportsdataverse-py/pull/1186) fix(basketball): integer NBA crosswalk bridge ids, WBB NCAA espn ids,  | saiemgilani | 0.0 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 8 | 8 |
| sportsdataverse/sportsdataverse-py | 10 | 7 |
| BillPetti/baseballr | 7 | 7 |
| sportsdataverse/sportyR | 5 | 5 |
| sportsdataverse/hoopR-nba-data | 6 | 5 |
| sportsdataverse/wehoop-wnba-data | 5 | 5 |
| sportsdataverse/sportsdataverse-data | 7 | 4 |
| sportsdataverse/wehoop-wbb-data | 4 | 4 |
| sportsdataverse/fastRhockey-nhl-data | 4 | 4 |
| sportsdataverse/hoopR-mbb-data | 3 | 3 |
| sportsdataverse/cfbfastR-cfb-data | 4 | 3 |
| sportsdataverse/sportypy | 2 | 2 |
| sportsdataverse/.github | 3 | 2 |
| sportsdataverse/softballR | 2 | 2 |
| sportsdataverse/hoopR-nba-stats-data | 4 | 2 |
| sportsdataverse/nfl-data | 2 | 2 |
| sportsdataverse/hoopR | 1 | 1 |
| sportsdataverse/sportsdataverse-js | 1 | 1 |
| sportsdataverse/wehoop | 1 | 1 |
| sportsdataverse/cfbfastR | 1 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/cfb4th | 1 | 1 |
| sportsdataverse/softballR-data | 1 | 1 |
| sportsdataverse/sdvmodels | 1 | 1 |
| sportsdataverse/wehoop-wnba-stats-data | 2 | 1 |
| sportsdataverse/hoopR-nba-stats-raw | 1 | 1 |
| sportsdataverse/ncaa-wbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mbb-hoops-data | 1 | 1 |
| sportsdataverse/ncaa-mfb-football-data | 1 | 1 |
| sportsdataverse/sdv-reference-data | 1 | 0 |
| sportsdataverse/sdvplot | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 33.1 | 0.1 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 106.8 | 0.8 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 725.4 | 32.3 |
| sportsdataverse/sportsdataverse-data | ncaa_whockey_groups | 387 | 2026-11-13T17:21 | 0.0 | 0.1 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.2 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 4.1 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.0 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.1 |
| sportsdataverse/sdvplot | v0.1.1 | 2026-10-26 | 0.1 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.2.0 | 2026-10-30 | 0.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.1 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.1 |
| sportsdataverse/sportsdataverse-py | v0.2.0b1 | 2026-10-26 | 0.0 |
| sportsdataverse/sportyR | v2.4.5 | 2026-10-27 | 0.1 |
| sportsdataverse/sportypy | v1.2.5 | 2026-10-30 | 0.1 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.0 |

## Unmapped release tags

8 `sportsdataverse/sportsdataverse-data` tags have no producer in `producers.json` (unattributed on purpose until the publishing code is found; never guessed).

- `phf_pbp`
- `phf_player_boxscores`
- `phf_schedules`
- `phf_team_boxscores`
- `ncaa_mhockey_groups`
- `ncaa_whockey_groups`
- `ncaa_softball_crosswalk`
- `nhl_xg_models`

## Warnings

Config and collection problems found by this run.

- none
