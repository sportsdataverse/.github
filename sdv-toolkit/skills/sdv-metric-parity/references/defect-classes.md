# The six metric-parity defect classes

From the 2026-10-08 percentile audit (ClaudeCowork `notes/2026-10-08-percentile-plausibility-audit.md`) and its
fixes (sdv-py #733 / #734, cfbfastR-cfb-data #139, nfl-data #79, sdv-db #135, GOP #312 / #313). Each class lists
the symptom, the test that catches it, and the real case.

## 1. Population mismatch

The display and the ladder divide by different row sets: the same numerator over rushes in one place and over all
plays in the other.

- **Symptom:** mean shown far from 49.5; the median value lands at the 3rd or 95th percentile.
- **Test:** `ladder_parity.py` → `MISMATCH`. Quick manual version: compare the box value's p50 with the ladder
  p50 for the same season; they should be within a few percent.
- **Cases:** CFB F1, Def Run Stuff Rate (`rushing_stuff_rate`, rushes, p50 .161) ranked against `play_stuffed`
  (`yards_gained <= 0` over all plays including incompletions, p50 .300): 13% showed 1st, should be ~34th. NFL B1
  the same (mean shown 13.4 → 49.7 after the fix). C1 `opportunity_run` over all plays (mean shown 95). D1 player
  percentiles over every player-game including 1-play QBs (fix: a position cohort plus a minimum-plays floor).

## 2. Definition drift

Same population, a slightly different numerator: one side includes a play type or yardage the other excludes.

- **Symptom:** mean shown 52-56 or 44-47 (`WATCH`), a few percentile points of systematic bias.
- **Test:** `WATCH` from the script; then diff the two definitions term by term.
- **Cases:** A2 / B5 Yards per Dropback: the box excluded sack yards, the ladder included them (mean shown 54.3).
  A3 Yards per Play: the ladder counted interception-return yards as offense (46.9). B4 NFL kneels kept in the box,
  excluded from the ladder. B6 NFL scrambles counted as rushes in the box, as dropbacks in the ladder. D4 passer
  success rate excluded sacks and interceptions.

## 3. Orientation

A field-position value read in the wrong frame: ESPN's NFL `start.yardLine` is home-relative, so a red-zone flag
built on it never fires for one side.

- **Symptom:** one side's mean shown is pinned near 0 or 100 while the other is near 50.
- **Test:** `--side-col home` → `SIDE-ASYMMETRY`. Remember that home-field advantage alone moves the sides 10-15
  points apart.
- **Cases:** B2 NFL `rz_play` / `goal_to_go` from home-relative `start.yardLine`: home red zone essentially never
  detected. CFB uses `start.yardsToEndzone`, which is possession-relative. The 2026 Arizona `AZ` alias broke the
  NFL field-position flip in the same way.

## 4. Split denominators

Situational splits (pass and rush, early and late downs) each divided by the whole situation's plays instead of
their own.

- **Symptom:** the pass and rush rates add up to the overall rate, and both read low.
- **Test:** `--split overall=part1+part2` → `SPLIT-SUMS`. Rates on their own denominators combine as a weighted mean,
  which lies between the parts, never at their sum.
- **Cases:** E1 sdv-py CFB late-down pass and rush success: `.mean()` over every late-down play
  (`cfb_pbp.py:9179-9180`). C-lane team-season values that equalled rush rate × per-carry rate for the same reason.

## 5. Ladder season and era

The right definition against the wrong year's ladder.

- **Symptom:** a game from an older or newer season shows a skewed mean when it is ranked against a fixed year; the
  ladder's own medians drift across seasons.
- **Test:** run the script for every season with that season's ladder; then grep the display for a pinned year
  (`PERCENTILE_YEAR`, a hard-coded `2025`) and check that each game uses its own season's ladder, with a fallback
  only when that ladder is missing or thin.
- **Cases:** A1 `PERCENTILE_YEAR = 2025` for every game; the havoc median moved 0.13 (2005-20) → 0.10 (2021-24) →
  0.123 (2025) → 0.145 (2026) because pass-breakup coverage in the pbp text changed (PBU 0.2% of plays in 2024,
  4.9% in 2026), so a median 2026 game showed 62nd and a 2021-24 game 26th.

## 6. Display semantics

The numbers match, but the display turns them into the wrong percentile.

- **Symptom:** visible only in rendered cells.
- **Test:** unit tests at the display layer: a null value renders a dash with no percentile; ties use midrank
  (`(below + 0.5 * equal) / n`), not the top of the tie run; a quarter or half is not ranked against a full-game
  ladder; level bands don't use margin keys.
- **Cases:** A4 a red zone with no snaps rendered "0%, 5th". A5 / D2 ties ranked at the top of the run. A6 the v2
  box ranked single quarters against a full-game ladder. A7 a trend-band typo (`success_pas`) and `_margin` keys
  on level bands.

## Two habits that would have caught most of these earlier

- **Every mapping from display metric to ladder key gets a parity row in CI**: one season's values and ladder, run
  through `ladder_parity.py`, asserting `OK`. A rename or redefinition on either side then fails the build instead of
  shipping a 1st-percentile cell.
- **Never redefine a column under its old name.** When `play_stuffed` became rush-only, cfb-data changed its
  definition and its consumers in one PR. A silent redefinition leaves every other reader quietly wrong.
