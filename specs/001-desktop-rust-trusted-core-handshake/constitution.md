# Constitution — S1 Desktop ↔ Rust Trusted Core Handshake

## Authority

1. The ratified V2.2 architecture remains controlling authority for S1.
2. Founder standing authorization permits S1 execution without repeated approval requests, but it does not waive qualification, evidence, review, security, or Trusted Completion gates.
3. `ReviewOutcome != CompletionDecision` and `Green CI != Completion` remain non-bypassable.
4. Connection to the Rust Core never grants filesystem, process, network, repository, source-admission, or completion authority.
5. The Desktop/WebView is untrusted presentation and transport. The Rust Core owns protocol validation and trusted handshake state.

## Scope

S1 establishes one typed, versioned, observable local request/response/event channel between a Tauri desktop process and a separate Rust Core process.

S1 includes only the minimum machinery required to prove:

- Core launch and liveness;
- protocol/version negotiation;
- health, version, and capability reporting;
- bounded typed request/response/event framing;
- correlation and replay/duplicate handling;
- cancellation semantics;
- malformed/oversized/unauthorized input denial;
- crash/restart/reconnect behavior without false authority;
- exact-binary/protocol evidence;
- Windows-first qualification plus cross-platform compile/contract evidence.

S1 does not implement project opening, terminal execution, AI workers, Fehrest, native review, repair, Trusted Completion, cloud control, or generalized plugin transport.

## Transport and protocol principles

1. `LOCAL_ONLY` is mandatory.
2. No TCP listener, localhost HTTP server, named service, or hosted control plane is justified for the base S1 handshake.
3. The preferred minimum transport is inherited child-process stdin/stdout, subject to Source Acquisition qualification and platform tests.
4. The protocol is WePLD-owned; framework transport or ACL semantics never become Nawat authority.
5. Frames are length-bounded before payload allocation/deserialization.
6. Protocol downgrade is never silent.
7. Unknown command/version/kind/principal data fails closed.
8. Missing, malformed, stale, duplicate, replayed, or over-budget evidence never becomes success.

## Reuse

Acquire solved machinery before writing equivalents. Runtime dependencies, build tooling, and donor code remain candidates until their exact S1 acquisition records satisfy the canonical source-acquisition gate. Broad source import is prohibited.

## Evidence

Every completion claim must bind to the exact S1 head, lockfile/toolchain identity, protocol version, test set, platform result, reviewer result, and acceptance record. A changed head invalidates stale exact-head conclusions where required by policy.
