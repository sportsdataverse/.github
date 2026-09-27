"""Tests for skills/sdv-api-sync/scripts/api_coverage.py.
Run: python -m unittest discover -s tools -p 'test_*.py'
Each test pins one input class the spec implies but a naive implementation
gets wrong: middle-segment paste0 params, parenthesised defaults in formals,
a yanked upstream release, a spec with no paths, a marker-less issue body.
"""

import json
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "skills", "sdv-api-sync", "scripts"),
)
import api_coverage as ac  # noqa: E402

SPEC = {
    "info": {"version": "9.9.9"},
    "paths": {
        "/a": {
            "get": {
                "operationId": "GetA",
                "tags": ["a"],
                "parameters": [
                    {"name": "year", "in": "query", "schema": {"type": "integer"}},
                    {"name": "firstName", "in": "query", "schema": {"type": "string"}},
                    {
                        "name": "classification",
                        "in": "query",
                        "schema": {"type": "string"},
                    },
                ],
            }
        },
        "/b/{id}/c": {
            "get": {
                "operationId": "GetBC",
                "tags": ["b"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
            }
        },
        "/d": {"get": {"operationId": "GetD", "tags": ["d"], "parameters": []}},
        "/teams/{teamId}/roster": {
            "get": {
                "operationId": "GetRoster",
                "tags": ["teams"],
                "parameters": [
                    {
                        "name": "teamId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
            }
        },
    },
}

# Extra spec paths for the query-key and bare-host idioms (merged into SPEC in setUp).
EXTRA_PATHS = {
    "/div": {
        "get": {
            "operationId": "GetDiv",
            "tags": ["x"],
            "parameters": [
                {"name": "classification", "in": "query", "schema": {"type": "string"}}
            ],
        }
    },
    "/wrong": {
        "get": {
            "operationId": "GetWrong",
            "tags": ["x"],
            "parameters": [
                {"name": "classification", "in": "query", "schema": {"type": "string"}}
            ],
        }
    },
    "/fg/ep": {"get": {"operationId": "GetFgEp", "tags": ["x"], "parameters": []}},
    "/commented": {
        "get": {
            "operationId": "GetCommented",
            "tags": ["x"],
            "parameters": [
                {"name": "year", "in": "query", "schema": {"type": "integer"}},
                {"name": "classification", "in": "query", "schema": {"type": "string"}},
            ],
        }
    },
}

LITERAL_R = """
cfbd_a <- function(year = NULL, first = NULL) {
  base_url <- "https://api.example.com/a"
  query_params <- list(
    "year" = year,
    "firstName" = first
  )
}
cfbd_div <- function(year = NULL, division = NULL) {
  base_url <- "https://api.example.com/div"
  query_params <- list("classification" = division)
}
cfbd_wrong <- function(classification = NULL) {
  base_url <- "https://api.example.com/wrong"
  query_params <- list("division" = classification)
}
cfbd_fg <- function() {
  base_url <- "https://api.example.com"
  endpoint_path <- "fg/ep"
  full_url <- paste0(base_url, "/", endpoint_path)
}
cfbd_dead <- function() {
  base_url <- "https://api.example.com/zzz"
}
cfbd_commented <- function(year = NULL, division = NULL) {
  base_url <- "https://api.example.com/commented?"
  query_params <- list(
    "year" = year,
    # CFBD renamed this to `classification`; sending `division=` isn't honoured (measured:
    # division=fcs returned all games). Keep the formal, send the new key.
    "classification" = division
  )
}
"""

HELPER_R = """
cbbd_bc <- function(id, season = most_recent_mbb_season(), team = NULL) {
  data <- .cbbd_get(paste0("/b/", id, "/c"))
}
cbbd_nested <- function(team) {
  data <- .cbbd_get(paste0("/teams/", toupper(trimws(team)), "/roster"), query = list(x = 1))
}
"""


class ApiCoverageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.spec = root / "spec.json"
        self.spec.write_text(
            json.dumps({**SPEC, "paths": {**SPEC["paths"], **EXTRA_PATHS}}),
            encoding="utf-8",
        )
        self.r = root / "R"
        self.r.mkdir()
        (self.r / "lit.R").write_text(LITERAL_R, encoding="utf-8")
        (self.r / "helper.R").write_text(HELPER_R, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _diff(self):
        _, eps = ac.load_spec(self.spec)
        r_lit = ac.scan_r_dir(self.r, "api.example.com", "cfbd")
        r_help = ac.scan_r_dir(self.r, "api.other.com", "cbbd")
        merged = {**r_lit, **r_help}
        return ac.diff(eps, merged)

    def test_missing_and_dead(self):
        d = self._diff()
        self.assertEqual([m["path"] for m in d["missing"]], ["/d"])
        self.assertEqual([x["path"] for x in d["dead"]], ["/zzz"])

    def test_paste0_middle_segment_param(self):
        r = ac.scan_r_dir(self.r, "api.other.com", "cbbd")
        self.assertIn("/b/{}/c", r)
        self.assertEqual(r["/b/{}/c"][0]["fn"], "cbbd_bc")

    def test_paste0_nested_call_args(self):
        # paste0("/teams/", toupper(trimws(team)), "/roster") must not stop at the first ')'
        r = ac.scan_r_dir(self.r, "api.other.com", "cbbd")
        self.assertIn("/teams/{}/roster", r)
        self.assertNotIn("/teams/{}", r)
        self.assertEqual(r["/teams/{}/roster"][0]["fn"], "cbbd_nested")

    def test_formals_balanced_parens(self):
        r = ac.scan_r_dir(self.r, "api.other.com", "cbbd")
        self.assertEqual(r["/b/{}/c"][0]["formals"], ["id", "season", "team"])

    def test_drift_uses_query_keys_not_formals(self):
        # Drift is judged on the camelCase keys the function SENDS, not on its formal names:
        # cfbd_a sends "firstName" (formal `first`) and cfbd_div sends "classification"
        # (formal `division`) -> no drift; cfbd_wrong sends "division" for a spec param
        # named classification -> real drift.
        d = self._diff()
        by_fn = {x["fn"]: x["missing_params"] for x in d["drift"]}
        # firstName is sent (as a key), so only classification -- which /a declares and
        # cfbd_a never sends -- is reported for it.
        self.assertEqual(by_fn.get("cfbd_a"), ["classification"])
        self.assertNotIn("cfbd_div", by_fn)
        self.assertEqual(by_fn.get("cfbd_wrong"), ["classification"])

    def test_bare_host_endpoint_path(self):
        # cfbfastR's cfbd_metrics_fg_ep idiom: base_url is the bare host and the path
        # lives in a separate `endpoint_path <- "..."` assignment.
        r = ac.scan_r_dir(self.r, "api.example.com", "cfbd")
        self.assertIn("/fg/ep", r)
        self.assertEqual(r["/fg/ep"][0]["fn"], "cfbd_fg")

    def test_query_keys_skip_comments(self):
        # A `#` comment inside the query list (with an apostrophe, backticks and parens)
        # must not swallow the keys that follow it: cfbd_commented sends both keys.
        r = ac.scan_r_dir(self.r, "api.example.com", "cfbd")
        self.assertEqual(r["/commented"][0]["query_keys"], ["year", "classification"])
        d = self._diff()
        self.assertNotIn("cfbd_commented", {x["fn"] for x in d["drift"]})

    def test_releases_between_yanked(self):
        tags = ["v5.31.1", "v5.31.0", "v5.30.1"]
        self.assertEqual(ac.releases_between(tags, "5.31.1", "5.31.0"), [])
        self.assertEqual(
            ac.releases_between(tags, "5.30.1", "5.31.1"), ["v5.31.1", "v5.31.0"]
        )
        self.assertEqual(ac.releases_between(tags, None, "5.31.1"), ["v5.31.1"])

    def test_spec_without_paths_exits_2(self):
        bad = pathlib.Path(self.tmp.name) / "bad.json"
        bad.write_text(
            json.dumps({"info": {"version": "1"}, "paths": {}}), encoding="utf-8"
        )
        with self.assertRaises(SystemExit) as cm:
            ac.load_spec(bad)
        self.assertEqual(cm.exception.code, 2)

    def test_parse_marker_absent(self):
        self.assertIsNone(ac.parse_marker(""))
        self.assertIsNone(ac.parse_marker("no marker here"))
        self.assertEqual(
            ac.parse_marker("x\n<!-- api-sync: version=5.31.1 -->\ny"), "5.31.1"
        )

    def test_cli_writes_report_and_summary(self):
        out_md = pathlib.Path(self.tmp.name) / "report.md"
        out_js = pathlib.Path(self.tmp.name) / "summary.json"
        rc = ac.main(
            [
                str(self.spec),
                str(self.r),
                str(out_md),
                str(out_js),
                "--host",
                "api.example.com",
                "--prefix",
                "cfbd",
            ]
        )
        self.assertEqual(rc, 0)
        s = json.loads(out_js.read_text(encoding="utf-8"))
        # /b/{id}/c, /d and /teams/{teamId}/roster are unwrapped in the cfbd (literal-URL) view
        self.assertEqual(s["counts"]["missing"], 3)
        self.assertIn(
            "## Spec endpoints with NO cfbd wrapper", out_md.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    unittest.main()
