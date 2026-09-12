# S3 Constitution — Terminal Fabric + Trusted Process Ownership

## Authority

This package is created under canonical policy v68 only.

```text
CANONICAL_BASE = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
V68 = CANONICAL_ACTIVE
S3_PLANNING_AUTHORITY = EXACT_SPEC_KIT_PACKAGE_ONLY
S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_RUNTIME_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
ROADMAP_MUTATION = NONE
```

Nothing in this Spec Kit package grants implementation, process execution, source import, dependency mutation, provider/model use, network access, or completion authority. `S2_STATE = CLOSED_CANONICAL` is the trusted precondition this package builds on; re-read canonical `main` live rather than trusting this file.

## Slice purpose

Per `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`'s revised roadmap interpretation and `docs/canonical/MASTER_PLAN_INDEX.md`, S3 adds exactly:

- an effect-proposal / effect-result envelope shape;
- process-tree identity;
- a containment-capability report;
- a Nawat PEP (Policy Enforcement Point) seam, without the full effect-time policy engine;
- a Windows-native containment investigation.

S3 is future-facing foundation for later tracks, not a product feature. Per `specs/006-issueops-agentic-engineering-control-plane/product-capability-tracks-plan.md` §4, S3 supplies: effect proposal/result envelopes; host/process-tree identity; capability observation; containment reporting; bounded cancellation; ownership/fencing prerequisites where process/input ownership exists; and the Nawat enforcement seam — without pulling the full later policy engine backward. **S3 does not implement a product-level automation engine.**

`S3-D` (the non-primary deterministic-assurance-seed gate named in `docs/canonical/MASTER_PLAN_INDEX.md` and `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`) is a distinct, separately gated unit. This package does not claim S3-D scope; a future package must open it explicitly if and when it is authorized.

## Constitutional invariants

```text
Connecting to a server != execution-host opt-in
Host registered != Host qualified
Host qualified != Effect authority
Host online != Runner ready
Requested runner != Qualified runner
Qualified runner != Nawat grant
Runner offline != Safe fallback to another runner
Process-tree containment != Hard filesystem isolation
Process-tree containment != Network isolation
Provider/vendor sandbox label != Containment posture
Containment downgrade != Silent / requires explicit requalification
Runtime ceiling != Widenable by lower-trust configuration
Effective execution envelope = intersection, never union
Dialect/vendor extension != Effect authority
Vendor permission option != Nawat decision
PEP seam existing != Policy engine complete
Route decision != Process-execution authority
Envelope shape defined != Effect executed
ReviewOutcome != CompletionDecision
Green CI != CompletionDecision
Planning != Implementation authority
Candidate policy text != Trusted authority
Review pending != Independent review complete
```

### C1 — Local-first, no network authority at this gate

S3 is local-first and cloud-independent, exactly as S1's handshake and S2's identity/storage foundations are. `NETWORK_AUTHORITY = NONE` at this gate: no distributed/remote host enrollment, no remote runner, no telemetry egress, and no external protocol. Per `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`, "no external protocol is required in S1–S3." Authenticated distributed host enrollment (`contracts/runtime-execution-fabric.md` FR-057) is explicitly future work, not this gate's authority.

### C2 — Explicit, opt-in host/process ownership

Loading WePLD Desktop, opening a project, or connecting Desktop to the Rust Core must never silently register the machine as an execution host or create process-ownership authority. Host execution opt-in must be an explicit, observable state, distinct from mere connection or liveness.

### C3 — Identity separation preserved, scoped to this gate's layer

S3 must preserve distinct identities for at least: host identity and runner/process-tree identity. `HostIdentity != RunnerIdentity` remains true even where an early tracer-bullet implementation collapses them into one process, per `contracts/runtime-execution-fabric.md`'s "core identity separation" rule — the durable identities/evidence must remain distinct wherever the trust question differs. `WorkerIdentity` and `AttemptIdentity` remain owned by `data-model.md` / `worker-delegation.md` and are out of S3's implementation scope except as a forward-compatible seam this package may specify but not build.

### C4 — Containment is multidimensional evidence, never a boolean

A single `sandboxed` boolean must never satisfy a security or acceptance decision. Containment evidence must be reported per dimension — process-tree, filesystem, network, namespace/container, syscall, mount/write, home/config visibility — each independently, with explicit `NONE`/`UNKNOWN` where a dimension is not established. A Windows Job Object-class backend qualifying for process-tree containment does not thereby qualify for filesystem or network isolation.

### C5 — Windows-native containment is the primary qualification target

Consistent with WePLD's desktop-first / Windows-first execution posture (`AGENTS.md` product thesis), S3's containment investigation is Windows-native first. Any cross-platform (Linux/macOS) containment claim must be recorded as explicit evidence or an explicit limitation, never inferred from the Windows result.

### C6 — Runtime ceiling is a hard upper bound

A deployment/operator runtime ceiling is a hard upper bound that lower-trust configuration (agent config, repository content, worker preference) cannot widen. The effective execution envelope is the intersection of every controlling ceiling/constraint/grant, never their union. An empty intersection blocks the attempt; it is never silently downgraded to a smaller-but-nonempty envelope.

### C7 — Deny-by-default environment exposure

Any process S3 spawns or supervises receives a deny-by-default environment. Ambient host environment variables and credentials are not inherited wholesale. This package may specify the `EnvironmentExposurePolicy` shape; it does not admit any concrete secret class or vendor allowlist as implementation.

### C8 — Nawat PEP seam only, not the policy engine

S3 defines the seam at which a proposed effect is checked against an authority decision before proceeding — the Policy Enforcement Point. It does not implement Mirefa route qualification, Edara topology selection, or the full effect-time Nawat policy engine (`S6-N`). A `NO_OBJECTION`/`ALLOW` result from any policy-adjacent mechanism this package specifies must never be treated as a Nawat grant by itself.

### C9 — Bounded cancellation and ownership/fencing prerequisites

Every process this package's contracts describe must be boundedly cancellable; unbounded waits are prohibited (consistent with S1's protocol invariants and S2's lock-acquisition invariants). Where process or input ownership exists, this package specifies the ownership/fencing *prerequisite* shape (a stale owner must not be able to continue accepting effects) as forward-compatible design; it does not implement distributed/restartable-runner fencing (`contracts/runtime-execution-fabric.md` FR-058), which remains S6+ scope once runners are distributed.

### C10 — Effect envelope shape only, no effect execution authority

S3 specifies the effect-proposal/effect-result envelope shape and process-tree/containment observation types. It does not grant Nawat effect authority, does not execute arbitrary commands, and does not implement a Terminal/PTY product feature. "Terminal Fabric" names the future subsystem this package lays prerequisites for; it is not this package's deliverable.

### C11 — Later slices, and S3-D, stay later

S3 does not implement:

- S3-D deterministic assurance seed (separate, non-primary gate);
- S4 Fehrest / semantic Project Graph;
- S5 Spec Kit mechanics / AGILLE / Plan Qualification;
- S6 Mission Runtime / UWC / Mirefa / Edara / full Nawat effect-time authority;
- S7 Native Assurance / AMAN;
- S8 controlled repair / Trusted Completion;
- model/provider execution;
- distributed/remote host enrollment and cross-host runner fencing;
- credential broker secret delivery (only the `CredentialCapability` *shape*, if specified at all, is in scope — never a working broker);
- browser/computer/automation product features;
- arbitrary command/process execution as a user-facing capability.

A minimal seam may be specified only when required to keep future compatibility; a seam is not implementation authority.

## Required build method

```text
constitution
-> specify
-> clarify
-> plan
-> checklist
-> analyze
-> tasks
-> Ponytail FULL
-> Source Acquisition Check
-> separately governed implementation-authority transition
-> minimum sufficient implementation
-> deterministic gates
-> independent review
-> applicable security review
-> finding reconciliation
-> acceptance evidence
-> Build Learning
```

## Planning completion rule

This package can become canonical planning only when **all** of the following are true on the exact final candidate:

1. live PR base SHA and trusted canonical `main` SHA are recorded and match the authorized trusted base;
2. the diff is exactly this package's planning paths under `specs/007-s3-terminal-fabric-trusted-process-ownership/`, and remains spec/planning/research-only;
3. pre-Ready exact-head `foundation-integrity` succeeds;
4. trusted-base `s1-admission-integrity` genuinely accepts the candidate;
5. exact-head external-review egress preflight is recorded per `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`;
6. at least one qualified independent exact-head review completes; if unavailable, state is `REVIEW_BLOCKED` and planning remains unaccepted;
7. every valid material finding is reconciled, and any repair is freshly requalified/reviewed;
8. final race checks confirm canonical main, PR base/head, exact diff, threads, and required checks have not drifted;
9. Ready-triggered trusted-base admission genuinely PASSes on the same exact head;
10. merge uses expected-head protection and no destructive history rewrite;
11. post-merge canonical `main` is re-read and post-merge `foundation-integrity` succeeds on that exact merge head.

Canonical planning still does not imply S3 implementation authority. Candidate governance/bootstrap documents remain non-authoritative until their trusted-base transition is guardedly merged and activation is proven from canonical `main`.
