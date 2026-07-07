---
name: scrape-job
description: Use when setting up any scraping/backfill job expected to run more than ~3 minutes (ESPN, stats.nba.com/wnba.com, stats.ncaa.org, Savant) — generates a user-executable runbook script with unbuffered timestamped logging, a live watch command, resumable checkpoints, and env-only rate tuning. Invoke for "set up a scrape", "backfill season X", "long scraping job", or "scraper runbook".
---

# Scrape-job — user-executable runbook for long scraping jobs

Long scrapes must be **runnable and watchable by the user directly**, not
babysat through the assistant: the user copy-pastes one command, sees
real-time timestamped output, can Ctrl-C safely, and can resume from a
checkpoint. The assistant may additionally watch in the background, but the
user never waits on the assistant to learn a job's status.

## Deliverables (all three, every time)

1. **A launcher script** (`dev/run_<job>.sh` or `.ps1`) the user runs in
   their own terminal.
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
LOG=dev/logs/<job>_$(date +%Y%m%d_%H%M%S).log
mkdir -p dev/logs
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
