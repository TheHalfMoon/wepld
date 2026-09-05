# Tasks — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_TASK_MAP_ONLY
CURRENT_ACTIVE_SLICE = S2
ALL_TASKS_ACTIVE = NO
IMPLEMENTATION_AUTHORITY = NONE
```

These tasks are a dependency map for future activation. They MUST NOT be executed merely because they appear here. Each group requires activation by its owning slice and the canonical build method.

## P — Planning / governance preparation

- [ ] `006-P001` Revalidate canonical main and roadmap before activation.
- [ ] `006-P002` Run full Spec Kit clarification again against then-current product state.
- [ ] `006-P003` Re-run Ponytail FULL for the exact first implementation tranche.
- [ ] `006-P004` Create separately governed source-registry revision candidate for newly needed sources.
- [ ] `006-P005` Qualify `mattpocock/skills` at the exact pinned/updated revision needed by the owning tranche.
- [ ] `006-P006` Qualify `amElnagdy/delegate-skills` at the exact pinned/updated revision needed by the owning tranche.
- [ ] `006-P007` Identify already-admitted machinery that supersedes any donor behavior before reuse.
- [ ] `006-P008` Define benchmark/negative-oracle corpus for autonomous IssueOps before enabling writes.
- [ ] `006-P009` Define privacy/content-classification policy for user-provided RAG/artifacts before external egress.
- [ ] `006-P010` Define measurable promotion criteria between autonomy ceilings.
- [ ] `006-P011` Define adversarial untrusted-content/prompt-injection corpus covering issues, PRs, logs, RAG sources, repository text, worker/model output, fake policy/review text, credential requests, encoded instructions, and cross-source conflicts.
- [ ] `006-P012` Define predeclared backlog-sweep quality thresholds per output class (precision/recall/abstention/evidence coverage) before benchmark execution; provider mutation thresholds remain separately governed.
- [ ] `006-P013` Define exact TB0 offline/read-only IssueOps fixture set and completion evidence packet before implementation.

## S3 — InputArtifact / terminal intake foundation

Depends on the S3 authority chain.

- [ ] `006-S3-I001` Specify `InputArtifact` contract and stable identity semantics.
- [ ] `006-S3-I002` Specify source kinds: path, directory, text, clipboard, URL, provider attachment, repository reference.
- [ ] `006-S3-I003` Specify inert-intake rule and forbidden implicit effects.
- [ ] `006-S3-I004` Implement CLI quoted/escaped path-paste recognition behind exact tests.
- [ ] `006-S3-I005` Implement bracketed-paste-aware intake where supported.
- [ ] `006-S3-I006` Implement Desktop/native drop adapter to the same contract.
- [ ] `006-S3-I007` Add multi-artifact intake and deterministic ordering.
- [ ] `006-S3-I008` Add size/type/symlink/path-boundary validation without parsing/execution side effects.
- [ ] `006-S3-I009` Add explicit follow-on intents: inspect, compare, attach, open project, add-to-RAG.
- [ ] `006-S3-I010` Add negative tests proving drop/paste cannot execute, fetch, install, mutate, or egress.
- [ ] `006-S3-I011` Persist intake evidence in the local evidence foundation.
- [ ] `006-S3-I012` Qualify platform behavior on Windows-first plus Linux/macOS compatibility targets.
- [ ] `006-S3-I013` Add trust/origin classification to every InputArtifact/context candidate without promoting content to instruction authority.
- [ ] `006-S3-I014` Add parser/active-content negative oracles for archives/documents/repositories/links appropriate to admitted source kinds.

## S3/S4 — intake-to-RAG integration checkpoint

No Agent Host, model/provider execution, or network is required.

- [ ] `006-S34-C001` Ingest one qualified local file/directory InputArtifact into a named local KnowledgeCollection.
- [ ] `006-S34-C002` Produce exact/lexical cited RetrievalEvidence from that artifact generation.
- [ ] `006-S34-C003` Prove stale source generation is surfaced after source change.
- [ ] `006-S34-C004` Prove embedded instruction text remains data and creates no WorkflowIntent/effect.
- [ ] `006-S34-C005` Record one replayable checkpoint showing `InputArtifact -> KnowledgeSource -> RetrievalEvidence` with zero network/provider/process effects.

## S4 — Fehrest/RAG minimum

Depends on S4 Fehrest activation and S3 artifact identity where applicable.

- [ ] `006-S4-R001` Specify `KnowledgeCollection` identity/scope/generation contract.
- [ ] `006-S4-R002` Specify source membership and freshness model.
- [ ] `006-S4-R003` Implement exact/path/key retrieval baseline.
- [ ] `006-S4-R004` Implement lexical/full-text retrieval baseline after Source Acquisition.
- [ ] `006-S4-R005` Integrate Fehrest syntax/symbol/reference facts as retrieval signals with exact fact identity/provenance.
- [ ] `006-S4-R006` Specify `RetrievalEvidence` provenance contract.
- [ ] `006-S4-R007` Add result citations/locations for supported source classes.
- [ ] `006-S4-R008` Add stale/missing/conflicting source-state handling.
- [ ] `006-S4-R009` Add collection scopes: session, project, workspace, global.
- [ ] `006-S4-R010` Add `/rag create|use|add|list|inspect|refresh|remove|clear|ask` contracts; `add --text` remains syntax sugar over inline InputArtifact ingestion.
- [ ] `006-S4-R011` Implement bounded context-pack construction from retrieval evidence with per-item trust/origin labels.
- [ ] `006-S4-R012` Build retrieval quality corpus and citation/provenance tests including natural-language, symbol/reference, stale, cross-source, and no-answer cases.
- [ ] `006-S4-R013` Evaluate whether semantic/vector retrieval materially improves predeclared qualified benchmarks for identified conceptual/paraphrastic query classes.
- [ ] `006-S4-R014` If justified, acquire/admit semantic/vector machinery behind replaceable contracts.
- [ ] `006-S4-R015` Add reranking only if incremental evidence justifies it.
- [ ] `006-S4-R016` Report incremental contribution of semantic/vector signals separately from exact/lexical/Fehrest signals; no post-hoc promotion threshold.
- [ ] `006-S4-R017` Add indirect prompt-injection corpus proving retrieved instructions cannot create WorkflowIntent, broaden context visibility, select remote/paid routes, or create effects.
- [ ] `006-S4-R018` Prove semantic/vector similarity cannot override contradictory exact source/graph evidence without surfacing the conflict.

## S5 — Workflow / skill layer

Depends on S5 Spec Kit/AGILLE/Plan Qualification activation and S4 retrieval for context-aware flows.

- [ ] `006-S5-W001` Specify common `WorkflowIntent` envelope.
- [ ] `006-S5-W002` Implement `/askme` capability router with deterministic local fallback-to-clarification, not provider fallback.
- [ ] `006-S5-W003` Implement `/btw` context-aware re-explanation without state mutation.
- [ ] `006-S5-W004` Implement `/triage` workflow contract.
- [ ] `006-S5-W005` Implement `/grill` decision-boundary workflow.
- [ ] `006-S5-W006` Implement `/architect` domain/boundary/deep-module workflow.
- [ ] `006-S5-W007` Integrate `/spec` with canonical Spec Kit generation/qualification.
- [ ] `006-S5-W008` Implement `/tickets` tracer-bullet task/dependency frontier.
- [ ] `006-S5-W009` Implement `/debug` feedback-loop-first reproduction/diagnosis workflow.
- [ ] `006-S5-W010` Implement `/prototype` bounded throwaway experiment workflow.
- [ ] `006-S5-W011` Implement `/research` cited primary-source workflow.
- [ ] `006-S5-W012` Implement `/wayfinder` decision-map workflow.
- [ ] `006-S5-W013` Implement `/questionnaire` external-decision capture workflow.
- [ ] `006-S5-W014` Implement `/wizard` human-only setup/migration workflow.
- [ ] `006-S5-W015` Implement `/retro` build-learning/environment-improvement workflow.
- [ ] `006-S5-W016` Implement `/workflow` checkpointed recurring-workflow definition.
- [ ] `006-S5-W017` Implement internal TDD primitive.
- [ ] `006-S5-W018` Implement internal domain-modeling/glossary/scenario primitive and expose it through `/architect` workflows.
- [ ] `006-S5-W019` Implement internal context-budget/progressive-disclosure primitive.
- [ ] `006-S5-W020` Implement internal intent-preserving conflict-resolution primitive subject to Git policy.
- [ ] `006-S5-W021` Implement internal standards-vs-spec review decomposition.
- [ ] `006-S5-W022` Verify all Matt-derived behavior is WePLD-native and no donor command branding leaks into core UX.
- [ ] `006-S5-W023` Implement deep-module/boundary analysis as a reusable internal architecture primitive, not a TypeScript-specific donor feature.
- [ ] `006-S5-W024` Implement **delegation dry-run only**: build `Assignment`, `WorkerRequirement`, and `TopologyProposal` from one Case using synthetic WorkerDescriptors, with no worker/model/provider/process execution and no Nawat grant.
- [ ] `006-S5-W025` Prove untrusted issue/RAG content cannot become WorkflowIntent or alter dry-run Assignment effect requirements.

## S6 — Worker catalog / delegation / provider adapters

Depends on S6 UWC + Mirefa + Edara + Mission Runtime + Nawat activation.

- [ ] `006-S6-D001` Specify `WorkerDescriptor` contract.
- [ ] `006-S6-D002` Specify capability/effect/containment/cost metadata.
- [ ] `006-S6-D003` Specify `Assignment` and `Attempt` append-only contracts.
- [ ] `006-S6-D004` Implement `/workers` qualification/availability surface.
- [ ] `006-S6-D005` Implement `/delegate <task>` route selection through Edara/Mirefa/Nawat.
- [ ] `006-S6-D006` Implement `/delegate --to <worker>` explicit-request semantics without authority bypass.
- [ ] `006-S6-D007` Implement provider session IDs as opaque provenance only.
- [ ] `006-S6-D008` Implement cancel/recovery/retry as new durable attempt events.
- [ ] `006-S6-D009` Enforce no silent worker/provider/model fallback.
- [ ] `006-S6-D010` Enforce cost/quota policy and silent-spend negative tests.
- [ ] `006-S6-D011` Qualify first local/connected worker adapter from the future acquisition set.
- [ ] `006-S6-D012` Qualify provider read-only/full-trust semantics against actual containment behavior.
- [ ] `006-S6-D013` Implement `/handoff --to <worker>` as context/session transfer distinct from assignment.
- [ ] `006-S6-D014` Build worker adapter conformance suite from delegate-skills behavior/failure oracles.
- [ ] `006-S6-D015` Implement typed `TopologyProposal -> RouteQualification -> NawatDecision -> Mission Runtime Attempt` interfaces exactly as defined by the delegation contract.
- [ ] `006-S6-D016` Add fail-closed tests for `CAPABILITY_MISMATCH`, `QUALIFICATION_STALE`, `CONTAINMENT_EVIDENCE_INSUFFICIENT`, `COST_OR_QUOTA_BLOCKED`, Nawat `DENY`, `APPROVAL_REQUIRED`, `REQUALIFY_REQUIRED`, and `STALE_TARGET`.
- [ ] `006-S6-D017` Prove Nawat denial/requalification is visible as a Case/Assignment frontier rather than a generic worker failure.
- [ ] `006-S6-D018` Prove Mission Runtime cannot widen grants, reuse expired grants, or silently substitute worker/provider/model.
- [ ] `006-S6-D019` Prove context-package manifests preserve trust/origin labels and untrusted worker context cannot expand effect scope.

## S6/S7 — Universal Case + GitHub-first IssueOps

External provider activation requires then-current network/auth/source authority.

- [ ] `006-I001` Specify stable `Case` identity and lifecycle.
- [ ] `006-I002` Specify `ProviderBinding`, `ProviderObservation`, provider-conflict, and provider-state preservation contracts.
- [ ] `006-I003` Specify typed Case relations and evidence/confidence semantics.
- [ ] `006-I004` Specify `DecisionBoundary` contract.
- [ ] `006-I005` Build local synthetic Case fixtures before network access.
- [ ] `006-I006` Qualify GitHub provider API/auth/event source route.
- [ ] `006-I007` Implement GitHub read-only issue import.
- [ ] `006-I008` Implement GitHub PR/check/review linkage observations.
- [ ] `006-I009` Implement Case timeline normalization without overwriting raw provider evidence.
- [ ] `006-I010` Implement read-only `/issues` and `/issues inbox`.
- [ ] `006-I011` Implement `/issues sweep` recommendation-only mode.
- [ ] `006-I012` Implement exact duplicate derivation from explicit/exact causal evidence and probable duplicate multi-signal candidates; title/semantic similarity alone cannot create exact duplicate identity.
- [ ] `006-I013` Implement common-root-cause candidates requiring deterministic reproduction/error/test/change/causal-symbol evidence stronger than topic similarity.
- [ ] `006-I014` Implement already-fixed-on-main candidate detection requiring current-main observation plus reproduction/regression/change evidence; closed provider state alone is insufficient.
- [ ] `006-I015` Implement reproduction-missing, decision-blocked, dependency-blocked, security-sensitive, small/high-confidence, and high-risk classifications with explicit evidence requirements.
- [ ] `006-I016` Implement Case room read model including stale/conflicted provider evidence.
- [ ] `006-I017` Add provider freshness/version/conflict preconditions for all future writes.
- [ ] `006-I018` Add webhook/poll duplicate-delivery/idempotency tests before writes.
- [ ] `006-I019` Build labeled sweep corpus containing true/false duplicates, same/different root causes, fixed/not-fixed, blocked/not-blocked, security-sensitive/non-sensitive, stale/conflicted, and adversarially similar Cases.
- [ ] `006-I020` Report per-sweep-output TP/FP/FN/abstention/evidence coverage and enforce predeclared recommendation promotion thresholds.
- [ ] `006-I021` Add negative oracles: probable duplicate never auto-closes, semantic topic cluster never becomes causal group without causal evidence, stale main never proves fixed, and missing evidence returns unknown/abstain.
- [ ] `006-I022` Specify provider/Case schema evolution so provider-specific fields remain adapter extensions until provider-independent semantics justify core promotion.
- [ ] `006-I023` Prove new adapter normalization versions preserve old raw observations, conflicts, relation confidence, and replayability.
- [ ] `006-I024` Deliver TB0 offline/read-only IssueOps proof from synthetic issue artifact through Case + local retrieval + triage + evidence-backed Case room, with zero network/provider/model/Git-write effects.
- [ ] `006-I025` After route authority exists, deliver TB1 live GitHub read-only import through the same pipeline with zero provider writes.

## S7 — Assurance for IssueOps

- [ ] `006-S7-A001` Define triage/reproduction/root-cause evidence quality gates.
- [ ] `006-S7-A002` Normalize independent review findings into Case evidence.
- [ ] `006-S7-A003` Preserve valid findings until reconciled.
- [ ] `006-S7-A004` Add security-sensitive Case classification and specialist-review routing.
- [ ] `006-S7-A005` Prevent implementer self-review from satisfying independent-review requirements.
- [ ] `006-S7-A006` Add stale-exact-head invalidation for PR review/acceptance evidence.
- [ ] `006-S7-A007` Define provider-closeout readiness evidence separately from Trusted Completion.
- [ ] `006-S7-A008` Qualify malicious issue/PR/RAG/repository content against the untrusted-content contract before effect-capable IssueOps.
- [ ] `006-S7-A009` Prove successful prompt-level manipulation of a worker still cannot bypass effect-time authorization/containment/review boundaries.
- [ ] `006-S7-A010` Preserve S7 independent-review production separately from S8 repair/completion consumption; tight loop does not collapse `ReviewOutcome != CompletionDecision`.

## S8 — Controlled autonomous execution / landing

Requires S8 authority and successful lower-ceiling qualification.

- [ ] `006-S8-X001` Implement autonomy profile ceilings: observe, triage, prepare, execute, land.
- [ ] `006-S8-X002` Implement `prepare` path for draft/comment/change preparation without landing.
- [ ] `006-S8-X003` Implement bounded `/build` assignment graph for one Case.
- [ ] `006-S8-X004` Implement deterministic test/check execution evidence.
- [ ] `006-S8-X005` Implement independent review and finding reconciliation loop.
- [ ] `006-S8-X006` Implement bounded repair/retry/reassignment.
- [ ] `006-S8-X007` Implement dynamic minimum-sufficient team assembly.
- [ ] `006-S8-X008` Implement GitHub comment/label/assignee effects one class at a time.
- [ ] `006-S8-X009` Implement PR create/update with exact target/version evidence.
- [ ] `006-S8-X010` Implement expected-head guarded merge effect.
- [ ] `006-S8-X011` Implement issue close/reopen effect separately from merge.
- [ ] `006-S8-X012` Implement completion review after provider landing/closeout.
- [ ] `006-S8-X013` Record Trusted Completion only when all governing evidence is satisfied.
- [ ] `006-S8-X014` Prove merge/close do not automatically produce Trusted Completion.
- [ ] `006-S8-X015` Qualify one controlled end-to-end Case before enabling autonomous sweeps with writes.
- [ ] `006-S8-X016` Define and validate the minimum `CompletionEvidence` packet: accepted target, reproduction/root-cause basis, deterministic gates, exact-target independent review, security review/applicable-N/A basis, reconciliations, effect/authority refs, provider closeout refs, residual limitations, and completion decision identity.
- [ ] `006-S8-X017` Fail completion review on stale/mismatched target evidence, unresolved material findings, missing required authority evidence, or contradictory acceptance-critical state.

## S9 — Evidence / recovery / quality passport

- [ ] `006-S9-E001` Link Case -> assignment -> attempt -> effects -> change -> tests -> reviews -> closeout.
- [ ] `006-S9-E002` Add replay/recovery for interrupted case workflows.
- [ ] `006-S9-E003` Add audit export and completion evidence packet.
- [ ] `006-S9-E004` Add longitudinal regression/reopen linkage.
- [ ] `006-S9-E005` Add Build Learning capture from successful and failed Cases.
- [ ] `006-S9-E006` Bound evidence growth with content-addressed deduplication/projection/retention rules while preserving acceptance-critical provenance.

## S10 — Organization-scale issue intelligence

- [ ] `006-S10-O001` Add multi-repository Case federation.
- [ ] `006-S10-O002` Add cross-provider Case federation with explicit conflict preservation.
- [ ] `006-S10-O003` Add backlog/root-cause/duplicate analytics using the qualified per-output evidence contracts.
- [ ] `006-S10-O004` Add recurring autonomous sweep scheduling under explicit policy.
- [ ] `006-S10-O005` Add throughput/quality/reopen/decision-boundary analytics.
- [ ] `006-S10-O006` Add resource/cost-aware multi-worker scheduling.
- [ ] `006-S10-O007` Evaluate additional issue providers by actual demand, one adapter at a time.

## Mandatory dependency frontier

```text
S3 InputArtifact
  -> S3/S4 local intake-to-cited-RAG checkpoint
  -> S4 provenance-first retrieval
  -> S5 workflow/context packaging + delegation dry-run
  -> S6 worker/delegation + provider adapter foundation
  -> S7 independent assurance
  -> S8 autonomous repair/landing + Trusted Completion
  -> S9 evidence/recovery
  -> S10 organization-scale automation
```

GitHub read-only Case import may be developed only when its source/network/auth route is independently authorized; GitHub write effects MUST NOT be used to shortcut the dependency frontier.
