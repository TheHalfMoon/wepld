# WePLD Pictorial Lock Metadata Overlay v9 Evidence — 2026-08-24

Status: **POLICY CANDIDATE EVIDENCE — NOT CANONICAL ADMISSION**

This record binds the single authorized post-import Pictorial lock metadata overlay.
It does **not** rewrite upstream provenance and does **not** authorize dependency,
donor, product-runtime, provider, model, or credential execution.

```text
CANONICAL_MAIN=08a06e9f2664735eb55db5b2f49f95d3d3f91c3f
PREDECESSOR_SOURCE_HEAD=28f0023b8ffb90c585213762dae5f4c1d57322ef
PREDECESSOR_SOURCE_TREE=ed9ee4e0b1065e73909adbb2b4f02a0464ea44fc
REPAIR_CANDIDATE_HEAD=04cc279133d536e2b4b68e01c019d7b595f0ed42
REPAIR_CANDIDATE_TREE=5397b0f31719703e1f346f41b52bb5cd53bca2f7
PREDECESSOR_VENDOR_TREE=4c5259bd1d0fdbdd827d433f01767686ff418cc0
REPAIRED_VENDOR_TREE=88b58da55a3696feccef89fad3865ce3317fc6fa
PREDECESSOR_PICTORIAL_TREE=066be2ce78c19d1830b8a8e76ea3afeaa85bb2ff
REPAIRED_PICTORIAL_TREE=3416c629e4b972765e0e00d3f6cb0ece56460481
AGILE_TREE_UNCHANGED=6248b8de14bb49cb70ebe51838c5e0564ebbf3cf
PACKAGE_JSON_BLOB_UNCHANGED=ba646522c498af6e9bfa02fd1dba2f098d9f6d42
ORIGINAL_BUN_LOCK_BLOB=f7114d1b93f26eb9d7796fc15ae3d639d2209c9d
REPAIRED_BUN_LOCK_BLOB=0045fb246c6ffac5375f7272f4f88b3dd7ef53d6
REPAIRED_BUN_LOCK_SHA256=92d73b6b1c491fd9c800c0243d6652b4287a4edd625d34ea5fd3af99021d3733
REPAIRED_CYCLONEDX_SHA256=4999c6af6eba6f6eefaebdc325ccf9d57a4cb837f75bbda5bb4a88a5244255de
REPAIRED_OSV_RESPONSE_SHA256=c955b897cd3c3d7469c43716f9e54bbe6aff48d68d0fc8da47ee5f0f219e16a4
```

## Provenance rule

The existing Pictorial source map remains the immutable record of the pinned upstream
donor snapshot. `vendor/pictorial/bun.lock` at blob `f7114d1b93f26eb9d7796fc15ae3d639d2209c9d` is the
source-mapped upstream/rebrand snapshot byte identity. The repaired lock blob
`0045fb246c6ffac5375f7272f4f88b3dd7ef53d6` is a **separate WePLD-owned dependency-metadata overlay** and
must never be represented as byte-identical to the upstream donor lock.

The overlay candidate is bound to the exact predecessor-to-candidate transition
`28f0023b8ffb90c585213762dae5f4c1d57322ef` → `04cc279133d536e2b4b68e01c019d7b595f0ed42`. The candidate has exactly one parent,
the predecessor source head above. The only changed tracked file between those two
commits is `vendor/pictorial/bun.lock`; `package.json`, Agile, legal/provenance
artifacts, branding artifacts, source maps, file modes, and every other tracked blob
remain unchanged.

## Static qualification already proven

The repaired Pictorial graph contains 235 lock entries, 11 semantic lock-key
changes/additions, 341 resolved dependency/optional/resolved-peer edges, zero
unresolved non-peer edges, no remaining previously identified vulnerable exact
identities, and zero OSV-affected exact npm identities in the qualified graph.
Remaining unresolved peer edges are optional peers only.

## Authority boundary

```text
SOURCE_ADMISSION=EXACT_SOURCE_PLUS_ONE_BOUND_LOCK_METADATA_OVERLAY
DEPENDENCY_ADMISSION=NONE
PACKAGE_INSTALLATION=NONE
PACKAGE_IMPORT_OR_EXECUTION=NONE
DONOR_CODE_EXECUTION=NONE
DONOR_WORKFLOW_EXECUTION=NONE
DONOR_HOOK_EXECUTION=NONE
DONOR_INSTALL_SCRIPT_EXECUTION=NONE
DONOR_PARITY_TEST_EXECUTION=NONE
DONOR_LIVE_TEST_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
MODEL_WEIGHT_ACCESS=NONE
MODEL_INFERENCE=NONE
CREDENTIAL_CONTENT_ACCESS=NONE
PRODUCT_IMPLEMENTATION_AUTHORITY=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
H0_014_PLUS=NOT_STARTED
H0_SCREEN_EXECUTION=NONE
CANONICAL_POLICY_MERGE=NOT_AUTHORIZED
PR136_SOURCE_HEAD_REPLACEMENT=NOT_AUTHORIZED
PR162_MERGE=NOT_AUTHORIZED
PR136_MERGE=NOT_AUTHORIZED
```
