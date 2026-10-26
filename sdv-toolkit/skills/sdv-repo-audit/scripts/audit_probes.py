#!/usr/bin/env python3
"""Mechanical probes for the sdv-repo-audit skill. Stdlib only, read-only.

Each subcommand prints markdown (or JSON with --json) and exits 0 when the probe
ran, 2 on a usage or I/O error. A finding is never an error exit: the auditor
decides what a probe hit means.

    python audit_probes.py archetype [REPO]
    python audit_probes.py release   [REPO] [--repo owner/name] [--pypi NAME] [--cran NAME] [--npm NAME]
    python audit_probes.py fragments [REPO] [--dir changelog.d] [--max-lines 3] [--groups a,b,...]
    python audit_probes.py leaks     [PATH ...] [--root REPO] [--private NAME ...]
    python audit_probes.py counts    [PATH ...] [--root REPO]
    python audit_probes.py osv       LOCKFILE

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


def detect_archetype(repo: pathlib.Path, remote: str = "") -> str:
    """sdv-py | python-package | r-package | producer | web | other, from files on disk and the remote name."""
    repo = pathlib.Path(repo).resolve()  # Path(".").name is ""
    name = remote.rstrip("/").rsplit("/", 1)[-1]
    name = name[:-4] if name.endswith(".git") else name
    if (repo / "tools" / "codegen" / "generate.py").exists():
        return "sdv-py"
    if name.endswith("-raw") or name.endswith("-data") or repo.name.endswith(("-raw", "-data")):
        return "producer"
    if (repo / "DESCRIPTION").exists() and (repo / "R").is_dir():
        return "r-package"
    if (repo / "package.json").exists():
        return "web"
    if (repo / "pyproject.toml").exists():
        return "python-package"
    return "other"


REFERENCE_FOR = {
    "sdv-py": "python-package.md",
    "python-package": "python-package.md",
    "r-package": "r-package.md",
    "producer": "producer.md",
    "web": "web.md",
    "other": "web.md (JS) or python-package.md (Python): pick the closer one and say so",
}


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


def probe_release(repo, owner_repo, pypi, cran, npm):
    local, src = local_version(repo)
    reg_name, registry = None, None
    if pypi:
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
    tags = sorted(
        {
            ln.split("refs/tags/")[1].replace("^{}", "")
            for ln in (ls or "").splitlines()
            if "refs/tags/" in ln and re.search(r"refs/tags/v?\d", ln)
        },
        key=vkey,
    )
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
    mism = compare_release(local, registry, tags if ls is not None else None, latest, None if head_dev else head)
    # every source that was NOT compared is a finding of its own, so "none" can only mean "all compared, all agree"
    if not reg_name:
        mism.append("no registry compared: pass --pypi, --cran or --npm")
    elif registry is None:
        mism.append("%s version unavailable (not published, or the registry was unreachable)" % reg_name)
    if local is None:
        mism.append("local version unreadable (no [project] version, DESCRIPTION Version or package.json version)")
    if ls is None:
        mism.append("git ls-remote failed: tags not compared")
    result["mismatches"] = mism
    result["compared"] = bool(reg_name and registry and local and ls is not None)
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


def probe_fragments(repo, d, max_lines, groups):
    fdir = repo / d
    if not fdir.is_dir():
        return {"dir": d, "present": False, "findings": []}
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
    return {
        "dir": d,
        "present": True,
        "fragments": len([f for f in fdir.glob("*.md") if f.name.lower() != "readme.md"]),
        "findings": findings,
    }


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


def parse_lock(path: pathlib.Path):
    """[(ecosystem, name, version)] from uv.lock, poetry.lock, renv.lock, or package-lock.json. Pure-ish: unit-tested."""
    name = path.name
    if name not in ("uv.lock", "poetry.lock", "renv.lock", "package-lock.json"):
        raise ValueError("unsupported lockfile: %s (uv.lock, poetry.lock, renv.lock, package-lock.json)" % name)
    txt = path.read_text(encoding="utf-8")
    if name in ("uv.lock", "poetry.lock"):
        out = []
        for block in re.split(r"(?m)^\[\[package\]\]\s*$", txt)[1:]:
            n = re.search(r'(?m)^name\s*=\s*"([^"]+)"', block)
            v = re.search(r'(?m)^version\s*=\s*"([^"]+)"', block)
            if n and v and "source = { editable" not in block and "source = { virtual" not in block:
                out.append(("PyPI", n.group(1), v.group(1)))
        return out
    data = json.loads(txt)
    if name == "renv.lock":
        return [
            ("CRAN", k, p.get("Version"))
            for k, p in data.get("Packages", {}).items()
            if p.get("Version") and p.get("Source", "Repository") in ("Repository", "CRAN")
        ]
    out = set()  # package-lock.json: v2/v3 "packages" map, v1 nested "dependencies" tree
    for key, p in (data.get("packages") or {}).items():
        if key and p.get("version") and "node_modules/" in key:
            out.add(("npm", key.rsplit("node_modules/", 1)[1], p["version"]))
    stack = [data.get("dependencies") or {}]
    while stack:
        for dep, p in stack.pop().items():
            if isinstance(p, dict):
                if p.get("version") and not str(p["version"]).startswith(("file:", "link:", "git")):
                    out.add(("npm", dep, p["version"]))
                stack.append(p.get("dependencies") or {})
    return sorted(out)


def probe_osv(lock: pathlib.Path, post=_get_json):
    pkgs = parse_lock(lock)
    if not pkgs:  # "0 advisories" for a lock nothing was read from is a false all-clear
        raise ValueError("parsed 0 packages from %s: unsupported lock layout or empty lock" % lock)
    vulns = []
    for i in range(0, len(pkgs), 500):
        chunk = pkgs[i : i + 500]
        body = {"queries": [{"package": {"ecosystem": e, "name": n}, "version": v} for e, n, v in chunk]}
        res = post("https://api.osv.dev/v1/querybatch", body)
        if not res or "results" not in res:
            return {"lockfile": lock.name, "packages": len(pkgs), "error": "OSV unreachable", "vulnerable": []}
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
    return {"lockfile": lock.name, "packages": len(pkgs), "vulnerable": vulns}


# --------------------------------------------------------------------------- output


def _md(cmd, res):
    lines = ["## probe: %s" % cmd, ""]
    if cmd == "release":
        for k, v in res.items():
            if k not in ("mismatches", "compared"):
                lines.append("- **%s**: `%s`" % (k, v))
        verdict = "" if res["mismatches"] and res["compared"] else ("none" if res["compared"] else "not compared")
        lines += ["", "**Mismatches:** " + verdict]
        lines += ["- " + m for m in res["mismatches"]]
    elif cmd in ("fragments", "leaks"):
        if cmd == "leaks":
            lines.append(
                "Scanned: %s. Hits by kind: %s" % (", ".join(res["scanned"]) or "(none)", res["by_kind"] or "none")
            )
        elif not res["present"]:
            lines.append("No `%s/` directory." % res["dir"])
        else:
            lines.append("%d fragments, %d findings." % (res["fragments"], len(res["findings"])))
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
                "%d packages in %s, %d with advisories." % (res["packages"], res["lockfile"], len(res["vulnerable"]))
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
    f = sub.add_parser("fragments")
    f.add_argument("repo", nargs="?", default=".")
    f.add_argument("--dir", default="changelog.d")
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
            arch = detect_archetype(repo, remote)
            res = {"archetype": arch, "remote": remote, "reference": REFERENCE_FOR[arch]}
        elif args.cmd == "release":
            res = probe_release(pathlib.Path(args.repo), args.owner_repo, args.pypi, args.cran, args.npm)
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
