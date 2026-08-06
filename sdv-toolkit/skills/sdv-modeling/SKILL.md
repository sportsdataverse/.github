---
name: sdv-modeling
description: Use when building, extending, or debugging any model in the SportsDataverse ecosystem — before writing model code, not after it breaks. This is the domain reference that sdv-model-spine (the build loop) pulls from: which method fits the problem, what data feeds it, what has already been built or tried and rejected, which metric gates it, and which silent failures to assert against. Reference files - methods (rating systems, the APM/RAPM family, EP/WP, xG, possession engines, projection and simulation), data-sources (which release dataset and loader feeds which feature family, season-coverage floors, the oracle catalog), prior-art (what exists, what was surveyed and rejected, and why), metrics-and-gates (metric selection by model type and the never-lower gate rule), failure-modes (the catalog of components that report success while doing nothing, each with its detection assertion), upstream-skills (routing to the general ML/DS skills rather than restating them), and per-sport inventories for cfb, nfl, nba-wnba, mbb-wbb, hockey, mlb, and soccer. Invoke for "which model should I use", "what data feeds this", "has this been tried", "what metric gates this", "why is my model silently wrong", "start a new model", or before any sdv-model-spine phase.
---

# Modeling domain reference (SDV)

`sdv-modeling` is a reference, not a workflow. `sdv-model-spine` is the build
*loop* — it answers how to run a model build. This skill answers the
questions the loop can't: which method fits, what data feeds it, what's
already been tried, what metric gates it, and what silently fails. Each
question below routes to one reference file; none of the answers live here.

## Reference files

| File | Question it answers |
|---|---|
| `references/methods.md` | Which modeling method fits this problem — rating systems, APM/RAPM family, EP/WP, xG, possession engines, projection and simulation? |
| `references/prior-art.md` | What already exists, what was surveyed and rejected, and why? |
| `references/data-sources.md` | Which release dataset and loader feeds which feature family, and what's the season-coverage floor? |
| `references/metrics-and-gates.md` | How do I know this model works — which metric, and the never-lower gate rule? |
| `references/failure-modes.md` | Why is my model silently wrong — the catalog of components that report success while doing nothing, with a detection assertion for each? |
| `references/upstream-skills.md` | Is there a general ML/DS skill for this already, instead of reinventing it here? |
| `references/sports/<sport>.md` | What's specific to this sport — `cfb`, `nfl`, `nba-wnba`, `mbb-wbb`, `hockey`, `mlb`, `soccer`? |

## Decision tree

- **What should I build?** → `prior-art.md`, then `methods.md`.
- **What feeds it?** → `data-sources.md` + the relevant `sports/<sport>.md`.
- **How do I know it works?** → `metrics-and-gates.md`.
- **Why is it wrong?** → `failure-modes.md`.
- **Is there a library for this?** → `upstream-skills.md`.

## Before you start the build loop

Read the relevant reference files here first — then invoke `sdv-model-spine`
to actually run the build. The spine assumes you already know which method,
which data, and which gate; this skill is where that decision gets made.
