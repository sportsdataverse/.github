# web-gop — Game on Paper (`saiemgilani/game-on-paper-app`)

Review target is `saiemgilani/game-on-paper-app` (`blackcb/…` is a fork; the local
`game-on-paper-app-cloudflare` checkout is parked — never review against it). Human
co-maintainer **akeaswaran** reviews design and conventions; Sourcery and CodeRabbit
review the rest.

**Architecture.**
- `astro/`: Astro SSR on Cloudflare Workers (`@astrojs/cloudflare`, exact-pinned —
  newer astro/adapter pairs break the workerd build), Svelte 5 islands, Bootstrap 5,
  dark mode from `prefers-color-scheme`. KV: `SESSION`, `SDV_API_CACHE`,
  `ESPN_API_CACHE`.
- `python/`: Flask/gunicorn processor in Docker on the DO API host; the image
  resolves **sportsdataverse-py `main` at build time** (`uv lock --upgrade-package`),
  so `uv.lock` alone neither ships nor blocks an sdv-py fix.
- Data: ESPN (via `resources/espn.ts`, relay through `espn_proxy.py` when Akamai
  403s Worker egress), the processor, the SDV Data API (`resources/sdv.ts`).
- **Caching:** Cloudflare Workers Caching with per-route `Astro.cache.set({maxAge,
  swr, tags})`. A cache HIT never runs the Worker or middleware. Completed games cache
  ~1 year; zone purges don't reach Workers Caching — only the Worker's
  `/admin/api/purge-game` or a deploy clears it.
- **Routing:** redirect/404/cache decisions live in `src/routes/*.ts` loaders; NFL is
  an explicit `src/pages/nfl/**` tree; legacy `/cfb/*` resolves in middleware.
- **Flags** (`astro/src/utils/features.ts`): `game-page-v2`, `scoreboard-compact`,
  `nfl` are `'preview'`. The **public** sees the frozen `components/game/classic/*`
  game page and a 404 on `/nfl`.
- **CI:** `test.yml` runs vitest + pytest; `pr-evidence.yml` posts a 4-shot screenshot
  matrix + base-vs-head Lighthouse as one `<!-- pr-evidence -->` comment (and flips
  every preview flag ON, so it **cannot see classic or the NFL 404**); `deploy.yml` on
  push to main and on `repository_dispatch` from sdv-py. **`astro check` is not a gate**
  (it has a large pre-existing error baseline — compare base vs head counts).

## Caching (Workers Caching)

- **GOP-CACHE-1** `[blocker]` Every "don't cache" path sets
  `Astro.response.headers.set("Cache-Control", "no-store")` **alongside**
  `Astro.cache.set(false)` — a bare `set(false)` emits no header, and Workers Caching
  holds header-less 200s for a heuristic ~2 h. — (`311d80e` froze live games)
- **GOP-CACHE-2** `[blocker]` Responses that vary by viewer (admin auth, preview
  cookie, `?preview_key=`, `/preview/*`) go through `withPreviewCacheGuard` or send
  no-store — a HIT skips auth. — (`821ff6a` cached authenticated `/admin` 200s; #217;
  akeaswaran on #213: keyed URLs get cached with the key)
- **GOP-CACHE-3** `[major]` Error/"unavailable" fallback renders don't keep the page's
  normal TTL. — (Sourcery on #228: rankings cached the ESPN-down page for 1 h + SWR)
- **GOP-CACHE-4** `[major]` A new cache tag is also added to `KNOWN_TAGS` in
  `pages/admin/api/purge-game.ts`, or `purge-game-cache.yml` rejects it with a 400.
- **GOP-CACHE-5** `[major]` Processor output changes for the same repo SHA rely on
  `APP_VERSION = ${sha}-${run_id}` in the processor fetch `cf.cacheKey` — never drop
  `run_id` (an sdv-py `repository_dispatch` redeploy reuses the SHA). — (#176)
- **GOP-CACHE-6** `[major]` Staleness/regression guards treat absent as unknown, not
  zero, and count **distinct** ids (ESPN repeats `drives.current` inside
  `drives.previous`); KV writes only on change (1 write/sec/key) and fail open. —
  (`807c287`, `311d80e`, `94469d1`)

## Routing and rendering

- **GOP-ROUTE-1** `[blocker]` No `Astro.rewrite()`/`Astro.redirect()` inside a
  **component** — it aborts the stream into an empty HTTP 200. Loaders return the
  decision; the page frontmatter acts on it. — (`62a76e0`/#227)
- **GOP-ROUTE-2** `[blocker]` Game-page component frontmatter changes keep
  `test/gamePage.render.test.ts` (Container API render of a real fixture) passing and
  extend it for new branches — a frontmatter throw also ships an empty 200 while
  `astro build` stays green. — (`f45dbf0`/#183 blanked every finished game)
- **GOP-ROUTE-3** `[major]` A page handles **every** variant its loader returns
  (`'redirect' in r`, `'notFound' in r`); otherwise the marker object renders
  "undefined …" as a 200. — (#230; `test/explicitRoutes.test.ts`)
- **GOP-ROUTE-4** `[blocker]` Middleware never lets a path rewrite carry a request past
  a gate that checked the **original** pathname: `/preview/admin/*` and `/nfl/admin/*`
  bounce, never rewrite. — (Sourcery on #217 critical; CodeRabbit on #229 CWE-288)
- **GOP-ROUTE-5** `[major]` `<script is:inline>` placed before the DOM it queries wires
  nothing — prefer a bundled `<script>` reading its target from `dataset`; test
  behaviour, not hook presence. — (`5d4c6dc`, PlayFilters inert in every browser)
- **GOP-ROUTE-6** `[major]` Nav anchors render under the same condition as their target
  panel; ids never collide with Svelte canvas ids (`wpChart`/`epChart`). — (#199 charts
  never drew)
- **GOP-ROUTE-7** `[minor]` Optional classes via `cx()`, team colors via
  `teamColorHex()`; never interpolate a possibly-undefined value into markup (`class`
  literally `undefined`; ESPN omitting `color` 500'd `/team/[id]`).

## Payload and performance

- **GOP-PERF-1** `[major]` Svelte island props are serialized into the HTML: pass only
  the fields the island reads, never whole `ProcessedPlay`/`ProcessedGame` objects, and
  never per-row. — (#208: 25 DriveChart islands were 4.4 MB, 84% of the page)
- **GOP-PERF-2** `[major]` Any PR touching `astro/**` or `python/**` has a green
  `<!-- pr-evidence -->` comment; a 🔴 regression has a cause or fix in the body;
  hand-pasted numbers are rejected; deltas the comment labels noise are not raised;
  live-game routes discount their deltas.
- **GOP-PERF-3** `[minor]` `Evidence routes:` names the pages the diff changes (≤4); a
  league-specific change lists the `/nfl` route **and** its CFB twin.

## Classic twin and flags

- **GOP-TWIN-1** `[major]` A fix to any v2 game-page component
  (`components/game/**` outside `classic/`) is checked against its twin in
  `components/game/classic/` (GamePage, PlayRow, PlaysTable, PlayerBoxScore,
  BinionBoxScore, TeamMetricsTable) and mirrored in the same PR — ideally by moving the
  logic into `astro/src/utils/`. pr-evidence cannot see classic, so a user-visible fix
  also needs a classic render assertion or a post-deploy smoke of the public URL. —
  (#250 fixed v2 only; #251 followed after the smoke)
- **GOP-TWIN-2** `[major]` Preview-gated work stays behind its flag; promotion is its
  own `'preview'→'on'` change that deletes the twin and flag-scoped guards (the `?span=`
  guard, classic/) in the same change and re-checks sitemap/header. Changelog entries
  never announce flagged or unbuilt features. An `nfl` promotion cites a fresh week
  audit.

## League awareness (cfb vs nfl)

- **GOP-LEAGUE-1** `[major]` No hard-coded `teamlogos/ncaa/500/<id>` in anything an NFL
  page can render — `teamLogoUrl(league, id, dark)` / `espnLogoLeague()` (NFL dark logos
  are abbreviation-keyed). Flag any PR that newly exposes an existing hard-coded logo to
  NFL.
- **GOP-LEAGUE-2** `[major]` League config, not CFB constants: `LEAGUES[league].teamCount`
  (not 134), schedule/cache config per league, `teamCategoriesFor(league)` for column
  sets. Shared-component changes for NFL can break **public** CFB pages. — (`f0c0505`/#233
  union of columns 400'd every college team profile for ~2 h)
- **GOP-LEAGUE-3** `[major]` A page selecting a new Data API column merges after the API
  serves it (nfl-data → sdv-db ingest → API restart → GOP); the PR body names the
  dependency and its deploy state.
- **GOP-LEAGUE-4** `[major]` Each league-aware page under `src/pages/` has a
  `src/pages/nfl/` twin (or is listed in `leagueless`/`cfbOnly` with a reason); no
  middleware rewrites for leagues (akeaswaran on #229).

## Football semantics

- **GOP-FB-1** `[blocker]` Drive-level answers come from the drives grouping
  (`game.drives`, `drive.team` = offense), never plays grouped by `drive.id` + `pos_team`;
  dedupe `current` vs `previous`, in TS and Python; ask for a partition test (team totals
  sum to the drive total). — (**U-DATA-6**; #247)
- **GOP-FB-2** `[major]` Play classification/shading trusts processor flags
  (`downs_turnover`, `turnover_vec`, blocked-kick flags) over yardage or text heuristics,
  excludes penalties and no-plays, and lives in a tested `astro/src/utils/*` helper — and
  the shading predicate agrees with the play-icon predicate. — (#250, #172 receiving line
  printed catches as TDs)
- **GOP-FB-3** `[major]` Nullable numerics (`period`, `net_adj_epa`, precision) are
  null-checked — 0 is valid and null is not 0. Player attribution keys on (team, id,
  role), never name alone; fumble recoveries belong to the recovering team.
- **GOP-FB-4** `[minor]` Official-scoring conventions differ by league (NFL sacks are
  neither rush nor pass attempts; CFB sacks are rushes); DQ/box code takes `league`.

## Python processor

- **GOP-PY-1** `[blocker]` A new runtime import in `python/app.py` is importable in the
  image: the Dockerfile copies top-level `*.py` only, so a new package directory or data
  file (`sql/`, `tools/`, fixtures) is not shipped. — (`07a2a28` `espn_proxy.py` missing
  → gunicorn crash-loop, 503 on every game page)
- **GOP-PY-2** `[blocker]` Merges/rebases touching `python/app.py` are marker-free and
  parse (**U-GIT-1**). — (#224 → #239)
- **GOP-PY-3** `[major]` Work that must affect the response runs **before** the orjson
  fast-path `return` (code after it is dead — #192, #206).
- **GOP-PY-4** `[major]` Optional enrichments fail open **individually** and log once
  what was skipped (**U-FAIL-5**); sometimes-absent ESPN fields use `.get()`.
- **GOP-PY-5** `[major]` General football metrics belong in **sportsdataverse-py**
  (akeaswaran on #221); GOP Python is glue. A PR relying on an sdv-py fix names the
  sdv-py PR/commit and confirms it is on `main`.
- **GOP-PY-6** `[minor]` New `python/sql/*.sql` migrations are applied by hand to the
  sdv-data `gop` schema — the PR states whether it was applied before merge (writers fail
  open, so silently).

## Workers runtime and security

- **GOP-WORKER-1** `[major]` `waitUntil` uses `locals.cfContext` (`locals.runtime.ctx`
  throws on adapter v14 — inside a fail-open try/catch it silently cancels background
  POSTs); fetch `redirect` is only `"follow"`/`"manual"` on workerd (`"error"` threw at
  the edge — #222). Don't flag `btoa`/`AbortSignal.timeout` as unavailable.
- **GOP-WORKER-2** `[major]` Admin endpoints take the actor from `locals.adminActor`,
  validate booleans strictly (`{"on":"false"}` enabled preview — #193), reject `//` and
  `\` redirect targets and verify origin (#213), and report success only after it
  happened. Relays attaching the bearer token require https.
- **GOP-WORKER-3** `[minor]` `PYTHON_HTTP_URL` stays a plaintext var (a same-name secret
  collides with the binding); new secrets land in `wrangler.jsonc secrets.required`,
  `deploy.yml`, and `vitest.config.ts` dummies.

## Tests and dependencies

- **GOP-TEST-1** `[major]` Tests fail when the guarded thing regresses: `toMatch`, not
  `toContain(regex)`; exact counts; no `if (fixtureHasX)` silent skips; call real
  functions rather than regex-matching source; fixtures committed with the test.
  Classification or shading changes replay old vs new logic over the committed
  processed-game fixtures (`astro/test/fixtures/*.json.gz`, CFB **and** NFL) and, for
  breadth, a season parquet with processor flags
  (`cfbfastR-cfb-data/cfb/pbp/parquet/`, `nfl-data/out/espn_nfl/pbp/`) — a CFB-only
  replay missed new NFL behaviour in a past review.
- **GOP-DEP-1** `[major]` `astro/package.json` changes come with a regenerated tracked
  `package-lock.json`; build-critical packages stay exact-pinned; no `../` paths in the
  lockfile (generated through a symlinked worktree `node_modules`).

## Site conventions (akeaswaran's recurring review)

- **GOP-UI-1** `[minor]` Good/bad coloring is **green/purple**, not green/red.
- **GOP-UI-2** `[minor]` Team logos honor dark mode and per-team override classes
  (`team-logo-<id>`, `DarkModeLogos`); team text goes through `cleanField` /
  `cleanLocation` / `cleanAbbreviation`.
- **GOP-UI-3** `[minor]` Game-page sections are `GenericPanel`, not cards; metric labels
  reuse existing names ("Success Rate", "Explosive Play Rate", "Havoc Rate",
  "Opportunity Conversion Rate"); separators are dashes/colons/slashes, not "·"; team
  columns left-justified, numerics centered, abbreviations on small screens.
- **GOP-UI-4** `[minor]` Pages with no request-time data are `prerender = true`
  (advertised with a trailing slash); canonical/og:url derive from `Astro.url.pathname`;
  one JSON-LD `<script>` per object, matching visible content.
- **GOP-UI-5** `[minor]` No references to surveyed competitor sites in commits, PR
  bodies, code comments, or `pr-assets`/`pr-previews`.

## Verify (droplet)

Node is not on PATH in tool shells; use `/mnt/sdv_repos/.node22/bin`. glibc 2.31 blocks
workerd, so `astro dev|build|preview` need Docker (`node:22-bookworm`).

```sh
export PATH=/mnt/sdv_repos/.node22/bin:$PATH
cd <tree>/astro && npm ci                                                 # ~30 s; never symlink the canonical node_modules
node node_modules/vitest/vitest.mjs run                                   # add --silent=false to see console.log from replay scripts
cd <tree>/python && PYTHON_HTTP_TOKEN=test uv run --frozen pytest -q -p no:cacheprovider
cd <tree>/astro && node node_modules/astro/bin/astro.mjs check 2>&1 | tail -3   # head error count
# base count without a second install: swap only the changed files back, re-run, restore
for f in $(gh pr diff <N> -R saiemgilani/game-on-paper-app --name-only | grep '^astro/'); do
  git -C /mnt/sdv_repos/game-on-paper-app show <base-sha>:"$f" > "<tree>/$f" 2>/dev/null || rm -f "<tree>/$f"; done
python3 -c "import ast; ast.parse(open('python/app.py').read())"          # GOP-PY-2
ls astro/src/components/game/classic/                                     # GOP-TWIN-1
gh pr view <N> -R saiemgilani/game-on-paper-app --comments | grep -A40 'pr-evidence'   # GOP-PERF-2
curl -sI https://gameonpaper.com/game/<id> | grep -iE 'HTTP/|cf-cache-status|cache-control'   # post-merge public (classic) smoke
```

Processor listens on 5000 with a base64 bearer; kill the gunicorn master PID, never
`pkill -f gunicorn` (matches the harness shell).
