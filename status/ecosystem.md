# SportsDataverse ecosystem status

_80 public repos · generated 2026-10-18T13:25Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

382 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 93.9 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 92.0 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 92.0 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 88.5 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 73.2 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 67.2 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 67.2 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 67.2 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 67.2 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 67.2 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 67.2 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 67.2 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 66.3 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 66.3 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 66.3 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 95 | 2026-08-13T05:20 | 66.3 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 65.8 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 65.8 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 65.8 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 65.8 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 65.8 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 65.8 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 65.8 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 65.7 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 61.0 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 61.0 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 61.0 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 61.0 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 61.0 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 61.0 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 61.0 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 59.5 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 59.5 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 59.5 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 59.5 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 59.5 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 59.5 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 55.5 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 55.5 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 55.2 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 55.2 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 52.1 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 52.1 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 51.8 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 51.8 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 51.8 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 51.8 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 51.8 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 51.8 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 51.7 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 51.7 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 51.7 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 46.7 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 46.7 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 46.7 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 46.7 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 46.7 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 46.7 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 46.7 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 46.7 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 45.8 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 45.8 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 45.8 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 45.8 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 45.8 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 45.8 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 45.8 | 2023 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 39.4 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 39.4 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 39.4 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 39.4 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 39.4 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 39.4 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 39.4 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 39.4 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 39.3 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 39.3 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 39.3 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 39.3 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 39.3 | 2026 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 21.4 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 21.4 | 2025 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 21.4 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 18.6 | 2026 |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 18.4 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 18.3 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 18.3 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 18.3 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 18.0 |  |
| nba_stats_hustle | hoopR-nba-stats-data | 90 | 2026-09-30T14:24 | 18.0 | 2026 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-30T14:28 | 18.0 | 2026 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-30T14:36 | 18.0 | 2027 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 17.5 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 17.5 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 17.5 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 17.5 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 17.5 | 2026 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 92 | 2026-10-01T22:01 | 16.6 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T22:33 | 16.6 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:28 | 10.0 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 10.0 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 10.0 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 10.0 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:28 | 10.0 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 10.0 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 10.0 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 10.0 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 10.0 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-10-08T13:29 | 10.0 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 10.0 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 10.0 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-10-08T13:30 | 10.0 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-10-08T13:30 | 10.0 | 2026 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-10-08T13:37 | 10.0 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-09T05:35 | 9.3 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-11T10:41 | 7.1 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-11T10:41 | 7.1 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-11T10:41 | 7.1 | 2026 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-11T11:57 | 7.1 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-11T13:12 | 7.0 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-11T13:12 | 7.0 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-11T13:14 | 7.0 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-11T13:14 | 7.0 | 2026 |
| mlb_groups | sdv-reference-data | 260 | 2026-10-11T15:00 | 6.9 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-10-11T15:00 | 6.9 |  |
| nfl_groups | sdv-reference-data | 122 | 2026-10-11T15:01 | 6.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-10-11T18:36 | 6.8 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-10-11T18:37 | 6.8 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 83 | 2026-10-12T00:20 | 6.5 | 2025 |
| nba_stats_draft | hoopR-nba-stats-data | 95 | 2026-10-12T03:05 | 6.4 | 2027 |
| mbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 6.3 | 2027 |
| wbb_groups | sdv-reference-data | 60 | 2026-10-12T06:14 | 6.3 | 2027 |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-10-12T06:16 | 6.3 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-12T06:52 | 6.3 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-10-12T06:59 | 6.3 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 55 | 2026-10-12T07:08 | 6.3 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-10-12T07:11 | 6.3 | 2027 |
| ncaa_baseball_crosswalk | baseballr-data | 5 | 2026-10-12T07:55 | 6.2 |  |
| cfb_model_artifacts | cfbfastR-cfb-data | 30 | 2026-10-12T09:34 | 6.2 |  |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-12T09:35 | 6.2 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-12T09:35 | 6.2 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-12T09:36 | 6.2 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-12T09:36 | 6.2 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-12T09:36 | 6.2 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-12T09:36 | 6.2 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-12T09:37 | 6.2 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-12T09:37 | 6.2 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-12T09:37 | 6.2 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-12T09:37 | 6.2 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-10-12T12:31 | 6.0 | 2026 |
| nhl_groups | sdv-reference-data | 226 | 2026-10-12T13:32 | 6.0 | 2027 |
| nba_player_impact | hoopR-nba-stats-data | 96 | 2026-10-12T16:42 | 5.9 | 2026 |
| nfl_players | nfl-data | 5 | 2026-10-12T18:51 | 5.8 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-10-12T18:54 | 5.8 |  |
| nba_crosswalk | hoopR-nba-data | 241 | 2026-10-12T19:32 | 5.7 | 2027 |
| espn_nba_team_boxscores | hoopR-nba-data | 103 | 2026-10-12T21:27 | 5.7 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 103 | 2026-10-12T21:28 | 5.7 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 103 | 2026-10-12T21:28 | 5.7 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 104 | 2026-10-12T21:29 | 5.7 | 2026 |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-10-12T21:58 | 5.6 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 59 | 2026-10-12T23:30 | 5.6 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 151 | 2026-10-12T23:38 | 5.6 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-13T11:48 | 5.1 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-10-13T20:01 | 4.7 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-10-13T23:48 | 4.6 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 109 | 2026-10-13T23:50 | 4.6 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 232 | 2026-10-14T15:16 | 3.9 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-16T11:47 | 2.1 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-16T11:49 | 2.1 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-16T11:50 | 2.1 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-16T11:50 | 2.1 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-16T11:50 | 2.1 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-16T11:50 | 2.1 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-16T11:51 | 2.1 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-16T11:55 | 2.1 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-16T11:59 | 2.1 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-16T12:00 | 2.1 | 2026 |
| espn_nba_schedules | hoopR-nba-data | 112 | 2026-10-17T11:31 | 1.1 | 2027 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-17T14:01 | 1.0 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-17T14:01 | 1.0 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-17T14:03 | 1.0 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-17T14:16 | 1.0 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-17T14:31 | 1.0 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-17T15:03 | 0.9 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-17T15:04 | 0.9 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-17T15:05 | 0.9 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-10-17T16:10 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-10-17T16:11 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-10-17T16:11 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-10-17T16:11 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-10-17T16:11 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-10-17T16:11 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-10-17T16:11 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-17T16:14 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-17T16:14 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-17T16:14 | 0.9 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-10-17T21:56 | 0.6 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-10-17T21:56 | 0.6 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-17T21:56 | 0.6 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-17T21:57 | 0.6 | 2026 |
| nfl_defense_vs_position | nfl-data | 32 | 2026-10-17T21:57 | 0.6 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-10-17T22:03 | 0.6 | 2026 |
| espn_nfl_qa | nfl-data | 51 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 25 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-10-17T22:04 | 0.6 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 25 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 25 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-10-17T22:05 | 0.6 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-10-17T22:06 | 0.6 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-10-17T22:06 | 0.6 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-10-17T22:06 | 0.6 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-10-17T22:06 | 0.6 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-10-17T22:06 | 0.6 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-10-17T22:06 | 0.6 |  |
| nfl_paper_index_games | nfl-data | 29 | 2026-10-17T22:06 | 0.6 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-10-17T22:29 | 0.6 | 2026 |
| nfl_player_stats | nfl-data | 5 | 2026-10-17T22:29 | 0.6 |  |
| nfl_team_stats | nfl-data | 5 | 2026-10-17T22:30 | 0.6 |  |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-10-18T03:02 | 0.4 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-10-18T03:14 | 0.4 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-18T08:01 | 0.2 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-18T08:02 | 0.2 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 58 | 2026-10-18T08:03 | 0.2 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 109 | 2026-10-18T08:04 | 0.2 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-18T08:04 | 0.2 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-18T08:04 | 0.2 | 2027 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-18T08:37 | 0.2 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-10-18T09:27 | 0.2 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-18T09:48 | 0.2 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-18T10:37 | 0.1 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-10-18T10:42 | 0.1 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-10-18T10:42 | 0.1 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-10-18T10:42 | 0.1 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-18T10:43 | 0.1 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 73 | 2026-10-18T10:43 | 0.1 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-10-18T10:51 | 0.1 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-10-18T10:51 | 0.1 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-18T10:51 | 0.1 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-18T10:52 | 0.1 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-18T10:52 | 0.1 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-10-18T10:52 | 0.1 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-18T10:52 | 0.1 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 94 | 2026-10-18T10:53 | 0.1 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-18T10:53 | 0.1 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-18T10:53 | 0.1 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-10-18T10:53 | 0.1 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-18T10:54 | 0.1 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-10-18T10:54 | 0.1 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-18T10:54 | 0.1 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-10-18T10:54 | 0.1 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-10-18T10:54 | 0.1 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-10-18T10:55 | 0.1 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-10-18T10:55 | 0.1 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-10-18T10:55 | 0.1 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-10-18T10:55 | 0.1 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-10-18T10:55 | 0.1 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-10-18T10:56 | 0.1 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-10-18T10:57 | 0.1 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 43 | 2026-10-18T10:57 | 0.1 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-10-18T11:13 | 0.1 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-10-18T11:13 | 0.1 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-10-18T11:14 | 0.1 | 2026 |
| cfb_crosswalk | cfbfastR-cfb-data | 35 | 2026-10-18T11:17 | 0.1 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-10-18T11:18 | 0.1 |  |
| espn_cfb_pbp | cfbfastR-cfb-data | 73 | 2026-10-18T11:22 | 0.1 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-18T11:24 | 0.1 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-18T11:24 | 0.1 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-18T11:25 | 0.1 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-18T11:26 | 0.1 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-18T11:27 | 0.1 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-18T11:28 | 0.1 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-18T11:29 | 0.1 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-18T11:29 | 0.1 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-18T11:31 | 0.1 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-18T11:32 | 0.1 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-18T11:32 | 0.1 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-18T11:33 | 0.1 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-10-18T11:33 | 0.1 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-18T11:34 | 0.1 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-18T11:35 | 0.1 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-18T11:35 | 0.1 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-18T11:36 | 0.1 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-18T11:37 | 0.1 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-18T11:38 | 0.1 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-18T11:43 | 0.1 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-18T11:48 | 0.1 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-18T11:53 | 0.1 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-18T11:57 | 0.1 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-10-18T12:03 | 0.1 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-18T12:08 | 0.1 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-10-18T12:13 | 0.0 | 2026 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-18T12:17 | 0.0 | 2027 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-10-18T12:25 | 0.0 | 2027 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-10-18T12:25 | 0.0 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-10-18T12:25 | 0.0 | 2027 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-18T12:28 | 0.0 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-18T12:28 | 0.0 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-18T12:28 | 0.0 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-18T12:29 | 0.0 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-18T12:30 | 0.0 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-10-18T12:31 | 0.0 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-10-18T12:34 | 0.0 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-10-18T12:35 | 0.0 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-10-18T12:36 | 0.0 | 2027 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-10-18T12:36 | 0.0 | 2026 |
| mlb_pitches | baseballr-data | 121 | 2026-10-18T12:36 | 0.0 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-10-18T12:36 | 0.0 | 2026 |
| mlb_schedules | baseballr-data | 121 | 2026-10-18T12:37 | 0.0 | 2026 |
| mlb_statcast | baseballr-data | 40 | 2026-10-18T12:42 | 0.0 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-18T12:46 | 0.0 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-10-18T12:51 | 0.0 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-10-18T12:56 | 0.0 | 2026 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-10-18T12:57 | 0.0 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-18T13:01 | 0.0 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-10-18T13:06 | 0.0 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-18T13:12 | 0.0 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-10-18T13:17 | 0.0 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-18T13:18 | 0.0 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-18T13:18 | 0.0 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-18T13:18 | 0.0 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-18T13:18 | 0.0 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-18T13:19 | 0.0 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-18T13:20 | 0.0 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-18T13:20 | 0.0 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-18T13:20 | 0.0 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-10-18T13:22 | 0.0 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-10-18T13:26 | 0.0 | 2026 |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-10-17<br>`cfb_fpi_weekly.yml` success 2026-10-17<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-10-17 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `daily_cfb.yml` success 2026-10-18 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-12 | 2026-10-12 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-12 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-10-17 | 2026-10-17 | 2026 | `espn_nfl_cron.yml` success 2026-10-17<br>`nfl_pbp_cron.yml` success 2026-10-17<br>`nfl_ratings_weekly.yml` success 2026-10-13<br>`nfl_rosters_players_cron.yml` success 2026-10-17<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `daily_ngs.yml` success 2026-10-18 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-10-18 | 2026-10-18 | 2026 | `daily_mbb.yml` success 2026-10-18<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-10-12 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-10-18 | 2026-10-18 | 2026 | `daily_nba.yml` success 2026-10-18 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-08-13 | 2026-10-12 | 2026 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` success 2026-10-12 |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-10-18 | 2026-10-18 | 2026 | `daily_wbb.yml` success 2026-10-18<br>`weekly_wbb.yml` success 2026-10-18<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-10-12 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `daily_wnba.yml` success 2026-10-18<br>`weekly_wnba.yml` success 2026-10-18<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `daily_wnba_stats.yml` success 2026-10-18<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-10-08 | 2026-10-08 | 2026 | `daily_pwhl_python.yml` success 2026-10-08<br>`pwhl_xg_cron.yml` success 2026-10-08 |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | fresh | yes | 2026-10-18 | 2026-10-18 | 2026 | `mlb_models_cron.yml` success 2026-10-17<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-10-12 | 2026-10-12 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 78.1 |
| sportsdataverse/cfbfastR | R-CMD-check | failure | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/39122472932) | 0.1 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 55.1 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 74.0 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 50.0 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/36903181691) | 16.8 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 131.2 |
| sportsdataverse/ncaa-mfb-football-raw | tests | failure | [run](https://github.com/sportsdataverse/ncaa-mfb-football-raw/actions/runs/38234290182) | 6.1 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/38222482361) | 6.2 |
| sportsdataverse/nfl-raw | tests | failure | [run](https://github.com/sportsdataverse/nfl-raw/actions/runs/38287620933) | 5.8 |
| sportsdataverse/sdvplotR | R-hub | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/39070634243) | 0.7 |
| sportsdataverse/sdvplotR | automation-example | failure | [run](https://github.com/sportsdataverse/sdvplotR/actions/runs/38312948847) | 5.7 |
| sportsdataverse/sportsdataverse-js | Live smoke | failure | [run](https://github.com/sportsdataverse/sportsdataverse-js/actions/runs/38295521880) | 5.8 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/38310951741) | 5.7 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/39120490426) | 0.1 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 51.9 |
| sportsdataverse/wehoop-wbb-data | tests | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-data/actions/runs/39129498725) | 0.0 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/39123478245) | 0.1 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 42.2 | 42.2 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 511.4 | 32.6 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 34.9 | 13.1 |  |
| saiemgilani/game-on-paper-app | [#313](https://github.com/saiemgilani/game-on-paper-app/pull/313) fix(percentiles): player game-log cohorts, midrank ties, position perc | saiemgilani | 9.4 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#312](https://github.com/saiemgilani/game-on-paper-app/pull/312) fix(game): Binion box percentiles: per-season ladder, midrank ties, da | saiemgilani | 9.4 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#308](https://github.com/saiemgilani/game-on-paper-app/pull/308) feat(team): Results by Opponent bars on the season team page (preview) | saiemgilani | 10.3 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#307](https://github.com/saiemgilani/game-on-paper-app/pull/307) feat(team): Situational Splits section on the season team page (previe | saiemgilani | 10.3 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#306](https://github.com/saiemgilani/game-on-paper-app/pull/306) feat(game): Paper Index factor impact on Deserved Win % (preview) | saiemgilani | 10.3 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#304](https://github.com/saiemgilani/game-on-paper-app/pull/304) feat(header): typed site search in the header (preview) | saiemgilani | 10.5 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#303](https://github.com/saiemgilani/game-on-paper-app/pull/303) feat(game): average starting field position in EP units in the Drives  | saiemgilani | 10.6 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#302](https://github.com/saiemgilani/game-on-paper-app/pull/302) feat(leaderboards): last-updated stamps on the leaderboards and trends | saiemgilani | 10.6 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#301](https://github.com/saiemgilani/game-on-paper-app/pull/301) feat(game): v2 WP chart download carries its title, URL and data time | saiemgilani | 10.6 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#297](https://github.com/saiemgilani/game-on-paper-app/pull/297) feat(charts): Chart Builder v2 control bar with Plot, median crosshair | saiemgilani | 13.7 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#296](https://github.com/saiemgilani/game-on-paper-app/pull/296) feat(leaderboards): nearby-rank lists on the team and player season pa | saiemgilani | 13.9 | 5.7 |  |
| saiemgilani/game-on-paper-app | [#309](https://github.com/saiemgilani/game-on-paper-app/pull/309) feat(share-card): GOP-rendered share card for every game state, with a | saiemgilani | 10.3 | 5.5 |  |
| sportsdataverse/sportsdataverse-py | [#839](https://github.com/sportsdataverse/sportsdataverse-py/pull/839) docs(tutorials): weekly refresh of executed notebook pages | github-actions[bot] | 5.6 | 0.6 |  |
| sportsdataverse/sportsdataverse-py | [#750](https://github.com/sportsdataverse/sportsdataverse-py/pull/750) sdv-py quality program: program-setup | saiemgilani | 7.2 | 0.3 | y |
| sportsdataverse/sportyR | [#58](https://github.com/sportsdataverse/sportyR/pull/58) chore: prepare sportyR 2.3.0 for CRAN | saiemgilani | 0.2 | 0.2 |  |
| sportsdataverse/sportsdataverse-py | [#759](https://github.com/sportsdataverse/sportsdataverse-py/pull/759) sdv-py quality program: test-harness | saiemgilani | 7.1 | 0.2 | y |
| sportsdataverse/sportsdataverse-py | [#856](https://github.com/sportsdataverse/sportsdataverse-py/pull/856) fix(nfl): repair pre-2014 ESPN periods; score overlay reads td flags;  | saiemgilani | 5.2 | 0.1 |  |
| sportsdataverse/sportsdataverse-py | [#854](https://github.com/sportsdataverse/sportsdataverse-py/pull/854) fix(cfb): read the rush yardage text forms that left yds_rushed null | saiemgilani | 5.3 | 0.1 |  |
| sportsdataverse/sdvplot-js | [#66](https://github.com/sportsdataverse/sdvplot-js/pull/66) chore(release): version packages | github-actions[bot] | 0.3 | 0.1 |  |
| sportsdataverse/sportyR | [#68](https://github.com/sportsdataverse/sportyR/pull/68) fix: lacrosse geometry quirks, NCAA coaching line, football border out | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#879](https://github.com/sportsdataverse/sportsdataverse-py/pull/879) ci(quality): run the mutation registry in six shards | saiemgilani | 0.0 | 0.0 |  |
| sportsdataverse/sportsdataverse-py | [#878](https://github.com/sportsdataverse/sportsdataverse-py/pull/878) fix(espn): rosters keep position columns, honour raw=, warn on logo-sh | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/sportypy | [#20](https://github.com/sportsdataverse/sportypy/pull/20) feat: sportyR 2.3.0 parity (lacrosse, softball, PWHL, Curling Canada)  | saiemgilani | 0.1 | 0.0 |  |
| sportsdataverse/sdvplot-js | [#71](https://github.com/sportsdataverse/sdvplot-js/pull/71) feat(sporty): sportyR 2.3.0 + geometry fixes, NCAA softball, every spo | saiemgilani | 0.0 | 0.0 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| BillPetti/baseballr | 7 | 7 |
| sportsdataverse/sportyR | 16 | 6 |
| sportsdataverse/sportsdataverse-py | 8 | 6 |
| saiemgilani/game-on-paper-app | 6 | 6 |
| sportsdataverse/wehoop-wnba-data | 5 | 3 |
| sportsdataverse/sdvplot | 4 | 3 |
| sportsdataverse/hoopR | 2 | 2 |
| sportsdataverse/fastRhockey-nhl-data | 3 | 2 |
| sportsdataverse/cfbfastR | 1 | 1 |
| sportsdataverse/cfbfastR-data | 1 | 1 |
| sportsdataverse/sportypy | 1 | 1 |
| sportsdataverse/sdvplotR | 1 | 1 |
| sportsdataverse/softballR | 1 | 1 |
| sportsdataverse/sportsdataverse-data | 5 | 1 |
| sportsdataverse/hoopR-nba-stats-data | 1 | 1 |
| sportsdataverse/wehoop-wnba-stats-data | 2 | 1 |
| sportsdataverse/wehoop-wbb-data | 3 | 1 |
| sportsdataverse/nfl-data | 1 | 1 |
| sportsdataverse/sportsdataverse-js | 1 | 0 |
| sportsdataverse/wehoop | 1 | 0 |
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/hoopR-mbb-data | 2 | 0 |
| sportsdataverse/hoopR-nba-data | 4 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |
| sportsdataverse/ncaa-mfb-football-data | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-11T15:55 | 6.9 | 0.1 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 80.7 | 0.0 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 699.2 | 6.1 |
| sportsdataverse/sportsdataverse-data | wnba_stats_rolling_windows | 382 | 2026-10-18T13:26 | 0.0 | 6.1 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.1 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 9.4 |
| sportsdataverse/cfb4th | model_archive | 2026-10-09 | 0.0 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 0.1 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 0.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 0.0 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.0 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 0.1 |
| sportsdataverse/sdvplot | v0.1.0 | 2026-10-05 | 0.0 |
| sportsdataverse/sdvplot-js | @sportsdataverse/sporty@0.1.0 | 2026-10-09 | 0.0 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.0 |
| sportsdataverse/sportsdataverse-js | v4.0.0 | 2026-10-09 | 0.1 |
| sportsdataverse/sportsdataverse-py | docs-index | 2026-10-06 | 0.0 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 0.1 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 0.0 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.0 |

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
