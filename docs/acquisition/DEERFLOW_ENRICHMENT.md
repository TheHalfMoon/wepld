# DeerFlow — Bounded Source / Behavior Enrichment

## Classification

```text
SOURCE = bytedance/deer-flow
REGISTRY_V1_ID = SRC-0364
PIN = 1dd6ba1acb03700589994b0366c5d1c7d05e2eff
ROOT_LICENSE = MIT
CLASS = AGENT_HARNESS + EDARA + UWC + FEHREST + MISSION_RUNTIME + SCHEDULING + OBSERVABILITY + RECOVERY_ORACLE
TIER = S+
DISPOSITION = PORT_CANDIDATE | ADAPT_CANDIDATE | TEST_QUARRY | NEGATIVE_ORACLE | REFERENCE
CANONICAL_SOURCE_REGISTRY_V1_CHANGE = 0
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

DeerFlow already exists in the frozen registry V1 as `SRC-0364`. This record enriches that existing source; it does not create another named entry or rewrite the 402-entry restoration artifact.

## Rights / provenance state

The pinned root license is MIT. Root licensing does not establish the rights or suitability of every transitive dependency, bundled skill, model/provider integration, remote service, or generated artifact.

```text
ROOT_LICENSE_ESTABLISHED = MIT
TRANSITIVE_RIGHTS_AUDIT = INCOMPLETE
PATH_LEVEL_RIGHTS_AUDIT = REQUIRED_BEFORE_REUSE
WHOLE_REPOSITORY_COPY = NOT_AUTHORIZED
```

## Pinned evidence anchors

```text
README.md
blob = 8444d5ec5e1d52597852c47a2a63084b13c831de

LICENSE
blob = 9dc98a4a6b9b549447a4fc314e4cf50529c184c7

backend/packages/harness/deerflow/subagents/AGENTS.md
blob = daf4b0e0bd07e3c567e5aab7aef81f29e34d0557

frontend/src/content/en/harness/memory.mdx
blob = e0f4ea906c55c41ce000a0ba209cf72ba6c07b9a

backend/app/scheduler/service.py
blob = ffce4af6d253205ed81c50ccdd00de336d72fc60

backend/tests/test_scheduled_task_service.py
blob = 4874a0fb90604eeb28b8d90b219c60e06b882bfc
```

The pinned main commit also changes `backend/app/scheduler/service.py` and its tests to enforce the configured global concurrent-run budget for manual triggers, while explicitly documenting that the count is a non-atomic best-effort guard rather than a database-level global cap.

## WePLD capability mapping

```text
Edara           <- benefit-based delegation + minimum-useful-subagent policy + bounded concurrency/total-run budget
Mission Runtime <- durable run/delegation events + run ids + explicit terminal/error/cap reasons
UWC             <- model/provider seams + deferred MCP/tool promotion + subagent result envelopes
Fehrest         <- structured cross-session memory + per-agent isolation + bounded injection + durable context
S7 Assurance    <- step capture + error/status contracts + trace/evidence mechanics
S8 Recovery     <- durable event persistence + capped/partial-result surfacing + orphan/delivery recovery ideas
S9/S10          <- run/session/usage/feedback evidence as future non-authoritative learning inputs
```

## Positive mechanics worth mining

### 1. Ponytail-compatible subagent routing

DeerFlow's subagent policy defaults to direct execution and treats delegation as an optimization, not a reflex. It dispatches only when parallel latency, specialist capability, or context-isolation benefit exceeds startup, duplicate-discovery, synthesis, state-conflict, and side-effect costs. Overlapping mutable state and output dependencies veto parallel dispatch. The lead uses the fewest useful subagents and re-evaluates later batches.

This is strongly aligned with WePLD `PONYTAIL_MODE = FULL` and Edara minimum-sufficient topology.

### 2. Separate concurrency and total-run delegation budgets

The subagent system enforces both a simultaneous concurrency cap and a durable total-delegation budget per run. Exhausted slots remove further task calls and surface a visible limit condition rather than allowing unbounded repeated legal-sized batches.

Mine the mechanism and tests; do not inherit numeric defaults as WePLD policy.

### 3. Additive stop reasons instead of breaking status enums

Turn, token, and loop guardrails surface additive `stop_reason` values such as capped turns/tokens/loops while retaining backwards-compatible status values. Durable delegation records preserve the reason so a parent can distinguish a clean result from a capped partial result.

This is useful for Mission Runtime result envelopes and Assurance coverage.

### 4. Status derives from structured markers, not display prose

Provider/model exceptions may be converted into a terminal assistant message so the graph can end cleanly, but DeerFlow marks the fallback structurally and the executor maps the run to failed. Error-looking prose alone is not parsed as a status protocol.

WePLD should preserve the stronger general rule:

```text
DISPLAY_TEXT != EXECUTION_STATUS
```

### 5. Durable subagent step capture

DeerFlow captures assistant turns and every tool output from newly appended stream tails, persists bounded step events, uses lifecycle envelopes, supports task-scoped paging, and accounts for history contraction during compaction. This is a high-value Mission Runtime / Assurance test quarry.

### 6. Deferred tool discovery without permission widening

Deferred MCP/tool schemas can be discovered and promoted later, but runtime skill policy still blocks business tools omitted by the active skill. Discovery/promotion is explicitly separated from execution permission.

This aligns with:

```text
TOOL_DISCOVERED != TOOL_EXECUTION_AUTHORIZED
```

### 7. Structured cross-session memory with bounded injection

DeerFlow memory stores work/personal context, top-of-mind state, history, and facts; supports per-agent isolation; has a configurable injection token budget; and separates passive middleware extraction from experimental model-directed CRUD tools.

These are Fehrest behavior oracles, not Fehrest authority semantics.

### 8. Observability and support evidence hygiene

The setup/support flow creates redacted support bundles that intentionally exclude `.env`, raw conversation messages, and user file contents. Trace correlation can link HTTP responses, logs, and tracing systems. This is useful evidence/support UX material.

## Negative oracles / required WePLD divergence

```text
DEERFLOW_SUBAGENT_STATUS_COMPLETED != WEPLD_COMPLETION_DECISION
DEERFLOW_STOP_REASON = EVIDENCE, NOT ACCEPTANCE
DEERFLOW_TOOL_DISCOVERY != NAWAT_GRANT
DEERFLOW_MODEL_ROUTE != AUTHORITY
DEERFLOW_MEMORY_WRITE != FEHREST_CANONICAL_WRITE_AUTHORITY
DEERFLOW_SKILL_POLICY != UNIVERSAL_EFFECT_AUTHORITY
DEERFLOW_TRACE_ENABLED != EGRESS_AUTHORIZED
```

### Memory mutation cannot become model authority

DeerFlow's experimental tool mode exposes `memory_add`, `memory_update`, and `memory_delete` to the model. WePLD may mine CRUD UX/contracts, but model selection of a memory tool cannot authorize mutation of canonical Project Brain truth.

### Storage fallback is not safe for canonical Project Brain by default

DeerFlow documents that failure to load a configured custom memory storage class falls back to the default file storage and logs an error. That can be a useful availability choice, but WePLD must not silently substitute persistence semantics for acceptance-critical or authority-bearing Fehrest state.

```text
CANONICAL_STORAGE_UNAVAILABLE != SILENT_STORAGE_SUBSTITUTION
```

### Global concurrent-run admission is explicitly best-effort

At the pinned revision, the manual-trigger global concurrency guard counts active runs before dispatch but documents that the global limit is not enforced atomically at the database level. WePLD may use such a check as an optimization, but any admission invariant that affects authority, safety, or bounded resource guarantees requires an atomic or otherwise proven arbiter.

### Capped completion is not trusted completion

A subagent can end with normal `completed` plus a cap reason when it produced usable partial output. WePLD must preserve the reason and prevent such semantic completion from being promoted to `CompletionDecision` without the applicable acceptance contract.

### External tracing is egress

DeerFlow notes that some tracing paths capture prompts, tool arguments, outputs, timings, and token counts and may send them off-box. Any equivalent WePLD integration remains subject to `EXTERNAL_REVIEW_EGRESS_POLICY.md` or a future generalized telemetry-egress policy.

## Acquisition decision

Mine DeerFlow capability-by-capability rather than importing it as the WePLD runtime.

Priority path-mining order:

1. `backend/packages/harness/deerflow/subagents/` — Edara/UWC delegation budgets, status contracts, step persistence, tests;
2. lead/subagent middleware assembly — context isolation, deferred tool promotion, loop/token/turn guards;
3. `backend/packages/harness/deerflow/agents/memory/` — Fehrest memory storage/update/injection boundaries and negative fallbacks;
4. scheduler service/repository paths — bounded scheduling, leases, overlap and global-budget race tests;
5. run-event/delivery/trace paths — Mission Runtime evidence and recovery;
6. support-bundle/redaction paths — operator evidence hygiene.

No source, dependency, skill, model, provider, sandbox, memory backend, tracing service, or scheduler implementation is admitted by this document.
