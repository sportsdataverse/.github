---
name: sdv-api-sync
description: Use to turn an open `api-sync` tracking issue in an SDV R package (cfbfastR for the CFBD API, hoopR for the CBBD API) into a reviewable PR that adds the missing upstream endpoints as wrappers in the package's own style and adds drifted query params to existing wrappers. The issue is opened daily by the reusable `api-spec-sync.yml` workflow in sportsdataverse/.github; this skill is the human-judgement half of that pipeline and is what the `sdv-api-sync` cloud routine runs. Invoke for "sync cfbfastR with the CFBD spec", "add the missing cbbd_ wrappers", "work the api-sync issue", or "/sdv-api-sync <repo-dir> <cfbd|cbbd>". Never deletes a function, never rewrites hand-written @details prose, never closes the issue, never merges.
---

# Work an `api-sync` tracking issue into a wrapper PR

Inputs: `<repo-dir>` (a checkout of cfbfastR or hoopR) and `<fn_prefix>` (`cfbd` or `cbbd`).
The detector already did the diff; this skill writes code the way the package's author would.
Everything below is a contract, not a suggestion: a cloud routine follows it unattended.

## 0. Preconditions (stop conditions)

1. `gh issue list --label api-sync --state open --json number,title,body` in the repo. **No open
   issue: stop, report "nothing to do".**
2. Read the marker `<!-- api-sync: version=X.Y.Z -->` from the body. No marker: stop and report
   "issue #N has no version marker; the detector must refresh it".
3. `gh pr list --state open --head "api-sync/<prefix>-X.Y.Z" --json number,url` and, separately,
   `gh pr list --state open --search "Tracker: #<issue> in:body" --json number,url`.
   **Either returns a PR: stop, report its URL.** The work is in flight. (Do not use `in:head`;
   it is not a search qualifier.)
4. `git status --porcelain` must be empty; `git fetch origin main` then branch from `origin/main`:
   `git checkout -b api-sync/<prefix>-X.Y.Z origin/main`.

## 1. Fetch the spec at the marker version and re-diff

| prefix | spec URL | `--host` (the WRAPPER host, not the spec host) |
|---|---|---|
| `cfbd` | `https://apinext.collegefootballdata.com/api/X.Y.Z/cfbd-openapi.json` | `api.collegefootballdata.com` |
| `cbbd` | `https://api.collegebasketballdata.com/api/X.Y.Z/cbbd-openapi.json` | `api.collegebasketballdata.com` |

Sanity stop: if `counts.missing` is more than half of `spec_operations` (both in
`/tmp/summary.json`), the host or prefix is misconfigured (a wrong host makes every wrapper
invisible). Stop and report; write nothing.

`curl -fsSL <url> -o /tmp/spec.json`, then
`python3 <toolkit>/skills/sdv-api-sync/scripts/api_coverage.py /tmp/spec.json R /tmp/report.md /tmp/summary.json --host <host> --prefix <prefix>`
where `<toolkit>` is this skill's plugin root, or the `sdv-toolkit/` folder of a
`sportsdataverse/.github` checkout when the org repo is available as a source. Work from
`/tmp/summary.json`, not from the issue text; the issue may be a day stale.
If every count is zero: comment `Clean on re-diff at X.Y.Z; nothing to add.` on the issue and stop.

## 2. Read the package's idiom before writing anything

Open the three `R/<prefix>_*.R` files nearest in name to each target tag and copy their shape.
The two packages differ on purpose:

| | cfbfastR (`cfbd_*`) | hoopR (`cbbd_*`) |
|---|---|---|
| request | literal `base_url <- "https://api.collegefootballdata.com/<path>"`; `query_params <- list("year" = year, ...)`; `full_url <- httr2::url_modify(base_url, query = .compact(query_params))`; `res <- get_req(full_url)`; `check_status(res)`; `parsed <- res |> httr2::resp_body_string(encoding = "UTF-8") |> jsonlite::fromJSON(flatten = TRUE)` | `data <- .cbbd_get("/<path>", query = list(season = season, seasonType = season_type, ...))`; path params via `paste0("/games/", game_id, "/preview")` |
| validation | `validate_api_key()`, `validate_year(year)`, `validate_season_type(season_type)`, `validate_division(classification)`, `validate_week(week)`, `validate_id(id)`, `team <- handle_accents(team)`; use the ones the neighbours use for the same param names | none inline; `.args <- .capture_args()` as the first line |
| result | `df <- parsed |> janitor::clean_names()` then `make_cfbfastR_data(df, "<Human label> from CollegeFootballData.com", Sys.time())` | `df <- janitor::clean_names(dplyr::as_tibble(data))` then `make_hoopR_data(df, "CBD <Label> from collegebasketballdata.com", Sys.time())` |
| errors | `tryCatch(expr = {...}, error = function(e) { message(glue::glue("{Sys.time()}: Invalid arguments or no <label> data available! {conditionMessage(e)}")) }, finally = {})`; returns `df` initialised as `data.frame()` | `tryCatch(expr = {...}, error = function(e) { .report_api_error(e, hint = "Invalid arguments or no <label> data available!", args = .args) }, warning = function(w) { .report_api_warning(w, hint = "Warning fetching CBD <label>", args = .args) }, finally = {})` |
| file | `R/<prefix>_<tag>.R` (`cfbd_games.R`, `cfbd_metrics.R`, `cfbd_teams.R`); append at the end | same (`cbbd_games.R`); append at the end |
| naming | `cfbd_<tag singular>_<rest of path, snake_case>`: `/games/schedule` gives `cfbd_game_schedule`; `/games/{gameId}/preview` gives `cfbd_game_preview`; `/games/{gameId}/preview/adjusted` gives `cfbd_game_preview_adjusted`; `/metrics/fg/ep` gives `cfbd_metrics_fg_ep`; `/teams/season/overview` gives `cfbd_team_season_overview`. Singularise the tag where the neighbours do (`cfbd_game_*`, `cfbd_team_*`). | `cbbd_<tag>_<rest>`; check `_pkgdown.yml` redirects for the family's rdname convention |
| formals | snake_case of the spec name; required spec params have no default, optional ones default `NULL`; path params first, then query params in spec order | same; a `season` param defaults to `most_recent_mbb_season()` when the neighbours do |

Spec name to R formal: `seasonType` is `season_type`, `gameId` is `game_id`, `firstName` is `first`
(cfbfastR abbreviates `first`/`last`; keep that only where the file already does).

## 3. Response shape decides the return type

Look at `paths[p].get.responses["200"].content["application/json"].schema` and resolve `$ref`s in
`components.schemas`:

- **array of objects** (e.g. `FieldGoalEP[]`): one tibble via the idiom above. This is the common case.
- **single object whose payload is one array field** (e.g. `GameSchedule{games: ScheduleGame[], window, selection}`):
  tibble of that array; carry the scalar siblings as attributes (`attr(df, "window") <- parsed$window`)
  and say so in `@return`.
- **single object with heterogeneous sections** (e.g. `GamePreview{game, analysis{...}, reason}`,
  `TeamSeasonOverview{record, ratings, advanced, passing, rushing, players}`): a **named list of
  tibbles**, one per top-level section, each passed through `make_<pkg>_data`; scalar sections become
  one-row tibbles. Precedent for flattening a nested payload when a single long tibble IS sensible:
  `cfbfastR/R/cfbd_games.R` `cfbd_game_box_advanced` (`purrr::map_if(is.data.frame, list) |> as_tibble() |> tidyr::unnest("teams")`).
  Prefer that when every section shares the same row grain; otherwise the named list.

Document the choice in `@return` ("A named list of tibbles: `record`, `ratings`, ...").

## 4. Write each missing endpoint

**Before writing any endpoint:** derive its function name (section 2), then
`grep -n "^<fn> <- function" R/*.R`. If it already exists, the detector missed it (an idiom the
script does not recognise). Write nothing for that row; list it in the PR body under
"Already wrapped (detector miss)" with the file:line, so the script gets a fixture. A second
definition of an exported function is a red R CMD check and a PR nobody can merge.

For every remaining row in `summary.missing`, in the tag's file (create `R/<prefix>_<tag>.R` only
if no file for that tag exists, copying the header block of the nearest sibling file):

1. **roxygen**: copy the neighbour's header verbatim in structure:
   `#' @title` / `#' **<Prefix> <Human title>**` / `#' @description` / `#' **<one sentence from the spec summary or, when empty, from the operationId>**`;
   one `#' @param <formal> (*<Type>* required|optional): <spec description, or the enum list>` per formal
   (Type = `Integer`/`String`/`Logical` in cfbfastR, `integer`/`character`/`logical` in hoopR; match the file);
   `#' @return` = the column table in the package's own format: **cfbfastR uses a markdown table
   in roxygen** (`#' |col_name |types |description |` / `#' |---|---|---|` rows, see
   `cfbd_passing.R`), **hoopR uses `\if{html}{\tabular{lll}{ col_name \tab types \tab description \cr ... }}`**
   (see `cbbd_games.R`); copy the neighbour's exact form. Build it from the resolved schema's
   `properties` (snake_case the names; types from
   `type`/`format`; description from the schema when present, else a plain-English reading of the name);
   for a named-list return, one short table per section. If a `$ref` cannot be resolved or a property
   has no `type`, write the rows you can and list the gap under "Schema gaps" in the PR body; never
   invent a column. Then `#' @keywords`, the `#' @importFrom` lines the body needs,
   `#' @family <same family string as the file>`, `#' @export`, and
   `#' @examples` as `\donttest{ try(<fn>(<smallest real args>)) }`.
   **Never touch a neighbour's `@details` / `@section` prose.**
2. **body**: per the idiom table. Query keys are the spec's camelCase names; values the snake_case formals.
3. **test**: append to `tests/testthat/test-<prefix>_<tag>.R` (create it next to the siblings if absent):

   ```r
   test_that("<PREFIX> - <Human title>", {
     skip_on_cran()
     # hoopR only: skip_on_ci(); skip_cbbd_test()
     x <- <fn>(<smallest real args>)
     if (is.null(x) || !is.data.frame(x) || nrow(x) == 0L) skip("<PREFIX> rate-limited or returned no rows")
     cols <- c(<4-8 columns you are sure of from the schema>)
     expect_in(cols, colnames(x))
     expect_s3_class(x, "data.frame")
     # hoopR only: Sys.sleep(1)
   })
   ```

   For a named-list return, assert `expect_type(x, "list")` and `expect_in(c("record", ...), names(x))`.
4. **NEWS.md**: one bullet under the current dev-version heading (the first `#` heading; do not
   change the version): `* Added <fn>() (CFBD /games/schedule, upstream vX.Y.Z).` with the function
   and path in backticks.
5. **_pkgdown.yml**: only if the tag's `contents:` list does not already glob the new name
   (cfbfastR: `starts_with("cfbd_game")`, `starts_with("cfbd_team")`, `starts_with("cfbd_metrics_")` already
   match; hoopR: `starts_with("cbbd_")` matches everything). If not globbed, add the quoted name to that subtitle.

## 5. Add drifted params to existing wrappers

For every row in `summary.drift`: open `<file>`, function `<fn>`. For each `missing_params` name, add a
snake_case formal with default `NULL` at the **end** of the formals, add the camelCase key to the query
list, add a `#' @param` line after the last existing `@param`, and (cfbfastR only) the matching
`validate_*` call if the neighbours validate that param. Change nothing else in that function. If the
name is a pure rename the function already covers under another formal (e.g. `division` for
`classification`), skip it and list it in the PR body under "Skipped drift (already covered)".

`summary.dead` rows: change nothing; list them in the PR body under "Needs a decision (removed upstream)".

## 6. Regenerate docs (Task 0 verdict: installable)

The spike (2026-09-27, cloud `Default` env) found: no R preinstalled; `sudo apt-get install -y -qq r-base-core`
works in ~25 s (R 4.3.3); a CRAN **source** build of roxygen2 fails on missing `libxml2-dev`/`libuv`.
So:

- If `Rscript` is on PATH: `Rscript -e 'roxygen2::roxygenise()'` then `git add man NAMESPACE`.
- Else, with a **10-minute cap** on the whole block:
  `sudo apt-get update -qq && sudo apt-get install -y -qq r-base-core r-cran-roxygen2 r-cran-devtools`
  (Ubuntu binaries; no compilation). `roxygenise()` loads the package, so its `Imports` must be
  installed too. apt aborts the whole transaction on one unknown package name (Ubuntu has no
  `r-cran-httr2`, for example), so install them ONE AT A TIME and tolerate misses:
  `for p in $(sed -n '/^Imports:/,/^[A-Z]/p' DESCRIPTION | grep -oE '^\s+[a-zA-Z0-9.]+' | tr -d ' ' | tr 'A-Z' 'a-z'); do sudo apt-get install -y -qq "r-cran-$p" || true; done`.
  Any Import with no Ubuntu binary will surface as a load error on the next line; that is the
  signal to fall through to the note below, not to start compiling from CRAN. Then
  `Rscript -e 'roxygen2::roxygenise()'`. If it completes: `git add man NAMESPACE`.
- Else (cap hit, or roxygenise errors): do NOT hand-write `man/*.Rd` or edit `NAMESPACE`. Add this block
  to the PR body:
  `> **man/ + NAMESPACE not regenerated** (no R toolchain in this environment). Run roxygen2::roxygenise() locally before merge.`

## 7. Commit, push, PR, hand back

- One commit per endpoint plus one for drift: `feat(<prefix>): add <fn>() — <PREFIX> <path> (v X.Y.Z)`;
  drift: `feat(<prefix>): add <n> upstream query params (v X.Y.Z)`. Conventional Commits; **no AI co-author trailers**.
- `git push -u origin HEAD:api-sync/<prefix>-X.Y.Z` (a cloud checkout sits on a `claude/*` branch: push
  `HEAD:<branch>`, never `origin main`). Verify: `git ls-remote origin api-sync/<prefix>-X.Y.Z`.
  **If the push is rejected (non-fast-forward, branch exists): stop and report.** Never `--force`,
  never rebase onto or reset the remote branch, never open a second PR: a rejected push means a
  human-reviewed branch already exists and stop condition 3 should have caught it.
- `gh pr create --title "feat(<prefix>): <PREFIX> X.Y.Z — <n> new wrappers, <m> drift params" --body-file /tmp/pr.md`
  where `/tmp/pr.md` holds: `Tracker: #<issue>` (a plain reference, NOT a `Closes #` keyword; the detector closes it),
  the missing table from `/tmp/report.md` with a done / skipped / needs-decision column, the drift
  table likewise, the return-shape choice per endpoint (section 3), and any section-6 note.
- `gh issue comment <issue> --body "PR opened: <url> (adds <n> wrappers, <m> drift params)"`.
- Final message: the PR URL and the three counts. Do not close the issue. Do not merge.
