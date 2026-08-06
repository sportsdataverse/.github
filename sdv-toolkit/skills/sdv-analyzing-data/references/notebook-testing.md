# Testing Notebooks

## Unit Tests for Notebook Code

```python
# test_notebook_utils.py
# Extract functions from notebook into testable module

from notebook_utils import clean_data

def test_clean_data():
    input_df = pd.DataFrame({'a': [1, None, 3]})
    result = clean_data(input_df)
    assert result['a'].isna().sum() == 0
```

## nbval for Notebook Testing

```bash
pip install nbval
pytest --nbval my_notebook.ipynb
```

Validates that cell outputs match stored outputs.

## Papermill for Parameterized Execution

```python
import papermill as pm

pm.execute_notebook(
    'template.ipynb',
    'output.ipynb',
    parameters={'alpha': 0.5, 'iterations': 1000}
)
```
