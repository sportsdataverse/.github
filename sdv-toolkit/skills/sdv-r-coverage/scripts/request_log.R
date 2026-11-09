# Triage wrappers that return 0 rows: log every httr2 request each call makes, its
# status and the response's top-level keys (with array lengths).
#
#   Rscript request_log.R <pkg dir> calls.txt
#
# Read the log as three cases -- each needs a different fix:
#   200 with `items[0]` / `[]`         upstream is empty for these args   -> pick other args, or accept
#   400 / 404                          route or id is dead upstream        -> new id, or report ESPN-side
#   200 with data, function 0 rows     PARSER BUG (renamed key, new route, a warning
#                                      swallowed by tryCatch(warning =))  -> fix the parser
# For the third case, run the wrapper body with warnings surfaced
# (withCallingHandlers(..., warning = function(w) print(w))) before reading the parser.

args <- commandArgs(trailingOnly = TRUE)
suppressMessages(devtools::load_all(args[[1]], quiet = TRUE))
calls <- readLines(args[[2]])
calls <- calls[nzchar(trimws(calls)) & !startsWith(trimws(calls), "#")]

summ <- function(b) {
  if (is.null(b)) return("non-JSON")
  if (is.null(names(b))) return(sprintf("[array of %d]", length(b)))
  n <- names(b)
  cnt <- vapply(n, function(k) if (is.list(b[[k]]) && is.null(names(b[[k]]))) as.character(length(b[[k]])) else "-", "")
  paste(paste0(n, "[", cnt, "]"), collapse = " ")
}

for (call in calls) {
  log <- character()
  out <- httr2::with_mocked_responses(function(req) {
    r <- tryCatch(httr2::req_perform(req, mock = NULL), httr2_http = function(e) e$resp)
    b <- tryCatch(jsonlite::fromJSON(httr2::resp_body_string(r), simplifyVector = FALSE),
                  error = function(e) NULL)
    log <<- c(log, sprintf("    %d %s\n       %s", httr2::resp_status(r),
                           sub("https?://", "", req$url), substr(summ(b), 1, 200)))
    r
  }, tryCatch(suppressMessages(eval(parse(text = call))), error = function(e) e))
  cat(sprintf("%s -> %s\n", call,
              if (is.data.frame(out)) paste(nrow(out), "rows") else class(out)[1]))
  cat(log, sep = "\n")
  cat("\n")
  Sys.sleep(0.2)
}
