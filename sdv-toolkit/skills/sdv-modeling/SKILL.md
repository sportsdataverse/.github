---
name: sdv-modeling
description: The single modeling reference for the SportsDataverse ecosystem — read before writing model code, not after it breaks. Answers which method fits the problem, what data feeds it, what has already been tried and rejected, which metric gates it, how to write the fit without a silent panel-data failure, and how to engineer the features. Reference files - methods (rating systems, the APM/RAPM family, EP/WP, CP/CPOE, xG, possession engines, projection and simulation), data-sources (which release dataset and loader feeds which feature family, season-coverage floors, the oracle catalog), prior-art (what exists, what was surveyed and rejected, and why), metrics-and-gates (metric selection by model type, Brier decomposition, expected calibration error, multiclass EP-shape evaluation, conformal intervals, the never-lower gate rule, the as-of-date leakage boundary, oracle-join integrity), sklearn-xgboost (ten panel-sports failure families each with a runnable detection test - splitting and leakage, purged and embargoed CV, Ridge/RAPM and sparse solver choice, Pipeline/ColumnTransformer, calibration, unseen entities, silent failure, determinism, persistence, performance, XGBoost interop), feature-engineering (cyclical encoding, as-of target encoding on entities, leakage-safe preprocessing, feature selection, id dtype discipline), resampling (cluster bootstrap, jackknife, permutation tests), interpretability (TreeSHAP, permutation importance, partial dependence), model-families (the AutoML zoo benchmarked on panel data, CatBoost ordered statistics), tabular-deep-learning (what the benchmark literature found, TabPFN), bayesian (hierarchical pooling, priors, MCMC diagnostics), count-survival-ordinal (Poisson/NB/zero-inflated, censored survival, ordinal, CRPS), causal (DiD, IV, propensity, clustered SEs), compute (GPU, the XGBoost device API, sparse solves, torch, parallelism), tracking (fingerprints, feature-set registry, experiment ledger, lineage), literature (the published work behind each family, keyed to the 685-paper local corpus in Sports-Research-Papers), failure-modes (the catalog of components that report success while doing nothing, each with its detection assertion), and per-sport inventories for cfb, nfl, nba-wnba, mbb-wbb, hockey, mlb, and soccer. Absorbed sdv-sklearn, sdv-evaluating-ml-models, sdv-engineering-ml-features, sdv-ml-pipeline, sdv-data-scientist and sdv-analyzing-data on 2026-08-28. Pairs with sdv-model-build (the build loop that runs a model to completion) and sdv-data-pipeline (registering, retraining and publishing it). Invoke for "which model should I use", "what data feeds this", "has this been tried", "what metric gates this", "why is my model silently wrong", "start a new model", "fit a model", "set up cross-validation", "cross-validation strategy", "purged CV", "leakage in my features", "RAPM", "ridge regression", "adjusted plus-minus", "calibrate probabilities", "calibration curve", "expected calibration error", "Brier score", "is my model calibrated", "prediction intervals", "conformal prediction", "feature engineering", "encode a categorical", "target encoding", "feature selection", "hyperparameter tuning", "evaluate this model", "error analysis", "bootstrap", "confidence interval", "standard error", "explain this model", "SHAP", "feature importance", "partial dependence", "which model should I use", "LightGBM", "CatBoost", "AutoML", "AutoGluon", "neural net for tabular", "hierarchical model", "partial pooling", "MCMC", "prior", "Poisson", "count model", "survival analysis", "ordinal", "CRPS", "difference-in-differences", "causal", "propensity score", "do I need a GPU", "cuda", "speed this up", "distributed training", "torch", "entity embeddings", "experiment tracking", "model registry", "feature store", "feature set", "MLflow", "lineage", "fingerprint", "save/load a model", "why is my model wrong but not erroring", "what does the literature say", "is there a paper on this", "prior work", "how do others model this", or before any sdv-model-build phase.
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
| `references/resampling.md` | How do I put an honest interval on this — cluster bootstrap, jackknife, permutation, and why a row-level bootstrap is 8.8x too narrow? |
| `references/interpretability.md` | Why did the model do that — TreeSHAP with no extra dependency, permutation importance, partial dependence, and slicing them by season and era? |
| `references/model-families.md` | Which learner — the AutoML zoo (GBMs, RF/ET, GLM, MLP) benchmarked under GroupKFold, and CatBoost's ordered target statistics for entity ids? |
| `references/tabular-deep-learning.md` | Should this be a neural net — what the tabular benchmark literature actually found, and the one regime (small-n team-season) where it changes? |
| `references/bayesian.md` | How do I pool across entities with unequal samples — hierarchical models, priors, and the r-hat / ESS / divergence gates that must run first? |
| `references/count-survival-ordinal.md` | The target is a count, a duration, or an ordered class — Poisson/NB/zero-inflated, censored survival, ordinal, and CRPS. |
| `references/causal.md` | Did X *cause* Y — difference-in-differences, instrumental variables, propensity scores, and the clustered standard errors they all need. |
| `references/compute.md` | Do I need a GPU — where hardware actually helps, the XGBoost device API (and the silent CPU fallback), sparse solves, torch for entity embeddings, and the parallelism that pays first. |
| `references/tracking.md` | What components does a model, experiment, dataset and feature set need — fingerprints, the missing feature-set registry, the ledger, and derivable lineage, all git-native with no service. |
| `references/failure-modes.md` | Why is my model silently wrong — components that report success while doing nothing, with a detection assertion for each? |
| `references/literature.md` | What has been PUBLISHED on this family — keyed to the 685-paper corpus already on disk at `Sports-Research-Papers/md/`, plus verified external anchors. |
| `references/upstream-skills.md` | Is there an existing skill for this instead of reinventing it here? |
| `references/sports/<sport>.md` | What is specific to this sport — `cfb`, `nfl`, `nba-wnba`, `mbb-wbb`, `hockey`, `mlb`, `soccer`? |

## Decision tree

- **What should I build?** → `prior-art.md`, then `methods.md`.
- **What feeds it?** → `data-sources.md` + the relevant `sports/<sport>.md`.
- **How do I build the features?** → `feature-engineering.md`.
- **How do I write the fit?** → `sklearn-xgboost.md`.
- **How do I know it works?** → `metrics-and-gates.md`.
- **How do I write the fit?** → also `model-families.md` to choose the learner.
- **How do I explain it?** → `interpretability.md`.
- **What is the interval?** → `resampling.md`.
- **The target isn't binary or continuous?** → `count-survival-ordinal.md`.
- **Entities with unequal samples?** → `bayesian.md`.
- **Did X cause Y?** → `causal.md`.
- **Is this slow, or do I need a GPU?** → `compute.md`.
- **How do I track models, experiments, datasets and feature sets?** → `tracking.md`, then `sdv-data-pipeline` for the operational half.
- **Why is it wrong?** → `failure-modes.md`.
- **What does the literature say?** → `literature.md` (the corpus is local; search it before the web).
- **Is there a library or skill for this?** → `upstream-skills.md`.

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
