# Modeling methods catalog

Distilled from the 13-system APM survey (`sdv-py/dev/apm-research/`, gitignored,
no other copy exists) plus four NBA method write-ups in `ClaudeCowork/nba_data/`.
Every rule below cites the source file it came from. Rejected approaches
(Lasso vs ridge, the `prism` academic lineage, dead/proprietary repos) belong
in `prior-art.md`, not here.

## Adjusted plus-minus family (RAPM, adjusted RAPM, prior-informed variants)

**RAPM *is* ridge regression on a sparse stint design matrix.** Each stint
(period between substitutions) is a row; each player gets two columns
(`_off`, `_def`) so the design is `(n_stints, 2*P)`. A player's offense
column is `+1` when their team is on offense that stint, `-1` for defense —
this offense/defense split is what makes it *adjusted* O-RAPM and D-RAPM
rather than one combined number. Target = points scored per stint (or per
100 possessions); sample weight = the stint's possession count.
(`apm-research/deep-research-report.md` §2.2; `nba_data/08-nba-rapm.md`;
`nba_data/09-adj-rapm-je.md`)

**The closed form:** `β̂ = (XᵀWX + λI)⁻¹XᵀWY`. λ is the L2 penalty that
resolves the multicollinearity of players who share the floor constantly —
without it, coefficients on tightly-paired players explode.
(`apm-research/deep-research-report.md` §2.1-2.2)

**λ/alpha selection actually used, by implementation:**
- sdv-py's shipped `nba_rapm.py`: `sklearn.RidgeCV` over
  `DEFAULT_RAPM_ALPHAS = np.logspace(2, 5, 8)` (i.e. 100 → 100,000).
  (`apm-research/local-code-inventory.md`)
- Ryan Davis (`NBA_Tutorials`): `RidgeCV(cv=5, fit_intercept=True)` with
  `sample_weight=possessions`; provides a `lambda_to_alpha(λ, n) = λ·n/2`
  conversion between the "λ" convention (Sill/Engelmann papers) and
  sklearn's `alpha` convention — needed when porting a published λ into
  sklearn. (`apm-research/local-code-inventory.md` #4)
- Adj-RAPM-JE (Jeremias Engelmann's own reference script): hand-specified
  alpha grid `[1500, 1750, …, 4000]`, `RidgeCV(cv=4)`. Large alphas
  (1.5k–4k) are *characteristic* of RAPM, not a bug — heavy shrinkage is
  expected because unregularized coefficients are wild.
  (`nba_data/09-adj-rapm-je.md`)
- `nba-rapm` notebook (Evan Zamir lineage): coarser grid
  `[0.01, 0.1, 1.0, 10, 100, 500, 750, 1000, 1500, 2000, 5000]`,
  `RidgeCV(cv=5)`. (`nba_data/08-nba-rapm.md`)
- `tonyelhabr/nba-rapm` (R): `glmnet` ridge with cross-validated λ.
  (`apm-research/code-catalog.md` Category 1)
- Sill's original method: out-of-sample K-fold CV minimizing held-out
  prediction error — the general principle every implementation above
  approximates with a coarse alpha grid.
  (`apm-research/deep-research-report.md` §2.2)

**A λ applied to nothing (a no-op ridge penalty) is a confirmed production
bug in this ecosystem** — see `references/failure-modes.md` (Task 6) for
the detection assertion. When wiring any ridge fit, assert the fitted
`alpha_`/`λ` actually entered the normal equations, not just that the model
object reports success.

**Season-decay weighting for multi-year pooling:** `{2024: 1.0, 2023: 0.9,
2022: 0.8}` — a `sample_weights` vector applied per stint-row alongside the
possession weight, so older seasons count less. Both Adj-RAPM-JE and
`nba-rapm`'s sibling repos use this convention; single-season fits leave
every weight at 1.0. (`nba_data/09-adj-rapm-je.md`;
`apm-research/local-code-inventory.md` #1)

**Prior-informed / Bayesian RAPM** (xRAPM, EPM, LEBRON, sdv-py's
`nba_adj_rapm.py`) residualizes the target against a box-score prior mean
`μ` before ridging: `y' = y − X·μ`, fit `δ̂ = (XᵀX+λI)⁻¹Xᵀy'` on the
residual, then `β̂ = μ + δ̂`. The prior is typically a Statistical
Plus-Minus (SPM) regression of multi-year RAPM on box-score stats.
(`apm-research/deep-research-report.md` §2.3; `apm-research/README.md`)

**RTO (randomize-then-optimize) posterior**, exact for
`N(β̂, σ̂²(XᵀX+λI)⁻¹)`: draw `ey ~ N(0, σ̂²I)` (len n) and
`ep ~ N(0, λσ̂²I)` (len 2P) per sample, solve
`(XᵀX+λI)δ = Xᵀ(y′+ey) + ep`, set `β_s = μ + δ`. Factorize `(XᵀX+λI)` once
(`scipy.sparse.linalg.factorized`) and back-solve per sample — this is the
mechanism sdv-py uses to get calibrated per-player confidence intervals
out of a ridge fit instead of a point estimate.
(`nba_data/plans/2026-07-02-nba-adj-rapm-prior-plan.md`, Task 2 grounded facts)

**Standard errors without RTO** — Jacobs's sandwich formula:
`Σ_β = σ̂²(XᵀWX+λI)⁻¹(XᵀWX)(XᵀWX+λI)⁻¹`. Cheap to compute directly from the
fitted design matrix; an alternative to full RTO sampling.
(`apm-research/deep-research-report.md` §2.14; `apm-research/README.md`)

**Alternative SE method:** bootstrap — refit on ~1,000 resampled stints and
take the empirical spread of the resulting coefficients (Engelmann's
approach for xRAPM). More expensive than the closed-form sandwich formula
but makes no Gaussian-posterior assumption.
(`apm-research/deep-research-report.md` §2.3)

**Known gaps vs the commercial systems** (LEBRON/PIPM/EPM), not yet closed
in sdv-py as of the survey date: (a) luck adjustment — replacing opponent
3P%/FT% outcomes with their expected value before regressing, since a
defense controls shot *frequency* but not make/miss variance; (b)
role/archetype-conditioned priors — regressing a player toward their
archetype's mean (e.g. "Spot-Up Shooter") rather than the league mean; (c)
exact standard errors (the Jacobs formula above, "cheap to add").
(`apm-research/README.md`)

**Pre-1997 historical possession estimation** (no possession field in the
box score): `POSS = 0.976 × (FGA + 0.44×FTA − OREB + TO)`.
(`apm-research/deep-research-report.md` §2.14)

## Projection systems (DARKO-style aging/prior blends)

**Shape:** a per-player Kalman filter over a multi-season rating panel,
with drift supplied by an empirically-fit aging curve — not a fixed
parametric aging function. (`apm-research/deep-research-report.md` §2.5;
`nba_data/plans/2026-07-02-nba-darko-projection-plan.md`)

**Aging curve — delta method:** group `Δ = rating[t+1] − rating[t]` by the
*starting* age `round(age[t])`; the mean `Δ` per age bucket is that age's
expected drift. Apply a centered moving-average smoothing window (odd
`smooth`, default 3) over the age axis before use. Drift into season `t` =
`delta(round(age[t-1]))`. (`nba_data/plans/2026-07-02-nba-darko-projection-plan.md`, Task 2)

**Kalman state:** latent skill `s`; predict step `s_pred = s + aging_curve.delta(age[t-1])`,
`P_pred = P + q` (process variance `q`); observation variance
`r_t = obs_base / weight[t]` (weight = e.g. possessions — noisier
estimates from low-minute seasons get less update weight); Kalman gain
`k = P_pred / (P_pred + r_t)`. Forecast next season:
`projected = s_final + aging_curve.delta(age_last)`,
`sd = sqrt(P_final + q)`. (`nba_data/plans/2026-07-02-nba-darko-projection-plan.md`, Task 3)

**Noise-parameter fitting:** `(q, obs_base)` are MLE-fit by maximizing the
one-step-ahead forecast log-likelihood (Nelder-Mead on the log-params,
deterministic, no RNG); fall back to `defaults=(0.25, 1.0)` if optimization
fails or returns non-finite values. Fit globally on the full panel (a
low-dimensional curve + 2 scalars — standard), while forecast validation
holds out per-player rating-history prefixes.
(`nba_data/plans/2026-07-02-nba-darko-projection-plan.md`, Tasks 4-5)

**Validation contract:** forecast RMSE must beat the carry-forward-last-value
baseline, and forecast correlation with the actual next-season rating
must be meaningfully positive — *only* when the underlying panel actually
carries persistent player skill. A meta-oracle should assert this on a
synthetic skill panel (predictable persistence) and confirm it does NOT
hold on a synthetic noise panel (no persistent skill) — a model that beats
baseline on pure noise means the validator is broken, not that the model
is good. (`nba_data/plans/2026-07-02-nba-darko-projection-plan.md`, Task 5)

**DARKO itself is closed-source** — no public repository implements the
real system; only the methodology (exponential decay + Kalman filter) is
published. The `darko-app` companion repo documents the feature-panel
schema it consumes: `box_dpm = box_ddpm + box_odpm`, a survivorship/longevity
table, and decay-weighted five-man net ratings filtered to
`total_poss >= 100`. (`apm-research/code-catalog.md` Category 4;
`apm-research/local-code-inventory.md` #8)

## Rating systems (CFB/NFL/MBB/WBB engines)

**The corpus does not cover this family.** Both source bundles are
basketball/APM-focused; neither the deep-research survey nor the code
catalog nor the two NBA method write-ups discuss CFB, NFL, MBB, or WBB
rating engines. The only adjacent content is NCAA *schedule-strength*
adjustment (Elo, KenPom) used to make college RAPM comparable across
disparate schedules — see the Possession engines section below for the
citation.

## EP / WP / CP / xYAC (the football model recipe)

**Not covered.** The corpus is entirely basketball-scoped; no source
document mentions expected points, win probability, completion probability,
or expected yards after catch.

## xG (hockey/soccer)

**Not covered.** No source document discusses hockey or soccer expected-goals
modeling.

## Possession engines (NBA / NCAA possession boundaries)

**sdv-py already ships the possession/lineup layer** the APM math consumes:
`nba_possessions.py` / `nba_possession_rules.py` / `nba_lineups.py` (stint +
on-court construction) and `nba_season_compile.py` (cached season compiler).
External repos below are for cross-validation, not reimplementation.
(`apm-research/local-code-inventory.md`)

**`pbpstats` (Darryl Blackport) is the gold-standard reference** for
NBA/WNBA/G-League possession parsing: it fixes out-of-order PBP events
(substitutions frequently log *after* free throws in the raw feed),
resolves the on-floor lineup for every event, and breaks possessions down
by start time, end time, and score margin. Do not hand-roll this parsing —
use it as the oracle. (`apm-research/deep-research-report.md` §4;
`apm-research/code-catalog.md` Category 8; `apm-research/local-code-inventory.md` #10)

**`nba-on-court`/`shufinskiy`** is a lighter alternative focused solely on
deriving the 10 on-court players per event via substitution analysis; its
sibling `nba_data` mirror is a rate-limit-free bulk backfill source
(1996-97 → present) for possession reconstruction.
(`apm-research/local-code-inventory.md` #9)

**College possession parsing is an ingestion problem, not a math problem**
— the model math is data-agnostic once possessions exist. NCAA PBP is
highly non-standardized; `nkal22/ncaa_hoops_pbp` (the hoop-explorer
backend) and `jflancer/bigballR`'s `get_lineups` are the two verified
open-source engines that resolve NCAA on-court lineups and on/off splits.
(`apm-research/deep-research-report.md` §5; `apm-research/code-catalog.md`
Category 6)

**College small-sample constraints:** a season is ~30 games; even a
high-minute starter logs only ~1,500 possessions vs >5,000 in the NBA.
Combined with tight coach rotations (starters together 80%+ of minutes),
ridge regression alone often cannot separate two players who rarely play
apart — this is why college RAPM leans harder on informative priors than
NBA RAPM does. (`apm-research/deep-research-report.md` §5)

**Schedule-strength anchoring:** hoop-explorer keys its RAPM so the
possession-weighted sum of a team's player RAPM ≈ that team's KenPom
adjusted efficiency margin, making cross-conference comparisons
interpretable despite wildly disparate schedules.
(`apm-research/deep-research-report.md` §2.11, §5)

**Freshman/rookie priors:** composite recruiting rank feeds the prior for
players with no college possession history — hoop-explorer's cited
example is "Top-10 recruit → +6.5 pts/100" as the seed value.
(`apm-research/deep-research-report.md` §2.11, §5)

**Role/archetype clustering for priors:** K-means on box-score attributes
(AST:TOV ratio, 3-point attempt rate, rebounding rate) assigns players to
micro-roles (e.g. "Scoring PG," "Stretch-PF") so priors regress a player
toward their role's mean rather than the league mean.
(`apm-research/deep-research-report.md` §2.11)

## Simulation (season sims and calibration)

**Not covered.** None of the five source documents discuss season
simulation or simulation calibration; this survey is about player-impact
point estimates and projections, not game/season outcome sampling.
