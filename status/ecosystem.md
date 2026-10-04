# SportsDataverse ecosystem status

_81 public repos · generated 2026-10-04T14:55Z by `.github/workflows/ecosystem-status.yml` · machine-readable twins: `ecosystem.json`, `summary.json` · badges: `badges/`._

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

377 tags on `sportsdataverse/sportsdataverse-data`, stalest first (tags with no assets last). `producer` comes from `producers.json`; `through season` is the newest season year in the tag's asset names (SDV end-year convention).

| tag | producer | assets | newest asset | age (d) | through season |
|---|---|---|---|---|---|
| cfb_crosswalk | cfbfastR-cfb-data | 26 | 2026-06-13T08:31 | 113.3 | 2025 |
| espn_wnba_draft | wehoop-wnba-data | 24 | 2026-07-16T15:58 | 80.0 | 2026 |
| pwhl_rosters | fastRhockey-pwhl-data | 13 | 2026-07-18T12:39 | 78.1 | 2026 |
| pwhl_schedules | fastRhockey-pwhl-data | 19 | 2026-07-18T12:39 | 78.1 | 2026 |
| nhl_rosters | fastRhockey-nhl-data | 55 | 2026-07-22T02:05 | 74.5 | 2026 |
| pwhl_pbp | fastRhockey-pwhl-data | 14 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_shifts | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_skater_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_goalie_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_team_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_game_info | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_game_rosters | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_scoring_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_penalty_summary | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_three_stars | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_officials | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_shots_by_period | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_shootout | fastRhockey-pwhl-data | 7 | 2026-07-22T21:39 | 73.7 | 2026 |
| pwhl_player_boxscores | fastRhockey-pwhl-data | 13 | 2026-07-22T21:39 | 73.7 | 2026 |
| cfb_recruiting_proj | cfbfastR-cfb-data | 11 | 2026-08-06T08:07 | 59.3 | 2025 |
| ncaa_mbb_team_ids | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 53.3 | 2026 |
| ncaa_mbb_schedule | ncaa-mbb-hoops-data | 51 | 2026-08-12T07:59 | 53.3 | 2026 |
| ncaa_mbb_team_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 53.3 | 2026 |
| ncaa_mbb_rosters | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:00 | 53.3 | 2026 |
| ncaa_mbb_pbp | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:03 | 53.3 | 2026 |
| ncaa_mbb_player_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:04 | 53.3 | 2026 |
| ncaa_mbb_team_box | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:05 | 53.3 | 2026 |
| ncaa_mbb_possessions | ncaa-mbb-hoops-data | 51 | 2026-08-12T08:08 | 53.3 | 2026 |
| nba_stats_game_lineups | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 52.4 | 2026 |
| nba_stats_pbp | hoopR-nba-stats-data | 91 | 2026-08-13T05:19 | 52.4 | 2026 |
| nba_stats_possessions | hoopR-nba-stats-data | 91 | 2026-08-13T05:20 | 52.4 | 2026 |
| nba_stats_schedules | hoopR-nba-stats-data | 95 | 2026-08-13T05:20 | 52.4 | 2026 |
| nba_stats_coaches | hoopR-nba-stats-data | 90 | 2026-08-13T17:38 | 51.9 | 2026 |
| nba_stats_draft | hoopR-nba-stats-data | 90 | 2026-08-13T17:39 | 51.9 | 2026 |
| nba_stats_rosters | hoopR-nba-stats-data | 90 | 2026-08-13T17:40 | 51.9 | 2026 |
| nba_stats_standings | hoopR-nba-stats-data | 90 | 2026-08-13T17:41 | 51.9 | 2026 |
| nba_stats_team_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 51.9 | 2026 |
| nba_stats_player_game_logs | hoopR-nba-stats-data | 90 | 2026-08-13T17:42 | 51.9 | 2026 |
| nba_stats_player_season_stats | hoopR-nba-stats-data | 90 | 2026-08-13T17:43 | 51.9 | 2026 |
| nba_stats_lineups | hoopR-nba-stats-data | 57 | 2026-08-13T17:46 | 51.9 | 2026 |
| nba_stats_leaguedash | hoopR-nba-stats-data | 833 | 2026-08-13T21:11 | 51.7 | 2026 |
| ncaa_wbb_team_ids | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 47.1 | 2026 |
| ncaa_wbb_schedule | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:37 | 47.1 | 2026 |
| ncaa_wbb_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:38 | 47.1 | 2026 |
| ncaa_wbb_player_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 47.1 | 2026 |
| ncaa_wbb_team_box | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:45 | 47.1 | 2026 |
| ncaa_wbb_possessions | ncaa-wbb-hoops-data | 51 | 2026-08-18T12:49 | 47.1 | 2026 |
| ncaa_wbb_pbp | ncaa-wbb-hoops-data | 51 | 2026-08-18T13:02 | 47.1 | 2026 |
| ncaa_wbb_team_rosters | ncaa-wbb-hoops-data | 51 | 2026-08-18T14:21 | 47.0 | 2026 |
| nba_crosswalk | hoopR-nba-data | 25 | 2026-08-19T01:34 | 46.6 | 2027 |
| ncaa_wbb_shots | ncaa-wbb-hoops-data | 24 | 2026-08-20T01:21 | 45.6 | 2026 |
| ncaa_mbb_shots | ncaa-mbb-hoops-data | 24 | 2026-08-20T01:25 | 45.6 | 2026 |
| ncaa_wbb_lineups | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:10 | 45.5 | 2026 |
| ncaa_wbb_matchup_stints | ncaa-wbb-hoops-data | 51 | 2026-08-20T02:12 | 45.5 | 2026 |
| ncaa_mbb_lineups | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:17 | 45.5 | 2026 |
| ncaa_mbb_matchup_stints | ncaa-mbb-hoops-data | 51 | 2026-08-20T02:18 | 45.5 | 2026 |
| ncaa_mbb_rapm_within_team | ncaa-mbb-hoops-data | 55 | 2026-08-24T02:01 | 41.5 | 2026 |
| ncaa_wbb_rapm_within_team | ncaa-wbb-hoops-data | 55 | 2026-08-24T02:04 | 41.5 | 2026 |
| ncaa_wbb_rapm | ncaa-wbb-hoops-data | 52 | 2026-08-24T08:32 | 41.3 | 2026 |
| ncaa_mbb_rapm | ncaa-mbb-hoops-data | 52 | 2026-08-24T08:32 | 41.3 | 2026 |
| cfb_team_info | cfbfastR-cfb-data | 52 | 2026-08-27T11:01 | 38.2 | 2026 |
| espn_cfb_teams | cfbfastR-cfb-data | 78 | 2026-08-27T11:09 | 38.2 | 2026 |
| ncaa_baseball_teams | baseballr-data | 9 | 2026-08-27T19:11 | 37.8 | 2026 |
| ncaa_baseball_rosters | baseballr-data | 9 | 2026-08-27T19:11 | 37.8 | 2026 |
| ncaa_baseball_linescore | baseballr-data | 9 | 2026-08-27T19:18 | 37.8 | 2026 |
| ncaa_baseball_team_stats | baseballr-data | 9 | 2026-08-27T19:18 | 37.8 | 2026 |
| ncaa_baseball_player_stats | baseballr-data | 9 | 2026-08-27T19:19 | 37.8 | 2026 |
| ncaa_baseball_situational_stats | baseballr-data | 9 | 2026-08-27T19:19 | 37.8 | 2026 |
| ncaa_baseball_schedules | baseballr-data | 59 | 2026-08-27T19:51 | 37.8 | 2026 |
| ncaa_baseball_pbp | baseballr-data | 39 | 2026-08-27T19:56 | 37.8 | 2026 |
| ncaa_baseball_games | baseballr-data | 30 | 2026-08-27T19:56 | 37.8 | 2026 |
| espn_mens_college_basketball_team_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:44 | 32.8 | 2026 |
| espn_mens_college_basketball_player_boxscores | hoopR-mbb-data | 76 | 2026-09-01T19:46 | 32.8 | 2026 |
| espn_mens_college_basketball_player_core | hoopR-mbb-data | 72 | 2026-09-01T20:00 | 32.8 | 2026 |
| espn_mens_college_basketball_shots | hoopR-mbb-data | 71 | 2026-09-01T20:01 | 32.8 | 2026 |
| espn_mens_college_basketball_player_season_stats | hoopR-mbb-data | 12 | 2026-09-01T20:17 | 32.8 | 2026 |
| espn_mens_college_basketball_team_season_stats | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 32.8 | 2026 |
| espn_mens_college_basketball_standings | hoopR-mbb-data | 78 | 2026-09-01T20:18 | 32.8 | 2026 |
| espn_mens_college_basketball_game_rosters | hoopR-mbb-data | 56 | 2026-09-01T20:26 | 32.8 | 2026 |
| espn_mens_college_basketball_officials | hoopR-mbb-data | 54 | 2026-09-01T20:27 | 32.8 | 2026 |
| espn_cfb_model_pbp | cfbfastR-cfb-data | 48 | 2026-09-02T18:05 | 31.9 | 2025 |
| nba_player_impact | hoopR-nba-stats-data | 95 | 2026-09-02T18:27 | 31.9 | 2026 |
| nfl_4th_down_models | nfl-data | 6 | 2026-09-02T18:28 | 31.9 |  |
| nfl_model_artifacts | nfl-data | 15 | 2026-09-02T18:28 | 31.9 |  |
| nhl_xg_models |  | 7 | 2026-09-02T18:29 | 31.9 |  |
| phf_pbp |  | 7 | 2026-09-02T18:29 | 31.9 | 2023 |
| phf_player_boxscores |  | 10 | 2026-09-02T18:29 | 31.9 | 2023 |
| phf_schedules |  | 10 | 2026-09-02T18:29 | 31.9 | 2023 |
| phf_team_boxscores |  | 10 | 2026-09-02T18:29 | 31.9 | 2023 |
| pwhl_xg_pbp | fastRhockey-pwhl-data | 14 | 2026-09-02T19:02 | 31.8 | 2026 |
| espn_womens_college_basketball_team_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:35 | 25.4 | 2026 |
| espn_womens_college_basketball_player_boxscores | wehoop-wbb-data | 72 | 2026-09-09T04:37 | 25.4 | 2026 |
| espn_womens_college_basketball_player_core | wehoop-wbb-data | 70 | 2026-09-09T04:40 | 25.4 | 2026 |
| espn_womens_college_basketball_shots | wehoop-wbb-data | 74 | 2026-09-09T04:41 | 25.4 | 2026 |
| espn_womens_college_basketball_player_season_stats | wehoop-wbb-data | 61 | 2026-09-09T04:42 | 25.4 | 2026 |
| espn_womens_college_basketball_team_season_stats | wehoop-wbb-data | 49 | 2026-09-09T04:42 | 25.4 | 2026 |
| espn_womens_college_basketball_standings | wehoop-wbb-data | 68 | 2026-09-09T04:42 | 25.4 | 2026 |
| espn_womens_college_basketball_game_rosters | wehoop-wbb-data | 71 | 2026-09-09T04:45 | 25.4 | 2026 |
| espn_womens_college_basketball_officials | wehoop-wbb-data | 37 | 2026-09-09T04:47 | 25.4 | 2026 |
| espn_nba_pbp | hoopR-nba-data | 79 | 2026-09-09T05:16 | 25.4 | 2026 |
| espn_nba_team_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 25.4 | 2026 |
| espn_nba_player_boxscores | hoopR-nba-data | 79 | 2026-09-09T05:17 | 25.4 | 2026 |
| espn_nba_player_core | hoopR-nba-data | 79 | 2026-09-09T05:18 | 25.4 | 2026 |
| espn_nba_shots | hoopR-nba-data | 80 | 2026-09-09T05:18 | 25.4 | 2026 |
| espn_nba_player_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 25.4 | 2026 |
| espn_nba_team_season_stats | hoopR-nba-data | 80 | 2026-09-09T05:19 | 25.4 | 2026 |
| espn_nba_standings | hoopR-nba-data | 80 | 2026-09-09T05:20 | 25.4 | 2026 |
| espn_nba_game_rosters | hoopR-nba-data | 80 | 2026-09-09T05:20 | 25.4 | 2026 |
| espn_nba_officials | hoopR-nba-data | 80 | 2026-09-09T05:21 | 25.4 | 2026 |
| espn_womens_college_basketball_schedules | wehoop-wbb-data | 88 | 2026-09-09T05:43 | 25.4 | 2027 |
| nhl_shootout | fastRhockey-nhl-data | 55 | 2026-09-09T11:00 | 25.2 | 2026 |
| cfb_model_artifacts | cfbfastR-cfb-data | 25 | 2026-09-09T14:13 | 25.0 |  |
| mlb_pitches | baseballr-data | 121 | 2026-09-10T04:38 | 24.4 | 2026 |
| mlb_runners | baseballr-data | 121 | 2026-09-10T04:58 | 24.4 | 2026 |
| mlb_pbp | baseballr-data | 121 | 2026-09-10T14:28 | 24.0 | 2026 |
| espn_mens_college_basketball_schedules | hoopR-mbb-data | 88 | 2026-09-15T08:21 | 19.3 | 2027 |
| espn_mens_college_basketball_rosters | hoopR-mbb-data | 15 | 2026-09-15T08:22 | 19.3 | 2027 |
| espn_womens_college_basketball_pbp | wehoop-wbb-data | 73 | 2026-09-19T00:45 | 15.6 | 2026 |
| espn_mens_college_basketball_pbp | hoopR-mbb-data | 70 | 2026-09-19T01:46 | 15.5 | 2026 |
| nba_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 7.5 | 2027 |
| ncaa_baseball_groups | sdv-reference-data | 42 | 2026-09-27T03:31 | 7.5 | 2026 |
| ncaa_softball_groups | sdv-reference-data | 96 | 2026-09-27T03:31 | 7.5 | 2025 |
| nfl_groups | sdv-reference-data | 122 | 2026-09-27T03:31 | 7.5 | 2026 |
| nhl_groups | sdv-reference-data | 224 | 2026-09-27T03:32 | 7.5 | 2026 |
| wnba_groups | sdv-reference-data | 68 | 2026-09-27T04:40 | 7.4 | 2026 |
| mbb_crosswalk | hoopR-mbb-data | 94 | 2026-09-27T10:25 | 7.2 | 2026 |
| wbb_crosswalk | wehoop-wbb-data | 82 | 2026-09-27T10:26 | 7.2 | 2026 |
| mlb_parks | sdv-reference-data | 2 | 2026-09-27T19:55 | 6.8 |  |
| mbb_groups | sdv-reference-data | 60 | 2026-09-28T13:33 | 6.1 | 2027 |
| mlb_groups | sdv-reference-data | 260 | 2026-09-28T13:34 | 6.1 | 2026 |
| wbb_groups | sdv-reference-data | 60 | 2026-09-28T13:34 | 6.1 | 2027 |
| nfl_rosters | nfl-data | 29 | 2026-09-28T17:32 | 5.9 | 2026 |
| nfl_players | nfl-data | 5 | 2026-09-28T17:33 | 5.9 |  |
| nfl_player_stats | nfl-data | 5 | 2026-09-28T17:33 | 5.9 |  |
| nfl_team_stats | nfl-data | 5 | 2026-09-28T17:34 | 5.9 |  |
| nfl_espn_qbr | nfl-data | 6 | 2026-09-28T17:39 | 5.9 |  |
| cfb_fpi_weekly | cfbfastR-cfb-data | 70 | 2026-09-28T20:22 | 5.8 | 2026 |
| wnba_crosswalk | wehoop-wnba-data | 16 | 2026-09-29T10:43 | 5.2 | 2026 |
| nfl_ratings_weekly | nfl-data | 32 | 2026-09-29T19:03 | 4.8 | 2026 |
| cfb_groups | sdv-reference-data | 322 | 2026-09-29T22:30 | 4.7 | 2026 |
| espn_nfl_pbp | nfl-data | 26 | 2026-09-29T23:32 | 4.6 | 2026 |
| espn_nfl_qa | nfl-data | 3 | 2026-09-29T23:32 | 4.6 | 2026 |
| espn_nfl_team_box | nfl-data | 26 | 2026-09-29T23:32 | 4.6 | 2026 |
| espn_nfl_player_box | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_team | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_passing | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_rushing | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_receiving | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_defensive | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_turnover | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_drives | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_situational | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_defensive_players | nfl-data | 25 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_adv_specialists | nfl-data | 23 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_play_participants | nfl-data | 14 | 2026-09-29T23:33 | 4.6 | 2026 |
| espn_nfl_drives | nfl-data | 26 | 2026-09-29T23:33 | 4.6 | 2026 |
| nfl_rolling_windows | nfl-data | 26 | 2026-09-29T23:35 | 4.6 | 2026 |
| espn_nfl_coach_careers | nfl-data | 1 | 2026-09-29T23:35 | 4.6 |  |
| wbb_ratings | wehoop-wbb-data | 23 | 2026-09-30T04:46 | 4.4 | 2026 |
| mbb_ratings | hoopR-mbb-data | 26 | 2026-09-30T05:15 | 4.4 | 2026 |
| mbb_player_value | hoopR-mbb-data | 27 | 2026-09-30T05:16 | 4.4 | 2026 |
| wbb_player_value | wehoop-wbb-data | 19 | 2026-09-30T05:17 | 4.4 | 2026 |
| nfl_model_pbp | nfl-data | 32 | 2026-09-30T05:27 | 4.4 | 2026 |
| espn_cfb_model_artifacts | cfbfastR-cfb-data | 29 | 2026-09-30T14:03 | 4.0 |  |
| nba_stats_synergy | hoopR-nba-stats-data | 794 | 2026-09-30T14:05 | 4.0 | 2026 |
| nba_stats_hustle | hoopR-nba-stats-data | 90 | 2026-09-30T14:24 | 4.0 | 2026 |
| nba_stats_matchups | hoopR-nba-stats-data | 56 | 2026-09-30T14:28 | 4.0 | 2026 |
| nba_stats_draft_combine | hoopR-nba-stats-data | 137 | 2026-09-30T14:36 | 4.0 | 2027 |
| espn_nfl_adv_player_usage | nfl-data | 25 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_position_group_usage | nfl-data | 14 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_tackles | nfl-data | 14 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_position_group_tackles | nfl-data | 14 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_team_usage | nfl-data | 26 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_drive_scripting | nfl-data | 26 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_st_kickers | nfl-data | 23 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_st_punters | nfl-data | 23 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_st_returners | nfl-data | 23 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_st_blocks | nfl-data | 21 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_adv_st_team | nfl-data | 26 | 2026-09-30T14:50 | 4.0 | 2026 |
| espn_nfl_usage_players | nfl-data | 25 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_position_groups | nfl-data | 14 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_tackles | nfl-data | 14 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_position_group_tackles | nfl-data | 14 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_teams | nfl-data | 26 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_drive_scripting | nfl-data | 26 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_st_kickers | nfl-data | 23 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_st_punters | nfl-data | 23 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_st_returners | nfl-data | 23 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_st_blocks | nfl-data | 21 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_usage_st_team | nfl-data | 26 | 2026-09-30T14:52 | 4.0 | 2026 |
| espn_nfl_team_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 4.0 | 2026 |
| espn_nfl_coach_tendencies | nfl-data | 26 | 2026-09-30T14:53 | 4.0 | 2026 |
| nba_stats_game_rosters | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 3.6 | 2026 |
| nba_stats_officials | hoopR-nba-stats-data | 94 | 2026-10-01T00:31 | 3.6 | 2026 |
| nba_stats_player_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 3.6 | 2026 |
| nba_stats_shots | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 3.6 | 2026 |
| nba_stats_team_boxscores | hoopR-nba-stats-data | 94 | 2026-10-01T00:32 | 3.6 | 2026 |
| nba_stats_game_matchups | hoopR-nba-stats-data | 31 | 2026-10-01T01:50 | 3.5 | 2026 |
| nfl_metric_curves | nfl-data | 32 | 2026-10-01T12:07 | 3.1 | 2026 |
| nba_stats_rolling_windows | hoopR-nba-stats-data | 92 | 2026-10-01T22:01 | 2.7 | 2026 |
| nba_stats_metric_curves | hoopR-nba-stats-data | 92 | 2026-10-01T22:33 | 2.7 | 2026 |
| mlb_game_state | baseballr-data | 116 | 2026-10-03T15:15 | 1.0 | 2026 |
| ncaa_mfb_teams | ncaa-mfb-football-data | 46 | 2026-10-03T15:41 | 1.0 | 2026 |
| ncaa_mfb_schedule | ncaa-mfb-football-data | 46 | 2026-10-03T15:42 | 1.0 | 2026 |
| ncaa_mfb_rosters | ncaa-mfb-football-data | 46 | 2026-10-03T15:42 | 1.0 | 2026 |
| ncaa_mfb_pbp | ncaa-mfb-football-data | 46 | 2026-10-03T15:42 | 1.0 | 2026 |
| ncaa_mfb_pbp_cfbfastr | ncaa-mfb-football-data | 46 | 2026-10-03T15:42 | 1.0 | 2026 |
| ncaa_mfb_team_stats | ncaa-mfb-football-data | 46 | 2026-10-03T15:42 | 1.0 | 2026 |
| ncaa_mfb_player_stats | ncaa-mfb-football-data | 46 | 2026-10-03T15:43 | 1.0 | 2026 |
| ncaa_mfb_drives | ncaa-mfb-football-data | 46 | 2026-10-03T15:43 | 1.0 | 2026 |
| ncaa_mfb_officials | ncaa-mfb-football-data | 46 | 2026-10-03T15:43 | 1.0 | 2026 |
| ncaa_mfb_linescore | ncaa-mfb-football-data | 46 | 2026-10-03T15:43 | 1.0 | 2026 |
| ncaa_mfb_qa | ncaa-mfb-football-data | 8 | 2026-10-03T15:43 | 1.0 | 2026 |
| mlb_hitting_models | baseballr-data | 110 | 2026-10-03T15:59 | 1.0 | 2026 |
| mlb_fielding_models | baseballr-data | 80 | 2026-10-03T16:00 | 1.0 | 2026 |
| mlb_pitching_models | baseballr-data | 113 | 2026-10-03T16:01 | 1.0 | 2026 |
| cfb_ratings | cfbfastR-cfb-data | 74 | 2026-10-03T17:01 | 0.9 | 2026 |
| espn_cfb_injuries | cfbfastR-cfb-data | 3 | 2026-10-03T17:02 | 0.9 | 2026 |
| espn_mlb_injuries | cfbfastR-cfb-data | 3 | 2026-10-03T17:02 | 0.9 | 2026 |
| espn_nba_injuries | cfbfastR-cfb-data | 3 | 2026-10-03T17:02 | 0.9 | 2027 |
| espn_nfl_injuries | cfbfastR-cfb-data | 3 | 2026-10-03T17:03 | 0.9 | 2026 |
| espn_nhl_injuries | cfbfastR-cfb-data | 4 | 2026-10-03T17:03 | 0.9 | 2027 |
| espn_wnba_injuries | cfbfastR-cfb-data | 3 | 2026-10-03T17:03 | 0.9 | 2026 |
| espn_mlb_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-03T17:05 | 0.9 | 2026 |
| espn_nba_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-03T17:05 | 0.9 | 2027 |
| espn_nfl_depthcharts | cfbfastR-cfb-data | 3 | 2026-10-03T17:05 | 0.9 | 2026 |
| cfb_poll_analytics | cfbfastR-cfb-data | 73 | 2026-10-03T17:45 | 0.9 | 2026 |
| cfb_poll_week_summary | cfbfastR-cfb-data | 73 | 2026-10-03T17:45 | 0.9 | 2026 |
| nhl_pbp_full | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_skater_boxscores | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_goalie_boxscores | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_team_boxscores | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_game_info | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_game_rosters | fastRhockey-nhl-data | 58 | 2026-10-04T08:01 | 0.3 | 2027 |
| nhl_shifts | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_scoring | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_penalties | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_scratches | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_linescore | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_three_stars | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_officials | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_shots_by_period | fastRhockey-nhl-data | 58 | 2026-10-04T08:02 | 0.3 | 2027 |
| nhl_pbp_lite | fastRhockey-nhl-data | 67 | 2026-10-04T08:03 | 0.3 | 2027 |
| nhl_player_boxscores | fastRhockey-nhl-data | 58 | 2026-10-04T08:03 | 0.3 | 2027 |
| nhl_schedules | fastRhockey-nhl-data | 64 | 2026-10-04T08:03 | 0.3 | 2027 |
| espn_wnba_pbp | wehoop-wnba-data | 79 | 2026-10-04T10:39 | 0.2 | 2026 |
| espn_wnba_team_boxscores | wehoop-wnba-data | 76 | 2026-10-04T10:39 | 0.2 | 2026 |
| espn_wnba_player_boxscores | wehoop-wnba-data | 79 | 2026-10-04T10:39 | 0.2 | 2026 |
| espn_wnba_player_core | wehoop-wnba-data | 76 | 2026-10-04T10:40 | 0.2 | 2026 |
| espn_wnba_schedules | wehoop-wnba-data | 85 | 2026-10-04T10:40 | 0.2 | 2026 |
| espn_wnba_shots | wehoop-wnba-data | 80 | 2026-10-04T10:40 | 0.2 | 2026 |
| espn_wnba_player_season_stats | wehoop-wnba-data | 75 | 2026-10-04T10:41 | 0.2 | 2026 |
| espn_wnba_team_season_stats | wehoop-wnba-data | 75 | 2026-10-04T10:41 | 0.2 | 2026 |
| espn_wnba_standings | wehoop-wnba-data | 76 | 2026-10-04T10:41 | 0.2 | 2026 |
| espn_wnba_game_rosters | wehoop-wnba-data | 80 | 2026-10-04T10:42 | 0.2 | 2026 |
| espn_wnba_officials | wehoop-wnba-data | 73 | 2026-10-04T10:42 | 0.2 | 2026 |
| nfl_team_summaries | nfl-data | 30 | 2026-10-04T10:51 | 0.2 | 2026 |
| nfl_passing | nfl-data | 30 | 2026-10-04T10:51 | 0.2 | 2026 |
| nfl_rushing | nfl-data | 30 | 2026-10-04T10:51 | 0.2 | 2026 |
| nfl_receiving | nfl-data | 30 | 2026-10-04T10:51 | 0.2 | 2026 |
| nfl_percentiles | nfl-data | 30 | 2026-10-04T10:52 | 0.2 | 2026 |
| nfl_player_percentiles | nfl-data | 30 | 2026-10-04T10:52 | 0.2 | 2026 |
| nfl_league_averages | nfl-data | 30 | 2026-10-04T10:52 | 0.2 | 2026 |
| nfl_team_opponent_splits | nfl-data | 30 | 2026-10-04T10:52 | 0.2 | 2026 |
| espn_cfb_adv_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-04T11:36 | 0.1 | 2026 |
| espn_cfb_usage_players | cfbfastR-cfb-data | 73 | 2026-10-04T11:41 | 0.1 | 2026 |
| espn_cfb_usage_position_groups | cfbfastR-cfb-data | 43 | 2026-10-04T11:45 | 0.1 | 2026 |
| nfl_ngs_schedules | nfl-ngs-data | 41 | 2026-10-04T11:47 | 0.1 | 2026 |
| nfl_ngs_teams | nfl-ngs-data | 33 | 2026-10-04T11:47 | 0.1 | 2026 |
| nfl_ngs_passing | nfl-ngs-data | 27 | 2026-10-04T11:47 | 0.1 | 2026 |
| nfl_ngs_rushing | nfl-ngs-data | 27 | 2026-10-04T11:48 | 0.1 | 2026 |
| nfl_ngs_receiving | nfl-ngs-data | 27 | 2026-10-04T11:48 | 0.1 | 2026 |
| nfl_ngs_statboard_leaders | nfl-ngs-data | 27 | 2026-10-04T11:48 | 0.1 | 2026 |
| nfl_ngs_leaders | nfl-ngs-data | 27 | 2026-10-04T11:48 | 0.1 | 2026 |
| nfl_ngs_gamecenter_passers | nfl-ngs-data | 41 | 2026-10-04T11:49 | 0.1 | 2026 |
| nfl_ngs_gamecenter_rushers | nfl-ngs-data | 29 | 2026-10-04T11:49 | 0.1 | 2026 |
| nfl_ngs_gamecenter_receivers | nfl-ngs-data | 29 | 2026-10-04T11:49 | 0.1 | 2026 |
| nfl_ngs_gamecenter_pass_rushers | nfl-ngs-data | 27 | 2026-10-04T11:49 | 0.1 | 2026 |
| nfl_ngs_gamecenter_leaders | nfl-ngs-data | 27 | 2026-10-04T11:49 | 0.1 | 2026 |
| nfl_ngs_highlights | nfl-ngs-data | 23 | 2026-10-04T11:50 | 0.1 | 2026 |
| espn_cfb_usage_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T11:50 | 0.1 | 2026 |
| espn_wnba_rosters | wehoop-wnba-data | 14 | 2026-10-04T11:50 | 0.1 | 2026 |
| nfl_ngs_highlight_participation | nfl-ngs-data | 23 | 2026-10-04T11:51 | 0.1 | 2026 |
| espn_nba_schedules | hoopR-nba-data | 88 | 2026-10-04T11:51 | 0.1 | 2027 |
| espn_nba_rosters | hoopR-nba-data | 14 | 2026-10-04T11:52 | 0.1 | 2027 |
| espn_nba_draft | hoopR-nba-data | 80 | 2026-10-04T11:52 | 0.1 | 2027 |
| nfl_ngs_highlight_events | nfl-ngs-data | 23 | 2026-10-04T11:53 | 0.1 | 2026 |
| nfl_ngs_highlight_tracking | nfl-ngs-data | 14 | 2026-10-04T11:53 | 0.1 | 2026 |
| espn_cfb_usage_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T11:54 | 0.1 | 2026 |
| espn_cfb_usage_teams | cfbfastR-cfb-data | 73 | 2026-10-04T11:58 | 0.1 | 2026 |
| espn_cfb_usage_drive_scripting | cfbfastR-cfb-data | 73 | 2026-10-04T12:02 | 0.1 | 2026 |
| espn_cfb_adv_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-04T12:07 | 0.1 | 2026 |
| espn_womens_college_basketball_rosters | wehoop-wbb-data | 11 | 2026-10-04T12:11 | 0.1 | 2027 |
| espn_cfb_adv_st_punters | cfbfastR-cfb-data | 73 | 2026-10-04T12:12 | 0.1 | 2026 |
| espn_cfb_adv_st_returners | cfbfastR-cfb-data | 73 | 2026-10-04T12:16 | 0.1 | 2026 |
| espn_cfb_adv_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-04T12:20 | 0.1 | 2026 |
| espn_cfb_adv_st_team | cfbfastR-cfb-data | 73 | 2026-10-04T12:24 | 0.1 | 2026 |
| espn_cfb_usage_st_kickers | cfbfastR-cfb-data | 73 | 2026-10-04T12:28 | 0.1 | 2026 |
| espn_cfb_usage_st_punters | cfbfastR-cfb-data | 73 | 2026-10-04T12:32 | 0.1 | 2026 |
| espn_cfb_usage_st_returners | cfbfastR-cfb-data | 73 | 2026-10-04T12:37 | 0.1 | 2026 |
| espn_cfb_usage_st_blocks | cfbfastR-cfb-data | 61 | 2026-10-04T12:41 | 0.1 | 2026 |
| espn_cfb_usage_st_team | cfbfastR-cfb-data | 73 | 2026-10-04T12:45 | 0.1 | 2026 |
| espn_cfb_adv_team_gamelog | cfbfastR-cfb-data | 73 | 2026-10-04T12:46 | 0.1 | 2026 |
| cfb_team_opponent_splits | cfbfastR-cfb-data | 73 | 2026-10-04T12:46 | 0.1 | 2026 |
| cfb_metric_curves | cfbfastR-cfb-data | 73 | 2026-10-04T12:46 | 0.1 | 2026 |
| espn_cfb_qa | cfbfastR-cfb-data | 96 | 2026-10-04T12:53 | 0.1 | 2026 |
| cfb_schedules | cfbfastR-cfb-data | 80 | 2026-10-04T12:53 | 0.1 | 2026 |
| espn_cfb_team_tendencies | cfbfastR-cfb-data | 73 | 2026-10-04T12:54 | 0.1 | 2026 |
| espn_cfb_coach_tendencies | cfbfastR-cfb-data | 73 | 2026-10-04T12:55 | 0.1 | 2026 |
| espn_cfb_rosters | cfbfastR-cfb-data | 76 | 2026-10-04T12:56 | 0.1 | 2026 |
| cfb_rolling_windows | cfbfastR-cfb-data | 73 | 2026-10-04T12:58 | 0.1 | 2026 |
| cfb_ratings_weekly | cfbfastR-cfb-data | 73 | 2026-10-04T12:58 | 0.1 | 2026 |
| cfb_matchup_features | cfbfastR-cfb-data | 43 | 2026-10-04T13:03 | 0.1 | 2026 |
| cfb_matchup_line | cfbfastR-cfb-data | 40 | 2026-10-04T13:15 | 0.1 | 2026 |
| cfb_recruits | cfbfastR-cfb-data | 27 | 2026-10-04T13:16 | 0.1 | 2026 |
| cfb_team_talent | cfbfastR-cfb-data | 24 | 2026-10-04T13:16 | 0.1 | 2026 |
| cfb_returning_production | cfbfastR-cfb-data | 25 | 2026-10-04T13:16 | 0.1 | 2026 |
| cfb_team_portal | cfbfastR-cfb-data | 14 | 2026-10-04T13:16 | 0.1 | 2026 |
| espn_cfb_coach_careers | cfbfastR-cfb-data | 7 | 2026-10-04T13:17 | 0.1 |  |
| cfbfastR_cfb_pbp | cfbfastR-data | 54 | 2026-10-04T13:18 | 0.1 | 2026 |
| espn_cfb_percentiles | cfbfastR-cfb-data | 73 | 2026-10-04T13:27 | 0.1 | 2026 |
| espn_cfb_team_summaries | cfbfastR-cfb-data | 73 | 2026-10-04T13:27 | 0.1 | 2026 |
| espn_cfb_passing | cfbfastR-cfb-data | 73 | 2026-10-04T13:28 | 0.1 | 2026 |
| espn_cfb_rushing | cfbfastR-cfb-data | 73 | 2026-10-04T13:28 | 0.1 | 2026 |
| espn_cfb_receiving | cfbfastR-cfb-data | 73 | 2026-10-04T13:28 | 0.1 | 2026 |
| cfb_league_averages | cfbfastR-cfb-data | 73 | 2026-10-04T13:28 | 0.1 | 2026 |
| cfb_team_summaries_weekly | cfbfastR-cfb-data | 73 | 2026-10-04T13:31 | 0.1 | 2026 |
| espn_cfb_pbp | cfbfastR-cfb-data | 72 | 2026-10-04T13:39 | 0.1 | 2026 |
| espn_cfb_play_participants | cfbfastR-cfb-data | 55 | 2026-10-04T13:42 | 0.1 | 2026 |
| espn_cfb_team_box | cfbfastR-cfb-data | 95 | 2026-10-04T13:43 | 0.0 | 2026 |
| espn_cfb_player_box | cfbfastR-cfb-data | 95 | 2026-10-04T13:44 | 0.0 | 2026 |
| espn_cfb_drives | cfbfastR-cfb-data | 95 | 2026-10-04T13:45 | 0.0 | 2026 |
| espn_cfb_game_rosters | cfbfastR-cfb-data | 95 | 2026-10-04T13:48 | 0.0 | 2026 |
| espn_cfb_betting | cfbfastR-cfb-data | 95 | 2026-10-04T13:49 | 0.0 | 2026 |
| espn_cfb_schedules | cfbfastR-cfb-data | 95 | 2026-10-04T13:50 | 0.0 | 2026 |
| espn_cfb_linescores | cfbfastR-cfb-data | 95 | 2026-10-04T13:51 | 0.0 | 2026 |
| espn_cfb_power_index | cfbfastR-cfb-data | 81 | 2026-10-04T13:52 | 0.0 | 2026 |
| espn_cfb_adv_team | cfbfastR-cfb-data | 73 | 2026-10-04T13:54 | 0.0 | 2026 |
| espn_cfb_adv_passing | cfbfastR-cfb-data | 73 | 2026-10-04T13:55 | 0.0 | 2026 |
| espn_cfb_adv_rushing | cfbfastR-cfb-data | 73 | 2026-10-04T13:56 | 0.0 | 2026 |
| espn_cfb_adv_receiving | cfbfastR-cfb-data | 73 | 2026-10-04T13:57 | 0.0 | 2026 |
| espn_cfb_adv_defensive | cfbfastR-cfb-data | 73 | 2026-10-04T13:58 | 0.0 | 2026 |
| espn_cfb_adv_turnover | cfbfastR-cfb-data | 73 | 2026-10-04T14:00 | 0.0 | 2026 |
| espn_cfb_adv_drives | cfbfastR-cfb-data | 73 | 2026-10-04T14:01 | 0.0 | 2026 |
| espn_cfb_adv_situational | cfbfastR-cfb-data | 73 | 2026-10-04T14:02 | 0.0 | 2026 |
| espn_cfb_adv_defensive_players | cfbfastR-cfb-data | 73 | 2026-10-04T14:03 | 0.0 | 2026 |
| espn_cfb_adv_specialists | cfbfastR-cfb-data | 73 | 2026-10-04T14:04 | 0.0 | 2026 |
| espn_cfb_adv_player_usage | cfbfastR-cfb-data | 73 | 2026-10-04T14:15 | 0.0 | 2026 |
| espn_cfb_adv_position_group_usage | cfbfastR-cfb-data | 43 | 2026-10-04T14:25 | 0.0 | 2026 |
| wnba_player_impact | wehoop-wnba-stats-data | 96 | 2026-10-04T14:31 | 0.0 | 2026 |
| wnba_stats_possessions | wehoop-wnba-stats-data | 91 | 2026-10-04T14:34 | 0.0 | 2026 |
| wnba_stats_game_lineups | wehoop-wnba-stats-data | 91 | 2026-10-04T14:34 | 0.0 | 2026 |
| wnba_stats_coaches | wehoop-wnba-stats-data | 92 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_draft | wehoop-wnba-stats-data | 95 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_game_rosters | wehoop-wnba-stats-data | 95 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_lineups | wehoop-wnba-stats-data | 8 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_metric_curves | wehoop-wnba-stats-data | 93 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_officials | wehoop-wnba-stats-data | 74 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_pbp | wehoop-wnba-stats-data | 99 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_player_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-04T14:35 | 0.0 | 2026 |
| espn_cfb_adv_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T14:35 | 0.0 | 2026 |
| wnba_stats_player_game_logs | wehoop-wnba-stats-data | 95 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_player_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_rolling_windows | wehoop-wnba-stats-data | 93 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_rosters | wehoop-wnba-stats-data | 95 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_schedules | wehoop-wnba-stats-data | 105 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_shots | wehoop-wnba-stats-data | 95 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_standings | wehoop-wnba-stats-data | 8 | 2026-10-04T14:36 | 0.0 | 2026 |
| wnba_stats_team_boxscores | wehoop-wnba-stats-data | 8 | 2026-10-04T14:37 | 0.0 | 2026 |
| wnba_stats_team_season_stats | wehoop-wnba-stats-data | 8 | 2026-10-04T14:37 | 0.0 | 2026 |
| wnba_stats_leaguedash | wehoop-wnba-stats-data | 771 | 2026-10-04T14:41 | 0.0 | 2026 |
| espn_cfb_adv_position_group_tackles | cfbfastR-cfb-data | 43 | 2026-10-04T14:45 | 0.0 | 2026 |
| espn_cfb_adv_team_usage | cfbfastR-cfb-data | 73 | 2026-10-04T14:55 | 0.0 | 2026 |
| espn_cfb_player_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_cfb_team_boxscores | cfbfastR-data | 0 | empty |  |  |
| espn_mbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |
| espn_wbb_injuries | cfbfastR-cfb-data | 0 | empty |  |  |

## Producers

One row per repo that publishes to `sportsdataverse-data` (config: `producers.json`). `data updated` and `through season` follow the play-by-play tags; `any tag updated` is the newest asset across all of the producer's tags. `idle` = out of season, never an alarm.

| repo | state | in season | data updated | any tag updated | through season | update workflows |
|---|---|---|---|---|---|---|
| [cfbfastR-cfb-data](https://github.com/sportsdataverse/cfbfastR-cfb-data) | fresh | yes | 2026-10-04 | 2026-10-04 | 2026 | `daily_cfb.yml` success 2026-09-29<br>`cfb_ratings_cron.yml` success 2026-10-02<br>`cfb_fpi_weekly.yml` success 2026-10-02<br>`cfb_recruiting_proj_cron.yml` failure 2026-08-05<br>`cfb_model_pipeline.yml` no runs<br>`espn_daily_snapshots.yml` success 2026-10-02 |
| [cfbfastR-data](https://github.com/sportsdataverse/cfbfastR-data) | fresh | yes | 2026-10-04 | 2026-10-04 | 2026 | `daily_cfb.yml` success 2026-10-04 |
| [ncaa-mfb-football-data](https://github.com/sportsdataverse/ncaa-mfb-football-data) | fresh | yes | 2026-10-03 | 2026-10-03 | 2026 | `daily_ncaa_mfb_data.yml` success 2026-10-03 |
| [nfl-data](https://github.com/sportsdataverse/nfl-data) | fresh | yes | 2026-09-29 | 2026-10-04 | 2026 | `espn_nfl_cron.yml` success 2026-09-29<br>`nfl_pbp_cron.yml` success 2026-09-30<br>`nfl_ratings_weekly.yml` success 2026-09-29<br>`nfl_rosters_players_cron.yml` success 2026-09-28<br>`nfl_model_pipeline.yml` no runs |
| [nfl-ngs-data](https://github.com/sportsdataverse/nfl-ngs-data) | fresh | yes | 2026-10-04 | 2026-10-04 | 2026 | `daily_ngs.yml` success 2026-10-04 |
| [hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) | idle | no | 2026-09-19 | 2026-09-30 | 2026 | `daily_mbb.yml` skipped 2026-09-30<br>`mbb_models_cron.yml` no runs |
| [ncaa-mbb-hoops-data](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | idle | no | 2026-08-12 | 2026-08-24 | 2026 | `ncaa_mbb_models.yml` no runs |
| [hoopR-nba-data](https://github.com/sportsdataverse/hoopR-nba-data) | idle | no | 2026-09-09 | 2026-10-04 | 2026 | `daily_nba.yml` success 2026-10-03 |
| [hoopR-nba-stats-data](https://github.com/sportsdataverse/hoopR-nba-stats-data) | idle | no | 2026-08-13 | 2026-10-01 | 2026 | `daily_nba_stats.yml` disabled 2026-07-12<br>`nba_models.yml` no runs<br>`annual_nba_stats_draft.yml` no runs |
| [wehoop-wbb-data](https://github.com/sportsdataverse/wehoop-wbb-data) | idle | no | 2026-09-19 | 2026-10-04 | 2026 | `daily_wbb.yml` success 2026-09-09<br>`weekly_wbb.yml` success 2026-09-27<br>`wbb_models_cron.yml` no runs |
| [ncaa-wbb-hoops-data](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | idle | no | 2026-08-18 | 2026-08-24 | 2026 | `ncaa_wbb_models.yml` no runs |
| [wehoop-wnba-data](https://github.com/sportsdataverse/wehoop-wnba-data) | fresh | yes | 2026-10-04 | 2026-10-04 | 2026 | `daily_wnba.yml` success 2026-10-04<br>`weekly_wnba.yml` success 2026-10-04<br>`annual_wnba_draft.yml` success 2026-05-30 |
| [wehoop-wnba-stats-data](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | fresh | yes | 2026-10-04 | 2026-10-04 | 2026 | `daily_wnba_stats.yml` success 2026-10-04<br>`wnba_models.yml` no runs<br>`annual_wnba_stats_draft.yml` success 2026-05-30 |
| [fastRhockey-nhl-data](https://github.com/sportsdataverse/fastRhockey-nhl-data) | idle | no | 2026-10-04 | 2026-10-04 | 2027 | `daily_nhl_python.yml` disabled 2026-07-22<br>`nhl_model_pipeline.yml` no runs |
| [fastRhockey-pwhl-data](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | idle | no | 2026-07-22 | 2026-09-02 | 2026 | `daily_pwhl_python.yml` no runs<br>`pwhl_xg_cron.yml` no runs |
| [baseballr-data](https://github.com/sportsdataverse/baseballr-data) | stale | yes | 2026-09-10 | 2026-10-03 | 2026 | `mlb_models_cron.yml` success 2026-10-03<br>`daily_ncaa_baseball.yml` failure 2026-08-01 |
| [sdv-reference-data](https://github.com/sportsdataverse/sdv-reference-data) | fresh | yes | 2026-09-29 | 2026-09-29 | 2027 | — |

## Red default-branch workflows

| repo | workflow | conclusion | last run | age (d) |
|---|---|---|---|---|
| sportsdataverse/baseballr-data | Update NCAA Baseball Data | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/30698726326) | 64.1 |
| sportsdataverse/baseballr-data | orphan-scripts | failure | [run](https://github.com/sportsdataverse/baseballr-data/actions/runs/37211098016) | 0.0 |
| sportsdataverse/cfbfastR | R-hub | cancelled | [run](https://github.com/sportsdataverse/cfbfastR/actions/runs/32725263629) | 41.1 |
| sportsdataverse/cfbfastR-cfb-data | CFB Recruiting Projections | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions/runs/31015046584) | 60.0 |
| sportsdataverse/cfbfastR-cfb-raw | Scrape CFB Raw Data | cancelled | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/33256748632) | 36.0 |
| sportsdataverse/cfbfastR-cfb-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/cfbfastR-cfb-raw/actions/runs/36903181691) | 2.9 |
| sportsdataverse/hoopR | R-CMD-check | failure | [run](https://github.com/sportsdataverse/hoopR/actions/runs/37044020360) | 1.9 |
| sportsdataverse/hoopR | R-hub | cancelled | [run](https://github.com/sportsdataverse/hoopR/actions/runs/27192006294) | 117.3 |
| sportsdataverse/ncaa-wbb-hoops-raw | orphan-scripts | failure | [run](https://github.com/sportsdataverse/ncaa-wbb-hoops-raw/actions/runs/36902076422) | 2.9 |
| sportsdataverse/sportsdataverse-py | codegen | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37209683719) | 0.0 |
| sportsdataverse/sportsdataverse-py | tests | cancelled | [run](https://github.com/sportsdataverse/sportsdataverse-py/actions/runs/37209683894) | 0.0 |
| sportsdataverse/sportsdataverse-web | Update data | failure | [run](https://github.com/sportsdataverse/sportsdataverse-web/actions/runs/33084519531) | 38.0 |
| sportsdataverse/wehoop-wbb-raw | Daily WBB Raw Scrape | failure | [run](https://github.com/sportsdataverse/wehoop-wbb-raw/actions/runs/25519402950) | 149.8 |

## Open PRs (most idle first)

| repo | PR | author | age (d) | idle (d) | draft |
|---|---|---|---|---|---|
| BillPetti/baseballr | [#424](https://github.com/BillPetti/baseballr/pull/424) stats is Imports, not Suggests | MichaelChirico | 28.3 | 28.3 |  |
| sportsdataverse/sportypy | [#13](https://github.com/sportsdataverse/sportypy/pull/13) Fix boundary filtering for constrained statistical plots | bensynapse | 21.0 | 20.9 |  |
| sportsdataverse/sportyR | [#42](https://github.com/sportsdataverse/sportyR/pull/42) first push - bwf specification for badminton court | AimanFariz | 497.4 | 18.7 |  |
| sportsdataverse/sportyR | [#52](https://github.com/sportsdataverse/sportyR/pull/52) Add NCAA softball field via geom_softball() | billyfryer | 5.0 | 3.3 |  |
| sportsdataverse/sdv-assets | [#11](https://github.com/sportsdataverse/sdv-assets/pull/11) data: monthly capture 2026-10-01 | saiemgilani | 3.3 | 3.3 |  |
| saiemgilani/game-on-paper-app | [#295](https://github.com/saiemgilani/game-on-paper-app/pull/295) Update astro depends to see if #205 is fixed | a5ehren | 0.8 | 0.8 |  |
| saiemgilani/game-on-paper-app | [#264](https://github.com/saiemgilani/game-on-paper-app/pull/264) test(tables): render-level contract tests, twin parity and aggregation | saiemgilani | 15.5 | 0.2 |  |
| sportsdataverse/sportsdataverse-py | [#664](https://github.com/sportsdataverse/sportsdataverse-py/pull/664) perf(docs): keep table rows out of the search index | saiemgilani | 0.0 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#284](https://github.com/saiemgilani/game-on-paper-app/pull/284) feat(team): Five Factors table on the season team page (preview) | saiemgilani | 6.8 | 0.0 |  |
| saiemgilani/game-on-paper-app | [#270](https://github.com/saiemgilani/game-on-paper-app/pull/270) Fixing design issues + Team Stats SSR + splitting Situational Metrics | akeaswaran | 14.6 | 0.0 |  |

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
| sportsdataverse/wehoop-wnba-stats-data | 1 | 0 |
| sportsdataverse/fastRhockey-nhl-data | 1 | 0 |
| sportsdataverse/cfbfastR-cfb-data | 1 | 0 |

## Release-asset freshness (data producers)

| repo | latest tag | releases | newest asset | age (d) | last push (d) |
|---|---|---|---|---|---|
| sportsdataverse/hoopR-nba-stats-raw | nba-stats-raw-json | 1 | 2026-10-01T01:33 | 3.6 | 0.0 |
| sportsdataverse/wehoop-wnba-stats-raw | wnba-stats-raw-json | 1 | 2026-07-29T21:35 | 66.7 | 0.0 |
| sportsdataverse/amf-location-data | amf_tracking_parquet | 2 | 2024-11-18T08:20 | 685.3 | 915.9 |
| sportsdataverse/sportsdataverse-data | wnba_stats_rolling_windows | 377 | 2026-10-04T14:55 | 0.0 | 2.6 |
| sportsdataverse/cfbfastR-cfb-data | espn_cfb_team_box | 19 |  | None | 0.0 |

## Package repos — latest release

| repo | latest tag | published | last push (d) |
|---|---|---|---|
| BillPetti/baseballr | v2.0.0 | 2026-08-27 | 4.0 |
| sportsdataverse/cfbfastR | v3.0.0 | 2026-08-27 | 3.2 |
| sportsdataverse/cfbseedR | v0.2.0 | 2026-09-09 | 4.0 |
| sportsdataverse/fastRhockey | v1.0.0 | 2026-08-27 | 4.0 |
| sportsdataverse/hoopR | v3.1.0 | 2026-08-27 | 4.0 |
| sportsdataverse/oddsapiR | v1.0.1 | 2026-08-28 | 4.0 |
| sportsdataverse/sdvplotR | sdvplotr_infrastructure | 2026-09-26 | 0.0 |
| sportsdataverse/sportsdataverse-js | v3.0.0 | 2026-06-17 | 4.0 |
| sportsdataverse/sportsdataverse-py | v0.1.4 | 2026-09-01 | 0.0 |
| sportsdataverse/sportyR | v2.1.0 | 2022-10-31 | 8.3 |
| sportsdataverse/sportypy | v1.0.0 | 2022-09-13 | 8.4 |
| sportsdataverse/wehoop | v3.0.0 | 2026-08-27 | 4.0 |

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
