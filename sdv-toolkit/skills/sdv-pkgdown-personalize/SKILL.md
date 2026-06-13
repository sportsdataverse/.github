---
name: sdv-pkgdown-personalize
description: Apply the bespoke SportsDataverse pkgdown theming and fix the shared extra.css Bootstrap-5 bugs (dark-mode-invisible text, dead .navbar-dark selectors).
disable-model-invocation: true
---

# SDV pkgdown Theming — Preserve Brand + Fix BS5 Bugs

The SDV R pkgdown sites share a bespoke look (custom fonts, glow effect). Two
Bootstrap 5 bugs are present in the shared `extra.css` across all sites. Apply
the fixes below WITHOUT flattening the brand.

---

## Ground rules

- **Do NOT apply a blanket bootswatch template** (e.g. `template: bootswatch: flatly`
  in `_pkgdown.yml`). This strips custom fonts, glow CSS, and color overrides.
- **Light theme: do not touch.** All visual regressions reported so far are dark-mode.
- **Dark mode: keep + fix on-brand.** The goal is legibility, not redesign.
- **Preview is not available locally** (bespoke fonts + Vercel CDN refs). Verify
  on deploy.

---

## _pkgdown.yml — settings to preserve

When editing `_pkgdown.yml`, keep these blocks unchanged:

```yaml
template:
  bslib:
    # keep any custom variable overrides already present, e.g.:
    # primary: "#...", font_scale: ..., etc.
  # Do NOT add: bootswatch: <theme>
```

If `bslib:` variables are absent and need to be added, only add explicit
overrides — never replace the block with a bootswatch name.

---

## Bug 1 — Dark-mode-invisible hardcoded text color

Any `color: #0f0f0f` (or similar near-black hex, e.g. `#111`, `#1a1a1a`,
`#0d0d0d`) in `pkgdown/extra.css` is invisible against dark-mode backgrounds.

**Before:**
```css
.some-selector {
  color: #0f0f0f;
}
```

**After:**
```css
.some-selector {
  color: var(--bs-body-color);
}
```

`--bs-body-color` is the Bootstrap 5 semantic token: `#212529` in light mode,
`#dee2e6` (or theme override) in dark mode. It tracks the active theme
automatically without a media query.

Search the file for all near-black hex literals before committing:

```bash
grep -nE 'color:\s*#(0[0-9a-f]{5}|1[0-3][0-9a-f]{4})' pkgdown/extra.css
```

---

## Bug 2 — Dead .navbar-dark selectors (Bootstrap 4 → 5 rename)

Bootstrap 5 removed the `.navbar-dark` utility class. SDV `extra.css` files
still target it, so those rules are silently ignored in dark mode.

**Before (BS4 / dead in BS5):**
```css
.navbar-dark .navbar-brand,
.navbar-dark .navbar-nav .nav-link {
  color: #ffffff;
}
```

**After (BS5):**
```css
[data-bs-theme="dark"] .navbar .navbar-brand,
[data-bs-theme="dark"] .navbar .navbar-nav .nav-link {
  color: #ffffff;
}
```

Also verify the navbar HTML in the rendered site uses `data-bs-theme="dark"`
on the `<nav>` element (pkgdown 1.6+ sets this automatically when
`bslib` dark mode is active). If you see `class="navbar navbar-dark"` in
the source, the pkgdown version is old — upgrade pkgdown first.

```r
remotes::install_github("r-lib/pkgdown")
```

---

## Checklist before pushing

- [ ] `grep -n 'navbar-dark' pkgdown/extra.css` returns zero results.
- [ ] `grep -nE 'color:\s*#[0-1][0-9a-f]' pkgdown/extra.css` returns zero results.
- [ ] `_pkgdown.yml` has no `bootswatch:` key.
- [ ] `bslib:` variable overrides are preserved (not replaced).
- [ ] `devtools::document()` runs clean (no roxygen warnings).
- [ ] Commit, push to `main` (or PR branch), verify on Vercel deploy.

---

## Regenerating the site locally (limited fidelity)

```r
pkgdown::build_site(preview = FALSE)
# Open docs/index.html in browser — fonts / glow may differ from deploy
```

Full fidelity only on Vercel. For a quick CSS-only sanity check, open the
built `docs/` HTML directly and inspect element with DevTools dark-mode
emulation (`Rendering > Emulate CSS media feature prefers-color-scheme: dark`).
