# platform — sdv-db, sdv-orch, sportsdataverse-web, sdv-next-clone, sdv-swagger, bin/, sportsdataverse-data, universe

The data platform runs on one DigitalOcean droplet: Postgres + the FastAPI Data API
(sdv-db), Prefect orchestration (sdv-orch), cron-driven scrapers, and a self-hosted
Actions runner. The public site and members-only platform (sportsdataverse-web) run on
Vercel. **Review-bot signal is near zero here** (CodeRabbit free tier is usually
rate-limited; Sourcery has no access to private repos) — the maintainer's PR body is
the main evidence, so demand it.

Operational facts every platform review needs:
- **The droplet checkout is production.** `sdv-db-api.service` runs from
  `/mnt/sdv_repos/sdv-db` with `uv run`; a branch checked out there is live.
- systemd and cron PATH lack `/root/.local/bin` → bare `uv run` exits 127.
- The `git_pull` cron checks out `main` in every repo at :40 of 1,5,9,13,17,21.
- Private repos: sdv-db, sdv-orch, sdv-internal-refs. Public: sdv-swagger,
  sportsdataverse-web, sportsdataverse-data, universe.

## sdv-db — Postgres warehouse + Data API

Ingest: `catalog.py` frozen `Dataset` REGISTRY, per-partition swaps in `load.py`,
systemd timers. API surface is codegen: `scripts/capture_schema.py` →
`api/gen/schema_snapshot.json` → `scripts/gen_api.py` → `api/generated/endpoints.py` +
`docs/sdv-data-api.openapi.json` (CI `--check`). Migrations are raw SQL
(`docs/migrations/`, `infra/postgresql/NN_*.sql`), no Alembic.

- **PLAT-DB-1** `[blocker]` New routes/routers register in `create_app` **before** the
  `/v1/{schema}/{table}` catch-alls (first registered wins; an unmatched POST falls into
  the write catch-all and answers 401/403, never 404). Keep `tests/test_orch_mount.py`
  style route-order tests. Verify a route with a minted throwaway key — a 401 proves
  nothing.
- **PLAT-DB-2** `[blocker]` Only kwargs naming a real column become filters; injected
  dependencies (`_key: KeyRecord`) never reach `build_select` (it became
  `unknown column '_key'` — #10).
- **PLAT-DB-3** `[blocker]` SQL construction: identifiers whitelisted against the
  snapshot/information_schema then `_quote()`d; values bound (`:v0`); no f-string SQL
  over request input (**U-SEC-2**).
- **PLAT-DB-4** `[blocker]` A PR that creates/drops/alters a served table recaptures
  `schema_snapshot.json`, reruns `gen_api.py`, commits `endpoints.py` + the OpenAPI
  JSON, and says `sdv-db-api` must be restarted and the droplet returned to `main`
  after merge.
- **PLAT-DB-5** `[major]` Catalog/served divergence baselines
  (`SERVED_WITHOUT_CATALOG_ROW`, `CATALOG_WITHOUT_SERVED_TABLE`, `UNCAPTURED_LEAGUES` in
  `tests/test_generated_api.py`) change with a reason comment whenever a catalog row or
  captured league does.
- **PLAT-DB-6** `[blocker]` Every new league/schema gets a `SEASON_END_YEAR_OFFSET`
  entry verified with a real-world fact **per table family** (**U-DATA-1**). When a
  loader's `season` differs from the requested season, set `loader_season_offset` /
  `db_season_offset` — never `{season + 1}` in `asset_url`/`repo_path` (it never
  evaluates, and `replace_partition` swapping the wrong child **destroys** the newer
  season — #36).
- **PLAT-DB-7** `[major]` Partition re-key SQL: per-table transactions (bound the
  ACCESS EXCLUSIVE lock), drop and re-add `<parent>__stg_bound` before `ATTACH`, shift
  `api.ingest_manifest` PKs through a temp table, count partitions with
  `relkind='r'`, exclude partition children from `capture_schema.py`. — (#41)
- **PLAT-DB-8** `[major]` Dtype drift is fixed in the producer, not by widening
  (`_widen_type` is int→bigint→double→text + directional booleans only). Per-season
  errors log `skip_season_error` and do **not** change the exit code — an ingest or
  backfill "succeeded" claim shows a log grep for it. — (#22 `cfb.percentiles` masked
  since registration)
- **PLAT-DB-9** `[blocker]` Access stays locked: no `trust` or `0.0.0.0/0` in
  `pg_hba`; new clients only via `infra/postgresql/allow_client_in_pg_hba.sh`; the
  `postgres` role is NOLOGIN, so units/scripts use peer auth (`User=sdv`,
  `sudo -u sdv psql`); unit files use `/mnt/sdv_repos/sdv-db/…` paths (`/opt/sdv-db`
  does not exist) and the repo copy equals the installed copy.
- **PLAT-DB-10** `[blocker]` Key scopes: `KeyRecord.allows("read")` is true for **any**
  key, so an isolating scope does nothing unless `allows()` and the route dependency
  both change; `write`/`admin` never enter `HTTP_MINTABLE_SCOPES`; delegated
  revoke/rotate fence by owner **and** scope, and wrong-owner vs unknown id return the
  identical 404; `key_hash` never appears in `_META_COLUMNS`. — (#44 + `92b178f`)
- **PLAT-DB-11** `[major]` Shared-secret headers compare with
  `secrets.compare_digest`; keys stored as sha256 only; nothing but `/health` is
  anonymous (`/openapi.json` needs a read key).
- **PLAT-DB-12** `[major]` The generic GET catch-all serves any schema the read role can
  see: a new internal schema never grants USAGE to the API's read role, or is added to
  both `list_schemas` exclusions and `_WRITE_BLOCKED_SCHEMAS`. Exposure of licensed
  schemas (PFF) is an owner decision (**U-SEC-5**).
- **PLAT-DB-13** `[minor]` Paging clamps `1 <= limit <= MAX_LIMIT` (a negative limit
  passes to Postgres → 500); caller-caused DB errors surface as 400.
- **PLAT-DB-14** `[major]` `uv sync --frozen` then `uv run --no-sync`; the sdv-py
  git-branch pin bumps in its own chore commit (a re-lock moved ingest semantics — #36);
  no `path = "../sdv-py"` source.

## sdv-orch — Prefect orchestration (branch `master`, no CI)

`sdv_orch/registry.py` is the catalog; `prefect/flows.py` serves deployments under
`sdv-orch-flows.service`; `sdv_orch/api/runs.py` is mounted **inside** the sdv-db API.

- **PLAT-ORCH-1** `[blocker]` Stage scripts survive the service PATH: call the venv
  interpreter by absolute path behind an `-x` guard (or `/root/.local/bin/uv`), never
  bare `uv run`. Evidence must be an `env -i` reproduction, not an interactive shell.
- **PLAT-ORCH-2** `[major]` A `season_expr` is proven to print the right season —
  `_resolve_season` swallows exceptions and silently falls back to `season_max`. Each
  new season bumps `season_max`.
- **PLAT-ORCH-3** `[blocker]` Schedule cutover: a pipeline with no `crons` gets no
  daily deployment; `serve()` re-applies `paused=not schedule_active` on every restart
  (a UI un-pause is lost); cutover sets `schedule_active=True` **and** disables the
  matching GH Actions workflow in the same change; stays inactive until one green
  end-to-end run is recorded.
- **PLAT-ORCH-4** `[major]` Registry edits state the restarts:
  `systemctl restart sdv-orch-flows` **and** `sdv-db-api` (it imports `sdv_orch`); a new
  rate class is added to `RATE_LIMITS` and registered via `prefect/flows.py setup`.
- **PLAT-ORCH-5** `[major]` Budgets and env are declared, not documented: stages that
  commit hold `_writer(repo)`; stages hitting a shared upstream declare their rate class;
  a transport named in a stage `note` is actually in `env`.
- **PLAT-ORCH-6** `[blocker]` A flow never returns before its futures resolve — every
  `run_stage.submit` is collected and `.result()`ed, `_exec` keeps raising on non-zero rc
  (otherwise the task runner cancels in-flight tasks and the flow reports Completed).
- **PLAT-ORCH-7** `[major]` `runs.py` never imports `prefect`, keeps forwarding
  `PREFECT_API_AUTH_STRING`, validates `stages` against the pipeline and clamps `limit`.
  Arg-style changes (`FLAG_SE` always emits `-r`; `FLAG_ACADEMIC_YEAR` passes
  `season + 1`) are checked against every stage using that style.
- **PLAT-ORCH-8** `[major]` No CI: the PR pastes `pytest tests -q` output; no new
  spike/probe scripts at the repo root.

## sportsdataverse-web — Next.js 16 on Vercel (`frontend/`)

App Router, React 19, Auth.js v5 (GitHub org membership → `isOrgMember`/`role`),
MongoDB, Supabase, server-side proxies to the Data API. **No PR CI** — Vercel builds
production after merge.

- **PLAT-WEB-1** `[blocker]` Frozen external contracts keep path, auth mode and status
  codes: `POST /api/platform/db-status`, `POST /api/platform/runs`, ranged
  `GET /api/platform/datasets/file`, `GET /api/revalidate`.
- **PLAT-WEB-2** `[blocker]` Every `app/api/platform/**` handler starts with
  `requireMemberApp()` / `requireAdminApp()` and returns `deny` **before** touching env
  or keys; CI/ingest routes use the timing-safe, fail-closed `checkIngestToken`.
- **PLAT-WEB-3** `[blocker]` Data API credentials are server-only: never
  `NEXT_PUBLIC_*`, never imported from a `"use client"` module, never in a response
  body; minted keys shown once; a proxy attaching a bearer key checks
  `isHttpsBase(BASE)`. Adding `import "server-only"` to `lib/platform/*-server.ts` is a
  welcome hardening.
- **PLAT-WEB-4** `[major]` Untrusted identifiers are validated before proxying
  (`^[a-z_][a-z0-9_]*$` for schema/table; GitHub logins parsed and ≠ session login);
  Mongo documents map to responses by explicit whitelist, never `{...doc}`;
  `target="_blank"` carries `rel="noreferrer noopener"`.
- **PLAT-WEB-5** `[major]` Next 16 route-handler `params` **is** a Promise
  (`await ctx.params`) — decline bot suggestions to type it as a plain object.
- **PLAT-WEB-6** `[major]` Demand local gates in the PR: `cd frontend && npm run tsc &&
  npm run lint && npm run build`. New env vars go into `frontend/.env.example` +
  `SETUP-platform.md` and the PR body (scope, sensitivity); features degrade to a 503
  JSON when the var is unset.
- **PLAT-WEB-7** `[minor]` GitHub API fan-out stays bounded (`settlePool`, ETag/304),
  releases sort by newest asset.

## sdv-next-clone — study reconstructions (Next.js, CI lint/typecheck/build)

- **PLAT-NC-1** `[blocker]` Never deployed under a domain implying the originals; source
  attribution stays in `src/app/page.tsx`.
- **PLAT-NC-2** `[major]` `AGENTS.md` is the source — run `scripts/sync-agent-rules.sh`
  for the generated agent files; assets in `public/` are `git add`ed; never
  `git add -A` (agent scratch).

## sdv-swagger — public OpenAPI specs (no CI)

- **PLAT-SW-1** `[blocker]` No live tokens, cookies (`__session`, `_premium_key`), JWTs
  or account-bound keys in `example:`/`default:`/`servers:`/descriptions; document the
  scheme only. Auth-gated or paywalled recon is an explicit decision to publish here.
- **PLAT-SW-2** `[major]` Mirrored specs are byte-identical to `sdv-internal-refs`
  (cite the upstream blob; fix the generator there); every add/rename updates the README
  index row; `{sport}`/`{league}` are path params, not forked specs.
- **PLAT-SW-3** `[major]` Specs describe request parameters, not just captured
  responses (Core v2 declared zero query params across 131 ops → silent truncation at
  `pageSize` 25); `required: true` and "silently ignored" notes come from live
  verification. The Data API's own spec lives in sdv-db, never copied here.

## bin/ — droplet ops scripts (local git, no remote, no CI)

- **PLAT-BIN-1** `[blocker]` The repo puller keeps: skip trees with uncommitted changes,
  no `reset`/`stash`/`--force`, `flock -n`, the status log line.
- **PLAT-BIN-2** `[major]` The health monitor never goes silently green: `gh api` errors
  are counted and reported (not `2>/dev/null` into zero rows); FAIL/STALE are the only
  non-zero exits; year matchers are `(?:19|20)\d{2}`.
- **PLAT-BIN-3** `[major]` Cron lines: `mkdir -p logs` before the redirect, dated or
  append logs with `2>&1` (`%` escaped), the `PATH=` header kept; hard-coded season args
  whose month window crosses into the next season are flagged.

## sportsdataverse-data — release host + generated release notes

- **PLAT-REL-1** `[blocker]` Release tag names are a contract — add tags, never rename
  or delete (`load_*` hard-code them).
- **PLAT-REL-2** `[blocker]` Never re-snapshot `data-raw/backup_bodies.json` from live
  release bodies (they are now generated notes; a re-snapshot nests notes inside notes
  on all releases). Durable prose goes in `families.py`.
- **PLAT-REL-3** `[major]` `DRY=1 bash push_notes.sh` first; automation parses the
  `EXIT=` line (the script exits 0 regardless); bodies stay under 125,000 chars; mass
  republishes batch ~40 uploads under the 5,000/hr limit and upload per file.

## universe — r-universe registry

- **PLAT-UNI-1** `[major]` `packages.json` parses; `package` equals the target
  DESCRIPTION `Package:`; `url` uses canonical owner casing; archived upstreams removed;
  "added to r-universe" is verified at `https://sportsdataverse.r-universe.dev/api/packages`
  (third-party entries register only after their owner installs the app).

## Verify

```sh
# sdv-db
uv sync --frozen --all-extras --dev && uv run --no-sync pytest -q && uv run --no-sync ruff check python tests
(cd python && uv run --no-sync --extra api python ../scripts/gen_api.py --check)
for u in systemd/*.service; do diff -q "$u" /etc/systemd/system/$(basename "$u"); done
# sdv-orch
./.venv/bin/python -m pytest tests -q
env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash <repo>/scripts/<stage>.sh -s 2026 -e 2026
# sportsdataverse-web
cd frontend && npm ci && npm run tsc && npm run lint && npm run build
grep -rn "NEXT_PUBLIC_.*KEY\|NEXT_PUBLIC_SDV" app lib components     # must be empty
# sdv-swagger
git diff origin/main | grep -nE '^\+.*(eyJ[A-Za-z0-9_-]{20,}|Bearer [A-Za-z0-9._-]{20,}|_premium_key=|__session=)'
```

Don't paste values from `/etc/sdv-db/sdv-db.env` or `/root/.sdv-*-key` into a review.
