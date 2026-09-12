# S3 Implementation Plan — Planning Candidate Only

## Authority header

```text
CANONICAL_PLANNING_BASE = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
S3_PLANNING_AUTHORITY = EXACT_SPEC_KIT_PACKAGE_ONLY
S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S4_PLUS_AUTHORITY = NONE
```

This document defines the minimum implementation shape to qualify later. It does not authorize source mutation, process spawning, or any Windows API binding.

## 1. Architectural target

```text
Future Mission Runtime / UWC (S6)      Future Doctor/Assurance surfaces (S4/S7)
              \                                     /
               \                                   /
                    Effect Proposal / Result seam
                              |
                       Nawat PEP seam (interface only)
                              |
             Host / Runner / Process-Tree identity + Containment reporting
                              |
                Trusted Rust Core / WePLD contracts
```

S3 makes host/process ownership and the effect seam first-class core concepts, exactly as S2 made project context first-class. Nothing above the PEP seam in this diagram is built by S3; it is drawn only to show why the seam's shape matters to slices that do not exist yet.

## 2. Minimal module ownership candidate

### `crates/contracts`

Own versioned serializable contract types:

- `ServerDescriptor`, `HostDescriptor`, `RunnerDescriptor`;
- `ProcessTreeIdentity`;
- `ContainmentCapabilityReport`, `ContainmentPosture`;
- `RuntimeCeiling`, `EnvironmentExposurePolicy`;
- `EffectProposal`, `PEPDecision`, `EffectResult`, `EffectDependency`.

Existing admitted `serde`/`serde_json` remain the preferred serialization substrate, exactly as S2 used them. No new package is granted by this plan.

### `crates/core`

Candidate modules, subject to later exact-path authority:

```text
runtime/
  host.rs
  runner.rs
  process_tree.rs
  containment.rs
  ceiling.rs
  environment.rs

effect/
  proposal.rs
  pep.rs
  result.rs
  dependency.rs
```

The exact filenames must be fixed by later implementation-authority bootstraps; this planning package must not create them.

## 3. Host/effect algorithm candidate

### Phase I — explicit host opt-in

1. present an explicit, unambiguous opt-in action distinct from ordinary Desktop/Core connection or S2 project opening;
2. record `HostDescriptor.host_execution_opt_in_state = true` only after that action;
3. no containment investigation, no `RunnerDescriptor`, and no `EffectProposal` may exist before this state is true.

### Phase II — host/containment qualification

If host opt-in is true:

1. observe `os_platform_identity`/`os_version_identity`;
2. investigate the Windows Job-Object-class backend first (§7);
3. produce a `ContainmentCapabilityReport` recording, per dimension, the qualified strength or `NONE`/`UNKNOWN`;
4. derive at least one `ContainmentPosture` from that report;
5. set `HostDescriptor.qualification_state` accordingly, with an explicit `qualification_expiry`.

No process is spawned during qualification. Qualification is observation of the host, not of any particular effect.

### Phase III — runner/ceiling establishment

1. establish exactly one `RunnerDescriptor` bound to the qualified `HostDescriptor` for the initial single-host tracer bullet;
2. bind a `RuntimeCeiling` and an `EnvironmentExposurePolicy` to that runner;
3. `current_network_state` and `max_network_class` are fixed `NONE`.

### Phase IV — effect proposal / PEP / result

1. a caller constructs an `EffectProposal` with a closed `proposed_effect_kind`;
2. the proposal is evaluated by the PEP seam, producing exactly one `PEPDecision`;
3. `ALLOW` may proceed toward an `EffectResult`; `DENY`/`UNKNOWN_FAIL_CLOSED` produce `REFUSED` directly;
4. a proceeding effect creates/updates a `ProcessTreeIdentity` and records its `ownership_epoch`;
5. cancellation, completion, or unknown-outcome reconciliation each produce their own `EffectResult`/successor record; none mutates a prior result in place.

Do not use a raw OS PID, a descriptor label, or a vendor `sandboxed` claim as authority at any phase.

## 4. Containment/host-qualification candidate

### 4.1 Windows-first investigation target

The initial qualified backend candidate is a Job-Object-class mechanism (Windows `CreateJobObject`/`AssignProcessToJobObject`/`SetInformationJobObject`/`QueryInformationJobObject`/`TerminateJobObject` family, exact API surface subject to Source Acquisition Check). It is investigated for `process_tree_strength` only; `filesystem_strength` and `network_strength` for the same backend default to `NONE`/`UNKNOWN` unless a separate mechanism is qualified and evidenced.

### 4.2 Qualification is idempotent and re-runnable

Re-running host qualification must not require re-opting-in. It must be safe to call repeatedly (e.g., after `qualification_expiry` or a detected OS update) and must always produce a report consistent with the host's actual current capability, never a cached stronger claim.

### 4.3 Ownership-epoch candidate

```text
ownership_epoch: monotonically increasing per RunnerDescriptor
epoch bump triggers: runner_runtime_restart, runner replacement, explicit revocation
STALE_EPOCH_PROPOSAL -> REFUSED (never silently rerouted to the new epoch)
```

The exact epoch representation (integer counter, opaque generation token, or OS-provided handle generation) is an implementation decision; the semantic guarantee above is the planning contract.

### 4.4 Bounded cancellation candidate

Planning freezes the shape of the cancellation contract, not final numeric bounds (per `clarify.md` Q13):

```text
CANCELLATION_REQUEST -> bounded wait -> CANCELLED | UNKNOWN(timeout)
CANCELLATION_SCOPE = entire process tree, not only the top-level process
UNBOUNDED_CANCELLATION_WAIT = PROHIBITED
```

Exact deadline/poll-interval defaults are deferred to the implementation-authority tranche once Job-Object termination behavior has been measured, mirroring how S2 deferred its Git-adapter timeout to Route A admission.

### 4.5 Corruption / staleness strategy

- an unrecognized/unsupported OS version report is `UNKNOWN`, never assumed capable;
- a `ContainmentCapabilityReport` past `expires_at` is stale and must be re-qualified before it backs a new `EffectProposal`;
- a `ProcessTreeIdentity` whose liveness cannot be confirmed is `UNKNOWN`, never silently treated as `live` or `exited`;
- destructive cleanup of stale records is not automatic and is not part of S3 minimum.

## 5. Nawat PEP seam plan

The PEP seam is rule-based and interface-only in S3, exactly as Doctor was rule-based and deterministic in S2 — but unlike Doctor, the PEP seam's *authority* is explicitly not owned by this package.

### 5.1 Minimal internal self-test evaluator (planning-only)

If `plan.md`/`tasks.md` specify any concrete `decision_source` implementation at all for internal contract testing, it must:

- be a narrow, explicitly enumerated allowlist (e.g., a fixed set of test-only `proposed_effect_kind`/host combinations);
- default every unenumerated case to `UNKNOWN_FAIL_CLOSED`;
- never be wired to a real product surface, S6 Mission Runtime, or any user-facing command;
- be clearly labeled as a test double, not a policy engine, in its own contract documentation.

### 5.2 Decision record integrity

`PEPDecision` records are append-only and reference a `policy_snapshot_ref`. A later change to the (still-unimplemented) real policy engine does not retroactively alter a previously recorded decision; it only affects future proposals under the revalidation triggers in `spec.md` FR-015.

## 6. Internal seam plan (no CLI surface)

S3 has no command of its own. Per `spec.md` §2, its outcome is enabling later slices, not a direct user interaction. `crates/contracts` types defined here are consumed internally by:

- a future S4/S7 Doctor-class surface that may report host/containment health (out of S3 scope to build; only the types must be stable enough to be referenced later);
- the future S6 Mission Runtime, which will be the first actual caller of `EffectProposal`.

No `wepld` CLI subcommand is added, changed, or reserved by this package.

## 7. Process-spawn admission gate

Exactly as S2 split Git-topology accuracy into a deferred adapter decision, S3 splits `SPAWN_PROCESS_TREE` into a deferred admission decision.

### Route A — qualified process-spawn adapter (deferred; not part of the first successor)

Before any admission:

- exact allowlisted argv shape (no shell string, no arbitrary command);
- resolved absolute executable invocation, rejecting project-local spoofed executables (mirroring S2's Git-executable-trust rule);
- explicit environment contract derived from `EnvironmentExposurePolicy` (deny-by-default, no ambient inheritance);
- Job-Object assignment before the child can execute meaningfully, to avoid an unowned window;
- bounded stdout/stderr capture with hard byte ceilings;
- bounded wall-clock timeout with cancellation wired to the entire process tree, not just the top-level process;
- no network, no hooks, no interactive prompt, no pager;
- exit-code/signal mapping into `EffectResult.exit_status`;
- adversarial/fuzz tests for the argv/environment boundary.

`SPAWN_PROCESS_TREE` admission is **not** part of the preferred first S3 implementation-authority successor (see §11).

### Route B — observation-only fallback

If spawn authority is denied or deferred indefinitely, S3 implementation still delivers `OBSERVE_PROCESS_TREE`/`REQUEST_CANCELLATION` for host/containment qualification value alone, with `SPAWN_PROCESS_TREE` left entirely unimplemented and explicitly reported as unavailable rather than approximated.

A later authority bootstrap chooses when (not whether) Route A opens; this plan does not self-authorize it.

## 8. Deterministic qualification matrix

Required test classes before S3 implementation acceptance:

### Unit/contract

- `PEPDecision` outcome derivation (`ALLOW`/`DENY`/`UNKNOWN_FAIL_CLOSED`) for every enumerated and unenumerated input;
- `EffectResult` outcome is never `EXECUTED` without a resolved `ALLOW` decision;
- `ContainmentPosture` per-dimension independence (a `PROCESS_TREE_ONLY` fixture never yields a stronger `filesystem_strength`);
- `RuntimeCeiling` intersection arithmetic, including the empty-intersection-blocks case;
- `EffectDependency` blocking rules for unavailable/`UNKNOWN` prerequisites;
- schema round trips for every new contract type.

### Host/containment adversarial

- Job-Object API unavailable (older Windows, restricted environment, sandboxed test runner) yields `NONE`/`UNKNOWN`, not a default `PROCESS_TREE_ONLY` claim;
- qualification re-run after simulated OS-version change does not reuse a stale stronger report;
- expired `ContainmentCapabilityReport` cannot back a new `EffectProposal`.

### Ownership/identity concurrency

- two proposals racing against the same `ProcessTreeIdentity` after an epoch bump: exactly one is honored under the old epoch's semantics (refused) and the fixture proves no double-effect;
- OS PID reuse simulation: a new unrelated process reusing a just-exited PID is not matched to the prior `ProcessTreeIdentity`;
- cancellation requested concurrently with natural process exit resolves deterministically to one terminal outcome, never both.

### PEP seam

- missing policy snapshot -> `UNKNOWN_FAIL_CLOSED`;
- malformed/stale policy snapshot -> `UNKNOWN_FAIL_CLOSED`;
- an unenumerated `proposed_effect_kind`/host combination against the planning-only self-test evaluator -> `UNKNOWN_FAIL_CLOSED`, never `ALLOW`;
- a `DENY` decision never produces `EXECUTED`.

### Cancellation/bounded waiting

- cancellation resolves within the documented bound under normal load;
- cancellation against a hung/unresponsive process-tree fixture resolves to bounded `UNKNOWN`, not an indefinite wait;
- cancellation scope covers the entire process tree, not only a top-level placeholder process, in any fixture that spawns a child-of-child.

### Platform

- Windows required;
- Linux/macOS: explicit `NONE`/`UNKNOWN` containment evidence recorded rather than assumed absent from the matrix (a limitation, not a silent gap).

## 9. Performance budgets to qualify

Planning targets, not PASS claims:

- host/containment qualification completes in bounded time and does not scale with anything other than the fixed API surface being probed;
- cancellation has a fixed, measured upper bound once Job-Object termination behavior is characterized (§4.4);
- `PEPDecision` evaluation for the planning-only self-test evaluator is O(1) against its fixed allowlist size.

Benchmarks must publish fixture shape and measured bounds before acceptance, exactly as S2 required for its lock-acquisition and evidence-parsing budgets.

## 10. Implementation-authority bootstrap strategy

After this planning package becomes canonical, use staged authority rather than one broad S3 grant, mirroring S1's and S2's precedent.

### Stage S3-AUTH-C — contracts-only preferred first successor

- only exact `crates/contracts` S3 contract modules/exports/tests for `HostDescriptor`/`RunnerDescriptor`/`ProcessTreeIdentity`/`ContainmentCapabilityReport`/`ContainmentPosture`/`RuntimeCeiling`/`EnvironmentExposurePolicy`/`EffectProposal`/`PEPDecision`/`EffectResult`/`EffectDependency`;
- existing admitted contract serialization graph only;
- no `crates/core` runtime behavior;
- no Windows API binding;
- no process spawn;
- no network;
- no new dependency unless a separate focused acquisition/admission gate proves it necessary.

### Stage S3-AUTH-HOST — read-only host/containment qualification

Only after contracts are canonical and separately authorized (per `clarify.md` Q18):

- Windows Job-Object-class investigation and `ContainmentCapabilityReport` production;
- no `EffectProposal` execution path of any kind, including `OBSERVE_PROCESS_TREE`, until this stage's own evidence is qualified;
- this is also the stage that, by requiring native Windows `wepld-core` CI execution for the first time, creates the precondition for closing the adopted `S2-S003` obligation (`clarify.md` Q19) — running S2's existing junction/reparse fixtures for real is not this stage's own deliverable, but this stage must not accidentally stand up native Windows execution without noting that S2-S003 can now be attempted.

### Stage S3-AUTH-OBSERVE — bounded observation only

- `OBSERVE_PROCESS_TREE` and `REQUEST_CANCELLATION` against processes admitted under a later spawn tranche, or against a narrow test-only fixture process, with the PEP seam wired to its planning-only self-test evaluator;
- still no `SPAWN_PROCESS_TREE`.

### Stage S3-AUTH-SPAWN — optional process-spawn adapter

Separate from every stage above. Admit only the exact executable/environment/argv/timeout/cancellation semantics in §7 after its own source/security review. This is the closest analogue to S2's optional Git-adapter stage and carries the same caution.

Every successor remains append-only, preserves frozen predecessors, and must state:

```text
S3_IMPLEMENTATION_AUTHORITY = <exact bounded paths/effects only>
DEPENDENCY_ADMISSION = <none unless separately qualified>
SOURCE_ADMISSION = <none unless separately qualified>
PROCESS_SPAWN_AUTHORITY = <none unless exact later spawn-adapter contract>
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S4_PLUS_AUTHORITY = NONE
```

The canonical plan cannot self-activate a successor.

## 11. Source/research decisions already captured

Non-authoritative research inputs used during this planning package:

```text
specs/006-issueops-agentic-engineering-control-plane/contracts/runtime-execution-fabric.md
  — the S3-owned subset of ServerDescriptor/HostDescriptor/RunnerDescriptor/
    ContainmentPosture/RuntimeCeiling/EnvironmentExposurePolicy this plan reuses.
Official Microsoft Job Objects documentation
  — behavior oracle for process-tree containment semantics; no source admitted.
Omnigent (per contracts/runtime-execution-fabric.md's own source-acquisition note)
  — named as a research-only mechanism quarry for the server/host/runner
    distinction and policy-choke-point shape; no source admitted by this plan.
```

Material decisions incorporated here:

- no Rust crate for Job-Object binding, process spawning, or any Windows API is admitted by this plan; that remains Source Acquisition Check's decision at the S3-AUTH-HOST/S3-AUTH-SPAWN stage;
- contracts-first remains the minimum successor, exactly as S2's Stage S2-AUTH-C;
- distributed/multi-host fencing (FR-058) and credential brokering are not researched here because they are out of S3's scope entirely (`clarify.md` Q8/Q9).

## 12. Delivery sequence

1. reconcile all planning-review findings across this Spec Kit package;
2. rerun exact-head `foundation-integrity`/trusted-base planning admission on the repaired head;
3. record fresh exact-head egress preflight and complete independent rereview;
4. reconcile any new valid material finding and repeat qualification if the head changes;
5. perform final main/base/head/diff/thread/check race verification;
6. mark the planning PR Ready only with exact-head evidence;
7. reread Ready-triggered trusted-base admission and require genuine PASS;
8. guarded merge with expected-head protection;
9. prove post-merge canonical planning activation/`foundation-integrity` on exact `main`;
10. re-read canonical planning and design/qualify the contracts-only S3-AUTH-C successor;
11. implement/qualify S3 contracts first;
12. separately authorize and implement read-only host/containment qualification (S3-AUTH-HOST);
13. separately authorize bounded observation-only effects (S3-AUTH-OBSERVE);
14. separately decide/admit the optional process-spawn adapter (S3-AUTH-SPAWN);
15. adversarial/platform/performance qualification at each stage;
16. independent correctness/security review and bounded repair at each stage;
17. S3 acceptance + Build Learning only with exact evidence, per stage and overall.
