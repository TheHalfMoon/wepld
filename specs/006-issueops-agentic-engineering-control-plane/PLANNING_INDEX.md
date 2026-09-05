# Spec 006 — Planning Index

```text
STATUS = FUTURE_PLANNING_INDEX
SPEC = 006_ISSUEOPS_AGENTIC_ENGINEERING_CONTROL_PLANE
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

This index defines the recommended reading order and ownership map for the Spec 006 planning package. It exists because the package is intentionally cross-cutting and now contains multiple contracts/addenda/research records. It does not make Spec 006 canonical implementation authority.

## 1. Start here

1. `spec.md` — parent product requirements.
2. `plan.md` — parent product/roadmap/tracer-bullet architecture.
3. `acceptance.md` — parent planning-coherence acceptance criteria.
4. `data-model.md` — canonical shared domain field vocabulary except where a dedicated contract explicitly owns a type.
5. `tasks.md` — parent dependency-ordered planning tasks.

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

### Browser / web

- `contracts/web-agent-boundary.md`

### Assurance / review

- `contracts/assurance-fabric.md`
- `contracts/review-independence.md`
- `contracts/command-surface.md`

## 3. Normative planning addenda

These extend the parent `spec.md` / `plan.md` / `acceptance.md` without changing roadmap numbering:

- `assurance-fabric-spec-addendum.md`
- `assurance-fabric-plan.md`
- `runtime-execution-fabric-spec-addendum.md`
- `runtime-execution-fabric-acceptance.md`
- `omnigent-plan-hardening-addendum.md`
- `web-agent.md`
- `web-agent-acceptance.md`

If an addendum and parent document appear to conflict, treat the planning package as **not internally coherent** until reconciled; do not silently choose one.

## 4. Task maps

- `assurance-fabric-tasks.md`
- `professional-plan-hardening-tasks.md`
- `openhands-assurance-integration-tasks.md`
- `omnigent-execution-fabric-integration-tasks.md`
- `runtime-distributed-safety-tasks.md`
- `web-agent-tasks.md`

Task-map presence does not activate implementation. The canonical owning slice/authority artifact remains controlling.

## 5. Source-acquisition / mechanism research

### General source-acquisition boundary

- `source-acquisition.md`
- `research/native-assurance-source-acquisition-2026-09-02.md`

### Specific mechanism quarries

- `research/munder-difflin-2026-09-01.md`
- `research/openhands-qualified-mechanism-extraction-2026-09-02.md`
- `research/omnigent-qualified-mechanism-extraction-2026-09-04.md`

Research records do not admit source, dependencies, processes, providers, models, browsers, or network access.

## 6. Review / reconciliation history

- `reviews/fable-2026-08-31-reconciliation.md` — historical predecessor architecture review/reconciliation.
- `reviews/professional-whole-plan-review-2026-09-02.md` — historical internal hardening review; its footer under-counted the enumerated findings and must not be used as final exact-head review accounting.
- later exact-head whole-plan review artifacts supersede historical status while preserving history.

No internal/self-authored planning review satisfies the required independent acceptance review.

## 7. Ownership map

```text
Case/provider semantics             -> data-model + case-provider
RAG/source/access                   -> data-model + retrieval-rag
untrusted instruction boundary      -> untrusted-content
inter-worker coordination           -> case-bus
worker requirements/routing         -> data-model + worker-delegation
server/host/runner/runtime fabric   -> runtime-execution-fabric
split-brain/event/runtime safety    -> runtime-distributed-safety-addendum
behavior policy                     -> behavior-policy-boundary
browser/WebMCP                      -> web-agent-boundary
review/security/test assurance      -> assurance-fabric
reviewer independence               -> review-independence
user command catalog                -> command-surface
shared types not otherwise owned    -> data-model
```

## 8. Cross-cutting invariants

```text
PLANNING != IMPLEMENTATION_AUTHORITY
SOURCE_RESEARCHED != SOURCE_ADMITTED
PROVIDER_CAPABILITY != QUALIFIED_CAPABILITY
POLICY_ALLOW != NAWAT_GRANT
SERVER != HOST != RUNNER != WORKER != ATTEMPT
WORKTREE_ISOLATION != SANDBOX
PROCESS_TREE_CONTAINMENT != FS_OR_NETWORK_ISOLATION
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
MESSAGE_RECEIVED != WORKFLOW_INTENT
REVIEW_OUTCOME != COMPLETION_DECISION
DIFFERENT_VENDOR_ALONE != REVIEW_INDEPENDENCE_PROOF
RETRIEVAL_SCORE != TRUTH
BROWSER_SNAPSHOT_STALE != VALID_ACTION_TARGET
UNKNOWN_EFFECT_OUTCOME != SAFE_TO_RETRY
PREREQUISITE_EFFECT_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_BLOCKED
NEW_EXACT_HEAD -> PRIOR_ACCEPTANCE_CRITICAL_EVIDENCE_STALE
```

## 9. Roadmap placement

```text
S2 = prerequisite foundations only; Spec 006 execution remains inactive
S3 = trusted intake/process + host/runner/containment/env/native bridge foundations
S4 = Fehrest/RAG/source generation/access
S5 = workflow/spec planning + dry-run protocol/execution-envelope planning
S6 = Mission Runtime/UWC/Edara/Mirefa/Nawat integration + provider/runner execution fabric
S7 = Native Assurance + independent review/security/fulltest
S8 = controlled repair/effect dependency/landing/Trusted Completion consumption
S9 = complete evidence/runtime/quality/recovery lineage
S10 = organization-scale analytics/federation/scheduling
```

## 10. Acceptance sequence for this planning package

Before any merge/acceptance claim for PR #241:

1. reread current canonical `main` governance;
2. reconcile the planning branch non-destructively with current canonical main;
3. verify the resulting whole diff is planning/spec/research-only;
4. run fresh exact-head deterministic qualification;
5. obtain a genuinely independent exact-head whole-scope engineering/correctness review;
6. reconcile every material finding;
7. prove zero unresolved material review threads;
8. verify finding counts/coverage declarations are internally consistent;
9. run final base/head/tree/diff/check/review race verification;
10. merge only if canonical governance then permits it.

Even after planning merge, each future implementation tranche remains separately gated by its owning canonical authority.