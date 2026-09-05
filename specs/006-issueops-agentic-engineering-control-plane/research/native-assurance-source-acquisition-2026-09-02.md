# Research — Native Assurance Fabric Source Acquisition / Behavior Oracles

```text
DATE = 2026-09-02
STATUS = RESEARCH_AND_FUTURE_SOURCE_ACQUISITION_INPUT_ONLY
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = PROHIBITED_BY_THIS_RECORD
DONOR_WORKFLOW_INSTALLATION = PROHIBITED_BY_THIS_RECORD
EXACT_PIN_AND_LICENSE_REVERIFICATION_AT_ADMISSION = REQUIRED
```

## 1. Purpose

This record turns the `/review`, `/security`, `/fulltest`, and IDE-assurance research into a future Source Acquisition queue. It distinguishes:

```text
SOURCE_DONOR_CANDIDATE      public source worth path-level mining after exact rights/provenance qualification
BEHAVIOR_ORACLE             product behavior worth learning/benchmarking; source reuse not assumed
TEST_QUARRY                 failure/edge-case patterns worth turning into WePLD negative oracles
INTERCHANGE_STANDARD        format/protocol worth supporting without adopting one engine
```

No item is admitted merely because it is open source, popular, installed elsewhere, or listed here.

## 2. Reuse policy

For every candidate actually needed by a future implementation tranche:

1. reverify exact repository/product identity;
2. pin exact revision/tree/artifact;
3. inspect exact license and material file-level exceptions;
4. classify source, dependency, build-tool, behavior-oracle, test-quarry, or reference-only use;
5. inspect only the minimum paths needed before considering broader acquisition;
6. verify transitive/build-time/native/runtime effects separately;
7. prohibit donor workflow/hook/installer execution during reconnaissance;
8. run security/provenance review appropriate to the change class;
9. record attribution/NOTICE obligations;
10. require a separate canonical source/dependency admission event before implementation use.

```text
LICENSE_OBSERVED != LICENSE_QUALIFIED
PUBLIC_REPOSITORY != SOURCE_ADMITTED
SOURCE_ADMITTED != DEPENDENCY_ADMITTED
BEHAVIOR_ORACLE != REIMPLEMENTATION_LICENSE
HOSTED_PRODUCT_FEATURE != PUBLIC_CORE_SOURCE
```

## 3. Priority matrix

### 3.1 P0 — local structural/evidence spine

#### tree-sitter

```text
UPSTREAM = https://github.com/tree-sitter/tree-sitter
ROLE = SOURCE_DONOR_CANDIDATE + BEHAVIOR_ORACLE
TARGET = incremental syntax parsing / editor-safe structural foundation
ADMISSION = NONE
```

Study/mining targets:

- incremental parsing fast enough for editor/live workflows;
- error-tolerant syntax trees during incomplete edits;
- language grammar boundary/loader design;
- changed-range/incremental update mechanics;
- Rust integration boundary.

WePLD use candidate: shared structural substrate for LIVE review/security rules and Fehrest facts where canonical architecture selects it. Tree-sitter facts remain syntax observations, not authority.

#### ast-grep

```text
UPSTREAM = https://github.com/ast-grep/ast-grep
ROLE = SOURCE_DONOR_CANDIDATE + BEHAVIOR_ORACLE
TARGET = Rust structural search / lint / rewrite rule mechanics over tree-sitter
ADMISSION = NONE
```

Study/mining targets:

- structural pattern/rule representation;
- language-independent matcher architecture;
- diagnostics/rule metadata;
- safe distinction between search/lint and rewrite;
- editor/CLI integration.

Negative oracle:

```text
STRUCTURAL_MATCH != REWRITE_AUTHORITY
```

#### reviewdog

```text
UPSTREAM = https://github.com/reviewdog/reviewdog
ROLE = SOURCE_DONOR_CANDIDATE + INTERCHANGE_BEHAVIOR_ORACLE
TARGET = diff-aware diagnostic filtering/reporting + SARIF-style bridges
ADMISSION = NONE
```

Study/mining targets:

- changed-line/diff filtering;
- severity/rule URL/message/location normalization;
- reporter abstraction;
- suggestion presentation;
- SARIF ingestion/output seams;
- fail-level semantics.

WePLD should adapt reporting/diff mechanics while keeping its richer internal Finding/Evidence schema.

#### Continue

```text
UPSTREAM = https://github.com/continuedev/continue
ROLE = EXISTING_WEPLD_SOURCE_FAMILY + SOURCE_DONOR_CANDIDATE + BEHAVIOR_ORACLE + TEST_QUARRY
EXISTING_WEPLD_PIN_OBSERVED = 5522c6f44ca0ac3528b37244818fbfa39b5af470
EXISTING_WEPLD_LICENSE_OBSERVED = Apache-2.0
ADMISSION = NONE_UNLESS_SEPARATELY_GRANTED_BY_CANONICAL_SOURCE_POLICY
```

Study/mining targets:

- source-controlled AI checks;
- repository rules as code/content;
- IDE/CI command/check UX;
- check result presentation and suggestions.

High-value negative oracle from public issue behavior study:

```text
CHECK_OR_TASK_RESULT_BOUND_TO_OLD_HEAD_MUST_NOT_BE_REUSED_AS_CURRENT_HEAD_EVIDENCE
```

Any exact issue/reference used in qualification must be reverified at use time.

#### CodeRabbit Skills

```text
UPSTREAM = https://github.com/coderabbitai/skills
ROLE = SOURCE_DONOR_CANDIDATE + BEHAVIOR_ORACLE
TARGET = review skill workflow / changed-scope review / review-fix-review mechanics
ADMISSION = NONE
```

Study/mining targets:

- review scope modes;
- severity grouping;
- fix/re-review workflow shape;
- agent integration boundaries;
- explicit treatment of remote review output as untrusted content.

Hosted CodeRabbit service remains separately governed by egress policy; public skills source does not establish rights to hosted core.

#### Trivy

```text
UPSTREAM = https://github.com/aquasecurity/trivy
ROLE = SOURCE_DONOR_CANDIDATE + ENGINE_ADAPTER_CANDIDATE + BEHAVIOR_ORACLE
TARGET = repository/image/filesystem vulnerability + misconfiguration + secret + license + SBOM evidence
ADMISSION = NONE
```

Study/mining targets:

- repository scan decomposition;
- package inventory/vulnerability joins;
- misconfiguration/secret result normalization;
- SBOM outputs;
- cache/database/offline behavior;
- language/ecosystem coverage limits.

#### OSV-Scanner

```text
UPSTREAM = https://github.com/google/osv-scanner
ROLE = SOURCE_DONOR_CANDIDATE + ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = OSV dependency vulnerability scanning / offline DB / remediation semantics
ADMISSION = NONE
```

High-value negative oracle:

Package-manager guided remediation may invoke package-manager behavior, scripts, registries, or project-controlled hooks. Therefore:

```text
REMEDIATION_PLAN != REMEDIATION_EXECUTION_AUTHORITY
PACKAGE_MANAGER_AVAILABLE != SAFE_TO_EXECUTE_UNTRUSTED_PROJECT
```

#### Syft

```text
UPSTREAM = https://github.com/anchore/syft
ROLE = SOURCE_DONOR_CANDIDATE + ENGINE_ADAPTER_CANDIDATE
TARGET = package inventory / SBOM generation / provenance formats
ADMISSION = NONE
```

Study/mining targets:

- filesystem/archive/image package cataloging;
- CycloneDX/SPDX output;
- cataloger/plugin boundaries;
- evidence identity/provenance;
- attestation-compatible output.

#### zizmor

```text
UPSTREAM = https://github.com/woodruffw/zizmor
ROLE = SOURCE_DONOR_CANDIDATE + ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = GitHub Actions / CI workflow security analysis
ADMISSION = NONE
```

Study/mining targets:

- template-injection checks;
- credential persistence/leakage;
- permissions/token scope;
- dangerous/confusable action refs;
- SARIF output and workflow-specific locations.

#### OpenSSF Scorecard

```text
UPSTREAM = https://github.com/ossf/scorecard
ROLE = SOURCE_DONOR_CANDIDATE + ENGINE_ADAPTER_CANDIDATE + BEHAVIOR_ORACLE
TARGET = repository/supply-chain security posture checks
ADMISSION = NONE
```

Potential Assurance evidence classes include branch protection, review practice, CI tests, SAST, security policy, signed releases, token permissions, and vulnerability posture. These are evidence signals, not a generic security score that becomes authority.

## 4. P1 — deeper static/test assurance

### Semgrep

```text
UPSTREAM = https://github.com/semgrep/semgrep
ROLE = ENGINE_ADAPTER_CANDIDATE + SOURCE_STUDY_CANDIDATE
TARGET = multi-language static-analysis engine + rule ecosystem
LICENSE_BOUNDARY = MUST_BE_REVERIFIED_EXACTLY_BEFORE_ANY_SOURCE_REUSE
ADMISSION = NONE
```

Study:

- source-like rule DSL;
- taint/dataflow behavior;
- result normalization;
- rule provenance/versioning;
- language support/unsupported-region semantics.

Do not assume hosted/proprietary product features are represented by the public engine.

### cargo-nextest

```text
UPSTREAM = https://github.com/nextest-rs/nextest
ROLE = ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = Rust test execution / retry / flaky semantics / reporting
ADMISSION = NONE
```

Primary behavior oracle:

```text
RETRY_PASS = FLAKY_EVIDENCE
RETRY_PASS != CLEAN_PASS
```

Study process-tree behavior, cancellation, partitions, profiles, JUnit/reporting, and platform semantics before integration.

### cargo-llvm-cov

```text
UPSTREAM = https://github.com/taiki-e/cargo-llvm-cov
ROLE = ENGINE_ADAPTER_CANDIDATE
TARGET = Rust LLVM source-based coverage
ADMISSION = NONE
```

Study changed-line/region/function/branch coverage extraction and platform/toolchain constraints. Coverage remains one typed evidence dimension.

### cargo-mutants

```text
UPSTREAM = https://github.com/sourcefrog/cargo-mutants
ROLE = ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = mutation testing / surviving mutant evidence
ADMISSION = NONE
```

Key product lesson:

```text
HIGH_LINE_COVERAGE != TEST_ASSERTION_QUALITY
SURVIVING_MUTANT = TEST_QUALITY_EVIDENCE
```

### Kani

```text
UPSTREAM = https://github.com/model-checking/kani
ROLE = ENGINE_ADAPTER_CANDIDATE + BEHAVIOR_ORACLE
TARGET = Rust model checking / proof and counterexample evidence
ADMISSION = NONE
```

Study proof harness identity, property/contracts, counterexamples, unsupported constructs, resource bounds, and difference between `PROVEN`, `COUNTEREXAMPLE`, and `INCONCLUSIVE/UNSUPPORTED`.

### Schemathesis

```text
UPSTREAM = https://github.com/schemathesis/schemathesis
ROLE = ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = OpenAPI/GraphQL property-based API testing
ADMISSION = NONE
```

Study generated case provenance, shrinking/reproduction, schema contract checks, stateful/API behavior, and exact target/network authority requirements.

### Playwright

```text
UPSTREAM = https://github.com/microsoft/playwright
ROLE = ENGINE_ADAPTER_CANDIDATE + IDE_BEHAVIOR_ORACLE + TEST_QUARRY
TARGET = browser/E2E tests, trace viewer, locator/test IDE behavior
ADMISSION = NONE
```

Study:

- deterministic browser-test identity;
- trace/network/console/source evidence;
- screenshot/timeline reproduction;
- VS Code testing/locator UX;
- browser/session/profile target identity;
- flake/retry behavior;
- containment/download/upload/network effects.

Browser test pass does not become Trusted Completion.

## 5. P2 — adversarial / dynamic security

### OpenSSF Package Analysis

```text
UPSTREAM = https://github.com/ossf/package-analysis
ROLE = SOURCE_DONOR_CANDIDATE + BEHAVIOR_ORACLE + TEST_QUARRY
TARGET = sandboxed dynamic package behavior analysis
ADMISSION = NONE
```

Study behavior capture for filesystem, commands/processes, network addresses, and changed behavior. The WePLD adaptation candidate is an isolated dependency-admission lab under explicit process/network/source authority.

### Nuclei

```text
UPSTREAM = https://github.com/projectdiscovery/nuclei
ROLE = ENGINE_ADAPTER_CANDIDATE + TEST_QUARRY
TARGET = template-driven application/network scanning
ADMISSION = NONE
```

Strong boundary:

```text
TEMPLATE_PRESENT != TEMPLATE_TRUSTED
TEMPLATE_MATCHER != TARGET_AUTHORITY
SCANNER_SERVICE_MODE != SAFE_DEFAULT
CODE_TEMPLATE_CAPABILITY != CODE_EXECUTION_AUTHORITY
```

Any future use requires explicit target/network/template/plugin/code-execution containment qualification.

### OWASP ZAP

```text
UPSTREAM = https://github.com/zaproxy/zaproxy
ROLE = ENGINE_ADAPTER_CANDIDATE + BEHAVIOR_ORACLE
TARGET = DAST / web application security scanning
ADMISSION = NONE
```

Study passive vs active scan boundaries, target/context definition, authentication/session handling, request budgets, alert normalization, and evidence capture.

## 6. Product / hosted behavior oracles

These sources are primarily used to learn product behavior, UX, benchmark expectations, and negative oracles. Public reusable hosted core source is not assumed.

### Aikido

```text
ROLE = BEHAVIOR_ORACLE + TEST_QUARRY
HOSTED_CORE_SOURCE = NOT_ASSUMED
```

Behavior targets:

- IDE live SAST/secrets/IaC experience;
- changed-file vs whole-workspace/full-context scan separation;
- dependency/function/contextual reachability;
- local scanner/offline privacy posture;
- AutoTriage/AutoFix UX while preserving WePLD authority separation;
- agent/MCP security-check interaction;
- package/supply-chain safety UX.

Negative-oracle quarry includes proxy/shim side effects from package-safety tooling: global proxy environment inherited by child processes can break unrelated/non-target traffic. WePLD should prefer scoped adapters/explicit process environments over global invisible mutation.

### Devin Review

```text
ROLE = BEHAVIOR_ORACLE
HOSTED_CORE_SOURCE = NOT_ASSUMED
```

Behavior targets:

- logical diff grouping;
- copy/move/refactor awareness;
- severity/confidence-oriented Bug Catcher UX;
- full-codebase context chat;
- isolated worktree review workflow;
- review -> fix -> re-review loop as a later S8 consumer;
- reviewer/build-context independence.

### Devin Security

```text
ROLE = BEHAVIOR_ORACLE
HOSTED_CORE_SOURCE = NOT_ASSUMED
```

Behavior targets:

- whole-codebase scans;
- threat-model-derived scan profiles;
- exploitability validation;
- incremental changed-code security scans;
- remediation proposal/PR workflow.

Vendor benchmark claims are product-oracle evidence only and MUST NOT become WePLD benchmark ground truth.

### Greptile

Existing WePLD enrichment remains authoritative research context:

`docs/acquisition/GREPTILE_ENRICHMENT.md`

Current bounded mapping already states:

```text
PRIMARY_OWNER_CANDIDATE = Assurance
CONTEXT_OWNER = Fehrest
SECURITY_FINDING_OWNER = AMAN when implemented
EFFECT_AUTHORITY = Nawat only
REPAIR_AUTHORITY = separate authorized Attempt only
```

Preserve its Review Context Capsule, cascading rules, cross-repo access gating, source-branch-config distrust, and learning-cannot-self-promote negative oracles.

### Qodo

```text
ROLE = BEHAVIOR_ORACLE
HOSTED_CORE_SOURCE = NOT_ASSUMED
```

Behavior targets:

- multi-agent/context-aware review;
- consistent standards/context across IDE and Git review surfaces;
- full-repository context engine concepts;
- enterprise/local/on-prem deployment behavior as an exit/privacy oracle where officially supported at use time.

Any public Qodo/PR-agent-related source considered for reuse requires exact current repository/license verification; no license claim is frozen by this document.

## 7. Interchange / platform standards and APIs

### SARIF

```text
ROLE = INTERCHANGE_STANDARD
TARGET = static-analysis result interchange
```

Support as import/export/report bridge where useful. Internal WePLD Finding/Evidence models remain richer and preserve target/freshness/reachability/reconciliation/authority fields.

### OSV

```text
ROLE = INTERCHANGE_STANDARD
TARGET = vulnerability record identity/ecosystem/version evidence
```

### CycloneDX / SPDX

```text
ROLE = INTERCHANGE_STANDARD
TARGET = SBOM inventory/provenance interchange
```

### VS Code Testing API / diagnostics

```text
ROLE = IDE_PLATFORM_API_BEHAVIOR_ORACLE
TARGET = native test explorer/run/debug/coverage/diagnostic integration
```

WePLD should adapt through platform APIs rather than recreate generic editor test UI primitives.

### JetBrains inspections/test surfaces

```text
ROLE = IDE_PLATFORM_API_BEHAVIOR_ORACLE
TARGET = native inspection/problems/test integration
```

Exact APIs/version compatibility are reverified when an owning IDE adapter tranche activates.

## 8. Negative-oracle register

Future source acquisition should convert these into deterministic fixtures before relying on the corresponding capability.

```text
AF-N001 OLD_HEAD_RESULT_NOT_CURRENT
AF-N002 SOURCE_BRANCH_REVIEW_CONFIG_CANNOT_DISABLE_CANONICAL_GATES
AF-N003 VALIDATED_FINDING_CANNOT_BE_VOTED_AWAY
AF-N004 RETRY_PASS_REMAINS_FLAKY
AF-N005 ENGINE_CRASH_OR_TIMEOUT_NOT_NO_FINDINGS
AF-N006 UNSUPPORTED_REGION_REMAINS_COVERAGE_GAP
AF-N007 UNKNOWN_DYNAMIC_REACHABILITY_NOT_UNREACHABLE
AF-N008 PACKAGE_REMEDIATION_NOT_PACKAGE_MANAGER_EXECUTION_AUTHORITY
AF-N009 PACKAGE_INSTALL_HOOKS_NEVER_IMPLICITLY_EXECUTED_DURING_SCAN
AF-N010 GLOBAL_PROXY_SHIM_MUST_NOT_CAPTURE_UNRELATED_CHILD_PROCESS_TRAFFIC
AF-N011 SARIF_JUNIT_SBOM_COVERAGE_OUTPUT_IS_UNTRUSTED_DATA
AF-N012 MALICIOUS_RULE_CONFIG_CANNOT_INSTALL_OR_EXECUTE_TOOLS
AF-N013 NUCLEI_TEMPLATE_OR_PLUGIN_NOT_EXECUTION_AUTHORITY
AF-N014 DAST_TARGET_DISCOVERED_NOT_TARGET_AUTHORIZED
AF-N015 AUTHENTICATED_BROWSER_NOT_SECURITY_TEST_AUTHORITY
AF-N016 HIGH_COVERAGE_NOT_TEST_QUALITY_PROOF
AF-N017 SURVIVING_MUTANT_MUST_REMAIN_VISIBLE
AF-N018 MODEL_CLEAN_REVIEW_NOT_DETERMINISTIC_SECURITY_PASS
AF-N019 REMOTE_REVIEWER_AVAILABLE_NOT_EGRESS_AUTHORIZED
AF-N020 TOOL_FOUND_ON_PATH_NOT_QUALIFIED_ENGINE_IDENTITY
AF-N021 SILENT_ENGINE_AUTOUPDATE_FORBIDDEN_FOR_ACCEPTANCE_EVIDENCE
AF-N022 GRAPH_INDEX_STALE_NOT_CURRENT_REACHABILITY_EVIDENCE
AF-N023 CLEAN_STATIC_SCAN_NOT_OVERRIDE_FAILING_SECURITY_REGRESSION
AF-N024 REVIEWER_IS_IMPLEMENTER_NOT_INDEPENDENT_ACCEPTANCE_REVIEW
AF-N025 TEST_SELECTION_FAST_NOT_TEST_SELECTION_QUALIFIED
AF-N026 EXTERNAL_VENDOR_BENCHMARK_NOT_WEPLD_ACCEPTANCE_BENCHMARK
```

## 9. Donor-execution prohibition during reconnaissance

Until exact source/dependency/build-tool authority exists:

```text
NO npm/pnpm/yarn install
NO pip/uv install
NO cargo install/build/test of donor
NO donor GitHub Actions/workflows
NO pre-commit/hooks
NO package-manager remediation
NO browser extension installation
NO scanner template/plugin execution
NO remote scanning/API calls
NO donor MCP server execution
```

Read-only source/documentation/provenance inspection is the default research posture.

## 10. Source-acquisition order

When S7 approaches activation, prefer the minimum useful stack:

```text
1. syntax/structure + reporting/interchange
2. test-result normalization
3. SBOM/dependency/workflow-security evidence
4. exact-head/freshness + IDE surface
5. Fehrest graph/reachability joins
6. coverage/mutation/property/model-checking adapters
7. optional external independent reviewers after egress qualification
8. dynamic/adversarial scanners only after process/network/browser/target authority
```

Do not admit multiple overlapping engines merely to maximize tool count. For each capability class, compare maintenance, determinism, platform support, license, output quality, security surface, and exit strategy, then choose the minimum sufficient set.
