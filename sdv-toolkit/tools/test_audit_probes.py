"""Tests for skills/sdv-repo-audit/scripts/audit_probes.py.

Run: python -m unittest discover -s tools -p 'test_*.py'

Fully offline: the pure functions get text, the probes get temp trees, and the
OSV probe gets a fake POST. Every pattern has a positive AND a negative case --
a leak regex that matches house style teaches the auditor to ignore it.
"""

import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(
    0,
    str(pathlib.Path(__file__).resolve().parent.parent / "skills" / "sdv-repo-audit" / "scripts"),
)

import audit_probes as ap  # noqa: E402


def tree(files):
    d = pathlib.Path(tempfile.mkdtemp())
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
        self.assertEqual(
            ap.newest_changelog_heading(tree({"CHANGELOG.md": "# Changelog\n\n## 0.1.5 Release: Oct 8\n## 0.1.4\n"}))[
                :1
            ],
            ("0.1.5",),
        )
        self.assertEqual(ap.newest_changelog_heading(tree({"NEWS.md": "# cfbfastR 3.0.0\n"}))[0], "3.0.0")
        dev = ap.newest_changelog_heading(tree({"NEWS.md": "# cfbfastR (development version)\n# cfbfastR 3.0.0\n"}))
        self.assertEqual((dev[0], dev[2]), (None, True))

    def test_vkey_orders_numerically(self):
        self.assertGreater(ap.vkey("0.1.10"), ap.vkey("0.1.9"))
        self.assertGreater(ap.vkey("v3.0.0.9000"), ap.vkey("3.0.0"))

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

    def test_blank_line_separates_bullets(self):
        probs = ap.lint_fragment_text("- one (#1)\n\n- two (#2)\n")
        self.assertEqual(probs, [])

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

    def test_negative(self):
        text = "\n".join(
            [
                "https://site.api.espn.com/apis/site/v2/sports/football/team/home/away/",
                "listen on 127.0.0.1 or 0.0.0.0; example 1.2.3.4 and 192.168.1.10 and 203.0.113.10",
                "requires polars 2.0.1.3 version",
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


class Counts(unittest.TestCase):
    def test_find(self):
        hits = ap.find_counts("We ship 4,566 ESPN wrappers across 40 leagues.\n")
        self.assertEqual([(n, noun) for _, n, noun, _ in hits], [(4566, "wrappers"), (40, "leagues")])

    def test_ignores_years_singletons_and_fences(self):
        text = "Since 2024 seasons\n1 function\n```\n128 wrappers\n```\nversion 0.1.5 leagues\n"
        self.assertEqual(ap.find_counts(text), [])

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
        with self.assertRaises(ValueError):
            ap.parse_lock(tree({"Cargo.lock": ""}) / "Cargo.lock")

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


class Cli(unittest.TestCase):
    def test_usage_error_exit_2(self):
        self.assertEqual(ap.main(["osv", str(tree({}) / "missing.lock")]), 2)


if __name__ == "__main__":
    unittest.main()
