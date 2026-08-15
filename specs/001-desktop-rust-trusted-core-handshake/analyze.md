# Analysis — S1 Desktop ↔ Rust Trusted Core Handshake

## Purpose

Reconcile the S1 constitution, specification, clarifications, plan, requirements checklist, Ponytail FULL result, acquisition preflight, threat model, and provisional task decomposition before execution-authoritative tasks are published.

```text
BASE = 6eff72319cad99c878a80f0d5bce9f107d213679
ANALYSIS_RESULT = PROCEED_TO_FINAL_TASKS_WITH_BLOCKED_IMPLEMENTATION
SOURCE_ACQUISITION_CHECK = OPEN
IMPLEMENTATION = BLOCKED
```

## Artifact consistency

### Authority consistency — PASS

All artifacts preserve:

- separate Desktop/Core processes;
- Desktop/WebView as untrusted presentation/transport;
- Core-owned validation/handshake state;
- connection/principal/Tauri ACL != Nawat authority;
- no project/filesystem/terminal/network/worker effects in S1;
- standing founder authorization != qualification bypass.

No artifact grants implementation or dependency admission merely because planning exists.

### Transport consistency — PASS

The artifacts consistently select inherited stdin/stdout as the minimum preferred transport and reject TCP/localhost and generalized endpoint machinery for base S1.

Named pipes remain a non-silent fallback candidate only if explicit Windows evidence proves inherited stdio insufficient.

### Protocol consistency — PASS WITH FINALIZATION TASKS

The protocol shape is coherent:

- v1;
- fixed 4-byte big-endian payload length;
- UTF-8 JSON;
- 64 KiB upper bound;
- typed message classes;
- `desktop_host` principal;
- launch/request IDs;
- duplicate/replay rejection;
- bounded event/cancellation operation;
- bounded state/backpressure;
- fail-closed restart semantics.

Implementation tasks must freeze exact Rust enum/struct field semantics and golden protocol fixtures before Desktop integration.

### Ponytail consistency — PASS

The provisional `crates/ipc` path is not justified as a standalone crate yet. A crate whose only purpose is forwarding frame bytes would add ownership/abstraction cost.

**Resolution:** initial final-task architecture uses:

```text
crates/contracts
  protocol types + pure frame codec + protocol constants/tests

crates/core
  Core state machine + Core executable

apps/desktop
  Tauri Desktop host + static presentation
```

A separate `crates/ipc` crate is deferred unless independent reuse/ownership emerges from implementation evidence. This remains compatible with V2.2 because expected paths are provisional, not entitlement.

### Dependency consistency — PASS / OPEN GATE

The planning package identifies the minimum direct dependency candidates but intentionally does not admit them yet:

- Tauri/Tauri-build for Desktop shell/build;
- Serde/serde_json for typed protocol encoding;
- Rust stdlib for Core transport/event-loop primitives.

`tauri-plugin-shell`, direct Tokio in Core, UUID, RPC frameworks, frontend frameworks, DB/network/telemetry packages remain rejected for base S1.

The unresolved evidence is mechanical and appropriately precedes implementation:

- exact candidate Cargo manifests;
- generated lockfile;
- direct/transitive feature inventory;
- SBOM;
- advisory scan;
- final dependency register/admission state.

### CI consistency — BLOCKING PRE-IMPLEMENTATION ITEM

P0 `foundation-integrity` is intentionally incompatible with implementation and dependency manifests. Adding S1 code before migrating this gate would create a known false structural failure; broadly weakening it would create a security regression.

**Resolution:** stage-aware foundation CI migration is its own bounded security-sensitive task and MUST precede dependency manifests/product code. It must preserve immutable P0 artifact/registry checks and replace only the fresh-foundation implementation prohibition with explicit S1 qualification rules.

### Security consistency — PASS FOR PLANNING

The threat model covers the actual S1 attack surfaces without making S3 containment claims. It explicitly includes protocol parser, process/executable identity, restart, WebView boundary, supply chain, and CI trust.

Implementation and workflow migration require applicable Codex Security coverage and independent engineering review before S1 acceptance.

## Provisional-task reconciliation

### PT-004 / PT-005 ordering corrected

The provisional list placed stage-aware CI migration and dependency resolution as adjacent tasks. Analysis determines they should remain separate changes:

1. **CI migration first** while the tree is still documentation-only, so the policy change can be reviewed without simultaneous package-graph noise.
2. **Candidate dependency-resolution bootstrap second**, after the gate can represent S1 correctly.

This separation makes review/rollback clearer and prevents an implementation manifest from arriving in a tree whose only deterministic gate still forbids it.

### PT-007 / PT-008 merged conceptually

Protocol frame codec and pure handshake state have different ownership but should be developed under one contract-first implementation phase with separate commits/tasks, because state-machine tests depend on the exact protocol types and both are pure Rust before process integration.

### PT-009 Core process narrowed

The Core process task must not introduce async frameworks, filesystem/network effects, daemon/service discovery, or S3 containment claims. It should be a small stdin/stdout child executable only.

### PT-010 Desktop host narrowed

Desktop work must separate:

- package/sibling-path lifecycle;
- pipe/client protocol handling;
- static UI projection.

No general shell plugin/API is admitted merely for convenience.

### PT-012 Windows qualification bounded against S3

S1 must prove child launch, pipes, exit detection, restart, packaging, and orphan observations on Windows. It must NOT claim hostile-worker containment or full trusted process ownership; those belong to S3.

If orphan prevention requires deeper Job Object/process-ownership machinery than S1 can justify, S1 records the residual limitation and blocks any stronger claim rather than silently pulling S3 forward. A minimal parent-owned cleanup primitive may be implemented only if required for correct S1 lifecycle and independently reviewed.

## Final task sequencing decision

Execution-authoritative tasks will use these gates:

```text
S1-001 planning baseline commit + Draft PR
S1-002 current-state checkpoint
S1-003 stage-aware foundation CI migration
  -> deterministic test of old P0 invariants + new S1 phase rules
  -> security review because workflow trust changes
S1-004 dependency-resolution bootstrap
  -> candidate manifests/toolchain only, no product behavior
S1-005 final component admission
  -> lock/tree/SBOM/advisory/features/dependency register
  -> Source Acquisition Check PASS required
S1-006 protocol contracts + codec
S1-007 pure handshake/replay/cancellation state
S1-008 Core child process
S1-009 Desktop host child lifecycle/protocol client
S1-010 minimal static UI projection
S1-011 cross-process/failure/adversarial suite
S1-012 Windows primary qualification + Linux/macOS secondary evidence
S1-013 benchmark/evidence packet
S1-014 applicable security + independent correctness review
S1-015 bounded repair/rerun/rereview
S1-016 standing-authority S1 acceptance + Build Learning capture
```

No task after S1-004 may begin merely because a candidate manifest resolves. `S1-005 SOURCE_ACQUISITION_CHECK = PASS` is the implementation admission gate.

## Risks retained explicitly

1. Tauri external-binary packaging path/update behavior must be proven on Windows, not inferred from documentation.
2. Direct stdlib sibling launch may require platform-specific executable path resolution; wrong-path/PATH search is prohibited.
3. Anonymous pipes constrain origin but are not cryptographic authentication and are not hostile-process containment.
4. Core orphan cleanup semantics on Windows may expose a boundary with S3; claim scope must stay precise.
5. A 64 KiB frame budget may be larger than necessary and should be tightened from evidence before acceptance.
6. Tauri's transitive dependency graph is broad relative to S1; exact lock/SBOM/advisory analysis may force feature/package adjustment.
7. Spec Kit upstream command ordering has drifted from WePLD canonical order; the compatibility record must remain explicit rather than silently following upstream.

## Analysis verdict

```text
SPEC_KIT_ANALYSIS = PASS_FOR_FINAL_TASK_DECOMPOSITION
PONYTAIL_FULL = COMPLETE_FOR_PLANNING
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION = BLOCKED
NEXT = PUBLISH_FINAL_TASKS_AND_ACCEPTANCE_CONTRACT
```
