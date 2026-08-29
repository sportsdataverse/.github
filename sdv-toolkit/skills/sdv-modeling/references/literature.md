# Literature — the published work behind each model family we ship

> Reference file of the `sdv-modeling` skill. Every local path below was verified
> to exist on disk when this file was written; every claim about a paper's
> content was read from the paper, not inferred from its title.

**The corpus is already on your machine.** `Sports-Research-Papers/md/` holds
**685 markdown-converted papers** (338k lines) — JQAS, MIT Sloan, NESSIS, CMSAC,
Hudl StatsBomb, plus a `randoms/` tier. Paths below are relative to
`GitHub-Data/sdv-dev/Sports-Research-Papers/md/`.

Search it before reaching for the web:

```sh
grep -ril "adjusted plus-minus" "Sports-Research-Papers/md" | head
```

---

## Read this one first if you touch fourth down

**`library/conferences/.../2023 Analytics have some humility a statistical view
of fourth-down decision making - Brill.md`**

This is not a reading-list entry. It is a direct critique of the class of model
we ship **default-on** (`nfl/nfl_fourth_down.py`, and the CFB fourth-down / FG /
two-point surfaces added in 0.0.68). From its abstract, quoted:

> "The EP and WP functions which are widely used today are statistical models
> fit from historical data. These models, however, are subject to serious
> statistical flaws: **selection bias, overfitting, ignoring autocorrelation,
> and ignoring uncertainty quantification.** ... far fewer fourth-down decisions
> are as obvious as analysts claim."

Three of those four flaws map onto gaps this toolkit only just closed or has
not closed:

| Brill's flaw | our state |
|---|---|
| ignoring autocorrelation | addressed by purged/embargoed CV (`sklearn-xgboost.md` §A2) — **new in 0.8.0** |
| ignoring uncertainty quantification | addressed by conformal intervals (`metrics-and-gates.md` §1) — **new in 0.8.0**, and not yet applied to any shipped surface |
| selection bias | **open** — see the Daly-Grafstein entry below |
| overfitting | partially: gates are oracle-based, but we have no catalytic-prior-style smoothing |

**Actionable consequence:** a fourth-down recommendation shipped without an
interval overstates its own confidence, and that is the paper's central finding.
This is a candidate `sdv-model-reviewer` gate, not just prose.

**`.../2023 - Correcting for preferential bias in NFL fourth-down decision
making - Daly-Grafstein.md`** is the selection-bias half: outcomes are only
observed for the decision the coach actually made, so a model fit on observed
fourth downs is fit on a non-random sample of game states.

---

## By model family

### EP — expected points

| paper | why it matters here |
|---|---|
| `2012 - A Markov Model of Football Using Stochastic Processes to Model a Football Drive` (Goldner) | The absorbing-Markov-chain derivation of EP: states are (down, distance, yardline), absorbing states are the drive outcomes, and EP is the point-weighted absorption probability. This is the *structural* alternative to our fitted 7-class GBM, and the reason to check that our class **mix** is right and not just the scalar `ep` (`metrics-and-gates.md`, multiclass section). |
| `nflWAR- A Reproducible Method for Offensive Player Evaluation in Football (Extended Ed)` and its JQAS version | The reproducible-pipeline framing our `nfl` surface descends from. |
| `2023 Analytics have some humility...` (Brill) | above |

### WP — win probability

| paper | why it matters here |
|---|---|
| `2016 Statistical methods in sports with a focus on win probability and...` | The broadest treatment in the corpus; the reference for what a WP model is and is not claiming. |
| `2023 Machine learning for sports betting should forecasting models be optimised for accuracy or calibration - Walsh, Joshi` | Directly the accuracy-vs-calibration question. Read this before setting any probability gate: it is the empirical case that the two objectives diverge, which is why `metrics-and-gates.md` gates calibration separately rather than trusting a single score. |
| `2012 - Solving the Problem of Inadequate Scoring Rules for Assessing Probabilistic Football Forecast Models` | Why a scalar proper score is not sufficient — the same argument as the Brier decomposition section. |

### RAPM / adjusted plus-minus

| paper | why it matters here |
|---|---|
| `.../2024 - Revisiting player contributions in regularized adjusted plus-minus models` | Closest published work to our RAPM family; read before changing the penalty or the design. |
| `.../2024 - Estimating positional plus-minus in the NBA - Gong et al` | Positional decomposition of the same design. |
| `2020 Identifying group contributions in NBA lineups with spectral analysis` | Lineup-level structure our stint design flattens. |
| `2010 NBA Adjusted Plus Minus using Regularization` (PDF, no md) · `2010 A_Regression_Based_Adjusted_Plus_Minus_Statistic for NHL - McDonald` · `2011 An_Improved_Adjusted_Plus_Minus...` | The origin papers, for the alpha/standardization conventions that our confirmed lambda-applied-to-nothing incident collided with (`failure-modes.md` §2). |

### Player impact, WAR, aging

| paper | why it matters here |
|---|---|
| `.../2022 - Estimating Aging Curves Using Multiple Imputation to Examine Career Trajectories of MLB Offensive Players` | **The only serious missing-data treatment in the corpus**, and it addresses the exact selection problem in aging curves: players who decline stop appearing, so a naive curve is fit on survivors. Relevant to every projection we publish. |
| `.../2024 - Introducing Grid WAR rethinking WAR for starting pitchers - Brill et al` | Modern WAR construction. |
| `.../2026 - Can a Stadium Full of Monkeys ... An empirical Bayesian Estimator of Manager Value - Kahan` | Empirical-Bayes shrinkage applied to a small-sample entity — the pattern our player priors need. |
| `.../2020 - PFF WAR Modeling Player Value in American Football` | Football-side WAR; pairs with our PFF recon. |

### Team strength, ratings, strength of schedule

| paper | why it matters here |
|---|---|
| `.../2019 - Efficient Estimation of Distribution-free dynamics in the Bradley-Terry Model` | **Bradley-Terry is the paired-comparison foundation our ratings implicitly assume and the toolkit never names.** Read before building another ratings engine. |
| `.../2025 - Pairwise-Elo rating system - Wong et al` | The most Elo-dense paper in the corpus; the k-factor and carryover conventions we have nowhere documented. |
| `2003 Colley Matrix Method` · `.../2012 - Robust Rankings for College Football` · `.../2012 - The Sensitivity of College Football Rankings to Several Modeling Choices` | Least-squares/Colley ratings and — importantly — how much the answer moves with modeling choices. That sensitivity result is the argument for our never-lower gate rule. |

### xG and shot value

| paper | why it matters here |
|---|---|
| `.../2025 - One x G model to rule them all` (Bajons, Harringer) | Cross-competition xG generalization — the question our PWHL/NHL xG split raises. |
| `2016 spatio temporal analysis for team sports` · `Modeling Player and Team Performance in Basketball - Terner, Franks` | Spatial structure of shot value; the NBA shot-value spine's context. |

### Simulation, brackets, season sims

| paper | why it matters here |
|---|---|
| `.../2020 - Models for generating NCAA men s basketball tournament bracket pools - Ludden et al` | Bracket simulation done properly, including the correlation between game outcomes that an independent-games sim gets wrong. |
| `.../2011 - Seed distributions for NCAA men's basketball tournament` · `.../2012 - The Dreaded Middle Seeds` | Seed-level base rates to calibrate a sim against. |

### The betting market as a baseline

| paper | why it matters here |
|---|---|
| `2018 Asset Pricing and Sports Betting - Tobias Moskowitz` | The strongest statement of the market-as-efficient-baseline that our MAE-vs-closing-line gates assume. |
| `.../2020 - Profiting from overreaction in soccer betting odds - Wheatcroft` | Where that efficiency breaks — the case for keeping a market baseline as a *gate* rather than a ceiling. |

---

## External anchors, verified

| source | what it gives |
|---|---|
| Baumer, Matthews & Nguyen (2023), *Big Ideas in Sports Analytics and Statistical Tools for their Investigation*, [arXiv:2301.04001](https://arxiv.org/abs/2301.04001) | The single best survey for this ecosystem: it organizes sports analytics around exactly our four families — **expected value of a game state, win probability, measures of team strength, and betting market data**. Start here for a new sport. |
| `BradleyTerry2` R package, [CRAN vignette](https://cran.r-project.org/web/packages/BradleyTerry2/vignettes/BradleyTerry.html) | Fits Bradley-Terry logit/probit/cauchit with contest-specific effects (home advantage), by ML, penalized quasi-likelihood, or bias-reduced ML. Note the documented limit: **no tie handling** — `BTm` needs a binary or binomial response, which rules it out unmodified for a sport with draws. |
| Russell Carleton's stabilization work, summarized at [FanGraphs](https://www.fangraphs.com/blogs/a-new-way-to-look-at-sample-size/) and [Baseball Prospectus](https://www.baseballprospectus.com/news/article/17659/baseball-therapy-its-a-small-sample-size-after-all/) | Split-half reliability, later Cronbach's alpha and Kuder-Richardson 21 for binary events, to find the sample at which a rate stat carries as much signal as noise (conventionally r ≈ 0.7). K-rate stabilizes near 60 PA; HR rate needs 300+. **We have no stabilization analysis anywhere**, which means every per-player rate we publish is served without a minimum-sample caveat. |

---

## What this file does NOT yet cover

Named honestly so nobody mistakes silence for absence:

- **Stabilization applied to our own stats.** The method is cited; the analysis
  has never been run on SDV data. Until it is, we do not know the minimum
  possessions/attempts for any published rate.
- **Survival/hazard models** (31 corpus papers) — injury, drive continuation,
  career length. No SDV model uses them.
- **Count and zero-inflated models** (45 corpus papers) — the natural family for
  scoring, which we currently model as a continuous margin.
- **Multiple-testing correction** (34 corpus papers). We scan thousands of
  players and dozens of features and report the extremes without correction.
- **Copula / correlated simulation** (8 corpus papers), which the odds workstream
  (WS5) will need and which no shipped simulator does.
