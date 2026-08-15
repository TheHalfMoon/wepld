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
  - serializes strictly increasing command IDs onto one writer
  - never grants S1 effects beyond handshake scope
              |
              | inherited stdin/stdout protocol byte streams
              | stderr diagnostics only
              | 4-byte BE length + JSON envelope
              v
Separate Rust Core Process
  - owns protocol parser/validation
  - owns handshake state
  - owns launch-wide monotonic replay floor/high-water mark
  - health/version/capability responses
  - bounded health observation + cancellation
              |
              v
No filesystem/project/network/worker authority in S1
```

## Proposed repository layout

Expected implementation paths remain provisional until Source Acquisition closes. Analysis removed the initially proposed abstraction-only `crates/ipc` crate; framing belongs with the protocol contracts unless implementation evidence later establishes an independent ownership boundary.

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
tests/
  desktop_core/
specs/001-desktop-rust-trusted-core-handshake/
```

Any further crate must have an independently justified contract/ownership reason; expected V2.2 paths are not entitlement to extra abstractions.

## Protocol v1 planning contract

Envelope fields are intentionally minimal and subject to typed implementation:

```text
protocol_version = 1
kind = request | response | event | cancel | protocol_error
principal = desktop_host
launch_id = u64
request_id = u64 where applicable
target_request_id = u64 for cancellation
operation = typed enum where applicable
payload = operation-specific typed value
```

Inbound Desktop→Core request/cancel IDs are allocated in serialized writer order, are strictly increasing within one launch, never wrap/reuse, and are rejected by Core when `id <= highest_accepted_command_id`. Responses/events may complete out of request order but must preserve launch/request correlation.

Framing:

```text
[u32 big-endian payload length][UTF-8 JSON payload]
MAX_PAYLOAD_BYTES = 65_536
```

Unknown version/kind/principal/operation, malformed length, over-budget payload, invalid JSON, stale launch identity, and non-monotonic/replayed command IDs fail closed.

## Implementation phases

### S1-P1 — Planning and source qualification

- complete Spec Kit artifacts;
- execute Ponytail FULL;
- re-pin required components and record candidate-only status;
- decide package versus stdlib mechanics;
- migrate `foundation-integrity` to a stage-aware invariant gate **before** any candidate implementation/dependency manifest is introduced;
- independently validate/review that workflow-trust migration and reconcile findings;
- only then authorize the minimum dependency-resolution bootstrap needed to produce a candidate lockfile/SBOM;
- inspect resolved direct/transitive features, dependencies, SBOM, and advisories;
- finalize component admission record and `SOURCE_ACQUISITION_CHECK = PASS` only when evidence is complete.

### S1-P2 — Contracts and pure protocol engine

- create minimal admitted Rust workspace/toolchain pin;
- implement typed protocol v1 contracts;
- implement bounded frame encoder/decoder;
- implement launch-wide monotonic replay rejection plus pure handshake/cancellation semantics;
- add unit/property/negative tests before Desktop integration.

### S1-P3 — Core process

- separate Core executable;
- protocol uses stdin/stdout only;
- stderr is diagnostics-only and must be continuously drained/handled without blocking protocol progress;
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
- concurrently drain/handle diagnostics stderr with bounded retained data and observable truncation;
- project typed status into a minimal local UI;
- expose no general shell/filesystem/process capability to WebView.

### S1-P5 — Cross-process integration / failure suite

- round-trip, event, cancellation;
- malformed and oversized frames;
- version/principal/downgrade attacks;
- launch-wide duplicate/replay/non-monotonic ID rejection;
- duplicate stateful observation/cancellation semantics;
- stale launch;
- Core unavailable/crash/restart;
- Desktop crash/pipe close;
- backpressure/flood budgets;
- stderr pipe-fill while protocol remains live;
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
- rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head;
- record S1 acceptance only after exact-head evidence is complete;
- Build Learning capture.

## Foundation-integrity migration

The P0 workflow currently intentionally rejects all implementation-language files and dependency manifests. S1 MUST NOT simply delete those protections.

Before candidate manifests or implementation are introduced, replace the P0-only boundary with a stage-aware gate that continues to prove:

- immutable P0 canonical archive and V2.2 identity;
- frozen 402 registry restoration evidence remains unchanged;
- no unauthorized source/dependency admission;
- no symlink/gitlink bypass;
- only S1-qualified implementation paths/manifests are allowed;
- required S1 planning/acquisition/lock/admission records exist;
- later slices remain absent;
- no temporary repair payload/workflow leakage;
- hosted-review repository configs remain manual-only;
- Cubic repository configuration is schema-valid and provider-effective state is not assumed from file comparison alone; Cubic stays blocked from being counted/used when provider validation evidence is unavailable.

That workflow change is security-relevant and requires exact-head security coverage.

## Budgets

Initial safety budgets, subject to measured tightening before acceptance:

```text
MAX_FRAME_BYTES = 65_536
MAX_IN_FLIGHT_REQUESTS = 32
MAX_HEALTH_WATCHES = 8
MAX_CAPABILITY_ITEMS = 64
MAX_PROTOCOL_ERROR_TEXT_BYTES = 1_024
MAX_RETAINED_DIAGNOSTIC_BYTES = 65_536
REPLAY_STATE = O(1) highest_accepted_command_id per launch
```

These are upper bounds, not throughput goals. Tests must prove rejection at and beyond boundaries. Command IDs never wrap or reuse within a launch; exhaustion requires a fresh launch rather than weakening the replay invariant.

## Recovery

- Core EOF/exit immediately invalidates `ready`.
- A restart receives a new `launch_id` and must re-negotiate protocol v1.
- Old response/event data is rejected by launch identity.
- In-flight requests become explicit interrupted/unknown terminal states; none is fabricated successful.
- S1 read-only/introspection operations may be safely reissued only after fresh handshake with new command IDs.
- Stderr retention pressure may truncate retained diagnostics but must not stop the drain or protocol progress.
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

S1 exits only when the exact accepted head demonstrates typed round-trip, bounded event delivery, cancellation, launch-wide replay rejection, fail-closed malformed/unauthorized input, no silent downgrade, crash/restart without false authority, non-blocking bounded stderr diagnostics handling, Windows runtime qualification, exact dependency/binary identity, applicable security review, independent engineering review, finding reconciliation, and authorized acceptance.
