---
name: sdv-conventions
description: Use when working in any SportsDataverse repo to load that repo archetype's binding conventions — the rules that differ between sdv-py, a -raw producer, a -data producer, and an R package, and that are the usual source of drift when moving between repos. Loaded automatically by the SessionStart router; invoke directly for "what are the conventions here", "what applies in this repo", "repo rules", or when a convention question arises mid-task. Reference files: sdv-py (polars 1.x surface, codegen is never hand-edited, manual_column_descriptions.yaml is the only place returns descriptions live, ID/join-key dtype discipline, mypy ratchet), raw (scraping-only, committed per-game JSON, rate discipline), data (NN_ stage numbering is intended build order not run order, idempotent re-runs, scripts earn scripts/ only via runbook wiring, models need registry rows), r-package (roxygen completeness, pkgdown reference coverage, tibble returns, snake_case). Also carries UNIVERSAL rules that apply in every archetype — validate the instrument, not just the result (a measurement that drives an action must carry a control, a reconciliation, or a negative case before it is reported, and a selector that narrows silently is worse than no selector); the shared-checkout collision protocol (gh pr list for your item before writing code, rebase-and-drop rather than force-push, never git reset --hard in a shared worktree); and the Windows file-rewrite hazards that turn a small diff into an unreviewable one (pathlib read_text/write_text flipping LF to CRLF, format-on-save reflowing untouched files, MSYS mangling leading-slash git arguments, and a pipe swallowing the exit code).
---

# SDV conventions — archetype packs

One reference file per repo archetype. Load only the one that matches the
repo you're in — these are the rules that DIFFER between archetypes, not a
full style guide.

| Archetype | File |
|---|---|
| sdv-py (the Python package) | `references/sdv-py.md` |
| `-raw` producer (scrape → commit JSON) | `references/raw.md` |
| `-data` producer (build → publish parquet) | `references/data.md` |
| R package (cfbfastR, hoopR, wehoop, …) | `references/r-package.md` |

## Universal — validate the instrument, not just the result

Applies in every archetype. **A measurement that drives an action carries one
of these three before it is reported or acted on:**

- **A control** — run the instrument where the answer is already known. A
  sibling repo that is already correct, or the published artifact, is usually
  sitting right there.
- **A reconciliation** — decompose the number and check the parts sum. If a
  total cannot be broken into parts that add up, it is not yet a fact.
- **A negative case** — confirm the glob/regex/filter EXCLUDES what it should
  and INCLUDES what it should. Exclusion is the side nobody checks, and it is
  where these fail.

This is the same discipline the gates already demand (guard-the-guard, mutation
proof, vacuous-pass floors) turned on your own ad-hoc greps. Real failures it
would have caught, all from one 2026-08-07 session:

| Claim | Why it was wrong |
|---|---|
| "38,900 surplus manifest rows" | the glob counted a 31k-row × 78-col DATASET that merely shared the filename suffix; real figure 1,929 |
| "these duplicate rows are corruption" | they were an intentional append LOG; `publish` collapses to one row per season. The published asset — a perfect control — was clean the whole time |
| "`tools.validation` is importable here" | `find_spec` succeeded; the actual import failed on a dev-only dep |
| "the R files are dead code" | read correctly, intent inverted — git showed a commit *restoring* them |
| a `\bnba\b` sed | silently left `nba_*` untouched (`_` is a word char) |

Corollary: **a check that narrows silently is worse than no check.** A filter
that quietly stops matching leaves every downstream assertion passing
vacuously, which reads greener than before while testing less. Whenever you
add a selector, add the assertion that fails when it selects nothing — or
selects too little.

### Positive control before absence

Those three cover a number that is wrong. The inverse is worse: **a null, empty,
or absent result is not evidence of absence until a known-positive case proves
the pipeline works in the same session.** Absence raises no error and reads as a
clean answer, so nothing prompts you to check. Four shapes, all 2026-08-12:

| Absence read as fact | What a control showed |
|---|---|
| `stats.nba.com` returned nothing for `drafthistory` | it **hangs** rather than errors, so a timeout and "no data" are the same bytes; a `franchisehistory` call in the same session proved the transport healthy and exposed a wrong `"barren"` catalog label that had blocked a wrapper → discovery → capture → dataset → model chain for years |
| 239 of 362 ESPN roster fetches came back empty | ESPN soft-throttles rapid sequential calls with **HTTP 200 and the `athletes` array simply absent** — zero exceptions, so no per-item `except` could have logged it; a paced re-run returned 0 empty |
| two NBA Finals games "missing from the raw store" | they were never played — the control was a demonstrably-played game in the same bracket also reading `0-0`, proving a pre-series snapshot |
| `remote_assets()` returned `{}` | it returns `{}` for BOTH "release absent" and "release empty", so a dry run planned uploads against a nonexistent tag and aborted mid-publish |

Cheapest form: one call whose answer you already know, through the same
transport, in the same session — run BEFORE reporting the absence, not after
someone doubts it.

## Universal — shared checkouts have no author affordance

Every agent commits as the same author, so `git log` cannot tell them apart.
Five agents in one checkout produced a reverted mid-flight edit, a test run that
passed **only because it started before the revert**, and four rounds of mutual
misattribution. Per-worktree reflogs (`.git/worktrees/<name>/logs/HEAD`) localize
WHERE a change came from; nothing localizes WHO.

- Work in your own worktree. Concurrency in one checkout is the whole problem.
- Never infer an author from commit adjacency — say "an agent I can't identify."
- A green run is evidence only about the tree as it stood when the run STARTED.
  Re-run after any concurrent write, and record the HEAD you tested.

**Collision protocol** — three rules, each paid for on 2026-09-01/02:

1. **`gh pr list` for your assigned item BEFORE writing any code.** Two agents
   collided on one stocktake item under *different* branch names, so nothing
   keyed on branch naming or worktree state caught it; one had built a complete
   implementation before finding the PR opened three minutes earlier.
   One search per target repo is the whole check — `gh pr list` defaults to the
   *current* repo, so `--repo` is required, and the item usually spans siblings:

   ```sh
   for r in sportsdataverse/sportsdataverse-py sportsdataverse/<sibling>; do
     gh pr list --repo "$r" --state open --search "<the item's subject>" \
       --json number,title,url
   done
   ```

   On finding one, **verify it and contribute the missing half** — do not
   duplicate it.
2. **Rebase and drop your superseded commits — never force-push.** When another
   session lands on your branch first, keep their work and drop the commits of
   yours that are equivalent-but-second, keeping only what they missed. Also
   re-check `git rev-parse origin/<branch>` immediately before the first edit
   *and* again before pushing.
3. **Never `git reset --hard` in a worktree another agent may share.** Unstaged
   edits are unrecoverable — no stash, no reflog blob. To drop your own commit
   use `git reset --soft/--mixed`, or `git checkout -- <your path>` for a single
   file. Save long-lived uncommitted work as a patch beside the ledger, not only
   in a transcript.

## Universal — on Windows, the tool rewrites files you did not edit

Four mechanisms turn a small change into a huge diff or a wrong command, all
recurring across these repos. The cost is not cosmetic: a 20-line diff arriving
as 300 lines is unreviewable, and it buries the real change.

- **`pathlib.read_text()` / `write_text()` round-trips flip LF → CRLF** (reads
  with universal newlines, writes with `os.linesep`). A 9-line qmd edit shipped
  as a 333-line diff; a 3-line `.gitignore` addition as a 9-line one; ~120 real
  lines as 1,650. **These repos genuinely mix conventions** — some files are
  CRLF in the index — so "normalize everything to LF" is also wrong. Use the
  Edit tool, or byte-level I/O that splices at a byte anchor and takes the
  surrounding line's own EOL. Check with `git ls-files --eol <path>` first.
- **Format-on-save and `ruff check --fix <dir>` reflow files you never
  touched.** Scope autofix to the paths you edited, stage explicit paths, and
  `git checkout --` the incidental churn. A `PostToolUse` formatter can also
  silently *revert* an edit to a scratch script — verify a scratch-file edit
  landed before consuming it, exactly as you would a commit.
- **Git Bash MSYS mangles leading-slash arguments.** `git sparse-checkout set
  '!/ncaa/'` became `!C:/Program Files/Git/ncaa/`, emptying the index and
  staging ~510k deletions (cost a worktree rebuild); `git cat-file -e
  origin/main:<path>` became `origin\main;<path>` and tested a garbage ref. Use
  cone mode with bare directory names, or prefix `MSYS_NO_PATHCONV=1`.
- **A pipe swallows the exit code.** `cmd | tail; echo RC=$?` reports *tail's*
  rc — a failed push printed `PUSH=0`. Same shape as `cmd | tail || fallback`,
  where the fallback never runs. This has silently skipped a `uv add` and a
  push. Use `${PIPESTATUS[0]}`, or run the command unpiped. Corollary: never end
  a verification chain with a `grep -c`, whose rc-1-means-no-matches makes
  "clean" read as FAILED.

**Before committing, read `git diff --numstat`** and flag any file whose
deletions ≈ its line count — that is a line-ending flip or a mass reformat, not
your change.

For the full producer lifecycle (not just the differing rules), see
`sdv-data-pipeline`. For documentation surface, see `sdv-document`.
