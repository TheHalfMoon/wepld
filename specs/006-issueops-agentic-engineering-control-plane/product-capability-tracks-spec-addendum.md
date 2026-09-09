# Product Capability Tracks — Specification Addendum

```text
STATUS = FUTURE_PLANNING_ADDENDUM
SPEC = 006_ISSUEOPS_AGENTIC_ENGINEERING_CONTROL_PLANE
SCOPE = PROJECTS_WORK_AUTOMATIONS_CONNECTIONS_BROWSER_WEBMCP_COMPUTER_USE
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
RUNTIME_AUTHORITY = NONE
```

This addendum shapes the product capabilities discussed as Projects, Work, automation/integration, Browser/WebMCP, and Computer Use without creating parallel orchestration, authority, evidence, or runtime systems. It extends the parent Spec 006 package only as future planning.

```text
DISCUSSION != IMPLEMENTATION
IDEA != PLAN
PLAN != AUTHORITY
RESEARCH != SOURCE_ADMISSION
LICENSE_AVAILABLE != SOURCE_ADMISSION
```

## 1. Product thesis

The user-facing product should remain simple while the trust architecture remains explicit underneath it.

Primary product surfaces:

```text
Projects
Work
Automations
```

Supporting capabilities:

```text
Connections / Integrations
Browser
Computer
```

`WebMCP` is a Browser route, not a top-level product or independent authority subsystem.

The goal is not to assemble a clone of Zapier, n8n, Claude Projects/Cowork, Codex Work, or Project Astra. The goal is to let different work surfaces converge on one explainable WePLD chain:

```text
intent
-> context
-> planning
-> qualification
-> authority
-> execution
-> observation
-> assurance
-> controlled reconciliation / repair
-> evidence
-> trusted completion
```

## 2. Cross-slice capability tracks

```text
PX — Project Experience
WK — Work Plane
AU — Automations and Connections
IS — Interactive Surfaces
```

These are capability tracks, not new roadmap slices or mandatory services.

```text
PX owns no authority.
WK owns no execution engine.
AU owns no orchestration engine.
IS owns no effect authority.
```

They mature only when the canonical owning slice supplies the prerequisite primitive and separate implementation authority.

## 3. Ownership map

```text
project identity/local storage             -> S2 foundation
project/code/architecture context          -> Fehrest / Fehrest.Maemar
user-facing durable work session           -> Work plane
minimum-sufficient task topology           -> Edara
route/runtime/connector qualification      -> Mirefa
effect-time authority                      -> Nawat
attempt/worker/runtime/recovery             -> Mission Runtime
provider/harness/tool normalization        -> UWC
trigger/event ingress                      -> Case Bus
security/risk evidence                     -> AMAN
review/test/claim assessment               -> Assurance Fabric
evidence relationships                     -> Evidence Graph
final completion                           -> Trusted Completion
Projects/Work/Automations interaction UX   -> Desktop/UI
```

No capability in this addendum may silently absorb another owner's semantics because implementation convenience makes that easy.

## 4. Project Experience requirements

A Project is a durable governed context boundary, not a chat folder, vector database, or alternate authority domain.

The Project experience should be able to present at least these conceptual context classes without pretending they have equal trust:

```text
CanonicalFact
ObservedFact
UserInstruction
UserProvidedArtifact
DerivedContext
LearnedPreference
ExternalObservation
```

Requirements:

1. project context preserves identity, provenance, observation time, content/generation identity, freshness, and trust/authority class sufficient to explain why WePLD believes a material fact;
2. repository canonical memory outranks chat/model summaries where the repository is the relevant authority;
3. project instructions constrain planning/behavior but do not grant effects;
4. learned/generated context remains a candidate until qualified under its owning contract;
5. Work sessions, Automations, Artifacts, Evidence, and ConnectionBindings may be associated with a Project without inheriting ambient authority from the association;
6. a future generalized non-repository Project model must not be pulled backward into S2 merely to imitate general-purpose project products.

```text
PROJECT_CONTEXT != AUTHORITY
PROJECT_INSTRUCTION != EFFECT_AUTHORITY
PROJECT_ASSOCIATION != CONNECTION_AUTHORITY
PROJECT_MEMORY != CANONICAL_TRUTH
```

## 5. Work requirements

Work is the durable user-facing interactive session and evidence surface. Mission Runtime remains the execution host.

```text
WORK_SESSION != MISSION
MISSION != ASSIGNMENT
ASSIGNMENT != ATTEMPT
ATTEMPT != WORKER
WORKER != HOST
```

A WorkSession may survive changes in client, host, worker, or attempt. Such continuity never means local capabilities silently followed the user or mission.

A Work surface should converge conversation, files, editor, terminal, browser, computer interaction, connectors, artifacts, approvals, and evidence into one inspectable timeline where applicable.

The shared `CapabilityPresence` planning record describes currently observed availability, not qualification or authority:

```text
CapabilityPresence {
  subject_scope
  host_or_route_ref?
  capability
  availability_state
  observed_at
  freshness
  evidence_refs[]
}
```

Example capability presence may distinguish local filesystem/browser/computer availability from cloud browser/shell or connector availability.

```text
CAPABILITY_PRESENT != CAPABILITY_QUALIFIED
CAPABILITY_QUALIFIED != EFFECT_AUTHORITY
SAME_WORK_SESSION != SAME_HOST
SAME_WORK_SESSION != SAME_ATTEMPT
CLOUD_CONTINUATION != LOCAL_CAPABILITY_CONTINUATION
```

Route migration after capability loss requires explicit state reconciliation and Mirefa requalification; pending effects require Nawat revalidation where applicable.

## 6. Automations and Connections requirements

An Automation is a durable trigger-to-Mission definition. It is not a second workflow runtime.

```text
Trigger
-> Case Bus / qualified trigger ingress
-> AutomationDefinition match
-> WorkflowIntent / Mission creation
-> Edara
-> Mirefa
-> Nawat
-> Mission Runtime
-> Evidence / Assurance / Trusted Completion
```

The user may see an `Automation run`, but core execution remains Mission + Assignment/Attempt + Evidence rather than a parallel execution identity.

Connections must preserve four distinct concepts:

```text
IntegrationDescriptor = what a service integration declares it can do
ConnectionBinding      = which authenticated account/tenant is bound to a scope
CredentialCapability   = bounded runtime authentication ability
AuthorityGrant         = permission for the exact effect at effect time
```

Detailed contracts are owned by `contracts/automation-connections.md`.

## 7. Interactive Surface requirements

Browser and Computer Use share an `InteractiveSurface` abstraction, but remain different product capabilities and effect classes.

Preferred Browser route order when semantics are equivalent and routes are qualified:

```text
1. Native Integration / API
2. WebMCP
3. Semantic Browser interaction
4. Browser protocol interaction
5. Visual grounding
6. Raw pointer / keyboard
```

Preferred arbitrary application/computer route order:

```text
1. App-native Integration / API
2. OS accessibility / automation API
3. Structured application surface
4. Visual grounding
5. Raw pointer / keyboard
```

The route order is a qualification preference, not an automatic fallback chain. A user or plan may require/forbid routes, and any material route change must remain visible.

Detailed contracts are owned by `contracts/interactive-surfaces.md`.

## 8. Effect and failure semantics

All effectful capabilities converge on the existing Spec 006 `EffectProposal -> NawatDecision -> EffectResult -> EffectReconciliation` model. This addendum creates no browser-, computer-, automation-, or connector-specific authority engine.

The execution UX must be able to distinguish at least:

```text
SUCCEEDED
FAILED_NO_EFFECT
FAILED_KNOWN_EFFECT
OUTCOME_UNKNOWN
CANCELLED
WAITING
BLOCKED
STALE
```

These are product-facing classes; the canonical field vocabulary remains the owning effect/runtime contract.

```text
TRANSPORT_RETRYABLE != EFFECT_RETRY_SAFE
EFFECT_OUTCOME_UNKNOWN != SAFE_TO_RETRY
RECONCILIATION != REEXECUTION
GUI_ACTION_COMPLETED != BUSINESS_EFFECT_CONFIRMED
```

An uncertain external effect must be reconciled before a duplicate or irreversible dependent effect is attempted unless a separate owning contract proves safe idempotency/retry semantics.

## 9. Security requirements

### 9.1 Browser state

```text
MANAGED_BROWSER != ATTACHED_USER_BROWSER
ATTACHED_USER_BROWSER != AMBIENT_USER_AUTHORITY
REMOTE_BROWSER != LOCAL_BROWSER
BROWSER_COOKIE_STATE = CREDENTIAL_BEARING_STATE
BROWSER_PROFILE_TRANSFER != ORDINARY_FILE_COPY
```

Managed, attached-user, and remote browser modes require distinct risk/credential treatment. Browser profile/cookie/session state must not silently synchronize across Projects, hosts, or cloud workers.

### 9.2 WebMCP

WebMCP declarations originate from the page and remain untrusted input.

```text
WEBMCP_TOOL_DECLARATION = UNTRUSTED_PAGE_INPUT
WEBMCP_TOOL_DESCRIPTION = UNTRUSTED_PAGE_INPUT
WEBMCP_TOOL_SCHEMA != SAFE_EFFECT
WEBMCP_TOOL != TRUSTED_TOOL
WEBMCP_HINT != NAWAT_GRANT
NAVIGATION_MAY_INVALIDATE_PAGE_SCOPED_TOOL_IDENTITY
```

### 9.3 Computer control

There is no boolean ambient `computer_access` capability. Observation, application/window interaction, pointer input, keyboard input, clipboard read/write, file picker, drag/drop, and similar powers are independently scoped capabilities.

Raw input actuation requires an expiring/fenced `InputLease` under the interactive-surface contract.

```text
SCREEN_CAPTURE != INPUT_AUTHORITY
CLIPBOARD_CAPABILITY != KEYBOARD_CAPABILITY
INPUT_CONTROL != GLOBAL_MACHINE_AUTHORITY
USER_INTERVENTION != EXECUTION_NOISE
```

Security-sensitive surfaces such as password managers, authentication dialogs, OS security settings, privileged prompts, financial actions, and destructive administrative controls require stronger risk/authority treatment rather than an after-the-fact blocklist assumption.

## 10. Evidence requirements

Do not create per-feature evidence stores. Material actions should link existing typed evidence primitives:

```text
Observation
EvidenceRef
QualificationReceipt
AuthorityGrant / NawatDecision
Attempt
RuntimeEvent
Finding
ClaimAssessment
EffectResult / EffectReconciliation
CompletionDecision
```

Interactive action proposals must bind to the observation/surface generation on which the target decision was based. Relevant state drift forces re-observation/revalidation.

```text
SURFACE_OBSERVATION != CURRENT_SURFACE_STATE
VISUAL_TARGET != STABLE_TARGET
STALE_SURFACE != SAFE_TO_ACT
NEW_RELEVANT_SURFACE_GENERATION -> PRIOR_TARGET_ASSUMPTIONS_MAY_BE_STALE
```

## 11. UX requirements

Ordinary UX should not expose internal governance names unnecessarily. User-facing states should map typed internal evidence into understandable conditions such as:

```text
Ready
Running
Waiting for you
Needs permission
Connection required
Device unavailable
Route unavailable
State changed
Recovering
Outcome uncertain
Blocked
Completed
```

The UI must not collapse `Completed` into provider success, green CI, model confidence, or a remote effect acknowledgement when Trusted Completion is required.

## 12. Distributed-system requirements

Any cross-host/client/provider capability must define identity, leases/fencing where ownership exists, causality, deduplication, idempotency boundaries, ordering requirements, retries, reconciliation, offline behavior, recovery, compatibility, and version negotiation before durable autonomy is qualified.

In particular:

```text
SAME_WORK_SESSION != SAME_EXECUTION_ROUTE
ROUTE_AVAILABILITY != ROUTE_QUALIFICATION
ROUTE_QUALIFICATION != EFFECT_AUTHORITY
SILENT_ROUTE_FALLBACK = PROHIBITED
```

## 13. Explicit non-goals for the initial track

The following remain later research or rejected initial architecture:

```text
Astra-like ambient camera/microphone/screen presence
mobile Computer Use as an initial requirement
fully autonomous global desktop control
cross-device browser-profile synchronization
automatic credential/profile migration
new generalized S2 Project identity model
n8n/Make/Zapier clone architecture
separate Automation Runtime
separate Browser/Computer authority engine
project memory as a vector database
direct source import merely because a license exists
Temporal or another durable orchestrator as a default runtime dependency
```

## 14. Acceptance and implementation boundary

This addendum is acceptable as planning only when `product-capability-tracks-acceptance.md` passes and the whole Spec 006 package remains internally coherent.

Even after Spec 006 planning merge:

```text
PLANNING_MERGED != FEATURE_IMPLEMENTATION_AUTHORIZED
SOURCE_CLASSIFIED != SOURCE_ADMITTED
DEPENDENCY_CANDIDATE != DEPENDENCY_ADMITTED
MATURITY_LEVEL != AUTHORITY
AUTONOMY_MODE != AUTHORITY
```

## 15. Complete product requirement families

These identifiers bind the detailed requirements in sections 4–12 to their concrete contracts, acceptance and tasks. Each family is conjunctive: a partial member does not satisfy the family. `product-capability-tracks-plan.md` sections 14–17 provide forward and reverse traceability and failure/UX obligations.

- **PCT-FR-PX**: Project identity, repository/worktree/file/directory/collection membership, instruction provenance/precedence, current/stale/revoked context, semantic retrieval, access-safe associations/history and inert import/export must follow `data-model.md` section 22 and `contracts/retrieval-rag.md`. Generalized roots remain an explicit deferred extension.
- **PCT-FR-WK**: durable WorkSession/Mission cardinality, objective/control revisions, idempotent pause/resume/cancel/handoff, client continuity, capability loss, approval freshness, evidence timeline and result/review/repair/completion distinction must follow `data-model.md` sections 15 and 23 plus runtime/worker contracts.
- **PCT-FR-AU**: immutable definitions, all admitted trigger kinds, authentic bounded capture, revision-independent occurrence dedupe, atomic intent association, timezone/DST/misfire rules, finite backlog/concurrency, pinned steps/conditions/approval waits, simulation, partial effects and reconciliation must follow `contracts/automation-connections.md` sections 2–4 and 16.
- **PCT-FR-CN**: versioned integration/action/trigger schemas, verified account bindings, multi-account selection, scopes/visibility, OAuth/refresh/rotation/revocation, per-operation credential derivation, pagination/rate-limit/error/subscription contracts and SDK conformance must follow `contracts/automation-connections.md` sections 5–8 and 17–18 and canonical CredentialCapability.
- **PCT-FR-BR**: all Browser operations, hierarchical identity, managed/attached ownership versus local/remote location, credential-bearing profiles, bounded DOM/accessibility/screenshot observation, stale-target/actionability checks, quarantine and takeover must follow `contracts/interactive-surfaces.md` sections 2–9 and 19 plus `contracts/web-agent-boundary.md`.
- **PCT-FR-CU**: host/session/app/process/window incarnations, monitor/DPI/capture transforms, independent observation/input classes, enforcing InputLease, user intervention, protected/non-observable refusal, cleanup and remote recovery must follow `contracts/interactive-surfaces.md` sections 10–20. Ambient multimodal autonomy is deferred.
- **PCT-FR-WM**: untrusted, bounded, versioned/namespaced declaration discovery; exact context/document/tool identity; canonical EffectProposal; proven route equivalence; Mirefa qualification before canonical Nawat decision; revocation/schema drift and evidence-bound outcome must follow `contracts/web-agent-boundary.md`.
- **PCT-FR-AF**: every significant product operation must produce exact target/policy/qualification/authority/execution/observation/failure evidence and an appropriate ClaimAssessment through the single Assurance Fabric; cache, independent review, unresolved findings, stale evidence and Trusted Completion follow `contracts/assurance-fabric.md` and `contracts/review-independence.md`.
- **PCT-FR-X**: all eight families must obey the failure, security, distributed, UX, developer and dependency obligations in plan sections 14–17. Product presentation cannot mint request, qualification, authority, execution, review or completion powers.
