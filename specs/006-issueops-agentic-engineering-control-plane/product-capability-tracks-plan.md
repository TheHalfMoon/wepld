# Product Capability Tracks — Cross-Slice Plan

```text
STATUS = FUTURE_PLANNING_ADDENDUM
TRACKS = PX_WK_AU_IS
ROADMAP_NUMBERING = UNCHANGED
NEW_SUBSYSTEM = NONE
IMPLEMENTATION_AUTHORITY = NONE
```

This plan integrates Project Experience, Work, Automations/Connections, Browser/WebMCP, and Computer Use into the existing P0 + S1..S10 architecture without creating a second control plane.

## 1. Architectural clarification

The parent `plan.md` diagram contains a `Workflow Engine` box. For this capability track, that phrase MUST be interpreted as workflow intent/planning/definition mechanics feeding the existing Edara/Mirefa/Nawat/Mission Runtime chain. It MUST NOT be interpreted as a second durable execution/orchestration engine.

```text
WORKFLOW_DEFINITION != ORCHESTRATION_RUNTIME
AUTOMATION != SECOND_MISSION_RUNTIME
AUTOMATION_RUN_UI = MISSION + ASSIGNMENT/ATTEMPT + EVIDENCE
```

If future parent-plan wording is revised, it should prefer `Workflow Intent / Planning` over `Workflow Engine` unless a separately justified primitive is actually required.

## 2. Product information architecture

Recommended primary surfaces:

```text
Projects
Work
Automations
```

Recommended supporting surfaces/capabilities:

```text
Connections / Integrations
Browser
Computer
Artifacts
Evidence
```

`WebMCP` remains a route inside Browser. Internal architecture names such as Mirefa and Nawat should remain inspectable for advanced evidence/debugging but are not required as ordinary navigation labels.

## 3. Track definitions

### PX — Project Experience

Goal: make Fehrest-backed project context usable as a durable product surface without building another memory/truth store.

Owning progression:

```text
S2 identity/storage foundation
-> S4 Fehrest/Project Brain
-> later S10 cross-project intelligence
```

### WK — Work Plane

Goal: provide one durable interactive session/evidence surface across local/cloud clients, workers, attempts, tools, browser/computer interaction, approvals, and artifacts.

Owning progression:

```text
S3 host/effect foundations
-> S6 Mission Runtime/UWC/Edara/Mirefa/Nawat interoperability
-> S9 durable continuation/recovery
```

### AU — Automations and Connections

Goal: convert qualified schedules/events/conditions into Missions and expose typed integration capabilities without creating a parallel workflow runtime or ambient credential authority.

Owning progression:

```text
S5 declarative intent/workflow planning
-> S6 connector/route qualification
-> S8 bounded effectful automation
-> S9 durable waits/recovery
-> S10 outcome analytics
```

### IS — Interactive Surfaces

Goal: provide one governed abstraction for Browser and Computer interaction, preferring semantic/structured routes over pixels/raw input and binding every effect to fresh observations and effect-time authority.

Owning progression:

```text
S3 host/process/effect foundations
-> S6 interactive-surface/route interoperability
-> S7 qualification/security benchmarks
-> S8 bounded actuation
-> S9 recovery/remote continuation
```

## 4. Slice mapping

### S1 — Desktop ↔ Rust Trusted Core

No scope expansion.

Projects/Work/Automations/Browser/Computer planning MUST NOT pull agent-host, connector, browser, network, or computer-control complexity backward into S1.

### S2 — Open Project + Project Doctor + local identity/storage

Preserve current S2 scope.

```text
S2_PROJECT_IDENTITY_FOUNDATION != GENERALIZED_PROJECT_EXPERIENCE
S2_STORAGE_FOUNDATION != FEHREST_PROJECT_BRAIN
```

No generalized Projects, Automations, Browser, Computer Use, connector execution, cloud Work, or S3+ capability is activated by this plan.

### S3 — Terminal Fabric + trusted process ownership

Future-facing foundations required by later tracks:

- effect proposal/result envelopes;
- host/process-tree identity;
- capability observation;
- containment reporting;
- bounded cancellation;
- ownership/fencing prerequisites where process/input ownership exists;
- Nawat enforcement seam without pulling the full later policy engine backward.

S3 does not implement a product-level automation engine.

### S4 — Fehrest Minimum / Project Experience foundation

PX may add, under separately granted S4 authority:

- provenance-aware project context classes;
- project instructions as non-authoritative context;
- source/generation freshness;
- project knowledge/artifact references;
- Work/Automation association references;
- ConnectionBinding references without raw secrets;
- product views over Fehrest truth rather than a second project memory store.

### S5 — Spec/plan qualification + Automation planning foundation

AU may add, under separately granted S5 authority:

- `AutomationDefinition`;
- `TriggerDefinition`;
- trigger-to-WorkflowIntent/Mission compilation contracts;
- required/preferred/forbidden route constraints;
- capability requirements;
- dry-run/explanation;
- declarative visual-flow UX that compiles to intent/topology constraints rather than becoming runtime topology itself.

```text
VISUAL_FLOW != RUNTIME_TOPOLOGY
AUTOMATION_DEFINITION != EXECUTION_AUTHORITY
SCHEDULE_FIRED != EFFECT_AUTHORITY
```

### S6 — UWC + Mirefa + Edara + Nawat / Work and Interactive interoperability

WK/AU/IS may add, under separately granted S6 authority:

- durable `WorkSession` semantics;
- `CapabilityPresence` observations;
- integration/connector adapter contract;
- `ConnectionBinding` and bounded credential-capability resolution;
- `ManagedBrowser` adapter candidate;
- `InteractiveSurface`;
- route hierarchy and route constraints;
- WebMCP adapter candidate as an untrusted browser route;
- local/cloud capability distinction;
- effect-time Nawat mediation for connector/browser/computer actions;
- explicit route migration/requalification rather than silent fallback.

### S7 — Native Assurance / AMAN qualification

Add qualification/evaluation plans for:

- connector supply-chain and secret/network behavior;
- webhook authenticity/replay/deduplication;
- WebMCP hostile tool descriptions/schemas/output;
- browser prompt injection and origin/navigation drift;
- stale-target and stale-surface races;
- attached-user-browser credential blast radius;
- Computer Use action safety and input-lease behavior;
- BrowserGym/WebArena/WorkArena-class browser evaluation;
- OSWorld-V2-class desktop evaluation;
- negative oracles for high-consequence actions and unknown outcomes.

### S8 — Controlled Repair / bounded effectful capability activation

Only after prerequisite qualification and explicit owning authority, S8 may activate:

- bounded Automation execution;
- bounded Browser actuation;
- bounded Computer Use;
- human approval through the existing Nawat path;
- effect reconciliation;
- proven idempotent/replay-safe execution where the exact effect contract supports it;
- controlled repair without ambient escalation.

No automation, browser, or computer capability receives a private approval/authority engine.

### S9 — Quality Passport / Recovery Time Machine / durable continuation

Add:

- long-lived scheduled/event-driven Missions;
- Work continuity across clients;
- host/worker loss recovery;
- capability loss/recovery evidence;
- route migration with requalification;
- browser/computer recovery checkpoints where proven safe;
- automation run history mapped to Mission/Attempt/effect evidence;
- browser/computer/connector effect reconciliation history.

### S10 — Fehrest expansion / outcome intelligence

Add:

- route reliability history;
- automation outcome analytics;
- capability success/failure/reconciliation evidence;
- cross-project reusable patterns;
- benchmark-informed route recommendations;
- Byan recommendations that never become authority.

## 5. Capability maturity model

The tracks should mature gradually rather than jump from discovery to ambient autonomy.

```text
LEVEL 0 — DISCOVER
LEVEL 1 — OBSERVE
LEVEL 2 — PROPOSE
LEVEL 3 — ACT WITH EXPLICIT APPROVAL
LEVEL 4 — ACT UNDER SCOPED AUTHORITY
LEVEL 5 — DURABLE AUTONOMOUS EXECUTION
```

These levels describe qualified product/runtime maturity only.

```text
MATURITY_LEVEL != AUTHORITY
AUTONOMY_MODE != AUTHORITY
```

A Level 5 capability still requires valid current qualification, effect-time authority, containment, and evidence for each applicable effect class.

## 6. Recommended build order

Subject to canonical slice authority, the safest useful ordering is:

1. Project Experience over Fehrest-backed context;
2. Work as the unified user-facing session/evidence surface;
3. Connections with read-only/low-effect integration capabilities first;
4. Managed Browser observation/read paths;
5. bounded Browser actuation + WebMCP after Nawat/AMAN prerequisites;
6. Automations after durable Mission triggering/waits/recovery are available;
7. Computer Use after InteractiveSurface, freshness, input lease, containment, and assurance are proven;
8. ambient multimodal/Astra-like behavior only as a later separately justified program.

This order is not implementation authority and must not override the canonical task frontier.

## 7. Route selection model

Mirefa qualifies routes. It does not authorize effects.

For equivalent semantics, prefer the least ambient, most structured qualified route.

Browser preference:

```text
Native Integration/API
> WebMCP
> Semantic Browser
> Browser Protocol
> Visual Grounding
> Raw Pointer/Keyboard
```

Arbitrary application preference:

```text
App-native Integration/API
> OS Accessibility/Automation
> Structured Application Surface
> Visual Grounding
> Raw Pointer/Keyboard
```

Route preference is not an unconditional fallback chain. The plan may state:

```text
preferred_routes[]
required_routes[]
forbidden_routes[]
```

If the required route is unavailable/unqualified, fail visibly rather than silently changing semantics.

## 8. Local/cloud continuation

Work continuity is user-facing continuity, not proof that capabilities moved between hosts.

A cloud continuation may preserve WorkSession/Mission context while losing local filesystem, local browser, attached-user-browser, local application, or local input capabilities.

```text
CLIENT_DISCONNECT != MISSION_FAILURE
CLOUD_CONTINUATION != LOCAL_CAPABILITY_CONTINUATION
REMOTE_BROWSER_STATE != LOCAL_BROWSER_STATE
```

Any route migration that could affect state, credentials, origin, effect semantics, or assurance must record reconciliation + requalification and revalidate pending authority where required.

## 9. Deployment/scaling model

The track names do not imply microservices. Early implementations should remain co-located where that is minimum sufficient, provided typed ownership boundaries remain enforceable and observable.

Separate processes/services become justified only by actual needs such as:

- containment/isolation;
- remote host lifecycle;
- browser/computer session ownership;
- long-lived scheduling/waits;
- independent scaling/failure domains;
- credential broker isolation;
- provider lifecycle constraints.

```text
ARCHITECTURAL_BOUNDARY != MICROSERVICE_REQUIREMENT
```

## 10. Shared primitives proposed for later qualification

Candidate primitives justified by cross-feature reuse:

```text
AutomationDefinition
IntegrationDescriptor
ConnectionBinding
TriggerEnvelope
CapabilityPresence
InteractiveSurface
InputLease
```

`RouteConstraint` should begin as a planning contract field rather than a new durable entity unless implementation proves a separate identity/lifecycle is necessary.

Do not create:

```text
AutomationRuntime
BrowserAuthority
ComputerAuthority
ConnectionAuthority
BrowserEvidenceStore
AutomationEvidenceStore
ComputerEvidenceStore
ProjectMemoryDatabase
```

## 11. Evidence convergence

All product surfaces should converge on one Work/Case evidence timeline where the events are relevant to the same work:

```text
intent
context retrieval
plan/topology
route qualification
authority decision
terminal/connector/browser/computer effect
post-effect observation
finding/review
repair/reconciliation
artifact
completion
```

Observability exports may exist, but no capability track creates canonical truth outside the WePLD evidence model.

## 12. Exit criteria from planning into an owning slice

A track may move from future planning into implementation planning only after:

1. its owning canonical slice is active and grants exact scope;
2. the relevant contract/primitives pass Ponytail FULL/minimum-sufficient review;
3. source/dependency candidates pass the applicable Source Acquisition gate;
4. failure/security/distributed semantics are defined before happy-path implementation;
5. deterministic test/negative-oracle strategy is ready;
6. no new authority or runtime subsystem is introduced implicitly.
