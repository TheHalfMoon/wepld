# Clarifications — Harness H0 Screening Falsification

All decisions below are bounded to `H0-SCREEN`. They do not reopen the canonical V2.2 roadmap, authorize product Harness implementation, or start S1-013+.

## C-001 — Is H0-SCREEN a roadmap slice?

**Decision:** no.

`ROADMAP_SLICE = NONE`. H0-SCREEN is a separately governed research-falsification program. It may inform later roadmap proposals, but it does not mutate P0+S1..S10 and cannot start S1-013.

## C-002 — Can screening satisfy H0 GO?

**Decision:** no.

```text
DISTINCT_TASKS = 40
ATTEMPTS_PER_TASK_ARM_MODEL = 1
PROMOTION_AUTHORITY = NONE
```

Screening validates experiment plumbing, variance/cost ranges, failure taxonomy, recipe semantics, and runner adequacy. `GO_STATIC`, `GO_ADAPTIVE`, and `NARROW_TO_STATIC` remain confirmatory-only outcomes.

## C-003 — What is the initial runner strategy?

**Decision:** `WEPLD_MINIMAL_LOCAL_RUNNER` remains the preferred H0-SCREEN runner if later implementation is separately authorized.

The runner is a replaceable data plane, not completion or promotion authority. Harbor remains a qualified reference/conditional confirmatory runner candidate and is not an H0-SCREEN dependency.

## C-004 — Does “local runner” require a new container platform?

**Decision:** no.

The runner may wrap an already available local process/container boundary through a narrow adapter. It MUST NOT embed a distributed scheduler, cloud-provider abstraction, remote job service, remote artifact server, or container platform.

Synthetic qualification fixtures may use controlled local processes where that is sufficient to test runner/evidence semantics. Real screening tasks requiring stronger isolation must use a separately qualified local container/runtime boundary before execution.

## C-005 — What language should authoritative H0 control/evidence code use?

**Decision:** Rust-first is the planning preference for trusted H0 control/evidence logic, consistent with canonical `AGENTS.md`.

This is not dependency/source admission. Exact toolchain/crates remain subject to Source Acquisition Check and a separate implementation authorization.

Non-authoritative synthetic fixture programs MAY use minimal scripts or executables when their bytes and expected behavior are frozen as test inputs. A fixture language does not become H0 authority.

## C-006 — Can the H0 runner reuse S1 dependency admission automatically?

**Decision:** no.

Existing S1 component evidence may be reused as prior evidence, but `EXACT_S1_GRAPH` is not blanket H0 admission. Any direct H0 use of Rust crates, external CLIs, container engines, or model-provider SDKs requires an H0-specific acquisition disposition or an explicit determination that no new dependency is introduced.

## C-007 — Is an SDK required for model providers?

**Decision:** not by planning default.

Provider/model integration is behind a replaceable boundary. Prefer the smallest already-admitted or separately qualified mechanism. No provider SDK is admitted by this Spec Kit package.

No silent provider/model fallback is permitted.

## C-008 — What is the component vocabulary?

**Decision:** H0 v1 is limited to:

```text
ContextPolicy
ToolSurfacePolicy
PlanningPolicy
VerifierCadencePolicy
RecoveryPolicy
StopPolicy
```

General memory, multi-agent delegation, sibling portfolios, self-evolution, harness search, HIR plugins, product authority engines, and product UI are excluded.

## C-009 — What is the shared B/C/D library rule?

**Decision:** B, C, and D select from the same predeclared option library.

```text
B_COMPONENT_LIBRARY == C_COMPONENT_LIBRARY == D_COMPONENT_LIBRARY
```

A is intentionally smaller and is not forced to carry the richer library.

## C-010 — May C route by model identity?

**Decision:** no.

C may use only `TaskFingerprint`, `EnvironmentFingerprint`, and `BudgetRiskEnvelope`. Model family, model ID, model profile, benchmark task ID, hidden answer, and H0 outcome history are prohibited C inputs.

## C-011 — How does D obtain model-awareness?

**Decision:** D uses a frozen `ModelCapabilityProfile` produced mechanically from a synthetic/micro-capability calibration suite disjoint from H0-SCREEN and H0-CONFIRM.

A provider/model revision that materially changes capability requires a new calibration profile identity. D may route only through frozen rules and the shared B/C/D library.

## C-012 — Is D an LLM/meta-agent router?

**Decision:** no for H0 v1.

```text
D_SELF_EVOLUTION = NO
D_DYNAMIC_CODE_GENERATION = NO
D_SIBLING_PORTFOLIO = NO
D_MODEL_WRITES_ITS_OWN_RECIPE = NO
D_LLM_ROUTER = NO
```

The first adaptive thesis is deterministic evidence-driven model-aware routing.

## C-013 — How are recipe decisions explained?

**Decision:** C and D emit `RecipeDecisionTrace` records containing input fingerprint hashes, evaluated rule IDs, selected/rejected option IDs with reason codes, applied budget/authority constraints, and the final RecipeManifest hash.

No chain-of-thought is requested or stored.

## C-014 — Who decides verified success?

**Decision:** only the WePLD evidence finalizer, using the frozen final objective verifier plus evidence-completeness and hard-gate policy.

Runner/model/harness completion maps to observations. Runner execution completion maps no further than `COLLECTING` until verification/finalization succeeds.

## C-015 — What happens when the verifier crashes?

**Decision:** record `VERIFIER_FAILURE`; `verified_success != true`. There is no fallback to model/harness claims or reviewer opinion.

## C-016 — How are retries handled?

**Decision:** each task/arm/model cell has exactly one started screening attempt. Task, harness, model, budget, verifier, and post-start infrastructure/provider failures are never retried.

A shared infrastructure/provider failure may be rescheduled at most once only when it is independently evidenced **before the cell attempt starts**. Such an event is recorded as `PRE_ATTEMPT_INFRASTRUCTURE_OBSERVATION`, does not create a TrialRecord, does not consume the cell's single attempt, and may not change the frozen task/model/recipe/environment/verifier/budget/effect identities. If the rescheduled readiness check fails again, the affected batch is `SCREENING_BLOCKED`; the cell is not repeatedly rescheduled.

The attempt-start boundary is the first transition into task/model/harness execution after manifest validation and shared readiness checks. Once that boundary is crossed, every terminal condition is retained as the cell's sole screening outcome.

## C-017 — What network policy applies?

**Decision:** task-environment network is deny-by-default. Model-serving traffic is a separately accounted channel when required.

Record independently:

```text
MODEL_PROVIDER_EGRESS
TASK_ENVIRONMENT_EGRESS
RUNNER_CONTROL_EGRESS
VERIFIER_EGRESS
OBSERVABILITY_EGRESS
```

No arm may receive a broader network/effect envelope than another paired arm.

## C-018 — Can secrets appear in manifests/logs?

**Decision:** secret values are prohibited from Git manifests and normalized public evidence. Synthetic canary secrets may be injected only at the execution boundary for F13. Credential reference names are allowed; values are separately controlled.

## C-019 — What does “same budget” mean?

**Decision:** paired arms receive the same maximum declared wall/token/money envelope where enforceable. An arm may use less. Internal substeps do not create extra budget and consumed resources remain part of efficiency evidence.

## C-020 — Is parallelism an experimental advantage?

**Decision:** no. Runner concurrency is plumbing only. Use one fixed host-level concurrency policy, isolated workspaces, balanced run ordering, and explicit resource-contention evidence. No arm-specific concurrency advantage is allowed.

## C-021 — When is the minimum runner considered inadequate?

**Decision:** runner replacement/repair is required before confirmatory planning if the stable screening rerun breaches any frozen runner criteria.

Runner overhead is computed mechanically for every **started screening trial**, including normal success/failure and runner-caused invalid/incomplete outcomes:

```text
trial_wall_seconds = monotonic(finalization_end - attempt_start)
runner_overhead_seconds = sum(exclusive runner-controlled orchestration intervals)
runner_overhead_fraction = runner_overhead_seconds / trial_wall_seconds
```

`runner_overhead_seconds` includes runner-controlled validation after attempt start, workspace/container/process orchestration, observation/control bookkeeping, artifact/evidence capture orchestration, cleanup, canonical serialization, and TrialRecord finalization. It excludes intervals spent waiting for task code, model/provider execution, and objective-verifier execution. Timers for a trial must be non-overlapping monotonic intervals so summed runner time cannot double-count concurrent phases.

Pre-attempt infrastructure observations from C-016 are excluded because no screening attempt has started; they are reported separately as readiness/infrastructure counts and operator burden. No post-start retry exists. A started trial with missing/nonpositive wall timing or unaccountable runner timing makes runner evidence incomplete and fails the adequacy gate rather than being removed from aggregation.

For the final stable screening batch:

```text
MEDIAN_RUNNER_OVERHEAD_FRACTION = median(per-started-trial runner_overhead_fraction)
P95_RUNNER_OVERHEAD_SECONDS = nearest-rank p95(per-started-trial runner_overhead_seconds)
```

Aggregation is across all started task/arm/model trials in the frozen batch, with no per-arm, per-model, per-cell, or success-only pre-aggregation.

Manual recovery uses the same explicit all-started-trial population. Define:

```text
STARTED_TRIAL_COUNT = count(TrialRecords that crossed attempt_start in the final stable screening batch)
OPERATOR_RECOVERY_MINUTES_TOTAL = sum(unplanned manual operator recovery minutes attributable to H0 runner/readiness operation in that batch)
OPERATOR_MINUTES_PER_100_STARTED_TRIALS = (OPERATOR_RECOVERY_MINUTES_TOTAL * 100) / STARTED_TRIAL_COUNT
```

`STARTED_TRIAL_COUNT` includes successful, failed, and runner-caused invalid/incomplete outcomes. `OPERATOR_RECOVERY_MINUTES_TOTAL` includes manual recovery attributable to pre-attempt readiness handling and started-trial orchestration/cleanup/evidence handling; planned experiment setup is excluded. A zero started-trial denominator or incomplete recovery-time accounting makes runner adequacy evidence incomplete and cannot pass.

Runner replacement/repair is required if any applies:

```text
RUNNER_CAUSED_INVALID_OR_INCOMPLETE_TRIAL_RATE > 2_PERCENT
MEDIAN_RUNNER_OVERHEAD_FRACTION > 15_PERCENT
OPERATOR_MINUTES_PER_100_STARTED_TRIALS > 120
DISTRIBUTED_SCHEDULER_REQUIRED = YES
NEW_CLOUD_PROVIDER_BACKEND_REQUIRED = YES
EVIDENCE_CONTRACT_FULLY_SATISFIED = NO
```

These thresholds decide runner adequacy only, not Harness GO.

## C-022 — Can H0-SCREEN modify canonical Harness research documents?

**Decision:** no. The seven research documents canonicalized by PR #42 are frozen under the current Harness research policy. This feature consumes them as upstream authority/evidence and does not edit them.

## C-023 — Can this Spec Kit package authorize implementation?

**Decision:** no.

After the package, Ponytail, and Source Acquisition Check are canonical and independently reviewed, a separate trusted-base policy migration must explicitly authorize the minimum implementation paths, dependencies, effects, fixtures, and gates. Until that policy is canonical and activation-proven:

```text
H0_SCREEN_IMPLEMENTATION = BLOCKED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
S1_013_PLUS = NOT_STARTED
```
