# Generic tier — technique references with no SDV adaptation

These 13 files came from the five skills merged into `sdv-modeling` on
2026-08-28. They are **generic**: correct ML/DS technique that would read the
same for credit-card transactions as for play-by-play. They are kept because
they are substantive and because deleting them would have destroyed 3,653 lines
of usable reference, but they carry no SDV-specific rule.

**Read the SDV tier first.** Where the two disagree about our data, the SDV tier
is right and this tier is generic advice that has not met a panel.

| Question | SDV tier (read first) | Generic tier here |
|---|---|---|
| Cross-validation | `../sklearn-xgboost.md` §A, §A2 · `../metrics-and-gates.md` §1b | `cross-validation.md` |
| Metric choice | `../metrics-and-gates.md` §1 | `metrics-guide.md` |
| Hyperparameter search | `../metrics-and-gates.md` §1b | `hyperparameter-tuning.md` |
| Model validation | `../metrics-and-gates.md` §2 (never-lower gates) | `model-validation.md` |
| Feature engineering | `../feature-engineering.md` | `feature-engineering-patterns.md`, `categorical-encoding.md`, `datetime-features.md`, `text-features.md` |
| Feature selection | `../feature-engineering.md` §4 | `feature-selection.md` |
| Training pipeline shape | `sdv-data-pipeline` ("Models are pipelines too") | `training-pipelines.md` |
| EDA and profiling | `../data-sources.md` for what exists | `profiling-automation.md`, `large-dataset-eda.md`, `statistical-tests.md` |

## The specific places this tier is wrong for us

Not hypothetical — these are the collisions that matter:

- **`cross-validation.md` presents `KFold` as a default.** On a play-by-play
  frame that is leakage; rows share a `game_id` and a `player_id`-season. See
  `../sklearn-xgboost.md` §A. It also has no notion of purging, which is what
  any feature with season-to-date memory requires (§A2).
- **`metrics-guide.md` treats a Brier score as a sufficient probability
  metric.** For us it is not: it hides the reliability/resolution split, and a
  base-rate model can post a respectable one. See `../metrics-and-gates.md` §1.
- **`model-validation.md` validates against a holdout.** Our acceptance test is
  an *external oracle* — Torvik, KenPom, FPI, the closing line — with a floor
  set below the value observed at gate time and never lowered afterwards.
- **`categorical-encoding.md`'s target encoding leaks for us.** The encoding
  must be computed as-of, from prior games only; a full-season mean joined onto
  a week-3 row carries the rest of the season backwards. See
  `../feature-engineering.md` §2.
- **`training-pipelines.md` assumes an MLOps stack we do not run.** Our registry
  is `models/REGISTRY.md`, our experiment log is `models/ledger.jsonl`, our
  artifact store is a GitHub release, and our reproducibility mechanism is a
  stage fingerprint. See `sdv-data-pipeline`.

## What was dropped rather than kept

- `experiment-tracking.md` (833 lines) and `pipeline-orchestration.md` (907) —
  MLflow, Kubeflow, Airflow, Feast, W&B. We use none of them; the equivalents
  are in `sdv-data-pipeline` and restating a stack we do not run is worse than
  silence.
- Nine visualization files (plotly-dash, streamlit, seaborn, altair, bokeh,
  holoviz-datashader, matplotlib-advanced, visualization-libraries,
  sharing-publishing) — the external `dataviz` skill covers chart choice,
  palettes and accessibility better and stays current.
- Five files in the old `sdv-analyzing-data` that were **byte-identical** copies
  of files in the ML skills (`metrics-guide`, `hyperparameter-tuning`,
  `cross-validation`) or near-copies (`categorical-encoding`,
  `feature-selection`). One copy each is kept here.
