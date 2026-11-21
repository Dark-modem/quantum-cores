# NOTICE — ctunnel

- Upstream project: C-Tunnel — <https://github.com/CIAUB/C-Tunnel>
- License: **AGPL-3.0** (full text: `LICENSE-ctunnel.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright holders: the C-Tunnel upstream authors (the AGPL-3.0 license
  text shipped by upstream is the authoritative attribution record; the
  upstream LICENSE header does not name individual holders).
- Attribution: this folder redistributes a repackaged upstream release
  binary of C-Tunnel. All rights belong to the upstream authors; the
  AGPL-3.0 terms govern the binary.

## Packaging

Upstream publishes raw single-file binaries
(`ctunnel-engine-linux-<arch>`) plus a `SHA256SUMS` file (verified at pack
time against the upstream file). The published tarball is a Quantum
release-pipeline repackage: the upstream binary plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`ctunnel_<version>/`. The artifact is signed with the Quantum
engine-artifact ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 1.1.1 (linux-amd64 + linux-arm64 both
  packed and verified).
