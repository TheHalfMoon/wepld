# Contract — Worker Delegation Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
PROCESS_EXECUTION_AUTHORITY = NONE
```

## Purpose

Provide one WePLD-owned delegation boundary for local, hosted, CLI, SDK, protocol, model, tool, and custom workers without making provider-native permissions or sessions authoritative.

## User surface

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
/handoff --to <worker>
```

`/delegate` assigns bounded work. `/handoff` transfers durable context/session responsibility. They are distinct operations.

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
