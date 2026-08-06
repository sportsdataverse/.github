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
| CV strategy, metric selection, hyperparameter tuning, experiment tracking | `evaluating-ml-models` | `evaluating-ml-models` |
| Feature engineering — encoding, scaling, datetime/text features, leakage-safe preprocessing | `engineering-ml-features` | `engineering-ml-features` |
| Model registry, retraining orchestration, MLflow/Weights & Biases, Feast, DVC | `ml-pipeline` | `ml-pipeline` |
| General statistical modeling / analytics not covered by a more specific row | `data-scientist` | `data-scientist` |
| Data-quality validation and observability on pipeline inputs | `assuring-data-pipelines` | `assuring-data-pipelines` |
| Polars idiom in general (non-SDV) | `polars` skill | `polars` |
| Polars idiom inside sdv-py specifically — pinned version, removed-API tiers, bool-mask/lookaround-regex conventions | `sdv-python-reviewer` (`lens: polars`) | `sdv-toolkit:sdv-python-reviewer` |
| Hot-path profiling and optimization | `python-performance-optimization` | `python-performance-optimization` |
| Notebook workflows (Jupyter/JupyterLab/marimo/Colab) | `working-in-notebooks` | `working-in-notebooks` |
| sklearn/XGBoost on panel-sports data — writing the fit | `sdv-sklearn` (first-party) | `sdv-toolkit:sdv-sklearn` |
| sklearn/XGBoost on panel-sports data — reviewing a fit already written | `sdv-model-reviewer` (`lens: sklearn-contract`) | `sdv-toolkit:sdv-model-reviewer` |

**Resolution note.** The eight non-first-party rows above are unscoped
skills installed at `~/.claude/skills/<name>` (symlinked from
`~/.agents/skills/<name>`), invoked by their bare name with no plugin
prefix — confirmed against each `SKILL.md`'s frontmatter `name:` field, which
matches its directory name in every case. This is a different layout than
the plugin cache/marketplace trees this ecosystem's own skills ship from; do
not assume the `plugin:skill` form for these eight. These eight are
personal, machine-local directories — not a git repo, not part of any
marketplace manifest, and not installed by `sdv-toolkit` or any other
plugin — with no verifiable public install source; if a row doesn't resolve
on your machine, read it as a **topic pointer** (the kind of skill to look
for) rather than a literal invocation. `sdv-sklearn` is the exception to
that caveat — it's this ecosystem's own first-party skill
(`sdv-toolkit/skills/sdv-sklearn/`), not a personal machine-local directory,
and it's shipped.
