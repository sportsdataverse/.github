---
name: sdv-reprocess
description: Use when a -raw corpus has to be rebuilt because sportsdataverse-py changed what it produces — after an sdv-py fix to play types, EPA/WPA or end states lands, on a SCHEMA_REV bump, or for "rev-N reprocess", "rebuild the finals", "bump the lock and reprocess", "re-run the corpus after the sdv-py fix". Phases — (1) gather every sdv-py PR the run must carry BEFORE bumping, because the processing stamp embeds the sdv-py commit and a later bump re-stales the whole corpus, (2) lock + SCHEMA_REV bump PRs in the -raw and -data repos under the shared locks, venv sync, stamp check, (3) clear the runway — the daily scrape/build chain, the :40 git_pull sweep, other sessions' rebuild jobs on the same locks, (4) launch `scripts/reprocess_chain.sh --data` detached and hand over watch commands, (5) the failure modes and their fixes (a season timing out on /tmp/git_pull_sdv.lock, a daemonized `git gc` holding it, git 2.25 ignoring GIT_CONFIG_COUNT, stopping by PID, a new sdv-py fix mid-run), (6) close-out. cfbfastR-cfb-raw / cfbfastR-cfb-data is the worked example.
---

# Reprocess a -raw corpus after an sdv-py change

A -raw repo's finals are stamped `<sdv-py version>+<sdv-py commit>.<SCHEMA_REV>`
(cfbfastR-cfb-raw: `PROCESSING_VERSION`, `python/cfb_raw_scrape/_cfb_raw_utils.py`). Moving
the lock re-stales every final; the reprocess rebuilds them season by season, then the -data
repo recompiles and republishes every dataset from them. A full CFB run is ~23 seasons at
~25-30 min each for the raw side, then hours per season for -data. Every step below cost a
restart on 2026-10-01 (rev 13); the incidents are in the ClaudeCowork ledger
`ledgers/2026-09-30-cfbd-return-docs/LEDGER.md`.

## Phase 1 — gather before you bump

- Not every sdv-py change needs a reprocess: a change to processed output (play types,
  EP/WP, end states, dropped or added rows) does; docs, loaders and codegen do not.
- **But the stamp carries the commit.** If the lock moves to include a docs-only PR after the
  run, every final goes stale again. List the open sdv-py PRs and ask which ones the run should
  carry ("wait for #650 to land too"). If one is red and idle, ask whether to take it over or
  keep waiting; do not decide for its owner.
- If an R sibling ports the same logic (cfbfastR's v2 engine ports sdv-py's relabels), its
  port is a separate PR and does not gate the reprocess.

## Phase 2 — bump, under the locks

- -raw: `uv lock --upgrade-package sportsdataverse`, and bump `SCHEMA_REV` with a comment that
  names the PRs and "every <old stamp> final must rebuild". A docs-only re-lock keeps the
  SCHEMA_REV (the commit already moves the stamp).
- -data: the same lock bump.
- Branch IN PLACE in the main checkout (never `git worktree add` cfbfastR-cfb-raw: a 4 GB
  checkout), holding the locks for the whole branch → PR → merge → switch-back cycle:
  `flock -w 600 /tmp/git_pull_sdv.lock bash -c '...'` (-data also holds
  `/tmp/cfbfastR-cfb-data-build.lock`). Then `uv sync` both, and check the stamp:
  `.venv/bin/python -c 'import sys; sys.path.insert(0, "python"); from cfb_raw_scrape._cfb_raw_utils import PROCESSING_VERSION; print(PROCESSING_VERSION)'`

## Phase 3 — clear the runway

- `fuser -v /tmp/git_pull_sdv.lock /tmp/cfbfastR-cfb-data-build.lock` and `ps` for the daily
  chain (`daily_cfb_scraper.sh` → `cron_daily_cfb.sh` → `daily_cfb_processor.sh`, launched 04:05
  ET; a 2026 daily build runs ~4.5 h) and for other sessions' jobs (`/mnt/sdv_repos/tmp/*/run.sh`).
- The daily chain: if the user cancels it ("no games last night"), kill its process tree BY
  PID, then restore the partial outputs it left (`git checkout -- <the season's parquets>`),
  or `cron_daily_cfb.sh` refuses the dirty tree later.
- Another session's job: leave it alone. It takes the same locks; the chain waits for it.
  Tell the user if the two overlap (a -data rebuild of every dataset supersedes a narrower
  republish) and let them decide.

## Phase 4 — launch

```bash
cd /mnt/sdv_repos/cfbfastR-cfb-raw
setsid nohup bash scripts/reprocess_chain.sh --data >/dev/null 2>&1 </dev/null &
```

It prints its log path and a watch command and ends with `chain done` / `EXIT=`. Check the
first season's log for `target processing_version : <new stamp>` and `to rebuild : <all>`.
Give the user the watch commands. A background watcher caps at 2 h: re-arm it at most once —
the chain drives itself, and `--data` starts the -data side when the raw side is clean.

## Phase 5 — when it goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| `season Y exit 1`, "no lock after Ns, held by:" | the :40 git_pull sweep, the daily chain, another job | the chain waits 3 h by default; rerun the listed seasons: `SEASONS="2011 2010" bash scripts/reprocess_chain.sh --data` |
| the lock held by `git gc --auto` / `git repack` | a daemonized gc after a commit inherited the lock's fd (held it 45 min) | fixed in `scripts/_commit.sh` (gc.auto=0); if it recurs and no `.tmp-*` pack exists yet, killing it is safe |
| `GIT_CONFIG_COUNT=…` had no effect | git 2.25 on the droplet; that variable is 2.31+ | `export GIT_CONFIG_PARAMETERS="'gc.auto=0'"`; check with `git config --get gc.auto` |
| need to stop the chain | — | kill BY PID: `ps -eo pid,args \| awk '$3=="scripts/reprocess_chain.sh"'`. Never `pkill -f` a pattern your own shell's command line contains (exit 144, self-kill); never edit a running bash script — stop and relaunch |
| a new sdv-py fix lands mid-run | — | stop between seasons, bump again (Phase 2), relaunch; finals already at the new stamp are skipped, so nothing finished is redone |
| a -data season `EXIT=1` on `gh release upload` | GitHub 500 on an asset | rerun that season's `cron_daily_cfb.sh -s Y -e Y` |

## Phase 6 — close out

- The raw log ends `chain done` / `EXIT=0`; the -raw checkout is not ahead of origin.
- Each -data season log ends `EXIT=0`; a release asset's `updated_at` moved.
- The DB does not re-ingest back seasons nightly (only current + prior): note it in the
  ledger, or re-run the ingest for the rebuilt seasons.
- Ledger entry with the stamp, the PRs carried, and any season reruns.
