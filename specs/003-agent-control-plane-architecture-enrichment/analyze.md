# Analyze — Spec 003

## Consistency analysis

### Authority
PASS candidate: new protocol/graph/sandbox layers remain outside authority. Nawat remains sole effect-time authority domain.

### Provider neutrality
PASS candidate: Agent Host uses capability-driven adapters; no selected model/provider becomes architectural truth.

### Local/air-gap
PASS candidate: core graph/evidence/policy/session design is local. Hosted APIs and telemetry are optional adapters.

### Rust-first
PASS candidate: trusted effect/policy/session contracts remain Rust-first; Cedar/ACP/A2A all have Rust-compatible paths, while non-Rust donors remain behind contracts.

### Acquisition discipline
PASS candidate: Tier-1 pins are research identities only. Frozen registry remains unchanged.

### Roadmap churn
PASS candidate: no slice renumbering. Five named non-primary gates refine existing slices.

## Key risks

1. **Protocol duplication** — UWC could duplicate ACP/AHP. Mitigation: keep UWC semantic/minimal and implement adapters.
2. **Graph overengineering** — code graph could become a new platform before user value. Mitigation: S4-G minimum graph only, storage deferred.
3. **Authority leakage** — agent permission APIs may be mistaken for Nawat. Mitigation: explicit invariants and negative tests.
4. **Policy lock-in** — ACS/Cedar semantics could become product semantics. Mitigation: WePLD request/decision contract wraps engines.
5. **Sandbox overclaim** — container/job/process controls may be called containment without evidence. Mitigation: capability-specific containment evidence and platform tests.
6. **Evidence explosion** — append-only timeline may become expensive. Mitigation: stable IDs, content addressing, tiered retention, derived indexes.
7. **External protocol churn** — MCP/ACP/AHP/A2A are evolving. Mitigation: adapters, version negotiation, no internal canonical data model defined by a transport.
8. **Licensing drift** — source licenses can change. Mitigation: exact pins, license blobs/notices at source-acquisition gate.
9. **Security graph false confidence** — incomplete static analysis can miss dynamic behavior. Mitigation: provenance/confidence/coverage labels and dynamic overlays.

## Architecture decision

Proceed with V2.3 candidate planning. Do not implement until owning future slices run their own Source Acquisition and dependency gates.
