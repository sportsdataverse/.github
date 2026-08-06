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
        (d / "SKILL.md").write_text("---\nname: %s\n---\n" % name, encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
