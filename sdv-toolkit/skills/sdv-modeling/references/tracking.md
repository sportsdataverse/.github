# Tracking — the components a model, experiment, dataset and feature set need

> Reference file of the `sdv-modeling` skill. Added 2026-08-29. `sdv-data-pipeline`
> owns the *operational* half (registry row, one-job-per-model, publish); this
> file is the **architecture**: which components exist, what each one is
> responsible for, and which ones we do not have yet.

The generic answer to this question is MLflow plus a feature store plus a model
registry service. That answer is wrong here, and it is worth being precise about
why: **our artifact store is a GitHub release, our compute is GitHub Actions, and
our source of truth is a git repo.** A tracking layer that needs a running
service to be consulted is a layer that will be stale the first week nobody
restarts it.

So the design constraint is: **git-native, file-based, diffable, no daemon.**
Everything below is a file in the producer repo.

---

## 1. The six components

| # | component | answers | file | state |
|---|---|---|---|---|
| 1 | **fingerprint** | is this output current? | `<output>.fingerprint.json` | proposed |
| 2 | **dataset registry** | what do we publish, with what schema and coverage? | release tags + `loader_map.json` + `release_coverage.json` | **partial** |
| 3 | **feature-set registry** | which columns, built how, from what? | `features/<name>.yaml` | **missing** |
| 4 | **model registry** | what is promoted, trained on what, gated how? | `models/REGISTRY.md` | **exists** |
| 5 | **experiment ledger** | what was tried, what did it score, what shipped? | `models/ledger.jsonl` | proposed |
| 6 | **lineage** | which dataset fed which feature set fed which model fed which published dataset? | derived from 1-5 | **missing** |

Two of six exist. The gap that matters most is **3 and 6** — we can say what a
model is, and not what it was built *from*.

---

## 2. Fingerprints — the component everything else leans on

A fingerprint is a content hash of everything that determines an output:

```json
{
  "stage": "train-ep",
  "code": "<git sha of the package subtree>",
  "inputs": {"pbp_full.parquet": "<sha256>"},
  "features": "ep_v3@<sha of the feature-set yaml>",
  "hparams": "ep_default@<sha>",
  "produced_at": "2026-08-29T04:00:00Z",
  "run_id": "<actions run id>"
}
```

A stage is **skipped** when its fingerprint matches and its outputs exist, unless
`--force`. That single mechanism buys three things at once:

- **restart from any step** — a re-run resumes at the first changed stage
- **per-feature-set iteration** — changing a config changes the hash, so exactly
  the affected stages re-run
- **honest caching** — the reason a stage was skipped is a file you can read

**Hash the code subtree, not the repo.** A README edit must not invalidate a
model. `git rev-parse HEAD:python/cfb_model_build/model_training` gives the tree
sha for one package.

**And hash the *inputs*, not their paths.** A path is not identity: the same
`pbp_full.parquet` filename holds different content after a reprocess, which is
exactly the case that must invalidate.

---

## 3. The feature-set registry — the missing component, and how to build one

Today a model's feature list lives inside the training code. That makes three
things impossible: comparing two feature sets, knowing which datasets a model
depends on, and answering "what changed" when a metric moves.

### 3.1 The shape

```yaml
# features/ep_v1.yaml
name: ep_v1
version: 1
description: Start-of-play game state for the CFB expected-points model.
model: ep                       # the models/REGISTRY.md row this serves
sources:                        # which published datasets this needs
  - dataset: espn_cfb_pbp
    columns: [TimeSecsRem, yards_to_goal, distance, down_1, down_2, down_3,
              down_4, pos_score_diff_start]
columns:                        # what this feature set EMITS, IN ORDER
  - {name: TimeSecsRem,         dtype: Float64, transform: passthrough}
  - {name: yards_to_goal,       dtype: Float64, transform: passthrough}
  - {name: distance,            dtype: Float64, transform: passthrough}
  - {name: down_1,              dtype: Int64,   transform: onehot(down, 1)}
  - {name: down_2,              dtype: Int64,   transform: onehot(down, 2)}
  - {name: down_3,              dtype: Int64,   transform: onehot(down, 3)}
  - {name: down_4,              dtype: Int64,   transform: onehot(down, 4)}
  - {name: pos_score_diff_start, dtype: Float64, transform: passthrough}
contracts:
  - no_nulls: [down_1, down_2, down_3, down_4, yards_to_goal]
  - id_dtype: {game_id: Utf8}
leakage: none                   # all same-snap state; GroupKFold(game_id) suffices
```

Four fields carry the weight:

- **`sources`** makes lineage derivable — a model's dataset dependencies are the
  union of its feature set's sources. That is component 6, for free.
- **`columns` is ORDERED**, because XGBoost validates `feature_names` alignment
  only when the booster carries them, and several shipped boosters have
  `feature_names=None` (`sklearn-xgboost.md` §J). The order *is* the contract.
- **`leakage`** tells the splitter what purge this feature set needs. `none` for
  same-snap state; `as_of` with `purge_units` for anything carrying season memory
  (`sklearn-xgboost.md` §A2). Right now that knowledge lives in whoever wrote the CV.
- **`contracts`** is where `sdv-assuring-data-pipelines`' validation attaches (§6).

### 3.2 Build it by DERIVING it, never by authoring it

**The feature list already exists.** In `cfbfastR-cfb-data` it is
`EP_SOURCE`, `WP_SOURCE`, `FG_FEATURES`, `XPASS_FEATURES`, `QBR_FEATURES` and
`TWO_PT_FEATURES` in `model_training/constants.py`. Hand-writing YAML beside
those constants creates a second source of truth that drifts by the second
retrain.

Do it in this order, and do not skip step 3:

1. **Generate.** Walk the existing constants and emit one YAML per model. The
   first version must reproduce the current lists *exactly* — this is a
   description of what ships today, not a redesign.
2. **Gate the equality.** A test asserts, per model, that the YAML's ordered
   `columns` equals the code's list. At this point the YAML is redundant, which
   is correct: it earns trust before it earns authority.
3. **Invert the dependency.** Change the training code to read the YAML and
   delete the constant. *Now* the YAML is the source of truth and the gate in
   step 2 becomes a check on the booster instead.

Skipping to step 3 means a hand-written list silently disagrees with a shipped
model. Stopping at step 1 means a decorative file nobody trusts.

### 3.3 The gate has to actually bite

**Verify by deletion before trusting it.** `cfbfastR-cfb-data`'s existing
registry↔stage correspondence test matches on **package** names, not per-model
rows — deleting the `ep` row still passed, because sibling rows mention
`model_training`. "Every stage is mentioned somewhere" is much weaker than
"rows are mandatory" sounds.

So the feature-set gate must assert three things, each verified by breaking it:

| assertion | break it by |
|---|---|
| every model in `REGISTRY.md` has a feature set | deleting a YAML |
| the YAML's ordered columns equal what the training code builds | reordering two columns |
| every `sources.dataset` resolves to a real release tag / loader | renaming a source |

If a mutation does not turn the test red, the test is decorative — the same
finding as the registry test above.

### 3.4 What it unlocks immediately

- **"This dataset was republished — what needs retraining?"** Every model whose
  feature set names it in `sources`. That is the CFB parser-fix → reprocess chain
  we have hit repeatedly, answerable by grep instead of by memory.
- **"Why did the metric move?"** Diff two feature-set YAMLs. That is a reviewable
  PR diff rather than an archaeology exercise across training code.
- **The right purge, automatically.** `leakage: as_of` selects the purged
  splitter; `none` selects `GroupKFold`. The CV stops depending on whoever wrote it.

## 4. The experiment ledger

Append-only `models/ledger.jsonl`, one row per stage run, rendered to a readable
`models/LEDGER.md`:

| field | why it is there |
|---|---|
| `run_id`, `stage`, `fingerprint` | identity and reproducibility |
| `features`, `hparams` | what was actually varied |
| `metrics`, `gate_verdict` | the measurement and whether it passed |
| `fold_spread` | **required** — a delta smaller than this is not a result (`model-families.md`) |
| `delta_vs_champion` | the scientific unit: not "0.87" but "+0.004 over champion" |
| `promoted` (bool) + `note` (required on promotion) | forces a written reason |
| `breakthrough` (bool) | set when a gate improves beyond a stated threshold |
| **`in_published_data`** | `null` until a reprocess ships it, then that run id |

`fold_spread` is the addition this file makes to the earlier proposal. Every
comparison in `model-families.md` came down to it: eight families inside 0.044
AUC with a spread of 0.002–0.004 means a 0.005 "win" is noise. A ledger that
records the delta without the spread invites exactly that mistake, permanently.

**`in_published_data` is the field nothing currently tracks.** A feature can be
trained, gated, promoted, committed and released — and still not be in
`espn_cfb_pbp`, because reaching published data needs the 20,698-game reprocess.
`ledger check` flags rows where `promoted=true` and `in_published_data=null`
older than N days: work that was done and never shipped to consumers.

---

## 5. Lineage falls out; it should not be built

With 2, 3 and 4 in place, the lineage graph is derivable:

```
release dataset --(feature-set sources)--> feature set
    --(registry row)--> model
    --(ledger in_published_data)--> published dataset
```

Two questions become answerable that are currently reconstructed by hand:

- **"This dataset was republished — what needs retraining?"** Every model whose
  feature set names it as a source. That is the CFB parser-fix → reprocess chain
  we have hit repeatedly.
- **"This model changed — what did consumers see?"** Follow `in_published_data`.

Do not build a graph database. It is a query over four files.

---

## 6. Validation belongs to the assurance skill, applied at the feature layer

**`sdv-assuring-data-pipelines` already owns Great Expectations and Pandera** —
expectation suites, schema validation, the tool comparison, and the
OpenTelemetry/Prometheus observability half. Do not restate it here.

What this file adds is *where* to attach it. Today validation runs on **published
datasets**. The `contracts:` block in §3 puts the same machinery on **feature
sets and model inputs**, which is where the failures actually originate:

| checked today | should also be checked |
|---|---|
| published parquet schema | the frame handed to `.fit()` |
| null rates on a release | null rates per feature, per season |
| row counts | join match rates against the floor |
| dtype on a loader | id dtype agreement before every join |

Two SDV-specific expectations worth writing once and reusing, both of which
encode failures that already happened here:

- **`expect_column_pair_dtypes_to_match`** before a join — the `"123.0"`
  float-origin id problem.
- **`expect_season_coverage_to_be_complete`** — a quarters model reading zero
  rows from a halves-era season reported success (`failure-modes.md`). A row
  count of 0 must be an error, never a state.

---

## 7. What to build first

The order matters, and one sequence is actively wrong:

1. **Fingerprints** (§2). Highest value alone: restart, iteration and caching.
2. **Feature-set registry** (§3). Makes lineage derivable and turns leakage and
   join rules into checked data.
3. **Ledger with `fold_spread` and `in_published_data`** (§4).
4. **Feature-layer validation** (§6), reusing the assurance skill's tooling.
5. **Commit promoted artifacts** — *after* 3, never before. Committing binaries
   before the ledger exists puts them in git history with no provenance and no
   reason attached.

**Nothing here needs a service.** Five files, all diffable, all reviewable in a
PR, all readable by the next session without anything running.

## See also

- `sdv-data-pipeline` "Models are pipelines too" — the operational half: registry
  row, one-job-per-model CI, publish, and who owns which step.
- `sdv-assuring-data-pipelines` — Great Expectations, Pandera, and observability.
- `compute.md` §6 — fingerprints remove more wall-clock than any hardware change.
- `metrics-and-gates.md` §2 — the never-lower rule the `gate_verdict` field records.
