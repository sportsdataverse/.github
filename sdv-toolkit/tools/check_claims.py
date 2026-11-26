#!/usr/bin/env python3
"""Report SDV facts in docs that the repo itself does not back.

Two mechanical checks, both report-only:

T1 (F1, function / export names)
    Call-shaped names in docs-like text -- a backticked ``name(`` or
    ``pkg::name``, a roxygen ``[name()]`` link or ``\\code{name()}``, and every
    call in an ``r`` / ``python`` / untagged code fence or roxygen
    ``@examples`` block -- resolved against R ``NAMESPACE`` exports and
    ``R/*.R`` definitions, and against Python ``def`` / ``class`` names and
    ``__all__``. Base R, Python builtins and keywords, names a ``NAMESPACE``
    imports, and (when Rscript is on PATH) the exports of DESCRIPTION
    dependencies also resolve. A name qualified with another package
    (``dplyr::filter``, ``pl.col``) is not checked.

T2 (F5, repo-relative paths)
    Tokens shaped like ``tests/codegen/test_x.py`` or ``R/foo.R`` whose first
    component is a top-level entry of the repo, checked with
    ``git cat-file --batch-check`` (the batch form of ``git cat-file -e``)
    against each ``--path-ref``.

Both skip a token whose sentence says it is planned (future tense) or absent
(negation); an absence phrase in the next sentence also counts, so "...adds
tests/x.py. That file does not exist on main." stays green. Both skip
placeholders (``R/pbp_xyz.R``, ``cfbd_new_endpoint()``) and markdown inside
``<!-- -->``.

T1 also skips a name attributed to other code: a sentence that names another
SDV package, a language or a dataframe library; ``pkg's `name()```; a list item
that opens with another package's link; and the spans chained to one of those
(```hoopR::a()` and `b()```). In Python sources it checks only names shaped like
the repo's own API (snake_case, a first word that starts 3+ public names), since
their docstrings quote maths and the R or JS functions a port follows; in a
repo with no DESCRIPTION the same filter covers its markdown too.

T2 also skips a path the sentence says is written or lives in another repo, one
the repo's ``.gitignore`` covers, one that resolves relative to the doc's own
directory, and one whose parent directory is absent (usually another repo's).

Docs-like text: tracked ``*.md`` / ``*.mdx`` / ``*.Rd`` files, everything under
``.github/``, roxygen ``#'`` lines in ``R/*.R``, and Python docstrings.
Generated paths are skipped (``man/``, pkgdown ``docs/``, ``*_espn_ext.py``,
``docs/docs/**/reference/``, ``docs/versioned_docs/``, files headed ``GENERATED ...
DO NOT EDIT``). ``NEWS.md``, ``CHANGELOG.md`` and planning notes
(``*proposal*``, ``*audit*``, ``*plan*``, ``*spec*``, ...) are checked only in
``--diff`` mode, on the lines the diff adds.

The script never blocks: it exits 0 unless ``--strict`` is passed and it found
something. Standard library only; polars, when importable, adds its own names
to the foreign allowlist.

Usage (from any directory)::

    python check_claims.py --repo ../sdv-py --ref origin/main      # whole files at a ref
    python check_claims.py --repo . --diff origin/main             # lines added since base
    python check_claims.py --repo . --format md --checks T1        # markdown table
"""

from __future__ import annotations

import argparse
import ast
import builtins
import difflib
import json
import keyword
import os
import posixpath
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

DATA = Path(__file__).resolve().parent / "check_claims_data"

DOC_SUFFIXES = (".md", ".mdx", ".Rd")
# Planning and working notes: their names are proposals, not claims (L2 reviews them).
PLANNING_FILES = re.compile(
    r"(?i)(?:^|[-_.])(?:proposals?|roadmap|todo|audit|missing|plans?|specs?|design)"
    r"(?:[-_.]|$)"
)
HISTORY_FILES = re.compile(r"(?i)^(?:news|changelog|history)(?:[-_][\w-]+)?\.mdx?$")
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "renv",
    ".worktrees",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".omc",
    ".superpowers",
}
GENERATED_HEADER = re.compile(r"GENERATED.{0,40}DO NOT EDIT", re.I)

# -- exemptions --------------------------------------------------------------

# Words that make the token's own sentence a statement about absence or change.
NEGATION = re.compile(
    r"\b(?:not|never|no longer|instead of|removed|deleted|renamed|deprecated|"
    r"defunct|formerly|replaced|replaces|superseded|dropped|missing|absent|"
    r"previously|earlier versions?|used to|legacy|retired|"
    r"nonexistent|non-existent|does not exist|doesn't exist|isn't|aren't|"
    r"wasn't|don't|doesn't|didn't|won't|cannot|can't|has no|have no|there is no|"
    r"no such)\b",
    re.I,
)
# Absence stated in the NEXT sentence ("...adds tests/x.py. That file does not exist").
ABSENCE_NEXT = re.compile(
    r"\b(?:does not exist|doesn't exist|do not exist|don't exist|is not on main|"
    r"isn't on main|not on main|not yet on main|no longer exists?|never existed|"
    r"was (?:removed|deleted|renamed|dropped)|has been (?:removed|deleted|renamed))\b",
    re.I,
)
# An example name (T2 only: "For example, `changelog.d/x.fixed.md`"); for T1 an
# example call is still a call a reader will run.
EXAMPLE = re.compile(r"\b(?:for example|for instance|e\.g\.|such as)", re.I)
# A path the sentence says is produced (T2 only): "writes tools/codegen/x.yaml".
OUTPUT = re.compile(
    r"\b(?:writes?|written|writing|outputs?|generates?|generated|emits?|creates?|"
    r"saves?|dumps?|produces?)\b",
    re.I,
)
# A path the sentence places in another repo (T2 only).
OTHER_REPO = re.compile(
    r"\b(?:in|from|of) (?!this |our |the current )"
    r"(?:the |those |these |each |every |other |sibling |a |an )?"
    r"(?:(?!this |our )[\w.-]+ )?repos?\b|\b(?<!this )(?<!our )repo's\b|"
    r"\bcopied (?:[\w-]+ )?from\b",
    re.I,
)
FUTURE = re.compile(
    r"\b(?:(?:will|would|shall|should|to) (?:be )?(?:add|added|write|written|create|"
    r"created|port|ported|land|ship|move|moved|rename|renamed|build|built)|"
    r"planned|planning|plan to|proposed?|proposal|todo|hypothetical|placeholder|"
    r"to be added|to be written|is adding|are adding|being added|should add|"
    r"next step|upcoming|future|(?:once|when|if) .{1,60} lands?|"
    r"not yet|wip)\b",
    re.I,
)

# -- token shapes ------------------------------------------------------------

IDENT = r"[A-Za-z.][\w.]*"
BACKTICK = re.compile(r"(`+)(.+?)\1")
# A span that IS a call: `name(`, `name()`, `pkg::name(x = 1)`; not `http(s)_proxy`.
SPAN_CALL = re.compile(r"^\s*(?:(%s):::?)?(%s)\((?:.*\))?\s*$" % (IDENT, IDENT))
SPAN_QUAL = re.compile(r"(?<![\w.])(%s)(:::?)(%s)" % (IDENT, IDENT))
ROXY_LINK = re.compile(r"\[(?:(%s)::)?(%s)\(\)\]" % (IDENT, IDENT))
RD_CODE = re.compile(r"\\code\{(?:\\link\{)?(?:(%s)::)?(%s)\(" % (IDENT, IDENT))
CODE_CALL = re.compile(r"(?<![\w.$@:\\])(?:(%s)(:::?))?(%s)\(" % (IDENT, IDENT))
# "hoopR's `load_nba_pbp()`": the name belongs to the package named just before it.
POSSESSIVE = re.compile(
    r"\b([A-Za-z][\w.]*)(?:\s*<[^>]*>)?`?_?'s?\s*(?:/\s*[A-Za-z][\w.]*'s?\s*)?$"
)
# "Python `espn_soccer_game_plays()`", "sdvplot-js (`binner()`)": named for another
# language or package right before the span.
LANGUAGE = re.compile(
    r"\b(Python|R|JS|JavaScript|TypeScript|Rust|Julia|[A-Za-z][\w.]*-(?:js|py))"
    r"(?:'s)?\s*\(?\s*$"
)
# A sentence naming another SDV package, a language, or a dataframe library is
# about that other code: its unqualified calls are not checked (T1 only).
FOREIGN_NAMES = (
    "R",
    "Python",
    "JS",
    "JavaScript",
    "TypeScript",
    "polars",
    "pandas",
    "numpy",
    "sdv-py",
    "sportsdataverse-py",
    "sdvplot",
    "sdvplot-js",
    "sdvplotR",
    "sportypy",
    "sportyR",
    "hoopR",
    "wehoop",
    "cfbfastR",
    "baseballr",
    "fastRhockey",
    "nflfastR",
    "nflreadr",
    "nflverse",
    "nflplotR",
    "cfbplotR",
    "cfb4th",
    "nfl4th",
    "f1dataR",
    "toRvik",
    "lubridate",
    "dplyr",
    "tidyr",
    "devtools",
    "roxygen2",
    "testthat",
)
# "`hoopR::a()` and `b()`", "hoopR's `a()` / `b()`": the next span keeps the owner.
CHAIN = re.compile(r"\s*(?:/|,|\+|&|and|or|and/or)\s*")
# "- [sdvplot](url) -- `court_coords()` ...": a list item that opens with another
# package's link (markdown or reST) is about that package.
LINKED_ITEM = re.compile(
    r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[([^\]]+)\]\([^)]*\)|`([^`<]+?)\s*(?:<[^>]*>)?`_|"
    r"\*\*([^*]+)\*\*)"
    r"\s*(?:\S+\s*)?(?:—|–|--|-|:)"
)
COMMIT_LINE = re.compile(
    r"^\s*(?:[0-9a-f]{7,40}\s+)?(?:feat|fix|docs|chore|refactor|test|perf|ci|build|"
    r"style|revert|data|"
    r"release|deps)(?:\([^)]*\))?!?:\s"
)
# Placeholder names in templates and examples: `cfbd_new_endpoint()`, `R/pbp_xyz.R`.
PLACEHOLDER = re.compile(
    r"(?i)(?:^|[_/.])(?:xyz|foo|bar|baz|new|my|your|example|some|fn|func|function|"
    r"pkg|entity|x)"
    r"(?:[_.]|$)"
)
FENCE = re.compile(r"^\s*(?:#'\s*)?(`{3,}|~{3,})\s*\{?\s*([\w+-]*)")
CODE_LANGS = {"", "r", "python", "py", "pycon", "python3", "rout", "splus"}
PATH = re.compile(
    r"(?<![\w/.:~@$<{-])((?:\./)?(?:[\w.-]+/)+[\w.-]+\."
    r"(?:py|R|r|md|mdx|qmd|Rmd|yaml|yml|json|toml|sh|ps1|csv|txt|sql|js|ts|tsv|"
    r"parquet|rds|Rd|cfg|ini))(?::\d+(?:[-:]\d+)*)?(?![\w/*{<]|\.\w)"
)
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+(?=\S)")


@dataclass
class Finding:
    path: str
    line: int
    check: str
    fact: str
    token: str
    message: str
    close: list = field(default_factory=list)


@dataclass
class Token:
    line: int
    kind: str  # "call" | "path"
    name: str
    qualifier: str = ""
    triple: bool = False  # pkg:::name
    in_code: bool = False
    context: str = ""  # own sentence (prose) or own line (code)
    next_context: str = ""


# -- sources -----------------------------------------------------------------


def _git(repo: Path, *args: str, stdin: str | None = None, check: bool = True) -> str:
    # bytes in and out: a text-mode pipe on Windows turns "\n" into "\r\n", and
    # git check-ignore then reads "path\r" and matches nothing
    out = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=stdin.encode("utf-8") if stdin is not None else None,
        capture_output=True,
        check=check,
    )
    return out.stdout.decode("utf-8", "replace")


class Source:
    """Tracked files of a repo, read from a git ref or from the working tree."""

    def __init__(self, repo: Path, ref: str | None):
        self.repo = repo
        self.ref = ref
        self._cache: dict[str, str] = {}
        if ref:
            # -z: git C-quotes non-ASCII paths otherwise
            out = _git(repo, "ls-tree", "-r", "-z", "--name-only", ref)
            self.files = [f for f in out.split("\0") if f]
        else:
            try:
                self.files = [f for f in _git(repo, "ls-files", "-z").split("\0") if f]
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.files = [
                    str(p.relative_to(repo)).replace(os.sep, "/")
                    for p in repo.rglob("*")
                    if p.is_file() and not (set(p.relative_to(repo).parts) & SKIP_DIRS)
                ]
        self.files = [f for f in self.files if not (set(f.split("/")[:-1]) & SKIP_DIRS)]

    def preload(self, paths: list[str]) -> None:
        if not self.ref or not paths:
            return
        todo = [p for p in paths if p not in self._cache]
        if not todo:
            return
        proc = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "--batch"],
            input="".join("%s:%s\n" % (self.ref, p) for p in todo).encode(),
            capture_output=True,
            check=True,
        )
        buf, pos = proc.stdout, 0
        for p in todo:
            nl = buf.index(b"\n", pos)
            header = buf[pos:nl].decode()
            pos = nl + 1
            if header.endswith("missing"):
                self._cache[p] = ""
                continue
            size = int(header.rsplit(" ", 1)[1])
            self._cache[p] = buf[pos : pos + size].decode("utf-8", "replace")
            pos += size + 1

    def read(self, path: str) -> str:
        if path in self._cache:
            return self._cache[path]
        if self.ref:
            self.preload([path])
            return self._cache[path]
        try:
            text = (self.repo / path).read_bytes().decode("utf-8", "replace")
        except OSError:
            text = ""
        self._cache[path] = text
        return text


def path_exists_map(repo: Path, refs: list[str], paths: set[str]) -> dict[str, bool]:
    """True for each path present (blob or tree) at ANY of refs."""
    found = {p: False for p in paths}
    for ref in refs:
        todo = [p for p, ok in found.items() if not ok]
        if not todo:
            break
        out = _git(
            repo,
            "cat-file",
            "--batch-check",
            stdin="".join("%s:%s\n" % (ref, p) for p in todo),
        ).splitlines()
        for p, line in zip(todo, out):
            if not line.endswith("missing"):
                found[p] = True
    return found


def gitignored(repo: Path, paths: set[str]) -> set[str]:
    """Paths the repo's .gitignore covers: local-only files named on purpose."""
    if not paths:
        return set()
    out = _git(
        repo,
        "check-ignore",
        "--no-index",
        "--stdin",
        "-z",
        stdin="".join(p + "\0" for p in sorted(paths)),
        check=False,  # exit 1 means "none ignored"
    )
    return {p for p in out.split("\0") if p}


def top_level(repo: Path, refs: list[str]) -> set[str]:
    names: set[str] = set()
    for ref in refs:
        try:
            names.update(_git(repo, "ls-tree", "--name-only", ref).splitlines())
        except subprocess.CalledProcessError:
            continue
    return names


# -- what the repo defines ---------------------------------------------------


@dataclass
class Names:
    package: str = ""
    exports: set = field(default_factory=set)
    defined: set = field(
        default_factory=set
    )  # R internals, Python defs/classes/__all__
    allowed: set = field(default_factory=set)  # base, builtins, imports, deps
    heads: set = field(default_factory=set)  # qualifiers that mean "this package"
    classes: set = field(default_factory=set)  # Python classes: Class.method resolves
    export_all: bool = False
    prefixes: dict = field(default_factory=dict)  # first snake word -> public names
    data: set = field(default_factory=set)  # R lazy data (data/*.rda)

    def known(self, name: str) -> bool:
        return name in self.exports or name in self.defined or name in self.allowed


R_DEF = re.compile(r"^\s*[`\"']?(%s)[`\"']?\s*(?:<<?-|=)\s*function\b" % IDENT, re.M)
PY_DEF = re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+(\w+)", re.M)
PY_CLASS = re.compile(r"^\s*class\s+(\w+)", re.M)
PY_ASSIGN = re.compile(r"^(\w+)\s*(?::[^=\n]+)?=(?!=)", re.M)
PY_ALL = re.compile(r"__all__\s*(?::[^=]+)?[+]?=\s*[\[(]([^\])]*)[\])]", re.S)


def _r_base() -> set[str]:
    path = DATA / "r_base.txt"
    if not path.exists():
        return set()
    return {
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    }


def _r_dep_exports(desc: str, enabled: bool) -> set[str]:
    if not enabled or not shutil.which("Rscript"):
        return set()
    deps: list[str] = []
    for fld in ("Depends", "Imports", "Suggests", "LinkingTo"):
        m = re.search(r"^%s:\s*(.*?)(?=^\S|\Z)" % fld, desc, re.M | re.S)
        if m:
            for part in m.group(1).split(","):
                name = re.sub(r"\(.*?\)", "", part).strip()
                if name and name != "R":
                    deps.append(name)
    if not deps:
        return set()
    # writeLines ends every name with a newline; cat(sep=) would glue the last
    # export of one package to the first of the next
    code = (
        "for (p in commandArgs(TRUE)) tryCatch("
        "writeLines(getNamespaceExports(p)), error = function(e) NULL)"
    )
    try:
        raw = subprocess.run(
            ["Rscript", "-e", code, *deps], capture_output=True, timeout=120
        ).stdout
        out = raw.decode("utf-8", "replace")
    except Exception as exc:  # report-only: a failed lookup only adds noise
        print(
            "check_claims: note: Rscript dependency lookup failed (%s); "
            "dependency calls may read as misses" % exc,
            file=sys.stderr,
        )
        return set()
    return {ln.strip() for ln in out.splitlines() if ln.strip()}


def _polars_names() -> set[str]:
    try:
        import polars as pl  # type: ignore[import-not-found]
    except Exception:
        return set()
    names: set[str] = set(dir(pl))
    for obj in (pl.DataFrame, pl.LazyFrame, pl.Series, pl.Expr):
        names.update(dir(obj))
    try:
        import polars.testing as plt  # type: ignore[import-not-found]

        names.update(dir(plt))
    except Exception:
        pass
    for ns in ("str", "dt", "list", "arr", "struct", "cat", "name", "bin"):
        names.update(dir(getattr(pl.col("x"), ns, None) or object))
    return {n for n in names if not n.startswith("_")}


def collect_names(src: Source, r_deps: bool) -> Names:
    n = Names()
    files = set(src.files)
    if "DESCRIPTION" in files:
        desc = src.read("DESCRIPTION")
        m = re.search(r"^Package:\s*(\S+)", desc, re.M)
        n.package = m.group(1) if m else ""
        n.allowed |= _r_dep_exports(desc, r_deps)
    if "NAMESPACE" in files or "DESCRIPTION" in files:
        n.allowed |= _r_base()
    if "NAMESPACE" in files:
        ns = src.read("NAMESPACE")
        for fn, args in re.findall(r"^(\w+)\((.*)\)\s*$", ns, re.M):
            parts = [a.strip().strip("\"'`") for a in args.split(",")]
            if fn == "export":
                n.exports.update(p for p in parts if p)
            elif fn == "exportPattern":
                n.export_all = True
            elif fn == "S3method" and len(parts) >= 2:
                n.exports.add(parts[0])
                n.exports.add("%s.%s" % (parts[0], parts[1]))
            elif fn == "importFrom" and len(parts) >= 2:
                n.allowed.update(parts[1:])
    # every tracked R file: test helpers and tools/ scripts are real definitions too
    r_files = [f for f in src.files if re.search(r"\.[Rr]$", f)]
    py_files = [f for f in src.files if f.endswith(".py")]
    src.preload(r_files + py_files)
    for f in r_files:
        n.defined.update(R_DEF.findall(src.read(f)))
    for f in src.files:  # lazy data: `hoopR::teams_links`
        m = re.match(r"data/([\w.]+)\.(?:rda|RData|rds)$", f)
        if m:
            n.defined.add(m.group(1))
            n.data.add(m.group(1))
    if n.export_all:
        n.exports |= n.defined
    for f in py_files:
        text = src.read(f)
        n.defined.update(PY_DEF.findall(text))
        n.classes.update(PY_CLASS.findall(text))
        n.defined.update(PY_ASSIGN.findall(text))
        for body in PY_ALL.findall(text):
            n.defined.update(re.findall(r"[\"'](\w+)[\"']", body))
        parts = f.split("/")
        if len(parts) > 1 and parts[-1] == "__init__.py":
            n.heads.add(parts[0] if parts[0] not in ("src", "python") else parts[1])
    if py_files:
        n.allowed |= set(dir(builtins)) | set(keyword.kwlist) | set(keyword.softkwlist)
        n.allowed |= _polars_names()
    if "sportsdataverse" in n.heads:
        n.heads.add("sdv")  # import sportsdataverse as sdv
    if n.package:
        n.heads.add(n.package)
    n.heads.discard("")
    return n


# -- extraction --------------------------------------------------------------


LOCAL_BINDINGS = (
    re.compile(r"^\s*(?:#'\s*)?(%s)\s*(?:<<?-|=(?!=))" % IDENT, re.M),  # x <- / x =
    re.compile(r"\bdef\s+\w+\(([^)]*)\)"),  # parameters: a callable passed in
    re.compile(r"\bfunction\s*\(([^)]*)\)"),
    re.compile(r"\bimport\s+([\w., ]+)"),  # from m import a, b / import m
    re.compile(r"\bas\s+(\w+)"),
    re.compile(r"\bfor\s+(\w+)\s+in\b"),
)
# Notebook display helpers that tutorials call unqualified.
NOTEBOOK = {"display", "Markdown", "HTML", "Image", "clear_output"}


def local_names(text: str) -> set[str]:
    """Names a file binds itself (defs, assignments, parameters, imports)."""
    names = set(R_DEF.findall(text)) | set(PY_DEF.findall(text)) | NOTEBOOK
    for rx in LOCAL_BINDINGS:
        for m in rx.findall(text):
            names.update(re.findall(r"[A-Za-z_.][\w.]*", m))
    return names


def is_generated(path: str, text: str, files: set[str]) -> bool:
    parts = path.split("/")
    if parts[0] == "man" or path.endswith("_espn_ext.py"):
        return True
    if re.match(r"docs/docs/(?:[^/]+/)?reference/", path) or "/_generated/" in path:
        return True
    if re.match(r"docs/versioned_(?:docs|sidebars)/", path):
        return True  # frozen snapshots of older releases: history, like NEWS.md
    if parts[0] == "docs" and "_pkgdown.yml" in files and "DESCRIPTION" in files:
        return True  # pkgdown output
    return bool(GENERATED_HEADER.search("\n".join(text.splitlines()[:5])))


def doc_segments(path: str, text: str) -> list[tuple[int, str]]:
    """(line number, docs-like text) for every docs-like line of a file."""
    if path.endswith((".md", ".mdx")):
        # blank out <!-- ... --> but keep the line count
        text = re.sub(
            r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S
        )
    lines = text.splitlines()
    if path.endswith(DOC_SUFFIXES) or path.startswith(".github/"):
        return [(i + 1, ln) for i, ln in enumerate(lines)]
    if re.match(r"(?:.*/)?R/[^/]+\.[Rr]$", path):
        return [
            (i + 1, ln.lstrip()[2:])
            for i, ln in enumerate(lines)
            if ln.lstrip().startswith("#'")
        ]
    if path.endswith(".py"):
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            return []
        out: list[tuple[int, str]] = []
        for node in ast.walk(tree):
            if not isinstance(
                node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue
            body = getattr(node, "body", [])
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(getattr(body[0], "value", None), ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                d = body[0]
                for ln in range(d.lineno, (d.end_lineno or d.lineno) + 1):
                    out.append((ln, lines[ln - 1]))
        return sorted(set(out))
    return []


def _units(segments: list[tuple[int, str]]):
    """Split docs text into prose units (paragraph / list item) and code lines.

    Yields ("code", [(line, text)]) or ("prose", [(line, text)]).
    """
    fence: str | None = None
    code_ok = False
    roxy_examples = False
    unit: list[tuple[int, str]] = []
    prev_line = None
    for ln, text in segments:
        if prev_line is not None and ln != prev_line + 1:
            # a gap (code between roxygen blocks, a new docstring) resets all state
            fence, roxy_examples = None, False
            if unit:
                yield "prose", unit
                unit = []
        prev_line = ln
        m = FENCE.match(text)
        if m:
            if unit:
                yield "prose", unit
                unit = []
            if fence is None:
                fence = m.group(1)[0]
                code_ok = m.group(2).lower() in CODE_LANGS
            elif m.group(1)[0] == fence:
                fence = None
            continue
        if fence is not None:
            if code_ok:
                yield "code", [(ln, text)]
            continue
        tag = re.match(r"\s*@(\w+)", text)
        if tag:
            roxy_examples = tag.group(1) in ("examples", "examplesIf")
            if unit:
                yield "prose", unit
                unit = []
            if roxy_examples:
                continue
        if roxy_examples:
            yield "code", [(ln, text)]
            continue
        stripped = text.strip()
        if text.lstrip().startswith(">>>") or text.lstrip().startswith("... "):
            if unit:
                yield "prose", unit
                unit = []
            yield "code", [(ln, re.sub(r"^\s*(?:>>>|\.\.\.)\s?", "", text))]
            continue
        new_item = (
            not stripped
            or re.match(r"(?:[-*+]|\d+[.)]|#{1,6}|\|)\s", stripped)
            or stripped.startswith("|")
        )
        if new_item and unit:
            yield "prose", unit
            unit = []
        if stripped:
            unit.append((ln, text))
    if unit:
        yield "prose", unit


def _sentences(unit: list[tuple[int, str]]):
    """[(start offset, end offset, sentence)] plus a char offset -> line map."""
    joined, starts = "", []
    for ln, text in unit:
        starts.append((len(joined), ln))
        joined += text + " "
    bounds, pos = [], 0
    for m in SENTENCE_END.finditer(joined):
        bounds.append((pos, m.start()))
        pos = m.end()
    bounds.append((pos, len(joined)))
    sents = [(a, b, joined[a:b]) for a, b in bounds]

    def line_at(off: int) -> int:
        line = starts[0][1]
        for s, ln in starts:
            if s <= off:
                line = ln
            else:
                break
        return line

    return joined, sents, line_at


def foreign_mention(own: frozenset) -> re.Pattern:
    names = sorted((n for n in FOREIGN_NAMES if n not in own), key=len, reverse=True)
    return re.compile(r"(?<![\w-])(?:%s)(?![\w-])" % "|".join(map(re.escape, names)))


def extract(
    segments: list[tuple[int, str]], roxygen: bool, own: frozenset = frozenset()
) -> list[Token]:
    tokens: list[Token] = []
    mentions = foreign_mention(own)
    for kind, unit in _units(segments):
        if kind == "code":
            ln, text = unit[0]
            code = re.sub(r"\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'", '""', text)
            code = code.split("#", 1)[0] if not text.lstrip().startswith("#") else ""
            if COMMIT_LINE.match(text):
                code = ""  # a commit subject, not a call
            for m in CODE_CALL.finditer(code):
                # exemptions read the code with strings and comments blanked, so
                # stop("not found") does not exempt the calls on its line
                tokens.append(
                    Token(
                        ln,
                        "call",
                        m.group(3),
                        m.group(1) or "",
                        m.group(2) == ":::",
                        True,
                        code,
                    )
                )
            for m in PATH.finditer(text):
                tokens.append(Token(ln, "path", m.group(1), in_code=True, context=text))
            continue
        joined, sents, line_at = _sentences(unit)
        linked = LINKED_ITEM.match(unit[0][1])
        owner_item = linked and (linked.group(1) or linked.group(2) or linked.group(3))
        foreign_item = bool(owner_item) and owner_item.strip() not in own
        for idx, (a, b, sent) in enumerate(sents):
            nxt = sents[idx + 1][2] if idx + 1 < len(sents) else ""
            found: list[tuple[int, str, str, bool]] = []
            about_other = bool(mentions.search(sent))
            prev_end, prev_foreign = -1, False
            for bm in BACKTICK.finditer(sent):
                span = bm.group(2)
                before = sent[: bm.start()]
                owner = POSSESSIVE.search(before) or LANGUAGE.search(before)
                qual = SPAN_QUAL.match(span)
                chained = prev_foreign and CHAIN.fullmatch(sent[prev_end : bm.start()])
                foreign = bool(
                    foreign_item
                    or (about_other and not (qual and qual.group(1) in own))
                    or (owner and owner.group(1) not in own)
                    or (qual and qual.group(1) not in own)
                    or chained
                )
                prev_end, prev_foreign = bm.end(), foreign
                if foreign:
                    continue  # another package's function, attributed in prose
                cm = SPAN_CALL.match(span)
                if cm:
                    found.append(
                        (bm.start(), cm.group(2), cm.group(1) or "", ":::" in span)
                    )
                else:
                    for qm in SPAN_QUAL.finditer(span):
                        found.append(
                            (bm.start(), qm.group(3), qm.group(1), qm.group(2) == ":::")
                        )
            if roxygen:
                for rx in (ROXY_LINK, RD_CODE):
                    for rm in rx.finditer(sent):
                        found.append(
                            (rm.start(), rm.group(2), rm.group(1) or "", False)
                        )
            for off, name, qual, triple in found:
                tokens.append(
                    Token(
                        line_at(a + off), "call", name, qual, triple, False, sent, nxt
                    )
                )
            for pm in PATH.finditer(sent):
                tokens.append(
                    Token(
                        line_at(a + pm.start()),
                        "path",
                        pm.group(1),
                        context=sent,
                        next_context=nxt,
                    )
                )
    return tokens


def exempt(tok: Token) -> bool:
    if FUTURE.search(tok.context) or NEGATION.search(tok.context):
        return True
    if tok.kind == "path" and (
        OUTPUT.search(tok.context)
        or OTHER_REPO.search(tok.context)
        or EXAMPLE.search(tok.context)
    ):
        return True  # a file the code writes, or one in another repo
    return bool(tok.next_context and ABSENCE_NEXT.search(tok.next_context))


def sdv_shaped(name: str, prefixes: dict[str, int]) -> bool:
    """A snake_case name whose first word starts several public names of this repo.

    Python docstrings quote maths (`Phi()`), the R or JS function a port follows
    (`saveRDS()`, `toMatchSnapshot()`) and polars/pandas methods; only a name shaped
    like this repo's own API (`nhl_web_boxscore`) is checked there.
    """
    if not re.fullmatch(r"[a-z][a-z0-9]*_[a-z0-9_]+", name):
        return False
    return prefixes.get(name.split("_", 1)[0], 0) >= 3


# -- resolution --------------------------------------------------------------


def resolve_call(tok: Token, names: Names) -> bool | None:
    """True resolved, False miss, None not checkable (foreign or a variable)."""
    name = tok.name.rstrip(".")
    if len(name) < 2 or name.startswith("."):
        return None
    if tok.qualifier:
        if tok.qualifier not in names.heads:
            return None  # another package: qualification is the allowlist
        if tok.triple:
            return names.known(name)
        if names.package and not names.export_all:
            # R: pkg::name needs an export (or lazy data); internals need :::
            return name in names.exports or name in names.data
        return name in names.exports or name in names.defined
    if names.known(name):
        return True
    if "." in name:
        head, _, rest = name.partition(".")
        last = rest.rsplit(".", 1)[-1]
        if head in names.heads or head in names.classes:
            return names.known(last) if last else None
        return None
    return False


def check_file(
    path: str,
    text: str,
    names: Names,
    checks: set[str],
    roots: set[str],
    local_defs: set[str],
) -> tuple[list[Finding], set[str]]:
    findings: list[Finding] = []
    wanted_paths: set[str] = set()
    roxygen = bool(re.match(r"(?:.*/)?R/[^/]+\.[Rr]$", path))
    python_doc = path.endswith(".py") or not names.package
    # the package's own language is not "another language" (an R doc says "R `x()`")
    own_names = set(names.heads) | ({"R"} if names.package else {"Python"})
    if "sportsdataverse" in own_names:
        own_names |= {"sdv-py", "sportsdataverse-py"}
    own = frozenset(own_names)
    for tok in extract(doc_segments(path, text), roxygen, own):
        if exempt(tok):
            continue
        if tok.kind == "call" and "T1" in checks:
            # a doc's own binding covers only unqualified calls: `pkg::helper()`
            # still has to be an export of pkg
            local = not tok.qualifier and tok.name in local_defs
            if local or PLACEHOLDER.search(tok.name):
                continue
            ok = resolve_call(tok, names)
            if ok is False and python_doc and not tok.qualifier:
                # sdv.load_x() is shaped by load_x, not by the alias in front
                if not sdv_shaped(tok.name.rsplit(".", 1)[-1], names.prefixes):
                    continue
            if ok is False:
                pool = names.exports | names.defined
                shown = (
                    "%s::%s" % (tok.qualifier, tok.name) if tok.qualifier else tok.name
                )
                findings.append(
                    Finding(
                        path,
                        tok.line,
                        "T1",
                        "F1",
                        shown + "()",
                        "not exported or defined by this repo (not indexed)",
                        difflib.get_close_matches(tok.name, sorted(pool), 3, 0.75),
                    )
                )
        elif tok.kind == "path" and "T2" in checks:
            p = tok.name[2:] if tok.name.startswith("./") else tok.name
            stem = p.rsplit(".", 1)[0]
            placeholder = PLACEHOLDER.search(stem) or len(stem.rsplit("/", 1)[-1]) < 2
            if p.split("/", 1)[0] in roots and not placeholder:
                wanted_paths.add(p)
                findings.append(Finding(path, tok.line, "T2", "F5", p, "", []))
    return findings, wanted_paths


# -- driver ------------------------------------------------------------------


def added_lines(repo: Path, base: str) -> dict[str, set[int]]:
    # pin the output shape: user diff config (noprefix, external diff, textconv)
    # must not change the prefixes or the line numbers
    out = _git(
        repo,
        "diff",
        "--unified=0",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        "--src-prefix=a/",
        "--dst-prefix=b/",
        "%s...HEAD" % base,
    )
    added: dict[str, set[int]] = {}
    cur = None
    prev = ""
    for line in out.splitlines():
        if line.startswith("+++ ") and prev.startswith("--- "):
            cur = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            start, count = int(m.group(1)), int(m.group(2) or 1)
            added.setdefault(cur, set()).update(range(start, start + count))
        prev = line
    return added


def run(args: argparse.Namespace) -> list[Finding]:
    repo = Path(args.repo).resolve()
    checks = {c.strip().upper() for c in args.checks.split(",")}
    # --diff reads HEAD, the same tree its line numbers come from
    src = Source(repo, "HEAD" if args.diff else args.ref)
    files = set(src.files)
    names = collect_names(src, args.r_deps)
    for extra_file in args.names_file or []:
        # names a static scan cannot see (wrappers a factory builds at import time)
        text = Path(extra_file).read_text(encoding="utf-8")
        names.defined.update(ln.strip() for ln in text.splitlines() if ln.strip())
    for public in names.exports | names.defined:
        if "_" in public.strip("_") and not public.startswith("_"):
            head = public.split("_", 1)[0]
            names.prefixes[head] = names.prefixes.get(head, 0) + 1

    path_refs = list(args.path_ref or [])
    if not path_refs:
        path_refs = [args.ref] if args.ref and not args.diff else ["HEAD"]
        for extra in ("origin/main", "origin/master"):
            try:
                _git(repo, "rev-parse", "--verify", "-q", extra)
                if extra not in path_refs:
                    path_refs.append(extra)
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    try:
        roots = top_level(repo, path_refs) if "T2" in checks else set()
    except FileNotFoundError:
        roots = set()

    added = added_lines(repo, args.diff) if args.diff else None
    candidates = [
        f
        for f in src.files
        if f.endswith(DOC_SUFFIXES + (".py",))
        or f.startswith(".github/")
        or re.match(r"R/[^/]+\.[Rr]$", f)
    ]
    if args.paths:
        wanted = []
        for raw in args.paths:
            w = posixpath.normpath(raw.replace("\\", "/")).rstrip("/")
            wanted.append("" if w == "." else w)  # "." is the whole repo
        candidates = [
            f
            for f in candidates
            if any(not w or f == w or f.startswith(w + "/") for w in wanted)
        ]
    if added is not None:
        candidates = [f for f in candidates if f in added]
    src.preload(candidates)

    findings: list[Finding] = []
    all_paths: set[str] = set()
    for f in sorted(candidates):
        base = f.rsplit("/", 1)[-1]
        if (
            added is None
            and f.endswith((".md", ".mdx"))
            and (
                HISTORY_FILES.match(base)
                or PLANNING_FILES.search(base.rsplit(".", 1)[0])
            )
        ):
            continue
        text = src.read(f)
        if not text or is_generated(f, text, files):
            continue
        local = local_names(text)
        got, paths = check_file(f, text, names, checks, roots, local)
        if added is not None:
            got = [g for g in got if g.line in added.get(f, set())]
        findings.extend(got)
        all_paths |= paths

    if all_paths:
        exists = path_exists_map(repo, path_refs, all_paths)
        missing = {p for p, ok in exists.items() if not ok}
        parents = {p.rsplit("/", 1)[0] for p in missing}
        parent_ok = path_exists_map(repo, path_refs, parents) if parents else {}
        ignored = gitignored(repo, missing)
        # a path written relative to the doc's own directory ("tests/x.R" in
        # examples/automation/README.md) resolves there
        rel = {
            (g.path, g.token): posixpath.normpath(
                posixpath.join(posixpath.dirname(g.path), g.token)
            )
            for g in findings
            if g.check == "T2" and g.token in missing and "/" in g.path
        }
        rel_ok = path_exists_map(repo, path_refs, set(rel.values())) if rel else {}
        kept = []
        for g in findings:
            if g.check != "T2":
                kept.append(g)
            elif (
                g.token in missing
                and g.token not in ignored
                and parent_ok.get(g.token.rsplit("/", 1)[0])
                and not rel_ok.get(rel.get((g.path, g.token), ""), False)
            ):
                # a missing file in a directory that exists is a stale name; a
                # missing directory is usually another repo's path, so it is skipped
                g.message = "path not found at %s" % " or ".join(path_refs)
                g.close = difflib.get_close_matches(g.token, sorted(files), 3, 0.8)
                kept.append(g)
        findings = kept
    return findings


def render(findings: list[Finding], fmt: str) -> str:
    if fmt == "json":
        return json.dumps([asdict(f) for f in findings], indent=2)
    if fmt == "md":
        rows = [
            "| # | file:line | check | token | message | close matches |",
            "|---|---|---|---|---|---|",
        ]
        for i, f in enumerate(findings, 1):
            rows.append(
                "| %d | `%s:%d` | %s/%s | `%s` | %s | %s |"
                % (
                    i,
                    f.path,
                    f.line,
                    f.check,
                    f.fact,
                    f.token,
                    f.message,
                    ", ".join("`%s`" % c for c in f.close) or "-",
                )
            )
        return "\n".join(rows)
    lines = []
    for f in findings:
        close = " (close: %s)" % ", ".join(f.close) if f.close else ""
        lines.append(
            "%s:%d: %s/%s %s: %s%s"
            % (f.path, f.line, f.check, f.fact, f.token, f.message, close)
        )
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=".", help="repo to check (default: cwd)")
    ap.add_argument(
        "--ref", help="read files at this git ref instead of the working tree"
    )
    ap.add_argument(
        "--diff", metavar="BASE", help="report only lines added since BASE...HEAD"
    )
    ap.add_argument(
        "--path-ref", action="append", help="ref(s) T2 resolves paths against"
    )
    ap.add_argument("--checks", default="T1,T2", help="comma list of T1,T2")
    ap.add_argument(
        "--names-file",
        action="append",
        help="extra defined names, one per line (e.g. dir() of every module)",
    )
    ap.add_argument("--format", choices=("text", "md", "json"), default="text")
    ap.add_argument(
        "--no-r-deps",
        dest="r_deps",
        action="store_false",
        help="skip the Rscript lookup of DESCRIPTION dependency exports",
    )
    ap.add_argument(
        "--strict", action="store_true", help="exit 1 when anything is found"
    )
    ap.add_argument("paths", nargs="*", help="limit to these files or directories")
    return ap


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    strict = "--strict" in argv
    try:  # a cp1252 console must not turn a non-ASCII token into a crash
        sys.stdout.reconfigure(errors="backslashreplace")  # type: ignore[union-attr]
    except Exception:
        pass
    try:
        args = parser().parse_args(argv)
    except SystemExit as exc:  # bad usage is reported, never a block
        return int(exc.code or 0) if strict else 0
    try:
        findings = run(args)
        out = render(findings, args.format)
        if out:
            print(out)
    except Exception as exc:  # report-only: a broken check never blocks
        print("check_claims: error: %s" % exc, file=sys.stderr)
        return 1 if args.strict else 0
    print("check_claims: %d finding(s)" % len(findings), file=sys.stderr)
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
