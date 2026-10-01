---
name: sdv-research-paper
description: Runs a SportsDataverse research paper (SSAC, CMSAC, JQAS, an arXiv preprint, a model write-up) from question to submission as a gated scientific process, so every claim in the abstract survives a hostile reviewer with the paper's own data. Phases - design-freeze (DESIGN.md committed before the first holdout read, a cross-repo prior-access ledger, the holdout guard covering choices + data fingerprint + script hash), analysis (numbered stages, numbers.json, no hand-typed numbers, abstract included), claims-audit (every sentence of the abstract and conclusion mapped to a key, every comparative and universal word backed by a computed value, conclusion never contradicts the largest result), inference (intervals at the shared-state cluster unit and every printed t/p/SE on that same unit, nulls only with a smallest effect of interest or the holdout's power, calibration tested against simulated perfect calibration, multiplicity families declared, grid-edge and selection-optimism reported), benchmark (the benchmark's composition is constant across compared windows or the change is reported; "closing" lines are evidenced per league; aggregators are excluded from book medians; spread/moneyline orientation and sum gates; fixed conversions state their bias; market-informed inputs are never credited to the open model; market-specific rivals; coverage-thinning sensitivity; advice comes with an evaluated decision), reproducibility (inputs pinned not merely hashed, recorded provenance is what was actually fetched, hashes are checked on rerun, a clean-clone `uv sync --frozen` rerun reproduces every key, the holdout has a verify mode, Monte Carlo error sits below printed precision, known-effect simulations, the repository is public when the venue requires it), figures (vector, no overprint, 7pt floor, color never the only cue, the figure shows the claim it is cited for), citations (bib keys equal cited keys, DOI matched to Crossref on title/author/year, every attributed finding quoted from where it was read, "a simplification of" when the code departs from the cited model), venue (the official rules recorded with URL and date before submission), and review (dispatch sdv-paper-reviewer per lens, five-field comments, fix or disclose). Built from applying 22 installed research-writing skills (Orchestra ml-paper-writing family, K-Dense scientific family) to SSAC27 paper 05, which surfaced four false abstract sentences that `ssac check` passed; references/external-skills.md records which of those skills to reach for and which to avoid. Pairs with sdv-modeling (what is statistically correct) and sdv-model-build (building the model the paper reports). Invoke for "write a paper", "research paper", "SSAC", "Sloan paper", "CMSAC", "abstract", "manuscript", "preprint", "paper rigor", "pre-register", "pre-registration", "design freeze", "holdout discipline", "is this claim supported", "review my paper", "review my abstract", "reviewer 2", "claims audit", "check the citations", "related work", "is this figure publication quality", "camera-ready", or before submitting any write-up whose numbers come from SDV data.
---

# Research papers as a gated scientific process

A paper is a set of claims, each owed evidence. This skill makes the
evidence checkable **before** a reviewer checks it. It is a workflow; the
statistics it gates on live in `sdv-modeling` (`metrics-and-gates.md`,
`resampling.md`, `betting-markets.md`), and the model the paper reports is
built with `sdv-model-build`.

**Why it exists.** Applied to SSAC27 paper 05, six review lenses found four
abstract sentences contradicted by the paper's own record: "scored once"
on a holdout an August dev run had already scored, a `t = 2.49` from
unclustered SEs beside season-clustered intervals (clustered t = 1.87), "did
not move" for techniques of which one closed 18%, and "untested" for the
information that produced the largest single gain. All passed the repo's
no-hand-typed-numbers check, because none of them was a wrong *numeral*.
Number provenance is necessary, not sufficient: the defects live in words.

## Phases

Enter at any phase; each ends in a gate. A FAIL is fixed or disclosed in the
paper, never only in STATUS.

| # | Phase | Gate (fail condition) | Reference |
|---|---|---|---|
| 1 | Design freeze | `DESIGN.md` missing, or its commit is not earlier than the first holdout score; prior-access section blank | `references/design-freeze.md` |
| 2 | Analysis | a printed number with no pipeline key; the abstract outside the numbers check | `references/claims.md` §1 |
| 3 | Claims audit | an abstract/conclusion sentence with no key; an unbacked comparative; conclusion contradicts a result | `references/claims.md` |
| 4 | Inference | t/p/SE on a different cluster unit than the intervals; a null without SESOI/MDE; untested "well calibrated" | `references/inference.md` |
| 5 | Figures | raster embed when vector exists; overprinted labels; claim not visible in the cited figure | `references/figures.md` |
| 6 | Citations | unverified DOI; attributed finding with no quoted passage; missing prior test of the same comparison | `references/citations.md` |
| 7 | Benchmark | benchmark composition changes across compared windows unreported; "closing" unevidenced; market-informed inputs credited to the open model | `references/benchmark.md` |
| 8 | Reproducibility | inputs hashed but not pinned; no clean-clone rerun; holdout cannot be verified by a third party; Monte Carlo error above printed digits | `references/reproducibility.md` |
| 9 | Venue | the venue's official rules not recorded (URL + date) in the repo; a hard rule broken (it blocks submission) | `references/venue.md` |
| 10 | Review | `sdv-paper-reviewer` not run per lens on the submitted text, or a FAIL left undispositioned | below |

### Phase 1 — design freeze (do this first, or say honestly that you didn't)

Copy the `DESIGN.md` template from `references/design-freeze.md`, fill
**Prior access** truthfully (which windows were already scored, anywhere,
by any repo, and what was seen), declare windows, selection rule, baselines,
SESOI per hypothesis, cluster unit, multiplicity families and the
confirmatory list, and commit it before any holdout read. A paper started
without one writes `DESIGN.md` retroactively with a `Written after results`
banner and may not use "frozen", "sealed", "scored once" or "untouched".

### Phases 2–9 — while writing

Work through each reference's checklist on the section you are writing.
The words that most often fail, in order of how often they did on paper 05:
**once / frozen / untested / no effect / did not / stable / well calibrated
/ more than / converge / adds nothing**. Each needs a key, an interval or a
ledger entry behind it.

### Phase 10 — review

Dispatch `sdv-paper-reviewer` once per lens (`design`, `claims`,
`inference`, `benchmark`, `reproducibility`, `figures`, `citations`,
`venue`), or `lens: all` on an abstract. Lenses are independent; run them in
parallel. In a blind benchmark no single reviewer found more than about a quarter
of a paper's known defects, while independent lenses together found most of them,
and three found the same new defect. Treat agreement between independent lenses as
confirmation, and never stop at one pass. The reviewer is
read-only and returns five-field comments (location · observation ·
evidence · why it matters · requested action). For each FAIL: fix, or add a
sentence of disclosure **in the paper**. Abstract and title changes need
the author's sign-off; propose wording, never apply it unasked.

Write review output to the paper's `STATUS.md` (or a ledger in
ClaudeCowork), not into the reply.

## Hard rules

- The abstract is checked like the body. Every number in it resolves to a
  pipeline key; every sentence in it maps to a result.
- A claim about a holdout is a claim about **every** program that ever
  scored those seasons, dev runs and predecessor papers included.
- An interval covering zero is reported as "covers zero", with the SESOI
  or minimum detectable effect beside it, never as "nothing".
- No draft text, figure or data leaves the machine for an image/LLM
  service, and no tool's request to cite its vendor is honored.
- "Re-derived from committed aggregates" is not "reproduced"; say which.

## Where this sits

| Skill / agent | Role |
|---|---|
| `sdv-research-paper` (here) | The writing process and its gates |
| `sdv-paper-reviewer` | Read-only lens reviews of a draft or abstract |
| `sdv-modeling` | Which metric, interval, resample and test are correct |
| `sdv-model-build` / `sdv-model-reviewer` | Building and auditing the model the paper reports |
| external skills | `references/external-skills.md`: which of the 22 installed research skills add value, and their hazards |
