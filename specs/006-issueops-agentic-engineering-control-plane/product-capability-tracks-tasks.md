# Product Capability Tracks — Dependency-Ordered Planning Tasks

```text
STATUS = FUTURE_PLANNING_TASK_MAP
TASKS_AUTHORIZE_IMPLEMENTATION = NO
CURRENT_ACTIVE_SLICE = S2
```

These tasks describe future planning/qualification work only. They do not alter the canonical active task frontier.

## PCT-P — Planning coherence

- [x] **PCT-P001** Define product information architecture: Projects / Work / Automations with supporting Connections, Browser, and Computer capabilities.
- [x] **PCT-P002** Map feature ownership to existing Fehrest/Edara/Mirefa/Nawat/Mission Runtime/UWC/AMAN/Assurance/Trusted Completion boundaries.
- [x] **PCT-P003** Reject parallel Automation runtime/authority/evidence architecture.
- [x] **PCT-P004** Define cross-slice tracks PX/WK/AU/IS without roadmap renumbering.
- [x] **PCT-P005** Define minimum candidate primitive set and Ponytail rejections.
- [ ] **PCT-P006** Obtain independent whole-scope exact-head review of the complete Spec 006 candidate after final reconciliation.

## PX — Project Experience

Future S4+ planning, not active implementation:

- [ ] **PX-001** Specify provenance-aware Project context classes over Fehrest.
- [ ] **PX-002** Define Project instruction precedence/freshness without authority inheritance.
- [ ] **PX-003** Define Project ↔ Work / Automation / Artifact / Evidence association semantics.
- [ ] **PX-004** Define ConnectionBinding references without secret storage in Project context.
- [ ] **PX-005** Benchmark/validate Project context freshness and canonical-vs-derived conflict handling.
- [ ] **PX-006** Re-evaluate generalized non-repository/multi-root Projects only after S4 proves the core context model.

## WK — Work Plane

Future S6/S9 planning, not active implementation:

- [ ] **WK-001** Specify durable WorkSession identity independently from Mission/Attempt/Worker/Host.
- [ ] **WK-002** Specify CapabilityPresence observations and stale/unavailable semantics.
- [ ] **WK-003** Define one append-only Work timeline projection across terminal/connector/browser/computer/artifact/approval evidence.
- [ ] **WK-004** Define local/cloud capability-loss UX and no-silent-migration rules.
- [ ] **WK-005** Define cross-client continuation and Mission/runtime recovery linkage.
- [ ] **WK-006** Falsify whether any Work-specific durable entity beyond WorkSession is necessary.

## AU — Automations and Connections

Future S5+ planning, not active implementation:

- [ ] **AU-001** Finalize AutomationDefinition/TriggerDefinition/TriggerEnvelope schemas under the owning slice.
- [ ] **AU-002** Specify trigger ingress through Case Bus with authenticity, replay, deduplication, and ambiguity handling.
- [ ] **AU-003** Specify trigger-to-WorkflowIntent/Mission compilation and prove message/event receipt cannot become intent automatically.
- [ ] **AU-004** Specify IntegrationDescriptor capability taxonomy and functional/schema validation.
- [ ] **AU-005** Specify ConnectionBinding and credential-capability broker seam.
- [ ] **AU-006** Define preferred/required/forbidden route constraints and no-silent-fallback behavior.
- [ ] **AU-007** Create connector examples/anti-examples for READ/SEARCH/CREATE/UPDATE/DELETE/EXECUTE/UPLOAD/DOWNLOAD/SUBSCRIBE/POLL/WEBHOOK/STREAM.
- [ ] **AU-008** Define provider idempotency/reconciliation contracts and unknown-effect negative oracles.
- [ ] **AU-009** Define long-lived schedule/wait/approval semantics on Mission Runtime/S9 recovery primitives.
- [ ] **AU-010** Design visual-flow UX as declarative intent/topology constraints; prove it does not become a second runtime DAG engine.
- [ ] **AU-011** Qualify read-only connector tracer bullets before effectful connector classes.

## IS-BR — Browser / WebMCP

Future S6+ planning, not active implementation:

- [ ] **IS-BR001** Finalize InteractiveSurface and SurfaceObservation payload contracts for Browser surfaces.
- [ ] **IS-BR002** Qualify ManagedBrowser lifecycle/profile isolation contract.
- [ ] **IS-BR003** Define AttachedUserBrowser blast-radius/credential/privacy contract separately.
- [ ] **IS-BR004** Define RemoteBrowser host/profile/network/recovery contract.
- [ ] **IS-BR005** Qualify route preference: Integration/API -> WebMCP -> semantic browser -> protocol -> visual -> raw input.
- [ ] **IS-BR006** Define WebMCP tool identity binding origin/navigation/document/schema/declaration digests.
- [ ] **IS-BR007** Add hostile WebMCP/tool-poisoning/output-injection/navigation-drift corpus.
- [ ] **IS-BR008** Define upload/download file/effect authority separation.
- [ ] **IS-BR009** Evaluate Playwright as dependency candidate behind a WePLD-owned Browser adapter.
- [ ] **IS-BR010** Evaluate WebDriver BiDi/CDP as protocol oracles without making provider-native types canonical.
- [ ] **IS-BR011** Build BrowserGym/WebArena/WorkArena-class qualification matrix with stale-action, wrong-action, injection, recovery, latency, cost, and intervention metrics.

## IS-CU — Computer Use

Future S6/S7/S8+ planning, not active implementation:

- [ ] **IS-CU001** Finalize InteractiveSurface semantics for desktop/application surfaces.
- [ ] **IS-CU002** Qualify Windows UI Automation / macOS AXUIElement / Linux AT-SPI-class semantic interaction routes by platform.
- [ ] **IS-CU003** Define visual-grounding fallback contract and target freshness cross-checks.
- [ ] **IS-CU004** Finalize InputLease expiry/fencing/ownership contract.
- [ ] **IS-CU005** Define USER_INTERVENTION causal behavior and stale actuation cancellation.
- [ ] **IS-CU006** Decompose screen/window/pointer/keyboard/clipboard/file-picker/drag-drop capabilities and risk classes.
- [ ] **IS-CU007** Define high-risk authentication/financial/admin/security surface policy requirements.
- [ ] **IS-CU008** Define remote host desktop-session identity, fencing, reconnect, and split-brain negative oracles.
- [ ] **IS-CU009** Pin and qualify OSWorld-V2-class benchmark release(s) plus WePLD-specific failure corpus.
- [ ] **IS-CU010** Study UI-TARS Desktop/operator mechanisms as behavior/source candidates without architecture adoption.
- [ ] **IS-CU011** Keep mobile Computer Use and ambient multimodal presence out of the initial implementation tranche.

## S7 — Assurance cross-track tasks

- [ ] **PCT-A001** Define connector supply-chain/secret/network security qualification.
- [ ] **PCT-A002** Define browser/WebMCP prompt-injection and hostile-page assurance suite.
- [ ] **PCT-A003** Define stale target/focus/modal/navigation race tests.
- [ ] **PCT-A004** Define Computer Use input ownership/user-intervention/high-consequence tests.
- [ ] **PCT-A005** Define benchmark measurement contracts with exact source/model/route/host/environment identity.
- [ ] **PCT-A006** Define claim-assessment rules so benchmark success does not become effect authority or Trusted Completion.

## S8 — Controlled effect activation tasks

These remain ineligible until prerequisite canonical authority exists:

- [ ] **PCT-E001** Activate first bounded effectful connector capability.
- [ ] **PCT-E002** Activate first bounded Browser actuation route.
- [ ] **PCT-E003** Activate first bounded Computer Use actuation route.
- [ ] **PCT-E004** Prove human approval flows consume Nawat rather than per-feature approval engines.
- [ ] **PCT-E005** Prove `EFFECT_OUTCOME_UNKNOWN` reconciliation before retry for selected consequential effects.

## S9/S10 — Durable continuation and outcome intelligence

- [ ] **PCT-R001** Add durable Automation schedule/event Mission continuation.
- [ ] **PCT-R002** Add cross-client Work continuation with capability presence/recovery evidence.
- [ ] **PCT-R003** Add route migration/requalification/reconciliation lineage.
- [ ] **PCT-R004** Add browser/computer recovery checkpoints only where safe semantics are proven.
- [ ] **PCT-R005** Add route reliability and automation outcome analytics as evidence, never authority.
- [ ] **PCT-R006** Add cross-project pattern recommendations under Fehrest/Byan without automatic effect grants.

## Source-acquisition follow-up

Before source/dependency use:

- [ ] **PCT-S001** Reverify exact upstream revisions/licenses/notice obligations for every candidate actually entering an owning slice.
- [ ] **PCT-S002** Run Source Acquisition against Activepieces pieces/framework paths before any adaptation/import.
- [ ] **PCT-S003** Treat Zapier/n8n/Make as oracles unless a separate gate proves an admissible use path.
- [ ] **PCT-S004** Qualify Nango/other credential/integration infrastructure before dependency use.
- [ ] **PCT-S005** Re-evaluate Temporal only if buy-vs-build evidence proves Mission Runtime would otherwise duplicate durable machinery; default remains no second orchestrator.
- [ ] **PCT-S006** Qualify Playwright and any browser runtime dependency at the owning Browser gate.
- [ ] **PCT-S007** Pin benchmark/research revisions before using them as acceptance evidence.

```text
TASK_LISTED != TASK_AUTHORIZED
TASK_AUTHORIZED != TASK_QUALIFIED
TASK_QUALIFIED != EFFECT_AUTHORITY
```
