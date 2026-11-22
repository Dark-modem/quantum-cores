# NOTICE — xray

- Upstream project: Xray-core — <https://github.com/XTLS/Xray-core>
- License: **MPL-2.0** (full text: `LICENSE-xray.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright holders: the Xray-core authors (the MPL-2.0 license text
  shipped by upstream is the authoritative attribution record; the upstream
  LICENSE header does not name individual holders).
- Attribution: this folder redistributes a repackaged upstream release
  binary of Xray-core. All rights belong to the upstream authors; the
  MPL-2.0 terms govern the binary.

## Packaging

The published tarball is a Quantum release-pipeline repackage: the upstream
binary extracted from the upstream release archive plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`xray_<version>/`. The artifact is signed with the Quantum engine-artifact
ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 24.12.31 (linux-amd64 + linux-arm64 both
  packed and verified).

## OVERNIGHT-A5 upgrade (2026-11-23)

`xray-v26.3.27` joins the manifest as `latest` (v24.12.31 stays published for
legacy agents). Repackage of the UPSTREAM release assets — Xray-linux-64.zip
(sha256 23cd9af9…) and Xray-linux-arm64-v8a.zip (sha256 4d30283a…), both
digest-verified against the GitHub API digest field AND the upstream .dgst
files, layout mirrored (xray_26.3.27/{xray,LICENSE,SOURCE.txt}).
Probe-proven on the repackaged binary: hysteria2 inbound `Configuration OK`,
hysteria2 outbound `Configuration OK` (version:2 required) — the
OVERNIGHT-A5 hysteria-inout blocker (v24.12.31 "unknown config id") is
closed. `masque` remains upstream-master-only (probe: unknown config id).
