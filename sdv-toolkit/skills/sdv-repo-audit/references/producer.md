# Producer lenses (`*-raw`, `*-data`)

Producers publish data, not an API, so "docs" means the README's promise about tags,
seasons and schedules, and "currency" means the published assets. Producers commit
straight to `main`; fixes still go through a confirmed batch. Never run a stage, a
scrape, or a publish entry point to measure something: read the assets instead.

## 01 contributor-docs

**Files:** `README.md`, `CLAUDE.md`, `AGENTS.md`, runbook docs (`docs/`, `RUNBOOK.md`),
`scripts/` (stage names), `.github/workflows/*.yml`, `pyproject.toml`, `column_descriptions.yaml`
(or the repo's equivalent), `tests.yml` sparse-checkout list.

| Claim kind | How to verify |
|---|---|
| Stage list and order | README/CLAUDE.md stages vs `scripts/NN_*` (NN = intended build order, not run order) and the workflow or droplet runner that calls them |
| Schedules | stated cron times vs `on: schedule:` in workflows (UTC) |
| Tags and datasets | every tag the README names exists (`gh release view <tag>`); every published tag is in the README |
| Season coverage | stated floors/ceilings vs asset names (`gh release view <tag> --json assets --jq '.assets[].name'`) |
| Column docs | `column_descriptions.yaml` columns vs a published asset's schema (read one parquet footer with pyarrow over HTTP, read-only) |
| sdv-py pin | the `sportsdataverse` git rev / version in `uv.lock` vs the claim ("built with sdv-py main") |
| Commands | each documented command exists in `scripts/` or the workflow and takes the documented flags (`--help`) |

## 02 companions

The consumers of this producer's tags: sdv-py `load_*` loaders, the R package's `load_*`,
sdv-db catalog rows, GOP pages. **Dispatch `sdv-dataset-coverage-auditor` for the
per-tag surface check instead of re-deriving it**; this lens only records its verdict
per tag and checks:

| Check | How |
|---|---|
| Loader points at the right tag | grep the loader's tag constant in sdv-py and the R package (sibling checkouts) |
| Docs both ways | the consuming package's docs link this repo; this README names the loaders |
| Twin producers | `-raw` ↔ `-data` README describe the same tag set and handoff |

## 03 coverage

**Files:** `README.md` tag/dataset tables, `status/producers.json` (org repo) entry, release list.

| Check | How |
|---|---|
| Tags table vs releases | `gh api repos/o/r/releases?per_page=100 --jq '.[].tag_name'` vs the README table |
| Assets per tag | expected season range present, no zero-byte or `.tmp` assets |
| Org status page | the producer's row in `sportsdataverse/.github` `status/` matches reality |
| Hard-coded counts | `counts` probe ("N seasons", "N games") against asset names |

## 04 currency

| Area | Commands |
|---|---|
| Last publish per tag | `gh release view <tag> --json assets --jq '[.assets[].updatedAt]|max'` vs the stated schedule; in-season staleness beyond one cycle is a finding |
| Scheduled runs | `gh run list --workflow <wf>.yml --limit 10` for each scheduled workflow; green-but-empty runs (success with no asset change) are the classic producer defect |
| Droplet jobs | runbook-stated timers vs what the last asset timestamps imply (read-only; no ssh writes) |
| Lock | `osv` probe on `uv.lock`; sdv-py rev age (`git -C <sdv-py> log -1 --format=%ci <rev>`) |
| Orphan scripts | the org's `orphan-scripts.yml` gate result on main |

## 05 polish

| Check | How |
|---|---|
| README header | one line on what is published, where, how often; badges resolve |
| Repo About box | description and topics (`gh repo view o/r --json description,repositoryTopics`) |
| Leaked internals | `leaks` probe on README/docs only. `/mnt/sdv_repos` and droplet paths are legitimate in a runbook marked maintainers-only; flag them in the README, and flag droplet IPs anywhere |
| Root clutter | committed large files (`git ls-files -z | xargs -0 du -k | sort -n | tail`), stray logs, notebooks with outputs, tracked files under ignored dirs (`git ls-files -ci --exclude-standard`) |
