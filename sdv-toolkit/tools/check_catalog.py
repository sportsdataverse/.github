#!/usr/bin/env python3
"""Assert catalog.json matches the skills/ and agents/ directories on disk.

The whole point of the catalog is that it cannot drift from the tree. This
runs in CI; a skill added without a catalog row fails the build.
"""

import json
import pathlib
import sys

REQUIRED_FIELDS = ("name", "kind", "purpose", "archetypes")
VALID_KINDS = ("skill", "agent", "hook")


def discover(root: pathlib.Path) -> tuple[set, set]:
    """Return (skill names, agent names) actually present on disk."""
    skills_dir = root / "skills"
    agents_dir = root / "agents"
    skills = (
        {
            d.name
            for d in skills_dir.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        }
        if skills_dir.is_dir()
        else set()
    )
    agents = {f.stem for f in agents_dir.glob("*.md")} if agents_dir.is_dir() else set()
    return skills, agents


def frontmatter_problems(name: str, text: str, kind: str = "skill") -> list:
    """Problems with one SKILL.md's (or agents/<name>.md's) front matter.

    `claude plugin validate` (2.1.326) does not check skills and tolerates these
    agent errors, but a plain value holding ': ' is a YAML error ("mapping values
    are not allowed here") that other loaders reject. A value holding ' #' is
    silently cut at the '#'.
    """
    # ponytail: stdlib subset check of top-level plain scalars, not a YAML parser
    # (tools stay stdlib-only so release.py runs on a bare python). Upgrade path:
    # yaml.safe_load once the tools take a dependency; test_check_catalog
    # cross-checks this against PyYAML when it is installed.
    who = "%s %r" % (kind, name)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ["%s: does not open with a --- front-matter block" % who]
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        return ["%s: front matter has no closing ---" % who]
    problems, values = [], {}
    body = lines[1:end]
    for i, line in enumerate(body):
        if not line.strip() or line[0] in " 	#-":
            continue  # continuation, nested block, comment or list item
        key, sep, value = line.partition(":")
        if not sep:
            problems.append("%s: front-matter line %r is not 'key: value'" % (who, line[:60]))
            continue
        value = value.strip()
        if value[:1] in ("|", ">"):
            nxt = body[i + 1] if i + 1 < len(body) else ""
            value = nxt.strip() if nxt[:1] in " 	" else ""
        elif value[:1] not in ("'", '"', "[", "{") and (": " in value or " #" in value):
            problems.append(
                "%s: %s is an unquoted value containing %r; quote it or use '>-'"
                % (who, key.strip(), ": " if ": " in value else " #")
            )
        values[key.strip()] = value
    if values.get("name", "").strip("'\"") != name:
        problems.append(
            "%s: front-matter name %r does not match its path" % (who, values.get("name"))
        )
    if not values.get("description", "").strip("'\""):
        problems.append("%s: front matter has no description" % who)
    return problems


def check(root: pathlib.Path) -> list:
    """Return a list of problem strings. Empty list means the catalog is bound."""
    problems = []
    catalog_path = root / "catalog.json"
    if not catalog_path.exists():
        return ["catalog.json is missing at %s" % catalog_path]

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return ["catalog.json is not valid JSON: %s" % exc]

    entries = catalog.get("entries", [])
    for i, entry in enumerate(entries):
        for field in REQUIRED_FIELDS:
            if not entry.get(field):
                problems.append(
                    "entry %d (%s): missing required field %r"
                    % (i, entry.get("name", "<unnamed>"), field)
                )
        kind = entry.get("kind")
        if kind and kind not in VALID_KINDS:
            problems.append(
                "entry %s: kind %r is not one of %s"
                % (entry.get("name"), kind, VALID_KINDS)
            )

    catalog_skills = {
        e["name"] for e in entries if e.get("kind") == "skill" and e.get("name")
    }
    catalog_agents = {
        e["name"] for e in entries if e.get("kind") == "agent" and e.get("name")
    }
    disk_skills, disk_agents = discover(root)

    for name in sorted(disk_skills - catalog_skills):
        problems.append("skill %r exists on disk but has no catalog.json row" % name)
    for name in sorted(catalog_skills - disk_skills):
        problems.append(
            "catalog.json lists skill %r but skills/%s/SKILL.md does not exist"
            % (name, name)
        )
    for name in sorted(disk_skills):
        text = (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        problems.extend(frontmatter_problems(name, text))
    for name in sorted(disk_agents):
        text = (root / "agents" / (name + ".md")).read_text(encoding="utf-8")
        problems.extend(frontmatter_problems(name, text, kind="agent"))
    for name in sorted(disk_agents - catalog_agents):
        problems.append("agent %r exists on disk but has no catalog.json row" % name)
    for name in sorted(catalog_agents - disk_agents):
        problems.append(
            "catalog.json lists agent %r but agents/%s.md does not exist" % (name, name)
        )

    return problems


def main(argv) -> int:
    root = (
        pathlib.Path(argv[1])
        if len(argv) > 1
        else pathlib.Path(__file__).resolve().parent.parent
    )
    problems = check(root)
    if problems:
        sys.stderr.write("catalog check FAILED (%d problem(s)):\n" % len(problems))
        for p in problems:
            sys.stderr.write("  - %s\n" % p)
        return 1
    sys.stdout.write("catalog check OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
