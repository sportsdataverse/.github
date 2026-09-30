# status/

Nightly machine + human snapshot of the whole ecosystem, written by
`.github/workflows/ecosystem-status.yml` (script: `.github/scripts/ecosystem_status.py`).
Public repositories only: the generator drops private repos explicitly.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Files](#files)
- [Badges](#badges)
- [producers.json](#producersjson)
- [Regenerating](#regenerating)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Files

- `ecosystem.json` — per repo: open PRs (age/idle), open + stale-unassigned issues,
  latest completed default-branch run per workflow (with its `file`), releases with
  asset counts, newest-asset timestamp and `max_season`, last push. `totals` at the top.
- `ecosystem.md` — the same as tables, with a doctoc table of contents. Sections, in
  order: sportsdataverse-data release tags (freshness, producer, through season),
  producers, red workflows, open PRs, open issues, release-asset freshness for
  producer repos, package repos, unmapped release tags.
- `summary.json` — compact and page-ready (read by sportsdataverse.org/status):
  - `release_tags[]` — one entry per `sportsdataverse-data` tag, **stalest first**,
    tags with no assets last: `tag`, `producer` (repo full name, or `null` when
    unmapped), `assets`, `newest_asset_at`, `max_season` (raw, per tag).
  - `producers[]` — `repo`, `label`, `sport`, `packages[]`, `raw_repo`, `schedule`,
    `season`, `stale_after_days`, `in_season`, `updated_at`, `age_days`,
    `through_season`, `data_state`, `state` (`fresh|idle|stale|failing|unknown`),
    `tags` (a count), `tag_names[]`, `workflows[]` (`name`, `file`, `conclusion`,
    `created_at`, `event`, `url`).
  - `packages[]` — `repo`, `latest_release_tag`, `published_at`, `workflows[]`.
  - `red_workflows[]`, `unmapped_tags[]`, `generated_at`, `totals`.
- `producers.json` — **hand-curated config, not generated** (see below).
- `badges/<repo-name>/<key>.json` — shields.io endpoint badges (see below). The
  whole `badges/` tree is rebuilt every run, so a deleted workflow loses its badge.

## Badges

Every file follows the shields endpoint schema: `schemaVersion: 1`, `label`,
`message`, `color`, `namedLogo: "github"`.

| key | label | message |
|---|---|---|
| `updated.json` | `data updated` | `YYYY-MM-DD` — newest release asset among the producer's tags |
| `through.json` | `through` | `YYYY season` — newest standalone year in the asset names of the producer's `through_tags` (its play-by-play tags), else of all its tags |
| `status.json` | `pipeline` | `fresh`, `idle (off-season)`, `stale Nd`, `failing`, `unknown` |
| `wf-<workflow-file-stem>.json` | the workflow's name | `passing · YYYY-MM-DD`, `failing · …`, `cancelled · …`, `no runs` |

`updated`, `through` and `status` exist for every producer in `producers.json`;
`wf-*` exists for every non-dynamic workflow of every public repo in the snapshot
(e.g. `badges/hoopR/wf-R-CMD-check.json`), including workflows with no completed
default-branch run (`no runs`). Colors: passing/fresh `brightgreen`, idle `blue`,
stale `orange`, failing `red`, cancelled `yellow`, unknown/no runs `lightgrey`.

Embed a badge with the URL-encoded raw file:

```text
https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2F<repo-name>%2F<key>.json
```

For example, markdown for the WBB pipeline badge:

```markdown
[![pipeline](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fstatus.json)](https://sportsdataverse.org/status)
```

Append `&label=<text>` to override the label (shields query parameter).

## producers.json

- `rules` — ordered tag-prefix rules; the **first** match wins, and the generator
  refuses a rule that an earlier, shorter prefix would shadow (so `nba_stats_` must
  precede `nba_`). `repo: null` marks a tag family deliberately left unattributed;
  those tags, and tags no rule matches, are reported in `unmapped_tags` — never
  guessed. `freshness: false` keeps a tag out of its producer's `updated`,
  `through` and staleness (the cross-league ESPN injury and depth-chart snapshots
  published daily by cfbfastR-cfb-data would otherwise mask a stalled pipeline).
- `producers` — `repo`, `label`, `sport`, `packages` (loader packages that read its
  tags, bare repo names from `package_repos`), `raw_repo`, `schedule` (free text),
  `season` (`start`/`end` as inclusive `MM-DD`; may wrap the year),
  `stale_after_days`, `update_workflows` (workflow file names), and optional
  `through_tags` (play-level tags that decide `through_season`, so a pre-season
  schedule file cannot claim the next season).
- `package_repos` — package repositories listed in `summary.json` `packages[]`.
  Their workflows, and those of every producer and `raw_repo`, are backfilled: an
  active workflow with no completed default-branch run among the latest 100 gets
  its own latest run, so its `wf-*` badge never says `no runs` wrongly.

State: `failing` if an update workflow's latest run failed (failure, timed out or
startup failure; never cancelled) **and** that run is newer than the producer's
newest counted asset — if data landed after the failure the pipeline is delivering,
though the workflow's own `wf-*` badge and `red_workflows` still show it; else
`stale` if in season and the newest counted asset is older than `stale_after_days`;
else `idle` if out of season (never red); else `fresh`; `unknown` without data.
Every mapping was verified against the producer's own code; add a rule only with
that evidence.

## Regenerating

The cloud sandbox of the chief-of-staff routines cannot reach api.github.com, which
is why they read these files. To regenerate locally (uses your `gh` login; the
private-repo filter keeps the output public):

```sh
python .github/scripts/ecosystem_status.py        # prints its gh api call count
npx --yes doctoc@2 status/ecosystem.md status/README.md --github
python -m unittest discover -s .github/scripts/tests
```
