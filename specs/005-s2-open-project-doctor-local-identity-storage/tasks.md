# S2 Task Ledger

## Canonical state markers — candidate until merged

```text
SLICE = S2
NAME = Open Project + Project Doctor + local identity/storage
PLANNING_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
INITIAL_REVIEWED_HEAD = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
PLANNING_STATE = REPAIRED_CANDIDATE_PENDING_FRESH_EXACT_HEAD_QUALIFICATION
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
ACTIVE_IMPLEMENTATION_TASK = NONE
NEXT_IMPLEMENTATION_TASK = S2-AUTH-001_NOT_AUTHORIZED_UNTIL_PLANNING_CANONICAL
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
- [x] **S2-P014A** Obtain initial exact-head Foundation qualification on `4a9b356...` (historical after tracked repair).
- [x] **S2-P015A** Record initial exact-head external-review egress preflight for `4a9b356...` (historical after tracked repair).
- [x] **S2-P016A** Obtain qualified independent CodeRabbit review on `4a9b356...`; review produced material findings.
- [x] **S2-P017A** Normalize/reconcile the nine CodeRabbit planning findings in the planning contracts/tasks.
- [ ] **S2-P014** Obtain fresh exact-head deterministic Foundation qualification on the repaired head.
- [ ] **S2-P015** Record fresh external-review egress preflight for the repaired exact head.
- [ ] **S2-P016** Obtain at least one qualified independent exact-head rereview of the repaired head.
- [ ] **S2-P017** Reconcile every valid material finding from the fresh rereview.
- [ ] **S2-P018** Rerun qualification/review after any further tracked repair.
- [ ] **S2-P019** Final race check and move planning PR Ready only with exact-head evidence.
- [ ] **S2-P019A** Reread Ready-triggered trusted-base admission and require genuine PASS on the same exact head.
- [ ] **S2-P020** Guarded merge with expected-head protection.
- [ ] **S2-P021** Prove post-merge canonical planning activation/Foundation on exact `main`.

Historical checks/reviews on a superseded head are evidence of the review process, not acceptance evidence for the repaired head. Tracked checkboxes are coordination only; live GitHub exact-head/post-merge evidence is authority for qualification claims.

## Initial independent-review finding reconciliation

The CodeRabbit review of `4a9b356...` created nine actionable threads. The repaired planning candidate incorporates these exact contract changes:

- [x] **S2-R001** Record exact live PR base SHA + trusted canonical main SHA and require equality before acceptance.
- [x] **S2-R002** Define qualified independent-review evidence and `REVIEW_BLOCKED`; reviewer unavailability is not PASS.
- [x] **S2-R003** Expand planning completion rule with trusted-base admission, egress, race checks, Ready-triggered admission, and pre/post-merge Foundation evidence.
- [x] **S2-R004** Serialize first-open identity creation with a bounded store-wide catalog reservation before per-project locking.
- [x] **S2-R005** Define immutable project generations plus atomic `CURRENT` selection so identity/index/evidence cannot be mixed across generations.
- [x] **S2-R006** Freeze bounded/cancellable `try_lock` polling and stable catalog/project busy errors; prohibit indefinite lock waits and PID lockfile takeover.
- [x] **S2-R007** Replace open-ended descriptor discovery with an exact root allowlist and explicit candidate/per-file/aggregate/depth limits.
- [x] **S2-R008** Bind Source Acquisition registry observations to trusted-base OID + source-check input head + exact registry blob SHA; require live GitHub verification for acceptance.
- [x] **S2-R009** Extend privacy to Doctor TTY/JSON/log/diagnostic output using WePLD-owned templates and allowlisted safe parameters.
- [ ] **S2-R010** Fresh independent rereview confirms the repaired head resolves the findings with no remaining material contradiction.

## Next authority transition — not yet authorized

The successor strategy is now staged so the plan in the repository is directly executable without granting broad authority prematurely.

### S2-AUTH-C — preferred first successor: contracts only

- [ ] **S2-AUTH-001** Re-read canonical S2 planning from live `main` after S2-P021.
- [ ] **S2-AUTH-002** Design the minimum append-only contracts-only successor using S1 staged-authority precedent.
- [ ] **S2-AUTH-003** Freeze exact `crates/contracts` S2 contract/export/test path allowlist for S2-C001..S2-C008.
- [ ] **S2-AUTH-004** Keep Core filesystem/process/network/model/S3/S4 effects structurally unavailable in S2-AUTH-C.
- [ ] **S2-AUTH-005** Preserve `SOURCE_ADMISSION=NONE`.
- [ ] **S2-AUTH-006** Preserve `DEPENDENCY_ADMISSION=NONE` unless a separately qualified dependency is genuinely required by the contracts tranche.
- [ ] **S2-AUTH-007** Self-test positive exact contracts candidate and negative mixed/extra-path/dependency/effect candidates.
- [ ] **S2-AUTH-008** Exact-head deterministic/review/security accounting.
- [ ] **S2-AUTH-009** Guarded merge + post-merge activation proof before S2 contract implementation.

### Later authority transitions

- [ ] **S2-AUTH-010** After contracts are canonical, authorize bounded locator/identity/evidence Core paths only.
- [ ] **S2-AUTH-011** Freeze per-platform data-root, lossless OS-path, opaque-ID, digest, catalog, generation, and locking machinery before corresponding Core mutation.
- [ ] **S2-AUTH-012** Decide any direct `uuid`/`sha2` Core dependency edge under a focused exact dependency-admission gate; transitive presence is not admission.
- [ ] **S2-AUTH-013** Decide external Git route separately: `NONE` or exact bounded Git adapter.
- [ ] **S2-AUTH-014** If Git adapter is selected, qualify executable/environment/argv/timeout/output/trust/no-hook/no-network boundaries before code.
- [ ] **S2-AUTH-015** Authorize Doctor + CLI projections only after underlying observations/contracts exist.
- [ ] **S2-AUTH-016** Keep network/model/S3/S4 authority denied throughout S2.

No S2 implementation task below becomes eligible until the canonical successor for that task explicitly grants its paths/effects.

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
- [ ] **S2-I005** Implement selected Git topology route only under exact later process/filesystem authority.
- [ ] **S2-I006** Implement worktree/common-repository distinction.
- [ ] **S2-I007** Implement superproject/submodule/nested-repository diagnostics.
- [ ] **S2-I008** Implement deterministic identity match strength ordering.
- [ ] **S2-I009** Implement conservative move/rename reassociation.
- [ ] **S2-I010** Implement collision/conflict/ambiguity handling.
- [ ] **S2-I011** Implement store-wide catalog reservation with `reserved|initialized` state and fixed catalog-before-project lock order.
- [ ] **S2-I012** Implement reservation crash recovery that reuses/revalidates the same project ID rather than allocating a second ID.
- [ ] **S2-I013** Add adversarial identity fixtures for copies/clones/worktrees/moves.
- [ ] **S2-I014** Add concurrent first-open fixture proving one identity or stable busy/conflict result, never silent duplicate identities.

## Local evidence-store tasks

- [ ] **S2-E001** Freeze per-platform WePLD local data-root contract.
- [ ] **S2-E002** Freeze lossless Unix/Windows machine path representation and safe display projection.
- [ ] **S2-E003** Implement safe opaque store/project/generation/record ID path derivation under admitted machinery.
- [ ] **S2-E004** Implement bounded record reads/version/digest/reference validation.
- [ ] **S2-E005** Implement bounded catalog/project `try_lock` protocol with 2000ms deadline, 25ms polling, cancellation, and stable busy errors.
- [ ] **S2-E006** Implement catalog temp-write/replace and reservation-state recovery.
- [ ] **S2-E007** Implement immutable project generation construction with manifest.
- [ ] **S2-E008** Implement small same-filesystem `CURRENT` temp-write/qualified-sync/atomic-replace commit point.
- [ ] **S2-E009** Implement read-once `CURRENT` generation selection; prohibit mixed-generation reads.
- [ ] **S2-E010** Implement crash/torn-write/orphan-generation/corrupt-current states.
- [ ] **S2-E011** Implement freshness state calculation/invalidation seams.
- [ ] **S2-E012** Implement privacy redaction/allowlisted persisted fields.
- [ ] **S2-E013** Add concurrent ordinary writer tests.
- [ ] **S2-E014** Add failure injection at every catalog reservation, generation-file, manifest, and `CURRENT` commit boundary.
- [ ] **S2-E015** Prove process-crash lock release on claimed platforms/filesystem classes; lock-file existence alone never blocks ownership recovery.
- [ ] **S2-E016** Add platform durability evidence; do not overclaim unsupported directory-entry/power-loss semantics.

## Project Doctor tasks

- [ ] **S2-D001** Establish stable finding-code registry and WePLD-owned text-template registry.
- [ ] **S2-D002** Identity/reservation/reassociation Doctor rules.
- [ ] **S2-D003** Repository/worktree/trust Doctor rules.
- [ ] **S2-D004** Implement exact root descriptor allowlist detection only.
- [ ] **S2-D005** Enforce `MAX_ROOT_DESCRIPTOR_CANDIDATES=32`.
- [ ] **S2-D006** Enforce parsed descriptor max 1 MiB, aggregate 4 MiB, structured nesting depth 64 before/while parsing.
- [ ] **S2-D007** Keep lock/package-manager markers presence-only in baseline S2 unless a later parser contract is explicitly authorized.
- [ ] **S2-D008** Toolchain descriptor facts remain descriptive; no command execution/eval.
- [ ] **S2-D009** Lockfile/package-manager ambiguity rules.
- [ ] **S2-D010** Evidence catalog/current-generation corruption rules.
- [ ] **S2-D011** Freshness/staleness rules.
- [ ] **S2-D012** Security-sensitive configuration observations report safe classes/counts without raw values.
- [ ] **S2-D013** Stable finding ordering/explanations/remediation hints using template IDs and safe parameters only.
- [ ] **S2-D014** Negative test proving Doctor executes no repository task/installer/remediation.
- [ ] **S2-D015** Negative TTY/JSON tests for credential URLs, environment tokens, manifest command strings, and ANSI/control injection.

## CLI / command-plane tasks

- [ ] **S2-CLI001** Reconcile exact exit-code values with existing CLI conventions.
- [ ] **S2-CLI002** Freeze stable machine error classes for identity conflict, catalog/store busy, capability unavailable, evidence corruption, and blocking Doctor findings.
- [ ] **S2-CLI003** Implement `open` command contract and human projection.
- [ ] **S2-CLI004** Implement `doctor` command contract and human projection.
- [ ] **S2-CLI005** Implement `status` command contract and human projection.
- [ ] **S2-CLI006** Implement stable `--json` projection from the same redacted semantic model as TTY.
- [ ] **S2-CLI007** Implement/verify `--no-input` behavior.
- [ ] **S2-CLI008** Verify unknown commands stay errors with suggestions.
- [ ] **S2-CLI009** Preserve explicit future JSONL/event interface without overbuilding streaming.
- [ ] **S2-CLI010** Shell-completion surface for new commands only if existing CLI architecture admits it.

## Security / adversarial tasks

- [ ] **S2-S001** Path traversal/canonicalization/TOCTOU test suite.
- [ ] **S2-S002** Symlink loop/broken link tests.
- [ ] **S2-S003** Windows junction/reparse/extended-length path tests where runner capability permits.
- [ ] **S2-S004** Case sensitivity/case-only path identity tests.
- [ ] **S2-S005** Git `safe.directory` refusal test; prove no auto-bypass.
- [ ] **S2-S006** Malicious `.git`/gitfile/topology parsing tests.
- [ ] **S2-S007** External Git output/environment/parser/timeout/no-hook/no-network tests if Git adapter admitted.
- [ ] **S2-S008** Secret-bearing remote/config/environment/output redaction tests across store, TTY, JSON, logs, diagnostics.
- [ ] **S2-S009** Corrupt/oversized/unsupported/mixed-generation evidence record tests.
- [ ] **S2-S010** First-open identity split race test.
- [ ] **S2-S011** Lock contention denial test proves bounded completion.
- [ ] **S2-S012** Descriptor amplification tests for count/per-file/aggregate/depth limits.
- [ ] **S2-S013** Repository mutation negative oracle: open/doctor/status leave project tree unchanged.
- [ ] **S2-S014** Network negative oracle: S2 command path has no required network effect.

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
- [ ] **S2-A007** Merge only under canonical authority with expected-head protection.
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
