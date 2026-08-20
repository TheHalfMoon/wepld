# Source Acquisition Check — Harness H0 Screening Falsification

## Status

```text
CHECK = ACTIVE / PRE-IMPLEMENTATION
FEATURE = 002-harness-h0-screening
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0-SCREEN
PLANNING_ORIGIN_MAIN = a377c75727456934ea6bde456e4a082bdaf710f5
PONYTAIL_FULL = COMPLETE_FOR_PLANNING_REVIEW
SOURCE_IMPORT = NONE
H0_DIRECT_DEPENDENCY_ADMISSION = NONE
HARBOR_ADMISSION = NONE
PRODUCT_RUNTIME_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
S1_013_PLUS = NOT_STARTED
```

This record intentionally remains `OPEN`. Existing S1 source/dependency evidence and the canonical Harness donor research are prior evidence only. They do not create H0 direct-dependency, source-import, runner, provider, or product authority.

## Acquisition principles

For each external component actually needed by H0-SCREEN:

1. establish the exact source/release/package identity;
2. inspect relevant source/tests/failure behavior;
3. establish license/notice/permission obligations;
4. inspect security/advisory and dependency surface;
5. prove portability for the claimed screening environment;
6. define the minimum features/API surface;
7. record maintenance health and replacement/exit strategy;
8. preserve WePLD-owned identity/evidence/verifier/authority contracts above the component;
9. reject the component if it expands machinery beyond the falsification need.

```text
SOURCE_AVAILABLE != SOURCE_ADMITTED
S1_ADMISSION != H0_ADMISSION
FOUNDER_PERMISSION != AUTOMATIC_ADMISSION
TRANSITIVE_PRESENCE != DIRECT_API_AUTHORITY
REFERENCE_ORACLE != RUNTIME_DEPENDENCY
```

## Prior evidence available for bounded reuse

Canonical S1 acquisition/governance already contains exact prior evidence for:

- a Rust stable toolchain candidate;
- typed Rust serialization via Serde/serde_json;
- a Windows-first Rust/Tauri toolchain and dependency graph;
- supply-chain/SBOM/advisory methodology;
- exact-head integrity and trusted-bootstrap mechanics.

H0 may cite/reuse that evidence where still applicable, but H0-specific direct use requires a new explicit disposition on the exact current H0 component set.

The canonical Harness research bundle also provides donor/runner reference evidence, including Harbor and other harness/evaluation systems. Those references remain `NOT_ADMITTED` unless an exact H0 acquisition task changes that state.

## ACQ-H0-01 — Rust toolchain

```text
ROLE = TRUSTED H0 CONTROL / EVIDENCE IMPLEMENTATION LANGUAGE
PRIOR_EVIDENCE = S1 RUST TOOLCHAIN RECORD
PLANNING_DISPOSITION = REUSE_CANDIDATE / REVERIFY
H0_ADMISSION = PENDING
```

Required before H0 admission:

- reverify the exact canonical S1 toolchain identity or select a separately justified exact toolchain;
- prove compatibility with the minimum H0 crate graph;
- record exact `rustc -Vv`/toolchain configuration in future evidence;
- preserve deterministic local build/test coverage on claimed platforms.

Do not update the toolchain merely because a newer release exists; prefer reuse if current canonical evidence remains sufficient.

## ACQ-H0-02 — Typed serialization substrate

```text
ROLE = TYPED MANIFEST / RECORD SERIALIZATION
PRIOR_EVIDENCE = S1 SERDE / SERDE_JSON ACQUISITION RECORDS
PLANNING_DISPOSITION = REUSE_CANDIDATE / REVERIFY EXACT FEATURES
H0_ADMISSION = PENDING
```

H0 requires typed representations but does not delegate canonical identity semantics to library defaults.

Required:

- exact package/source/version/features;
- deterministic serialization tests;
- explicit WePLD canonicalization rules;
- rejection/normalization rules for ambiguous or unsupported values;
- no reliance on unspecified map iteration/order;
- license/advisory/transitive evidence on the exact H0 graph.

A different mature serialization substrate may be selected only if it is smaller or materially better for the frozen H0 evidence contract.

## ACQ-H0-03 — SHA-256 implementation

```text
ROLE = CONTENT-ADDRESSED MANIFEST / RECORD IDENTITY
ALGORITHM = SHA-256
CUSTOM_IMPLEMENTATION = REJECT
PLANNING_DISPOSITION = QUALIFY_COMMODITY_IMPLEMENTATION
H0_ADMISSION = PENDING
```

Required:

- exact package/source/release pin;
- minimal features;
- license/notice review;
- advisory/security review;
- deterministic known-answer tests;
- replacement/exit path preserving SHA-256 output compatibility.

Do not silently substitute another identity algorithm because a package is easier to use; the canonical H0 research contract currently specifies SHA-256.

## ACQ-H0-04 — Local process execution primitives

```text
ROLE = MINIMUM RUNNER PROCESS LIFECYCLE
PREFERRED = RUST STDLIB FIRST
EXTERNAL_PACKAGE_REQUIRED = NOT_YET_PROVEN
H0_ADMISSION = NONE_PENDING_NEED
```

`std::process`, standard I/O/file APIs, threads/synchronization, and bounded local work queues should be evaluated before adding a process orchestration framework or async runtime solely for runner plumbing.

A direct external process/runtime crate requires a measured need and separate disposition.

## ACQ-H0-05 — Controlled local container/runtime boundary

```text
ROLE = REAL SCREENING TASK ISOLATION / EFFECT BOUNDARY
PLANNING_DISPOSITION = EXISTING_LOCAL_RUNTIME_CLI_OR_EQUIVALENT / NARROW_ADAPTER
EXACT_RUNTIME = NOT_YET_QUALIFIED
H0_PRODUCT_DEPENDENCY = NO
```

Synthetic qualification fixtures may use local processes when safe and sufficient. Real H0-SCREEN tasks may require a stronger controlled environment to substantiate network/filesystem/process isolation claims.

Before real screening execution, qualify the exact chosen runtime/CLI:

- exact product/version/build identity;
- installation/availability assumptions;
- command/API surface used by H0;
- task-network deny behavior where claimed;
- writable/readable mount semantics;
- non-privileged execution;
- no host container-engine socket exposed inside tasks;
- timeout/stop/kill/cleanup behavior;
- workspace isolation under bounded concurrency;
- stdout/stderr/artifact capture;
- resource-limit behavior where claimed;
- cross-platform limitation accounting;
- replacement/exit strategy.

Do not introduce a cloud SDK, container orchestration platform, or distributed scheduler for H0-SCREEN.

## ACQ-H0-06 — Model-provider integration boundary

```text
ROLE = MODEL INVOCATION / USAGE OBSERVATION
PLANNING_DISPOSITION = REPLACEABLE MINIMUM INTERFACE
EXACT_PROVIDER_SET = NOT_YET_FROZEN
PROVIDER_SDK_ADMISSION = NONE
```

The final screening model set is not yet frozen. Therefore no provider SDK can be justified or admitted in this planning package.

Before H0-SCREEN execution:

- freeze exact eligible model/provider/serving identities and settings;
- choose the minimum invocation mechanism for those models;
- prefer existing admitted or simple separately qualified interfaces;
- record token/cost/usage evidence exposed by the provider;
- inject credentials only at execution time by reference;
- prohibit secret values in Git/manifests/normalized public evidence;
- separate model-serving egress from task-environment egress;
- prohibit silent provider/model fallback;
- define replacement/exit behavior.

If multiple provider SDKs would be required, re-evaluate whether a smaller provider-neutral boundary or existing admitted mechanism avoids unnecessary direct dependencies.

## ACQ-H0-07 — Harbor

```text
ROLE = EVALUATION / RUNNER REFERENCE; CONDITIONAL CONFIRMATORY CANDIDATE
SCREENING_RUNNER = NO
CODE_IMPORT = NONE
H0_SCREENING_DEPENDENCY = NO
ADMISSION = NONE
```

Harbor is not admitted for H0-SCREEN. Its inspected concepts may remain behavioral/test/failure oracles.

Reopen only if the final stable screening evidence triggers runner replacement and a separate exact-pin qualification is authorized for confirmatory planning.

## ACQ-H0-08 — Harness donor repositories / papers

```text
ROLE = RESEARCH / BEHAVIOR / FAILURE / ARCHITECTURE ORACLES
SOURCE_IMPORT = NONE
RUNTIME_DEPENDENCY = NONE
ADMISSION = NONE
```

The canonical donor inventory and research dossier remain reference evidence. H0-SCREEN does not authorize importing donor runtime code merely because the research program identified useful mechanisms or founder permission exists.

Any future code reuse needs source-specific exact-pin rights/license/security/maintenance/portability/exit evidence under a separate acquisition step.

## Rejected unnecessary component classes

```text
GENERAL_HIR_FRAMEWORK = REJECT
PLUGIN_MARKETPLACE = REJECT
LLM_ROUTER = REJECT_H0_V1
GENERAL_MEMORY_PACKAGE = REJECT_H0_V1
MULTI_AGENT_ORCHESTRATION_FRAMEWORK = REJECT_H0_V1
SELF_EVOLUTION_FRAMEWORK = REJECT_H0_V1
HARNESS_SEARCH_FRAMEWORK = REJECT_H0_V1
DISTRIBUTED_SCHEDULER = REJECT
DATABASE_SERVICE = REJECT
REMOTE_JOB_SERVICE = REJECT
REMOTE_ARTIFACT_SERVICE = REJECT
CLOUD_PROVIDER_ABSTRACTION = REJECT
HOSTED_OBSERVABILITY_SDK = REJECT
CUSTOM_SHA256 = REJECT
HARBOR_SCREENING_DEPENDENCY = REJECT
```

## Dependency-resolution boundary

If the final minimum Rust component set requires new or H0-specific manifest/lock changes, dependency resolution itself must be separately authorized before implementation source is introduced.

```text
DEPENDENCY_RESOLUTION_AUTHORIZED
!=
H0_DIRECT_DEPENDENCY_ADMITTED
!=
H0_SCREEN_IMPLEMENTATION_AUTHORIZED
```

The resolution evidence must expose exact direct/transitive versions, features, licenses/notices, SBOM, advisories, and why each direct dependency remains minimum-sufficient.

## Security / egress acquisition boundary

External component/source review must follow canonical egress policy. Unknown private-data/rights/provider handling is fail-closed.

Model-provider and runner execution credentials are never acquisition artifacts. Only reference names/config contracts may be committed.

Security review is applicable to the future implementation-policy migration and any runtime/effect/container/provider boundary implementation. Codex Security unavailable remains `NOT_RUN_NON_BLOCKING`, never Security PASS.

## Final Source Acquisition Check conditions

`SOURCE_ACQUISITION_CHECK = PASS` only when one exact reviewed head establishes all of:

```text
H0_RUST_TOOLCHAIN = EXACT_AND_QUALIFIED
TYPED_SERIALIZATION_SET = EXACT_AND_QUALIFIED
CANONICALIZATION_RULES = FROZEN_AND_TESTABLE
SHA256_IMPLEMENTATION = EXACT_AND_QUALIFIED
LOCAL_EXECUTION_BOUNDARY = EXACT_AND_QUALIFIED
REAL_SCREENING_ISOLATION_RUNTIME = EXACT_AND_QUALIFIED_IF_REQUIRED
MODEL_PROVIDER_BOUNDARY = EXACT_AND_QUALIFIED_FOR_FROZEN_MODEL_SET
DIRECT_DEPENDENCY_SET = EXACT_AND_MINIMUM
TRANSITIVE_FEATURE_INVENTORY = COMPLETE_WHERE_APPLICABLE
SBOM = COMPLETE_WHERE_APPLICABLE
ADVISORY_RECONCILIATION = COMPLETE_WHERE_APPLICABLE
LICENSE_NOTICE_REVIEW = COMPLETE
REPLACEMENT_EXIT_STRATEGIES = RECORDED
HARBOR_ADMISSION = NONE_FOR_SCREENING
PRODUCT_RUNTIME_ADMISSION = NONE
```

Until then:

```text
SOURCE_ACQUISITION_CHECK = OPEN
H0_SCREEN_IMPLEMENTATION = BLOCKED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
HARNESS_SOURCE_ADMISSION = NONE
HARNESS_DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```
