# Categorical Encoding Reference

Complete guide to encoding categorical variables for machine learning.

## Selection Guide

| Cardinality | Recommended | Notes |
|---|---|---|
| **Low (< 10-15)** | One-hot encoding | Sparse, interpretable |
| **Medium (15-100)** | Target encoding, frequency encoding | Balances info vs dimensionality |
| **High (> 100)** | Target encoding, embedding | Avoid dimension explosion |
| **Ordinal** | Ordinal encoding | Preserves order information |
| **Binary** | Label encoding (0/1) | Simple, efficient |

## Low Cardinality: One-Hot Encoding

```python
from sklearn.preprocessing import OneHotEncoder

# Basic one-hot
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(X_cat)

# With unknown category handling
encoder = OneHotEncoder(
    handle_unknown='ignore',      # Unknown → all zeros
    sparse_output=False
)
X_encoded = encoder.fit_transform(X_cat)

# With rare category grouping
encoder = OneHotEncoder(
    handle_unknown='infrequent_if_exist',
    min_frequency=0.01,           # Group categories below 1%
    max_categories=20             # Limit total categories
)
X_encoded = encoder.fit_transform(X_cat)
```

## High Cardinality: Target Encoding

```python
from category_encoders import TargetEncoder

# Basic target encoding
encoder = TargetEncoder(smoothing=10)
X_encoded = encoder.fit_transform(X_cat, y)
```

**When to use:** High cardinality, strong relationship with target
**Risks:** Overfitting without smoothing, data leakage if not careful

### Cross-Fold Target Encoding (Prevents Leakage)

For leak-free target encoding, encode each fold using statistics from other folds:

```python
from category_encoders import TargetEncoder
from sklearn.model_selection import KFold
import numpy as np

def cross_fold_target_encode(X_cat, y, n_splits=5, smoothing=10, random_state=42):
    """Target encoding with cross-fold encoding to prevent leakage."""
    X_encoded = np.zeros_like(X_cat, dtype=float)
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    for train_idx, val_idx in kf.split(X_cat):
        encoder = TargetEncoder(smoothing=smoothing)
        encoder.fit(X_cat.iloc[train_idx], y[train_idx])
        X_encoded[val_idx] = encoder.transform(X_cat.iloc[val_idx]).values.ravel()
    
    return X_encoded

# Usage
X_encoded = cross_fold_target_encode(X_cat, y, n_splits=5, smoothing=10)
```

**Alternative:** Use sklearn's `TargetEncoder` (available in scikit-learn 1.3+) which has built-in CV support:

```python
from sklearn.preprocessing import TargetEncoder

# sklearn TargetEncoder with built-in cross-fold encoding
encoder = TargetEncoder(
    smooth='auto',               # Automatic smoothing
    cv=5                         # 5-fold CV encoding (built-in)
)
X_encoded = encoder.fit_transform(X_cat, y)
```

## Frequency Encoding

```python
# Map categories to their frequencies
freq_map = df['category'].value_counts(normalize=True).to_dict()
df['category_freq'] = df['category'].map(freq_map)
```

**When to use:** Quick baseline, high cardinality alternative
**Benefits:** No leakage risk, captures popularity signal

## Ordinal Encoding

```python
from sklearn.preprocessing import OrdinalEncoder

# Explicit category order
encoder = OrdinalEncoder(
    categories=[['low', 'medium', 'high', 'very_high']]
)
X_encoded = encoder.fit_transform(X_cat)

# Alphabetical order (default)
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X_cat)
```

**When to use:** Categories have natural order (low/med/high, small/medium/large)
**Warning:** Using for nominal categories implies false ordering

## Binary Encoding

```python
from category_encoders import BinaryEncoder

# Efficient for high cardinality
encoder = BinaryEncoder(cols=['category'])
X_encoded = encoder.fit_transform(df)
```

**Benefits:** Logarithmic number of features vs one-hot

## Handling Rare Categories

```python
# Pre-group rare categories
def group_rare_categories(series, threshold=0.01):
    counts = series.value_counts(normalize=True)
    frequent = counts[counts >= threshold].index
    return series.apply(lambda x: x if x in frequent else 'Other')

df['category_grouped'] = group_rare_categories(df['category'], threshold=0.01)
```

## Pipeline Integration

```python
from sklearn.compose import ColumnTransformer
from category_encoders import TargetEncoder

# Different encoders for different columns
preprocessor = ColumnTransformer([
    ('onehot', OneHotEncoder(handle_unknown='ignore'), low_cardinality_cols),
    ('target', TargetEncoder(smoothing=10), high_cardinality_cols),
    ('ordinal', OrdinalEncoder(), ordinal_cols)
])
```

## Leakage Prevention

❌ **Never do this:**
```python
# WRONG: Target encoding on full dataset
df['encoded'] = TargetEncoder().fit_transform(df['category'], df['target'])
train, test = train_test_split(df)  # Leakage!
```

✅ **Correct approach:**
```python
# RIGHT: Fit on train, transform all
X_train_enc = encoder.fit_transform(X_train_cat, y_train)
X_test_enc = encoder.transform(X_test_cat)
```
