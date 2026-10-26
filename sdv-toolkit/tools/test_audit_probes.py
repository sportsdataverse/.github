"""Tests for skills/sdv-repo-audit/scripts/audit_probes.py and the skill's safety text.

Run: python -m unittest discover -s tools -p 'test_*.py'

Fully offline: the pure functions get text, the probes get temp trees, and the
network and git calls are stubbed. Every pattern has a positive AND a negative
case -- a leak regex that matches house style teaches the auditor to ignore it,
and a probe that prints "none" for a source it never compared reads greener than
it checked.
"""

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLKIT = pathlib.Path(__file__).resolve().parent.parent
SKILL = TOOLKIT / "skills" / "sdv-repo-audit"
AGENT = TOOLKIT / "agents" / "sdv-repo-auditor.md"
sys.path.insert(0, str(SKILL / "scripts"))

import audit_probes as ap  # noqa: E402

_DIRS = []


def tearDownModule():
    for d in _DIRS:
        shutil.rmtree(d, ignore_errors=True)


def tree(files, name=None):
    d = pathlib.Path(tempfile.mkdtemp())
    _DIRS.append(d)
    if name:
        d = d / name
        d.mkdir()
    for rel, body in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return d


class Archetype(unittest.TestCase):
    def test_detect(self):
        self.assertEqual(ap.detect_archetype(tree({"tools/codegen/generate.py": ""})), "sdv-py")
        self.assertEqual(ap.detect_archetype(tree({"README.md": ""}), "git@github.com:o/nfl-data.git"), "producer")
        self.assertEqual(ap.detect_archetype(tree({"DESCRIPTION": "Package: x", "R/x.R": ""})), "r-package")
        self.assertEqual(ap.detect_archetype(tree({"package.json": "{}"})), "web")
        self.assertEqual(ap.detect_archetype(tree({"pyproject.toml": ""})), "python-package")
        self.assertEqual(ap.detect_archetype(tree({"README.md": ""})), "other")

    def test_dot_path_resolves_before_name(self):
        d = tree({"README.md": ""}, name="foo-data")
        cwd = os.getcwd()
        os.chdir(d)
        try:
            self.assertEqual(ap.detect_archetype(pathlib.Path(".")), "producer")
        finally:
            os.chdir(cwd)

    def test_no_router_mirror_claim(self):
        self.assertNotIn("sdv_router", ap.detect_archetype.__doc__)

    def test_every_archetype_has_a_reference(self):
        for arch in ("sdv-py", "python-package", "r-package", "producer", "web", "other"):
            self.assertIn(arch, ap.REFERENCE_FOR)


class Release(unittest.TestCase):
    def test_local_version_sources(self):
        py = tree({"pyproject.toml": '[build-system]\nversion = "9"\n[project]\nname = "x"\nversion = "0.1.5"\n'})
        self.assertEqual(ap.local_version(py), ("0.1.5", "pyproject.toml"))
        r = tree({"DESCRIPTION": "Package: x\nVersion: 3.0.0.9000\n"})
        self.assertEqual(ap.local_version(r), ("3.0.0.9000", "DESCRIPTION"))
        js = tree({"package.json": json.dumps({"version": "4.0.0"})})
        self.assertEqual(ap.local_version(js), ("4.0.0", "package.json"))

    def test_changelog_heading(self):
        head = ap.newest_changelog_heading(tree({"CHANGELOG.md": "# Changelog\n\n## 0.1.5 Release: Oct 8\n## 0.1.4\n"}))
        self.assertEqual(head[0], "0.1.5")
        self.assertEqual(ap.newest_changelog_heading(tree({"NEWS.md": "# cfbfastR 3.0.0\n"}))[0], "3.0.0")
        dev = ap.newest_changelog_heading(tree({"NEWS.md": "# cfbfastR (development version)\n# cfbfastR 3.0.0\n"}))
        self.assertEqual((dev[0], dev[2]), (None, True))

    def test_vkey_orders_numerically(self):
        self.assertGreater(ap.vkey("0.1.10"), ap.vkey("0.1.9"))
        self.assertGreater(ap.vkey("v3.0.0.9000"), ap.vkey("3.0.0"))

    def test_vkey_pads_trailing_zeros(self):
        self.assertEqual(ap.vkey("1.0"), ap.vkey("1.0.0"))
        out = ap.compare_release("1.0", "1.0.0", ["v1.0.0"], "v1.0.0", None)
        self.assertFalse(any("BEHIND" in m for m in out), out)

    def test_unreleased_changelog_is_the_sdv_py_case(self):
        tags = ["v0.1.3", "v0.1.4", "0.36.0", "0.37.0"]  # old-line tags sort above the current line
        out = ap.compare_release("0.1.5", "0.1.4", tags, "v0.1.4", "0.1.5")
        self.assertTrue(any("unreleased work" in m for m in out))
        self.assertTrue(any("never published" in m for m in out))
        self.assertFalse(any("no git tag" in m or "Latest" in m for m in out), out)

    def test_in_sync_is_silent(self):
        self.assertEqual(ap.compare_release("1.0.0", "1.0.0", ["v1.0.0"], "v1.0.0", "1.0.0"), [])

    def test_r_dev_version_is_not_unreleased_work(self):
        out = ap.compare_release("3.0.0.9000", "3.0.0", ["v3.0.0"], "v3.0.0", None)
        self.assertEqual(len(out), 1)
        self.assertIn("development version", out[0])

    def test_tagged_but_not_published(self):
        out = ap.compare_release("0.2.0", "0.1.4", ["v0.1.4", "v0.2.0"], "v0.2.0", None)
        self.assertTrue(any("publish step did not run" in m for m in out))
        self.assertTrue(any("'Latest' release v0.2.0" in m for m in out))

    def test_registry_version_without_tag(self):
        self.assertTrue(any("no git tag" in m for m in ap.compare_release("1.0.0", "1.0.0", ["v0.9"], "", None)))
        # tags unavailable (None) is not "no tag"
        self.assertEqual(ap.compare_release("1.0.0", "1.0.0", None, None, None), [])

    def test_count_fragments(self):
        d = tree({"changelog.d/a.fixed.md": "-", "changelog.d/b.fixed.md": "-", "changelog.d/README.md": ""})
        self.assertEqual(ap.count_fragments(d), {"fixed": 2})
        self.assertIsNone(ap.count_fragments(tree({})))


class ProbeRelease(unittest.TestCase):
    """probe_release with git and the network stubbed: a degraded source is a finding, never 'none'."""

    PY = {"pyproject.toml": '[project]\nname = "x"\nversion = "1.0.0"\n'}

    def run_probe(self, files, pypi=None, registry="1.0.0", ls="abc\trefs/tags/v1.0.0\n", since="3\n"):
        def fake_run(cmd, cwd=None, timeout=60):
            if "ls-remote" in cmd:
                return ls
            if "get-url" in cmd:
                return "https://github.com/o/r.git\n"
            if cmd[0] == "gh":
                return "v1.0.0\n"
            if "rev-list" in cmd:
                return since
            return None

        def fake_json(url, data=None, timeout=30):
            return {"info": {"version": registry}} if registry else None

        saved = ap._run, ap._get_json
        ap._run, ap._get_json = fake_run, fake_json
        try:
            res = ap.probe_release(tree(files), None, pypi, None, None)
        finally:
            ap._run, ap._get_json = saved
        return res, ap._md("release", res)

    def test_in_sync_says_none(self):
        res, md = self.run_probe(self.PY, pypi="x")
        self.assertEqual(res["mismatches"], [])
        self.assertIn("**Mismatches:** none", md)
        self.assertEqual(res["commits_since_registry_tag"], "v1.0.0: 3")

    def test_no_registry_flag_is_not_compared(self):
        res, md = self.run_probe(self.PY)
        self.assertTrue(any("no registry compared" in m for m in res["mismatches"]), res["mismatches"])
        self.assertIn("**Mismatches:** not compared", md)
        self.assertNotIn("**Mismatches:** none", md)

    def test_registry_unavailable_is_not_compared(self):
        res, md = self.run_probe(self.PY, pypi="x", registry=None)
        self.assertTrue(any("PyPI version unavailable" in m for m in res["mismatches"]))
        self.assertIn("**Mismatches:** not compared", md)

    def test_local_version_unreadable(self):
        res, md = self.run_probe({"README.md": ""}, pypi="x")
        self.assertTrue(any("local version unreadable" in m for m in res["mismatches"]), res["mismatches"])
        self.assertIn("**Mismatches:** not compared", md)

    def test_ls_remote_failed(self):
        res, md = self.run_probe(self.PY, pypi="x", ls=None)
        self.assertEqual(res["tags_by_version"], "unavailable")
        self.assertTrue(any("git ls-remote failed" in m for m in res["mismatches"]), res["mismatches"])
        self.assertIn("**Mismatches:** not compared", md)

    def test_rev_list_failure_is_unavailable(self):
        res, _ = self.run_probe(self.PY, pypi="x", since=None)
        self.assertEqual(res["commits_since_registry_tag"], "v1.0.0: unavailable")


class Run(unittest.TestCase):
    def test_run_never_prompts(self):
        seen = {}

        def fake(cmd, **kw):
            seen.update(kw)
            return subprocess.CompletedProcess(cmd, 0, "ok", "")

        saved = ap.subprocess.run
        ap.subprocess.run = fake
        try:
            self.assertEqual(ap._run(["git", "status"]), "ok")
        finally:
            ap.subprocess.run = saved
        self.assertIs(seen["stdin"], subprocess.DEVNULL)
        self.assertEqual(seen["env"]["GIT_TERMINAL_PROMPT"], "0")

    def test_docstring_names_gh_api(self):
        self.assertNotIn("gh release list", ap.__doc__)
        self.assertIn("gh api", ap.__doc__)


class Fragments(unittest.TestCase):
    def test_good_fragment(self):
        self.assertEqual(ap.lint_fragment_text("- **NFL:** fix the thing (#123)\n"), [])
        self.assertEqual(ap.lint_fragment_text("- **NFL:** fix\n  over two lines (#1)\n"), [])

    def test_missing_pr(self):
        self.assertEqual(ap.lint_fragment_text("- **NFL:** fix the thing\n"), [(1, "no PR number")])

    def test_too_long_and_internal_ids(self):
        text = "- **CFB:** a (#1)\n  b\n  c\n  d (B-M31, task 3.8)\n"
        probs = [p for _, p in ap.lint_fragment_text(text)]
        self.assertIn("bullet runs 4 lines (max 3)", probs)
        self.assertIn("internal id 'B-M31'", probs)
        self.assertIn("internal id 'task 3.8'", probs)

    def test_capital_phase_is_an_internal_id(self):
        self.assertIn("internal id 'Phase 5'", [p for _, p in ap.lint_fragment_text("- see Phase 5 (#1)\n")])

    def test_blank_line_separates_bullets(self):
        self.assertEqual(ap.lint_fragment_text("- one (#1)\n\n- two (#2)\n"), [])

    def test_no_bullet(self):
        self.assertEqual(ap.lint_fragment_text("just prose (#1)\n"), [(1, "no bullet (expected '- ...')")])

    def test_probe_names_and_newline(self):
        d = tree(
            {"changelog.d/ok.fixed.md": "- x (#1)\n", "changelog.d/bad.md": "- x (#1)", "changelog.d/README.md": "x"}
        )
        res = ap.probe_fragments(d, "changelog.d", 3, ["fixed"])
        probs = {(f["file"], f["problem"]) for f in res["findings"]}
        self.assertIn(("changelog.d/bad.md", "name is not <slug>.<group>.md with a known group"), probs)
        self.assertIn(("changelog.d/bad.md", "no final newline"), probs)
        self.assertFalse(any(f.startswith("changelog.d/ok") for f, _ in probs))
        self.assertEqual(res["fragments"], 2)


class Leaks(unittest.TestCase):
    def kinds(self, text, private=("sdv-internal-refs",)):
        return {(k, t) for _, k, t in ap.scan_leaks(text, list(private))}

    def ip_hits(self, line):
        return [t for _, k, t in ap.scan_leaks(line, []) if k == "ip-address"]

    def test_positive(self):
        text = "\n".join(
            [
                "see C:/Users/saiem/Documents/x",
                "or c:\\Users\\saiem\\x",
                "lives in /mnt/sdv_repos/cfb",
                "box 165.227.83.92",
                "rule (A-L60) and Task 3.1 and R828-4",
                "# ponytail: lazy",
                "see dev/phase5f-live-proof.md",
                "read sdv-internal-refs/nba/README.md",
            ]
        )
        kinds = {k for k, _ in self.kinds(text)}
        self.assertEqual(
            kinds,
            {"local-path", "server-path", "ip-address", "internal-id", "agent-note", "working-note", "private-repo"},
        )

    def test_real_ips_next_to_dashes_and_version_words(self):
        for line in (
            "165.227.83.92 - prod droplet",
            "ssh root@165.227.83.92 (python v3.12)",
            "curl http://165.227.83.92/api/v1/teams",
        ):
            self.assertEqual(self.ip_hits(line), ["165.227.83.92"], line)

    def test_negative(self):
        text = "\n".join(
            [
                "https://site.api.espn.com/apis/site/v2/sports/football/team/home/away/",
                "listen on 127.0.0.1 or 0.0.0.0; example 1.2.3.4 and 192.168.1.10 and 203.0.113.10",
                "requires polars>=2.0.1.3 and numpy==1.26.4.1",
                "release v3.12.0.1 and version 2.0.1.3",
                "mount -t /mnt-style paths are fine in prose like dev-dependencies",
                "the B-tree and A-league",
                "docs/dev/guide.md is not a dev/ working note",
            ]
        )
        self.assertEqual(self.kinds(text), set())

    def test_probe_applies_exclude_globs(self):
        d = tree(
            {"README.md": "C:/Users/saiem/x\n", "docs/a.md": "ok\n", "docs/versioned_docs/v1/a.md": "C:/Users/x/y\n"}
        )
        res = ap.probe_leaks(d, [], [], ["*versioned_docs/*"])
        self.assertEqual([(f["file"], f["kind"]) for f in res["findings"]], [("README.md", "local-path")])

    def test_tracked_only_in_a_git_tree(self):
        d = tree({"README.md": "C:/Users/saiem/x\n", "docs/notes.md": "C:/Users/saiem/y\n"})
        for cmd in (["git", "init", "-q"], ["git", "add", "README.md"]):
            subprocess.run(cmd, cwd=d, check=True, capture_output=True)
        res = ap.probe_leaks(d, [], [])
        self.assertEqual([f["file"] for f in res["findings"]], ["README.md"])

    def test_explicit_path_resolves_against_root(self):
        d = tree({"README.md": "C:/Users/saiem/x\n"})
        res = ap.probe_leaks(d, [pathlib.Path("README.md")], [])
        self.assertEqual([f["file"] for f in res["findings"]], ["README.md"])

    def test_missing_explicit_path_is_an_error(self):
        d = tree({"README.md": "ok\n"})
        with self.assertRaisesRegex(ValueError, "nope.md"):
            ap.probe_leaks(d, [pathlib.Path("nope.md")], [])
        with self.assertRaisesRegex(ValueError, "nope.md"):
            ap.probe_counts(d, [pathlib.Path("nope.md")])
        self.assertEqual(ap.main(["leaks", "nope.md", "--root", str(d)]), 2)
        self.assertEqual(ap.main(["counts", "nope.md", "--root", str(d)]), 2)


class Counts(unittest.TestCase):
    def test_find(self):
        hits = ap.find_counts("We ship 4,566 ESPN wrappers across 40 leagues.\n")
        self.assertEqual([(n, noun) for _, n, noun, _ in hits], [(4566, "wrappers"), (40, "leagues")])

    def test_ignores_years_singletons_and_fences(self):
        text = "Since 2024 seasons\n1 function\n```\n128 wrappers\n```\nversion 0.1.5 leagues\n"
        self.assertEqual(ap.find_counts(text), [])

    def test_comma_numbers_in_year_range_are_counts(self):
        self.assertEqual([n for _, n, _, _ in ap.find_counts("1,950 functions and 2,048 wrappers\n")], [1950, 2048])

    def test_probe_groups_by_noun(self):
        d = tree(
            {
                "README.md": "126 short names across 40 leagues\n",
                "docs/intro.md": "105 leagues\n",
                "docs/nba/reference/x.md": "999 leagues\n",
            }
        )
        res = ap.probe_counts(d, [], ["*/reference/*"])
        self.assertEqual(res["nouns_quoted_with_several_numbers"], {"leagues": [40, 105]})


class Osv(unittest.TestCase):
    UV = (
        '[[package]]\nname = "certifi"\nversion = "2026.6.17"\nsource = { registry = "x" }\n\n'
        '[[package]]\nname = "sportsdataverse"\nversion = "0.1.5"\nsource = { editable = "." }\n'
    )

    def test_parse_locks(self):
        d = tree(
            {
                "uv.lock": self.UV,
                "renv.lock": json.dumps(
                    {
                        "Packages": {
                            "cli": {"Version": "3.6.0", "Source": "Repository"},
                            "mine": {"Version": "1.0", "Source": "GitHub"},
                        }
                    }
                ),
                "package-lock.json": json.dumps(
                    {"packages": {"": {"version": "1"}, "node_modules/a/node_modules/@s/b": {"version": "2.0.0"}}}
                ),
            }
        )
        self.assertEqual(ap.parse_lock(d / "uv.lock"), [("PyPI", "certifi", "2026.6.17")])
        self.assertEqual(ap.parse_lock(d / "renv.lock"), [("CRAN", "cli", "3.6.0")])
        self.assertEqual(ap.parse_lock(d / "package-lock.json"), [("npm", "@s/b", "2.0.0")])

    def test_unsupported_lockfile_is_named_before_parsing(self):
        d = tree({"Cargo.lock": "[[package]]\nname = 'x'\n", "yarn.lock": "x@1:\n  version 1\n"})
        for name in ("Cargo.lock", "yarn.lock"):
            with self.assertRaisesRegex(ValueError, "unsupported lockfile"):
                ap.parse_lock(d / name)

    def test_package_lock_v1_dependencies(self):
        lock = {
            "lockfileVersion": 1,
            "dependencies": {"a": {"version": "1.0.0", "dependencies": {"b": {"version": "2.0.0"}}}},
        }
        d = tree({"package-lock.json": json.dumps(lock)})
        self.assertEqual(ap.parse_lock(d / "package-lock.json"), [("npm", "a", "1.0.0"), ("npm", "b", "2.0.0")])

    def test_zero_packages_is_an_error(self):
        d = tree({"uv.lock": "version = 1\n", "package-lock.json": json.dumps({"lockfileVersion": 3})})
        for name in ("uv.lock", "package-lock.json"):
            with self.assertRaisesRegex(ValueError, "0 packages"):
                ap.probe_osv(d / name, post=lambda u, b: {"results": []})
            self.assertEqual(ap.main(["osv", str(d / name)]), 2)

    def test_probe_with_fake_post(self):
        d = tree({"uv.lock": self.UV})
        calls = []

        def post(url, body):
            calls.append(url)
            return {"results": [{"vulns": [{"id": "GHSA-x"}]} for _ in body["queries"]]}

        orig = ap._get_json
        ap._get_json = lambda url, data=None, timeout=30: {
            "database_specific": {"severity": "CRITICAL"},
            "summary": "bad",
            "aliases": ["CVE-1"],
        }
        try:
            res = ap.probe_osv(d / "uv.lock", post=post)
        finally:
            ap._get_json = orig
        self.assertEqual(calls, ["https://api.osv.dev/v1/querybatch"])
        self.assertEqual(res["vulnerable"][0]["name"], "certifi")
        self.assertEqual(res["vulnerable"][0]["advisories"][0]["severity"], "CRITICAL")

    def test_unreachable_is_reported_not_guessed(self):
        res = ap.probe_osv(tree({"uv.lock": self.UV}) / "uv.lock", post=lambda u, b: None)
        self.assertEqual(res["error"], "OSV unreachable")


class DocsSafety(unittest.TestCase):
    """The audit's read-only and hostile-host rules must be stated wherever an auditor reads."""

    DOCS = [SKILL / "SKILL.md", AGENT] + sorted((SKILL / "references").glob("*.md"))

    def text(self, p):
        return p.read_text(encoding="utf-8")

    def test_safety_block_everywhere(self):
        for p in self.DOCS:
            t = self.text(p)
            for needle in (
                "stats.nba.com",
                "stats.ncaa.org",
                "SDV_PY_LIVE_TESTS",
                "SDV_PY_NBA_STATS_LIVE",
                "sandbox.sh",
                "--frozen",
            ):
                self.assertIn(needle, t, "%s lacks %r" % (p.name, needle))

    def test_every_uv_tree_is_frozen(self):
        for p in self.DOCS:
            for m in re.finditer(r"uv tree[^`\n]*", self.text(p)):
                self.assertIn("--frozen", m.group(0), "%s: %s" % (p.name, m.group(0)))
                if "--invert" in m.group(0):
                    self.assertIn("--package", m.group(0), "%s: %s" % (p.name, m.group(0)))

    def test_no_run_every_command(self):
        self.assertNotIn("Run every command", self.text(SKILL / "SKILL.md"))

    def test_skill_details(self):
        sk = self.text(SKILL / "SKILL.md")
        self.assertNotIn("sdv_router", sk)  # the probe's rules are its own
        self.assertNotRegex(sk, r"\.worktrees/audit-main\b")  # one fixed name collides across audits
        self.assertIn('mkdir -p "$O"', sk)  # probes redirect into it
        # the worktree is removed only after verification and synthesis
        self.assertGreater(sk.index("worktree remove"), sk.index("## Phase 5"))

    def test_producer_lens_does_not_nest_a_sixth_agent(self):
        t = self.text(SKILL / "references" / "producer.md")
        self.assertNotIn("Dispatch `sdv-dataset-coverage-auditor`", t)
        self.assertIn("inline", t)

    def test_table_pipes_escaped(self):
        for p in sorted((SKILL / "references").glob("*.md")):
            for i, line in enumerate(self.text(p).splitlines(), 1):
                if line.startswith("|"):
                    for code in re.findall(r"`([^`]*)`", line):
                        self.assertNotRegex(code, r"(?<!\\)\|", "%s:%d unescaped pipe in %r" % (p.name, i, code))

    def test_r_recipes(self):
        t = self.text(SKILL / "references" / "r-package.md")
        self.assertNotIn('package_deps("<W>")', t)
        self.assertIn("dev_package_deps", t)
        self.assertNotIn('load_all("<W>"', t)

    def test_python_recipe_is_generic(self):
        t = self.text(SKILL / "references" / "python-package.md")
        self.assertIn("src/", t)
        self.assertIn("<import_name>", t)


class Cli(unittest.TestCase):
    def test_usage_error_exit_2(self):
        self.assertEqual(ap.main(["osv", str(tree({}) / "missing.lock")]), 2)


if __name__ == "__main__":
    unittest.main()
