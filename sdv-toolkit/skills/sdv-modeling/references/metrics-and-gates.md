# Metrics and gates — how do I know this model works?

Distilled from the NBA model-validation-harness spec/plan (the only source
that designs a validation harness from first principles), the shipped
`sdv-model-reviewer` agent (the authoritative statement of the gate/leakage/
metric-fit rules — this file expands it, never contradicts it), and real
gate tests + fixture READMEs already committed in `sdv-py`. Every rule below
cites the file it came from; an uncited claim here should be treated as
invented. Metric names, thresholds, and code identifiers are quoted
verbatim from source — do not take a paraphrase over the cited line.

Shorthand used in citations:

| Shorthand | Full path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `reviewer.md` | `sportsdataverse-org/sdv-toolkit/agents/sdv-model-reviewer.md` |
| `harness-design.md` | `ClaudeCowork/nba_data/specs/2026-07-01-nba-model-validation-harness-design.md` |
| `harness-plan.md` | `ClaudeCowork/nba_data/plans/2026-07-01-nba-model-validation-harness-plan.md` |
| `metrics.py` | `sdv-py/sportsdataverse/_common/metrics.py` |
| `cfb-ratings-oracle.py` | `sdv-py/tests/cfb/test_cfb_ratings_oracle.py` |
| `cfb-prediction-backtest.py` | `sdv-py/tests/cfb/test_cfb_prediction_backtest.py` |
| `cfb-season-odds-calibration.py` | `sdv-py/tests/cfb/test_cfb_season_odds_calibration.py` |
| `cfb-ratings-parity-ship.md` | `sdv-py/dev/session-notes/2026-07-28-cfb-ratings-parity-ship.md` |
| `mbb-prediction-backtest.py` | `sdv-py/tests/mbb/test_mbb_prediction_backtest.py` |
| `nba-playtype-constants.py` | `sdv-py/sportsdataverse/nba/nba_playtype_constants.py` |
| `mbb_prediction/README.md` | `sdv-py/tests/fixtures/mbb_prediction/README.md` |
| `nhl_player_impact/README.md` | `sdv-py/tests/fixtures/nhl_player_impact/README.md` |
| `cfb_prediction/README.md` | `sdv-py/tests/fixtures/cfb_prediction/README.md` |
| `ncaa-crosswalk-test.py` | `sdv-py/tests/mbb/test_ncaa_espn_team_crosswalk.py` |
| `player-value-oracle.py` | `sdv-py/tests/mbb/test_mbb_player_value_oracle.py` |

`data-sources.md` §4 in this same skill already catalogs the oracle
fixtures and several of their gate values — this file is about *how* gates
work, not a second copy of that catalog; cross-reference it rather than
re-deriving numbers it already states.

---

## 1. Metric selection by model type

`reviewer.md` §3 (`metric-fit` lens) is the authoritative statement:
probabilities get Brier and/or log-loss **plus** a calibration table (a good
Brier score can hide miscalibration); point predictions (spread/total) get
MAE vs the closing market line with the sign convention handled explicitly;
ratings get Spearman rank correlation plus MAE vs the external oracle;
simulators get retrospective calibration (advancement at ~predicted rates,
slope band) with seeded RNG. Flag a metric that doesn't match the model's
output type — RMSE alone on a probability column, or no calibration check on
anything that outputs a probability (`reviewer.md` §3).

The shared implementation every per-sport `*_prediction_constants` /
`*_projection_constants` module re-exports lives in exactly one place —
`metrics.py` — six functions: `brier_score(y_true, p_pred)`,
`log_loss_score(y_true, p_pred, eps=1e-15)`, `spearman_corr(a, b)`,
`mae(a, b)`, `calibration_table(y_true, p_pred, n_bins=10)` (returns a
`polars.DataFrame` with `bin_mid, mean_pred, mean_actual, n`), and
`as_of_ratings_split(results, cutoff_date)` — extracted because these six
were duplicated verbatim across every league before consolidation
(`metrics.py:1-8, 23-163`).

### Probabilities → Brier + calibration table

`brier_score` is mean squared error between predicted probability and the
binary outcome; `calibration_table` buckets predictions into `n_bins`
equal-width bins and reports `mean_pred` vs `mean_actual` per bin
(`metrics.py:23-40, 107-143`). A win-probability gate is not just a Brier
floor — `mbb-prediction-backtest.py` gates the win-prob **calibration
slope** on neutral courts to `0.9 <= slope <= 1.1`
(`mbb-prediction-backtest.py:185-202`), and the NBA in-game WP gate does the
same at `[0.85, 1.15]` (`sdv-py/tests/nba/test_nba_in_game_wp.py:120-124`) —
both are the calibration-table idea collapsed to one number via a
regression-slope statistic, not a replacement for the binned table.

### Spreads/totals → MAE vs the closing market line

`mae(a, b)` is the shared helper (`metrics.py:87-104`). Sign convention must
be handled explicitly, not assumed: `cfb_prediction/README.md` documents
`close_spread_home` as the sportsbook **home** spread (negative = home
favored), so the market-implied home margin is `-close_spread_home`, and
records the observed correlation `corr(predicted_margin, -close_spread_home)
= -0.95` as the check that the sign wasn't silently flipped
(`cfb_prediction/README.md:39-40`). `cfb-prediction-backtest.py` distinguishes
**agreement with the closing line** from **accuracy against actual
outcomes** as two different questions that must not be conflated — a
previous gate version reported "spread MAE 4.06" (agreement) while the real
error against actual margins was ~15, because the metric answered a
different question than its name implied (`cfb-prediction-backtest.py:1-22`).

### Ratings → Spearman + MAE vs the external oracle

`spearman_corr(a, b)` ranks both arrays via `scipy.stats.rankdata` then
correlates the ranks (`metrics.py:66-84`). `cfb-ratings-oracle.py` gates
opponent-adjusted net EPA against three published oracles by Spearman with
the floor set below the value observed at gate time (`adj_net` vs FPI:
floor `>= 0.90`, observed `0.928`, `cfb-ratings-oracle.py:30-35`). §6 below
covers why Spearman alone is not sufficient for a ratings gate.

### Simulators → retrospective calibration + seeded RNG

`cfb-season-odds-calibration.py` is the concrete instance: a season Monte
Carlo re-simulated on the full FBS slate, seeded (`seed=0`), asserting three
sim-*aggregation* properties distinct from the per-game predictor's own
Brier gate — win totals conserved (`mean(exp_wins) == mean(actual_wins)`),
win totals rank-calibrated (`spearman(exp_wins, actual) >= 0.90`), and the
elite teams' simulated playoff probability separates from the field median
(`cfb-season-odds-calibration.py:1-16`). The harness design's Oracle ④
(interval calibration) is the credible-interval analogue for player-rating
posteriors: empirical coverage at 50/80/90/95% against a held-out half,
returning `n/a` for point-estimate models rather than fabricating a number
(`harness-design.md` §4 Oracle ④, "for models with a `posterior` ... Plain
RAPM has no posterior → this oracle returns `n/a` for it").

---

## 2. The never-lower gate rule

Stated in `reviewer.md` §1: gate floors/ceilings must be **derived from
observed values** and documented in the test docstring with the observed
number, and the never-lower rule itself must be stated in the gate test's
docstring — a lowered floor without a documented re-derivation is
merge-blocking.

`cfb-ratings-oracle.py`'s module docstring states the rationale, not just
the rule: "Floors are set from the value observed at gate time and
documented here, per the binding 'never lower a gate to make it pass --
debug the model' rule: the fixture + engine are proven correct, so a floor
below the observed value guards against regression without inviting a
silently-degraded model" (`cfb-ratings-oracle.py:8-11`). This is the
mechanism, not just the slogan: the floor's job is regression detection,
which only works if it sits strictly below (never at, never above) the
value the current, trusted implementation actually produces.

`cfb-prediction-backtest.py` shows the pattern applied across five gates in
one file, each floor commented with its measured value:

```python
_MIN_GAMES = 500              # measured 557
_MARGIN_MAE_FLOOR = 14.65     # measured 13.32 (superseded constants: 14.49)
_BRIER_FLOOR = 0.2298         # measured 0.2090
_ACCURACY_FLOOR = 0.6089      # measured 0.6409
_SPREAD_AGREEMENT_FLOOR = 6.41  # measured 5.83 -- AGREEMENT, not accuracy
```

(`cfb-prediction-backtest.py:51-57`) — the comment records what moved,
so a future change can see exactly what the floor was set relative to.

**The rule cuts both ways — it also forbids *widening a passing band* to
match an observed defect.** `cfb-season-odds-calibration.py` documents a
case where the sim's win-total dispersion slope is observed at ~1.55
against a would-be target of ~1.0, root-caused to ridge-shrunk ratings
under-estimating team-quality magnitude (a Phase-1 property, not a Phase-4
sampler bug) — and states explicitly "widening a slope band to 1.55 would
only enshrine the shrinkage," leaving it an open follow-up instead of
loosening the gate (`cfb-season-odds-calibration.py:18-25`).

A gate that asserts on a trivially small comparison set passes vacuously —
`reviewer.md` §1 requires a minimum-size assert on the joined frame
(`assert j.height >= N`). Real instances: `assert joined.height >= 2000`
guarding an oracle join from silently collapsing (`player-value-oracle.py:80`)
and `assert rows.height > 300, f"{league} {season} looks truncated"` guarding
a per-season match-rate check from running on a truncated frame
(`ncaa-crosswalk-test.py:93`).

---

## 3. The as-of-date leakage boundary

`reviewer.md` §2 states the rule: every predictive backtest must rate event
G using only data strictly before G — an as-of split (`date < cutoff`,
never `<=`) — and a split helper existing is not enough; the backtest must
actually route through it.

The shared implementation is `as_of_ratings_split(results, cutoff_date)`:
`results.filter(pl.col("date") < cutoff_date)` — strict `<`, not `<=`
(`metrics.py:146-163`).

`cfb-prediction-backtest.py` shows what testing the *actual join* rather
than a proxy for it looks like — and names the failure mode explicitly. An
earlier gate version re-derived the same `through_week + 1` offset the join
uses and asserted it was `>= 2`, which is a property of the fixture, not of
the join: had the join itself been changed to use same-week or future
ratings, that earlier test would still have passed, because it never
touched a predicted row. The current test instead checks the snapshot each
*prediction* actually landed on, per side, and asserts the week-vs-snapshot
offset is exactly `[1]` for every row. Its own docstring names the general
failure mode: "Testing a proxy for the thing is how leakage survives a
green suite" (`cfb-prediction-backtest.py:100-118`).

Window/lag features must be grouped (`.over("game_id")` / per-season); an
ungrouped `shift`/`cum_sum` leaks across game boundaries when frames
concatenate, and `through_week`/`through_date`/`as_of` cutoff arguments
must be treated as EXCLUSIVE — a real production bug in this ecosystem was
`through_week` implemented as `<=` instead of `<`, leaking the target week
into training (`reviewer.md` §2). This file does not have a second,
independent instance of that specific bug to add beyond what `reviewer.md`
already records — an honest gap, not a re-derivation.

---

## 4. Oracle-join integrity

`reviewer.md` §7 states the two load-bearing checks: dtype agreement
asserted before every oracle/crosswalk join
(`left.schema[k] == right.schema[k]`, ids `Utf8` cast from the raw integer,
never from a float), and a documented, non-systematic match-rate floor on
inner joins against a name-crosswalked oracle.

**Dtype agreement is asserted inline at the join site, not just documented.**
Real instances in `sdv-py`'s CFB modules:

```python
assert games.schema["team_id"] == pl.Utf8
assert netted.schema["team_id"] == pl.Utf8
```
(`sdv-py/sportsdataverse/cfb/cfb_ratings.py:297-298`)

```python
assert talent.schema["team_id"] == returning.schema["team_id"] == pl.Utf8
```
(`sdv-py/sportsdataverse/cfb/cfb_recruiting_projection.py:139`)

```python
assert prod_prev.schema["player_id"] == roster_curr.schema["player_id"] == pl.Utf8
```
(`sdv-py/sportsdataverse/cfb/cfb_returning_production.py:138`)

Also asserted at the oracle-test level, joining the ratings engine's output
directly against a fixture: `assert e.schema["team_id"] == _FPI.schema["team_id"]
== pl.Utf8` before computing the Spearman gate (`cfb-ratings-oracle.py:33`).
`data-sources.md` §4's opening paragraph documents the ecosystem-wide
version of this bug class in concrete numbers: the NHL MoneyPuck/
EvolvingHockey fixtures are `Int64`-keyed while the ESPN-derived
basketball/football fixtures are `Utf8` — joining one straight into the
other is exactly the silent-zero-match dtype bug.

**Match-rate floors are documented numbers, not vibes**, and a floor test
enforces them the same way a gate test enforces a metric floor:

```python
RECENT_FLOOR = 0.97
OVERALL_FLOOR = 0.95
...
rate = rows.filter(pl.col("espn_team_id").is_not_null()).height / rows.height
assert rate >= RECENT_FLOOR, f"{league} {season} match rate {rate:.3%} < {RECENT_FLOOR:.0%}"
```
(`ncaa-crosswalk-test.py:24-25, 94-95`)

Fixture-README-documented match rates (verify against `data-sources.md` §4
rather than re-deriving): Torvik ratings 350/362 teams (96.7%) matched to an
ESPN `team_id`, with the 12 unmatched named as one-off small-school naming
irregularities rather than a systematic class
(`mbb_prediction/README.md:36-42`); MoneyPuck per-shot xGoal 265/273 shots
(97%) matched by `(game_id, shooter_id, game_seconds)`
(`nhl_player_impact/README.md:76`). `reviewer.md` §7's structural point —
verify the *dropped* entities are one-off irregulars, not a systematic
class (e.g. dropping every "St." school would bias a rating gate) — is
exactly what the Torvik README's unmatched list demonstrates satisfying.

**A small n changes what a Spearman value means, and the fixture README
must say so.** `nhl_player_impact/README.md` gates three concurrent-validity
checks against EvolvingHockey/MoneyPuck at three different evidentiary
weights from the same n=6/n=72 samples: GSAx vs MoneyPuck Spearman `0.771`
(n=6 goalies) gated at floor `0.65` is labeled "a small-sample **sanity**
check ... not a powered validity certification"; skater RAPM vs EH EV
Spearman `0.406` (n=72) gated at floor `0.30` is labeled "a powered
magnitude gate" because n=72 clears the Spearman significance threshold;
WAR vs EH WAR Spearman `0.132` (n=72) is *inside* the noise band at that n
(below the ~0.23 two-sided significance threshold), so its gate is a
directional sign check (`corr > 0`) rather than a magnitude floor
(`nhl_player_impact/README.md:112-122`). The lesson for any new oracle-join
gate: state whether n clears the correlation's own significance threshold
before treating the observed value as a magnitude floor.

---

## 5. What a fixture provenance README must contain

`reviewer.md` §7: every fixture directory the tests read must have a
provenance README (source, capture date, row counts, id dtypes, known
gaps); a missing README is an IMPORTANT finding, and gate tests must be
runnable offline against committed fixtures with live variants gated
behind the repo's live-test env flag.

Three committed READMEs satisfy this in practice and are the pattern to
follow for a new one:

- **Source + capture date + regeneration command up front.**
  `mbb_prediction/README.md` opens with "Captured **2026-07-07** for the
  **2024** season ... Regenerate with `uv run python
  dev/mbb_prediction/capture_oracle.py`" before any table
  (`mbb_prediction/README.md:11-17`).
- **ID convention stated once, not per-file.** "every team / game id is
  `Utf8` (cast from the raw ESPN integer via
  `pl.col(id).cast(pl.Int64).cast(pl.Utf8)`)" (`mbb_prediction/README.md:19-21`).
- **A per-file table: rows, source wrapper/URL, and notes** — every fixture
  in `nhl_player_impact/README.md`'s Contents table carries `Rows` and a
  `Notes` column stating exact dtypes per column
  (`nhl_player_impact/README.md:20-28`).
- **Known gaps named, not hidden.** `cfb_prediction/README.md` documents
  that three `close_total` values are `null` and are `drop_nulls`'d by the
  MAE gate, and that the predictor/odds sample is a down-selection of only
  the completed games ESPN published a line for
  (`cfb_prediction/README.md:32-37`); `mbb_prediction/README.md` documents
  that `adj_tempo` is null because the tempo-bearing barttorvik endpoint is
  bot-blocked, and states explicitly that no gate depends on that column
  (`mbb_prediction/README.md:50-54`).
- **Auth/paywall provenance for external oracles**, when applicable:
  `nhl_player_impact/README.md` documents the EvolvingHockey capture needs
  `EVOLVING_HOCKEY_USER`/`EVOLVING_HOCKEY_PASS` read from `~/.Renviron` at
  call time, never hardcoded or committed (`nhl_player_impact/README.md:79-82`).
- **A "sanity anchors" section** — a handful of real, human-checkable
  values asserted directly in the oracle tests, e.g. "SP+ (`sp_overall`):
  Michigan 31.3 (#1), Georgia 31.2 (#2)" — catches a gross join/sign
  regression that a correlation-only gate could miss
  (`cfb_prediction/README.md:52-56`).

---

## 6. The trap: Spearman is scale-blind

A ratings gate that only checks rank correlation can pass a model whose
*scale* is wrong, because Spearman is invariant to any monotone
transformation of one side — reordering never changes the rank correlation,
even if the reordered values are off by a constant factor.

This is not a hypothetical — it happened in this ecosystem's CFB ratings
work and shipped before being caught. From the session notes: "User flagged
adj_net magnitudes (0.63 top) vs expected <0.46 → diagnosed: published stat
was ridge coefficient+intercept (competitive-only), NOT the R adjust_epa
netted average (gameonpaper 2024 max 0.366). **Spearman gates are
scale-blind → shipped unseen.**" (`cfb-ratings-parity-ship.md:44-47`). The
Spearman-only ratings gate (§1 above, `cfb-ratings-oracle.py`) had been
green the entire time the magnitude was wrong, because reordering the wrong
scale onto the right rank order doesn't move the rank correlation at all.

The fix that followed in the same session was a **magnitude gate** added
alongside the existing rank gate, plus a full rescale (netted `adj_*`
values, refit constants) — not a Spearman-floor change
(`cfb-ratings-parity-ship.md:53-55`, "netted adj_*, true-EPA ST, refit
constants ... magnitude gate"). The general rule this instance backs:
**a ratings gate needs a scale check (MAE/RMSE vs the oracle, or a
magnitude-band assert) in addition to Spearman — never Spearman alone**,
which is exactly what `reviewer.md` §3 already states ("Ratings → rank
correlation (Spearman) + MAE vs the external oracle").

---

## 7. Honest gaps

- **This file does not have a second, independently-sourced instance of
  the `through_week`-as-inclusive-leak bug** beyond the one `reviewer.md`
  §2 already records in its failure table; the CFB backtest gate's own
  `through_week` handling (§3 above) is a different mechanism (a published
  weekly-snapshot offset, verified empirically to be a strict one-week-prior
  join) and is cited there as a positive instance of testing the actual
  join, not as a second occurrence of the bug.
- **Neither `harness-design.md` nor `harness-plan.md` scores probabilities
  with Brier/log-loss at all** — the NBA validation harness is entirely
  regression-shaped (game-margin RMSE/correlation, split-half reliability,
  cross-season rating correlation, interval coverage), because RAPM-family
  models predict points, not win probability. The Brier/calibration-table
  grounding in §1 above comes from the CFB/MBB/NBA win-probability gates
  instead, not from the harness sources named in this task's brief.
