# Web lenses (sportsdataverse-js, sdvplot-js, game-on-paper-app, sportsdataverse-web, docs sites)

Read-only: no `npm install` in the main checkout (it rewrites the lock); if a build or
script must run, install in a throwaway copy with `npm ci`. Never trigger a deploy.

## 01 contributor-docs

**Files:** `README.md` (root and per-package in a monorepo), `CONTRIBUTING.md`, `CLAUDE.md`,
`AGENTS.md`, `CHANGELOG.md` / `.changeset/*`, `package.json` (every workspace),
`.nvmrc` / `engines`, `.env.example`, `.github/ISSUE_TEMPLATE/*`, `.github/pull_request_template.md`,
`.github/workflows/*.yml`.

| Claim kind | How to verify |
|---|---|
| Scripts named in docs (`npm run x`) | exist in the right workspace's `package.json` |
| Node version | docs vs `engines` vs `.nvmrc` vs the CI matrix |
| Env vars | `.env.example` and docs vs `process.env.X` / `import.meta.env.X` in code; a documented var nothing reads, or a read var nothing documents |
| Package names and exports | `@sportsdataverse/*` names in docs vs `package.json` `name`/`exports`; import examples resolve |
| Changesets / changelog | pending changesets vs the claimed next version |
| Contradictions / jargon | same fact twice with two values; internal ids, private repos, local paths |

## 02 companions

For sdv-js / sdvplot-js: React and Svelte are first-class targets; the companion set is
the published `@sportsdataverse/*` packages and the chart libraries they integrate.
For GOP / sportsdataverse-web: the sdv-py / sdv-db data they render.

| Check | How |
|---|---|
| Peer deps | ranges match the versions the examples use; React and Svelte entry points both exist where documented |
| Examples / storybook coverage | one row per package: example present? renders? uses current API? |
| Cross-package versions | workspace packages depend on each other at the published versions |
| Links both directions | docs site ↔ npm README ↔ GitHub README agree on URLs |

## 03 coverage

**Files:** routes (`src/pages/**`, `app/**`), nav/sidebar config, sitemap, the data registry
the site renders (leagues, sports), home page component.

| Check | How |
|---|---|
| Nav vs routes | every route reachable from nav or an index; no nav entry 404s (live sample via WebFetch) |
| Registry vs pages | every league/sport the data layer supports has a page, and no page for a dropped one |
| Hard-coded counts | `counts` probe over pages and components |
| Naming | display names from one source, not re-typed per page |

## 04 currency

| Area | Commands |
|---|---|
| Release | `release` probe (`--npm <pkg>`) per published package; tags vs GitHub Releases |
| Outdated deps | `npm outdated --json` in a throwaway copy (or read the lock against `registry.npmjs.org/<pkg>/latest` for direct deps) |
| Advisories | `osv` probe on `package-lock.json` |
| Deploy freshness | `gh api repos/o/r/deployments?per_page=5` (Vercel/Pages) sha vs main HEAD; live `Last-Modified` |
| CI and crons | `gh run list --branch main --limit 30`; every `schedule:` workflow's last 5 runs |

## 05 polish

Rank: live home → top pages by traffic or nav order → npm page → GitHub landing → 404.

| Check | How |
|---|---|
| Metadata | `<title>`, meta description, og:image/twitter card on the BUILT HTML (WebFetch the live page), favicon, canonical URL |
| Home page | value statement, install/usage line, working primary action above the fold |
| Accessibility basics | images have alt text, headings in order, link text not "click here" |
| 404 and robots | custom 404 exists; `robots.txt` and `sitemap.xml` live and current |
| Leaked internals | `leaks` probe over `src/`, `public/`, docs; source maps published to production expose local paths |
| Repo About box | description, topics, homepage |
| Root clutter | stray build output, tracked `.env*`, duplicate configs |
