# SportsDataverse ecosystem status

_81 public repos · generated 2026-10-09T16:26Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

381 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| cfb_crosswalk | cfbfastR-cfb-data | 26 | 2026-06-13T08:31 | 118.3 | 2025 |
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 85.0 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 83.2 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 83.2 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 79.6 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 64.3 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 58.4 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 58.4 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 58.4 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 58.4 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 58.3 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 58.3 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:05 | 58.3 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 58.3 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 57.5 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 57.5 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 57.5 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 95 | 2026-08-13T05:20 | 57.5 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 56.9 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 56.9 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 56.9 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 56.9 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 56.9 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 56.9 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 56.9 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 56.9 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 56.8 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 52.2 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 52.2 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 52.2 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 52.2 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 52.2 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 52.2 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 52.1 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 52.1 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 50.6 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 50.6 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 50.6 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 50.6 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 50.6 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 50.6 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 46.6 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 46.6 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 46.3 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 46.3 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 43.2 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 43.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 42.9 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 42.9 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 42.9 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 42.9 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 42.9 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 42.9 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 42.9 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 42.9 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 42.9 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 37.9 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 37.9 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 37.9 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 37.9 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 37.8 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 37.8 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 37.8 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 56 | 2026-09-01T20:26 | 37.8 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 37.8 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 48 | 2026-09-02T18:05 | 36.9 | 2025 |
| nba_player_impact | hoopR-nba-stats-data | 95 | 2026-09-02T18:27 | 36.9 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 36.9 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 36.9 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 36.9 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 36.9 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 36.9 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 36.9 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 36.9 | 2023 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 30.5 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 30.5 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 30.5 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 30.5 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 30.5 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 30.5 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-09-09T04:42 | 30.5 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 30.5 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 30.5 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-09-09T05:16 | 30.5 | 2026 |
| espn_nba_team_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 30.5 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 30.5 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 79 | 2026-09-09T05:18 | 30.5 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 30.5 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 30.5 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 30.5 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 30.5 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 30.5 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 30.5 | 2026 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-09-09T05:43 | 30.4 | 2027 |
| cfb_model_artifacts | cfbfastR-cfb-data | 25 | 2026-09-09T14:13 | 30.1 |  |
| mlb_pitches | baseballr-data | 121 | 2026-09-10T04:38 | 29.5 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-09-10T04:58 | 29.5 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-09-10T14:28 | 29.1 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-09-15T08:21 | 24.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-09-15T08:22 | 24.3 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-09-19T00:45 | 20.7 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-09-19T01:46 | 20.6 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 12.5 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 12.5 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 12.5 | 2025 |
| nfl_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 12.5 | 2026 |
| nhl_groups | sdv-reference-data | 224 | 2026-09-27T03:32 | 12.5 | 2026 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 12.5 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 94 | 2026-09-27T10:25 | 12.3 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 82 | 2026-09-27T10:26 | 12.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-09-27T19:55 | 11.9 |  |
| mbb_groups | sdv-reference-data | 60 | 2026-09-28T13:33 | 11.1 | 2027 |
| mlb_groups | sdv-reference-data | 260 | 2026-09-28T13:34 | 11.1 | 2026 |
| wbb_groups | sdv-reference-data | 60 | 2026-09-28T13:34 | 11.1 | 2027 |
| wnba_crosswalk | wehoop-wnba-data | 16 | 2026-09-29T10:43 | 10.2 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 9.7 | 2026 |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 9.5 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 9.5 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 9.5 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 9.5 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 9.1 |  |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-09-30T14:05 | 9.1 | 2026 |
| nba_stats_hustle | hoopR-nba-stats-data | 90 | 2026-09-30T14:24 | 9.1 | 2026 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-30T14:28 | 9.1 | 2026 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-30T14:36 | 9.1 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 8.7 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 8.7 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 8.7 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 8.7 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 8.6 | 2026 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 92 | 2026-10-01T22:01 | 7.8 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T22:33 | 7.7 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-10-04T12:11 | 5.2 | 2027 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-10-05T15:38 | 4.0 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-10-05T18:13 | 3.9 | 2026 |
| nfl_players | nfl-data | 5 | 2026-10-05T18:13 | 3.9 |  |
| nfl_player_stats | nfl-data | 5 | 2026-10-05T18:14 | 3.9 |  |
| nfl_team_stats | nfl-data | 5 | 2026-10-05T18:15 | 3.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-10-05T18:18 | 3.9 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-10-05T21:24 | 3.8 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-10-06T19:16 | 2.9 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-06T23:26 | 2.7 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-10-06T23:26 | 2.7 | 2026 |
| nba_crosswalk | hoopR-nba-data | 25 | 2026-10-07T11:34 | 2.2 | 2027 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 1.1 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 1.1 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 1.1 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 1.1 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 1.1 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 1.1 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 1.1 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 1.1 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 1.1 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 1.1 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 1.1 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 1.1 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 1.1 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 1.1 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:37 | 1.1 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-08T17:55 | 0.9 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-08T18:49 | 0.9 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-08T18:50 | 0.9 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-08T18:51 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-10-08T19:11 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-10-08T19:12 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-10-08T19:12 | 0.9 | 2027 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-10-08T19:12 | 0.9 | 2026 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-10-08T19:12 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-10-08T19:12 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-10-08T19:12 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-08T19:14 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-08T19:14 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-08T19:15 | 0.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-10-08T19:39 | 0.9 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-10-08T19:39 | 0.9 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-10-09T05:32 | 0.5 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-09T05:35 | 0.5 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-09T06:06 | 0.4 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-09T06:08 | 0.4 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-09T06:09 | 0.4 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-09T06:10 | 0.4 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-09T06:13 | 0.4 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-09T06:14 | 0.4 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-09T06:15 | 0.4 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-09T06:16 | 0.4 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-09T06:16 | 0.4 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-09T06:39 | 0.4 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-09T06:48 | 0.4 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-09T06:57 | 0.4 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-09T07:07 | 0.4 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-10-09T07:16 | 0.4 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-09T07:26 | 0.4 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-10-09T07:36 | 0.4 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-10-09T07:47 | 0.4 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-10-09T08:00 | 0.4 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-09T08:01 | 0.4 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-09T08:01 | 0.4 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-09T08:01 | 0.4 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.4 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.4 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.4 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.3 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.3 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-09T08:02 | 0.3 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 67 | 2026-10-09T08:03 | 0.3 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-09T08:04 | 0.3 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-09T08:04 | 0.3 | 2027 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-09T08:15 | 0.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-10-09T08:26 | 0.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-09T08:39 | 0.3 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-09T08:50 | 0.3 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-10-09T09:02 | 0.3 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-10-09T09:13 | 0.3 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-09T09:24 | 0.3 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-10-09T09:37 | 0.3 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-09T09:51 | 0.3 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-10-09T10:07 | 0.3 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-10-09T10:18 | 0.3 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-09T10:30 | 0.2 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-09T10:40 | 0.2 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-09T10:40 | 0.2 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-09T10:41 | 0.2 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-09T10:41 | 0.2 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 85 | 2026-10-09T10:41 | 0.2 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-09T10:42 | 0.2 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-09T10:42 | 0.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-09T10:42 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-09T10:42 | 0.2 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-09T10:43 | 0.2 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-09T10:43 | 0.2 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-10-09T10:43 | 0.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-09T10:43 | 0.2 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-09T10:44 | 0.2 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 43 | 2026-10-09T10:44 | 0.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-10-09T11:08 | 0.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-10-09T11:08 | 0.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-10-09T11:17 | 0.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-10-09T11:20 | 0.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-10-09T11:23 | 0.2 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 16 | 2026-10-09T11:30 | 0.2 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-10-09T11:38 | 0.2 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-09T11:47 | 0.2 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-09T11:48 | 0.2 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-09T11:48 | 0.2 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-09T11:48 | 0.2 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-09T11:48 | 0.2 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-09T11:49 | 0.2 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-09T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-09T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-09T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-09T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-09T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-09T11:50 | 0.2 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-09T11:51 | 0.2 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-09T11:53 | 0.2 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-10-09T11:54 | 0.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-09T11:54 | 0.2 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-10-09T11:54 | 0.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-10-09T11:55 | 0.2 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-10-09T11:55 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-10-09T11:56 | 0.2 |  |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-09T11:56 | 0.2 | 2026 |
| espn_nba_schedules | hoopR-nba-data | 88 | 2026-10-09T11:56 | 0.2 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-09T11:56 | 0.2 | 2027 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-09T11:56 | 0.2 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-09T11:57 | 0.2 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-09T13:12 | 0.1 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-09T13:12 | 0.1 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-09T13:13 | 0.1 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-09T13:13 | 0.1 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-09T13:13 | 0.1 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-09T13:13 | 0.1 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-09T13:13 | 0.1 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-09T13:14 | 0.1 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-09T13:14 | 0.1 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-09T13:14 | 0.1 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-09T13:14 | 0.1 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-09T13:14 | 0.1 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-09T13:15 | 0.1 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-09T13:15 | 0.1 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-09T13:15 | 0.1 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-09T14:01 | 0.1 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-09T14:01 | 0.1 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-09T14:01 | 0.1 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-09T14:01 | 0.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-09T14:06 | 0.1 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-09T14:30 | 0.1 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-09T15:07 | 0.1 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-09T15:07 | 0.1 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-09T15:07 | 0.1 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-09T15:08 | 0.1 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-09T15:08 | 0.1 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-09T15:08 | 0.1 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-09T15:08 | 0.1 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-09T15:08 | 0.1 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-09T15:09 | 0.1 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-09T15:09 | 0.1 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-10-09T15:09 | 0.1 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-09T16:01 | 0.0 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-09T16:02 | 0.0 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-09T16:03 | 0.0 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-09T16:04 | 0.0 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-09T16:06 | 0.0 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-09T16:07 | 0.0 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-09T16:08 | 0.0 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-09T16:09 | 0.0 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-10-09T16:09 | 0.0 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-10-09T16:09 | 0.0 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-10-09T16:12 | 0.0 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-10-09T16:14 | 0.0 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-10-09T16:14 | 0.0 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-10-09T16:14 | 0.0 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-10-09T16:14 | 0.0 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-10-09T16:15 | 0.0 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-10-09T16:15 | 0.0 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-10-09T16:15 | 0.0 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-10-09T16:18 | 0.0 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-10-09T16:21 | 0.0 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-10-09T16:22 | 0.0 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-10-09T16:23 | 0.0 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-10-09T16:23 | 0.0 |  |
| nfl_paper_index_games | nfl-data | 29 | 2026-10-09T16:23 | 0.0 | 2026 |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-10-09T16:25 | 0.0 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-09T16:26 | 0.0 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-09T16:28 | 0.0 | 2026 |
| espn_cfb_player_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_cfb_team_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-10-08<br>`cfb_fpi_weekly.yml` success 2026-10-08<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-10-08 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-10-05 | 2026-10-05 | 2026 | `daily_cfb.yml` success 2026-10-05 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-09 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `espn_nfl_cron.yml` success 2026-10-06<br>`nfl_pbp_cron.yml` success 2026-10-06<br>`nfl_ratings_weekly.yml` success 2026-10-06<br>`nfl_rosters_players_cron.yml` success 2026-10-05<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `daily_ngs.yml` success 2026-10-09 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-09-19 | 2026-09-30 | 2026 | `daily_mbb.yml` skipped 2026-09-30<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-08-24 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-09-09 | 2026-10-09 | 2026 | `daily_nba.yml` success 2026-10-09 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-08-13 | 2026-10-09 | 2026 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` no runs |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-09-19 | 2026-10-04 | 2026 | `daily_wbb.yml` success 2026-09-09<br>`weekly_wbb.yml` success 2026-10-04<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-08-24 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `daily_wnba.yml` success 2026-10-09<br>`weekly_wnba.yml` success 2026-10-04<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2026 | `daily_wnba_stats.yml` success 2026-10-09<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-10-09 | 2026-10-09 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-10-08 | 2026-10-08 | 2026 | `daily_pwhl_python.yml` success 2026-10-08<br>`pwhl_xg_cron.yml` success 2026-10-08 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | stale | yes | 2026-09-10 | 2026-10-08 | 2026 | `mlb_models_cron.yml` success 2026-10-08<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-09-29 | 2026-09-29 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| BillPetti/baseballr | R-CMD-check | failure | [run](https://github.com/BillPetti/baseballr/actions/runs/37884459013) | 0.5 |
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 69.2 |
| sportsdataverse/baseballr-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/37211098016) | 5.1 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 46.2 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 65.1 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 41.1 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/36903181691) | 7.9 |
| sportsdataverse/cfbplotR | R-CMD-check | failure | [run](https://github.com/sportsdataverse/cfbplotR/actions/runs/37888457617) | 0.5 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 122.4 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/36902076422) | 7.9 |
| sportsdataverse/sportsdataverse-js | Live smoke | failure | [run](https://github.com/sportsdataverse/sportsdataverse-js/actions/runs/37356819427) | 3.9 |
| sportsdataverse/sportsdataverse-py | codegen | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37907401072) | 0.3 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37372540649) | 3.8 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37907400991) | 0.3 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 43.1 |
| sportsdataverse/wehoop-wbb-data | Weekly R/Python Output Parity | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-data/actions/runs/37368533186) | 3.8 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/25519402950) | 154.8 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 33.4 | 33.4 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 502.5 | 23.8 |  |
| sportsdataverse/sdv-assets | [#11](https://github.com/sportsdataverse/sdv-assets/pull/11) data: monthly capture 2026-10-01 | saiemgilani | 8.4 | 8.4 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 26.1 | 4.2 |  |
| saiemgilani/game-on-paper-app | [#309](https://github.com/saiemgilani/game-on-paper-app/pull/309) feat(share-card): GOP-rendered share card for every game state, with a | saiemgilani | 1.4 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#308](https://github.com/saiemgilani/game-on-paper-app/pull/308) feat(team): Results by Opponent bars on the season team page (preview) | saiemgilani | 1.4 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#307](https://github.com/saiemgilani/game-on-paper-app/pull/307) feat(team): Situational Splits section on the season team page (previe | saiemgilani | 1.4 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#306](https://github.com/saiemgilani/game-on-paper-app/pull/306) feat(game): Paper Index factor impact on Deserved Win % (preview) | saiemgilani | 1.4 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#304](https://github.com/saiemgilani/game-on-paper-app/pull/304) feat(header): typed site search in the header (preview) | saiemgilani | 1.6 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#303](https://github.com/saiemgilani/game-on-paper-app/pull/303) feat(game): average starting field position in EP units in the Drives  | saiemgilani | 1.7 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#302](https://github.com/saiemgilani/game-on-paper-app/pull/302) feat(leaderboards): last-updated stamps on the leaderboards and trends | saiemgilani | 1.7 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#301](https://github.com/saiemgilani/game-on-paper-app/pull/301) feat(game): v2 WP chart download carries its title, URL and data time | saiemgilani | 1.7 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#300](https://github.com/saiemgilani/game-on-paper-app/pull/300) feat(team): Record splits section on the season team page (preview) | saiemgilani | 1.7 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#297](https://github.com/saiemgilani/game-on-paper-app/pull/297) feat(charts): Chart Builder v2 control bar with Plot, median crosshair | saiemgilani | 4.9 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#296](https://github.com/saiemgilani/game-on-paper-app/pull/296) feat(leaderboards): nearby-rank lists on the team and player season pa | saiemgilani | 5.0 | 0.9 |  |
| saiemgilani/game-on-paper-app | [#310](https://github.com/saiemgilani/game-on-paper-app/pull/310) fix(game): close GEI on the final result, not on possession | saiemgilani | 1.4 | 0.7 |  |
| saiemgilani/game-on-paper-app | [#313](https://github.com/saiemgilani/game-on-paper-app/pull/313) fix(percentiles): player game-log cohorts, midrank ties, position perc | saiemgilani | 0.5 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#312](https://github.com/saiemgilani/game-on-paper-app/pull/312) fix(game): Binion box percentiles: per-season ladder, midrank ties, da | saiemgilani | 0.5 | 0.5 |  |
| saiemgilani/game-on-paper-app | [#305](https://github.com/saiemgilani/game-on-paper-app/pull/305) chore(python): move to polars 2.0 and sportsdataverse main | saiemgilani | 1.4 | 0.3 |  |
| sportsdataverse/hoopR | [#231](https://github.com/sportsdataverse/hoopR/pull/231) docs(nba): playbyplayv2 covers 1996-97 onward, not 2016-17 | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/wehoop | [#92](https://github.com/sportsdataverse/wehoop/pull/92) docs(wnba): period convention is halves 1997-2005, quarters from 2006 | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/cfbfastR | [#182](https://github.com/sportsdataverse/cfbfastR/pull/182) docs(models): two-point era cuts are 2006/2013/2020, matching .XPASS_E | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/softballR | [#6](https://github.com/sportsdataverse/softballR/pull/6) fix(ncaa): derive season ceilings from the calendar and the roster id  | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/sportsdataverse-py | [#738](https://github.com/sportsdataverse/sportsdataverse-py/pull/738) fix: honour the catalogued rule-change and data-format eras (WBB halve | saiemgilani | 0.1 | 0.1 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| BillPetti/baseballr | 7 | 7 |
| sportsdataverse/sportyR | 6 | 6 |
| sportsdataverse/sportsdataverse-py | 7 | 6 |
| saiemgilani/game-on-paper-app | 6 | 6 |
| sportsdataverse/wehoop-wnba-data | 3 | 2 |
| sportsdataverse/hoopR | 2 | 1 |
| sportsdataverse/cfbfastR | 1 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/sportypy | 1 | 1 |
| sportsdataverse/softballR | 1 | 1 |
| sportsdataverse/sportsdataverse-data | 1 | 1 |
| sportsdataverse/hoopR-nba-stats-data | 1 | 1 |
| sportsdataverse/wehoop-wbb-data | 1 | 1 |
| sportsdataverse/fastRhockey-nhl-data | 1 | 1 |
| sportsdataverse/nfl-data | 1 | 1 |
| sportsdataverse/sportsdataverse-js | 1 | 0 |
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/sdvplotR | 1 | 0 |
| sportsdataverse/wehoop-wnba-stats-data | 1 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |
| sportsdataverse/sdvplot | 3 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-01T01:33 | 8.6 | 0.2 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 71.8 | 0.1 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 690.3 | 920.9 |
| sportsdataverse/sportsdataverse-data | wnba_stats_rolling_windows | 381 | 2026-10-09T16:28 | 0.0 | 2.7 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.0 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 0.5 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.3 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.2 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.5 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.4 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.2 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.4 |
| sportsdataverse/sdvplot | v0.1.0 | 2026-10-05 | 0.5 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.1.0 | 2026-10-09 | 0.5 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.3 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.4 |
| sportsdataverse/sportsdataverse-py | docs-index | 2026-10-06 | 0.1 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 0.6 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 0.6 |
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
