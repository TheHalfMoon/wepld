# WePLD Local Intelligence Capability Amendment

```text
STATUS = BOUNDED_CROSS_CUTTING_PLAN_AMENDMENT
BASE_OBSERVED = 666e62d7d9e040505baca277a474d734afcc07a0
ROADMAP_CHANGE = NONE
TASK_DAG_CHANGE = NONE
NEW_AUTHORITY_DOMAIN = NONE
NEW_CANONICAL_DATABASE = NONE
IMPLEMENTATION_AUTHORITY = INHERIT_EXISTING_TASK_GRANTS_ONLY
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_EXECUTION_AUTHORITY = NONE
```

This amendment integrates the founder-requested local OCR/document intelligence, retrieval/RAG, scoped memory, typed decisions/PLD, tool/skill discovery, browser acquisition, desktop interaction and event intelligence into the existing WePLD architecture. It is a product-composition and planning amendment only. It does not create a second roadmap, a competing authority root, a new durable runtime or a blanket donor admission.

The existing P0 + S1-S10 roadmap, 63-task Astro DAG, canonical field owners, trusted-bootstrap rules, Source Acquisition Check, Nawat effect-time authority, Assurance and Trusted Completion remain controlling.

## 1. Product objective

The user should be able to enable only the local intelligence capabilities needed for a Work item or project while preserving one governed engineering truth.

```text
SOURCE
-> perceive when needed
-> derive source-backed facts
-> retrieve minimum sufficient evidence
-> make calibrated candidate decisions when useful
-> plan
-> select qualified models/tools/workers
-> execute only through authorized effects
-> collect receipts
-> independently evaluate
-> determine completion
-> learn from accepted outcomes
```

Target user-facing capabilities:

```text
OCR / DOCUMENT INTELLIGENCE
RAG / RETRIEVAL
SCOPED MEMORY
PLD / TYPED DECISIONS
TOOLS / SKILLS / MCP
BROWSER / WEB ACQUISITION
DESKTOP / TERMINAL INTERACTION
EVENT INTELLIGENCE / ACTION CARDS
```

All are optional and replaceable.

```text
OPTIONAL_CAPABILITY != OPTIONAL_GOVERNANCE
LOCAL_MODEL != TRUSTED_MODEL
MODEL_CONFIDENCE != AUTHORITY
RETRIEVAL_SCORE != TRUTH
OCR_OUTPUT != SOURCE_TRUTH
TOOL_DISCOVERY != INVOCATION_GRANT
DESKTOP_ACCESS != EFFECT_AUTHORITY
ACTION_CARD != EFFECT
```

## 2. Architecture decision: no new intelligence authority domain

"Intelligence Fabric" may be used as a product/UX grouping name only. It does not own durable truth.

Canonical ownership stays:

| Concern | Canonical owner |
|---|---|
| Work, projects, rooms, user-visible outcomes | Work |
| Intent/specification/plan qualification | AGILLE |
| Source facts, retrieval evidence, memory, ContextPackage | Fehrest / Fehrest.Maemar |
| Model/provider/tool/skill/capability qualification | Mirefa |
| Minimum-sufficient worker topology | Edara |
| Mission/Task/Attempt execution lifecycle | Mission Runtime |
| Normalized worker/tool/interactive adapters | UWC |
| Identity, grants, effect-time revalidation | Nawat |
| Risk/security signals | AMAN |
| Review/Test/Security evaluation | Assurance |
| Exact-outcome acceptance | Trusted Completion |
| Outcome/benchmark analytics and learning candidates | Byan |

No donor may become a competing owner.

```text
DeepSeek-OCR-2 != WePLD Perception
SemIf != WePLD Typed Decisions
Decider != WePLD Typed Decisions
Nimble != WePLD Typed Decisions
Treg != WePLD Capability Registry
Google AX != WePLD Runtime
Desktop Commander != WePLD Desktop Authority
TinyFish/AgentQL != WePLD Browser Authority
Laya != WePLD Work
Morize != WePLD Project Brain
```

They are mechanisms or behavior references behind WePLD-owned contracts.

## 3. End-to-end composition

```text
User / Work
    |
    v
Source or Intent
    |
    +-----------------------------+
    |                             |
    v                             v
Perception                    Native source readers
OCR / Vision / Audio          Code / docs / events
    |                             |
    +-------------+---------------+
                  |
                  v
            Fehrest / Maemar
      Source facts and generations
                  |
                  v
           Retrieval Planner
 Exact / Lexical / Metadata / Syntax /
 Symbol / Reference / Graph / Vector /
 Rerank / Freshness
                  |
                  v
             ContextPackage
                  |
      +-----------+-----------+
      |                       |
      v                       v
    AGILLE            CalibratedDecision
                         PLD/Jev-style
      |                       |
      +-----------+-----------+
                  |
                Mirefa
                  |
                Edara
                  |
           Mission Runtime
                  |
           EffectProposal
                  |
                Nawat
                  |
          enforcing adapter
                  |
 +--------+-------+--------+----------+
 |        |       |        |          |
files  terminal browser  desktop   connector
 |        |       |        |          |
 +--------+-------+--------+----------+
                  |
             EffectReceipt
                  |
            AMAN / Assurance
                  |
          Trusted Completion
                  |
                Byan
```

## 4. Cross-cutting capability contract

A future owning task should freeze a shared logical `CapabilityProfile` vocabulary rather than create a new subsystem.

Proposed fields:

```text
CapabilityProfile
- capability_id
- capability_kind
- canonical_owner
- provider_or_adapter_identity
- package_or_model_identity?
- exact_revision_or_digest
- source_acquisition_ref
- locality
- supported_platforms
- hardware_requirements
- data_classes
- requested_effect_classes
- network_requirement
- egress_profile
- qualification_state
- benchmark_evidence_refs
- recovery_profile
- fallback_policy
- residual_limitations
```

This record describes capability availability and qualification. It does not grant use.

```text
CapabilityProfile != AuthorityGrant
CapabilityAvailable != InvocationAuthorized
CapabilityQualified != OutcomeAccepted
```

The owning freeze path is split across existing tasks rather than adding a new DAG node:
- acquisition/source identity: ASTRO-A09;
- capability package/admission shape: ASTRO-H01;
- model/harness route identity: ASTRO-A05/F05;
- effect authority: ASTRO-F06;
- profile-specific manifests: ASTRO-K01/K02/K03/P03/P04/P05/H02/O03.

## 5. User capability preferences

User choice is separate from authority.

Use three capability-selection preferences:

```text
OFF
ASK
AUTO
```

Semantics:

- `OFF`: Mirefa must not select the capability for that scope.
- `ASK`: selection requires an explicit user choice before invocation.
- `AUTO`: Mirefa may select a qualified route when its task contract permits selection.

`AUTO` does not authorize filesystem, process, browser, network, connector, publication, purchase, message-send or other effects. Nawat still decides each protected effect under current scope.

Do not add an `ALWAYS_ALLOW` setting that bypasses effect-time policy. Reusable grants, where canonical policy supports them, must still have scope, epoch, expiry/revocation semantics and risk limits.

## 6. Locality and no-silent-fallback contract

Local-first means local-authoritative, not a false claim that every connector works without a network.

Required locality states:

```text
LOCAL_ONLY
CONTROLLED_EGRESS
HYBRID
```

A capability route records its actual locality. Examples:
- local OCR model: `LOCAL_ONLY`;
- GitHub connector: `CONTROLLED_EGRESS`;
- local browser against the public web: local execution + controlled network egress;
- hosted model: controlled egress, never local.

If the user selects `LOCAL_ONLY` and the local route becomes unavailable:

```text
LOCAL_ROUTE_UNAVAILABLE
```

must be returned. Silent substitution to a hosted provider is prohibited.

A provider/model/harness/quantization/host change that is material to route qualification or effect binding creates a new route identity. Execution on that materially changed route requires a successor `EffectProposal` and successor `NawatDecision` bound to the new `RouteQualification`, plus the appropriate new Attempt/evidence identity. A route change that is not material to qualification or effect binding does not by itself require a successor authorization.

## 7. Hardware-aware routing

Mirefa should eventually consume a source-backed `HardwareProfile` observed by Project Doctor / qualified host machinery.

Candidate fields:

```text
os
architecture
cpu
ram
gpu_vendor
gpu_model
vram
npu?
driver/runtime versions
available_disk
power_state?
resource_pressure?
```

Each model route needs a `ModelExecutionProfile` containing at least:

```text
model_identity
model_revision
runtime
quantization
required_ram
required_vram
supported_os
supported_accelerators
context/input limits
modality support
latency observations
quality/calibration evidence
privacy/locality class
```

Routing rule:

```text
NO_MODEL_WHEN_A_DETERMINISTIC_TOOL_IS_MORE_PRECISE
```

Examples:
- exact file lookup -> exact/path search;
- symbol definition -> symbol index;
- call relation -> code graph;
- small typed classification -> qualified small decision model;
- broad calibrated decision batch -> SemIf/Decider-style local route;
- complex evidence-grounded typed judgment -> qualified Nimble-like route;
- scanned document -> qualified OCR route;
- architecture synthesis -> general reasoning model plus deterministic verification, not PLD alone.

## 8. Perception and document intelligence

### 8.1 Source truth

The original artifact stays canonical source evidence. OCR/parser output is a derived projection.

```text
OriginalArtifact
-> ArtifactGeneration
-> PerceptionProjection
```

Candidate projection vocabulary:

```text
page
region
text_block
heading
paragraph
table
cell
figure
caption
equation
reading_order
bounding_box
source_span
confidence_observation?
```

Every projection must bind to:

```text
source_id
source_generation
source_digest
parser_or_model_identity
parser_or_model_revision
projection_schema_version
projection_generation
page/span/bbox
created_at
```

No OCR text may silently replace source bytes.

### 8.2 Routing

Use deterministic/native extraction first when it preserves more source structure:

```text
native PDF text available -> qualified native parser
DOCX/HTML/Markdown/structured data -> qualified native parser
scanned page/image -> OCR
complex visual page/table/form -> multimodal document parser
low-confidence or conflicting region -> second parser, deterministic cross-check or human review
```

OCR should not run merely because a file is a PDF.

### 8.3 DeepSeek-OCR-2

DeepSeek-OCR-2 is a candidate local document-intelligence engine, not admitted by this amendment.

Its current public README demonstrates image/PDF flows and a Transformers path using `trust_remote_code=True`. WePLD must not inherit that trust decision automatically.

Qualification must cover:
- exact source/model revision and weight digests;
- tokenizer/config/custom-code digests;
- all build/import hooks;
- no unqualified remote-code fetch;
- dependency and CUDA/runtime requirements;
- malicious image/PDF/parser fixtures;
- bounded page/image dimensions and decompression;
- output/path bounds;
- cancellation/resource ceilings;
- Arabic, English and mixed-direction document fixtures;
- hallucinated-text and missing-region accounting;
- source-page/bounding-box traceability where supported;
- local/offline proof for the qualified route.

Cohere Parse is a behavior/benchmark reference only unless separately admitted. It must not become a core network dependency.

### 8.4 Perception security

Required negative oracles include:

```text
OCR_INSTRUCTION_TEXT_CANNOT_CREATE_WORKFLOW_INTENT
OCR_INSTRUCTION_TEXT_CANNOT_GRANT_EFFECT
MALICIOUS_DOCUMENT_CANNOT_ESCAPE_PARSER_BOUNDARY
EXTERNAL_REFERENCE_IN_DOCUMENT_CANNOT_CAUSE_NETWORK_FETCH_WITHOUT_AUTHORITY
OVERSIZE_IMAGE_OR_PDF_FAILS_BOUNDEDLY
OCR_PROJECTION_CANNOT_OVERWRITE_ORIGINAL_SOURCE
STALE_PROJECTION_CANNOT_MASQUERADE_AS_CURRENT_SOURCE_GENERATION
```

Primary owner/task mapping:
- acquisition: ASTRO-A09;
- parser/source boundary foundation: ASTRO-A04;
- source facts: ASTRO-F03;
- document/image modality product profile: ASTRO-P03;
- security validation: ASTRO-S01/S02/S03 as applicable.

## 9. Retrieval / RAG

The existing `contracts/retrieval-rag.md` remains the controlling planning boundary. This amendment does not replace it.

Preserve the existing replaceable signals:

```text
EXACT
PATH_OR_KEY
LEXICAL
METADATA
SYNTAX
SYMBOL
REFERENCE
CALL_GRAPH
SEMANTIC_VECTOR
RERANK
FRESHNESS
```

### 9.1 Retrieval planner

Do not implement a mandatory "chunk everything -> embed everything -> top-k" pipeline.

The planner selects the minimum sufficient signal set for the query/source class. Exact/lexical/structured retrieval remains functional without embeddings.

Semantic/vector machinery is:
- optional;
- derived/rebuildable;
- access-scoped;
- generation-bound;
- independently benchmarked for incremental value;
- removable without destroying canonical source or memory.

### 9.2 Retrieval truth and access

Preserve:

```text
RETRIEVAL_SCORE != TRUTH
RERANK_SCORE != TRUTH
EMBEDDING_DISTANCE != TRUTH
INDEX != CANONICAL_TRUTH
COLLECTION_MEMBERSHIP != VISIBILITY_AUTHORITY
```

Source revocation, membership loss, redaction or tombstoning must invalidate derived retrieval eligibility. Old vectors/chunks cannot remain a back door to deleted or revoked content.

### 9.3 RAG promotion gate

Before semantic/vector admission, benchmark the non-vector baseline on:
- exact path/file lookup;
- error/log lookup;
- lexical natural-language evidence;
- symbol/reference/call-graph questions;
- cross-source citations;
- stale source exclusion;
- revoked source exclusion;
- atomic refresh generation changes;
- explicit no-answer/abstention.

Only promote vectors/reranking for query classes with preregistered, material quality benefit at acceptable latency/resource/privacy cost.

### 9.4 Jev Search mechanism

`caio0452/jev_search` is a bounded donor for search scheduling and decision filtering, not a production dependency. Mine:
- file discovery/ignore behavior;
- keyword-density and top-file prioritization;
- bounded chunking;
- high-priority then low-priority scheduling;
- concurrent decision filtering;
- progressive result emission.

Its current OpenRouter Decisions dependency must not become a default WePLD route. The decision step is replaced by a qualified `CalibratedDecision` provider chosen by Mirefa, respecting `LOCAL_ONLY` and no-silent-fallback semantics.

```text
JEV_SEARCH_SCHEDULER != RETRIEVAL_TRUTH
REMOTE_DECISION_API != REQUIRED_RETRIEVAL_DEPENDENCY
SEARCH_SCORE != AUTHORITY
```

Primary owner/task mapping:
- source profile acquisition: ASTRO-A04;
- facts: ASTRO-F03;
- ContextPackage/retrieval: ASTRO-F04;
- memory extension: ASTRO-K02;
- context improvement benchmark: ASTRO-B03.

## 10. Scoped memory

Morize and other user-owned/source-registry memory work are mechanism sources, not a second Project Brain.

Fehrest stays the canonical owner.

Required namespace separation:

```text
PersonalMemory
TeamMemory
ProjectMemory
MissionMemory
ExperienceMemory
```

A durable memory record needs source/provenance, scope, version/generation, correction/retraction lineage, sensitivity/access state and conflict representation.

Preserve:

```text
MEMORY_CANDIDATE != DURABLE_MEMORY
MEMORY != POLICY
MEMORY != AUTHORITY
FOREIGN_VERIFIED_FLAG != LOCAL_VERIFIED_FACT
```

Memory retrieval is part of the prompt-injection threat model.

Required tests include:
- cross-project and cross-tenant collision;
- membership revocation;
- deletion/tombstone propagation;
- poisoned instruction persistence;
- contradiction retention;
- stale derived index;
- unknown schema;
- export/import semantic loss.

Primary owner/task: ASTRO-K02, with ASTRO-F04/T01 prerequisites.

## 11. Typed decisions / PLD / Jev-compatible behavior

WePLD should own the `CalibratedDecision` contract. Providers are replaceable.

Candidate engines:
- SemIf;
- Mapika Decider;
- Bespoke Nimble 9B;
- Laya-CoreML for qualified Apple-Silicon local routes;
- classifier.dev mechanisms and eval harness behind WePLD-owned local/controlled-egress adapters;
- a future TypeSafe/Jev adapter;
- future qualified local decision models.

Candidate logical request:

```text
DecisionRequest
- evidence_refs
- question
- decision_type
- options
- criteria
- risk_class
- calibration_profile
- abstention_policy
```

Candidate result:

```text
CalibratedDecision
- selected_option?
- option_probabilities
- raw_confidence?
- calibrated_confidence?
- abstained
- evidence_refs
- model_identity
- model_revision
- route_identity
- prompt_or_input_digest
- calibration_profile_id
- created_at
```

Never merge this with `NawatDecision`.

```text
CalibratedDecision != NawatDecision
PLD_CONFIDENCE != SECURITY_PASS
PLD_CONFIDENCE != REVIEW_PASS
PLD_CONSENSUS != COMPLETION
```

### 11.1 Appropriate use

Prefer PLD for small runtime-defined semantic decisions such as:
- likely subsystem owner;
- evidence supports/does-not-support a bounded criterion;
- candidate repair class;
- route suitability;
- triage/prioritization;
- risk/similarity classifications where deterministic policy does not already answer.

Do not use PLD alone to:
- design the whole architecture;
- prove containment;
- establish a legal fact;
- authorize an effect;
- establish security or completion;
- replace multi-step technical reasoning.

Preferred composition:

```text
general reasoning -> decompose
typed decision engine -> calibrated atomic judgments
deterministic machinery -> verify
Nawat/human/policy -> authorize
Assurance/Trusted Completion -> evaluate/accept
```

### 11.2 Calibration and route identity

Each material model/runtime/quantization route is separately qualified. Calibration from one route cannot silently transfer to another.

Required evaluation:
- accuracy;
- Brier/proper scoring measure;
- NLL where applicable;
- calibration error/reliability curve;
- selective risk;
- coverage versus abstention;
- OOD/adversarial confidence;
- malformed type handling;
- route/model revision mismatch;
- latency and resource use.

Primary owner/task: ASTRO-K03 with ASTRO-A05 and ASTRO-B01.

### 11.3 Laya-CoreML and classifier.dev acquisition profile

Laya-CoreML is the strongest current candidate for a fast, local, probability-returning Apple-Silicon route. Mine its prompt/result/tokenizer boundary, artifact verification, offline-cache mode, conversion-fidelity fixtures, ANE/Core ML hardware profiles and calibration-safety behavior. Its route is platform-specific and must not be reported as a cross-platform default.

classifier.dev contributes a different layer: typed zero-shot/multi-label API shape, batching, confidence/escalation/fallback accounting, CLI/SDK/MCP packaging and a reusable evaluation harness. WePLD should mine those mechanisms without making the hosted Cloudflare Worker or its provider fallback chain a required dependency.

Required invariants:

```text
LayaCoreMLRoute != UniversalRoute
ClassifierDevHostedAPI != CoreDependency
HostedFallback != LOCAL_ONLYFallback
EscalationModelChange = NewRouteIdentity
CalibrationProfile = BoundToExactModelRuntimeQuantization
```

## 12. Tool, skill and MCP capability fabric

Treg is a high-value mechanism source for:
- tool discovery by capability;
- stable catalog facade;
- CLI descriptors;
- skill bundles;
- MCP front door patterns;
- credential bindings;
- provider health;
- audit/usage patterns.

WePLD must not inherit Treg as an authority owner or mandatory hosted service.

Mapping:

```text
Treg-like catalog mechanism
-> Mirefa CapabilityPackage / ToolCapability
-> ASTRO-H01 admission manifest
-> optional ASTRO-H02 distribution lifecycle
-> Nawat invocation decision
-> UWC enforcing adapter
```

Secrets are referenced through scoped credential bindings/handles; they must not be copied into model prompts merely because a skill/tool needs them.

Tool descriptions, skill instructions and MCP metadata are untrusted package data. They cannot grant network/filesystem/process/credential effects.

Treg's current public license has additional hosted/embedded-service restrictions beyond Apache-2.0. The founder asserts separate permission to copy/use the source. Any import relying on rights beyond the public terms must preserve the custom grant evidence in its acquisition record.

Primary owner/tasks: ASTRO-A09, H01, H02, F06.

## 13. Runtime patterns from Google AX

Google AX is a runtime-design source, not a deployment dependency.

Mechanisms to study/adapt:
- declarative Task;
- Workspace;
- Gateway/egress profile;
- Model route resource;
- watch;
- suspend/resume;
- resource declarations;
- repeatable workspace bootstrap.

Do not import Kubernetes/Redis merely to reproduce those concepts.

Mapping:

```text
AX Task -> Mission Runtime Task / Attempt
AX Workspace -> WorkingCopy + ContextPackage + ToolSet bindings
AX Gateway -> egress/network enforcement profile; never Nawat replacement
AX Model -> Mirefa ModelRoute
AX watch/suspend/resume -> Runtime lifecycle evidence and control
```

Task workspace setup must not execute arbitrary package/build instructions without the normal source/effect authority.

Primary owner/tasks: ASTRO-A05, F05, U01/U02, F06, O03 where remote compatibility is relevant.

### 13.1 Unreal Agent harness patterns

`unreallabsai/unreal-agent` is a second runtime-design donor, not a runtime authority. Mine:
- stable caller-supplied Input IDs and session-scoped deduplication;
- append-only persisted sessions and forks;
- context-builder accounting for omitted/truncated/compacted material;
- schema-bound Tool -> pure synchronous ToolTranslator -> serializable Operation separation;
- operation state separate from model-facing tool-call status;
- swappable durable operation manager;
- cancellation, retry timing, resume and recovery tests.

Map those mechanics onto existing owners:

```text
Unreal Session -> Mission Runtime session/attempt evidence
Unreal ToolTranslator -> UWC validation/translation seam
Unreal Operation -> WePLD EffectProposal / authorized operation record
Unreal OperationManager -> enforcing Runtime/UWC adapter behind Nawat
Unreal Inbox Dedup -> input/event idempotency mechanism
```

Do not import the donor's session store or operation manager as canonical authority. Nawat effect-time revalidation and Trusted Completion remain mandatory.

## 14. Browser and web acquisition

TinyFish/AgentQL and BigSet are mechanism/behavior references.

Useful AgentQL-style mechanisms:
- semantic element/page querying;
- structured extraction;
- browser state observation;
- bounded interaction patterns.

Useful BigSet-style workflow:

```text
DatasetIntent
-> SchemaProposal
-> Discovery
-> Parallel Acquisition
-> Verification
-> Deduplication
-> Provenance
-> Refresh
```

Do not make TinyFish cloud or OpenRouter a core dependency. BigSet's public AGPL-3.0 terms and hosted-service dependencies require explicit disposition; mechanism reference and clean adapter design are safer defaults unless a qualified import record justifies more.

Web content remains untrusted data.

Required browser negative oracles:
- hidden page instruction cannot expand authority;
- redirect/DNS rebinding cannot escape destination scope;
- page cannot reveal clipboard/credential data without a separate grant;
- stale screenshot/DOM cannot authorize a later changed target;
- form submit and navigation are explicit effects;
- browser/account/profile identity is bound to the action receipt;
- cancellation at dispatch is fenced.

Primary tasks: ASTRO-K01 and ASTRO-P05, with F06 authority and UWC/Runtime prerequisites.

## 15. Desktop and terminal interaction

Desktop Commander is a mechanism/UX reference for local files, terminal and processes. Real-machine access is not itself a sandbox.

Candidate desktop records:

```text
DesktopObservation
ApplicationRef
WindowRef
UIElementRef
DesktopActionRequest
DesktopActionDecision
DesktopActionReceipt
InputLease
```

Every action binds to current application/window/screen generation and target identity where available.

Required negative oracles:
- stale screenshot cannot target a replaced window;
- focus change invalidates unsafe coordinate-only action;
- secure/password surfaces are not captured or typed into without explicit qualified policy;
- desktop/terminal availability does not grant filesystem/process/network effects;
- an interactive shell is not a containment boundary;
- process spawn/cancel remains under Runtime/Nawat.

Primary tasks: ASTRO-P05, O02/O03, X03/U02/F06.

## 16. Event intelligence and Action Cards

The Laya desktop product remains a behavior reference for notification/event intelligence. Separately, `mizorewww/laya-coreml@4619e0483f07adf39068532e85b42ec2347edb83` is now an exact source candidate for typed local decisions; it does not replace the event-intelligence behavior reference or establish the desktop app's source identity.

The useful pattern is:

```text
ProviderEvent
-> TriggerEnvelope
-> Normalize
-> Deduplicate
-> Correlate
-> retrieve bounded context
-> optional calibrated triage
-> ActionProposal
-> ActionCard
```

An ActionCard is a proposal/view, not an effect.

Required semantics:
- provider event identity/revision;
- replay/idempotency;
- stale event state;
- access revocation;
- actor/principal attribution;
- source connector freshness;
- proposed action scope;
- no automatic send/close/publish merely because triage is high confidence.

Prefer WePLD-native connector/event contracts rather than making n8n or another workflow product the authority core.

Primary tasks: ASTRO-P04, F05/F06, T01/T02 as applicable.

## 17. Source and rights strategy

The founder asserts permission to copy and use the requested sources and sources available in the founder's GitHub repositories. Record that assertion, but do not convert it into fabricated public license metadata or blanket source admission.

```text
FOUNDER_PERMISSION_ASSERTED = YES
FOUNDER_PERMISSION_REAFFIRMED_2026_09_23 = laya-coreml + jev_search + unreal-agent + classifier-dev
FOUNDER_PERMISSION_ASSERTION != SOURCE_ADMISSION
FOUNDER_PERMISSION_ASSERTION != PATH_PROVENANCE
PUBLIC_LICENSE != TECHNICAL_QUALIFICATION
```

Every actual import must record:
- source identity;
- exact commit/revision/tree/blob;
- exact selected paths;
- upstream tests/fixtures/failure corpus selected;
- public license/NOTICE;
- custom grant evidence if relied upon;
- transitive dependencies;
- build/install/import hooks;
- network/remote-code behavior;
- supported OS/runtime;
- maintenance/advisory observation;
- WePLD adapter/contract;
- rollback/replacement route;
- conformance and negative tests.

Do not bulk-import an organization or the founder's GitHub merely because permission exists. Search broadly; admit narrowly per mechanism.

See `INTELLIGENCE_SOURCE_INTAKE.md` for the candidate pins observed with this amendment.

## 18. Security and threat-to-test additions

These rows extend the existing Astro threat model; they do not replace it.

| Threat | Required control / negative oracle |
|---|---|
| OCR hidden instruction | Perception projection cannot create WorkflowIntent or grant |
| Malicious PDF/image/parser input | bounded parser/model execution; no unauthorized external references |
| Remote-code model loader | custom code pinned and qualified before execution; no silent `trust_remote_code` |
| RAG poisoning | source provenance/taint/conflict retained; instruction text stays data |
| Deleted source survives vector/cache | tombstone/revocation removes new retrieval eligibility |
| Cross-scope vector/memory leakage | tenant/project/access-qualified indexes and at-use recheck |
| PLD high-confidence OOD result | calibration + abstention; cannot grant |
| Two wrappers over same backend | producer/model correlation recorded; not independent votes |
| Quantization/runtime calibration shift | route-specific calibration and revision identity |
| Skill/tool asks for broader secret | new capability/permission requires re-admission/re-authorization |
| Tool description prompt injection | metadata cannot grant effect |
| Browser hidden instruction | content taint + explicit effect target |
| Desktop stale visual state | current screen/window/input-lease binding |
| Provider event replay | revision/idempotency/freshness |
| Connector revoked during action | effect-time recheck and uncertain-outcome reconciliation |
| GPU/resource exhaustion | explicit RAM/VRAM/time/concurrency ceilings and cancellation |
| Silent cloud fallback | fail closed or ask; never automatic |
| Model/tool update expands capabilities | immutable version and permission diff; re-admission |
| Derived artifact loses source linkage | projection cannot enter qualified context without provenance |

Relevant security tasks: ASTRO-S01/S02/S03 plus the owning feature tasks. Security coverage follows actual changed behavior, not this table alone.

## 19. Recovery requirements

Each capability must define what is canonical, what is rebuildable and what may require compensation.

| Capability | Recovery rule |
|---|---|
| OCR/perception | regenerate projection from immutable original artifact generation |
| RAG/indexes | rebuild derived lexical/vector/graph indexes from qualified sources |
| Memory | immutable versions/generations plus explicit correction/retraction/tombstone |
| PLD | prior decision receipt remains historical; rerun creates a new decision identity |
| Models | reacquire only from pinned identity/digest; model cache is not canonical truth |
| Tool/skill registry | versioned rollback, revocation and package-owned cleanup |
| Browser/Desktop | arbitrary external effects may be irreversible; use receipts/reconciliation/compensation |
| Event intelligence | replay normalized event log with idempotency/freshness fences |
| Connector credentials | revoke/rotate handles; never reconstruct secrets from evidence |

Preserve:

```text
DELETE_INDEX != DELETE_SOURCE
GIT_ROLLBACK != EXTERNAL_EFFECT_ROLLBACK
REBUILDABLE_PROJECTION != DURABLE_SOURCE
```

## 20. Benchmark and promotion gates

No capability becomes a release-quality claim because a donor README or demo looks good.

### 20.1 OCR/document intelligence

Preregister and measure:
- text accuracy;
- reading order;
- table structure;
- forms/key-value extraction where claimed;
- page/span/bbox alignment;
- Arabic;
- English;
- mixed Arabic/English and RTL/LTR;
- degraded scans;
- hallucinated content;
- omitted regions;
- latency/page throughput;
- RAM/VRAM;
- cancellation/resource ceilings.

Compare deterministic/native extraction first, then qualified local OCR/document models. External services such as Cohere Parse may be benchmark references without becoming dependencies.

### 20.2 RAG

Measure:
- evidence recall;
- citation/location precision;
- stale-source rejection;
- no-answer abstention;
- revoked-access exclusion;
- refresh-generation correctness;
- latency;
- index size/build time;
- incremental benefit of vectors and reranking.

Compare at least:
- lexical baseline;
- structured/code graph;
- lexical + structured;
- + semantic vector;
- + reranker where admitted.

### 20.3 PLD

Measure:
- task accuracy;
- proper scoring/Brier;
- NLL where applicable;
- reliability/calibration;
- selective risk;
- abstention coverage;
- OOD confidence;
- malformed-type handling;
- revision/route mismatch;
- latency and RAM/VRAM.

### 20.4 Tool/runtime routing

Measure:
- accepted task success;
- wrong-tool/route selection;
- unauthorized-effect rate;
- latency;
- resource/cost;
- human intervention;
- cancellation/recovery;
- fallback/reassignment visibility.

### 20.5 Product-level claim

B01/B02/B03 remain the owners of comparative WePLD claims. Capability-specific benchmarks feed evidence into those experiments; they do not create a second benchmark authority.

## 21. Existing 63-task DAG mapping

No new DAG nodes are introduced by this amendment.

| Capability / concern | Existing task owner |
|---|---|
| Parser/retrieval candidate qualification | ASTRO-A04 |
| Worker/model/harness route | ASTRO-A05 |
| Policy machinery | ASTRO-A06 |
| Later source/model/donor acquisition records | ASTRO-A09 |
| Versioned source facts | ASTRO-F03 |
| RAG / ContextPackage | ASTRO-F04 |
| Runtime route identity and first-loop contract | ASTRO-F05 |
| Effect-time authority | ASTRO-F06 |
| Tool/skill/capability admission | ASTRO-H01 |
| Community/private distribution lifecycle | ASTRO-H02 |
| Research/web acquisition | ASTRO-K01 |
| Memory/interchange | ASTRO-K02 |
| PLD/Jev-compatible typed decisions, Laya-CoreML/classifier routes | ASTRO-K03 |
| Decision-filtered retrieval/search scheduling | ASTRO-A04/F04/K03 |
| Async harness/session/operation mechanics | ASTRO-A05/F05/U01/U02/F06 |
| OCR/vision/document intelligence product profile | ASTRO-P03 |
| Laya-style schedules/connectors/events | ASTRO-P04 |
| Browser/desktop/computer/text-assist | ASTRO-P05 |
| Remote/mobile compatibility | ASTRO-O03 |
| Security qualification | ASTRO-S01/S02/S03 |
| Usage/budget/resource accounting | ASTRO-T03 |
| Capability and whole-product measurement | ASTRO-B01/B02/B03 |

ASTRO-A09 is the primary near-term place to freeze the additional donor/source records. It does not admit them.

ASTRO-P01 remains the edition-aware feature-completeness manifest and should consume A09 records rather than inventing new source identities.

## 22. Capability definition of ready-for-release

A capability must not be shown as fully available/qualified until its owning profile has evidence for every applicable item:

```text
SOURCE_IDENTITY_QUALIFIED
RIGHTS_RECORDED
DEPENDENCIES_PINNED
CONTRACT_FROZEN
PLATFORM_PROFILE_PROVEN
HARDWARE_REQUIREMENTS_PROVEN
LOCALITY_TRUTHFUL
PRIVACY_EGRESS_BOUNDARY_PROVEN
NEGATIVE_ORACLES_PASS
RESOURCE_LIMITS_PROVEN
CANCELLATION_PROVEN
RECOVERY_PROVEN
BENCHMARK_COMPLETE
SECURITY_REVIEW_COMPLETE
USER_DISABLE_PATH_PROVEN
REMOVAL_REPLACEMENT_PATH_PROVEN
RESIDUAL_LIMITATIONS_VISIBLE
```

Otherwise use explicit product states such as:

```text
EXPERIMENTAL
UNAVAILABLE
UNSUPPORTED_ON_THIS_HARDWARE
REQUIRES_MODEL_DOWNLOAD
REQUIRES_NETWORK
REQUIRES_EGRESS_APPROVAL
NOT_QUALIFIED
BLOCKED
```

Do not paint missing capability evidence green.

## 23. Gap-closure checklist

The plan is not complete for a capability until the owning task answers all applicable questions:

1. Who owns canonical truth?
2. What is original source versus derived projection?
3. What exact source/model/tool revision is selected?
4. What rights/license/custom grant applies to the selected paths?
5. What dependencies/build hooks/remote-code behavior execute?
6. What local/offline claim is actually proven?
7. What hardware/platform limits exist?
8. What user preference controls selection?
9. What effect classes require Nawat?
10. What data can leave the host and under what egress profile?
11. What prompt-injection/untrusted-input boundary applies?
12. What negative oracles prove the boundary?
13. What happens on cancellation, crash and restart?
14. What is rebuildable and what is canonical?
15. What happens on source/access/credential revocation?
16. What happens when the route/model/provider changes?
17. What benchmark proves material value?
18. What unsupported/abstention state is shown?
19. How is the capability removed or replaced?
20. What residual limitation remains visible?

## 24. Explicit non-goals

This amendment does not:
- create S11 or another roadmap;
- bulk-admit or bulk-import source merely because copy/use permission exists;
- install models/dependencies;
- run DeepSeek-OCR-2 or any other donor;
- admit a vector database;
- require a graph server;
- require Kubernetes, Redis, n8n, TinyFish cloud, OpenRouter or Treg hosted service;
- grant browser/desktop/terminal/network authority;
- make Jev/PLD confidence an authorization input;
- make OCR or RAG output canonical truth;
- edit protected `MASTER_PLAN_INDEX.md`;
- claim WePLD is "best" before B01/B02/B03 evidence.

## 25. Implementation-readiness state

At the observed base, ASTRO-G01 and ASTRO-F01 are already canonical. The local-intelligence additions do not create a new prerequisite chain; they attach to existing owners. Therefore:

```text
PLAN_GAP_FOR_LOCAL_INTELLIGENCE = NONE_UNOWNED
ASTRO-A04 = DEPENDENCY_READY
ASTRO-A05 = DEPENDENCY_READY
ASTRO-A06 = DEPENDENCY_READY
ASTRO-A07 = DEPENDENCY_READY
ASTRO-A08 = DEPENDENCY_READY
ASTRO-A09 = DEPENDENCY_READY
ASTRO-P01 = BLOCKED_ON_ASTRO-A09
SOURCE_ADMISSION = NONE_UNTIL_OWNING_TASK_ACCEPTS
```

“Ready” here means the implementation/acquisition path, owner, negative oracles, recovery obligations and acceptance gate are specified. It does not mean a donor, model, dependency or effect has already passed qualification.

## 25. Next governed actions

Once this amendment's exact head is independently accepted and merged, the existing task order remains authoritative. It does not reopen accepted G01/F01 history or create a second execution gate.

Near-term integration work should occur through:
1. ASTRO-A09: capture/freeze source/model/donor records from `INTELLIGENCE_SOURCE_INTAKE.md`;
2. ASTRO-A04/A05/A06 as their already-unlocked qualification paths permit;
3. ASTRO-P01 after A09, preserving its existing dependency;
4. later owning profiles K01/K02/K03/P03/P04/P05/H01/H02/O03 only when their current DAG prerequisites are accepted.

No implementation path is unlocked merely by merging this amendment.