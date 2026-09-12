# S3 Clarifications

## Status

```text
CLARIFICATION_STATUS = COMPLETE_FOR_PLANNING_CANDIDATE
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

## Q1 — Does S3 implement a working Terminal the user can interact with?

**Decision:** No. "Terminal Fabric" names the future subsystem this package lays prerequisites for. S3 specifies the effect-proposal/result envelope, process-tree identity, containment reporting, and the PEP seam — not a PTY, not a terminal UI, and not a product-level automation engine.

## Q2 — Does S3 grant authority to actually spawn a process right now?

**Decision:** No. This package specifies the `EffectProposal`/`PEPDecision`/`EffectResult` shapes and the `SPAWN_PROCESS_TREE` closed-enum kind exists in the domain model, but no concrete argv/command allowlist is frozen here, and no implementation authority to actually call an OS process-creation API is granted by planning. That is a separately governed successor decision, exactly as S1-003/S1-004/S1-005 staged Rust dependency/component admission and S2's Q9 staged the Git-adapter question.

## Q3 — What exactly does "process ownership" mean at this gate?

**Decision:** Durable, non-PID-confusable identity (`ProcessTreeIdentity`) for a process tree WePLD itself spawned, plus an ownership epoch that lets a later effect proposal be refused once that ownership is superseded. It does not mean generalized system process monitoring, and it does not mean containment enforcement is proven — only that containment is *reported* per dimension with explicit evidence.

## Q4 — Does S3 claim authority over processes WePLD did not spawn?

**Decision:** No. `ProcessTreeIdentity` and the effect-result path apply only to process trees created through an `EffectProposal` this package's seam admits. S3 does not specify or claim any observation/ownership authority over pre-existing or foreign OS processes; that would be a materially different (and much broader) privacy/security surface requiring its own constitution and threat model.

## Q5 — Can the PEP's default evaluator, if specified, ever return `ALLOW`?

**Decision:** Only for a narrow, explicitly enumerated, internally-testable rule — never as a general policy evaluator, and never wired to a real user-facing surface without a separately governed authority transition. `PEP_SEAM_PRESENT != POLICY_ENGINE_COMPLETE` (constitution C8) governs this: if plan.md specifies any concrete default rule at all, it must be narrow enough that its absence changes nothing about later S6-N policy-engine design, and it must default every unrecognized/unevaluable case to `UNKNOWN_FAIL_CLOSED`.

## Q6 — Is a real Windows Job Object binding implemented by this package?

**Decision:** No. S3 planning specifies the `ContainmentCapabilityReport`/`ContainmentPosture` shapes and the requirement that Windows Job-Object-class containment be investigated first. Binding to an actual Windows API (via `windows-rs`, `winapi`, or an equivalent) is a Source Acquisition Check decision for a later implementation-authority tranche, not this planning package.

## Q7 — Are AppContainer / restricted tokens / other stronger Windows sandboxing primitives claimed?

**Decision:** No. Baseline investigation targets Job-Object-class process-tree containment. Stronger Windows primitives are recorded as explicit future investigation candidates in `plan.md`; this package does not claim they are evaluated or available.

## Q8 — Is distributed/multi-host runner fencing in scope?

**Decision:** No. `contracts/runtime-execution-fabric.md` FR-058 (lease/epoch/fencing for distributed, restartable runners) is explicitly S6+ scope once runners are distributed. S3 specifies only a *local*, single-host ownership-epoch check (FR-014 in `spec.md`) sufficient to refuse a stale-owner effect proposal on the same host.

## Q9 — Does S3 handle credentials in any form?

**Decision:** No. `CredentialCapability` is entirely out of scope. No S3 domain type references a secret, token, or credential broker.

## Q10 — Does S3 specify a generic harness/worker protocol adapter?

**Decision:** No. `HarnessProtocolAdapter`/`HarnessDialectExtension` are S6-owned (Mission Runtime/UWC). S3's `RunnerDescriptor` represents only a local execution-runtime instance capable of owning a process tree; it has no protocol-adapter or worker-family fields.

## Q11 — Does S3 name Cedar or any specific policy language for the PEP?

**Decision:** No. `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md` names "Cedar candidate evaluation" under `S6-N`, not S3. The `PEPDecision.decision_source` field in this package is policy-language-agnostic; naming a concrete evaluator technology is S6-N's decision.

## Q12 — Is a `ContainmentCapabilityReport` produced automatically when Desktop connects, before any user opt-in?

**Decision:** No. Per FR-001/FR-004, the report is produced only as part of an explicit host-qualification step that follows explicit host execution opt-in (`HostDescriptor.host_execution_opt_in_state = true`). Profiling the machine's containment capability before consent is exactly the kind of silent registration `HOST_REGISTERED != HOST_QUALIFIED` (and the S2-precedent "no hidden repository mutation" posture) is meant to prevent.

## Q13 — Does planning freeze exact `RuntimeCeiling` numeric defaults (max processes, wall-clock bound, etc.), the way S2 froze lock-acquisition timing?

**Decision:** Not in this package. S2's `LOCK_ACQUIRE_DEADLINE_MS`/`LOCK_POLL_INTERVAL_MS` defaults had direct precedent (OS lock semantics, well-understood polling). S3's numeric ceilings depend on Windows Job-Object measurement this package has not yet performed. `plan.md` must either propose measured/justified candidate defaults or explicitly defer them to the implementation-authority tranche; `spec.md`'s domain model intentionally leaves these fields typed but unpopulated with concrete numbers.

## Q14 — Does `EffectResult.outcome = UNKNOWN` ever get silently rewritten to `EXECUTED`/`REFUSED` once the true outcome becomes known?

**Decision:** No. Per FR-017 and the `EffectDependency` rules, reconciling an `UNKNOWN` outcome is itself a separate, explicitly evidenced effect (mirroring `contracts/runtime-execution-fabric.md`'s "compensation is a separate effect" rule). The original `EffectResult` record is never mutated in place; a later reconciliation record supersedes it with its own evidence and timestamp.

## Q15 — How does cancellation actually terminate a Windows process tree — is a specific API frozen now?

**Decision:** No. Planning requires only that whichever mechanism a later implementation chooses (e.g., `TerminateJobObject` versus per-process `TerminateProcess`) satisfies the bounded-cancellation contract (FR-013) and correctly bounds the *entire* process tree, not merely the top-level process. The exact API choice is implementation, gated by Source Acquisition/Ponytail like any other mechanism decision.

## Q16 — What does independent-review unavailability mean for this package's acceptance?

**Decision:** It is not PASS, exactly as S2's Q31 decided. Review evidence must identify a qualified independent reviewer and exact base/head coverage. If no qualified reviewer can complete, record `REVIEW_BLOCKED`; planning remains unaccepted.

## Q17 — Does canonical planning acceptance for this package grant S3 implementation authority?

**Decision:** No, exactly as every prior slice's planning merge did not grant implementation authority (P0/S1/S2 precedent, restated in `constitution.md`'s Authority section). A separately governed successor policy must grant exact S3 implementation paths/effects/dependencies before any code.

## Q18 — What is the preferred first implementation-authority tranche after this planning package is canonical?

**Decision:** **Read-only host/containment qualification only** — a tranche that implements `HostDescriptor`/`ContainmentCapabilityReport`/`ContainmentPosture` production (the Windows Job-Object investigation and reporting) with no `EffectProposal` execution path at all. This mirrors S1's staged dependency-resolution precedent and S2's Q32 "contracts-only first" precedent: prove the observation/reporting layer is correct and safe before granting any authority to actually spawn or own a process tree. `SPAWN_PROCESS_TREE` admission is a later, separately justified tranche.
