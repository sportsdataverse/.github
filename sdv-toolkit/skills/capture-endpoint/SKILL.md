---
name: capture-endpoint
description: Hardened, provider-agnostic single-body capture for ESPN/Fox/CBS — structured id discovery, error-envelope skip, atomic writes.
disable-model-invocation: true
---

## Purpose

Fetch one representative response body per endpoint and write it to
`<provider>/inputs/sample_bodies/<league>/<host>/<endpoint>.json`.
Avoids the two known bugs in naive capture scripts: (1) greedy first-long-number regex matching an inner id instead of the top-level event id; (2) storing ESPN error envelopes as if they were valid payloads.

---

## Provider constants

```python
ESPN_SITE      = "https://site.api.espn.com/apis/site/v2/sports"
ESPN_SITE_ALT  = "https://site.web.api.espn.com/apis/site/v2/sports"
ESPN_WEB       = "https://web.api.espn.com/apis/v2/sports"
ESPN_CORE      = "https://sports.core.api.espn.com/v2/sports"
ESPN_CORE3     = "https://sports.core.api.espn.com/v3/sports"
ESPN_CDN       = "https://cdn.espn.com/core"

FOX_BASE       = "https://bifrost.foxsports.com/prod/v1"
FOX_HEADERS    = {"apikey": "<key>", "api-version": "2"}

CBS_BASE       = "https://www.cbssports.com/nfl/scorestrip/feed"  # napi variant per sport
```

---

## Error-envelope predicate

```python
def is_error_envelope(body: dict) -> bool:
    """Return True if ESPN/Fox returned an error dict, not real data."""
    if not isinstance(body, dict):
        return False
    keys = set(body.keys())
    # ESPN: {"code": 400, "message": "..."} or {"code":..., "detail":...}
    if keys <= {"code", "message", "detail", "name", "error"}:
        return True
    # Fox/CBS: {"error": "..."} top-level only
    if "error" in keys and len(keys) <= 2:
        return True
    return False
```

---

## Structured event-id discovery (fixes cricket IPL inner-id bug)

**Never** parse the scoreboard URL or body with a greedy `re.search(r'\d{6,}', ...)`. Walk the structure:

```python
import requests, json

def get_event_ids(sport: str, league: str, limit: int = 3) -> list[int]:
    """Discover top-level event ids from the ESPN scoreboard endpoint."""
    url = f"{ESPN_SITE}/{sport}/{league}/scoreboard"
    r = requests.get(url, params={"limit": limit}, timeout=15)
    r.raise_for_status()
    body = r.json()
    # ESPN Site v2 shape: body["events"][i]["id"]
    events = body.get("events") or []
    return [int(e["id"]) for e in events if "id" in e]
```

For non-Site v2 endpoints (Core, Web), adapt the key path accordingly — always use `["id"]` on the top-level event object, not on nested team/athlete dicts.

---

## Atomic write

```python
import os, tempfile, pathlib, json

def atomic_write(path: str | pathlib.Path, data: dict) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.rename(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
```

---

## Full single-endpoint capture recipe

```python
import requests, pathlib, json

def capture_endpoint(
    sport: str,
    league: str,
    endpoint: str,          # e.g. "summary", "scoreboard"
    params: dict,           # e.g. {"event": event_id}
    out_dir: pathlib.Path,
    host: str = "site",     # "site" | "site_alt" | "web" | "core"
) -> pathlib.Path | None:
    base = {
        "site": ESPN_SITE, "site_alt": ESPN_SITE_ALT,
        "web": ESPN_WEB,   "core": ESPN_CORE,
    }[host]
    url = f"{base}/{sport}/{league}/{endpoint}"
    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        print(f"SKIP {url} → HTTP {r.status_code}")
        return None
    body = r.json()
    if is_error_envelope(body):
        print(f"SKIP {url} → error envelope: {list(body.keys())}")
        return None
    out_path = out_dir / league / host / f"{endpoint}.json"
    atomic_write(out_path, body)
    print(f"OK   {out_path}")
    return out_path
```

---

## Typical invocation

```bash
# From sdv-internal-refs/espn/tools/
python espn_capture_league.py soccer epl
# Or call the recipe directly in a one-off script:
event_ids = get_event_ids("soccer", "epl")
capture_endpoint("soccer", "epl", "summary",
                 {"event": event_ids[0]},
                 pathlib.Path("espn/inputs/sample_bodies"))
```
