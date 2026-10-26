---
name: sdv-repo-audit
description: Use to audit a whole SportsDataverse repo's documentation, currency and public polish at one commit, read-only — after a big merge or layout move, before a release, or when asked "is the README/CONTRIBUTING/CHANGELOG still true", "are we behind on the release or deps", "what does the site look like to a stranger", "docs audit", "polish pass", "currency check". Works on R, Python and JS/TS libraries, DB/API services and web apps: detects the archetype (sdv-py, python-package, r-package, -raw/-data producer, js-package, web-app, db-service; mixed repos get a primary plus secondaries, and every matching reference loads), runs five lenses in parallel through the sdv-repo-auditor agent — contributor docs and templates checked claim-by-claim against the code, companion-package integration (sdvplot/sportypy, cfbplotR/nflplotR/sportyR), front-page coverage against the registries, currency (release vs PyPI/CRAN/npm vs tags vs GitHub Releases, outdated deps, OSV advisories in the lock, docs/MCP index freshness, CI and crons on main), and public polish ranked by visibility (live pages, leaked internal content, metadata/SEO, root clutter, README header, repo description/topics) — and synthesizes a verdict table plus cleanup in PR-sized batches. Never edits; each fix batch is tier 1, confirmed separately. Not for reviewing one PR (sdv-review-pr), the issue queue (sdv-triage), or dataset propagation (sdv-dataset-lifecycle).
---

# sdv-repo-audit — is everything this repo says about itself still true?

A repo drifts in public. After a layout move or a 700-commit stretch without a release,
the README quotes counts from three releases ago, CONTRIBUTING calls an unpublished
version "the newest release", the bug template asks for an attribute that doesn't
exist, the lock carries a critical advisory, and a docstring renders a private repo
name onto the live site. No CI gate sees any of it. This skill measures all of it at
one commit and hands back **verified findings with file:line, evidence and fix**,
grouped into PRs someone can actually land.

Worked example: the 2026-10-26 sdv-py audit after #1020 (five lenses, ~1,000 lines of
findings, eight cleanup batches). The lens checklists in `references/` are that audit
generalized; its headline finds are the red flags below.

## Authorization

| Tier | Action | Authorization |
|---|---|---|
| 0 | Read the repo; create a detached audit worktree; run `scripts/audit_probes.py`; read-only network (registry JSON, `git ls-remote`, `gh api` GETs, OSV queries, fetching live site pages); dispatch auditors; write the report directory | Autonomous |
| 1 | Any fix: edit files, branch, commit, push, open a PR, cut a release, `gh repo edit` (description/topics), toggle Dependabot, open or close issues | **Explicit confirmation, per batch** |

The audit never edits the repo it audits — not a typo, not a dead link. A fix found
mid-audit becomes a finding. After a batch is confirmed, it lands through `/sdv-ship`
(branch + PR, codegen regen first in sdv-py).

## Safety — every phase, every auditor

- **Never call stats.nba.com, stats.wnba.com, stats.ncaa.org or Sports Reference** from
  the audit, directly or through the package (their wrappers, live tests, notebooks). They
  block datacenter IPs and hang; a claim about them is verified statically.
- Keep `SDV_PY_LIVE_TESTS` and `SDV_PY_NBA_STATS_LIVE` (and every other live-test toggle)
  **unset**.
- Repo code runs only inside `sdv-review-pr`'s `scripts/sandbox.sh` (no network, no
  secrets), or not at all. Outside it, verify a command statically or with a read-only
  `--help` / `--check`.
- `--frozen` on every uv command (`uv run --frozen --no-sync`, `uv tree --frozen`): any uv
  command without it can re-lock `uv.lock`.

## Phase 0 — Scope and archetype

```sh
python <this-skill-dir>/scripts/audit_probes.py archetype <repo>
```

It prints a **primary** archetype, any **secondary** ones, the evidence for each, and
the reference files to load. Rows are in precedence order: the first that matches is
primary; every other match is a secondary.

| # | Archetype | Detected by | Example | Reference |
|---|---|---|---|---|
| 1 | `sdv-py` | `tools/codegen/generate.py` (implies `python-package`) | sportsdataverse-py | `python-package.md` (+ its sdv-py rows) |
| 2 | `producer` | repo name ends `-raw` / `-data` | cfbfastR-cfb-data | `producer.md` |
| 3 | `r-package` | `DESCRIPTION` + `R/` | hoopR | `r-package.md` |
| 4 | `js-package` | published `package.json` (not `private`, with `main`/`module`/`exports`/`types`/`bin`), or npm/pnpm workspace members that are; TypeScript included | sportsdataverse-js, sdvplot-js | `js-package.md` |
| 5 | `web-app` | framework dependency or config (`next`, `astro`, `@docusaurus/core`, `@sveltejs/kit`, `remix`, `nuxt`, a vite app with `index.html`) at the root — or one level down when the root has **no** manifest | blazing-the-nets, game-on-paper-app (`astro/`) | `web-app.md` |
| 6 | `db-service` | migrations (`alembic/`, `migrations/`, `*.sql`) or systemd units, plus an API server dependency (FastAPI, Express), a Dockerfile/compose file, a catalog, or more such files; outranks `python-package` | sdv-db | `db-service.md` |
| 7 | `python-package` | `pyproject.toml` / `setup.py` | sdvplot | `python-package.md` |
| 8 | `web-app` (secondary) | a framework site one level down in a repo that has a root manifest: a docs site | sdv-py `docs/`, sdvplot `docs/` | `web-app.md` |
| 9 | `other` | none (papers, the toolkit itself) | | the closest reference; say which |

**Mixed repos load every reference the probe lists** (sdv-py: `python-package.md` +
`web-app.md`; cfbfastR-cfb-data: `producer.md` + `r-package.md` + `python-package.md`;
game-on-paper-app: `web-app.md` + `db-service.md`). Each auditor runs its lens section from
every listed file and labels a finding with the archetype whose checklist produced it.

These rules are the probe's own (the SessionStart router's archetypes differ: it splits
`raw`/`data` and knows no `js-package`, `web-app` or `db-service`). A repo instruction file (`CLAUDE.md`,
`AGENTS.md`, `CONTRIBUTING.md`) that contradicts a reference wins for that repo; record
the conflict.

Ask (or take from the request) which lenses and which questions. Default: all five.

## Phase 1 — Pin the commit

Audit one SHA, never a moving checkout:

```sh
git -C <repo> fetch origin main
SHA=$(git -C <repo> rev-parse --short origin/main)                      # goes in every report header
W=<repo>/.worktrees/audit-$(date +%Y%m%d)-$SHA                           # unique per audit: no collision with another session's
git -C <repo> worktree add --detach "$W" "$SHA"                          # read-only by convention
```

Without a local checkout, export with `git archive` or audit over `gh api` (slower; say
so in the header). Report directory, first that applies:
1. the path the user names;
2. `<repo>/dev/<YYYY-MM-DD>-repo-audit/` when `git check-ignore -q dev/x` succeeds
   (sdv-py's convention — gitignored working notes);
3. `$SCRATCH/repo-audit/<repo>-<YYYY-MM-DD>/`.

Never a tracked path. Note the main checkout's `git status --short` and `uv.lock` /
`renv.lock` hash before and after: an audit that re-locked or dirtied the tree has
edited the repo (`uv run` re-locks silently).

## Phase 2 — Probes (mechanical leads)

Run these once, in the audit worktree, before dispatching; write each to
`<report-dir>/probes/<name>.md` and hand the paths to the auditors. Probe hits are
**leads**: each becomes a finding only after a human-readable check of the line.

Substitute before running: pick **one** registry flag per `release` run and run `osv`
once per lockfile the repo has (the alternatives are listed in the comments). A mixed repo
runs `release` once per published artifact (an R package and its PyPI twin are two runs).
A probe that exits 2 (a missing path, a lockfile with 0 packages, an unsupported lockfile)
is a probe failure to fix, never an empty result.

```sh
P=<this-skill-dir>/scripts/audit_probes.py; O="<report-dir>/probes"   # W and SHA from Phase 1
mkdir -p "$O"
python "$P" archetype "$W"                          > "$O/archetype.md"
python "$P" release   "$W" --pypi <dist>            > "$O/release.md"   # or: --cran <pkg> / --runiverse <owner> / --npm <pkg> / --workspaces
python "$P" fragments "$W"                          > "$O/fragments.md" # changelog.d/, .changeset/, NEWS.md; option: --dir <dir>
python "$P" leaks     --root "$W"                   > "$O/leaks.md"     # option: --private <extra names>
python "$P" counts    --root "$W"                   > "$O/counts.md"
python "$P" osv       "$W/uv.lock"                  > "$O/osv.md"       # or: renv.lock / package-lock.json / pnpm-lock.yaml / yarn.lock / poetry.lock / requirements.txt
```

| Probe | Checks | Known blind spots |
|---|---|---|
| `release` | local version vs PyPI / CRAN / r-universe / npm vs tags (by name, not "newest": sdv-py carries old-line `0.36.0`/`0.37.0` tags) vs GitHub `Latest`; `--workspaces`: every published member vs npm vs its `@scope/pkg@x.y.z` tag; newest CHANGELOG/NEWS heading vs registry; commits since the registry's tag; "not compared" for every source it could not check | conda-forge, docs version dropdowns, pins in downstream repos |
| `fragments` | every system present: `changelog.d/` (names, final newline, one PR number per bullet, ≤ N lines), `.changeset/*.md` (valid bump per package, non-empty summary), NEWS.md's top section (bullets without a PR/issue ref counted); internal ids (`B-M31`, `R828-4`, `Task 3.1`, `Phase 5`) in all three; "no fragment system" when there is none | whether the **Area:** lead and wording match the house contract |
| `leaks` | tracked public files only: local/server paths, non-placeholder IPs, internal ids, agent notes (`ponytail:`, `.superpowers/`), `dev/*.md` citations, private repo names (`sdv-internal-refs`, `ClaudeCowork`, …) | rendered pages built from docstrings (grep the built site or the docstrings too); images; deliberate provenance registers |
| `counts` | every "N <noun>" claim in hand-written docs, grouped by noun | context: "128 wrappers" (one stem) and "4,566 wrappers" (all ESPN) can both be right — measure each |
| `osv` | every locked package against OSV, with severity | whether the package reaches runtime (`uv tree --frozen --invert --package <pkg>`; extras/dev only is lower) |

## Phase 3 — Dispatch the five lenses

One `sdv-repo-auditor` per lens, **in parallel, at most 5 at once** (more trips the
session rate limit). Never a `general-purpose` agent for a lens this agent owns. Each
prompt carries exactly:

```
lens: <contributor-docs | companions | coverage | currency | polish>
archetype: <primary> (+ secondary: <secondary, ...>)
repo: <owner/name>   audit tree: <W>   sha: <short sha>   date: <YYYY-MM-DD>
references: <this-skill-dir>/references/<file>.md, ...   (every file the archetype probe listed; run only your lens's section in each)
files: <the explicit file list for this lens, from the reference's "Files" line, resolved against W>
probes: <O>/<the probe outputs this lens uses>
output: <report-dir>/<NN>-<lens>.md
questions: <the user's questions this lens answers, verbatim>
```

| NN | Lens | Answers |
|---|---|---|
| 01 | `contributor-docs` | Is every concrete claim in CHANGELOG/fragments, CONTRIBUTING, README, CLAUDE.md/AGENTS.md, copilot-instructions and the issue/PR templates true at this SHA? |
| 02 | `companions` | Do the companions install, integrate, appear in notebooks/vignettes/examples, and link both ways? (plotting/surface packages for libraries; producers and consumers for producers, services and web apps) |
| 03 | `coverage` | Do the front pages (home, intro, README, nav) cover what the registries say exists, with consistent names and live links? |
| 04 | `currency` | Release state, outdated deps, lock advisories, docs/MCP/search index freshness, CI and crons on main |
| 05 | `polish` | What a stranger sees first, ranked by visibility: live pages, leaks, metadata/SEO, root clutter, README header, repo description/topics |

When subagents are unavailable, read `<this-skill-dir>/../../agents/sdv-repo-auditor.md`
and run each lens inline, one after another, writing the same files.

The five lenses are the whole agent budget: no lens starts a sixth agent. A producer's
per-tag surface check applies `sdv-dataset-coverage-auditor`'s definition **inline**
inside lens 02 (`references/producer.md`). Run that agent separately only after the
five lenses have reported.

Keep `W` until Phase 5 is done: verification reruns commands against it.

## Phase 4 — Verify the reports

For each report, before synthesis:
1. Spot-check the top three findings yourself at the SHA (open the line; rerun the
   command). One wrong top finding means re-reading the whole report.
2. Every finding has file:line, evidence (command + output, or a quoted line) and a fix.
   A finding without evidence moves to that report's **Unverified** section.
3. Dedupe across lenses (the release story appears in 01, 04 and 05 — keep it once,
   in the most specific lens, and cross-reference).
4. A "verified accurate" list is part of the result: claims checked and found true are
   what lets the next audit skip them.

## Phase 5 — Synthesize `README.md`

`<report-dir>/README.md`, in this shape (the sdv-py synthesis was 31 lines; stay short):

```markdown
# <repo> docs, currency and polish audit (<date>, main `<sha>`)

<one line: what was audited and when>. Detail, with file:line and evidence: `01-…md` … `05-…md`.

## Answers

| Question | Verdict |
|---|---|
| <file or question> | **<current · minor drift · needs work · wrong>**: <the one or two facts that decide it> |

## Cleanup, in PR-sized batches (most visible or most blocking first)

1. **<batch title>** (<lens refs, e.g. 01#1, 04 §1>): <what changes, which files>. Gate: <archetype gate>.
```

Rules for the table and the batches:
- One row per file the user named (CHANGELOG, CONTRIBUTING, README, CLAUDE.md, templates,
  …) plus one per lens question. The verdict word comes first and is bold when it is not
  `current`.
- A batch is one PR: one theme, one reviewer's sitting, its own gate. Split a batch that
  touches generated docs and hand-written prose unless one regen covers both.
- Order: what blocks other batches (an unreleased release, a security re-lock), then by
  visibility (live home page, README, PyPI/CRAN page), then contributor-only docs, then
  root clutter.
- Name code bugs found by a docs lens (sdv-py's `function_count()` hard-coding 45 of 105
  leagues) as their own batch; they need tests, not prose edits.

In the terminal: the Answers table, the batch list, and the report path. Ask which
batch to start; each one is a separate tier-1 confirmation.

Only now, with every auditor reported and the synthesis written, remove the audit
worktree: `git -C <repo> worktree remove "$W"`. Then compare the main checkout's
`git status --short` and lock hash with the Phase 1 notes.

## Red flags — what the audit exists to catch

| Thought | Reality |
|---|---|
| "The CHANGELOG has a 0.1.5 section, so 0.1.5 shipped" | sdv-py's did not: no tag, no GitHub Release, PyPI at 0.1.4, 789 commits behind. Check the registry. |
| "The README is hand-written, so someone keeps it current" | It covered 50 of 105 leagues. Compare against the registry, not against memory. |
| "The template field must work, people fill it in" | The bug template asked for `sportsdataverse.__version__`, which does not exist. Verify each command a template or doc asks for statically (the symbol, flag or file exists at the SHA) or with a read-only `--help` / `--check`. |
| "The extra is called `[sdvplot]`, so it installs plotting" | It installed no matplotlib or sportypy; every plotting notebook's first import failed. Read what each extra resolves to. |
| "Counts in docs are roughly right" | Three files quoted three package sizes. Measure by importing the package from the audit tree (assert `__file__`). |
| "Docstrings are code, not public content" | They render: `ponytail:` notes, `sdv-internal-refs` paths and `Task 3.1` ids reached the live reference pages. |
| "The lock is fine, tests pass" | certifi carried a CRITICAL advisory in runtime deps. Run `osv`. |
| "CI is green on main" | The weekly live-tests cron had been red three weeks running. Look at the scheduled workflows, not the push run. |
| "I'll just fix this typo while I'm here" | The audit never edits. It becomes a finding in a batch. |
| "Six lenses at once will be faster" | More than ~5–8 parallel agents trips the rate limit. Cap at 5. |

## Keeping this skill sharp

A drift that a later audit (or a user) found and this audit missed is a missing check:
add it to the lens checklist in the archetype's reference with the incident that
taught it, and when it is mechanically matchable, add it to `scripts/audit_probes.py`
with a positive and a negative case in `tools/test_audit_probes.py`. A probe pattern
that keeps matching house style (a placeholder IP, a URL path) is a false positive to
fix in the probe, not a line to teach auditors to skip. Capture through `/sdv-learn`.
