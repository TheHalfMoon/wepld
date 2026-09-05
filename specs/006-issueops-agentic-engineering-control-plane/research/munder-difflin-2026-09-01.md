# Research / Plan Addendum — Munder Difflin Coordination Patterns

```text
STATUS = FUTURE_PLANNING_RESEARCH_ADDENDUM
OBSERVED_ON = 2026-09-01
UPSTREAM_REPOSITORY = chaitanyagiri/munder-difflin
PINNED_REVISION = d27303e8a4cc86a98cfef408bb7e7b1fadb5ccad
UPSTREAM_TREE = 1a716287ebc57da16e012e5b674ec507f391d698
LICENSE_OBSERVED_FOR_SOURCE_CODE = MIT
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION_AUTHORITY = NONE
PROCESS_EXECUTION_AUTHORITY = NONE
GIT_EXECUTION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
```

This addendum records planning lessons from a pinned public upstream revision. It does not admit the upstream source, dependencies, assets, runtime, protocols, or implementation into WePLD. A future owning Source Acquisition Check must independently decide whether any concept, test oracle, fixture, dependency, or source fragment is admissible.

The upstream license states that the project source code is MIT-licensed while bundled pixel-art assets have separate licensing/attribution requirements. WePLD MUST NOT infer that all repository assets are MIT-licensed.

## 1. Why this source is relevant

Munder Difflin is a local multi-agent harness that wraps real terminal-agent CLIs behind a coordination layer. The useful planning signal for WePLD is not the office/avatar presentation. The useful signal is the coordination substrate underneath it:

- provider-neutral CLI/process wrapping;
- per-agent identity and durable memory;
- inbox/outbox mailboxes routed by a controller;
- one-message-per-file atomic delivery;
- a shared task ledger and append-only event log;
- single-writer/single-committer discipline around shared state and Git;
- bounded message semantics with deduplication and hop limits;
- optional semantic memory layered over markdown-first durable memory;
- per-agent worktree isolation;
- a stable agent-facing retrieval CLI contract over replaceable retrieval internals;
- trusted-side redaction before selected message content crosses into less-trusted presentation surfaces.

These are design quarries and behavior-oracle candidates only.

## 2. WePLD-native adaptation: Case Bus

Spec 006 SHOULD treat worker coordination as a durable Case-scoped substrate rather than as ad hoc provider-to-provider chat.

Candidate logical shape:

```text
Case
  |
  +-- WorkerRegistry
  +-- Assignment / Attempt graph
  +-- CaseMailboxRouter
  +-- per-worker inbox/outbox
  +-- CaseEventLedger
  +-- DecisionBoundary queue/view
  +-- Findings / reconciliation
  +-- RetrievalEvidence refs
  +-- Authority / qualification refs
  +-- CompletionEvidence
```

The implementation does not have to use literal directories or one JSON file per message. Those are upstream mechanisms, not WePLD requirements. The WePLD contract SHOULD preserve the properties that make the mechanism useful:

```text
DURABLE_DELIVERY = REQUIRED
MESSAGE_IDEMPOTENCY = REQUIRED
SINGLE_WRITER_OR_EQUIVALENT_CONFLICT_CONTROL = REQUIRED
APPEND_ONLY_MATERIAL_HISTORY = REQUIRED
EXPLICIT_ROUTER_OWNERSHIP = REQUIRED
BOUNDED_RETRY_AND_LOOP_CONTROL = REQUIRED
EVIDENCE_REFERENCES_PRESERVED = REQUIRED
AUTHORITY_REFERENCES_PRESERVED = REQUIRED
```

`CaseEventLedger` is evidence/history, not authority:

```text
EVENT_RECORDED != AUTHORIZED_EFFECT
MESSAGE_RECEIVED != WORKFLOW_INTENT
WORKER_REQUEST != NAWAT_GRANT
PROVIDER_ACK != TRUSTED_COMPLETION
```

## 3. Bounded inter-worker message protocol

The upstream `request | inform | propose | query | agree | refuse | done` speech-act model and hop-cap/idempotency rules are useful behavior-oracle candidates.

A WePLD-owned future protocol SHOULD use a provider-neutral typed act set, for example:

```text
REQUEST
INFORM
PROPOSE
QUERY
AGREE
REFUSE
RESULT
BLOCKED
ESCALATE
```

A material message SHOULD be able to bind:

```text
message_id
conversation_id
in_reply_to?
case_id
assignment_id?
attempt_id?
from_worker_id
recipient
action/act
subject
payload_ref_or_bounded_body
requires_reply
hop_count
created_at
trust_class
retrieval_evidence_refs[]
authority_refs[]
```

Required safety semantics:

- only acts that semantically require a reply should obligate a reply;
- duplicate `message_id` delivery is a no-op after first successful processing;
- a bounded hop/reply budget prevents worker-to-worker ping-pong;
- exceeding the bound produces a visible `BLOCKED`/`ESCALATE` frontier rather than infinite autonomous traffic;
- message content remains data and cannot mint WorkflowIntent, policy, route qualification, effect authority, review acceptance, or Trusted Completion.

Candidate negative oracles:

```text
DUPLICATE_MESSAGE_ID_IS_IDEMPOTENT
INFORM_OR_RESULT_DOES_NOT_FORCE_REPLY
HOP_CAP_PREVENTS_AGENT_PING_PONG
MESSAGE_BODY_CANNOT_CREATE_NAWAT_GRANT
WORKER_ESCALATION_CANNOT_SELF_APPROVE
```

## 4. Provider-neutral worker harness boundary

The upstream demonstrates that multiple terminal-agent CLIs can sit behind one coordination substrate. This reinforces, but does not authorize, the existing Spec 006 worker-delegation direction:

```text
WePLD Workflow / Case
        |
        v
WorkerDescriptor + Assignment
        |
        v
Mirefa route qualification
        |
        v
Nawat effect-time decision
        |
        v
Mission Runtime
        |
        v
UWC Worker Adapter
        |
        +-- Codex
        +-- Claude
        +-- Cursor
        +-- Gemini-class CLI
        +-- other separately qualified worker
```

Provider hooks, terminal semantics, session IDs, permission flags, auto-continue mechanisms, and lifecycle events MUST be normalized by adapters and MUST NOT become WePLD authority.

A future provider-neutral lifecycle SHOULD target semantic events such as:

```text
WORKER_STARTED
TURN_STARTED
TOOL_OR_EFFECT_PROPOSED
TOOL_OR_EFFECT_FINISHED
WORKER_IDLE
WORKER_BLOCKED
WORKER_COMPLETED
WORKER_FAILED
WORKER_CANCELLED
```

Provider-specific hooks may be one observation route after exact qualification; they are not the architecture.

## 5. Single-writer and governed Git broker candidate

The upstream uses a single-committer pattern to avoid concurrent Git index corruption while multiple workers operate. This is a relevant design candidate for WePLD's future effect architecture, especially when parallel Attempts use worktrees.

WePLD SHOULD evaluate a brokered shape instead of unrestricted worker Git access:

```text
worker proposes Git/process operation
        |
        v
bounded operation contract
        |
        v
Mirefa qualification evidence
        |
        v
Nawat exact-context grant/revalidation
        |
        v
Mission Runtime / qualified Git broker
        |
        +-- exact executable identity
        +-- exact argv family
        +-- exact repository/worktree target
        +-- environment scrubbing
        +-- timeout/output bounds
        +-- hook/network constraints
        +-- pre/post tree/index evidence
        v
result/evidence
```

This addendum does **not** change active S2 authority. In particular:

```text
S2_AUTH_013_ROUTE_DECISION != GIT_EXECUTION_AUTHORITY
S2_AUTH_014_QUALIFICATION != IMPLIED_BY_THIS_RESEARCH
SINGLE_COMMITTER_PATTERN != CURRENT_IMPLEMENTATION_AUTHORITY
```

A future owning task must compare single-committer, serialized broker, per-worktree, transactional/index-lock, and other qualified strategies rather than copying the upstream mechanism by default.

## 6. Worktree isolation

Per-worker worktrees are a useful parallel-execution candidate because they separate ordinary filesystem mutation and branch state. They do not solve authority, unsafe process behavior, hidden global state, network effects, credentials, hooks, or shared external-provider effects.

```text
WORKTREE_ISOLATION != SANDBOX
WORKTREE_ISOLATION != PROCESS_AUTHORITY
WORKTREE_ISOLATION != GIT_WRITE_AUTHORITY
WORKTREE_ISOLATION != SAFE_PARALLELISM_PROOF
```

Edara must still prove a minimum-sufficient topology and reject unsafe parallelism. Mirefa/Nawat/Mission Runtime retain their existing responsibilities.

## 7. Durable memory: canonical artifacts first, indexes second

The upstream's markdown-first memory plus optional semantic index reinforces a desirable WePLD property: durable source artifacts should remain inspectable and usable when an acceleration/index layer is unavailable.

For future Case/worker memory:

```text
DURABLE_CASE_ARTIFACT != VECTOR_INDEX
INDEX != SOURCE
EMBEDDING != EVIDENCE
GRAPH_FACT != AUTHORITY
MEMORY_RECALL != CURRENT_TRUTH
```

Candidate design:

```text
canonical Case/Assignment/Attempt/evidence artifacts
        |
        +-- lexical/FTS index
        +-- Fehrest/Maemar structured facts
        +-- optional semantic/vector index
        +-- optional graph projection
```

Indexes are rebuildable projections with generation/freshness identity. They do not become the sole durable record.

## 8. Stable retrieval seam

The upstream Knowledge Graph design exposes a small agent-facing retrieval command contract while allowing retrieval internals to evolve. Spec 006 should preserve the same architectural property without copying the specific CLI or storage implementation.

The WePLD-owned logical contract remains backend-neutral:

```text
collection/list/inspect
retrieve(query, scope, constraints)
fetch(source_id, exact_location?)
refresh(source)
provenance(result)
freshness(result)
explain_selection(result)
```

A CLI/UI surface such as `/rag` maps to this logical contract. Lexical, FTS, Fehrest.Maemar structured retrieval, vector search, rerankers, or future engines are replaceable signals/implementations.

```text
RAG_COMMAND != RETRIEVAL_ENGINE
RETRIEVAL_BACKEND != PROJECT_BRAIN
RETRIEVAL_SCORE != TRUTH
BACKEND_AVAILABILITY != SOURCE_ADMISSION
```

This supports the existing Spec 006 requirement that vector/embedding machinery must be benchmark-justified rather than mandatory for the first useful RAG slice.

## 9. Trusted broker / redaction boundary

The upstream implementation includes main-process redaction of secret-shaped content before selected message data crosses to renderer/voice surfaces. The reusable lesson is boundary placement, not its exact regex set.

WePLD SHOULD prefer:

```text
raw sensitive observation
        |
        v
trusted classification/redaction/egress boundary
        |
        v
minimum-sufficient normalized projection
        |
        v
UI / model / external provider
```

rather than sending raw data to a less-trusted surface and relying on that surface to hide it.

Any future redaction implementation needs its own threat model, corpus, negative oracles, false-negative analysis, and handling for structured secrets, binary artifacts, logs, screenshots, DOM/network captures, and provider transcripts.

```text
REDACTED_VIEW != SAFE_SOURCE
REGEX_REDACTION != COMPLETE_SECRET_DETECTION
REDACTION != EGRESS_AUTHORITY
```

## 10. Patterns intentionally rejected or narrowed

### 10.1 Supervisor prompt as authority

The upstream orchestrator uses prompt-level escalation policy as an important control surface. WePLD MUST NOT adopt that authority model.

```text
SUPERVISOR_PROMPT = ADVISORY_BEHAVIOR
NAWAT_POLICY_DECISION = EFFECT_AUTHORITY
MODEL_ASSERTION_OF_PERMISSION != PERMISSION
```

The planner/supervisor may propose routing, answer routine questions, or identify DecisionBoundaries. It cannot approve its own effects or convert provider permission prompts into WePLD authority.

### 10.2 Provider-specific autonomous-loop hooks

Provider Stop/hooks or auto-continue behavior may be useful adapter observations but MUST NOT define WePLD's worker lifecycle. No provider-specific loop may bypass Mission Runtime cancellation, authority revalidation, quota/cost policy, or circuit breaking.

### 10.3 Visual office metaphor

The avatar/office UI is product-specific and not a WePLD requirement. WePLD may visualize Case topology, active workers, evidence, findings, messages, and blocked frontiers, but every visualization must communicate operational truth rather than exist as decorative simulation.

### 10.4 Blind source reuse

MIT availability does not itself make upstream code a suitable dependency or source import. Future reuse must decide independently among:

```text
REJECT
DESIGN_QUARRY_ONLY
BEHAVIOR_ORACLE
TEST_OR_NEGATIVE_ORACLE
DOCUMENTATION_PATTERN
BOUNDED_SOURCE_REUSE
DEPENDENCY_OR_ADAPTER_CANDIDATE
```

Any bounded source reuse must preserve applicable attribution/license notices and must separately handle non-MIT assets.

## 11. Integration map into Spec 006

This addendum strengthens existing planning contracts rather than creating a second architecture:

| Observed pattern | WePLD planning destination |
|---|---|
| provider-neutral CLI harness | `contracts/worker-delegation.md` / UWC adapters |
| inbox/outbox + router | Case-scoped coordination / Mission Runtime |
| task ledger | `Assignment` / work graph |
| append-only event log | Case Evidence Timeline / Attempt history |
| speech acts + hop cap | future bounded inter-worker protocol |
| single committer | future qualified Git/process broker candidate |
| worktrees | Edara safe-parallelism + Mission Runtime isolation candidate |
| markdown-first memory | durable Case/worker artifacts |
| semantic memory | optional retrieval/index projection |
| stable retrieval CLI seam | `contracts/retrieval-rag.md` backend-neutral seam |
| main-side redaction | untrusted-content / egress / trusted-broker boundary |
| god/supervisor agent | Edara/planner/router assistance only; never Nawat authority |

## 12. Future qualification questions

Before any implementation tranche adopts these patterns, the owning slice must answer at least:

1. What is the canonical durable Case coordination store and its crash/recovery model?
2. What exact conflict-control guarantee replaces or implements single-writer semantics?
3. How are message delivery, deduplication, ordering, retry, poison-message quarantine, and hop limits proven?
4. Which inter-worker message acts are required, and which may obligate replies?
5. How are untrusted worker messages prevented from becoming WorkflowIntent or authority?
6. What process/session lifecycle is common across qualified worker adapters?
7. What containment exists when a provider has no enforceable read-only/sandbox mode?
8. Which Git serialization/worktree/broker strategy wins under Windows/Linux/macOS qualification?
9. How are global Git config, hooks, credentials, locks, environment, and network behavior contained?
10. What memory artifacts are canonical, and which indexes are rebuildable projections?
11. What retrieval contract stays stable if the backend changes?
12. Where must redaction/classification occur before UI/model/provider exposure?
13. What tests prove the orchestrator cannot grant authority to itself or its workers?
14. What evidence proves circuit breakers terminate loops without losing material history?
15. Which upstream source/code/test fragments, if any, are worth formal Source Acquisition rather than independent WePLD-native reimplementation?

## 13. Planning conclusion

The strongest reusable idea is a **Case Bus**: durable worker coordination, event history, bounded messaging, evidence references, and authority references under a WePLD-owned control plane.

```text
CASE_BUS
  = durable coordination substrate
  + worker registry
  + Assignment/Attempt routing
  + bounded message protocol
  + append-only material event history
  + evidence/provenance refs
  + qualification/authority refs
  + deterministic effect broker boundaries

CASE_BUS != MESSAGE_BROKER_PRODUCT_REQUIREMENT
CASE_BUS != WORKER_AUTHORITY
CASE_BUS != GIT_AUTHORITY
CASE_BUS != TRUSTED_COMPLETION
```

This is a future planning direction only. It must not be pulled backward into active S2 or used to bypass any source, dependency, process, Git, network, provider, security, or review gate.
