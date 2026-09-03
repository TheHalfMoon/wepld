# Omnigent Execution-Fabric Integration Tasks

```text
STATUS = FUTURE_PLANNING_TASK_MAP
SOURCE = omnigent-ai/omnigent@f4e93c2b74158a2712d07f13e591abb90a999171
SOURCE_ADMISSION = NONE
IMPLEMENTATION_AUTHORITY = NONE
CURRENT_ACTIVE_SLICE = S2
```

This task map converts the qualified Omnigent mechanism study into dependency-ordered WePLD-native work. It does not authorize any task before its owning canonical slice activates it.

## S3 — process, host, containment, native-boundary foundation

### OM-S3-001 — Host / runner identity contracts

Implement future typed identities equivalent to the planning `HostDescriptor` and `RunnerDescriptor`.

Acceptance:

```text
ServerIdentity != HostIdentity != RunnerIdentity != WorkerIdentity != AttemptIdentity
server connection cannot auto-enable hosting
host registration is explicit
host liveness and runner liveness are distinct
```

### OM-S3-002 — Containment posture vocabulary

Implement a multidimensional containment observation rather than boolean `sandboxed`.

Required dimensions:

```text
process tree
filesystem
network
namespace/container
syscall/seccomp where relevant
home/config visibility
write mounts
known downgrade/limitations
```

Negative oracle: process-tree-only containment must never satisfy a hard filesystem/network sandbox requirement.

### OM-S3-003 — Required-sandbox fail-loud behavior

If a selected/required containment backend is unavailable, refuse execution rather than silently running unsandboxed.

### OM-S3-004 — Environment exposure policy

Deny-by-default process environment with explicit baseline, adapter-family, and assignment passthrough rules.

Negative oracles:

```text
ambient provider A key cannot reach provider B worker
raw host environment cannot become evidence/context
unknown generic ACP adapter gets no vendor secret family automatically
```

### OM-S3-005 — Native desktop bridge contract

Qualify a narrow native bridge with sender/application-origin checks, serialization-safe schemas, and no raw IPC/Node/shell exposure.

No remote SPA page receives general native authority.

### OM-S3-006 — Credential broker feasibility/security spike

Design only the smallest WePLD credential-capability boundary needed for later S6/S8. Do not implement network credential injection merely because the planning contract exists.

Deliverables:

- threat model;
- target canonicalization model;
- broker/secret-store separation;
- no-proxy-bypass requirements;
- placeholder/non-secret semantics;
- audit/usage-receipt contract;
- Windows/Linux/macOS feasibility matrix;
- decision: clean-room implementation vs admitted source reuse vs reject.

## S5 — protocol and capability dry-run

### OM-S5-001 — Harness protocol capability schema

Construct `HarnessProtocolAdapter` + `HarnessDialectExtension` fixtures without executing any model/provider/process.

Test:

```text
ACP-like generic protocol
vendor dialect adds subagent metadata
unknown extension field remains opaque
extension cannot create effect class or Nawat authority
```

### OM-S5-002 — Execution-envelope dry-run

Given synthetic Server/Host/Runner/Worker/Assignment/Route/Nawat fixtures, compute the intersection-based `ExecutionEnvelope` without execution.

Prove a weaker lower-trust config cannot widen a deployment runtime ceiling.

## S6 — Mission Runtime / UWC execution fabric

### OM-S6-001 — Explicit host opt-in and runner registration

Implement host/runner lifecycle under canonical authority.

Required states:

```text
HOST_UNREGISTERED
HOST_REGISTERED_UNQUALIFIED
HOST_QUALIFIED_OFFLINE
HOST_QUALIFIED_ONLINE
RUNNER_STARTING
RUNNER_READY
RUNNER_DRAINING
RUNNER_OFFLINE
RUNNER_ORPHANED_OR_UNKNOWN
```

Exact state names may change under owning Spec Kit, but semantics must remain explicit.

### OM-S6-002 — Generic protocol executor seam

Implement one protocol-pure adapter path plus typed vendor/dialect extensions. Do not scatter vendor-name branches through Mission Runtime.

### OM-S6-003 — Capability negotiation and conformance

Require exact adapter/dialect capabilities and version identity before routing.

Unknown semantics are unsupported/opaque, never inferred from branding.

### OM-S6-004 — No silent runner/worker/model fallback

A requested route becoming unavailable produces blocked/requalification/explicit-alternative state, not silent substitution.

### OM-S6-005 — Runtime ceiling enforcement

Enforce intersection of deployment ceiling, project/workspace constraints, Assignment, WorkerRequirement, RouteQualification, and Nawat grant.

### OM-S6-006 — Credential capability broker, if admitted

Only after S3 security/source qualification and network authority exist:

- keep reusable secret outside worker when feasible;
- bind credential use to exact target/attempt/egress/Nawat grant;
- use non-secret placeholders only when required by a client;
- refuse wrong-target replay;
- emit credential-use receipt without secret content;
- revoke on attempt/grant expiry;
- fail closed on broker/route uncertainty.

### OM-S6-007 — Cost/budget hierarchy

Normalize budget evidence at appropriate scopes:

```text
Attempt
Assignment
Case/subtree
user/workspace/day where policy requires
```

Budget policy can narrow/ask/block but never creates authority. Paid fallback remains explicit.

### OM-S6-008 — Recovery and runner restart semantics

Transport/session reconnection must not imply safe Attempt resume. Revalidate current runner identity, context, containment, route qualification, grants, and unknown effects first.

## Browser integration — future owning slices

### OM-WEB-001 — Browser snapshot observation

Add `BrowserSnapshotObservation` and `BrowserElementRef` to the canonical web boundary.

### OM-WEB-002 — Exact snapshot-bound action

A ref-based click/type/submit must bind exact:

```text
browser session
browser context
origin
document/snapshot identity
element ref
input identity
Nawat grant
```

Navigation/snapshot supersession blocks stale action.

### OM-WEB-003 — Schema advertisement vs execution

Browser/tool schemas advertise capabilities only. Actual execution remains in the qualified runner/browser adapter path.

Negative oracle: a schema-only tool object cannot execute merely because a worker calls it through the wrong path.

## S7 — review and assurance

### OM-S7-001 — Typed `ReviewIndependenceReceipt`

Record builder/reviewer identity separation as evidence, not prose.

At minimum bind:

```text
reviewed target
builder attempts/workers/provider-model-harness identities
reviewer attempt/worker/provider-model-harness identity
shared context
excluded context
independence policy
conflict checks
evidence
result
```

### OM-S7-002 — Independence policies

Support policies stronger than `different vendor`, for example:

- different worker identity;
- different model family/provider when required;
- no mutable builder worktree/process inheritance;
- review context limited to exact target + contract + required architecture evidence;
- reviewer has no acceptance-critical write authority;
- reviewer cannot review its own generated repair.

### OM-S7-003 — Assurance receipt integration

`ClaimAssessment` consuming independent review must reference a current `ReviewIndependenceReceipt` satisfying the selected AssurancePolicySnapshot.

## S8 — controlled effects / repair / landing

### OM-S8-001 — Effect dependency graph

Represent prerequisite/dependent effect ordering explicitly.

### OM-S8-002 — Unknown prerequisite blocks irreversible dependent effect

Test:

```text
prerequisite unavailable -> dependent destructive effect not started
prerequisite outcome unknown -> dependent destructive effect not started
```

### OM-S8-003 — Reconciliation before retry

Credentialed network/provider/browser operations with unknown outcome must reconcile postcondition/idempotency state before retry when duplicate effects are possible.

### OM-S8-004 — Compensation semantics

If compensation exists, record it as a separate authorized effect. `COMPENSATED` must not rewrite historical evidence to `ORIGINAL_EFFECT_NOT_APPLIED`.

## S9 — evidence and recovery

### OM-S9-001 — Host/runner/execution lineage

Quality Passport / timeline must preserve:

```text
server identity
host identity
runner runtime identity
worker/harness/model identity
containment posture
environment policy
credential capability use
route qualification
Nawat grants
Attempt lineage
```

### OM-S9-002 — Credential-use receipts

Persist only bounded non-secret usage evidence. Raw credentials/placeholders are not durable evidence unless a specific security investigation policy requires a protected identity hash/reference.

### OM-S9-003 — Recovery replay

A recovered session must be able to distinguish transport recovery, runtime recovery, Attempt resume eligibility, authority revalidation, and external-effect reconciliation.

## Cross-cutting negative-oracle suite

```text
OMNI_N_SERVER_CONNECTION_CANNOT_ENABLE_HOST
OMNI_N_HOST_ONLINE_CANNOT_CREATE_ROUTE_AUTHORITY
OMNI_N_RUNNER_CHANGE_CANNOT_KEEP_STALE_QUALIFICATION
OMNI_N_EXTENSION_CANNOT_GRANT_EFFECT
OMNI_N_RUNTIME_CEILING_CANNOT_BE_WIDENED_DOWNSTREAM
OMNI_N_PROCESS_TREE_ONLY_CANNOT_SATISFY_HARD_SANDBOX
OMNI_N_REQUIRED_SANDBOX_MISSING_CANNOT_RUN_UNSANDBOXED
OMNI_N_AMBIENT_SECRET_CANNOT_LEAK_TO_UNRELATED_WORKER
OMNI_N_PLACEHOLDER_CANNOT_AUTHENTICATE_WRONG_TARGET
OMNI_N_CREDENTIAL_BROKER_CANNOT_INJECT_WITH_EXPIRED_GRANT
OMNI_N_SNAPSHOT_SUPERSESSION_BLOCKS_REF_ACTION
OMNI_N_DIFFERENT_VENDOR_ALONE_NOT_REVIEW_INDEPENDENCE
OMNI_N_RECONNECTED_RUNNER_NOT_AUTO_SAFE_RESUME
OMNI_N_UNKNOWN_PREREQUISITE_BLOCKS_IRREVERSIBLE_DEPENDENT_EFFECT
OMNI_N_FOREIGN_DESKTOP_ORIGIN_CANNOT_USE_PRIVILEGED_BRIDGE
```

## Activation rule

Every task remains planning-only until its owning slice grants exact implementation/source/dependency/process/network paths. Omnigent's source availability and Apache-2.0 license do not activate any task.