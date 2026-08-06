# Altair Grammar of Graphics

## Transformation Pipeline

```python
import altair as alt

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('month:T', timeUnit='month'),
    y='average(value):Q'
).transform_filter(
    alt.datum.year == 2024
)
```

## Faceting

```python
chart.facet(
    column='category:N',
    row='region:N'
)
```

## Interactive Selections

```python
brush = alt.selection_interval()

points = alt.Chart(df).mark_point().encode(
    x='x:Q',
    y='y:Q',
    color=alt.condition(brush, 'category:N', alt.value('lightgray'))
).add_params(brush)
```

## Export

```python
chart.save('chart.html')  # Self-contained
chart.save('chart.png', scale_factor=2)  # High-res static
```
