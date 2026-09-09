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

All criteria in sections A–I must first be checked with concrete planning evidence, or marked not applicable with a scoped rationale and supporting evidence accepted by the independent review. An unchecked criterion is incomplete; the presence of a contract or this procedural gate does not satisfy it. Drafting tasks and implementation qualification remain separate.

1. reconcile PR #241 non-destructively with current canonical main;
2. prove all changed paths remain under the Spec 006 planning package;
3. run fresh exact-head deterministic qualification;
4. obtain independent qualified whole-scope exact-head engineering/correctness review, with qualification evidence and scope/exclusions;
5. reconcile every material finding;
6. rerun freshness-dependent qualification after any head change;
7. prove zero unresolved material review threads;
8. perform final live base/head/tree/diff/check/review race verification.

Whole-scope review covers every file in the final Spec 006 candidate delta against the current canonical base plus necessary owner contracts. A provider status, incremental review, older-head review, sampled source scan or repair author's report cannot substitute. The review must declare included/excluded scope, exact base/head, reviewer independence, findings and reconciliation. A required reviewer being unavailable, unqualified, stale or materially incomplete is `REVIEW_BLOCKED`, never implicit acceptance. Before external sharing, canonical `EXTERNAL_REVIEW_EGRESS_POLICY.md` requires an exact base/head scope, classification, screening, required redaction/handling, eligible provider/product identity and recorded authorization; perform this before sending source or review context.

### Adversarial closure checks

- [ ] Executable effects bind intent/Mission/Assignment/Attempt/principal/route/credentials/risk and preserve logical operation identity across dispatch attempts.
- [ ] Crash after durable dispatch but before receipt is unknown; eventual-consistency not-found does not prove no effect without a qualified visibility bound.
- [ ] Every fenced route names an enforcing sink; raw credential/input bypass and uncertain old-owner shutdown prevent automatic takeover.
- [ ] Durable connection bindings derive bounded per-attempt credentials; revocation/refresh/version changes invalidate affected eligibility.
- [ ] Trigger capture/intent association is durable and deduplicated across crash/replay, with scoped key-conflict, retention and schedule-misfire semantics.
- [ ] WorkSession/Mission cardinality, objective revision and client-versus-controller continuity use existing owners.
- [ ] Browser lifecycle ownership and host location are separately qualified; GUI check-to-act race limits remain explicit.
- [ ] Review repair cannot self-certify, and all applicable criteria have evidence before planning acceptance.

```text
PLANNING_ACCEPTANCE != IMPLEMENTATION_ACCEPTANCE
PLANNING_MERGED != SOURCE_ADMISSION
PLANNING_MERGED != DEPENDENCY_ADMISSION
PLANNING_MERGED != RUNTIME_AUTHORITY
```

## K. Product acceptance families and planning evidence

These are conjunctive design/fixture contracts. Planning verification checks that the rules, ownership, failure responses and tasks are complete and coherent; runtime execution evidence is required only at the future owning implementation gate. Current draft evidence is linked through plan sections 14–17. Checkboxes remain open until that planning assessment is independently qualified; they do not claim the future tests have run.

- [ ] **PX-A** (PCT-FR-PX; PX-001..006): prove exact Project membership/provenance/current-vs-derived conflicts, instruction precedence without authority, revoked-source filtering through retrieval/history/associations, and inert import/export with credential/grant exclusion. A stale or revoked source cannot be presented as current; multi-root expansion cannot alter S2 identity.
- [ ] **WK-A** (PCT-FR-WK; WK-001..006, PCT-R002/003): prove one session/many Missions, exact objective/control revisions, concurrent control-request dedupe/conflicts, pause request versus quiescence, cancellation versus cessation/outcome, client reconnect/cursor gaps and fenced handoff. Approval binds target/input/account/policy/expiry, and completion consumes evidence rather than a worker success label.
- [ ] **AU-A** (PCT-FR-AU; AU-001..003/008..010, PCT-R001): prove duplicate delivery across definition edits creates one pinned intent, crash-safe capture/cursor/outbox, DST fold/gap and bounded misfire policies, overflow refusal, schema drift and signature failure, finite declarative branch/template expansion, expired approval waits, partial effects and separately authorized compensation. Simulation cannot obtain live credentials or create effects.
- [ ] **CN-A** (PCT-FR-CN; AU-004..007/011, PCT-A001/E001): prove exact account binding and no fallback, OAuth callback/state/PKCE protections, cross-host refresh/rotation/revocation CAS, complete scoped capability activation and HTTPS redirects, pagination incompleteness, rate-limit budgets, webhook lifecycle, key retention and schema migration. Every semantic capability has a bounded example/anti-example and a live-vs-sample qualification label.
- [ ] **BR-A** (PCT-FR-BR; IS-BR001..005/008..011, PCT-E002/R004): cover every operation in IS §19, hierarchical context/frame/document identity, managed/attached versus local/remote modes, cookie/profile privacy, bounded observations, navigation/actionability races, user takeover and quarantine/upload provenance. A required unavailable semantic route cannot silently become eval/raw coordinates; an uncertain click outcome cannot retry blindly.
- [ ] **CU-A** (PCT-FR-CU; IS-CU001..011, PCT-A004/E003/R004): prove host/session/process/window incarnation and monitor/DPI transforms, semantic/pixel freshness, per-class input/clipboard grants, enforcing lease queue, focus/modal/user intervention, held-input cleanup and remote old-owner rejection. Protected/non-observable UI blocks unattended input; ambient/mobile remains deferred.
- [ ] **WM-A** (PCT-FR-WM; IS-BR006/007, web-agent task groups): prove bounded untrusted discovery/version/schema namespace, collisions, malicious descriptions/outputs, exact canonical effect/context/input bindings, equivalent-route evidence, Mirefa-before-Nawat ordering, expiry/revocation/schema/navigation drift and invocation/postcondition lineage. Tool-declared success/permissions do not become authority or completion.
- [ ] **AF-A** (PCT-FR-AF; PCT-A002/003/005/006, PCT-E004/005/R005/006): prove the significant-operation evidence table in AF §27 for all eight features, immutable policy/required-claim cache binding, exact target/engine/route/authority/outcome evidence, every non-clean test class, conflicts/coverage gaps, fresh independent review after repair and separate Trusted Completion. Evidence privacy precedes persistence and egress.
- [ ] **X-A** (PCT-FR-X; PCT-P/PCT-S and all feature tasks): walk every failure cell in plan §15 and every UX state in §16; each must reach its canonical owner and observable evidence without silently widening access, authority, route or retry powers. Check all task/requirement/acceptance edges and roadmap prerequisites, classified research with no source admission, and section J's exact-head whole-scope qualification gate.

## Local design assessment for sections A–I — 2026-09-07

AUTHOR_ASSESSMENT = DESIGN_INSPECTED for A–I, supported by the table below. INDEPENDENT_QUALIFICATION = PENDING. All A–I checkboxes remain unchecked until qualified exact-head planning acceptance; the author assessment cannot check them or serve as runtime test execution or merge authority. Each numbered range refers to the criteria in that section in display order. No N/A exemption is used. Sections J/K and the final independent whole-package qualification remain open and must be assessed against the final immutable candidate.

| Criteria | Draft evidence and reasoning | Implementable acceptance/task link |
|---|---|---|
| A1–A7 | Product plan §§2/14 names one Projects/Work/Automations hierarchy and existing owners. DM §§15/22/23 makes Projects a Fehrest projection and Work a MissionRuntime association. AC §§1/4/16 compiles accepted triggers to existing Missions; §§5–8/17 separates descriptor/account/capability/grant. IS §§2/19/20 separates Browser/Computer identity and powers; WB keeps declarations untrusted. No feature gains a second orchestrator or authority store. | PX-A/WK-A/AU-A/CN-A/BR-A/CU-A/WM-A; product plan §17 |
| B1–B3 | Parent plan's Workflow Engine clarification and product plan §§1/13 constrain the term to intent/definition mechanics. Product specification §3 and plan §14 preserve the full owner chain. The exact PR delta contains only 58 Spec 006 Markdown files; canonical S2/governance/runtime files are unchanged relative to current main. | X-A; PCT-P001..005 and parent acceptance A/F |
| C1–C3 | Product plan §10 and Ponytail keep RouteConstraint as fields. DM §19 owns all effect records, grant aliases and reconciliation; OH Canonical primitive convergence collapses advertisement/backend/tool/effect/event sketches into existing projections/payloads. AC definition/account identity and IS InputLease each have explicit independent lifecycle need. | X-A; PCT-P003/005, WK-006, HARD-C001..004 |
| D1–D8 | DM §19 records logical operation versus dispatch, unknown outcome and closed retry-safety states. AC §§4/16 pins first occurrence and atomically associates intent; IS §§4/12/13/19/20 enforces stale target/input ownership and declares residual races. Product plan §15 covers all 38 failures and §16 prevents an acknowledgement or retryable transport from becoming safe completion/retry. | AU-A/WK-A/BR-A/CU-A/WM-A; AU-002/003/008, IS-BR/IS-CU, PCT-E005 |
| E1–E8 | AC §§7/8/17 and RF CredentialCapability separate authentication/egress/effect authority and scope every credential use. IS §§5/6/19 separates ownership from location and protects profiles/cookies. WB lifecycle treats all declarations/output as untrusted. IS §§11/12/19/20 requires independent input/clipboard grants, enforced lease and protected-UI refusal. WB artifacts requires inert quarantine/exact upload artifact before separately authorized use. | CN-A/BR-A/CU-A/WM-A; AU-005, PCT-A001..004, IS-BR008, IS-CU004..008 |
| F1–F5 | DM §§15/23 binds Work to durable identities/control revisions with access-checked cursor replay. AC §3 defines CapabilityPresence as Observation. RF/RD requires exact authenticated host/runner/harness, enforcing ownership fences, current resource admission and version handshake; AC §§4/16 makes acceptance/intent/outbox durable before effects and S9 adds extended history. | WK-A/AU-A/CU-A; WK-001..005, PCT-R001..004, RT/OM recovery tasks |
| G1–G5 | AF §27 maps every significant product operation to existing target/policy/engine/observation/effect/claim records. IS §3/4 binds proposals to observation generation; RF/DM retain authority/execution lineage. Product tasks PCT-A001..006 and IS-BR011/IS-CU009 define the hostile/failure and benchmark corpus. AF PerformanceEvidence and Lily source study require exact source/model/route/environment, predeclared measurement and uncertainty. | AF-A; PCT-A001..006, AF/HARD/OH task maps |
| H1–H3 | Existing source acquisition product addendum and mechanism study's Completion source study list bounded real-code/doc observations, immutable pins, exact reuse classifications and limitations. Lily runtime/extra orchestrators/ambient plugins are rejected; no donor code, dependencies or registry edits enter this planning delta. Candidate/import rights remain future governed gates. | X-A; PCT-S001..007 and parent acceptance M |
| I1–I7 | Product plan §§4/13/17 matches canonical P0+S1..S10, preserving active S2. S4 context, S5 intent, S6 interoperability/authority, S7 assurance, S8 bounded effects and S9 history are dependency ordered. S10 means Fehrest/Byan expansion, with other scale ideas conditional. Minimum durable safety/privacy precedes execution; ambient/mobile remains deferred in IS §20 and the product non-goals. | X-A; product §17 dependency edges, PX-006, IS-CU011 and PCT-E/PCT-R |

Structural inventory result on d2d385ac09518fea15afa625565ade3fa8e9f523: 556 task definitions and 113 numbered parent/runtime/Assurance requirements resolve through the bidirectional maps; 38 failure rows and 14 UX states are present. This is a structural check, not proof of every contract's correctness. The final candidate must rerun structural/trusted-base checks after this assessment/lifecycle repair. Independent assessment and unresolved-thread closure cannot be supplied by this author table.
