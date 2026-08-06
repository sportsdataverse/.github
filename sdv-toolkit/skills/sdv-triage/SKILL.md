---
name: sdv-triage
description: Use to work the inbound queue across the SportsDataverse GitHub org — open issues and pull requests across the ~40 repos, which no other skill looks at. Sweeps (bounded per run, ordered by staleness and label), classifies each item via the sdv-issue-triage agent, does the safe work autonomously, and proposes everything else for authorization. Verdicts are actionable-now, already-fixed, needs-info, real-but-large, out-of-scope, and bot-noise. Action tiers — tier 0 (read, classify, write the triage report) and tier 1 (draft a fix on a local branch and run its tests) run autonomously because nothing leaves the machine; tiers 2 through 4 (push a branch, open a PR, comment on or label or close someone else's issue, merge an outside contributor's PR) ALWAYS require explicit per-item authorization, including when a sweep produces many obviously-correct actions. Invoke for "what's open across the org", "triage the issues", "any PRs waiting on me", "check the backlog", "weekly issue sweep", or "review the open PRs".
---

# Triage the inbound queue

Every other skill in this toolkit acts on repos we drive. This one reads
what the org is asking of us: open issues and pull requests across the
~40 SportsDataverse repos, filed by people who are not us. Its defining
constraint is a gate, not a capability — a comment, close, or PR goes out
under the org's name and cannot be quietly undone.

## Action tiers — read before doing anything

| Tier | Action | Authorization |
|---|---|---|
| 0 | Read, classify, write the triage report | Autonomous — nothing leaves the machine |
| 1 | Draft a fix on a local branch, run its tests | Autonomous — local only, nothing published |
| 2 | Push a branch, open a PR | **Explicit confirmation, per item** |
| 3 | Comment on, label, or close someone else's issue or PR | **Explicit confirmation, per item** |
| 4 | Merge an outside contributor's PR | **Explicit confirmation + a reviewer pass** |

Tiers 2-4 are never autonomous. A sweep that produces twenty obviously-correct
tier-3 actions still takes one authorization before any of them fire —
"obviously correct in bulk" is precisely when unauthorized outward action does
the most damage, because it is irreversible across twenty other people's
threads at once.

Batch the proposals. Present the menu. Act only on what was authorized.

## Phase 0 — Auth check

```sh
gh auth status
gh api rate_limit --jq '.rate.remaining'
```

`GITHUB_PAT` lives in `~/.Renviron` and is read only by R at startup — bash
and Python do NOT see it; `gh` carries its own separate auth store, so this
check is independent of that gotcha. If `gh auth status` fails, STOP and
report — every later step depends on it. If the rate limit is low, narrow
the sweep (fewer repos, or issues-only / PRs-only) rather than burning the
budget mid-sweep.

## Phase 1 — Bounded sweep

Don't sweep unbounded — 40 repos of full history is not a triage run, it's
a scrape. Default scope, override on request:

```sh
gh search issues --owner sportsdataverse --state open --sort updated --order asc --limit 50
gh search prs --owner sportsdataverse --state open --sort updated --order asc --limit 50
```

- **Order by staleness first** (oldest-updated first) — a sweep that only
  ever reaches the newest items lets old ones rot silently.
- **Then by label** where the repo has triage labels (`bug`, `good first
  issue`, `help wanted`) — surface those ahead of unlabeled noise.
- **Bound the run** to a page size the report stays reviewable at (50 is the
  default above); a larger org-wide ask should be phased, not swept in one
  shot.
- Note repos with zero hits as swept-clean, not skipped — a report that's
  silent about a repo is indistinguishable from one that never checked it.

## Phase 2 — Per-item dispatch

For every item in scope, dispatch to the `sdv-issue-triage` agent (one call
per item, or batched per repo if the agent supports it) and collect its
verdict: **actionable-now**, **already-fixed**, **needs-info**,
**real-but-large**, **out-of-scope**, or **bot-noise**.

Before dispatching, apply the source-specific shortcuts — they change what
gets investigated at all, not just what gets proposed:

- **Outside-contributor PRs** — before any merge is even considered, route
  the diff through `sdv-python-reviewer` or `sdv-r-reviewer` by file
  archetype (`.py` → python reviewer with the matching lens, `.R`/`man/` →
  r reviewer). The review is required input to a tier-4 proposal, not
  optional polish.
- **Dependabot PRs** (`author:app/dependabot`) — pull out of individual
  triage and batch into a single lane: one proposal line covering "N
  dependency bumps, repos X/Y/Z" rather than N separate items. They share
  one authorization, not N.
- **Parked findings** — before treating an issue as new, grep it against
  every `.superpowers/sdd/*/progress.md` ledger in this org checkout
  (`grep -rl "<keyword>" .superpowers/sdd/*/progress.md`). A match means the
  finding is already tracked — link the issue to that ledger entry instead
  of re-investigating from scratch.

## Phase 3 — Tier 0/1 execution (autonomous)

For items the agent verdicts **actionable-now** with a small, well-scoped
fix:

1. Write the triage report (tier 0) — every swept item, its verdict, and
   the proposed next action. This always happens, for every item, regardless
   of what happens next.
2. For fixable items, draft the fix on a local branch and run its tests
   (tier 1) — no push, no PR. This is prep work so the tier-2 proposal
   already has a diff to point at, not a promise to write one later.

Nothing in this phase touches the network write path. `git push`, `gh pr
create`, `gh issue comment`, `gh pr comment`, `gh issue close`, `gh pr close`,
`gh pr merge` — none of these run in this phase, for any item, no matter how
confident the classification.

## Phase 4 — Proposal menu

Present everything at tier 2+ as one batched menu, grouped by tier, each
line identifying the repo, item, verdict, and proposed action:

```
Tier 2 (push + open PR):
  [1] cfbfastR-py#42 — actionable-now, fix drafted on local branch, tests green
  [2] hoopR-py#17 — actionable-now, fix drafted on local branch, tests green

Tier 3 (comment/label/close):
  [3] wehoop#88 — already-fixed in 0.0.73, propose close-with-comment
  [4] nflverse-py#5 — needs-info, propose clarifying comment

Tier 3 (batched — dependabot):
  [5] 6 dependency-bump PRs across nfl-data, cfb-data, hoopR-nba-data — propose one merge lane

Tier 4 (merge outside PR):
  [6] cfbfastR-py#39 — outside contributor, sdv-python-reviewer clean, propose merge
```

Wait for explicit per-item (or explicitly-batched, per Dependabot) sign-off.
Act only on what was authorized — an unauthorized item stays proposed, not
done, into the next run.

## Report

Whether or not any tier-2+ action was authorized, the triage report itself
(Phase 3, step 1) is always produced — repos swept, items found, verdicts,
and outcomes (autonomous tier-0/1 work done vs. proposals pending
authorization vs. proposals authorized-and-executed this run).
