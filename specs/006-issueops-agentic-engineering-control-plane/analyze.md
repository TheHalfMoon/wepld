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
