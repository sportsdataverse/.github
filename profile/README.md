<p align="center">
  <a href="https://sportsdataverse.org/" title="The home page of the SportsDataverse Organization"><img src="https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-gh.png" width="640" alt="SportsDataverse"/></a>
</p>

<p align="center">
  <b>Open sports data for R, Python and JavaScript.</b><br/>
  Tidy play-by-play, box scores, schedules, rosters and fitted models (expected points, win probability, expected goals)
  for college and pro football, basketball, hockey and baseball, published by automated pipelines that every package reads from.
</p>

<p align="center">
  <a href="https://github.com/sportsdataverse"><img src="https://img.shields.io/github/followers/sportsdataverse?label=Follow&logo=github&logoColor=white&style=for-the-badge" alt="GitHub followers"/></a>
  <a href="https://github.com/sportsdataverse"><img src="https://img.shields.io/github/stars/sportsdataverse?label=Stars&logo=github&logoColor=white&style=for-the-badge" alt="GitHub stars"/></a>
  <a href="https://bsky.app/profile/sportsdataverse.org"><img src="https://img.shields.io/bluesky/followers/sportsdataverse.org?logo=bluesky&label=Bluesky&logoColor=white&style=for-the-badge" alt="Bluesky followers"/></a>
  <a href="https://x.com/sportsdataverse"><img src="https://img.shields.io/badge/%40sportsdataverse-000000?logo=x&logoColor=white&style=for-the-badge" alt="Follow on X"/></a>
  <br/>
  <a href="https://sportsdataverse.r-universe.dev"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fecosystem%2Fcran-downloads.json&style=for-the-badge" alt="CRAN downloads"/></a>
  <a href="https://pepy.tech/project/sportsdataverse"><img src="https://img.shields.io/pepy/dt/sportsdataverse?label=PyPI%20downloads&logo=python&logoColor=white&color=blue&style=for-the-badge" alt="PyPI downloads"/></a>
  <a href="https://www.npmjs.com/package/sportsdataverse"><img src="https://img.shields.io/npm/dt/sportsdataverse?label=npm%20downloads&logo=npm&color=blue&style=for-the-badge" alt="npm downloads"/></a>
  <a href="https://sportsdataverse.r-universe.dev"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages&query=%24.length&label=r-universe%20packages&logo=r&color=blue&style=for-the-badge" alt="R-universe packages"/></a>
</p>

<p align="center">
  <a href="https://sportsdataverse.org/">Website</a> ·
  <a href="https://sportsdataverse.org/cheatsheets">Cheat sheets</a> ·
  <a href="https://sportsdataverse.r-universe.dev">R-universe</a> ·
  <a href="https://github.com/sportsdataverse/sportsdataverse-data/releases">Data releases</a> ·
  <a href="https://sportsdataverse.org/status">Data status</a> ·
  <a href="https://sportsdataverse.org/join">Join the list</a> ·
  <a href="https://www.patreon.com/sportsdataverse">Patreon</a>
</p>

## Get started

```r
# R: the whole family from R-universe (the core packages are also on CRAN)
install.packages("sportsdataverse",
  repos = c("https://sportsdataverse.r-universe.dev", "https://cloud.r-project.org"))
pbp <- cfbfastR::load_cfb_pbp(2025)
```

```python
# Python: pip install sportsdataverse
from sportsdataverse.cfb import load_cfb_pbp
pbp = load_cfb_pbp(seasons=[2025])  # a polars DataFrame; return_as_pandas=True for pandas
```

```sh
# Node.js
npm install sportsdataverse
```

## R Packages

<p align="center"><a href='https://r.sportsdataverse.org/'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-hex-wall.png' width='560' alt='The SportsDataverse R package hex wall'/></a></p>

| Package | Covers | Version | Downloads | Cheat sheet |
| --- | --- | --- | --- | --- |
| [sportsdataverse](https://r.sportsdataverse.org/) | The meta-package: installs and loads the core SDV R packages in one call | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2Fsportsdataverse&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/sportsdataverse) | | [PDF](https://sportsdataverse.org/cheatsheets/sportsdataverse-R.pdf) |
| [cfbfastR](https://cfbfastR.sportsdataverse.org/) | College football play-by-play, EPA and win probability (CollegeFootballData, ESPN, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/cfbfastR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=cfbfastR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FcfbfastR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=cfbfastR) | [PDF](https://sportsdataverse.org/cheatsheets/cfbfastR.pdf) |
| [hoopR](https://hoopR.sportsdataverse.org/) | Men's basketball, NBA and college (NBA Stats API, ESPN, KenPom, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/hoopR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=hoopR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FhoopR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=hoopR) | [PDF](https://sportsdataverse.org/cheatsheets/hoopR.pdf) |
| [wehoop](https://wehoop.sportsdataverse.org/) | Women's basketball, WNBA and college (WNBA Stats API, ESPN, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/wehoop?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=wehoop) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2Fwehoop&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=wehoop) | [PDF](https://sportsdataverse.org/cheatsheets/wehoop.pdf) |
| [fastRhockey](https://fastrhockey.sportsdataverse.org/) | Hockey play-by-play and stats (NHL, PWHL, HockeyTech leagues) | [![CRAN version](https://img.shields.io/cran/v/fastRhockey?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=fastRhockey) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FfastRhockey&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=fastRhockey) | [PDF](https://sportsdataverse.org/cheatsheets/fastRhockey.pdf) |
| [baseballr](https://BillPetti.github.io/baseballr/) | Baseball data (MLB Stats API, Statcast, FanGraphs, Baseball Reference, NCAA) | [![CRAN version](https://img.shields.io/cran/v/baseballr?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=baseballr) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2Fbaseballr&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=baseballr) | [PDF](https://sportsdataverse.org/cheatsheets/baseballr.pdf) |
| [oddsapiR](https://oddsapir.sportsdataverse.org/) | Sportsbook odds (The Odds API) | [![CRAN version](https://img.shields.io/cran/v/oddsapiR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=oddsapiR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FoddsapiR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=oddsapiR) | [PDF](https://sportsdataverse.org/cheatsheets/oddsapiR.pdf) |
| [cfbseedR](https://cfbseedR.sportsdataverse.org/) | College football season simulation: conference tiebreakers and CFP seeding | [![CRAN version](https://img.shields.io/cran/v/cfbseedR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=cfbseedR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FcfbseedR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=cfbseedR) | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [cfb4th](https://cfb4th.sportsdataverse.org/) | College football fourth-down decisions | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2Fcfb4th&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/cfb4th) | | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [cfbplotR](https://cfbplotr.sportsdataverse.org/) | College football logos and colors for ggplot2 | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2FcfbplotR&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/cfbplotR) | | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [sdvplotR](https://sdvplotr.sportsdataverse.org/) | **New:** team logos, wordmarks, headshots and colors across leagues for ggplot2, gt and reactable | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2FsdvplotR&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/sdvplotR) | | |
| [recruitR](https://recruitr.sportsdataverse.org/) | College football recruiting (CollegeFootballData, 247Sports) | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2FrecruitR&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/recruitR) | | |
| [usfootballR](https://usfootballr.sportsdataverse.org/) | MLS and NWSL play-by-play (ESPN) | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2FusfootballR&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/usfootballR) | | |
| [softballR](https://github.com/sportsdataverse/softballR) | College softball (NCAA, ESPN) | [![R-universe version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsportsdataverse.r-universe.dev%2Fapi%2Fpackages%2FsoftballR&query=%24.Version&label=r-universe&logo=r&color=blue&style=for-the-badge)](https://sportsdataverse.r-universe.dev/softballR) | | |
| [sportyR](https://sportyr.sportsdataverse.org/) | Regulation playing surfaces for ggplot2 | [![CRAN version](https://img.shields.io/cran/v/sportyR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=sportyR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FsportyR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=sportyR) | [PDF](https://sportsdataverse.org/cheatsheets/sportyR.pdf) |
| [mlbplotR](https://camdenk.github.io/mlbplotR/) | MLB logos for ggplot2 and gt | [![CRAN version](https://img.shields.io/cran/v/mlbplotR?label=CRAN&style=for-the-badge)](https://CRAN.R-project.org/package=mlbplotR) | [![CRAN downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcranlogs.r-pkg.org%2Fdownloads%2Ftotal%2F2012-10-01%3Alast-day%2FmlbplotR&query=%24%5B0%5D.downloads&label=downloads&color=blue&style=for-the-badge)](https://CRAN.R-project.org/package=mlbplotR) | [PDF](https://sportsdataverse.org/cheatsheets/mlbplotR.pdf) |

Community packages in the family:
[ggshakeR](https://abhiamishra.github.io/ggshakeR/) (soccer analysis and visuals: FBref, StatsBomb, Understat) ·
[soccerAnimate](https://github.com/Dato-Futbol/soccerAnimate) (2D animations of soccer tracking data) ·
[nwslR](https://github.com/nwslR/nwslR) (National Women's Soccer League datasets) ·
[puntr](https://puntalytics.github.io/puntr) (puntalytics) ·
[chessR](https://jaseziv.github.io/chessR/) (Lichess and Chess.com game data).
All of them install from [sportsdataverse.r-universe.dev](https://sportsdataverse.r-universe.dev).

## Python Packages <a href="https://pypi.org/user/saiemgilani/" alt="Saiem's Python Packages" target="_blank"> <img src="https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/python-original.svg" alt="python" width="40" height="40"/> </a>

<a href='https://pypi.org/project/sportsdataverse/'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-py-logo.png' width="18%" min-width="100px" alt="sportsdataverse-py logo"/></a>

| Package | Covers | Version | Downloads |
| --- | --- | --- | --- |
| [sportsdataverse](https://py.sportsdataverse.org/) | 29 leagues across ESPN, NBA/WNBA Stats, HockeyTech, stats.ncaa.org, MLB Statcast and more, plus every release loader and the EP/WP models · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf) | [![PyPI version](https://img.shields.io/pypi/v/sportsdataverse?label=PyPI&style=for-the-badge)](https://pypi.org/project/sportsdataverse/) | [![PyPI downloads](https://img.shields.io/pepy/dt/sportsdataverse?label=downloads&color=blue&style=for-the-badge)](https://pepy.tech/project/sportsdataverse) |
| [sdvplot](https://sdvplot.sportsdataverse.org/) | **New, pre-release:** team logos, wordmarks, headshots and colors for matplotlib, plotnine and table plots ([source](https://github.com/sportsdataverse/sdvplot)) | not yet on PyPI | |
| [sportypy](https://sportypy.sportsdataverse.org/) | Regulation playing surfaces in Python, the companion to sportyR · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportypy.pdf) | [![PyPI version](https://img.shields.io/pypi/v/sportypy?label=PyPI&style=for-the-badge)](https://pypi.org/project/sportypy/) | [![PyPI downloads](https://img.shields.io/pepy/dt/sportypy?label=downloads&color=blue&style=for-the-badge)](https://pepy.tech/project/sportypy) |
| [collegebaseball](https://collegebaseball.readthedocs.io/en/latest/) | College baseball data and analysis (NCAA, Boyd's World) | | |
| [nwslpy](https://github.com/nwslR/nwslpy) | National Women's Soccer League data | | |

[**Documentation**](https://py.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf)

## <a href="https://nodejs.org" target="_blank">Node.js modules</a>

<a href='https://www.npmjs.com/package/sportsdataverse'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-js.png' width="18%" min-width="100px" alt="sportsdataverse-js logo"/></a>

[![npm](https://img.shields.io/npm/v/sportsdataverse?style=for-the-badge)](https://js.sportsdataverse.org/)  [![npm](https://img.shields.io/npm/dm/sportsdataverse?style=for-the-badge)](https://www.npmjs.com/package/sportsdataverse)

ESPN, 247Sports and NCAA endpoints for Node.js. [**Documentation**](https://js.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-js.pdf)

## Data releases and status

Every `load_*()` function reads the automated
[`sportsdataverse-data` releases](https://github.com/sportsdataverse/sportsdataverse-data/releases), free to download
directly. Freshness and pipeline health for every producer are on
**[sportsdataverse.org/status](https://sportsdataverse.org/status)**, rebuilt nightly. Out of season a league reads *idle*
rather than *stale*; red means its update pipeline failed.

[![CFB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-cfb-data%2Fstatus.json&label=CFB&style=for-the-badge)](https://sportsdataverse.org/status)
[![NFL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-data%2Fstatus.json&label=NFL&style=for-the-badge)](https://sportsdataverse.org/status)
[![NBA](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-data%2Fstatus.json&label=NBA&style=for-the-badge)](https://sportsdataverse.org/status)
[![MBB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-mbb-data%2Fstatus.json&label=MBB&style=for-the-badge)](https://sportsdataverse.org/status)
[![WNBA](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-data%2Fstatus.json&label=WNBA&style=for-the-badge)](https://sportsdataverse.org/status)
[![WBB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fstatus.json&label=WBB&style=for-the-badge)](https://sportsdataverse.org/status)
[![NHL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-nhl-data%2Fstatus.json&style=for-the-badge&label=NHL)](https://sportsdataverse.org/status)
[![PWHL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-pwhl-data%2Fstatus.json&label=PWHL&style=for-the-badge)](https://sportsdataverse.org/status)
[![MLB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fbaseballr-data%2Fstatus.json&label=MLB&style=for-the-badge)](https://sportsdataverse.org/status)

## Built on the SportsDataverse

- [**Game on Paper**](https://gameonpaper.com/cfb "Game on Paper: live analytics for the modern age"): live college
  football analytics on the same expected-points and win-probability models the packages ship.
- [**sdv-toolkit**](https://github.com/sportsdataverse/.github/tree/main/sdv-toolkit): a [Claude Code](https://claude.com/claude-code)
  plugin with skills, agents, hooks and an MCP server encoding the SDV engineering conventions (codegen-safe edit guards,
  multi-provider league scaffolding, returns-schema and docstring auditors, polars 1.x and parser-contract reviewers,
  R pkgdown/roxygen helpers).

  ```sh
  claude plugin marketplace add sportsdataverse/sportsdataverse
  claude plugin install sdv-toolkit@sportsdataverse
  ```

## Contributors

Thank you to everyone who has filed an issue, sent a fix or added a league.

<a href="https://github.com/sportsdataverse/sportsdataverse-py/graphs/contributors"><img src="https://contrib.rocks/image?repo=sportsdataverse/sportsdataverse-py&max=48&columns=16" alt="sportsdataverse-py contributors"/></a>
<a href="https://github.com/sportsdataverse/hoopR/graphs/contributors"><img src="https://contrib.rocks/image?repo=sportsdataverse/hoopR&max=48&columns=16" alt="hoopR contributors"/></a>
<a href="https://github.com/sportsdataverse/cfbfastR/graphs/contributors"><img src="https://contrib.rocks/image?repo=sportsdataverse/cfbfastR&max=48&columns=16" alt="cfbfastR contributors"/></a>
<a href="https://github.com/sportsdataverse/wehoop/graphs/contributors"><img src="https://contrib.rocks/image?repo=sportsdataverse/wehoop&max=48&columns=16" alt="wehoop contributors"/></a>

## Cheat sheets

Printable one-page references for every package: the function families, the loaders, and what each one returns. Free to
download, print and hand out; every sheet ships light and dark on US Letter landscape.
**[Browse them all at sportsdataverse.org/cheatsheets](https://sportsdataverse.org/cheatsheets)**

<details><summary>Every sheet</summary>

| Sheet | Covers |
| --- | --- |
| [sportsdataverse (R)](https://sportsdataverse.org/cheatsheets/sportsdataverse-R.pdf) | the R metapackage |
| [sportsdataverse (Python)](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf) | the Python package, 6 pages |
| [sportsdataverse (Node.js)](https://sportsdataverse.org/cheatsheets/sportsdataverse-js.pdf) | the JavaScript client |
| [cfbfastR](https://sportsdataverse.org/cheatsheets/cfbfastR.pdf) | college football |
| [hoopR](https://sportsdataverse.org/cheatsheets/hoopR.pdf) | men's basketball, NBA + NCAA |
| [wehoop](https://sportsdataverse.org/cheatsheets/wehoop.pdf) | women's basketball, WNBA + NCAA |
| [baseballr](https://sportsdataverse.org/cheatsheets/baseballr.pdf) | baseball |
| [fastRhockey](https://sportsdataverse.org/cheatsheets/fastRhockey.pdf) | hockey, NHL + PWHL |
| [oddsapiR](https://sportsdataverse.org/cheatsheets/oddsapiR.pdf) | sportsbook odds |
| [cfbplotR · cfb4th · cfbseedR](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) | the college football toolkit |
| [sportyR](https://sportsdataverse.org/cheatsheets/sportyR.pdf) | playing surfaces in R |
| [sportypy](https://sportsdataverse.org/cheatsheets/sportypy.pdf) | playing surfaces in Python |
| [mlbplotR](https://sportsdataverse.org/cheatsheets/mlbplotR.pdf) | MLB logos for ggplot2 + gt |

</details>

## About the SportsDataverse

The SportsDataverse is led by [Saiem Gilani](https://github.com/saiemgilani), who authors or maintains most of the
packages above with a community of contributors. The first conversation on the SportsDataverse projects happened at the
[Carnegie Mellon Sports Analytics Conference](https://www.stat.cmu.edu/cmsac/conference/2021/) in 2021, where the paper
was selected as the winner of the Data and Software contribution, Open Track, in the reproducible research competition:
[Slides](https://saiemgilani.github.io/The_SportsDataverse_Initiative/) ·
[Repository](https://github.com/saiemgilani/The_SportsDataverse_Initiative) ·
[Paper](https://www.stat.cmu.edu/cmsac/conference/2021/assets/pdf/SaiemGilani.pdf)

## Connect with us

<a href="https://bsky.app/profile/sportsdataverse.org"><img src="https://img.shields.io/badge/Bluesky-%40sportsdataverse.org-0285FF?logo=bluesky&logoColor=white&style=for-the-badge" alt="Bluesky @sportsdataverse.org"/></a>
<a href="https://x.com/sportsdataverse"><img src="https://img.shields.io/badge/%40sportsdataverse-000000?logo=x&logoColor=white&style=for-the-badge" alt="X @sportsdataverse"/></a>
<a href="https://x.com/cfbfastR"><img src="https://img.shields.io/badge/%40cfbfastR-000000?logo=x&logoColor=white&style=for-the-badge" alt="X @cfbfastR"/></a>
<a href="https://sportsdataverse.org/join"><img src="https://img.shields.io/badge/Newsletter-join-2b6cb0?logo=maildotru&logoColor=white&style=for-the-badge" alt="Join the newsletter"/></a>

Release notes and new-dataset announcements by email: **[sportsdataverse.org/join](https://sportsdataverse.org/join)**

[![Become a member on Patreon](https://img.shields.io/badge/Patreon-become%20a%20member-F96854?logo=patreon&logoColor=white&style=for-the-badge)](https://www.patreon.com/sportsdataverse)
[![Support on Ko-fi](https://img.shields.io/badge/Ko--fi-support-FF5E5B?logo=kofi&logoColor=white&style=for-the-badge)](https://ko-fi.com/G2G0KJ588)

[![DigitalOcean referral](https://img.shields.io/badge/DigitalOcean-referral-0080FF?logo=digitalocean&logoColor=white&style=for-the-badge)](https://www.digitalocean.com/?refcode=38816e14651f&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
