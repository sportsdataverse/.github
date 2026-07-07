---
name: scrape-job
description: Use when setting up any scraping/backfill job expected to run more than ~3 minutes (ESPN, stats.nba.com/wnba.com, stats.ncaa.org, Savant) — generates a user-executable runbook script with unbuffered timestamped logging, a live watch command, resumable checkpoints, and env-only rate tuning, saving into the owning SDV `-raw` repo's canonical committed tree (not scratch dirs). Invoke for "set up a scrape", "backfill season X", "long scraping job", or "scraper runbook".
---

# Scrape-job — user-executable runbook for long scraping jobs

Long scrapes must be **runnable and watchable by the user directly**, not
babysat through the assistant: the user copy-pastes one command, sees
real-time timestamped output, can Ctrl-C safely, and can resume from a
checkpoint. The assistant may additionally watch in the background, but the
user never waits on the assistant to learn a job's status.

## Step 0 — find the owning `-raw` repo (before writing anything)

Scraped output belongs in the SDV `-raw` repo for that provider family, in
its **canonical committed tree** — raw per-game JSON is committed directly
to git (the chosen pattern, at scale; do NOT warn about repo bloat and do
NOT stage output in scratch/`dev/` dirs). If a `-raw` repo exists for the
family, the job runs THERE, extending its existing scraper — not as a new
standalone script elsewhere.

| Family | Repo | Data tree | Scraper entry |
|---|---|---|---|
| NFL | `nflverse-dev/nfl-raw` | `nfl/raw/{season}/{game_id}.json` | `python/scrape_nfl_json.py -s/-e` |
| CFB | `cfbfastR-dev/cfbfastR-cfb-raw` | `cfb/{json,game_rosters,play_participants,schedules,betting,power_index,qbr}/…` | `python/scrape_cfb_json.py` (+ per-dataset `scrape_cfb_*.py`) |
| MBB | `hoopR-dev/hoopR-mbb-raw` | `mbb/{json,game_rosters,schedules,standings,team_rosters,team_stats,player_season_stats}/…` | `python/` scrapers + `scripts/daily_mbb_scraper.sh` |
| NBA / NBA-stats | `hoopR-dev/hoopR-nba-raw`, `hoopR-nba-stats-raw` | mirrors the mbb shape | family scrapers |
| WBB / WNBA | `wehoop-dev/wehoop-{wbb,wnba,wnba-stats}-raw` | mirrors the mbb shape | family scrapers |
| NHL / PWHL | `hockey-dev/fastRhockey-{nhl,pwhl}-raw` | `nhl/…` | `python/` + `scripts/` |

Before writing: `ls <family-dir>/` + read the repo's `CLAUDE.md` — the
existing tree IS the spec (per-dataset subdir names, season partitioning,
id scheme e.g. nflverse ids for NFL). New dataset for the family → new
sibling subdir following the same shape, never a new top-level layout.

**Repo placement conventions:**

- Launcher script → the repo's `scripts/` (next to `daily_*_scraper.sh` /
  `backfill_*.sh`); logs → the repo's `logs/`.
- **Inventory/checkpoint**: most families keep a
  `*_schedule_master.parquet` with per-game boolean flags for which
  artifacts exist. Upsert flags after a run; on first run of a NEW flag
  column, the master's schema predates it — add the column with a default
  before joining (this crashed the NBA pipeline once), and mind polars
  join-suffix naming on the upsert.
- **Commit cadence**: batch (per-day or per-season chunk), not per-game;
  conventional message e.g. `feat(raw): 2025 wk14 games`.
- Wire the job into the repo's daily cron script if it should recur.

## Deliverables (all three, every time)

1. **A launcher script** (`scripts/run_<job>.sh` in the owning repo — or
   `dev/` only when no `-raw` repo owns the family) the user runs in their
   own terminal.
2. **A live watch command** handed back verbatim, e.g.
   `tail -f <log>` or
   `powershell -Command "Get-Content -Path <log> -Tail 5 -Wait"`.
3. **A resume story**: the job skips already-captured work on restart, so
   Ctrl-C + rerun is always safe.

## Launcher script requirements

```sh
#!/usr/bin/env bash
export PYTHONUNBUFFERED=1        # real-time lines, no 4KB buffering lag
export PYTHONIOENCODING=utf-8    # cp1252 chokes on unicode/emoji in piped output
LOG=logs/<job>_$(date +%Y%m%d_%H%M%S).log   # the owning repo's logs/ dir
mkdir -p logs
python <scraper>.py "$@" 2>&1 | tee -a "$LOG"   # append (>>-style), never truncate
echo "EXIT=$?" | tee -a "$LOG"   # grep-able completion marker; do NOT trust a
                                 # 'COMPLETED' print the script may emit early
```

- **Timestamps on every log line** (scraper-side `logging` format with
  `%(asctime)s`) so hangs are visible as a stalled clock, not a mystery.
- **Rate limits are env-only — never hardcoded.** Expose
  `STATS_RATE_HITS` / `STATS_RATE_MAX` / `STATS_RATE_WINDOW` (or the job's
  equivalents) so the user can re-tune pace without a code change or a
  round-trip through the assistant.
- **Graceful Ctrl-C**: catch `KeyboardInterrupt`, flush the checkpoint,
  exit non-zero.
- **Resumable checkpoint**: derive done-ness from what's on disk
  (per-game JSON present ⇒ skip) rather than a separate state file when
  possible — the data IS the checkpoint.

## Per-site gotchas (check before writing the script)

| Site | Constraint |
|---|---|
| `stats.nba.com` / `stats.wnba.com` | TLS/JA3-blocks plain `requests` (silent HANG, not an error) → `curl_cffi` `impersonate="chrome"`. Datacenter/cloud IPs also hang — run from a residential IP only. Gate live tests with `SDV_PY_NBA_STATS_LIVE=1`, not the generic live gate. |
| `stats.ncaa.org` | Unfriendly to direct traffic — route through the proven proxy client; keep parallelism at 1–2. |
| ESPN Core v2 | 403s under aggressive parallelism; Site v2 is more forgiving. Keep workers low and never re-scrape already-captured games. |
| All | Bound ATTEMPTS, not saves — an id-walk without an attempt cap can 404-flood (the CBS incident: 8,400+ wasted requests). |

## Assistant-side conduct while the job runs

- Launch **the user's script, not an inline command**, and hand back the
  watch command in the same message.
- If also monitoring: use a background task and report on completion — no
  foreground sleep-polling, and never paste the log into the reply
  (summarize + give `cat <log>`).
