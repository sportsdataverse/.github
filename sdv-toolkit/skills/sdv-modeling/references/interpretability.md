# Interpretability — explaining a model we already ship

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. Before this the
> toolkit had **zero** mentions of SHAP or partial dependence and one of
> permutation importance, while the ecosystem ships nine boosted models
> (`ep`, `wp_naive`, `wp_spread`, `cp`, `fg`, `fd`, `xpass`, `two_pt`, `qbr`).

The practical problem this solves is not curiosity. It is: **a model behaves
oddly for one stratum and there is no standard first move.** Aggregate metrics
are the last place a sports-model bug shows up, because the bug lives in a
stratum (`metrics-and-gates.md` §1b). These are the tools that find it.

---

## 1. You do not need the `shap` package

Every model we ship is XGBoost, and **XGBoost computes exact TreeSHAP itself**:

```python
contribs = booster.predict(dmatrix, pred_contribs=True)   # (n_rows, n_features + 1)
```

The last column is the base value; the rest are per-feature contributions in
**margin space** (log-odds for a binary objective, not probability). Verified:
`contribs.sum(axis=1)` equals `booster.predict(..., output_margin=True)`, and the
values are identical to `shap.TreeExplainer` to 1e-4.

`booster.predict(dmatrix, pred_interactions=True)` returns the
`(n, p+1, p+1)` interaction tensor the same way.

| you want | reach for | dependency |
|---|---|---|
| per-row attributions for a shipped model | `pred_contribs=True` | **none — xgboost only** |
| the plotting surface, beeswarm/waterfall | `shap.TreeExplainer` | optional `shap` |
| a model-agnostic answer (non-tree, or a pipeline) | `sklearn.inspection.permutation_importance` | **none — sklearn only** |
| the shape of a relationship | `sklearn.inspection.partial_dependence` | **none — sklearn only** |

**Prefer the dependency-free route** for anything that runs in a producer
pipeline. `shap` is worth installing for interactive investigation, not for a
scheduled job.

---

## 2. The three tools answer three different questions

Do not treat them as interchangeable; they disagree for real reasons.

| tool | question | scope |
|---|---|---|
| SHAP | *for this play*, what moved the prediction? | per row, additive |
| permutation importance | if this feature were noise, how much worse is the model? | global, prediction-quality |
| partial dependence | as this feature varies, what shape does the prediction trace? | global, functional form |

Measured on a synthetic WP-shaped model (features `score_margin`, `time_left`,
`down`), the two global measures rank the features identically but on different
scales — SHAP in margin units, permutation in lost-accuracy units:

```
mean |SHAP|            score_margin 1.809   time_left 0.334   down 0.154
permutation importance score_margin 0.319   time_left 0.035   down 0.009
```

**A feature can have large SHAP and near-zero permutation importance.** That
happens when it is redundant with another feature: SHAP splits credit between
correlated features, permutation lets the survivor absorb the loss. In our data
that is the normal case, not an edge case — `score_margin` and
`score_differential_post`, `yardline_100` and `yardline`, `ep` and its own
inputs are all near-duplicates. **Report both, and treat a large gap between
them as a redundancy finding rather than a contradiction.**

---

## 3. Partial dependence is how you check a monotonicity claim

The toolkit already recommends `monotone_constraints` for WP in score margin and
time remaining. Partial dependence is how you *verify* the constraint did what
you think — and, when unconstrained, whether the model learned something absurd.

```python
from sklearn.inspection import partial_dependence

pd_ = partial_dependence(model, X, [margin_ix], kind="average", grid_resolution=20)
grid, curve = pd_["grid_values"][0], pd_["average"][0]
assert np.all(np.diff(curve) >= -1e-9), (
    "win probability is not monotone in score margin -- either set "
    "monotone_constraints or explain why this model should not be"
)
```

**A real finding from writing this file:** on an unconstrained fit of a
deliberately monotone data-generating process, the PDP curve came back
`[0.031, 0.098, 0.174, 0.625, 0.861, 0.861]` — **not monotone** under a strict
check, because the last two grid points tie and boosting produces flat steps.
Two consequences worth carrying:

- Use a **tolerance** (`>= -1e-9`), not `> 0`. Tree models produce exact ties by
  construction, and a strict-increase assertion fails on a correct model.
- **A monotone DGP does not give you a monotone model.** If monotonicity is a
  property you want to publish, constrain it at fit time; do not hope for it and
  discover otherwise in review.

`kind="individual"` gives ICE curves — one line per row. Use them when the
average curve looks flat: an average of a strongly positive and a strongly
negative subgroup is a flat line, and ICE is what distinguishes "no effect" from
"two opposite effects".

---

## 4. Slice before you aggregate — the SDV-specific part

A global importance ranking on a season of plays is nearly useless for debugging,
because our failures are stratum-shaped. Compute SHAP once, then aggregate it
**by the slices `metrics-and-gates.md` §1b already tells you to check**:

```python
import polars as pl

# contribs: (n, p+1) from pred_contribs; drop the base column
sv = contribs[:, :-1]
frame = pl.DataFrame({n: sv[:, i] for i, n in enumerate(feature_names)}).with_columns(
    season=pl.Series(seasons), week_bucket=pl.Series(week_buckets), is_home=pl.Series(is_home)
)
by_season = frame.group_by("season", maintain_order=True).agg(
    [pl.col(n).abs().mean().alias(n) for n in feature_names]
)
```

Note `maintain_order=True` — without it `group_by` does not preserve a sort, a
gotcha already recorded in this ecosystem.

**What to look for**, in order of how often it has actually bitten here:

1. **A feature's importance jumping at a rule-era boundary** (2016 for WBB
   halves→quarters, the CFB `ERA_SEASON_CUTS` at 2001/2005/2013/2017). If the
   model leans on a feature only after a rule change, the era split is doing
   work the model should be doing.
2. **A feature that matters only in one week bucket** — usually a
   season-to-date feature that is noise in week 1 and signal in week 12, which
   is a purging problem (`sklearn-xgboost.md` §A2), not an importance finding.
3. **An id-like feature with non-trivial importance.** A `game_id` or a
   `team_id` left in the matrix will happily carry signal and will not
   generalize. This is the cheapest leak detector we have.

---

## 5. Ship the artifact, do not just look at it

An explanation nobody can find is not an explanation. Every model with a
`models/REGISTRY.md` row should also commit a small importance artifact
alongside its model card:

```
cfb/models/ep/  ep.ubj  ep.model_card.md  ep.importance.json
```

`ep.importance.json` holds mean |SHAP| per feature, globally and by season. It
is a few kilobytes, it is diffable, and a change in it between retrains is a
signal — a feature whose importance moves sharply while the gate metric holds
steady means the model found a different route to the same score, which is worth
knowing before it is worth ignoring.

**This is the basis of a proposed `sdv-model-reviewer` lens,
`explainability-present`:** a shipped GBM must have a committed importance
artifact, so "why did the model do that" has a standing answer rather than
needing a fresh investigation each time.

---

## 6. See also

- `metrics-and-gates.md` §1b — the slice list to aggregate over.
- `sklearn-xgboost.md` §J — feature-name ordering, which SHAP output inherits;
  attributions against a booster whose `feature_names` is `None` are positional
  and will silently mislabel every column if the caller's order drifts.
- `failure-modes.md` — for the case where the model is not wrong but a component
  upstream of it did nothing.
