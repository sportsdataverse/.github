#!/usr/bin/env python3
"""Mechanical probes for the sdv-repo-audit skill. Stdlib only, read-only.

Each subcommand prints markdown (or JSON with --json) and exits 0 when the probe
ran, 2 on a usage or I/O error. A finding is never an error exit: the auditor
decides what a probe hit means.

    python audit_probes.py archetype [REPO]          primary + secondary archetypes, with evidence
    python audit_probes.py release   [REPO] [--repo owner/name]
                                     (--pypi NAME | --cran NAME | --npm NAME | --runiverse OWNER | --workspaces)
    python audit_probes.py fragments [REPO] [--dir changelog.d] [--max-lines 3] [--groups a,b,...]
                                     changelog.d/, .changeset/ and NEWS.md; "no fragment system" when none
    python audit_probes.py leaks     [PATH ...] [--root REPO] [--private NAME ...]
    python audit_probes.py counts    [PATH ...] [--root REPO]
    python audit_probes.py osv       LOCKFILE        uv.lock, poetry.lock, renv.lock, package-lock.json,
                                                     yarn.lock (v1/berry), pnpm-lock.yaml, requirements*.txt

Network (release, osv) is read-only GETs/POSTs to public registries plus
`git ls-remote` and `gh api` GETs; an unreachable source is reported as
`unavailable`, never guessed, and a source never compared is reported as
`not compared`, never `none`. Explicit PATHs resolve against --root; a missing
path, or a lockfile with 0 packages, is an error (exit 2).
"""

import argparse
import collections
import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "sdv-repo-audit/1 (+https://github.com/sportsdataverse)"}
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".worktrees",
    "build",
    "dist",
    ".docusaurus",
    ".pytest_cache",
    ".ruff_cache",
    "renv",
}
BINARY_EXT = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".parquet",
    ".rds",
    ".gz",
    ".zip",
    ".whl",
    ".woff",
    ".woff2",
    ".ttf",
    ".svg",
    ".ubj",
    ".pkl",
    ".so",
    ".pyd",
}

# --------------------------------------------------------------------------- helpers


def _run(cmd, cwd=None, timeout=60):
    try:
        out = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,  # never wait on a credential or pager prompt
            env=dict(os.environ, GIT_TERMINAL_PROMPT="0"),
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout if out.returncode == 0 else None


def _get_json(url, data=None, timeout=30):
    req = urllib.request.Request(
        url,
        headers=dict(UA, **({"Content-Type": "application/json"} if data else {})),
        data=json.dumps(data).encode() if data is not None else None,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"__status__": e.code}
    except (urllib.error.URLError, OSError, ValueError):
        return None


def _get_text(url, timeout=30):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return {"__status__": e.code}
    except (urllib.error.URLError, OSError):
        return None


def vkey(v):
    """Sortable key for a version string: '0.1.10' > '0.1.9', '1.0' == '1.0.0'; non-numeric parts sort low."""
    parts = re.split(r"[.\-+]", (v or "").lstrip("vV"))
    key = [(int(p), "") if p.isdigit() else (-1, p) for p in parts]
    while len(key) > 1 and key[-1] == (0, ""):
        key.pop()
    return tuple(key)


def iter_text_files(paths):
    for p in paths:
        p = pathlib.Path(p)
        if p.is_file():
            yield p
            continue
        if not p.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                fp = pathlib.Path(dirpath) / f
                if fp.suffix.lower() in BINARY_EXT:
                    continue
                yield fp


def read_text(fp):
    try:
        raw = fp.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192]:
        return None
    return raw.decode("utf-8", "replace")


def _rel(fp, root):
    try:
        return pathlib.Path(fp).resolve().relative_to(pathlib.Path(root).resolve()).as_posix()
    except ValueError:
        return pathlib.Path(fp).as_posix()


# --------------------------------------------------------------------------- archetype


ARCHETYPES = (
    "sdv-py", "producer", "r-package", "js-package", "web-app", "db-service", "python-package", "other",
)  # fmt: skip
REFERENCE_FOR = {
    "sdv-py": "python-package.md",
    "python-package": "python-package.md",
    "r-package": "r-package.md",
    "producer": "producer.md",
    "js-package": "js-package.md",
    "web-app": "web-app.md",
    "db-service": "db-service.md",
    "other": "the closest reference file: pick one and say so",
}
WEB_DEPS = {
    "next",
    "astro",
    "@docusaurus/core",
    "@sveltejs/kit",
    "@remix-run/react",
    "@remix-run/node",
    "nuxt",
    "gatsby",
}
WEB_CONFIG_RE = re.compile(r"^(?:next|astro|docusaurus|remix|nuxt|gatsby)\.config\.[cm]?[jt]s$")
API_SERVERS = {"fastapi", "flask", "uvicorn", "starlette", "express", "fastify", "hono", "koa"}
COMPOSE_RE = re.compile(r"^(?:docker-)?compose(?:\.[\w-]+)?\.ya?ml$")
CATALOG_RE = re.compile(r"^catalog\.(?:json|ya?ml|toml)$")
NOT_SERVICE_DIRS = {"tests", "test", "fixtures", "testdata", "inst"}  # SQL here is test data or package data


def _py_dependencies(txt):
    """Distribution names from pyproject `dependencies = [...]`, the optional-dependencies arrays and
    `[tool.poetry.dependencies]` keys -- never keywords, classifiers or prose."""
    names = []
    m = re.search(r"(?ms)^dependencies\s*=\s*\[(.*?)\]", txt)
    arrays = [m.group(1)] if m else []
    for sec in re.finditer(r"(?ms)^\[project\.optional-dependencies\]\s*$(.*?)(?=^\[|\Z)", txt):
        arrays += re.findall(r"(?s)=\s*\[(.*?)\]", sec.group(1))
    for arr in arrays:
        names += [re.match(r"[A-Za-z0-9._-]+", s).group(0) for s in re.findall(r"[\"']([A-Za-z0-9][^\"']*)[\"']", arr)]
    for sec in re.finditer(r"(?ms)^\[tool\.poetry\.dependencies\]\s*$(.*?)(?=^\[|\Z)", txt):
        names += re.findall(r"(?m)^([A-Za-z0-9._-]+)\s*=", sec.group(1))
    return {n.lower() for n in names}


def _api_server_deps(repo, rel):
    """API-server packages among a manifest's runtime dependencies."""
    txt = read_text(repo / rel) or ""
    if rel.endswith("package.json"):
        try:
            deps = set((json.loads(txt).get("dependencies") or {}))
        except ValueError:
            deps = set()
    else:
        deps = _py_dependencies(txt)
    return sorted(deps & API_SERVERS)


def repo_files(repo, max_depth=4):
    """Posix paths of the repo's files: git-tracked when it is a checkout, else a bounded walk."""
    tracked = tracked_files(repo)
    if tracked is not None:
        return sorted(tracked)
    out = []
    for dirpath, dirnames, filenames in os.walk(repo):
        rel = pathlib.Path(dirpath).relative_to(repo)
        depth = len(rel.parts)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS] if depth < max_depth else []
        out += [(rel / f).as_posix() for f in filenames]
    return sorted(out)


def _json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _published(pkg):
    """A package.json that npm would publish as a library: not private, with an entry point."""
    return (
        bool(pkg) and not pkg.get("private") and any(pkg.get(k) for k in ("main", "module", "exports", "types", "bin"))
    )


def _glob_re(pat):
    """A workspace glob as a regex on a posix dir path: `*` is one segment, `**` any depth."""
    pat = pat.strip().strip("'\"").rstrip("/")
    pat = pat[2:] if pat.startswith("./") else pat
    out, i = "", 0
    while i < len(pat):
        if pat.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pat.startswith("/**", i) and i + 3 == len(pat):
            out, i = out + "(?:/.*)?", i + 3
        elif pat.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pat[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pat[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pat[i]), i + 1
    return re.compile(out + r"\Z")


def _pnpm_packages_block(txt):
    """List items of the top-level `packages:` key only (not onlyBuiltDependencies or catalogs)."""
    items, inside = [], False
    for ln in txt.splitlines():
        if re.match(r"^\S", ln):
            inside = bool(re.match(r"^packages\s*:", ln))
            continue
        m = re.match(r"^\s+-\s*['\"]?([^'\"\s#]+)", ln) if inside else None
        if m:
            items.append(m.group(1))
    return items


def workspace_members(repo):
    """[(dir, package.json dict)] for npm/yarn `workspaces` or pnpm-workspace.yaml `packages:` globs.

    Members are git-tracked `<glob>/package.json` files (a bounded walk outside a checkout), never
    anything under node_modules, minus `!` exclusions.
    """
    root = _json(repo / "package.json") or {}
    pats = root.get("workspaces") or []
    if isinstance(pats, dict):  # yarn: {"packages": [...]}
        pats = pats.get("packages") or []
    pw = repo / "pnpm-workspace.yaml"
    if pw.exists():
        pats = list(pats) + _pnpm_packages_block(pw.read_text(encoding="utf-8"))
    include = [_glob_re(p) for p in pats if not p.startswith("!")]
    exclude = [_glob_re(p[1:]) for p in pats if p.startswith("!")]
    if not include:
        return []
    members = []
    for f in repo_files(repo, max_depth=8):
        if not f.endswith("/package.json") or "node_modules" in f.split("/"):
            continue
        d = f[: -len("/package.json")]
        if any(rx.match(d) for rx in include) and not any(rx.match(d) for rx in exclude):
            pkg = _json(repo / f)
            if pkg is not None:
                members.append((repo / d, pkg))
    return members


def _web_dir(repo, rel_dir, names):
    """Does this directory hold a web-app framework (a config file, or a framework dependency)?"""
    d = repo / rel_dir
    if any(WEB_CONFIG_RE.match(n) for n in names):
        return True
    pkg = _json(d / "package.json") if "package.json" in names else None
    if not pkg:
        return False
    deps = set(pkg.get("dependencies") or {}) | set(pkg.get("devDependencies") or {})
    if deps & WEB_DEPS:  # WEB_DEPS covers SvelteKit apps too
        return True
    return "vite" in deps and "index.html" in names and not _published(pkg)  # a vite APP, not a vite-built library


def probe_archetype(repo, remote=""):
    """Primary archetype by precedence, plus secondaries for mixed repos, with the evidence for each.

    Precedence: sdv-py > producer > r-package > js-package > web-app (at the root, or in a subdir when
    the root has no manifest) > db-service > python-package > web-app (a docs site in a subdir) > other.
    """
    repo = pathlib.Path(repo).resolve()  # Path(".").name is ""
    name = remote.rstrip("/").rsplit("/", 1)[-1]
    name = name[:-4] if name.endswith(".git") else name
    files = repo_files(repo)
    by_dir = collections.defaultdict(set)
    for f in files:
        parent, _, base = f.rpartition("/")
        by_dir[parent].add(base)
    root = by_dir.get("", set())
    sig = collections.defaultdict(list)

    if "tools/codegen/generate.py" in files:
        sig["sdv-py"].append("tools/codegen/generate.py")
    if name.endswith(("-raw", "-data")) or repo.name.endswith(("-raw", "-data")):
        sig["producer"].append("repo name %s" % (name or repo.name))
    if "DESCRIPTION" in root and any(f.startswith("R/") for f in files):
        sig["r-package"].append("DESCRIPTION + R/")
    if "pyproject.toml" in root or "setup.py" in root:
        sig["python-package"].append("pyproject.toml" if "pyproject.toml" in root else "setup.py")
    if _published(_json(repo / "package.json")):
        sig["js-package"].append("package.json (published entry point)")
    pub = [pkg.get("name", str(d)) for d, pkg in workspace_members(repo) if _published(pkg)]
    if pub:
        sig["js-package"].append("workspace members: " + ", ".join(pub))
    for d in sorted(by_dir):
        if d.count("/") < 1 and _web_dir(repo, d, by_dir[d]):  # the root and one level down
            sig["web-root" if d == "" else "web-sub"].append(d or ".")
    for f in files:
        parts = f.split("/")
        base = parts[-1]
        if NOT_SERVICE_DIRS & set(parts[:-1]) or "node_modules" in parts:
            continue
        if {"alembic", "migrations"} & set(parts[:-1]) or base.endswith(".sql"):
            sig["db-strong"].append(f)
        elif base.endswith((".service", ".timer")):
            sig["db-strong"].append(f)
        elif base == "Dockerfile" or COMPOSE_RE.match(base) or (CATALOG_RE.match(base) and len(parts) <= 2):
            sig["db-weak"].append(f)
        elif base in ("pyproject.toml", "package.json") and len(parts) <= 2:
            servers = _api_server_deps(repo, f)
            if servers:
                sig["db-weak"].append("%s (API server dependency: %s)" % (f, ", ".join(servers)))
    # a service needs both halves: state (migrations, SQL, units) AND a way to serve or run it
    if sig.get("db-strong") and sig.get("db-weak"):
        sig["db-service"] = sig["db-strong"][:5] + sig["db-weak"][:5]
    no_root_manifest = not root & {"pyproject.toml", "setup.py", "package.json", "DESCRIPTION"}

    ranked = []
    for arch in ("sdv-py", "producer", "r-package", "js-package"):
        if sig.get(arch):
            ranked.append(arch)
    if sig.get("web-root") or (sig.get("web-sub") and no_root_manifest):
        ranked.append("web-app")
    for arch in ("db-service", "python-package"):
        if sig.get(arch):
            ranked.append(arch)
    if sig.get("web-sub") and "web-app" not in ranked:
        ranked.append("web-app")
    if ranked and ranked[0] == "sdv-py" and "python-package" in ranked:
        ranked.remove("python-package")  # sdv-py already is one
    primary = ranked[0] if ranked else "other"
    secondary = ranked[1:]
    refs = []
    for arch in [primary] + secondary:
        ref = REFERENCE_FOR[arch]
        if arch != "other" and ref not in refs:
            refs.append(ref)
    shown = {k: v for k, v in sig.items() if k not in ("web-root", "web-sub")}
    if sig.get("web-root") or sig.get("web-sub"):
        shown["web-app"] = sig.get("web-root", []) + sig.get("web-sub", [])
    return {"primary": primary, "secondary": secondary, "references": refs, "signals": dict(shown)}


def detect_archetype(repo, remote=""):
    """The primary archetype only; see probe_archetype for the secondaries and the evidence."""
    return probe_archetype(repo, remote)["primary"]


# --------------------------------------------------------------------------- release


def local_version(repo: pathlib.Path):
    """(version, source file) from pyproject [project], DESCRIPTION, or package.json."""
    pp = repo / "pyproject.toml"
    if pp.exists():
        txt = pp.read_text(encoding="utf-8")
        sec = re.search(r"(?ms)^\[project\]\s*$(.*?)(?=^\[)", txt + "\n[")
        m = re.search(r'(?m)^version\s*=\s*["\']([^"\']+)["\']', sec.group(1) if sec else "")
        if m:
            return m.group(1), "pyproject.toml"
    desc = repo / "DESCRIPTION"
    if desc.exists():
        m = re.search(r"(?m)^Version:\s*(\S+)", desc.read_text(encoding="utf-8"))
        if m:
            return m.group(1), "DESCRIPTION"
    pj = repo / "package.json"
    if pj.exists():
        try:
            v = json.loads(pj.read_text(encoding="utf-8")).get("version")
        except ValueError:
            v = None
        if v:
            return v, "package.json"
    return None, None


_HEAD_RE = re.compile(
    r"(?m)^#{1,3}\s+(?:\[?v?(\d+\.\d+(?:\.\d+)*(?:[.\-]\w+)?)\]?|\S+\s+v?(\d+\.\d+(?:\.\d+)*(?:[.\-]\w+)?))"
)


def newest_changelog_heading(repo: pathlib.Path):
    """(version, file, is_dev) from the first version heading of CHANGELOG.md or NEWS.md."""
    for name in ("CHANGELOG.md", "NEWS.md"):
        fp = repo / name
        if not fp.exists():
            continue
        txt = fp.read_text(encoding="utf-8", errors="replace")
        for line in txt.splitlines():
            if not line.startswith("#"):
                continue
            if re.search(r"(?i)development version|unreleased", line):
                return None, name, True
            m = _HEAD_RE.match(line)
            if m:
                return m.group(1) or m.group(2), name, False
    return None, None, False


def count_fragments(repo: pathlib.Path, d="changelog.d"):
    fdir = repo / d
    if not fdir.is_dir():
        return None
    groups = collections.Counter()
    for f in fdir.glob("*.md"):
        if f.name.lower() == "readme.md":
            continue
        parts = f.name.split(".")
        groups[parts[-2] if len(parts) >= 3 else "?"] += 1
    return dict(groups)


def tag_for(version, tags):
    """The tag naming `version` ('v0.1.4' or '0.1.4'), or None."""
    return next((t for t in tags if version and t.lstrip("vV") == version), None)


def compare_release(local, registry, tags, latest_release, changelog_head):
    """Mismatch strings between the version sources. Pure: unit-tested.

    Tags are matched by name, never by "newest": SDV repos carry old-line tags
    (sdv-py's pandas-era 0.36.0/0.37.0) that sort above the current line.
    """
    out = []
    if registry and local and vkey(local) < vkey(registry):
        out.append("local version %s is BEHIND the registry (%s)" % (local, registry))
    if registry and local and vkey(local) > vkey(registry):
        if re.search(r"\.9\d{3}$", local):  # R dev version: normal between releases
            out.append("development version %s (registry: %s): weigh the commits since the tag" % (local, registry))
        else:
            out.append(
                "local version %s is not on the registry yet (registry: %s): unreleased work" % (local, registry)
            )
    if registry and tags is not None and not tag_for(registry, tags):
        out.append("registry version %s has no git tag" % registry)
    if local and registry and vkey(local) > vkey(registry) and tag_for(local, tags or []):
        out.append(
            "tag %s exists but %s is not on the registry: the publish step did not run" % (tag_for(local, tags), local)
        )
    if latest_release is not None and registry and latest_release.lstrip("vV") != registry:
        out.append("GitHub 'Latest' release %s != registry version %s" % (latest_release or "(none)", registry))
    if changelog_head and registry and vkey(changelog_head) > vkey(registry):
        out.append(
            "changelog's newest released heading %s was never published (registry: %s)" % (changelog_head, registry)
        )
    return out


def _npm_latest(name):
    j = _get_json("https://registry.npmjs.org/%s/latest" % name.replace("/", "%2F"))
    return (j or {}).get("version") if j and "__status__" not in j else None


def compare_workspaces(members, registry, tags):
    """Per published workspace member: its version vs npm vs its tags. Pure: unit-tested.

    Monorepo tags name the package (`@scope/pkg@0.1.0`, the changesets form). Repo-wide `v0.1.0`
    tags are never borrowed: in a monorepo they belong to no single member.
    """
    rows = []
    for d, pkg in members:
        if not _published(pkg):
            continue
        name, local = pkg.get("name"), pkg.get("version")
        if not name:
            rows.append({"name": "(unnamed: %s)" % d, "local": local, "registry": None, "tags": [],
                         "mismatches": ["package.json has no name: skipped"]})  # fmt: skip
            continue
        mine = sorted((t[len(name) + 1 :] for t in tags if t.startswith(name + "@")), key=vkey)
        reg = registry.get(name)
        mism = compare_release(local, reg, mine if mine else None, None, None)
        if not mine:
            mism.append("no per-package tags (%s@x.y.z): tags not compared" % name)
        if reg is None:
            mism.append("npm version unavailable (not published, or the registry was unreachable)")
        if local is None:
            mism.append("no version in package.json")
        rows.append({"name": name, "local": local, "registry": reg, "tags": mine[-3:], "mismatches": mism})
    return rows


def probe_release(repo, owner_repo, pypi, cran, npm, runiverse=None, workspaces=False):
    local, src = local_version(repo)
    reg_name, registry = None, None
    if runiverse:
        desc = repo / "DESCRIPTION"
        m = re.search(r"(?m)^Package:\s*(\S+)", desc.read_text(encoding="utf-8")) if desc.exists() else None
        j = _get_json("https://%s.r-universe.dev/api/packages/%s" % (runiverse, m.group(1))) if m else None
        reg_name, registry = "r-universe", (j or {}).get("Version") if j and "__status__" not in j else None
    elif pypi:
        j = _get_json("https://pypi.org/pypi/%s/json" % pypi)
        reg_name, registry = "PyPI", (j or {}).get("info", {}).get("version") if j and "__status__" not in j else None
    elif cran:
        t = _get_text("https://cran.r-project.org/web/packages/%s/DESCRIPTION" % cran)
        m = re.search(r"(?m)^Version:\s*(\S+)", t) if isinstance(t, str) else None
        reg_name, registry = "CRAN", m.group(1) if m else None
    elif npm:
        j = _get_json("https://registry.npmjs.org/%s/latest" % npm)
        reg_name, registry = "npm", (j or {}).get("version") if j and "__status__" not in j else None
    ls = _run(["git", "-C", str(repo), "ls-remote", "--tags", "origin"])
    all_tags = sorted(
        {ln.split("refs/tags/")[1].replace("^{}", "") for ln in (ls or "").splitlines() if "refs/tags/" in ln}
    )
    tags = sorted((t for t in all_tags if re.match(r"v?\d", t)), key=vkey)
    if not owner_repo:
        m = re.search(
            r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$",
            (_run(["git", "-C", str(repo), "remote", "get-url", "origin"]) or "").strip(),
        )
        owner_repo = m.group(1) if m else None
    # gh api (not `gh release list --json`, which older gh lacks); "" = no Latest release, None = unavailable
    latest = None
    if owner_repo:
        out = _run(["gh", "api", "repos/%s/releases/latest" % owner_repo, "--jq", ".tag_name"])
        if out is not None:
            latest = out.strip()
        else:
            j = _get_json("https://api.github.com/repos/%s/releases/latest" % owner_repo)
            latest = "" if j and j.get("__status__") == 404 else (j or {}).get("tag_name")
    head, head_file, head_dev = newest_changelog_heading(repo)
    base_tag = tag_for(registry, tags) if registry else None
    since = _run(["git", "-C", str(repo), "rev-list", "--count", "%s..HEAD" % base_tag]) if base_tag else None
    result = {
        "local_version": local,
        "local_source": src,
        "registry": reg_name,
        "registry_version": registry if reg_name else None,
        "tags_by_version": tags[-6:] if ls is not None else "unavailable",
        "github_latest_release": latest if latest is not None else "unavailable",
        "changelog_newest_heading": "development version" if head_dev else head,
        "changelog_file": head_file,
        "commits_since_registry_tag": (
            "%s: %s" % (base_tag, since.strip() if since and since.strip().isdigit() else "unavailable")
            if base_tag
            else None
        ),
        "unreleased_fragments": count_fragments(repo),
    }
    if workspaces:  # a monorepo: each published member is its own release line
        rows = compare_workspaces(
            workspace_members(repo),
            {p.get("name"): _npm_latest(p["name"]) for _, p in workspace_members(repo) if _published(p)},
            all_tags,
        )
        result["workspaces"] = rows
        mism = ["%s: %s" % (r["name"], m) for r in rows for m in r["mismatches"]]
        if not rows:
            mism.append("no published workspace members found (workspaces / pnpm-workspace.yaml)")
        if ls is None:
            mism.append("git ls-remote failed: tags not compared")
        result["mismatches"] = mism
        result["compared"] = bool(rows) and ls is not None and all(r["registry"] for r in rows)
        return result
    mism = compare_release(local, registry, tags if ls is not None else None, latest, None if head_dev else head)
    # every source that was NOT compared is a finding of its own, so "none" can only mean "all compared, all agree"
    if not reg_name:
        mism.append("no registry compared: pass --pypi, --cran, --npm, --runiverse or --workspaces")
    elif registry is None:
        mism.append("%s version unavailable (not published, or the registry was unreachable)" % reg_name)
    if local is None:
        mism.append("local version unreadable (no [project] version, DESCRIPTION Version or package.json version)")
    if ls is None:
        mism.append("git ls-remote failed: tags not compared")
    result["mismatches"] = mism
    if latest is None:
        mism.append("GitHub Latest release not compared (gh and the GitHub API both failed, or no GitHub remote)")
    result["compared"] = bool(reg_name and registry and local and ls is not None and latest is not None)
    return result


# --------------------------------------------------------------------------- fragments

INTERNAL_ID_RE = re.compile(r"\b[A-Z]{1,2}-[LM]\d+\b|\bR\d{3,}-\d+\b|\b[Tt]ask \d+(?:\.\d+)*\b|\b[Pp]hase ?\d+[a-z]?\b")
PR_RE = re.compile(r"#\d+|/pull/\d+")


def lint_fragment_text(text, max_lines=3):
    """Problems in one fragment's bullets: (line_no, problem). Pure: unit-tested."""
    bullets, cur = [], None
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^[-*] ", line):
            cur = [i, [line]]
            bullets.append(cur)
        elif not line.strip():
            cur = None  # a blank line ends the bullet
        elif cur:
            cur[1].append(line)
    probs = []
    if not bullets:
        probs.append((1, "no bullet (expected '- ...')"))
    for start, lines in bullets:
        body = " ".join(lines)
        if not PR_RE.search(body):
            probs.append((start, "no PR number"))
        if len(lines) > max_lines:
            probs.append((start, "bullet runs %d lines (max %d)" % (len(lines), max_lines)))
        for m in INTERNAL_ID_RE.finditer(body):
            probs.append((start, "internal id %r" % m.group(0)))
    return probs


BUMPS = ("patch", "minor", "major")
REF_RE = re.compile(r"#\d+|/pull/\d+|/issues/\d+")


def lint_changeset(text):
    """Problems in one .changeset/*.md: frontmatter of `"pkg": bump` lines, then a summary."""
    probs = []
    m = re.match(r"(?s)^---\r?\n(.*?)\r?\n?---\r?\n?(.*)$", text)
    if not m:
        probs.append((1, 'no frontmatter (--- "pkg": bump ---)'))
        body = text
    else:
        for i, ln in enumerate(m.group(1).splitlines(), 2):
            kv = re.match(r"^\s*(.+?)\s*:\s*(\S+)\s*$", ln)
            bump = kv.group(2).strip("\"'") if kv else None  # `"@s/a": "minor"` is valid YAML too
            if kv and bump not in BUMPS:
                probs.append((i, "bump %r for %s is not patch/minor/major" % (bump, kv.group(1))))
        body = m.group(2)
        if not body.strip():
            probs.append((1, "empty summary"))
    for hit in INTERNAL_ID_RE.finditer(body):
        probs.append((1, "internal id %r" % hit.group(0)))
    return probs


def _is_version_heading(line):
    return bool(_HEAD_RE.match(line) or re.match(r"^#{1,3}\s.*(?i:development version|unreleased)", line))


def news_top_section(text):
    """(heading, first_line_no, lines) of NEWS.md's first VERSION section, at whatever heading level
    (`# pkg 1.0`, `## v1.0` under a `# Changelog` title, `## pkg (development version)`); it ends at the
    next heading of the same or a higher level. (None, 0, []) when no heading names a version."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("#") and _is_version_heading(ln):
            level = len(ln) - len(ln.lstrip("#"))
            end = next(
                (j for j in range(i + 1, len(lines))
                 if re.match(r"^#{1,%d}\s" % level, lines[j])),
                len(lines),
            )  # fmt: skip
            return ln, i + 1, lines[i + 1 : end]
    return None, 0, []


def lint_news(text):
    """(summary, findings) for the top NEWS.md section: R NEWS bullets rarely carry PR refs, so missing refs
    are counted, not listed; internal ids are findings."""
    heading, start, body = news_top_section(text)
    bullets, cur = [], None
    for i, ln in enumerate(body, start + 1):
        if re.match(r"^[-*] ", ln):
            cur = [i, [ln]]
            bullets.append(cur)
        elif not ln.strip() or ln.startswith("#"):
            cur = None
        elif cur:
            cur[1].append(ln)
    findings = [(i, "internal id %r" % h.group(0)) for i, b in bullets for h in INTERNAL_ID_RE.finditer(" ".join(b))]
    without = sum(1 for _, b in bullets if not REF_RE.search(" ".join(b)))
    return {"section": heading, "bullets": len(bullets), "without_ref": without}, findings


def probe_fragments(repo, d=None, max_lines=3, groups=()):
    """Lint every fragment system present: `changelog.d/` (or --dir), `.changeset/`, and NEWS.md's top section.

    With no system present the result says so (`systems: []`): never "0 problems".
    """
    systems, findings, res = [], [], {}
    if d or (repo / "changelog.d").is_dir():
        d = d or "changelog.d"
        if (repo / d).is_dir():
            systems.append(d)
            res["fragments"], dir_findings = _lint_fragment_dir(repo, d, max_lines, groups)
            findings += dir_findings
        else:
            res["missing_dir"] = d
        explicit = True
    else:
        explicit = False
    if not explicit or d == "changelog.d":
        cs = repo / ".changeset"
        if cs.is_dir():
            systems.append("changesets")
            files = [f for f in sorted(cs.glob("*.md")) if f.name.lower() != "readme.md"]
            res["changesets"] = len(files)
            for f in files:
                for line, prob in lint_changeset(read_text(f) or ""):
                    findings.append({"file": ".changeset/%s" % f.name, "line": line, "problem": prob})
        news = repo / "NEWS.md"
        if news.exists():
            summary, news_findings = lint_news(read_text(news) or "")
            if summary["section"] is None:
                res["news_unlinted"] = True  # a NEWS.md with no version heading: say so, never "0 bullets"
            else:
                systems.append("NEWS.md")
                res["news"] = summary
                findings += [{"file": "NEWS.md", "line": i, "problem": p} for i, p in news_findings]
    res.update(systems=systems, findings=findings)
    return res


def _lint_fragment_dir(repo, d, max_lines, groups):
    fdir = repo / d
    findings = []
    for f in sorted(fdir.glob("*")):
        if f.is_dir() or f.name.lower() == "readme.md":
            continue
        parts = f.name.split(".")
        if f.suffix != ".md" or len(parts) < 3 or (groups and parts[-2] not in groups):
            findings.append(
                {
                    "file": "%s/%s" % (d, f.name),
                    "line": 1,
                    "problem": "name is not <slug>.<group>.md with a known group",
                }
            )
        txt = read_text(f) or ""
        if txt and not txt.endswith("\n"):
            findings.append({"file": "%s/%s" % (d, f.name), "line": 1, "problem": "no final newline"})
        for line, prob in lint_fragment_text(txt, max_lines):
            findings.append({"file": "%s/%s" % (d, f.name), "line": line, "problem": prob})
    return len([f for f in fdir.glob("*.md") if f.name.lower() != "readme.md"]), findings


# --------------------------------------------------------------------------- leaks

DEFAULT_PRIVATE = ["sdv-internal-refs", "ClaudeCowork", "sdv-data-api", "rbgh"]
LEAK_PATTERNS = [
    # `(?<![\w.:/])` keeps URL paths such as `/team/home/away/` out
    ("local-path", re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+\w+|(?<![\w.:/])/(?:home|Users)/[A-Za-z_][\w-]*/")),
    ("server-path", re.compile(r"(?<![\w.:/])/mnt/[\w.-]+|(?<![\w.:/])/root/\.[\w-]+")),
    ("ip-address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?!\.\d)")),
    ("internal-id", INTERNAL_ID_RE),
    ("agent-note", re.compile(r"\bponytail:|\.superpowers/|\bSDD\b|\bRESTART\.md\b")),
    ("working-note", re.compile(r"(?<![\w/])dev/[\w./-]+\.(?:md|py|R|ipynb)\b")),
]
# loopback, unspecified, broadcast, RFC 1918 private, RFC 5737 documentation, and the usual placeholders
_IP_OK = re.compile(
    r"^(?:0\.0\.0\.0|127\.\d+\.\d+\.\d+|255\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|192\.0\.2\.\d+|198\.51\.100\.\d+|203\.0\.113\.\d+"
    r"|1\.2\.3\.4|1\.1\.1\.1|8\.8\.8\.8|8\.8\.4\.4)$"
)
# a four-part version, not an address: only when a version marker sits IMMEDIATELY before the token
_VERSION_MARKER = re.compile(r"(?i)(?:\bv|==|>=|<=|~=|\bversion\s)\s*$")


def scan_leaks(text, private):
    """[(line_no, kind, match)] for one file's text. Pure: unit-tested."""
    pats = list(LEAK_PATTERNS)
    if private:
        pats.append(("private-repo", re.compile("|".join(re.escape(p) for p in private))))
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for kind, rx in pats:
            for m in rx.finditer(line):
                tok = m.group(0)
                if kind == "ip-address" and (_IP_OK.match(tok) or _VERSION_MARKER.search(line[: m.start()])):
                    continue
                hits.append((i, kind, tok))
    return hits


DEFAULT_PUBLIC = [
    "README.md",
    "README.Rmd",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "NEWS.md",
    "changelog.d",
    "docs",
    "vignettes",
    "man",
    "_pkgdown.yml",
    "pkgdown",
    ".github",
    "DESCRIPTION",
    "pyproject.toml",
    "package.json",
    "src/pages",
    "examples",
]


def excluded(fp, root, patterns):
    rel = _rel(fp, root)
    return any(fnmatch.fnmatch(rel, p) for p in patterns)


def tracked_files(root):
    """Root-relative posix paths git tracks, or None outside a git checkout.

    Untracked agent state (.omc/, gitignored plans) is not public and is not a finding.
    """
    out = _run(["git", "-C", str(root), "ls-files", "-z"])
    return set(out.split("\0")) - {""} if out is not None else None


def _skip(fp, root, exclude, tracked):
    return excluded(fp, root, exclude) or (tracked is not None and _rel(fp, root) not in tracked)


def resolve_paths(root, paths, defaults):
    """Explicit paths resolve against root (not cwd) and must exist; no paths -> the defaults present."""
    if not paths:
        return [root / p for p in defaults if (root / p).exists()]
    out = [pathlib.Path(p) if pathlib.Path(p).is_absolute() else root / p for p in paths]
    missing = [str(p) for p in out if not p.exists()]
    if missing:
        raise ValueError("path not found under --root %s: %s" % (root, ", ".join(missing)))
    return out


def probe_leaks(root, paths, private, exclude=()):
    paths = resolve_paths(root, paths, DEFAULT_PUBLIC)
    tracked = tracked_files(root)
    by_kind = collections.Counter()
    findings = []
    for fp in iter_text_files(paths):
        if _skip(fp, root, exclude, tracked):
            continue
        txt = read_text(fp)
        if not txt:
            continue
        for line, kind, tok in scan_leaks(txt, private):
            by_kind[kind] += 1
            findings.append({"file": _rel(fp, root), "line": line, "kind": kind, "match": tok})
    return {"scanned": [_rel(p, root) for p in paths], "by_kind": dict(by_kind), "findings": findings}


# --------------------------------------------------------------------------- counts

COUNT_NOUNS = (
    "wrappers|functions|leagues|endpoints|providers|loaders|parsers|modules|skills|agents|datasets|"
    "families|sports|tests|surfaces|stems|fixtures|competitions|tables|columns|releases|repos|packages|"
    "notebooks|vignettes|seasons|teams|exports"
)
COUNT_RE = re.compile(
    r"(?i)(?<![\w.#/-])(~|about |over |more than |nearly )?(\d{1,3}(?:,\d{3})+|\d+)(\+)?\s+"
    r"(?:[a-z-]+\s+){0,2}?(" + COUNT_NOUNS + r")\b"
)


def find_counts(text):
    """[(line_no, number, noun, snippet)]. Pure: unit-tested."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in COUNT_RE.finditer(line):
            raw = m.group(2)
            n = int(raw.replace(",", ""))
            if n < 2 or ("," not in raw and len(raw) == 4 and 1900 <= n <= 2100):  # bare years only
                continue
            out.append((i, n, m.group(4).lower(), line.strip()[:160]))
    return out


def probe_counts(root, paths, exclude=()):
    paths = resolve_paths(root, paths, DEFAULT_PUBLIC + ["CLAUDE.md", "AGENTS.md"])
    tracked = tracked_files(root)
    by_noun = collections.defaultdict(list)
    for fp in iter_text_files(paths):
        if _skip(fp, root, exclude, tracked):
            continue
        if fp.suffix.lower() not in {
            ".md",
            ".mdx",
            ".rmd",
            ".qmd",
            ".yml",
            ".yaml",
            ".txt",
            ".rst",
            ".json",
            ".tsx",
            ".ts",
            ".js",
            ".r",
            ".py",
            "",
        }:
            continue
        txt = read_text(fp)
        if not txt:
            continue
        for line, n, noun, snip in find_counts(txt):
            by_noun[noun].append({"file": _rel(fp, root), "line": line, "n": n, "text": snip})
    # a lead, not a finding: "128 wrappers" (one stem) and "4,566 wrappers" (all ESPN) can both be right
    several = {k: sorted({h["n"] for h in v}) for k, v in by_noun.items() if len({h["n"] for h in v}) > 1}
    return {"by_noun": dict(by_noun), "nouns_quoted_with_several_numbers": several}


# --------------------------------------------------------------------------- osv


LOCKFILES = ("uv.lock", "poetry.lock", "renv.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml")
_YARN_WORKSPACE = ("@workspace:", "@patch:", "@portal:", "@link:")  # the repo's own packages: not dependencies
_NON_REGISTRY = re.compile(r"(?i)^(?:git[+:]|github:|gitlab:|bitbucket:|file:|https?:|link:|portal:|exec:)|#")
_PNPM_KEY = re.compile(r"^  (?! )['\"]?/?((?:@[^/@\s'\"]+/)?[^@\s'\"(/]+)@([^(\s'\"]+?)(?:\(.*)?['\"]?:\s*(?:\{.*)?$")
_REQ_PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*={2,3}\s*([^\s;#,]+)")


def _split_spec(spec):
    """'@babel/core@^7.0.0' -> ('@babel/core', '^7.0.0'); the range keeps any 'npm:' protocol."""
    spec = spec.strip().strip("\"'")
    i = spec.find("@", 1)
    return (spec[:i], spec[i + 1 :]) if i > 0 else (spec, "")


def _yarn_target(spec):
    """(registry name, unchecked?) for one header spec: an `x@npm:real@^1` alias resolves to `real`;
    git, file, URL and other non-registry ranges cannot be checked against OSV."""
    name, rng = _split_spec(spec)
    if rng.startswith("npm:"):
        rng = rng[4:]
        if "@" in rng.lstrip("@"):  # alias: npm:<real-name>@<range>
            name, rng = _split_spec(rng)
    return name, bool(_NON_REGISTRY.search(rng))


def _parse_yarn(txt):
    out, unchecked = set(), 0
    berry = "__metadata:" in txt
    for block in re.split(r"\n\s*\n", txt):
        lines = [ln for ln in block.splitlines() if ln.strip() and not ln.startswith("#")]
        if not lines or lines[0].startswith(" ") or not lines[0].rstrip().endswith(":"):
            continue
        header = lines[0].rstrip()[:-1]
        if header == "__metadata" or any(s in header for s in _YARN_WORKSPACE):
            continue
        field = {}
        for ln in lines[1:]:
            m = re.match(r'^  (version|resolution):?\s+"?([^"]+?)"?\s*$', ln)
            if m:
                field[m.group(1)] = m.group(2)
        ver = field.get("version")
        if not ver or "use.local" in ver:
            continue
        if berry and "resolution" in field:  # resolution names the package actually installed: "string-width@npm:4.2.3"
            res = field.get("resolution", "")
            name, rng = _split_spec(res)
            if rng.startswith("npm:"):
                out.add(("npm", name, rng[4:] or ver))
            else:
                unchecked += 1
            continue
        targets = {_yarn_target(s) for s in header.split(",")}
        if any(bad for _, bad in targets):
            unchecked += 1
        for name, bad in targets:
            if not bad:
                out.add(("npm", name, ver))
    return sorted(out), unchecked


def _parse_pnpm(txt):
    out, unchecked, section = set(), 0, None
    for ln in txt.splitlines():
        if ln and not ln.startswith(" "):
            section = ln.rstrip(":").strip()
            continue
        if section in ("packages", "snapshots"):
            m = _PNPM_KEY.match(ln)
            if not m:
                continue
            if re.match(r"\d", m.group(2)):
                out.add(("npm", m.group(1), m.group(2)))
            else:  # tarball / git keys: `foo@https://codeload...`
                unchecked += 1
    return sorted(out), unchecked


def _parse_requirements(txt):
    """Exact `==`/`===` pins only; ranges and `-r`/`-e` lines cannot be checked against one version."""
    out, unchecked = set(), 0
    for ln in txt.splitlines():
        ln = ln.split("#", 1)[0].strip()
        if not ln or ln.startswith("-"):
            continue
        m = _REQ_PIN.match(ln)
        if m:
            out.add(("PyPI", m.group(1).lower(), m.group(2)))
        else:
            unchecked += 1
    return sorted(out), unchecked


def parse_lock_full(path: pathlib.Path):
    """([(ecosystem, name, version)], unchecked) from any LOCKFILES name or requirements*.txt.

    `unchecked` counts entries that cannot be looked up by name and version (git, file, URL and tarball
    specs, unpinned requirements), so a clean OSV result never hides them. Pure-ish: unit-tested.
    """
    name = path.name
    low = name.lower()  # fnmatchcase on the lowered name: the same answer on Windows and Linux
    is_req = fnmatch.fnmatchcase(low, "requirements*.txt")
    if low not in LOCKFILES and not is_req:
        raise ValueError("unsupported lockfile: %s (%s, requirements*.txt)" % (name, ", ".join(LOCKFILES)))
    txt = path.read_text(encoding="utf-8")
    if is_req:
        return _parse_requirements(txt)
    if low == "yarn.lock":
        return _parse_yarn(txt)
    if low == "pnpm-lock.yaml":
        return _parse_pnpm(txt)
    if low in ("uv.lock", "poetry.lock"):
        out = []
        for block in re.split(r"(?m)^\[\[package\]\]\s*$", txt)[1:]:
            n = re.search(r'(?m)^name\s*=\s*"([^"]+)"', block)
            v = re.search(r'(?m)^version\s*=\s*"([^"]+)"', block)
            if n and v and "source = { editable" not in block and "source = { virtual" not in block:
                out.append(("PyPI", n.group(1), v.group(1)))
        return out, 0
    data = json.loads(txt)
    if low == "renv.lock":
        pkgs = data.get("Packages", {})
        out = [
            ("CRAN", k, p.get("Version"))
            for k, p in pkgs.items()
            if p.get("Version") and p.get("Source", "Repository") in ("Repository", "CRAN")
        ]
        return out, len(pkgs) - len(out)
    out, unchecked = set(), 0  # package-lock.json: v2/v3 "packages" map, v1 nested "dependencies" tree
    for key, p in (data.get("packages") or {}).items():
        if key and p.get("version") and "node_modules/" in key:
            if _NON_REGISTRY.search(str(p.get("resolved", ""))) and "registry" not in str(p.get("resolved", "")):
                unchecked += 1
            else:
                out.add(("npm", key.rsplit("node_modules/", 1)[1], p["version"]))
    stack = [data.get("dependencies") or {}]
    while stack:
        for dep, p in stack.pop().items():
            if isinstance(p, dict):
                if p.get("version") and not _NON_REGISTRY.search(str(p["version"])):
                    out.add(("npm", dep, p["version"]))
                elif p.get("version"):
                    unchecked += 1
                stack.append(p.get("dependencies") or {})
    return sorted(out), unchecked


def parse_lock(path: pathlib.Path):
    """[(ecosystem, name, version)]: parse_lock_full without the unchecked count."""
    return parse_lock_full(path)[0]


def probe_osv(lock: pathlib.Path, post=_get_json):
    pkgs, unchecked = parse_lock_full(lock)
    if not pkgs:  # "0 advisories" for a lock nothing was read from is a false all-clear
        raise ValueError("parsed 0 packages from %s: unsupported lock layout or empty lock" % lock)
    vulns = []
    for i in range(0, len(pkgs), 500):
        chunk = pkgs[i : i + 500]
        body = {"queries": [{"package": {"ecosystem": e, "name": n}, "version": v} for e, n, v in chunk]}
        res = post("https://api.osv.dev/v1/querybatch", body)
        if not res or "results" not in res:
            return {"lockfile": lock.name, "packages": len(pkgs), "unchecked": unchecked, "error": "OSV unreachable", "vulnerable": []}
        for (e, n, v), r in zip(chunk, res["results"]):
            ids = [x["id"] for x in r.get("vulns", [])]
            if ids:
                vulns.append({"ecosystem": e, "name": n, "version": v, "ids": ids})
    detail = {}
    for vid in sorted({i for v in vulns for i in v["ids"]})[:200]:
        d = _get_json("https://api.osv.dev/v1/vulns/%s" % vid) or {}
        sev = (d.get("database_specific") or {}).get("severity") or ("CVSS" if d.get("severity") else "?")
        detail[vid] = {
            "severity": sev,
            "summary": (d.get("summary") or "")[:120],
            "aliases": [a for a in d.get("aliases", []) if a.startswith("CVE-")][:2],
        }
    for v in vulns:
        v["advisories"] = [dict(id=i, **detail.get(i, {})) for i in v["ids"]]
        del v["ids"]
    return {"lockfile": lock.name, "packages": len(pkgs), "unchecked": unchecked, "vulnerable": vulns}


# --------------------------------------------------------------------------- output


def _md(cmd, res):
    lines = ["## probe: %s" % cmd, ""]
    if cmd == "release":
        for k, v in res.items():
            if k not in ("mismatches", "compared", "workspaces"):
                lines.append("- **%s**: `%s`" % (k, v))
        if res.get("workspaces"):
            lines += ["", "| member | local | npm | tags | mismatches |", "|---|---|---|---|---|"]
            for r in res["workspaces"]:
                lines.append("| `%s` | %s | %s | %s | %s |" % (
                    r["name"], r["local"], r["registry"] or "unavailable", ", ".join(r["tags"]) or "none",
                    "; ".join(r["mismatches"]) or "none"))  # fmt: skip
        verdict = "" if res["mismatches"] and res["compared"] else ("none" if res["compared"] else "not compared")
        lines += ["", "**Mismatches:** " + verdict]
        lines += ["- " + m for m in res["mismatches"]]
    elif cmd in ("fragments", "leaks"):
        if cmd == "leaks":
            lines.append(
                "Scanned: %s. Hits by kind: %s" % (", ".join(res["scanned"]) or "(none)", res["by_kind"] or "none")
            )
        elif not res["systems"]:
            lines.append(
                "**no fragment system** (no changelog.d/, .changeset/ or NEWS.md%s): nothing was linted."
                % ("; --dir %s/ does not exist" % res["missing_dir"] if res.get("missing_dir") else "")
            )
        else:
            counts = [
                "%s: %d files" % (k, res[k]) for k in ("fragments", "changesets") if k in res
            ] + (
                ["NEWS.md top section %r: %d bullets, %d without a PR/issue ref"
                 % (res["news"]["section"], res["news"]["bullets"], res["news"]["without_ref"])]
                if "news" in res else []
            )  # fmt: skip
            lines.append(
                "Systems: %s. %s. %d findings." % (", ".join(res["systems"]), "; ".join(counts), len(res["findings"]))
            )
        if cmd == "fragments" and res.get("news_unlinted"):
            lines.append("NEWS.md: no version section found, not linted.")
        if res["findings"]:
            lines += [
                "",
                "| file:line | %s |" % ("kind | match" if cmd == "leaks" else "problem"),
                "|---|---|" + ("---|" if cmd == "leaks" else ""),
            ]
        for f in res["findings"]:
            tail = "%s | `%s`" % (f["kind"], f["match"]) if cmd == "leaks" else f["problem"]
            lines.append("| `%s:%d` | %s |" % (f["file"], f["line"], tail))
    elif cmd == "counts":
        lines.append(
            "Nouns quoted with several numbers (leads: verify each against a measured count): "
            + (
                json.dumps(res["nouns_quoted_with_several_numbers"])
                if res["nouns_quoted_with_several_numbers"]
                else "none"
            )
        )
        for noun, hits in sorted(res["by_noun"].items()):
            lines += ["", "### %s" % noun]
            lines += [
                "- `%s:%d` **%d**: %s" % (h["file"], h["line"], h["n"], h["text"].replace("|", "\\|")) for h in hits
            ]
    elif cmd == "osv":
        if res.get("error"):
            lines.append("**%s** (%d packages parsed)" % (res["error"], res["packages"]))
        else:
            lines.append(
                "%d packages in %s, %d with advisories; %d unchecked (git, file, URL or tarball specs, unpinned lines)."
                % (res["packages"], res["lockfile"], len(res["vulnerable"]), res.get("unchecked", 0))
            )
            lines += ["", "| package | version | advisory | severity | summary |", "|---|---|---|---|---|"]
            for v in res["vulnerable"]:
                for a in v["advisories"]:
                    lines.append(
                        "| %s | %s | %s %s | %s | %s |"
                        % (
                            v["name"],
                            v["version"],
                            a["id"],
                            " ".join(a.get("aliases", [])),
                            a.get("severity", "?"),
                            a.get("summary", "").replace("|", "/"),
                        )
                    )
    else:
        lines.append(json.dumps(res, indent=2))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("archetype")
    a.add_argument("repo", nargs="?", default=".")
    r = sub.add_parser("release")
    r.add_argument("repo", nargs="?", default=".")
    r.add_argument("--repo", dest="owner_repo", help="owner/name for gh (default: the checkout's origin)")
    g = r.add_mutually_exclusive_group()
    g.add_argument("--pypi")
    g.add_argument("--cran")
    g.add_argument("--npm")
    g.add_argument("--runiverse", metavar="OWNER", help="r-universe owner; the package name comes from DESCRIPTION")
    g.add_argument("--workspaces", action="store_true", help="npm/pnpm monorepo: compare every published member")
    f = sub.add_parser("fragments")
    f.add_argument("repo", nargs="?", default=".")
    f.add_argument("--dir", default=None, help="fragment dir (default: changelog.d/ when present)")
    f.add_argument("--max-lines", type=int, default=3)
    f.add_argument("--groups", default="breaking,added,changed,deprecated,removed,fixed,security,data")
    lk = sub.add_parser("leaks")
    lk.add_argument("paths", nargs="*")
    lk.add_argument("--root", default=".")
    lk.add_argument(
        "--private", nargs="*", default=None, help="private repo/vendor names (default: %s)" % DEFAULT_PRIVATE
    )
    lk.add_argument("--exclude", nargs="*", default=["*versioned_docs/*"], help="globs on the root-relative path")
    c = sub.add_parser("counts")
    c.add_argument("paths", nargs="*")
    c.add_argument("--root", default=".")
    c.add_argument(
        "--exclude",
        nargs="*",
        default=["*versioned_docs/*", "*/reference/*", "*/superpowers/*"],
        help="globs on the root-relative path (default skips generated reference pages)",
    )
    o = sub.add_parser("osv")
    o.add_argument("lockfile")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "archetype":
            repo = pathlib.Path(args.repo)
            remote = (_run(["git", "-C", str(repo), "remote", "get-url", "origin"]) or "").strip()
            res = dict(probe_archetype(repo, remote), remote=remote)
        elif args.cmd == "release":
            res = probe_release(
                pathlib.Path(args.repo),
                args.owner_repo,
                args.pypi,
                args.cran,
                args.npm,
                args.runiverse,
                args.workspaces,
            )
        elif args.cmd == "fragments":
            res = probe_fragments(
                pathlib.Path(args.repo), args.dir, args.max_lines, [x for x in args.groups.split(",") if x]
            )
        elif args.cmd == "leaks":
            root = pathlib.Path(args.root)
            res = probe_leaks(
                root,
                [pathlib.Path(p) for p in args.paths],
                DEFAULT_PRIVATE if args.private is None else args.private,
                args.exclude,
            )
        elif args.cmd == "counts":
            root = pathlib.Path(args.root)
            res = probe_counts(root, [pathlib.Path(p) for p in args.paths], args.exclude)
        else:
            res = probe_osv(pathlib.Path(args.lockfile))
    except (OSError, ValueError) as exc:
        sys.stderr.write("audit_probes: %s\n" % exc)
        return 2
    out = json.dumps(res, indent=2) + "\n" if args.json else _md(args.cmd, res)
    sys.stdout.buffer.write(out.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
