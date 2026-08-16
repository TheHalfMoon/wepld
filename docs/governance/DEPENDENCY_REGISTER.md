# Dependency Register

```text
FRESH_IMPLEMENTATION_DEPENDENCIES = 0
```

Every future dependency requires capability need, exact version/hash, source-acquisition record, rights/NOTICE, transitive/SBOM/security evidence, maintenance/platform state, admission decision, update plan, and exit strategy.

## Current governed state

```text
REGISTER_SCOPE = S1
S1_SOURCE_ACQUISITION_CHECK = PASS
S1_LOCK_PACKAGE_COUNT = 417
S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 4
S1_EXCEPTIONAL_TRANSITIVE_PATH_OVERRIDES = 1

RUNTIME_DEPENDENCY_ADMISSION = NONE_UNTIL_PR_11_IS_EXACT_HEAD_REVIEWED_ACCEPTED_AND_MERGED
PRODUCT_IMPLEMENTATION = BLOCKED
S1_006 = BLOCKED
```

The exact full graph is identified by `Cargo.lock` and the retained SBOM/evidence
identities. This register records the deliberately exposed/direct or exceptional
components; it does not duplicate all 417 lock entries.

## S1 graph identity

```text
CANONICAL_BASE = 048dc246aea6c17e2b9e0209be2c317a689f61cb
COMPONENT_BYTES_HEAD = 590f7453d022f8192af9a0259560f92de280c8ed
COMPONENT_TREE = 4552c2910de58759ca5d65354dee37a721b1e7c8
CARGO_TOML_SHA256 = 6688d45616ad298c0e89d0a792d0fe9e2b1e86165089956ce1c273c58b6d73a9
CARGO_LOCK_SHA256 = 3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9
LOCK_PACKAGE_COUNT = 417
```

SBOM identities:

```text
wepld-desktop.cdx.json =
  a21aa12d4515cccec075b51f4353a522db45dc956c1a46727f28f69a183e4932
wepld-contracts.cdx.json =
  8653a364db69e5e20d443f4416472d490cc8fbec84742d279cfc62a86a7eb3de
wepld-core.cdx.json =
  614ddacb180edddaf5305ef7bc03ee798213d80686228950f56f571da1cbfe9a
```

## Registered component decisions

### Rust toolchain 1.97.1

```text
ROLE = COMPILER / BUILD TOOLCHAIN
VERSION = 1.97.1
RELEASE_COMMIT = 8bab26f4f68e0e26f0bb7960be334d5b520ea452
ADMISSION_CLASS = TOOLCHAIN
UPDATE_PLAN = PINNED_UPGRADE_WITH_FULL_GATES
EXIT_STRATEGY = NORMAL_RUST_TOOLCHAIN_REPLACEMENT
```

The toolchain grants no runtime authority.

### Tauri 2.11.5

```text
ROLE = DESKTOP_SHELL / WEBVIEW HOST / BUNDLING
VERSION = 2.11.5
SOURCE_COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6
DIRECT_DEFAULT_FEATURES = false
DIRECT_FEATURES = wry
RESOLVED_FEATURES = tauri-runtime-wry,webkit2gtk,webview2-com,wry
LICENSE = Apache-2.0 OR MIT
MAINTENANCE = CURRENT_LATEST_RELEASE_AT_S1_005_RECONCILIATION
ADMISSION_CLASS = DIRECT_RUNTIME_CANDIDATE
```

Boundary:

```text
TAURI_ACL != NAWAT_AUTHORITY
GENERAL_WEBVIEW_SHELL_AUTHORITY = NONE
GENERAL_WEBVIEW_FILESYSTEM_AUTHORITY = NONE
HANDSHAKE_NETWORK_AUTHORITY = NONE
```

Update/exit: preserve WePLD-owned Desktop/Core protocol, process identity, capability
projection, packaging, and cross-platform contracts behind any Tauri upgrade or
replacement.

### tauri-build 2.6.3

```text
ROLE = BUILD-TIME TAURI CONFIG / CODEGEN
VERSION = 2.6.3
SOURCE_COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6
DIRECT_DEFAULT_FEATURES = false
RESOLVED_FEATURES = NONE
LICENSE = Apache-2.0 OR MIT
ADMISSION_CLASS = DIRECT_BUILD_CANDIDATE
```

No runtime authority. It exits with the Tauri packaging path if no longer necessary.

### Serde 1.0.229

```text
ROLE = TYPED SERIALIZATION
VERSION = 1.0.229
RELEASE_COMMIT = 7fc3b4c30c94f73a96ebd1553f2b090d928fc3a8
DIRECT_FEATURES = derive
RESOLVED_FEATURES = alloc,default,derive,rc,serde_derive,std
LICENSE = MIT OR Apache-2.0
ADMISSION_CLASS = DIRECT_RUNTIME_CANDIDATE
```

Exit: replace only behind WePLD-owned protocol types, framing, versioning, validation,
golden fixtures, and negative tests.

### serde_json 1.0.151

```text
ROLE = S1 JSON ENCODING / DECODING
VERSION = 1.0.151
RELEASE_COMMIT = de8500740cdcabffb9734f503e4889def823cf10
RESOLVED_FEATURES = alloc,default,raw_value,std,unbounded_depth
LICENSE = MIT OR Apache-2.0
ADMISSION_CLASS = DIRECT_RUNTIME_CANDIDATE
```

`serde_json::Value` is not the protocol authority. Exit/replacement is qualified through
the same WePLD-owned protocol contract.

### Exceptional vendored glib 0.18.5 security backport

```text
ROLE = TRANSITIVE TAURI LINUX GTK3 DEPENDENCY / SECURITY BACKPORT
UPSTREAM_VERSION = 0.18.5
LICENSE = MIT

PUBLISHED_CRATE_SHA256 = 233daaf6e83ae6a12a52055f568f9d7cf4671dabb78ff9560ab6da230ce00ee5
SOURCE_VCS_SHA = 42b9caf98e03ded086362d9653ca58fe94dc8658
VENDOR_TREE_SHA = c064fcd71830730d12645b54228326cefefd6188
PATCHED_VARIANT_BLOB_SHA = e0997f651b103f7b198e528ee41137ad374e19b8
PATCH_SHA256 = 586516d5219b681bbb9692380cf37370056ced644e2b3fb4c24cfefd43813a95
VENDOR_FILE_COUNT = 121
CHANGED_FILES_FROM_PUBLISHED = src/variant_iter.rs

ADVISORY = RUSTSEC-2024-0429
OFFICIAL_FIXED_RANGE = >=0.20.0
DISPOSITION = EXACT_UPSTREAM_SOUNDNESS_FIX_BACKPORTED_TO_EOL_0_18_LINE
ADMISSION_CLASS = EXCEPTIONAL_TRANSITIVE_PATH_OVERRIDE_CANDIDATE
```

The exact patch is only:

```text
let p  -> let mut p
&p     -> &mut p
```

No generalized fork is admitted.

Exit trigger:

```text
QUALIFIED_TAURI_LINUX_GRAPH_NO_LONGER_REQUIRES_GTK3_GLIB_0_18
```

At exit, remove the crates.io patch and complete vendor subtree, regenerate the lock,
dependency/feature tree, SBOM, license evidence, and advisory evidence, then re-review
the migration.

## Known transitive maintenance debt

Current exact RustSec evidence reports zero vulnerabilities and 14 unmaintained
warnings.

GTK3/Tauri chain:

```text
RUSTSEC-2024-0413 atk 0.18.2
RUSTSEC-2024-0416 atk-sys 0.18.2
RUSTSEC-2024-0412 gdk 0.18.2
RUSTSEC-2024-0418 gdk-sys 0.18.2
RUSTSEC-2024-0411 gdkwayland-sys 0.18.2
RUSTSEC-2024-0415 gtk 0.18.2
RUSTSEC-2024-0420 gtk-sys 0.18.2
RUSTSEC-2024-0419 gtk3-macros 0.18.2
RUSTSEC-2024-0370 proc-macro-error 1.0.4
```

UNIC/Tauri-utils chain:

```text
RUSTSEC-2025-0100 unic-ucd-ident 0.9.0
RUSTSEC-2025-0081 unic-char-property 0.9.0
RUSTSEC-2025-0075 unic-char-range 0.9.0
RUSTSEC-2025-0098 unic-ucd-version 0.9.0
RUSTSEC-2025-0080 unic-common 0.9.0
```

These are accepted only as transitive maintenance debt for the exact graph. Every
dependency refresh/advisory run re-evaluates them; a reportable vulnerability reopens
admission.

## License and distribution evidence

Target-scoped `cargo-deny 0.19.7` license inventories passed for:

```text
x86_64-unknown-linux-gnu
x86_64-pc-windows-msvc
aarch64-apple-darwin
x86_64-apple-darwin
```

Each target had `EXTERNAL_EMPTY_LICENSES = 0`.

Detected Rust-crate identifiers:

```text
0BSD
Apache-2.0
Apache-2.0 WITH LLVM-exception
CC0-1.0
MIT
MIT-0
MPL-2.0
Unicode-3.0
Unlicense
Zlib
```

Evidence artifact:

```text
ID = 9269179220
SHA256 = 0ea6889f3cff9611477a5817ed0f2b169c9a8b62d7767eb02a34de47b5f657c0
INDEPENDENT_REVERIFICATION = PASS
```

This is Rust-crate evidence only. Native system-library distribution obligations are
not waived. The vendored glib COPYRIGHT explicitly preserves the possibility of
LGPL/other obligations for linked GNOME libraries; concrete Linux package compliance
remains required in S1-010.

## Explicit non-admissions

```text
tauri-plugin-shell = NOT_ADMITTED
direct Tokio in Core = NOT_ADMITTED
UUID/random-ID crate = NOT_ADMITTED
RPC framework = NOT_ADMITTED
alternate binary serialization framework = NOT_ADMITTED
React/Vite/Tailwind = NOT_ADMITTED
database = NOT_ADMITTED
network client/server library = NOT_ADMITTED
telemetry SDK = NOT_ADMITTED
```

Transitive presence is not direct WePLD API authority.

## Evidence references

```text
RAW_COMPONENT_EVIDENCE_RUN = 31967901318
RAW_COMPONENT_EVIDENCE_JOB = 95215749968
RAW_COMPONENT_EVIDENCE_ARTIFACT = 9269055750
RAW_COMPONENT_EVIDENCE_SHA256 =
  70698d62180a77a438ce7e690a690d6727c55830ca55c1bd360cc3a2b1f9b1ac

TARGET_LICENSE_RUN = 31968572880
TARGET_LICENSE_JOB = 95217373212
TARGET_LICENSE_ARTIFACT = 9269179220
TARGET_LICENSE_ARTIFACT_SHA256 =
  0ea6889f3cff9611477a5817ed0f2b169c9a8b62d7767eb02a34de47b5f657c0
```

See
`specs/001-desktop-rust-trusted-core-handshake/s1-005-component-admission-evidence.md`
and Issue #8 for acquisition, independent rehashing, warning paths, policy bootstrap,
provider-negative-oracle, and review evidence.

## Authority invariant

```text
SOURCE_ACQUISITION_CHECK_PASS != RUNTIME_DEPENDENCY_ADMISSION
GREEN_CI != COMPLETION_DECISION
CLEAN_REVIEW != COMPLETION_DECISION
MERGE_REQUIRED_BEFORE_RUNTIME_ADMISSION = YES
PRODUCT_IMPLEMENTATION = BLOCKED
S1_006 = BLOCKED
```
