# Professional Plan Hardening Task Map

```text
STATUS = FUTURE_TASK_MAP_ONLY
SOURCE_REVIEW = reviews/professional-whole-plan-review-2026-09-02.md
CURRENT_ACTIVE_SLICE = S2
ALL_TASKS_ACTIVE = NO
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
```

This task map binds the material findings from the 2026-09-02 whole-plan professional review to the existing S3-S9 roadmap. It does not create a new roadmap or authority path.

## Contract convergence — before any owning implementation tranche

- [ ] `006-HARD-C001` Add a future machine-readable schema/contract consistency gate for shared records so `ProviderObservation`, `ProviderConflict`, `ContextPackage`, `WorkerRequirement`, `WorkerDescriptor`, `EffectProposal`, and `WebToolObservation` cannot drift across documents/implementations.
- [ ] `006-HARD-C002` Treat `data-model.md` as the canonical field vocabulary for shared domain records unless a dedicated contract explicitly owns the type.
- [ ] `006-HARD-C003` Treat `contracts/web-agent-boundary.md` as canonical owner for WebMCP/browser semantic records and prohibit secondary incompatible redeclarations.
- [ ] `006-HARD-C004` Version shared capability/effect/trust/outcome vocabularies before multiple adapters depend on them.

## S3 — runtime/effect recovery and engine containment

- [ ] `006-HARD-S3-001` Implement durable `EFFECT_OUTCOME_UNKNOWN` semantics and `EffectReconciliation` before retrying any externally observable non-idempotent effect after interruption.
- [ ] `006-HARD-S3-002` Prove local timeout/disconnect/crash does not imply remote effect was not applied.
- [ ] `006-HARD-S3-003` Add process-tree termination/orphan detection and classify cancellation acknowledgement separately from termination proof.
- [ ] `006-HARD-S3-004` Define reusable resource envelopes for local engines/workers: CPU, memory, process count, handles/FDs, output, temporary disk, wall clock, concurrency slot, cleanup, inherited environment, credential exposure.
- [ ] `006-HARD-S3-005` Bind acceptance-critical engine runs to resolved executable/runtime/artifact identity and digest where available; PATH/version-string match alone is not sufficient.
- [ ] `006-HARD-S3-006` Prove temporary artifacts and process descendants are either cleaned/reaped or leave explicit incomplete-cleanup evidence.

## S4 — RAG/source authorization and generation correctness

- [ ] `006-HARD-S4-001` Define source/collection/access-policy propagation through chunks, indexes, embeddings, graph projections, RetrievalEvidence, ContextPackage, and worker egress.
- [ ] `006-HARD-S4-002` Prove permission revocation or visibility narrowing invalidates derived context eligibility even when cached content identity is unchanged.
- [ ] `006-HARD-S4-003` Implement immutable complete source generations and atomic current-generation publication; prohibit mixed-generation retrieval as one current view.
- [ ] `006-HARD-S4-004` Give every derived chunk/projection stable source-generation provenance and current access-policy reference.
- [ ] `006-HARD-S4-005` Implement tombstone/redaction/retention propagation so deleted or no-longer-authorized source content is not exposed through stale indexes.
- [ ] `006-HARD-S4-006` Qualify remote URL ingestion only with explicit SSRF/redirect/DNS-rebinding/private-address/metadata-service/credential-forwarding controls and exact network authority.
- [ ] `006-HARD-S4-007` Prove cross-collection/project/workspace isolation under adversarial source references and stale caches.

## S5 — assurance claim/policy planning

- [ ] `006-HARD-S5-001` Implement immutable `AssurancePolicySnapshot` and versioned profile semantics before acceptance/release claim evaluation.
- [ ] `006-HARD-S5-002` Classify every Assurance check as `REQUIRED`, `CONDITIONAL`, or `OPTIONAL` for the exact requested claim.
- [ ] `006-HARD-S5-003` Make `BUDGET_EXCEEDED`, `NOT_AVAILABLE`, `NOT_AUTHORIZED`, or `UNSUPPORTED` on a required check produce an unsatisfied/blocked/inconclusive claim rather than silent downgrade.
- [ ] `006-HARD-S5-004` Define deterministic configuration precedence and fail on undefined conflicts rather than latest-write-wins.
- [ ] `006-HARD-S5-005` Prove stronger profiles/claims cannot silently require less evidence for the same risk class without an explicit compatibility/substitution proof.

## S6 — provider/worker completeness and recovery

- [ ] `006-HARD-S6-001` Normalize provider observation completeness and authenticity; partial/unauthenticated provider data cannot masquerade as complete current state.
- [ ] `006-HARD-S6-002` Add provider rate-limit/backoff/circuit-breaker states and prove stale cache is never silently reported fresh.
- [ ] `006-HARD-S6-003` Qualify webhook/event authenticity and duplicate-delivery identities before provider-triggered workflows.
- [ ] `006-HARD-S6-004` Version the WePLD worker capability vocabulary and fail closed on unknown capability semantics.
- [ ] `006-HARD-S6-005` Qualify adapter cancellation/recovery/session-resume semantics and orphan behavior before resumable Mission Runtime claims.
- [ ] `006-HARD-S6-006` Ensure access-policy revocation stales any prebuilt ContextPackage before worker/provider egress.

## S7 — Assurance claim, finding, evidence, and benchmark hardening

- [ ] `006-HARD-S7-001` Implement typed `ClaimAssessment` outcomes: `SUPPORTED`, `NOT_SUPPORTED`, `PARTIALLY_SUPPORTED`, `INCONCLUSIVE`, `BLOCKED`, `STALE`.
- [ ] `006-HARD-S7-002` Prove missing/stale required evidence, unresolved blocking findings, or material unresolved conflicts cannot produce `SUPPORTED`.
- [ ] `006-HARD-S7-003` Implement stable evidence-backed finding fingerprints and typed correlation relations without erasing producer-specific records.
- [ ] `006-HARD-S7-004` Implement governed `FindingDisposition` for false positive/accepted risk/suppression/rule exception/fixed/superseded with scope, authority, target/policy, evidence, and expiry/review date.
- [ ] `006-HARD-S7-005` Prove source-branch/untrusted config cannot forge or extend accepted-risk/suppression state.
- [ ] `006-HARD-S7-006` Implement `EvidenceHandlingPolicy` for visibility, storage/encryption requirement, redaction, retention/tombstone, export/egress, and safe rendering.
- [ ] `006-HARD-S7-007` Add evidence-handling adversarial fixtures for secrets, private source excerpts, network traces, browser screenshots, terminal escapes, malformed SARIF/JUnit/SBOM, and redacted history.
- [ ] `006-HARD-S7-008` Represent independent-review file/context coverage as typed coverage evidence.
- [ ] `006-HARD-S7-009` Implement known-flake/quarantine records with owner, evidence, scope, expiry/review date, and follow-up; quarantine cannot erase failure evidence.
- [ ] `006-HARD-S7-010` Implement qualified `PerformanceEvidence` with baseline, environment, warmup/repetitions, sample/noise summary, threshold, and explicit inconclusive states.
- [ ] `006-HARD-S7-011` Add dirty-workspace target fixtures covering untracked/ignored/nested/submodule/generated material so workspace assurance does not overclaim commit-only coverage.

## S7/S8 — browser artifact and effect boundaries

- [ ] `006-HARD-WEB-001` Route browser uploads/downloads through explicit `InputArtifact`/artifact-transfer identity and access/handling policy rather than ambient filesystem paths.
- [ ] `006-HARD-WEB-002` Add separate browser effect classes for clipboard read/write, permission prompts, native file chooser, popup/new-tab/frame target creation, and download acceptance where applicable.
- [ ] `006-HARD-WEB-003` Preserve browser target/frame/opener/session/origin identities across multi-context navigation and fail closed on ambiguous target selection.
- [ ] `006-HARD-WEB-004` Quarantine or explicitly classify downloaded artifacts before any parser/execution follow-on action.
- [ ] `006-HARD-WEB-005` Prove an authenticated browser/profile/password-manager/autofill/clipboard state cannot expand artifact visibility or action authority.

## S9 — durable evidence evolution and recovery

- [ ] `006-HARD-S9-001` Qualify evidence/event schema migration with pre/post identities and rollback/fail-closed behavior.
- [ ] `006-HARD-S9-002` Add backup/restore verification sufficient to reconstruct the exact target/policy/evidence graph supporting historical completion/assurance decisions.
- [ ] `006-HARD-S9-003` Propagate redaction/tombstone/access-policy changes through historical projections while preserving non-sensitive audit identity.
- [ ] `006-HARD-S9-004` Bound evidence growth without deleting acceptance-critical provenance required to explain a historical decision.

## S10 — scale deferral, not current blocker

- [ ] `006-HARD-S10-001` Before multi-case autonomous scheduling, define per-project/provider resource quotas, fairness/starvation policy, priority semantics, and concurrency conflict domains.

## Contract-level negative oracles

```text
MISSING_REQUIRED_ASSURANCE_EVIDENCE_CANNOT_PRODUCE_SUPPORTED
BUDGET_LIMIT_CANNOT_SILENTLY_WEAKEN_RELEASE_CLAIM
POLICY_VERSION_CHANGE_DOES_NOT_REINTERPRET_HISTORICAL_BUNDLE
PATH_VERSION_MATCH_DOES_NOT_PROVE_ENGINE_BINARY_IDENTITY
ACCEPTED_RISK_WITHOUT_AUTHORITY_OR_EXPIRY_IS_INVALID
EVIDENCE_SECRET_DOES_NOT_BECOME_DURABLE_UNREDACTED_LOG_BY_DEFAULT
SOURCE_ACCESS_REVOCATION_PROPAGATES_TO_DERIVED_RETRIEVAL_AND_CONTEXT
MIXED_SOURCE_GENERATIONS_CANNOT_MASQUERADE_AS_ONE_CURRENT_REFRESH
REMOTE_URL_SOURCE_CANNOT_REACH_UNAUTHORIZED_PRIVATE_TARGET
PARTIAL_PROVIDER_PAGINATION_CANNOT_MASQUERADE_AS_COMPLETE_STATE
UNAUTHENTICATED_WEBHOOK_CANNOT_DRIVE_TRUSTED_PROVIDER_STATE
UNKNOWN_EFFECT_OUTCOME_BLOCKS_UNSAFE_RETRY
BROWSER_DOWNLOAD_DOES_NOT_BECOME_EXECUTABLE_INPUT
DIRTY_WORKSPACE_CANNOT_BE_CLAIMED_COVERED_BY_COMMIT_SHA_ALONE
```

## Completion relationship

This hardening map is complete as planning when every task has an owning canonical slice and the contracts/specs make its semantics explicit. Actual completion requires future implementation, deterministic evidence, exact-head review, and the normal canonical acceptance path.
