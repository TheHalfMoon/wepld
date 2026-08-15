# Tasks — S1 Desktop ↔ Rust Trusted Core Handshake

This is the execution-authoritative S1 task ledger. A checked box requires stable evidence; a task description never grants authority beyond its own gate.

```text
SLICE = S1
BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
BRANCH = feat/s1-desktop-rust-core-handshake
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

Evidence: this initial S1 planning commit and `specs/001-desktop-rust-trusted-core-handshake/**`.

## S1-002 — Publish live S1 checkpoint

- [ ] Open Draft PR against `main` from the S1 branch.
- [ ] Update `docs/canonical/CURRENT_STATE.md` with exact PR number/head and P0 merged identity.
- [ ] Verify planning-only `foundation-integrity` on the exact checkpoint head.

Gate: no implementation/dependency manifest may enter during this task.

## S1-003 — Migrate P0 foundation CI to stage-aware S1 integrity

- [ ] Preserve immutable P0 archive/V2.2/402-registry validation.
- [ ] Preserve symlink/gitlink/repair-payload/duplicate-policy protections.
- [ ] Replace the P0-only implementation prohibition with an explicit S1 phase/path/admission contract.
- [ ] Ensure later-slice implementation paths remain rejected.
- [ ] Add deterministic negative fixtures/probes proving unauthorized manifests/code still fail.
- [ ] Keep hosted reviewer auto-trigger disabled.
- [ ] Run exact-head deterministic workflow tests.
- [ ] Run/apply security review because CI trust boundary changes.
- [ ] Reconcile all valid findings before S1-004.

Gate: S1-004 blocked until the stage-aware gate is independently validated.

## S1-004 — Resolve candidate dependency graph without product behavior

- [ ] Add exact Rust toolchain pin.
- [ ] Add minimum candidate Cargo workspace/manifests only.
- [ ] Candidate direct deps: Tauri 2.11.5, Tauri-build 2.6.3, Serde 1.0.229, serde_json 1.0.151 as justified by ownership.
- [ ] Keep `tauri-plugin-shell` absent.
- [ ] Keep direct Tokio/Core async framework absent unless a fresh evidence-backed need is accepted.
- [ ] Generate `Cargo.lock`.
- [ ] Capture direct/transitive feature tree.
- [ ] Generate SBOM.
- [ ] Run advisory/security dependency scan.
- [ ] No product behavior/source implementation beyond manifest/build skeleton required for resolution.

Status semantics:

```text
DEPENDENCY_RESOLUTION_AUTHORIZED = YES_AFTER_S1_003
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
- [ ] Implement 4-byte big-endian length framing.
- [ ] Reject frames above the accepted bound before payload allocation/deserialization.
- [ ] Strictly reject unknown versions/kinds/principals/operations and malformed required data.
- [ ] Add golden fixtures and unit/property/negative tests.
- [ ] No process, filesystem, network, UI, or project effects.

## S1-007 — Implement pure handshake / replay / cancellation state

- [ ] Implement launch/request correlation semantics.
- [ ] Implement bounded recent-ID replay window.
- [ ] Implement bounded in-flight/watch state.
- [ ] Implement health/version/capability operations.
- [ ] Implement bounded health-observation state and idempotent cancellation.
- [ ] Prove stale launch IDs, duplicate IDs, cancellation races, and budget exhaustion fail deterministically.
- [ ] Keep logic testable without Tauri or OS child processes.

## S1-008 — Implement separate Rust Core child process

- [ ] Core executable reads/writes only inherited stdin/stdout/stderr for S1 protocol.
- [ ] Use stdlib process/IO/concurrency primitives unless a separately qualified need changes this.
- [ ] No network listener/client.
- [ ] No project/filesystem/terminal/worker authority.
- [ ] EOF/broken input terminates or degrades predictably.
- [ ] Malformed/oversized protocol data cannot fabricate success.
- [ ] Add Core process integration tests.

## S1-009 — Implement Desktop-owned Core lifecycle and protocol client

- [ ] Resolve explicit packaged sibling Core executable path; no shell/PATH lookup.
- [ ] Launch separate Core child with piped stdin/stdout/stderr.
- [ ] Assign `desktop_host` principal and fresh launch ID internally.
- [ ] Implement typed request/event/cancel client.
- [ ] EOF/child exit immediately invalidates readiness.
- [ ] Restart uses a new launch ID and invalidates prior in-flight operations.
- [ ] Bound restart/retry behavior; no infinite silent restart loop.
- [ ] Record observed orphan/cleanup behavior without claiming S3 containment.

## S1-010 — Implement minimal Tauri shell and static presentation

- [ ] Minimal Tauri Desktop application only.
- [ ] Bundle Core using the minimum qualified Tauri external-binary mechanism.
- [ ] Expose only narrow typed status/control projection needed by S1 UI.
- [ ] No general shell/filesystem/network permission to WebView.
- [ ] Static local UI shows Core readiness/health/version/capabilities and cancellable observation state.
- [ ] Keyboard/focus/status semantics satisfy the applicable accessibility baseline for this minimal UI.
- [ ] No React/Vite/Tailwind/frontend package manager unless a new measured need is qualified.

## S1-011 — Cross-process failure/adversarial suite

- [ ] Valid request/response round-trip.
- [ ] Event delivery and cancellation.
- [ ] Unknown command/version/principal and downgrade attempt.
- [ ] zero/oversized/truncated/malformed frames.
- [ ] invalid UTF-8/text contract cases.
- [ ] duplicate/replay/stale launch.
- [ ] cancellation of unknown/completed/already-cancelled request and cancellation race.
- [ ] in-flight/watch/recent-ID budget exhaustion.
- [ ] Core unavailable/crash/restart.
- [ ] Desktop writer/reader loss and Desktop exit.
- [ ] stale response/event after restart.
- [ ] wrong/missing/mismatched Core binary/package scenario.

## S1-012 — Windows-first qualification and secondary platform evidence

- [ ] Windows x86_64 MSVC build from clean checkout.
- [ ] Windows Desktop launches intended packaged Core sibling.
- [ ] Windows typed round-trip/event/cancel/failure suite passes.
- [ ] Windows Core crash/restart and Desktop-exit child behavior recorded.
- [ ] Windows packaging path/version mismatch cases exercised.
- [ ] Linux compile + protocol/contract tests.
- [ ] macOS compile + protocol/contract tests when CI runner availability permits; otherwise record exact coverage limitation.
- [ ] No compile-only result is reported as runtime containment/process-ownership proof.

## S1-013 — Performance and evidence packet

- [ ] Measure cold Core spawn + handshake.
- [ ] Measure health request p50/p95/p99.
- [ ] Measure bounded small-request throughput.
- [ ] Measure idle Desktop/Core memory and idle CPU.
- [ ] Measure cancellation latency.
- [ ] Measure crash detection + fresh-handshake recovery.
- [ ] Measure malformed/oversized rejection cost.
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
- [ ] Rerun all affected deterministic/platform/security/review gates on the resulting exact head.
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
COMPLETED = S1-001 PLANNING CONTENT PREPARED
NEXT = ATOMIC PLANNING COMMIT -> DRAFT PR -> S1-002
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
```
