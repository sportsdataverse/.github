---
name: sdv-r-coverage
description: Use to raise test coverage of a SportsDataverse R package (cfbfastR, hoopR, wehoop, baseballr, fastRhockey, oddsapiR, …) or to set up its coverage badge — "improve coverage", "why is coverage so low", "add a Codecov badge", "the coverage badge says unknown", "add offline tests". Reads per-file coverage from the CI run and ranks zero-coverage function families by lines; finds why each is zero (no tests, tests gated off on CI, skip_on_ci); records live httr2 responses once and replays them offline (URL-indexed fixtures, arrays trimmed with a "# keep" escape, explicit seasons) so wrapper tests run on CI with no network; triages wrappers that return 0 rows into upstream-empty vs dead route vs parser bug (renamed keys, moved routes, warnings swallowed by tryCatch(warning =)); installs the house test-coverage workflow (env mirrors R-CMD-check, non-fatal Codecov upload) or the self-hosted shields-endpoint badge when Codecov can't be set up. Took baseballr from 21.3% to 68.1% (2026-11-09). Not for Python (sdv-py has its own harness) and never for stats.ncaa.org / stats.nba.com wrappers, which must not be scraped to build fixtures.
---

# Raise an SDV R package's test coverage

Inputs: `<pkg>` checkout (a fresh clone, never the user's working copy), `<slug>`
(`owner/repo`), the id of the latest `test-coverage` run on the default branch.
Scripts are in this skill's `scripts/`; templates in `templates/`.

## 1. Measure where the uncovered lines are — by lines, not files

```bash
python <skill>/scripts/ci_coverage.py --repo <slug> --run <run-id> --src <pkg> --out ci_cov.csv
```

It prints the total and the zero-coverage lines per function family. Work the
largest family first: in baseballr one family (`espn_`, 11,249 lines) was 58% of the
whole package and had 0%.

For each big zero family, find out **why** before writing anything:

| Cause | Check | Fix |
|---|---|---|
| no tests at all | `ls tests/testthat \| grep <family>` | record/replay tests (step 2) |
| tests gated off on CI | the skip helper's env flag isn't in the workflow `env:` | record/replay; don't flip live flags on for CI |
| `skip_on_ci()` in the test | `grep -l skip_on_ci tests/testthat` | record/replay |
| pure function, needs data | function takes a data frame | a small recorded `.rds` (one game) under `tests/testthat/fixtures/` |

## 2. Record once, replay offline

1. Copy `scripts/record_fixtures.R` and `scripts/generate_tests.R` to
   `data-raw/http_fixtures/` (it's `.Rbuildignore`d) and `templates/helper-http_fixtures.R`
   to `tests/testthat/`.
2. Build `data-raw/http_fixtures/calls.txt`, one call per line. Seed it from the Rd
   examples (`grep -ohE '^\s*try\((<prefix>_[a-z_]+\(.*\))\)' man/*.Rd`), then add calls for
   exports with no example from their formals, using ids you've seen work. **Pass every
   season / date argument explicitly** — a `most_recent_season()` default moves the URL and
   the fixture stops matching next year.
3. `Rscript data-raw/http_fixtures/record_fixtures.R [candidates.txt]` (background it; it
   paces requests). It performs each request through httr2 itself, so per-source user
   agents and headers still apply (FanGraphs' `okhttp` UA, Fox's `Origin`). JSON arrays
   are trimmed to 5 items **before the function sees them**, so a call only counts as
   recorded if it returns data on the trimmed fixture. Parsers that need every element
   (play-by-play, standings) go in with a trailing `# keep`; a keep call refetches a URL an
   earlier call saved trimmed. Only successful calls stay in `calls.txt`; unused responses
   are dropped.
4. `Rscript data-raw/http_fixtures/generate_tests.R` writes `test-<source>_offline.R`, one
   `test_that()` per call. Every test opens with `skip_on_cran()` (CI sets `NOT_CRAN=true`,
   so they still run there).
5. A function that reads a second source inside (e.g. `statline_from_statcast()` fetches
   `fg_guts()`) needs that call recorded too and `local_http_fixtures()` in its test.

**Never record stats.ncaa.org, stats.nba.com / stats.wnba.com or Sports Reference** —
they IP-ban scrapers. Leave those families at their live-gated tests.

## 3. Verify offline, then measure

```bash
# every request the code makes must be answered by a fixture -- break the network to prove it
http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 \
HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 NOT_CRAN=true \
  Rscript -e 'devtools::load_all(); testthat::test_dir("tests/testthat", filter = "offline")'
Rscript <skill>/scripts/measure_coverage.R <pkg> "offline" ci_cov.csv
R CMD build --no-build-vignettes . && R CMD check --no-manual <pkg>_*.tar.gz
```

Report the combined number as "at least N%" (it's a lower bound) and confirm it from the
first `test-coverage` run on the default branch after merge. Keep the built tarball under
CRAN's 5 MB: baseballr's 195 fixtures were 755 KB, tarball 1.07 MB.

## 4. Triage wrappers that come back empty

Recording surfaces wrappers that return 0 rows even with good ids. Run
`scripts/request_log.R <pkg> zero.txt`; each call falls in one bucket:

- `200` with `items[0]` / `[]` → upstream has nothing for these args. Try other args or
  accept it; the function is correct.
- `400` / `404` → route or id is dead upstream. Swap the example id if one works; else list
  it as source-side in the PR.
- `200` **with data** but 0 rows → **parser bug**. Seen in baseballr: ESPN moved a lineup
  from `items` to `entries` + `pitchers`; a site-v2 route started answering with an empty
  body while the core-API route still served it; and a harmless `data.frame()` warning
  swallowed by `tryCatch(warning = )` (step 5). Fix it and add the call to `calls.txt`.

## 5. Failure modes and the assertion that catches each

| Failure mode | Assertion |
|---|---|
| `tryCatch(warning = )` unwinds, so any warning returns the empty default with no error | a test whose mocked response triggers a warning still gets rows; the fix is a calling handler (`templates/utils_try_catch.R`'s `.try_catch()` keeps the `tryCatch` signature). Do not convert calls that use the warning as a fallback signal (e.g. a "not installed" check) |
| a recorded call passes on a fixture the function never reads | the dead-proxy run above — an unrecorded URL gets a 404 and the test fails |
| fixture drifts from the URL the code builds | explicit season/date args in `calls.txt`; a 404 from the replay helper names the URL |
| trimming breaks a parser | the recording run itself returns 0 rows for that call → add `# keep` |
| an empty-payload branch untested | a hand-written test that mocks `{"<key>": []}` and expects the documented empty frame |

## 6. The coverage workflow and badge

- **Org repos**: `templates/test-coverage.yaml` — covr with `NOT_CRAN=true`, the **same
  test env vars as that repo's `R-CMD-check.yaml`** (copy them; a secret-gated repo also
  gets the fork-PR guard `if:`), and a `continue-on-error` Codecov upload using the org
  `CODECOV_TOKEN`. A workflow that only uploads an artifact leaves the Codecov badge at
  "unknown" — check for a `codecov/codecov-action` step, not just the file name.
- **Repos outside the org** whose owner can't add a Codecov token (Codecov answers
  `"Repository not found"`): `templates/test-coverage-with-badge.yaml` adds a master-only
  `badge` job (`contents: write`) that writes a shields endpoint JSON to `coverage.json` on
  a `badges` branch, and the README uses
  `https://img.shields.io/endpoint?url=<raw badges/coverage.json>`. The README checker
  accepts a `Coverage` badge in place of `Codecov`.
- A package with no `tests/testthat` gets no coverage workflow and no Codecov badge.

## 7. Ship

Branch + PR per repo; one logical change per commit (fixes, docs/examples, test tooling).
Regenerate `man/` with the roxygen2 version the repo pins (`Config/roxygen2/version`) —
another version rewrites every Rd. Add a NEWS "Tests" entry and list the bug fixes.
Then `sdv-repo-audit`'s README checker if the badge changed.
