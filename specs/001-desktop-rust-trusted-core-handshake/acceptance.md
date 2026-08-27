# Acceptance — S1 Desktop ↔ Rust Trusted Core Handshake

S1 acceptance is exact-head evidence, not a checkbox ritual. Historical gates/reviews remain historical after a changed head.

## Planning / authority

- [x] P0 foundation was founder-accepted and merged before S1 branch creation.
- [x] S1 branch starts from canonical `main` merge commit `6eff72319cad99c878a80f0d5bce9f107d213679`.
- [x] Founder standing authorization permits governed S1 execution without repeated approval requests.
- [x] V2.2 master plan hash is `e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44`.
- [x] Spec Kit planning sequence reconciles upstream order drift explicitly.
- [x] Ponytail FULL completed for planning.
- [x] Threat/authority model exists.
- [x] Source Acquisition Check exists and is PASS for the admitted S1 graph.

Evidence: S1-001/S1-002 planning records and the execution-authoritative `tasks.md` checkpoint. S1-005 established `SOURCE_ACQUISITION_CHECK = PASS` before product implementation.

## Source / dependency gate

- [x] Stage-aware S1 integrity gate validated without weakening P0 invariants.
- [x] Exact Rust toolchain pin admitted.
- [x] Exact resolved Tauri/Tauri-build/Serde/serde_json graph admitted.
- [x] `Cargo.lock` retained and bound to acceptance head.
- [x] Direct/transitive feature inventory reconciled.
- [x] SBOM retained.
- [x] Advisory results reconciled with no unresolved reportable finding/coverage gap represented as PASS.
- [x] `tauri-plugin-shell` absent, or separately requalified with explicit evidence if the initial stdlib approach was proven insufficient.
- [x] Dependency register accurately represents the admitted S1 graph.
- [x] `SOURCE_ACQUISITION_CHECK = PASS` on the implementation-authorizing head.

Evidence: S1-003 through S1-005 in `tasks.md`; PR #7 dependency-resolution evidence and PR #11 component-admission evidence. The admitted direct graph remains Tauri 2.11.5, Tauri-build 2.6.3, Serde 1.0.229, and serde_json 1.0.151 with `tauri-plugin-shell` absent.

## Protocol / correctness

- [x] Desktop and Core are separate OS processes.
- [x] Runtime channel is local-only and opens no network listener.
- [x] Protocol v1 is typed and versioned.
- [x] Fixed-length frame prefix is bounded before allocation/deserialization.
- [x] Unknown/malformed/oversized/version-mismatch/principal-mismatch inputs fail closed.
- [x] No silent protocol downgrade.
- [x] Health/version/capability round-trip works.
- [x] Event delivery works under explicit bounds.
- [x] Cancellation is correlated, idempotent where specified, and race-tested.
- [x] Duplicate/replay/stale-launch semantics are deterministic.
- [x] Backpressure/in-flight/watch bounds and the launch-wide monotonic command-ID high-water invariant are enforced.
- [x] Core crash/EOF immediately invalidates ready state.
- [x] Restart negotiates a fresh launch identity and does not fabricate prior completion.

Evidence: S1-006 through S1-011 in `tasks.md`; canonical merges for protocol contracts, state machine, Core process, Desktop lifecycle, minimal shell, and the adversarial suite. The S1-011 suite covers replay, stale launch, cancellation races, framing boundaries, crash/restart, diagnostics pressure, and packaged-binary mismatch cases.

## Authority / security

- [x] WebView cannot mint/select Core principal authority.
- [x] Tauri ACL/capability/connectivity is not consumed as Nawat authority.
- [x] S1 WebView has no generalized shell/filesystem/network permission.
- [x] Core has no project/filesystem/terminal/worker/network effect in S1.
- [x] Explicit packaged Core path is used; shell/PATH lookup is absent.
- [x] Exact Desktop/Core binary and protocol identities are captured.
- [x] Applicable security review is completed/accounted under canonical policy.
- [x] No unresolved material security finding or coverage limitation is mislabeled PASS.

Evidence: S1-008 through S1-014 plus `s1-014-review-evidence.md`. Codex Security remained unavailable for the applicable S1 review range and is retained as `NOT_RUN_NON_BLOCKING`; `SECURITY_PASS = NO`. This coverage limitation is explicit and is not substituted by Qodo or any other reviewer.

## Platform / recovery

- [x] Windows x86_64 MSVC clean-checkout build succeeds.
- [x] Windows packaged Desktop launches the intended Core sibling.
- [x] Windows round-trip/event/cancel/adversarial suite succeeds.
- [x] Windows crash/restart/exit/orphan observations are recorded honestly.
- [x] Linux compile + protocol/contract suite succeeds.
- [x] macOS compile + protocol/contract suite succeeds when runner availability permits, or exact limitation is recorded.
- [x] S1 makes no hostile-worker containment or S3 process-ownership claim without matching evidence.

Evidence: S1-012 in `tasks.md`, PR #37 merge `848566d89e5995e215295b92d9da4a9cfbe28927`, post-merge Foundation run `32291764730` / #331, and post-merge contracts run `32291764814` / #118 with Linux, macOS, and Windows jobs. `WINDOWS_PREEXEC_BINARY_IDENTITY_ATTESTATION=NOT_IMPLEMENTED_NOT_CLAIMED` remains a recorded limitation and no S3 containment claim is inferred.

## Performance / user-visible quality

- [x] Cold spawn + handshake measurement retained.
- [x] Request latency distribution retained.
- [x] Throughput/backpressure measurement retained.
- [x] Idle memory/CPU retained.
- [x] Cancellation and recovery latency retained.
- [x] Initial safety budgets tightened where evidence supports it.
- [x] Minimal UI accurately exposes ready/degraded/restarting/unavailable state.
- [x] Minimal user-facing UI meets applicable keyboard/focus/status accessibility baseline.

Evidence: S1-010 and S1-013 in `tasks.md`, `s1-013-performance-evidence.md`, PR #179 merge `96fa229610f31598326493b75b40a3353b46bbbf`, and post-merge performance run `32955348872` / #5. Measurement did not prove a safe lower bound for existing safety limits, so no limit was reduced merely because measurements were favorable.

## Review / completion

- [x] Deterministic gates PASS on exact candidate head.
- [x] At least one qualified independent correctness/engineering review completed on exact candidate head.
- [x] All valid findings reconciled.
- [x] A changed repair head reran affected gates/reviews; no stale PASS inherited.
- [x] Build Learning capture completed.
- [x] S1 acceptance record bound to exact accepted head.

Evidence composition:
- the complete S1 implementation range received Qodo Deep review at S1-014;
- the one valid material finding was repaired by PR #197 at exact head `1229bdd9a411c70cce5494185c1f6c7814fa2085`;
- that repair head passed Foundation, trusted-base admission, performance, and Qodo review;
- PR #197 merged as `9ae784106f36c2234e3cdf6befdb03449a224c34`, whose post-merge Foundation #738 and performance #8 passed;
- the exact S1-015 closeout merge `9a826e14fa2dd213f656b0ea2fec1ff737eb56dd` passed post-merge Foundation run `33083905553` / #744;
- no product/runtime/dependency source changed after the reviewed repair merge; later changes were bounded policy/evidence/ledger transitions governed by v17 and its exact-delta admission path;
- Build Learning rows `BL-0004` through `BL-0009` are proposed as `QUALIFIED` in the same S1-016 acceptance transition and become canonical only after this exact transition receives applicable independent review and founder-authorized merge.

## S1-016 acceptance record

```text
S1_ACCEPTANCE_RECORD = EXACT_S1_016_RECONCILIATION
DATE = 2026-08-27
ACCEPTED_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
ACCEPTED_EXECUTION_TREE = c63bea084edd9cc1f3fcfe5f574518339f510426
S1_015_CLOSEOUT_PR = #199
S1_015_CLOSEOUT_MERGE = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd
S1_015_CLOSEOUT_POST_MERGE_FOUNDATION = 33083905553 / #744 / SUCCESS
S1_014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1_014_SECURITY_PASS = NO
S1_015_UNRESOLVED_MATERIAL_FINDINGS = 0
S1_BUILD_LEARNING_ROWS = BL-0004..BL-0009
S1_BUILD_LEARNING_PROPOSED_STATUS = QUALIFIED
S1_ACCEPTANCE_AUTHORITY = FOUNDER_STANDING_AUTHORIZATION
S2_AUTHORITY = NOT_GRANTED_BY_S1_ACCEPTANCE
```

The accepted execution head is the exact canonical S1-015 closeout head. Review and performance evidence is composed only across explicitly unchanged or separately requalified scopes; no changed material source inherits stale PASS. The S1-016 acceptance transition itself remains subject to exact-head deterministic qualification, independent review, guarded merge, and post-merge canonical verification before `S1_ACCEPTED = YES` is canonical.

## Current verdict

```text
S1_ACCEPTED = YES
PLANNING = CLOSED_CANONICAL
SOURCE_ACQUISITION_CHECK = PASS
DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
PLATFORM_QUALIFICATION = S1_012_PROVEN
PERFORMANCE_EVIDENCE = S1_013_PROVEN
REVIEW_RECONCILIATION = S1_014_AND_S1_015_PROVEN
CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
SECURITY_PASS = NO
BUILD_LEARNING_CAPTURE = BL-0004_THROUGH_BL-0009_QUALIFIED_ON_CANONICAL_MERGE
S2_AUTHORITY = NOT_GRANTED
```
