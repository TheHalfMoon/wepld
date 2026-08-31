# Acceptance — IssueOps Agentic Engineering Control Plane Planning Candidate

```text
STATUS = PLANNING_ACCEPTANCE_CRITERIA
IMPLEMENTATION_AUTHORITY = NONE
```

This file defines what must be true for the planning candidate itself to be considered internally coherent. It does not accept or activate product implementation.

## A. Governance fit

- [ ] Preserves canonical P0 + S1..S10 roadmap numbering.
- [ ] Adds no S2 product scope.
- [ ] Adds no implementation, source, dependency, network, model/provider, Git-write, or issue-provider-write authority.
- [ ] Preserves Nawat as the only effect-time authority.
- [ ] Preserves Mirefa qualification, Edara minimum-sufficient topology, Mission Runtime execution, UWC normalization, Assurance, and Trusted Completion separation.
- [ ] Preserves `RETRIEVAL_SCORE != TRUTH`, `GREEN_CI != CompletionDecision`, and no-silent-fallback invariants.
- [ ] Makes clear that named architecture boundaries are semantic contracts and may be co-located in early implementations without collapsing their authority/trust semantics.

## B. IssueOps completeness

- [ ] Defines a provider-neutral `Case` rather than making GitHub the core model.
- [ ] Places GitHub first while keeping later providers behind adapters.
- [ ] Separates Case lifecycle from provider state.
- [ ] Preserves contradictory provider observations explicitly and defines fail-closed/abstention behavior when acceptance/effects require one current semantic.
- [ ] Defines provider/normalization schema evolution without silently promoting provider-specific fields into core Case semantics.
- [ ] Covers ingest, triage, reproduction, diagnosis, planning, delegation, implementation, verification, review, repair, landing, closeout, and completion evidence.
- [ ] Defines backlog sweep, duplicate/common-root-cause analysis, Case rooms, and decision-boundary escalation.
- [ ] Defines concrete evidence requirements for exact/probable duplicate, root-cause, already-fixed, reproduction-missing, blocked, security-sensitive, execution-candidate, and high-risk sweep outputs.
- [ ] Defines labeled corpus, predeclared quality thresholds, TP/FP/FN/abstention/evidence-coverage reporting, and negative oracles for recommendation-only sweep qualification.
- [ ] Prohibits probable duplicate auto-close and semantic/topic similarity from becoming exact/causal relations without stronger evidence.
- [ ] Defines autonomy ceilings without treating them as authorization.
- [ ] Defines TB0 as an offline/read-only end-to-end Case -> local retrieval -> triage -> evidence proof before agent/provider complexity.

## C. RAG completeness

- [ ] Defines arbitrary supported source ingestion and named knowledge collections.
- [ ] Defines session/project/workspace/global scopes.
- [ ] Defines provenance/freshness/citation evidence.
- [ ] Keeps exact/lexical/structured/graph retrieval available without requiring vectors.
- [ ] Treats retrieval signals as minimum-sufficient/query-aware rather than a rigid serial ladder.
- [ ] Defines when semantic/vector is a justified candidate signal and requires predeclared benchmark evidence of incremental value before admission.
- [ ] Defines Fehrest.Maemar exact fact/provenance integration as stronger evidence than similarity when exact graph/source facts exist.
- [ ] Makes vector/semantic machinery optional and source-acquisition gated.
- [ ] Explicitly prevents retrieval evidence from becoming truth or authority.
- [ ] Requires no-answer/abstention and stale/conflicting-source test cases.

## D. Intake completeness

- [ ] Defines one `InputArtifact` contract for native drop and terminal path-paste behavior.
- [ ] Supports files/directories/text/URL/provider-attachment style inputs as planned source kinds.
- [ ] Explicitly prevents drop/paste from executing, fetching, installing, mutating, or egressing by itself.
- [ ] Defines trust/origin classification for context candidates.
- [ ] Includes negative-oracle requirements for unsafe implicit effects and active-content/parser behavior.
- [ ] Defines an S3/S4 checkpoint proving local InputArtifact -> KnowledgeCollection -> cited RetrievalEvidence with no agent/network/provider effects.

## E. Untrusted content / prompt injection

- [ ] Defines `EXTERNAL_CONTENT != INSTRUCTION_AUTHORITY` and `RETRIEVED_TEXT != TOOL_INTENT` structurally, not only as prompt guidance.
- [ ] Defines trust/origin labels and a context-package manifest.
- [ ] Requires effect proposals to originate from explicit WorkflowIntent/Assignment/policy rather than instructions found only in untrusted content.
- [ ] Prohibits untrusted content from expanding file/secret/collection/network/provider/cost/autonomy visibility or authority.
- [ ] Separates parser/active-content qualification from ordinary ingestion.
- [ ] Treats model/worker/review output as non-authoritative evidence requiring normal follow-on qualification/authorization.
- [ ] Requires adversarial corpora for direct/indirect prompt injection, fake policy/review/grant text, secret requests, tool coercion, obfuscation, cross-source conflicts, and worker/model output escalation.
- [ ] Proves prompt-level manipulation remains unable to bypass effect-time authorization/containment/review boundaries even if sanitization/classification fails.

## F. Workflow-skill completeness

- [ ] Defines `/askme`, `/btw`, `/rag`, `/issues`, `/triage`, `/grill`, `/architect`, `/spec`, `/tickets`, `/build`, `/debug`, `/review`, `/prototype`, `/research`, `/wayfinder`, `/handoff`, `/teach`, `/questionnaire`, `/wizard`, `/retro`, `/workflow`, `/delegate`, and `/workers` as planned native surfaces.
- [ ] Distinguishes the command catalog from day-one primary UX; supports progressive disclosure and advanced worker controls.
- [ ] Maps reusable Matt-derived methods to internal capabilities instead of forcing every donor skill into a command.
- [ ] Makes domain modeling and deep-module/boundary analysis explicit reusable workflow primitives.
- [ ] Records all 37 studied Matt skill definitions.
- [ ] Prevents donor branding from becoming the core product architecture.

## G. Delegation completeness

- [ ] Records all 18 studied delegate-skills definitions.
- [ ] Defines one provider-neutral delegation surface.
- [ ] Defines worker capability, containment, cost, provider identity, session, availability, and qualification metadata.
- [ ] Defines explicit typed Edara `TopologyProposal`, Mirefa `RouteQualification`, Nawat effect decision, and Mission Runtime Attempt boundaries with success/failure states.
- [ ] Proves qualification cannot create effect authority and Mission Runtime cannot widen/reuse grants or silently substitute workers/providers/models.
- [ ] Makes Nawat denial/requalification/stale-target states visible as workflow frontiers rather than generic worker failures.
- [ ] Separates provider “read-only” claims from WePLD containment evidence.
- [ ] Prohibits silent provider/model/worker fallback and silent paid/quota consumption.
- [ ] Distinguishes `/delegate` assignment from `/handoff` context/session transfer.
- [ ] Allows S5 delegation dry-run over synthetic workers without pulling real worker/model/process execution or Nawat runtime authority before S6.

## H. Delivery safety

- [ ] Uses vertical tracer bullets rather than a monolithic autonomous-engineer implementation.
- [ ] Defines TB0/TB1/TB2/TB3/TB4/TB5 progression with explicit user value, effects, security boundary, negative oracles, evidence, and out-of-scope statements.
- [ ] Delays `land` until lower autonomy ceilings are qualified.
- [ ] Requires exact-target/version/idempotency semantics for external writes.
- [ ] Requires independent review and finding reconciliation for material autonomous changes.
- [ ] Preserves S7 Assurance production separately from S8 repair/completion consumption even when feedback loops are tight.
- [ ] Proves merge/issue closeout do not themselves establish Trusted Completion.
- [ ] Preserves failed/reassigned attempts and findings in durable history.

## I. Trusted Completion completeness

- [ ] Defines minimum CompletionEvidence fields for accepted target, reproduction/root-cause basis, change identity, deterministic gates, exact-target independent review, security review/applicable-N/A basis, reconciliations, authority/effect refs, provider closeout refs, residual limitations, and completion decision identity.
- [ ] Requires all acceptance-critical evidence to bind the exact accepted target/generation.
- [ ] Fails closed on stale/mismatched evidence, unresolved material findings, missing required authority evidence, or contradictory acceptance-critical provider state.
- [ ] Keeps merge/close/green-CI/model-review/provider state as evidence inputs, never the completion decision itself.

## J. Source-acquisition completeness

- [ ] Records `mattpocock/skills@6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` as research-only candidate.
- [ ] Records `amElnagdy/delegate-skills@b781ee2e23089630e2fbee1cfd6174afe4edeb76` as research-only candidate.
- [ ] Records observed MIT licensing without treating licensing as admission.
- [ ] Requires a separately governed future source-registry revision before reuse/import.
- [ ] Requires per-capability minimum reuse decisions rather than wholesale copying.

## K. Planning review gate

Before this planning candidate can be treated as accepted planning evidence:

```text
TRUSTED_BASE_REREAD = REQUIRED
EXACT_HEAD_DETERMINISTIC_GATES = REQUIRED
INDEPENDENT_CORRECTNESS_ENGINEERING_REVIEW = REQUIRED
REVIEW_COVERAGE_DECLARATION = REQUIRED
REVIEW_FINDING_COUNT_INTERNAL_CONSISTENCY = REQUIRED
SECURITY_REVIEW = NOT_APPLICABLE only if the final diff remains documentation/specification-only and changes no executable/trust boundary
UNRESOLVED_MATERIAL_FINDINGS = 0
UNRESOLVED_REVIEW_THREADS = 0
FINAL_RACE_RECHECK = REQUIRED
MERGE = AUTHORIZED_ONLY_AFTER_ALL_APPLICABLE_GATES
```

A review that explicitly samples only part of the requested whole-repository scope or whose finding table/counts are internally inconsistent may provide useful review evidence, but it does not satisfy the final qualified review gate until a fresh exact-head review closes those coverage/accounting gaps.

Even after merge, future implementation remains separately gated by the owning slices.
