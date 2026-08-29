# Feature engineering — building the columns a model fits on

> Reference file of the `sdv-modeling` skill. Merged from the retired
> `sdv-engineering-ml-features` skill on 2026-08-28 and rewritten against this
> ecosystem's shapes. The generic encoder/scaler catalogue was dropped — it is
> correct and unchanged from any sklearn tutorial. What is kept is the part
> that behaves differently on panel-sports data.

Which release dataset feeds which feature family is `data-sources.md`. This
file is about the *transformation*, not the source.

---

## 1. Cyclical encoding — clock, season-week, and day-of-year

**The trap.** Encoding a game clock, a week number, or a day-of-year as a plain
integer tells the model that week 1 and week 15 are maximally distant, when for
anything that wraps — day-of-year across a New Year bowl window, a clock
counting down within a period — they are adjacent.

```python
import numpy as np


def cyclical(values, period):
    """Encode a wrapping quantity as a (sin, cos) pair.

    Args:
        values: The raw quantity -- day-of-year, minute-of-game, month.
        period: The wrap length -- 365, 60, 12. Getting this wrong is silent:
            the pair is still smooth, just periodic at the wrong rate.

    Returns:
        (sin, cos) arrays. Both are needed -- sin alone maps two distinct
        points in the cycle to the same value.
    """
    theta = 2 * np.pi * np.asarray(values) / period
    return np.sin(theta), np.cos(theta)
```

**When NOT to use it.** A CFB season week does *not* wrap — week 15 is followed
by the postseason, not by week 1, and the two are not adjacent in any sense a
model should learn. Cyclical encoding is for genuinely periodic quantities:
clock within a period, month, day-of-year for a sport that crosses the New
Year. Applying it to a monotone season index invents an adjacency that is not
there. Ask "does the last value neighbour the first?" before reaching for it.

---

## 2. Target encoding on entities — where leakage actually enters

Team and player identity are the highest-cardinality categoricals we have
(~5,000 NCAA players per season) and target encoding is the standard answer.
It is also the single easiest way to leak.

**The rule: the encoding must be fit inside the CV fold, from data strictly
prior to the row it encodes.** A team's mean EPA computed over the full season
and joined onto week-3 rows carries weeks 4-15 into a week-3 prediction. That
is not a fold-hygiene technicality — it is the same as-of-date boundary that
`metrics-and-gates.md` §3 gates, applied to a feature instead of a split.

Three requirements, all checkable:

1. Fit the encoder inside a `Pipeline` so `cross_val_score` refits it per fold
   (`sklearn-xgboost.md` §C).
2. Compute it as-of, from prior games only — an expanding mean, not a full-season
   mean.
3. Shrink toward the population mean for low-sample entities, or a player with
   four possessions gets an encoding equal to his four-possession average and
   the model treats it as fact. This is the same empirical-Bayes shrinkage the
   RAPM family already applies to ratings; see `methods.md`.

**Unknown entities at predict time** are guaranteed, not exceptional — every
season introduces freshmen and every trade deadline moves players. Configure
`handle_unknown="infrequent_if_exist"` (or `"ignore"`) explicitly and assert
the encoder does not raise on an unseen id; `sklearn-xgboost.md` §E is the full
treatment.

---

## 3. Leakage-safe preprocessing is a Pipeline question, not a feature question

Scaling, imputation, and selection fit on the full frame before CV leaks fold
statistics forward. The fix is structural — everything inside a `Pipeline`,
never a `.fit_transform()` on the whole frame — and it is documented once, with
its detection test, in `sklearn-xgboost.md` §C (`assert_no_preprocessing_leak`).
It is not restated here.

The feature-specific corollary: **a feature that looks backwards needs a purge,
not just a Pipeline.** A `Pipeline` refits the transform per fold; it does not
know that a `rolling_4_game_epa` column was computed from games sitting in the
other fold. That is `sklearn-xgboost.md` §A2.

---

## 4. Feature selection: the substrate is usually low-dimensional

Measured, on our own data: CFB pregame went 15.14 → 12.97 MAE against a 12.27
market ceiling, and **60 features beat 244** — the predictive substrate is
roughly one-dimensional (`prior-art.md`, CFB higher-order models). Special
teams, added as 18 separate columns, turned out to be overstated 18x.

Practical consequence: reach for selection *before* a hyperparameter search,
and prefer the cheap filters. Mutual information and L1 both work; recursive
elimination rarely earns its cost at our feature counts. The honest check is
whether a smaller set holds up against the oracle, not whether it holds up in
CV — CV rewards the larger set for exactly the leakage this file is about.

---

## 5. Naming and dtype discipline

- **Feature order is load-bearing at consume time.** XGBoost validates
  `feature_names` alignment only when the booster carries them; some of our
  bundled models were saved with `feature_names=None`, so the caller-side
  ordering contract is the only protection. `sklearn-xgboost.md` §J names the
  exact call sites.
- **Join keys are `Utf8` or `Int64`, pinned once at the boundary.** A
  float-origin id stringifies as `"123.0"` and silently matches nothing. This
  is the ecosystem-wide rule in `sdv-py/CLAUDE.md` and it bites hardest in
  feature joins, where a 0% match rate looks like a legitimately sparse feature.
- **Assert the match rate after every entity join**, with a floor. A crosswalk
  that silently drops 40% of players produces a feature column that is mostly
  null and a model that quietly learns "null means bad".
