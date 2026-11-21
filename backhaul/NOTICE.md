# NOTICE — backhaul

- Upstream project: Backhaul — <https://github.com/Musixal/Backhaul>
- License: **AGPL-3.0** (full text: `LICENSE-backhaul.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright holders: the Backhaul upstream authors (the AGPL-3.0 license
  text shipped by upstream is the authoritative attribution record; the
  upstream LICENSE header does not name individual holders).
- Attribution: this folder redistributes a repackaged upstream release
  binary of Backhaul. All rights belong to the upstream authors; the
  AGPL-3.0 terms govern the binary.

## Packaging

The published tarball is a Quantum release-pipeline repackage: the upstream
binary extracted from the upstream release archive plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`backhaul_<version>/`. The artifact is signed with the Quantum
engine-artifact ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 0.7.2 (linux-amd64 + linux-arm64 both
  packed and verified).
