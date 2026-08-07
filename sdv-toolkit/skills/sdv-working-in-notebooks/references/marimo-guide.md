# Marimo Guide

Comprehensive guide for marimo notebooks: reactive execution, pure Python format, UI components, and best practices.

---

## Table of Contents

1. [What is Marimo?](#what-is-marimo)
2. [Installation and Setup](#installation-and-setup)
3. [Reactive Execution Model](#reactive-execution-model)
4. [Pure Python Format](#pure-python-format)
5. [UI Components](#ui-components)
6. [State Management](#state-management)
7. [Converting from Jupyter](#converting-from-jupyter)
8. [Running Marimo](#running-marimo)
9. [Version Control Best Practices](#version-control-best-practices)
10. [Marimo vs Jupyter](#marimo-vs-jupyter)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)

---

## What is Marimo?

Marimo is a reactive Python notebook that solves core reproducibility problems in Jupyter:

- **Reactive execution** — Cells automatically re-run when dependencies change
- **Pure Python** — Notebooks are `.py` files, not JSON
- **Git-friendly** — Readable diffs, no output blobs
- **Deterministic** — No hidden state from out-of-order execution

---

## Installation and Setup

### Installation

```bash
# With pip
pip install marimo

# With uv (fast)
uv pip install marimo

# With conda (coming soon)
# conda install -c conda-forge marimo
```

### Verify installation

```bash
marimo --version
```

---

## Reactive Execution Model

Marimo's key innovation is reactive execution. When you change a cell, all dependent cells automatically re-run.

### How it works

```python
# Cell 1: Define data
import marimo as mo
import pandas as pd

df = pd.DataFrame({
    'x': range(100),
    'y': [i**2 for i in range(100)]
})

# Cell 2: Create interactive control
threshold = mo.ui.slider(0, 100, value=50, label="Threshold")
threshold

# Cell 3: Reactive computation
# This cell AUTOMATICALLY re-runs when threshold.value changes
filtered = df[df['x'] > threshold.value]
mo.md(f"Rows with x > {threshold.value}: {len(filtered)}")
```

### Dependency tracking

Marimo builds a dependency graph from your code. It knows which cells depend on which variables.

```python
# Cell A
x = 5

# Cell B  
y = x * 2  # Depends on Cell A

# Cell C
z = y + 10  # Depends on Cell B

# If you change x in Cell A:
# - Cell B automatically re-runs
# - Cell C automatically re-runs
```

### Disabling reactivity

```python
# Use mo.stop() to conditionally stop execution
if not validate_data(df):
    mo.stop(mo.md("❌ Invalid data"))

# This only runs if validation passes
process_data(df)
```

---

## Pure Python Format

Marimo notebooks are stored as standard Python files, not JSON.

### File structure

```python
# notebook.py
import marimo

__generated_with = "0.1.0"
app = marimo.App()

@app.cell
def __():
    import pandas as pd
    return pd,

@app.cell
def __(pd):
    df = pd.DataFrame({"x": [1, 2, 3]})
    return df,

@app.cell

def __(df):
    df.head()
    return

if __name__ == "__main__":
    app.run()
```

### Benefits of .py format

| Aspect | Jupyter (.ipynb) | Marimo (.py) |
|--------|------------------|--------------|
| Git diffs | Unreadable JSON changes | Clean Python diffs |
| Code review | Difficult | Normal Python review |
| IDE support | Limited | Full Python IDE features |
| Search | Can't grep code | Standard text search |
| Import | Complex (nbimporter) | Just `import notebook` |

### Running as script

```bash
# Run notebook as Python script
python notebook.py

# Or use marimo CLI
marimo run notebook.py
```

---

## UI Components

Marimo provides built-in UI components that integrate seamlessly with reactive execution.

### Input widgets

```python
import marimo as mo

# Slider
slider = mo.ui.slider(0, 100, value=50, label="Value")
slider

# Number input
number = mo.ui.number(0, 100, value=50, label="Number")
number

# Text input
text = mo.ui.text(value="Hello", label="Name")
text

# Text area
textarea = mo.ui.text_area(value="Long text...", label="Description")
textarea

# Dropdown
dropdown = mo.ui.dropdown(["A", "B", "C"], value="A", label="Option")
dropdown

# Multiselect
multiselect = mo.ui.multiselect(["A", "B", "C"], label="Options")
multiselect

# Checkbox
checkbox = mo.ui.checkbox(value=True, label="Enable")
checkbox

# Date picker
date = mo.ui.date(label="Date")
date
```

### Displaying values

```python
# Access widget value with .value
mo.md(f"Slider value: {slider.value}")

# Use in computations
filtered_df = df[df['column'] > slider.value]
```

### Layout components

```python
# Tabs
tabs = mo.ui.tabs({
    "Tab 1": mo.md("Content 1"),
    "Tab 2": mo.md("Content 2"),
    "Tab 3": mo.md("Content 3"),
})
tabs

# Accordion
accordion = mo.ui.accordion({
    "Section 1": mo.md("Hidden content 1"),
    "Section 2": mo.md("Hidden content 2"),
})
accordion

# Sidebar
mo.sidebar(
    mo.md("## Controls"),
    slider,
    dropdown
)

# Stack (vertical layout)
mo.vstack([
    mo.md("## Header"),
    slider,
    mo.md("Results below...")
], gap=1)

# Horizontal stack
mo.hstack([slider, button, output], gap=1)
```

### Tables and dataframes

```python
# Display DataFrame with interactive controls
mo.ui.dataframe(df)

# Display with pagination
mo.ui.table(df, pagination=True, page_size=10)
```

### Async and progress

```python
# Note: In marimo, top-level await is allowed in cells
import asyncio

async def compute():
    with mo.status.spinner(subtitle="Computing..."):
        await asyncio.sleep(2)
        return expensive_computation()

result = asyncio.run(compute())

# Progress bar
for i in mo.status.progress_bar(range(100)):
    process_item(i)
```

---

## State Management

### Local state per cell

Each cell runs in its own namespace by default. Variables are automatically shared based on dependencies.

```python
# Cell 1: Define global-ish state
app_state = {
    'counter': 0,
    'data': None
}

# Cell 2: Use and modify (triggers re-run)
app_state['counter'] += 1
mo.md(f"Count: {app_state['counter']}")
```

### Reactive state patterns

> **Note:** The following examples show the `.py` file structure that marimo generates. When editing in the marimo IDE, you write cell contents directly; the `@app.cell` decorators are managed automatically.

```python
# Complete runnable example: notebook.py
import marimo

app = marimo.App()

@app.cell
def load_data():
    import pandas as pd
    df = pd.read_csv('data.csv')
    return df,

@app.cell  
def process_data(df):
    summary = df.groupby('category').sum()
    return summary,

@app.cell
def display_results(summary):
    import marimo as mo
    mo.ui.table(summary)

if __name__ == "__main__":
    app.run()
```

### Avoiding circular dependencies

Marimo detects circular dependencies and raises an error:

```python
# Cell A
x = y + 1  # Error: y not defined yet

# Cell B
y = x + 1  # Circular if both defined
```

Fix by restructuring:

```python
# Cell A: Base value
base = 10

# Cell B: Derived from base
x = base + 1

# Cell C: Derived from base
y = base + 2
```

---

## Converting from Jupyter

### Basic conversion

```bash
# Convert .ipynb to marimo .py
marimo convert notebook.ipynb -o notebook.py

# Convert and open immediately
marimo convert notebook.ipynb | marimo edit -
```

### What converts well

- Standard Python code cells
- Markdown cells
- Basic ipywidgets (some)
- Pandas DataFrame display
- Matplotlib/Plotly figures

### What needs manual adjustment

- Complex ipywidgets (use mo.ui components)
- Out-of-order execution patterns
- Hidden state dependencies
- Jupyter-specific extensions

### Post-conversion cleanup

```python
# Remove if __name__ == "__main__" cells (not needed)
# Replace manual display() calls with implicit last-expression display
# Replace get_ipython() calls with standard Python
# Convert %magic commands to standard Python or remove
```

---

## Running Marimo

### Edit mode

```bash
# Create or edit notebook
marimo edit notebook.py

# Create new notebook
marimo edit

# Edit on specific port
marimo edit notebook.py --port 8080

# Edit with host binding
marimo edit notebook.py --host 0.0.0.0
```

### Run mode (app mode)

```bash
# Run as read-only app
marimo run notebook.py

# Run on specific port
marimo run notebook.py --port 8080
```

### Export formats

```bash
# Export to HTML
marimo export html notebook.py -o notebook.html

# Export to static HTML (no server needed)
marimo export html notebook.py -o notebook.html --no-code

# Export to static Markdown
marimo export md notebook.py -o notebook.md

# Watch and auto-export
marimo export html notebook.py -o notebook.html --watch
```

---

## Version Control Best Practices

### Git setup

```bash
# .gitignore for marimo projects
__pycache__/
*.pyc
.pytest_cache/
.env
*.egg-info/
dist/
build/

# Data files (optional, depends on size)
data/*.csv
data/*.parquet
!data/README.md
```

### No output stripping needed

Unlike Jupyter, marimo doesn't embed outputs in the `.py` file. This means:

- ✅ No `nbstripout` needed
- ✅ Clean diffs by default
- ✅ No accidentally committed 50MB notebook files

### Code review workflow

```bash
# 1. Make changes to notebook.py
echo "x = 5" >> notebook.py

# 2. Normal git workflow
git add notebook.py
git commit -m "Update analysis"

# 3. Reviewers see clean Python diffs
git diff HEAD~1
```

### CI/CD for notebooks

```yaml
# .github/workflows/notebooks.yml
name: Test Notebooks
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install marimo pandas numpy
      - run: python notebook.py  # Validates notebook runs
```

---

## Marimo vs Jupyter

### When to choose marimo

| Scenario | Choose Marimo |
|----------|---------------|
| Team uses git heavily | ✅ Readable diffs |
| Need reproducibility | ✅ No hidden state |
| Building interactive apps | ✅ Reactive UI |
| Code review required | ✅ Python format |
| Sharing via version control | ✅ Clean files |

### When to choose Jupyter

| Scenario | Choose Jupyter |
|----------|---------------|
| Need specific extensions | ✅ Mature ecosystem |
| Google Colab integration | ✅ Cloud GPUs |
| Teaching beginners | ✅ Familiar format |
| Complex widget needs | ✅ ipywidgets maturity |
| Integration with specific tools | ✅ Broader support |

### Hybrid workflows

You can use both together:

```bash
# Explore in Jupyter/Colab with GPUs
# Convert to marimo for production/reporting
marimo convert exploration.ipynb -o production.py
```

---

## Advanced Features

### Custom CSS

```python
# Apply custom styles
mo.md("""
<style>
.custom-class {
    color: blue;
    font-weight: bold;
}
</style>

<div class="custom-class">Styled content</div>
""")
```

### Embedding in other apps

```python
# Embed marimo app in Flask/FastAPI
from marimo import MarimoApp

app = MarimoApp("notebook.py")
# Use app.render() in your web framework
```

### Configuration

```python
# App configuration
app = marimo.App(
    css_file="custom.css",
    head_file="head.html",
)
```

---

## Troubleshooting

### Port already in use

```bash
# Use different port
marimo edit notebook.py --port 8080

# Or let system choose
marimo edit notebook.py --port 0
```

### Module not found

```python
# Check which Python marimo is using
import sys
print(sys.executable)

# Install in that environment
# /path/to/python -m pip install package
```

### Circular dependency errors

```python
# Marimo will show which cells form a cycle
# Fix by:
# 1. Combining cells
# 2. Restructuring dependencies
# 3. Using mo.state() for complex state
```

### Performance issues

```python
# Cache expensive computations
import functools

@functools.lru_cache(maxsize=None)
def expensive_function(x):
    return x * 2

# Or use mo.cache (marimo's caching)
@mo.cache
def cached_computation(df):
    return df.expensive_operation()
```

---

## References

- [Marimo Documentation](https://docs.marimo.io/)
- [Marimo GitHub](https://github.com/marimo-team/marimo)
- [Marimo Examples](https://github.com/marimo-team/marimo/tree/main/examples)
