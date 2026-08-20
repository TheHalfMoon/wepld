# WePLD Harness Program — H0 Evidence and Runner Contract

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / EXECUTION-EVIDENCE CONTRACT
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
RUNTIME_ADOPTION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## 1. Purpose

This document defines the minimum WePLD-owned execution/evidence boundary required to run the H0 Harness Thesis Tournament without allowing an external evaluation framework, model, harness, or reviewer to become completion authority.

The governing quantitative decision contract is:

`docs/acquisition/WEPLD_HARNESS_H0_THESIS_TOURNAMENT_CONTRACT_2026-08-20.md`

The initial evaluation-donor reconnaissance is:

`docs/acquisition/WEPLD_HARNESS_H0_EVALUATION_DONOR_RECONNAISSANCE_2026-08-20.md`

This document does not select Harbor or any other runner.

```text
HARBOR_NEEDED = UNDECIDED
RUNNER_IMPLEMENTATION = NOT_AUTHORIZED
H0_EXPERIMENT_EXECUTION = NOT_STARTED
```

## 2. Core architectural rule

The execution runner is a replaceable data-plane mechanism.

The WePLD evidence/control contract owns experiment identity, authority boundaries, verifier identity, trial finalization semantics, and promotion analysis.

```text
                   WEPLD H0 CONTROL PLANE
                             |
          frozen content-addressed manifests
                             |
                    Runner Adapter API
                             |
                  REPLACEABLE RUNNER
                             |
           process/container/tool execution
                             |
                    raw result material
                             |
                   WEPLD EVIDENCE PLANE
                             |
          objective verifier + hard-gate logic
                             |
                    FINAL TRIAL RECORD
                             |
                    PAIRED ANALYSIS
```

The runner may execute. It may not decide whether H0 passed.

## 3. Trust boundary

```text
RUNNER_CAN_EXECUTE = YES
RUNNER_CAN_EMIT_RAW_OBSERVATIONS = YES
RUNNER_CAN_EMIT_USAGE_OBSERVATIONS = YES
RUNNER_CAN_CAPTURE_ARTIFACTS = YES

RUNNER_CAN_DECLARE_VERIFIED_SUCCESS = NO
RUNNER_CAN_CHANGE_EFFECT_AUTHORITY = NO
RUNNER_CAN_CHANGE_BUDGET = NO
RUNNER_CAN_CHANGE_TASK = NO
RUNNER_CAN_CHANGE_VERIFIER = NO
RUNNER_CAN_DROP_UNFAVORABLE_RUNS = NO
RUNNER_CAN_PROMOTE_HARNESS = NO
RUNNER_CAN_AUTHOR_H0_DECISION = NO
```

A model or harness has strictly less decision authority than the runner.

## 4. Content-addressed identity rule

Decision-relevant inputs must be bound to immutable identities before execution.

Preferred identity function:

```text
identity = sha256(canonical_bytes)
```

Canonical serialization rules must be frozen before execution. Mutable labels such as `latest`, branch names, provider marketing model aliases, or container tags are insufficient by themselves.

Where the upstream system cannot expose an immutable digest/revision, record that limitation explicitly and add all observable provider/runtime identity fields.

## 5. ExperimentManifest

Minimum research schema:

```text
ExperimentManifest
- contract_version
- experiment_id
- created_at
- screening_or_confirmatory
- arm_definitions
- task_manifest_set_hash
- model_manifest_set_hash
- recipe_manifest_set_hash
- environment_manifest_set_hash
- verifier_manifest_set_hash
- budget_policy_hash
- retry_policy_hash
- failure_taxonomy_version
- statistical_plan_version
- authority_policy_hash
- egress_policy_hash
- expected_run_count
- manifest_hash
```

The confirmatory `ExperimentManifest` is frozen before the first confirmatory outcome is observed.

## 6. TaskManifest

```text
TaskManifest
- task_id
- task_archetype
- source_identity
- source_revision
- prompt_hash
- fixture_tree_hash
- setup_hash
- expected_mutation_surface
- objective_verifier_id
- objective_verifier_hash
- allowed_effect_envelope_hash
- timeout_budget
- token_budget
- money_budget_if_available
- eligibility_notes
- manifest_hash
```

Task text, fixtures, setup, and verifier are one identity-bearing unit.

A task cannot silently change between arms.

## 7. ModelManifest

```text
ModelManifest
- model_id
- model_family
- provider_or_serving_stack
- provider_route
- provider_revision_if_exposed
- context_limit_used
- temperature
- top_p
- max_output_tokens
- seed_if_supported
- reasoning_or_effort_setting
- tool_call_mode
- structured_output_mode
- system_instruction_hash
- provider_feature_flags
- credential_reference_id
- manifest_hash
```

`credential_reference_id` identifies a separately controlled secret source. Secret material must never be embedded in the manifest or research artifact.

## 8. RecipeManifest

```text
RecipeManifest
- recipe_id
- arm
- recipe_version
- provenance
- system_prompt_hash
- context_policy_hash
- tool_surface_hash
- planning_policy_hash
- memory_policy_hash
- delegation_policy_hash
- recovery_policy_hash
- verifier_cadence_policy_hash
- stop_policy_hash
- effect_envelope_hash
- resource_budget_hash
- model_adaptive_routing_enabled
- task_environment_compilation_enabled
- known_limitations
- manifest_hash
```

For D, the routing policy itself receives an immutable identity.

The selected recipe for each D trial must be recorded before the model begins task execution.

## 9. EnvironmentManifest

```text
EnvironmentManifest
- environment_id
- os
- architecture
- container_engine_or_runtime
- image_reference
- image_digest
- fixture_mount_policy
- writable_paths
- process_policy
- network_policy
- DNS_policy_if_relevant
- clock_policy_if_relevant
- CPU_budget
- memory_budget
- filesystem_limits
- environment_variable_name_set
- secret_reference_name_set
- setup_hash
- manifest_hash
```

Mutable image tags without an immutable image digest are insufficient for confirmatory evidence.

## 10. VerifierManifest

```text
VerifierManifest
- verifier_id
- task_id
- verifier_type
- executable_or_script_hash
- runtime_identity
- inputs
- expected_outputs
- pass_semantics
- fail_semantics
- timeout
- network_policy
- authority_requirements
- nondeterminism_notes
- manifest_hash
```

The final verifier must not depend on the candidate harness's own declaration of success.

## 11. BudgetPolicy

Budget rules are experiment inputs, not runner suggestions.

```text
BudgetPolicy
- wall_time_limit
- model_turn_limit
- input_token_limit_if_enforceable
- output_token_limit_if_enforceable
- money_limit_if_enforceable
- process_count_limit
- concurrent_subagent_limit
- external_request_limit
- external_egress_policy
- disk_limit_if_enforceable
```

If a provider cannot enforce a budget dimension prospectively, record observed usage and classify the enforcement limitation.

## 12. EffectEnvelope

Every trial binds an effect envelope before execution.

```text
EffectEnvelope
- readable_paths
- writable_paths
- executable_process_classes
- network_mode
- allowed_hosts_if_any
- allowed_protocols_if_any
- credential_classes
- external_service_classes
- irreversible_effects
- merge_deploy_publish_authority
- human_approval_requirements
- envelope_hash
```

H0 should prefer reversible, container-local task effects.

```text
DEFAULT_NETWORK_MODE = DENY_EXCEPT_MODEL_PROVIDER_WHEN_REQUIRED
DEFAULT_EXTERNAL_SIDE_EFFECTS = NONE
DEFAULT_MERGE_DEPLOY_PUBLISH = DENY
```

If provider API access is external, that model-serving egress is accounted separately from task-environment egress.

## 13. TrialIdentity

A trial ID must bind the entire comparison cell:

```text
TrialIdentity = sha256(
  experiment_manifest_hash
  + task_manifest_hash
  + model_manifest_hash
  + recipe_manifest_hash
  + environment_manifest_hash
  + verifier_manifest_hash
  + attempt_number
  + seed_if_supported
)
```

The exact encoding/concatenation format must be canonical and domain-separated in any implementation.

## 14. Trial state machine

Conceptual state machine:

```text
CREATED
  -> PREPARED
  -> RUNNING
  -> COLLECTING
  -> VERIFYING
  -> FINALIZED

Exceptional terminals:
  INFRASTRUCTURE_FAILED
  POLICY_BLOCKED
  EVIDENCE_INCOMPLETE
```

Only the WePLD evidence finalizer may emit `FINALIZED`.

The runner may report execution completion, but that maps to `COLLECTING`, not verified success.

## 15. RunnerAdapter contract

Conceptual minimum interface:

```text
RunnerAdapter
- validate_environment(EnvironmentManifest)
- prepare_trial(TrialIdentity, manifests)
- start_trial()
- observe_trial()
- stop_trial(reason)
- collect_stdout_stderr()
- collect_artifacts()
- collect_usage()
- collect_effect_events()
- cleanup()
```

The adapter returns observations and artifact references. It does not return authoritative `pass=true`.

## 16. Runner independence

The H0 evidence schema must be runner-neutral enough that the same experiment can be replayed through:

```text
WEPLD_MINIMAL_LOCAL_RUNNER
HARBOR_EXTERNAL_RUNNER
OTHER_FUTURE_RUNNER
```

without redefining:

```text
TrialIdentity
VerifierManifest
EffectEnvelope
TrialRecord
MetricRecord
FailureRecord
H0 decision rules
```

Runner-specific metadata belongs in an extension field and cannot alter common semantics.

## 17. RawObservationRecord

```text
RawObservationRecord
- trial_id
- source
- sequence_number
- monotonic_timestamp_if_available
- wall_timestamp
- observation_type
- content_hash
- bounded_inline_summary
- artifact_reference
```

Raw observations should be append-oriented and retained even when later classified as irrelevant or failed.

## 18. ArtifactRecord

```text
ArtifactRecord
- trial_id
- artifact_id
- relative_path_or_logical_name
- content_hash
- size_bytes
- media_type
- producer
- created_phase
- verifier_input
- retention_class
```

Large artifacts may live outside Git, but their cryptographic identity and provenance must be retained.

## 19. UsageRecord

```text
UsageRecord
- trial_id
- model_requests
- input_tokens
- output_tokens
- cache_read_tokens_if_available
- cache_write_tokens_if_available
- total_tokens
- provider_reported_cost_if_available
- measured_wall_seconds
- model_wall_seconds_if_available
- tool_wall_seconds_if_available
- verifier_wall_seconds
- runner_overhead_wall_seconds_if_measurable
```

Missing fields are marked unavailable; they are not imputed from unrelated providers.

## 20. EffectEventRecord

Every observable effect attempt should be classifiable as:

```text
REQUESTED
ATTEMPTED
ALLOWED
DENIED
COMPLETED
FAILED
```

Minimum event fields:

```text
EffectEventRecord
- trial_id
- sequence_number
- effect_class
- target
- requested_authority
- envelope_decision
- execution_result
- external_egress
- credential_class_if_any
- irreversible
- evidence_reference
```

Hard H0 gates are derived from these records where instrumentation supports them.

## 21. VerifierRecord

```text
VerifierRecord
- trial_id
- verifier_manifest_hash
- verifier_start
- verifier_end
- exit_status
- deterministic_pass
- stdout_hash
- stderr_hash
- output_artifact_hashes
- verifier_failure_class
- residual_limitations
```

If the verifier itself fails to execute reliably, do not convert that condition into task success.

## 22. FailureRecord

```text
FailureRecord
- trial_id
- failure_id
- failure_class
- first_bad_phase
- evidence_references
- model_contribution
- harness_contribution
- runner_contribution
- environment_contribution
- verifier_contribution
- shared_infrastructure
- retry_eligible_under_frozen_policy
- replacement_trial_id_if_any
```

Failure attribution may contain uncertainty; raw evidence remains primary.

## 23. TrialRecord

Final durable trial record:

```text
TrialRecord
- trial_id
- all_manifest_hashes
- runner_identity
- runner_version_or_commit
- state_history
- start/end times
- raw_observation_index_hash
- artifact_index_hash
- usage_record_hash
- effect_event_index_hash
- verifier_record_hash
- failure_record_hashes
- verified_success
- hard_gate_events
- evidence_completeness
- final_record_hash
```

`verified_success` is mechanically derived from the frozen verifier semantics plus evidence completeness/hard-gate policy; it is not copied from model or runner text.

## 24. RetryPolicy

Retry behavior is frozen before confirmatory execution.

Default H0 rule:

```text
TASK_OR_HARNESS_FAILURE_RETRY = NO
MODEL_BEHAVIOR_FAILURE_RETRY = NO
BUDGET_EXHAUSTION_RETRY = NO
SHARED_INFRASTRUCTURE_REPLACEMENT = MAX_1_IF_INDEPENDENTLY_PROVEN
PROVIDER_OUTAGE_REPLACEMENT = MAX_1_IF_INDEPENDENTLY_PROVEN
```

A replacement attempt never deletes the original failed run.

The same rule applies across arms.

## 25. Evidence completeness gate

A trial cannot enter confirmatory analysis as a normal success/failure observation if required identity or verifier evidence is missing in a way that makes the outcome uninterpretable.

Instead classify:

```text
EVIDENCE_INCOMPLETE
```

and preserve it in denominator/accounting according to the preregistered missing-evidence rule.

No operator may silently remove it.

## 26. False-completion accounting

A false-completion event occurs when the model/harness claims completion but the final verifier does not pass.

```text
FalseCompletionRecord
- trial_id
- completion_claim_evidence
- verifier_failure_evidence
- claim_to_verifier_latency
```

This is a first-class H0 metric because proof-carrying completion is a core WePLD thesis.

## 27. No-progress accounting

No-progress detection may use runner-independent signals where possible:

```text
repeated_identical_tool_calls
repeated_patch_reversion
repeated_same_failure_without_new_evidence
turns_without_artifact_state_change
turns_without_verifier_state_change
```

Any heuristic detector must be versioned and must not alter final task acceptance.

## 28. Provider/model egress separation

Model-serving traffic is not equivalent to task-environment network authority.

Record separately:

```text
MODEL_PROVIDER_EGRESS
TASK_ENVIRONMENT_EGRESS
RUNNER_CONTROL_EGRESS
VERIFIER_EGRESS
OBSERVABILITY_EGRESS
```

H0 should minimize all categories except the model-serving path required by the selected model.

## 29. Secret handling

```text
SECRETS_IN_GIT = NO
SECRETS_IN_MANIFESTS = NO
SECRETS_IN_RAW_LOGS = NO_BY_POLICY
SECRET_REFERENCE_NAMES = ALLOWED
SECRET_VALUES = INJECTED_ONLY_AT_EXECUTION_BOUNDARY
```

Before external review/publication, evidence artifacts require secret/private-data screening.

## 30. Local-first research posture

For the initial falsification implementation, prefer:

```text
LOCAL_OR_CONTROLLED_CONTAINER = YES
TASK_NETWORK = DENY_BY_DEFAULT
CLOUD_SANDBOX = OPTIONAL_NOT_REQUIRED
REMOTE_OBSERVABILITY = OFF_BY_DEFAULT
IRREVERSIBLE_EXTERNAL_EFFECTS = NONE
```

This reduces provider/environment variance and keeps H0 focused on harness effects.

This does not imply that future production WePLD execution must be local-only.

## 31. Concurrency rule

Parallelism is experiment plumbing, not an arm advantage.

Concurrency settings must not change per arm in a way that grants more effective budget or causes known resource contention bias.

Record:

```text
host_identity_or_pool
concurrency_limit
resource_allocation
queue_delay_if_measurable
```

Randomize or balance run order across arms/models/tasks where practical to reduce temporal/provider drift.

## 32. Run-order randomization

Before confirmatory execution, generate and freeze run ordering or batching rules.

Requirements:

- avoid running all of one arm before all of another;
- balance model/provider temporal drift across arms;
- preserve task pairing;
- avoid concurrent sibling trials that contend for the same mutable task state;
- keep randomization seed/algorithm in the evidence packet.

## 33. Paired-analysis export

The evidence plane must export a runner-neutral table with at least:

```text
trial_id
task_id
task_archetype
model_family
model_id
arm
recipe_id
attempt_number
verified_success
input_tokens
output_tokens
total_tokens
cost_if_available
wall_seconds
no_progress_turns
false_completion
unauthorized_attempted_effects
accepted_unauthorized_effects
unaccounted_external_egress
verifier_bypass
failure_class
replacement_of_trial_id
```

The H0 analyzer consumes this normalized export plus the frozen manifests.

## 34. Analysis isolation

The paired analyzer must not need model credentials, runner credentials, or task execution authority.

Preferred posture:

```text
ANALYSIS_INPUT = IMMUTABLE_NORMALIZED_EVIDENCE
ANALYSIS_NETWORK = NONE_REQUIRED
ANALYSIS_WRITE_AUTHORITY = REPORT_OUTPUT_ONLY
```

This makes statistical recomputation independently reviewable.

## 35. Mechanical H0 decision derivation

A decision report should be derivable mechanically from:

```text
H0 contract version
normalized trial evidence
paired bootstrap result
hard-gate event counts
generalization guardrails
complexity/economics guardrails
```

Expected output enum:

```text
GO_STATIC_RESEARCH
GO_ADAPTIVE_RESEARCH
NARROW_TO_STATIC_COMPILATION
PORTFOLIO_ONLY
KILL_STANDALONE_HARNESS_PROGRAM
EXPERIMENT_INVALID_REQUIRES_NEW_PROTOCOL
```

The analyzer may produce explanatory diagnostics, but it may not invent a new result class after seeing outcomes.

## 36. External runner qualification checklist

Before using Harbor or another external runner for H0, prove at minimum:

```text
EXACT_PIN
LICENSE_RIGHTS
INSTALLATION_REPRODUCIBILITY
TASK_IDENTITY_PRESERVATION
ENVIRONMENT_DIGEST_PRESERVATION
MODEL_SETTING_PRESERVATION
RAW_ARTIFACT_ACCESS
RAW_STDOUT_STDERR_ACCESS_OR_DOCUMENTED_LIMITATION
TOKEN_USAGE_ACCESS_OR_DOCUMENTED_LIMITATION
NO_SILENT_RETRY
NO_SILENT_TASK_DROP
NETWORK_POLICY_COMPATIBILITY
SECRET_HANDLING_COMPATIBILITY
CLEANUP_BEHAVIOR
EXIT_PATH
```

If a runner cannot satisfy a decision-critical requirement, either wrap it safely or reject it for H0.

## 37. Minimal-runner versus Harbor decision rule

No runner is selected in this document.

Research selection should follow minimum-sufficient complexity:

```text
IF a small WePLD-owned runner can satisfy H0 manifests,
container execution, evidence capture, and required concurrency
WITHOUT recreating substantial mature infrastructure:
    prefer the small runner for H0.

ELSE IF Harbor can satisfy the same WePLD-owned contract
behind a narrow replaceable adapter with acceptable dependency/egress burden:
    separately qualify Harbor as an external research runner.

ELSE:
    evaluate another replaceable runner.
```

Runner selection must not change H0 success thresholds.

## 38. Donor-code boundary

Nothing in this contract authorizes copying donor implementation.

```text
HARBOR_CODE_IMPORT = NONE
HARNESS_BENCH_CODE_IMPORT = BLOCKED_RIGHTS_NOT_ESTABLISHED
SCAFFOLD_EFFECTS_CODE_IMPORT = NONE
```

Behavioral learning and public-interface inspection remain research evidence only.

## 39. Minimum falsification implementation boundary

If a future separately authorized research implementation is opened, the smallest justified implementation should cover only:

```text
manifest canonicalization + hashing
trial identity
one replaceable local/container runner adapter
artifact + usage capture
objective verifier invocation
failure/effect record capture
normalized export
paired H0 analyzer
mechanical decision report
```

Explicitly out of initial H0 implementation:

```text
GENERAL HIR
PRODUCTION HARNESS ROUTER
SELF_EVOLUTION
HARNESS GYM SEARCH
MODEL TRAINING
MODEL_HARNESS FLYWHEEL
MULTI_CLOUD ORCHESTRATION
PRODUCT UI
GENERAL PLUGIN MARKETPLACE
S1_013 WORK
```

## 40. Current research decision

```text
H0_EVIDENCE_CONTRACT = DEFINED_ON_RESEARCH_BRANCH
RUNNER_SELECTED = NO
HARBOR_ADOPTED = NO
H0_IMPLEMENTATION = NOT_STARTED
H0_SCREENING = NOT_STARTED
H0_CONFIRMATORY = NOT_STARTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
S1_013_PLUS = NOT_STARTED
```

Next research action:

> Perform a bounded runner decision review: estimate the smallest local runner required by this contract versus the exact Harbor pin, then choose the minimum sufficient experimental substrate before any implementation authorization.
