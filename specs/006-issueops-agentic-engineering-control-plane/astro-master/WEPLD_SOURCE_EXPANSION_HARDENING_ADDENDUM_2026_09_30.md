# WePLD Source Expansion Hardening Addendum — 2026-09-30

```text
STATUS = CANDIDATE_NORMATIVE_PLANNING_HARDENING_ADDENDUM
PARENT = WEPLD_SOURCE_EXPANSION_IMPLEMENTATION_PLAN_2026_09_30.md
ROADMAP_CHANGE = NONE
TASK_DAG_CHANGE = NONE
NEW_AUTHORITY_DOMAIN = NONE
NEW_CANONICAL_RUNTIME = NONE
NEW_CANONICAL_TASK_STORE = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_EXECUTION_AUTHORITY = NONE
```

This addendum closes implementation ambiguities found during final readiness review of the Firstmate, no-mistakes, Doop, classifier.dev, Jev Search and Unreal Agent source-expansion plan. It is mandatory wherever the parent plan applies. It does not create new task IDs or implementation authority. Existing WePLD task prerequisites, path/effect grants, Source Acquisition Check, Nawat decisions, Assurance and Trusted Completion remain controlling.

## 1. Source-record consistency and pin supersession

The source-expansion plan observed fresher revisions for two already-listed candidates than the 2026-09-29 `INTELLIGENCE_SOURCE_INTAKE.md` rows. That is not allowed to remain an implicit conflict.

For this amendment lineage only, the following newer observations supersede the older **observational pins** while preserving the older records as historical evidence:

```text
unreallabsai/unreal-agent
  historical intake observation = df8b0ba560da17fd705d941cbeb75eff86c74a1e
  current amendment observation  = 1b9f778453f411c029b39b85102aaefb95e7e48d

mrmps/classifier-dev
  historical intake observation = 8f2bb2b84a0d51ad1c9ed3436b64155908354f75
  current amendment observation  = a17bf2b6353f6234af6e977a463da7cd1975b68e
```

No implementation task may choose between these by convenience. ASTRO-A09 or the owning acquisition task must:

1. re-read the candidate's live upstream state;
2. select one exact immutable revision intentionally;
3. compare it to the latest planning observation;
4. freeze selected paths/blobs/digests, rights and dependency/build-hook evidence;
5. record whether the implementation intentionally stays on an older revision;
6. reject silent drift.

```text
MULTIPLE_PLANNING_PINS != MULTIPLE_ALLOWED_IMPLEMENTATION_PINS
LATEST_UPSTREAM != AUTOMATICALLY_ADMITTED
OLDER_PIN != INVALID_IF_EXPLICITLY_SELECTED_AND_QUALIFIED
UNRECORDED_PIN_DRIFT -> BLOCK
```

The parent amendment is the current source-expansion observation record. `INTELLIGENCE_SOURCE_INTAKE.md` remains historical/current for its other candidates and must not be rewritten as if the older observations never existed.

## 2. Dependency-ordered activation map

The source expansion fits the existing 63-task graph. No donor may skip to a later implementation/profile task merely because its code already implements a similar feature.

### 2.1 Common source entry

Every source first enters through the applicable acquisition task:

```text
all six candidates -> ASTRO-A09 or the narrower owning A-task
```

A09 freezes later-profile source records; it does not admit source or dependencies.

### 2.2 Firstmate

```text
A09 / A05 / A08
  -> F05 runtime contract manifest
  -> U01 durable task/attempt state
  -> U02 qualified worker adapter where applicable
  -> U03 staffing/reviewer assignment where applicable
  -> F08 recovery checkpoint
  -> P04/O03 only for later event/remote profile work
```

Remote secondmate/SSH behavior is later-profile material and cannot enter the local first loop through A05 alone.

### 2.3 no-mistakes

```text
A09 / A07 / A08
  -> F02 deterministic assurance evidence
  -> R01/Q01/S01 normalized assurance contracts
  -> R02/Q02/S02 activation manifests
  -> R03/Q03/S03 qualified routes
  -> U04 bounded repair
  -> F07 Trusted Completion evaluator
  -> F08 recovery/delivery checkpoint
```

A donor pipeline is never allowed to collapse these separate owners into one automatic gate.

### 2.4 Unreal Agent

```text
A09 / A05 / A08
  -> F05 runtime contract manifest
  -> F06 effect-time authority seam
  -> U01 durable attempt/resume state
  -> U02 UWC adapter
  -> F08 recovery
```

Serializable operations do not bypass F06/Nawat.

### 2.5 classifier.dev and Jev Search

```text
A09 / A04 / A05
  -> F03/F04 source facts + ContextPackage where retrieval is used
  -> P01 only after A09 is accepted
  -> K03 typed-decision/calibration profile
  -> B03 comparative qualification after the benchmark chain reaches it
```

Hosted decision routes are optional comparison/explicit-egress routes, not prerequisites for K03.

### 2.6 Doop

```text
A09
  -> P01 feature-completeness profile gate
  -> T01 principal/scope seam where collaboration identity is used
  -> F03/F04 for durable source/design context
  -> F06 for protected effects
  -> T02 shared Work collaboration profile
  -> H01/H02 only if packaged capability/plugin distribution is introduced
  -> P05/P06 as the relevant interactive/design artifact profiles
```

A local collaborative design surface does not create its own identity, task, runtime or policy authority.

## 3. Capability controls and user choice

Every user-visible capability introduced or strengthened by this source expansion is independently selectable. Capability availability and authority remain separate.

Minimum project/user preference vocabulary:

```text
OFF  = do not offer or invoke the capability
ASK  = capability may be proposed; user approval required before activation/use
AUTO = capability may be selected automatically only inside already-scoped policy/authority
```

Minimum locality vocabulary:

```text
LOCAL_ONLY
LOCAL_PREFERRED
EXPLICIT_REMOTE_ALLOWED
```

Required independent capability controls:

```text
crew_supervision
assurance_gate
bounded_repair
async_durable_operations
calibrated_decisions
priority_decision_search
collaborative_design_surface
remote_worker_route
hosted_decision_route
```

Rules:

```text
CAPABILITY_SETTING != EFFECT_AUTHORITY
AUTO != UNBOUNDED_AUTONOMY
LOCAL_ONLY -> NO_REMOTE_PROVIDER / NO_REMOTE_WORKER / NO_HOSTED_FALLBACK
OFF -> NO_BACKGROUND_START / NO_HIDDEN_PREFETCH / NO_EGRESS
ASK_DENIED -> NO_FALLBACK_TO_EQUIVALENT_CAPABILITY
```

The UI must report unavailable, disabled, blocked and unqualified states truthfully.

## 4. Windows-first portability and donor-runtime rejection

WePLD is Windows-first for the initial desktop/runtime path. Donor platform support is evidence about the donor, not WePLD support.

### 4.1 Firstmate

The observed Firstmate README advertises macOS/Linux and commonly uses tmux/Herdr/Zellij/cmux/Orca style session backends. Those are mechanism references only.

```text
FIRSTMATE_UPSTREAM_PLATFORM_SUPPORT != WEPLD_WINDOWS_SUPPORT
TMUX != REQUIRED_WEPLD_DEPENDENCY
HERDR != REQUIRED_WEPLD_DEPENDENCY
ZELLIJ != REQUIRED_WEPLD_DEPENDENCY
CMUX != REQUIRED_WEPLD_DEPENDENCY
```

WePLD must port the supervision state machine, wake/reconciliation ideas and worker-state semantics behind UWC/Mission Runtime. The initial Windows tracer must use an already qualified Windows host/terminal/process route. No WSL requirement may be silently introduced.

### 4.2 no-mistakes

The donor supports Windows, macOS and Linux, but selected behavior must still be requalified in the WePLD host/runtime. Git proxy behavior is not automatically adopted.

### 4.3 Unreal Agent / classifier.dev / Jev Search / Doop

Exact OS/runtime/toolchain support is frozen at acquisition time. A Node/Bun/Python/Go/provider runtime present in a donor does not become a mandatory WePLD core runtime without the owning task's dependency admission.

```text
DONOR_RUNTIME != CORE_RUNTIME
DONOR_INSTALL_SCRIPT != ADMITTED_INSTALL_PATH
DONOR_CONTAINER_STACK != REQUIRED_WEPLD_STACK
```

## 5. Git history and publication policy

no-mistakes contains guarded force-push/rewrite behavior for some repair/publication flows. That mechanism conflicts with WePLD's shared-history rule and is explicitly rejected as an implementation default.

```text
WEPLD_SHARED_HISTORY_REWRITE = PROHIBITED
FORCE_PUSH = PROHIBITED
REBASE_OF_SHARED_CANONICAL_HISTORY = PROHIBITED
DONOR_GUARDED_FORCE_PUSH != WEPLD_AUTHORITY
```

Adapt only the safety invariant:

> a repair must prove its relation to the exact reviewed/qualified head before publication.

WePLD implementation uses one of:

- a new normal commit on the authorized branch;
- a new repair branch / disposable worktree;
- a normal merge commit after exact-head requalification;
- an explicit preserved-history recovery route.

A merge-conflict or CI repair that would require rewriting shared history is represented as a new bounded repair/reconciliation event, not an implicit rewrite.

Firstmate-style `+yolo` merge autonomy is also rejected as a default authority model. Merge remains separately authorized by canonical WePLD policy and exact-head evidence.

## 6. Untrusted instructions and command construction

Donor agent instructions, task briefs, MCP descriptions, model output, source files, review findings and design comments are untrusted content.

Required controls:

```text
UNTRUSTED_TEXT != SHELL
UNTRUSTED_TEXT != TOOL_AUTHORITY
UNTRUSTED_MCP_DESCRIPTION != TRUSTED_TOOL
REVIEW_FINDING_TEXT != REPAIR_COMMAND
DESIGN_COMMENT != EFFECT_AUTHORITY
```

Any process launch or command line assembled from a task/agent/backend record must use structured argument boundaries and the qualified host/spawn contract. String concatenation into a shell is not an accepted implementation shortcut.

Path inputs require canonicalization plus symlink/reparse-point and race-resistant object handling where applicable. A task worktree path, report path, recovery anchor path, design artifact path or session path cannot escape its authorized root through traversal or link substitution.

## 7. Remote workers and SSH are opt-in later profiles

Firstmate remote secondmate mechanisms are useful references for remote-route state, but remote execution is not part of the first local tracer.

A remote worker route requires at minimum:

```text
EXPLICIT_REMOTE_ALLOWED
exact host identity
SSH host-key verification or equivalent authenticated transport identity
principal/project scope
remote working-root identity
source/artifact transfer policy
secret-forwarding policy
network egress grant
route qualification generation
cancel/reconnect/restart semantics
no silent local fallback
```

Network failure, changed host identity or stale route qualification blocks or reconciles the route. It never causes a silent move to a different machine.

## 8. Persisted-state versioning and migration

Any adopted mechanism that persists state must use WePLD-owned, versioned boundaries.

Applicable state includes:

```text
crew/task supervision state
wake/input queue records
Attempt/resume records
serialized operation records
review coverage / finding state
repair/custody/recovery records
calibrated-decision receipts
search progress/result records
collaborative canvas/frame metadata
design-memory/style-rule proposals
```

Every persisted schema declares:

- schema/version identity;
- owner and scope;
- creation/update generation;
- compatibility range;
- migration path;
- unsupported-version failure behavior;
- export/backup behavior where user data is involved;
- deletion/retention behavior;
- rollback/restore behavior.

```text
UNKNOWN_PERSISTED_VERSION -> EXPLICIT_BLOCK
MIGRATION_FAILURE -> OLD_DATA_PRESERVED / NEW_STATE_NONCURRENT
DOWNGRADE_WITHOUT_COMPATIBILITY -> BLOCK
DONOR_DATABASE_SCHEMA != CANONICAL_WEPLD_SCHEMA
```

Doop/PGlite/Postgres state, Unreal session stores, Firstmate flat-file state and no-mistakes gate state are mechanism references, not canonical stores.

## 9. Identity, tenant/project isolation and credentials

Every source-derived mechanism is scoped by canonical principal/project/team identity.

```text
DONOR_USER_ID != CANONICAL_PRINCIPAL_ID
DONOR_SESSION != CANONICAL_WORK_SESSION
MCP_OAUTH_IDENTITY != NAWAT_GRANT
WORKTREE_PATH != TENANT_BOUNDARY
WEBSOCKET_ROOM != AUTHORIZATION_BOUNDARY_BY_ITSELF
```

Required checks at use:

- current principal and project/tenant scope;
- capability/profile enablement;
- current route qualification;
- current credential binding when external access exists;
- Nawat effect authorization for protected effects;
- revocation epoch/generation where applicable.

Credentials never enter model context, review findings, generic logs, design comments, search results or exported diagnostic bundles. Provider tokens and MCP/OAuth credentials remain host-owned opaque bindings.

## 10. Collaborative design isolation and conflict semantics

A Doop-inspired collaborative surface requires more than iframe sandboxing and presence.

The profile must define:

```text
canvas/workspace identity
frame/artifact identity + version
author/agent attribution
ACL generation
presence session generation
operation/edit ID
causal/order metadata or deterministic server ordering
conflict/retry semantics
undo/redo ownership
comment anchor versioning
share-link state + revocation
```

Required failures:

```text
STALE_ACL_GENERATION -> EDIT_REJECTED_OR_REAUTHORIZED
REVOKED_SHARE_LINK -> NO_NEW_SESSION
DUPLICATE_EDIT_ID -> ONE_ACCEPTED_EDIT
RECONNECT_REPLAY -> NO_DUPLICATE_EDIT
STALE_FRAME_VERSION + CONFLICTING_EDIT -> EXPLICIT_CONFLICT / REBASE_FLOW
PRESENCE_EVENT -> NOT_DURABLE_CONTENT_AUTHORITY
IFRAME_ESCAPE_ATTEMPT -> BLOCK
CROSS_CANVAS_OBJECT_REFERENCE -> SCOPE_CHECK
```

Frame HTML/CSS/JS is untrusted active content. Network access from frames is denied by default unless a separately qualified profile allows exact destinations. Clipboard, download, navigation, storage and credential exposure are explicit capabilities, not iframe defaults.

Design-memory/style-rule distillation produces a proposal with provenance. It never silently rewrites durable project policy.

## 11. Assurance independence and repair semantics

no-mistakes review mechanics are useful only if they preserve WePLD review independence.

```text
SAME_BUILDER_REVIEWING_OWN_PATCH != INDEPENDENT_REVIEW
DIFFERENT_WRAPPER_SAME_BACKEND != INDEPENDENCE_PROOF
REVIEW_COVERAGE_COMPLETE != REVIEW_CORRECT
REVIEW_FINDING != COMPLETION_DECISION
```

Review evidence records reviewer/provider/model/tool identity, target base/head/tree, changed-path coverage, limitations and freshness.

A repair creates a new target identity. Prior review/test/security evidence is reused only when its canonical contract explicitly proves that the evidence remains valid for the new target; otherwise affected evidence is refreshed.

Mechanical repair allowlists are narrow, deterministic and separately authorized. Anything that changes product intent, security policy, dependency/source choice, authority, data handling or acceptance criteria is not a mechanical repair.

## 12. Runtime liveness, progress and completion separation

Firstmate/Unreal liveness signals strengthen observation but never decide completion.

```text
PANE_ACTIVITY != WORK_PROGRESS
FILE_WRITE != ACCEPTED_PROGRESS
HEARTBEAT != EFFECT_SUCCESS
QUEUE_DRAIN != TASK_COMPLETION
PROCESS_EXIT_0 != TRUSTED_COMPLETION
OPERATION_EXECUTED != OUTCOME_ACCEPTED
```

Mission Runtime owns structured Attempt state. A liveness observation includes source, timestamp/generation and confidence/classification. Unknown or contradictory evidence remains explicit.

Dead, missing, paused, externally waiting, human-decision waiting, busy, wedged and unknown are distinct states. Automated recovery may occur only for the exact classes and retry-safe effects allowed by the owning task contract.

## 13. Resource governance

Each qualified profile freezes finite limits. Defaults are conservative and user/project policy may lower them.

### Crew / supervision

```text
max workers
max nested delegation depth
max active worktrees
max queued wakes/events
watch/poll resource budget
stale/wedge thresholds
max automatic restart/recovery attempts
max report/output bytes
```

### Assurance / repair

```text
max review passes
max focused coverage-completion passes
max repair cycles
max changed paths/bytes per review unit
max CI/log bytes retained in context
max retry attempts per external check
```

### Async operations

```text
max concurrent operations
max serialized operation bytes
max session history/context bytes
max tool output bytes
max retry count
wall-clock deadline
cancel/reconciliation deadline
```

### Decision/search

```text
max files
max file bytes
max chunks
max chunk bytes
max concurrent decision calls
max total decision/model budget
confidence/abstention profile
search wall-clock deadline
```

### Collaborative design

```text
max canvases/frames in active session
max frame source bytes
max live collaborators/agents
max queued edits/comments
event/history retention budget
frame execution CPU/time/memory budget where enforceable
```

Exhausting a bound is an explicit bounded failure/partial result. It does not silently lift the bound or move to a more expensive/remote route.

## 14. Receipts, audit and observability

Every material source-derived action emits structured evidence owned by canonical WePLD components.

Minimum fields where applicable:

```text
principal/project/work/task/attempt identity
capability/profile ID + revision
route qualification ID + generation
source candidate/revision/path set used
input/event/operation/edit ID
Nawat decision / effect identity for protected effects
target base/head/tree for code/review flows
status/result + start/end timestamps
resource usage / budget settlement
coverage/provenance limitations
cancel/retry/recovery relation
successor/predecessor relation
```

Audit data is minimized. Raw prompts, source bodies, model context, credentials and design contents are not duplicated into generic audit events unless a specific evidence contract requires them.

Receipts are evidence, not authority or completion.

## 15. Hosted-route privacy and egress

Hosted classifier/model routes are disabled under `LOCAL_ONLY` and require explicit policy under `EXPLICIT_REMOTE_ALLOWED`.

Before first use, the route qualification records:

- exact provider/service/endpoint identity;
- data categories allowed to leave the machine;
- credential binding;
- retention/training-use assumptions or documented unknowns;
- transport/security requirements;
- timeout/retry behavior;
- region/residency constraints if applicable;
- user-visible indicator that remote processing is active.

```text
HOSTED_ROUTE_AVAILABLE != HOSTED_ROUTE_ALLOWED
PROVIDER_PRIVACY_CLAIM != WEPLD_POLICY
UNKNOWN_RETENTION + SENSITIVE_DATA -> BLOCK_UNLESS_EXPLICIT_POLICY_ACCEPTS
```

No remote route receives repository-wide content when a narrower selected evidence slice suffices.

## 16. Supply-chain and import strategy

Permission to copy entire repositories does not make bulk import desirable.

Preferred order:

1. reimplement small generic mechanisms from the specification/behavior when cheaper and safer;
2. adapt selected path-level code with provenance and tests;
3. vendor a narrow module only when maintenance/security benefits justify it;
4. import a larger subsystem only when benchmarked against the narrower alternatives and explicitly accepted.

Every selected import freezes:

```text
exact source revision/tree/blob/path set
public license/NOTICE + founder custom-rights evidence if relied upon
transitive dependency lock
build scripts / codegen / install hooks
network-at-build/runtime behavior
generated files and generators
native binaries / downloaded assets
model/weight/tokenizer identity where relevant
SBOM/provenance record where the owning task requires it
known advisories/maintenance observation
removal/replacement plan
```

Do not execute donor install scripts, containers, package postinstall hooks or remote-code loaders merely to inspect them.

## 17. Rollout, rollback and removal

Every source-derived capability ships behind an independently controllable profile/feature state until its release gate is satisfied.

Suggested rollout progression:

```text
DISABLED
-> DISCOVERABLE_UNQUALIFIED
-> QUALIFIED_TEST_ONLY
-> USER_OPT_IN
-> DEFAULT_AVAILABLE
```

No step is automatic solely because the previous one passed.

Rollback/removal must answer:

- how to disable new execution immediately;
- which persisted data remains readable;
- how pending attempts/operations are reconciled;
- how source/dependency packages are removed;
- how users export/delete capability-specific data;
- whether downgrade is supported or blocked;
- how old receipts remain interpretable after removal;
- what fallback, if any, is explicitly qualified.

```text
ROLLBACK != HISTORY_REWRITE
REMOVE_PROVIDER != DELETE_USER_DATA
DISABLE_CAPABILITY != DELETE_EVIDENCE
UNINSTALL_DONOR != INVALIDATE_HISTORICAL_RECEIPTS
```

## 18. Fault-injection and conformance matrix

Each owning implementation task selects applicable cases; these are mandatory planning inputs, not claims that they already pass.

| Area | Required injected failures |
|---|---|
| crew supervision | duplicate wake; lost wake; restart during dispatch; stale worker after successor; declared wait; dead endpoint; unknown liveness; worktree cleanup with dirty/private state |
| remote route | DNS/transport failure; changed host key/identity; disconnect during effect; reconnect to stale Attempt; denied egress; unavailable remote with local route present |
| assurance | partial review coverage; fabricated reviewed path; stale head; same-backend correlated reviewer; CI repair changes intent; repair conflicts with upstream; missing custody artifact |
| Git/publication | remote head moves; merge conflict; attempted force-push; unpublished private commit; branch deleted/recreated; exact-head evidence stale |
| async operations | duplicate input; duplicate operation; crash before/after persistence cut; cancel race; unknown external outcome; unsupported session version; output truncation |
| decision/search | malformed criteria; parser ambiguity; adversarial file names; symlink/path escape; huge/binary input; provider timeout; confidence miscalibration; all routes unavailable; LOCAL_ONLY with hosted route configured |
| collaborative design | revoked user during session; revoked share link; duplicate/reordered edit; reconnect replay; malicious frame; cross-canvas reference; stale ACL; provider unavailable; design-memory poisoning |
| persistence | interrupted migration; partial write; checksum/version mismatch; downgrade attempt; backup/restore from older schema |

Unknown external-effect outcome always reconciles before retry.

## 19. Implementation-ready leaf manifest

Before an owning task writes product code, its bounded manifest must resolve these fields for the exact leaf:

```text
LEAF_ID
CAPABILITY_ID
USER_SETTING = OFF / ASK / AUTO
LOCALITY = LOCAL_ONLY / LOCAL_PREFERRED / EXPLICIT_REMOTE_ALLOWED
OWNER
DEPENDENCIES_ACCEPTED
EXACT_ALLOWED_PATHS
SOURCE_RECORD + SELECTED_REVISION + SELECTED_PATHS
RIGHTS_BASIS
DEPENDENCIES / BUILD_HOOKS
CANONICAL_TYPES_USED
PERSISTED_STATE_SCHEMA_VERSION
IDENTITY / TENANT / PROJECT SCOPE
RESOURCE_BOUND_PROFILE
NAWAT_EFFECT_CLASS_IF_ANY
DATA / SECRET / EGRESS POLICY
POSITIVE_FIXTURES
NEGATIVE_ORACLES
FAULT_INJECTION_CASES
BENCHMARK_BUDGET_OR_NOT_APPLICABLE
MIGRATION / RECOVERY / ROLLBACK / REMOVAL
OBSERVABILITY / RECEIPTS
PLATFORM_MATRIX
INDEPENDENT_REVIEW_REQUIREMENT
SECURITY_REVIEW_REQUIREMENT
RELEASE_CLAIM
RESIDUAL_LIMITATIONS
```

Missing required fields block the leaf instead of being delegated to implementation-time guessing.

## 20. First implementation order after canonical acceptance

This amendment does not override the live frontier. When dependencies and exact grants permit, the preferred source-expansion order is:

```text
1. A09 source records for all selected candidates
2. A05/A08 bounded Unreal + Firstmate runtime/recovery mechanism qualification
3. A07/A08 bounded no-mistakes assurance/recovery mechanism qualification
4. A04/A05 bounded local decision/search mechanism qualification
5. only then source-specific implementation through existing F/U/R/Q/S/K/T/P/H tasks as their graph dependencies become accepted
6. Doop collaborative surface only after principal/scope, context and effect seams needed by its profile are accepted
```

This ordering maximizes value without pulling late product profiles into the first runtime loop.

## 21. Final readiness criteria

The source-expansion planning amendment is implementation-ready only when all statements below are true for the accepted exact head:

```text
SOURCE_IDENTITIES_PINNED_OR_EXPLICITLY_DEFERRED_TO_OWNING_ACQUISITION = YES
CONFLICTING_PLANNING_PINS_RECONCILED = YES
PUBLIC_RIGHTS_AND_FOUNDER_RIGHTS_BOUNDARY_EXPLICIT = YES
CANONICAL_OWNER_PER_CAPABILITY = YES
TASK_OWNER_PER_IMPLEMENTATION_LEAF = YES
DEPENDENCY_ORDER_EXPLICIT = YES
USER_CAPABILITY_CONTROLS_EXPLICIT = YES
LOCALITY_AND_NO_SILENT_FALLBACK_EXPLICIT = YES
WINDOWS_FIRST_PORTABILITY_RULE_EXPLICIT = YES
NO_SHARED_HISTORY_REWRITE_RULE_EXPLICIT = YES
PERSISTED_STATE_VERSIONING_EXPLICIT = YES
IDENTITY_AND_TENANT_SCOPE_EXPLICIT = YES
SECURITY_NEGATIVE_ORACLES_EXPLICIT = YES
RESOURCE_BOUNDS_EXPLICIT = YES
FAULT_INJECTION_PLAN_EXPLICIT = YES
OBSERVABILITY_RECEIPTS_EXPLICIT = YES
HOSTED_EGRESS_BOUNDARY_EXPLICIT = YES
SUPPLY_CHAIN_IMPORT_RULES_EXPLICIT = YES
ROLLOUT_ROLLBACK_REMOVAL_EXPLICIT = YES
BENCHMARK_OWNERSHIP_EXPLICIT = YES
NO_NEW_TASK_IDS = YES
NO_NEW_AUTHORITY_ROOTS = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

These are planning-readiness statements, not implementation/test PASS claims.

Canonical acceptance additionally requires the repository's normal exact-head deterministic validation, qualified independent review, material-finding reconciliation, guarded merge and post-merge integrity.

```text
PLANNING_CONTENT_COMPLETE = YES
KNOWN_UNOWNED_IMPLEMENTATION_PLANNING_GAPS = 0
IMPLEMENTATION_READY = ONLY_AFTER_EXACT_HEAD_INDEPENDENT_REVIEW_AND_CANONICAL_ACCEPTANCE
REVIEW_UNAVAILABLE_OUTCOME = REVIEW_BLOCKED
```
