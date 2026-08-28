"""Tests for render_readme_status. Run: python -m unittest discover -s tools -p 'test_*.py'

These cover the two fields the renderer can state BACKWARDS rather than merely
omit -- a schedule and a trigger list. An omission is visible; a confident wrong
answer is not, and both of these shipped wrong once.
"""

import unittest

import render_readme_status as r


class DescribeCron(unittest.TestCase):
    def test_day_of_week_replaces_daily_rather_than_trailing_it(self):
        # `dow 6` fires on Saturdays. Rendering it "daily ... dow 6" asserts the
        # opposite of the truth on six days out of seven.
        self.assertEqual(
            r.describe_cron("0 14 * 9-11 6"), "Saturdays 14:00 UTC in Sep-Nov"
        )
        self.assertEqual(
            r.describe_cron("0 22 * 9-11 1-5"), "weekdays 22:00 UTC in Sep-Nov"
        )

    def test_unrestricted_day_of_week_is_still_daily(self):
        self.assertEqual(r.describe_cron("0 14 * 12 *"), "daily 14:00 UTC in Dec")

    def test_restricted_day_of_month_and_week_are_ORed_not_ANDed(self):
        # POSIX cron ORs the two fields: this fires on the 5th AND on every
        # weekday, not only on a 5th that happens to fall on a weekday.
        self.assertEqual(r.describe_cron("0 1 5 * 1-5"), "day 5 or weekdays 01:00 UTC")

    def test_named_days_are_spelled_out(self):
        self.assertEqual(r.describe_cron("0 1 * * 0"), "Sundays 01:00 UTC")
        self.assertEqual(r.describe_cron("0 1 * * 2,4"), "Tue/Thu 01:00 UTC")

    def test_sunday_folds_so_seven_and_zero_agree(self):
        self.assertEqual(r.describe_cron("0 1 * * 6,0"), "weekends 01:00 UTC")
        self.assertEqual(r.describe_cron("0 1 * * 6,7"), "weekends 01:00 UTC")

    def test_sunday_to_monday_is_not_a_weekend(self):
        # `0-1` is Sunday THROUGH Monday. Calling it "weekends" hides a Monday run.
        self.assertEqual(r.describe_cron("0 1 * * 0-1"), "Sun/Mon 01:00 UTC")

    def test_day_names_and_step_values_parse(self):
        self.assertEqual(r.describe_cron("0 1 * * mon-fri"), "weekdays 01:00 UTC")
        self.assertEqual(r.describe_cron("0 1 * * 1-5/2"), "Mon/Wed/Fri 01:00 UTC")

    def test_out_of_range_day_falls_back_instead_of_raising(self):
        # `8` is not a day. Filtering it while still indexing the unfiltered
        # first value raised KeyError rather than falling back.
        self.assertEqual(r.describe_cron("0 1 * * 8,6"), "dow 8,6 01:00 UTC")

    def test_unparseable_fields_fall_back_to_the_raw_expression(self):
        self.assertEqual(r.describe_cron("0 1 * * frobday"), "dow frobday 01:00 UTC")
        self.assertEqual(r.describe_cron("nonsense"), "`nonsense`")


class DescribeTriggers(unittest.TestCase):
    def test_only_declared_triggers_are_named(self):
        # The old hardcoded "on push / PR / dispatch" documented a PR trigger on
        # push-only workflows, sending anyone debugging "why didn't this run on
        # my PR" in the wrong direction.
        wf = "on:\n  push:\n    paths: ['scripts/**']\n  workflow_dispatch:\n"
        self.assertEqual(r._describe_triggers(wf), "on push / dispatch")

    def test_all_three_when_all_three_are_declared(self):
        wf = "on:\n  push:\n  pull_request:\n  workflow_dispatch:\n"
        self.assertEqual(r._describe_triggers(wf), "on push / PR / dispatch")

    def test_scalar_and_list_forms(self):
        self.assertEqual(r._describe_triggers("on: push\n"), "on push")
        self.assertEqual(r._describe_triggers("on: [push, fork]\n"), "on push / fork")
        self.assertEqual(
            r._describe_triggers("on:\n  - push\n  - fork\n"), "on push / fork"
        )

    def test_quoted_on_key(self):
        # YAML 1.1 reads a bare `on` as the boolean true, so some repos quote it.
        self.assertEqual(
            r._describe_triggers('"on":\n    push:\n    pull_request:\n'),
            "on push / PR",
        )

    def test_a_job_named_push_is_not_a_trigger(self):
        # Matching trigger names anywhere in the file counted a job named `push`
        # as a push trigger; scoping to the `on` block is what prevents that.
        wf = "on:\n  workflow_dispatch:\njobs:\n  push:\n    steps: []\n"
        self.assertEqual(r._describe_triggers(wf), "on dispatch")

    def test_no_recognised_trigger_says_so(self):
        self.assertEqual(
            r._describe_triggers("jobs:\n  b:\n    steps: []\n"), "on demand"
        )


class Splice(unittest.TestCase):
    def test_a_half_marked_readme_is_refused_not_guessed(self):
        with self.assertRaises(r.MalformedMarkersError):
            r.splice(f"# t\n\n{r.BEGIN}\n", "block")

    def test_write_reports_malformed_markers_instead_of_a_traceback(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as d:
            readme = Path(d) / "README.md"
            readme.write_text(f"# t\n\n{r.BEGIN}\n", encoding="utf-8")
            argv = [
                "--repo",
                "o/n",
                "--readme",
                str(readme),
                "--write",
                "--keep-on-offline",
            ]
            self.assertNotEqual(r.main(argv), 0)


if __name__ == "__main__":
    unittest.main()
