# Analyze — IssueOps Agentic Engineering Control Plane

```text
STATUS = PLANNING_ANALYSIS
IMPLEMENTATION_AUTHORITY = NONE
```

## 1. Consistency with canonical V2.3

The proposed capability set fits the existing P0 + S1..S10 roadmap without renumbering or reopening the architecture root:

- S3 owns trusted terminal/process/input foundations.
- S4 owns Fehrest minimum and retrieval/project-brain foundations.
- S5 owns Spec Kit/AGILLE/Plan Qualification/Ponytail and is the natural home for workflow/skill UX.
- S6 already owns UWC, Mirefa, Edara, Agent Host interoperability, and Nawat effect-time authority, so provider-neutral delegation belongs there.
- S7 owns Native Review/Assurance and can qualify IssueOps review/security behavior.
- S8 owns controlled repair/reassignment/Trusted Completion and is the natural home for autonomous issue repair/landing loops.
- S9 owns the evidence/quality/recovery timeline.
- S10 owns expansion/analytics and can scale IssueOps across repositories/providers.

No new parallel authority system is required.

## 2. Critical separations

The plan is unsafe if any of these are collapsed:

```text
Case identity vs provider issue identity
Case lifecycle vs provider open/closed state
Autonomy ceiling vs effect authorization
Worker selection vs worker qualification
Worker qualification vs containment
Containment vs authority
RAG retrieval vs truth
Review output vs completion decision
Merge/closeout vs Trusted Completion
Drop/paste input vs execution
Provider session identity vs WePLD durable session identity
```

All implementation specs must preserve these separations structurally, not only in documentation.

## 3. Highest-risk capability areas

### 3.1 External issue writes

Comments, labels, assignees, PR creation/update, merge, and issue close/reopen are externally visible effects and need exact-target/idempotency/retry semantics. Duplicate webhook delivery or retry must not produce duplicate mutations.

### 3.2 Untrusted artifact ingestion

Files, archives, documents, repositories, URLs, and logs may be malicious, huge, malformed, recursive, symlinked, or privacy-sensitive. Intake must remain inert until parser/access paths are qualified.

### 3.3 RAG freshness and conflict

Stale indexed content can cause plausible but wrong repairs. Retrieval evidence must expose source generation/freshness and make missing/stale/conflicting evidence visible.

### 3.4 Agent containment variance

Different agent CLIs expose materially different sandbox/read-only semantics. WePLD must independently qualify actual effects and containment rather than trust provider labels.

### 3.5 Autonomous landing

The dangerous failure mode is a system that is excellent at generating and merging changes but weak at proving root cause, exact-head review, authorization, and residual risk. `land` must therefore be the final bounded capability, not the MVP.

### 3.6 Backlog-scale automation

Sweeps can amplify classification mistakes across hundreds of issues. Early sweeps should produce evidence-backed recommendations/frontiers before autonomous bulk mutations.

## 4. Required negative oracles

Future implementation must include deterministic tests/evidence for at least:

- dropped path never executes;
- URL attachment never fetches without network authority;
- unsupported/malformed source fails closed;
- stale retrieval is surfaced, not silently treated as current;
- worker unavailable does not silently select another provider;
- paid/quota worker is not silently invoked;
- advisory provider read-only mode is not represented as containment;
- duplicate external event does not duplicate provider mutation;
- stale issue/PR target prevents unsafe write/merge;
- changed PR head invalidates prior acceptance evidence;
- merged PR does not automatically mark Case Trusted Complete;
- closed provider issue does not automatically mark Case Trusted Complete;
- implementer output cannot self-satisfy independent-review requirement;
- valid reviewer finding remains in the reconciliation set until fixed/rebutted/proven obsolete;
- failed worker attempt remains in history after reassignment;
- RAG result without provenance cannot satisfy a provenance-required context package;
- provider state disagreement is preserved rather than overwritten by normalization.

## 5. Data and state strategy

Prefer append-only events plus derived state over mutable opaque workflow state. Material transitions should be reconstructable from durable evidence. External providers are synchronized peers/edges, not the sole database of truth.

Expected event families:

```text
CASE_DISCOVERED
PROVIDER_OBSERVED
ARTIFACT_ATTACHED
SOURCE_INGESTED
RETRIEVAL_OBSERVED
TRIAGE_RECORDED
REPRODUCTION_RECORDED
ROOT_CAUSE_CANDIDATE_RECORDED
DECISION_BOUNDARY_OPENED/CLOSED
ASSIGNMENT_CREATED
ATTEMPT_STARTED/FINISHED/FAILED/CANCELLED
EFFECT_PROPOSED/AUTHORIZED/DENIED/EXECUTED
CHECK_RECORDED
REVIEW_FINDING_RECORDED/RECONCILED
LANDING_PROPOSED/EXECUTED
PROVIDER_CLOSEOUT_EXECUTED
TRUSTED_COMPLETION_RECORDED
```

## 6. Issue relation model

Relations should be evidence-backed and typed, not only free-form labels:

```text
EXACT_DUPLICATE_OF
PROBABLE_DUPLICATE_OF
COMMON_ROOT_CAUSE_WITH
REGRESSION_OF
BLOCKED_BY
DEPENDS_ON
SUPERSEDES
FIXED_BY
VERIFIED_BY
```

Probabilistic relations carry confidence/evidence and must not silently become exact relations.

## 7. UX analysis

The simplest surface should remain command/intention driven:

```text
/issues
/fix <case-or-url>
/triage <case-or-url>
/rag ...
/delegate ...
/btw
```

`/fix` may later be an alias/intention into the IssueOps workflow rather than a separate authority path. The UI should show state and blockers in human terms while preserving exact evidence behind expandable details.

The Case room should optimize for “what is happening, why, what is blocked, what needs me?” rather than expose raw multi-agent chatter by default.

## 8. Autonomy analysis

The safest progression is monotonic by capability ceiling:

```text
observe -> triage -> prepare -> execute -> land
```

Each level should be independently testable and deployable. A repository should be able to remain permanently at `prepare` while another reaches `land`.

## 9. RAG analysis

A universal `/rag` capability should not force every source into one representation. Preserve source-native identities and derive indexes as secondary projections. The primary ingestion contract should be content/provenance/freshness, while lexical, graph, vector, and rerank indexes remain replaceable views.

This avoids making a vector database the Project Brain and preserves the canonical invariant that Fehrest informs but does not authorize.

## 10. Delegation analysis

The studied delegate skills show useful provider CLI mechanics but also demonstrate why provider-level “read-only” and “full trust” switches cannot define WePLD safety. The durable value is the normalized worker catalog, dispatch brief, session tracking, queue/poll/cancel behavior, and review/land separation.

## 11. Matt skills analysis

The strongest reusable design pattern is not the command names; it is a workflow grammar:

```text
understand -> clarify decisions -> gather evidence -> spec/plan -> tracer-bullet tasks
-> implement with tight feedback -> independent review -> reconcile -> handoff/learn
```

WePLD should encode that grammar behind native commands and Case workflows while preserving its stronger authority/evidence model.

## 12. Open future decisions

These are intentionally deferred to owning-slice Spec Kit/Source Acquisition rather than guessed now:

- exact GitHub authentication/application model;
- webhook vs polling strategy and local/offline behavior;
- exact parser set and archive policy;
- lexical index implementation;
- whether semantic/vector retrieval is justified and which engine;
- exact worker adapters admitted first;
- exact issue providers after GitHub;
- exact case/event storage representation after S2 foundations mature;
- organization-scale scheduling/resource policy;
- metrics thresholds for autonomous `land` qualification.

Deferring these is deliberate scope control, not a planning gap.

## Supporting-package bidirectional traceability

The product matrix and product acceptance families live in `product-capability-tracks-plan.md` sections 14–17 and its acceptance section K. This table covers the supporting requirement/task/acceptance paths. Each row is a conjunctive work package: its tasks collectively implement the listed requirements; a task's concrete verb/object selects its corresponding obligation, never permission to omit the others. Reverse lookup uses the same row's task prefix/range and owner. Cross-cutting security/failure requirements additionally apply to every affected operation. Task IDs/ranges retain their owning files and roadmap slices.

Contract abbreviations: DM=data-model; CP=case-provider; RR=retrieval-rag; UC=untrusted-content; WD=worker-delegation; CS=command-surface; RF=runtime-execution-fabric; RD=runtime-distributed-safety-addendum; BP=behavior-policy-boundary; WB=web-agent-boundary; AF=assurance-fabric; RI=review-independence (all contracts except DM are under `contracts/`). Acceptance letters refer to `acceptance.md`; runtime letters refer to `runtime-execution-fabric-acceptance.md`. Exact contract sections are the headings named by each requirement; detailed negative oracles are in each owning contract and task's tracer bullet.

| Requirements | Owner / contract | Tasks (explicit owning namespace) | Acceptance / evidence / prerequisite |
|---|---|---|---|
| FR-014..016 | trusted intake, Fehrest / DM InputArtifact, UC | 006-S3-I001..014; 006-S34-C001..005 | D/E; inert artifact -> cited generation with no implicit effect; S3 -> S4 |
| FR-010..013, FR-025, FR-043 | Fehrest/Maemar / DM Knowledge*, RR, UC | 006-S4-R001..018 | C/E; exact/lexical/graph provenance, direct/projection variants, access/revocation/remote-ingestion and benchmark oracles; S4 |
| FR-006, FR-017/018, FR-026 | Edara planning / DM WorkflowIntent/DecisionBoundary, CS, WD topology | 006-S5-W001..025 | F/G; no-effect command/skill/Assignment plans and dependency frontier; S5 before live workers |
| FR-019..024, FR-025/026 | Mirefa/Nawat/MissionRuntime/UWC / DM and WD | 006-S6-D001..019 | G/H; exact capability/route/cost/containment/authority/cancel evidence and no fallback; S3–S5 before S6 |
| FR-001..005, FR-008/009, FR-042 | Case provider adapters, Case Bus / DM Case/Provider*/relations, CP | 006-I001..025 | B/E/H; synthetic TB0 before live read TB1, authentic complete observations and labelled sweep false-positive/abstention corpus; S6/S7 |
| FR-027 | IssueOps Assurance/AMAN integration / AF, RI | 006-S7-A001..010 in tasks.md | I/H; exact-target independent findings and non-erasing coverage/security evidence; S7 |
| FR-037 | Assurance claim assessment / AF ClaimAssessment and AssurancePolicySnapshot, RI | 006-HARD-S5-001..005, 006-HARD-S7-001/002; 006-AF-S7-A005/008/009/010/011/012 | I, AF-A; missing/stale evidence, required-check failure and conflicts cannot support claims; S5 policy before S7 assessment |
| FR-038 | Assurance evidence handling / AF EvidenceHandlingPolicy, AMAN | 006-HARD-S7-006/007; 006-AF-S7-D002; 006-RT-S6-PRIV001, 006-RT-S9-PRIV001 | I, runtime E/L, AF-A; secret/private-content capture, storage, rendering and export negatives; minimum privacy before S6 effects, S7/S9 expansion |
| FR-039 | Qualified engine execution / AF EngineDescriptor/EngineRun, RF | 006-HARD-S3-004/005/006; 006-AF-S3-001..009; 006-AF-S7-A003 | I, runtime D, AF-A; exact executable/configuration and resource/containment/cleanup evidence; S3 foundations before S6/S7 execution |
| FR-040 | Assurance finding governance / AF Finding/FindingDisposition, RI | 006-HARD-S7-003/004/005; 006-AF-S7-A004/007/010/011 | I, AF-A; non-erasure, scoped authorized expiry and forged suppression/false-fix negatives; S7 |
| FR-041 | Assurance performance assessment / AF PerformanceEvidence | 006-HARD-S7-010; 006-AF-S7-T014 | I, AF-A; pinned baseline/environment/fixture, warmup/repetitions/noise and inconclusive outcomes; S7 |
| FR-007, FR-028..030 | Nawat/MissionRuntime/S8/Trusted Completion / DM §19/20, CP, WD, AF | 006-S8-X001..017 | H/K; bounded repair, canonical effect dispatch/reconciliation and exact accepted completion packet; S6+S7 before S8 |
| FR-031, FR-044 | Evidence Graph/Quality Passport / DM events/completion, AF history | 006-S9-E001..006 | L/K; replay, migration, restore, redaction and historical decision reconstruction; minimum runtime safety before S9 expansion |
| FR-003/008/024/031 | Fehrest/Byan recommendations, qualified providers / CP, WD | 006-S10-O001..007 | B/G/L; bounded cross-provider analytics and explicit optional schedule/federation gates; conditional later work under product plan §13, not revised canonical S10 |
| PCT-FR-X, FR-007/016/018/024/027/031 | canonical governance and owning source/quality boundary | 006-P001..013 | A/M/N plus source-acquisition.md and plan tracer bullets; admission/benchmark/egress evidence before reuse or effect activation |

The `006-S7-A` entries above belong only to the parent IssueOps task ledger. `006-HARD-` entries belong to `professional-plan-hardening-tasks.md`, `006-AF-` entries to `assurance-fabric-tasks.md`, and `006-RT-` entries to `runtime-distributed-safety-tasks.md`. The FR-037..041 rows refine those exact owners; acceptance letters are criteria, never task namespaces.

### Runtime and distributed traceability

OM tasks are in `omnigent-execution-fabric-integration-tasks.md`; RT/POL tasks are in `runtime-distributed-safety-tasks.md`. Every row consumes the full named contract, including later mandatory refinements rather than a reduced local schema.

| Requirement | Owner / contract | Tasks | Acceptance / exact evidence |
|---|---|---|---|
| FR-045 | MissionRuntime/UWC / RF identity | OM-S3-001, OM-S6-001 | runtime A; authenticated distinct Server/Host/Runner/Worker/Attempt and explicit host opt-in |
| FR-046 | Nawat ceilings/MissionRuntime / RF envelope | OM-S5-002, OM-S6-005/007 | runtime C; intersection/empty envelope, cost and reservation decision fixtures |
| FR-047 | trusted process/runtime / RF containment | OM-S3-002/003 | runtime D; per-dimension guarantees and unavailable-required-sandbox refusal |
| FR-048/049 | RF credential broker | OM-S3-004/006, OM-S6-006, OM-S9-002 | runtime E/F; deny-default environment, complete credential scope/activation/revocation/HTTPS/use receipts |
| FR-050 | UWC / RF protocol/dialect | OM-S5-001, OM-S6-002/003/004 | runtime B; exact protocol/extension, neutral unknown fields and no fallback |
| FR-051 | Browser adapter / WB, IS | OM-WEB-001..003 | runtime G and BR-A/WM-A; schema observation without execution and exact snapshot-bound action |
| FR-052 | Assurance / RI | OM-S7-001..003 | runtime H; policy-qualified builder/reviewer/context/authority/target independence receipt |
| FR-053 | Nawat/MissionRuntime / DM §19, RF | OM-S8-001..004 | runtime I; effect DAG, unknown prerequisite blocking and authorized compensation |
| FR-054 | native adapter / RF desktop, IS | OM-S3-005 | runtime J and CU-A; typed bounded native bridge, no generic process/shell authority |
| FR-055/056 | MissionRuntime/Evidence handling / RF, RD, AF | OM-S6-008, OM-S9-001..003; 006-RT-S6-PRIV001, 006-RT-S9-PRIV001 | runtime E/I/L; crash/ownership reconciliation and secret exclusion before persistence, including replay/export |
| FR-057 | MissionRuntime / RD enrollment | 006-RT-S3-001/002, 006-RT-S6-006 | runtime L; authenticated/revoked host and replay-resistant reconnect |
| FR-058 | MissionRuntime enforcing sink / RD leases | 006-RT-S6-001/002 | runtime L; old-owner partition, expired lease, enforcing fence and no unsafe takeover |
| FR-059 | MissionRuntime + Case Bus transport / RD events | 006-RT-S3-003/004, 006-RT-S9-001/002 | runtime L; producer/incarnation/sequence/causal gaps, key conflicts and replay without duplicate effects |
| FR-060 | UWC/Mirefa / RD harness identity | 006-RT-S6-003/004, 006-RT-S7-001 | runtime L; artifact/config/protocol replacement stales exact qualification |
| FR-061 | canonical behavior-policy boundary + Nawat / BP | 006-POL-S5-001, 006-POL-S6-001..003, 006-POL-S7-001 | runtime M; monotonic narrowing, no self-activation, NO_OBJECTION cannot grant |
| FR-062 | Mirefa qualification/MissionRuntime admission / RD, RF | 006-RT-S6-005, OM-S5-002 | runtime L; REQUIRED vs NOT_REQUIRED typed determination and live matching reservation |
| FR-063 | UWC/MissionRuntime / RD handshake | 006-RT-S3-005, 006-RT-S6-006 | runtime L; unknown required effectful semantics refuse, no silent downgrade |

Runtime acceptance K additionally maps OM-S3-006 and the source-acquisition Omnigent addendum (FR-049/PCT-FR-X); N maps PCT-P001..007 and HARD-C001..004 (package discovery/coherence). These are planning/source checks, not claims that runtime fixtures ran.

### Assurance traceability

AF-FR identifiers are defined in `assurance-fabric-spec-addendum.md`. Every unprefixed task token in this Assurance table expands into the `006-AF-` namespace of `assurance-fabric-tasks.md`, never the parent `tasks.md` ledger. For example, `S7-A001..012` means `006-AF-S7-A001` through `006-AF-S7-A012`, and `S6-001..005/008` means `006-AF-S6-001` through `006-AF-S6-005` plus `006-AF-S6-008`. Explicit `HARD-` references retain the separate hardening namespace defined below. They use the single AF contract, Fehrest context, AMAN security, RF engine execution, RI review and S8 completion owners. Acceptance is parent section I plus AF-A, the contract's explicit negative oracles and the named AF-TB tracer bullet. Each task group has the same incoming S3 -> S4 -> S5 -> S6 -> S7 -> S8 -> S9 dependency order; pure planning is not execution authority.

| Requirement set | Tasks | Contract/evidence and tracer |
|---|---|---|
| AF-FR001/002/008/019/028/039/040/041 | S7-A001..012 | AF target, Findings/ClaimAssessment/Bundle, failure/conflict/staleness; AF-TB2 |
| AF-FR003/004/005/020/036/042/047/048 | S5-001..012 | AF intent/plan/policy/check requirements/config; no-effect AF-TB0 |
| AF-FR006/007/032 | S7-T001..014 | AF typed tests/coverage/performance; non-clean outcomes, selection recall/counterexamples; AF-TB2 |
| AF-FR009/010/030/049 | S6-006, S7-R001..010 | AF review/RI exact-target, independence, scope and quality corpus; AF-TB3 |
| AF-FR011/014/015 | S4-001..010 | Fehrest + AF reachability/provenance/generations, unknown dynamic edges; AF-TB0/2 |
| AF-FR012/013/016/031/033 | S7-S001..014 | AMAN + AF security classes/threat-derived checks, labelled corpus and explicit gaps; AF-TB2 |
| AF-FR017/022/044 | S7-D001..010, S6-007 | AF dynamic/egress/handling, RF credential/network scope; synthetic fixtures before external targets |
| AF-FR018/034/035/045 | S3-001..010, S6-001..005/008 | AF engine artifact/config/resource identity, discovery without effects, qualified RF execution; AF-TB1 |
| AF-FR021/029/037/038 | P001..014 | source gates, bounded local-first baseline, predeclared metrics and budgets; AF-TB0 before promotion |
| AF-FR023 | S7-X001..009 | AF interchange preserves rich identities/unsupported fields/coverage; malformed format fixtures |
| AF-FR024/025 | S7-I001..010 | AF IDE/findings/plan inspection/safe rendering; same bundle identities, no effects on typing |
| AF-FR026 | S8-001..007 | AF FixProposal/Reverification + Nawat/S8; independent repair loop AF-TB3 |
| AF-FR027/050 | S9-001..007 | AF historical policy/target/evidence reconstruction, staleness and privacy; AF-TB4 |
| AF-FR043/046 | supporting HARD-S7-003/004/005/009/010 below; S7-A004, S7-T006/014 | AF disposition/performance evidence; false suppression, expiry, warmup/repetition/noise fixtures |

### Supporting hardening, Web and source-mechanism tasks

These tables make supplemental tasks refinements of existing requirements, not new owners. HARD prefixes expand to `006-HARD-` in `professional-plan-hardening-tasks.md`; WEB prefixes to `006-WEB-` in `web-agent-tasks.md`; OH identifiers are in `openhands-assurance-integration-tasks.md`.

| Task group | Requirement / owner-contract | Acceptance and evidence |
|---|---|---|
| HARD-C001..004 | PCT-FR-X; FR-001/019/032; DM/WB canonical schemas | A/B/G/J, X-A; reject divergent shared field/enum definitions |
| HARD-S3-001..006 | FR-029/039/044/047/055; RF/DM effect/engine | H/I/runtime D/I/L; dispatch-unknown, bounded engine/cleanup and exact artifact fixtures |
| HARD-S4-001..007 | FR-010..013/025/043; RR/UC | C/E; generation/revocation/SSRF/isolation fixtures |
| HARD-S5-001..005 | AF-FR042/047/048; AF policy/checks | I; immutable policy, required-check monotonicity and conflict fixtures |
| HARD-S6-001..006 | FR-019/025/042/055; CP/WD/RF | B/G/H; provider completeness/authenticity and worker version/recovery/access fixtures |
| HARD-S7-001..011 | FR-037..041; AF-FR006/041..049; AF/RI | I; claims, disposition, privacy, flake, performance, dirty target and scope evidence |
| HARD-WEB-001..005 | FR-032..035, PCT-FR-BR/WM; WB/IS | J, BR-A/WM-A; artifact/clipboard/context/credential boundaries |
| HARD-S9-001..004 | FR-044, AF-FR050; AF/RD | L; schema/restore/redaction/retention evidence |
| HARD-S10-001 | FR-024, PCT-FR-X; WD/RD | G/L; fairness/conflict/quota evidence before conditional later scheduling |
| WEB-P001..008 | PCT-FR-X, FR-032..036; WB/source gate | M, web-agent-acceptance.md; exact source/protocol/privacy/adversarial qualification |
| WEB-S3-001..006, WEB-S4-001..005 | FR-033/034/051, PCT-FR-BR; WB/IS/RR | J/C, BR-A; identity, inert intake, provenance before execution |
| WEB-S5-001..008, WEB-S6-001..011 | FR-032/035/036, PCT-FR-WM; WB/CS/WD | J, WM-A; WEB-TB0/1 bounded untrusted discovery/qualification/publisher read/proposal-only |
| WEB-S7-001..006, WEB-S8-001..008 | FR-027/028/032..035, PCT-FR-BR/WM/AF; WB/AF/RI | J/K, BR-A/WM-A/AF-A; WEB-TB2/3 hostile input, fresh qualification, bounded actuation and independent repair |
| WEB-S9-001..003, WEB-S10-001..003 | FR-031/044, PCT-FR-BR/WM; WB/RD/AF | J/L; exact historical context/privacy and qualified recovery; later policy/scale conditional under product plan §13 |
| OH-S3-001/002, OH-S6-001/002 | FR-019/021/022/045/046/060; RF/WD/RD | G/runtime A/C/L; capability separation, observed presence, exact binding and removed-backend refusal |
| OH-S7-001..006 | AF-FR009/010/011/030/049; AF/Fehrest/RI | I, AF-TB2/3; deterministic architecture rule, evidence-proportional review and independent coverage |
| OH-S7-007..010 | FR-016/022/027/053/059, AF-FR008/028; DM effect, AF/RD | E/H/I; no tool-call authority, no clean-majority erasure, canonical event lineage |
| OH-S7-011/012 | AF-FR005/007/032; AF | I, AF-TB2; impact selection and evidence-gap findings |
| OH-S9-001 | FR-031/044, AF-FR027/050; AF/RD | L; Quality Passport projection with exact historic policy/evidence |
| OH-TB1..5 | same OH requirements above | deterministic architecture bypass, removed backend, ungranted model call, conflicting producers and FullTest evidence-gap scenarios; no extra runtime owner |

Planning criteria A–N in parent acceptance bind the rows carrying those letters. Runtime A–N bind the runtime rows; Web acceptance binds WEB rows; product A–K bind PCT rows; Assurance tracer/negative criteria bind AF/HARD/OH rows. Per-task inline acceptance remains additional, not replaced. A criterion that cannot resolve to a row and concrete fixture is a planning gap. Completion gates remain open until actual fresh independent qualification; future execution fixtures remain unrun until authorized.
