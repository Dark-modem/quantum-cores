# NOTICE — sing-box

- Upstream project: sing-box — <https://github.com/SagerNet/sing-box>
- License: **GPL-3.0** (upstream `LICENSE`, shipped verbatim inside every
  published tarball as `sing-box/LICENSE`; copyright nekohasekai /
  SagerNet).
- Attribution: this folder redistributes a SOURCE-BUILT binary of sing-box.
  Per the C-Tunnel ruling (AGPL vendor-only, zero source copying) the GPL
  binary is vendored as an EXTERNAL CORE — no GPL source enters Quantum
  (aggregation, not derivation). All rights belong to the upstream authors.

## Packaging

Quantum OVERNIGHT-C source build: release tag `v1.14.4` (commit c005f3530),
linux amd64+arm64, go1.27.3 via `GOPROXY=goproxy.io,direct`, version stamped
through the upstream `constant.Version` ldflags hook (`-version`
smoke-tested: sing-box version 1.14.4). Build tags:
`with_gvisor,with_quic,with_dhcp,with_wireguard,with_utls,with_acme,with_clash_api,with_tailscale,with_openvpn`
(+`badlinkname,tfogo_checklinkname0` upstream defaults). The tarball carries
`sing-box/<binary>` + the upstream LICENSE + SOURCE.txt. Signed with the
Quantum engine-artifact ed25519 key (rc lineage).

## Known gaps

- cronet-bound features EXCLUDED (naive, ocm, ccm, cloudflared,
  openconnect): upstream cronet-go ships no arm64 library — the import
  breaks any arm64 build. Documented per the manifest; the tagged features
  cover the Iran-path protocols (vless/vmess/trojan/ss/hysteria2/tuic/
  anytls/shadowtls/ssh/snell/wireguard/openvpn/tun/tailscale).
