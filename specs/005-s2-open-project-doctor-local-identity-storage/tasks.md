# S2 Task Ledger

## Canonical state markers — candidate until merged

```text
SLICE = S2
NAME = Open Project + Project Doctor + local identity/storage
PLANNING_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
INITIAL_REVIEWED_HEAD = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
SECOND_REVIEWED_HEAD = 63270002470a32d8ffef34be9c75e0befc30e7a9
PLANNING_STATE = MERGED_TO_CANONICAL_MAIN
S2_IMPLEMENTATION_AUTHORITY = EXACT_DOCTOR_CLI_PROJECTION_TRANCHE_ONLY_AFTER_V49_ACTIVATION
ACTIVE_IMPLEMENTATION_TASK = NONE
NEXT_IMPLEMENTATION_TASK = NOT_AUTHORIZED_UNTIL_A_SUCCESSOR_GRANTS_ITS_EXACT_PATHS
NEXT_AUTHORITY_GATE = S2-ACCEPTANCE
```

This update was made by the session that merged PR 280. It has direct live evidence for
the three tranches recorded below (PR 274, PR 280, and the S2-AUTH-014/015 policy
activations) and none beyond that. `S2-I006`/`S2-I007` are recorded partial rather than
done because no dedicated adversarial fixture for either was found in the merged test
suite; the underlying fields exist and are wired, but that is not the same evidence as a
fixture proving the distinction. `S2-A001..S2-A009` (the acceptance gate) are left
unchecked on purpose: `Builder != Acceptance Authority for acceptance-critical work`
(`AGENTS.md`), and the S2 acceptance decision (`S2-A006`) has not been made.

```text
LAST_MERGED_TRANCHE = S2-AUTH-015 Doctor + CLI projection tranche
LAST_MERGED_TRANCHE_PR = 280
LAST_MERGED_TRANCHE_BASE = 5fbf068fa618beb9d61d8d5281925055944d3736
LAST_MERGED_TRANCHE_HEAD = 9b78232622d10538ef163592da662b7617b2b189
LAST_MERGED_TRANCHE_MERGE = dae6115c4cec88e7c2151b3e4b7e86946a5644de
LAST_MERGED_TRANCHE_REVIEW = SATISFIED, CodeRabbit, exact-head 9b78232, 4/4 findings
  independently re-verified fixed and threads resolved by the reviewer itself
LAST_MERGED_TRANCHE_UNRESOLVED_FINDINGS_AT_MERGE = 0, INDEPENDENTLY CHECKABLE
  (CodeRabbit's own resolution replies, not merely asserted by the merging session)
LAST_MERGED_TRANCHE_UNRESOLVED_THREADS_NOW = 0_INDEPENDENTLY_CHECKABLE
LAST_MERGED_TRANCHE_POST_MERGE_FOUNDATION = SUCCESS, run 33868781922, activation markers
  wepld_policy_successor_v50=S2_V49_DOCTOR_CLI_SELFTEST_PROJECTION_REPAIR_ONLY /
  doctor_cli_authority_v50=DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY /
  next_authority_gate_v49=S2-ACCEPTANCE / every dangerous authority (shell, arbitrary
  process, package install, project-native command, Git mutation, safe.directory
  mutation, remediation exec, network, model/provider, S3+) reads NONE
LAST_MERGED_TRANCHE_ACCEPTANCE_RECORD = NONE_YET; slice acceptance is a separate
  founder-reserved decision (S2-A006), not implied by this merge

PRIOR_TRANCHE = S2 identity and local evidence store
PRIOR_TRANCHE_PR = 240
PRIOR_TRANCHE_BASE = 573670eca575a5972e52b623b01b3143d036d281
PRIOR_TRANCHE_HEAD = bdebfbaa8f146115321e6d204da9e49d367047e2
PRIOR_TRANCHE_MERGE = a6edc3af9e0435ed6283b2bf42ab0aff240b10db
PRIOR_TRANCHE_TREE = c1b7f68992211f28aac8b4ad4dff54db1b18939f
PRIOR_TRANCHE_REVIEW_ROUNDS = 17_BY_PROJECT_DEFINITION_NOT_A_GITHUB_CONCEPT
PRIOR_TRANCHE_UNRESOLVED_FINDINGS_AT_MERGE = 0_ASSERTED_BY_THE_MERGING_SESSION
PRIOR_TRANCHE_UNRESOLVED_THREADS_NOW = 0_INDEPENDENTLY_CHECKABLE
PRIOR_TRANCHE_ACCEPTANCE_RECORD = PR 240 comment 5483115585, EDITED AFTER THE MERGE

INTERMEDIATE_TRANCHE = bounded Git topology adapter (S2-AUTH-014 product side)
INTERMEDIATE_TRANCHE_PR = 274
INTERMEDIATE_TRANCHE_BASE = 75ef1bcd91584b1c3f98b0efc2ba22b4f53038f4
INTERMEDIATE_TRANCHE_HEAD = 7aac2147f507ee2530293c761b4185bb9b5fd41a
INTERMEDIATE_TRANCHE_MERGE = 24791b11196106f0440ca01aa5344a5168e650f8
INTERMEDIATE_TRANCHE_REVIEW = SATISFIED, CodeRabbit, exact-head 7aac214, 0 unresolved
  threads (three findings reconciled across the review, final head 7aac214)
INTERMEDIATE_TRANCHE_POST_MERGE_FOUNDATION = SUCCESS, run 33784207241
```

## Planning gates

- [x] **S2-P001** Re-read canonical governance and V2.3 S2 scope.
- [x] **S2-P002** Create exact eleven-file Spec Kit package under v21 planning authority.
- [x] **S2-P003** Complete constitution.
- [x] **S2-P004** Complete specification.
- [x] **S2-P005** Complete clarification decisions.
- [x] **S2-P006** Complete implementation plan candidate.
- [x] **S2-P007** Complete requirements checklist.
- [x] **S2-P008** Complete cross-artifact analysis.
- [x] **S2-P009** Complete task ledger.
- [x] **S2-P010** Complete Ponytail FULL.
- [x] **S2-P011** Complete Source Acquisition Check for planning/no-import boundary.
- [x] **S2-P012** Complete threat model.
- [x] **S2-P013** Complete acceptance contract.
- [x] **S2-P014A** Superseded/pre-repair Foundation qualification evidence on `4a9b356...`; it does not qualify any later repaired head.
- [x] **S2-P015A** Superseded/pre-repair external-review egress preflight evidence on `4a9b356...`; it does not authorize review of any later repaired head.
- [x] **S2-P016A** Obtain qualified independent CodeRabbit review on `4a9b356...`; review produced nine material findings.
- [x] **S2-P017A** Normalize/reconcile the nine CodeRabbit planning findings in the planning contracts/tasks.
- [x] **S2-P014B** Superseded Foundation/trusted-admission qualification completed on `632700...` before the second tracked repair; stale after the current head changes.
- [x] **S2-P015B** Superseded external-review egress preflight completed for `632700...`; stale after the current head changes.
- [x] **S2-P016B** Qualified independent CodeRabbit rereview completed on `632700...`; it produced five material findings and therefore did not satisfy planning acceptance.
- [x] **S2-P017B** Reconcile the five CodeRabbit findings from `632700...` in the current planning candidate.
- [ ] **S2-P014** Obtain fresh exact-head deterministic Foundation/trusted-admission qualification on the current repaired head.
- [ ] **S2-P015** Record fresh canonical-policy external-review egress preflight for the current repaired exact head.
- [ ] **S2-P016** Obtain at least one qualified independent exact-head rereview of the current repaired head.
- [ ] **S2-P017** Reconcile every valid material finding from that fresh rereview.
- [ ] **S2-P018** Rerun qualification/review after any further tracked repair.
- [ ] **S2-P019** Final race check and move planning PR Ready only with exact-head evidence.
- [ ] **S2-P019A** Reread Ready-triggered trusted-base admission and require genuine PASS on the same exact head.
- [ ] **S2-P020** Guarded merge with current founder/canonical authorization evidence plus expected-head protection.
- [ ] **S2-P021** Prove post-merge canonical planning activation/Foundation on exact `main`.

Two of the markers above name things GitHub does not expose, and they are qualified rather than left to look like platform facts.

A review round is a project concept. GitHub reports reviews, comments and timeline events and has no notion of a round, so that count is narrative and cannot be reproduced from the API.

The merge-instant finding count is weaker than it first appears, and the weakness is disclosed rather than papered over. The acceptance record was created at `19:03:35Z` and the merge completed at `19:03:58Z`, so it was written first; but the comment was then edited at `19:04:03Z`, after the merge, to repair code blocks a shell-quoting error had emptied. GitHub serves no earlier revision of a comment body, so its current text cannot establish what it said at the merge instant. GitHub also exposes no resolution timestamp for a review thread and no historical snapshot of thread state, so the platform cannot answer the question either way.

What is therefore true: the count is an assertion by the session that performed the merge, and it is labelled as one. What is independently checkable is the present state, that PR 240 has four review threads and none unresolved.

Historical checks/reviews on a superseded head are evidence of the review process, not acceptance evidence for the current repaired head. Tracked checkboxes are coordination only; live GitHub exact-head/post-merge evidence is authority for qualification claims.

The `S2-P014` through `S2-P021` rows above are left exactly as they were by the update that recorded the merged implementation tranche. That update had direct live evidence for the tranche it merged and none for those planning steps, and flipping a checkbox without evidence is the defect class this slice spent seventeen review rounds removing. Anyone with that evidence should record it here with the run and merge identities attached.

## Independent-review finding reconciliation

The CodeRabbit review of `4a9b356...` created nine actionable threads. The first repaired candidate incorporated these contract changes:

- [x] **S2-R001** Record exact live PR base SHA + trusted canonical main SHA and require equality before acceptance.
- [x] **S2-R002** Define qualified independent-review evidence and `REVIEW_BLOCKED`; reviewer unavailability is not PASS.
- [x] **S2-R003** Expand planning completion rule with trusted-base admission, egress, race checks, Ready-triggered admission, and pre/post-merge Foundation evidence.
- [x] **S2-R004** Serialize first-open identity creation with a bounded store-wide catalog reservation before per-project locking.
- [x] **S2-R005** Define immutable project generations plus atomic `CURRENT` selection so identity/index/evidence cannot be mixed across generations.
- [x] **S2-R006** Freeze bounded/cancellable `try_lock` polling and stable catalog/project busy errors; prohibit indefinite lock waits and PID lockfile takeover.
- [x] **S2-R007** Replace open-ended descriptor discovery with an exact root allowlist and explicit candidate/per-file/aggregate/depth limits.
- [x] **S2-R008** Bind Source Acquisition registry observations to trusted-base OID + source-check input head + exact registry blob SHA; require live GitHub verification for acceptance.
- [x] **S2-R009** Extend privacy to Doctor TTY/JSON/log/diagnostic output using WePLD-owned templates and allowlisted safe parameters.

The fresh CodeRabbit rereview of `632700...` created five additional material findings. The current candidate incorporates these repairs:

- [x] **S2-R010** Make external-review egress fail closed against the exact canonical `EXTERNAL_REVIEW_EGRESS_POLICY.md`: classification, screening, provider handling, approval, and exact scope are required; unavailable controls become `EGRESS_BLOCKED`.
- [x] **S2-R011** Require current founder/canonical authorization evidence for each GitHub mutation in the acceptance flow, and separately bind merge to the exact authorized head plus `expected_head_sha`.
- [x] **S2-R012** Include required negative secret-safety task `S2-C009` in the first contracts-only authority tranche and its self-tests.
- [x] **S2-R013** Label `4a9b356...` Foundation/egress evidence explicitly superseded/pre-repair rather than implying it qualifies a repaired head.
- [x] **S2-R014** Define the evidence-store authenticity boundary: unkeyed schema/version/digest/manifest/reference checks detect corruption/coherence only and do not defend against writer-level tampering.
- [ ] **S2-R015** Fresh independent rereview confirms the current repaired head resolves both review waves with no remaining material contradiction.

## Next authority transition — not yet authorized

The successor strategy is now staged so the plan in the repository is directly executable without granting broad authority prematurely.

### S2-AUTH-C — preferred first successor: contracts only

- [ ] **S2-AUTH-001** Re-read canonical S2 planning from live `main` after S2-P021.
- [ ] **S2-AUTH-002** Design the minimum append-only contracts-only successor using S1 staged-authority precedent.
- [ ] **S2-AUTH-003** Freeze exact `crates/contracts` S2 contract/export/test path allowlist for S2-C001..S2-C009.
- [ ] **S2-AUTH-004** Keep Core filesystem/process/network/model/S3/S4 effects structurally unavailable in S2-AUTH-C.
- [ ] **S2-AUTH-005** Preserve `SOURCE_ADMISSION=NONE`.
- [ ] **S2-AUTH-006** Preserve `DEPENDENCY_ADMISSION=NONE` unless a separately qualified dependency is genuinely required by the contracts tranche.
- [ ] **S2-AUTH-007** Self-test a positive exact S2-C001..S2-C009 contracts candidate, including the C009 secret-safe negative contract surface, plus negative mixed/extra-path/dependency/effect candidates.
- [ ] **S2-AUTH-008** Exact-head deterministic/review/security accounting.
- [ ] **S2-AUTH-009** Guarded merge + post-merge activation proof before S2 contract implementation.

### Later authority transitions

- [ ] **S2-AUTH-010** After contracts are canonical, authorize bounded locator/identity/evidence Core paths only.
- [ ] **S2-AUTH-011** Freeze per-platform data-root, lossless OS-path, opaque-ID, digest, catalog, generation, and locking machinery before corresponding Core mutation.
- [ ] **S2-AUTH-012** Decide any direct `uuid`/`sha2` Core dependency edge under a focused exact dependency-admission gate; transitive presence is not admission.
- [x] **S2-AUTH-013** Decide external Git route separately: `NONE` or exact bounded Git adapter. Decided `SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER`; evidence below.
- [x] **S2-AUTH-014** If Git adapter is selected, qualify executable/environment/argv/timeout/output/trust/no-hook/no-network boundaries before code. Qualified `READ_ONLY_TOPOLOGY_OBSERVATION_ONLY` via v45; evidence below.
- [x] **S2-AUTH-015** Authorize Doctor + CLI projections only after underlying observations/contracts exist. Authorized `DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY` via v49/v50; evidence below.
- [ ] **S2-AUTH-016** Keep network/model/S3/S4 authority denied throughout S2. Verified NONE on every activation marker through v50 (see evidence blocks below); left unchecked because it is a standing invariant for the whole slice, not a one-time task, and S2 is not yet closed.

No S2 implementation task below becomes eligible until the canonical successor for that task explicitly grants its paths/effects.

### S2-AUTH-013 evidence

```text
DECISION = SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER
PR = 254
BASE = 0bdddf875a8ac8b53404f28d2be2e24dba520599
ACCEPTED_HEAD = 58f313acbb0b9f23ebe0944c0fdb43c3c3cbc803
ACCEPTED_TREE = 0e50014ad9030118318f8c749de759e081ee7072
CHANGED_FILES = 4
PRODUCT_PATHS = 0
SPEC_PATHS = 0
MERGE = 0b8259f3c448adeecacb3cde04efe52c09dbf2d4
MERGE_TREE = 0e50014ad9030118318f8c749de759e081ee7072
EXACT_HEAD_FOUNDATION = SUCCESS, run 33443112504 / 943
TRUSTED_BASE_RUN = 33443112545 / 765, expected successor bootstrap negative oracle
POST_MERGE_FOUNDATION = SUCCESS, run 33486599768 / 944
ACTIVATION_MARKER = git_route_decision_v36=SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER
INDEPENDENT_REVIEW = SATISFIED, CodeRabbit, PR 254 comment 5491029654
CODEX_SECURITY = NOT_RUN_NON_BLOCKING, provider usage-limit refusal, PR 254 comment 5491014720
SECURITY_PASS = NOT_CLAIMED
```

Every identity above is a GitHub or Actions fact rather than a project determination, except
`INDEPENDENT_REVIEW`, which is the project's qualification of the reviewer output cited beside it.

The merge tree equals the accepted tree, so nothing outside the reviewed range entered canonical
`main`.

What the decision grants is narrower than its name suggests. The canonical policy emitted, on the
post-merge run:

```text
GIT_PROCESS_ADMISSION = NONE
GIT_EXECUTION_AUTHORITY = NONE
EXTERNAL_PROCESS_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
```

The two candidate command families stay specification-only:

```text
rev-parse:closed_allowlisted_topology_query
worktree:list:porcelain-z
```

`S2-I005`, `S2-I006` and `S2-I007` therefore remained ineligible until `S2-AUTH-014` granted
their authority (below); they are recorded separately under their own task rows.

### S2-AUTH-014 evidence

```text
DECISION = READ_ONLY_TOPOLOGY_OBSERVATION_ONLY
POLICY_PR = 273
POLICY_BASE = 53d8883418d9c9ab1c2081de8d7c9436aacdeba3
POLICY_HEAD = 14d5d985eb1a66bf0730eb4aa1ac768abe9e8205  (post-repair; superseded pre-repair
  head 3b109077097f4c68e778861617834e1758559ae2 does not qualify)
POLICY_MERGE = f059f11b325630cd32746cf49d24f6395abcc06f
EXACT_HEAD_FOUNDATION = SUCCESS, run 33690549308
TRUSTED_BASE_RUN = 33690547233, expected successor bootstrap negative oracle
POST_MERGE_FOUNDATION = SUCCESS, run 33691476822
ACTIVATION_MARKER = wepld_policy_successor_v45=S2_AUTH_014_EXACT_GIT_TOPOLOGY_PROCESS_TRANCHE /
  git_execution_authority_v45=READ_ONLY_TOPOLOGY_OBSERVATION_ONLY /
  external_process_authority_v45=EXACT_QUALIFIED_GIT_EXECUTABLE_CLOSED_TOPOLOGY_ARGV_ONLY /
  doctor_cli_authority_v45=NONE / next_authority_gate_v45=S2-AUTH-015
INDEPENDENT_REVIEW = SATISFIED, CodeRabbit, PR 273, 0 unresolved threads
CODEX_SECURITY = NOT_RUN_NON_BLOCKING (no reachable surface); security-review accounting
  recorded on PR 273 per docs/canonical/SECURITY_REVIEW_POLICY.md
SECURITY_PASS = NOT_CLAIMED
PRODUCT_TRANCHE = PR 274 (git_topology.rs); see S2-I005..S2-I007 below
```

v46 (PR 275), v47 (PR 276) and v48 (PR 277) are predecessor-selftest-projection repairs
over v45 — they widen nothing, grant no new authority, and are not separately recorded
as authority gates.

### S2-AUTH-015 evidence

```text
DECISION = DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY
POLICY_PR = 278
POLICY_BASE = 24791b11196106f0440ca01aa5344a5168e650f8
POLICY_HEAD = d23a38e6fda4d48f8a53fe360c9aa58e39371ca2
POLICY_MERGE = 705d9b529791a97c27ccfd955b2b4e08e189cac3
EXACT_HEAD_FOUNDATION = SUCCESS, run 33810560705
TRUSTED_BASE_RUN = 33810560707, expected successor bootstrap negative oracle
POST_MERGE_FOUNDATION = SUCCESS, run 33816696689
ACTIVATION_MARKER = wepld_policy_successor_v49=S2_AUTH_015_EXACT_DOCTOR_CLI_PROJECTION_TRANCHE /
  doctor_cli_authority_v49=DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY /
  general_shell_authority_v49=NONE / arbitrary_process_authority_v49=NONE /
  package_install_authority_v49=NONE / git_mutation_authority_v49=NONE /
  safe_directory_mutation_authority_v49=NONE / remediation_execution_authority_v49=NONE /
  next_authority_gate_v49=S2-ACCEPTANCE
INDEPENDENT_REVIEW = SATISFIED, CodeRabbit, PR 278, 0 unresolved threads
CODEX_SECURITY = NOT_RUN_NON_BLOCKING (no reachable surface)
SECURITY_PASS = NOT_CLAIMED
PRODUCT_TRANCHE = PR 280 (doctor.rs / cli.rs / bin/wepld.rs); see S2-D*/S2-CLI*/S2-S* below
```

v50 (PR 279) is a predecessor-selftest-projection repair over v49 — same class as v46-v48,
widens nothing, not separately recorded as an authority gate. Its own activation marker
confirms `next_authority_gate_v49=S2-ACCEPTANCE` unchanged.

`S2-AUTH-010`, `S2-AUTH-011` and `S2-AUTH-012` are left unchecked on purpose. The merged S2
identity/evidence-store tranche and the recorded `getrandom`/`sha2` dependency admission suggest
their substance was performed, but this update carries no assembled run and merge identities for
them. Flipping them on that inference is the defect class this ledger already refuses elsewhere.
Anyone holding that evidence should record it here the way `S2-AUTH-013` is recorded above.

## Contract tasks — first implementation tranche candidate

- [ ] **S2-C001** Define versioned `ProjectLocator` including lossless machine path representation seam.
- [ ] **S2-C002** Define versioned `RepositoryTopology` contract.
- [ ] **S2-C003** Define local project identity, catalog reservation, reassociation, conflict, and busy-result contracts.
- [ ] **S2-C004** Define evidence envelope, project generation manifest/`CURRENT` reference, provenance, freshness, and status contracts.
- [ ] **S2-C005** Define Doctor finding/report/remediation contracts with template IDs, opaque evidence refs, and closed safe parameters.
- [ ] **S2-C006** Define command response/error JSON envelopes including ambiguity, catalog/store busy, capability unavailable, and corruption classes.
- [ ] **S2-C007** Add bounded canonical serialization/deserialization helpers inside admitted contract machinery.
- [ ] **S2-C008** Add contract snapshot/round-trip/unknown-version/unknown-enum/redaction/bounds tests.
- [ ] **S2-C009** Negative contract test proves raw secret-bearing values cannot inhabit fields designated safe/template parameters without explicit sanitization type.

## Project locator / identity tasks

- [ ] **S2-I001** Implement input + lexical absolute path observation.
- [ ] **S2-I002** Implement resolved-path observation with explicit errors.
- [ ] **S2-I003** Implement bounded symlink/reparse metadata observation.
- [ ] **S2-I004** Implement non-Git project root semantics.
- [x] **S2-I005** Implement selected Git topology route only under exact later process/filesystem authority. `git_topology.rs` (PR 274) under S2-AUTH-014; 5 tests in `git_topology_v1.rs` (current checkout, project-local candidate rejection, cancellation, relative-locator rejection, malformed-worktree-output fail-closed).
- [~] **S2-I006** Implement worktree/common-repository distinction. `worktree_root` / `git_common_dir` / `is_bare` / `linked_worktree_state` fields exist and are typed (`git_topology.rs`), but no dedicated linked-worktree/common-dir adversarial fixture was found in the merged test suite — recorded partial rather than done.
- [~] **S2-I007** Implement superproject/submodule/nested-repository diagnostics. `superproject_worktree` is observed and wired into `nested_candidate_ambiguity` (`doctor.rs` via PR 280's `bin/wepld.rs`), but there is no dedicated submodule/nested-repository fixture — recorded partial rather than done.
- [x] **S2-I008** Implement deterministic identity match strength ordering.
- [x] **S2-I009** Implement conservative move/rename reassociation.
- [x] **S2-I010** Implement collision/conflict/ambiguity handling.
- [x] **S2-I011** Implement store-wide catalog reservation with `reserved|initialized` state and fixed catalog-before-project lock order.
- [x] **S2-I012** Implement reservation crash recovery that reuses/revalidates the same project ID rather than allocating a second ID.
- [x] **S2-I013** Add adversarial identity fixtures for copies/clones/worktrees/moves.
- [x] **S2-I014** Add concurrent first-open fixture proving one identity or stable busy/conflict result, never silent duplicate identities.

## Local evidence-store tasks

- [ ] **S2-E001** Freeze per-platform WePLD local data-root contract.
- [ ] **S2-E002** Freeze lossless Unix/Windows machine path representation and safe display projection.
- [x] **S2-E003** Implement safe opaque store/project/generation/record ID path derivation under admitted machinery.
- [x] **S2-E004** Implement bounded record reads/version/digest/reference validation.
- [x] **S2-E005** Implement bounded catalog/project `try_lock` protocol with 2000ms deadline, 25ms polling, cancellation, and stable busy errors.
- [x] **S2-E006** Implement catalog temp-write/replace and reservation-state recovery.
- [x] **S2-E007** Implement immutable project generation construction with manifest.
- [x] **S2-E008** Implement small same-filesystem `CURRENT` temp-write/qualified-sync/atomic-replace commit point.
- [x] **S2-E009** Implement read-once `CURRENT` generation selection; prohibit mixed-generation reads.
- [x] **S2-E010** Implement crash/torn-write/orphan-generation/corrupt-current states.
- [x] **S2-E011** Implement freshness state calculation/invalidation seams.
- [x] **S2-E012** Implement privacy redaction/allowlisted persisted fields.
- [x] **S2-E013** Add concurrent ordinary writer tests.
- [x] **S2-E014** Add failure injection at every catalog reservation, generation-file, manifest, and `CURRENT` commit boundary.
- [~] **S2-E015** Prove process-crash lock release on claimed platforms/filesystem classes; lock-file existence alone never blocks ownership recovery. PARTIAL: the lock-file half is demonstrated, the process-crash half is reasoned from handle-close semantics and not observed, because spawning a process is outside the merged tranche.
- [x] **S2-E016** Add platform durability evidence; do not overclaim unsupported directory-entry/power-loss semantics.
- [x] **S2-E017** Preserve the explicit S2 authenticity limitation: structurally valid unkeyed generations are not authenticated against an actor with writer access to the complete store; any future authenticated trust anchor requires separate planning/authority.

## Project Doctor tasks

- [x] **S2-D001** Establish stable finding-code registry and WePLD-owned text-template registry. `doctor.rs::codes` / `doctor.rs::templates` (PR 280).
- [x] **S2-D002** Identity/reservation/reassociation Doctor rules. `doctor.rs::evaluate` identity branch; `doctor_v1.rs` (`unavailable_identity_is_not_healthy`, `ambiguous_identity_is_blocking_and_carries_only_a_safe_count`).
- [x] **S2-D003** Repository/worktree/trust Doctor rules. `doctor_v1.rs` (`git_trust_refusal_is_blocking_and_never_proposes_editing_safe_directory`, `non_git_project_is_valid_with_repository_facts_absent`).
- [x] **S2-D004** Implement exact root descriptor allowlist detection only. `bin/wepld.rs::PARSED_DESCRIPTORS` / `PRESENCE_MARKERS` (closed lists).
- [x] **S2-D005** Enforce `MAX_ROOT_DESCRIPTOR_CANDIDATES=32`. `doctor.rs::MAX_ROOT_DESCRIPTOR_CANDIDATES`; `doctor_v1.rs::descriptor_budget_bounds_fail_closed_at_each_limit`.
- [x] **S2-D006** Enforce parsed descriptor max 1 MiB, aggregate 4 MiB, structured nesting depth 64 before/while parsing. Same budget test; no structured parse occurs (nesting depth is 0 by construction, FR-022).
- [x] **S2-D007** Keep lock/package-manager markers presence-only in baseline S2 unless a later parser contract is explicitly authorized. `bin/wepld.rs::PRESENCE_MARKERS` never reads file contents.
- [x] **S2-D008** Toolchain descriptor facts remain descriptive; no command execution/eval. `bin_source_starts_no_project_task_and_opens_no_socket` (`cli_v1.rs`).
- [x] **S2-D009** Lockfile/package-manager ambiguity rules. `doctor_v1.rs::multiple_lockfiles_and_ambiguous_package_manager_are_reported_not_resolved`; `cli_v1.rs::doctor_completes_and_flags_package_manager_ambiguity`.
- [x] **S2-D010** Evidence catalog/current-generation corruption rules. `doctor_v1.rs` (`unavailable_store_is_blocking`, `partial_store_is_not_complete`, `unavailable_status_store_is_distinct_from_partial`, `corrupt_store_is_blocking_integrity_defect`).
- [x] **S2-D011** Freshness/staleness rules. `doctor_v1.rs::stale_required_record_is_not_fresh`.
- [~] **S2-D012** Security-sensitive configuration observations report safe classes/counts without raw values. PARTIAL: the `SecuritySensitiveObservation` type, the `D-SEC-CREDENTIAL-BEARING-CONFIG` rule, and its safe-count-only templates exist and are unit-tested (`doctor_v1.rs::security_sensitive_config_reports_only_safe_counts_no_raw_values`), but `bin/wepld.rs::run_doctor` always passes `SecuritySensitiveObservation::default()` — no git-config/remote-URL classification feeds it. Populating it needs a bounded git-config/remote read, which is external-process authority beyond S2-AUTH-014's closed topology enum (`rev-parse:closed_allowlisted_topology_query`, `worktree:list:porcelain-z` only) and therefore needs its own authority successor. No leak risk: the type carries only safe enums/counts. Disclosed in PR 280's description at merge.
- [x] **S2-D013** Stable finding ordering/explanations/remediation hints using template IDs and safe parameters only. `doctor_v1.rs::evaluation_is_deterministic_and_sorted_by_category_then_severity_then_code`, `every_finding_uses_wepld_owned_templates_and_d_prefixed_codes`.
- [x] **S2-D014** Negative test proving Doctor executes no repository task/installer/remediation. `cli_v1.rs::bin_source_starts_no_project_task_and_opens_no_socket`; `doctor_v1.rs::doctor_module_source_contains_no_process_or_network_effect`.
- [x] **S2-D015** Negative TTY/JSON tests for credential URLs, environment tokens, manifest command strings, and ANSI/control injection. `cli_v1.rs::no_secret_or_ansi_pattern_appears_in_any_surface`, `terminal_control_sequences_never_reach_human_or_json_output`, `safe_display_path_redacts_credential_bearing_remote_urls`.

## CLI / command-plane tasks

- [x] **S2-CLI001** Reconcile exact exit-code values with existing CLI conventions. `cli.rs::ExitClass` frozen 0/1/2/3/4/5/6; `cli_v1.rs::exit_class_codes_are_frozen`.
- [x] **S2-CLI002** Freeze stable machine error classes for identity conflict, catalog/store busy, capability unavailable, evidence corruption, and blocking Doctor findings. `bin/wepld.rs::store_failure` maps every `StoreError` variant to one frozen `ExitClass`.
- [x] **S2-CLI003** Implement `open` command contract and human projection. `bin/wepld.rs::run_open`; `cli_v1.rs::open_on_a_plain_directory_succeeds_and_reuses_one_identity`.
- [x] **S2-CLI004** Implement `doctor` command contract and human projection. `bin/wepld.rs::run_doctor`; `cli_v1.rs::doctor_completes_and_flags_package_manager_ambiguity`.
- [x] **S2-CLI005** Implement `status` command contract and human projection. `bin/wepld.rs::run_status`; `cli_v1.rs::status_reports_no_association_before_open_then_the_identity_after`.
- [x] **S2-CLI006** Implement stable `--json` projection from the same redacted semantic model as TTY. `cli.rs::render` dispatches human/json from one `CommandOutcome`; `cli_v1.rs::human_and_json_come_from_one_model_and_are_deterministic`, `json_output_is_byte_deterministic_and_control_free`.
- [x] **S2-CLI007** Implement/verify `--no-input` behavior. `cli.rs::Invocation::no_input`; exercised in `cli_v1.rs::json_output_is_byte_deterministic_and_control_free`.
- [x] **S2-CLI008** Verify unknown commands stay errors with suggestions. `cli_v1.rs::unknown_command_is_an_error_with_a_suggestion_never_a_prompt`, `unknown_command_exits_two_with_a_suggestion_and_never_prompts`.
- [x] **S2-CLI009** Preserve explicit future JSONL/event interface without overbuilding streaming. No streaming/event machinery was added; the JSON projection stays one deterministic object per invocation.
- [ ] **S2-CLI010** Shell-completion surface for new commands only if existing CLI architecture admits it. Not attempted: no existing WePLD CLI shell-completion generator is admitted for this binary to extend.

## Security / adversarial tasks

- [ ] **S2-S001** Path traversal/canonicalization/TOCTOU test suite.
- [ ] **S2-S002** Symlink loop/broken link tests.
- [ ] **S2-S003** Windows junction/reparse/extended-length path tests where runner capability permits.
- [ ] **S2-S004** Case sensitivity/case-only path identity tests.
- [ ] **S2-S005** Git `safe.directory` refusal test; prove no auto-bypass.
- [ ] **S2-S006** Malicious `.git`/gitfile/topology parsing tests.
- [ ] **S2-S007** External Git output/environment/parser/timeout/no-hook/no-network tests if Git adapter admitted.
- [x] **S2-S008** Secret-bearing remote/config/environment/output redaction tests across store, TTY, JSON, logs, diagnostics. `cli_v1.rs::no_secret_or_ansi_pattern_appears_in_any_surface` (fake `ghp_...` token + userinfo-bearing URL fixture, asserted absent from stdout+stderr across `open`/`doctor`/`status`, human and `--json`). Scoped to the descriptor-scan/CLI-output surface this tranche controls; does not cover a git-config/remote-URL source, since none is read (see S2-D012).
- [ ] **S2-S009** Corrupt/oversized/unsupported/mixed-generation evidence record tests.
- [ ] **S2-S010** First-open identity split race test.
- [ ] **S2-S011** Lock contention denial test proves bounded completion.
- [ ] **S2-S012** Descriptor amplification tests for count/per-file/aggregate/depth limits.
- [x] **S2-S013** Repository mutation negative oracle: open/doctor/status leave project tree unchanged. `cli_v1.rs::open_doctor_status_do_not_mutate_the_project_tree` (byte-identical directory snapshot before/after; also proves no `.wepld/` is written into the project).
- [x] **S2-S014** Network negative oracle: S2 command path has no required network effect. `cli_v1.rs::bin_source_starts_no_project_task_and_opens_no_socket` (source-level negative oracle: no `std::net`/`TcpStream`/`UdpSocket`/`reqwest` reference in `bin/wepld.rs`).
- [x] **S2-S015** Writer-level tampering fixture proves an internally self-consistent forged unkeyed store cannot be labeled cryptographically authenticated/tamper-evident; the implementation reports the documented authenticity limitation rather than a false PASS. `doctor_v1.rs::store_authenticity_is_structural_coherence_only_never_a_pass`; `cli_v1.rs::open_reports_the_documented_authenticity_limitation_not_a_false_pass`.

## Platform / performance tasks

- [ ] **S2-Q001** Windows deterministic gate.
- [ ] **S2-Q002** Linux deterministic gate.
- [ ] **S2-Q003** macOS gate when available or explicit coverage limitation.
- [ ] **S2-Q004** Large-repository fixture proves baseline open/Doctor avoids whole-tree traversal.
- [ ] **S2-Q005** Descriptor discovery ceiling evidence for exact 32/1MiB/4MiB/depth-64 contracts.
- [ ] **S2-Q006** Evidence-store bounded-read/size tests.
- [ ] **S2-Q007** Lock deadline/contention performance evidence.
- [ ] **S2-Q008** Git adapter timeout/output ceiling benchmark if admitted.
- [ ] **S2-Q009** Publish p50/p95 or deterministic ceiling evidence with fixture identity.

## Acceptance / learning tasks

- [ ] **S2-A001** Exact-head full deterministic qualification.
- [ ] **S2-A002** Independent correctness/engineering review with reviewer qualification + exact base/head evidence.
- [ ] **S2-A003** Codex Security when available/applicable; otherwise exact limitation accounting.
- [ ] **S2-A004** Reconcile all findings; no voting away valid defects.
- [ ] **S2-A005** Final race check and Ready-triggered trusted admission.
- [ ] **S2-A006** Guarded S2 acceptance decision with exact-head evidence.
- [ ] **S2-A007** Merge only under current canonical/founder authorization with expected-head protection.
- [ ] **S2-A008** Post-merge canonical verification.
- [ ] **S2-A009** Build Learning capture including donor/reviewer positive and negative mechanisms.

## Explicit stop conditions

Stop implementation and return to authority/planning if any task requires:

- an unlisted source path;
- a new dependency not admitted by the active policy;
- source import;
- arbitrary project process execution;
- network access;
- repository mutation beyond exact S2 authority;
- descriptor/workspace traversal beyond the frozen bounded contract;
- unbounded lock/process/parser waiting;
- raw secret-bearing data in trusted output;
- S3 Terminal Fabric;
- S4 semantic graph;
- model/provider execution;
- weakening Git/platform trust controls.