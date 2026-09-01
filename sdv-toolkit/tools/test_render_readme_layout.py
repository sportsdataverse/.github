"""Tests for render_readme_layout.py."""

from __future__ import annotations

from pathlib import Path

import pytest
from render_readme_layout import (
    MAX_CHILDREN_DATA,
    BEGIN,
    END,
    committed_block,
    main,
    render,
    tree_lines,
)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "hoopR-nba-raw"
    (root / "python").mkdir(parents=True)
    (root / "python" / "espn_nba_01_schedules_scrape.py").write_text("x")
    (root / "python" / "espn_nba_02_pbp_scrape.py").write_text("x")
    (root / "scripts").mkdir()
    (root / "scripts" / "daily_nba_scraper.sh").write_text("x")
    (root / "nba" / "raw").mkdir(parents=True)
    (root / "nba" / "schedules").mkdir()
    (root / "tests").mkdir()
    return root


def test_root_line_names_the_repo(repo: Path) -> None:
    assert tree_lines(repo)[0] == "hoopR-nba-raw/"


def test_top_level_dirs_are_listed_and_sorted(repo: Path) -> None:
    tops = [ln for ln in tree_lines(repo) if ln.startswith(("├── ", "└── "))]
    names = [ln.split("── ")[1].split("/")[0] for ln in tops]
    assert names == sorted(names)
    assert {"python", "scripts", "nba", "tests"} <= set(names)


def test_last_top_level_uses_the_corner_elbow(repo: Path) -> None:
    tops = [ln for ln in tree_lines(repo) if ln.startswith(("├── ", "└── "))]
    assert tops[-1].startswith("└── ")


def test_code_dirs_list_their_stage_files(repo: Path) -> None:
    out = "\n".join(tree_lines(repo))
    assert "espn_nba_01_schedules_scrape.py" in out
    assert "daily_nba_scraper.sh" in out


def test_data_dirs_list_subdirs_not_files(repo: Path) -> None:
    (repo / "nba" / "raw" / "401.json").write_text("{}")
    out = "\n".join(tree_lines(repo))
    assert "raw/" in out and "schedules/" in out
    assert "401.json" not in out


def test_glossary_annotates_known_directories(repo: Path) -> None:
    out = "\n".join(tree_lines(repo))
    assert "# Python pipeline stages, numbered in build order" in out


def test_children_beyond_the_cap_are_summarised(repo: Path) -> None:
    for i in range(20):
        (repo / "nba" / f"season_{2000 + i}").mkdir()
    out = "\n".join(tree_lines(repo))
    assert "… " in out and " more" in out
    assert out.count("season_") <= MAX_CHILDREN_DATA


def test_a_single_extra_entry_is_shown_not_elided(repo: Path) -> None:
    """ "… 1 more" costs the same line as the entry and tells the reader less."""
    for i in range(MAX_CHILDREN_DATA + 1 - 2):  # fixture already has raw/ + schedules/
        (repo / "nba" / f"extra_{i:02d}").mkdir()
    out = "\n".join(tree_lines(repo))
    assert "… 1 more" not in out
    assert f"extra_{MAX_CHILDREN_DATA - 3:02d}" in out


def test_code_dirs_get_the_larger_budget(repo: Path) -> None:
    for i in range(3, MAX_CHILDREN_DATA + 4):
        (repo / "python" / f"espn_nba_{i:02d}_stage.py").write_text("x")
    out = "\n".join(tree_lines(repo))
    # more than the data cap survives, because stage scripts are the point
    assert out.count("espn_nba_") > MAX_CHILDREN_DATA


def test_tooling_caches_are_skipped(repo: Path) -> None:
    (repo / "__pycache__").mkdir()
    (repo / ".venv").mkdir()
    (repo / "python" / "__pycache__").mkdir()
    out = "\n".join(tree_lines(repo))
    assert "__pycache__" not in out
    assert ".venv" not in out


def test_hidden_directories_are_skipped(repo: Path) -> None:
    (repo / ".github").mkdir()
    assert ".github" not in "\n".join(tree_lines(repo))


def test_render_is_fenced_and_marker_wrapped(repo: Path) -> None:
    block = render(repo)
    assert block.startswith(BEGIN) and block.endswith(END)
    assert block.count("```") == 2


def test_render_is_deterministic(repo: Path) -> None:
    assert render(repo) == render(repo)


def test_committed_block_returns_none_without_markers() -> None:
    assert committed_block("# readme\n\nno markers here\n") is None


def test_write_replaces_only_the_block(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text(f"# title\n\nkeep me\n\n{BEGIN}\nstale\n{END}\n\ntrailing\n")
    assert main(["--repo-root", str(repo), "--readme", str(readme), "--write"]) == 0
    text = readme.read_text()
    assert "keep me" in text and "trailing" in text
    assert "stale" not in text
    assert "hoopR-nba-raw/" in text


def test_write_refuses_when_markers_are_absent(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text("# title\n\nno markers\n")
    assert main(["--repo-root", str(repo), "--readme", str(readme), "--write"]) == 1
    assert "no markers" in readme.read_text()


def test_check_passes_on_a_rendered_readme(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text(f"# title\n\n{BEGIN}\nx\n{END}\n")
    main(["--repo-root", str(repo), "--readme", str(readme), "--write"])
    assert main(["--readme", str(readme), "--check"]) == 0


def test_check_fails_without_markers(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text("# title\n")
    assert main(["--readme", str(readme), "--check"]) == 1


def test_check_fails_when_the_fence_is_missing(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text(f"{BEGIN}\nno fence\n{END}\n")
    assert main(["--readme", str(readme), "--check"]) == 1


def test_check_does_not_compare_contents(repo: Path) -> None:
    """A sparse checkout omits directories; that must not redden the gate."""
    readme = repo / "README.md"
    readme.write_text(f"{BEGIN}\n\n```\nsomething-else/\n```\n\n{END}\n")
    assert main(["--readme", str(readme), "--check"]) == 0


def test_check_without_readme_is_a_usage_error(repo: Path) -> None:
    assert main(["--repo-root", str(repo), "--check"]) == 2


def test_write_refuses_an_empty_tree(tmp_path: Path) -> None:
    """A sparse checkout shows no directories; that must not commit as fact."""
    bare = tmp_path / "amf-location-data"
    bare.mkdir()
    (bare / "check_data.py").write_text("x")  # files only, no directories
    readme = bare / "README.md"
    readme.write_text(f"# t\n\n{BEGIN}\nreal content\n{END}\n")
    assert main(["--repo-root", str(bare), "--readme", str(readme), "--write"]) == 1
    assert "real content" in readme.read_text()  # prior block preserved


def test_stdout_still_prints_an_empty_tree(tmp_path: Path, capsys) -> None:
    bare = tmp_path / "empty-repo"
    bare.mkdir()
    assert main(["--repo-root", str(bare)]) == 0
    assert "empty-repo/" in capsys.readouterr().out


def test_crlf_readme_keeps_its_line_endings(repo: Path) -> None:
    """A one-section edit must not rewrite every line of a CRLF file."""
    readme = repo / "README.md"
    readme.write_bytes(f"# t\r\n\r\nkeep\r\n\r\n{BEGIN}\r\nold\r\n{END}\r\n".encode())
    assert main(["--repo-root", str(repo), "--readme", str(readme), "--write"]) == 0
    raw = readme.read_bytes()
    assert b"\r\n" in raw
    assert b"keep\r\n" in raw
    # no bare LF outside the CRLF pairs
    assert raw.replace(b"\r\n", b"") .count(b"\n") == 0


def test_lf_readme_stays_lf(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_bytes(f"# t\n\nkeep\n\n{BEGIN}\nold\n{END}\n".encode())
    assert main(["--repo-root", str(repo), "--readme", str(readme), "--write"]) == 0
    assert b"\r\n" not in readme.read_bytes()
