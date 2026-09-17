# Feature construction — transforms, redundancy, interactions, generated features, and model outputs as inputs

> Reference file of the `sdv-modeling` skill. `feature-engineering.md` covers the
> encodings that behave differently on panel-sports data (cyclical, as-of target
> encoding, selection); `competition.md` §1 is the input audit and §7 is
> importance that does not lie. This file covers **building and combining columns
> so more real signal reaches the model**: when a transform helps, what
> correlated columns do to importance, how to find and test interactions, how to
> generate candidates automatically without fooling yourself, and how to feed one
> model's output into another without leaking.

**Every number below was measured on real data** unless it says otherwise:
nflverse `model_pbp` 2023 (train, 35,474 pass/run plays, `GroupKFold` by game)
and 2024 (held-out season, 34,903 plays), predicting `pass` from pre-snap
situation — `down`, `ydstogo`, `yardline_100`, `score_differential`,
`game_seconds_remaining`, `half_seconds_remaining`, `posteam_timeouts_remaining`,
`shotgun`, `no_huddle`, `spread_line`, `wp`. XGBoost 3.4.1 (`max_depth=4`, 300
trees), scikit-learn 1.9.1. Every helper below was re-run against that data to
confirm it fires or stays silent as described (Provenance).

---

## 0. Which learner you use decides whether construction pays

| learner | monotone transform of one column | hand-built interaction | generated candidates |
|---|---|---|---|
| gradient-boosted trees | **no effect** — AUC 0.81118 raw vs 0.81118 with `log1p`/`sqrt`/cube (hist) | small; the trees already split on it | **+0.00006** AUC from the top 10 generated columns |
| logistic / GLM / ridge / RAPM | quantile +0.002, **splines +0.017** | large | **+0.017** — the same gain splines alone give |
| kNN, neural nets (not measured here) | scale and shape matter | expected to help | expected to help |

Two lessons, both measured. **Trees are invariant to monotone transforms**: under
`tree_method="hist"` the AUC was bit-identical, and under `"exact"` it moved in
the fifth decimal (0.810942 → 0.810949) — binning, not information. **Generated
features mostly re-deliver what a flexible basis already gives a linear model**:
the ten best generated pairwise columns lifted logistic regression from 0.7780
to 0.7950, and a spline basis on the raw columns reached 0.7954 with nothing
generated at all.

So before building features, ask what the learner cannot already represent. The
NHL xG work reached the same verdict from the other side: reparameterizations of
geometry the trees had already split on scored 0.7762 against 0.7769, and only
*new information* (shooter handedness, +0.0021 in 16/16 seasons) moved the score
(`tracking-data-cv.md` §8).

---

## 1. The fitted-statistic litmus test

**Rule.** A feature computed from statistics of the data — a mean, a quantile, a
rank, a category vocabulary, a target rate — must be fitted on the training fold
and applied to the validation fold. The test that decides it, credited to the
`probabl-ai` `build-ml-pipeline` skill: **would this feature's value on a
training row change if you computed it on the training rows alone instead of the
whole frame?** If yes, it is a fitted transform and belongs inside the fold.

Row-wise arithmetic (`ydstogo / down`, `log1p(x)`, a clock split) passes and can
be computed once. A percentile rank, quantile bins, `KBinsDiscretizer(strategy=
"quantile")`, a category list, target-aware imputation and any target encoding
fail.

**How big the error is depends on the statistic.** A full-frame percentile rank of
`ydstogo` moved training-row values by at most **0.0016** against the
training-only rank — negligible at 35k rows. A target encoding on a sparse entity
is not negligible; that case is measured in `feature-engineering.md` §2. The test
is about correctness first, so apply it even when the magnitude is small: the same
code on a 400-row hackathon frame is not small.

```python
import numpy as np
import polars as pl


def assert_fit_in_fold(feature_fn, frame, train_mask, key="row_id", atol=1e-12):
    """Fail when a feature depends on rows outside the training subset.

    feature_fn(df) -> pl.Series aligned with df. A stateless (row-wise) feature
    gives identical training-row values whether computed on the training rows
    or the full frame. A fitted one does not, and must go inside the fold.
    """
    full = frame.with_columns(feature_fn(frame).alias("_v"))
    train = frame.filter(pl.Series(train_mask))
    part = train.with_columns(feature_fn(train).alias("_v"))
    j = part.select(key, "_v").join(full.select(key, pl.col("_v").alias("_v_full")), on=key)
    assert j.height == train.height, "key did not match every training row"
    diff = (j["_v"] - j["_v_full"]).abs().max()
    assert diff is None or diff <= atol, (
        f"feature changes by up to {diff:.3g} on training rows when computed on the "
        "full frame: it is fitted from data and must be fitted inside each fold"
    )
```

---

## 2. Transformations — for the learners that need them

A transform earns its place only for learners that are not already invariant to
it (§0). For a linear or GLM model, prefer a **spline basis** over hand-picked
`log`/`sqrt`: it lets the data choose the shape, and it measured +0.017 AUC where a
quantile-normal transform gave +0.002.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import SplineTransformer

# Fitted per fold by the Pipeline: knot positions come from the training rows.
spline_logit = make_pipeline(
    SplineTransformer(n_knots=6, degree=3),
    LogisticRegression(max_iter=4000),
)
```

- `SplineTransformer` places knots from the training data — evenly between the
  training min and max by default (`knots="uniform"`), at training quantiles with
  `knots="quantile"` — so it fails §1 and must live in the `Pipeline`, never be
  pre-applied.
- `PowerTransformer(method="yeo-johnson")` handles zeros and negatives;
  Box-Cox needs strictly positive input.
- `QuantileTransformer` flattens outliers but destroys the spacing a linear model
  might have used — here it gained 0.002 against the spline basis's 0.017.
- For a monotone known-sign relationship in a tree, use
  `monotone_constraints` instead of a transform (`sklearn-xgboost.md`).

---

## 3. Redundancy and covariation — correlated columns split the credit

**Trap.** Two columns carrying the same information share the model's credit, so
**each looks less important than the information is**, and a selection step can
drop both.

**Measured.** Adding a near-copy of `ydstogo` (the column plus noise of sd 0.01):

| | permutation importance (Δ AUC) |
|---|---|
| `ydstogo`, alone | **0.0657** |
| `ydstogo`, with a copy present | **0.0119** |
| the copy | 0.0265 |

The original's importance fell **5.5×**, and XGBoost's total gain split almost
evenly (9,799 vs 10,433). Alone, `ydstogo` ranked third of eleven; with the copy
present, neither column looks like it.

**Upstream model outputs are the usual source.** `wp` is a fitted model's output,
and its Spearman correlation with `score_differential` — one of its own inputs —
was **0.963**, the only pair above 0.7 in the set. §6 has the rest of that story.

**Fix.** Cluster before interpreting or selecting, then keep one representative
per cluster or permute and ablate each cluster as a unit (`competition.md` §7).
For linear models, check the variance inflation factor as well: correlation
misses a column that is a combination of several others.

```python
import numpy as np
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr


def correlation_clusters(X, names, max_abs_rho=0.7):
    """Groups of columns whose |Spearman rho| links them above max_abs_rho."""
    X = np.asarray(X, float)
    if X.shape[1] < 2:
        return []
    rho = spearmanr(X, nan_policy="omit").correlation
    dist = 1.0 - np.abs(np.nan_to_num(rho))
    np.fill_diagonal(dist, 0.0)
    Z = hierarchy.linkage(squareform(dist, checks=False), method="average")
    labels = hierarchy.fcluster(Z, t=1.0 - max_abs_rho, criterion="distance")
    return [[names[i] for i in np.flatnonzero(labels == c)]
            for c in np.unique(labels) if (labels == c).sum() > 1]


def variance_inflation(X):
    """VIF per column: 1 / (1 - R^2) regressing each column on the others."""
    X = np.asarray(X, float)
    X = (X - X.mean(0)) / np.where(X.std(0) == 0, 1.0, X.std(0))
    out = []
    for j in range(X.shape[1]):
        others = np.delete(X, j, axis=1)
        beta, *_ = np.linalg.lstsq(others, X[:, j], rcond=None)
        resid = X[:, j] - others @ beta
        r2 = 1.0 - resid.var() / X[:, j].var() if X[:, j].var() > 0 else 0.0
        out.append(np.inf if r2 >= 1.0 else 1.0 / (1.0 - r2))
    return np.array(out)
```

Average linkage with `t = 1 − max_abs_rho` is a heuristic, not a guarantee: a
cluster can hold a pair below the threshold if both link strongly to a third
column. VIF above ~10 is the usual flag; it assumes a linear relationship.

---

## 4. Interactions — find them, then test whether they matter

**Find them with SHAP interaction values.** XGBoost computes them natively; no
`shap` dependency is needed. Each prediction's contribution splits into main
effects and pairwise terms, so the mean absolute off-diagonal term ranks pairs.

```python
import numpy as np
import xgboost as xgb
from itertools import combinations


def interaction_pairs(booster, X, names, top=5):
    """Rank feature pairs by mean |SHAP interaction| (logit units, both halves)."""
    phi = booster.predict(xgb.DMatrix(np.asarray(X, float)), pred_interactions=True)
    M = np.abs(phi[:, :-1, :-1]).mean(axis=0)      # drop the bias row/column
    pairs = [(2.0 * M[i, j], names[i], names[j])
             for i, j in combinations(range(len(names)), 2)]
    return sorted(pairs, reverse=True)[:top]
```

Measured top pairs: `down × ydstogo` ≈0.20, `game_seconds_remaining × wp` ≈0.13,
`down × shotgun` ≈0.10 — stable in order across two 3,000-row samples, moving
±0.01 in size. Cost grows with features squared, so subsample rows before calling it.

**Test whether they matter with interaction constraints.** Ranking is not
evidence. Refit with **no interactions allowed** and compare held-out skill:

| model | 2024 AUC |
|---|---|
| unconstrained | **0.8112** |
| additive (every feature in its own group) | 0.7951 |
| additive + `down × ydstogo` only | 0.7997 |

Interactions are worth **0.016 AUC** here, and the single top pair recovers about
**29%** of that gap — informative, and a warning that the top-ranked pair is not
the whole story.

```python
import json


def additive_model(params, n_features, allowed_pairs=()):
    """XGBClassifier restricted to main effects plus the listed index pairs."""
    paired = {i for p in allowed_pairs for i in p}
    groups = [list(p) for p in allowed_pairs] + [[i] for i in range(n_features)
                                                  if i not in paired]
    # XGBoost 3.4.1 sklearn API + a NumPy X: a Python list of int lists raises
    # "Constrained features are not a subset of training data feature names".
    # A JSON string works, as do column-name lists with a DataFrame.
    return xgb.XGBClassifier(**{**params, "interaction_constraints": json.dumps(groups)})
```

**Found an interaction that matters? A linear model needs it built explicitly;**
the trees already have it. That is where the generated `down/ydstogo` column in
§5 came from.

---

## 5. Generated features — candidates, a null bar, and a later season

Automatic generation is cheap: 11 columns give 165 pairwise `×`, `−`, `÷`
candidates. The danger is selection — with enough candidates something always
looks like a gain.

**Screen every candidate against a null bar built the same way.** Apply the same
operators to columns permuted independently across rows (no information, same
marginals), score those, and require a real candidate to beat the **maximum** null
gain, not a p-value on one test.

**Measured** (logistic regression, 3-fold `GroupKFold` gain over the base set):

| | CV gain |
|---|---|
| best null candidate (all 165 scored) | **0.00005** |
| `down / ydstogo` | **0.0070** |
| `game_seconds_remaining × wp` | 0.0041 |
| `score_differential × game_seconds_remaining` | 0.0030 |

The null maximum depends on the permutation draw — 0.00005 here, 0.00013 on a
second draw — but stays about two orders of magnitude below the useful gains. The winners
cleared it by more than 50×, and the best candidate's gain on the 2024 season
(**0.0094**) exceeded its CV screen: real signal, not selection optimism.

**The bar screens out noise, not weak columns.** 58 of the 165 real candidates
cleared it: 17 by at least 0.001 AUC, the other 41 by less. Many of the survivors
share columns, so cluster them (§3) as well. Rank what survives, keep the few with material gains, and confirm
them on a later season. When screened gains sit within a few multiples of the
null maximum, treat them as noise.

```python
import numpy as np
from itertools import combinations


def pairwise_candidates(X, names):
    """Row-wise x, -, / for every column pair. Stateless, so §1 is satisfied."""
    X = np.asarray(X, float)
    cols, labels = [], []
    for i, j in combinations(range(X.shape[1]), 2):
        a, b = X[:, i], X[:, j]
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(b == 0, np.nan, a / b)
        for op, v in (("*", a * b), ("-", a - b), ("/", ratio)):
            cols.append(v)
            labels.append(f"{names[i]}{op}{names[j]}")
    return np.column_stack(cols), labels


def screen_against_null(score_gain, X, names, seed=0):
    """Keep candidates whose gain beats the best gain of permuted-input candidates.

    score_gain(extra_column) -> CV gain over the base set, using the grouped
    splitter. Returns (kept [(label, gain)], null_max). Every null candidate is
    scored -- all three operators -- because the null maximum is only a bar if it
    ranges over the same kinds of candidate as the real set.
    """
    rng = np.random.default_rng(seed)
    real, labels = pairwise_candidates(X, names)
    Xp = np.asarray(X, float).copy()
    for c in range(Xp.shape[1]):
        Xp[:, c] = rng.permutation(Xp[:, c])
    null, _ = pairwise_candidates(Xp, names)
    null_gains = [score_gain(null[:, k]) for k in range(null.shape[1])]
    null_max = float(np.max(null_gains)) if null_gains else 0.0
    gains = [score_gain(real[:, k]) for k in range(real.shape[1])]
    kept = sorted(((labels[k], g) for k, g in enumerate(gains) if g > null_max),
                  key=lambda t: -t[1])
    return kept, null_max
```

`score_gain` must use the same grouped splitter as the final model, and anything
it fits (a scaler, an imputer) must be fitted inside its folds.

### Libraries, and what each is actually for

| library | licence | what it generates | caveat, verified 2026-09-17 |
|---|---|---|---|
| `skrub` 0.10.1 | BSD-3 | `AggJoiner` / `AggTarget` aggregate a related table onto rows; `TableVectorizer` encodes mixed columns | the aggregators are estimators, so they fit in-fold — the right shape for "team's average X" features |
| `featuretools` 1.31.0 | BSD-3 | deep feature synthesis across related tables | `dfs(cutoff_time=...)` is its as-of mechanism — **pass it**, or aggregates include the future. Fails to import in a fresh env: its `woodwork` dependency imports `pkg_resources`, removed in setuptools 81, so pin `setuptools<81` |
| `autofeat` 2.1.3 | MIT | nonlinear transforms + products, then L1 selection | built for linear models, which §0 says is where generation pays |
| `OpenFE` 0.0.12 | MIT | expand-and-reduce generation for GBDTs | last commit 2024-05; treat as unmaintained |

For trees, §0 says expect little. The measured ten generated columns added
**0.00006** AUC to XGBoost.

---

## 6. Model outputs as inputs — nested out-of-fold, or the downstream model learns a lie

Feeding one model's prediction into another — xG into a win-probability model,
an expected-pass rate into a play-calling model, a rating into a pregame spread —
is stacking with a different target, and it leaks the same way.

**Trap.** An upstream model scored on the same rows it was fitted on is far more
accurate there than it will ever be on new data. The downstream model learns to
trust that score, and its own cross-validation cannot see the problem, because
the leak was baked into the column before the downstream split.

**Measured.** Upstream: a deep XGBoost (`max_depth=8`, 600 trees) on
team/opponent/week dummies plus the situation, predicting `pass`. Downstream:
logistic regression on the situation plus the upstream score.

| upstream score on training rows | upstream AUC there | downstream 2023 CV AUC | downstream 2024 AUC |
|---|---|---|---|
| **in-sample** (fitted on all training rows) | 0.991 | **0.995** | **0.792** |
| **out-of-fold** (same game groups) | 0.801 | 0.808 | **0.809** |

(2024 upstream scores are the fold-averaged predictions of the five fold models in
both rows.) The in-sample version reported **0.995** and delivered **0.792** — worse
on the new season than the out-of-fold version: its weights were fitted to an
upstream score far more accurate than that score is at prediction time. The
out-of-fold version's CV (0.808) predicted its test (0.809).

**Rule.** Upstream predictions for training rows are **out-of-fold, using the same
groups** as the downstream split. Upstream predictions for test rows are the
**average of the fold models**. Measured against a single refit on all training
rows: upstream 2024 AUC 0.806 vs 0.799, downstream 0.809 vs 0.806. The refit was
not more confident here (mean |logit| 1.97 against 2.00 out-of-fold); the gain is
the averaging of five models.

```python
import numpy as np
from sklearn.model_selection import GroupKFold


def oof_upstream(make_model, X, y, groups, X_test, n_splits=5):
    """Upstream scores safe to use as a downstream feature.

    Training rows get out-of-fold scores; test rows get the mean of the fold
    models' scores, so both come from models that never saw the row.
    """
    X, y, X_test = np.asarray(X), np.asarray(y), np.asarray(X_test)
    oof = np.full(len(y), np.nan)
    test = np.zeros(len(X_test))
    for tr, va in GroupKFold(n_splits=n_splits).split(X, y, groups):
        model = make_model().fit(X[tr], y[tr])
        oof[va] = model.predict_proba(X[va])[:, 1]
        test += model.predict_proba(X_test)[:, 1] / n_splits
    assert not np.isnan(oof).any(), "some training rows never received an OOF score"
    return oof, test


def assert_upstream_not_in_sample(train_score, oof_score, y, metric, max_gap=0.02,
                                  higher_is_better=True):
    """Fail when the score fed downstream is far better than its OOF counterpart.

    `higher_is_better=False` for losses (log loss, Brier), so an in-sample score
    with a lower loss still registers as a positive gap.
    """
    gap = metric(y, train_score) - metric(y, oof_score)
    if not higher_is_better:
        gap = -gap
    assert gap <= max_gap, (
        f"upstream score is {gap:.3f} better on training rows than out-of-fold: "
        "it was scored in-sample and will leak into the downstream fit"
    )
```

**Two more checks for published upstream models** — the ones you load rather
than fit (`wp`, `ep`, `xpass`, `cp` in nflverse and sdv-py):

- **Training window.** A published model fitted on seasons that include your
  evaluation season is in-sample for those rows. Read its model card or fitting
  script and evaluate only on seasons it never saw (`competition.md` §2).
- **Redundancy with its inputs.** `wp` correlated 0.963 with `score_differential`
  (§3). Adding a model output alongside its own inputs splits importance and
  rarely adds information; the output is most useful when it encodes inputs the
  downstream model does *not* have.

The Bayesian analogue — combining models by predictive weights rather than by
feeding outputs forward — is the installed `model-evaluation` skill
(ArviZ LOO and stacking weights).

---

## 7. Missing values — leak, signal, or noise

**Missingness can be the leak.** `air_yards` is null on almost every run and
filled on most passes, so `air_yards.is_null()` alone scored **AUC 0.941** for predicting
`pass` — a post-play field whose *presence* encodes the answer. `competition.md`
§1b's single-feature ceiling catches it; run it over missingness indicators too,
not only the values.

**Missingness can be signal.** When values are missing not at random, keep the
fact that they were missing. Measured by hiding `shotgun` on half of its shotgun
plays (a formation a charting feed misses), then filling with the mean:

| learner | NaN kept | mean-imputed | mean-imputed + indicator |
|---|---|---|---|
| XGBoost | 0.8111 | 0.8111 | 0.8112 |
| logistic | — | **0.7668** | **0.7780** |

Trees route NaN down a learned branch and barely noticed. The linear model lost
0.011 AUC to imputation and recovered all of it with an indicator. **For trees,
leave NaN in; for linear models, impute inside the Pipeline with
`SimpleImputer(add_indicator=True)`.**

**Sentinels are missing values in disguise.** `-1`, `0`, `99`, `999` standing in
for "unknown" look like real numbers to every learner.

```python
import numpy as np


def sentinel_candidates(values, min_share=0.01, peak=5.0,
                        candidates=(-999, -99, -1, 0, 99, 999)):
    """Common codes separated from the other values by a gap, or spiking above
    every populated neighbour -- likely 'unknown' stand-ins."""
    v = np.asarray(values, float)
    v = v[~np.isnan(v)]
    out = []
    for s in candidates:
        share = float(np.mean(v == s)) if v.size else 0.0
        if share < min_share:
            continue
        others = v[v != s]
        # a gap, not just the edge: the largest real value is not a sentinel
        outside = others.size == 0 or s < others.min() - 1 or s > others.max() + 1
        near = [np.mean(v == k) for k in (s - 2, s - 1, s + 1, s + 2) if np.any(v == k)]
        spike = not near or share > peak * max(near)
        if outside or spike:
            out.append((s, round(share, 4)))
    return out
```

A flagged value is a question, not a verdict: `0` timeouts remaining is real.

---

## 8. The predict-time smoke test — rows requested equal rows returned

**Trap.** A feature built from history — a lag, a rolling mean, a
previous-play value — is computed on the rows you have. At training time that is
the whole season; at prediction time it may be a slice with no history in front
of it. The first rows of the slice get nulls, a `drop_nulls` removes them, and
the prediction count quietly shrinks.

**Measured.** A previous-play `pass` lag on 2024 second halves: **17,489** rows
requested; built on the second-half slice and null-dropped, **17,204** returned —
**285 lost**, one at the start of each game's slice. Built on full game history
first, then sliced: all 17,489.

The idea is the `probabl-ai` `smoke-test-ml-pipeline` skill's: fit on part of the
real data, predict a later slice that deliberately has no history in front of it,
and assert structure before quality.

```python
from collections import Counter

import numpy as np


def assert_predict_rows_preserved(predict_fn, requested, id_col, max_ratio=3.0,
                                  score_fn=None, y_true=None, cv_error=None):
    """Hard: one prediction per requested row. Soft: error not far above CV.

    predict_fn(requested) -> (ids, predictions). `score_fn` is an ERROR (lower is
    better), compared with the cross-validated error of the same model.
    """
    ids, preds = predict_fn(requested)
    want = Counter(requested[id_col].to_list())
    got = Counter(np.asarray(ids).tolist())
    missing, extra = want - got, got - want      # multiset differences
    assert len(ids) == len(preds) == requested.height and not missing and not extra, (
        f"{requested.height} rows requested, {len(ids)} ids and {len(preds)} "
        f"predictions returned; missing {list(missing.elements())[:3]}, extra "
        f"{list(extra.elements())[:3]} -- history-based features were computed "
        "on the prediction slice, or rows were duplicated"
    )
    preds = np.asarray(preds, float)
    assert np.isfinite(preds).all(), "non-finite predictions: a feature is NaN at predict time"
    if score_fn is not None:
        assert y_true is not None and cv_error is not None, (
            "score_fn needs y_true and cv_error to compare against"
        )
        err = score_fn(y_true, preds)
        assert err <= max_ratio * cv_error, (
            f"predict-time error {err:.4f} is over {max_ratio}x the CV error "
            f"{cv_error:.4f}: features differ between fit and predict"
        )
```

The row assertion is the one that catches this bug; the error ratio catches the
second failure, where the count is right but features are silently null or
defaulted at prediction time.

---

## 9. Checklist

1. **Learner first** (§0). Trees: skip transforms, expect little from generated
   columns, spend the effort on new information. Linear/GLM: splines, then
   interactions, then generation.
2. **Every fitted statistic inside the fold** — run `assert_fit_in_fold` on any
   feature you are unsure of (§1).
3. **Cluster correlated columns** before reading importance or selecting (§3).
4. **Rank interactions, then test them** with an additive refit (§4).
5. **Generated candidates must beat a permuted-input null maximum**, and survive a
   later season (§5).
6. **Upstream model outputs are out-of-fold with the same groups**, and published
   ones never saw the evaluation season (§6).
7. **Missingness**: check indicators for leaks, keep NaN for trees, add indicators
   for linear models, hunt sentinels (§7).
8. **Smoke-test prediction on a slice with no history** before trusting a
   pipeline (§8).

---

## Provenance

- All tables in §0–§8: nflverse `model_pbp` 2023/2024 from the local
  `nfl-data` checkout, measured 2026-09-17 with XGBoost 3.4.1 and scikit-learn
  1.9.1. The task, features and splits are stated at the top of this file; the
  helpers in §1–§8 were executed against the same frames and checked to fire on
  the failure and stay silent on the fix.
- The §1 litmus test and the §8 row-count smoke test are adapted from
  `probabl-ai/skills` (`build-ml-pipeline`, `smoke-test-ml-pipeline`; BSD-3,
  scikit-learn/skrub maintainers). Ideas only; no text copied. That skill set
  is not installed globally: it triggers on any preprocessing code and mandates
  skrub DataOps, pixi and a scratch-file workflow, which conflicts with SDV's
  polars + uv pipelines.
- NHL reparameterization and handedness figures: `tracking-data-cv.md` §8.
- Library versions, licences and the `featuretools` import failure: checked
  against PyPI and GitHub, 2026-09-17.
