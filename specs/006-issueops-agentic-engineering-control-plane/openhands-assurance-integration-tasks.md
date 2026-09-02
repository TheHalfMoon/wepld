# OpenHands Mechanism Integration Task Map

```text
STATUS = FUTURE_TASK_MAP_BOUND_TO_CANONICAL_SLICE_ACTIVATION
SOURCE_RECORD = research/openhands-qualified-mechanism-extraction-2026-09-02.md
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE_BY_THIS_FILE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

This task map turns the path-level OpenHands mechanism extraction into dependency-ordered WePLD-native implementation work. No task becomes eligible merely because it appears here. Each task requires the then-current canonical slice/authority to grant its exact product/test paths and effects.

## A. S3 — bounded runtime capability substrate

### OH-S3-001 — capability-split workspace contract

Depends on: S3 runtime/process planning and canonical authority.

Implement WePLD-owned capability interfaces rather than one broad OpenHands-style workspace:

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

Acceptance:

- selecting a workspace grants no capability by itself;
- process execution cannot imply network;
- Git observation cannot imply Git mutation;
- file read cannot imply file write;
- capability IDs are exact and inspectable;
- no ambient environment callback may create network effects.

Negative oracles: `AF-N031`, `AF-N032`.

### OH-S3-002 — runtime capability advertisement contract

Depends on: OH-S3-001.

Implement a structured, non-authoritative runtime advertisement model inspired by OpenHands runtime-service metadata:

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
  auth_reference
  provenance
  freshness_basis
```

Acceptance:

- absent service is absent, never guessed;
- malformed/missing required runtime identity fails closed;
- advertisement cannot grant network/process/browser/file authority;
- prompt text is only a projection of the structured record;
- service freshness is explicit.

Negative oracle: `AF-N033`.

## B. S6 — exact backend/runtime binding

### OH-S6-001 — backend registry model

Depends on: S3 runtime identity.

Implement explicit registered-backend inventory and active selection as separate concepts.

Required states:

```text
registered
selected
unavailable
unhealthy
removed
selection_stale
```

### OH-S6-002 — AttemptBackendBinding

Depends on: OH-S6-001.

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

Acceptance:

```text
selected backend missing -> BACKEND_UNAVAILABLE
selected backend unhealthy -> BACKEND_UNAVAILABLE
selected backend removed -> BACKEND_SELECTION_STALE
NO_SILENT_FALLBACK
NO_CAPABILITY_BORROWING_FROM_OTHER_BACKEND
```

A backend replacement requires an explicit new selection/authority transition.

Negative oracle: `AF-N034`.

## C. S7-A — Assurance architecture-rule core

### OH-S7-001 — ArchitectureRule contract

Depends on: Fehrest ownership/context interfaces available to S7.

```text
ArchitectureRule
  rule_id
  owner
  rule_version
  source_scope
  allowed_dependency_direction
  forbidden_relation_classes[]
  bounded_exceptions[]
  severity
  rationale
  evidence_requirements[]
```

### OH-S7-002 — executable architecture guard engine

Depends on: OH-S7-001 + structural source facts.

Implement deterministic architecture checks as first-class Assurance producers, not prose-only review instructions.

Initial rule candidates:

```text
UI_OR_AGENT_PRESENTATION != DIRECT_EFFECT_EXECUTION
ASSURANCE_FINDING != NAWAT_GRANT
AMAN_FINDING != DIRECT_REPAIR_AUTHORITY
FEHREST_INDEX != SOURCE_OF_TRUTH
S8_REPAIR != REVIEW_ACCEPTANCE
RUNTIME_ADAPTER != SILENT_PROVIDER_FALLBACK
```

Acceptance:

- deterministic findings have exact locations/relation evidence;
- bounded exceptions are visible and reviewed as architecture changes;
- textual fallback checks cannot claim semantic proof;
- rule configuration from an untrusted source branch cannot weaken canonical rules.

Negative oracles: `AF-N027`, `AF-N028`.

### OH-S7-003 — repeated-review-to-rule promotion proposal

Depends on: finding history available.

Detect repeated equivalent architecture findings and propose, but never auto-authorize, a deterministic rule candidate.

```text
REPEATED_FINDING -> RULE_PROPOSAL
RULE_PROPOSAL != RULE_ADMISSION
```

## D. S7-R — `/review` evidence-proportional planning

### OH-S7-004 — change/evidence-class matrix

Define minimum evidence classes by changed behavior:

```text
UI behavior -> focused interaction/runtime evidence
CLI/API/script behavior -> exact invocation + structured observed result
full-stack behavior -> integration/E2E evidence
architecture boundary -> deterministic architecture guard + semantic review
security-sensitive behavior -> AMAN/security evidence + relevant deterministic engines
```

### OH-S7-005 — review noise suppression

Deterministic formatter/linter-only issues should remain tool diagnostics, while semantic `/review` prioritizes correctness, architecture, security, evidence gaps, and acceptance contradictions.

```text
FORMATTER_FINDING != SEMANTIC_REVIEW_FINDING_BY_DEFAULT
```

### OH-S7-006 — review evidence lineage

Depends on: OH-S7-010 event lineage below.

Bind each finding to exact target/head, producer identity/version, context/evidence references, and freshness state.

## E. S7-S — `/security` action/risk separation

### OH-S7-007 — ToolCallProposal contract

```text
ToolCallProposal
  proposal_id
  provider_call_id
  proposed_tool
  raw_arguments_digest
  normalized_intent
  exact_target_ref
  risk_evidence_refs[]
```

### OH-S7-008 — AuthorizedEffect projection

Depends on: Nawat effect authority surface.

```text
AuthorizedEffect
  proposal_ref
  nawat_grant_ref
  exact_capability_ref
  exact_target_ref
  normalized_arguments
```

Acceptance:

```text
MODEL_TOOL_CALL != EXECUTABLE_ACTION
TOOL_CALL_PARSED != AUTHORIZED_EFFECT
MODEL_RISK_LABEL != AMAN_FINDING
```

Negative oracle: `AF-N035`.

### OH-S7-009 — non-erasing security aggregation

Preserve all findings. Aggregate severity is a projection only.

Rules:

```text
ONE_VALIDATED_HIGH_FINDING_REMAINS_HIGH
CLEAN_ENGINE_CANNOT_VOTE_AWAY_VALIDATED_FINDING
ENGINE_EXCEPTION != CLEAN_RESULT
UNKNOWN_COVERAGE != SAFE_COVERAGE
```

Use fail-closed producer-error semantics without collapsing every producer result into one scalar record.

Negative oracles: `AF-N036`, `AF-N037`, `AF-N038`.

## F. S7/S9 — event and provenance lineage

### OH-S7-010 — AttemptEvent envelope

Reuse OpenHands event lineage semantics as a behavior oracle, while retaining WePLD's generation-based durable store.

```text
AttemptEvent
  schema_version
  event_id
  attempt_id
  mission_id
  parent_event_id
  event_kind
  producer
  exact_target_ref
  authority_ref
  evidence_refs[]
  observed_at
  payload_digest
  payload
```

Acceptance:

- event ID immutable;
- parent exists or is explicit root;
- cycles invalid;
- missing parent fails closed;
- transient stream item is not durable evidence unless promoted by contract;
- event storage must use WePLD durability semantics, not copy OpenHands file-per-event/NFS-sensitive locking.

Negative oracles: `AF-N029`, `AF-N030`, `AF-N039`.

### OH-S9-001 — Quality Passport provenance projection

Depends on: OH-S7-010 + S9.

Project exact Assurance/Attempt event lineage into Quality Passport history without making history itself authority.

## G. S7-T — `/fulltest` integration

### OH-S7-011 — evidence-proportional FullTest selector

Use changed behavior + requested confidence claim + exact available engine capabilities to generate the minimum-sufficient plan.

```text
FULLTEST != RUN_EVERY_TOOL
FAST_SELECTION != QUALIFIED_SELECTION
UNIT_PASS != END_TO_END_PROOF
```

### OH-S7-012 — evidence gap finding

If required evidence class cannot be produced, emit a typed gap rather than silently degrading the claim.

Examples:

```text
E2E_REQUIRED_BUT_UNAVAILABLE
PLATFORM_REQUIRED_BUT_UNAVAILABLE
SECURITY_ENGINE_REQUIRED_BUT_FAILED
ARCHITECTURE_CONTEXT_STALE
```

## H. Tracer bullets

### OH-TB1 — architecture bypass

Fixture intentionally bypasses a typed/owned boundary.

Expected:

- deterministic architecture finding;
- exact location;
- owning rule ID/version;
- `/review` surfaces it before hosted reviewer output;
- exception cannot be added from untrusted project config.

### OH-TB2 — removed backend

An Attempt is bound to backend A. A disappears while backend B remains healthy.

Expected:

```text
BACKEND_SELECTION_STALE
NO execution on B
NO silent fallback
```

### OH-TB3 — model tool call without grant

A model emits a syntactically valid process/tool call.

Expected:

- proposal event recorded;
- risk evidence may be produced;
- no executable action without Nawat grant;
- no side effect.

### OH-TB4 — conflicting security producers

Producer A validates a HIGH finding; producer B reports clean; producer C crashes.

Expected:

- HIGH finding preserved;
- B cannot erase A;
- C represented as producer error/coverage gap;
- aggregate UI remains blocking/high/unknown according to WePLD policy, not majority vote.

### OH-TB5 — FullTest evidence gap

A full-stack change requires E2E evidence but the required runtime is unavailable.

Expected:

- no false PASS;
- explicit evidence-gap finding;
- completion claim remains unsatisfied.

## I. Source strategy

Default implementation strategy for these tasks:

```text
CLEAN_ROOM_WEPLD_NATIVE_ADAPTATION = PREFERRED
DIRECT_OPENHANDS_SOURCE_COPY = NO_BY_DEFAULT
NEW_OPENHANDS_RUNTIME_DEPENDENCY = NO_BY_DEFAULT
```

Only consider direct source reuse when a future source-admission analysis proves that the exact source machinery is materially better than a small native implementation and its maintenance/security/dependency cost is justified.

## J. Completion rule

This task map is ready when every extracted mechanism has an owning future slice, dependencies, explicit acceptance conditions, negative oracles, and tracer-bullet coverage.

It is not implementation evidence.

```text
TASK_MAP_READY = YES
CURRENT_PRODUCT_IMPLEMENTATION_AUTHORITY = UNCHANGED
CURRENT_SOURCE_ADMISSION = NONE
```
