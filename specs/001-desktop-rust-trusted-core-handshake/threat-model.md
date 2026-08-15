# Threat Model — S1 Desktop ↔ Rust Trusted Core Handshake

## Scope

This threat model covers only the S1 boundary between:

```text
WebView / local presentation
        ↓
Desktop Rust host
        ↓ inherited anonymous pipes
Separate Rust Core child
```

It does not claim S3 hostile-worker containment, Nawat authorization, project filesystem security, terminal confinement, or network sandboxing.

## Protected properties

S1 must preserve:

1. Core protocol parser/state cannot be bypassed by WebView-supplied data.
2. A successful connection/handshake cannot mint authority.
3. Only the Desktop-owned Core child is used by the base transport design.
4. Frames cannot induce unbounded pre-deserialization allocation.
5. Stale/replayed/duplicate messages cannot be accepted as fresh effects.
6. Restart/crash cannot fabricate request success or preserve stale readiness.
7. Cancellation cannot cross request identity boundaries.
8. Runtime S1 does not require network access or secrets.
9. Dependency/build provenance remains exact and auditable.
10. UI cannot obtain generalized process/filesystem/shell permissions merely for S1.

## Trust boundaries

### TB-1 — WebView → Desktop Rust host

**Trust:** untrusted input crosses into local Rust host.

Threats:
- forged principal or protocol fields;
- oversized strings/payloads;
- arbitrary command invocation;
- UI attempting to acquire shell/filesystem/process permissions;
- stale UI state displaying Core as ready after loss.

Controls:
- Desktop assigns principal/launch identity internally;
- narrow typed commands/projections only;
- no general shell/filesystem/network WebView capability;
- ready state derives from live Core lifecycle state, not UI memory.

### TB-2 — Desktop Rust host → Core child stdin

**Trust:** Desktop host is transport owner but still cannot bypass Core validation.

Threats:
- malformed frame length/body;
- unsupported version/downgrade;
- forged or stale launch identity;
- duplicate/replay IDs;
- request flood;
- cancellation identifier confusion.

Controls:
- fixed 4-byte length prefix;
- 64 KiB maximum payload before allocation/deserialization;
- strict typed version/kind/principal/operation validation;
- bounded in-flight and recent-ID state;
- deterministic duplicate/replay rejection;
- correlated cancellation.

### TB-3 — Core stdout → Desktop Rust host

Threats:
- malformed/truncated frames;
- unexpected event/response kind;
- stale response after restart;
- response ID mismatch;
- output flood;
- forged readiness/capability shape.

Controls:
- same bounded frame decoder on Desktop side;
- exact launch/request correlation;
- typed response/event enums;
- bounded queues/state;
- broken pipe/EOF invalidates readiness;
- unknown or malformed output fails channel state closed.

### TB-4 — Process lifecycle / executable identity

Threats:
- wrong executable path;
- PATH search/substitution;
- stale bundled Core binary;
- Core orphan after Desktop exit;
- rapid crash/restart loop;
- update/install leaves mismatched Desktop/Core versions.

Controls/planned evidence:
- launch an explicit packaged sibling path, never shell/PATH lookup;
- capture exact Core/Desktop binary identity in acceptance evidence;
- protocol/version mismatch fails closed;
- Windows package/upgrade and lifecycle tests;
- bounded restart policy/no infinite silent restart loop;
- orphan behavior is measured and failure is explicit.

S1 does NOT claim a strong hostile-process containment boundary merely because Desktop spawned Core.

### TB-5 — Build/dependency supply chain

Threats:
- mutable/unpinned tool/package identity;
- unnecessary dependencies increase attack surface;
- vulnerable transitive crate;
- dependency confusion or feature creep;
- generated lockfile/SBOM drift;
- CI weakening to permit arbitrary implementation paths.

Controls:
- exact toolchain/package candidates;
- generated Cargo.lock before final admission;
- direct/transitive feature inventory;
- SBOM + advisory scan;
- Ponytail rejects unnecessary packages;
- stage-aware CI uses explicit S1 path/admission constraints rather than removing P0 controls;
- exact-head security review for workflow/security-boundary changes.

## Threat catalogue

| ID | Threat | Impact | S1 control / required evidence |
|---|---|---|---|
| S1-T01 | oversized length prefix | memory exhaustion | reject > `MAX_FRAME_BYTES` before allocation |
| S1-T02 | truncated frame | parser desync / false success | exact-length read or explicit terminal protocol error |
| S1-T03 | malformed JSON | parser confusion | typed deserialize error, channel remains fail-closed |
| S1-T04 | unknown protocol version | downgrade/undefined semantics | reject; no implicit v1 fallback |
| S1-T05 | unknown principal | authority confusion | only internally assigned `desktop_host` accepted |
| S1-T06 | duplicate request ID | duplicate effect | deterministic duplicate/replay rejection |
| S1-T07 | stale launch response | cross-restart confusion | launch ID must match current child lifecycle |
| S1-T08 | cancellation ID collision | wrong operation cancelled | launch + request correlation and terminal-state checks |
| S1-T09 | request/event flood | memory/CPU exhaustion | explicit queue/in-flight/watch/window budgets |
| S1-T10 | Core crash during request | fabricated completion | mark interrupted/unknown; never success |
| S1-T11 | Desktop loses pipe | stale ready state | EOF/broken pipe transitions out of ready immediately |
| S1-T12 | wrong Core executable | binary substitution | explicit sibling path + package/binary identity evidence |
| S1-T13 | mismatched packaged versions | protocol corruption | version negotiation + packaging tests |
| S1-T14 | WebView obtains shell access | privilege expansion | no shell plugin/general process permission in base S1 |
| S1-T15 | Tauri capability mistaken for authority | authorization bypass | canonical invariant; Core never consumes Tauri ACL as Nawat grant |
| S1-T16 | runtime network unexpectedly opened | new remote attack surface | no network listener/client requirement; verify runtime behavior |
| S1-T17 | CI allowlist broadly relaxed | later unauthorized source/dependency admission | stage-aware explicit allowlist/admission checks + security review |
| S1-T18 | dependency advisory ignored | supply-chain vulnerability | advisory reconciliation blocks final admission when reportable |
| S1-T19 | restart loop | availability/resource exhaustion | bounded restart policy + visible failure state |
| S1-T20 | orphan Core child | stray process/state | Windows lifecycle test; failure retained honestly if not solved within S1 without importing S3 scope |

## Explicit non-claims

```text
CHILD_PROCESS_RELATIONSHIP != CONTAINMENT
ANONYMOUS_PIPE != CRYPTOGRAPHIC_AUTHENTICATION
PRINCIPAL_LABEL != NAWAT_GRANT
TAURI_ACL != CORE_AUTHORITY
PROTOCOL_VALIDATION != WINDOWS_SANDBOX
CLEAN_SECURITY_REVIEW != TRUSTED_COMPLETION
```

## Security review applicability

S1 implementation and the stage-aware CI migration are security-relevant under `docs/canonical/SECURITY_REVIEW_POLICY.md` because they affect process/IPC boundaries, external-input parsing, configuration, dependency execution, and workflow trust.

A Codex Security diff scan is therefore applicable when available and egress policy permits. Any missing applicable coverage is recorded as coverage limitation/`NOT_RUN_NON_BLOCKING` under policy, never rewritten as PASS.
