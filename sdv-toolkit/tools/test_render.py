"""Tests for render. Run: python -m unittest discover -s tools -p 'test_*.py'"""

import unittest

import render

CATALOG = {
    "version": "0.4.0",
    "entries": [
        {
            "name": "sdv-ship",
            "kind": "skill",
            "purpose": "Land a change.",
            "archetypes": ["sdv-py"],
        },
        {
            "name": "sdv-port",
            "kind": "skill",
            "purpose": "Port between languages.",
            "archetypes": ["sdv-py"],
        },
        {
            "name": "sdv-python-reviewer",
            "kind": "agent",
            "purpose": "Python review by lens.",
            "archetypes": ["sdv-py"],
        },
    ],
}


class RenderTest(unittest.TestCase):
    def test_readme_lists_every_entry(self):
        out = render.render_readme(CATALOG)
        for name in ("sdv-ship", "sdv-port", "sdv-python-reviewer"):
            self.assertIn(name, out)

    def test_readme_separates_skills_from_agents(self):
        out = render.render_readme(CATALOG)
        self.assertIn("## Skills", out)
        self.assertIn("## Agents", out)

    def test_plugin_description_reports_true_counts(self):
        out = render.render_plugin_description(CATALOG)
        self.assertIn("2 skills", out)
        self.assertIn("1 agent", out)

    def test_marketplace_description_is_bounded(self):
        out = render.render_marketplace_description(CATALOG)
        self.assertLessEqual(len(out), 400)

    def test_counts_track_the_catalog(self):
        smaller = {"version": "0.4.0", "entries": CATALOG["entries"][:1]}
        self.assertIn("1 skill", render.render_plugin_description(smaller))

    def test_readme_escapes_pipe_in_purpose(self):
        catalog = {
            "version": "0.4.0",
            "entries": [
                {
                    "name": "sdv-pipey",
                    "kind": "agent",
                    "purpose": "Review by lens: polars | http | docstring.",
                    "archetypes": ["sdv-py"],
                }
            ],
        }
        out = render.render_readme(catalog)
        row = next(line for line in out.splitlines() if "sdv-pipey" in line)
        self.assertIn("polars \\| http \\| docstring.", row)
        # exactly two data cells: leading/trailing "|" plus one separator "|"
        self.assertEqual(row.count("|") - row.count("\\|"), 3)


if __name__ == "__main__":
    unittest.main()
