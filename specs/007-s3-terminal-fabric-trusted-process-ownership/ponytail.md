# S3 Ponytail FULL

## Verdict

```text
PONYTAIL_MODE = FULL
PONYTAIL_STATUS = COMPLETE_FOR_INITIAL_PLANNING_CANDIDATE_PENDING_EXACT_HEAD_REVIEW
NEW_DEPENDENCY_REQUIRED_BY_PLAN = NO
SOURCE_IMPORT_REQUIRED_BY_PLAN = NO
DATABASE_REQUIRED_BY_PLAN = NO
MODEL_REQUIRED_BY_PLAN = NO
NETWORK_REQUIRED_BY_PLAN = NO
DISTRIBUTED_RUNTIME_REQUIRED_BY_PLAN = NO
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

Ponytail asks whether each proposed mechanism needs to exist now, already exists in admitted/native machinery, can be acquired, or can be smaller. S3's own master-plan scope (`docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`) is already narrow; this pass exists to prevent the S6-owned machinery visible in `contracts/runtime-execution-fabric.md` from being pulled forward merely because it lives in the same contract file.

## 1. Host/runner identity model

### Full distributed Server/Host/Runner/Worker/Attempt fleet model now

**Reject.** S3 is single local host. Distributed enrollment (FR-057) has no user or product need at this gate.

### Collapse Host and Runner into one identity

**Reject.** `contracts/runtime-execution-fabric.md`'s core identity separation rule ("the durable identities/evidence MUST remain distinct wherever the trust question differs") applies even in a one-process tracer bullet: a host-opt-in decision and a runner-liveness fact answer different trust questions.

### Selected minimum

`ServerDescriptor`/`HostDescriptor`/`RunnerDescriptor` as three distinct, minimal record types, scoped to one local host, with every distributed/multi-tenant field dropped.

## 2. Process-tree identity

### Raw OS PID as identity

**Reject.** PIDs are reused after process exit; using a bare PID as durable identity creates exactly the misattribution class S1/S2 already learned to avoid with other weak identifiers (canonical path, remote URL).

### Full distributed process-registry service

**Reject.** No second durable process, no network, no daemon is needed to track one host's process trees.

### Selected minimum

`ProcessTreeIdentity` pairing `os_process_id` with `os_process_start_time` (or an equivalent OS-provided non-reusable token) plus a local `ownership_epoch` counter.

## 3. Containment model

### Single `sandboxed` boolean

**Reject.** `contracts/runtime-execution-fabric.md` explicitly prohibits this for acceptance/security decisions, and the master plan names "Windows-native containment investigation," not "a sandbox flag."

### Full cross-platform containment matrix (Linux namespaces/cgroups/seccomp, macOS sandbox, Windows AppContainer) investigated simultaneously

**Reject for S3 minimum.** WePLD is desktop-first/Windows-first (`AGENTS.md` product thesis). Investigating every backend now is unbounded discovery work with no current product need; Linux/macOS remain explicit `NONE`/`UNKNOWN` until their own gate.

### Selected minimum

`ContainmentPosture`/`ContainmentCapabilityReport` typed per-dimension, Windows Job-Object-class investigation only for this package, every other dimension/platform explicit `NONE`/`UNKNOWN`.

## 4. Runtime ceiling / resource admission

### Full deployment/tenant/cost ceiling model (multi-tenant `max_cost`, `max_credential_class`, cross-deployment intersection)

**Reject.** No tenant, no deployment fleet, no credential concept exists at S3. `contracts/runtime-execution-fabric.md`'s `RuntimeCeiling` fields for credential class and cost are dropped.

### No ceiling at all ("trust the caller")

**Reject.** `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md` names the effect envelope as core S3 scope specifically because an unbounded caller is the failure mode this package exists to prevent.

### Selected minimum

A single-host `RuntimeCeiling` (process/CPU/memory/output/wall-clock bounds, no network, no credential, no cost fields) and the intersection rule.

## 5. Environment exposure

### Full vendor/adapter-family secret-allowlist taxonomy

**Reject.** No harness/vendor adapter exists in S3; `adapter_family_allowlist` from the parent contract is dropped.

### No environment policy ("inherit ambient environment, filter later")

**Reject.** Ambient inheritance is exactly the leak class FR-048/SR of the parent contract exists to prevent, and S2 already established the "no raw secret capture" precedent this package must not regress.

### Selected minimum

`EnvironmentExposurePolicy` with baseline allowlist, explicit per-launch passthrough, forced/scrub values, and prohibited secret classes — shape only, no concrete values frozen yet.

## 6. Effect proposal / PEP / result

### General-purpose command execution API now

**Reject.** This is exactly the authority `constitution.md` C10 and `clarify.md` Q2 defer. A closed `proposed_effect_kind` enum is the minimum shape that lets later slices build on a stable seam without granting execution now.

### No seam at all — let S6 invent one later

**Reject.** The master plan names the effect envelope and the PEP seam as S3's own deliverable specifically so S6 does not have to retrofit authority discipline onto an already-built execution path. Building the seam narrow-but-real now is smaller in total system cost than building execution first and bolting on authority later (the class of defect `ARCHITECTURE_INVARIANTS.md` "Findings never grant... authority" exists to prevent).

### Full Cedar/OPA-class policy engine now

**Reject.** `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md` explicitly assigns "Cedar candidate evaluation" to `S6-N`, not S3. A full policy language/engine here would duplicate that later work and create two effect-authority systems, which `constitution.md` C8 forbids.

### Selected minimum

`EffectProposal`/`PEPDecision`/`EffectResult` typed envelopes; a PEP seam interface with, at most, a narrow fail-closed self-test evaluator for internal contract testing only.

## 7. Cancellation

### Unbounded blocking wait for process exit

**Reject.** Same class of availability defect S2's Q28/lock-acquisition finding already established for this codebase: an untrusted or hung peer must not be able to convert an ordinary operation into an indefinite hang.

### A generic distributed cancellation/saga framework

**Reject.** One host, one process tree at a time in this package's scope; no saga/workflow engine is needed to cancel a bounded local operation.

### Selected minimum

A bounded cancellation contract (request → bounded wait → `CANCELLED`/`UNKNOWN`), exact deadlines deferred to measurement at the implementation-authority stage (mirroring S2's evidence-backed-tuning precedent for its lock deadline).

## 8. Process spawning

### Admit a process-spawn adapter as part of this planning package's first successor

**Reject.** Mirrors S2's Q9 Git-adapter deferral exactly: starting a process is an effect, and effect authority is not planning's to grant. `plan.md` §7 Route A is specified but explicitly excluded from the first (`S3-AUTH-C`) successor.

### Never specify a spawn path at all, even as future design

**Reject.** Some forward shape is required so a later authorized successor is not designed from nothing; a seam is not implementation authority (`constitution.md`, closing line of C11).

### Selected minimum

`SPAWN_PROCESS_TREE` exists as one closed-enum value in `EffectProposal.proposed_effect_kind`; its concrete argv/admission contract is `plan.md` §7 Route A, explicitly deferred to a separate `S3-AUTH-SPAWN` stage.

## 9. Windows API binding

### Add `windows-rs`/`winapi` (or an equivalent) now

**Reject for this planning package.** No dependency admission occurs during planning. The exact crate/version choice is `S3-AUTH-HOST`'s Source Acquisition Check decision, informed by which crate is already Microsoft-official/maintained versus legacy.

## 10. Distributed/multi-host runner fencing

**Reject for S3.** `contracts/runtime-execution-fabric.md` FR-058 explicitly names this S6+ scope once runners are distributed. S3 specifies only a local ownership-epoch check sufficient for a single host.

## 11. Credential brokering

**Reject for S3.** No credential concept of any kind exists in this package; `CredentialCapability` is entirely S6+/AU-track scope.

## 12. Harness/worker protocol adapters

**Reject for S3.** `HarnessProtocolAdapter`/`HarnessDialectExtension` are explicitly S6 Mission Runtime/UWC scope in `contracts/runtime-execution-fabric.md`'s own `PRIMARY_OWNERS` header.

## 13. Native desktop bridge (`NativeBridgeCapability`)

**Reject for S3.** This is a Desktop-SPA-to-native-IPC boundary concern, materially different from server/host/runner process ownership; it does not belong in this package even though it shares a contract file with the S3-owned types.

## 14. Runtime event identity / causal replay (FR-059)

**Reject for S3.** This concerns distributed event delivery across server/host/runner boundaries once runners are remote. A single local host has no duplicate-delivery/reconnect-replay problem to solve yet.

## 15. Exact harness execution identity (FR-060)

**Reject for S3.** No AI harness/worker exists to identify at this gate; this is S6 scope.

## 16. Behavior-policy layer (`contracts/behavior-policy-boundary.md`)

**Reject for S3.** A future cost/workflow/safety policy layer is explicitly a *narrowing* layer on top of Nawat, not part of the PEP seam itself. Building it now would risk exactly the "second effect-authority system" `constitution.md` C8 and FR-061 prohibit.

## 17. One broad S3 implementation authorization

**Reject.** Mirrors S2's Ponytail §39 finding exactly: too much authority at once, inconsistent with the proven S1/S2 staged-admission precedent.

### Selected staged strategy

1. **S3-AUTH-C:** contracts-only paths/tests, no Core runtime effects/Windows API/process/network/model/new dependencies by default.
2. **S3-AUTH-HOST:** read-only host/containment qualification after contracts are canonical.
3. **S3-AUTH-OBSERVE:** bounded observation-only effects after host qualification is canonical.
4. **S3-AUTH-SPAWN:** optional, separately qualified process-spawn adapter.

## 18. Current dependency posture

```text
NEW_RUNTIME_DEPENDENCIES = NONE_PREFERRED
EXISTING_ADMITTED_SERIALIZATION = wepld-contracts -> serde + serde_json
WINDOWS_API_BINDING = LATER_S3_AUTH_HOST_CANDIDATE_NOT_ADMITTED_DIRECTLY
PROCESS_SPAWN_MECHANISM = LATER_S3_AUTH_SPAWN_CANDIDATE_NOT_ADMITTED_DIRECTLY
DATABASE = REJECT
ASYNC_RUNTIME = REJECT_FOR_S3_MINIMUM
CREDENTIAL_BROKER = REJECT_FOR_S3
DISTRIBUTED_FENCING = REJECT_FOR_S3
```

Any exception must be justified by a concrete failing requirement and separately admitted.

## 19. Ponytail residual questions converted to tasks

- exact contract source path allowlist for `S3-AUTH-C`;
- exact Windows Job-Object API surface and candidate binding crate for `S3-AUTH-HOST`;
- measured cancellation deadline/poll-interval defaults once Job-Object termination behavior is characterized;
- exact `ownership_epoch` representation (counter vs. opaque token vs. OS handle generation);
- exact `SPAWN_PROCESS_TREE` argv allowlist shape, if and when `S3-AUTH-SPAWN` is authorized;
- concrete narrow self-test PEP evaluator rule set for internal contract tests only.

These are explicit tasks in `tasks.md`; they are not permission to overbuild.

## 20. Final minimum-sufficient result

This planning package deliberately adds **only** the mechanisms the master plan names for S3:

```text
host/runner/process-tree identity separation, for one local host
process-tree identity beyond a raw PID (start-time + ownership epoch)
multidimensional containment reporting, Windows-first
runtime-ceiling intersection rule
deny-by-default environment-exposure shape
effect-proposal / PEP-decision / effect-result envelope, closed-enum bounded
bounded cancellation contract
```

No credential broker, harness adapter, native bridge, distributed fencing, event-replay system, behavior-policy layer, or process-spawn execution authority is required to satisfy S3's own named scope. That is the Ponytail justification for this plan.
