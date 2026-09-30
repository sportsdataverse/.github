#!/usr/bin/env python3
"""Nightly org-wide status snapshot for the SportsDataverse ecosystem.

Writes, under status/:
  ecosystem.json   full machine snapshot (PRs, issues, workflows, releases)
  ecosystem.md     the same as tables, with a doctoc TOC
  summary.json     compact, page-ready view (release tags, producers, packages)
  badges/<repo>/   shields.io endpoint JSON (updated / through / status / wf-*)

Consumed by the chief-of-staff routines (which cannot reach api.github.com),
by sportsdataverse.org/status, and by every README badge in the ecosystem.

Uses `gh api` (GITHUB_TOKEN on Actions; your login locally). Public repos only:
private repos are dropped explicitly, because a local run can see them.
status/producers.json (hand-curated) maps sportsdataverse-data release tags to
the repos that publish them.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

ORG = "sportsdataverse"
EXTRA_REPOS = ["saiemgilani/game-on-paper-app", "BillPetti/baseballr"]
HUB = f"{ORG}/sportsdataverse-data"
STALE_DAYS = 7
OUT = Path(os.environ.get("STATUS_DIR", "status"))
NOW = datetime.now(timezone.utc)
CALLS = 0  # every `gh api` invocation, printed at the end (Actions budget ~800)

# A standalone season year in an asset file name: play_by_play_2026.parquet -> 2026;
# never part of a longer digit run (20260929, 120255).
SEASON_RE = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)")
FAILING = {"failure", "timed_out", "startup_failure"}
COLORS = {
    "passing": "brightgreen",
    "fresh": "brightgreen",
    "idle": "blue",
    "stale": "orange",
    "failing": "red",
    "cancelled": "yellow",
    "unknown": "lightgrey",
    "no runs": "lightgrey",
}
TOC_START = "<!-- START doctoc generated TOC please keep comment here to allow auto update -->"
TOC_END = "<!-- END doctoc generated TOC please keep comment here to allow auto update -->"
RELEASE_TAGS_HEADING = "## sportsdataverse-data release tags — freshness"


# --- GitHub ------------------------------------------------------------------


def _gh_once(path: str):
    global CALLS
    CALLS += 1
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


# --- small pure helpers (unit-tested) ---------------------------------------


def iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def age_days(s, now: datetime | None = None):
    d = iso(s)
    return round(((now or NOW) - d).total_seconds() / 86400, 1) if d else None


def max_season(names) -> int | None:
    """Max standalone 4-digit season year across asset file names."""
    years = [int(y) for n in names for y in SEASON_RE.findall(n)]
    return max(years) if years else None


def in_season(season: dict, today: date) -> bool:
    """`start`/`end` are inclusive MM-DD; a window with start > end wraps the year."""
    md = (today.month, today.day)
    start = tuple(int(x) for x in season["start"].split("-"))
    end = tuple(int(x) for x in season["end"].split("-"))
    if start <= end:
        return start <= md <= end
    return md >= start or md <= end


def drop_private(repos: list) -> list:
    """Nothing private may reach status/: a local run with a user login sees them."""
    return [r for r in repos if not r.get("private") and not r.get("archived") and not r.get("disabled")]


def check_bare_names(full_names) -> None:
    """Badge directories are keyed by bare repo name; refuse to overwrite one."""
    seen: dict = {}
    for full in full_names:
        bare = full.split("/")[1]
        if bare in seen:
            raise SystemExit(f"badge directory collision: {seen[bare]} and {full} share '{bare}'")
        seen[bare] = full


def is_dynamic(path: str | None) -> bool:
    """Dependabot / Copilot 'dynamic' workflows have no file under .github/workflows."""
    return not (path or "").startswith(".github/workflows/")


def wf_stem(path: str) -> str:
    return PurePosixPath(path).stem


def load_producers(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    rules = cfg["rules"]
    for i, r in enumerate(rules):
        for earlier in rules[:i]:
            if r["prefix"].startswith(earlier["prefix"]):
                raise SystemExit(
                    f"producers.json: rule '{r['prefix']}' is shadowed by earlier "
                    f"rule '{earlier['prefix']}' (put the more specific prefix first)"
                )
    bare_pkgs = {p.split("/")[1] for p in cfg["package_repos"]}
    for p in cfg["producers"]:
        missing = set(p["packages"]) - bare_pkgs
        if missing:
            raise SystemExit(f"producers.json: {p['repo']} packages not in package_repos: {missing}")
    return cfg


def match_rule(tag: str, rules: list) -> dict | None:
    """First matching prefix wins (load_producers guarantees no shadowing)."""
    for r in rules:
        if tag.startswith(r["prefix"]):
            return r
    return None


def data_state(updated_at, season: dict, stale_after_days: int, today: date, now: datetime):
    """(state, age_days) for the data alone: fresh | idle | stale | unknown."""
    if not updated_at:
        return "unknown", None
    age = age_days(updated_at, now)
    if not in_season(season, today):
        return "idle", age
    if age > stale_after_days:
        return "stale", age
    return "fresh", age


def producer_state(dstate: str, workflows, updated_at) -> str:
    """failing beats stale beats idle beats fresh (R-SV-8).

    failing = an update workflow's latest run failed AND that run is newer than
    the newest counted asset. If data has landed since the failure, the pipeline
    is evidently delivering, so the data state stands (the workflow's own badge
    and red_workflows still show the failure)."""
    last_data = iso(updated_at)
    for w in workflows:
        if w.get("conclusion") in FAILING:
            ran = iso(w.get("created_at"))
            if last_data is None or ran is None or ran > last_data:
                return "failing"
    return dstate


def badge(label: str, message: str, color: str) -> dict:
    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
        "namedLogo": "github",
    }


def wf_badge(wf: dict) -> dict:
    c, when = wf.get("conclusion"), (wf.get("created_at") or "")[:10]
    if not c:
        return badge(wf["name"], "no runs", COLORS["no runs"])
    if c == "success":
        word = "passing"
    elif c in FAILING:
        word = "failing"
    else:
        word = c  # cancelled / skipped / neutral / action_required / stale
    return badge(wf["name"], f"{word} · {when}", COLORS.get(word, "lightgrey"))


def producer_badges(p: dict) -> dict:
    """{key: badge} for updated / through / status of one summary producer."""
    ds = p["data_state"]
    updated = (
        badge("data updated", p["updated_at"][:10], COLORS[ds])
        if p["updated_at"]
        else badge("data updated", "unknown", COLORS["unknown"])
    )
    through = (
        badge("through", f"{p['through_season']} season", "blue")
        if p["through_season"]
        else badge("through", "unknown", COLORS["unknown"])
    )
    msg = {
        "fresh": "fresh",
        "idle": "idle (off-season)",
        "stale": f"stale {int(p['age_days'] or 0)}d",
        "failing": "failing",
        "unknown": "unknown",
    }[p["state"]]
    return {
        "updated": updated,
        "through": through,
        "status": badge("pipeline", msg, COLORS[p["state"]]),
    }


# --- snapshot -----------------------------------------------------------------


def list_repos() -> list:
    repos = gh(f"orgs/{ORG}/repos?per_page=100&type=all", paginate=True, pages_cap=3) or []
    for full in EXTRA_REPOS:
        r = gh(f"repos/{full}")
        if r:
            repos.append(r)
    return drop_private(repos)


def _run_entry(run: dict, name: str | None = None) -> dict:
    return {
        "name": name or run["name"],
        "file": run["path"],
        "conclusion": run["conclusion"],
        "created_at": run["created_at"],
        "age_days": age_days(run["created_at"]),
        "url": run["html_url"],
        "event": run.get("event"),
    }


def snapshot_workflows(full: str, default: str, backfill: bool) -> dict:
    """{display key: workflow} for every non-dynamic workflow of the repo.

    Latest completed default-branch run per workflow FILE from a 100-run window;
    for producer / raw / package repos, an active workflow with no run in the window
    gets one extra call for its own latest completed run."""
    runs = gh(f"repos/{full}/actions/runs?branch={default}&per_page=100") or {}
    by_file: dict = {}
    for run in runs.get("workflow_runs", []):  # newest-first
        if run.get("status") != "completed" or is_dynamic(run.get("path")):
            continue
        by_file.setdefault(run["path"], _run_entry(run))
    listed = gh(f"repos/{full}/actions/workflows?per_page=100")
    if listed is None:  # Actions disabled / no access: what the runs show is all we know
        wfs = [{"path": p, "name": e["name"], "state": None} for p, e in by_file.items()]
    else:
        wfs = [w for w in listed.get("workflows", []) if w.get("state") != "deleted"]
    out: dict = {}
    for w in sorted(wfs, key=lambda w: w["path"]):
        path = w["path"]
        if is_dynamic(path):
            continue
        entry = by_file.get(path)
        if entry:
            entry = {**entry, "name": w["name"]}
        elif backfill and w.get("state") == "active" and wf_stem(path) != "orphan_scripts":
            # No status= filter: GitHub serves it from a stale index (daily_wbb.yml's
            # newest "completed" run came back from April while September runs existed).
            one = gh(f"repos/{full}/actions/workflows/{w['id']}/runs?branch={default}&per_page=10") or {}
            got = [x for x in one.get("workflow_runs") or [] if x.get("status") == "completed"]
            entry = _run_entry(got[0], w["name"]) if got else None
        if entry is None:
            entry = {
                "name": w["name"],
                "file": path,
                "conclusion": None,
                "created_at": None,
                "age_days": None,
                "url": f"https://github.com/{full}/actions/workflows/{PurePosixPath(path).name}",
                "event": None,
            }
        entry["state"] = w.get("state")
        key = entry["name"] if entry["name"] not in out else path
        out[key] = entry
    return out


def keep_latest_runs(workflows: dict, prev_workflows: dict) -> dict:
    """Never let a workflow's latest run move backwards versus the last snapshot.

    GitHub's runs listing intermittently serves a stale replica (observed: the same
    call returned 375 runs ending 08-24, then 513 ending 09-30), which would flip a
    badge to an old conclusion for a night. Matched by workflow file."""
    prev_by_file = {w.get("file"): w for w in prev_workflows.values() if w.get("file")}
    run_keys = ("conclusion", "created_at", "url", "event")
    out = {}
    for key, w in workflows.items():
        old = prev_by_file.get(w["file"])
        if old and old.get("created_at") and (old["created_at"] > (w.get("created_at") or "")):
            w = {**w, **{k: old.get(k) for k in run_keys}, "age_days": age_days(old["created_at"])}
        out[key] = w
    return out


def snapshot_repo(r: dict, backfill: bool = False, prev: dict | None = None) -> dict:
    full, default = r["full_name"], r.get("default_branch", "main")
    out: dict = {
        "full_name": full,
        "private": r.get("private", False),
        "default_branch": default,
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
    out["workflows"] = keep_latest_runs(snapshot_workflows(full, default, backfill), (prev or {}).get("workflows", {}))
    out["red_workflows"] = [
        n for n, w in out["workflows"].items() if w["conclusion"] not in ("success", "skipped", None)
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
            "max_season": max_season(a["name"] for a in assets),
        }
    out["latest_release_tag"] = rels[0]["tag_name"] if rels else None
    out["newest_asset_at"] = newest_asset
    out["newest_asset_age_days"] = age_days(newest_asset)
    return out


# --- summary --------------------------------------------------------------------


def _wf_public(w: dict) -> dict:
    return {k: w.get(k) for k in ("name", "file", "conclusion", "created_at", "event", "url")}


def build_summary(snap: dict, cfg: dict, now: datetime) -> dict:
    repos = snap["repos"]
    today = now.date()
    hub = repos.get(HUB, {}).get("releases", {})
    owner = {t: match_rule(t, cfg["rules"]) for t in hub}
    release_tags = sorted(
        (
            {
                "tag": t,
                "producer": (owner[t] or {}).get("repo"),
                "assets": x["assets"],
                "newest_asset_at": x["newest_asset_at"],
                "max_season": x.get("max_season"),
            }
            for t, x in hub.items()
        ),
        # stalest first; empty tags (no assets) are not "stale", so they go last
        key=lambda d: (d["newest_asset_at"] is None, d["newest_asset_at"] or "", d["tag"]),
    )
    producers = []
    for p in cfg["producers"]:
        d = repos.get(p["repo"])
        if d is None:  # private, archived or gone: public producers only
            print(f"WARN producer {p['repo']} not in the public snapshot", file=sys.stderr)
            continue
        tags = sorted(t for t, r in owner.items() if r and r["repo"] == p["repo"])
        counted = [t for t in tags if owner[t].get("freshness", True)]
        stamps = [hub[t]["newest_asset_at"] for t in counted if hub[t]["newest_asset_at"]]
        # R-SV-9: through = play-level tags when configured, else every counted tag
        through_tags = p.get("through_tags", counted)
        for t in set(through_tags) - set(tags):
            print(f"WARN {p['repo']}: through tag {t} is not one of its tags", file=sys.stderr)
        seasons = [hub[t]["max_season"] for t in through_tags if (hub.get(t) or {}).get("max_season")]
        updated_at = max(stamps, default=None)
        by_file = {PurePosixPath(w["file"]).name: w for w in d["workflows"].values()}
        wfs = []
        for f in p["update_workflows"]:
            w = by_file.get(f)
            if w is None:
                print(f"WARN {p['repo']}: update workflow {f} not found", file=sys.stderr)
                continue
            wfs.append(_wf_public(w))
        ds, age = data_state(updated_at, p["season"], p["stale_after_days"], today, now)
        producers.append(
            {
                "repo": p["repo"],
                "label": p["label"],
                "sport": p["sport"],
                "packages": p["packages"],
                "raw_repo": p.get("raw_repo"),
                "schedule": p["schedule"],
                "season": p["season"],
                "stale_after_days": p["stale_after_days"],
                "in_season": in_season(p["season"], today),
                "updated_at": updated_at,
                "age_days": age,
                "through_season": max(seasons, default=None),
                "data_state": ds,
                "state": producer_state(ds, wfs, updated_at),
                "tags": len(tags),
                "tag_names": tags,
                "workflows": wfs,
            }
        )
    packages = []
    for full in cfg["package_repos"]:
        d = repos.get(full)
        if d is None:
            continue
        tag = d.get("latest_release_tag")
        packages.append(
            {
                "repo": full,
                "latest_release_tag": tag,
                "published_at": d["releases"][tag]["published_at"] if tag else None,
                "workflows": [_wf_public(w) for w in d["workflows"].values()],
            }
        )
    red = [{"repo": n, **_wf_public(d["workflows"][w])} for n, d in sorted(repos.items()) for w in d["red_workflows"]]
    unmapped = [t["tag"] for t in release_tags if not t["producer"]]
    states: dict = {}
    for p in producers:
        states[p["state"]] = states.get(p["state"], 0) + 1
    return {
        "generated_at": snap["generated_at"],
        "totals": {
            **snap["totals"],
            "release_tags": len(release_tags),
            "unmapped_tags": len(unmapped),
            "producers": states,
        },
        "release_tags": release_tags,
        "producers": producers,
        "packages": packages,
        "red_workflows": red,
        "unmapped_tags": unmapped,
    }


# --- badges ---------------------------------------------------------------------


def badge_files(snap: dict, summary: dict) -> dict:
    """{relative path under badges/: badge} -- every non-dynamic workflow of every
    repo, plus updated / through / status per producer."""
    files: dict = {}
    for full, d in snap["repos"].items():
        bare = full.split("/")[1]
        for w in d["workflows"].values():
            key = f"{bare}/wf-{wf_stem(w['file'])}.json"
            if key in files:
                raise SystemExit(f"two workflows of {full} share the badge {key}")
            files[key] = wf_badge(w)
    for p in summary["producers"]:
        bare = p["repo"].split("/")[1]
        for k, b in producer_badges(p).items():
            files[f"{bare}/{k}.json"] = b
    return files


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


# --- markdown -------------------------------------------------------------------


def _cell(s) -> str:
    return str(s if s is not None else "").replace("|", "\\|")


def render_md(snap: dict, summary: dict) -> str:
    repos = snap["repos"]
    bare = lambda full: (full or "").split("/")[-1]  # noqa: E731
    L = [
        "# SportsDataverse ecosystem status",
        "",
        f"_{len(repos)} public repos · generated {snap['generated_at'][:16]}Z by "
        "`.github/workflows/ecosystem-status.yml` · machine-readable twins: "
        "`ecosystem.json`, `summary.json` · badges: `badges/`._",
        "",
        TOC_START,
        TOC_END,
        "",
    ]
    rt = summary["release_tags"]
    L += [
        RELEASE_TAGS_HEADING,
        "",
        f"{len(rt)} tags on `{HUB}`, stalest first (tags with no assets last). "
        "`producer` comes from "
        "`producers.json`; `through season` is the newest standalone year in the "
        "tag's asset names (SDV end-year convention).",
        "",
        "| tag | producer | assets | newest asset | age (d) | through season |",
        "|---|---|---|---|---|---|",
    ]
    for t in rt:
        L.append(
            f"| {t['tag']} | {bare(t['producer'])} | {t['assets']} | "
            f"{(t['newest_asset_at'] or 'empty')[:16]} | {_cell(age_days(t['newest_asset_at']))} | "
            f"{_cell(t['max_season'])} |"
        )
    L += [
        "",
        "## Producers",
        "",
        "One row per repo that publishes to `sportsdataverse-data` (config: "
        "`producers.json`). `idle` = out of season, never an alarm.",
        "",
        "| repo | state | in season | data updated | through season | update workflows |",
        "|---|---|---|---|---|---|",
    ]
    for p in summary["producers"]:
        wfs = "<br>".join(
            f"`{w['file'].rsplit('/', 1)[-1]}` {w['conclusion'] or 'no runs'} {(w['created_at'] or '')[:10]}".rstrip()
            for w in p["workflows"]
        )
        L.append(
            f"| [{bare(p['repo'])}](https://github.com/{p['repo']}) | {p['state']} | "
            f"{'yes' if p['in_season'] else 'no'} | {(p['updated_at'] or '')[:10]} | "
            f"{_cell(p['through_season'])} | {wfs or '—'} |"
        )
    red = sorted((n, w) for n, d in repos.items() for w in d["red_workflows"])
    L += [
        "",
        "## Red default-branch workflows",
        "",
        "| repo | workflow | conclusion | last run | age (d) |",
        "|---|---|---|---|---|",
    ]
    for n, w in red:
        x = repos[n]["workflows"][w]
        L.append(f"| {n} | {w} | {x['conclusion']} | [run]({x['url']}) | {x['age_days']} |")
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
        "## Open issues",
        "",
        f"Stale = unassigned with no update for at least {STALE_DAYS} days.",
        "",
        "| repo | open issues | stale unassigned |",
        "|---|---|---|",
    ]
    for n, d in sorted(repos.items(), key=lambda t: -len(t[1]["stale_unassigned_issues"])):
        if d["open_issues"]:
            L.append(f"| {n} | {d['open_issues']} | {len(d['stale_unassigned_issues'])} |")
    data_repos = {
        n: d
        for n, d in repos.items()
        if d["releases"] and (n.endswith(("-data", "-raw")) or "sportsdataverse-data" in n)
    }
    L += [
        "",
        "## Release-asset freshness (data producers)",
        "",
        "| repo | latest tag | releases | newest asset | age (d) | last push (d) |",
        "|---|---|---|---|---|---|",
    ]
    for n, d in sorted(data_repos.items(), key=lambda t: t[1]["newest_asset_age_days"] or 9e9):
        L.append(
            f"| {n} | {d['latest_release_tag']} | {len(d['releases'])} | {(d['newest_asset_at'] or '')[:16]} | {d['newest_asset_age_days']} | {d['pushed_age_days']} |"
        )
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
            L.append(f"| {n} | {d['latest_release_tag']} | {pub[:10]} | {d['pushed_age_days']} |")
    un = summary["unmapped_tags"]
    L += [
        "",
        "## Unmapped release tags",
        "",
        f"{len(un)} `{HUB}` tags have no producer in `producers.json` (unattributed "
        "on purpose until the publishing code is found; never guessed).",
        "",
    ]
    L += [f"- `{t}`" for t in un] or ["- none"]
    return "\n".join(L) + "\n"


# --- main -----------------------------------------------------------------------


def main() -> int:
    cfg = load_producers(OUT / "producers.json")
    try:  # last committed snapshot: the floor under each workflow's latest run
        prev = json.loads((OUT / "ecosystem.json").read_text(encoding="utf-8"))["repos"]
    except (OSError, ValueError, KeyError):
        prev = {}
    repos = list_repos()
    check_bare_names(r["full_name"] for r in repos)
    # producer, raw and package repos: consumer pages link their wf-* badges, and a
    # busy raw repo pushes a weekly workflow out of the 100-run window
    backfill = (
        {p["repo"] for p in cfg["producers"]}
        | {p["raw_repo"] for p in cfg["producers"] if p.get("raw_repo")}
        | set(cfg["package_repos"])
    )
    print(f"{len(repos)} public repos", file=sys.stderr)
    snap = {
        "generated_at": NOW.isoformat(),
        "org": ORG,
        "stale_days": STALE_DAYS,
        "repos": {},
    }
    for r in repos:
        try:
            snap["repos"][r["full_name"]] = snapshot_repo(r, r["full_name"] in backfill, prev.get(r["full_name"]))
            print(f"  ok {r['full_name']} ({CALLS} calls)", file=sys.stderr)
        except Exception as e:  # one bad repo must not kill the snapshot
            print(f"  FAIL {r['full_name']}: {e}", file=sys.stderr)
    snap["totals"] = {
        "repos": len(snap["repos"]),
        "open_prs": sum(len(d["open_prs"]) for d in snap["repos"].values()),
        "red_workflows": sum(len(d["red_workflows"]) for d in snap["repos"].values()),
        "stale_unassigned_issues": sum(len(d["stale_unassigned_issues"]) for d in snap["repos"].values()),
    }
    summary = build_summary(snap, cfg, NOW)
    files = badge_files(snap, summary)
    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "ecosystem.json", snap)
    write_json(OUT / "summary.json", summary)
    (OUT / "ecosystem.md").write_text(render_md(snap, summary), encoding="utf-8", newline="\n")
    shutil.rmtree(OUT / "badges", ignore_errors=True)  # workflows that vanished lose their badge
    for rel, b in files.items():
        write_json(OUT / "badges" / rel, b)
    print(json.dumps(summary["totals"]), file=sys.stderr)
    print(f"gh api calls: {CALLS}; badge files: {len(files)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
