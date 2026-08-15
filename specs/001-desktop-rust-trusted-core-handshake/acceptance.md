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
- [x] Source Acquisition Check exists and currently blocks implementation.

## Source / dependency gate

- [ ] Stage-aware S1 integrity gate validated without weakening P0 invariants.
- [ ] Exact Rust toolchain pin admitted.
- [ ] Exact resolved Tauri/Tauri-build/Serde/serde_json graph admitted.
- [ ] `Cargo.lock` retained and bound to acceptance head.
- [ ] Direct/transitive feature inventory reconciled.
- [ ] SBOM retained.
- [ ] Advisory results reconciled with no unresolved reportable finding/coverage gap represented as PASS.
- [ ] `tauri-plugin-shell` absent, or separately requalified with explicit evidence if the initial stdlib approach was proven insufficient.
- [ ] Dependency register accurately represents the admitted S1 graph.
- [ ] `SOURCE_ACQUISITION_CHECK = PASS` on the implementation-authorizing head.

## Protocol / correctness

- [ ] Desktop and Core are separate OS processes.
- [ ] Runtime channel is local-only and opens no network listener.
- [ ] Protocol v1 is typed and versioned.
- [ ] Fixed-length frame prefix is bounded before allocation/deserialization.
- [ ] Unknown/malformed/oversized/version-mismatch/principal-mismatch inputs fail closed.
- [ ] No silent protocol downgrade.
- [ ] Health/version/capability round-trip works.
- [ ] Event delivery works under explicit bounds.
- [ ] Cancellation is correlated, idempotent where specified, and race-tested.
- [ ] Duplicate/replay/stale-launch semantics are deterministic.
- [ ] Backpressure/in-flight/watch/recent-ID bounds are enforced.
- [ ] Core crash/EOF immediately invalidates ready state.
- [ ] Restart negotiates a fresh launch identity and does not fabricate prior completion.

## Authority / security

- [ ] WebView cannot mint/select Core principal authority.
- [ ] Tauri ACL/capability/connectivity is not consumed as Nawat authority.
- [ ] S1 WebView has no generalized shell/filesystem/network permission.
- [ ] Core has no project/filesystem/terminal/worker/network effect in S1.
- [ ] Explicit packaged Core path is used; shell/PATH lookup is absent.
- [ ] Exact Desktop/Core binary and protocol identities are captured.
- [ ] Applicable security review is completed/accounted under canonical policy.
- [ ] No unresolved material security finding or coverage limitation is mislabeled PASS.

## Platform / recovery

- [ ] Windows x86_64 MSVC clean-checkout build succeeds.
- [ ] Windows packaged Desktop launches the intended Core sibling.
- [ ] Windows round-trip/event/cancel/adversarial suite succeeds.
- [ ] Windows crash/restart/exit/orphan observations are recorded honestly.
- [ ] Linux compile + protocol/contract suite succeeds.
- [ ] macOS compile + protocol/contract suite succeeds when runner availability permits, or exact limitation is recorded.
- [ ] S1 makes no hostile-worker containment or S3 process-ownership claim without matching evidence.

## Performance / user-visible quality

- [ ] Cold spawn + handshake measurement retained.
- [ ] Request latency distribution retained.
- [ ] Throughput/backpressure measurement retained.
- [ ] Idle memory/CPU retained.
- [ ] Cancellation and recovery latency retained.
- [ ] Initial safety budgets tightened where evidence supports it.
- [ ] Minimal UI accurately exposes ready/degraded/restarting/unavailable state.
- [ ] Minimal user-facing UI meets applicable keyboard/focus/status accessibility baseline.

## Review / completion

- [ ] Deterministic gates PASS on exact candidate head.
- [ ] At least one qualified independent correctness/engineering review completed on exact candidate head.
- [ ] All valid findings reconciled.
- [ ] A changed repair head reran affected gates/reviews; no stale PASS inherited.
- [ ] Build Learning capture completed.
- [ ] S1 acceptance record bound to exact accepted head.

## Current verdict

```text
S1_ACCEPTED = NO
PLANNING = READY_FOR_DRAFT_PR
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
```
