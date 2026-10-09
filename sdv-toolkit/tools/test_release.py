"""Tests for release. Run: python -m unittest discover -s tools -p 'test_*.py'"""

from __future__ import annotations

import contextlib
import io
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import release

PLUGIN = (
    b'{\r\n  "name": "sdv-toolkit",\r\n  "version": "0.18.2",\r\n'
    b'  "description": "x"\r\n}\r\n'
)


GIT_CFG = [
    "-c", "core.autocrlf=false", "-c", "core.safecrlf=false",
    "-c", "user.name=t", "-c", "user.email=t@example.com",
    "-c", "commit.gpgsign=false",
]  # fmt: skip


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", *GIT_CFG, *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def _write(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _snapshot(root: Path) -> dict:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file()
    }


class BumpTest(unittest.TestCase):
    def _bump(self, spec: str) -> bytes:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp) / "plugin.json", PLUGIN)
            with contextlib.redirect_stdout(io.StringIO()):
                release.bump(path, spec)
            return path.read_bytes()

    def test_patch_keeps_crlf_and_only_changes_version(self):
        self.assertEqual(self._bump("patch"), PLUGIN.replace(b"0.18.2", b"0.18.3"))

    def test_minor(self):
        self.assertEqual(self._bump("minor"), PLUGIN.replace(b"0.18.2", b"0.19.0"))

    def test_major(self):
        self.assertEqual(self._bump("major"), PLUGIN.replace(b"0.18.2", b"1.0.0"))

    def test_explicit(self):
        self.assertEqual(self._bump("2.3.4"), PLUGIN.replace(b"0.18.2", b"2.3.4"))

    def test_rejects_garbage(self):
        with self.assertRaises(ValueError):
            self._bump("1.2")


class RestoreCrlfTest(unittest.TestCase):
    def test_restores_crlf_indexed_file_and_leaves_lf_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _git(repo, "init", "-q")
            crlf = _write(repo / "sub" / "crlf.md", b"a\r\nb\r\n")
            lf = _write(repo / "lf.md", b"a\nb\n")
            _git(repo, "add", "sub/crlf.md", "lf.md")

            def fake_render():  # what render.py does on Linux: LF out
                crlf.write_bytes(b"a\nb\nc\n")
                lf.write_bytes(b"a\nb\nc\n")

            restored = release.restore_crlf(repo, fake_render)
            self.assertEqual(restored, ["sub/crlf.md"])
            self.assertEqual(crlf.read_bytes(), b"a\r\nb\r\nc\r\n")
            self.assertEqual(lf.read_bytes(), b"a\nb\nc\n")

            # Already-CRLF working copy: no-op.
            self.assertEqual(release.restore_crlf(repo, lambda: None), [])
            self.assertEqual(crlf.read_bytes(), b"a\r\nb\r\nc\r\n")

    def test_leaves_crlf_indexed_binary_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _git(repo, "init", "-q")
            latin1 = _write(repo / "latin1.txt", b"caf\xe9\r\nna\xefve\r\n")
            blob = _write(repo / "blob.dat", b"a\r\nb\r\n")
            _git(repo, "add", "latin1.txt", "blob.dat")
            self.assertEqual(
                sorted(release.crlf_paths(repo)), ["blob.dat", "latin1.txt"]
            )
            latin1_new = b"caf\xe9\nna\xefve\r\n"  # bare LF, not UTF-8
            blob_new = b"\x00\x01\n\x02"  # bare LF, NUL

            def fake_render():
                latin1.write_bytes(latin1_new)
                blob.write_bytes(blob_new)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                restored = release.restore_crlf(repo, fake_render)
            self.assertEqual(restored, [])
            self.assertEqual(latin1.read_bytes(), latin1_new)
            self.assertEqual(blob.read_bytes(), blob_new)
            self.assertIn("latin1.txt", out.getvalue())
            self.assertIn("blob.dat", out.getvalue())


class RenderFailureTest(unittest.TestCase):
    def test_render_failure_prints_output_and_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _git(repo, "init", "-q")
            _write(
                repo / "tools" / "render.py",
                b"import sys\nprint('render says no')\nsys.exit(3)\n",
            )
            err = io.StringIO()
            with mock.patch.object(release, "TOOLKIT", repo), mock.patch.object(
                release, "REPO", repo
            ), contextlib.redirect_stderr(err), contextlib.redirect_stdout(
                io.StringIO()
            ):
                code = release.main(["render"])
        self.assertEqual(code, 2)
        self.assertIn("render says no", err.getvalue())


def _symlink(test, link, target, **kw):
    """Create a symlink, or skip the test where the platform refuses (Windows without the privilege)."""
    try:
        link.symlink_to(target, **kw)
    except (OSError, NotImplementedError) as e:
        test.skipTest("cannot create symlinks here: %s" % e)


class MirrorTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name).resolve()
        self.org = self.base / "org"
        self.src = self.org / "sdv-toolkit"
        self.dot = self.base / "dotfiles"
        self.dest = self.dot / "sdv-toolkit"
        # Source: an org checkout. Everything below is tracked, junk included,
        # so the exclusions are tested against the tracked set.
        _write(self.src / "README.md", b"# t\r\nline\r\n")
        _write(self.src / "pkg" / "mod.py", b"x = 1\n")
        _write(self.src / "pkg" / "__pycache__" / "m.pyc", b"\x00pyc")
        _write(self.src / "pkg" / "stray.pyc", b"\x00pyc")
        _write(self.src / ".omc" / "x.json", b"{}")
        _write(self.src / ".pytest_cache" / "v", b"x")
        _write(self.src / ".ruff_cache" / "CACHEDIR.TAG", b"x")
        _write(self.src / ".venv" / "lib.py", b"x")
        _write(self.src / "logo.bin", b"\x89PNG\r\n\x00\r\n")
        script = _write(self.src / "scripts" / "run.sh", b"#!/bin/sh\necho hi\n")
        script.chmod(0o755)
        _git(self.org, "init", "-q")
        _git(self.org, "add", "-f", "sdv-toolkit")
        _git(self.org, "commit", "-q", "--no-verify", "-m", "init")
        self.scratch = _write(self.src / "scratch.txt", b"untracked")
        # Dest: the dotfiles checkout. Tracked files, plus one untracked file.
        _write(self.dest / "stale.txt", b"old")
        _write(self.dest / "gone" / "deep.txt", b"old")
        _write(self.dest / ".omc" / "keep", b"session")
        _git(self.dot, "init", "-q")
        _git(self.dot, "add", "-f", "sdv-toolkit")
        self.notes = _write(self.dest / "local-notes.txt", b"mine")

    def tearDown(self):
        self._tmp.cleanup()

    def _mirror(self, dry_run=False, dest=None, **kw):
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
            err
        ):
            result = release.mirror(
                self.src, dest or self.dest, dry_run=dry_run, **kw
            )
        self.stderr = err.getvalue()
        return result

    def _verify(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = release.verify(self.src, self.dest)
        return code, out.getvalue()

    def test_a_symlinked_dest_file_is_refused_and_its_target_untouched(self):
        # Copilot on #50: following a dest symlink would overwrite a file outside dest.
        outside = _write(self.base / "outside.txt", b"precious")
        _symlink(self, self.dest / "README.md", outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self._mirror()
        self.assertEqual(outside.read_bytes(), b"precious")

    def test_a_dest_that_is_itself_a_symlink_is_refused(self):
        # CodeRabbit on #50: with --allow-non-git, a symlink named sdv-toolkit to an outside dir must not pass.
        real = self.base / "outside" / "sdv-toolkit"
        _write(real / "keep.txt", b"precious")
        link_parent = self.base / "links"
        link_parent.mkdir()
        _symlink(self, link_parent / "sdv-toolkit", real, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self._mirror(dest=link_parent / "sdv-toolkit", allow_non_git=True)
        self.assertEqual((real / "keep.txt").read_bytes(), b"precious")

    def test_a_symlinked_dest_directory_is_refused(self):
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        _symlink(self, self.dest / "pkg", elsewhere, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self._mirror()
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_mirror(self):
        added, updated, deleted = self._mirror()
        self.assertEqual(
            sorted(added), ["README.md", "logo.bin", "pkg/mod.py", "scripts/run.sh"]
        )
        self.assertEqual(updated, [])
        self.assertEqual(sorted(deleted), ["gone/deep.txt", "stale.txt"])
        self.assertEqual((self.dest / "README.md").read_bytes(), b"# t\nline\n")
        self.assertEqual((self.dest / "logo.bin").read_bytes(), b"\x89PNG\r\n\x00\r\n")
        for junk in (".omc/x.json", "pkg/__pycache__", "pkg/stray.pyc",
                     ".pytest_cache", ".ruff_cache", ".venv", "scratch.txt"):
            self.assertFalse((self.dest / junk).exists(), junk)
        self.assertFalse((self.dest / "stale.txt").exists())
        self.assertFalse((self.dest / "gone").exists())
        self.assertEqual((self.dest / ".omc" / "keep").read_bytes(), b"session")
        self.assertEqual(self.notes.read_bytes(), b"mine")  # untracked: kept
        # Second run is a no-op.
        self.assertEqual(self._mirror(), ([], [], []))

    def test_warns_about_uncommitted_source(self):
        (self.src / "README.md").write_bytes(b"# edited\n")
        self._mirror(dry_run=True)
        self.assertIn("scratch.txt", self.stderr)
        self.assertIn("README.md", self.stderr)
        self.scratch.unlink()
        _git(self.org, "checkout", "--", "sdv-toolkit/README.md")
        self._mirror(dry_run=True)
        self.assertEqual(self.stderr, "")  # clean checkout: no warning

    @unittest.skipIf(os.name == "nt", "no POSIX exec bit on Windows")
    def test_mirror_preserves_exec_bit(self):
        self._mirror()
        script = self.dest / "scripts" / "run.sh"
        self.assertTrue(script.stat().st_mode & stat.S_IXUSR)
        script.chmod(0o644)  # mode-only drift is an update...
        code, out = self._verify()  # ...and verify must see it too
        self.assertEqual(code, 1)
        self.assertIn("scripts/run.sh", out)
        self.assertEqual(self._mirror(), ([], ["scripts/run.sh"], []))
        self.assertTrue(script.stat().st_mode & stat.S_IXUSR)
        self.assertEqual(self._verify(), (0, ""))

    def test_verify(self):
        self._mirror()
        self.assertEqual(self._verify(), (0, ""))
        (self.dest / "pkg" / "mod.py").write_bytes(b"x = 2\n")
        code, out = self._verify()
        self.assertEqual(code, 1)
        self.assertIn("pkg/mod.py", out)
        self.assertNotIn("README.md", out)  # CRLF-only difference is ignored

    def test_verify_reports_missing_and_extra(self):
        self._mirror()
        (self.dest / "README.md").unlink()
        _write(self.dest / "extra.txt", b"x")
        _git(self.dot, "add", "sdv-toolkit/extra.txt")
        code, out = self._verify()
        self.assertEqual(code, 1)
        self.assertIn("README.md", out)
        self.assertIn("extra.txt", out)
        self.assertNotIn("local-notes.txt", out)  # untracked dest-only file

    def test_dry_run_writes_nothing(self):
        before = _snapshot(self.dest)
        added, _, deleted = self._mirror(dry_run=True)
        self.assertTrue(added and deleted)
        self.assertEqual(_snapshot(self.dest), before)

    def test_refuses_dangerous_dest(self):
        _git(self.org, "worktree", "add", "-q", str(self.base / "org-wt2"))
        for dest in (
            self.dot,  # wrong name: would wipe a repo root
            self.src,  # dest is the source
            self.org / "nested" / "sdv-toolkit",  # inside the org checkout
            self.base / "org-wt2" / "sdv-toolkit",  # a second org worktree
            self.base / "plain" / "sdv-toolkit",  # not a git work tree
        ):
            with self.assertRaises(ValueError, msg=str(dest)):
                self._mirror(dry_run=True, dest=dest)

    def test_non_git_dest_with_allow_flag(self):
        plain = self.base / "plain" / "sdv-toolkit"
        _write(plain / "stale.txt", b"old")
        _write(plain / ".git" / "fake", b"not a repo")
        if release._toplevel(plain) is not None:
            self.skipTest("temp dir is inside a git work tree")
        added, _, deleted = self._mirror(dest=plain, allow_non_git=True)
        self.assertIn("README.md", added)
        self.assertEqual(deleted, ["stale.txt"])  # non-git: every file is ours
        self.assertTrue((plain / ".git" / "fake").exists())  # .git never touched


if __name__ == "__main__":
    unittest.main()
