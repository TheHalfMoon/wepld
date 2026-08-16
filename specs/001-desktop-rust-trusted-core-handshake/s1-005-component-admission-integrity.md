# S1-005 — exact frozen-component admission-policy migration

## Identity

```text
TASK = S1-005
POLICY_BASE_MAIN = f1919396eacb90d8d947b06f023ae9da233a4580
POLICY_BASE_TREE = 902265157e9db7a0775d9794edd9db8d03724354
PREP_VENDOR_HEAD = f13b214c6fe42fec80b9ce05f44f7ea2a96da3e5
PREP_VENDOR_TREE = c064fcd71830730d12645b54228326cefefd6188
PATCHED_VARIANT_BLOB = e0997f651b103f7b198e528ee41137ad374e19b8
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

This migration changes only the integrity policy needed to inspect one exact S1 component-acquisition candidate. It does not merge the vendor candidate, admit any runtime dependency, waive any advisory, or authorize product behavior.

## Why a new stage is required

S1-004 proved the exact Cargo graph and handed `RUSTSEC-2024-0429` (`glib 0.18.5`) to S1-005 as a material security blocker. Official-byte acquisition and independent reproduction established a narrow security backport candidate, and Cargo resolution proved that selecting the frozen path override changes `glib 0.18.5` into a source-less/checksum-less path package while leaving the resolved package count at 417.

The current trusted policy intentionally rejects both `third_party/**` and every source-less package except the three Stage-B workspace packages. That remains correct for ordinary Stage B. A separately governed policy migration is therefore required before the exact frozen component can be presented to the trusted gate.

```text
FROZEN_COMPONENT_CANDIDATE != RUNTIME_DEPENDENCY_ADMISSION
PATH_OVERRIDE_SELECTED != SECURITY_ADVISORY_CLOSED
POLICY_MIGRATION_MERGED != SOURCE_ACQUISITION_PASS
```

## New stage

The policy adds exactly one stage:

```text
S1_COMPONENT_ACQUISITION_CANDIDATE
```

A candidate enters this stage when any tracked path begins with `third_party/`. The candidate must also contain the complete existing Stage-B2 path set. Partial component candidates fail closed.

The only eligible vendor prefix is:

```text
third_party/glib-0.18.5-wepld1
```

Prefix membership is not authority. The Git subtree object must be exactly:

```text
c064fcd71830730d12645b54228326cefefd6188
```

That tree identity binds the complete descendant path set, file modes, and blob identities. The independently verified patched `src/variant_iter.rs` blob inside that tree is recorded as corroborative acquisition evidence; enforcement of that file identity is transitive through the exact subtree SHA rather than a second independent runtime check:

```text
e0997f651b103f7b198e528ee41137ad374e19b8
```

Any file addition, deletion, byte change, or mode change changes the subtree identity and is rejected.

## Exact Cargo contract

In this stage only, root `Cargo.toml` is exactly:

```toml
[workspace]
resolver = "2"
members = [
  "apps/desktop/src-tauri",
  "crates/contracts",
  "crates/core",
]

[patch.crates-io]
glib = { path = "third_party/glib-0.18.5-wepld1" }
```

All other Stage-B manifests, skeletons, and `rust-toolchain.toml` retain their existing exact byte contracts.

The resolution-only probe on Rust `1.97.1` produced:

```text
CARGO_TOML_SHA256 = 6688d45616ad298c0e89d0a792d0fe9e2b1e86165089956ce1c273c58b6d73a9
CARGO_LOCK_SHA256 = 3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9
LOCK_PACKAGE_COUNT = 417
CARGO_TREE_FEATURES_SHA256 = aea7d62ec7c22290ad4b975ba7167750d065fb0bc9d27d0a9e96a4456bd7f0e2
GLIB_REVERSE_TREE_SHA256 = 09bb41be5e50873e99d8dd90e76b25f1f3497d2777b859b4c169133ff3095e8f
```

The exact `glib 0.18.5` package entry has no `source` and no `checksum`, as Cargo requires for the selected path source. The component stage additionally requires the complete `Cargo.lock` bytes to match the independently reproduced SHA-256 `3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9`. A structurally plausible but hand-edited component lock is rejected.

The policy also requires the exact source-less `glib 0.18.5` identity to be transitively reachable from the `wepld-desktop 0.0.0` workspace root in the resolved lock graph. Mere presence of a disconnected source-less glib table is not component-acquisition evidence.

## Lock fail-closed rule

Ordinary Stage B2 is unchanged: source-less package identities remain restricted to the exact three WePLD workspace packages.

Only in `S1_COMPONENT_ACQUISITION_CANDIDATE`:

```text
("glib", "0.18.5")
```

must be present and must be source-less/checksum-less. A registry-sourced `glib 0.18.5` in this stage is rejected because it proves the frozen path override was not selected. No other source-less package becomes eligible.

```text
SOURCELESS_GLIB_WITH_EXACT_FROZEN_TREE_AND_EXACT_LOCK_AND_REACHABILITY = COMPONENT_CANDIDATE_EVIDENCE
DISCONNECTED_SOURCELESS_GLIB = REJECT
COMPONENT_LOCK_SHA256_DRIFT = REJECT
SOURCELESS_GLIB_WITHOUT_EXACT_FROZEN_TREE = REJECT
ARBITRARY_SOURCELESS_PACKAGE = REJECT
```

## Trusted remote inspection

The repository-view abstraction gains subtree identity inspection.

For local self-checks, the subtree identity is resolved from the committed Git tree. For the trusted remote path, `RemoteRepositoryView` records tree objects from the already identity-bound recursive Git tree response. Candidate source remains data only.

```text
CANDIDATE_CHECKOUT_BY_PULL_REQUEST_TARGET = NONE
CANDIDATE_CODE_EXECUTION = NONE
CANDIDATE_VENDOR_EXECUTION = NONE
CANDIDATE_BUILD = NONE
SUBTREE_IDENTITY_SOURCE = GIT_OBJECT_DATA
```

The root recursive tree response remains bound to the exact requested root tree SHA before entries are consumed. Subtree SHA values are required to be syntactically valid Git object identities before they are retained.

## Acquisition evidence bound to this migration

Official source:

```text
URL = https://static.crates.io/crates/glib/glib-0.18.5.crate
PUBLISHED_CRATE_SHA256 = 233daaf6e83ae6a12a52055f568f9d7cf4671dabb78ff9560ab6da230ce00ee5
SOURCE_VCS_SHA = 42b9caf98e03ded086362d9653ca58fe94dc8658
PUBLISHED_FILES = 121
```

Frozen candidate:

```text
PUBLISHED_TO_VENDOR_CHANGED_FILES = src/variant_iter.rs
VENDOR_FILES = 121
VENDOR_TREE_SHA = c064fcd71830730d12645b54228326cefefd6188
PATCHED_VARIANT_BLOB = e0997f651b103f7b198e528ee41137ad374e19b8
PATCH_SHA256 = 586516d5219b681bbb9692380cf37370056ced644e2b3fb4c24cfefd43813a95
```

GitHub-side acquisition and post-run independent rehashing both reproduced the same identities. Issue #8 is the durable evidence ledger.

## Deterministic probes

The candidate policy must retain all existing S1-003 probes and add at least:

- arbitrary `third_party/evil/**` rejection;
- missing frozen vendor subtree identity;
- malformed frozen vendor subtree identity;
- wrong frozen vendor subtree identity;
- trusted remote recursive-tree capture of the exact frozen subtree identity;
- trusted remote rejection of malformed subtree SHA and non-tree mode;
- frozen vendor present with the old root Cargo template;
- patched root Cargo presented as ordinary Stage B2 without a vendor stage;
- source-less `glib 0.18.5` rejected in ordinary Stage B2;
- registry-sourced `glib 0.18.5` rejected in the component stage;
- disconnected source-less `glib 0.18.5` rejected for missing workspace reachability;
- synthetic/hand-edited component lock bytes rejected unless the exact frozen lock SHA-256 matches;
- positive reachable frozen-component graph fixture, with the exact production lock exercised by the remote-object canary;
- all existing source, symlink, gitlink, case-fold, policy-control, immutable-baseline, object-identity, and trusted-base path-preservation probes.

Every negative probe must assert the intended rejection reason.

## Bootstrap limitation

`.github/scripts/wepld_integrity.py` is a base-controlled judge. The current trusted-base `s1-admission-integrity` must therefore reject the PR that changes it.

```text
CURRENT_TRUSTED_BASE_REJECTION_OF_POLICY_MUTATION = EXPECTED
EXPECTED_REJECTION != POLICY_PASS
EXPECTED_REJECTION != MERGE_AUTHORITY
```

Following the S1-003 precedent, this policy migration requires:

```text
PR_HEAD_FOUNDATION_SELFCHECK = REQUIRED
SECURITY_REVIEW_APPLICABILITY = APPLICABLE
INDEPENDENT_CORRECTNESS_REVIEW = REQUIRED
EXACT_HEAD_BINDING = REQUIRED
FOUNDER_BOOTSTRAP_ACCEPTANCE = REQUIRED
POST_MERGE_MAIN_INTEGRITY = REQUIRED
FIRST_POST_MERGE_TRUSTED_BASE_CANARY = REQUIRED
```

The exact eventual policy PR head is intentionally not recorded here because doing so would recursively change that identity.

If Codex Security is unavailable in the execution host, record `NOT_RUN_NON_BLOCKING`; never relabel it PASS. Cubic remains blocked until provider-effective state is independently proven safe.

## Activation boundary

Even after this migration is merged:

```text
PREP_VENDOR_PR_ELIGIBLE = NO
```

until a fresh docs-only canary proves the newly canonical trusted-base `s1-admission-integrity` can inspect an ordinary candidate successfully.

Only after that activation proof may the frozen prep branch be updated with the exact root Cargo path override and regenerated lock, then presented as the S1-005 component-acquisition candidate.

Product implementation remains blocked throughout this migration.


## Exact-head review reconciliation — Qodo

On exact PR head `95aaf017c8af1dca41aa663283b63dc77cc94d7c`, Qodo identified that a disconnected source-less `glib 0.18.5` table could satisfy the component lock validator because structural edge resolution did not establish workspace reachability. The finding was independently reconciled as `VALID / MATERIAL / SECURITY_RELEVANT`. The repair requires both transitive reachability from `wepld-desktop` and the exact independently reproduced component-lock SHA-256.

Qodo also noted that `FROZEN_GLIB_PATCHED_VARIANT_BLOB_SHA` was not read by policy logic. That finding is `VALID / NON-MATERIAL`: the exact vendor subtree identity already transitively binds the patched blob. The constant remains as corroborative acquisition evidence and is now explicitly documented as such.
