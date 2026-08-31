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
ProviderObservationId
ProviderConflictId
InputArtifactId
KnowledgeCollectionId
KnowledgeSourceId
RetrievalEvidenceId
WorkflowIntentId
ContextPackageId
WorkerId
RouteQualificationId
AssignmentId
AttemptId
DecisionBoundaryId
FindingId
EffectProposalId
NawatDecisionId
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
  provider_conflict_refs[]
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
- external object deletion or permission loss does not erase prior observations;
- unresolved acceptance-critical provider conflicts prevent dependent writes/completion until abstained, resolved, or explicitly ruled irrelevant under the owning contract.

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
  adapter_contract_version
  normalization_contract_version
  observation_refs[]
  last_observed_version
  last_observed_state
  last_observed_at
  read_capability_state
  write_capability_state
  provenance
}
```

Provider writes require fresh target/version observations according to the owning adapter contract.

## 4. ProviderObservation / ProviderConflict

```text
ProviderObservation {
  provider_observation_id
  binding_id
  provider_version_or_etag?
  observed_state
  observed_relationships[]
  observed_at
  raw_or_hash_addressed_evidence_ref
  adapter_identity
  normalization_contract_version
}

ProviderConflict {
  provider_conflict_id
  case_id
  subject_semantic
  observation_refs[]
  conflict_kind
  resolution_state
  resolution_rule_or_decision_ref?
  first_detected_at
  latest_evaluated_at
}
```

Provider observations are append-only evidence. Latest-write-wins is not a generic Case-resolution rule. Contradictory observations remain inspectable after resolution.

## 5. CaseRelation

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
RELATED_TOPIC
REGRESSION_OF
BLOCKED_BY
DEPENDS_ON
SUPERSEDES
FIXED_BY
VERIFIED_BY
```

`PROBABLE_*` or confidence-bearing relations never silently become exact relations. Semantic/topic similarity is insufficient for causal relation promotion without stronger evidence.

## 6. InputArtifact

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
  instruction_eligibility
  parser_qualification_state
  source_access_state
  created_at
  provenance
}
```

Creation is inert. The record carries no implicit parse, fetch, extraction, execution, repository mutation, egress, or instruction authority. External/retrieved/repository content defaults to data-only instruction eligibility.

## 7. KnowledgeCollection

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

## 8. KnowledgeSource

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
  trust_classification
  provenance
}
```

Indexes are replaceable projections over source identity/provenance.

## 9. RetrievalEvidence

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
  trust_classification
  created_at
}
```

Scores are observations only. A missing required source generation or stale source state cannot be silently represented as current evidence. Retrieved instructions remain data and do not create WorkflowIntent.

## 10. WorkflowIntent

```text
WorkflowIntent {
  intent_id
  surface_command_or_origin
  normalized_capability
  target_refs[]
  requested_worker?
  requested_autonomy?
  user_constraints[]
  controlling_origin_class
  created_at
}
```

The intent is input to routing and authorization; it is not authority. `controlling_origin_class` must come from an allowed user/WePLD control path, not merely from untrusted source text.

## 11. ContextPackage

```text
ContextPackage {
  context_package_id
  assignment_id
  included_item_refs[]
  source_identity_by_item
  trust_class_by_item
  visibility_scope_by_item
  freshness_or_generation_by_item
  redaction_or_exclusion_evidence[]
  egress_class
  created_at
}
```

A package is evidence of what a worker may be shown. It does not authorize worker effects. Minimum-sufficient packaging is preferred over repository/collection dumping.

## 12. WorkerDescriptor

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

## 13. RouteQualification

```text
RouteQualification {
  route_qualification_id
  assignment_id
  worker_id
  adapter_identity
  matched_capabilities[]
  candidate_effect_classes[]
  containment_evidence_refs[]
  egress_class
  cost_class
  quota_state
  availability_observation
  qualification_conditions[]
  qualification_evidence_refs[]
  qualified_at
  expires_at?
}
```

Qualification means the route may be considered. It never contains effect authority.

## 14. Assignment

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

## 15. Attempt

```text
Attempt {
  attempt_id
  assignment_id
  worker_id
  route_qualification_ref
  provider_session_identity?
  context_package_ref
  start_event
  terminal_event?
  result_refs[]
  effect_refs[]
  check_refs[]
  failure_or_cancel_reason?
}
```

Retry or reassignment creates a new Attempt. Prior attempts are immutable history.

## 16. DecisionBoundary

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

## 17. ReviewFinding

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

## 18. EffectProposal / NawatDecision / EffectResult

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

NawatDecision {
  nawat_decision_id
  effect_proposal_id
  route_qualification_ref?
  decision
  exact_scope_or_target
  conditions[]
  containment_preconditions[]
  expires_or_revalidate_at?
  policy_and_evidence_refs[]
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

## 19. CompletionEvidence

```text
CompletionEvidence {
  completion_evidence_id
  case_or_work_ref
  accepted_target_identity
  reproduction_or_root_cause_refs[]
  change_or_implementation_refs[]
  deterministic_gate_refs[]
  independent_review_refs[]
  security_review_refs[]
  security_review_not_applicable_basis?
  reconciliation_refs[]
  authority_refs[]
  provider_land_closeout_refs[]
  residual_limitations[]
  completion_decision
  completion_decision_producer
  created_at
}
```

A provider merge/close status is only one possible evidence input.

### Completion verification rules

Before `COMPLETED_TRUSTED`:

1. every acceptance-critical evidence reference must bind to the exact accepted target/generation;
2. all required deterministic gates must be current and successful according to the owning acceptance contract;
3. independent review must be genuinely independent and bound to the accepted target;
4. security review must either exist or carry a policy-qualified not-applicable basis;
5. no material finding remains unresolved;
6. material effects must have matching authority/effect records and postcondition evidence;
7. stale/conflicting provider state relevant to acceptance must be resolved, explicitly abstained from, or proven irrelevant;
8. residual limitations must be stated rather than silently omitted;
9. merge/close/green-CI/model-review/provider state cannot itself set `completion_decision`.

## 20. Event model

Prefer append-only events with deterministic derived state. Minimum event families are defined in `analyze.md`. Future storage design must support replay, interruption recovery, duplicate-event handling, audit export, schema/version evolution, and bounded evidence growth before autonomous multi-case operation is qualified.

Event sourcing is not required for ephemeral UI/cache state that can be recomputed and is not acceptance/security/recovery evidence. The owning slice should persist only durable facts/transitions needed for replay, audit, authority, recovery, or product memory.
