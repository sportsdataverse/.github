---
name: add-cbs-league
description: Add a CBS Sports (NAPI) league/resource — capture + catalog in sdv-internal-refs/cbs.
disable-model-invocation: true
---

# Add CBS League

Adds a new sport or league to the CBS Sports NAPI catalog in sdv-internal-refs. The NAPI is a REST API with a self-describing registry. Data-backed endpoints are auth-free; live scoring and recruiting resources are gated or id-restricted.

---

## Provider Facts

| Property | Value |
|---|---|
| Primary base | `https://api.cbssports.com/napi` |
| Cloud mirror | `https://sdf-api.cbssports.cloud/napi` |
| Auth | None for data resources; torq-token for live/recruiting |
| Self-docs | `GET /resource/endpoint/registry` |
| OpenAPI | `c:\Users\saiem\Documents\GitHub-Data\sdv-dev\sdv-swagger\cbssports-napi.openapi.yaml` |
| Body captures | `c:\Users\saiem\Documents\sdv-internal-refs\cbs\captures\_sample\` |
| OpenAPI gen | `c:\Users\saiem\Documents\sdv-internal-refs\cbs\gen_napi_openapi.py` |

---

## Data-Backed Resource Paths (auth-free)

| Resource | Path | Notes |
|---|---|---|
| League info | `/resource/league/{leagueId}` | League metadata |
| Season teams | `/resource/season/teams/{seasonId}` | All teams in a season |
| Team players | `/resource/team/players/{teamId}` | Current roster |
| Team standings | `/resource/team/standings/{teamId}` | Team standings block |

**Discover IDs** by querying the registry endpoint first:

```bash
curl -s "https://api.cbssports.com/napi/resource/endpoint/registry" \
  | python -m json.tool | grep -i "<sport>"
```

This lists all registered endpoints with their parameter shapes — use it to identify `leagueId` / `seasonId` values before capturing.

---

## Step 1 — Discover IDs via the registry

```bash
curl -s "https://api.cbssports.com/napi/resource/endpoint/registry" \
  > cbs/captures/_sample/endpoint_registry.json

# Find league IDs
python -c "
import json
reg = json.load(open('cbs/captures/_sample/endpoint_registry.json'))
# inspect reg for your sport
"
```

---

## Step 2 — Capture data-backed resources

```
cbs/captures/_sample/<sport>/<league>/league.json
cbs/captures/_sample/<sport>/<league>/season_teams_<seasonId>.json
cbs/captures/_sample/<sport>/<league>/team_players_<teamId>.json
cbs/captures/_sample/<sport>/<league>/team_standings_<teamId>.json
```

```bash
SPORT="<sport>"
LEAGUE_ID="<leagueId>"
SEASON_ID="<seasonId>"
TEAM_ID="<teamId>"
BASE="https://api.cbssports.com/napi"

curl -s "$BASE/resource/league/$LEAGUE_ID" \
  | python -m json.tool > cbs/captures/_sample/$SPORT/$LEAGUE_ID/league.json

curl -s "$BASE/resource/season/teams/$SEASON_ID" \
  | python -m json.tool > cbs/captures/_sample/$SPORT/$LEAGUE_ID/season_teams_$SEASON_ID.json

curl -s "$BASE/resource/team/players/$TEAM_ID" \
  | python -m json.tool > cbs/captures/_sample/$SPORT/$LEAGUE_ID/team_players_$TEAM_ID.json

curl -s "$BASE/resource/team/standings/$TEAM_ID" \
  | python -m json.tool > cbs/captures/_sample/$SPORT/$LEAGUE_ID/team_standings_$TEAM_ID.json
```

---

## Step 3 — Regenerate the OpenAPI

After adding new captures, regenerate the OpenAPI spec from the live registry:

```bash
cd c:\Users\saiem\Documents\sdv-internal-refs
python cbs/gen_napi_openapi.py
# output: sdv-swagger/cbssports-napi.openapi.yaml (via symlink or copy)
```

---

## Step 4 — Write the returns doc

Create `cbs/catalogs/<sport>_returns.md`:

```markdown
# CBS Sports NAPI — <Sport> Returns

Captured: YYYY-MM-DD  
League ID: `<leagueId>`  
Season ID: `<seasonId>`

## /resource/league/{leagueId}

**URL:** `https://api.cbssports.com/napi/resource/league/<leagueId>`  
**Top-level keys:** `["league", "conferences", "divisions"]`

| Field | Type | Notes |
|---|---|---|
| league.id | string | |
...

## Divergence notes

- <shape differences vs other CBS leagues>
```

---

## Step 5 — Extend the CBS catalog

Open `cbs/cbs_catalog.yaml` and add:

```yaml
- sport: <sport>
  league_id: <leagueId>
  season_id: <seasonId>
  resources_captured:
    - league
    - season_teams
    - team_players
    - team_standings
  capture_date: YYYY-MM-DD
  returns_doc: catalogs/<sport>_returns.md
```

---

## Gotchas

- **Do not probe recruiting endpoints.** A prior crawl spent 8,400+ requests attempting to reach recruiting data behind the torq gate — all 404s. If an endpoint requires a torq token, document it as gated and stop. The API registry will show `auth: torq` for those resources.
- The cloud mirror (`sdf-api.cbssports.cloud`) is functionally identical to the primary. Use the primary for captures; note the mirror in the catalog for redundancy.
- `seasonId` values are not always predictable. Derive them from the registry or from an existing known-good league response before running bulk captures.
- Live per-game scoring endpoints (`/resource/game/...`) require a game ID that is only meaningful during the season. Do not attempt off-season bulk captures of live resources.
