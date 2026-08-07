# sdv-toolkit

SportsDataverse engineering toolkit, shared across the ~40 SDV repos (Python + R).

<!-- GENERATED FROM catalog.json BY tools/render.py -- DO NOT EDIT BY HAND -->

Every skill invokes as `/<name>`. A `SessionStart` router emits a per-archetype
routing card automatically; run `/sdv-guide` for the full index.

## Skills

| Skill | When to reach for it |
|---|---|
| `/sdv-add-source` | Add a league/sport/endpoint/provider to sdv-py: capture, catalog, returns doc, scaffold, fixtures, drift gate. |
| `/sdv-analyzing-data` | Exploratory data analysis: dataset profiling, chart selection, statistical tests, and insight-communicating visualizations. |
| `/sdv-assuring-data-pipelines` | Data quality validation and observability for pipelines via Great Expectations/Pandera plus OpenTelemetry/Prometheus monitoring. |
| `/sdv-building-data-pipelines` | Production batch data pipelines with Polars, DuckDB, and PyArrow -- ETL patterns, medallion architecture, and partitioning. |
| `/sdv-conventions` | Archetype convention packs; the router points here. |
| `/sdv-data-pipeline` | Producer lifecycle for -raw/-data repos: standardize, placement, scrape, build, validate, publish. |
| `/sdv-data-scientist` | Advanced analytics, ML modeling, and statistical analysis for data-driven insights and business intelligence. |
| `/sdv-dataset-lifecycle` | Drive a new or updated release tag through all 12 downstream surfaces across five repos; record deliberate skips. |
| `/sdv-document` | Produce documentation surface: Python returns schema, roxygen @return table, notebook, pkgdown theming. |
| `/sdv-engineering-ml-features` | Feature engineering for machine learning: encoding, scaling, datetime/text transforms, and leakage-safe preprocessing pipelines. |
| `/sdv-evaluating-ml-models` | Model evaluation and validation: cross-validation strategies, metrics selection, hyperparameter tuning, experiment tracking, and model comparison. |
| `/sdv-guide` | Callable index: what the toolkit has, when to use each part, and the rename map. |
| `/sdv-learn` | Promote a durable session finding into the right toolkit surface, with its detection test. |
| `/sdv-ml-pipeline` | Production ML pipeline infrastructure: experiment tracking, Kubeflow/Airflow DAGs, feature stores, model registries, and retraining automation. |
| `/sdv-model-spine` | Oracle-gated model build loop: capture oracle, worktree, harness, TDD, gates, parity, close-out. |
| `/sdv-modeling` | Modeling domain reference: methods, data sources, prior art, metrics and gates, failure modes, per-sport inventories. |
| `/sdv-polars` | High-performance polars DataFrame patterns for ETL and analytics -- lazy queries, streaming, and Arrow interop. |
| `/sdv-port` | Port logic between R, Python, and pandas/polars, parity-test-first against real fixtures. |
| `/sdv-python-performance-optimization` | Profile and optimize Python code with cProfile and memory profilers to find and fix performance bottlenecks. |
| `/sdv-regen-docs` | Regenerate sdv-py reference docs, verify the Docusaurus build, and snapshot a versioned archive at release. |
| `/sdv-ship` | Land a change: regen docs, preflight, commit, push, bot-triage, codegen gate, merge, stack retarget, release. |
| `/sdv-sklearn` | scikit-learn and XGBoost modeling failures specific to panel-sports data, each with its detection test. |
| `/sdv-triage` | Sweep open issues and PRs across the org, classify each, act on tiers 0-1, propose tiers 2-4. |
| `/sdv-working-in-notebooks` | Reproducible Jupyter/JupyterLab/marimo/Colab notebook workflows for exploration, analysis, documentation, and teaching. |

## Agents

| Agent | What it reviews |
|---|---|
| `sdv-dataset-coverage-auditor` | Read-only: report which of the 12 dataset propagation surfaces are missing, per dataset or across the inventory. |
| `sdv-docs-reviewer` | Audit or produce the three-column returns table, Python or R; map a provider payload into documentation. |
| `sdv-harness-triage` | Triage a validation-harness WARN by finding_type and emit a Verdict. |
| `sdv-issue-triage` | Classify one open issue or PR into one of six verdicts, read-only, with evidence. |
| `sdv-model-reviewer` | Audit new model/validation code: gates, leakage boundary, metric fit, silent no-op, sklearn contract, lineage, oracle joins. |
| `sdv-parity-reviewer` | Audit a cross-language port for ID-dtype, regex, indexing, null-semantics, and numeric-fidelity bug classes. |
| `sdv-python-reviewer` | Python review by lens: polars \| http \| parser-contract \| docstring. |
| `sdv-r-reviewer` | R review by lens; owns roxygen/pkgdown/parity, routes general R concerns upstream. |
