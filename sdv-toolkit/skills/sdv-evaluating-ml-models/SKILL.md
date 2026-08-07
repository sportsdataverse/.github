---
name: sdv-evaluating-ml-models
description: "Model evaluation and validation: cross-validation strategies, metrics selection, hyperparameter tuning, experiment tracking, and model comparison. Use when assessing model performance, diagnosing issues, selecting models, or optimizing hyperparameters."
dependsOn: ["@sdv-engineering-ml-features", "@sdv-building-data-pipelines"]
---

# Evaluating ML Models

Use this skill for rigorously assessing model performance, comparing alternatives, diagnosing issues, and optimizing hyperparameters.

## When to use this skill

- **Model training complete** — need systematic performance assessment
- **Comparing multiple models/algorithms** — statistical model comparison
- **Diagnosing overfitting/underfitting** — bias-variance analysis
- **Hyperparameter tuning** — finding optimal configurations
- **Selecting appropriate metrics** — matching metrics to business objectives
- **Experiment tracking** — reproducible experimentation
- **Production readiness check** — validation before deployment

## When NOT to use this skill

- Feature engineering and preprocessing → use `sdv-engineering-ml-features`
- Exploratory data analysis → use `sdv-analyzing-data`
- Building interactive data apps → use `@building-data-apps` (external skill, not bundled in sdv-toolkit)
- Notebook setup and workflows → use `@sdv-working-in-notebooks`

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| Cross-validation | **sklearn.model_selection** | Standard CV, stratified, time series, grouped |
| Classification metrics | **sklearn.metrics** | Accuracy, precision, recall, F1, ROC-AUC, PR-AUC |
| Regression metrics | **sklearn.metrics** | MAE, RMSE, R², MAPE |
| Hyperparameter tuning | **Optuna** | Bayesian optimization with pruning |
| Distributed tuning | **Ray Tune** | Large-scale distributed search |
| Experiment tracking | **MLflow** | Open-source, model registry |
| Cloud experiment tracking | **Weights & Biases** | Collaboration-focused |
| Model comparison | **scipy.stats** | Paired t-test, McNemar's test |

## Evaluation workflow

### 1. Choose cross-validation strategy

Match CV to your data characteristics:

| Data Type | CV Strategy | Implementation |
|---|---|---|
| Standard tabular | K-Fold | `KFold(n_splits=5, shuffle=True)` |
| Classification (imbalanced) | Stratified K-Fold | `StratifiedKFold(n_splits=5)` |
| Time series | Time Series Split | `TimeSeriesSplit(n_splits=5)` |
| Grouped/ clustered | Group K-Fold | `GroupKFold(n_splits=5)` |

### 2. Select appropriate metrics

**Classification:**
- Balanced: Accuracy
- Imbalanced: F1, Precision-Recall, ROC-AUC
- Cost-sensitive: Custom business metrics

**Regression:**
- Scale-independent: MAPE, R²
- Error magnitude: MAE (robust), RMSE (penalizes large errors)

### 3. Analyze performance

- Cross-validation mean ± std (estimate variance)
- Validation curves (bias-variance tradeoff)
- Learning curves (data sufficiency)
- Error analysis by segment

### 4. Hyperparameter optimization

Use Bayesian optimization for efficient search:

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 10, 200),
        'max_depth': trial.suggest_int('max_depth', 2, 32, log=True)
    }
    model = RandomForestClassifier(**params)
    return cross_val_score(model, X, y, cv=5).mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

### 5. Track and compare experiments

Log everything for reproducibility:
- Hyperparameters
- Metrics (CV and test)
- Model artifacts
- Dataset versions

## Core implementation rules

### 1. Always use proper validation

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='roc_auc')
print(f"CV AUC: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

### 2. Match metrics to problem type

```python
# Classification with imbalance
from sklearn.metrics import classification_report, roc_auc_score

print(classification_report(y_true, y_pred))
y_proba = model.predict_proba(X_test)[:, 1]
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")

# Regression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

print(f"MAE: {mean_absolute_error(y_true, y_pred):.3f}")
print(f"RMSE: {root_mean_squared_error(y_true, y_pred):.3f}")
```

### 3. Validate on hold-out test set

```python
# Final evaluation on untouched test set
# Never optimize hyperparameters on test data!
y_pred = best_model.predict(X_test)
test_score = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {test_score:.3f}")
```

### 4. Analyze errors systematically

```python
# Error by segment
errors = y_pred != y_true
error_df = X_test[errors].copy()
error_df['true'] = y_true[errors]
error_df['pred'] = y_pred[errors]

# Analyze patterns
print(error_df.groupby('category').size())
```

## Common anti-patterns

| Anti-pattern | Solution |
|---|---|
| ❌ Single train/test split without CV | Use stratified k-fold for robust estimates |
| ❌ Optimizing accuracy on imbalanced data | Use F1, PR-AUC, or class-balanced metrics |
| ❌ Data leakage in preprocessing | Fit preprocessors on train only, use pipelines |
| ❌ Not checking calibration for probabilities | Use `sklearn.calibration.CalibratedClassifierCV` |
| ❌ Ignoring inference speed/memory | Profile prediction time, consider model size |
| ❌ No error analysis | Segment errors by features to find patterns |
| ❌ Overfitting validation set | Keep final test set completely untouched |
| ❌ Not tracking random seeds | Set `random_state` everywhere for reproducibility |

## Progressive disclosure

Detailed reference guides for specific topics:

- `references/cross-validation.md` — CV strategies for different data types (K-Fold, Stratified, Time Series, Group K-Fold)
- `references/metrics-guide.md` — Choosing and interpreting classification and regression metrics
- `references/hyperparameter-tuning.md` — Optuna and Ray Tune optimization patterns
- `references/experiment-tracking.md` — MLflow and Weights & Biases setup

## Related skills

- `@sdv-engineering-ml-features` — Upstream feature engineering before evaluation
- `@orchestrating-data-pipelines` (external skill, not bundled in sdv-toolkit) — Production model deployment
- `@sdv-assuring-data-pipelines` — Model monitoring in production

## References

- [scikit-learn Model Selection](https://scikit-learn.org/stable/modules/model_selection.html)
- [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [Ray Tune Documentation](https://docs.ray.io/en/latest/tune/index.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
- [Weights & Biases Documentation](https://docs.wandb.ai/)
