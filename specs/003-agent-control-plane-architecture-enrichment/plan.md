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

Deliver:
- `docs/acquisition/WEPLD_AGENT_CONTROL_PLANE_MAJOR_RECONNAISSANCE_2026-08-24.md`;
- focused addenda when new high-value sources materially change an acquisition or architecture decision, including `docs/acquisition/WEPLD_TRAE_AGENT_RECONNAISSANCE_2026-08-24.md`.

Product-reference and open-source-source surfaces must be classified separately. Do not infer that a commercial product's implementation is represented by a separately published open-source agent or SDK.

## Phase 2 — Architecture synthesis

### Work plane
Adopt evidence-timeline semantics: stable session/chat identities, append-only/replayable engineering actions and results.

Use current agent products such as TRAE only as UX/reference evidence for visible autonomy modes, inspectable subagent/team topology and integrated editor/browser/terminal/document work surfaces. Product UX never defines canonical evidence semantics.

### Mission Runtime / Edara
Plan provider-neutral host; provider-native SDK identities remain opaque. Use capabilities, not provider switches.

Path-mine multiple independent harness quarries rather than selecting one agent wholesale. VS Code Agent Host/AHP, Codex/DeepSeek Harness and Trae Agent provide complementary evidence for session ownership, event/trajectory recording, tool/provider seams, bounded step loops, recovery and containment routing.

Any donor pattern that routes model output directly to a tool executor is a negative authority oracle: WePLD inserts host-owned effect proposal + Nawat decision before effect execution.

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

Use code-graph-rag/Graphify as positive structural quarries and Trae Agent's local CKG as an additional lightweight-index/failure oracle. In particular, Fehrest freshness must be content/object-addressed; dirty-file provenance must not depend only on Git status strings, mtimes or file sizes.

### AMAN
Plan deterministic, structural, graph/data-flow, model-assisted and dynamic evidence layers.

### Assurance
Plan parallel independent evaluators, confidence as metadata only, finding reconciliation, and bounded candidate-generation/test-time-scaling experiments. Trae Agent's generation/pruning/patch-selection research is a quarry for search/evaluation mechanics only:

```text
SELECTOR_SCORE != TRUTH
ENSEMBLE_VOTE != AUTHORITY
PATCH_SELECTION != TRUSTED_COMPLETION
```

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
6. Codex/DeepSeek Harness;
7. ByteDance Trae Agent — bounded mining of agent loop, trajectory, CKG, Docker/tool seams and patch-selection/evaluation mechanics only; whole-project adoption is not selected.

Reference-only product surfaces:
- TRAE/trae.ai current IDE/SOLO/Work behavior and agent-team UX;
- Claude Code under its current repository terms;
- CodeQL in Spec 003 as a security oracle/evaluation surface;
- other commercial products unless an exact separately licensed source surface is established.

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

For agent/harness candidates additionally require:
- model/provider credential and network surface inventory;
- tool/MCP/process-effect inventory;
- trajectory/replay integrity model;
- containment versus authorization separation;
- provider/session identity versus WePLD Work identity mapping;
- evidence of cleanup/cancellation/concurrency behavior.

For code-intelligence candidates additionally require:
- exact freshness/content-identity semantics;
- dirty-worktree behavior;
- language/construct coverage declaration;
- incremental update/rebuild semantics;
- unknown/stale evidence behavior.

## Phase 5 — Qualification of planning candidate
- Foundation exact-head check.
- Trusted-base `s1-admission-integrity` exact-head check against the same candidate head; Foundation alone is insufficient.
- Documentation/specification changed-file scope check.
- If an external reviewer is used, exact-head egress preflight before review trigger.
- Independent engineering review, with `REVIEW_BLOCKED` recorded if an independently qualified reviewer is unavailable.
- Findings reconciliation.
- After any repair or reconnaissance addition that changes the head, rerun both deterministic checks and obtain a fresh independently qualified correctness/engineering review of the exact new head regardless of whether that review is internal or external. If the rereview is external, repeat the exact-head egress preflight before triggering it. If no independently qualified reviewer is available, record `REVIEW_BLOCKED` and stop qualification.
- Final live-evidence race over current PR/base/head/changed-file/check/review state, including both deterministic check results and the exact unresolved-material-findings value.
- No implementation, source admission, dependency admission, donor execution or canonical-index mutation.

## Implementation sequencing impact

No immediate implementation is authorized. Future slice order remains S2→S10; each new gate activates only within the owning slice after that slice's own Spec Kit/Ponytail/Source Acquisition.

Trae-specific impact without renumbering:
- S4-G may use Trae CKG as a freshness/coverage negative oracle and local-index quarry;
- S6-AH may mine Trae agent-loop/trajectory/tool/Docker seams alongside VS Code/Codex/DeepSeek harness sources;
- S7-S/Assurance may evaluate candidate generation/pruning/patch selection as advisory search mechanics;
- S9-P may reuse trajectory field ideas while preserving append-only/content-addressed WePLD evidence.
