# Tasks — S1 Desktop ↔ Rust Trusted Core Handshake

This is the execution-authoritative S1 task ledger. A checked box requires stable evidence; a task description never grants authority beyond its own gate.

```text
SLICE = S1
S1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
CURRENT_CANONICAL_MAIN = 12fd72c19d639b4b72a8dec8dba644282383d0db
ACTIVE_TASK = S1-003
ACTIVE_BRANCH = ci/s1-stage-aware-foundation-integrity
ACTIVE_PR = #4
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
```

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

Active PR: #4.

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

### Still required before PR #4 can merge

- [ ] Re-run `foundation-integrity` on the exact head after canonical-memory/task checkpoint.
- [ ] Inspect deterministic job steps and preserve exact run ID.
- [ ] Record exact-head Codex Security status; if unavailable, `NOT_RUN_NON_BLOCKING`, never PASS.
- [ ] Perform exact-head public-source secret-marker screening before any hosted reviewer.
- [ ] Obtain at least one independently qualified exact-head correctness/engineering review. Cubic is currently ineligible.
- [ ] Validate every finding against current code/policy.
- [ ] Repair only valid findings.
- [ ] Rerun every affected gate/review after repair.
- [ ] Zero unresolved material findings.
- [ ] Merge PR #4 only as the reviewed S1-003 policy migration, not as S1 acceptance.

### Post-merge S1-003 activation proof

PR #4 cannot exercise `s1-admission-integrity` authoritatively because the workflow is not present in its base commit.

- [ ] Verify post-merge canonical-main `foundation-integrity`.
- [ ] Create a docs-only activation-canary PR from the post-merge main.
- [ ] Prove `s1-admission-integrity` runs from the base policy.
- [ ] Prove the authoritative path reads candidate Git objects as data only and reports `S1_PLANNING_ONLY`.
- [ ] Confirm no candidate checkout/build/script execution occurs in that privileged path.
- [ ] Close/merge the canary only according to its narrow evidence purpose.
- [ ] Set `S1_003_ACTIVATION_PROVEN = YES` only after canary evidence is exact and complete.

Gate: **S1-004 manifests are prohibited until the post-merge activation canary passes.**

## S1-004 — Resolve candidate dependency graph without product behavior

- [ ] Start only after `S1_003_ACTIVATION_PROVEN = YES`.
- [ ] Add the exact Rust toolchain candidate required by S1-003 policy.
- [ ] Add the exact minimum Cargo workspace/manifests/skeletons allowed by S1-003 Stage B1.
- [ ] Candidate direct deps: Tauri 2.11.5, Tauri-build 2.6.3, Serde 1.0.229, serde_json 1.0.151.
- [ ] Keep `tauri-plugin-shell` absent.
- [ ] Keep direct Tokio/Core async framework absent.
- [ ] Pass authoritative `s1-admission-integrity` in `S1_DEPENDENCY_RESOLUTION_INPUT`.
- [ ] Generate `Cargo.lock`.
- [ ] Pass authoritative `s1-admission-integrity` in `S1_DEPENDENCY_RESOLUTION_LOCKED`.
- [ ] Capture direct/transitive feature tree.
- [ ] Generate SBOM.
- [ ] Run advisory/security dependency scan.
- [ ] No product behavior beyond exact manifest/toolchain/target skeleton required for resolution.

Status semantics:

```text
DEPENDENCY_RESOLUTION_AUTHORIZED = YES_ONLY_AFTER_S1_003_ACTIVATION_CANARY
RUNTIME_DEPENDENCY_ADMITTED = NO_UNTIL_S1_005
```

## S1-005 — Finalize component admission / Source Acquisition Check

- [ ] Reconcile exact resolved versions and features against intended candidates.
- [ ] Reconcile every reportable advisory or coverage limitation.
- [ ] Prove no unnecessary direct dependency remains.
- [ ] Record Tauri capability surface and package/sidecar strategy.
- [ ] Record replacement/exit strategy per admitted component.
- [ ] Update `docs/governance/DEPENDENCY_REGISTER.md` for the exact S1 graph.
- [ ] Add immutable S1 component-admission evidence.
- [ ] Set `SOURCE_ACQUISITION_CHECK = PASS` only if all required evidence is complete.

Gate: **S1 product implementation is prohibited until this task passes.**

## S1-006 — Implement protocol v1 contracts and bounded frame codec

- [ ] Create typed protocol request/response/event/cancel/error enums/structs.
- [ ] Freeze protocol v1 constants and capability schema.
- [ ] Freeze one framing-size contract: `LENGTH_PREFIX_BYTES = 4`, `MAX_PAYLOAD_BYTES = 65_536`, `MAX_WIRE_FRAME_BYTES = 65_540`.
- [ ] Implement 4-byte big-endian payload-length framing.
- [ ] Read/validate the prefix before payload allocation/read/deserialization; reject declared payload length `> 65_536`.
- [ ] Prove declared payload length exactly `65_536` is within bound and `65_537` is rejected before payload allocation/read/deserialization.
- [ ] Strictly reject unknown versions/kinds/principals/operations and malformed required data.
- [ ] Add golden fixtures and unit/property/negative tests.
- [ ] No process, filesystem, network, UI, or project effects.

## S1-007 — Implement pure handshake / replay / cancellation state

- [ ] Implement launch/request correlation semantics.
- [ ] Implement serialized strictly increasing inbound command IDs per launch and an O(1) Core high-water mark; IDs never wrap/reuse within a launch.
- [ ] Reject every command with `id <= highest_accepted_command_id` before dispatch.
- [ ] Implement bounded in-flight/watch state.
- [ ] Implement health/version/capability operations.
- [ ] Implement bounded health-observation state and deterministic cancellation.
- [ ] Prove duplicate observation cannot allocate a second watch/event stream.
- [ ] Prove replayed cancellation cannot mutate state again and fresh cancellation of an already terminal operation is deterministic/non-mutating.
- [ ] Prove stale launch IDs, non-monotonic/reused IDs, cancellation races, and budget exhaustion fail deterministically.
- [ ] Keep logic testable without Tauri or OS child processes.

## S1-008 — Implement separate Rust Core child process

- [ ] Core protocol bytes use inherited stdin/stdout only.
- [ ] Core stderr is diagnostics-only and is never parsed as protocol data.
- [ ] Use stdlib process/IO/concurrency primitives unless a separately qualified need changes this.
- [ ] No network listener/client for the S1 Desktop ↔ Core handshake.
- [ ] No project/filesystem/terminal/worker authority.
- [ ] EOF/broken input terminates or degrades predictably.
- [ ] Malformed/oversized protocol data cannot fabricate success.
- [ ] Add Core process integration tests.

## S1-009 — Implement Desktop-owned Core lifecycle and protocol client

- [ ] Resolve explicit packaged sibling Core executable path; no shell/PATH lookup.
- [ ] Launch separate Core child with piped stdin/stdout and an explicit stderr strategy.
- [ ] If stderr is piped, drain it concurrently with bounded retained diagnostics and observable truncation.
- [ ] Assign `desktop_host` principal and fresh launch ID internally.
- [ ] Allocate request/cancel command IDs in the same serialized order frames are written to Core.
- [ ] Implement typed request/event/cancel client.
- [ ] EOF/child exit immediately invalidates readiness.
- [ ] Restart uses a new launch ID and invalidates prior in-flight operations.
- [ ] Bound restart/retry behavior; no infinite silent restart loop.
- [ ] Record observed orphan/cleanup behavior without claiming S3 containment.

## S1-010 — Implement minimal Tauri shell and static presentation

- [ ] Minimal Tauri Desktop application only.
- [ ] Bundle Core using the minimum qualified Tauri external-binary mechanism.
- [ ] Expose only narrow typed status/control projection needed by S1 UI.
- [ ] No general shell/filesystem/network permission to WebView merely for the S1 handshake.
- [ ] Static local UI shows Core readiness/health/version/capabilities and cancellable observation state.
- [ ] Keyboard/focus/status semantics satisfy the applicable accessibility baseline.
- [ ] No React/Vite/Tailwind/frontend package manager unless a new measured need is qualified.

## S1-011 — Cross-process failure/adversarial suite

- [ ] Valid request/response round-trip.
- [ ] Event delivery and cancellation.
- [ ] Unknown command/version/principal and downgrade attempt.
- [ ] Zero-length payload and malformed/truncated framing.
- [ ] Declared payload length `65_536` is within bound; `65_537` is rejected before payload allocation/read/deserialization.
- [ ] Invalid UTF-8/text contract cases.
- [ ] Duplicate/replay/non-monotonic command IDs and stale launch.
- [ ] Replay after terminal/cache eviction remains rejected by launch-wide high-water state.
- [ ] Duplicate observation cannot allocate a second watch/event stream.
- [ ] Replayed cancellation cannot mutate twice; fresh cancel of terminal target is deterministic/non-mutating.
- [ ] Cancellation of unknown/completed/already-cancelled request and cancellation race.
- [ ] In-flight/watch budget exhaustion.
- [ ] Core unavailable/crash/restart.
- [ ] Desktop writer/reader loss and Desktop exit.
- [ ] Stale response/event after restart.
- [ ] Wrong/missing/mismatched Core binary/package scenario.
- [ ] Emit diagnostics beyond expected OS stderr pipe capacity while protocol exchanges continue.

## S1-012 — Windows-first qualification and secondary platform evidence

- [ ] Windows x86_64 MSVC build from clean checkout.
- [ ] Windows Desktop launches intended packaged Core sibling.
- [ ] Windows typed round-trip/event/cancel/failure suite passes.
- [ ] Windows Core crash/restart and Desktop-exit child behavior recorded.
- [ ] Windows packaging path/version mismatch cases exercised.
- [ ] Linux compile + protocol/contract tests.
- [ ] macOS compile + protocol/contract tests when runner availability permits; otherwise record exact coverage limitation.
- [ ] No compile-only result is reported as runtime containment/process-ownership proof.

## S1-013 — Performance and evidence packet

- [ ] Measure cold Core spawn + handshake.
- [ ] Measure health request p50/p95/p99.
- [ ] Measure bounded small-request throughput.
- [ ] Measure idle Desktop/Core memory and idle CPU.
- [ ] Measure cancellation latency.
- [ ] Measure crash detection + fresh-handshake recovery.
- [ ] Measure malformed/oversized-payload rejection cost.
- [ ] Measure sustained diagnostic-drain behavior and retained-diagnostics truncation.
- [ ] Tighten initial budgets where evidence supports a lower bound.
- [ ] Record exact Desktop/Core binaries, toolchain, lockfile, protocol version, commit and platform identities.

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
COMPLETED = S1-001 + S1-002
CURRENT = S1-003 PR #4 EXACT-HEAD REVIEW / RECONCILIATION
LAST_POLICY_HEAD = 7bafe4b1f0e9cb6319526cfd957baf92ba6d7775
LAST_POLICY_HEAD_INTEGRITY = 31909208235 / #148 PASS
NEXT = CHECKPOINT HEAD -> EXACT CI -> SECURITY ACCOUNTING -> INDEPENDENT REVIEW
S1_004 = BLOCKED
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
```
