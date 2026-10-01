# Claims audit: numbers are necessary, words are where papers fail

A numbers-provenance check (every numeral comes from `numbers.json`) catches
hand-typed numbers. It does not catch a true number under a false word. All
four false sentences in SSAC27 paper 05's abstract passed it.

## 1. Provenance (phase 2)

- Every printed number resolves to a pipeline key, **in the abstract too**.
  If the abstract is a separate file (`abstract.md`), the check must read it.
  FAIL if any abstract numeral is hand-typed, even when it currently matches.
- Every number keeps its key's precision; round the uncertainty first, then the
  estimate to match (see `inference.md`).
- "Re-derived from committed aggregates" ≠ "reproduced from inputs". Say which.

## 2. Claim → evidence table (phase 3)

Build a table with one row per sentence of the abstract and of the conclusion:

| # | Sentence | Claim type | Key(s) / table / figure | Holds for every result it covers? |

FAIL a row when:

1. **No key.** The sentence asserts a size or direction with nothing computed behind it.
2. **Unbacked comparative or universal.** "more than", "larger", "stable",
   "every", "none", "converge", "nothing", "only", "always" with no computed
   value or assertion. *Paper 05: "can move a Brier score by more than the gap" (0.0026 vs 0.0054).*
3. **Summary overreach.** A summary sentence that one result in the paper
   contradicts. Check each against the **largest** effects in the results.
   *Paper 05: "techniques did not move the gap" while one closed 18%; "untested"
   for the roster/recruiting priors that were the largest single gain.*
4. **One quantity, one name, one sign.** The same difference is called the same
   thing with the same sign in body, abstract, tables, CSVs and axes.
   *Paper 05: a "blend minus line" difference is called a "gain", and a CSV prints it with the opposite sign.*
   The converse also holds: one name means one quantity. *Paper 11: "consensus"
   meant both the market median and the four-system mean.*
5. **Out-of-sample leads.** Any in-sample champion number in the abstract,
   introduction or conclusion has its holdout counterpart in the same
   sentence, and is labelled "selected from k configurations on these games".
6. **Like-for-like.** A ranking of models where one got inputs or tuning the
   others did not, unless the matched comparison is also reported.
7. **Correlation ≠ agreement.** High correlation between estimators is not
   evidence they're equally accurate when their accuracy gaps are comparable to
   the headline effect.
8. **Pointer integrity.** A claim cited to a figure or table must be visible
   there. *Paper 05: "stable across seasons" cited to a figure in which the gap widens after 2016.*
9. **Design constants.** Every fixed constant (blend weight, prior strength,
   sigma, de-vig method) gets a source, a reason, or a sensitivity check.
   Compared model families get the same knobs tuned.
10. **Motivating claims carry numbers.** An introduction claim about a size
    prints the size from the pipeline.
11. **The abstract uses the body's preferred measure.** If the body says a
    measure is biased and replaces it, the abstract reports the replacement.
    *Paper 11: the abstract's convergence week came from a self-correlation the
    body says flatters a slow-moving rater; the corrected measure moved FPI
    from week 2 to week 8.*
12. **One sentence, one sample.** Numbers sharing a sentence come from the
    same sample (seasons, units, filters), or the sentence names each sample.
    *Paper 11: team-weeks 2015–25 and games 2016–25 under one "same 6,082 games".*
13. **No post-hoc reinstatement.** A result left out of an earlier draft (for
    example as "suggestive only") may not return to the abstract once its
    value is known, unless the paper says so. The same goes for a correction
    family or test chosen after the p-value was seen. *Paper 15: a spread
    result dropped on 09-30 came back with a three-contrast family picked after
    the fact (adjusted p 0.08).*
14. **"Only" is a universal.** "Only in X" needs the same test run on every
    other unit and on both sides of each market, using the paper's own rule.
    *Paper 15: "longshot bias only in men's college basketball", while NHL
    longshots pass the paper's own Bonferroni cutoff; only the favorite side
    had been tested.*
15. **Sibling consistency.** Slate or program papers that rule on the same
    seasons and markets don't reach opposite verdicts without citing each
    other. *Paper 15 calls closing football lines calibrated; paper 05 finds
    them miscalibrated on overlapping seasons.*

16. **Scope claims cover every number they cover.** A blanket claim about the
    method ("uses only information available before kickoff") must hold for every
    forecast the paper reports, including leave-one-season-out blends fit on
    future seasons. Otherwise scope it ("the open model uses …").
17. **No generalising from a narrow variant set.** "Play-by-play features don't
    help" can't rest on 3 college-only variants. State the set tried.

## 3. Reasoning pass on Discussion and Conclusion

Flag: argument from ignorance ("didn't help here → won't help"), post hoc
rationalization of a surprise, hasty generalization from a finite technique
list, and causal verbs on unmeasured variables.

## 4. Automating it

The cheapest mechanical check is a word lint, which then routes to human/agent
judgment: grep abstract + conclusion for
`once|frozen|sealed|untouched|untested|no effect|did not|not detectably|nothing|stable|well[- ]calibrated|within error|more than|converge|adds nothing|every|none|only|always`
and require each hit to appear in the claim→evidence table with a key.
