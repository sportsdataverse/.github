"""Tests for check_catalog. Run: python -m unittest discover -s tools -p 'test_*.py'"""

import json
import pathlib
import tempfile
import unittest

import check_catalog


def build(root: pathlib.Path, skills, agents, catalog) -> None:
    """Create a fake toolkit tree plus a catalog.json."""
    for name in skills:
        d = root / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\nname: %s\ndescription: Use when testing.\n---\n" % name,
            encoding="utf-8",
        )
    (root / "agents").mkdir(parents=True, exist_ok=True)
    for name in agents:
        (root / "agents" / (name + ".md")).write_text(
            "---\nname: %s\ndescription: Use when testing.\n---\n" % name,
            encoding="utf-8",
        )
    (root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")


def entry(name, kind):
    return {"name": name, "kind": kind, "purpose": "p", "archetypes": ["sdv-py"]}


class CheckCatalogTest(unittest.TestCase):
    def test_matching_tree_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(
                root,
                ["sdv-ship"],
                ["sdv-python-reviewer"],
                {
                    "entries": [
                        entry("sdv-ship", "skill"),
                        entry("sdv-python-reviewer", "agent"),
                    ]
                },
            )
            self.assertEqual(check_catalog.check(root), [])

    def test_skill_on_disk_missing_from_catalog_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(
                root,
                ["sdv-ship", "sdv-port"],
                [],
                {"entries": [entry("sdv-ship", "skill")]},
            )
            problems = check_catalog.check(root)
            self.assertTrue(any("sdv-port" in p for p in problems), problems)

    def test_catalog_row_with_no_directory_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(
                root,
                ["sdv-ship"],
                [],
                {"entries": [entry("sdv-ship", "skill"), entry("sdv-ghost", "skill")]},
            )
            problems = check_catalog.check(root)
            self.assertTrue(any("sdv-ghost" in p for p in problems), problems)

    def test_entry_missing_required_field_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(
                root,
                ["sdv-ship"],
                [],
                {"entries": [{"name": "sdv-ship", "kind": "skill"}]},
            )
            problems = check_catalog.check(root)
            self.assertTrue(any("purpose" in p for p in problems), problems)

    def test_agent_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(root, [], ["sdv-python-reviewer"], {"entries": []})
            problems = check_catalog.check(root)
            self.assertTrue(any("sdv-python-reviewer" in p for p in problems), problems)


GOOD = {
    "plain": "---\nname: s\ndescription: Use when testing.\n---\nbody\n",
    "folded": "---\nname: s\ndescription: >-\n  Phases: (1) one, #2 two\n---\n",
    "quoted": '---\nname: s\ndescription: "Phases: (1) one"\n---\n',
    "nested": "---\nname: s\ndescription: d\nmetadata:\n  author: x\nallowed-tools:\n  - Read\n---\n",
    "url": "---\nname: s\ndescription: see https://example.com/a\n---\n",
    "bom": chr(0xFEFF) + "---\nname: s\ndescription: d\n---\n",
    "comment-line": "---\n# a comment\nname: s\ndescription: d\n---\n",
    "crlf": "---\r\nname: s\r\ndescription: d\r\n---\r\n",
    # block-scalar lines that open with '#' are content, not comments
    "folded-hash-line": "---\nname: s\ndescription: >-\n  #1 rule\n  text\n---\n",
    "literal-heading": "---\nname: s\ndescription: |\n  # Heading\n  text\n---\n",
    "folded-blank-first": "---\nname: s\ndescription: >-\n\n  text\n---\n",
    "multiline-plain": "---\nname: s\ndescription: first line\n  second line\n---\n",
    "quoted-then-comment": '---\nname: s\ndescription: "d" # c\n---\n',
}
# label: (text, needle on the stdlib path, needle on the PyYAML path)
BAD = {
    "colon": (
        "---\nname: s\ndescription: Phases: (1) one\n---\n",
        "unquoted",
        "not valid YAML",
    ),
    "hash": ("---\nname: s\ndescription: Use it #now\n---\n", "' #'", "' #'"),
    "continuation-hash": (
        "---\nname: s\ndescription: first\n  second #x\n---\n",
        "' #'",
        "' #'",
    ),
    "continuation-colon": (
        "---\nname: s\ndescription: first line\n  second: line\n---\n",
        "': '",
        "not valid YAML",
    ),
    "tab-indent": ("---\nname: s\ndescription: a\n\tb\n---\n", "tab", "not valid YAML"),
    "tab-after-colon": (
        "---\nname: s\ndescription:\td\n---\n",
        "space after ':'",
        "not valid YAML",
    ),
    "no-space": (
        "---\nname: s\ndescription:value\n---\n",
        "space after ':'",
        "not valid YAML",
    ),
    "no-fm": ("name: s\n", "does not open", "does not open"),
    "unclosed": ("---\nname: s\ndescription: d\n", "no closing", "no closing"),
    "wrong-name": (
        "---\nname: t\ndescription: d\n---\n",
        "does not match",
        "does not match",
    ),
    "no-desc": ("---\nname: s\n---\n", "no description", "no description"),
}
# YAML errors the stdlib subset misses (documented in _subset_values); PyYAML must catch them.
SUBSET_GAPS = {
    "trailing-colon": "---\nname: s\ndescription: Use when this:\n---\n",
    "star": "---\nname: s\ndescription: *bold* text\n---\n",
    "at": "---\nname: s\ndescription: @user text\n---\n",
    "backtick": "---\nname: s\ndescription: `code` text\n---\n",
    "quoted-then-text": '---\nname: s\ndescription: "a" b\n---\n',
}


def _yaml():
    try:
        import yaml

        return yaml
    except ImportError:
        return None


def _paths():
    """Both code paths: the stdlib subset always, PyYAML when installed (CI)."""
    return [False] + ([True] if _yaml() else [])


def _independent_ok(yaml, name, text):
    """Oracle written apart from check_catalog: a closed --- block that PyYAML
    parses, with the right name and a description, where every plain string value
    reads back whole (a value cut at ' #' reads back shorter than its raw text)."""
    norm = text.lstrip(chr(0xFEFF)).replace("\r\n", "\n")
    if not norm.startswith("---\n") or "\n---" not in norm[3:]:
        return False
    fm = norm[4:].split("\n---", 1)[0]
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError:
        return False
    if not (
        isinstance(data, dict) and data.get("name") == name and data.get("description")
    ):
        return False
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        key, sep, raw = line.partition(": ")
        opener = raw[:1] in ("|", ">", "'", '"', "[", "{")
        top = sep and line[:1] not in (" ", "#", "-")
        if not top or opener or not isinstance(data.get(key), str):
            continue
        # a plain value, maybe continued on indented lines: YAML joins the lines
        # with single spaces, so the parsed value must equal the joined raw text
        parts = [raw.strip()]
        for nxt in lines[i + 1 :]:
            if not nxt.startswith(" "):
                break
            parts.append(nxt.strip())
        if data[key] != " ".join(parts):
            return False
    return True


class FrontmatterTest(unittest.TestCase):
    def test_good_front_matter_passes(self):
        for use_yaml in _paths():
            for label, text in GOOD.items():
                with self.subTest(label, use_yaml=use_yaml):
                    self.assertEqual(
                        check_catalog.frontmatter_problems(
                            "s", text, use_yaml=use_yaml
                        ),
                        [],
                    )

    def test_bad_front_matter_is_named(self):
        for use_yaml in _paths():
            for label, (text, subset_needle, yaml_needle) in BAD.items():
                needle = yaml_needle if use_yaml else subset_needle
                with self.subTest(label, use_yaml=use_yaml):
                    problems = check_catalog.frontmatter_problems(
                        "s", text, use_yaml=use_yaml
                    )
                    self.assertTrue(any(needle in p for p in problems), problems)

    def test_pyyaml_path_rejects_subset_gaps(self):
        if not _yaml():
            self.skipTest("PyYAML not installed")
        for label, text in SUBSET_GAPS.items():
            with self.subTest(label):
                problems = check_catalog.frontmatter_problems("s", text, use_yaml=True)
                self.assertTrue(any("not valid YAML" in p for p in problems), problems)

    def test_check_reports_a_broken_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(root, ["sdv-ship"], [], {"entries": [entry("sdv-ship", "skill")]})
            (root / "skills" / "sdv-ship" / "SKILL.md").write_text(
                "---\nname: sdv-ship\ndescription: Phases: (1) x\n---\n",
                encoding="utf-8",
            )
            problems = check_catalog.check(root)
            self.assertTrue(
                any(p.startswith("skill 'sdv-ship':") for p in problems), problems
            )

    def test_check_reports_a_broken_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            build(
                root,
                [],
                ["sdv-r-reviewer"],
                {"entries": [entry("sdv-r-reviewer", "agent")]},
            )
            (root / "agents" / "sdv-r-reviewer.md").write_text(
                "---\nname: sdv-r-reviewer\ndescription: Lenses: roxygen\n---\n",
                encoding="utf-8",
            )
            problems = check_catalog.check(root)
            self.assertTrue(
                any(p.startswith("agent 'sdv-r-reviewer':") for p in problems), problems
            )

    def test_both_paths_agree_with_independent_oracle(self):
        """Both paths reach the oracle's verdict on every GOOD/BAD case and every real
        skill and agent, so a bare-python run (release.py) matches CI. CI installs
        PyYAML, so this is not skipped there."""
        yaml = _yaml()
        if not yaml:
            self.skipTest("PyYAML not installed")
        root = pathlib.Path(__file__).resolve().parent.parent
        real = {
            f.parent.name: f.read_text(encoding="utf-8")
            for f in root.glob("skills/*/SKILL.md")
        }
        real.update(
            {f.stem: f.read_text(encoding="utf-8") for f in root.glob("agents/*.md")}
        )
        self.assertGreaterEqual(len(real), 35)
        cases = [("s", t) for t in GOOD.values()] + [("s", v[0]) for v in BAD.values()]
        for name, text in cases + list(real.items()):
            want = _independent_ok(yaml, name, text)
            for use_yaml in (False, True):
                with self.subTest(name, use_yaml=use_yaml, text=text[:40]):
                    got = (
                        check_catalog.frontmatter_problems(
                            name, text, use_yaml=use_yaml
                        )
                        == []
                    )
                    self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
