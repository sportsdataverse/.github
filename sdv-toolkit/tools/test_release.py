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

import release

PLUGIN = (
    b'{\r\n  "name": "sdv-toolkit",\r\n  "version": "0.18.2",\r\n'
    b'  "description": "x"\r\n}\r\n'
)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", *args],
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


class MirrorTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.src = base / "org" / "sdv-toolkit"
        self.dest = base / "dotfiles" / "sdv-toolkit"
        _write(self.src / "README.md", b"# t\r\nline\r\n")
        _write(self.src / "pkg" / "mod.py", b"x = 1\n")
        _write(self.src / "pkg" / "__pycache__" / "m.pyc", b"\x00pyc")
        _write(self.src / "pkg" / "stray.pyc", b"\x00pyc")
        _write(self.src / ".omc" / "x.json", b"{}")
        _write(self.src / ".pytest_cache" / "v", b"x")
        _write(self.src / ".ruff_cache" / "CACHEDIR.TAG", b"x")
        _write(self.src / "logo.bin", b"\x89PNG\r\n\x00\r\n")
        script = _write(self.src / "scripts" / "run.sh", b"#!/bin/sh\necho hi\n")
        script.chmod(0o755)
        _write(self.dest / "stale.txt", b"old")
        _write(self.dest / "gone" / "deep.txt", b"old")
        _write(self.dest / ".omc" / "keep", b"session")

    def tearDown(self):
        self._tmp.cleanup()

    def _mirror(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return release.mirror(self.src, self.dest, dry_run=dry_run)

    def _verify(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = release.verify(self.src, self.dest)
        return code, out.getvalue()

    def test_mirror(self):
        added, updated, deleted = self._mirror()
        self.assertEqual(
            sorted(added), ["README.md", "logo.bin", "pkg/mod.py", "scripts/run.sh"]
        )
        self.assertEqual(updated, [])
        self.assertEqual(sorted(deleted), ["gone/deep.txt", "stale.txt"])
        self.assertEqual((self.dest / "README.md").read_bytes(), b"# t\nline\n")
        self.assertEqual((self.dest / "logo.bin").read_bytes(), b"\x89PNG\r\n\x00\r\n")
        self.assertFalse((self.dest / ".omc" / "x.json").exists())
        self.assertFalse((self.dest / "pkg" / "__pycache__").exists())
        self.assertFalse((self.dest / "pkg" / "stray.pyc").exists())
        self.assertFalse((self.dest / ".pytest_cache").exists())
        self.assertFalse((self.dest / ".ruff_cache").exists())
        self.assertFalse((self.dest / "stale.txt").exists())
        self.assertFalse((self.dest / "gone").exists())
        self.assertEqual((self.dest / ".omc" / "keep").read_bytes(), b"session")
        # Second run is a no-op.
        self.assertEqual(self._mirror(), ([], [], []))

    @unittest.skipIf(os.name == "nt", "no POSIX exec bit on Windows")
    def test_mirror_preserves_exec_bit(self):
        self._mirror()
        script = self.dest / "scripts" / "run.sh"
        self.assertTrue(script.stat().st_mode & stat.S_IXUSR)
        script.chmod(0o644)  # mode-only drift is an update
        self.assertEqual(self._mirror(), ([], ["scripts/run.sh"], []))
        self.assertTrue(script.stat().st_mode & stat.S_IXUSR)

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
        code, out = self._verify()
        self.assertEqual(code, 1)
        self.assertIn("README.md", out)
        self.assertIn("extra.txt", out)

    def test_dry_run_writes_nothing(self):
        before = _snapshot(self.dest)
        added, _, deleted = self._mirror(dry_run=True)
        self.assertTrue(added and deleted)
        self.assertEqual(_snapshot(self.dest), before)

    def test_refuses_dangerous_dest(self):
        with self.assertRaises(ValueError):
            self._mirror_to(self.dest.parent)  # wrong name: would wipe a repo root
        with self.assertRaises(ValueError):
            self._mirror_to(self.src)  # dest is the source

    def _mirror_to(self, dest):
        with contextlib.redirect_stdout(io.StringIO()):
            release.mirror(self.src, dest, dry_run=True)


if __name__ == "__main__":
    unittest.main()
