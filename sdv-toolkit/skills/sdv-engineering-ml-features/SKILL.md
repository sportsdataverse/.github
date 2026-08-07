---
name: sdv-engineering-ml-features
description: "Feature engineering for machine learning: encoding categorical variables, scaling numeric features, datetime transformations, text features, and leakage-safe preprocessing pipelines. Use when preparing data for modeling or improving model performance through better representations."
dependsOn: ["@sdv-analyzing-data", "@sdv-building-data-pipelines"]
---

# Engineering ML Features

Use this skill for creating, transforming, and selecting features that improve model performance. Covers categorical encoding, numeric scaling, datetime engineering, text features, and building leakage-safe pipelines.

## When to use this skill

- **Categorical variables** need encoding for ML algorithms
- **Numeric features** require scaling or transformation
- **Datetime columns** need conversion to meaningful features
- **Text data** needs to be converted to numerical representations
- **Preventing data leakage** during feature engineering
- **Selecting the most predictive features** from a large set
- Building reusable, production-ready preprocessing pipelines

## When NOT to use this skill

- General data exploration → use `sdv-analyzing-data`
- Model evaluation and selection → use `@sdv-evaluating-ml-models`
- Building interactive data apps → use `@building-data-apps` (external skill, not bundled in sdv-toolkit)
- Notebook setup and workflows → use `@sdv-working-in-notebooks`

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| Categorical encoding | **category_encoders** | Beyond sklearn's limited options |
| Feature scaling | **sklearn.preprocessing** | Standard, Robust, Power transforms |
| Pipeline composition | **sklearn.pipeline + ColumnTransformer** | Reproducible, CV-safe |
| Text vectorization | **sklearn.feature_extraction.text** | TF-IDF, CountVectorizer |
| Text embeddings | **sentence-transformers** | Pre-trained semantic embeddings |
| Feature selection | **sklearn.feature_selection** | Mutual info, RFE, SelectFromModel |

## Feature engineering workflows

### 1. Categorical encoding

**Low cardinality (< 10-15 categories):** One-hot encoding
**High cardinality (> 15-100):** Target encoding or frequency encoding
**Ordinal:** Ordinal encoding with explicit category order

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from category_encoders import TargetEncoder

# One-hot for low cardinality
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Target encoding for high cardinality
te = TargetEncoder(smoothing=10)

# Ordinal for ordered categories
ord_enc = OrdinalEncoder(categories=[['low', 'medium', 'high']])
```

### 2. Numeric scaling and transformation

| Method | Use When | Algorithm Impact |
|---|---|---|
| **StandardScaler** | Features normally distributed, outliers rare | Required for SVM, neural nets, PCA |
| **RobustScaler** | Outliers present, want median/IQR centering | Same as Standard, more robust |
| **MinMaxScaler** | Need bounded range [0,1] or [-1,1] | Neural nets, image data |
| **PowerTransformer** | Skewed distributions, want normality | Improves linear model performance |
| **QuantileTransformer** | Heavy tails, want uniform/normal | Tree models unaffected, linear improves |

```python
from sklearn.preprocessing import StandardScaler, RobustScaler, PowerTransformer

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Power transform for skewness
pt = PowerTransformer(method='yeo-johnson')
X_transformed = pt.fit_transform(X_train)
```

### 3. Datetime feature engineering

Extract components and encode cyclical patterns:

```python
import numpy as np

# Component extraction
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['dayofweek'] = df['timestamp'].dt.dayofweek
df['hour'] = df['timestamp'].dt.hour

# Cyclical encoding (preserves circular nature)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# Duration features
df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days
```

### 4. Text feature engineering

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# TF-IDF for classical NLP
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(texts)

# Embeddings for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)

# Basic text statistics
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
```

### 5. Leakage-safe pipelines

**Critical rule:** Always fit on training data only, transform on all data.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

# Define preprocessing for each column type
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

# Full pipeline
pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', RandomForestClassifier())
])

# Correct: fit on train only
pipeline.fit(X_train, y_train)

# Transform train and test separately through the fitted pipeline
y_pred = pipeline.predict(X_test)  # No manual transform needed
```

**CV-safe cross-validation:**

```python
from sklearn.model_selection import cross_val_score

# Pipeline ensures preprocessing happens within each CV fold
scores = cross_val_score(pipeline, X, y, cv=5)
```

### 6. Feature selection

| Method | Description | Best For |
|---|---|---|
| **Filter (mutual_info)** | Statistical measure vs target | Quick screening, many features |
| **Filter (correlation)** | Linear correlation with target | Linear models, fast baseline |
| **Wrapper (RFE)** | Recursive feature elimination | Small-medium feature sets |
| **Embedded (L1)** | Lasso zeroes out features | Linear models with sparsity |
| **Embedded (tree)** | Feature importance from trees | Tree-based models |

```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif, RFE
from sklearn.linear_model import Lasso

# Mutual information filter
selector = SelectKBest(mutual_info_classif, k=20)
X_selected = selector.fit_transform(X_train, y_train)

# Recursive feature elimination
rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=20)
X_rfe = rfe.fit_transform(X_train, y_train)

# L1 regularization (embedded)
lasso = Lasso(alpha=0.01)
lasso.fit(X_train, y_train)
selected_features = X_train.columns[lasso.coef_ != 0]
```

## Core implementation rules

### 1. Prevent data leakage

❌ **Wrong:** Fitting encoders/scalers on full dataset
✅ **Right:** `fit_transform()` on train, `transform()` on test

```python
# Train
scaler.fit_transform(X_train)
# Test - ONLY transform!
scaler.transform(X_test)
```

### 2. Handle unknown categories

```python
# Unknown categories become all zeros
OneHotEncoder(handle_unknown='ignore')

# Unknown categories grouped with rare ones
OneHotEncoder(handle_unknown='infrequent_if_exist', min_frequency=0.01)
```

### 3. Track feature names through pipelines

```python
# Get feature names after ColumnTransformer
feature_names = preprocessor.get_feature_names_out()
```

### 4. Document feature importance

Track which features were created, why, and their expected impact on model performance.

## Common anti-patterns

| Anti-pattern | Solution |
|---|---|
| ❌ Fitting preprocessors on full dataset | Use train/test split before any fitting |
| ❌ One-hot encoding high-cardinality features (>100 categories) | Use target encoding or frequency encoding |
| ❌ Ignoring scaling for distance-based models | Always scale for SVM, k-NN, neural nets, PCA |
| ❌ Creating features without domain reasoning | Validate features make business sense |
| ❌ Not validating feature distributions match between train/test | Use distribution tests or visual comparison |
| ❌ Target encoding without smoothing | Use smoothing parameter to handle rare categories |
| ❌ Forgetting cyclical encoding for time | Use sin/cos for hour, dayofweek, month |

## Progressive disclosure

Reference guides for detailed implementations:

- `references/categorical-encoding.md` — Comprehensive encoding strategies and selection guidance
- `references/datetime-features.md` — Time-based feature patterns and cyclical encoding
- `references/text-features.md` — NLP feature engineering with TF-IDF and embeddings
- `references/feature-selection.md` — Selection strategies and implementation patterns

## Related skills

- `sdv-analyzing-data` — Understand data before engineering features
- `@sdv-evaluating-ml-models` — Validate feature impact on model performance
- `@sdv-building-data-pipelines` — Data processing fundamentals and pipeline patterns

## References

- [scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [category_encoders](https://contrib.scikit-learn.org/category_encoders/)
- [Feature-engine Documentation](https://feature-engine.trainindata.com/)
- [Sentence Transformers](https://www.sbert.net/)
