# Fable Architecture Review Reconciliation — 2026-08-31

```text
STATUS = REVIEW_RECONCILIATION_EVIDENCE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_REVIEW_ARTIFACT = USER_PROVIDED_EXTERNAL_FILE
SOURCE_VERDICT = ACCEPTABLE_WITH_REPAIRS
REVIEWED_MAIN = 573670eca575a5972e52b623b01b3143d036d281
REVIEWED_PR241_HEAD = 4558bb3d484316de03a87c98a4d383ce9cb6a20f
REVIEWED_PR241_TREE = e7283b53a3ab527dbac7b6f6326b9b9dae5b057a
REVIEWED_PR240_HEAD = 62991eed3e658209635dd5540148842d8917c166
```

This document records reconciliation of the Fable / Principal Architect review supplied outside the repository. It does not claim the source review satisfies the final independent-review gate; a fresh review is required on the repaired exact head.

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

**Rejected repair direction:** Collapsing Edara, Mirefa, and Nawat into one `WorkerLicensing` authority is not accepted. Canonical V2.3 deliberately separates minimum-sufficient topology/staffing, route/capability qualification, and effect-time authority. Collapsing those semantics would weaken `qualification != authorization` and create a second/ambiguous authority model.

**Repair:** Spec 006 now explicitly states that these are semantic trust/ownership boundaries, not mandatory deployment units. Early tracer bullets may co-locate them as direct modules/contracts while preserving typed inputs/outputs and authority separation. TB0 intentionally requires no Agent Host/control-plane runtime at all.

**Disposition:** `REPAIRED`.

### ISSUEOPS-001 — ACCEPTED_REPAIRED

The backlog-sweep section was too abstract.

**Repair:** `plan.md` now defines evidence requirements and negative oracles for exact/probable duplicates, common-root-cause groups, already-fixed-on-main, reproduction-missing, decision/dependency blocked, security-sensitive, small/high-confidence, and high-risk outputs. It requires a labeled corpus, predeclared thresholds, TP/FP/FN/abstention/evidence-coverage reporting, and forbids probable-duplicate auto-close or causal promotion from topic similarity alone. `tasks.md` contains corresponding qualification tasks.

**Disposition:** `REPAIRED`; fresh review required.

### RAG-001 — PARTIALLY_ACCEPTED_REPAIRED

**Valid concern:** Natural-language conceptual/paraphrastic queries may need semantic retrieval before a purely lexical pipeline achieves useful recall.

**Rejected implication:** Semantic/vector should not become an unconditional earlier prerequisite. The source report itself also states that exact/lexical/structured-first with optional vector is sound.

**Repair:** The retrieval model is now query/source-aware rather than a rigid ladder. Semantic/vector may be selected early for conceptual/paraphrastic queries, vocabulary mismatch, or measured low lexical recall. Admission still requires predeclared benchmark evidence of incremental value, privacy/cost/latency qualification, and an exit path. Fehrest.Maemar exact symbol/reference/call facts remain stronger evidence than similarity when available.

**Disposition:** `REPAIRED`.

### DELEGATE-001 — ACCEPTED_REPAIRED

The existing delegation flow named Mirefa -> Nawat -> Mission Runtime without sufficiently explicit interface/failure contracts.

**Repair:** `contracts/worker-delegation.md` now defines candidate `TopologyProposal`, `RouteQualification`, `NawatDecision`, and Mission Runtime Attempt handoffs, including required fields, success/failure states, denial visibility, expiry/requalification, and negative oracles proving qualification cannot mint authority and runtime cannot widen/reuse grants or silently substitute routes.

**Disposition:** `REPAIRED`; fresh review required.

### SECURITY-001 — ACCEPTED_REPAIRED

The planning candidate lacked sufficient structural detail for prompt injection and malicious external content.

**Repair:** `constitution.md` now defines explicit instruction/data separation and effect-origin rules. New `contracts/untrusted-content.md` specifies trust/origin classes, context-package manifests, access non-expansion, parser/active-content isolation, model/worker-output non-authority, egress controls, adversarial corpora, and effect-boundary negative oracles. `tasks.md` adds qualification tasks through S3/S4/S5/S6/S7.

Sanitization or prompt filters are explicitly defense-in-depth only; they do not replace Nawat/effect-time enforcement.

**Disposition:** `REPAIRED`; fresh review required.

## Missing-capability reconciliation

### Conflicting provider observations — REPAIRED

`contracts/case-provider.md` and `data-model.md` now define append-only `ProviderObservation` / `ProviderConflict` semantics, conflict kinds, fail-closed dependent effects, and rejection of generic latest-write-wins resolution.

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

`contracts/case-provider.md` defines adapter/normalization versioning and rules for keeping provider-specific semantics as extensions until provider-independent promotion is justified. Old raw observations and relation/conflict evidence remain inspectable after upgrades.

### Trusted Completion evidence — REPAIRED

`plan.md`, `data-model.md`, `tasks.md`, and `acceptance.md` now define the minimum CompletionEvidence packet and fail-closed exact-target/staleness/finding/authority conditions.

## Overengineering / roadmap recommendation reconciliation

### Combine Edara + Mirefa + Nawat — REJECTED_SEMANTIC_COLLAPSE / ACCEPTED_IMPLEMENTATION_SIMPLIFICATION

Keep separate semantics; permit co-located/direct implementation until scaling/isolation requires separation.

### Consolidate `/delegate`, `/workers`, `/handoff` — PARTIALLY_ACCEPTED

The commands represent different intents and remain available, but initial UX uses progressive disclosure: `/delegate` is primary; `/workers` and `/handoff` may remain advanced surfaces until worker interoperability exists.

### RAG `add` vs `add --text` — ACCEPTED_AS_SYNTAX_ONLY

`add --text` is now explicitly syntax sugar over inline-text InputArtifact ingestion, not a separate architecture/storage route.

### Move worker delegation S6 -> S5 — PARTIALLY_ACCEPTED

S5 now permits delegation **dry-run contracts only** using synthetic WorkerDescriptors and no worker/model/provider/process execution. Real Mission Runtime/UWC/Mirefa/Edara/Nawat execution remains S6-owned.

### Merge S7 + S8 — REJECTED

A tight feedback loop is desirable, but S7 independent Assurance must remain semantically distinct from S8 repair/completion consumption so `ReviewOutcome != CompletionDecision` remains enforceable.

### Add S3/S4 intake-RAG checkpoint — ACCEPTED_REPAIRED

A no-agent/no-network local `InputArtifact -> KnowledgeCollection -> cited RetrievalEvidence` checkpoint is now explicit in plan/tasks/acceptance.

## Review-derived product priorities retained

The repair preserves the five differentiation directions identified by Fable:

1. Issue -> Trusted Completion automation with inspectable evidence.
2. Cross-provider Case graph with provenance/conflict preservation.
3. Durable organizational engineering memory that informs but never authorizes.
4. Qualified heterogeneous worker routing with explicit containment evidence.
5. Exact-target review and finding reconciliation before governed completion.

## Fresh rereview requirements

The next independent review must bind the repaired exact head and:

- inspect every changed Spec 006 artifact plus the controlling canonical/active authority chain;
- explicitly reconcile all five listed source-review findings;
- state whether any additional material findings exist;
- ensure finding table and final severity totals match;
- provide an honest coverage declaration; if full requested scope needs staged subreviews, perform them before the final synthesis;
- return zero unresolved material findings before the planning candidate may satisfy its final independent-review gate.
