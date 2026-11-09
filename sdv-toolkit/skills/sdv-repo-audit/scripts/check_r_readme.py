#!/usr/bin/env python3
"""Check an R package checkout's README.Rmd / README.md against the SDV README standard
(skills/sdv-conventions/references/readme.md).

Usage:
    python check_r_readme.py --repo-dir <clone> --slug owner/repo [--pending-coverage]

Backing (CRAN, R-universe, workflows, cheat sheet, CoC) is resolved live, so a badge is
required exactly when what it reports on exists. Exit 1 on any ERROR; WARN lines don't fail.
check_file() is pure given a ctx dict, so tools/test_check_r_readme.py tests it offline.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path


def http_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "sdv-readme-check"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except Exception:
        return False


COMBINED_SHEETS = [
    "cfbplotR-cfb4th-cfbseedR"
]  # ponytail: hand list; scrape the index if it grows


def combined_sheets(pkg: str) -> list[str]:
    return [n for n in COMBINED_SHEETS if pkg in n.split("-")]


def runiverse_pkgs() -> set[str]:
    url = "https://sportsdataverse.r-universe.dev/api/packages"
    with urllib.request.urlopen(url, timeout=30) as r:
        return {p["Package"] for p in json.load(r)}


def description(repo: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    key = None
    for line in (repo / "DESCRIPTION").read_text(encoding="utf-8").splitlines():
        if line[:1].isspace() and key:
            fields[key] += "\n" + line
        elif ":" in line:
            key, val = line.split(":", 1)
            fields[key] = val.strip()
    return fields


def aut_families(authors_r: str) -> list[str]:
    fams = []
    for call in re.findall(r"person\((.*?)\)\s*[,)]", authors_r, flags=re.S):
        if '"aut"' not in call and "'aut'" not in call:
            continue
        # family = "X", else the second positional string: person("Given", "Family", ...)
        m = re.search(r"""family\s*=\s*["']([^"']+)["']""", call)
        strs = re.findall(r"""["']([^"']*)["']""", call)
        m_val = (
            m.group(1)
            if m
            else (strs[1] if len(strs) > 1 and "@" not in strs[1] else None)
        )
        if m_val:
            fams.append(m_val)
    return fams


REQUIRED_ORDER = [
    ("Installation", r"installation"),
    ("Quick start", r"quick ?start|usage"),
    ("Documentation", r"documentation"),
    ("Companion packages", r"companion packages|plotting and related packages"),
    ("The SportsDataverse", r"the sportsdataverse"),
    ("Follow", r"follow .*sportsdataverse"),
    ("Our Authors", r"our authors"),
    ("Cheat sheet", r"cheat ?sheet"),
    ("Code of Conduct", r"code of conduct"),
    ("Citations", r"citations?"),
    ("License", r"license"),
]


def check_file(path: Path, ctx: dict) -> tuple[list[str], list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    text = path.read_text(encoding="utf-8")
    name = path.name
    pkg, slug = ctx["pkg"], ctx["slug"]

    lines = text.splitlines()
    in_fence = False
    heads: list[tuple[int, str]] = []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,2}) (.*)$", ln)
        if m:
            heads.append((len(m.group(1)), m.group(2).strip()))

    if not heads or heads[0][0] != 1 or not heads[0][1].startswith(f"**{pkg}**"):
        errs.append(f"{name}: first heading must be '# **{pkg}**'")
    elif "<img" not in heads[0][1]:
        warns.append(f"{name}: H1 has no logo image")
    elif not re.search(r"<img[^>]*\balt=", heads[0][1]):
        errs.append(
            f"{name}: H1 logo <img> has no alt text (the link has no other name)"
        )
    for lvl, h in heads:
        if not h.startswith("**"):
            errs.append(f"{name}: heading not bold: {'#' * lvl} {h[:60]}")

    # section order (## only)
    h2 = [
        re.sub(r"[*`]|\[([^\]]*)\]\([^)]*\)", r"\1", h).strip().lower()
        for lvl, h in heads
        if lvl == 2
    ]
    want = [
        (label, rx)
        for label, rx in REQUIRED_ORDER
        if not (label == "Cheat sheet" and not ctx["cheatsheet"])
        and not (label == "Code of Conduct" and not ctx["coc"])
    ]
    pos = []
    for label, rx in want:
        idx = next(
            (
                i
                for i, h in enumerate(h2)
                if re.fullmatch(rx, h) or (label == "Follow" and re.match(rx, h))
            ),
            None,
        )
        if idx is None:
            errs.append(f"{name}: missing section '## **{label}**'")
        else:
            pos.append((idx, label))
    found = [label for _, label in pos]
    ordered = [label for _, label in sorted(pos)]
    if found != ordered:
        errs.append(f"{name}: sections out of order: {ordered} (want {found})")
    if ctx["cheatsheet"] is False and any(re.fullmatch(r"cheat ?sheet", h) for h in h2):
        errs.append(
            f"{name}: Cheat sheet section but sportsdataverse.org/cheatsheets/{pkg}.pdf is not live"
        )

    # badges
    m = re.search(r"<!-- badges: start -->(.*?)<!-- badges: end -->", text, flags=re.S)
    if not m:
        errs.append(f"{name}: no <!-- badges: start/end --> block")
        block = ""
    else:
        block = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S)
    alts = [re.sub(r"\s+", " ", a) for a in re.findall(r"\[!\[([^\]]*)\]", block)]
    has = lambda rx: any(re.search(rx, a, flags=re.I) for a in alts)  # noqa: E731
    expect = {
        "CRAN version": ctx["cran"],
        "CRAN downloads": ctx["cran"],
        "R-universe": ctx["runiverse"],
        "Version-Number": True,
        "R-CMD-check": ctx["wf_check"],
        "Codecov": ctx["wf_cov"],
        "pkgdown": ctx["wf_pkgdown"],
        "License": True,
        "Contributors": True,
        "GitHub stars": True,
        "X Follow": True,
    }
    for badge, needed in expect.items():
        rx = {
            "X Follow": r"x follow|twitter follow",
            # self-hosted shields endpoint badge where Codecov can't be set up (baseballr)
            "Codecov": r"^(codecov|coverage)$",
        }.get(badge, re.escape(badge))
        if needed and not has(rx):
            errs.append(f"{name}: missing badge '{badge}'")
        if not needed and has(rx):
            errs.append(f"{name}: badge '{badge}' has no backing - remove it")
    stage = "stable" if ctx["major"] >= 1 else "experimental"
    if not has(rf"lifecycle:? ?{stage}"):
        errs.append(
            f"{name}: missing badge 'Lifecycle: {stage}' (version {ctx['version']})"
        )

    # links / text
    if re.search(r"https?://(www\.)?twitter\.com", text):
        errs.append(f"{name}: twitter.com link(s) - use x.com")
    if re.search(r"\bon Twitter\b", text):
        errs.append(f"{name}: 'on Twitter' - use 'on X'")
    if re.search(r"github\.com/[^/\s)\"']+/[^/\s)\"']+/stargazers", text):
        errs.append(
            f"{name}: /stargazers link - link the repo root (stargazers 404s logged out)"
        )

    # installation
    inst = re.search(r"^## \*\*Installation\*\*(.*?)(?=^## )", text, flags=re.S | re.M)
    if inst:
        body = inst.group(1)
        if "pak::pak(" not in body:
            errs.append(f"{name}: Installation has no pak::pak() dev install")
        if ctx["cran"] and f'install.packages("{pkg}")' not in body.replace("'", '"'):
            errs.append(f"{name}: Installation has no CRAN install line")
        if ctx["runiverse"] and "sportsdataverse.r-universe.dev" not in body:
            errs.append(f"{name}: Installation has no R-universe install line")
        if (
            "remotes::install_github(" in body
            and 'install.packages("remotes")' not in body
        ):
            errs.append(
                f"{name}: remotes::install_github() fallback without installing remotes first"
            )

    # authors
    auth = re.search(r"^## \*\*Our Authors\*\*(.*?)(?=^## )", text, flags=re.S | re.M)
    if auth:
        for fam in ctx["aut"]:
            if fam.lower() not in auth.group(1).lower():
                warns.append(f"{name}: DESCRIPTION author '{fam}' not in Our Authors")

    return errs, warns, [f"{'#' * l} {h}" for l, h in heads]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", required=True, type=Path)
    ap.add_argument("--slug", required=True)
    ap.add_argument(
        "--pending-coverage",
        action="store_true",
        help="test-coverage.yaml is in an open PR, so the Codecov badge is expected",
    )
    a = ap.parse_args()
    repo = a.repo_dir
    desc = description(repo)
    pkg = desc["Package"]
    version = desc.get("Version", "0")
    wf = repo / ".github" / "workflows"
    names = {p.name for p in wf.glob("*")} if wf.exists() else set()
    ctx = {
        "pkg": pkg,
        "slug": a.slug,
        "version": version,
        "major": int(re.match(r"\d+", version).group()),
        "cran": http_ok(f"https://crandb.r-pkg.org/{pkg}"),
        "runiverse": pkg in runiverse_pkgs(),
        "wf_check": bool({"R-CMD-check.yaml", "R-CMD-check.yml"} & names),
        "wf_cov": bool({"test-coverage.yaml", "test-coverage.yml"} & names)
        or a.pending_coverage,
        "wf_pkgdown": bool({"pkgdown.yaml", "pkgdown.yml"} & names),
        # the PDF may be named after the package, the repo (sportsdataverse-R.pdf), or be a
        # combined sheet naming the package (cfbplotR-cfb4th-cfbseedR.pdf)
        "cheatsheet": any(
            http_ok(f"https://sportsdataverse.org/cheatsheets/{n}.pdf")
            for n in {pkg, a.slug.split("/")[1], *combined_sheets(pkg)}
        ),
        "coc": any(
            (repo / d / f).exists()
            for d in (".", ".github")
            for f in ("CODE_OF_CONDUCT.md", "CODE-OF-CONDUCT.md")
        ),
        "aut": aut_families(desc.get("Authors@R", "")),
    }
    print(
        "backing:",
        {k: v for k, v in ctx.items() if k not in ("aut",)},
        "aut:",
        ctx["aut"],
    )
    all_errs: list[str] = []
    heads_by_file = {}
    for fname in ("README.Rmd", "README.md"):
        p = repo / fname
        if not p.exists():
            all_errs.append(f"{fname}: missing")
            continue
        errs, warns, heads = check_file(p, ctx)
        heads_by_file[fname] = heads
        all_errs += errs
        for w in warns:
            print("WARN ", w)
    if (
        len(heads_by_file) == 2
        and heads_by_file["README.Rmd"] != heads_by_file["README.md"]
    ):
        all_errs.append("README.Rmd and README.md headings differ")
    for e in all_errs:
        print("ERROR", e)
    print("PASS" if not all_errs else f"FAIL ({len(all_errs)} errors)")
    return 1 if all_errs else 0


if __name__ == "__main__":
    sys.exit(main())
