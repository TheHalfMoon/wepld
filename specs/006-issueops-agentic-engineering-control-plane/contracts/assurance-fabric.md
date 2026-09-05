# Contract — Native Assurance Fabric

```text
STATUS = FUTURE_PLANNING_CONTRACT
PRIMARY_OWNER = S7_ASSURANCE
SECURITY_EVIDENCE_OWNER = AMAN
PROJECT_GRAPH_CONTEXT_OWNER = FEHREST.MAEMAR
EFFECT_AUTHORITY = NAWAT_ONLY
REPAIR_AUTHORITY = S8_AUTHORIZED_ATTEMPT_ONLY
COMPLETION_AUTHORITY = TRUSTED_COMPLETION_ONLY
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
```

## 1. Purpose

This contract defines the semantic boundary shared by `/review`, `/security`, `/fulltest`, IDE assurance, Case assurance, and later Quality Passport evidence.

It does not select concrete engine implementations and grants no execution authority.

The fabric must answer an explicit assurance claim, not merely aggregate tool output.

## 2. Mandatory separation

```text
User intent
  -> AssuranceIntent
  -> AssurancePolicySnapshot
  -> AssurancePlan
  -> engine qualification
  -> effect authorization when needed
  -> EngineRun
  -> EvidenceRef / Finding / CoverageClaim
  -> ClaimAssessment
  -> AssuranceBundle
  -> consumer (human, Case, S8, S9, Trusted Completion)
```

No arrow implies authority inheritance.

```text
ASSURANCE_INTENT != EXECUTION_AUTHORITY
ASSURANCE_PLAN != EXECUTION_AUTHORITY
ENGINE_QUALIFIED != NAWAT_GRANTED
ENGINE_RUN_SUCCESS != NO_FINDINGS
NO_FINDINGS != ASSURANCE_COMPLETE
CLAIM_SUPPORTED != COMPLETION_DECISION
ASSURANCE_BUNDLE != COMPLETION_DECISION
```

## 3. `AssuranceTarget`

An acceptance-critical assurance artifact MUST bind an exact immutable target identity sufficient for its claim.

Candidate minimum:

```text
AssuranceTarget {
  project_id
  repository_identity?
  workspace_generation
  base_revision?
  head_revision?
  tree_identity?
  change_set_identity?
  workspace_material_manifest_identity?
  untracked_material_identity?
  ignored_material_policy_identity?
  submodule_or_nested_repo_state_identity?
  generated_artifact_policy_identity?
  spec_target?
  task_target?
  graph_generation?
  rule_pack_identity?
  platform_runtime_identity?
}
```

For a clean committed target, some workspace-material fields may be not applicable. For workspace assurance, the target identity must account for material uncommitted/untracked/nested/generated state according to the owning target policy; a Git commit SHA alone is not enough.

When any field material to a claim changes, the evidence becomes `STALE` until requalified or explicitly reconciled.

## 4. `AssurancePolicySnapshot`

The meaning of an assurance claim is versioned and immutable for historical evidence.

```text
AssurancePolicySnapshot {
  policy_snapshot_id
  profile_policy_id
  profile_policy_version
  requested_claim_schema_version
  canonical_policy_refs[]
  rule_pack_identity
  required_evidence_classes[]
  conditional_evidence_rules[]
  optional_evidence_classes[]
  allowed_effect_classes[]
  staleness_rules
  conflict_rules
  finding_disposition_rules
  benchmark_threshold_refs[]
  created_at
}
```

```text
PROFILE_NAME != STABLE_POLICY_MEANING
POLICY_CHANGED -> OLD_CLAIM_ASSESSMENT_REMAINS_HISTORICAL
```

Historical AssuranceBundles retain the exact policy snapshot under which their claim was assessed.

## 5. `AssuranceIntent`

```text
AssuranceIntent {
  intent_id
  command_surface
  target
  requested_claim
  profile
  scope
  explicit_includes[]
  explicit_excludes[]
  maximum_effect_class
  budget
  user_policy_constraints
}
```

Valid `command_surface` candidates include:

```text
REVIEW
SECURITY
FULLTEST
INTERNAL_ASSURANCE_WORKFLOW
```

## 6. `AssurancePlan` and check requirement semantics

```text
AssurancePlan {
  plan_id
  intent_id
  target
  requested_claim
  assurance_policy_snapshot_ref
  selected_checks[]
  selected_engines[]
  context_manifest
  required_effects[]
  qualification_requirements[]
  execution_budget
  expected_evidence_types[]
  omitted_checks[]
  staleness_policy
  planner_evidence
}
```

Each selected or omitted check is classified:

```text
CHECK_REQUIREMENT = REQUIRED | CONDITIONAL | OPTIONAL
```

Every `omitted_check` MUST include an explicit reason:

```text
NOT_APPLICABLE
NOT_QUALIFIED
NOT_AUTHORIZED
NOT_AVAILABLE
BUDGET_EXCEEDED
UNSUPPORTED_TARGET
INSUFFICIENT_EVIDENCE_TO_SELECT
SUPERSEDED_BY_STRONGER_EXACT_CHECK
```

Silently omitting a required check is prohibited.

```text
REQUIRED_CHECK_OMITTED -> CLAIM_ASSESSMENT != SUPPORTED
BUDGET_EXCEEDED != PERMISSION_TO_DOWNGRADE_REQUIRED_EVIDENCE
NOT_AUTHORIZED_REQUIRED_CHECK -> CLAIM_BLOCKED_OR_INCONCLUSIVE
```

Profile/claim strengthening is monotonic for the same target/risk class unless an explicit compatibility/substitution rule in the policy snapshot proves that a different evidence set is at least as strong for the requested claim.

## 7. `EngineDescriptor`

```text
EngineDescriptor {
  engine_id
  engine_family
  exact_version_or_product_identity
  source_provenance?
  expected_artifact_or_binary_identity?
  capabilities[]
  supported_languages_ecosystems[]
  input_formats[]
  output_formats[]
  process_effects[]
  filesystem_effects[]
  network_effects[]
  browser_effects[]
  credential_requirements[]
  containment_requirements[]
  resource_requirements[]
  config_trust_model
  source_admission_state
  dependency_admission_state
  qualification_evidence[]
  limitations[]
}
```

Discovery of an executable or tool configuration MUST NOT automatically install, update, or execute it.

## 8. `EngineRun`

```text
EngineRun {
  run_id
  engine_descriptor_id
  assurance_target
  resolved_executable_or_runtime_identity?
  executable_or_artifact_digest?
  engine_database_identity?
  rule_pack_or_template_snapshot_identity?
  input_manifest
  config_identity
  command_or_invocation_identity?
  environment_identity?
  authority_record?
  resource_envelope
  started_at
  finished_at
  result_class
  exit_identity?
  stdout_evidence?
  stderr_evidence?
  produced_evidence[]
  cleanup_evidence[]
  coverage_limitations[]
}
```

The resource envelope may include, where applicable:

```text
wall_clock_timeout
cpu_limit
memory_limit
process_count_limit
file_descriptor_or_handle_limit
output_limit
temporary_disk_limit
network_limit
concurrency_slot
process_tree_termination_policy
temporary_artifact_cleanup_policy
inherited_environment_policy
credential_exposure_policy
```

`result_class` candidates:

```text
COMPLETED
FAILED_CHECKS
ENGINE_ERROR
TIMEOUT
CANCELLED
NOT_AUTHORIZED
NOT_QUALIFIED
UNSUPPORTED
INFRA_FAILURE
RESOURCE_LIMIT
CLEANUP_INCOMPLETE
```

`ENGINE_ERROR`, `TIMEOUT`, `UNSUPPORTED`, `INFRA_FAILURE`, `RESOURCE_LIMIT`, or material `CLEANUP_INCOMPLETE` MUST NOT normalize to clean/no-findings.

```text
VERSION_STRING_MATCH != EXECUTABLE_IDENTITY_MATCH
PATH_ENTRY_FOUND != QUALIFIED_ENGINE_IDENTITY
```

## 9. `Finding`, fingerprint, correlation, and disposition

```text
Finding {
  finding_id
  finding_fingerprint
  finding_kind
  severity
  validation_state
  confidence?
  title
  description
  rule_or_check_identity?
  primary_location
  related_locations[]
  code_resource_flow[]
  reachability_state?
  producer_run_ids[]
  evidence_refs[]
  reproduction_ids[]
  first_seen_target
  last_verified_target
  status
  disposition_ref?
  correlation_refs[]
  reconciliation_records[]
}
```

`finding_fingerprint` is a stable evidence-backed identity over the smallest semantics sufficient to correlate recurrence without assuming that same-line/same-message means same defect.

Candidate correlation relations:

```text
SAME_FINDING_REOBSERVED
DUPLICATE_SIGNAL
SAME_ROOT_CAUSE_CANDIDATE
RELATED_FINDING
SUPERSEDES_FINDING
REGRESSION_OF_FINDING
```

Correlation never deletes producer-specific evidence.

`validation_state` candidates:

```text
UNVALIDATED_CANDIDATE
VALIDATED
DISPROVEN
INCONCLUSIVE
```

`status` candidates:

```text
OPEN
REQUIRES_MORE_EVIDENCE
REJECTED_FALSE_POSITIVE
REPAIRED_PENDING_REVERIFY
VERIFIED_FIXED
ACCEPTED_RISK
SUPERSEDED
```

A validated finding is finding-specific evidence. Clean output from another reviewer/engine cannot erase it without reconciliation evidence addressing that finding.

### `FindingDisposition`

```text
FindingDisposition {
  disposition_id
  finding_id
  disposition_kind
  target_scope
  reason
  authority_or_decision_ref
  policy_snapshot_ref
  created_at
  expires_at_or_review_at?
  evidence_refs[]
}
```

Disposition candidates include:

```text
FALSE_POSITIVE
ACCEPTED_RISK
TEMPORARY_SUPPRESSION
RULE_EXCEPTION
VERIFIED_FIXED
SUPERSEDED
```

Untrusted repository content cannot forge or extend a disposition. Expired accepted-risk/suppression evidence becomes stale and cannot silently suppress a current finding.

## 10. Reachability

Candidate values:

```text
REACHABLE
UNREACHABLE_PROVEN
CONDITIONALLY_REACHABLE
UNKNOWN_DYNAMIC
UNKNOWN_UNSUPPORTED
NOT_APPLICABLE
```

Unknown is not unreachable.

Reachability evidence MUST state the graph/index/runtime assumptions and generation used.

## 11. `EvidenceRef` and handling policy

```text
EvidenceRef {
  evidence_id
  evidence_kind
  producer_identity
  target_identity
  source_location_or_artifact
  content_identity
  generation?
  observed_at
  trust_classification
  content_classification
  access_policy_ref
  handling_policy_ref
  redaction_state
  retention_state
  freshness_state
  coverage_limitations[]
}
```

`handling_policy_ref` resolves an `EvidenceHandlingPolicy` appropriate to the evidence class:

```text
EvidenceHandlingPolicy {
  handling_policy_id
  visibility_scope
  encryption_or_storage_requirement
  redaction_rules
  retention_or_expiry
  export_policy
  external_egress_class
  deletion_or_tombstone_policy
  sensitive_rendering_policy
}
```

Possible evidence kinds include:

```text
DIAGNOSTIC
SARIF
TEST_RESULT
JUNIT
COVERAGE
MUTATION
FUZZ_COUNTEREXAMPLE
MODEL_CHECK_PROOF
MODEL_CHECK_COUNTEREXAMPLE
SBOM
OSV_RECORD
DEPENDENCY_INVENTORY
CALL_PATH
TAINT_PATH
RESOURCE_PATH
BROWSER_TRACE
SCREENSHOT
NETWORK_TRACE
PERFORMANCE_RESULT
REVIEW_COMMENT
REVIEW_OUTCOME
REPRODUCTION
THREAT_MODEL
```

Raw evidence may contain secrets, source excerpts, browser session data, request/response data, file paths, or private content. Durable storage/export must follow current handling/access policy; evidence identity is preserved even when content is redacted or tombstoned.

## 12. `CoverageClaim`

```text
CoverageClaim {
  claim_id
  target
  dimension
  covered_set_or_measure
  uncovered_set_or_measure
  unsupported_set
  exclusions[]
  producer_runs[]
  freshness_state
}
```

Coverage dimensions are typed. A line-coverage value cannot satisfy rule coverage, dependency coverage, reviewer context coverage, platform coverage, reachability coverage, mutation evidence, or reviewer scope coverage.

A review can therefore produce an explicit `REVIEW_CONTEXT_COVERAGE` claim rather than a prose-only statement that it examined enough of the codebase.

## 13. Test outcome and flake normalization

```text
FIRST_PASS
CONSISTENT_FAIL
RETRY_PASS_FLAKY
RETRY_FAIL
TIMEOUT
INFRA_FAILURE
CANCELLED
NOT_RUN
UNSUPPORTED
```

```text
RETRY_PASS_FLAKY != FIRST_PASS
RETRY_PASS_FLAKY != CLEAN_PASS
INFRA_FAILURE != TEST_PASS
NOT_RUN != TEST_PASS
```

Known-flake/quarantine policy is explicit:

```text
FlakeDisposition {
  test_identity
  owner
  evidence_refs[]
  scope
  created_at
  expires_or_review_at
  required_follow_up
}
```

Quarantine may change scheduling or claim policy where explicitly allowed; it cannot erase the failure observation or become permanent without review.

## 14. `PerformanceEvidence`

A performance regression claim is not based on one noisy wall-clock observation.

```text
PerformanceEvidence {
  performance_evidence_id
  target
  benchmark_identity
  baseline_target
  hardware_runtime_identity
  dataset_or_fixture_identity
  warmup_policy
  repetition_policy
  sample_summary
  variance_or_noise_summary
  threshold_or_budget
  statistical_or_deterministic_decision_rule
  result
  evidence_refs[]
}
```

Candidate results:

```text
NO_REGRESSION_DETECTED
REGRESSION_DETECTED
IMPROVEMENT_DETECTED
INCONCLUSIVE_NOISE
INSUFFICIENT_SAMPLES
ENVIRONMENT_MISMATCH
```

## 15. `Reproduction`

```text
Reproduction {
  reproduction_id
  target
  finding_or_check_id
  exact_inputs
  environment_identity
  invocation_identity
  authority_record?
  expected_observation
  actual_observation
  repeatability
  minimization_state
  evidence_refs[]
}
```

## 16. `FixProposal`

```text
FixProposal {
  proposal_id
  target
  finding_ids[]
  proposed_change_scope
  rationale
  predicted_required_tests[]
  predicted_risks[]
  evidence_refs[]
  WRITE_AUTHORITY = NONE
}
```

S8 may transform a proposal into a separately authorized Attempt. Assurance cannot do so by itself.

## 17. `Reverification`

```text
Reverification {
  prior_finding_id
  prior_target
  new_target
  selected_checks[]
  result
  evidence_refs[]
}
```

Result candidates:

```text
VERIFIED_FIXED
STILL_PRESENT
CHANGED_FINDING
INCONCLUSIVE
NOT_REPRODUCIBLE_DUE_TO_ENVIRONMENT_GAP
```

## 18. `ClaimAssessment`

Every AssuranceBundle that answers a user/acceptance/release question includes an explicit assessment.

```text
ClaimAssessment {
  claim_assessment_id
  target
  requested_claim
  assurance_policy_snapshot_ref
  outcome
  required_evidence_classes[]
  satisfied_evidence_refs[]
  missing_required_evidence[]
  blocking_findings[]
  unresolved_conflicts[]
  unresolved_coverage_gaps[]
  stale_evidence_refs[]
  residual_limitations[]
  rationale
  assessed_at
}
```

Outcome candidates:

```text
SUPPORTED
NOT_SUPPORTED
PARTIALLY_SUPPORTED
INCONCLUSIVE
BLOCKED
STALE
```

Rules:

```text
MISSING_REQUIRED_EVIDENCE -> outcome != SUPPORTED
STALE_REQUIRED_EVIDENCE -> outcome != SUPPORTED
UNRESOLVED_BLOCKING_FINDING -> outcome != SUPPORTED
MATERIAL_CONFLICT -> SUPPORTED only if policy defines and evidence satisfies an explicit resolution rule
BUDGET_EXCEEDED_REQUIRED_CHECK -> BLOCKED | INCONCLUSIVE
ENGINE_UNAVAILABLE_REQUIRED_CHECK -> BLOCKED | INCONCLUSIVE
```

`SUPPORTED` means the exact requested assurance claim is currently supported under the exact policy snapshot. It is still not Trusted Completion.

## 19. `AssuranceBundle`

```text
AssuranceBundle {
  bundle_id
  target
  requested_claim
  assurance_policy_snapshot_ref
  plan_id
  engine_runs[]
  findings[]
  coverage_claims[]
  reproductions[]
  performance_evidence[]
  review_evidence[]
  security_evidence[]
  test_evidence[]
  claim_assessment_ref
  unresolved_conflicts[]
  unresolved_coverage_gaps[]
  freshness_state
  created_at
}
```

An `AssuranceBundle` MAY be consumed by S8/S9/Case/Trusted Completion. It MUST NOT carry an implicit generic `PASS`; the typed `ClaimAssessment` is the only assurance-level answer to the requested claim.

## 20. Freshness / staleness

Candidate states:

```text
FRESH_EXACT
FRESH_COMPATIBILITY_PROVEN
STALE_TARGET_CHANGED
STALE_ENGINE_CHANGED
STALE_RULES_CHANGED
STALE_POLICY_CHANGED
STALE_GRAPH_CHANGED
STALE_ENVIRONMENT_CHANGED
STALE_EXTERNAL_STATE_CHANGED
STALE_ACCESS_OR_HANDLING_POLICY_CHANGED
UNKNOWN_FRESHNESS
```

Default acceptance-critical rule:

```text
NEW_EXACT_HEAD -> PRIOR_HEAD_ASSURANCE_STALE
```

A future compatibility proof may preserve evidence only when the owning gate defines and validates the exact equivalence relation; heuristic similarity is insufficient.

## 21. Cross-engine correlation

Correlation may group evidence by exact fingerprint/symbol/resource/path/dependency/test/change identity. It MUST preserve producer identities and contradictions.

```text
CORRELATED != DUPLICATED
MULTIPLE_FINDINGS_SAME_PATH != ONE_FINDING_WITHOUT_EVIDENCE
MAJORITY_CLEAN != VALIDATED_FINDING_FALSE
```

## 22. Configuration trust and precedence

Configuration sources carry trust provenance and deterministic precedence:

```text
CANONICAL_POLICY
TRUSTED_REPOSITORY_CONFIG
COMPONENT_OR_SPEC_CONFIG
SOURCE_BRANCH_PROPOSED_CONFIG
EXTERNAL_PROVIDER_CONFIG
USER_SESSION_OVERRIDE
```

The owning policy snapshot defines which lower layer may specialize which field. A lower-precedence source may narrow optional behavior only where permitted and cannot weaken canonical authority/security/acceptance/evidence requirements.

Conflicting configuration without a defined precedence/merge rule produces `CONFIG_CONFLICT` / `PLAN_INCOMPLETE`; it is not resolved by last-write-wins.

A proposed/source-branch config may add advisory checks only where policy permits. It cannot disable canonical authority/security/acceptance requirements for its own change.

## 23. Egress boundary

Hosted engines/reviewers/models are governed by `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`.

The plan/run record must preserve:

```text
provider/product identity
exact egressed file/artifact scope
content classification
screening evidence
redactions
approval
base/head or immutable target
result coverage limitations
```

External output is untrusted evidence and must be normalized like any other engine output.

## 24. Dynamic security boundary

A dynamic scanner/API/browser engine descriptor MUST expose target/network/credential/template/code-execution effects before qualification.

Required future run envelope includes:

```text
authorized target set
origin/host/port/protocol bounds
method/action bounds
credential identity + least privilege
rate/concurrency/request/time budget
template/plugin identity
sandbox/containment
forbidden targets
stop conditions
secret/private-data handling
```

## 25. IDE boundary

IDE adapters may render plans, claim assessments, findings, evidence, test results, coverage, history, and stale state. IDE UI actions do not bypass the core contracts.

```text
IDE_CLICK_RUN != EXECUTION_AUTHORITY
IDE_QUICK_FIX != WRITE_AUTHORITY
IDE_SUPPRESS != ACCEPTED_RISK
IDE_TEST_GREEN != TRUSTED_COMPLETION
GENERIC_GREEN_ICON != CLAIM_ASSESSMENT
```

## 26. Error semantics

Assurance must fail explicitly when evidence is unavailable or incomplete.

Candidate error classes:

```text
TARGET_UNRESOLVED
TARGET_STALE
PLAN_INCOMPLETE
POLICY_SNAPSHOT_UNRESOLVED
CONFIG_CONFLICT
ENGINE_UNAVAILABLE
ENGINE_UNQUALIFIED
ENGINE_IDENTITY_MISMATCH
EFFECT_NOT_AUTHORIZED
UNSUPPORTED_LANGUAGE_OR_REGION
CONFIG_UNTRUSTED
PARSER_ERROR
ENGINE_ERROR
TIMEOUT
RESOURCE_LIMIT
CLEANUP_INCOMPLETE
NETWORK_BLOCKED
CREDENTIAL_BLOCKED
EGRESS_BLOCKED
ACCESS_POLICY_BLOCKED
COVERAGE_GAP
CONFLICTING_EVIDENCE
INDEPENDENT_REVIEW_MISSING
REQUIRED_EVIDENCE_MISSING
```

No generic success state may hide one of these when it is material to the requested claim.
