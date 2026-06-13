---
name: add-fox-league
description: Add a Fox Sports (Bifrost) league/sport — capture + catalog in sdv-internal-refs/fox.
disable-model-invocation: true
---

# Add Fox League

Adds a new sport or league to the Fox Sports (Bifrost) catalog in sdv-internal-refs. The Bifrost API is uniform across all sports — one OpenAPI spec governs every endpoint. This skill covers capture + catalog only (no sdv-py wrappers yet; Fox is not currently wired into sdv-py codegen).

---

## Provider Facts

| Property | Value |
|---|---|
| Base URL | `https://api.foxsports.com/bifrost/v1` |
| Auth | `apikey=<key>` + `api-version=<ver>` as query params (public, no account) |
| OpenAPI spec | `c:\Users\saiem\Documents\GitHub-Data\sdv-dev\sdv-swagger\foxsports-api-openapi.yaml` |
| Body captures | `c:\Users\saiem\Documents\sdv-internal-refs\fox\inputs\sample_bodies\` |

The `{sport}` slug is a path segment. Example: `hockey`, `basketball`, `football`, `baseball`, `soccer`, `golf`, `tennis`, `mma`.

---

## Bifrost Endpoint Surfaces

These are the surfaces defined in the OpenAPI spec. All are parameterized on `{sport}`:

| Category | Path pattern | Notes |
|---|---|---|
| Scoreboard | `/{sport}/scoreboard` | Event list with scores |
| League hub | `/{sport}/league/{leagueId}/teamnav` | Team nav |
| League hub | `/{sport}/league/{leagueId}/standings` | Standings |
| League hub | `/{sport}/league/{leagueId}/conferences` | Conferences |
| League hub | `/{sport}/league/{leagueId}/polls` | AP/Coaches polls |
| League hub | `/{sport}/league/{leagueId}/stats-con` | Stats |
| League hub | `/{sport}/league/{leagueId}/odds` | Odds hub |
| Event | `/{sport}/event/{eventId}/data` | Full event data |
| Event | `/{sport}/event/{eventId}/matchup` | Matchup |
| Event | `/{sport}/event/{eventId}/recap` | Recap |
| Event | `/{sport}/event/{eventId}/odds` | Event odds |
| Team | `/{sport}/team/{teamId}/roster` | Roster |
| Team | `/{sport}/team/{teamId}/stats` | Stats |
| Team | `/{sport}/team/{teamId}/gamelog` | Game log |
| Team | `/{sport}/team/{teamId}/standings` | Standings |
| Team | `/{sport}/team/{teamId}/header` | Team header |
| Search | `/search` | Cross-sport search |
| Explore | `/{sport}/explore` | Explore hub |
| Trending | `/{sport}/trending` | Trending content |

---

## Step 1 — Identify the sport slug and leagueId

Look at existing captures in `fox/inputs/sample_bodies/` for naming conventions (e.g. `football/nfl/`, `basketball/nba/`). The `leagueId` is visible in the Fox Sports web UI URL or in an existing scoreboard response.

---

## Step 2 — Capture representative bodies

```
fox/inputs/sample_bodies/<sport>/<league>/scoreboard.json
fox/inputs/sample_bodies/<sport>/<league>/standings.json
fox/inputs/sample_bodies/<sport>/<league>/event_data.json
fox/inputs/sample_bodies/<sport>/<league>/team_roster.json
```

Fetch manually with curl or httpx. Example:

```bash
API_KEY="<your-key>"
API_VER="<version>"
SPORT="hockey"
LEAGUE_ID="<leagueId>"

curl -s "https://api.foxsports.com/bifrost/v1/$SPORT/league/$LEAGUE_ID/standings?apikey=$API_KEY&api-version=$API_VER" \
  | python -m json.tool > fox/inputs/sample_bodies/$SPORT/$LEAGUE_ID/standings.json
```

Capture at minimum: scoreboard, standings, one event/data, one team/roster.

---

## Step 3 — Write the returns doc

Create `fox/catalogs/<sport>_<league>_returns.md`:

```markdown
# Fox Sports Bifrost — <Sport> <League> Returns

Captured: YYYY-MM-DD  
Sport slug: `<sport>`  
League ID: `<leagueId>`

## scoreboard

**URL:** `https://api.foxsports.com/bifrost/v1/<sport>/scoreboard?...`  
**Top-level keys:** `["games", "league", "date", ...]`

| Field | Type | Notes |
|---|---|---|
| games[].id | string | |
| games[].status | string | |
...

## standings

...

## Divergence notes

- <any shape differences vs other Fox leagues>
```

---

## Step 4 — Extend the Fox catalog

Open `fox/fox_catalog.yaml` and add the new entry:

```yaml
- sport: <sport>
  league: <league-label>
  league_id: <leagueId>
  surfaces_captured:
    - scoreboard
    - standings
    - event_data
    - team_roster
  capture_date: YYYY-MM-DD
  returns_doc: catalogs/<sport>_<league>_returns.md
```

---

## Gotchas

- The `apikey` is a public browser key observable in network traffic on foxsports.com. It is not a secret but may rotate; keep a note of the version you used.
- Some `{sport}/league/{leagueId}/polls` endpoints 404 for leagues that do not have polls (e.g. minor leagues). Document as absent rather than retrying.
- `event/{eventId}/odds` may be empty before lines are posted. Capture a pre-game body closer to kickoff.
- Refer to `sdv-swagger/foxsports-api-openapi.yaml` for the authoritative schema; the OpenAPI is the source of truth if a response shape is ambiguous.
