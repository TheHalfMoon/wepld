# WePLD Native Assurance Fabric — Future Product / Architecture Plan

```text
STATUS = FUTURE_PLANNING_CANDIDATE
OWNER_SLICE = S7_NATIVE_REVIEW_AND_ASSURANCE
CROSS_SLICE_DEPENDENCIES = S3 + S4 + S5 + S6 + S8 + S9
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PROCESS_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
DYNAMIC_SECURITY_EXECUTION_AUTHORITY = NONE
ROADMAP_RENUMBERING = NONE
```

## 1. Product thesis

WePLD should not ship three unrelated features named code review, security, and testing. It should ship one native **Assurance Fabric** that can answer a stronger question:

> For this exact code/project/change identity, what engineering claims are currently supported by deterministic, graph-backed, test-backed, security-backed, and independently reviewed evidence; what remains unknown; and what evidence became stale when the target changed?

The primary user-facing intent surfaces are:

```text
/review
/security
/fulltest
```

They are profiles over the same evidence, planning, engine-adapter, freshness, and IDE surfaces. They do not create independent authority paths.

The product goal is an engineering-assurance operating system where a code change can be inspected, tested, attacked, traced, reviewed, repaired in a later authorized slice, and proven against one governed project truth without forcing the user to stitch together separate SaaS dashboards.

## 2. Why a shared fabric instead of three silos

A siloed design would duplicate project parsing, change identity, rules, findings, evidence storage, graph construction, IDE rendering, CI integration, staleness handling, and repair workflows. It would also make contradictions hard to reason about: a security scanner could call a path reachable while the test system says no relevant test exists, yet the product would have no common model in which to express that gap.

The shared fabric instead normalizes:

```text
one target identity
one Project/Code Graph owner
one evidence model
one finding lifecycle
one coverage model
one freshness model
one engine-adapter contract
one IDE assurance surface
one history/passport model
multiple assurance profiles and engines
```

This enables cross-domain questions that should become a WePLD differentiator:

```text
Is this vulnerability reachable from an exposed entrypoint?
Which tests cover that path?
Which change introduced or last modified the path?
Did the current test selection exercise the vulnerable behavior?
Which reviewer/scanner produced each claim?
Does a fix invalidate the previous review/security/test evidence?
Can the current exact head support the requested release/completion claim?
```

## 3. Roadmap ownership and non-bypass rules

The Assurance Fabric is primarily **S7 Native Review & Assurance**, but it consumes capabilities owned elsewhere. The owning slice must not pull those capabilities forward.

| Concern | Owning / prerequisite slice | Assurance use |
| --- | --- | --- |
| trusted process execution, command containment, timeouts, platform qualification | S3 | run local test/scanner/tool adapters only after exact process authority exists |
| Fehrest / Project Brain / Maemar code and architecture graph | S4 | canonical graph/context input; Assurance MUST NOT create a competing authoritative project graph |
| command normalization, Spec Kit, workflow intents, rules/plan qualification | S5 | `/review`, `/security`, `/fulltest` intent surfaces and plan construction |
| UWC/Mirefa/Edara/Nawat/Mission Runtime | S6 | qualify worker/tool routes and authorize effectful execution when needed |
| Native Review & Assurance / AMAN | S7 | Assurance Fabric core, findings, evidence normalization, review independence, static security, test evidence, reachability |
| bounded repair / retry / reassignment | S8 | consume validated findings and failed evidence; Assurance itself does not gain write/repair authority |
| Quality Passport / Evidence Timeline / recovery | S9 | durable assurance history, exact-target evidence, provenance, expiry/staleness, release/completion packets |

Controlling invariants:

```text
ASSURANCE_PLAN != EFFECT_AUTHORITY
ENGINE_AVAILABLE != ENGINE_AUTHORIZED
ENGINE_OUTPUT != TRUTH
ENGINE_OUTPUT != COMPLETION_DECISION
REVIEW_OUTCOME != COMPLETION_DECISION
SECURITY_FINDING != WRITE_AUTHORITY
TEST_PASS != TRUSTED_COMPLETION
COVERAGE_PERCENTAGE != BEHAVIORAL_PROOF
RETRY_PASS != CLEAN_PASS
FLAKY != PASS
MODEL_REVIEW != DETERMINISTIC_GATE
MULTIPLE_CLEAN_REVIEWERS != INVALIDATE_ONE_VALIDATED_FINDING
PROJECT_GRAPH_RELEVANCE != AUTHORITY
SOURCE_LICENSE != SOURCE_ADMISSION
SOURCE_ADMISSION != DEPENDENCY_ADMISSION
```

## 4. Stable user surfaces

### 4.1 `/review`

Purpose: review the exact requested change/project target for correctness, architecture, maintainability, spec/contract conformance, regressions, performance risk, test quality, and security-relevant engineering issues.

Planned forms:

```text
/review
/review --diff
/review --pr <ref>
/review --workspace
/review --architecture
/review --spec
/review --correctness
/review --performance
/review --security
/review --full
```

Core rules:

- bind every result to an immutable target identity;
- use Fehrest.Maemar context rather than isolated diff text when available and qualified;
- preserve independent-review semantics when the result is acceptance-critical;
- separate standards/correctness from spec-conformance where both apply;
- never let source-branch review configuration disable canonical review/security/authority policy;
- findings remain open until explicitly reconciled or invalidated by evidence;
- a changed exact head stales prior acceptance-critical review evidence unless explicit coverage accounting proves otherwise.

### 4.2 `/security`

Purpose: construct the minimum-sufficient security assurance plan for the requested scope and authority envelope.

Planned forms:

```text
/security --quick
/security --diff
/security --workspace
/security --sast
/security --secrets
/security --dependencies
/security --supply-chain
/security --sbom
/security --iac
/security --ci
/security --reachability
/security --threat-model
/security --dynamic
/security --deep
```

The command may combine deterministic rules, structural analysis, dependency/vulnerability evidence, reachability, CI/IaC checks, secret scanning, SBOM/provenance, and later dynamic/adversarial checks.

`--dynamic` is not a convenience alias for unrestricted network scanning. It requires future exact target authorization, network authority, containment, rate/budget limits, credential policy, template/plugin qualification, and attack-scope proof.

### 4.3 `/fulltest`

Purpose: build and, only when authorized, execute the **minimum sufficient assurance test plan** needed for the requested confidence claim.

It MUST NOT mean “blindly execute every repository command.”

Planned forms:

```text
/fulltest --quick
/fulltest --changed
/fulltest --standard
/fulltest --workspace
/fulltest --deep
/fulltest --release
/fulltest --adversarial
```

The plan can select among:

```text
format / style
compile / build
type-check
lint / static checks
unit
integration
contract / schema
snapshot / golden
property-based
coverage
mutation
fuzz
API/schema-driven
browser/E2E
security regression
platform-specific
formal/model checking
performance/regression
```

Selection is evidence-backed. Omitted categories must be visible with a reason such as `NOT_APPLICABLE`, `NOT_QUALIFIED`, `NOT_AUTHORIZED`, `BUDGET_EXCEEDED`, or `INSUFFICIENT_EVIDENCE_TO_SELECT`.

## 5. Assurance profiles

Profiles are policy/latency/risk envelopes, not separate engines.

```text
LIVE         = editor-safe, low-latency structural/rule checks; no surprise process/network effects
QUICK        = changed-file/change-impact focused local checks
WORKSPACE    = project-wide deterministic review/security/test plan within local authority
DEEP         = interprocedural graph/reachability, broader tests, dependency/security context, mutation/coverage where justified
ADVERSARIAL  = fuzz/property/mutation/dynamic security/browser/runtime attack-style checks under exact authority
RELEASE      = exact release/change claim packet with all required evidence classes and stale-evidence rejection
```

A profile must show:

```text
requested claim
exact target identity
included engines/check classes
omitted classes + reasons
estimated effect classes
process/network/filesystem/browser/provider requirements
budget/timeout envelope
freshness requirements
expected evidence outputs
```

## 6. Core domain contracts

The exact serialized form belongs to the future owning Spec Kit. This plan freezes semantic ownership only.

### 6.1 `AssuranceTarget`

Binds evidence to the exact object under assurance.

Candidate fields:

```text
project_id
repository_identity
workspace_generation
base_revision
head_revision
tree_identity
change_set_identity
worktree/session identity when applicable
spec/task/acceptance target identity
rule-pack identity
graph/index generation
platform/runtime identity when execution matters
```

No acceptance-critical evidence may silently float to another target.

### 6.2 `AssuranceIntent`

Normalized user/workflow request containing requested claim, scope, profile, explicit include/exclude constraints, maximum effect class, budget, and target.

`AssuranceIntent` is not process/network/write authority.

### 6.3 `AssurancePlan`

Deterministic/inspectable plan explaining what will run and why.

Candidate fields:

```text
intent_id
target_id
requested_claim
selected check classes
selected EngineDescriptor identities
input/context manifests
required effect classes
qualification requirements
budget/timeout/concurrency envelope
expected evidence types
omitted checks + reasons
staleness policy
plan-generation evidence
```

The IDE/CLI should be able to show the plan before effectful execution.

### 6.4 `EngineDescriptor`

Normalized description of an internal or external engine/adapter:

```text
engine_id
engine_version / pinned source or product identity
capabilities
input formats
output formats
language/ecosystem support
effect classes
process/network requirements
sandbox/containment requirements
configuration trust boundary
license/source-admission state
qualification evidence
known limitations
```

### 6.5 `EngineRun`

One immutable run over one exact target/context/engine identity with command/config identity, timestamps, environment, exit/result class, stdout/stderr evidence references, and coverage limitations.

### 6.6 `Finding`

One normalized engineering/security/test-quality concern.

Candidate fields:

```text
finding_id
finding_kind
severity
confidence / validation state
rule/check identity
primary location
related locations / flow path
symbol/resource identities
reachability state
engine producers
reproduction evidence
proof/counterexample evidence
first-seen target
last-verified target
status
suppression/acceptance decision + authority identity when applicable
```

Finding status candidates:

```text
CANDIDATE
VALIDATED
REJECTED_FALSE_POSITIVE
REQUIRES_MORE_EVIDENCE
OPEN
REPAIRED_PENDING_REVERIFY
VERIFIED_FIXED
ACCEPTED_RISK
SUPERSEDED
```

A finding is never deleted merely because a later engine is clean.

### 6.7 `EvidenceRef`

Durable pointer to exact source/run/log/test/trace/SARIF/SBOM/coverage/graph/browser evidence with producer identity, target binding, generation, hash/identity, freshness, and trust classification.

### 6.8 `CoverageClaim`

Coverage is multi-dimensional, not one percentage.

Candidate dimensions:

```text
changed files/symbols covered
reachable paths covered
rules/check classes executed
languages/ecosystems covered
tests selected/executed
statement/branch/function/region coverage when meaningful
mutation operators attempted/killed/survived
dependency inventory coverage
security-flow/reachability coverage
platform/runtime/browser coverage
reviewer context coverage
known exclusions / unsupported regions
```

### 6.9 `Reproduction`

Exact reproduction or counterexample linked to a finding/check with target, inputs, environment, command/action identity, observed output, minimization status, and repeatability.

### 6.10 `FixProposal`

Advisory repair proposal. It belongs to Assurance evidence but carries zero write authority. S8 may consume it only after a separately authorized Attempt.

### 6.11 `Reverification`

Links a prior finding/check to new exact-target evidence and records whether the claim is fixed, still present, changed, or inconclusive.

### 6.12 `AssuranceBundle`

A queryable packet of exact-target evidence for one requested claim. It can be consumed by Case rooms, Trusted Completion, release readiness, or S9 Quality Passport, but cannot itself make the completion decision.

## 7. Finding normalization and interchange

WePLD should own a richer internal schema and support adapters for existing formats rather than forcing every engine into a lowest-common-denominator representation.

Candidate interchange inputs/outputs:

```text
SARIF 2.1.x
JUnit XML / native test-event streams
coverage formats (LCOV/Cobertura/LLVM/native)
CycloneDX / SPDX SBOM
OSV vulnerability records
compiler/linter diagnostics
property/fuzz counterexamples
mutation reports
Playwright/browser traces
custom proof/model-checker evidence
```

SARIF is valuable as a static-analysis interchange boundary, but internal WePLD findings need additional exact-target, reachability, evidence, authority, reconciliation, and freshness fields.

## 8. Review architecture

### 8.1 Logical change view

Borrow the best product behavior from modern review systems without coupling WePLD to a hosted reviewer:

```text
raw diff
-> logical change groups
-> move/copy/refactor detection
-> changed symbols
-> callers/usages/dependencies
-> related implementations
-> explicit architecture/schema/spec context
-> repository + scoped review rules
-> relevant deterministic/test/security evidence
-> bounded Review Context Capsule
```

Fehrest owns canonical project/context graph facts. Assurance owns review orchestration/findings. AMAN owns security/risk evidence. Nawat owns effect-time authority.

### 8.2 Independent review

When review is acceptance-critical:

- implementer identity and reviewer identity must be distinct according to the owning qualification policy;
- reviewer context should not blindly inherit the builder's private chain/context; use the minimum sufficient evidence/context capsule;
- exact base/head/changed-file scope must be explicit;
- a changed head invalidates prior review unless explicit coverage reconciliation proves equivalence;
- unresolved material threads/findings block the applicable gate;
- review output remains untrusted external/tool/model data until validated/normalized.

### 8.3 Rule hierarchy

Candidate rule layers:

```text
canonical WePLD policy / security / authority rules
repository-level engineering rules
component/directory scoped rules
spec/task/acceptance rules
language/ecosystem rules
advisory team preferences / learned patterns
```

Lower scopes may specialize only where canonical policy permits. PR/source-branch configuration can add advisory context but may not weaken canonical gates.

## 9. Security architecture

### 9.1 Deterministic static foundation

Prioritize local/open deterministic coverage before AI-only security claims:

```text
structural SAST rules
secret/private-data detection
dependency/SCA vulnerability evidence
SBOM generation
license/policy checks
IaC/config checks
CI/workflow security checks
malicious/suspicious dependency/package signals
code/resource/taint reachability
security regression tests
```

### 9.2 Reachability as a first-class join

Security and tests should share graph evidence sufficient to express:

```text
vulnerable dependency/function
-> imported/reachable?
-> reachable from which application entrypoint/resource?
-> under which configuration/platform?
-> which changed symbol affects the route?
-> which tests exercise the route?
-> which tests omit it?
```

Ambiguous dynamic-language/reflection/runtime cases must remain conservative/unknown rather than fabricated unreachable.

### 9.3 Threat-model-derived scan plans

`/security --threat-model` should map assets, trust boundaries, entrypoints, identities, privileged effects, secrets, external inputs, dependency/supply-chain surfaces, browser/network surfaces, and recovery paths into explicit check requirements.

A model-generated threat model is candidate evidence; deterministic project facts and human/policy decisions still govern risk acceptance.

### 9.4 Supply-chain admission lab candidate

Future deep/adversarial assurance may inspect newly introduced packages in an isolated environment and record filesystem/process/network behavior. This is a future S3/S6/S7 capability and MUST NOT be implemented by silently running package install scripts on the user's host.

### 9.5 Dynamic security boundary

Future DAST/template/browser/API security execution requires:

```text
explicit target identity + proof of authorization
network authority
allowed origins/hosts/ports/protocols
credential source + least privilege + redaction rules
rate/concurrency/request/time budgets
safe default method set
scanner/template/plugin identity and qualification
code/template execution restrictions
sandbox/containment
forbidden external targets
stop conditions
request/response evidence policy
secret/PII handling
```

`LOCAL_PROJECT_OPEN` or `BROWSER_LOGGED_IN` never implies permission to attack/test a remote system.

## 10. Testing architecture

### 10.1 Impact-based test planning

`/fulltest --changed` should use qualified facts such as:

```text
changed files/symbols
call/reference graph
package/module ownership
build graph
test-to-symbol historical/coverage mapping
schema/API contract edges
runtime/platform metadata
prior failures/flakiness
security-sensitive affected paths
```

The plan should minimize work while maximizing recall for the requested confidence claim. A selection algorithm must expose why each test/check was selected or omitted.

### 10.2 Flakiness semantics

Retries are evidence, not erasure:

```text
FIRST_PASS
CONSISTENT_FAIL
RETRY_PASS_FLAKY
RETRY_FAIL
TIMEOUT
INFRA_FAILURE
NOT_RUN
```

`RETRY_PASS_FLAKY` MUST NOT normalize to a clean pass.

### 10.3 Test quality beyond coverage percentage

Use multiple signals where justified:

```text
statement/branch/function coverage
changed-line/changed-symbol coverage
mutation score and surviving mutants
property-based counterexamples
fuzz corpus/crash/minimization evidence
contract/schema edge cases
platform matrix
browser trace/network/console evidence
formal/model-checking proof/counterexample
performance distributions/regressions
```

A high line-coverage number alone must not establish test quality.

### 10.4 Adversarial test classes

Future deep assurance can combine mutation, property, fuzz, security regression, malformed input, race/concurrency, timeout/resource, crash recovery, permission, and browser/network failure injection under exact containment/effect authority.

## 11. IDE / Desktop product surface

The Assurance Fabric should feel native in the IDE and WePLD Desktop, not like links to external dashboards.

### 11.1 Primary Assurance view

Candidate navigation:

```text
Overview
Review
Security
Tests
Coverage
Findings
Evidence
History
```

### 11.2 Editor integration

Planned UX:

- gutter markers and diagnostics for findings;
- inline explanation with evidence, not only model prose;
- code-flow/reachability path visualization;
- “tests covering this symbol/path” view;
- quick filtered rerun for the current file/symbol/change;
- stale badge when the exact target changed;
- fix proposal action only as an advisory handoff to an authorized S8 workflow;
- suppress/accept-risk actions requiring explicit reason/authority according to policy;
- navigation from a finding to scanner output, test failure, graph edge, trace, or reproduction.

### 11.3 Finding card

A high-value finding card should include:

```text
severity + validation state
kind/rule
exact target revision
location + related flow locations
producer engines
reachability
why it matters
reproduction/proof
confidence + coverage limitations
related tests and whether they exercised the path
first-seen / last-verified target
reconciliation history
available next actions subject to authority
```

### 11.4 Test integration

Use native IDE test/diagnostic APIs where available rather than rebuilding generic IDE primitives. VS Code Testing API/Test Explorer and JetBrains inspection/test surfaces are adapter targets; WePLD remains the evidence/plan/authority owner.

## 12. Local-first / air-gap-first behavior

The baseline should remain useful with:

```text
no hosted reviewer
no remote model
no cloud security service
no remote telemetry requirement
no network
```

Local deterministic engines, local graph/context, local tests, local findings, and local evidence history should provide meaningful assurance.

Hosted reviewers/models/security services are optional adapters behind explicit egress classification, screening, provider-handling decisions where required, exact-scope approval, and exact-target result binding.

```text
REMOTE_REVIEWER_AVAILABLE != EGRESS_AUTHORIZED
REMOTE_MODEL_AVAILABLE != ASSURANCE_REQUIRED
OFFLINE_MODE != DEGRADED_AUTHORITY
```

## 13. Engine adapter architecture

Candidate flow:

```text
AssuranceIntent
  -> Target Resolver
  -> Fehrest/Project context + change-impact facts
  -> Assurance Planner
  -> Engine qualification / capability matching
  -> Nawat/effect decision when execution is effectful
  -> bounded EngineRun(s)
  -> parser/import adapters
  -> normalized Finding / EvidenceRef / CoverageClaim
  -> cross-engine correlation + reachability joins
  -> independent review where required
  -> AssuranceBundle
  -> S8 repair consumer / S9 passport consumer / Case room / user
```

Adapter requirements:

- exact engine identity/version;
- no hidden auto-install/update;
- no execution during mere discovery;
- bounded inputs/outputs;
- timeout/cancellation;
- stdout/stderr size limits and safe rendering;
- no trust in source-controlled scanner configuration unless qualified;
- explicit network/process/filesystem effects;
- stable parser or fail-closed unknown format;
- engine failure distinct from “no findings.”

## 14. Source acquisition and behavior-oracle strategy

WePLD should acquire solved machinery instead of recreating mature parsers/scanners/test runners, but every source still requires exact pin/license/provenance/use-boundary review before admission.

Priority research families:

### P0 — structural/local evidence foundation

```text
tree-sitter                 incremental syntax structure / IDE-safe parsing
ast-grep                    Rust structural search/rule/rewrite mechanics
reviewdog                   diff filtering + normalized diagnostic/reporting + SARIF bridge
Continue                    source-controlled checks/rules + CI behavior; existing WePLD registry family
CodeRabbit Skills           agent-review workflow/skill behavior; public source candidate
Trivy                       vulnerability/misconfig/secret/license/SBOM repository scanning
OSV-Scanner                 OSV/SCA source scanning + offline DB/remediation negative oracles
Syft                        SBOM generation / package inventory
zizmor                      GitHub Actions / workflow security analysis
OpenSSF Scorecard           repository/supply-chain posture checks
```

### P1 — deeper test/security assurance

```text
Semgrep                     multi-language static-analysis engine/rule ecosystem; license boundary must be reviewed
cargo-nextest               test execution/retry/flaky semantics
cargo-llvm-cov              Rust source-based coverage
cargo-mutants               mutation testing
Kani                        Rust model checking / proof/counterexample
Schemathesis                OpenAPI/GraphQL property-based API testing
Playwright                  browser/E2E test + trace behavior and IDE integration
```

### P2 — later adversarial/dynamic capability

```text
OpenSSF Package Analysis    sandboxed package-behavior analysis oracle
Nuclei                      template-driven network/application scanning; strict template/network authority required
OWASP ZAP                   DAST/web application scanning
```

### Product/behavior oracles, not assumed reusable hosted core source

```text
Aikido                      IDE + local/full scan split, reachability, SCA/SAST/secrets/IaC, supply-chain UX
Devin Review                logical change grouping, bug catcher, codebase-aware review, worktree/review UX
Devin Security              whole-codebase/threat-model/incremental/remediation behavior oracle
Greptile hosted core        graph-aware full-codebase review behavior; public edge only currently established in WePLD
Qodo                        context-aware multi-agent review and IDE/Git consistency behavior
```

A dedicated source-acquisition dossier in this Spec records the research matrix and negative oracles. None of these sources/services are admitted by this plan.

## 15. Negative-oracle quarry

The source study should preserve failures, not only happy-path features.

Candidate high-value oracles already identified:

```text
STALE_REVIEW_TASK_OR_RESULT_ID_MUST_NOT_APPLY_TO_NEW_HEAD
RETRY_PASS_MUST_REMAIN_FLAKY
ONE_VALIDATED_EXPLOIT_MUST_NOT_BE_VOTED_AWAY_BY_MULTIPLE_CLEAN_REVIEWERS
SOURCE_BRANCH_REVIEW_CONFIG_MUST_NOT_DISABLE_CANONICAL_GATES
OSV_REMEDIATION_OR_PACKAGE_MANAGER_MUST_NOT_EXECUTE_UNTRUSTED_SCRIPTS_WITHOUT_AUTHORITY
GLOBAL_PROXY_SHIM_MUST_NOT_BREAK_OR_CAPTURE_UNRELATED_CHILD_PROCESS_TRAFFIC
NUCLEI_TEMPLATE_OR_CODE_EXECUTION_MUST_NOT_BYPASS TEMPLATE/SOURCE/PROCESS/NETWORK_AUTHORITY
UNKNOWN_DYNAMIC_REACHABILITY_MUST_NOT_BE_REPORTED_UNREACHABLE
ENGINE_CRASH_MUST_NOT_NORMALIZE_TO NO_FINDINGS
PARSER_UNSUPPORTED_REGION_MUST_REMAIN COVERAGE_GAP
SARIF_OR_SCANNER_OUTPUT_MUST_BE TREATED_AS_UNTRUSTED_DATA
MALICIOUS_REPOSITORY_CONFIG_MUST_NOT CAUSE TOOL_INSTALL_OR_EXTERNAL_EGRESS
```

## 16. Threat model for the Assurance Fabric itself

The assurance subsystem is security-sensitive because it intentionally reads untrusted repositories and may later execute tools against them.

Threat classes to qualify:

```text
malicious source-controlled scanner/test config
prompt injection in source/comments/logs/findings
secret exfiltration through hosted reviewer/scanner/model
unsafe package-manager hooks
PATH/tool shadowing and executable substitution
symlink/path traversal and workspace escape
archive/decompression bombs
unbounded parser/regex/graph computation
scanner template/plugin/code execution
malformed SARIF/JUnit/SBOM/coverage payloads
terminal escape / log rendering attacks
network scanning outside authorized targets
credential reuse across targets
browser/session ambient authority
sandbox escape / host filesystem leakage
stale findings/evidence applied to a new head
cache poisoning / graph-generation mismatch
suppression or “accepted risk” forged by untrusted project content
engine version drift / silent auto-update
reviewer collusion or builder self-review satisfying independence
```

Every future implementation tranche involving these surfaces requires the canonical security-review policy in addition to correctness review.

## 17. Performance and resource policy

Assurance must remain usable during editing while still supporting deep checks.

Candidate budgets are benchmark targets, not frozen implementation numbers:

```text
LIVE: no surprise child processes/network; incremental parser/rule path only; editor-safe latency goal
QUICK: changed-scope bounded wall-clock/resource budget
WORKSPACE: explicit user-invoked project budget
DEEP: explicit larger budget with progress/cancellation and checkpointed evidence
ADVERSARIAL: explicit target/effect/budget authorization
RELEASE: deterministic completion-oriented plan, potentially composed of cached exact-target evidence plus fresh required checks
```

Cache reuse requires exact compatibility across target, engine, rule/config, environment, graph/index generation, and evidence freshness requirements. Cache hit is not a license to reuse stale evidence.

## 18. Quality and benchmark framework

Before automated promotion, define labeled corpora and predeclared thresholds.

### 18.1 Review quality

Measure by finding class:

```text
validated true positives
false positives
false negatives from seeded/held-out defects
abstentions / insufficient-context results
severity calibration
exact-head freshness failures caught
context coverage
repair/reverification success in later slices
```

### 18.2 Security quality

Use seeded known vulnerabilities/misconfigurations/secrets/dependency cases, reachable/unreachable/unknown cases, taint/resource flows, malicious CI/config, and supply-chain fixtures.

Report deterministic-engine contribution separately from AI reviewer contribution.

### 18.3 Test-plan quality

Measure:

```text
changed-defect detection recall
selected-vs-total test cost
missed impacted tests
flaky-test identification
mutation survival
coverage gaps
counterexample quality
platform/browser matrix adequacy
false confidence cases
```

A “fast” selector may not be promoted merely because it runs fewer tests.

### 18.4 Cross-engine evidence quality

Seed contradictory evidence:

- scanner finding + clean reviewer;
- clean static scan + failing security regression;
- high coverage + surviving mutant;
- retry pass + deterministic prior fail;
- vulnerability present but graph reachability unknown;
- old-head clean review + new-head code change.

The expected output is explicit conflict/uncertainty, not majority voting.

## 19. Delivery sequence

This sequence is dependency-ordered and does not activate itself.

### AF0 — Spec / Source Acquisition / evidence contracts

- finalize exact typed contracts;
- build source/behavior-oracle dossiers;
- create SARIF/test/SBOM/coverage fixture corpus;
- establish exact-target/freshness semantics;
- no donor execution.

### AF1 — Local deterministic assurance spine

After owning S3/S4/S7 gates:

- target resolver;
- AssurancePlan;
- engine registry/adapters;
- normalized findings/evidence;
- syntax/structural rules;
- test result normalization;
- dependency/SBOM/workflow-security adapters;
- exact-head invalidation.

### AF2 — IDE Live / Quick assurance

- diagnostics/gutter/problems surfaces;
- changed-scope plan;
- test explorer integration;
- evidence/finding card;
- stale target indicators;
- no surprise network/effects.

### AF3 — Graph / reachability / change-impact assurance

After Fehrest.Maemar foundations:

- symbol/call/reference/resource graph joins;
- test-to-code impact evidence;
- security reachability;
- Review Context Capsules;
- uncertainty handling for dynamic/unsupported regions.

### AF4 — Deep test/review/security orchestration

- coverage;
- mutation;
- property/API testing;
- model checking where applicable;
- multiple deterministic engines;
- independent review adapters;
- exact result reconciliation.

### AF5 — Adversarial / dynamic assurance

Only after process/network/browser/credential/containment authority:

- fuzzing;
- package behavior lab;
- DAST/API/browser security;
- dynamic target plans;
- explicit attack-scope evidence.

### AF6 — Controlled repair integration

Owned by S8:

- finding -> bounded Attempt proposal;
- authorized fix execution;
- mandatory reverification;
- no finding erasure;
- repair agent remains distinct from acceptance authority.

### AF7 — Quality Passport / Assurance history

Owned by S9:

- exact-target assurance bundles;
- evidence timeline;
- staleness/expiry;
- reusable release/completion packets;
- project assurance trend analytics without converting metrics into authority.

## 20. First tracer bullets

Future implementation should prove value with narrow slices rather than integrate every scanner immediately.

### TB-A — offline exact-head Review

```text
synthetic/local repository fixture
-> exact target
-> structural change facts
-> one deterministic rule engine
-> one independent reviewer adapter or fixture
-> normalized findings
-> exact-head staleness after one new commit
```

No network required.

### TB-B — offline Security

```text
fixture repo with seeded secret + dependency vulnerability + unsafe workflow
-> local deterministic adapters
-> normalized findings/SBOM/security evidence
-> reachability = KNOWN / UNKNOWN, never fabricated
-> exact finding reproduction/locations
```

### TB-C — FullTest change plan

```text
fixture repo with changed symbol + mapped tests + flaky test + surviving mutant fixture
-> impact plan
-> explicit selected/omitted tests
-> execution under bounded process authority
-> RETRY_PASS_FLAKY preserved
-> coverage/mutation evidence joined to change
```

### TB-D — unified Assurance view

One exact change intentionally produces:

```text
review concern
security finding
test failure
coverage gap
```

The UI must correlate them to one code path/target without collapsing the four evidence classes or voting one away.

## 21. Acceptance criteria for S7 Assurance Fabric maturity

A future S7 milestone is not complete until it can prove, for the qualified target classes:

1. every acceptance-critical result is bound to an exact target and becomes stale correctly;
2. engine failure/unsupported regions remain visible coverage gaps;
3. review/security/test evidence share normalized provenance and can be cross-linked;
4. Fehrest supplies project graph/context without Assurance creating a competing authority graph;
5. AMAN security evidence and Nawat effect authority remain distinct;
6. `/review`, `/security`, and `/fulltest` construct inspectable plans before effectful work;
7. no source-controlled config can disable canonical security/review/authority policy;
8. local/offline baseline remains useful;
9. hosted egress is explicit and policy-qualified;
10. deterministic findings cannot be overridden by reviewer majority without finding-specific evidence;
11. flaky/retry/test-infra states are not normalized to clean pass;
12. deep/dynamic engines cannot run before process/network/target/credential/template authority exists;
13. independent review requirements cannot be satisfied by the implementer;
14. repair proposals remain advisory until S8 grants a bounded Attempt;
15. S9 can consume exact AssuranceBundles with complete provenance/staleness metadata;
16. benchmark/negative-oracle thresholds are predeclared and measured by finding/check class rather than one aggregate score.

## 22. Explicit non-goals of this planning candidate

- no S2 implementation;
- no donor clone/install/execution;
- no source/dependency admission;
- no new process/network/browser/provider/model authority;
- no background remote scan;
- no default remote reviewer/model dependency;
- no generic “AI score” as completion/security quality;
- no auto-fix/write authority inside Assurance;
- no duplicate authoritative code/project graph;
- no implicit remote penetration testing;
- no claim that a product behavior oracle is reusable source;
- no claim that a license observed during research establishes final admission rights.

## 23. Product differentiation summary

If executed under the canonical roadmap, WePLD can offer a combination that current point tools usually split across products:

```text
local-first codebase-aware review
+ exact-head freshness
+ deterministic SAST/SCA/secrets/IaC/CI/supply-chain evidence
+ graph/reachability joins
+ impact-based full testing
+ coverage/mutation/property/fuzz/formal evidence
+ native IDE findings/evidence/history
+ independent reviewer semantics
+ optional governed hosted adapters
+ controlled repair in S8
+ Quality Passport in S9
+ one authority/evidence model across all of it
```

The moat is not “more scanners.” It is the governed, exact-target evidence graph connecting review, security, tests, code/architecture context, repair, and completion without allowing any producer to silently become authority.
