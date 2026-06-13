---
name: add-provider-source
description: Add a league/source for ANY SportsDataverse provider (ESPN, Fox Bifrost, CBS NAPI, Yahoo, 247Sports, Torvik) — capture bodies, generate the returns doc, extend the catalog, scaffold the wrapper.
disable-model-invocation: true
---

# Add Provider Source

Router skill. Identify the provider first, then follow the matching sub-flow. All providers share a common Part A (capture + catalog in sdv-internal-refs) before any sdv-py wiring.

---

## Provider Routing Table

| Provider | Skill | Base URL | Auth |
|---|---|---|---|
| ESPN | `add-espn-league` + `add-sport-parser` | `site.api.espn.com` / `sports.core.api.espn.com` | None (public) |
| Fox Sports (Bifrost) | `add-fox-league` | `api.foxsports.com/bifrost/v1` | `apikey` + `api-version` query params |
| CBS Sports (NAPI) | `add-cbs-league` | `api.cbssports.com/napi` | None for data resources |
| Yahoo Sports | `add-yahoo-source` | `sports.yahoo.com` (HTML scrape) | None (scrape) |
| 247Sports | See below | `247sports.com` | None (HTML scrape) |
| Barttorvik | See below | `barttorvik.com` | None (CSV/JSON endpoints) |

**For ESPN** → use `add-espn-league` (wrapper registration) and `add-sport-parser` (parser layer). This skill does not repeat those steps.

---

## Part A — Capture + Catalog (all non-ESPN providers)

**Working dir:** `c:\Users\saiem\Documents\sdv-internal-refs`

### 1. Capture representative bodies

Create the directory structure:

```
<provider>/inputs/sample_bodies/<sport-or-league>/<endpoint>.json
```

Fetch and save bodies manually or via a helper script. Record:
- Full URL with query params used
- Capture date (`YYYY-MM-DD`)
- Response status / size

### 2. Write the returns doc

Create `<provider>/catalogs/<sport>_returns.md`:

```markdown
# <Provider> — <Sport/League> Returns

Captured: YYYY-MM-DD

## <endpoint-name>

**URL:** `https://...`  
**Host:** `api.provider.com`  
**Top-level keys:** `["events", "season", ...]`

| Field | Type | Notes |
|---|---|---|
| id | string | |
| ...

**Divergence notes:** ...
```

### 3. Extend the provider catalog

Each provider directory has a master catalog file (e.g. `fox/fox_catalog.yaml`, `cbs/cbs_catalog.yaml`). Add your new sport/league entry following the existing schema.

---

## Part B — sdv-py Wiring (provider-specific)

### ESPN

→ Follow `add-espn-league` for wrapper registration.  
→ Follow `add-sport-parser` for the parser layer.

### Fox Sports

→ Follow `add-fox-league`. The OpenAPI at `c:\Users\saiem\Documents\GitHub-Data\sdv-dev\sdv-swagger\foxsports-api-openapi.yaml` covers the full Bifrost surface.

### CBS Sports

→ Follow `add-cbs-league`. Regenerate the OpenAPI with `python cbs/gen_napi_openapi.py` after capturing new resources.

### Yahoo Sports

→ Follow `add-yahoo-source`. Extracting the embedded JSON blob is the critical first step.

### 247Sports

247Sports serves content as HTML with embedded JSON in `<script id="__NEXT_DATA__">` (Next.js). Steps:
1. Capture the page HTML: `<provider>/inputs/sample_bodies/247sports/<sport>/<page>.html`
2. Extract `JSON.parse(document.getElementById('__NEXT_DATA__').textContent)` or equivalent Python `BeautifulSoup` + `json.loads` extraction.
3. Document the nested path to the data of interest (recruiting rankings, team stats, etc.) in the returns doc.
4. Mark as a scrape with capture date — 247Sports structure drifts across recruiting cycles.

### Barttorvik (Men's CBB)

Barttorvik exposes clean CSV/JSON endpoints (no auth). The barttorvik catalog in sdv-internal-refs maps the known endpoints. Steps:
1. Fetch from `https://barttorvik.com/<endpoint>.json?...` or `...csv`.
2. Save to `barttorvik/inputs/sample_bodies/<endpoint>.json`.
3. The sdv-py wrapper already exists in `sportsdataverse/mbb/` (Torvik-backed functions). Check the existing surface before adding a new one — the function may already exist.
4. For new endpoints, follow the single-table module pattern: `espn_<league>_<dataset>(...)` returning `pl.DataFrame`.

---

## Commit Convention

```
feat(<provider>): add <sport/league> capture + catalog
feat(<prefix>): scaffold <provider> <sport> wrappers
```

No `Co-Authored-By` trailers.
