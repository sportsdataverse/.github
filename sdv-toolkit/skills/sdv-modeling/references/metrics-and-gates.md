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
Brier score can hide miscalibration), with **in-game WP specifically
requiring per-time-bucket calibration**; point predictions (spread/total)
get MAE vs the closing market line with the sign convention handled
explicitly; ratings get Spearman rank correlation plus MAE vs the external
oracle; simulators get retrospective calibration (advancement at
~predicted rates, slope band) with seeded RNG. Flag a metric that doesn't
match the model's output type — RMSE alone on a probability column, or no
calibration check on anything that outputs a probability (`reviewer.md`
§3, "in-game WP → per-time-bucket calibration").

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
regression-slope statistic, not a replacement for the binned table. Neither
exemplar is the agent's **per-time-bucket** in-game-WP calibration above:
both bin on predicted-*probability*, not on time/clock-bucket, so treat
them as calibration-slope instances, not as evidence the per-time-bucket
rule is already satisfied.


#### Brier alone hides which half is broken

A Brier score is a sum of three terms (Murphy 1973), and reporting only the
scalar throws away the part that says *what to fix*:

```
Brier = reliability - resolution + uncertainty
        (lower better) (higher better) (fixed by the data)
```

- **Reliability** — are predicted 0.7s actually 70% winners? This is what
  recalibration fixes, cheaply, without retraining.
- **Resolution** — does the model separate outcomes at all, or does it predict
  the base rate every time? A model that always answers "0.52" has *perfect*
  reliability and zero resolution, and its Brier looks respectable.
- **Uncertainty** — the base rate's own variance. Not a property of the model,
  so it must not move between a champion and a challenger evaluated on the same
  holdout; if it does, the holdouts differ and the comparison is invalid.

The failure this catches: a WP model that degrades to near-base-rate still
posts a passable Brier, and a Brier-only gate lets it through. Gate reliability
and resolution separately, or gate Brier *and* a separation statistic.

#### Expected calibration error — the scalar to pair with the table

The calibration table (`metrics.py:107-143`) is the honest artifact; ECE is its
one-number summary, useful as a gate threshold where a table cannot be:

```python
import numpy as np


def expected_calibration_error(y_true, y_prob, n_bins=10, strategy="quantile"):
    """Weighted mean |accuracy - confidence| across probability bins.

    Args:
        y_true: Binary outcomes, 0/1.
        y_prob: Predicted probability of the positive class.
        n_bins: Number of bins.
        strategy: "quantile" for equal-count bins (default -- equal-WIDTH bins
            leave the extreme bins nearly empty on a WP model, where most mass
            sits near 0 and 1, and a bin of 3 plays dominates the average),
            or "uniform" for equal-width.

    Returns:
        ECE in probability units, comparable across models on the same holdout.
    """
    y_true, y_prob = np.asarray(y_true), np.asarray(y_prob)
    if strategy == "quantile":
        edges = np.quantile(y_prob, np.linspace(0, 1, n_bins + 1))
        edges = np.unique(edges)
    else:
        edges = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(y_prob, edges[1:-1]), 0, len(edges) - 2)
    ece = 0.0
    for b in range(len(edges) - 1):
        m = idx == b
        if not m.any():
            continue
        ece += m.mean() * abs(y_true[m].mean() - y_prob[m].mean())
    return float(ece)
```

**Use quantile bins.** Equal-width binning on an in-game WP model puts almost
every play in the first and last bin and computes the middle eight from a
handful of rows — the resulting ECE is dominated by noise and moves between
runs on the same model.

**Report ECE next to the table, never instead of it.** ECE is a mean of
absolute deviations, so a model that is 10 points over-confident at the top and
10 points under-confident at the bottom scores the same as one that is
uniformly 10 points off — and only the table shows which.

**ECE reads 0.000 for a model that predicts the base rate every play.** Measured
on the function above: 20,000 rows, a constant 0.5 prediction against a 50%
base rate, quantile binning — `ECE = 0.0000`, a perfect score for a model with
no resolution whatsoever. Quantile edges on a near-constant predictor collapse
to a single bin, and one bin is trivially well-calibrated. This is the same hole
as the Brier decomposition above, and it is why **ECE can never be the only
probability gate**. Pair it with a resolution or separation statistic (AUC, the
calibration-table row count actually populated, or the variance of the
predictions), and assert that the bin count did not degenerate:

```python
assert len(np.unique(np.quantile(y_prob, np.linspace(0, 1, n_bins + 1)))) > 3, (
    "predictions too concentrated to bin -- ECE is meaningless here"
)
```

#### Multiclass targets — EP is seven classes, not one

Every calibration note above is binary-framed, but `ep_model` emits a 7-class
softprob vector (TD, FG, safety, and the defensive mirrors, plus no-score) and
`ep` is the dot product of that vector with `_EP_POINT_VALUES`
(`sdv-py/sportsdataverse/nfl/model_vars.py`). Two consequences:

- **Score the vector, not just the derived scalar.** A multiclass Brier
  (`sum over classes of (p_k - y_k)^2`, averaged) or the multinomial log loss
  catches a model whose class *mix* is wrong in a way that cancels in the
  point-value dot product. Two probability vectors with very different shapes
  can produce the same `ep`.
- **Calibrate per class, one-vs-rest.** A single reliability curve on `ep`
  cannot tell you that the safety class is systematically over-predicted; a
  per-class curve can, and safety is exactly the low-frequency class where a
  boosted model drifts.

Gate the scalar `ep` against the oracle **and** the class mix against the
empirical class frequencies on the holdout. The oracle correlation for `ep`
is 0.996 (`sdv-py/CLAUDE.md`, NFL section) and that number is compatible with
a materially wrong class mix.

#### Intervals — conformal prediction for ratings and projections

Ratings, projections, and pregame margins publish as point estimates with no
interval anywhere in the ecosystem. Split conformal is the cheapest honest fix:
it is distribution-free, wraps any fitted estimator, and needs only a held-out
calibration split.

```python
import numpy as np


def split_conformal_interval(residuals_cal, alpha=0.1):
    """Half-width of a (1 - alpha) prediction interval from calibration residuals.

    Args:
        residuals_cal: |y - yhat| on a calibration split the model never saw.
            For a season model this MUST be a later-season split, not a random
            one -- a random split reuses carried state and reports an interval
            that is too narrow.
        alpha: Miscoverage rate; 0.1 gives a 90% interval.

    Returns:
        The half-width q. The interval is yhat +/- q, with finite-sample
        coverage at least 1 - alpha under exchangeability.
    """
    n = len(residuals_cal)
    # The (1-alpha)(n+1)/n quantile, not the (1-alpha) quantile -- the finite-
    # sample correction is what makes the coverage guarantee hold at small n,
    # and a season's worth of teams IS small n.
    q_level = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(residuals_cal, q_level, method="higher"))
```

**The exchangeability caveat is the whole game for us.** Conformal guarantees
coverage when calibration and test points are exchangeable. Across a season
they are not — teams improve, rosters turn over, the rule set changes. Use a
*late-season* calibration split and validate coverage on the following season
before quoting the interval; if realized coverage on a held-out season is far
below `1 - alpha`, the non-exchangeability is real and the interval is
decoration. `mapie` implements this and its cross-conformal variants against
the sklearn API if you want more than the split method above.


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
posteriors: form credible intervals per player rating and measure empirical
coverage at 50/80/90/95% (a calibration curve), returning `n/a` for
point-estimate models rather than fabricating a number (`harness-design.md`
§4 Oracle ④, "for models with a `posterior` ... Plain RAPM has no posterior
→ this oracle returns `n/a` for it"). The design leaves the exact holdout
mechanism unspecified at Oracle ④ itself — "held-out half" is Oracle ②'s
(split-half reliability) construction, not Oracle ④'s; don't conflate them
(`harness-design.md` §4 Oracle ②, "Randomly halve the season's games ... ";
Oracle ④, "For models with a `posterior`, form credible intervals per
player rating and measure empirical coverage").

---


#### Simulator hygiene — three cheap things we do none of

**Common random numbers.** Two scenarios compared with independent RNG streams
differ by sampling noise as well as by the change you made. Seed each scenario
identically so the *same* random draws drive both, and the difference is the
effect. Nearly free, and it is what makes "playoff odds moved 3 points" a claim
rather than a coincidence.

```python
base = simulate(season, rng=np.random.default_rng(20260828))
alt  = simulate(season_with_injury, rng=np.random.default_rng(20260828))  # SAME seed
```

**Antithetic variates.** Pair each draw `u` with `1-u`. Halves the variance of a
mean for the same number of simulations on any monotone response, which a
playoff-odds sum is.

**CRPS, not just calibration slope.** A calibration slope says the probabilities
are honest; it says nothing about whether the *shape* of the simulated
distribution is right. CRPS is the proper scoring rule for a full predictive
distribution and reduces to MAE for a point forecast. Verified: a correct
ensemble scored 0.5804, the same ensemble shifted by 1.0 scored 0.8055.

```python
import properscoring as ps
ps.crps_ensemble(observed, draws)      # (n,) observed vs (n, m) simulated
```

Full treatment of distributional targets and their scoring:
`count-survival-ordinal.md`.

---

## 1b. Choosing the evaluation itself

Merged from the retired `sdv-evaluating-ml-models` skill on 2026-08-28 and
rewritten against this ecosystem's shapes. The generic advice ("use
`cross_val_score`, tune with Optuna, log to MLflow") is correct and mostly
irrelevant here, because our constraint is never the tuner — it is that the
rows are not exchangeable and the ground truth is an external oracle.

### Pick the splitter from the feature memory, not from habit

| model shape | splitter | why |
|---|---|---|
| within-play, memoryless (EP, CP, xG on same-snap state) | `GroupKFold(groups=game_id)` | rows correlate within a game, nothing carries across games |
| in-game WP | `GroupKFold(groups=game_id)` | same, but gate calibration per time bucket, not just overall |
| pregame WP, ratings, projections | **purged + embargoed** time split | features carry season-to-date state; see `sklearn-xgboost.md` §A2 |
| anything reported per season | `TimeSeriesSplit` on season, or leave-one-season-out | a season is the unit a consumer trusts |
| player-level impact (RAPM, EPM shape) | leave-one-season-out | within-season folds share the same stint design |

The single question that picks the row: **does any feature look backwards past
the current game?** If yes, `GroupKFold` is not enough.

### Hyperparameter search: bound it by the gate, not by the budget

Tune on a validation split; report on a holdout the tuner never saw; gate on
the oracle. Three rules that are specific to us:

- **The oracle is not a validation set.** Tuning against the Torvik/FPI/market
  comparison until the correlation clears the floor is fitting the gate. The
  oracle is the acceptance test, used once per candidate.
- **A tuning run that improves the metric by less than its own fold-to-fold
  spread has found nothing.** Report the spread alongside the point estimate,
  or a re-run with a different seed will "beat" the champion.
- **Search the feature set before the hyperparameters.** CFB pregame went
  15.14 → 12.97 MAE against a 12.27 market ceiling, and the finding was that
  60 features beat 244 — the substrate is roughly one-dimensional
  (`prior-art.md`, CFB higher-order models). No hyperparameter search recovers
  that.

### Error analysis by segment is where the real defects surface

An aggregate metric is the last place a sports-model bug shows up, because the
bug usually lives in a stratum. Slice every candidate at least by: season, week
(early vs late), conference or division tier, home/away/neutral, favorite vs
underdog, and score-margin bucket. Real examples this would have caught faster:

- Special-teams EPA overstated 18x, invisible in the pooled number
  (`prior-art.md`, CFB).
- A WBB quarters model silently emptying six pre-2016 seasons that are played
  in halves — 0 rows read as "no data", not as an error
  (`failure-modes.md`).
- Pre-2005 WNBA team logs that were garbage in aggregate but fine per player.

### Experiment tracking: our stack is not MLflow

The retired `sdv-ml-pipeline` skill's MLflow/Kubeflow/Feast templates do not
map onto this ecosystem and were dropped rather than carried over. The
equivalents here:

| generic MLOps concept | what we actually use |
|---|---|
| experiment tracking | `models/ledger.jsonl` -> `models/LEDGER.md`, one row per stage run |
| model registry | `models/REGISTRY.md` in the owning `-data` repo |
| artifact store | the release tag on `sportsdataverse/sportsdataverse-data` |
| run reproducibility | stage fingerprints (code subtree + input digests + feature set + hparams) |
| deployment | the loader in `sdv-py` that reads the published parquet |

All five are specified in `sdv-data-pipeline` ("Models are pipelines too").
Reach for that skill for the operational half; this file covers only whether
the model is *correct*.


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
than a proxy for it looks like — and names the failure mode explicitly. Its
docstring states why the `+1` offset exists at all: "`through_week == W`
INCLUDES week W, so joining a week-W game to the W snapshot would let it
see its own result" (`cfb-prediction-backtest.py:103-104`) — treating
`through_week` as inclusive of its own boundary, exactly the failure
`reviewer.md` §2 names, is precisely why the join must offset by one week
rather than join same-week. An earlier gate version re-derived the same
`through_week + 1` offset the join uses and asserted it was `>= 2`, which is
a property of the fixture, not of the join: had the join itself been
changed to use same-week or future ratings, that earlier test would still
have passed, because it never touched a predicted row. The current test
instead checks the snapshot each *prediction* actually landed on, per side,
and asserts the week-vs-snapshot offset is exactly `[1]` for every row. Its
own docstring names the general failure mode: "Testing a proxy for the
thing is how leakage survives a green suite"
(`cfb-prediction-backtest.py:100-118`).

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
**rescaling** of one side — multiplying, shifting, or otherwise stretching
the values along a monotone curve never changes the rank correlation, even
if the rescaled values are off by a large constant factor. (Reordering the
values is the one operation that *would* move Spearman — a rescale, by
definition, does not reorder anything.)

This is not a hypothetical — it happened in this ecosystem's CFB ratings
work and shipped before being caught. From the session notes: "User flagged
adj_net magnitudes (0.63 top) vs expected <0.46 → diagnosed: published stat
was ridge coefficient+intercept (competitive-only), NOT the R adjust_epa
netted average (gameonpaper 2024 max 0.366). Spearman gates are
scale-blind → shipped unseen." (`cfb-ratings-parity-ship.md:45-47`). The
Spearman-only ratings gate (§1 above, `cfb-ratings-oracle.py`) had been
green the entire time the magnitude was wrong, because rescaling the wrong
magnitude onto the right rank order doesn't move the rank correlation at all.

The fix that followed in the same session was a **magnitude gate** added
alongside the existing rank gate, plus a full rescale (netted `adj_*`
values, refit constants) — not a Spearman-floor change. The same cited fix
also **re-derived two existing floors downward** (SP+ off 0.82, exp-wins
0.885) and raised one, "all in-test documented"
(`cfb-ratings-parity-ship.md:53-55`, "netted adj_*, true-EPA ST, refit
constants ... magnitude gate ... 2 floors re-derived down ... + 1 raised —
all in-test documented") — exactly the re-derivation-after-a-rescale case §2
licenses: a floor can move when the underlying quantity's *definition*
changes, as long as the new floor is documented against a newly-observed
value, not loosened to paper over a regression in the old definition. The
general rule this instance backs: **a ratings gate needs a scale check
(MAE/RMSE vs the oracle, or a magnitude-band assert) in addition to
Spearman — never Spearman alone**, which is exactly what `reviewer.md` §3
already states ("Ratings → rank correlation (Spearman) + MAE vs the
external oracle").

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
