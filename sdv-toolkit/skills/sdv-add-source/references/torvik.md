# Provider: Barttorvik (men's college basketball)

The simplest provider in the routing table: clean CSV/JSON endpoints, no
auth, no HTML scrape. A Torvik-backed wrapper surface **already exists** in
`sportsdataverse/mbb/` — check it before adding a new one.

## Host / URL family

| Property | Value |
|---|---|
| Base URL | `https://barttorvik.com/` |
| Auth | none |
| Format | `<endpoint>.json?...` or `<endpoint>.csv?...` per endpoint |

## Id-discovery strategy

N/A — Barttorvik endpoints are flat, parameterized by query string (season,
team, etc.), not by an id you have to discover from a scoreboard walk.

## Error-envelope shape

N/A — a bad request returns a non-200 or an unexpected content-type; there is
no JSON error envelope to special-case. Treat a non-200 or a response that
fails to parse as CSV/JSON the same way the capture phase treats any other
skip: log and don't save.

## Catalog location

`sdv-internal-refs/barttorvik/inputs/sample_bodies/<endpoint>.json` — the
barttorvik catalog there maps the known endpoints.

## Scaffold notes

For new endpoints, follow the sdv-py single-table module pattern:
`espn_<league>_<dataset>(...)` returning `pl.DataFrame` — despite the `espn_`
naming convention on other providers' functions in `mbb/`, Torvik-backed
functions live alongside them; match the existing file's naming rather than
inventing a `torvik_` prefix unless the existing surface already uses one.

## Divergences / gotchas

- No auth and no rate-limit concerns reported so far — still capture with a
  date stamp since Torvik's own ratings methodology can revise mid-season.
- Confirm against the live existing `sportsdataverse/mbb/` surface before
  writing a new wrapper — Torvik coverage here predates this skill and may
  already answer the ask.
