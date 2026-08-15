# S1-003 — Stage-aware foundation-integrity migration

## Identity

```text
SLICE = S1
TASK = S1-003
BASE_MAIN = 12fd72c19d639b4b72a8dec8dba644282383d0db
PR_3_PLANNING_BASELINE_MERGE = 12fd72c19d639b4b72a8dec8dba644282383d0db
BRANCH = ci/s1-stage-aware-foundation-integrity
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

This record refines the already-approved S1 plan for one security-relevant workflow migration. It does not reopen the S1 architecture, admit packages, create Cargo manifests, or authorize product behavior.

## Purpose

The P0 `foundation-integrity` workflow intentionally rejects every implementation-language file and dependency manifest. That preserved the fresh foundation, but S1-004 must later create a bounded dependency-resolution candidate before final component admission can be decided.

S1-003 therefore changes the integrity gate from a single documentation-only allowlist into a **stage-aware fail-closed policy** while preserving every immutable P0/source-registry invariant.

The migration must make the next acquisition step possible without creating a self-authorizing path from mutable planning/status text to product implementation.

## Non-bypassable design rule

```text
MUTABLE_MARKDOWN_FLAG != PHASE_AUTHORITY
PR_BRANCH_NAME != SOURCE_ADMISSION
FILE_PRESENCE != PRODUCT_IMPLEMENTATION_AUTHORITY
DEPENDENCY_RESOLUTION_CANDIDATE != RUNTIME_DEPENDENCY_ADMITTED
S1_003_MERGED != SOURCE_ACQUISITION_PASS
```

The workflow MUST derive the active repository stage from the actual tracked-tree shape and policy-owned structural rules. It MUST NOT unlock code by reading a mutable `PASS`, `AUTHORIZED`, stage name, checkbox, PR label, branch name, or other same-PR text value as authority.

## Stage model

### Stage A — `S1_PLANNING_ONLY`

This is the current tree shape.

Allowed:

- current canonical/governance/acquisition Markdown;
- current S1 Spec Kit Markdown;
- immutable canonical artifact archive;
- `AGENTS.md` / `README.md`;
- approved reviewer repository configs;
- the canonical integrity workflow;
- `src/.gitkeep` only under the root historical placeholder `src/`.

Rejected:

- Cargo/package/dependency manifests;
- implementation-language files;
- additional workflows/scripts/binaries;
- symlinks/gitlinks;
- temporary repair payloads;
- any product/runtime behavior.

### Stage B — `S1_DEPENDENCY_RESOLUTION_CANDIDATE`

This future stage exists only so S1-004 can resolve and inspect the minimum intended Cargo graph.

It MAY add only an explicitly enumerated candidate set such as:

```text
Cargo.toml
Cargo.lock
rust-toolchain.toml
apps/desktop/src-tauri/Cargo.toml
apps/desktop/src-tauri/src/main.rs
crates/contracts/Cargo.toml
crates/contracts/src/lib.rs
crates/core/Cargo.toml
crates/core/src/main.rs
```

The S1-003 implementation MUST finalize the exact permitted set before merge. Any target stub required only so Cargo recognizes a package MUST have an exact bounded skeleton contract; arbitrary Rust content is prohibited in Stage B.

Stage B is **not product implementation**. It permits dependency-resolution mechanics only.

### Stage C — product implementation

```text
S1_PRODUCT_IMPLEMENTATION = BLOCKED_BY_S1_003
```

S1-003 MUST NOT create a generic rule that admits arbitrary Rust, Tauri UI, JavaScript, build scripts, capabilities, plugins, or other product paths after a Markdown flag changes.

A later reviewed gate may expand the integrity policy only after S1-005 has produced exact admitted dependency evidence and `SOURCE_ACQUISITION_CHECK = PASS`.

## Candidate manifest policy

The Stage B policy must constrain direct dependencies semantically, not only by filename.

Initial allowed candidate component families are limited to the S1 acquisition record:

```text
tauri = 2.11.5 candidate only
tauri-build = 2.6.3 candidate only
serde = 1.0.229 candidate only
serde_json = 1.0.151 candidate only
local WePLD workspace path dependencies = candidate mechanics only
```

The workflow policy MUST reject, as direct dependencies unless a separately reviewed acquisition decision changes the contract:

```text
tauri-plugin-shell
Tokio direct dependency in Core
UUID/random-ID crate
RPC framework
protobuf / Cap'n Proto / MessagePack framework
frontend framework/package manager stack
DB client/runtime
network client/server library
telemetry SDK
unapproved git dependency
unapproved alternate registry
wildcard/unbounded direct version requirement
```

The exact initial Tauri feature/default-feature candidate must be explicitly enumerated in the workflow policy and reviewed before S1-003 closes. Feature names are admission-sensitive surface and cannot be left as arbitrary same-PR input.

## Candidate source skeleton rule

If Cargo requires target files for metadata/lock resolution, S1-003 may permit only exact minimal skeleton files at the enumerated paths.

Requirements:

- bounded byte size;
- no filesystem/process/network/project effects;
- no Tauri application startup;
- no IPC/protocol behavior;
- no unsafe code;
- exact or equivalently strict deterministic content validation;
- any deviation remains rejected until a later reviewed policy phase.

This avoids treating “a `.rs` file exists” as product implementation authority.

## Cargo.lock constraints

When Stage B appears, the gate should treat the lockfile as candidate supply-chain evidence rather than authority.

At minimum:

- bounded file size;
- parseable lockfile structure;
- no `git+` package source unless separately qualified;
- no unapproved alternate registry source;
- checksums expected for registry packages where Cargo supplies them;
- exact direct candidate versions remain consistent with the manifests;
- lockfile presence never equals runtime admission.

Full resolved transitive/advisory/SBOM reconciliation remains S1-004/S1-005 work.

## Immutable P0 protections that survive unchanged

S1-003 MUST preserve evidence equivalent to or stronger than the current gate for:

- immutable foundation baseline commit identity;
- canonical artifact archive SHA-256;
- V2.2 master-plan SHA-256;
- exact canonical archive member set and bounded extraction;
- frozen 402-source restoration registry count/uniqueness;
- `admission_status = NOT_ADMITTED` across the frozen registry;
- CSV/JSON registry consistency protections already present;
- bounded/no-follow canonical archive read;
- symlink rejection;
- gitlink/submodule rejection;
- repair-payload / temporary-repair-workflow rejection;
- duplicate canonical-security-policy rejection;
- reviewer repository config fail-closed profile;
- frozen `FRESH_IMPLEMENTATION_DEPENDENCIES = 0` P0 evidence as historical foundation truth, without misusing it to claim S1 dependency admission.

## Reviewer egress controls

S1-003 MUST preserve the current repository-level controls:

```text
CodeRabbit automatic review = disabled
CodeRabbit automatic incremental review = disabled
Cubic reviews = disabled
Cubic PR descriptions = disabled
Cubic auto-approve = disabled
Cubic Ultrareview = disabled
Cubic automatic Ultrareview = disabled
Cubic thread auto-resolution = disabled
Cubic fix/write surfaces = disabled
```

Repository-file validation remains distinct from provider-effective state:

```text
LOCAL_REVIEWER_CONFIG_VALIDATION != PROVIDER_EFFECTIVE_STATE
CUBIC_PROVIDER_EFFECTIVE_STATE = NOT_PROVEN
```

Current Cubic documentation states that partial YAML fields can inherit lower-priority configuration and that invalid repository YAML falls back to UI settings. Therefore S1-003 must preserve exact explicit security-relevant fields and add a deterministic schema/semantic validation strategy or equivalent reviewed contract. It still MUST NOT report Cubic provider-effective state as proven without provider-side evidence.

## Negative probes

The migrated gate must include deterministic policy probes that prove rejection of representative bypass attempts. At minimum probe:

- arbitrary root `package.json`;
- arbitrary `src/main.rs` under the historical root `src/`;
- extra Rust module outside the exact Stage B skeleton paths;
- `crates/worker/Cargo.toml` or another later-slice crate;
- a second workflow file that is not explicitly admitted;
- a symlink or gitlink path;
- direct `tauri-plugin-shell`;
- direct Core `tokio`;
- direct network/database/telemetry package;
- wildcard/unpinned direct candidate dependency;
- git dependency / alternate registry candidate;
- product-like Rust content in a Stage B skeleton;
- a mutable Markdown `SOURCE_ACQUISITION_CHECK = PASS` that attempts to unlock code.

The negative tests must exercise the same policy functions/rules used against the actual checked-out tree, not a disconnected illustrative implementation.

## Main post-merge integrity dependency

The PR #3 merge created canonical `main` commit:

```text
12fd72c19d639b4b72a8dec8dba644282383d0db
```

Push run `foundation-integrity` #146 / `31908187069` was queued when this S1-003 planning record was created. It is not reported as PASS while queued.

Substantive S1-003 workflow mutation is blocked until that canonical-main post-merge run completes successfully or an explicit failure is investigated and reconciled.

## S1-003 review requirements

This migration changes CI/workflow trust and future source/dependency admission mechanics, so:

```text
SECURITY_REVIEW_APPLICABILITY = APPLICABLE
CODEX_SECURITY_IF_AVAILABLE_AND_EGRESS_PERMITTED = REQUIRED_BY_POLICY
INDEPENDENT_CORRECTNESS_REVIEW = REQUIRED
EXACT_HEAD_BINDING = REQUIRED
```

If Codex Security remains unavailable in the current host, record `NOT_RUN_NON_BLOCKING`; never call it PASS.

Any hosted correctness review requires a fresh exact-head pre-egress record and must not reactivate automatic review.

## Acceptance for S1-003 only

S1-003 may close only when one exact head proves:

- post-P0 archive/registry invariants preserved;
- Stage A remains as strict as the reviewed planning baseline;
- Stage B admits only the exact dependency-resolution candidate shape;
- Stage C/product behavior remains blocked;
- candidate manifest/dependency semantics are fail-closed;
- exact skeleton content cannot carry product behavior;
- negative bypass probes pass;
- reviewer automatic-egress controls remain fail-closed;
- deterministic workflow gate passes;
- applicable security coverage is honestly accounted;
- independent correctness review is complete;
- all valid findings are reconciled;
- zero unresolved material findings remain.

S1-003 completion authorizes **only** the S1-004 bounded dependency-resolution bootstrap described by the S1 plan.

```text
S1_ACCEPTED = NO
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
NEXT_AFTER_S1_003 = S1-004 dependency-resolution candidate
```
