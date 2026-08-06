# `-raw` producer conventions

- Scraping-only. Never add ML/model deps or reshaping/publish logic here —
  that's the sibling `-data` repo's job.
- Raw per-game JSON is committed directly to git (the chosen pattern, at
  scale) — do not warn about repo bloat, do not stage output in `dev/`.
- The `-raw`/`-data` boundary is one-way: raw repos never import from data
  repos and never grow modeling deps.
- Placement decides lifecycle: durable stage logic in `python/<pkg>/`;
  `scripts/` is drivers/launchers ONLY (every file must be referenced by a
  README run-order, workflow, or another driver — the orphan-scripts CI
  gate enforces this); `ops/oneoff/` for dated one-shots
  (`YYYYMMDD_<what>.py`); `dev/`/scratchpad is the default birthplace — a
  script earns `scripts/` only by being wired into the runbook in the same
  commit.
- Stage numbering `espn_{lg}_NN_{name}_scrape.py`: 01 schedules, 02 pbp, 03
  standings, … 99 master. A missing dataset leaves a HOLE — never compact
  the numbers. `NN_` = intended build order, not run order.
- Idempotency: season/date as CLI args; resume = skip-already-captured WITH
  a validity check (presence is not validity — never persist an empty
  payload); atomic writes (tmp+rename); boolean CLI flags use tolerant
  `str2bool` (never `argparse type=bool`).
- Rate limits are env-only, never hardcoded (`STATS_RATE_HITS/MAX/WINDOW`
  or the family's equivalent).
- Launcher scripts: `PYTHONUNBUFFERED=1`, `PYTHONIOENCODING=utf-8`, log in
  append mode with timestamps on every line, `echo EXIT=$?` as the
  grep-able completion marker.
- Per-site rate discipline: `stats.nba.com`/`stats.wnba.com` TLS/JA3-block
  plain `requests` (silent hang) — use `curl_cffi impersonate="chrome"`
  from a residential IP; `stats.ncaa.org` route through the proven proxy
  client at parallelism 1–2; ESPN Core v2 403s under aggressive
  parallelism — keep workers low, never re-scrape captured games.
- Commit cadence: batch (per-day/per-season), not per-game; Conventional
  Commits, no AI co-author trailer.
