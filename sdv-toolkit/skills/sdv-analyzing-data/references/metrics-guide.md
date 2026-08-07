# Metrics Guide

## Classification

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, classification_report
)

# Basic metrics
print(classification_report(y_true, y_pred))

# ROC-AUC (probability)
y_proba = model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_proba)

# PR-AUC (imbalanced)
pr_auc = average_precision_score(y_test, y_proba)
```

## Regression

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
r2 = r2_score(y_true, y_pred)
```

## Custom Business Metrics

```python
# Example: Revenue-weighted accuracy
def revenue_accuracy(y_true, y_pred, revenue):
    correct = (y_true == y_pred)
    return np.sum(correct * revenue) / np.sum(revenue)
```
