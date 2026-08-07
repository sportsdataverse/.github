# Feature Selection Reference

## Filter Methods

```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# Mutual information
selector = SelectKBest(mutual_info_classif, k=20)
X_selected = selector.fit_transform(X, y)

# Correlation with target
correlations = X.apply(lambda col: col.corr(y))
selected = correlations.abs().nlargest(20).index
```

## Wrapper Methods

```python
from sklearn.feature_selection import RFE

rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=20)
X_rfe = rfe.fit_transform(X, y)
```

## Embedded Methods

```python
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier

# L1 regularization
lasso = Lasso(alpha=0.01)
lasso.fit(X, y)
selected = X.columns[lasso.coef_ != 0]

# Tree importance
rf = RandomForestClassifier()
rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=X.columns)
selected = importances.nlargest(20).index
```
