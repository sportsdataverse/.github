---
name: add-espn-league
description: Register a new ESPN league family in sdv-py — leagues.yaml row, pre-create package dir + __init__, regenerate, gated live test, verify the drift gate.
disable-model-invocation: true
---

# Add ESPN League

Registers a new ESPN league in sdv-py end-to-end. Two optional phases: Part A captures bodies in sdv-internal-refs; Part B wires the Python package.

---

## Part A — Capture in sdv-internal-refs (optional but recommended)

```bash
cd c:\Users\saiem\Documents\sdv-internal-refs
python espn/tools/espn_capture_league.py <sport> <league>          # e.g. hockey men-college-hockey
python espn/tools/espn_capture_league.py <sport> <league> --ncaa   # if NCAA-scoped
python espn/tools/gen_returns_doc.py espn/inputs/sample_bodies/<league>/
```

Captured bodies land in `espn/inputs/sample_bodies/<league>/`. The returns doc records host, endpoint, top-level keys, and row shapes.

---

## Part B — Wire in sdv-py

**Working dir:** `c:\Users\saiem\Documents\GitHub-Data\sdv-dev\sdv-py`

### Step 1 — Add the leagues.yaml row

Open `tools/codegen/endpoints/leagues.yaml`. Add a new entry under the correct sport block:

```yaml
- prefix: <prefix>       # e.g. mhockey
  sport: <sport>         # e.g. hockey
  league: <league-slug>  # e.g. mens-college-hockey
  scopes:
    - universal
    # - ncaa        # add for NCAA-scoped extras
    # - football    # add for gridiron extras
    # - mlb         # add for baseball extras
```

### Step 2 — Pre-create the package dir (CRITICAL — codegen does NOT scaffold dirs)

**Codegen will `FileNotFoundError` if the package directory does not exist before you run it.**

```bash
PREFIX=<prefix>  # e.g. mhockey
mkdir -p sportsdataverse/$PREFIX
printf 'from __future__ import annotations\n\nfrom sportsdataverse.%s.%s_espn_ext import *  # noqa: F401,F403\n' "$PREFIX" "$PREFIX" \
  > sportsdataverse/$PREFIX/__init__.py
```

PowerShell equivalent:

```powershell
$p = "<prefix>"
New-Item -ItemType Directory -Force "sportsdataverse\$p"
Set-Content "sportsdataverse\$p\__init__.py" "from __future__ import annotations`n`nfrom sportsdataverse.$p.${p}_espn_ext import *  # noqa: F401,F403`n"
```

### Step 3 — Regenerate

```bash
uv run python tools/codegen/generate.py
```

This writes:
- `sportsdataverse/<prefix>/<prefix>_espn_ext.py` (live module)
- `tools/codegen/_generated/<prefix>_espn_ext.py` (staging copy)
- `docs/docs/<prefix>/` (reference docs)

### Step 4 — Verify import + wrapper count

```python
python -c "
import importlib, sportsdataverse.<prefix> as m
fns = [k for k in dir(m) if k.startswith('espn_')]
print(len(fns), 'wrappers')
print(fns[:5])
"
```

Expected counts: universal-only ≈ 110, +ncaa ≈ 113, +football ≈ 115, +ncaa+football ≈ 118.

### Step 5 — Drift gate

```bash
uv run python tools/codegen/generate.py --check
uv run pytest tests/codegen/ -q
```

Both must pass cleanly before committing.

### Step 6 — Add a gated live test

Append to `tests/test_espn_live.py`:

```python
def test_espn_<prefix>_teams_live():
    from sportsdataverse.<prefix> import espn_<prefix>_teams
    data = espn_<prefix>_teams()
    assert isinstance(data, dict)
    assert len(data) > 0
```

The module-level `pytestmark = skip_if_no_live` gates this automatically.

### Step 7 — Run gated live tests

```bash
SDV_PY_LIVE_TESTS=1 uv run pytest -k "<prefix>" -v
```

### Step 8 — Commit

```bash
git add sportsdataverse/<prefix>/ tools/codegen/endpoints/leagues.yaml \
        tools/codegen/_generated/ docs/docs/<prefix>/
git commit -m "feat(<prefix>): register ESPN <league> league family (~NNN wrappers)"
```

No `Co-Authored-By` trailers. Conventional Commits format only.

---

## Worked Example — Adding NCAA Men's Ice Hockey

```yaml
# leagues.yaml
- prefix: mhockey
  sport: hockey
  league: mens-college-hockey
  scopes:
    - universal
    - ncaa
```

```bash
mkdir -p sportsdataverse/mhockey
printf 'from __future__ import annotations\n\nfrom sportsdataverse.mhockey.mhockey_espn_ext import *  # noqa: F401,F403\n' \
  > sportsdataverse/mhockey/__init__.py
uv run python tools/codegen/generate.py
python -c "import sportsdataverse.mhockey as m; print(sum(1 for k in dir(m) if k.startswith('espn_')))"
# expect ~113
uv run python tools/codegen/generate.py --check
```
