"""Tests for skills/sdv-review-pr/scripts/pr_context.py.

Run: python -m unittest discover -s tools -p 'test_*.py'

Every signal regex gets a positive AND a negative case. A tripwire that
silently stops matching reads greener than before while checking less, and a
tripwire that matches house style (a setext `=======` heading, a spawn-context
pool) teaches the reviewer to ignore it.
"""

import pathlib
import re
import sys
import unittest

sys.path.insert(
    0,
    str(
        pathlib.Path(__file__).resolve().parent.parent
        / "skills"
        / "sdv-review-pr"
        / "scripts"
    ),
)

import pr_context as pc  # noqa: E402


def diff_for(path, *added, context=()):
    body = [" " + c for c in context] + ["+" + a for a in added]
    return "--- a/%s\n+++ b/%s\n@@ -1,1 +1,%d @@\n%s\n" % (
        path,
        path,
        len(body),
        "\n".join(body),
    )


def rules(diff_text):
    return [s.rule for s in pc.scan_diff(diff_text)]


class ParsePrRef(unittest.TestCase):
    def test_url_slug_and_number(self):
        self.assertEqual(
            pc.parse_pr_ref(
                "https://github.com/saiemgilani/game-on-paper-app/pull/250"
            ),
            ("saiemgilani/game-on-paper-app", 250),
        )
        self.assertEqual(
            pc.parse_pr_ref("sportsdataverse/.github#26"),
            ("sportsdataverse/.github", 26),
        )
        self.assertEqual(
            pc.parse_pr_ref("29", "sportsdataverse/hoopR-nba-stats-data"),
            ("sportsdataverse/hoopR-nba-stats-data", 29),
        )

    def test_bare_number_without_repo_is_an_error_not_a_guess(self):
        with self.assertRaises(ValueError):
            pc.parse_pr_ref("29")


class RepoArchetypes(unittest.TestCase):
    def test_sportsdataverse_data_is_not_a_producer(self):
        # The -data suffix misleads: it is an R package + release-note generator.
        self.assertEqual(
            pc.repo_archetypes("sportsdataverse", "sportsdataverse-data"),
            ["r-package", "platform"],
        )

    def test_python_producer_with_description_stays_a_producer(self):
        # Python -data repos also carry DESCRIPTION + R/; the suffix rule must win.
        self.assertEqual(
            pc.repo_archetypes(
                "sportsdataverse", "hoopR-nba-data", root_names=["DESCRIPTION", "R"]
            ),
            ["data"],
        )

    def test_forks_and_outside_owners_are_out_of_scope(self):
        self.assertEqual(
            pc.repo_archetypes("blackcb", "game-on-paper-app"), ["out-of-scope"]
        )
        self.assertEqual(
            pc.repo_archetypes("sportsdataverse", "staged-recipes", is_fork=True),
            ["out-of-scope"],
        )

    def test_maintainer_owned_repos_skip_house_rules(self):
        self.assertEqual(
            pc.repo_archetypes("sportsdataverse", "sportyR"), ["maintainer-owned"]
        )

    def test_named_repos(self):
        self.assertEqual(
            pc.repo_archetypes("saiemgilani", "game-on-paper-app"), ["web-gop"]
        )
        self.assertEqual(pc.repo_archetypes("sportsdataverse", "sdv-db"), ["platform"])
        self.assertEqual(pc.repo_archetypes("sportsdataverse", ".github"), ["toolkit"])
        self.assertEqual(
            pc.repo_archetypes("saiemgilani", "Sports-Research-Papers"),
            ["research-docs"],
        )
        self.assertEqual(
            pc.repo_archetypes(
                "sportsdataverse", "cfbfastR", root_names=["DESCRIPTION", "NAMESPACE"]
            ),
            ["r-package"],
        )

    def test_references_always_start_with_universal_and_dedupe(self):
        self.assertEqual(
            pc.references_for(["raw", "data", "models"]),
            ["references/universal.md", "references/producers.md"],
        )


class ClassifyPath(unittest.TestCase):
    def test_mixed_pr_paths(self):
        self.assertIn("gha", pc.classify_path(".github/workflows/daily_cfb.yml"))
        self.assertIn("r-package", pc.classify_path("vignettes/intro.Rmd"))
        self.assertIn("models", pc.classify_path("sportsdataverse/cfb/models/ep.ubj"))
        self.assertIn(
            "web-gop", pc.classify_path("astro/src/components/game/PlayRow.astro")
        )
        self.assertEqual(pc.classify_path("README.md"), [])


class LineSignals(unittest.TestCase):
    def test_conflict_marker_but_not_a_setext_heading(self):
        self.assertIn("U-GIT-1", rules(diff_for("python/app.py", "<<<<<<< HEAD")))
        self.assertNotIn("U-GIT-1", rules(diff_for("README.md", "Title", "=======")))

    def test_ai_trailer(self):
        self.assertIn(
            "U-GIT-4",
            rules(diff_for("x.md", "Co-Authored-By: Claude <noreply@anthropic.com>")),
        )
        self.assertNotIn(
            "U-GIT-4", rules(diff_for("x.md", "Co-Authored-By: Akshay <a@b.org>"))
        )

    def test_masked_push_but_not_a_checked_push(self):
        self.assertIn(
            "U-FAIL-1", rules(diff_for("scripts/x.sh", "git push origin main || true"))
        )
        self.assertNotIn(
            "U-FAIL-1", rules(diff_for("scripts/x.sh", "git push origin main"))
        )

    def test_broad_except_only_in_python(self):
        self.assertIn(
            "U-FAIL-1", rules(diff_for("python/a.py", "    except Exception:"))
        )
        self.assertIn(
            "U-FAIL-1", rules(diff_for("python/a.py", "except: return pl.DataFrame()"))
        )
        self.assertNotIn(
            "U-FAIL-1", rules(diff_for("python/a.py", "    except HTTPError as e:"))
        )
        self.assertNotIn("U-FAIL-1", rules(diff_for("docs/a.md", "except Exception:")))

    def test_retry_count_from_config(self):
        self.assertIn(
            "U-FAIL-6",
            rules(
                diff_for(
                    "python/p.py", "for attempt in range(1, GH_RETRY_ATTEMPTS + 1):"
                )
            ),
        )
        self.assertNotIn(
            "U-FAIL-6", rules(diff_for("python/p.py", "for attempt in range(1, 4):"))
        )

    def test_season_shift(self):
        self.assertIn(
            "U-DATA-1", rules(diff_for("python/b.py", "published = season + 1"))
        )
        self.assertIn(
            "U-DATA-1",
            rules(diff_for("python/c.py", 'url = f"nba_{season+1}.parquet"')),
        )
        self.assertNotIn(
            "U-DATA-1",
            rules(diff_for("python/b.py", "seasons = list(range(a, b + 1))")),
        )

    def test_shell_arithmetic_season_shift_only_in_shell_and_workflows(self):
        # hoopR-nba-stats-data#29: `--season "$((i + 1))"` was the double shift.
        self.assertIn(
            "U-DATA-1",
            rules(diff_for("scripts/daily.sh", '--season "$((i + 1))" --stamp-only')),
        )
        self.assertNotIn(
            "U-DATA-1", rules(diff_for("python/a.py", "total = $((i + 1))"))
        )

    def test_untrusted_expression_in_workflow_but_not_elsewhere(self):
        wf = ".github/workflows/daily.yml"
        self.assertIn(
            "U-CI-2",
            rules(
                diff_for(
                    wf, '  echo "${{ github.event.client_payload.commit_message }}"'
                )
            ),
        )
        self.assertIn(
            "U-CI-2", rules(diff_for(wf, "  run: ./x.sh ${{ inputs.season }}"))
        )
        self.assertNotIn(
            "U-CI-2", rules(diff_for(wf, "  if: github.ref == 'refs/heads/main'"))
        )
        self.assertNotIn(
            "U-CI-2", rules(diff_for("docs/ci.md", "${{ inputs.season }}"))
        )

    def test_token_fallback_and_self_hosted(self):
        wf = ".github/workflows/pub.yml"
        self.assertIn(
            "U-CI-3",
            rules(
                diff_for(
                    wf, "GH_TOKEN: ${{ secrets.SDV_GH_TOKEN || secrets.GITHUB_TOKEN }}"
                )
            ),
        )
        self.assertIn(
            "U-CI-5", rules(diff_for(wf, "runs-on: [self-hosted, sdv-droplet]"))
        )
        self.assertNotIn("U-CI-5", rules(diff_for(wf, "runs-on: ubuntu-latest")))

    def test_credentials(self):
        self.assertIn("U-SEC-1", rules(diff_for("a.py", 'T = "ghp_' + "a" * 36 + '"')))
        self.assertNotIn(
            "U-SEC-1", rules(diff_for("a.py", 'T = os.environ["GITHUB_PAT"]'))
        )

    def test_process_pool_spawn(self):
        self.assertIn(
            "RAW-4",
            rules(
                diff_for(
                    "python/s.py", "with ProcessPoolExecutor(max_workers=4) as ex:"
                )
            ),
        )
        self.assertNotIn(
            "RAW-4",
            rules(
                diff_for(
                    "python/s.py",
                    'with ProcessPoolExecutor(4, mp_context=get_context("spawn")) as ex:',
                )
            ),
        )

    def test_bare_uv_run_only_in_orchestrated_scripts(self):
        self.assertIn(
            "PLAT-ORCH-1",
            rules(diff_for("scripts/pipeline/03_build.sh", "uv run python -m x")),
        )
        self.assertNotIn("PLAT-ORCH-1", rules(diff_for("README.md", "uv run pytest")))

    def test_gop_cache_and_routing(self):
        self.assertIn(
            "GOP-CACHE-1",
            rules(diff_for("astro/src/routes/week.ts", "Astro.cache.set(false);")),
        )
        self.assertIn(
            "GOP-ROUTE-1",
            rules(
                diff_for(
                    "astro/src/components/routes/GameRoute.astro",
                    'return Astro.redirect("/404")',
                )
            ),
        )
        self.assertNotIn(
            "GOP-ROUTE-1",
            rules(
                diff_for(
                    "astro/src/pages/game/[id].astro", 'return Astro.redirect("/404")'
                )
            ),
        )

    def test_vignette_self_install_only_for_the_package_itself(self):
        def r3(text, path="vignettes/a.Rmd", repo="cfbfastR"):
            return [s.rule for s in pc.scan_diff(diff_for(path, text), repo)]

        self.assertIn("R-3", r3('pak::pak(c("dplyr", "cfbfastR"))'))
        # cfbfastR#154's corrected lines install only dependencies -- not a lead.
        self.assertNotIn("R-3", r3('pak::pak(c("dplyr", "tidyr", "gt"))'))
        self.assertNotIn("R-3", r3('pak::pak(c("cfbfastR"))', path="R/zzz.R"))

    def test_comment_lines_skip_leads_but_not_credentials(self):
        # hoopR-nba-stats-data#29 flagged a comment explaining `$((i + 1))`.
        self.assertNotIn(
            "U-DATA-1",
            rules(diff_for("scripts/d.sh", "# $((i + 1)), not ${i}: stages disagree")),
        )
        self.assertIn(
            "U-DATA-1", rules(diff_for("scripts/d.sh", '--season "$((i + 1))"'))
        )
        self.assertIn("U-SEC-1", rules(diff_for("a.py", "# token ghp_" + "b" * 36)))
        self.assertNotIn(
            "U-FAIL-1", rules(diff_for("a.sh", "#!/bin/bash"))
        )  # shebang is not a comment, and not a signal either

    def test_line_numbers_follow_the_new_file(self):
        d = "+++ b/x.py\n@@ -10,2 +20,3 @@\n context\n+ok = 1\n+published = season + 1\n"
        (sig,) = [s for s in pc.scan_diff(d) if s.rule == "U-DATA-1"]
        self.assertEqual(sig.line, 22)

    def test_deleted_file_lines_are_ignored(self):
        d = "--- a/old.py\n+++ /dev/null\n@@ -1 +0,0 @@\n-git push || true\n"
        self.assertEqual(rules(d), [])


def f(name, status="modified"):
    return {"filename": name, "status": status}


def frules(files, repo=""):
    return [s["rule"] for s in pc.file_signals(files, repo)]


class FileSignals(unittest.TestCase):
    def test_gop_v2_change_without_classic_twin(self):
        v2 = f("astro/src/components/game/plays/PlayRow.astro")
        self.assertIn("GOP-TWIN-1", frules([v2]))
        self.assertNotIn(
            "GOP-TWIN-1",
            frules([v2, f("astro/src/components/game/classic/PlayRow.astro")]),
        )
        self.assertNotIn(
            "GOP-TWIN-1", frules([f("astro/src/components/game/classic/PlayRow.astro")])
        )

    def test_lock_without_manifest_and_manifest_without_lock(self):
        self.assertIn("U-DEP-4", frules([f("uv.lock")]))
        self.assertIn("U-DEP-4", frules([f("pyproject.toml")]))
        self.assertNotIn("U-DEP-4", frules([f("uv.lock"), f("pyproject.toml")]))
        self.assertIn("U-DEP-4", frules([f("astro/package.json")]))
        self.assertNotIn(
            "U-DEP-4", frules([f("astro/package.json"), f("astro/package-lock.json")])
        )

    def test_generated_output_without_codegen_input(self):
        gen = f("sportsdataverse/nfl/nfl_espn_ext.py")
        self.assertIn("PY-2", frules([gen]))
        self.assertNotIn("PY-2", frules([gen, f("tools/codegen/endpoints/nfl.yaml")]))
        # Docs regenerate from a public docstring edit (sportsdataverse-py#495).
        self.assertNotIn(
            "PY-2",
            frules(
                [
                    f("docs/docs/nfl/reference/additional.md"),
                    f("sportsdataverse/nfl/nfl_pbp.py"),
                ]
            ),
        )
        # sdv-db's OpenAPI regenerates from the captured schema snapshot (#59).
        self.assertIn("PY-2", frules([f("docs/sdv-data-api.openapi.json")]))
        self.assertNotIn(
            "PY-2",
            frules(
                [
                    f("docs/sdv-data-api.openapi.json"),
                    f("python/src/sdv_db/api/gen/schema_snapshot.json"),
                ]
            ),
        )
        self.assertIn(
            "PY-1", frules([f("tools/codegen/manual_column_descriptions.yaml")])
        )

    def test_deletions_are_listed(self):
        (sig,) = [
            s
            for s in pc.file_signals([f("sportsdataverse/nbagl/x.py", "removed")])
            if s["rule"] == "U-GIT-2"
        ]
        self.assertEqual(sig["paths"], ["sportsdataverse/nbagl/x.py"])

    def test_fixture_readme(self):
        fx = f("tests/fixtures/espn/g1.json", "added")
        self.assertIn("U-TEST-3", frules([fx]))
        self.assertNotIn(
            "U-TEST-3", frules([fx, f("tests/fixtures/espn/README.md", "added")])
        )

    def test_gop_new_python_subpackage(self):
        added = f("python/sql_tools/q.py", "added")
        self.assertIn("GOP-PY-1", frules([added], "game-on-paper-app"))
        self.assertNotIn(
            "GOP-PY-1",
            frules([f("python/espn_proxy.py", "added")], "game-on-paper-app"),
        )

    def test_toolkit_change_without_version_bump(self):
        self.assertIn("TK-1", frules([f("sdv-toolkit/skills/sdv-ship/SKILL.md")]))
        self.assertNotIn(
            "TK-1",
            frules(
                [
                    f("sdv-toolkit/skills/sdv-ship/SKILL.md"),
                    f("sdv-toolkit/.claude-plugin/plugin.json"),
                ]
            ),
        )


class CallerCandidates(unittest.TestCase):
    def test_entry_points_only_and_never_removed_files(self):
        files = [
            f("scripts/daily_nba_stats_python_processor.sh"),
            f("python/nba_03_reshape.py"),
            f(
                "python/nba_data_build/reshape/cli.py"
            ),  # package internals: callers are imports
            f("scripts/old_driver.sh", "removed"),
            f("R/espn_nba_01_pbp_creation.R"),
            f("README.md"),
        ]
        self.assertEqual(
            pc.caller_candidates(files),
            [
                "daily_nba_stats_python_processor.sh",
                "nba_03_reshape.py",
                "espn_nba_01_pbp_creation.R",
            ],
        )

    def test_missing_checkouts_yield_no_callers_rather_than_an_error(self):
        self.assertEqual(
            pc.find_callers("no-such-repo", "main", ["x.sh"], sdv_root="/nonexistent"),
            {},
        )


class ModuleRefs(unittest.TestCase):
    TREE = [
        "python/nhl_data_19_publish.py",
        "python/nhl_data_01_fetch.py",
        "python/nhl_data_build/__init__.py",
        "python/nhl_data_build/season.py",
        "scripts/daily_nhl_python_processor.sh",
    ]

    def test_module_name(self):
        self.assertEqual(
            pc.module_name("python/nhl_data_build/season.py"), "nhl_data_build.season"
        )
        self.assertEqual(
            pc.module_name("python/nhl_data_build/__init__.py"), "nhl_data_build"
        )
        self.assertIsNone(pc.module_name("scripts/run.sh"))

    def test_module_candidates_only_package_roots(self):
        files = [
            f("python/nhl_data_build/season.py"),
            f("tests/test_season.py"),
            f("python/old.py", "removed"),
        ]
        self.assertEqual(pc.module_candidates(files), ["nhl_data_build.season"])

    def test_renamed_stage_is_dangling(self):
        # fastRhockey-nhl-data: stage 03 -> 19 rename left `-m nhl_data_03_publish` behind.
        lines = [
            ("scripts/daily.sh:136", "  python -m nhl_data_03_publish --seasons 2026")
        ]
        (d,) = pc.dangling_module_refs(lines, self.TREE)
        self.assertEqual(d["module"], "nhl_data_03_publish")

    def test_interpreter_variables_count_too(self):
        # The droplet driver calls `"${PYBIN}" -m nhl_data_03_publish`.
        lines = [
            (
                "scripts/d.sh:136",
                '( cd python && "${PYBIN}" -m nhl_data_03_publish -s "${i}" )',
            )
        ]
        self.assertEqual(
            [d["module"] for d in pc.dangling_module_refs(lines, self.TREE)],
            ["nhl_data_03_publish"],
        )

    def test_pytest_markers_are_not_modules(self):
        lines = [("tests.yml:9", 'uv run pytest -m "not archive" -q')]
        self.assertEqual(pc.dangling_module_refs(lines, self.TREE), [])

    def test_existing_modules_and_foreign_tools_are_not_flagged(self):
        lines = [
            ("a.yml:1", "uv run python -m nhl_data_build.season -s 2026"),
            ("a.yml:2", "python -m nhl_data_19_publish"),
            ("a.yml:3", "python -m pytest -q"),
            ("a.yml:4", "python3 -m http.server 8000"),
            ("a.yml:5", "python -u -m nhl_data_01_fetch"),
        ]
        self.assertEqual(pc.dangling_module_refs(lines, self.TREE), [])


class RuleIdsResolve(unittest.TestCase):
    """A signal pointing at a rule id no reference defines is a dead end."""

    SKILL = pathlib.Path(pc.__file__).resolve().parent.parent

    def emitted_ids(self):
        ids = {rule for rule, _rx, _path, _note in pc.LINE_SIGNALS}
        source = pathlib.Path(pc.__file__).read_text(encoding="utf-8")
        ids |= set(re.findall(r'add\(\s*"([A-Z][A-Z0-9-]+)"', source))
        return ids

    def defined_ids(self):
        text = "\n".join(
            p.read_text(encoding="utf-8")
            for p in [
                self.SKILL / "SKILL.md",
                *sorted((self.SKILL / "references").glob("*.md")),
            ]
        )
        return set(
            re.findall(
                r"\*\*([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+|REVIEW-SIZE|U-PATH)\*\*", text
            )
        )

    def test_every_emitted_rule_id_is_defined_in_a_reference(self):
        emitted = self.emitted_ids()
        self.assertGreater(len(emitted), 20)  # the extractor itself must find ids
        self.assertEqual(sorted(emitted - self.defined_ids()), [])

    def test_every_referenced_file_exists(self):
        for ref in set(pc.REFERENCES.values()):
            with self.subTest(ref):
                self.assertTrue((self.SKILL / ref).is_file())


class Headline(unittest.TestCase):
    def test_coderabbit_banner_is_skipped_for_the_bold_title(self):
        body = (
            "_🎯 Functional Correctness_ | _🟠 Major_ | _⚡ Quick win_\n\n"
            "<details><summary>🧩 Analysis chain</summary>rg -n foo</details>\n"
            "**Make `position_group` mandatory for `fantasy_game`.**\n\nMore text."
        )
        self.assertEqual(
            pc.headline(body),
            "[Major] Make `position_group` mandatory for `fantasy_game`.",
        )

    def test_plain_body_falls_back_to_first_substantive_line(self):
        self.assertEqual(
            pc.headline("issue (bug_risk): retry loop never runs"),
            "issue (bug_risk): retry loop never runs",
        )


class ReviewProof(unittest.TestCase):
    HEAD = "abc123"

    def review(self, **kw):
        base = {
            "user": {"login": "coderabbitai[bot]"},
            "state": "COMMENTED",
            "commit_id": self.HEAD,
            "body": "Actionable comments posted: 2",
        }
        base.update(kw)
        return base

    def test_review_at_head_with_body_and_no_threads_counts(self):
        self.assertTrue(
            pc.review_proof([self.review()], self.HEAD, 0)["reviewed_at_head"]
        )

    def test_each_lying_green_signal_reads_unreviewed(self):
        cases = {
            "stale head": [self.review(commit_id="old999")],
            "empty shell": [self.review(body="")],
            "rate limited": [self.review(body="Review rate limited. Try again later.")],
            "human only": [self.review(user={"login": "saiemgilani"})],
            "no reviews": [],
        }
        for label, reviews in cases.items():
            with self.subTest(label):
                self.assertFalse(
                    pc.review_proof(reviews, self.HEAD, 0)["reviewed_at_head"]
                )

    def test_unresolved_threads_block_reviewed(self):
        self.assertFalse(
            pc.review_proof([self.review()], self.HEAD, 3)["reviewed_at_head"]
        )


if __name__ == "__main__":
    unittest.main()
