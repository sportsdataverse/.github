# Hyperparameter Tuning Reference

## Optuna (Recommended)

Bayesian optimization with pruning.

```python
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 10, 200)
    max_depth = trial.suggest_int('max_depth', 2, 32, log=True)
    
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    return cross_val_score(clf, X, y, cv=5).mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f'Best score: {study.best_value:.3f}')
print(f'Best params: {study.best_params}')
```

## Ray Tune

Distributed hyperparameter tuning for larger scale.

```python
from ray import tune
from ray.tune.sklearn import TuneSearchCV

search = TuneSearchCV(
    estimator,
    param_distributions,
    n_trials=100,
    use_gpu=False
)
search.fit(X, y)
```

## Key Principles

1. Define search space based on domain knowledge
2. Use early stopping to save compute
3. Always validate best config on hold-out test set
4. Track all experiments for reproducibility
