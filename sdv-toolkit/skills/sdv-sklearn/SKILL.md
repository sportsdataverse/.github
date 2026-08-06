---
name: sdv-sklearn
description: Use before fitting, tuning, persisting, or debugging any scikit-learn or XGBoost model on SportsDataverse data — the parts of those APIs that silently produce a WRONG sports model rather than erroring. Generic scikit-learn guidance teaches the API; this catalogs the panel-sports-shaped failures it will not flag, because generically they look fine. Ten failure families, each entry carrying its detection test - A splitting and leakage (a bare KFold shuffling across games within a season is leakage; GroupKFold on game_id, TimeSeriesSplit on season), B Ridge and RAPM (alpha scale vs standardization, fit_intercept, sparse solvers, sample_weight, and the confirmed lambda-applied-to-nothing no-op), C Pipeline and ColumnTransformer (preprocessing outside the Pipeline leaks through CV; feature-name ordering), D calibration (LogisticRegression regularizes by default unlike statsmodels), E unseen entities (players and teams absent from the training season), F silent failure (swallowed ConvergenceWarning), G determinism, H persistence (why models ship as XGBoost .ubj not pickles), I performance (sparse densification), J XGBoost interop. Invoke for "fit a model", "set up cross-validation", "why is my model wrong but not erroring", "RAPM", "ridge", "calibrate probabilities", "save/load a model", or before any sdv-model-spine fitting phase.
---

# scikit-learn / XGBoost on panel-sports data

A generic sklearn tutorial is correct about sklearn and wrong about your data.
`KFold` is a perfectly good splitter — for i.i.d. rows. A play-by-play frame
is not i.i.d.: every row belongs to a `game_id`, most belong to a `player_id`
that repeats for a whole season, and the season itself is ordered in time.
None of that is visible to sklearn's API, so none of it is checked. The model
fits, `.score()` returns a number, CI is green — and the number is wrong. This
file is the panel-sports-specific vocabulary `sdv-model-reviewer`'s
`sklearn-contract` lens (`sdv-toolkit/agents/sdv-model-reviewer.md` §5) already
assumes at review time; this is its build-time counterpart — where to reach
for it *while writing* the fit. **Any contradiction between this file and that
lens is a defect in this file, not in the lens.**

**Family B is why this skill is first-party, not a routing table entry.**
RAPM *is* ridge regression (`sdv-modeling/references/methods.md` §"Adjusted
plus-minus family") — this ecosystem has a whole model family built directly
on `sklearn.linear_model.RidgeCV`, and the confirmed production incident in
that family, a ridge penalty applied to nothing, shipped live for two days
with every column present and plausible
(`sdv-modeling/references/failure-modes.md` §2, `cfb-data@8cbaa4d`). A generic
sklearn skill has no way to know that failure exists, because generically
`RidgeCV(alphas=...)` is fine — the failure is entirely in the *scale
convention* colliding with a panel-sports fitting recipe copied from a
different ridge implementation. Every other family below is grounded the same
way: a real call site in this codebase, or an honest statement that none
exists yet.

Every entry: the trap · why it never errors · **the detection test** (runnable,
would actually fire on the failure it names) · a real citation where one
exists.

## Ground truth: what this codebase actually calls

Confirmed by grepping `sportsdataverse/` for every sklearn/XGBoost entry
point (`RidgeCV`, `LogisticRegression`, `GaussianMixture`, `Booster`,
`DMatrix`, `Pipeline`, `ColumnTransformer`, `OneHotEncoder`, `KFold`,
`GroupKFold`, `TimeSeriesSplit`, `random_state`, `n_jobs`, `pickle`, `joblib`)
— this is the inventory every family below cites against, not a hypothetical:

| Component | Real call sites | Never seen |
|---|---|---|
| `RidgeCV` (RAPM family) | `nba/nba_rapm.py:236`, `nba/nba_rapm_variants.py:247`, `nba/nba_matchup_drapm.py:177`, `nba/nba_model_validation.py:179` | `Ridge(solver=...)` with a hand-picked solver; `Lasso`/`ElasticNet` |
| `LogisticRegression` | `nhl/nhl_faceoff_value.py:195`, `nhl/nhl_microstat_constants.py:462`, `pwhl/pwhl_xg_proxy.py:545,725` | `CalibratedClassifierCV`, `SVC`, any decision-boundary classifier |
| `GaussianMixture` | `mlb/mlb_pitch_classify.py:68` (the one call site that threads `random_state=`) | — |
| XGBoost native `Booster`/`DMatrix` | 25+ sites across `cfb/`, `nfl/`, `nba/`, `nhl/`, `mbb/`, `mlb/` — every one passes `feature_names=` explicitly | `XGBClassifier`/`XGBRegressor` sklearn wrapper — zero uses anywhere |
| `Pipeline` / `ColumnTransformer` | none | — the whole family is prospective, see Family C |
| `OneHotEncoder` / `LabelEncoder` / `OrdinalEncoder` | none (`pd.get_dummies` hand-rolled instead, `nhl/nhl_faceoff_value.py:159,188`) | — |
| `GroupKFold` / `TimeSeriesSplit` (production) | none in `sportsdataverse/`; `GroupKFold(n_splits=5)` grouped by `game_id` in the dev CV harness `dev/t5_xg_reevaluation/xg_cv_harness.py:105,109` | bare `KFold`/`train_test_split` — also none, so the codebase hasn't yet violated Family A either |
| `warnings.filterwarnings`/`catch_warnings` around a `.fit(` | none | — Family F is currently clean; stays that way only if new fits keep it that way |
| `pickle`/`joblib` model persistence | none — every persisted artifact is XGBoost `.ubj` + a `.card.json` sidecar (`cfb/models/*.ubj`, `nfl/models/*.ubj`) | any pickled sklearn estimator |

Where a family's trap has no real instance yet, that's stated plainly below
rather than manufactured — see `failure-modes.md` §20's convention: a
documented hazard is not a confirmed incident, and conflating the two is
worse than naming the gap.

---

## A. Splitting & leakage

**Trap.** A frame with repeated groups (multiple rows per `game_id`, per
`player_id`-season) split with a bare `sklearn.model_selection.KFold` or
`train_test_split(shuffle=True)` puts correlated rows on both sides of the
split. **Never a bare `KFold` on grouped or time-ordered data** — use
`GroupKFold(groups=...)` for panel data, `TimeSeriesSplit` for anything
ordered in time (`sdv-model-reviewer.md` §5, verbatim). A `GroupKFold`
*instantiated* but never given `groups=` at `.split()` degrades silently to
an ungrouped split — same failure, one line quieter.

**Why invisible.** The fit runs, `cross_val_score` returns a number, and the
number looks *better* than the honest one — a model that memorized which
`game_id` it's seeing wins twice on the shuffled-in duplicate.
`cross_val_score` on a bare estimator has the same shape one level up:
preprocessing fit inside the scoring loop on the full fold instead of just
the training split leaks fold statistics forward, and the CV score is
optimistic in a way nothing flags.

**Real citation.** The codebase already does this correctly where it
matters most — the PWHL xG cross-validation harness explicitly groups by
`game_id`:

```python
# dev/t5_xg_reevaluation/xg_cv_harness.py:103-111
games = allsh["game_id"].to_numpy()
game_ids = allsh["game_id"].unique().to_list()
idx = np.arange(len(game_ids))
gk_folds = []
for tr_i, te_i in GroupKFold(n_splits=5).split(idx, groups=idx):
    gk_folds.append(([game_ids[i] for i in tr_i], [game_ids[i] for i in te_i]))
_report("GroupKFold(5) by game", _collect(pbp, gk_folds))
```

The season-ordered counterpart is `nba_model_validation.py:927 walk_forward`
— not literally `TimeSeriesSplit`, but the same discipline by hand: fit only
on `game_date <= D`, predict only `D < game_date <= D + horizon_days`, walk
`D` forward. `metrics-and-gates.md` §3 covers the adjacent `through_week`
EXCLUSIVE-boundary rule for this same walk; cross-referenced, not restated.

No `sportsdataverse/` production module currently calls a bare `KFold` — the
grep in the table above found zero hits, so this family is a documented
discipline to keep, not a confirmed incident to fix.

**Detection test.**

```python
import numpy as np
from sklearn.model_selection import KFold, GroupKFold

def assert_no_group_leak(game_ids: np.ndarray, splitter) -> None:
    """Fires on a bare KFold applied to panel data; passes on GroupKFold."""
    for train_idx, val_idx in splitter.split(game_ids, groups=game_ids):
        train_games = set(game_ids[train_idx])
        val_games = set(game_ids[val_idx])
        leaked = train_games & val_games
        assert not leaked, f"{len(leaked)} game_ids appear on both sides of the split"

# fires on the trap (KFold ignores groups= — accepted only for API compatibility):
assert_no_group_leak(game_ids, KFold(n_splits=5, shuffle=True))   # AssertionError
# passes on the fix:
assert_no_group_leak(game_ids, GroupKFold(n_splits=5))            # OK
```

Would this fire? Yes — with `shuffle=True` and repeated `game_id` values,
row-level shuffling scatters a game's rows across folds almost certainly once
there are more distinct games than folds; `GroupKFold` keeps every row for a
given group on one side by construction, so the same assertion passes on it.

---

## B. Ridge / RAPM

**This is the family the skill exists for** — see the intro above and
`failure-modes.md` §2 for the full incident (`cfb_adjusted_epa`'s ridge
penalty was left at the glmnet-scale `325`; under sklearn's `alpha =
lambda * n` convention that crushes every coefficient toward zero,
`adj_off_epa` correlated 0.9928 with its own raw unadjusted input, and it
shipped for two days before anyone measured the output). **That incident is
cross-referenced, not restated here** — its assertion
(`corr(adjusted, raw) < 0.95`) lives in `failure-modes.md` §2 and
`checks.py`. What follows is the general form of the same class, plus the
sub-traps the brief names that the λ-no-op doesn't cover.

**Alpha scale depends on the λ convention the source used.** glmnet's λ and
sklearn's `alpha` are NOT the same number for the same regularization
strength — `alpha ≈ lambda * n_samples`, and `n_samples` means the design
matrix's *row* count (possessions), not the player count. Copying a
published λ straight into sklearn's `alphas=` without the conversion is
exactly how the confirmed incident happened. This ecosystem's own oracle-fit
variant path performs the conversion explicitly and documents *why*
`n_samples` means possessions, not players:

```python
# sportsdataverse/nba/nba_rapm_variants.py:63-90 (oracle_rapm_alphas)
# Ryan Davis's reference RAPM: lambda_to_alpha(l, n) = l * n / 2.0
# n = X.shape[0] (possessions, i.e. regression samples) -- NOT len(player_ids).
ORACLE_RAPM_LAMBDAS: tuple[float, ...] = (0.01, 0.05, 0.1)
ORACLE_RAPM_CV: int = 5
```

against the plain-RAPM path's independently-tuned, non-interchangeable grid:

```python
# sportsdataverse/nba/nba_rapm.py:22-23,236
DEFAULT_RAPM_ALPHAS: np.ndarray = np.logspace(2, 5, 8)   # 100 .. 100,000
model = RidgeCV(alphas=alphas, fit_intercept=True)        # sparse csr_matrix, solver="auto"
```

The module docstring for the variants file is explicit that the two grids are
"a binding ruling... **not** interchangeable" — the codebase has already
learned, in writing, that swapping one alpha convention for another silently
changes what "regularized" means.

**`sample_weight` for possession weighting** is real and already load-bearing
here, not a hypothetical parameter:

```python
# sportsdataverse/nba/nba_matchup_drapm.py:177-178
model = RidgeCV(alphas=cfg.ridge_alphas, fit_intercept=True)
model.fit(X, y, sample_weight=w)
```

A ridge fit missing `sample_weight` on possession-count-weighted RAPM data
silently treats a 2-possession stint and a 40-possession stint as equally
informative — no error, just a wrong answer that skews toward noisy short
stints. The same file's neighboring comment ("no extra ×100, that was a
double-scale bug") is itself evidence of how easy this family is to get
wrong even with a careful, existing test suite watching it.

**Solver behavior on sparse matrices is a Family-B/Family-I boundary, not a
silent Family-B bug by itself.** `Ridge(solver="cholesky")`/`"svd"` on a
sparse `X` *raises* (`check_array(accept_sparse=False)` for those solvers) —
loud, not the class this skill catalogs. `RidgeCV`'s default `solver="auto"`
picks a sparse-safe path, which is why `nba_rapm.py:235`'s own comment notes
it explicitly: `# RidgeCV — accepts sparse csr_matrix with default
solver="auto"`. The actually-silent version is `sag`/`saga`: they're
iterative and stochastic, and an under-iterated fit returns a plausible,
wrong coefficient vector without raising — that's Family F's
`ConvergenceWarning`/`n_iter_` trap wearing a ridge-specific hat; the
detection test below is the ridge-specific form, and cross-references
Family F for the general one.

**Detection test — sub-convergence solver check (a general form of the
λ-no-op assertion, applicable to any ridge fit, not restated from the
`cfb_adjusted_epa` incident):**

```python
import numpy as np
from sklearn.linear_model import Ridge

def assert_solver_agrees_with_exact(X, y, alpha, *, solver="saga", tol=0.02, max_iter=5000):
    """sag/saga are iterative and stochastic; an under-iterated fit still
    returns coefficients that run and look plausible. Compare against the
    exact closed-form solution and require numerical agreement."""
    X_dense = X.toarray() if hasattr(X, "toarray") else X
    exact = Ridge(alpha=alpha, solver="cholesky", fit_intercept=False).fit(X_dense, y)
    approx = Ridge(alpha=alpha, solver=solver, max_iter=max_iter, fit_intercept=False).fit(X, y)
    rel_err = np.linalg.norm(approx.coef_ - exact.coef_) / np.linalg.norm(exact.coef_)
    assert rel_err < tol, f"{solver} coefficients diverge {rel_err:.3f} from the exact ridge solution"
```

Would this fire? Yes — cap `max_iter` low enough on a real design and the
relative error against the closed form grows past `tol` well before `saga`
converges; raise `max_iter` back up and it passes.

**Detection test — the alpha grid actually brackets an optimum.** A second,
distinct no-op shape from the confirmed incident: `RidgeCV` silently picks
whichever alpha in the grid scores best *even if the true optimum lies
outside the searched range* — a hardcoded, too-narrow grid (a single
copied λ, or a grid centered on the wrong scale) can land the "cross-
validated" alpha exactly on the grid's own edge, which means the grid never
actually bracketed anything:

```python
def assert_alpha_not_at_grid_edge(ridge_cv, alphas) -> None:
    """RidgeCV.alpha_ landing on min(alphas) or max(alphas) means the grid
    didn't bracket the true optimum -- the 'cross-validated' choice is only
    as good as the narrowest or widest value someone hardcoded."""
    chosen = ridge_cv.alpha_
    lo, hi = min(alphas), max(alphas)
    assert chosen not in (lo, hi), (
        f"RidgeCV selected alpha={chosen} at the edge of the searched grid [{lo}, {hi}]"
    )
```

**A cautionary note earned by verifying this file's own tests before
shipping them** (per the "would this test actually fire" discipline this
skill asks of every other detection test): an earlier draft of this section
compared `corr(ridge.coef_, ols.coef_)` as a general no-op check. Running it
against a real `RidgeCV(alphas=np.logspace(2, 5, 8))` fit — the exact grid
`nba_rapm.py` ships — showed the correlation stays **0.9993**, i.e. it fires
as a false alarm on a normal, correctly-regularized fit, because ridge
shrinkage is close to a uniform rescaling and Pearson correlation is
scale-invariant — it cannot see shrinkage at all. That draft is not in this
file; the mechanism that actually caught the real incident is a correlation
between the **derived output value** (adjusted vs. raw EPA) and its
input, not between two coefficient vectors from the same design — that
assertion is `failure-modes.md` §2's, verified there, not re-derived
(incorrectly) here.

---

## C. Pipeline / ColumnTransformer

**Trap.** Preprocessing (`StandardScaler`, `OneHotEncoder`) fit on the full
frame *before* a train/test split or CV loop leaks held-out statistics into
training — it must live inside `Pipeline([...])`
(`sdv-model-reviewer.md` §5, verbatim: "Flag any `.fit(` or `.fit_transform(`
on a preprocessing transformer that is not wrapped in `Pipeline(...)`...
before a `train_test_split`/CV loop"). `ColumnTransformer(remainder="drop")`
silently discards any input column not claimed by an explicit transformer —
no warning, the output frame is just narrower than the input. And
`get_feature_names_out()` can reorder relative to `feature_names_in_` across
a refit (a `ColumnTransformer`'s internal transformer order, or a
`remainder="passthrough"` block moving to the end) — the model still
predicts, on the wrong column for every weight.

**Why invisible.** All three produce a same-shaped, plausible-looking
prediction. A dropped `remainder` column just means the model never saw a
feature it should have; a reordered `get_feature_names_out()` means every
coefficient is now paired with the wrong column, and the score can even
*improve* by coincidence on a small validation set.

**Real citation.** Zero `Pipeline(`/`ColumnTransformer(` call sites exist in
`sportsdataverse/` today — every current sklearn fit (RAPM, faceoff logistic,
umpire zone) builds a single untransformed numeric or sparse design matrix
inline, so this specific trap hasn't bitten yet. The codebase's actual guard
against the *same class* of failure — feature-column-order silently drifting
between fit and predict — is manual, at the XGBoost boundary, not a
`Pipeline`:

```python
# sportsdataverse/nfl/ep_wp.py:169
# Feature order must match the trained model's ``feature_names`` exactly.
```

Read this as the codebase's existing hardening against exactly the failure
`get_feature_names_out()` ordering would introduce if a `Pipeline` were
added here — see Family J for the full XGBoost-specific form.

**Detection test.**

```python
def assert_feature_order_locked(pipeline, expected_names: list[str]) -> None:
    """A refit Pipeline can silently reorder get_feature_names_out() output --
    the model still predicts, just against the wrong column per weight."""
    actual = list(pipeline[:-1].get_feature_names_out())
    assert actual == expected_names, f"pipeline output columns reordered: {actual} != {expected_names}"


def assert_remainder_not_dropping(column_transformer, all_input_columns: set[str]) -> None:
    """remainder='drop' (the default) discards any column no transformer claims."""
    handled: set[str] = set()
    for _, _, cols in column_transformer.transformers:
        handled.update(cols if isinstance(cols, (list, tuple)) else [cols])
    if column_transformer.remainder == "drop":
        dropped = all_input_columns - handled
        assert not dropped, f"remainder='drop' silently discards {dropped}"
```

Would this fire? Yes on both — reorder a `ColumnTransformer`'s
`transformers=` list between fit and the assertion and the first check trips;
add a column to `all_input_columns` that no transformer entry claims and the
second trips, exactly as `remainder="drop"` would silently behave.

---

## D. Calibration

**Trap.** `sklearn.linear_model.LogisticRegression`'s default is `C=1.0` —
real L2 regularization — unlike an unregularized `statsmodels.Logit`/R `glm`
MLE fit; porting a recipe from either without adding `C=1e6`ish silently
shrinks every coefficient toward zero. `predict_proba` on a
non-probabilistic decision-boundary classifier (an SVM) is not automatically
a real probability — it needs `CalibratedClassifierCV` (sigmoid/Platt for
small samples or a monotonic prior, isotonic only with enough data to fit a
free-form monotone curve without overfitting it). `class_weight="balanced"`
reweights the loss AND moves the fitted intercept, which corrupts anything
downstream that assumes the model's own baseline rate.

**Why invisible.** `predict_proba` always returns a number in `[0, 1]` that
*looks* like a probability whether or not it's calibrated. A shrunk
coefficient still predicts, just less confidently than the honest MLE would
— nothing distinguishes "correctly regularized on purpose" from "silently
regularized because nobody set `C`."

**Real citation.** Every `LogisticRegression` call site in this codebase
currently accepts the sklearn default `C=1.0`:

```python
# nhl/nhl_faceoff_value.py:195, nhl/nhl_microstat_constants.py:462,
# pwhl/pwhl_xg_proxy.py:545,725 -- all four:
clf = LogisticRegression(max_iter=1000)
```

That's not flagged as a bug — small-n contextual logistics (a faceoff-zone
model, a microstat classifier) plausibly *want* the shrinkage — but none of
the four sites states that choice is deliberate versus a copied default, and
none of the four currently compares against an unregularized fit to know how
much shrinkage `C=1.0` is actually applying on its own data.
`CalibratedClassifierCV` has zero call sites anywhere in this codebase —
this sub-trap is prospective, for the day a decision-boundary classifier
shows up here, not a confirmed incident.

**Detection test.**

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def assert_regularization_is_intentional(X, y, *, c=1.0, tol=0.05) -> None:
    """Compares C=1.0 (the sklearn default, and the default at every current
    LogisticRegression call site in this codebase) against an effectively
    unregularized fit; a large gap means the default is doing real,
    unexamined shrinkage."""
    default_fit = LogisticRegression(C=c, max_iter=1000).fit(X, y)
    unreg_fit = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
    shrinkage = 1 - np.linalg.norm(default_fit.coef_) / max(np.linalg.norm(unreg_fit.coef_), 1e-12)
    assert shrinkage < tol, f"C={c} shrinks ||coef|| by {shrinkage:.1%} vs. the unregularized fit"


from sklearn.calibration import calibration_curve

def assert_probabilities_calibrated(y_true, y_prob, *, n_bins=10, max_gap=0.05) -> None:
    """A model can have a great Brier score and still be miscalibrated in a
    specific bucket -- metrics-and-gates.md requires the calibration table
    alongside Brier for exactly this reason."""
    frac_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="quantile")
    gap = float(np.max(np.abs(np.asarray(frac_pos) - np.asarray(mean_pred))))
    assert gap < max_gap, f"max calibration gap {gap:.3f} across bins"
```

Would this fire? Yes — the first raises whenever `C` is small enough on a
given `X`/`y` to meaningfully shrink `||coef||` relative to the near-MLE
`C=1e6` fit; the second raises whenever any quantile bin's observed rate
diverges from its mean predicted probability by more than `max_gap`, exactly
the shape a good-Brier/bad-calibration model produces.

---

## E. Unseen entities

**Trap.** `OneHotEncoder(handle_unknown="ignore")` — the safe-looking option,
chosen specifically to avoid the default `"error"` raising at predict time —
makes a player/team id absent from the training season encode as an
all-zero row: every known category is `False`. The model doesn't know the
entity is new; it scores it as if it matches the reference level of every
category simultaneously, and returns a normal-looking number.
`LabelEncoder`/`OrdinalEncoder` applied to a categorical *feature* (team ID,
not a target) imposes a numeric ordering with no real meaning — a
tree-only model that just splits on it is often fine; any linear or
distance-based component reading the code as a magnitude is silently
learning a fake relationship between, say, team id 14 and team id 28.

**Why invisible.** `predict_proba`/`.predict()` never raises for an
all-zero one-hot row or an arbitrary-magnitude ordinal code — both produce a
plausible number for a player who has never appeared in training data, or a
"prediction" that changes if you merely relabel the same categories in a
different order.

**Real citation.** The codebase's own hand-rolled version of
`handle_unknown="ignore"` already exists, and inherits exactly this failure
mode:

```python
# sportsdataverse/nhl/nhl_faceoff_value.py:157-163
def _context_design_matrix(rows: pl.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    frame = rows.select("zone_code", "strength_state", "is_home").to_pandas()
    dummies = pd.get_dummies(frame, columns=["zone_code", "strength_state"], dtype=float)
    for col in feature_names:
        if col not in dummies.columns:
            dummies[col] = 0.0     # <- a category absent from *this batch* is
    return dummies[feature_names]  #    filled to False, exactly like handle_unknown="ignore"
```

This is a deliberate, working pattern for realigning predict-time columns to
the fit-time schema — but a `zone_code`/`strength_state` combination absent
from the *fit* sample (not just the current predict batch) predicts as if it
doesn't exist rather than surfacing that it's new. No `OneHotEncoder` or
`LabelEncoder`/`OrdinalEncoder` call exists anywhere in `sportsdataverse/` —
every categorical encoding in this codebase currently goes through this
hand-rolled `pd.get_dummies` path.

**Detection test.**

```python
import numpy as np

def assert_unseen_categories_are_flagged(
    fit_categories: set, predict_categories: np.ndarray, encoded_rows: np.ndarray
) -> None:
    """Fires when a category absent from the fit sample silently collapses
    to the all-reference-level (all-zero) encoded row instead of being
    flagged -- the failure mode of handle_unknown='ignore' and of
    nhl_faceoff_value._context_design_matrix's column-align-and-zero-fill."""
    unseen = ~np.isin(predict_categories, list(fit_categories))
    if not unseen.any():
        return
    all_zero = ~encoded_rows[unseen].any(axis=1)
    assert not all_zero.any(), f"{int(all_zero.sum())} unseen-category rows encoded as all-zero"


def assert_not_treating_ids_as_ordinal(fit_and_predict_fn, ids, y) -> None:
    """Adversarial construction, not a bigger probe (failure-modes.md #12's
    lesson applies here too): reverse the id-to-code mapping and require the
    fit to be invariant. A model reading the ordinal code as a magnitude
    gives DIFFERENT predictions when the arbitrary mapping is reversed."""
    codes_fwd = {v: i for i, v in enumerate(sorted(set(ids)))}
    codes_rev = {v: i for i, v in enumerate(sorted(set(ids), reverse=True))}
    pred_fwd = fit_and_predict_fn(np.array([codes_fwd[i] for i in ids]), y)
    pred_rev = fit_and_predict_fn(np.array([codes_rev[i] for i in ids]), y)
    assert np.allclose(pred_fwd, pred_rev, atol=1e-6), (
        "predictions changed when the id -> code mapping was reversed -- "
        "the model is reading the ordinal code as a magnitude"
    )
```

Would this fire? Yes on both — the first raises whenever any row for a
category outside `fit_categories` encodes to all zeros (the `ignore`/
hand-rolled behavior); the second raises for any model whose fit isn't
invariant to an arbitrary relabeling of a categorical id, which is every
linear or distance-based model and is specifically NOT true of a model that
correctly treats the id as unordered categorical.

---

## F. Silent failure

**Trap.** A blanket `warnings.filterwarnings("ignore")` /
`catch_warnings()` scoped around a `.fit(` call swallows
`ConvergenceWarning` along with everything else — the model "fits," its
coefficients are whatever the solver had reached when it gave up, and
nothing downstream can tell. `SimpleImputer` on a column that is entirely
null (by default `keep_empty_features=False`) silently **drops** that
column from the output rather than imputing it — the output matrix is
narrower than the input, and everything after it is shifted one column.
`n_iter_` sitting at exactly `max_iter` after a fit is the receipt for "did
not converge" — checked, or not checked, nothing forces it.

**Why invisible.** All three "succeed": the object is fitted, `.predict()`
works, the shape is plausible. `sdv-model-reviewer.md` §5's third bullet is
this family's review-time counterpart, verbatim: "A blanket
`warnings.filterwarnings("ignore")`... around a `.fit(` call hides a model
that never actually converged — its coefficients are meaningless."

**Real citation.** Grepping every `.py` file under `sportsdataverse/` for
`filterwarnings`/`catch_warnings`/`simplefilter`/`ConvergenceWarning`
returns **zero hits** — this codebase currently does not violate this family
at all, and that's the honest state to report rather than manufacturing a
finding. What *is* an honest gap: none of the four
`LogisticRegression(max_iter=1000)` call sites (`nhl_faceoff_value.py:195`,
`nhl_microstat_constants.py:462`, `pwhl_xg_proxy.py:545,725` — same four
cited in Family D) checks `.n_iter_` against `max_iter` after fitting. A grep
for `n_iter_` across `sportsdataverse/` also returns zero hits — the
convergence receipt exists on every fitted estimator and none of the four
sites reads it.

**Detection test.**

```python
import numpy as np

def assert_converged(fitted_estimator) -> None:
    """n_iter_ sitting at exactly max_iter means the solver hit the
    iteration wall, not the optimum -- a plausible-looking non-answer.
    None of nhl_faceoff_value.py:195, nhl_microstat_constants.py:462, or
    pwhl_xg_proxy.py:545/725 currently checks this."""
    n_iter = np.atleast_1d(fitted_estimator.n_iter_)
    max_iter = fitted_estimator.max_iter
    assert not np.any(n_iter >= max_iter), f"n_iter_={n_iter} hit max_iter={max_iter}"


from sklearn.impute import SimpleImputer

def assert_imputer_didnt_drop_columns(imputer: SimpleImputer, expected_n_features: int) -> None:
    """SimpleImputer silently drops an all-NaN column by default
    (keep_empty_features=False) -- everything downstream is shifted one
    column left with no error."""
    out_width = len(imputer.get_feature_names_out())
    assert out_width == expected_n_features, (
        f"SimpleImputer dropped {expected_n_features - out_width} all-NaN column(s) -- "
        "pass keep_empty_features=True if a constant-imputed column is required"
    )
```

Would this fire? Yes — the first raises whenever the reported `n_iter_`
reaches `max_iter` (the exact non-convergence receipt, not a proxy for it);
the second raises whenever `SimpleImputer` returns fewer columns than it
was given, the exact shape of the silent column-drop.

---

## G. Determinism

**Trap.** `random_state` not threaded through every stochastic component —
a shuffled splitter, `sag`/`saga`, `GaussianMixture`, any
sklearn/XGBoost randomness — means two runs over identical data produce
different fitted coefficients, and a backtest, gate, or published artifact
becomes non-reproducible without ever raising. `n_jobs > 1` can also change
the floating-point reduction order in parallel tree building or BLAS calls,
producing tiny run-to-run numeric drift — invisible unless something diffs
exact bytes (this is the mechanism behind the "cheap pre-check only"
distinction in `failure-modes.md` §2's λ-no-op-republish row: a timestamp
move is not proof of byte-identical content).

**Why invisible.** Nothing errors on a different random draw; the model
"works" every time, it's just not the *same* model every time, and a gate
that only checks the metric (not the artifact) can pass twice on two
different fits.

**Real citation.** Exactly one call site in this codebase explicitly seeds a
stochastic sklearn component:

```python
# sportsdataverse/mlb/mlb_pitch_classify.py:68
model = GaussianMixture(n_components=k, random_state=seed, n_init=1)
```

Every `RidgeCV`/`LogisticRegression` call site elsewhere (`nba_rapm.py`,
`nba_matchup_drapm.py`, `nhl_faceoff_value.py`, `pwhl_xg_proxy.py`) never
passes `random_state=` — currently harmless, because their default solvers
(`RidgeCV`'s closed-form/LOOCV path, `LogisticRegression`'s default `lbfgs`)
are deterministic. The omission becomes live the moment a solver switches to
`sag`/`saga` (Family B) or a CV splitter starts shuffling (Family A) — worth
threading `random_state` now rather than only after one of those changes.

**Detection test.**

```python
import numpy as np

def assert_reproducible_across_runs(fit_fn, X, y, **kwargs) -> None:
    """An un-seeded stochastic path (a shuffled splitter, solver='sag'/'saga',
    a GaussianMixture without random_state) gives different coefficients on
    two runs over identical data. It never raises -- it just quietly stops
    being the same model twice."""
    coef_a = fit_fn(X, y, **kwargs)
    coef_b = fit_fn(X, y, **kwargs)
    assert np.allclose(coef_a, coef_b), (
        "two fits over identical data diverged -- an un-seeded stochastic "
        "component is in the path; thread random_state through it"
    )


import os

def assert_blas_threads_pinned_when_parallel(n_jobs) -> None:
    """sklearn's n_jobs (joblib) parallelism stacks with BLAS's own internal
    threading -- n_jobs=8 workers each spawning 8 OpenBLAS/MKL threads
    oversubscribes the box. It never errors, it just runs slower while
    looking identical in the code."""
    if n_jobs not in (1, None):
        for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
            assert os.environ.get(var) == "1", f"n_jobs={n_jobs} without {var}=1"
```

Would this fire? Yes — the first raises whenever `fit_fn` has any
un-seeded randomness reachable from identical inputs (swap in a
`RidgeCV(solver="saga")` without a fixed `random_state` and it diverges
between calls); `GaussianMixture(random_state=seed)` at
`mlb_pitch_classify.py:68` passes it by construction.

---

## H. Persistence

**Trap.** Pickling a fitted sklearn estimator ties the artifact to the
sklearn (and often numpy/scipy) version that created it. Loading it under a
different version can raise outright, or — worse — succeed with an
`InconsistentVersionWarning` while the estimator's internals have silently
shifted underneath, or silently return an unpickled object whose methods
behave differently than the one that was saved.

**Why invisible.** A version-drifted unpickle that doesn't raise looks
identical to a clean load — `.predict()` still runs, still returns numbers
shaped like the old ones.

**Real citation.** This is why every persisted model in this ecosystem ships
as XGBoost `.ubj` (self-describing) paired with a `.card.json` sidecar, never
a pickle:

```
sportsdataverse/cfb/models/*.ubj   (10 files: ep_model, fd_model, fg_model,
                                     qbr_model, two_pt_model, wp_naive,
                                     wp_spread, xpass_model, cfb_cp_model)
sportsdataverse/nfl/models/*.ubj   (9 files, same family)
```

`ep_model.card.json` documents exactly what's needed to verify a loaded
booster against its trained contract — `xgboost_version`, the ordered
`features` list, `hyperparameters`, `training_seasons`, `n_training_rows`,
`trained_date`. Grepping every `.py` file under `sportsdataverse/` for
`import pickle`/`joblib` returns **zero hits** — the ecosystem has never
persisted a sklearn estimator; every `RidgeCV`/`LogisticRegression`/
`GaussianMixture` fit (RAPM, faceoff logistic, pitch classification) is
refit on demand from source data. `.ubj`'s embedded `feature_names` is the
mechanism `cfb_pbp.py`'s own comment names directly:

```python
# sportsdataverse/cfb/cfb_pbp.py:169
# names so xgboost validates feature_names alignment.
```

**Detection test.**

```python
from xgboost import Booster

def assert_booster_matches_contract(model_path: str, expected_features: list[str]) -> None:
    """A stale or swapped .ubj (wrong file copied into models/) loads fine
    and predicts fine -- only a feature_names check catches the mismatch
    before a wrong prediction ships. Some boosters in this ecosystem were
    trained WITHOUT embedded feature_names (ep_wp.py:200) -- skip those,
    they're covered by Family J's caller-side check instead."""
    booster = Booster()
    booster.load_model(model_path)
    if booster.feature_names is not None:
        assert booster.feature_names == expected_features, (
            f"{model_path} feature_names {booster.feature_names} != expected {expected_features}"
        )
```

Would this fire? Yes — swap in any `.ubj` whose embedded `feature_names`
differ from `expected_features` (a wrong model file, or one trained on a
different feature set) and this raises before that model scores a single
real play.

---

## I. Performance

**Trap.** A RAPM design matrix (`sportsdataverse/nba/nba_rapm.py`'s
`build_rapm_design`) is ~99% zeros — 10 of `2P` columns nonzero per
possession row, `P` the distinct player count for the season. An accidental
densify (`.toarray()`, `np.asarray(X)`, or an estimator/solver choice that
requires dense input — the `Ridge(solver="cholesky")` case from Family B)
doesn't error; it multiplies memory and time by roughly `2P/10` for the
identical answer. `n_jobs` × BLAS thread oversubscription is the same shape
one level up: sklearn's joblib-based `n_jobs` parallelism stacks with
OpenBLAS/MKL's own internal threading, so `n_jobs=8` can spawn ~64 threads
contending for however many cores actually exist — dramatically slower, not
faster, and nothing in the code or the output distinguishes it from "the
machine is just busy."

**Why invisible.** Both produce the exact right answer, just slowly (or, at
NCAA/multi-season scale, until it OOMs — and the crash site is three
function calls downstream of the actual densify, so the root cause reads as
unrelated).

**Real citation.** `nba_rapm.py:41-138`'s `build_rapm_design` is explicit
about staying sparse start to finish:

```python
# sportsdataverse/nba/nba_rapm.py:136-137
X = csr_matrix((data, (rows, cols)), shape=(n, 2 * P))
y = possessions["points"].to_numpy().astype(np.float64)
```

and the one place a reduction touches the full design (`X.sum(axis=0)` at
line 247, to get per-player possession counts) stays cheap specifically
because it sums *into* a `1 × 2P` result rather than materializing `X`
itself — the kind of call site worth re-checking any time a *new* reduction
over the same `X` is added, since `np.asarray(X)` (the whole matrix) instead
of `np.asarray(X.sum(axis=0))` (the tiny reduction) is exactly the silent
densify this family names.

**Detection test.**

```python
from scipy.sparse import issparse

def assert_design_matrix_stays_sparse(X) -> None:
    """A RAPM design is ~99% zeros. An accidental densify doesn't error --
    it just makes the fit 10-100x slower and uses 10-100x the memory for
    the identical answer."""
    assert issparse(X), f"design matrix is {type(X)}, not sparse"
    density = X.nnz / (X.shape[0] * X.shape[1])
    assert density < 0.05, f"design matrix density {density:.1%} is too high for a RAPM indicator matrix"


import os

def assert_blas_threads_pinned(n_jobs) -> None:
    """See Family G -- the same check, restated here because it's a
    performance symptom (silent slowdown) as much as a determinism one."""
    if n_jobs not in (1, None):
        assert os.environ.get("OMP_NUM_THREADS") == "1", f"n_jobs={n_jobs} without OMP_NUM_THREADS=1"
```

Would this fire? Yes — call `assert_design_matrix_stays_sparse(X.toarray())`
on any real RAPM design and `issparse` immediately fails; on the actual
`csr_matrix` from `build_rapm_design`, density sits well under 5% given only
10 of `2P` columns are ever nonzero per row, so it passes.

---

## J. XGBoost interop

**Trap.** The sklearn wrapper (`XGBClassifier`/`XGBRegressor`) infers
feature order from a fit-time pandas `DataFrame.columns`; the native
`Booster`+`DMatrix` path requires the caller to pass `feature_names=`
explicitly (or falls back to positional order). Mixing the two APIs — fit
via the sklearn wrapper, hand `.get_booster()` to native code that builds its
`DMatrix` with a *different* column order — silently mis-scores every row,
because both column counts still match. Early stopping needs a genuine
holdout the CV/hyperparameter search never touched; reusing a CV fold both
to pick hyperparameters and to decide the stopping round leaks the stopping
decision into what's reported as validation performance.
`monotone_constraints=` binds to feature *position*, not feature *name* — if
training's column order drifts from the order the constraint tuple was
written against, the constraint silently pins the wrong feature.

**Why invisible.** A `DMatrix` built with the wrong `feature_names=` order
still has the right shape, predicts a real number for every row, and the
booster itself only validates the order when its own embedded
`feature_names` are present — for a `.ubj` trained *without* embedded names
(`ep_wp.py:200` documents this happens in this ecosystem), there is nothing
on the model side to check the caller's order against at all.

**Real citation.** This is the one family where the codebase's existing
discipline is already the fix, consistently, at every call site — zero
`XGBClassifier`/`XGBRegressor` sklearn-wrapper uses exist anywhere in
`sportsdataverse/` (confirmed by grep); every model is native
`Booster`+`DMatrix`, and every single `.predict(DMatrix(...))` call across
`nfl/ep_wp.py` (7+ sites), `nfl/nfl_pbp.py` (10+ sites), `cfb/cfb_pbp.py`,
`cfb/cfb_fourth_down.py`, `nfl/nfl_fourth_down.py`, and
`nfl/nfl_playcall.py` passes `feature_names=` explicitly against a named
constant (`EP_FEATURES`, `WP_NAIVE_FEATURES`, `CP_FEATURES`, `FD_FEATURES`,
`XPASS_FEATURES`, `PLAYCALL_FEATURE_ORDER`) rather than relying on whatever
order a DataFrame happened to produce:

```python
# sportsdataverse/nfl/ep_wp.py:169
# Feature order must match the trained model's ``feature_names`` exactly.
# sportsdataverse/nfl/ep_wp.py:200
# trained without embedded ``feature_names`` (Booster.feature_names is None), so
# the input matrix MUST be supplied with columns in EXACTLY this order.
```

For models trained *with* embedded `feature_names`, xgboost itself raises a
real `ValueError` on a mismatch — that half of the contract is already loud,
not silent. For models trained *without* them (the `ep_wp.py:200` case), the
caller's own constant list is the only source of truth, with nothing
verifying it against the trainer. That constant is provably correct today —
`cfb/model_vars.py:80-89`'s `ep_final_names` matches `cfb/models/
ep_model.card.json`'s `"features"` list (`TimeSecsRem`, `yards_to_goal`,
`distance`, `down_1`..`down_4`, `pos_score_diff_start`) exactly.

**Detection test.**

```python
def assert_feature_order_matches_training(booster, dmatrix_feature_names: list[str]) -> None:
    """If the .ubj carries embedded feature_names, xgboost itself already
    raises on a mismatch. The genuinely silent case is a booster trained
    WITHOUT embedded names (ep_wp.py:200) -- there, the caller's own
    constant list is the only contract, so pin it against the model card
    rather than trusting it re-read here."""
    if booster.feature_names is not None:
        assert booster.feature_names == dmatrix_feature_names, (
            "xgboost would already raise on this -- unreachable if the .ubj is embedded"
        )


def test_ep_features_match_model_card() -> None:
    """Real, runnable today: cfb/model_vars.py:80-89 vs. cfb/models/ep_model.card.json."""
    from sportsdataverse.cfb.model_vars import ep_final_names

    expected = [
        "TimeSecsRem", "yards_to_goal", "distance",
        "down_1", "down_2", "down_3", "down_4", "pos_score_diff_start",
    ]  # cfb/models/ep_model.card.json "features"
    assert list(ep_final_names) == expected
```

Would this fire? Yes — reorder or rename anything in `ep_final_names`
relative to the shipped `ep_model.card.json`'s `features` list and
`test_ep_features_match_model_card` fails immediately; as written today
against the real files it passes, because the two are confirmed identical.

---

## Where to go next

- Fitting a RAPM/ridge model → read `sdv-modeling/references/methods.md`
  "Adjusted plus-minus family" first, then Family B above.
- Reviewing a fit someone else wrote →
  `sdv-toolkit:sdv-model-reviewer` (`lens: sklearn-contract`), not this
  file — that's the read-only audit counterpart.
- General CV strategy, feature engineering, or MLOps tooling not shaped by
  the panel-sports structure above → `sdv-modeling/references/
  upstream-skills.md`'s routing table (`evaluating-ml-models`,
  `engineering-ml-features`, `ml-pipeline`).
- Why a component that ran without error still produced a wrong dataset,
  outside the sklearn/XGBoost surface specifically →
  `sdv-modeling/references/failure-modes.md`.
