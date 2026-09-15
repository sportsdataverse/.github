# producers — `*-raw`, `*-data`, and the models inside them

`-raw` repos scrape and commit per-game JSON (scraping only — no ML deps). Every push
to `main` fires a `repository_dispatch` into the sibling `-data` repo. `-data` repos
build, reshape, publish release assets to `sportsdataverse/sportsdataverse-data`,
and host live model code (`cfbfastR-cfb-data/python/cfb_model_build/`,
`nfl-data/python/model_training/`, `baseballr-data/python/mlb_model_publish/`).
`cfbfastR-models` is dormant, `sdvmodels` is an empty stub, `psql-to-models` is third
party.

Automation commits land directly on `main`; **code changes still go through PRs**.
Highest blast radius in the ecosystem: a wrong season key or a green-but-empty publish
reaches every loader, the DB, and GOP.

**Routed, not restated:** stage placement and numbering, idempotency, `str2bool`,
launcher logging, two-tier manifests, README contract → `sdv-conventions`
(`raw.md`/`data.md`) and `sdv-data-pipeline`; model correctness → `sdv-model-reviewer`;
new tags across the 12 surfaces → `sdv-dataset-coverage-auditor`; harness WARNs →
`sdv-harness-triage`.

## Shared (raw and data)

- **PROD-1** `[major]` Driver shell fails loudly: `set -euo pipefail`; rc carried out
  of pipes (`PIPESTATUS`/temp file); interpreter resolved once at top level
  (`scripts/_venv.sh` + `sdv_preflight`), never `uv run` for a scrape/reprocess (it
  re-syncs under a live job) and never inside a `{ …; } | tee` subshell; footer
  `echo EXIT=$rc` reflects the real rc. — (nfl-ngs-raw run #1 `PY: unbound variable`
  pushed 18 log-only commits; a trailing `tail` reported 0 over an OOM 137)
- **PROD-2** `[major]` Moving code into a package changes path anchors:
  `Path(__file__).parents[N]` re-checked, no `Path()` around a URL root, `Path.glob`
  never used on a URL root; the PR tests the resolved root. — (wnba-stats-raw wrote
  4,551 payloads to an untracked dir and green-committed nothing)
- **PROD-3** `[major]` Cross-repo callers checked before renaming/moving scripts; the
  orphan-scripts gate needs every new `scripts/`/`ops/` file referenced in the same
  commit and cannot see droplet crontab callers. — (cfb-raw's QBR shim is run by
  cfb-data's `cfb_model_pipeline.yml`)
- **PROD-REBASE** `[major]` Rebase a rejected push in these binary repos with
  `git rebase --merge origin/main`, never `git pull --rebase` (the am backend
  base64-encodes parquet and stalls).
- **PROD-5** `[blocker]` Every `python -m <module>` in workflows, driver scripts, and
  the sdv-orch registry resolves to a module at the head. Stage renames leave dangling
  references that fail on the next run — and a driver that ignores that step's exit code
  turns it into a green run that publishes nothing. `context.md` lists dangling targets;
  a PR whose goal runs through a dangling stage cannot achieve it. — (fastRhockey-nhl-data:
  stage 03→19 rename left both production callers on `nhl_data_03_publish`)
- **PROD-4** `[minor]` CI sparse-checkout lists and `CLAUDE.md` follow structural
  changes (new top-level code dir, pin form, workflows). Code in an unlisted dir is
  neither tested nor linted.

## Raw producers

- **RAW-1** `[blocker]` The scraper's data-commit subject is parsed downstream — keep
  `"<Sport> Raw Update (Start: YYYY End: YYYY)"` (and `CFB Reprocess Update (…)`,
  `NBA Stats Update (…)`). Adding any other digits is also a blocker while consumers use
  permissive year greps (**DATA-2**). A conventional-commit rewrite once put a run id
  into `END_YEAR`.
- **RAW-2** `[blocker]` Every `*_data_trigger` workflow guards
  `github.ref == 'refs/heads/main'` (the dispatch payload hardcodes `refs/heads/main`,
  so an unguarded feature-branch push starts a production build of unlanded work —
  cfb-raw#10). A PR adding pushes (per-stage log commits, lock bumps) adds dispatches;
  only the newest pending run survives.
- **RAW-3** `[major]` Mass changes (renames, backfills, re-parses) commit and push per
  season; code and data trees go in separate PRs (cfb-raw#7: 949 files, both bots
  skipped).
- **RAW-4** `[blocker]` A process pool started after polars is imported uses
  `mp_context=multiprocessing.get_context("spawn")` and module-level callables; fork
  deadlocks at 0% CPU on the first real run (cfb-raw `df65c1a2`; same pattern in
  ncaa-mfb-football-raw and nfl-data). Fork is fine only when polars is imported
  lazily inside the worker.
- **RAW-5** `[blocker]` The processing stamp moves whenever output can change — any
  sdv-py lock bump, final-shape or enrichment change: bump `SCHEMA_REV` or fold the
  sdv-py commit into the stamp (`0.1.3+7be22b5a.3`). Otherwise reprocess skips exactly
  the games that need rebuilding. — (cfb-raw#15)
- **RAW-6** `[major]` Every new write path (reprocess, backfill, repair) carries the
  scraper's guards (e.g. `status_state == "pre"`), with a test. — (cfb-raw#8 pre-game
  shells made `filter_undone` skip 2026; #16 pushed 940 empty shells)
- **RAW-7** `[major]` Lock bumps get their own `chore(deps)` commit and a stamp
  decision (**RAW-5**); PR CI stays `--frozen`. (wehoop-wbb-raw's daily job commits
  `uv lock --upgrade` with data by design — not a finding there.)
- **RAW-8** `[major]` CFB stage numbers follow cold-start execution order;
  nba/mbb/wnba/wbb number by dataset identity. Reject "renumber to match siblings" in
  either direction.
- **RAW-9** `[minor]` Current-season daily runs refetch in-progress data (no
  `--skip-existing` after day one; refetch until `completed`); capture windows are
  sized so a green run captured something, with a non-zero-capture assertion (a 10-day
  odds horizon captured 0 NFL props and looked clean).

## Data producers

- **DATA-1** `[blocker]` One season convention per sport at the asset and row boundary
  (**U-DATA-1** table); `-data` stamps `season` unconditionally; only `-raw` may speak
  academic years.
- **DATA-2** `[blocker]` Workflows never interpolate the dispatch commit message into
  `run:` and parse years with the anchored `grep -oP 'Start:\s*\K[0-9]{4}'` (passed via
  `env: COMMIT_MESSAGE:`), never `grep -o -E '[0-9]+' | head -1`. Correct shape:
  `cfbfastR-cfb-data/.github/workflows/daily_cfb.yml`. Flag any PR touching or copying
  those steps.
- **DATA-3** `[blocker]` Asset names, formats and sidecars are a loader contract: stems
  match sdv-py loader URLs and R `load_*`; `.rds` kept where R reads it; publish stamps
  `timestamp`/`package_function` sidecars. Renaming, dropping a format, or moving a tag
  lists the consumer PRs.
- **DATA-4** `[blocker]` Publishing never finishes green with nothing published:
  - ensure the tag exists (`gh release view || gh release create`) before
    `gh release upload`;
  - retry only idempotent `upload --clobber`, never `release create`;
  - upload the paths **this run wrote** (a `written` list), never a directory glob;
  - mark a season published only when every format landed; manifests written
    atomically (temp + `os.replace`);
  - retry knobs validated at import; exhaustion raises (**U-FAIL-6**).

  — (cfb-data#75 uploads into never-created tags for 55 min/run; #76 attempts=0 no-op;
  hoopR-nba-stats-data#35 "defeated the empty guard by the back door"; cfb-data#58, #69)
- **DATA-5** `[blocker]` Exactly one publisher per release tag (droplet cron **or**
  Actions, never both). Don't drive a backfill through per-season raw pushes — recut
  locally with `--cache-dir` (CI re-downloads ~2.7 GB per season and only the newest
  dispatch runs).
- **DATA-6** `[blocker]` A builder PR proves non-zero output on a known-populated season
  (**U-FAIL-4**); only 404/410 mean absent. For a new, vendored, or derived table,
  replay the builder and diff its **entity coverage** (teams, players, games per
  season) against the neighbouring published season — a coverage-band test (90–140
  teams) passed while 9 FBS programs were silently dropped.
- **DATA-7** `[major]` Cross-repo publish uses `SDV_GH_TOKEN` (`Contents: write`) with
  **no** `GITHUB_TOKEN` fallback; an absent secret fails before the build. (**U-CI-3/4**)
- **DATA-8** `[major]` A published or committed build states its column diff against
  the current release (column count, `only_in_published == 0`). — (nfl-data#35 found
  three vintages of 2024 `model_pbp`: 120/257/326 columns)
- **DATA-9** `[major]` Snapshot datasets (injuries, depth charts) append with
  `as_of_date`, replace same-day rows, never publish a zero-row asset; id casts parse
  Utf8→Int64 and raise rather than null a join key; the grain keeps load-bearing keys
  (NFL depth charts need `position_slot`).
- **DATA-10** `[major]` A new `pkg::fn` in a workflow is checked against that package's
  `NAMESPACE` (`cfbfastR::most_recent_cfb_season()` is not exported — every
  unparameterised run failed); compute default seasons in bash with `10#` months.
- **DATA-11** `[minor]` `CLAUDE.md` commands match the real packaging root and pin form
  (nfl-data documents `python/` while `pyproject.toml` is at the root).

## Models (inside -data repos and sdv-py bundles)

- **MOD-1** `[blocker]` Every new published model/artifact has a complete registry row
  (artifact, tag, training data, fitting script, gates, last retrain, cadence — "frozen"
  written out). `tests/test_model_registry.py` matches package names, not rows —
  check rows by hand.
- **MOD-2** `[blocker]` Retrain publishing stays opt-in (`nfl_model_pipeline.yml`
  `publish` input defaults off; publish requires stage success).
- **MOD-3** `[blocker]` Booster, card and bundle move together; `feature_names` checked
  at package and consume time; artifacts copied into `sportsdataverse/<lg>/models/`
  match the release tag.
- **MOD-4** `[major]` Score with the era cuts the model was trained on — read them from
  the card, never restate them (sportsdataverse-py#463, cfbfastR#150).
- **MOD-5** `[major]` A "model is broken / flat" claim derives feature support from the
  trainer (`features.py`), checks split thresholds and `base_score` (cfbfastR#149
  retraction).
- **MOD-6** `[minor]` Heavy artifacts are download-on-demand, not bundled (10 MB guard;
  explicit package-data list).
- **MOD-7** `[major]` Metadata writers merge rather than overwrite (a card writer
  clobbered 7 cards' objective/training_seasons/hyperparameters); class order comes
  from `MANIFEST.json`.

Gate integrity, leakage, metric fit, uncertainty and lineage depth →
`sdv-model-reviewer` with the matching lens.

## Verify

```sh
grep -n 'git commit -m' scripts/daily_*_scraper.sh scripts/*reprocess*.sh        # RAW-1
grep -n "github.ref == 'refs/heads/main'" .github/workflows/*trigger*            # RAW-2
grep -rn 'ProcessPoolExecutor(\|\.Pool(' python | grep -v spawn                 # RAW-4
grep -rn 'SCHEMA_REV\|PROCESSING_VERSION' python | head                          # RAW-5
grep -n 'client_payload.commit_message' .github/workflows/*.yml                  # DATA-2
git diff --name-only origin/main...HEAD | awk -F/ '{print $1"/"$2}' | sort | uniq -c   # RAW-3 code vs data
gh release view <tag> -R sportsdataverse/sportsdataverse-data --json assets \
  --jq '.assets[] | [.name,.updatedAt,.size] | @tsv' | sort | tail                # DATA-3/6: landed, fresh, non-trivial
env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash scripts/<stage>.sh   # PROD-1 service env
uv lock --check && uv sync --frozen --dev && uv run --frozen pytest -q
```

Avoid `git show`/`git log -p` on data commits while reviewing — they take minutes.
