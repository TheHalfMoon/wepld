# Spec Addendum — Runtime Execution Fabric

```text
STATUS = FUTURE_PLANNING_SPEC_ADDENDUM
PARENT_SPEC = spec.md
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

This addendum extends Spec 006 with execution-fabric requirements derived from the whole-plan review and Omnigent mechanism study. It does not change roadmap ordering.

## FR-045 — Server / Host / Runner / Worker / Attempt identity separation

WePLD MUST model control-plane server identity, execution host identity, runner runtime identity, worker identity, and Attempt identity as distinct typed identities whenever they are material to qualification, authority, recovery, or evidence.

```text
SERVER_ID != HOST_ID != RUNNER_ID != WORKER_ID != ATTEMPT_ID
```

Connecting a client/desktop to a server MUST NOT implicitly opt the machine into executing agent work.

## FR-046 — Runtime ceiling and execution envelope

Effectful execution MUST derive a frozen `ExecutionEnvelope` from the intersection of deployment/project ceilings, Assignment/WorkerRequirement constraints, route qualification, containment/environment/credential state, and current Nawat grants.

Lower-trust agent/provider/repository configuration MUST NOT widen a stronger controlling ceiling.

## FR-047 — Multidimensional containment and fail-loud sandboxing

Containment MUST be represented by evidence across relevant dimensions such as process-tree, filesystem, network, namespace/container, syscall, mount/write, home/config visibility, and platform limitations.

A boolean provider/runtime `sandboxed` claim MUST NOT satisfy security/acceptance decisions by itself.

When a route requires containment that is unavailable:

```text
REQUIRED_CONTAINMENT_UNAVAILABLE -> EXECUTION_REFUSED_OR_EXPLICITLY_REQUALIFIED_ALTERNATIVE
```

Silent unsandboxed downgrade is prohibited.

## FR-048 — Deny-by-default worker environment

Worker processes MUST use an explicit `EnvironmentExposurePolicy`. Ambient host variables/credentials MUST NOT be inherited wholesale.

The policy MUST distinguish baseline runtime variables, adapter-family variables, Assignment-specific passthrough, forced safety values, scrubbed variables, and prohibited secret classes.

## FR-049 — Credential capability / secretless broker preference

When technically feasible, WePLD SHOULD keep reusable credentials outside the worker and expose only a narrowly scoped credential capability bound to exact target, route, Attempt, egress, expiry, and Nawat authority.

A target-bound non-secret placeholder or scoped ephemeral credential MAY be used for clients that require local credential material.

```text
CREDENTIAL_CAPABILITY != SECRET
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
EGRESS_ALLOWLIST != CREDENTIAL_AUTHORITY
```

Direct reusable-secret exposure MUST be explicit, separately qualified, and visible as a weaker security route.

## FR-050 — Generic harness protocol + explicit dialect extension

UWC SHOULD prefer a protocol-pure generic adapter plus explicit additive dialect extensions over scattered provider-name branching.

Vendor-specific permission/sub-agent/metadata semantics MUST remain extension claims until qualified and MUST NOT mint Nawat authority.

Unknown dialect data MUST remain opaque/unsupported rather than silently interpreted.

## FR-051 — Browser snapshot-bound action freshness

Ref-based browser actions MUST bind the exact browser document/snapshot identity and element reference that produced the target.

Navigation, reload, context/frame/origin change, document replacement, or snapshot supersession MUST stale the action proposal when material.

```text
STALE_BROWSER_SNAPSHOT != VALID_ACTION_TARGET
```

## FR-052 — Typed review independence

When an assurance policy requires independent review, acceptance MUST include a current `ReviewIndependenceReceipt` proving the required separation dimensions for the exact target.

Different-vendor identity MAY be evidence but MUST NOT alone prove independence.

A policy may require separation of worker/Attempt, provider/model/harness, mutable workspace/process state, context, and effect/write authority.

## FR-053 — Effect prerequisite ordering

Composite effect workflows MUST represent prerequisite/dependent effect relationships where order is material to safety or recoverability.

An irreversible dependent effect MUST NOT start while a required prerequisite is unavailable or remains `EFFECT_OUTCOME_UNKNOWN`.

Compensation/rollback MUST be represented as a separate effect with its own authority/evidence rather than rewriting historical outcome.

## FR-054 — Native desktop bridge least authority

A native desktop shell MUST expose remote/server-served UI only to a narrow typed native bridge with context isolation, sender/application-origin validation, serialization-safe arguments/results, and per-capability effect classification.

Raw Node/process/shell/filesystem/IPC capability MUST NOT be exposed to remote page content.

Navigation to a foreign origin MUST make privileged bridge access inert until the trusted application context is re-established/revalidated.

## FR-055 — Runtime recovery is not transport recovery

Runner/session reconnection MUST NOT automatically mark an interrupted Attempt safe to resume.

Before effectful resume, WePLD MUST re-establish runtime identity and revalidate any containment, route, context, credential, authority, or external-effect state declared stale by the owning contract.

```text
TRANSPORT_RECOVERED != ATTEMPT_SAFE_TO_RESUME
RUNNER_RECONNECTED != EFFECT_RECONCILED
```

## FR-056 — Credential and runtime evidence privacy

Durable evidence SHOULD record credential-capability identities, policy/target scope, broker/use receipts, environment policy identity, containment posture, and runtime lineage without persisting reusable secret values or raw ambient environment content.

Security investigations requiring protected secret-derived identity evidence must use a separately qualified handling policy.