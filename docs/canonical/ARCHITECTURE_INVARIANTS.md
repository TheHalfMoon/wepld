# WePLD Architecture Invariants

These invariants are non-bypassable unless superseded by an explicit founder-ratified architecture decision.

## Authority

- `ReviewOutcome != CompletionDecision`.
- A finding never grants write, merge, deploy, publish, release, or acceptance authority.
- Builders and acceptance-critical reviewers may not self-certify their own work.
- UI modes, CLI flags, model choices, plugin presence, parent-child agent relationships, memory, context, and provenance do not mint authority.
- Nawat owns effect-time grants and revalidation.
- Trusted Completion is separate from CI, merge, deploy, publish, or reviewer approval.

## Evidence

- Unknown, missing, malformed, stale, unavailable, or incomplete evaluator/context/coverage evidence fails closed.
- Evaluator failure must never fabricate a quality score.
- A citation is provenance evidence, not automatic truth.
- Rerank/retrieval/model scores are not authority or acceptance.
- Claims of containment, durability, recovery, rollback, or local-only processing require evidence matching the exact claim.

## Project Brain

- Fehrest context informs but never authorizes.
- Canonical durable project memory outranks chat memory.
- Human-readable Markdown may project canonical truth but does not silently replace typed operational authority.
- Learned preferences are candidates until qualified; repetition is not proof of correctness.

## Workers and routing

- Models/workers/tools are replaceable.
- No silent route/provider/model fallback.
- Mirefa qualifies routes/capabilities.
- Edara uses the minimum sufficient worker topology.
- Parallelism is justified only by marginal accepted-outcome value exceeding coordination/risk cost.

## Reuse

- Solved commodity machinery must be acquired, adapted, ported, packaged, benchmarked, or referenced before custom implementation is justified.
- Every reused mechanism remains behind a WePLD-owned contract.
- Upstream tests, fixtures, failure corpora, and negative oracles are first-class acquisition targets.
- Source presence or permissive license does not equal admission.

## Fresh reconstitution

- Old repository content is historical evidence, not current authority.
- No old code or document is retained merely because it exists.
- Salvage requires exact origin/path, immutable identity when available, retained concept/mechanism, reason, destination, and disposition.
