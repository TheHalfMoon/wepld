# S1-004 Dependency-Resolution Evidence Reconciliation

## Status

```text
TASK = S1-004
EVIDENCE_SUBJECT_HEAD = d818e553734e2b9e8e48ae31825728bdf3366b3e
EVIDENCE_SUBJECT_PARENT = 3c4e8634c2b0031c70ee0e2350c80d6eae0a67f3
BASE_MAIN = af000ec9cd4a1ce71545cdc509f13af0e69429f9
STAGE = S1_DEPENDENCY_RESOLUTION_LOCKED
S1_004_TECHNICAL_EXECUTION = COMPLETE
S1_004_PR_REVIEW = PENDING_EXACT_HEAD_REREVIEW
S1_004_MERGE = NO
ADVISORY_RECONCILIATION = HANDOFF_TO_S1_005
S1_005_ADMISSION_BLOCKER = RUSTSEC-2024-0429
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

This record preserves the S1-004 resolved-graph evidence and its current disposition. S1-004 generated the candidate lock, dependency tree, SBOM, and advisory scan required by the task ledger. Final advisory disposition and runtime component admission remain S1-005 responsibilities. This record does not authorize S1-005, dependency admission, product implementation, Ready state, or merge.

## Lock identity and generation provenance

```text
RUST_TOOLCHAIN = 1.97.1
LOCK_GENERATOR = cargo +1.97.1 generate-lockfile
LOCK_GENERATION_HOST = founder Windows PowerShell environment
CARGO_LOCK_SHA256 = 6ec6c22aa5bbde22d0a0b1a1e384e375a77c4e011e97c357fdd918788d0e8007
CARGO_LOCK_GIT_BLOB = 4ae63bab12b9057f245df2c06d6604da244464cc
LOCK_PACKAGE_TABLES = 417
METADATA_PACKAGES = 417
RESOLVE_NODES = 417
```

The Stage-B policy independently classified the exact lock head as `S1_DEPENDENCY_RESOLUTION_LOCKED` in both the PR-head self-check and the trusted-base `pull_request_target` path. That stage classification is dependency-resolution evidence only.

## Raw evidence retention boundary

Raw evidence was generated outside the repository and retained locally at generation time under:

```text
C:\tmp\WEPLD_S1_004_EVIDENCE_d818e553
```

The Stage-B integrity policy permits ordinary additions under `docs/` and `specs/` only when they are Markdown. Therefore the JSON, CSV, CycloneDX JSON, and text artifacts listed below are **not stored as raw bytes in the PR tree**. GitHub retention in this record is currently:

```text
GITHUB_RETENTION = SUMMARY + COMPLETE_RECORDED_SHA256_IDENTITIES
RAW_EVIDENCE_BYTES_IN_PR_TREE = NO
RAW_EVIDENCE_BYTES_LOCAL_ONLY = YES_AT_GENERATION_TIME
RAW_EVIDENCE_DURABLE_REMOTE_RETENTION = NOT_YET_PROVEN
```

A digest proves identity of bytes if those bytes are later recovered; it does not preserve the bytes themselves. No statement in this record may represent the raw external evidence as durably retained on GitHub.

## Complete recorded SHA-256 manifest

The following is the complete `SHA256SUMS.txt` printed by the founder evidence run. It enumerates all 37 files that existed when that manifest was generated:

```text
b60f76550a97fc383109143356e13587bd1f854ba64d5a4e32ddc8d99662a922  cargo-audit.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  cargo-audit.stderr.txt
9d260002c140970623cc62813823d8d73ba944dd85fa8a42ed0af01c2add4789  cargo-audit-version.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  cargo-cyclonedx-attestation.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  cargo-cyclonedx-version.txt
979038dd1844a5fa6ba15fcdc4219603d0ccca3178138d15324cb749739d2719  cargo-duplicates.txt
9a3f51aa27c74bf6488b550fa388765ef599c56c8288f0e3bea981abcc51ca15  cargo-feature-tree-all-targets.txt
15eff4461bf66d6dccb78190cc2ea29bbb194742f4c6e7aaabcefc0c0c89a6a1  cargo-lock-git-blob.txt
3787fee2417ddfae047ef0e82047c7d06f73985ac93fca736b36f97583fe1788  cargo-lock-sha256.txt
3580ea8d5e1baa5ff1f035716cddfb7fc8f94f326fffd1f1e5c9ecc529909012  cargo-metadata.json
7e45eae9eb41f21bbc71157bf6363b1e0de48b2e78e88f7d416d1d937aec0644  cargo-tree-all-targets.txt
766601879d48aaeb37f00ff03a4bc31bdb9363c94c126373a066bd53707db06f  cargo-version.txt
1e2ba035649c9b4adebb63d2af39cecfd0f1022a763f2a0b0d8a5f669afaa8a3  repo-head.txt
937e7459c4af8ec40e8971497136f83071f2f15935cd55e2fc1c122ac459adb7  repo-head-parent.txt
5751599ae23883702c9e5b27f2bb115c67a454faffa331e99772bcc31cc92676  resolved-multiversion-packages.csv
fdfc4e42096cc27917cf06c52047e615ad79bf22a87a608438581be934fd2f8e  rustc-vv.txt
e2baa36bc841cd47c82533560b4c21ebecc584816f3697131f2ce0f545f8ebfd  rustsec-advisory-db-head.txt
5fdca0bd4a169d13cfe1fda8eeb57c5aad9721bc57749063bf80d38fd1991162  sbom__apps__desktop__src-tauri__wepld-desktop_all.cdx.json
fd994e8ffad3e22628645d367508d0ee60d6de179c1ee0ef462361a61d05052c  sbom__crates__contracts__wepld-contracts_all.cdx.json
b7350beb7c4b7aa3117d188c31bcc35074ed3994713688646a6697fcfd591757  sbom__crates__core__wepld-core_all.cdx.json
997b8aeacec08b44ec779765b578d1b89a8f0381ef79946f5bf0f8748817e3e2  SUMMARY.txt
29dd879f77e8c861c710406bd9f1eb12ec0a395d94a4fffd0abeda10981dc4a7  warning-advisories.csv
0b9801f2e809dfaba6c247c6fb80306179b7e33f6a7214295b489143323ad1da  warning-tree__RUSTSEC-2024-0370__proc-macro-error__1.0.4.txt
9119dc138ebbbd58dc1ab28fb112eea7c31d21640bfd908b14e06f061d298c0d  warning-tree__RUSTSEC-2024-0411__gdkwayland-sys__0.18.2.txt
f786ad0ec554d24f5de3913f1ff638627edf514e102ce513d08a824c644a73b0  warning-tree__RUSTSEC-2024-0412__gdk__0.18.2.txt
79ebd0a01e6daff03cbb1332aa0ed1b93c36dea1ec83d5d3617e4ae20f47c209  warning-tree__RUSTSEC-2024-0413__atk__0.18.2.txt
005bb6f40d6dee24463a11b6eb13c7c59032b018ea3203050b5999353d264bf3  warning-tree__RUSTSEC-2024-0415__gtk__0.18.2.txt
518147028170aba26cb996ebba3d7cea43a4e2ec71a55aa1f27ffe7b7956f755  warning-tree__RUSTSEC-2024-0416__atk-sys__0.18.2.txt
de25abccec14ea7477a59b13743117ad93f9873870f8e86eb3cf6b5a9ad62ba7  warning-tree__RUSTSEC-2024-0418__gdk-sys__0.18.2.txt
ee4c6728556c05c96b9096bbb77212aa09e01bdc14a1747ee652831ccc51e731  warning-tree__RUSTSEC-2024-0419__gtk3-macros__0.18.2.txt
46a8059080c4b3a816e7a72c6ab1137709460522a52d196685569d316c06efd5  warning-tree__RUSTSEC-2024-0420__gtk-sys__0.18.2.txt
aa8b3adee3f46131af32c9e02c45a00a19cafb5802194ed1a104a4d7a37cf0d0  warning-tree__RUSTSEC-2024-0429__glib__0.18.5.txt
0daee41183cc8d54ea3f9a1ac3c0a1d2fa0e8731e0bae4e761020c164869a0c2  warning-tree__RUSTSEC-2025-0075__unic-char-range__0.9.0.txt
33f71f773592463e7742ab86ab355a765788f63d27a04ead303543eaba7f88ac  warning-tree__RUSTSEC-2025-0080__unic-common__0.9.0.txt
5068399e3ec4890b789b5ff8fbc62a332db9f7f3f94679b482020059dfde213a  warning-tree__RUSTSEC-2025-0081__unic-char-property__0.9.0.txt
630990b59392412f3f3b3df681cc03269da66748698a1326406bff6cc1a54964  warning-tree__RUSTSEC-2025-0098__unic-ucd-version__0.9.0.txt
3a03def41e50bd8679823661f311e03155309d594fa69fad90a58691012b012c  warning-tree__RUSTSEC-2025-0100__unic-ucd-ident__0.9.0.txt
```

## Evidence-run summary retained in GitHub

```text
TIMESTAMP_UTC=2026-08-16T15:22:49.1712354Z
REPO_HEAD=d818e553734e2b9e8e48ae31825728bdf3366b3e
STAGE=S1_DEPENDENCY_RESOLUTION_LOCKED
RUST_TOOLCHAIN=1.97.1
LOCK_PACKAGE_TABLES=417
METADATA_PACKAGES=417
RESOLVE_NODES=417
DUPLICATE_TREE_LINES=920
CARGO_AUDIT_VERSION=0.22.2
CARGO_AUDIT_EXIT=0
RUSTSEC_ADVISORY_DB_HEAD=69f93e1d081d8b6fbee010e48f0b5e0d13661415
AUDIT_VULNERABILITY_COUNT=0
AUDIT_WARNING_SUMMARY=unmaintained=14,unsound=1
CARGO_CYCLONEDX_VERSION=0.5.9
CYCLONEDX_SPEC=1.5
CYCLONEDX_TARGET=all
CYCLONEDX_SOURCE_DATE_EPOCH=1786892865
SBOM_FILE_COUNT=3
REPOSITORY_STATUS_AFTER_EVIDENCE=CLEAN
SOURCE_ACQUISITION_CHECK=OPEN
RUNTIME_DEPENDENCY_ADMISSION=NONE
PRODUCT_IMPLEMENTATION=BLOCKED
```

The `DUPLICATE_TREE_LINES=920` field is the raw output-line count captured by the earlier evidence script; it is **not** interpreted as a count of duplicate package identities. Metadata reconciliation below is authoritative for multi-version package-name analysis.

## Advisory scan result

```text
CARGO_AUDIT_VERSION = 0.22.2
CARGO_AUDIT_EXIT = 0
VULNERABILITIES = 0
WARNINGS = 15
UNMAINTAINED = 14
UNSOUND = 1
```

`cargo audit` exit success is not treated as warning acceptance. Every reportable warning remains visible to S1-005 admission review.

### RUSTSEC-2024-0429 — glib 0.18.5

```text
CATEGORY = unsound
CURRENT_VERSION = 0.18.5
PATCHED = >=0.20.0
UNAFFECTED = <0.15.0
DISPOSITION = BLOCK_FINAL_ADMISSION
MATERIALITY = MATERIAL / SECURITY-RELEVANT
S1_004_EFFECT = HANDOFF_FINDING
S1_005_EFFECT = ADMISSION_BLOCKER_UNTIL_RECONCILED
```

The pinned RustSec record states that `glib::VariantStrIter` iterator implementations perform unsound mutation through an immutable reference, resulting in undefined behaviour and observed optimized-build null-pointer crashes. The affected range is `>=0.15.0,<0.20.0`.

This is not a false positive and is not irrelevant to S1 platform scope:

- canonical S1 acceptance requires Linux compile plus protocol/contract evidence;
- Tauri `2.11.5` directly selects `gtk = 0.18` on Linux/BSD-family targets;
- the pinned Tauri upstream audit configuration explicitly records `RUSTSEC-2024-0429` as an ignored known debt and states that it is fixed by updating to GTK4;
- the current WePLD candidate directly pins Tauri `=2.11.5` with the `wry` feature, so a manifest feature toggle does not remove Tauri's Linux GTK3 dependency.

Therefore the current Tauri 2.11.5 graph is **not eligible for final runtime dependency admission** while Linux remains part of S1 acceptance. S1-004 records this truth; S1-005 must resolve it before `SOURCE_ACQUISITION_CHECK = PASS` can be claimed.

Potential S1-005 resolution families include requalifying a framework/runtime graph that removes the affected GTK3/GLib 0.18 path, or a separately governed security backport/replacement strategy. A platform-scope change must never be used as an implicit advisory waiver.

### Informational unmaintained warnings

The following 14 warnings are valid informational maintenance findings. They are not security vulnerabilities by themselves and do not independently invalidate S1-004 dependency-resolution execution. They remain tracked dependency-health debt and require explicit S1-005 admission disposition/replacement strategy.

```text
RUSTSEC-2024-0370 | proc-macro-error 1.0.4 | DEFER / TRACK | no patched release
RUSTSEC-2024-0411 | gdkwayland-sys 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0412 | gdk 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0413 | atk 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0415 | gtk 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0416 | atk-sys 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0418 | gdk-sys 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0419 | gtk3-macros 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2024-0420 | gtk-sys 0.18.2 | DEFER / TRACK | GTK3 binding unmaintained
RUSTSEC-2025-0075 | unic-char-range 0.9.0 | DEFER / TRACK | rust-unic family unmaintained
RUSTSEC-2025-0080 | unic-common 0.9.0 | DEFER / TRACK | rust-unic family unmaintained
RUSTSEC-2025-0081 | unic-char-property 0.9.0 | DEFER / TRACK | rust-unic family unmaintained
RUSTSEC-2025-0098 | unic-ucd-version 0.9.0 | DEFER / TRACK | rust-unic family unmaintained
RUSTSEC-2025-0100 | unic-ucd-ident 0.9.0 | DEFER / TRACK | rust-unic family unmaintained
```

Additional observations:

- RustSec recommends maintained alternatives for `proc-macro-error` and the `rust-unic` family, but direct substitution is controlled by upstream dependants and is not silently rewritten in WePLD.
- Tauri 2.11.5's own upstream audit records GTK3 and rust-unic maintenance warnings. Upstream allowance is context, not WePLD admission authority.

## Multi-version graph observation

The resolved metadata contains 32 package names with more than one resolved version. This is not automatically a defect: Cargo may legitimately resolve semver-incompatible versions simultaneously.

```text
MULTIVERSION_PACKAGE_NAME_COUNT = 32
```

Observed package names and versions:

```text
base64 | versions=2 | 0.21.7, 0.22.1
bitflags | versions=2 | 1.3.2, 2.13.1
getrandom | versions=3 | 0.2.17, 0.3.4, 0.4.3
hashbrown | versions=2 | 0.12.3, 0.17.1
heck | versions=2 | 0.4.1, 0.5.0
indexmap | versions=2 | 1.9.3, 2.14.0
jni-sys | versions=2 | 0.3.1, 0.4.1
png | versions=2 | 0.17.16, 0.18.1
proc-macro-crate | versions=3 | 1.3.1, 2.0.2, 3.5.0
r-efi | versions=2 | 5.3.0, 6.0.0
schemars | versions=3 | 0.8.22, 0.9.0, 1.2.2
serde_spanned | versions=2 | 0.6.9, 1.1.1
syn | versions=3 | 1.0.109, 2.0.119, 3.0.3
thiserror | versions=2 | 1.0.69, 2.0.20
thiserror-impl | versions=2 | 1.0.69, 2.0.20
toml | versions=3 | 0.8.2, 0.9.12+spec-1.1.0, 1.1.4+spec-1.1.0
toml_datetime | versions=3 | 0.6.3, 0.7.5+spec-1.1.0, 1.1.1+spec-1.1.0
toml_edit | versions=3 | 0.19.15, 0.20.2, 0.25.13+spec-1.1.0
windows_aarch64_gnullvm | versions=2 | 0.42.2, 0.52.6
windows_aarch64_msvc | versions=2 | 0.42.2, 0.52.6
windows_i686_gnu | versions=2 | 0.42.2, 0.52.6
windows_i686_msvc | versions=2 | 0.42.2, 0.52.6
windows_x86_64_gnu | versions=2 | 0.42.2, 0.52.6
windows_x86_64_gnullvm | versions=2 | 0.42.2, 0.52.6
windows_x86_64_msvc | versions=2 | 0.42.2, 0.52.6
windows-core | versions=2 | 0.61.2, 0.62.2
windows-link | versions=2 | 0.1.3, 0.2.1
windows-result | versions=2 | 0.3.4, 0.4.1
windows-strings | versions=2 | 0.4.2, 0.5.1
windows-sys | versions=3 | 0.45.0, 0.59.0, 0.61.2
windows-targets | versions=2 | 0.42.2, 0.52.6
winnow | versions=3 | 0.5.40, 0.7.15, 1.0.4
```

No bulk deduplication or manifest override is authorized from this observation alone. Any optimization must preserve the exact graph and undergo a fresh lock/SBOM/advisory pass.

## Evidence-capture limitations

Two generated capture files are empty by SHA-256 identity:

```text
cargo-cyclonedx-attestation.txt = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
cargo-cyclonedx-version.txt = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The founder console summary separately records `CARGO_CYCLONEDX_VERSION=0.5.9`, but the empty version-capture file means that value is retained as console-summary evidence, not as independently retained tool-output bytes.

Additionally, `RECONCILIATION_INPUT.txt` was created after the enumerated evidence-file set used to produce `SHA256SUMS.txt`, so the checksum manifest is not a final closure manifest for files created later in the reconciliation session.

Disposition:

```text
CYCLONEDX_SBOM_BYTES = GENERATED_AND_IDENTITY_RECORDED
CYCLONEDX_TOOL_VERSION_CONSOLE_SUMMARY = RETAINED
CYCLONEDX_TOOL_VERSION_RAW_CAPTURE = INCOMPLETE
CYCLONEDX_ATTESTATION_RAW_CAPTURE = INCOMPLETE
FINAL_POST_RECONCILIATION_MANIFEST_CLOSURE = INCOMPLETE
```

These limitations do **not** erase the demonstrated S1-004 generation steps. They remain evidence-retention/closure limitations that must not be mislabeled as complete raw retention and must be reconciled before any final component-admission or S1 acceptance claim that depends on them.

## Per-advisory inverse-tree evidence identities

```text
RUSTSEC-2024-0370 proc-macro-error 1.0.4 = 0b9801f2e809dfaba6c247c6fb80306179b7e33f6a7214295b489143323ad1da
RUSTSEC-2024-0411 gdkwayland-sys 0.18.2 = 9119dc138ebbbd58dc1ab28fb112eea7c31d21640bfd908b14e06f061d298c0d
RUSTSEC-2024-0412 gdk 0.18.2 = f786ad0ec554d24f5de3913f1ff638627edf514e102ce513d08a824c644a73b0
RUSTSEC-2024-0413 atk 0.18.2 = 79ebd0a01e6daff03cbb1332aa0ed1b93c36dea1ec83d5d3617e4ae20f47c209
RUSTSEC-2024-0415 gtk 0.18.2 = 005bb6f40d6dee24463a11b6eb13c7c59032b018ea3203050b5999353d264bf3
RUSTSEC-2024-0416 atk-sys 0.18.2 = 518147028170aba26cb996ebba3d7cea43a4e2ec71a55aa1f27ffe7b7956f755
RUSTSEC-2024-0418 gdk-sys 0.18.2 = de25abccec14ea7477a59b13743117ad93f9873870f8e86eb3cf6b5a9ad62ba7
RUSTSEC-2024-0419 gtk3-macros 0.18.2 = ee4c6728556c05c96b9096bbb77212aa09e01bdc14a1747ee652831ccc51e731
RUSTSEC-2024-0420 gtk-sys 0.18.2 = 46a8059080c4b3a816e7a72c6ab1137709460522a52d196685569d316c06efd5
RUSTSEC-2024-0429 glib 0.18.5 = aa8b3adee3f46131af32c9e02c45a00a19cafb5802194ed1a104a4d7a37cf0d0
RUSTSEC-2025-0075 unic-char-range 0.9.0 = 0daee41183cc8d54ea3f9a1ac3c0a1d2fa0e8731e0bae4e761020c164869a0c2
RUSTSEC-2025-0080 unic-common 0.9.0 = 33f71f773592463e7742ab86ab355a765788f63d27a04ead303543eaba7f88ac
RUSTSEC-2025-0081 unic-char-property 0.9.0 = 5068399e3ec4890b789b5ff8fbc62a332db9f7f3f94679b482020059dfde213a
RUSTSEC-2025-0098 unic-ucd-version 0.9.0 = 630990b59392412f3f3bdf681cc03269da66748698a1326406bff6cc1a54964
RUSTSEC-2025-0100 unic-ucd-ident 0.9.0 = 3a03def41e50bd8679823661f311e03155309d594fa69fad90a58691012b012c
```

The raw inverse-tree bytes remain external evidence; these hashes preserve identity but do not substitute for durable byte retention.

## Current decision

```text
S1_004_TECHNICAL_EXECUTION = COMPLETE
S1_004_STAGE_B2 = QUALIFIED_ON_EVIDENCE_SUBJECT_HEAD
RESOLVED_GRAPH = GENERATED
SBOM = GENERATED_EXTERNAL_RAW_EVIDENCE
ADVISORY_SCAN = COMPLETED
ADVISORY_RECONCILIATION = HANDOFF_TO_S1_005
S1_005_ADMISSION_BLOCKER = RUSTSEC-2024-0429
GITHUB_EVIDENCE_RETENTION = SUMMARY_AND_DIGESTS_ONLY
RAW_EVIDENCE_DURABLE_REMOTE_RETENTION = NOT_YET_PROVEN
S1_004_PR_REVIEW = PENDING_EXACT_HEAD_REREVIEW
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
S1_005 = NOT_STARTED
READY = NO
MERGE = NO
```

No green CI status, upstream ignore list, zero-vulnerability count, digest-only retention, or reviewer output overrides the unresolved unsoundness finding, the raw-retention limitation, or the S1-005 admission boundary.