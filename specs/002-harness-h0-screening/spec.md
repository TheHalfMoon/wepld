# Specification — Harness H0 Screening Falsification

## Problem

The WePLD Harness Program has a strong research thesis but no execution evidence yet. Without a bounded screening slice, the project could drift into building a large agent framework, adaptive router, HIR, self-evolution stack, or evaluation platform before proving that harness compilation adds measurable verified value.

H0-SCREEN must therefore validate the minimum experimental machinery and collect representative screening evidence while preserving one central rule:

> Screening is allowed to falsify the design and repair experiment plumbing; it is not allowed to promote the Harness Program or authorize production implementation.

## Research-visible outcome

A successful H0-SCREEN slice produces a content-addressed evidence packet showing that:

- the runner/evidence plane passes all required synthetic qualification fixtures;
- A/B/C/D recipes are deterministic and conform to their frozen boundaries;
- D uses only disjoint calibration evidence and cannot memorize screening identities;
- 40 distinct screening tasks can be executed under common verifier, budget, and authority contracts;
- every trial has complete immutable identity and normalized evidence;
- runner overhead, failure rate, cleanup burden, and operational adequacy are measurable;
- hard-gate incidents are explicit and cannot be hidden by aggregate performance;
- screening evidence is sufficient to decide whether the minimum runner is adequate for later confirmatory planning.

The outcome may also be `SCREENING_BLOCKED`, `RUNNER_REPLACE_OR_REPAIR`, or `H0_DESIGN_REPAIR_REQUIRED`. None of these is silently converted to GO.

## Functional requirements

### FR-001 — Screening-only phase

The experiment phase MUST be `H0-SCREEN`.

```text
DISTINCT_TASKS = 40
ATTEMPTS_PER_TASK_ARM_MODEL = 1
PROMOTION_AUTHORITY = NONE
```

No H0-confirmatory task may be executed under this slice.

### FR-002 — Exact four-arm vocabulary

The screening implementation MUST expose exactly these conceptual arms:

```text
A = MINIMAL_BASELINE
B = FIXED_RICH_BASELINE
C = WEPLD_STATIC_COMPILED_RECIPE
D = WEPLD_ADAPTIVE_ROUTED_RECIPE
```

No fifth production or portfolio arm may be introduced.

### FR-003 — Arm A boundary

A MUST remain the minimum generic execution loop:

- bounded current instruction/context;
- minimum task-required file/read/write/execute tool surface;
- no separate general planner;
- final-only verifier cadence except task-requested tests;
- one bounded error-aware continuation path;
- stop on budget exhaustion, objective-verifier success, or deterministic unrecoverable failure.

A MUST NOT gain model routing, general dynamic context compilation, subagent portfolios, harness search, or self-evolution.

### FR-004 — Shared B/C/D component library

B, C, and D MUST select from one frozen option library containing only:

```text
ContextPolicy
ToolSurfacePolicy
PlanningPolicy
VerifierCadencePolicy
RecoveryPolicy
StopPolicy
```

D cannot win by receiving components unavailable to B/C.

### FR-005 — B fixed-rich semantics

B MUST use one globally fixed richer recipe across supported screening model/task cells. It MUST NOT route by model family, task archetype, benchmark task identity, or observed outcomes.

### FR-006 — C static compiler semantics

C MUST be deterministic for identical inputs and may use only:

```text
TaskFingerprint
EnvironmentFingerprint
BudgetRiskEnvelope
```

C MUST NOT inspect model identity/family/profile, benchmark task IDs, gold answers, or H0 outcome history.

### FR-007 — D adaptive compiler semantics

D MUST use the exact C inputs plus a frozen `ModelCapabilityProfile` derived mechanically from a calibration suite that is:

```text
DISJOINT_FROM_H0_SCREEN = YES
DISJOINT_FROM_H0_CONFIRM = YES
PROMOTION_EVIDENCE = NO
```

D MUST NOT use an LLM router, dynamic code generation, model-written recipes, self-evolution, harness search, or sibling portfolios.

### FR-008 — Recipe compiler conformance

Before H0-SCREEN tasks, deterministic conformance fixtures MUST prove at least R01-R07:

- identical C input -> identical RecipeManifest hash;
- C ignores model identity;
- D may differ only through frozen model-profile routing rules;
- unknown component selection fails closed;
- authority expansion fails closed;
- budget expansion fails closed;
- raw benchmark/task-ID special cases are prohibited.

### FR-009 — Synthetic runner qualification

Before any H0-SCREEN task, the runner/evidence implementation MUST pass F01-F16 from the canonical screening-fixture contract, covering:

```text
PASSING_TASK
FAILING_TASK
FALSE_COMPLETION
TIMEOUT
PROCESS_CRASH
MALFORMED_OUTPUT
MISSING_ARTIFACT
OVERSIZED_STDOUT_STDERR
VERIFIER_CRASH
CLEANUP_FAILURE
DENIED_NETWORK_ATTEMPT
UNEXPECTED_EXTERNAL_EGRESS_IF_INSTRUMENTABLE
SECRET_REDACTION_BOUNDARY
PARALLEL_ISOLATION
RETRY_POLICY
RUN_ORDER_IDENTITY
```

The fixture pass gate requires zero unexplained evidence mismatch, accepted unauthorized effect, secret-canary leak to public evidence, or cross-trial contamination.

### FR-010 — Content-addressed manifests

Decision-relevant experiment/task/model/recipe/environment/verifier/budget/effect identities MUST use frozen canonical serialization and content hashes. The implementation MUST reject malformed, missing, or identity-inconsistent manifests before trial execution.

### FR-011 — Trial identity

Each trial MUST bind the full comparison cell, including experiment, task, model, recipe, environment, verifier, attempt number, and seed where supported. Schedule position MUST NOT change TrialIdentity.

### FR-012 — Trial state machine

The future implementation MUST preserve:

```text
CREATED -> PREPARED -> RUNNING -> COLLECTING -> VERIFYING -> FINALIZED
```

with exceptional terminals including `INFRASTRUCTURE_FAILED`, `POLICY_BLOCKED`, and `EVIDENCE_INCOMPLETE`.

Only the WePLD evidence finalizer may emit `FINALIZED`.

### FR-013 — Final verifier authority

Runner/model/harness completion is never equivalent to verified success. `verified_success` MUST be mechanically derived from the frozen final objective verifier plus evidence-completeness and hard-gate semantics.

Verifier failure MUST NOT fall back to a model/harness completion claim.

### FR-014 — Effect and egress accounting

Every trial MUST bind an `EffectEnvelope`. All arms in a paired comparison receive the same maximum authority/effect envelope.

At minimum, account separately for:

```text
MODEL_PROVIDER_EGRESS
TASK_ENVIRONMENT_EGRESS
RUNNER_CONTROL_EGRESS
VERIFIER_EGRESS
OBSERVABILITY_EGRESS
```

Task-environment network is deny-by-default. Merge/deploy/publish authority is denied.

### FR-015 — Budget fairness

All paired arms MUST receive the same maximum wall/token/money budgets where enforceable. An arm may consume less; it may not self-extend its budget.

### FR-016 — Failure taxonomy

The implementation MUST preserve the frozen H0 failure classes and retain original run evidence. Harness-induced crashes, loops, malformed tool requests, context failures, or verifier misuse are outcomes, not infrastructure exclusions.

### FR-017 — One-attempt and pre-attempt infrastructure semantics

Each task/arm/model cell MUST have exactly one started screening attempt. Task, harness, model, budget, verifier, and any infrastructure/provider failure after attempt start MUST NOT be retried.

A shared infrastructure/provider readiness failure MAY be rescheduled at most once only when independently evidenced before attempt start. It MUST be recorded as a `PRE_ATTEMPT_INFRASTRUCTURE_OBSERVATION`, MUST NOT create a TrialRecord or consume the cell's single attempt, and MUST NOT alter any frozen cell identity, recipe, verifier, budget, effect envelope, or run-order rule. A second pre-attempt readiness failure blocks the affected batch rather than creating repeated reschedules.

The attempt-start boundary is the first transition into task/model/harness execution after manifest validation and shared readiness checks. Once crossed, every terminal condition remains the cell's sole screening outcome.

### FR-018 — Bounded local concurrency

The runner MAY use a fixed bounded worker pool. It MUST NOT create arm-specific concurrency advantage, shared mutable task workspaces, or distributed scheduling. Run order must be balanced across arms/models/tasks where practical.

### FR-019 — Runner adequacy metrics

H0-SCREEN MUST measure:

```text
runner_setup_failures
container_start_failures
cleanup_failures
artifact_capture_failures
usage_capture_failures
verifier_invocation_failures
median_runner_overhead_seconds
p95_runner_overhead_seconds
median_runner_overhead_fraction
host_resource_contention_events
manual_recovery_events
operator_minutes_per_100_trials
runner_caused_invalid_or_incomplete_trial_rate
```

For every started screening trial, timing MUST be derived from non-overlapping monotonic intervals:

```text
trial_wall_seconds = finalization_end - attempt_start
runner_overhead_seconds = sum(exclusive runner-controlled orchestration intervals)
runner_overhead_fraction = runner_overhead_seconds / trial_wall_seconds
```

Runner-controlled orchestration includes runner validation after attempt start, workspace/container/process orchestration, observation/control bookkeeping, artifact/evidence capture orchestration, cleanup, canonical serialization, and TrialRecord finalization. It excludes waiting time attributable to task code, model/provider execution, and objective-verifier execution.

Pre-attempt infrastructure observations are excluded from trial-overhead aggregation because no screening attempt has started; they are reported separately. All started trials, including ordinary failures and runner-caused invalid/incomplete outcomes, are included. Missing/nonpositive wall timing or unaccountable runner timing makes runner adequacy evidence incomplete and MUST NOT be silently excluded.

For the final stable screening batch:

```text
MEDIAN_RUNNER_OVERHEAD_FRACTION = median(per-started-trial runner_overhead_fraction)
P95_RUNNER_OVERHEAD_SECONDS = nearest-rank p95(per-started-trial runner_overhead_seconds)
```

Aggregation is across all started task/arm/model trials with no per-arm, per-model, per-cell, or success-only pre-aggregation.

These metrics decide runner adequacy only; they do not alter Harness thesis GO thresholds.

### FR-020 — Screening outputs

The final screening packet MUST contain at least:

```text
A/B/C/D screening metrics
failure taxonomy counts
recipe-selection traces
model calibration profiles
runner adequacy metrics
runner-caused invalid/incomplete rate
runner overhead
operator recovery burden
hard-gate incidents
component-level defects
normalized trial export
```

### FR-021 — No confirmatory claim

The screening implementation MUST NOT compute or publish `GO_STATIC`, `GO_ADAPTIVE`, or `NARROW_TO_STATIC` as an H0 promotion decision. Those outcomes require the separately frozen H0-CONFIRM protocol.

### FR-022 — No product or roadmap mutation

H0-SCREEN MUST NOT modify S1 authoritative tasks, start S1-013, alter P0+S1..S10 roadmap authority, mutate the frozen 402-source registry, or integrate a Harness runtime into production WePLD.

## Security and trust requirements

- No real credentials in fixtures, Git, manifests, normalized evidence, or public logs.
- Synthetic canary secrets only for redaction tests.
- Host filesystem mounts are minimum-sufficient and task-manifested.
- Container privileged mode is denied.
- Host Docker/container socket is not exposed inside the task environment.
- External side effects are none by default.
- Missing evaluator/effect/evidence coverage cannot become PASS.
- No silent provider/model/worker substitution.
- Candidate planning/spec text does not create authority before canonicalization.

## Non-goals

- H0-CONFIRM execution or promotion decision;
- Harbor integration/adoption;
- distributed/cloud execution;
- generalized HIR/plugin architecture;
- model-training flywheel;
- autonomous harness mutation;
- production model routing;
- product UI;
- persistent database/service;
- source-registry revision;
- S1-013 or later roadmap execution.
