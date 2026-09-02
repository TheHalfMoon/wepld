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

## 2. Mandatory separation

```text
User intent
  -> AssuranceIntent
  -> AssurancePlan
  -> engine qualification
  -> effect authorization when needed
  -> EngineRun
  -> EvidenceRef / Finding / CoverageClaim
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
  spec_target?
  task_target?
  graph_generation?
  rule_pack_identity?
  platform_runtime_identity?
}
```

When any field material to a claim changes, the evidence becomes `STALE` until requalified or explicitly reconciled.

## 4. `AssuranceIntent`

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

## 5. `AssurancePlan`

```text
AssurancePlan {
  plan_id
  intent_id
  target
  requested_claim
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

## 6. `EngineDescriptor`

```text
EngineDescriptor {
  engine_id
  engine_family
  exact_version_or_product_identity
  source_provenance?
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
  config_trust_model
  source_admission_state
  dependency_admission_state
  qualification_evidence[]
  limitations[]
}
```

Discovery of an executable or tool configuration MUST NOT automatically install, update, or execute it.

## 7. `EngineRun`

```text
EngineRun {
  run_id
  engine_descriptor_id
  assurance_target
  input_manifest
  config_identity
  rule_pack_identity?
  command_or_invocation_identity?
  environment_identity?
  authority_record?
  started_at
  finished_at
  result_class
  exit_identity?
  stdout_evidence?
  stderr_evidence?
  produced_evidence[]
  coverage_limitations[]
}
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
```

`ENGINE_ERROR`, `TIMEOUT`, `UNSUPPORTED`, and `INFRA_FAILURE` MUST NOT normalize to clean/no-findings.

## 8. `Finding`

```text
Finding {
  finding_id
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
  reconciliation_records[]
}
```

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

## 9. Reachability

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

## 10. `EvidenceRef`

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
  freshness_state
  coverage_limitations[]
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

## 11. `CoverageClaim`

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

Coverage dimensions are typed. A line-coverage value cannot satisfy rule coverage, dependency coverage, reviewer context coverage, platform coverage, reachability coverage, or mutation evidence.

## 12. Test outcome normalization

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

## 13. `Reproduction`

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

## 14. `FixProposal`

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

## 15. `Reverification`

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

## 16. `AssuranceBundle`

```text
AssuranceBundle {
  bundle_id
  target
  requested_claim
  plan_id
  engine_runs[]
  findings[]
  coverage_claims[]
  reproductions[]
  review_evidence[]
  security_evidence[]
  test_evidence[]
  unresolved_conflicts[]
  unresolved_coverage_gaps[]
  freshness_state
  created_at
}
```

An `AssuranceBundle` MAY be consumed by S8/S9/Case/Trusted Completion. It MUST NOT carry an implicit `PASS` unless the consuming gate defines an explicit claim and all required evidence for that claim is satisfied.

## 17. Freshness / staleness

Candidate states:

```text
FRESH_EXACT
FRESH_COMPATIBILITY_PROVEN
STALE_TARGET_CHANGED
STALE_ENGINE_CHANGED
STALE_RULES_CHANGED
STALE_GRAPH_CHANGED
STALE_ENVIRONMENT_CHANGED
STALE_EXTERNAL_STATE_CHANGED
UNKNOWN_FRESHNESS
```

Default acceptance-critical rule:

```text
NEW_EXACT_HEAD -> PRIOR_HEAD_ASSURANCE_STALE
```

A future compatibility proof may preserve evidence only when the owning gate defines and validates the exact equivalence relation; heuristic similarity is insufficient.

## 18. Cross-engine correlation

Correlation may group evidence by exact symbol/resource/path/dependency/test/change identity. It MUST preserve producer identities and contradictions.

```text
CORRELATED != DUPLICATED
MULTIPLE_FINDINGS_SAME_PATH != ONE_FINDING_WITHOUT_EVIDENCE
MAJORITY_CLEAN != VALIDATED_FINDING_FALSE
```

## 19. Configuration trust

Configuration sources MUST carry trust provenance:

```text
CANONICAL_POLICY
TRUSTED_REPOSITORY_CONFIG
SOURCE_BRANCH_PROPOSED_CONFIG
EXTERNAL_PROVIDER_CONFIG
USER_SESSION_OVERRIDE
```

A proposed/source-branch config may add or narrow advisory checks only where the owning policy permits. It cannot disable canonical authority/security/acceptance requirements for its own change.

## 20. Egress boundary

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

## 21. Dynamic security boundary

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

## 22. IDE boundary

IDE adapters may render plans, findings, evidence, test results, coverage, history, and stale state. IDE UI actions do not bypass the core contracts.

```text
IDE_CLICK_RUN != EXECUTION_AUTHORITY
IDE_QUICK_FIX != WRITE_AUTHORITY
IDE_SUPPRESS != ACCEPTED_RISK
IDE_TEST_GREEN != TRUSTED_COMPLETION
```

## 23. Error semantics

Assurance must fail explicitly when evidence is unavailable or incomplete.

Candidate error classes:

```text
TARGET_UNRESOLVED
TARGET_STALE
PLAN_INCOMPLETE
ENGINE_UNAVAILABLE
ENGINE_UNQUALIFIED
EFFECT_NOT_AUTHORIZED
UNSUPPORTED_LANGUAGE_OR_REGION
CONFIG_UNTRUSTED
PARSER_ERROR
ENGINE_ERROR
TIMEOUT
NETWORK_BLOCKED
CREDENTIAL_BLOCKED
EGRESS_BLOCKED
COVERAGE_GAP
CONFLICTING_EVIDENCE
INDEPENDENT_REVIEW_MISSING
```

No generic success state may hide one of these when it is material to the requested claim.
