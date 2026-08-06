#!/usr/bin/env python3
"""Render README, plugin.json, and marketplace.json descriptions from catalog.json.

plugin.json's hand-written description drifted (claimed 25 skills against a
tree of 26) and marketplace.json's drifted separately. Generating both from
the catalog removes the drift class rather than fixing an instance of it.
"""

import json
import pathlib
import sys


def _split(catalog):
    entries = catalog.get("entries", [])
    skills = sorted(
        [e for e in entries if e.get("kind") == "skill"], key=lambda e: e["name"]
    )
    agents = sorted(
        [e for e in entries if e.get("kind") == "agent"], key=lambda e: e["name"]
    )
    return skills, agents


def _plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def render_readme(catalog) -> str:
    skills, agents = _split(catalog)
    out = [
        "# sdv-toolkit",
        "",
        "SportsDataverse engineering toolkit, shared across the ~40 SDV repos (Python + R).",
        "",
        "<!-- GENERATED FROM catalog.json BY tools/render.py -- DO NOT EDIT BY HAND -->",
        "",
        "Every skill invokes as `/<name>`. A `SessionStart` router emits a per-archetype",
        "routing card automatically; run `/sdv-guide` for the full index.",
        "",
        "## Skills",
        "",
        "| Skill | When to reach for it |",
        "|---|---|",
    ]
    for e in skills:
        out.append("| `/%s` | %s |" % (e["name"], e["purpose"]))
    out += ["", "## Agents", "", "| Agent | What it reviews |", "|---|---|"]
    for e in agents:
        out.append("| `%s` | %s |" % (e["name"], e["purpose"]))
    out.append("")
    return "\n".join(out)


def render_plugin_description(catalog) -> str:
    skills, agents = _split(catalog)
    names = ", ".join("/" + e["name"] for e in skills)
    return (
        "SportsDataverse engineering toolkit -- %s and %s shared across the ~40 SDV repos "
        "(Python + R). A SessionStart router detects the repo archetype and emits a routing "
        "card, so conventions load on arrival instead of being recalled. Skills: %s."
        % (_plural(len(skills), "skill"), _plural(len(agents), "agent"), names)
    )


def render_marketplace_description(catalog) -> str:
    skills, agents = _split(catalog)
    return (
        "SportsDataverse engineering toolkit: %s and %s covering the ship lifecycle, "
        "R/Python porting, the raw/data producer pipeline, model spines, provider "
        "onboarding, and documentation -- with an archetype router that loads the right "
        "conventions on session start."
        % (_plural(len(skills), "skill"), _plural(len(agents), "agent"))
    )


def main(argv) -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    org_root = root.parent
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    check = "--check" in argv

    targets = []

    readme = render_readme(catalog)
    targets.append((root / "README.md", readme, None))

    plugin_path = root / ".claude-plugin" / "plugin.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    plugin["description"] = render_plugin_description(catalog)
    targets.append((plugin_path, json.dumps(plugin, indent=2) + "\n", None))

    market_path = org_root / ".claude-plugin" / "marketplace.json"
    if market_path.exists():
        market = json.loads(market_path.read_text(encoding="utf-8"))
        for p in market.get("plugins", []):
            if p.get("name") == "sdv-toolkit":
                p["description"] = render_marketplace_description(catalog)
        targets.append((market_path, json.dumps(market, indent=2) + "\n", None))

    stale = []
    for path, content, _ in targets:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != content:
            if check:
                stale.append(str(path))
            else:
                path.write_text(content, encoding="utf-8")

    if check and stale:
        sys.stderr.write("render --check FAILED; these are stale:\n")
        for s in stale:
            sys.stderr.write("  - %s\n" % s)
        sys.stderr.write("Run: python tools/render.py\n")
        return 1
    sys.stdout.write("render %s\n" % ("OK" if check else "written"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
