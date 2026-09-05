# WePLD Native Assurance Fabric — Planning Index

```text
STATUS = FUTURE_PLANNING_INDEX
PRIMARY_OWNER_SLICE = S7_NATIVE_REVIEW_AND_ASSURANCE
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PROCESS_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
ROADMAP_RENUMBERING = NONE
```

This index makes the future WePLD Native Assurance Fabric explicit and discoverable inside Spec 006. It does not activate implementation. `PLANNING_INDEX.md` is the whole Spec 006 read-order index; this file is the Assurance-focused index.

## Product surfaces

```text
/review
/security
/fulltest
```

These commands are profiles over one Assurance Fabric, not separate authority paths or separate product engines.

## Planning package

Read in this order for Assurance/runtime context:

1. `assurance-fabric-plan.md` — product thesis, architecture, ownership, profiles, evidence model, review/security/testing design, IDE experience, freshness, dynamic-security boundary, benchmarks, and roadmap mapping.
2. `contracts/assurance-fabric.md` — canonical semantic contracts for exact targets, immutable policy snapshots, plans, engine descriptors/runs, findings/dispositions, evidence handling, coverage, performance, reproduction, fix proposals, reverification, typed claim assessment, and Assurance bundles.
3. `contracts/review-independence.md` — typed builder/reviewer separation, context/workspace/authority conflict checks, and exact-target `ReviewIndependenceReceipt` evidence.
4. `contracts/runtime-execution-fabric.md` — Server/Host/Runner identity, protocol/dialect adapters, containment posture, runtime ceilings, environment exposure, credential capabilities, effect dependency ordering, and native desktop bridge boundaries consumed by later Assurance/runtime work.
5. `contracts/runtime-distributed-safety-addendum.md` — authenticated host enrollment, runner lease/fencing, exact harness execution identity, runtime event dedupe/causality, resource admission, and protocol/version safety.
6. `contracts/behavior-policy-boundary.md` — behavior-policy trust and fail-closed pre-effect policy semantics while preserving Nawat as the sole effect authority.
7. `contracts/case-bus.md` — typed Case-scoped coordination messages that cannot become WorkflowIntent, Assignment, authority, review acceptance, or completion by receipt alone.
8. `assurance-fabric-spec-addendum.md` — functional requirements and acceptance constraints for the Assurance surface.
9. `runtime-execution-fabric-spec-addendum.md` — functional requirements for execution-fabric/containment/credential/recovery/distributed safety.
10. `runtime-execution-fabric-acceptance.md` — planning acceptance gates for execution fabric, distributed runtime, policy trust, Omnigent source boundary, and discoverability.
11. `assurance-fabric-tasks.md` — dependency-ordered future Assurance task map from revalidation/source acquisition through S3/S4/S5/S6/S7/S8/S9.
12. `professional-plan-hardening-tasks.md` — cross-cutting task map for the earlier whole-plan review findings without creating a new roadmap/authority path.
13. `omnigent-execution-fabric-integration-tasks.md` — S3/S5/S6/S7/S8/S9 task map for host/runner identity, containment, credential brokering, ACP/vendor extension seams, browser freshness, review independence, and effect ordering.
14. `runtime-distributed-safety-tasks.md` — host authentication, fencing, causal events, exact harness identity, resource admission, protocol compatibility, and behavior-policy implementation tasks.
15. `reviews/professional-whole-plan-review-2026-09-02.md` — historical internal architecture/product/execution review; useful repair evidence but not independent acceptance review.
16. `research/native-assurance-source-acquisition-2026-09-02.md` — source families, behavior oracles, reusable machinery candidates, license/admission boundaries, negative oracles, and future exact-pin qualification work.
17. `research/openhands-qualified-mechanism-extraction-2026-09-02.md` — exact pinned OpenHands source quarries, extracted mechanisms, rejected semantics, clean-room adaptation decisions, and negative oracles.
18. `openhands-assurance-integration-tasks.md` — dependency-ordered S3/S6/S7/S8/S9 implementation tasks and tracer bullets for the OpenHands-derived mechanisms.
19. `research/omnigent-qualified-mechanism-extraction-2026-09-04.md` — exact pinned Omnigent mechanism quarry covering meta-harness/runtime identities, ACP extension seams, policy choke points, containment, secretless credentials, browser snapshot freshness, review independence, recovery, and desktop trust boundaries.
20. `source-acquisition-omnigent-addendum.md` — exact future source-acquisition posture, license/NOTICE boundaries, security-specific reuse gates, and minimum-reuse decisions for Omnigent.
21. `contracts/command-surface.md` — canonical user-facing command catalog and `/review`, `/security`, `/fulltest` intent semantics.

## Architectural placement

```text
S3  trusted process execution / host-runner identity / local engine containment / env/native bridge / host trust + event identity + unknown-effect recovery
S4  Fehrest.Maemar context + Project Brain evidence + source/access generations
S5  command/intention normalization + policy-bound Assurance plan construction + protocol/execution-envelope/policy dry-runs
S6  qualification/routing/Nawat integration + UWC protocol/dialect adapters + runner fabric/fencing + credential capabilities + resource admission
S7  Assurance Fabric core + Native Review + AMAN Security + FullTest + ClaimAssessment + ReviewIndependenceReceipt
S8  separately authorized controlled repair/reassignment/reverification + effect dependency/reconciliation/compensation loops
S9  Quality Passport + host/runner/harness/attempt/credential-use/runtime-event evidence history/migration/backup/recovery
```

Assurance MUST consume existing WePLD ownership instead of duplicating it:

```text
FEHREST = canonical project/code/architecture context owner
AMAN = security/risk evidence owner
NAWAT = effect-time authority owner
ASSURANCE = assurance orchestration/findings/evidence/claim-assessment owner
S8 = repair authority consumer under separately authorized Attempts
TRUSTED_COMPLETION = completion decision boundary
```

## Core invariants

```text
ASSURANCE_PLAN != EFFECT_AUTHORITY
ENGINE_AVAILABLE != ENGINE_AUTHORIZED
ENGINE_OUTPUT != TRUTH
REVIEW_OUTCOME != COMPLETION_DECISION
SECURITY_FINDING != WRITE_AUTHORITY
TEST_PASS != TRUSTED_COMPLETION
CLAIM_SUPPORTED != TRUSTED_COMPLETION
COVERAGE_PERCENTAGE != BEHAVIORAL_PROOF
RETRY_PASS != CLEAN_PASS
FLAKY != PASS
ENGINE_ERROR != NO_FINDINGS
UNKNOWN_REACHABILITY != UNREACHABLE
MISSING_REQUIRED_EVIDENCE != SUPPORTED
BUDGET_EXCEEDED != REQUIRED_EVIDENCE_WAIVER
MULTIPLE_CLEAN_REVIEWERS != INVALIDATE_ONE_VALIDATED_FINDING
NEW_EXACT_HEAD -> PRIOR_ACCEPTANCE_CRITICAL_EVIDENCE_STALE
SOURCE_ACCESS_REVOKED -> DERIVED_CONTEXT_ELIGIBILITY_REVOKED
SOURCE_LICENSE != SOURCE_ADMISSION
SOURCE_ADMISSION != DEPENDENCY_ADMISSION
POLICY_NO_OBJECTION != NAWAT_GRANT
SERVER_ID != HOST_ID != RUNNER_ID != WORKER_ID != ATTEMPT_ID
HOST_ID_CLAIM != AUTHENTICATED_HOST
PROCESS_TREE_CONTAINMENT_ONLY != HARD_SANDBOX
SANDBOX_REQUIRED_AND_UNAVAILABLE -> EXECUTION_REFUSED
AMBIENT_SECRET != WORKER_VISIBLE_SECRET
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
STALE_RUNNER_FENCING_TOKEN -> EFFECT_REFUSED
DUPLICATE_RUNTIME_EVENT != SECOND_EFFECT
WORKER_DESCRIPTOR_VERSION != EXECUTED_HARNESS_IDENTITY
DIFFERENT_VENDOR_ALONE != REVIEW_INDEPENDENCE_PROOF
MESSAGE_RECEIVED != WORKFLOW_INTENT
PREREQUISITE_EFFECT_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_BLOCKED
```

## Differentiation target

The intended product is not another code-review bot or scanner dashboard. WePLD should provide one local-first, exact-target engineering assurance system that can join review, security, test, coverage, mutation/fuzz/property/formal evidence, dependency/supply-chain evidence, reachability, project graph context, IDE diagnostics, evidence handling/freshness, execution-host provenance, distributed-runner ownership, reviewer independence, credential-use evidence, and a typed policy-bound claim assessment into one inspectable model.

A user should be able to ask questions such as:

```text
Is this vulnerability actually reachable?
Which entrypoint reaches it?
Which tests exercise that path?
Which tests should have exercised it but did not?
Which change introduced the path?
Which exact reviewer/scanner/test run supports this claim?
Was the reviewer genuinely independent under the active policy?
Which host/runner/harness/containment posture executed acceptance-critical checks?
Was that runner still the fenced owner when the effect occurred?
Did a credentialed effect use a bounded capability or expose a reusable secret?
What exact policy/profile defines this claim?
Did the latest commit, policy, access, runtime, harness, or ownership change stale any prior evidence?
What required check could not run, and does that block the claim?
What was intentionally omitted from this assurance run, and why?
What remains unknown before release or Trusted Completion?
```

## Source-acquisition boundary

The research package includes strong candidates and behavior oracles such as Continue, CodeRabbit Skills, Greptile, Qodo, Devin Review/Security, Aikido, OpenHands Agent Canvas / Software Agent SDK, Omnigent, tree-sitter, ast-grep, reviewdog, Semgrep, Trivy, OSV-Scanner, Syft, zizmor, OpenSSF Scorecard/Package Analysis, cargo-nextest, cargo-llvm-cov, cargo-mutants, Kani, Schemathesis, Playwright, Nuclei, and OWASP ZAP.

OpenHands is treated as a path-level mechanism quarry rather than a runtime architecture authority. The default disposition for extracted OpenHands mechanisms is clean-room WePLD-native adaptation; direct source import or dependency admission remains separately gated.

Omnigent is treated as a high-value execution-fabric mechanism quarry, especially for Server/Host/Runner separation, generic ACP/vendor extension seams, fail-loud containment, secretless credential brokering, browser snapshot freshness, different-vendor review as an independence signal, recovery semantics, and thin desktop native bridges. Its policy engine is a behavior oracle only; `ALLOW/ASK/DENY` does not replace Nawat authority. Repository Apache-2.0 licensing and the presence of a NOTICE file do not imply source or dependency admission.

No listed source is admitted merely by being named here. Exact future reuse requires current revision/license/provenance/rights verification and the owning Source Acquisition gate. Donor dependencies, workflows, hooks, scanners, templates, installers, policy modules, sandboxes, credential proxies, native bridges, or package scripts must not be executed during reconnaissance merely because they are open source.

## Activation rule

This planning package becomes executable only when the canonical roadmap reaches the owning slice and a then-current authority artifact activates an exact tranche.

```text
PLANNED != AUTHORIZED
DOCUMENTED != IMPLEMENTED
SOURCE_RESEARCHED != SOURCE_ADMITTED
ENGINE_QUALIFIED != EFFECT_AUTHORIZED
CLAIM_SUPPORTED != TRUSTED_COMPLETION
```
