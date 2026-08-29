# Tabular deep learning — what the benchmark literature actually found

> Reference file of the `sdv-modeling` skill. Added 2026-08-28. Every abstract
> below was read from the paper's arXiv page, not recalled.

The question "should we use a neural net for this?" has a strong empirical
literature and a boring answer, and knowing the answer saves weeks. This file
exists so nobody re-runs that experiment on SDV data by accident.

---

## 1. The four papers that settle it

| paper | finding, quoted or closely paraphrased from the abstract |
|---|---|
| **Grinsztajn, Oyallon & Varoquaux (2022)**, *Why do tree-based models still outperform deep learning on tabular data?* — NeurIPS D&B, [arXiv:2207.08815](https://arxiv.org/abs/2207.08815) | Across a standardized 45-dataset benchmark, **tree-based models remain state of the art on medium-sized data (~10K samples) even without accounting for their superior speed.** The gap is *not* mostly due to categorical features and *does not disappear after tuning*. |
| **Shwartz-Ziv & Armon (2021)**, *Tabular Data: Deep Learning is Not All You Need* — [arXiv:2106.03253](https://arxiv.org/abs/2106.03253) | **XGBoost outperforms the proposed deep models across datasets — including the datasets used in the papers that proposed those deep models** — and requires much less tuning. On the positive side, **an ensemble of deep models and XGBoost beat XGBoost alone.** |
| **Gorishniy et al. (2021)**, *Revisiting Deep Learning Models for Tabular Data* — [arXiv:2106.11959](https://arxiv.org/abs/2106.11959) | The field lacked effective baselines. Two simple architectures raise the bar: a **ResNet-like** MLP that is a strong baseline often missing from prior work, and **FT-Transformer**. |
| **Erickson et al. (2020)**, *AutoGluon-Tabular* — [arXiv:2003.06505](https://arxiv.org/abs/2003.06505) | Unlike frameworks focused on model/hyperparameter selection, AutoGluon **succeeds by ensembling multiple models and stacking them in multiple layers**; that multi-layer combination uses the training-time budget better than searching for the single best model. |

**What this means for us.** The two benchmark papers say a boosted tree is the
right default on tabular data of our size, and the ecosystem already ships
XGBoost everywhere — so the default is correct and nothing needs to change. Our
own measurement agrees and adds a sharper point (`model-families.md`): on a
WP-shaped panel, **eight families landed inside 0.044 AUC and the top six inside
0.009, with a fold-to-fold spread of 0.002–0.004.**

The two constructive findings are the ones worth acting on:

- Shwartz-Ziv & Armon's *ensemble* result and AutoGluon's *stacking* result point
  the same way: the gain is in combination, not in a better single learner.
- Gorishniy's point about missing baselines is the one that applies hardest here.
  In our measurement **logistic regression was 0.009 AUC behind the best model at
  zero cost.** If a deep model is proposed for an SDV problem, the bar it must
  clear is the GLM, by more than the fold spread.

---

## 2. TabPFN — the one regime where this changes

**Hollmann, Müller, Eggensperger & Hutter**, *TabPFN: A Transformer That Solves
Small Tabular Classification Problems in a Second*, [arXiv:2207.01848](https://arxiv.org/abs/2207.01848).
From the abstract: it does supervised classification for **small** tabular
datasets in under a second, **needs no hyperparameter tuning**, and is
competitive with state-of-the-art methods. It performs in-context learning — a
single forward pass over the labeled examples, no parameter updates — as a
Prior-Data Fitted Network approximating Bayesian inference over synthetic
datasets drawn from a causal-reasoning-informed prior.

**Why this is interesting for SDV specifically:** a great deal of our team-level
work lives in exactly the small-n regime the method targets.

| problem | rows |
|---|---:|
| one NFL season, team level | 32 |
| one FBS season, team level | ~134 |
| one D-I basketball season, team level | ~350 |
| one season of NCAA tournament games | 67 |

At those sizes a boosted tree overfits, a GLM is competitive (§1), and tuning
cost dominates. That is the description of TabPFN's target regime.

**Not verified here** — it is not installed and no SDV bake-off has been run.
Treat this as the one deep-learning direction with a real prior for working on
our data, and judge it by `model-families.md`'s rule: it must beat the GLM
baseline by more than the fold spread, under a group- or season-aware split.

---

## 3. If you do fit a neural net here, three things bite

1. **Scaling is mandatory and belongs in the `Pipeline`.** An unscaled MLP on
   raw `yardline_100`, `time_left` (0–3600) and `down` (1–4) is dominated by
   whichever feature has the largest range. Outside a `Pipeline`, the scaler
   also leaks fold statistics — `sklearn-xgboost.md` §C.
2. **No monotone constraints.** All three boosting libraries accept
   `monotone_constraints`; MLPs, RF and ExtraTrees do not
   (`model-families.md` §2). If WP must be monotone in score margin, a neural
   net cannot give you that guarantee — only a post-hoc PDP check
   (`interpretability.md` §3), which detects violations rather than preventing
   them.
3. **Cost.** In our benchmark the MLP was the most accurate model *and* 15x
   slower to fit than LightGBM for 0.0015 AUC. On a per-season refit or a
   hyperparameter sweep that difference decides what experiments are affordable.

**Entity embeddings** are the one genuinely neural idea with a natural fit here:
learning a dense vector per team or player instead of one-hot or target
encoding. It is the same problem CatBoost's ordered target statistics solve
(`model-families.md` §3) and carries the same leakage hazard — an embedding
trained on the full season has seen the holdout. Train it inside the fold.

---

## 4. The honest summary

- **Default to boosted trees.** Two independent benchmark papers and our own
  measurement agree.
- **Always fit the GLM baseline**, because the literature's own critique is that
  baselines were missing, and on our data it is nearly free and nearly as good.
- **Spend complexity budget on features, validation and intervals**, not on
  architecture. CFB pregame improved 15.14 → 12.97 MAE by *removing* features
  (60 beat 244, `prior-art.md`); no architecture change in the literature offers
  a gain of that size on this kind of data.
- **The two places deep learning has a real case here** are TabPFN in the
  small-n team-season regime, and entity embeddings for high-cardinality ids —
  both testable against the GLM bar.

## See also

- `model-families.md` — the measured bake-off across eight families.
- `interpretability.md` — how to check whichever model you pick.
- `sklearn-xgboost.md` — the panel-data failures that apply regardless of family.
