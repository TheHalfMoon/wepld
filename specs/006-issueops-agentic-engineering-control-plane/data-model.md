# Data Model — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_MODEL
IMPLEMENTATION_AUTHORITY = NONE
STORAGE_REPRESENTATION = DEFERRED_TO_OWNING_SLICE
```

This document defines semantic entities and invariants only. It does not select a database, serialization library, remote service, vector store, or provider SDK.

## 1. Identity types

Every durable entity uses a WePLD-owned stable identifier. Provider identifiers remain typed external references.

```text
CaseId
ProviderBindingId
InputArtifactId
KnowledgeCollectionId
KnowledgeSourceId
RetrievalEvidenceId
WorkflowIntentId
WorkerId
AssignmentId
AttemptId
DecisionBoundaryId
FindingId
EffectProposalId
EffectResultId
CompletionEvidenceId
```

Opaque provider/session identifiers are stored as provenance, never promoted into WePLD identity.

## 2. Case

```text
Case {
  case_id
  title
  normalized_kind
  lifecycle_state
  autonomy_ceiling
  provider_bindings[]
  relations[]
  artifact_refs[]
  knowledge_refs[]
  decision_boundaries[]
  assignment_refs[]
  finding_refs[]
  completion_evidence_ref?
  created_event
  latest_derived_state_event
}
```

### Case invariants

- provider open/closed state does not directly set `lifecycle_state`;
- `COMPLETED_TRUSTED` requires a `CompletionEvidence` record;
- a Case may bind to multiple provider objects;
- all derived summary state is reconstructable from durable evidence/events;
- external object deletion or permission loss does not erase prior observations.

## 3. ProviderBinding

```text
ProviderBinding {
  binding_id
  case_id
  provider_kind
  provider_account_or_host_identity
  external_object_kind
  external_object_id
  canonical_external_locator
  last_observed_version
  last_observed_state
  last_observed_at
  read_capability_state
  write_capability_state
  provenance
}
```

Provider writes require fresh target/version observations according to the owning adapter contract.

## 4. CaseRelation

```text
CaseRelation {
  source_case_id
  relation_kind
  target_case_id
  evidence_refs[]
  confidence_class
  created_at
}
```

Planned relation kinds:

```text
EXACT_DUPLICATE_OF
PROBABLE_DUPLICATE_OF
COMMON_ROOT_CAUSE_WITH
REGRESSION_OF
BLOCKED_BY
DEPENDS_ON
SUPERSEDES
FIXED_BY
VERIFIED_BY
```

`PROBABLE_*` or confidence-bearing relations never silently become exact relations.

## 5. InputArtifact

```text
InputArtifact {
  artifact_id
  observed_source_kind
  observed_locator
  display_name?
  media_type_or_kind?
  size_observation?
  content_identity?
  path_or_uri_identity?
  trust_classification
  parser_qualification_state
  source_access_state
  created_at
  provenance
}
```

Creation is inert. The record carries no implicit parse, fetch, extraction, execution, repository mutation, or egress authority.

## 6. KnowledgeCollection

```text
KnowledgeCollection {
  collection_id
  name
  scope
  project_binding?
  members[]
  active_generation
  created_at
  updated_at
}
```

Scope candidates:

```text
SESSION
PROJECT
WORKSPACE
GLOBAL
```

Scope controls visibility/lifetime expectations, not effect authority.

## 7. KnowledgeSource

```text
KnowledgeSource {
  source_id
  collection_id
  artifact_or_external_source_ref
  source_kind
  source_identity
  ingest_generation
  parser_identity
  freshness_observation
  content_hash_or_equivalent?
  index_views[]
  provenance
}
```

Indexes are replaceable projections over source identity/provenance.

## 8. RetrievalEvidence

```text
RetrievalEvidence {
  retrieval_id
  collection_id
  query_or_intent_identity
  source_id
  source_generation
  exact_location_or_citation?
  freshness_state
  retrieval_signals[]
  rank_or_score_observations[]
  rerank_observations[]
  excerpt_identity?
  created_at
}
```

Scores are observations only. A missing required source generation or stale source state cannot be silently represented as current evidence.

## 9. WorkflowIntent

```text
WorkflowIntent {
  intent_id
  surface_command_or_origin
  normalized_capability
  target_refs[]
  requested_worker?
  requested_autonomy?
  user_constraints[]
  created_at
}
```

The intent is input to routing and authorization; it is not authority.

## 10. WorkerDescriptor

```text
WorkerDescriptor {
  worker_id
  adapter_kind
  provider_identity?
  model_identity?
  version_identity?
  capabilities[]
  supported_effect_classes[]
  containment_claims[]
  containment_evidence_refs[]
  session_semantics
  cost_class
  quota_class
  availability_state
  qualification_state
  qualification_evidence_refs[]
  qualification_expiry?
}
```

Provider flags such as `read-only`, `sandbox`, `yolo`, or `full trust` are recorded as provider claims until independently qualified.

## 11. Assignment

```text
Assignment {
  assignment_id
  case_id?
  task_identity
  objective
  acceptance_criteria[]
  dependency_assignment_ids[]
  context_package_refs[]
  required_capabilities[]
  proposed_effect_classes[]
  autonomy_ceiling
  created_at
}
```

## 12. Attempt

```text
Attempt {
  attempt_id
  assignment_id
  worker_id
  provider_session_identity?
  start_event
  terminal_event?
  result_refs[]
  effect_refs[]
  check_refs[]
  failure_or_cancel_reason?
}
```

Retry or reassignment creates a new Attempt. Prior attempts are immutable history.

## 13. DecisionBoundary

```text
DecisionBoundary {
  decision_id
  case_or_work_ref
  decision_kind
  question
  known_facts[]
  admissible_options[]
  recommendation?
  authority_required
  status
  resolution?
  resolution_evidence?
}
```

The system should not ask a human to rediscover facts that qualified agents can establish. Decision boundaries are for non-inferable choices or required approvals.

## 14. ReviewFinding

```text
ReviewFinding {
  finding_id
  reviewed_base_or_target
  reviewed_head_or_generation
  producer_identity
  finding_class
  severity
  claim
  evidence_refs[]
  reconciliation_state
  reconciliation_evidence?
}
```

Valid findings remain live until fixed, rebutted with evidence, or proven obsolete by a later exact candidate.

## 15. EffectProposal / EffectResult

```text
EffectProposal {
  effect_proposal_id
  effect_class
  exact_target
  proposed_input_identity
  complete_precondition_snapshot
  worker_or_work_origin
  created_at
}

EffectResult {
  effect_result_id
  effect_proposal_id
  nawat_decision_ref
  execution_identity
  observed_result
  postcondition_evidence
  created_at
}
```

External issue writes, Git operations, network fetches, process execution, parser expansion with side effects, and provider/model execution are distinct effect classes.

## 16. CompletionEvidence

```text
CompletionEvidence {
  completion_evidence_id
  case_or_work_ref
  accepted_target_identity
  deterministic_gate_refs[]
  independent_review_refs[]
  security_review_refs[]
  reconciliation_refs[]
  authority_refs[]
  provider_land_closeout_refs[]
  residual_limitations[]
  completion_decision
  created_at
}
```

A provider merge/close status is only one possible evidence input.

## 17. Event model

Prefer append-only events with deterministic derived state. Minimum event families are defined in `analyze.md`. Future storage design must support replay, interruption recovery, duplicate-event handling, and audit export before autonomous multi-case operation is qualified.
