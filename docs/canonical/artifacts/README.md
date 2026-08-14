# Canonical Raw Artifacts

This directory preserves the byte-level source artifacts behind the lightweight canonical indexes.

Archive:

```text
WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz
SHA256 = f2d96ceda6f0b5a761c209a4596fe47211d4caafdbf1f2c355ba4d3644c0b0e4
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

Restore locally with:

```bash
mkdir -p /tmp/wepld-canonical-artifacts
tar -xzf docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz -C /tmp/wepld-canonical-artifacts
sha256sum /tmp/wepld-canonical-artifacts/WEPLD_MASTER_ARCHITECTURE_EXECUTION_PLAN_2026-08-12_V2_2.md
```

The human-readable indexes remain the normal agent bootstrap path. The archive exists to prevent loss of the complete frozen plan and source registry and to permit byte-level recovery/audit.
