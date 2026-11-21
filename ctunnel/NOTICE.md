# NOTICE — ctunnel

- Upstream project: C-Tunnel — <https://github.com/CIAUB/C-Tunnel>
- License: **AGPL-3.0** (full text: `LICENSE-ctunnel.txt` in the release
  artifact store; also shipped inside every published tarball).
- Copyright holders: the C-Tunnel upstream authors (the AGPL-3.0 license
  text shipped by upstream is the authoritative attribution record; the
  upstream LICENSE header does not name individual holders).
- Attribution: this folder redistributes repackaged upstream binaries of
  C-Tunnel (AGPL aggregation, like frp/xray/gost). All rights belong to the
  upstream authors; the AGPL-3.0 terms govern the binaries. ZERO upstream
  source is copied into any Quantum repository — all Quantum-side code
  (panel, agent driver, pipelines) is Quantum's own.

## Provenance of this version (2.0.0)

- Version: **2.0.0** — the upstream CHANGELOG `[2.0.0]` release
  (49 methods across 6 families: kernel L3 ×16, kernel L2 ×7,
  UDP-Crypt ×11, stealth ×2, reverse-L4 ×9, gaming ×4; the `methods[]`
  block in `MANIFEST.json` mirrors the upstream `pkg/catalog/catalog.go`
  rows field-for-field).
- **Built from source**, not from the upstream release binaries: the
  source of truth is the human-provided deterministic upstream v2.0.0
  snapshot (workspace path `03-RESEARCH/c-tunnel-review/C-Tunnel-main`,
  WSL tree fingerprint
  `b9206cc1b4b5b722b0a139c68d0094bd12fbd7846598e475b36eb1607aa1e293`).
- Build: WSL Ubuntu-24.04, `GOTOOLCHAIN=go1.26.9 CGO_ENABLED=0`,
  `go build -trimpath -ldflags "-s -w -X ctunnel/pkg/version.Version=2.0.0"`
  for linux-amd64 + linux-arm64. The module's `toolchain go1.26.10`
  directive is intentionally not fetched (an explicit `GOTOOLCHAIN`
  overrides it; the `go 1.26.0` language requirement is satisfied).
  Upstream's own CI binaries are go1.26.10 builds, so upstream's
  `SHA256SUMS` entries do not apply to a source build (upstream checksum:
  not applicable — provenance is the snapshot fingerprint above plus the
  Quantum pack-time signature).
- Tarball contents per arch: `ctunnel_2.0.0/{ctunnel, ctunnel-engine,
  ctunnel-local}` + upstream `LICENSE` + `SOURCE.txt`. The agent extracts
  only `ctunnel-engine` (the userspace data plane, driven via
  `-config <env>`). `ctunnel-local` ships per the core contract (it exists
  in upstream `cmd/` but is absent from upstream release assets). The
  upstream `ctunnel-kernel.sh` is NOT shipped and NOT run — the Quantum
  agent driver performs the equivalent kernel operations itself
  (additive-only, arg-list exec, per-tunnel ownership tags).

## Packaging

The published tarball is a Quantum release-pipeline repackage
(`scripts/pack-engine.sh`, offline `--from` staging of the source-build
output): the three binaries plus the upstream `LICENSE` text and a
`SOURCE.txt` (upstream home page) inside `ctunnel_2.0.0/`. The artifact is
signed with the Quantum engine-artifact ed25519 key (see `README.md` —
M2 invariant).

## Known gaps

- amd64 binaries are smoke-executed in an isolated container (`-h`,
  `-version`, `-selftest` all report correctly); the arm64 binaries are
  cross-compiled from the same source and verified by ELF header +
  inner-tar sha256, but not executed (no arm64 host/container in this lab).
- The v2 engine's userspace carriers are IPv4-underlay (UDP `udp4`
  sockets, AF_INET raw sockets upstream) — reflected in the `ipver`
  column of `MANIFEST.json` (`v6` only for the four IPv6Underlay kernel
  methods).
