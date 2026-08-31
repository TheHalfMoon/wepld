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

## S4 — Fehrest/RAG minimum

Depends on S4 Fehrest activation and S3 artifact identity where applicable.

- [ ] `006-S4-R001` Specify `KnowledgeCollection` identity/scope/generation contract.
- [ ] `006-S4-R002` Specify source membership and freshness model.
- [ ] `006-S4-R003` Implement exact/path/key retrieval baseline.
- [ ] `006-S4-R004` Implement lexical/full-text retrieval baseline after Source Acquisition.
- [ ] `006-S4-R005` Integrate Fehrest syntax/symbol/reference facts as retrieval signals.
- [ ] `006-S4-R006` Specify `RetrievalEvidence` provenance contract.
- [ ] `006-S4-R007` Add result citations/locations for supported source classes.
- [ ] `006-S4-R008` Add stale/missing/conflicting source-state handling.
- [ ] `006-S4-R009` Add collection scopes: session, project, workspace, global.
- [ ] `006-S4-R010` Add `/rag create|use|add|list|inspect|refresh|remove|clear|ask` contracts.
- [ ] `006-S4-R011` Implement bounded context-pack construction from retrieval evidence.
- [ ] `006-S4-R012` Build retrieval quality corpus and citation/provenance tests.
- [ ] `006-S4-R013` Evaluate whether semantic/vector retrieval materially improves qualified benchmarks.
- [ ] `006-S4-R014` If justified, acquire/admit semantic/vector machinery behind replaceable contracts.
- [ ] `006-S4-R015` Add reranking only if incremental evidence justifies it.

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
- [ ] `006-S5-W018` Implement internal domain-modeling/glossary primitive.
- [ ] `006-S5-W019` Implement internal context-budget/progressive-disclosure primitive.
- [ ] `006-S5-W020` Implement internal intent-preserving conflict-resolution primitive subject to Git policy.
- [ ] `006-S5-W021` Implement internal standards-vs-spec review decomposition.
- [ ] `006-S5-W022` Verify all Matt-derived behavior is WePLD-native and no donor command branding leaks into core UX.

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

## S6/S7 — Universal Case + GitHub-first IssueOps

External provider activation requires then-current network/auth/source authority.

- [ ] `006-I001` Specify stable `Case` identity and lifecycle.
- [ ] `006-I002` Specify `ProviderBinding` contract and provider-state preservation.
- [ ] `006-I003` Specify typed Case relations and evidence/confidence semantics.
- [ ] `006-I004` Specify `DecisionBoundary` contract.
- [ ] `006-I005` Build local synthetic Case fixtures before network access.
- [ ] `006-I006` Qualify GitHub provider API/auth/event source route.
- [ ] `006-I007` Implement GitHub read-only issue import.
- [ ] `006-I008` Implement GitHub PR/check/review linkage observations.
- [ ] `006-I009` Implement Case timeline normalization without overwriting raw provider evidence.
- [ ] `006-I010` Implement read-only `/issues` and `/issues inbox`.
- [ ] `006-I011` Implement `/issues sweep` recommendation-only mode.
- [ ] `006-I012` Implement exact/probable duplicate relation candidates.
- [ ] `006-I013` Implement common-root-cause clustering candidates.
- [ ] `006-I014` Implement already-fixed-on-main candidate detection.
- [ ] `006-I015` Implement blocker/decision/security classification.
- [ ] `006-I016` Implement Case room read model.
- [ ] `006-I017` Add provider freshness/version preconditions for all future writes.
- [ ] `006-I018` Add webhook/poll duplicate-delivery/idempotency tests before writes.

## S7 — Assurance for IssueOps

- [ ] `006-S7-A001` Define triage/reproduction/root-cause evidence quality gates.
- [ ] `006-S7-A002` Normalize independent review findings into Case evidence.
- [ ] `006-S7-A003` Preserve valid findings until reconciled.
- [ ] `006-S7-A004` Add security-sensitive Case classification and specialist-review routing.
- [ ] `006-S7-A005` Prevent implementer self-review from satisfying independent-review requirements.
- [ ] `006-S7-A006` Add stale-exact-head invalidation for PR review/acceptance evidence.
- [ ] `006-S7-A007` Define provider-closeout readiness evidence separately from Trusted Completion.

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

## S9 — Evidence / recovery / quality passport

- [ ] `006-S9-E001` Link Case -> assignment -> attempt -> effects -> change -> tests -> reviews -> closeout.
- [ ] `006-S9-E002` Add replay/recovery for interrupted case workflows.
- [ ] `006-S9-E003` Add audit export and completion evidence packet.
- [ ] `006-S9-E004` Add longitudinal regression/reopen linkage.
- [ ] `006-S9-E005` Add Build Learning capture from successful and failed Cases.

## S10 — Organization-scale issue intelligence

- [ ] `006-S10-O001` Add multi-repository Case federation.
- [ ] `006-S10-O002` Add cross-provider Case federation.
- [ ] `006-S10-O003` Add backlog/root-cause/duplicate analytics.
- [ ] `006-S10-O004` Add recurring autonomous sweep scheduling under explicit policy.
- [ ] `006-S10-O005` Add throughput/quality/reopen/decision-boundary analytics.
- [ ] `006-S10-O006` Add resource/cost-aware multi-worker scheduling.
- [ ] `006-S10-O007` Evaluate additional issue providers by actual demand, one adapter at a time.

## Mandatory dependency frontier

```text
S3 InputArtifact
  -> S4 provenance-first retrieval
  -> S5 workflow/context packaging
  -> S6 worker/delegation + provider adapter foundation
  -> S7 assurance
  -> S8 autonomous repair/landing
  -> S9 evidence/recovery
  -> S10 organization-scale automation
```

GitHub read-only Case import may be developed only when its source/network/auth route is independently authorized; GitHub write effects MUST NOT be used to shortcut the dependency frontier.
