# Ponytail FULL — S1 Desktop ↔ Rust Trusted Core Handshake

```text
MODE = FULL
SOURCE = DietrichGebert/ponytail
REVISION = 2ed6c52c9d7e5e56942508591085fd45dea277d3
SKILL_BLOB = 02c0712c86277d49d18a77da3a2b825657bf02d1
RESULT = COMPLETE_FOR_PLANNING
IMPLEMENTATION_AUTHORITY = NO
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

Ponytail reduces machinery only after understanding the full S1 flow. It does not simplify away trust-boundary validation, denial behavior, recovery, evidence, security, or accessibility.

## 1 — Does the handshake need to exist?

**YES.** V2.2 S1 explicitly requires a typed, versioned, observable channel between Tauri Desktop and a separate Rust Core process. Folding Core into the Tauri process would remove the process boundary and violate the ratified architecture.

## 2 — Does existing WePLD code already solve it?

**NO active implementation.** P0 intentionally merged with empty implementation source. Historical repositories remain quarry-only and cannot be inherited wholesale.

Prior WePLD handshake evidence may be used only as test/failure oracle after bounded salvage review.

## 3 — Can the standard library solve the transport/runtime mechanics?

**LARGELY YES.** Rust `std::process::Command`, `Stdio::piped`, `ChildStdin`, `ChildStdout`, threads, `std::sync::mpsc`, atomics, `HashMap`/`VecDeque`, and `Read`/`Write` are sufficient for the minimum separate-process byte-stream transport and Core event loop.

Therefore S1 does not justify an RPC framework, socket library, async runtime for Core, actor framework, UUID crate, retry framework, or IPC daemon.

## 4 — Is a native platform primitive preferable?

**YES: inherited anonymous pipes.** They are OS-native handles created by the parent process and avoid a separately addressable service endpoint.

Windows named pipes remain a future fallback candidate only if inherited stdio fails measured requirements. TCP/localhost HTTP is rejected for base S1.

## 5 — Does an already selected/installed dependency solve necessary packaging?

Tauri is the ratified desktop shell candidate and its bundler supports `externalBin`. That solves packaging of the Core executable.

The Tauri shell plugin can also launch sidecars, but its package surface includes general shell/process mechanics that S1 does not need. Its inspected implementation ultimately resolves the packaged child relative to the current executable, pipes stdin/stdout/stderr, and writes bytes to child stdin.

**Disposition:** use Tauri bundling + Rust stdlib process launch first. Do not admit `tauri-plugin-shell` for S1 unless direct launch fails an explicit packaging/recovery acceptance test.

## 6 — Can a one-line/simple mechanism replace proposed abstractions?

Several proposed abstractions are rejected:

- no generalized `Transport` trait with multiple unused backends;
- no generic RPC router;
- no plugin bus;
- no event sourcing framework;
- no generalized policy engine in S1;
- no network broker;
- no frontend framework;
- no database;
- no logging/telemetry SDK unless deterministic evidence later proves stdio/test output insufficient.

Protocol types remain explicit enums/structs rather than dynamic maps because typed failure semantics are a core S1 requirement, not abstraction overhead.

## 7 — Minimum custom code that remains justified

Custom WePLD-owned code is still required for:

- protocol v1 envelope and operation types;
- fixed-length bounded framing;
- strict validation;
- principal/launch/correlation semantics;
- duplicate/replay window;
- bounded health observation and cancellation;
- Core state machine;
- Desktop-owned Core lifecycle/restart state;
- exact acceptance/failure tests.

These are WePLD trust semantics and cannot be delegated to a framework ACL.

## Dependency dispositions

| Candidate | Ponytail disposition | Reason |
|---|---|---|
| Rust stable toolchain | USE / PIN | product implementation language and toolchain |
| `tauri` | PACKAGE CANDIDATE | required desktop framework under V2.2; exact S1 admission pending |
| `tauri-build` | BUILD PACKAGE CANDIDATE | minimum Tauri build/config integration |
| `serde` | PACKAGE CANDIDATE | typed serialization; handwritten equivalent rejected |
| `serde_json` | PACKAGE CANDIDATE | compact human-inspectable protocol encoding; handwritten JSON rejected |
| `tauri-plugin-shell` | REFERENCE / REJECT INITIAL | stdlib process launch is smaller; plugin is fallback only after measured failure |
| `tokio` in Core | REJECT DIRECT DEPENDENCY | stdlib threads/mpsc/timers are sufficient for S1 |
| UUID/random-ID crate | REJECT | S1 IDs are correlation, not cryptographic grants; monotonic bounded IDs suffice |
| Protobuf/Cap'n Proto/MessagePack | REJECT FOR S1 | extra schema/build/dependency machinery not justified by tiny local contract |
| React/Vite/Tailwind | REJECT FOR S1 | static presentation is sufficient; UI system is outside S1 |

## Scope reductions produced by Ponytail

Compared with an unconstrained desktop IPC implementation, S1 intentionally removes:

- TCP/HTTP server;
- named pipe server and ACL design;
- shell plugin dependency;
- Node package manager/runtime from the base UI;
- generalized RPC framework;
- generalized streaming subsystem;
- project/file/process/network effects;
- cloud telemetry/control;
- cryptographic identity claims that S1 does not need.

## Non-reducible controls

Ponytail MUST NOT remove:

- frame bounds before allocation;
- strict protocol/version validation;
- unknown principal denial;
- stale-launch rejection;
- duplicate/replay semantics;
- cancellation correctness;
- backpressure/state bounds;
- child crash/restart handling;
- Windows runtime evidence;
- exact lock/SBOM/advisory review;
- security review;
- independent engineering review;
- exact-head acceptance evidence.

## Gate conclusion

`PONYTAIL_FULL = COMPLETE_FOR_PLANNING`.

Implementation remains blocked until `source-acquisition.md` reaches a qualified component-admission state and the P0-only foundation CI boundary is safely migrated to a stage-aware S1 gate.
