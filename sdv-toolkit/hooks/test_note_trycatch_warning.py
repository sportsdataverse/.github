"""Tests for note_trycatch_warning. Run: python -m unittest discover -s hooks -p 'test_*.py'"""

import json
import pathlib
import subprocess
import sys
import unittest

HOOK = pathlib.Path(__file__).resolve().parent / "note_trycatch_warning.py"

UNWINDING = """
  tryCatch(
    expr = { x <- parse(resp) },
    error = function(e) .report_api_error(e),
    warning = function(w) .report_api_warning(w),
    finally = {}
  )
"""
CALLING = """
  withCallingHandlers(
    tryCatch(expr, error = function(e) NULL),
    warning = function(w) { report(w); invokeRestart("muffleWarning") }
  )
"""


def run_hook(tool_input, raw=None):
    payload = raw if raw is not None else json.dumps({"tool_input": tool_input})
    return subprocess.run(
        [sys.executable, str(HOOK)], input=payload, capture_output=True, text=True
    )


class NoteTryCatchWarningTest(unittest.TestCase):
    def assertNoted(self, r):
        self.assertEqual(r.returncode, 0)
        self.assertIn("UNWINDS", r.stderr)

    def assertQuiet(self, r):
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")

    def test_write_of_unwinding_handler_in_R_dir_is_noted(self):
        self.assertNoted(
            run_hook({"file_path": "/repo/R/espn_mlb_data.R", "content": UNWINDING})
        )

    def test_edit_new_string_windows_path_is_noted(self):
        self.assertNoted(
            run_hook({"file_path": "C:\\repo\\R\\fox_mlb.R", "new_string": UNWINDING})
        )

    def test_multiedit_is_noted(self):
        self.assertNoted(
            run_hook(
                {
                    "file_path": "/repo/R/x.R",
                    "edits": [{"new_string": "a"}, {"new_string": UNWINDING}],
                }
            )
        )

    def test_calling_handler_is_quiet(self):
        self.assertQuiet(run_hook({"file_path": "/repo/R/x.R", "content": CALLING}))

    def test_error_only_trycatch_is_quiet(self):
        self.assertQuiet(
            run_hook(
                {
                    "file_path": "/repo/R/x.R",
                    "content": "tryCatch(f(), error = function(e) NULL)",
                }
            )
        )

    def test_file_outside_R_dir_is_quiet(self):
        self.assertQuiet(
            run_hook(
                {"file_path": "/repo/tests/testthat/test-x.R", "content": UNWINDING}
            )
        )
        self.assertQuiet(
            run_hook({"file_path": "/repo/data-raw/build.R", "content": UNWINDING})
        )

    def test_bad_json_fails_open(self):
        self.assertQuiet(run_hook(None, raw="not json"))


if __name__ == "__main__":
    unittest.main()
