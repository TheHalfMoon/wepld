# Tasks — S1 Desktop ↔ Rust Trusted Core Handshake

This is the execution-authoritative S1 task ledger. A checked box requires stable evidence; a task description never grants authority beyond its own gate.

```text
SLICE = S1
S1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
CANONICAL_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
LEDGER_RECONCILIATION_BASE = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
LIVE_MAIN = MUST_BE_READ_FROM_GITHUB
ACTIVE_TASK = NONE
NEXT_TASK = S2_NOT_STARTED_NOT_AUTHORIZED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER
S1_015 = CLOSED_CANONICAL_PROVEN
S1_016 = CLOSED_CANONICAL_PROVEN
S1_ACCEPTED = YES
S2 = NOT_STARTED
S2_AUTHORITY = NOT_GRANTED
```

## Canonical reconciliation checkpoint — 2026-08-20

This checkpoint reconciles the execution-authoritative ledger against live GitHub merge and post-merge evidence. Historical status text below is retained for traceability, but the current task state is the reconciled state above and the checked requirements below.

```text
S1-003 = CLOSED_CANONICAL_PROVEN / PR #4 / merge af000ec9cd4a1ce71545cdc509f13af0e69429f9
S1-003_ACTIVATION = PROVEN / canary PR #6 / closed without merge
S1-004 = CLOSED_CANONICAL_PROVEN / PR #7 / merge f1919396eacb90d8d947b06f023ae9da233a4580
S1-005 = CLOSED_CANONICAL_PROVEN / PR #11 / merge 3ab1818802352d7eab45448ed3284489e67631f4
S1-006 = CLOSED_CANONICAL_PROVEN / PR #14 / merge a2dcc7d148eb0c38243eb2da655e0c3aac5651c9
S1-007 = CLOSED_CANONICAL_PROVEN / PR #17 / merge 24ef630d38b184cd05238dd62d4e5e92efe014ae
S1-008 = CLOSED_CANONICAL_PROVEN / PR #19 / merge e629322723c63448874a86c1cd4871579d64dfe1
S1-009 = CLOSED_CANONICAL_PROVEN / PR #22 / merge acd60e5cd8df31597bdc9263b1508d233b86cc24
S1-010 = CLOSED_CANONICAL_PROVEN / PR #25 / merge eeb8d78b95a1710e3489d8174a3aff979df4d6dd
S1-011 = CLOSED_CANONICAL_PROVEN / PR #33 / merge fbfe484dd8f506ca563affa8a2777ce37863580f
S1-012 = CLOSED_CANONICAL_PROVEN / PR #37 / merge 848566d89e5995e215295b92d9da4a9cfbe28927
S1-012_POST_MERGE_FOUNDATION = run 32291764730 / #331 / push / PASS
S1-012_POST_MERGE_CONTRACTS = run 32291764814 / #118 / push / PASS
S1-013_PLUS = NOT_STARTED
```

`CANONICAL_EXECUTION_HEAD` records the last code/policy execution milestone, not a promise that the live `main` ref will remain byte-identical after later docs-only reconciliation commits. Read live GitHub before every write, review, Ready transition, merge, or next-task start.

## Canonical S1-013 reconciliation checkpoint — 2026-08-26

This checkpoint reconciles the execution-authoritative ledger against the exact repaired S1-013 performance measurement now canonical on `main`. The candidate text used to propose this checkpoint did not grant closeout authority; the checkpoint counts only when its exact content-addressed transition has been qualified, merged, and verified from canonical `main` under the governing successor policy.

```text
S1-013 = CLOSED_CANONICAL_PROVEN
S1-013_MEASUREMENT_PR = #179
S1-013_MEASUREMENT_HEAD = c4fe5b1bbc4c27c68413e57019d3b47c9520997c
S1-013_MEASUREMENT_MERGE = 96fa229610f31598326493b75b40a3353b46bbbf
S1-013_POST_MERGE_FOUNDATION = run 32955349075 / #700 / push / PASS
S1-013_POST_MERGE_CONTRACTS = run 32955348827 / #162 / push / PASS_3_OF_3
S1-013_POST_MERGE_PERFORMANCE = run 32955348872 / #5 / push / PASS
S1-013_EVIDENCE = specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md
S1-013_RAW_ACTION_ARTIFACT = NONE_UPLOADED
S1-013_BUDGET_TIGHTENING_DECISION = NO_SAFE_LOWER_BOUND_PROVEN_KEEP_EXISTING_SAFETY_LIMITS
S1-014_PLUS = NOT_STARTED
```

The absence of an uploaded Actions artifact is retained as an evidence-retention limitation; the canonical GitHub workflow log/summary remains the source of measured values. The measured values do not justify lowering any existing S1 safety upper bound, so keeping the existing limits is the evidence-based S1-013 decision rather than an unproven tuning change.

## Canonical S1-014 review reconciliation checkpoint — 2026-08-27

This checkpoint reconciles the exact S1 review gate against the complete S1 range and the canonical acceptance candidate at `58ad0d166b6177ae69d04ff59da17aa8cc0e3c28`. Completion of S1-014 means the required review/accounting work was performed and normalized; it does **not** mean the review was clean, the unavailable Codex Security surface passed, or S1 is accepted. One valid material finding remains and is routed to S1-015.

```text
S1-014 = CLOSED_CANONICAL_PROVEN
S1-014_ACCEPTANCE_CANDIDATE = 58ad0d166b6177ae69d04ff59da17aa8cc0e3c28
S1-014_ORIGINAL_RANGE_BASE = 6eff72319cad99c878a80f0d5bce9f107d213679
S1-014_REVIEW_ONLY_PR = #191 / CLOSED_UNMERGED
S1-014_QODO_REVIEW_COMMENT = 5434723966 / DEEP / 2_BUGS / 2_RULE_VIOLATIONS
S1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1-014_SECURITY_PASS = NO
S1-014_VALID_MATERIAL_FINDINGS = 1
S1-014_VALID_FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE
S1-014_EVIDENCE = specs/001-desktop-rust-trusted-core-handshake/s1-014-review-evidence.md
S1-015 = NOT_STARTED
```

The review-only PR intentionally used the original S1 base solely to expose the complete 427-commit / 286-file range to hosted review and was closed without merge. Its synthetic-base Foundation failure is not acceptance evidence. The exact candidate remains the canonical `main` commit above, whose Foundation #723 passed. Findings were validated against that exact candidate: one performance-workflow trigger-coverage defect is material and requires bounded S1-015 repair; two machine-readable-report rule findings are non-material external policy rules with canonical rejection precedent; and the alleged missing-v13 admission script is a synthetic-review-base false positive contradicted by genuine trusted-base admission runs #561 and #562.

## Canonical S1-015 repair reconciliation checkpoint — 2026-08-27

This checkpoint closes only the bounded repair/reconciliation task after the exact repair was qualified, reviewed, merged, and exercised by the canonical post-merge performance workflow.

```text
S1-015 = CLOSED_CANONICAL_PROVEN
S1-015_FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE
S1-015_REPAIR_PR = #197
S1-015_REPAIR_HEAD = 1229bdd9a411c70cce5494185c1f6c7814fa2085
S1-015_REPAIR_MERGE = 9ae784106f36c2234e3cdf6befdb03449a224c34
S1-015_REPAIRED_WORKFLOW_BLOB = 3ccd118aea80fd31866973371babc329913aafb8
S1-015_EXACT_HEAD_FOUNDATION = run 33068200273 / #737 / PASS
S1-015_EXACT_HEAD_ADMISSION = run 33069378037 / #576 / PASS
S1-015_EXACT_HEAD_PERFORMANCE = run 33068200332 / #7 / PASS
S1-015_QODO_REVIEW = comment 5438445407 / 0_BUGS / 0_RULE_VIOLATIONS / 0_REQUIREMENT_GAPS
S1-015_POST_MERGE_FOUNDATION = run 33069506354 / #738 / PASS
S1-015_POST_MERGE_PERFORMANCE = run 33069506387 / #8 / PASS
S1-015_UNRESOLVED_MATERIAL_FINDINGS = 0
S1-015_EVIDENCE = specs/001-desktop-rust-trusted-core-handshake/s1-015-repair-evidence.md
S1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1-014_SECURITY_PASS = NO
S1_ACCEPTED = NO
S1-016 = NOT_STARTED
```

The Codex Security coverage limitation remains explicit and is not converted into PASS. S1-015 closeout also does not accept S1; S1-016 remains the separate acceptance and Build Learning task.

## Canonical S1-016 acceptance and Build Learning reconciliation checkpoint — 2026-08-27

This checkpoint accepts S1 only after the complete S1 evidence chain, bounded repair, canonical S1-015 closeout, and post-merge Foundation verification are reconciled. It records the accepted execution head and the Build Learning material promoted by this exact transition. It grants no S2 implementation or roadmap-mutation authority.

```text
S1-016 = CLOSED_CANONICAL_PROVEN
S1_ACCEPTED = YES
S1_ACCEPTANCE_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
S1_ACCEPTANCE_EXECUTION_TREE = c63bea084edd9cc1f3fcfe5f574518339f510426
S1-015_CLOSEOUT_PR = #199
S1-015_CLOSEOUT_MERGE = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
S1-015_CLOSEOUT_POST_MERGE_FOUNDATION = run 33083905553 / #744 / PASS
S1_ACCEPTANCE_RECORD = specs/001-desktop-rust-trusted-core-handshake/acceptance.md
S1_BUILD_LEARNING_LEDGER = docs/learning/BUILD_LEARNING_LEDGER.md
S1_BUILD_LEARNING_QUALIFIED = BL-0004..BL-0009
S1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1-014_SECURITY_PASS = NO
S1-015_UNRESOLVED_MATERIAL_FINDINGS = 0
S2 = NOT_STARTED
S2_AUTHORITY = NOT_GRANTED
```

The accepted head does not erase explicit coverage limitations. Codex Security remains non-PASS, S3 containment is not claimed, and no later-slice authority is inferred from S1 acceptance.

## S1-001 — Establish planning baseline

- [x] Create S1 branch from accepted P0 merge commit.
- [x] Recover byte-identical V2.2 plan and exact S1 requirements.
- [x] Complete constitution/spec/clarify/plan/checklist.
- [x] Execute Ponytail FULL for planning.
- [x] Establish component-level Source Acquisition preflight.
- [x] Complete threat model.
- [x] Reconcile provisional decomposition through `analyze.md`.

Evidence: planning commit `b114fc503c5fba17072b2870612815fd07cc8c8c` and `specs/001-desktop-rust-trusted-core-handshake/**`.

## S1-002 — Publish and close reviewed S1 planning baseline

- [x] Open Draft PR #3 against `main`.
- [x] Publish live canonical checkpoint.
- [x] Reconcile all planning/reviewer-egress findings.
- [x] Pass exact-head `foundation-integrity` on final planning head `f3f88eeed8789c48a6a1f4b280126333d2d2d2e8`. Evidence: run `31907831641` / #145.
- [x] Obtain qualified exact-head independent review with zero unresolved material threads.
- [x] Merge reviewed planning baseline.
- [x] Verify canonical-main post-merge integrity.

Evidence:

```text
PR_3_FINAL_HEAD = f3f88eeed8789c48a6a1f4b280126333d2d2d2e8
PR_3_MERGE_COMMIT = 12fd72c19d639b4b72a8dec8dba644282383d0db
MAIN_POST_MERGE_INTEGRITY = 31908187069 / #146 PASS
```

The planning merge did not accept S1 or admit dependencies.

## S1-003 — Migrate P0 foundation CI to stage-aware S1 integrity

Historical execution PR: #4.

### Implemented on policy head `7bafe4b1f0e9cb6319526cfd957baf92ba6d7775`

- [x] Preserve immutable P0 archive/V2.2/402-registry validation.
- [x] Preserve bounded/no-follow local archive reads and bounded remote candidate-blob reads.
- [x] Preserve symlink/gitlink/repair-payload/duplicate-security-policy protections.
- [x] Add case-insensitive tracked-path collision rejection.
- [x] Replace the P0-only one-shape prohibition with explicit structural stages:
  - `S1_PLANNING_ONLY`;
  - `S1_DEPENDENCY_RESOLUTION_INPUT`;
  - `S1_DEPENDENCY_RESOLUTION_LOCKED`.
- [x] Keep product implementation as an unavailable stage; no Markdown/status/branch/label switch unlocks code.
- [x] Define the exact Stage-B Cargo/toolchain/skeleton candidate shape.
- [x] Reject partial Stage-B trees.
- [x] Reject direct `tauri-plugin-shell`, Core `tokio`, network package, wildcard dependency, git dependency, arbitrary package-manager files, later-slice crates, extra Rust modules, and extra workflows through exact templates/path policy.
- [x] Define bounded candidate `Cargo.lock` parsing/source/checksum/package rules.
- [x] Add deterministic policy self-tests using the same classification/template/lock/base-control functions used by real verification.
- [x] Pin `actions/checkout` v7.0.1 to commit `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- [x] Keep the PR-head `foundation-integrity` path tokenless with `permissions: {}`.
- [x] Add base-controlled `s1-admission-integrity` using `pull_request_target` with `contents:read`.
- [x] Ensure the privileged/base-controlled path performs **no candidate checkout and no candidate code execution**; candidate Git tree/blob objects are inspected as data through GitHub API.
- [x] Freeze policy/workflow/core-governance paths byte-for-byte against ordinary future candidate mutation.
- [x] Preserve explicit CodeRabbit/Cubic repository config defense-in-depth.
- [x] Record that Cubic provider-effective behavior conflicts with repository intent after a second automatic-description incident; Cubic is `BLOCKED/NOT_RUN`, never PASS.
- [x] Document that GitHub platform required-check enforcement is not proven/configured by this PR.
- [x] Pass policy implementation exact-head self-check. Evidence: `31909208235` / #148 PASS on `7bafe4b1f0e9cb6319526cfd957baf92ba6d7775`.

### Required before PR #4 merge — completed

- [x] Re-run `foundation-integrity` on the exact head after canonical-memory/task checkpoint.
- [x] Inspect deterministic job steps and preserve exact run ID.
- [x] Record exact-head Codex Security status; if unavailable, `NOT_RUN_NON_BLOCKING`, never PASS.
- [x] Perform exact-head public-source secret-marker screening before any hosted reviewer.
- [x] Obtain at least one independently qualified exact-head correctness/engineering review. Cubic is currently ineligible.
- [x] Validate every finding against current code/policy.
- [x] Repair only valid findings.
- [x] Rerun every affected gate/review after repair.
- [x] Zero unresolved material findings.
- [x] Merge PR #4 only as the reviewed S1-003 policy migration, not as S1 acceptance.

### Post-merge S1-003 activation proof — completed

PR #4 could not exercise `s1-admission-integrity` authoritatively because the workflow was not present in its base commit. Canary PR #6 later proved activation from canonical base and was closed without merge.

- [x] Verify post-merge canonical-main `foundation-integrity`.
- [x] Create a docs-only activation-canary PR from the post-merge main.
- [x] Prove `s1-admission-integrity` runs from the base policy.
- [x] Prove the authoritative path reads candidate Git objects as data only and reports the expected prior stage.
- [x] Confirm no candidate checkout/build/script execution occurs in that privileged path.
- [x] Close the canary according to its narrow evidence purpose without merging its inert marker.
- [x] Set `S1_003_ACTIVATION_PROVEN = YES` only after canary evidence is exact and complete.

Evidence: PR #4 merge `af000ec9cd4a1ce71545cdc509f13af0e69429f9`; PR #6 records `S1_003_ACTIVATION_PROVEN = YES` with trusted-base admission PASS.

Gate satisfied: **S1-004 manifests remained prohibited until the post-merge activation canary passed.**

## S1-004 — Resolve candidate dependency graph without product behavior

- [x] Start only after `S1_003_ACTIVATION_PROVEN = YES`.
- [x] Add the exact Rust toolchain candidate required by S1-003 policy.
- [x] Add the exact minimum Cargo workspace/manifests/skeletons allowed by S1-003 Stage B1.
- [x] Candidate direct deps: Tauri 2.11.5, Tauri-build 2.6.3, Serde 1.0.229, serde_json 1.0.151.
- [x] Keep `tauri-plugin-shell` absent.
- [x] Keep direct Tokio/Core async framework absent.
- [x] Pass authoritative `s1-admission-integrity` in `S1_DEPENDENCY_RESOLUTION_INPUT`.
- [x] Generate `Cargo.lock`.
- [x] Pass authoritative `s1-admission-integrity` in `S1_DEPENDENCY_RESOLUTION_LOCKED`.
- [x] Capture direct/transitive feature tree.
- [x] Generate SBOM.
- [x] Run advisory/security dependency scan.
- [x] No product behavior beyond exact manifest/toolchain/target skeleton required for resolution.

Evidence: PR #7 merged as `f1919396eacb90d8d947b06f023ae9da233a4580`; its exact-head evidence records `S1_DEPENDENCY_RESOLUTION_LOCKED`, SBOM/advisory output, and no product authorization.

Status semantics:

```text
DEPENDENCY_RESOLUTION_AUTHORIZED = YES_AFTER_S1_003_ACTIVATION_CANARY
RUNTIME_DEPENDENCY_ADMITTED = NO_UNTIL_S1_005
```

## S1-005 — Finalize component admission / Source Acquisition Check

- [x] Reconcile exact resolved versions and features against intended candidates.
- [x] Reconcile every reportable advisory or coverage limitation.
- [x] Prove no unnecessary direct dependency remains.
- [x] Record Tauri capability surface and package/sidecar strategy.
- [x] Record replacement/exit strategy per admitted component.
- [x] Update `docs/governance/DEPENDENCY_REGISTER.md` for the exact S1 graph.
- [x] Add immutable S1 component-admission evidence.
- [x] Set `SOURCE_ACQUISITION_CHECK = PASS` only if all required evidence is complete.

Evidence: PR #11 merged as `3ab1818802352d7eab45448ed3284489e67631f4`; exact-head evidence records `SOURCE_ACQUISITION_CHECK=PASS`, zero audit vulnerabilities, explicit maintenance-debt reconciliation, and exact GLib backport provenance.

Gate satisfied: **S1 product implementation remained prohibited until this task passed.**

## S1-006 — Implement protocol v1 contracts and bounded frame codec

- [x] Create typed protocol request/response/event/cancel/error enums/structs.
- [x] Freeze protocol v1 constants and capability schema.
- [x] Freeze one framing-size contract: `LENGTH_PREFIX_BYTES = 4`, `MAX_PAYLOAD_BYTES = 65_536`, `MAX_WIRE_FRAME_BYTES = 65_540`.
- [x] Implement 4-byte big-endian payload-length framing.
- [x] Read/validate the prefix before payload allocation/read/deserialization; reject declared payload length `> 65_536`.
- [x] Prove declared payload length exactly `65_536` is within bound and `65_537` is rejected before payload allocation/read/deserialization.
- [x] Strictly reject unknown versions/kinds/principals/operations and malformed required data.
- [x] Add golden fixtures and unit/property/negative tests.
- [x] No process, filesystem, network, UI, or project effects.

Evidence: PR #14 merged as `a2dcc7d148eb0c38243eb2da655e0c3aac5651c9` after exact-head foundation/contracts/admission gates and independent review.

## S1-007 — Implement pure handshake / replay / cancellation state

- [x] Implement launch/request correlation semantics.
- [x] Implement serialized strictly increasing inbound command IDs per launch and an O(1) Core high-water mark; IDs never wrap/reuse within a launch.
- [x] Reject every command with `id <= highest_accepted_command_id` before dispatch.
- [x] Implement bounded in-flight/watch state.
- [x] Implement health/version/capability operations.
- [x] Implement bounded health-observation state and deterministic cancellation.
- [x] Prove duplicate observation cannot allocate a second watch/event stream.
- [x] Prove replayed cancellation cannot mutate state again and fresh cancellation of an already terminal operation is deterministic/non-mutating.
- [x] Prove stale launch IDs, non-monotonic/reused IDs, cancellation races, and budget exhaustion fail deterministically.
- [x] Keep logic testable without Tauri or OS child processes.

Evidence: PR #17 merged as `24ef630d38b184cd05238dd62d4e5e92efe014ae`; exact-head admission classified `S1_HANDSHAKE_STATE_CANDIDATE / S1_007_ONLY` and the bounded state suite passed.

## S1-008 — Implement separate Rust Core child process

- [x] Core protocol bytes use inherited stdin/stdout only.
- [x] Core stderr is diagnostics-only and is never parsed as protocol data.
- [x] Use stdlib process/IO/concurrency primitives unless a separately qualified need changes this.
- [x] No network listener/client for the S1 Desktop ↔ Core handshake.
- [x] No project/filesystem/terminal/worker authority.
- [x] EOF/broken input terminates or degrades predictably.
- [x] Malformed/oversized protocol data cannot fabricate success.
- [x] Add Core process integration tests.

Evidence: PR #19 merged as `e629322723c63448874a86c1cd4871579d64dfe1`; exact-head admission classified `S1_CORE_PROCESS_CANDIDATE / S1_008_ONLY` and process tests passed.

## S1-009 — Implement Desktop-owned Core lifecycle and protocol client

- [x] Resolve explicit packaged sibling Core executable path; no shell/PATH lookup.
- [x] Launch separate Core child with piped stdin/stdout and an explicit stderr strategy.
- [x] If stderr is piped, drain it concurrently with bounded retained diagnostics and observable truncation.
- [x] Assign `desktop_host` principal and fresh launch ID internally.
- [x] Allocate request/cancel command IDs in the same serialized order frames are written to Core.
- [x] Implement typed request/event/cancel client.
- [x] EOF/child exit immediately invalidates readiness.
- [x] Restart uses a new launch ID and invalidates prior in-flight operations.
- [x] Bound restart/retry behavior; no infinite silent restart loop.
- [x] Record observed orphan/cleanup behavior without claiming S3 containment.

Evidence: PR #22 merged as `acd60e5cd8df31597bdc9263b1508d233b86cc24`; exact-head Windows lifecycle tests and trusted-base `S1_009_ONLY` admission passed.

## S1-010 — Implement minimal Tauri shell and static presentation

- [x] Minimal Tauri Desktop application only.
- [x] Bundle Core using the minimum qualified Tauri external-binary mechanism.
- [x] Expose only narrow typed status/control projection needed by S1 UI.
- [x] No general shell/filesystem/network permission to WebView merely for the S1 handshake.
- [x] Static local UI shows Core readiness/health/version/capabilities and cancellable observation state.
- [x] Keyboard/focus/status semantics satisfy the applicable accessibility baseline.
- [x] No React/Vite/Tailwind/frontend package manager unless a new measured need is qualified.

Evidence: PR #25 merged as `eeb8d78b95a1710e3489d8174a3aff979df4d6dd` after canonical v18 admission; final visual/branding design remains separately deferred and the tracked icon is a neutral technical build fixture.

## S1-011 — Cross-process failure/adversarial suite

- [x] Valid request/response round-trip.
- [x] Event delivery and cancellation.
- [x] Unknown command/version/principal and downgrade attempt.
- [x] Zero-length payload and malformed/truncated framing.
- [x] Declared payload length `65_536` is within bound; `65_537` is rejected before payload allocation/read/deserialization.
- [x] Invalid UTF-8/text contract cases.
- [x] Duplicate/replay/non-monotonic command IDs and stale launch.
- [x] Replay after terminal/cache eviction remains rejected by launch-wide high-water state.
- [x] Duplicate observation cannot allocate a second watch/event stream.
- [x] Replayed cancellation cannot mutate twice; fresh cancel of terminal target is deterministic/non-mutating.
- [x] Cancellation of unknown/completed/already-cancelled request and cancellation race.
- [x] In-flight/watch budget exhaustion.
- [x] Core unavailable/crash/restart.
- [x] Desktop writer/reader loss and Desktop exit.
- [x] Stale response/event after restart.
- [x] Wrong/missing/mismatched Core binary/package scenario.
- [x] Emit diagnostics beyond expected OS stderr pipe capacity while protocol exchanges continue.

Evidence: PR #33 merged as `fbfe484dd8f506ca563affa8a2777ce37863580f`; canonical v22 authorized only the exact adversarial projection and final exact-head foundation/contracts/admission/review gates passed.

## S1-012 — Windows-first qualification and secondary platform evidence

- [x] Windows x86_64 MSVC build from clean checkout.
- [x] Windows Desktop launches intended packaged Core sibling.
- [x] Windows typed round-trip/event/cancel/failure suite passes.
- [x] Windows Core crash/restart and Desktop-exit child behavior recorded.
- [x] Windows packaging path/version mismatch cases exercised.
- [x] Linux compile + protocol/contract tests.
- [x] macOS compile + protocol/contract tests when runner availability permits; otherwise record exact coverage limitation.
- [x] No compile-only result is reported as runtime containment/process-ownership proof.

Evidence: PR #37 merged as `848566d89e5995e215295b92d9da4a9cfbe28927`. Post-merge push `foundation-integrity #331` / run `32291764730` passed on that exact merge SHA. Post-merge push `s1-contracts #118` / run `32291764814` passed 3/3 jobs on the same exact merge SHA: Linux and macOS secondary evidence plus Windows adversarial qualification, pinned-source Tauri CLI build, NSIS build/install, packaged launch/missing/mismatch exercises, and cleanup. `WINDOWS_PREEXEC_BINARY_IDENTITY_ATTESTATION=NOT_IMPLEMENTED_NOT_CLAIMED`; no S3 containment claim is inferred.

## S1-013 — Performance and evidence packet

- [x] Measure cold Core spawn + handshake.
- [x] Measure health request p50/p95/p99.
- [x] Measure bounded small-request throughput.
- [x] Measure idle Desktop/Core memory and idle CPU.
- [x] Measure cancellation latency.
- [x] Measure crash detection + fresh-handshake recovery.
- [x] Measure malformed/oversized-payload rejection cost.
- [x] Measure sustained diagnostic-drain behavior and retained-diagnostics truncation.
- [x] Tighten initial budgets where evidence supports a lower bound.
- [x] Record exact Desktop/Core binaries, toolchain, lockfile, protocol version, commit and platform identities.

Evidence: PR #179 merged as `96fa229610f31598326493b75b40a3353b46bbbf`. Post-merge push `foundation-integrity #700` / run `32955349075` passed, `s1-contracts #162` / run `32955348827` passed 3/3 jobs, and `s1-performance #5` / run `32955348872` passed on that exact merge SHA. The durable measurement reconciliation is `s1-013-performance-evidence.md`. No uploaded Actions artifact exists for the performance run; exact run logs/summary retain the measured values. Measurement did not prove a safe lower bound for any existing safety limit, so no limit was lowered merely because latency/throughput measurements were favorable.

## S1-014 — Security and independent correctness review

- [x] Run exact-range Codex Security diff scan when available and egress policy permits; otherwise record canonical non-PASS status/coverage limitation.
- [x] Obtain at least one independently qualified correctness/engineering review on exact S1 acceptance candidate.
- [x] Account every named reviewer surface actually used/unavailable without implying PASS.
- [x] Normalize findings; do not vote them away.

Evidence: `s1-014-review-evidence.md` binds the complete S1 review range to acceptance candidate `58ad0d166b6177ae69d04ff59da17aa8cc0e3c28`, records `CODEX_SECURITY_STATUS=NOT_RUN_NON_BLOCKING` / `SECURITY_PASS=NO`, records Qodo Deep review comment `5434723966`, and normalizes all four reported findings. One finding is valid and material, so S1-015 is required.

## S1-015 — Finding reconciliation / bounded repair / rerun

- [x] Validate each finding against exact current code.
- [x] Repair only valid findings within bounded scope.
- [x] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [x] Zero unresolved material findings.
- [x] Zero stale-evidence inheritance across changed heads.

Evidence: PR #197 repaired exactly `F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE` at head `1229bdd9a411c70cce5494185c1f6c7814fa2085` and merged as `9ae784106f36c2234e3cdf6befdb03449a224c34`. Exact-head Foundation #737, authoritative admission #576, performance #7, and Qodo review comment `5438445407` were clean for the repair; post-merge Foundation #738 and performance #8 passed on the canonical merge. Durable closeout evidence is `s1-015-repair-evidence.md`.

## S1-016 — Accept S1 and capture learning

- [x] Verify all S1 acceptance criteria on exact head.
- [x] Record standing-founder-authority S1 acceptance bound to that exact head.
- [x] Do not treat merge/deploy/reviewer output as completion authority.
- [x] Capture qualified positive mechanics and negative oracles in Build Learning.
- [x] Merge only after exact-head acceptance/evidence and repository merge rules are satisfied.
- [x] Do not begin S2 until S1 is accepted and merged or otherwise canonically closed.

Evidence: `acceptance.md` binds S1 acceptance to canonical execution head `9a826e14fa2dd213f656b0ea2fec1ff737eb56dd` after post-merge Foundation #744; `docs/learning/BUILD_LEARNING_LEDGER.md` promotes BL-0004 through BL-0009 in the same exact transition. This transition becomes canonical only after v18 exact-head qualification, independent review, guarded merge, and post-merge verification. S2 remains not started and not authorized by S1 acceptance.

## Current gate

```text
COMPLETED = S1-001 THROUGH S1-016
CURRENT = NONE
CANONICAL_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN
S1_015_REPAIR_CLOSEOUT = PROVEN
S1_016_ACCEPTANCE_CLOSEOUT = PROVEN
S1_ACCEPTED = YES
NEXT = S2
S2 = NOT_STARTED
S2_AUTHORITY = NOT_GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
```
