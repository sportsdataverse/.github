# Upstream ML/DS skills — is there a library for this already?

Same inverted-ownership pattern `sdv-r-reviewer` already uses for R (`roxygen`
owned here, `tidy-idiom`/`style`/`cran`/etc. routed to the authoritative
upstream skill): own the SDV-specific, delegate the general, because restated
upstream guidance drifts out of date the next time the upstream skill changes.
Every row below was confirmed to resolve on disk before shipping — a routing
table pointing at a skill that doesn't exist is worse than no table, because
a reader follows it, finds nothing, and stops trusting the rest of the file.

Shorthand used in citations:

| Shorthand | Full path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `model-reviewer.md` | `sportsdataverse-org/sdv-toolkit/agents/sdv-model-reviewer.md` |
| `python-reviewer.md` | `sportsdataverse-org/sdv-toolkit/agents/sdv-python-reviewer.md` |

## Why sklearn/XGBoost is the one first-party exception

Every row below except one delegates outright, because the concern is
general — a `StandardScaler` or a Kubeflow DAG behaves the same whether the
rows are basketball plays or credit-card transactions, so an upstream skill's
answer is already correct here. **sklearn/XGBoost on panel-sports data does
not get that pass**, because the failures that bite are shaped by the panel
structure itself: a bare `sklearn.model_selection.KFold` shuffling rows
across games within a season is leakage — correlated rows (same game, same
player-season) land on both sides of the split — but a *generic* ML skill
has no way to know the rows are grouped that way, so it will never flag it;
generically, plain `KFold` is fine. `model-reviewer.md` §5 (the
`sklearn-contract` lens) already encodes the fix as a review-time check —
"never a bare `KFold`... must use `GroupKFold` (groups=) for panel data or
`TimeSeriesSplit` for anything ordered in time" — which is exactly the
SDV-specific rule a generic sklearn skill would never restate. `sdv-sklearn`
(first-party) is the build-time counterpart: where to reach for it *while
writing* the fit, not just at review time.

## Routing table

| Need | Route to | Invocation |
|---|---|---|
| CV strategy, metric selection, hyperparameter tuning, experiment tracking | `sdv-evaluating-ml-models` | `sdv-toolkit:sdv-evaluating-ml-models` |
| Feature engineering — encoding, scaling, datetime/text features, leakage-safe preprocessing | `sdv-engineering-ml-features` | `sdv-toolkit:sdv-engineering-ml-features` |
| Model registry, retraining orchestration, MLflow/Weights & Biases, Feast, DVC | `sdv-ml-pipeline` | `sdv-toolkit:sdv-ml-pipeline` |
| General statistical modeling / analytics not covered by a more specific row | `sdv-data-scientist` | `sdv-toolkit:sdv-data-scientist` |
| Data-quality validation and observability on pipeline inputs | `sdv-assuring-data-pipelines` | `sdv-toolkit:sdv-assuring-data-pipelines` |
| Polars idiom in general (non-SDV) | `sdv-polars` skill | `sdv-toolkit:sdv-polars` |
| Polars idiom inside sdv-py specifically — pinned version, removed-API tiers, bool-mask/lookaround-regex conventions | `sdv-python-reviewer` (`lens: polars`) | `sdv-toolkit:sdv-python-reviewer` |
| Hot-path profiling and optimization | `sdv-python-performance-optimization` | `sdv-toolkit:sdv-python-performance-optimization` |
| Notebook workflows (Jupyter/JupyterLab/marimo/Colab) | `sdv-working-in-notebooks` | `sdv-toolkit:sdv-working-in-notebooks` |
| Exploratory data analysis — profiling, chart selection, statistical tests | `sdv-analyzing-data` | `sdv-toolkit:sdv-analyzing-data` |
| Batch pipeline construction with Polars/DuckDB/PyArrow — ETL, medallion architecture, partitioning | `sdv-building-data-pipelines` | `sdv-toolkit:sdv-building-data-pipelines` |
| sklearn/XGBoost on panel-sports data — writing the fit | `sdv-sklearn` (first-party) | `sdv-toolkit:sdv-sklearn` |
| sklearn/XGBoost on panel-sports data — reviewing a fit already written | `sdv-model-reviewer` (`lens: sklearn-contract`) | `sdv-toolkit:sdv-model-reviewer` |

**Resolution note.** The ten non-`sdv-sklearn` rows above are vendored,
first-party skills shipped from `sdv-toolkit/skills/sdv-<name>/` — see
`sdv-toolkit/NOTICE.md` for provenance (original name, source path, and
licence state as found). They were previously personal, machine-local
directories at `~/.claude/skills/<name>` with no verifiable public install
source; vendoring replaced that machine-local dependency, so every row above
is now a literal, portable `sdv-toolkit:sdv-<name>` invocation like any other
skill in this plugin — not a topic pointer. `sdv-sklearn` remains the one
row that was never vendored from anywhere: it's this ecosystem's own
first-party skill, purpose-built for the SDV-specific concern described
above.
