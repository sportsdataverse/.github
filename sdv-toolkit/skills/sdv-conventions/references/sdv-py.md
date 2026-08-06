# sdv-py conventions

- polars 1.x modern API only: `group_by` not `groupby`, `with_row_index`,
  `map_elements(f, return_dtype=)`, `pl.len()`, `how="full", coalesce=True`,
  `cum_sum`, `str.strip_chars`. A 0.18-era call is a bug, not a style choice.
- Bool masks explicit: `pl.col("c") == True` / `== False` (not bare `~col`).
- polars/Rust regex has no lookaround — use the inline case toggle
  `(?i)prefix(?-i: NAMES)` to stop a capture without `(?=...)`/`(?<=...)`.
- Codegen output is never hand-edited (`*_espn_ext.py`, generated
  `docs/**/reference/*`). Edit `tools/codegen/` YAML/templates, then
  `uv run python tools/codegen/generate.py && … --check` before every push.
- Returns-table column descriptions live ONLY in
  `manual_column_descriptions.yaml` (schema-keyed) — never in
  `schemas/**.yaml`, which is clobbered on re-capture.
- ID / join-key dtype discipline: pick one dtype per id at the boundary;
  assert `left.schema[k] == right.schema[k]` before any join; never paper
  over a mismatch with a float→Utf8 cast (`"123.0"` bug).
- Output columns snake_case via `dl_utils.underscore`; empty frames still
  carry the documented schema.
- New modules must be fully typed; append the module path to the
  `[tool.mypy] files` ratchet in `pyproject.toml` once it types clean.
- All HTTP goes through `dl_utils.download()`; wrappers do not wrap it in
  try/except — trust it to return or raise.
- `uv` for everything (`uv run pytest|ruff|mypy`); PEP 621 `pyproject.toml`
  only, no `setup.py` / `requirements*.txt`.
- Live tests gated by `SDV_PY_LIVE_TESTS=1`; `stats.nba.com`/`stats.wnba.com`
  use the separate `SDV_PY_NBA_STATS_LIVE=1` gate (they hang, not error, on
  datacenter/cloud IPs).
- Public callables ship Google-style docstrings with Args/Returns/Raises
  and a napoleon `Example::` block — no raw `>>>` doctest prompts.
- Don't add new per-type NFL loaders (`load_nfl_ngs_*`, per-type advstats) —
  extend the unified `load_nfl_nextgen_stats`/`load_nfl_pfr_advstats`.
- Conventional Commits, scoped subjects (`feat(cfb): …`); never an AI
  co-author trailer.
