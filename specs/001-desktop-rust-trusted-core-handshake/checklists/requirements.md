# Requirements Checklist — S1 Desktop ↔ Rust Trusted Core Handshake

This checklist evaluates specification quality and execution readiness. Checked items require explicit support in the S1 artifacts; they do not mean implementation is complete.

## Architecture and authority

- [x] Separate Desktop and Core processes are mandatory.
- [x] Desktop/WebView is untrusted presentation/transport.
- [x] Core owns protocol validation and handshake state.
- [x] Connection/health/Tauri ACL/principal metadata do not grant Nawat authority.
- [x] S1 non-goals exclude project/filesystem/terminal/worker/cloud scope.
- [x] Founder standing authorization is distinguished from qualification evidence.

## Protocol

- [x] Protocol version is explicit.
- [x] Request/response/event/cancel/error semantics are distinct.
- [x] Framing has a pre-allocation size bound.
- [x] Unknown version/kind/principal/operation fails closed.
- [x] Silent downgrade is prohibited.
- [x] Correlation and launch identity are required.
- [x] Duplicate/replay behavior is deterministic.
- [x] Cancellation has explicit in-flight semantics.
- [x] Backpressure and retained-state budgets are explicit.
- [x] EOF/crash/restart invalidates ready state.

## Transport

- [x] Runtime network requirement is `NONE`.
- [x] Preferred minimum transport is inherited stdin/stdout.
- [x] TCP/localhost service is rejected for base S1.
- [x] Named pipes are fallback-only, not silently selected.
- [x] Tauri sidecar packaging is separated from protocol authority.

## Ponytail

- [x] Need for the separate process boundary is proven by V2.2.
- [x] No active implementation is inherited from the historical repository.
- [x] Stdlib primitives are evaluated before adding an IPC/RPC framework.
- [x] `tauri-plugin-shell` is rejected initially as unnecessary direct surface.
- [x] Async/RPC/UUID/frontend-framework/database/network dependencies are rejected unless a measured need reopens them.
- [x] Trust-boundary/security/recovery/evidence controls are explicitly non-reducible.

## Source acquisition

- [x] Tauri prior P0-A evidence is treated as historical and re-pinned.
- [x] Rust toolchain candidate is pinned to an exact release identity.
- [x] Tauri and Tauri-build candidate identities are pinned.
- [x] Serde and serde_json candidate identities are pinned.
- [x] Shell plugin reference identity is pinned despite initial rejection.
- [x] Methodology references for Spec Kit/Ponytail are pinned.
- [x] Dependency-resolution authorization is separated from runtime admission.
- [ ] Candidate lockfile resolved.
- [ ] Direct/transitive feature inventory recorded.
- [ ] SBOM generated.
- [ ] Advisory scan reconciled.
- [ ] Dependency register updated for the exact admitted graph.
- [ ] Final component admission record completed.

## CI and security

- [x] P0 `foundation-integrity` incompatibility with implementation is identified before code is added.
- [x] Stage-aware CI migration is planned instead of deleting P0 protections.
- [x] Workflow migration is classified security-relevant.
- [x] S1 requires exact-range Codex Security coverage when available/egress-permitted.
- [x] S1 requires independent correctness/engineering review.
- [x] Missing applicable security/reviewer coverage cannot become PASS.

## Platform

- [x] Windows x86_64 MSVC is primary runtime qualification target.
- [x] Linux/macOS secondary compile/contract evidence is planned.
- [x] Compile evidence is not misrepresented as runtime containment/behavior evidence.
- [x] Sidecar packaging and orphan/cleanup behavior are explicit Windows tests.

## Test corpus

- [x] Valid round-trip is covered.
- [x] Health/version/capability responses are covered.
- [x] Event delivery and cancellation are covered.
- [x] Unknown command/version/principal are covered.
- [x] Downgrade attack is covered.
- [x] Oversize/truncated/malformed frames are covered.
- [x] Duplicate/replay/stale-launch cases are covered.
- [x] Flood/budget exhaustion is covered.
- [x] Core unavailable/crash/restart is covered.
- [x] Desktop crash/pipe close is covered.

## Evidence and acceptance

- [x] Exact binary/protocol/toolchain/lock identities are required.
- [x] Performance measurements are required but not used as correctness substitutes.
- [x] Acceptance requires rerun after material repair/head change as applicable.
- [x] Build Learning capture is part of exit.
- [ ] Implementation exact-head deterministic gates complete.
- [ ] Security review complete/accounted.
- [ ] Independent engineering review complete.
- [ ] Findings reconciled.
- [ ] S1 acceptance recorded.

## Checklist verdict

```text
PLANNING_REQUIREMENTS = SUFFICIENT_TO_PROCEED_TO_ANALYSIS
SOURCE_ACQUISITION = OPEN
IMPLEMENTATION = BLOCKED
```
