# Model families — the AutoML zoo, judged on panel-sports data

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. The toolkit
> documented XGBoost thoroughly and every other tabular family not at all, so a
> reader had no basis for choosing anything else — or for knowing what an AutoML
> tool would have tried on their behalf.

AutoGluon, H2O AutoML, FLAML and auto-sklearn search essentially the same tabular
zoo: regularized linear, random forest, extremely randomized trees, three
gradient-boosting implementations, a small neural net, and a stacked ensemble
over the survivors. This file covers that zoo **for our data specifically** —
where the panel structure changes the answer.

**The headline: an AutoML tool will hand you a leaked score on our data unless
you pass the group.** The §1 table is measured under `GroupKFold(game_id)`; the
same numbers under a shuffled `KFold` are meaningless (`sklearn-xgboost.md` §A).

**Scope note.** `GroupKFold(game_id)` keeps a game's rows together and nothing
more — it does not isolate teams, players or seasons, so a score for a feature
with entity or season memory can still be optimistic and needs the purged
splitter (§A2). §3's encoding comparison uses a plain train/holdout split, and
§5 is explicitly unverified.

---

## 1. Measured, under GroupKFold

A WP-shaped problem — 400 games × 40 plays, features `score_margin`,
`time_left`, `down`, with a game-level random effect. `GroupKFold(4)` on
`game_id`, ROC-AUC:

| family | AUC | fit (s) | note |
|---|---:|---:|---|
| MLP (sklearn, scaled) | 0.8598 | 5.9 | best here, and 15x the cost of LightGBM |
| CatBoost | 0.8594 | 1.1 | |
| LightGBM | 0.8583 | **0.1** | best accuracy-per-second by a wide margin |
| HistGradientBoosting (sklearn) | 0.8567 | 2.0 | no extra dependency |
| XGBoost | 0.8546 | 0.4 | what we ship |
| **LogisticRegression** | **0.8511** | **0.0** | within 0.009 of the best, at zero cost |
| RandomForest | 0.8258 | 0.9 | |
| ExtraTrees | 0.8160 | 0.7 | |

**Read the spread, not the ranking.** The six non-bagging families sit inside
0.009 AUC of each other, and the fold-to-fold standard deviation is 0.002–0.004.
A "winner" chosen on a 0.005 gap is chosen on noise — the rule
`metrics-and-gates.md` §1b already states, here with numbers.

**Logistic regression at 0.8511 is the finding that matters.** It is 0.009 AUC
behind the best model at literally zero fit cost and full interpretability. On a
sports problem where the substrate is close to one-dimensional — and CFB pregame
already showed 60 features beating 244 (`prior-art.md`) — **the honest baseline
is a GLM, and a boosted model must beat it by more than the PAIRED spread of
the per-fold difference to justify itself.** Not the fold spread of either
model's level: the folds' own difficulty is shared by both models and cancels
in the paired delta (`metrics-and-gates.md` §1b; measured on hoopsq the level
sd across games was 0.0262 and the paired sd 0.0054). And the GLM must be a
*tuned* GLM: hoopsq's baseline at a fixed `C = 1` scored 0.6665 where a
CV-tuned ridge on the same columns scored **0.6429** — trees still won by
~0.014, but the claimed margin had been double that.

Bagging families (RF, ExtraTrees) trail by 0.03–0.04. That is consistent across
sports problems with smooth, largely monotone relationships: boosting fits the
shape, bagging averages over it.

---

## 2. What each family gives you that the others do not

| family | its actual advantage here |
|---|---|
| **CatBoost** | **native high-cardinality categoricals via ordered target statistics** — see §3. The only family that solves our entity-id problem inside the model. |
| **LightGBM** | speed. 0.1s where XGBoost took 0.4 and the MLP 5.9. For sweeps, LOSO validation, or per-season refits, this is the difference between an affordable experiment and a skipped one. Also `categorical_feature=` for mid-cardinality. |
| **XGBoost** | what the ecosystem ships, `.ubj` persistence, exact TreeSHAP via `pred_contribs`, `monotone_constraints`, and the objectives in `count-survival-ordinal.md`. Do not switch away without cause. |
| **HistGradientBoosting** | the same algorithm with **no third-party dependency**. Reach for it when a producer must not grow its dependency set. |
| **RandomForest / ExtraTrees** | out-of-bag error and low tuning sensitivity. Useful as a sanity model, rarely as the shipped one. |
| **Regularized linear (GLM)** | the baseline every other model must beat, plus coefficients a domain reader can argue with. |
| **MLP** | interactions boosting misses; competitive here but 15x the cost and it needs scaling, which means a `Pipeline` (`sklearn-xgboost.md` §C). |

**Monotone constraints** — available in **all three** boosting libraries
(verified: `xgboost`, `lightgbm` and `catboost` all accept
`monotone_constraints`). Not available in RF/ExtraTrees/MLP. If WP must be
monotone in score margin, that rules out three of the eight families.

---

## 3. CatBoost's ordered target statistics vs our leakage rule

`feature-engineering.md` §2 requires that target encoding on an entity be
computed **as-of, from prior rows only**. CatBoost's ordered boosting gets you
*part* of the way, and the distinction matters:

**By default (`has_time=False`, verified) CatBoost orders rows by a RANDOM
permutation, not by time.** Each row's target statistic excludes itself, which
prevents the self-leak that a naive full-sample encoding has — but a row can
still draw on games played *later* in the season. That is not as-of discipline.

For a time-ordered panel, set it explicitly:

```python
cb.CatBoostClassifier(cat_features=[0], has_time=True)   # respects input row order
```

with the frame **sorted chronologically** and the folds time-safe. `has_time=True`
makes the permutation the given row order, which is what turns the ordered
statistic into a genuine as-of encoding.

Measured on a 350-level team id (4,000 rows, 3,000 train / 1,000 holdout):

| encoding | holdout AUC |
|---|---:|
| naive full-sample target encoding | **0.872** ← saw the holdout rows |
| train-only target encoding | 0.821 |
| CatBoost `cat_features` (ordered, `has_time=False`) | 0.814 |

**The leak is worth 5 AUC points**, and it is the exact mistake a first
implementation makes. CatBoost's number is slightly *below* honest train-only
encoding here, which is the correct direction: ordered statistics are more
conservative because early rows in each permutation see fewer prior observations.

**Practical rule:** for a high-cardinality entity id — teams (~130 FBS, ~350
D-I), players (~5,000/season) — pass it to CatBoost as a `cat_feature` rather
than hand-rolling target encoding: it removes the self-leak and you cannot forget
it. **Add `has_time=True` with chronologically sorted input** whenever the panel
is time-ordered. When you must hand-roll (XGBoost, a GLM), the expanding
train-only mean plus shrinkage in `feature-engineering.md` §2 is the contract.

**Two cases where the ordered statistic is not the answer:**

- **Not every panel is time-ordered.** A fixed corpus of games validated by
  leave-one-game-out (hoopsq: 10 games, 1,324 shots) has no meaningful
  `has_time` order — the rows of a game are simultaneous for this purpose and
  the games are exchangeable. There the group split is the contract, not the
  row order; `has_time=True` on an arbitrary order is a random permutation
  with a misleading name. Say which regime the panel is in.
- **Per-entity n and an external prior.** An ordered statistic learns each
  entity from its own in-corpus rows. With a median of a few shots per shooter
  it learns almost nothing, and an **out-of-sample external aggregate** (a
  season-total rate with the evaluation units removed, `sklearn-xgboost.md`
  §A2) is the right tool instead — hoopsq's in-corpus shooter random effect
  added 0.0000, its penalized id block scored worse than no id, and the
  external prior was the only entity term that did not hurt (≈ 0). CatBoost
  ordered target statistics were never run there (`one_hot_max_size` swallowed
  the id), so the comparison is owed; the rule is: check the per-entity count
  before choosing between an in-model encoding and an external prior.

---

## 4. Stacking and bagging — AutoGluon's actual trick

AutoGluon's gains over any single model come mostly from **multi-layer stacking
with bagged base models**, not from a better base learner. Two things change on
our data:

- **Every fold in every bag must be a group fold.** Stacking generates
  out-of-fold predictions as features for the next layer; if those OOF
  predictions come from a shuffled split, the leak is laundered into a feature
  and the meta-learner cannot see it. Pass `groups` all the way down.
- **The meta-learner needs its own purge** when base features carry season
  memory (`sklearn-xgboost.md` §A2).

Given the 0.009 spread in §1, the honest expectation for stacking on a problem
like this is *small*. Spend the complexity budget on features and on
correct validation before spending it on an ensemble.

**If you run AutoGluon on SDV data, the minimum viable call is not the default:**
pass a group-aware split, hold out by season rather than at random, and score
against the oracle rather than the internal validation. Its leaderboard is a
model-selection tool, not a gate.

---

## 5. TabPFN and the small-n case

Prior-fitted transformers (TabPFN) target exactly the regime a lot of our
team-level work sits in: **~130 FBS teams in a season, ~350 D-I teams, 32 NFL
teams**. A single season of team-level data is a few hundred rows, which is the
regime where a boosted model overfits and a GLM is competitive.

Not installed here and not verified, so treat this as a pointer rather than a
recommendation: it is worth a bake-off against the GLM baseline on a
team-season problem, judged by the §1 rule that the winner must beat the
baseline by more than the fold spread.

---

## 6. How to choose, in order

1. **Fit the GLM first, and tune its penalty.** It is free and it sets the bar
   every other model must clear by more than the paired per-fold spread (§1).
2. **If the entity id is the feature and entities have enough rows, reach for
   CatBoost.** The ordered statistic is the whole reason; with a handful of
   rows per entity, an external out-of-sample prior does more (§3).
3. **If you are sweeping, use LightGBM.** Ten sweeps at 0.1s beat one at 5.9s.
4. **If it ships, use XGBoost** — persistence, TreeSHAP, monotone constraints
   and the objectives are all already wired into this ecosystem.
5. **If a dependency is unacceptable, use HistGradientBoosting.**
6. **Report the paired spread with the number**, always, seed-averaged for any
   stochastic learner. A model that wins by less than the paired per-fold
   standard deviation (or the seed sd) has not won — and "XGBoost wins" is
   only a claim when the other families had the same tuning budget (hoopsq:
   ~30 XGBoost variants against one configuration per other family; LightGBM
   tied on the same columns, 0.6328 vs 0.6320, and beat it on another set).
   Name the result at the level the evidence supports — "boosted trees", not
   one library.

## See also

- `sklearn-xgboost.md` — the panel-data failure families that apply to all of
  these, not just XGBoost.
- `interpretability.md` — explaining whichever one you pick.
- `count-survival-ordinal.md` — when the target is not binary or continuous.
- `resampling.md` — the interval around any of these numbers.
