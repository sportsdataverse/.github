# Competition play — Kaggle, hackathons, and any leaderboard

> Reference file of the `sdv-modeling` skill. Covers what changes when the
> objective is a **leaderboard score under a deadline** rather than a model that
> will be retrained and published. Most of it is the same discipline as
> production modeling pointed at a different failure: in production a leak ships
> a wrong number; in a competition it ships a wrong *submission*, and the public
> leaderboard rewards it until the private one doesn't.

A generic competition recipe assumes i.i.d. rows and a test set drawn from the
same distribution as train. Sports data breaks both: rows cluster inside games,
games inside seasons, and the hidden test set is usually *later in time* or
*different games*. Every public "Kaggle pipeline" skill surveyed on 2026-09-16
used a shuffled `StratifiedKFold`, and the most-installed one also early-stopped
on the same fold it scored and built its stacking test features from a full
refit. Each is corrected below with a detection test.

Every entry: **the trap · why it never errors · the detection test · a real
citation** where this ecosystem has one.

**Contents**

0. Time-box: what actually wins
1. Input signal audit — clean, meaningful inputs before any tuning
2. Validation that tracks the private leaderboard
3. The out-of-fold pipeline, corrected
4. Early stopping without grading its own homework
5. Stacking and blending without meta-leakage
6. Seed and fold bagging — measure the variance first
7. Feature selection that does not lie
8. Augmentation — label-preserving and in-fold only
9. Tuning — where it pays and where it cannot
10. Post-processing to the metric
11. Claiming an improvement honestly
12. Pre-submission checklist

---

## 0. Time-box: what actually wins

In a fixed-deadline setting the order of work matters more than any single
technique. The durable ranking, strongest first:

1. **A validation scheme that tracks the private leaderboard** (§2). Without it
   every later decision is noise-fitting.
2. **Inputs that carry information the model does not already have** (§1). On
   the NHL 5v5 xG corpus, ten feature directions were searched; nine that
   *re-expressed* existing geometry scored within ±0.001 AUC, and the only one
   that helped (+0.0021, 16/16 seasons) added information the feed did not
   carry — shooter handedness.
3. **The learner and its capacity.** Usually last. Doubling tree depth on that
   same corpus moved LOSO AUC by **+0.0007**; capacity was not the constraint.
4. **Ensembling and seed bagging** — reliable small gains *after* 1–3 are done.

Ship a **dumb baseline in the first hour** (league average, a single logistic
regression, or the provided benchmark) and score it through the full validation
path. It proves the path works end to end, and it is the number every later
"improvement" has to beat on the same folds.

---

## 1. Input signal audit — clean, meaningful inputs before any tuning

Tuning a model on a leaked or noisy feature optimizes the leak. Run this audit
**before** the first hyperparameter search and again whenever a feature is added.

### 1a. The shuffled-target sanity check

**Trap.** The pipeline itself leaks — a target-derived column, a fold-crossing
join, an index that encodes the label — so the model scores well on *any* target.

**Why invisible.** A good score is the expected outcome; nobody investigates
success.

**Detection test.** Permute the target **globally** — across the whole frame —
and rerun the exact validation path with the *original* groups. With the signal
destroyed the score must fall to chance. If it does not, the leak is in the
pipeline, not the features.

**Permute globally, never within groups.** Within-group permutation is the
intuitive choice and it is wrong: it preserves each group's target rate, so any
honest group-level feature (team strength, a player's season rate) still predicts
the permuted target, and a clean pipeline "fails". Measured on a grouped frame
with one honest group-level feature under `GroupKFold`: real target **0.733** AUC,
within-group permuted **0.734** (a false alarm), global permutation **0.487**
(chance). With one row per group, within-group permutation is also a pure no-op.

```python
import numpy as np

def assert_shuffled_target_is_chance(score_fn, X, y, groups, chance, tol,
                                     n_repeats=3, seed=0):
    """score_fn(X, y, groups) -> validation score through the REAL pipeline.

    Permutes y GLOBALLY, destroying every feature/target link including group
    base rates, while `groups` is passed unchanged so the splitter still runs.
    Averages a few permutations so one lucky shuffle cannot pass or fail it.
    A score that stays above chance means the pipeline -- not the features --
    is supplying the signal.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(y)
    s = float(np.mean([score_fn(X, rng.permutation(y), groups)
                       for _ in range(n_repeats)]))
    assert abs(s - chance) <= tol, (
        f"shuffled-target score {s:.4f} is not chance ({chance}±{tol}): the "
        "pipeline leaks the label independent of the features"
    )
    return s
```

### 1b. The single-feature leak ceiling

**Trap.** One column is a near-copy of the target: a post-event field, an outcome
flag, a score that updates *after* the play.

**Why invisible.** It becomes the top feature, which reads as "found the signal".

**Detection test.** Score every numeric feature **alone** against the target.
Calibrate the ceiling from the honest features first — never pick a round number.

```python
from sklearn.metrics import roc_auc_score

def assert_no_single_feature_leak(df, target, features, ceiling):
    """Fails if any single feature separates the target better than `ceiling`.

    Orientation-free: max(auc, 1-auc), so a leak that runs backwards still fires.
    Set `ceiling` just above the best HONEST feature, measured, not guessed.
    """
    y = df[target].to_numpy()
    offenders = {}
    for f in features:
        x = df[f].to_numpy()
        ok = ~np.isnan(x.astype(float))
        if ok.sum() < 50 or len(np.unique(y[ok])) < 2:
            continue
        auc = roc_auc_score(y[ok], x[ok])
        auc = max(auc, 1 - auc)
        if auc > ceiling:
            offenders[f] = round(auc, 4)
    assert not offenders, f"single-feature leak above {ceiling}: {offenders}"
```

**Real citation.** NHL xG (2026-09-03). The ceiling was first set at a guessed
0.62 and fired on the two most legitimate features in the game — `shot_distance`
scored **0.697** alone and `abs_y` **0.679**. Recalibrated to **0.75** by
measuring the honest features. The same guard would have caught the real leak:
`home_score`/`away_score` are recorded *after* the event on 97.9% of goal rows,
and a naive `score_diff` scored **0.8495** LOSO against a **0.7769** control.
Fixed by lagging the score within game.

**The pooled ceiling fires on honest physics; stratify it.** A feature can beat
the best honest feature *pooled* because it proxies shot type, not the outcome.
hoopsq (2026-09-17): ball height at release scored AUC **0.626** alone, above
distance's 0.602 — and it is not a leak. Within distance strata it collapses to
shot-type information: 0.607 under 4 ft, 0.659 at 4–10 ft, **0.532** at 10–22 ft,
**0.507** on threes. A real post-outcome column stays high inside every stratum.
Run the pooled test first, then the stratified one on anything it flags, and
commit the stratified numbers so the next reviewer does not re-litigate them.

```python
def single_feature_auc_by_stratum(df, target, feature, strata_col, bins):
    """Orientation-free AUC of one feature within bins of the dominant honest feature.

    A leak stays high in every bin; a shot-type proxy falls to ~0.5 in the bins
    where the type is fixed. Returns {bin_label: auc}.
    """
    import numpy as np, pandas as pd
    from sklearn.metrics import roc_auc_score
    out = {}
    cut = pd.cut(df[strata_col], bins=bins)
    for label, sub in df.groupby(cut, observed=True):
        y, x = sub[target].to_numpy(), sub[feature].to_numpy(float)
        ok = ~np.isnan(x)
        if ok.sum() < 50 or len(np.unique(y[ok])) < 2:
            continue
        auc = roc_auc_score(y[ok], x[ok])
        out[str(label)] = round(max(auc, 1 - auc), 3)
    return out
```

### 1c. Every new boolean must actually fire on real data

**Trap.** A flag built on a field that is constant, or on a window that can
never be satisfied, is all-False and contributes nothing — silently.

**Detection test.** `assert df[flag].sum() > 0` on the *real* competition data,
and print the True-count next to the feature's importance.

**Real citation.** hoopsq (SkillCorner ACB, 2026-09-15): `fouls.isTeam` and
`fouls.isTechnical` are False on **all 443** fouls in the 10 games, and a
"within 20 s of a timeout" window can never fire because video-frame gaps
around a timeout are ≥ 80 s.

### 1d. Ids and joins that point the wrong way in time

**Trap.** An event-linking id that refers to the *next* or *previous* event
rather than the one you think — so a "before the shot" feature is built from
something that happened after it.

**Why invisible.** The feature is predictive, and the join key looks right.

**Detection test.** For every feature built from a separate event table, assert
that **every consumed source row's frame/timestamp precedes the target event's
start** — on real data, not a fixture.

```python
import polars as pl

def assert_sources_precede_event(consumed, event_start, key="event_id"):
    """consumed: rows [key, source_frame] actually used to build the feature.
    event_start: rows [key, start_frame] for the event being predicted.

    Checks EVERY consumed row. An inner join would silently drop rows with no
    matching event, and a null frame makes the comparison null, which a filter
    also drops -- either way the guard passes without verifying those rows.
    """
    j = consumed.join(event_start, on=key, how="left")
    unmatched = j.filter(pl.col("start_frame").is_null())
    assert unmatched.height == 0, (
        f"{unmatched.height} consumed rows have no event start (missing key or "
        "null start_frame): their ordering cannot be verified"
    )
    no_frame = j.filter(pl.col("source_frame").is_null())
    assert no_frame.height == 0, f"{no_frame.height} consumed rows have a null source_frame"
    bad = j.filter(pl.col("source_frame") >= pl.col("start_frame"))
    assert bad.height == 0, (
        f"{bad.height} feature rows consume a source at or after the event start"
    )
```

**Real citation.** hoopsq: `timeouts.chanceId` points **backwards** — it names
the chance the timeout interrupted (56 of 65 timeout frames fall *after* that
chance ends, 0 before it starts). An `after_timeout` flag built on it tagged
55 shots, **51 made** (the conceding team calls timeout), and produced a
**−0.012 log-loss "win" that was pure outcome leakage**.

### 1e. Ask what the rows ARE, not how many

**Trap.** A measured anomaly — a spike of negative values, an era-shaped gap —
gets a plausible cause attached and acted on without checking the mechanism.

**Detection test.** Before dropping, imputing or filing anything, run one
`group_by` over the category column on the violating subset and read it.

**Real citation.** cfbfastR-cfb-data #67 (retracted): 49,535 rows of
`start.distance == -1` looked like a corrupt upstream sentinel leaking into
EP/WP. One `group_by("type.text")` showed they were extra points and two-point
tries — a **deliberate** sentinel the parser sets, forty lines from code already
read. See `failure-modes.md` for the component-level version of this rule.

### 1f. Adversarial validation — is test drawn from train's distribution?

**Trap.** The hidden test set differs systematically from train (later season,
rule change, new venues, different tracking vendor). CV on train looks great;
the leaderboard does not.

**Why invisible.** CV cannot see a shift it never samples.

**Detection test.** Label train rows 0 and test rows 1, train a classifier to
tell them apart, and read the AUC. **~0.5 means no detectable shift.** Well
above 0.5 means drift — and the top features of *that* model are exactly the
ones whose distribution moved.

```python
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from xgboost import XGBClassifier

def adversarial_validation(X_train, X_test, max_auc=0.60, seed=0):
    """Returns (auc, model). Raises if train and test are separable.

    Uses a plain stratified split ON PURPOSE: here the rows are the unit being
    compared and there is no target to leak. Group structure does not apply.
    """
    X = np.vstack([X_train, X_test])
    is_test = np.r_[np.zeros(len(X_train)), np.ones(len(X_test))]
    clf = XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1,
                        subsample=0.8, random_state=seed, n_jobs=-1)
    p = cross_val_predict(clf, X, is_test,
                          cv=StratifiedKFold(5, shuffle=True, random_state=seed),
                          method="predict_proba")[:, 1]
    auc = roc_auc_score(is_test, p)
    clf.fit(X, is_test)
    assert auc <= max_auc, (
        f"adversarial AUC {auc:.3f} > {max_auc}: train and test are separable; "
        "inspect clf.feature_importances_ for the drifting columns"
    )
    return auc, clf
```

**What to do when it fires.** In rough order: drop or de-trend the drifting
columns if they are not causal; **validate on the train rows most like test**
(sort by the adversarial probability and hold out the top slice); or reweight
train by `p / (1 - p)` so the fit emphasizes test-like rows. Do not "fix" it by
tuning until CV agrees with the leaderboard — that is fitting the public split.

### 1g. Duplicates and near-duplicates across the split

A row appearing in both train and validation (re-broadcast events, a game
scraped twice, the same shot under two player-id aliases) inflates CV silently.
Hash the defining columns and assert zero overlap between folds; for entities,
resolve aliases first. hoopsq found **9 players carrying two ids**
(`player_id_aliases.csv`) — an entity-level near-duplicate that splits one
player's history across folds.

---

## 2. Validation that tracks the private leaderboard

**Trap.** A fast shuffled K-fold agrees with itself and disagrees with the
leaderboard, because it samples the same games on both sides.

**Rule.** Choose the splitter to **mirror how the hidden test was drawn**:

| Hidden test is… | Splitter |
|---|---|
| different games, same season | `GroupKFold(groups=game_id)` |
| a later season | leave-one-season-out, or `TimeSeriesSplit` over seasons |
| later in time within a season | forward-chaining with an embargo (`resampling.md`, purged CV in `sklearn-xgboost.md` §A) |
| different teams/players entirely | `GroupKFold(groups=team_or_player_id)` |
| unknown | adversarial validation (§1f) to find out, then choose |

**Trust CV over the public leaderboard when they disagree, if the CV is the
right shape.** The public LB is usually a small, noisy slice; tuning to it is
fitting that slice. Track **CV-vs-public correlation** across submissions: if
improvements in CV reliably move public in the same direction, both are
measuring the same thing; if they do not, suspect the CV splitter first, the
public slice's size second.

**Detection test — does CV rank submissions the way the leaderboard does?**

```python
from scipy.stats import spearmanr

def assert_cv_tracks_leaderboard(cv_scores, lb_scores, min_rho=0.6):
    """Parallel lists, one entry per submitted variant, same metric direction."""
    assert len(cv_scores) >= 5, "need >= 5 submissions for a rank correlation"
    rho, p = spearmanr(cv_scores, lb_scores)
    assert rho >= min_rho, (
        f"CV and leaderboard disagree on rank (rho={rho:.2f}): revisit the "
        "splitter before tuning further"
    )
    return rho
```

**Real citation.** hoopsq scored every candidate **leave-one-game-out** across
10 games because the evaluation unit is the game; the NHL xG search used
**leave-one-season-out** across 16 seasons because the production model is
applied to a season it has not seen.

---

## 3. The out-of-fold pipeline, corrected

Every downstream step — stacking, blending, threshold tuning, calibration —
consumes out-of-fold (OOF) predictions. Build them once, correctly.

```python
import numpy as np
from sklearn.model_selection import GroupKFold
from xgboost import XGBClassifier

def oof_fit_predict(X, y, groups, X_test, params, n_splits=5, inner_frac=0.15,
                    seed=0):
    """OOF predictions for train + fold-averaged predictions for test.

    Three corrections to the common public recipe:
      1. GroupKFold on the real grouping, never a shuffled StratifiedKFold.
      2. Early stopping on an INNER split of the training fold, so the outer
         fold is scored by a model that never saw it (see section 4).
      3. Test predictions are the AVERAGE of the fold models -- the same models
         that produced OOF -- never a separate full refit (see section 5).
    """
    X, y, groups = np.asarray(X), np.asarray(y), np.asarray(groups)
    oof = np.full(len(X), np.nan)
    test = np.zeros(len(X_test))
    rng = np.random.default_rng(seed)
    for tr, va in GroupKFold(n_splits=n_splits).split(X, y, groups):
        tr_groups = np.unique(groups[tr])
        inner = set(rng.choice(tr_groups, max(1, int(len(tr_groups) * inner_frac)),
                               replace=False))
        is_inner = np.isin(groups[tr], list(inner))
        fit_idx, stop_idx = tr[~is_inner], tr[is_inner]
        # Merge rather than pass twice: a caller's params containing random_state
        # or early_stopping_rounds would otherwise raise a duplicate-keyword
        # TypeError at construction.
        model = XGBClassifier(**{**params, "early_stopping_rounds": 50,
                                 "random_state": seed})
        model.fit(X[fit_idx], y[fit_idx],
                  eval_set=[(X[stop_idx], y[stop_idx])], verbose=False)
        oof[va] = model.predict_proba(X[va])[:, 1]
        test += model.predict_proba(X_test)[:, 1] / n_splits
    assert not np.isnan(oof).any(), "some rows never landed in a validation fold"
    return oof, test
```

**API note, verified on xgboost 3.3.0.** `early_stopping_rounds` is a
**constructor** argument. Passing it to `.fit()` raises
`TypeError: XGBClassifier.fit() got an unexpected keyword argument
'early_stopping_rounds'` — recipes that pass it to `fit` predate XGBoost 2 and do
not run today.

---

## 4. Early stopping without grading its own homework

**Trap.** `fit(..., eval_set=[(X_val, y_val)])` with early stopping, then score
`X_val`. The validation fold chose the number of trees *and* graded the result.

**Why invisible.** It runs, and the score is only slightly optimistic — per fold.
Across a hyperparameter search that bias compounds: the search selects whichever
configuration happened to stop luckiest.

**Fix.** Stop on an inner split of the training fold (§3). Alternatively, run
CV once to find the best iteration per fold, fix `n_estimators` to the median,
and refit without early stopping.

**Detection test.** Compare the two on identical folds. A positive gap is the
optimism the naive version reports.

```python
def early_stopping_optimism(score_fn_naive, score_fn_inner):
    """Each returns a CV score on identical folds. Higher is better."""
    naive, honest = score_fn_naive(), score_fn_inner()
    return naive - honest   # > 0: the naive estimate is inflated by this much
```

---

## 5. Stacking and blending without meta-leakage

**Trap 1 — train/test meta-feature mismatch.** Train meta-features come from
`cross_val_predict` (out-of-fold), but test meta-features come from base models
**refit on the full training set**. The two can come from different
distributions — a refit on more data is often more confident than a fold model —
so the meta-learner is fit on one and applied to the other.

**Fix.** Test meta-features are the **fold-averaged** predictions of the same
fold models (§3 returns exactly that). Measured on NFL pass prediction
(`feature-construction.md` §6), fold-averaging beat the refit (upstream 2024 AUC
0.806 vs 0.799) even though the refit was *not* more confident there — averaging
five models is a gain in its own right.

**Trap 2 — the meta-learner scored on the rows it learned from.** Fitting the
stacker on all OOF rows and reporting its score on those rows.

**Fix.** Nest it: cross-validate the stacker over the OOF matrix with the **same
groups**.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

def stack_cv(oof_matrix, y, groups, n_splits=5):
    """oof_matrix: (n_rows, n_models) OOF probabilities. Returns honest CV loss."""
    oof_matrix, y, groups = np.asarray(oof_matrix), np.asarray(y), np.asarray(groups)
    meta_oof = np.full(len(y), np.nan)
    for tr, va in GroupKFold(n_splits=n_splits).split(oof_matrix, y, groups):
        m = LogisticRegression(C=1.0).fit(_logit(oof_matrix[tr]), y[tr])
        meta_oof[va] = m.predict_proba(_logit(oof_matrix[va]))[:, 1]
    return log_loss(y, meta_oof)

def _logit(p, eps=1e-6):
    p = np.clip(p, eps, 1 - eps)
    return np.log(p / (1 - p))
```

**Prefer the simplest blender that wins.** A weighted average of logits (or of
ranks, for AUC) usually matches a learned stacker on small data and cannot
overfit a meta-layer. Stack in **logit space** for probabilities: averaging raw
probabilities pulls every blend toward 0.5.

**Eligibility is a rule, not an afterthought.** If the competition or the write-up
distinguishes a single model from an ensemble, decide *before* comparing what
counts. hoopsq's ruling: augmented single models were winner-eligible;
ensembles and entries that only *complement* a reference score were reported but
not eligible.

---

## 6. Seed and fold bagging — measure the variance first

**Trap.** Declaring a +0.001 improvement from one seed when seed-to-seed spread
on that configuration is ±0.003.

**Detection test.** Before comparing two configurations, run the baseline over
several seeds and report the spread. An effect smaller than that spread is not
established.

```python
def seed_spread(score_fn, seeds=(0, 1, 2, 3, 4)):
    s = np.array([score_fn(seed) for seed in seeds])
    return s.mean(), s.std(ddof=1)
```

**Thread count is a second seed, and it is not tiny.** XGBoost's parallel
histogram build changes the floating-point reduction order with `n_jobs`, and
on a small frame that moves the score by as much as a seed does. hoopsq
(2026-09-17, 1,324 rows): the same configuration scored **0.63153 / 0.63160 /
0.63149 / 0.63210 / 0.63200** at 1 / 2 / 4 / 8 / 24 threads — a 0.0006 spread,
the size of the #1-vs-#2 gap and of the leaderboard's tie tolerance — and
per-shot probabilities moved by up to **0.044** between 1 and 24 threads. The
committed single-seed, unpinned-thread number was also the winner's *worst* of
six seeds (seed sd 0.0004–0.0008). Two rules, both cheap:

- **Pin `n_jobs`** (or `nthread`) in the estimator factory and record it in
  the run metadata — a leaderboard whose entries ran on different thread counts
  is not comparable at the third decimal.
- **Compare seed-averaged scores, never one seed.** Score every tree entry on
  3–5 seeds; a claim smaller than the seed sd is not a claim. Seed-averaged, the
  same hoopsq winner-vs-reference delta went from "not significant at 5%" (one
  seed: t p 0.13) to −0.0036, 9/10 games, t p 0.014.

```python
def assert_threads_pinned(model):
    """A boosted model whose thread count floats gives a different number per box."""
    n = getattr(model, "n_jobs", None) or getattr(model, "nthread", None)
    assert n not in (None, -1, 0), "pin n_jobs/nthread explicitly and record it in run_meta"
```

**Bagging.** Averaging the same model over several seeds (and several fold
assignments) reduces variance for little risk and is one of the few "free" late
gains. It does not fix bias, leakage, or a wrong splitter.

---

## 7. Feature selection that does not lie

> Correlated columns split importance between them (measured 5.5× on a
> near-copy); cluster them first — `feature-construction.md` §3. Generated
> candidates need a permuted-input null bar — §5 there.

Three rules, each learned on real data. The companion detail — the low-dimensional
substrate, why 60 features beat 244 — is in `feature-engineering.md` §4.

1. **Gain importance misleads; use permutation on held-out data.** On NHL xG,
   gain ranked `empty_net` at **38.3%** and buried `shot_distance` at 5.3%.
   Permutation on a held-out season inverted that — AUC drop **0.2068** for
   `shot_distance`, 0.0365 for `empty_net`.
2. **Permute one-hot blocks together**, with one shared row order — permuting
   columns one at a time lets the model rebuild the signal from the siblings.
3. **Permutation is blind to anything constant within the evaluation group.**
   The five era one-hots measured exactly **0.0000** by permutation inside a
   held-out season — then dropping them cost **−0.0142 LOSO**, the largest
   single effect measured. Inside one season every era column has `n_unique ==
   1`, so permuting it is a no-op by construction. **Season-constant (or
   group-constant) features must be judged by ablation — retrain without them.**

**Null importance.** To separate real importance from what a model extracts
from noise, refit with the **target permuted** many times and compare each
feature's actual importance against its null distribution. Keep features whose
actual importance exceeds, say, the 90th percentile of their nulls.

```python
def null_importance_keep(fit_importance, X, y, n_null=30, pct=90, seed=0):
    """fit_importance(X, y) -> 1-D array of per-feature importances.

    Uses importances from a model fit on permuted targets as the null. Returns a
    boolean keep-mask. Any feature the model 'finds' on shuffled labels is
    fitting noise, and its real-label importance is not evidence of signal.
    """
    rng = np.random.default_rng(seed)
    actual = fit_importance(X, y)
    nulls = np.vstack([fit_importance(X, rng.permutation(y)) for _ in range(n_null)])
    return actual > np.percentile(nulls, pct, axis=0)
```

**A random-noise probe column** is the cheap version: add one or two columns of
pure noise; any real feature ranking below them is a candidate to drop.

---

## 8. Augmentation — label-preserving and in-fold only

**Rules.**
- The transform must **preserve the label** (a reflected court is the same shot;
  a jittered position may not be).
- Augment **inside each training fold only** — never the validation fold, and
  never before splitting, or the reflected copy of a validation row trains the
  model that scores it.

- **A row-adding augmentation needs a duplication control.** Doubling the rows
  doubles the gradient/hessian mass a boosted model sees, which halves the
  effective `min_child_weight` and `reg_lambda` — a regularisation change that
  has nothing to do with the transform. Register a "duplicate without
  transform" arm (or hold the hessian constant with `sample_weight = 1/copies`)
  before attributing any gain to the augmentation.

**Real citation — what helped and what hurt.** hoopsq (2026-09-15, re-measured
2026-09-17 with the duplication control, 5 seeds), all leave-one-game-out:

| arm (winner's settings) | log loss |
|---|---|
| plain | 0.63197 |
| **rows stacked twice, no reflection** (the control) | 0.62986 |
| court reflection (y → −y, left/right vocabulary swapped), unweighted | 0.62802 |
| court reflection, each copy at weight 0.5 (hessian held constant) | ≈ −0.0023 vs plain |
| position jitter at the tracker's `predError` scale | **+0.006** (hurts) |
| season-aggregate `base_margin` (XGBoost) | **+0.004 to +0.009** (hurts) |
| game bagging | neutral |

The first-reported "−0.003, 9/10 games" was about **half duplication**:
reflection beyond the control is ≈ −0.0018, and three independent reviewers
found it only because the control arm was added. Reflection is still the only
one of the four that preserves the label exactly; jitter at the noise scale
*adds* noise to a model already limited by it. Note also that "weighted vs
unweighted" is not a weighting test when every weight is 0.5 — assert
`np.unique(sample_weight).size > 1` before calling something a weighting
experiment (`failure-modes.md` §15b).

```python
def augmentation_arms(fit_score, X, y, transform, seeds=(0, 1, 2, 3, 4)):
    """Three arms, seed-averaged: plain / duplicated-untransformed / transformed.

    fit_score(X, y, seed) -> held-out loss under the grouped splitter.
    Attribute to the transform only (arms[2] - arms[1]); arms[1] - arms[0] is
    the regularisation change from doubling the rows.
    """
    import numpy as np
    Xt, yt = transform(X, y)
    arms = [(X, y), (np.vstack([X, X]), np.concatenate([y, y])),
            (np.vstack([X, Xt]), np.concatenate([y, yt]))]
    return [np.mean([fit_score(a, b, s) for s in seeds]) for a, b in arms]
```

---

## 9. Tuning — where it pays and where it cannot

- **Tune on the right folds.** Hyperparameter search inside grouped CV (§2),
  never against a single split and never against the public leaderboard.
- **Search space first, sampler second.** For gradient boosting the high-leverage
  knobs are learning rate × number of trees (via early stopping), tree
  complexity (`max_depth` / `num_leaves`), row and column subsampling, and
  L1/L2 regularization. Lower the learning rate late, not early.
- **Optuna** (TPE sampler, `MedianPruner`) is the default search driver; prune on
  the grouped-CV objective, not a single fold.
- **Know when capacity is not the constraint.** If depth 4 → 8 moves the score by
  less than seed spread (§6), stop tuning and go back to §1. The NHL xG case:
  **+0.0007** for doubling depth, against a ceiling set by what the feed does not
  record (pre-shot passing, screens, traffic).
- **An unreachable gate is a measurement, not a tuning target.** That same model
  carried a 0.82 CV-AUC gate inherited from a miscalibrated artifact; the honest
  ceiling was ~0.78. Retune the gate from evidence (`metrics-and-gates.md`'s
  never-lower rule governs *raising* a floor you have met, not keeping one no
  honest fit can reach).

---

## 10. Post-processing to the metric

Optimize **the metric the leaderboard uses**, on OOF predictions, then apply the
same transform to test.

| Metric | Post-processing |
|---|---|
| log loss | calibrate (isotonic/Platt on OOF, `metrics-and-gates.md`); **clip** to `[eps, 1-eps]` — one confident miss dominates |
| Brier | calibrate; clipping helps less |
| AUC | ranks only — calibration and monotone transforms change nothing; blend on ranks |
| F1 / accuracy | tune the decision **threshold** on OOF, not 0.5 |
| MAE | predict the conditional **median**, not the mean |
| RMSE | predict the conditional mean; beware outliers in blending |
| quantile / pinball | fit quantile objectives directly |

**Trap.** Tuning the threshold or calibrator on the same OOF rows you then report.
Nest it, or hold out a group slice for the post-processor.

---

## 11. Claiming an improvement honestly

A single mean difference across folds is not evidence. Report:

- **Per-fold wins.** How many folds improved? A **sign test** on fold wins is
  cheap and assumption-light.
- **Paired comparisons** on identical folds and seeds — never compare runs with
  different splits.
- **The variance you measured** (§6) next to the effect.

**Real citation.** NHL handedness: +0.0021 mean LOSO AUC looked marginal, but it
was positive in **16 of 16** held-out seasons — sign-test *p* ≈ 1.5×10⁻⁵, decisive.
The first 4-season run, also 4/4, was only *p* ≈ 0.06 — suggestive. Same effect
size; the difference was the number of independent folds.

```python
from scipy.stats import binomtest

def sign_test(fold_deltas):
    """fold_deltas: per-fold (candidate - baseline), higher is better."""
    d = np.asarray(fold_deltas)
    wins, n = int((d > 0).sum()), int((d != 0).sum())
    if n == 0:                      # tied on every fold: no evidence either way
        return 0, 0, 1.0
    return wins, n, binomtest(wins, n, 0.5, alternative="greater").pvalue
```

---

## 12. Pre-submission checklist

- [ ] Baseline scored through the **same** validation path (§0)
- [ ] Shuffled-target check falls to chance (§1a)
- [ ] No single feature above the **measured** leak ceiling (§1b)
- [ ] Every boolean feature fires on real data (§1c)
- [ ] Every event-table feature consumes only sources before the event (§1d)
- [ ] Adversarial validation run; drift handled or explained (§1f)
- [ ] No duplicate rows or split entity aliases across folds (§1g)
- [ ] Splitter mirrors how the hidden test was drawn (§2)
- [ ] Early stopping on an inner split, not the scored fold (§4)
- [ ] Stacker test features are fold-averaged; stacker itself cross-validated (§5)
- [ ] Improvement exceeds seed spread and wins a sign test across folds (§6, §11)
- [ ] Group-constant features judged by ablation, not permutation (§7)
- [ ] Augmentation label-preserving and in-fold only (§8)
- [ ] Post-processing fit on OOF and applied identically to test (§10)
- [ ] Submission file validated against the sample submission: ids, row count,
      column order, value range, no NaN

---

## Provenance

The failure modes, detection tests and numbers above are this ecosystem's own:
NHL xG leave-one-season-out search and handedness capture (fastRhockey-nhl-data,
2026-09-03); the hoopsq SkillCorner shot-quality entry for the PySport Analytics
Cup 2.0 (2026-09-14/15); cfbfastR-cfb-data #67. The survey that motivated the
corrections in §3–§5 reviewed public skills including
`tondevrel/scientific-agent-skills@xgboost-lightgbm` (MIT) and
`K-Dense-AI/scientific-agent-skills@scikit-learn` (MIT); no text was copied, and
the recipes here correct defects found in the surveyed versions. Those skills
remain installed for API reference — see `upstream-skills.md`.
