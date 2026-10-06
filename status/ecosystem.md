# SportsDataverse ecosystem status

_82 public repos · generated 2026-10-06T16:07Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

380 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| cfb_crosswalk | cfbfastR-cfb-data | 26 | 2026-06-13T08:31 | 115.3 | 2025 |
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 82.0 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 80.1 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 80.1 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 76.6 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-07-22T21:39 | 75.8 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 75.8 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 61.3 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 55.3 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 55.3 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 55.3 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 55.3 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 55.3 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 55.3 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:05 | 55.3 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 55.3 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 54.4 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 54.4 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 54.4 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 95 | 2026-08-13T05:20 | 54.4 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 53.9 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 53.9 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 53.9 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 53.9 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 53.9 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 53.9 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 53.9 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 53.9 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 53.8 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 49.1 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 49.1 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 49.1 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 49.1 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 49.1 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 49.1 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 49.1 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 49.1 | 2026 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 47.6 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 47.6 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 47.6 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 47.6 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 47.6 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 47.6 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 43.6 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 43.6 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 43.3 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 43.3 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 40.2 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 40.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 39.9 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 39.9 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 39.9 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 39.9 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 39.9 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 39.9 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 39.8 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 39.8 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 39.8 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 34.8 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 34.8 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 34.8 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 34.8 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 34.8 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 34.8 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 34.8 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 56 | 2026-09-01T20:26 | 34.8 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 34.8 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 48 | 2026-09-02T18:05 | 33.9 | 2025 |
| nba_player_impact | hoopR-nba-stats-data | 95 | 2026-09-02T18:27 | 33.9 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 33.9 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 33.9 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 33.9 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 33.9 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 33.9 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 33.9 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 33.9 | 2023 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-09-02T19:02 | 33.9 | 2026 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 27.5 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 27.5 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 27.5 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 27.5 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 27.5 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 27.5 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-09-09T04:42 | 27.5 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 27.5 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 27.5 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-09-09T05:16 | 27.5 | 2026 |
| espn_nba_team_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 27.5 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 27.5 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 79 | 2026-09-09T05:18 | 27.5 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 27.5 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 27.4 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 27.4 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 27.4 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 27.4 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 27.4 | 2026 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-09-09T05:43 | 27.4 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 27.2 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 25 | 2026-09-09T14:13 | 27.1 |  |
| mlb_pitches | baseballr-data | 121 | 2026-09-10T04:38 | 26.5 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-09-10T04:58 | 26.5 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-09-10T14:28 | 26.1 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-09-15T08:21 | 21.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-09-15T08:22 | 21.3 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-09-19T00:45 | 17.6 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-09-19T01:46 | 17.6 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 9.5 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 9.5 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 9.5 | 2025 |
| nfl_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 9.5 | 2026 |
| nhl_groups | sdv-reference-data | 224 | 2026-09-27T03:32 | 9.5 | 2026 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 9.5 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 94 | 2026-09-27T10:25 | 9.2 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 82 | 2026-09-27T10:26 | 9.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-09-27T19:55 | 8.8 |  |
| mbb_groups | sdv-reference-data | 60 | 2026-09-28T13:33 | 8.1 | 2027 |
| mlb_groups | sdv-reference-data | 260 | 2026-09-28T13:34 | 8.1 | 2026 |
| wbb_groups | sdv-reference-data | 60 | 2026-09-28T13:34 | 8.1 | 2027 |
| wnba_crosswalk | wehoop-wnba-data | 16 | 2026-09-29T10:43 | 7.2 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-09-29T19:03 | 6.9 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 6.7 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-09-29T23:32 | 6.7 | 2026 |
| espn_nfl_qa | nfl-data | 3 | 2026-09-29T23:32 | 6.7 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-09-29T23:32 | 6.7 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 23 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-09-29T23:33 | 6.7 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-09-29T23:33 | 6.7 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-09-29T23:35 | 6.7 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-09-29T23:35 | 6.7 |  |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 6.5 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 6.5 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 6.5 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 6.5 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-09-30T05:27 | 6.4 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 6.1 |  |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-09-30T14:05 | 6.1 | 2026 |
| nba_stats_hustle | hoopR-nba-stats-data | 90 | 2026-09-30T14:24 | 6.1 | 2026 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-30T14:28 | 6.1 | 2026 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-30T14:36 | 6.1 | 2027 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 23 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-09-30T14:50 | 6.1 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 23 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-09-30T14:52 | 6.1 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 6.1 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 6.1 | 2026 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 5.6 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 5.6 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 5.6 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 5.6 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 5.6 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 5.6 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-01T12:07 | 5.2 | 2026 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 92 | 2026-10-01T22:01 | 4.8 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T22:33 | 4.7 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-10-04T10:51 | 2.2 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-04T10:51 | 2.2 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-04T10:51 | 2.2 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-10-04T10:51 | 2.2 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-04T10:52 | 2.2 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-10-04T10:52 | 2.2 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-10-04T10:52 | 2.2 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-10-04T10:52 | 2.2 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-10-04T12:11 | 2.2 | 2027 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-04T16:43 | 2.0 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-04T16:44 | 2.0 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-04T16:45 | 2.0 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-10-04T17:21 | 1.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-10-04T17:21 | 1.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-10-04T17:21 | 1.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-10-04T17:21 | 1.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-10-04T17:21 | 1.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-10-04T17:21 | 1.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-04T17:23 | 1.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-04T17:24 | 1.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-04T17:24 | 1.9 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-10-04T18:42 | 1.9 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-10-04T18:42 | 1.9 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-04T18:52 | 1.9 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-04T19:31 | 1.9 | 2026 |
| nfl_defense_vs_position | nfl-data | 31 | 2026-10-04T19:34 | 1.9 | 2025 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T19:42 | 1.9 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T19:52 | 1.8 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-10-04T20:30 | 1.8 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T20:39 | 1.8 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T20:47 | 1.8 | 2026 |
| cfb_defense_vs_position | cfbfastR-cfb-data | 10 | 2026-10-04T23:04 | 1.7 | 2015 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-10-04T23:08 | 1.7 | 2026 |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-10-05T15:38 | 1.0 | 2026 |
| nfl_rosters | nfl-data | 29 | 2026-10-05T18:13 | 0.9 | 2026 |
| nfl_players | nfl-data | 5 | 2026-10-05T18:13 | 0.9 |  |
| nfl_player_stats | nfl-data | 5 | 2026-10-05T18:14 | 0.9 |  |
| nfl_team_stats | nfl-data | 5 | 2026-10-05T18:15 | 0.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-10-05T18:18 | 0.9 |  |
| mlb_game_state | baseballr-data | 116 | 2026-10-05T19:41 | 0.9 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-10-05T21:00 | 0.8 | 2026 |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-10-05T21:24 | 0.8 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-10-05T21:25 | 0.8 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-10-05T21:25 | 0.8 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-05T21:43 | 0.8 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-05T22:18 | 0.7 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-06T05:26 | 0.4 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-06T08:01 | 0.3 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-06T08:01 | 0.3 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-06T08:01 | 0.3 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-06T08:01 | 0.3 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-06T08:02 | 0.3 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 67 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-06T08:03 | 0.3 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-06T08:03 | 0.3 | 2027 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-10-06T08:10 | 0.3 | 2026 |
| espn_cfb_pbp | cfbfastR-cfb-data | 72 | 2026-10-06T08:15 | 0.3 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-06T08:17 | 0.3 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-06T08:18 | 0.3 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-06T08:19 | 0.3 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-06T08:20 | 0.3 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-06T08:21 | 0.3 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-06T08:21 | 0.3 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-06T08:22 | 0.3 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-06T08:23 | 0.3 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-06T08:24 | 0.3 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-06T08:25 | 0.3 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-06T08:25 | 0.3 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-06T08:26 | 0.3 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-06T08:27 | 0.3 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-06T08:27 | 0.3 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-06T08:28 | 0.3 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-06T08:29 | 0.3 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-06T08:30 | 0.3 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-06T08:36 | 0.3 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-10-06T08:56 | 0.3 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-06T09:02 | 0.3 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-10-06T09:07 | 0.3 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-10-06T09:27 | 0.3 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-06T09:32 | 0.3 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-06T09:38 | 0.3 | 2026 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-10-06T09:43 | 0.3 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-10-06T10:58 | 0.2 | 2026 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-06T11:08 | 0.2 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-06T11:08 | 0.2 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-06T11:09 | 0.2 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-06T11:09 | 0.2 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 85 | 2026-10-06T11:09 | 0.2 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-06T11:10 | 0.2 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-06T11:10 | 0.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-06T11:10 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-06T11:10 | 0.2 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-06T11:11 | 0.2 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-06T11:11 | 0.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-06T11:11 | 0.2 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-10-06T11:15 | 0.2 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-06T11:24 | 0.2 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-10-06T11:31 | 0.2 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-10-06T11:37 | 0.2 | 2026 |
| nba_crosswalk | hoopR-nba-data | 25 | 2026-10-06T11:42 | 0.2 | 2027 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-06T11:48 | 0.2 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-06T11:48 | 0.2 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-06T11:48 | 0.2 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-06T11:48 | 0.2 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-06T11:49 | 0.2 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-06T11:49 | 0.2 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-06T11:49 | 0.2 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-06T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-06T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-06T11:50 | 0.2 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-06T11:51 | 0.2 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-06T11:51 | 0.2 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-10-06T11:51 | 0.2 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-06T11:51 | 0.2 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-10-06T11:51 | 0.2 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-10-06T11:52 | 0.2 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-06T11:52 | 0.2 | 2026 |
| cfb_paper_index_games | cfbfastR-cfb-data | 37 | 2026-10-06T11:52 | 0.2 | 2014 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-06T11:53 | 0.2 | 2026 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-06T11:56 | 0.2 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-06T11:56 | 0.2 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-10-06T12:03 | 0.2 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-10-06T12:03 | 0.2 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-10-06T12:05 | 0.2 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-10-06T12:06 | 0.2 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-10-06T12:07 | 0.2 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-10-06T12:07 | 0.2 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-10-06T12:07 | 0.2 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-10-06T12:08 | 0.2 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-10-06T12:08 | 0.2 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-10-06T12:08 | 0.2 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-10-06T12:08 | 0.2 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-10-06T12:08 | 0.2 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-10-06T12:10 | 0.2 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-10-06T12:12 | 0.2 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-06T12:13 | 0.2 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-10-06T12:13 | 0.2 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-10-06T12:14 | 0.2 |  |
| espn_nba_schedules | hoopR-nba-data | 88 | 2026-10-06T12:15 | 0.2 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-06T12:15 | 0.2 | 2027 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-06T12:16 | 0.2 | 2027 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-06T13:34 | 0.1 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-06T13:34 | 0.1 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-06T13:35 | 0.1 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-06T13:35 | 0.1 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-06T13:35 | 0.1 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-06T13:35 | 0.1 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-06T13:35 | 0.1 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-06T13:36 | 0.1 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-06T13:36 | 0.1 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-06T13:36 | 0.1 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-06T13:36 | 0.1 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-06T13:36 | 0.1 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-06T13:37 | 0.1 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-06T13:37 | 0.1 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-06T13:37 | 0.1 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-06T14:01 | 0.1 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-06T14:01 | 0.1 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-06T14:01 | 0.1 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-06T14:01 | 0.1 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-06T14:11 | 0.1 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-06T14:30 | 0.1 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-06T15:32 | 0.0 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-06T15:32 | 0.0 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-06T15:33 | 0.0 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-06T15:33 | 0.0 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-06T15:33 | 0.0 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-06T15:33 | 0.0 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-06T15:33 | 0.0 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-06T15:34 | 0.0 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-06T15:34 | 0.0 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-06T15:34 | 0.0 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 60 | 2026-10-06T15:34 | 0.0 | 2026 |
| espn_cfb_player_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_cfb_team_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-06 | 2026-10-06 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-10-02<br>`cfb_fpi_weekly.yml` success 2026-10-05<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` failure 2026-10-05 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-10-05 | 2026-10-05 | 2026 | `daily_cfb.yml` success 2026-10-05 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-06 | 2026-10-06 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-06 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-09-29 | 2026-10-05 | 2026 | `espn_nfl_cron.yml` success 2026-09-29<br>`nfl_pbp_cron.yml` success 2026-09-30<br>`nfl_ratings_weekly.yml` success 2026-09-29<br>`nfl_rosters_players_cron.yml` success 2026-10-05<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-06 | 2026-10-06 | 2026 | `daily_ngs.yml` success 2026-10-06 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-09-19 | 2026-09-30 | 2026 | `daily_mbb.yml` skipped 2026-09-30<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-08-24 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-09-09 | 2026-10-06 | 2026 | `daily_nba.yml` success 2026-10-03 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-08-13 | 2026-10-01 | 2026 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` no runs |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-09-19 | 2026-10-04 | 2026 | `daily_wbb.yml` success 2026-09-09<br>`weekly_wbb.yml` success 2026-10-04<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-08-24 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-10-06 | 2026-10-06 | 2026 | `daily_wnba.yml` success 2026-10-05<br>`weekly_wnba.yml` success 2026-10-04<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-10-06 | 2026-10-06 | 2026 | `daily_wnba_stats.yml` success 2026-10-05<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | idle | no | 2026-10-06 | 2026-10-06 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-07-22 | 2026-09-02 | 2026 | `daily_pwhl_python.yml` no runs<br>`pwhl_xg_cron.yml` no runs |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | stale | yes | 2026-09-10 | 2026-10-05 | 2026 | `mlb_models_cron.yml` success 2026-10-04<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-09-29 | 2026-09-29 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 66.2 |
| sportsdataverse/baseballr-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/37211098016) | 2.0 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 43.2 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 62.1 |
| sportsdataverse/cfbfastR-cfb-data | ESPN Daily Snapshots | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/37373099829) | 0.8 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 38.1 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/36903181691) | 4.9 |
| sportsdataverse/hoopR | R-CMD-check | failure | [run](https://github.com/sportsdataverse/hoopR/actions/runs/37357103484) | 0.9 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 119.3 |
| sportsdataverse/hoopR | api-sync | failure | [run](https://github.com/sportsdataverse/hoopR/actions/runs/37363813442) | 0.9 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/36902076422) | 4.9 |
| sportsdataverse/sportsdataverse-js | Live smoke | failure | [run](https://github.com/sportsdataverse/sportsdataverse-js/actions/runs/37356819427) | 0.9 |
| sportsdataverse/sportsdataverse-py | live-tests-cron | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37372540649) | 0.8 |
| sportsdataverse/sportsdataverse-py | tests | failure | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37451600617) | 0.2 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 40.1 |
| sportsdataverse/wehoop-wbb-data | Weekly R/Python Output Parity | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-data/actions/runs/37368533186) | 0.8 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/25519402950) | 151.8 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 30.4 | 30.4 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 499.5 | 20.7 |  |
| sportsdataverse/sportyR | [#52](https://github.com/sportsdataverse/sportyR/pull/52) Add NCAA softball field via geom_softball() | billyfryer | 7.0 | 5.4 |  |
| sportsdataverse/sdv-assets | [#11](https://github.com/sportsdataverse/sdv-assets/pull/11) data: monthly capture 2026-10-01 | saiemgilani | 5.3 | 5.3 |  |
| saiemgilani/game-on-paper-app | [#295](https://github.com/saiemgilani/game-on-paper-app/pull/295) Update astro depends to see if #205 is fixed | a5ehren | 2.9 | 2.9 |  |
| saiemgilani/game-on-paper-app | [#296](https://github.com/saiemgilani/game-on-paper-app/pull/296) feat(leaderboards): nearby-rank lists on the team and player season pa | saiemgilani | 2.0 | 2.0 |  |
| saiemgilani/game-on-paper-app | [#299](https://github.com/saiemgilani/game-on-paper-app/pull/299) feat(game): linked hover between the WP chart, play tables and drives  | saiemgilani | 1.8 | 1.8 |  |
| saiemgilani/game-on-paper-app | [#298](https://github.com/saiemgilani/game-on-paper-app/pull/298) feat(schedule): previous/next week stepper and folded phone filters (p | saiemgilani | 1.8 | 1.8 |  |
| saiemgilani/game-on-paper-app | [#297](https://github.com/saiemgilani/game-on-paper-app/pull/297) feat(charts): Chart Builder v2 metric rail, median crosshair and rando | saiemgilani | 1.8 | 1.8 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 23.0 | 1.2 |  |
| sportsdataverse/sdvplot-js | [#4](https://github.com/sportsdataverse/sdvplot-js/pull/4) chore(release): version packages | github-actions[bot] | 0.5 | 0.4 |  |
| sportsdataverse/sportsdataverse-py | [#708](https://github.com/sportsdataverse/sportsdataverse-py/pull/708) feat: sdv-py wrappers for the wave-2 intake providers (ESPN content, T | saiemgilani | 0.1 | 0.1 |  |

## Open issues

Stale = unassigned with no update for at least 7 days.

| repo | open issues | stale unassigned |
|---|---|---|
| saiemgilani/game-on-paper-app | 7 | 7 |
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
| sportsdataverse/sportsdataverse-js | 1 | 0 |
| sportsdataverse/.github | 1 | 0 |
| sportsdataverse/sdvplotR | 1 | 0 |
| sportsdataverse/wehoop-wnba-stats-data | 1 | 0 |
| sportsdataverse/fastRhockey-nhl-data | 1 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |
| sportsdataverse/sdvplot | 3 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-01T01:33 | 5.6 | 0.2 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 68.8 | 0.1 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 687.3 | 917.9 |
| sportsdataverse/sportsdataverse-data | wnba_stats_rolling_windows | 380 | 2026-10-06T15:34 | 0.0 | 1.7 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.2 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 6.1 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 5.2 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 6.1 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 6.1 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 0.9 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 6.1 |
| sportsdataverse/sdvplot | v0.1.0 | 2026-10-05 | 0.0 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.3 |
| sportsdataverse/sportsdataverse-js | v3.0.0 | 2026-06-17 | 0.2 |
| sportsdataverse/sportsdataverse-py | docs-index | 2026-10-06 | 0.1 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 10.4 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 10.4 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 0.9 |

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
