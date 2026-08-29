---
name: sdv-modeling
description: The single modeling reference for the SportsDataverse ecosystem — read before writing model code, not after it breaks. Answers which method fits the problem, what data feeds it, what has already been tried and rejected, which metric gates it, how to write the fit without a silent panel-data failure, and how to engineer the features. Reference files - methods (rating systems, the APM/RAPM family, EP/WP, CP/CPOE, xG, possession engines, projection and simulation), data-sources (which release dataset and loader feeds which feature family, season-coverage floors, the oracle catalog), prior-art (what exists, what was surveyed and rejected, and why), metrics-and-gates (metric selection by model type, Brier decomposition, expected calibration error, multiclass EP-shape evaluation, conformal intervals, the never-lower gate rule, the as-of-date leakage boundary, oracle-join integrity), sklearn-xgboost (ten panel-sports failure families each with a runnable detection test - splitting and leakage, purged and embargoed CV, Ridge/RAPM and sparse solver choice, Pipeline/ColumnTransformer, calibration, unseen entities, silent failure, determinism, persistence, performance, XGBoost interop), feature-engineering (cyclical encoding, as-of target encoding on entities, leakage-safe preprocessing, feature selection, id dtype discipline), failure-modes (the catalog of components that report success while doing nothing, each with its detection assertion), and per-sport inventories for cfb, nfl, nba-wnba, mbb-wbb, hockey, mlb, and soccer. Absorbed sdv-sklearn, sdv-evaluating-ml-models, sdv-engineering-ml-features, sdv-ml-pipeline, sdv-data-scientist and sdv-analyzing-data on 2026-08-28. Pairs with sdv-model-build (the build loop that runs a model to completion) and sdv-data-pipeline (registering, retraining and publishing it). Invoke for "which model should I use", "what data feeds this", "has this been tried", "what metric gates this", "why is my model silently wrong", "start a new model", "fit a model", "set up cross-validation", "cross-validation strategy", "purged CV", "leakage in my features", "RAPM", "ridge regression", "adjusted plus-minus", "calibrate probabilities", "calibration curve", "expected calibration error", "Brier score", "is my model calibrated", "prediction intervals", "conformal prediction", "feature engineering", "encode a categorical", "target encoding", "feature selection", "hyperparameter tuning", "evaluate this model", "error analysis", "save/load a model", "why is my model wrong but not erroring", or before any sdv-model-build phase.
---

# Modeling — the domain reference for SDV models

`sdv-modeling` is a **reference**, not a workflow. It answers *what to build,
what feeds it, how to write it, and how to know it works*. Running the build to
completion is `sdv-model-build`; operating and publishing the result is
`sdv-data-pipeline`. Each question below routes to one reference file; the
answers live there, not here.

## Where this sits — three skills, three different questions

| Skill | Question | Reach for it when |
|---|---|---|
| **`sdv-modeling`** (here) | *What* should this be, and how do I write it correctly? | Before and during model code |
| **`sdv-model-build`** | *How do I run this build to completion?* Oracle capture, worktree, TDD phases, gates, close-out | Executing a model plan end to end |
| **`sdv-data-pipeline`** | *How does it live in production?* Registry row, fingerprints, one-job-per-model, ledger, release | The model exists and must run on a schedule |

They compose in that order. A build that skips this skill picks a method that
was already surveyed and rejected; one that skips `sdv-data-pipeline` ships an
artifact nobody can retrain.

## Reference files

| File | Question it answers |
|---|---|
| `references/methods.md` | Which modeling method fits — rating systems, APM/RAPM, EP/WP, CP/CPOE, xG, possession engines, projection, simulation? |
| `references/prior-art.md` | What already exists, what was surveyed and rejected, and why? |
| `references/data-sources.md` | Which release dataset and loader feeds which feature family, and what is the season-coverage floor? |
| `references/feature-engineering.md` | How do I build the columns — cyclical encoding, as-of target encoding, leakage-safe preprocessing, selection, id dtypes? |
| `references/sklearn-xgboost.md` | How do I write the fit without a silent panel-data failure — splitting, purged CV, ridge/RAPM, calibration, persistence, XGBoost interop? |
| `references/metrics-and-gates.md` | How do I know it works — metric by model type, calibration, intervals, and the never-lower gate rule? |
| `references/failure-modes.md` | Why is my model silently wrong — components that report success while doing nothing, with a detection assertion for each? |
| `references/upstream-skills.md` | Is there an existing skill for this instead of reinventing it here? |
| `references/generic/` | Generic technique with no SDV adaptation — model validation, CV, metrics, tuning, encoders, selection, EDA. **Read the SDV tier above first**; `generic/README.md` lists the five places this tier is actively wrong for panel-sports data. |
| `references/sports/<sport>.md` | What is specific to this sport — `cfb`, `nfl`, `nba-wnba`, `mbb-wbb`, `hockey`, `mlb`, `soccer`? |

## Decision tree

- **What should I build?** → `prior-art.md`, then `methods.md`.
- **What feeds it?** → `data-sources.md` + the relevant `sports/<sport>.md`.
- **How do I build the features?** → `feature-engineering.md`.
- **How do I write the fit?** → `sklearn-xgboost.md`.
- **How do I know it works?** → `metrics-and-gates.md`.
- **Why is it wrong?** → `failure-modes.md`.
- **Is there a library or skill for this?** → `upstream-skills.md`.
- **Need the generic technique, not the SDV rule?** → `generic/`, after reading its README.

## The one rule that outranks everything else here

**A component that runs without error has not been shown to do anything.**
Every confirmed production incident in this ecosystem is of that shape: a ridge
penalty applied to nothing, a Boolean `fill_null` that was a no-op, a lambda
selected and then discarded, a quarters model reading 0 rows from a halves-era
season and reporting success. Assert on the **output changing**, never on the
code path running. `failure-modes.md` is the catalog; every entry carries the
assertion that would have caught it.

## Review, not self-review

Reaching for a reviewer is not optional at gate time:

- `sdv-model-reviewer` — design-time audit of new model or validation code.
  Lenses: `gate-integrity`, `leakage-boundary`, `metric-fit`, `silent-no-op`,
  `sklearn-contract`, `lineage`, `oracle-join`. The `sklearn-contract` lens is
  the read-only counterpart of `references/sklearn-xgboost.md`; **any
  contradiction between them is a defect in the reference file, not the lens.**
- `sdv-harness-triage` — for a validation-harness WARN on an *existing*
  dataset, with a `finding_type`. Not for new model code.
- `sdv-parity-reviewer` — when the model was ported from R.

Never `general-purpose` for these.

## Before you start the build loop

Read the relevant reference files here first, then invoke `sdv-model-build` to
run the build. That skill assumes you already know which method, which data,
and which gate — this skill is where those decisions get made.
