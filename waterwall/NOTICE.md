# NOTICE — WaterWall

- Upstream project: WaterWall — <https://github.com/radkesvat/WaterWall>
- License: **MPL-2.0** (upstream `LICENSE.txt`, shipped verbatim inside the
  published tarball as `waterwall/LICENSE`).
- Attribution: this folder redistributes a SOURCE-BUILT binary of WaterWall
  (not an upstream CI asset). All rights belong to the upstream authors;
  the MPL-2.0 terms govern the binary (file-level copyleft — the vendored
  BINARY is aggregation, not derivation, per the cores separation).

## Packaging

Quantum OVERNIGHT-C2 ride-along source build: release tag `v1.6.0` (commit
f4a5b3b1), linux **amd64 ONLY**, built inside a quantum-test-devagent-*
container (cmake 3.28 + ninja + g++13 + git; CPM deps cloned during the
build; the full 3390-step compile incl. Chromium quiche completed clean).
Smoke: `Waterwall version 1.6.0`. The tarball carries `waterwall/<binary>`
+ the upstream LICENSE + SOURCE.txt. Signed with the Quantum
engine-artifact ed25519 key (rc lineage).

## Known gaps

- **arm64 SHIPPED (OVERNIGHT-A4, 2026-11-22)**: the aarch64 cross build
  landed via the containerized path — gcc-aarch64-linux-gnu g++ 13 +
  libssl-dev:arm64 + libpcap-dev:arm64 (ports.ubuntu.com per-arch apt
  sources) + the libatomic.a symlink (ww/CMakeLists.txt:1485 resolves it
  by exact name under the cross root path), full 3371-step ninja compile
  EXIT 0 on the same release-tag source. Binary = ELF 64-bit ARM
  aarch64, stripped; smoke via qemu-aarch64-static: "Waterwall version
  1.6.0". Asset `waterwall-linux-arm64.tar.gz`
  (sha256 0efa4f7de2008cc5f518b20db5c76388e53428a05e860b6958b076ee3b08fbe4)
  + base64 ed25519 `.sig`, same engine-artifact key lineage (verified
  against the existing amd64 asset sig).
- The driver wave (AGENT-3x) has NOT landed yet: the core is published;
  driving it is the documented next agent task.
