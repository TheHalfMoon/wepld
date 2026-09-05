# Product Capability Tracks — Planning Acceptance

```text
STATUS = FUTURE_PLANNING_ACCEPTANCE
IMPLEMENTATION_AUTHORITY = NONE
```

This acceptance contract determines whether the Projects / Work / Automations / Connections / Browser / WebMCP / Computer Use planning extension is coherent enough to remain in Spec 006. It does not accept or authorize implementation.

## A. Product/ownership coherence

- [ ] Primary user-facing surfaces remain `Projects`, `Work`, and `Automations`; supporting capabilities do not become unnecessary top-level subsystems.
- [ ] Project Experience is explicitly Fehrest-backed and does not create a second truth/memory authority.
- [ ] Work is a durable session/evidence surface and does not duplicate Mission Runtime.
- [ ] Automations compile triggers/definitions into the existing Mission path and do not create a second orchestrator.
- [ ] Connections separate IntegrationDescriptor, ConnectionBinding, CredentialCapability, and effect authority.
- [ ] Browser and Computer share InteractiveSurface freshness/identity mechanics without sharing ambient authority.
- [ ] WebMCP remains an untrusted Browser route rather than an authority or core domain dependency.

## B. Parent-plan reconciliation

- [ ] The parent `Workflow Engine` wording is explicitly constrained to intent/planning/definition mechanics and cannot be interpreted as a second durable execution engine.
- [ ] No addendum conflicts with canonical V2.3 ownership: Fehrest informs, Edara plans topology, Mirefa qualifies, Nawat authorizes effects, Mission Runtime executes, Assurance evaluates, Trusted Completion decides completion.
- [ ] S2 remains unchanged in scope and no S3+ feature implementation is pulled backward.

## C. Primitive sufficiency

Candidate primitives are accepted for planning only if each has a distinct lifecycle/identity need:

```text
AutomationDefinition
IntegrationDescriptor
ConnectionBinding
TriggerEnvelope
CapabilityPresence
InteractiveSurface
InputLease
```

- [ ] `RouteConstraint` remains a planning field unless later evidence proves independent identity/lifecycle is necessary.
- [ ] No `AutomationRuntime`, `BrowserAuthority`, `ComputerAuthority`, per-feature evidence store, or ProjectMemoryDatabase is introduced.
- [ ] Existing `EffectProposal / NawatDecision / EffectResult / EffectReconciliation` remains the shared effect model.

## D. Failure semantics

- [ ] Unknown effect outcome is distinct from known failure/no-effect.
- [ ] Transport retryability is not treated as effect retry safety.
- [ ] Reconciliation is required before unsafe retry of an unknown consequential effect.
- [ ] Duplicate trigger/event delivery cannot silently duplicate irreversible effects.
- [ ] Route migration is visible and requires reconciliation/requalification where semantics/state/capabilities differ.
- [ ] Stale interactive observations/targets fail closed before actuation.
- [ ] User intervention is treated as a causal event where it changes input/surface state.
- [ ] Local UI action acknowledgement is not treated as proof of business-effect completion.

## E. Security/trust boundary

- [ ] Connection success/OAuth success never becomes a Nawat grant.
- [ ] Browser cookie/profile state is classified as credential-bearing state.
- [ ] ManagedBrowser, AttachedUserBrowser, and RemoteBrowser have distinct risk/state semantics.
- [ ] WebMCP tool declarations/descriptions/schemas/output remain untrusted page input.
- [ ] Computer Use is decomposed into scoped observation/input/clipboard/etc. capabilities instead of a global boolean.
- [ ] Raw input ownership uses an expiring/fenced InputLease where required.
- [ ] High-risk authentication/financial/admin/security surfaces require stronger qualification/authority treatment.
- [ ] File upload/download separates filesystem/read authority, network/browser effect authority, and parse/execute authority.

## F. Distributed/recovery semantics

- [ ] Same WorkSession is not assumed to mean same host/worker/attempt/route.
- [ ] CapabilityPresence is an observation, not qualification or authority.
- [ ] Cross-host route migration defines identity, freshness, capability refresh, and effect-time revalidation requirements.
- [ ] Remote input/browser ownership has fencing/split-brain requirements before durable autonomy.
- [ ] Long-lived Automations use durable Mission/S9 recovery semantics rather than in-memory callbacks as truth.

## G. Evidence/assurance

- [ ] No new per-feature canonical evidence store is introduced.
- [ ] Interactive action proposals bind to relevant SurfaceObservation identity/generation/preconditions.
- [ ] Browser/Computer/connector effects produce ordinary typed effect/evidence records.
- [ ] Future S7 evaluation includes connector supply chain, WebMCP/tool poisoning, browser prompt injection, stale-target races, Computer Use safety, and high-consequence unknown-outcome tests.
- [ ] Benchmark claims require exact benchmark version/revision, environment/route/model identity, measurement boundary, and reproducible evidence rather than product demos.

## H. Source-acquisition boundary

- [ ] Activepieces, Zapier, n8n, Make, Nango, Trigger.dev, Temporal, Playwright, WebMCP, WebDriver BiDi/CDP, BrowserGym, OSWorld-V2, UI-TARS, accessibility APIs, commercial product UX references, and Lily remain classified only according to the source study.
- [ ] No source/dependency admission is inferred from public availability, permissive licensing, product similarity, or this planning merge.
- [ ] Restricted/non-permissive sources are not copied into WePLD merely because they are inspectable.

## I. Roadmap discipline

- [ ] S1/S2 receive no feature-scope expansion from this addendum.
- [ ] PX starts from S4 after S2 foundations.
- [ ] AU planning begins no earlier than the owning S5 planning mechanics; effectful execution waits for later authority.
- [ ] WK/IS interoperability waits for S6 owners.
- [ ] assurance precedes broad actuation/autonomy.
- [ ] S9 owns durable continuation/recovery lineage.
- [ ] Astra-like ambient multimodal presence and mobile Computer Use remain later research rather than initial requirements.

## J. Planning-package merge gate

Before this planning package itself is merged:

1. reconcile PR #241 non-destructively with current canonical main;
2. prove all changed paths remain under the Spec 006 planning package;
3. run fresh exact-head deterministic qualification;
4. obtain genuinely independent whole-scope exact-head engineering/correctness review;
5. reconcile every material finding;
6. rerun freshness-dependent qualification after any head change;
7. prove zero unresolved material review threads;
8. perform final live base/head/tree/diff/check/review race verification.

```text
PLANNING_ACCEPTANCE != IMPLEMENTATION_ACCEPTANCE
PLANNING_MERGED != SOURCE_ADMISSION
PLANNING_MERGED != DEPENDENCY_ADMISSION
PLANNING_MERGED != RUNTIME_AUTHORITY
```
