# Ponytail FULL — Spec 003

## Question: do we need a new universal internal protocol?
**No.** UWC remains a thin WePLD-owned contract; ACP/AHP/MCP/A2A adapters prevent reinvention.

## Question: do we need a custom parser for every language?
**No.** Acquire incremental parser/indexer machinery. Normalize facts behind Fehrest-owned schemas.

## Question: do we need a graph database now?
**No.** Define graph semantics first. Storage selection is deferred and replaceable.

## Question: do we need a custom policy language?
**Probably not initially.** Define Nawat request/decision semantics and evaluate Cedar/ACS/OPA machinery.

## Question: do we need a full cloud sandbox platform?
**No for initial Windows desktop.** Start with native Windows containment capabilities; keep gVisor/Firecracker/OpenSandbox/E2B as stronger remote tiers.

## Question: do we need a new telemetry backend?
**No.** Local canonical evidence first; OpenTelemetry is an export adapter.

## Question: do we need model-powered graph construction?
**No.** Canonical structural/semantic graph facts are deterministic/indexer-derived. Models may propose hypotheses only.

## Question: should we fork VS Code or Claude Code?
**No.** Acquire bounded machinery from permissive Code-OSS/AHP paths; Claude Code remains behavior reference-only.

## Minimum sufficient abstractions

1. `WorkEvent` / evidence envelope.
2. `WorkerAdapter` / UWC.
3. `CapabilityEvidence` / Mirefa.
4. `EffectProposal` + `AuthorityDecision` / Nawat.
5. `ProjectFact` + provenance / Fehrest.
6. `RiskFinding` / AMAN.
7. `ContainmentProfile`.
8. `AssuranceFinding`.
9. export adapters only where interoperability justifies them.

Anything beyond these requires slice-specific proof.
