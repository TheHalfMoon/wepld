# Clarifications — S1 Desktop ↔ Rust Trusted Core Handshake

All clarifications below are bounded S1 decisions. They do not reopen V2.2 architecture.

## C-001 — What is the base S1 transport?

**Decision:** inherited child-process stdin/stdout pipes are the preferred minimum transport.

**Reason:** S1 requires a separate Core process and `LOCAL_ONLY`, but it does not require a discoverable service endpoint. Inherited pipes remove TCP port selection, localhost exposure, named-pipe ACL design, stale socket cleanup, and remote-origin concerns from the minimum slice.

**Qualification:** this remains subject to Windows runtime/packaging tests. Failure of the child-pipe design to satisfy acceptance reopens transport selection only within S1; it does not authorize silent fallback.

## C-002 — Does Tauri IPC provide Core authority?

**Decision:** no.

Tauri is a desktop framework and may mediate WebView-to-Desktop-host presentation requests. Tauri ACL/capability state, successful invocation, process connectivity, and sidecar packaging never become Nawat authority or Trusted Core authorization.

## C-003 — Is `tauri-plugin-shell` required?

**Decision:** not for the initial S1 implementation candidate.

Tauri `externalBin` solves bundling of a sidecar binary. The Rust standard library can launch a known packaged sibling executable with piped stdin/stdout and an explicit stderr strategy. Installing the shell plugin would add a broader command/process package and additional transitive surface when S1 needs only one owned child executable.

`tauri-plugin-shell` remains a reference/negative oracle and a fallback candidate only if direct `std::process::Command` plus Tauri bundling fails measured packaging/recovery requirements. Any fallback requires a new explicit acquisition disposition; there is no silent substitution.

## C-004 — What framing is used?

**Decision:** 4-byte unsigned big-endian length prefix followed by one UTF-8 JSON payload.

**Reason:** the fixed prefix permits a hard allocation bound before deserialization and works over arbitrary byte-stream chunking. Newline-delimited JSON is rejected because a line parser does not itself give an equally direct pre-allocation length gate and creates escaping/framing ambiguity. A binary schema framework is premature for the small S1 contract.

Initial maximum payload: `65_536` bytes.

## C-005 — What serialization dependency is allowed conceptually?

**Decision:** Serde + serde_json are the preferred commodity serialization candidates. Hand-writing a JSON parser/serializer is rejected by Ponytail. Runtime admission remains pending the component acquisition gate and resolved lockfile/audit evidence.

## C-006 — How is principal identity represented?

**Decision:** S1 has exactly one protocol principal class: `desktop_host`.

The Desktop Rust host assigns it; arbitrary WebView input cannot select or manufacture another principal. Core rejects any other principal representation. This is boundary/correlation metadata, not a security grant.

## C-007 — How are launches and correlations identified?

**Decision:** each Desktop-managed Core launch has a monotonic Desktop-local `launch_id`. Within one launch, every new request/cancel command gets a `u64` message/request ID allocated in the same serialized writer order in which frames are placed on the single Desktop→Core byte stream. IDs MUST be strictly increasing on that stream and MUST NOT wrap or be reused within a launch. Responses/events echo the relevant launch/request identities. Stale launch identities fail closed.

The Core retains an O(1) launch-wide high-water mark for accepted command IDs. A new request/cancel frame with an ID less than or equal to that mark is a replay/duplicate and is rejected before dispatch. Response completion may occur out of order; only inbound command acceptance is monotonic in wire order. If the `u64` command-ID space were ever exhausted, the launch must terminate and a fresh launch/handshake is required rather than wrapping.

No cryptographic authenticity claim is made for these IDs. The inherited pipe relationship provides the minimum local origin constraint for S1; future authority-bearing operations require Nawat-owned grants and stronger evidence as applicable.

## C-008 — What proves event delivery and cancellation?

**Decision:** protocol v1 includes one bounded handshake-owned health observation operation that emits typed health events until completion or cancellation.

This exists to prove the event/cancellation contract with a real runtime path rather than a test-only fake command. It is not a generalized streaming or telemetry subsystem. Event interval, lifetime, and concurrent-watch count are bounded.

## C-009 — What happens on duplicate or replayed command IDs?

**Decision:** duplicate/replayed IDs are rejected deterministically before dispatch and never re-execute work. S1 does not rely on a bounded recent-ID cache for this security property. The launch-wide monotonic high-water mark from C-007 continues to reject every previously accepted ID even after any unrelated terminal-result/cache state has been discarded.

For the stateful S1 operations specifically:

- replaying the original health-observation command ID cannot allocate a second watch or emit a second event stream;
- a cancellation command has its own fresh monotonic command ID and names a target observation request ID;
- replaying the same cancellation command ID is rejected before state mutation;
- a different fresh cancellation command targeting an already-cancelled/completed observation returns a deterministic terminal/no-op result and does not mutate operation state again.

## C-010 — Is out-of-order concurrency required?

**Decision:** limited concurrency is required only to the extent necessary for an in-flight health observation plus cancellation and ordinary introspection requests. Inbound command frames remain serialized and monotonically identified on one Desktop→Core stream; responses/events may complete or arrive out of request order where their typed semantics permit it. S1 does not build a generalized async RPC runtime.

## C-011 — What frontend stack is required?

**Decision:** no frontend framework is justified for S1. Use the smallest local static presentation sufficient to show Core status/version/capabilities and cancellation state. React/Vite/Tailwind/pnpm are deferred unless a later user-interface slice provides an independent need.

## C-012 — What does restart recovery mean?

**Decision:** restart means fresh process identity, fresh protocol negotiation, fresh `launch_id`, and explicit invalidation of prior in-flight requests. No previous request is inferred successful. The Desktop may retry only operations whose S1 semantics are explicitly safe to repeat.

## C-013 — Does S1 need a network permission?

**Decision:** no. Runtime S1 network requirement is `NONE`.

Build-time package acquisition is a separate controlled software-supply-chain activity and is not a runtime network capability.

## C-014 — What is stderr used for?

**Decision:** protocol bytes use stdin/stdout only. Core stderr is diagnostics-only and is never parsed as protocol input.

If stderr is piped, the Desktop must drain it concurrently so a full OS pipe cannot block Core progress. Retained diagnostic data must be bounded; overflow may truncate/drop retained diagnostic bytes while the drain continues, and the truncation must be observable. An integration test must deliberately emit more diagnostic stderr than the platform pipe capacity while a normal protocol exchange continues successfully.
