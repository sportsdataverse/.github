# Bayesian workflow — pooling, priors, and the diagnostics that must gate it

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. The audit found
> `prior-art.md` *describing* Bayesian work that was built, "hierarchical /
> partial pooling" mentioned **once** (in a routing table), and MCMC diagnostics
> **zero** times — under a capability `methods.md` claims.

Partial pooling is not an exotic technique here. It is the correct answer to the
single most common shape in our data: **many entities, wildly unequal sample
sizes.** A player with 4 possessions and a player with 2,000 are currently
served the same way (see the stabilization gap in `literature.md`), and pooling
is what fixes that at the model level rather than with a minimum-minutes filter.

---

## 1. What pooling buys, measured

200 players, possessions drawn from 3 to 600, a true skill drawn N(0, 1.2), and
an observation whose noise scales as `6/sqrt(n)` — i.e. low-minute players are
observed badly. A two-level model:

```text
mu    ~ Normal(0, 5)              # league mean
tau   ~ HalfNormal(2)             # between-player spread, FITTED not assumed
theta ~ Normal(mu, tau)           # per-player skill
y     ~ Normal(theta, 6/sqrt(n))  # what we observe
```

| | RMSE vs the true skill |
|---|---:|
| raw observed value | 0.606 |
| **posterior mean (pooled)** | **0.418** |
| raw, players with n < 20 | 1.91 |
| **pooled, players with n < 20** | **0.96** |

**Pooling halves the error for the players it is hardest to measure**, and costs
almost nothing for the well-measured ones. That is the whole argument. The
shrinkage strength is `tau`, and the model *fits* it — which is the difference
between this and picking a magic regularization constant.

This is the same idea as the RAPM prior already in the codebase
(`nba_adj_rapm.py::_fit_prior_ridge`); the difference is that a hierarchical fit
estimates the pooling strength from the data instead of selecting it by CV.

---

## 2. Three diagnostics, and none of them is optional

The toolkit's top-level rule is that **a component which ran without error has
not been shown to do anything.** An MCMC fit is the purest case: it always
returns samples. The samples can be garbage.

Measured on the model above — a fit that looks healthy on two diagnostics:

```text
divergences  = 0          ok
min ess_bulk = 1707       ok
max r_hat    = 1.0246     FAILS  (want < 1.01)
```

**Zero divergences and high ESS did not mean the chains converged.** Report all
three or you will ship the run above believing it was fine.

| diagnostic | threshold | what it means when it fails |
|---|---|---|
| `r_hat` | **< 1.01** | chains disagree — the posterior you are reading is one chain's opinion. Run longer, or reparameterize. |
| `ess_bulk` | > 400 **pooled** | not enough independent information for the mean/sd. `az.summary` reports ESS pooled across chains and draws, so this threshold is on the pooled value, not per chain. |
| `ess_tail` | > 400 pooled | the *interval* is unreliable even if the mean is fine — and intervals are what we would publish. |
| divergences | **exactly 0** | the sampler could not follow the geometry. Non-zero divergences invalidate the run; they are not a warning. |

```python
import arviz as az

def assert_mcmc_healthy(idata, rhat_max=1.01, ess_min=400):
    """Fail the fit, not the review, when the sampler did not converge.

    Call this BEFORE reading any posterior quantity. A run with divergences or
    r_hat above threshold has not estimated the thing you are about to publish.
    """
    # Raise, do not assert: `python -O` strips assert statements, and a gate that
    # vanishes under an optimization flag is not a gate.
    s = az.summary(idata)
    div = int(idata.sample_stats["diverging"].sum())
    problems = []
    if div:
        problems.append(f"{div} divergent transitions -- reparameterize (section 3)")
    if s["r_hat"].max() >= rhat_max:
        problems.append(f"max r_hat {s['r_hat'].max():.4f} >= {rhat_max}")
    if s["ess_bulk"].min() <= ess_min:
        problems.append(f"min ess_bulk {s['ess_bulk'].min():.0f} <= {ess_min}")
    if s["ess_tail"].min() <= ess_min:
        problems.append(f"min ess_tail {s['ess_tail'].min():.0f} <= {ess_min}")
    if problems:
        raise RuntimeError("MCMC did not converge: " + "; ".join(problems))
```

**ArviZ API note (1.3.0).** `az.rhat(idata).to_array()` raises
`AttributeError: 'DataTree' object has no attribute 'to_array'` — the return
type changed in ArviZ 1.x. `az.summary(idata)` is the portable route and is what
the helper above uses. Its interval columns are also `eti89_lb`/`eti89_ub` now,
not the `hdi_3%`/`hdi_97%` older code expects.

---

## 3. Centered vs non-centered — measure, do not follow the folklore

The standard advice is "hierarchical model diverges → use the non-centered
parameterization." **Measured, that advice is right in one regime and expensive
in the other.** Same model, same data, 4 chains × 2000 draws:

| regime | parameterization | r_hat | min ESS | divergences |
|---|---|---:|---:|---:|
| informative (`tau` = 1.2) | **centered** | 1.0027 | **12,089** | 0 |
| informative (`tau` = 1.2) | non-centered | 1.0038 | 685 | 0 |
| weak signal (`tau` = 0.15) | centered | **1.3020** | 11 | **278** |
| weak signal (`tau` = 0.15) | **non-centered** | 1.0033 | **2,092** | 1 |

Two findings, both actionable:

- **When the data is informative, centered is 18x more efficient.** Reaching for
  non-centered by reflex costs an order of magnitude of ESS in the common case —
  which for us is any well-sampled entity (a full-season team, a 2,000-possession
  player).
- **When the signal is weak relative to the noise, only non-centered works.**
  Centered gave 278 divergences and an r_hat of 1.30 — a completely failed fit.
  That is the funnel: when `tau` is small, `theta` is squeezed into a neck the
  sampler cannot traverse.

Our data spans both regimes *within a single model*, because possession counts
range from 3 to 2,000. **Fit it both ways once, require BOTH to clear every gate
in §2, and among those that pass keep the higher ESS.** Selecting on ESS alone
would pick a run with more effective draws from a chain set that never converged
— higher ESS with a failing r_hat is a more confident wrong answer.

```python
# centered -- prefer when entities are well sampled
theta = numpyro.sample("theta", dist.Normal(mu, tau))

# non-centered -- required when tau is small relative to the observation noise
theta_raw = numpyro.sample("theta_raw", dist.Normal(0, 1))
theta = numpyro.deterministic("theta", mu + tau * theta_raw)
```

**And check the sampling budget before blaming the geometry.** The r_hat = 1.0246
failure in §2 came from 2 chains × 500 draws; the *same* centered model at
4 × 2000 gives r_hat = 1.0027 with zero divergences. A high r_hat with zero
divergences usually means "run longer"; divergences mean "reparameterize".

## 4. Priors are a modeling decision, so state them

A flat prior is a choice, and usually a bad one on our data because it says a
player could plausibly be 50 points better than average.

| parameter | reasonable prior | why |
|---|---|---|
| league mean `mu` | `Normal(0, 5)` on a centered scale | weakly informative; the scale comes from the stat's units |
| between-entity spread `tau` | `HalfNormal(sd)` with `sd` near the observed spread | **never** `Uniform(0, 100)` — it puts most mass on absurd spreads and causes divergences |
| a rate or probability | `Beta` matched to the league base rate | the base rate is known; use it |
| a coefficient | `Normal(0, 1)` on standardized inputs | equivalent to ridge, and interpretable |

**Record the prior in the model card.** A posterior is not reproducible from the
data alone, and "what prior did this use" is exactly the question a reader of a
published rating will ask. This belongs in the `models/REGISTRY.md` row's
lineage, like any other fitted constant.

---

## 5. When you do not need MCMC

Most of the value above is available without a sampler, and the cheaper routes
have no extra dependency:

- **Empirical Bayes / James-Stein.** Estimate `tau` by method of moments from
  the observed spread minus the average sampling variance, then shrink each
  entity by `tau^2 / (tau^2 + se_i^2)`. Pure numpy, closed form, and it captures
  most of the RMSE gain in §1. This is the right first move for a leaderboard.
- **Ridge with a prior mean** — already in the codebase for RAPM. Equivalent to
  a Gaussian prior centered on the prior mean.
- **`RidgeCV` / hierarchical-flavored GLMs** when you want pooling without a
  posterior.

Reach for full MCMC when you need **the interval**, a non-Gaussian likelihood,
or a multi-level structure (player within team within season) that closed forms
cannot express.

---

## 6. Tooling

`numpyro` + `arviz` is the stack verified for this file (numpyro 0.21, arviz
1.3, jax 0.11). PyMC is equivalent and slower to install; Stan/`brms` is the R
route and the local `r-skills:r-bayes` skill covers it.

**None of these are dependencies of `sdv-py`,** and they should not become hard
ones. A Bayesian fit belongs in a producer's `python/` package with the library
in that repo's own dependency group, or in `dev/` for an experiment — the same
placement rule as any other stage (`sdv-data-pipeline` Phase 2).

## See also

- `resampling.md` — the frequentist route to the same intervals, and the
  clustering rule that applies to both.
- `metrics-and-gates.md` §1 — a posterior interval still has to be *calibrated*;
  coverage is checked the same way as a conformal interval's.
- `methods.md` — where the player-impact family that needs this is described.
