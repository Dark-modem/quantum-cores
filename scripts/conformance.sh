#!/usr/bin/env bash
# conformance.sh — CORES-3 contract-conformance gate for Dark-modem/quantum-cores.
#
# Validates EVERY published release against the architect-fixed contract:
#   (a) tag shape <core>-v<2-or-3-segment numeric semver> — udp2raw calver is
#       legal; suffixed / non-numeric / no-v refused. Byte-identical to the
#       panel's coresTagRe (quantum-panel d692ef2 cores_discovery.go:51).
#   (b) asset names <core>-<os>-<arch>.tar.gz with the artifacts-store enums
#       (os=linux, arch amd64|arm64) + .sig companions named <asset>.sig.
#   (c) every tarball has a .sig companion that decodes to a 64-byte ed25519
#       signature — the panel's fetchCoreSig order: RAW-64 untrimmed first
#       (a raw sig may end in a whitespace-valued byte), then trimmed-raw,
#       then base64-std; fail-closed otherwise.
#   (d) MANIFEST.json parity both ways: every release tag is a manifest
#       version, every manifest version is a live release, every asset's
#       sha256 matches the manifest (GitHub API digest field — an asset
#       without a digest cannot prove parity and FAILS), no orphan assets
#       or orphan manifest rows either way.
#   (e) NOTICE.md present in every core folder.
#   (f) NO binaries in the git tree — tracked OR untracked/ignored strays
#       (tarballs/sigs/archives/executables).
#
# FAILS LOUD: one "CONFORMANCE FAIL:" line per violation, exit 1 on any.
# READ-ONLY: never mutates the repo, the releases, or anything else.
#
# Data sources (all read-only):
#   - releases JSON: $CORES_RELEASES_JSON (pre-fetched
#     `gh api --paginate repos/Dark-modem/quantum-cores/releases`),
#     else fetched live via gh;
#   - detached sigs: $CORES_SIG_CACHE_DIR/<tag>/<asset>.sig, else downloaded
#     via gh into a temp cache (removed on exit);
#   - manifests/NOTICE/git tree: this clone ($CORES_DIR overrides the root;
#     a non-git CORES_DIR — fixture mode — skips only check (f), loudly).
#
# Runner scripts in environments without gh auth (e.g. WSL-side gates) must
# prefetch and set CORES_RELEASES_JSON + CORES_SIG_CACHE_DIR — the same
# least-fragile-offline pattern as the release repo's QUANTUM_CORES_DIR.

set -u

CORES_DIR="${CORES_DIR:-}"
[ -n "$CORES_DIR" ] || CORES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$CORES_DIR" || { echo "FATAL: no repo at $CORES_DIR"; exit 2; }

FAILS=0
fail() { echo "CONFORMANCE FAIL: $*"; FAILS=$((FAILS+1)); }
info() { echo "CONFORMANCE INFO: $*"; }

command -v python3 >/dev/null 2>&1 || { echo "FATAL: python3 not found"; exit 2; }

TMPD=""
PYTMP=""
cleanup() { [ -n "$TMPD" ] && rm -rf "$TMPD"; [ -n "$PYTMP" ] && rm -f "$PYTMP"; return 0; }
trap cleanup EXIT

RELJSON="${CORES_RELEASES_JSON:-}"
SIGCACHE="${CORES_SIG_CACHE_DIR:-}"

if [ -z "$RELJSON" ]; then
    command -v gh >/dev/null 2>&1 || { echo "FATAL: no CORES_RELEASES_JSON and no gh to fetch the live releases"; exit 2; }
    TMPD="$(mktemp -d)"
    RELJSON="$TMPD/releases.json"
    gh api --paginate repos/Dark-modem/quantum-cores/releases > "$RELJSON" \
        || { echo "FATAL: gh api releases fetch failed"; exit 2; }
    info "fetched live releases via gh -> $RELJSON"
fi

# (f) NO binaries in the git tree — tracked, untracked, AND ignored strays.
#     A fixture CORES_DIR is not a git repo: skip this check loudly.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    PATS=('*.tar.gz' '*.tgz' '*.zip' '*.sig' '*.b64' '*.sha256' '*.exe' '*.bin' '*.pyc')
    while IFS= read -r f; do
        [ -n "$f" ] && fail "(f) binary TRACKED in git: $f"
    done < <(git ls-files -- "${PATS[@]}")
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        st="${line%% *}"
        p="${line:3}"
        case $p in
            *.tar.gz|*.tgz|*.zip|*.sig|*.b64|*.sha256|*.exe|*.bin) fail "(f) binary in the working tree (status $st): $p" ;;
        esac
    done < <(git status --porcelain=v1 --ignored=matching)
    info "(f) git tree checked: tracked + untracked/ignored (incl. .gitignore'd strays)"
else
    info "(f) SKIPPED — $CORES_DIR is not a git working tree (fixture mode)"
fi

# Prefetch sigs when no cache was given (auto mode needs gh auth).
if [ -z "$SIGCACHE" ]; then
    command -v gh >/dev/null 2>&1 || { echo "FATAL: no CORES_SIG_CACHE_DIR and no gh to fetch sigs"; exit 2; }
    [ -n "$TMPD" ] || TMPD="$(mktemp -d)"
    SIGCACHE="$TMPD/sigs"
    mkdir -p "$SIGCACHE"
    python3 scripts/conformance.py --sig-plan "$RELJSON" > "$TMPD/sigplan.txt" || exit 2
    while IFS=$'\t' read -r TAG NAME ID; do
        TAG="${TAG%$'\r'}"; NAME="${NAME%$'\r'}"; ID="${ID%$'\r'}"
        [ -n "$TAG" ] || continue
        mkdir -p "$SIGCACHE/$TAG"
        gh api -H "Accept: application/octet-stream" "repos/Dark-modem/quantum-cores/releases/assets/$ID" \
            > "$SIGCACHE/$TAG/$NAME" \
            || fail "(c) could not download sig $TAG/$NAME"
    done < "$TMPD/sigplan.txt"
    info "fetched detached sigs via gh -> $SIGCACHE"
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Stream python's FAIL lines through, count them for the exact total
# (the exit code alone cannot carry the count), and keep the transcript.
PYTMP="$(mktemp)"
CORES_DIR="$CORES_DIR" CORES_RELEASES_JSON="$RELJSON" CORES_SIG_CACHE_DIR="$SIGCACHE" \
    python3 "$HERE/conformance.py" "$@" | tee "$PYTMP"
PYEXIT="${PIPESTATUS[0]}"
PYFAILS="$(grep -c '^CONFORMANCE FAIL:' "$PYTMP" || true)"
rm -f "$PYTMP"; PYTMP=""
[ -n "$PYFAILS" ] || PYFAILS=0
FAILS=$((FAILS + PYFAILS))
# python exit 0 = green (PYFAILS==0), 1 = violations (PYFAILS>=1); anything
# else is a crash — count it as one extra violation so the run stays loud.
[ "$PYEXIT" -eq 0 ] || [ "$PYEXIT" -eq 1 ] || FAILS=$((FAILS + 1))

if [ "$FAILS" -gt 0 ]; then
    echo "CONFORMANCE: $FAILS total violation(s) — NOT conformant"
    exit 1
fi
echo "CONFORMANCE: all checks green — releases conform to the contract"
exit 0
