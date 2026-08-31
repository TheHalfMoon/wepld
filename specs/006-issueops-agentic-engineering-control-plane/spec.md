# Spec 006 — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CANDIDATE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
CURRENT_ACTIVE_SLICE = S2
```

## Problem

Engineering issues are fragmented across issue trackers, pull requests, CI systems, error trackers, chat, email, local logs, documentation, and model/agent sessions. Existing tools mostly expose queues; they do not provide a durable, governed control plane that can understand an issue, retrieve the right context, assemble qualified workers, reproduce the problem, plan and implement a fix, reconcile review findings, land an authorized change, and prove completion.

WePLD should become the best place to operate engineering issues with humans and agents while preserving its authority/evidence architecture.

## Product outcome

A user can bring a GitHub issue, another tracker item, a dropped file/directory, a URL, repository context, or an observed failure into WePLD and obtain one normalized `Case`. WePLD can then triage, retrieve evidence, reproduce, plan, delegate, implement, review, repair, land, close, and learn within explicit authority.

## Functional requirements

### FR-001 — Universal Case model

WePLD MUST represent external issue/ticket/incident objects as a provider-neutral `Case` with stable WePLD identity, source bindings, state, evidence, relationships, decisions, attempts, findings, and completion records.

### FR-002 — GitHub-first IssueOps

GitHub Issues and pull requests MUST be first-class provider bindings. Provider-specific identifiers and states MUST remain external bindings rather than becoming WePLD's canonical internal identity or completion semantics.

### FR-003 — Multi-provider adapters

The architecture MUST permit later adapters for GitLab, Linear, Jira, Azure DevOps, Sentry-class error systems, chat reports, email, and customer-support sources without changing the `Case` contract.

### FR-004 — Agentic lifecycle

A `Case` MUST support a governed lifecycle that can include ingest, normalize, deduplicate, classify, reproduce, diagnose, plan, task decomposition, worker routing, implementation, deterministic verification, independent review, repair, landing, provider closeout, and Trusted Completion evidence.

### FR-005 — Decision-boundary escalation

Automation SHOULD resolve discoverable facts itself and escalate only genuine product, architecture, authority, policy, ambiguity, or residual-risk decisions that cannot be safely inferred.

### FR-006 — Autonomy profiles

WePLD MUST support repository/workspace autonomy profiles with at least:

```text
observe
triage
prepare
execute
land
```

The selected profile constrains possible workflow behavior but MUST NOT replace effect-time Nawat authorization.

### FR-007 — Issue sweep

WePLD SHOULD support backlog sweeps that cluster duplicates and probable common root causes, identify already-fixed issues, classify blocked/decision-needed cases, surface quick wins, and produce an execution-ready frontier.

### FR-008 — Case rooms

Each active `Case` SHOULD expose a durable room showing assigned roles/workers, current attempts, dependencies, decisions, evidence, findings, blockers, and completion state.

### FR-009 — Arbitrary RAG collections

Users MUST be able to create named knowledge collections and add qualified supported sources including files, directories, pasted text, URLs, documentation, repositories, structured data, logs, and later additional source types.

### FR-010 — RAG scopes

Knowledge collections MUST support explicit scope semantics such as session, project, workspace, and global, with visibility and authority remaining separate concerns.

### FR-011 — Provenance-first retrieval

Every material retrieval result MUST retain source identity, location/citation where available, ingest identity, freshness, parser/index provenance, and sufficient evidence to explain why it was retrieved. Retrieval scores MUST NOT become truth or authority.

### FR-012 — Hybrid retrieval

The architecture MUST support exact/lexical retrieval first and optional semantic/vector, symbol, syntax, reference/call-graph, metadata, freshness, and reranking signals as their owning slices qualify them.

### FR-013 — Drag/drop and paste intake

Desktop and CLI surfaces MUST normalize dropped, pasted, or selected artifacts into an inert `InputArtifact` representation. Native desktop drop events and terminal path-paste behavior MUST converge on the same contract.

### FR-014 — No implicit execution from intake

Dropping, pasting, attaching, or adding a URL MUST NOT execute code, install dependencies, expand untrusted archives, access the network, mutate a repository, or send content externally without separate qualified actions.

### FR-015 — WePLD-native command surface

The planned command surface SHOULD include:

```text
/askme
/btw
/rag
/issues
/triage
/grill
/architect
/spec
/tickets
/build
/debug
/review
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

Commands are intent surfaces over WePLD capabilities, not independent authority paths.

### FR-016 — Skill primitives

Reusable behaviors such as TDD, domain modeling, deep-module design, code-review axes, diagnostic feedback loops, context packaging, grilling, writing-for-agents, merge-intent recovery, and architecture-boundary analysis SHOULD be internal capabilities rather than mandatory top-level commands.

### FR-017 — Provider-neutral delegation

`/delegate` MUST assign work through WePLD-owned worker/capability contracts. Provider-specific commands MUST NOT define the core product architecture.

### FR-018 — Explicit worker selection

A user MAY request a specific worker through a form such as `/delegate --to <worker> ...`, but explicit selection MUST still pass capability qualification, containment requirements, cost policy, and Nawat authorization.

### FR-019 — Worker catalog

WePLD MUST support a worker catalog describing stable WePLD worker identity, provider/adapter identity, capabilities, containment characteristics, supported effect classes, cost/metering properties, availability, and qualification evidence.

### FR-020 — No silent fallback

If a requested or selected worker/provider/model is unavailable or unqualified, WePLD MUST fail closed or request/obtain an explicitly authorized alternative. Silent substitution is prohibited.

### FR-021 — Cost-aware execution

Paid, quota-consuming, or materially metered worker execution MUST be explicit in worker metadata and MUST NOT be silently initiated when the controlling policy disallows it.

### FR-022 — Bounded context packages

Delegated work SHOULD receive the minimum sufficient context package: relevant files/symbols, spec/task fragments, decisions, tests, known failures, RAG evidence with provenance, and an authority/effect envelope.

### FR-023 — Dynamic teams

Edara SHOULD assemble minimum-sufficient worker topologies per case rather than use a fixed agent team. Roles MAY include triager, reproducer, diagnostician, implementer, test worker, security worker, and independent reviewer.

### FR-024 — Independent assurance

Material autonomous execution MUST preserve deterministic gates and independently qualified review. The implementer MUST NOT become acceptance authority for its own acceptance-critical work.

### FR-025 — Repair loops

Valid findings, failed checks, stale evidence, and changed external state MUST be able to trigger bounded repair/reassignment loops without erasing prior attempts or findings.

### FR-026 — Issue/PR landing

Issue provider mutation, branch/PR creation or update, merge, and issue closeout MUST be modeled as explicit effects with exact-target preconditions and replay/idempotency protections appropriate to the provider.

### FR-027 — Completion evidence

Closing or merging an external object MUST NOT itself establish completion. WePLD MUST record the evidence used for the governed completion decision.

### FR-028 — Learning

Completed cases SHOULD contribute evidence-backed reusable mechanics, failure patterns, negative oracles, retrieval hints, and routing signals through the existing Build Learning/Project Brain model. Learned behavior remains candidate evidence, not authority.

## Non-goals for this planning candidate

- no implementation in S2;
- no source/dependency admission;
- no external issue-provider access;
- no model/worker execution;
- no vector database selection;
- no provider SDK selection;
- no new process/network/Git authority;
- no canonical roadmap renumbering;
- no automatic merging or issue closing before the owning future authority exists.
