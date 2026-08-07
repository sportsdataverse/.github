# Large Dataset EDA

Strategies for exploratory analysis with large datasets.

## Overview

When datasets exceed available memory or visualization capacity, special techniques are needed for effective exploration.

## Sampling Strategies

### Random Sampling

```python
import polars as pl

# Sample for initial exploration
sample = pl.scan_parquet("large.parquet").collect().sample(10000)
```

### Stratified Sampling

```python
from sklearn.model_selection import train_test_split

sample, _ = train_test_split(
    df, train_size=10000, 
    stratify=df['category']
)
```

## Aggregation Techniques

### Pre-binned Visualization

```python
import altair as alt

alt.Chart(df).mark_rect().encode(
    x=alt.X('x:Q', bin=alt.Bin(maxbins=50)),
    y=alt.Y('y:Q', bin=alt.Bin(maxbins=50)),
    color='count()'
)
```

### Datashader for Rasterization

```python
import datashader as ds
import datashader.transfer_functions as tf

cvs = ds.Canvas(plot_width=800, plot_height=600)
agg = cvs.points(df, 'x', 'y')
img = tf.shade(agg)
```

## Lazy Evaluation with Polars

```python
import polars as pl

lf = pl.scan_parquet("large/*.parquet")

# Chain operations lazily
result = (
    lf.filter(pl.col('value') > 0)
    .group_by('category')
    .agg(pl.col('value').mean())
    .collect()  # Execute only at the end
)
```

## Memory-Efficient Patterns

| Dataset Size | Strategy |
|--------------|----------|
| < 1M rows | Load fully, use standard tools |
| 1M - 10M rows | Sample for exploration, full data for aggregates |
| 10M - 100M rows | Lazy evaluation, chunked processing |
| > 100M rows | Datashader, database engines, distributed |

## References

- [Datashader Docs](https://datashader.org/)
- [Polars Lazy API](https://docs.pola.rs/user-guide/lazy/)
