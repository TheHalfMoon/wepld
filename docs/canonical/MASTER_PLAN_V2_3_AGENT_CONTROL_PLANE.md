# WePLD Master Architecture & Execution Plan — V2.3 Agent Control Plane

```text
STATUS = CANONICAL
PREDECESSOR_CANONICAL_PLAN = V2.2
PREDECESSOR_CANONICAL_BASE = 08a06e9f2664735eb55db5b2f49f95d3d3f91c3f
CANONICAL_PLAN_NAME = V2.3-AGENT-CONTROL-PLANE
ROADMAP_NUMBERING = UNCHANGED / P0 + S1..S10
ARCHITECTURE_REOPENING = BOUNDED_ENRICHMENT_ONLY
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
```

## Candidate thesis

WePLD remains a Universal Engineering Intelligence System. V2.3 makes explicit that its execution surface is a governed **Agent Development Control Plane**.

The control plane hosts replaceable workers and synchronized sessions while preserving a separate authority/evidence architecture:

```text
Work = durable session/evidence coordination
Mission Runtime = agent/process execution host
Edara = minimum-sufficient topology and staffing
UWC = normalized worker/protocol edge
Mirefa = capability/route qualification
Nawat = effect-time authority and revalidation
Fehrest = durable Project Brain
Fehrest.Maemar = semantic code/architecture intelligence
AMAN = security/risk evidence
Assurance = independent evaluation
Trusted Completion = governed completion decision
```

## Candidate invariants added to V2.2

```text
AGENT_PROTOCOL_PERMISSION != NAWAT_GRANT
AGENT_HOST_STATE != EFFECT_AUTHORITY
MCP_AUTHORIZATION != EFFECT_AUTHORITY
SANDBOX != AUTHORIZATION
CONTAINMENT != QUALIFICATION
GRAPH_FACT != AUTHORITY
RETRIEVAL_SCORE != TRUTH
TELEMETRY_SPAN != CANONICAL_EVIDENCE
REMOTE_AGENT_IDENTITY != TRUST
MODEL_REVIEW != SECURITY_COMPLETION
```

Existing V2.2 invariants continue to control.

## Protocol layering

```text
Client/session synchronization     AHP-like semantics
Coding-agent edge                 UWC + ACP-compatible adapter candidate
Tool/resource edge                UWC + MCP-compatible adapter candidate
External peer-agent edge          A2A candidate, later/non-primary
Provider-native APIs              behind worker adapters
Authority                         WePLD-owned Nawat only
```

No external protocol is required in S1–S3. Protocol compatibility enters only when its owning slice reaches Ponytail and Source Acquisition.

## Semantic Project Brain

Fehrest.Maemar is planned as a layered, provenance-first intelligence substrate:

1. repository/blob identity;
2. incremental Tree-sitter-class syntax facts;
3. SCIP-class precise semantic facts;
4. normalized code/property graph;
5. AMAN taint/resource/security overlays;
6. optional dynamic-runtime evidence;
7. optional retrieval/vector indexes.

Every graph fact must carry source/provenance/freshness sufficient to answer “why does WePLD believe this?” Missing or stale graph evidence is unknown, not truth.

## Agent Host

Mission Runtime must provide a provider-neutral host whose durable state is independent from any SDK session.

Required contracts:
- stable WePLD session/chat identities;
- opaque provider backing identities;
- capability descriptors instead of provider switches;
- append-only/replayable action/evidence envelopes;
- cancellation and recovery;
- multiple concurrent chats/subagents without leaking provider semantics;
- local-first persistence;
- no silent provider fallback.

The host records effects but does not authorize them.

## Nawat intervention model

Nawat must mediate effectful boundaries, with a candidate intervention vocabulary inspired by current open agent-governance work:

```text
SESSION_START
INPUT
PRE_MODEL
POST_MODEL
PRE_TOOL
POST_TOOL
OUTPUT
SESSION_END
```

The product may later refine this vocabulary, but the mandatory effect boundary is:

```text
proposed effect
 -> complete host snapshot
 -> Mirefa evidence
 -> Nawat decision/revalidation
 -> containment precondition
 -> effect execution
 -> post-effect evidence
```

The engine is preferably Rust-native. Cedar is the first policy-engine acquisition candidate. OPA/Rego remains an adapter candidate. Microsoft ACS is a specification/runtime quarry, not the owner of WePLD authority semantics.

## Containment strategy

Containment is platform-specific behind WePLD contracts.

Windows-first evaluation order:
1. native Process Sandbox / AppContainer and restricted capability model;
2. Job Objects, integrity/mitigation/process-tree controls;
3. Windows Sandbox/VM boundary when stronger separation is required.

Linux/remote evaluation:
1. OS/container baseline;
2. gVisor/runsc for application-kernel isolation where compatible;
3. Firecracker-class microVM boundary for hostile/high-risk execution;
4. OpenSandbox/E2B-class lifecycle API patterns for scalable remote workers.

The exact choice is deferred to the S3/S6 source-acquisition gate.

## Evidence Timeline

Work must preserve an append-only, queryable engineering timeline that links:
- intent and spec;
- context/retrieval facts;
- worker and session identity;
- proposed actions;
- authority decisions;
- tool/process side effects;
- ChangeUnits;
- tests and benchmarks;
- security/review findings;
- repairs/retries;
- final acceptance/completion evidence.

OpenTelemetry may export observational copies. in-toto/SLSA-inspired attestations may serialize signed provenance. The local canonical evidence model remains WePLD-owned.

## Revised roadmap interpretation

### P0 — Foundation
Unchanged. Governance, build method, source-acquisition discipline and authority separation remain root constraints.

### S1 — Desktop ↔ Rust Trusted Core
Unchanged. Do not pull agent-host/protocol complexity backward into S1.

### S2 — Open Project + Project Doctor + local identity/storage
Add:
- canonical project/repository identity;
- content/freshness primitives required by Fehrest;
- local evidence store foundations;
- no code graph yet.

### S3 — Terminal Fabric + trusted process ownership
Add:
- effect proposal/effect result envelope;
- process-tree identity;
- containment capability report;
- Nawat PEP seam without full policy engine;
- Windows-native containment investigation.
S3-D remains the deterministic assurance seed.

### S4 — Fehrest Minimum
Expand into **S4-G Semantic Project Graph Foundation**:
- incremental syntax facts;
- precise semantic-index adapter seam;
- normalized symbol/reference/call graph;
- provenance/freshness;
- graph diff;
- no model required for graph truth.

### S5 — Spec Kit + AGILLE + Plan Qualification + Ponytail
Add:
- graph-informed scope/blast-radius evidence;
- plan-to-symbol/file/contract references;
- retrieval is advisory;
- plan qualification never grants effects.

### S6 — UWC + Mirefa Minimum + Edara Minimum
Add two named gates:

**S6-AH — Agent Host Interoperability**
- provider-neutral Mission Runtime;
- AHP-like session state;
- ACP-compatible UWC adapter candidate;
- MCP tool adapter remains untrusted edge;
- append-only/replayable session events.

**S6-N — Nawat Effect-Time Authority**
- complete effect snapshot contract;
- allow/deny/approval/transform/requalify semantics;
- Cedar candidate evaluation;
- fail-closed unknown/malformed/stale evidence;
- authority expiry/revalidation;
- containment preconditions.

A2A remains optional future interoperability, not an S6 requirement.

### S7 — Native Review & Assurance
Add **S7-S AMAN Security Graph**:
- deterministic static rules;
- structural findings;
- graph/taint/resource reachability;
- change-aware attack-surface evidence;
- independent security reviewer adapters;
- findings never grant fixes automatically.

### S8 — Controlled Repair + Trusted Completion
Add:
- scoped effect grants for repair;
- replayable repair attempts;
- containment-aware execution;
- explicit reassignment/fallback evidence;
- no silent model/worker substitution.

### S9 — Quality Passport + Recovery Time Machine
Add **S9-P Execution Provenance & Evidence Timeline**:
- append-only action/effect timeline;
- signed/content-addressed evidence where applicable;
- attestation export profile;
- recovery checkpoints tied to ChangeUnits and authority decisions.

### S10 — Fehrest expansion + Byan
Add:
- dynamic graph evidence;
- cross-project architecture intelligence;
- historical outcome/benchmark analytics;
- Byan learns from outcomes but never authorizes.

## Candidate acceptance criteria

V2.3 may become canonical only if:
1. Spec Kit 003 is internally consistent and complete for planning scope.
2. Ponytail FULL shows the added contracts are minimum sufficient.
3. acquisition research differentiates source donor, protocol, reference-only and negative oracle.
4. no frozen registry evidence is silently rewritten.
5. current Pictorial/Agile work is not entangled with this amendment.
6. both the Foundation exact-head check and trusted-base `s1-admission-integrity` exact-head check pass and are recorded for the same candidate head.
7. at least one qualified independent engineering review examines the exact head.
8. all material findings are reconciled.
9. final diff changes planning/research only and grants no source/dependency/runtime authority.

## Explicit non-authorization

This candidate does not authorize implementation of Agent Host, code graph, Nawat engine, security graph, sandbox integration, protocol adapter, telemetry, remote agent execution, source import, or dependency admission.
