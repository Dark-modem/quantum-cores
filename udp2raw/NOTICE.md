# NOTICE — udp2raw

- Upstream project: udp2raw — <https://github.com/wangyu-/udp2raw>
- License: **MIT** (full text: `LICENSE-udp2raw.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright: `Copyright (c) 2017 Yu Wang (wangyucn at gmail.com)` (from the
  upstream LICENSE header shipped in the packed artifact).
- Attribution: this folder redistributes a repackaged upstream release
  binary of udp2raw. All rights belong to the upstream author; the MIT
  terms govern the binary.

## Versioning note

udp2raw is date-versioned upstream. The tag shape used here is
`udp2raw-v<date>.<seq>` — e.g. `udp2raw-v20230206.0` for upstream's
`20230206.0` release.

## Packaging

Upstream 20230206.0 ships ONE bundle (`udp2raw_binaries.tar.gz`) containing
per-arch binaries. The published tarball is a Quantum release-pipeline
repackage: the upstream `udp2raw_amd64` binary extracted from the upstream
bundle plus the upstream `LICENSE` text and a `SOURCE.txt` (upstream home
page) inside `udp2raw_<version>/`. The artifact is signed with the Quantum
engine-artifact ed25519 key (see `README.md` — M2 invariant).

## Known gaps

- **linux-arm64 NOT packed.** Upstream replaced their release archive after
  2026-11-08 and it no longer contains `udp2raw_aarch64` (verified
  2026-11-09 in the Quantum pack pipeline). Deployed Quantum agents are
  amd64; the arm64 asset will be added when upstream restores an aarch64
  binary.
