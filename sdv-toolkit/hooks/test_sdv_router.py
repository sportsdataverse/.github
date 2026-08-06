"""Tests for sdv_router. Run: python -m unittest discover -s hooks -p 'test_*.py'"""

import pathlib
import tempfile
import unittest

import sdv_router

CATALOG = {
    "entries": [
        {
            "name": "sdv-data-pipeline",
            "kind": "skill",
            "purpose": "build",
            "archetypes": ["raw", "data"],
        },
        {
            "name": "sdv-ship",
            "kind": "skill",
            "purpose": "land",
            "archetypes": ["sdv-py", "raw", "data", "r-package"],
        },
        {
            "name": "sdv-python-reviewer",
            "kind": "agent",
            "purpose": "review",
            "archetypes": ["sdv-py", "data"],
        },
    ]
}


class DetectTest(unittest.TestCase):
    def test_codegen_marker_means_sdv_py(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "tools" / "codegen").mkdir(parents=True)
            (root / "tools" / "codegen" / "generate.py").write_text(
                "", encoding="utf-8"
            )
            self.assertEqual(
                sdv_router.detect(
                    root, "https://github.com/sportsdataverse/sportsdataverse-py.git"
                ),
                "sdv-py",
            )

    def test_raw_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                sdv_router.detect(
                    pathlib.Path(tmp), "https://github.com/sportsdataverse/cfb-raw.git"
                ),
                "raw",
            )

    def test_data_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                sdv_router.detect(
                    pathlib.Path(tmp), "https://github.com/sportsdataverse/nfl-data.git"
                ),
                "data",
            )

    def test_r_package_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "R").mkdir()
            (root / "DESCRIPTION").write_text("Package: cfbfastR\n", encoding="utf-8")
            self.assertEqual(
                sdv_router.detect(
                    root, "https://github.com/sportsdataverse/cfbfastR.git"
                ),
                "r-package",
            )

    def test_non_sdv_repo_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(
                sdv_router.detect(
                    pathlib.Path(tmp), "https://github.com/someone/unrelated.git"
                )
            )

    def test_no_remote_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(sdv_router.detect(pathlib.Path(tmp), ""))


class RenderTest(unittest.TestCase):
    def test_card_lists_only_matching_archetype(self):
        card = sdv_router.render_card("data", "nfl-data", CATALOG, {})
        self.assertIn("sdv-data-pipeline", card)
        self.assertIn("sdv-ship", card)
        self.assertIn("archetype: data", card)

    def test_card_excludes_other_archetypes(self):
        card = sdv_router.render_card("r-package", "cfbfastR", CATALOG, {})
        self.assertNotIn("sdv-data-pipeline", card)

    def test_override_line_is_appended(self):
        card = sdv_router.render_card(
            "data",
            "hoopR-data",
            CATALOG,
            {"hoopR-data": "ARCHIVE - read-only; do not build here"},
        )
        self.assertIn("ARCHIVE", card)

    def test_card_is_bounded(self):
        card = sdv_router.render_card("data", "nfl-data", CATALOG, {})
        self.assertLessEqual(
            len(card.splitlines()), 30, "router card must stay ~25 lines"
        )


if __name__ == "__main__":
    unittest.main()
