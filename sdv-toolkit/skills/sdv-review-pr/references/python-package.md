# python-package — sportsdataverse-py (sdv-py)

A polars-first multi-league SDK with codegen-owned wrappers and docs
(`tools/codegen/`), bundled XGBoost artifacts, and release-asset loaders. `main` is
installed **unpinned** by production crons, so a merge is a deploy.

CI: `codegen.yml` (drift gate — the one that matters), `quality.yml` (ruff, mypy
ratchet, contract tests), `tests.yml` (offline on PRs; live job skips PRs). Every job
runs Python 3.13.2 with `uv sync --frozen`. `local /mnt/sdv_repos/sdv-py` and
`sportsdataverse-py` are both clones of the same repo — review against `origin/main`.

**Routed, not restated:** polars API tiers, `dl_utils.download`, the ESPN parser
contract, docstrings → `sdv-python-reviewer` (lenses `polars` | `http` |
`parser-contract` | `docstring`); returns-table descriptions → `sdv-docs-reviewer`;
ports → `sdv-parity-reviewer`; model gates → `sdv-model-reviewer`; regen procedure
and bot triage for your own PR → `sdv-ship`.

## Rules

- **PY-1** `[blocker]` A PR that changes a codegen input ships regenerated output and
  `generate.py --check` is green. Inputs: `tools/codegen/{endpoints,schemas,templates}/`,
  `manual_column_descriptions.yaml`, `endpoints/{releases,parameters,leagues}.yaml`,
  `schemas/loader_schemas.yaml`, and the docstring or `__all__` of any public function.
  Local hooks miss two of those — the `sdv-codegen` pre-commit hook fires only on
  `endpoints|schemas|templates/`, so a `manual_column_descriptions.yaml` or
  docstring-only edit passes locally and fails CI.
- **PY-2** `[blocker]` Generated files are never hand-edited: `*_espn_ext.py`,
  `sportsdataverse/parsed/*.py`, `docs/docs/<sport>/reference/*`, generated container
  `__init__.py`. A review comment on generated text is fixed in the YAML source (a
  `week` param description fixed in `parameters.yaml` fixed every sport at once —
  #458). A small PR with large unrelated reference-doc deletions usually means HEAD
  moved mid-regen (the droplet `git_pull` cron).
- **PY-3** `[major]` New flat-API family traps: the first full regen after bootstrap
  shows phantom drift — commit only the second run; `query_params:` is silently
  ignored (use `params:`/`extra_params:` + `query_key:`); a cross-sport provider goes
  in `_NONLEAGUE_EXTRA`, not a pseudo-league; a grouped league nests at
  `sportsdataverse/<group>/<prefix>/`.
- **PY-4** `[major]` Loader-schema capture is scoped to the loaders the PR touches (a
  full re-capture reorders ~160 unrelated blocks — #478); inferred types are
  re-captured against a populated season, never hand-fixed (an all-null season infers
  `Boolean` — #486); a new loader without a captured schema renders no Returns table.
- **PY-5** `[blocker]` `uv.lock` matches `pyproject.toml` — ask for `uv lock --check`
  (CI's `--frozen` doesn't check it). The lock change lands in the same commit as the
  pyproject change. (#454 added `nflpro` without re-locking; the delta rode into #466;
  version bumps rode into #409 and #421.)
- **PY-6** `[blocker]` Removing or renaming a public name keeps a back-compat path (a
  `_MOVED` entry with `__getattr__` deprecation, or `_deprecation.deprecated`) and a
  breaking marker (`type!:` / `BREAKING CHANGE:` + the template's Breaking changes
  section). Guarded by `tests/test_namespace_backcompat.py`, `tests/test_deprecation.py`.
- **PY-7** `[major]` Don't repurpose names: no new per-type NFL loaders, no reuse of a
  deprecated nflverse alias for a different source (`load_nfl_ngs(dataset=)` is unified
  for exactly this reason).
- **PY-8** `[blocker]` Loader URL/season changes match the published assets exactly.
  nba_stats public `seasons=` stays START while assets are END-named;
  `compile_nba_season(2024)` means 2023-24; wnba_stats is single-year and never
  shifted — require anchored patterns plus a test that WNBA URLs are unchanged (#367
  shifted 8). See **U-DATA-1**.
- **PY-9** `[major]` A changed loader is tested with the cache off
  (`update_config(cache_mode="off")`): `@cached_loader` keys on
  `(qualified_name, args, kwargs)`, not the URL or body, so a changed URL serves stale
  frames. Cache keys include everything that changes the answer (account — #454;
  query dates — #487).
- **PY-10** `[blocker]` A failed fetch never becomes an empty season: `NoDataError` =
  fetched and nothing there; `AssetFetchError` = the fetch failed. A 403/5xx never
  takes the "absent" branch for an optional asset (#397/#402/#403/#404). Transport
  mechanics are the `http` lens; the review decision is which error class a miss maps
  to.
- **PY-11** `[major]` Merge = production deploy for these unpinned consumers:
  cfbfastR-cfb-data (`cfb_ratings_cron`, `espn_daily_snapshots`,
  `cfb_recruiting_proj_cron`) and nfl-data (`nfl_pbp_cron`,
  `nfl_rosters_players_cron`, `nfl_model_pipeline`), plus GOP's image build. A PR
  changing what they call (`build_nfl_*`, `cfb_ratings`, `espn_snapshots.parse_*`,
  `enrich_nfl_pbp`, `CFBPlayProcess`/`NFLPlayProcess`) states the downstream effect and
  the consumer `SCHEMA_REV` bump + reprocess it needs.
- **PY-12** `[major]` Only `sportsdataverse*` ships in the wheel: a runtime
  `import tools…` from `sportsdataverse/**` is a blocker; `package-data` globs are
  explicit and non-recursive, so a bundled file in a new directory doesn't ship unless
  listed. Consumers never use `PYTHONPATH=$SDV_PY_DIR`.
- **PY-13** `[major]` CI never exercises the 3.9 floor (`requires-python >=3.9`, jobs
  run 3.13.2). Runtime-evaluated PEP 604/585 annotations or `match` need the
  `from __future__ import annotations` import. **Do not** ask to remove that import —
  bots have demanded it in ~15 PRs; the repo's own docs contradict each other.
- **PY-14** `[major]` Live tests sit on the right gate: `stats.nba.com`/`stats.wnba.com`
  → `@skip_if_no_nba_stats_live` (`SDV_PY_NBA_STATS_LIVE=1`), never
  `@skip_if_no_live` (they hang the macOS job). The live job skips PRs — a
  data-touching PR needs a local `SDV_PY_LIVE_TESTS=1` transcript.
- **PY-15** `[major]` Fixture directories keep a provenance README; fixtures are
  excluded from whitespace hooks on purpose (**U-TEST-3**).
- **PY-16** `[major]` Regenerated `tools/validation/schemas/*.json` snapshots report
  added/changed/**REMOVED** counts per frame; REMOVED is 0 or justified column by
  column; String ids checked for `"123.0"` (#415 225 bogus errors from a stale
  snapshot; #484 "REMOVED=0" as the load-bearing fact).
- **PY-17** `[minor]` Side artifacts: `CHANGELOG.md` edits include the synced
  `docs/src/pages/CHANGELOG.md`; exports added/renamed get a cheat-sheet revision note;
  the 10 MB large-file guard is not raised (only `cfb/models/fd_model.ubj` is exempt).

## Verify (worktree at the PR head)

```sh
git diff --stat origin/main...HEAD
git diff --diff-filter=D --name-only origin/main...HEAD           # U-GIT-2
uv lock --check                                                   # PY-5
uv run --frozen python tools/codegen/generate.py --check          # PY-1 (can exceed 10 min: run in background)
uv run --frozen ruff check sportsdataverse tests tools && uv run --frozen ruff format --check sportsdataverse tests tools
uv run --frozen mypy
uv run --frozen pytest -q tests/test_id_conventions.py tests/contracts tests/test_namespace_backcompat.py tests/test_deprecation.py tests/codegen
grep -rn 'skip_if_no_live' tests | grep -iE 'nba_stats|wnba_stats'  # PY-14
uv build && unzip -l dist/sportsdataverse-*.whl | grep -E ' (tools|dev)/'   # PY-12
gh pr checks <N> -R sportsdataverse/sportsdataverse-py            # codegen drift job is the gate
```

`uv run` can silently re-lock `uv.lock`; `git status` after, and never let it into a
review fix.
