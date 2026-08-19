#!/usr/bin/env python3
"""Nightly org-wide status snapshot for the SportsDataverse ecosystem.

Writes status/ecosystem.json (machine) + status/ecosystem.md (human). Consumed by
the chief-of-staff routines (which cannot reach api.github.com themselves) and by
anyone who wants a one-page view of open PRs, stale issues, default-branch
workflow health, and release-asset freshness across every repo.

Uses `gh api` (GITHUB_TOKEN on Actions; your login locally). Public repos only
need read; private repos the token can't see are skipped, not failed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ORG = "sportsdataverse"
EXTRA_REPOS = ["saiemgilani/game-on-paper-app"]
STALE_DAYS = 7
OUT = Path(os.environ.get("STATUS_DIR", "status"))
NOW = datetime.now(timezone.utc)


def _gh_once(path: str):
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json", path]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        if not any(k in r.stderr for k in ("404", "403", "410")):
            print(f"WARN gh api {path}: {r.stderr.strip()[:200]}", file=sys.stderr)
        return None
    return json.loads(r.stdout or "null")


def gh(path: str, paginate: bool = False, pages_cap: int = 5):
    """Call `gh api`; None on 403/404/410 (private / disabled). Manual pagination
    (works on old gh without --slurp); capped at pages_cap pages of 100."""
    if not paginate:
        return _gh_once(path)
    flat: list = []
    for page in range(1, pages_cap + 1):
        sep = "&" if "?" in path else "?"
        data = _gh_once(f"{path}{sep}page={page}")
        if not isinstance(data, list):
            break
        flat.extend(data)
        if len(data) < 100:
            break
    return flat


def iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def age_days(s):
    d = iso(s)
    return round((NOW - d).total_seconds() / 86400, 1) if d else None


def list_repos() -> list:
    repos = (
        gh(f"orgs/{ORG}/repos?per_page=100&type=all", paginate=True, pages_cap=3) or []
    )
    for full in EXTRA_REPOS:
        r = gh(f"repos/{full}")
        if r:
            repos.append(r)
    return [r for r in repos if not r.get("archived") and not r.get("disabled")]


def snapshot_repo(r: dict) -> dict:
    full, default = r["full_name"], r.get("default_branch", "main")
    out: dict = {
        "full_name": full,
        "private": r.get("private", False),
        "pushed_at": r.get("pushed_at"),
        "pushed_age_days": age_days(r.get("pushed_at")),
        "open_prs": [],
        "open_issues": 0,
        "stale_unassigned_issues": [],
        "workflows": {},
        "red_workflows": [],
        "releases": {},
    }
    for p in gh(f"repos/{full}/pulls?state=open&per_page=100") or []:
        out["open_prs"].append(
            {
                "number": p["number"],
                "title": p["title"],
                "author": p["user"]["login"],
                "draft": p.get("draft", False),
                "updated_at": p["updated_at"],
                "age_days": age_days(p["created_at"]),
                "idle_days": age_days(p["updated_at"]),
                "url": p["html_url"],
            }
        )
    issues = [
        i
        for i in (
            gh(
                f"repos/{full}/issues?state=open&per_page=100",
                paginate=True,
                pages_cap=3,
            )
            or []
        )
        if "pull_request" not in i
    ]
    out["open_issues"] = len(issues)
    cutoff = NOW - timedelta(days=STALE_DAYS)
    out["stale_unassigned_issues"] = [
        {
            "number": i["number"],
            "title": i["title"],
            "idle_days": age_days(i["updated_at"]),
            "url": i["html_url"],
        }
        for i in issues
        if not i.get("assignees") and iso(i["updated_at"]) < cutoff
    ][:25]
    runs = gh(f"repos/{full}/actions/runs?branch={default}&per_page=30") or {}
    latest: dict = {}
    for run in runs.get("workflow_runs", []):  # newest-first
        if run.get("status") != "completed" or run.get("event") == "dynamic":
            continue  # dynamic = Dependabot graph updates, not CI
        latest.setdefault(
            run["name"],
            {
                "conclusion": run["conclusion"],
                "created_at": run["created_at"],
                "age_days": age_days(run["created_at"]),
                "url": run["html_url"],
                "event": run.get("event"),
            },
        )
    out["workflows"] = latest
    out["red_workflows"] = [
        n
        for n, w in latest.items()
        if w["conclusion"] not in ("success", "skipped", None)
    ]
    rels = gh(f"repos/{full}/releases?per_page=100", paginate=True, pages_cap=5) or []
    newest_asset = None
    for rel in rels:
        assets = rel.get("assets", [])
        mx = max((a["updated_at"] for a in assets), default=None)
        if mx and (newest_asset is None or mx > newest_asset):
            newest_asset = mx
        out["releases"][rel["tag_name"]] = {
            "published_at": rel.get("published_at"),
            "assets": len(assets),
            "asset_bytes": sum(a.get("size", 0) for a in assets),
            "newest_asset_at": mx,
        }
    out["latest_release_tag"] = rels[0]["tag_name"] if rels else None
    out["newest_asset_at"] = newest_asset
    out["newest_asset_age_days"] = age_days(newest_asset)
    return out


def render_md(snap: dict) -> str:
    repos = snap["repos"]
    L = [
        f"# SportsDataverse ecosystem status — {snap['generated_at'][:16]}Z",
        "",
        f"_{len(repos)} repos · regenerated nightly by `.github/workflows/ecosystem-status.yml`. "
        "Machine-readable twin: `ecosystem.json`._",
        "",
    ]
    red = sorted((n, w) for n, d in repos.items() for w in d["red_workflows"])
    L += [
        "## Red default-branch workflows",
        "",
        "| repo | workflow | conclusion | last run | age (d) |",
        "|---|---|---|---|---|",
    ]
    for n, w in red:
        x = repos[n]["workflows"][w]
        L.append(
            f"| {n} | {w} | {x['conclusion']} | [run]({x['url']}) | {x['age_days']} |"
        )
    if not red:
        L.append("| — | none red | | | |")
    L += [
        "",
        "## Open PRs (most idle first)",
        "",
        "| repo | PR | author | age (d) | idle (d) | draft |",
        "|---|---|---|---|---|---|",
    ]
    prs = [(n, p) for n, d in repos.items() for p in d["open_prs"]]
    for n, p in sorted(prs, key=lambda t: -(t[1]["idle_days"] or 0)):
        title = p["title"][:70].replace("|", "\\|")
        L.append(
            f"| {n} | [#{p['number']}]({p['url']}) {title} | {p['author']} | {p['age_days']} | {p['idle_days']} | {'y' if p['draft'] else ''} |"
        )
    if not prs:
        L.append("| — | none open | | | | |")
    L += [
        "",
        f"## Open issues (stale = unassigned, no update ≥ {STALE_DAYS}d)",
        "",
        "| repo | open issues | stale unassigned |",
        "|---|---|---|",
    ]
    for n, d in sorted(
        repos.items(), key=lambda t: -len(t[1]["stale_unassigned_issues"])
    ):
        if d["open_issues"]:
            L.append(
                f"| {n} | {d['open_issues']} | {len(d['stale_unassigned_issues'])} |"
            )
    data_repos = {
        n: d
        for n, d in repos.items()
        if d["releases"]
        and (n.endswith(("-data", "-raw")) or "sportsdataverse-data" in n)
    }
    L += [
        "",
        "## Release-asset freshness (data producers)",
        "",
        "| repo | latest tag | releases | newest asset | age (d) | last push (d) |",
        "|---|---|---|---|---|---|",
    ]
    for n, d in sorted(
        data_repos.items(), key=lambda t: t[1]["newest_asset_age_days"] or 9e9
    ):
        L.append(
            f"| {n} | {d['latest_release_tag']} | {len(d['releases'])} | {(d['newest_asset_at'] or '')[:16]} | {d['newest_asset_age_days']} | {d['pushed_age_days']} |"
        )
    hub = repos.get(f"{ORG}/sportsdataverse-data")
    if hub:
        L += [
            "",
            f"## sportsdataverse-data release tags — freshness ({len(hub['releases'])} tags, stalest first)",
            "",
            "| tag | assets | newest asset | age (d) |",
            "|---|---|---|---|",
        ]
        tags = sorted(hub["releases"].items(), key=lambda t: t[1]["newest_asset_at"] or "")
        for tag, x in tags:
            L.append(f"| {tag} | {x['assets']} | {(x['newest_asset_at'] or '')[:16]} | {age_days(x['newest_asset_at'])} |")
    L += [
        "",
        "## Package repos — latest release",
        "",
        "| repo | latest tag | published | last push (d) |",
        "|---|---|---|---|",
    ]
    for n, d in sorted(repos.items()):
        if d["releases"] and n not in data_repos:
            pub = d["releases"][d["latest_release_tag"]]["published_at"] or ""
            L.append(
                f"| {n} | {d['latest_release_tag']} | {pub[:10]} | {d['pushed_age_days']} |"
            )
    return "\n".join(L) + "\n"


def main() -> int:
    repos = list_repos()
    print(f"{len(repos)} repos", file=sys.stderr)
    snap = {
        "generated_at": NOW.isoformat(),
        "org": ORG,
        "stale_days": STALE_DAYS,
        "repos": {},
    }
    for r in repos:
        try:
            snap["repos"][r["full_name"]] = snapshot_repo(r)
            print(f"  ok {r['full_name']}", file=sys.stderr)
        except Exception as e:  # one bad repo must not kill the snapshot
            print(f"  FAIL {r['full_name']}: {e}", file=sys.stderr)
    snap["totals"] = {
        "repos": len(snap["repos"]),
        "open_prs": sum(len(d["open_prs"]) for d in snap["repos"].values()),
        "red_workflows": sum(len(d["red_workflows"]) for d in snap["repos"].values()),
        "stale_unassigned_issues": sum(
            len(d["stale_unassigned_issues"]) for d in snap["repos"].values()
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ecosystem.json").write_text(
        json.dumps(snap, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    (OUT / "ecosystem.md").write_text(render_md(snap), encoding="utf-8")
    print(json.dumps(snap["totals"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
