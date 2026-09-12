# S3 Task Ledger

## Canonical state markers — candidate until merged

```text
SLICE = S3
NAME = Terminal Fabric + trusted process ownership
PLANNING_BASE = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
PLANNING_STATE = DRAFTED_PENDING_EXACT_HEAD_REVIEW
S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
NEXT_AUTHORITY_GATE = S3_PLANNING_ACCEPTANCE (acceptance.md §A)
S2_S003_ADOPTED = YES (acceptance.md §H.1)
```

This ledger lists the dependency-ordered planning-package tasks (§1, largely complete — this is the drafting session) and the future implementation/acceptance task map (§2–§7, entirely `[ ]` because `S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED`). Task-map presence does not activate implementation, exactly as `specs/006-.../PLANNING_INDEX.md` states for its own task maps.

## 1. Planning-package tasks

- [x] **S3-P001** Draft `constitution.md`, scoped to the master-plan-named S3 deliverables and excluding every S6+/credential/harness-adapter/native-bridge/distributed-fencing mechanism that shares a contract file with S3.
- [x] **S3-P002** Draft `spec.md`: problem statement, user outcomes, in/out-of-scope, domain model (S3-owned subset of `contracts/runtime-execution-fabric.md`), functional/security/non-functional requirements, acceptance scenarios.
- [x] **S3-P003** Draft `clarify.md`, resolving 19 scoping ambiguities including the `S2-S003` adoption (Q19).
- [x] **S3-P004** Draft `plan.md`: module ownership, host/effect algorithm, containment-qualification approach, PEP-seam plan, process-spawn admission gate (Route A/B), deterministic qualification matrix, staged implementation-authority bootstrap.
- [x] **S3-P005** Draft `checklists/requirements.md`.
- [x] **S3-P006** Draft `ponytail.md`, rejecting every mechanism not named by the master plan's S3 scope.
- [x] **S3-P007** Draft `source-acquisition.md`, naming Windows Job Objects as the qualification oracle with no API binding admitted.
- [x] **S3-P008** Draft `threat-model.md` (19 threats).
- [x] **S3-P009** Draft `analyze.md` (cross-artifact self-consistency pass).
- [x] **S3-P010** Draft `acceptance.md`, including the `S2-S003` disposition section (§H.1).
- [ ] **S3-P011** Open the planning PR against canonical `main` at `28e42da95e4d6304f24c1d2513ebd40f6f1c483a` (or later trusted successor).
- [ ] **S3-P012** Record the exact-head external-review egress preflight per `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`.
- [ ] **S3-P013** Trigger and complete an independent exact-head review, or record `REVIEW_BLOCKED`.
- [ ] **S3-P014** Reconcile every material finding; requalify/rereview any repair.
- [ ] **S3-P015** Final race check (canonical main, PR base/head, exact diff, threads, required checks).
- [ ] **S3-P016** Ready transition, then reread Ready-triggered trusted-base admission on the same exact head.
- [ ] **S3-P017** Guarded merge with `--match-head-commit` expected-head protection.
- [ ] **S3-P018** Post-merge canonical `main` reread and post-merge `foundation-integrity` verification on the exact merge head.

Planning acceptance (`S3-P011`..`S3-P018`) grants no implementation authority; it only makes this package canonical planning.

## 2. Contract tasks — `S3-AUTH-C` (contracts-only successor)

None of the following may begin before a separately governed `S3-AUTH-C` successor grants exact `crates/contracts` paths.

- [ ] **S3-C001** `ServerDescriptor` contract type + schema round-trip test.
- [ ] **S3-C002** `HostDescriptor` contract type; test that `host_execution_opt_in_state` defaults false and no constructor path sets it implicitly.
- [ ] **S3-C003** `RunnerDescriptor` contract type; test that `current_network_state` is fixed `NONE` and cannot be constructed otherwise.
- [ ] **S3-C004** `ProcessTreeIdentity` contract type; test that equality/matching requires both `os_process_id` and `os_process_start_time`.
- [ ] **S3-C005** `ContainmentCapabilityReport` contract type.
- [ ] **S3-C006** `ContainmentPosture` contract type; test that each strength dimension is settable independently (a `PROCESS_TREE_ONLY` fixture does not imply any other dimension).
- [ ] **S3-C007** `RuntimeCeiling` contract type; test the intersection arithmetic, including the empty-intersection-blocks case.
- [ ] **S3-C008** `EnvironmentExposurePolicy` contract type.
- [ ] **S3-C009** `EffectProposal` contract type; test that `proposed_effect_kind` is a closed enum and an unrecognized value is a construction error, not a pass-through.
- [ ] **S3-C010** `PEPDecision` contract type; test that the default/missing-input path is `UNKNOWN_FAIL_CLOSED`, never `ALLOW`.
- [ ] **S3-C011** `EffectResult` contract type; test that no construction path can produce `outcome = EXECUTED` without a referenced `PEPDecision.decision = ALLOW`.
- [ ] **S3-C012** `EffectDependency` contract type; test the prerequisite/dependent blocking rules.
- [ ] **S3-C013** Negative secret-safety contract test: no field on any S3 contract type accepts an unbounded/raw string typed for environment or process-output content without going through an explicit allowlisted evidence field.

## 3. Host/containment qualification tasks — `S3-AUTH-HOST`

Depends on §2 being canonical. None of the following may begin before a separately governed `S3-AUTH-HOST` successor grants exact paths.

- [ ] **S3-H001** Research the exact Windows Job Object API surface and candidate binding crate (`source-acquisition.md` §3); this is the point at which a concrete crate/version is actually admitted, not assumed from planning.
- [ ] **S3-H002** Implement the explicit host-execution opt-in flow (default off, distinct from S1/S2 actions).
- [ ] **S3-H003** Implement Windows Job-Object-class containment investigation.
- [ ] **S3-H004** Implement `ContainmentCapabilityReport`/`ContainmentPosture` production from that investigation, including explicit `NONE`/`UNKNOWN` on unqualified dimensions.
- [ ] **S3-H005** Establish native Windows `wepld-core` CI execution for this investigation (this is the point at which the `S2-S003` precondition is first satisfiable).
- [ ] **S3-H006** Attempt `S2-S003` closure: execute S2's existing junction/reparse fixtures on the now-available native Windows CI surface. Do not modify S2's fixtures to make them pass; report what they actually show.
- [ ] **S3-H007** Record the `S2-S003` disposition (closed with evidence, or explicitly re-carried) in this package's `acceptance.md` §H.1 before `S3-AUTH-HOST` is considered accepted.

## 4. Effect/PEP seam tasks — `S3-AUTH-OBSERVE`

Depends on §3 being canonical. None of the following may begin before a separately governed `S3-AUTH-OBSERVE` successor grants exact paths.

- [ ] **S3-E001** Implement `ownership_epoch` bump-on-restart and stale-epoch refusal.
- [ ] **S3-E002** Implement the bounded cancellation contract; measure and publish the actual deadline once Job-Object termination behavior is characterized (`plan.md` §4.4).
- [ ] **S3-E003** Implement `OBSERVE_PROCESS_TREE` against a narrow, internally admitted test-fixture process.
- [ ] **S3-E004** Implement `REQUEST_CANCELLATION`, scoped to the entire process tree via the Job-Object termination mechanism.
- [ ] **S3-E005** Implement the narrow, fail-closed, internally-testable self-test PEP evaluator (`plan.md` §5.1); document it explicitly as a test double, not a policy engine.
- [ ] **S3-E006** Implement `EffectDependency` evaluation for composite test fixtures.

## 5. Process-spawn adapter tasks — `S3-AUTH-SPAWN` (deferred, optional)

Explicitly **not** part of the preferred first successors. Requires its own separate source/security review before any of the following begins.

- [ ] **S3-SP001** Define the exact `SPAWN_PROCESS_TREE` argv allowlist.
- [ ] **S3-SP002** Implement resolved-absolute-executable invocation with rejection of project-local spoofed executables.
- [ ] **S3-SP003** Implement deny-by-default environment injection for the spawned process, overriding the stdlib's ambient-inheritance default (`source-acquisition.md` §2).
- [ ] **S3-SP004** Bind the spawned process to its Job Object before it can execute meaningfully (no unowned window).
- [ ] **S3-SP005** Implement bounded stdout/stderr capture with hard byte ceilings.
- [ ] **S3-SP006** Implement bounded wall-clock timeout wired to whole-tree cancellation.
- [ ] **S3-SP007** Adversarial/fuzz tests for the argv/environment boundary.

## 6. Security / adversarial tasks

- [ ] **S3-S001** PID-reuse simulation fixture: an unrelated process reusing a just-exited PID is not matched to the prior `ProcessTreeIdentity`.
- [ ] **S3-S002** Stale-ownership-epoch race fixture: a proposal against a superseded epoch is refused.
- [ ] **S3-S003** Job-Object-unavailable fixture (older Windows/restricted environment) yields `NONE`/`UNKNOWN`, never a default `PROCESS_TREE_ONLY` claim.
- [ ] **S3-S004** PEP missing/stale/malformed policy input yields `UNKNOWN_FAIL_CLOSED`.
- [ ] **S3-S005** `RuntimeCeiling` empty-intersection fixture is refused, not silently narrowed.
- [ ] **S3-S006** Environment-leak fixture: no ambient secret reaches a spawned process outside its allowlist (once `S3-AUTH-SPAWN` exists).
- [ ] **S3-S007** Cancellation-hang fixture: a hung/adversarial process resolves to bounded `UNKNOWN`, never an indefinite wait.
- [ ] **S3-S008** Multi-level process-tree cancellation fixture (child-of-child) proves whole-tree termination, not just top-level.
- [ ] **S3-S009** `EffectDependency` unknown-prerequisite fixture blocks the irreversible dependent effect.
- [ ] **S3-S010** No-raw-secret-in-evidence fixture across every S3 record type (proposal, result, decision, containment report).
- [ ] **S3-S011** No-network fixture: no S3 operation performs or requires network access.

## 7. Platform / qualification tasks

- [ ] **S3-Q001** Windows native `wepld-core` CI execution gate (shared precondition with `S3-H005`/`S2-S003`).
- [ ] **S3-Q002** Linux/macOS gates explicitly record `NONE`/`UNKNOWN` containment evidence rather than omitting the platform from the matrix.
- [ ] **S3-Q003** Cancellation-deadline measurement/benchmark, published with fixture shape (mirrors S2's benchmark-evidence discipline).
- [ ] **S3-Q004** Windows version-compatibility matrix for Job Object nesting/feature support; unqualified versions recorded `UNKNOWN`.

## 8. Acceptance-program tasks — after implementation, mirrors S2's `S2-A001..A009` pattern

- [ ] **S3-A001** Exact-head full deterministic qualification.
- [ ] **S3-A002** Independent correctness/engineering review.
- [ ] **S3-A003** Codex Security when available/applicable; otherwise exact limitation accounting.
- [ ] **S3-A004** Reconcile all findings; no voting away valid defects.
- [ ] **S3-A005** Final race check and Ready-triggered trusted admission.
- [ ] **S3-A006** Guarded S3 acceptance decision (a Founder ruling on any bounded limitations still open at that point, exactly as `S2-A006` ruled on S2's eight `[~]` rows).
- [ ] **S3-A007** Merge only under current canonical/founder authorization with expected-head protection.
- [ ] **S3-A008** Post-merge canonical verification.
- [ ] **S3-A009** Build Learning capture.
- [ ] **S3-A010** Final `S2-S003` disposition confirmed at S3 acceptance: closed with genuine evidence, or explicitly re-carried forward to the next slice — never silently dropped.

## Explicit stop conditions

Stop implementation and return to authority/planning if any task requires:

- process-spawn authority before `S3-AUTH-SPAWN` is separately granted;
- a Windows API binding crate before `S3-AUTH-HOST`'s own admission decision;
- distributed/multi-host runner fencing;
- credential brokering of any kind;
- a harness/worker protocol adapter;
- native desktop bridge capability;
- network access;
- S3-D (deterministic assurance seed);
- S4 semantic graph;
- S5 Spec Kit/AGILLE/Plan Qualification;
- S6 Mission Runtime/UWC/Mirefa/Edara/full Nawat effect-time authority;
- model/provider execution;
- weakening any invariant in `constitution.md`/`spec.md` to make a test pass.
