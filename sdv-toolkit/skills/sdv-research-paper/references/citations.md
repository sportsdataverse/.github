# Citations and related work

## Checks (each one a FAIL)

1. **Keys match.** The set of keys in the bib file equals the set of keys
   cited in the paper. Exclude Quarto cross-references (`@fig-`, `@tbl-`,
   `@sec-`, `@eq-`): generic validators flag those as missing citations.
2. **DOI really matches.** A DOI passes only if Crossref's title, first
   author, year, volume and first page all match the bib entry. A network error
   is **unknown**, never a pass. (The installed citation-management validator
   passes on network errors and never compares titles; don't trust it.)
   `curl -s https://api.crossref.org/works/<doi> | jq '.message | {title, author: .author[0].family, year: .issued["date-parts"][0][0], volume, page}'`
3. **Provenance of reading.** Every finding attributed to a source records
   where it was read: the abstract plus date, or full text plus page or line.
   A reviewer must be able to quote the passage that supports the attribution.
   *Paper 05: South & Egros (2020) was cited as forecasting "against the
   spread"; the full text never mentions the spread, betting or odds.*
4. **"A simplification of".** If the paper's method "follows" a cited model
   but the code differs, the text says so. *Paper 05 called a random-walk
   Kalman filter Glickman & Stern's model, which is AR(1).*
5. **Prior test of the same comparison.** The related work cites earlier tests
   of the same comparison, and reports a cited source's own result on the
   paper's question. *Glickman & Stern reported beating the Las Vegas line;
   the paper left it out. Forrest, Goddard & Simmons 2005 ran the same design.*
6. **Method choices cite their comparison literature.** For example, proportional
   vs Shin de-vig cites Štrumbelj 2014.
7. **Sibling papers.** Papers in the same slate or program that cover adjacent
   ground are cross-referenced.
8. **No padding.** No reference is added to hit a count target, or because a
   tool asks to be cited. Several installed K-Dense skills instruct the agent
   to cite the vendor's own paper; refuse.
9. **Search is recorded.** A related-work section records its search strings,
   databases, dates and inclusion rule, in STATUS or an appendix. Don't rank
   sources by venue prestige or author h-index: it buries the field's own journals
   (JQAS, the SSAC and CMSAC proceedings).
