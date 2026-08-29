# Relationships — which skill owns what, and where to go instead

Same inverted-ownership pattern `sdv-r-reviewer` uses for R: **own the
SDV-specific, delegate the general**, because restated upstream guidance drifts
out of date the next time the upstream skill changes.

**Changed 2026-08-28.** This table used to route six modeling concerns to
separate `sdv-`-prefixed skills. Five of those were vendored generics with no
SDV adaptation — two were byte-identical to the upstream copies installed under
their own names — and they competed with `sdv-modeling` and `sdv-sklearn` for
the router on every modeling ask. They were merged in; the sixth
(`sdv-sklearn`) was first-party and became `references/sklearn-xgboost.md`. The
rows below now point at a *file in this skill* where the concern is
SDV-specific, and at an external skill where it genuinely is not.

---

## Why sklearn/XGBoost is owned here rather than delegated

A `StandardScaler` behaves the same whether the rows are basketball plays or
credit-card transactions, so an upstream skill's answer is already correct.
**sklearn/XGBoost on panel-sports data does not get that pass**, because the
failures that bite are shaped by the panel structure itself: a bare
`sklearn.model_selection.KFold` shuffling rows across games within a season is
leakage — correlated rows land on both sides of the split — but a *generic* ML
skill has no way to know the rows are grouped that way, so it will never flag
it. Generically, plain `KFold` is fine.

The same argument extends to everything merged in on 2026-08-28: our CV
strategy is chosen by *feature memory*, our metrics are gated against an
*external oracle*, and our target encoding leaks through *as-of date* rather
than through fold hygiene. None of that survives a generic restatement.

---

## Routing table

### Owned here — the concern is SDV-shaped

| Need | Go to |
|---|---|
| Writing the fit — splitting, ridge/RAPM, calibration, persistence, XGBoost interop | `references/sklearn-xgboost.md` |
| Cross-validation strategy, including purged and embargoed splits | `references/sklearn-xgboost.md` §A, §A2 · chosen via `metrics-and-gates.md` §1b |
| Metric selection, Brier decomposition, ECE, multiclass EP evaluation, conformal intervals | `references/metrics-and-gates.md` §1, §1b |
| Hyperparameter search discipline, error analysis by segment | `references/metrics-and-gates.md` §1b |
| Feature engineering — cyclical encoding, as-of target encoding, selection, id dtypes | `references/feature-engineering.md` |
| Which method fits the problem | `references/methods.md` |
| Which dataset and loader feeds it | `references/data-sources.md` |
| Whether it has been tried already **here** | `references/prior-art.md` |
| What has been PUBLISHED on it | `references/literature.md` — the 685-paper corpus is on disk at `Sports-Research-Papers/md/`; grep it before searching the web |
| Why a component that ran without error still produced a wrong result | `references/failure-modes.md` |

### Delegated — the concern is general, or lives in another SDV skill

| Need | Route to | Invocation |
|---|---|---|
| Running a model build end to end — oracle capture, worktree, TDD phases, gates, close-out | `sdv-model-build` | `sdv-toolkit:sdv-model-build` |
| Model registry row, fingerprints, one-job-per-model CI, experiment ledger, publishing artifacts | `sdv-data-pipeline` ("Models are pipelines too") | `sdv-toolkit:sdv-data-pipeline` |
| Reviewing model code someone already wrote | `sdv-model-reviewer` (pick a lens) | `sdv-toolkit:sdv-model-reviewer` |
| A validation-harness WARN on an existing dataset | `sdv-harness-triage` (pass `finding_type`) | `sdv-toolkit:sdv-harness-triage` |
| A model ported from R — id dtypes, regex semantics, NA/null drift, numeric fidelity | `sdv-parity-reviewer` | `sdv-toolkit:sdv-parity-reviewer` |
| Data-quality validation and observability on pipeline inputs | `sdv-assuring-data-pipelines` | `sdv-toolkit:sdv-assuring-data-pipelines` |
| Batch pipeline construction with Polars/DuckDB/PyArrow | `sdv-building-data-pipelines` | `sdv-toolkit:sdv-building-data-pipelines` |
| Polars idiom in general | `sdv-polars` | `sdv-toolkit:sdv-polars` |
| Polars idiom inside sdv-py — pinned version, removed-API tiers, bool-mask and lookaround-regex conventions | `sdv-python-reviewer` (`lens: polars`) | `sdv-toolkit:sdv-python-reviewer` |
| Hot-path profiling and optimization | `sdv-python-performance-optimization` | `sdv-toolkit:sdv-python-performance-optimization` |
| Notebook workflows (Jupyter/marimo/Colab) | `sdv-working-in-notebooks` | `sdv-toolkit:sdv-working-in-notebooks` |
| Charts and plots — chart choice, palettes, accessibility | the `dataviz` skill (external) | `dataviz` |
| Bayesian workflow in R — priors, pooling, diagnostics | `r-skills:r-bayes` (external) | `r-skills:r-bayes` |

---

## External libraries worth reaching for, by model family

Not skills — libraries, listed because the family they serve is one we actually
ship and the reference files above name them.

| Library / source | What it gives | Family |
|---|---|---|
| López de Prado, *Advances in Financial ML* ch. 7 | purged k-fold + embargo; the ordered-overlapping-window problem is ours exactly | pregame WP, ratings, projections |
| `sklearn.calibration` — `calibration_curve`, `CalibratedClassifierCV` | reliability binning; isotonic vs Platt selection | WP, CP, xG |
| Murphy (1973) Brier decomposition | reliability / resolution / uncertainty as three reported terms | every probability model |
| `mapie` | conformal prediction intervals against the sklearn API | ratings, projections, margins |
| `scipy.sparse.linalg.lsqr` / `lsmr`; `Ridge(solver="sparse_cg")` | tractable solves on a wide sparse design | RAPM / APM |
| `numpyro`, PyMC | partial pooling with the shrinkage strength fitted rather than assumed | player-impact priors (EPM/DARKO shape) |
| `properscoring` — CRPS | scores a simulator's full predictive distribution, not just its calibration slope | season and playoff simulators |
| `xgboost` `monotone_constraints` | enforce WP monotone in score margin and time remaining | WP, and any model with a known-sign relationship |

---

## Retired skills — where their content went

| Retired 2026-08-28 | Went to |
|---|---|
| `sdv-sklearn` (first-party, 1,201 lines) | `references/sklearn-xgboost.md`, unchanged plus §A2 purged CV and §B2 sparse solvers |
| `sdv-evaluating-ml-models` | `metrics-and-gates.md` §1b (splitter choice, tuning discipline, error analysis); its three reference files kept under `generic/` |
| `sdv-engineering-ml-features` | `references/feature-engineering.md`, SDV-rewritten; its four reference files kept under `generic/` |
| `sdv-ml-pipeline` | `generic/model-validation.md`, `generic/training-pipelines.md`, `generic/feature-engineering-patterns.md` (2,391 lines kept); `metrics-and-gates.md` §1b "our stack is not MLflow" — the MLflow/Kubeflow/Feast templates were dropped, not carried; the operational half is `sdv-data-pipeline` |
| `sdv-data-scientist` | nothing — persona and capability boilerplate with no SDV content |
| `sdv-analyzing-data` | the three non-viz references (`statistical-tests`, `large-dataset-eda`, `profiling-automation`) kept under `generic/`; the nine visualization files delegated to the external `dataviz` skill; five files were byte-identical or near-identical duplicates of the ML skills' and were dropped as dupes |

`sdv-model-spine` was **renamed** `sdv-model-build` in the same change. Same
content; "spine" was internal jargon that did not say the skill runs a build.
