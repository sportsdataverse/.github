---
name: sdv-reprocess
description: Use when a -raw corpus has to be rebuilt because sportsdataverse-py changed what it produces — after an sdv-py fix to play types, EPA/WPA or end states lands, on a SCHEMA_REV bump, or for "rev-N reprocess", "rebuild the finals", "bump the lock and reprocess", "re-run the corpus after the sdv-py fix". Phases — (1) gather every sdv-py PR the run must carry BEFORE bumping, because the processing stamp embeds the sdv-py commit and a later bump re-stales the whole corpus, (2) lock + SCHEMA_REV bump PRs in the -raw and -data repos under the shared locks, venv sync, stamp check, (3) clear the runway — the daily scrape/build chain, the :40 git_pull sweep, other sessions' rebuild jobs on the same locks, (4) launch `scripts/reprocess_chain.sh --data` detached and hand over watch commands, (5) the failure modes and their fixes (a season timing out on /tmp/git_pull_sdv.lock, a daemonized `git gc` or `credential-cache--daemon` holding it, git 2.25 ignoring GIT_CONFIG_COUNT, stopping by PID, a new sdv-py fix mid-run), (6) close-out. Also the three rules every -raw/-data repo keeps, in any sport — commit + push per season, a lock holder runs git with the lock fd closed (`9>&-` / `flock -o`), and a manual -data build never overlaps the daily build (in cfbfastR-cfb-data it holds that repo's build lock). cfbfastR-cfb-raw / cfbfastR-cfb-data is the worked example.
---

# Reprocess a -raw corpus after an sdv-py change

A -raw repo's finals are stamped `<sdv-py version>+<sdv-py commit>.<SCHEMA_REV>`
(cfbfastR-cfb-raw: `PROCESSING_VERSION`, `python/cfb_raw_scrape/_cfb_raw_utils.py`). Moving
the lock re-stales every final; the reprocess rebuilds them season by season, then the -data
repo recompiles and republishes every dataset from them. A full CFB run is ~23 seasons at
~25-30 min each for the raw side, then hours per season for -data. Every step below cost a
restart on 2026-10-01 (rev 13); the incidents are in the ClaudeCowork ledger
`ledgers/2026-09-30-cfbd-return-docs/LEDGER.md`.

## Three rules for every -raw / -data repo

Not CFB rules: every sport's drivers keep them, and a new driver, backfill or chain must too.
Rule 3 is for -data repos; its lock file exists only in cfbfastR-cfb-data.

- **Commit and push per season.** A mass change (backfill, reprocess, re-parse, rename)
  commits AND pushes one season at a time, subject `<Sport> … (Start: Y End: Y)` (the
  dispatch parses that year; the format is load-bearing). Never `git add` a multi-season
  tree into one commit. The daily drivers already loop `for i in $(seq START END)` and call
  `sdv_commit_push` per season; copy that shape.
- **A lock holder never lends its fd to git.** `exec 9>L; flock 9`, `( flock 9; cmd ) 9>L` and
  `flock L cmd` all pass the lock fd to every child, and git daemonizes two children that
  outlive the job: `gc --auto` (after commit, fetch, merge) and `credential-cache--daemon`
  (~15 min after an https fetch/push; the droplet runs `credential.helper=cache`). Either keeps
  the lock held after the job exits, so `flock -n` sweeps skip and `flock -w` waiters time out.
  Run git-touching children with the fd closed, `cmd 9>&-` (or `flock -o L cmd`), while the
  shell keeps the lock. `gc.auto=0` alone misses the credential daemon. Applied 2026-10-01 to
  `bin/git_pull_cron.sh`, cfb-data `cron_daily_cfb.sh`, cfb-raw `reprocess_chain.sh` and the
  `run_autocommit.sh` loops (ncaa-{mbb,wbb}-hoops-raw, pff-{cfb,nfl}-raw).
- **A manual -data build never overlaps the daily build.** Two builds from different sdv-py
  commits race: the later push conflicts on binary parquet (git cannot merge it), `main` is
  left diverged, and every later cron fails its `pull --ff-only`. Incident 2026-11-26: a
  2004-2026 republish ran outside the lock during the daily cfb-data build, which had pulled
  5 min before a lock bump merged and built 2026 on the old sdv-py.
  - cfbfastR-cfb-data (the only -data repo with a build lock today): `cron_daily_cfb.sh`
    holds `/tmp/cfbfastR-cfb-data-build.lock` for its whole pull → build → push, and any
    other build that writes the repo's outputs (a republish, a model refit, a season rerun,
    a lock bump's `uv sync` of `.venv`) holds it too. Its entry points take it themselves:
    `cron_daily_cfb.sh -s Y -e Y` (a season), `cron_alt_fill.sh` (the players crosswalk
    only), cfb-raw's `reprocess_chain.sh --data`. Never wrap one in `flock`: the inner
    `flock -w` waits on the outer one for 3 h, then fails. They refuse any branch but `main`,
    so a build in a worktree or clone wraps its own command, with `-o` so no git child
    inherits the fd (rule 2): `flock -o -w 10800 /tmp/cfbfastR-cfb-data-build.lock bash …`.
  - One season per lock hold. A `-s 2004 -e 2026` run holds the lock for the whole range,
    and each daily cron behind it gives up after 3 h without building the current season.
    Loop per season, as `reprocess_chain.sh --data` does.
  - A lock in `/tmp` does not reach GitHub Actions: don't dispatch `daily_cfb.yml` or a
    model workflow that pushes to the repo while a droplet build runs.
  - A -data repo with no build lock: `ps` for its daily build, wait for it to exit, and check
    `crontab -l` for the next fire; if the build would overlap it, ask before holding that
    entry.

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
  `flock -o -w 600 /tmp/git_pull_sdv.lock bash -c '...'` (-data also holds
  `/tmp/cfbfastR-cfb-data-build.lock`). When the main checkout is busy (a chain runs in it),
  a script fix still gets a branch without the 4 GB checkout:
  `git worktree add --no-checkout -b <br> <scratch>/wt origin/main && git -C <scratch>/wt reset -q && git -C <scratch>/wt checkout -- <file>`,
  then edit, commit that path, push, PR, `git worktree remove --force <scratch>/wt`.
  Then `uv sync` both (the -data one under the build lock: a sync mid-build gives later
  datasets the new sdv-py and earlier ones the old), and check the stamp:
  `.venv/bin/python -c 'import sys; sys.path.insert(0, "python"); from cfb_raw_scrape._cfb_raw_utils import PROCESSING_VERSION; print(PROCESSING_VERSION)'`

## Phase 3 — clear the runway

- `fuser -v /tmp/git_pull_sdv.lock /tmp/cfbfastR-cfb-data-build.lock` and `ps` for the daily
  chain (`daily_cfb_scraper.sh` → `cron_daily_cfb.sh` → `daily_cfb_processor.sh`, launched 04:05
  ET; a 2026 daily build runs ~4.5 h) and for other sessions' jobs (`/mnt/sdv_repos/tmp/*/run.sh`).
- The daily chain: if the user cancels it ("no games last night"), kill its process tree BY
  PID, then restore the partial outputs it left (`git checkout -- <the season's parquets>`),
  or `cron_daily_cfb.sh` refuses the dirty tree later.
- Another session's job: leave it alone. A job launched through the repo's scripts takes the
  same locks and the chain waits for it. An ad-hoc one may not (rule 3), and `fuser` cannot
  see a job that skipped the lock: look for builders by process and cwd too,
  `ps -eo pid,lstart,args | grep -E 'daily_cfb_processor|cfb-data' | grep -v grep` and
  `ls -l /proc/[0-9]*/cwd 2>/dev/null | grep cfb-data`.
  Tell the user if the two overlap (a -data rebuild of every dataset supersedes a narrower
  republish) and let them decide.

## Phase 4 — launch

```bash
cd /mnt/sdv_repos/cfbfastR-cfb-raw
setsid nohup bash scripts/reprocess_chain.sh --data >/dev/null 2>&1 </dev/null &
```

Another sport has no `reprocess_chain.sh` yet: copy cfb-raw's and point it at that repo's
per-season driver, keeping the per-season lock, the `9>&-` and the per-season commits.

It prints its log path and a watch command and ends with `chain done` / `EXIT=`. Check the
first season's log for `target processing_version : <new stamp>` and `to rebuild : <all>`.
Give the user the watch commands. A background watcher caps at 2 h: re-arm it at most once —
the chain drives itself, and `--data` starts the -data side when the raw side is clean.

## Phase 5 — when it goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| `season Y exit 1`, "no lock after Ns, held by:" | the :40 git_pull sweep, the daily chain, another job | the chain waits 3 h by default; rerun the listed seasons: `SEASONS="2011 2010" bash scripts/reprocess_chain.sh --data` |
| the lock held by `git gc --auto` / `git repack` / `git credential-cache--daemon` | a git daemon inherited the lock's fd (a repack held it 45 min; the credential daemon lives ~15 min after an https push) | the holder must run git children with `9>&-` (see rule 2 above); for a stray one now: killing a gc is safe while no `.tmp-*` pack exists, and `git credential-cache exit` ends the credential daemon |
| `GIT_CONFIG_COUNT=…` had no effect | git 2.25 on the droplet; that variable is 2.31+ | `export GIT_CONFIG_PARAMETERS="'gc.auto=0'"`; check with `git config --get gc.auto` |
| need to stop the chain | — | kill BY PID: `ps -eo pid,args \| awk '$3=="scripts/reprocess_chain.sh"'`. Never `pkill -f` a pattern your own shell's command line contains (exit 144, self-kill); never edit a running bash script — stop and relaunch |
| a new sdv-py fix lands mid-run | — | stop between seasons, bump again (Phase 2), relaunch; finals already at the new stamp are skipped, so nothing finished is redone |
| the daily -data log says `cannot rebase onto origin/main`; `main` is ahead N, behind M | two builds raced (rule 3); the loser built on an older base or sdv-py | (1) `git log --format='%h %s' origin/main..main`: every commit must be a `… Data Updated` / `log update (Start: Y End: Y)` from the loser's run; anything else, stop and ask. (2) Superseded: the loser's pin is `git show $(git merge-base main origin/main):uv.lock \| grep -m1 'sportsdataverse-py?branch'` (not its venv, which the next sync rewrites); in a fetched sdv-py, `git merge-base --is-ancestor <loser> <winner>` must exit 0 with the two commits different (exit 128 = unknown commit, fetch first). Loser newer: don't reset, ask. (3) `git bundle create /mnt/sdv_repos/tmp/<repo>_<date>.bundle origin/main..main && git bundle verify …` (not the session scratchpad). (4) Ask, then hold both locks: `flock -o -n /tmp/cfbfastR-cfb-data-build.lock flock -o -w 3600 /tmp/git_pull_sdv.lock git -C <repo> reset --hard origin/main`. (5) The reset does not touch releases: `grep -aE 'INFO +uploaded ' <loser log>` lists what it published; rerun `cron_daily_cfb.sh -s Y -e Y` for that season, whose sha-diff publish re-uploads what differs |
| a -data season `EXIT=1` on `gh release upload` | GitHub 500 on an asset | rerun that season's `cron_daily_cfb.sh -s Y -e Y` |

## Phase 6 — close out

- The raw log ends `chain done` / `EXIT=0`; the -raw checkout is not ahead of origin.
- Each -data season log ends `EXIT=0`; a release asset's `updated_at` moved.
- The DB does not re-ingest back seasons nightly (only current + prior): note it in the
  ledger, or re-run the ingest for the rebuilt seasons.
- Ledger entry with the stamp, the PRs carried, and any season reruns.
