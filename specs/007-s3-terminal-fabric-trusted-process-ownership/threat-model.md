# S3 Threat Model — Terminal Fabric + Trusted Process Ownership

## 1. Scope

S3 introduces a new trust boundary: WePLD begins owning/observing operating-system process trees and checking effect proposals against a policy-enforcement seam before any effect proceeds. Everything upstream of `HostDescriptor.host_execution_opt_in_state = true` is untrusted-by-default; everything a spawned/observed process does is potentially adversarial input (its exit code, output, and liveness signals). The PEP seam's real decision-making authority does not exist yet in this package — it is a fail-closed interface only — so this threat model treats "the PEP has no real policy behind it yet" as a known, explicit condition, not a residual surprise.

This threat model is planning evidence. It grants no implementation/effect authority.

## 2. Assets

- correctness of process-tree identity (no PID-reuse misattribution);
- correctness of ownership-epoch enforcement (no stale-owner effect injection);
- accuracy of containment-capability claims (no overclaimed isolation);
- the fail-closed property of the PEP seam;
- runtime ceiling integrity (no silent widening);
- environment/secret privacy for any process WePLD spawns;
- bounded cancellation (no indefinite hang, no orphaned process tree);
- absence of unauthorized network access;
- future authority separation between the PEP seam and the real S6-N policy engine.

## 3. Trust boundaries

### TB-1 — Desktop/Core connection → host opt-in

Merely connecting Desktop to Core (S1) is untrusted with respect to execution authority; it must not itself create host/runner state.

### TB-2 — host/OS → `ContainmentCapabilityReport`

The OS's own reported capability (API availability, version) is the input; a hostile or misconfigured environment could misreport, and the qualification step must not simply trust a strong-looking answer without evidence.

### TB-3 — caller → `EffectProposal`

Any future caller (initially only internal contract tests; eventually S6 Mission Runtime) is a source of a proposal that must not be trusted merely because it exists.

### TB-4 — `EffectProposal` → PEP seam

The PEP seam's `decision_source` must be WePLD-owned and trusted; nothing repository-controlled or untrusted-content-derived may reach it.

### TB-5 — PEP seam → `EffectResult`

An `EffectResult` claiming `EXECUTED` is a strong claim; it must be traceable to exactly one `ALLOW` decision and one process-tree effect, never fabricated or inferred.

### TB-6 — spawned/observed process tree → trusted core

Once a process exists, its exit code, stdout/stderr, and liveness signals are untrusted external input, exactly as a repository's Git config was untrusted input to S2.

### TB-7 — core contracts → future consumers (S4/S6/S7)

A future Doctor-class or Mission-Runtime consumer of these contracts must not receive a schema that lets it confuse a containment *report* with a containment *guarantee*, or a PEP `ALLOW` with a Nawat grant.

## 4. Threats and mitigations

### T-001 — Silent execution-host registration

**Attack:** Loading Desktop or opening a project (S1/S2 actions) is misread as consent to execute processes.

**Mitigation:** `host_execution_opt_in_state` defaults false; only an explicit, distinct action sets it (FR-001); no S1/S2 code path is specified to set it.

### T-002 — Containment badge inflation

**Attack:** A Job Object being present is represented as full sandboxing (filesystem/network isolation included).

**Mitigation:** `ContainmentPosture` is multidimensional; `PROCESS_TREE_ONLY != HARD_FILESYSTEM_ISOLATION`/`!= NETWORK_ISOLATION` is an explicit invariant (FR-006); filesystem/network default `NONE`/`UNKNOWN` for the Job-Object backend unless separately evidenced.

### T-003 — Unqualified host claims stronger containment than proven

**Attack:** A host with no completed qualification, or an unrecognized OS version, is treated as having at least baseline containment.

**Mitigation:** `qualification_state != qualified` blocks any stronger-than-`UNKNOWN` claim (FR-004); unrecognized OS/backend versions fail closed to `UNKNOWN` (FR-019).

### T-004 — PID reuse misattribution

**Attack:** A process exits, its PID is reused by an unrelated process, and an effect proposal or cancellation targets the wrong process.

**Mitigation:** `ProcessTreeIdentity` binds PID with start-time/equivalent non-reusable token (FR-003); adversarial fixture required (`plan.md` §8).

### T-005 — Stale-owner effect injection

**Attack:** A runner is restarted/replaced, but a caller still holding a reference to the old ownership state submits a further effect proposal against the process tree.

**Mitigation:** `ownership_epoch` bump on qualified restart/replacement; a proposal bound to a stale epoch is refused, never silently rerouted (FR-014).

### T-006 — PEP fail-open regression

**Attack:** Missing, malformed, or stale policy input is misread as an implicit allow.

**Mitigation:** `UNKNOWN_FAIL_CLOSED` is the mandatory outcome for any unevaluable decision (FR-011); `EffectResult` cannot be `EXECUTED` without a resolved `ALLOW` (FR-010).

### T-007 — PEP seam mistaken for the real policy engine

**Attack:** A future consumer (or a careless implementation) treats a narrow planning-only self-test evaluator's `ALLOW` as equivalent to a genuine S6-N Nawat grant.

**Mitigation:** `PEP_ALLOW != NAWAT_GRANT` and `PEP_SEAM_PRESENT != POLICY_ENGINE_COMPLETE` are explicit invariants (constitution C8, spec §4.10); any planning-only evaluator must be documented as a test double, never wired to a real surface (`plan.md` §5.1, `ponytail.md` §6).

### T-008 — Runtime ceiling widened by lower-trust configuration

**Attack:** Agent/repository/worker configuration attempts to widen `RuntimeCeiling` beyond its frozen value.

**Mitigation:** the effective envelope is an intersection, never a union (FR-007); an empty intersection blocks the proposal rather than silently narrowing to "close enough."

### T-009 — Ambient environment/secret leakage into a spawned process

**Attack:** A future implementation inherits the parent's full environment (the `std::process::Command` default, per `source-acquisition.md` §2) into a spawned process, leaking ambient secrets.

**Mitigation:** `EnvironmentExposurePolicy` is deny-by-default; only `baseline_allowlist` plus explicit passthrough reaches the child (FR-008); this package flags the stdlib default as a known gap the implementation must explicitly override, not rely on.

### T-010 — Indefinite cancellation hang

**Attack:** A hung or adversarial process ignores termination and a cancellation request waits forever.

**Mitigation:** bounded cancellation contract (FR-013); `UNBOUNDED_CANCELLATION_WAIT = PROHIBITED` (`plan.md` §4.4); cancellation must cover the entire process tree via the Job-Object termination mechanism, not merely the top-level process (closing `Child::kill`'s known gap, per `source-acquisition.md` §2).

### T-011 — Orphaned process tree on ownership loss

**Attack:** The owning runner crashes/restarts, leaving a spawned process tree running with no owner able to cancel or account for it.

**Mitigation:** `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`-class behavior is named as the qualification target for this property (`source-acquisition.md` §3); this package requires the property, not a specific implementation, since the API binding is not admitted here.

### T-012 — Unknown effect outcome silently rewritten

**Attack:** An `EffectResult` with `outcome = UNKNOWN` is later overwritten in place with `EXECUTED` or `REFUSED` once assumed to be known, without new evidence.

**Mitigation:** reconciliation is a separate, explicitly evidenced record (`clarify.md` Q14); the original `UNKNOWN` record is never mutated in place.

### T-013 — Irreversible dependent effect started against an unknown prerequisite

**Attack:** A composite effect proceeds to an irreversible step while its prerequisite's outcome is still `UNKNOWN`.

**Mitigation:** `EffectDependency` blocking rule: `PREREQUISITE_EFFECT_OUTCOME_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_NOT_STARTED` (FR-017).

### T-014 — Hidden network access through a spawned process

**Attack:** A spawned process, or the qualification/containment logic itself, performs network I/O.

**Mitigation:** `NETWORK_AUTHORITY = NONE` throughout (constitution C1); `max_network_class`/`current_network_state` fixed `NONE` (FR-016); no S3 domain type or FR grants network access.

### T-015 — Scope creep into observing foreign (non-WePLD-spawned) processes

**Attack:** An implementation extends `ProcessTreeIdentity`/observation to arbitrary pre-existing OS processes, silently expanding into system-wide process monitoring — a materially larger privacy/security surface than this package's threat model covers.

**Mitigation:** `clarify.md` Q4 explicitly excludes this; `ProcessTreeIdentity` applies only to process trees created through an admitted `EffectProposal`.

### T-016 — Distributed-fencing gap mistaken for solved

**Attack:** A future distributed/multi-host deployment reuses the single-host `ownership_epoch` mechanism as if it were sufficient cross-host fencing (FR-058-class protection), when it has not been designed or qualified for that.

**Mitigation:** `constitution.md` C9 and `clarify.md` Q8 explicitly scope the epoch mechanism to a single host and name distributed fencing as separate, unimplemented S6+ scope; this package's own evidence must not be cited as satisfying FR-058.

### T-017 — Vendor/provider `sandboxed` label trusted directly

**Attack:** A future adapter or library reports its own `sandboxed: true` claim, and that claim is used directly as `ContainmentPosture` without independent qualification.

**Mitigation:** `PROVIDER_SANDBOX_LABEL != CONTAINMENT_POSTURE` (spec §4.6); containment evidence must derive from WePLD's own qualification step (`source-acquisition.md` §3, SR-003).

### T-018 — Candidate governance self-authorizes planning

**Attack:** Candidate text/checks in this PR are treated as trusted completion authority before trusted-base admission/Ready/post-merge activation.

**Mitigation:** record exact live base/main/head; trusted-base admission required; candidate policy cannot self-authorize; Ready-triggered admission reread; guarded merge; post-merge `foundation-integrity` on canonical main (same discipline as S2's T-043).

### T-019 — Reviewer unavailability silently becomes approval

**Attack:** A requested/pending/rate-limited reviewer is treated as clean.

**Mitigation:** explicit `REVIEW_BLOCKED`; require reviewer qualification, exact-head coverage, and completed state (same discipline as S2's T-044, and this session's own live CodeRabbit-rate-limit handling on PR #335).

## 5. Abuse-case acceptance tests

At minimum, implementation qualification must include negative tests proving:

1. no `HostDescriptor` with `host_execution_opt_in_state = true` exists after ordinary Desktop/Core connection or S2 project opening;
2. an unqualified host cannot produce a `ContainmentPosture` stronger than `UNKNOWN` on any dimension;
3. a `PROCESS_TREE_ONLY` containment fixture is never consumed as satisfying a filesystem- or network-isolation requirement;
4. a PID reused by an unrelated process after original-process exit is not matched to the original `ProcessTreeIdentity`;
5. an `EffectProposal` bound to a superseded `ownership_epoch` is refused;
6. an `EffectProposal` with no resolved `PEPDecision`, or with a `DENY`/`UNKNOWN_FAIL_CLOSED` decision, never produces `EXECUTED`;
7. an `EffectProposal` whose constraints intersect to an empty `RuntimeCeiling` envelope is refused, not silently narrowed;
8. a spawned-process fixture (once any spawn path exists) receives no ambient environment variable outside its `EnvironmentExposurePolicy` allowlist;
9. a cancellation request against a live effect resolves to `CANCELLED` or bounded `UNKNOWN` within the documented deadline, and never hangs;
10. cancellation terminates an entire multi-level process tree fixture (child-of-child), not only the top-level process;
11. an `EffectDependency` with `EFFECT_OUTCOME_UNKNOWN` on a prerequisite blocks its irreversible dependent effect;
12. no S3 evidence record — proposal, result, decision, containment report — contains a raw environment value or unredacted process output;
13. no S3 operation performs or requires network access.

## 6. Security review applicability

S3 implementation will touch process creation/termination, OS API surfaces, environment handling, and the effect-authority seam. Therefore:

```text
CODEX_SECURITY_APPLICABILITY = APPLICABLE_TO_IMPLEMENTATION_WHEN_AVAILABLE
MISSING_CODEX_SECURITY = NOT_PASS
```

For this planning-only documentation package, security review examines whether the plan creates unsafe authority or omits required threat classes. No security PASS is asserted merely by planning text.

## 7. Residual risks

- Windows Job Object nesting/behavior varies by OS version and edition; `ContainmentCapabilityReport` must fail closed on anything not explicitly qualified, and cross-version qualification gaps will remain until each version is separately tested;
- the PEP seam has no real policy engine behind it in this package; every `ALLOW` this package could produce is, by design, from a narrow test double — treating that as meaningful authorization would be a defect this threat model exists to prevent, not a claim this package makes;
- `Child::kill`-class single-process termination is a known stdlib gap; until an actual Job-Object binding is qualified and implemented, no implementation of this package's cancellation contract can exist that safely covers a multi-process tree;
- Linux/macOS containment remains entirely `NONE`/`UNKNOWN` after this package; this is an explicit scope limitation, not a solved problem deferred quietly;
- distributed/multi-host fencing (FR-058) is not solved by the local ownership-epoch mechanism and must not be assumed solved by a future S6+ implementer skimming this package's evidence;
- a hostile or buggy caller could flood the PEP seam with proposals; this package specifies no rate-limiting of proposal submission itself, since no real caller exists yet — a future authority stage must address this before any real integration.

Residual risk must be reported; it must not be converted into PASS by optimistic prose.
