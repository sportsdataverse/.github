# Design freeze for observational sports studies

Sports papers are observational: no randomization, blinding or blocking is
available, and none of the DOE / CONSORT / allocation machinery in generic
experimental-design skills applies. What *does* transfer is the discipline of
deciding before looking, and recording every look.

**Which checks apply.** A *predictive* study (anything tuned, selected or fit,
then scored on held-out data) takes all of the checks below. A *descriptive*
study (no model selection, no holdout) skips 2–4. It still owes 1 for every
window it compares to a benchmark that an earlier run of yours already scored
(paper 11's window had been scored by a 09-27 refit), plus 5–9.

## Checks (each one a FAIL)

1. **Prior-access ledger.** Key each evaluation window by (league, seasons,
   outcome, benchmark) in one cross-repo ledger listing every scoring event
   (date, repo, script, result seen). FAIL if the paper's holdout has an
   earlier entry the prose doesn't disclose. FAIL on "scored once", "frozen
   before", "sealed" or "untouched" unless the ledger shows exactly one look.
   *Paper 05: an August CMSAC dev run had scored 2022–25; the paper said "scored once".*
2. **Freeze precedes score in git.** `DESIGN.md`'s commit is earlier than the
   first commit of the scored holdout artifact. FAIL if the holdout script
   and its result land in the same commit: then git can't prove the order.
3. **Guard covers choices, data and code.** The holdout guard key is (frozen
   choices, evaluation-data fingerprint = hash of ids + outcomes, scoring
   script hash), and **all three are compared**, not just recorded. FAIL if a
   hash is written and never checked.
4. **Look count printed.** Each holdout scoring increments a counter that the
   paper prints. FAIL if looks > 1 and the prose is silent, or if a re-look
   follows a seen result with no stated reason.
5. **Selection on availability.** When a comparison is restricted to units
   with a benchmark (lined games, tracked plays, scraped seasons), report
   coverage by season and by tune/holdout split, and compare included and
   excluded units on one observable.
6. **Era blocks.** Declare breaks (rule changes, 2020 COVID, 2021+ portal/NIL,
   schedule length). FAIL if a window spanning a break is reported only
   pooled.
7. **Claim types.** Tag each research question as descriptive, predictive,
   incremental-information or causal. FAIL on causal verbs ("drives",
   "comes from", "because of") attached to an unmeasured variable.
8. **Rivals table.** For each headline contrast (including tune→holdout
   drift), list at least winner's curse, era shift, benchmark composition,
   noise, each with one discriminating check that is run or explicitly
   deferred.
9. **Dropped analyses disclosed in the paper,** not only in STATUS.
10. **The freeze stays frozen.** After its freeze commit, `DESIGN.md` changes
    only by appends to the deviation log (`git diff <freeze>..HEAD -- DESIGN.md`).
    No results commit is an ancestor of the freeze. Re-run both checks at submission.
11. **Plans are never deleted alongside results.** A pre-results plan file
    (PLAN.md, a work plan, an early abstract) is never deleted in a commit that
    adds results. *Paper 05's only pre-results plan was deleted in the same commit
    that added every script and result, so git can't show the plan came first.*
12. **Inheritance from earlier looks.** List every hyperparameter, grid range or
    variant set carried over from a dev run or predecessor paper that saw the
    holdout. Narrowing the grid using an earlier holdout result counts as a look.
13. **Exploratory is labelled.** Everything not on the confirmatory list appears
    under an "Exploratory" heading in the body, and the abstract leads with
    confirmatory results.
14. **Cuts cite measured costs.** A design cut made for compute cost (a smaller
    grid, fewer seasons) cites a measured cost, not an estimate. *Paper 05 cut its
    grid on an "hours on CPU" guess; the measured cost was 5–35 s per configuration.*

Mechanical audit: science-superpowers' `prereg.sh audit` is a usable checker
for 10–11. **Don't use its `freeze` mode**, which makes commits on its own.

## `DESIGN.md` template

```markdown
# Design freeze: <paper slug>  (commit BEFORE the first holdout read; amend only by dated deviation)

## Prior access (mandatory, honest)
- Windows already scored anywhere (repo, date, result seen):
- Summaries/plots of the evaluation window already viewed:
- Looks so far on the holdout: N

## Questions and claim types
| RQ | Claim type (descr./predictive/incremental/causal) | Estimand or metric | Unit |

## Hypotheses with falsifiers
| H | Prediction | Falsified if | Indeterminate if | SESOI δ |

## Data and selection
- Sources + commit/hash; leagues; seasons; unit of analysis
- Inclusion filter and expected coverage by season
- Era blocks:
- Known availability biases (who lacks the benchmark, and why)

## Windows
- Tune: …   Holdout: …   (disjoint; fingerprint = sha256 of ids + outcomes)
- Guard key = frozen choices + data fingerprint + script hash (all compared)

## Selection rule (decided now)
- Search space (k configs, grid values incl. edges), selection metric, tie-break
- Frozen for holdout scoring:

## Baselines and controls
- Floor (naive rule), ceiling (market / oracle), negative control

## Analysis
- Primary metric; secondary metrics
- Cluster unit (justify vs shared model state) + coarser-unit sensitivity
- Multiplicity families with sizes; correction or "exploratory" label
- Confirmatory list (only these may appear as findings in the abstract)

## Planned rival checks
| Headline contrast | Rival | Discriminating check |

## Deviation log (append-only)
| date | section | change | reason | result known? | impact |
```

A retroactive `DESIGN.md` is allowed, and better than none, but it carries a
`Written after results were seen` banner, and the paper may not use the
single-look vocabulary.
