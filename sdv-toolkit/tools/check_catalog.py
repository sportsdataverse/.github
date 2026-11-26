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


def _scalars(node):
    """Every value scalar under a composed PyYAML node (mapping keys skipped)."""
    if hasattr(node, "value") and isinstance(node.value, list):
        for item in node.value:
            yield from _scalars(item[1] if isinstance(item, tuple) else item)
    elif node is not None:
        yield node


def _yaml_values(yaml, who: str, body: list) -> tuple:
    """Parse the front matter with PyYAML: exact, used whenever it is installed (CI)."""
    src = "\n".join(body)
    try:
        root, data = yaml.compose(src), yaml.safe_load(src)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        what = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        at = " at line %d" % (mark.line + 2) if mark else ""
        return [
            "%s: front matter is not valid YAML (%s%s); quote the value or use '>-'"
            % (who, what, at)
        ], None
    if not isinstance(data, dict):
        return ["%s: front matter is not a key: value mapping" % who], None
    problems = []
    for node in _scalars(root):
        # A '#' after a plain value on the same line starts a comment: YAML keeps
        # only the text before it. Block (| >) and quoted scalars are not affected.
        line, col = node.end_mark.line, node.end_mark.column
        if (
            node.style is None
            and line < len(body)
            and body[line][col:].lstrip().startswith("#")
        ):
            problems.append(
                "%s: line %d: ' #' after an unquoted value starts a comment, so YAML "
                "drops the rest; quote it or use '>-'" % (who, line + 2)
            )
    return problems, {k: "" if v is None else str(v) for k, v in data.items()}


def _subset_values(who: str, body: list) -> tuple:
    """Stdlib fallback: top-level scalars only."""
    # ponytail: subset, not a YAML parser, so release.py still runs on a bare python.
    # It misses e.g. a trailing ':', a value opening with * @ ` % !, and text after a
    # closing quote; CI installs PyYAML and takes the exact path instead.
    problems, values, plain = [], {}, None

    def bad(n, msg):
        problems.append("%s: line %d: %s; quote it or use '>-'" % (who, n + 2, msg))

    for i, line in enumerate(body):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            if line[0] == "\t":
                bad(i, "indented with a tab, which YAML does not allow")
            elif plain and (": " in line or " #" in line):
                bad(
                    i,
                    "continues unquoted %s and contains %r"
                    % (plain, ": " if ": " in line else " #"),
                )
            continue  # continuation, nested block or block-scalar content
        plain = None
        if line[0] == "-":
            continue
        key, sep, value = line.partition(":")
        key = key.strip()
        if not sep:
            problems.append(
                "%s: front-matter line %r is not 'key: value'" % (who, line[:60])
            )
            continue
        if value[:1] not in ("", " "):
            bad(i, "%s needs one space after ':', not %r" % (key, value[:1]))
            continue
        value = value.strip()
        if value[:1] in ("|", ">"):
            nxt = next((l for l in body[i + 1 :] if l.strip()), "")
            value = nxt.strip() if nxt[:1] == " " else ""
        elif value[:1] not in ("'", '"', "[", "{"):
            plain = key if value else None
            if ": " in value or " #" in value:
                bad(
                    i,
                    "%s is an unquoted value containing %r"
                    % (key, ": " if ": " in value else " #"),
                )
        values[key] = value.strip("'\"")
    return problems, values


def frontmatter_problems(
    name: str, text: str, kind: str = "skill", use_yaml=None
) -> list:
    """Problems with one SKILL.md's (or agents/<name>.md's) front matter.

    `claude plugin validate` (2.1.326) does not check skills and tolerates these
    agent errors, but a plain value holding ': ' is a YAML error ("mapping values
    are not allowed here") that other loaders reject, and a ' #' after a plain value
    silently cuts it there. use_yaml: None = PyYAML if installed, else the subset.
    """
    who = "%s %r" % (kind, name)
    lines = text.lstrip(chr(0xFEFF)).splitlines()
    if not lines or lines[0].strip() != "---":
        return ["%s: does not open with a --- front-matter block" % who]
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        return ["%s: front matter has no closing ---" % who]
    body = lines[1:end]
    yaml = None
    if use_yaml is not False:
        try:
            import yaml
        except ImportError:
            if use_yaml:
                raise
    problems, values = (
        _yaml_values(yaml, who, body) if yaml else _subset_values(who, body)
    )
    if values is None:
        return problems
    if values.get("name", "") != name:
        problems.append(
            "%s: front-matter name %r does not match its path"
            % (who, values.get("name"))
        )
    if not values.get("description", "").strip():
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
    try:
        import yaml  # noqa: F401
    except ImportError:
        # Not silent: a bare-python pass is partial; CI (PyYAML installed) is exact.
        sys.stderr.write(
            "NOTE: PyYAML not installed, so front matter was checked with the stdlib "
            "subset only (it misses e.g. a trailing ':'). CI runs the exact check; for "
            "it here: uv run --with pyyaml python tools/check_catalog.py .\n"
        )
    sys.stdout.write("catalog check OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
