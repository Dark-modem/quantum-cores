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

- **arm64 not shipped this wave**: the cross build needs the aarch64
  libssl/pcap set inside the build image (the CMake presets support it;
  the toolchain file is trivial) — documented next wave.
- The driver wave (AGENT-3x) has NOT landed yet: the core is published;
  driving it is the documented next agent task.
