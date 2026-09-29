# WePLD Data, Agent Orchestration, and Local Planning Implementation Plan

```text
STATUS = IMPLEMENTATION_READY_CROSS_CUTTING_PLAN
OBSERVATION_DATE = 2026-09-29
BASE_CANONICAL_MAIN = 666e62d7d9e040505baca277a474d734afcc07a0
ROADMAP_CHANGE = NONE
TASK_DAG_CHANGE = NONE
NEW_AUTHORITY_DOMAIN = NONE
NEW_CANONICAL_DATABASE = NONE
GLOBAL_IMPLEMENTATION_AUTHORITY = NONE
TASK_SPECIFIC_IMPLEMENTATION = EXISTING_ASTRO_GRANTS_ONLY
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
```

This plan extends the accepted Astro execution package with three founder-authorized source candidates:

- `t8y2/dbx`
- `paperclipai/paperclip`
- `metadist/synaplan`

The founder explicitly states permission to copy and use their source code as needed. Public license metadata remains independently recorded. Permission does not bulk-admit any repository, dependency, service, model, secret, network destination, database connection, or effect.

The purpose is to make WePLD implementation-ready without creating a second control plane. DBX, Paperclip, and Synaplan are mechanism donors. Existing WePLD owners remain authoritative.

```text
DBX != WePLD Data Authority
Paperclip != WePLD Mission Runtime
Paperclip Org Chart != Edara Authority
Synaplan Planner != AGILLE Authority
Synaplan Capability != Nawat Grant
Synaplan RAG Index != Fehrest Truth
DONOR_PASS != WEPLD_PASS
```

## 1. Exact source observations and disposition

| Source | Exact observed revision | Public rights observed | Founder permission | WePLD disposition |
|---|---|---|---|---|
| `t8y2/dbx` | `4269a61e2cf6c19afdcaba41fed1e57d6e5e3512` | Apache-2.0 | Explicitly asserted 2026-09-29 | SALVAGE/ADAPT database connection, MCP scope, stateful session, transaction, plugin permission and credential-isolation mechanisms |
| `paperclipai/paperclip` | `24beb005755465f71a19ec92a85da0958d1b9740` | MIT | Explicitly asserted 2026-09-29 | SALVAGE/ADAPT Work/agent orchestration, atomic checkout, heartbeat/wakeup, budget, recovery, routine, audit and plugin-governance mechanisms |
| `metadist/synaplan` | `e81eb3431deb3e242c3a114e8cbf08e2fbfd1e88` | Apache-2.0 | Explicitly asserted 2026-09-29 | SALVAGE/ADAPT bounded DAG validation, capability vocabulary, access-scoped RAG, optional local routing, saved-task and connector patterns |

No later upstream revision is silently substituted. A later pin requires a new source-acquisition observation and diff.

## 2. Why each source is useful

### 2.1 DBX — data/database capability donor

DBX is valuable because it already solves several database-tool problems WePLD must not solve casually:

- connection-scoped MCP access;
- database and tool allowlists;
- schema-context extraction for AI clients;
- bounded query result sizes;
- stateful SQL sessions with explicit expiry;
- explicit transaction begin/commit/rollback where the backend can prove rollback semantics;
- batch execution with preflight policy across the whole script;
- explicit unsupported outcomes instead of auto-commit fallback;
- read-only and destructive-query policy rechecks on every request;
- connection credentials kept host-side rather than injected into model-visible schemas;
- plugin manifests with versioned host APIs and deny-unknown-field structures;
- capability permissions including read-only schema/data scopes and bounded HTTPS origins;
- user opt-in before plugin tools are visible to built-in AI or an external MCP surface;
- lazy MCP tool discovery to avoid flooding model context with tool schemas.

High-value observed mining targets:

```text
docs/content/docs/mcp.mdx
  - MCP connection/tool/database scoping
  - stateful query sessions
  - explicit transactions
  - batch SQL policy
  - plugin MCP lazy discovery
  - bounded result/output semantics

docs/content/docs/plugin-development.mdx
  - manifest/permission/contribution model
  - host-owned credential binding
  - read-only data/query capability
  - network origin declaration
  - plugin package lifecycle
crates/dbx-plugin-runtime/src/plugins/manifest.rs
  - strict versioned manifest parsing
  - permission registry
  - bounded network-origin declarations
  - host API compatibility
  - explicit MCP exposure flags
```

Do **not** import DBX as a second desktop application, canonical connection registry, policy engine, or database truth store. WePLD owns the capability package, principal scope, effect decision, evidence and completion semantics.

### 2.2 Paperclip — Work/Edara/Mission Runtime donor

Paperclip is valuable because it has explicit operational semantics for long-lived teams of agents rather than only agent invocation:

- structural parent/subtask relations separated from blocker/dependency relations;
- ownership separated from execution state;
- atomic task checkout;
- separate current-owner lock and live-execution identity;
- compare-and-clear stale-lock finalization;
- no retry-spam against a real live owner;
- routable blocked states instead of prose-only waits;
- durable wakeups and idempotent skip diagnostics;
- configuration validation before dispatch;
- persistent task context across heartbeats/restarts;
- recovery after orphaned/stale runs;
- explicit human versus agent ownership differences;
- bounded parent/child report channels rather than lateral write authority;
- company/project/agent scoped cost and budget policies;
- warning thresholds and hard stops;
- pause plus queued/running-work cancellation hooks;
- recurring routines with concurrency/catch-up policy;
- agent/provider adapters and persistent sessions;
- plugin and secret handling patterns;
- auditability of work, cost, recovery and approvals.

High-value observed mining targets:

```text
doc/execution-semantics.md
  - ownership vs execution
  - checkoutRunId vs executionRunId semantics
  - blocker/parent distinction
  - blocked-state liveness
  - stale-lock recovery
  - review handoff
  - parent/child report boundaries
server/src/services/recovery/service.ts
  - durable recovery causes
  - retry accounting
  - stale execution reconciliation
  - budget-aware recovery
  - cancellation and watchdog patterns
server/src/services/budgets.ts
  - scope-specific budgets
  - warning/hard-stop state
  - pause/cancel hooks
  - approval/incident evidence
```

Do **not** import Paperclip as a competing task database, company authority, completion authority, or universal agent scheduler. Work, Edara, Mission Runtime, Nawat, Assurance, Trusted Completion and Byan retain their current owners.

### 2.3 Synaplan — AGILLE/Fehrest/Mirefa donor

Synaplan is useful in three places:

1. bounded plan-DAG validation;
2. access-scoped retrieval/RAG;
3. capability-to-runtime/model separation.

Observed mechanisms include:

- strict versioned plan payloads;
- bounded node count (`MAX_NODES`);
- unique node IDs;
- explicit `depends_on` references;
- rejection of self-dependencies and unknown dependencies;
- explicit acyclicity validation;
- allowed-capability filtering;
- reply-node validation;
- safe fallback rather than execution of malformed plans;
- capability vocabulary separated from model selection;
- planner chooses a capability while a later route resolves the model;
- read/write MCP capabilities represented separately;
- planner-visible versus builder-only capabilities;
- RAG scope filters that preserve owner/group/file scope in MariaDB and Qdrant;
- local/offline deployment patterns and optional local model routes;
- optional components rather than a mandatory vector/office stack.

High-value observed mining targets:

```text
backend/src/Service/Multitask/Plan/TaskPlanValidator.php
  - bounded DAG validation
  - capability allowlist
  - acyclicity
  - reply-node validation
backend/src/Service/Multitask/Plan/Capability.php
  - capability vocabulary
  - capability/model separation
  - read versus write tool distinctions
  - planner-hidden builder-only operations
backend/src/Service/RAG/VectorStorage/RagScopeFilter.php
  - owner/group/file access scope projected consistently to SQL and Qdrant
```

Do **not** import Synaplan's PHP/Vue/Docker stack, Qdrant, Redis, MariaDB, Ollama, Tika or other sidecars as mandatory WePLD dependencies. Mine mechanisms behind WePLD contracts. Optional components stay optional.

## 3. Canonical ownership after integration

| Concern | WePLD owner | Donor contribution |
|---|---|---|
| Work item identity, hierarchy and user-visible state | Work | Paperclip issue/task semantics inform invariants only |
| Plan qualification and task DAG | AGILLE | Synaplan bounded plan validator informs validation |
| Context/source facts and database schema facts | Fehrest / Maemar | DBX schema context + Synaplan scoped RAG mechanisms |
| Model/tool/capability qualification | Mirefa | Synaplan capability/model separation + DBX plugin descriptors |
| Team topology and delegation | Edara | Paperclip roles/reporting/delegation mechanisms |
| Task/Attempt lifecycle and resume | Mission Runtime | Paperclip checkout/wakeup/recovery mechanisms |
| Tool/worker/database adapters | UWC | DBX MCP/query/session adapters; Paperclip worker adapter patterns |
| Principal scope/effect-time authorization | Nawat | DBX permissions and Paperclip policy are inputs, never authority replacements |
| Security/risk overlays | AMAN | donor threat/test corpora only |
| Review/Test/Security | Assurance | Paperclip review-state mechanics are evidence/lifecycle references |
| Completion | Trusted Completion | donor `done` or green status never decides completion |
| Learning/measurement | Byan | donor cost, routing and workflow observations become measured evidence only |

## 4. Product capability additions without a new roadmap

The following are product profiles under existing owners and tasks. They are **not** new Astro nodes.

```text
DATA / DATABASE WORKBENCH
  owner: Work + Fehrest + Mirefa/UWC + Nawat
  donor: DBX

AGENT ORGANIZATION / WORK ORCHESTRATION
  owner: Work + Edara + Mission Runtime + Nawat
  donor: Paperclip

BOUNDED DAG / LOCAL AI ROUTING / SCOPED RAG
  owner: AGILLE + Fehrest + Mirefa
  donor: Synaplan
```

The edition-aware P01 manifest must expose these only as bounded profiles whose implementation leaves remain governed by H01/F03/F04/F05/F06/U01/U02/U03/T02/T03/P04/K02 and the owning security/benchmark gates.

## 5. Implementation contract — Data / Database Workbench

### 5.1 Canonical records

A future implementation may add bounded data-tool records under the owning task's accepted schema. The logical contract must cover at least:

```text
DataConnectionRef
- connection_id
- capability_package_id
- principal_scope_ref
- locality
- backend_kind
- database_scope
- read_only
- production_classification
- credential_handle_ref
- observed_generation
- last_verified_at

DataOperationRequest
- target_connection_ref
- operation_kind
- statement_or_command_digest
- requested_database/schema
- expected_effect_class
- row/output bounds
- transaction_mode
- route_identity
- source_work/task/attempt

DataOperationDecision
- NawatDecisionRef
- allowed_effect_class
- exact target scope
- expiry/epoch
- confirmation_requirement

DataOperationReceipt
- target identity/generation
- operation digest
- transaction/session identity?
- affected/returned row count
- truncated/incomplete flags
- backend acknowledgement
- timing
- error/uncertain outcome
```

Credentials are never model-visible configuration fields. Model/tool schemas receive stable connection identities and policy-safe metadata only.

### 5.2 Effect classes

At minimum distinguish:

```text
DATA_METADATA_READ
DATA_QUERY_READ
DATA_QUERY_WRITE
DATA_DDL
DATA_ADMIN
DATA_TRANSACTION_BEGIN
DATA_TRANSACTION_COMMIT
DATA_TRANSACTION_ROLLBACK
DATA_CONNECTION_CREATE
DATA_CONNECTION_EDIT
DATA_CONNECTION_DELETE
DATA_EXTERNAL_MESSAGE_SEND
```

Read permission never implies write. One database scope never implies another database. Session ownership never widens data policy.

### 5.3 Stateful sessions

If WePLD admits a stateful database-session route:

- session is bound to one qualified connection and principal scope;
- unknown/expired session IDs fail closed;
- expiry is explicit;
- connection-level policy is rechecked per request;
- stateful session does not bypass Nawat effect-time authorization;
- active transaction state is explicit;
- commit/rollback uses backend acknowledgement;
- unsupported transaction backends return `TRANSACTION_UNSUPPORTED`, never silent auto-commit;
- crash during an unknown commit outcome enters reconciliation, not blind retry.

### 5.4 Batch execution

A script/batch must be parsed before execution and evaluated as one requested effect envelope.

Required behavior:

```text
ONE_FORBIDDEN_STATEMENT -> BATCH_REJECTED
READ_ONLY_SCOPE + WRITE_OR_DDL -> REJECTED
TRANSACTION_REQUEST + NONROLLBACKABLE_DDL -> UNSUPPORTED_OR_REJECTED
CONTINUE_ON_ERROR + ATOMIC_TRANSACTION -> REJECTED
UNKNOWN_STATEMENT_CLASS -> FAIL_CLOSED
```

Per-statement receipts remain visible when non-atomic execution is explicitly authorized.

### 5.5 Plugin/tool capability packaging

Mine DBX's strict manifest ideas into H01 rather than cloning its manifest wholesale:

- stable package ID/version/publisher;
- host/API compatibility;
- deny unknown security-sensitive fields;
- exact permissions;
- exact contributions/tool surfaces;
- explicit built-in-AI exposure versus external-MCP exposure;
- bounded network origins;
- path traversal rejection;
- host-owned secret binding;
- optional lazy tool discovery.

A plugin being installed does not expose it to an agent. User preference, H01 admission, Mirefa qualification and Nawat at-use checks remain separate gates.

## 6. Implementation contract — Work / Agent Orchestration

### 6.1 Separate structure, dependency, ownership and execution

Preserve four distinct relationships:

```text
STRUCTURE != DEPENDENCY
DEPENDENCY != OWNERSHIP
OWNERSHIP != LIVE_EXECUTION
```

A parent/child relation explains decomposition. A blocker edge controls readiness. An assignee identifies responsibility. An Attempt identifies actual execution.

### 6.2 Atomic claim / attempt lease

WePLD's existing Task/Attempt model must preserve these Paperclip lessons:

- at most one active execution owner for a bounded task lease unless the task explicitly permits comparison/parallelism;
- claim and readiness validation are atomic;
- stale terminal/missing attempt references may be reconciled;
- a live attempt is never cleared because another worker wants the task;
- finalization compare-and-clears only a lease still bound to the finalizing Attempt;
- successor Attempt adoption never lets a predecessor clear the successor's lease;
- conflict is a real conflict, not a retry invitation.

### 6.3 Routable waiting states

A blocked/waiting state is valid only with a machine-routable reason:

```text
blocker edge
pending approval/review interaction
structured owner + required action
time/source condition with owned re-check
external provider condition with bounded monitor
```

Prose-only blocking is not healthy state. It must become `NEEDS_ATTENTION`/equivalent with a visible owner instead of silently stranding work.

### 6.4 Durable wakeup and idempotency

Scheduled, dependency, connector and user-triggered wakeups require stable identity and deduplication.

Repeated observations of the same unchanged gate may coalesce diagnostically, but:

```text
SKIPPED_WAKE != FUTURE_WAKE_DELIVERED
GATE_CLEARED != OTHER_GATES_CLEARED
RETRY != NEW_AUTHORITY
```

Every dispatch rechecks current principal scope, task state, dependencies, budget, configuration, capability route and effect grant.

### 6.5 Pre-dispatch completeness

Known missing requirements must block before worker invocation:

- missing secret handle/binding;
- unresolved workspace/base ref;
- unavailable qualified route;
- unsupported hardware/runtime;
- expired principal scope;
- budget hard stop;
- unresolved blockers;
- required reviewer/worker unavailable when the task contract needs one.

Known pre-dispatch incompleteness is not recorded as a failed model attempt.

### 6.6 Delegation/report boundary

Delegated workers report through canonical channels. A child/reviewer role does not gain arbitrary write access to parent/sibling tasks.

Allowed report channels must be explicit and provenance-bearing. Cross-subtree coordination creates a new governed work item/message rather than widening ambient write authority.

### 6.7 Budget and cost control

T03 should mine Paperclip's scoped budget-policy shape without copying its authority model.

Required budget dimensions may include:

```text
principal/team
project/work
worker
provider/model/route
capability
calendar/lifetime window
billed cost
token/compute/time/resource quantity
```

Budget behavior:

```text
WARNING_THRESHOLD -> evidence + visible warning
HARD_STOP -> pause new affected dispatch
HARD_STOP -> cancel queued work where safe
RUNNING_EXTERNAL_EFFECT -> reconcile before declaring cancelled
BUDGET_INCREASE -> fresh policy generation
BUDGET_RESET != RETRY_AUTHORITY
```

### 6.8 Recovery

Recovery owns a bounded repair/reconciliation action, not the source task itself.

Paperclip-style recovery mechanisms are useful for:

- process lost;
- provider quota;
- interrupted native session;
- missing disposition after successful worker exit;
- configuration incomplete;
- workspace validation failure;
- retry accounting;
- stale execution lease;
- output inactivity watchdog.

Each recovery cause requires stable identity, maximum attempts, current-state recheck, and explicit escalation after exhaustion.

## 7. Implementation contract — Bounded DAG / Capability Routing / Scoped RAG

### 7.1 Plan graph validation

Before an AGILLE plan becomes a qualified executable plan, validate at least:

```text
schema_version supported
node_count <= configured bound
node IDs unique and non-empty
capability names known and admitted
capability allowed in current user/project/profile scope
dependencies reference existing nodes
no self-dependency
DAG acyclic
required reply/final-output node exists
inputs reference declared predecessors or approved source inputs
all effectful leaves identify authority/effect class
```

Malformed model output is evidence, not executable input.

Do not silently repair a materially different graph and execute it. A repair creates a new plan revision requiring the normal qualification/acceptance path.

### 7.2 Capability selection versus route selection

Adopt Synaplan's useful separation:

```text
AGILLE selects WHAT capability a node needs
Mirefa selects WHICH qualified route may satisfy it
Nawat decides WHETHER requested effects are allowed
Mission Runtime executes an accepted bounded plan
Trusted Completion decides whether the outcome is complete
```

The planner does not pick a provider/model to bypass Mirefa qualification.

### 7.3 Planner-hidden operations

Some operations may be available only to an authored/accepted plan or explicit user action, not to open-ended model planning.

Examples:

- external webhook/send;
- generic tool call;
- code execution;
- destructive database operation;
- organization/credential mutation.

A hidden capability is not merely omitted from UI; validation rejects it unless the accepted profile explicitly permits it.

### 7.4 Scoped retrieval parity

Mine Synaplan's principle that access scope must compile equivalently into every retrieval backend.

If WePLD supports multiple retrieval/index backends, the same logical scope must produce equivalent eligibility:

```text
principal/tenant
project/team
source collection
document/file IDs
source generation
access epoch
```

The vector/index query is always narrower than or equal to canonical source visibility.

```text
INDEX_SCOPE_SUPERSET_OF_SOURCE_ACCESS = SECURITY_FAILURE
VECTOR_RESULT_WITH_REVOKED_SOURCE = REJECT
UNKNOWN_SCOPE_TRANSLATION = FAIL_CLOSED
```

### 7.5 Optional infrastructure

Synaplan's local/offline product behavior is a useful reference, but WePLD must not require Qdrant, MariaDB, Redis, Docker, Ollama, Tika, Collabora or any hosted AI provider for the core loop.

Use optional adapters. Exact/lexical/structured retrieval must remain functional when vector infrastructure is disabled.

## 8. Source acquisition and path-level mining plan

### 8.1 DBX acquisition record — ASTRO-A09 / H01 / F06 / A04

Candidate source set to inspect before any import:

```text
t8y2/dbx@4269a61e2cf6c19afdcaba41fed1e57d6e5e3512
LICENSE
docs/content/docs/mcp.mdx
docs/content/docs/plugin-development.mdx
crates/dbx-plugin-runtime/src/plugins/manifest.rs
plugins/manifest.schema.json   # pin exact blob before import
related focused tests for selected manifest/MCP/session behavior
```

Import decision is expected to be mixed:

```text
ADAPT concepts/contracts
SALVAGE focused Rust validation where it beats reimplementation
DO_NOT_IMPORT full desktop/server/runtime
```

### 8.2 Paperclip acquisition record — ASTRO-A09 / A05 / A08

Candidate source set:

```text
paperclipai/paperclip@24beb005755465f71a19ec92a85da0958d1b9740
LICENSE
doc/execution-semantics.md
server/src/services/recovery/service.ts
server/src/services/budgets.ts
focused checkout/heartbeat/recovery/budget tests selected during A09
```

Expected disposition:

```text
SALVAGE algorithms/tests where narrow and framework-independent
ADAPT state-machine semantics into WePLD Task/Attempt/Work models
DO_NOT_IMPORT Paperclip database/server/UI as a second control plane
```

### 8.3 Synaplan acquisition record — ASTRO-A09 / A04 / A05

Candidate source set:

```text
metadist/synaplan@e81eb3431deb3e242c3a114e8cbf08e2fbfd1e88
LICENSE
backend/src/Service/Multitask/Plan/TaskPlanValidator.php
backend/src/Service/Multitask/Plan/Capability.php
backend/src/Service/RAG/VectorStorage/RagScopeFilter.php
focused unit tests/fixtures for plan validation and RAG scope translation
```

Expected disposition:

```text
PORT/ADAPT invariants to Rust contracts
SALVAGE fixtures and adversarial cases where rights/provenance are preserved
DO_NOT_IMPORT PHP/Vue/Docker service topology as WePLD core
```

## 9. Threat-to-test matrix

### 9.1 DBX-derived threats

| Threat | Required negative oracle |
|---|---|
| Model sees raw DB password/token/private key | tool/context snapshot contains only stable handle/ref and redacted metadata |
| Read-only route smuggles write/DDL inside batch | one write/DDL statement rejects whole batch before execution |
| Database switch escapes allowed database | target DB rechecked at use; unauthorized `USE`/equivalent rejected |
| Transaction unsupported but silently auto-commits | returns explicit unsupported outcome; zero statement execution |
| Commit response lost | marks outcome uncertain; no automatic retry until backend reconciliation |
| Expired/stale session silently falls back to pool | explicit unknown/expired-session error |
| Plugin declares unknown permission/field | package admission rejects or quarantines under version policy |
| Plugin network permission includes path/wildcard/token | manifest validation rejects |
| MCP plugin installed but not user-enabled | tool absent from model-visible surface |
| Connection A scope reused for B | connection generation/scope mismatch fails closed |
| Query result exceeds bounds | output truncation is explicit; rows are not silently clipped without flags |

### 9.2 Paperclip-derived threats

| Threat | Required negative oracle |
|---|---|
| Two workers claim same single-owner task | exactly one lease wins; loser receives ownership conflict |
| Old attempt finalization clears successor lease | compare-and-clear leaves successor intact |
| Dead `blocked` state with prose owner | transition rejected or escalated to visible attention state |
| Parent relation treated as blocker | scheduler executes unless explicit dependency edge exists |
| Cancelled blocker incorrectly satisfies dependency | dependent remains blocked until edge is removed/replaced or policy says otherwise |
| Reviewer gains parent/sibling mutation authority | write denied except explicitly allowed report channel |
| Repeated timer/wakeup duplicates work | idempotency key/coalescing produces one execution admission |
| Budget hard stop races dispatch | final pre-dispatch budget/policy check denies new run |
| Recovery loop retries forever | stable incident identity + bounded attempts + escalation |
| Provider quota treated as task completion | waiting/recovery evidence only; no completion decision |
| Missing secret dispatches worker and fails later | configuration-incomplete before worker invocation |
| Cross-tenant/company task/secret leak | tenant/principal scope enforced on every read/write and receipt |

### 9.3 Synaplan-derived threats

| Threat | Required negative oracle |
|---|---|
| Model-generated plan contains cycle | rejected before execution |
| Plan references unknown dependency | rejected |
| Plan exceeds node bound | rejected or requires new accepted plan profile; never truncated silently |
| Planner names unqualified capability | rejected by allowed-capability set |
| Planner selects provider/model directly | route field ignored/rejected; Mirefa resolves route |
| Builder-only effect capability appears in model-generated plan | rejected without explicit accepted profile |
| SQL and vector scope translators disagree | differential fixture must produce equivalent eligible source set |
| Revoked file remains vector-searchable | access epoch/source visibility recheck removes result |
| Optional Qdrant/local-model service unavailable | explicit unsupported/degraded state; no hidden cloud fallback |
| MCP read capability becomes write | separate capability/effect identity and Nawat decision required |

## 10. Recovery and migration contract

### 10.1 Database capability

- derived schema/cache/index can be rebuilt;
- connection config is versioned and secrets remain in secret storage;
- active session loss produces a new session, never pretend-preserves backend state;
- active transaction loss is `UNKNOWN_OR_ABORTED` until reconciled;
- plugin uninstall/revocation removes future tool eligibility and does not erase historical receipts;
- database writes are external effects: Git rollback does not undo them.

### 10.2 Agent orchestration

- Work/Task/Attempt history is append-only/versioned where audit requires it;
- crashed attempt recovery never rewrites predecessor evidence;
- leases can be reconciled only from terminal/missing owner evidence;
- schedule/routine replay uses stable occurrence identity;
- retry counters survive restart;
- budget and pause state survives restart;
- recovery action ownership is separate from source-task ownership;
- exhausted recovery escalates visibly rather than looping.

### 10.3 Plan/RAG routing

- accepted plan revision remains immutable evidence;
- replan creates a successor revision;
- route/model change creates a new route identity and fresh authorization where material;
- vector/semantic indexes are rebuildable from source facts;
- index backend migration must preserve scope-equivalence fixtures;
- source revocation/tombstone propagates to all derived indexes;
- optional component removal produces an explicit capability-unavailable state.

## 11. Benchmark and qualification plan

No upstream benchmark establishes WePLD quality.

### 11.1 Database/data capability

Preregister:

```text
schema discovery accuracy
query classification accuracy (read/write/DDL/admin)
destructive-query false-negative rate
scope escape rate
credential exposure rate
transaction correctness
unknown-outcome handling
stateful-session correctness
latency p50/p95
memory overhead
result-bound correctness
plugin manifest rejection corpus
```

Comparison arms may include:

```text
manual deterministic SQL tooling
WePLD deterministic DB adapter
+ AI SQL proposal with deterministic policy
+ optional qualified PLD/risk classification
```

### 11.2 Agent/work orchestration

Preregister:

```text
double-work rate
claim conflict correctness
stale-lock recovery correctness
orphaned-run recovery time
retry amplification
blocked-state liveness
budget overshoot after hard stop
scheduled-work duplicate rate
human intervention rate
accepted task outcome rate
runtime overhead
```

Compare the same worker/task/budget with raw worker versus governed WePLD orchestration.

### 11.3 Plan/RAG/local routing

Preregister:

```text
valid-plan rate
cycle/unknown-capability rejection
plan node count / token cost
accepted-outcome rate
route selection quality
no-model deterministic routing rate
retrieval recall / citation precision
cross-scope leakage = 0 target
revocation correctness
vector incremental value over lexical/structured baseline
local-route availability and latency
no-silent-fallback rate = 100%
```

B01/B02/B03 remain the owners of comparative release claims.

## 12. Dependency-ordered mapping to the existing 63-task DAG

No new task IDs are created.

| Mechanism | First owning task(s) | Later implementation/profile consumers |
|---|---|---|
| DBX source/rights/path freeze | ASTRO-A09 | H01/F06/A04 |
| DBX plugin/capability manifest | ASTRO-H01 | H02/F06/P01 leaf |
| DB schema/source facts | ASTRO-A04 | F03/F04 |
| DB query/effect adapter | ASTRO-F06 | U02/P01 leaf |
| DB MCP/tool surface | ASTRO-H01 | H02/U02 |
| Paperclip worker/runtime source qualification | ASTRO-A05 | F05/U01/U02 |
| Paperclip recovery mechanisms | ASTRO-A08 | F08/U01/U05 |
| Paperclip Work/claim/dependency semantics | ASTRO-W01/F05 | U01/U03/T02 |
| Paperclip staffing/delegation patterns | ASTRO-U03 | T02/B03 |
| Paperclip budgets/cost | ASTRO-T03 | B02/B03/T04 |
| Paperclip routines/schedules | ASTRO-P04 | U01/F06 |
| Synaplan plan validator/capability vocabulary | ASTRO-A05/W01 | F05/K03/P01 |
| Synaplan scoped RAG | ASTRO-A04 | F03/F04/K02/B03 |
| Synaplan local/model routing pattern | ASTRO-A05 | F05/K03/T03 |
| Synaplan MCP/plugin behavior | ASTRO-A09/H01 | H02/P04/P05 |

P01 must include the profiles in its edition-aware feature-completeness manifest after A09 is accepted. P01 does not itself admit the donors.

## 13. Implementation sequence once dependency gates permit

The sequence below is implementation-ready but remains subordinate to the canonical dependency graph.

### Phase A — acquisition and contract freeze

1. **A09**: create exact acquisition records for DBX, Paperclip and Synaplan with selected path/blob hashes, public rights, founder permission, dependencies, build hooks, network behavior, security disposition and exit strategy.
2. **A04**: decide whether DBX schema metadata and Synaplan RAG-scope fixtures materially improve the selected Brain parser/retrieval profile.
3. **A05**: decide whether Paperclip runtime/worker and Synaplan planner-route mechanisms improve the selected worker/harness route.
4. **A08**: qualify the Paperclip-derived recovery algorithms/tests selected for F08/U01.
5. **H01 design record**: freeze versioned capability-package permission fields required for DB/plugin/MCP surfaces; do not import DBX manifest wholesale.

### Phase B — first implementation leaves

6. **F03/F04**: add schema/source facts and access-checked database/RAG context using canonical Fehrest visibility.
7. **F05/U01**: implement durable task claim/Attempt resume semantics informed by Paperclip, with separate structure/dependency/ownership/execution fields.
8. **F06**: add database/tool effect classes and exact target binding through Nawat; no raw database credentials in model-visible context.
9. **W01/U03**: add accepted plan DAG validation and bounded staffing/delegation semantics; planner capabilities remain distinct from route selection.
10. **T03**: add budget-policy profile with final pre-dispatch hard-stop checks and external-effect reconciliation.
11. **P04**: add idempotent routine/schedule wakeup profile only after U01/F06 prerequisites.
12. **H01/H02**: capability package/plugin admission and lifecycle, including explicit AI/MCP exposure and revocation.

### Phase C — product profile and qualification

13. **P01**: expose database/data workbench, agent organization, and local DAG/RAG profiles with truthful availability states.
14. Run applicable S/R/Q security/review/test gates.
15. Run B02/B03 only after their canonical prerequisites; measure marginal value and overhead.
16. Promote only mechanisms that outperform simpler admitted machinery without weakening privacy, locality, authority or recovery.

## 14. Product UX contract

User choice stays explicit:

```text
Database / Data tools       OFF | ASK | AUTO
Agent delegation            OFF | ASK | AUTO
Recurring work              OFF | ASK | AUTO
Semantic/vector retrieval   OFF | ASK | AUTO
External MCP connectors     OFF | ASK | AUTO
```

`AUTO` permits selection only. It never grants an effect.

For database actions, UI must distinguish at least:

```text
Read metadata
Read data
Write data
Schema change
Administrative action
External message/queue send
```

For agent work, UI must distinguish:

```text
Assigned
Ready
Running
Waiting on dependency
Waiting on human/approval
Waiting on external condition
In review
Done
Cancelled
Needs attention
```

A status is not a completion decision unless Trusted Completion/human acceptance requirements for that Work item are satisfied.

## 15. No-gap closure matrix

| Concern introduced by donors | Owner / closure task | Plan status |
|---|---|---|
| Source identity and rights | A09 | CLOSED_IN_PLAN: exact repos/revisions/licenses/permission recorded; path blobs still task-time acquisition evidence |
| Full-app versus mechanism import | A09/H01 | CLOSED_IN_PLAN: selective salvage/adapt only; no second control plane |
| DB credentials | F06/H01 | CLOSED_IN_PLAN: host secret handles; never model-visible |
| Read/write/DDL/admin separation | F06 | CLOSED_IN_PLAN: distinct effect classes + whole-batch preflight |
| Stateful DB sessions | F06/U01 | CLOSED_IN_PLAN: bound scope, expiry, per-call recheck, unsupported fail-closed |
| Transaction uncertainty | F06/F08 | CLOSED_IN_PLAN: reconcile, never blind retry |
| Plugin permission/network scope | H01/F06 | CLOSED_IN_PLAN: versioned exact permission surface and bounded origins |
| Data/RAG cross-scope leakage | F04/T01 | CLOSED_IN_PLAN: canonical access translated equivalently; fail closed on mismatch |
| Plan cycles/unknown nodes | W01/F05 | CLOSED_IN_PLAN: strict bounded DAG validation |
| Capability versus model route | AGILLE/Mirefa A05/F05 | CLOSED_IN_PLAN: planner selects capability, Mirefa selects route |
| Effectful planner-only leaves | W01/F06 | CLOSED_IN_PLAN: explicit accepted-profile gate |
| Double work/task claim race | U01/F05 | CLOSED_IN_PLAN: atomic claim + lease identity |
| Stale attempt cleanup | U01/F08 | CLOSED_IN_PLAN: terminal/missing evidence only; compare-and-clear |
| Prose-only blocked state | Work/T02 | CLOSED_IN_PLAN: structured routable wait or needs-attention |
| Wakeup/retry duplication | U01/P04 | CLOSED_IN_PLAN: stable occurrence/idempotency identity |
| Budget race | T03/F05 | CLOSED_IN_PLAN: final pre-dispatch check + reconciliation |
| Recovery retry storm | A08/F08 | CLOSED_IN_PLAN: bounded attempts + escalation |
| Donor completion semantics | Trusted Completion | CLOSED_IN_PLAN: donor done/green is evidence only |
| Optional vector/service dependencies | A04/F04 | CLOSED_IN_PLAN: optional/rebuildable; deterministic baseline remains |
| Silent cloud fallback | A05/F05 | CLOSED_IN_PLAN: LOCAL_ONLY fails closed/asks; no substitution |
| Migration/removal | A08/H02 | CLOSED_IN_PLAN: versioned records, revocation, derived rebuild and exit strategy |
| Benchmark claims | B01/B02/B03 | CLOSED_IN_PLAN: preregistered WePLD measurements required |

```text
UNOWNED_NEW_PLANNING_GAPS = 0
NEW_BLOCKER_CURRENT = 0
FUTURE_GATES = OWNED_BY_EXISTING_ASTRO_TASKS
```

## 16. Definition of implementation-ready

This amendment is ready to drive implementation when accepted into the planning package because every requested donor mechanism has:

- exact source revision;
- rights status and founder permission;
- explicit disposition (salvage/adapt/reject whole-app import);
- canonical WePLD owner;
- existing Astro task owner;
- target contract/invariant;
- security negative oracles;
- recovery semantics;
- benchmark obligations;
- migration/removal path;
- explicit non-goals;
- dependency-ordered implementation sequence.

Implementation still cannot start on a leaf whose canonical predecessor or exact path/effect grant is absent.

```text
PLAN_READY_FOR_DEPENDENCY_ORDERED_IMPLEMENTATION = YES
NO_UNOWNED_PLANNING_GAPS = YES
SOURCE_ADMITTED = NO
DEPENDENCY_ADMITTED = NO
RUNTIME_QUALIFIED = NO
RELEASE_READY = NO
```

Those final `NO` values are governance gates, not missing planning.
