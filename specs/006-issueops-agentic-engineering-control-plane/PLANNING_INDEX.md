# Spec 006 — Planning Index

```text
STATUS = ACTIVE_SPEC006_PLANNING_AND_EXECUTION_INDEX
SPEC = 006_ISSUEOPS_AGENTIC_ENGINEERING_CONTROL_PLANE
CURRENT_ACTIVE_FRONTIER = ASTRO / S3 + cross-slice acquisition preparation
IMPLEMENTATION_AUTHORITY = TASK_SPECIFIC_EXACT_GRANTS_ONLY
SOURCE_ADMISSION = TASK_SPECIFIC_ONLY
DEPENDENCY_ADMISSION = TASK_SPECIFIC_ONLY
```

This index defines the recommended reading order and ownership map for the Spec 006 planning and dependency-ordered execution package. It does not create blanket implementation authority: current authority is derived from canonical task prerequisites plus exact accepted path/effect/source/dependency grants. Live GitHub state must be re-read before mutation.

## 1. Start here

0. `astro-master/WEPLD_CANONICAL_MASTER_BUILD_PLAN.md` — accepted Astro roadmap refinement, current execution-frontier interpretation, capability ownership and no-unowned-gap rule.
0. `astro-master/WEPLD_MUSE_EXECUTION_HANDOFF.md` — 63-task dependency graph and bounded task contracts.
0. `astro-master/WEPLD_DECISION_AND_GAP_LEDGER.md` — all known gaps/limitations with owner and closure gate.
0. `astro-master/WEPLD_LOCAL_INTELLIGENCE_CAPABILITY_AMENDMENT.md` + `astro-master/INTELLIGENCE_SOURCE_INTAKE.md` — OCR/RAG/memory/typed decisions/tools/browser/desktop/event intelligence and the 2026-09-23 donor/source additions.

1. `spec.md` — parent product requirements.
2. `plan.md` — parent product/roadmap/tracer-bullet architecture.
3. `product-capability-tracks-spec-addendum.md` — Projects / Work / Automations / Connections / Browser / WebMCP / Computer Use product-shaping requirements.
4. `product-capability-tracks-plan.md` — PX/WK/AU/IS cross-slice integration; sections 14–17 own the eight-feature completeness matrix, all failure/UX obligations and product traceability. `analyze.md` owns supporting-package bidirectional traceability. Neither matrix nor internal assessment substitutes for independent acceptance.
5. `acceptance.md` — parent planning-coherence acceptance criteria.
6. `product-capability-tracks-acceptance.md` — added product-capability planning acceptance criteria.
7. `data-model.md` — canonical shared domain field vocabulary except where a dedicated contract explicitly owns a type.
8. `tasks.md` — parent dependency-ordered planning tasks.
9. `product-capability-tracks-tasks.md` — dependency-ordered future task map for the added tracks.

## 2. Normative contract package

### Issue / provider / retrieval / content

- `contracts/case-provider.md`
- `contracts/retrieval-rag.md`
- `contracts/untrusted-content.md`
- `contracts/case-bus.md`

### Worker / execution / authority-adjacent boundaries

- `contracts/worker-delegation.md`
- `contracts/runtime-execution-fabric.md`
- `contracts/runtime-distributed-safety-addendum.md`
- `contracts/behavior-policy-boundary.md`

### Automations / connections

- `contracts/automation-connections.md` — canonical Spec 006 owner for `AutomationDefinition`, trigger envelope semantics, `IntegrationDescriptor`, and `ConnectionBinding`.

### Browser / web / computer interaction

- `contracts/web-agent-boundary.md`
- `contracts/interactive-surfaces.md` — canonical Spec 006 owner for `InteractiveSurface`, browser-mode distinctions, and `InputLease`.

### Assurance / review

- `contracts/assurance-fabric.md`
- `contracts/review-independence.md`
- `contracts/command-surface.md`

## 3. Normative planning addenda

These extend the parent `spec.md` / `plan.md` / `acceptance.md` without changing roadmap numbering:

- `product-capability-tracks-spec-addendum.md`
- `product-capability-tracks-plan.md`
- `product-capability-tracks-acceptance.md`
- `product-capability-tracks-ponytail.md`
- `assurance-fabric-spec-addendum.md`
- `assurance-fabric-plan.md`
- `runtime-execution-fabric-spec-addendum.md`
- `runtime-execution-fabric-acceptance.md`
- `omnigent-plan-hardening-addendum.md`
- `web-agent.md`
- `web-agent-acceptance.md`

If an addendum and parent document appear to conflict, treat the planning package as **not internally coherent** until reconciled; do not silently choose one.

The parent `plan.md` diagram names the Intent / Plan Compiler. Earlier `Workflow Engine` wording denotes those same planning/definition mechanics feeding Edara/Mirefa/Nawat/Mission Runtime, never a second durable orchestration runtime.

The September 6 contract repairs define WorkSession/Mission cardinality in `data-model.md`, make TriggerEnvelope a RuntimeEvent payload, CapabilityPresence/SurfaceObservation ordinary Observation payloads, ReviewFinding a canonical Finding projection, and AuthorityGrant/EffectReceipt semantic aliases of NawatDecision/EffectResult. Dedicated contracts own their fields; these names do not create duplicate stores or authorities.

Read `reviews/adversarial-pre-change-review-2026-09-06.md` for the pre-repair findings and explicit coverage limitations, and `research/adversarial-mechanism-recheck-2026-09-06.md` for fresh pinned source/documentation evidence. Both are review/research input, not independent acceptance of their author's patch. Historical September 2/4 review anchors remain historical; their `CURRENT_*` labels are not live references. The September 2 list contains 16 findings (7 high, 8 medium, 1 low), despite its summary count of 15. This accounting correction does not rewrite the old artifact.

## 4. Task maps

- `product-capability-tracks-tasks.md`
- `assurance-fabric-tasks.md`
- `professional-plan-hardening-tasks.md`
- `openhands-assurance-integration-tasks.md`
- `omnigent-execution-fabric-integration-tasks.md`
- `runtime-distributed-safety-tasks.md`
- `web-agent-tasks.md`

Task-map presence does not activate implementation. The canonical owning slice/authority artifact remains controlling. As of the 2026-09-23 live snapshot, ASTRO-G01 and ASTRO-F01 are canonical; PR #342 is the ASTRO-B01 candidate, PR #343 is the ASTRO-C01 candidate, and ASTRO-A01/A04..A09 are dependency-ready but still require their own exact task/acquisition/authority gates.

## 5. Source-acquisition / mechanism research

### General source-acquisition boundary

- `source-acquisition.md`
- `source-acquisition-product-capability-tracks-addendum.md`
- `research/native-assurance-source-acquisition-2026-09-02.md`

### Specific mechanism quarries

- `research/adversarial-mechanism-recheck-2026-09-06.md`
- `research/product-capability-source-study-2026-09-06.md`
- `research/munder-difflin-2026-09-01.md`
- `research/openhands-qualified-mechanism-extraction-2026-09-02.md`
- `research/omnigent-qualified-mechanism-extraction-2026-09-04.md`

Research records do not admit source, dependencies, processes, providers, models, browsers, remote workers, network access, computer control, or connector execution.

## 6. Review / reconciliation history

- `reviews/fable-2026-08-31-reconciliation.md` — historical predecessor architecture review/reconciliation.
- `reviews/professional-whole-plan-review-2026-09-02.md` — historical internal hardening review; its footer under-counted the enumerated findings and must not be used as final exact-head review accounting.
- `reviews/professional-whole-plan-review-2026-09-04.md` — latest historical internal whole-plan hardening review before the 2026-09-06 product-capability extension.
- later exact-head whole-plan review artifacts supersede historical status while preserving history.

No internal/self-authored planning review satisfies the required independent acceptance review. The 2026-09-06 product-capability extension therefore makes all prior whole-plan acceptance-critical reviews historical until a fresh exact-head whole-scope independent review exists.

## 7. Ownership map

```text
Case/provider semantics                    -> data-model + case-provider
RAG/source/access                          -> data-model + retrieval-rag
untrusted instruction boundary             -> untrusted-content
inter-worker / trigger ingress             -> case-bus
automation/integration/connection types     -> automation-connections
worker requirements/routing                -> data-model + worker-delegation
server/host/runner/runtime fabric          -> runtime-execution-fabric
split-brain/event/runtime safety           -> runtime-distributed-safety-addendum
behavior policy                            -> behavior-policy-boundary
browser/WebMCP existing web-agent boundary -> web-agent-boundary
shared Browser/Computer surface semantics  -> interactive-surfaces
review/security/test assurance             -> assurance-fabric
reviewer independence                      -> review-independence
user command catalog                       -> command-surface
shared types not otherwise owned           -> data-model
```

Cross-slice product ownership:

```text
PX Project Experience      -> Fehrest-backed product surface; no authority
WK Work Plane              -> durable session/evidence surface; no execution engine
AU Automations/Connections -> trigger/integration planning; no orchestration engine
IS Interactive Surfaces    -> Browser/Computer interaction primitives; no effect authority
```

## 8. Cross-cutting invariants

```text
PLANNING != IMPLEMENTATION_AUTHORITY
SOURCE_RESEARCHED != SOURCE_ADMITTED
PROVIDER_CAPABILITY != QUALIFIED_CAPABILITY
POLICY_ALLOW != NAWAT_GRANT
SERVER != HOST != RUNNER != WORKER != ATTEMPT
WORK_SESSION != MISSION
MISSION != ATTEMPT
WORKTREE_ISOLATION != SANDBOX
PROCESS_TREE_CONTAINMENT != FS_OR_NETWORK_ISOLATION
INTEGRATION != CONNECTION
CONNECTION != CREDENTIAL
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
AUTOMATION_DEFINITION != EXECUTION_AUTHORITY
TRIGGER_RECEIVED != WORKFLOW_INTENT
MESSAGE_RECEIVED != WORKFLOW_INTENT
CAPABILITY_PRESENT != CAPABILITY_QUALIFIED
CAPABILITY_QUALIFIED != EFFECT_AUTHORITY
MANAGED_BROWSER != ATTACHED_USER_BROWSER
BROWSER_COOKIE_STATE = CREDENTIAL_BEARING_STATE
WEBMCP_TOOL_DECLARATION = UNTRUSTED_PAGE_INPUT
WEBMCP_TOOL != TRUSTED_TOOL
SCREEN_CAPTURE != INPUT_AUTHORITY
INPUT_CONTROL != GLOBAL_MACHINE_AUTHORITY
USER_INTERVENTION != EXECUTION_NOISE
REVIEW_OUTCOME != COMPLETION_DECISION
DIFFERENT_VENDOR_ALONE != REVIEW_INDEPENDENCE_PROOF
RETRIEVAL_SCORE != TRUTH
BROWSER_SNAPSHOT_STALE != VALID_ACTION_TARGET
STALE_SURFACE != SAFE_TO_ACT
TRANSPORT_RETRYABLE != EFFECT_RETRY_SAFE
UNKNOWN_EFFECT_OUTCOME != SAFE_TO_RETRY
RECONCILIATION != REEXECUTION
PREREQUISITE_EFFECT_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_BLOCKED
ROUTE_AVAILABILITY != ROUTE_QUALIFICATION
ROUTE_QUALIFICATION != EFFECT_AUTHORITY
SILENT_ROUTE_FALLBACK = PROHIBITED
NEW_EXACT_HEAD -> PRIOR_ACCEPTANCE_CRITICAL_EVIDENCE_STALE
```

## 9. Roadmap placement

```text
S2 = prerequisite identity/storage foundations only; added capability execution remains inactive
S3 = trusted intake/process + host/runner/containment/effect/input-ownership prerequisites
S4 = Fehrest/RAG/source generation/access + PX Project Experience foundation
S5 = workflow/spec planning + AutomationDefinition/trigger/route-constraint planning
S6 = Mission Runtime/UWC/Edara/Mirefa/Nawat integration + WK/AU/IS interoperability
S7 = Native Assurance + connector/browser/WebMCP/Computer Use qualification
S8 = controlled repair/effect dependency + bounded Automation/Browser/Computer actuation
S9 = complete evidence/runtime/quality/recovery + long-lived Automation/Work continuation
S10 = Fehrest expansion + Byan dynamic graph / cross-project and historical outcome intelligence
```

No roadmap renumbering is implied. Canonical `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md` and `product-capability-tracks-plan.md` section 13 govern this placement. Federation, organization policy and scheduling extensions are conditional follow-on candidates, not additions to canonical S10's required scope. Their safety prerequisites cannot be postponed until analytics; Byan learns from outcomes and never authorizes effects.

## 10. Product capability maturity

```text
LEVEL 0 — DISCOVER
LEVEL 1 — OBSERVE
LEVEL 2 — PROPOSE
LEVEL 3 — ACT WITH EXPLICIT APPROVAL
LEVEL 4 — ACT UNDER SCOPED AUTHORITY
LEVEL 5 — DURABLE AUTONOMOUS EXECUTION

MATURITY_LEVEL != AUTHORITY
AUTONOMY_MODE != AUTHORITY
```

## 11. Initial explicit non-goals

```text
new Automation Runtime
new Browser/Computer authority engines
project memory as vector database
global computer_access boolean
screenshot-first Browser/Computer architecture
silent browser-profile synchronization to cloud
WebMCP as trusted/core authority model
Temporal as default runtime dependency
full n8n/Zapier/Activepieces platform import
Astra-like ambient multimodal presence in the initial scope
mobile Computer Use in the initial scope
```

## 12. Acceptance and execution sequence

The historical Spec 006 planning package has already progressed beyond PR #241. Do not use a hard-coded historical PR as the execution frontier.

For every new Astro plan amendment or execution task:

1. read trusted canonical governance from live `main`;
2. re-read the current Astro master, handoff, gap ledger and relevant task records;
3. verify every declared dependency is canonically accepted;
4. verify exact current path/effect/source/dependency authority for the bounded task;
5. run Spec Kit / Ponytail FULL / Source Acquisition Check as applicable;
6. run exact-head deterministic gates;
7. obtain qualified independent engineering review and applicable security review;
8. reconcile every material finding and prove zero unresolved material threads;
9. invalidate and rerun freshness-dependent evidence after any head change;
10. accept and merge only with exact-head evidence and the guarded expected-head merge;
11. verify post-merge canonical integrity before unlocking successors.

Current accepted predecessor evidence is recorded in the Astro master/handoff. Open PRs, “mergeable” state, task-file presence, or a green status never substitute for this sequence.

```text
DEPENDENCY_READY != AUTHORIZED
OPEN_PR != ACCEPTED
GREEN_CI != COMPLETION
MERGED_TASK != SUCCESSOR_AUTHORITY_UNLESS_GRAPH_AND_GRANT_BOTH_ALLOW
```
