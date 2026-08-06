# Seaborn Statistical Visualization

## Distribution Plots

```python
import seaborn as sns

# KDE with rug
sns.kdeplot(data=df, x='value', hue='category', fill=True)
sns.rugplot(data=df, x='value')

# Boxen plot (letter-value plot)
sns.boxenplot(data=df, x='category', y='value')
```

## Regression Plots

```python
# Linear regression with confidence interval
sns.regplot(data=df, x='x', y='y', ci=95)

# Multiple regression lines
sns.lmplot(data=df, x='x', y='y', hue='category', col='group')
```

## Categorical Plots

```python
# Violin + swarm
sns.violinplot(data=df, x='cat', y='val', inner=None)
sns.swarmplot(data=df, x='cat', y='val', color='k', alpha=0.5)

# Point plot (aggregated)
sns.pointplot(data=df, x='time', y='value', hue='group', ci=68)
```

## Multi-plot Grids

```python
g = sns.FacetGrid(df, col='category', row='region')
g.map(sns.scatterplot, 'x', 'y')
```
