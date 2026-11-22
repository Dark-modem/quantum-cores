# NOTICE — paqet

- Upstream project: paqet — <https://github.com/hanselime/paqet>
- License: **MIT** (upstream `LICENSE`, shipped verbatim inside the
  published tarball as `paqet/LICENSE`).
- Attribution: this folder redistributes a SOURCE-BUILT binary of paqet.
  All rights belong to the upstream authors; the MIT terms govern the
  binary.

## Packaging

Quantum OVERNIGHT-C source build: release tag `v1.0.0-alpha.21` (commit
4b81ce0), linux **amd64 ONLY**, go1.27.3 (WSL, CGO_ENABLED=1 — upstream
needs gopacket/pcap ⇒ libpcap), GOPROXY=goproxy.io,direct. The tarball
carries `paqet/<binary>` + the upstream LICENSE + SOURCE.txt. Signed with
the Quantum engine-artifact ed25519 key (rc lineage).

## Known gaps

- **arm64 not shipped this wave**: the arm64 CGO link needs the arm64
  libpcap dev files (multiarch), absent on this build host. amd64-only is
  fail-closed honest packaging (mirrors the udp2raw amd64-only precedent);
  arm64 = documented next wave.
