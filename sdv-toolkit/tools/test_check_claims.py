"""Tests for check_claims. Run: python -m unittest discover -s tools -p 'test_*.py'

Each red fixture is a real excerpt (see check_claims_data/fixtures/README.md).
"""

import contextlib
import io
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import check_claims

FIXTURES = pathlib.Path(__file__).resolve().parent / "check_claims_data" / "fixtures"
HAS_GIT = shutil.which("git") is not None


def run(repo, *extra):
    """Findings for a repo, offline (no Rscript dependency lookup)."""
    ns = check_claims.parser().parse_args(["--repo", str(repo), "--no-r-deps", *extra])
    return check_claims.run(ns)


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        env={
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
            "PATH": __import__("os").environ.get("PATH", ""),
            "HOME": tempfile.gettempdir(),
            "GIT_CONFIG_NOSYSTEM": "1",
        },
    )


def copy_fixture(name, dest):
    shutil.copytree(FIXTURES / name, dest, dirs_exist_ok=True)


class T1RegisterCfbd(unittest.TestCase):
    """cfbfastR R/cfbd_api_key.R:8 told users to call a function nothing defines."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("cfbfastR", self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_flags_the_missing_function(self):
        got = [f for f in run(self.repo, "--checks", "T1") if f.check == "T1"]
        self.assertEqual(
            [(f.path, f.line, f.token) for f in got],
            [("R/cfbd_api_key.R", 8, "register_cfbd()")],
        )

    def test_exported_neighbours_resolve(self):
        # negative case: lines 7, 9, 10 name exported functions and must stay quiet
        lines = {f.line for f in run(self.repo, "--checks", "T1")}
        self.assertFalse(lines & {7, 9, 10}, lines)

    def test_strict_exits_1_and_default_exits_0(self):
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            base = ["--repo", str(self.repo), "--no-r-deps", "--checks", "T1"]
            self.assertEqual(check_claims.main(base), 0)
            self.assertEqual(check_claims.main(base + ["--strict"]), 1)


class NeverBlocks(unittest.TestCase):
    """Report-only: exit 0 on an internal error and on bad usage, unless --strict."""

    def quiet(self, argv):
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return check_claims.main(argv)

    def test_internal_error_exits_0(self):
        real = check_claims.run
        check_claims.run = lambda args: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            self.assertEqual(self.quiet(["--repo", "."]), 0)
            self.assertEqual(self.quiet(["--repo", ".", "--strict"]), 1)
        finally:
            check_claims.run = real

    def test_bad_usage_exits_0(self):
        self.assertEqual(self.quiet(["--format", "nonesuch"]), 0)


@unittest.skipUnless(HAS_GIT, "git not on PATH")
class DiffMode(unittest.TestCase):
    """--diff reports only the lines a commit adds, at HEAD's line numbers."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("cfbfastR", self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        git(self.repo, "branch", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def test_only_added_lines_are_reported(self):
        # move the real bad bullet (line 8) to the top: the old line 8 is not
        # added, the new line 1 is
        p = self.repo / "R" / "cfbd_api_key.R"
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        bad = lines.pop(7)
        p.write_text(bad + "".join(lines), encoding="utf-8")
        git(self.repo, "commit", "-q", "-am", "move")
        got = run(self.repo, "--diff", "base", "--checks", "T1")
        self.assertEqual([(f.line, f.token) for f in got], [(1, "register_cfbd()")])

    def test_nothing_added_reports_nothing(self):
        self.assertEqual(run(self.repo, "--diff", "base", "--checks", "T1"), [])


class T1ValidTeamNames(unittest.TestCase):
    """sdvplotR's data-issue template asked reporters to run a function NAMESPACE lacks."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("sdvplotR", self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_flags_the_code_fence_call(self):
        got = [(f.path, f.line, f.token) for f in run(self.repo, "--checks", "T1")]
        self.assertEqual(
            got, [(".github/ISSUE_TEMPLATE/data_issue.md", 34, "valid_team_names()")]
        )

    def test_exported_call_on_next_line_resolves(self):
        self.assertNotIn(35, {f.line for f in run(self.repo, "--checks", "T1")})


@unittest.skipUnless(HAS_GIT, "git not on PATH")
class T2LedgerNegation(unittest.TestCase):
    """A ledger line that names a path and says it does not exist must stay green."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("ledger", self.repo)
        (self.repo / "tests" / "codegen").mkdir(parents=True)
        (self.repo / "tests" / "codegen" / "test_other.py").write_text(
            "def test_x():\n    pass\n", encoding="utf-8"
        )
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def test_negated_path_stays_green(self):
        self.assertEqual(run(self.repo, "--checks", "T2", "--path-ref", "HEAD"), [])

    def test_same_path_without_the_negation_is_flagged(self):
        # positive control: the path check itself fires, so the green above is the exemption
        p = self.repo / "ledger.md"
        line = (FIXTURES / "ledger" / "progress.md").read_text(encoding="utf-8")
        p.write_text(line.split(". That file")[0] + ".\n", encoding="utf-8")
        git(self.repo, "add", "ledger.md")
        git(self.repo, "commit", "-q", "-m", "control")
        got = run(self.repo, "--checks", "T2", "--path-ref", "HEAD", "ledger.md")
        self.assertEqual(
            [(f.path, f.line, f.token) for f in got],
            [("ledger.md", 1, "tests/codegen/test_source_gate.py")],
        )

    def test_existing_path_resolves(self):
        p = self.repo / "notes.md"
        p.write_text(
            "See `tests/codegen/test_other.py:1` for the gate.\n", encoding="utf-8"
        )
        git(self.repo, "add", "notes.md")
        git(self.repo, "commit", "-q", "-m", "n")
        self.assertEqual(
            run(self.repo, "--checks", "T2", "--path-ref", "HEAD", "notes.md"), []
        )


class T1ForeignAttribution(unittest.TestCase):
    """Roxygen that names sibling packages' functions is not a claim about this one."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("foreign", self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_names_attributed_to_other_packages_stay_green(self):
        # `hoopR::a()` and `b()`; hoopR's/wehoop's `a()` / `b()`
        self.assertEqual(run(self.repo, "--checks", "T1"), [])

    def test_unattributed_call_on_the_same_lines_is_flagged(self):
        # positive control: strip the attribution and the second name is a miss
        p = self.repo / "R" / "court_coords.R"
        text = p.read_text(encoding="utf-8").replace("hoopR's/wehoop's", "the")
        p.write_text(text, encoding="utf-8")
        got = {f.token for f in run(self.repo, "--checks", "T1")}
        self.assertIn("load_wnba_stats_shots()", got)


@unittest.skipUnless(HAS_GIT, "git not on PATH")
class T2TemplateComment(unittest.TestCase):
    """A PR template's example paths sit inside an HTML comment: not claims."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        copy_fixture("foreign", self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def test_commented_example_paths_stay_green(self):
        got = run(self.repo, "--checks", "T2", "--path-ref", "HEAD")
        self.assertEqual(got, [])

    def test_same_paths_outside_the_comment_are_flagged(self):
        p = self.repo / ".github" / "PULL_REQUEST_TEMPLATE.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("<!--", "").replace("-->", ""),
            encoding="utf-8",
        )
        git(self.repo, "commit", "-q", "-am", "uncomment")
        got = {f.token for f in run(self.repo, "--checks", "T2", "--path-ref", "HEAD")}
        self.assertIn("R/query_sales.R", got)


class Exemptions(unittest.TestCase):
    def tok(self, context, next_context=""):
        return check_claims.Token(
            1, "path", "tests/x.py", context=context, next_context=next_context
        )

    def test_future_tense(self):
        self.assertTrue(check_claims.exempt(self.tok("We will add tests/x.py next.")))

    def test_absence_in_next_sentence(self):
        self.assertTrue(
            check_claims.exempt(
                self.tok("tests/x.py.", "That file does not exist on main.")
            )
        )

    def test_plain_statement_is_not_exempt(self):
        self.assertFalse(
            check_claims.exempt(
                self.tok("The gate lives in tests/x.py.", "It runs in CI.")
            )
        )


class Resolution(unittest.TestCase):
    def names(self):
        n = check_claims.Names(package="cfbfastR", exports={"load_cfb_pbp"})
        n.allowed = {"library"}
        n.heads = {"cfbfastR"}
        return n

    def test_foreign_qualified_is_not_checked(self):
        t = check_claims.Token(1, "call", "nonesuch", qualifier="dplyr")
        self.assertIsNone(check_claims.resolve_call(t, self.names()))

    def test_own_qualified_needs_export(self):
        t = check_claims.Token(1, "call", "nonesuch", qualifier="cfbfastR")
        self.assertFalse(check_claims.resolve_call(t, self.names()))

    def test_base_resolves(self):
        t = check_claims.Token(1, "call", "library")
        self.assertTrue(check_claims.resolve_call(t, self.names()))


if __name__ == "__main__":
    unittest.main()
