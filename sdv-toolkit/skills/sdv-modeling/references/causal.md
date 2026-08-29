# Causal inference — when the question is "did X cause Y", not "predict Y"

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. The audit found
> **zero** mentions of difference-in-differences, instrumental variables or
> propensity scores anywhere in the toolkit — while the local paper corpus has a
> whole cluster of sports work using them.

Most of what this ecosystem ships is prediction, and for prediction none of this
matters. It matters the moment a question changes shape:

| prediction question | causal question |
|---|---|
| how many points will this team score? | did the rule change alter scoring? |
| what is this player's impact? | did the coaching change cause the improvement? |
| what is P(win)? | does resting starters cost wins? |
| which fourth-down call is better? | **what would have happened had the coach chosen otherwise?** |

That last row is not hypothetical. It is exactly the fourth-down selection-bias
problem Daly-Grafstein (2023) treats and Brill (2023) names as a flaw in the
surfaces we ship (`literature.md`). **We already have a causal problem in
production and are treating it as a prediction problem.**

---

## 1. The failure that motivates everything else

Difference-in-differences with a placebo: 60 teams, 20 seasons, half "treated"
from season 10, **true effect exactly 0**, and within-team shocks that are
serially correlated (AR(1), ρ = 0.9) — which is what team quality actually looks
like across seasons.

| standard errors | coefficient | SE | t | p |
|---|---:|---:|---:|---:|
| plain OLS | 1.320 | 0.1643 | 8.04 | **< 0.0001** |
| team-clustered | 1.320 | 0.4271 | 3.09 | 0.0020 |

**A true effect of zero produced a "highly significant" 1.320.** This is the
Bertrand–Duflo–Mullainathan result, reproduced on a sports-shaped panel:
serial correlation in the outcome makes plain DiD standard errors badly
anti-conservative.

Note the second row honestly: **clustering widened the SE 2.6x and still
rejected.** Clustering is necessary and was not sufficient here. With 60 clusters
and strong serial correlation you also want a placebo test — run the same
regression on pre-treatment periods only. A placebo that "finds" an effect is
**strong evidence against the design**; a clean placebo is only weak evidence
for it, since the test has limited power and pre-periods are not the
counterfactual that matters. Treat it as a screen that can condemn, not certify.

**And a counterexample that keeps the rule honest:** in a second DGP where the
correlation was a pure team-level *level* shift, adding team fixed effects
absorbed it and the clustered SE came out 0.95x — *narrower* than plain.
Clustering is not automatically conservative. Cluster because the dependence is
real and unabsorbed, not as a ritual.

---

## 2. Difference-in-differences

```python
import statsmodels.formula.api as smf

m = smf.ols("y ~ did + C(team) + C(season)", d).fit(
    cov_type="cluster", cov_kwds={"groups": d["team"]}
)
```

Two-way fixed effects plus a `treated × post` interaction. Recovered 1.547
against a true 1.5 in the clean case.

**The identifying assumption is parallel trends**, and it is an assumption, not
an output — and it concerns the *unobserved* post-treatment counterfactual, which
no test can reach. Pre-period checks give **compatibility evidence, not proof**:
pre-trends that move together are consistent with the assumption; a rejection can
come from sampling variation and a non-rejection from low power. Report the
pre-trend evidence, and justify parallel trends on design grounds — why this
treatment's timing is plausibly unrelated to the outcome path — not on a passing
test.

**Where this fits SDV data:** rule changes (the CFB `ERA_SEASON_CUTS` at
2001/2005/2013/2017, the WBB halves→quarters break at 2016, NHL overtime and
shootout changes, the NFL kickoff rules), conference realignment, stadium moves,
and the transfer portal. Each is a treatment applied to some units at a known
date — the DiD setup, sitting in data we already publish.

**Staggered adoption caveat.** When units are treated at *different* times,
classic two-way FE is biased (the Goodman-Bacon problem) because already-treated
units serve as controls. Conference realignment is exactly staggered. Use a
modern estimator (Callaway–Sant'Anna, Sun–Abraham) or restrict to a clean
never-treated control group, and say which you did.

---

## 3. Instrumental variables

When the treatment is chosen for reasons correlated with the outcome — which is
most coaching decisions — OLS is biased and no amount of controls fixes it.

Verified on a confounded design with a true effect of 2.0:

| estimator | estimate |
|---|---:|
| OLS | 1.455 (biased toward the confounder) |
| **2SLS** | **2.031** |

```python
from statsmodels.sandbox.regression.gmm import IV2SLS
iv = IV2SLS(y, exog_with_x, instruments).fit()
```

**A valid instrument must move the treatment and affect the outcome only
through it.** That second half is untestable and is where sports IV arguments
usually fail. Candidates that have been used in the corpus's tradition: weather
(moves pass/run choice, plausibly nothing else), injuries to unrelated players,
schedule quirks, and coin-flip outcomes in overtime.

**Report the first-stage F — `IV2SLS.fit()` does not compute one.** It returns
the second-stage result only, so run the first stage yourself and test the
*excluded* instruments jointly:

```python
import statsmodels.api as sm

first = sm.OLS(treatment, sm.add_constant(np.column_stack([controls, instruments]))).fit()
n_ctrl = controls.shape[1] if controls.ndim > 1 else 1
r_matrix = np.eye(first.params.size)[1 + n_ctrl:]     # rows for the instruments only
f_stat = float(first.f_test(r_matrix).fvalue)
if f_stat < 10:
    raise RuntimeError(f"weak instruments: first-stage F {f_stat:.1f} < 10")
```

Below ~10 the instrument is weak and 2SLS is biased *toward* OLS while looking
respectable — the worst case, because the bias points at the answer you were
trying to escape.

---

## 4. Propensity scores and matching

For a binary treatment with observed confounders: model P(treated | X), then
compare treated to control units with similar propensity — by matching,
stratification, or inverse-probability weighting.

The corpus has this applied to sports directly (`Player Tracking Facilitates
Valid Causal Inference`; `Scoring a Touchdown with Variable Pricing`).

Three rules that decide whether it works:

1. **Check overlap first.** If treated and control propensity distributions
   barely intersect, there is no comparable control and no weighting fixes it.
   Plot the two distributions before estimating anything.
2. **Balance is the diagnostic, not the propensity model's own accuracy.** After
   matching, standardized mean differences on every confounder should be < 0.1.
   A propensity model with excellent AUC and poor balance has failed.
3. **It only adjusts for what you measured.** Unlike IV, propensity methods
   assume no unobserved confounding. In sports that assumption is usually
   heroic — coaches know things the data does not record.

---

## 5. The one to actually build first

**Fourth-down selection bias.** We publish recommendations from a model fit on
outcomes that are only observed for the branch the coach chose. The counterfactual
— what would a punt have produced in this state — is never observed for the
states where coaches always go for it, and vice versa. That is textbook selection
on the treatment.

Daly-Grafstein (2023) is in the local corpus with the correction. This is the
highest-value causal work available to us because the affected surface is already
in production and shipping default-on.

---

## 6. Dependency and placement

`statsmodels` is not an `sdv-py` dependency and should not become one. Causal
analysis is research, not a producer stage: it belongs in `dev/` for an
experiment or in a producer repo's own dependency group, per `sdv-data-pipeline`
Phase 2. What *may* graduate into a release is the estimate plus its interval —
with the design, the identifying assumption, and the placebo result recorded in
the model card, because a causal estimate is not reproducible from the data
alone.

## See also

- `resampling.md` — the clustered permutation test is the non-parametric route
  to the same inference, and the clustering rule is identical.
- `literature.md` — Daly-Grafstein and Brill on fourth down; the corpus's
  DiD/propensity cluster.
- `metrics-and-gates.md` — a causal estimate is gated by the honesty of its
  design, not by a holdout metric.
