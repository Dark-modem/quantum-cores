# NOTICE — naive

- Upstream project: NaiveProxy — <https://github.com/klzgrad/naiveproxy>
- License: **BSD-3-Clause** (Chromium's `LICENSE`, shipped verbatim inside
  every published tarball as `naive/LICENSE`; copyright The Chromium
  Authors. The bundled Caddy-forwardproxy pieces are Apache-2.0 — both
  permissive; no GPL/AGPL anywhere in the artifact). Binary redistribution
  with LICENSE + this NOTICE is vendorable.
- Attribution: this folder redistributes **UNMODIFIED upstream release
  binaries**. The binaries are byte-identical to the upstream release
  artifacts of tag `v154.0.8037.49-5` (verified twice: the OVERNIGHT-D2
  staging hash-check and the CORES-6 fresh re-hash on 2026-11-23 against
  the live GitHub API asset digests — x64 `80214dfe…44c7d`, arm64
  `8f4d917f…4114d8d`). The corresponding source is the upstream repository
  at the pinned tag —
  <https://github.com/klzgrad/naiveproxy/tree/v154.0.8037.49-5>. (A source
  build is a full Chromium build — depot_tools/gn/ninja, tens of GB — so
  the upstream release binaries are the artifact source, per the D2
  recipe; the cores contract does not require source builds.) No
  modification, no source copying — the binary is an EXTERNAL core (the
  C-Tunnel aggregation posture).

## Packaging

Quantum CORES-6 (staged by OVERNIGHT-D2, `HOLD.md` recipe): upstream
release binaries from tag `v154.0.8037.49-5` (published 2026-10-22, not
draft/prerelease; the `-4` pin was withdrawn upstream, `-5` is current —
BackPack's pin), both linux arches, each digest-verified against the
upstream release's GitHub API asset digest before packing. Repackaged
only: `naive/naive` + `naive/LICENSE` + `naive/USAGE.txt` + `naive/SOURCE.txt`.
Smoke: `naive 154.0.8037.49` (WSL amd64, version stamp matches the tag).
Signed with the Quantum engine-artifact ed25519 key (rc lineage,
fingerprint-verified `40ab0b9f1360cc99`).

## Tag-contract note (CORES-6 exception)

The release tag mirrors upstream VERBATIM: Chromium versions are
`v<major>.<build>.<branch>.<patch>-<respins>` (`v154.0.8037.49-5` = 4
numeric segments + a re-spin suffix). The standing cores tag shape
(`<core>-v<2-or-3-segment numeric semver>`, byte-identical to the panel's
`coresTagRe`) cannot carry that, and a lossy mapping (`naive-v154.0`) was
refused per the paqet precedent — it collides within the Chromium
major/re-spin and misidentifies the artifact. Published instead under the
CORES-6 tag-contract exception in `scripts/conformance.py` (naive-only,
documented there). KNOWN DIVERGENCE: the panel's discovery regex does not
accept the shape yet — naive stays invisible to the §2.22 feed until the
panel mirrors the exception (flagged to the architect;
`00-ADMIN/CORES-6-REPORT.md`).

## Method coverage

`methods[]` carries the `naive-http2` row (the h2 CONNECT forward proxy
protocol). The BackPack `naive-http2 (managed)` item = THIS client binary
(operator-managed, `insecure-concurrency` 1-16) + a sing-box naive
inbound as the server. Server-half options for the driver wave: (a) an
amd64-only sing-box build variant with the naive package (diverges from
our both-arch core), or (b) the klzgrad/forwardproxy Caddy fork (Apache-2.0,
plain Go, both arches trivially) as its own core — upstream's recommended
naive server with the padding layer; (b) is the cleaner both-arch path.
TLS = operator cert (naive requires valid TLS unless the client opts
`insecure`); secrets = http-basic user/pass. Wiring spec:
`00-ADMIN/OVERNIGHT-D2-REPORT.md` §4.

## Known gaps

- No Quantum DRIVER yet — the panel cannot drive this core end-to-end
  until a driver wave lands (the managed-mode wiring spec lives in
  `00-ADMIN/OVERNIGHT-D2-REPORT.md` §4). The core is downloadable and
  conformance-green; `methods[]` is informational per §2.22.
- arm64: upstream-built artifact (digest-verified), ELF aarch64 verified;
  not executed (no arm64 host — the same honest caveat class as the
  easytier arm64 landing; the amd64 build is smoke-tested).
- The panel-side tag-regex mirror (see the tag-contract note above) is
  pending — without it the §2.22 feed does not surface naive.
