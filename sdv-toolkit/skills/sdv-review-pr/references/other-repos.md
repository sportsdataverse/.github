# other repos — JS package, plotting libs, research & papers, toolkit & dotfiles, maintainer-owned

## Third-party and maintainer-owned mode

Some in-scope repos belong to an outside maintainer's conventions: **sportyR / sportypy**
(Ross Drucker), **cfb4th** (Jared Lee), **baseballr** (BillPetti upstream),
**mlbplotR** (camdenk upstream; SDV only lists it in r-universe). Outside-contributor
PRs anywhere (sportyR #42/#47, sportypy #13) get the same treatment.

- **EXT-1** `[major]` Review against the repo's own CONTRIBUTING / style config, not
  SDV house rules — no uv/pyproject/polars/codegen demands in unrelated PRs. Universal
  correctness, security and failure-path rules still apply.
- **EXT-2** `[major]` A contributor PR is never merged, pushed to, or commented on
  without explicit per-item authorization (the `sdv-triage` tier rules); the review is
  prepared locally first.

## sportsdataverse-js — npm `sportsdataverse` (ESM TypeScript, codegen)

CI (`ci.yml`, Node 20/22): `codegen:check`, typecheck, dist smoke, no-network mocha,
`docs:examples:check`, docusaurus build (`onBrokenLinks: throw`).

- **JS-1** `[blocker]` Never hand-edit `src/generated/**`, `docs/docs/reference/**`,
  `docs/src/playground/endpoints.json`, `docs/src/generated/reference-sidebar.js` —
  edit `tools/codegen/endpoints/*.yaml` or `generate.mjs`, run `npm run codegen`, commit
  outputs together.
- **JS-2** `[blocker]` `{ parsed: true }` is strictly additive: a wrapper's default raw
  return never changes.
- **JS-3** `[major]` A change under `src/parsers/**` also changes
  `docs/src/playground/parsers.bundle.mjs` (`npm run bundle:parsers` then
  `npm run docs:examples`) — the CI staleness guard compares registry **key sets** only,
  so a logic edit without a rebundle passes CI.
- **JS-4** `[major]` `FLAT_API_NAMESPACES` has three hand-synced copies
  (`src/index.ts`, `tools/codegen/generate.mjs`, `test/flat-contract.test.js`) plus
  `FLAT_API_FILES`/`FLAT_API_META` — a new family updates all of them.
- **JS-5** `[major]` Tests are no-network; live suites sit behind `SDV_LIVE=1`, never set
  in CI. ESM hygiene: relative imports carry `.js`, no `require`, JSON imports use
  `with { type: 'json' }`.
- **JS-6** `[minor]` No new credential requirement (NFL bearer tokens auto-mint);
  provider keys are env overrides only; surface renames get a cheat-sheet note.

## Plotting libraries — sportyR, sportypy, cfbplotR

- **PLOT-1** `[blocker]` sportyR dimension edits go in
  `data-raw/surface-dimensions.json` with a regenerated `R/sysdata.rda` committed
  alongside (re-source `data-raw/internal-datasets.R`); cfbplotR `R/sysdata.rda`,
  `data/*.rda`, `NAMESPACE`, `man/`, `README.md` are regenerated from `data-raw/` and
  roxygen, never hand-edited.
- **PLOT-2** `[major]` New sports ship features + geom + tests and keep 100% coverage
  (sportyR, sportypy); leagues are parameterized in the JSON, not hard-coded; geometry
  changes are mirrored between sportyR and sportypy or get a parity issue (key spelling
  has already drifted: `little league` vs `little_league`).
- **PLOT-3** `[major]` cfbplotR skips vdiffr on CI — geom/element PRs include locally
  accepted `_snaps/**/*.svg` (never delete snapshots to pass); `ggpath::element_path` is
  S7 (construct it, never `structure(list(), class=)`).
- **PLOT-4** `[minor]` sportypy is a legacy `setup.py` package on numpydoc; flag publish
  auth modernization (PyPI password auth is dead) separately rather than inside a feature
  PR.

## cfb4th

- **C4TH-1** `[blocker]` `.onLoad` fetches `ep_model`/`fg_model` inside
  `try(silent = TRUE)` — offline they become NULL and legs degrade silently. Changes keep
  a visible failure path; never add more silent `try`.
- **C4TH-2** `[major]` Bundled `fd_model`/`wp_model` stay native UBJ via
  `xgboost::xgb.load` with `xgboost (>= 2.0.0)`; never ship RDS boosters or re-pin
  `< 2.0`. New tests hitting the network add `skip_if_offline()` + `skip_on_cran()`.
- **C4TH-3** `[major]` It depends on cfbfastR pbp column names and the legacy EP
  artifact; flag EP/WP semantics drift against cfbfastR dev's XGBoost bundle explicitly.

## Research and papers

**Sports-Research-Papers** (public reading library: PDFs + markdown twins + manifest +
feed bots). **ClaudeCowork `cmsac-2026/`** (authored Quarto papers). Model writeups in
`-data` repos follow `sdv-data-pipeline` Step 9c (Quarto → committed GFM).

- **DOC-1** `[blocker]` No PDF or full text whose licence doesn't permit public
  redistribution — closed-access works get a metadata + abstract stub; never
  shadow-library or paywall-bypass routes; never cookies/storage state.
- **DOC-2** `[major]` Every library addition has a `library/manifest.jsonl` row
  (`dedupe_key` = DOI/arXiv id, `sha256`, `licence`, `content_form`) and a `md/` twin
  with the `<!-- source: … -->` header in the same change; duplicates are recorded, not
  re-added.
- **DOC-3** `[major]` Ranking changes are append-only ("Additions since the <date>
  pass"); every figure quoted in MD/HTML is recomputed from the CSV.
- **DOC-4** `[blocker]` In an authored paper, every quantitative claim maps to a
  `NUMBERS.md` row with a provenance class (`[S]` script-rederived, `[PR]` PR+commit,
  `[C]` counted at a stated commit, `[L]` private log — labelled as such in prose).
- **DOC-5** `[major]` Papers pin the sportsdataverse-py version and the repo HEAD SHAs
  used; render cleanly to PDF and HTML; one citation mechanism (`references.bib` +
  `bibliography:`); captions state scope, n, units, generating script.
- **DOC-6** `[major]` Publish scripts never `git add -A` a paper tree into a public
  repo; licensed data (PFF, odds) never goes public.
- **DOC-7** `[minor]` Scheduled writers pin Python, run tests before committing, and
  rebase before push.

## Toolkit (`sportsdataverse/.github`) and dotfiles

- **TK-1** `[blocker]` A change to skills, agents or hooks bumps
  `sdv-toolkit/.claude-plugin/plugin.json` `version`, adds/updates the `catalog.json`
  row, and re-renders (`python tools/render.py`) so `check_catalog.py .` and
  `render.py --check` pass. `README.md` and `marketplace.json` are CRLF in the index —
  a Linux re-render that flips them to LF is unrelated churn (**U-GIT-5**).
- **TK-2** `[major]` Mirror discipline: the org repo lands first, then
  `dotfiles:claude/plugins/sdv-toolkit/` mirrors the released version (compare with
  `diff -r --strip-trailing-cr`); never edit the mirror first.
- **TK-3** `[major]` Router changes (`hooks/sdv_router.py`) come with
  `hooks/test_sdv_router.py` cases; the AI-attribution guard in `hooks/hooks.json` stays
  (dropping it was reverted); new signal regexes carry positive and negative tests.
- **TK-4** `[major]` Skill text follows the toolkit's own discipline: rules cite a real
  incident, descriptions state triggers, no enumerating everything; a new rule is added
  through `sdv-learn` with its detection test.
- **TK-5** `[blocker]` dotfiles: no secrets or real identity values (`.gitconfig` keeps
  a placeholder email with a local override); the global `commit-msg` hook keeps chaining
  to the repo-local hook via `git rev-parse --git-dir` and keeps the policy check first;
  `install.sh` backs up before replacing; `*.sh` stay LF per `.gitattributes`.
- **TK-6** `[minor]` Generated `status/*` changes only via the nightly bot; the reusable
  `orphan-scripts.yml` sparse list and `ref_sources` globs change together.

## sdvmodels (empty stub)

- **SDVM-1** `[major]` The first real PR decides the stack and adds packaging, CI, and a
  README with artifact provenance and consumers before code; no artifact duplicated from
  an existing owner.
