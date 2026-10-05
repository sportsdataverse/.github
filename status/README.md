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
  producer repos, package repos, unmapped release tags, warnings.
- `summary.json` — compact and page-ready (read by sportsdataverse.org/status):
  - `release_tags[]` — one entry per `sportsdataverse-data` tag, **stalest first**,
    tags with no assets last: `tag`, `producer` (repo full name, or `null` when
    unmapped), `assets`, `newest_asset_at`, `max_season` (raw, per tag).
  - `producers[]` — `repo`, `label`, `sport`, `packages[]`, `raw_repo`, `schedule`,
    `season`, `stale_after_days`, `in_season`, `updated_at` (newest play-level
    asset), `any_updated_at` (newest asset across all its tags), `age_days`,
    `through_season`, `through_tags`, `data_state`, `state`
    (`fresh|idle|stale|failing|unknown`), `tags` (a count), `tag_names[]`,
    `badge_dir`, `carried_forward`, `workflows[]`.
  - `packages[]` — `repo`, `latest_release_tag`, `published_at`, `badge_dir`,
    `workflows[]`.
  - Every workflow entry: `name`, `file`, `conclusion`, `created_at` (run start,
    shown on badges), `completed_at` (what `failing` compares), `event`, `url`,
    `state` (`active`, `disabled_manually`, …) and `badge` (its file under `badges/`).
  - `red_workflows[]` (same fields plus `repo`; disabled workflows excluded),
    `unmapped_tags[]`, `warnings[]` (config and collection problems as strings),
    `generated_at`, `totals`.
- `producers.json` — **hand-curated config, not generated** (see below).
- `badges/<repo-name>/<key>.json` — shields.io endpoint badges (see below). The
  whole `badges/` tree is rebuilt every run, so a deleted workflow loses its badge.

## Badges

Every file follows the shields endpoint schema: `schemaVersion: 1`, `label`,
`message`, `color`, `namedLogo: "github"`.

| key | label | message |
|---|---|---|
| `updated.json` | `data updated` | `YYYY-MM-DD` — newest release asset among the producer's play-level tags (`through_tags`), else all its counted tags |
| `through.json` | `through` | `YYYY season` — newest season year in the asset names of those same tags (a span `2025-26` reads as 2026) |
| `status.json` | `pipeline` | `fresh`, `idle (off-season)`, `stale Nd`, `failing`, `unknown` |
| `wf-<workflow-file-stem>.json` | the workflow's name | `passing · YYYY-MM-DD`, `failing · …`, `cancelled · …`, `disabled · …`, `no runs` |
| `ecosystem/cran-downloads.json` | `CRAN downloads` | all-time CRAN downloads (RStudio mirror, via cranlogs) summed over `package_repos` with valid R package names, e.g. `252k`; `namedLogo: "r"`; a failed cranlogs read carries the previous number forward |

`updated`, `through` and `status` exist for every producer in `producers.json`;
`wf-*` exists for every non-dynamic workflow of every public repo in the snapshot
(e.g. `badges/hoopR/wf-R-CMD-check.json`), including workflows with no completed
default-branch run (`no runs`). A disabled workflow reads `disabled`, never
`passing`. Runs of fork or pull-request events are ignored. Colors: passing/fresh
`brightgreen`, idle `blue`, stale `orange`, failing `red`, cancelled `yellow`,
unknown / no runs / disabled `lightgrey`.

The directory is the bare repo name; if two repos share it, the one outside the
org uses `<owner>__<name>`. If two workflows of one repo share a file stem, the
second badge uses the full file name (`wf-pkgdown.yml.json`). `summary.json`
gives each workflow's exact `badge` path, so pages need not guess.

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
  `season` (`start`/`end` as inclusive `MM-DD`, starting at the first games; may
  wrap the year), `stale_after_days` (sized to the league's normal in-season gaps:
  all-star breaks, bye weeks), `update_workflows` (workflow file names; a disabled
  one is kept only while it is still the documented update path), and optional
  `through_tags` — the play-level tags that decide `through_season`, `updated_at`,
  staleness and the `failing` comparison, so a pre-season schedule file cannot
  claim the next season and an unrelated daily output cannot hide stalled
  play-by-play.
- `package_repos` — package repositories listed in `summary.json` `packages[]`.
  Their workflows, and those of every producer and `raw_repo`, are backfilled: an
  active workflow with no completed default-branch run among the latest 100 gets
  its own latest run, so its `wf-*` badge never says `no runs` wrongly.

State: `failing` if an active update workflow's latest run failed (failure, timed
out or startup failure; never cancelled or disabled) **and** that run COMPLETED
after the producer's newest play-level asset — if data landed after the failure the
pipeline is delivering, though the workflow's own `wf-*` badge and `red_workflows`
still show it; else `stale` if in season and the newest play-level asset is older
than `stale_after_days` (the clock starts at the later of that asset and the season
start, so opening day is not an alarm); else `idle` if out of season (never red);
else `fresh`; `unknown` without data. Every mapping was verified against the
producer's own code; add a rule only with that evidence.

API failures never become output: only a genuine 404/410 (or a 403 that is not a
rate limit) reads as "absent"; a rate limit, a 5xx or a failed later page raises.
A repo that fails is carried forward from the previous committed snapshot
(`carried_forward: true` plus the reason, and a warning) so its badges survive; the
run exits non-zero and writes nothing when `sportsdataverse-data` fails or more than
10% of repos fail. A stale run listing cannot move a workflow's latest run backwards:
the previous run is kept if it still exists.

## Regenerating

The cloud sandbox of the chief-of-staff routines cannot reach api.github.com, which
is why they read these files. To regenerate locally (uses your `gh` login; the
private-repo filter keeps the output public):

```sh
python .github/scripts/ecosystem_status.py        # prints its gh api call count
npm_config_ignore_scripts=true npx --yes doctoc@2.5.0 status/ecosystem.md status/README.md --github
python -m unittest discover -s .github/scripts/tests
```
