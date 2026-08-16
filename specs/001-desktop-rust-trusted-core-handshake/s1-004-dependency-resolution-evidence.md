# S1-004 Dependency-Resolution Evidence Reconciliation

## Status

```text
TASK = S1-004
EVIDENCE_SUBJECT_HEAD = d818e553734e2b9e8e48ae31825728bdf3366b3e
EVIDENCE_SUBJECT_PARENT = 3c4e8634c2b0031c70ee0e2350c80d6eae0a67f3
BASE_MAIN = af000ec9cd4a1ce71545cdc509f13af0e69429f9
STAGE = S1_DEPENDENCY_RESOLUTION_LOCKED
S1_004_EVIDENCE_RECONCILIATION = BLOCKED
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

This record preserves the resolved-graph evidence and its current disposition. It is not a component-admission record and does not authorize S1-005 or product implementation.

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

## Raw evidence set

Raw evidence was generated outside the repository and retained locally at generation time under:

```text
C:\tmp\WEPLD_S1_004_EVIDENCE_d818e553
```

Important artifact SHA-256 values:

```text
cargo-audit.json = b60f76550a97fc383109143356e13587bd1f854ba64d5a4e32ddc8d99662a922
cargo-audit.stderr.txt = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
cargo-audit-version.txt = 9d260002c140970623cc62813823d8d73ba944dd85fa8a42ed0af01c2add4789
cargo-duplicates.txt = 979038dd1844a5fa6ba15fcdc4219603d0ccca3178138d15324cb749739d2719
cargo-feature-tree-all-targets.txt = 9a3f51aa27c74bf6488b550fa388765ef599c56c8288f0e3bea981abcc51ca15
cargo-metadata.json = 3580ea8d5e1baa5ff1f035716cddfb7fc8f94f326fffd1f1e5c9ecc529909012
cargo-tree-all-targets.txt = 7e45eae9eb41f21bbc71157bf6363b1e0de48b2e78e88f7d416d1d937aec0644
warning-advisories.csv = 29dd879f77e8c861c710406bd9f1eb12ec0a395d94a4fffd0abeda10981dc4a7
resolved-multiversion-packages.csv = 5751599ae23883702c9e5b27f2bb115c67a454faffa331e99772bcc31cc92676
rustsec-advisory-db-head.txt = e2baa36bc841cd47c82533560b4c21ebecc584816f3697131f2ce0f545f8ebfd
```

CycloneDX 1.5 SBOM outputs:

```text
wepld-desktop_all.cdx.json = 5fdca0bd4a169d13cfe1fda8eeb57c5aad9721bc57749063bf80d38fd1991162
wepld-contracts_all.cdx.json = fd994e8ffad3e22628645d367508d0ee60d6de179c1ee0ef462361a61d05052c
wepld-core_all.cdx.json = b7350beb7c4b7aa3117d188c31bcc35074ed3994713688646a6697fcfd591757
```

RustSec advisory database identity used by the scan:

```text
69f93e1d081d8b6fbee010e48f0b5e0d13661415
```

## Advisory scan result

```text
CARGO_AUDIT_VERSION = 0.22.2
CARGO_AUDIT_EXIT = 0
VULNERABILITIES = 0
WARNINGS = 15
UNMAINTAINED = 14
UNSOUND = 1
```

`cargo audit` exit success is not treated as warning acceptance. Every warning is reconciled below.

### RUSTSEC-2024-0429 — glib 0.18.5

```text
CATEGORY = unsound
CURRENT_VERSION = 0.18.5
PATCHED = >=0.20.0
UNAFFECTED = <0.15.0
DISPOSITION = BLOCK
MATERIALITY = MATERIAL / SECURITY-RELEVANT
```

The pinned RustSec record states that `glib::VariantStrIter` iterator implementations perform unsound mutation through an immutable reference, resulting in undefined behaviour and observed optimized-build null-pointer crashes. The affected range is `>=0.15.0,<0.20.0`.

This is not a false positive and is not irrelevant to S1 platform scope:

- canonical S1 acceptance requires Linux compile plus protocol/contract evidence;
- Tauri `2.11.5` directly selects `gtk = 0.18` on Linux/BSD-family targets;
- the pinned Tauri upstream audit configuration explicitly records `RUSTSEC-2024-0429` as an ignored known debt and states that it is fixed by updating to GTK4;
- the current WePLD candidate directly pins Tauri `=2.11.5` with the `wry` feature, so a manifest feature toggle does not remove Tauri's Linux GTK3 dependency.

Therefore the current Tauri 2.11.5 graph is **not eligible for final runtime dependency admission** while Linux remains part of S1 acceptance.

Required resolution is one of:

1. requalify a framework/runtime graph that removes the affected GTK3/GLib 0.18 path; or
2. make an explicit canonical platform-scope change with corresponding acceptance/security consequences.

The second option must not occur implicitly as an advisory waiver.

### Informational unmaintained warnings

The following 14 warnings are valid informational maintenance findings. They are not security vulnerabilities by themselves and do not independently block S1-004 while the unsoundness blocker remains open. They remain tracked dependency-health debt and require explicit S1-005 admission disposition/replacement strategy.

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

Observed names include `syn`, `toml`, `toml_edit`, `windows-sys`, `windows-targets`, `getrandom`, `schemars`, and others. No bulk deduplication or manifest override is authorized from this observation alone. Any optimization must preserve the exact graph and undergo a fresh lock/SBOM/advisory pass.

## Evidence coverage gaps discovered during reconciliation

Two generated capture files are empty by SHA-256 identity:

```text
cargo-cyclonedx-attestation.txt = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
cargo-cyclonedx-version.txt = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This means the run may have succeeded operationally, but the textual tool-version/attestation outputs were not retained in those files. They must not be represented as retained evidence.

Additionally, `RECONCILIATION_INPUT.txt` was created after the last enumerated evidence-file set used to produce `SHA256SUMS.txt`, so the current checksum manifest is not a final closure manifest for every later reconciliation file.

Disposition:

```text
CYCLONEDX_BYTES = RETAINED_BY_SHA256
CYCLONEDX_TOOL_VERSION_CAPTURE = INCOMPLETE
CYCLONEDX_ATTESTATION_CAPTURE = INCOMPLETE
FINAL_EVIDENCE_MANIFEST_CLOSURE = INCOMPLETE
```

These are evidence-quality gaps and must be repaired before an S1-004 completion claim.

## Per-advisory inverse-tree evidence hashes

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
RUSTSEC-2025-0098 unic-ucd-version 0.9.0 = 630990b59392412f3f3b3df681cc03269da66748698a1326406bff6cc1a54964
RUSTSEC-2025-0100 unic-ucd-ident 0.9.0 = 3a03def41e50bd8679823661f311e03155309d594fa69fad90a58691012b012c
```

The raw inverse-tree bytes remain external evidence; these hashes preserve identity but do not substitute for future canonical artifact-retention policy.

## Current decision

```text
S1_004_STAGE_B2 = QUALIFIED
RESOLVED_GRAPH = GENERATED
SBOM = GENERATED_EXTERNAL_RAW_EVIDENCE
ADVISORY_SCAN = COMPLETED
ADVISORY_RECONCILIATION = BLOCKED_ON_RUSTSEC_2024_0429
EVIDENCE_CAPTURE_CLOSURE = INCOMPLETE
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
S1_005 = NOT_AUTHORIZED_BY_THIS_RECORD
```

No green CI status, upstream ignore list, or zero-vulnerability count overrides the unresolved unsoundness finding or the evidence-capture gaps.