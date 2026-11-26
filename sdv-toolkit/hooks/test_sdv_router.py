"""Tests for sdv_router. Run: python -m unittest discover -s hooks -p 'test_*.py'"""

import pathlib
import shutil
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

    def test_card_carries_the_facts_line(self):
        card = sdv_router.render_card("sdv-py", "sportsdataverse-py", CATALOG, {})
        self.assertIn(sdv_router.FACTS_LINE, card)
        self.assertNotIn("DEGRADED", card)

    def test_degraded_line_when_docs_mcp_cannot_start(self):
        card = sdv_router.render_card(
            "r-package", "cfbfastR", CATALOG, {}, "uvx is not on PATH"
        )
        self.assertIn("DEGRADED: sdv-docs cannot start (uvx is not on PATH)", card)
        self.assertIn("[unverified: from memory]", card)


class DocsMcpProbeTest(unittest.TestCase):
    def write(self, root, servers):
        (root / ".mcp.json").write_text(
            '{"mcpServers": %s}' % servers, encoding="utf-8"
        )

    def test_missing_launcher_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write(
                root,
                '{"sdv-docs": {"type": "stdio", "command": "no-such-launcher-xyz"}}',
            )
            self.assertEqual(
                sdv_router.docs_mcp_problem(root), "no-such-launcher-xyz is not on PATH"
            )

    @unittest.skipUnless(shutil.which("git"), "git not on PATH")
    def test_launcher_on_path_is_healthy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write(root, '{"sdv-docs": {"type": "stdio", "command": "git"}}')
            self.assertIsNone(sdv_router.docs_mcp_problem(root))

    def test_missing_entry_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write(root, '{"context7": {"type": "http", "url": "x"}}')
            self.assertEqual(
                sdv_router.docs_mcp_problem(root), "no sdv-docs entry in .mcp.json"
            )

    def test_shipped_config_names_sdv_docs(self):
        # the real plugin config must still have the entry the probe looks for
        root = pathlib.Path(sdv_router.__file__).resolve().parent.parent
        self.assertNotIn(
            sdv_router.docs_mcp_problem(root),
            {".mcp.json is unreadable", "no sdv-docs entry in .mcp.json"},
        )


class BoundedTest(unittest.TestCase):
    def test_card_is_bounded(self):
        card = sdv_router.render_card(
            "data", "nfl-data", CATALOG, {}, "uvx is not on PATH"
        )
        self.assertLessEqual(
            len(card.splitlines()), 30, "router card must stay ~25 lines"
        )


if __name__ == "__main__":
    unittest.main()
