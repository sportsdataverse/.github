# [SportsDataverse](https://sportsdataverse.org/ "The home page of the SportsDataverse Organization")

## Data and automation status

Every SportsDataverse loader reads the `sportsdataverse-data` releases; how fresh each producer's data is and whether its pipeline is passing is on [sportsdataverse.org/status](https://sportsdataverse.org/status), rebuilt nightly from [status/ecosystem.md](https://github.com/sportsdataverse/.github/blob/main/status/ecosystem.md).

[![WBB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fstatus.json&label=WBB)](https://github.com/sportsdataverse/wehoop-wbb-data/actions)
[![WNBA](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-data%2Fstatus.json&label=WNBA)](https://github.com/sportsdataverse/wehoop-wnba-data/actions)
[![MBB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-mbb-data%2Fstatus.json&label=MBB)](https://github.com/sportsdataverse/hoopR-mbb-data/actions)
[![NBA](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-data%2Fstatus.json&label=NBA)](https://github.com/sportsdataverse/hoopR-nba-data/actions)
[![CFB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-cfb-data%2Fstatus.json&label=CFB)](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions)
[![NFL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-data%2Fstatus.json&label=NFL)](https://github.com/sportsdataverse/nfl-data/actions)
[![NHL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-nhl-data%2Fstatus.json&label=NHL)](https://github.com/sportsdataverse/fastRhockey-nhl-data/actions)
[![PWHL](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-pwhl-data%2Fstatus.json&label=PWHL)](https://github.com/sportsdataverse/fastRhockey-pwhl-data/actions)
[![MLB](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fbaseballr-data%2Fstatus.json&label=MLB)](https://github.com/sportsdataverse/baseballr-data/actions)


## R Packages

<a href='https://r.sportsdataverse.org/'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-hex-wall.png' align='right' width='38%' min-width='260px' alt='The SportsDataverse R package hex wall'/></a>

- [{sportsdataverse}](https://sportsdataverse.org/) - The SportsDataverse meta-package for R — loads the core SDV R packages in one call · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportsdataverse-R.pdf)
- [{cfbfastR}](https://cfbfastR.sportsdataverse.org/) - An R package to quickly obtain clean and tidy college football play by play data (Data sources: CollegeFootballData, ESPN) · [cheat sheet](https://sportsdataverse.org/cheatsheets/cfbfastR.pdf)
- [{hoopR}](https://hoopR.sportsdataverse.org/) - A utility to quickly obtain clean and tidy men's · [cheat sheet](https://sportsdataverse.org/cheatsheets/hoopR.pdf)
    basketball play by play data (Data sources: NBA Stats API, ESPN, KenPom)
- [{wehoop}](https://wehoop.sportsdataverse.org/) - A utility to quickly obtain clean and tidy women's · [cheat sheet](https://sportsdataverse.org/cheatsheets/wehoop.pdf)
    basketball play by play data (Data sources: WNBA Stats API, ESPN)
- [{baseballr}](https://BillPetti.github.io/baseballr/) - Provides numerous utilities for acquiring and analyzing · [cheat sheet](https://sportsdataverse.org/cheatsheets/baseballr.pdf)
    baseball data from online sources (Data sources: Baseball Reference, FanGraphs, MLB Stats API, NCAA)
- [{fastRhockey}](https://fastrhockey.sportsdataverse.org/) - A utility to scrape and load hockey play-by-play data and statistics (Data sources: NHL, PWHL) · [cheat sheet](https://sportsdataverse.org/cheatsheets/fastRhockey.pdf)
- [{sportyR}](https://sportyr.sportsdataverse.org/) - Create scaled 'ggplot' representations of playing surfaces. Playing surfaces are drawn pursuant to rule-book specifications. · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportyR.pdf)
- [{ggshakeR}](https://abhiamishra.github.io/ggshakeR/) - Analysis and visualization R package that works with publically available soccer data (Compatible data sources: FB Reference, StatsBomb, Understat)
- [{soccerAnimate}](https://github.com/Dato-Futbol/soccerAnimate) - Create 2D animations of soccer tracking data (Compatible data sources: Metrica Sports, Catapult)
- [{oddsapiR}](https://oddsapir.sportsdataverse.org/) - Access sports odds from the Odds API (Data sources: The Odds API) · [cheat sheet](https://sportsdataverse.org/cheatsheets/oddsapiR.pdf)
- [{mlbplotR}](https://camdenk.github.io/mlbplotR/) - Create 'ggplot2' and 'gt' Visuals with Major League Baseball Logos · [cheat sheet](https://sportsdataverse.org/cheatsheets/mlbplotR.pdf)
- [{cfbplotR}](https://cfbplotr.sportsdataverse.org/) - A set of functions to visualize college football teams in 'ggplot2' · [cheat sheet](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf)
- [{cfb4th}](http://cfb4th.sportsdataverse.org/) - A set of functions to analyze NCAA Football 4th Downs · [cheat sheet](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf)
- [{cfbseedR}](https://cfbseedR.sportsdataverse.org/) - Simulate and evaluate college football seasons: conference tiebreakers, CFP seeding and season simulations (Data sources: cfbfastR, CollegeFootballData) · [cheat sheet](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf)
- [{softballR}](https://github.com/sportsdataverse/softballR) - Scrapes and cleans college softball data (Data sources: NCAA, ESPN)
- [{nwslR}](https://github.com/nwslR/nwslR) - Compiles dataset for the National Women's Soccer League (NWSL)
- [{usfootballR}](https://usfootballr.sportsdataverse.org/) - MLS and NWSL play-by-play data (Data sources: ESPN)
- [{recruitR}](https://recruitr.sportsdataverse.org/) - A college football recruiting package (Data sources: CollegeFootballData, 247sports)
- [{puntr}](https://puntalytics.github.io/puntr) - Package for puntalytics
- [{chessR}](https://jaseziv.github.io/chessR/) - A set of functions to enable users to extract chess game data from popular chess sites (Data sources: Lichess, Chess.com)


## Python Packages <a href="https://pypi.org/user/saiemgilani/" alt="Saiem's Python Packages" target="_blank"> <img src="https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/python-original.svg" alt="python" width="40" height="40"/> </a>

<a href='https://pypi.org/project/sportsdataverse/'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-py-logo.png' style="float:center;margin:20px"  width="18%" min-width="100px"  /></a>

[![PyPI](https://img.shields.io/pypi/v/sportsdataverse?label=sportsdataverse&logo=python&style=for-the-badge)](https://pypi.org/project/sportsdataverse/) <a href='https://pypi.org/project/sportsdataverse/'><img alt="PyPI - Down
loads" src="https://img.shields.io/pypi/dm/sportsdataverse?style=for-the-badge"></a>

[**Documentation**](https://py.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf)

- [sportsdataverse](https://py.sportsdataverse.org/) - The Python package covering 29 leagues across ESPN, NBA/WNBA Stats, HockeyTech, stats.ncaa.org, MLB Statcast and more · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf)
- [sportypy](https://sportypy.sportsdataverse.org/) - Draw regulation playing surfaces in Python, the companion to sportyR · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportypy.pdf)
- [collegebaseball](https://collegebaseball.readthedocs.io/en/latest/) - College baseball data and analysis (Data sources: NCAA, Boyd's World)
- [nwslpy](https://github.com/nwslR/nwslpy) - National Women's Soccer League data in Python

## <a href="https://nodejs.org" target="_blank">Node.js modules</a>

<a href='https://www.npmjs.com/package/sportsdataverse'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-js.png' style="float:center;margin:20px"  width="18%" min-width="100px"/></a>

[![npm](https://img.shields.io/npm/v/sportsdataverse?style=for-the-badge)](https://js.sportsdataverse.org/)  [![npm](https://img.shields.io/npm/dm/sportsdataverse?style=for-the-badge)](https://www.npmjs.com/package/sportsdataverse)
<a href='https://www.npmjs.com/package/sportsdataverse'>[![NPM](https://nodei.co/npm/sportsdataverse.png)](https://npmjs.org/package/sportsdataverse)</a>

[**Documentation**](https://js.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-js.pdf)

## Claude Code plugin

The SportsDataverse ships a [Claude Code](https://claude.com/claude-code) plugin —
**`sdv-toolkit`** — with skills, agents, hooks, and an MCP server encoding the SDV
engineering conventions (codegen-safe edit guards, multi-provider league scaffolding,
returns-schema + docstring auditors, polars-1.x / parser-contract reviewers, and
R pkgdown/roxygen helpers).

```sh
claude plugin marketplace add sportsdataverse/sportsdataverse
claude plugin install sdv-toolkit@sportsdataverse
```

## Cheat sheets

Printable one-page references for every package — the function families, the
loaders, and what each one returns. Free to download, print and hand out; every
sheet ships light and dark on US Letter landscape.

**[Browse them all at sportsdataverse.org/cheatsheets](https://sportsdataverse.org/cheatsheets)**

| Sheet | Covers |
|---|---|
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

## About the SportsDataverse

The first conversation on the SportsDataverse projects happened at the [Carnegie Mellon Sports Analytics Conference](https://www.stat.cmu.edu/cmsac/conference/2021/). The paper our lead engineer, Saiem Gilani, wrote for the conference was selected as the winner for the Data and Software contribution, Open Track for their reproducible research competition.

The conference materials can be found here:
  - [Slides](https://saiemgilani.github.io/The_SportsDataverse_Initiative/)
  - [Repository](https://github.com/saiemgilani/The_SportsDataverse_Initiative)
  - [Paper](https://www.stat.cmu.edu/cmsac/conference/2021/assets/pdf/SaiemGilani.pdf)



<h3 align="left">Connect with us:</h3>
<a href="https://x.com/sportsdataverse" target="blank"><img src="https://img.shields.io/twitter/follow/sportsdataverse?color=blue&label=%40sportsdataverse&logo=x&style=for-the-badge" alt="sportsdataverse" /></a> <a href="https://x.com/cfbfastR" target="blank"><img src="https://img.shields.io/twitter/follow/cfbfastR?color=blue&label=%40cfbfastR&logo=x&style=for-the-badge" alt="cfbfastR" /></a> <a href="https://x.com/saiemgilani" target="blank"><img src="https://img.shields.io/twitter/follow/saiemgilani?color=blue&label=%40saiemgilani&logo=x&style=for-the-badge" alt="saiemgilani" /></a>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G0KJ588)

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=38816e14651f&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
