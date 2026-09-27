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
    },
}

LITERAL_R = """
cfbd_a <- function(year = NULL, first = NULL) {
  base_url <- "https://api.example.com/a"
}
cfbd_dead <- function() {
  base_url <- "https://api.example.com/zzz"
}
"""

HELPER_R = """
cbbd_bc <- function(id, season = most_recent_mbb_season(), team = NULL) {
  data <- .cbbd_get(paste0("/b/", id, "/c"))
}
"""


class ApiCoverageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.spec = root / "spec.json"
        self.spec.write_text(json.dumps(SPEC), encoding="utf-8")
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

    def test_formals_balanced_parens(self):
        r = ac.scan_r_dir(self.r, "api.other.com", "cbbd")
        self.assertEqual(r["/b/{}/c"][0]["formals"], ["id", "season", "team"])

    def test_drift_alias_and_real(self):
        d = self._diff()
        rows = [x for x in d["drift"] if x["fn"] == "cfbd_a"]
        self.assertEqual(len(rows), 1)
        # firstName is covered by the R abbreviation `first`; classification is real drift
        self.assertEqual(rows[0]["missing_params"], ["classification"])

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
        self.assertEqual(
            s["counts"]["missing"], 2
        )  # /b/{id}/c and /d are unwrapped in the cfbd view
        self.assertIn(
            "## Spec endpoints with NO cfbd wrapper", out_md.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    unittest.main()
