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
2. `contracts/assurance-fabric.md` — semantic contracts for exact targets, plans, engine descriptors/runs, findings, evidence, coverage, reproduction, fix proposals, reverification, and Assurance bundles.
3. `assurance-fabric-spec-addendum.md` — functional requirements and acceptance constraints.
4. `assurance-fabric-tasks.md` — dependency-ordered future task map from revalidation/source acquisition through S3/S4/S5/S6/S7/S8/S9.
5. `research/native-assurance-source-acquisition-2026-09-02.md` — source families, behavior oracles, reusable machinery candidates, license/admission boundaries, negative oracles, and future exact-pin qualification work.
6. `contracts/command-surface.md` — user-facing `/review`, `/security`, and `/fulltest` intent semantics.

## Architectural placement

```text
S3  trusted process execution / local engine containment
S4  Fehrest.Maemar context + Project Brain evidence
S5  command/intention normalization + Assurance plan construction
S6  qualification/routing/Nawat effect authority integration
S7  Assurance Fabric core + Native Review + AMAN Security + FullTest
S8  separately authorized controlled repair/reassignment/reverification loops
S9  Quality Passport + evidence history/recovery
```

Assurance MUST consume existing WePLD ownership instead of duplicating it:

```text
FEHREST = canonical project/code/architecture context owner
AMAN = security/risk evidence owner
NAWAT = effect-time authority owner
ASSURANCE = assurance orchestration/findings/evidence owner
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
COVERAGE_PERCENTAGE != BEHAVIORAL_PROOF
RETRY_PASS != CLEAN_PASS
FLAKY != PASS
ENGINE_ERROR != NO_FINDINGS
UNKNOWN_REACHABILITY != UNREACHABLE
MULTIPLE_CLEAN_REVIEWERS != INVALIDATE_ONE_VALIDATED_FINDING
NEW_EXACT_HEAD -> PRIOR_ACCEPTANCE_CRITICAL_EVIDENCE_STALE
SOURCE_LICENSE != SOURCE_ADMISSION
SOURCE_ADMISSION != DEPENDENCY_ADMISSION
```

## Differentiation target

The intended product is not another code-review bot or scanner dashboard. WePLD should provide one local-first, exact-target engineering assurance system that can join review, security, test, coverage, mutation/fuzz/property/formal evidence, dependency/supply-chain evidence, reachability, project graph context, IDE diagnostics, and evidence freshness into one inspectable claim model.

A user should be able to ask questions such as:

```text
Is this vulnerability actually reachable?
Which entrypoint reaches it?
Which tests exercise that path?
Which tests should have exercised it but did not?
Which change introduced the path?
Which exact reviewer/scanner/test run supports this claim?
Did the latest commit stale any prior review/security/test evidence?
What was intentionally omitted from this assurance run, and why?
What remains unknown before release or Trusted Completion?
```

## Source-acquisition boundary

The research package includes strong candidates and behavior oracles such as Continue, CodeRabbit Skills, Greptile, Qodo, Devin Review/Security, Aikido, tree-sitter, ast-grep, reviewdog, Semgrep, Trivy, OSV-Scanner, Syft, zizmor, OpenSSF Scorecard/Package Analysis, cargo-nextest, cargo-llvm-cov, cargo-mutants, Kani, Schemathesis, Playwright, Nuclei, and OWASP ZAP.

No listed source is admitted merely by being named here. Exact future reuse requires current revision/license/provenance/rights verification and the owning Source Acquisition gate. Donor dependencies, workflows, hooks, scanners, templates, or package scripts must not be executed during reconnaissance merely because they are open source.

## Activation rule

This planning package becomes executable only when the canonical roadmap reaches the owning slice and a then-current authority artifact activates an exact tranche.

```text
PLANNED != AUTHORIZED
DOCUMENTED != IMPLEMENTED
SOURCE_RESEARCHED != SOURCE_ADMITTED
ENGINE_QUALIFIED != EFFECT_AUTHORIZED
ASSURANCE_CLEAN != TRUSTED_COMPLETION
```
