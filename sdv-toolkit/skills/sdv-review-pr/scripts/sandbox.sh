#!/usr/bin/env bash
# Run PR code (tests, mutations, replays, CLIs) with no network, no secrets, and
# only the review tree writable.
#
#   sandbox.sh <tree> -- <command...>     run <command> inside <tree>
#   sandbox.sh --self-test                prove secrets + network are unreachable
#
# The droplet runs reviews as root next to ~/.Renviron, /root/.sdv-*-key,
# /etc/sdv-db/sdv-db.env, gh/ssh credentials, and a live network. Blocking `gh`
# on PATH stops none of that; this does. Install dependencies BEFORE entering
# (e.g. `uv sync --frozen` in the tree) -- there is no network inside.
#
# Requires bubblewrap (`bwrap`). Without it the script refuses rather than
# running unsandboxed.
set -euo pipefail

die() { echo "sandbox.sh: $*" >&2; exit 2; }
command -v bwrap >/dev/null 2>&1 || die "bwrap not found -- do not run PR code on this host; review statically"

# Toolchains that live under hidden directories, re-exposed read-only.
# (uv-managed CPython builds that every repo venv symlinks into; the uv binary.)
TOOLCHAIN_RO=(/root/.local/share/uv/python /root/.local/bin/uv)

run_sandboxed() {
    local tree="$1"; shift
    local args=(
        --ro-bind / /
        --dev /dev --proc /proc
        --tmpfs /tmp --tmpfs /root --tmpfs /home --tmpfs /etc/sdv-db
        --unshare-net --unshare-pid --die-with-parent
    )
    local p
    for p in "${TOOLCHAIN_RO[@]}"; do
        [ -e "$p" ] && args+=(--ro-bind "$p" "$p")
    done
    args+=(--bind "$tree" "$tree" --chdir "$tree")
    mkdir -p "$tree/.home"
    env -i HOME="$tree/.home" LANG=C.UTF-8 TERM=dumb \
        PATH="$tree/.venv/bin:/root/.local/bin:/mnt/sdv_repos/.node22/bin:/usr/local/bin:/usr/bin:/bin" \
        UV_OFFLINE=1 UV_NO_SYNC=1 UV_CACHE_DIR="$tree/.home/uv-cache" \
        bwrap "${args[@]}" "$@"
}

self_test() {
    mkdir -p /mnt/sdv_repos/tmp/pr-review 2>/dev/null || true
    SELFTEST_TREE="$(mktemp -d /mnt/sdv_repos/tmp/pr-review/.selftest-XXXXXX 2>/dev/null || mktemp -d)"
    trap 'rm -rf "${SELFTEST_TREE:-}"' EXIT
    local tree="$SELFTEST_TREE"
    cat >"$tree/probe.py" <<'PY'
import glob, os, sys, urllib.request
leaks = []
def reachable(label, fn):
    try:
        fn()
        leaks.append(label)
    except Exception:
        pass
def read_any(pattern):
    hits = glob.glob(pattern)
    if not hits:
        raise FileNotFoundError(pattern)
    for h in hits:
        open(h, "rb").read(1)
reachable("/root/.Renviron", lambda: read_any("/root/.Renviron"))
reachable("/root/.sdv-*-key", lambda: read_any("/root/.sdv-*-key"))
reachable("/etc/sdv-db/*.env", lambda: read_any("/etc/sdv-db/*.env"))
reachable("gh hosts.yml", lambda: read_any("/root/.config/gh/hosts.yml"))
reachable("ssh keys", lambda: read_any("/root/.ssh/id_*"))
reachable("network", lambda: urllib.request.urlopen("https://github.com", timeout=5))
reachable("write outside tree", lambda: open("/mnt/sdv_repos/.sandbox_write_probe", "w").write("x"))
open("inside.txt", "w").write("ok")
print("leaks:", leaks or "none", "| env:", sorted(os.environ))
sys.exit(1 if leaks else 0)
PY
    # Positive control: unsandboxed, the same probe must see at least one secret or
    # the network -- otherwise a clean sandbox result proves nothing.
    if (cd "$tree" && python3 probe.py >/dev/null 2>&1); then
        echo "self-test INCONCLUSIVE: nothing is reachable even unsandboxed on this host" >&2
    fi
    rm -f /mnt/sdv_repos/.sandbox_write_probe
    if run_sandboxed "$tree" python3 probe.py; then
        [ -f "$tree/inside.txt" ] || die "self-test FAILED: cannot write inside the tree"
        echo "self-test PASSED"
    else
        rm -f /mnt/sdv_repos/.sandbox_write_probe
        die "self-test FAILED: the sandbox leaks (see above) -- do not run PR code"
    fi
}

[ "${1:-}" = "--self-test" ] && { self_test; exit 0; }
[ $# -ge 3 ] && [ "$2" = "--" ] || die "usage: sandbox.sh <tree> -- <command...> | sandbox.sh --self-test"
tree="$(cd "$1" && pwd)"; shift 2
case "$tree" in
    /|/root|/root/*|/etc|/etc/*) die "refusing to bind $tree writable" ;;
esac
run_sandboxed "$tree" "$@"
