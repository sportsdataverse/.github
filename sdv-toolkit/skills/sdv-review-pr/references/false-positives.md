# False positives — do not raise these

Read before finalizing findings. Every entry was suggested by a bot or reviewer and
declined for a documented reason (75 declines read across 810 PRs). Raising them
costs the author a reply and teaches them to skim the review.

When a finding *looks* like one of these, either drop it or reframe it as the real
question named in the right-hand column.

| Don't raise | Why it's wrong here | The real question, if any |
|---|---|---|
| Rewrite `pl.col(x) == True` / `== False` to `pl.col(x)` / `~`, or add `# noqa: E712` | House style for polars boolean masks; ruff suppresses E712 (CodeRabbit runs flake8, which is not the repo linter) | **Can the column be null?** (U-DATA-5) |
| Remove `from __future__ import annotations` in sdv-py | Needed for PEP 604/585 on the 3.9 floor; bots demanded removal ~15 times; repo docs contradict each other | none — flag the contradictory docs separately, not in the PR |
| Typing, Google docstrings, or mypy fixes on test modules, private `_modules`, producer-only tooling, or generated shims | The mypy `files` ratchet scopes typing to source modules; generated files are fixed in the generator | Only exported public callables need docstrings (route to `sdv-python-reviewer` docstring lens) |
| E501 line length, E704 one-line stubs | Not enabled in the repo linter | none |
| Pin GitHub Actions to commit SHAs in one workflow | Org convention is tag pins; re-pinning existing SHA pins to node24 SHAs is fine | `persist-credentials: false` when a later step pushes |
| SSRF / OS-injection / credential findings on operator-controlled CLI args, hard-coded URLs, list-form `subprocess` args, or localhost placeholder creds in plans | No untrusted input reaches them | Untrusted **workflow expressions** in `run:` are real (U-CI-2) |
| "Fix" a verbatim R port so it diverges from the R oracle (mean-of-rates, coalesce order, defaults) | Parity against R output is the contract | Open an upstream issue; partition assertions if a divergence is deliberate |
| Edit verbatim raw captures or immutable run-log manifests | Captures are evidence; editing them corrupts provenance | none |
| `btoa` / `AbortSignal.timeout` "may not exist"; Next.js route `params` "is not a Promise" | Node ≥22 and Workers have both; Next 15+/16 `params` is a Promise | none |
| "polars `str.replace` defaults to literal"; "avoid `empty_as_null` before polars 1.36" | Wrong: it defaults to regex; the lock pins polars 1.42 | Check the installed version before any polars API claim |
| Route every HTTP read through `dl_utils.download()` | Wrong for remote columnar (Arrow/parquet) reads and status-based retry; sdv-py CLAUDE.md documents the exception | Status classification (PY-10) |
| Re-level markdown headings in NEWS.md / docs against file-wide convention | Breaks the file's existing structure | none |
| Apply a repo rule outside its scope ("no HTTP in this repo" on a capture-only path; a sibling repo's sparse-checkout list) | Rules have scopes | Quote the rule's scope before citing it |
| "Missing year shift" where the shift happens one layer up | Adding it creates a double shift | Trace the season through every layer (U-DATA-1) |
| A finding against code that is already fixed at the current head | Stale-head review | Verify every finding against `headRefOid` |
| Delete real data to satisfy a consistency heuristic (e.g. clear pass-breakup credit on interceptions) | Would erase real events (78 tip-drill plays) | Ask for a partition or flag, not a deletion |
| Refactor/consolidate a verbatim lift of battle-tested code inside a phased PR | Scope creep; the phase plan owns it | A linked follow-up phase |
| UI "consistency" that contradicts an existing design decision (compact rows on one route, interleaved Lighthouse runs) | Deliberate decisions | Ask whether the decision still holds, don't assert |
| Suggest `git pull --rebase`, `setup.py`/`requirements*.txt`, pandas instead of polars, lookaround regex in polars, an id→Utf8 "paper-over" cast, or an AI co-author trailer | Contradict CLAUDE.md conventions | none |
| `skip_on_ci()` on cfbfastR `cfbd_*` / artifact tests | CI sets `NOT_CRAN` and `CFBD_API_KEY` deliberately | none |
| Owner-decided residual risks (ufw 5432 open, PFF under the read scope) when the PR doesn't change them | Already decided | Raise only if the PR changes the exposure |

## Framing rules for anything that survives

- A finding states the **failure scenario** (input/state → wrong output), not a
  preference.
- Moved code is in scope (U-GIT-6); code the PR didn't touch or move is an
  "observation", never a blocker.
- A bot finding already open on the PR is cited by link, not restated as new.
