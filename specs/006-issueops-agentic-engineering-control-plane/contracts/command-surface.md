# Contract — Native Command Surface

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
```

## Command principle

Slash commands are user-intent surfaces. They normalize intent into WePLD capabilities and never bypass qualification, containment, Nawat authority, deterministic gates, review, security policy, or Trusted Completion.

## Planned stable commands

```text
/askme
/btw
/issues
/rag
/web
/triage
/grill
/architect
/spec
/tickets
/build
/debug
/review
/security
/fulltest
/prototype
/research
/wayfinder
/handoff
/teach
/questionnaire
/wizard
/retro
/workflow
/delegate
/workers
```

This list is the canonical planned stable-command catalog for Spec 006. Other planning artifacts should reference it rather than maintain incompatible subsets.

## Command semantics

### `/askme`

Routes the current user goal to the minimum sufficient qualified capability/workflow. It may recommend or invoke another command path according to current authority, but it must not silently select an unqualified paid/provider route.

### `/btw`

Re-explains current project/case/result/blocker state. Read-only by default and must not mutate workflow state merely by explaining it.

### `/issues`

Entry point for provider-neutral Case operations. Planned subcommands include inbox/list/sweep/show/attach/watch and later bounded execution intents.

### `/rag`

Creates/uses/manages named knowledge collections and performs provenance-first retrieval. Source access or refresh that requires filesystem/network effects remains separately governed. Derived retrieval/context visibility remains subject to current source access and egress policy.

### `/web`

Entry point for governed browser/WebMCP engineering workflows. Initial planned forms are:

```text
/web inspect
/web tools
/web reproduce <Case>
/web verify <Case>
```

Browser/WebMCP discovery, diagnostics, actuation, artifact transfer, clipboard/native-dialog/context effects, network access, credentials, and provider state remain separately classified/qualified/authorized. `/web` never implies browser authority merely because a browser is running or authenticated.

### `/triage`

Produces evidence-backed classification, reproduction readiness, duplicate/root-cause candidates, blockers, and next frontier.

### `/grill`

Opens decision-boundary questions only after discoverable facts are gathered to the available qualified extent.

### `/architect`

Uses domain, boundary, seam, interface, dependency, and deep-module analysis. It does not authorize refactors.

### `/spec`

Produces/updates Spec Kit planning artifacts under the canonical build method.

### `/tickets`

Builds tracer-bullet tasks and a dependency frontier, including blockers and expand/contract steps where required.

### `/build`

Executes the authorized implementation workflow over a qualified spec/task target. TDD and deterministic checks are internal methods, not bypassable optional decorations when required.

### `/debug`

Creates a tight reproduction/feedback loop, records falsifiable hypotheses, diagnoses, repairs when authorized, and preserves regression evidence.

### `/review`

Runs or coordinates an exact-target assurance profile focused on independent correctness/engineering review, architecture and maintainability risk, spec/contract conformance, regression risk, test quality, performance risk, and security-relevant engineering concerns. When review is acceptance-critical, implementer and qualified reviewer remain independent. Review findings are evidence and never grant completion or repair authority.

Planned forms include:

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

### `/security`

Builds the minimum-sufficient exact-target security assurance plan and, only where current authority permits, runs qualified security engines. It may combine deterministic SAST/structural checks, secrets, dependency/SCA evidence, SBOM, supply-chain checks, IaC/configuration, CI/workflow security, graph/taint/resource reachability, threat-model-driven checks, security regressions, and later dynamic/adversarial checks.

Planned forms include:

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

`/security --dynamic` does not imply unrestricted scanning. Network/target/credential/template/plugin/rate/budget/containment authority remains separately qualified and authorized. `LOCAL_PROJECT_OPEN`, `BROWSER_LOGGED_IN`, or a discovered target never imply permission to attack or scan it.

### `/fulltest`

Builds and, only when authorized, executes the minimum-sufficient assurance test plan needed to support the requested confidence claim. It does not mean blindly executing every command in a repository.

Planned forms include:

```text
/fulltest --quick
/fulltest --changed
/fulltest --standard
/fulltest --workspace
/fulltest --deep
/fulltest --release
/fulltest --adversarial
```

The plan may select format/style, compile/build, type checking, lint/static checks, unit, integration, contract/schema, snapshot/golden, property-based, coverage, mutation, fuzz, API/schema-driven, browser/E2E, security regression, platform, formal/model-checking, and performance/regression checks.

Every selected/omitted check has `REQUIRED`, `CONDITIONAL`, or `OPTIONAL` semantics under the exact `AssurancePolicySnapshot`. Omitted classes remain visible with explicit reasons. A required check blocked by budget, authority, availability, unsupported scope, or evidence gap prevents a `SUPPORTED` claim; it is not silently downgraded away.

### `/prototype`

Runs a bounded throwaway experiment to answer one explicit engineering/product question. Prototype output is evidence, not automatically production code.

### `/research`

Produces source-backed research with provenance/citations and preserves uncertainty/conflict.

### `/wayfinder`

Builds a decision map/frontier for large foggy work without pretending unresolved decisions are implementation tasks.

### `/handoff`

Transfers durable context/session responsibility. It does not assign new bounded work unless explicitly combined with a delegation workflow.

### `/teach`

Maintains a durable learning flow and learning assets while preserving the distinction between instruction and engineering authority.

### `/questionnaire`

Produces structured questions/choices for external decision capture.

### `/wizard`

Guides human-only setup/migration steps where direct autonomous execution is unavailable or intentionally inappropriate.

### `/retro`

Captures evidence-backed workflow/environment improvements after work. Learning output remains candidate evidence.

### `/workflow`

Defines/checkpoints recurring or resumable workflows. Recurrence does not grant future effects beyond policy.

### `/delegate`

Assigns bounded work to a qualified worker through Edara/Mirefa/Nawat/Mission Runtime/UWC. Supports optional explicit `--to <worker>` requests without bypassing qualification or cost/containment policy.

### `/workers`

Shows worker catalog, capability, availability, containment evidence, cost/metering, qualification, and expiry where available.

## Assurance command convergence

`/review`, `/security`, and `/fulltest` are not three independent engines. They are user-intent profiles over the shared future `Assurance Fabric` defined by:

- `../assurance-fabric-plan.md`
- `assurance-fabric.md`
- `../assurance-fabric-spec-addendum.md`
- `../assurance-fabric-tasks.md`
- `../professional-plan-hardening-tasks.md`
- `../research/native-assurance-source-acquisition-2026-09-02.md`

They share exact target identity, versioned policy snapshots, plan construction, engine qualification, Fehrest context, AMAN security evidence where applicable, normalized findings/evidence, typed claim assessment, coverage/freshness semantics, IDE presentation, and S9 history/passport integration.

Controlling invariants include:

```text
ASSURANCE_COMMAND != EFFECT_AUTHORITY
REVIEW_OUTCOME != COMPLETION_DECISION
SECURITY_FINDING != WRITE_AUTHORITY
TEST_PASS != TRUSTED_COMPLETION
CLAIM_SUPPORTED != TRUSTED_COMPLETION
NEW_EXACT_HEAD -> PRIOR_ACCEPTANCE_CRITICAL_EVIDENCE_STALE
ENGINE_ERROR != NO_FINDINGS
UNKNOWN_REACHABILITY != UNREACHABLE
FLAKY != CLEAN_PASS
```

## Optional aliases

User-friendly aliases such as `/fix <case-or-url>` may later normalize into `/issues` + `/build` workflow intent. An alias must not create a new authority path and is not part of the stable catalog until separately promoted.

## Input composition

Commands may consume:

- current project/case/session context;
- explicit arguments;
- `InputArtifact` attachments;
- `@rag:<collection>` references;
- provider object URLs/references;
- explicit worker requests.

All composed inputs preserve source/provenance/access identity.

## Error semantics

Unknown, unsupported, stale, unqualified, unauthorized, cost-blocked, coverage-limited, access-blocked, or inconclusive states must be explicit. Commands must not hide these conditions behind automatic fallback or a generic green result.
