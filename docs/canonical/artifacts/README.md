# Canonical Raw Artifacts

This directory preserves the byte-level source artifacts behind the lightweight canonical indexes.

Archive:

```text
WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz
SHA256 = 35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0
```

Contents:

```text
WEPLD_MASTER_ARCHITECTURE_EXECUTION_PLAN_2026-08-12_V2_2.md
WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1.json
WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1.csv
WEPLD_SOURCE_ARTIFACT_PIN_LEDGER_2026-08-14_V1.md
WEPLD_SOURCE_CAPABILITY_MINING_PRIORITY_MATRIX_2026-08-14_V1.md
```

Important integrity anchors:

```text
MASTER_PLAN_V2_2_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
ACCOUNTED_SOURCE_ENTRIES = 402
```

The repository CI verifies the archive hash, exact member set, master-plan hash, JSON/CSV source counts and uniqueness, and that every source entry remains `NOT_ADMITTED`.

Restore locally with fail-closed verification:

```bash
set -euo pipefail

printf '%s  %s\n' \
  '35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0' \
  'docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz' \
  | sha256sum --check -

rm -rf /tmp/wepld-canonical-artifacts
mkdir -p /tmp/wepld-canonical-artifacts
tar -xzf docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz \
  -C /tmp/wepld-canonical-artifacts

printf '%s  %s\n' \
  'e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44' \
  '/tmp/wepld-canonical-artifacts/WEPLD_MASTER_ARCHITECTURE_EXECUTION_PLAN_2026-08-12_V2_2.md' \
  | sha256sum --check -
```

A failed archive or plan hash stops restoration; successful extraction alone is not integrity evidence.

The human-readable indexes remain the normal agent bootstrap path. The archive exists to prevent loss of the complete frozen plan and source registry and to permit byte-level recovery/audit.
