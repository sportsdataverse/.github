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
            "---\nname: %s\n---\n" % name, encoding="utf-8"
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
}
BAD = {
    "colon": ("---\nname: s\ndescription: Phases: (1) one\n---\n", "unquoted"),
    "hash": ("---\nname: s\ndescription: Use it #now\n---\n", "' #'"),
    "no-fm": ("name: s\n", "does not open"),
    "unclosed": ("---\nname: s\ndescription: d\n", "no closing"),
    "wrong-name": ("---\nname: t\ndescription: d\n---\n", "does not match"),
    "no-desc": ("---\nname: s\n---\n", "no description"),
}


class FrontmatterTest(unittest.TestCase):
    def test_good_front_matter_passes(self):
        for label, text in GOOD.items():
            with self.subTest(label):
                self.assertEqual(check_catalog.frontmatter_problems("s", text), [])

    def test_bad_front_matter_is_named(self):
        for label, (text, needle) in BAD.items():
            with self.subTest(label):
                problems = check_catalog.frontmatter_problems("s", text)
                self.assertTrue(any(needle in p for p in problems), problems)

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
                any("sdv-ship" in p and "unquoted" in p for p in problems), problems
            )

    def test_agrees_with_pyyaml(self):
        """Oracle: the subset check and a real YAML parser agree on every case and
        every real skill. CI installs PyYAML so this runs there, not skipped."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        skills = pathlib.Path(__file__).resolve().parent.parent / "skills"
        real = {
            f.parent.name: f.read_text(encoding="utf-8")
            for f in skills.glob("*/SKILL.md")
        }
        self.assertGreater(len(real), 0)
        cases = [("s", t) for t in GOOD.values()] + [("s", BAD["colon"][0])]
        for name, text in cases + list(real.items()):
            with self.subTest(name):
                try:
                    fm = text.split("\n---", 1)[0][4:]
                    d = yaml.safe_load(fm)
                    yaml_ok = (
                        isinstance(d, dict)
                        and d.get("name") == name
                        and bool(d.get("description"))
                        # a ' #' in a plain value parses, but YAML drops the rest
                        # as a comment: a silently truncated description is not ok
                        and fm.count("#") == yaml.safe_dump(d).count("#")
                    )
                except yaml.YAMLError:
                    yaml_ok = False
                ours_ok = check_catalog.frontmatter_problems(name, text) == []
                self.assertEqual(ours_ok, yaml_ok)


if __name__ == "__main__":
    unittest.main()
