# Provider: Fox Sports (Bifrost)

Capture + catalog only — Fox is **not currently wired into sdv-py codegen**.
The Bifrost API is uniform across all sports, so one OpenAPI spec governs
every endpoint; there is no per-league scaffold step here.

## Host / URL family

| Property | Value |
|---|---|
| Base URL | `https://api.foxsports.com/bifrost/v1` |
| Auth | `apikey=<key>` + `api-version=<ver>` query params (public browser key, not a secret, but may rotate) |
| OpenAPI spec | `sdv-swagger/foxsports-api-openapi.yaml` — authoritative when a response shape is ambiguous |

`{sport}` is a path segment: `hockey`, `basketball`, `football`, `baseball`,
`soccer`, `golf`, `tennis`, `mma`.

## Endpoint surfaces (all parameterized on `{sport}`)

| Category | Path pattern |
|---|---|
| Scoreboard | `/{sport}/scoreboard` |
| League hub | `/{sport}/league/{leagueId}/{teamnav,standings,conferences,polls,stats-con,odds}` |
| Event | `/{sport}/event/{eventId}/{data,matchup,recap,odds}` |
| Team | `/{sport}/team/{teamId}/{roster,stats,gamelog,standings,header}` |
| Search | `/search` (cross-sport) |
| Explore / Trending | `/{sport}/explore`, `/{sport}/trending` |

## Id-discovery strategy

`leagueId` is visible in the Fox Sports web UI URL or in an existing
scoreboard response. Look at existing captures under `fox/inputs/sample_bodies/`
for naming precedent (e.g. `football/nfl/`) before inventing a new one.

## Error-envelope shape

Bare `{"error": "..."}`, top-level only, `len(keys) <= 2` — distinct from
ESPN's `{"code", "message", ...}` shape.

## Catalog location

`sdv-internal-refs/fox/`:
- `inputs/sample_bodies/<sport>/<league>/{scoreboard,standings,event_data,team_roster}.json`
- `catalogs/<sport>_<league>_returns.md`
- `fox_catalog.yaml` — master catalog; add an entry per sport/league:

  ```yaml
  - sport: <sport>
    league: <league-label>
    league_id: <leagueId>
    surfaces_captured: [scoreboard, standings, event_data, team_roster]
    capture_date: YYYY-MM-DD
    returns_doc: catalogs/<sport>_<league>_returns.md
  ```

## Divergences / gotchas

- Capture at minimum: scoreboard, standings, one `event/data`, one
  `team/roster`.
- `{sport}/league/{leagueId}/polls` 404s for leagues without polls (minor
  leagues) — document as absent, don't retry.
- `event/{eventId}/odds` is often empty pre-lines-posting; capture closer to
  kickoff for a populated sample.
- If/when Fox is wired into sdv-py, it becomes a flat-API family (new
  endpoints YAML registered in `FLAT_APIS`, `tools/codegen/generate.py`) —
  same scaffold shape as the NHL/MLB native families, not the ESPN
  leagues.yaml path.
