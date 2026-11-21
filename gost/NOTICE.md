# NOTICE — gost

- Upstream project: gost (v3) — <https://github.com/go-gost/gost>
- License: **MIT** (full text: `LICENSE-gost.txt` in the release artifact
  store; also shipped inside every published tarball).
- Copyright: `Copyright (c) 2016 ginuerzh` (from the upstream LICENSE
  header shipped in the packed artifact).
- Attribution: this folder redistributes a repackaged upstream release
  binary of gost. All rights belong to the upstream authors; the MIT terms
  govern the binary.

## Packaging

The published tarball is a Quantum release-pipeline repackage: the upstream
binary extracted from the upstream release archive plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`gost_<version>/`. The artifact is signed with the Quantum engine-artifact
ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 3.3.3 (linux-amd64 + linux-arm64 both
  packed and verified).
