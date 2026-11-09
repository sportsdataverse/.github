"""Tests for skills/sdv-repo-audit/scripts/check_r_readme.py.

Run: python -m unittest discover -s tools -p 'test_*.py'

Offline: check_file() takes the backing as a ctx dict, so no CRAN / R-universe / GitHub
call is made. One compliant README passes, and each rule has a README that breaks only
that rule -- a check that never fails teaches the auditor to trust it.
"""

import pathlib
import sys
import tempfile
import unittest

TOOLKIT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLKIT / "skills" / "sdv-repo-audit" / "scripts"))

import check_r_readme as crr  # noqa: E402

GOOD = """# **pkgx** <a href='https://pkgx.sportsdataverse.org/'><img alt="pkgx hex logo" src='logo.png' align="right"/></a>

<!-- badges: start -->
[![CRAN version](https://img.shields.io/cran/v/pkgx)](https://CRAN.R-project.org/package=pkgx)
[![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/pkgx)](https://CRAN.R-project.org/package=pkgx)
[![R-universe](https://img.shields.io/badge/r-universe-x)](https://sportsdataverse.r-universe.dev/pkgx)
[![Version-Number](https://img.shields.io/github/r-package/v/sportsdataverse/pkgx)](https://github.com/sportsdataverse/pkgx/)
[![R-CMD-check](https://img.shields.io/badge/check-x)](https://github.com/sportsdataverse/pkgx/actions)
[![Codecov](https://img.shields.io/codecov/c/github/sportsdataverse/pkgx)](https://app.codecov.io/gh/sportsdataverse/pkgx)
[![pkgdown](https://img.shields.io/badge/pkgdown-x)](https://github.com/sportsdataverse/pkgx/actions)
[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-brightgreen.svg)](https://lifecycle.r-lib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/sportsdataverse/pkgx/blob/main/LICENSE.md)
[![Contributors](https://img.shields.io/github/contributors/sportsdataverse/pkgx)](https://github.com/sportsdataverse/pkgx/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/sportsdataverse/pkgx)](https://github.com/sportsdataverse/pkgx)
[![X Follow](https://img.shields.io/twitter/follow/SportsDataverse)](https://x.com/SportsDataverse)
<!-- badges: end -->

The goal of pkgx is to test.

## **Installation**

```r
install.packages("pkgx")
install.packages("pkgx", repos = c("https://sportsdataverse.r-universe.dev", getOption("repos")))
pak::pak("sportsdataverse/pkgx")
# if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
# remotes::install_github("sportsdataverse/pkgx")
```

## **Quick start**

## **Documentation**

## **Companion packages**

## **The SportsDataverse**

## **Follow the [SportsDataverse](https://x.com/SportsDataverse) on X and star this repo**

## **Our Authors**

- [Saiem Gilani](https://x.com/saiemgilani)

## **Citations**

## **License**
"""

CTX = {
    "pkg": "pkgx",
    "slug": "sportsdataverse/pkgx",
    "version": "1.2.0",
    "major": 1,
    "cran": True,
    "runiverse": True,
    "wf_check": True,
    "wf_cov": True,
    "wf_pkgdown": True,
    "cheatsheet": False,
    "coc": False,
    "aut": ["Gilani"],
}


def errors(text, **ctx):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "README.md"
        p.write_text(text, encoding="utf-8")
        errs, _warns, _heads = crr.check_file(p, {**CTX, **ctx})
    return errs


class CheckRReadmeTest(unittest.TestCase):
    def test_compliant_readme_passes(self):
        self.assertEqual(errors(GOOD), [])

    def test_plain_heading_fails(self):
        self.assertTrue(
            any(
                "not bold" in e
                for e in errors(GOOD.replace("## **Quick start**", "## Quick start"))
            )
        )

    def test_missing_section_fails(self):
        self.assertTrue(
            any(
                "Documentation" in e
                for e in errors(GOOD.replace("## **Documentation**\n", ""))
            )
        )

    def test_twitter_link_fails(self):
        self.assertTrue(
            any(
                "twitter.com" in e
                for e in errors(GOOD + "\n[x](https://twitter.com/SportsDataverse)\n")
            )
        )

    def test_stargazers_link_fails(self):
        bad = GOOD.replace(
            "](https://github.com/sportsdataverse/pkgx)\n[![X",
            "](https://github.com/sportsdataverse/pkgx/stargazers)\n[![X",
        )
        self.assertTrue(any("stargazers" in e for e in errors(bad)))

    def test_logo_without_alt_fails(self):
        self.assertTrue(
            any(
                "alt text" in e
                for e in errors(GOOD.replace('alt="pkgx hex logo" ', ""))
            )
        )

    def test_cran_badge_without_cran_fails_and_missing_badge_fails(self):
        errs = errors(GOOD, cran=False)
        self.assertTrue(any("CRAN version' has no backing" in e for e in errs))
        no_codecov = GOOD.replace("[![Codecov]", "[![NotCov]")
        self.assertTrue(any("missing badge 'Codecov'" in e for e in errors(no_codecov)))

    def test_self_hosted_coverage_badge_counts_as_codecov(self):
        self.assertEqual(errors(GOOD.replace("[![Codecov]", "[![Coverage]")), [])

    def test_lifecycle_follows_version(self):
        self.assertTrue(
            any("experimental" in e for e in errors(GOOD, version="0.3.0", major=0))
        )

    def test_remotes_fallback_needs_remotes_install(self):
        bad = GOOD.replace(
            '# if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")\n',
            "",
        )
        self.assertTrue(any("installing remotes first" in e for e in errors(bad)))

    def test_cheat_sheet_section_without_live_pdf_fails(self):
        bad = GOOD.replace("## **Citations**", "## **Cheat sheet**\n\n## **Citations**")
        self.assertTrue(any("Cheat sheet section" in e for e in errors(bad)))

    def test_single_quoted_person_authors_are_read(self):
        self.assertEqual(
            crr.aut_families("c(person('Saiem', 'Gilani', role = c('aut', 'cre')))"),
            ["Gilani"],
        )

    def test_combined_cheat_sheet_names_the_package(self):
        self.assertIn("cfbplotR-cfb4th-cfbseedR", crr.combined_sheets("cfb4th"))
        self.assertEqual(crr.combined_sheets("hoopR"), [])


if __name__ == "__main__":
    unittest.main()
