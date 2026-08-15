# Specification — S1 Desktop ↔ Rust Trusted Core Handshake

## Problem

WePLD needs a desktop shell that can communicate with a separate Rust Trusted Core without collapsing presentation, transport, validation, and authority into one process or one framework ACL. The first executable slice must prove that this boundary is typed, versioned, bounded, observable, cancellable, restart-safe, Windows-first, and incapable of minting authority merely because a connection exists.

## User-visible outcome

On a supported workstation, launching the WePLD desktop starts or attaches only to its intended local Core child, negotiates protocol v1, and can display:

- Core health;
- Core version/build identity;
- supported S1 capabilities;
- whether the handshake is ready, degraded, restarting, or unavailable.

A cancellable handshake-owned operation must be demonstrably cancellable. If Core is absent, crashes, restarts, emits malformed data, or is incompatible, the desktop reports a bounded failure state rather than fabricating readiness or authority.

## Functional requirements

### FR-001 — Separate processes

Desktop and Core MUST be separate OS processes. The WebView MUST NOT host Trusted Core state.

### FR-002 — Local-only transport

The base S1 channel MUST remain local-only and MUST NOT open a network listener. The minimum preferred design is inherited stdin/stdout pipes between the Desktop Rust host and its Core child.

### FR-003 — Typed versioned envelope

Every protocol payload MUST belong to an explicit protocol version and typed envelope family. At minimum the protocol MUST distinguish request, response, event, cancellation, and protocol-error semantics.

### FR-004 — Bounded framing

The receiver MUST validate a fixed-width frame length before allocating or deserializing the payload. Oversized, truncated, malformed, unknown-version, and unknown-kind frames MUST fail closed.

The initial S1 frame budget is 64 KiB. This is a planning budget, not a permanent product constant; benchmarks and observed S1 payloads may justify reducing it before acceptance. Raising it requires an explicit evidence-backed change.

### FR-005 — Principal binding without false authority

Requests MUST carry or inherit an explicit Desktop-host principal identity that cannot be supplied or enlarged by arbitrary WebView input. Core MUST reject unknown principal values. Principal identity in S1 is correlation/trust-boundary metadata only; it grants no filesystem, process, network, repository, or completion authority.

### FR-006 — Correlation and launch identity

Requests and responses MUST carry bounded correlation identifiers. A Core launch/restart MUST have a launch identity so stale responses/events from a previous launch cannot be accepted as current.

### FR-007 — Replay / duplicate semantics

Duplicate or replayed request identifiers MUST have deterministic behavior and MUST NOT execute a second effect. S1 commands are non-effecting handshake/introspection operations; the protocol still MUST establish a reusable duplicate-detection invariant for later slices.

### FR-008 — Core introspection

Protocol v1 MUST provide typed health, version/build identity, and capability-description responses.

### FR-009 — Events and cancellation

The protocol MUST support a bounded long-lived S1-owned observation operation sufficient to prove event delivery and cancellation. Cancellation MUST be correlated to an in-flight operation, idempotent, and unable to cancel a different request by identifier confusion.

### FR-010 — Backpressure and bounded state

The Core MUST place explicit bounds on frame size, queued/in-flight operations, retained duplicate identifiers, and emitted events. Flooding MUST produce bounded rejection/backpressure rather than unbounded memory growth.

### FR-011 — Restart and EOF semantics

EOF, broken pipe, child exit, malformed terminal frame, and Core crash MUST move the Desktop channel out of ready state. Reconnect/restart MUST negotiate a fresh launch identity. No in-flight request may be fabricated complete across a restart.

### FR-012 — Minimal desktop presentation

The S1 UI MUST be deliberately minimal. It MAY use static local HTML/JavaScript with no frontend framework. It MUST NOT expose general shell/process/filesystem permissions to WebView code merely to implement the handshake.

### FR-013 — Exact build identity

Acceptance evidence MUST identify the exact Desktop binary, Core binary, protocol version, Rust toolchain, dependency lockfile, and tested commit.

### FR-014 — Platform qualification

Windows x86_64 MSVC is the primary acceptance platform. macOS and Linux require compile/contract coverage according to the S1 plan; absence of Windows runtime evidence blocks the Windows-first S1 claim.

## Security and trust requirements

- Desktop/WebView input is untrusted.
- Core validates every externally supplied field before trusted-state mutation.
- No Tauri capability/ACL, process relationship, connection state, principal label, protocol version, or successful health response is a Nawat grant.
- The Core handshake carries no project content, credentials, secrets, PHI, private customer data, or hosted telemetry.
- Network access is not required for runtime operation.
- Automatic external-review egress remains prohibited without the canonical pre-egress gate.

## Failure corpus

The deterministic suite MUST cover at least:

- unknown command;
- unknown/unsupported protocol version;
- attempted schema downgrade;
- forged/unknown principal;
- request-id duplicate/replay;
- stale launch identity;
- zero-length and oversized frame;
- truncated prefix/body;
- invalid UTF-8 where text is required;
- malformed JSON;
- unexpected fields where the S1 contract marks them invalid;
- cancellation of unknown/completed/already-cancelled request;
- cancellation race;
- flood/in-flight budget exhaustion;
- Core unavailable before launch;
- Desktop-side writer loss;
- Core crash;
- Desktop crash / stdin close;
- stale response/event after restart.

## Performance budgets to measure

No performance result is a correctness substitute. S1 records at minimum:

- cold Core spawn + handshake latency;
- health request p50/p95/p99 latency;
- bounded throughput for small requests;
- idle Desktop/Core memory;
- CPU while idle;
- cancellation latency;
- crash detection and fresh-handshake recovery latency;
- malformed/oversized-frame rejection cost.

Thresholds are finalized from measured baseline evidence before S1 acceptance rather than invented as success criteria in advance.

## Non-goals

- project filesystem access;
- terminal/process execution beyond launching the owned Core child;
- network broker or cloud sync;
- worker/model routing;
- Fehrest persistence;
- generalized RPC framework;
- arbitrary plugin transport;
- remote clients;
- updater implementation;
- trusted completion beyond the S1 slice itself.
