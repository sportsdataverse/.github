# Targets that are not binary or continuous — counts, durations, ordered classes

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. Each of these
> families previously had exactly **one** mention in the toolkit: the line in
> `literature.md` saying we do not cover it.

Three target shapes appear constantly in sports data and are modeled here as if
they were something else:

| what it is | what we currently do | what it should be |
|---|---|---|
| a **score** (0, 3, 7, 10, …) | continuous margin | a count |
| **time until an event** (career length, drive length, injury return) | not modeled | a duration, with censoring |
| an **ordered outcome** (seed, tier, EP class) | multiclass or continuous | ordinal |

Getting the family right is not pedantry. A normal margin model puts positive
probability on a team scoring −4 points and cannot answer "what is P(exactly 24)"
— which is what a total, an exact-score or an alternate-line market needs.

---

## 1. Counts — scoring, penalties, turnovers, shots

```python
import statsmodels.api as sm

Xc   = sm.add_constant(X)
pois = sm.GLM(y, Xc, family=sm.families.Poisson()).fit()
nb   = sm.NegativeBinomial(y, Xc).fit()   # ESTIMATES alpha; the GLM form fixes it
```

**Use `sm.NegativeBinomial`, not `GLM(family=NegativeBinomial(alpha=...))`.** The
GLM form takes `alpha` as a *fixed* input and does not estimate dispersion, so an
AIC comparison against it tests Poisson against one preselected variance rather
than against the best-fitting NB. Measured on genuinely Poisson data:

| fit | AIC |
|---|---:|
| Poisson | 13,239.3 |
| NB, `alpha` fixed at 1.0 | 14,935.4 ← an artifact of the fixed value |
| **NB, `alpha` estimated** | **13,241.3** (α̂ ≈ 0.00001) |

With `alpha` estimated the two essentially tie and α̂ collapses to zero, which is
the right answer: the NB *nests* Poisson and correctly finds no overdispersion.
The dramatic "NB is worse" gap was entirely the fixed value.

**Diagnose dispersion conditionally, not marginally.** `y.var() / y.mean()` is a
marginal ratio inflated by legitimate variation in the conditional mean across
covariates — on the Poisson data above it reads **1.335** while the model-based
Pearson dispersion reads **0.969**:

```python
dispersion = pois.pearson_chi2 / pois.df_resid   # ~1 => Poisson; >> 1 => overdispersed
```

On genuinely overdispersed data both flag it (marginal 2.43, Pearson 1.96) — but
only the Pearson statistic is answering the question the model actually poses.
Confirm with held-out predictive performance before switching families.

**Zero-inflation** is for a separate process that generates structural zeros —
a team that never attempts a two-point conversion is different from one that
attempts and fails. `sm.ZeroInflatedPoisson(y, X, exog_infl=Z)` fits both parts.

> **It emitted a `ConvergenceWarning` on the first fit in testing.** Zero-inflated
> models are the least stable family here. This is exactly the toolkit's
> silent-failure class: the object is returned, the parameters are populated, and
> nothing raises. **Assert `mle_retvals["converged"]` before reading any
> coefficient** — see `sklearn-xgboost.md` §F on swallowed convergence warnings.

**Boosted counts:** `xgb.XGBRegressor(objective="count:poisson")` works and its
mean prediction matched the observed mean to two decimals (2.03 vs 2.03). Use it
when the count depends on many interacting features; use the GLM when you want
coefficients and an honest interval.

**Why this matters for the simulators** (`literature.md`, agenda 3.4): a
bivariate Poisson with a correlation term gives correctly-shaped *joint* score
distributions. A normal margin gives you the spread and nothing else.

---

## 2. Durations with censoring — the part that is easy to get wrong

Censoring is the whole reason this is its own family. A player whose career is
ongoing has not "survived 6 years and stopped" — you know only that the career
is **at least** 6 years. Dropping those rows biases every estimate downward;
treating them as events biases it further.

```python
from lifelines import CoxPHFitter, KaplanMeierFitter

cph = CoxPHFitter().fit(df, duration_col="T", event_col="E")   # E: 1 = observed, 0 = censored
km  = KaplanMeierFitter().fit(df["T"], df["E"])
```

Verified against a known truth: with 30% right-censoring, `CoxPHFitter` recovered
a hazard ratio of **1.632** against a true `exp(0.5) = 1.649`. Kaplan-Meier gives
the survival curve and median without any covariates.

**XGBoost also fits survival**, with a gotcha worth stating because it does not
look like the rest of the API:

```python
d = xgb.DMatrix(X)
d.set_float_info("label_lower_bound", t)
d.set_float_info("label_upper_bound", np.where(censored, np.inf, t))  # inf = right-censored
xgb.train({"objective": "survival:aft", "eval_metric": "aft-nloglik",
           "aft_loss_distribution": "normal", "aft_loss_distribution_scale": 1.0}, d, 100)
```

`survival:aft` takes **interval labels, not `label`** — passing `label=` the
usual way raises. `survival:cox` uses the conventional `label` with negative
values marking censored rows.

**Where this applies here:** career length and aging (`literature.md`, agenda
3.3 — the survivor-bias problem in aging curves *is* a censoring problem),
injury return, drive continuation, time-to-first-score, and coach tenure. We do
none of it today.

---

## 3. Ordered outcomes — and why EP is not one

```python
from statsmodels.miscmodels.ordinal_model import OrderedModel
om = OrderedModel(y_ordered, X, distr="logit").fit(method="bfgs")
```

Proportional-odds ordinal regression estimates one coefficient per feature plus
`k-1` thresholds, rather than `k-1` separate coefficient vectors. Use it when the
classes are genuinely ordered and you want the parsimony: tournament seed,
injury severity, a graded scouting tier.

**EP's seven classes are *not* ordered** — touchdown, field goal, safety and
their defensive mirrors have point *values*, but they are not rungs on a ladder,
and the proportional-odds assumption would be false. EP stays
`multi:softprob`; what it needs is the multiclass *evaluation* in
`metrics-and-gates.md`, not an ordinal fit.

**The test for whether a target is ordinal:** would collapsing adjacent classes
still make sense? Seeds 1 and 2 collapse fine; touchdown and safety do not.

---

## 4. Scoring a distribution — CRPS

Once a model emits a distribution rather than a point, squared error is the wrong
score. **CRPS** is the proper scoring rule for a full predictive distribution and
reduces to MAE when the forecast is deterministic.

```python
import properscoring as ps
ps.crps_ensemble(observed, ensemble)   # (n,) obs against (n, m) simulated draws
ps.crps_gaussian(observed, mu, sigma)  # closed form when the forecast is normal
```

Verified: a correct ensemble scored **0.5804**; the same ensemble shifted by 1.0
scored **0.8055** — worse, in the right direction. The Gaussian closed form on
the same data gave 0.5751.

**This is what our season simulators are missing.** They are currently scored by
calibration slope alone, which checks that the probabilities are honest but says
nothing about whether the *shape* of the simulated distribution is right. CRPS
scores both at once, and it is the natural gate for anything that emits draws.

---

## 5. Dependencies

`statsmodels`, `lifelines` and `properscoring` are **not** `sdv-py` dependencies
and should not become hard ones. Counts and survival are both available in
`xgboost` (already a dependency) via `count:poisson`, `survival:cox` and
`survival:aft`; reach for the GLM libraries in a producer's own dependency group
or in `dev/` for an experiment — the placement rule in `sdv-data-pipeline`
Phase 2.

## See also

- `model-families.md` — choosing the learner once the family is settled.
- `metrics-and-gates.md` — multiclass evaluation for EP-shaped targets.
- `resampling.md` — intervals for any of these, clustered by game.
- `bayesian.md` — the hierarchical versions, when entities have unequal samples.
