# Contract — Worker Delegation Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
PROCESS_EXECUTION_AUTHORITY = NONE
```

## Purpose

Provide one WePLD-owned delegation boundary for local, hosted, CLI, SDK, protocol, model, tool, and custom workers without making provider-native permissions or sessions authoritative.

The components named here are semantic contracts and trust boundaries. They do not require separate processes/services in the first tracer bullets; an implementation may co-locate them while preserving the distinct inputs, outputs, failure states, evidence, and authority semantics below.

Shared `WorkerRequirement`, `WorkerDescriptor`, `Assignment`, `Attempt`, `RouteQualification`, `ContextPackage`, and effect records use the canonical field vocabulary in `../data-model.md`.

## User surface

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
/handoff --to <worker>
```

`/delegate` assigns bounded work. `/handoff` transfers durable context/session responsibility. They are distinct operations. Early UX may expose `/handoff` and detailed `/workers` controls as advanced surfaces while keeping `/delegate` as the primary assignment intent.

## Worker requirement

A routing request is represented by canonical `WorkerRequirement`, not an untyped list of provider features. It includes required/prohibited effect classes, containment, platform/runtime, egress, cost/quota, independence, and session requirements.

```text
WORKER_REQUIREMENT != WORKER_SELECTION
WORKER_REQUIREMENT != ROUTE_QUALIFICATION
WORKER_REQUIREMENT != EFFECT_AUTHORITY
```

## Worker descriptor requirements

A qualified worker description follows the canonical `WorkerDescriptor` and must cover:

```text
worker_id
adapter_kind
provider_identity?
model_identity?
version_identity?
capability_vocabulary_version
capabilities[]
supported_effect_classes[]
provider_permission_claims[]
containment_claims[]
containment_evidence_refs[]
session_semantics
cancellation_semantics
recovery_semantics
cost_class
quota_class
availability
qualification_state
qualification_evidence_refs[]
qualification_expiry?
```

Provider-native capability labels are mapped into a versioned WePLD capability vocabulary. Unknown capability semantics remain unknown rather than silently creating a new effect class.

## Delegation flow

```text
WorkflowIntent / Assignment
-> WorkerRequirement + proposed effect classes
-> Edara minimum-sufficient topology
-> Mirefa route/worker qualification
-> Nawat effect-time grant/revalidation
-> Mission Runtime attempt
-> UWC adapter
-> worker/provider execution
-> normalized events/results/effects
-> deterministic checks
-> Assurance
-> Trusted Completion / next frontier
```

No arrow implies authority inheritance. Each boundary below has an explicit contract.

## Edara -> Mirefa contract

Edara proposes the **minimum-sufficient work topology**. It does not qualify workers and does not grant effects.

Candidate `TopologyProposal` fields:

```text
topology_id
assignment_refs[]
worker_requirement_refs[]
dependency_edges[]
required_capability_sets[]
proposed_effect_classes[]
concurrency_constraints[]
resource_constraints[]
independence_requirements[]
selection_rationale
created_from_intent_ref
```

Required success state:

```text
TOPOLOGY_PROPOSED
```

Representative failure/abstention states:

```text
INSUFFICIENT_TASK_DEFINITION
UNRESOLVED_DECISION_BOUNDARY
UNSAFE_PARALLELISM
NO_MINIMUM_SUFFICIENT_TOPOLOGY
```

Edara must not silently add work solely to occupy extra agents.

## Mirefa qualification contract

Mirefa consumes assignment/topology/WorkerRequirement plus observed worker/route evidence and determines whether a candidate route is **qualified for consideration**. Qualification is evidence, not effect authority.

The canonical `RouteQualification` in `../data-model.md` is controlling. Provider/model identity and permission claims remain reachable through the exact `WorkerDescriptor` and its qualification evidence rather than being duplicated as mutable route identity.

Success means only:

```text
ROUTE_QUALIFIED_FOR_CONSIDERATION
```

Representative fail-closed states:

```text
CAPABILITY_MISMATCH
CAPABILITY_VOCABULARY_MISMATCH
QUALIFICATION_STALE
CONTAINMENT_EVIDENCE_INSUFFICIENT
ROUTE_UNAVAILABLE
COST_OR_QUOTA_BLOCKED
EGRESS_ROUTE_UNQUALIFIED
PROVIDER_IDENTITY_MISMATCH
ADAPTER_CONFORMANCE_FAILED
```

Mirefa MUST NOT return `ALLOW_EFFECT`, broaden an Assignment, change the autonomy ceiling, or represent provider-native read-only/sandbox claims as WePLD authority.

## Mirefa -> Nawat evidence handoff

A Nawat decision that depends on a route must reference the exact current `RouteQualification` plus the Assignment, WorkerRequirement, exact target, effect class, controlling origin, and current evidence. A stale or mismatched qualification requires requalification; it is not silently refreshed by Nawat or Mission Runtime.

## Nawat decision contract

Nawat owns effect-time authority and revalidation. It evaluates one canonical `EffectProposal` (or a precisely bounded grant scope when canonical policy permits) against the complete current snapshot.

The proposal must carry the typed controlling origin from `../data-model.md`:

```text
controlling_origin_kind
controlling_origin_ref
```

Allowed origin kinds are defined by canonical policy and may include an explicit `WorkflowIntent`, `Assignment`, or controlling policy path. Untrusted content, worker/model output, provider text, and retrieved text cannot become a controlling origin merely by asking for an effect.

Candidate decision outcomes:

```text
ALLOW
DENY
APPROVAL_REQUIRED
TRANSFORM_TO_NARROWER_EFFECT
REQUALIFY_REQUIRED
STALE_TARGET
INSUFFICIENT_EVIDENCE
```

An allow decision/grant must bind at least:

```text
grant_id
exact effect class
exact target or bounded target set
input identity / constraints
controlling origin ref
worker or route constraint where relevant
containment preconditions
expiry / revalidation condition
policy/evidence refs
```

Nawat denial is a normal, inspectable workflow outcome. The user-facing Case/Assignment state must show the reason category and next frontier (for example `NEEDS_DECISION`, `REQUALIFICATION_REQUIRED`, `STALE_EVIDENCE`, or `DENIED_BY_POLICY`) rather than presenting the worker as mysteriously broken.

## Mission Runtime contract

Mission Runtime executes/hosts Attempts; it does not infer or widen authority.

Before an effectful attempt or effect step, Mission Runtime must have the exact required grant/revalidation and containment preconditions. It receives:

```text
assignment_ref
worker_requirement_ref
attempt_id
selected_worker_id
route_qualification_ref
context_package_ref
applicable_nawat_grant_refs[]
cancellation/recovery contract
result/evidence contract
```

Mission Runtime MUST NOT:

- substitute another worker/provider/model without a new explicit routing/qualification path;
- widen an effect class or target;
- reuse an expired grant;
- continue after a mandatory revalidation boundary fails;
- treat worker/provider tool success as authorization;
- hide a Nawat denial behind generic provider errors;
- retry an effect whose outcome is unknown until the canonical effect-reconciliation contract permits retry.

Representative runtime transitions:

```text
ATTEMPT_READY
ATTEMPT_STARTED
ATTEMPT_BLOCKED_AUTHORITY
ATTEMPT_BLOCKED_QUALIFICATION
ATTEMPT_RECOVERING
ATTEMPT_BLOCKED_UNKNOWN_EFFECT_OUTCOME
ATTEMPT_CANCELLED
ATTEMPT_FAILED_RUNTIME
ATTEMPT_FINISHED
```

A route change, reassignment, or unsafe-to-resume interruption creates a new Attempt and, where relevant, fresh qualification/authority evidence.

## Cancellation, recovery, and orphan handling

Each worker adapter must declare whether cancellation is acknowledged, best-effort, or externally unverifiable, and whether a session can be safely resumed.

After host/runtime interruption:

1. recover durable Attempt/effect history;
2. determine whether any material effect has `EFFECT_OUTCOME_UNKNOWN`;
3. reconcile unknown effects before retry/reassignment when duplicate effects are possible;
4. prove old worker/session/process ownership is terminated or explicitly classify an orphan/unknown state;
5. create a new Attempt unless safe resume is proven by the adapter/runtime contract.

```text
CANCEL_REQUESTED != CANCELLED_PROVEN
PROCESS_DISCONNECTED != PROCESS_TERMINATED
SESSION_ID_PRESENT != SESSION_SAFE_TO_RESUME
```

## Explicit worker request

`--to <worker>` is a routing preference/request. It must not bypass:

- availability;
- capability match and vocabulary compatibility;
- qualification freshness;
- containment requirements;
- cost/quota policy;
- effect authority;
- egress policy;
- independent-review requirements.

If the requested route is unavailable or disallowed, fail closed or surface an explicit alternative decision. Do not silently substitute.

## Context package

A worker receives the canonical `ContextPackage` from `../data-model.md`. It should contain the minimum sufficient evidence for its Assignment, potentially including:

```text
objective
acceptance criteria
relevant files/symbols
spec/task fragments
decisions/constraints
known failures
reproduction evidence
tests/check commands or contracts
RAG evidence with citations/provenance
allowed/proposed effect classes
target identities
completion/reporting contract
```

The package manifest preserves source identity, trust class, visibility scope, access-policy reference, freshness/generation, redaction/exclusion evidence, policy snapshot, and egress class per the canonical model.

Repository-wide or collection-wide context should not be sent when a smaller qualified package is sufficient. A permission/access revocation after package construction stales the package for future use.

## Provider session identity

Provider session/conversation/run IDs are opaque provenance. They do not become `WorkerId`, WePLD session identity, authorization, or trust.

## Read-only / sandbox claims

Provider-native flags must be classified as claims until independently qualified. For example:

```text
PROVIDER_READONLY_FLAG != WEPLD_CONTAINMENT
PROVIDER_SANDBOX_FLAG != NAWAT_GRANT
PROVIDER_FULL_TRUST_MODE != WEPLD_AUTHORITY
```

A provider whose read-only mode is advisory requires stronger external containment before WePLD may represent the route as contained.

## Cost and quota

Paid/quota/metered execution is explicit worker metadata. Routing must obey controlling policy and user/repository constraints. Silent paid execution and silent paid fallback are prohibited.

## Retry / reassignment

Retrying the same worker or assigning another worker creates a new `Attempt` unless exact safe-resume semantics are independently established. Prior attempts, effects, failures, findings, and evidence remain append-only history.

## Parallelism

Edara may schedule independent frontier tasks concurrently only when dependencies, shared effects, repository topology, resource limits, authority, and conflict domains permit. Parallelism is never a goal by itself.

A future scheduler must expose resource/fairness policy rather than allowing one Case or worker family to starve unrelated qualified work.

## Review separation

An implementer attempt cannot satisfy the independently qualified review requirement for its own acceptance-critical work. Review workers are separately routed/qualified and produce findings/coverage evidence, not completion authority.

## Adapter conformance

Future adapters inspired by `amElnagdy/delegate-skills` should be tested against a common conformance suite covering:

- identity/version reporting;
- capability vocabulary/version and discovery;
- stdin/stdout or API protocol behavior;
- context/brief delivery;
- timeout/cancellation;
- queue/poll/session recovery;
- error normalization;
- output/result capture;
- filesystem/process/network effects;
- read-only/full-trust behavior;
- cost/quota disclosure;
- clean shutdown and orphan handling;
- unknown-effect reconciliation;
- failure and retry evidence.

## Required boundary negative oracles

```text
QUALIFIED_ROUTE_WITHOUT_NAWAT_GRANT_CANNOT_EFFECT
NAWAT_DENIAL_IS_VISIBLE_AND_EFFECT_FREE
STALE_ROUTE_QUALIFICATION_REQUIRES_REQUALIFICATION
WORKER_REQUIREMENT_DOES_NOT_SELECT_OR_AUTHORIZE_WORKER
MISSION_RUNTIME_CANNOT_WIDEN_GRANT
MISSION_RUNTIME_CANNOT_SILENTLY_SUBSTITUTE_WORKER
PROVIDER_TOOL_SUCCESS_CANNOT_CREATE_AUTHORITY
UNTRUSTED_CONTEXT_INSTRUCTION_CANNOT_EXPAND_ASSIGNMENT_OR_EFFECTS
CANCEL_REQUEST_DOES_NOT_PROVE_REMOTE_TERMINATION
UNKNOWN_EFFECT_OUTCOME_BLOCKS_UNSAFE_RETRY
ACCESS_REVOCATION_STALES_CONTEXT_PACKAGE
```
