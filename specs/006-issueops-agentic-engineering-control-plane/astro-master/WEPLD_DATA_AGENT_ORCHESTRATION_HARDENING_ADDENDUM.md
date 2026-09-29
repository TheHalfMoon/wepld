# WePLD Data, Agent Orchestration, and Local Planning Hardening Addendum

```text
STATUS = NORMATIVE_PLANNING_HARDENING_ADDENDUM
PARENT = WEPLD_DATA_AGENT_ORCHESTRATION_IMPLEMENTATION_PLAN.md
ROADMAP_CHANGE = NONE
TASK_DAG_CHANGE = NONE
NEW_AUTHORITY_DOMAIN = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

This addendum closes implementation ambiguities found during final self-review of the DBX, Paperclip and Synaplan integration plan. It does not create new task IDs. The parent implementation plan remains the source-to-task map; this record adds mandatory failure, concurrency, data-handling and first-tracer-bullet requirements that every owning task must preserve.

## 1. Database enforcement is defense in depth

A SQL parser/classifier is a planning and policy aid, not the sole security boundary.

```text
STATEMENT_CLASSIFICATION != BACKEND_ENFORCEMENT
READ_SYNTAX != SIDE_EFFECT_FREE
SELECT_PREFIX != SAFE_READ
```

Every database route must combine, where the backend supports them:

1. **least-privilege database identity** — read routes use credentials/roles that cannot write, administer, load extensions or invoke dangerous server-side facilities;
2. **backend-native read-only mode** — read-only transaction/session flags where supported;
3. **dialect-aware statement classification** — the exact qualified parser/profile for the backend and version;
4. **Nawat effect authorization** — exact connection/database/schema/effect scope at use;
5. **driver/session policy** — timeout, cancellation, multi-statement and transaction behavior;
6. **receipt/reconciliation** — backend acknowledgement and uncertain-outcome handling.

The system must never claim that lexical inspection of a query proves absence of side effects.

### 1.1 Dialect-specific negative corpus

A database profile is not qualified until its negative corpus covers applicable forms such as:

```text
multi-statement smuggling
comments / whitespace / encoding obfuscation
CTEs containing write operations
stored procedures / functions with side effects
SELECT-like calls that execute user/server functions
DDL hidden inside procedural blocks
COPY / bulk-import / bulk-export facilities
server-side file/program execution facilities
extension loading
ATTACH / DETACH or cross-database attachment
PRAGMA or vendor session settings with security effect
temporary objects and search-path changes
transaction-control statements
role / grant / revoke statements
connection/database switch statements
trigger creation or trigger-mediated writes
vendor-specific admin commands
```

A statement the qualified profile cannot classify is rejected or routed to an explicitly broader effect class requiring separate authorization.

### 1.2 Backend permissions are part of qualification

The acceptance fixture must prove the **actual backend principal** for a read route cannot perform write/DDL/admin operations even when the classifier is bypassed in a negative test harness.

```text
PARSER_BYPASS + READ_PRINCIPAL -> WRITE_DENIED_BY_BACKEND
```

If a backend cannot provide a meaningful read-only principal/session boundary, the limitation is explicit and that route cannot be marketed as strongly read-only.

## 2. Database connection, pool, and session isolation

A pooled or reused connection can carry state across requests. Therefore every qualified pool/session profile defines reset semantics for applicable state:

```text
active transaction
isolation level
read-only/read-write mode
selected database/schema/search path
role / impersonation
session variables
prepared statements when security-relevant
advisory/application locks
temporary objects
loaded extensions/modules when applicable
```

A connection that cannot be proven clean is discarded, not returned to the pool.

```text
UNKNOWN_SESSION_STATE -> DROP_CONNECTION
POOL_REUSE != AUTHORITY_REUSE
```

Session IDs and pool keys bind to principal, connection generation, database scope and policy epoch. A session from one user/project/connection can never be adopted by another.

## 3. Local SQLite/file-backed databases

The first zero-network database tracer bullet should prefer a local SQLite-compatible profile because it proves the Work/Fehrest/UWC/Nawat path without requiring network egress or server administration.

The file target must still satisfy filesystem authority:

- canonical path resolution;
- symlink/reparse-point policy;
- file identity/generation checks where available;
- race-resistant open that binds authorization to the file object SQLite uses;
- handle-based identity/generation revalidation before read or write, with fail-closed behavior when the authorized object cannot be established;
- read/write distinction;
- lock/busy timeout;
- bounded database size/result size;
- no automatic extension loading;
- `ATTACH`/cross-file behavior denied unless explicitly authorized;
- WAL/journal side effects accounted for on write routes;
- backup/replace is a separate effect, not implicit query authority.

Path authorization is not complete until the opened SQLite file object is proven to be the authorized object. If the runtime cannot establish a race-resistant binding or revalidate the handle/object identity before access, the operation fails closed rather than falling back to path-only trust.

### First database tracer bullet

```text
PROFILE = LOCAL_SQLITE_READ_V1
NETWORK = NONE
SOURCE = one explicitly selected local database file
ALLOWED = metadata introspection + bounded read query
WRITE = DISABLED
DDL = DISABLED
ADMIN = DISABLED
EXTENSION_LOAD = DISABLED
ATTACH = DISABLED
MODEL_REQUIRED = NO
AI_SQL_PROPOSAL = OPTIONAL / PROPOSE_ONLY
```

Acceptance requires a deterministic direct-query path without any model. An optional AI proposal route may suggest SQL but cannot execute without the same deterministic validation and Nawat path.

A later write tracer is a separate profile and acceptance event.

## 4. Remote databases and tunnels are later profiles

PostgreSQL/MySQL/remote SQL, SSH tunnels, TLS/client certificates and cloud databases are not prerequisites for the local tracer bullet.

A remote profile additionally requires:

```text
exact destination identity
DNS/rebinding treatment
TLS mode and hostname verification
CA/client-certificate provenance
SSH host-key verification when used
jump-host/proxy identity when used
credential binding
network egress grant
connection timeout/retry policy
server-version/dialect identity
```

Do not silently downgrade TLS verification, accept changed SSH host keys, or fall back from a local connection target to a hosted proxy.

## 5. Data sensitivity, context, and retrieval boundary

Database rows are source data, not automatically project memory or RAG content.

```text
QUERY_RESULT != FEHREST_DURABLE_FACT
QUERY_RESULT != MEMORY
QUERY_RESULT != VECTOR_ADMISSION
```

A database source profile records:

- source owner/project/tenant scope;
- connection/database/schema/table visibility;
- sensitivity classification where known;
- source generation/freshness observation;
- retention/export policy;
- whether derived indexing is permitted.

Sending query results into ContextPackage, memory, embeddings, external review or a model route requires the applicable data/egress policy. A read permission does not imply permission to persist/index/export all returned rows.

At-use source visibility is rechecked before derived RAG evidence is delivered.

## 6. Query resource governance

Every query route has bounded:

```text
wall-clock timeout
statement timeout when backend supports it
row count
byte count
column/value size
concurrent queries
memory budget
spill/temp storage if applicable
cancel path
```

Cancellation is not assumed successful until the backend/driver acknowledges it or reconciliation proves termination. A timed-out write with unknown backend outcome is not retried blindly.

## 7. Task lease fencing

Atomic claim alone is insufficient for a distributed/restarted runtime. Every exclusive task lease/claim needs a monotonic **lease epoch / fencing token** (or equivalent compare-and-swap generation).

Worker writes that can change task/attempt state include the current lease epoch. A stale predecessor cannot mutate state after a successor lease is issued.

```text
ATTEMPT_A lease_epoch=7
ATTEMPT_B lease_epoch=8
ATTEMPT_A late write with 7 -> REJECT
```

Heartbeat timestamps alone are not fencing tokens.

Clock skew must not allow a worker to self-authorize lease ownership. The durable authority store decides current ownership/epoch.

## 8. Budget reservations and concurrent dispatch

A final budget read immediately before dispatch is necessary but insufficient when multiple attempts can start concurrently.

For hard budgets, T03/F05 must define atomic reservation or equivalent concurrency-safe accounting:

```text
AVAILABLE_BUDGET
-> reserve bounded dispatch budget
-> dispatch
-> settle observed cost
-> release unused reservation
```

Two concurrent dispatches cannot each spend the same remaining budget.

Required cases:

```text
concurrent reservation race
worker dies before settlement
provider reports delayed cost
actual cost exceeds reservation
external effect cannot be cancelled at hard stop
budget policy changes during run
manual budget increase/reset
```

Budget enforcement is a resource policy, not completion or authorization for unrelated effects.

## 9. Scheduled work, time zones, and recurrence

Recurring work must use a stable occurrence identity derived from the accepted schedule revision and intended occurrence, not only wall-clock observation.

A schedule profile defines:

```text
time zone
DST behavior
missed-occurrence catch-up policy
maximum catch-up count
concurrency policy
jitter/window policy where allowed
schedule revision identity
idempotency/occurrence key
pause/resume semantics
```

DST gaps/overlaps, clock changes and restart replay require deterministic fixtures.

```text
RESTART != DUPLICATE_OCCURRENCE
SCHEDULE_EDIT != SAME_OCCURRENCE_IDENTITY
```

## 10. DAG bounds beyond node count

A plan can be harmful even below the node-count ceiling. AGILLE/F05 validation therefore binds configurable limits for:

```text
node count
edge count
maximum depth
maximum fan-out
maximum fan-in
per-node retry count
whole-plan retry/repair budget
parallelism
wall-clock budget
model/tool/token/resource budget
artifact/input/output bytes
```

An accepted plan records the bound profile used for validation.

## 11. Typed node inputs and outputs

Each executable plan node declares the input/output contract needed by its capability.

Node inputs may reference only:

- accepted source inputs;
- declared predecessor outputs;
- explicit immutable configuration/parameter records.

Each reference binds producer/revision/content identity and expected type/schema. Missing, stale or incompatible outputs do not become empty strings or model guesses.

```text
MISSING_REQUIRED_INPUT -> NODE_BLOCKED
SCHEMA_MISMATCH -> NODE_BLOCKED
STALE_PRODUCER_GENERATION -> REQUALIFY_OR_BLOCK
```

Large/untrusted outputs remain tainted and bounded before entering another model/tool.

## 12. Dynamic branching and plan mutation

Condition nodes may select among **predeclared** accepted branches. They do not grant arbitrary runtime graph growth.

Any material addition/removal/reordering of nodes or effects after plan acceptance creates a successor plan revision and passes the normal qualification/authorization path.

```text
RUNTIME_BRANCH_SELECTION != RUNTIME_PLAN_REWRITE
MODEL_REQUESTS_NEW_EFFECTFUL_NODE -> SUCCESSOR_PLAN_REQUIRED
```

Emergency/repair operations remain bounded by their existing repair authority; they do not silently rewrite the canonical plan.

## 13. MCP/tool argument validation

A capability being admitted does not make arbitrary model-generated arguments valid.

For every tool/MCP/database capability:

- validate against versioned input schema;
- reject unknown security-sensitive fields;
- normalize/canonicalize targets before policy evaluation;
- bind target identity into EffectProposal/NawatDecision;
- cap strings/lists/files/query size;
- keep secret handles opaque;
- preserve output schema and producer identity.

Read and write variants use different effect classes even when served by the same MCP server.

## 14. First orchestration tracer bullet

The first Paperclip-informed runtime tracer should remain small:

```text
ONE project/work scope
ONE parent Work item
TWO bounded child tasks
ONE qualified builder route
ONE independent reviewer role
ONE exclusive task lease at a time per child
ONE lease epoch/fencing token
ONE restart/resume drill
ONE blocked-dependency drill
ONE budget policy with warning + hard stop fixture
NO recurring schedule required for first tracer
NO multi-host execution
```

Acceptance proves:

1. structure and dependency are distinct;
2. a blocked child does not run;
3. one claimant wins an exclusive claim race;
4. a stale claimant cannot write after lease succession;
5. restart reconciles active/terminal Attempt state;
6. reviewer cannot mutate outside its authorized report channel;
7. budget hard-stop blocks a new dispatch;
8. Trusted Completion remains separate from task status.

## 15. First bounded DAG / RAG tracer bullet

The first Synaplan-informed plan tracer should use no vector service and no hosted model requirement.

```text
PLAN_NODES <= 8
DEPTH <= 4
PARALLELISM <= 2
CAPABILITIES = deterministic/local admitted subset only
RETRIEVAL = exact + lexical + structured/symbol where applicable
VECTOR = OFF
HOSTED_MODEL = OFF
DYNAMIC_GRAPH_GROWTH = OFF
```

Acceptance includes:

- valid DAG executes in dependency order;
- cycle/self/unknown dependency rejected;
- node/depth/edge/fan-out bounds enforced;
- unknown/unqualified capability rejected;
- typed predecessor output mismatch blocks consumer;
- model/provider fields cannot bypass Mirefa;
- effectful capability cannot bypass Nawat;
- scope-equivalent source visibility proved for every retrieval backend used in the tracer;
- deterministic baseline remains usable with all optional semantic/model routes disabled.

## 16. Crash consistency and durable write ordering

For Work/Task/Attempt/lease/budget/effect records, implementation tasks must document durable write ordering around dispatch and completion.

The system must survive crashes at least at these cut points:

```text
after claim before Attempt persist
after Attempt persist before worker dispatch
after external dispatch before receipt persist
after worker exit before disposition persist
after budget reservation before dispatch
after cost incurred before settlement
after successor lease issued before predecessor observes it
```

Recovery never invents an effect result. Unknown external outcomes remain unknown until reconciled.

## 17. Audit and privacy minimization

Receipts/logs/audit records must contain enough identity to reproduce authority and outcome without becoming a secret/data dump.

Do not log by default:

```text
raw database passwords/tokens/private keys
full sensitive query results
whole prompts containing sensitive rows when digest/reference suffices
session cookies
opaque credential values
```

Record stable handles, hashes, counts, target identities, classification and bounded error details instead.

## 18. Hardening ownership map

| Hardening requirement | Owning existing tasks |
|---|---|
| DB dialect/parser + source facts | A04, A09, F03 |
| DB least privilege / effect classes / exact target | F06, H01 |
| DB sessions/cancellation/reconciliation | U01, F06, F08 |
| DB/RAG sensitivity and visibility | F04, T01, K02 |
| lease epoch/fencing | F05, U01 |
| claim/restart/recovery | U01, A08, F08 |
| concurrent budget reservations | T03, F05 |
| schedules/time zones/idempotency | P04, U01 |
| DAG bounds and typed dataflow | W01, F05 |
| capability/route separation | A05, F05, K03 |
| MCP/tool schema/effects | H01, F06, U02 |
| benchmark proof | B01, B02, B03 |
| security/adversarial validation | S01/S02/S03 plus owning task |

No requirement in this addendum creates implementation authority. The owning task must have its normal exact grant before code changes.

## 19. Hardening closure

```text
SQL_CLASSIFIER_AS_SOLE_BOUNDARY = PROHIBITED
STALE_WORKER_WRITE_WITHOUT_FENCING = PROHIBITED
CONCURRENT_BUDGET_DOUBLE_SPEND = PROHIBITED
UNBOUNDED_DAG_SHAPE = PROHIBITED
RUNTIME_GRAPH_GROWTH_WITHOUT_SUCCESSOR_PLAN = PROHIBITED
DATABASE_RESULT_AUTO_MEMORY_OR_VECTOR_ADMISSION = PROHIBITED
SILENT_REMOTE_DB_OR_HOSTED_MODEL_FALLBACK = PROHIBITED

HARDENING_GAPS_IDENTIFIED_BY_FINAL_SELF_REVIEW = OWNED
UNOWNED_HARDENING_GAPS = 0
```

This is a planning claim. Exact-head independent review remains required before the parent planning amendment is accepted; if qualified independent review is unavailable, the state is `REVIEW_BLOCKED`, never PASS.
