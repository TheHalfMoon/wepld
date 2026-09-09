# Product Capability Tracks — Ponytail FULL

```text
STATUS = FUTURE_PLANNING_PONYTAIL_FULL
SCOPE = PROJECTS_WORK_AUTOMATIONS_CONNECTIONS_INTERACTIVE_SURFACES
IMPLEMENTATION_AUTHORITY = NONE
```

Question: what is the minimum architecture sufficient to deliver the proposed user value without duplicating WePLD's existing control plane?

## 1. New top-level Connect subsystem

**Reject.**

User value is better represented by `Automations` plus supporting `Connections / Integrations`. A `Connect` subsystem would blur integration definition, authenticated binding, credentials, routing, execution, and authority.

## 2. Separate Automation Runtime

**Reject.**

Automations should compile triggers/definitions into Missions and reuse Edara/Mirefa/Nawat/Mission Runtime. A second scheduler/workflow executor would duplicate attempts, retries, recovery, evidence, and authority-adjacent semantics.

## 3. AutomationRun as mandatory canonical execution entity

**Defer.**

Use a UI/query projection over AutomationDefinition revision + TriggerEnvelope + Mission/Assignments/Attempts first. Add a durable entity only if implementation proves independent lifecycle/identity semantics.

## 4. Separate Browser authority/approval engine

**Reject.**

Browser effects consume Mirefa qualification and Nawat authority like other effects.

## 5. Separate Computer authority/approval engine

**Reject.**

Computer actuation consumes the same authority chain. `InputLease` is an ownership/execution precondition, not a competing authority system.

## 6. Browser and Computer as one product feature

**Reject.**

They share `InteractiveSurface` identity/freshness mechanics but have different user expectations, routes, risk, and capability vocabularies. Keep separate product capabilities over shared primitives.

## 7. `Window` as the primary Browser product name

**Reject.**

`Window` becomes ambiguous across browser windows, desktop windows, remote surfaces, tabs, and embedded views. Use `Browser` for the product capability and `InteractiveSurface` internally.

## 8. WebMCP as an independent subsystem

**Reject.**

WebMCP is one untrusted structured Browser route. It must not own authority, page truth, or a separate evidence model.

## 9. WebMCP as core internal domain model

**Reject initial coupling.**

Treat WebMCP as an adapter/spec target behind WePLD-owned contracts because the standard may evolve and page declarations are untrusted.

## 10. Screenshot-first Browser

**Reject.**

Prefer qualified native integration/API, WebMCP, semantic/DOM/accessibility, and browser-protocol routes before visual grounding/raw input when semantics are equivalent.

## 11. Screenshot-first Computer Use

**Reject.**

Prefer app-native and OS accessibility/automation semantics before visual grounding/raw pointer/keyboard.

## 12. Global `computer_access` boolean

**Reject.**

Decompose observation/window/pointer/keyboard/clipboard/file-picker/drag-drop capabilities and scope ownership with InputLease where required.

## 13. Browser profile as ordinary cache

**Reject.**

Authenticated browser state is credential-bearing state and needs separate lifecycle/security treatment.

## 14. Automatic browser-profile synchronization to cloud

**Reject initial architecture.**

It creates unnecessary credential/privacy blast radius. Prefer isolated managed contexts and selective authentication/brokering.

## 15. Project as vector database / RAG collection

**Reject.**

Project Experience is a Fehrest-backed governed context boundary. Vector retrieval is an optional projection/signal, not project truth.

## 16. New Project memory database beside Fehrest

**Reject.**

Would create competing project truth/freshness semantics.

## 17. General-purpose non-repository Project model in S2

**Reject backward pull.**

S2 remains project identity/storage foundation. Revisit generalized project roots/scopes after Fehrest Project Experience exists.

## 18. Work as chat thread only

**Reject.**

Work needs durable session/evidence semantics across missions, attempts, tools, artifacts, approvals, and client/host continuity.

## 19. Work as execution engine

**Reject.**

Mission Runtime owns execution; Work owns durable user/session/evidence coordination.

## 20. Per-feature evidence stores

**Reject.**

Browser, Computer, Automation, and Connections should emit typed records into the existing evidence model.

## 21. New route-selection service

**Reject.**

Mirefa already owns route/capability qualification.

## 22. New policy engine for feature behavior

**Reject.**

Nawat remains effect-time authority; behavior policy may narrow, never grant.

## 23. Blind retry after connector/browser/computer timeout

**Reject.**

Reuse existing `EffectReconciliation`. Unknown consequential outcomes are reconciled before unsafe retry.

## 24. Temporal as initial runtime dependency

**Reject initially / retain as oracle.**

Temporal is valuable for durable-execution/replay behavior study, but importing another durable orchestrator before proving Mission Runtime cannot satisfy the minimum contract risks nested orchestration and duplicated truth.

## 25. n8n full engine adaptation

**Reject.**

Mine behavior/failure/security mechanisms only. The proposed architecture is not an n8n clone and n8n's license also requires separate source-use analysis.

## 26. Zapier platform source as default donor

**Reject.**

Use schema/runtime concepts as specification/behavior oracles unless a separate source gate establishes admissible reuse.

## 27. Activepieces full platform import

**Reject broad import; retain bounded candidate.**

Potential value lies in typed piece/integration framework mechanisms and community integration examples. Any adaptation must be path-bounded and separately admitted.

## 28. Playwright types as WePLD Browser API

**Reject.**

Playwright is a strong dependency/behavior candidate but must stay behind WePLD-owned Browser contracts.

## 29. InteractiveSurface

**Keep as minimum cross-feature primitive candidate.**

It prevents Browser/Computer from inventing duplicate host/surface/freshness identity while carrying no authority.

## 30. InputLease

**Keep as minimum primitive candidate for raw/ownership-sensitive input.**

It represents expiring/fenced actuation ownership; Nawat still owns authority.

## 31. CapabilityPresence

**Keep as lightweight planning/observation candidate.**

It explains local/cloud/client capability loss without pretending presence means qualification or authority.

## 32. AutomationDefinition

**Keep.**

Durable declarative revision identity is required to explain which trigger configuration produced a Mission.

## 33. TriggerEnvelope

**Keep.**

Authenticity/replay/deduplication and event identity require a durable typed observation distinct from WorkflowIntent.

## 34. IntegrationDescriptor

**Keep.**

Typed integration capability/schema/risk/version identity is required for connector qualification and generated DX.

## 35. ConnectionBinding

**Keep.**

Project/Work/Automation-to-account binding is distinct from raw credentials and authority.

## 36. RouteConstraint as new entity

**Defer.**

Start as fields (`preferred/required/forbidden_routes`) inside existing planning records. Promote only if independent identity/lifecycle emerges.

## 37. Astra-like ambient multimodal presence in the initial scope

**Reject initial scope / later research.**

Continuous camera/microphone/screen perception introduces a materially larger privacy, retention, intent-inference, and ambient-capability program than reliable Computer Use.

## 38. Mobile Computer Use as initial requirement

**Reject initial scope / later research.**

Prove desktop/browser semantics and trust boundaries first.

## 39. Final minimum-sufficient planning set

```text
Primary UX:
  Projects
  Work
  Automations

Supporting UX/capabilities:
  Connections / Integrations
  Browser
  Computer

Shared candidate primitives:
  AutomationDefinition
  IntegrationDescriptor
  ConnectionBinding
  TriggerEnvelope
  CapabilityPresence
  InteractiveSurface
  InputLease

Existing owners reused:
  Fehrest / Maemar
  Edara
  Mirefa
  Nawat
  Mission Runtime
  UWC
  Case Bus
  AMAN
  Assurance Fabric
  Evidence Graph
  Trusted Completion
```

```text
PONYTAIL_RESULT = MINIMUM_SUFFICIENT_FOR_FUTURE_PLANNING
PONYTAIL_RESULT != IMPLEMENTATION_AUTHORITY
PONYTAIL_RESULT != SOURCE_ADMISSION
PONYTAIL_RESULT != DEPENDENCY_ADMISSION
```
