# Spec Addendum — Native Assurance Fabric

```text
STATUS = FUTURE_PLANNING_SPEC_ADDENDUM
PARENT = SPEC_006_ISSUEOPS_AGENTIC_ENGINEERING_CONTROL_PLANE
PRIMARY_ROADMAP_OWNER = S7_NATIVE_REVIEW_AND_ASSURANCE
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PROCESS_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
ROADMAP_REMAP = NONE
```

## Problem

Code review, security scanning, and test execution are normally fragmented across unrelated tools, result formats, dashboards, freshness semantics, and authority models. This creates false confidence when one system reports green while another result is stale, unsupported, failed to run, or refers to a different code revision.

WePLD needs one native assurance plane that can bind review, security, testing, graph/reachability, and evidence to the same exact project/change identity while preserving independent review, deterministic gates, effect authority, repair authority, and Trusted Completion as separate concepts.

## Product outcome

A user can invoke `/review`, `/security`, or `/fulltest` from WePLD or a supported IDE surface and receive an inspectable assurance plan, an exact-target evidence bundle, and a typed assessment of the exact requested claim. The system can correlate findings across code context, security reachability, selected tests, coverage, mutation/property/fuzz/formal evidence, CI state, and independent review without allowing any engine, model, scanner, test runner, or majority vote to become completion authority.

## Functional requirements

### AF-FR001 — One shared Assurance Fabric

WePLD MUST implement `/review`, `/security`, and `/fulltest` as profiles over one shared Assurance Fabric rather than three unrelated evidence systems.

The shared fabric MUST own normalized target binding, planning, engine descriptors/runs, findings, evidence references, coverage claims, freshness/staleness, correlation, claim assessment, and AssuranceBundle production.

### AF-FR002 — Exact assurance target

Every acceptance-critical assurance artifact MUST bind the exact target identity required by its claim, including exact base/head/tree/change identity and relevant workspace-material/graph/rule/environment generations where applicable.

Workspace assurance MUST account for material uncommitted/untracked/nested/generated state according to the owning target policy; a commit SHA alone is insufficient when that state affects the claim.

A material target change MUST invalidate prior evidence unless a separately defined compatibility proof establishes equivalence for that evidence class.

```text
NEW_EXACT_HEAD -> PRIOR_HEAD_ACCEPTANCE_EVIDENCE_STALE
```

### AF-FR003 — Stable command surfaces

The future native command surface MUST include:

```text
/review
/security
/fulltest
```

Commands MUST normalize user intent into `AssuranceIntent`. A command invocation MUST NOT itself grant process, filesystem, network, browser, provider, model, credential, Git, repair, or completion authority.

### AF-FR004 — Inspectable plan before effectful execution

Before an assurance action performs an effectful engine run, WePLD MUST be able to produce an inspectable `AssurancePlan` containing:

- requested claim and exact target;
- exact `AssurancePolicySnapshot`;
- selected check classes and engines;
- selected context/input manifests;
- required/conditional/optional classification for each check;
- required effect classes and qualifications;
- timeout/resource/budget envelope;
- expected evidence outputs;
- omitted checks and explicit reasons;
- freshness policy.

No required check may be silently omitted.

### AF-FR005 — Minimum-sufficient `/fulltest`

`/fulltest` MUST mean “construct the minimum-sufficient qualified assurance test plan for the requested confidence claim.” It MUST NOT blindly execute every project command, script, test, package-manager hook, or discovered tool.

Impact selection SHOULD use qualified changed-file/symbol, reference/call graph, package/build graph, test mapping, coverage history, runtime/platform, and risk evidence where available.

A budget or availability limit MUST NOT silently downgrade required evidence. If a required check cannot run, the requested claim becomes blocked/inconclusive/not-supported according to the exact policy snapshot.

### AF-FR006 — Typed test outcomes

Test normalization MUST preserve at least:

```text
FIRST_PASS
CONSISTENT_FAIL
RETRY_PASS_FLAKY
RETRY_FAIL
TIMEOUT
INFRA_FAILURE
CANCELLED
NOT_RUN
UNSUPPORTED
```

`RETRY_PASS_FLAKY`, `INFRA_FAILURE`, `NOT_RUN`, or `UNSUPPORTED` MUST NOT normalize to a clean pass.

Known-flake/quarantine state MUST have owner/evidence/scope/expiry or review date and MUST NOT erase the underlying failure observation.

### AF-FR007 — Test quality beyond line coverage

The architecture MUST support typed evidence for coverage, changed-region coverage, mutation testing, property-based tests, fuzzing, API/schema testing, browser/E2E traces, platform matrices, formal/model checking, performance regressions, and other qualified assurance classes.

A high line-coverage percentage MUST NOT by itself establish test quality or completion.

### AF-FR008 — Normalized findings without majority erasure

A validated finding MUST remain durable until finding-specific reconciliation evidence establishes a new state such as false positive, verified fixed, accepted risk, or superseded.

Multiple clean reviewers or scanners MUST NOT erase one independently validated finding merely by majority vote.

### AF-FR009 — Independent review semantics

When review is acceptance-critical, the implementer MUST NOT satisfy its own independent-review requirement.

Review evidence MUST preserve reviewer/producer identity, qualification, independence, exact target, covered scope, findings, and coverage limitations. Reviewer scope/context coverage SHOULD be represented as a typed `CoverageClaim` rather than prose only.

Reviewer context MAY consume a bounded Fehrest-derived Review Context Capsule but MUST NOT automatically inherit builder-private reasoning or become authority.

### AF-FR010 — Review axes

Assurance MUST be able to represent distinct review axes including correctness/engineering standards and spec/contract conformance where applicable. Architecture, performance, maintainability, testing, and security concerns MAY be additional typed axes.

A clean axis MUST NOT silently imply a clean result for an unexecuted or unsupported axis.

### AF-FR011 — Fehrest.Maemar context ownership

Fehrest.Maemar MUST remain the canonical project/code/architecture graph owner. Assurance MUST consume qualified graph/context facts through stable interfaces rather than create a competing authoritative project graph.

Graph relevance or retrieval score MUST remain evidence, not authority or truth.

### AF-FR012 — AMAN security evidence ownership

Security/risk findings produced by Assurance MUST map into AMAN-owned security evidence when AMAN is implemented. Assurance orchestration MUST NOT collapse security evidence ownership into effect authorization.

```text
SECURITY_FINDING != NAWAT_GRANT
```

### AF-FR013 — Deterministic security baseline

The security profile SHOULD support, through qualified engines/adapters, deterministic evidence classes including:

```text
SAST / structural rules
secrets/private-data detection
SCA/dependency vulnerabilities
SBOM/package inventory
license/policy checks
IaC/config checks
CI/workflow checks
supply-chain/package signals
graph/taint/resource reachability
security regression tests
```

AI/model review MAY supplement these classes but MUST NOT replace required deterministic coverage.

### AF-FR014 — Reachability states are explicit

Reachability MUST distinguish at least:

```text
REACHABLE
UNREACHABLE_PROVEN
CONDITIONALLY_REACHABLE
UNKNOWN_DYNAMIC
UNKNOWN_UNSUPPORTED
NOT_APPLICABLE
```

Unknown MUST NOT be reported as unreachable.

Reachability evidence MUST record graph/index/runtime assumptions and generation.

### AF-FR015 — Security/test graph joins

Where evidence exists, WePLD SHOULD correlate a security finding or vulnerable dependency/function with exposed entrypoints/resources, changed symbols, and tests that do or do not exercise the relevant route.

A missing test-path mapping MUST remain an explicit coverage gap rather than being inferred away.

### AF-FR016 — Threat-model-derived assurance plans

`/security --threat-model` SHOULD produce a threat-model-derived scan plan using qualified project facts about assets, trust boundaries, entrypoints, identities, privileged effects, secrets, external inputs, dependencies, CI, browser/network surfaces, and recovery paths.

Model-generated threat claims remain candidate evidence and cannot authorize risk acceptance.

### AF-FR017 — Dynamic security is separately authorized

Dynamic security/DAST/API/browser/network testing MUST remain disabled until the owning slices provide exact target authorization, process/network/browser authority, containment, credential handling, rate/request/time budgets, scanner/template/plugin qualification, stop conditions, and evidence policy.

```text
LOCAL_PROJECT_OPEN != REMOTE_SECURITY_TEST_AUTHORITY
AUTHENTICATED_BROWSER != REMOTE_SECURITY_TEST_AUTHORITY
SCANNER_TARGET_DISCOVERED != SCANNER_TARGET_AUTHORIZED
```

### AF-FR018 — Engine discovery has no execution side effect

Finding a scanner/test tool/configuration in PATH, a repository, an IDE, a manifest, or a package manager MUST NOT automatically install, update, configure, or execute it.

Every engine used for acceptance-critical evidence MUST have a qualified exact executable/artifact/runtime identity and effect profile, not only a matching version string.

### AF-FR019 — Engine failure is not clean evidence

Engine crash, parser failure, timeout, cancellation, unsupported language/region, missing database, missing credential, blocked network, resource-limit breach, incomplete cleanup, or infrastructure failure MUST remain an explicit run/coverage state. None may normalize to `NO_FINDINGS` or `PASS`.

### AF-FR020 — Source-controlled configuration is untrusted

Repository/PR/source-branch scanner, review, test, rule, template, plugin, workflow, or tool configuration MUST carry provenance/trust classification and deterministic precedence.

A proposed change MUST NOT be able to weaken canonical review, security, authority, egress, or acceptance requirements for itself. A configuration conflict without a defined merge/precedence rule MUST fail explicitly rather than use generic latest-write-wins.

### AF-FR021 — Local-first useful baseline

WePLD MUST retain a meaningful local/offline assurance baseline without requiring a hosted reviewer, remote model, cloud security service, remote telemetry, or network connection.

Hosted services MAY be optional adapters after egress and provider qualification.

### AF-FR022 — Hosted egress is explicit

Any hosted reviewer/scanner/model or external assurance service MUST obey `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` and preserve exact scope, classification, screening, redactions, approval, provider/product identity, exact target, and coverage limitations.

External output MUST enter WePLD as untrusted evidence, not authority.

### AF-FR023 — Interchange without lowest-common-denominator ownership

Assurance SHOULD support qualified adapters for formats such as SARIF, JUnit/native test events, coverage formats, CycloneDX/SPDX, OSV, browser traces, mutation reports, fuzz counterexamples, and proof/model-checker results.

WePLD MUST retain a richer internal Finding/Evidence model where exact target, reachability, freshness, authority, reconciliation, handling, and coverage semantics exceed an interchange format.

### AF-FR024 — Native IDE assurance surface

Supported IDE/Desktop surfaces SHOULD expose native Assurance views for Review, Security, Tests, Coverage, Findings, Evidence, History, and the current exact claim assessment, with gutter/inline diagnostics and exact-target stale indicators.

IDE actions MUST remain routed through core authority/evidence contracts.

```text
IDE_CLICK_RUN != EXECUTION_AUTHORITY
IDE_QUICK_FIX != WRITE_AUTHORITY
IDE_SUPPRESS != ACCEPTED_RISK
IDE_TEST_GREEN != TRUSTED_COMPLETION
GENERIC_GREEN_ICON != CLAIM_ASSESSMENT
```

### AF-FR025 — Finding card evidence

A material finding presentation SHOULD expose severity, validation state, rule/kind, exact target, locations/flow, producers, reachability, reproduction/proof, coverage limitations, related tests, first-seen/last-verified identities, reconciliation/disposition history, and authorized next-action availability.

### AF-FR026 — Repair remains S8-owned

Assurance MAY produce a `FixProposal` but MUST NOT gain write/repair authority. S8 MAY consume validated findings/proposals only through a separately authorized `Attempt`, followed by exact-target reverification.

Finding history MUST NOT be erased by repair.

### AF-FR027 — Assurance history remains S9-owned

S9 Quality Passport/Evidence Timeline SHOULD consume exact `AssuranceBundle` records including provenance, target identity, policy snapshot, producer versions, findings, coverage gaps, conflicts, claim assessment, and freshness/expiry state.

A historical supported claim MUST remain historical after a target or material engine/rule/policy/environment change.

### AF-FR028 — Cross-engine conflicts remain visible

Assurance MUST preserve contradictory evidence, including cases such as:

- clean reviewer + validated scanner finding;
- clean static scan + failing security regression;
- high coverage + surviving mutant;
- retry pass + earlier deterministic failure;
- dependency vulnerability + unknown reachability;
- old-head clean review + new-head code change.

Contradiction SHOULD produce explicit conflict/uncertainty, not majority voting.

### AF-FR029 — Predeclared benchmark promotion

Before an engine, selector, reviewer, reachability model, test planner, or security classifier is promoted to acceptance-critical use, the owning gate MUST define the relevant labeled corpus, negative oracles, metrics, and promotion thresholds before evaluation.

Vendor benchmark claims or aggregate scores MUST NOT substitute for WePLD qualification evidence.

### AF-FR030 — Review-quality metrics

Review qualification SHOULD report finding-class true positives, false positives, false negatives from seeded/held-out defects, abstentions, severity calibration, exact-head freshness failures caught, context coverage, and unsupported regions.

### AF-FR031 — Security-quality metrics

Security qualification SHOULD include seeded known vulnerabilities, secrets, dependency cases, reachable/unreachable/unknown flows, malicious CI/config, supply-chain fixtures, and coverage gaps. Deterministic-engine contribution SHOULD be reported separately from AI/model contribution.

### AF-FR032 — Test-plan quality metrics

Impact-based test planning SHOULD report changed-defect detection recall, selected-vs-total cost, missed impacted tests, flaky identification, mutation survival, coverage gaps, counterexample quality, and platform/browser adequacy where applicable.

Running fewer tests is not by itself a successful selector outcome.

### AF-FR033 — Assurance subsystem threat model

Future implementation MUST explicitly threat-model malicious repository configuration, prompt injection, secret exfiltration, package hooks, executable shadowing, symlink/path escape, archive/parser/resource attacks, malicious scanner templates/plugins, malformed result formats, terminal/log rendering, unauthorized network targets, credential reuse, browser ambient authority, sandbox escape, stale evidence, cache poisoning, forged suppressions, silent engine update, and reviewer-independence failure.

### AF-FR034 — Bounded engine execution

Effectful engine runs MUST support explicit timeout/cancellation, bounded output/log handling, process-tree termination, resource/budget limits appropriate to the engine, temporary-artifact cleanup, minimized inherited environment/credentials, concurrency arbitration, and deterministic distinction between engine failure and check failure.

### AF-FR035 — No hidden engine auto-update

Acceptance-critical evidence MUST bind the actual executable/artifact/version/rule/database/template/config identity used. Silent automatic updates that change any material identity MUST invalidate or requalify affected evidence.

### AF-FR036 — Assurance profiles

The architecture SHOULD support policy-defined profiles such as:

```text
LIVE
QUICK
WORKSPACE
DEEP
ADVERSARIAL
RELEASE
```

Profiles MUST have versioned policy identities and define allowed effects, expected evidence, required/conditional/optional checks, budgets, staleness requirements, and omitted-check behavior. `LIVE` MUST default to editor-safe behavior without surprise process/network effects.

### AF-FR037 — Source acquisition before reinvention

For mature solved machinery, WePLD MUST prefer Source Acquisition and qualified adapters/reuse over rebuilding scanners, parsers, test runners, or interchange machinery from scratch when reuse is legally, architecturally, and operationally justified.

Listing a candidate source in research MUST NOT admit it.

### AF-FR038 — Minimum engine set

The owning tranche SHOULD choose the minimum sufficient non-overlapping engine set based on determinism, maintenance, platform support, license, evidence quality, security surface, offline behavior, and exit strategy rather than maximizing scanner/tool count.

### AF-FR039 — Quality claim is explicit

Every `AssuranceBundle` consumed by a user, acceptance, or release gate MUST identify the requested claim and contain a typed `ClaimAssessment`. A generic green icon or aggregate “quality score” MUST NOT stand in for an explicit claim and its required evidence.

### AF-FR040 — Trusted Completion remains separate

No `ClaimAssessment`, test pass, clean scan, clean reviewer, high coverage, no-open-findings state, merged PR state, or AssuranceBundle creation may directly set Trusted Completion without the owning completion decision boundary.

### AF-FR041 — Typed claim assessment

Assurance MUST represent the outcome of the exact requested claim using at least:

```text
SUPPORTED
NOT_SUPPORTED
PARTIALLY_SUPPORTED
INCONCLUSIVE
BLOCKED
STALE
```

The assessment MUST bind the exact target and policy snapshot and preserve required evidence, satisfied evidence, missing evidence, blocking findings, conflicts, coverage gaps, stale evidence, residual limitations, and rationale.

Missing/stale required evidence or unresolved blocking findings MUST prevent `SUPPORTED`.

### AF-FR042 — Immutable assurance policy snapshot

Every acceptance/release-relevant plan and claim assessment MUST bind an immutable `AssurancePolicySnapshot` containing the exact profile-policy version, claim schema, required/conditional/optional evidence rules, canonical policy refs, rule-pack identity, conflict/staleness/disposition rules, and benchmark thresholds used.

A later policy change MUST NOT silently reinterpret a historical bundle.

### AF-FR043 — Finding correlation and governed disposition

Assurance MUST support stable finding fingerprints/correlation without collapsing producer evidence. Accepted-risk, suppression, false-positive, rule-exception, fixed, and superseded dispositions MUST bind exact scope, reason, target/policy, authority/decision evidence, and expiry/review date where applicable.

Untrusted repository configuration MUST NOT forge, broaden, or indefinitely extend a disposition.

### AF-FR044 — Evidence handling and privacy

Durable evidence MUST carry content/trust classification, access-policy reference, handling-policy reference, redaction state, retention/expiry state, and freshness.

Handling policy MUST cover visibility, storage/encryption requirements where applicable, redaction, retention/tombstone, export/egress, and safe rendering. Secret/private browser/network/log/source content MUST NOT become a durable secondary leak merely because it is evidence.

### AF-FR045 — Exact engine artifact and resource identity

Acceptance-critical `EngineRun` MUST bind the actual resolved executable/runtime/artifact identity and digest where available, plus material rule/database/template/config snapshots and resource envelope. PATH discovery or a matching version string alone is insufficient qualification evidence.

### AF-FR046 — Performance evidence is statistically/environmentally qualified

A material performance claim MUST bind benchmark identity, baseline target, hardware/runtime identity, fixture/data identity, warmup/repetition policy, sample/noise summary, threshold/decision rule, and explicit inconclusive states.

One noisy wall-clock sample MUST NOT become a performance regression or clean-performance claim.

### AF-FR047 — Required-check monotonicity

For the same target/risk class, a stronger assurance/release claim MUST NOT silently select a strictly weaker required evidence set than a weaker profile. Evidence substitution requires an explicit policy-defined compatibility/equivalence rule and supporting evidence.

### AF-FR048 — Configuration precedence is deterministic

The assurance policy MUST define precedence/merge rules across canonical, trusted repository, component/spec, source-branch proposed, provider, and user-session configuration. Undefined conflict produces explicit plan/config failure rather than latest-write-wins.

### AF-FR049 — Review coverage is explicit evidence

Acceptance-critical independent review MUST preserve the exact reviewed base/head/file scope and a typed review-context/scope coverage claim sufficient to expose omitted or unsupported regions. Reviewer confidence or prose that the review was “comprehensive” is not coverage proof by itself.

### AF-FR050 — Evidence-store evolution and recovery

Before S9 treats Assurance history as durable project memory, the owning implementation MUST qualify schema migration, backup/restore, corruption/partial-migration behavior, redaction/tombstone propagation, and reconstruction of the exact policy/target/evidence graph supporting a historical decision.

## Non-goals

This addendum does not authorize:

- S2 implementation;
- donor code/workflow/hook execution;
- package installation or dependency admission;
- process/network/browser/provider/model execution;
- remote penetration testing;
- automatic external egress;
- auto-fix/write authority;
- canonical roadmap renumbering;
- replacement of Fehrest, AMAN, Nawat, S8, or S9 ownership boundaries;
- treating hosted product behavior as public/reusable source;
- treating one observed repository license as final file-level reuse clearance.

## Acceptance relationship

This addendum is fulfilled only through the dependency-ordered tasks in `assurance-fabric-tasks.md`, the semantic contract in `contracts/assurance-fabric.md`, and the architecture/source-acquisition records referenced by those tasks. It is future planning and does not self-activate any task.
