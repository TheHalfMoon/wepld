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

This index makes the future WePLD Native Assurance Fabric explicit and discoverable inside Spec 006. It does not activate implementation.

## Product surfaces

```text
/review
/security
/fulltest
```

These commands are profiles over one Assurance Fabric, not separate authority paths or separate product engines.

## Planning package

Read in this order:

1. `assurance-fabric-plan.md` — product thesis, architecture, ownership, profiles, evidence model, review/security/testing design, IDE experience, freshness, dynamic-security boundary, benchmarks, and roadmap mapping.
2. `contracts/assurance-fabric.md` — canonical semantic contracts for exact targets, immutable policy snapshots, plans, engine descriptors/runs, findings/dispositions, evidence handling, coverage, performance, reproduction, fix proposals, reverification, typed claim assessment, and Assurance bundles.
3. `assurance-fabric-spec-addendum.md` — functional requirements and acceptance constraints, including AF-FR041..050 hardening requirements.
4. `assurance-fabric-tasks.md` — dependency-ordered future task map from revalidation/source acquisition through S3/S4/S5/S6/S7/S8/S9.
5. `professional-plan-hardening-tasks.md` — cross-cutting task map for the material whole-plan review findings without creating a new roadmap/authority path.
6. `reviews/professional-whole-plan-review-2026-09-02.md` — internal architecture/product/execution review that found the hardening gaps; useful repair evidence but not the independent acceptance review.
7. `research/native-assurance-source-acquisition-2026-09-02.md` — source families, behavior oracles, reusable machinery candidates, license/admission boundaries, negative oracles, and future exact-pin qualification work.
8. `research/openhands-qualified-mechanism-extraction-2026-09-02.md` — exact pinned OpenHands source quarries, nine extracted mechanisms, rejected semantics, clean-room adaptation decisions, and negative oracles.
9. `openhands-assurance-integration-tasks.md` — dependency-ordered S3/S6/S7/S8/S9 implementation tasks and tracer bullets for the OpenHands-derived mechanisms.
10. `contracts/command-surface.md` — canonical user-facing command catalog and `/review`, `/security`, `/fulltest` intent semantics.

## Architectural placement

```text
S3  trusted process execution / local engine containment + unknown-effect recovery
S4  Fehrest.Maemar context + Project Brain evidence + source/access generations
S5  command/intention normalization + policy-bound Assurance plan construction
S6  qualification/routing/Nawat effect authority integration
S7  Assurance Fabric core + Native Review + AMAN Security + FullTest + ClaimAssessment
S8  separately authorized controlled repair/reassignment/reverification loops
S9  Quality Passport + evidence history/migration/backup/recovery
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
```

## Differentiation target

The intended product is not another code-review bot or scanner dashboard. WePLD should provide one local-first, exact-target engineering assurance system that can join review, security, test, coverage, mutation/fuzz/property/formal evidence, dependency/supply-chain evidence, reachability, project graph context, IDE diagnostics, evidence handling/freshness, and a typed policy-bound claim assessment into one inspectable model.

A user should be able to ask questions such as:

```text
Is this vulnerability actually reachable?
Which entrypoint reaches it?
Which tests exercise that path?
Which tests should have exercised it but did not?
Which change introduced the path?
Which exact reviewer/scanner/test run supports this claim?
What exact policy/profile defines this claim?
Did the latest commit or policy/access change stale any prior evidence?
What required check could not run, and does that block the claim?
What was intentionally omitted from this assurance run, and why?
What remains unknown before release or Trusted Completion?
```

## Source-acquisition boundary

The research package includes strong candidates and behavior oracles such as Continue, CodeRabbit Skills, Greptile, Qodo, Devin Review/Security, Aikido, OpenHands Agent Canvas / Software Agent SDK, tree-sitter, ast-grep, reviewdog, Semgrep, Trivy, OSV-Scanner, Syft, zizmor, OpenSSF Scorecard/Package Analysis, cargo-nextest, cargo-llvm-cov, cargo-mutants, Kani, Schemathesis, Playwright, Nuclei, and OWASP ZAP.

OpenHands is treated as a path-level mechanism quarry rather than a runtime architecture authority. The default disposition for the extracted OpenHands mechanisms is clean-room WePLD-native adaptation; direct source import or dependency admission remains separately gated.

No listed source is admitted merely by being named here. Exact future reuse requires current revision/license/provenance/rights verification and the owning Source Acquisition gate. Donor dependencies, workflows, hooks, scanners, templates, or package scripts must not be executed during reconnaissance merely because they are open source.

## Activation rule

This planning package becomes executable only when the canonical roadmap reaches the owning slice and a then-current authority artifact activates an exact tranche.

```text
PLANNED != AUTHORIZED
DOCUMENTED != IMPLEMENTED
SOURCE_RESEARCHED != SOURCE_ADMITTED
ENGINE_QUALIFIED != EFFECT_AUTHORIZED
CLAIM_SUPPORTED != TRUSTED_COMPLETION
```
