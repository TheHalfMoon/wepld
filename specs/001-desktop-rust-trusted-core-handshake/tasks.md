# Tasks — S1 Desktop ↔ Rust Trusted Core Handshake

This is the execution-authoritative S1 task ledger. A checked box requires stable evidence; a task description never grants authority beyond its own gate.

```text
SLICE = S1
S1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
CANONICAL_EXECUTION_HEAD = 96fa229610f31598326493b75b40a3353b46bbbf
LEDGER_RECONCILIATION_BASE = 96fa229610f31598326493b75b40a3353b46bbbf
LIVE_MAIN = MUST_BE_READ_FROM_GITHUB
ACTIVE_TASK = NONE
NEXT_TASK = S1-014_NOT_STARTED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER
S1_014_PLUS = NOT_STARTED
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

- [ ] Run exact-range Codex Security diff scan when available and egress policy permits; otherwise record canonical non-PASS status/coverage limitation.
- [ ] Obtain at least one independently qualified correctness/engineering review on exact S1 acceptance candidate.
- [ ] Account every named reviewer surface actually used/unavailable without implying PASS.
- [ ] Normalize findings; do not vote them away.

## S1-015 — Finding reconciliation / bounded repair / rerun

- [ ] Validate each finding against exact current code.
- [ ] Repair only valid findings within bounded scope.
- [ ] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [ ] Zero unresolved material findings.
- [ ] Zero stale-evidence inheritance across changed heads.

## S1-016 — Accept S1 and capture learning

- [ ] Verify all S1 acceptance criteria on exact head.
- [ ] Record standing-founder-authority S1 acceptance bound to that exact head.
- [ ] Do not treat merge/deploy/reviewer output as completion authority.
- [ ] Capture qualified positive mechanics and negative oracles in Build Learning.
- [ ] Merge only after exact-head acceptance/evidence and repository merge rules are satisfied.
- [ ] Do not begin S2 until S1 is accepted and merged or otherwise canonically closed.

## Current gate

```text
COMPLETED = S1-001 THROUGH S1-013
CURRENT = NONE
CANONICAL_EXECUTION_HEAD = 96fa229610f31598326493b75b40a3353b46bbbf
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
NEXT = S1-014
S1_014_PLUS = NOT_STARTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
```
