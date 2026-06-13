---
name: new-example-notebook
description: Scaffold a per-sport intro Jupyter notebook (examples/notebooks/0X_<sport>_intro.ipynb).
disable-model-invocation: true
---

## Purpose

Add a new per-sport intro notebook that parallels the existing set under `examples/notebooks/`. Each notebook demonstrates the canonical surface for one sport in a consistent order, making the set easy to navigate across sports.

---

## Numbering convention

Notebooks use zero-padded two-digit prefixes so they sort correctly:

```
examples/notebooks/
  01_nfl_intro.ipynb
  02_cfb_intro.ipynb
  03_nba_intro.ipynb
  04_wnba_intro.ipynb
  05_mbb_intro.ipynb
  06_wbb_intro.ipynb
  07_nhl_intro.ipynb
  08_mlb_intro.ipynb
  09_<new_sport>_intro.ipynb   ← your file
```

Pick the next available number. The set must stay parallel — every sport gets exactly one intro notebook.

---

## Cell outline

### Cell 1 — Markdown header

```markdown
# <Sport Full Name> — sportsdataverse-py intro

Short one-paragraph description of the sport module and what data it provides.
Links: package docs, companion R package (e.g. hoopR / wehoop / cfbfastR).
```

### Cell 2 — Imports + version pin

```python
import polars as pl
import sportsdataverse.<sport> as <abbr>

print(pl.__version__)
print(<abbr>.__version__ if hasattr(<abbr>, "__version__") else "ok")
```

### Cell 3 — Schedule

```python
schedule = <abbr>.espn_<sport>_schedule(season=2024, return_parsed=True)
print(schedule.shape)
schedule.head(5)
```

One markdown cell before it explaining what the schedule endpoint returns (columns to highlight: `game_id`, `date`, `home_team`, `away_team`, `home_score`, `away_score`).

### Cell 4 — Play-by-play (if available)

```python
# Pick a recent completed game_id from schedule above
game_id = int(schedule.filter(pl.col("home_score").is_not_null())["game_id"][0])
pbp = <abbr>.espn_<sport>_pbp(event_id=game_id, return_parsed=True)
print(pbp.shape)
pbp.select(["clock_display_value", "type_text", "text", "score_value"]).head(10)
```

### Cell 5 — Teams

```python
teams = <abbr>.espn_<sport>_teams(return_parsed=True)
print(teams.shape)
teams.head(5)
```

### Cell 6 — Season stats / standings

```python
standings = <abbr>.espn_<sport>_standings(season=2024, return_parsed=True)
standings.head(10)
```

Adapt to whatever the sport's canonical season-level endpoint is (`scoreboard`, `standings`, `statistics`).

### Cell 7 — Cache + config (NFL or any cached loader)

Include only when the sport uses the NFL-style cache layer:

```python
from sportsdataverse.nfl import get_config, update_config, clear_cache
print(get_config())
update_config(cache_mode="memory", cache_duration=3600)
# ... call a loader ...
clear_cache()
```

### Cell 8 — Markdown closing

```markdown
## Next steps
- PBP deep-dive: see `examples/notebooks/0X_<sport>_pbp_deep_dive.ipynb` (if it exists)
- R parity: [<companion R package>](<url>)
- Full API reference: [sportsdataverse docs](https://py.sportsdataverse.org)
```

---

## Output hygiene

If the repo has `nbstripout` configured (check `.gitattributes` for `*.ipynb filter=nbstripout`), all cell outputs are stripped automatically on `git add`. If not configured, strip outputs manually before committing:

```bash
uv run jupyter nbconvert --ClearOutputPreprocessor.enabled=True \
    --to notebook --inplace examples/notebooks/09_<sport>_intro.ipynb
```

Never commit notebooks with large embedded outputs (images, full DataFrames) — they bloat the repo and produce noisy diffs.

---

## Checklist before committing

- [ ] File named `0X_<sport>_intro.ipynb` with the correct next number.
- [ ] All cells execute top-to-bottom without errors against a live API (run `SDV_PY_LIVE_TESTS=1 uv run jupyter nbconvert --to notebook --execute ...`).
- [ ] Outputs stripped.
- [ ] Markdown cells use plain English, no internal jargon.
- [ ] `See Also` cross-links point to the correct companion R package URL from the CLAUDE.md table.
