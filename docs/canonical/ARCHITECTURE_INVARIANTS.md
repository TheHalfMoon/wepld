# WePLD Architecture Invariants

## Authority

- `ReviewOutcome != CompletionDecision`.
- Findings never grant write, merge, deploy, publish, release, or acceptance authority.
- UI modes, flags, model choices, plugins, memory, context, provenance, or parent-agent identity do not mint authority.
- Nawat owns effect-time grants/revalidation.
- Trusted Completion remains separate from CI, merge, deploy, publish, and reviewer approval.

## Evidence

- Unknown/missing/malformed/stale evaluator, context, coverage, or containment evidence fails closed.
- Evaluator failure must never fabricate a quality score.
- Citation, retrieval score, rerank score, model confidence, or reviewer consensus is not automatic truth or authority.
- Recovery/rollback/durability/containment claims require evidence matching the exact claim.

## Project Brain

- Fehrest informs; it never authorizes.
- Repository canonical memory outranks chat memory.
- Learned preferences are candidates until qualified.

## Workers

- Models/workers/tools are replaceable.
- No silent provider/model/worker fallback.
- Mirefa qualifies; Edara uses minimum-sufficient topology; Nawat authorizes effects.

## Reuse

- Acquire solved machinery before custom implementation.
- Reused machinery remains behind WePLD-owned contracts.
- Tests, fixtures, failure corpora, and negative oracles are first-class acquisition targets.
- Source availability or permissive licensing does not equal admission.
