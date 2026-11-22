# NOTICE — easytier

- Upstream project: EasyTier — <https://github.com/EasyTier/EasyTier>
- License: **LGPL-3.0** (upstream `LICENSE`, shipped verbatim inside every
  published tarball as `easytier/LICENSE`; copyright the EasyTier authors).
- Attribution: this folder redistributes UNMODIFIED upstream release
  binaries. LGPL-3.0 compliance: the binaries are byte-identical to the
  upstream release artifacts (verified against the upstream `SHA256SUMS` of
  tag `v2.7.1`), the license text ships inside every tarball, and the
  corresponding source is the upstream repository at the pinned tag —
  <https://github.com/EasyTier/EasyTier/tree/v2.7.1> (commit
  `0d9c52b169dc2112687ddefcf571cd01d383193c`). No modification, no source
  copying, no linking from Quantum code — the binary is an EXTERNAL core.

## Packaging

Quantum OVERNIGHT-D2: upstream release binaries from tag `v2.7.1` (amd64 =
`easytier-linux-x86_64-v2.7.1.zip`, arm64 = `easytier-linux-aarch64-v2.7.1.zip`),
each digest-verified against the release's own `SHA256SUMS` before packing.
Repackaged only: `easytier/easytier-core` + `easytier/easytier-cli` +
`easytier/easytier-web` + `easytier/easytier-web-embed` + `LICENSE` +
`SOURCE.txt`. Binary version stamp `2.7.1-0d9c52b1-20261115` matches the
upstream tag commit (`easytier-core --version` smoke-tested on WSL amd64).
Signed with the Quantum engine-artifact ed25519 key (rc lineage,
fingerprint-verified `40ab0b9f1360cc99`).

## Method coverage

`methods[]` carries the `easytier-mesh` row (the L3 TUN overlay). Everything
else the core offers (DHCP, subnet export, config server, the ring/faketcp
listener shapes) are modes/features of that one mesh method — enumerated in
the method title, not as separate rows.

## Known gaps

- None arch-wise: both linux-amd64 and linux-arm64 ship (upstream publishes
  both for v2.7.1).
- No Quantum DRIVER yet — the panel cannot drive this core end-to-end until
  a driver wave lands (the wiring spec lives in
  `00-ADMIN/OVERNIGHT-D2-REPORT.md`). The core is downloadable and
  conformance-green; `methods[]` is informational per §2.22.
