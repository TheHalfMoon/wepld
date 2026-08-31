# Clarify — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CLARIFICATIONS
IMPLEMENTATION_AUTHORITY = NONE
```

## Resolved planning clarifications

### Q1 — Is GitHub the internal issue model?

No. GitHub is the first reference provider. WePLD owns a provider-neutral `Case` identity/lifecycle/evidence model.

### Q2 — Can provider state set Case completion?

No. Provider open/closed/merged/resolved state is evidence only. Trusted Completion is a separate governed decision.

### Q3 — How are conflicting provider observations handled?

Observations remain append-only. Generic latest-write-wins is prohibited for cross-provider semantics. Acceptance/effect paths that require one current semantic must re-observe, abstain/fail closed, resolve through an explicit rule, or open a DecisionBoundary. The losing/older evidence remains inspectable.

### Q4 — Does adding a new provider require expanding the Case schema?

Not by default. Provider-specific fields remain adapter observations/extensions. Core Case semantics evolve only when provider-independent engineering meaning is justified and the adapter/normalization migration is explicitly versioned.

### Q5 — Is `/issues sweep` allowed to produce opaque AI clusters?

No. Every output class must have inspectable evidence requirements and negative oracles. Probable duplicates cannot auto-close or merge Case identity. Common-root-cause requires causal evidence stronger than topic/semantic similarity. Recommendation thresholds are predeclared and measured against a labeled corpus.

### Q6 — Is semantic/vector retrieval a mandatory later step after lexical retrieval?

No. Retrieval signals are query/source aware, not a rigid sequence. Semantic/vector may be selected early for conceptual/paraphrastic queries or measured lexical recall gaps, but remains optional and requires predeclared incremental-value qualification before admission.

### Q7 — What is the minimum useful RAG capability?

A user can ingest qualified local sources into a named collection, ask natural-language/exact/code-reference questions, receive inspectable cited evidence, see stale/conflicting/no-answer states, and do so without requiring embeddings/vector infrastructure.

### Q8 — Can retrieved or provider content instruct agents?

Not merely by containing imperative text. External/retrieved/repository/worker/model content is data by default. It cannot mint WorkflowIntent, authority, paid/remote routes, broader context access, review approval, or Trusted Completion. Prompt filtering is defense-in-depth; effect-time structural enforcement remains required.

### Q9 — Must Edara, Mirefa, Nawat, Mission Runtime, and UWC be separate services from the beginning?

No. They are semantic trust/ownership boundaries, not mandatory deployment units. Early implementations may co-locate them as direct modules/contracts. Their authority distinctions must remain enforceable and evidenced.

### Q10 — Can Mirefa qualification authorize execution?

No. Mirefa says whether a route is qualified for consideration. Nawat alone owns effect-time authority/revalidation. Mission Runtime may execute only within the exact current grant/containment constraints and cannot widen or silently substitute them.

### Q11 — Should delegation move into S5 to prove value sooner?

Only as a dry-run planning contract. S5 may construct Assignment/WorkerRequirement/TopologyProposal against synthetic workers. Real worker/model/provider/process execution and the full Edara/Mirefa/Nawat/Mission Runtime path remain S6-owned.

### Q12 — Should S7 and S8 be merged to tighten review/repair feedback?

No semantic merge. A tight feedback loop is desirable, but Assurance must remain independent from the repair/completion boundary consuming findings so `ReviewOutcome != CompletionDecision` remains structural.

### Q13 — What is the first IssueOps end-to-end tracer bullet?

TB0 is offline/read-only: synthetic/local issue artifact -> Case -> local repository identity -> cited local retrieval -> triage/reproduction-readiness/relations/decision frontier -> evidence-backed Case summary. No network, provider write, model/provider execution, Git write, merge, or issue close is required.

### Q14 — What must Trusted Completion prove?

It must bind exact accepted target/generation, deterministic gates, genuine independent review, security review or qualified not-applicable basis, all material finding reconciliations, material effect/authority evidence, provider closeout where required, residual limitations, and the completion decision producer. Stale/mismatched evidence or unresolved findings fail closed.

### Q15 — Are all proposed slash commands day-one primary UX?

No. The catalog describes native intent surfaces. Initial UX should expose a smaller primary set through `/askme` and progressive disclosure. Specialist worker controls such as `/workers` and `/handoff` may remain advanced until their owning capabilities exist.

## Deferred owning-slice decisions

The following remain intentionally deferred because this planning candidate does not have implementation/source/dependency authority:

- exact GitHub app/token/authentication model;
- webhook vs polling implementation and replay storage;
- exact parser implementations and archive/document policies;
- lexical index engine;
- vector database/embedding model, if benchmark-justified;
- first concrete worker/provider adapters;
- exact policy-engine/sandbox implementation;
- exact persistent event-store representation and retention thresholds;
- organization-scale scheduling/resource policy;
- numeric autonomy-promotion and sweep-action thresholds, which must be declared before their owning benchmark run.
