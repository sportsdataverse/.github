# Automated Profiling

Tools for fast, comprehensive dataset profiling.

## Overview

Automated profiling tools generate complete dataset summaries in seconds, including:
- Type inference and cardinality
- Distribution statistics
- Missing value patterns
- Correlation analysis
- Alerts for potential issues

## Tools

### ydata-profiling (recommended)

```python
from ydata_profiling import ProfileReport

profile = ProfileReport(df, title="Dataset Profile")
profile.to_file("profile_report.html")
```

### Sweetviz

```python
import sweetviz as sv

report = sv.analyze(df)
report.show_html("sweetviz_report.html")
```

### D-Tale

```python
import dtale

d = dtale.show(df)
d.open_browser()
```

## When to use

- First look at a new dataset
- Data quality assessment
- Sharing dataset overview with team
- Documenting dataset characteristics

## Tradeoffs

| Tool | Speed | Detail | Output Format | Best For |
|------|-------|--------|---------------|----------|
| ydata-profiling | Medium | High | HTML | Comprehensive reports |
| Sweetviz | Fast | Medium | HTML | Quick comparisons |
| D-Tale | Fast | Medium | Web UI | Interactive exploration |

## References

- [ydata-profiling Docs](https://docs.profiling.ydata.ai/)
- [Sweetviz GitHub](https://github.com/fbdesignpro/sweetviz)
- [D-Tale GitHub](https://github.com/man-group/dtale)
