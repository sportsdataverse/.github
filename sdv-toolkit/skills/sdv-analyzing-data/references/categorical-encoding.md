# Categorical Encoding Reference

## Low Cardinality (< 10-15 categories)

### One-Hot Encoding
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_encoded = encoder.fit_transform(X_cat)
```

## High Cardinality (> 15-100 categories)

### Target Encoding (Mean Encoding)
```python
from category_encoders import TargetEncoder

encoder = TargetEncoder()
X_encoded = encoder.fit_transform(X_cat, y)
```

### Frequency Encoding
```python
freq_map = df['category'].value_counts().to_dict()
df['category_freq'] = df['category'].map(freq_map)
```

## Ordinal Categories

### Ordinal Encoding
```python
from sklearn.preprocessing import OrdinalEncoder

encoder = OrdinalEncoder(categories=[['low', 'medium', 'high']])
X_encoded = encoder.fit_transform(X_cat)
```

## Handling Rare Categories

```python
# Group rare categories
df['category'] = df['category'].apply(
    lambda x: x if x in frequent_categories else 'Other'
)
```
