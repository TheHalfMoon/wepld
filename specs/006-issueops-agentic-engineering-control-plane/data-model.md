# Data Model — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_MODEL
IMPLEMENTATION_AUTHORITY = NONE
STORAGE_REPRESENTATION = DEFERRED_TO_OWNING_SLICE
```

This document defines semantic entities and invariants only. It does not select a database, serialization library, remote service, vector store, or provider SDK.

For shared domain records, this file is the canonical field vocabulary unless a dedicated contract explicitly declares itself the canonical owner of that type. Other planning files should reference these shapes rather than create competing aliases.

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
WorkerRequirementId
WorkerId
RouteQualificationId
AssignmentId
AttemptId
DecisionBoundaryId
FindingId
EffectProposalId
NawatDecisionId
EffectResultId
EffectReconciliationId
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
- external object deletion or permission loss does not erase the observation identity, but protected content remains subject to current redaction/retention/access policy;
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
  observation_completeness
  observation_authenticity
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

Provider observations are append-only evidence. Latest-write-wins is not a generic Case-resolution rule. Contradictory observations remain inspectable after resolution. Partial or unauthenticated observations remain explicitly classified and cannot masquerade as complete current provider truth.

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
  access_policy_ref?
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
  access_policy_ref
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

Scope controls visibility/lifetime expectations, not effect authority. Collection membership does not override the narrower access policy of a member source.

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
  projection_generation_refs[]
  access_policy_ref
  trust_classification
  retention_or_tombstone_state
  provenance
}
```

Indexes/chunks/embeddings/graph views are replaceable projections over source identity/provenance. They inherit the source access policy and generation; derived projections may narrow visibility but may not widen it.

A refresh publishes one complete source generation atomically. Queries MUST NOT silently mix projections from two generations as one current source view.

## 9. RetrievalEvidence

```text
RetrievalEvidence {
  retrieval_id
  collection_id
  query_or_intent_identity
  source_id
  source_generation
  projection_generation?
  exact_location_or_citation?
  freshness_state
  retrieval_signals[]
  rank_or_score_observations[]
  rerank_observations[]
  excerpt_identity?
  access_policy_ref
  trust_classification
  created_at
}
```

Scores are observations only. A missing required source generation or stale source state cannot be silently represented as current evidence. Retrieved instructions remain data and do not create WorkflowIntent.

A source-access revocation, collection-visibility reduction, provider permission loss, or protected-content redaction invalidates downstream eligibility of affected derived projections and context packages even if their content hashes remain unchanged.

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
  access_policy_ref_by_item
  freshness_or_generation_by_item
  redaction_or_exclusion_evidence[]
  policy_snapshot_ref
  egress_class
  created_at
}
```

A package is evidence of what a worker may be shown. It does not authorize worker effects. Minimum-sufficient packaging is preferred over repository/collection dumping.

Every included item's effective visibility is the intersection of source access, collection scope, assignment visibility, route/egress policy, and current revocation/redaction state. Package construction must fail closed if that intersection cannot be established.

## 12. WorkerRequirement

```text
WorkerRequirement {
  worker_requirement_id
  assignment_id
  required_capabilities[]
  required_effect_classes[]
  prohibited_effect_classes[]
  required_containment_properties[]
  required_platform_runtime?
  egress_class
  maximum_cost_class?
  quota_constraints[]
  independence_requirement?
  session_requirements[]
  created_at
}
```

`WorkerRequirement` is a routing/qualification input, not a worker selection or authority grant.

## 13. WorkerDescriptor

```text
WorkerDescriptor {
  worker_id
  adapter_kind
  provider_identity?
  model_identity?
  version_identity?
  capability_vocabulary_version
  capabilities[]
  supported_effect_classes[]
  provider_permission_claims[]
  containment_claims[]
  containment_evidence_refs[]
  session_semantics
  cancellation_semantics
  recovery_semantics
  cost_class
  quota_class
  availability
  qualification_state
  qualification_evidence_refs[]
  qualification_expiry?
}
```

Provider flags such as `read-only`, `sandbox`, `yolo`, or `full trust` are recorded as provider claims until independently qualified.

Capabilities use a versioned WePLD vocabulary. Provider-native capability names are provenance/adapter inputs and cannot silently create new core effect classes.

## 14. RouteQualification

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

## 15. Assignment

```text
Assignment {
  assignment_id
  case_id?
  task_identity
  objective
  acceptance_criteria[]
  dependency_assignment_ids[]
  context_package_refs[]
  worker_requirement_refs[]
  required_capabilities[]
  proposed_effect_classes[]
  autonomy_ceiling
  created_at
}
```

## 16. Attempt

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
  recovery_state?
  failure_or_cancel_reason?
}
```

Retry or reassignment creates a new Attempt. Prior attempts are immutable history. Resuming an interrupted Attempt is permitted only when its owning runtime contract proves session/effect recovery semantics; otherwise create a new Attempt linked to the interrupted one.

## 17. DecisionBoundary

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

## 18. ReviewFinding

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

Valid findings remain live until fixed, rebutted with evidence, accepted under explicit authority/risk policy, or proven obsolete by a later exact candidate.

## 19. EffectProposal / NawatDecision / EffectResult / EffectReconciliation

```text
EffectProposal {
  effect_proposal_id
  effect_class
  exact_target
  proposed_input_identity
  complete_precondition_snapshot
  controlling_origin_kind
  controlling_origin_ref
  assignment_ref?
  attempt_ref?
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
  outcome_class
  observed_result?
  postcondition_evidence[]
  recovery_ref?
  created_at
}

EffectReconciliation {
  effect_reconciliation_id
  effect_proposal_id
  execution_identity
  unknown_outcome_evidence_refs[]
  reconciliation_observation_refs[]
  result
  retry_safety_state
  created_at
}
```

Canonical effect outcomes include:

```text
CONFIRMED_APPLIED
CONFIRMED_NOT_APPLIED
EFFECT_OUTCOME_UNKNOWN
FAILED_WITHOUT_EFFECT_PROVEN
CANCELLED_WITHOUT_EFFECT_PROVEN
```

Recovery result candidates include:

```text
CONFIRMED_APPLIED
CONFIRMED_NOT_APPLIED
STILL_UNKNOWN
```

External issue writes, Git operations, network fetches, process execution, parser expansion with side effects, browser submissions/uploads/downloads, and provider/model execution are distinct effect classes.

```text
LOCAL_TIMEOUT != REMOTE_EFFECT_NOT_APPLIED
UNKNOWN_EFFECT_OUTCOME != SAFE_TO_RETRY
```

## 20. CompletionEvidence

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
  effect_reconciliation_refs[]
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
7. no acceptance-critical material effect may remain `EFFECT_OUTCOME_UNKNOWN`;
8. stale/conflicting provider state relevant to acceptance must be resolved, explicitly abstained from, or proven irrelevant;
9. residual limitations must be stated rather than silently omitted;
10. merge/close/green-CI/model-review/provider state cannot itself set `completion_decision`.

## 21. Event model

Prefer append-only events plus deterministic derived state over opaque mutable workflow state. Minimum event families are defined in `analyze.md`. Future storage design must support replay, interruption recovery, duplicate-event handling, audit export, schema/version evolution, bounded evidence growth, redaction/tombstone semantics, backup/restore, and migration validation before autonomous multi-case operation is qualified.

Event sourcing is not required for ephemeral UI/cache state that can be recomputed and is not acceptance/security/recovery evidence. The owning slice should persist only durable facts/transitions needed for replay, audit, authority, recovery, or product memory.
