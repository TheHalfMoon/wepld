# Plan — S1 Desktop ↔ Rust Trusted Core Handshake

## Identity

```text
SLICE = S1
NAME = Desktop ↔ Rust Trusted Core Handshake
BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
P0_ACCEPTED_HEAD = b67fc1be0e505b7cbd1adf286c6a26db9da9c95c
MASTER_PLAN = V2.2
MASTER_PLAN_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
FOUNDER_STANDING_AUTHORIZATION = RECORDED_IN_PR_2
IMPLEMENTATION = NOT_STARTED
RUNTIME_DEPENDENCY_ADMISSION = NOT_YET_COMPLETE
```

## Build-method provenance

WePLD canonical order remains:

```text
constitution -> specify -> clarify -> plan -> checklist -> analyze -> tasks
-> Ponytail FULL
-> Source Acquisition Check
-> implementation
```

The current inspected Spec Kit source is `github/spec-kit@bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`, whose current quickstart places `tasks` before `analyze`.

To avoid silently changing either authority, S1 uses this compatibility sequence:

```text
constitution
-> specify
-> clarify
-> plan
-> checklist
-> provisional task decomposition
-> analyze
-> corrected/final tasks
```

Only `tasks.md` is execution-authoritative for S1. `analyze.md` records the cross-artifact reconciliation that produced the final task set.

Ponytail source inspected for this slice:

```text
DietrichGebert/ponytail
REVISION = 2ed6c52c9d7e5e56942508591085fd45dea277d3
SKILL = skills/ponytail/SKILL.md
BLOB = 02c0712c86277d49d18a77da3a2b825657bf02d1
MODE = FULL
```

## Architecture

```text
Untrusted WebView / minimal presentation
              |
              | narrow Tauri app commands / projections only
              v
Desktop Rust Host
  - owns Core child lifecycle
  - assigns desktop_host principal
  - allocates launch_id/request_id
  - never grants S1 effects beyond handshake scope
              |
              | inherited stdin/stdout byte streams
              | 4-byte BE length + JSON envelope
              v
Separate Rust Core Process
  - owns protocol parser/validation
  - owns handshake state
  - health/version/capability responses
  - bounded health observation + cancellation
  - duplicate/replay rejection
              |
              v
No filesystem/project/network/worker authority in S1
```

## Proposed repository layout

Expected implementation paths are provisional until Source Acquisition closes:

```text
Cargo.toml
Cargo.lock
rust-toolchain.toml
apps/desktop/
  src-tauri/
    Cargo.toml
    build.rs
    tauri.conf.json
    capabilities/
    src/
  ui/
    index.html
    app.js
crates/
  contracts/
    Cargo.toml
    src/
  core/
    Cargo.toml
    src/
  ipc/
    Cargo.toml
    src/
tests/
  desktop_core/
specs/001-desktop-rust-trusted-core-handshake/
```

The final tree must remain smaller if a crate has no independent contract/ownership reason. `crates/ipc` is not automatically justified merely because V2.2 lists it as an expected path; Ponytail may fold framing into `contracts` or `core` if that is simpler without mixing ownership.

## Protocol v1 planning contract

Envelope fields are intentionally minimal and subject to typed implementation:

```text
protocol_version = 1
kind = request | response | event | cancel | protocol_error
principal = desktop_host
launch_id = u64
request_id = u64 where applicable
operation = typed enum where applicable
payload = operation-specific typed value
```

Framing:

```text
[u32 big-endian payload length][UTF-8 JSON payload]
MAX_PAYLOAD_BYTES = 65_536
```

Unknown version/kind/principal/operation, malformed length, over-budget payload, invalid JSON, and stale launch identity fail closed.

## Implementation phases

### S1-P1 — Planning and source qualification

- complete Spec Kit artifacts;
- execute Ponytail FULL;
- re-pin required components;
- decide package versus stdlib mechanics;
- authorize only the minimum dependency-resolution step needed to produce a lockfile/SBOM candidate;
- inspect resolved transitive dependencies and advisories;
- finalize component admission record;
- evolve `foundation-integrity` into a stage-aware invariant gate before implementation paths are introduced.

### S1-P2 — Contracts and pure protocol engine

- create minimal Rust workspace/toolchain pin;
- implement typed protocol v1 contracts;
- implement bounded frame encoder/decoder;
- implement pure handshake state/replay/cancellation semantics;
- add unit/property/negative tests before Desktop integration.

### S1-P3 — Core process

- separate Core executable;
- stdin reader + bounded event loop using stdlib unless a qualified need changes this;
- health/version/capabilities;
- bounded health observation and cancellation;
- deterministic EOF/crash behavior;
- no network/filesystem/project effects.

### S1-P4 — Desktop host and minimal UI

- minimal Tauri desktop binary;
- bundle Core via `externalBin` or the minimum qualified bundling mechanism;
- launch only the owned sibling Core executable;
- pipe framing and child lifecycle;
- project typed status into a minimal local UI;
- expose no general shell/filesystem/process capability to WebView.

### S1-P5 — Cross-process integration / failure suite

- round-trip, event, cancellation;
- malformed and oversized frames;
- version/principal/downgrade attacks;
- duplicate/replay/stale launch;
- Core unavailable/crash/restart;
- Desktop crash/pipe close;
- backpressure/flood budgets;
- exact-binary identity capture.

### S1-P6 — Windows-first qualification and cross-platform evidence

Primary runtime qualification:

```text
x86_64-pc-windows-msvc
```

Required secondary evidence:

- Linux compile + contract tests;
- macOS compile + contract tests where CI runner availability permits;
- no platform claim may be inferred from compilation alone.

### S1-P7 — Review, repair, acceptance

- deterministic gates;
- Codex Security diff scan because S1 changes process/IPC/trust boundaries and CI/workflow logic;
- independently qualified correctness/engineering review;
- normalize/reconcile all findings;
- bounded repair only;
- rerun affected gates/reviews on exact head;
- record S1 acceptance only after exact-head evidence is complete;
- Build Learning capture.

## Foundation-integrity migration

The P0 workflow currently intentionally rejects all implementation-language files and dependency manifests. S1 MUST NOT simply delete those protections.

Before implementation begins, replace the P0-only boundary with a stage-aware gate that continues to prove:

- immutable P0 canonical archive and V2.2 identity;
- frozen 402 registry restoration evidence remains unchanged;
- no unauthorized source/dependency admission;
- no symlink/gitlink bypass;
- only S1-qualified implementation paths/manifests are allowed;
- required S1 planning/acquisition/lock/admission records exist;
- later slices remain absent;
- no temporary repair payload/workflow leakage.

That workflow change is security-relevant and requires exact-head security coverage.

## Budgets

Initial safety budgets, subject to measured tightening before acceptance:

```text
MAX_FRAME_BYTES = 65_536
MAX_IN_FLIGHT_REQUESTS = 32
MAX_HEALTH_WATCHES = 8
RECENT_REQUEST_ID_WINDOW = 1_024
MAX_CAPABILITY_ITEMS = 64
MAX_PROTOCOL_ERROR_TEXT_BYTES = 1_024
```

These are upper bounds, not throughput goals. Tests must prove rejection at and beyond boundaries.

## Recovery

- Core EOF/exit immediately invalidates `ready`.
- A restart receives a new `launch_id` and must re-negotiate protocol v1.
- Old response/event data is rejected by launch identity.
- In-flight requests become explicit interrupted/unknown terminal states; none is fabricated successful.
- S1 read-only/introspection operations may be safely reissued only after fresh handshake.
- Child cleanup behavior is measured on Windows; orphaning is a defect, not a tolerated normal state.

## Evidence retention

The S1 acceptance packet must retain or link exact immutable evidence for:

- base/head SHAs;
- Rust toolchain;
- Cargo.lock digest;
- SBOM/advisory output;
- protocol contract/version;
- deterministic gate run IDs;
- Windows runtime test evidence;
- secondary platform evidence;
- benchmark output;
- security review;
- independent engineering review;
- reconciled findings;
- founder/standing-authority acceptance record.

## Exit condition

S1 exits only when the exact accepted head demonstrates typed round-trip, bounded event delivery, cancellation, fail-closed malformed/unauthorized input, no silent downgrade, crash/restart without false authority, Windows runtime qualification, exact dependency/binary identity, applicable security review, independent engineering review, finding reconciliation, and authorized acceptance.
