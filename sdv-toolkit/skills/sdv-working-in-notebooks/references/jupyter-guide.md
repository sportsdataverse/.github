# Jupyter and JupyterLab Guide

Comprehensive guide for Jupyter notebooks and JupyterLab IDE. Covers magic commands, widgets, extensions, kernel management, and best practices.

---

## Table of Contents

1. [Jupyter vs JupyterLab](#jupyter-vs-jupyterlab)
2. [Getting Started](#getting-started)
3. [Magic Commands](#magic-commands)
4. [Cell Types and Best Practices](#cell-types-and-best-practices)
5. [Kernel Management](#kernel-management)
6. [Widgets and Interactivity](#widgets-and-interactivity)
7. [VS Code Integration](#vs-code-integration)
8. [Google Colab](#google-colab)
9. [Extensions](#extensions)
10. [Common Anti-Patterns](#common-anti-patterns)
11. [Troubleshooting](#troubleshooting)

---

## Jupyter vs JupyterLab

| Feature | Jupyter (Classic) | JupyterLab |
|---------|-------------------|------------|
| Interface | Single-document | Multi-panel IDE |
| File browser | Basic | Full file manager |
| Extensions | Limited | Rich ecosystem |
| Terminals | Separate | Integrated |
| Recommendation | Legacy use | **Default choice** |

JupyterLab is the next-generation interface and should be preferred for new projects.

---

## Getting Started

### Installation

```bash
# Basic installation
pip install jupyterlab

# With common data science packages
pip install jupyterlab pandas numpy matplotlib

# Using conda
conda install -c conda-forge jupyterlab
```

### Launching

```bash
# Start JupyterLab
jupyter lab

# Start on specific port
jupyter lab --port 8888

# Start without browser
jupyter lab --no-browser

# Start with specific directory
jupyter lab --notebook-dir=/path/to/project
```

### Creating a new notebook

1. Launch JupyterLab
2. Click `File > New > Notebook`
3. Select kernel (Python, R, Julia, etc.)

---

## Magic Commands

Magic commands are IPython-specific features (not standard Python) that start with `%` (line magic) or `%%` (cell magic).

### Essential magics

```ipython
# Auto-reload modules during development
%load_ext autoreload
%autoreload 2

# Time a single statement
%timeit sum(range(1000))

# Time an entire cell
%%timeit
import numpy as np
np.random.rand(1000, 1000)

# Enter debugger on exception
%debug

# List all variables
%who
%whos  # More detail

# Run a Python script
%run script.py

# Write cell contents to file
%%writefile myscript.py
print("Hello from file")

# Load code from file
%load myscript.py

# Run shell commands
!ls -la
!pip list

# Capture shell output
files = !ls *.csv
```

### Profiling and debugging

```ipython
# Profile a function
%prun some_function()

# Line-by-line profiling (requires line_profiler)
%load_ext line_profiler
%lprun -f my_function my_function()

# Memory profiling (requires memory_profiler)
%load_ext memory_profiler
%memit my_function()
```

### Environment documentation

```ipython
# Install: pip install watermark
%load_ext watermark
%watermark -v -m -p numpy,pandas,sklearn -g

# Output example:
# CPython 3.9.7
# IPython 7.31.0
# numpy 1.21.0
# pandas 1.3.5
# sklearn 1.0.2
# Git hash: a1b2c3d
```

---

## Cell Types and Best Practices

### Cell types

1. **Code cells** — Executable Python/R/etc. code
2. **Markdown cells** — Narrative text, equations, images
3. **Raw cells** — Unformatted text (nbconvert passes through)

### Markdown cell features

```markdown
# Headers
## Subheaders

**Bold** and *italic* text

- Bullet
- Points

1. Numbered
2. List

[Links](https://example.com)

| Tables | Work | Too |
|--------|------|-----|
| A      | B    | C   |

$LaTeX: e^{i\pi} + 1 = 0$

```python
# Code blocks within markdown
print("Hello")
```
```

### Best practices

```python
# ✅ One concept per cell
import pandas as pd

# ✅ Clear markdown before complex code
# Filter customers by region
df_regional = df[df['region'] == 'US']

# ✅ Keep cells under 50 lines
# Refactor long code into functions

# ✅ Restart and run all before sharing
# Kernel > Restart Kernel and Run All Cells
```

---

## Kernel Management

### What is a kernel?

A kernel is the computational engine that executes code. Each notebook runs in its own kernel.

### Kernel commands

```bash
# List available kernels
jupyter kernelspec list

# Install kernel for virtual environment
python -m ipykernel install --user --name=myenv --display-name="Python (myenv)"

# Remove a kernel
jupyter kernelspec uninstall myenv
```

### Kernel management in UI

- **Restart kernel** — Clear all variables, restart Python process
- **Interrupt kernel** — Stop current execution (Ctrl+C equivalent)
- **Shut down kernel** — Stop kernel to free memory

### Managing multiple environments

```bash
# Create isolated environment
python -m venv myproject_env
source myproject_env/bin/activate  # Linux/Mac
# myproject_env\Scripts\activate  # Windows

# Install kernel
pip install ipykernel
python -m ipykernel install --user --name=myproject --display-name="My Project"
```

---

## Widgets and Interactivity

Widgets add GUI elements to notebooks for interactive exploration.

### Basic widgets

```python
import ipywidgets as widgets
from IPython.display import display

# Slider
slider = widgets.IntSlider(value=50, min=0, max=100, step=1, description='Value:')
display(slider)

# Dropdown
dropdown = widgets.Dropdown(
    options=['Option 1', 'Option 2', 'Option 3'],
    value='Option 1',
    description='Choice:'
)
display(dropdown)

# Text input
text = widgets.Text(value='Hello', description='Text:')
display(text)

# Button
button = widgets.Button(description="Click me!")
output = widgets.Output()

def on_button_click(b):
    with output:
        print("Button clicked!")

button.on_click(on_button_click)
display(button, output)
```

### Interactive plots with widgets

```python
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact

@interact(freq=(1, 10, 0.1))
def plot_sine(freq=1):
    x = np.linspace(0, 2*np.pi, 1000)
    y = np.sin(freq * x)
    
    plt.figure(figsize=(10, 4))
    plt.plot(x, y)
    plt.title(f'Sine wave with frequency {freq}')
    plt.show()
```

### Linked widgets

```python
from ipywidgets import link

slider1 = widgets.FloatSlider(description='Slider 1')
slider2 = widgets.FloatSlider(description='Slider 2')

# Link the two sliders
link((slider1, 'value'), (slider2, 'value'))

display(slider1, slider2)
```

---

## VS Code Integration

VS Code provides a first-class notebook experience with IDE features.

### Setup

1. Install VS Code
2. Install Python extension (Microsoft)
3. Install Jupyter extension (Microsoft)

### Features

- **IntelliSense** — Code completion, type hints
- **Variable explorer** — Inspect DataFrames and arrays
- **Debugging** — Set breakpoints in notebook cells
- **Git integration** — Diff notebooks, strip outputs on commit
- **Multi-language** — Support for Python, R, Julia

### Running notebooks in VS Code

1. Open `.ipynb` file
2. Select kernel (top-right)
3. Run cells with Shift+Enter or play button

---

## Google Colab

Colab is a free cloud-hosted Jupyter environment with GPU/TPU access.

### Unique features

- Free Tesla T4 GPUs
- Free TPUs
- Google Drive integration
- Easy sharing (like Google Docs)
- Pre-installed data science packages

### Colab-specific commands

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Upload files
from google.colab import files
uploaded = files.upload()

# Enable GPU/TPU
# Runtime > Change runtime type > Hardware accelerator
```

```ipython
# Check GPU
!nvidia-smi
```

### Best practices for Colab

```python
# Save to Drive to persist
import shutil
shutil.copy('notebook.ipynb', '/content/drive/MyDrive/')

# Install packages (in separate cell with shell syntax)
```

```ipython
!pip install -q package_name
```

```python
# Clone repositories (via Python subprocess or use shell cell)
import subprocess
subprocess.run(['git', 'clone', 'https://github.com/user/repo.git'])
```

---

## Extensions

### JupyterLab extensions

```bash
# Install extension manager
pip install jupyterlab-git jupyterlab-code-formatter

# Table of contents
pip install jupyterlab-toc

# Variable inspector
pip install lckr-jupyterlab-variableinspector
```

### Classic notebook extensions (nbextensions)

```bash
# Install nbextensions
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# Useful extensions:
# - Table of Contents
# - Collapsible Headings
# - ExecuteTime (shows cell execution time)
# - Codefolding
```

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Run cells out of order | Hidden state, non-reproducible | Kernel > Restart and Run All |
| Giant cells | Unreadable, hard to debug | Split into logical chunks |
| Hidden state from deleted cells | Variables exist but cell is gone | Restart kernel regularly |
| Hardcoded paths | Breaks on other machines | Use relative paths or env vars |
| Committing outputs | Bloated git history | Use nbstripout or .gitattributes |
| Inline large data | Notebook becomes huge | Use external data files |
| No markdown context | Notebooks become unreadable | Explain every code section |

---

## Troubleshooting

### Kernel won't start

```bash
# Check Jupyter installation
jupyter --version

# Reinstall kernel
pip install --force-reinstall ipykernel
python -m ipykernel install --user --name=python3 --force
```

### Module not found

```python
# Check which Python is running
import sys
print(sys.executable)
```

```ipython
# Install in correct environment (in notebook)
!{sys.executable} -m pip install package_name

# Or use subprocess in pure Python:
```

```python
import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", "package_name"])
```

### Notebook won't open

```bash
# Convert to script and back
jupyter nbconvert --to script notebook.ipynb
jupyter nbconvert --to notebook notebook.py
```

### Memory issues

```python
# Monitor memory
import psutil
print(f"Memory used: {psutil.virtual_memory().percent}%")

# Clear output to free memory
from IPython.display import clear_output
clear_output()
```

---

## References

- [Jupyter Documentation](https://docs.jupyter.org/)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [IPython Magics Documentation](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
- [ipywidgets Documentation](https://ipywidgets.readthedocs.io/)
- [Google Colab Documentation](https://colab.research.google.com/notebooks/intro.ipynb)
