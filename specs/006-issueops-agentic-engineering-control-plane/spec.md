# Spec 006 — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CANDIDATE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
CURRENT_ACTIVE_SLICE = S2
```

## Problem

Engineering issues are fragmented across issue trackers, pull requests, CI systems, error trackers, chat, email, local logs, documentation, browsers, websites, and model/agent sessions. Existing tools mostly expose queues or isolated automation surfaces; they do not provide a durable, governed control plane that can understand an issue, retrieve the right context, reproduce browser/web behavior, assemble qualified workers, plan and implement a fix, reconcile review findings, land an authorized change, and prove completion.

WePLD should become the best place to operate engineering issues with humans and agents while preserving its authority/evidence architecture.

## Product outcome

A user can bring a GitHub issue, another tracker item, a dropped file/directory, a URL, repository context, browser/web context, or an observed failure into WePLD and obtain one normalized `Case`. WePLD can then triage, retrieve evidence, reproduce, inspect browser/application behavior, plan, delegate, implement, review, secure, test, repair, verify, land, close, and learn within explicit authority.

## Functional requirements

### FR-001 — Universal Case model

WePLD MUST represent external issue/ticket/incident objects as a provider-neutral `Case` with stable WePLD identity, source bindings, state, evidence, relationships, decisions, attempts, findings, provider conflicts, and completion records.

### FR-002 — GitHub-first IssueOps

GitHub Issues and pull requests MUST be first-class provider bindings. Provider-specific identifiers and states MUST remain external bindings rather than becoming WePLD's canonical internal identity or completion semantics.

### FR-003 — Multi-provider adapters

The architecture MUST permit later adapters for GitLab, Linear, Jira, Azure DevOps, Sentry-class error systems, chat reports, email, and customer-support sources without changing the core authority/completion model.

Provider-specific fields SHOULD remain versioned adapter observations/extensions until a provider-independent engineering semantic justifies promotion into the Case model.

### FR-004 — Provider observation conflicts

Provider observations MUST be append-only evidence. Contradictory provider states, relationships, freshness, completeness, authenticity, or identity-binding evidence MUST remain inspectable and MUST NOT be silently resolved through generic latest-write-wins behavior.

When a dependent effect or completion decision requires a single complete current semantic, unresolved acceptance-critical conflict/partial/unauthenticated state MUST cause fail-closed, abstention, re-observation, or an explicit DecisionBoundary under the owning contract.

### FR-005 — Agentic lifecycle

A `Case` MUST support a governed lifecycle that can include ingest, normalize, deduplicate, classify, reproduce, diagnose, plan, task decomposition, worker routing, implementation, deterministic verification, independent review, repair, landing, provider closeout, and Trusted Completion evidence.

### FR-006 — Decision-boundary escalation

Automation SHOULD resolve discoverable facts itself and escalate only genuine product, architecture, authority, policy, ambiguity, or residual-risk decisions that cannot be safely inferred.

### FR-007 — Autonomy profiles

WePLD MUST support repository/workspace autonomy profiles with at least:

```text
observe
triage
prepare
execute
land
```

The selected profile constrains possible workflow behavior but MUST NOT replace effect-time Nawat authorization.

### FR-008 — Issue sweep

WePLD SHOULD support backlog sweeps that produce evidence-backed candidate relations/classifications, including exact/probable duplicates, common-root-cause groups, already-fixed-on-main candidates, reproduction-missing, blocked/decision-needed, security-sensitive, small/high-confidence, and high-risk cases.

Every sweep output class MUST define explicit evidence requirements, abstention behavior, a labeled benchmark corpus, predeclared promotion criteria, and negative oracles. Probable duplicate or semantic/topic similarity MUST NOT silently auto-close, merge Case identity, or establish causal/root-cause equivalence.

### FR-009 — Case rooms

Each active `Case` SHOULD expose a durable room showing assigned roles/workers, current attempts, dependencies, decisions, evidence, provider conflicts/staleness, findings, blockers, and completion state.

### FR-010 — Arbitrary RAG collections

Users MUST be able to create named knowledge collections and add qualified supported sources including files, directories, pasted text, URLs, documentation, repositories, structured data, logs, and later additional source types.

### FR-011 — RAG scopes and access

Knowledge collections MUST support explicit scope semantics such as session, project, workspace, and global, while source access, collection scope, worker visibility, egress permission, and effect authority remain separate concerns.

Source/access revocation MUST propagate to derived retrieval/index/context eligibility; cached derived content MUST NOT preserve broader visibility than the current source policy.

### FR-012 — Provenance-first retrieval

Every material retrieval result MUST retain source identity, generation/projection identity, location/citation where available, freshness, parser/index provenance, current access policy, trust classification, and sufficient evidence to explain why it was retrieved. Retrieval scores MUST NOT become truth or authority.

### FR-013 — Hybrid retrieval

The architecture MUST support replaceable exact, lexical, metadata, Fehrest.Maemar syntax/symbol/reference/call-graph, semantic/vector, freshness, and reranking signals.

Signal selection MUST be minimum-sufficient and query/source aware rather than a rigid serial ladder. Semantic/vector retrieval MAY be selected early for conceptual/paraphrastic query classes but MUST NOT become a prerequisite without predeclared benchmark evidence of incremental value and qualified privacy/cost/latency/exit behavior.

Source refresh MUST use generation semantics that prevent mixed old/new projections from masquerading as one current source view.

### FR-014 — Drag/drop and paste intake

Desktop and CLI surfaces MUST normalize dropped, pasted, selected, downloaded, or otherwise imported artifacts into an inert `InputArtifact` representation where the artifact crosses into WePLD-managed source/workflow handling. Native desktop drop events and terminal path-paste behavior MUST converge on the same contract.

### FR-015 — No implicit execution from intake

Dropping, pasting, attaching, downloading, or adding a URL MUST NOT execute code, install dependencies, expand untrusted archives, access the network, mutate a repository, enter RAG, or send content externally without separate qualified actions.

### FR-016 — Untrusted content remains data

Issue bodies, PR descriptions, comments, repositories, logs, documents, browser/page content, WebMCP metadata/output, downloaded artifacts, provider attachments, retrieved passages, worker output, and model output MUST default to data/evidence rather than instruction authority.

Untrusted content MUST NOT by itself create `WorkflowIntent`, change autonomy ceilings, expand file/secret/collection/network/provider/browser access, select a paid/remote route, disable containment/review, mint Nawat authority, or mark Trusted Completion.

Effect-capable workflows MUST preserve source/trust/access labels in context packages and MUST validate effects independently at exact effect-time boundaries. Sanitization, prompt filtering, model-side refusal, or injection classifiers MAY provide defense-in-depth but MUST NOT substitute for structural authority enforcement.

### FR-017 — WePLD-native command surface

The canonical planned stable catalog is owned by `contracts/command-surface.md` and includes:

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

Commands are intent surfaces over WePLD capabilities, not independent authority paths. The full catalog does not imply equal day-one prominence; initial UX SHOULD use routing and progressive disclosure.

### FR-018 — Skill primitives

Reusable behaviors such as TDD, domain modeling, deep-module design, code-review axes, diagnostic feedback loops, context packaging, grilling, writing-for-agents, merge-intent recovery, and architecture-boundary analysis SHOULD be internal capabilities rather than mandatory top-level commands.

Domain modeling and deep-module/boundary analysis SHOULD be explicit reusable modes in the architecture workflow rather than donor-study notes only.

### FR-019 — Provider-neutral delegation

`/delegate` MUST assign work through WePLD-owned `WorkerRequirement`/worker/capability contracts. Provider-specific commands MUST NOT define the core product architecture.

### FR-020 — Explicit worker selection

A user MAY request a specific worker through a form such as `/delegate --to <worker> ...`, but explicit selection MUST still pass capability-vocabulary compatibility, qualification, containment requirements, cost policy, and Nawat authorization.

### FR-021 — Worker catalog

WePLD MUST support a worker catalog describing stable WePLD worker identity, provider/adapter identity, versioned capabilities, provider permission claims, containment evidence, session/cancellation/recovery semantics, supported effect classes, cost/metering properties, availability, and qualification evidence.

### FR-022 — Qualification / authorization / runtime separation

Edara topology/staffing, Mirefa route qualification, Nawat effect-time authority, Mission Runtime execution hosting, and UWC adapter behavior MUST remain semantically distinct even if an early implementation co-locates them in one process.

Mirefa qualification MUST NOT mint effect authority. Mission Runtime MUST NOT widen or reuse expired grants, hide Nawat denial, silently substitute worker/provider/model routes, or blindly retry a material effect whose external outcome is unknown.

### FR-023 — No silent fallback

If a requested or selected worker/provider/model/browser/assurance-engine route is unavailable or unqualified, WePLD MUST fail closed or request/obtain an explicitly authorized alternative. Silent substitution is prohibited.

### FR-024 — Cost-aware execution

Paid, quota-consuming, or materially metered worker/browser/assurance execution MUST be explicit in metadata and MUST NOT be silently initiated when the controlling policy disallows it.

### FR-025 — Bounded context packages

Delegated work SHOULD receive the minimum sufficient canonical `ContextPackage`: relevant files/symbols, spec/task fragments, decisions, tests, known failures, RAG/browser evidence with provenance/trust/access labels, and an authority/effect envelope.

A source/access-policy change after package construction MUST stale affected future package use/egress.

### FR-026 — Dynamic teams

Edara SHOULD assemble minimum-sufficient worker topologies per case rather than use a fixed agent team. Roles MAY include triager, reproducer, diagnostician, implementer, test worker, security worker, browser verifier, and independent reviewer.

### FR-027 — Independent assurance

Material autonomous execution MUST preserve deterministic gates and independently qualified review. The implementer MUST NOT become acceptance authority for its own acceptance-critical work.

S7 Assurance MAY participate in a tight repair loop with S8 but MUST remain semantically independent from the repair/completion boundary that consumes findings.

### FR-028 — Repair loops

Valid findings, failed checks, stale evidence, changed external state, access revocation, and stale browser/page/tool generations MUST be able to trigger bounded repair/reassignment/reverification loops without erasing prior attempts or findings.

### FR-029 — Issue/PR landing and uncertain outcomes

Issue provider mutation, branch/PR creation/update, merge, issue closeout, browser submission, upload/download, and other externally observable effects MUST be explicit effects with exact-target preconditions and replay/idempotency/reconciliation protections appropriate to the route.

If execution may have committed remotely but the local result is lost, the state MUST become `EFFECT_OUTCOME_UNKNOWN`; WePLD MUST reconcile before unsafe retry.

### FR-030 — Completion evidence

Closing or merging an external object, passing a browser check, receiving WebMCP success, or obtaining a supported Assurance claim MUST NOT itself establish completion. WePLD MUST record the exact evidence used for the governed completion decision, and no acceptance-critical effect may remain outcome-unknown.

### FR-031 — Learning

Completed cases SHOULD contribute evidence-backed reusable mechanics, failure patterns, negative oracles, retrieval hints, browser/web verification evidence, and routing signals through the existing Build Learning/Project Brain model. Learned behavior remains candidate evidence, not authority.

### FR-032 — Governed WebMCP interoperability

WePLD SHOULD support WebMCP-class website tools as a replaceable browser/application interoperability protocol after the owning Source Acquisition and browser/runtime qualification gates.

A discovered website tool MUST be represented by the canonical `WebToolObservation` from `contracts/web-agent-boundary.md` as an untrusted capability observation. Tool availability, descriptions, schemas, annotations, `read-only` hints, outputs, browser login state, cookies, or ambient session authority MUST NOT substitute for WePLD effect classification, Mirefa qualification, Nawat authorization, containment, or user intent.

### FR-033 — Browser diagnostics/control/artifact boundary

WePLD SHOULD support a separately qualified DevTools-class browser adapter for diagnostics and bounded browser control, including Chromium/Edge/WebView2-class targets when independently qualified.

Browser diagnostics, WebMCP invocation, actuation, artifact transfer, clipboard/native-dialog/permission effects, and context-target control MUST remain distinguishable capability/effect classes even when one runtime exposes all of them.

### FR-034 — Exact browser/web context

Acceptance-critical browser/WebMCP effects MUST bind explicit browser session/profile/context/frame/target, origin, tool definition/generation, input/artifact identity, effect class, qualification evidence, Nawat decision, containment/access state, and expected postcondition.

Material navigation, origin, authentication, profile, target/context/frame, tool-set, definition, containment, access-policy, or freshness changes MUST force revalidation.

### FR-035 — No silent browser fallback

WePLD MUST NOT silently fall back among WebMCP structured tools, raw DOM click/type automation, DevTools actions, headless/local/remote browsers, Chrome, Edge, WebView2, another browser profile/session/context, or another upload/download artifact route. An alternative route requires explicit qualification and governing authorization.

### FR-036 — Web agent publisher mode

A future WePLD web/Desktop surface MAY expose selected capabilities through WebMCP. Such tools SHOULD expose safe intent/proposal/read surfaces by default. A WebMCP call into WePLD MUST NOT become a direct authority grant; any effectful operation still traverses the native WePLD qualification/authorization/execution/evidence pipeline.

### FR-037 — Explicit Assurance claim semantics

`/review`, `/security`, and `/fulltest` MUST use one shared Assurance Fabric and produce a typed `ClaimAssessment` for the exact requested claim under an immutable `AssurancePolicySnapshot`.

Missing/stale required evidence, unresolved blocking findings, material unresolved conflicts, or blocked required checks MUST prevent `SUPPORTED`.

```text
CLAIM_SUPPORTED != TRUSTED_COMPLETION
```

### FR-038 — Assurance evidence handling

Durable review/security/test/browser/performance evidence MUST carry content/trust classification, access and handling policy, redaction, retention/tombstone, freshness, and export/egress semantics sufficient to prevent the evidence timeline from becoming a secondary secret/private-data leak.

### FR-039 — Assurance engine identity and containment

Acceptance-critical engine execution MUST bind the actual executable/runtime/artifact identity and material rule/database/template/config snapshots plus a bounded resource/cleanup environment. PATH discovery or a matching version string alone MUST NOT satisfy engine identity.

### FR-040 — Finding governance

Assurance MUST preserve validated findings without majority erasure and support evidence-backed correlation plus scoped/authorized/expiring finding disposition for accepted risk, suppression, false positive, rule exception, fixed, and superseded states.

### FR-041 — Qualified performance evidence

A material performance finding/claim MUST bind benchmark/baseline/environment/fixture identity, warmup/repetition/noise semantics, threshold/decision rule, and explicit inconclusive states. A one-shot noisy timing MUST NOT become acceptance-critical performance evidence.

### FR-042 — Provider observation completeness/authenticity

Provider reads/events MUST expose completeness/authenticity, pagination/permission/rate-limit limitations, and stale state. Partial or unauthenticated observations MUST NOT silently become complete current provider truth.

### FR-043 — Remote RAG source security

Future remote URL/documentation ingestion MUST require exact network/source authority and defenses for redirect escape, DNS rebinding, private/link-local/metadata targets, credential/header forwarding, content/size/time bounds, and parser/decompression effects.

### FR-044 — Durable recovery and schema evolution

Before autonomous scale, durable Case/evidence/Assurance history MUST define schema migration, backup/restore, interruption recovery, tombstone/redaction propagation, and reconstruction sufficient to explain historical authority/assurance/completion decisions.

## Non-goals for this planning candidate

- no implementation in S2;
- no source/dependency admission;
- no external issue-provider or browser access;
- no live WebMCP invocation;
- no DevTools/browser control execution;
- no model/worker execution;
- no vector database selection;
- no provider SDK or browser automation framework selection;
- no new process/network/Git/browser/issue-write authority;
- no canonical roadmap renumbering;
- no automatic merging, browser submission, or issue closing before the owning future authority exists.
