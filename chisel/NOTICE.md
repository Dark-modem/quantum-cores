# NOTICE — chisel

- Upstream project: chisel — <https://github.com/jpillora/chisel>
- License: **MIT** (full text: `LICENSE-chisel.txt` in the release artifact
  store; also shipped inside every published tarball).
- Copyright: `Copyright (c) 2024 Jaime Pillora <dev@jpillora.com>` (from
  the upstream LICENSE header shipped in the packed artifact).
- Attribution: this folder redistributes a repackaged upstream release
  binary of chisel. All rights belong to the upstream author; the MIT
  terms govern the binary.

## Packaging

Upstream ships chisel as a FLAT `.gz` single binary. The published tarball
is a Quantum release-pipeline repackage: the upstream binary decompressed
from the upstream `.gz` plus the upstream `LICENSE` text and a `SOURCE.txt`
(upstream home page) inside `chisel_<version>/`. The artifact is signed
with the Quantum engine-artifact ed25519 key (see `README.md` — M2
invariant).

## Known gaps

- none recorded at pack time for 1.10.1 (linux-amd64 + linux-arm64 both
  packed and verified).
