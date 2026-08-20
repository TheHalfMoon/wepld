# WePLD Harness Program — H0 Screening Fixture and Recipe Boundary

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / FALSIFICATION BOUNDARY
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

This document freezes the minimum synthetic runner qualification fixtures and the conceptual A/B/C/D recipe boundaries required before H0 screening implementation may be authorized.

It prevents H0 from turning into an unbounded agent framework build.

Governing documents:

- `WEPLD_HARNESS_H0_THESIS_TOURNAMENT_CONTRACT_2026-08-20.md`
- `WEPLD_HARNESS_H0_EVIDENCE_AND_RUNNER_CONTRACT_2026-08-20.md`
- `WEPLD_HARNESS_H0_RUNNER_DECISION_REVIEW_2026-08-20.md`

## 2. H0 component boundary

H0 is not a test of every proposed Harness Program subsystem.

The initial recipe component vocabulary is limited to:

```text
ContextPolicy
ToolSurfacePolicy
PlanningPolicy
VerifierCadencePolicy
RecoveryPolicy
StopPolicy
```

Explicitly excluded from H0 v1:

```text
GENERAL_MEMORY_SYSTEM
MULTI_AGENT_DELEGATION
SIBLING_PORTFOLIO
SELF_EVOLUTION
HARNESS_SEARCH
TRAINING_FLYWHEEL
GENERAL HIR PLUGIN SYSTEM
PRODUCTION AUTHORITY ENGINE
PRODUCT UI
```

Existing WePLD authority/effect controls remain external constraints, not experimental knobs.

## 3. Shared component library rule

B, C, and D must select from the same predeclared component option set.

```text
B_COMPONENT_LIBRARY == C_COMPONENT_LIBRARY == D_COMPONENT_LIBRARY
```

This prevents D from winning because it secretly receives components unavailable to C/B.

A intentionally represents a smaller minimal baseline.

## 4. Arm A — minimal baseline boundary

A should contain only the minimum generic loop needed to attempt an eligible task.

Conceptual recipe:

```text
A_MINIMAL
context = current instruction + bounded recent observations + changed artifacts needed now
tools = minimum file/read/write/execute surface required by task environment
planning = none as a separate phase
verifier_cadence = final-only except explicit user/task-requested tests
recovery = one bounded error-aware continuation path, no reflection loop
stop = budget exhausted OR objective verifier success OR deterministic unrecoverable failure
```

A may inspect test/compiler output produced by ordinary tool use. It does not receive a general separate planning/reflection/meta-agent loop.

## 5. Shared B/C/D component options

### 5.1 ContextPolicy options

```text
CTX_MINIMAL
- active instruction
- current changed artifacts
- latest relevant tool evidence

CTX_STRUCTURED
- immutable task invariants
- current plan state
- changed artifacts
- unresolved failures
- relevant recent observations
- bounded historical decisions

CTX_COMPACTING
- CTX_STRUCTURED
- deterministic threshold-triggered compaction
- exact references for rehydration
```

No semantic model-generated long-term memory store in H0 v1.

### 5.2 ToolSurfacePolicy options

```text
TOOLS_MINIMAL
- minimum generic file + execution operations

TOOLS_TASK_SCOPED
- predeclared subset selected from task/environment fingerprint

TOOLS_FULL_ALLOWED
- all H0-admitted tools permitted by the same effect envelope
```

Tool selection cannot expand authority.

### 5.3 PlanningPolicy options

```text
PLAN_NONE
PLAN_ONCE
PLAN_ONCE_PLUS_REPLAN_ON_VERIFIER_FAILURE
```

No recursive planner hierarchy.

### 5.4 VerifierCadencePolicy options

```text
VERIFY_FINAL_ONLY
VERIFY_AFTER_MUTATION_BATCH
VERIFY_ON_FAILURE_BOUNDARY
VERIFY_AFTER_MUTATION_AND_ON_FAILURE
```

All options still use the same frozen final acceptance verifier.

### 5.5 RecoveryPolicy options

```text
RECOVERY_MINIMAL
- continue from first actionable failure evidence

RECOVERY_CLASSIFIED
- classify failure into frozen H0 failure classes
- choose one bounded predeclared intervention

RECOVERY_CLASSIFIED_WITH_SINGLE_REPLAN
- same as above plus one bounded replan when permitted
```

No mutation of the harness itself.

### 5.6 StopPolicy options

```text
STOP_BUDGET_OR_FINAL_PASS
STOP_BUDGET_OR_FINAL_PASS_OR_NO_PROGRESS
```

No arm may self-extend its budget.

## 6. Arm B — fixed rich baseline

B uses one fixed richer recipe across every supported model/task cell.

Initial research candidate:

```text
B_FIXED_RICH
context = CTX_STRUCTURED
tools = TOOLS_FULL_ALLOWED
planning = PLAN_ONCE
verifier_cadence = VERIFY_AFTER_MUTATION_BATCH
recovery = RECOVERY_CLASSIFIED
stop = STOP_BUDGET_OR_FINAL_PASS_OR_NO_PROGRESS
```

The exact B recipe may be changed during pre-confirmatory screening repair, but must be globally fixed before confirmatory execution.

B cannot route by model, task archetype, or benchmark task identity.

## 7. Arm C — static task/environment compiler

C deterministically selects component options from only:

```text
TaskFingerprint
EnvironmentFingerprint
BudgetRiskEnvelope
```

C must not inspect:

```text
model family
model identity
model calibration profile
H0 outcome history for the task
benchmark-specific task ID lookup tables
```

Conceptual compiler:

```text
StaticRecipeCompiler(task, environment, budget_risk) -> RecipeManifest
```

The compiler is deterministic for identical inputs.

### Candidate static routing dimensions

Allowed task/environment signals:

```text
expected_mutation_surface
repository_scale_bucket
verifier_availability
expected_horizon
security_sensitivity
reversibility
language_toolchain_class
build_cost_bucket
network_requirement
concurrency_suitability
```

Do not route on hidden task answers or historical success labels.

## 8. Arm D — adaptive model-aware compiler

D uses the exact C inputs plus a frozen ModelCapabilityProfile.

```text
AdaptiveRecipeCompiler(
  model_profile,
  task,
  environment,
  budget_risk
) -> RecipeManifest
```

D selects from the same B/C/D component library.

D v1 is **deterministic evidence-driven routing**, not a meta-agent that writes new harness code.

```text
D_SELF_EVOLUTION = NO
D_DYNAMIC_CODE_GENERATION = NO
D_SIBLING_PORTFOLIO = NO
D_MODEL_WRITES_ITS_OWN_RECIPE = NO
```

This isolates whether model-aware routing is useful before testing autonomous harness mutation.

## 9. Model capability calibration boundary

D requires a ModelCapabilityProfile that is independent of H0 benchmark outcomes.

Use a separate calibration suite:

```text
H0_CALIBRATION_TASKS = SYNTHETIC / MICRO-CAPABILITY
DISJOINT_FROM_H0_SCREEN = YES
DISJOINT_FROM_H0_CONFIRM = YES
PROMOTION_EVIDENCE = NO
```

Candidate measured dimensions:

```text
tool_call_reliability
structured_output_reliability
parallel_tool_reliability_if_used
shell_command_accuracy
patch_application_accuracy
instruction_retention_under_length
context_degradation_bucket
planning_gain_microtest
verifier_feedback_recovery_gain
compaction_sensitivity
no_progress_signature
```

Calibration fixtures must not contain H0 screening/confirmatory task solutions or benchmark-specific identifiers.

## 10. Calibration repeatability

Before confirmatory execution:

- freeze calibration fixture identities;
- run the same calibration protocol for each model family;
- record exact model/provider settings;
- derive the profile mechanically from recorded outcomes;
- freeze the profile hash used by D.

If a provider/model revision changes materially, recalibration creates a new profile identity.

## 11. No screening-outcome router training

H0-SCREEN may expose implementation defects and variance, but D's confirmatory router may not be trained to memorize screening task identities or exploit their labels.

Allowed screening use:

```text
fix generic implementation bugs
remove ambiguous component semantics
freeze operational thresholds
validate model-profile calibration
validate routing determinism
```

Forbidden:

```text
if task_id == known_screening_task: choose recipe X
optimize directly against screening task answers
carry benchmark-specific solution text into recipe rules
```

## 12. Budget fairness

A/B/C/D receive the same maximum per-task declared budget envelope for a paired comparison.

A recipe may consume less.

```text
SAME_MAX_WALL_BUDGET
SAME_MAX_TOKEN_BUDGET_WHERE_ENFORCEABLE
SAME_MAX_MONEY_BUDGET_WHERE_ENFORCEABLE
SAME_EFFECT_ENVELOPE
```

If one arm deliberately allocates more substeps within the same total budget, the consumed tokens/time remain part of its efficiency result.

## 13. Prompt fairness

Every arm receives the same user/task instruction bytes for the same task.

Harness-specific system/developer instructions are part of the recipe and are hashed as experimental variables.

No arm receives hidden gold answers.

## 14. Tool fairness

Tool semantics must be equivalent when a tool class is shared across arms.

Different tool **selection** is allowed as the studied harness variable; different hidden effect authority is not.

A typed high-level tool and a low-level primitive may be compared only if both remain within the same effect envelope and their capability difference is explicitly part of the recipe policy.

## 15. Final verifier fairness

Every arm for a task is judged by the exact same final VerifierManifest.

Internal tests/verifiers chosen during execution may differ by recipe cadence, but final acceptance does not.

## 16. Synthetic runner qualification suite

Synthetic runner fixtures are executed before any H0 model/harness screening task.

They validate runner/evidence mechanics only.

### F01 — deterministic passing task

Expected:

```text
runner completes
artifact captured
objective verifier passes
TrialRecord.verified_success = true
no hard-gate event
```

### F02 — deterministic failing task

Expected:

```text
runner completes
objective verifier fails
TrialRecord.verified_success = false
TASK_FAILURE recorded
```

### F03 — false completion

Synthetic agent prints a completion claim without producing required artifact.

Expected:

```text
final verifier fails
verified_success = false
FALSE_COMPLETION recorded
```

### F04 — timeout

Synthetic agent exceeds wall budget.

Expected:

```text
process stopped
BUDGET_EXHAUSTION/TIMEOUT recorded
cleanup attempted
no success fabrication
```

### F05 — process crash

Expected:

```text
nonzero/unexpected process termination retained
PROCESS/HARNESS failure classification
partial logs preserved
```

### F06 — malformed runner output

Expected:

```text
raw output retained
parser failure does not erase trial
EVIDENCE_INCOMPLETE or runner failure according to frozen rule
```

### F07 — missing required artifact

Expected:

```text
verifier fails or evidence completeness fails
verified_success != true
```

### F08 — oversized stdout/stderr

Generate output beyond retained-inline limits.

Expected:

```text
bounded inline representation
full/raw artifact handling according to policy
truncation observable
runner remains live
```

### F09 — verifier crash

Expected:

```text
VERIFIER_FAILURE
verified_success != true
no fallback-to-model-claim
```

### F10 — cleanup failure

Expected:

```text
trial outcome evidence retained
cleanup failure separately recorded
next fixture cannot inherit mutable workspace/process state
```

### F11 — denied network attempt

Synthetic task tries a forbidden host.

Expected where instrumentation supports enforcement:

```text
attempt denied
EffectEventRecord emitted
accepted_unauthorized_effect = 0
```

### F12 — unexpected allowed egress detector

Where testable, intentionally configure a canary endpoint outside the envelope.

Expected:

```text
no successful connection
or hard-gate incident if the environment incorrectly permits it
```

### F13 — secret redaction boundary

Inject a synthetic canary secret at execution boundary.

Expected:

```text
secret absent from committed manifests
secret absent from normalized public evidence
raw-log handling follows private retention policy
```

Do not use real credentials for this fixture.

### F14 — parallel workspace isolation

Run two synthetic trials concurrently with colliding logical filenames.

Expected:

```text
no cross-trial file visibility
no artifact mix-up
correct TrialIdentity binding
```

### F15 — retry policy

Force one eligible shared-infrastructure failure and one ineligible task failure.

Expected:

```text
eligible replacement <= 1
original retained
ineligible task failure not retried
```

### F16 — run-order identity

Execute fixtures in reordered batches.

Expected:

```text
TrialIdentity unchanged by schedule position
results remain bound to exact manifests
```

## 17. Synthetic fixture pass gate

Before H0-SCREEN:

```text
ALL_REQUIRED_FIXTURES = PASS
UNEXPLAINED_EVIDENCE_MISMATCH = 0
ACCEPTED_UNAUTHORIZED_EFFECT = 0
SECRET_CANARY_LEAK_TO_PUBLIC_EVIDENCE = 0
CROSS_TRIAL_CONTAMINATION = 0
```

A fixture failure is a runner/evidence defect, not evidence about A/B/C/D.

## 18. Recipe compiler conformance fixtures

Separate deterministic unit fixtures should prove:

### R01 — identical C input produces identical recipe

```text
same task/env/budget -> same RecipeManifest hash
```

### R02 — C ignores model identity

Swap only ModelManifest.

Expected:

```text
C recipe unchanged
```

### R03 — D may differ by model profile

Keep task/env/budget fixed and use two frozen model profiles with a predeclared relevant capability difference.

Expected:

```text
D recipe may differ only according to frozen routing rule
```

### R04 — D cannot select unknown component

Expected:

```text
fail closed
```

### R05 — no authority expansion

Any component combination requesting effect authority outside task envelope:

```text
recipe validation fails
```

### R06 — no budget expansion

Any compiler output exceeding task BudgetPolicy:

```text
recipe validation fails
```

### R07 — no benchmark-ID special case

Compiler behavior must be explainable from declared fingerprint/profile fields, not raw benchmark task identity.

## 19. Minimum routing-rule transparency

Every C/D selected recipe should emit a machine-readable decision trace:

```text
RecipeDecisionTrace
- input fingerprint hashes
- rule identifiers evaluated
- selected component option IDs
- rejected option IDs with reason codes
- budget constraints applied
- authority constraints applied
- final RecipeManifest hash
```

No chain-of-thought is required or retained.

The trace records decision facts, not private model reasoning.

## 20. No LLM router in H0 v1

The initial D router should not itself be an LLM call.

Reason:

- introduces another model and stochastic variable;
- complicates attribution;
- can consume meaningful budget;
- risks task-content leakage into routing;
- makes the first adaptive claim harder to falsify.

H0 v1 tests whether **evidence-driven model-aware routing** has value. An LLM/meta-agent router can be a later separately falsified hypothesis if D v1 earns its complexity.

## 21. No automatic harness mutation

A/B/C/D recipes are assembled from frozen options.

```text
HARNESS_MUTATION_DURING_TRIAL = NO
HARNESS_MUTATION_BETWEEN_CONFIRMATORY_RUNS = NO
SELF_PROMOTION = NO
```

Any recipe revision before confirmatory execution creates a new recipe identity and must be frozen globally before use.

## 22. Minimal H0 implementation surface implied by this document

If separately authorized later, implementation needs only enough to support:

```text
frozen option enums/configs
A recipe construction
B fixed recipe
C deterministic static compiler
D deterministic model-aware compiler
model calibration fixtures/profile derivation
synthetic runner fixtures
recipe conformance fixtures
```

This does not justify a generalized HIR framework.

## 23. Screening output required before confirmatory planning

H0-SCREEN must produce both experiment and infrastructure evidence:

```text
A/B/C/D screening metrics
failure taxonomy
recipe-selection traces
model calibration profiles
runner adequacy metrics
runner-caused invalid/incomplete rate
runner overhead
operator recovery burden
hard-gate incidents
component-level obvious defects
```

Only after this evidence may the confirmatory runner decision be resolved.

## 24. Research stop rule

At this point the Harness Program has enough architecture to seek implementation authorization.

Do not add more major H0 subsystems before execution evidence.

```text
MORE_ARCHITECTURE_BEFORE_SCREENING = BLOCKED_UNLESS_REQUIRED_BY_A_PROVEN_GAP
GENERAL_HIR_DESIGN_EXPANSION = STOP
SELF_EVOLUTION_DESIGN_EXPANSION = STOP
HARNESS_GYM_DESIGN_EXPANSION = STOP
```

## 25. Current authority state

```text
H0_TOURNAMENT_CONTRACT = DEFINED
H0_EVIDENCE_RUNNER_CONTRACT = DEFINED
H0_RUNNER_STRATEGY = STAGED_MINIMAL_THEN_CONDITIONAL_HARBOR
H0_RECIPE_BOUNDARIES = DEFINED
H0_SYNTHETIC_FIXTURE_BOUNDARY = DEFINED
H0_IMPLEMENTATION_AUTHORITY = NONE
H0_SCREENING = NOT_STARTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
S1_013_PLUS = NOT_STARTED
```

Next action is governance, not more architecture:

> Inspect canonical WePLD policy and determine the smallest separately governed authorization required to implement the H0 screening-only research surface without opening S1-013 or changing the product roadmap.
