# S1-005 — Final component admission evidence

## Decision scope

This file is the durable closeout record for the S1-005 Source Acquisition Check. It
supersedes only the planning-era **status** statements in `source-acquisition.md`; the
source identities, design rationale, negative oracles, and acquisition history there
remain evidence.

```text
TASK = S1-005
CANONICAL_BASE = 048dc246aea6c17e2b9e0209be2c317a689f61cb
COMPONENT_BYTES_HEAD = 590f7453d022f8192af9a0259560f92de280c8ed
COMPONENT_TREE = 4552c2910de58759ca5d65354dee37a721b1e7c8

SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = NONE_UNTIL_PR_11_IS_EXACT_HEAD_REVIEWED_ACCEPTED_AND_MERGED
PRODUCT_IMPLEMENTATION = BLOCKED
S1_006 = BLOCKED
```

`SOURCE_ACQUISITION_CHECK = PASS` means the exact component candidate has complete
source/advisory/license/maintenance/exit-strategy/dependency-register evidence. It does
**not** grant runtime or product authority. Final PR review/acceptance and merge remain
separate gates.

The final PR head is intentionally not embedded in this file because doing so would
recursively change that identity. Exact-head CI/review records bind the eventual head.

## Frozen component identities

```text
RUST_TOOLCHAIN = 1.97.1
RUST_RELEASE_COMMIT = 8bab26f4f68e0e26f0bb7960be334d5b520ea452

TAURI = 2.11.5
TAURI_SOURCE_COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6

TAURI_BUILD = 2.6.3
SERDE = 1.0.229
SERDE_JSON = 1.0.151

CARGO_TOML_SHA256 = 6688d45616ad298c0e89d0a792d0fe9e2b1e86165089956ce1c273c58b6d73a9
CARGO_LOCK_SHA256 = 3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9
LOCK_PACKAGE_COUNT = 417

GLIB_PUBLISHED_VERSION = 0.18.5
GLIB_PUBLISHED_CRATE_SHA256 = 233daaf6e83ae6a12a52055f568f9d7cf4671dabb78ff9560ab6da230ce00ee5
GLIB_SOURCE_VCS_SHA = 42b9caf98e03ded086362d9653ca58fe94dc8658
GLIB_VENDOR_TREE = c064fcd71830730d12645b54228326cefefd6188
GLIB_PATCHED_VARIANT_BLOB = e0997f651b103f7b198e528ee41137ad374e19b8
GLIB_PATCH_SHA256 = 586516d5219b681bbb9692380cf37370056ced644e2b3fb4c24cfefd43813a95
GLIB_VENDOR_FILE_COUNT = 121
GLIB_PUBLISHED_TO_VENDOR_CHANGED_FILES = src/variant_iter.rs
```

The vendored tree is byte-identical to the official `glib-0.18.5.crate` file set except
for the exact upstream soundness fix in `src/variant_iter.rs`:

```text
let p  -> let mut p
&p     -> &mut p
```

No other source, mode, or path change is admitted.

## Exact direct dependency surface

WePLD-owned manifests keep the external direct surface at the minimum justified by S1:

```text
apps/desktop/src-tauri:
  tauri = 2.11.5
  direct default-features = false
  direct features = [wry]
  build dependency:
    tauri-build = 2.6.3
    direct default-features = false

crates/contracts:
  serde = 1.0.229
  direct features = [derive]
  serde_json = 1.0.151

crates/core:
  external direct dependencies = NONE
```

Explicit non-admissions remain:

```text
tauri-plugin-shell = REJECT_INITIAL
direct Tokio/Core async framework = REJECT
UUID/random-ID crate = REJECT
RPC framework = REJECT
Protobuf/Cap'n Proto/MessagePack = REJECT
React/Vite/Tailwind = REJECT
database = REJECT
network client/server library = REJECT
telemetry SDK = REJECT
```

The complete resolved graph has 417 package entries. Resolved feature evidence for
pinned or exceptional packages includes:

```text
tauri 2.11.5:
  tauri-runtime-wry, webkit2gtk, webview2-com, wry

tauri-build 2.6.3:
  no resolved crate features

serde 1.0.229:
  alloc, default, derive, rc, serde_derive, std

serde_json 1.0.151:
  alloc, default, raw_value, std, unbounded_depth

glib 0.18.5 path override:
  default, gio, gio_ffi, v2_58, v2_60, v2_62, v2_64, v2_66, v2_68, v2_70
```

Transitive feature activation does not mint new direct API authority.

## Canonical component-stage proof

The component bytes were presented to the canonical base-controlled admission policy
without candidate checkout or execution by the privileged workflow.

```text
FOUNDATION_INTEGRITY_RUN = 31967584536
FOUNDATION_INTEGRITY = PASS

S1_ADMISSION_INTEGRITY_RUN = 31967584658
S1_ADMISSION_INTEGRITY_JOB = 95215005776
S1_ADMISSION_INTEGRITY = PASS

mode = REMOTE_CANDIDATE_DATA_ONLY
stage = S1_COMPONENT_ACQUISITION_CANDIDATE
source_registry_entries = 402
source_admission = 0
product_implementation_authorized = NO
```

The gate proves the exact frozen subtree, exact component lock bytes, path-source glib
shape, and reachability of source-less `glib 0.18.5` from `wepld-desktop`.

## RUSTSEC-2024-0429 disposition

```text
ADVISORY = RUSTSEC-2024-0429
AFFECTED_COMPONENT = glib 0.18.5
UPSTREAM_OFFICIAL_PATCHED_RANGE = >=0.20.0
GLIB_0_18_MAINTENANCE_STATE = EOL / NO_NEW_RELEASE_EXPECTED
DISPOSITION = PATCHED_BY_EXACT_VENDOR_BACKPORT
```

Primary upstream evidence establishes that:

- RustSec records the official fixed range as `>=0.20.0`;
- gtk-rs upstream fixed the soundness bug with the exact +2/-2 change frozen here;
- gtk-rs maintainers state the 0.18 line is EOL and no new 0.18 release is expected;
- the later request for a `glib 0.18.6` release was closed against that maintenance
  decision;
- current Tauri `2.11.5` still requires the GTK3 `0.18` family on Linux, so a normal
  Tauri upgrade does not remove the blocker.

A clean scanner result is **not** treated as proof of this fix because a local path
package changes registry-advisory matching semantics. The proof is the official archive
identity + exact patch + exact patched blob + exact frozen subtree.

## Current advisory evidence

Raw dependency/advisory/SBOM evidence was regenerated from the exact component bytes
using Rust/Cargo 1.97.1 without building, testing, or running WePLD product/vendor code.

```text
RUN = 31967901318
JOB = 95215749968
RESULT = PASS

CARGO_AUDIT = 0.22.2
CARGO_DENY = 0.19.7
CARGO_CYCLONEDX = 0.5.9

METADATA_PACKAGES = 417
RESOLVE_NODES = 417
AUDIT_VULNERABILITY_COUNT = 0
AUDIT_WARNING_UNMAINTAINED = 14
SBOM_FILE_COUNT = 3

RUSTSEC_ADVISORY_DB_HEAD = 69f93e1d081d8b6fbee010e48f0b5e0d13661415
RUSTSEC_ADVISORY_DB_COUNT = 1216
```

The RustSec database head embedded in the audit was independently compared with live
`RustSec/advisory-db` and was current at reconciliation time.

### Explicit unmaintained-warning reconciliation

The 14 warnings are retained as known **transitive maintenance debt**, not hidden and
not reclassified as vulnerabilities.

GTK3/Tauri Linux chain:

```text
RUSTSEC-2024-0413  atk 0.18.2
RUSTSEC-2024-0416  atk-sys 0.18.2
RUSTSEC-2024-0412  gdk 0.18.2
RUSTSEC-2024-0418  gdk-sys 0.18.2
RUSTSEC-2024-0411  gdkwayland-sys 0.18.2
RUSTSEC-2024-0415  gtk 0.18.2
RUSTSEC-2024-0420  gtk-sys 0.18.2
RUSTSEC-2024-0419  gtk3-macros 0.18.2
RUSTSEC-2024-0370  proc-macro-error 1.0.4
```

These are reached through Tauri's Linux GTK3/WebKit/Wry stack. They are admitted only
as unavoidable transitive maintenance debt for the current latest Tauri graph.

UNIC/Tauri-utils chain:

```text
RUSTSEC-2025-0100  unic-ucd-ident 0.9.0
RUSTSEC-2025-0081  unic-char-property 0.9.0
RUSTSEC-2025-0075  unic-char-range 0.9.0
RUSTSEC-2025-0098  unic-ucd-version 0.9.0
RUSTSEC-2025-0080  unic-common 0.9.0
```

These are reached through `tauri -> tauri-utils -> urlpattern`.

```text
KNOWN_CURRENT_REPORTABLE_VULNERABILITY = NONE_IN_CURRENT_RUSTSEC_AUDIT
UNMAINTAINED_WARNING_COUNT = 14
SILENT_IGNORE = NO
FUTURE_ADVISORY_REEVALUATION = REQUIRED
```

Any future transition of these packages from maintenance warning to reportable
vulnerability reopens component admission.

## Raw evidence retention and independent verification

Primary raw artifact:

```text
ARTIFACT_ID = 9269055750
ARTIFACT_NAME = s1-005-exact-component-admission-evidence
ARTIFACT_RETENTION = 90 days
ARTIFACT_SHA256 = 70698d62180a77a438ce7e690a690d6727c55830ca55c1bd360cc3a2b1f9b1ac
EVIDENCE_TXT_SHA256 = 36ba142751e96ebb4d3fa4ad0b1671bca7c7266b6475e1f0eb12cb54b67631e3
SHA256SUMS_TXT_SHA256 = 810d75547f9c1dc2bb28a806b030d8aa770a9cfe35cb1e622adb7d3f05a213df
```

Independent post-download validation:

```text
ZIP_ENTRIES = 28
UNSAFE_PATHS = 0
SYMLINKS = 0
SHA256SUMS_VERIFIED = 26/26
INDEPENDENT_RAW_EVIDENCE_VERIFICATION = PASS
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

Artifact retention is intentionally finite. The repository permanently retains the
immutable inputs, hashes, tool identities, run/job IDs, and regeneration contract;
finite artifact retention is not misrepresented as permanent raw-byte storage.

## Rust-crate license evidence

Target-scoped Rust-crate license evidence was generated separately from the exact same
component bytes.

A first verifier attempt (`31968422611`) failed fail-closed because it incorrectly
treated target-filtered Cargo metadata as the exact cargo-deny coverage denominator.
The verifier was corrected without changing candidate bytes.

Corrected proof:

```text
RUN = 31968572880
JOB = 95217373212
RESULT = PASS
CARGO_DENY = 0.19.7

x86_64-unknown-linux-gnu:
  METADATA_RESOLVE_NODES = 281
  CARGO_DENY_LISTED = 260
  EXTERNAL_EMPTY_LICENSES = 0

x86_64-pc-windows-msvc:
  METADATA_RESOLVE_NODES = 254
  CARGO_DENY_LISTED = 233
  EXTERNAL_EMPTY_LICENSES = 0

aarch64-apple-darwin:
  METADATA_RESOLVE_NODES = 246
  CARGO_DENY_LISTED = 226
  EXTERNAL_EMPTY_LICENSES = 0

x86_64-apple-darwin:
  METADATA_RESOLVE_NODES = 246
  CARGO_DENY_LISTED = 226
  EXTERNAL_EMPTY_LICENSES = 0
```

Detected Rust-crate license identifiers across these target graphs are within:

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

Target-license artifact:

```text
ARTIFACT_ID = 9269179220
ARTIFACT_NAME = s1-005-target-license-evidence
ARTIFACT_RETENTION = 90 days
ARTIFACT_SHA256 = 0ea6889f3cff9611477a5817ed0f2b169c9a8b62d7767eb02a34de47b5f657c0
LICENSE_COVERAGE_SHA256 = b255e4dc48a7e8c17f2f8cb32285430ec967d69809546ff972f500b1d190f7b6
SHA256SUMS_SHA256 = bf17684673b17731a7a2ebf01c336fdfb8fe229ccae9cd75777d607af239b99c
```

Independent post-download validation:

```text
ZIP_ENTRIES = 11
UNSAFE_PATHS = 0
SYMLINKS = 0
SHA256SUMS_VERIFIED = 10/10
TARGET_JSON_RECOMPUTATION = PASS
EXTERNAL_EMPTY_LICENSES = 0_FOR_ALL_FOUR_TARGETS
INDEPENDENT_TARGET_LICENSE_REVERIFICATION = PASS
```

Direct/exceptional component license metadata:

```text
tauri 2.11.5 = Apache-2.0 OR MIT
tauri-build 2.6.3 = Apache-2.0 OR MIT
serde 1.0.229 = MIT OR Apache-2.0
serde_json 1.0.151 = MIT OR Apache-2.0
vendored glib 0.18.5 = MIT
```

The exact upstream `glib` `LICENSE` and `COPYRIGHT` files are retained in the frozen
vendor subtree.

### Native Linux licensing boundary

Rust-crate SPDX evidence is not treated as the complete license analysis of native
system libraries. The upstream glib crate COPYRIGHT explicitly notes that binaries
linked with native GNOME libraries can carry LGPL/other obligations.

Therefore:

```text
RUST_CRATE_LICENSE_DETECTION = COMPLETE_FOR_S1_TARGET_GRAPHS
NATIVE_LINUX_SYSTEM_LIBRARY_PACKAGING_OBLIGATIONS = DEFERRED_TO_S1_010_PACKAGE_PROOF
NATIVE_OBLIGATIONS_SILENTLY_WAIVED = NO
```

S1-010 must verify and preserve all applicable native-library notices/source-offer or
other distribution obligations for the concrete packaged Linux artifact.

## Tauri capability and sidecar boundary

Tauri is admitted only as the desktop shell/WebView/bundling mechanism.

For S1:

```text
WEBVIEW_GENERAL_SHELL_PERMISSION = NONE
WEBVIEW_GENERAL_FILESYSTEM_PERMISSION = NONE
WEBVIEW_GENERAL_NETWORK_PERMISSION_FOR_HANDSHAKE = NONE
TAURI_PLUGIN_SHELL = NOT_ADMITTED
CORE_PROCESS = WEPLD_OWNED_SEPARATE_SIBLING_BINARY
CORE_PROTOCOL_AUTHORITY = WEPLD_OWNED
TAURI_ACL = NOT_NAWAT_AUTHORITY
```

The packaging design uses Tauri's minimum qualified external-binary/sibling mechanism
(`externalBin` or a smaller equivalent if later proven sufficient). Actual packaged
path, target suffix, launch, mismatch, and recovery behavior remains a test obligation
for S1-009/S1-010/S1-012; S1-005 does not fabricate runtime proof.

## Replacement and exit strategies

### Rust toolchain 1.97.1
Normal toolchain upgrades are permitted only after deterministic compile/test/security
gates. Protocol semantics are WePLD-owned and do not depend on a specific compiler
vendor feature.

### Tauri 2.11.5 / tauri-build 2.6.3
Tauri remains behind WePLD-owned Desktop/Core contracts. A future Tauri upgrade or
replacement must preserve the typed projection, Core process identity, capability
boundary, packaging behavior, and cross-platform evidence. `tauri-build` leaves with
the Tauri packaging path if no longer needed.

### Serde 1.0.229 / serde_json 1.0.151
Serialization is commodity machinery behind WePLD-owned protocol structs/enums,
framing, limits, versioning, and semantic validation. Replacement may change encoding
machinery only after protocol compatibility and negative tests are requalified.

### Vendored glib 0.18.5
This is a narrowly scoped security backport, not a permanent fork.

Exit trigger:

```text
QUALIFIED_TAURI_LINUX_GRAPH_NO_LONGER_REQUIRES_GTK3_GLIB_0_18
```

Then, in one separately reviewed dependency migration:

1. remove `[patch.crates-io] glib`;
2. delete `third_party/glib-0.18.5-wepld1/**`;
3. resolve a fresh lock;
4. regenerate dependency tree/features/SBOM/license/advisory evidence;
5. prove no equivalent advisory regression.

Prefer an upstream-maintained GTK4/newer-glib graph when Tauri provides a qualified
path.

### Transitive UNIC maintenance debt
Exit when an admitted upstream `tauri-utils`/`urlpattern` graph removes or replaces the
unmaintained UNIC 0.9 family. Re-evaluate on every dependency refresh.

## Temporary evidence capability neutralization

The evidence workflow lived only on `evidence/s1-005-component-admission`. After the
raw artifacts were captured and independently checked, the workflow was deleted.

```text
EVIDENCE_BRANCH_NEUTRALIZED_HEAD = 490bee9b41206eb4813d175cf303c35a005b8ee2
EVIDENCE_BRANCH_TREE = 6a62afd382360196567837ddd5768e82f0b9b4e4
CANONICAL_MAIN_TREE = 6a62afd382360196567837ddd5768e82f0b9b4e4
TEMPORARY_EVIDENCE_WORKFLOW_ACTIVE = NO
```

The branch's current tree is byte-identical to canonical main. Its history remains
audit evidence only.

## Final S1-005 condition reconciliation

```text
Rust toolchain pin fixed                                  PASS
Tauri/Tauri-build/Serde/serde_json versions fixed       PASS
resolved features captured                               PASS
tauri-plugin-shell absent                                PASS
Cargo.lock frozen                                        PASS
417-package graph captured                               PASS
3 CycloneDX SBOMs generated                              PASS
current RustSec audit reconciled                         PASS
RUSTSEC-2024-0429 exact backport proven                  PASS
14 unmaintained warnings explicitly dispositioned        PASS
unnecessary direct dependencies absent                   PASS
Tauri capability surface minimized                       PASS
sidecar packaging/launch design testable                 PASS
replacement/exit strategies recorded                     PASS
Rust-crate target-license evidence complete              PASS
native Linux packaging obligations preserved as later gate PASS
dependency register updated                              PASS
component-admission integrity policy migrated            PASS
post-merge policy activation proven                      PASS
exact frozen component accepted by canonical data-only gate PASS
```

Therefore the **Source Acquisition Check is complete for this candidate**.

What remains before runtime admission:

```text
FINAL_PR_HEAD_DETERMINISTIC_RERUN = REQUIRED
FINAL_PR_HEAD_INDEPENDENT_CORRECTNESS_REVIEW = REQUIRED
FINAL_PR_HEAD_FINDING_RECONCILIATION = REQUIRED
FOUNDER_ACCEPTANCE = REQUIRED
PR_11_MERGE = REQUIRED

RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
S1_006 = BLOCKED
```

Reviewer output, green CI, and this acquisition PASS are evidence; none independently
grants merge, runtime, or product authority.
