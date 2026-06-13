---
name: add-sport-parser
description: Add sport-specific tidy parsers for an ESPN sport (soccer/cricket pattern) — parser module + per-sport codegen routing + fixtures + TDD.
disable-model-invocation: true
---

# Add Sport Parser

Adds tidy polars/pandas parsers for a sport that uses `league_param: true` mode (e.g. soccer, cricket) or any sport needing per-sport parser overrides in the ESPN cross-league surface.

---

## Parser Contract (universal across all parser modules)

- Return `polars.DataFrame` by default; pandas via `return_as_pandas=True`.
- Empty / malformed payloads → zero-row frame with documented schema. Never raise.
- Output columns snake-cased via `sportsdataverse.dl_utils.underscore`.
- Use `pandas.json_normalize` for nested flattening, then convert to polars at the end.
- Stringify list-valued cells so polars accepts the frame.
- **NEVER import from `_common_espn_parsers`** — circular import. Import only `polars`, `pandas`, `typing`, `sportsdataverse.dl_utils`.

---

## Step 1 — Create the parser module

```
sportsdataverse/<sport>/<sport>_espn_parsers.py
```

Minimal skeleton:

```python
from __future__ import annotations

from typing import Any

import pandas as pd
import polars as pl

from sportsdataverse.dl_utils import underscore


def _to_frame(records: list[dict], return_as_pandas: bool) -> pl.DataFrame | pd.DataFrame:
    if not records:
        df = pl.DataFrame()
        return df.to_pandas() if return_as_pandas else df
    pdf = pd.json_normalize(records)
    pdf.columns = [underscore(c) for c in pdf.columns]
    # stringify any list cells
    for col in pdf.columns:
        if pdf[col].apply(lambda x: isinstance(x, list)).any():
            pdf[col] = pdf[col].astype(str)
    frame = pl.from_pandas(pdf)
    return frame.to_pandas() if return_as_pandas else frame


def parse_<sport>_scoreboard(
    payload: dict[str, Any],
    return_as_pandas: bool = False,
) -> pl.DataFrame | pd.DataFrame:
    events = payload.get("events", [])
    return _to_frame(events, return_as_pandas)


def parse_<sport>_summary(
    payload: dict[str, Any],
    section: str | None = None,
    return_as_pandas: bool = False,
) -> dict[str, pl.DataFrame | pd.DataFrame] | pl.DataFrame | pd.DataFrame:
    """Dispatch all 21 sub-frames or a single named section."""
    parsers = {
        "header": _parse_summary_header,
        "lineups": _parse_summary_lineups,
        # add more sections here
    }
    if section is not None:
        fn = parsers.get(section, lambda p, r: _to_frame([], r))
        return fn(payload, return_as_pandas)
    return {name: fn(payload, return_as_pandas) for name, fn in parsers.items()}
```

Add one `_parse_summary_<section>` private helper per section.

---

## Step 2 — Register parser overrides in codegen

Open `tools/codegen/generate.py`. Add two entries:

```python
_SPORT_PARSER_OVERRIDES["<sport>"] = {
    "scoreboard": "parse_<sport>_scoreboard",
    "summary":    "parse_<sport>_summary",
    # add remaining short names
}

_SPORT_PARSER_MODULE["<sport>"] = "sportsdataverse.<sport>.<sport>_espn_parsers"
```

The codegen's `sport_parser_imports` block picks these up and emits the correct import + routing in the generated ext module. **Do not re-export from `_common_espn_parsers.py`.**

---

## Step 3 — Drop fixtures

```
tests/fixtures/espn/<sport>/<league>/<endpoint>.json
```

Capture from sdv-internal-refs or directly:

```bash
python c:\Users\saiem\Documents\sdv-internal-refs\espn\tools\espn_capture_league.py \
    <sport> <league>
cp c:\Users\saiem\Documents\sdv-internal-refs\espn\inputs\sample_bodies\<league>\... \
    tests/fixtures/espn/<sport>/<league>/
```

Add a `README.md` in each fixture directory documenting the URL + capture date.

---

## Step 4 — TDD: write failing tests first

Create `tests/test_espn_<sport>_parsers.py`:

```python
import json, pathlib, pytest
import polars as pl

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures" / "espn" / "<sport>"

def load(league: str, endpoint: str) -> dict:
    return json.loads((FIXTURE_DIR / league / f"{endpoint}.json").read_text())

def test_parse_<sport>_scoreboard_columns():
    from sportsdataverse.<sport>.<sport>_espn_parsers import parse_<sport>_scoreboard
    payload = load("<league>", "scoreboard")
    df = parse_<sport>_scoreboard(payload)
    assert isinstance(df, pl.DataFrame)
    assert df.height > 0
    assert "id" in df.columns  # adjust to actual schema

def test_parse_<sport>_scoreboard_empty():
    from sportsdataverse.<sport>.<sport>_espn_parsers import parse_<sport>_scoreboard
    df = parse_<sport>_scoreboard({})
    assert isinstance(df, pl.DataFrame)
    assert df.height == 0

def test_parse_<sport>_scoreboard_pandas():
    import pandas as pd
    from sportsdataverse.<sport>.<sport>_espn_parsers import parse_<sport>_scoreboard
    payload = load("<league>", "scoreboard")
    df = parse_<sport>_scoreboard(payload, return_as_pandas=True)
    assert isinstance(df, pd.DataFrame)
```

Run to confirm failure, implement parsers, re-run to green:

```bash
uv run pytest tests/test_espn_<sport>_parsers.py -v
```

---

## Step 5 — Regenerate + drift gate

```bash
uv run python tools/codegen/generate.py
uv run python tools/codegen/generate.py --check
uv run pytest tests/codegen/ tests/test_espn_<sport>_parsers.py -q
```

The generated ext for this sport should now route `return_parsed=True` calls through the sport-specific parsers.

---

## Step 6 — Commit

```bash
git add sportsdataverse/<sport>/<sport>_espn_parsers.py \
        tests/test_espn_<sport>_parsers.py \
        tests/fixtures/espn/<sport>/ \
        tools/codegen/generate.py \
        tools/codegen/_generated/
git commit -m "feat(<sport>): add ESPN <sport> tidy parsers (scoreboard, summary dispatcher)"
```
