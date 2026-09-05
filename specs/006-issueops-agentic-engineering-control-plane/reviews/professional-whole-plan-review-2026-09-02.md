# Professional Whole-Plan Review — 2026-09-02

```text
REVIEW_CLASS = INTERNAL_ARCHITECTURE_PRODUCT_EXECUTION_REVIEW
REVIEWED_PR = 241
REVIEWED_PRE_REPAIR_HEAD = e1f7042a2010d66beae8a93005bf723ef96456f3
TRUSTED_CANONICAL_BASE_RECONSTITUTION = 8657b81e19241ce61b8e45b61ed5086b0a49e918
CURRENT_ACTIVE_SLICE = S2
INDEPENDENT_REVIEW_GATE_SATISFIED_BY_THIS_REVIEW = NO
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
```

## Review objective

Review the complete Spec 006 planning package as a production-grade architecture/product/execution plan, not as prose. The review covers:

- canonical V2.3 placement and ownership;
- authority and trust boundaries;
- domain-model consistency;
- IssueOps provider semantics;
- RAG/source access and freshness;
- worker/runtime/delegation contracts;
- browser/WebMCP boundaries;
- Native Assurance `/review`, `/security`, `/fulltest`;
- evidence, privacy, recovery, idempotency, and durability;
- IDE/CLI product semantics;
- source acquisition and OpenHands-derived mechanisms;
- performance/benchmark semantics;
- dependency ordering and tracer-bullet executability.

This review is authored as part of the planning repair and therefore **does not** satisfy the independently qualified exact-head review required before planning acceptance.

## Overall assessment

```text
ARCHITECTURE_DIRECTION = STRONG
AUTHORITY_MODEL = STRONG
SECURITY_POSTURE = STRONG_BUT_NEEDS_EVIDENCE_HANDLING_AND_RECOVERY_CLOSURE
PRODUCT_DIFFERENTIATION = STRONG
TRACER_BULLET_STRATEGY = STRONG
IMPLEMENTATION_READINESS_PRE_REPAIR = NOT_YET
PRIMARY_DEFECT_CLASS = CROSS_ARTIFACT_CONTRACT_DRIFT + MISSING_CLAIM/RECOVERY/ACCESS_SEMANTICS
```

The plan should be repaired, not redesigned. Its strongest property is the explicit separation of qualification, authority, execution, evidence, review, repair, and Trusted Completion. The remaining gaps are mostly where a future implementation could otherwise make two plausible but incompatible choices.

## Material findings

### PLAN-CONTRACT-001 — HIGH — cross-artifact canonical schema divergence

Current planning artifacts define incompatible shapes/names for `ProviderObservation`, `ProviderConflict`, `ContextPackage`, `WorkerDescriptor`, `EffectProposal`, and `WebToolObservation`; `WorkerRequirement` is referenced but undefined.

Risk: adapters/serializers/runtime components could independently implement different meanings for the same domain entity, making replay, qualification, and authority checks ambiguous.

Required repair:

1. make `data-model.md` canonical for shared domain records unless a dedicated contract explicitly owns the type;
2. make dedicated contracts reference, not redeclare, the canonical shape;
3. define `WorkerRequirement` once;
4. add typed effect controlling-origin fields.

### ASSURANCE-CLAIM-001 — HIGH — no typed claim assessment/verdict contract

`AssuranceIntent`, `AssurancePlan`, and `AssuranceBundle` carry `requested_claim`, but the fabric lacks a typed assessment that says whether that exact claim is supported.

Risk: the product can become an excellent evidence dashboard without an auditable answer to the user's assurance question.

Required repair: add `ClaimAssessment` with at least:

```text
SUPPORTED
NOT_SUPPORTED
PARTIALLY_SUPPORTED
INCONCLUSIVE
BLOCKED
STALE
```

and bind it to required evidence, satisfied evidence, missing evidence, conflicts, coverage gaps, policy snapshot, target, and rationale.

### ASSURANCE-POLICY-001 — HIGH — assurance policy/profile identity is not frozen with claim evaluation

Rule-pack identity exists, but the complete policy defining what `RELEASE`, `DEEP`, or another claim requires is not a first-class immutable record.

Risk: identical target evidence could be interpreted differently after profile/policy evolution while appearing to support the same historical claim.

Required repair: introduce `AssurancePolicySnapshot` / stable profile-policy identity and bind plans/claim assessments/bundles to it.

### EFFECT-RECOVERY-001 — HIGH — unknown external-effect outcome after interruption is not first-class

Provider writes are idempotency-aware, but the general runtime model lacks a durable state for: request may have reached an external system, local process crashed before result was recorded, effect outcome is unknown.

Risk: blind retry can duplicate comments, submissions, merges, browser actions, or other non-idempotent effects.

Required repair:

```text
EFFECT_OUTCOME_UNKNOWN
-> reconcile exact external target/idempotency key/postcondition
-> CONFIRMED_APPLIED | CONFIRMED_NOT_APPLIED | STILL_UNKNOWN
-> retry only when policy permits
```

### RAG-AUTH-001 — HIGH — source access/visibility revocation is not propagated through derived retrieval artifacts

Collections have scope and context packages have trust/visibility labels, but the plan does not define authorization inheritance/revocation from source -> chunk/index -> RetrievalEvidence -> ContextPackage -> worker egress.

Risk: removed permissions or collection membership can leave previously derived searchable content visible to a later worker.

Required repair: access-policy identity and visibility scope must propagate to every derived projection; revocation invalidates or quarantines affected indexes/evidence/context eligibility.

### EVIDENCE-HANDLING-001 — HIGH — general evidence privacy/retention/access policy is under-specified

The plan may persist source excerpts, logs, SARIF, network traces, screenshots, test output, SBOMs, review content, and possibly secret-bearing findings. Dynamic-security sections mention PII/secret handling, but the common Evidence contract lacks classification, redaction, retention, visibility, encryption/storage-policy, and export controls.

Risk: the Assurance/Evidence Timeline becomes a durable secondary data leak.

Required repair: add an `EvidenceHandlingPolicyRef` or equivalent typed fields to durable evidence and define minimum handling semantics before evidence persistence/export.

### FULLTEST-CLAIM-001 — HIGH — required-vs-optional checks and budget failure semantics are incomplete

`AssurancePlan` records omitted checks and allows `BUDGET_EXCEEDED`, but it does not explicitly distinguish checks required to establish the claim from optional enrichment.

Risk: a release claim could silently become weaker because a required expensive check was omitted for budget while the UI still appears broadly green.

Required repair:

```text
CHECK_REQUIREMENT = REQUIRED | CONDITIONAL | OPTIONAL
REQUIRED_CHECK_OMITTED -> CLAIM BLOCKED/INCONCLUSIVE
BUDGET_EXCEEDED != PERMISSION_TO_DOWNGRADE_REQUIRED_EVIDENCE
```

Also define monotonic profile semantics: a stronger claim may reuse compatible evidence but cannot silently require less assurance than a weaker profile for the same risk class.

### PROVIDER-OBS-001 — MEDIUM — provider observation completeness/authenticity/backpressure semantics are incomplete

Provider adapters cover freshness, idempotency, duplicate delivery, and conflicts but do not yet specify:

- webhook/event authenticity evidence;
- pagination/completeness and partial-observation state;
- rate-limit/backoff/circuit-breaker state;
- edited/deleted/redacted provider-content history semantics.

Risk: partial or unauthenticated provider data may be interpreted as complete current state.

### RAG-GEN-001 — MEDIUM — retrieval refresh publication and derived projection identity are incomplete

The plan has source/index generations but does not explicitly require atomic publication of a complete refresh, chunk/projection identity, tombstones, or purge behavior.

Risk: a query can join old and new source fragments or retain deleted material after refresh.

Required repair: immutable source generation + derived projection generation + atomic current-generation publication + explicit tombstone/revocation handling.

### RAG-NET-001 — MEDIUM — remote URL ingestion security boundary is incomplete

URL/documentation sources are planned, but future network qualification does not explicitly enumerate SSRF/redirect/DNS-rebinding/private-address/credential-forwarding defenses.

Risk: `/rag add <url>` can become a network pivot or credential leak when network authority eventually exists.

### ASSURANCE-ENGINE-001 — MEDIUM — engine identity/resource containment is not sufficiently exact

`EngineDescriptor` and `EngineRun` include version/invocation/environment, but acceptance-critical execution should freeze actual executable/artifact digest, resolved path/runtime identity, rule/database/template snapshot, and a full resource envelope.

Required resource semantics include process-tree kill/reaping, CPU/memory/disk/file/process limits where applicable, temporary artifact cleanup, inherited environment/credential minimization, and concurrency arbitration.

### FINDING-GOV-001 — MEDIUM — finding correlation and accepted-risk/suppression governance are under-specified

The plan preserves findings and reconciliation, but lacks:

- stable finding fingerprint/correlation semantics across engines/heads;
- explicit finding relations (`SAME_ROOT_CAUSE`, `DUPLICATE_SIGNAL`, `SUPERSEDES`, etc.);
- accepted-risk/suppression scope, reason, authority, expiry/review date, target binding, and rule provenance.

Risk: duplicated findings overwhelm users, or suppressions become invisible permanent policy bypasses.

### BENCH-PERF-001 — MEDIUM — performance evidence lacks statistical baseline semantics

Performance is included in `/review` and `/fulltest`, but a qualified performance claim needs benchmark identity, baseline target, warmup/repetition strategy, hardware/runtime identity, variance/noise handling, threshold, and regression confidence.

Risk: noisy one-shot measurements become material findings or false clean evidence.

### WEB-ARTIFACT-001 — MEDIUM — browser artifact and multi-context effect boundaries need expansion

Browser planning covers sessions/origins/tool generation well, but upload/download/clipboard/native permission prompts/popups/new tabs/frames should feed explicit artifact/context/effect contracts.

Risk: browser actuation can bypass `InputArtifact`, context visibility, or target identity through downloaded/uploaded files or auxiliary contexts.

### UX-CATALOG-001 — MEDIUM — native command catalog is inconsistent

`spec.md` includes `/web` but omits `/security` and `/fulltest`; `contracts/command-surface.md` includes `/security` and `/fulltest` but omits `/web`; parent `acceptance.md` omits `/web`, `/security`, and `/fulltest` from its workflow completeness list.

Risk: implementation/CLI/IDE teams cannot identify one canonical stable command catalog.

### REVIEW-META-001 — LOW — review and PR metadata label historical identities as current

The Fable reconciliation carries `CURRENT_REPAIRED_AND_EXPANDED_HEAD/TREE` values that are no longer current. PR #241 body also contains stale exact-head/main/count metadata.

Risk: later agents can accidentally treat historical scope as live qualification evidence.

## Additional professional hardening requirements

These are cross-cutting repairs bundled into the findings above rather than separate architecture changes:

1. Dirty/uncommitted target identity must explicitly account for untracked/ignored/submodule/generated/LFS-like state when material to a claim; Git commit identity alone is insufficient for workspace assurance.
2. Rule/config precedence must define conflict resolution; untrusted lower-precedence configuration cannot weaken a stronger layer.
3. Reviewer scope/coverage should be a typed coverage claim, not only prose.
4. Flake governance should support known-flake/quarantine ownership and expiry; quarantine cannot erase failure evidence.
5. Engine/profile policy definitions must be versioned so historical bundles retain meaning.
6. Durable-store migration/backup/restore and evidence schema migration belong in S9 acceptance, not implicit implementation detail.
7. Multi-case S10 scheduling must eventually define fairness/starvation/resource quotas, but this remains an owning-slice deferred decision rather than a current blocker.

## Strengths explicitly retained

The review found no reason to reopen these architectural decisions:

- provider-neutral `Case` rather than GitHub as core model;
- append-only conflicting provider evidence;
- provenance-first RAG with vector optional and benchmark-gated;
- untrusted content structurally unable to mint intent/authority;
- Edara/Mirefa/Nawat/Mission Runtime/UWC separation;
- no silent provider/model/worker/browser/engine fallback;
- exact-target independent review;
- S7 Assurance distinct from S8 repair/completion;
- one Assurance Fabric instead of review/security/test silos;
- Fehrest.Maemar as graph owner;
- AMAN as security-evidence owner;
- Nawat as effect authority;
- `/fulltest` as minimum-sufficient assurance, not run-everything;
- local/air-gap-first baseline;
- source acquisition before reinvention;
- OpenHands used as a mechanism quarry with clean-room adaptation preferred;
- browser/WebMCP metadata/session state treated as non-authoritative;
- exact-head evidence staleness and non-erasing finding semantics.

## Repair acceptance

This internal review is considered reconciled only when:

- every HIGH and MEDIUM finding above has an explicit contract/task repair or a justified owning-slice deferral with no ambiguity in current interfaces;
- cross-artifact shared type names are canonical and mechanically checkable later;
- parent command catalog is internally consistent;
- the final planning head receives fresh deterministic qualification after canonical reconciliation;
- a genuinely independent exact-head whole-scope review is completed;
- all material findings from that independent review are reconciled.

```text
INTERNAL_REVIEW_COMPLETE = YES
INTERNAL_REVIEW_FINDINGS = 15
HIGH = 7
MEDIUM = 7
LOW = 1
PRE_REPAIR_PLAN_VERDICT = STRONG_DIRECTION_WITH_MATERIAL_REPAIRS_REQUIRED
INDEPENDENT_ACCEPTANCE_REVIEW = STILL_REQUIRED
```