# R package conventions

- Every exported function needs a complete roxygen2 block: title +
  description before the first `@param`, `@param` for every argument,
  `@examples` present with live network calls wrapped in `\dontrun{}`.
- `@return` must include a `| col_name | type | description |` markdown
  table (R-style types: `character`, `integer`, `double`, `logical`,
  `list`, `data.frame`, `tibble`) — a one-liner without a table is a gap.
- `DESCRIPTION` needs `Roxygen: list(markdown = TRUE)` or the `@return`
  table renders as plain text in pkgdown instead of a table.
- Functions return tibbles; output columns are snake_case.
- `_pkgdown.yml`'s `reference:` section must list every export — no orphan
  exports (exported, not listed) and no phantom references (listed, not
  exported).
- Python ↔ R documentation parity: when the same dataset is documented on
  both sides, use identical `col_name` values and aligned descriptions —
  Python's live in `manual_column_descriptions.yaml`, R's in the `@return`
  roxygen block; update both when a column changes.
- R numeric fidelity for cross-language parity: R>=4.0 `fround` semantics,
  80-bit long-double sum, non-`na.rm` null-poisoning (R's sum/max return
  `NA`, polars skips nulls), dplyr C-locale group order.
- pkgdown theming: never apply a blanket bootswatch template — it strips
  the bespoke fonts/glow. Light theme stays untouched; fix dark mode only.
  Hardcoded near-black text (`#0f0f0f` etc.) → `var(--bs-body-color)`.
  Dead BS4 `.navbar-dark` selectors → `[data-bs-theme="dark"] .navbar`.
- Install packages with `remotes::install_github()`, not `devtools::`.
- Conventional Commits, no AI co-author trailer.
