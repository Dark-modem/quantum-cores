# NOTICE — rathole

- Upstream project: rathole — <https://github.com/rapiz1/rathole>
- License: **Apache-2.0** (full text: `LICENSE-rathole.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright holders: the rathole upstream authors (the Apache-2.0 license
  text shipped by upstream is the authoritative attribution record; the
  upstream LICENSE header does not name individual holders).
- Attribution: this folder redistributes a repackaged upstream release
  binary of rathole. All rights belong to the upstream authors; the
  Apache-2.0 terms govern the binary.

## Packaging

The published tarball is a Quantum release-pipeline repackage: the upstream
binary extracted from the upstream release archive plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`rathole_<version>/`. The artifact is signed with the Quantum
engine-artifact ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 0.5.0 (linux-amd64 + linux-arm64 both
  packed and verified).
