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

## B. IssueOps completeness

- [ ] Defines a provider-neutral `Case` rather than making GitHub the core model.
- [ ] Places GitHub first while keeping later providers behind adapters.
- [ ] Separates Case lifecycle from provider state.
- [ ] Covers ingest, triage, reproduction, diagnosis, planning, delegation, implementation, verification, review, repair, landing, closeout, and completion evidence.
- [ ] Defines backlog sweep, duplicate/common-root-cause analysis, Case rooms, and decision-boundary escalation.
- [ ] Defines autonomy ceilings without treating them as authorization.

## C. RAG completeness

- [ ] Defines arbitrary supported source ingestion and named knowledge collections.
- [ ] Defines session/project/workspace/global scopes.
- [ ] Defines provenance/freshness/citation evidence.
- [ ] Keeps exact/lexical/structured/graph retrieval available without requiring vectors.
- [ ] Makes vector/semantic machinery optional and source-acquisition gated.
- [ ] Explicitly prevents retrieval evidence from becoming truth or authority.

## D. Intake completeness

- [ ] Defines one `InputArtifact` contract for native drop and terminal path-paste behavior.
- [ ] Supports files/directories/text/URL/provider-attachment style inputs as planned source kinds.
- [ ] Explicitly prevents drop/paste from executing, fetching, installing, mutating, or egressing by itself.
- [ ] Includes negative-oracle requirements for unsafe implicit effects.

## E. Workflow-skill completeness

- [ ] Defines `/askme`, `/btw`, `/rag`, `/issues`, `/triage`, `/grill`, `/architect`, `/spec`, `/tickets`, `/build`, `/debug`, `/review`, `/prototype`, `/research`, `/wayfinder`, `/handoff`, `/teach`, `/questionnaire`, `/wizard`, `/retro`, `/workflow`, `/delegate`, and `/workers` as planned native surfaces.
- [ ] Maps reusable Matt-derived methods to internal capabilities instead of forcing every donor skill into a command.
- [ ] Records all 37 studied Matt skill definitions.
- [ ] Prevents donor branding from becoming the core product architecture.

## F. Delegation completeness

- [ ] Records all 18 studied delegate-skills definitions.
- [ ] Defines one provider-neutral delegation surface.
- [ ] Defines worker capability, containment, cost, provider identity, session, availability, and qualification metadata.
- [ ] Separates provider “read-only” claims from WePLD containment evidence.
- [ ] Prohibits silent provider/model/worker fallback and silent paid/quota consumption.
- [ ] Distinguishes `/delegate` assignment from `/handoff` context/session transfer.

## G. Delivery safety

- [ ] Uses vertical tracer bullets rather than a monolithic autonomous-engineer implementation.
- [ ] Delays `land` until lower autonomy ceilings are qualified.
- [ ] Requires exact-target/version/idempotency semantics for external writes.
- [ ] Requires independent review and finding reconciliation for material autonomous changes.
- [ ] Proves merge/issue closeout do not themselves establish Trusted Completion.
- [ ] Preserves failed/reassigned attempts and findings in durable history.

## H. Source-acquisition completeness

- [ ] Records `mattpocock/skills@6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` as research-only candidate.
- [ ] Records `amElnagdy/delegate-skills@b781ee2e23089630e2fbee1cfd6174afe4edeb76` as research-only candidate.
- [ ] Records observed MIT licensing without treating licensing as admission.
- [ ] Requires a separately governed future source-registry revision before reuse/import.
- [ ] Requires per-capability minimum reuse decisions rather than wholesale copying.

## I. Planning review gate

Before this planning candidate can be treated as accepted planning evidence:

```text
TRUSTED_BASE_REREAD = REQUIRED
EXACT_HEAD_DETERMINISTIC_GATES = REQUIRED
INDEPENDENT_CORRECTNESS_ENGINEERING_REVIEW = REQUIRED
SECURITY_REVIEW = NOT_APPLICABLE only if the final diff remains documentation/specification-only and changes no executable/trust boundary
UNRESOLVED_MATERIAL_FINDINGS = 0
UNRESOLVED_REVIEW_THREADS = 0
FINAL_RACE_RECHECK = REQUIRED
MERGE = AUTHORIZED_ONLY_AFTER_ALL_APPLICABLE_GATES
```

Even after merge, future implementation remains separately gated by the owning slices.
