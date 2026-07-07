---
name: sdv-stack
description: Use to manage a chain of stacked PRs in an SDV repo — mapping the stack, merging bottom-up, retargeting + rebasing children after a squash-merge, and re-running the codegen drift gate at each new branch head. Invoke for "merge the stack", "land these stacked PRs", "retarget after merge", "stacked PR status", or when 2+ open PRs base on each other.
---

# Stack — land stacked PRs bottom-up without stranding work

Stacked PRs (each branch based on the previous) let phased work ship
reviewably, but every landed parent invalidates its children: SDV repos
squash-merge, so a child branch still carries the parent's now-duplicate
commits and must be rebased, and the codegen drift gate must re-pass at the
child's NEW head. This skill encodes the sequence that avoids the three
failure modes that have actually happened: stale-base drift failures,
hand-merged docs conflicts, and premature branch deletion stranding work.

**Depth cap: ~4.** Beyond that, one bottom-of-stack change costs N rebases +
N drift re-checks. If the stack is deeper, land the bottom before opening
the next PR.

## 1. Map the stack

```sh
gh pr list --state open --json number,title,headRefName,baseRefName \
  --template '{{range .}}{{.number}}\t{{.baseRefName}} <- {{.headRefName}}\t{{.title}}\n{{end}}'
```

Draw the parent graph (base ← head). The **bottom** PR is the one whose base
is `main`. Everything else merges only after its parent.

## 2. Land the bottom PR

1. Confirm CI green. Distinguish real failures from known repo flakes
   (0-second Vercel previews; live-test timeout races) — a flake on an
   unrelated surface does not block, but say so explicitly when merging.
2. Merge (squash). **Do NOT delete the head branch until
   `gh pr view <n> --json state` says `MERGED`** — premature cleanup has
   stranded work before.

## 3. Retarget + rebase the next child

GitHub auto-retargets children to `main` when the merged head branch is
deleted, but the child branch still CONTAINS the parent's pre-squash
commits. Rebase them away — never merge them forward:

```sh
git fetch origin
git checkout <child-branch>
git rebase --onto origin/main <old-parent-branch> <child-branch>
git push --force-with-lease origin <child-branch>
```

`--force-with-lease` only; never plain `--force`. If the PR didn't
auto-retarget, `gh pr edit <n> --base main` first.

**Conflict rule for generated files:** never hand-merge codegen output or
generated docs. Take either side, finish the rebase, then regenerate —
the regeneration in step 4 makes the tree correct regardless.

## 4. Re-verify at the new head

The drift gate passing at the old head means nothing at the new one:

```sh
uv run python tools/codegen/generate.py && uv run python tools/codegen/generate.py --check
uv run pytest -q   # or the repo's scoped preflight
```

Commit any regen delta as its own `chore(docs): regenerate reference docs`
commit. Check `git status` for a silent `uv.lock` re-lock before committing.

## 5. Repeat

The child is now the bottom. Loop steps 2–4 until the stack is flat.

## Quick reference — the three past incidents this prevents

| Incident | Guard |
|---|---|
| Drift gate red after retarget (regenerated at old head) | Step 4 always re-runs `generate.py --check` at the new head |
| Docs merge-conflict hand-resolved wrong | Step 3 conflict rule: take either side, regenerate |
| Branch deleted while PR still open → stranded work | Step 2: verify `state == MERGED` before any cleanup |
