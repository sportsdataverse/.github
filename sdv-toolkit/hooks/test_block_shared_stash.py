"""Tests for block_shared_stash. Run: python -m unittest discover -s hooks -p 'test_*.py'"""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

HOOK = pathlib.Path(__file__).resolve().parent / "block_shared_stash.py"


def _git(*args):
    subprocess.run(["git", *args], check=True, capture_output=True)


def run_hook(command, cwd, raw=None):
    payload = (
        raw
        if raw is not None
        else json.dumps({"cwd": str(cwd), "tool_input": {"command": command}})
    )
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


class BlockSharedStashTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        base = pathlib.Path(cls._tmp.name)
        cls.plain = base / "plain"  # not a git repo
        cls.single = base / "single"  # one worktree
        cls.multi = base / "multi"  # main worktree + one linked worktree
        cls.linked = base / "multi-wt"
        cls.plain.mkdir()
        for repo in (cls.single, cls.multi):
            _git("init", "-q", str(repo))
            _git(
                "-C",
                str(repo),
                "-c",
                "user.name=t",
                "-c",
                "user.email=t@example.com",
                "commit",
                "-q",
                "--allow-empty",
                "-m",
                "init",
            )
        _git("-C", str(cls.multi), "worktree", "add", "-q", str(cls.linked), "-b", "wt")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def assertBlocked(self, command, cwd):
        r = run_hook(command, cwd)
        self.assertEqual(r.returncode, 2, (command, r.stderr))
        self.assertIn("BLOCKED", r.stderr)
        self.assertIn("2 worktrees", r.stderr)

    def assertAllowed(self, command, cwd):
        r = run_hook(command, cwd)
        self.assertEqual(r.returncode, 0, (command, r.stderr))

    def test_single_worktree_stash_allowed(self):
        self.assertAllowed("git stash", self.single)

    def test_multi_worktree_bare_stash_blocked(self):
        self.assertBlocked("git stash", self.multi)

    def test_multi_worktree_pop_from_linked_blocked(self):
        self.assertBlocked("git stash pop", self.linked)

    def test_dash_c_resolves_repo(self):
        self.assertBlocked("git -C %s stash apply" % self.linked, self.plain)
        self.assertAllowed("git -C %s stash apply" % self.single, self.plain)

    def test_cd_chain_resolves_repo(self):
        self.assertBlocked("cd '%s' && git stash push -m x" % self.multi, self.plain)
        self.assertAllowed("cd %s && git stash push -m x" % self.single, self.plain)

    def test_chain_and_redirect(self):
        self.assertBlocked("git status; git stash 2>/dev/null || true", self.multi)
        self.assertBlocked("git stash -u", self.multi)

    def test_list_and_show_allowed(self):
        self.assertAllowed("git stash list", self.multi)
        self.assertAllowed("git stash show -p stash@{0}", self.multi)

    def test_non_git_stash_word_allowed(self):
        self.assertAllowed("grep -rn stash . | head; echo 'git stash pop'", self.multi)
        self.assertAllowed('git commit -m "avoid git stash"', self.multi)

    def test_malformed_input_fails_open(self):
        self.assertEqual(run_hook(None, self.multi, raw="not json{").returncode, 0)
        self.assertEqual(run_hook(None, self.multi, raw="").returncode, 0)
        self.assertEqual(run_hook('git stash "unclosed', self.multi).returncode, 0)


if __name__ == "__main__":
    unittest.main()
