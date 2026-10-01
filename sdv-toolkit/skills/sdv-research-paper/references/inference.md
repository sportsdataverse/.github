# Inference checks for panel sports data

Which test, metric and resample is correct lives in `sdv-modeling`
(`metrics-and-gates.md`, `resampling.md`). This file is the paper-side
checklist: what a printed inferential statement must carry.

Generic statistics skills (statistical-analysis, exploratory-data-analysis)
default to normality / equal-variance checks on rows treated as independent.
On games nested in seasons and teams that misleads; ignore those defaults.

## Checks (each one a FAIL)

1. **One cluster unit.** Every printed t, p and SE uses the same resampling or
   cluster unit as the paper's intervals. *Paper A: abstract t = 2.49 used
   unclustered SEs (`_common.py`); season-clustered t = 1.87, p = 0.08.*
2. **Cluster ≥ shared state.** The resample unit is at or above the level
   where model state or conditions are shared: season for a season-carried
   filter or rating, game for play-level work. A limitation that calls the
   finer interval "slightly narrow" must cite the measured SE ratio across
   candidate units. *Paper A: season clustering widened SEs 11–43%.*
   **With few clusters (under about 15 seasons),** the cluster-bootstrap
   percentile interval under-covers, and row-level inference over-rejects.
   Neither is valid, and taking the wider of the two carries no coverage
   guarantee. Report the per-season estimates, an exact sign-flip
   (randomization) p, and a `t(G−1)` interval on the per-season deltas
   (`sdv-modeling` → `resampling.md` §1b; Cameron & Miller 2015). The
   row-vs-cluster SE ratio is a diagnostic, never the interval. *Paper B, 10
   seasons: the ratio ran 0.58× to 1.17× depending on the statistic.*
3. **Nulls are bounded on the scale the conclusion acts on.** "No effect / adds
   nothing / did not help" needs a pre-declared smallest effect of interest δ
   with an interval compared to ±δ (equivalence), or the minimum detectable
   effect at the achieved n. Never just "CI covers 0" or a t-stat. The bound
   must be on the scale of the conclusion: a null on rank correlation does not
   support a conclusion about points or money. *Paper B: bounded on ρ, but in
   points the line could still be 0.69 worse, twice the best rater's whole gap.*
4. **Holdout power.** A holdout sign flip or "did not replicate" is reported
   with the holdout's power for the in-sample effect. *Paper A: MDE was 5.9×
   the in-sample effect, power ~8%, and a sign flip had a 32% chance even if
   the effect were real.*
5. **Calibration is tested.** "Well calibrated" requires the calibration
   error (quantile bins) to be compared with its distribution under simulated
   perfect calibration. "Discrimination, not calibration" requires the Brier
   reliability/resolution decomposition. *Paper A: in both leagues the market's ECE
   (0.024) exceeded the null 95th percentile (0.014 / 0.019).*
6. **Bounds are bounds.** No point estimate is phrased as a bound ("at most
   18%"); every ratio or share gets an interval (that 18% ran ~10–26%).
7. **Interval label.** Each interval states level, method and resample unit
   where it first appears, and in the abstract.
8. **Differences get intervals.** A comparison of two estimates prints an
   interval on the difference, not two separate intervals.
9. **Multiplicity declared, and applied to every member.** Name each family
   of tests and its size (configurations, techniques × leagues, subgroups).
   For any family with more than one member, correct or label it "exploratory".
   With few clusters, use a max-T permutation or a model confidence set
   (`resampling.md` §1b). A Bonferroni cutoff below the sign-flip resolution
   floor 2/2^G can never reject. The family and correction are fixed before the
   p-values are seen. The reviewer applies the
   paper's own decision rule to **every** member of the family, not only the
   ones the prose reports.
   **Significance is not a difference.** Ranking groups by which interval
   excludes the null ("A is calibrated, B is not") is not a test that A and B
   differ. Test the difference.
10. **Selection optimism.** A grid winner reports the optimism of picking the
    best of k (leave-one-season-out re-selection is a cheap check). Any
    winning value on the edge of its grid is reported.
11. **Stability is measured.** "Stable across seasons" needs a trend test and
    a heterogeneity statistic, not just a per-season figure. A holdout shift
    attributed to a cause needs that cause sized.
12. **Trend before pooling.** If the per-season series has a slope, print the
    recent-era estimate next to the pooled one. Before blaming a tune-to-holdout
    shift on selection or overfitting, compare it with (i) the last k tune
    seasons (k = holdout length), (ii) the trend's extrapolation, and (iii) a
    change in benchmark composition (`benchmark.md` check 1). *Paper A credited
    the holdout widening to picking the best of many configurations, but four
    blind reviewers found the gap already that wide in 2017–21. Measured, the
    selection effect was about 0.0003.*
13. **Calibration has more than one number.** Report calibration slope (and
    intercept) or the Brier reliability term with an interval, alongside ECE.
    ECE depends on how predictions are binned; slope does not.
14. **Shared inputs, shared answers.** Agreement between estimators that share an
    input (for example, all built from final scores) is partly by construction,
    so it isn't evidence of "one latent quantity". Compared predictors are put
    on the same scale and range before ranking them.
15. **Replacing is not adding.** Swapping one input for another doesn't test
    whether adding that information helps. Test the addition.
16. **Precision follows uncertainty.** Round the uncertainty to 1–2
    significant figures, then the estimate to the same decimal place.
