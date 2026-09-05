# Tasks — Native Assurance Fabric

```text
STATUS = FUTURE_TASK_MAP_ONLY
OWNER_SLICE = S7_NATIVE_REVIEW_AND_ASSURANCE
CURRENT_ACTIVE_SLICE = S2
ALL_TASKS_ACTIVE = NO
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PROCESS_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
DYNAMIC_SECURITY_EXECUTION_AUTHORITY = NONE
```

This file is the dependency-ordered implementation map for the future WePLD Native Assurance Fabric. The existence of a task does not authorize execution. Every tranche still requires then-current canonical activation, Spec Kit, Ponytail FULL, Source Acquisition, exact allowlists, deterministic qualification, independent review, security accounting where applicable, and Trusted Completion rules.

The three primary user surfaces are profiles over one fabric:

```text
/review
/security
/fulltest
```

They MUST NOT become separate authority paths or duplicate Fehrest/AMAN/Nawat ownership.

## P — Revalidation, qualification design, and source acquisition

- [ ] `006-AF-P001` Re-read then-current canonical governance, roadmap, active slice, and exact implementation authority before any Assurance tranche.
- [ ] `006-AF-P002` Re-run full Spec Kit clarification for the first activated Assurance tracer bullet.
- [ ] `006-AF-P003` Run Ponytail FULL against the exact first Assurance tranche and record missing acceptance or falsification boundaries.
- [ ] `006-AF-P004` Reverify every required donor/reference source at an exact revision, license, provenance, and availability state before reuse.
- [ ] `006-AF-P005` Distinguish `BEHAVIOR_ORACLE`, `TEST_QUARRY`, `SOURCE_CANDIDATE`, `DEPENDENCY_CANDIDATE`, `INTERCHANGE_STANDARD`, and `HOSTED_REVIEWER_CANDIDATE` for every source.
- [ ] `006-AF-P006` Prove already-admitted WePLD machinery cannot satisfy the need before admitting new dependencies.
- [ ] `006-AF-P007` Define exact engine qualification records including version, supported languages, effect classes, configuration trust, known limitations, output format, and reproducibility expectations.
- [ ] `006-AF-P008` Define a labeled Assurance benchmark corpus before promotion thresholds are tuned.
- [ ] `006-AF-P009` Define cross-domain negative oracles for false clean, stale evidence, engine crash, partial coverage, contradictory findings, dynamic reachability ambiguity, and flaky retry behavior.
- [ ] `006-AF-P010` Define latency/budget envelopes for `LIVE`, `QUICK`, `WORKSPACE`, `DEEP`, `ADVERSARIAL`, and `RELEASE` profiles.
- [ ] `006-AF-P011` Define exact target/freshness rules before any acceptance-critical reviewer or scanner can be counted.
- [ ] `006-AF-P012` Define egress qualification for every hosted reviewer/security provider under the canonical external-review egress policy.
- [ ] `006-AF-P013` Preserve local/offline operation as the reference path; prove remote reviewer absence does not disable local deterministic Assurance.
- [ ] `006-AF-P014` Define the first minimal tracer bullet without source/network/provider execution.

## S3 — Trusted process execution and engine-adapter substrate

Depends on S3 Terminal Fabric and exact process authority.

- [ ] `006-AF-S3-001` Define `EngineDescriptor` and executable identity semantics.
- [ ] `006-AF-S3-002` Define exact argv/environment/cwd/stdin/stdout/stderr/timeout/output-size contracts for local Assurance engines.
- [ ] `006-AF-S3-003` Define engine effect classes: pure in-process, local-read, local-process, filesystem-write, network, browser, provider, credential-bearing.
- [ ] `006-AF-S3-004` Implement fail-closed adapter execution through the trusted process boundary only after process authority exists.
- [ ] `006-AF-S3-005` Prove no shell interpolation or ambient hook/profile startup is needed for deterministic engine invocation.
- [ ] `006-AF-S3-006` Add output-size, timeout, cancellation, orphan-process, and malformed-output negative tests.
- [ ] `006-AF-S3-007` Normalize process failure distinctly from `NO_FINDINGS`.
- [ ] `006-AF-S3-008` Preserve command/config/environment identities as `EngineRun` evidence.
- [ ] `006-AF-S3-009` Qualify Windows-first path/process behavior before cross-platform claims.
- [ ] `006-AF-S3-010` Prove untrusted repository configuration cannot silently enable network/process/write effects.

## S4 — Fehrest context, graph joins, and evidence persistence

Depends on S4 Fehrest / Project Brain activation.

- [ ] `006-AF-S4-001` Define `AssuranceTarget` identity over project/workspace/base/head/tree/change/spec/rule generations.
- [ ] `006-AF-S4-002` Consume Fehrest.Maemar graph facts through stable interfaces; do not build a competing authoritative project graph.
- [ ] `006-AF-S4-003` Define changed-symbol, caller, usage, dependency, ownership, test, schema, and entrypoint context joins.
- [ ] `006-AF-S4-004` Define `ReviewContextCapsule` with bounded provenance and explicit context coverage.
- [ ] `006-AF-S4-005` Define durable `EvidenceRef` identity/freshness/trust semantics.
- [ ] `006-AF-S4-006` Define exact graph/index generation binding and stale-generation invalidation.
- [ ] `006-AF-S4-007` Add evidence joins from finding -> symbol/resource -> reachability path -> test coverage -> change identity.
- [ ] `006-AF-S4-008` Add conservative `UNKNOWN_REACHABILITY` for unresolved dynamic/reflection/runtime cases.
- [ ] `006-AF-S4-009` Add cross-repository context only behind explicit source/read authority and provenance.
- [ ] `006-AF-S4-010` Persist historical findings without promoting repeated patterns into canonical rules.

## S5 — Intent, planning, rules, and no-effect dry runs

Depends on S5 workflow/Spec Kit mechanics.

- [ ] `006-AF-S5-001` Define `AssuranceIntent` as a normalized user/workflow request distinct from authority.
- [ ] `006-AF-S5-002` Implement no-effect `/review` plan generation over synthetic/local fixtures.
- [ ] `006-AF-S5-003` Implement no-effect `/security` plan generation over synthetic/local fixtures.
- [ ] `006-AF-S5-004` Implement no-effect `/fulltest` plan generation over synthetic/local fixtures.
- [ ] `006-AF-S5-005` Define `AssurancePlan` with selected/omitted checks, reasons, effect requirements, budgets, and expected evidence.
- [ ] `006-AF-S5-006` Implement rule hierarchy: canonical -> repository -> component -> spec/task -> language/ecosystem -> advisory preference.
- [ ] `006-AF-S5-007` Prove source-branch/PR-controlled review configuration cannot weaken canonical requirements.
- [ ] `006-AF-S5-008` Implement `LIVE`, `QUICK`, `WORKSPACE`, `DEEP`, `ADVERSARIAL`, and `RELEASE` planning profiles without executing unauthorized effects.
- [ ] `006-AF-S5-009` Require every omitted check class to carry an explicit reason.
- [ ] `006-AF-S5-010` Require plan explanations to show why each selected check is relevant to the requested claim.
- [ ] `006-AF-S5-011` Prove `/fulltest` does not degenerate into blindly executing every repository script/command.
- [ ] `006-AF-S5-012` Prove untrusted issue/RAG/code/log content cannot create an Assurance intent or expand the selected effect envelope.

## S6 — Qualification, routing, and authority integration

Depends on UWC/Mirefa/Edara/Nawat/Mission Runtime activation.

- [ ] `006-AF-S6-001` Represent each Assurance engine/tool/reviewer as a qualified route with explicit capability and effect metadata.
- [ ] `006-AF-S6-002` Keep engine availability distinct from engine qualification.
- [ ] `006-AF-S6-003` Keep qualification distinct from Nawat effect-time authorization.
- [ ] `006-AF-S6-004` Prohibit silent fallback among local, hosted, paid, model, scanner, browser, or provider routes.
- [ ] `006-AF-S6-005` Add cost/quota/latency/containment constraints to route qualification.
- [ ] `006-AF-S6-006` Add reviewer independence metadata and eligibility checks.
- [ ] `006-AF-S6-007` Add exact egress preflight integration for hosted reviewers before content transmission.
- [ ] `006-AF-S6-008` Prove a provider/model/tool result cannot mint write, repair, merge, or completion authority.

## S7-A — Assurance core and evidence model

Primary owning slice.

- [ ] `006-AF-S7-A001` Implement `AssuranceTarget` exact-target identity.
- [ ] `006-AF-S7-A002` Implement `AssurancePlan` and immutable plan identity.
- [ ] `006-AF-S7-A003` Implement `EngineDescriptor` / `EngineRun` normalized evidence.
- [ ] `006-AF-S7-A004` Implement normalized `Finding` lifecycle.
- [ ] `006-AF-S7-A005` Implement `CoverageClaim` as multi-dimensional evidence rather than one percentage.
- [ ] `006-AF-S7-A006` Implement `Reproduction` and counterexample evidence.
- [ ] `006-AF-S7-A007` Implement `Reverification` linking old findings to new exact-target evidence.
- [ ] `006-AF-S7-A008` Implement queryable `AssuranceBundle` without completion authority.
- [ ] `006-AF-S7-A009` Implement exact-head/workspace-generation staleness propagation.
- [ ] `006-AF-S7-A010` Preserve contradictory engine outputs instead of majority-voting them into one answer.
- [ ] `006-AF-S7-A011` Prove one validated finding is not erased by multiple clean engines.
- [ ] `006-AF-S7-A012` Normalize `ENGINE_ERROR`, `UNSUPPORTED`, `NOT_RUN`, `PARTIAL`, `INCONCLUSIVE`, `CLEAN`, and finding-producing outcomes separately.

## S7-R — Native `/review`

- [ ] `006-AF-S7-R001` Build logical change grouping over raw diffs using Fehrest structural context.
- [ ] `006-AF-S7-R002` Add moved/copied/refactored-code recognition sufficient to reduce diff noise.
- [ ] `006-AF-S7-R003` Build bounded Review Context Capsules from callers/usages/dependencies/related implementations/specs/rules/evidence.
- [ ] `006-AF-S7-R004` Implement standards/correctness axis separately from spec/contract-conformance axis.
- [ ] `006-AF-S7-R005` Add architecture/maintainability/performance/test-quality/security-risk review categories.
- [ ] `006-AF-S7-R006` Add independent reviewer eligibility and exact-base/head/file-scope evidence.
- [ ] `006-AF-S7-R007` Add material thread/finding reconciliation with explicit resolved/invalidated/accepted-risk evidence.
- [ ] `006-AF-S7-R008` Invalidate acceptance-critical review after target change unless explicit coverage reconciliation proves equivalence.
- [ ] `006-AF-S7-R009` Add false-positive/false-negative benchmark corpus across representative repository change classes.
- [ ] `006-AF-S7-R010` Support qualified local review engines and optional hosted reviewers without making hosted service availability mandatory.

## S7-S — Native `/security` and AMAN integration

- [ ] `006-AF-S7-S001` Integrate AMAN security/risk evidence ownership with Assurance finding normalization.
- [ ] `006-AF-S7-S002` Qualify a local structural/SAST foundation after Source Acquisition.
- [ ] `006-AF-S7-S003` Add secret/private-data detection before external review egress.
- [ ] `006-AF-S7-S004` Add dependency/SCA vulnerability evidence using exact package/version/ecosystem identity.
- [ ] `006-AF-S7-S005` Add SBOM generation/import with CycloneDX/SPDX interchange where qualified.
- [ ] `006-AF-S7-S006` Add IaC/configuration/security-policy checks.
- [ ] `006-AF-S7-S007` Add GitHub Actions/CI workflow security checks.
- [ ] `006-AF-S7-S008` Add supply-chain/package-risk evidence and malicious-package intelligence adapters.
- [ ] `006-AF-S7-S009` Implement graph/taint/resource reachability joins with conservative unknown states.
- [ ] `006-AF-S7-S010` Join vulnerability reachability to affected tests and coverage evidence.
- [ ] `006-AF-S7-S011` Generate threat-model-derived check requirements from assets, boundaries, entrypoints, secrets, privileged effects, dependencies, browser/network surfaces, and recovery paths.
- [ ] `006-AF-S7-S012` Prove model judgment cannot downgrade deterministic security-sensitive evidence by itself.
- [ ] `006-AF-S7-S013` Build a labeled security corpus including reachable/unreachable/unknown vulnerable dependencies, workflow injection, secrets, IaC, and supply-chain cases.
- [ ] `006-AF-S7-S014` Preserve `NOT_RUN_NON_BLOCKING` / coverage gaps explicitly rather than manufacturing a security PASS.

## S7-T — Native `/fulltest`

- [ ] `006-AF-S7-T001` Build changed-file/symbol impact-based test selection.
- [ ] `006-AF-S7-T002` Join code graph, package/build ownership, schema/API edges, historical failures, and test coverage into selection evidence.
- [ ] `006-AF-S7-T003` Support normalized format/lint/build/type/unit/integration/contract/snapshot result classes.
- [ ] `006-AF-S7-T004` Add JUnit/native test event ingestion with exact target/run identity.
- [ ] `006-AF-S7-T005` Add source/branch/function/region coverage where meaningful while preserving `COVERAGE != BEHAVIORAL_PROOF`.
- [ ] `006-AF-S7-T006` Add flaky/retry semantics where `RETRY_PASS != CLEAN_PASS`.
- [ ] `006-AF-S7-T007` Add mutation testing and survived-mutant evidence for qualified ecosystems.
- [ ] `006-AF-S7-T008` Add property-based and fuzz counterexample ingestion.
- [ ] `006-AF-S7-T009` Add API/schema-driven tests for qualified OpenAPI/GraphQL surfaces.
- [ ] `006-AF-S7-T010` Add browser/E2E test evidence through the separately qualified browser boundary.
- [ ] `006-AF-S7-T011` Add formal/model-checking evidence for high-value Rust/core invariants where justified.
- [ ] `006-AF-S7-T012` Add platform/runtime matrix evidence and prevent unsupported-platform silence from appearing green.
- [ ] `006-AF-S7-T013` Implement release profile requiring the exact predeclared evidence classes for its requested claim.
- [ ] `006-AF-S7-T014` Build selection-quality benchmarks: relevant test recall, unnecessary-test cost, missed regression rate, flake handling, stale-test mapping, and abstention.

## S7-I — IDE / Desktop Assurance experience

- [ ] `006-AF-S7-I001` Add one Assurance sidebar with `Overview`, `Review`, `Security`, `Tests`, `Coverage`, `Findings`, `Evidence`, and `History` views.
- [ ] `006-AF-S7-I002` Add gutter/inline diagnostics backed by normalized Finding identities.
- [ ] `006-AF-S7-I003` Add exact-target/freshness badges and visible stale-evidence state.
- [ ] `006-AF-S7-I004` Add pre-execution Assurance Plan inspection including selected/omitted checks and effect requirements.
- [ ] `006-AF-S7-I005` Add finding cards with severity, location, producers, reachability, evidence, confidence, exact revision, related tests, reproduction, and status.
- [ ] `006-AF-S7-I006` Add path visualization for vulnerable/reviewed code to entrypoints/resources and related tests.
- [ ] `006-AF-S7-I007` Integrate qualified test runners through native editor testing APIs where appropriate rather than rebuilding all runner UX.
- [ ] `006-AF-S7-I008` Keep live/editor checks effect-safe and low-latency; no surprise process/network execution from typing/saving.
- [ ] `006-AF-S7-I009` Add explicit user-visible engine errors and unsupported/coverage-limited regions.
- [ ] `006-AF-S7-I010` Support CLI/Desktop/IDE query of the same AssuranceBundle identities.

## S7-X — Interchange and adapter qualification

- [ ] `006-AF-S7-X001` Implement SARIF 2.1.x import/export adapter without reducing the richer internal finding schema to SARIF limitations.
- [ ] `006-AF-S7-X002` Implement JUnit/native test event adapters.
- [ ] `006-AF-S7-X003` Implement coverage adapters for qualified LCOV/Cobertura/LLVM/native formats.
- [ ] `006-AF-S7-X004` Implement CycloneDX/SPDX SBOM adapters.
- [ ] `006-AF-S7-X005` Implement OSV vulnerability record adapters.
- [ ] `006-AF-S7-X006` Implement compiler/linter diagnostic adapters.
- [ ] `006-AF-S7-X007` Implement property/fuzz/mutation counterexample adapters.
- [ ] `006-AF-S7-X008` Implement Playwright/browser trace evidence adapter after browser qualification.
- [ ] `006-AF-S7-X009` Require every adapter to preserve target identity, producer identity, unsupported fields, and coverage limitations.

## S7-D — Dynamic/adversarial security gate

Requires separate S3/S6/S7 network/target/scanner authority. These tasks are not implied by static Assurance activation.

- [ ] `006-AF-S7-D001` Define explicit authorized target/origin/host/port/protocol scope.
- [ ] `006-AF-S7-D002` Define credential source, least privilege, redaction, and retention rules.
- [ ] `006-AF-S7-D003` Define request/rate/concurrency/time budgets and stop conditions.
- [ ] `006-AF-S7-D004` Qualify scanner/template/plugin identities and disable arbitrary template/code execution by default.
- [ ] `006-AF-S7-D005` Add DAST/API scanner adapter only after target/network authority exists.
- [ ] `006-AF-S7-D006` Add browser-assisted adversarial checks only through the qualified browser boundary.
- [ ] `006-AF-S7-D007` Build safe local/synthetic vulnerable targets before any external target qualification.
- [ ] `006-AF-S7-D008` Prove `LOCAL_PROJECT_OPEN`, ambient credentials, cookies, or authenticated browser state cannot authorize scanning.
- [ ] `006-AF-S7-D009` Add request/response evidence handling that prevents secret/PII leakage into durable logs.
- [ ] `006-AF-S7-D010` Add explicit abort/recovery evidence for partial dynamic scans.

## S8 — Controlled repair integration

Depends on S8 activation; Assurance remains evidence producer, not write authority.

- [ ] `006-AF-S8-001` Define `FixProposal` as advisory evidence with zero write authority.
- [ ] `006-AF-S8-002` Convert a validated finding into a separately authorized bounded repair Attempt.
- [ ] `006-AF-S8-003` Preserve original finding/run/evidence while repair creates new attempt history.
- [ ] `006-AF-S8-004` Re-run only the minimum required invalidated checks after a repair, plus mandatory global gates.
- [ ] `006-AF-S8-005` Require exact-target reverification before `VERIFIED_FIXED`.
- [ ] `006-AF-S8-006` Support bounded retry/reassignment without collapsing reviewer independence.
- [ ] `006-AF-S8-007` Prove repair success does not itself become Trusted Completion.

## S9 — Quality Passport, history, and recovery

Depends on S9 activation.

- [ ] `006-AF-S9-001` Store AssuranceBundle identities in the Quality Passport/Evidence Timeline.
- [ ] `006-AF-S9-002` Record first-seen/last-verified finding generations and staleness transitions.
- [ ] `006-AF-S9-003` Record test flake, mutation, coverage, security, review, and engine qualification history without rewriting prior runs.
- [ ] `006-AF-S9-004` Produce release/change Assurance packets with exact evidence provenance and residual limitations.
- [ ] `006-AF-S9-005` Support recovery/time-machine views showing which evidence supported a historical decision.
- [ ] `006-AF-S9-006` Prove a historical green packet cannot be silently reused after its target/rule/engine/context generation becomes stale.
- [ ] `006-AF-S9-007` Feed evidence-backed false positives, missed findings, flaky tests, and routing mechanics into Build Learning/Project Brain as candidate learning only.

## Acceptance tracer bullets

### AF-TB0 — no-effect planning

```text
synthetic/local exact target
-> /review|/security|/fulltest AssuranceIntent
-> AssurancePlan
-> Fehrest fixture context
-> selected/omitted checks with reasons
-> zero process/network/provider/write effects
```

### AF-TB1 — local deterministic engine

Requires S3 process authority and one qualified local engine.

```text
exact local target
-> AssurancePlan
-> one qualified deterministic local engine
-> EngineRun
-> normalized Finding/Evidence/Coverage
-> exact-target stale invalidation test
```

### AF-TB2 — unified review + security + test evidence

Requires S7 core.

```text
one synthetic change
-> logical review context
-> one validated security finding/reachability state
-> impacted test plan + execution evidence
-> shared finding/evidence graph
-> one AssuranceBundle
```

The acceptance oracle must prove that a clean reviewer/test does not erase a separately validated security finding.

### AF-TB3 — independent review and repair handoff

Requires S8.

```text
validated exact-target finding
-> independent review evidence
-> separately authorized repair Attempt
-> new exact target
-> old evidence stale
-> bounded reverification
-> finding VERIFIED_FIXED or still OPEN
```

### AF-TB4 — release/passport evidence

Requires S9.

```text
exact release target
-> RELEASE AssurancePlan
-> required evidence classes
-> residual limitations
-> Quality Passport / Evidence Timeline packet
-> Trusted Completion consumes but is not replaced by AssuranceBundle
```

## Required negative oracles

```text
NEW_HEAD_STALES_PRIOR_ACCEPTANCE_REVIEW
ENGINE_CRASH_IS_NOT_CLEAN
PARTIAL_SCAN_IS_NOT_SECURITY_PASS
UNKNOWN_REACHABILITY_IS_NOT_UNREACHABLE
COVERAGE_PERCENTAGE_IS_NOT_BEHAVIORAL_PROOF
RETRY_PASS_IS_NOT_CLEAN_PASS
ONE_VALIDATED_FINDING_SURVIVES_MULTIPLE_CLEAN_ENGINES
PR_CONTROLLED_RULE_CANNOT_DISABLE_CANONICAL_GATE
MODEL_ONLY_SECURITY_DOWNGRADE_DENIED
HOSTED_REVIEWER_UNAVAILABLE_DOES_NOT_DISABLE_LOCAL_ASSURANCE
LOCAL_PROJECT_OPEN_DOES_NOT_AUTHORIZE_DYNAMIC_SCAN
AUTHENTICATED_BROWSER_DOES_NOT_AUTHORIZE_DYNAMIC_SCAN
ASSURANCE_FINDING_DOES_NOT_GRANT_REPAIR_AUTHORITY
ASSURANCE_BUNDLE_DOES_NOT_GRANT_COMPLETION
SOURCE_AVAILABLE_DOES_NOT_ADMIT_DEPENDENCY
```
