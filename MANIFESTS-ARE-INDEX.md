# MANIFESTS-ARE-INDEX

The `MANIFEST.json` file in each core folder is a **manually-curated,
informational index** — a convenience for humans skimming the repo.

It is **not** the authoritative source of truth:

- the authoritative record of published versions and assets is the repo's
  **releases themselves** (tags `<core>-v<semver>` + their assets);
- a manifest can lag behind or precede a release while it is being edited;
- consumers (including the Quantum panel's core discovery) must **enumerate
  releases**, not scrape these files, and must always verify sha256 +
  ed25519 signature themselves — see the M2 note in `README.md`.
