# DB/API service lenses (sdv-db, sdv-data, sdv-orch, and the backend half of GOP)

Migrations (`alembic/`, `migrations/`, `*.sql`), systemd units, or a schema/catalog, plus an
API server (FastAPI, Express), a Dockerfile or a compose file. It outranks
`python-package` when those signals exist; a repo whose main deliverable is a web app
carries it as a secondary.

**Safety — stricter than every other archetype:**
- **Never connect to a production database** — not with `psql`, not through the service's
  own CLI, not "read-only". **Never run migrations**, `alembic upgrade`, seed scripts,
  ingest/ETL entry points, or `systemctl` on any host. **Only read from the repo.**
- Live checks are limited to public HTTP health or status endpoints **the repo itself
  documents** (`GET /health`, `/status`, a public status page). No authenticated endpoint,
  no write method, no endpoint found by guessing.
- Secrets: **names only, never values.** Report which env var or secret file a doc names;
  never read `.env`, `/etc/<svc>/*.env`, `~/.Renviron` or a key file, and never quote a value.
- Never call stats.nba.com, stats.wnba.com, stats.ncaa.org or Sports Reference; keep
  `SDV_PY_LIVE_TESTS` and `SDV_PY_NBA_STATS_LIVE` unset; run repo code (tests included)
  only inside `sdv-review-pr`'s `scripts/sandbox.sh` (no network, no secrets) or not at all;
  `--frozen` on every uv command (`uv run --frozen --no-sync`, `uv tree --frozen`).

## 01 contributor-docs

**Files:** `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/**` (schema docs, runbooks,
migrations notes), `alembic/` or `migrations/` / `docs/migrations/*.sql`, `systemd/*`,
`infra/**`, `Dockerfile*`, `docker-compose*.yml`, `.env.example`, `pyproject.toml` /
`package.json`, API app modules (routers), `.github/workflows/*.yml`.

| Claim kind | How to verify |
|---|---|
| Schema docs vs migrations | every table/column the docs describe exists in the migration history (read the SQL / alembic versions in order); dropped or renamed objects still documented are findings |
| Catalog / README tables | the README or catalog's dataset and table lists vs the tables the migrations create and the catalog file declares |
| API docs vs routes | OpenAPI spec (committed `openapi.json`, or the one the docs link) vs the routers' decorators: missing, extra and renamed paths, methods, params |
| Runbooks vs units | each documented timer/service and its schedule vs `systemd/*.timer` `OnCalendar=` and the `ExecStart=` it runs; deploy steps vs the files that exist |
| Backup/restore docs | a documented procedure exists, names the real dump/restore scripts, and states retention; missing entirely is a finding for a database service |
| Secrets documentation | each secret is documented by **name** with where it lives; a doc that embeds a value is a high finding (report the file:line, not the value) |
| Commands | each documented command exists (script, CLI subcommand, make target) and takes the documented flags (read the argparse/typer definition) |

## 02 companions

The consumers and producers around the service: the `-data` producers that feed it,
the web apps and packages that read its API (GOP, sportsdataverse-web, sdv-py helpers).

| Check | How |
|---|---|
| Consumer pins | which version / git rev of this service's client or schema each dependent repo pins (`uv.lock`, `package.json`, a vendored spec) and whether it is behind main |
| Producer contracts | the release tags or tables the ingest reads are the ones the producers publish (names and columns, from the producer repos and the catalog) |
| Spec mirrors | an OpenAPI copy in sdv-swagger or a consumer repo vs this repo's routes |

## 03 coverage

| Check | How |
|---|---|
| Tables vs catalog vs docs | three-way set difference; each side's extras listed |
| Endpoints vs docs vs spec | three-way set difference |
| Units vs runbook | every unit documented; every documented job has a unit |
| Hard-coded counts | `counts` probe ("N tables", "N endpoints", "N datasets") against the measured sets |

## 04 currency

| Area | Commands |
|---|---|
| Data freshness vs crons | the documented schedule vs evidence the repo or a public status endpoint exposes (a status page's last-ingest time, a published heartbeat); never query the database |
| Last deploy | deploy workflow's last run on main; the commit a public `/health` or `/version` reports, if documented, vs main HEAD |
| Dependencies | `uv tree --frozen --outdated --depth 1`; framework currency (FastAPI, SQLAlchemy, alembic, Express) |
| Advisories | `osv` probe on `uv.lock` / `package-lock.json`; for each hit `uv tree --frozen --invert --package <pkg>` (runtime vs dev) |
| CI and crons | `gh run list --branch main --limit 30`; every `schedule:` workflow's last 5 runs |

## 05 polish

Rank: GitHub landing → the public API docs page → a public status page → runbooks.

| Check | How |
|---|---|
| README header | what the service is, who consumes it, how to run it locally against a local database |
| Public API docs | the docs page loads, its examples match the routes, no internal hostnames |
| Leaked internals | `leaks` probe over README, docs, `infra/`, units: droplet IPs, `/root` and `/mnt` paths in public docs, private repo names, credentials in examples |
| Repo About box | description, topics; a private service repo says so |
| Root clutter | tracked `.env`, dumps, logs, `.idea/`, scratch SQL outside the migrations |
