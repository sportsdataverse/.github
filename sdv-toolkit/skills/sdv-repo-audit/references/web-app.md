# Web-app lenses (game-on-paper-app, sportsdataverse-web, blazing-the-nets, docs sites)

A `package.json` with a framework dependency or config (`next`, `astro`, `@docusaurus/core`,
`@sveltejs/kit`, `remix`, `nuxt`, a vite app with `index.html`) at the root, or in a subdir
when the root has no manifest (GOP's `astro/`). A docs site inside a library repo is this
archetype as a **secondary**: audit the site with this file and the library with its own.

Read-only: no `npm install` in the main checkout (it rewrites the lock). Builds run only in
a throwaway copy inside `sdv-review-pr`'s `scripts/sandbox.sh`. Never trigger a deploy,
a revalidation hook, or a cache purge.

**Safety:** never call stats.nba.com, stats.wnba.com, stats.ncaa.org or Sports Reference
(pages that proxy them are checked from their code and the deployed static output, never
by hitting the source); keep `SDV_PY_LIVE_TESTS` and `SDV_PY_NBA_STATS_LIVE` unset; run
repo code only inside `sdv-review-pr`'s `scripts/sandbox.sh` (no network, no secrets) or
not at all; `--frozen` on any uv command a Python helper needs. **Env vars: names only,
never values** — never print, log or quote a value from `.env`, a deploy dashboard or a
secret store; never read `.env` (read `.env.example`).

## 01 contributor-docs

**Files:** `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, `package.json` (every
app dir), `.nvmrc` / `engines`, `.env.example`, framework config (`next.config.*`,
`astro.config.*`, `docusaurus.config.*`, `svelte.config.*`), `vercel.json`, `wrangler.toml`,
`docker-compose*.yml`, `.github/workflows/*.yml`, `docs/` runbooks.

| Claim kind | How to verify |
|---|---|
| Scripts and dev setup | every documented command exists in `package.json` scripts; the documented Node version matches `engines`, `.nvmrc` and CI |
| Env vars | each name in docs and `.env.example` vs `process.env.X` / `import.meta.env.X` / `Astro.env` reads in code: documented-but-unread and read-but-undocumented are both findings; report **names only** |
| Deploy docs | the documented target (Vercel, gh-pages, Cloudflare, a droplet compose stack) matches the config files and workflows that actually deploy |
| Architecture claims | routes, data sources and API endpoints named in docs exist in the code |
| Contradictions / jargon | the same fact twice with two values; internal ids, private repos, local paths, droplet IPs |

## 02 companions

The data the app renders and the packages it depends on: sdv-py / sdv-db / sdv-data
endpoints for GOP and sportsdataverse-web, sdvplot-js for charts, the docs generator for a
docs site.

| Check | How |
|---|---|
| Data contracts | the endpoints or release assets the app reads exist and still return the fields it uses (read the documented public endpoint or the asset; no credentials) |
| Shared packages | `@sportsdataverse/*` versions vs the latest published; local `file:`/`link:` deps that only work on one machine |
| Twin pages | a feature fixed in one page/route also exists in its public twin (classic vs new page in GOP) |
| Links both directions | the app links the packages and docs it is built on; they link back |

## 03 coverage

**Files:** routes (`src/pages/**`, `app/**`, `src/routes/**`, `docs/**` for Docusaurus),
nav / sidebar config, `sitemap.xml` source, the data registry the site renders (leagues,
sports), the home page component.

| Check | How |
|---|---|
| Live routes vs nav vs sitemap | every route reachable from the nav or an index; every nav entry and sitemap URL returns 200 (sample via WebFetch) |
| Registry vs pages | every league/sport the data layer supports has a page, and no page for a dropped one |
| 404 handling | a custom 404 exists and unknown ids render it (not a 500 or a blank page) |
| Hard-coded counts | `counts` probe over pages and components |
| Naming | display names from one source, not re-typed per page |

## 04 currency

| Area | Commands |
|---|---|
| Deploy freshness | Vercel/Pages: `gh api repos/o/r/deployments?per_page=5` sha vs main HEAD; gh-pages: head commit of the `gh-pages` branch; live `Last-Modified` / build id |
| Deploy status | last deploy workflow run on main succeeded; a `disabled_manually` deploy workflow is deliberate or a finding |
| Framework currency | framework version vs npm latest (`next`, `astro`, `@docusaurus/core`, `@sveltejs/kit`); a major behind is a finding with the upgrade note |
| Outdated deps | `npm outdated --json` in the throwaway copy, or direct deps against the registry |
| Advisories | `osv` probe on `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`, plus any Python backend lock |
| CI and crons | `gh run list --branch main --limit 30`; every `schedule:` workflow's last 5 runs |

## 05 polish

Rank: live home → top pages by nav order → a deep page (game, team, reference) → 404 → GitHub landing.

| Check | How |
|---|---|
| Metadata | `<title>`, meta description, canonical URL, og:image / twitter card on the BUILT HTML (WebFetch the live page, not the source), favicon |
| Lighthouse-level basics | images have alt text and dimensions, headings in order, link text not "click here", no layout-shifting hero |
| Screenshots | README and docs screenshots match the current UI (a renamed nav item or old theme is stale) |
| Analytics and privacy | which analytics run (Vercel, Plausible, GA), and whether a privacy note or cookie notice says so |
| 404 and robots | custom 404; `robots.txt` and `sitemap.xml` live and current |
| Leaked internals | `leaks` probe over `src/`, `public/`, docs; production source maps exposing local paths; admin routes reachable without auth |
| Repo About box | description, topics, homepage |
| Root clutter | stray proposals, captures, build output, tracked `.env*` |
