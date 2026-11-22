# quantum-cores — Quantum external engine cores (release channel)

This repo is the **public release channel for the third-party tunnel/relay
"engine cores"** the Quantum panel and agents deploy as external processes
(frp, xray, backhaul, rathole, gost, chisel, wstunnel, udp2raw, ctunnel).

There is **no source and no binary in git**. Git holds only the per-core
metadata (an informational `MANIFEST.json` + a `NOTICE.md` per core folder).
The binaries live exclusively in **GitHub releases**:

- one release per core per version, tag shape **`<core>-v<semver>`**
  (e.g. `frp-v0.61.1`; `udp2raw` is date-versioned upstream — its tags look
  like `udp2raw-v20230206.0`);
- release assets are named **`<core>-<os>-<arch>.tar.gz`**
  (e.g. `frp-linux-amd64.tar.gz`) plus a detached signature **`<asset>.sig`**;
- the `.sig` file is the **base64 (std encoding) of the 64-byte ed25519
  signature over the exact `.tar.gz` bytes** — the same representation the
  Quantum engine-artifact store uses, so it feeds directly into the existing
  verification path;
- every tarball is repackaged by the Quantum release pipeline: upstream
  binary/binaries extracted from the upstream archive, plus the upstream
  `LICENSE` text and a `SOURCE.txt` inside the archive.

## Security model (M2 invariant)

The signing key is the Quantum **engine-artifact ed25519 key**; its public
half is pinned in the shipped agent binaries (also recorded per pack as
`ENGINE-PUB-KEY.txt` in the artifact store). The **panel verifies sha256 +
the ed25519 signature of every core artifact BEFORE handing anything to an
agent** (`engine.VerifyArtifact` in quantum-agent: sha256 hex digest must
match, ed25519 signature over the artifact bytes must verify against the
pinned key — fail-closed). Consumers of this repo must keep that invariant:
never trust a download without both checks.

## Cores currently published

| core     | version    | arches               | upstream license |
|----------|------------|----------------------|------------------|
| frp      | 0.61.1     | linux-amd64, linux-arm64 | Apache-2.0   |
| xray     | 24.12.31   | linux-amd64, linux-arm64 | MPL-2.0      |
| backhaul | 0.7.2      | linux-amd64, linux-arm64 | AGPL-3.0     |
| rathole  | 0.5.0      | linux-amd64, linux-arm64 | Apache-2.0   |
| gost     | 3.3.3      | linux-amd64, linux-arm64 | MIT          |
| chisel   | 1.10.1     | linux-amd64, linux-arm64 | MIT          |
| wstunnel | 10.1.9     | linux-amd64, linux-arm64 | BSD-3-Clause |
| udp2raw  | 20230206.0 | linux-amd64 (arm64 gap — see `udp2raw/NOTICE.md`) | MIT |
| ctunnel  | 1.1.1      | linux-amd64, linux-arm64 | AGPL-3.0     |

`versions` history grows with every new packed version; `MANIFEST.json`
files are the human-readable index of it (see `MANIFESTS-ARE-INDEX.md`).

## Exemptions (intentionally absent)

- **matrix** — an in-process Quantum engine (Go code inside quantum-agent).
  It ships with the agent binary itself: no upstream binary, no packed
  artifact, hence no folder here.
- **wireguard** — uses the host kernel module; there is no upstream userspace
  binary to pack (an optional wireguard-go fallback would be packed via
  `engine_params` if ever needed).

## Provenance

All current assets were mirrored byte-identical from the signed artifact
store in `Dark-modem/quantum-release` (`dist/engines-2026-11-09`), which is
what the shipped bundles pin. On 2026-11-21 every stored artifact re-passed
its sha256 check and its ed25519 signature verified against the
agent-pinned public key (34/34 artifact checks).

## Licensing

Each core folder carries a `NOTICE.md` naming the upstream project, license
(SPDX) and attribution. These are third-party cores — all rights belong to
their upstream authors; the per-core license terms govern the binaries. The
upstream license text also ships inside every tarball.

## Adding a new core version

The repo is self-guarding: `scripts/conformance.sh` validates **every
published release** against the contract (tag shape `<core>-v<2-or-3-segment
numeric semver>` — with the CORES-6 naive exception: the `naive` core
additionally admits its VERBATIM upstream Chromium shape
`naive-v<4 numeric segments>-<respins>`, e.g. `naive-v154.0.8037.49-5`,
documented in `conformance.py`/`naive/NOTICE.md`, panel mirror pending;
asset names `<core>-<os>-<arch>.tar.gz` with the store's
os/arch enums; a `.sig` companion per tarball that decodes to a 64-byte
ed25519 signature; manifest ⇄ release parity both ways including per-asset
sha256; a `NOTICE.md` per core folder; no binaries in the git tree). It
fails loud — one `CONFORMANCE FAIL:` line per violation, exit 1 — and is
strictly read-only.

The publish flow for core `X` version `N+1`:

1. **manifest update** — add the new `versions` row (tag `X-vN+1`, per-arch
   asset name + sha256) to `X/MANIFEST.json` (informational index first,
   so the gate can prove parity the moment the release lands);
2. **release publish** — tag `X-vN+1` with assets `X-linux-<arch>.tar.gz`
   (+ `.sig` companions, signed by the engine-artifact key) for every arch
   the core ships, byte-identical to the artifact store;
3. **conformance green** — run `scripts/conformance.sh` (fetches the live
   releases via `gh`; or prefetch and set `CORES_RELEASES_JSON` +
   `CORES_SIG_CACHE_DIR` for offline runners). `CONFORMANCE: all checks
   green` = done; anything else names the drift.

`CORES_DIR`, `CORES_RELEASES_JSON`, `CORES_SIG_CACHE_DIR` also make the
gate runnable against a local fixture (used for its mutation proof — see
CORES-3-REPORT) — a fixture tree without git simply skips check (f), loudly.

