# OpenHands Qualified Mechanism Extraction — Native Assurance / Runtime Inputs

```text
DATE = 2026-09-02
STATUS = RESEARCH_AND_SOURCE_ACQUISITION_INPUT_ONLY
CURRENT_ACTIVE_SLICE = S2
TARGET_FUTURE_SLICES = S3 + S6 + S7 + S8 + S9
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = PROHIBITED
DONOR_INSTALLATION = PROHIBITED
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

## 1. Purpose

This record converts the OpenHands reconnaissance into exact, path-level mechanism candidates for WePLD.

The goal is not to clone OpenHands or import its runtime wholesale. The goal is to identify the smallest solved mechanisms worth adapting into WePLD-owned contracts while preserving stricter WePLD authority, evidence, freshness, security, and completion boundaries.

```text
OPENHANDS_MECHANISM != WEPLD_ARCHITECTURE_AUTHORITY
PUBLIC_SOURCE != SOURCE_ADMISSION
MIT_LICENSE_OBSERVED != IMPORT_AUTHORIZED
RISK_CLASSIFICATION != EFFECT_AUTHORITY
RUNTIME_CONTEXT != EFFECT_AUTHORITY
BACKEND_AVAILABLE != BACKEND_SELECTED
BACKEND_FAILURE != SILENT_FALLBACK_PERMISSION
EVENT_RECORDED != AUTHORIZED_EFFECT
TEST_PASS != TRUSTED_COMPLETION
```

## 2. Exact upstream identities

### 2.1 Agent Canvas / control-center repository

```text
REPOSITORY = OpenHands/OpenHands
PIN = a4aca995912b5041ed5c9f8dd4389b06fc283cab
LICENSE_FILE = LICENSE
LICENSE_OBSERVED = MIT
ROLE = frontend control center + backend selection + local-stack orchestration + review/architecture guard examples
```

### 2.2 Canonical agent/runtime repository

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
LICENSE_FILE = LICENSE
LICENSE_OBSERVED = MIT
ROLE = agents + tools + conversations + events + workspaces + Agent Server + security-risk machinery
```

The current OpenHands architecture is multi-repository. `OpenHands/OpenHands` is not the canonical owner of agent/tool/workspace execution. Runtime/source admission must therefore be evaluated against the exact owning repository/path, not the product name alone.

## 3. Candidate OH-M001 — executable architecture guard

### Exact source quarry

```text
REPOSITORY = OpenHands/OpenHands
PIN = a4aca995912b5041ed5c9f8dd4389b06fc283cab
PRIMARY_PATH = src/api/no-direct-agent-server-calls.test.ts
PRIMARY_BLOB = fcf6b3255db3e64af3340682db7e742ec0018124
SUPPORTING_PATH = eslint.config.js
SUPPORTING_BLOB = 6645535212971a69e49ddab85c7d8bb7c2027788
REVIEW_RULE_PATH = .agents/skills/custom-codereview-guide.md
REVIEW_RULE_BLOB = d0e7f2fdb7cdf048cb698d140ab3f947eb6aeb44
```

### Mechanism extracted

OpenHands makes a repository architecture decision executable in two layers:

1. a focused repository test scans source files and rejects known direct/bypass access patterns;
2. a local lint rule catches one important bypass class in the editor/normal lint loop.

The review guide then treats the executable guard as the source of truth rather than duplicating a brittle allowlist into prose.

### WePLD adaptation

Create an Assurance architecture-rule class that can express:

```text
ArchitectureRule
  rule_id
  owner
  allowed_dependency_direction
  forbidden_patterns[]
  bounded_exceptions[]
  source_scope
  evidence_producer
  severity
  rationale
```

Initial native `/review --architecture` tracer-bullet candidates should enforce WePLD-owned boundaries such as:

```text
UI_OR_AGENT_PRESENTATION != DIRECT_EFFECT_EXECUTION
ASSURANCE_FINDING != NAWAT_GRANT
AMAN_FINDING != DIRECT_REPAIR_AUTHORITY
FEHREST_INDEX != SOURCE_OF_TRUTH
S8_REPAIR != REVIEW_ACCEPTANCE
RUNTIME_ADAPTER != SILENT_PROVIDER_FALLBACK
```

The implementation should prefer AST/semantic rules where available, with bounded textual guards only for rules whose failure mode is reliably represented textually.

### Negative oracles

```text
OH-N009 ARCHITECTURE_GUIDE_ONLY_NOT_ENOUGH
OH-N010 TEXT_REGEX_GUARD_NOT_SEMANTIC_PROOF
OH-N011 EXCEPTION_ALLOWLIST_CHANGE_IS_ARCHITECTURE_CHANGE
OH-N012 LINT_PASS_NOT_WHOLE_REPOSITORY_REVIEW_PASS
```

## 4. Candidate OH-M002 — evidence-proportional review

### Exact source quarry

```text
REPOSITORY = OpenHands/OpenHands
PIN = a4aca995912b5041ed5c9f8dd4389b06fc283cab
PATH = .agents/skills/custom-codereview-guide.md
BLOB = d0e7f2fdb7cdf048cb698d140ab3f947eb6aeb44
```

### Mechanism extracted

The review policy distinguishes evidence by behavior class rather than treating one green unit-test suite as universal proof. It also asks reviewers to focus on correctness/security/architecture and to avoid manufacturing low-value formatting feedback already handled by deterministic tools.

### WePLD adaptation

Use this as a behavior oracle for `AssurancePlan` selection:

```text
change_class -> minimum evidence class
UI behavior -> focused interaction/runtime evidence
CLI/API/script behavior -> exact invocation + observed structured result
full-stack behavior -> integration/E2E evidence
architecture boundary -> executable architecture guard + semantic review
security-sensitive behavior -> deterministic security evidence + AMAN finding state
```

This reinforces:

```text
FULLTEST = MINIMUM_SUFFICIENT_ASSURANCE_FOR_REQUESTED_CLAIM
FULLTEST != RUN_EVERY_AVAILABLE_COMMAND
UNIT_PASS != END_TO_END_PROOF
FORMATTER_CLEAN != SEMANTIC_REVIEW_CLEAN
```

## 5. Candidate OH-M003 — immutable event identity + lineage

### Exact source quarry

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
EVENT_PATH = openhands-sdk/openhands/sdk/event/base.py
EVENT_BLOB = 7c464d661d3f1ea948c4d76d855ae3b1468f47b8
EVENT_STORE_PATH = openhands-sdk/openhands/sdk/conversation/event_store.py
EVENT_STORE_BLOB = d36eb0143f95a63561ad6914a989a3268301221f
```

### Mechanism extracted

Useful mechanics:

- immutable event models;
- stable event IDs;
- explicit `parent_id` lineage;
- branch-aware path-to-root traversal;
- duplicate-ID rejection;
- parent existence validation;
- explicit cycle detection;
- a distinction between persistent events and transient streaming behavior elsewhere in the event model.

### WePLD adaptation

Do not copy OpenHands persistence as the WePLD evidence store. Reuse only the lineage/event semantics as design input for Mission/Attempt/Assurance provenance.

Candidate WePLD-owned event envelope:

```text
AttemptEvent
  schema_version
  event_id
  attempt_id
  mission_id
  parent_event_id = value | root
  event_kind
  producer
  exact_target_ref
  authority_ref = optional
  evidence_refs[]
  observed_at
  payload_digest
  payload
```

Required rules:

```text
EVENT_ID = IMMUTABLE
PARENT_REF_MUST_EXIST_OR_EXPLICIT_ROOT
EVENT_GRAPH_CYCLE = INVALID
EVENT_ORDER != EFFECT_AUTHORITY
EVENT_APPEND != TRUSTED_COMPLETION
STREAMING_EVENT != DURABLE_EVIDENCE_UNLESS_PROMOTED_BY_CONTRACT
```

### OpenHands mechanics not adopted

OpenHands `EventLog` uses a file-per-event log plus file-store locking and explicitly notes limitations on NFS/network filesystems. WePLD already has stronger generation/current-pointer and bounded lock semantics in S2. Therefore:

```text
OPENHANDS_EVENT_PERSISTENCE = BEHAVIOR_ORACLE_ONLY
WEPLD_GENERATION_MODEL = RETAIN
```

No source-admission candidate should copy the event-store persistence layer unless a future benchmark demonstrates a missing mechanism not already solved by WePLD.

## 6. Candidate OH-M004 — workspace abstraction, with authority split

### Exact source quarry

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
PATH = openhands-sdk/openhands/sdk/workspace/base.py
BLOB = 187312f8783dc0823c92d8411818385181e04c3a
RELATED_FACTORY_PATH = openhands-sdk/openhands/sdk/workspace/workspace.py
REMOTE_IMPLEMENTATION_FAMILY = openhands-sdk/openhands/sdk/workspace/remote/
CONTAINER_IMPLEMENTATION_FAMILY = openhands-workspace/openhands/workspace/docker/
```

### Mechanism extracted

OpenHands separates a common workspace interface from local/remote/container-backed implementations and gives workspaces explicit lifecycle/resource-management behavior.

### WePLD adaptation

WePLD must split the interface more aggressively than OpenHands because a broad workspace with `execute_command`, file read/write, Git, and callbacks collapses capabilities that Nawat must govern separately.

Candidate WePLD decomposition:

```text
WorkspaceIdentity
WorkspaceReadCapability
WorkspaceWriteCapability
ProcessExecutionCapability
GitObservationCapability
BrowserCapability
NetworkCapability
ArtifactTransferCapability
RuntimeLifecycleCapability
```

A runtime backend may implement several capabilities, but an Attempt receives only exact granted capability handles.

```text
WORKSPACE_SELECTED != ALL_WORKSPACE_CAPABILITIES_GRANTED
WORKSPACE_PATH != FILESYSTEM_AUTHORITY
PROCESS_CAPABILITY != NETWORK_CAPABILITY
GIT_OBSERVATION != GIT_MUTATION
REMOTE_RUNTIME != REMOTE_EGRESS_AUTHORITY
```

### Critical negative oracle from upstream

OpenHands `BaseWorkspace` includes environment-driven best-effort completion callbacks over HTTP. That mechanism must not be inherited into a WePLD generic workspace base. In WePLD:

```text
RUNTIME_LIFECYCLE_CALLBACK != IMPLICIT_NETWORK_AUTHORITY
ENV_VAR_PRESENT != EGRESS_AUTHORIZATION
```

Any callback/automation/report transport belongs behind explicit network/egress authority and typed destination identity.

## 7. Candidate OH-M005 — explicit runtime-service advertisement

### Exact source quarry

```text
REPOSITORY = OpenHands/OpenHands
PIN = a4aca995912b5041ed5c9f8dd4389b06fc283cab
PATH = scripts/runtime-services-info.mjs
BLOB = 0519076637424ab95532bbb4e2bfcede688b2e5b
TEST_PATH = __tests__/scripts/runtime-services-info.test.ts
```

### Mechanism extracted

OpenHands constructs one structured description of services reachable from the agent's point of view and sends that explicit topology to the agent instead of having the agent probe random ports.

Useful principles:

- runtime topology has one producer;
- URLs are expressed from the consumer/agent point of view;
- absent services are omitted rather than advertised as guessed placeholders;
- invalid missing required runtime identity fails early.

### WePLD adaptation

Candidate contract:

```text
RuntimeCapabilityAdvertisement
  runtime_id
  attempt_id
  observed_at
  service_id
  service_kind
  endpoint_identity
  transport
  capability_classes[]
  auth_reference = opaque | none
  provenance
  freshness_basis
```

But this record is context only:

```text
ADVERTISEMENT != NAWAT_GRANT
ENDPOINT_ADVERTISED != NETWORK_AUTHORITY
AUTH_REFERENCE_PRESENT != AUTHORIZED_USE
PROMPT_CONTEXT != TRUSTED_AUTHORITY
```

WePLD should prefer structured runtime context outside free-form prompt text where possible; prompt rendering can be a projection, not the authority-bearing representation.

## 8. Candidate OH-M006 — backend registry UX, with no-fallback inversion

### Exact source quarry

```text
REPOSITORY = OpenHands/OpenHands
PIN = a4aca995912b5041ed5c9f8dd4389b06fc283cab
PATH = src/api/backend-registry/active-store.ts
BLOB = 8373cbdb87cb43579d6c24c8874820c4fa576633
```

### Mechanism extracted

Useful behavior:

- durable backend registry;
- explicit active selection;
- sentinel for no usable backend;
- backend-kind-aware routing;
- selected backend context kept separate from registered backend inventory.

### Mechanism explicitly rejected

The OpenHands implementation contains deterministic fallback behavior that may choose another healthy/local backend when the explicit selection is absent or removed.

That is a product-UX choice in OpenHands and a **negative oracle** for WePLD effectful Attempts.

WePLD must instead use:

```text
AttemptBackendBinding
  attempt_id
  backend_id
  backend_kind
  runtime_identity
  capability_snapshot_ref
  selected_at
  freshness_basis
```

and enforce:

```text
SELECTED_BACKEND_MISSING -> BACKEND_UNAVAILABLE
SELECTED_BACKEND_UNHEALTHY -> BACKEND_UNAVAILABLE
SELECTED_BACKEND_REMOVED -> BACKEND_SELECTION_STALE
NO SILENT FALLBACK
NO BORROWING_CAPABILITY_FROM_ANOTHER_REGISTERED_BACKEND
```

A user may explicitly choose a replacement backend in a new authority-bearing transition. The runtime must not silently do so.

## 9. Candidate OH-M007 — action event separates executable action from model/tool-call representation

### Exact source quarry

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
PATH = openhands-sdk/openhands/sdk/event/llm_convertible/action.py
BLOB = 94816b2b5f7eb51f8b3f5af5fecb1f3bd8169a2b
```

### Mechanism extracted

OpenHands keeps both the model-returned tool call and a separately validated/executable action field, and allows an action to be absent even when a function/tool call exists.

This is directly useful for WePLD's proposal/effect split.

Candidate mapping:

```text
ToolCallProposal
  provider_call_id
  proposed_tool
  raw_arguments_digest
  normalized_intent
  risk_evidence_ref

AuthorizedEffect
  proposal_ref
  nawat_grant_ref
  exact_capability_ref
  exact_target_ref
  normalized_arguments
```

Required invariant:

```text
MODEL_TOOL_CALL != EXECUTABLE_ACTION
TOOL_CALL_PARSED != AUTHORIZED_EFFECT
ACTION_SUMMARY != AUTHORITY
MODEL_RISK_LABEL != AMAN_FINDING
```

## 10. Candidate OH-M008 — security risk taxonomy + confirmation oracle

### Exact source quarry

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
RISK_PATH = openhands-sdk/openhands/sdk/security/risk.py
RISK_BLOB = 755fa1553c9dbcb3ca9a37ca8224fd538d06ddaf
CONFIRMATION_PATH = openhands-sdk/openhands/sdk/security/confirmation_policy.py
CONFIRMATION_BLOB = ea1d65f01624793082e237f1feaa557d7e101493
```

### Mechanism extracted

Useful behavior:

- closed concrete risk levels plus UNKNOWN;
- UNKNOWN is deliberately not comparable to concrete risk levels;
- confirmation policy can be configured separately from risk assessment.

### WePLD adaptation

Retain AMAN as risk/security evidence owner and Nawat as effect authority owner.

Possible shared presentation severity may learn from the closed enum, but authority cannot be derived from it.

```text
UNKNOWN_RISK != LOW_RISK
LOW_RISK != AUTHORIZED
HIGH_RISK != AUTOMATIC_DENIAL_WITHOUT_POLICY_CONTEXT
NEVER_CONFIRM != AUTHORIZED
CONFIRM_RISKY != NAWAT_POLICY
```

## 11. Candidate OH-M009 — worst-case security fusion

### Exact source quarry

```text
REPOSITORY = OpenHands/software-agent-sdk
PIN = e26683288ab4dd69518810016b74682de2a8c4e4
PATH = openhands-sdk/openhands/sdk/security/ensemble.py
BLOB = f98f04dcdd94eab21bb3d9e76f0d7d6063722f47
```

### Mechanism extracted

The ensemble uses maximum concrete severity and treats analyzer exceptions as HIGH rather than silently reducing risk. It can also propagate UNKNOWN in a stricter mode.

### WePLD adaptation

Do not reduce all Assurance findings to one scalar risk number. Preserve each finding and its evidence. However, the non-erasure principle is valuable:

```text
ONE_VALIDATED_HIGH_FINDING_REMAINS_HIGH
CLEAN_ANALYZER_OUTPUT_CANNOT_VOTE_AWAY_VALIDATED_FINDING
ENGINE_EXCEPTION != CLEAN_RESULT
UNKNOWN_COVERAGE != SAFE_COVERAGE
```

For an aggregate UI badge, derive a projection from preserved findings; never replace them with the projection.

## 12. Source-admission disposition

### P0 — strong candidates for clean-room adaptation first

```text
OH-M001 executable architecture guard
OH-M002 evidence-proportional review rules
OH-M005 explicit runtime-service advertisement semantics
OH-M006 backend registry identity/selection model, with fallback inverted to fail-closed
OH-M007 tool-call proposal != executable action
OH-M009 non-erasing security fusion semantics
```

Preferred initial method:

```text
MODE = CLEAN_ROOM_ADAPTATION_FROM_BEHAVIOR_AND_CONTRACT
SOURCE_COPY = NO
DEPENDENCY_IMPORT = NO
```

Reason: the useful ideas are small and can be represented directly in WePLD-owned Rust/contracts without importing JavaScript/Python runtime machinery.

### P1 — path-level source study after owning slice activates

```text
OH-M003 event lineage model
OH-M004 workspace interface family
OH-M008 risk/confirmation model
```

Before any direct source reuse:

1. reverify exact upstream pin;
2. reverify license and any path-level exceptions;
3. record attribution obligations;
4. prove the smallest exact source path is preferable to a clean-room implementation;
5. create canonical source-admission evidence;
6. prohibit donor build/install/hooks/workflows during reconnaissance;
7. independently review the adapted exact WePLD head.

## 13. Native Assurance mapping

```text
/review
  <- OH-M001 executable architecture rules
  <- OH-M002 evidence-proportional review
  <- OH-M003 lineage for review evidence

/security
  <- OH-M007 proposal/action separation
  <- OH-M008 risk representation oracle
  <- OH-M009 non-erasing fail-closed fusion
  <- AMAN remains canonical security owner

/fulltest
  <- OH-M002 evidence proportional to change/claim
  <- OH-M003 exact event/evidence lineage
  <- TEST_PASS != TRUSTED_COMPLETION

S3
  <- OH-M004 capability-split workspace/runtime patterns

S6
  <- OH-M005 explicit runtime advertisement
  <- OH-M006 exact backend binding / no silent fallback

S8
  <- OH-M007 proposal -> authorized effect split

S9
  <- OH-M003 event lineage as provenance input
```

## 14. Required negative-oracle additions

```text
AF-N027 ARCHITECTURE_GUIDE_ONLY_NOT_ENOUGH
AF-N028 ARCHITECTURE_EXCEPTION_CHANGE_REQUIRES_REVIEW
AF-N029 EVENT_PARENT_MISSING_FAILS_CLOSED
AF-N030 EVENT_GRAPH_CYCLE_INVALID
AF-N031 WORKSPACE_SELECTED_NOT_ALL_CAPABILITIES_GRANTED
AF-N032 ENV_CALLBACK_NOT_IMPLICIT_NETWORK_AUTHORITY
AF-N033 RUNTIME_ADVERTISEMENT_NOT_EFFECT_AUTHORITY
AF-N034 BACKEND_REMOVAL_NOT_SILENT_FALLBACK
AF-N035 MODEL_TOOL_CALL_NOT_EXECUTABLE_ACTION
AF-N036 UNKNOWN_RISK_NOT_SAFE
AF-N037 ANALYZER_EXCEPTION_NOT_CLEAN_RESULT
AF-N038 CLEAN_ENGINE_CANNOT_VOTE_AWAY_VALIDATED_FINDING
AF-N039 OPENHANDS_EVENT_STORE_NFS_LIMITATION_NOT_WEPLD_DURABILITY_PROOF
```

## 15. Acceptance boundary

This extraction is complete as research when the exact upstream identities, source paths, mechanism decisions, rejected semantics, negative oracles, and WePLD mappings are preserved in repository-visible planning.

It does not make source or implementation eligible by itself.

```text
MECHANISM_EXTRACTED = YES
SOURCE_ADMITTED = NO
IMPLEMENTATION_AUTHORIZED_BY_THIS_RECORD = NO
DONOR_CODE_EXECUTED = NO
DONOR_DEPENDENCY_INSTALLED = NO
```

The next implementation action remains governed by the live canonical slice. When S3/S6/S7 authority activates, prefer the clean-room WePLD-owned contracts above before considering any direct OpenHands source import.