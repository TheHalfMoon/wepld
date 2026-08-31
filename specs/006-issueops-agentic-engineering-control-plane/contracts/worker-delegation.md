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

## User surface

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
/handoff --to <worker>
```

`/delegate` assigns bounded work. `/handoff` transfers durable context/session responsibility. They are distinct operations. Early UX may expose `/handoff` and detailed `/workers` controls as advanced surfaces while keeping `/delegate` as the primary assignment intent.

## Worker descriptor requirements

A qualified worker description must cover:

```text
worker_id
adapter_kind
provider_identity?
model_identity?
version_identity?
capabilities[]
supported_effect_classes[]
provider_permission_claims[]
containment_claims[]
containment_evidence[]
session_semantics
cancellation_semantics
recovery_semantics
cost_class
quota_class
availability
qualification_state
qualification_evidence[]
qualification_expiry?
```

## Delegation flow

```text
WorkflowIntent / Assignment
-> required capabilities + proposed effect classes
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

Mirefa consumes assignment/topology requirements plus observed worker/route evidence and determines whether a candidate route is **qualified for consideration**. Qualification is evidence, not effect authority.

Candidate `RouteQualification` fields:

```text
route_qualification_id
assignment_id
worker_id
adapter_identity
provider_identity?
model_identity?
matched_capabilities[]
candidate_effect_classes[]
containment_evidence_refs[]
provider_permission_claim_refs[]
egress_class
cost_class
quota_state
availability_observation
qualification_conditions[]
qualification_evidence_refs[]
qualified_at
expires_at?
```

Success means only:

```text
ROUTE_QUALIFIED_FOR_CONSIDERATION
```

Representative fail-closed states:

```text
CAPABILITY_MISMATCH
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

A Nawat decision that depends on a route must reference the exact current `RouteQualification` (or an equivalent qualified route snapshot) plus the Assignment, exact target, effect class, and current evidence. A stale or mismatched qualification requires requalification; it is not silently refreshed by Nawat or Mission Runtime.

## Nawat decision contract

Nawat owns effect-time authority and revalidation. It evaluates one proposed effect (or a precisely bounded grant scope when canonical policy permits) against the complete current snapshot.

Candidate `NawatDecision` inputs:

```text
effect_proposal_id
assignment_id
attempt_id?
workflow_intent_ref
autonomy_ceiling
exact_target
proposed_input_identity
proposed_effect_class
route_qualification_ref?
containment_precondition_refs[]
current_project_case_state_refs[]
provider_target_freshness_ref?
cost_or_egress_constraints[]
controlling_policy_refs[]
```

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
attempt_id
selected_worker_id
route_qualification_ref
context_package_manifest_ref
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
- hide a Nawat denial behind generic provider errors.

Representative runtime transitions:

```text
ATTEMPT_READY
ATTEMPT_STARTED
ATTEMPT_BLOCKED_AUTHORITY
ATTEMPT_BLOCKED_QUALIFICATION
ATTEMPT_CANCELLED
ATTEMPT_FAILED_RUNTIME
ATTEMPT_FINISHED
```

A route change, retry, or reassignment creates a new Attempt and, where relevant, fresh qualification/authority evidence.

## Explicit worker request

`--to <worker>` is a routing preference/request. It must not bypass:

- availability;
- capability match;
- qualification freshness;
- containment requirements;
- cost/quota policy;
- effect authority;
- egress policy;
- independent-review requirements.

If the requested route is unavailable or disallowed, fail closed or surface an explicit alternative decision. Do not silently substitute.

## Context package

A worker should receive the minimum sufficient package for its Assignment, potentially including:

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

Every package should also carry a manifest that identifies source/trust class and visibility for each included artifact. Untrusted issue/RAG/provider content remains data and cannot become worker-control instructions merely because it is present in the package.

Repository-wide or collection-wide context should not be sent when a smaller qualified package is sufficient.

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

Retrying the same worker or assigning another worker creates a new `Attempt`. Prior attempts, effects, failures, findings, and evidence remain append-only history.

## Parallelism

Edara may schedule independent frontier tasks concurrently only when dependencies, shared effects, repository topology, resource limits, and authority permit. Parallelism is never a goal by itself.

## Review separation

An implementer attempt cannot satisfy the independently qualified review requirement for its own acceptance-critical work. Review workers are separately routed/qualified and produce findings, not completion authority.

## Adapter conformance

Future adapters inspired by `amElnagdy/delegate-skills` should be tested against a common conformance suite covering:

- identity/version reporting;
- capability discovery;
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
- failure and retry evidence.

## Required boundary negative oracles

```text
QUALIFIED_ROUTE_WITHOUT_NAWAT_GRANT_CANNOT_EFFECT
NAWAT_DENIAL_IS_VISIBLE_AND_EFFECT_FREE
STALE_ROUTE_QUALIFICATION_REQUIRES_REQUALIFICATION
MISSION_RUNTIME_CANNOT_WIDEN_GRANT
MISSION_RUNTIME_CANNOT_SILENTLY_SUBSTITUTE_WORKER
PROVIDER_TOOL_SUCCESS_CANNOT_CREATE_AUTHORITY
UNTRUSTED_CONTEXT_INSTRUCTION_CANNOT_EXPAND_ASSIGNMENT_OR_EFFECTS
```
