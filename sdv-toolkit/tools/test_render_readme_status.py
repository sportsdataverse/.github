"""Tests for render_readme_status. Run: python -m unittest discover -s tools -p 'test_*.py'

These cover the two things the renderer can state BACKWARDS rather than merely
omit -- a schedule and a trigger list. An omission is visible; a confident wrong
answer is not, and both of these shipped wrong once.
"""

import unittest

import render_readme_status as r


class DescribeCron(unittest.TestCase):
    def test_day_of_week_replaces_daily_rather_than_trailing_it(self):
        # `dow 6` fires on Saturdays. Rendering it "daily ... dow 6" asserts the
        # opposite of the truth on six days out of seven.
        self.assertEqual(r.describe_cron("0 14 * 9-11 6"), "Saturdays 14:00 UTC in Sep-Nov")
        self.assertEqual(r.describe_cron("0 22 * 9-11 1-5"), "weekdays 22:00 UTC in Sep-Nov")

    def test_unrestricted_day_of_week_is_still_daily(self):
        self.assertEqual(r.describe_cron("0 14 * 12 *"), "daily 14:00 UTC in Dec")

    def test_day_of_month_keeps_dow_as_a_qualifier(self):
        self.assertEqual(r.describe_cron("0 1 5 * 1-5"), "day 5 01:00 UTC, weekdays")

    def test_named_days_are_spelled_out(self):
        self.assertEqual(r.describe_cron("0 1 * * 0"), "Sundays 01:00 UTC")
        self.assertEqual(r.describe_cron("0 1 * * 2,4"), "Tue/Thu 01:00 UTC")

    def test_unparseable_fields_fall_back_to_the_raw_expression(self):
        self.assertEqual(r.describe_cron("0 1 * * mon-fri"), "dow mon-fri 01:00 UTC")
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

    def test_no_recognised_trigger_says_so(self):
        self.assertEqual(r._describe_triggers("on:\n  schedule:\n    - cron: '0 1 * * *'\n"), "on demand")

    def test_a_step_named_push_is_not_a_trigger(self):
        # Trigger keys sit under `on:` at one indent level; a deeper `push:` is a
        # step, and counting it would invent a trigger the workflow lacks.
        wf = "on:\n  workflow_dispatch:\njobs:\n  b:\n    steps:\n      - name: x\n        push: true\n"
        self.assertEqual(r._describe_triggers(wf), "on dispatch")


if __name__ == "__main__":
    unittest.main()
