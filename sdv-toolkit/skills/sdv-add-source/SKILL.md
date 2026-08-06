---
name: sdv-add-source
description: Use when adding any new league, sport, endpoint, or provider surface to sdv-py — one workflow across every provider (ESPN, Fox Bifrost, CBS NAPI, Yahoo, 247Sports, Torvik). Phases — (1) capture real response bodies with structured id discovery, error-envelope skip, and atomic writes, (2) extend the provider catalog in sdv-internal-refs, (3) generate the col_name/type/description returns doc from the captured payload, (4) scaffold the wrapper — for ESPN that is a leagues.yaml row plus a pre-created package dir and __init__, for a flat API a new endpoints YAML registered in FLAT_APIS, (5) add sport-specific tidy parsers plus fixtures and TDD where the sport needs them, (6) regenerate and verify the codegen drift gate. Invoke for "add an ESPN league", "register a new league", "add a Fox league", "add a CBS league", "add a Yahoo source", "add a 247Sports source", "add a Torvik source", "add a provider", "capture this endpoint", "capture a body", "add a sport parser", "add tidy parsers for this sport", or "scaffold the wrapper for this endpoint".
---

# Add a provider source — one workflow, six phases

This replaced a family of seven near-duplicate skills, one of which
(`sdv-add-provider-source`) was *already* an attempt at this same
consolidation and had **zero** invocations. Merging alone did not fix
discovery — the fix is this skill's description trigger phrases plus the
router that dispatches here. Don't re-fragment this back into
per-provider skills; extend a phase or a `references/*.md` file instead.

Every provider goes through the same six phases; only the mechanics differ,
and those live in `references/{espn,fox,cbs,yahoo,sports247,torvik}.md`.
**Identify the provider first**, read its reference file, then work the
phases below in order.

| Provider | Reference | sdv-py wired today? |
|---|---|---|
| ESPN | `references/espn.md` | yes — full leagues.yaml + parser scaffold |
| Fox Sports (Bifrost) | `references/fox.md` | no — capture + catalog only |
| CBS Sports (NAPI) | `references/cbs.md` | no — capture + catalog only |
| Yahoo Sports | `references/yahoo.md` | no — capture + catalog only |
| 247Sports | `references/sports247.md` | partially — `sports247` / `sports247_site_pages` flat-API stems already ship; check before adding |
| Barttorvik (men's CBB) | `references/torvik.md` | yes — wrappers already live in `sportsdataverse/mbb/`; check before adding |

For a provider not wired into sdv-py yet, phases 1–3 (capture, catalog,
returns-doc) are the whole job — stop there and note the scaffold as
follow-up. Don't invent a wrapper scaffold for a provider whose reference
file says "capture + catalog only."

## Phase menu — jump to the phase that matches the ask

| Entry phrase | Start at |
|---|---|
| "capture this endpoint", "capture a body" | Phase 1 |
| "add a Fox/CBS/Yahoo/247Sports/Torvik source" | Phases 1–3 |
| "extend the provider catalog" | Phase 2 |
| "generate the returns doc" | Phase 3 |
| "add an ESPN league", "register a new league" | Phases 1–4, 6 |
| "add a sport parser", "add tidy parsers for this sport" | Phase 5 |
| "scaffold the wrapper for this endpoint" | Phase 4 |

### Review (mandatory, before shipping)

- **`sdv-python-reviewer`** with lens `parser-contract` for any new/changed
  parser module, lens `http` for any capture/fetch/retry code.
- **`sdv-docs-reviewer`** for the returns doc and any generated reference
  docs the codegen touched.

Do not substitute `general-purpose`.

---

## Phase 1 — Capture

Fetch one representative response body per endpoint and write it to
`<provider>/inputs/sample_bodies/<league>/<host>/<endpoint>.json`. This is
the hardened, provider-agnostic recipe — it avoids two known bugs in naive
capture scripts.

**Working dir:** `sdv-internal-refs` (sibling checkout), unless the
provider's reference file says otherwise.

### 1. Structured id discovery

**Never** parse a URL or body with a greedy `re.search(r'\d{6,}', ...)` —
that matches whatever big number appears first, which can be a nested
team/athlete id instead of the top-level event id (the cricket IPL inner-id
bug). Walk the structure instead; each provider's reference file has the
concrete recipe (ESPN: scoreboard `events[].id`; CBS: the
`/resource/endpoint/registry` self-docs; Yahoo/247Sports: a key-path walk
into the embedded JSON blob; Fox: `leagueId` from the web UI or an existing
scoreboard body; Torvik: no id discovery needed, endpoints are flat).

### 2. Error-envelope skip

Don't store an error response as if it were real data — it silently
poisons every returns-doc and fixture built from it downstream.

```python
def is_error_envelope(body: dict) -> bool:
    """True if the provider returned an error dict, not real data."""
    if not isinstance(body, dict):
        return False
    keys = set(body.keys())
    if keys <= {"code", "message", "detail", "name", "error"}:   # ESPN shape
        return True
    if "error" in keys and len(keys) <= 2:                       # Fox/CBS shape
        return True
    return False
```

For HTML-scrape providers (Yahoo, 247Sports) there is no JSON envelope to
check — the equivalent failure is the extraction regex/selector not
matching. Treat that the same way: skip and log, don't save a partial body.

### 3. Atomic writes

```python
import pathlib, json

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

### Full single-endpoint capture recipe (ESPN shape; adapt hosts per provider)

```python
import requests, pathlib

def capture_endpoint(sport, league, endpoint, params, out_dir, host="site"):
    base = {
        "site": ESPN_SITE, "site_alt": ESPN_SITE_ALT,
        "web": ESPN_WEB,   "core": ESPN_CORE,
    }[host]
    url = f"{base}/{sport}/{league}/{endpoint}"
    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        print(f"SKIP {url} -> HTTP {r.status_code}")
        return None
    body = r.json()
    if is_error_envelope(body):
        print(f"SKIP {url} -> error envelope: {list(body.keys())}")
        return None
    out_path = out_dir / league / host / f"{endpoint}.json"
    atomic_write(out_path, body)
    print(f"OK   {out_path}")
    return out_path
```

**Bound attempts, not saves** — an id-walk without an attempt cap can
404-flood a provider (the CBS incident: 8,400+ wasted requests probing a
torq-gated recruiting resource). If a resource is documented as gated,
stop; don't loop past it hoping for a different response.

Record for every capture: full URL with query params, capture date
(`YYYY-MM-DD`), response status/size. Provider-specific host constants,
auth, and endpoint surfaces are in the matching `references/*.md`.

---

## Phase 2 — Catalog

Each provider directory in `sdv-internal-refs` has a master catalog file
(e.g. `fox/fox_catalog.yaml`, `cbs/cbs_catalog.yaml`, `yahoo/yahoo_catalog.yaml`).
Add an entry for the new sport/league/page following the existing schema —
the exact shape (fields, capture-date convention, fragility flag) is in the
provider's reference file. ESPN doesn't use this catalog shape; its capture
tooling (`espn_capture_league.py`) and returns-doc generator are
self-contained (see `references/espn.md`).

---

## Phase 3 — Returns doc

Generate a `col_name | type | description` returns table from the captured
payload — this is what downstream consumers (a scaffolded wrapper, a
parser, a model) read instead of re-deriving the shape from a raw body.

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
...

**Divergence notes:** <shape differences vs. sibling endpoints/leagues for this provider>
```

For ESPN, `espn/tools/gen_returns_doc.py <sample_bodies_dir>` generates a
first pass from the captured bodies directly — start there instead of
hand-writing the table. Always fill in **Divergence notes** — this is the
single place per-provider parser/scaffold decisions get made from later.

If sdv-py already has a `returns_schema` structure for this endpoint's
family (see `sportsdataverse/CLAUDE.md` "Returns-table descriptions"), the
column descriptions belong in `manual_column_descriptions.yaml`, never in a
`schemas/**.yaml` file — those get clobbered on re-capture.

---

## Phase 4 — Scaffold the wrapper

This phase only applies once a provider is wired into sdv-py. Two shapes:

**ESPN** — a `leagues.yaml` row plus a pre-created package directory and
`__init__.py`, then `uv run python tools/codegen/generate.py`. Codegen does
**not** scaffold directories — it `FileNotFoundError`s if the package dir
doesn't exist first. Full steps, the leagues.yaml schema, and a worked
example (NCAA Men's Ice Hockey) are in `references/espn.md`.

**Flat API** (NHL api-web/edge/stats-rest, MLB Stats API, `sports247`,
`on3`, and any future Fox/CBS surface once wired) — a new
`tools/codegen/endpoints/<stem>.yaml`, registered as a
`(yaml_stem, league_prefix)` tuple in `FLAT_APIS`
(`tools/codegen/generate.py`). Each flat-API YAML gets its own parser
module and its own reference-docs grouping on the league index; an
authenticated family additionally needs `auth: true` + `getter_module:` in
the YAML (see the NFL.com `nfl_api` family for the pattern).

If the provider isn't wired yet (Fox, CBS, Yahoo today), stop after Phase 3
and note the scaffold as explicit follow-up rather than inventing one.

---

## Phase 5 — Fixtures: sport-specific parsers + TDD

Applies whenever a sport needs tidy polars/pandas parsers beyond the
generic ESPN dispatchers — the `league_param: true` sports (soccer, cricket)
and any sport needing per-sport parser overrides.

### Parser contract (universal across every parser module in sdv-py)

- Return `polars.DataFrame` by default; pandas via `return_as_pandas=True`.
- Empty/malformed payloads → zero-row frame with the documented schema.
  Never raise.
- Output columns snake-cased via `sportsdataverse.dl_utils.underscore`.
- `pandas.json_normalize` for nested flattening, convert to polars at the
  end; stringify list-valued cells so polars accepts the frame.
- **Never import from `_common_espn_parsers`** — circular import. A sport
  parser module imports only `polars`, `pandas`, `typing`, and
  `sportsdataverse.dl_utils`.

### Steps

1. **Create the parser module** `sportsdataverse/<sport>/<sport>_espn_parsers.py`
   — one `parse_<sport>_<short>` function per endpoint short name, plus a
   `parse_<sport>_summary(payload, section=None, ...)` dispatcher for
   multi-section endpoints (one `_parse_summary_<section>` private helper
   per section).
2. **Register in codegen** — `tools/codegen/generate.py`:

   ```python
   _SPORT_PARSER_OVERRIDES["<sport>"] = {
       "scoreboard": "parse_<sport>_scoreboard",
       "summary":    "parse_<sport>_summary",
   }
   _SPORT_PARSER_MODULE["<sport>"] = "sportsdataverse.<sport>.<sport>_espn_parsers"
   ```

   The `sport_parser_imports` codegen block picks these up and routes
   `return_parsed=True` calls through them. Do not re-export from
   `_common_espn_parsers.py`.
3. **Drop fixtures** in `tests/fixtures/espn/<sport>/<league>/<endpoint>.json`
   (captured via Phase 1's tooling), with a `README.md` per directory
   documenting URL + capture date.
4. **Write failing tests first** (`tests/test_espn_<sport>_parsers.py`) —
   column presence, empty-payload zero-row behavior, and the
   `return_as_pandas=True` path. Run to confirm the right failure (not an
   import error), implement the parser, re-run to green.

---

## Phase 6 — Drift gate

```bash
uv run python tools/codegen/generate.py
uv run python tools/codegen/generate.py --check
uv run pytest tests/codegen/ tests/test_espn_<sport>_parsers.py -q
```

Both the regenerate and `--check` must pass cleanly before committing — a
change that touched endpoint YAML, schemas, docstrings, loaders, or
wrappers leaves the generated `docs/docs/` reference subtree stale until
regenerated, and CI's drift gate + the `sdv-codegen` pre-commit hook both
enforce it.

For ESPN, also add a gated live test (`tests/test_espn_live.py`, guarded by
the module-level `pytestmark = skip_if_no_live`) and run it:

```bash
SDV_PY_LIVE_TESTS=1 uv run pytest -k "<prefix>" -v
```

---

## Commit convention

```
feat(<provider>): add <sport/league> capture + catalog
feat(<prefix>): register <provider> <league> league family (~NNN wrappers)
feat(<sport>): add ESPN <sport> tidy parsers (scoreboard, summary dispatcher)
```

No `Co-Authored-By` trailers. Conventional Commits format only.

## See also

- `references/{espn,fox,cbs,yahoo,sports247,torvik}.md` — per-provider
  hosts, id-discovery strategy, error-envelope shape, catalog schema, and
  divergence notes.
- `sdv-python-reviewer` (agent, lenses `parser-contract` / `http`) — dispatch
  in Review, before shipping.
- `sdv-docs-reviewer` (agent) — dispatch in Review for the returns doc +
  generated reference docs.
- `/sdv-regen-docs`, `/sdv-ship` — hand off once the drift gate is green.
