# NOTICE — wstunnel

- Upstream project: wstunnel — <https://github.com/erebe/wstunnel>
- License: **BSD-3-Clause** (full text: `LICENSE-wstunnel.txt` in the
  release artifact store; also shipped inside every published tarball).
- Copyright: `Copyright (c) 2016-2024, Erèbe - Romain Gerard` (from the
  upstream LICENSE header shipped in the packed artifact).
- Attribution: this folder redistributes a repackaged upstream release
  binary of wstunnel. All rights belong to the upstream author; the
  BSD-3-Clause terms govern the binary.

## Packaging

The published tarball is a Quantum release-pipeline repackage: the upstream
binary extracted from the upstream release archive plus the upstream
`LICENSE` text and a `SOURCE.txt` (upstream home page) inside
`wstunnel_<version>/`. The artifact is signed with the Quantum
engine-artifact ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- none recorded at pack time for 10.1.9 (linux-amd64 + linux-arm64 both
  packed and verified).
