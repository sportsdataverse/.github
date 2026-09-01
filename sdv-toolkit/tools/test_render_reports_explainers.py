"""Unit tests for render_reports_explainers.py (offline; git calls stubbed).

Stdlib ``unittest`` on purpose: the catalog workflow runs ``python -m unittest``,
which collects only TestCase subclasses. These nine tests previously used
pytest-style bare functions with ``tmp_path``/``monkeypatch``/``capsys``, so
discovery skipped them silently and the job's green never covered this renderer
-- the one rolled out to 29 repos.
"""

import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

import render_reports_explainers as rre


class _FakeProc:
    def __init__(self, stdout: str) -> None:
        self.returncode = 0
        self.stdout = stdout


class ReportsExplainersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._real_run = subprocess.run
        self.fake_git()

    def tearDown(self) -> None:
        subprocess.run = self._real_run
        self._tmp.cleanup()

    def fake_git(self, date: str = "2026-09-01") -> None:
        """Stub subprocess.run so no test shells out to git."""
        stdout = f"{date}\n" if date else ""
        subprocess.run = lambda cmd, **kw: _FakeProc(stdout)  # type: ignore[assignment]

    def test_empty_repo_renders_none_yet(self) -> None:
        block = rre.render(self.root)
        self.assertIn(rre.BEGIN, block)
        self.assertIn(rre.END, block)
        self.assertIn("_none yet_", block)

    def test_dir_family_collapses_to_one_row(self) -> None:
        d = self.root / "docs" / "datasets"
        d.mkdir(parents=True)
        for n in ("pbp", "schedule", "rosters"):
            (d / f"{n}.md").write_text(f"# {n}\n", encoding="utf-8")
        block = rre.render(self.root)
        self.assertEqual(block.count("docs/datasets/"), 1)
        self.assertIn("3 files", block)
        self.assertNotIn("_none yet_", block)

    def test_top_level_docs_itemized_with_own_heading(self) -> None:
        d = self.root / "docs"
        d.mkdir()
        (d / "SCRAPING_NOTES.md").write_text(
            "# Scraping notes\n\nbody\n", encoding="utf-8"
        )
        self.assertIn("[Scraping notes](docs/SCRAPING_NOTES.md)", rre.render(self.root))

    def test_registry_row_present(self) -> None:
        m = self.root / "models"
        m.mkdir()
        (m / "REGISTRY.md").write_text("# registry\n", encoding="utf-8")
        self.assertIn("[Model registry](models/REGISTRY.md)", rre.render(self.root))

    def test_untracked_file_labelled_uncommitted(self) -> None:
        self.fake_git(date="")  # git log prints nothing for an untracked path
        d = self.root / "docs"
        d.mkdir()
        (d / "note.md").write_text("# Note\n", encoding="utf-8")
        self.assertIn("uncommitted", rre.render(self.root))

    def test_write_replaces_only_between_markers(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            f"# repo\n\n## Reports & explainers\n\n{rre.BEGIN}\nstale\n{rre.END}\n\n"
            "## After\nkeep me\n",
            encoding="utf-8",
        )
        rc = rre.main(
            ["--repo-root", str(self.root), "--readme", str(readme), "--write"]
        )
        self.assertEqual(rc, 0)
        text = readme.read_text(encoding="utf-8")
        self.assertNotIn("stale", text)
        self.assertIn("keep me", text)
        self.assertIn("_none yet_", text)

    def test_write_refuses_without_markers(self) -> None:
        readme = self.root / "README.md"
        readme.write_text("# repo\n", encoding="utf-8")
        err = io.StringIO()
        with redirect_stderr(err):
            rc = rre.main(
                ["--repo-root", str(self.root), "--readme", str(readme), "--write"]
            )
        self.assertEqual(rc, 1)
        self.assertIn("add them first", err.getvalue())

    def test_check_passes_on_rendered_block_and_fails_without_markers(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(f"{rre.BEGIN}\nx\n{rre.END}\n", encoding="utf-8")
        rc = rre.main(
            ["--repo-root", str(self.root), "--readme", str(readme), "--write"]
        )
        self.assertEqual(rc, 0)
        self.assertEqual(rre.main(["--readme", str(readme), "--check"]), 0)
        bare = self.root / "bare.md"
        bare.write_text("# no markers\n", encoding="utf-8")
        with redirect_stderr(io.StringIO()):
            self.assertEqual(rre.main(["--readme", str(bare), "--check"]), 1)

    def test_check_rejects_block_without_table_header(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(f"{rre.BEGIN}\n| arbitrary |\n{rre.END}\n", encoding="utf-8")
        with redirect_stderr(io.StringIO()):
            self.assertEqual(rre.main(["--readme", str(readme), "--check"]), 1)


if __name__ == "__main__":
    unittest.main()
