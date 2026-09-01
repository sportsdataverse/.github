"""Unit tests for render_reports_explainers.py (offline; git calls stubbed)."""

import subprocess

import render_reports_explainers as rre


def _fake_git(monkeypatch, date="2026-09-01"):
    def fake_run(cmd, **kw):
        class P:
            returncode = 0
            stdout = date + "\n"

        return P()

    monkeypatch.setattr(subprocess, "run", fake_run)


def test_empty_repo_renders_none_yet(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    block = rre.render(tmp_path)
    assert rre.BEGIN in block and rre.END in block
    assert "_none yet_" in block


def test_dir_family_collapses_to_one_row(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    d = tmp_path / "docs" / "datasets"
    d.mkdir(parents=True)
    for n in ("pbp", "schedule", "rosters"):
        (d / f"{n}.md").write_text(f"# {n}\n", encoding="utf-8")
    block = rre.render(tmp_path)
    assert block.count("docs/datasets/") == 1
    assert "3 files" in block
    assert "_none yet_" not in block


def test_top_level_docs_itemized_with_own_heading(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    d = tmp_path / "docs"
    d.mkdir()
    (d / "SCRAPING_NOTES.md").write_text("# Scraping notes\n\nbody\n", encoding="utf-8")
    block = rre.render(tmp_path)
    assert "[Scraping notes](docs/SCRAPING_NOTES.md)" in block


def test_registry_row_present(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    m = tmp_path / "models"
    m.mkdir()
    (m / "REGISTRY.md").write_text("# registry\n", encoding="utf-8")
    block = rre.render(tmp_path)
    assert "[Model registry](models/REGISTRY.md)" in block


def test_untracked_file_labelled_uncommitted(tmp_path, monkeypatch):
    def fake_run(cmd, **kw):
        class P:
            returncode = 0
            stdout = ""  # git log prints nothing for an untracked path

        return P()

    monkeypatch.setattr(subprocess, "run", fake_run)
    d = tmp_path / "docs"
    d.mkdir()
    (d / "note.md").write_text("# Note\n", encoding="utf-8")
    assert "uncommitted" in rre.render(tmp_path)


def test_write_replaces_only_between_markers(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    readme = tmp_path / "README.md"
    readme.write_text(
        f"# repo\n\n## Reports & explainers\n\n{rre.BEGIN}\nstale\n{rre.END}\n\n## After\nkeep me\n",
        encoding="utf-8",
    )
    rc = rre.main(["--repo-root", str(tmp_path), "--readme", str(readme), "--write"])
    assert rc == 0
    text = readme.read_text(encoding="utf-8")
    assert "stale" not in text
    assert "keep me" in text
    assert "_none yet_" in text


def test_write_refuses_without_markers(tmp_path, monkeypatch, capsys):
    _fake_git(monkeypatch)
    readme = tmp_path / "README.md"
    readme.write_text("# repo\n", encoding="utf-8")
    rc = rre.main(["--repo-root", str(tmp_path), "--readme", str(readme), "--write"])
    assert rc == 1
    assert "add them first" in capsys.readouterr().err


def test_check_passes_on_rendered_block_and_fails_without_markers(tmp_path, monkeypatch):
    _fake_git(monkeypatch)
    readme = tmp_path / "README.md"
    readme.write_text(f"{rre.BEGIN}\nx\n{rre.END}\n", encoding="utf-8")
    rc = rre.main(["--repo-root", str(tmp_path), "--readme", str(readme), "--write"])
    assert rc == 0
    assert rre.main(["--readme", str(readme), "--check"]) == 0
    bare = tmp_path / "bare.md"
    bare.write_text("# no markers\n", encoding="utf-8")
    assert rre.main(["--readme", str(bare), "--check"]) == 1


def test_check_rejects_block_without_table_header(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(f"{rre.BEGIN}\n| arbitrary |\n{rre.END}\n", encoding="utf-8")
    assert rre.main(["--readme", str(readme), "--check"]) == 1
