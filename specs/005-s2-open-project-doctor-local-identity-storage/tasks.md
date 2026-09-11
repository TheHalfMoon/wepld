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

```text
S2-P014..S2-P021 = SEPARATE_PLANNING_PACKAGE_ACCEPTANCE_TRACK
```

`S2-P014..S2-P021` are the `acceptance.md` §A planning-package acceptance steps for the current repaired planning head. They belong to §A planning-package acceptance; neither `S2-A006` nor §J `CLOSED_CANONICAL` names `S2-P*` in its own checklist. `S2-AUTH-001` ("re-read canonical S2 planning from live `main` after S2-P021") remains an effective, unchecked authority edge; it depends on `S2-P014..S2-P021` and this ledger does not change that. The six implementation tranches (PR #240, #274, #280, #283, #286, #287) that merged under staged policy successors v25..v52 without `S2-P021` did so ahead of that edge — that is a recorded **process deviation** (same class as the PR #287 merge-before-final-review deviation), not a nullification of the edge; `S2-AUTH-013/014/015` are `[x]` while `S2-AUTH-001..012` remain `[ ]`, and `NEXT_AUTHORITY_GATE = S2-ACCEPTANCE` is an observed state marker, not authority to skip the edge. Whether S2 implementation acceptance (`S2-A006` / §J) may proceed with `S2-AUTH-001` and `S2-P014..S2-P021` still open is a Founder / canonical-governance determination — surfaced at `S2-A006`, not resolved here. These rows are recorded as an explicit separate track: not skipped, and not marked complete without their own §A evidence.

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
- [x] **S2-R015** Fresh independent rereview confirms the current repaired head resolves both review waves with no remaining material contradiction. Round 14 (auto-review, diff `901bb55..5215e3b`, no actionable comments) plus round 6's formal review (fully reconciled) close this; see "S2-A002 / S2-R015" evidence below.

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
- [x] **S2-AUTH-016** Keep network/model/S3/S4 authority denied throughout S2. Verified NONE on every activation marker through v50 (see evidence blocks below); re-verified across the full v21->v65 cascade at the exact final S2 code head as part of the S2-A006 acceptance reconciliation (see "S2-AUTH-001..S2-AUTH-012 / S2-AUTH-016 — narrow evidence-led reconciliation" below) — the standing invariant now closes with S2's own acceptance rather than remaining open past it.

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

- [x] **S2-C001** Define versioned `ProjectLocator` including lossless machine path representation seam. `crates/contracts/src/project.rs` + `crates/contracts/tests/project_v1.rs::project_contract_v1_constants_are_frozen`, `project_locator_preserves_machine_path_layers_and_safe_display` (versioned `ProjectLocator`, lossless `MachinePath` seam, safe display projection); PR #240 (merge `a6edc3af9e0435ed6283b2bf42ab0aff240b10db`).
- [x] **S2-C002** Define versioned `RepositoryTopology` contract. `crates/contracts/tests/project_v1.rs::repository_topology_round_trips_and_future_contract_values_fail_closed`; PR #240.
- [x] **S2-C003** Define local project identity, catalog reservation, reassociation, conflict, and busy-result contracts. `crates/contracts/tests/project_v1.rs::identity_reservation_resolution_and_busy_states_are_versioned_and_bounded`; PR #240.
- [x] **S2-C004** Define evidence envelope, project generation manifest/`CURRENT` reference, provenance, freshness, and status contracts. `crates/contracts/tests/project_v1.rs::evidence_generation_and_current_reference_preserve_authenticity_limitation`; PR #240.
- [x] **S2-C005** Define Doctor finding/report/remediation contracts with template IDs, opaque evidence refs, and closed safe parameters. `crates/contracts/tests/project_v1.rs::doctor_report_uses_only_closed_safe_parameters`; PR #240.
- [x] **S2-C006** Define command response/error JSON envelopes including ambiguity, catalog/store busy, capability unavailable, and corruption classes. `crates/contracts/tests/project_v1.rs::command_envelopes_cover_required_machine_error_classes`; PR #240.
- [x] **S2-C007** Add bounded canonical serialization/deserialization helpers inside admitted contract machinery. `crates/contracts/tests/project_v1.rs::canonical_json_is_deterministic_and_bounded`; PR #240.
- [x] **S2-C008** Add contract snapshot/round-trip/unknown-version/unknown-enum/redaction/bounds tests. `crates/contracts/tests/project_v1.rs` snapshot/round-trip/unknown-version/unknown-enum/redaction/bounds coverage: `repository_topology_round_trips_and_future_contract_values_fail_closed`, `tagged_project_contract_enums_reject_unknown_fields`, `identity_reservation_resolution_and_busy_states_are_versioned_and_bounded`, `canonical_json_is_deterministic_and_bounded`; PR #240.
- [x] **S2-C009** Negative contract test proves raw secret-bearing values cannot inhabit fields designated safe/template parameters without explicit sanitization type. `crates/contracts/tests/project_v1.rs::c009_raw_secret_bearing_text_cannot_enter_safe_parameter_contract` (raw `user:supersecret@...?token=` rejected from `SafeParameter::Path` and `raw_text`; `MachinePath::safe_display` redacts; explicit sanitization type required); PR #240.

## Project locator / identity tasks

- [x] **S2-I001** Implement input + lexical absolute path observation. `crates/core/tests/project_v1.rs::lexical_absolute_path_normalizes_without_filesystem_resolution`, `lexical_absolute_path_rejects_empty_and_relative_base`, `project_locator_preserves_input_lexical_and_resolved_layers`, `windows_drive_relative_locator_is_rejected_without_ambient_drive_state`; PR #240.
- [x] **S2-I002** Implement resolved-path observation with explicit errors. `crates/core/tests/project_v1.rs::project_locator_records_canonicalization_failure_instead_of_fabricating_resolution`; PR #240.
- [x] **S2-I003** Implement bounded symlink/reparse metadata observation. `crates/core/tests/project_v1.rs::metadata_observation_is_bounded_to_path_components_and_does_not_walk_the_tree`, `metadata_observation_rejects_non_absolute_input`, `linux_eloop_maps_to_symlink_loop`, `macos_eloop_maps_to_symlink_loop`, `windows_cant_resolve_filename_maps_to_symlink_loop`; PR #240.
- [x] **S2-I004** Implement non-Git project root semantics. `crates/core/tests/project_v1.rs::non_git_directory_root_uses_revalidated_resolved_path`, `non_git_directory_root_rejects_locator_path_mismatch_before_fallback`; PR #240.
- [x] **S2-I005** Implement selected Git topology route only under exact later process/filesystem authority. `git_topology.rs` (PR 274) under S2-AUTH-014; 5 tests in `git_topology_v1.rs` (current checkout, project-local candidate rejection, cancellation, relative-locator rejection, malformed-worktree-output fail-closed).
- [x] **S2-I006** Implement worktree/common-repository distinction. DONE: `worktree_root` / `git_common_dir` / `is_bare` / `linked_worktree_state` fields exist and are typed (`git_topology.rs`, PR 274 under S2-AUTH-014). The dedicated adversarial fixture landed under the bounded, single-use v52 Git-topology evidence-reopen authority (policy PR #286, merged `9340874c398e19169e8898161d2934c5c9e8f2ba`, activation markers `wepld_policy_successor_v52=S2_GIT_TOPOLOGY_EVIDENCE_REOPEN_ONLY` / `git_topology_evidence_reopen_authority_v52=SINGLE_USE_TEST_ONLY_REOPEN_OF_GIT_TOPOLOGY_V1_RS`; product PR #287, merged `fee75a9bce1596a69cae83b3fa4aca60e8a2b310`), which reopened exactly `crates/core/tests/git_topology_v1.rs` after v45's own product-tranche freeze blocked the originally-proposed fixture PR #285 (`v45 Git-topology product tranche is frozen after first canonical landing`). `git_topology_v1.rs::linked_worktree_observes_distinct_root_and_shared_common_dir` creates a real `git worktree add` linked worktree and proves `worktree_root` (the linked worktree) is distinct from `git_common_dir` (still the main repository's shared `.git`) and from the worktree's own `absolute_git_dir`, each checked by exact canonicalized-path equality against an independent second `git rev-parse --absolute-git-dir` / `--git-common-dir` invocation (not the adapter under test grading its own output). Independent review (chronological, exactly as GitHub records it): (1) CodeRabbit manual review of PR #287 at head `1464f025fc177ad5d8b53dbea7d02c0b257453ea` (2026-09-05T11:44:52Z, COMMENTED) raised one Minor / Functional Correctness finding - the fixtures originally asserted on path-label substrings (`.contains(...)`), which could pass for the wrong reason (a wrong path that happens to contain the label, or any unrelated `absolute_git_dir` distinct from `git_common_dir`). (2) Fix commit `3bbb070b59d9b7e9053a0b80aed345ac0d68be8f` replaced every substring assertion with exact canonicalized-path equality cross-checked against independent `git rev-parse --absolute-git-dir` / `--git-common-dir` / `--show-superproject-working-tree` oracle invocations. (3) PR #287 was merged 2026-09-05T12:08:45Z on head `3bbb070b` - i.e. BEFORE any independent review terminating at that fixed head existed; this merge-before-final-review ordering is a recorded process deviation. (4) The independent re-review of the merged head was obtained afterward: CodeRabbit manual re-trigger on the merged PR (comment https://github.com/TheHalfMoon/wepld/pull/287#issuecomment-5552787325, 2026-09-05T15:22:16Z) - verdict "I found no issues in the final assertion changes", with CodeRabbit independently reconstructing a fresh linked-worktree topology and confirming Git returns distinct absolute paths for `--absolute-git-dir` vs `--git-common-dir`. It is an issue comment rather than a second formal review object because CodeRabbit's incremental engine does not open a new formal review on an already-reviewed PR; GitHub's `pulls/287/reviews` therefore still lists only the head-`1464f025` COMMENTED review. Net: the landed content (`3bbb070b`) now has a clean exact-head independent correctness review; the only residual is the disclosed ordering deviation. CI on the exact merged head `3bbb070b`: `foundation-integrity` and `s1-admission-integrity` both PASS (v52's reopen makes this delta an authorized candidate, not the `EXPECTED_SUCCESSOR_BOOTSTRAP_REJECTION` a policy-only PR draws), plus `desktop-windows`, `secondary-platform` macOS + Ubuntu, and `windows-performance` green; post-merge `foundation-integrity` green against merge commit `fee75a9bce1596a69cae83b3fa4aca60e8a2b310` with activation marker `reopen_available_v52=False` confirming the single-use grant is now permanently consumed. Test evidence: `cargo test -p wepld-core` 197 tests (195 -> 197, +2 new), `cargo fmt --check -p wepld-core` and `cargo clippy -p wepld-core --all-targets -- -D warnings` both clean.
- [x] **S2-I007** Implement superproject/submodule/nested-repository diagnostics. DONE: `superproject_worktree` is observed and wired into `nested_candidate_ambiguity` (`doctor.rs` via PR 280's `bin/wepld.rs`). The dedicated adversarial fixture landed in the same PR #287 under the same single-use v52 reopen as S2-I006 above - same policy/product merge commits, same independent review chain (head-`1464f025` COMMENTED review + head-`3bbb070b` clean re-review comment https://github.com/TheHalfMoon/wepld/pull/287#issuecomment-5552787325), same CI evidence, and the same disclosed merge-before-final-review ordering deviation. `git_topology_v1.rs::submodule_worktree_observes_its_superproject` creates a real `git submodule add` submodule and proves `superproject_worktree` resolves to the exact superproject root from inside the submodule, checked by exact canonicalized-path equality against an independent `git rev-parse --show-superproject-working-tree` invocation rather than a path-substring match. Scope note: this fixture covers the submodule -> superproject observation; the broader nested-repository / ambiguous-candidate distinctions remain exercised only by the pre-existing `nested_candidate_ambiguity` wiring and its `doctor_v1.rs` coverage, not by a new dedicated topology fixture.
- [x] **S2-I008** Implement deterministic identity match strength ordering.
- [x] **S2-I009** Implement conservative move/rename reassociation.
- [x] **S2-I010** Implement collision/conflict/ambiguity handling.
- [x] **S2-I011** Implement store-wide catalog reservation with `reserved|initialized` state and fixed catalog-before-project lock order.
- [x] **S2-I012** Implement reservation crash recovery that reuses/revalidates the same project ID rather than allocating a second ID.
- [x] **S2-I013** Add adversarial identity fixtures for copies/clones/worktrees/moves.
- [x] **S2-I014** Add concurrent first-open fixture proving one identity or stable busy/conflict result, never silent duplicate identities.

## Local evidence-store tasks

- [x] **S2-E001** Freeze per-platform WePLD local data-root contract. `crates/core/src/project.rs::platform_data_root` implements one closed per-platform contract: Linux prefers an absolute `XDG_STATE_HOME` (`DataRootSource::XdgStateHome`); a relative `XDG_STATE_HOME` is ignored in favor of `~/.local/state` (`DataRootSource::HomeLocalStateFallback`, `ignored_relative_xdg_state_home=true`); a missing fallback base fails closed with `DataRootBaseUnavailable`; macOS uses `Application Support/WePLD` (`DataRootSource::MacosApplicationSupport`); Windows uses `LocalAppData/WePLD` (`DataRootSource::WindowsLocalAppData`). A relative `XDG_STATE_HOME` is the one candidate that is silently ignored rather than rejected, because a fallback base still exists; once a base is actually selected (the fallback, or the sole candidate on macOS/Windows), that selected base must be absolute or the observation fails closed with `DataRootBaseNotAbsolute` before any path is derived (`data_root_from_base`). `crates/core/tests/project_v1.rs::linux_data_root_prefers_absolute_xdg_state_home`, `::linux_data_root_ignores_relative_xdg_and_uses_absolute_home_fallback`, `::linux_data_root_fails_closed_when_fallback_home_is_unavailable` (`#[cfg(target_os = "linux")]`, exercise the real per-platform function body, executed natively on ubuntu-latest `s1-contracts`); `::macos_data_root_uses_explicit_application_support_base` (`#[cfg(target_os = "macos")]`, executed natively on macos-latest); `::windows_data_root_uses_explicit_local_app_data_base` (`#[cfg(windows)]`, compiled but not executed natively — `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` per `acceptance.md` §H.1, the same limitation already recorded for S2-Q001/S2-E015); implemented in PR #240. No repository-local `.wepld` directory is created (`plan.md` §4.1); the `<wepld-data>/projects/...` conceptual layout in `plan.md` §4.1 is the frozen target this derivation feeds, and is unaffected by this entry.
- [x] **S2-E002** Freeze lossless Unix/Windows machine path representation and safe display projection. Representation: `crates/contracts/src/project.rs::MachinePath` is a closed three-variant contract (`Utf8(String)`, `UnixBytes(Vec<u8>)`, `WindowsWtf16(Vec<u16>)`); this entry's evidence covers only the two raw-path variants that `crates/core/src/project.rs::machine_path_from_path` actually produces (`UnixBytes` via `OsStr::as_bytes` on unix, `WindowsWtf16` via `OsStr::encode_wide` on Windows, with no lossy UTF-8 round trip); each variant is bounded by `MAX_MACHINE_PATH_BYTES`/`MAX_MACHINE_PATH_WIDE_UNITS` (32,768) and refuses oversize input as `ContractValueError::MachinePathTooLong`. `Utf8` is a separate contract-level constructor (`MachinePath::utf8`) with no `machine_path_from_path` call site and no dedicated test in the cited evidence; it is out of scope for this entry's losslessness/safe-display claim. Losslessness proof: `crates/core/tests/project_v1.rs::unix_machine_path_preserves_non_utf8_bytes_losslessly` (a real invalid-UTF-8 byte `0xff` round-trips unchanged; `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest), `::windows_machine_path_preserves_wtf16_units_losslessly` (an unpaired surrogate `0xd800` round-trips unchanged; `#[cfg(windows)]`, compiled but not executed natively — same `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` limitation), and `::machine_path_preserves_exact_case_and_never_lowercases` (mixed case is never generically folded, threat model T-003). Safe-display projection: `MachinePath::safe_display` (`crates/contracts/src/project.rs`) is proven, on the `UnixBytes` and `WindowsWtf16` variants and with no platform `#[cfg]` gate at all, by `crates/contracts/tests/project_v1.rs::project_locator_preserves_machine_path_layers_and_safe_display` (the `Utf8` variant's `safe_display` arm is not exercised by this test) — a `UnixBytes` NUL byte projects to the literal escape `a\x00b`, and a `WindowsWtf16` unpaired surrogate `0xd800` projects to the literal escape `C:\ud800`, so the raw unsafe byte/unit never reaches the projected string; this test executes on every `s1-contracts` platform (ubuntu-latest + macos-latest, `cargo test --locked --package wepld-contracts --all-targets`) because `MachinePath` construction and `safe_display` are pure data logic with no OS-specific `#[cfg]`. Implemented in PR #240. `S2-S004`'s remaining open half — case-only path *identity*/collision behavior on a case-insensitive filesystem — is a distinct claim from representation losslessness and display safety, and is not closed by this entry.
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
- [x] **S2-E015** Prove process-crash lock release on claimed platforms/filesystem classes; lock-file existence alone never blocks ownership recovery. `crates/core/tests/identity_store_v1.rs::process_crash_releases_the_os_owned_catalog_lock` — the parent re-executes the test binary (`std::env::current_exe()`, one test-name arg + `--exact` + one env var, within v55 `TEST_CHILD_PROCESS_AUTHORITY`); the child acquires the store-wide catalog lock, writes a readiness marker, and `std::process::abort()`s while still holding it (no `Drop`, no orderly unlock); the parent waits for the child (no orphan), asserts it did not exit successfully, asserts `catalog/catalog.lock` is still on disk (presence is not ownership), and re-acquires the same lock in `< LOCK_ACQUIRE_DEADLINE_MS` (prompt OS advisory-lock release on handle close, not a full-deadline wait). Runtime-proven by `cargo test --locked -p wepld-core --all-targets` on ubuntu-latest + macos-latest (`s1-contracts` `secondary-platform`); PR #301. `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` per `acceptance.md` §H.1 — the `wepld-core` suite does not execute natively on Windows.
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
- [x] **S2-D012** Security-sensitive configuration observations report safe classes/counts without raw values. DONE: authorized under policy v51 (PR 282, merged as `1e4ed3ee072d90573476616203b338acce40296e`), which granted the bounded closed `ConfigQuery` vocabulary (`--local --no-includes --null --get-regexp` reads only) as a successor to S2-AUTH-014's topology-only authority. Implemented and merged in PR 283 (`git_topology.rs::observe_security_sensitive_config[_with_cancel]`, `ConfigQuery`, `url_value_has_http_credential`; `doctor.rs` availability-gated `D-SEC-CREDENTIAL-BEARING-CONFIG`/`D-SEC-OBSERVATION-UNAVAILABLE` rules; `bin/wepld.rs::run_doctor` now populates `SecuritySensitiveObservation` from a real observation instead of `::default()`). Test evidence: `security_sensitive_config_v1.rs` (11 tests: clean config, credential-bearing remote/pushurl/proxy/helper/extraHeader/insteadOf/sshCommand, non-credential SSH/file/local forms, `--no-includes` scope, no mutation, cancellation), `doctor_v1.rs` (`security_sensitive_config_reports_only_safe_counts_no_raw_values`, `unavailable_security_observation_is_distinct_from_a_clean_one`, `unavailable_availability_with_nonzero_count_never_emits_credential_finding`), `cli_v1.rs`. Independent review: CodeRabbit (manual trigger, PR 283) found two correctness defects on head `86805665` (URL-classifier authority boundary misclassifying `@` in a query/fragment and empty userinfo as credential-bearing; the credential finding emittable on an `Unavailable`-availability observation) — both fixed and regression-tested on head `fe9873a9230626a313200f7946b7b105de4a9f19`, re-reviewed by CodeRabbit against the exact fixed head with 0 further findings. CI green pre-merge (`foundation-integrity`, `s1-admission-integrity`, `s1-contracts`, `s1-performance`, all platforms) and post-merge on `main` (`foundation-integrity`, `s1-contracts`, `s1-performance` against merge commit `c7b43b5b4c772b67cc6b12169675627717da4983`, parents `[1e4ed3ee072d90573476616203b338acce40296e, fe9873a9230626a313200f7946b7b105de4a9f19]`; `s1-admission-integrity` is `pull_request_target`-triggered and pre-merge-only, so it does not run on a push to `main`). `OBSERVATION_SCOPE` note: `--no-includes` means the observation is honestly bounded to the qualified repository-local no-includes scope, not repository-owned `include`/`includeIf` directives — a clean result means no security-sensitive entry in that qualified scope, not a claim about the full effective configuration. No leak risk: only safe enums/counts cross into `DoctorFinding`/CLI output; raw values are transient locals dropped inside the observer and never enter an error variant, `Debug` impl, or output surface.
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
- [x] **S2-CLI010** Shell-completion surface for new commands only if existing CLI architecture admits it. `SHELL_COMPLETION = PERMITTED_LIMITATION`: no WePLD CLI shell-completion generator is admitted for this binary to extend. The task is conditional by its own wording ("only if existing CLI architecture admits it"); no acceptance item requires a completion surface. Recorded as a canonical permitted limitation, not a defect.

## Security / adversarial tasks

- [~] **S2-S001** Path traversal/canonicalization/TOCTOU test suite. PARTIAL: threat model `T-002` (TOCTOU replacement) is proven for the identity reservation/recovery flow by `crates/core/tests/project_v1.rs::symlink_retargeted_between_reservation_and_recovery_is_a_toctou_mismatch` — a real on-disk symlink is retargeted to a different real directory between an opener's reservation and a later recovery of that same reservation (same input path, different real target); `ProjectMatchFacts::facts_digest` binds identity to the resolved path precisely so this race is detected, and `recover_reservation` reports `Mismatch` rather than silently resuming under the attacker's new location, while a sanity assertion confirms recovery against the original, unretargeted facts still resumes normally. `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest (`s1-contracts` `secondary-platform`); landed via the v59 single-use reopen of `crates/core/tests/project_v1.rs` (policy PR #306, product PR #307). This complements, and does not duplicate, `identity_store_v1.rs::reservation_for_different_facts_is_not_adopted`, which proves the same `Mismatch` decision against two independently synthetic facts values with no filesystem involved. LEXICAL-ESCAPE / INVALID-BYTE ANGLE PROVEN at the project-locator layer: `crates/core/tests/project_v1.rs::project_locator_clamps_parent_escape_and_types_invalid_paths_without_fabrication` (landed via the v63 single-use reopen of `crates/core/tests/project_v1.rs`, policy PR #320, product PR #321) asserts three things about `observe_project_locator` / `lexical_absolute_path` against adversarial inputs, distinct from the already-covered `safe_path_segment` store-ID layer (S2-S009/S2-E003): (1) a `..` run far deeper than the lexical base normalizes without erroring, no `Component::ParentDir` survives, and the result is exactly `/etc/wepld-s2-s001-absent-target` (root-anchored, independent of checkout depth — never a path above root); (2) `observe_project_locator` on that same `..`-bearing input preserves the raw traversal spelling verbatim in `input_path` (not silently normalized), records the collapsed path in `lexical_absolute_path`, and returns `resolved_path = Observation::Unavailable { NotFound }` — no fabricated `Available` resolution for the non-existent escaped target; (3) a path carrying an interior NUL byte returns a bounded, typed `resolved_path = Observation::Unavailable { InvalidPath }` — never a panic, never a fabricated resolve. `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest. NOT YET COVERED: no fixture exercises a Windows reserved/device-name path (`CON`, `NUL`, `COM1`, trailing dot/space, ADS `:` streams) under real Windows semantics — on the Unix CI matrix these are ordinary path segments, so this angle is not exercisable on the current S2 execution surface and inherits the `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` bounded limitation (`acceptance.md` §H.1); it is surfaced at the `S2-A006` decision, not discharged by S2.
- [x] **S2-S002** Symlink loop/broken link tests. `crates/core/tests/project_v1.rs::real_symlink_cycle_resolves_to_symlink_loop_without_hanging` (a real on-disk `a -> b -> a` symlink cycle resolves to an explicit `ObservationErrorClass::SymlinkLoop` with bounded completion under 5s, no fabricated resolved path) and `::broken_symlink_target_is_reported_not_fabricated` (a dangling symlink resolves to `ObservationErrorClass::NotFound` — the missing target is reported, never guessed or fabricated — while the link entry itself is still observed as `PathEntryKind::Symlink`); both `#[cfg(unix)]`, executed on ubuntu-latest + macos-latest `secondary-platform`; PR #295. Windows reparse/junction symlink behavior is the separate `S2-S003` obligation.
- [~] **S2-S003** Windows junction/reparse/extended-length path tests where runner capability permits. PARTIAL: extended-length verbatim-prefix path normalization (`\\?\` and `\\?\UNC\` forms) is proven by `crates/core/tests/identity_store_v1.rs::windows_root_forms_normalise_without_loss` (injected inputs, executed on Linux/macOS). Real Windows junction/reparse behavior is NOT proven — no native Windows `wepld-core` runtime (`acceptance.md` §H.1). It remains an open, **unowned** obligation: no S3 planning artifact or task currently accepts it (`acceptance.md` §H.1). S2 acceptance does not discharge it; the owning later slice (expected S3) MUST record it at that slice's planning time and cannot close without satisfying it or explicitly re-recording it as still open.
- [x] **S2-S004** Case sensitivity/case-only path identity tests. CASE PRESERVATION PROVEN: `crates/core/tests/project_v1.rs::machine_path_preserves_exact_case_and_never_lowercases` — a mixed-case path's `MachinePath::UnixBytes` bytes round-trip unchanged (never generically lowercased, threat model T-003; the sibling `MachinePath::WindowsWtf16` assertion is `#[cfg(windows)]`, compiled but not executed on the S2 CI matrix), and a real mixed-case directory's `input_path` + `lexical_absolute_path` locator layers preserve the exact spelling (the filesystem-derived `resolved_path` layer is not asserted here); the executed portion runs on ubuntu-latest + macos-latest; PR #295. CASE-ONLY IDENTITY PROVEN: `crates/core/tests/project_v1.rs::case_only_paths_collapse_to_one_identity_iff_the_filesystem_is_case_insensitive` (landed via the v64 single-use reopen of `project_v1.rs`, policy PR #323, product PR #324) drives a mixed-case directory spelling and its all-lowercase counterpart through `observe_project_locator` and selects its assertion arm by a runtime `std::fs::canonicalize` probe rather than `target_os`, so each CI leg exercises the arm matching its real filesystem. On the case-insensitive leg (macos-latest, APFS): the two spellings' `resolved_path` values are equal, `ProjectMatchFacts::facts_digest()` is equal for the two spellings, and a reservation `build_reservation`-ed under the mixed-case spelling recovers as `ReservationRecovery::ResumeSameProject` with the same `project_id` under the lowercase spelling — one identity, no spurious second project. On the case-sensitive leg (ubuntu-latest, ext4): only the exact-case directory exists, so the lowercase spelling's `resolved_path` is `Observation::Unavailable { NotFound }` and differs from the mixed-case spelling's — the miss is reported, never fabricated onto the directory that does exist. The `input_path` layer preserves the exact lowercase spelling on both legs. `#[cfg(unix)]`; both legs green on `s1-contracts` `secondary-platform`. PR #324 carried its own independent exact-head review (CodeRabbit, no actionable comments, coverage bound to the merged head `f90b1481`) and a guarded merge to canonical `1adfb70`; this row records that already-canonical, already-reviewed, runtime-green evidence, and this reconciliation is itself independently reviewed before merge. BOUNDED LIMITATION: native Windows `wepld-core` runtime is not exercised (`S2_WINDOWS_CORE_RUNTIME = NOT_COVERED`, `acceptance.md` §H.1); Windows case-fold identity behavior inherits that limitation and is surfaced at the `S2-A006` decision, not discharged by S2.
- [~] **S2-S005** Git `safe.directory` refusal test; prove no auto-bypass. NO-AUTO-BYPASS PROVEN: `crates/core/tests/git_topology_v1.rs::observing_topology_never_writes_safe_directory` asserts `global_safe_directory_entries()` is byte-identical before and after topology observation (observation never adds or widens `safe.directory`), and `acceptance.md` §C bare-repository handling is proven by `::bare_repository_is_observed_as_explicitly_bare` (checked against an independent `git rev-parse --is-bare-repository` oracle); both on ubuntu-latest + macos-latest, PR #292. The `RefusedByGit` stderr-to-classification mapping is proven by `crates/core/src/git_topology.rs::failure_classifier_maps_only_safe_closed_classes` (synthetic "detected dubious ownership ... add safe.directory" stderr at exit 128 maps to `GitTopologyError::UntrustedRepositoryRefusedByGit`). BOUNDED LIMITATION: the real end-to-end ownership-mismatch refusal is `NOT_EXERCISABLE_ON_HOSTED_CI` — GitHub-hosted runners set `/etc/gitconfig` `safe.directory = *` and the adapter scrubs `GIT_CONFIG_NOSYSTEM`, so no path is ever dubious; that end-to-end oracle is carried to a slice with containerized / self-hosted CI, and S2 acceptance does not discharge it.
- [x] **S2-S006** Malicious `.git`/gitfile/topology parsing tests. Four angles proven: (1) the hook-execution angle of a hostile `.git` directory — see `topology_observation_never_triggers_a_repository_hook` cited under S2-S007 below (v60, PR #310); (2) malformed/adversarial `worktree list --porcelain -z` machine output — `crates/core/tests/git_topology_v1.rs::malformed_worktree_machine_output_fails_closed` (PR #240-era, pre-existing); (3) the malicious `.git` *gitfile* redirect — `crates/core/tests/git_topology_v1.rs::a_malicious_git_gitfile_pointer_yields_a_bounded_typed_error` (landed via the v61 single-use reopen, policy PR #312, product PR #313): a hand-crafted `.git` *file* whose `gitdir:` pointer is bogus, malformed, empty, or names a real non-Git directory yields a bounded, typed `GitTopologyError` from the closed failure-classification set (`NotGitRepository` / `GitProcessFailed` / `UntrustedRepositoryRefusedByGit`), never an `Ok` topology, never an uncaught panic, and the adapter never acts on the pointer in its own logic (it delegates resolution to the qualified system Git); `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest; (4) a generally malformed/adversarial `.git` *directory* structure — `crates/core/tests/git_topology_v1.rs::a_malformed_git_directory_yields_a_bounded_typed_error` (landed via the v65 single-use reopen, policy PR #326, product PR #327): a `.git` that is a real directory (not a gitfile) but structurally broken across four cases — empty, a garbage `HEAD`, `objects`/`refs` present with `HEAD` missing, and a syntactically invalid `config` — each yields a bounded, typed `GitTopologyError` from the same closed failure-classification set, never an `Ok` topology and never an uncaught panic; the fixture does not pin which specific variant fires for each case, only that the result is a member of the closed set; isolated under the OS temp directory (not `CARGO_TARGET_TMPDIR`) so Git's discovery cannot ascend past the malformed directory into the real checkout repository — a real failure caught and fixed via CI runtime evidence during this PR (both `secondary-platform` legs failed identically before the fix); `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest. BOUNDED LIMITATION: native Windows `wepld-core` runtime is not exercised (`S2_WINDOWS_CORE_RUNTIME = NOT_COVERED`, `acceptance.md` §H.1); surfaced at the `S2-A006` decision, not discharged by S2.
- [~] **S2-S007** External Git output/environment/parser/timeout/no-hook/no-network tests if Git adapter admitted. PARTIAL, landed via the v60 single-use reopen (policy PR #309, product PR #310): the no-hook half is proven by `crates/core/tests/git_topology_v1.rs::topology_observation_never_triggers_a_repository_hook` — a hostile repository plants an executable marker script for each of a selected set of twelve hook names spanning the checkout/commit/push/rewrite/reference-update families (`pre-commit`, `post-commit`, `post-checkout`, `post-merge`, `pre-push`, `pre-rebase`, `post-rewrite`, `reference-transaction`, `pre-auto-gc`, `post-index-change`, `post-applypatch`, `fsmonitor-watchman`); this is a curated list, not an exhaustive enumeration of Git's hook set (e.g. `prepare-commit-msg`, `push-to-checkout`, `proc-receive`, `sendemail-validate` are not planted). With `core.hooksPath` pinned repo-locally so an inherited override cannot make the result vacuous (a CodeRabbit finding, fixed before merge), none of the twelve planted hooks ever fires during `observe_git_topology`'s real `rev-parse`/`worktree list --porcelain -z` calls. `#[cfg(unix)]`, executed natively on ubuntu-latest + macos-latest. The output, environment, and parser halves are proven at the unit level inside `crates/core/src/git_topology.rs`'s `#[cfg(test)]` module: `bounded_reader_stops_at_limit_and_signals_overflow` (the `spawn_bounded_reader` used for both Git stdout and stderr truncates at exactly its byte limit and raises the overflow flag; `run_git` converts that flag to `GitTopologyError::GitOutputTooLarge { stream, max_bytes }` and force-terminates the child); `environment_scrub_removes_git_and_loader_override_routes` (`sanitized_git_environment_from` strips `GIT_DIR`, `GIT_CONFIG_COUNT`, `GIT_TRACE2_EVENT`, `LD_PRELOAD`, and forces `GIT_TERMINAL_PROMPT=0` / `LC_ALL=C`); `worktree_porcelain_parser_requires_absolute_paths_and_valid_head`, `worktree_porcelain_parser_rejects_a_path_repeated_across_records`, and the integration-level `malformed_worktree_machine_output_fails_closed`. No-network is structurally bounded rather than fixture-proven: the adapter's argv is a closed enum containing only `rev-parse` and `worktree list --porcelain -z` (no `fetch`/`pull`/`remote`/`ls-remote`/`clone`), `--no-lazy-fetch` is always passed, and the environment scrub above strips every `GIT_`-prefixed variable (including `GIT_PROXY_COMMAND`). Generic `HTTP(S)_PROXY` / `ALL_PROXY` / `NO_PROXY` variables are *not* stripped by the scrub, but they are inert for this adapter because neither authorized subcommand performs a network transfer for a proxy to act on.

BOUNDED LIMITATIONS — S2 acceptance does not discharge these, matching the S2-S003 / S2-S005 pattern:

1. `REAL_HARD_TIMEOUT_END_TO_END = NOT_EXERCISED`. `GIT_TOPOLOGY_TIMEOUT_MS` is a fixed compile-time constant with no test seam, and a qualified system Git running only the closed topology argv cannot be made to hang for ten seconds without changing product source (which a test-only reopen forbids). The kill-and-reap machinery the timeout path shares is exercised by the cancellation fixture `cancellation_terminates_the_spawned_git_and_returns_a_stable_error`; the elapsed-time *trigger* specifically is carried to a slice that can add a bounded timeout seam or a self-hosted runner fixture. This is the same "explicit obligation" already recorded in `git_topology_v1.rs`'s module doc.
2. `REAL_OVERSIZED_OUTPUT_END_TO_END = NOT_EXERCISED`. The overflow *mechanism* is unit-proven above, but no integration fixture drives a real Git process to emit more than `GIT_STDOUT_MAX_BYTES` (1 MiB) of topology output, because `rev-parse` and `worktree list --porcelain -z` on a plausible fixture cannot produce that volume (it would take thousands of real `git worktree add` operations). Carried to the same later slice.
- [x] **S2-S008** Secret-bearing remote/config/environment/output redaction tests across store, TTY, JSON, logs, diagnostics. `cli_v1.rs::no_secret_or_ansi_pattern_appears_in_any_surface` (fake `ghp_...` token + userinfo-bearing URL fixture, asserted absent from stdout+stderr across `open`/`doctor`/`status`, human and `--json`), covering the descriptor-scan/CLI-output surface. As of S2-D012 (PR 283) this coverage now also includes a real git-config/remote-URL source: `security_sensitive_config_v1.rs::credential_bearing_remote_url_is_counted_and_never_echoed` and siblings prove a genuine `.git/config` credential-bearing entry is classified into a safe count and never echoed, and `doctor_v1.rs::security_sensitive_config_reports_only_safe_counts_no_raw_values` proves the resulting Doctor finding carries only `SafeParameter::Count` values.
- [x] **S2-S009** Corrupt/oversized/unsupported/mixed-generation evidence record tests. `crates/core/tests/identity_store_v1.rs::torn_record_is_detected_by_digest_mismatch`, `an_oversized_persisted_record_is_classified_as_corrupt`, `an_oversized_persisted_manifest_is_classified_as_corrupt`, `an_unsupported_producer_contract_version_is_refused_at_publish_and_read`, `an_unsupported_persisted_schema_version_is_reported_as_corruption`, `interrupted_generation_never_becomes_current`, `readers_never_observe_bytes_rewritten_in_a_selected_generation` (corrupt / oversized / unsupported / mixed-generation distinguished); PR #240.
- [x] **S2-S010** First-open identity split race test. `crates/core/tests/identity_store_v1.rs::concurrent_first_open_yields_one_identity_or_a_stable_busy`; PR #240.
- [x] **S2-S011** Lock contention denial test proves bounded completion. `crates/core/tests/identity_store_v1.rs::contended_lock_returns_a_stable_busy_result_within_the_deadline`, `cancellation_stops_lock_acquisition_promptly`, `releasing_a_lock_allows_immediate_reacquisition` (bounded completion, stable busy result, never an indefinite wait); PR #240.
- [x] **S2-S012** Descriptor amplification tests for count/per-file/aggregate/depth limits. `crates/core/tests/doctor_v1.rs::descriptor_budget_bounds_fail_closed_at_each_limit` against `doctor.rs::MAX_ROOT_DESCRIPTOR_CANDIDATES` (=32) and the 1 MiB / 4 MiB / depth-64 constants frozen in `plan.md` §8 (limit and limit+1 fail-closed at each boundary); PR #280.
- [x] **S2-S013** Repository mutation negative oracle: open/doctor/status leave project tree unchanged. `cli_v1.rs::open_doctor_status_do_not_mutate_the_project_tree` (byte-identical directory snapshot before/after; also proves no `.wepld/` is written into the project).
- [x] **S2-S014** Network negative oracle: S2 command path has no required network effect. `cli_v1.rs::bin_source_starts_no_project_task_and_opens_no_socket` (source-level negative oracle: no `std::net`/`TcpStream`/`UdpSocket`/`reqwest` reference in `bin/wepld.rs`).
- [x] **S2-S015** Writer-level tampering fixture proves an internally self-consistent forged unkeyed store cannot be labeled cryptographically authenticated/tamper-evident; the implementation reports the documented authenticity limitation rather than a false PASS. `doctor_v1.rs::store_authenticity_is_structural_coherence_only_never_a_pass`; `cli_v1.rs::open_reports_the_documented_authenticity_limitation_not_a_false_pass`.

## Platform / performance tasks

- [~] **S2-Q001** Windows deterministic gate. LIMITATION: `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` per `acceptance.md` §H.1 (PR #289, merge `5d60fd32aaa272d89d7bbc42607909b402f4c825`). `wepld-core` builds on `windows-latest` (`desktop-windows` job) but the S2 `wepld-core` suite executes only on ubuntu/macOS (`secondary-platform`). Compile coverage != Windows-shaped injected semantic coverage != native Windows runtime coverage; no native Windows `wepld-core` runtime claim is made.
- [x] **S2-Q002** Linux deterministic gate. CI job `secondary-platform (ubuntu-latest)` runs `cargo test --locked -p wepld-core --all-targets`; PASS on canonical `main` `s1-contracts` run `33965216227` / job `101304020914` (merge `fee75a9bce1596a69cae83b3fa4aca60e8a2b310`); standing across every core-touching tranche #240..#287. Re-binds on the final S2 head at S2-A001.
- [x] **S2-Q003** macOS gate when available or explicit coverage limitation. CI job `secondary-platform (macos-latest)` runs `cargo test --locked -p wepld-core --all-targets`; PASS on canonical `main` `s1-contracts` run `33965216227` / job `101304020763` (merge `fee75a9bce1596a69cae83b3fa4aca60e8a2b310`). Re-binds on the final S2 head at S2-A001.
- [~] **S2-Q004** Large-repository fixture proves baseline open/Doctor perform no non-allowlisted content reads and no descriptor classification from below the project root. `crates/core/tests/cli_v1.rs::baseline_open_and_doctor_do_not_traverse_a_large_project_tree` (landed via the v62 single-use reopen of `cli_v1.rs`, policy PR #316, product PR #317): a genuinely large project tree — 600 top-level files, a 40-level nested subtree — is driven through `wepld open` and `wepld doctor`, with two independent observable signals distinguishing the bounded root-only allowlist scan (`bin/wepld.rs` iterates `PARSED_DESCRIPTORS`/`PRESENCE_MARKERS` and `symlink_metadata`s each name under the project root once) from a content-reading or deep-classifying walk: (1) two 8 MiB non-allowlisted blobs, one at the root and one buried deep, would trip the Doctor's 4 MiB aggregate-descriptor budget and surface `D-WS-DESCRIPTOR-BUDGET-REJECTED` if their contents were read; (2) a pair of conflicting package-manager lockfiles (`package-lock.json` + `yarn.lock`) buried 40 levels deep, plus a single clean `Cargo.toml` at the root, would surface `D-PM-AMBIGUOUS` / `D-LOCK-MULTIPLE-MARKERS` if the scan classified descriptors from anywhere below the root. The test asserts the run is both budget-clean and ambiguity-free, writes no `.wepld/` into the project, and completes within a fixed `< 30s` wall-clock bound for this single fixture. Cross-platform source (not `#[cfg(unix)]`); the `wepld-core` suite executes natively on ubuntu-latest + macos-latest only (`secondary-platform`), Windows compiles but does not run it (`S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` per `acceptance.md` §H.1). LIMITATION: a purely `stat`-based recursive enumeration that reads no bytes and classifies no descriptor below the root would not be distinguished by this fixture (no direct traversal-syscall assertion); the `< 30s` bound is a single-fixture wall-clock ceiling, not a tree-size scaling benchmark — both remain open, re-recorded at S2-A001. A first CodeRabbit finding — that signal (1) alone proved no byte-read but only weakly proved no enumeration — was fixed by adding signal (2) before merge; a second CodeRabbit finding narrowed the traversal, timing, and platform claims recorded here.
- [x] **S2-Q005** Descriptor discovery ceiling evidence for exact 32/1MiB/4MiB/depth-64 contracts. Same oracle as S2-S012 — `crates/core/tests/doctor_v1.rs::descriptor_budget_bounds_fail_closed_at_each_limit` proves the exact 32 / 1 MiB / 4 MiB / depth-64 contracts (one oracle satisfies S2-S012 and S2-Q005); PR #280.
- [x] **S2-Q006** Evidence-store bounded-read/size tests. `crates/core/tests/identity_store_v1.rs::a_persisted_artifact_of_exactly_the_limit_is_accepted_and_one_byte_more_is_not`, `the_evidence_reference_cap_holds_on_both_the_constructor_and_the_disk_path`, `a_manifest_beyond_the_digest_bound_reports_the_bound_not_the_count`, `oversized_record_is_refused_before_it_is_written` (per-record and aggregate byte bounds); PR #240.
- [x] **S2-Q007** Lock deadline/contention performance evidence. `crates/core/tests/identity_store_v1.rs::contended_lock_returns_a_stable_busy_result_within_the_deadline` asserts `elapsed >= LOCK_ACQUIRE_DEADLINE_MS` and `elapsed < LOCK_ACQUIRE_DEADLINE_MS * 4` — the contended acquisition waits out the full S2-E005 deadline, then returns a stable `StoreError::Busy { IdentityCatalog }`, and never exceeds 4× the deadline (bounded, never an unbounded wait). `cancellation_stops_lock_acquisition_promptly` proves prompt cancellation. These read elapsed wall-clock time via `Instant::now()` with a generous 4× tolerance; they do not assert the 25ms poll interval, a deterministic clock, or sub-deadline completion. The 25ms poll and the deadline value are S2-E005 contract constants asserted by the code, not measured here (`STATED_BOUND != MEASURED_BOUND`); PR #240.
- [~] **S2-Q008** Git adapter timeout / output-ceiling evidence. `BENCHMARK_HARNESS = NOT_ADMITTED` (`DEPENDENCY_ADMISSION=NONE`; no `criterion`/`divan`/`iai` in `Cargo.lock`, no `crates/core/benches`), so the "benchmark if admitted" clause does not apply; each ceiling is a fixed compile-time constant, not a measured distribution, and both halves below are partially proven — the truncation/overflow mechanism and the forced-termination path are unit-tested, but neither is exercised through `run_git` at the real constants. OUTPUT CEILING — partially proven: `crates/core/src/git_topology.rs::bounded_reader_stops_at_limit_and_signals_overflow` unit-tests the *mechanism* — `spawn_bounded_reader` stops at exactly its byte limit and raises the overflow flag — but at a synthetic 32-byte limit, not through `run_git` and not at `GIT_STDOUT_MAX_BYTES` (1 MiB) / `GIT_STDERR_MAX_BYTES` (256 KiB). The production wiring — `run_git` converting that flag, via `kill_and_reap` + `ForcedTermination::OutputOverflow`, into a typed `GitTopologyError::GitOutputTooLarge { stream, max_bytes }` carrying the exact per-stream constant — is by source inspection only; no fixture drives `run_git` over either real ceiling (`REAL_OVERSIZED_OUTPUT_END_TO_END = NOT_EXERCISED`, S2-S007). The protection is that per-stream capture ceiling plus the `ForcedTermination::OutputOverflow` teardown, not any inherent bound on the command's output volume — the closed argv fixes the command *forms* only, and `worktree list --porcelain -z` emits metadata proportional to the worktree count, which the argv does not limit. TIMEOUT — partially proven: `GIT_TOPOLOGY_TIMEOUT_MS = 10_000` is a fixed compile-time constant enforced in the same forced-termination poll loop whose sibling `ForcedTermination::Cancelled` arm is exercised end-to-end by `crates/core/tests/git_topology_v1.rs::cancellation_terminates_the_spawned_git_and_returns_a_stable_error` (real system Git spawned, `kill_and_reap`d, stable typed `GitCancelled` returned); the `Timeout` arm shares that exact `kill_and_reap` + join-reader machinery and returns a stable typed `GitTimeout`. LIMITATION: no fixture drives a real >=10 s Git hang — no fault-injection / fake-Git seam is admitted and a multi-second real wait is not an acceptable deterministic CI test; the real hard-timeout firing (as distinct from the shared forced-termination path proven via cancellation) and a real over-ceiling Git stream (on either the 1 MiB stdout or the 256 KiB stderr limit) are carried forward to a slice that admits such a seam, re-recorded at S2-A001. Executed portions run on ubuntu-latest + macos-latest (`secondary-platform`); `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` (`acceptance.md` §H.1).
- [~] **S2-Q009** Performance ceiling evidence with fixture identity. Route: deterministic ceiling evidence (`acceptance.md` §I "deterministic ceiling" branch); measured p50/p95 publication is not produced because no benchmark harness is admitted (see S2-Q008), so `STATED_BOUND != MEASURED_BOUND` (same class as S2-Q007). CEILINGS and their oracles (fail-closed test oracle except where marked partial): descriptor discovery 32 / 1 MiB per file / 4 MiB aggregate / depth 64 — `crates/core/tests/doctor_v1.rs::descriptor_budget_bounds_fail_closed_at_each_limit` (S2-S012 / S2-Q005); Git stdout 1 MiB (`GIT_STDOUT_MAX_BYTES`) and stderr 256 KiB (`GIT_STDERR_MAX_BYTES`) — PARTIAL: `git_topology.rs::bounded_reader_stops_at_limit_and_signals_overflow` unit-tests the truncation/overflow mechanism at a synthetic 32-byte limit; the `run_git` -> `GitOutputTooLarge` wiring at the real constants is source-inspected, not exercised (S2-Q008); Git observation hard timeout 10 s — PARTIAL: the `GIT_TOPOLOGY_TIMEOUT_MS` constant plus the shared forced-termination path (proven only via its `Cancelled` sibling arm, not a real timeout trigger); the 10 s trigger itself is unexercised and carried forward per the S2-Q008 limitation; lock acquisition deadline — `identity_store_v1.rs::contended_lock_returns_a_stable_busy_result_within_the_deadline` asserts `>= deadline` and `< 4x deadline` (S2-Q007). FIXTURE IDENTITY: the selected performance fixture is `crates/core/tests/cli_v1.rs::baseline_open_and_doctor_do_not_traverse_a_large_project_tree`'s tree — content / topology identified here as 600 top-level files, one 40-level nested subtree, two 8 MiB non-allowlisted blobs (one at the root, one buried at depth 40), a buried conflicting `package-lock.json` + `yarn.lock` pair at depth 40, and a single clean root `Cargo.toml`; the run is asserted budget-clean, ambiguity-free, `.wepld/`-free, and within a fixed `< 30s` wall-clock bound for that one fixture (S2-Q004). LIMITATION: the Git output and timeout ceilings above are not exercised at their real constants (mechanism unit-tests + source-inspected wiring only); "published latency evidence is reproducible" (`acceptance.md` §I) is bounded here to re-running the enumerated fail-closed oracle tests; no timing distribution is published, and the `< 30s` figure is a single-fixture ceiling, not a scaling benchmark. Re-recorded at S2-A001.

## Acceptance / learning tasks

- [x] **S2-A001** Exact-head full deterministic qualification. Evidence below.
- [x] **S2-A002** Independent correctness/engineering review with reviewer qualification + exact base/head evidence. Reviewer: CodeRabbit; 14 rounds against successive exact heads, base `71a87fe`, final clean round 14 at head `5215e3b`. Evidence below.
- [x] **S2-A003** Codex Security when available/applicable; otherwise exact limitation accounting. Evidence below.
- [x] **S2-A004** Reconcile all findings; no voting away valid defects. All 15 findings across 14 rounds fixed and independently re-verified; round 14 confirms zero remaining. Evidence below.
- [x] **S2-A005** Final race check and Ready-triggered trusted admission. Performed immediately before this commit; evidence below.
- [x] **S2-A006** Guarded S2 acceptance decision with exact-head evidence. Founder ruling recorded below.
- [ ] **S2-A007** Merge only under current canonical/founder authorization with expected-head protection.
- [ ] **S2-A008** Post-merge canonical verification.
- [ ] **S2-A009** Build Learning capture including donor/reviewer positive and negative mechanisms. Separate follow-up: `docs/learning/BUILD_LEARNING_LEDGER.md` is governed by the frozen `PRE->FINAL` content-addressed transition regime (last opened by v38..v44) and needs its own reopening policy successor.

### S2-A001 evidence — exact-head full deterministic qualification

Two-tier exact-head chain; `git diff --stat 7af08de 71a87fe` touches only this ledger file (one line), so no code drifted between the tiers.

Last code-touching S2 merge, `7af08defe67218ea740056c8b0f12816340d6f14` (PR #327, S2-S006 malformed-`.git`-directory fixture):

```text
PR_HEAD_PRE_MERGE = ad3c6252adcdbe712664236b32dcd4c28b2bcf8e
  foundation-integrity   run 34557232235 / #1197 / pull_request / PASS
  s1-contracts           run 34557232286 / #301  / pull_request / PASS
  s1-performance         run 34557232336 / #103  / pull_request / PASS
  s1-admission-integrity run 34557230220 / #971  / pull_request_target / PASS
POST_MERGE_PUSH = 7af08defe67218ea740056c8b0f12816340d6f14
  foundation-integrity   run 34560177143 / #1198 / push / PASS
  s1-contracts           run 34560177057 / #302  / push / PASS
  s1-performance         run 34560177048 / #104  / push / PASS
```

Current canonical `main` head `71a87fe9a4e834fc9b80745a35c42df6dac58a70` (PR #328, docs-only ledger reconciliation, single-file diff):

```text
foundation-integrity run 34567333001 / #1200 / push / PASS
```

`s1-contracts`/`s1-performance` are path-filtered to `crates/core/**`/`Cargo.*` and correctly did not trigger on the docs-only merge — no code changed between `7af08de` and `71a87fe`. `s1-admission-integrity` is `pull_request_target`-only and does not run on a push to `main`; the code-touching head's PR-time run above already covers it. This re-binds and supersedes the "re-binds on the final S2 head at S2-A001" notes carried on S2-Q002/S2-Q003/S2-Q004/S2-Q008/S2-Q009.

**What `S2-A001`'s checked status actually certifies, precisely stated:** the exact-head deterministic qualification of the S2 *code* state — the two-tier chain above (`7af08de` code-touching merge, `71a87fe` current canonical `main`) — which is fixed and already fully PASS at both tiers, and is not reopened or reduced by this docs-only ledger PR's own in-flight editing. It does **not** certify that this candidate PR's *own current head* has finished its own CI run at the moment this checkbox is read — that is a distinct, narrower fact (round 11, comment on head `d58deb4`, correctly observed that this PR's own applicable checks were still `IN_PROGRESS` for that exact head at review time). Conflating the two is the recurring defect class rounds 6, 9, 10, and 11 have each caught a variant of: a fast-iterating docs PR's own head changes every reconciliation commit, so any claim tying `S2-A001` to *this PR's* literal current-head CI status is stale within roughly a minute of being written.

This candidate PR (#329) is itself a docs-only ledger change (`crates/core` untouched throughout), so it draws exactly the same applicable-gate shape as PR #328 above (`foundation-integrity` + `pull_request_target`-scoped `s1-admission-integrity`; `s1-contracts`/`s1-performance` correctly do not trigger). Every one of this PR's own rounds has reached green on both applicable checks before its next trigger (exact run identity per round recorded in the "S2-A002 / S2-R015 / S2-A004" round-history section below) — but that per-round green status is evidence for *this PR's own mergeability* (`S2-A005` final race check, `S2-A007` guarded merge, `S2-A008` post-merge verification), not a component of what `S2-A001` itself certifies. `S2-A001` stays correctly `[x]` throughout this PR's iteration on that basis; the *actual merge head's* own CI is independently re-verified one final time as part of `S2-A005`, immediately before the guarded merge in `S2-A007` — that is the binding check for "the head that actually gets merged is green," not this paragraph.

### S2-A003 evidence — Codex Security when available/applicable; otherwise exact limitation accounting

This acceptance-record candidate is itself documentation-only (`specs/005-.../tasks.md`), with no executable/runtime/trust-boundary effect; under `docs/canonical/SECURITY_REVIEW_POLICY.md` ("Documentation-only changes with no executable/security-boundary effect may be `NOT_APPLICABLE`") its own `SECURITY_REVIEW = NOT_APPLICABLE`.

Rolling up the whole S2 slice: every recorded Codex Security attempt in this ledger is `NOT_RUN_NON_BLOCKING`, and a grep of this file for `CODEX_SECURITY` finds exactly three recorded instances, all `NOT_RUN_NON_BLOCKING` / `SECURITY_PASS = NOT_CLAIMED`, with zero occurrences of a Codex Security `PASS` anywhere in the ledger:

```text
S2-AUTH-013 (PR 254): NOT_RUN_NON_BLOCKING, provider usage-limit refusal, comment 5491014720
S2-AUTH-014 (PR 273): NOT_RUN_NON_BLOCKING, no reachable surface
S2-AUTH-015 (PR 278): NOT_RUN_NON_BLOCKING, no reachable surface
S2_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S2_SECURITY_PASS = NO
```

This is an explicit, consistently disclosed non-blocking coverage limitation across the whole slice, never rewritten as `PASS` (`SECURITY_REVIEW_POLICY.md`: "`NOT_RUN_NON_BLOCKING` is never rewritten as `PASS`"), matching the S1 precedent exactly (`S1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING`, `S1-014_SECURITY_PASS = NO`, carried unconverted through `S1-016` acceptance). The gate this closes is "accounting complete", not "security passed" — identical to how S1-014 closed with the same non-PASS status.

### S2-AUTH-001..S2-AUTH-012 / S2-AUTH-016 — narrow evidence-led reconciliation

Founder ruling on `S2-A006` requires classifying each open `S2-AUTH-*` row as exactly one of `PROVEN_CANONICAL_EVIDENCE_AVAILABLE`, `PROCESS_DEVIATION_HISTORICAL`, `NOT_APPLICABLE_TO_CURRENT_ACCEPTANCE`, or `STILL_REQUIRED_BLOCKER` before `CLOSED_CANONICAL`, and to stop and satisfy any row discovered to be a genuine controlling prerequisite for §J rather than stale ledger debt. None of §J's `CLOSED_CANONICAL` checklist (`acceptance.md` §J) or `S2-A006` names any `S2-AUTH-*` row, so none of the five groups below is a controlling §J prerequisite; `S2-AUTH-001..S2-AUTH-012` are disclosed process history, while `S2-AUTH-016` is proven canonical evidence.

- **S2-AUTH-001** ("re-read canonical S2 planning from live `main` after `S2-P021`") = `PROCESS_DEVIATION_HISTORICAL`. Its literal precondition (`S2-P014..S2-P021` complete) is still open; `S2-P014..S2-P021` remain `SEPARATE_PLANNING_PACKAGE_ACCEPTANCE_TRACK` (`acceptance.md` §A), not closed by this reconciliation. Implementation tranches merged under staged policy successors v25..v65 ahead of this edge (already recorded, `tasks.md` line 117). This session's own live re-verification of `main`/`tasks.md` before acting substantively performs the re-read the row names, just not in the sequential position ("after S2-P021") its literal text specifies, since S2-P021 has not occurred. Left `[ ]`; reclassified from unstarted to explicit disclosed deviation, not a blocker.
- **S2-AUTH-002..S2-AUTH-009** (the originally-sketched `S2-AUTH-C` contracts-only-first successor design/freeze/self-test/merge sequence) = `PROCESS_DEVIATION_HISTORICAL`. The actual route taken was different and already canonical: `v24` (`wepld_s2_core_observation_bootstrap_v24_integrity.py`) authorized the Core observation/locator tranche and `v25` (`wepld_s2_identity_store_bootstrap_v25_integrity.py`) froze it and authorized the identity/evidence-store tranche, both landing together as PR #240 (`BASE=573670eca575a5972e52b623b01b3143d036d281`, `ACCEPTED_HEAD=bdebfbaa8f146115321e6d204da9e49d367047e2`, `SCOPE=EXACT_FOUR_GOVERNED_PRODUCT_PATHS`, `INDEPENDENT_REVIEW=SATISFIED`, 0 unresolved findings/threads at acceptance — `docs/canonical/CURRENT_STATE.md` "S2 — identity and evidence-store tranche merged"). This achieves a materially equivalent authorization boundary (bounded, structurally effect-free contract/locator/identity/evidence paths only, `SOURCE_ADMISSION=NONE`) through a different successor shape than the `S2-AUTH-C` sketch, not its literal sequence (e.g. a standalone contracts-only-first tranche). Not flipped `[x]`: no exact run/merge identity maps each row's specific text to the v24/v25 route.
- **S2-AUTH-010 / S2-AUTH-011** (bounded locator/identity/evidence Core authorization; per-platform data-root/path/ID/digest/catalog/generation/locking freeze) = `PROCESS_DEVIATION_HISTORICAL`, same v24/v25 -> PR #240 route and reasoning as above. `tasks.md` already recorded (lines 273-277) these are left unchecked on purpose because no assembled run/merge identity ties this exact row text to that tranche, and flipping on inference is the defect class this ledger refuses; that reasoning stands, this reconciliation only adds the explicit classification the Founder ruling requires.
- **S2-AUTH-012** (direct `uuid`/`sha2` Core dependency edge under a focused dependency-admission gate) = `PROCESS_DEVIATION_HISTORICAL`. `getrandom`/`sha2` dependency admission is observed alongside the merged identity/evidence-store tranche, but no assembled run/merge identity exists for a standalone focused `S2-AUTH-012` gate distinct from PR #240's own dependency accounting, so it is not flipped `[x]` on that inference either.
- **S2-AUTH-016** ("keep network/model/S3/S4 authority denied throughout S2") = `PROVEN_CANONICAL_EVIDENCE_AVAILABLE`. The predecessor selftest cascade printed on the exact-head `foundation-integrity` run for the last code-touching S2 merge (`7af08de`, run `34560177143` / #1198), independently re-counted from the raw log: `network_authority_vNN=NONE` and `s3_plus_authority_vNN=NONE` each appear at every printed version from `v22` (their earliest occurrence) through the exact final `v65`, with no exception in any printed occurrence (34 and 25 distinct printed versions respectively; the cascade does not reprint every historical version's markers verbatim at every later version, so these counts are the printed evidence, not a claim of a fully continuous v22-v65 print). `general_shell_authority_vNN=NONE`, `arbitrary_process_authority_vNN=NONE`, `package_install_authority_vNN=NONE`, `git_mutation_authority_vNN=NONE`, `safe_directory_mutation_authority_vNN=NONE`, and `remediation_execution_authority_vNN=NONE` each first appear at `v49` (the S2-AUTH-015 Doctor/CLI grant that introduced these specific authority concepts) and read `NONE` at every printed version through the exact final `v65`, with no exception. `git_execution_authority_vNN` reads `NONE` at every printed version `v22`-`v44` and `READ_ONLY_TOPOLOGY_OBSERVATION_ONLY` (S2-AUTH-014's own bounded grant, not a widening) at every printed version `v45`-`v65`; `external_process_authority_vNN` reads `NONE` at every printed version through `v37` and `EXACT_QUALIFIED_GIT_EXECUTABLE_CLOSED_TOPOLOGY_ARGV_ONLY` (the same grant) at every printed version `v45`-`v65`; neither ever regresses to a wider value at any printed point. The same run log, independently re-verified from the raw log, emits `effective_model_provider_execution_vN=NONE` for `v2` through `v20` and `model_provider_execution_vNN=NONE` for `v21` through `v25` and `v49` through the current `v65`; it prints no direct per-version marker for `v26` through `v48`. For that range, source inspection of every frozen `..._vNN_integrity.py` file at the exact head, `v26` through `v48` individually confirmed (one integrity file per version number, no duplicates), shows: `v26` and `v36` through `v45` each locally (re)assign `MODEL_PROVIDER_EXECUTION` to a `NONE`-equivalent constant (e.g. `wepld_s2_identity_store_governance_v26_integrity.py:138` `= None`; `wepld_s2_git_route_governance_v36_integrity.py:69` through `wepld_s2_git_topology_authority_v45_integrity.py` each `= "NONE"`); `v46` through `v48` each locally reassign it as `= q.MODEL_PROVIDER_EXECUTION`, an explicit inherit-unchanged-by-reference from the immediately preceding version; `v27` through `v35` contain no occurrence of the name at all and inherit it purely through the tower's append-only predecessor-import architecture (each `vNN` imports its frozen `vNN-1` module object and inherits every authority value by reference unless it explicitly monkey-patches that seam). No point anywhere in the tower, at any version, (re)assigns `MODEL_PROVIDER_EXECUTION` to a value other than `NONE`/`"NONE"`/inherited-unchanged. The v65 self-test (`wepld_s2_s006_gitdir_reopen_v65_selftest.py`) separately asserts, at the current head: (a) an `inherited_unchanged` check that `MODEL_PROVIDER_EXECUTION` (among other authority names) equals its immediate predecessor `v64`'s value exactly (`p.MODEL_PROVIDER_EXECUTION == p.q.MODEL_PROVIDER_EXECUTION`, failing the selftest otherwise), and (b) a direct `MODEL_PROVIDER_EXECUTION == "NONE"` check alongside `NETWORK_AUTHORITY`/`S3_PLUS_AUTHORITY`/the six v49-introduced Doctor/CLI authority names. Verified at the exact final S2 code head across direct run-log evidence, frozen-source inspection, and the v65 selftest's own equality/value assertions; flipped `[x]`.

### S2-A006 evidence — guarded S2 acceptance decision with exact-head evidence

Founder decision. Per a CodeRabbit finding on the formal review of `901bb55` (this PR carried no durable GitHub-hosted source, Founder identity, or stated decision scope for the ruling — it existed only in the out-of-band governance conversation that authorized this reconciliation), the ruling is now recorded verbatim as a durable, versioned, GitHub-hosted, independently-checkable record, posted as a comment under the Founder's own authenticated account (a GitHub issue/PR comment is editable by its author, so "durable and independently checkable" is the accurate claim here, not "immutable"):

```text
DECISION_SOURCE = https://github.com/TheHalfMoon/wepld/pull/329#issuecomment-5638475618
DECISION_AUTHOR = TheHalfMoon (repository owner / Founder GitHub account — same account as every other PR/commit author and the PR #2 standing-authorization comment in this repository)
DECISION_POSTED_AT = 2026-09-11T17:45:52Z
DECISION_SCOPE = S2-A006 only — grants S2 acceptance-program authority (S2-A001..S2-A009) to proceed carrying the 8 documented bounded [~] rows forward as explicit unresolved obligations; does not grant S3 implementation authority
S2_A006_DECISION = ACCEPT_WITH_EXPLICIT_BOUNDED_LIMITATIONS
CANONICAL_MAIN_AT_DECISION = 71a87fe9a4e834fc9b80745a35c42df6dac58a70
S2_ACCEPTANCE = ACCEPTED_WITH_BOUNDED_LIMITATIONS
```

S2 may proceed through `S2-A001..S2-A009` toward `CLOSED_CANONICAL` while carrying the following eight `[~]` rows forward as explicit unresolved obligations: `ACCEPTED_LIMITATION != PROVEN_REQUIREMENT`, `CARRIED_FORWARD != DISCHARGED`, `CLOSED_CANONICAL_S2 != ALL_FUTURE_PLATFORM_EVIDENCE_PROVEN`, `ABSENCE_OF_EVIDENCE != PASS`. None of the eight is converted to `[x]` by this decision; each row's own text above already states what is proven, what is not, why proof is not currently producible, the exact bounded limitation, what future capability closes it, and that S2 acceptance does not discharge it:

1. **S2-S001** — Windows reserved/device-name path angle: `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED`; closes with native Windows `wepld-core` runtime (`acceptance.md` §H.1).
2. **S2-S003** — Windows junction/reparse: `S2_S003_DISPOSITION = OPEN_CROSS_SLICE_OBLIGATION`, `EXPECTED_NEXT_OWNER = S3_PLANNING`, `DISCHARGED_BY_S2 = NO`. Unowned until S3 planning explicitly adopts it; no speculative S3 implementation is created now to manufacture ownership.
3. **S2-S005** — real end-to-end `safe.directory` refusal: `REAL_SAFE_DIRECTORY_REFUSAL = NOT_EXERCISABLE_ON_CURRENT_GITHUB_HOSTED_CI` (hosted runners set `safe.directory=*` globally); closes with containerized/self-hosted CI. Product Git semantics are not changed to manufacture the refusal.
4. **S2-S007** — Git timeout/output-ceiling real firing: `REAL_HARD_TIMEOUT_END_TO_END = NOT_EXERCISED`, `REAL_OVERSIZED_OUTPUT_END_TO_END = NOT_EXERCISED`; unit-tested mechanism + source-inspected wiring is not end-to-end trigger evidence; closes with an admitted fault-injection/fake-Git seam.
5. **S2-Q001** — Windows deterministic gate: `WINDOWS_COMPILE_COVERAGE != WINDOWS_NATIVE_CORE_RUNTIME_COVERAGE`; closes with native Windows runtime in CI.
6. **S2-Q004** — traversal-avoidance at scale: proven on one materialized fixture, not a scaling benchmark; closes with a tree-size scaling measurement.
7. **S2-Q008** — Git ceiling evidence: `BENCHMARK_HARNESS = NOT_ADMITTED`; deterministic-ceiling evidence only, no measured distribution; closes with an admitted benchmark harness and the fault-injection seam from (4).
8. **S2-Q009** — performance-ceiling evidence: same `BENCHMARK_HARNESS = NOT_ADMITTED` bound as (7), fixture-identified, not a published p50/p95; same closing condition.

This decision grants S2 acceptance-program authority only; it does not grant S3 implementation authority. `S2-P014..S2-P021` and the `S2-AUTH-001..012` reconciliation above are preserved exactly as recorded, not silently marked complete by this decision.

### S2-A002 / S2-R015 / S2-A004 evidence — independent review, rereview, and finding reconciliation

Reviewer: CodeRabbit (`coderabbitai[bot]`), manually triggered per the egress preflight required by `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` (preflight comments on this PR: `5638035187`, `5638065992`, `5638090993`, `5638146723`, `5638215693`). Chat-style incremental review (not a formal GitHub review object — same class as PR #287's and PR #303's merged-head re-reviews), explicitly requested to assess whether the current S2 planning + implementation state contains any remaining material contradiction against the two original planning review waves (`S2-R001..R009`, `S2-R010..R014`) and whether the `S2-A001`/`S2-A003`/`S2-A006`/`S2-AUTH-001..012/016` claims are accurately supported by their cited evidence.

Thirteen completed rounds against successive exact heads on this PR (twelve chat-style incremental replies — rounds 1-5 and 7-13 — plus one formal `PullRequestReview` object as round 6, discovered on the same head as round 5), each round finding real issues fixed before the next trigger except rounds 5 and 12 (which found none) — no material finding was voted away or left unaddressed. A fourteenth round, against this section's own fix of round 13's finding, is pending on this PR's current head:

```text
ROUND 1 (head 09fa482, comment 5638048545): 1 finding — S2-AUTH-016 claimed no
  model/provider authority marker exists in the exact-head log; the marker
  model_provider_execution_vNN=NONE does exist. Also: "no additional material
  contradiction with S2-R001..R014" found. FIXED on 2a8734a.
ROUND 2 (head 2a8734a, comment 5638074935): 1 finding — the single marker name
  claim was imprecise: two distinct names exist across the cascade
  (effective_model_provider_execution_vN for v2-v20,
  model_provider_execution_vNN for v21+). FIXED on c4cab92.
ROUND 3 (head c4cab92, comment 5638104602): 1 finding — the model_provider_
  execution_vNN marker is not printed for every version v21-v65; v26-v48 have
  no direct log marker (v21-v25 and v49-v65 only). FIXED on 5c812f1 with
  exhaustive frozen-source inspection of v26-v48.
ROUND 4 (head 5c812f1, comment 5638160107): 1 finding — the evidence text said
  "flipped [x]" but the S2-AUTH-016 task-row checkbox (line 166) was still
  [ ], asserting two different states for the same task. FIXED on 1f41029.
  (A further self-audit before round 5, not a CodeRabbit finding, caught and
  fixed the identical "every vNN" overclaim pattern for the other 8 authority
  markers cited in the same paragraph, on 901bb55.)
ROUND 5 (head 901bb55, comment 5638242353, chat-style incremental reply): "I
  found no additional material evidence-ledger contradiction on 901bb55" —
  confirms the direct run markers, the v45 git_execution_authority/
  external_process_authority transition, the v65 selftest's inherited-
  unchanged check, and the v65 selftest's NONE-value assertions all match
  the inspected evidence.
ROUND 6 (head 901bb55, formal GitHub PullRequestReview id 5181778172,
  COMMENTED, submitted 2026-09-11T17:40:12Z — a separate review object from
  the chat-style rounds above, discovered by checking
  `gh api .../pulls/329/reviews` directly rather than trusting only the
  issue-comment channel this session had been polling): 3 actionable inline
  findings on `901bb55` (comments 3991875542, 3991875552, 3991875569): (a)
  Major — S2-A001 cited only older code-tranche heads, not this PR's own
  current-head CI runs (`foundation-integrity` 34627911602,
  `s1-admission-integrity` 34627907979, both PASS for `901bb55`); (b) Minor —
  the S2-AUTH reconciliation summary said "none of the four below" for five
  bullet groups, and called every group "process history" including
  `S2-AUTH-016`, which is `PROVEN_CANONICAL_EVIDENCE_AVAILABLE`, not process
  history; (c) Major — `S2-A006` cited no immutable GitHub-hosted Founder
  decision source, author identity, or stated decision scope; the ruling
  existed only in the out-of-band governance conversation. All three
  confirmed valid and fixed: (a) this section now cites the current-round
  CI identity directly above, with the final-merge-head binding deferred to
  S2-A005/S2-A008 as designed rather than claimed here; (b) the summary
  sentence above now names five groups and states `S2-AUTH-016` separately
  from the process-history four; (c) the Founder ruling is now posted
  verbatim as PR #329 comment 5638475618, authored under the Founder's own
  GitHub account, and cited by URL/author/timestamp/scope in the S2-A006
  evidence block above.
ROUND 7 (head 07f73b9, comment 5638516466, chat-style): confirms all three
  round-6 findings reconciled ("The prior three formal findings are
  reconciled" with each restated and confirmed correct). One further
  precision issue: the S2-A006 evidence block called the Founder-decision
  GitHub comment "immutable", but a GitHub comment is editable by its
  author, so "durable"/"versioned GitHub-hosted" is the accurate word, not
  "immutable". FIXED on this head: reworded to "durable, versioned,
  GitHub-hosted, independently-checkable", with the editability caveat
  stated explicitly rather than overclaimed away.
ROUND 8 (head dab7275, comment 5638549311, chat-style): confirmed the round-7
  editability fix as correct, then found 2 items: (a) a round-count narrative
  contradiction — the section said "six rounds (five chat-style + one formal)"
  while separately listing seven numbered rounds (six chat-style: 1,2,3,4,5,7;
  one formal: 6); (b) as of the review moment, `s1-admission-integrity` had
  FAILED on `dab727517a1e5e6ca63d9e9b3f3b8318b31d22b4` (run `34629917039`),
  so current-head qualification was not complete and `S2-A001`/`S2-A002`/
  `S2-A004`/`S2-R015` had to stay unqualified until that check passed on the
  reviewed head. Both confirmed and addressed: (a) this narrative and the
  `S2_A002_ROUNDS_SO_FAR` line below now say eight rounds / six chat-style +
  one formal + one further chat-style, matching the eight numbered entries
  exactly; (b) independently re-diagnosed the failure before treating it as
  resolved — the job log (`gh run view 34629917039 --log-failed`) shows a
  transient `GitHub API request failed ... HTTP Error 403: Forbidden` inside
  `wepld_s2_s006_gitdir_reopen_v65_integrity.py verify-remote`'s remote-commit
  lookup, not a policy/content defect (this exact check had passed 8/8 times
  in a row on this branch immediately before, `runs 34626545953` through
  `34628322888`, consistent with transient GitHub API secondary rate-limiting
  under this PR's burst of successive triggers, not a reproducible failure);
  reran the identical job via `gh run rerun 34629917039 --failed` against the
  same unchanged head `dab7275` — result: **SUCCESS** (job `verify`,
  `s1-admission-integrity`, run `34629917039`, re-queried
  `2026-09-11T19:37:5xZ`). `gh pr view 329 --json statusCheckRollup` now
  shows both `foundation-integrity` and `s1-admission-integrity` as `SUCCESS`
  for the current, unchanged head `dab7275`. Current-head qualification for
  `S2-A001` is therefore genuinely complete on this exact head; not treated
  as PASS from the stale failing attempt, only from the fresh rerun result.
ROUND 9 (head 7c14055, comment 5639746161, chat-style): confirmed the round-8
  round-count fix as correct, then found 1 item: round 8's own text named its
  head imprecisely as "this PR's current head" (line 491, pre-fix) and folded
  the still-pending review of this exact fix into the round-8 count (line 586,
  pre-fix `S2_A002_ROUNDS_SO_FAR = 8 (... + this section's own pending next
  round)`), when round 8 in fact ran on `dab7275` and the pending review of
  `7c14055` is a distinct round 9, not part of round 8's count. Also noted,
  as of the review moment, both current-head checks were still `IN_PROGRESS`
  (`foundation-integrity` run `34640068359`, `s1-admission-integrity` run
  `34640066290`) and that `S2-A001`/`S2-A002`/`S2-A004`/`S2-R015` must stay
  unqualified until they complete successfully. FIXED on this head: round 8's
  narrative now names `dab7275` explicitly as its head; round 9 (this finding,
  now fixed) is itself counted as a completed round, and the pending review of
  this exact fix is round 10, not folded into round 9's own count. Independently
  re-queried after the review comment landed: `gh pr view 329 --json
  headRefOid,statusCheckRollup` shows head `7c14055` with both
  `foundation-integrity` and `s1-admission-integrity` as `SUCCESS` (the two
  runs the review cited had completed by query time) — current-head
  qualification for `S2-A001` is genuinely complete on `7c14055`, confirmed
  after, not assumed before, the checks finished.
ROUND 10 (head 54a50b1, comment 5639810201, chat-style): confirmed the
  round-9 head-naming/count fix as correct ("round-count correction is
  accurate ... correctly records nine completed rounds and a pending round
  10"), then found 1 item: this section's own "not yet closed" paragraph
  claimed "this exact fix's own head now carries green ... checks" for head
  `54a50b1`, but at review time that head's own applicable runs
  (`foundation-integrity` `34640587189`, `s1-admission-integrity`
  `34640583088`) were still `IN_PROGRESS` — the cited green runs
  (`34640068359`/`34640066290`) belonged to the prior head `7c14055`, not
  `54a50b1`. Root cause, stated plainly: a commit cannot truthfully assert
  its own resulting head's CI status, because that head and its CI runs do
  not exist yet at authoring/commit time — the round-9 fix's "not yet
  closed" paragraph made exactly that structurally-impossible claim. FIXED
  on this head: the paragraph no longer asserts the current fix's own head
  is green; it names only the most recently *independently confirmed*
  green head, and states this commit's own resulting head's qualification
  as pending until confirmed in a later step (the next round's evidence, or
  the S2-A005 final race check). The `S2-A001` evidence paragraph above was
  also generalized to stop pinning one specific head/run pair — the same
  structural trap recurs every round otherwise, as rounds 6/9/10 each show.
  Independently re-queried after this review comment landed: `gh pr view
  329 --json headRefOid,statusCheckRollup` shows head `54a50b1` with both
  `foundation-integrity` and `s1-admission-integrity` as `SUCCESS` — noted
  here as an independently-confirmed fact obtained after those runs
  completed, not asserted inside the commit that created that head.
ROUND 11 (head d58deb4, comment 5639868769, chat-style): confirmed the
  round-10 fix as correct ("addresses the prior finding"), then found 1
  further item, a deeper variant of the same class: `S2-A001` stays `[x]`
  while this candidate PR's own *literal current head* (`d58deb4`) had its
  own applicable checks still `IN_PROGRESS` (`foundation-integrity` run
  `34641102509`, `s1-admission-integrity` run `34641100233`) at review
  time. Root cause identified and fixed structurally rather than by another
  per-round patch: `S2-A001`'s checked status was never meant to depend on
  *this candidate PR's own* literal current-head CI in the first place —
  its actual subject is the exact-head qualification of the S2 *code*
  state (the two-tier `7af08de`/`71a87fe` chain above), which is fixed and
  unaffected by this docs-only PR's ongoing ledger edits. FIXED on this
  head: added an explicit "what `S2-A001` actually certifies" statement
  above distinguishing that from this PR's own per-round CI (which is
  `S2-A005`/`S2-A007`/`S2-A008` merge-admission evidence, not `S2-A001`
  evidence) — this ends the pattern rounds 6, 9, 10, and 11 each caught a
  variant of, rather than requiring an ever-later independent re-query on
  every future round.
ROUND 12 (head 671e024, comment 5639920148, chat-style): "The S2-A001
  structural correction is accurate. S2-A001 now certifies the fixed S2
  code state at 7af08de and 71a87fe. It no longer incorrectly depends on
  the moving head of this docs-only PR. The ledger correctly assigns this
  PR-head CI evidence to S2-A005, S2-A007, and S2-A008. I found no
  additional material evidence-ledger contradiction in 671e024." Noted, as
  of the review moment, `foundation-integrity` run `34641515242` and
  `s1-admission-integrity` run `34641513756` were still `IN_PROGRESS` for
  head `671e024`, with the explicit instruction not to use them until
  GitHub reports successful completion. Independently re-queried after the
  review comment landed: both runs show `status=completed,
  conclusion=success` for `head_sha=671e024ca5fc7455edadd7790a6e041d574dedc2`;
  `gh pr view 329 --json headRefOid,statusCheckRollup` confirms the same;
  `gh api .../pulls/329/reviews` shows no new formal `PullRequestReview`
  object beyond the existing round-6 one. This establishes three distinct
  facts, stated separately rather than merged into one "both channels
  clean at this head" claim (round 13's own finding on this text, below):
  the chat-style review is clean at exact head `671e024`; the round-6
  formal review's three findings (on head `901bb55`) are fully reconciled;
  and no later formal-review object exists for any head after `901bb55`,
  including `671e024` — an absence of a formal review, not a demonstrated
  clean formal review at this exact head (`AGENTS.md`: missing coverage
  evidence != PASS). `671e024`'s own CI is independently confirmed green
  after the fact.
ROUND 13 (head e24ac8f, comment 5639981277, chat-style): found 1 item: the
  round-12 entry's closing clause ("both the chat-style and formal-review
  channels are clean at this exact head") overstated the formal-review
  evidence — the only formal review object (`5181778172`) reviewed
  `901bb55`, not `671e024`; its absence on `671e024` is silence, not a
  demonstrated clean result for that exact head. FIXED on this head: the
  round-12 entry above now states the three facts separately (chat-style
  clean at `671e024`; round-6 formal findings reconciled at `901bb55`; no
  formal review exists for any later head) instead of merging them into one
  overstated two-channel claim. `S2-R015`'s standard is "no remaining
  material contradiction against both review waves" (the planning waves
  `S2-R001..009`/`S2-R010..014`, not "two live review channels on the exact
  final head") — satisfied by the chat-style round-12 confirmation plus the
  formal round-6 findings' reconciliation, not by an uncontradicted claim of
  formal-channel silence being equivalent to a pass. `e24ac8f`'s own checks
  were `IN_PROGRESS` at review time (`foundation-integrity` run
  `34642037150`, `s1-admission-integrity` run `34642035726`); independently
  re-queried after the review landed: both `SUCCESS` for
  `head_sha=e24ac8fb318dc018b7a0d051dfab16e5926ae0ff`.
ROUND 14 (head 5215e3b, CodeRabbit's persistent auto-review summary comment
  `5638026015`, last updated 2026-09-11T21:30:45Z — a distinct evidence class
  from rounds 1-13: not a chat-style reply and not a formal `PullRequestReview`
  object, but the incremental auto-review system's own per-push "recent
  review" section, which this repository's own `EXTERNAL_REVIEW_EGRESS_POLICY`
  preflight-gated `@coderabbitai review` triggers at 21:27:48/21:28:25/21:28:57
  caused to re-run and refresh): the comment states its own diff coverage
  explicitly — "Reviewing files that changed from the base of the PR and
  between `901bb55dde78671d0379b975175c74377c4d0ea7` and
  `5215e3b08be69efad5f21d751515039f7bad5f5e`" — i.e. exactly round 13's fix
  commit through this PR's current exact head, confirmed unchanged at review
  time (`gh pr view 329 --json headRefOid` = `5215e3b08be69efad5f21d751515039f7bad5f5e`).
  Verdict: "No actionable comments were generated in the recent review." Zero
  new formal `PullRequestReview` objects exist for any head after `901bb55`
  (`gh api .../pulls/329/reviews` still lists only the round-6 object) — this
  round's clean result is on the chat/auto-review channel only, the same
  channel every round since 6 has been exercised on, not a claim that the
  formal-review channel produced a second clean review. The comment also
  records `specs/.../tasks.md` as both the one file selected for processing
  and, separately, a file "skipped from review as similar to previous
  changes" — stated here verbatim rather than smoothed over, since it means
  this pass leaned on the targeted rounds 7-13 already having covered the
  bulk of the incremental diff, not a fresh full-file re-read; independently,
  this session re-read the full current-head file content directly
  (`git show origin/docs/s2-acceptance-a001-a003-a006:specs/.../tasks.md`)
  and confirmed round 13's fix text, the S2-A001 current-round CI citation,
  and the S2-A006 Founder-decision citation are all genuinely present and
  correctly worded at this exact head, rather than relying on the auto-review
  comment's "no actionable comments" line alone. `S2-A005`'s own final race
  check, immediately before merge, independently re-confirms this head's CI
  one more time rather than reusing this round's evidence. Included
  auto-review quota is now exhausted for this PR ("0 remain after this
  review" per the plan's 1-per-hour allowance) — noted as an availability
  fact about future rounds, not a qualifier on this round's own result.
```

Every finding across all fourteen rounds was reproduced/verified independently against the cited raw evidence (`gh run view <id> --log`/`--log-failed`, direct `grep`/source inspection of the frozen policy files, direct `gh api .../pulls/329/reviews` queries, direct `gh run view`/`gh pr view --json statusCheckRollup,headRefOid` re-queries) before being fixed or accepted, not merely accepted on the reviewer's assertion — consistent with `[[wepld-ledger-annotation-discipline]]`: state exactly what a check asserts, no stronger. Round 6 is itself evidence that polling only the chat-style issue-comment channel was an incomplete review-discovery method; the formal `pulls/329/reviews` endpoint is checked directly on every round rather than inferred from issue comments alone. Rounds 9-11 are evidence that describing a fast-iterating PR's own live state inside the very commit that creates or depends on that state is a structurally unreliable pattern; round 13 is evidence that "channel clean" and "channel silent" are different facts that must not be merged into one claim — silence on the formal-review channel is `AGENTS.md`'s "missing coverage evidence", not a demonstrated pass.

`S2-A002`/`S2-A004`/`S2-R015` are now **closed**: round 14, against the exact head carrying round 13's fix (`5215e3b`), reports no further material finding — "No actionable comments were generated in the recent review" for the diff `901bb55..5215e3b`, independently corroborated by this session's own direct re-read of the current-head ledger text (not accepted on the auto-review comment's assertion alone). Per this PR's own established discipline (rounds 6-13), that satisfies the "subsequent clean round on the head carrying the fix" condition. No internal/self-authored review substituted for this gate (`AGENTS.md`); the qualifying round was CodeRabbit's own auto-review system, external to this session.

```text
S2_A002_REVIEWER = CodeRabbit (coderabbitai[bot]); chat-style incremental replies (rounds 1-5,7-13), one formal PullRequestReview object (round 6), and one auto-review summary-comment refresh (round 14)
S2_A002_BASE_SHA = 71a87fe9a4e834fc9b80745a35c42df6dac58a70
S2_A002_ROUNDS_COMPLETED = 14 (12 chat-style + 1 formal review + 1 auto-review refresh); rounds 5, 12, and 14 found nothing, every other round found a real, fixed issue
S2_A002_FINDINGS_TOTAL_SO_FAR = 13 (CodeRabbit: 4 rounds 1-4, 3 round 6 formal, 1 round 7, 2 round 8, 1 round 9, 1 round 10, 1 round 11, 1 round 13) + 1 (self-audit, pre-round-5) = 15
S2_A004_UNRESOLVED_MATERIAL_FINDINGS = 0 — all 15 findings fixed and independently re-verified against their respective heads; round 14 confirms no additional finding at the current exact head `5215e3b`
S2_R015_VERDICT = CONFIRMED — round 14 (auto-review, diff `901bb55..5215e3b`) plus round 6's formal review (fully reconciled) together show no remaining material contradiction against `S2-R001..R009`/`S2-R010..R014` at this PR's current exact head
```

### S2-A005 evidence — final race check immediately before guarded merge

Re-queried live, immediately before authoring this commit (no other authorized work touches this branch concurrently): `gh pr view 329 --json headRefOid,baseRefOid,mergeable,mergeStateStatus,statusCheckRollup,state`:

```text
S2_A005_TIME = 2026-09-11T22:2x UTC (this session's live query, real wall-clock, ahead of round 14's 21:30:45Z)
S2_A005_HEAD = 5215e3b08be69efad5f21d751515039f7bad5f5e (unchanged since round 13's fix / round 14's clean review)
S2_A005_BASE = 71a87fe9a4e834fc9b80745a35c42df6dac58a70 (matches live `origin/main`; no new canonical-main commit landed during this PR's review cycle)
S2_A005_MERGEABLE = MERGEABLE, mergeStateStatus = CLEAN
S2_A005_CHECKS = foundation-integrity/verify SUCCESS, s1-admission-integrity/verify SUCCESS, CodeRabbit status SUCCESS — all three unchanged since round 14
S2_A005_STATE = OPEN, no new commits, no new reviews, no unresolved review threads (all three formal round-6 threads independently re-verified fixed at this exact head and marked resolved this session)
```

This commit itself (recording `S2-A002`/`S2-A004`/`S2-R015`/`S2-A005` closure) becomes this PR's new head after it is pushed. It is not exempted from review as "mere bookkeeping": per this PR's own established discipline (rounds 1-14, including narrative-only findings in rounds 8-13), this new head requires its own round-15 review reaching a clean result before `S2-A007`'s guarded merge — pending as of this commit, not yet triggered/reported.

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