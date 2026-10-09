#!/usr/bin/env python3
"""Wait on a PR's CI and review bots, then print one verdict.

Owner rules:
  1. Stop waiting on CI --cap after start once every bot review is addressed and
     no job has failed. Any failure ends the wait at once (never capped).
  2. On a package PR (repo not ending -raw/-data), if CodeRabbit AND Sourcery
     are both rate-limited for more than --bots-limited-after, request a GitHub
     Copilot review when the actor is allowed (saiemgilani, or a login in
     SDV_COPILOT_REVIEWERS); otherwise stop and ask the user.

REST only (`gh api`), except this one call, made at most once per head:
`gh pr edit --add-reviewer @copilot` (GraphQL), when the REST Copilot request did
not take. `gh pr checks` / `gh pr view` would burn the shared GraphQL quota.

Usage:
    python3 ci_wait.py owner/repo (--pr N | --sha SHA) [--interval 60s] [--cap 15m]
        [--timeout 60m] [--bots-limited-after 5m] [--bots-grace 5m]
        [--copilot auto|ask|never] [--package | --no-package]

A push restarts --cap and --bots-grace (CodeRabbit/Sourcery with no review of the
current head count as pending for --bots-grace); --timeout never restarts.

Exit: 0 ready / ready-capped / merged, 1 failed, 2 conflict, 3 timeout, 4 ask-user,
      5 bots-unaddressed, 6 error (including usage errors), 7 closed without merging.
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter

OWNER = "saiemgilani"
COPILOT_REVIEWER = "copilot-pull-request-reviewer[bot]"
COPILOT_LOGINS = {COPILOT_REVIEWER, "Copilot", "copilot-pull-request-reviewer"}
BOTS = {
    "CodeRabbit": {"coderabbitai[bot]"},
    "Sourcery": {"sourcery-ai[bot]"},
    "Copilot": COPILOT_LOGINS,
}
# CodeRabbit's notice carries a hidden marker + heading. A bare "rate limit"
# would also match its walkthrough of any PR that is ABOUT rate limits.
LIMITED = {
    "CodeRabbit": re.compile(
        r"rate limited by coderabbit|##\s*(rate limit exceeded|review limit reached)"
        r"|review rate limited",
        re.I,
    ),
    "Sourcery": re.compile(r"review budget|rate limit", re.I),
}
PENDING = {"CodeRabbit": re.compile(r"currently processing|review in progress", re.I)}
GUIDE = "start review_guide"  # Sourcery's reviewer's guide summarises the PR text
# stale: GitHub retired the check without it ever succeeding
FAILED = {
    "failure",
    "timed_out",
    "cancelled",
    "action_required",
    "startup_failure",
    "stale",
}
EXIT = {
    "ready": 0,
    "ready-capped": 0,
    "failed": 1,
    "conflict": 2,
    "timeout": 3,
    "ask-user": 4,
    "bots-unaddressed": 5,
    "error": 6,
    "merged": 0,
    "closed": 7,
}


class GhError(RuntimeError):
    pass


def _gh(argv):
    try:
        p = subprocess.run(["gh", *argv], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, "", str(e)
    return p.returncode, p.stdout, p.stderr


class Gh:
    """`gh` subprocess layer; `runner(argv) -> (rc, stdout, stderr)` is injectable."""

    def __init__(self, runner=_gh, now=time.time, sleep=time.sleep):
        self.runner, self.now, self.sleep = runner, now, sleep

    def get(self, path):
        failures = limited = 0
        while True:
            rc, out, err = self.runner(["api", path])
            if rc == 0:
                return json.loads(out) if out.strip() else None
            if re.search(r"rate limit|HTTP 429", err, re.I) and limited < 12:
                limited += 1
                wait = self._reset_wait()
                print("gh rate-limited; sleeping %ds" % wait, file=sys.stderr)
                self.sleep(wait)
            elif failures < 3:
                failures += 1
                self.sleep(5 * failures)
            else:
                raise GhError("gh api %s: %s" % (path, err.strip()[:300]))

    def _reset_wait(self):
        rc, out, _ = self.runner(["api", "rate_limit"])
        try:
            reset = json.loads(out)["resources"]["core"]["reset"] if rc == 0 else 0
        except (ValueError, KeyError, TypeError):
            reset = 0
        wait = int(reset - self.now())
        return min(wait if wait > 0 else 60, 300)

    def get_list(self, path):
        """Page a per_page=100 list (or check-runs / status object) to a short page."""
        items, page = [], 1
        while True:
            chunk = self.get(path if page == 1 else "%s&page=%d" % (path, page))
            if isinstance(chunk, dict):  # check-runs / combined status wrap the list
                rows = chunk.get("check_runs", chunk.get("statuses")) or []
            else:
                rows = chunk or []
            items.extend(rows)
            if len(rows) < 100:
                return items
            page += 1

    def copilot_landed(self, repo, n, since):
        """REST re-read: Copilot in requested_reviewers, or a review_requested
        event for it no older than `since` (60 s of clock-skew slack)."""
        base = "repos/%s/" % repo
        if copilot_requested(self.get(base + "pulls/%d" % n)):
            return True
        # The LATEST Copilot request/removal event since the request decides: a removal cancels it.
        events = [
            e
            for e in self.get_list(base + "issues/%d/timeline?per_page=100" % n)
            if e.get("event") in ("review_requested", "review_request_removed")
            and (e.get("requested_reviewer") or {}).get("login") in COPILOT_LOGINS
            and (ts(e.get("created_at")) or 0) >= since - 60
        ]
        if not events:
            return False
        return (
            max(events, key=lambda e: ts(e.get("created_at")) or 0)["event"]
            == "review_requested"
        )

    def request_copilot(self, repo, n):
        """Return (ok, detail): (a) the REST reply lists Copilot; else (b) a REST
        re-read shows it; else (c) `gh pr edit --add-reviewer @copilot` -- GraphQL,
        the one exception to REST-only, at most once per head (the caller) --
        re-verified with (b); else (d) not ok, with both errors."""
        asked = self.now()
        rc, out, err = self.runner(
            [
                "api",
                "-X",
                "POST",
                "repos/%s/pulls/%d/requested_reviewers" % (repo, n),
                "-f",
                "reviewers[]=" + COPILOT_REVIEWER,
            ]
        )
        if rc == 0:
            try:
                if copilot_requested(json.loads(out or "{}")):
                    return True, "REST requested_reviewers"
            except ValueError:
                pass
            rest = "200 but the reply lists no Copilot"
        else:
            rest = one_line(err, 120)
        if self.copilot_landed(repo, n, asked):
            return True, "REST requested_reviewers, confirmed by re-read"
        rc, _, err = self.runner(
            ["pr", "edit", str(n), "-R", repo, "--add-reviewer", "@copilot"]
        )
        if rc != 0:
            return False, "REST: %s; gh pr edit: %s" % (rest, one_line(err, 120))
        if self.copilot_landed(repo, n, asked):
            return True, "gh pr edit --add-reviewer @copilot; REST: %s" % rest
        return False, (
            "REST: %s; gh pr edit: ran, but Copilot is in neither"
            " requested_reviewers nor the timeline" % rest
        )


def duration(text):
    m = re.fullmatch(r"(\d+)([smh]?)", str(text).strip())
    if not m:
        raise argparse.ArgumentTypeError("bad duration %r (use 90s, 15m, 1h)" % text)
    return int(m.group(1)) * {"": 1, "s": 1, "m": 60, "h": 3600}[m.group(2)]


def one_line(text, limit=200):
    return " ".join(str(text).split())[:limit]


def copilot_requested(pr):
    users = pr.get("requested_reviewers") if isinstance(pr, dict) else None
    return any(
        isinstance(u, dict) and u.get("login") in COPILOT_LOGINS for u in users or []
    )


def ts(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ")) if s else None


def login(obj):
    return (obj.get("user") or {}).get("login") or ""


def is_bot(name):
    return name.endswith("[bot]") or name == "Copilot"


def snapshot(gh, repo, n, sha):
    snap = {"pr": None, "comments": [], "inline": [], "reviews": []}
    if n:
        base = "repos/%s/" % repo
        snap["pr"] = gh.get(base + "pulls/%d" % n)
        sha = snap["pr"]["head"]["sha"]
        snap["comments"] = gh.get_list(base + "issues/%d/comments?per_page=100" % n)
        snap["inline"] = gh.get_list(base + "pulls/%d/comments?per_page=100" % n)
        snap["reviews"] = gh.get_list(base + "pulls/%d/reviews?per_page=100" % n)
    snap["sha"] = sha
    runs = gh.get_list("repos/%s/commits/%s/check-runs?per_page=100" % (repo, sha))
    latest = {}  # a re-run supersedes the earlier run of the same job
    for r in runs:
        key = ((r.get("check_suite") or {}).get("id"), r["name"])
        if key not in latest or r["id"] > latest[key]["id"]:
            latest[key] = r
    snap["runs"] = sorted(latest.values(), key=lambda r: r["name"])
    # combined status: latest per context, but `statuses` is paged (30 by default)
    snap["statuses"] = gh.get_list(
        "repos/%s/commits/%s/status?per_page=100" % (repo, sha)
    )
    return snap


def bot_states(snap):
    """{bot: (state, rate_limited_since_epoch_or_None)}."""
    pr = snap.get("pr") or {}
    requested = {u.get("login") for u in pr.get("requested_reviewers") or []}
    cr_status = next(
        (s["state"] for s in snap["statuses"] if s["context"] == "CodeRabbit"), None
    )
    states = {}
    for bot, logins in BOTS.items():
        wrote = [c for c in snap["comments"] if login(c) in logins]
        said = [c for c in wrote if GUIDE not in (c.get("body") or "")]
        # An in-thread reply is an empty-body review + an inline reply: not a review.
        real = [
            r
            for r in snap["reviews"]
            if login(r) in logins and (r.get("body") or "").strip()
        ]
        latest = max(real, key=lambda r: ts(r.get("submitted_at")) or 0, default=None)
        head = snap.get("sha")
        stale = bool(
            head and latest and latest.get("commit_id") not in (None, "", head)
        )
        done = [ts(r.get("submitted_at")) for r in real]
        done += [
            ts(c.get("created_at"))
            for c in snap["inline"]
            if login(c) in logins and not c.get("in_reply_to_id")
        ]
        last_review = max((t for t in done if t), default=None)

        def newest(rx):
            hits = [
                ts(c.get("updated_at") or c.get("created_at"))
                for c in said
                if rx and rx.search(c.get("body") or "")
            ]
            hit = max((t for t in hits if t), default=None)
            return hit if hit and (last_review is None or hit > last_review) else None

        status = cr_status if bot == "CodeRabbit" else None
        limited = newest(LIMITED.get(bot))
        if limited:
            states[bot] = ("rate-limited", limited)
        elif status == "pending" or newest(PENDING.get(bot)) or requested & logins:
            states[bot] = ("pending", None)
        elif status == "success" or (not stale and (last_review or wrote)):
            # status is per-commit; a review of an older commit is not one of this head
            states[bot] = ("reviewed", None)
        else:
            states[bot] = ("absent", None)
    return states


def unaddressed(inline):
    human_replied = {c.get("in_reply_to_id") for c in inline if not is_bot(login(c))}
    return [
        c
        for c in inline
        if not c.get("in_reply_to_id")
        and is_bot(login(c))
        and c["id"] not in human_replied
    ]


class _Parser(argparse.ArgumentParser):
    """Usage errors exit 6 (`error`): argparse's own 2 would read as `conflict`."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(EXIT["error"], "%s: error: %s\n" % (self.prog, message))


def parse_args(argv):
    p = _Parser(description=__doc__.split("\n")[0])
    p.add_argument("repo", help="owner/repo")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--pr", type=int)
    target.add_argument("--sha")
    p.add_argument("--interval", type=duration, default=60)
    p.add_argument("--cap", type=duration, default=15 * 60)
    p.add_argument("--timeout", type=duration, default=60 * 60)
    p.add_argument("--bots-limited-after", type=duration, default=5 * 60)
    p.add_argument("--bots-grace", type=duration, default=5 * 60)
    p.add_argument("--copilot", choices=("auto", "ask", "never"), default="auto")
    p.add_argument("--package", dest="package", action="store_true")
    p.add_argument("--no-package", dest="package", action="store_false")
    p.set_defaults(package=None)
    return p.parse_args(argv)


def run(
    argv=None, gh=None, now=time.time, sleep=time.sleep, env=os.environ, out=sys.stdout
):
    a = parse_args(argv)
    gh = gh or Gh(now=now, sleep=sleep)
    package = (
        a.package if a.package is not None else not re.search(r"-(raw|data)$", a.repo)
    )
    ask = "ACTION: ask the user whether to request a GitHub Copilot review on %s#%s" % (
        a.repo,
        a.pr,
    )
    allowed = {OWNER} | {
        x.strip() for x in env.get("SDV_COPILOT_REVIEWERS", "").split(",") if x.strip()
    }

    def say(line):
        print(line, file=out, flush=True)

    def finish(verdict, snap, notes, threads=()):
        for r in (snap or {}).get("runs", []):
            say("%s\t%s" % (r.get("conclusion") or r.get("status"), r["name"]))
        for s in (snap or {}).get("statuses", []):
            say("%s\t%s" % (s["state"], s["context"]))
        for c in threads:
            say(
                "THREAD %s:%s  %s"
                % (
                    c.get("path"),
                    c.get("line") or c.get("original_line"),
                    " ".join((c.get("body") or "").split())[:100],
                )
            )
        for note in notes:
            say(note)
        say("VERDICT: " + verdict)
        return EXIT[verdict]

    t0 = now()  # --timeout clock: never restarts
    cap_start = head_seen = t0  # --cap and bot-grace clocks: restart on a push
    head_moved_at = last_sha = both_since = actor = copilot_asked_at = snap = None
    copilot_tried = False
    while True:
        try:
            snap = snapshot(gh, a.repo, a.pr, a.sha)
            elapsed = now() - t0
            if last_sha and snap["sha"] != last_sha:
                say(
                    "head moved %s -> %s: --cap, bot grace and the Copilot rule restart"
                    % (last_sha[:7], snap["sha"][:7])
                )
                cap_start = head_seen = head_moved_at = now()
                both_since, copilot_tried, copilot_asked_at = None, False, None
            last_sha = snap["sha"]
            state = (snap["pr"] or {}).get("state")
            if (
                a.pr and state == "closed"
            ):  # merged mid-wait (PR 736): a stuck bot status would hold it to --timeout
                merged = bool((snap["pr"] or {}).get("merged"))
                return finish(
                    "merged" if merged else "closed",
                    snap,
                    [
                        "PR is merged: nothing left to wait for"
                        if merged
                        else "PR was closed without merging"
                    ],
                )
            runs = snap["runs"]
            ci = [s for s in snap["statuses"] if s["context"] != "CodeRabbit"]
            failed = [
                r["name"]
                for r in runs
                if r["status"] == "completed" and r.get("conclusion") in FAILED
            ]
            failed += [s["context"] for s in ci if s["state"] in ("failure", "error")]
            pending = [r["name"] for r in runs if r["status"] != "completed"]
            pending += [s["context"] for s in ci if s["state"] == "pending"]
            if not runs and not ci:  # just pushed: checks not registered yet
                pending = ["(no checks registered yet)"]
            threads = unaddressed(snap["inline"])
            bots = bot_states(snap) if a.pr else {}
            pr = snap["pr"] or {}

            counts = Counter(r.get("conclusion") or r["status"] for r in runs)
            say(
                "[%dm%02ds] %s | checks: %s | statuses: %s | %s | open bot threads: %d"
                % (
                    int(elapsed) // 60,
                    int(elapsed) % 60,
                    snap["sha"][:7],
                    ", ".join("%d %s" % (v, k) for k, v in sorted(counts.items()))
                    or "none",
                    ", ".join(
                        "%d %s" % (v, k)
                        for k, v in sorted(Counter(s["state"] for s in ci).items())
                    )
                    or "none",
                    " ".join("%s=%s" % (b, st[0]) for b, st in bots.items())
                    or "bots: n/a",
                    len(threads),
                )
            )

            if failed:
                return finish("failed", snap, ["FAILED: " + n for n in failed], threads)
            if pr.get("mergeable_state") == "dirty":
                return finish(
                    "conflict",
                    snap,
                    [
                        "PR conflicts with base: no pull_request workflows will start; "
                        "merge the base branch first"
                    ],
                    threads,
                )

            waiting = [b for b, st in bots.items() if st[0] == "pending"]
            # GitHub returns mergeable null / "unknown" while it recomputes after a push;
            # until then a conflict is undecided, so neither ready nor the cap may pass it.
            if pr and (
                pr.get("mergeable") is None or pr.get("mergeable_state") == "unknown"
            ):
                waiting.append("mergeability (GitHub is computing it)")
            # An auto-reviewer with no review of THIS head may still be coming;
            # once the grace is over, absent means "not installed".
            if now() - head_seen < a.bots_grace:
                waiting += [
                    b
                    for b in ("CodeRabbit", "Sourcery")
                    if bots.get(b, ("",))[0] == "absent"
                ]
            if (  # we requested Copilot but it never showed up: stop after the grace
                copilot_asked_at is not None
                and bots["Copilot"][0] == "absent"
                and now() - copilot_asked_at < a.bots_grace
            ):
                waiting.append("Copilot")
            cr, so = bots.get("CodeRabbit", ("",))[0], bots.get("Sourcery", ("",))[0]
            if cr == so == "rate-limited":
                # after a push the 5m window starts at the push, not at old notices
                seen = max(
                    bots["CodeRabbit"][1], bots["Sourcery"][1], head_moved_at or 0
                )
                both_since = seen if both_since is None else min(both_since, seen)
            else:
                both_since = None
            if (
                both_since is not None
                and package
                and a.copilot != "never"
                and bots["Copilot"][0] == "absent"
                and not copilot_tried
            ):
                if now() - both_since <= a.bots_limited_after:
                    waiting.append("CodeRabbit+Sourcery rate-limited")
                else:
                    if a.copilot == "auto" and actor is None:
                        actor = (gh.get("user") or {}).get("login", "")
                    if a.copilot == "ask" or actor not in allowed:
                        return finish(
                            "ask-user",
                            snap,
                            [
                                "CodeRabbit and Sourcery both rate-limited > %ds"
                                % a.bots_limited_after,
                                ask,
                            ],
                            threads,
                        )
                    copilot_tried = True
                    ok, how = gh.request_copilot(a.repo, a.pr)
                    if not ok:
                        return finish(
                            "ask-user",
                            snap,
                            [
                                "ACTION: Copilot review request failed (%s)" % how,
                                ask,
                            ],
                            threads,
                        )
                    say("ACTION: requested Copilot review (%s)" % how)
                    copilot_asked_at = now()
                    waiting.append("Copilot")

            if not waiting and not pending:
                if threads:
                    return finish(
                        "bots-unaddressed",
                        snap,
                        [
                            "UNADDRESSED: %d bot thread(s) without a human reply"
                            % len(threads)
                        ],
                        threads,
                    )
                return finish("ready", snap, [], threads)
            if not waiting and not threads and now() - cap_start >= a.cap:
                return finish("ready-capped", snap, ["PENDING: " + n for n in pending])
            if elapsed >= a.timeout:
                return finish(
                    "timeout",
                    snap,
                    ["PENDING: " + n for n in pending]
                    + ["WAITING ON: " + b for b in waiting],
                    threads,
                )
        except GhError as e:
            return finish("error", snap, ["ERROR: " + one_line(e, 300)])
        # A bad payload must not traceback: exit 1 would read as "CI failed".
        except Exception as e:
            return finish(
                "error",
                None,
                ["ERROR: unexpected %s: %s" % (type(e).__name__, one_line(e))],
            )
        sleep(a.interval)


if __name__ == "__main__":
    sys.exit(run())
