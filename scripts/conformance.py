#!/usr/bin/env python3
"""CORES-3 contract-conformance gate for Dark-modem/quantum-cores (helper).

Every published release must satisfy the architect-fixed contract; any drift
prints one "CONFORMANCE FAIL:" line and the run exits 1. Read-only: parses
the releases JSON, the local MANIFEST.json files, and the cached detached
sigs — it never writes, never mutates the repo or the releases.

Called by scripts/conformance.sh (which resolves data sources and owns the
git-tree check (f)); env:
    CORES_DIR             repo root (core folders + MANIFEST.json/NOTICE.md)
    CORES_RELEASES_JSON   `gh api --paginate repos/Dark-modem/quantum-cores/releases`
    CORES_SIG_CACHE_DIR   <tag>/<asset>.sig detached-signature cache

Special mode: `conformance.py --sig-plan <releases.json>` prints the
tag<TAB>asset<TAB>asset-id rows the caller needs to prefetch sigs (auto mode).
"""
import base64
import json
import os
import re
import sys

# The ONLY tag shape — byte-identical to the panel's coresTagRe
# (quantum-panel d692ef2 internal/panel/cores_discovery.go:51, TestCoresTagShape):
# 2-or-3 numeric segments (frp-v0.61.1, udp2raw-v20230206.0 calver);
# suffixed / non-numeric / no-v refused; anchored so a parsed tag can never
# carry path separators or spaces into a download URL.
CORE_TAG_RE = re.compile(r"^([a-z][a-z0-9_-]*)-v(\d+\.\d+(\.\d+)?)$")

# Asset contract shapes with the artifacts-store os/arch enums (the store
# packs linux only; arch names are Go arch names, matching the packs).
ASSET_RE = re.compile(r"^([a-z][a-z0-9_-]*)-linux-(amd64|arm64)\.tar\.gz$")
SIG_RE = re.compile(r"^([a-z][a-z0-9_-]*)-linux-(amd64|arm64)\.tar\.gz\.sig$")
STORE_OSARCH = ("linux-amd64", "linux-arm64")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
SIG_BYTES = 64  # ed25519

fails = 0


def FAIL(msg):
    global fails
    print("CONFORMANCE FAIL: " + msg)
    fails += 1


def decode_sig(data):
    """Panel fetchCoreSig order (d692ef2 cores_discovery.go): RAW-64 untrimmed
    FIRST (a raw signature may legitimately END in a whitespace-valued byte —
    nothing may be trimmed before this check), then the trailing-newline case
    (trimmed line of 64 raw bytes), then base64-std of the trimmed line.
    Anything else is refused (fail-closed). Returns the 64 bytes or None."""
    if len(data) == SIG_BYTES:
        return data
    line = data.decode("utf-8", "replace").strip()
    if len(line) == SIG_BYTES:
        return line.encode("utf-8")
    try:
        sig = base64.b64decode(line, validate=True)
    except Exception:
        return None
    if len(sig) == SIG_BYTES:
        return sig
    return None


def sig_plan(rels_path):
    """--sig-plan: tag<TAB>name<TAB>asset-id for every .sig asset."""
    with open(rels_path, encoding="utf-8") as f:
        rels = json.load(f)
    for r in rels:
        if r.get("draft"):
            continue
        for a in r.get("assets") or []:
            if SIG_RE.match(a.get("name", "")):
                print("%s\t%s\t%s" % (r["tag_name"], a["name"], a["id"]))
    return 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--sig-plan":
        return sig_plan(sys.argv[2])
    repo = os.environ["CORES_DIR"]
    rels_path = os.environ["CORES_RELEASES_JSON"]
    sigdir = os.environ["CORES_SIG_CACHE_DIR"]

    with open(rels_path, encoding="utf-8") as f:
        rels = json.load(f)

    # Core folders + manifests.
    manifests = {}
    for entry in sorted(os.listdir(repo)):
        mf_path = os.path.join(repo, entry, "MANIFEST.json")
        if os.path.isdir(os.path.join(repo, entry)) and os.path.isfile(mf_path):
            try:
                with open(mf_path, encoding="utf-8") as f:
                    manifests[entry] = json.load(f)
            except ValueError as e:
                FAIL("(d) %s/MANIFEST.json is not valid JSON: %s" % (entry, e))

    # (e) NOTICE.md in every core folder.
    for core in sorted(manifests):
        if not os.path.isfile(os.path.join(repo, core, "NOTICE.md")):
            FAIL("(e) %s/NOTICE.md missing" % core)

    # (a) tag shape over EVERY published release.
    live_tags = {}
    for r in rels:
        if r.get("draft"):
            print("CONFORMANCE INFO: draft release skipped: %s" % r.get("tag_name", "?"))
            continue
        tag = r.get("tag_name", "")
        m = CORE_TAG_RE.match(tag)
        if not m:
            FAIL("(a) release tag %r is not contract-shaped <core>-v<2-or-3-segment numeric semver>" % tag)
            continue
        live_tags[tag] = (m.group(1), r)

    # (b)(c)(d) per-release checks.
    for tag, (core, r) in sorted(live_tags.items()):
        tballs = {}
        sigs = {}
        for a in r.get("assets") or []:
            n = a.get("name", "")
            if ASSET_RE.match(n):
                tballs[n] = a
            elif SIG_RE.match(n):
                sigs[n] = a
            else:
                FAIL("(b) release %s asset %r does not match <core>-linux-<amd64|arm64>.tar.gz[.sig] (store enums)" % (tag, n))
        for n in sorted(tballs):
            if n + ".sig" not in sigs:
                FAIL("(c) release %s: no .sig companion for %s" % (tag, n))
        for n in sorted(sigs):
            if n[:-4] not in tballs:
                FAIL("(b) release %s: orphan .sig asset %s (no matching tarball)" % (tag, n))

        mf = manifests.get(core)
        if mf is None:
            FAIL("(d) release %s has no %s/MANIFEST.json in the repo (unledgered core)" % (tag, core))
            continue
        vrow = next((v for v in (mf.get("versions") or []) if v.get("tag") == tag), None)
        if vrow is None:
            FAIL("(d) release %s is not listed in %s/MANIFEST.json" % (tag, core))
            continue

        massets = vrow.get("assets") or {}
        if len(massets) != len(tballs):
            FAIL("(d) release %s: manifest lists %d asset row(s), release holds %d tarball(s)" % (tag, len(massets), len(tballs)))

        # manifest -> release
        for osarch, row in sorted(massets.items()):
            want_name = "%s-%s.tar.gz" % (core, osarch)
            if osarch not in STORE_OSARCH:
                FAIL("(d) %s %s: manifest osarch key %r outside the artifacts-store enums" % (tag, core, osarch))
                continue
            if row.get("name") != want_name:
                FAIL("(d) %s %s: manifest asset name %r != contract %r" % (tag, osarch, row.get("name"), want_name))
                continue
            sha = (row.get("sha256") or "").lower()
            if not SHA_RE.match(sha):
                FAIL("(d) %s %s: manifest sha256 %r is not a 64-hex digest" % (tag, osarch, sha))
                continue
            a = tballs.get(want_name)
            if a is None:
                FAIL("(d) %s %s: manifest asset %s absent from the release" % (tag, osarch, want_name))
                continue
            dig = a.get("digest") or ""
            if not dig.startswith("sha256:"):
                FAIL("(d) %s %s: release asset carries no sha256 digest — parity unprovable" % (tag, osarch))
                continue
            if dig[len("sha256:"):] != sha:
                FAIL("(d) %s %s: sha256 DRIFT — release digest %s… vs manifest %s…" % (tag, osarch, dig[7:19], sha[:12]))

        # release -> manifest (no unledgered release assets)
        man_names = set("%s-%s.tar.gz" % (core, k) for k in massets)
        for n in sorted(tballs):
            if n not in man_names:
                FAIL("(d) release %s: tarball %s is not in %s/MANIFEST.json (unledgered asset)" % (tag, n, core))

    # (d) reverse manifest direction: every manifest version is a live release.
    for core, mf in sorted(manifests.items()):
        if mf.get("core") != core:
            FAIL("(d) %s/MANIFEST.json core field %r != folder name" % (core, mf.get("core")))
        for v in mf.get("versions") or []:
            vt = v.get("tag", "")
            if not CORE_TAG_RE.match(vt):
                FAIL("(a) %s/MANIFEST.json version tag %r is not contract-shaped" % (core, vt))
            if vt not in live_tags:
                FAIL("(d) %s/MANIFEST.json version %s has no live release" % (core, vt))

    # (c) every sig decodes to a 64-byte ed25519 signature (fetchCoreSig order).
    for tag, (_core, r) in sorted(live_tags.items()):
        for a in r.get("assets") or []:
            n = a.get("name", "")
            if not SIG_RE.match(n):
                continue
            p = os.path.join(sigdir, tag, n)
            if not os.path.isfile(p):
                FAIL("(c) sig file missing from cache: %s/%s" % (tag, n))
                continue
            with open(p, "rb") as f:
                data = f.read()
            if decode_sig(data) is None:
                FAIL("(c) %s/%s is neither raw 64-byte ed25519 nor base64 of it (panel fetchCoreSig order, fail-closed)" % (tag, n))

    print("conformance: %d core folder(s), %d published release(s) checked, %d violation(s)"
          % (len(manifests), len(live_tags), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
