# Feature Selection Reference

Complete guide to selecting the most predictive features.

## Selection Strategy Overview

| Method Type | Speed | Overfitting Risk | Best For |
|---|---|---|---|
| **Filter** | Fast | Low | Many features, quick screening |
| **Wrapper** | Slow | Medium | Small feature sets, model-specific |
| **Embedded** | Medium | Low | Regularization, tree-based models |

## Filter Methods

Filter methods use statistical measures independent of any model.

### Correlation with Target

```python
# Pearson correlation (linear relationships)
correlations = X.apply(lambda col: col.corr(y))
top_features = correlations.abs().nlargest(20).index

# Spearman correlation (monotonic relationships)
from scipy.stats import spearmanr
correlations = X.apply(lambda col: spearmanr(col, y)[0])
```

### Mutual Information

Captures any statistical dependency (linear and non-linear):

```python
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

# Classification
mi_scores = mutual_info_classif(X, y, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns)
top_features = mi_series.nlargest(20).index

# Regression
mi_scores = mutual_info_regression(X, y, random_state=42)
```

### Statistical Tests

```python
from sklearn.feature_selection import SelectKBest, f_classif, chi2, f_regression

# F-test (ANOVA) - classification
selector = SelectKBest(f_classif, k=20)
X_selected = selector.fit_transform(X, y)

# Chi-square - categorical features, classification
selector = SelectKBest(chi2, k=20)
X_selected = selector.fit_transform(X, y)

# F-test - regression
selector = SelectKBest(f_regression, k=20)
X_selected = selector.fit_transform(X, y)
```

### Variance Threshold

Remove low-variance features (near-constant):

```python
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.01)  # Remove features with <1% variance
X_selected = selector.fit_transform(X)
```

## Wrapper Methods

Wrapper methods use model performance to evaluate feature subsets.

### Recursive Feature Elimination (RFE)

```python
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier

# Basic RFE
estimator = RandomForestClassifier(n_estimators=100)
selector = RFE(
    estimator=estimator,
    n_features_to_select=20,
    step=1                      # Remove 1 feature at a time
)
X_selected = selector.fit_transform(X, y)

# With cross-validation to find optimal k
selector = RFECV(
    estimator=estimator,
    step=1,
    cv=5,
    scoring='accuracy'
)
X_selected = selector.fit_transform(X, y)
print(f"Optimal number of features: {selector.n_features_}")
```

### Sequential Feature Selection

```python
from sklearn.feature_selection import SequentialFeatureSelector

# Forward selection
sfs = SequentialFeatureSelector(
    estimator=RandomForestClassifier(),
    n_features_to_select=20,
    direction='forward',        # Start with 0, add features
    cv=3
)
X_selected = sfs.fit_transform(X, y)

# Backward selection
sfs = SequentialFeatureSelector(
    estimator=RandomForestClassifier(),
    n_features_to_select=20,
    direction='backward',       # Start with all, remove features
    cv=3
)
```

## Embedded Methods

Embedded methods perform selection during model training.

### L1 Regularization (Lasso)

Automatically zeroes out unimportant features:

```python
from sklearn.linear_model import Lasso, LogisticRegression

# Lasso for regression
lasso = Lasso(alpha=0.01)
lasso.fit(X, y)
selected = X.columns[lasso.coef_ != 0]

# L1-regularized logistic regression for classification
logreg = LogisticRegression(
    penalty='l1',
    solver='liblinear',
    C=0.1                      # Inverse of regularization strength
)
logreg.fit(X, y)
selected = X.columns[logreg.coef_[0] != 0]
```

### Tree-Based Feature Importance

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Random forest importance
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=X.columns)
selected = importances.nlargest(20).index

# With permutation importance (more reliable)
from sklearn.inspection import permutation_importance

result = permutation_importance(rf, X_test, y_test, n_repeats=10)
perm_importances = pd.Series(result.importances_mean, index=X.columns)
```

### SelectFromModel

```python
from sklearn.feature_selection import SelectFromModel

# Select features using tree importance
selector = SelectFromModel(
    estimator=RandomForestClassifier(n_estimators=100),
    max_features=20,
    threshold=-np.inf           # Use max_features only
)
X_selected = selector.fit_transform(X, y)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
```

## Boruta (Shadow Features)

```python
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier

# Boruta for feature selection
rf = RandomForestClassifier(n_estimators=100)
boruta = BorutaPy(rf, n_estimators='auto', verbose=2)
boruta.fit(X.values, y)

# Selected features
selected = X.columns[boruta.support_].tolist()

# Tentative features (uncertain)
tentative = X.columns[boruta.support_weak_].tolist()
```

## Selection Pipeline Integration

```python
from sklearn.pipeline import Pipeline

# Combine selection with modeling
pipeline = Pipeline([
    ('select', SelectKBest(mutual_info_classif, k=50)),
    ('classify', RandomForestClassifier())
])

# With cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(pipeline, X, y, cv=5)
```

## Stability Selection

Identify features consistently selected across bootstrap samples:

```python
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.utils import resample
import numpy as np

def stability_selection(X, y, n_iterations=50, alpha=0.01, threshold=0.5):
    """
    Stability selection using repeated Lasso on bootstrapped samples.
    
    Parameters
    ----------
    X : DataFrame
        Feature matrix
    y : array-like
        Target variable
    n_iterations : int
        Number of bootstrap iterations
    alpha : float
        Lasso regularization strength
    threshold : float
        Minimum selection frequency to be considered stable (0-1)
    
    Returns
    -------
    selected : Index
        Features selected in >threshold% of iterations
    """
    n_features = X.shape[1]
    selection_counts = np.zeros(n_features)
    
    for i in range(n_iterations):
        # Bootstrap sample
        X_boot, y_boot = resample(X, y, random_state=i)
        
        # Fit Lasso with feature selection
        lasso = Lasso(alpha=alpha, random_state=42)
        selector = SelectFromModel(lasso, threshold='median')
        selector.fit(X_boot, y_boot)
        
        # Count selections
        selection_counts += selector.get_support().astype(int)
    
    # Features selected in >threshold% of iterations
    selection_freq = selection_counts / n_iterations
    selected = X.columns[selection_freq > threshold]
    
    return selected

# Usage
stable_features = stability_selection(X, y, n_iterations=50, alpha=0.01, threshold=0.6)
print(f"Stable features: {list(stable_features)}")
```

**Alternative:** Use `sklearn.linear_model.RandomizedLasso`'s replacement via the `celer` package for faster Lasso solving, or implement with `LogisticRegression` for classification tasks.

## Feature Selection Do's and Don'ts

### ✅ Do
- **Fit selectors on training data only**
- **Use domain knowledge** to guide selection
- **Validate selection stability** across CV folds
- **Consider computational cost** for wrapper methods
- **Combine methods** (filter then wrapper on subset)

### ❌ Don't
- **Select on full dataset** before train/test split (leakage!)
- **Use too few features** without validation
- **Ignore feature interactions** (filter methods miss these)
- **Rely solely on default thresholds** - tune for your problem

## Selection by Problem Type

| Problem | Recommended Approach |
|---|---|
| Many features (>1000) | Mutual information filter → Embedded |
| Small sample, many features | L1 regularization, Elastic Net |
| Need interpretability | Correlation, Lasso |
| Non-linear relationships | Tree importance, Mutual information |
| Feature interactions | RFE, Sequential selection |
| High-cardinality categorical | Chi-square, Mutual information |
