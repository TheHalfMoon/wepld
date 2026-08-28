# S2 Task Ledger

## Canonical state markers — candidate until merged

```text
SLICE = S2
NAME = Open Project + Project Doctor + local identity/storage
PLANNING_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
PLANNING_STATE = CANDIDATE_NOT_CANONICAL
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
- [ ] **S2-P014** Obtain exact-head deterministic Foundation qualification.
- [ ] **S2-P015** Record external-review egress preflight for exact planning head.
- [ ] **S2-P016** Obtain at least one qualified independent exact-head planning review.
- [ ] **S2-P017** Reconcile every valid material finding.
- [ ] **S2-P018** Rerun qualification/review after any tracked repair.
- [ ] **S2-P019** Move planning PR Ready only with exact-head evidence.
- [ ] **S2-P020** Guarded merge with expected-head protection.
- [ ] **S2-P021** Prove post-merge canonical planning activation on `main`.

Tracked checkboxes are coordination only. Live GitHub exact-head/post-merge evidence is authority for qualification claims.

## Next authority transition — not yet authorized

- [ ] **S2-AUTH-001** From canonical S2 planning, design the minimum append-only implementation-authority successor (provisional v22).
- [ ] **S2-AUTH-002** Freeze exact implementation path allowlist.
- [ ] **S2-AUTH-003** Decide external Git process route: `NONE` or exact bounded Git adapter.
- [ ] **S2-AUTH-004** Keep network/model/S3/S4 authority denied.
- [ ] **S2-AUTH-005** Preserve `SOURCE_ADMISSION=NONE` unless a separately qualified source import is genuinely required.
- [ ] **S2-AUTH-006** Preserve `DEPENDENCY_ADMISSION=NONE` unless a separately qualified dependency is genuinely required.
- [ ] **S2-AUTH-007** Self-test successor with positive/negative exact-delta fixtures.
- [ ] **S2-AUTH-008** Exact-head deterministic/review/security accounting.
- [ ] **S2-AUTH-009** Guarded merge + post-merge activation proof.

No S2 implementation task below becomes eligible until the canonical successor explicitly grants its paths/effects.

## Contract tasks

- [ ] **S2-C001** Define versioned `ProjectLocator` contract.
- [ ] **S2-C002** Define versioned `RepositoryTopology` contract.
- [ ] **S2-C003** Define local project identity/reassociation result contracts.
- [ ] **S2-C004** Define evidence envelope, provenance, freshness, and status contracts.
- [ ] **S2-C005** Define Doctor finding/report/remediation-hint contracts.
- [ ] **S2-C006** Define command response/error JSON envelopes.
- [ ] **S2-C007** Add bounded canonical serialization/deserialization helpers inside admitted contract machinery.
- [ ] **S2-C008** Add contract snapshot/round-trip/unknown-version/redaction tests.

## Project locator / identity tasks

- [ ] **S2-I001** Implement input + lexical absolute path observation.
- [ ] **S2-I002** Implement resolved-path observation with explicit errors.
- [ ] **S2-I003** Implement bounded symlink/reparse metadata observation.
- [ ] **S2-I004** Implement non-Git project root semantics.
- [ ] **S2-I005** Implement selected Git topology route under exact process/filesystem authority.
- [ ] **S2-I006** Implement worktree/common-repository distinction.
- [ ] **S2-I007** Implement superproject/submodule/nested-repository diagnostics.
- [ ] **S2-I008** Implement deterministic identity match strength ordering.
- [ ] **S2-I009** Implement conservative move/rename reassociation.
- [ ] **S2-I010** Implement collision/conflict/ambiguity handling.
- [ ] **S2-I011** Add adversarial identity fixtures for copies/clones/worktrees/moves.

## Local evidence-store tasks

- [ ] **S2-E001** Freeze per-platform WePLD local data-root contract.
- [ ] **S2-E002** Implement safe store/project ID path derivation.
- [ ] **S2-E003** Implement bounded record reads/version validation/digest validation.
- [ ] **S2-E004** Implement qualified lock/concurrency protocol.
- [ ] **S2-E005** Implement same-store temp-write + commit/replace protocol.
- [ ] **S2-E006** Implement crash/torn-write/corrupt-record states.
- [ ] **S2-E007** Implement freshness state calculation/invalidation seams.
- [ ] **S2-E008** Implement privacy redaction/allowlisted persisted fields.
- [ ] **S2-E009** Add concurrent writer and failure-injection tests.
- [ ] **S2-E010** Add platform durability evidence; do not overclaim unsupported directory-flush semantics.

## Project Doctor tasks

- [ ] **S2-D001** Establish stable finding-code registry.
- [ ] **S2-D002** Identity/reassociation Doctor rules.
- [ ] **S2-D003** Repository/worktree/trust Doctor rules.
- [ ] **S2-D004** Workspace descriptor detection.
- [ ] **S2-D005** Toolchain descriptor detection.
- [ ] **S2-D006** Lockfile/package-manager ambiguity rules.
- [ ] **S2-D007** Evidence-store corruption rules.
- [ ] **S2-D008** Freshness/staleness rules.
- [ ] **S2-D009** Security-sensitive configuration observations.
- [ ] **S2-D010** Stable finding ordering/explanations/remediation hints.
- [ ] **S2-D011** Negative test proving Doctor executes no repository task/installer/remediation.

## CLI / command-plane tasks

- [ ] **S2-CLI001** Reconcile exact exit-code values with existing CLI conventions.
- [ ] **S2-CLI002** Implement `open` command contract and human projection.
- [ ] **S2-CLI003** Implement `doctor` command contract and human projection.
- [ ] **S2-CLI004** Implement `status` command contract and human projection.
- [ ] **S2-CLI005** Implement stable `--json` projection.
- [ ] **S2-CLI006** Implement/verify `--no-input` behavior.
- [ ] **S2-CLI007** Verify unknown commands stay errors with suggestions.
- [ ] **S2-CLI008** Preserve explicit future JSONL/event interface without overbuilding streaming.
- [ ] **S2-CLI009** Shell-completion surface for new commands if existing CLI architecture admits it.

## Security / adversarial tasks

- [ ] **S2-S001** Path traversal/canonicalization/TOCTOU test suite.
- [ ] **S2-S002** Symlink loop/broken link tests.
- [ ] **S2-S003** Windows junction/reparse/extended-length path tests where runner capability permits.
- [ ] **S2-S004** Case sensitivity/case-only path identity tests.
- [ ] **S2-S005** Git `safe.directory` refusal test; prove no auto-bypass.
- [ ] **S2-S006** Malicious `.git`/gitfile/topology parsing tests.
- [ ] **S2-S007** External Git output bounds/parser fuzz/timeout tests if Git adapter admitted.
- [ ] **S2-S008** Secret-bearing remote/config redaction tests.
- [ ] **S2-S009** Corrupt/oversized/unsupported evidence record tests.
- [ ] **S2-S010** Repository mutation negative oracle: open/doctor/status leave project tree unchanged.
- [ ] **S2-S011** Network negative oracle: S2 command path has no required network effect.

## Platform / performance tasks

- [ ] **S2-Q001** Windows deterministic gate.
- [ ] **S2-Q002** Linux deterministic gate.
- [ ] **S2-Q003** macOS gate when available or explicit coverage limitation.
- [ ] **S2-Q004** Large-repository fixture proves baseline open avoids whole-tree traversal.
- [ ] **S2-Q005** Evidence-store bounded-read/size tests.
- [ ] **S2-Q006** Git adapter timeout/output ceiling benchmark if admitted.
- [ ] **S2-Q007** Publish p50/p95 or deterministic ceiling evidence with fixture identity.

## Acceptance / learning tasks

- [ ] **S2-A001** Exact-head full deterministic qualification.
- [ ] **S2-A002** Independent correctness/engineering review.
- [ ] **S2-A003** Codex Security when available/applicable; otherwise exact limitation accounting.
- [ ] **S2-A004** Reconcile all findings; no voting away valid defects.
- [ ] **S2-A005** Guarded S2 acceptance decision with exact-head evidence.
- [ ] **S2-A006** Merge only under canonical authority.
- [ ] **S2-A007** Post-merge canonical verification.
- [ ] **S2-A008** Build Learning capture.

## Explicit stop conditions

Stop implementation and return to authority/planning if any task requires:

- an unlisted source path;
- a new dependency not admitted by the active policy;
- source import;
- arbitrary project process execution;
- network access;
- repository mutation beyond exact S2 authority;
- S3 Terminal Fabric;
- S4 semantic graph;
- model/provider execution;
- weakening Git/platform trust controls.
