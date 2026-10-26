# JS/TS package lenses (sportsdataverse-js, sdvplot-js and other npm libraries)

A published `package.json` (not `"private": true`, with `main`/`module`/`exports`/`types`/`bin`),
or a workspace whose members are. TypeScript libraries count here. A docs site inside the
repo is a secondary `web-app`: load `web-app.md` for it too.

Read-only: no `npm install` / `pnpm install` in the main checkout (it rewrites the lock).
If a build is needed to compare `exports` with what is emitted, run it in a throwaway copy
(`git -C <W> archive HEAD | tar -x -C <copy>`, then `npm ci` / `pnpm install --frozen-lockfile`)
inside `sdv-review-pr`'s `scripts/sandbox.sh`, or read the committed `dist/` and the
published tarball (`npm view <pkg> dist.tarball`) instead.

**Safety:** never call stats.nba.com, stats.wnba.com, stats.ncaa.org or Sports Reference
(no wrapper calls, live tests or examples that fetch them); keep `SDV_PY_LIVE_TESTS`,
`SDV_PY_NBA_STATS_LIVE` and the package's own live-test toggles unset; run repo code
(builds, tests, scripts) only inside `sdv-review-pr`'s `scripts/sandbox.sh` (no network,
no secrets) or not at all; `--frozen` on any uv command a Python helper needs. Never
`npm publish`, `changeset publish` or `npm dist-tag`.

## 01 contributor-docs

**Files:** `README.md` (root and every published member), `CONTRIBUTING.md`, `CLAUDE.md`,
`AGENTS.md`, `CHANGELOG.md` (per package in a monorepo), `.changeset/*`, `RELEASING.md`,
every `package.json`, `pnpm-workspace.yaml`, `tsconfig*.json`, `typedoc.json`,
`api-extractor*.json`, `.nvmrc`, `.github/ISSUE_TEMPLATE/*`, `.github/pull_request_template.md`,
`.github/workflows/*.yml`.

| Claim kind | How to verify |
|---|---|
| Scripts named in docs (`npm run x`, `pnpm -F pkg x`) | exist in the right workspace's `package.json` |
| Import examples | every `import { x } from "pkg/sub"` resolves through `exports` (a subpath missing from `exports` is not importable) and `x` is exported from that entry |
| ESM/CJS claims | "works with require()" needs a `require` condition or CJS `main`; `"type": "module"` with only `import` conditions is ESM-only |
| Types | `types` / `exports[...].types` point at files the build emits; typedoc / api-extractor configs name the same entries |
| Node support | README / `engines.node` vs `.nvmrc` vs the CI matrix |
| Changesets / CHANGELOG | `fragments` probe (`.changeset/*.md`: valid bump per package, non-empty summary, no internal ids); CHANGELOG top entry vs the published version |
| Bundle size claims | quoted sizes vs the published tarball (`npm view <pkg> dist.unpackedSize`) or a size-limit config |
| Contradictions / jargon | the same fact twice with two values; internal ids, private repos, local paths |

## 02 companions

For sdv-js / sdvplot-js: the `@sportsdataverse/*` packages, the chart libraries they
integrate (React and Svelte are first-class targets: Recharts, nivo, Victory, LayerChart),
and the Python/R siblings whose names they mirror (sdvplot, sdvplotR, sportyR).

| Check | How |
|---|---|
| Peer dependencies | ranges match the versions the examples and docs use; React and Svelte entry points both exist where documented |
| Cross-package versions | workspace packages depend on each other at versions that are published (a `workspace:*` that publishes as an unreleased version breaks installs) |
| Examples / storybook coverage | one row per package: example present, uses the current API, renders in the docs site |
| Naming parity | function and theme names match the Python/R siblings where the docs claim parity |
| Links both directions | npm README ↔ GitHub README ↔ docs site agree; the siblings link back |

## 03 coverage

**Files:** `exports` maps, `src/index.*` barrels, typedoc output config, README API tables,
the docs-site nav (if a secondary `web-app`).

| Check | How |
|---|---|
| Public surface vs docs | every `exports` entry and barrel export appears in the README/API docs; nothing documented is unexported |
| Files shipped | `files` / `.npmignore` vs what docs promise (types, CSS, fixtures); `npm pack --dry-run` in the copy lists them |
| Hard-coded counts | `counts` probe ("N themes", "N chart types") against the barrel |
| Naming | one display name per package across README, docs site and npm |

## 04 currency

| Area | Commands |
|---|---|
| Release | `release` probe: `--npm <pkg>` for one package, `--workspaces` for a monorepo (every published member vs npm vs its `@scope/pkg@x.y.z` tag); GitHub Releases per tag |
| Unreleased | pending `.changeset/*.md` count and bump levels; commits since each member's tag |
| Provenance | trusted publishing: `npm view <pkg> --json` shows `dist.attestations` / provenance for the latest version; the publish workflow uses OIDC (`id-token: write`), not a long-lived `NPM_TOKEN` |
| Outdated deps | `npm outdated --json` / `pnpm outdated` in the throwaway copy, or direct deps against `registry.npmjs.org/<pkg>/latest` |
| Advisories | `osv` probe on `package-lock.json`, `pnpm-lock.yaml` or `yarn.lock` |
| CI and crons | `gh run list --branch main --limit 30`; every `schedule:` workflow's last 5 runs |
| Docs site | if a secondary `web-app`: deploy SHA vs main (`web-app.md` 04) |

## 05 polish

Rank: npm page → GitHub landing → docs home → API reference → examples → 404.

| Check | How |
|---|---|
| npm page | `description`, `keywords`, `repository`, `homepage`, `license` set and current (`npm view <pkg> --json`) |
| README header | badges resolve and agree (npm version, CI, bundle size), install line names the scoped package |
| Repo About box | `gh repo view o/r --json description,repositoryTopics,homepageUrl` |
| Leaked internals | `leaks` probe over `src/`, `README*`, docs; published source maps exposing local paths (`npm view <pkg> dist.tarball`, look for `*.map` with absolute `sources`) |
| Root clutter | stray probe/output files, tracked `dist/` that disagrees with the build, duplicate configs |
