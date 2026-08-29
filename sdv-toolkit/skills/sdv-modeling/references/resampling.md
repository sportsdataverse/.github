# Resampling — bootstrap, jackknife and permutation on panel-sports data

> Reference file of the `sdv-modeling` skill. Added 2026-08-28 to close the
> highest-risk gap in the toolkit's coverage audit: bootstrap appeared 22 times
> and **cluster bootstrap zero times**.

Every interval this ecosystem might publish comes from a resample. The toolkit
already documents at length why a bare `KFold` is wrong on our data
(`sklearn-xgboost.md` §A) — **the identical argument applies to resampling and
was never carried over**. A row-level bootstrap on play-by-play understates the
standard error for exactly the same reason: rows within a game are not
independent draws.

Only numpy is needed for everything in this file. No optional dependency.

---

## 1. The size of the error, measured

The understatement is not a rounding concern. Simulated on a realistic panel —
300 games × 150 plays, with a game-level random effect giving an intraclass
correlation of 0.5:

| resample | SE of the mean |
|---|---:|
| row-level bootstrap | 0.00686 |
| **cluster bootstrap (by game)** | **0.06056** |

**The naive interval is 8.8× too narrow.** That matches the design-effect
formula almost exactly:

```
design effect  =  sqrt(1 + (m - 1) * ICC)
               =  sqrt(1 + 149 * 0.5)  =  8.69x
```

where `m` is the average cluster size and `ICC` the intraclass correlation. Read
the formula before you argue the effect is small on your data: **it scales with
cluster size**, and our clusters are large. A 150-play game with even a modest
ICC of 0.05 still gives a 2.9× understatement.

A 95% interval that is 8.8× too narrow is not a slightly optimistic interval. It
is a published number asserting a precision that does not exist.

---

## 2. Cluster bootstrap — the default for anything play-level

**Resample whole clusters with replacement, then take every row in the chosen
clusters.** The cluster is the unit at which observations are independent. In
this ecosystem that is almost always `game_id`.

```python
import numpy as np


def cluster_bootstrap(stat_fn, values, groups, n_boot=1000, seed=0):
    """Bootstrap a statistic by resampling whole groups, not rows.

    Args:
        stat_fn: Callable taking the resampled values and returning a scalar.
        values: Array (or 2-D array of rows) the statistic is computed on.
        groups: Cluster label per row -- `game_id` for play-level data.
            The cluster must be the level at which rows are INDEPENDENT; see
            section 3 for the cases where `game_id` is the wrong choice.
        n_boot: Number of bootstrap replicates.
        seed: RNG seed. Always set one -- an unseeded interval is not
            reproducible and cannot be compared across runs.

    Returns:
        The array of bootstrap replicates. Take a percentile interval from it,
        or its standard deviation as the standard error.
    """
    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    keys = np.unique(groups)
    # Index once. Rebuilding the membership per replicate is the difference
    # between seconds and minutes on a season of plays.
    members = {k: np.flatnonzero(groups == k) for k in keys}
    out = np.empty(n_boot)
    for b in range(n_boot):
        picked = rng.choice(keys, size=len(keys), replace=True)
        rows = np.concatenate([members[k] for k in picked])
        out[b] = stat_fn(values[rows])
    return out
```

**Detection test.** The assertion is not "the interval exists" — it is that
clustering *changed* it. If the two agree, either the data has no within-cluster
correlation (check, do not assume) or the clustering was applied to the wrong
column.

```python
def assert_clustering_matters(values, groups, tol=1.15, seed=0):
    """Fail if the cluster bootstrap SE is not meaningfully wider than the naive one.

    A cluster SE that matches the row-level SE means the grouping had no effect,
    which on play-by-play data means the grouping is wrong -- not that the data
    is independent.
    """
    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    n = len(values)
    naive = np.std([values[rng.integers(0, n, n)].mean() for _ in range(400)], ddof=1)
    clustered = cluster_bootstrap(np.mean, values, groups, n_boot=400, seed=seed).std(ddof=1)
    assert clustered > tol * naive, (
        f"cluster SE {clustered:.5f} is not > {tol}x naive SE {naive:.5f} -- "
        "check that `groups` is the game/entity id and not a row index"
    )
```

Would this fire? Yes — on the simulated panel above it separates 0.061 from
0.0069. It fails when `groups` is passed a unique-per-row value, which is the
realistic way to get this wrong.

---

## 3. Choosing the cluster — the part that is actually hard

`game_id` is the default, not the answer. Pick the level at which two
observations stop sharing information:

| what you are estimating | cluster on | why |
|---|---|---|
| a play-level rate (success %, EPA/play) | `game_id` | plays share game script, weather, officials, opponent |
| a team-season statistic | `team_id` | a team's games are not independent of each other |
| a player statistic across seasons | `player_id` | the same player is one draw, not N |
| a rating fitted across a league | **`game_id`, but see below** | each game informs two teams |
| a stint-level RAPM quantity | `game_id`, not `stint_id` | stints within a game share lineups and context |

**Two clusterings at once.** A team-season panel is correlated *within team* and
*within season* — a rule change or a scheduling quirk hits every team in a year.
The honest answer there is a two-way cluster, and the cheap approximation is to
cluster on whichever dimension gives the **wider** interval, then say so. Never
pick the narrower one because it looks better.

**The block bootstrap for ordered data.** When the dependence is temporal rather
than grouped — a rating series across weeks — resample contiguous *blocks* of
length `L` rather than single observations, with `L` at least as long as the
dependence you believe exists. Same code as above with `groups` set to a block
index (`np.arange(n) // L`).

---

## 4. Jackknife — when you want influence, not an interval

Leave-one-cluster-out gives you both a variance estimate and, more usefully,
**which cluster is driving the result**.

```python
def jackknife_by_cluster(stat_fn, values, groups):
    """Leave-one-cluster-out estimates. Returns (keys, per-key estimate).

    The spread is a variance estimate; the OUTLIERS are the point. A rating that
    moves materially when one game is removed is a rating built on one game.
    """
    values = np.asarray(values)
    keys = np.unique(groups)
    return keys, np.array([stat_fn(values[groups != k]) for k in keys])
```

This is the cheapest available check on a small-sample entity: if dropping a
single game moves a player's season number by more than its own interval, the
number is not a season estimate.

---

## 5. Permutation tests — for "is this effect real at all"

When the null is *no association* and the sampling distribution is awkward
(a Spearman correlation against an oracle, a crew effect, a home-field effect),
permute the labels **within the cluster structure** and recompute.

```python
def cluster_permutation_test(stat_fn, values, groups, labels, n_perm=2000, seed=0):
    """Two-sided p-value from permuting labels ACROSS clusters, not rows.

    Permuting row labels destroys the clustering along with the association and
    produces a null that is far too tight -- the same error as the row-level
    bootstrap, in the other direction.
    """
    rng = np.random.default_rng(seed)
    values, labels = np.asarray(values), np.asarray(labels)
    keys = np.unique(groups)
    # One label per cluster: the treatment is assigned at cluster level
    # (a crew works a game; a rule applies to a season), so that is the level
    # the permutation must respect.
    per_key = np.array([labels[groups == k][0] for k in keys])
    observed = stat_fn(values, np.array([dict(zip(keys, per_key))[g] for g in groups]))
    count = 0
    for _ in range(n_perm):
        shuffled = rng.permutation(per_key)
        mapped = np.array([dict(zip(keys, shuffled))[g] for g in groups])
        if abs(stat_fn(values, mapped)) >= abs(observed):
            count += 1
    return (count + 1) / (n_perm + 1)  # +1 keeps p > 0; a p of exactly 0 is a lie
```

---

## 5b. Classical tests, and why they mostly do not apply here

A t-test, a chi-square, a Pearson or Spearman significance test, a Shapiro-Wilk —
every one of them assumes independent observations. On play-level data none of
them hold, and each is anti-conservative in the same direction as the row-level
bootstrap.

| you want | do NOT | do |
|---|---|---|
| compare two groups of plays | `ttest_ind` | cluster bootstrap the difference in means (§2) |
| test an association | `pearsonr` p-value | cluster permutation test (§5) |
| compare a rate across eras | chi-square on plays | aggregate to game or season, then test |
| check normality | Shapiro-Wilk on plays | it will reject on any real sample of this size; check the residual plot instead |

The general escape hatch is **aggregate to the cluster level first**. A test on
300 game-level means is honest; the same test on 45,000 plays is not, and its
p-value will be smaller by roughly the design effect.

`scipy.stats` has all of these and none of them know about your groups.

---

## 6. Where this composes with the rest of the skill

- **Conformal intervals** (`metrics-and-gates.md` §1) need a calibration split
  that respects the same clustering — split by game, never by row, or the
  residuals are not exchangeable with the test set.
- **Purged CV** (`sklearn-xgboost.md` §A2) handles the *training* side of the
  same dependence. This file handles the *inference* side. A model can be
  correctly cross-validated and still ship an 8x-too-narrow interval.
- **Stabilization analysis** (see `literature.md`) uses split-half reliability,
  and the halves must be split by cluster for the identical reason.

**The rule to carry:** anywhere the toolkit says "assert dtype agreement before a
join", the parallel rule here is **assert the cluster before a resample**. Both
are one line, and both catch a class of silently-wrong published number.
