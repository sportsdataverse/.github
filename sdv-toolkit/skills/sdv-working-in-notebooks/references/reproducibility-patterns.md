# Reproducibility Patterns for Notebooks

Best practices for making notebooks reproducible: environment management, dependency pinning, random seeds, data versioning, and secrets handling.

---

## Table of Contents

1. [The Reproducibility Checklist](#the-reproducibility-checklist)
2. [Setting Random Seeds](#setting-random-seeds)
3. [Environment Management](#environment-management)
4. [Dependency Pinning](#dependency-pinning)
5. [Data Versioning](#data-versioning)
6. [Container Patterns](#container-patterns)
7. [Git and Pre-commit Hooks](#git-and-pre-commit-hooks)
8. [Secrets Management](#secrets-management)
9. [Avoiding Hardcoded Paths](#avoiding-hardcoded-paths)
10. [Validation and Testing](#validation-and-testing)

---

## The Reproducibility Checklist

Before sharing or publishing a notebook, verify:

- [ ] **Random seeds set** — All stochastic libraries seeded
- [ ] **Dependencies pinned** — requirements.txt or equivalent
- [ ] **Python version specified** — In README or pyproject.toml
- [ ] **Secrets externalized** — No API keys in code
- [ ] **Paths relative** — No absolute paths
- [ ] **Data accessible** — Data source documented and versioned
- [ ] **Outputs clean** — No accidental credentials in outputs
- [ ] **Runs end-to-end** — Kernel restart + run all succeeds

---

## Setting Random Seeds

### Core libraries

```python
import random
import numpy as np

# Set seeds for reproducibility
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
```

### PyTorch

```python
import torch

torch.manual_seed(RANDOM_SEED)

# For GPU determinism (may impact performance)
torch.cuda.manual_seed_all(RANDOM_SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```

### TensorFlow

```python
import tensorflow as tf

tf.random.set_seed(RANDOM_SEED)

# For full determinism (TF 2.x)
import os
os.environ['TF_DETERMINISTIC_OPS'] = '1'
```

### Complete seed function

```python
def set_all_seeds(seed: int = 42) -> None:
    """Set seeds for all random number generators."""
    import random
    import numpy as np
    
    random.seed(seed)
    np.random.seed(seed)
    
    # PyTorch (optional)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
    
    # TensorFlow (optional)
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass
    
    # Set Python hash seed (must be done before Python starts)
    # export PYTHONHASHSEED=42

# Usage
set_all_seeds(42)
```

### Documenting seeds in notebooks

```markdown
## Reproducibility

Random seed: 42

Seeds set for: Python random, NumPy, PyTorch

Expected output variance: ±0.01 due to floating-point differences
```

---

## Environment Management

### Virtual environments

```bash
# Create venv
python -m venv myproject_env

# Activate (Linux/Mac)
source myproject_env/bin/activate

# Activate (Windows)
myproject_env\Scripts\activate

# Deactivate
deactivate
```

### Conda environments

```bash
# Create from file
conda env create -f environment.yml

# Create manually
conda create -n myproject python=3.11 pandas numpy

# Activate
conda activate myproject

# Export current environment
conda env export > environment.yml
```

### Modern tools: uv

```bash
# Install uv: https://github.com/astral-sh/uv

# Create virtual environment
uv venv

# Activate
source .venv/bin/activate

# Install packages (fast!)
uv pip install pandas numpy matplotlib

# Sync from requirements
uv pip sync requirements.txt

# Freeze current state
uv pip freeze > requirements.txt
```

### Modern tools: Poetry

```bash
# Install poetry: https://python-poetry.org/

# Initialize project
poetry init

# Add dependencies
poetry add pandas numpy matplotlib

# Add dev dependencies
poetry add --group dev pytest jupyterlab

# Install all dependencies
poetry install

# Run in poetry environment
poetry run jupyter lab

# Export to requirements.txt
poetry export -f requirements.txt > requirements.txt
```

### environment.yml example

```yaml
name: myproject
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pandas=2.1.0
  - numpy=1.24.0
  - matplotlib=3.7.0
  - scikit-learn=1.3.0
  - jupyterlab=4.0.0
  - pip
  - pip:
    - some-package-only-on-pypi==1.0.0
```

---

## Dependency Pinning

### Why pin?

Without pinning:

```text
pandas  # Will install latest (breaking changes possible)
```

With pinning:

```text
pandas==2.1.0  # Exact version, reproducible
```

### requirements.txt formats

```text
# Exact pins (most reproducible)
pandas==2.1.0
numpy==1.24.0

# Minimum versions (more flexible)
pandas>=2.0.0
numpy>=1.20.0

# Compatible release (semvar-aware)
pandas~=2.1.0  # >=2.1.0, <2.2.0
```

### Generating requirements

```bash
# From current environment (not recommended - may include dev packages)
pip freeze > requirements.txt

# Using pip-tools (recommended)
pip install pip-tools

# requirements.in (high-level deps)
echo "pandas" > requirements.in
echo "numpy" >> requirements.in

# Compile to pinned requirements.txt
pip-compile requirements.in

# Sync environment to exact pins
pip-sync
```

### Poetry lock files

```bash
# poetry.lock is auto-generated and should be committed
# It pins transitive dependencies too

# Update lock file
poetry lock

# Update specific package
poetry update pandas
```

### Checking for updates

```bash
# pip-audit for security
echo "pip-audit" >> requirements-dev.txt
pip-audit

# pip-outdated
echo "pip-outdated" >> requirements-dev.txt
pip-outdated
```

---

## Data Versioning

### Option 1: DVC (Data Version Control)

```bash
# Install DVC
pip install dvc

# Initialize in project
dvc init

# Track data files
dvc add data/raw_dataset.csv

# Commit .dvc files to git
git add data/raw_dataset.csv.dvc data/.gitignore
git commit -m "Add raw dataset"

# Push to remote storage
dvc remote add -d myremote s3://mybucket/dvc
dvc push
```

### Option 2: Git LFS (for smaller files)

```bash
# Install Git LFS
git lfs install

# Track files
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "models/*.pkl"

# Commit .gitattributes
git add .gitattributes
git commit -m "Track data files with LFS"
```

### Option 3: Data registry / external storage

```python
# Download from S3/ GCS with version
import boto3

def download_data(version: str = "v1.0"):
    s3 = boto3.client('s3')
    s3.download_file(
        'mybucket',
        f'data/{version}/dataset.csv',
        'data/dataset.csv'
    )

# Document version in notebook
print("Data version: v1.0 (2024-01-15)")
```

### Option 4: Hash-based verification

```python
import hashlib

def file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# Verify data integrity
expected_hash = "a1b2c3d4..."
actual_hash = file_hash('data/dataset.csv')
assert actual_hash == expected_hash, "Data file has changed!"
```

---

## Container Patterns

### Dockerfile for notebooks

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy notebook and data
COPY notebook.ipynb .
COPY data/ ./data/

# Set random seed environment variable
ENV RANDOM_SEED=42

# Expose Jupyter port
EXPOSE 8888

# Run Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  notebook:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./data:/app/data
      - ./notebooks:/app/notebooks
    environment:
      - RANDOM_SEED=42
```

### Using the container

```bash
# Build
docker-compose build

# Run
docker-compose up

# Or with Docker directly
docker build -t my-notebook .
docker run -p 8888:8888 my-notebook
```

---

## Git and Pre-commit Hooks

### nbstripout (Jupyter)

```bash
# Install
pip install nbstripout

# Install git filter
nbstripout --install

# Apply to existing repo
nbstripout --install --attributes .gitattributes

# Manual strip
nbstripout notebook.ipynb
```

### Pre-commit framework

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.6.1
    hooks:
      - id: nbstripout
        
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.0
    hooks:
      - id: isort
        
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### .gitattributes for Jupyter

```text
# .gitattributes
*.ipynb filter=nbstripout
*.ipynb diff=ipynb
```

### .gitignore template

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints
.jupyter/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Data (adjust as needed)
data/raw/*.csv
data/processed/*.csv
!data/raw/.gitkeep
!data/processed/.gitkeep

# Models
models/*.pkl
models/*.joblib
models/*.h5
!models/.gitkeep

# Secrets
.env
.env.local
secrets.json
config.local.yml
```

---

## Secrets Management

### Never hardcode secrets

```python
# ❌ BAD: Hardcoded API key
api_key = "sk-abc123def456"

# ✅ GOOD: Environment variable
import os
api_key = os.environ.get("OPENAI_API_KEY")

# ✅ GOOD: With error handling
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

### .env files

```bash
# Install
pip install python-dotenv
```

```python
# Load .env file
from dotenv import load_dotenv
load_dotenv()  # Loads .env file into environment

# Access variables
import os
api_key = os.environ.get("OPENAI_API_KEY")
```

```text
# .env (add to .gitignore!)
OPENAI_API_KEY=sk-abc123def456
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Cloud secret managers

```python
# AWS Secrets Manager
import boto3
import json

def get_secret(secret_name: str) -> dict:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret("myproject/production")
api_key = secrets['api_key']
```

```python
# Google Cloud Secret Manager
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version_id: str = "latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### Checking for secrets before commit

```bash
# Install git-secrets
brew install git-secrets  # macOS
# or build from source

# Set up in repo
git secrets --install
git secrets --register-aws  # AWS patterns
git secrets --add 'sk-[a-zA-Z0-9]{20,}'  # OpenAI pattern

# Scan before commit
git secrets --scan
```

---

## Avoiding Hardcoded Paths

### Pathlib (Python 3.6+)

```python
from pathlib import Path

# Get project root (relative to notebook location)
PROJECT_ROOT = Path(__file__).parent.parent  # If in script
# Or for notebooks:
PROJECT_ROOT = Path.cwd().parent  # Adjust based on structure

# Build paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw" / "dataset.csv"
PROCESSED_DATA = DATA_DIR / "processed" / "clean.csv"

# Use the path
import pandas as pd
df = pd.read_csv(RAW_DATA)
```

### Environment-based paths

```python
import os
from pathlib import Path

# Allow override via environment
DATA_ROOT = Path(os.environ.get("DATA_ROOT", "./data"))
RAW_DATA = DATA_ROOT / "raw" / "dataset.csv"
```

### Configuration files

```yaml
# config.yml
data_paths:
  raw: ./data/raw
  processed: ./data/processed
  external: /mnt/shared/data
```

```python
import yaml
from pathlib import Path

with open("config.yml") as f:
    config = yaml.safe_load(f)

raw_path = Path(config['data_paths']['raw'])
```

---

## Validation and Testing

### Run-all testing

```bash
# Test that notebook runs end-to-end
jupyter nbconvert --to notebook --execute notebook.ipynb --output test.ipynb

# Or with papermill
papermill notebook.ipynb output.ipynb
```

### Notebook diff tools

```bash
# nbdime for better notebook diffs
pip install nbdime
nbdime diff notebook_v1.ipynb notebook_v2.ipynb

# Web-based diff
nbdime diff-web notebook_v1.ipynb notebook_v2.ipynb
```

### Reproducibility testing script

```python
# test_reproducibility.py
import subprocess
import sys

def test_notebook_runs():
    """Test that notebook executes without errors."""
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to", "notebook", 
         "--execute", "notebook.ipynb", "--output", "/dev/null"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Notebook failed:\n{result.stderr}"

def test_deterministic():
    """Test that notebook produces same results."""
    import hashlib
    # Run twice, compare key outputs
    pass

if __name__ == "__main__":
    test_notebook_runs()
    print("✅ Notebook runs successfully")
```

---

## References

- [nbstripout](https://github.com/kynan/nbstripout)
- [pre-commit](https://pre-commit.com/)
- [DVC Documentation](https://dvc.org/doc)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
- [Git LFS](https://git-lfs.github.com/)
