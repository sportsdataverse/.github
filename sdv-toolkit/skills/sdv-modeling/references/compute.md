# Compute — GPU, torch, and parallelism, for the jobs we actually run

> Reference file of the `sdv-modeling` skill. Added 2026-08-29. The toolkit had
> no GPU or torch coverage on the modeling surface at all; the only mentions
> anywhere were in the polars and notebook skills.

The honest starting point: **most SDV model training does not need a GPU.** An
XGBoost fit on a season of plays takes seconds on CPU (measured, 0.4s in
`model-families.md`), and a GPU adds transfer overhead for no gain. This file is
about the four cases where compute genuinely bites, and about not fooling
yourself that you are using hardware you are not.

---

## 1. The XGBoost GPU API changed, and the old form now raises

**`tree_method="gpu_hist"` is removed in XGBoost 3.x.** Verified against 3.4.1:

```
XGBoostError: Invalid Input: 'gpu_hist', valid values are:
  {'approx', 'auto', 'exact', 'hist'}
```

The modern form separates *device* from *algorithm*:

```python
xgb.XGBClassifier(device="cuda", tree_method="hist")   # correct on 2.0+
xgb.XGBClassifier(tree_method="gpu_hist")              # raises on 3.x
```

Any training script written before XGBoost 2.0 carries the old spelling and will
fail outright on the current version. That is the good case — it fails loudly.

## 2. `device="cuda"` does NOT fail when there is no GPU

Measured on a CPU-only box (`torch.cuda.is_available() == False`):

```python
m = xgb.XGBClassifier(device="cuda", tree_method="hist").fit(X, y)   # succeeds
json.loads(m.get_booster().save_config())["learner"]["generic_param"]["device"]
# -> 'cuda:0'
```

**The fit succeeds, prediction works, and the booster reports its device as
`cuda:0` on a machine with no CUDA device.** XGBoost emits a C++-level warning
about a device mismatch, but it did not surface through Python's
`warnings.catch_warnings` in testing — `len(w) == 0` inside the context manager.

So neither of the two obvious checks works: you cannot detect this by catching
warnings, and you cannot detect it by reading the booster's config, because both
say cuda.

**Check the hardware before the fit, not the model after it:**

```python
def assert_gpu_available():
    """Fail before training, not after a silently-CPU run finishes.

    A job requested with device="cuda" that quietly ran on CPU is the expensive
    version of this mistake: it completes, the artifact is correct, and the
    timing budget for the next run is set from a number that means nothing.
    """
    import subprocess
    try:
        subprocess.run(["nvidia-smi"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        raise RuntimeError("device='cuda' requested but no CUDA device is present") from e
```

This is the same failure family as everything in `failure-modes.md`: the
component ran, reported success, and did not do the thing.

---

## 3. Where GPU actually helps here, and where it does not

| workload | GPU? | why |
|---|---|---|
| a single XGBoost fit on a season | **no** | 0.4s on CPU; transfer overhead dominates |
| a hyperparameter sweep or LOSO over 20 seasons | **maybe** | it is many fits, but they parallelize across *cores* just as well |
| RAPM / APM on a league-season sparse design | **sometimes** | see §4 — the win is the solver, not the device |
| a season simulator, 10k+ replicates | **no** | embarrassingly parallel across processes; use cores |
| entity embeddings or a tabular transformer | **yes** | the one genuinely GPU-shaped model family we might build |
| TabPFN in the small-n team-season regime | **yes** | a forward pass, and the published claim is sub-second |

**The default answer is more cores, not a GPU.** `n_jobs=-1` on the estimator,
or a process pool over seasons, gets most of the available speedup for none of
the setup. Reach for a GPU when the model is a neural net, not when the job is
merely slow.

---

## 4. Sparse solves — the RAPM case

`sklearn-xgboost.md` §B2 covers solver choice (`sparse_cg`, `lsqr`, `lsmr`) and
that is usually the whole answer. If you do want the GPU for a very wide design,
the bridge is direct:

```python
import scipy.sparse as sp, torch, numpy as np

A = sp.coo_matrix(design)                       # players x stints, ~1% dense
t = torch.sparse_coo_tensor(
    np.vstack([A.row, A.col]), A.data, A.shape, device="cuda"
)
# torch.sparse.mm for the normal-equations product; torch.linalg.lstsq for dense.
```

Verified available: `torch.sparse_coo_tensor`, `torch.sparse.mm`,
`torch.linalg.lstsq`.

**Measure before you port.** The `assert_stays_sparse` check in
`sklearn-xgboost.md` §B2 catches the actual usual problem — a design that
densified — and fixing that is worth more than a device change. A dense
10,000×10,000 solve is slow on a GPU too.

---

## 5. Torch, when you do reach for it

Only one model family in this ecosystem is genuinely torch-shaped: **entity
embeddings** for high-cardinality ids (`tabular-deep-learning.md` §3). If you
build one, three rules carry over unchanged:

- **The embedding is fit on data and therefore leaks.** Train it inside the CV
  fold, exactly like a target encoder (`feature-engineering.md` §2). An
  embedding trained on the full season has seen the holdout.
- **Seed everything and record the seed.** `torch.manual_seed`, the numpy
  generator, and the dataloader's shuffle. Non-determinism in a model whose
  output is published is not acceptable (`sklearn-xgboost.md` §G).
- **Distributed training is out of scope and should stay that way.** Our largest
  training frame is a few million rows; that is a single-machine problem. If a
  proposal needs multi-GPU, the first question is whether the feature set is
  wrong, not whether the cluster is too small — CFB pregame improved by
  *removing* 184 features.

---

## 6. Parallelism that actually pays, in order

1. **`n_jobs=-1`** on the estimator. Free.
2. **A process pool over seasons or over sweep configurations.** The natural
   grain: each unit is an independent fit, and cross-season leakage is
   impossible by construction.
3. **Cache the expensive input once.** Most "slow training" here is re-deriving
   the same frame per stage. Stage fingerprints (`tracking.md`) fix that
   properly; a parquet on disk fixes it today.
4. **Only then, hardware.**

For scraping and backfill parallelism — a different problem with different
constraints — `sdv-data-pipeline` Phase 3 is the authority; keep concurrency low
and rate limits env-only.

## See also

- `tracking.md` — fingerprints, which remove more wall-clock than any device change.
- `sklearn-xgboost.md` §B2, §G, §I — solver choice, determinism, and sparse densification.
- `model-families.md` — the CPU timings that make the "do you need a GPU" case.
