# Contract — Behavior Policy Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
PRIMARY_OWNER = FUTURE_POLICY_LAYER_UNDER_OWNING_SLICE
EFFECT_AUTHORITY = NAWAT_ONLY
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

## Purpose

Define a future composable behavior-policy layer for cost, workflow, safety, model-selection, organization, and session constraints without allowing policy evaluation to become a second effect-authority system.

Omnigent's `ALLOW` / `ASK` / `DENY` policy choke point is a useful behavior oracle. WePLD adopts the separation below rather than treating that model as Nawat.

## Core invariants

```text
BEHAVIOR_POLICY_ALLOW != NAWAT_GRANT
BEHAVIOR_POLICY_ASK != NAWAT_APPROVAL_RECORD
BEHAVIOR_POLICY_DENY MAY_BLOCK_OR_NARROW
BEHAVIOR_POLICY_TRANSFORM != EFFECT_AUTHORITY
POLICY_MODULE_LOADED != POLICY_TRUSTED
AGENT_PROPOSED_POLICY != ACTIVE_CONTROLLING_POLICY
```

A behavior-policy system is an additional constraint layer. It can never widen the authority already permitted by canonical governance/Nawat.

## `BehaviorPolicyDefinition`

```text
BehaviorPolicyDefinition {
  behavior_policy_id
  policy_kind
  policy_version
  policy_source_class
  policy_source_identity
  configuration_identity
  applicable_scope
  evaluation_phases[]
  input_schema_identity
  output_schema_identity
  state_mutation_capability
  external_effect_capability
  trust_classification
  source_admission_ref?
  dependency_admission_ref?
  qualification_evidence_refs[]
}
```

Candidate `policy_source_class` values:

```text
WEPLD_BUILTIN_DECLARATIVE
QUALIFIED_CONSTRAINED_EXPRESSION
QUALIFIED_SANDBOXED_PLUGIN
TRUSTED_NATIVE_EXTENSION
EXTERNAL_OR_UNTRUSTED_POLICY_CANDIDATE
```

No implementation technology is selected by these names. The owning Source Acquisition gate decides whether CEL/WASM/native/plugin machinery is needed.

## `BehaviorPolicyEvaluation`

```text
BehaviorPolicyEvaluation {
  evaluation_id
  behavior_policy_ref
  policy_snapshot_ref
  workflow_or_attempt_ref
  evaluation_phase
  exact_input_identity
  actor_identity?
  worker_or_route_identity?
  result
  reason_code
  proposed_transform_identity?
  proposed_state_updates[]
  evidence_refs[]
  evaluated_at
}
```

Candidate result vocabulary:

```text
NO_OBJECTION
DENY
REQUIRE_SEPARATE_APPROVAL_PATH
TRANSFORM_TO_NARROWER_REQUEST
UNAVAILABLE
ERROR
STALE
```

The user-facing UI may render friendlier `ALLOW/ASK/DENY` language, but canonical semantics MUST preserve that `NO_OBJECTION` is not effect authority.

## Mandatory pre-effect policy availability

If a controlling policy is configured as a mandatory pre-effect gate and it cannot be evaluated, execution fails closed.

```text
MANDATORY_PRE_EFFECT_POLICY_UNAVAILABLE -> EFFECT_BLOCKED
```

A post-effect/advisory policy cannot retroactively claim that an already-incurred effect was prevented.

## Policy precedence

Policy layers may include organization/server, workspace/project, agent/workflow, and session/user scopes.

The precedence rule must be explicit and versioned. A lower-trust layer cannot weaken a stronger controlling restriction.

```text
EFFECTIVE_BEHAVIOR_POLICY = INTERSECTION_OR_MONOTONIC_NARROWING
```

If two policies conflict in a way the owning semantics cannot safely resolve, the result is blocked/needs-decision rather than latest-write-wins.

## State updates

Behavior-policy-local state (for example counters or remembered warning checkpoints) must be distinct from authority state.

```text
POLICY_STATE_UPDATE != GRANT
POLICY_LABEL != EFFECT_AUTHORITY
```

Any durable policy state that influences later decisions needs provenance, version, access, and migration semantics.

## Custom/executable policy code

Repository content, agent-generated Python/JavaScript, downloaded modules, or user-provided arbitrary executable policy code MUST NOT auto-load as trusted policy.

Loading executable policy code may itself require:

```text
source admission
dependency admission
process/runtime qualification
containment
network restrictions
secret/environment handling
exact policy identity
security review
```

Default product preference:

1. WePLD-native declarative/builtin policy;
2. constrained deterministic expression/evaluator if justified;
3. sandboxed plugin only when required and qualified;
4. trusted native extension as an explicit high-trust route;
5. arbitrary executable policy loading is not a default architecture path.

## Agent/session policy proposals

An agent MAY propose a stricter policy or request that the user enable one, but cannot self-activate a policy that widens its own capabilities or changes canonical authority.

```text
AGENT_POLICY_PROPOSAL -> USER_OR_CONTROLLING_POLICY_DECISION
```

A session policy can add/narrow gates; removal/relaxation follows the controlling authority/role model and cannot bypass higher-level restrictions.

## Cost/model policy

Cost and model-selection policy may:

- warn;
- require a separate decision;
- narrow to cheaper qualified routes;
- block routes exceeding budget;
- record scoped budget state.

It MUST NOT silently substitute a model/provider/worker. Any alternative route still passes normal routing/qualification and Nawat requirements.

## Required negative oracles

```text
POLICY_NO_OBJECTION_CANNOT_EXECUTE_WITHOUT_NAWAT_GRANT
AGENT_CANNOT_SELF_INSTALL_AUTHORITY_WIDENING_POLICY
LOWER_TRUST_SESSION_POLICY_CANNOT_DISABLE_SERVER_RESTRICTION
UNTRUSTED_REPO_POLICY_MODULE_CANNOT_AUTO_LOAD
MANDATORY_POLICY_ENGINE_FAILURE_BLOCKS_PRE_EFFECT_ACTION
POLICY_STATE_LABEL_CANNOT_BECOME_AUTHORITY
POLICY_TRANSFORM_CANNOT_EXPAND_EFFECT_SCOPE
COST_POLICY_CANNOT_SILENTLY_SWITCH_PROVIDER
STALE_POLICY_VERSION_CANNOT_GOVERN_NEW_EFFECT_WITHOUT_ALLOWED_COMPATIBILITY
```

## Source-acquisition note

Omnigent's policy engine and types are useful behavior quarries, particularly explicit evaluation contexts, composed decisions, fail-closed pre-effect phases, state/labels, and scoped cost policy. Direct source reuse or Python policy-module loading is not admitted by this contract.