# Statistical Tests

Statistical testing for data analysis and hypothesis validation.

## Overview

Statistical tests help validate assumptions about data distributions, relationships, and differences between groups.

## Common Tests

### Normality Tests

```python
from scipy import stats

# Shapiro-Wilk (best for small samples, n < 5000)
stat, p = stats.shapiro(data)

# D'Agostino's K^2 (better for larger samples)
stat, p = stats.normaltest(data)

# Anderson-Darling (more sensitive in tails)
result = stats.anderson(data, dist='norm')
```

### Correlation Tests

```python
# Pearson (linear relationship, normal data)
stat, p = stats.pearsonr(x, y)

# Spearman (monotonic relationship, rank-based)
stat, p = stats.spearmanr(x, y)

# Kendall's tau (ordinal association)
stat, p = stats.kendalltau(x, y)
```

### Group Comparison

```python
# t-test (two groups, normal data)
stat, p = stats.ttest_ind(group_a, group_b)

# Mann-Whitney U (non-parametric alternative)
stat, p = stats.mannwhitneyu(group_a, group_b)

# ANOVA (more than two groups)
stat, p = stats.f_oneway(group_a, group_b, group_c)

# Kruskal-Wallis (non-parametric ANOVA)
stat, p = stats.kruskal(group_a, group_b, group_c)
```

### Chi-Square Tests

```python
# Independence test for categorical variables
contingency = pd.crosstab(df['var_a'], df['var_b'])
chi2, p, dof, expected = stats.chi2_contingency(contingency)
```

## Interpretation Guide

| p-value | Interpretation |
|---------|----------------|
| < 0.01 | Strong evidence against null hypothesis |
| 0.01 - 0.05 | Moderate evidence against null hypothesis |
| 0.05 - 0.10 | Weak evidence |
| > 0.10 | No significant evidence |

## References

- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels Documentation](https://www.statsmodels.org/)
