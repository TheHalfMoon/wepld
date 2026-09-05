# Acceptance — IssueOps Agentic Engineering Control Plane Planning Candidate

```text
STATUS = PLANNING_ACCEPTANCE_CRITERIA
IMPLEMENTATION_AUTHORITY = NONE
```

This file defines what must be true for the planning candidate itself to be considered internally coherent. It does not accept or activate product implementation.

## A. Governance fit

- [ ] Preserves canonical P0 + S1..S10 roadmap numbering.
- [ ] Adds no S2 product scope.
- [ ] Adds no implementation, source, dependency, network, model/provider, Git-write, browser, or issue-provider-write authority.
- [ ] Preserves Nawat as the only effect-time authority.
- [ ] Preserves Mirefa qualification, Edara minimum-sufficient topology, Mission Runtime execution, UWC normalization, Fehrest.Maemar graph ownership, AMAN security ownership, Assurance, and Trusted Completion separation.
- [ ] Preserves `RETRIEVAL_SCORE != TRUTH`, `GREEN_CI != CompletionDecision`, and no-silent-fallback invariants.
- [ ] Makes clear that named architecture boundaries are semantic contracts and may be co-located in early implementations without collapsing their authority/trust semantics.

## B. IssueOps completeness

- [ ] Defines a provider-neutral `Case` rather than making GitHub the core model.
- [ ] Places GitHub first while keeping later providers behind adapters.
- [ ] Separates Case lifecycle from provider state.
- [ ] Preserves contradictory provider observations explicitly and defines fail-closed/abstention behavior when acceptance/effects require one current semantic.
- [ ] Defines provider observation completeness/authenticity, pagination/permission/rate-limit limitations, and stale-state handling; partial/unauthenticated observations cannot masquerade as complete current state.
- [ ] Defines provider/normalization schema evolution without silently promoting provider-specific fields into core Case semantics.
- [ ] Defines provider webhook/event authenticity and duplicate-delivery identity as future qualification requirements.
- [ ] Covers ingest, triage, reproduction, diagnosis, planning, delegation, implementation, verification, review, repair, landing, closeout, and completion evidence.
- [ ] Defines backlog sweep, duplicate/common-root-cause analysis, Case rooms, and decision-boundary escalation.
- [ ] Defines concrete evidence requirements for exact/probable duplicate, root-cause, already-fixed, reproduction-missing, blocked, security-sensitive, execution-candidate, and high-risk sweep outputs.
- [ ] Defines labeled corpus, predeclared quality thresholds, TP/FP/FN/abstention/evidence-coverage reporting, and negative oracles for recommendation-only sweep qualification.
- [ ] Prohibits probable duplicate auto-close and semantic/topic similarity from becoming exact/causal relations without stronger evidence.
- [ ] Defines autonomy ceilings without treating them as authorization.
- [ ] Defines TB0 as an offline/read-only end-to-end Case -> local retrieval -> triage -> evidence proof before agent/provider complexity.

## C. RAG completeness

- [ ] Defines arbitrary supported source ingestion and named knowledge collections.
- [ ] Defines session/project/workspace/global scopes while keeping source access/visibility separate.
- [ ] Defines provenance/freshness/citation/access-policy evidence.
- [ ] Propagates source visibility/access policy through source generations, derived chunks/indexes/embeddings/graph views, RetrievalEvidence, ContextPackage, and worker/provider egress eligibility.
- [ ] Defines access revocation/redaction/tombstone behavior so stale derived caches cannot preserve broader visibility.
- [ ] Defines immutable complete source generations and atomic current-generation publication; mixed old/new refresh state cannot masquerade as one current view.
- [ ] Keeps exact/lexical/structured/graph retrieval available without requiring vectors.
- [ ] Treats retrieval signals as minimum-sufficient/query-aware rather than a rigid serial ladder.
- [ ] Defines when semantic/vector is a justified candidate signal and requires predeclared benchmark evidence of incremental value before admission.
- [ ] Defines Fehrest.Maemar exact fact/provenance integration as stronger evidence than similarity when exact graph/source facts exist.
- [ ] Makes vector/semantic machinery optional and source-acquisition gated.
- [ ] Explicitly prevents retrieval evidence from becoming truth or authority.
- [ ] Requires no-answer/abstention, stale/conflicting-source, access-revocation, and atomic-refresh test cases.
- [ ] Defines future remote URL/documentation ingestion security requirements for redirects, DNS rebinding, private/link-local/metadata targets, credential forwarding, and content/parser bounds before network activation.

## D. Intake / artifact completeness

- [ ] Defines one `InputArtifact` contract for native drop, terminal path-paste, and governed browser-download/upload handoff.
- [ ] Supports files/directories/text/URL/provider-attachment style inputs as planned source kinds.
- [ ] Explicitly prevents drop/paste/download from executing, fetching, installing, mutating, entering RAG, or egressing by itself.
- [ ] Defines trust/origin/access classification for context candidates.
- [ ] Includes negative-oracle requirements for unsafe implicit effects and active-content/parser behavior.
- [ ] Defines an S3/S4 checkpoint proving local InputArtifact -> KnowledgeCollection -> cited RetrievalEvidence with no agent/network/provider effects.

## E. Untrusted content / prompt injection

- [ ] Defines `EXTERNAL_CONTENT != INSTRUCTION_AUTHORITY` and `RETRIEVED_TEXT != TOOL_INTENT` structurally, not only as prompt guidance.
- [ ] Defines trust/origin labels and uses the canonical `ContextPackage` manifest vocabulary.
- [ ] Requires effect proposals to carry typed `controlling_origin_kind` + `controlling_origin_ref` and originate from allowed WorkflowIntent/Assignment/policy rather than instructions found only in untrusted content.
- [ ] Prohibits untrusted content from expanding file/secret/collection/network/provider/browser/artifact/cost/autonomy visibility or authority.
- [ ] Rechecks source/access visibility when context is used or egressed; old context packages cannot bypass revocation.
- [ ] Separates parser/active-content qualification from ordinary ingestion.
- [ ] Treats model/worker/review output as non-authoritative evidence requiring normal follow-on qualification/authorization.
- [ ] Requires adversarial corpora for direct/indirect prompt injection, fake policy/review/grant text, secret requests, tool coercion, obfuscation, cross-source conflicts, and worker/model output escalation.
- [ ] Proves prompt-level manipulation remains unable to bypass effect-time authorization/containment/review boundaries even if sanitization/classification fails.

## F. Workflow-skill completeness

- [ ] Uses `contracts/command-surface.md` as the canonical stable command catalog.
- [ ] Catalog includes `/askme`, `/btw`, `/issues`, `/rag`, `/web`, `/triage`, `/grill`, `/architect`, `/spec`, `/tickets`, `/build`, `/debug`, `/review`, `/security`, `/fulltest`, `/prototype`, `/research`, `/wayfinder`, `/handoff`, `/teach`, `/questionnaire`, `/wizard`, `/retro`, `/workflow`, `/delegate`, and `/workers`.
- [ ] Distinguishes the command catalog from day-one primary UX; supports progressive disclosure and advanced worker controls.
- [ ] Maps reusable Matt-derived methods to internal capabilities instead of forcing every donor skill into a command.
- [ ] Makes domain modeling and deep-module/boundary analysis explicit reusable workflow primitives.
- [ ] Records all 37 studied Matt skill definitions.
- [ ] Prevents donor branding from becoming the core product architecture.

## G. Delegation completeness

- [ ] Records all 18 studied delegate-skills definitions.
- [ ] Defines one provider-neutral delegation surface.
- [ ] Defines canonical `WorkerRequirement` and versioned worker capability vocabulary.
- [ ] Defines worker capability, provider-permission claims, containment evidence, cost, provider identity, session/cancellation/recovery semantics, availability, and qualification metadata.
- [ ] Defines explicit typed Edara `TopologyProposal`, Mirefa `RouteQualification`, Nawat effect decision, and Mission Runtime Attempt boundaries with success/failure/recovery states.
- [ ] Proves qualification cannot create effect authority and Mission Runtime cannot widen/reuse grants or silently substitute workers/providers/models.
- [ ] Makes Nawat denial/requalification/stale-target states visible as workflow frontiers rather than generic worker failures.
- [ ] Separates provider “read-only” claims from WePLD containment evidence.
- [ ] Prohibits silent provider/model/worker fallback and silent paid/quota consumption.
- [ ] Distinguishes `/delegate` assignment from `/handoff` context/session transfer.
- [ ] Defines cancel-request vs termination proof, safe-resume vs new-Attempt behavior, and orphan/unknown worker state.
- [ ] Allows S5 delegation dry-run over synthetic workers without pulling real worker/model/process execution or Nawat runtime authority before S6.

## H. Delivery / recovery safety

- [ ] Uses vertical tracer bullets rather than a monolithic autonomous-engineer implementation.
- [ ] Defines TB0/TB1/TB2/TB3/TB4/TB5 progression with explicit user value, effects, security boundary, negative oracles, evidence, and out-of-scope statements.
- [ ] Delays `land` until lower autonomy ceilings are qualified.
- [ ] Requires exact-target/version/idempotency semantics for external writes.
- [ ] Defines `EFFECT_OUTCOME_UNKNOWN` for interruptions where an external effect may have committed and requires reconciliation before unsafe retry.
- [ ] Requires independent review and finding reconciliation for material autonomous changes.
- [ ] Preserves S7 Assurance production separately from S8 repair/completion consumption even when feedback loops are tight.
- [ ] Proves merge/issue closeout/browser/WebMCP success do not themselves establish Trusted Completion.
- [ ] Preserves failed/reassigned attempts and findings in durable history.

## I. Native Assurance completeness

- [ ] Implements `/review`, `/security`, and `/fulltest` as profiles over one shared Assurance Fabric.
- [ ] Defines exact `AssuranceTarget`, including material dirty-workspace identity when the requested claim covers uncommitted state.
- [ ] Defines immutable/versioned `AssurancePolicySnapshot` for profile/claim meaning.
- [ ] Classifies checks as `REQUIRED`, `CONDITIONAL`, or `OPTIONAL` and prohibits budget/availability/authority limitations from silently downgrading required evidence.
- [ ] Defines typed `ClaimAssessment`: `SUPPORTED`, `NOT_SUPPORTED`, `PARTIALLY_SUPPORTED`, `INCONCLUSIVE`, `BLOCKED`, `STALE`.
- [ ] Missing/stale required evidence, unresolved blocking findings, or material unresolved conflicts prevent `SUPPORTED`.
- [ ] Binds acceptance-critical EngineRun to actual executable/runtime/artifact identity and material rule/database/template/config snapshots plus bounded resource/cleanup envelope.
- [ ] Defines stable finding fingerprint/correlation while preserving producer-specific evidence.
- [ ] Defines governed FindingDisposition for false positive/accepted risk/suppression/rule exception/fixed/superseded with scope, authority, policy/target, evidence, and expiry/review date.
- [ ] Defines EvidenceHandlingPolicy covering visibility, storage/encryption requirements where applicable, redaction, retention/tombstone, safe rendering, and export/egress.
- [ ] Defines review-context/file-scope coverage as typed evidence.
- [ ] Defines known-flake/quarantine ownership/expiry without erasing failure evidence.
- [ ] Defines qualified performance evidence with baseline/environment/repetitions/noise/decision rules.
- [ ] Preserves Fehrest.Maemar, AMAN, Nawat, S8, S9, and Trusted Completion ownership boundaries.

## J. Browser/WebMCP completeness

- [ ] Uses `contracts/web-agent-boundary.md` as canonical owner for browser/session/context/WebTool semantic records; no incompatible duplicate WebToolObservation exists.
- [ ] WebMCP tools and DevTools diagnostics remain distinct capability paths.
- [ ] Browser actuation, artifact transfer, clipboard/native-dialog/permission, and context-target effects are separately classified where material.
- [ ] Browser session/profile/context/frame/origin/tool-generation identity and freshness are explicit.
- [ ] Authenticated browser/cookies/SSO/password-manager/autofill/clipboard state cannot become implicit authority.
- [ ] Browser download produces inert governed artifact state before parser/RAG/execution follow-on.
- [ ] Upload uses one exact authorized InputArtifact and cannot browse/substitute arbitrary local paths.
- [ ] Popups/new tabs/frames cannot silently inherit authorization from another browser context.
- [ ] Failed WebMCP/browser routes cannot silently downgrade to another automation/browser/profile/context.
- [ ] Browser unknown-effect outcomes are reconciled before unsafe duplicate submission/retry.

## K. Trusted Completion completeness

- [ ] Defines minimum CompletionEvidence fields for accepted target, reproduction/root-cause basis, change identity, deterministic gates, exact-target independent review, security review/applicable-N/A basis, reconciliations, authority/effect/effect-reconciliation refs, provider closeout refs, residual limitations, and completion decision identity.
- [ ] Requires all acceptance-critical evidence to bind the exact accepted target/generation/policy where applicable.
- [ ] Fails closed on stale/mismatched evidence, unresolved material findings, missing required authority evidence, unknown material effect outcome, or contradictory acceptance-critical provider state.
- [ ] Keeps merge/close/green-CI/model-review/provider/Assurance state as evidence inputs, never the completion decision itself.

## L. Durable evidence evolution

- [ ] Plans evidence/event schema migration with fail-closed partial-migration behavior.
- [ ] Plans backup/restore verification sufficient to reconstruct historical target/policy/authority/evidence relations.
- [ ] Plans redaction/tombstone/access-policy propagation through historical projections without erasing required non-sensitive audit identity.
- [ ] Plans bounded evidence growth/retention without silently deleting provenance required for historical decisions.

## M. Source-acquisition completeness

- [ ] Records `mattpocock/skills@6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` as research-only candidate.
- [ ] Records `amElnagdy/delegate-skills@b781ee2e23089630e2fbee1cfd6174afe4edeb76` as research-only candidate.
- [ ] Records OpenHands mechanism extraction as research/source-acquisition input only with clean-room WePLD-native adaptation preferred.
- [ ] Records observed licenses without treating licensing as admission.
- [ ] Requires a separately governed future source-registry revision before reuse/import where canonical registry policy requires it.
- [ ] Requires per-capability minimum reuse decisions rather than wholesale copying.

## N. Planning review gate

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

The internal professional review in `reviews/professional-whole-plan-review-2026-09-02.md` is repair input and MUST NOT be counted as the independent acceptance review.

A review that explicitly samples only part of the requested whole-repository scope or whose finding table/counts are internally inconsistent may provide useful review evidence, but it does not satisfy the final qualified review gate until a fresh exact-head review closes those coverage/accounting gaps.

Even after merge, future implementation remains separately gated by the owning slices.
