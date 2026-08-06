# Provider: ESPN

The only provider with a full sdv-py wrapper + parser pipeline (`_common_espn.py`
+ codegen). Every other provider stops at capture + catalog until it earns its
own scaffold phase.

## Hosts / URL families

| Host constant | Base URL | Notes |
|---|---|---|
| `ESPN_SITE` | `https://site.api.espn.com/apis/site/v2/sports` | primary, most wrappers |
| `ESPN_SITE_ALT` | `https://site.web.api.espn.com/apis/site/v2/sports` | alt Site v2 |
| `ESPN_WEB` | `https://web.api.espn.com/apis/v2/sports` | Web v3 |
| `ESPN_CORE` | `https://sports.core.api.espn.com/v2/sports` | Core v2, `$ref`-heavy |
| `ESPN_CORE3` | `https://sports.core.api.espn.com/v3/sports` | Core v3 |
| `ESPN_CDN` | `https://cdn.espn.com/core` | CDN sidecars (e.g. playbyplay) |

Path shape is `{base}/{sport}/{league}/{endpoint}` for Site/Web hosts.

## Id-discovery strategy

Walk the structure — **never** a greedy `re.search(r'\d{6,}', ...)` over a URL
or body (that's how the cricket IPL inner-id bug happened: it matched a nested
team/athlete id instead of the top-level event id).

```python
import requests

def get_event_ids(sport: str, league: str, limit: int = 3) -> list[int]:
    url = f"{ESPN_SITE}/{sport}/{league}/scoreboard"
    r = requests.get(url, params={"limit": limit}, timeout=15)
    r.raise_for_status()
    events = r.json().get("events") or []
    return [int(e["id"]) for e in events if "id" in e]
```

For Core/Web hosts, adapt the key path but always read `["id"]` off the
top-level event/resource object, not a nested one.

## Error-envelope shape

```python
def is_error_envelope(body: dict) -> bool:
    if not isinstance(body, dict):
        return False
    keys = set(body.keys())
    return keys <= {"code", "message", "detail", "name", "error"}
```

Skip and log rather than saving — an error envelope stored as if it were a
real payload silently poisons every downstream returns-doc / fixture built
from it.

## Catalog location

`sdv-internal-refs/espn/`:
- `inputs/sample_bodies/<league>/` — captured bodies
- `tools/espn_capture_league.py <sport> <league> [--ncaa]` — capture helper
- `tools/gen_returns_doc.py espn/inputs/sample_bodies/<league>/` — returns-doc generator

## sdv-py scaffold (leagues.yaml + package dir)

**Working dir:** the sdv-py checkout.

1. Add a row to `tools/codegen/endpoints/leagues.yaml`:

   ```yaml
   - prefix: <prefix>       # e.g. mhockey
     sport: <sport>         # e.g. hockey
     league: <league-slug>  # e.g. mens-college-hockey
     scopes:
       - universal
       # - ncaa        # NCAA-scoped extras
       # - football    # gridiron extras
       # - mlb         # baseball extras
   ```

2. **Pre-create the package dir — codegen does NOT scaffold directories and
   will `FileNotFoundError` if it's missing:**

   ```bash
   PREFIX=<prefix>
   mkdir -p sportsdataverse/$PREFIX
   printf 'from __future__ import annotations\n\nfrom sportsdataverse.%s.%s_espn_ext import *  # noqa: F401,F403\n' \
     "$PREFIX" "$PREFIX" > sportsdataverse/$PREFIX/__init__.py
   ```

3. Regenerate: `uv run python tools/codegen/generate.py` — writes
   `sportsdataverse/<prefix>/<prefix>_espn_ext.py`,
   `tools/codegen/_generated/<prefix>_espn_ext.py`, and `docs/docs/<prefix>/`.

4. Verify wrapper count:

   ```python
   import sportsdataverse.<prefix> as m
   print(sum(1 for k in dir(m) if k.startswith("espn_")))
   ```

   Expected: universal-only ≈ 110, +ncaa ≈ 113, +football ≈ 115, +ncaa+football ≈ 118.

5. Add a gated live test to `tests/test_espn_live.py`:

   ```python
   def test_espn_<prefix>_teams_live():
       from sportsdataverse.<prefix> import espn_<prefix>_teams
       data = espn_<prefix>_teams()
       assert isinstance(data, dict) and len(data) > 0
   ```

   The module-level `pytestmark = skip_if_no_live` gates it automatically.

### Worked example — NCAA Men's Ice Hockey

```yaml
- prefix: mhockey
  sport: hockey
  league: mens-college-hockey
  scopes: [universal, ncaa]
```

```bash
mkdir -p sportsdataverse/mhockey
printf 'from __future__ import annotations\n\nfrom sportsdataverse.mhockey.mhockey_espn_ext import *  # noqa: F401,F403\n' \
  > sportsdataverse/mhockey/__init__.py
uv run python tools/codegen/generate.py
python -c "import sportsdataverse.mhockey as m; print(sum(1 for k in dir(m) if k.startswith('espn_')))"
# expect ~113
uv run python tools/codegen/generate.py --check
```

## Sport-specific parsers (`league_param: true` sports — soccer, cricket, …)

Some sports need per-sport parser overrides instead of the generic
`_common_espn_parsers.py` dispatchers. See the fixtures phase in `SKILL.md`
for the parser contract + TDD flow; the codegen wiring is two entries in
`tools/codegen/generate.py`:

```python
_SPORT_PARSER_OVERRIDES["<sport>"] = {
    "scoreboard": "parse_<sport>_scoreboard",
    "summary":    "parse_<sport>_summary",
}
_SPORT_PARSER_MODULE["<sport>"] = "sportsdataverse.<sport>.<sport>_espn_parsers"
```

**Never import from `_common_espn_parsers` inside a sport parser module** —
circular import. Only `polars`, `pandas`, `typing`, `sportsdataverse.dl_utils`.

## Divergences from sibling providers

- ESPN is the only provider with a codegen scaffold phase today; Fox/CBS/Yahoo
  stop at Part A (capture + catalog) until they're wired into sdv-py.
- ESPN error envelopes use `{"code", "message", ...}`; Fox/CBS use a bare
  `{"error": "..."}` — the two predicates differ (see `sdv-capture-endpoint`
  logic folded into `SKILL.md`'s capture phase).
