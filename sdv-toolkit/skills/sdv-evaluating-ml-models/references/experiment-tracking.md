# Experiment Tracking

## MLflow

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metrics({'accuracy': acc, 'f1': f1})
    mlflow.sklearn.log_model(model, 'model')
    mlflow.log_artifact('confusion_matrix.png')
```

## Weights & Biases

```python
import wandb

wandb.init(project='my-project', config=params)
wandb.log({'accuracy': acc, 'f1': f1})
wandb.sklearn.plot_confusion_matrix(y_true, y_pred, labels)
```

## Best Practices

- Log hyperparameters before training
- Log metrics at each epoch/iteration
- Version datasets used
- Log artifacts (plots, model files)
- Tag runs for organization
