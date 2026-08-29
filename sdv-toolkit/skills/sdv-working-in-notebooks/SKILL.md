---
name: sdv-working-in-notebooks
description: "Use for Jupyter, JupyterLab, marimo, and Google Colab workflows. Choose this skill when creating, converting, or improving reproducible notebooks for data exploration, analysis, documentation, or teaching."
---

# Working in Notebooks

Use this skill to create, maintain, and choose between notebook environments (Jupyter, marimo, Colab) for data work. Covers tool selection, reproducibility patterns, and workflow best practices.

## When to use this skill

- **Setting up a notebook environment** — choosing between Jupyter, marimo, VS Code, or Colab
- **Converting between notebook formats** — Jupyter to marimo, .ipynb to .py, or vice versa
- **Making notebooks reproducible** — pinning dependencies, managing random seeds, avoiding hardcoded paths
- **Improving notebook structure** — organizing cells, refactoring code, adding tests
- **Publishing or sharing notebooks** — nbconvert, Quarto, Voilà, or Git workflows
- **Jupyter-specific features** — magic commands, widgets, extensions, kernel management
- **Marimo-specific workflows** — reactive execution, UI components, version control patterns

## When NOT to use this skill

Use a different skill for these related but distinct tasks:

| Instead of... | Use this skill | Because... |
|---------------|----------------|------------|
| Building a stakeholder-facing dashboard | `building-data-apps` | Apps are for external users; notebooks are for analysts/developers |
| Creating interactive data explorers for non-technical users | `building-data-apps` | Streamlit, Panel, Gradio are purpose-built for this |
| Exploratory data analysis patterns | `sdv-modeling` (`references/data-sources.md`) for what to explore; the external `dataviz` skill for how to show it | `sdv-analyzing-data` was retired in 0.8.0 |
| Visualization library selection | the external `dataviz` skill | Chart choice, palettes and accessibility live there |
| Production ML feature engineering | `sdv-engineering-ml-features` | Feature engineering logic is domain-specific |
| Model evaluation and cross-validation | `sdv-evaluating-ml-models` | Model comparison and metrics belong there |

### Quick boundary check

- **Notebook** = code + markdown + outputs in cells, run interactively, often .ipynb or .py format
- **Data app** = deployed web interface with widgets, for non-coders to interact with
- If the user asks for a "dashboard," "app," or mentions "users clicking buttons," use `building-data-apps`
- If the user asks for "notebook," "Jupyter," "marimo," or "explore data interactively," use this skill

## Tool selection guide

### Quick decision checklist

| Question | If yes, consider |
|----------|------------------|
| Need reactive execution (cells auto-update)? | **marimo** |
| Want pure Python files for version control? | **marimo** |
| Need specific Jupyter extensions ecosystem? | **JupyterLab** |
| Using Google Colab features (TPU, shared GPUs)? | **Google Colab** |
| Want IDE-native experience (IntelliSense, debugger)? | **VS Code + Jupyter** |
| Converting from existing .ipynb files? | **Jupyter → marimo with `marimo convert`** |
| Teaching beginners (familiarity matters)? | **JupyterLab or Colab** |

### Tool comparison

| Tool | Best For | Key Feature | File Format |
|------|----------|-------------|-------------|
| **JupyterLab** | Traditional data science, rich extensions | Full IDE experience, 1000+ extensions | `.ipynb` (JSON) |
| **marimo** | Reproducible notebooks, reactive execution | Python-native, version-control friendly | `.py` (pure Python) |
| **VS Code + Jupyter** | IDE-native notebook experience | IntelliSense, debugging, git integration | `.ipynb` |
| **Google Colab** | Cloud GPUs, easy sharing, collaboration | Free TPU/GPU, zero setup | `.ipynb` (cloud) |

## Core workflow: Creating a reproducible notebook

### Step 1: Choose your tool

See decision checklist above. If starting fresh and reproducibility matters → marimo. If ecosystem/extensions matter → JupyterLab.

### Step 2: Set up the environment

```python
# Cell 1: Environment setup (run first)
# Set random seeds for reproducibility
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# For torch users:
# import torch
# torch.manual_seed(42)
```

### Step 3: Pin dependencies

Create `requirements.txt` or `environment.yml`:

```text
# requirements.txt
pandas==2.1.0
numpy==1.24.0
matplotlib==3.7.0
```

Or use modern tools:

```bash
# With uv
uv pip freeze > requirements.txt

# With poetry
poetry export -f requirements.txt > requirements.txt
```

### Step 4: Structure for readability

```markdown
# Title: Clear project/question description

## Setup
Imports and configuration

## Data Loading
Load and validate data

## Analysis
- Subsection per question/hypothesis
- Clear markdown explanations
- Visualizations with interpretations

## Conclusions
Key findings and next steps
```

### Step 5: Never hardcode secrets

```python
# ✅ Use environment variables
import os

api_key = os.environ.get("OPENAI_API_KEY")

# ❌ Never do this
api_key = "sk-abc123..."
```

### Step 6: Clean outputs before git (Jupyter)

```bash
# Install nbstripout
pip install nbstripout
nbstripout --install

# Or use pre-commit
pip install pre-commit
pre-commit install
```

## Validation and feedback loop

### Self-check questions

Before considering a notebook "done":

1. [ ] Can someone else run this from a fresh environment?
2. [ ] Are all random seeds set?
3. [ ] Are dependencies pinned (requirements.txt or similar)?
4. [ ] Are secrets loaded from environment variables?
5. [ ] Are cells organized logically (not execution-order dependent)?
6. [ ] Are helper functions extracted to `.py` files if >30 lines?
7. [ ] Are outputs stripped before committing (if using Jupyter)?

### Testing notebook code

See `../sdv-analyzing-data/references/notebook-testing.md` for:
- Unit tests for notebook code
- nbval for output validation
- Papermill for parameterized execution

## Progressive disclosure

### Core references

- `references/jupyter-guide.md` — Jupyter/JupyterLab deep dive: magic commands, widgets, extensions, kernel management
- `references/marimo-guide.md` — marimo deep dive: reactive execution, UI components, migration from Jupyter
- `references/reproducibility-patterns.md` — Environment management, dependency pinning, nbstripout, secrets handling

### Related references (in other skills)

- `../sdv-analyzing-data/references/notebook-testing.md` — Unit tests, nbval, Papermill for notebook validation
- `../sdv-analyzing-data/references/sharing-publishing.md` — nbconvert, Quarto, Voilà for publishing notebooks

### External resources

- [Jupyter Documentation](https://docs.jupyter.org/)
- [marimo Documentation](https://docs.marimo.io/)
- [nbstripout](https://github.com/kynan/nbstripout)
- [Quarto](https://quarto.org/)

## Common anti-patterns

- ❌ Running cells out of order (Jupyter) → Use "Run All" to verify, or switch to marimo
- ❌ Giant cells with mixed concerns → One concept per cell, <50 lines
- ❌ Hardcoded file paths → Use relative paths or environment variables
- ❌ Hardcoded secrets → Load from environment
- ❌ Committing large output files → Use .gitignore, data/ folder, or strip outputs
- ❌ Inline data → Use data/ folder or external sources
- ❌ No markdown explanations → Every code block deserves context

## Quick commands reference

### Jupyter

```bash
# Start JupyterLab
jupyter lab

# Convert notebook
jupyter nbconvert notebook.ipynb --to html
jupyter nbconvert notebook.ipynb --to script

# List kernels
jupyter kernelspec list

# Install kernel for virtual environment
python -m ipykernel install --user --name=myenv
```

### marimo

```bash
# Create/edit a notebook
marimo edit notebook.py

# Run as app (read-only)
marimo run notebook.py

# Convert from Jupyter
marimo convert notebook.ipynb -o notebook.py

# Export to HTML
marimo export html notebook.py -o notebook.html
```

### Environment validation

```python
# Check installed versions
import pandas as pd
import numpy as np

print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
```

## Related skills

| Skill | Relationship | When to use |
|-------|--------------|-------------|
| `sdv-analyzing-data` | Complementary | EDA patterns, profiling, statistical tests—use with notebooks |
| `building-data-apps` | Distinct boundary | Building stakeholder-facing dashboards—**not** this skill |
| `sdv-evaluating-ml-models` | Complementary | Cross-validation, metrics, experiment tracking |
| `sdv-engineering-ml-features` | Complementary | Feature engineering patterns and transformations |

## Migration notes

This skill replaces `data-science-notebooks` with the following changes:

- Removed `dependsOn` from frontmatter (non-standard field)
- Added explicit when-to-use and when-not-to-use sections
- Split content into focused reference files
- Clear boundary documentation vs `building-data-apps`
- Progressive disclosure with direct file paths (no `@skill` hybrid syntax)
