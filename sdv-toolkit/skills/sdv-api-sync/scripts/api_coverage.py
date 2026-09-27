"""Coverage diff: an upstream OpenAPI spec vs the R wrappers in an SDV package.

Usage:
    python api_coverage.py SPEC_JSON R_DIR REPORT_MD SUMMARY_JSON --host HOST --prefix PREFIX

Detects two R idioms for the request path:
  * literal URLs   "https://HOST/path"                                  (cfbfastR)
  * helper calls   .PREFIX_get("/path") | .PREFIX_get(paste0("/p/", id, "/q"))  (hoopR)

Exit codes: 0 = ran (a dirty diff is a RESULT, not an error); 2 = spec unusable
(no paths: a moved host that returns HTML, or an empty document).
Stdlib only: this runs inside a GitHub Actions step with no venv.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

METHODS = {"get", "post", "put", "delete", "patch"}
# R formals are snake_case, spec params camelCase; both fold to lower + no underscores.
# The R side abbreviates a few: map spec-fold -> R-fold explicitly. Anything else that
# differs is reported as drift; do NOT grow this table to hide real gaps.
ALIASES = {"firstname": "first", "lastname": "last"}
IGNORED_FORMALS = {"...", "verbose", "proxy"}
MARKER_RE = re.compile(r"<!--\s*api-sync:\s*version=([0-9][\w.\-]*)\s*-->")
FN_HEAD_RE = re.compile(r"^([A-Za-z0-9_.]+)\s*<-\s*function\s*\(", re.M)


def fold(name: str) -> str:
    return re.sub(r"[_\s]", "", name).lower()


def norm(path: str) -> str:
    """/games/{gameId}/preview -> /games/{}/preview (param names differ per side)."""
    return re.sub(r"\{[^}]*\}", "{}", path)


def load_spec(path):
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    eps = {}
    for p, ops in (spec.get("paths") or {}).items():
        for method, op in ops.items():
            if method.lower() not in METHODS or not isinstance(op, dict):
                continue
            q = [x for x in op.get("parameters", []) if x.get("in") == "query"]
            eps[(method.upper(), p)] = {
                "operationId": op.get("operationId", ""),
                "tags": list(op.get("tags", [])),
                "deprecated": bool(op.get("deprecated", False)),
                "params": [x["name"] for x in q],
                "required": [x["name"] for x in q if x.get("required")],
            }
    if not eps:
        print(f"spec has no paths: {path}", file=sys.stderr)
        sys.exit(2)
    return spec.get("info", {}).get("version", "?"), eps


def _balanced_end(src: str, open_idx: int) -> int:
    """Index of the ')' matching the '(' at open_idx; quote-aware so a ')' inside a
    string literal does not close the call. Returns len(src) if unbalanced."""
    depth, i, in_str = 0, open_idx, None
    while i < len(src):
        ch = src[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == in_str:
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(src)


def _split_top(inner: str) -> list[str]:
    """Split a call's argument text on commas at depth 0 and outside string literals,
    so `f(a = g(1, 2), b = "x,y")` yields two args, not four."""
    parts, depth, cur, in_str = [], 0, "", None
    for ch in inner + ",":
        if in_str:
            cur += ch
            if ch == in_str:
                in_str = None
            continue
        if ch in "\"'":
            in_str = ch
            cur += ch
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return [p for p in parts if p]


def _formals(src: str, open_idx: int) -> list[str]:
    """Formal names from the '(' at open_idx to its balanced ')'. Defaults may
    contain calls (`season = most_recent_mbb_season()`), so split at depth 0 only."""
    inner = src[open_idx + 1 : _balanced_end(src, open_idx)]
    names = [p.split("=", 1)[0].strip() for p in _split_top(inner)]
    return [n for n in names if n and n not in IGNORED_FORMALS]


def _paste_path(inner: str) -> str:
    """paste0("/b/", id, "/c") -> /b/{}/c ; non-literal args (including nested calls
    such as toupper(trimws(team))) become one path param each."""
    out = []
    for arg in _split_top(inner):
        if len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in "\"'":
            out.append(arg[1:-1])
        else:
            out.append("{}")
    return "".join(out)


def scan_r_dir(r_dir, host: str, prefix: str):
    lit = re.compile(r"https://" + re.escape(host) + r"(/[A-Za-z0-9_/{}\-]*)")
    # group 1 = a literal path; no group 1 = a paste0( call whose args are scanned
    # to the balanced ')' (nested calls and commas inside literals are safe).
    helper = re.compile(
        r"\." + re.escape(prefix) + r"_get\(\s*(?:\"(/[^\"]*)\"|paste0\()"
    )
    found = {}
    for f in sorted(Path(r_dir).glob("*.R")):
        src = f.read_text(encoding="utf-8", errors="replace")
        heads = [
            (m.start(), m.group(1), _formals(src, m.end() - 1))
            for m in FN_HEAD_RE.finditer(src)
        ]
        hits = [(m.start(), m.group(1)) for m in lit.finditer(src)]
        hits += [
            (
                m.start(),
                m.group(1)
                or _paste_path(src[m.end() : _balanced_end(src, m.end() - 1)]),
            )
            for m in helper.finditer(src)
        ]
        for pos, p in hits:
            p = p.rstrip("/") or "/"
            if p == "/":
                continue  # a bare host mention in prose, not a wrapper
            fn, formals = "<module>", []
            for start, name, fs in heads:
                if start < pos:
                    fn, formals = name, fs
            found.setdefault(norm(p), []).append(
                {"file": f.name, "fn": fn, "formals": formals, "path": p}
            )
    return found


def diff(eps, r_eps):
    spec_by_norm = {}
    for (m, p), meta in eps.items():
        spec_by_norm.setdefault(norm(p), []).append((m, p, meta))
    missing = [
        {"method": m, "path": p, **meta}
        for (m, p), meta in sorted(
            eps.items(), key=lambda kv: (kv[1]["tags"], kv[0][1])
        )
        if norm(p) not in r_eps
    ]
    dead = [
        {"path": k, "fns": sorted({e["fn"] for e in v})}
        for k, v in sorted(r_eps.items())
        if k not in spec_by_norm
    ]
    drift = []
    for k, entries in sorted(r_eps.items()):
        if k not in spec_by_norm:
            continue
        spec_params = {q for _, _, meta in spec_by_norm[k] for q in meta["params"]}
        for e in entries:
            if e["fn"] == "<module>":
                continue
            fm = {fold(x) for x in e["formals"]}
            absent = sorted(
                q
                for q in spec_params
                if fold(q) not in fm and ALIASES.get(fold(q), fold(q)) not in fm
            )
            if absent:
                drift.append(
                    {
                        "path": k,
                        "fn": e["fn"],
                        "file": e["file"],
                        "missing_params": absent,
                    }
                )
    return {"missing": missing, "dead": dead, "drift": drift}


def render_markdown(version: str, prefix: str, d) -> str:
    L = [f"# {prefix.upper()} {version} vs `{prefix}_*` wrappers", ""]
    L.append(
        f"| missing | dead | drift |\n|---|---|---|\n| {len(d['missing'])} | {len(d['dead'])} | {len(d['drift'])} |\n"
    )
    L.append(f"## Spec endpoints with NO {prefix} wrapper ({len(d['missing'])})\n")
    L.append(
        "| method | path | tag | operationId | query params |\n|---|---|---|---|---|"
    )
    for m in d["missing"]:
        L.append(
            f"| {m['method']} | `{m['path']}` | {','.join(m['tags'])} | {m['operationId']} | {', '.join(m['params'])} |"
        )
    L.append(
        f"\n## Wrapped paths NOT in the spec (removed upstream) ({len(d['dead'])})\n"
    )
    for x in d["dead"]:
        L.append(f"- `{x['path']}` — {', '.join(x['fns'])}")
    L.append(
        f"\n## Param drift: spec query params absent from the R formals ({len(d['drift'])})\n"
    )
    L.append("| path | R fn | file | missing params |\n|---|---|---|---|")
    for x in d["drift"]:
        L.append(
            f"| `{x['path']}` | {x['fn']} | {x['file']} | {', '.join(x['missing_params'])} |"
        )
    return "\n".join(L) + "\n"


def parse_marker(body):
    m = MARKER_RE.search(body or "")
    return m.group(1) if m else None


def _ver(tag: str):
    return tuple(int(x) if x.isdigit() else 0 for x in tag.lstrip("v").split("."))


def releases_between(tags, last_seen, latest):
    """Tags t with last_seen < t <= latest (semver), or just latest on a first run.
    A yanked release (last_seen > latest) yields []; the caller decides 'changed'
    from string inequality, never from this list."""
    hi = _ver(latest)
    if not last_seen:
        return [t for t in tags if _ver(t) == hi]
    lo = _ver(last_seen)
    return [t for t in tags if lo < _ver(t) <= hi]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("spec")
    ap.add_argument("r_dir")
    ap.add_argument("report_md")
    ap.add_argument("summary_json")
    ap.add_argument("--host", required=True)
    ap.add_argument("--prefix", required=True)
    a = ap.parse_args(argv)
    version, eps = load_spec(a.spec)
    d = diff(eps, scan_r_dir(a.r_dir, a.host, a.prefix))
    Path(a.report_md).write_text(
        render_markdown(version, a.prefix, d), encoding="utf-8"
    )
    Path(a.summary_json).write_text(
        json.dumps(
            {
                "version": version,
                "prefix": a.prefix,
                "counts": {k: len(v) for k, v in d.items()},
                **d,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"{a.prefix} {version}: missing={len(d['missing'])} dead={len(d['dead'])} drift={len(d['drift'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
