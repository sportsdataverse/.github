"""Offline tests for ecosystem_status.py (stdlib unittest, no network).

Run: python -m unittest discover -s .github/scripts/tests

Ruling map (each has at least one test that goes red when the rule is broken):
  R-SV-4  idle never red, season windows ........ SeasonWindow, StateMachine.test_idle_is_never_red
  R-SV-8  failing = failure newer than the data . StateMachine.*failing*, Summary.test_non_update_workflow_*
  R-SV-9  through from play-level tags .......... Summary.test_through_tags_limit_through_season
  R-SV-10 empty tags last ....................... Summary.test_release_tags_stalest_first_empty_last
  R-SV-11 producers[].tags is a count ........... Summary.test_tags_is_a_count_with_names_beside_it
  R-SV-12 freshness from play-level tags ........ Summary.test_freshness_follows_play_level_tags
  R-SV-13 API errors never become output ........ GhErrors, Collect
  R-SV-14 completion time, disabled, forks, drafts StateMachine.test_compares_completion_*, Snapshot*
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ecosystem_status as es  # noqa: E402

PRODUCERS = HERE.parents[2] / "status" / "producers.json"
NOW = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)
REPO = "sportsdataverse/r"


def wf(name, file, conclusion=None, created_at=None, completed_at=None, state="active"):
    return {
        "name": name,
        "file": f".github/workflows/{file}",
        "run_id": None,
        "conclusion": conclusion,
        "created_at": created_at,
        "completed_at": completed_at or created_at,
        "age_days": None,
        "url": f"https://github.com/x/actions/workflows/{file}",
        "event": "schedule" if conclusion else None,
        "state": state,
    }


def api_run(rid, file, conclusion, created, completed=None, *, status="completed", event="schedule", head=REPO):
    return {
        "id": rid,
        "name": file,
        "path": f".github/workflows/{file}",
        "status": status,
        "conclusion": conclusion,
        "created_at": created,
        "updated_at": completed or created,
        "html_url": f"https://github.com/{REPO}/actions/runs/{rid}",
        "event": event,
        "head_repository": {"full_name": head} if head else None,
    }


class FakeGh:
    """Stands in for es.gh: first route whose prefix matches wins; errors raise."""

    def __init__(self, routes, errors=()):
        self.routes, self.errors, self.calls = routes, errors, []

    def __call__(self, path, paginate=False, pages_cap=5):
        self.calls.append(path)
        for prefix in self.errors:
            if path.startswith(prefix):
                raise es.GhError(path)
        for prefix, payload in self.routes:
            if path.startswith(prefix):
                return payload
        return None


def rel(newest, season, n=1):
    return {
        "published_at": "2025-01-01T00:00:00Z",
        "assets": n,
        "asset_bytes": 1,
        "newest_asset_at": newest,
        "max_season": season,
    }


def repo(full, wfs, releases=None):
    return {
        "full_name": full,
        "private": False,
        "open_prs": [],
        "open_issues": 0,
        "stale_unassigned_issues": [],
        "workflows": {w["name"]: w for w in wfs},
        "red_workflows": [w["name"] for w in wfs if w["conclusion"] == "failure"],
        "releases": releases or {},
        "latest_release_tag": next(iter(releases or {}), None),
        "newest_asset_at": None,
        "newest_asset_age_days": None,
        "pushed_age_days": 1.0,
    }


def fake_snap():
    """Three producers, one package, a hub with mapped / unmapped / snapshot tags."""
    return {
        "generated_at": NOW.isoformat(),
        "totals": {"repos": 5},
        "repos": {
            "sportsdataverse/sportsdataverse-data": repo(
                "sportsdataverse/sportsdataverse-data",
                [],
                {
                    "espn_wnba_pbp": rel("2026-09-29T00:00:00Z", 2026),
                    "espn_wnba_schedules": rel("2026-09-28T00:00:00Z", 2027),  # pre-season file
                    "espn_wnba_injuries": rel("2026-09-30T00:00:00Z", 2027),
                    "espn_nba_pbp": rel("2026-06-20T00:00:00Z", 2026),
                    "mlb_pbp": rel("2026-09-10T00:00:00Z", 2026),  # stalled play-by-play
                    "mlb_models": rel("2026-09-29T00:00:00Z", 2026),  # unrelated daily output
                    "phf_pbp": rel("2023-03-01T00:00:00Z", 2023),
                    "zzz_new": rel(None, None, 0),
                },
            ),
            "sportsdataverse/wehoop-wnba-data": repo(
                "sportsdataverse/wehoop-wnba-data",
                [
                    wf("Update WNBA Data", "daily_wnba.yml", "success", "2026-09-29T07:00:00Z"),
                    # a red workflow that is NOT an update workflow must not turn the producer red
                    wf("tests", "tests.yml", "failure", "2026-09-30T08:00:00Z"),
                ],
            ),
            "sportsdataverse/cfbfastR-cfb-data": repo(
                "sportsdataverse/cfbfastR-cfb-data",
                [wf("ESPN Daily Snapshots", "espn_daily_snapshots.yml", "success", "2026-09-30T13:00:00Z")],
            ),
            "sportsdataverse/baseballr-data": repo(
                "sportsdataverse/baseballr-data",
                [wf("MLB Models", "mlb_models_cron.yml", "success", "2026-09-29T10:00:00Z")],
            ),
            "sportsdataverse/hoopR": repo(
                "sportsdataverse/hoopR",
                [
                    wf("R-CMD-check", "R-CMD-check.yaml", "failure", "2026-09-20T00:00:00Z"),
                    wf("pkgdown", "pkgdown.yaml"),
                ],
                {"v3.0.0": rel(None, None, 0)},
            ),
        },
    }


def producer(repo_, season, stale, update, through=None, **kw):
    p = {
        "repo": repo_,
        "label": repo_,
        "sport": "x",
        "packages": [],
        "raw_repo": None,
        "schedule": "Daily",
        "season": season,
        "stale_after_days": stale,
        "update_workflows": update,
        **kw,
    }
    if through is not None:
        p["through_tags"] = through
    return p


def fake_cfg():
    return {
        "package_repos": ["sportsdataverse/hoopR"],
        "rules": [
            {"prefix": "espn_wnba_injuries", "repo": "sportsdataverse/cfbfastR-cfb-data", "freshness": False},
            {"prefix": "phf_", "repo": None},
            {"prefix": "espn_wnba_", "repo": "sportsdataverse/wehoop-wnba-data"},
            {"prefix": "mlb_", "repo": "sportsdataverse/baseballr-data"},
        ],
        "producers": [
            producer(
                "sportsdataverse/wehoop-wnba-data",
                {"start": "05-08", "end": "10-20"},
                7,
                ["daily_wnba.yml"],
                ["espn_wnba_pbp"],
                packages=["hoopR"],
            ),
            producer(
                "sportsdataverse/cfbfastR-cfb-data",
                {"start": "08-27", "end": "01-22"},
                12,
                ["espn_daily_snapshots.yml"],
            ),
            producer(
                "sportsdataverse/baseballr-data",
                {"start": "02-13", "end": "11-02"},
                7,
                ["mlb_models_cron.yml"],
                ["mlb_pbp"],
            ),
        ],
    }


def find(summary, suffix):
    return next(p for p in summary["producers"] if p["repo"].endswith(suffix))


class Base(unittest.TestCase):
    def setUp(self):
        es.WARNINGS.clear()


class SeasonWindow(Base):
    WRAP = {"start": "11-03", "end": "04-08"}
    PLAIN = {"start": "05-08", "end": "10-20"}

    def test_wrapping_window_both_boundaries(self):
        f = lambda m, d: es.in_season(self.WRAP, date(2026, m, d))  # noqa: E731
        self.assertFalse(f(11, 2))
        self.assertTrue(f(11, 3))
        self.assertTrue(f(12, 31))
        self.assertTrue(f(1, 1))
        self.assertTrue(f(4, 8))
        self.assertFalse(f(4, 9))
        self.assertFalse(f(7, 1))

    def test_plain_window_both_boundaries(self):
        f = lambda m, d: es.in_season(self.PLAIN, date(2026, m, d))  # noqa: E731
        self.assertFalse(f(5, 7))
        self.assertTrue(f(5, 8))
        self.assertTrue(f(10, 20))
        self.assertFalse(f(10, 21))

    def test_full_year_and_leap_day(self):
        self.assertTrue(es.in_season({"start": "01-01", "end": "12-31"}, date(2028, 2, 29)))
        self.assertTrue(es.in_season({"start": "02-13", "end": "11-02"}, date(2028, 2, 29)))

    def test_days_since_season_start_wraps(self):
        self.assertEqual(es.days_since_season_start(self.WRAP, date(2027, 1, 3)), 61)
        self.assertEqual(es.days_since_season_start(self.WRAP, date(2026, 11, 3)), 0)


class MaxSeason(Base):
    def test_accepts_standalone_year(self):
        self.assertEqual(es.max_season(["play_by_play_2026.parquet"]), 2026)
        self.assertEqual(es.max_season(["a_2019.rds", "b_2025.csv.gz", "timestamp.json"]), 2025)

    def test_rejects_dates_and_long_digit_runs(self):
        self.assertIsNone(es.max_season(["pbp_20260929.parquet"]))
        self.assertIsNone(es.max_season(["game_120255.json", "id_401520281.parquet"]))
        self.assertIsNone(es.max_season(["x_1066.rds", "y_2099.rds"]))  # outside 1950-2049
        self.assertIsNone(es.max_season([]))

    def test_spans_read_as_their_end_year(self):
        self.assertEqual(es.max_season(["shots_2025-26.csv"]), 2026)
        self.assertEqual(es.max_season(["shots_2025_26.parquet"]), 2026)
        self.assertEqual(es.max_season(["x_1999-00.rds"]), 2000)
        self.assertEqual(es.max_season(["snapshot_2026-09-29.json"]), 2026)  # a dashed date is not a span
        self.assertEqual(es.max_season(["nhl_pbp2024.rds", "shots_2023-24.csv"]), 2024)


class Ages(Base):
    def test_age_is_clamped_at_zero(self):
        clamped = es.age_days("2026-09-30T18:00:00Z", NOW)  # uploaded during the run
        self.assertEqual((clamped, str(clamped)), (0.0, "0.0"))
        self.assertEqual(es.age_days("2026-09-29T12:00:00Z", NOW), 1.0)
        self.assertIsNone(es.age_days(None, NOW))


class Rules(Base):
    cfg = es.load_producers(PRODUCERS)

    def owner(self, tag):
        r = es.match_rule(tag, self.cfg["rules"])
        return r and r["repo"]

    def test_specific_prefix_wins(self):
        self.assertEqual(self.owner("nba_stats_pbp"), "sportsdataverse/hoopR-nba-stats-data")
        self.assertEqual(self.owner("nba_player_impact"), "sportsdataverse/hoopR-nba-stats-data")
        self.assertEqual(self.owner("nba_crosswalk"), "sportsdataverse/hoopR-nba-data")
        self.assertEqual(self.owner("cfbfastR_cfb_pbp"), "sportsdataverse/cfbfastR-data")
        self.assertEqual(self.owner("cfb_ratings"), "sportsdataverse/cfbfastR-cfb-data")
        self.assertEqual(self.owner("cfb_groups"), "sportsdataverse/sdv-reference-data")
        self.assertEqual(self.owner("espn_nba_injuries"), "sportsdataverse/cfbfastR-cfb-data")
        self.assertEqual(self.owner("espn_nba_pbp"), "sportsdataverse/hoopR-nba-data")
        self.assertEqual(self.owner("nfl_ngs_passing"), "sportsdataverse/nfl-ngs-data")
        self.assertEqual(self.owner("nfl_pbp"), "sportsdataverse/nfl-data")
        self.assertEqual(self.owner("wnba_stats_pbp"), "sportsdataverse/wehoop-wnba-stats-data")
        self.assertEqual(self.owner("wnba_crosswalk"), "sportsdataverse/wehoop-wnba-data")

    def test_unattributed_and_unknown_stay_unmapped(self):
        self.assertIsNone(self.owner("phf_pbp"))
        self.assertIsNone(self.owner("nhl_xg_models"))
        self.assertIsNone(self.owner("brand_new_family_2027"))

    def _refused(self, cfg):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "producers.json"
            p.write_text(json.dumps(cfg), encoding="utf-8")
            with self.assertRaises(SystemExit):
                es.load_producers(p)

    def test_shadowed_rule_is_refused(self):
        self._refused(
            {
                "package_repos": [],
                "rules": [{"prefix": "nba_", "repo": None}, {"prefix": "nba_stats_", "repo": None}],
                "producers": [],
            }
        )

    def test_rule_repo_typo_is_refused(self):
        cfg = fake_cfg()
        cfg["rules"][2]["repo"] = "sportsdataverse/wehoop-wnba-dat"
        self._refused(cfg)

    def test_through_tags_belong_to_their_producer(self):
        for p in self.cfg["producers"]:
            for t in p.get("through_tags", []):
                self.assertEqual(self.owner(t), p["repo"], t)

    def test_every_producer_entry_is_complete(self):
        keys = {"repo", "label", "sport", "packages", "raw_repo", "schedule", "season", "stale_after_days"}
        for p in self.cfg["producers"]:
            self.assertLessEqual(keys | {"update_workflows"}, set(p), p["repo"])
            for k in ("start", "end"):
                self.assertRegex(p["season"][k], r"^\d\d-\d\d$")


class StateMachine(Base):
    season = {"start": "05-08", "end": "10-20"}
    DATA = "2026-09-20T00:00:00Z"  # newest counted asset

    def ds(self, updated_at, today, season=None, stale=5):
        return es.data_state(updated_at, season or self.season, stale, today, NOW)[0]

    @staticmethod
    def wf_run(conclusion, completed="2026-09-25T00:00:00Z", created=None, state="active"):
        return {"conclusion": conclusion, "created_at": created or completed, "completed_at": completed, "state": state}

    def test_data_states(self):
        self.assertEqual(self.ds("2026-09-29T00:00:00Z", date(2026, 9, 30)), "fresh")
        self.assertEqual(self.ds("2026-09-01T00:00:00Z", date(2026, 9, 30)), "stale")
        self.assertEqual(self.ds("2026-09-01T00:00:00Z", date(2026, 12, 1)), "idle")
        self.assertEqual(self.ds(None, date(2026, 9, 30)), "unknown")

    def test_staleness_clock_starts_at_season_start(self):
        wrap = {"start": "11-03", "end": "04-08"}
        april = "2026-04-07T00:00:00Z"
        self.assertEqual(self.ds(april, date(2026, 11, 5), wrap, 7), "fresh")  # 2 days into the season
        self.assertEqual(self.ds(april, date(2026, 11, 11), wrap, 7), "stale")  # 8 days in, nothing landed

    def test_failing_beats_stale_beats_idle(self):
        r = self.wf_run
        self.assertEqual(es.producer_state("stale", [r("success"), r("failure")], self.DATA), "failing")
        self.assertEqual(es.producer_state("stale", [r("success"), r(None, None), r("cancelled")], self.DATA), "stale")
        self.assertEqual(es.producer_state("idle", [r("success")], self.DATA), "idle")
        self.assertEqual(es.producer_state("unknown", [], None), "unknown")

    def test_failure_older_than_last_data_is_not_failing(self):
        old = self.wf_run("failure", "2026-08-05T00:00:00Z")
        self.assertEqual(es.producer_state("fresh", [old], self.DATA), "fresh")
        self.assertEqual(es.producer_state("stale", [old], self.DATA), "stale")

    def test_failure_newer_than_last_data_is_failing_even_off_season(self):
        self.assertEqual(es.producer_state("idle", [self.wf_run("timed_out")], self.DATA), "failing")
        self.assertEqual(es.producer_state("fresh", [self.wf_run("startup_failure")], self.DATA), "failing")

    def test_failed_run_and_no_data_is_failing(self):
        self.assertEqual(es.producer_state("unknown", [self.wf_run("failure")], None), "failing")

    def test_boundary_failure_at_the_same_instant_as_the_data_is_not_failing(self):
        self.assertEqual(es.producer_state("fresh", [self.wf_run("failure", self.DATA)], self.DATA), "fresh")

    def test_compares_completion_not_start(self):
        # started before the schedules upload, failed on play-by-play after it
        run = self.wf_run("failure", completed="2026-09-20T00:30:00Z", created="2026-09-19T23:50:00Z")
        self.assertEqual(es.producer_state("fresh", [run], self.DATA), "failing")

    def test_cancelled_and_disabled_are_never_failing(self):
        self.assertEqual(es.producer_state("fresh", [self.wf_run("cancelled")], self.DATA), "fresh")
        off = self.wf_run("failure", state="disabled_manually")
        self.assertEqual(es.producer_state("fresh", [off], self.DATA), "fresh")

    def test_idle_is_never_red(self):
        p = {
            "state": "idle",
            "data_state": "idle",
            "updated_at": "2026-06-01T00:00:00Z",
            "age_days": 120.0,
            "through_season": 2026,
        }
        for b in es.producer_badges(p).values():
            self.assertNotEqual(b["color"], "red")
        self.assertEqual(es.producer_badges(p)["status"]["message"], "idle (off-season)")
        self.assertEqual(es.producer_badges(p)["status"]["color"], "blue")


class Badges(Base):
    SHAPE = {"schemaVersion", "label", "message", "color", "namedLogo"}

    def check(self, b, label, message, color):
        self.assertEqual(set(b), self.SHAPE)
        self.assertEqual(b["schemaVersion"], 1)
        self.assertEqual(b["namedLogo"], "github")
        self.assertEqual((b["label"], b["message"], b["color"]), (label, message, color))

    def test_workflow_badges(self):
        ok = wf("Update WBB Data", "daily_wbb.yml", "success", "2026-09-09T07:00:00Z")
        self.check(es.wf_badge(ok), "Update WBB Data", "passing · 2026-09-09", "brightgreen")
        bad = wf("R-CMD-check", "R-CMD-check.yaml", "failure", "2026-09-20T00:00:00Z")
        self.check(es.wf_badge(bad), "R-CMD-check", "failing · 2026-09-20", "red")
        cx = wf("x", "x.yml", "cancelled", "2026-09-21T00:00:00Z")
        self.check(es.wf_badge(cx), "x", "cancelled · 2026-09-21", "yellow")
        self.check(es.wf_badge(wf("pkgdown", "pkgdown.yaml")), "pkgdown", "no runs", "lightgrey")

    def test_disabled_workflow_is_never_passing(self):
        off = wf("NBA Stats", "daily_nba_stats.yml", "success", "2026-07-12T07:00:00Z", state="disabled_manually")
        self.check(es.wf_badge(off), "NBA Stats", "disabled · 2026-07-12", "lightgrey")
        never = wf("x", "x.yml", state="disabled_inactivity")
        self.check(es.wf_badge(never), "x", "disabled", "lightgrey")

    def test_producer_badges(self):
        p = {
            "state": "stale",
            "data_state": "stale",
            "updated_at": "2026-09-01T10:00:00Z",
            "age_days": 29.1,
            "through_season": 2026,
        }
        b = es.producer_badges(p)
        self.check(b["updated"], "data updated", "2026-09-01", "orange")
        self.check(b["through"], "through", "2026 season", "blue")
        self.check(b["status"], "pipeline", "stale 29d", "orange")
        p = {
            "state": "failing",
            "data_state": "fresh",
            "updated_at": "2026-09-29T10:00:00Z",
            "age_days": 1.0,
            "through_season": None,
        }
        b = es.producer_badges(p)
        self.check(b["updated"], "data updated", "2026-09-29", "brightgreen")
        self.check(b["through"], "through", "unknown", "lightgrey")
        self.check(b["status"], "pipeline", "failing", "red")
        p = {"state": "unknown", "data_state": "unknown", "updated_at": None, "age_days": None, "through_season": None}
        self.check(es.producer_badges(p)["status"], "pipeline", "unknown", "lightgrey")

    def test_write_json_is_utf8_lf_sorted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "b" / "x.json"
            es.write_json(p, {"b": "passing · 2026-09-09", "a": 1})
            raw = p.read_bytes()
        self.assertIn("·".encode("utf-8"), raw)
        self.assertNotIn(b"\r\n", raw)
        self.assertTrue(raw.endswith(b"}\n"))
        self.assertLess(raw.index(b'"a"'), raw.index(b'"b"'))

    def test_badge_files_cover_every_workflow_and_producer(self):
        snap = fake_snap()
        files = es.badge_files(snap, es.build_summary(snap, fake_cfg(), NOW))
        for key in (
            "hoopR/wf-R-CMD-check.json",
            "hoopR/wf-pkgdown.json",
            "wehoop-wnba-data/wf-daily_wnba.json",
            "wehoop-wnba-data/updated.json",
            "wehoop-wnba-data/through.json",
            "wehoop-wnba-data/status.json",
            "cfbfastR-cfb-data/status.json",
        ):
            self.assertIn(key, files)
        self.assertEqual(files["hoopR/wf-pkgdown.json"]["message"], "no runs")

    def test_duplicate_workflow_stem_falls_back_to_file_name(self):
        snap = fake_snap()
        wfs = snap["repos"]["sportsdataverse/hoopR"]["workflows"]
        wfs["dup"] = {**wfs["pkgdown"], "name": "dup", "file": ".github/workflows/pkgdown.yml"}
        summary = es.build_summary(snap, fake_cfg(), NOW)
        files = es.badge_files(snap, summary)
        self.assertEqual(files["hoopR/wf-pkgdown.json"]["label"], "pkgdown")  # .yaml sorts first
        self.assertEqual(files["hoopR/wf-pkgdown.yml.json"]["label"], "dup")
        pkg = summary["packages"][0]["workflows"]
        self.assertIn("hoopR/wf-pkgdown.yml.json", [w["badge"] for w in pkg])
        self.assertTrue(any("share the stem" in w for w in summary["warnings"]))

    def test_repo_name_collision_uses_owner_prefix(self):
        dirs = es.badge_dirs(["sportsdataverse/baseballr", "BillPetti/baseballr", "sportsdataverse/hoopR"])
        self.assertEqual(
            dirs,
            {
                "sportsdataverse/baseballr": "baseballr",
                "BillPetti/baseballr": "BillPetti__baseballr",
                "sportsdataverse/hoopR": "hoopR",
            },
        )


class GhErrors(Base):
    def test_classification(self):
        absent = [
            "gh: Not Found (HTTP 404)",
            "gh: Gone (HTTP 410)",
            "gh: Resource not accessible by integration (HTTP 403)",
        ]
        errors = [
            "gh: API rate limit exceeded for installation ID 1. (HTTP 403)",
            "gh: You have exceeded a secondary rate limit. (HTTP 403)",
            "gh: Server Error (HTTP 502)",
            "gh: Too Many Requests (HTTP 429)",
            "error connecting to api.github.com: dial tcp: i/o timeout",
        ]
        for s in absent:
            self.assertEqual(es.classify_gh_failure(s), "absent", s)
        for s in errors:
            self.assertEqual(es.classify_gh_failure(s), "error", s)

    def _fake_run(self, stderr):
        return lambda *a, **k: subprocess.CompletedProcess(a, 1, stdout="", stderr=stderr)

    def test_rate_limit_raises_and_404_is_absent(self):
        with mock.patch.object(es.subprocess, "run", self._fake_run("gh: API rate limit exceeded (HTTP 403)")):
            with self.assertRaises(es.GhError):
                es._gh_once("repos/x/y")
        with mock.patch.object(es.subprocess, "run", self._fake_run("gh: Not Found (HTTP 404)")):
            self.assertIsNone(es._gh_once("repos/x/y"))

    def test_failed_later_page_raises(self):
        pages = {1: [{}] * 100, 2: None}
        with mock.patch.object(es, "_gh_once", lambda p: pages[int(p.rsplit("=", 1)[1])]):
            with self.assertRaises(es.GhError):
                es.gh("repos/x/y/issues?per_page=100", paginate=True)

    def test_first_page_404_is_absent_and_cap_warns(self):
        with mock.patch.object(es, "_gh_once", lambda p: None):
            self.assertIsNone(es.gh("repos/x/y/releases?per_page=100", paginate=True))
        with mock.patch.object(es, "_gh_once", lambda p: [{}] * 100):
            got = es.gh("repos/x/y/releases?per_page=100", paginate=True, pages_cap=2)
        self.assertEqual(len(got), 200)
        self.assertTrue(any("pagination cap" in w for w in es.WARNINGS))


class Snapshots(Base):
    def test_snapshot_workflows_filters_and_backfills(self):
        runs = {
            "workflow_runs": [
                api_run(9, "a.yml", None, "2026-09-30T01:00:00Z", status="in_progress"),
                api_run(8, "a.yml", "failure", "2026-09-29T00:00:00Z", event="pull_request", head="fork/r"),
                # a pull_request run is never a default-branch run, even from this repo
                api_run(10, "a.yml", "failure", "2026-09-29T06:00:00Z", event="pull_request_target"),
                api_run(7, "a.yml", "failure", "2026-09-28T00:00:00Z", event="push", head="someone/r"),
                {**api_run(6, "x", "success", "2026-09-27T00:00:00Z"), "path": "dynamic/dependabot/dependabot-updates"},
                api_run(5, "a.yml", "success", "2026-09-20T00:00:00Z", "2026-09-20T00:20:00Z"),
            ]
        }
        workflows = {
            "workflows": [
                {"id": 1, "path": ".github/workflows/a.yml", "name": "A", "state": "active"},
                {"id": 2, "path": ".github/workflows/b.yml", "name": "B", "state": "active"},
                {"id": 3, "path": ".github/workflows/c.yml", "name": "C", "state": "disabled_manually"},
                {"id": 4, "path": ".github/workflows/orphan_scripts.yml", "name": "orphan", "state": "active"},
                {"id": 5, "path": "dynamic/copilot-swe-agent/copilot", "name": "Copilot", "state": "active"},
                {"id": 6, "path": ".github/workflows/gone.yml", "name": "Gone", "state": "deleted"},
            ]
        }
        b_runs = {
            "workflow_runs": [
                api_run(21, "b.yml", None, "2026-09-30T00:00:00Z", status="queued"),
                api_run(20, "b.yml", "success", "2026-09-29T00:00:00Z", event="pull_request_target", head="fork/r"),
                api_run(19, "b.yml", "failure", "2026-08-01T00:00:00Z"),
            ]
        }
        c_runs = {"workflow_runs": [api_run(30, "c.yml", "success", "2026-07-12T07:00:00Z")]}
        fake = FakeGh(
            [
                (f"repos/{REPO}/actions/workflows/2/runs", b_runs),
                (f"repos/{REPO}/actions/workflows/3/runs", c_runs),
                (f"repos/{REPO}/actions/workflows?", workflows),
                (f"repos/{REPO}/actions/runs?", runs),
            ]
        )
        with mock.patch.object(es, "gh", fake):
            got = {w["file"].rsplit("/", 1)[-1]: w for w in es.snapshot_workflows(REPO, "main", True).values()}
        self.assertEqual(set(got), {"a.yml", "b.yml", "c.yml", "orphan_scripts.yml"})
        self.assertEqual((got["a.yml"]["conclusion"], got["a.yml"]["run_id"]), ("success", 5))
        self.assertEqual(got["a.yml"]["completed_at"], "2026-09-20T00:20:00Z")
        self.assertEqual((got["b.yml"]["conclusion"], got["b.yml"]["run_id"]), ("failure", 19))
        self.assertEqual(es.wf_badge(got["c.yml"])["message"], "disabled · 2026-07-12")
        self.assertIsNone(got["orphan_scripts.yml"]["conclusion"])
        self.assertFalse(any("workflows/4/runs" in c for c in fake.calls))

    def test_list_repos_drops_private_extra_repos(self):
        fake = FakeGh(
            [
                (
                    "orgs/sportsdataverse/repos",
                    [
                        {"full_name": "sportsdataverse/a", "private": False},
                        {"full_name": "sportsdataverse/secret", "private": True},
                        {"full_name": "sportsdataverse/old", "private": False, "archived": True},
                    ],
                ),
                ("repos/saiemgilani/game-on-paper-app", {"full_name": "saiemgilani/game-on-paper-app"}),
                ("repos/BillPetti/baseballr", {"full_name": "BillPetti/baseballr", "private": True}),
            ]
        )
        with mock.patch.object(es, "gh", fake):
            names = [r["full_name"] for r in es.list_repos()]
        self.assertEqual(names, ["sportsdataverse/a", "saiemgilani/game-on-paper-app"])

    def test_snapshot_repo_skips_drafts(self):
        asset = lambda n: {"name": n, "updated_at": "2026-09-01T00:00:00Z", "size": 1}  # noqa: E731
        releases = [
            {"tag_name": "v9-draft", "draft": True, "published_at": None, "assets": [asset("pbp_2027.parquet")]},
            {
                "tag_name": "v1",
                "draft": False,
                "published_at": "2026-09-01T00:00:00Z",
                "assets": [asset("pbp_2026.parquet")],
            },
        ]
        fake = FakeGh(
            [
                (f"repos/{REPO}/releases", releases),
                (f"repos/{REPO}/actions/runs?", {"workflow_runs": []}),
                (f"repos/{REPO}/actions/workflows?", {"workflows": []}),
                (f"repos/{REPO}/pulls", []),
                (f"repos/{REPO}/issues", []),
            ]
        )
        with mock.patch.object(es, "gh", fake):
            snap = es.snapshot_repo({"full_name": REPO, "default_branch": "main"})
        self.assertEqual(list(snap["releases"]), ["v1"])
        self.assertEqual(snap["latest_release_tag"], "v1")


class KeepLatestRuns(Base):
    PREV = {
        "Update WBB Data": {
            **wf("Update WBB Data", "daily_wbb.yml", "success", "2026-09-09T05:21:38Z"),
            "url": f"https://github.com/{REPO}/actions/runs/555",
        }
    }

    def test_stale_read_is_pinned_when_the_run_still_exists(self):
        seen = []

        def fetch(rid):
            seen.append(rid)
            return api_run(rid, "daily_wbb.yml", "success", "2026-09-09T05:21:38Z", "2026-09-09T06:00:00Z")

        stale = {"Update WBB Data": wf("Update WBB Data", "daily_wbb.yml", "failure", "2026-07-12T20:34:32Z")}
        got = es.keep_latest_runs(REPO, stale, self.PREV, fetch)["Update WBB Data"]
        self.assertEqual(
            (got["conclusion"], got["created_at"], got["run_id"]), ("success", "2026-09-09T05:21:38Z", 555)
        )
        self.assertEqual(seen, [555])  # run id recovered from the old snapshot's url

    def test_a_run_that_no_longer_exists_is_not_pinned(self):
        stale = {"Update WBB Data": wf("Update WBB Data", "daily_wbb.yml", "failure", "2026-07-12T20:34:32Z")}
        got = es.keep_latest_runs(REPO, stale, self.PREV, lambda rid: None)["Update WBB Data"]
        self.assertEqual(got["conclusion"], "failure")

    def test_newer_run_and_new_workflow_pass_through_without_calls(self):
        prev = {"x": wf("x", "x.yml", "success", "2026-09-01T00:00:00Z")}
        new = {
            "x": wf("x", "x.yml", "failure", "2026-09-02T00:00:00Z"),
            "y": wf("y", "y.yml", "success", "2026-09-03T00:00:00Z"),
        }
        calls = []
        got = es.keep_latest_runs(REPO, new, prev, lambda rid: calls.append(rid))
        self.assertEqual(got, new)
        self.assertEqual(calls, [])


class Collect(Base):
    PREV = {
        "sportsdataverse/b": {
            **repo("sportsdataverse/b", [wf("CI", "ci.yml", "success", "2026-09-01T00:00:00Z")]),
        }
    }

    def snapshot(self, r, backfill, prev):
        if r["full_name"] == "sportsdataverse/a":
            return repo("sportsdataverse/a", [])
        raise es.GhError(f"gh api repos/{r['full_name']}: API rate limit exceeded (HTTP 403)")

    def test_failed_repo_is_carried_forward_or_left_out(self):
        repos = [{"full_name": f"sportsdataverse/{n}"} for n in "abc"]
        out, failed = es.collect(repos, set(), self.PREV, self.snapshot)
        self.assertEqual(failed, ["sportsdataverse/b", "sportsdataverse/c"])
        self.assertNotIn("carried_forward", out["sportsdataverse/a"])
        b = out["sportsdataverse/b"]
        self.assertTrue(b["carried_forward"])
        self.assertIn("GhError", b["carried_forward_reason"])
        self.assertEqual(b["workflows"]["CI"]["conclusion"], "success")  # badges rebuilt from last good data
        self.assertNotIn("sportsdataverse/c", out)
        self.assertEqual(len([w for w in es.WARNINGS if "carried forward" in w or "no previous" in w]), 2)

    def test_abort_on_hub_or_more_than_a_tenth(self):
        self.assertIsNotNone(es.should_abort([es.HUB], 80))
        self.assertIsNone(es.should_abort([f"o/r{i}" for i in range(8)], 80))  # exactly 10%
        self.assertIsNotNone(es.should_abort([f"o/r{i}" for i in range(9)], 80))
        self.assertIsNone(es.should_abort([], 80))


class Main(Base):
    def test_hub_failure_exits_nonzero_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "producers.json").write_text(PRODUCERS.read_text(encoding="utf-8"), encoding="utf-8")
            (out / "ecosystem.json").write_text('{"repos": {}}', encoding="utf-8")
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            with (
                mock.patch.object(es, "OUT", out),
                mock.patch.object(es, "list_repos", lambda: [{"full_name": es.HUB}]),
                mock.patch.object(es, "collect", lambda *a, **k: ({}, [es.HUB])),
            ):
                self.assertEqual(es.main(), 2)
            self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)


class Summary(Base):
    def setUp(self):
        super().setUp()
        self.snap = fake_snap()
        self.summary = es.build_summary(self.snap, fake_cfg(), NOW)

    def test_release_tags_stalest_first_empty_last(self):
        rt = self.summary["release_tags"]
        self.assertEqual(
            [t["tag"] for t in rt],
            [
                "phf_pbp",
                "espn_nba_pbp",
                "mlb_pbp",
                "espn_wnba_schedules",
                "espn_wnba_pbp",
                "mlb_models",
                "espn_wnba_injuries",
                "zzz_new",
            ],
        )
        self.assertEqual(set(rt[0]), {"tag", "producer", "assets", "newest_asset_at", "max_season"})
        self.assertIsNone(rt[0]["producer"])
        self.assertEqual(rt[4]["producer"], "sportsdataverse/wehoop-wnba-data")
        self.assertEqual(rt[3]["max_season"], 2027)  # per-tag max_season stays raw
        self.assertEqual(self.summary["unmapped_tags"], ["phf_pbp", "espn_nba_pbp", "zzz_new"])

    def test_through_tags_limit_through_season(self):
        self.assertEqual(find(self.summary, "wehoop-wnba-data")["through_season"], 2026)  # not the 2027 schedule
        cfg = fake_cfg()
        del cfg["producers"][0]["through_tags"]
        s = es.build_summary(fake_snap(), cfg, NOW)
        self.assertEqual(find(s, "wehoop-wnba-data")["through_season"], 2027)  # default: every counted tag

    def test_freshness_follows_play_level_tags(self):
        mlb = find(self.summary, "baseballr-data")
        self.assertEqual(mlb["updated_at"], "2026-09-10T00:00:00Z")
        self.assertEqual(mlb["any_updated_at"], "2026-09-29T00:00:00Z")
        self.assertEqual(mlb["state"], "stale")  # models landing yesterday do not hide 20-day-old pbp

    def test_tags_is_a_count_with_names_beside_it(self):
        wnba = find(self.summary, "wehoop-wnba-data")
        self.assertEqual(wnba["tags"], 2)
        self.assertEqual(wnba["tag_names"], ["espn_wnba_pbp", "espn_wnba_schedules"])

    def test_freshness_false_tags_do_not_count(self):
        cfb = find(self.summary, "cfbfastR-cfb-data")
        self.assertEqual(cfb["tag_names"], ["espn_wnba_injuries"])
        self.assertIsNone(cfb["updated_at"])
        self.assertEqual(cfb["any_updated_at"], "2026-09-30T00:00:00Z")
        self.assertEqual(cfb["state"], "unknown")

    def test_non_update_workflow_failure_does_not_make_the_producer_failing(self):
        wnba = find(self.summary, "wehoop-wnba-data")
        self.assertEqual(wnba["state"], "fresh")
        self.assertEqual([w["file"] for w in wnba["workflows"]], [".github/workflows/daily_wnba.yml"])
        self.assertIn(".github/workflows/tests.yml", [r["file"] for r in self.summary["red_workflows"]])

    def test_workflow_entries_keep_the_page_contract(self):
        w = find(self.summary, "wehoop-wnba-data")["workflows"][0]
        for k in ("name", "file", "conclusion", "created_at", "event", "url", "completed_at", "state", "badge"):
            self.assertIn(k, w)
        self.assertEqual(w["badge"], "wehoop-wnba-data/wf-daily_wnba.json")

    def test_config_warnings_are_surfaced(self):
        cfg = fake_cfg()
        cfg["producers"][0]["through_tags"] = ["espn_wnba_pbpp"]
        cfg["producers"][0]["update_workflows"] = ["daily_wnbaa.yml"]
        es.WARNINGS.clear()
        s = es.build_summary(fake_snap(), cfg, NOW)
        self.assertTrue(any("espn_wnba_pbpp" in w for w in s["warnings"]))
        self.assertTrue(any("daily_wnbaa.yml" in w for w in s["warnings"]))
        self.assertIn("espn_wnba_pbpp", es.render_md(fake_snap(), s).split("## Warnings")[1])


class Markdown(Base):
    def setUp(self):
        super().setUp()
        snap = fake_snap()
        self.md = es.render_md(snap, es.build_summary(snap, fake_cfg(), NOW))

    def test_empty_tags_print_empty_and_sort_last(self):
        rows = [l for l in self.md.splitlines() if l.startswith("| ") and "|---" not in l]
        tag_rows = rows[1:9]  # header, then the eight release tags
        self.assertTrue(tag_rows[-1].startswith("| zzz_new |"))
        self.assertIn("| empty |", tag_rows[-1])

    def test_doctoc_markers_exactly_once(self):
        self.assertEqual(self.md.count(es.TOC_START), 1)
        self.assertEqual(self.md.count(es.TOC_END), 1)
        self.assertLess(self.md.index(es.TOC_START), self.md.index("\n## "))

    def test_section_order(self):
        heads = [l for l in self.md.splitlines() if l.startswith("## ")]
        self.assertEqual(heads[0], es.RELEASE_TAGS_HEADING)
        self.assertEqual(heads[1], "## Producers")
        self.assertEqual(heads[-2:], ["## Unmapped release tags", "## Warnings"])

    def test_headings_hold_no_counts_or_dates(self):
        for l in self.md.splitlines():
            if l.startswith("#"):
                self.assertIsNone(re.search(r"\d", l), l)


class CranDownloads(Base):
    def test_sums_valid_r_package_names_only(self):
        seen = []

        def fetch(url):
            seen.append(url)
            return [{"package": "hoopR", "downloads": 1_200_000}, {"package": "wehoop", "downloads": 34_567}]

        b = es.cran_downloads_badge(
            ["sportsdataverse/hoopR", "sportsdataverse/wehoop", "sportsdataverse/sportsdataverse-py"], fetch
        )
        self.assertEqual(seen, [es.CRANLOGS + "hoopR,wehoop"])  # a hyphenated name 404s the whole query
        self.assertEqual((b["label"], b["message"], b["namedLogo"]), ("CRAN downloads", "1.2M", "r"))

    def test_failed_fetch_is_none_never_zero(self):
        def down(url):
            raise OSError("cranlogs down")

        self.assertIsNone(es.cran_downloads_badge(["sportsdataverse/hoopR"], down))
        # cranlogs answers a bad query with an error object, not a list
        self.assertIsNone(es.cran_downloads_badge(["sportsdataverse/hoopR"], lambda url: {"error": "Invalid query"}))
        self.assertTrue(any("cranlogs" in w for w in es.WARNINGS))

    def test_human_count(self):
        self.assertEqual([es.human_count(n) for n in (999, 287_487, 1_234_567)], ["999", "287k", "1.2M"])


if __name__ == "__main__":
    unittest.main()
