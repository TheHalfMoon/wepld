# Tasks — Harness H0 Screening Falsification

```text
FEATURE = 002-harness-h0-screening
TASK_AUTHORITY = COORDINATION_ONLY
IMPLEMENTATION_AUTHORITY = NONE_UNTIL_EXPLICIT_TASK_PREREQUISITE_IS_PROVEN
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

Task state is repository coordination, not effect authority. A task may move only when its explicit canonical prerequisites are proven. No task in this file can self-authorize implementation, dependency admission, external egress, or completion.

## Canonicalization semantics

H0-001 and H0-002 are necessarily **pre-canonicalization bootstrap steps** for this file itself. This `tasks.md` becomes execution-authoritative only after H0-002 is merged and post-merge refreeze is proven.

Therefore:

```text
PRE_CANONICALIZATION_NEXT = H0-001
CANONICAL_ENTRYPOINT_AFTER_H0_002 = H0-003
```

After this package is canonical, H0-001/H0-002 are historical prerequisites and MUST NOT be reopened merely because their instructions remain preserved here.

## Governance / planning canonicalization

### H0-001 — Bootstrap H0 Spec-Kit integrity policy

**State in this package:** PRE-CANONICALIZATION PREREQUISITE

Create a dedicated trusted-bootstrap policy that permits only:

1. its own bounded policy/workflow bootstrap; and
2. after canonical activation, one exact content-addressed `specs/002-harness-h0-screening/` planning package.

Required invariants:

```text
HARNESS_H0_SPEC_KIT_AUTHORIZED = EXACT_ONE_TIME_PACKAGE
HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED = NO
HARNESS_SOURCE_ADMISSION = NONE
HARNESS_DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

The policy must freeze the package after canonicalization and delegate unrelated changes to the prior canonical Harness research policy.

**Exit:** policy PR merged on exact reviewed head + post-merge foundation activation proven.

### H0-002 — Canonicalize exact H0 Spec Kit package

**State in this package:** PRE-CANONICALIZATION SELF-CANONICALIZATION STEP / BLOCKED_ON_H0_001

Add exactly the frozen H0 planning files authorized by H0-001, with no source/runtime/dependency/roadmap changes.

Required gates:

- trusted-base admission in candidate-data-only mode;
- candidate exact-head foundation integrity;
- exact-head secret/private-data/egress preflight;
- independent correctness/engineering review;
- finding reconciliation;
- final race check;
- exact-head merge;
- post-merge refreeze proof.

**Exit:** `H0_SPEC_KIT = CLOSED_CANONICAL_PROVEN`.

### H0-003 — Reconcile canonical planning status

**State:** CANONICAL_ENTRYPOINT / REQUIRES_H0_002

Verify that canonical main contains exact planned blobs and that no excluded Harness research handoff, product source, dependency manifest, or S1-013 mutation entered through the planning transition.

Also bind the exact H0-001 policy activation and H0-002 planning-package refreeze evidence externally in GitHub/repository evidence without rewriting a purported final PR head into the historical planning blobs.

**Exit:** planning identity packet recorded and H0-004 may start.

## Ponytail / Source Acquisition closeout

### H0-004 — Ponytail FULL closeout

**State:** BLOCKED_ON_H0_003

Re-run/verify Ponytail FULL against the canonical Spec Kit package and current repository/source truth. Confirm that every proposed abstraction/dependency still earns its place.

Must explicitly challenge:

```text
GENERAL_HIR
LLM_ROUTER
MEMORY_SYSTEM
MULTI_AGENT_PORTFOLIO
SELF_EVOLUTION
HARNESS_SEARCH
DISTRIBUTED_SCHEDULER
DATABASE/SERVICE
CLOUD_PROVIDER_SDK
HARBOR_SCREENING_DEPENDENCY
MODEL_PROVIDER_SDK
CUSTOM_CRYPTO/HASH_IMPLEMENTATION
```

**Exit:** `PONYTAIL_FULL = COMPLETE_FOR_IMPLEMENTATION_BOUNDARY` or implementation remains blocked with documented reductions/gaps.

### H0-005 — Qualify Rust toolchain reuse for H0

**State:** BLOCKED_ON_H0_003

Determine whether the exact canonical Rust toolchain evidence already used by S1 can be reused for H0 control/evidence implementation. Reverify exact source/release identity and H0 build requirements.

**Constraint:** prior S1 admission is evidence, not automatic H0 admission.

### H0-006 — Qualify typed serialization/canonicalization substrate

**State:** BLOCKED_ON_H0_003

Select the minimum typed serialization package set and freeze WePLD canonical serialization rules for all decision-relevant H0 manifests/records.

Must prove deterministic canonical bytes independent of map iteration/order and reject unsupported/ambiguous values.

### H0-007 — Qualify SHA-256 implementation

**State:** BLOCKED_ON_H0_003

Select an established commodity SHA-256 implementation; do not hand-write cryptographic hashing. Pin exact source/package/version/features and inspect maintenance/security/license/exit strategy.

### H0-008 — Qualify local execution/container boundary

**State:** BLOCKED_ON_H0_003

Define the exact local process/container execution mechanism for H0-SCREEN.

Requirements:

- narrow replaceable adapter;
- no cloud SDK;
- no distributed scheduler;
- task network denial/instrumentation where claimed;
- minimum host mounts;
- no privileged container mode;
- no host container-engine socket inside task;
- deterministic cleanup/isolation evidence;
- exact runtime/CLI identity captured.

### H0-009 — Qualify model-provider boundary

**State:** BLOCKED_ON_H0_003

Define a replaceable model invocation boundary without silently admitting a broad provider SDK.

Requirements:

- exact model/provider/serving identity fields;
- no silent provider/model fallback;
- credentials by reference and execution-time injection only;
- model-serving egress separated from task egress;
- usage capture limitations explicit.

### H0-010 — Source Acquisition final reconciliation

**State:** BLOCKED_ON_H0_004..H0_009

Create exact H0 component admission evidence, dependency/feature inventory, license/notice disposition, advisory/SBOM evidence where applicable, and replacement/exit paths.

**Exit gate:**

```text
SOURCE_ACQUISITION_CHECK = PASS
H0_DIRECT_COMPONENT_SET = EXACT_AND_MINIMUM
HARBOR_ADMISSION = NONE
PRODUCT_RUNTIME_ADMISSION = NONE
```

No implementation policy may be proposed before H0-010 passes.

## Separate implementation authorization

### H0-011 — Design H0-SCREEN implementation integrity policy

**State:** BLOCKED_ON_H0_010

Create a dedicated policy that authorizes only the exact minimum source/config/fixture/dependency surface established by canonical planning + Ponytail + Source Acquisition.

Must preserve:

```text
PRODUCT_HARNESS_INTEGRATION = NO
H0_CONFIRMATORY_EXECUTION = NO
HARBOR_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

### H0-012 — Qualify and activate implementation policy

**State:** BLOCKED_ON_H0_011

Use trusted-bootstrap procedure: exact-head deterministic qualification, applicable security accounting, egress preflight, independent review, reconciliation, exact merge, post-merge activation proof.

**Exit:** `H0_SCREEN_IMPLEMENTATION_AUTHORIZED = EXACT_BOUNDED_SURFACE`.

## Evidence/control implementation — blocked until H0-012

### H0-013 — Canonical serialization and identity core

**State:** NOT_STARTED / REQUIRES_H0_012

Implement canonical bytes, SHA-256 identities, domain separation, manifest validation, and deterministic TrialIdentity.

### H0-014 — H0 manifest and policy types

**State:** NOT_STARTED / REQUIRES_H0_012

Implement typed minimum representations for ExperimentManifest, TaskManifest, ModelManifest, RecipeManifest, EnvironmentManifest, VerifierManifest, BudgetPolicy, EffectEnvelope, and the frozen attempt-start/pre-attempt-readiness policy.

### H0-015 — Evidence record/finalizer core

**State:** NOT_STARTED / REQUIRES_H0_012

Implement append-oriented raw observations, artifacts, usage/effects/verifier/failure records, trial state history, evidence completeness, hard-gate derivation, and mechanical `verified_success` finalization.

The runner cannot author final success.

## Recipe and calibration implementation — blocked until H0-012

### H0-016 — Frozen component option library

**State:** NOT_STARTED / REQUIRES_H0_012

Implement only ContextPolicy, ToolSurfacePolicy, PlanningPolicy, VerifierCadencePolicy, RecoveryPolicy, and StopPolicy options frozen by the canonical research boundary.

### H0-017 — Arm A and B constructors

**State:** NOT_STARTED / REQUIRES_H0_012

Implement A minimal and one fixed B recipe. B must remain globally fixed across screening model/task cells.

### H0-018 — C static compiler

**State:** NOT_STARTED / REQUIRES_H0_012

Implement deterministic task/environment/budget-risk compilation with explicit denial of model/profile/task-ID/outcome-history inputs.

### H0-019 — D adaptive compiler

**State:** NOT_STARTED / REQUIRES_H0_012

Implement deterministic C+ModelCapabilityProfile routing only. No LLM router, code generation, self-evolution, portfolio, or unknown component selection.

### H0-020 — RecipeDecisionTrace and conformance suite

**State:** NOT_STARTED / REQUIRES_H0_012

Implement decision-fact traces and R01-R07. All recipe conformance fixtures must pass before H0-SCREEN task execution.

### H0-021 — Disjoint calibration suite

**State:** NOT_STARTED / REQUIRES_H0_012

Implement frozen micro-capability calibration fixtures/profile derivation, mechanically hashed and disjoint from screening/confirmatory identities.

## Runner implementation — blocked until H0-012

### H0-022 — Minimal RunnerAdapter

**State:** NOT_STARTED / REQUIRES_H0_012

Implement only validate/prepare/start/observe/stop/collect/cleanup behavior required by the evidence contract. No database, remote service, cloud SDK, plugin marketplace, or workflow engine.

### H0-023 — Bounded concurrency and workspace isolation

**State:** NOT_STARTED / REQUIRES_H0_012

Add one fixed bounded worker-pool policy, isolated trial workspaces, balanced scheduling, and resource-contention accounting.

### H0-024 — F01-F16 synthetic runner fixtures

**State:** NOT_STARTED / REQUIRES_H0_012

Implement and pass all required synthetic runner/evidence fixtures, including F15 proving that post-start failures cannot be retried, one pre-attempt shared-readiness failure may be rescheduled at most once without creating a TrialRecord/attempt, and a second readiness failure blocks the affected batch.

Hard prerequisite for any real screening task:

```text
ALL_REQUIRED_FIXTURES = PASS
UNEXPLAINED_EVIDENCE_MISMATCH = 0
ACCEPTED_UNAUTHORIZED_EFFECT = 0
SECRET_CANARY_LEAK_TO_PUBLIC_EVIDENCE = 0
CROSS_TRIAL_CONTAMINATION = 0
```

## Screening freeze and execution — blocked until prior gates

### H0-025 — Freeze exact 40-task screening manifest

**State:** BLOCKED_ON_H0_020,H0_021,H0_024

Select/freeze exactly 40 screening tasks, archetypes, fixture hashes, environments, verifiers, allowed effects, and eligibility notes. Identities must be disjoint from future confirmatory tasks.

### H0-026 — Freeze exact screening model set

**State:** BLOCKED_ON_H0_021

Freeze eligible model/provider identities/settings and their calibration profiles. No silent substitution after freeze.

### H0-027 — Freeze screening budgets/attempt/failure/run-order/overhead policy

**State:** BLOCKED_ON_H0_025,H0_026

Freeze before the first real screening outcome:

- per-task maximum budgets;
- exact one-started-attempt-per-task/arm/model rule;
- attempt-start boundary;
- pre-attempt shared-readiness observation/reschedule policy with at most one reschedule and batch block on a second readiness failure;
- failure taxonomy;
- concurrency;
- balanced run-order algorithm/seed;
- expected started-trial count;
- runner-overhead timing boundaries, inclusion/exclusion rules, formula, and deterministic batch aggregation.

No post-start retry or replacement is permitted.

### H0-028 — Execute H0-SCREEN

**State:** BLOCKED_ON_H0_025..H0_027

Run exactly one started attempt per task/arm/model cell using common runner plumbing. Preserve every started trial and evidence classification as the cell's sole outcome. Pre-attempt shared-readiness failures are retained separately, may be rescheduled at most once without creating a TrialRecord or consuming the cell attempt, and a second readiness failure blocks the affected batch. No confirmatory tasks and no GO decision.

### H0-029 — Produce normalized screening evidence

**State:** BLOCKED_ON_H0_028

Emit the runner-neutral TrialRecord set, separately retained pre-attempt infrastructure observations, normalized export, screening metrics, calibration profiles, recipe traces, failure counts, hard-gate incidents, evidence-completeness accounting, and mechanically recomputable runner-overhead timing records.

### H0-030 — Evaluate runner adequacy

**State:** BLOCKED_ON_H0_029

For every started trial compute:

```text
trial_wall_seconds = monotonic(finalization_end - attempt_start)
runner_overhead_seconds = sum(non-overlapping exclusive runner-controlled orchestration intervals)
runner_overhead_fraction = runner_overhead_seconds / trial_wall_seconds
```

Include every started trial in aggregation, including ordinary failures and runner-caused invalid/incomplete outcomes. Exclude pre-attempt infrastructure observations from trial-overhead aggregation and report them separately. Missing/nonpositive wall timing or unaccountable runner timing fails runner-evidence completeness rather than removing the trial.

Across all started trials in the final stable batch, with no per-arm/model/cell/success-only pre-aggregation:

```text
MEDIAN_RUNNER_OVERHEAD_FRACTION = median(per-started-trial runner_overhead_fraction)
P95_RUNNER_OVERHEAD_SECONDS = nearest-rank p95(per-started-trial runner_overhead_seconds)
```

Then apply the frozen runner criteria:

```text
INVALID_OR_INCOMPLETE_RATE <= 2_PERCENT
MEDIAN_RUNNER_OVERHEAD_FRACTION <= 15_PERCENT
MANUAL_RECOVERY <= 2_OPERATOR_HOURS_PER_100_COMPLETED_TRIALS
NO_DISTRIBUTED_SCHEDULER_REQUIRED
NO_NEW_CLOUD_PROVIDER_BACKEND_REQUIRED
EVIDENCE_CONTRACT_FULLY_SATISFIED
```

### H0-031 — Independent screening review and closeout

**State:** BLOCKED_ON_H0_029,H0_030

Run all applicable deterministic/security/reviewer gates on the exact screening evidence/implementation head, reconcile findings, and record one bounded screening closeout state.

Allowed closeout states:

```text
SCREENING_EVIDENCE_READY_FOR_CONFIRMATORY_PLANNING
RUNNER_REPAIR_REQUIRED
RUNNER_REPLACEMENT_QUALIFICATION_REQUIRED
H0_DESIGN_REPAIR_REQUIRED
H0_RESEARCH_KILL_OR_NARROW_CANDIDATE
```

None authorizes product Harness implementation or S1-013.

## Global prohibition

Until H0-012 is canonical and activation-proven, tasks H0-013 through H0-031 are coordination-only and MUST NOT be started.

```text
IF_THIS_PACKAGE_IS_NOT_YET_CANONICAL:
  NEXT = H0-001

IF_H0_SPEC_KIT_CLOSED_CANONICAL_PROVEN:
  NEXT = H0-003

H0_SCREEN_IMPLEMENTATION = NOT_STARTED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
S1_013_PLUS = NOT_STARTED
```
