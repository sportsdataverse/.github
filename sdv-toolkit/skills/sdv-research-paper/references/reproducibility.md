# Reproducibility: a stranger can regenerate every number

"Code and results are in the repository" is a claim, and the paper owes it the same
evidence as any other claim. Paper 05 recorded input hashes but fetched live
releases that keep changing, git-ignored the cache, and its holdout step either
copied the stored result or refused to run. So "three commands regenerate this
paper" held for nobody but the author.

## Checks (each one a FAIL)

1. **Inputs pinned, not just hashed.** Every input is a pinned release asset, a
   committed snapshot, or an archived file with a DOI or URL plus checksum. A
   hash of a moving "latest" release is a fail, because the hash records the
   drift and doesn't prevent it.
2. **Provenance is what was fetched.** Record the upstream commit or tag the cached
   data actually came from, not the latest commit at run time.
3. **Hashes are checked.** On rerun, every recorded input and script hash is
   compared, and a mismatch stops the run.
4. **Clean-clone rerun.** Before submission, run in a fresh clone with
   `uv sync --frozen` and the documented commands. Every `numbers.json` key
   must reproduce at its printed precision. Record the date and commit in STATUS.
5. **The holdout has a verify mode.** The holdout guard has a mode that
   recomputes the score from pinned inputs and compares it with the record. It
   neither copies the record nor refuses to run. Third parties can then reproduce
   it without breaking the single-look rule (the look ledger counts *new*
   scorings, not verifications).
6. **Monte Carlo error is below printed precision.** Re-run bootstraps and
   simulations with 2 or 3 other seeds. A printed digit must be steadier than the spread
   across seeds. *Paper 05's 5-decimal interval endpoints moved by 1–2e-5.*
7. **Known-effect simulation.** Every estimator and interval method the abstract
   relies on has a committed simulation. It recovers a planted effect, and its
   null coverage matches its nominal level. The output is checked into
   `results/`.
8. **Repository visibility.** If the paper or the venue says the work is open source,
   the repository is public at submission, with licences that permit it. Licensed
   data is released only as aggregates, and the paper says so.
9. **Post-result changes are classified.** Every change made after a result was seen
   is logged with its cause: *bug*, *data* or *real*. A change caused by something
   real is reported as exploratory, never as a "fix".
