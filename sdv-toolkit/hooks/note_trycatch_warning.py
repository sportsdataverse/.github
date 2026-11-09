#!/usr/bin/env python3
"""PreToolUse(Edit|MultiEdit|Write) note: tryCatch(warning = ) in an R package's R/ code.

A `warning =` handler given to tryCatch() unwinds the call, so any harmless warning
raised while parsing makes the wrapper return its empty default with no error.
baseballr had 126 of these; espn_mlb_team_current_roster() returned 0 rows for every
team (2026-11-09). This only prints a NOTE (exit 0): a handler that substitutes a
fallback value on purpose is legitimate. Code that already resumes with
invokeRestart("muffleWarning") is a calling handler and is not flagged.
Fails open on any parse error.
"""

import json
import re
import sys

TRYCATCH = re.compile(r"\btryCatch\s*\(")
WARN_HANDLER = re.compile(r"\bwarning\s*=\s*function\s*\(")
R_SOURCE = re.compile(r"(^|/)R/[^/]+\.[Rr]$")

NOTE = (
    "NOTE: tryCatch() with a `warning =` handler in R/ -- the handler UNWINDS the call, so a "
    "harmless parse warning returns the empty default with no error. Unless the handler "
    "returns a deliberate fallback value, report it with a calling handler instead: "
    "withCallingHandlers(tryCatch(expr, error = ...), warning = function(w) { report(w); "
    'invokeRestart("muffleWarning") }) or the package\'s .try_catch() '
    "(sdv-r-coverage/templates/utils_try_catch.R; see the sdv-r-reviewer `conditions` lens)."
)


def new_text(tool_input):
    parts = [tool_input.get("content") or "", tool_input.get("new_string") or ""]
    for e in tool_input.get("edits") or []:
        if isinstance(e, dict):
            parts.append(e.get("new_string") or "")
    return "\n".join(parts)


def should_note(payload):
    ti = payload.get("tool_input") or {}
    path = str(ti.get("file_path") or "").replace("\\", "/")
    if not R_SOURCE.search(path):
        return False
    text = new_text(ti)
    if "muffleWarning" in text:
        return False
    return bool(TRYCATCH.search(text) and WARN_HANDLER.search(text))


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0
    try:
        if should_note(payload):
            print(NOTE, file=sys.stderr)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
