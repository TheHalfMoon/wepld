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

The parent `plan.md` diagram now names the `Intent / Plan Compiler`. Its earlier `Workflow Engine` label meant workflow intent/planning/definition mechanics feeding the existing Edara/Mirefa/Nawat/Mission Runtime chain. Neither label defines a second durable execution/orchestration engine.

```text
WORKFLOW_DEFINITION != ORCHESTRATION_RUNTIME
AUTOMATION != SECOND_MISSION_RUNTIME
AUTOMATION_RUN_UI = MISSION + ASSIGNMENT/ATTEMPT + EVIDENCE
```

Keep this owner terminology consistent across parent and addenda; a new execution primitive requires separate justification and cannot be introduced by a label change.

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

The Spec 006 planning package itself also requires the whole-scope exact-head independent review and explicit criteria disposition defined in `product-capability-tracks-acceptance.md` section J. A per-track exit cannot bypass that package gate. Minimum durable dispatch/reconciliation and enforced ownership precede the first consequential S8 effect; S9 remains the owner of extended recovery/audit work.

### User-visible failure handling

Work presents an actionable primary state with evidence-backed secondary reasons. `Outcome uncertain` suppresses blind retry even if transport is reconnecting. `Needs permission` identifies the exact account, target, proposed action/argument change, expiry and scope. `Cancel requested` stays distinct from proven cessation; an already sent action may still require reconciliation. `Completed` requires the Trusted Completion decision. Connection health is a separate fact and cannot overwrite work outcome.

Projects show source kind, provenance, current/historical status, scope and freshness as separate dimensions over Fehrest records. An external observation can also be stale or model-summarized; these are not mutually exclusive authority classes. Work timelines and supporting Browser/Computer panels use existing records. Automations become prominent when useful to the user's repeat work, without forcing a separate execution engine or ambient autonomy into the initial experience.

## 13. Roadmap prerequisite interpretation

P0 owns the canonical architecture/governance baseline; S1 owns the desktop/core trust boundary; active S2 owns qualified local Project identity/Doctor/storage only. S3 supplies trusted process ownership, effect envelope and Nawat enforcement seam; S4 supplies Fehrest/Maemar minimum; S5 supplies qualified intent/plan/topology. S6-AH supplies MissionRuntime/UWC interoperability, S6 supplies Mirefa/Edara, and S6-N supplies complete effect-time Nawat policy/authority. S7 supplies Native Assurance/AMAN, S8 controlled repair/Trusted Completion, S9 provenance/recovery history, and S10 Fehrest expansion plus Byan dynamic graph, cross-project and historical outcome intelligence.

Scheduling, federation, organization policy or cross-browser matrices mentioned under S10 in supporting task maps are conditional follow-on capabilities, not additions to canonical S10's required scope. Their security, identity, permission and compatibility prerequisites must exist before any earlier execution; they cannot be deferred to analytics. Minimum durable dispatch, dedupe, fencing, secret exclusion and reconciliation precede the first affected S6/S8 capability. S9 adds extended persistence/recovery qualification, not retroactive safety.

The task maps describe future implementation/qualification of the concrete contracts now defined here. Older verbs such as Specify/Define/Finalize mean implementing the contract under its owning slice and proving its acceptance fixtures, not leaving the present design unspecified. No future task checkbox is marked complete by this planning repair. Implementation requires the then-current canonical activation and exact scope.

## 14. Feature completeness matrix

This matrix concerns design readiness for future owning slices, not implementation authority or evidence that runtime fixtures have run. All rows remain **PARTIAL** until the final whole-package coherence/acceptance review closes their shared qualification gap. The exact sections below supply drafted design evidence; section 17 and the acceptance file define executable future oracles. A final disposition must not infer READY from this table's existence.

Abbreviations are document references within Spec 006: DM = `data-model.md`; AC = `contracts/automation-connections.md`; IS = `contracts/interactive-surfaces.md`; WB = `contracts/web-agent-boundary.md`; RD = `contracts/runtime-distributed-safety-addendum.md`; RF = `contracts/runtime-execution-fabric.md`; AF = `contracts/assurance-fabric.md`; RI = `contracts/review-independence.md`; RR = `contracts/retrieval-rag.md`. Requirements PCT-FR-* are in the product specification section 15. The three tables form one matrix keyed by Feature; shared dimensions are mandatory, not omitted.

| Feature / requirement | User problem / primary surface | Architectural owner / primitive type | Canonical contract / data-model owner | Intent source / qualification / authority |
|---|---|---|---|---|
| Projects / PCT-FR-PX | Know scope, applicable context and changes / Projects | Fehrest/Maemar / projection over S2 Project, KnowledgeSource and associations | RR; DM §§7–9,22 | explicit project/context request; access/freshness through RR and Mirefa for routes; context/instructions never authority, effects use Nawat |
| Work / PCT-FR-WK | Understand active work and decisions across clients / Work | MissionRuntime with Edara/UWC / WorkSession, Mission, typed control event | worker-delegation + RF/RD; DM §§15–19,23 | explicit controlling intent/objective revision; Edara topology -> Mirefa -> Nawat exact effect/approval |
| Automations / PCT-FR-AU | Repeat work predictably and inspect each run / Automations -> Work | Edara planning, MissionRuntime execution / immutable definition, typed trigger payload | AC §§2–4,16; AC owns its records, DM owns resulting intent/Mission | manual or qualified schedule/webhook/poll/provider/stream occurrence -> authenticated durable capture -> qualified intent; Mirefa/Nawat remain separate |
| Connections / PCT-FR-CN | Know which account can support which action / Connections in Project/Work | UWC adapters and RF credential broker, Mirefa/Nawat / descriptor, binding, derived capability | AC §§5–8,17–18; RF CredentialCapability | explicit account binding/action intent; schema/auth is evidence -> Mirefa behavior/route qualification -> Nawat operation and independent egress grant |
| Browser / PCT-FR-BR | Interact with web applications visibly / Browser inside Work | MissionRuntime/UWC adapter; Mirefa/Nawat / InteractiveSurface and Observation payloads | IS §§2–9,19; WB browser/session/context/artifact records | explicit Work/Automation effect proposal; exact semantic route/context qualification -> Nawat and current input/containment prerequisites |
| Computer Use / PCT-FR-CU | Complete bounded desktop/application work / Computer inside Work | MissionRuntime/UWC actuator; Mirefa/Nawat / typed surface identity, Observation, InputLease | IS §§10–20; RD ownership | explicit capability-scoped intent; platform/target/guarantee qualification -> Nawat -> enforcing input lease; manual OS permission alone is insufficient |
| WebMCP / PCT-FR-WM | Use a site's declared operation when semantics are proven / Browser, developer details | Browser interoperability adapter / untrusted observation and proposal projection | WB discovery/invocation/lifecycle; DM §19 canonical effect/decision | page declares capability only; user intent -> complete proposal -> WebRouteQualification -> Nawat; no self-granted page authority |
| Assurance / PCT-FR-AF | Know what is proved, missing or unsafe / Work evidence/review panels | Assurance Fabric, AMAN, Trusted Completion / engine evidence, Finding, ClaimAssessment, bundle | AF §§3–20, RI; DM §20 completion | explicit or policy-required assurance intent; qualified plan/engine/reviewer -> Nawat for effects; claims cannot authorize execution or completion |

| Feature | Execution / observation | Evidence required / recovery | Security / distributed model | UX / failure / developer experience |
|---|---|---|---|---|
| Projects | Fehrest projection/retrieval; source generation and access observations | exact source/location/content/access/freshness and history refs; rebuild derived projections, invalidate revoked lineage | RR/untrusted-content; DM §22 filtered associations/import; generation publication and causal source refresh | project context differences, stale/revoked/partial sources; §15 failures; fixtures for source/provider access, import remapping and conflict provenance |
| Work | Edara Assignments -> UWC Attempts; runtime event/control receipts | exact Server/Host/Runner/Worker/Attempt, objective/control revision, result and completion lineage; fence/reconcile before handoff/resume | RF/RD/RI; principal-scoped cursor and decision access; atomic control CAS, leases and causal replay | §16 states, active host/account/route and decision preview; §15 failures; deterministic control/replay/debug traces |
| Automations | compile definition to existing Mission topology; accepted occurrence/run events | pinned revisions, authentic occurrence/key, atomic intent association, branch/wait evidence and effect results; reconcile unknown outcomes, compensation as new effect | AC §§4,16 + RF/RD; tenant/source dedupe, backpressure, schedule clock bounds and persisted acceptance | preview/test label, missed-run/disabled/backlog/run history; §15 failures; typed bounded templates, simulated/live separation |
| Connections | UWC provider adapter with broker-mediated credential use; verified identity/provider observations | schema/version/account/scope/binding generation, derivation/use receipts, completeness and provider operation result; refresh/revoke/reconnect with generation CAS | AC §§17–18 + RF complete scope/HTTPS; no ambient secret/account fallback; cross-host refresh serialization and key retention | account/scopes/health distinct from permissions; §15 failures; SDK conformance and operation examples/anti-examples |
| Browser | qualified semantic/protocol adapter, separately permitted visual/input; exact frame/document snapshots | operation matrix IS §19, before/after target, grant/dispatch, bounded artifact/postcondition evidence; unknown results reconcile, no replayed click | IS profiles/credential privacy, WB egress/quarantine; RD fencing; navigation/context generation and explicit remote reconnect | action/route/account preview, takeover, stale/partial observation; §15 failures; protocol fixtures, operation matrix and trace viewer |
| Computer Use | qualified OS semantic/actuator route, bounded observation and serialized input | IS §20 exact incarnations/geometry/semantic/pixel evidence, lease/grant, postcondition/cleanup; no raw-event replay on reconnect | independent capture/input/clipboard scopes, protected UI refusal, RF/RD fencing and residual race limits | visible device/surface/control owner, takeover/cleanup uncertainty; §15 failures; platform conformance and deterministic synthetic race fixtures |
| WebMCP | Browser route invokes exact declared tool once under canonical effect dispatch; bounded inert output | declaration/protocol/schema/context/input/qualification/grant and outcome lineage; schema/revocation drift forces fresh proposal | WB hostile declaration parsing/prompt boundary, credential auth identity; canonical RD event/effect replay rules | normally hidden route detail, refusal explains unsupported/equivalence issue; §15 failures; local static hostile-tool fixture and schema version corpus |
| Assurance | admitted deterministic/model engines in RF envelopes; EngineRun and Finding observations | exact target and immutable policy, required-check coverage, independence, failure and conflicts; rerun/reassess stale evidence and independently review repairs | AF handling/egress/config trust; RD resource/lease/identity, bounded producer outputs and replay | supported/unsupported/insufficient/conflicting/stale claim distinct from completion; §15 failures; rule/plugin conformance, redacted diagnostics and exact-target negative corpus |

| Feature | Provider/source dependencies | Acceptance / task coverage | Roadmap / dependency gates | Non-goals / readiness / open gap |
|---|---|---|---|---|
| Projects | Claude/OpenAI product docs BEHAVIOR_ORACLE; Lily cache/benchmark TEST_ORACLE; RR source gates | PX-A; PX-001..006 | NEXT S4 after S2 identity; S5 planning, S9 history, S10 Fehrest/Byan | no ProjectMemoryDatabase or new S2 roots; PARTIAL: final coherence qualification pending |
| Work | OpenAI/Claude docs BEHAVIOR_ORACLE; OpenHands/Omnigent mechanisms ADAPT after admission | WK-A; WK-001..006, PCT-R002/003 | LATER S6 after S3–S5; S7 review, S8 completion, S9 continuity | no second Work runtime/ambient cloud migration; PARTIAL: final coherence qualification pending |
| Automations | n8n/Make/Zapier/Activepieces/Trigger.dev BEHAVIOR_ORACLE; Temporal SPEC_ORACLE | AU-A; AU-001..003,008..010, PCT-R001 | NEXT design S5, LATER S6 durable prerequisites -> S7 -> S8 effects -> S9 extended history | no extra scheduler/runtime dependency or unbounded script graph; PARTIAL: final coherence qualification pending |
| Connections | Zapier SPEC_ORACLE/BEHAVIOR_ORACLE/CLEAN_ROOM_REIMPLEMENT only; Activepieces bounded SDK ADAPT candidate after separate source gate; Nango broker BEHAVIOR_ORACLE; no source admission | CN-A; AU-004..007,011, PCT-A001, PCT-E001 | LATER S6 contracts/qualification -> S7 security -> S8 bounded effects | no generic plugin powers/account fallback/ambient credentials; PARTIAL: final coherence qualification pending |
| Browser | Playwright DEPENDENCY_CANDIDATE; BiDi/CDP SPEC_ORACLE; BrowserGym TEST_ORACLE | BR-A; IS-BR001..005,008..011, PCT-E002 | LATER S6 observation/interoperability -> S7 -> S8 controlled actuation; S9 qualified recovery | no profile sync or generic eval escape hatch; PARTIAL: final coherence qualification pending |
| Computer Use | platform accessibility SPEC_ORACLE; OSWorld/UI-TARS TEST_ORACLE; Astra PRODUCT_CLAIM only | CU-A; IS-CU001..011, PCT-A004, PCT-E003 | LATER S6 qualified observation/ownership -> S7 -> S8 bounded input; S9 recovery | ambient/mobile DEFERRED; global computer grant REJECTED; PARTIAL: final coherence qualification pending |
| WebMCP | evolving WebMCP draft SPEC_ORACLE; Browser dependencies separately gated | WM-A; IS-BR006/007, WEB-S6/S7/S8 task groups | LATER S6 Browser prerequisites -> S7 hostile corpus -> S8 exact effect | no trusted-page-tool shortcut or silent fallback; PARTIAL: final coherence qualification pending |
| Assurance | existing native assurance source matrix; exact engine admission and RI qualification | AF-A; PCT-A002/003/005/006, PCT-E004/005, AF/OH task maps | S3 deterministic seed -> S4 context -> S5 plan -> S6 engine envelope -> S7 assurance -> S8 repair -> S9 history | no clean-by-majority/CI completion/cache policy bypass; PARTIAL: final coherence qualification pending |

## 15. Failure-first cross-feature matrix

Every cell is a required behavior, including when the failure enters through an associated Work run, source, connector or assurance engine. It is not an assertion that every feature directly owns a host or credential. Compound cells require both behaviors. Canonical record ownership stays in the preceding matrix.

Codes: **B** block affected qualification/dispatch with an explicit reason; **O** preserve bounded partial/unknown observation and prohibit an absence/success claim; **S** invalidate affected identity/generation/access eligibility and re-observe/requalify; **F** fence ownership and queued effects at the enforcing sink, then reconcile; **D** causal dedupe/replay with key/payload conflict and gap detection, no re-execution; **R** preserve effect uncertainty/partial results, reconcile before retry or dependent irreversible work; **U** record user control change, stop queued input/work and require explicit fresh resume; **Q** quarantine untrusted content/artifact/config, with no instruction/authority promotion. B on an already dispatched effect additionally requires R. No code authorizes a retry.

| Failure | Projects | Work | Automations | Connections | Browser | Computer | WebMCP | Assurance |
|---|---|---|---|---|---|---|---|---|
| unavailable | O B | B R | B | B R | B R | B R | B | O B |
| unsupported | O B | B | B | B | B | B | B | O B |
| partial | O | O R | O R | O R | O R | O R | O R | O |
| stale | S | S | S | S | S | S | S | S |
| corrupt | Q O | Q B | Q B | Q B | Q B | Q B | Q B | Q O |
| ambiguous | O B | B R | B | B R | B R | B R | B | O B |
| conflicting | O B | D B | D B | D B | S B | S B | S B | O B |
| unauthorized | B | B | B | B | B | B | B | B |
| unqualified | B | B | B | B | B | B | B | O B |
| timeout | O | R | R | R | R | R | R | O B |
| cancelled | O | F R | F R | R | U R | U R | R | O B |
| offline | O S | F R | B D | B R | B R | F R | B R | O B |
| rate limited | O | B R | B D | B R | B R | B | B R | O B |
| provider failure | O S | R | R | R | R | R | R | O B |
| worker loss | O | F R | F R | F R | F R | F R | F R | O B |
| host loss | O S | F R | F R | F R | F R | F R | F R | O B |
| controller loss | O | F R | F R | F R | F R | F R | F R | O B |
| split brain | D B | F R | F D R | F R | F R | F R | F R | D B |
| lease expiry | S B | F R | F R | F R | F R | F R | F R | O B |
| fence loss | B | F B R | F B R | F B R | F B R | F B R | F B R | O B |
| replay | D | D | D | D | D R | D R | D R | D |
| duplicate event | D | D | D | D | D | D | D | D |
| out-of-order event | D O | D O | D O | D O | D O | D O | D O | D O |
| schema drift | S B | S B | S B | S B | S B | S B | S B | S O |
| credential expiry | S B | S B | S B | S B | S B | S B | S B | S B |
| credential revocation | S B | S B | S B | S B | S B | S B | S B | S B |
| permission change | S B | S B | S B | S B | S B | S B | S B | S B |
| unknown effect outcome | O R | R | R | R | R | R | R | O R |
| irreversible partial completion | O R | R | R | R | R | R | R | O R |
| user takeover | S U | U R | U R | U R | U F R | U F R | U R | U O |
| browser navigation race | S O | S R | S R | S R | S R | S R | S R | S O |
| stale browser snapshot | S O | S B | S B | S B | S B | S B | S B | S O |
| stale desktop surface | S O | S B | S B | S B | S B | S B | S B | S O |
| download hazard | Q | Q B | Q B | Q B | Q B | Q B | Q B | Q O |
| prompt injection | Q | Q B | Q B | Q B | Q B | Q B | Q B | Q B |
| policy injection | Q B | Q B | Q B | Q B | Q B | Q B | Q B | Q B |
| tool-schema injection | Q B | Q B | Q B | Q B | Q B | Q B | Q B | Q B |
| supply-chain compromise | Q B | Q B | Q B | Q B | Q B | Q B | Q B | Q B |

Fencing means a proved enforcing sink rejects the old epoch. If enforcement or old-owner cessation cannot be proved, the system refuses replacement actuation; it cannot claim F succeeded. Read-only consumers of an affected operation expose its uncertainty and stale evidence rather than acquire execution powers. Provider rate limits use finite budgets/retry-after; offline snapshots remain access-checked historical evidence, not current qualification.

## 16. Unified UX, security and developer obligations

Projects / Work / Automations remain the top-level information architecture. Connections is a reusable account-management surface; Browser and Computer are Work panels. WebMCP is usually hidden route detail. Each view links to the same Work/evidence records and preserves access filters. Ordinary labels explain the action and next decision without requiring knowledge of internal owner names.

| State | Evidence and permitted next action |
|---|---|
| READY | prerequisites observed current; starting still requires effect-time qualification/authority |
| RUNNING | identified active Attempt and route; show host/account, progress and bounded cancellation |
| WAITING | declared dependency, schedule or durable wait and next wake condition; not an approval |
| NEEDS_APPROVAL | exact proposed operation/account/target/input/scope/expiry; submit decision evidence to Nawat |
| BLOCKED | named failed prerequisite; repair that prerequisite and requalify |
| UNSUPPORTED | route/capability/version lacks a qualified implementation; choose an explicitly reviewed alternative |
| PARTIALLY_OBSERVED | bounded/truncated/incomplete observation with missing scope; do not infer absence |
| STALE | changed identity/generation/access/policy; refresh and requalify affected work |
| RECOVERING | identified recovery/reconciliation action and prior attempt lineage; no blind effect replay |
| OUTCOME_UNCERTAIN | sent effect lacks a proved outcome; reconciliation action only, generic Retry disabled |
| FAILED | proved failure with known/unknown effect details; retry offered only with canonical retry-safety evidence |
| CANCEL_REQUESTED | cessation requested, still pending proof; retain reconciliation for sent effects |
| CANCELLED | cessation/cleanup proved for execution; any unresolved external outcome stays visible separately |
| COMPLETED | current Trusted Completion decision with supporting claims/coverage/findings and exact evidence |

The primary state is deterministic: OUTCOME_UNCERTAIN takes precedence for any unresolved consequential effect, then CANCEL_REQUESTED, then blocking/unsupported/stale/partial prerequisites, then pending approval/wait/recovery, then running/ready; terminal FAILED/CANCELLED/COMPLETED appear only when their evidence exists. Orthogonal reasons and lifecycle details remain visible. Conflicting terminal evidence produces BLOCKED/conflict, not last-write-wins. A cancelled Attempt with an unknown external effect therefore shows Outcome uncertain plus Cancelled execution. Capability panels cannot overwrite a Mission's completion state.

Security applies at each boundary: project/repository/Git/terminal/model content is untrusted data; source parsers, archives and downloads are bounded and inert; filesystem/process/network/browser/clipboard/input are separate effect classes; credentials/OAuth/cookies/profiles stay brokered and classified; connectors, tools, plugins and engine updates require admission and exact identity. Remote/cloud workers require authenticated host ownership, containment and explicit egress. Cross-tenant/project scope is checked at lookup, association, context assembly, dispatch, replay and export; UI hiding is insufficient. Instruction/schema/risk annotations cannot edit policy or combine request, qualification, authority, execution, review and completion powers. Existing untrusted-content, RF, RD, AF and RI contracts own enforcement and evidence; this is not a new policy engine.

Developer workflows provide versioned typed schemas, local synthetic providers/surfaces, deterministic replay, exact operation preview, bounded redacted diagnostics, fixture import and compatibility reports. Browser/Computer adapters prove target/lease enforcement with platform-specific conformance, not just a demo. Connector and assurance extensions have immutable package/protocol identities, declared effects, budgets and update qualification. Debug views expose scope/generation/route/claim lineage without dumping secrets, raw environment or private browser state. Acceptance fixtures in section 17 are required SDK examples and anti-examples; measured benchmark success never authorizes an operation.

## 17. Dependency-ordered traceability and evidence expectations

The rows below are bidirectional: every listed task implements its row's requirement under the named owners in section 14 and must satisfy its acceptance family. Future task ranges are inclusive; supporting cross-cutting/source tasks additionally inherit PCT-FR-X. No runtime checkbox is completed by drafting this mapping.

| Requirement | Concrete future tasks in product-capability-tracks-tasks.md | Acceptance in product-capability-tracks-acceptance.md | Required dependency / evidence |
|---|---|---|---|
| PCT-FR-PX | PX-001..006 | PX-A | S2 identity -> S4 source access/generation -> projection/retrieval; exact membership and revoked-source conflict/import fixtures |
| PCT-FR-WK | WK-001..006; PCT-R002/003 | WK-A | S3 process -> S5 intent -> S6 RF/RD control -> S9 continuation; concurrent-client CAS, pause/cancel proof, handoff fence and cursor gap receipts |
| PCT-FR-AU | AU-001..003, AU-008..010; PCT-R001 | AU-A | S5 definition compiler -> S6 durable occurrence/intent and safety -> S7 -> S8 effects; revision edit replay, DST/misfire, crash capture and approval-expiry fixtures |
| PCT-FR-CN | AU-004..007, AU-011; PCT-A001; PCT-E001 | CN-A | descriptor/admission -> binding/broker -> read-only qualification -> effect qualification; account/refresh/revocation/HTTPS/pagination/idempotency receipts |
| PCT-FR-BR | IS-BR001..005, IS-BR008..011; PCT-E002; PCT-R004 | BR-A | S6 exact Browser observation -> S7 operation/security corpus -> S8 grants/input -> S9 safe checkpoints; each IS §19 operation has success, stale-target and refused-route fixture |
| PCT-FR-CU | IS-CU001..011; PCT-A004; PCT-E003; PCT-R004 | CU-A | S6 identity/lease/observation -> S7 platform corpus -> S8 actuation -> S9 recovery; resize/DPI/handle reuse/focus/takeover/protected UI and old-owner fixtures |
| PCT-FR-WM | IS-BR006/007; supporting web-agent-tasks.md S5/S6/S7/S8 groups | WM-A | Browser prerequisites -> bounded declaration observation -> semantic equivalence -> Mirefa -> Nawat; hostile schema/collision/revocation/navigation/input mismatch fixtures |
| PCT-FR-AF | PCT-A002/003/005/006; PCT-E004/005; PCT-R005/006 | AF-A | exact AF target/policy + RF engine envelope -> S7 qualified checks/review -> S8 repair/TC -> S9 history/S10 analytics; all-product claim/effect mapping, policy-cache invalidation, non-clean results and stale-review fixtures |
| PCT-FR-X | PCT-P001..007; PCT-S001..007; all rows above | X-A; sections A–J | planning coherence then canonical activation, source/admission gates before dependency use, §15 all failures and §16 all states; exact-head qualified independent whole-scope review before planning merge |

Special dependency edges: AU-005 and AU-008 precede PCT-E001; IS-BR001/002/005/008 and PCT-A002/003 precede PCT-E002; IS-CU001..008 and PCT-A004 precede PCT-E003. All PCT-E tasks require complete RF/RD/credential/privacy prerequisites and S7 qualification. PCT-R tasks add historical/recovery qualification after the minimum safe runtime, not before it. PCT-S admission tasks precede actual imported code/dependencies; their research oracles alone grant nothing. PX-006 and IS-CU011 are explicit deferral guards, not hidden implementation requirements.
