#!/usr/bin/env python3
"""Gather the review context for one pull request into a single file.

Usage:
    python3 pr_context.py <N | owner/repo#N | PR URL> [-R owner/repo] [--out DIR]

Writes <out>/<repo>-<N>/{context.md,context.json,diff.patch} and prints the
context.md path. Read-only: it only calls `gh` read endpoints.

Everything under "Signals" is a LEAD, not a finding. Each regex below exists
because the pattern shipped a real defect at least once (the rule id points at
the reference file entry); a match still has to be confirmed by reading the
code at the PR head.

Stdlib only, so it runs from any repo's interpreter or bare python3.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import asdict, dataclass

IN_SCOPE_OWNERS = {"sportsdataverse", "saiemgilani"}

# Repos whose conventions belong to an outside maintainer: review them against
# THEIR CONTRIBUTING, not SDV house rules (uv, polars, codegen).
MAINTAINER_OWNED = {"sportyR", "sportypy", "cfb4th", "mlbplotR", "baseballr"}

PLATFORM_REPOS = {
    "sdv-db",
    "sdv-orch",
    "sdv-swagger",
    "sdv-internal-refs",
    "sportsdataverse-web",
    "sdv-next-clone",
    "universe",
    "bin",
}
TOOLKIT_REPOS = {".github", "dotfiles"}
RESEARCH_REPOS = {"Sports-Research-Papers", "ClaudeCowork"}

REFERENCES = {
    "universal": "references/universal.md",
    "python-package": "references/python-package.md",
    "r-package": "references/r-package.md",
    "raw": "references/producers.md",
    "data": "references/producers.md",
    "models": "references/producers.md",
    "platform": "references/platform.md",
    "web-gop": "references/web-gop.md",
    "js-package": "references/other-repos.md",
    "research-docs": "references/other-repos.md",
    "toolkit": "references/other-repos.md",
    "maintainer-owned": "references/other-repos.md",
    "python-generic": "references/universal.md",
}

BOT_LOGIN = re.compile(r"(?i)coderabbit|copilot|sourcery")
AI_TRAILER = re.compile(
    r"(?i)co-authored-by:.*(claude|copilot|gpt|gemini|cursor)|generated with \[?claude"
)


# --------------------------------------------------------------------------- #
# PR reference parsing
# --------------------------------------------------------------------------- #


def parse_pr_ref(ref, repo_flag=None):
    """Return (owner/repo, number) from a number, owner/repo#N, or a PR URL."""
    ref = ref.strip()
    m = re.match(r"^https?://github\.com/([^/]+/[^/]+)/pull/(\d+)", ref)
    if m:
        return m.group(1), int(m.group(2))
    m = re.match(r"^([\w.-]+/[\w.-]+)#(\d+)$", ref)
    if m:
        return m.group(1), int(m.group(2))
    if ref.isdigit():
        if not repo_flag:
            raise ValueError("a bare PR number needs -R owner/repo")
        return repo_flag, int(ref)
    raise ValueError("unrecognised PR reference: %r" % ref)


# --------------------------------------------------------------------------- #
# Archetype classification
# --------------------------------------------------------------------------- #


def repo_archetypes(owner, name, is_fork=False, root_names=()):
    """Default archetypes for the repository as a whole."""
    roots = set(root_names)
    if is_fork or owner not in IN_SCOPE_OWNERS:
        return ["out-of-scope"]
    if name in MAINTAINER_OWNED:
        return ["maintainer-owned"]
    if name == "sportsdataverse-py" or name == "sdv-py":
        return ["python-package"]
    if name == "game-on-paper-app":
        return ["web-gop"]
    if name == "sportsdataverse-data":
        # R package + release-note generator; the -data suffix misleads.
        return ["r-package", "platform"]
    if name in PLATFORM_REPOS:
        return ["platform"]
    if name in TOOLKIT_REPOS or ".claude-plugin" in roots:
        return ["toolkit"]
    if name in RESEARCH_REPOS or "_quarto.yml" in roots:
        return ["research-docs"]
    if name.endswith("-raw"):
        return ["raw"]
    if name.endswith("-data"):
        return ["data"]
    if name.endswith("-models") or name in {"sdvmodels", "sdv-engine"}:
        return ["models"]
    if {"DESCRIPTION", "NAMESPACE"} <= roots:
        return ["r-package"]
    if "package.json" in roots:
        return ["js-package"]
    if roots & {"pyproject.toml", "setup.py"}:
        return ["python-generic"]
    return []


_PATH_RULES = [
    (re.compile(r"(^|/)\.github/workflows/"), "gha"),
    (
        re.compile(
            r"(^|/)(R/[^/]+\.R|man/[^/]+\.Rd|NAMESPACE|DESCRIPTION|_pkgdown\.yml|vignettes/)"
        ),
        "r-package",
    ),
    (
        re.compile(
            r"(\.ubj|\.card\.json|(^|/)models/REGISTRY\.md|model_training/|_model_publish/|_model_build/)"
        ),
        "models",
    ),
    (
        re.compile(r"(^|/)tools/codegen/|_espn_ext\.py$|(^|/)sportsdataverse/"),
        "python-package",
    ),
    (
        re.compile(
            r"(^|/)astro/|(^|/)python/(app|gop_routes|span_box|paper_index|dq|espn_proxy)\.py$"
        ),
        "web-gop",
    ),
    (re.compile(r"(\.sql$|(^|/)migrations?/|(^|/)infra/postgresql/)"), "sql"),
    (
        re.compile(r"(^|/)(Dockerfile|docker-compose[^/]*\.ya?ml)$|(^|/)systemd/"),
        "deploy",
    ),
    (re.compile(r"\.(qmd|Rmd)$"), "docs"),
    (
        re.compile(
            r"(^|/)(skills/[^/]+/SKILL\.md|agents/[^/]+\.md|hooks/hooks\.json|catalog\.json)$"
        ),
        "toolkit",
    ),
]


def classify_path(path):
    """Tags for one changed path (a PR can span several archetypes)."""
    return sorted({tag for rx, tag in _PATH_RULES if rx.search(path)})


def references_for(archetypes):
    """Ordered, de-duplicated reference files to load for these archetypes."""
    out = [REFERENCES["universal"]]
    for a in archetypes:
        ref = REFERENCES.get(a)
        if ref and ref not in out:
            out.append(ref)
    return out


# --------------------------------------------------------------------------- #
# Diff signals -- leads only, each tied to a reference rule id
# --------------------------------------------------------------------------- #


@dataclass
class Signal:
    rule: str
    path: str
    line: int
    note: str
    text: str


# (rule id, compiled regex over an ADDED line, path filter regex or None, note)
LINE_SIGNALS = [
    ("U-GIT-1", re.compile(r"^(<{7}|>{7})( |$)"), None, "merge conflict marker"),
    ("U-GIT-4", AI_TRAILER, None, "AI attribution trailer/footer"),
    (
        "U-SEC-1",
        re.compile(
            r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{20,}\.eyJ)"
        ),
        None,
        "credential-shaped literal",
    ),
    (
        "U-FAIL-1",
        re.compile(r"git (push|commit)\b[^#\n]*\|\|\s*(true|echo|:)"),
        None,
        "git push/commit failure masked",
    ),
    (
        "U-FAIL-1",
        re.compile(r"set -uo pipefail\s*$"),
        re.compile(r"\.(sh|ya?ml)$"),
        "pipefail without -e",
    ),
    (
        "U-FAIL-1",
        re.compile(
            r"^\s*except\s*(Exception|BaseException)?\s*:\s*(pass|continue|return\b.*)?\s*$"
        ),
        re.compile(r"\.py$"),
        "broad except -- what does the failure branch return?",
    ),
    (
        "U-FAIL-6",
        re.compile(r"range\(\s*1\s*,\s*[A-Za-z_][\w.]*\s*\+\s*1\s*\)"),
        re.compile(r"\.py$"),
        "retry loop from an env/config count -- validate >= 1",
    ),
    (
        "U-DATA-1",
        re.compile(
            r"\b(season|year|yr|end_year|start_year)\w*\s*[+-]\s*1\b|\{season\s*[+-]\s*1\}"
        ),
        None,
        "season shift -- convention applied exactly once?",
    ),
    (
        "U-DATA-1",
        re.compile(r"\$\(\(\s*\w+\s*[+-]\s*1\s*\)\)"),
        re.compile(r"\.(sh|ya?ml)$"),
        "shell arithmetic +/-1 -- if this is a season, which convention does each caller pass?",
    ),
    (
        "U-DATA-2",
        re.compile(r"_id\b.*strict\s*=\s*False|strict\s*=\s*False.*_id\b"),
        re.compile(r"\.py$"),
        "non-strict cast on an id",
    ),
    (
        "U-CI-2",
        re.compile(
            r"\$\{\{\s*(github\.event\.(inputs|client_payload|pull_request\.(title|body|head\.ref)|issue\.(title|body)|comment\.body)|inputs\.)"
        ),
        re.compile(r"(^|/)\.github/workflows/"),
        "untrusted expression -- must reach run: only via env:",
    ),
    (
        "U-CI-3",
        re.compile(r"secrets\.\w+\s*\|\|\s*secrets\.GITHUB_TOKEN"),
        re.compile(r"(^|/)\.github/workflows/"),
        "GITHUB_TOKEN fallback (403s cross-repo after the build)",
    ),
    (
        "U-CI-5",
        re.compile(r"pull_request_target|runs-on:.*self-hosted"),
        re.compile(r"(^|/)\.github/workflows/"),
        "fork-triggerable event or self-hosted (production) runner",
    ),
    (
        "DATA-2",
        re.compile(r"grep -o -E '\[0-9\]\+'"),
        re.compile(r"(^|/)\.github/workflows/"),
        "permissive year regex over a commit message",
    ),
    (
        "U-PATH",
        re.compile(r"(C:[\\/]+Users[\\/]|/Users/[a-z]|~/Documents/)"),
        None,
        "machine-specific path",
    ),
    (
        "RAW-4",
        re.compile(r"(ProcessPoolExecutor|\bPool)\((?![^)]*spawn)"),
        re.compile(r"\.py$"),
        "process pool -- spawn context if polars is imported",
    ),
    (
        "PLAT-ORCH-1",
        re.compile(r"(^|[\s;&|(])uv run\b"),
        re.compile(r"(^|/)(scripts/.*\.sh|systemd/.*|.*registry\.py)$"),
        "bare `uv run` under systemd/cron PATH exits 127",
    ),
    (
        "PLAT-DB-9",
        re.compile(r"/opt/sdv-db|psql\s+-U\s+postgres|0\.0\.0\.0/0|\btrust\s*$"),
        None,
        "droplet path/auth anti-pattern",
    ),
    (
        "PLAT-WEB-3",
        re.compile(r"NEXT_PUBLIC_\w*(KEY|TOKEN|SECRET)"),
        None,
        "server credential exposed to the client bundle",
    ),
    (
        "GOP-CACHE-1",
        re.compile(r"Astro\.cache\.set\(\s*false\s*\)"),
        None,
        "set(false) emits no header -- needs Cache-Control: no-store",
    ),
    (
        "GOP-ROUTE-1",
        re.compile(r"Astro\.(redirect|rewrite)\("),
        re.compile(r"(^|/)components/.*\.astro$"),
        "redirect/rewrite inside a component ships an empty 200",
    ),
    (
        "GOP-LEAGUE-1",
        re.compile(r"teamlogos/ncaa/"),
        re.compile(r"(^|/)astro/"),
        "hard-coded college logo path",
    ),
    (
        "GOP-WORKER-1",
        re.compile(r"runtime\.ctx|redirect:\s*['\"]error['\"]"),
        re.compile(r"(^|/)astro/"),
        "invalid on Cloudflare adapter v14 / workerd",
    ),
    (
        "GOP-ROUTE-5",
        re.compile(r"<script[^>]*\bis:inline"),
        re.compile(r"\.astro$"),
        "is:inline script runs where placed",
    ),
    (
        "R-3",
        re.compile(r"pak::pak\("),
        re.compile(r"(^|/)vignettes/"),
        "vignette installs packages -- never the package itself",
    ),
    (
        "R-5",
        re.compile(r"\bgh::|gh_cli\("),
        re.compile(r"(^|/)vignettes/"),
        "vignette needs GITHUB_PAT -- gate on nzchar()",
    ),
    (
        "PROD-REBASE",
        re.compile(r"git pull --rebase"),
        None,
        "am backend stalls on binary repos -- git rebase --merge",
    ),
]


def parse_diff(diff_text):
    """Yield (path, new_line_number, added_text) for every added line."""
    path, new_ln = None, 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            p = raw[4:].strip()
            path = None if p == "/dev/null" else re.sub(r"^b/", "", p)
            continue
        if raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            new_ln = int(m.group(1)) if m else 0
            continue
        if path is None or raw.startswith("--- "):
            continue
        if raw.startswith("+"):
            yield path, new_ln, raw[1:]
            new_ln += 1
        elif raw.startswith(" "):
            new_ln += 1


# A comment that mentions a pattern is not the pattern. Credentials, conflict
# markers and attribution trailers are real wherever they appear, so they are
# scanned even on comment lines.
COMMENT_LINE = re.compile(r"^\s*(#(?!!)|//|/\*|\*\s|<!--|--\s)")
SCAN_COMMENTS_TOO = {"U-SEC-1", "U-GIT-1", "U-GIT-4"}


def scan_diff(diff_text, repo_name=None):
    """Line signals for every added line of a unified diff (comments skip non-security rules)."""
    signals = []
    for path, ln, text in parse_diff(diff_text):
        is_comment = bool(COMMENT_LINE.match(text))
        for rule, rx, path_rx, note in LINE_SIGNALS:
            if path_rx is not None and not path_rx.search(path):
                continue
            if is_comment and rule not in SCAN_COMMENTS_TOO:
                continue
            # R-3 is about a vignette installing the package ITSELF; other pak
            # installs are fine (cfbfastR#154 removed exactly the self-installs).
            if rule == "R-3" and not (
                repo_name and re.search(r"[\"']%s[\"']" % re.escape(repo_name), text)
            ):
                continue
            if rx.search(text):
                signals.append(Signal(rule, path, ln, note, text.strip()[:160]))
    return signals


# --------------------------------------------------------------------------- #
# Callers of changed entry points (a callee fixed for one caller breaks others)
# --------------------------------------------------------------------------- #

ENTRY_POINT = re.compile(
    r"^(scripts/.+\.(sh|py|R)|python/[^/]+\.py|ops/.+\.(sh|py)|R/[^/]+_creation\.R)$"
)


def gone_paths(files):
    """Paths that no longer exist at the head: deletions and the old side of renames."""
    gone = set()
    for f in files:
        if f.get("status") == "removed":
            gone.add(f["filename"])
        if f.get("previous_filename"):
            gone.add(f["previous_filename"])
    return gone


def _touched_paths(files):
    """Every path a caller might still reference: head names plus renamed-from names."""
    for f in files:
        yield f["filename"]
        if f.get("previous_filename"):
            yield f["previous_filename"]


def caller_candidates(files):
    """Basenames of changed entry points worth a caller search.

    Deleted entry points and the old names of renamed ones are included on purpose:
    a surviving caller of a name that is gone is exactly the dangling reference.
    """
    out = []
    for name in _touched_paths(files):
        if not ENTRY_POINT.match(name):
            continue
        base = pathlib.PurePosixPath(name).name
        if base not in out:
            out.append(base)
    return out


def module_name(path):
    """`python/nhl_data_build/season.py` -> `nhl_data_build.season` (None if not .py)."""
    if not path.endswith(".py"):
        return None
    p = re.sub(r"^(python|src)/", "", path)[: -len(".py")]
    p = re.sub(r"/(__init__|__main__)$", "", p)
    return p.replace("/", ".") if p and "-" not in p else None


def module_candidates(files):
    """Dotted module names of changed Python files (incl. deleted/renamed-from names)."""
    out = []
    for name in _touched_paths(files):
        mod = module_name(name)
        if mod and re.match(r"^(python|src)/", name) and mod not in out:
            out.append(mod)
    return out


def _git(local, *args, timeout=120):
    """Run a read-only git command; stdout on success, None on failure or timeout.

    `git grep` exits 1 when nothing matches -- that is a successful empty search.
    """
    try:
        p = subprocess.run(
            ["git", "-C", str(local), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode == 0 or (args[:1] == ("grep",) and p.returncode == 1):
        return p.stdout
    return None


# Any interpreter-ish token: `python3`, `uv run python`, `"${PYBIN}"`, `$PY`.
MODULE_REF = re.compile(
    r"(?i)(?:python[0-9.]*|\$\{?\w*py\w*\}?\"?)\s+(?:-[A-Za-z]+\s+)*-m\s+([A-Za-z_][\w.]*)"
)


def dangling_module_refs(ref_lines, tree_paths):
    """`python -m X` references (in workflows/scripts) whose X is not in the tree.

    Only names sharing a local module prefix (first two `_` tokens, e.g. `nhl_data`)
    are judged, so `python -m pytest` / `http.server` are never flagged.
    """
    local = {m for m in (module_name(p) for p in tree_paths) if m}
    prefixes = {
        "_".join(m.split(".")[0].split("_")[:2])
        for m in local
        if "_" in m.split(".")[0]
    }
    out = []
    for loc, text in ref_lines:
        for mod in MODULE_REF.findall(text):
            top = mod.split(".")[0]
            if "_".join(top.split("_")[:2]) in prefixes and mod not in local:
                out.append({"module": mod, "where": loc, "text": text.strip()[:160]})
    return out


def local_module_refs(repo_name, base_ref, files, diff_text, sdv_root="/mnt/sdv_repos"):
    """Dangling `-m` targets at (origin/<base> + this PR's file changes). Leads only."""
    local = pathlib.Path(sdv_root) / repo_name
    if not (local / ".git").exists():
        return None
    ref = "origin/%s" % base_ref
    tree = _git(local, "ls-tree", "-r", "--name-only", ref)
    grep = _git(
        local,
        "grep",
        "-n",
        "-E",
        r"[Pp][Yy][^ ]* .*-m ",
        ref,
        "--",
        ".github/workflows",
        "scripts",
        "ops",
        timeout=60,
    )
    if tree is None or grep is None:
        return None  # ref missing/unfetched or git failed: "not checked", never "none"
    paths = (set(tree.splitlines()) - gone_paths(files)) | {
        f["filename"] for f in files if f.get("status") != "removed"
    }
    changed = set(_touched_paths(files))
    grep = grep.splitlines()
    lines = []
    for g in grep:
        parts = g[len(ref) + 1 :].split(":", 2)
        if (
            len(parts) == 3 and parts[0] not in changed
        ):  # changed files: use the PR's lines
            lines.append(("%s:%s" % (parts[0], parts[1]), parts[2]))
    for path, ln, text in parse_diff(diff_text):
        if re.search(r"(^|/)(\.github/workflows|scripts|ops)/", path):
            lines.append(("%s:%d (this PR)" % (path, ln), text))
    return dangling_module_refs(lines, paths)


def find_callers(
    repo_name, base_ref, candidates, sdv_root="/mnt/sdv_repos", changed=(), modules=()
):
    """Best-effort, read-only caller search in local checkouts. Leads only.

    Searches origin/<base> (the callers that exist before this PR). Hits inside files
    the PR changes are skipped -- those are already in the diff. `modules` are dotted
    names, also searched under python/ so `-m pkg.mod` and imports are found.

    Returns (hits, unchecked): `unchecked` names why the repo search could not run
    (no checkout, missing base ref, git failure) so the report never reads an
    unrun search as "no callers".
    """
    hits = {}
    unchecked = None
    changed = set(changed)
    local = pathlib.Path(sdv_root) / repo_name
    orch = pathlib.Path(sdv_root) / "sdv-orch" / "sdv_orch" / "registry.py"
    ref = "origin/%s" % base_ref
    if not (local / ".git").exists():
        unchecked = "no local checkout at %s" % local
    elif _git(local, "rev-parse", "--verify", "--quiet", ref + "^{commit}") is None:
        unchecked = "%s is not available in %s (fetch it)" % (ref, local)
    terms = [(c, False) for c in candidates[:25]] + [(m, True) for m in modules[:25]]
    for base, is_module in terms:
        found = []
        if unchecked is None:
            where = [".github/workflows", "scripts", "ops", "RUNBOOK.md", "CLAUDE.md"]
            if is_module:
                where.append("python")
            out = _git(local, "grep", "-n", "-F", base, ref, "--", *where, timeout=60)
            if out is None:
                unchecked = "git grep failed in %s" % local
                out = ""
            for line in out.splitlines():
                parts = line[len(ref) + 1 :].split(":", 2)
                path = parts[0]
                if path in changed or path.endswith("/" + base) or path == base:
                    continue
                if is_module and module_name(path) == base:
                    continue
                found.append(line[len(ref) + 1 :][:200])
        if orch.exists():
            for i, text in enumerate(orch.read_text(encoding="utf-8").splitlines(), 1):
                if base in text:
                    found.append(
                        "sdv-orch/sdv_orch/registry.py:%d:%s" % (i, text.strip()[:160])
                    )
        if found:
            hits[base] = found[:12]
    return hits, unchecked


# --------------------------------------------------------------------------- #
# File-list signals
# --------------------------------------------------------------------------- #

GENERATED = re.compile(
    r"(_espn_ext\.py$|(^|/)sportsdataverse/parsed/|(^|/)docs/docs/[^/]+/reference/|"
    r"(^|/)src/generated/|(^|/)api/generated/|(^|/)docs/sdv-data-api\.openapi\.json$)"
)
CODEGEN_INPUT = re.compile(
    r"(^|/)tools/codegen/(endpoints|schemas|templates)/|manual_column_descriptions\.yaml$"
)
# Anything a generator legitimately reads: sdv-py docs regenerate from public
# docstrings; sdv-db's API/OpenAPI regenerate from the captured schema snapshot.
GENERATOR_SOURCE = re.compile(
    r"(^|/)tools/codegen/|manual_column_descriptions\.yaml$|schema_snapshot\.json$|"
    r"(^|/)scripts/(gen_api|capture_schema)\.py$|(^|/)tools/codegen/generate\.mjs$"
)
DATA_FILE = re.compile(r"\.(parquet|rds|json|csv|html|gz)$")


def file_signals(files, repo_name=""):
    """`files` is a list of {"filename": str, "status": str} (REST shape)."""
    names = [f["filename"] for f in files]
    nameset = set(names)
    out = []

    def add(rule, note, paths=()):
        out.append({"rule": rule, "note": note, "paths": list(paths)[:15]})

    deleted = [f["filename"] for f in files if f.get("status") == "removed"]
    if deleted:
        add(
            "U-GIT-2",
            "%d deleted file(s) -- each must be announced in the PR body"
            % len(deleted),
            deleted,
        )

    def changed(rx):
        return [n for n in names if re.search(rx, n)]

    if "uv.lock" in nameset and "pyproject.toml" not in nameset:
        add(
            "U-DEP-4",
            "uv.lock changed without pyproject.toml -- deliberate re-lock or ride-along?",
        )
    if "pyproject.toml" in nameset and "uv.lock" not in nameset:
        add(
            "U-DEP-4",
            "pyproject.toml changed without uv.lock -- if deps changed, `uv lock --check` fails (CI --frozen won't)",
        )
    for pkg in changed(r"(^|/)package\.json$"):
        lock = re.sub(r"package\.json$", "package-lock.json", pkg)
        if lock not in nameset:
            add("U-DEP-4", "%s changed without %s" % (pkg, lock))

    gen = changed(GENERATED)
    hand_source = [
        n
        for n in names
        if n not in gen
        and (
            GENERATOR_SOURCE.search(n)
            or re.search(r"(^|/)(sportsdataverse|src)/.+\.(py|ts)$", n)
        )
    ]
    if gen and not hand_source:
        add(
            "PY-2",
            "generated output edited with no codegen input change -- hand edit?",
            gen,
        )
    if changed(CODEGEN_INPUT) and not gen:
        add("PY-1", "codegen input changed but no regenerated output in the diff")

    if changed(r"(^|/)\.github/workflows/"):
        add(
            "U-CI-1",
            "workflow files changed -- read them in full",
            changed(r"(^|/)\.github/workflows/"),
        )

    v2 = [
        n
        for n in names
        if re.search(r"(^|/)astro/src/components/game/", n) and "/classic/" not in n
    ]
    if v2 and not changed(r"/components/game/classic/"):
        add(
            "GOP-TWIN-1",
            "v2 game components changed, classic/ twin untouched -- public page still renders classic",
            v2,
        )
    new_py_dirs = [
        f["filename"]
        for f in files
        if f.get("status") == "added"
        and re.match(r"^python/[^/]+/.+\.py$", f["filename"])
    ]
    if new_py_dirs and repo_name == "game-on-paper-app":
        add(
            "GOP-PY-1",
            "new python/ subpackage file -- Dockerfile copies top-level *.py only",
            new_py_dirs,
        )

    if changed(r"(^|/)infra/postgresql/|(^|/)sdv_db/catalog\.py$") and not changed(
        r"schema_snapshot\.json$"
    ):
        add(
            "PLAT-DB-4",
            "schema/catalog changed without a recaptured api/gen/schema_snapshot.json",
        )
    if changed(r"(^|/)sdv_orch/registry\.py$"):
        add(
            "PLAT-ORCH-4",
            "registry edited -- PR must state the sdv-orch-flows + sdv-db-api restarts",
        )

    tk = changed(r"(^|/)(skills/[^/]+/|agents/[^/]+\.md$|hooks/)")
    if tk:
        plugin = [
            f
            for f in files
            if re.search(r"(^|/)\.claude-plugin/plugin\.json$", f["filename"])
        ]
        # A touched plugin.json is not a bump: require an added "version" line.
        bumped = any(
            re.search(r'(?m)^\+\s*"version"\s*:', f.get("patch") or "") for f in plugin
        )
        if not bumped:
            add(
                "TK-1",
                "toolkit surfaces changed without a plugin.json version bump"
                + (" (plugin.json touched, version line unchanged)" if plugin else ""),
                tk,
            )
        new_entries = [
            f["filename"]
            for f in files
            if f.get("status") == "added"
            and re.search(
                r"(^|/)(skills/[^/]+/SKILL\.md|agents/[^/]+\.md)$", f["filename"]
            )
        ]
        if new_entries and not changed(r"(^|/)catalog\.json$"):
            add(
                "TK-1",
                "new skill/agent without a catalog.json row (CI rejects it)",
                new_entries,
            )

    new_fixtures = [
        f["filename"]
        for f in files
        if f.get("status") == "added"
        and re.search(
            r"(^|/)tests?/.*fixtures?/.*\.(parquet|json|csv|rds)$", f["filename"]
        )
    ]
    if new_fixtures:
        dirs = {str(pathlib.PurePosixPath(p).parent) for p in new_fixtures}
        if not any((d + "/README.md") in nameset for d in dirs):
            add(
                "U-TEST-3",
                "new fixtures without a provenance README in the same diff",
                new_fixtures,
            )

    data = [
        n
        for n in names
        if DATA_FILE.search(n) and not re.search(r"(^|/)(tests?|fixtures?)/", n)
    ]
    code = [
        n for n in names if re.search(r"\.(py|R|ts|js|astro|svelte|sh|ya?ml|sql)$", n)
    ]
    if len(data) >= 20 and code:
        add(
            "U-GIT-5",
            "%d data files mixed with %d code files -- split code from data"
            % (len(data), len(code)),
        )

    if len(names) > 300:
        add(
            "REVIEW-SIZE",
            "%d files -- bot reviewers skip PRs this large; fan out by archetype"
            % len(names),
        )
    return out


# --------------------------------------------------------------------------- #
# Review proof (sdv-ship Phase 5 Step 0, reviewer-side)
# --------------------------------------------------------------------------- #


def review_proof(reviews, head_sha, unresolved_threads):
    """Summarise whether any bot review actually covers the head commit."""
    rows = []
    covered = False
    for r in reviews:
        login = (r.get("user") or {}).get("login", "")
        if not BOT_LOGIN.search(login):
            continue
        body = r.get("body") or ""
        at_head = r.get("commit_id") == head_sha
        rate_limited = bool(
            re.search(r"(?i)rate limit|review limit|limit reached", body)
        )
        rows.append(
            {
                "by": login,
                "state": r.get("state"),
                "at_head": at_head,
                "body_len": len(body),
                "rate_limited": rate_limited,
                "outside_diff": bool(re.search(r"(?i)outside diff range", body)),
            }
        )
        if at_head and body and not rate_limited:
            covered = True
    return {
        "bot_reviews": rows,
        "unresolved_threads": unresolved_threads,
        "reviewed_at_head": covered and unresolved_threads == 0,
    }


# --------------------------------------------------------------------------- #
# gh I/O (thin; everything above is pure and unit-tested)
# --------------------------------------------------------------------------- #


def gh(*args, check=True):
    """Run `gh` read-only; stdout, raising on failure when `check` is set."""
    p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=180)
    if check and p.returncode != 0:
        raise RuntimeError(
            "gh %s failed: %s" % (" ".join(args[:3]), p.stderr.strip()[:300])
        )
    return p.stdout


def gh_json(*args, check=True):
    """Run `gh` and parse its stdout as JSON (None for empty output)."""
    out = gh(*args, check=check)
    return json.loads(out) if out.strip() else None


def gh_paginated(endpoint):
    """GET a paginated REST endpoint and flatten every page into one list."""
    out = gh("api", "--paginate", "--slurp", endpoint)
    pages = json.loads(out) if out.strip() else []
    return [item for page in pages for item in page]


THREADS_Q = """query($o:String!,$r:String!,$n:Int!,$c:String){repository(owner:$o,name:$r){pullRequest(number:$n){
reviewThreads(first:100,after:$c){pageInfo{hasNextPage endCursor}
nodes{isResolved isOutdated path line comments(first:1){nodes{author{login} body}}}}}}}"""


def fetch_threads(owner, name, number):
    """All review threads on a PR via GraphQL, following pagination."""
    threads, cursor = [], None
    while True:
        args = [
            "api",
            "graphql",
            "-f",
            "query=" + THREADS_Q,
            "-F",
            "o=" + owner,
            "-F",
            "r=" + name,
            "-F",
            "n=%d" % number,
        ]
        if cursor:
            args += ["-F", "c=" + cursor]
        data = gh_json(*args)
        rt = data["data"]["repository"]["pullRequest"]["reviewThreads"]
        threads += rt["nodes"]
        if not rt["pageInfo"]["hasNextPage"]:
            return threads
        cursor = rt["pageInfo"]["endCursor"]


def headline(body):
    """One-line title for a review comment (bold title first, severity prefixed)."""
    body = re.sub(r"<details>.*?</details>", " ", body or "", flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    severity = re.search(r"(Critical|Major|Minor|Trivial|Nitpick)", body)
    bold = re.search(r"\*\*(.{12,}?)\*\*", body)
    if bold:
        prefix = "[%s] " % severity.group(1) if severity else ""
        return (prefix + bold.group(1))[:160]
    for line in body.splitlines():
        line = line.strip(" _*#>")
        if len(line) > 12 and not line.lower().startswith(
            ("potential issue", "🧩", "🏁")
        ):
            return line[:140]
    return ""


def gather(repo, number):
    """Collect everything `context.md` reports for one PR; returns (context, diff)."""
    owner, name = repo.split("/", 1)
    fields = "number,title,url,state,isDraft,author,baseRefName,headRefName,headRefOid,isCrossRepository,mergeable,mergeStateStatus,additions,deletions,changedFiles,body,reviewDecision,statusCheckRollup,mergedAt,commits,labels"
    pr = gh_json("pr", "view", str(number), "-R", repo, "--json", fields)
    meta = gh_json(
        "repo", "view", repo, "--json", "isFork,visibility,defaultBranchRef,isArchived"
    )
    roots = [
        e["name"]
        for e in (
            gh_json(
                "api",
                "repos/%s/contents?ref=%s" % (repo, pr["baseRefName"]),
                check=False,
            )
            or []
        )
        if isinstance(e, dict)
    ]
    files = gh_paginated("repos/%s/pulls/%d/files?per_page=100" % (repo, number))
    diff = gh("pr", "diff", str(number), "-R", repo, check=False)
    if not diff.strip():  # "diff too large": rebuild from per-file patches
        diff = "\n".join(
            "+++ b/%s\n%s" % (f["filename"], f.get("patch", "")) for f in files
        )
    reviews = gh_paginated("repos/%s/pulls/%d/reviews?per_page=100" % (repo, number))
    threads = fetch_threads(owner, name, number)

    arche = repo_archetypes(owner, name, meta.get("isFork", False), roots)
    path_tags = {}
    for f in files:
        for t in classify_path(f["filename"]):
            path_tags.setdefault(t, []).append(f["filename"])
    union = list(arche) + [t for t in path_tags if t in REFERENCES and t not in arche]

    unresolved = [t for t in threads if not t["isResolved"]]
    checks = pr.get("statusCheckRollup") or []
    check_summary = {}
    for c in checks:
        k = (
            c.get("conclusion") or c.get("state") or c.get("status") or "PENDING"
        ).upper()
        check_summary[k] = check_summary.get(k, 0) + 1

    commit_msgs = "\n".join(
        (c.get("messageHeadline", "") + "\n" + c.get("messageBody", ""))
        for c in pr.get("commits", [])
    )
    trailer_hits = [ln for ln in commit_msgs.splitlines() if AI_TRAILER.search(ln)]
    callers, callers_unchecked = find_callers(
        name,
        pr["baseRefName"],
        caller_candidates(files),
        changed=list(_touched_paths(files)),
        modules=module_candidates(files),
    )

    return {
        "repo": repo,
        "pr": {
            k: pr.get(k)
            for k in (
                "number",
                "title",
                "url",
                "state",
                "isDraft",
                "baseRefName",
                "headRefName",
                "headRefOid",
                "isCrossRepository",
                "mergeable",
                "mergeStateStatus",
                "additions",
                "deletions",
                "changedFiles",
                "reviewDecision",
                "mergedAt",
            )
        },
        "author": (pr.get("author") or {}).get("login"),
        "repo_meta": meta,
        "archetypes": union,
        "path_tags": {k: v[:20] for k, v in path_tags.items()},
        "references": references_for(union),
        "checks": check_summary,
        "failing_checks": [
            c.get("name")
            for c in checks
            if (c.get("conclusion") or "").upper()
            in {"FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED"}
        ],
        "review_proof": review_proof(reviews, pr["headRefOid"], len(unresolved)),
        "unresolved_threads": [
            {
                "by": (t["comments"]["nodes"][0]["author"] or {}).get("login")
                if t["comments"]["nodes"]
                else None,
                "path": t["path"],
                "line": t["line"],
                "outdated": t["isOutdated"],
                "headline": headline(t["comments"]["nodes"][0]["body"])
                if t["comments"]["nodes"]
                else "",
            }
            for t in unresolved
        ],
        "commit_trailer_hits": trailer_hits,
        "caller_terms": caller_candidates(files) + module_candidates(files),
        "callers": callers,
        "callers_unchecked": callers_unchecked,
        "dangling_module_refs": local_module_refs(name, pr["baseRefName"], files, diff),
        "file_signals": file_signals(files, name),
        "signals": [asdict(s) for s in scan_diff(diff, name)],
        "files": [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f.get("additions"),
                "deletions": f.get("deletions"),
            }
            for f in files
        ],
    }, diff


def render_markdown(ctx):
    """Render the gathered context as the `context.md` a reviewer reads first."""
    p = ctx["pr"]
    rp = ctx["review_proof"]
    lines = [
        "# PR context: %s#%s -- %s" % (ctx["repo"], p["number"], p["title"]),
        "",
        "| field | value |",
        "|---|---|",
        "| url | %s |" % p["url"],
        "| state | %s%s%s |"
        % (
            p["state"],
            " (DRAFT)" if p["isDraft"] else "",
            " merged " + p["mergedAt"] if p.get("mergedAt") else "",
        ),
        "| author | %s%s |"
        % (ctx["author"], " (fork)" if p["isCrossRepository"] else ""),
        "| base <- head | %s <- %s @ %s |"
        % (p["baseRefName"], p["headRefName"], p["headRefOid"]),
        "| size | +%s/-%s in %s files |"
        % (p["additions"], p["deletions"], p["changedFiles"]),
        "| mergeable | %s / %s |" % (p["mergeable"], p["mergeStateStatus"]),
        "| review decision | %s (advisory: no repo requires checks; admins bypass) |"
        % p["reviewDecision"],
        "| visibility | %s |" % ctx["repo_meta"].get("visibility"),
        "| checks (runs + commit statuses) | %s |"
        % (
            ", ".join("%s=%d" % kv for kv in sorted(ctx["checks"].items()))
            or "none reported"
        ),
        "| failing checks | %s |" % (", ".join(ctx["failing_checks"]) or "-"),
        "",
        "## Archetypes -> load these references",
        "",
        "Archetypes: **%s**"
        % (", ".join(ctx["archetypes"]) or "unclassified (use universal + judgement)"),
        "",
    ]
    lines += ["- `%s`" % r for r in ctx["references"]]
    lines += ["", "Per-path tags:", ""]
    lines += [
        "- %s: %d file(s), e.g. `%s`" % (k, len(v), v[0])
        for k, v in sorted(ctx["path_tags"].items())
    ] or ["- none beyond the repo archetype"]
    lines += [
        "",
        "## Bot review proof (reviewed only if at head AND non-empty AND 0 unresolved)",
        "",
        "reviewed_at_head: **%s** | unresolved threads: %d"
        % (rp["reviewed_at_head"], rp["unresolved_threads"]),
        "",
        "| bot | reviews | non-empty | non-empty at head | rate-limited | outside-diff findings |",
        "|---|---|---|---|---|---|",
    ]
    per_bot = {}
    for r in rp["bot_reviews"]:
        b = per_bot.setdefault(
            r["by"], {"n": 0, "body": 0, "head": 0, "rl": False, "od": False}
        )
        b["n"] += 1
        b["body"] += 1 if r["body_len"] else 0
        b["head"] += 1 if (r["at_head"] and r["body_len"]) else 0
        b["rl"] = b["rl"] or r["rate_limited"]
        b["od"] = b["od"] or r["outside_diff"]
    lines += [
        "| %s | %d | %d | %d | %s | %s |"
        % (k, v["n"], v["body"], v["head"], v["rl"], v["od"])
        for k, v in sorted(per_bot.items())
    ] or ["| - | 0 | 0 | 0 | | |"]
    if ctx["unresolved_threads"]:
        lines += ["", "Unresolved threads:", ""]
        lines += [
            "- %s `%s:%s`%s -- %s"
            % (
                t["by"],
                t["path"],
                t["line"],
                " (outdated)" if t["outdated"] else "",
                t["headline"],
            )
            for t in ctx["unresolved_threads"][:40]
        ]
    lines += ["", "## File-level signals (leads, not findings)", ""]
    lines += [
        "- **%s** %s%s"
        % (
            s["rule"],
            s["note"],
            (": `" + "`, `".join(s["paths"][:6]) + "`") if s["paths"] else "",
        )
        for s in ctx["file_signals"]
    ] or ["- none"]
    lines += ["", "## Line signals in added code (leads, not findings)", ""]
    sig = ctx["signals"]
    lines += [
        "- **%s** `%s:%d` %s -- `%s`"
        % (s["rule"], s["path"], s["line"], s["note"], s["text"].replace("`", "'"))
        for s in sig[:80]
    ] or ["- none"]
    if len(sig) > 80:
        lines.append("- ... %d more in context.json" % (len(sig) - 80))
    lines += [
        "",
        "## Callers of changed entry points (local checkouts at origin/<base>; also check crontab and sibling repos)",
        "",
    ]
    lines += [
        "- `%s`:\n%s"
        % (base, "\n".join("  - `%s`" % h.replace("`", "'") for h in hits))
        for base, hits in ctx.get("callers", {}).items()
    ]
    if ctx.get("callers_unchecked") and ctx.get("caller_terms"):
        lines.append(
            "- repo search NOT CHECKED: %s -- only the sdv-orch registry was searched"
            % ctx["callers_unchecked"]
        )
    elif not ctx.get("callers"):
        if ctx.get("caller_terms"):
            lines.append(
                "- searched `%s`: no callers outside this PR's own files. NOT an all-clear --"
                " grep crontab, sdv-orch, and sibling repos yourself."
                % "`, `".join(ctx["caller_terms"][:8])
            )
        else:
            lines.append(
                "- no entry points or python modules changed (nothing to search)"
            )
    lines += ["", "## `python -m` targets that resolve to no module (PROD-5)", ""]
    dangling = ctx.get("dangling_module_refs")
    if dangling is None:
        lines.append(
            "- NOT CHECKED (no local checkout, origin/<base> unavailable, or git failed)"
        )
    else:
        lines += [
            "- `%s` in `%s` -- `%s`"
            % (d["module"], d["where"], d["text"].replace("`", "'"))
            for d in dangling
        ] or ["- none"]
    if ctx["commit_trailer_hits"]:
        lines += ["", "## Commit messages carrying AI attribution (U-GIT-4)", ""] + [
            "- `%s`" % h for h in ctx["commit_trailer_hits"]
        ]
    lines += ["", "## Files", ""]
    lines += [
        "- %s `%s` +%s/-%s"
        % (f["status"], f["filename"], f["additions"], f["deletions"])
        for f in ctx["files"][:200]
    ]
    if len(ctx["files"]) > 200:
        lines.append("- ... %d more in context.json" % (len(ctx["files"]) - 200))
    return "\n".join(lines) + "\n"


def main(argv=None):
    """CLI entry: gather one PR's context and write context.{md,json} and diff.patch."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pr", help="N, owner/repo#N, or a PR URL")
    ap.add_argument("-R", "--repo", help="owner/repo when pr is a bare number")
    ap.add_argument("--out", default=".", help="output directory (default: cwd)")
    a = ap.parse_args(argv)
    repo, number = parse_pr_ref(a.pr, a.repo)
    ctx, diff = gather(repo, number)
    d = pathlib.Path(a.out) / ("%s-%d" % (repo.split("/")[1], number))
    d.mkdir(parents=True, exist_ok=True)
    (d / "context.json").write_text(json.dumps(ctx, indent=2), encoding="utf-8")
    (d / "diff.patch").write_text(diff, encoding="utf-8")
    (d / "context.md").write_text(render_markdown(ctx), encoding="utf-8")
    print(d / "context.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
