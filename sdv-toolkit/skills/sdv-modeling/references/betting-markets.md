# Betting markets — as oracle, as feature, and as the thing to beat

> Reference file of the `sdv-modeling` skill. Covers modeling **against or with
> betting markets**: turning prices into probabilities, the market as a baseline
> and a leakage source, closing-line value as the evaluation gate, and staking.
> The spread/total accuracy gate and the agreement-vs-accuracy distinction live in
> `metrics-and-gates.md` §"Spreads/totals → MAE vs the closing market line" and are
> not repeated here.

The closing line is the strongest public baseline in sports prediction. It is a
consensus of informed money that has already absorbed injuries, weather, lineups
and every public model — including yours. That makes it three different things
depending on how it is used, and confusing them is the root of most betting-model
failures:

| Role | Question | Leakage risk |
|---|---|---|
| **Oracle / baseline** | Does my model beat the market's own probability? | none, if compared on identical games |
| **Feature** | Does the market price improve my prediction? | **high** — the close carries information from after most features were fixed |
| **Target of a betting strategy** | Do my bets beat the price I could actually get? | the price available *at bet time* must be the one used |

Every entry: **the trap · why it never errors · the detection test · a real
citation** where this ecosystem has one.

**Contents**

1. Prices to probabilities — removing the vig
2. The market is a baseline you must beat on identical games
3. Time — which line existed when
4. Placeholder odds masquerading as market data
5. Closing-line value — the gate for a betting model
6. Staking — Kelly, and why a miscalibrated model must bet less
7. Backtest hygiene
8. Data sources and skills

---

## 1. Prices to probabilities — removing the vig

A book's implied probabilities sum to more than 1; the excess (the overround) is
its margin. Raw implied probabilities are **biased upward** and cannot be compared
to a model's probabilities until the margin is removed.

**Trap.** Using `1 / decimal_odds` directly as "the market probability".

**Why invisible.** The values are in [0, 1] and correlate perfectly with the right
answer; they are just all too high, and a model that "beats" them may only be
beating the vig.

Four removal methods, in rising sophistication. **Multiplicative** is fine for
two-way markets with a small margin; **Shin** models the favourite–longshot bias
and is preferred for multi-outcome markets (futures, props) where the margin is
not spread evenly.

```python
import numpy as np
from scipy.optimize import brentq

def implied(decimal_odds):
    return 1.0 / np.asarray(decimal_odds, float)

def devig_multiplicative(decimal_odds):
    q = implied(decimal_odds)
    return q / q.sum()

def devig_additive(decimal_odds):
    q = implied(decimal_odds)
    return q - (q.sum() - 1.0) / len(q)       # can go negative on long shots

def devig_power(decimal_odds):
    q = implied(decimal_odds)
    k = brentq(lambda k: (q ** k).sum() - 1.0, 1.0, 50.0)
    return q ** k

def devig_shin(decimal_odds):
    """Shin (1993): margin attributed to insider trading, which inflates longshots."""
    q = implied(decimal_odds)
    s = q.sum()
    def probs(z):
        return (np.sqrt(z ** 2 + 4 * (1 - z) * q ** 2 / s) - z) / (2 * (1 - z))
    z = brentq(lambda z: probs(z).sum() - 1.0, 0.0, 0.999)
    return probs(z)
```

**Detection test — every method must return a probability distribution that
preserves the book's ordering.**

```python
def assert_devig_valid(fn, decimal_odds, tol=1e-9):
    p = fn(decimal_odds)
    assert abs(p.sum() - 1.0) < tol, f"{fn.__name__}: sums to {p.sum():.6f}"
    assert (p >= 0).all(), f"{fn.__name__}: negative probability {p.min():.4f}"
    order = np.argsort(np.asarray(decimal_odds, float))
    assert (np.diff(p[order]) <= tol).all(), f"{fn.__name__}: reordered the outcomes"
    return p
```

`devig_additive` is included because it is common, and it **fails this test
whenever a longshot's implied probability is below `overround / n`**, producing
negative probabilities. That condition is rare in two- and three-way markets and
routine in large-field futures: measured on a 30-team futures board with a 15.4%
overround, it returned **7 negative probabilities**; on a 6-way market with an
11.2% overround, none. Prefer the other three.

**American odds.** Convert first: `+150 → 2.50`, `-150 → 1.6667`
(`d = 1 + a/100` if `a > 0`, else `1 + 100/|a|`). Spreads and totals are priced
near −110/−110 (`1.909`), so both sides' implied probabilities sum to ~1.048.

---

## 2. The market is a baseline you must beat on identical games

**Trap.** Reporting a model's Brier score or log loss in isolation, or comparing
it to the market on a different set of games (the market is missing for some
games, so the comparison drops them for one side only).

**Why invisible.** Both numbers are real; they are just not measuring the same
population. Games without a posted line skew toward low-profile matchups and
different base rates.

**Rule.** Restrict both to the **identical** games with a valid pre-event market
price, de-vig the market (§1), and compare with a paired, game-clustered test.

**Real citation.** The win-expectancy bake-off (sdv-py, 2026-08-07) did exactly
this on a like-for-like slice: CFB champion **0.1701 Brier vs market 0.1639** on
the identical **9,456 games** (gap 0.0062); NFL **0.2200 vs 0.2128** (gap 0.0072).
Both champions landed within the 0.01 band — **close to the market, not better
than it**, which is the typical honest outcome for a public-data model. CFB pregame
margin tells the same story in MAE: 15.14 → 12.97 against a **12.27** market
ceiling (`metrics-and-gates.md`).

**What beating the market requires.** Information or speed the market lacks — an
injury priced late, a rule or weather effect underweighted, a thin market (lower
divisions, props, women's sports) — not a better generic learner on the same
public inputs.

---

## 3. Time — which line existed when

**Trap.** Using the **closing** line as a feature, or as the price a strategy
"bets at", when the prediction or bet happens earlier.

**Why invisible.** The close is the most accurate line precisely because it
absorbed everything up to kickoff — including the late injury news your features
do not have. Features that include it inherit that future information; strategies
that bet at it assume a price nobody could have taken.

**Rule.** Every price carries a **timestamp**, and each use states its as-of
time:

| Use | Price to use |
|---|---|
| Pre-game model evaluated at a fixed lead time | the line **as of that time** |
| A betting strategy's execution price | the line **available when the bet is placed** |
| The evaluation benchmark for that strategy | the **closing** line (§5) |
| Explaining variance after the fact | the close is fine |

**Detection test — no price observed after the decision time.**

```python
import polars as pl

def assert_prices_as_of(features, prices, key="game_id",
                        decision_col="decision_ts", price_col="price_ts"):
    """Every price joined into features must be timestamped before the decision.

    A null timestamp makes the comparison null, and a filter drops null rows --
    so an unstamped price would pass silently. Require both stamps first.
    """
    j = features.join(prices, on=key, how="inner")
    unstamped = j.filter(pl.col(price_col).is_null() | pl.col(decision_col).is_null())
    assert unstamped.height == 0, (
        f"{unstamped.height} joined rows lack a price or decision timestamp: "
        "their timing cannot be verified"
    )
    late = j.filter(pl.col(price_col) > pl.col(decision_col))
    assert late.height == 0, (
        f"{late.height} rows use a price observed after the decision time — "
        "the closing line is leaking into a pre-decision feature"
    )
```

---

## 4. Placeholder odds masquerading as market data

**Trap.** A pipeline that cannot find a line fills a **default** and carries on. The
default looks like a real price.

**Why invisible.** The column is fully populated, finite and in range.

**Real citation — this ecosystem has shipped this.** sdv-py's CFB odds resolution
cascades from the game summary's `pickcenter` to the live odds API and, on failure,
**defaults to spread 2.5, total 55.5, home favoured** (`CLAUDE.md`, "CFB — offline
reprocess"). ESPN's `pickcenter` is empty for 2024+ games, so the fallback is not
rare. The provenance is recorded in `odds_source` —
`summary_pickcenter` | `core_odds_api` | `default` | `injected` — **and a model must
filter on it**. The model-writeup improvements program (2026-09-01) found CFB
2004–05 carrying default spreads in published data.

**Detection test — a price that repeats far too often is a placeholder.**

```python
def assert_no_placeholder_prices(df, cols=("spread", "total"), max_share=0.05,
                                 provenance_col="odds_source"):
    if provenance_col in df.columns:
        n_default = df.filter(pl.col(provenance_col) == "default").height
        assert n_default == 0, f"{n_default} rows carry default (not market) odds"
    for c in cols:
        if c not in df.columns:
            continue
        top = df.group_by(c).len().sort("len", descending=True).row(0)
        share = top[1] / df.height
        assert share <= max_share, (
            f"{c}={top[0]} appears on {share:.1%} of rows: likely a placeholder"
        )
```

A real market's most common spread rarely covers more than a few percent of
games; a default fills a large block of one value.

---

## 5. Closing-line value — the gate for a betting model

**Trap.** Judging a strategy on win rate or ROI over a few hundred bets.

**Why invisible.** Returns are dominated by variance at that sample size. A
−110 bettor needs a 52.4% win rate to break even; the standard error of a win rate
over 500 bets is about 2.2 percentage points, so a genuinely +2% edge and a −2%
edge are routinely indistinguishable.

**The gate.** **Closing-line value (CLV)**: did you get a better price than the
close? Because the close is efficient, consistently beating it is the strongest
observable evidence of an edge, and it accrues signal on every bet, independent
of the result.

```python
def clv(bet_decimal_odds, close_decimal_odds_same_side, close_decimal_odds_other_side):
    """Expected value of the bet priced against the NO-VIG closing probability.

    > 0 means the bet was placed at a better price than the market's final
    fair estimate. Average over many bets; report the mean and its SE.
    """
    p_fair = devig_multiplicative([close_decimal_odds_same_side,
                                   close_decimal_odds_other_side])[0]
    return p_fair * bet_decimal_odds - 1.0
```

Report mean CLV with a standard error clustered by date (bets on the same slate
share information), alongside realized ROI — never ROI alone.

---

## 6. Staking — Kelly, and why a miscalibrated model must bet less

The Kelly fraction maximizes long-run log growth **if the probability is right**:

```python
def kelly_fraction(p, decimal_odds):
    """Fraction of bankroll to stake. 0 when there is no edge."""
    b = decimal_odds - 1.0
    return max(0.0, (p * decimal_odds - 1.0) / b)
```

**Trap.** Full Kelly with an overconfident model.

**Why invisible.** Kelly's sizing is proportional to the edge, so an inflated
probability inflates the stake exactly on the bets most likely to be wrong. Growth
looks strong until the drawdown.

**Rules.**
- **Bet fractional Kelly** (a quarter to a half). The asymmetry is severe:
  under-betting costs a little growth, over-betting destroys it. Simulated with
  `kelly_growth` below — a model that says 58% on even-money bets whose true rate
  is 53% (5 points overconfident) — log growth per bet, median across 40 simulated
  paths, was **+0.0015** at
  quarter Kelly, **+0.0014** at half, **−0.0036 at full Kelly**, and **−0.035 at
  double**. The overconfidence is enough to turn *full* Kelly negative.
- **Calibrate first** (`metrics-and-gates.md`). Kelly consumes a probability, so
  its correctness depends entirely on calibration, not on AUC.
- **Size from the no-vig edge**, not the raw implied price.
- **Correlated bets** (same game, same slate, parlays) are not independent; sizing
  them as if they were compounds the over-bet.

**Detection test — does the staking survive the model's own miscalibration?**
Simulate growth with the true probability deliberately worse than the model's.

```python
def kelly_growth(p_true, p_model, decimal_odds, fraction, n_bets=2000, seed=0):
    """Mean log-bankroll growth per bet along ONE simulated path, betting on a
    model that may be wrong. Take the median over seeds for a stable estimate
    (the figures above are the median of 40 paths of 4,000 bets)."""
    rng = np.random.default_rng(seed)
    f = fraction * kelly_fraction(p_model, decimal_odds)
    wins = rng.random(n_bets) < p_true
    log_g = np.where(wins, np.log1p(f * (decimal_odds - 1.0)), np.log1p(-f))
    return float(log_g.mean())
```

---

## 7. Backtest hygiene

- **Use the price you could have taken** (§3), including the vig, and respect the
  book's limits.
- **Line shopping inflates backtests.** Taking the best price across many books at
  every moment is not reproducible by one account; state which books and when.
- **Survivorship.** Markets and books that disappear, and games whose lines were
  pulled, drop out of historical data non-randomly.
- **Evaluate on a later season** (`competition.md` §2) and report CLV, not just ROI.
- **Account for correlation.** Clustering by date or slate for standard errors.
- **Props and thin markets** are where edges exist and where closing data is
  sparsest; say how CLV was measured when no reliable close exists.

---

## 8. Data sources and skills

| Source | What it gives |
|---|---|
| `odds-data` (private, sportsdataverse) | historical The Odds API captures, 7 sports 2020–2026, 96.4% crosswalked to ESPN game ids |
| `oddsapiR` (CRAN) | R client for The Odds API |
| sdv-py CFB odds + `odds_source` | ESPN-derived spreads/totals with provenance (filter `default`, §4) |
| `data-sources.md` | per-league market closing-line fixtures and their differing schemas |

**Installed skills.** `sports-betting-analyzer` (local) covers spreads, totals and
props at an analyst level. Public registry skills surveyed on 2026-09-16 —
`machina-sports/sports-skills@betting` (odds comparison, arbitrage, line movement)
and `joellewis/finance_skills@bet-sizing` — are market-data and sizing
utilities with **no model-evaluation guidance**; none covered de-vig method choice,
as-of line timing, placeholder odds, or CLV as a gate.

---

## Provenance

The ecosystem citations are this project's own: the win-expectancy bake-off
(sdv-py, 2026-08-07), CFB higher-order models, sdv-py's CFB odds cascade and
`odds_source` provenance, and the 2026-09-01 model-writeup improvements program.
The de-vig methods are standard: multiplicative and additive normalization; the
power method; and Shin, H. S. (1993), "Measuring the incidence of insider trading
in a market for state-contingent claims", *Economic Journal* 103(420). The Kelly
criterion is Kelly, J. L. (1956), "A new interpretation of information rate",
*Bell System Technical Journal* 35(4). No text was copied from surveyed skills.
