---
name: regen-docs
description: Regenerate sdv-py reference docs, verify the Docusaurus build, and snapshot a versioned archive at release.
disable-model-invocation: true
---

## Purpose

Keep the generated reference docs in sync after adding or changing endpoints, parsers, or schemas. All commands run from the repo root (`c:\Users\saiem\Documents\GitHub-Data\sdv-dev\sdv-py`) unless noted.

---

## What is generated vs. hand-authored

| Path | Status |
|---|---|
| `docs/docs/<sport>/index.md` | GENERATED — never hand-edit |
| `docs/docs/<sport>/reference/*.md` | GENERATED — never hand-edit |
| `docs/docs/<sport>/_category_.json` | GENERATED — never hand-edit |
| `docs/docs/reference/` | GENERATED — never hand-edit |
| `docs/docs/intro.md` | Hand-authored — survives regen |
| `docs/docs/architecture/` | Hand-authored — survives regen |
| `docs/docs/parsers/` | Hand-authored — survives regen |
| `docs/docs/quality-of-life.md` | Hand-authored — survives regen |

---

## Step 1 — Regenerate

```bash
# Rewrites generated per-league reference subtrees and docs/docs/reference/.
# Conceptual pages (intro, architecture, parsers) are preserved.
uv run python tools/codegen/generate.py --docs
```

To also regenerate wrapper/loader/parser modules (not just docs):

```bash
uv run python tools/codegen/generate.py   # wrappers + docs together
```

---

## Step 2 — Drift gate

```bash
# Fails if generated files are stale relative to YAML sources.
# Run this before committing; CI runs it on every PR.
uv run python tools/codegen/generate.py --check
```

The `sdv-codegen` pre-commit hook also runs `--check` automatically when `tools/codegen/` or `*.yaml` files are staged.

---

## Step 3 — Docusaurus build check

```bash
cd docs
yarn build
```

Expected warnings that are **OK to ignore**:
- Broken-link warnings inside the frozen `versioned_docs/version-0.0.50/` tree.
- Broken internal links in `CHANGELOG.md` doctoc fragments.

Any new broken-link warning outside those two locations is a real error to fix.

---

## Step 4 — Release snapshot (do once per release)

```bash
cd docs
yarn version:docs <x.y.z>   # e.g. yarn version:docs 0.0.52
```

This snapshots `docs/docs/` → `versioned_docs/version-<x.y.z>/` and adds an entry to `versions.json`. Then commit:

```bash
git add docs/versioned_docs/version-<x.y.z>/ docs/versions.json
git commit -m "docs(release): snapshot version <x.y.z>"
```

**Never** change `lastVersion` away from `'current'` in `docusaurus.config.ts` — the live unversioned tree must stay the default URL.

---

## Deployment

Vercel auto-deploys on every push to `main`. Do **not** add a GitHub Pages action — it would double-publish. To preview locally:

```bash
cd docs
yarn start   # http://localhost:3000
```

---

## Common mistakes

- Editing a file under `docs/docs/<sport>/reference/` by hand — it will be clobbered on the next `--docs` run.
- Running `yarn version:docs` without first building (`yarn build`) — the snapshot captures whatever is on disk, so a broken build gets frozen.
- Forgetting `--check` before pushing — the drift gate will fail CI.
