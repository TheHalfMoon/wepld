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

Case messages are the IssueOps profile of the existing Mission Runtime coordination transport. Generic Work/Mission events and TriggerEnvelope payloads use that same transport with an explicit tenant/work namespace; they do not require creating an artificial Case. `CaseMessage.case_id` remains mandatory for the Case profile only. The enclosing RuntimeEventEnvelope supplies event identity, producer incarnation and causality; the message/payload never creates a second durable event log.

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
  payload_schema_version
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

`payload_schema_version` identifies the complete CaseMessage schema, including `message_act`, `body_or_summary`, references and their semantics. It is distinct from the enclosing RuntimeEventEnvelope's `policy_schema_version`. The runtime `payload_identity` covers the version and exact serialized payload. Producers/consumers negotiate supported versions before routing; unknown acts or required fields and incompatible versions are preserved as bounded opaque evidence and refused for semantic routing. Replay uses the recorded version, never the latest interpretation. A qualified migration emits a successor with original identity/provenance; it cannot rewrite history or replay an effect.

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

`trust_classification` is derived or validated at ingress from authenticated sender/producer identity, trusted Case/Assignment state and recorded message provenance. A producer-supplied label is an untrusted claim and cannot promote its own trust. Missing, mismatched or unverifiable provenance blocks semantic routing; retained diagnostic content is explicitly untrusted. Worker/provider bodies remain untrusted content even if their transport is authenticated or they claim to relay control-plane instructions. Only the separately resolved canonical control record can establish a controlling action.

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

Before routing, the bus resolves `access_policy_ref` and the typed `recipient_kind`/`recipient_ref` against current trusted Case, Assignment, recipient enrollment and referenced item state. It validates exact tenant/project/Case/Assignment membership, recipient identity/eligibility, current access/revocation and any narrower message constraints. Unknown, stale, mismatched, cross-scope or broader references are rejected before delivery; the producer cannot select a broader policy or a recipient by free text. A message routed to a worker/provider then passes the same context/egress access intersection as a ContextPackage. The intersection is an invariant; trusted reference resolution and checks at routing/replay are the enforcing boundary.

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
FORGED_TRUST_LABEL_CANNOT_PROMOTE_AUTHENTICATED_WORKER_TEXT
UNKNOWN_STALE_OR_BROADER_POLICY_AND_RECIPIENT_REFS_REFUSE_ROUTING
UNSUPPORTED_PAYLOAD_VERSION_OR_ACT_CANNOT_ROUTE_OR_REPLAY_AS_LATEST
```

## Source relationship

Munder Difflin's inbox/outbox patterns and Omnigent's multi-agent/session coordination are useful behavior quarries. This contract is WePLD-native and grants no source admission.
