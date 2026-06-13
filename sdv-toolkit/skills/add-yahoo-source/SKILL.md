---
name: add-yahoo-source
description: Add a Yahoo Sports source — capture + catalog in sdv-internal-refs/yahoo (HTML/JSON scrape).
disable-model-invocation: true
---

# Add Yahoo Source

Adds a new Yahoo Sports data source to the sdv-internal-refs/yahoo catalog. Yahoo Sports is a **scrape** (no clean public API). Data is embedded as JSON in HTML pages or available from partial XHR endpoints observable via browser DevTools. Treat all Yahoo captures as brittle with a capture date.

---

## Provider Facts

| Property | Value |
|---|---|
| Base URL | `https://sports.yahoo.com` |
| Auth | None (session cookie for some personalized pages; not required for public data) |
| Data delivery | Embedded JSON in HTML (`root.App.main = {...}` or `__PRELOADED_STATE__`) OR partial XHR JSON |
| Catalog | `c:\Users\saiem\Documents\sdv-internal-refs\yahoo\` |
| Body captures | `c:\Users\saiem\Documents\sdv-internal-refs\yahoo\inputs\sample_bodies\` |
| Fragility | HIGH — Yahoo restructures pages across seasons; always date-stamp captures |

---

## Step 1 — Locate the embedded JSON blob

Open `https://sports.yahoo.com/<sport>/<page>` in a browser with DevTools open.

**Method A — Page source search:**

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://sports.yahoo.com/<sport>/<page>" \
  | grep -o 'root\.App\.main = {.*' | head -c 500
```

The blob is typically `root.App.main = {...};` or `window.__PRELOADED_STATE__ = {...};` in a `<script>` tag.

**Method B — XHR intercept (browser DevTools → Network → Filter: Fetch/XHR):**

Navigate to the page, look for requests returning `application/json`. Common XHR patterns:
- `https://api-secure.sports.yahoo.com/v1/editorial/...`
- `https://sports.yahoo.com/_td/<sport>/...`
- `https://query1.finance.yahoo.com/...` (finance crossover for sports betting lines)

Document the full URL + any required headers (User-Agent, Referer, Cookie if applicable).

---

## Step 2 — Extract and save the embedded blob (Python)

```python
import re, json, httpx, pathlib

url = "https://sports.yahoo.com/<sport>/<page>"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

resp = httpx.get(url, headers=headers, follow_redirects=True)
html = resp.text

# Try root.App.main pattern
m = re.search(r'root\.App\.main\s*=\s*(\{.+?\});\s*\n', html, re.DOTALL)
if not m:
    # Try __PRELOADED_STATE__ pattern
    m = re.search(r'__PRELOADED_STATE__\s*=\s*(\{.+?\});\s*\n', html, re.DOTALL)

blob = json.loads(m.group(1))

out = pathlib.Path("yahoo/inputs/sample_bodies/<sport>/<page>.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(blob, indent=2))
print(f"Saved {out} — top-level keys: {list(blob.keys())[:10]}")
```

---

## Step 3 — Navigate to the data of interest

The embedded blob is large (often 300KB–2MB). Navigate the key path:

```python
import json, pathlib

blob = json.loads(pathlib.Path("yahoo/inputs/sample_bodies/<sport>/<page>.json").read_text())

# Common paths:
# blob["context"]["dispatcher"]["stores"]["GamesStore"]["games"]
# blob["context"]["dispatcher"]["stores"]["TeamStore"]["teams"]
# blob["context"]["dispatcher"]["stores"]["StandingsStore"]["standings"]

# Walk it:
def walk_keys(d, depth=0):
    if depth > 3 or not isinstance(d, dict):
        return
    for k, v in d.items():
        print("  " * depth + k, type(v).__name__,
              f"({len(v)} items)" if isinstance(v, (list, dict)) else "")
        walk_keys(v, depth + 1)

walk_keys(blob)
```

Document the key path (e.g. `context.dispatcher.stores.GamesStore.games`) in the returns doc.

---

## Step 4 — Write the returns doc

Create `yahoo/catalogs/<sport>_<page>_returns.md`:

```markdown
# Yahoo Sports — <Sport> <Page> Returns

**Source type:** HTML embedded JSON (scrape)  
**Captured:** YYYY-MM-DD  
**URL:** `https://sports.yahoo.com/<sport>/<page>`  
**Blob key:** `root.App.main`  
**Data path:** `context.dispatcher.stores.<Store>.items`

| Field | Type | Notes |
|---|---|---|
| id | string | |
...

## Extraction selector

```python
blob["context"]["dispatcher"]["stores"]["<Store>"]["items"]
```

## Fragility notes

- Structure last verified: YYYY-MM-DD
- Known to change: page layout restructures at season start
- Fallback: check XHR tab for `_td/<sport>/` endpoints
```

---

## Step 5 — Extend the Yahoo catalog

Open `yahoo/yahoo_catalog.yaml` and add:

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

---

## Gotchas

- **No stable API contract.** Yahoo rebuilds pages aggressively. A capture from one season may not work the next. Always record the capture date and re-verify at season start.
- **Some pages require a cookie.** The home page and most scoreboard pages do not, but some fantasy-adjacent pages do. Do not scrape authenticated pages without explicit project approval.
- **XHR endpoints change without notice.** The `_td/<sport>/` pattern is observable today but has changed before. Treat XHR captures as lower-reliability than embedded JSON.
- **Rate limit gently.** Yahoo blocks aggressive scrapers. Add `time.sleep(1)` between requests in any bulk capture script.
- Mark all Yahoo sources `fragility: high` in the catalog. This informs downstream decisions about whether to maintain a Yahoo-backed wrapper vs. deprecating it.
