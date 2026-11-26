# check_claims fixtures

Real excerpts, copied verbatim (trimmed to the lines named) from public repos
before the fix landed. `tools/test_check_claims.py` builds a temp repo from
each one. Do not edit them to make a test pass.

| Fixture | Source | What the check must do |
|---|---|---|
| `cfbfastR/R/cfbd_api_key.R` | sportsdataverse/cfbfastR `a4ea625`, `R/cfbd_api_key.R` lines 1-10 | T1 flags line 8 (a roxygen bullet naming a function no file defines) and resolves lines 7, 9 and 10 |
| `cfbfastR/NAMESPACE` | same commit, the three `export()` lines for the key helpers | the exports line 7, 9 and 10 resolve against |
| `sdvplotR/.github/ISSUE_TEMPLATE/data_issue.md` | sportsdataverse/sdvplotR `3054c50`, whole file | T1 flags line 34 (a call in a code fence that `NAMESPACE` lacks) and resolves line 35 |
| `sdvplotR/NAMESPACE` | same commit, whole file | |
| `ledger/progress.md` | one line of a progress ledger | T2 stays green: the path's next sentence says the file does not exist |
| `foreign/R/geom_sdv_headshots.R` | sportsdataverse/sdvplotR `4043700`, `R/geom_sdv_headshots.R` lines 9-13 | T1 stays green: each unqualified name follows a `pkg::name()` span it is chained to |
| `foreign/R/court_coords.R` | same commit, `R/court_coords.R` lines 5-8 | T1 stays green: `hoopR's/wehoop's` owns both names after it |
| `foreign/.github/PULL_REQUEST_TEMPLATE.md` | sportsdataverse/hoopR `aba3054`, its pull-request template, lines 48-55 | T2 stays green: the example paths sit inside an HTML comment |

The `cfbfastR` and `sdvplotR` `DESCRIPTION` files hold only the `Package:` and
`Title:` lines of the same commits; `foreign/DESCRIPTION` and `foreign/NAMESPACE`
are one line each, enough to make the fixture an R package.
