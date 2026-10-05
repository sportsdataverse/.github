# [SportsDataverse](https://sportsdataverse.org/ "The home page of the SportsDataverse Organization")

**Open sports data for R, Python and JavaScript.** Tidy play-by-play, box scores, schedules, rosters and fitted
models (expected points, win probability, expected goals) for college and pro football, basketball, hockey and
baseball, published by automated pipelines that every package reads from.

[![GitHub stars](https://img.shields.io/github/stars/sportsdataverse?label=stars&logo=github)](https://github.com/sportsdataverse)
[![R-universe packages](https://sportsdataverse.r-universe.dev/badges/:packages)](https://sportsdataverse.r-universe.dev)
[![PyPI downloads](https://img.shields.io/pypi/dm/sportsdataverse?label=PyPI&logo=python&logoColor=white)](https://pypi.org/project/sportsdataverse/)
[![npm downloads](https://img.shields.io/npm/dm/sportsdataverse?label=npm&logo=npm)](https://www.npmjs.com/package/sportsdataverse)

[Website](https://sportsdataverse.org/) · [Data status](https://sportsdataverse.org/status) · [Cheat sheets](https://sportsdataverse.org/cheatsheets) · [R-universe](https://sportsdataverse.r-universe.dev) · [Data releases](https://github.com/sportsdataverse/sportsdataverse-data/releases) · [Join the list](https://sportsdataverse.org/join)

## Data and automation status

Every SportsDataverse loader (`load_cfb_pbp()`, `load_nba_pbp()` and their siblings) reads the
[`sportsdataverse-data`](https://github.com/sportsdataverse/sportsdataverse-data) releases. How fresh each producer's
data is and whether its pipeline is passing is on [sportsdataverse.org/status](https://sportsdataverse.org/status),
rebuilt nightly from [status/ecosystem.md](https://github.com/sportsdataverse/.github/blob/main/status/ecosystem.md).
A league out of season reads **idle**, never red; a badge turns red only when an update run fails after the newest data.

| Data | Pipeline | Updated | Through | Read it with |
| --- | --- | --- | --- | --- |
| **College football** · [ESPN](https://github.com/sportsdataverse/cfbfastR-cfb-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-cfb-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/cfbfastR-cfb-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-cfb-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-cfb-data%2Fthrough.json&label=) | cfbfastR · sportsdataverse-py |
| **College football** · [CollegeFootballData](https://github.com/sportsdataverse/cfbfastR-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/cfbfastR-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FcfbfastR-data%2Fthrough.json&label=) | cfbfastR · sportsdataverse-py |
| **College football** · [stats.ncaa.org](https://github.com/sportsdataverse/ncaa-mfb-football-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mfb-football-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/ncaa-mfb-football-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mfb-football-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mfb-football-data%2Fthrough.json&label=) | cfbfastR · sportsdataverse-py |
| **NFL** · [ESPN](https://github.com/sportsdataverse/nfl-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/nfl-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-data%2Fthrough.json&label=) | sportsdataverse-py |
| **NFL** · [Next Gen Stats](https://github.com/sportsdataverse/nfl-ngs-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-ngs-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/nfl-ngs-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-ngs-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fnfl-ngs-data%2Fthrough.json&label=) | sportsdataverse-py |
| **NBA** · [ESPN](https://github.com/sportsdataverse/hoopR-nba-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/hoopR-nba-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-data%2Fthrough.json&label=) | hoopR · sportsdataverse-py |
| **NBA** · [NBA Stats API](https://github.com/sportsdataverse/hoopR-nba-stats-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-stats-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/hoopR-nba-stats-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-stats-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-nba-stats-data%2Fthrough.json&label=) | hoopR · sportsdataverse-py |
| **Men's college basketball** · [ESPN](https://github.com/sportsdataverse/hoopR-mbb-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-mbb-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/hoopR-mbb-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-mbb-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FhoopR-mbb-data%2Fthrough.json&label=) | hoopR · sportsdataverse-py |
| **Men's college basketball** · [stats.ncaa.org](https://github.com/sportsdataverse/ncaa-mbb-hoops-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mbb-hoops-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/ncaa-mbb-hoops-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mbb-hoops-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-mbb-hoops-data%2Fthrough.json&label=) | hoopR · sportsdataverse-py |
| **WNBA** · [ESPN](https://github.com/sportsdataverse/wehoop-wnba-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/wehoop-wnba-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-data%2Fthrough.json&label=) | wehoop · sportsdataverse-py |
| **WNBA** · [WNBA Stats API](https://github.com/sportsdataverse/wehoop-wnba-stats-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-stats-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/wehoop-wnba-stats-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-stats-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wnba-stats-data%2Fthrough.json&label=) | wehoop · sportsdataverse-py |
| **Women's college basketball** · [ESPN](https://github.com/sportsdataverse/wehoop-wbb-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/wehoop-wbb-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fwehoop-wbb-data%2Fthrough.json&label=) | wehoop · sportsdataverse-py |
| **Women's college basketball** · [stats.ncaa.org](https://github.com/sportsdataverse/ncaa-wbb-hoops-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-wbb-hoops-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/ncaa-wbb-hoops-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-wbb-hoops-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fncaa-wbb-hoops-data%2Fthrough.json&label=) | wehoop · sportsdataverse-py |
| **NHL** · [NHL API](https://github.com/sportsdataverse/fastRhockey-nhl-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-nhl-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/fastRhockey-nhl-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-nhl-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-nhl-data%2Fthrough.json&label=) | fastRhockey · sportsdataverse-py |
| **PWHL** · [HockeyTech](https://github.com/sportsdataverse/fastRhockey-pwhl-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-pwhl-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/fastRhockey-pwhl-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-pwhl-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2FfastRhockey-pwhl-data%2Fthrough.json&label=) | fastRhockey · sportsdataverse-py |
| **MLB and college baseball** · [MLB Stats API, NCAA](https://github.com/sportsdataverse/baseballr-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fbaseballr-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/baseballr-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fbaseballr-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fbaseballr-data%2Fthrough.json&label=) | baseballr · sportsdataverse-py |
| **Reference** · [conferences, divisions, ballparks](https://github.com/sportsdataverse/sdv-reference-data) | [![pipeline status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fsdv-reference-data%2Fstatus.json&label=)](https://github.com/sportsdataverse/sdv-reference-data/actions) | ![data updated](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fsdv-reference-data%2Fupdated.json&label=) | ![through season](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsportsdataverse%2F.github%2Fmain%2Fstatus%2Fbadges%2Fsdv-reference-data%2Fthrough.json&label=) | every R package |

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

<p align="center"><a href='https://r.sportsdataverse.org/'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-hex-wall.png' width='520' alt='The SportsDataverse R package hex wall'/></a></p>

| Package | Covers | Version | Downloads | Cheat sheet |
| --- | --- | --- | --- | --- |
| [sportsdataverse](https://r.sportsdataverse.org/) | The meta-package: installs and loads the core SDV R packages in one call | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/sportsdataverse)](https://sportsdataverse.r-universe.dev/sportsdataverse) | | [PDF](https://sportsdataverse.org/cheatsheets/sportsdataverse-R.pdf) |
| [cfbfastR](https://cfbfastR.sportsdataverse.org/) | College football play-by-play, EPA and win probability (CollegeFootballData, ESPN, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/cfbfastR?label=CRAN)](https://CRAN.R-project.org/package=cfbfastR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/cfbfastR)](https://CRAN.R-project.org/package=cfbfastR) | [PDF](https://sportsdataverse.org/cheatsheets/cfbfastR.pdf) |
| [hoopR](https://hoopR.sportsdataverse.org/) | Men's basketball, NBA and college (NBA Stats API, ESPN, KenPom, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/hoopR?label=CRAN)](https://CRAN.R-project.org/package=hoopR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/hoopR)](https://CRAN.R-project.org/package=hoopR) | [PDF](https://sportsdataverse.org/cheatsheets/hoopR.pdf) |
| [wehoop](https://wehoop.sportsdataverse.org/) | Women's basketball, WNBA and college (WNBA Stats API, ESPN, stats.ncaa.org) | [![CRAN version](https://img.shields.io/cran/v/wehoop?label=CRAN)](https://CRAN.R-project.org/package=wehoop) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/wehoop)](https://CRAN.R-project.org/package=wehoop) | [PDF](https://sportsdataverse.org/cheatsheets/wehoop.pdf) |
| [fastRhockey](https://fastrhockey.sportsdataverse.org/) | Hockey play-by-play and stats (NHL, PWHL, HockeyTech leagues) | [![CRAN version](https://img.shields.io/cran/v/fastRhockey?label=CRAN)](https://CRAN.R-project.org/package=fastRhockey) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/fastRhockey)](https://CRAN.R-project.org/package=fastRhockey) | [PDF](https://sportsdataverse.org/cheatsheets/fastRhockey.pdf) |
| [baseballr](https://BillPetti.github.io/baseballr/) | Baseball data (MLB Stats API, Statcast, FanGraphs, Baseball Reference, NCAA) | [![CRAN version](https://img.shields.io/cran/v/baseballr?label=CRAN)](https://CRAN.R-project.org/package=baseballr) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/baseballr)](https://CRAN.R-project.org/package=baseballr) | [PDF](https://sportsdataverse.org/cheatsheets/baseballr.pdf) |
| [oddsapiR](https://oddsapir.sportsdataverse.org/) | Sportsbook odds (The Odds API) | [![CRAN version](https://img.shields.io/cran/v/oddsapiR?label=CRAN)](https://CRAN.R-project.org/package=oddsapiR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/oddsapiR)](https://CRAN.R-project.org/package=oddsapiR) | [PDF](https://sportsdataverse.org/cheatsheets/oddsapiR.pdf) |
| [cfbseedR](https://cfbseedR.sportsdataverse.org/) | College football season simulation: conference tiebreakers and CFP seeding | [![CRAN version](https://img.shields.io/cran/v/cfbseedR?label=CRAN)](https://CRAN.R-project.org/package=cfbseedR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/cfbseedR)](https://CRAN.R-project.org/package=cfbseedR) | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [cfb4th](https://cfb4th.sportsdataverse.org/) | College football fourth-down decisions | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/cfb4th)](https://sportsdataverse.r-universe.dev/cfb4th) | | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [cfbplotR](https://cfbplotr.sportsdataverse.org/) | College football logos and colors for ggplot2 | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/cfbplotR)](https://sportsdataverse.r-universe.dev/cfbplotR) | | [PDF](https://sportsdataverse.org/cheatsheets/cfbplotR-cfb4th-cfbseedR.pdf) |
| [sdvplotR](https://sdvplotr.sportsdataverse.org/) | **New:** team logos, colors, headshots and themes across leagues for ggplot2, gt and reactable | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/sdvplotR)](https://sportsdataverse.r-universe.dev/sdvplotR) | | |
| [recruitR](https://recruitr.sportsdataverse.org/) | College football recruiting (CollegeFootballData, 247Sports) | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/recruitR)](https://sportsdataverse.r-universe.dev/recruitR) | | |
| [usfootballR](https://usfootballr.sportsdataverse.org/) | MLS and NWSL play-by-play (ESPN) | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/usfootballR)](https://sportsdataverse.r-universe.dev/usfootballR) | | |
| [softballR](https://github.com/sportsdataverse/softballR) | College softball (NCAA, ESPN) | [![R-universe version](https://sportsdataverse.r-universe.dev/badges/softballR)](https://sportsdataverse.r-universe.dev/softballR) | | |
| [sportyR](https://sportyr.sportsdataverse.org/) | Regulation playing surfaces for ggplot2 | [![CRAN version](https://img.shields.io/cran/v/sportyR?label=CRAN)](https://CRAN.R-project.org/package=sportyR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/sportyR)](https://CRAN.R-project.org/package=sportyR) | [PDF](https://sportsdataverse.org/cheatsheets/sportyR.pdf) |
| [mlbplotR](https://camdenk.github.io/mlbplotR/) | MLB logos for ggplot2 and gt | [![CRAN version](https://img.shields.io/cran/v/mlbplotR?label=CRAN)](https://CRAN.R-project.org/package=mlbplotR) | [![CRAN downloads](https://cranlogs.r-pkg.org/badges/grand-total/mlbplotR)](https://CRAN.R-project.org/package=mlbplotR) | [PDF](https://sportsdataverse.org/cheatsheets/mlbplotR.pdf) |

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
| [sportsdataverse](https://py.sportsdataverse.org/) | 29 leagues across ESPN, NBA/WNBA Stats, HockeyTech, stats.ncaa.org, MLB Statcast and more, plus every release loader and the EP/WP models · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf) | [![PyPI version](https://img.shields.io/pypi/v/sportsdataverse?label=PyPI)](https://pypi.org/project/sportsdataverse/) | [![PyPI downloads](https://static.pepy.tech/badge/sportsdataverse)](https://pepy.tech/project/sportsdataverse) |
| [sdvplot](https://sdvplot.sportsdataverse.org/) | **New, pre-release:** team logos, wordmarks, headshots and colors for matplotlib, plotnine and table plots ([source](https://github.com/sportsdataverse/sdvplot)) | not yet on PyPI | |
| [sportypy](https://sportypy.sportsdataverse.org/) | Regulation playing surfaces in Python, the companion to sportyR · [cheat sheet](https://sportsdataverse.org/cheatsheets/sportypy.pdf) | [![PyPI version](https://img.shields.io/pypi/v/sportypy?label=PyPI)](https://pypi.org/project/sportypy/) | [![PyPI downloads](https://static.pepy.tech/badge/sportypy)](https://pepy.tech/project/sportypy) |
| [collegebaseball](https://collegebaseball.readthedocs.io/en/latest/) | College baseball data and analysis (NCAA, Boyd's World) | | |
| [nwslpy](https://github.com/nwslR/nwslpy) | National Women's Soccer League data | | |

[**Documentation**](https://py.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-py.pdf)

## <a href="https://nodejs.org" target="_blank">Node.js modules</a>

<a href='https://www.npmjs.com/package/sportsdataverse'><img src='https://raw.githubusercontent.com/sportsdataverse/.github/main/profile/sdv-js.png' width="18%" min-width="100px" alt="sportsdataverse-js logo"/></a>

[![npm](https://img.shields.io/npm/v/sportsdataverse?style=for-the-badge)](https://js.sportsdataverse.org/)  [![npm](https://img.shields.io/npm/dm/sportsdataverse?style=for-the-badge)](https://www.npmjs.com/package/sportsdataverse)

ESPN, 247Sports and NCAA endpoints for Node.js. [**Documentation**](https://js.sportsdataverse.org/) · [**Cheat sheet (PDF)**](https://sportsdataverse.org/cheatsheets/sportsdataverse-js.pdf)

## Built on the SportsDataverse

- [**Game on Paper**](https://gameonpaper.com/cfb "Game on Paper: live analytics for the modern age") — live college
  football analytics on the same expected-points and win-probability models the packages ship.
- [**sportsdataverse.org/status**](https://sportsdataverse.org/status) — nightly freshness and pipeline health for
  every data producer.
- [**sportsdataverse-data releases**](https://github.com/sportsdataverse/sportsdataverse-data/releases) — the
  parquet, RDS and CSV files behind every `load_*()` function, free to download directly.

## Claude Code plugin

The SportsDataverse ships a [Claude Code](https://claude.com/claude-code) plugin,
**`sdv-toolkit`**, with skills, agents, hooks, and an MCP server encoding the SDV
engineering conventions (codegen-safe edit guards, multi-provider league scaffolding,
returns-schema and docstring auditors, polars 1.x and parser-contract reviewers, and
R pkgdown/roxygen helpers).

```sh
claude plugin marketplace add sportsdataverse/sportsdataverse
claude plugin install sdv-toolkit@sportsdataverse
```

## Cheat sheets

Printable one-page references for every package: the function families, the
loaders, and what each one returns. Free to download, print and hand out; every
sheet ships light and dark on US Letter landscape.

**[Browse them all at sportsdataverse.org/cheatsheets](https://sportsdataverse.org/cheatsheets)**

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

## About the SportsDataverse

The SportsDataverse is led by [Saiem Gilani](https://github.com/saiemgilani), who authors or maintains
most of the packages above with a community of contributors. The first conversation on the SportsDataverse
projects happened at the [Carnegie Mellon Sports Analytics Conference](https://www.stat.cmu.edu/cmsac/conference/2021/)
in 2021, where the paper was selected as the winner of the Data and Software contribution, Open Track, in the
reproducible research competition.

The conference materials can be found here:
  - [Slides](https://saiemgilani.github.io/The_SportsDataverse_Initiative/)
  - [Repository](https://github.com/saiemgilani/The_SportsDataverse_Initiative)
  - [Paper](https://www.stat.cmu.edu/cmsac/conference/2021/assets/pdf/SaiemGilani.pdf)

<h3 align="left">Connect with us:</h3>
<a href="https://x.com/sportsdataverse" target="blank"><img src="https://img.shields.io/twitter/follow/sportsdataverse?color=blue&label=%40sportsdataverse&logo=x&style=for-the-badge" alt="sportsdataverse" /></a> <a href="https://x.com/cfbfastR" target="blank"><img src="https://img.shields.io/twitter/follow/cfbfastR?color=blue&label=%40cfbfastR&logo=x&style=for-the-badge" alt="cfbfastR" /></a> <a href="https://x.com/saiemgilani" target="blank"><img src="https://img.shields.io/twitter/follow/saiemgilani?color=blue&label=%40saiemgilani&logo=x&style=for-the-badge" alt="saiemgilani" /></a>

Get release notes and new-dataset announcements by email: **[sportsdataverse.org/join](https://sportsdataverse.org/join)**

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G0KJ588)

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=38816e14651f&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
