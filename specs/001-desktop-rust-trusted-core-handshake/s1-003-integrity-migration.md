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
- validate the separately governed immutable remote baseline on **every** run;
- execute policy self-tests on every run;
- use `actions/checkout` pinned to `v7.0.1` commit `3d3c42e5aac5ba805825da76410c181273ba90b1`.

#### Immutable remote baseline validation

A checked-out policy that owns its own expected digests can be satisfied by a candidate that changes the canonical artifact and the embedded constants together. That is the data-plane defect `docs/governance/FOUNDATION_INTEGRITY_BASELINE.md` exists to close, so every run validates the immutable baseline object at the pinned baseline commit.

```text
BASELINE_VALIDATION_ON_PR_HEAD = REQUIRED
BASELINE_VALIDATION_ON_PUSH_TO_MAIN = REQUIRED
BASELINE_FAILURE = FAIL_CLOSED
```

The immutable baseline identity is bound end-to-end through the separately governed contract:

```text
BASELINE_COMMIT = 421c769b47fd8ad4f5bcba67ff8b00ba0adfc6c3
BASELINE_PATH = .wepld/foundation-integrity-baseline-v1.json
BASELINE_BLOB = a7c1423c95683f94479fb4a166ec73b3c35149ed
```

The Contents API response must report that exact blob identity before its content is decoded. The complete baseline chain is therefore the immutable commit plus exact path plus exact returned blob identity plus the expected baseline semantic fields plus base ancestry. No single element substitutes for another.

```text
REQUESTED_BASELINE_COMMIT_PATH != RETURNED_BASELINE_BLOB_IDENTITY
BASELINE_CONTENT_FIELDS_MATCH != BASELINE_BLOB_IDENTITY_PROVEN
```

The workflow establishes one explicit comparison SHA and passes it to the policy:

```text
WEPLD_COMPARISON_SHA = github.event.pull_request.base.sha || github.sha
pull_request -> the exact PR base SHA
push to main -> the pushed canonical commit SHA
```

An exact comparison SHA is **required**. When `--remote-baseline` is selected and the comparison SHA is missing or malformed, verification fails closed rather than degrading to identity-only checking.

The baseline request is deliberately unauthenticated, which is sufficient because the repository and the baseline object are public, and it keeps any credential out of the candidate-controlled head workflow.

```text
JOB_PERMISSIONS = {}
PERSIST_CREDENTIALS = false
GITHUB_TOKEN_PASSED_TO_POLICY_SCRIPT = NO
```

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

#### Returned object identity is bound to the requested SHA

Each Git data response is bound to the object identity that was actually requested, not merely to the request URL:

```text
COMMIT_RESPONSE_SHA == REQUESTED_CANDIDATE_COMMIT_SHA
TREE_RESPONSE_SHA   == REQUESTED_TREE_SHA
BLOB_RESPONSE_SHA   == REQUESTED_BLOB_SHA
IDENTITY_MISMATCH   = FAIL_CLOSED_BEFORE_CONSUMPTION
```

The returned SHA must exist, be a valid Git object SHA, and equal the requested SHA case-insensitively, consistent with the existing SHA normalization policy. A tree response is rejected before its entries are enumerated, and a blob response is rejected before its content is decoded or consumed. Size and content-shape checks are not treated as a substitute for identity.

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

These paths remain byte-frozen against the trusted base, separately from the presence rule below.

### Trusted-base tracked path preservation

The stage allowlist permits any Markdown under `docs/` or `specs/`, and `REQUIRED_PATHS` is a deliberate subset rather than a complete inventory of trusted-base documentation/evidence. Without a further rule, a candidate could silently delete canonical governance, acquisition, historical, learning, or evidence documents that no fixed list enumerates.

The authoritative layer therefore validates both tracked-entry sets and rejects deletions:

```text
TRUSTED_BASE_EXISTING_PATH -> candidate may preserve
TRUSTED_BASE_EXISTING_PATH -> candidate may modify only if other policy permits
TRUSTED_BASE_EXISTING_PATH -> candidate may not silently delete
NEW_CANDIDATE_PATH         -> allowed only through the stage allowlist
```

This is **presence** preservation, derived from the trusted base checkout rather than a hard-coded enumeration.

```text
PRESENCE_PRESERVATION != CONTENT_FREEZE
```

Markdown is not byte-frozen: candidate modifications to non-base-controlled `docs/`/`specs/` documents remain eligible under existing stage rules, `BASE_CONTROLLED_PATHS` continue byte-for-byte comparison, and candidate additions must still satisfy the stage allowlist.

This records the S1 admission policy's current fail-closed behavior. It does not create an eternal prohibition on deletion; a separately governed future policy migration may define deletion/retirement semantics.

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

### Structural graph rules

Presence of the required name/version tuples is not sufficient; a hand-authored or minimally synthetic package list must not satisfy Stage B2. The lock must additionally satisfy:

- **duplicate name/version rejection** — no `(name, version)` identity may appear more than once; entries that differ only by declared source still collide and are rejected;
- **workspace source binding** — the exact Stage-B workspace identities `wepld-desktop 0.0.0`, `wepld-contracts 0.0.0`, and `wepld-core 0.0.0` must be source-less and checksum-less; they may not be represented as crates.io/registry packages;
- **restricted source-less packages** — no identity other than those exact workspace/path packages may be source-less;
- **dependency reference resolution** — `dependencies` must be a list of strings; the reference forms `name`, `name version`, and `name version (source)` are parsed; every reference must resolve uniquely to a package identity present in the lock; unresolved and ambiguous references are rejected;
- **dependency source binding** — when a dependency reference explicitly includes `(source)`, that qualifier must exactly match the observed source of the resolved package rather than being discarded.

Required direct workspace edges, version-bound, implied by the exact Stage-B manifests (Cargo.lock merges normal and build dependencies into one `dependencies` array, so `tauri-build` is expected on `wepld-desktop`):

```text
wepld-desktop 0.0.0 ->
  tauri 2.11.5
  wepld-contracts 0.0.0
  tauri-build 2.6.3

wepld-contracts 0.0.0 ->
  serde 1.0.229
  serde_json 1.0.151

wepld-core 0.0.0 ->
  wepld-contracts 0.0.0
```

Transitive edges are not asserted, because they are not implied by WePLD-owned manifests.

### Claim boundary

These rules are evaluated by parsing bytes in a data-only path. No candidate Cargo and no candidate code of any kind is executed by `pull_request_target` or the privileged policy path, and parsing cannot establish what produced a file.

```text
STRUCTURALLY_CONSISTENT_LOCK != CARGO_GENERATION_PROVENANCE
```

Cargo-generation provenance, `cargo tree`, feature inventory, SBOM, and advisory evidence remain S1-004/S1-005 responsibilities. The lockfile still does not establish runtime admission.

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
- historical `FRESH_IMPLEMENTATION_DEPENDENCIES = 0` evidence;
- immutable remote baseline validation on every `foundation-integrity` run;
- returned Git tree/blob identity binding;
- immutable baseline Contents API blob identity binding;
- workspace package/source binding and source-qualified dependency-edge validation;
- trusted-base tracked-path presence preservation in the authoritative path.

## Review-finding reconciliation

Reviewer output is untrusted evidence, not repository authority. Canonical WePLD documents outrank reviewer-product rules.

```text
REVIEW_HEAD = a29382c99286c1d1b32d9fb799ed3e8ac78fe32a
```

Dispositions derived from validated review evidence across subsequent exact heads:

```text
R1_IMMUTABLE_BASELINE =
VALID / BLOCKING / REPAIRED

R2_TREE_BLOB_IDENTITY =
VALID / BLOCKING / REPAIRED

R3_LOCKFILE_STRUCTURE =
VALID_IN_PART / MATERIAL / STRUCTURAL_REPAIR

R3_GENERATION_PROVENANCE =
NOT_PROVEN / DEFERRED_TO_S1_004_S1_005

R4_TRUSTED_BASE_PATH_DELETION =
VALID / MATERIAL / REPAIRED

R5_IMMUTABLE_BASELINE_BLOB_IDENTITY =
VALID / MATERIAL / SECURITY_RELEVANT / REPAIRED

R6_WORKSPACE_SOURCE_IDENTITY =
VALID / MATERIAL / REPAIRED

R7_DEPENDENCY_SOURCE_QUALIFIER =
VALID / MATERIAL / REPAIRED

R8_CASE_VARIANT_PATH_DELETION =
REJECTED / FALSE_POSITIVE / NO_REPAIR

R9_LOCK_IDENTITY_SPEC_ALIGNMENT =
VALID / MATERIAL / DOCS_TRUTH_REPAIR

R10_ORDER_DEPENDENT_WORKSPACE_SELFTEST =
VALID / LOW / NON_MATERIAL / DEFERRED

QODO_BUILD_REPORT_ARTIFACT =
REJECTED / NON_CANONICAL_REVIEWER_RULE / NO_REPAIR
```

`R3` is a structural repair by design. The finding framed the defect as a lockfile that is not the generated resolved graph; structural parsing cannot establish generation provenance, and executing candidate Cargo in the privileged path is prohibited. The repair therefore closes the fabricated-list bypass without making the provenance claim.

R6 closes the inverse source-identity gap: the three exact workspace identities are not merely the only identities *allowed* to be source-less; they are also *required* to remain source-less/checksum-less, so a registry package cannot masquerade as an exact local workspace member.

R7 preserves and checks an explicit Cargo.lock dependency source qualifier instead of discarding it after parsing. A source-qualified dependency reference is accepted only when the qualifier equals the observed source of the resolved name/version package; the ordinary unqualified Cargo.lock forms remain supported.

R8 is rejected because the proposed bypass does not exist in the current exact-path subtraction. If the trusted base contains `docs/Foo.md` and the candidate only contains `docs/foo.md`, then `base_paths - candidate_paths` still contains `docs/Foo.md`, so the candidate is already rejected as a deletion. Case-folding across the two trees as suggested would instead weaken exact-path preservation by treating a case-only replacement as presence. No R8 mutation is made.

R9 corrects the specification to match the fail-closed implementation: duplicate rejection is keyed by `(name, version)`, so entries that differ only by declared source are still duplicates. The previous wording incorrectly said source was part of that duplicate identity while simultaneously claiming source-only variants collided.

R10 is a valid maintainability observation but does not change the current policy result: the fixture order is stable and exact-head selftests exercise the intended workspace-source failure. It is explicitly deferred rather than relabeled as a correctness/security PASS or silently ignored.

The Qodo rule requiring a machine-readable per-run build-report artifact is rejected. A trusted-base reread of `AGENTS.md`, the canonical documents, the governance documents, and the active S1 Spec Kit files established no matching WePLD requirement. No `actions/upload-artifact`, additional workflow permission, or build-report subsystem is introduced; adding that machinery on reviewer-product authority alone would expand S1-003 scope and workflow attack surface.

The new exact head is intentionally **not** recorded in this tracked file: writing the resulting SHA here would recursively change that SHA. Exact-head CI, security, egress, and independent-review binding remain GitHub-side evidence.

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
- base-controlled policy mutation;
- absent or malformed immutable-baseline comparison SHA;
- immutable baseline response with wrong, missing, or malformed returned blob identity;
- immutable baseline response with non-base64 encoding;
- Git tree response returning an object SHA other than the requested tree;
- Git blob response returning an object SHA other than the requested blob;
- malformed returned object identity;
- fabricated minimal lock containing only the required package tuples;
- duplicate lock package identity;
- unexpected source-less lock package;
- exact workspace identity represented as a registry package;
- missing required direct workspace edge;
- required edge resolving to the wrong version;
- dependency reference to a nonexistent package;
- dependency reference to an unresolved version;
- dependency reference with a mismatched explicit source qualifier;
- ambiguous unversioned dependency reference;
- malformed dependency reference;
- silently deleted optional trusted-base evidence document.

A paired positive lock fixture also proves that a dependency reference qualified with the exact canonical crates.io source remains accepted, so source binding does not degrade into rejection of valid source-qualified references.

Each negative probe asserts the **reason** for rejection rather than accepting any failure, so a probe cannot pass incidentally; the reason-asserting helper is itself meta-tested against a wrong-reason failure and a non-failure. The object-identity probes drive the real `RemoteRepositoryView` logic against canned Git data responses, proving rejection occurs before tree entries are enumerated or blob content is decoded, and that correct responses still succeed. The lock probes are paired with a positive structurally valid fixture, so hardening cannot degrade into "reject every lock".

These dependency-labeled probes prove **exact Stage-B template drift rejection** plus the structural graph rules above. They do not claim Cargo-generation provenance or independent semantic manifest rules beyond the exact templates.

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