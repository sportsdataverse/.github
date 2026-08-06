# Provider: Yahoo Sports

Capture + catalog only, and the most fragile provider in the routing table —
Yahoo has no clean public API. Data is embedded as JSON in HTML pages, or in
partial XHR endpoints observable via browser DevTools. Treat every capture as
brittle and date-stamped.

## Host / URL family

| Property | Value |
|---|---|
| Base URL | `https://sports.yahoo.com` |
| Auth | none for public pages (a session cookie gates some personalized/fantasy-adjacent pages — do not scrape those without explicit approval) |
| Data delivery | embedded JSON (`root.App.main = {...}` or `window.__PRELOADED_STATE__ = {...}` in a `<script>` tag) OR partial XHR JSON |
| Fragility | **HIGH** — Yahoo restructures pages across seasons |

## Id-discovery strategy

There's no numeric event id to discover the way ESPN has one — the "id" here
is the **key path** into the embedded blob. Locate it two ways:

**A — page-source search:**

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://sports.yahoo.com/<sport>/<page>" \
  | grep -o 'root\.App\.main = {.*' | head -c 500
```

**B — XHR intercept** (browser DevTools → Network → Fetch/XHR filter). Common
patterns: `api-secure.sports.yahoo.com/v1/editorial/...`,
`sports.yahoo.com/_td/<sport>/...`. Document the full URL + any required
headers (User-Agent, Referer, Cookie).

Once you have the blob, walk it to find the data of interest instead of
guessing depth:

```python
def walk_keys(d, depth=0):
    if depth > 3 or not isinstance(d, dict):
        return
    for k, v in d.items():
        print("  " * depth + k, type(v).__name__,
              f"({len(v)} items)" if isinstance(v, (list, dict)) else "")
        walk_keys(v, depth + 1)
```

Common store paths: `context.dispatcher.stores.GamesStore.games`,
`...TeamStore.teams`, `...StandingsStore.standings`.

## Extraction (Python)

```python
import re, json, httpx

resp = httpx.get(url, headers={"User-Agent": "Mozilla/5.0 ..."}, follow_redirects=True)
m = re.search(r'root\.App\.main\s*=\s*(\{.+?\});\s*\n', resp.text, re.DOTALL)
if not m:
    m = re.search(r'__PRELOADED_STATE__\s*=\s*(\{.+?\});\s*\n', resp.text, re.DOTALL)
blob = json.loads(m.group(1))
```

## Error-envelope shape

N/A — HTML scrapes don't return a JSON error envelope; the failure mode is
either an HTTP error or a regex miss (the `root.App.main` /
`__PRELOADED_STATE__` pattern not matching, meaning the page structure
changed). Treat a failed extraction the same way the capture phase treats an
error envelope: skip and log, don't save a partial/garbage body.

## Catalog location

`sdv-internal-refs/yahoo/`:
- `inputs/sample_bodies/<sport>/<page>.json`
- `catalogs/<sport>_<page>_returns.md` — include `Blob key`, `Data path`,
  and a `Fragility notes` section (last-verified date, known drift triggers,
  fallback XHR pattern)
- `yahoo_catalog.yaml`:

  ```yaml
  - sport: <sport>
    page: <page>
    source_type: html_embedded_json
    blob_key: root.App.main
    data_path: context.dispatcher.stores.<Store>.items
    capture_date: YYYY-MM-DD
    fragility: high
    returns_doc: catalogs/<sport>_<page>_returns.md
  ```

## Divergences / gotchas

- No stable contract — a capture that works one season may break the next.
  Always record the capture date and re-verify at season start.
- XHR endpoints are lower-reliability than embedded JSON; the `_td/<sport>/`
  pattern has changed before without notice.
- Rate limit gently — Yahoo blocks aggressive scrapers; `time.sleep(1)`
  between requests in any bulk capture script.
- Mark every Yahoo catalog entry `fragility: high` — it's the signal
  downstream decisions use to decide whether to maintain a Yahoo-backed
  wrapper vs. deprecating it.
