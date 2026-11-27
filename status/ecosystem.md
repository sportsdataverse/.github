# SportsDataverse ecosystem status

_80 public repos · generated 2026-11-27T19:06Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

391 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 132.3 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 132.3 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 113.5 | 2025 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 95.7 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 95.7 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 95.4 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 95.4 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 92.3 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 92.3 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 86.0 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 86.0 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 86.0 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 86.0 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 86.0 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 86.0 | 2023 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 58.2 |  |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 50.2 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 50.2 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 50.2 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 50.2 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 50.2 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 50.2 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 50.2 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 50.2 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 50.2 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 50.2 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 50.2 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 50.2 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 50.2 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 50.2 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 47.3 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 47.2 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 47.2 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 47.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 47.2 |  |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 46.8 | 2025 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 46.5 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 46.4 |  |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-10-18T14:16 | 40.2 | 2027 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-27T13:13 | 31.2 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 31.1 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-27T17:13 | 31.1 | 2026 |
| nfl_model_pbp_backup_rev7_20261027 | nfl-data | 14 | 2026-10-27T18:09 | 31.0 |  |
| mlb_pbp | baseballr-data | 121 | 2026-10-29T12:33 | 29.3 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-29T12:34 | 29.3 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-29T12:35 | 29.3 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-29T12:35 | 29.3 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-31T13:13 | 27.2 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-31T13:13 | 27.2 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-31T13:13 | 27.2 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 27.2 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-31T13:14 | 27.2 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:14 | 27.2 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-31T13:14 | 27.2 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 27.2 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-31T13:15 | 27.2 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-31T13:15 | 27.2 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-31T13:16 | 27.2 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-31T14:01 | 27.2 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-31T14:01 | 27.2 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-31T14:01 | 27.2 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-31T14:06 | 27.2 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-31T15:15 | 27.2 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-31T17:11 | 27.1 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-31T17:12 | 27.1 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-31T17:12 | 27.1 | 2026 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 58 | 2026-11-01T12:46 | 26.3 | 2027 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 58 | 2026-11-02T12:50 | 25.3 | 2027 |
| ncaa_mhockey_groups |  | 66 | 2026-11-03T00:16 | 24.8 | 2027 |
| ncaa_whockey_groups |  | 66 | 2026-11-03T00:16 | 24.8 | 2027 |
| mlb_groups | sdv-reference-data | 263 | 2026-11-03T11:20 | 24.3 | 2026 |
| wnba_groups | sdv-reference-data | 75 | 2026-11-03T11:38 | 24.3 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-04T02:47 | 23.7 | 2027 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-04T02:49 | 23.7 | 2027 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-11-08T14:06 | 19.2 | 2027 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-11-09T06:50 | 18.5 | 2026 |
| mlb_statcast | baseballr-data | 40 | 2026-11-09T13:37 | 18.2 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 186 | 2026-11-09T19:26 | 18.0 | 2026 |
| nba_current_impact | hoopR-nba-stats-data | 62 | 2026-11-12T05:10 | 15.6 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 97 | 2026-11-12T15:46 | 15.1 | 2027 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-11-13T05:58 | 14.5 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-11-13T10:13 | 14.4 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-11-13T10:17 | 14.4 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 100 | 2026-11-13T10:18 | 14.4 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-11-13T10:18 | 14.4 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 14.4 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-11-13T10:19 | 14.4 | 2026 |
| espn_wnba_draft | wehoop-wnba-data | 32 | 2026-11-13T11:16 | 14.3 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 95 | 2026-11-13T12:56 | 14.3 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 79 | 2026-11-13T13:16 | 14.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 95 | 2026-11-13T16:22 | 14.1 | 2026 |
| nhl_xg_models |  | 7 | 2026-11-13T18:11 | 14.0 |  |
| wnba_stats_matchups | wehoop-wnba-stats-data | 45 | 2026-11-21T06:29 | 6.5 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-11-22T03:42 | 5.6 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-11-22T15:02 | 5.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 77 | 2026-11-22T15:03 | 5.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-11-23T18:35 | 4.0 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-11-23T19:31 | 4.0 | 2026 |
| nfl_players | nfl-data | 5 | 2026-11-23T20:43 | 3.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-11-23T20:48 | 3.9 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-11-24T01:28 | 3.7 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-11-24T23:42 | 2.8 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-25T03:39 | 2.6 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-11-25T04:26 | 2.6 | 2026 |
| cfb_groups | sdv-reference-data | 329 | 2026-11-25T19:57 | 2.0 | 2026 |
| mbb_groups | sdv-reference-data | 67 | 2026-11-25T19:57 | 2.0 | 2027 |
| nba_groups | sdv-reference-data | 129 | 2026-11-25T19:57 | 2.0 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-11-25T19:57 | 2.0 |  |
| ncaa_softball_crosswalk |  | 5 | 2026-11-25T19:57 | 2.0 |  |
| nfl_groups | sdv-reference-data | 129 | 2026-11-25T19:57 | 2.0 | 2026 |
| nhl_groups | sdv-reference-data | 229 | 2026-11-25T19:57 | 2.0 | 2027 |
| wbb_groups | sdv-reference-data | 67 | 2026-11-25T19:57 | 2.0 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-11-25T19:57 | 2.0 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 98 | 2026-11-25T19:57 | 2.0 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-11-25T22:56 | 1.8 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-11-25T22:56 | 1.8 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-11-26T08:03 | 1.5 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-11-26T08:04 | 1.5 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-11-26T08:05 | 1.5 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 1.5 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 1.5 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 109 | 2026-11-26T08:06 | 1.5 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 1.5 | 2027 |
| nhl_rosters | fastRhockey-nhl-data | 58 | 2026-11-26T08:06 | 1.5 | 2027 |
| espn_nba_pbp | hoopR-nba-data | 82 | 2026-11-26T12:39 | 1.3 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 106 | 2026-11-26T12:39 | 1.3 | 2027 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-11-26T12:41 | 1.3 | 2027 |
| espn_nba_shots | hoopR-nba-data | 83 | 2026-11-26T12:41 | 1.3 | 2027 |
| espn_nba_team_season_stats | hoopR-nba-data | 107 | 2026-11-26T12:42 | 1.3 | 2027 |
| espn_nba_standings | hoopR-nba-data | 83 | 2026-11-26T12:42 | 1.3 | 2027 |
| espn_nba_game_rosters | hoopR-nba-data | 107 | 2026-11-26T12:42 | 1.3 | 2027 |
| espn_nba_officials | hoopR-nba-data | 107 | 2026-11-26T12:43 | 1.3 | 2027 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 34 | 2026-11-26T17:33 | 1.1 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 97 | 2026-11-26T17:33 | 1.1 | 2027 |
| nba_stats_lineups | hoopR-nba-stats-data | 64 | 2026-11-26T17:33 | 1.1 | 2027 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 95 | 2026-11-26T17:33 | 1.1 | 2027 |
| nba_stats_officials | hoopR-nba-stats-data | 97 | 2026-11-26T17:34 | 1.1 | 2027 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 106 | 2026-11-26T17:34 | 1.1 | 2027 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 95 | 2026-11-26T17:34 | 1.1 | 2027 |
| nba_stats_shots | hoopR-nba-stats-data | 97 | 2026-11-26T17:35 | 1.1 | 2027 |
| nba_stats_standings | hoopR-nba-stats-data | 97 | 2026-11-26T17:35 | 1.1 | 2027 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 106 | 2026-11-26T17:35 | 1.1 | 2027 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 97 | 2026-11-26T17:36 | 1.1 | 2027 |
| wbb_ratings | wehoop-wbb-data | 24 | 2026-11-26T22:02 | 0.9 | 2027 |
| wbb_player_value | wehoop-wbb-data | 20 | 2026-11-26T22:03 | 0.9 | 2027 |
| mbb_ratings | hoopR-mbb-data | 27 | 2026-11-26T22:03 | 0.9 | 2027 |
| mbb_player_value | hoopR-mbb-data | 28 | 2026-11-26T22:04 | 0.9 | 2027 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-11-26T22:12 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-11-26T22:12 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-11-26T22:13 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-11-26T22:13 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-11-26T22:13 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-11-26T22:13 | 0.9 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-11-26T22:14 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-26T22:15 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-26T22:15 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-11-26T22:15 | 0.9 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-11-26T22:48 | 0.8 | 2026 |
| nfl_model_pbp | nfl-data | 33 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-11-27T02:39 | 0.7 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-11-27T02:40 | 0.7 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-11-27T02:40 | 0.7 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-11-27T02:41 | 0.7 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-11-27T02:42 | 0.7 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-11-27T02:43 | 0.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-11-27T02:43 | 0.7 |  |
| nfl_paper_index_games | nfl-data | 29 | 2026-11-27T02:44 | 0.7 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-11-27T03:00 | 0.7 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-11-27T03:01 | 0.7 |  |
| nfl_team_stats | nfl-data | 5 | 2026-11-27T03:01 | 0.7 |  |
| soccer_transfermarkt |  | 11 | 2026-11-27T05:07 | 0.6 |  |
| mlb_game_state | baseballr-data | 134 | 2026-11-27T05:42 | 0.6 | 2026 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-11-27T08:03 | 0.5 | 2027 |
| nhl_pregame_snapshots | fastRhockey-nhl-data | 5 | 2026-11-27T08:03 | 0.5 | 2027 |
| nba_player_impact | hoopR-nba-stats-data | 192 | 2026-11-27T09:00 | 0.4 | 2027 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-11-27T09:27 | 0.4 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-11-27T09:29 | 0.4 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-11-27T09:30 | 0.4 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-11-27T09:31 | 0.4 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-11-27T09:32 | 0.4 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-11-27T09:34 | 0.4 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-11-27T09:35 | 0.4 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-11-27T09:36 | 0.4 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-11-27T09:37 | 0.4 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-11-27T09:37 | 0.4 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-11-27T09:39 | 0.4 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-11-27T09:40 | 0.4 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-11-27T09:41 | 0.4 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-11-27T09:41 | 0.4 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-11-27T09:42 | 0.4 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-11-27T09:43 | 0.4 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-11-27T09:44 | 0.4 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-11-27T09:45 | 0.4 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-11-27T09:46 | 0.4 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-11-27T09:47 | 0.4 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-11-27T09:54 | 0.4 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-11-27T10:03 | 0.4 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-11-27T10:11 | 0.4 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-27T10:18 | 0.4 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-11-27T10:27 | 0.4 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-27T10:34 | 0.4 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-11-27T10:43 | 0.3 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-11-27T10:52 | 0.3 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-11-27T11:00 | 0.3 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-11-27T11:08 | 0.3 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 79 | 2026-11-27T11:10 | 0.3 | 2027 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 79 | 2026-11-27T11:11 | 0.3 | 2027 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-11-27T11:16 | 0.3 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-11-27T11:23 | 0.3 | 2027 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 74 | 2026-11-27T11:24 | 0.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 14 | 2026-11-27T11:25 | 0.3 | 2027 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-11-27T11:25 | 0.3 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-27T11:34 | 0.3 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 80 | 2026-11-27T11:38 | 0.3 | 2027 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 80 | 2026-11-27T11:38 | 0.3 | 2027 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 83 | 2026-11-27T11:40 | 0.3 | 2027 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 77 | 2026-11-27T11:41 | 0.3 | 2027 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-11-27T11:42 | 0.3 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 73 | 2026-11-27T11:44 | 0.3 | 2027 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-11-27T11:51 | 0.3 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-11-27T12:06 | 0.3 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-11-27T12:14 | 0.3 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-11-27T12:22 | 0.3 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 106 | 2026-11-27T12:23 | 0.3 | 2027 |
| espn_nba_player_core | hoopR-nba-data | 106 | 2026-11-27T12:24 | 0.3 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-11-27T12:24 | 0.3 | 2027 |
| espn_nba_player_season_stats | hoopR-nba-data | 107 | 2026-11-27T12:25 | 0.3 | 2027 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-11-27T12:29 | 0.3 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:31 | 0.3 | 2027 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:32 | 0.3 | 2027 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:35 | 0.3 | 2027 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:36 | 0.3 | 2027 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:37 | 0.3 | 2027 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:38 | 0.3 | 2027 |
| espn_nfl_pbp | nfl-data | 26 | 2026-11-27T12:39 | 0.3 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-11-27T12:39 | 0.3 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:39 | 0.3 | 2027 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 58 | 2026-11-27T12:41 | 0.3 | 2027 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 31 | 2026-11-27T12:42 | 0.3 | 2027 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-11-27T12:48 | 0.3 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-11-27T12:48 | 0.3 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-11-27T12:49 | 0.3 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-11-27T12:49 | 0.3 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-11-27T12:49 | 0.3 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-11-27T12:49 | 0.3 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-11-27T12:49 | 0.3 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-11-27T12:49 | 0.3 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-11-27T12:50 | 0.3 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-11-27T12:50 | 0.3 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:51 | 0.3 | 2027 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-11-27T12:51 | 0.3 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-11-27T12:52 | 0.3 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:52 | 0.3 | 2027 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-11-27T12:52 | 0.3 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-11-27T12:52 | 0.3 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-11-27T12:53 | 0.3 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-11-27T12:53 | 0.3 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-11-27T12:53 | 0.3 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:54 | 0.3 | 2027 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:55 | 0.3 | 2027 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:56 | 0.3 | 2027 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:57 | 0.3 | 2027 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 58 | 2026-11-27T12:59 | 0.3 | 2027 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-11-27T12:59 | 0.3 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 58 | 2026-11-27T13:00 | 0.3 | 2027 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 31 | 2026-11-27T13:01 | 0.3 | 2027 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-11-27T13:02 | 0.3 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-11-27T13:02 | 0.3 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-11-27T13:04 | 0.3 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-11-27T13:04 | 0.3 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-11-27T13:05 | 0.3 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-11-27T13:06 | 0.3 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-11-27T13:07 | 0.2 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-11-27T13:07 | 0.2 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-11-27T13:07 | 0.2 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-11-27T13:08 | 0.2 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-11-27T13:08 | 0.2 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-11-27T13:08 | 0.2 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-11-27T13:08 | 0.2 | 2026 |
| cfb_team_adjustment_ledger | cfbfastR-cfb-data | 73 | 2026-11-27T13:16 | 0.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-11-27T13:17 | 0.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-11-27T13:18 | 0.2 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-11-27T13:21 | 0.2 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-11-27T13:21 | 0.2 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-11-27T13:26 | 0.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-11-27T13:36 | 0.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 25 | 2026-11-27T13:36 | 0.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-11-27T13:36 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-11-27T13:38 | 0.2 |  |
| nba_stats_schedules | hoopR-nba-stats-data | 98 | 2026-11-27T15:16 | 0.2 | 2027 |
| nba_stats_pbp | hoopR-nba-stats-data | 94 | 2026-11-27T15:16 | 0.2 | 2027 |
| nba_stats_possessions | hoopR-nba-stats-data | 94 | 2026-11-27T15:16 | 0.2 | 2027 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 94 | 2026-11-27T15:16 | 0.2 | 2027 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 871 | 2026-11-27T15:18 | 0.2 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 830 | 2026-11-27T15:18 | 0.2 | 2027 |
| nba_stats_matchups | hoopR-nba-stats-data | 78 | 2026-11-27T15:19 | 0.2 | 2027 |
| nba_stats_hustle | hoopR-nba-stats-data | 94 | 2026-11-27T15:19 | 0.2 | 2027 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-11-27T15:55 | 0.1 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-11-27T15:55 | 0.1 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-11-27T15:56 | 0.1 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-11-27T15:56 | 0.1 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-11-27T15:56 | 0.1 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-11-27T15:56 | 0.1 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-11-27T15:57 | 0.1 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-11-27T15:57 | 0.1 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-11-27T15:57 | 0.1 | 2026 |
| ncaa_baseball_teams | baseballr-data | 52 | 2026-11-27T16:03 | 0.1 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 64 | 2026-11-27T16:04 | 0.1 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 52 | 2026-11-27T16:04 | 0.1 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 56 | 2026-11-27T16:19 | 0.1 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 49 | 2026-11-27T16:19 | 0.1 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 49 | 2026-11-27T16:20 | 0.1 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 49 | 2026-11-27T16:21 | 0.1 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 49 | 2026-11-27T16:21 | 0.1 | 2026 |
| ncaa_baseball_games | baseballr-data | 49 | 2026-11-27T16:21 | 0.1 | 2026 |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-11-27T16:32 | 0.1 | 2027 |
| nba_stats_injury_report | hoopR-nba-stats-data | 29 | 2026-11-27T17:11 | 0.1 | 2027 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 97 | 2026-11-27T17:12 | 0.1 | 2027 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 97 | 2026-11-27T17:12 | 0.1 | 2027 |
| nba_stats_rosters | hoopR-nba-stats-data | 97 | 2026-11-27T17:12 | 0.1 | 2027 |
| nba_stats_team_game_logs | hoopR-nba-stats-data | 97 | 2026-11-27T17:12 | 0.1 | 2027 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 79 | 2026-11-27T17:19 | 0.1 | 2027 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 76 | 2026-11-27T17:23 | 0.1 | 2027 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 76 | 2026-11-27T17:23 | 0.1 | 2027 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 76 | 2026-11-27T17:25 | 0.1 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 91 | 2026-11-27T17:25 | 0.1 | 2027 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 77 | 2026-11-27T17:26 | 0.1 | 2027 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-11-27T17:26 | 0.1 | 2027 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 59 | 2026-11-27T17:28 | 0.1 | 2027 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 58 | 2026-11-27T17:28 | 0.1 | 2027 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 86 | 2026-11-27T17:29 | 0.1 | 2027 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 77 | 2026-11-27T17:29 | 0.1 | 2027 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 47 | 2026-11-27T17:30 | 0.1 | 2027 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 80 | 2026-11-27T17:32 | 0.1 | 2027 |
| wbb_crosswalk | wehoop-wbb-data | 175 | 2026-11-27T17:33 | 0.1 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 76 | 2026-11-27T17:35 | 0.1 | 2027 |
| mbb_crosswalk | hoopR-mbb-data | 223 | 2026-11-27T17:36 | 0.1 | 2027 |
| cfb_crosswalk | cfbfastR-cfb-data | 57 | 2026-11-27T17:59 | 0.0 | 2026 |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-11-26<br>`cfb_fpi_weekly.yml` success 2026-11-26<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` success 2026-11-04<br>`espn_daily_snapshots.yml` success 2026-11-26 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-11-23 | 2026-11-23 | 2026 | `daily_cfb.yml` success 2026-11-23 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-11-27 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2026 | `espn_nfl_cron.yml` success 2026-11-27<br>`nfl_pbp_cron.yml` success 2026-11-27<br>`nfl_ratings_weekly.yml` success 2026-11-24<br>`nfl_rosters_players_cron.yml` success 2026-11-27<br>`nfl_model_pipeline.yml` success 2026-11-04 |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2026 | `daily_ngs.yml` success 2026-11-27 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2027 | `daily_mbb.yml` success 2026-11-27<br>`mbb_models_cron.yml` success 2026-11-26 |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2027 | `ncaa_mbb_models.yml` success 2026-11-04 |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | fresh | yes | 2026-11-26 | 2026-11-27 | 2027 | `daily_nba.yml` success 2026-11-27 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2027 | `daily_nba_stats.yml` success 2026-11-27<br>`nba_models.yml` failure 2026-11-04<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2027 | `daily_wbb.yml` success 2026-11-27<br>`weekly_wbb.yml` success 2026-11-22<br>`wbb_models_cron.yml` success 2026-11-26 |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | fresh | yes | 2026-11-27 | 2026-11-27 | 2027 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | idle | no | 2026-11-13 | 2026-11-22 | 2026 | `daily_wnba.yml` success 2026-11-27<br>`weekly_wnba.yml` success 2026-11-22<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | idle | no | 2026-10-31 | 2026-11-21 | 2026 | `daily_wnba_stats.yml` success 2026-11-20<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-11-26 | 2026-11-27 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` failure 2026-11-12 |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | fresh | yes | 2026-10-08 | 2026-11-26 | 2026 | `daily_pwhl_python.yml` success 2026-11-27<br>`pwhl_xg_cron.yml` success 2026-11-26 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | idle | no | 2026-11-27 | 2026-11-27 | 2026 | `mlb_models_cron.yml` success 2026-10-31<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-11-25 | 2026-11-25 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| BillPetti/baseballr | pkgdown | failure | [run](https://github.com/BillPetti/baseballr/actions/runs/45901741512) | 0.9 |
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 118.3 |
| sportsdataverse/cfb4th | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485962) | 2.8 |
| sportsdataverse/cfb4th | pkgdown | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485900) | 2.8 |
| sportsdataverse/cfb4th | test-coverage | cancelled | [run](https://github.com/sportsdataverse/cfb4th/actions/runs/45522485968) | 2.8 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 114.2 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 90.2 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/45415359666) | 3.2 |
| sportsdataverse/cfbplotR | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498606) | 2.8 |
| sportsdataverse/cfbplotR | pkgdown | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498961) | 2.8 |
| sportsdataverse/cfbplotR | test-coverage | cancelled | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/45522498686) | 2.8 |
| sportsdataverse/fastRhockey-nhl-data | NHL xG Model Pipeline | failure | [run](https://github.com/sportsdataverse/fastRhockey-nhl-data/actions/runs/43147042866) | 15.7 |
| sportsdataverse/hoopR-nba-raw | tests | failure | [run](https://github.com/sportsdataverse/hoopR-nba-raw/actions/runs/45997646664) | 0.3 |
| sportsdataverse/hoopR-nba-stats-data | NBA Model Datasets | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/41791350576) | 23.5 |
| sportsdataverse/hoopR-nba-stats-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions/runs/45835682844) | 1.2 |
| sportsdataverse/hoopR-nba-stats-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/hoopR-nba-stats-raw/actions/runs/43557893472) | 13.6 |
| sportsdataverse/ncaa-mbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-mbb-hoops-raw/actions/runs/43314603538) | 14.9 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/42785104475) | 17.4 |
| sportsdataverse/ncaa-wbb-hoops-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/43314623437) | 14.9 |
| sportsdataverse/sdvmodels | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522579211) | 2.8 |
| sportsdataverse/sdvmodels | pkgdown | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522579185) | 2.8 |
| sportsdataverse/sdvmodels | test-coverage | cancelled | [run](https://github.com/sportsdataverse/sdvmodels/actions/runs/45522578899) | 2.8 |
| sportsdataverse/sportsdataverse-R | R-CMD-check | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610197) | 2.8 |
| sportsdataverse/sportsdataverse-R | pkgdown | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610199) | 2.8 |
| sportsdataverse/sportsdataverse-R | test-coverage | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-R/actions/runs/45522610121) | 2.8 |
| sportsdataverse/sportsdataverse-baseball-data | Update Statcast PBP | failure | [run](https://github.com/sportsdataverse/sportsdataverse-baseball-data/actions/runs/46040233412) | 0.1 |
| sportsdataverse/sportsdataverse-js | Vendor sync (sdv-py) | failure | [run](https://github.com/sportsdataverse/sportsdataverse-js/actions/runs/45305067695) | 3.7 |
| sportsdataverse/sportsdataverse-py | docs-deploy | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/46008479970) | 0.2 |
| sportsdataverse/sportsdataverse-py | live tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/46008479584) | 0.2 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45297142863) | 3.8 |
| sportsdataverse/sportsdataverse-py | quality | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/46008479487) | 0.2 |
| sportsdataverse/sportsdataverse-py | tutorials-refresh | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/45298703925) | 3.8 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 92.2 |
| sportsdataverse/sportypy | docs-deploy | cancelled | [run](https://github.com/sportsdataverse/sportypy/actions/runs/43576181613) | 13.4 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 75.2 | 53.4 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 551.6 | 36.5 |  |
| sportsdataverse/sportsdataverse-js | [#136](https://github.com/sportsdataverse/sportsdataverse-js/pull/136) chore(vendor): sync sdv-py codegen YAML to 39e9f0e77c | github-actions[bot] | 10.8 | 10.8 |  |
| sportsdataverse/sportypy | [#44](https://github.com/sportsdataverse/sportypy/pull/44) build(deps): bump the actions group with 2 updates | dependabot[bot] | 5.4 | 5.4 |  |
| sportsdataverse/sportypy | [#43](https://github.com/sportsdataverse/sportypy/pull/43) build(deps-dev): bump ruff from 0.17.3 to 0.17.4 in the python-deps gr | dependabot[bot] | 12.4 | 5.4 |  |
| sportsdataverse/sdvplot | [#174](https://github.com/sportsdataverse/sdvplot/pull/174) build(deps): bump astral-sh/setup-uv from 10.3.3 to 10.4.0 in the acti | dependabot[bot] | 4.0 | 4.0 |  |
| sportsdataverse/sdvplot | [#173](https://github.com/sportsdataverse/sdvplot/pull/173) docs(tutorials): weekly refresh of executed notebook pages and home fi | github-actions[bot] | 10.8 | 3.8 |  |
| sportsdataverse/sportsdataverse-py | [#1252](https://github.com/sportsdataverse/sportsdataverse-py/pull/1252) docs(tutorials): weekly refresh of executed notebook pages | github-actions[bot] | 3.8 | 3.7 |  |
| sportsdataverse/sdvplot | [#182](https://github.com/sportsdataverse/sdvplot/pull/182) build(deps): bump the python-deps group across 1 directory with 8 upda | dependabot[bot] | 2.4 | 2.4 |  |
| sportsdataverse/sdvplot-js | [#101](https://github.com/sportsdataverse/sdvplot-js/pull/101) chore(release): version packages | github-actions[bot] | 28.6 | 1.7 |  |
| sportsdataverse/sdvplotR | [#114](https://github.com/sportsdataverse/sdvplotR/pull/114) docs: name functions that exist in help pages and contributor docs | saiemgilani | 0.9 | 0.9 |  |
| sportsdataverse/hoopR-nba-stats-data | [#62](https://github.com/sportsdataverse/hoopR-nba-stats-data/pull/62) feat(possessions): BB-D44 2-for-1 columns on the possessions table | saiemgilani | 0.6 | 0.6 |  |
| sportsdataverse/wehoop-wnba-stats-data | [#37](https://github.com/sportsdataverse/wehoop-wnba-stats-data/pull/37) feat(possessions): BB-D44 2-for-1 columns on the possessions table | saiemgilani | 0.6 | 0.6 |  |
| sportsdataverse/sportsdataverse-py | [#1364](https://github.com/sportsdataverse/sportsdataverse-py/pull/1364) feat(game-story): hockey, baseball and soccer adapters | saiemgilani | 0.6 | 0.5 | y |
| sportsdataverse/nfl-data | [#103](https://github.com/sportsdataverse/nfl-data/pull/103) feat(team-summaries): opponent-adjusted EPA on the current fit, garbag | saiemgilani | 0.4 | 0.4 | y |

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
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 47.1 | 0.2 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 120.9 | 1.3 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 739.4 | 46.4 |
| sportsdataverse/sportsdataverse-data | soccer_transfermarkt | 391 | 2026-11-27T17:59 | 0.0 | 0.5 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.0 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 0.9 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.5 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.1 |
| sportsdataverse/sdvplot | v0.1.1 | 2026-10-26 | 0.1 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.2.0 | 2026-10-30 | 0.1 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.1 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.1 |
| sportsdataverse/sportsdataverse-py | v0.2.0b1 | 2026-10-26 | 0.1 |
| sportsdataverse/sportyR | v2.4.5 | 2026-10-27 | 0.1 |
| sportsdataverse/sportypy | v1.2.6 | 2026-11-14 | 0.1 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.1 |

## Unmapped release tags

9 `sportsdataverse/sportsdataverse-data` tags have no producer in `producers.json` (unattributed on purpose until the publishing code is found; never guessed).

- `phf_pbp`
- `phf_player_boxscores`
- `phf_schedules`
- `phf_team_boxscores`
- `ncaa_mhockey_groups`
- `ncaa_whockey_groups`
- `nhl_xg_models`
- `ncaa_softball_crosswalk`
- `soccer_transfermarkt`

## Warnings

Config and collection problems found by this run.

- none
