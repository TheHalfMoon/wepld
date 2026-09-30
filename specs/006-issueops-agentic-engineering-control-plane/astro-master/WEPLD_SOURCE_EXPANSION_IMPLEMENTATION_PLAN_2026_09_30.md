# WePLD Source Expansion Implementation Plan — 2026-09-30

```text
STATUS = CANDIDATE_NORMATIVE_PLANNING_AMENDMENT
OBSERVATION_DATE = 2026-09-30
BASE_CANONICAL_MAIN = 0a843a2c0913236d9c93b31abb0d54bbdb023f23
ROADMAP_CHANGE = NONE
TASK_DAG_CHANGE = NONE
NEW_AUTHORITY_DOMAIN = NONE
NEW_CANONICAL_RUNTIME = NONE
NEW_CANONICAL_TASK_STORE = NONE
GLOBAL_IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_EXECUTION_AUTHORITY = NONE
```

This amendment extends the accepted Astro planning package with six founder-authorized source candidates. It does not create a second control plane, runtime, assurance authority, decision authority, collaboration authority, or execution graph. Existing WePLD owners remain canonical.

The founder explicitly states permission to copy/use the requested source code as needed. Public license metadata remains independently recorded. Founder permission is not source admission, dependency admission, runtime qualification, or permission to bypass provenance/NOTICE/custom-grant evidence.

```text
FOUNDER_PERMISSION_REAFFIRMED_2026_09_30 =
  kunchenguid/firstmate,
  kunchenguid/no-mistakes,
  kgoedecke/doop,
  classifier.dev / mrmps/classifier-dev,
  caio0452/jev_search,
  unreallabsai/unreal-agent

FOUNDER_PERMISSION_ASSERTION != SOURCE_ADMISSION
FOUNDER_PERMISSION_ASSERTION != PUBLIC_LICENSE_METADATA
FOUNDER_PERMISSION_ASSERTION != PATH_LEVEL_PROVENANCE
DONOR_PASS != WEPLD_PASS
DONOR_AUTHORITY != WEPLD_AUTHORITY
```

## 1. Exact observed source anchors

| Source | Observed revision / identity | Public rights observed | Initial disposition | Primary WePLD owners / tasks |
|---|---|---|---|---|
| `kunchenguid/firstmate` | `23e5584714e6765cc223a1740d385d0e85f8ad8e` | MIT | SALVAGE/ADAPT crew supervision, worktree isolation mechanics, durable wake/reconciliation, route/backend state, bounded remote secondmate patterns and turn-end supervision guards | Edara, Mission Runtime, UWC; A09, A05, A08, F05/F08, U01/U03, T02, P04 |
| `kunchenguid/no-mistakes` | `a1c06cdaefcefa7cbc6902ac507f68ce9eed14ad` (`1.85.3` release head) | MIT | SALVAGE/ADAPT isolated validation-gate mechanics, complete review coverage accounting, finding lifecycle, safe-repair routing, CI repair custody, exact-head publication interlocks, recovery anchors and fail-closed reconciliation | Assurance, Trusted Completion, Work recovery; A09, A07, F02, F08, S01/S02/S03, T02, U05, B02/B03 |
| `kgoedecke/doop` | `77cb306aad47b9c901979c9d246105958458d7fb` | AGPL-3.0 public repository license; founder separately asserts copy/use permission | BEHAVIOR_REFERENCE first; selectively SALVAGE/ADAPT only when exact custom-rights evidence or AGPL-compatible use is recorded. Mine collaborative agent canvas, sandboxed HTML frame, MCP identity/access inheritance, live presence/activity, design-memory and specialist-pass mechanics | Work/PX/Interactive Surfaces/Fehrest/H01/F06; A09, P01 profile leaf, H01/H02, F03/F04, P05, S01/S02 |
| `mrmps/classifier-dev` (source of `classifier.dev`) | `a17bf2b6353f6234af6e977a463da7cd1975b68e` | MIT | SALVAGE/BENCHMARK typed bulk classification, calibrated confidence, uncertainty escalation, TypeSafe-compatible surface, MCP/CLI/SDK packaging, idempotency/usage accounting and eval harness. Hosted service remains optional | Mirefa/Fehrest/Byan; A09, A04/A05, K03, H01, B03 |
| `caio0452/jev_search` | `ea073f6db48f5bff73ae4b9f2240d2d302fb9dc1` | No public license file observed at this revision; founder asserts copy/use permission | REFERENCE/SALVAGE algorithmic shape only: criteria DSL, keyword-density prioritization, bounded chunking, two-stage search, parallel decision filtering and progressive emission. Reject OpenRouter as a required route | Fehrest/Mirefa; A09, A04, F04, K03 |
| `unreallabsai/unreal-agent` | `1b9f778453f411c029b39b85102aaefb95e7e48d` | MIT | SALVAGE/ADAPT async harness invariants: stable input IDs, inbox deduplication, append-only/forkable sessions, pure tool translators, serializable operations, atomic persistence, context omission accounting, durable operation execution and recovery | Mission Runtime/UWC/Mirefa; A09, A05, F05, U01/U02, F06, A08, O03 |

No later upstream revision is silently substituted. Any later revision requires a fresh acquisition observation and diff before import.

## 2. Priority decision

The sources are intentionally not treated as equally authoritative or equally mature.

```text
PRIORITY_A_MECHANISM_DONORS = unreallabsai/unreal-agent, kunchenguid/no-mistakes, kunchenguid/firstmate
PRIORITY_B_OPTIONAL_PRODUCT_OR_DECISION_DONORS = mrmps/classifier-dev, kgoedecke/doop
PRIORITY_C_REFERENCE_ONLY_UNTIL_REIMPLEMENTED_AND_QUALIFIED = caio0452/jev_search
```

Rationale:

- `unreal-agent` has a clean composable async execution model whose operation/session boundaries align directly with Mission Runtime/UWC without becoming authority.
- `no-mistakes` has mature failure/repair/publication mechanics that can strengthen Assurance and recovery while preserving the existing WePLD rule that a reviewer finding never grants write authority and green CI never decides completion.
- `firstmate` has valuable multi-agent supervision/reconciliation mechanics, but WePLD must mine those mechanisms behind Edara/Mission Runtime rather than adopt Firstmate as the control plane.
- `classifier-dev` is useful for calibrated bulk triage, uncertainty routing and evaluation, but a hosted decision service cannot become a required WePLD dependency and its probabilities never authorize effects.
- `doop` is valuable for optional collaborative design/workspace behavior, agent presence, MCP identity inheritance and sandboxed frame execution. Its public AGPL terms and the founder's asserted custom permission must stay explicit at path-level acquisition time.
- `jev_search` explicitly describes itself as AI-generated and not production-ready. Its architecture may inspire a safer local implementation, but its current network/provider requirement and missing public license file make it unsuitable as a direct core runtime dependency.

## 3. Canonical ownership is unchanged

```text
Work                      owns user-visible work identity/state
AGILLE                    owns plan qualification/decomposition
Fehrest/Maemar            owns source/context facts and projections
Mirefa                    owns model/tool/worker/route qualification
Edara                     owns staffing/team topology/delegation
Mission Runtime           owns Task/Attempt lifecycle, continuation and reconciliation
UWC                       owns normalized worker/tool/runtime adapters
Nawat                     owns protected effect authorization at use
AMAN                      owns risk/security overlays
Assurance                 owns independent review/test/security evidence
Trusted Completion        owns completion decision
Byan                      owns measured learning and policy proposals
Interactive Surfaces      owns browser/computer/design-surface interaction contracts
```

The donor relationship is therefore:

```text
Firstmate supervisor != Edara authority
Firstmate watcher != Mission Runtime authority
No-mistakes gate != Assurance authority
No-mistakes auto-fix != repair authorization
Classifier confidence != Mirefa qualification
Classifier confidence != Nawat authorization
Jev Search match != source truth
Unreal operation manager != Mission Runtime authority
Doop agent != Work authority
Doop MCP OAuth != Nawat grant
Doop frame sandbox != global containment proof
```

## 4. Firstmate mechanism integration contract

### 4.1 Mine these mechanisms

High-value candidate targets include:

```text
README.md
docs/architecture.md
docs/turnend-guard.md
docs/remote-secondmates.md
docs/extension-bindings.md
bin/fm-watch.sh
bin/fm-wake-lib.sh
bin/fm-crew-state.sh
bin/fm-spawn.sh
bin/fm-backend.sh
focused tests covering restart, stale/wedge detection, worktree/endpoint identity and remote-route recovery
```

The useful concepts are:

- one user-facing liaison delegating bounded work to a visible fleet;
- isolated task worktrees to prevent ordinary concurrent Git collisions;
- explicit ship/scout work shapes;
- event-driven supervision that wakes the coordinating layer on actionable evidence rather than token-burning polling;
- distinct declared waits, human decisions, true wedges and dead endpoints;
- durable wake queues / restart reconciliation;
- explicit backend/agent endpoint identity;
- persistent subordinate supervisors (`secondmates`) with isolated homes and state;
- remote-route failure that does not silently fall back to a different local route;
- turn-end guards that detect blind stopping while governed work remains active.

### 4.2 WePLD adaptation

WePLD should adapt these only behind canonical types:

```text
Work / Task / Attempt
EdaraTeam / WorkerRequirement
Mission / WorkSession
RouteQualification
RuntimeEvent
Observation
ContextPackage
NawatDecision
EffectResult
```

A Firstmate-style crew becomes an Edara-selected set of qualified workers. A worktree is an isolation aid, not a security boundary. The Mission Runtime remains the durable owner of Attempt state and restart recovery.

### 4.3 Required negative oracles

```text
WORKTREE_ISOLATION -> NOT_ACCEPTED_AS_SANDBOX
REMOTE_ROUTE_UNAVAILABLE -> NO_SILENT_LOCAL_SUBSTITUTION
QUIET_WORKER_WITH_DECLARED_WAIT -> NOT_MISCLASSIFIED_AS_WEDGE
DEAD_ENDPOINT -> NOT_REPORTED_AS_LIVE_PROGRESS
RESTART -> NO_DUPLICATE_TASK_ADMISSION
TURN_END_WITH_ACTIVE_GOVERNED_WORK -> BLOCK_OR_EXPLICIT_HANDOFF
SECONDARY_SUPERVISOR -> NO_PARENT_OR_SIBLING_AMBIENT_WRITE_AUTHORITY
```

## 5. no-mistakes assurance and repair contract

### 5.1 Mine these mechanisms

Candidate mining areas:

```text
README.md
internal/pipeline/steps/review*.go
internal/pipeline/steps/ci*.go
internal/pipeline/steps/*coverage*_test.go
internal/gate/
internal/branchsync/
recovery-anchor / custody / publication-interlock tests
configuration and generated agent skill contracts
```

High-value behavior:

- run validation in a disposable/isolated worktree;
- model review/test/docs/lint/CI as explicit gates;
- represent findings with action classes such as safe mechanical repair versus human judgment;
- preserve complete changed-file review coverage instead of accepting a clean but partial review;
- apply safe fixes only through a bounded repair path;
- after a repair, bind publication to the exact reviewed/qualified head or route back through review;
- preserve private/unpublished history with recovery anchors before destructive cleanup;
- reconcile rewritten remote/publication bindings without treating preservation evidence as containment evidence;
- record attestations and exact failure state rather than collapsing every CI failure into one boolean;
- fail closed when coverage, custody, head identity or recovery evidence is ambiguous.

### 5.2 WePLD adaptation

No-mistakes must strengthen existing Assurance/repair semantics rather than become an alternate gate authority.

```text
ReviewFinding -> Assurance evidence
safe-fix candidate -> RepairProposal only
RepairProposal -> separate repair authorization
repaired head -> prior review evidence stale unless contract explicitly proves preserved exact coverage
CI attestation -> evidence only
publication interlock -> Work/Trusted Completion delivery control
recovery anchor -> custody/preservation evidence only
```

The existing WePLD rule remains absolute:

```text
REVIEW_FINDING != WRITE_AUTHORITY
AUTO_FIX_CAPABILITY != AUTO_FIX_AUTHORITY
GREEN_CI != COMPLETION
PRESERVATION_PROOF != CONTAINMENT_PROOF
PUBLISHED_PR != ACCEPTED_OUTCOME
```

### 5.3 Required negative oracles

```text
PARTIAL_REVIEW_COVERAGE + ZERO_FINDINGS -> NOT_PASS
REPAIR_ON_STALE_BASE -> NOT_PUBLISH
REMOTE_HEAD_CHANGED_AFTER_REVIEW -> REQUALIFY
REPAIR_TOUCHES_INTENT_SENSITIVE_SCOPE -> HUMAN_OR_EXACT_AUTHORITY_REQUIRED
RECOVERY_ANCHOR_EXISTS -> DOES_NOT_PROVE_CONTENT_LANDED
CI_FAILURE_REPAIR -> MUST_PRESERVE_OR_REESTABLISH_REVIEW_COVERAGE
UNPUBLISHED_PRIVATE_HEAD -> PRESERVE_BEFORE_DESTRUCTIVE_CLEANUP
```

## 6. Unreal Agent async-runtime contract

### 6.1 Mine these mechanisms

Candidate target package:

```text
README.md
harness/session*
harness/coordinator*
harness/context*
harness/tools*
harness/operations*
harness/primitives/
benchmarks/
focused tests for input dedupe, atomic tool-call/operation persistence, cancellation, process output, recovery and session resume
```

Useful invariants observed in the public architecture:

- caller-supplied globally unique input IDs remain stable across redelivery;
- session-scoped inbox deduplicates external/control/crash inputs;
- sessions are append-only, persisted and forkable;
- session-store format is versioned and unsupported versions fail explicitly;
- tool definitions are schema-bound;
- tool translators validate/translate synchronously, perform no I/O, and produce serializable operations;
- operation execution is separate from model-facing tool-call translation status;
- tool-call status and resulting operations are recorded atomically;
- context assembly returns explicit omission/truncation/compaction accounting;
- operation execution is owned by a swappable durable manager;
- provider adapters own provider authentication, cancellation and provider errors.

### 6.2 WePLD adaptation

```text
Unreal Input ID          -> RuntimeEvent/TriggerEnvelope idempotency evidence
Unreal Session           -> WorkSession/Mission evidence, not a replacement store
Unreal Tool Translator   -> UWC adapter validation layer
Unreal Operation         -> effect proposal / bounded executable operation representation
Operation Manager        -> Mission Runtime/UWC mechanism, never Nawat authority
Context omission record  -> ContextPackage provenance/coverage evidence
```

### 6.3 Required negative oracles

```text
REDELIVERED_INPUT_ID -> ONE_ACCEPTED_EVENT
TRANSLATOR_PERFORMS_IO -> QUALIFICATION_FAIL
TOOL_CALL_STATUS_PERSISTED_WITHOUT_OPERATIONS_ATOMICITY -> FAIL
UNSUPPORTED_SESSION_VERSION -> EXPLICIT_BLOCK
CONTEXT_TRUNCATION_WITHOUT_DISCLOSURE -> FAIL
CANCEL_REQUEST -> NOT_SUCCESS_UNTIL_EXECUTOR/PROVIDER_ACK_OR_RECONCILIATION
OPERATION_RETRY -> REQUIRES_EFFECT_RETRY_SAFETY
```

## 7. classifier.dev / calibrated-decision contract

The public service exposes bulk classification, calibrated confidence, TypeSafe-compatible structured decision calls, MCP/CLI/SDK surfaces, idempotency controls and evaluation material. Public requests are forwarded to model providers; the service states that request content is not stored by default, but provider egress still exists. Therefore the hosted route is optional and never the local-authoritative baseline.

### 7.1 Mine these mechanisms

```text
mrmps/classifier-dev@a17bf2b6353f6234af6e977a463da7cd1975b68e
src/jev.ts
src/index.ts
privacy / cost / limiter / billing / idempotency modules
eval/
cli/
sdk/python/
sdk/go/
MCP and skill descriptors
```

Adapt:

- single-label and bounded multi-label typed decisions;
- per-label scores plus calibrated confidence;
- explicit uncertain-case escalation to a stronger route;
- bulk screening so only selected evidence enters expensive model/context stages;
- route/model identity in every result;
- explicit usage/cost accounting;
- stable idempotency identity for billable/retry-sensitive calls;
- benchmark/eval harness design.

### 7.2 Locality rule

```text
LOCAL_ONLY -> hosted classifier route unavailable unless user changes locality policy
HOSTED_CLASSIFIER -> explicit egress + exact provider/route identity
FREE_TIER -> availability/cost optimization only, never architectural dependency
CLASSIFIER_UNAVAILABLE -> no hidden fallback
```

A local calibrated-decision route, if qualified, is preferred for local-authoritative operation. The hosted service can remain an optional comparison arm or user-selected provider.

### 7.3 Decision safety

```text
CONFIDENCE != TRUTH
CONFIDENCE != AUTHORITY
CLASSIFICATION != QUALIFICATION
CLASSIFICATION != COMPLETION
UNCERTAIN -> ABSTAIN_OR_ESCALATE
MATERIAL_ROUTE_CHANGE -> SUCCESSOR_ROUTE_QUALIFICATION_AND_EFFECT_BINDING_WHERE_APPLICABLE
```

## 8. Jev Search algorithmic donor contract

The observed repository warns that it is fully AI-generated and should not be used in production. No public license file was observed at the pinned revision. The founder asserts permission to copy/use; path-level custom-grant evidence remains required if code is imported.

Only mine these ideas initially:

- criteria expression grammar with AND/OR/grouping/quoted phrases;
- source-file discovery and ignore rules;
- keyword-density prioritization;
- bounded chunking;
- high-priority then low-priority scheduling;
- parallel typed-decision filtering;
- confidence thresholding;
- progressive result emission.

WePLD must re-specify and test the parser, escaping, path handling, chunk boundaries, resource ceilings, result ordering and calibration behavior. OpenRouter is not a required dependency.

```text
JEV_SEARCH_CODE = UNQUALIFIED_UNTIL_TASK_TIME
OPENROUTER_REQUIRED_BY_DONOR != OPENROUTER_REQUIRED_BY_WEPLD
SEARCH_MATCH != FEHREST_FACT
SEARCH_CONFIDENCE != NAWAT_AUTHORITY
```

## 9. Doop collaborative-design/workspace contract

Doop provides a useful behavior reference for a collaborative surface where humans and agents edit together in real time. Its public repository is AGPL-3.0; the founder separately asserts permission to copy/use. Any path-level code import must preserve the exact rights basis used.

### 9.1 Mine these mechanisms

High-value candidate targets named by the upstream documentation include:

```text
README.md
shared/agents.ts
server/distill.ts
server/openaiAgent.ts
server/agentModel.ts
MCP server/authentication implementation
canvas/frame access-control and WebSocket presence implementation
frame sandbox implementation
activity/feed/comment/task records
design-memory / durable guideline logic
```

Useful product behavior:

- shareable collaborative canvases with frames/artboards;
- sandboxed HTML frame rendering;
- live cursors/presence and agent status;
- comments anchored to design elements;
- activity feed and streaming agent edits;
- agents authenticating through MCP under the approving user's identity and access;
- private-by-default collaboration plus explicit link sharing;
- specialist roles such as UX/copy/brand/accessibility that can execute bounded passes;
- durable design-memory/style-rule proposals;
- optional provider integrations that fail unavailable rather than silently changing authority.

### 9.2 WePLD adaptation

Doop should become an optional **Collaborative Design Surface** profile under existing Work/PX/Interactive Surfaces contracts, not a new runtime.

```text
Canvas -> Work/PX collaborative surface
Frame -> bounded interactive artifact / preview surface
Agent role -> Edara worker role
MCP identity -> ConnectionBinding / PrincipalScope input
Design memory -> Fehrest-derived proposal; not automatic durable truth
Agent task -> Work/Task projection; Mission Runtime still owns execution
Frame sandbox -> surface containment evidence only
```

### 9.3 Required negative oracles

```text
AGENT_MCP_IDENTITY -> CANNOT_EXCEED_APPROVING_PRINCIPAL_SCOPE
LINK_SHARING -> NEVER_IMPLICIT
FRAME_HTML -> CANNOT_ESCAPE_FRAME_SANDBOX
FRAME_SANDBOX -> NOT_GLOBAL_PROCESS/FS/NETWORK_CONTAINMENT
DESIGN_MEMORY_PROPOSAL -> NOT_AUTO_ADMITTED_AS_CANONICAL_RULE
AGENT_SPECIALIST_PASS -> DOES_NOT_AUTHORIZE_EFFECTS_OUTSIDE_TASK
UNCONFIGURED_MODEL_PROVIDER -> WAIT/UNAVAILABLE, NOT_SILENT_SUBSTITUTE
```

## 10. Unified source-to-WePLD mapping

| Capability | Primary donor(s) | Canonical owner | Existing task owners |
|---|---|---|---|
| multi-agent crew supervision | Firstmate | Edara + Mission Runtime | A05, F05, U01/U03, T02 |
| event-driven worker wake/liveness | Firstmate | Mission Runtime | A08, F08, U01, P04 |
| exact-head validation/publication gate | no-mistakes | Assurance + Work delivery | A07, F02, S01/S02/S03, T02 |
| bounded safe repair + re-review | no-mistakes | Repair/Assurance/Trusted Completion | F08, U05, S01/S02/S03 |
| async serializable operations | Unreal Agent | Mission Runtime + UWC | A05, F05/F06, U01/U02 |
| input idempotency/session recovery | Unreal Agent + Firstmate | Mission Runtime | A08, U01, F08 |
| calibrated bulk decision/triage | classifier-dev | Mirefa + Fehrest + Byan | A04/A05, K03, B03 |
| prioritized criteria search | jev_search | Fehrest + Mirefa | A04, F04, K03 |
| collaborative agent design surface | Doop | Work/PX + Interactive Surfaces | H01/H02, P05, F03/F04, P01 profile leaf |
| MCP user/access inheritance | Doop + classifier-dev | H01 + ConnectionBinding + Nawat | H01/H02, F06 |

No row creates implementation authority. Each owning task must have an accepted exact grant before code import or runtime changes.

## 11. Cross-source architecture

The combined design remains one WePLD architecture:

```text
Human intent
  -> Work / AGILLE
  -> Fehrest context and source facts
  -> Mirefa qualification / calibrated triage where useful
  -> Edara bounded staffing
  -> Mission Runtime Task/Attempt lifecycle
  -> UWC worker/tool adapters and serializable operations
  -> Nawat exact effect-time authorization
  -> execution / receipts / reconciliation
  -> Assurance review-test-security evidence
  -> separately authorized repair when needed
  -> Trusted Completion acceptance decision
  -> Work delivery/recovery
  -> Byan measured learning proposals
```

Optional collaborative design adds only a surface around this loop. It does not fork the loop.

## 12. First tracer bullets

### 12.1 Crew supervision tracer

```text
ONE Work scope
TWO child Tasks
ONE ship-style task
ONE scout/investigation task
ONE Edara staffing decision
ONE isolated worktree per modifying task
ONE durable Attempt identity per worker
ONE restart/resume drill
ONE declared-wait drill
ONE dead/wedged endpoint distinction drill
NO multi-host requirement
NO silent backend substitution
```

Acceptance requires the coordinator to resume from durable state without duplicate admission, preserve worker/task identity, distinguish waiting from failure, and never treat worktree isolation as security containment.

### 12.2 Assurance/publication tracer

```text
ONE bounded code change
ONE independent review route
ONE deterministic test/lint set
ONE complete changed-path review coverage record
ONE safe mechanical repair fixture
ONE intent-sensitive repair fixture that must stop for authority
ONE head-change-after-review fixture
ONE publication interlock
ONE recovery-anchor/custody fixture
```

Acceptance requires the reviewed/qualified head to remain the publication head or to be requalified. Zero findings with incomplete coverage is not PASS.

### 12.3 Calibrated search/decision tracer

```text
LOCAL_EXACT_OR_LEXICAL_PREFILTER = ON
JEV_SEARCH_STYLE_PRIORITY_SCHEDULING = REIMPLEMENTED_LOCALLY
CALIBRATED_DECISION_ROUTE = LOCAL_IF_QUALIFIED
HOSTED_CLASSIFIER_ROUTE = OPTIONAL_EXPLICIT_EGRESS_ONLY
ABSTENTION = REQUIRED
PROGRESSIVE_RESULTS = ALLOWED_WITH_PROVENANCE
```

Benchmark simple deterministic/lexical retrieval against decision-assisted filtering on the same corpus. Promote only if measured accepted-outcome/precision/recall gains justify cost, latency and privacy tradeoffs.

### 12.4 Collaborative design tracer

```text
ONE local collaborative canvas
TWO bounded frames
ONE human editor
ONE qualified agent
PRIVATE_BY_DEFAULT = YES
LINK_SHARING = OFF
AGENT_ACCESS = HUMAN_SCOPE_OR_NARROWER
FRAME_HTML = SANDBOXED
HOSTED_MODEL_REQUIRED = NO
DESIGN_MEMORY_AUTO_ADMISSION = NO
```

Acceptance verifies identity inheritance, frame containment, provenance of agent edits, explicit sharing state and truthful unavailability when an optional model route is absent.

## 13. Security hardening matrix

| Threat | Required control / negative oracle |
|---|---|
| worktree treated as security sandbox | explicit invariant and security test reject that claim |
| quiet valid wait treated as failure | structured wait reason/owner/recheck semantics |
| dead worker endlessly reported as progress | endpoint generation/liveness and bounded escalation |
| duplicated wake/input after restart | stable input/idempotency identity |
| stale worker writes after successor | existing lease epoch/fencing token remains controlling |
| partial review reported as clean | complete reviewable-path coverage required |
| safe-repair route changes intent | intent-sensitive scope requires separate authority |
| repair published on changed remote/head | exact-head/custody interlock; re-review when proof breaks |
| recovery evidence mistaken for content delivery | preservation/custody evidence kept separate from containment/delivery proof |
| decision confidence used as authorization | explicit type boundary and tests |
| hosted classifier silently receives local-only content | locality/egress policy blocks route |
| classifier/provider silently changes | route identity + no-silent-fallback |
| Jev Search parser accepts ambiguous/injected criteria | reimplemented parser with adversarial grammar/escaping corpus |
| Doop-style agent exceeds approving user scope | principal/connection/effect checks at use |
| shared design link becomes public implicitly | private default + explicit share transition receipt |
| sandboxed frame treated as host containment | separate frame and host containment claims |
| design memory becomes durable policy automatically | proposal-only until normal Fehrest/policy admission |

## 14. Benchmark obligations

No donor benchmark establishes WePLD superiority.

Preregister at B01/B02/B03 as applicable:

```text
crew: duplicate-work rate, restart recovery, blocked-state liveness, supervisor token/cost overhead, accepted outcome rate
assurance: defect catch rate, false-positive burden, review coverage completeness, repair requalification rate, publication-head mismatch rate
async runtime: duplicate-input rate, lost-wakeup rate, recovery correctness, cancellation/unknown-outcome correctness, operation persistence overhead
decision/search: precision, recall, calibration error, abstention quality, cost, latency, context-token savings, provider/route failure behavior
design collaboration: access leakage = 0 target, sandbox escape = 0 target, edit attribution completeness, reconnect/replay correctness, agent/human conflict recovery
```

The benchmark comparison should use the same available worker/model/task budget wherever possible.

## 15. Source acquisition obligations before import

Every imported/adapted path requires a normal A09 or owning-task acquisition record with at least:

```text
repository/source identity
exact revision/tree/blob
selected path/file set
public license/NOTICE
founder custom permission evidence when relied upon
package/release mapping
code/test evidence
transitive dependencies
build/install/import hooks
network behavior
remote-code/custom-loader behavior
supported OS/toolchain/hardware
advisory/maintenance observation date
data/secret boundary
authority boundary
adaptation/porting decision
conformance fixtures
negative oracles
benchmark evidence
performance budget
rollback/removal/replacement route
residual limitations
decision owner
```

Do not bulk-import entire applications just because source permission exists.

## 16. Import posture by source

```text
FIRSTMATE
  SALVAGE: watcher/wake/state/reconciliation tests and algorithms where portable
  ADAPT: crew/secondmate semantics into Edara/Mission Runtime
  REJECT: Firstmate as canonical WePLD control plane

NO_MISTAKES
  SALVAGE: coverage, finding, custody, exact-head, recovery-anchor, CI repair tests/algorithms
  ADAPT: gates into Assurance and bounded repair
  REJECT: reviewer or auto-fix path as acceptance/write authority

UNREAL_AGENT
  SALVAGE: serializable operation/session/idempotency primitives and tests where compatible
  ADAPT: coordinator/translator/operation-manager mechanics behind Mission Runtime/UWC
  REJECT: alternate effect authority

CLASSIFIER_DEV
  SALVAGE: request/decision/eval/idempotency/observability code where task-qualified
  ADAPT: bulk triage and calibrated abstention into Mirefa/Fehrest
  REJECT: hosted service as mandatory dependency

JEV_SEARCH
  REFERENCE/SALVAGE: parser/search scheduling ideas only after fresh code audit
  REIMPLEMENT: production-safe parser, local route, fixtures and bounds
  REJECT: current OpenRouter requirement as architecture

DOOP
  BEHAVIOR_REFERENCE first
  SALVAGE/ADAPT: only paths with explicit rights basis compatible with intended distribution
  REJECT: Doop as second Work/runtime/identity authority
```

## 17. Zero-cost/local-first constraint

This plan does not require paid APIs, hosted providers, paid SaaS or founder-funded cloud infrastructure.

```text
CORE_LOOP = LOCAL_AUTHORITATIVE
HOSTED_DECISION = OPTIONAL
HOSTED_MODEL = OPTIONAL
HOSTED_DESIGN_SERVICE = OPTIONAL
PAID_ROUTE_REQUIRED_FOR_CORE = NO
SILENT_CLOUD_FALLBACK = PROHIBITED
```

If an optional free service changes limits or disappears, core functionality must degrade truthfully rather than substitute a paid or hosted route.

## 18. Planning closure

```text
NEW_TASK_IDS = 0
NEW_ROADMAP_NODES = 0
NEW_AUTHORITY_ROOTS = 0
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_EXECUTION_AUTHORITY = NONE
PLANNING_CONTENT_COMPLETE = YES
UNOWNED_NEW_PLANNING_GAPS = 0
IMPLEMENTATION_READY = ONLY_AFTER_EXACT_HEAD_INDEPENDENT_REVIEW_AND_CANONICAL_ACCEPTANCE
REVIEW_UNAVAILABLE_OUTCOME = REVIEW_BLOCKED
```

This is a planning claim only. It becomes canonical planning input only after exact-head deterministic validation, independently qualified review, finding reconciliation, guarded merge and post-merge integrity. Each later implementation leaf still requires its normal dependency and exact path/effect/source/dependency grant.