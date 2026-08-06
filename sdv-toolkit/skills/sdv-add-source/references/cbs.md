# Provider: CBS Sports (NAPI)

Capture + catalog only — CBS is not currently wired into sdv-py codegen.
The NAPI is a REST API with a self-describing registry; data-backed resources
are auth-free, live scoring / recruiting resources are gated (`torq-token`).

## Host / URL family

| Property | Value |
|---|---|
| Primary base | `https://api.cbssports.com/napi` |
| Cloud mirror | `https://sdf-api.cbssports.cloud/napi` (functionally identical; use primary for captures, note the mirror in the catalog) |
| Auth | none for data resources; `torq-token` for live/recruiting |
| Self-docs | `GET /resource/endpoint/registry` |
| OpenAPI | `sdv-swagger/cbssports-napi.openapi.yaml`, regenerated via `cbs/gen_napi_openapi.py` |

## Data-backed resource paths (auth-free)

| Resource | Path |
|---|---|
| League info | `/resource/league/{leagueId}` |
| Season teams | `/resource/season/teams/{seasonId}` |
| Team players | `/resource/team/players/{teamId}` |
| Team standings | `/resource/team/standings/{teamId}` |

## Id-discovery strategy

Query the registry endpoint first — it lists every registered endpoint with
its parameter shapes, which is how you find `leagueId` / `seasonId` values
before capturing:

```bash
curl -s "https://api.cbssports.com/napi/resource/endpoint/registry" \
  | python -m json.tool | grep -i "<sport>"
```

`seasonId` values are not always predictable — derive from the registry or
an existing known-good league response, never guess.

## Error-envelope shape

Same bare `{"error": "..."}`, `len(keys) <= 2` shape as Fox.

## Catalog location

`sdv-internal-refs/cbs/`:
- `captures/_sample/<sport>/<league>/{league,season_teams_<seasonId>,team_players_<teamId>,team_standings_<teamId>}.json`
- `catalogs/<sport>_returns.md`
- `cbs_catalog.yaml`:

  ```yaml
  - sport: <sport>
    league_id: <leagueId>
    season_id: <seasonId>
    resources_captured: [league, season_teams, team_players, team_standings]
    capture_date: YYYY-MM-DD
    returns_doc: catalogs/<sport>_returns.md
  ```

After adding captures, regenerate the OpenAPI: `python cbs/gen_napi_openapi.py`
from `sdv-internal-refs`.

## Divergences / gotchas

- **Do not probe recruiting endpoints.** A prior crawl burned 8,400+ requests
  trying to reach recruiting data behind the torq gate — all 404s. If the
  registry shows `auth: torq` for a resource, document it as gated and stop;
  don't attempt-loop past it (same "bound attempts, not saves" rule as the
  capture phase's error-envelope skip).
- Live per-game scoring endpoints (`/resource/game/...`) need a game id only
  meaningful in-season — don't attempt off-season bulk captures of them.
- If/when CBS is wired into sdv-py it becomes a flat-API family (endpoints
  YAML in `FLAT_APIS`), not an ESPN-style `leagues.yaml` row.
