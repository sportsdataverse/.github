"""Unit tests for render_readme_layout.py.

Stdlib ``unittest`` on purpose: the catalog workflow runs ``python -m unittest``,
which collects only TestCase subclasses. A pytest-style module here is either
never executed (bare function tests are skipped silently) or, if it imports
pytest, breaks collection outright and reddens the job.
"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from render_readme_layout import (
    BEGIN,
    END,
    MAX_CHILDREN_DATA,
    committed_block,
    main,
    render,
    tree_lines,
)


class LayoutTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "hoopR-nba-raw"
        (self.repo / "python").mkdir(parents=True)
        (self.repo / "python" / "espn_nba_01_schedules_scrape.py").write_text("x")
        (self.repo / "python" / "espn_nba_02_pbp_scrape.py").write_text("x")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts" / "daily_nba_scraper.sh").write_text("x")
        (self.repo / "nba" / "raw").mkdir(parents=True)
        (self.repo / "nba" / "schedules").mkdir()
        (self.repo / "tests").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def out(self) -> str:
        return "\n".join(tree_lines(self.repo))

    def tops(self) -> list[str]:
        return [ln for ln in tree_lines(self.repo) if ln.startswith(("├── ", "└── "))]

    # --- tree shape ---------------------------------------------------------

    def test_root_line_names_the_repo(self) -> None:
        self.assertEqual(tree_lines(self.repo)[0], "hoopR-nba-raw/")

    def test_top_level_dirs_are_listed_and_sorted(self) -> None:
        names = [ln.split("── ")[1].split("/")[0] for ln in self.tops()]
        self.assertEqual(names, sorted(names))
        self.assertLessEqual({"python", "scripts", "nba", "tests"}, set(names))

    def test_last_top_level_uses_the_corner_elbow(self) -> None:
        self.assertTrue(self.tops()[-1].startswith("└── "))

    def test_code_dirs_list_their_stage_files(self) -> None:
        self.assertIn("espn_nba_01_schedules_scrape.py", self.out())
        self.assertIn("daily_nba_scraper.sh", self.out())

    def test_data_dirs_list_subdirs_not_files(self) -> None:
        (self.repo / "nba" / "raw" / "401.json").write_text("{}")
        out = self.out()
        self.assertIn("raw/", out)
        self.assertIn("schedules/", out)
        self.assertNotIn("401.json", out)

    def test_glossary_annotates_known_directories(self) -> None:
        self.assertIn("# Python pipeline stages, numbered in build order", self.out())

    # --- capping ------------------------------------------------------------

    def test_children_beyond_the_cap_are_summarised(self) -> None:
        for i in range(20):
            (self.repo / "nba" / f"season_{2000 + i}").mkdir()
        out = self.out()
        self.assertIn(" more", out)
        self.assertLessEqual(out.count("season_"), MAX_CHILDREN_DATA)

    def test_a_single_extra_entry_is_shown_not_elided(self) -> None:
        for i in range(MAX_CHILDREN_DATA + 1 - 2):  # fixture has raw/ + schedules/
            (self.repo / "nba" / f"extra_{i:02d}").mkdir()
        self.assertNotIn("… 1 more", self.out())

    def test_code_dirs_get_the_larger_budget(self) -> None:
        for i in range(3, MAX_CHILDREN_DATA + 4):
            (self.repo / "python" / f"espn_nba_{i:02d}_stage.py").write_text("x")
        self.assertGreater(self.out().count("espn_nba_"), MAX_CHILDREN_DATA)

    # --- exclusions ---------------------------------------------------------

    def test_tooling_caches_are_skipped(self) -> None:
        (self.repo / "__pycache__").mkdir()
        (self.repo / ".venv").mkdir()
        (self.repo / "python" / "__pycache__").mkdir()
        out = self.out()
        self.assertNotIn("__pycache__", out)
        self.assertNotIn(".venv", out)

    def test_hidden_directories_are_skipped(self) -> None:
        (self.repo / ".github").mkdir()
        self.assertNotIn(".github", self.out())

    # --- block rendering ----------------------------------------------------

    def test_render_is_fenced_and_marker_wrapped(self) -> None:
        block = render(self.repo)
        self.assertTrue(block.startswith(BEGIN))
        self.assertTrue(block.endswith(END))
        self.assertEqual(block.count("```"), 2)

    def test_render_is_deterministic(self) -> None:
        self.assertEqual(render(self.repo), render(self.repo))

    def test_committed_block_returns_none_without_markers(self) -> None:
        self.assertIsNone(committed_block("# readme\n\nno markers\n"))

    # --- write path ---------------------------------------------------------

    def test_write_replaces_only_the_block(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text(f"# t\n\nkeep me\n\n{BEGIN}\nstale\n{END}\n\ntrailing\n")
        self.assertEqual(
            main(["--repo-root", str(self.repo), "--readme", str(readme), "--write"]), 0
        )
        text = readme.read_text()
        self.assertIn("keep me", text)
        self.assertIn("trailing", text)
        self.assertNotIn("stale", text)
        self.assertIn("hoopR-nba-raw/", text)

    def test_write_refuses_when_markers_are_absent(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text("# t\n\nno markers\n")
        self.assertEqual(
            main(["--repo-root", str(self.repo), "--readme", str(readme), "--write"]), 1
        )
        self.assertIn("no markers", readme.read_text())

    def test_write_refuses_an_empty_tree(self) -> None:
        """A sparse checkout shows no directories; that must not commit as fact."""
        with tempfile.TemporaryDirectory() as td:
            bare = Path(td) / "amf-location-data"
            bare.mkdir()
            (bare / "check_data.py").write_text("x")
            readme = bare / "README.md"
            readme.write_text(f"# t\n\n{BEGIN}\nreal content\n{END}\n")
            self.assertEqual(
                main(["--repo-root", str(bare), "--readme", str(readme), "--write"]), 1
            )
            self.assertIn("real content", readme.read_text())

    def test_stdout_still_prints_an_empty_tree(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bare = Path(td) / "empty-repo"
            bare.mkdir()
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(main(["--repo-root", str(bare)]), 0)
            self.assertIn("empty-repo/", buf.getvalue())

    # --- line endings -------------------------------------------------------

    def test_crlf_readme_keeps_its_line_endings(self) -> None:
        readme = self.repo / "README.md"
        readme.write_bytes(
            f"# t\r\n\r\nkeep\r\n\r\n{BEGIN}\r\nold\r\n{END}\r\n".encode()
        )
        self.assertEqual(
            main(["--repo-root", str(self.repo), "--readme", str(readme), "--write"]), 0
        )
        raw = readme.read_bytes()
        self.assertIn(b"keep\r\n", raw)
        self.assertEqual(raw.replace(b"\r\n", b"").count(b"\n"), 0)

    def test_lf_readme_stays_lf(self) -> None:
        readme = self.repo / "README.md"
        readme.write_bytes(f"# t\n\nkeep\n\n{BEGIN}\nold\n{END}\n".encode())
        self.assertEqual(
            main(["--repo-root", str(self.repo), "--readme", str(readme), "--write"]), 0
        )
        self.assertNotIn(b"\r\n", readme.read_bytes())

    # --- check path ---------------------------------------------------------

    def test_check_passes_on_a_rendered_readme(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text(f"# t\n\n{BEGIN}\nx\n{END}\n")
        main(["--repo-root", str(self.repo), "--readme", str(readme), "--write"])
        self.assertEqual(main(["--readme", str(readme), "--check"]), 0)

    def test_check_fails_without_markers(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text("# t\n")
        self.assertEqual(main(["--readme", str(readme), "--check"]), 1)

    def test_check_fails_when_the_fence_is_missing(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text(f"{BEGIN}\nno fence\n{END}\n")
        self.assertEqual(main(["--readme", str(readme), "--check"]), 1)

    def test_check_does_not_compare_contents(self) -> None:
        """A sparse checkout omits directories; that must not redden the gate."""
        readme = self.repo / "README.md"
        readme.write_text(f"{BEGIN}\n\n```\nsomething-else/\n```\n\n{END}\n")
        self.assertEqual(main(["--readme", str(readme), "--check"]), 0)

    def test_check_without_readme_is_a_usage_error(self) -> None:
        self.assertEqual(main(["--repo-root", str(self.repo), "--check"]), 2)


if __name__ == "__main__":
    unittest.main()
