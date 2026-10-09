"""Tests for skills/sdv-ship/scripts/ci_wait.py.

Run: python -m unittest discover -s tools -p 'test_*.py'

Fully offline: a fake `gh` runner serves REST fixtures by path and records
every POST, and a fake clock replaces time.time/time.sleep.
"""

import calendar
import contextlib
import io
import json
import pathlib
import sys
import unittest

sys.path.insert(
    0,
    str(
        pathlib.Path(__file__).resolve().parent.parent
        / "skills"
        / "sdv-ship"
        / "scripts"
    ),
)

import ci_wait as cw  # noqa: E402

SHA = "abc123"
T0_ISO = "2026-10-09T08:00:00Z"
T0 = calendar.timegm((2026, 10, 9, 8, 0, 0))
CR = "coderabbitai[bot]"
SOURCERY = "sourcery-ai[bot]"
COPILOT_BOT = "copilot-pull-request-reviewer[bot]"

# Real notice text (hoopR-mbb-data#25, sportsdataverse-py#736), trimmed.
CR_LIMITED = (
    "<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->\n\n"
    "> [!WARNING]\n> ## Review limit reached\n> \n"
    "> **Next included review available in 15 minutes.**"
)
SOURCERY_BUDGET = (
    "Sorry @saiemgilani, you've used your own review budget of 250,000 diff "
    "characters for the last 7 days."
)


def iso(epoch):
    import time

    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))


def pr(state="clean", sha=SHA, requested=()):
    return {
        "head": {"sha": sha},
        "mergeable": state != "dirty",
        "mergeable_state": state,
        "user": {"login": "saiemgilani"},
        "requested_reviewers": [{"login": r} for r in requested],
    }


def run_(name, conclusion="success", status="completed", id=1, suite=1):
    return {
        "id": id,
        "name": name,
        "status": status,
        "conclusion": conclusion if status == "completed" else None,
        "check_suite": {"id": suite},
    }


def checks(*runs):
    return {"total_count": len(runs), "check_runs": list(runs)}


def status(*pairs):
    return {
        "statuses": [{"context": c, "state": s, "description": ""} for c, s in pairs]
    }


def comment(login, body, at=T0_ISO):
    return {"user": {"login": login}, "body": body, "created_at": at, "updated_at": at}


def inline(id, login, body="Consider X", path="a.py", line=3, reply_to=None):
    return {
        "id": id,
        "in_reply_to_id": reply_to,
        "user": {"login": login},
        "path": path,
        "line": line,
        "original_line": line,
        "body": body,
        "created_at": T0_ISO,
    }


def review(login, at=T0_ISO, body="**Actionable comments posted: 1**", commit_id=None):
    r = {
        "user": {"login": login},
        "state": "COMMENTED",
        "submitted_at": at,
        "body": body,
    }
    if commit_id:
        r["commit_id"] = commit_id
    return r


def routes(
    repo,
    n=7,
    pr_=None,
    checks_=None,
    status_=None,
    comments=(),
    inline_=(),
    reviews=(),
    user="saiemgilani",
    reset=None,
):
    """Map each REST path to a fixture; a list value is served one item per call."""
    base = "repos/%s" % repo
    return {
        "%s/pulls/%d" % (base, n): pr_ if pr_ is not None else pr(),
        "%s/commits/%s/check-runs?per_page=100" % (base, SHA): checks_ or checks(),
        "%s/commits/%s/status?per_page=100" % (base, SHA): status_ or status(),
        "%s/issues/%d/comments?per_page=100" % (base, n): list(comments),
        "%s/pulls/%d/comments?per_page=100" % (base, n): list(inline_),
        "%s/pulls/%d/reviews?per_page=100" % (base, n): list(reviews),
        "%s/issues/%d/timeline?per_page=100" % (base, n): [],
        "user": {"login": user},
        "rate_limit": {"resources": {"core": {"reset": reset or 0}}},
    }


def add_head(table, repo, sha, checks_, status_=None):
    """Serve check-runs and status for a second head SHA (a push mid-wait)."""
    base = "repos/%s/commits/%s" % (repo, sha)
    table[base + "/check-runs?per_page=100"] = checks_
    table[base + "/status?per_page=100"] = status_ or status()
    return table


# REST POST requested_reviewers reply that really added Copilot.
COPILOT_ADDED = {"requested_reviewers": [{"login": "Copilot"}]}
# REST 200 that silently added nobody (the CodeRabbit finding on PR #50).
NOBODY_ADDED = (0, json.dumps({"requested_reviewers": []}), "")


TIMELINE = "repos/%s/issues/7/timeline?per_page=100"


def requested_event(at, who="Copilot"):
    return {"event": "review_requested", "created_at": at, "requested_reviewer": {"login": who}}


class Seq:
    """A fixture served differently on each call (last one sticks)."""

    def __init__(self, *items):
        self.items = list(items)

    def next(self):
        return self.items.pop(0) if len(self.items) > 1 else self.items[0]


class FakeGh:
    def __init__(self, table, post_ok=True):
        self.table = table
        self.post_ok = post_ok
        self.gets = []
        self.posts = []
        self.post_times = []
        self.clock = None

    def __call__(self, argv):
        if argv[0] == "pr" or "-X" in argv:
            self.posts.append(argv)
            self.post_times.append(self.clock.t if self.clock else None)
            # Override with table["POST"] (REST) / table["EDIT"] (gh pr edit).
            if argv[0] == "pr":
                ok, key = (0, "", ""), "EDIT"
                bad = (1, "", "GraphQL: Could not add reviewer")
            else:
                ok, key = (0, json.dumps(COPILOT_ADDED), ""), "POST"
                bad = (1, "", "HTTP 422")
            return self.table.get(key, ok if self.post_ok else bad)
        path = argv[1]
        self.gets.append(path)
        value = self.table[path]
        if isinstance(value, Seq):
            value = value.next()
        if isinstance(value, BaseException):
            raise value
        if isinstance(value, tuple):  # (returncode, stdout, stderr) raw reply
            return value
        return (0, json.dumps(value), "")


class Clock:
    def __init__(self, t):
        self.t = t
        self.sleeps = []

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


def go(repo, table, *args, start=T0, env=None, post_ok=True):
    fake = FakeGh(table, post_ok=post_ok)
    clock = Clock(start)
    fake.clock = clock
    out = io.StringIO()
    argv = [repo, "--pr", "7", "--interval", "60s", *args]
    gh = cw.Gh(fake, now=clock.now, sleep=clock.sleep)
    rc = cw.run(argv, gh=gh, now=clock.now, sleep=clock.sleep, env=env or {}, out=out)
    return rc, out.getvalue(), fake, clock


PY = "sportsdataverse/sportsdataverse-py"
DATA = "sportsdataverse/cfbfastR-cfb-data"
GREEN = checks(run_("ruff + mypy", id=1), run_("pytest", id=2))


class Durations(unittest.TestCase):
    def test_units(self):
        self.assertEqual(cw.duration("90s"), 90)
        self.assertEqual(cw.duration("15m"), 900)
        self.assertEqual(cw.duration("1h"), 3600)
        self.assertEqual(cw.duration("45"), 45)
        with self.assertRaises(Exception):
            cw.duration("soon")


class Verdicts(unittest.TestCase):
    def test_failed_matrix_job_named(self):
        table = routes(
            PY,
            checks_=checks(
                run_("test (3.10)", id=1),
                run_("test (3.11)", "failure", id=2),
                run_("test (3.12)", id=3),
                run_("lint", id=4),
            ),
        )
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 1)
        self.assertIn("failure\ttest (3.11)", out)
        self.assertIn("FAILED: test (3.11)", out)
        self.assertNotIn("FAILED: test (3.10)", out)
        self.assertTrue(out.rstrip().endswith("VERDICT: failed"))

    def test_rerun_supersedes_failure(self):
        table = routes(
            PY,
            checks_=checks(
                run_("pytest", "failure", id=1), run_("pytest", "success", id=2)
            ),
        )
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 0, out)

    def test_failed_commit_status(self):
        table = routes(PY, checks_=GREEN, status_=status(("ci/legacy", "error")))
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 1)
        self.assertIn("FAILED: ci/legacy", out)

    def test_failed_status_on_page_two_is_not_missed(self):
        # The combined-status endpoint pages `statuses` (30 by default).
        page1 = status(*[("ci/ctx-%03d" % i, "success") for i in range(100)])
        page1["total_count"] = 101
        table = routes(PY, checks_=GREEN, status_=page1)
        table["repos/%s/commits/%s/status?per_page=100&page=2" % (PY, SHA)] = status(
            ("ci/late", "failure")
        )
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 1, out)
        self.assertIn("FAILED: ci/late", out)

    def test_all_green_ready(self):
        table = routes(
            PY,
            checks_=GREEN,
            status_=status(("CodeRabbit", "success")),
            reviews=[review(CR)],
        )
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 0)
        self.assertIn("success\truff + mypy", out)
        self.assertIn("success\tCodeRabbit", out)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready"))

    def test_a_stale_check_run_is_a_failure_not_green(self):
        # Copilot on #50: a completed run with conclusion `stale` never succeeded.
        table = routes(PY, checks_=checks(run_("tests", conclusion="stale"), run_("lint", id=2)))
        rc, out, _, _ = go(PY, table, "--bots-grace", "0s")
        self.assertEqual(rc, 1)
        self.assertIn("tests", out)
        self.assertTrue(out.rstrip().endswith("VERDICT: failed"))

    def test_merged_pr_stops_at_once_even_with_a_stuck_bot(self):
        # PR 736 merged mid-review: CodeRabbit's status stayed pending and the wait ran to --timeout.
        merged = {**pr(), "state": "closed", "merged": True}
        table = routes(
            PY, pr_=merged, checks_=checks(run_("tests", status="in_progress"))
        )
        rc, out, _, clock = go(PY, table)
        self.assertEqual(rc, 0)
        self.assertTrue(out.rstrip().endswith("VERDICT: merged"))
        self.assertEqual(clock.sleeps, [])

    def test_closed_unmerged_pr_stops_at_once(self):
        closed = {**pr(), "state": "closed", "merged": False}
        table = routes(
            PY, pr_=closed, checks_=checks(run_("tests", status="in_progress"))
        )
        rc, out, _, clock = go(PY, table)
        self.assertEqual(rc, 7)
        self.assertTrue(out.rstrip().endswith("VERDICT: closed"))
        self.assertEqual(clock.sleeps, [])

    def test_a_usage_error_is_exit_6_not_conflicts_2(self):
        with (
            self.assertRaises(SystemExit) as cm,
            contextlib.redirect_stderr(io.StringIO()),
        ):
            cw.run(["sportsdataverse/sportsdataverse-py"])  # neither --pr nor --sha
        self.assertEqual(cm.exception.code, 6)

    def test_conflict_with_zero_check_runs(self):
        table = routes(PY, pr_=pr("dirty"), checks_=checks())
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 2)
        self.assertIn("no pull_request workflows will start", out)
        self.assertIn("merge the base branch first", out)
        self.assertTrue(out.rstrip().endswith("VERDICT: conflict"))

    def test_ready_capped_lists_pending(self):
        table = routes(
            PY,
            checks_=checks(
                run_("lint", id=1), run_("docs build", status="in_progress", id=2)
            ),
            reviews=[review(CR)],
            inline_=[inline(10, CR), inline(11, "saiemgilani", "Fixed", reply_to=10)],
        )
        rc, out, _, clock = go(PY, table, "--cap", "15m", "--timeout", "60m")
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(clock.t - T0, 900)
        self.assertLess(clock.t - T0, 3600)
        self.assertIn("PENDING: docs build", out)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready-capped"))

    def test_cap_does_not_apply_while_bot_threads_open(self):
        table = routes(
            PY,
            checks_=checks(run_("docs build", status="in_progress")),
            reviews=[review(CR)],
            inline_=[inline(10, CR)],
        )
        rc, out, _, _ = go(PY, table, "--cap", "1m", "--timeout", "5m")
        self.assertEqual(rc, 3)
        self.assertTrue(out.rstrip().endswith("VERDICT: timeout"))

    def test_zero_checks_is_not_instant_ready(self):
        table = routes(PY, checks_=checks())
        rc, out, _, clock = go(PY, table, "--cap", "5m")
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(clock.t - T0, 300)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready-capped"))

    def test_bots_unaddressed(self):
        table = routes(
            PY,
            checks_=GREEN,
            reviews=[review(CR)],
            inline_=[
                inline(
                    10,
                    CR,
                    "Guard the empty frame " + "x" * 200,
                    path="src/a.py",
                    line=42,
                ),
                inline(11, CR, "bot self-reply does not count", reply_to=10),
                inline(20, "Copilot", "Rename this", path="b.py", line=7),
                inline(21, "saiemgilani", "Done", reply_to=20),
                inline(30, "saiemgilani", "human thread, not a bot's"),
            ],
        )
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 5)
        self.assertIn("src/a.py:42", out)
        self.assertNotIn("b.py:7", out)
        self.assertNotIn("x" * 101, out)
        self.assertTrue(out.rstrip().endswith("VERDICT: bots-unaddressed"))

    def test_timeout(self):
        table = routes(
            PY,
            checks_=checks(run_("slow", status="queued")),
            status_=status(("CodeRabbit", "pending")),
        )
        rc, out, _, _ = go(PY, table, "--timeout", "3m")
        self.assertEqual(rc, 3)
        self.assertTrue(out.rstrip().endswith("VERDICT: timeout"))


class BotStates(unittest.TestCase):
    def snap(self, comments=(), reviews=(), statuses=(), inline_=(), requested=()):
        return {
            "pr": pr(requested=requested),
            "comments": list(comments),
            "reviews": list(reviews),
            "inline": list(inline_),
            "statuses": [{"context": c, "state": s} for c, s in statuses],
        }

    def test_coderabbit_success_status_but_rate_limited_comment(self):
        st = cw.bot_states(
            self.snap(
                comments=[comment(CR, CR_LIMITED)], statuses=[("CodeRabbit", "success")]
            )
        )
        self.assertEqual(st["CodeRabbit"][0], "rate-limited")
        self.assertEqual(st["CodeRabbit"][1], T0)
        for heading in ("> ## Review limit reached", "> ## Rate limit exceeded"):
            st = cw.bot_states(self.snap(comments=[comment(CR, heading)]))
            self.assertEqual(st["CodeRabbit"][0], "rate-limited", heading)

    def test_review_after_limit_notice_is_reviewed(self):
        later = iso(T0 + 600)
        st = cw.bot_states(
            self.snap(comments=[comment(CR, CR_LIMITED)], reviews=[review(CR, later)])
        )
        self.assertEqual(st["CodeRabbit"][0], "reviewed")

    def test_limit_notice_after_review_is_rate_limited(self):
        st = cw.bot_states(
            self.snap(
                comments=[comment(CR, CR_LIMITED, iso(T0 + 600))],
                reviews=[review(CR, T0_ISO)],
            )
        )
        self.assertEqual(st["CodeRabbit"][0], "rate-limited")

    def test_thread_reply_after_limit_notice_is_not_a_review(self):
        # A bot's in-thread reply shows up as an empty-body review plus an
        # inline reply (sportsdataverse-py#736); neither means it re-reviewed.
        later = iso(T0 + 600)
        reply = inline(12, CR, "Thanks for fixing", reply_to=10)
        reply["created_at"] = later
        st = cw.bot_states(
            self.snap(
                comments=[comment(CR, CR_LIMITED)],
                reviews=[review(CR, later, body="")],
                inline_=[reply],
            )
        )
        self.assertEqual(st["CodeRabbit"][0], "rate-limited")

    def test_walkthrough_mentioning_rate_limits_is_not_a_limit(self):
        body = "<!-- summarize by coderabbit.ai -->\nAdds rate limit handling to the scraper."
        guide = "<!-- Generated by sourcery-ai[bot]: start review_guide -->\nAdds rate limit backoff."
        st = cw.bot_states(
            self.snap(comments=[comment(CR, body), comment(SOURCERY, guide)])
        )
        self.assertEqual(st["CodeRabbit"][0], "reviewed")
        self.assertEqual(st["Sourcery"][0], "reviewed")

    def test_sourcery_budget_then_guide_stays_limited(self):
        guide = "<!-- Generated by sourcery-ai[bot]: start review_guide -->\nReviewer's Guide"
        st = cw.bot_states(
            self.snap(
                comments=[
                    comment(SOURCERY, SOURCERY_BUDGET),
                    comment(SOURCERY, guide, iso(T0 + 7)),
                ]
            )
        )
        self.assertEqual(st["Sourcery"][0], "rate-limited")

    def test_pending_signals(self):
        st = cw.bot_states(self.snap(statuses=[("CodeRabbit", "pending")]))
        self.assertEqual(st["CodeRabbit"][0], "pending")
        st = cw.bot_states(
            self.snap(
                comments=[comment(CR, "Currently processing new changes in this PR.")]
            )
        )
        self.assertEqual(st["CodeRabbit"][0], "pending")

    def test_absent_and_copilot(self):
        st = cw.bot_states(self.snap())
        self.assertEqual(st["CodeRabbit"][0], "absent")
        self.assertEqual(st["Copilot"][0], "absent")
        st = cw.bot_states(self.snap(requested=["Copilot"]))
        self.assertEqual(st["Copilot"][0], "pending")
        # GitHub drops a reviewer from requested_reviewers once they review,
        # so "still requested" means a (re-)review is outstanding.
        st = cw.bot_states(
            self.snap(reviews=[review(COPILOT_BOT)], requested=["Copilot"])
        )
        self.assertEqual(st["Copilot"][0], "pending")
        st = cw.bot_states(self.snap(reviews=[review(COPILOT_BOT)]))
        self.assertEqual(st["Copilot"][0], "reviewed")


class CopilotRule(unittest.TestCase):
    def limited(self, repo, **kw):
        return routes(
            repo,
            checks_=GREEN,
            status_=status(("CodeRabbit", "success")),
            comments=[comment(CR, CR_LIMITED), comment(SOURCERY, SOURCERY_BUDGET)],
            **kw,
        )

    def test_allowed_actor_requests_once_and_keeps_waiting(self):
        table = self.limited(PY)
        table["repos/%s/pulls/7" % PY] = Seq(pr(), pr(requested=["Copilot"]), pr())
        table["repos/%s/pulls/7/reviews?per_page=100" % PY] = Seq(
            [], [], [review(COPILOT_BOT)]
        )
        rc, out, fake, _ = go(PY, table, start=T0 + 360)
        self.assertEqual(len(fake.posts), 1)
        self.assertIn("requested_reviewers", fake.posts[0][3])
        self.assertIn("reviewers[]=copilot-pull-request-reviewer[bot]", fake.posts[0])
        self.assertIn("ACTION: requested Copilot review (", out)
        self.assertEqual(rc, 0)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready"))

    @staticmethod
    def kinds(fake):
        return [p[0] for p in fake.posts]  # "api" = REST POST, "pr" = gh pr edit

    def test_rest_reply_listing_copilot_needs_no_fallback(self):
        rc, out, fake, _ = go(PY, self.limited(PY), "--timeout", "2m", start=T0 + 360)
        self.assertEqual(self.kinds(fake), ["api"])
        self.assertNotIn(TIMELINE % PY, fake.gets)  # (a) is enough: no re-read
        self.assertIn("ACTION: requested Copilot review (REST", out)

    def test_rest_reply_without_copilot_but_timeline_event_needs_no_fallback(self):
        # saiemgilani/dotfiles#27: the REST POST did add Copilot; only the
        # timeline (review_requested Copilot) shows it.
        table = self.limited(PY)
        table["POST"] = NOBODY_ADDED
        table[TIMELINE % PY] = [requested_event(iso(T0 + 361))]
        rc, out, fake, _ = go(PY, table, "--timeout", "2m", start=T0 + 360)
        self.assertEqual(self.kinds(fake), ["api"])
        self.assertIn("ACTION: requested Copilot review (REST", out)

    def test_rest_reply_without_copilot_but_requested_on_reread_needs_no_fallback(self):
        table = self.limited(PY)
        table["POST"] = NOBODY_ADDED
        table["repos/%s/pulls/7" % PY] = Seq(pr(), pr(requested=["Copilot"]), pr())
        rc, out, fake, _ = go(PY, table, "--timeout", "2m", start=T0 + 360)
        self.assertEqual(self.kinds(fake), ["api"])

    def test_unconfirmed_rest_falls_back_once_then_reverifies(self):
        table = self.limited(PY)
        table["POST"] = NOBODY_ADDED
        # A Copilot request from BEFORE this run's POST, or a human's request
        # after it, must not count.
        table[TIMELINE % PY] = [
            requested_event(T0_ISO),
            requested_event(iso(T0 + 361), who="alice"),
        ]
        # poll 1, re-read after REST, re-read after gh pr edit, poll 2, then gone.
        table["repos/%s/pulls/7" % PY] = Seq(
            pr(), pr(), pr(requested=["Copilot"]), pr(requested=["Copilot"]), pr()
        )
        rc, out, fake, _ = go(PY, table, start=T0 + 360)
        self.assertEqual(self.kinds(fake), ["api", "pr"])
        self.assertEqual(fake.posts[1][:2], ["pr", "edit"])
        self.assertIn("--add-reviewer", fake.posts[1])
        self.assertIn("ACTION: requested Copilot review (gh pr edit", out)
        self.assertEqual(rc, 0)

    def test_fallback_runs_at_most_once_per_head(self):
        table = self.limited(PY)
        table["POST"] = NOBODY_ADDED
        table["repos/%s/commits/%s/check-runs?per_page=100" % (PY, SHA)] = checks(
            run_("slow", status="in_progress")
        )
        table["repos/%s/pulls/7" % PY] = Seq(
            pr(), pr(), pr(requested=["Copilot"]), pr()
        )
        rc, out, fake, clock = go(PY, table, start=T0 + 360)  # runs to --cap
        self.assertTrue(out.rstrip().endswith("VERDICT: ready-capped"))
        self.assertGreater(clock.t - T0 - 360, 600)
        self.assertEqual(self.kinds(fake).count("pr"), 1)

    def test_both_paths_unverified_asks_user(self):
        table = self.limited(PY)
        table["POST"] = NOBODY_ADDED  # and the re-read shows no Copilot either
        rc, out, fake, _ = go(PY, table, start=T0 + 360)
        self.assertEqual(self.kinds(fake), ["api", "pr"])
        action = [l for l in out.splitlines() if l.startswith("ACTION: Copilot")]
        self.assertEqual(len(action), 1, out)
        self.assertIn("REST:", action[0])
        self.assertIn("gh pr edit:", action[0])
        self.assertEqual(rc, 4)
        self.assertTrue(out.rstrip().endswith("VERDICT: ask-user"))

    def test_both_paths_error_asks_user_with_both_errors(self):
        rc, out, fake, _ = go(PY, self.limited(PY), start=T0 + 360, post_ok=False)
        self.assertEqual(self.kinds(fake), ["api", "pr"])
        action = [l for l in out.splitlines() if l.startswith("ACTION: Copilot")]
        self.assertEqual(len(action), 1, out)
        self.assertIn("HTTP 422", action[0])
        self.assertIn("Could not add reviewer", action[0])
        self.assertEqual(rc, 4)

    def test_requested_copilot_that_never_appears_is_let_go_after_grace(self):
        # POST succeeded but Copilot never shows in requested_reviewers or reviews.
        rc, out, fake, clock = go(PY, self.limited(PY), start=T0 + 360)
        self.assertEqual(len(fake.posts), 1)
        self.assertEqual(rc, 0)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready"))
        self.assertEqual(clock.t, T0 + 360 + 300)  # waited the 5m grace, not --timeout

    def test_env_listed_actor_is_allowed(self):
        table = self.limited(PY, user="helper")
        rc, out, fake, _ = go(
            PY,
            table,
            "--timeout",
            "2m",
            start=T0 + 360,
            env={"SDV_COPILOT_REVIEWERS": "alice, helper"},
        )
        self.assertEqual(len(fake.posts), 1)

    def test_not_allowed_actor_asks(self):
        table = self.limited(PY, user="someone")
        rc, out, fake, _ = go(PY, table, start=T0 + 360)
        self.assertEqual(rc, 4)
        self.assertEqual(fake.posts, [])
        self.assertIn(
            "ACTION: ask the user whether to request a GitHub Copilot review on %s#7"
            % PY,
            out,
        )
        self.assertTrue(out.rstrip().endswith("VERDICT: ask-user"))

    def test_copilot_ask_mode_asks(self):
        rc, _, fake, _ = go(PY, self.limited(PY), "--copilot", "ask", start=T0 + 360)
        self.assertEqual(rc, 4)
        self.assertEqual(fake.posts, [])

    def test_data_repo_never_posts_or_asks(self):
        rc, out, fake, _ = go(DATA, self.limited(DATA), start=T0 + 360)
        self.assertEqual(fake.posts, [])
        self.assertNotIn("ACTION:", out)
        self.assertEqual(rc, 0)

    def test_never_mode(self):
        rc, out, fake, _ = go(
            PY, self.limited(PY), "--copilot", "never", start=T0 + 360
        )
        self.assertEqual(fake.posts, [])
        self.assertEqual(rc, 0)

    def test_under_threshold_waits_then_fires(self):
        table = self.limited(PY, user="someone")
        rc, out, _, clock = go(PY, table, start=T0 + 60)
        self.assertEqual(rc, 4)
        self.assertGreater(clock.t - T0, 300)


NEW = "def456"


class HeadChanges(unittest.TestCase):
    def test_push_mid_wait_restarts_the_cap_clock(self):
        # Push at minute 14; at minute 15 the new head's checks have run 1 minute.
        table = routes(
            PY, checks_=checks(run_("slow", status="in_progress")), reviews=[review(CR)]
        )
        table["repos/%s/pulls/7" % PY] = Seq(*([pr()] * 14), pr(sha=NEW))
        add_head(table, PY, NEW, checks(run_("slow", status="in_progress")))
        rc, out, _, clock = go(PY, table, "--cap", "15m")
        self.assertIn("head moved abc123 -> def456", out)
        self.assertEqual(rc, 0)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready-capped"))
        self.assertEqual(clock.t - T0, 14 * 60 + 15 * 60)

    def test_push_mid_wait_rearms_the_copilot_rule(self):
        # Copilot reviewed the OLD head; after the push both bots are still
        # limited, so the rule must fire again, 5m after the push (not at once).
        limited = [comment(CR, CR_LIMITED), comment(SOURCERY, SOURCERY_BUDGET)]
        table = routes(PY, checks_=GREEN, comments=limited)
        table["repos/%s/pulls/7" % PY] = Seq(
            pr(), pr(requested=["Copilot"]), pr(sha=NEW)
        )
        table["repos/%s/pulls/7/reviews?per_page=100" % PY] = Seq(
            [], [], [review(COPILOT_BOT, iso(T0 + 400), commit_id=SHA)]
        )
        add_head(table, PY, NEW, GREEN, status(("CodeRabbit", "success")))
        rc, out, fake, _ = go(PY, table, "--timeout", "30m", start=T0 + 360)
        self.assertEqual(fake.post_times, [T0 + 360, T0 + 480 + 360])


class Staleness(unittest.TestCase):
    def test_review_of_an_older_commit_waits_out_the_grace(self):
        # Sourcery has no commit status: its review of the previous commit must
        # not count as a review of this head.
        table = routes(
            PY,
            checks_=GREEN,
            status_=status(("CodeRabbit", "success")),
            reviews=[review(CR, commit_id=SHA), review(SOURCERY, commit_id="0ld0ld")],
        )
        rc, out, _, clock = go(PY, table)
        self.assertEqual(rc, 0)
        self.assertTrue(out.rstrip().endswith("VERDICT: ready"))
        self.assertEqual(clock.t - T0, 300)

    def test_bots_grace_flag(self):
        table = routes(PY, checks_=GREEN, reviews=[review(CR)])
        rc, out, _, clock = go(PY, table, "--bots-grace", "0s")
        self.assertEqual((rc, clock.t), (0, T0))
        rc, out, _, clock = go(PY, table, "--bots-grace", "2m")
        self.assertEqual((rc, clock.t - T0), (0, 120))

    def test_bot_states_marks_a_stale_review_absent(self):
        def st(*reviews):
            snap = {
                "pr": pr(),
                "sha": SHA,
                "comments": [],
                "inline": [],
                "reviews": list(reviews),
                "statuses": [],
            }
            return cw.bot_states(snap)["Sourcery"][0]

        self.assertEqual(st(review(SOURCERY, commit_id="0ld0ld")), "absent")
        self.assertEqual(st(review(SOURCERY, commit_id=SHA)), "reviewed")
        self.assertEqual(st(review(SOURCERY)), "reviewed")  # no commit_id: trust it
        self.assertEqual(
            st(
                review(SOURCERY, commit_id=SHA),
                review(SOURCERY, iso(T0 + 60), commit_id="0ld0ld"),
            ),
            "absent",
        )


class UnexpectedErrors(unittest.TestCase):
    def test_bad_payloads_end_in_error_not_a_traceback(self):
        cases = {
            "pr without head": ("repos/%s/pulls/7" % PY, {}),
            "bad json": ("repos/%s/pulls/7" % PY, (0, "<html>not json", "")),
            "bad timestamp": (
                "repos/%s/issues/7/comments?per_page=100" % PY,
                [comment(CR, CR_LIMITED, at="yesterday")],
            ),
        }
        for name, (path, value) in cases.items():
            with self.subTest(name):
                table = routes(PY, checks_=GREEN)
                table[path] = value
                rc, out, _, _ = go(PY, table)
                self.assertEqual(rc, 6)
                errors = [l for l in out.splitlines() if l.startswith("ERROR:")]
                self.assertEqual(len(errors), 1, out)
                self.assertTrue(out.rstrip().endswith("VERDICT: error"))

    def test_keyboard_interrupt_still_propagates(self):
        table = routes(PY)
        table["repos/%s/pulls/7" % PY] = KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            go(PY, table)


class GhRetries(unittest.TestCase):
    def test_rate_limit_sleeps_until_reset_capped_and_retries(self):
        table = routes(PY, checks_=GREEN, reviews=[review(CR)], reset=T0 + 1000)
        key = "repos/%s/pulls/7" % PY
        table[key] = Seq(
            (1, "", "gh: API rate limit exceeded for user (HTTP 403)"), pr()
        )
        rc, out, fake, clock = go(PY, table)
        self.assertEqual(clock.sleeps[0], 300)
        self.assertIn("rate_limit", fake.gets)
        self.assertEqual(fake.gets.count(key), 2)
        self.assertEqual(rc, 0)

    def test_persistent_error_gives_error_verdict(self):
        table = routes(PY)
        table["repos/%s/pulls/7" % PY] = (1, "", "HTTP 404: Not Found")
        rc, out, _, _ = go(PY, table)
        self.assertEqual(rc, 6)
        self.assertTrue(out.rstrip().endswith("VERDICT: error"))


if __name__ == "__main__":
    unittest.main()
