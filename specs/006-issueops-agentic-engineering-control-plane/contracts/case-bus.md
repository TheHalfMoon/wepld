# Contract — Case Bus

```text
STATUS = FUTURE_PLANNING_CONTRACT
PRIMARY_OWNER = S6_MISSION_RUNTIME_COORDINATION
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
PROCESS_EXECUTION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

## Purpose

Define the Case-scoped durable coordination substrate referenced by the IssueOps plan so workers do not communicate through ad hoc provider-to-provider chat or treat arbitrary received text as workflow authority.

The Case Bus carries bounded typed coordination messages and references to durable artifacts/evidence. It is not an authority system, secret store, free-form shared memory, or provider session bus.

## Core invariants

```text
MESSAGE_RECEIVED != WORKFLOW_INTENT
MESSAGE_RECEIVED != ASSIGNMENT
MESSAGE_RECEIVED != NAWAT_GRANT
MESSAGE_RECORDED != EFFECT_AUTHORIZED
PROVIDER_ACK != MESSAGE_TRUTH
CASE_BUS != EVIDENCE_STORE
CASE_BUS != MEMORY_SOURCE_OF_TRUTH
```

## `CaseMessage`

```text
CaseMessage {
  case_message_id
  case_id
  message_act
  sender_identity
  sender_attempt_ref?
  recipient_kind
  recipient_ref
  assignment_ref?
  reply_to_message_ref?
  correlation_id?
  idempotency_key?
  body_or_summary
  artifact_refs[]
  evidence_refs[]
  decision_boundary_ref?
  trust_classification
  access_policy_ref
  created_at
  expiry_or_hop_budget?
}
```

Candidate message acts:

```text
REQUEST_WORK
PROGRESS
RESULT
FINDING
QUESTION
ANSWER
BLOCKER
HANDOFF
CANCEL_REQUEST
CANCEL_ACKNOWLEDGEMENT
REVIEW_REQUEST
REVIEW_RESULT
EVIDENCE_POINTER
```

A message act is coordination semantics only. For example `REQUEST_WORK` does not create an Assignment; the controlling workflow must explicitly create/accept one through the normal planner/runtime path.

## Addressing

Recipients are typed, for example:

```text
CASE_COORDINATOR
ASSIGNMENT
ATTEMPT
WORKER
REVIEW_ROLE
HUMAN_DECISION_BOUNDARY
```

Provider-native session/channel identifiers may appear only as provenance/transport references.

## Payload bounds

Prefer references over duplicating large context:

```text
ContextPackageRef
InputArtifactRef
RetrievalEvidenceRef
FindingRef
AssuranceBundleRef
EffectResultRef
```

Messages must have explicit size/count/hop/retention limits. Large repository dumps, secret-bearing logs, or full transcripts should not become coordination payloads by default.

## Delivery semantics

Future implementation must define at-least-once/ack/retry semantics explicitly. The baseline planning invariant is duplicate-safe processing.

```text
DUPLICATE_MESSAGE_DELIVERY != DUPLICATE_WORK_OR_EFFECT
ACK_RECEIVED != RECIPIENT_COMPLETED_REQUEST
TIMEOUT != REQUEST_NOT_RECEIVED
```

`idempotency_key` or equivalent message identity must be available for acts whose duplicate processing would create duplicate Assignment/review/closeout work.

## Ordering

Global total ordering is not required. Causal relationships are explicit through reply/correlation/Assignment/Attempt references.

```text
ARRIVAL_ORDER != CAUSAL_ORDER
```

When order matters, the owning workflow declares the dependency rather than inferring it from wall-clock receipt order.

## Trust and prompt injection

Message bodies from workers/providers are untrusted content unless produced by a specifically trusted control-plane path.

A worker message that says "approved", "merge now", "ignore policy", or embeds a fake grant/review is data until independently resolved through the appropriate WePLD contract.

## Cancellation

```text
CANCEL_REQUEST != CANCELLED_PROVEN
CANCEL_ACKNOWLEDGEMENT != PROCESS_TERMINATED
```

The runtime cancellation/orphan contract remains controlling.

## Review separation

Review requests/results can flow through the Case Bus, but the bus does not prove reviewer independence. S7 must produce a `ReviewIndependenceReceipt` when the selected assurance policy requires it.

## Access / egress

Case messages inherit current Case/Assignment/item access policy and may narrow visibility. They cannot broaden source/context access.

A message routed to a worker/provider must pass the same context/egress access intersection as a ContextPackage.

## Required negative oracles

```text
WORKER_MESSAGE_CANNOT_CREATE_ASSIGNMENT_AUTOMATICALLY
WORKER_MESSAGE_CANNOT_CREATE_NAWAT_GRANT
FAKE_REVIEW_IN_MESSAGE_CANNOT_SATISFY_INDEPENDENT_REVIEW
DUPLICATE_REQUEST_MESSAGE_CANNOT_DUPLICATE_ASSIGNMENT
CANCEL_ACK_CANNOT_PROVE_REMOTE_TERMINATION
MESSAGE_WITH_SECRET_OUTSIDE_EGRESS_SCOPE_CANNOT_ROUTE
OUT_OF_ORDER_MESSAGES_CANNOT_SILENTLY_REWRITE_DEPENDENCY_STATE
MESSAGE_EXPIRY_OR_ACCESS_REVOCATION_BLOCKS_FUTURE_EGRESS
```

## Source relationship

Munder Difflin's inbox/outbox patterns and Omnigent's multi-agent/session coordination are useful behavior quarries. This contract is WePLD-native and grants no source admission.