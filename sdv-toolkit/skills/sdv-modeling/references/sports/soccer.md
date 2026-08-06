# Soccer — designed, not built

**Designed, not built.** `sportsdataverse/soccer/` ships exactly two files — `soccer_espn_ext.py` (112 ESPN wrappers) + `soccer_espn_parsers.py` — no `soccer_xg.py`/`soccer_player_rating.py`/`soccer_possession_value.py`/`models/` exist (verified by directory listing). `mlb.md` in this directory is the sport whose parallel "design-only" brief claim turned out false — soccer is where it's actually true. Shorthand: `plan.md` = `ClaudeCowork/plans/2026-07-07-soccer-models.md`; `design.md` = `ClaudeCowork/specs/2026-07-07-soccer-models-design.md`.

## The designed spine (all four: designed, not shipped)

① Coarse xG (ship-ready) · ② Expected threat/possession value (**data-gated** — needs event x/y, not in ESPN, ships only as a documented zero-row stub) · ③ Expected assists (data-gated, conditional path if a chance-creation column exists) · ④ Player-rating composite (ship-ready) (`design.md` §2).

**xG mechanism** (one of the four families `methods.md` says the APM corpus doesn't cover): no shot coordinates on ESPN, so instead of a per-shot logistic, a **shot-component conversion model** on per-team-match aggregates: `xg_open = β_ot·sot_np + β_off·soff` (non-pen on/off-target, β_off ≪ β_ot), `team_xg = scale·xg_open + p_pen·pen_shots`, `player_xg = team_xg · player_shots/team_shots` (pro-rata, explicitly coarse). `β_ot`/`β_off` fit by Poisson identity-link MLE; `scale` forces `Σteam_xg == Σgoals` on the training competition (`design.md` §3.3) — no fitter or fitted constant exists on disk.

**Rating mechanism:** a transparent composite, `rating = clip(base + scale·Σw_k·component_k·90/minutes, 0, 10)` over `player_xg, goals, assists, sot, saves, tackles, −fouls, −cards`; only `base`/`scale` are fitted (anchor mean≈6.5, SD≈0.7) — the weights are documented methodology, not fitted magic (`design.md` §3.4).

## Data feed

Everything is designed to route through `espn_soccer_summary` → `parse_soccer_summary` (`team_stats`/`key_events`/`leaders`), the existing ESPN cross-league surface — no new loader was needed (`design.md` §2). Future-build gotcha: `team_stats` arrives as `character` — cast `Float64` (`strict=False`), strip `%` first (`plan.md` Global Constraints).

## Gotchas (for whoever builds this)

- **Competition-agnostic algorithms, competition-specific constants**: no number hard-coded in an algorithm — every one comes from `get_competition_constants(comp)`, one sport parameterized by `league=` (unlike MBB/WBB's sibling shims); no bundled artifact by design either — closed-form + fitted scalars only, `soccer/models/` deliberately empty (`design.md` §3.1-3.2).
- **Leakage boundary is season-level**: fit on one competition-season, gate on a held-out season (EPL 2022-23→2023-24, reverse fold) — only a future rolling-form extension would need a per-match as-of cutoff (`design.md` §4).
- **②③ must never fake a stub** — a zero-row frame with the documented future schema plus a `logging.warning`, never raise; the module docstring itself is meant to BE the capture contract for the loader that would unblock them (`design.md` §3.5).

## Oracle (designed, not captured)

Two tiers, neither committed: internal calibration (Σ`team_xg` within 3% of Σ`goals` held-out; `spearman(team_xg,goals) ≥ 0.55` per-match — a noise ceiling, not a bug, since xG tracks but doesn't equal single-match goals) and rough concurrent validity vs. a designed ~20-match Understat/FBref snapshot (`≥ 0.7`), methodology-reference only, no scraping of a third party's model (`design.md` §4). No fixtures exist in `tests/fixtures/` — `data-sources.md` §4 carries no soccer row, consistent with this file's core finding.
