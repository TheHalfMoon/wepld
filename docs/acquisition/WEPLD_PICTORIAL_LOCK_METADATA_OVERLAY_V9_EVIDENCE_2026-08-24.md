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

## Independent exact-head review repair — F1/F2/F3

The independent review of rejected v9 head
`9d7cec43dca2a41a149f7749aa5f6cfb1ad25714` identified three findings.
This evidence revision records the bounded repair design only; it does not grant
merge, dependency, donor, product-runtime, provider/model, or completion authority.

### F1 — current no-snapshot canonical progression

After v9 is canonical, the first source-admission candidate must converge the exact
trusted v9 policy base with the exact repaired source reference
`04cc279133d536e2b4b68e01c019d7b595f0ed42`. The candidate is accepted only when:

- every changed path relative to the trusted policy base is a v7-classified
  Pictorial/Agile source/provenance/legal path;
- the complete source surface (Git mode + blob identity) is byte-identical to the
  exact repaired reference source surface;
- the repaired vendor, Pictorial, Agile, package.json, and bun.lock identities
  remain the content-addressed values recorded above; and
- the candidate commit is an exact two-parent convergence of the repaired reference
  and the trusted v9 policy base.

The raw `04cc279...` tree by itself is not an admission candidate after v9 becomes
canonical because it does not contain the canonical v9 policy/evidence bytes. A
fresh convergence candidate is therefore required and remains separately governed.

### F2 — pre-merge remote and post-merge local activation topology

Remote PR qualification and post-merge local activation intentionally use different
view types. v9 now verifies the same source-surface identity in both cases instead
of requiring a LocalRepositoryView to satisfy RemoteRepositoryView type checks.

For pre-merge qualification, the remote candidate must have exactly the repaired
reference and trusted v9 policy base as its two parents. For post-merge activation,
the pushed local checkout must be the merge of the trusted v9 policy base and that
qualified convergence candidate. The convergence candidate itself must still have
exactly the repaired reference and trusted v9 policy base as parents. This preserves
repair lineage across both stages without weakening the data-only PR gate.

### F3 — evidence retention

Whenever the v9 policy wrapper is present, this evidence file is mandatory and its
Git blob must equal the policy-bound evidence identity. Deletion, rename, or byte
mutation fails closed. The v9 self-tests include explicit deletion and mutation
negative oracles.

```text
REJECTED_V9_HEAD=9d7cec43dca2a41a149f7749aa5f6cfb1ad25714
REVIEW_RESULT=FAIL_REPAIRED_BY_SUCCESSOR_CANDIDATE
F1_CURRENT_NO_SNAPSHOT_PROGRESSION=REPAIRED_IN_CANDIDATE
F2_LOCAL_REMOTE_ACTIVATION_TOPOLOGY=REPAIRED_IN_CANDIDATE
F3_EVIDENCE_RETENTION=REPAIRED_IN_CANDIDATE
DEPENDENCY_ADMISSION=NONE
PACKAGE_EXECUTION=NONE
DONOR_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
CANONICAL_POLICY_MERGE=NOT_AUTHORIZED
PR164_READY=NOT_AUTHORIZED
PR162_MERGE=NOT_AUTHORIZED
PR136_MERGE=NOT_AUTHORIZED
```

## F2 exact local+remote activation repair — successor correction

The first F1/F2 successor candidate repaired the intended topology but an actual
`verify-local --remote-baseline` diagnostic against exact head
`7d24c3047191822d687b5fb3cd52e228a6353651` exposed a remaining F2 defect:
a later callback can compare two LocalRepositoryView instances after the canonical
v5 runner has already established the trusted remote-baseline client. The prior
helper rejected that callback with `v9 repaired-source admission requires one
trusted remote view`.

This successor does not weaken lineage, source-surface, tree, package.json, lock,
or evidence checks. It creates one scoped GitHubClient only inside the existing
`verify-local --remote-baseline` entrypoint, makes that client available to nested
local/local callbacks, and clears it in `finally`. A Local+Local callback outside
that exact remote-baseline scope remains fail-closed.

```text
F2_REJECTED_HEAD=7d24c3047191822d687b5fb3cd52e228a6353651
F2_FAILURE=v9 repaired-source admission requires one trusted remote view
F2_REPAIR=SCOPED_REMOTE_BASELINE_CLIENT_BRIDGE
DEPENDENCY_ADMISSION=NONE
PACKAGE_EXECUTION=NONE
DONOR_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
CANONICAL_POLICY_MERGE=NOT_AUTHORIZED
PR164_READY=NOT_AUTHORIZED
PR162_MERGE=NOT_AUTHORIZED
PR136_MERGE=NOT_AUTHORIZED
```

