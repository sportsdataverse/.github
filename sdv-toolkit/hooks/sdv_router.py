#!/usr/bin/env python3
"""SessionStart router: detect the SDV repo archetype and emit a routing card.

Every other hook in this plugin is reactive -- it fires once a violation is
already in flight. This one briefs on arrival, which is the whole point.

Silent by design outside SDV repos: no archetype means no output, no cost.
"""

import json
import os
import pathlib
import subprocess
import sys

ARCHETYPE_BINDINGS = {
    "sdv-py": "polars 1.x only · codegen output is never hand-edited · returns descriptions "
    "live in manual_column_descriptions.yaml · pin one dtype per join key",
    "raw": "scraping only · commit per-game JSON · keep parallelism low (ESPN Core v2 403s) "
    "· never re-scrape captured games",
    "data": "NN_ stage numbering = intended build order, not run order · idempotent re-runs "
    "· scripts earn scripts/ only via runbook wiring · models need registry rows",
    "r-package": "roxygen @param/@return-table/@examples complete · pkgdown reference coverage "
    "· tibble returns · snake_case",
    "toolkit": "catalog.json is the source of truth · every skill needs a catalog row "
    "· bump plugin.json and mirror before it takes effect",
    "generic-sdv": "branch + PR, never push main · Conventional Commits · no AI co-author trailers",
}

ARCHETYPE_GATES = {
    "sdv-py": "uv run pytest -q  |  CI-green == codegen drift gate only",
    "raw": "uv run pytest -q",
    "data": "uv run pytest -q  |  CI-green == codegen drift gate only",
    "r-package": 'Rscript -e "devtools::check()"',
    "toolkit": "python tools/check_catalog.py .",
    "generic-sdv": "",
}


def git_remote(cwd: pathlib.Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def repo_name(remote: str) -> str:
    if not remote:
        return ""
    tail = remote.rstrip("/").rsplit("/", 1)[-1]
    return tail[:-4] if tail.endswith(".git") else tail


def detect(cwd: pathlib.Path, remote: str):
    """Return the archetype slug, or None when this is not an SDV repo."""
    name = repo_name(remote)
    if (cwd / "tools" / "codegen" / "generate.py").exists():
        return "sdv-py"
    if name.endswith("-raw"):
        return "raw"
    if name.endswith("-data"):
        return "data"
    if (cwd / "DESCRIPTION").exists() and (cwd / "R").is_dir():
        return "r-package"
    if (cwd / ".claude-plugin").is_dir():
        return "toolkit"
    if "sportsdataverse" in remote.lower():
        return "generic-sdv"
    return None


def load_overrides(path: pathlib.Path) -> dict:
    overrides = {}
    if not path.exists():
        return overrides
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            overrides[parts[0].strip()] = parts[1].strip()
    return overrides


def render_card(archetype: str, repo: str, catalog: dict, overrides: dict) -> str:
    entries = catalog.get("entries", [])

    def applies(entry):
        arch = entry.get("archetypes", [])
        return "all" in arch or archetype in arch

    skills = [e["name"] for e in entries if e.get("kind") == "skill" and applies(e)]
    agents = [e["name"] for e in entries if e.get("kind") == "agent" and applies(e)]

    lines = ["SDV ROUTER - archetype: %s  (repo: %s)" % (archetype, repo or "?")]
    binding = ARCHETYPE_BINDINGS.get(archetype, "")
    if binding:
        lines.append("Binding: " + binding)
    if skills:
        lines.append("Skills:  " + " · ".join("/" + s for s in sorted(skills)))
    if agents:
        lines.append(
            "Review:  " + " · ".join(sorted(agents)) + "  (never general-purpose)"
        )
    gate = ARCHETYPE_GATES.get(archetype, "")
    if gate:
        lines.append("Gate:    " + gate)
    lines.append("Index:   /sdv-guide   ·   Found something durable? /sdv-learn")
    note = overrides.get(repo)
    if note:
        lines.append("NOTE:    " + note)
    return "\n".join(lines)


def main() -> int:
    cwd = pathlib.Path(os.getcwd())
    remote = git_remote(cwd)
    archetype = detect(cwd, remote)
    if archetype is None:
        return 0  # silent outside SDV repos

    here = pathlib.Path(__file__).resolve().parent
    catalog_path = here.parent / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception:
        return 0  # never let a broken catalog break session start

    overrides = load_overrides(here / "sdv-overrides.tsv")
    sys.stdout.write(
        render_card(archetype, repo_name(remote), catalog, overrides) + "\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
