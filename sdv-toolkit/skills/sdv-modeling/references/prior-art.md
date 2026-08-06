# Prior art — has this been tried?

"Has this been tried, and what happened?" Distilled from five SDV-model-program
documents in `ClaudeCowork/` (roadmap, two survey bundles, an NBA mimicry-gap
spec, a program-status snapshot) plus two sections of the `sdv-py/dev/apm-research/`
survey bundle (gitignored, no other copy exists — same corpus `methods.md` draws
its method mechanics from). Every claim below cites the source file it came
from. Where the roadmap and the later status note disagree, the status note
wins — flagged explicitly below each time it happens.

Shorthand used in citations:

| Shorthand | Full path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `roadmap.md` | `ClaudeCowork/plans/2026-07-17-sdv-model-roadmap.md` |
| `survey-reports.md` | `ClaudeCowork/notes/2026-07-17-sdv-model/survey-reports.md` |
| `reference-port-surveys.md` | `ClaudeCowork/notes/2026-07-17-sdv-model/2026-07-22-reference-port-surveys.md` |
| `model-zoo-v2-gap-analysis.md` | `ClaudeCowork/nba_data/specs/2026-07-02-model-zoo-v2-mimicry-gap-analysis.md` |
| `program-status.md` | `ClaudeCowork/notes/2026-07-17-sdv-model/program-status-2026-07-21.md` |
| `apm-research/deep-research-report.md` | `sdv-py/dev/apm-research/deep-research-report.md` (gitignored) |
| `apm-research/code-catalog.md` | `sdv-py/dev/apm-research/code-catalog.md` (gitignored) |

---

## 1. Built and shipped

### NBA APM / projection zoo — lives in `sdv-py` main today

Merged as of the 2026-07-02 gap-analysis snapshot, one module per system,
league-agnostic so WNBA/G-League inherit the same code:

| Module | PR | Mimics | Fidelity |
|---|---|---|---|
| `nba_rapm` | #139 | plain RAPM | single/pooled-season ridge on the possession stint matrix |
| `nba_adj_rapm` | #156 | xRAPM / EPM *skeleton* | Bayesian ridge toward a prior mean (residualized ridge + RTO posterior for credible intervals); priors from SPM or BPM |
| `nba_spm` | #154 | SPM (box→RAPM) | ridge on box-only per-100 features, separate O/D regressions |
| `nba_bpm` | #155 | B-Ref BPM 2.0 | published coefficients, position/role regression, team adjustment, LeBron 2016-17 anchor |
| `nba_darko` | #157 | DARKO *reduced form* | per-player Kalman on a **season-level composite** rating + delta-method aging curve; deliberately not the real DARKO's daily per-stat state-space (see §3) |
| `nba_model_validation` + `nba_season_compile` | #153 | the field's own validation | 4 oracles: holdout game-margin retrodiction, split-half reliability, cross-season predictivity, interval calibration |

(`model-zoo-v2-gap-analysis.md` §1 table.) Real external oracle CSVs already on
disk for these (Ryan Davis RAPM, Dunks&Threes EPM, DARKO DPM, LEBRON) are
listed in the same document §1 — used to score, not to re-derive, the mimicry.

### Validation harness, calibration primitives, season sims — also `sdv-py` main

- **Validation harness** `tools/validation/`: six check families wired in
  `cli.py` (`schema_contract`, `extraction`, `numeric_parity`, `sweep`,
  `boundary_leakage`, `constant_column`) plus Python/R leakage lint and
  Tier-2 triage subagents; `NflfastrOracle` (corr floors 0.99) and
  `CfbSelfOracle`. (`survey-reports.md` Report 4 §1.)
- **Calibration/baseline metrics**: `sportsdataverse/_common/metrics.py` ships
  `brier_score`, `calibration_table(y_true, p_pred, n_bins=10)`,
  `log_loss_score`, `spearman_corr`, `mae`, re-exported into every spine's
  `*_prediction_constants` / `*_projection_constants`. No shared
  beat-the-baseline comparator existed at this snapshot — baseline
  comparison was inline per-model. (`survey-reports.md` Report 4 §2.)
- **Season/tournament Monte Carlo**: `nfl_simulations.py` (nflseedR v2 port),
  `cfb_simulations.py` (week-loop Elo), `mbb_season_sim.py` +
  `mbb_bracketology.py`, `wbb_season_sim.py` + `wbb_bracketology.py`. No
  possession-level generative sim existed under `nba/` at this snapshot —
  `nba_play_context.py` was labeling, not a simulator. (`survey-reports.md`
  Report 4 §6.)
- **sdv-db Dataset catalog**: `sdv_db/catalog.py` `Dataset` dataclass is an
  ingest declaration only (league/name/source/loader/module/partition_col/
  asset_url) — no schema/dtype contract, no expected row ranges, no
  freshness field at this snapshot. (`survey-reports.md` Report 4 §3.)

### The much larger "SDV model program" (WS1–WS6 + reference-port waves) — built, but NOT in sdv-py

Starting 2026-07-17 a six-workstream program, WS1–WS6 (publish-integrity gate,
eval/experiment-ledger, declarative FeatureSet layer, a full generative
possession/drive/event-stream simulator for all nine SDV sports, odds/markets
math, and opportunistic fold-ins including the per-league feature-catalog port
of a reference stack) was built and gated on real fixtures across dozens of
addenda. (`roadmap.md` "Sequencing & effort" table, WS1–WS6.) **Its final home is not
`sdv-py`.** The 2026-07-22 delivery decision (the later of the roadmap's many
status updates, and the one recorded last in `program-status.md` too)
supersedes every earlier "ship vehicle: sdv-py PR" note in the roadmap's
original workstream table:

> "sdv-engine is the SOLE home of the entire sdv-model surface, and
> sportsdataverse-py main never carries it." The donor branch `feat/sdv-model`
> never merges and stays frozen as porting provenance; sdv-py "keeps
> nothing." (`roadmap.md` Addendum 22; confirmed in `program-status.md`
> "Delivery decision — 2026-07-22".)

`sdv-engine` (import `sdvengine`) is a standalone local-git-only repo with no
GitHub remote and a `Private :: Do Not Upload` PyPI classifier, so an
accidental publish is structurally blocked. (`roadmap.md` Addendum 21.) It
carries `modeling/{integrity,eval,features,registry}` (publish-audit
fingerprint+drift+completeness, experiment ledger, `FeatureSetSpec`,
`learned_bins`, `mixed_effects`, `model_registry`/`ModelCard`,
`DataContract`), `sims/{basketball,football,football_college,baseball,hockey,
wnba,mbb,wbb}` (possession-tree / drive-state-machine / event-stream engines
for all nine sports, each gated by a conservation oracle that reconstructs a
real final score exactly), `playtext` (a provider-dialect play-text renderer
registry), and `odds_math` (no-vig, copula-correlated parlay pricing).
(`roadmap.md` Addendum 13 module inventory, Addendum 10 "Design 2 modeling
library".) In a later reversal of the original dependency direction,
`sportsdataverse` (sdv-py) itself became a direct **editable-path dependency
of** `sdv-engine` — the engine consumes sdv-py's loaders, not the other way
around. (`roadmap.md` Addendum 28.)

**Practical consequence for anyone routed here by the decision tree:** if you
are looking for `_common/publish_audit.py`, `modeling/eval/metrics.py`,
`nba_possession_sim/`, or `odds/odds_math.py` inside `sdv-py`, they are not
there — that surface exists only in the private `sdv-engine` checkout. Only
the NBA APM/projection zoo, the validation harness, `_common/metrics.py`,
and the four sport season-sims above are in `sdv-py` main.

---

## 2. Surveyed and rejected

### Explicit anti-pattern list (not imported from the reference stack)

`eval(argv[1])` dict-literal CLIs; filename-suffix model versioning
(`_000015`, estimator-variant suffixes — `survey-reports.md` Report 1 item
36); magic-number role/position ids in SQL with no enum (same item 36);
500-model sprawl without a registry (the program's experiment ledger is the
registry instead); model-on-model features without dependency tracking;
unthresholded "eyeball the ratio table" acceptance (replaced by the
deterministic Tier-1 harness); heavyweight cache/broker infra where a
parquet file plus a dict suffices; monolithic 100KB+ `Game` classes (the
NBA `Node` event-tree pattern was ported instead, because it is the one
sport whose sim code was already decomposed into ~20 per-event classes —
`survey-reports.md` Report 1 item 19's `DecisionTreeNode.py`).
(`roadmap.md` "Explicitly NOT importing (anti-patterns)"; `survey-reports.md`
Report 1 items 19 and 36.)

### Infra swaps rejected outright

- **LMDB `Shelf` key-value cache** — skipped; the program's own in-memory +
  parquet shelf round-trip already "wins local-first." (`reference-port-surveys.md`
  Tree C port-ranking table item 5; Tree D item 10.)
- **Redis prob-array strip codec** (zlib+float32 buffers) — skipped; ensemble
  distributions stay in parquet/in-memory frames instead.
  (`reference-port-surveys.md` Tree C item 14.)
- **MySQL ORM + event-broker + distributed poller/scaler infra** — replaced
  wholesale, not ported: MySQL → PostgreSQL via `psycopg`, S3/boto3 →
  DigitalOcean Spaces, event-broker → dropped entirely (no equivalent built).
  (`survey-reports.md` Report 2 shared-library section; `reference-port-surveys.md`
  Tree C "BACKEND DIRECTIVE".)
- **shared-library "orphans"** (serving layer, distributed orchestration) —
  evaluated when the rest of the shared library was promoted into
  `sdvengine/modeling/`, and explicitly "stay rejected." (`roadmap.md`
  Addendum 10.)

### Scope decisions later reversed — an honest "prefer the later note" case

Two decisions were stated as firm design calls early in the program and then
quietly overturned by later addenda in the *same* document:

- **"NHL stays direct-xG by design, no generative engine"** was recorded as a
  deliberate tiering decision — "match modeling depth to data + value."
  (`survey-reports.md` Report 1 item 33.) Two weeks later the same program
  shipped `nhl/nhl_game_sim.py`, a full event-stream simulator gated on a
  real Stanley Cup Final Game 7 fixture. (`roadmap.md` Addendum 3.) The later
  build supersedes the earlier "stays direct" framing — treat the original
  rationale as abandoned, not as a standing constraint.
- **Player-level football simulation** was rejected once, on the grounds that
  "player-level football sim is NOT portable (no participation data)" —
  team/drive-level sim was adopted instead as a win-probability complement.
  (`roadmap.md` WS4.) This decision was **not** reversed in any later
  addendum; the shipped `nfl/nfl_drive_sim.py` / `cfb/cfb_drive_sim.py`
  (`roadmap.md` Addendum 3) stay team/drive-level, and a later addendum
  separately notes CFB participation data is still unavailable at the
  on-field-list grain needed for a true participation base (§3 below).

### Lasso (L1) regularization — no recorded rejection rationale

`methods.md`'s RAPM catalog lists five different Ridge implementations
(sklearn `RidgeCV`, `glmnet`, hand-specified alpha grids) and zero Lasso
implementations across every corpus document read for either file. The
academic lineage (below) records that Omidiran (2011) introduced L1/Lasso
APM specifically to force low-impact or highly-collinear player coefficients
to exactly zero — a real, documented alternative to Ridge's shrink-but-never-zero
behavior. **The corpus never records an explicit "we evaluated Lasso and
rejected it because X" decision anywhere in the five program documents or
the two apm-research files read for this task.** The honest read is: every
implementation surveyed independently converged on Ridge, and Lasso is an
unexplored alternative, not a rejected one.

### Dead, moved, or hallucination-risk artifacts

Several heavily-cited player-impact systems do not exist as clonable public
code — worth recording explicitly so nobody (human or agent) confidently
cites source that isn't there:

- **DARKO (Kostya Medvedovsky)** — no public GitHub repository. The
  methodology (exponential decay, Kalman state-space updating) is published;
  the implementation is proprietary to Medvedovsky and his API.
- **PIPM (Jacob Goldstein)** — public updates and open-source code ceased
  after Goldstein was hired by the Washington Wizards. His luck-adjustment
  methodology (replacing 3P%/FT% outcomes with expected values) must be
  reconstructed from BBall-Index and Nylon Calculus blog posts, not code.
- **Deshpande & Jensen (2016)** win-probability APM — the authors never
  released a GitHub repository for their exact MCMC implementation. The
  `cmu_score_preprints` and `nick3703` repositories provide PyMC3/Stan
  architectures that can replicate the *approach*, not the original code.
- **Squared2020 (Ryan Davis) historical RAPM** (1984-1996 reconstructions) —
  data is shared via Google Sheets/Pastebin, not a centralized GitHub ETL
  repo; `tonyelhabr/nba-rapm` ships a `squared2020-setup.R` helper that
  references this work without containing it.
- **"hwchase17 basketball RAPM"** — does not exist as a distinct repository.
  Harrison Chase (`hwchase17`) has authored unrelated sports-AI/RAG code
  (RAPTOR-adjacent implementations); searches conflating that with an actual
  statistical APM solver are a pure hallucination risk.

(All five: `apm-research/code-catalog.md` §4 "Dead, Moved, or
Hallucination-Risk Artifacts".)

### The *prism* academic lineage

The Ridge-regression RAPM family every SDV implementation is built on traces
to five papers (`apm-research/deep-research-report.md` §5):

- **Sill, J. (2010)**, "Improved NBA adjusted +/- using regularization and
  out-of-sample testing" — introduced Ridge Regression (RAPM) itself,
  validated via out-of-sample cross-validation against future game outcomes.
  This is the origin of every Ridge implementation in `methods.md`'s catalog.
- **Engelmann, J.** (various / ESPN) — pioneered fusing box-score-derived
  Statistical Plus-Minus priors with RAPM to shorten the burn-in period
  before RAPM becomes predictive. Direct ancestor of `methods.md`'s
  "prior-informed / Bayesian RAPM" family (xRAPM, EPM, sdv-py's
  `nba_adj_rapm.py`).
- **Omidiran, D. (2011)**, "A new look at adjusted plus/minus for basketball
  analysis" — introduced L1/Lasso regularized APM (see the rejection note
  above; not adopted anywhere in the corpus).
- **Deshpande, S.K. & Jensen, S.T. (2016)** — Bayesian model with win
  probability, not raw point spread, as the response variable, modeling
  impact via leverage/clutch performance. Code unavailable (see dead-artifacts
  above).
- **Franks, A.M. et al. (2016)**, "Meta-analytics" — three meta-metrics for
  evaluating *any* APM model: Discrimination (true skill vs. noise),
  Stability (rating evolution over time), Independence (redundancy across
  metrics). The Franks meta-metric *suite* itself is not implemented
  anywhere in the corpus (no hit for "Franks" or "meta-analytic" in either
  program document set) — an open opportunity, not a rejection. Note this
  is narrower than "Discrimination is unmeasured": the SDV program does
  separately measure discrimination, engine-side, as its own walk-forward
  metric — "DISCRIMINATION UNLOCKED" / "WALK-FORWARD NOW MEASURES
  DISCRIMINATION" (`roadmap.md` Addendum 26) — just not via Franks's
  formal meta-metric framework.

---

## 3. Open / blocked

### Post-merge wiring — re-targeted at the private engine, one item dissolved

`program-status.md`'s "Outstanding" table (written before the delivery
decision) lists producer `audit=` opt-ins, an `sdv-build-data` (now
`/sdv-data-pipeline`) toolkit step, an sdv-web ingest endpoint, and sdv-db
contract fields as follow-ups meant to
land once the donor branch merged into `sdv-py`. **That premise no longer
holds, but the items are not dead work.** Addendum 22 draws a line between
two different buckets: point (4) DISSOLVES the "post-merge call-site
migration off the `_common` shims" item outright — "the shims exist only on
the frozen branch; the engine's imports are already canonical" — and
likewise "sdv-py keeps X" becomes "sdv-py keeps nothing." Point (5) covers
the items actually named above (producer opt-ins, toolkit step, sdv-web
endpoint, sdv-db fields) and says the opposite of dissolved: these
integrations "consume the ENGINE privately," and scheduling the
engine-side gates that used to be sdv-py CI's job is explicitly "**the
reframed open item**" — re-targeted, not closed. (`roadmap.md` Addendum 22,
point 4 for the dissolved shim-migration item, point 5 for the re-targeted
producer/harness/sdv-web/sdv-db items; superseding `program-status.md`'s
"Outstanding" table framing, which predates the delivery decision.)

### Data-blocked

- **Sharp-line divergence signal** and the `backtest.reference_fn` market
  half — need ingested odds history not yet available.
- **Odds contracts** (cross-book reconcile, no-vig sanity check, staleness
  ceilings) — the prerequisite layer for the sharp-line signal above; still
  listed open in the latest program-status update.
- **Tennis / individual-sport vertical template** — shelved until a data
  source lands. Note this is NOT yet ported into `sdv-engine`: the surveyed
  external reference stack's `test/elo_class/elo.py` (surface-split,
  serve/return Elo) and `test/toy_sim/tennis_sim.py` (recursive
  `Overall`→`Match`→`Set`→`Game`→point sim) were flagged as a portable
  template, but the WS6 fold-in table lists this item without a commit hash
  — unlike its sibling rows — meaning it was identified, not built.
  (`survey-reports.md` "vertical-sport-pipeline (tennis)" section.)

(`program-status.md` "Outstanding" table + "Update — 2026-07-21"
addendum; `roadmap.md` WS5/WS6.)

### Feature/participation gaps

- **CFB participation feature base** — the reference source is
  involvement-grain only; it has no on-field player lists, so a true
  participation base (the football analogue of the possession-engine's
  lineup layer) cannot be built from it. (`roadmap.md` Addendum 35,
  "HONESTLY BLOCKED/REMAINING".)
- **Basketball jumpball tip node** — raw jumpball events carry no
  home-team identity; resolving it needs a join against the games table at
  fit time that was not wired as of the last addendum read. (`roadmap.md`
  Addendum 35.)
- **`load_nba_stats_pbp`** — needed to light up the NBA half of the
  possession-sim season glue (the schedule half already works: 1230/1230
  2025-26 games). Blocked specifically because publishing a new loader into
  `sdv-py` main means *pushing* to `sdv-py`, and the program's standing
  directive is "Everything LOCAL, nothing pushed." (`roadmap.md` Addendum
  27 "NOTHING PUSHED — both repos local-only by directive", Addendum 28's
  verbatim "Everything LOCAL, nothing pushed.", reaffirmed "push-barred" in
  Addendum 35a.)
- **Feature-drift-in-crons** (wiring `model_registry.feature_drift` into
  scheduled retrains) — still listed open as of the latest read; unlike the
  post-merge-wiring items above, this one is about the *engine's own* crons,
  not an sdv-py integration, so the 2026-07-22 delivery decision does not
  dissolve it. (`roadmap.md` Addendum 12 "post-merge", reclassified
  "(data/merge blocked)" by Addendum 20; `program-status.md` "Update —
  2026-07-21": "Items (6) odds and (7) feature-drift-in-crons remain open
  (data/merge blocked)" — the status note is later and is preferred here.)

### NBA Model Zoo v2 mimicry-gap proposal — status unresolved

`model-zoo-v2-gap-analysis.md` is headed **"STATUS: PROPOSAL — awaiting user
review (not an approved spec)"**, dated 2026-07-02. It proposes 15 additions
across three tiers (5 each, `model-zoo-v2-gap-analysis.md` §3 lines 86-116),
plus 3 more (items 16-18) in a later "daily axis" addendum — 18 total — to
close the gap between sdv-py's shipped NBA zoo and
LEBRON/DARKO/xRAPM/EPM: Tier 1 (oracle-in-hand thin slices — luck-adjusted
LA-RAPM, four-factor RAPM, multi-season time-decay RAPM, a concurrent-validity
Oracle ⑤, a shared WAR/e-wins layer), Tier 2 (fidelity upgrades — tracking-informed
prior, age/height prior features, a predictive-tuning loop, low-minute
padding, garbage-time down-weighting), and Tier 3 (new arcs — daily per-stat
DARKO, rookie/draft-slot priors, availability projection, role-conditioned
priors, shot-quality xPTS), plus a later "daily axis" addendum (through-date
ratings engine, walk-forward daily retrodiction Oracle ⑥, single-game BPM).
**None of the four other corpus documents — the roadmap, either survey
bundle, or the program-status snapshot — mention any of these 18 items
shipping.** The proposal's disposition is genuinely unresolved in the
corpus: don't assume it was approved, and don't assume it was rejected.
(`model-zoo-v2-gap-analysis.md` header, §3, §4.)

---

## 4. External reference implementations to clone

A curated "clone these first" list for a unified NBA + WNBA + college APM
stack, verified against the GitHub API (25/25 claimed repos confirmed to
exist — no hallucinated repos in this specific list).
(`apm-research/code-catalog.md` §3 "Top 10 Repositories to Clone First";
verification in the "Verification Addendum" section of the same file.)

1. `dblackrun/pbpstats` (Python) — NBA/WNBA pbp parsing; handles the
   out-of-order substitution edge cases; the gold-standard reference
   `methods.md` also names for possession parsing.
2. `nkal22/ncaa_hoops_pbp` (R) — originally attributed as hoop-explorer's
   backend. **That attribution is corrected later in the same source
   document** (see below) — this repo is still real and useful for NCAA pbp
   lineup parsing on its own, just not the hoop-explorer SPA's code.
3. `tonyelhabr/nba-rapm` (R) — cleanest `glmnet` Ridge-CV RAPM
   implementation; good reference for the stint-matrix pivot.
4. `dteuscher1/Adjusted-Plus-Minus` (R) — cross-references ESPN pbp with
   Basketball-Reference to fix WNBA substitution errors before running RAPM.
5. `sportsdataverse/wehoop` (R) — WNBA + women's NCAA ESPN data.
6. `sportsdataverse/hoopR` (R) — the NBA + men's NCAA equivalent of wehoop.
7. `nick3703/Code-For-A-Bayesian-Adjusted-Plus-Minus-Analysis-for-the-Esport-Dota2`
   (R/Stan) — esports domain, but the most mathematically complete public
   Bayesian Hierarchical APM via MCMC (Stan); the model transfers.
8. `jflancer/bigballR` (R) — NCAA lineup generation (`get_lineups`) for
   parsing complex NCAA substitution sequences.
9. `shufinskiy/nba-on-court` (Python) — lightweight, fast alternative to
   `pbpstats` focused solely on the 10-on-court-players problem.
10. `keithtyser/hoops-elo` (Python) — Elo/KenPom-style schedule adjustment,
    without which raw college APM is meaningless given disparate schedules.

**Correction on entry 2:** the report originally attributed hoop-explorer.com's
backend to `nkal22/ncaa_hoops_pbp`. A later section of the *same* source
document corrects this after a GitHub code-search for hoop-explorer.com
self-references: the actual hoop-explorer codebase is
`Alex-At-Home/cbb-on-off-analyzer` (TypeScript/HTML — the SPA itself,
including the on/off + luck-adjustment + RAPM leaderboard computation) plus
`Alex-At-Home/cbb-explorer` (Scala — the ingestion/parsing side) and
`Alex-At-Home/ncaawhoopR` (R — the NCAA women's variant, directly relevant to
a WBB pipeline). Low star counts on these three do not indicate low value —
this is the production code of the most complete public college RAPM system,
maintained through 2026. (`apm-research/code-catalog.md` "Correction: the
real hoop-explorer stack".)
