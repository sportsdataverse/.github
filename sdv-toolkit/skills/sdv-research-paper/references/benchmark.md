# Benchmark integrity (betting markets, ratings, oracles)

When a paper's claim is "X vs a benchmark", the benchmark is a measured
instrument, and its construction is part of the result. How to build it (de-vig,
line timing, matching) lives in `sdv-modeling` → `references/betting-markets.md`.
This file covers what the paper must show about it.

No installed external skill (market-mechanics-betting, sports-betting-analyzer,
statsmodels) would have caught any of these on paper 05. One of them computes edge
on raw prices with the vig still in.

## Checks (each one a FAIL)

1. **Same instrument across compared windows.** Report the benchmark's
   composition (books per game, share of single-source games, source mix) by
   season and by tune/holdout split. FAIL if it changes across a compared
   boundary and the paper doesn't say so. *Paper 05: from 2020 the college
   archive fell from 12–22 offshore books to 3–5, and 39–47% of 2023–25 games
   are single-book. The in-tune gap for 2020–21 (0.0084) already matched the
   holdout's (0.0074), so the "holdout widening" is partly a different market.*
2. **Only real sources in the aggregate.** A "median across books" excludes
   aggregators and model sites (`consensus`, `numberfire`, `teamrankings`).
   List the sources that were included.
3. **"Closing" is evidenced.** "Closing line" requires quote timestamps, or a
   documented archive convention, **per league**. Without them, write "final
   archived line" and give the same hedge to every league it applies to.
   *Paper 05 hedged NFL timing but not college.*
4. **Orientation and sum gates.** Assert spread and moneyline favor the same
   side; that matters most at neutral sites. Assert de-vigged probabilities sum
   to 1 and raw book sums lie in a plausible overround band. Report the
   failures and how much they move the metric.
5. **Fixed conversions state their bias.** A fixed spread-to-probability σ, or
   any untuned conversion, is either fitted or reported with the direction it
   moves the headline gap. *Paper 05: the fitted σ (11.83 NFL / 14.15 college vs
   13.45 / 15.5 used) understates the gap by about 0.0002.*
6. **Method sensitivity reported.** Give the headline gap under each margin-removal
   method (proportional, Shin, power) and any blend weight, even when the
   effect is small: "≤ 0.00007" is a result.
7. **Market-informed inputs are labelled.** Any model input built from the
   benchmark itself (closing spread or total, line movement) makes that model
   *market-informed*. Its gains are never credited to "the open model" or to
   "public data". *Paper 05: the "18%" link was fed the closing spread.*
8. **Rivals specific to markets.** Every headline model-vs-market contrast lists,
   among its rivals:
   - the market aggregates many bettors' models of the same public data, so it
     is not necessarily "outside information";
   - the benchmark already contains the candidate model;
   - the benchmark's composition changed (check 1);
   - the archive covers games non-randomly.
   Each rival gets a check, and a tested rival is reported with its measured size.
9. **Coverage isn't random.** Re-run the headline with the thinnest-archive
   seasons dropped. *Paper 05: the only seasons where the model beats the line,
   2006 and 2008, are the thinnest years in the archive.*
10. **Advice needs an evaluated decision.** A paper that addresses bettors or
    teams evaluates a decision: a bet rule with its closing-line value (CLV) and
    calibration, or a team choice with its expected value. Otherwise the
    conclusion doesn't address them. Never frame output as betting advice (some
    installed skills end in "place bet" and Kelly-stake steps).
