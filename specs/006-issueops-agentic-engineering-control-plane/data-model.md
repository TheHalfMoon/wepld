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

Browser downloads enter this model through the single canonical `DownloadObservation` payload defined in [web-agent-boundary.md](contracts/web-agent-boundary.md), Browser artifact transfer / Download. Its exact browser context, origin, sealed staging identity/digest and handling-policy evidence reference this InputArtifact; this section does not redeclare a competing download schema.

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
  retrieval_basis = DirectSource | DerivedProjection
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

`retrieval_basis` is a closed discriminated union:

```text
DirectSource {
  kind = DIRECT_SOURCE
  exact_location_or_citation
  source_content_identity
}
DerivedProjection {
  kind = DERIVED_PROJECTION
  projection_generation
  exact_location_or_citation
  source_content_identity
  projection_content_identity
}
```

Every identity resolves to the exact bounded bytes/location used, with access and freshness inherited from the enclosing source generation. DirectSource prohibits projection fields; DerivedProjection requires all five fields. Unknown tags, mixed variants, absent/empty identities and an unresolved generation are invalid. Missing generation never selects a direct-read fallback. `excerpt_identity`, if present, identifies a further excerpt of this evidence, not a substitute for its required content identity.

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
  project_scope_ref
  workspace_scope_ref
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

Every included item's effective visibility is the intersection of source access, collection scope, project scope, workspace scope, assignment visibility, route/egress policy, and current revocation/redaction state. An explicitly qualified projectless/workspace-less scope is a recorded value, never an omitted check. Package construction and subsequent consumption must fail closed if that intersection cannot be established.

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

`WorkerRequirement` is a typed transient S5/S6 routing/qualification input, not a worker selection, persistent worker catalog or authority grant. Its `assignment_id` identifies the proposed Assignment; `required_capabilities` preserves that Assignment's `required_capabilities` and forms the corresponding member of `TopologyProposal.required_capability_sets`. Edara may add explicit constraints but cannot silently drop a required capability. A missing or contradictory mapping blocks route qualification. The same schema is used for synthetic S5 delegation dry-runs and the S6 handoff; no second dry-run requirement type exists.

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
  reservation_requirement = REQUIRED | NOT_REQUIRED
  reservation_determination_evidence_refs[]
  qualification_conditions[]
  qualification_evidence_refs[]
  qualified_at
  expires_at?
}
```

Qualification means the route may be considered. It never contains effect authority.

## 15. Assignment

### WorkSession and Mission ownership

```text
WorkSession {
  work_session_id
  project_scope_ref
  participant_access_policy_ref
  mission_refs[]
  timeline_cursor
  lifecycle_state
  created_at
}

Mission {
  mission_id
  work_session_ref
  controlling_intent_ref
  objective_revision
  control_revision
  control_state = ACTIVE | PAUSE_REQUESTED | PAUSED | CANCEL_REQUESTED | CANCEL_CONFIRMED | HANDOFF_PENDING | HANDOFF_COMPLETE
  acceptance_contract_ref
  assignment_refs[]
  runtime_state
  completion_decision_ref?
}
```

WorkSession is the durable user-work association under Mission Runtime with a UI projection; it has zero or more Missions. Each Mission belongs to one WorkSession and may have multiple Assignments and Attempts. A Case is an optional engineering concern linked to that work, not a prerequisite for generic work. Session lifecycle is `OPEN`, `ARCHIVED`, or `DELETION_PENDING`; archiving only changes presentation. Deletion follows evidence retention/access policy and cannot silently cancel or erase running work.

Mission runtime state is `PLANNED`, `READY`, `RUNNING`, `WAITING`, `RECOVERING`, or `TERMINAL`, with typed reason/effect evidence. Terminal execution is not successful completion: only a current Trusted Completion decision can establish the accepted outcome. An objective change creates a new objective revision, invalidates affected plans/acceptance evidence and requires renewed qualification/authority; it cannot rewrite prior attempts. Client reconnect uses an authorized timeline cursor; a client disconnect does not transfer execution ownership. Mission Runtime owns durable continuation, Edara owns assignment topology, and the UI owns neither.

```text
Assignment {
  assignment_id
  mission_ref
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

`ReviewFinding` is the review-facing projection of the canonical `Finding` in `contracts/assurance-fabric.md`. It retains that finding's identity, provenance, evidence and reconciliation history; it is not a second finding store or independent closure authority. The fields below describe the projection, not an alternative canonical lifecycle.

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
  logical_operation_id
  proposal_state = DRAFT | EXECUTABLE
  workflow_intent_ref?
  mission_ref?
  effect_class
  exact_target
  proposed_input_identity
  complete_precondition_snapshot
  controlling_origin_kind = WORKFLOW_INTENT | ASSIGNMENT | POLICY
  controlling_origin_ref
  assignment_ref?
  attempt_ref?
  proposing_principal_ref
  route_qualification_ref?
  credential_capability_refs[]?
  risk_evidence_refs[]?
  execution_envelope_ref?
  worker_or_work_origin
  created_at
}

NawatDecision {
  nawat_decision_id
  effect_proposal_id
  route_qualification_ref
  decision = ALLOW | DENY | APPROVAL_REQUIRED | TRANSFORM_TO_NARROWER_EFFECT | REQUALIFY_REQUIRED | STALE_TARGET | INSUFFICIENT_EVIDENCE
  grant_id?
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
  logical_operation_id
  dispatch_event_ref
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
  logical_operation_id
  visibility_or_consistency_proof_refs[]
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

The `?` fields above have conditional requiredness, not implicit execution defaults:

| Discriminator | Required bindings / validation |
|---|---|
| DRAFT | Execution bindings (`mission_ref`, `assignment_ref`, `attempt_ref`, `route_qualification_ref`, `execution_envelope_ref`, credential/risk lists) may be absent while unresolved. Identity, proposing principal, typed controlling origin and proposed effect/target/input remain explicit. Drafts cannot dispatch or obtain active credentials. |
| EXECUTABLE | Every execution binding listed above is required, nonempty where it is a reference, mutually consistent and current. Credential/risk lists must be present; empty lists require the qualified not-required evidence described below. Missing bindings are malformed executable proposals, never downgraded to drafts. |
| WORKFLOW_INTENT origin | `controlling_origin_ref` resolves to WorkflowIntent; `workflow_intent_ref` is required and equals it in either proposal state. |
| ASSIGNMENT origin | `controlling_origin_ref` resolves to Assignment; `assignment_ref` is required and equals it in either state. `workflow_intent_ref` may be absent; if supplied it must match that Assignment's originating intent. |
| POLICY origin | `controlling_origin_ref` resolves to the exact trusted controlling policy/version. `workflow_intent_ref` may be absent; if supplied, the derived intent must trace to that same policy authority and remain within its scope. Execution still requires normalized Mission/Assignment/Attempt and all other EXECUTABLE bindings. |

Origin conditions apply in addition to proposal-state conditions. Unknown discriminator values, wrong reference kinds and mismatched origin chains are rejected. Resolving a draft produces a successor proposal under the same logical operation only when intended operation/account/target/input are unchanged; changing them requires a new operation. No material binding change inherits a prior decision. Direct user work is normalized to Mission/Assignment/Attempt before execution, without requiring a Case. Empty credential/risk lists must carry a qualified not-required determination in the precondition snapshot; they cannot silently omit applicable checks. The snapshot binds exact account/tenant, target, argument digest, observations and their generations, applicable policy and authority scope. A changed material binding requires a new proposal and decision.

`retry_safety_state` is one of `NOT_RETRYABLE`, `RECONCILIATION_REQUIRED`, `SAFE_WITH_PROVIDER_IDEMPOTENCY`, `SAFE_AFTER_CONFIRMED_NO_EFFECT`, or `NO_RETRY_NEEDED`. Safety is evidence bound to the same logical operation, arguments, account, target and provider key retention window; it is not permission to execute. `STILL_UNKNOWN` requires reconciliation or a proven provider dedupe contract, never an ordinary blind retry. Conflicting or incomplete reconciliation remains unknown. Provider not-found results require the declared visibility bound/watermark or equivalent proof before establishing no effect.

One `logical_operation_id` survives delivery/transport retries of the same intended effect. Every dispatch has a distinct `execution_identity`. An intentional repeat creates a new operation only through fresh controlling intent and authority. Reusing an operation/provider key with changed arguments is a conflict. Provider key expiry, scope or route change invalidates any prior retry-safety conclusion.

`grant_id` is required and nonempty exactly when `decision = ALLOW`; it is prohibited otherwise. It identifies the granting outcome of this decision, not a second grant store. Approval-required and transform outcomes do not dispatch: approval evidence or a narrower proposal must return through Nawat. Every consumer uses this enum without adapter-specific aliases.

`AuthorityGrant` denotes the granting outcome of `NawatDecision`; `EffectReceipt` denotes the execution evidence in `EffectResult`. These are semantic aliases, not additional authority or evidence records.

### Dispatch and cancellation boundary

Mission Runtime durably records an ordinary RuntimeEvent with operation, execution, proposal, decision and fencing identities before releasing a consequential request to an enforcing effect adapter/broker. The dispatch record and state transition are one atomic local commit; if this cannot be established, dispatch is refused. This is not an atomic transaction with an arbitrary external provider. A crash after that commit and before receipt leaves a possibly sent effect, even if the request may never have left the host.

The enforcing adapter checks current qualification, authority, credential revocation and ownership at dispatch. A timeout, cancellation request, worker death or lost acknowledgement after possible send becomes `EFFECT_OUTCOME_UNKNOWN` until reconciled. Cancellation does not prove cessation. Irreversible dependent effects remain blocked while a prerequisite is unknown. Compensation is a separately proposed/authorized logical operation whose result cannot erase the original effect. Use existing events and effects; no separate dispatch ledger or receipt authority is introduced.

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

## 22. Project context projection

Fehrest/Maemar owns this projection over existing S2 Project identity, KnowledgeCollection/KnowledgeSource, retrieval and Evidence Graph records. It is not a new Project database or another source of truth.

```text
ProjectContextProjection {
  project_ref
  context_generation
  access_policy_ref
  entries[] = {
    source_ref
    source_kind = REPOSITORY | FILE | DIRECTORY | KNOWLEDGE_COLLECTION | INSTRUCTION
    exact_locator
    source_generation
    content_identity
    repository_revision_and_worktree_ref?
    provenance_evidence_refs[]
    freshness = CURRENT | STALE | UNKNOWN | REVOKED | HISTORICAL
    trust_class
    access_policy_ref
    instruction_provenance_and_precedence_ref?
  }
  work_session_refs[]
  automation_refs[]
  connection_binding_refs[]
  artifact_and_completion_evidence_refs[]
  observed_at
}
```

Repository entries require repository revision and exact worktree identity when applicable; files/directories resolve within the qualified roots and generation, never by an unchecked path string. Instruction entries require the instruction provenance/precedence reference. Context generation binds membership and revisions, not a mutable label. The projection exposes additions/removals, changed content and freshness since a selected prior generation. Inaccessible entries are filtered on every read; counts, titles, snippets and history cannot disclose revoked content. Associations never enlarge access or transfer authority.

User/project instructions express advisory preferences and task constraints. They cannot become canonical policy, override a higher-trust rule or mint WorkflowIntent/effect authority from retrieved text. Conflicting applicable instructions are surfaced with provenance; absent a defined canonical precedence, qualification stops for a material conflict. Revisions invalidate affected context and plan assumptions. Current canonical evidence prevails over stale/derived summaries, which retain their historical provenance.

Project import/export is an inert, versioned context manifest: stable source references, allowed provenance and qualified portable content only, with classification/access checks. Export excludes reusable credentials, live broker capabilities, cookies, grants and active runtime tokens. Import remaps references through S2 identity/Fehrest reconciliation and current access checks; unavailable sources remain unavailable and no work executes. Generalized non-repository/multi-root membership is deferred until S4's core context qualification; S2 identity is unchanged.

## 23. Work control payloads

WorkSession groups zero or more Missions; each Mission belongs to exactly one WorkSession. Moving a visible session between clients changes a projection subscription, not Mission identity or execution ownership. MissionRuntime owns control transitions using typed RuntimeEventEnvelope payloads, not another Work runtime.

```text
WorkControlRequest {
  runtime_event_ref
  request_id
  work_session_ref
  mission_ref
  requesting_principal_ref
  expected_objective_revision
  expected_control_revision
  action = PAUSE | RESUME | CANCEL | HANDOFF
  requested_target_route_ref?
  current_access_evidence_ref
}
```

Before accepting a WorkControlRequest or applying any Mission transition, MissionRuntime MUST validate the containing RuntimeEventEnvelope authenticity evidence under the distributed contract, including the requesting principal, namespace, exact payload, current access and applicable producer incarnation/ownership fence. Missing, forged, stale or mismatched proof produces no control transition; a UI-provided principal string or access-evidence reference alone is insufficient. Runtime persistence atomically deduplicates request_id within the tenant/Mission, compares the expected control revision, records the transition and increments that revision. Same key/different body conflicts; concurrent clients cannot both win incompatible transitions. Mission.control_state is orthogonal to its coarse runtime_state and references the control transition's RuntimeEvent evidence; neither can overwrite EffectResult. PAUSE_REQUESTED stops new dispatch, then PAUSED requires evidence that admitted activity reached a safe quiescent point. Unsupported pause is visible and must not pretend to freeze an external operation. RESUME requires refreshed context, qualification, leases and authority before returning to ACTIVE. CANCEL_REQUESTED stops new work and requests cessation; CANCEL_CONFIRMED requires proven cessation/cleanup, while already-sent external effects retain their separate result/reconciliation state. Terminal execution and uncertain business outcome can coexist.

HANDOFF requires a qualified target route, ownership fencing and reconciliation of in-flight operations before the successor dispatches. HANDOFF_PENDING blocks new dispatch on the relinquishing owner; HANDOFF_COMPLETE records successful ownership transfer, then a separately validated resume returns ACTIVE. Failure leaves the pending/blocked state with evidence rather than resurrecting the old owner. Host/worker/controller loss uses the distributed runtime recovery contract. A disconnected client does not terminate the Mission; an expired controller lease fences its effects. Cursor replay is access checked, bounded and read only; missing/compacted history produces an explicit gap with a safe snapshot reference.

Human approvals use DecisionBoundary, bound to the exact proposal/input/target/account/route, requested authority scope, current policy and expiry. An approval is evidence for Nawat's decision, not a grant created by the UI. Changed inputs, objective, account or stale target invalidate affected approvals. Work shows Server, Host, Runner, Worker, Attempt and provider/account distinctly when useful, using friendly labels. Results are claims; review, AMAN evidence, controlled repair and Trusted Completion remain separate timeline events. A repair creates fresh target-specific qualification and review obligations.
