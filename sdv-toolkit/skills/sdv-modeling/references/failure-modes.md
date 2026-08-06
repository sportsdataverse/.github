# Failure modes — why is my model silently wrong?

This ecosystem has already named the bug class this file catalogs, in its own
words, in a module built to gate against it: **"components reporting success
while doing nothing."** `checks.py`'s docstring states the shape directly —
"Nothing failed. The build ran green, the columns were present, the values
were plausible, every downstream consumer got numbers. The dataset shipped
and sat live for two days. It was found only because someone measured the
output" — and names three instances of the same shape in one sentence: "the
ridge no-op itself, a `fill_null(0.0)` that is a no-op on Boolean columns, and
a verify pass that only checked the rows it had targeted" (`checks.py:64-69`).

**A description is not an entry here.** Every row below states the failure,
how it presented (in every confirmed instance: silently, with a green run),
the assertion that would have caught it, and where it actually happened —
a note file for the narrative, a git commit for the fix and the real
assertion. Distilled from `higher-order-models.md`, `ratings-phase2-openq.md`,
`t5-xg-findings.md`, and `possession-reconciliation.md` (the four sources
this task was scoped to), the shipped `reviewer.md` §4 table (authoritative —
this file expands it, never contradicts it), and the git history of the two
repos where the confirmed instances actually live, `cfbfastR-cfb-data` and
`sdv-py`, found by grepping commit messages for the terms the notes used.
Metric selection and the leakage/oracle-join mechanics live in
`metrics-and-gates.md`; this file cross-references rather than re-deriving
where the two overlap.

Shorthand used in citations:

| Shorthand | Full path (under `GitHub-Data/sdv-dev/`) |
|---|---|
| `reviewer.md` | `sportsdataverse-org/sdv-toolkit/agents/sdv-model-reviewer.md` |
| `higher-order-models.md` | `ClaudeCowork/notes/2026-08-03-cfb-higher-order-models.md` |
| `higher-models-HANDOFF.md` | `ClaudeCowork/notes/2026-08-03-cfb-higher-models-HANDOFF.md` |
| `bayesian-evaluation.md` | `ClaudeCowork/notes/2026-08-03-cfb-bayesian-evaluation.md` |
| `ratings-phase2-openq.md` | `ClaudeCowork/notes/2026-07-16-cfb-ratings-phase2-openq-findings.md` |
| `t5-xg-findings.md` | `sdv-py/dev/t5_xg_reevaluation/2026-07-12-findings.md` |
| `possession-reconciliation.md` | `sdv-py/dev/bigballr_port/possession_engine_reconciliation.md` |
| `checks.py` | `cfbfastR-dev/cfbfastR-cfb-data/python/cfb_data_build/checks.py` |
| `cfb-data@<sha>` | a commit in `cfbfastR-dev/cfbfastR-cfb-data` (`git show -s <sha>`) |
| `sdv-py@<sha>` | a commit in `sdv-py` (`git show -s <sha>`) |

---

## 1. The catalog

Every row in `reviewer.md` §4's shipped table (rows 1–7) appears below with a
compatible assertion, plus seven more confirmed in the wider corpus (rows
8–14) and four bonus instances (rows 15–18) found while grounding the
required fourteen. "Confirmed" means a real commit fixes it — where I could
not find one, §7 says so instead of inventing a citation.

| # | Failure | Assertion |
|---|---|---|
| 1 | ridge fit with λ applied to nothing | `corr(adjusted, raw) < 0.95` — genuine adjustment measured 0.57–0.72, the no-op 0.99 |
| 2 | Boolean `fill_null` no-op | null count strictly decreased; rate is not pinned at exactly 1.0 |
| 3 | release tag on the wrong commit | tag SHA == build SHA |
| 4 | λ no-op republish (stale artifact) | `updatedAt` on the published asset moved past the fix commit's timestamp |
| 5 | `through_week` treated as INCLUSIVE | the boundary week/game is absent from the training frame (see `metrics-and-gates.md` §3) |
| 6 | schedule/season-scoped reprocess skipping units | processed count == expected unit count, per unit, not just a nonzero total |
| 7 | build with no retry, partial write | row/asset count matches the manifest; upload failure raises instead of logging |
| 8 | ESPN `-1` sentinel read as a real value | sentinel filtered before aggregation, on the *derived* column, not just the guard column |
| 9 | percentile "shares" that were never rates | `pass_x + rush_x ≈ overall_x`, not `pass_x + rush_x == overall_x` (sums, not sits near) |
| 10 | special-teams contribution 18× overstated | component magnitude checked standalone AND jointly (`incremental_value()`) |
| 11 | simulator iterating non-FBS teams | simulated population count == the rated population, not the schedule population |
| 12 | `group_by` without `maintain_order` discarding a prior sort | order preserved, or re-sorted after re-aggregation, and asserted |
| 13 | NaN ≠ null in polars | both checked (`is_nan() \| is_null()`), not just `is_not_null()` |
| 14 | mixed-source ID dtypes at a join | `left.schema[k] == right.schema[k]` asserted pre-join (see `metrics-and-gates.md` §4) |
| 15 | a feature silently absent from its own A/B arm | the two arms' input columns differ, not just their metrics |
| 16 | `fill_null(0.0)` that doesn't no-op — it lies | null-coordinate rows routed out, not defaulted into a real-looking value |
| 17 | a derived count that depends on which side you computed it from | the same entity re-derived from the other side matches exactly |
| 18 | a cross-run leak kept on purpose to match a broken oracle | per-unit isolation re-verified before publish, independent of why the leak was tolerated in dev |

---

## 2. Ridge fit with λ applied to nothing (#1) + λ no-op republish (#4)

**These are two faces of one incident**, not two independent bugs — worth
stating honestly rather than manufacturing a second story. `cfb_adjusted_epa`'s
ridge penalty defaulted to the glmnet-scale `325`; under sklearn's
`alpha = lambda * n` convention that crushes every team coefficient to ~0, so
`adj_off_epa` correlated **0.9928** with its own raw, unadjusted
`EPAplay_off` (`adj_def_epa` 0.9921) — "the 'adjusted' columns were the
unadjusted ones" (`higher-order-models.md` §4c). **Nothing failed**: the build
ran green, all 384 columns were present and plausible, and it shipped live
for two days before anyone measured the output (`cfb-data@8cbaa4d`).

**Face 1 — the fit itself.** The fix, `checks.assert_adjustment_is_real()`,
asserts on the *output*, not the config, because "any future cause trips it —
a wrong lambda, a caller override, a solver change" (`checks.py:1-70`,
`cfb-data@8cbaa4d`):

```python
NOOP_CORR_THRESHOLD = 0.95   # genuine adjustment: 0.57-0.72; no-op: 0.99
def assert_adjustment_is_real(df, *, threshold=NOOP_CORR_THRESHOLD, ...): ...
```

Validated in both directions on real data: fires on the live bad set
(0.9928), passes on the rebuilt summaries (0.7197/0.6556), and the spread
correctly widens (sd 0.127 → 0.168) once schedule strength is genuinely
credited (`cfb-data@8cbaa4d`).

**Face 2 — the republish never happened.** The 08-02/08-03 republish cascade
that fixed the lambda in code covered pbp, `adv_*`, and season datasets, but
**missed both weekly datasets** — `cfb_ratings_weekly` and
`cfb_team_summaries_weekly` kept serving bytes built under the old default
(`higher-order-models.md` §4c). The author's own postmortem is the sharpest
statement of the general trap: "I found the dead `_RIDGE_LAMBDA = 325.0`...
concluded the live lambda was 0.035. True of the CODE, irrelevant to the
ARTIFACT... **A stale artifact is not a code question**"
(`higher-order-models.md` §4c). The verify command names the real assertion —
check the published asset's timestamp, not the source file:

```sh
gh release view cfb_team_summaries_weekly --repo sportsdataverse/sportsdataverse-data \
  --json assets -q '[.assets[].updatedAt]|sort|last'
```
(`higher-models-HANDOFF.md`)

`reviewer.md` §4 states rows 1 and 4 as ridge-coefficient and
artifact-hash checks respectively — both are satisfied by this one incident's
two fixes, and both must be checked, not just one: a `checks.py`-style output
gate catches a bad fit; a timestamp check catches a good fit that never
shipped.

---

## 3. Boolean `fill_null` no-op (#2)

polars leaves Boolean nulls **untouched** when the fill value is a float — no
error, no warning. Every aggregation frame in the CFB advanced-stats builder
used `.fill_null(0.0)`, so boolean flags kept their nulls, and `.mean()` on a
flag that is null-where-absent silently averages over only the `True` rows —
returning `1.0`. `rushing_power_rate` **shipped as exactly 1.0 for every team
in every season**; the real 2024 figure is `3437/63017 = 0.055`
(`sdv-py@3cf7332f`).

```python
# before: booleans kept their nulls under a float fill -> mean() over True-only rows -> 1.0
power_rush_attempt.fill_null(0.0)

# after: _fill_missing() -- booleans -> False, numerics -> 0.0 -- across all 10 fill sites
```

The commit audited the *whole class* rather than patching the one column: of
44 boolean `.mean()` aggregations in the module, exactly one had nulls in its
source and was wrong; a look-alike (`rushing_power_success_rate` at 0.774)
was checked and is correct, because its frame is pre-filtered to power
attempts only (`sdv-py@3cf7332f`). **The assertion this licenses is narrower
than "check nulls decreased":** a rate pinned at exactly 1.0 (or exactly 0.0)
on a boolean-derived mean is the tell, independent of whether the null count
moved — check both.

---

## 4. Release tag on the wrong commit (#3)

`reviewer.md` §4 states the assertion (`tag SHA == build SHA`) as one of the
seven confirmed instances but is itself the only citable source for this row
in the material read for this task — an honest attribution, not padding: no
second independent occurrence surfaced in `higher-order-models.md`,
`ratings-phase2-openq.md`, `t5-xg-findings.md`, or
`possession-reconciliation.md`.

---

## 5. `through_week` treated as INCLUSIVE (#5)

Fully covered in `metrics-and-gates.md` §3 — the `through_week == W` /
`through_week + 1` offset mechanics, the docstring quote ("Testing a proxy
for the thing is how leakage survives a green suite"), and the file:line
citation live there; this entry exists only so the row is visibly present in
both catalogs, per the compatibility requirement. Do not re-derive it here.

---

## 6. Schedule/season-scoped reprocess silently skipping units (#6)

`reviewer.md` §4 names the shape; the confirmed near-instance is the CFB
downstream fan-out driver's own stated failure mode: "The first P2 pbp
publish died on a single `gh` timeout and abandoned 20 seasons... **that must
not repeat** across a 220-unit adv sweep" (`cfb-data@1c45699`). The fix
isolates every dataset-season so one failure is recorded rather than silently
dropping the remaining units:

```
adv 2018       all 10 datasets, 0 failures (adv_team 1,776 rows = 888x2)
summaries 2008 percentiles 99, team_summaries 120 (correct FBS count), ...
```
(`cfb-data@1c45699`)

The assertion the smoke-test output demonstrates is exactly `reviewer.md`'s
shape, made concrete: report the **per-unit processed count against a known
expected count** (here, the correct FBS team count and per-table row counts),
not a single aggregate "N succeeded" that a silently-abandoned sweep can still
satisfy for the units it did reach.

---

## 7. Build with no retry, partial write (#7)

`pb_upload_both` caught every upload error, logged it, and returned exit `0`
— "a publish cron reports success while dropping data." Not hypothetical:
the 2026-07-16 team_summaries re-backfill exited `0` with two parquet files
silently un-uploaded — one release never became visible, one got an HTML
error page instead of a file (`cfb-data@217ecc5`). Both failures were
transient (an eventual-consistency race; a rate-limited API returning an
error page), so the fix is retry-then-raise, not retry-forever:

```
- retry the upload (3 attempts, 5s apart)
- on exhaustion, stop() rather than log-and-continue
- .ensure_release_visible returning FALSE now raises too
```
(`cfb-data@217ecc5`)

"A hard stop mid-run is deliberate: a partial publish that reports success is
strictly worse than a loud failure a re-run fixes" (`cfb-data@217ecc5`) — the
assertion isn't a number, it's the control-flow shape: **exhaustion must
raise**, and the calling driver's exit code must reflect it.

---

## 8. ESPN's `-1` sentinel read as a real value (#8)

ESPN uses `-1` to mean "no end-state yards-to-endzone," but the existing
guard only checked that `end.yardLine is not null` — and ESPN populates
`end.yardLine` perfectly well on exactly the plays carrying the sentinel, so
the guard passed and the fallback never fired for the case it exists to
handle (`sdv-py@fd134181`). 2016 week 2 shipped with `end.yardsToEndzone ==
-1` on all 238 plays of one game; downstream, `EP_end` scored as if the
offense were on its own 1-yard line after every snap, and mean EPA ran
**~-2.6/play** where a healthy game sits near 0 — reaching the published
percentiles as a 1st-percentile early-down EPA of -2.97, "roughly six times
every neighbouring season," invisible because the median and upper tail were
untouched (`sdv-py@fd134181`).

```
corrupt  400868877  mean EPA -2.292 -> -0.158   212/234 plays changed
controls 4 games in 2019 and 4 in 2023: 0 plays changed, max|dEPA| 0.0000
```

**The assertion isn't "check the guard column" — it's "check the derived
column."** The guard (`end.yardLine is not null`) was satisfied; the bug was
in the column it was meant to gate (`end.yardsToEndzone`). Filter the
sentinel on the value actually consumed downstream, and a companion check
(`warn_implausible_epa_games`, per-game `|mean EPA| > 0.5`) catches the class
even when the specific sentinel value isn't known in advance
(`cfb-data@ce5d2cc`).

---

## 9. Percentile "shares" that were never rates (#9)

`prepare_percentiles` computed `pass_success` as `mean(epa_success * pass)`
over **every** play — that product is 1 only on a successful pass and 0 on
every other play including every rush, so the mean is `(# successful
passes) / (# ALL plays)`, the *share of all plays* that were successful
passes, not the pass success *rate* (`cfb-data@ce5d2cc`). The tell was
arithmetic, not a domain judgment: the published pass/rush halves **summed**
to the overall metric instead of each sitting near it —

```
success  0.4426   pass_success 0.2153 + rush_success 0.2190 = 0.4343
```

— and a real pass success rate is ~0.44, not ~0.22 (`cfb-data@ce5d2cc`). Fix:
filter before averaging, not multiply-then-average:

```python
# before (shares, not rates): 1 only on made pass, silently 0 on every rush
pass_success=(pl.col("epa_success") * pl.col("pass")).mean()
# after (rates): null on games with no attempts, which the quantile step correctly skips
pass_success=pl.col("epa_success").filter(pl.col("pass") == 1).mean()
```

**Assertion:** `pass_x + rush_x` should sit *near* `overall_x`, not sum to
it exactly — an exact sum across a partition is the signature of a
share-of-all-rows computation masquerading as a within-partition rate.

---

## 10. Special-teams contribution 18× overstated (#10)

The CFB higher-order pregame model's special-teams composite mixed field
goals, punting, and returns into one number "that was ~18x overstated in
apparent size (`points_scale`)" — and collapsing three unrelated skills into
one coefficient also buried the one genuinely useful signal (starting field
position, a persistent team trait) under two noisy ones (FG outcomes are
near-noise year to year) (`cfb-data@1524bc7`). Pricing them separately:

```
component                pts_alone  pts_joint  spread_joint   corr
start_position_margin        0.419      0.279          2.25  0.165
on top of off/def/st ratings:  MAE 14.385 -> 14.289  (+0.096)
```

**The assertion is `incremental_value()` itself** — the module exists
specifically "to force that distinction: a field-position metric always
looks respectable standalone, and the only question worth asking is what it
adds once offence and defence are already in the model" (`cfb-data@1524bc7`).
A component magnitude checked only in isolation (`pts_alone`) cannot catch
an overstatement that only appears once it's priced jointly with what it's
correlated with.

---

## 11. Simulator iterating non-FBS teams (#11)

`cfb_season_odds` builds its team population from the **schedule** (every
opponent an FBS team played — 704 teams in 2023), not from `cfb_ratings`
(133 rated teams). `make_ratings_compute_results` documents "teams absent
from it are treated as league-average (0.0)" — so 571 FCS/D2/D3/NAIA
programs were simulated as **median FBS teams** (`cfb-data@52e2752`).
Measured on a real 2023 run: ~24% of championship probability went to
schools that cannot enter the playoff —

```
Michigan             0.569   <- actual champion, correct
South Dakota State    0.045
Ave Maria              0.025
```

— "incoherent on its face, and it never raised anything. The engine itself
is fine; the population fed to it was wrong" (`cfb-data@52e2752`). The fix
names the general principle, not just this instance: "'Missing → league
average' is a sound default for a team with sparse data and a catastrophic
one for a team that does not belong in the population. At the point of the
lookup the two are indistinguishable — both are a failed join — so the
default has to be chosen by WHY the row is absent, not by what is convenient
when it is" (`cfb-data@52e2752`). `simulate_season(..., fbs_only=True)`
restricts to teams carrying a real rating, renormalizes the probability
columns over the remaining field, and **raises if the filter empties the
frame** (a namespace disagreement, not a working filter) — the assertion is
`simulated_population == rated_population`, and the guard against an
over-eager filter is that it must never silently zero the frame either.

---

## 12. `group_by` without `maintain_order` discarding a prior sort (#12)

No confirmed production instance of this specific shape surfaced in
`higher-order-models.md`, `ratings-phase2-openq.md`, `t5-xg-findings.md`,
`possession-reconciliation.md`, or a targeted git-log search of `sdv-py` and
`cfbfastR-cfb-data` for commits mentioning `maintain_order` or a discarded
sort. `reviewer.md` §4 names it as one of the seven confirmed rows, so it is
carried here for compatibility, but this file has no second, independent
citation to offer beyond the agent table itself — an honest gap, not a
fabricated one. The assertion the row states is still actionable without a
named incident: after any `group_by` whose input was sorted for a reason
(e.g. `sort("game_seconds")` before segmenting possessions, the exact shape
`possession-reconciliation.md` §1c's chain state machine depends on), assert
the output order matches the expected order, or pass `maintain_order=True`
and assert that flag is actually set at the call site.

---

## 13. NaN ≠ null in polars (#13)

A degenerate early-season week made the CFB/MBB ratings fixed point emit a
`NaN adj_em` → `NaN margin` → `NaN pregame_home_prob`. **NaN is not null in
polars**, so the guarding `is_not_null()` filter let it straight through, and
**44,000 plays in WBB 2015 got a NaN `pregame_home_prob`** in a published
release asset (`sdv-py@6c861aa4`):

```python
# NaN is not null in polars -- is_not_null() alone lets it through
# fix: drop non-finite in _pregame_probs, guard the per-game anchor in _compile_season_wp
```

The same commit fixed a sibling instance in the same build: some historical
seasons (e.g. WBB 2005) publish pbp but no boxscores, so the team-box frame
is empty and column-less, and a downstream `.filter(game_date < cutoff)`
raised `ColumnNotFoundError`, aborting the *whole season's* build rather than
falling back per-game (`sdv-py@6c861aa4`). **Assertion:** any null-guard on a
float computed from a fitted quantity must check `is_nan() | is_null()`
together, not `is_not_null()` alone — and the guard must be validated against
a real degenerate window (an early season, a boxscore-less season), not just
a normal one.

---

## 14. Mixed-source ID dtypes at a join (#14)

Fully covered in `metrics-and-gates.md` §4 (the `left.schema[k] ==
right.schema[k]` assertion pattern, the CFB `cfb_ratings.py`/
`cfb_recruiting_projection.py`/`cfb_returning_production.py` real assert
sites, and the NHL `Int64` vs basketball/football `Utf8` fixture-dtype
divergence) — cross-referenced rather than re-derived. One instance from this
task's own corpus that is not yet in that catalog: **PWHL `game_id` is
`Utf8`** while **NHL `game_id`/ids are `Int64`** — "fine within a league; a
hazard for any cross-league parity join — pin + assert at the boundary"
(`t5-xg-findings.md` §W9). No cross-league PWHL/NHL join exists yet in the
corpus read for this task, so this is a documented hazard to assert against
before one is built, not yet a confirmed incident.

---

## 15. Bonus: a feature silently absent from its own A/B test

Not one of the fourteen required rows, but the same shape and worth carrying
— it happened to the CFB higher-order-models author **one hour after**
shipping the `checks.py` gate against exactly this class: `add_rest` looked
for a kickoff date, found none (the fixed column select had dropped it), and
did `return games` unchanged. The A/B reported:

```
base          MAE 13.026  Brier 0.1879
base + rest   MAE 13.026  Brier 0.1879        # byte-identical
```

"The honest reading is 'rest was never tested'; the available one is 'rest
doesn't help.' It survived only because the script printed the column list
next to the metric" (`higher-order-models.md` §4e). A second version of the
same trap followed immediately: `diff_features` already pairs
`rest_home`/`rest_away` into `rest_diff`, so "base + rest" would again have
been identical unless the *baseline* removed the rest block rather than the
treatment arm adding it. The fix generalizes past this one feature:
`add_rest` now **raises** when there's no date column instead of returning
the frame unchanged, the date is derived before the column-dropping select,
and `build_game_frame` raises if `enrich=True` yields zero rest columns —
belt-and-braces on the same wiring (`cfb-data@dea732e`). **The general rule,
stated verbatim because it generalizes past this file entirely: "identical
numbers across two arms is not a weak effect, it is usually a disconnected
wire. Print what varied, not just what resulted"** (`higher-order-models.md`
§4e). Assertion: **the two arms' input columns must differ before their
metrics are compared** — diff the schemas, not just the scores.

---

## 16. Bonus: `fill_null(0.0)` that doesn't no-op — it actively lies

The inverse failure to #2 and #16's row above: `PwhlCoordXGModel.predict`
does `shot_distance.fill_null(0.0)`, so a shot with a **null coordinate**
(missing/unparsed geometry) becomes distance `0.0` — point-blank — and scores
`xG ≫ 0.5`, the opposite of "unknown." The ratings pipeline masks this with a
separate `fallback_rate`, but calling `predict()` directly is a footgun the
test file documents but does not close (`t5-xg-findings.md` §W9,
`test_pwhl_xg_proxy_oracle.py:216-219`). Assertion: null-geometry rows must
be **routed out** of the prediction (excluded, or scored by the fallback
rate explicitly), never defaulted into a coordinate that looks like real
data — a `fill_null(0.0)` in a geometry column is a correctness bug even when
it doesn't raise and doesn't produce an obviously-impossible number.

---

## 17. Bonus: a derived count that depends on which side you computed it from

hoop-explorer's NCAA possession engine is team-relative — the same team run
through as the "home" side vs the "away" side should report an identical
possession count. It does not:

```
wbb 5728709        run as Notre Dame   run as Texas
Texas possessions          82                 83
```

Root cause: the engine's `lineup_balancer` greedy round-robin split and
`lineup_fixer`'s clamps (`pts > 0 and poss <= 0 → 1`) operate on *that team's*
stint boundaries, which differ depending on which side's box score seeded the
parse — and the clamp is not conservative, it mints possessions
(`possession-reconciliation.md` BUG-1). "A published dataset built this way
is not well-defined: `Texas @ possessions` has two values depending on the
row you build it from" (`possession-reconciliation.md` §4). This is not
quite a fitted-component no-op — the component runs, produces a plausible
number, and never raises — but it fails the same test an assertion for
"ran without error" cannot catch. Assertion: **re-derive the same entity from
the other side and require exact agreement** before publishing any
team-relative count.

---

## 18. Bonus: a cross-run leak kept on purpose to match a broken oracle

The bigballR possession segmenter runs `pl.col("event_type").shift(1)`
**ungrouped, deliberately**, because "oracle parity depends on the leak" —
its own docstring says do NOT add `.over("game_id")` (`possession-reconciliation.md`
BUG-4). Demonstrated: `game 6479639` parsed alone gets
`start_event_type = None`; parsed in a 2-game frame, its first possession
inherits `game 6470186`'s **last** event. "Parity is a fine reason for a
test; it is **not** a fine reason for a published dataset"
(`possession-reconciliation.md` BUG-4) — every game's opening possession in a
multi-game publish run silently carries state from whichever game happened
to precede it in that batch. Assertion: **publish per-game, or add
`.over("game_id")` behind an explicit flag** — a leak tolerated for oracle
parity in a dev/test harness must never reach a multi-unit publish path
unguarded, and the guard must be re-verified at publish time independent of
why the leak existed in dev.

---

## 19. Design lesson (not a bug): the substrate is roughly one dimension

Not a failure — the finding that closes out the CFB higher-order-models
program, worth carrying here because it's the one place "add more features"
was tested directly and measured to be the wrong lever. Walk-forward on the
corrected (post-λ-fix) spine, 2014–2025, n=5,089 (`cfb-data@6bd24e4`):

```
set                          n     MAE    Brier  cal_err
all                        244  13.027   0.1875    0.052
minus efficiency           167  12.962   0.1864    0.045
core + prior + finishing    60  12.966   0.1870    0.043
core: other + rating        35  13.135   0.1889    0.053
other only                  18  13.217   0.1910    0.068
```

**60 features match 167 within 0.004 MAE and beat the full 244 on every
metric including calibration.** "Dropping 77 efficiency columns IMPROVES the
model: they re-measure a dimension already present, so their only marginal
contribution is variance" (`cfb-data@6bd24e4`). The full out-of-sample arc,
against the closing-line market ceiling:

```
shipped cfb_game_predict   15.14
closed-form refit          13.95
GBM, 244 features          13.03
GBM, 60 features           12.97
market                     12.27
```

This is the same conclusion a separate, independent evaluation reached from a
different angle the same week: "the 384-column substrate is ~one dimension
measured 200 ways, no family is necessary, and dropping 77 efficiency
features changes nothing detectable" (`bayesian-evaluation.md` §6); an
earlier ablation on the same program had already shown `rating` alone
(7 features) scoring 13.62 against 13.26 for all 211 —
close, not free, but the same direction (`higher-models-HANDOFF.md`). **The
lever in this substrate is not feature count** — it is fixing what a feature
actually measures (the ridge no-op in §2 above turned the entire `rating`
family raw for weeks without moving anyone's headline MAE, because the
redundant `adj_*` efficiency columns were carrying the same signal anyway;
`cfb-data@6bd24e4`'s own postmortem: "the pregame model was insulated by the
same redundancy that makes 184 of its features droppable"). Only one feature
family — `rt_*`, the `cfb_ratings` block carrying special teams, FEI, and
`adj_net` — was confirmed non-redundant three independent ways (family
ablation, leave-one-block-out, this prune); removing it cost 0.14 MAE while
every other removal cost ≤0.05 (`higher-models-HANDOFF.md`).

---

## 20. Honest gaps

- **`group_by` without `maintain_order` (#12)** has no independent
  confirmed-instance citation in this file — see §12. Carried for
  `reviewer.md` compatibility, not padded with an invented incident.
- **Release tag on the wrong commit (#3)** likewise has no second source
  beyond `reviewer.md` itself in the material read for this task — see §4.
- **Mixed-source PWHL/NHL `game_id` dtype (#14 addendum, §14)** is a
  documented hazard, not yet a confirmed incident — no cross-league join
  exists in the corpus read for this task that has actually tripped over it.
- **"60 features beat 244" (§19) is the real, verified number** — worth
  stating explicitly because an earlier draft of the program plan this task
  was scoped from had already misattributed a source once; the number above
  was re-derived from `cfb-data@6bd24e4`'s own commit body, not copied from
  a downstream summary of it.
