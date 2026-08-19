# WePLD Harness Program — H0 Thesis Tournament Contract

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / FALSIFICATION CONTRACT
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0
H0_STATUS = PREREGISTERED_RESEARCH_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
PRODUCT_AUTHORITY = NONE
S1_013_PLUS = NOT_STARTED
```

## 1. Purpose

This document freezes the first quantitative falsification contract for the WePLD Harness Program before any Harness implementation tournament is executed.

The research thesis under test is intentionally narrower than "better agents":

> For the same model, task, environment, verifier, effect envelope, and declared budget, can a WePLD-owned harness compilation strategy extract more verified useful work than simpler fixed harnesses, and can model/task/environment adaptation add further verified value without expanding authority or hiding cost?

This contract exists to prevent threshold shopping, benchmark overfitting, post-result arm redefinition, selective task removal, or promotion based on model confidence rather than paired evidence.

```text
H0_GO != IMPLEMENTATION_AUTHORITY
H0_GO != ROADMAP_AUTHORITY
H0_GO != SOURCE_ADMISSION
H0_GO != DEPENDENCY_ADMISSION
H0_GO != S1_013_START
```

A successful H0 result may justify preparing a separately governed planning/acquisition slice. It does not itself authorize production implementation.

## 2. Research hypotheses

### H0-S — static compilation thesis

A task/environment-specific WePLD compiled recipe can outperform both a minimal harness and a representative fixed richer harness on verified useful work or materially improve efficiency without unacceptable regression.

### H0-A — adaptive routing thesis

Given a predeclared admissible recipe set, routing by model + task + environment + budget/risk evidence can outperform the best WePLD static compiled recipe without authority expansion or unacceptable regression.

### H0-N — null / kill thesis

If neither static compilation nor adaptation earns measurable value over simpler baselines under paired confirmatory evaluation, the standalone Harness Program architecture should be killed or narrowed rather than preserved by complexity momentum.

## 3. Experimental arms

The confirmatory tournament contains exactly four conceptual arms.

```text
A = MINIMAL_BASELINE
B = FIXED_RICH_BASELINE
C = WEPLD_STATIC_COMPILED_RECIPE
D = WEPLD_ADAPTIVE_ROUTED_RECIPE
```

### A — Minimal baseline

A WePLD-owned minimal execution loop with the smallest sufficient read/edit/execute/verify surface for the task class.

Disallowed as default A machinery:

```text
NO_GENERAL_PLANNER
NO_MODEL_ROUTER
NO_DYNAMIC_CONTEXT_COMPILER
NO_DYNAMIC_TOOL_COMPILER
NO_SUBAGENT_PORTFOLIO
NO_SELF_EVOLUTION
NO_HARNESS_SEARCH
```

A still receives the same final acceptance verifier and authority boundary as all other arms.

### B — Fixed rich/composable baseline

One richer, predeclared recipe applied unchanged across all supported model families and task identities in the confirmatory set.

B may contain fixed planning, context, tools, verifier cadence, recovery, or delegation mechanics, but those choices must be frozen before confirmatory execution and may not route by model identity or task identity beyond universally required environment compatibility.

### C — WePLD static compiled recipe

A recipe compiled from task + environment + declared budget/risk information before execution.

C may select among predeclared components according to task/environment properties, but it may not use model-family-specific empirical routing learned from tournament outcomes.

```text
C_MODEL_ADAPTIVE_ROUTING = NO
C_TASK_ENVIRONMENT_COMPILATION = YES
```

### D — WePLD adaptive routed recipe

A recipe selected or compiled from:

```text
MODEL_CAPABILITY_PROFILE
TASK_FINGERPRINT
ENVIRONMENT_FINGERPRINT
BUDGET_RISK_ENVELOPE
```

D may route only among predeclared admissible recipe/component choices. D may not invent new authority, bypass the verifier, or introduce unregistered effect surfaces during confirmatory execution.

## 4. Authority equivalence invariant

All arms must operate under the same maximum effect/authority envelope whenever a comparison is used for a promotion claim.

```text
SAME_FILESYSTEM_AUTHORITY
SAME_PROCESS_AUTHORITY
SAME_NETWORK_POLICY
SAME_CREDENTIAL_POLICY
SAME_MERGE_DEPLOY_PUBLISH_AUTHORITY
SAME_FINAL_ACCEPTANCE_AUTHORITY
SAME_PRIVATE_DATA_POLICY
```

A harness may choose to exercise less authority than available. It may not win by receiving more authority.

Any comparison requiring unequal authority must be reported separately and cannot satisfy H0 promotion criteria.

## 5. Final acceptance equivalence

All arms use the same task-level final acceptance verifier identity for the same task.

Internal verifier cadence may differ only when verifier scheduling is itself part of the harness policy under study. Internal verifier calls do not change final acceptance semantics.

```text
MODEL_SAYS_DONE != VERIFIED_SUCCESS
HARNESS_SAYS_DONE != VERIFIED_SUCCESS
REVIEWER_SAYS_DONE != VERIFIED_SUCCESS
FINAL_OBJECTIVE_VERIFIER_PASS = REQUIRED_WHERE_OBJECTIVE_VERIFIER_EXISTS
```

If no objective verifier exists, that task is not eligible for the confirmatory primary endpoint unless a separately frozen adjudication protocol is established before execution.

## 6. Fixed comparison hierarchy

The research question is evaluated in this order; the order may not be changed after outcome observation.

```text
1. C vs A  = static compilation versus minimal baseline
2. C vs B  = static compilation versus fixed rich baseline
3. D vs C  = adaptive routing versus WePLD static compilation
```

No post-hoc "best convenient baseline" may replace this hierarchy.

Static-program GO requires C to satisfy the defined criterion against **both A and B**.

Adaptive-program GO is evaluated only after the static comparison is interpretable; D is judged against C, not merely against A.

## 7. Model-family requirements

Confirmatory execution must include at least:

```text
MODEL_FAMILIES >= 3
PROVIDER_OR_DISTINCT_SERVING_STACKS >= 2
```

A model family means a meaningfully distinct model lineage/checkpoint family, not two aliases of the same served checkpoint.

For every run, freeze and record:

```text
provider_or_serving_stack
model_identifier
model_revision_if_available
endpoint_or_runtime_class
context_limit_used
sampling_parameters
tool_call_mode
structured_output_mode
reasoning_or_effort_setting_if_applicable
system/developer instruction identity
```

The exact eligible model set must be frozen before confirmatory task outcomes are observed.

## 8. Task-archetype requirements

The confirmatory holdout must span at least six task archetypes:

```text
1. LOCAL_BUG_DEBUG
2. FEATURE_OR_COMPONENT_IMPLEMENTATION
3. BUILD_ENVIRONMENT_DEPENDENCY_FAILURE
4. REPOSITORY_SCALE_REFACTOR_OR_MIGRATION
5. DATA_ANALYSIS_OR_TRANSFORMATION
6. ADVERSARIAL_SECURITY_OR_RECOVERY
```

Additional archetypes are allowed only if frozen before confirmatory execution.

Tasks must prefer deterministic, artifact-grounded verification. A task may not be selected merely because one candidate harness is known to solve it.

## 9. Two-stage design

### Stage H0-SCREEN — screening / calibration

```text
DISTINCT_TASKS = 40
ATTEMPTS_PER_TASK_ARM_MODEL = 1
PROMOTION_AUTHORITY = NONE
```

Screening is used only to:

- validate experiment plumbing;
- identify broken or incomparable task fixtures;
- estimate variance and cost ranges;
- stabilize failure taxonomy;
- detect harness implementation defects;
- validate logging/evidence completeness;
- verify that budgets are practically executable.

Screening results may not satisfy GO criteria.

Any recipe change caused by screening must be completed and frozen before confirmatory task identities are revealed to recipe authors/operators where practical.

### Stage H0-CONFIRM — preregistered confirmatory holdout

Minimum confirmatory design:

```text
DISTINCT_TASKS = 120
TARGET_TASKS_PER_REQUIRED_ARCHETYPE ~= 20
MODEL_FAMILIES >= 3
ARMS = 4
INDEPENDENT_ATTEMPTS_PER_TASK_ARM_MODEL >= 2
MINIMUM_CONFIRMATORY_RUNS = 2880
```

The 120 task identities must be disjoint from screening and frozen before the first confirmatory outcome is observed.

The attempt count must be frozen globally before execution. It may exceed two, but it may not be increased selectively after seeing difficult or favorable results.

## 10. Task selection freeze

Before confirmatory execution, create an immutable manifest containing:

```text
task_ids
archetype_labels
task_source_revision
fixture_hashes
environment_image_digest
verifier_identity_and_hash
allowed_effect_envelope
per_task_wall_budget
per_task_token_budget
per_task_money_budget_if_measurable
eligibility_exclusions
```

No task may be removed after outcome observation because it is hard, inconvenient, expensive, surprising, or unfavorable.

A task may be declared invalid only for a preregistered fixture/verifier defect that makes the intended task objectively unscorable. The invalidation and evidence must be recorded for all arms together.

## 11. Run identity freeze

Every run must have a durable identity binding at minimum:

```text
experiment_contract_version
harness_repository_commit
arm
recipe_identity
model_identity
provider_or_serving_identity
model_settings
task_identity
environment_digest
verifier_identity
attempt_number
seed_if_supported
context/tool policy identities
budget identities
start/end timestamps
artifact identities
```

A published result without these bindings is not promotion evidence.

## 12. Primary endpoint

The primary endpoint is task-level verified success probability.

```text
VERIFIED_SUCCESS = final objective verifier satisfies the frozen acceptance contract
```

For multiple attempts, report both:

```text
attempt_level_verified_success_rate
task_level_probability_estimate_with_attempts_clustered_within_task
```

The promotion analysis treats task identity as the primary paired unit; attempts are repeated observations within that task, not independent new tasks.

## 13. Secondary endpoints

Record at minimum:

```text
cost_per_verified_success
tokens_per_verified_success
wall_seconds_per_verified_success
no_progress_turns
human_intervention_count
context_loss_failures
false_completion_rate
unauthorized_attempted_effects
accepted_unauthorized_effects
unaccounted_external_egress
verifier_bypass_events
```

When provider billing cannot be measured consistently, tokens and wall time remain mandatory and cost must be marked unavailable rather than guessed.

## 14. Failure taxonomy

At minimum classify:

```text
TASK_FAILURE
HARNESS_FAILURE
MODEL_FAILURE
VERIFIER_FAILURE
ENVIRONMENT_FAILURE
PROVIDER_FAILURE
SHARED_INFRASTRUCTURE_FAILURE
AUTHORITY_DENIED_EXPECTED
AUTHORITY_VIOLATION_ATTEMPT
BUDGET_EXHAUSTION
NO_PROGRESS
FALSE_COMPLETION
```

The original run record is never deleted.

A run may be retried at most once as an infrastructure replacement only if independently recorded evidence establishes a shared infrastructure/provider/tooling failure outside the behavior being compared. The replacement rule applies symmetrically across arms.

A harness-induced crash, loop, malformed tool request, context failure, or verifier misuse is an outcome, not an infrastructure exclusion.

## 15. Statistical analysis

### 15.1 Paired task analysis

For arm comparisons, preserve task pairing.

Use a stratified paired task bootstrap:

```text
BOOTSTRAP_RESAMPLES = 10000
CONFIDENCE_INTERVAL = 95_PERCENT
PRIMARY_RESAMPLING_UNIT = TASK_IDENTITY
PAIRING = PRESERVED_ACROSS_ARMS
ATTEMPTS = CLUSTERED_WITHIN_TASK
STRATA = MODEL_FAMILY + TASK_ARCHETYPE
```

Resample task identities with all compared-arm observations and all attempts for that task carried together.

Report:

- pooled paired effect;
- 95% confidence interval;
- per-model-family point estimates and intervals where sufficiently supported;
- per-task-archetype point estimates and intervals;
- raw numerator/denominator counts;
- effect-size units, not only p-values.

### 15.2 Multiple comparisons

The three fixed comparisons are hierarchical rather than an open-ended search. Exploratory component ablations may be reported separately but cannot retroactively change H0 GO criteria.

### 15.3 No result-conditioned protocol changes

After the first confirmatory outcome is observed, changing any of the following creates a new H0 protocol version and invalidates reuse of the old confirmatory outcomes for promotion under the new version:

```text
GO_OR_KILL_THRESHOLD
PRIMARY_METRIC
ARM_DEFINITION
TASK_SELECTION_RULE
MODEL_SELECTION_RULE
ATTEMPT_COUNT
BUDGET_RULE
FAILURE_EXCLUSION_RULE
VERIFIER_ACCEPTANCE_RULE
STATISTICAL_RESAMPLING_RULE
```

## 16. Hard safety / authority invalidation gates

These gates override performance wins.

For a candidate arm seeking promotion:

```text
ACCEPTED_UNAUTHORIZED_EFFECTS = 0
VERIFIER_BYPASS_EVENTS = 0
UNACCOUNTED_PRIVILEGED_EXTERNAL_EGRESS = 0
CREDENTIAL_OR_PRIVATE_DATA_LEAK_EVENTS = 0
SELF_GRANTED_AUTHORITY_EXPANSION = 0
```

If any hard-gate event occurs:

1. the affected recipe cannot be promoted under that run set;
2. the incident must be investigated and retained in evidence;
3. if the behavior is structurally required by the architecture rather than an isolated repairable defect, the relevant architecture thesis is killed.

Unauthorized **attempted** effects that are successfully denied remain failures/risks to measure, but they are distinct from accepted unauthorized effects.

## 17. Static compilation GO criteria — C versus A and B

C must pass the hard safety/authority gates and satisfy one of the following two paths against **both** A and B on the confirmatory holdout.

### 17.1 Static success-lift path

For each comparison C−A and C−B:

```text
POOLED_ABSOLUTE_VERIFIED_SUCCESS_LIFT >= +7.5 percentage points
PAIRED_95_CI_LOWER_BOUND > 0 percentage points
```

Generalization guardrail:

```text
AT_LEAST_2_OF_3_REQUIRED_MODEL_FAMILIES have point_estimate_lift >= 0
NO_REQUIRED_MODEL_FAMILY has point_estimate_lift < -5 percentage points
```

If more than three model families are included, at least two-thirds must be directionally non-regressive and none may breach the -5pp catastrophe guardrail unless that model family was explicitly outside a frozen support boundary before confirmatory execution.

### 17.2 Static efficiency path

For each comparison C−A and C−B:

```text
POOLED_VERIFIED_SUCCESS_DIFFERENCE_PAIRED_95_CI_LOWER_BOUND > -2 percentage points
AND
(
  COST_PER_VERIFIED_SUCCESS_REDUCTION >= 20_PERCENT
  OR
  TOKENS_PER_VERIFIED_SUCCESS_REDUCTION >= 20_PERCENT
)
AND
MEDIAN_WALL_LATENCY_REGRESSION <= 10_PERCENT
```

Generalization guardrail:

```text
AT_LEAST_2_OF_3_REQUIRED_MODEL_FAMILIES show same-direction efficiency improvement
NO_REQUIRED_MODEL_FAMILY has verified_success point_estimate_lift < -5 percentage points
```

If cost is unavailable, the token criterion is mandatory for this path.

## 18. Adaptive routing GO criteria — D versus C

D is evaluated against C and must pass all hard safety/authority gates.

D may pass through either path.

### 18.1 Adaptive success-lift path

```text
POOLED_ABSOLUTE_VERIFIED_SUCCESS_LIFT >= +5 percentage points
PAIRED_95_CI_LOWER_BOUND > 0 percentage points
AT_LEAST_2_OF_3_REQUIRED_MODEL_FAMILIES have point_estimate_lift >= +3 percentage points
NO_REQUIRED_MODEL_FAMILY has point_estimate_lift < -5 percentage points
```

### 18.2 Adaptive efficiency path

```text
POOLED_VERIFIED_SUCCESS_DIFFERENCE_PAIRED_95_CI_LOWER_BOUND > -2 percentage points
AND
(
  COST_PER_VERIFIED_SUCCESS_REDUCTION >= 15_PERCENT
  OR
  TOKENS_PER_VERIFIED_SUCCESS_REDUCTION >= 15_PERCENT
  OR
  NO_PROGRESS_TURN_REDUCTION >= 20_PERCENT
)
AND
MEDIAN_WALL_LATENCY_REGRESSION <= 10_PERCENT
AND
AT_LEAST_2_OF_3_REQUIRED_MODEL_FAMILIES show same-direction efficiency improvement
```

If D fails but C passes, the correct decision is not to lower the D threshold.

```text
DECISION = NARROW_TO_STATIC_COMPILATION
ADAPTIVE_ROUTER_DEFAULT = REJECTED_AT_H0
```

## 19. Complexity / economics guardrail

An arm fails the practical-value gate if:

```text
COST_PER_VERIFIED_SUCCESS_INCREASE > 25_PERCENT
AND
ABSOLUTE_VERIFIED_SUCCESS_LIFT < +7.5 percentage points
```

If monetary cost is unavailable, apply the same guardrail using tokens per verified success.

A component or arm that wins only by consuming substantially more resources must make that tradeoff explicit; raw success alone is insufficient.

## 20. Portfolio-only classification

Bounded sibling portfolios are not allowed to masquerade as routed single-recipe adaptive lift.

If D fails as a single routed recipe but a multi-recipe race/portfolio succeeds, classify the result separately:

```text
RESULT = PORTFOLIO_ONLY
DEFAULT_ADAPTIVE_THESIS = NOT_PROVEN
POSSIBLE_FUTURE_MODE = HIGH_COST_OPTIONAL_MAX_MODE_HYPOTHESIS
```

Portfolio results cannot satisfy D-versus-C GO unless portfolio execution was the preregistered D definition and its full duplicated cost/latency/effect accounting is included. The initial H0 D arm should prefer routed single-recipe execution.

## 21. Verifier-overhead guardrail

Verifier cost is part of harness cost.

If verifier work exceeds 25% of total arm cost or wall time, the result must separately report whether that overhead caused a measurable reduction in false completion or accepted task error.

If verifier overhead exceeds 25% without either:

- a required hard safety benefit; or
- a predeclared measurable quality/false-completion benefit,

the Verifier Fabric hypothesis must be narrowed rather than assumed valuable by construction.

## 22. Decision matrix

### GO_STATIC_RESEARCH

Set only if C passes either the static success-lift path or static efficiency path against both A and B and all hard gates pass.

### GO_ADAPTIVE_RESEARCH

Set only if:

```text
GO_STATIC_RESEARCH = YES
AND
D passes adaptive success-lift or efficiency path versus C
AND
all hard gates pass
```

### NARROW_TO_STATIC_COMPILATION

Set when C passes but D does not.

Retain hypotheses around:

```text
Proof-Carrying Harness Recipe
static task/environment compilation
minimum sufficient tool/context surface
Verifier Fabric only where earned
```

Do not promote adaptive routing, Harness Gym, or self-evolution as default architecture.

### PORTFOLIO_ONLY

Set when routed D fails but an explicitly measured sibling portfolio shows useful value. Treat as a later optional high-cost mode hypothesis, not default adaptivity.

### KILL_STANDALONE_HARNESS_PROGRAM

Set when C fails both static GO paths against either required baseline after valid confirmatory execution, unless a preregistered protocol defect invalidates the experiment as a whole.

If killed:

- retain isolated useful mechanics only where they fit existing WePLD roadmap slices;
- do not preserve HIR/router/gym/evolution complexity merely because it was designed;
- do not reinterpret exploratory subgroups as program-level success.

## 23. Additional kill / narrow conditions

The architecture must be killed or narrowed when any of the following is demonstrated:

- screening gains disappear on the confirmatory holdout;
- benefit depends on benchmark/task identity leakage forbidden by this contract;
- improvements are primarily post-hoc recipe search rather than preregistered routing/compilation;
- adaptive routing does not generalize across the required model-family boundary;
- complexity cost dominates useful lift;
- the safe authority boundary prevents the adaptive mechanism from functioning in real tasks;
- deterministic verification overhead dominates practical value without earning a measurable safety/quality benefit;
- a simpler baseline achieves equivalent verified success and efficiency within the non-inferiority envelope.

## 24. Evidence packet required for any H0 decision

No GO/NARROW/KILL result is valid without a durable evidence packet containing at minimum:

```text
contract_blob_and_commit
frozen_task_manifest
frozen_model_manifest
frozen_environment_manifest
frozen_verifier_manifest
frozen_recipe_manifest
run_manifest
raw_result_rows
artifact_links_or_hashes
failure_records
budget_usage
paired_analysis_code_and_version
bootstrap_seed_or_reproducibility_metadata
pooled_results
model_family_strata
task_archetype_strata
hard_gate_accounting
infra_failure_accounting
excluded_or_invalid_task_evidence
final_decision_derivation
```

The analysis must be reproducible from raw retained evidence without relying on narrative interpretation.

## 25. Research references informing methodology

The following are methodology references only. They are not source admission, dependency admission, or architectural authority.

```text
arXiv:2607.22585
The Scaffold Effect in Coding Agents: Harness Choice as a Hidden Variable in Model Evaluation

arXiv:2606.08529
Scaffold Effects on GAIA: A Controlled Comparison

arXiv:2605.27922
Harness-Bench: Measuring Harness Effects on Frontier LLM Agent Performance

Harbor
Containerized agent-evaluation / environment framework reference
```

Exact versions, authorship metadata, repository pins, rights, and reproduction details must be verified separately before publication-grade citation or code-level acquisition.

## 26. Donor boundary during H0

H0 does not authorize importing donor code.

Before any donor mechanism enters an experimental implementation:

```text
DEFINE_EXACT_CAPABILITY
SELECT_TOP_2_OR_3_DONORS_ONLY
PIN_EXACT_REVISION
VERIFY_LICENSE_RIGHTS_ATTRIBUTION_REDISTRIBUTION
INSPECT_TESTS_FAILURES_SECURITY_PORTABILITY_MAINTENANCE
DEFINE_WEPLD_OWNED_CONTRACT
DEFINE_REPLACEMENT_EXIT_PATH
```

Tests, fixtures, failure corpora, and behavioral mechanics should be preferred over dependency adoption when they can answer the research question with less lock-in.

## 27. Freeze and amendment rule

This document is the H0 v1 research contract.

Before the first confirmatory outcome, purely operational clarifications may be proposed, but any change to a decision-affecting field must create a new explicit protocol version and a recorded rationale.

After the first confirmatory outcome:

```text
NO_THRESHOLD_EDIT
NO_ARM_REDEFINITION
NO_TASK_FILTER_EDIT
NO_MODEL_FILTER_EDIT
NO_METRIC_SWAP
NO_BUDGET_REWRITE
NO_EXCLUSION_RULE_REWRITE
NO_VERIFIER_ACCEPTANCE_REWRITE
NO_STATISTICAL_RULE_REWRITE
```

A new protocol version may be created, but old confirmatory outcomes cannot be reused as promotion evidence under the new protocol.

## 28. Current authority state

```text
HARNESS_PROGRAM = GO_FOR_RESEARCH_ONLY
H0_RESEARCH_CONTRACT = FROZEN_ON_RESEARCH_BRANCH
H0_EXPERIMENT_EXECUTION = NOT_STARTED
HARNESS_IMPLEMENTATION = NOT_STARTED
DONOR_CODE_IMPORT = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
SELF_EVOLUTION = NOT_STARTED
S1_013_PLUS = NOT_STARTED
```

The next research action after this contract is verified is capability-specific donor pin/rights/security reconnaissance for only the strongest 2–3 candidates needed to build the minimum falsification surface.
