# WePLD Harness Program — H0 Runner Decision Review

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / RUNNER DECISION REVIEW
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
RUNTIME_ADOPTION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## 1. Decision

The H0 research runner strategy is staged.

```text
H0_SCREENING_PREFERRED_RUNNER = WEPLD_MINIMAL_LOCAL_RUNNER
H0_CONFIRMATORY_RUNNER = UNDECIDED_UNTIL_SCREENING_EVIDENCE
HARBOR_STATUS = QUALIFIED_REFERENCE / CONDITIONAL_EXTERNAL_RUNNER_CANDIDATE
HARBOR_PRODUCT_DEPENDENCY = NO
HARBOR_CODE_IMPORT = NONE
```

This is a research architecture decision only. No runner implementation is authorized by this document.

## 2. Why not select Harbor immediately

The exact inspected Harbor pin provides mature machinery for:

```text
Task / Dataset / Agent / Environment / Trial / Job abstractions
trial lifecycle
trial queues
artifact handling
network policy
single-step and multi-step execution
regrade flows
many local/cloud environment providers
parallel jobs
```

That machinery is valuable, but the inspected package also carries a broad default dependency set and a large optional cloud/provider surface.

H0 screening does not need the majority of that surface.

Selecting Harbor before proving the need would risk making evaluation infrastructure complexity part of the Harness thesis rather than a replaceable implementation detail.

## 3. Why not build a large WePLD runner

The opposite failure mode is equally unacceptable.

WePLD must not recreate:

```text
distributed scheduling
multi-cloud sandbox orchestration
benchmark registry
viewer platform
RL rollout infrastructure
provider marketplace
remote artifact service
complex resumable job server
```

merely to avoid an external dependency.

The purpose of a WePLD minimal runner is to prove the H0 evidence boundary with minimum sufficient machinery, not to become another evaluation framework.

## 4. Screening runner scope

If separately authorized for implementation, the screening runner should be limited to:

```text
1. load frozen manifests
2. validate hashes and trial identities
3. materialize one local/container task environment
4. launch one selected harness/agent command
5. enforce wall/turn/process boundaries where practical
6. capture stdout/stderr and declared artifacts
7. capture provider usage when exposed
8. record effect/egress observations available at the boundary
9. invoke the frozen objective verifier separately
10. emit normalized immutable trial evidence
11. clean up the environment
12. run bounded local concurrency
```

Explicitly excluded:

```text
NO WEB UI
NO DATABASE SERVICE
NO REMOTE OBSERVABILITY SERVICE
NO CLOUD PROVIDER SDK
NO PLUGIN MARKETPLACE
NO DATASET REGISTRY
NO RL SUPPORT
NO GENERAL WORKFLOW ENGINE
NO SELF_EVOLUTION
NO HARNESS SEARCH
NO PRODUCT INTEGRATION
```

## 5. Preferred local execution mechanism

The H0 design should prefer a simple replaceable boundary around an already available local container engine rather than embedding a container platform.

Conceptual execution:

```text
Frozen Trial Manifests
        |
WePLD Minimal Runner
        |
local container/process boundary
        |
agent/harness command
        |
raw artifacts/logs/usage
        |
WePLD verifier + evidence finalizer
```

The runner should treat the container/runtime CLI or API as a replaceable transport.

## 6. Screening concurrency

The minimal runner may support bounded local concurrency because H0-SCREEN contains many cells.

Concurrency must remain plumbing only:

```text
FIXED_MAX_CONCURRENCY_PER_HOST
NO ARM-SPECIFIC CONCURRENCY ADVANTAGE
NO SHARED_MUTABLE_TASK_WORKSPACE
BALANCED_RUN_ORDER
RESOURCE_CONTENTION_RECORDED
```

A simple bounded worker pool is acceptable. A distributed scheduler is not part of the minimal runner.

## 7. Screening is also a runner adequacy test

H0-SCREEN has two jobs:

1. calibrate harness experiment plumbing;
2. measure whether the minimal runner is sufficient for confirmatory execution.

Record runner-specific operational metrics:

```text
runner_setup_failures
container_start_failures
cleanup_failures
artifact_capture_failures
usage_capture_failures
verifier_invocation_failures
median_runner_overhead_seconds
p95_runner_overhead_seconds
host_resource_contention_events
manual_recovery_events
operator_minutes_per_100_trials
```

These metrics do not affect harness GO directly; they decide whether the runner itself should be replaced before confirmatory work.

## 8. Confirmatory runner switch triggers

Before H0-CONFIRM, evaluate the minimal runner against the following triggers.

Harbor qualification for confirmatory becomes preferred if **one or more** of these are true and cannot be removed with a small bounded repair:

```text
TRIGGER_A
confirmatory throughput requires remote/cloud container execution

TRIGGER_B
minimal runner would require adding a distributed scheduler or remote job service

TRIGGER_C
minimal runner would require implementing more than one materially different environment backend

TRIGGER_D
manual recovery burden exceeds 2 operator-hours per 100 completed trials

TRIGGER_E
runner-caused invalid/incomplete trial rate exceeds 2% during the final stable screening rerun

TRIGGER_F
runner overhead exceeds 15% of median total task wall time for the final stable screening rerun

TRIGGER_G
reliable resume/recovery at confirmatory scale would require substantial new orchestration machinery
```

The numeric operational thresholds above govern runner selection only. They do not change Harness thesis success thresholds.

## 9. Minimal-runner retention criteria

The minimal runner remains preferred for confirmatory only if the final stable screening rerun satisfies all:

```text
RUNNER_CAUSED_INVALID_OR_INCOMPLETE_TRIAL_RATE <= 2_PERCENT
MEDIAN_RUNNER_OVERHEAD_FRACTION <= 15_PERCENT
MANUAL_RECOVERY <= 2_OPERATOR_HOURS_PER_100_COMPLETED_TRIALS
LOCAL_OR_EXISTING_CONTROLLED_CAPACITY_CAN_EXECUTE_CONFIRMATORY_WITHIN_DECLARED_BUDGET
NO_DISTRIBUTED_SCHEDULER_REQUIRED
NO_NEW_CLOUD_PROVIDER_BACKEND_REQUIRED
EVIDENCE_CONTRACT_FULLY_SATISFIED
```

## 10. Harbor confirmatory qualification boundary

If a switch trigger fires, Harbor is not automatically admitted.

A separate exact-pin qualification must prove:

```text
LICENSE/NOTICE REVIEW COMPLETE FOR INTENDED USE
EXACT HARBOR VERSION/COMMIT PIN
INSTALL/LOCK REPRODUCIBLE
WEPLD TrialIdentity PRESERVED
WEPLD manifests remain source of comparison identity
NO SILENT RETRIES
NO SILENT TASK DROPS
RAW ARTIFACT ACCESS
RAW FAILURE ACCESS
TOKEN/USAGE ACCESS OR EXPLICIT LIMITATION
NETWORK POLICY COMPATIBLE
MODEL-SERVING EGRESS SEPARATED FROM TASK EGRESS
SECRET HANDLING COMPATIBLE
CLEANUP/RESUME BEHAVIOR TESTED
WEPLD OBJECTIVE VERIFIER REMAINS FINAL AUTHORITY
WEPLD NORMALIZED EVIDENCE EXPORT PRESERVED
EXIT PATH TESTED
```

Harbor-generated reward or result summaries are observations, not H0 promotion authority.

## 11. Harbor integration shape if later qualified

Preferred architecture:

```text
WePLD ExperimentManifest
        |
WePLD HarborAdapter
        |
Harbor pinned external runner
        |
raw Harbor trial/artifact output
        |
WePLD evidence importer
        |
WePLD objective verifier binding
        |
WePLD TrialRecord
```

Do not import Harbor's internal object model into WePLD HIR or product runtime.

## 12. Harbor features explicitly out of H0 scope

Even if Harbor becomes the confirmatory runner, H0 does not need to enable:

```text
RL optimization
remote result viewer
Supabase upload
all cloud providers
all agent adapters
all benchmark adapters
computer-use stacks
training extras
DSPy/Tinker integrations
remote observability stacks
```

Use only the exact required surface.

## 13. Scaffold Effects role in runner decision

Scaffold Effects is not a runner candidate for WePLD H0.

It is retained as:

```text
analysis/provenance oracle
trial-record inspiration
failure-metric oracle
reproduction-pattern reference
```

Its inspected package depends on a Harbor + Daytona runtime path; H0 should not inherit that coupling by default.

## 14. Harness-Bench role in runner decision

Harness-Bench is not a code runner candidate until rights are established.

Its task/oracle/trace design remains a useful behavioral reference.

```text
CODE_REUSE = BLOCKED
BEHAVIORAL_REFERENCE = YES
```

## 15. Runner must not become a fifth experimental arm

All A/B/C/D arms must use the same runner implementation within a valid paired comparison.

If the runner changes during the experiment:

```text
SCREENING = may restart after plumbing changes
CONFIRMATORY = runner change requires a new frozen execution batch/protocol treatment
```

Do not compare A/B on one runner and C/D on another and attribute the difference to harness design.

## 16. Runner validation fixtures

Before real screening tasks, a future implementation must pass synthetic runner fixtures covering at minimum:

```text
PASSING_TASK
FAILING_TASK
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
```

These fixtures validate the runner/evidence contract. They are not H0 model/harness evaluation tasks.

## 17. Runner security posture

Initial screening posture:

```text
TASK_NETWORK = DENY_BY_DEFAULT
MODEL_PROVIDER_ACCESS = EXPLICIT_SEPARATE_CHANNEL_WHERE_REQUIRED
CREDENTIALS = EXECUTION_TIME_INJECTION_ONLY
TASK_EXTERNAL_SIDE_EFFECTS = NONE
MERGE_DEPLOY_PUBLISH = DENY
HOST_FILESYSTEM = MINIMUM_MOUNTS
CONTAINER_PRIVILEGED_MODE = DENY
HOST_DOCKER_SOCKET_INSIDE_TASK = DENY
RAW_SECRET_LOGGING = DENY
```

Any unavoidable exception must be task-manifested and cannot differ by arm.

## 18. Decision consequences

### Current research preference

```text
SCREENING = MINIMAL_LOCAL_RUNNER
```

This keeps the first implementation, if later authorized, small enough to falsify quickly.

### After screening

```text
IF minimal runner retention criteria pass:
    H0_CONFIRMATORY_RUNNER = MINIMAL_LOCAL_RUNNER
ELSE IF Harbor exact-pin qualification passes:
    H0_CONFIRMATORY_RUNNER = HARBOR_EXTERNAL_REPLACEABLE_RUNNER
ELSE:
    H0_CONFIRMATORY_BLOCKED_PENDING_RUNNER_REPAIR_OR_REPLACEMENT
```

## 19. Anti-complexity kill switch

If implementing the "minimal" runner begins to require any two of:

```text
distributed scheduler
persistent service/database
cloud-provider abstraction
remote artifact server
general plugin system
multi-benchmark registry
complex resume controller
```

stop expansion and re-evaluate Harbor or another mature external runner.

The Harness Program must not spend its falsification budget rebuilding evaluation infrastructure.

## 20. Current authority state

```text
RUNNER_DECISION_REVIEW = COMPLETE_FOR_RESEARCH
H0_SCREENING_PREFERRED_RUNNER = WEPLD_MINIMAL_LOCAL_RUNNER
H0_CONFIRMATORY_RUNNER = UNDECIDED
HARBOR_ADMISSION = NONE
RUNNER_IMPLEMENTATION = NOT_STARTED
H0_SCREENING = NOT_STARTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
S1_013_PLUS = NOT_STARTED
```

Next research step:

> Define the exact H0-SCREEN synthetic runner-fixture contract and minimal A/B/C/D recipe boundaries, then seek a separately governed implementation authorization rather than continuing architecture expansion.
