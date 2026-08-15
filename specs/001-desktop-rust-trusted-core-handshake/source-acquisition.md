# Source Acquisition Check — S1 Desktop ↔ Rust Trusted Core Handshake

## Status

```text
CHECK = ACTIVE / PRE-IMPLEMENTATION
BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
PONYTAIL = COMPLETE_FOR_PLANNING
SOURCE_IMPORT = NONE
RUNTIME_DEPENDENCY_ADMISSION = NONE
DEPENDENCY_RESOLUTION = NOT_YET_EXECUTED
SBOM = NOT_YET_GENERATED
IMPLEMENTATION = BLOCKED_PENDING_FINAL_COMPONENT_ADMISSION
```

Founder standing authorization supplies decision/write authority once each component is qualified. It is not blanket source/dependency admission.

The frozen 402-source restoration registry remains immutable evidence. S1 uses component-specific acquisition and does not silently rewrite the registry.

## Prior acquisition evidence reused

The preserved P0-A path-level acquisition ledger already identified Tauri as `P0A-02`, with disposition `PACKAGE_CANDIDATE + REFERENCE` and explicit negative oracle: Tauri IPC/ACL is not Nawat authority. Its record required a fresh release/package pin and exact transitive audit before S1 admission.

That requirement is being executed here; the older research pin is historical evidence only.

## Component ACQ-S1-01 — Rust toolchain

```text
ROLE = BUILD + RUNTIME LANGUAGE TOOLCHAIN
SOURCE = rust-lang/rust
VERSION = 1.97.1
TAG_OBJECT = bd3cd8fdf9945e13d317642df03363bfa1b4c30e
RELEASE_COMMIT = 8bab26f4f68e0e26f0bb7960be334d5b520ea452
OFFICIAL_RELEASE_DATE = 2026-07-16
DISPOSITION = PIN_TOOLCHAIN_CANDIDATE
ADMISSION = PENDING_LOCK_AND_CI_PROOF
```

Reason: current stable point release at acquisition time; it fixes a reported LLVM miscompilation from 1.97.0. Tauri 2.11.5 declares an MSRV of Rust 1.77.2, so 1.97.1 is above the framework requirement.

Required before final admission:

- `rust-toolchain.toml` exact channel/component/target declaration;
- Windows `x86_64-pc-windows-msvc` compile/test proof;
- Linux/macOS CI availability accounting;
- exact `rustc -Vv` evidence in acceptance packet.

Exit strategy: the protocol/contracts remain stable across normal Rust toolchain upgrades; toolchain bump requires gates, not architecture change.

## Component ACQ-S1-02 — Tauri runtime

```text
ROLE = DESKTOP SHELL / WEBVIEW HOST / BUNDLING
SOURCE = tauri-apps/tauri
VERSION = 2.11.5
TAG = tauri-v2.11.5
COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6
CRATE_MANIFEST_BLOB = 17cf19d2be677d42b46c8e4c365bcabb23050b36
WORKSPACE_MANIFEST_BLOB = 670a647672c2e11476d0ceb03e7d52fdb55e96cf
DISPOSITION = PACKAGE_CANDIDATE
ADMISSION = PENDING_RESOLVED_LOCK_SBOM_AUDIT
```

Observed relevant properties at the pinned release:

- `tauri` crate version is 2.11.5;
- workspace MSRV is Rust 1.77.2;
- desktop support includes Windows/macOS/Linux;
- Tauri already depends on Serde/serde_json/Tokio internally, but WePLD does not infer direct-dependency authority from transitive presence;
- Tauri bundler `externalBin` appends target-triple/platform suffixes to source sidecar names;
- Tauri is not selected as the Core protocol authority and its ACL/capability model is a negative boundary oracle for WePLD authority.

Security/supply-chain notes:

- the upstream 2.11.5 release audit records several warnings in its large workspace; an upstream workspace audit is not equivalent to the future WePLD resolved lockfile audit;
- therefore S1 must run its own `cargo audit`/OSV-equivalent check after lock resolution and must record every allowed advisory/warning explicitly rather than inheriting upstream conclusions.

Required before final admission:

- exact crate features/default-feature decision;
- resolved `Cargo.lock`;
- dependency tree and SBOM;
- advisory scan;
- minimal Tauri capability manifest;
- no general shell/filesystem/network WebView permission for S1;
- Windows package/sidecar sibling-path test;
- replacement/exit path preserving WePLD contracts.

## Component ACQ-S1-03 — Tauri build helper

```text
ROLE = BUILD-TIME TAURI CONFIG/CODEGEN
SOURCE = tauri-apps/tauri
VERSION = tauri-build 2.6.3
SOURCE_COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6
MANIFEST_BLOB = 6535de37c6e66aef396ac592957e9f33c87c8a9b
DISPOSITION = BUILD_PACKAGE_CANDIDATE
ADMISSION = PENDING_RESOLVED_LOCK_SBOM_AUDIT
```

No runtime authority is granted by the build helper.

## Component ACQ-S1-04 — Serde

```text
ROLE = TYPED SERIALIZATION
SOURCE = serde-rs/serde
VERSION = 1.0.229
TAG = v1.0.229
TAG_OBJECT = 95ff3321ad95a8c1f4b488b54027302e7c3911f4
RELEASE_COMMIT = 7fc3b4c30c94f73a96ebd1553f2b090d928fc3a8
TAG_VERIFICATION = VERIFIED
DISPOSITION = PACKAGE_CANDIDATE
ADMISSION = PENDING_RESOLVED_LOCK_SBOM_AUDIT
```

Reason: typed `Serialize`/`Deserialize` machinery is solved commodity behavior. Hand-written equivalent is rejected by Ponytail.

S1 only needs the minimum derive support required by protocol types.

## Component ACQ-S1-05 — serde_json

```text
ROLE = S1 JSON ENCODING/DECODING
SOURCE = serde-rs/json
VERSION = 1.0.151
TAG = v1.0.151
TAG_OBJECT = 23d32e33e1bf94b3a1dd8248d1090d5c994417ec
RELEASE_COMMIT = de8500740cdcabffb9734f503e4889def823cf10
TAG_VERIFICATION = VERIFIED
DISPOSITION = PACKAGE_CANDIDATE
ADMISSION = PENDING_RESOLVED_LOCK_SBOM_AUDIT
```

Reason: S1 benefits from a compact inspectable payload format. The frame prefix, size bounds, protocol validation, and semantic authority remain WePLD-owned. `serde_json::Value` is not the canonical protocol model; typed structs/enums are.

## Component ACQ-S1-06 — Tauri shell plugin

```text
ROLE = SIDECAR/PROCESS REFERENCE OR FALLBACK ONLY
SOURCE = tauri-apps/plugins-workspace
REVISION = db9c5998feff9384f9cbbefcbe0d45937c00a1fc
OBSERVED_CRATE_VERSION = 2.3.5
PROCESS_MODULE_BLOB = 7a1c2db241cf4484df6b4d68dc6c1885ada64e71
DISPOSITION = REFERENCE + NEGATIVE_ORACLE
RUNTIME_ADMISSION = REJECT_INITIAL
```

Useful observed mechanics:

- byte-oriented stdout events are available;
- child stdin uses `write_all`;
- process stdio is piped;
- Windows child launch uses no-console process creation;
- packaged command-path resolution is small enough that S1 can test a stdlib launch path rather than installing the broader plugin.

Reopen condition:

Only if direct `std::process::Command` launch of the Tauri-bundled Core fails an explicit Windows packaging/recovery requirement. Reopening requires a new acquisition record and cannot occur as silent fallback.

## Component ACQ-S1-07 — Spec Kit methodology reference

```text
SOURCE = github/spec-kit
REVISION = bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c
ROLE = DEVELOPMENT-METHOD REFERENCE
RUNTIME_DEPENDENCY = NO
ADMISSION = REFERENCE_ONLY
```

The current quickstart order differs from the WePLD canonical planning order. S1 records and reconciles that drift in `plan.md`; the tool does not override repository authority.

## Component ACQ-S1-08 — Ponytail methodology reference

```text
SOURCE = DietrichGebert/ponytail
REVISION = 2ed6c52c9d7e5e56942508591085fd45dea277d3
SKILL_BLOB = 02c0712c86277d49d18a77da3a2b825657bf02d1
ROLE = SUFFICIENCY/MINIMALISM METHOD
RUNTIME_DEPENDENCY = NO
ADMISSION = REFERENCE_ONLY
```

## Rejected unnecessary dependencies for base S1

```text
tauri-plugin-shell = REJECT_INITIAL
Tokio direct dependency in Core = REJECT
UUID/random-ID crate = REJECT
RPC framework = REJECT
Protobuf/Cap'n Proto/MessagePack = REJECT
React/Vite/Tailwind = REJECT
Database = REJECT
Network client/server library = REJECT
Telemetry SDK = REJECT
```

A transitive dependency brought by Tauri is not automatically a direct WePLD API dependency.

## Dependency-resolution bootstrap boundary

The master plan requires exact transitive/SBOM/security evidence before final component admission, but that evidence depends on a resolved candidate lockfile.

Therefore S1 uses two distinct states:

```text
DEPENDENCY_RESOLUTION_AUTHORIZED
!=
RUNTIME_DEPENDENCY_ADMITTED
```

After this planning package is reconciled, a bounded acquisition step may create only the candidate Rust manifests/toolchain file needed to resolve the intended minimum dependency graph and generate:

- `Cargo.lock`;
- `cargo tree` evidence;
- SBOM;
- advisory scan;
- feature inventory.

That bounded resolution step does not authorize implementation behavior. If the resolved graph is incompatible with S1 policy, the candidate is rejected and the manifests are repaired/removed before implementation.

## Final Source Acquisition Check conditions

`SOURCE_ACQUISITION_CHECK = PASS` only when all are true on one exact head:

- Rust toolchain pin fixed;
- Tauri/Tauri-build/Serde/serde_json exact resolved versions and features fixed;
- `tauri-plugin-shell` absent unless separately requalified;
- lockfile generated;
- SBOM generated;
- advisory results reconciled;
- no unnecessary direct dependencies;
- Tauri capability surface minimized;
- Windows sidecar packaging/launch design testable;
- every admitted component has replacement/exit strategy;
- dependency register and S1 admission record are updated without rewriting the frozen 402 restoration registry;
- `foundation-integrity` is migrated safely to permit only qualified S1 paths while retaining P0 invariants.

Until then:

```text
SOURCE_ACQUISITION_CHECK = OPEN
IMPLEMENTATION = BLOCKED
```
