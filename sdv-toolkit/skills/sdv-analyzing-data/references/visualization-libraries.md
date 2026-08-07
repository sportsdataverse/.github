# Visualization Libraries

Detailed guide to Python visualization libraries.

## Matplotlib

Fine-grained control for publication-quality static plots.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, alpha=0.6)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Title')
plt.tight_layout()
```

## Seaborn

Statistical visualization with sensible defaults.

```python
import seaborn as sns

# Distribution
sns.histplot(data=df, x='value', kde=True)

# Categorical
sns.boxplot(data=df, x='category', y='value')

# Correlation
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

## Plotly

Interactive web-based visualizations.

```python
import plotly.express as px

fig = px.scatter(df, x='x', y='y', color='category',
                 marginal_x='histogram')
fig.show()
```

## Altair

Declarative statistical visualization.

```python
import altair as alt

chart = alt.Chart(df).mark_circle().encode(
    x='x:Q',
    y='y:Q',
    color='category:N'
).interactive()
```

## hvPlot / HoloViz

Large data and linked views.

```python
import hvplot.pandas

df.hvplot.scatter(x='x', y='y', datashade=True)
```

## Bokeh

Custom interactive web applications.

```python
from bokeh.plotting import figure, show

p = figure(title="Plot")
p.circle('x', 'y', source=source)
show(p)
```

## References

- [Matplotlib Docs](https://matplotlib.org/)
- [Seaborn Docs](https://seaborn.pydata.org/)
- [Plotly Python](https://plotly.com/python/)
- [Altair Docs](https://altair-viz.github.io/)
- [HoloViz](https://holoviz.org/)
- [Bokeh Docs](https://docs.bokeh.org/)
