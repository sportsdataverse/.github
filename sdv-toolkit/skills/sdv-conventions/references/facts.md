# Facts come from lookups — detail

The rules live in `SKILL.md` § "Facts come from lookups". This file holds the
fact classes, the lookup order per class, the exemptions, and the incidents.

## Fact classes

A **checkable SDV fact** is a token of one of these classes, stated as true about
an SDV repo. Opinions, plans, future tense ("we will add X") and facts about
third-party systems that SDV does not wrap are out of scope.

| Class | Examples | Resolves against |
|---|---|---|
| F1 function / export | `cfbd_game_info()`, `load_mlb_pbp` | Python `__all__` and module defs; R `NAMESPACE` exports plus `R/*.R` definitions |
| F2 column + dtype | `rushing_fumbles_lost`, `key_mlbam: Int64` | `tools/codegen/schemas/loader_schemas.yaml` and the rest of `tools/codegen/schemas/**`, a returns table, a captured payload |
| F3 endpoint + params | `scoreboard?dates=YYYYMMDD` | `tools/codegen/endpoints/*.yaml`, a capture, or one live probe |
| F4 release asset / tag | `mlb_game_state/mlb_re24_matrix_2024.parquet` | `tools/codegen/endpoints/releases.yaml`; `gh release view <tag>` |
| F5 path / test / script | `tests/codegen/test_league_registry.py` | `git cat-file -e origin/main:<path>` (set `MSYS_NO_PATHCONV=1` in Git Bash) |
| F6 env var / CLI flag | `SDV_PY_NBA_STATS_LIVE`, `--check` | a grep of the source; `--help` |

## Lookup order and citation

1. **sdv-docs MCP** (`plugin:sdv-toolkit:sdv-docs`): the indexed docs, schemas and
   registries.
2. **Repo source at `origin/main`**: `git show origin/main:<path>`, `git grep -n <token>
   origin/main`. A local checkout's working tree is not `origin/main`; fetch first.
3. **A captured payload**: the provider capture store or a test fixture.
4. **One live probe**: one call, its HTTP status written down. Never a crawl; never
   stats.nba.com, stats.wnba.com, stats.ncaa.org or Sports Reference from a
   datacenter host.

Cite where it resolved, inline: `R/cfbd_api_key.R:8`, `_PLAYER_STATS_SCHEMA` in
`sportsdataverse/nfl/nfl_loaders.py`, "probe 2026-11-26: 400". Leave the citation implicit only when
the same diff defines the fact (you are adding the function you document).

**A miss is a finding.** Write `not indexed` and give the close matches (`git grep`
for the stem, `difflib`-style near names). Never fall back to the spelling you
remember: that is exactly how a nonexistent helper reached a roxygen bullet, a
CLAUDE.md and a copilot-instructions file in one package.

## Degraded mode (sdv-docs unreachable)

When the MCP fails to connect (the session banner lists it under "failed to
connect", or a call errors), say so **once** in the session, then keep resolving
through steps 2-4. Every fact still unchecked when you write it carries
`[unverified: from memory]` until a later step resolves it. A durable surface (repo
file, PR body, ledger, register row, spec) should not ship with that label: resolve
the fact or drop the sentence.

The SessionStart router prints a degraded line when it can tell, without network,
that the server cannot start: the plugin's `.mcp.json` has no `sdv-docs` entry, or
its command (`uvx`) is not on `PATH`. A server that starts and then fails (a package
resolution error, a crash, a cached connection failure) is invisible to the hook, so
the session banner stays the signal for those.

## Exemptions (what is not a claim)

- **Future tense / plans**: "will add", "planned", "proposed", "TODO", "is adding",
  "once #123 lands". A spec naming a function it intends to write is not wrong.
- **Negation / history**: "does not exist", "not on main", "removed", "renamed",
  "replaced", "instead of", "no longer", "previously", "earlier versions". The
  absence phrase may sit in the next sentence ("…adds `tests/x.py`. That file does
  not exist on main.").
- **History files**: `NEWS.md`, `CHANGELOG.md` and frozen versioned docs record what
  was true then. Check only the lines a change adds.
- **Foreign names**: a name qualified with another package (`dplyr::filter`,
  `pl.col`) or attributed in prose ("hoopR's `load_nba_pbp()`"). Unqualified foreign
  names in repo docs should be qualified; that is a style fix, not a wrong fact.
- **Generated surfaces**: `man/`, pkgdown `docs/`, `*_espn_ext.py`,
  `docs/docs/**/reference/`. Codegen gates own them; fix the source instead.
- **Placeholders and hidden text**: `R/pbp_xyz.R`, `cfbd_new_endpoint()`, and
  markdown inside `<!-- -->` (template instructions).
- **Planning notes** (`*proposal*`, `*audit*`, `*plan*`, `*spec*` files) get the
  L2 read, not the script, except on lines a change adds.

## Mechanical checks

`tools/check_claims.py` in the toolkit (stdlib only; report-only):

| Test | Class | What it does |
|---|---|---|
| T1 | F1 | call-shaped names in docs-like text (backticked `name(`, `pkg::name`, roxygen `[name()]`, calls in `r`/`python`/untagged fences and `@examples`) against `NAMESPACE`, R definitions, Python defs and `__all__`, base R, builtins and the DESCRIPTION dependencies |
| T2 | F5 | repo-relative paths whose first part is a top-level entry, against `git cat-file --batch-check <ref>:<path>` |

```sh
python <toolkit>/tools/check_claims.py --repo . --ref origin/main          # whole files
python <toolkit>/tools/check_claims.py --repo . --diff origin/main         # added lines only
```

It exits 0 unless `--strict` is passed. It is not wired into any pre-commit or CI:
it goes blocking only after a week of report-only runs measures at least 90% of its
findings as real.

## Incidents

| Claim | What was true |
|---|---|
| a roxygen bullet and CLAUDE.md told users to call a key-registration helper | no file defined it; three sibling helpers did exist (T1) |
| an issue template asked reporters to run a team-names helper | `NAMESPACE` lacked it, so every reporter got "could not find function" (T1) |
| a column list in a projection helper named `fumbles_lost` | the input schema emits only the three per-play-type variants, so fumbles never reached scoring: a silent no-op (F2; not yet mechanical) |
| "the scoreboard docstring advertises date ranges" | the docstring already said ranges get HTTP 400; a live probe agreed. The false report came from memory of a probe, not from the file (rule 1) |
| the docs MCP failed to connect and nothing said to label unchecked facts | degraded mode |
