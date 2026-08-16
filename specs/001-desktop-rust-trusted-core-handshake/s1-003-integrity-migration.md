# S1-003 — Stage-aware foundation-integrity migration

## Identity

```text
SLICE = S1
TASK = S1-003
BASE_MAIN = 12fd72c19d639b4b72a8dec8dba644282383d0db
PR_3_PLANNING_BASELINE_MERGE = 12fd72c19d639b4b72a8dec8dba644282383d0db
ACTIVE_PR = #4
BRANCH = ci/s1-stage-aware-foundation-integrity
MAIN_POST_MERGE_INTEGRITY = PASS
MAIN_POST_MERGE_INTEGRITY_RUN = 31908187069 / #146
PR_4_INITIAL_PLANNING_INTEGRITY = PASS
PR_4_INITIAL_PLANNING_INTEGRITY_RUN = 31908422218 / #147
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

This record refines the already-reviewed S1 plan for one security-relevant workflow migration. It does not reopen the S1 architecture, admit packages, create a dependency lock, or authorize product behavior.

## Why the P0 gate must change

The P0 `foundation-integrity` workflow intentionally rejected every implementation-language file and dependency manifest. That was correct for the fresh foundation, but S1-004 must later create a **bounded candidate** Cargo graph so its exact transitive dependencies, features, lockfile, SBOM, and advisories can be inspected before admission.

S1-003 therefore changes the gate from one documentation-only tree shape into a stage-aware, fail-closed policy while preserving immutable P0/source-registry evidence.

```text
DEPENDENCY_RESOLUTION_CANDIDATE != RUNTIME_DEPENDENCY_ADMISSION
S1_003_MERGED != SOURCE_ACQUISITION_PASS
SOURCE_ACQUISITION_PASS != S1_ACCEPTANCE
```

## Authority rule

No mutable same-PR text may unlock implementation.

```text
MUTABLE_MARKDOWN_FLAG != PHASE_AUTHORITY
PR_BRANCH_NAME != SOURCE_ADMISSION
PR_LABEL != SOURCE_ADMISSION
CHECKBOX != SOURCE_ADMISSION
FILE_PRESENCE != PRODUCT_IMPLEMENTATION_AUTHORITY
```

The policy derives the candidate stage from the actual tracked Git object graph and exact policy-owned file/content contracts.

## Two-layer integrity model

S1-003 introduces two complementary checks.

### Layer 1 — `foundation-integrity`

`foundation-integrity` remains the familiar self-check and canonical-main check.

- `pull_request`: inspect the exact PR head checkout with `permissions: {}`; `actions/checkout` still receives its required token input by default, credentials are not persisted, and no `GITHUB_TOKEN` is passed to the policy script;
- `push` to `main`: inspect canonical main with the same embedded immutable baseline constants;
- execute policy self-tests on every run;
- use `actions/checkout` pinned to `v7.0.1` commit `3d3c42e5aac5ba805825da76410c181273ba90b1`.

This layer is useful evidence, but a PR-controlled workflow/policy cannot be the sole authority that judges its own mutation.

### Layer 2 — `s1-admission-integrity`

After S1-003 is merged into canonical `main`, `s1-admission-integrity` runs on `pull_request_target` using the **base branch's trusted workflow and policy**.

Security design:

```text
CANDIDATE_CHECKOUT = NONE
CANDIDATE_CODE_EXECUTION = NONE
CANDIDATE_BUILD = NONE
CANDIDATE_SCRIPT_EXECUTION = NONE
TOKEN_PERMISSION = contents:read
POLICY_SOURCE = exact PR base SHA
CANDIDATE_INPUT = Git tree/blob data fetched through GitHub API
```

The trusted policy fetches the candidate commit/tree/blob objects through GitHub's Git data API, validates object identities/modes/paths/sizes, and parses only the narrowly required text/TOML/archive data. It never checks out or executes candidate code.

This deliberately follows GitHub's `pull_request_target` security guidance: privileged workflows must not check out and then execute untrusted PR code.

### Base-controlled paths

For ordinary future candidate PRs, the authoritative layer byte-compares these candidate paths to their base copies:

```text
.coderabbit.yaml
cubic.yaml
.github/scripts/wepld_integrity.py
.github/workflows/foundation-integrity.yml
.github/workflows/s1-admission-integrity.yml
AGENTS.md
docs/canonical/ARCHITECTURE_INVARIANTS.md
docs/canonical/BUILD_METHOD.md
docs/canonical/SECURITY_REVIEW_POLICY.md
docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md
docs/canonical/FOUNDER_RATIFICATION.md
docs/canonical/MASTER_PLAN_INDEX.md
docs/governance/FOUNDATION_INTEGRITY_BASELINE.md
```

An ordinary dependency/product PR therefore cannot rewrite the gate or the core governance contracts used to judge it. A legitimate later policy migration requires a separately governed bootstrap/override path; it is not silently self-authorizing.

## Stage model

### Stage A — `S1_PLANNING_ONLY`

Allowed tree classes:

- `AGENTS.md`, `README.md`;
- canonical/governance/acquisition/learning/historical Markdown under `docs/`;
- Spec Kit/planning Markdown under `specs/`;
- immutable canonical artifact archive;
- reviewer repository config files;
- the two integrity workflows and policy script;
- empty `src/.gitkeep` historical placeholder.

Rejected:

- dependency manifests/lockfiles;
- implementation-language files outside the policy script itself;
- arbitrary root/package-manager files;
- extra workflows/scripts;
- symlinks/gitlinks;
- temporary repair payloads/workflows;
- product/runtime behavior.

### Stage B1 — `S1_DEPENDENCY_RESOLUTION_INPUT`

Stage B1 exists only to let S1-004 run Cargo dependency resolution.

It requires **all** of this exact candidate input shape:

```text
Cargo.toml
rust-toolchain.toml
apps/desktop/src-tauri/Cargo.toml
apps/desktop/src-tauri/src/main.rs
crates/contracts/Cargo.toml
crates/contracts/src/lib.rs
crates/core/Cargo.toml
crates/core/src/main.rs
```

Partial Stage B is rejected.

### Stage B2 — `S1_DEPENDENCY_RESOLUTION_LOCKED`

Stage B2 is Stage B1 plus:

```text
Cargo.lock
```

The lock is candidate supply-chain evidence, not admission.

### Stage C — product implementation

```text
S1_PRODUCT_IMPLEMENTATION = BLOCKED
```

S1-003 does not create a Markdown/status switch that unlocks arbitrary Rust, Tauri UI, JS, capabilities, plugins, build scripts, or later-slice paths.

## Exact Stage-B candidate content

The stage-aware policy uses exact content rather than a permissive TOML allowlist.

### Root workspace

```toml
[workspace]
resolver = "2"
members = [
  "apps/desktop/src-tauri",
  "crates/contracts",
  "crates/core",
]
```

### Desktop candidate

```toml
[package]
name = "wepld-desktop"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
tauri = { version = "=2.11.5", default-features = false, features = ["wry"] }
wepld-contracts = { path = "../../../crates/contracts" }

[build-dependencies]
tauri-build = { version = "=2.6.3", default-features = false }
```

`default-features = false` plus explicit `wry` is an acquisition **candidate**, not final admission. The pinned Tauri 2.11.5 source shows its default feature set adds additional platform/capability surface; S1-004/S1-005 may change this only through measured evidence and reviewed acquisition reconciliation.

### Contracts candidate

```toml
[package]
name = "wepld-contracts"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
serde = { version = "=1.0.229", features = ["derive"] }
serde_json = "=1.0.151"
```

### Core candidate

```toml
[package]
name = "wepld-core"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
wepld-contracts = { path = "../contracts" }
```

### Toolchain candidate

```toml
[toolchain]
channel = "1.97.1"
profile = "minimal"
components = ["clippy", "rustfmt"]
targets = ["x86_64-pc-windows-msvc"]
```

### Exact target skeletons

Desktop/Core binary target:

```rust
#![forbid(unsafe_code)]

fn main() {}
```

Contracts library:

```rust
#![forbid(unsafe_code)]
```

These files exist only so Cargo recognizes the candidate packages. Any product-like behavior or extra Rust module remains rejected.

## Direct dependency exclusions

Exact templates prevent direct introduction of:

```text
tauri-plugin-shell
Tokio in Core
UUID/random-ID crate
RPC framework
protobuf / Cap'n Proto / MessagePack framework
frontend framework/package manager
database client/runtime
network client/server package
telemetry SDK
unapproved git dependency
unapproved alternate registry
wildcard/unbounded direct version
```

A transitive package appearing through an admitted candidate is not equivalent to a direct WePLD API dependency; S1-004/S1-005 must still inspect and reconcile it.

## Cargo.lock policy

Stage B2 requires:

- UTF-8 TOML;
- maximum 2 MiB;
- lock format version 4;
- bounded package count;
- package sources either workspace/path (`source` absent) or crates.io's canonical registry source;
- no git sources;
- no alternate registry;
- registry checksums present and 64-hex;
- exact candidate packages/versions present;
- `tauri-plugin-shell` absent.

The lockfile still does not establish runtime admission.

## Immutable P0 protections retained

The policy preserves or strengthens:

- immutable foundation baseline identity;
- canonical artifact archive SHA-256;
- V2.2 SHA-256;
- exact archive member set;
- bounded no-follow local archive read;
- bounded remote blob read;
- frozen 402-row source registry;
- JSON/CSV source-name consistency;
- every frozen registry row remains `NOT_ADMITTED`;
- symlink rejection;
- gitlink/submodule rejection;
- case-insensitive tracked-path collision rejection;
- temporary repair payload/workflow rejection;
- duplicate canonical security-policy rejection;
- historical `FRESH_IMPLEMENTATION_DEPENDENCIES = 0` evidence.

## Reviewer egress controls and Cubic limitation

Repository policy continues to require explicit manual-only CodeRabbit/Cubic configuration bytes.

However two observed Cubic incidents now prove repository intent is not provider-effective proof:

- PR #3 incident: comment `5303961793`;
- PR #4 incident: comment `5304248582`.

```text
LOCAL_REVIEWER_CONFIG_VALIDATION != PROVIDER_EFFECTIVE_STATE
CUBIC_PROVIDER_EFFECTIVE_STATE = CONFLICTING_WITH_REPOSITORY_INTENT / NOT_PROVEN_SAFE
CUBIC_REVIEW_ELIGIBILITY = BLOCKED
CUBIC_OUTPUT_COUNTS_AS_REVIEW_PASS = NO
```

No intentional Cubic review may be triggered until provider-side effective settings are independently verified. Repository config remains defense in depth, not proof of external provider behavior.

## Deterministic negative probes

The policy self-test exercises the same classification/content functions used by real verification and requires rejection of representative bypasses:

- partial Stage B candidate;
- arbitrary `package.json`;
- root `src/main.rs`;
- extra Rust module;
- later-slice crate;
- extra workflow;
- symlink;
- gitlink;
- case-fold path collision;
- Markdown `SOURCE_ACQUISITION_CHECK = PASS` trying to change stage;
- direct `tauri-plugin-shell`;
- direct Core `tokio`;
- direct network dependency;
- wildcard dependency;
- git dependency;
- product behavior in a skeleton;
- git/alternate-registry lock source;
- base-controlled policy mutation.

These dependency-labeled probes currently prove **exact Stage-B template drift rejection**. They do not claim independent semantic manifest rules beyond the exact templates unless such semantic validators are added later.

## Bootstrap limitation

The new `pull_request_target` workflow does not exist in PR #4's **base** (`12fd72c...`), so it cannot authoritatively run against the PR that introduces it.

Therefore:

```text
PR_4_HEAD_SELFCHECK = REQUIRED
PR_4_INDEPENDENT_SECURITY/CORRECTNESS_REVIEW = REQUIRED
POST_MERGE_MAIN_INTEGRITY = REQUIRED
FIRST_POST_MERGE_BASE_CONTROLLED_CANARY = REQUIRED_BEFORE_S1_004_MANIFESTS
S1_003_ACTIVATION_PROVEN_BEFORE_CANARY = NO
```

After PR #4 is reviewed/merged, create a docs-only canary PR from the new main and require `s1-admission-integrity` to inspect it successfully. Only after that base-controlled activation proof may S1-004 add candidate manifests.

## Platform enforcement limitation

This session has no GitHub connector action capable of configuring branch protection/rulesets, and the branch-protection endpoint is not readable by the integration.

```text
PLATFORM_REQUIRED_CHECK_ENFORCEMENT = NOT_PROVEN
PLATFORM_RULESET_MUTATION_BY_THIS_PR = NONE
```

Canonical WePLD governance will treat `s1-admission-integrity` as mandatory evidence, but that process rule must not be misreported as GitHub platform enforcement.

## Security/review requirements

S1-003 changes workflow trust and future dependency-resolution admission mechanics.

```text
SECURITY_REVIEW_APPLICABILITY = APPLICABLE
CODEX_SECURITY_IF_AVAILABLE_AND_EGRESS_PERMITTED = REQUIRED_BY_POLICY
INDEPENDENT_CORRECTNESS_REVIEW = REQUIRED
EXACT_HEAD_BINDING = REQUIRED
```

If Codex Security is unavailable in this host, record `NOT_RUN_NON_BLOCKING`; never call it PASS.

Any hosted correctness review requires a fresh exact-head pre-egress record. Cubic is currently ineligible because provider-effective automatic processing contradicts repository intent.

### Exact-head evidence protocol

The final PR candidate cannot safely self-record its own commit SHA inside this tracked file because changing the file would change that SHA again. Exact-head binding therefore lives in GitHub/PR evidence after the final content commit.

Before merge or activation, require and record:

```text
LIVE_PR_HEAD_SHA = <current GitHub PR head>
FOUNDATION_INTEGRITY_RUN_ID = <exact run id>
FOUNDATION_INTEGRITY_RUN_HEAD_SHA = <run head_sha>
FOUNDATION_INTEGRITY_CONCLUSION = success
REQUIRED_EQUALITY = LIVE_PR_HEAD_SHA == FOUNDATION_INTEGRITY_RUN_HEAD_SHA
INDEPENDENT_REVIEW_RANGE_END = LIVE_PR_HEAD_SHA
```

If any content commit changes `LIVE_PR_HEAD_SHA`, prior CI, security accounting, egress preflight, and independent review are historical and must be rebound to the new head. A run number without matching `run.head_sha` is insufficient evidence.

## S1-003 closure

PR #4 may merge only after its exact head passes the local/head policy self-check, preserves the reviewed planning invariants, completes independent review, reconciles findings, and records security coverage honestly.

But **S1-003 activation is not fully proven by PR #4 alone**. The post-merge docs-only canary must prove the base-controlled `s1-admission-integrity` path before S1-004 manifests are introduced.

```text
S1_ACCEPTED = NO
SOURCE_ACQUISITION_CHECK = OPEN
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
NEXT_AFTER_PR_4 = POST_MERGE S1-003 ACTIVATION CANARY
NEXT_AFTER_CANARY_PASS = S1-004 DEPENDENCY-RESOLUTION CANDIDATE
```
