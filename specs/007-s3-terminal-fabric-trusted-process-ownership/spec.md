# S3 Specification — Terminal Fabric + Trusted Process Ownership

## 1. Problem statement

S1 proved a trusted Desktop ↔ Rust Core channel. S2 proved WePLD can deterministically know *what project* it is looking at. Neither S1 nor S2 lets WePLD own, observe, or bound an operating-system process on the user's behalf, and neither defines the seam at which a proposed effect is checked against authority before it runs.

S3 must answer: **when WePLD (or a future worker acting through WePLD) proposes to spawn, observe, or cancel a process, what durable identity does that process tree get, what containment is actually proven versus merely claimed, and what stops that proposal from silently becoming an executed effect?**

Per `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`'s revised roadmap interpretation, S3 adds exactly five things: an effect-proposal/effect-result envelope; process-tree identity; a containment-capability report; a Nawat PEP seam without the full policy engine; and a Windows-native containment investigation. It does not add a working Terminal, a working automation engine, or any actual effect authority.

## 2. User outcomes

S3 is foundation, not a user-facing feature. It has no direct CLI/UI outcome of its own; its outcome is enabling later slices to build one safely. The nearest planning-visible outcomes are internal/developer-facing:

### UO-1 — A future effect proposal cannot silently execute

Any future WePLD subsystem that wants to run a process must go through one typed proposal → PEP-decision → result path. There is no second, informal way to spawn a process that bypasses this seam.

### UO-2 — Containment claims are evidence, not a badge

A future Doctor/Assurance surface can ask "what containment does this host actually have?" and receive per-dimension evidence (process-tree/filesystem/network/...), never a single trust-me boolean.

### UO-3 — A stale or replaced process owner cannot keep acting

If the process that owned a process tree is restarted or replaced, further effect proposals against the old ownership are refused rather than silently honored.

## 3. Scope

### In scope

- `ServerDescriptor`/`HostDescriptor`/`RunnerDescriptor` identity separation, scoped to a single local host (no distributed/remote enrollment);
- explicit, observable host execution opt-in state;
- process-tree identity distinct from a raw OS PID (PID-reuse / restart detection);
- a Windows-native containment-capability investigation and report (Job-Object-class process-tree containment as the primary target);
- multidimensional `ContainmentPosture` representation (process-tree/filesystem/network/... independently, never a single boolean);
- a local `RuntimeCeiling` and the intersection rule for the effective execution envelope;
- a deny-by-default `EnvironmentExposurePolicy` shape for any process S3 later spawns;
- `EffectProposal`/`EffectResult` envelope shapes, closed-enum and bounded;
- a Nawat PEP (Policy Enforcement Point) seam: every proposal is checked against a decision before a result can exist, and an unevaluable decision fails closed;
- bounded cancellation semantics for any process-tree effect;
- a local ownership-epoch / stale-owner-refusal prerequisite (single host; not distributed fencing);
- effect-dependency ordering for composite proposals (prerequisite/dependent, unknown-outcome blocking);
- revalidation triggers that stale a frozen envelope/decision when a material input changes;
- runtime/process evidence privacy (no raw environment values or unredacted process output in durable evidence);
- adopting `S2-S003` (native Windows junction/reparse coverage, `EXPECTED_NEXT_OWNER = S3_PLANNING` per `specs/005-.../acceptance.md` §H.1) as an explicit, tracked S3 obligation — see §10.

### Out of scope

- S3-D (the separate, non-primary deterministic-assurance-seed gate);
- actual Terminal/PTY user-facing execution;
- a product-level automation engine;
- Mission Runtime, UWC, Mirefa, Edara, or the full effect-time Nawat policy engine (S6/S6-N);
- distributed/remote host enrollment and cross-host runner fencing (FR-057/FR-058 in `contracts/runtime-execution-fabric.md`, deferred to S6+);
- `HarnessProtocolAdapter`/`HarnessDialectExtension` (S6-owned);
- `CredentialCapability`/credential brokering of any kind;
- `NativeBridgeCapability` (Desktop SPA ↔ native IPC boundary; a separate concern from server/host/runner process ownership);
- network access of any kind;
- model/provider execution;
- Worker/Assignment/Attempt records (`data-model.md`/`worker-delegation.md`-owned).

## 4. Domain model

This model is the S3-owned subset of `specs/006-issueops-agentic-engineering-control-plane/contracts/runtime-execution-fabric.md`, narrowed to a single local host with no network, credential, or harness-adapter concepts. Where a field from that contract is dropped here, it is dropped because it belongs to a later slice, not because it was found unnecessary.

### 4.1 ServerDescriptor

The local control point identity (WePLD Desktop/Core taken together, at this gate).

```text
server_id
deployment_identity
software_identity
policy_snapshot_ref
observed_at
```

Connecting a client to this local control point creates no execution authority by itself.

### 4.2 HostDescriptor

```text
host_id
server_binding_ref?
machine_identity
os_platform_identity
os_version_identity
host_execution_opt_in_state
available_containment_backends[]
process_tree_containment_capability
filesystem_containment_capability
last_liveness_observation
qualification_state
qualification_evidence_refs[]
qualification_expiry?
```

```text
HOST_REGISTERED != HOST_QUALIFIED
HOST_QUALIFIED != EFFECT_AUTHORITY
HOST_ONLINE != RUNNER_READY
```

`host_execution_opt_in_state` must default to not-opted-in. Merely loading WePLD Desktop or completing the S1 handshake must not set it.

### 4.3 RunnerDescriptor

One local execution-runtime instance owned by a host (the process/thread pool actually capable of owning a process tree).

```text
runner_id
host_id
runner_runtime_identity
process_or_service_identity?
containment_posture_ref
runtime_ceiling_ref
environment_exposure_policy_ref
current_liveness_state
current_capacity
current_network_state = NONE
qualification_state
qualification_evidence_refs[]
qualification_expiry?
```

`current_network_state` is fixed to `NONE` for every S3 runner; a runner that needs network authority is out of this package's scope by definition.

### 4.4 ProcessTreeIdentity

The durable ownership record for one spawned/observed OS process tree — this is the "process-tree identity" the master plan names directly.

```text
process_tree_identity_id
runner_ref
os_process_id
os_process_start_time
parent_process_id?
containment_handle_ref?
ownership_epoch
liveness_state
observed_at
```

`os_process_id` alone is never sufficient identity: `os_process_start_time` (or an equivalent OS-provided non-reusable token) must be checked together with the PID to detect PID reuse after exit. `ownership_epoch` increments whenever the owning runner instance is qualified as restarted/replaced; an effect proposal bound to a stale epoch is refused.

```text
OS_PID != PROCESS_TREE_IDENTITY
STALE_OWNERSHIP_EPOCH -> EFFECT_REFUSED
```

### 4.5 ContainmentCapabilityReport

The discovery-time report of what containment is actually available on this host/OS version — produced once per host qualification (and re-produced when `qualification_expiry` lapses or a material OS change is observed), not asserted from a label.

```text
containment_capability_report_id
host_ref
os_platform_identity
os_version_identity
available_backends[]
per_backend_strength_map
evidence_refs[]
observed_at
expires_at?
```

On Windows, the primary investigated backend is a Job-Object-class mechanism for process-tree containment. Filesystem and network strength for that same backend default to `NONE`/`UNKNOWN` unless independently proven; they are never inferred from process-tree strength.

### 4.6 ContainmentPosture

Reused verbatim from `contracts/runtime-execution-fabric.md`, scoped to the dimensions S3 can actually evidence on the current host:

```text
containment_posture_id
backend_identity
platform_runtime_identity
process_tree_strength
filesystem_strength
network_strength
namespace_or_container_strength?
seccomp_or_syscall_policy_identity?
read_mount_policy_identity?
write_mount_policy_identity?
home_visibility_state
temporary_storage_policy
escape_or_downgrade_limitations[]
evidence_refs[]
observed_at
expires_at?
```

Normalized strength candidates: `HARD_ISOLATION`, `HARD_WITH_EXPLICIT_LIMITATION`, `PROCESS_TREE_ONLY`, `ADVISORY`, `NONE`, `UNKNOWN`.

```text
PROCESS_TREE_ONLY != HARD_FILESYSTEM_ISOLATION
PROCESS_TREE_ONLY != NETWORK_ISOLATION
PROVIDER_SANDBOX_LABEL != CONTAINMENT_POSTURE
SANDBOX_REQUIRED + QUALIFIED_BACKEND_UNAVAILABLE -> EXECUTION_REFUSED
CONTAINMENT_DOWNGRADE -> EXPLICIT_REQUALIFICATION
```

### 4.7 RuntimeCeiling

Scoped to a single local host; no cross-deployment/tenant fields.

```text
runtime_ceiling_id
max_effect_classes[]
max_network_class = NONE
max_process_scope
max_parallel_process_trees
max_wall_clock
max_cpu?
max_memory?
max_output?
allowed_containment_postures[]
policy_snapshot_ref
```

The effective envelope is an intersection, never a union:

```text
EffectiveExecutionEnvelope =
  RuntimeCeiling
  INTERSECT ContainmentPosture-implied bound
  INTERSECT EffectProposal constraints
```

An empty intersection blocks the proposal.

### 4.8 EnvironmentExposurePolicy

```text
environment_policy_id
baseline_allowlist[]
explicit_process_launch_passthrough[]
forced_values[]
scrub_patterns[]
prohibited_secret_classes[]
home_config_visibility_policy
inherited_path_policy
policy_snapshot_ref
```

```text
AMBIENT_HOST_ENV != PROCESS_ENV
```

A spawned process receives only `baseline_allowlist` plus any `explicit_process_launch_passthrough` the caller names; nothing else is inherited wholesale.

### 4.9 EffectProposal

```text
effect_proposal_id
proposed_effect_kind
host_ref
runner_ref?
process_tree_identity_ref?
containment_requirement_ref
runtime_ceiling_ref
environment_exposure_policy_ref
requested_at
requested_by
effect_dependency_refs[]
```

`proposed_effect_kind` is a closed enum bounded to what S3 itself can request, at minimum: `SPAWN_PROCESS_TREE`, `OBSERVE_PROCESS_TREE`, `REQUEST_CANCELLATION`. It is never an arbitrary command string interpreted later; the exact argv/command shape for `SPAWN_PROCESS_TREE`, if specified at all in this package, is closed and allowlisted, not general shell invocation.

### 4.10 PEPDecision

The Nawat PEP seam. This is an interface contract, not the policy engine behind it.

```text
pep_decision_id
effect_proposal_ref
decision
decision_source
evaluated_at
policy_snapshot_ref
rationale_evidence_refs[]
```

`decision` is a closed enum: `ALLOW`, `DENY`, `UNKNOWN_FAIL_CLOSED`. `decision_source` must be a WePLD-owned trusted evaluator identity; repository-controlled or untrusted-content-derived sources cannot populate this field. Missing, stale, or unevaluable policy input produces `UNKNOWN_FAIL_CLOSED`, never `ALLOW`.

```text
PEP_ALLOW != NAWAT_GRANT
PEP_SEAM_PRESENT != POLICY_ENGINE_COMPLETE
UNKNOWN_POLICY_INPUT -> UNKNOWN_FAIL_CLOSED
```

### 4.11 EffectResult

```text
effect_result_id
effect_proposal_ref
pep_decision_ref
outcome
process_tree_identity_ref?
containment_posture_observed_ref?
started_at?
ended_at?
exit_status?
evidence_refs[]
```

`outcome` is a closed enum: `EXECUTED`, `REFUSED`, `CANCELLED`, `UNKNOWN`. Every `EffectResult` requires a resolved `pep_decision_ref`; a proposal with no resolved `PEPDecision` produces no `EffectResult` at all (FR-010). Once a decision is resolved: `DENY` and `UNKNOWN_FAIL_CLOSED` both produce `REFUSED`; only `ALLOW` may lead to `EXECUTED`, and even then the in-flight effect may still resolve to `CANCELLED`/`UNKNOWN` per the cancellation/recovery rules below. `EXECUTED` is never reachable from `DENY` or `UNKNOWN_FAIL_CLOSED`.

### 4.12 EffectDependency

```text
prerequisite_effect_ref
dependent_effect_ref
required_prerequisite_postcondition
failure_policy
irreversible_boundary?
```

```text
PREREQUISITE_UNAVAILABLE -> DEPENDENT_EFFECT_NOT_STARTED
PREREQUISITE_EFFECT_OUTCOME_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_NOT_STARTED
```

## 5. Functional requirements

### FR-001 — Explicit host opt-in

`HostDescriptor.host_execution_opt_in_state` defaults to not-opted-in. No S1/S2 action sets it. Only an explicit, user-observable action sets it.

### FR-002 — Identity separation preserved

`ServerIdentity`, `HostIdentity`, and `RunnerIdentity` are distinct typed identities. An early tracer-bullet implementation may run them in one process, but the evidence/identity records remain separate wherever the trust question differs.

### FR-003 — Process-tree identity beyond a raw PID

A `ProcessTreeIdentity` binds `os_process_id` together with `os_process_start_time` (or an equivalent non-reusable token). A PID observed after its originally-identified process has exited must not be treated as the same process-tree identity.

### FR-004 — Containment capability is discovered, not assumed

`ContainmentCapabilityReport` is produced by an explicit host-qualification step. A host with no completed qualification has `qualification_state != qualified`, and no `ContainmentPosture` derived from it may report a strength stronger than `UNKNOWN`.

### FR-005 — Windows-native containment investigated first

The primary S3 containment investigation targets a Windows Job-Object-class backend for process-tree strength. Filesystem/network strength on that same host/backend are `NONE`/`UNKNOWN` unless a separate, explicitly evidenced mechanism proves otherwise.

### FR-006 — Containment is multidimensional

No S3 evidence record may represent containment as one boolean. Each dimension in `ContainmentPosture` is set independently.

### FR-007 — Runtime ceiling is a hard upper bound

`RuntimeCeiling` values are never widened by an `EffectProposal`, a later-loaded configuration, or repository content. The effective envelope is the intersection of the ceiling and every other controlling constraint; an empty intersection blocks the proposal outright.

### FR-008 — Deny-by-default process environment

Any process a future S3 implementation spawns receives only `EnvironmentExposurePolicy.baseline_allowlist` plus explicit passthrough. Ambient host environment variables are not inherited wholesale.

### FR-009 — Closed-enum effect proposals

`EffectProposal.proposed_effect_kind` is a closed enum. An implementation must reject an unrecognized kind rather than passing it through to a generic executor.

### FR-010 — Every proposal passes the PEP seam

No `EffectResult` may exist without a resolved `PEPDecision` for the same `EffectProposal`. A missing or unresolved decision blocks the result; it is not treated as an implicit allow.

### FR-011 — Fail-closed PEP evaluation

A `PEPDecision` that cannot be evaluated — missing, stale, or malformed policy input — is `UNKNOWN_FAIL_CLOSED`. `UNKNOWN_FAIL_CLOSED` and `DENY` both refuse the proposal; only `ALLOW` may lead to `EXECUTED`.

### FR-012 — PEP is a seam, not the engine

This package specifies the `PEPDecision` interface only. It does not specify or implement Mirefa qualification, Edara topology selection, or the full S6-N effect-time policy engine behind `decision_source`. A minimal, explicitly narrow, fail-closed default evaluator may be specified for planning coherence, but it is not a general policy evaluator and must not be represented as one.

### FR-013 — Bounded cancellation

Every process-tree effect this package describes has a documented bounded-cancellation contract: a cancellation request against a live `EffectResult` produces `CANCELLED` or a stable timeout-bounded `UNKNOWN` within a fixed bound. No cancellation path waits unboundedly.

### FR-014 — Stale ownership epoch refused

An `EffectProposal` referencing a `process_tree_identity_ref` whose `ownership_epoch` no longer matches the current epoch for that process tree is refused. The refusal is explicit (a `REFUSED` `EffectResult`), never silently redirected to a different, newer process tree.

### FR-015 — Revalidation triggers stale prior evidence

At minimum, `HOST_CHANGE`, `RUNNER_RUNTIME_RESTART`, `CONTAINMENT_CHANGE`, `ENV_POLICY_CHANGE`, and `PEP_DECISION_EXPIRY` each stale any envelope/decision computed before the change, for any subsequent proposal.

### FR-016 — No network authority

No S3 domain type or functional requirement grants network access. `RunnerDescriptor.current_network_state` and `RuntimeCeiling.max_network_class` are fixed to `NONE`.

### FR-017 — Effect dependency ordering

A composite proposal may declare `EffectDependency` edges. A dependent effect whose prerequisite is unavailable does not start; an irreversible dependent effect whose prerequisite outcome is `UNKNOWN` does not start either.

### FR-018 — Runtime/process evidence privacy

No S3 durable evidence record may contain a raw environment variable value, an unredacted process argument, or unredacted process output content, except through an explicit allowlisted evidence field defined by a later authority.

### FR-019 — Version/capability negotiation fails closed

An unrecognized or unsupported OS/containment-backend version is recorded as `UNKNOWN`, never assumed to support a stronger containment posture than proven.

### FR-020 — Resource admission is distinguished from qualification

A `RunnerDescriptor` being `qualified` does not by itself mean resource admission (an actual reservation of CPU/memory/process-count capacity) has occurred for a given proposal. This package specifies the distinction; it does not specify a reservation algorithm.

## 6. Security requirements

### SR-001

A repository-controlled value (config, remote URL, file content) must never be able to influence `PEPDecision.decision_source` or widen a `RuntimeCeiling`.

### SR-002

`EffectProposal.proposed_effect_kind = SPAWN_PROCESS_TREE`, if specified at all in a later planning phase of this package, must use a closed, allowlisted argv/command shape — never a general shell string.

### SR-003

`ContainmentPosture` fields must never be populated from a vendor/provider self-reported `sandboxed` boolean; they must derive from an evidenced, WePLD-owned qualification step.

### SR-004

`ProcessTreeIdentity` reuse-detection (FR-003) is mandatory wherever a stale-PID confusion could misattribute an effect to the wrong process.

### SR-005

Evidence for `EffectProposal`/`EffectResult`/`ContainmentCapabilityReport` must exclude raw environment values and unredacted process output, per FR-018.

### SR-006

Cancellation/timeout paths (FR-013) must be bounded so that an untrusted or hung process cannot force an ordinary S3 operation to wait forever.

## 7. Non-functional requirements

### NFR-001 — Determinism

Given the same qualified host/runner/containment observations, `PEPDecision` and `EffectResult` outcomes for equivalent proposals are deterministic.

### NFR-002 — Windows-first, cross-platform explicit

Windows is the first qualification target. Any Linux/macOS containment claim is explicit evidence, never inferred from the Windows result.

### NFR-003 — Bounded waiting

No S3 operation (qualification, proposal evaluation, cancellation) waits unboundedly.

### NFR-004 — Backward-compatible schemas

`EffectProposal`, `EffectResult`, `PEPDecision`, `ContainmentPosture`, and `ContainmentCapabilityReport` are versioned from first release.

## 8. Acceptance scenarios

1. Loading WePLD Desktop and completing the S1 handshake produces no `HostDescriptor` with `host_execution_opt_in_state = true`.
2. A host with no completed containment qualification cannot produce a `ContainmentPosture` stronger than `UNKNOWN` on any dimension.
3. On a Windows host without Job-Object support (or where support cannot be proven), `process_tree_strength = NONE/UNKNOWN`, not `PROCESS_TREE_ONLY`.
4. A `ContainmentPosture` with `process_tree_strength = PROCESS_TREE_ONLY` and `filesystem_strength = NONE` is never consumed as satisfying a filesystem-isolation requirement.
5. An `EffectProposal` with no corresponding `PEPDecision` never produces an `EXECUTED` `EffectResult`.
6. A `PEPDecision` computed against a stale/missing policy snapshot is `UNKNOWN_FAIL_CLOSED`, and the corresponding `EffectResult` is `REFUSED`.
7. An OS PID reused by an unrelated process after the original process-tree exit is not matched to the original `ProcessTreeIdentity` (start-time/epoch check distinguishes them).
8. A cancellation request against a live `EffectResult` resolves to `CANCELLED` or a bounded `UNKNOWN` within the documented deadline; it never hangs.
9. An `EffectProposal` whose requested constraints, intersected with the current `RuntimeCeiling`, produce an empty envelope is refused rather than silently narrowed and executed anyway.
10. An `EffectProposal` referencing a `process_tree_identity_ref` with a superseded `ownership_epoch` is refused.
11. A dependent effect declared against a prerequisite effect with `EFFECT_OUTCOME_UNKNOWN`, marked `irreversible_boundary`, does not start.
12. No S3 evidence record — proposal, result, decision, or containment report — contains a raw environment variable value or unredacted process output.

## 9. Planning status

```text
SPEC_STATUS = INITIAL_PLANNING_CANDIDATE_PENDING_CLARIFY_AND_PLAN
IMPLEMENTATION = BLOCKED_BY_AUTHORITY
SOURCE_IMPORT = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
```

## 10. Adopted cross-slice obligation — `S2-S003`

`specs/005-s2-open-project-doctor-local-identity-storage/tasks.md` records `S2-S003` (Windows junction/reparse/extended-length path tests) as `[~]` PARTIAL: extended-length verbatim-prefix normalization is proven on injected Linux/macOS inputs, but real Windows junction/reparse behavior under native Windows `wepld-core` runtime is not proven, because no S2 CI surface runs `wepld-core` natively on Windows (`acceptance.md` §H.1: `WINDOWS_NATIVE_CORE_RUNTIME_COVERAGE = ABSENT`). That acceptance section and `tasks.md`'s own disposition (`S2_S003_DISPOSITION = OPEN_CROSS_SLICE_OBLIGATION`, `EXPECTED_NEXT_OWNER = S3_PLANNING`) require the next slice's planning to explicitly adopt it rather than leave it unowned.

This package adopts it as follows:

```text
S2_S003_ADOPTED_BY = S3_PLANNING (this package)
S2_S003_DISCHARGE_MECHANISM = S3-AUTH-HOST's own Windows-native containment
  investigation requires actual native Windows wepld-core runtime execution
  in CI (to call Job Object APIs) — the same precondition S2-S003 was
  blocked on. Once that CI surface exists, S2's own existing junction/reparse
  fixtures (owned by S2's crate, not rewritten by this package) can be
  executed for real on that same native Windows runner.
S2_S003_NOT_DISCHARGED_BY = specifying this package's contracts alone; only
  actual S3-AUTH-HOST-stage native Windows execution evidence can discharge it.
S2_S003_STILL_OPEN_IF = S3-AUTH-HOST is not reached, or is reached without
  actually enabling native Windows CI execution of wepld-core; in that case
  S3's own acceptance must explicitly re-record S2-S003 as still open for
  the next slice, exactly as S2 did for S3.
```

S3 does not rewrite or re-implement S2's junction/reparse test fixtures. It is responsible only for the native-Windows-runtime precondition and for explicit, honest bookkeeping — not silently discharging or silently dropping the obligation.
