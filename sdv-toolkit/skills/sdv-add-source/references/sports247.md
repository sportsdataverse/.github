# Provider: 247Sports

HTML scrape with embedded JSON (Next.js `__NEXT_DATA__`), primarily for
recruiting data. **Two sdv-py surfaces already ship from this provider** —
`sports247` (the 247Sports Recruit Database, `ipa.247sports.com`, curl_cffi)
and `sports247_site_pages` — both flat-API families
(`tools/codegen/endpoints/sports247*.yaml`, registered in `FLAT_APIS`). Check
that surface before adding a new wrapper; the endpoint you want may already
exist.

## Host / URL family

| Property | Value |
|---|---|
| Site pages | `247sports.com` — HTML, embedded JSON in `<script id="__NEXT_DATA__">` |
| RDB API | `ipa.247sports.com` — the underlying recruit-database API the shipped `sports247` stem wraps (needs `curl_cffi`, not plain `requests` — same TLS-fingerprint consideration as stats.nba.com) |
| Auth | none (HTML scrape / public API) |

## Id-discovery strategy

For the site-pages route: capture the page, then
`JSON.parse(document.getElementById('__NEXT_DATA__').textContent)` (or the
Python equivalent, `BeautifulSoup` + `json.loads`) and document the nested
path to the data of interest (recruiting rankings, team stats, etc.).

For the RDB API route: prefer extending the existing `sports247` flat-API
YAML over a fresh scrape — it already has the endpoint + id shapes mapped.

## Error-envelope shape

Site-pages: a missing/malformed `__NEXT_DATA__` blob is the failure signal
(structural drift, not a JSON error envelope) — treat like Yahoo's failed
regex match, skip and log. RDB API: follows the generic bare-`{"error": ...}`
shape.

## Catalog location

`sdv-internal-refs/247sports/inputs/sample_bodies/<sport>/<page>.html` for
site-page captures; document the nested data path + capture date in the
returns doc alongside the extraction snippet.

## Divergences / gotchas

- **Structure drifts across recruiting cycles** — mark every capture with a
  date, same discipline as Yahoo.
- Don't build a second HTML scraper for data the `sports247` / `On3`
  (`on3.yaml`) flat-API stems already cover — check `sportsdataverse/`'s
  existing recruiting surface first.
- ESPN also has a recruiting-adjacent surface; when adding a new recruiting
  endpoint, confirm which provider actually owns the field before scraping
  247Sports for something ESPN already exposes cleanly.
