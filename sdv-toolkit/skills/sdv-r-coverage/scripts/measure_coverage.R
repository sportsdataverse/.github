# Coverage of just the new tests, and a lower bound for the combined number.
#
#   Rscript measure_coverage.R <pkg dir> "<test filter regex>" [ci per-file csv]
#
# The csv is ci_coverage.py --out (file, pct, lines). Combined is a LOWER bound:
# per file it takes max(CI-covered, new-covered) because the two suites overlap.
# Report it as "at least N%" and confirm with the next master coverage run.

args <- commandArgs(trailingOnly = TRUE)
pkg <- normalizePath(args[[1]], winslash = "/")
filter <- args[[2]]
Sys.setenv(NOT_CRAN = "true")

cov <- covr::package_coverage(
  pkg, type = "none", quiet = TRUE,
  code = sprintf(
    'testthat::test_dir("%s/tests/testthat", filter = "%s", load_package = "installed", stop_on_failure = FALSE, reporter = "silent")',
    pkg, filter
  )
)
d <- covr::tally_coverage(cov, by = "line")
per <- aggregate(value ~ filename, d, function(v) c(cov = sum(v > 0), n = length(v)))
per <- data.frame(file = sub(".*?(R/[^/]+)$", "\\1", per$filename),
                  covered = per$value[, "cov"], lines = per$value[, "n"])
cat(sprintf("new tests alone: %.1f%% (%d of %d lines)\n",
            100 * sum(per$covered) / sum(per$lines), sum(per$covered), sum(per$lines)))

if (length(args) >= 3) {
  ci <- utils::read.csv(args[[3]])
  m <- merge(per, ci[, c("file", "pct")], by = "file", all.x = TRUE)
  m$pct[is.na(m$pct)] <- 0
  ci_cov <- round(m$lines * m$pct / 100)
  cat(sprintf("CI before: %.1f%%   combined (lower bound): %.1f%%\n",
              100 * sum(ci_cov) / sum(m$lines),
              100 * sum(pmax(ci_cov, m$covered)) / sum(m$lines)))
}
