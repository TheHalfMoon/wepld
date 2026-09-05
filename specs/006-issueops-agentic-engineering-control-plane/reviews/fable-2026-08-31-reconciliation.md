# Fable Architecture Review Reconciliation — 2026-08-31

```text
STATUS = HISTORICAL_REVIEW_RECONCILIATION_EVIDENCE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_REVIEW_ARTIFACT = USER_PROVIDED_EXTERNAL_FILE
SOURCE_VERDICT = ACCEPTABLE_WITH_REPAIRS
REVIEWED_MAIN = 573670eca575a5972e52b623b01b3143d036d281
REVIEWED_PR241_HEAD = 4558bb3d484316de03a87c98a4d383ce9cb6a20f
REVIEWED_PR241_TREE = e7283b53a3ab527dbac7b6f6326b9b9dae5b057a
REVIEWED_PR240_HEAD = 62991eed3e658209635dd5540148842d8917c166
HISTORICAL_POST_REVIEW_REPAIR_HEAD = 797b143bc9a0f83b1ca30cd4a178d71e04b2e346
HISTORICAL_POST_REVIEW_REPAIR_TREE = b35675ce2d5a22583a050f63e40ef8330e1e8a4c
LIVE_CURRENT_HEAD = MUST_BE_READ_FROM_GITHUB
```

This document records reconciliation of the Fable / Principal Architect review supplied outside the repository. It does not claim the source review satisfies the final independent-review gate. The candidate has materially evolved after the reviewed head, including WebMCP/browser planning, Native Assurance, OpenHands mechanism extraction, and the later professional whole-plan hardening review. A fresh exact-head whole-scope independent rereview is required.

The historical repair head/tree above identify one past post-review snapshot only. They MUST NOT be interpreted as the current PR head or current qualification evidence.

## Source-review accounting note

The supplied report contains five enumerated material finding IDs:

```text
ARCH-001       MEDIUM
ISSUEOPS-001   HIGH
RAG-001        MEDIUM
DELEGATE-001   MEDIUM
SECURITY-001   HIGH
```

but its final count states:

```text
CRITICAL = 0
HIGH = 2
MEDIUM = 4
LOW = 0
TOTAL_MATERIAL_FINDINGS = 6
```

The report also states that it did not inspect every file in the repository due to time constraints. The original requested review required either full requested-scope coverage or staged subreviews before claiming whole-repository coverage.

Therefore:

```text
SOURCE_REVIEW = USEFUL_MATERIAL_REVIEW_EVIDENCE
SOURCE_REVIEW_FINAL_QUALIFIED_WHOLE_REPO_GATE = NO
FRESH_EXACT_HEAD_REREVIEW = REQUIRED
```

No missing sixth finding is invented. The fresh rereview must reconcile its own finding table/count and coverage declaration.

## Finding reconciliation

### ARCH-001 — PARTIALLY_ACCEPTED_REPAIRED

**Valid concern:** Canonical control-plane layers can become implementation/deployment overengineering if treated as mandatory services before product value is proven.

**Rejected repair direction:** Collapsing Edara, Mirefa, and Nawat into one authority is not accepted. Canonical V2.3 deliberately separates minimum-sufficient topology/staffing, route/capability qualification, and effect-time authority.

**Repair:** Spec 006 states that these are semantic trust/ownership boundaries, not mandatory deployment units. Early tracer bullets may co-locate them as direct modules/contracts while preserving typed inputs/outputs and authority separation. TB0 requires no Agent Host/control-plane runtime.

**Disposition:** `REPAIRED`.

### ISSUEOPS-001 — ACCEPTED_REPAIRED

The backlog-sweep section was too abstract.

**Repair:** `plan.md` defines evidence requirements and negative oracles for exact/probable duplicates, common-root-cause groups, already-fixed-on-main, reproduction-missing, decision/dependency blocked, security-sensitive, small/high-confidence, and high-risk outputs. It requires a labeled corpus, predeclared thresholds, TP/FP/FN/abstention/evidence-coverage reporting, and forbids probable-duplicate auto-close or causal promotion from topic similarity alone. `tasks.md` contains corresponding qualification tasks.

**Disposition:** `REPAIRED`; fresh review required.

### RAG-001 — PARTIALLY_ACCEPTED_REPAIRED

**Valid concern:** Natural-language conceptual/paraphrastic queries may need semantic retrieval before a purely lexical pipeline achieves useful recall.

**Rejected implication:** Semantic/vector should not become an unconditional prerequisite.

**Repair:** The retrieval model is query/source-aware rather than a rigid ladder. Semantic/vector may be selected early for conceptual/paraphrastic queries, vocabulary mismatch, or measured low lexical recall. Admission still requires predeclared benchmark evidence of incremental value, privacy/cost/latency qualification, and an exit path. Fehrest.Maemar exact symbol/reference/call facts remain stronger evidence than similarity when available.

Later hardening additionally adds access-policy propagation, atomic generation publication, tombstone/redaction semantics, and remote URL security boundaries.

**Disposition:** `REPAIRED`.

### DELEGATE-001 — ACCEPTED_REPAIRED

The existing delegation flow named Mirefa -> Nawat -> Mission Runtime without sufficiently explicit interface/failure contracts.

**Repair:** `contracts/worker-delegation.md` defines canonical `WorkerRequirement`, worker descriptor semantics, `TopologyProposal`, `RouteQualification`, typed EffectProposal origin, Nawat decision, Mission Runtime Attempt/recovery handoffs, success/failure/recovery states, denial visibility, expiry/requalification, and negative oracles proving qualification cannot mint authority and runtime cannot widen/reuse grants or silently substitute routes.

**Disposition:** `REPAIRED`; fresh review required.

### SECURITY-001 — ACCEPTED_REPAIRED

The planning candidate lacked sufficient structural detail for prompt injection and malicious external content.

**Repair:** `constitution.md` defines explicit instruction/data separation and effect-origin rules. `contracts/untrusted-content.md` specifies canonical context-package semantics, trust/origin classes, access non-expansion/revocation, parser/active-content isolation, model/worker-output non-authority, egress controls, adversarial corpora, and effect-boundary negative oracles.

Sanitization or prompt filters are defense-in-depth only; they do not replace Nawat/effect-time enforcement.

**Disposition:** `REPAIRED`; fresh review required.

## Missing-capability reconciliation

### Conflicting provider observations — REPAIRED

`contracts/case-provider.md` and `data-model.md` define append-only `ProviderObservation` / `ProviderConflict` semantics, completeness/authenticity, conflict kinds, fail-closed dependent effects, and rejection of generic latest-write-wins resolution.

### First IssueOps tracer bullet — REPAIRED

`plan.md` defines TB0 as an offline/read-only end-to-end proof:

```text
InputArtifact(issue fixture)
-> Case
-> local repository/project identity
-> local cited retrieval
-> triage / reproduction readiness
-> relation candidates / decision boundary where needed
-> evidence-backed Case room summary
```

No network, provider writes, model/provider execution, Git writes, merge, or issue close are part of TB0.

### Case-model evolution — REPAIRED

`contracts/case-provider.md` defines adapter/normalization versioning and rules for keeping provider-specific semantics as extensions until provider-independent promotion is justified. Old observations and relation/conflict identities remain inspectable subject to current access/redaction/retention policy after upgrades.

### Trusted Completion evidence — REPAIRED

`plan.md`, `data-model.md`, `tasks.md`, and `acceptance.md` define the minimum CompletionEvidence packet and fail-closed exact-target/staleness/finding/authority/unknown-effect conditions.

## Overengineering / roadmap recommendation reconciliation

### Combine Edara + Mirefa + Nawat — REJECTED_SEMANTIC_COLLAPSE / ACCEPTED_IMPLEMENTATION_SIMPLIFICATION

Keep separate semantics; permit co-located/direct implementation until scaling/isolation requires separation.

### Consolidate `/delegate`, `/workers`, `/handoff` — PARTIALLY_ACCEPTED

The commands represent different intents and remain available, but initial UX uses progressive disclosure: `/delegate` is primary; `/workers` and `/handoff` may remain advanced surfaces until worker interoperability exists.

### RAG `add` vs `add --text` — ACCEPTED_AS_SYNTAX_ONLY

`add --text` is syntax sugar over inline-text InputArtifact ingestion, not a separate architecture/storage route.

### Move worker delegation S6 -> S5 — PARTIALLY_ACCEPTED

S5 permits delegation **dry-run contracts only** using synthetic WorkerDescriptors and no worker/model/provider/process execution. Real Mission Runtime/UWC/Mirefa/Edara/Nawat execution remains S6-owned.

### Merge S7 + S8 — REJECTED

A tight feedback loop is desirable, but S7 independent Assurance remains semantically distinct from S8 repair/completion consumption so `ReviewOutcome != CompletionDecision` stays enforceable.

### Add S3/S4 intake-RAG checkpoint — ACCEPTED_REPAIRED

A no-agent/no-network local `InputArtifact -> KnowledgeCollection -> cited RetrievalEvidence` checkpoint is explicit in plan/tasks/acceptance.

## Post-review scope expansion

After the Fable-reviewed predecessor head, the candidate materially expanded with:

- `web-agent.md` and canonical `contracts/web-agent-boundary.md`;
- browser/WebMCP task/acceptance/source-acquisition records;
- Native Assurance `/review`, `/security`, `/fulltest` planning and contracts;
- Assurance source-acquisition research;
- OpenHands mechanism extraction and integration task map;
- `reviews/professional-whole-plan-review-2026-09-02.md` and its hardening repairs/task map.

None of this later scope was covered by the historical Fable review.

## Review-derived product priorities retained

1. Issue -> Trusted Completion automation with inspectable evidence.
2. Cross-provider Case graph with provenance/conflict preservation.
3. Durable organizational engineering memory that informs but never authorizes.
4. Qualified heterogeneous worker routing with explicit containment evidence.
5. Exact-target review and finding reconciliation before governed completion.

Browser/Assurance additions extend these priorities without making browser/session/tool/scanner/test state authority.

## Fresh rereview requirements

The next independent review must bind the exact current head and:

- inspect every changed Spec 006 artifact plus the controlling canonical/active authority chain;
- explicitly reconcile all five historical Fable findings;
- inspect WebMCP/browser-agent, Native Assurance, OpenHands-derived planning, and professional hardening changes;
- verify shared contract vocabulary is internally consistent;
- inspect IssueOps/RAG/untrusted-content/delegation/Nawat/Assurance/Trusted Completion interactions;
- state whether any additional material findings exist;
- ensure finding table and final severity totals match;
- provide an honest exact file/context coverage declaration;
- return zero unresolved material findings before the planning candidate may satisfy its final independent-review gate.
