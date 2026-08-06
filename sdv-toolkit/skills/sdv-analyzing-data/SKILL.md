---
name: sdv-analyzing-data
description: "Exploratory data analysis and visualization: profiling datasets, choosing appropriate charts, applying statistical tests, and creating effective visualizations for insight communication. Use when understanding data structure, exploring distributions and relationships, selecting visualization libraries, or producing analysis-ready charts."
---

# Analyzing Data

Use this skill for exploratory data analysis and visualization: understanding dataset structure, identifying patterns, choosing the right visualization approach, and communicating insights effectively.

## When to use this skill

- New dataset — need orientation on structure, types, distributions
- Choosing visualization libraries and chart types for a project
- Data quality investigation — find anomalies, missing patterns, outliers
- Statistical hypothesis testing — validate assumptions about data
- Creating publication-quality figures or exploratory charts
- Large dataset exploration — sampling and aggregation strategies
- Understanding missing value mechanisms (MCAR/MAR/MNAR)
- Before feature engineering — understand variable relationships
- Model preparation — validate assumptions about data

## When NOT to use this skill

- Building interactive dashboards or data applications → use `@building-data-apps` (external skill, not bundled in sdv-toolkit)
- Feature engineering for ML pipelines → use `@sdv-engineering-ml-features`
- Model evaluation and comparison → use `@sdv-evaluating-ml-models`
- Notebook-specific workflows (Jupyter/marimo setup) → use `@sdv-working-in-notebooks`

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| Automated profiling | **ydata-profiling / pandas-profiling** | Fast comprehensive reports |
| Interactive exploration | **ipywidgets + plotly** | Drill-down capability |
| Statistical visualization | **Seaborn** | Quick EDA with statistical defaults |
| Publication-quality static plots | **Matplotlib** | Fine control over every element |
| Interactive web charts | **Plotly** | Easy interactive dashboards |
| Large datasets (100k+ points) | **hvPlot + Datashader** | Automatic rasterization |
| Large-data EDA (memory-efficient) | **Polars + lazy** | Memory-efficient operations |
| Declarative grammar | **Altair** | Vega-Lite transformations |
| Statistical tests | **scipy.stats** | Normality, correlations, t-tests |

## Core analysis workflow

1. **Profile structure**
   - Schema, types, cardinality
   - Missing value patterns
   - Automated profiling with ydata-profiling

2. **Analyze distributions**
   - Numerical: histograms, boxplots, KDE, skewness
   - Categorical: frequencies, rare categories
   - Identify outliers and anomalies

3. **Explore relationships**
   - Correlation matrix (numerical)
   - Cross-tabulations (categorical)
   - Target-variable relationships
   - Statistical significance tests

4. **Identify issues**
   - Outliers and anomalies (document, don't auto-remove)
   - **Duplicates** — check for duplicate rows/keys
   - **Class imbalance** — for classification, check target distribution
   - **Temporal patterns** — for time series, check seasonality, trends, gaps
   - **Inconsistencies** — conflicting values, broken referential integrity

5. **Visualize for insight**
   - Match chart type to question
   - Maximize data-ink ratio
   - Choose appropriate interactivity level

6. **Validate and document**
   - Check assumptions against domain knowledge
   - Document findings for team
   - Flag issues for investigation

## Library selection guide

### Static visualization

| Library | Best For | Learning Curve |
|---|---|---|
| **Matplotlib** | Publication-quality plots, fine control | Moderate |
| **Seaborn** | Statistical visualization, quick EDA | Easy |

### Interactive visualization

| Library | Best For | Interactivity |
|---|---|---|
| **Plotly** | Web charts, dashboards | High |
| **Altair** | Declarative statistical charts | Medium |
| **hvPlot/HoloViz** | Large data, linked brushing | High |
| **Bokeh** | Custom interactive web apps | High |

### Statistical analysis

| Library | Best For |
|---|---|
| **scipy.stats** | Hypothesis tests, distributions |
| **statsmodels** | Regression diagnostics, time series |

## Core implementation principles

### Match chart to question

| Question | Chart Type |
|---|---|---|
| Distribution? | Histogram, KDE, boxplot, violin |
| Relationship? | Scatter, line, heatmap |
| Comparison? | Bar, grouped bar, dot plot |
| Trend over time? | Line, area |
| Composition? | Stacked bar, treemap (avoid pie charts) |

### Maximize data-ink ratio

- Remove unnecessary gridlines, borders, backgrounds
- Use color purposefully (not decoration)
- Label directly when possible
- One message per visualization

### Validate assumptions

- Check for expected ranges/business rules
- Verify temporal consistency
- Confirm key relationships match domain knowledge
- Apply appropriate statistical tests

## Common anti-patterns

- ❌ Skipping profiling and jumping to modeling
- ❌ Treating all outliers as errors (some are valid signals)
- ❌ Ignoring missing value mechanisms (MCAR/MAR/MNAR)
- ❌ Pie charts with many slices (use bar charts instead)
- ❌ Dual y-axes (hard to read, try normalization)
- ❌ 3D charts (distorts perception)
- ❌ Rainbow colormaps (use perceptually uniform: viridis, plasma)
- ❌ Overplotting large datasets without handling
- ❌ Not documenting findings for team

## Common issues and solutions

| Problem | Solution |
|---|---|
| Overplotting (100k+ points) | Use Datashader (rasterization), hexbin, or 2D histogram |
| Slow interactivity | Reduce data points, use WebGL (Plotly), or pre-aggregate |
| Large file size | Save as JSON (Plotly/Altair) or use static images |
| Color blindness | Use colorblind-friendly palettes (viridis, colorbrewer) |

## Progressive disclosure

- `references/profiling-automation.md` — ydata-profiling, Sweetviz, D-Tale automated profiling
- `references/statistical-tests.md` — SciPy and statsmodels statistical testing guide
- `references/visualization-libraries.md` — Matplotlib, Seaborn, Plotly, Altair, HoloViz, Bokeh patterns
- `references/large-dataset-eda.md` — Sampling, aggregation, Datashader for large data

## Related skills

- `@sdv-engineering-ml-features` — Next step: transform insights into model features
- `@sdv-evaluating-ml-models` — Validate modeling assumptions with proper evaluation
- `@building-data-apps` (external skill, not bundled in sdv-toolkit) — Build interactive dashboards from analysis results
- `@sdv-working-in-notebooks` — Notebook-specific workflows and reproducibility

## References

- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Plotly Python](https://plotly.com/python/)
- [Altair Documentation](https://altair-viz.github.io/)
- [HoloViz Tutorial](https://holoviz.org/tutorial/)
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Python Graph Gallery](https://python-graph-gallery.com/)
