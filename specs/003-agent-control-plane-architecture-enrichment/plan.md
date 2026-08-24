# Plan — Spec 003 Agent Control Plane Architecture Enrichment

## Phase 0 — Trusted baseline
- Bind to canonical V2.2/main.
- Keep active acquisition/runtime PRs separate.
- Treat candidate governance text as non-authoritative until a separately governed canonicalization event.
- Do not mutate `docs/canonical/MASTER_PLAN_INDEX.md` in this ordinary planning PR; trusted integrity policy classifies it as base-controlled and requires a separately governed bootstrap/override event for legitimate future mutation.

## Phase 1 — Major reconnaissance
Research five planes:
1. agent/session interoperability;
2. semantic code intelligence;
3. policy/effect governance;
4. containment/runtime;
5. evidence/provenance/assurance.

Deliver `docs/acquisition/WEPLD_AGENT_CONTROL_PLANE_MAJOR_RECONNAISSANCE_2026-08-24.md`.

## Phase 2 — Architecture synthesis

### Work plane
Adopt evidence-timeline semantics: stable session/chat identities, append-only/replayable engineering actions and results.

### Mission Runtime / Edara
Plan provider-neutral host; provider-native SDK identities remain opaque. Use capabilities, not provider switches.

### UWC
Define adapter families:
- ACP-compatible coding-agent adapter;
- MCP-compatible tool/resource adapter;
- native UWC adapter;
- later A2A external peer adapter.

### Mirefa
Qualify capabilities/routes based on declared and observed evidence. Never authorize effects.

### Nawat
Define effect proposal snapshot, decision, approval/transform/requalify behavior, expiry and revalidation. Keep host enforcement point external to workers.

### Fehrest.Maemar
Plan syntax + semantic-index + normalized graph + dynamic overlays. No graph database selection in Spec 003.

### AMAN
Plan deterministic, structural, graph/data-flow, model-assisted and dynamic evidence layers.

### Assurance
Plan parallel independent evaluators, confidence as metadata only, and finding reconciliation.

## Phase 3 — Roadmap amendment candidate
Create a non-canonical V2.3 candidate preserving P0 + S1..S10 and proposing:
- S4-G semantic graph gate;
- S6-AH agent-host interoperability gate;
- S6-N Nawat authority gate;
- S7-S AMAN security graph gate;
- S9-P execution provenance gate.

The candidate may be persisted for review without changing the canonical V2.2 index. Any future canonical-index mutation is a separate bootstrap/override event under trusted-base governance.

## Phase 4 — Acquisition work queue
Tier-1 path mining candidates:
1. VS Code Agent Host / AHP;
2. ACP;
3. Code-Graph-RAG + Graphify;
4. Microsoft ACS/AGT;
5. Cedar;
6. Codex/DeepSeek Harness.

Additional capability-triggered mining, deferred until the owning slice activates:
1. Tree-sitter/SCIP/ast-grep;
2. sandbox candidates;
3. Joern/CPG and OpenGrep;
4. OPA/OpenHands/Goose/Cline/Aider;
5. provenance/export candidates such as in-toto/SLSA/OpenTelemetry.

For each future path-mining gate require:
- exact commit/tree/file pins;
- exact license/notice analysis;
- source/test/failure-corpus inventory;
- dependency/runtime/network/provider surface inventory;
- portability/Windows assessment;
- maintenance/security history;
- replacement/exit strategy;
- minimum reuse decision.

## Phase 5 — Qualification of planning candidate
- Foundation exact-head check.
- Documentation/specification changed-file scope check.
- If an external reviewer is used, exact-head egress preflight before review trigger.
- Independent engineering review, with `REVIEW_BLOCKED` recorded if a required qualified review is unavailable.
- Findings reconciliation.
- Rerun affected checks and external-review preflight/review after any repair that changes the head.
- Final live-evidence race over current PR/base/head/changed-file/check/review state.
- No implementation, source admission, dependency admission, or canonical-index mutation.

## Implementation sequencing impact

No immediate implementation is authorized. Future slice order remains S2→S10; each new gate activates only within the owning slice after that slice's own Spec Kit/Ponytail/Source Acquisition.
