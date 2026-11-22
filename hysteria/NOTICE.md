# NOTICE — hysteria

- Upstream project: hysteria (v2) — <https://github.com/apernet/hysteria>
- License: **MIT** (upstream `LICENSE.md`, shipped verbatim inside every
  published tarball as `hysteria/LICENSE`).
- Copyright holders: the hysteria upstream authors (per the upstream
  LICENSE.md, Copyright 2023 Toby).
- Attribution: this folder redistributes a SOURCE-BUILT binary of hysteria
  (not an upstream CI asset). All rights belong to the upstream authors;
  the MIT terms govern the binary.

## Packaging

Quantum OVERNIGHT-C source build: release tag `app/v2.14.0` (commit c2b181e),
linux amd64+arm64, go1.27.3 via `GOTOOLCHAIN=auto GOPROXY=goproxy.io,direct`,
version stamped with the upstream ldflags hook
(`cmd.appVersion=2.14.0`; `-version` smoke-tested: Version 2.14.0). The
tarball carries `hysteria/<binary>` + the upstream LICENSE + SOURCE.txt.
Signed with the Quantum engine-artifact ed25519 key (rc lineage).

## Known gaps

- none recorded at pack time for 2.14.0 (both arches packed, signed and
  smoke-tested).
