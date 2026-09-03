# Contract Addendum — Distributed Runtime Safety

```text
STATUS = FUTURE_PLANNING_CONTRACT_ADDENDUM
PARENT_CONTRACT = contracts/runtime-execution-fabric.md
PRIMARY_OWNERS = S3_PROCESS_FOUNDATION + S6_MISSION_RUNTIME
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
```

## Purpose

Close the distributed-systems safety gaps created once Server, Host, and Runner are distinct: authenticated host binding, split-brain prevention, lease/fencing semantics, exact harness execution identity, event deduplication/causality, capacity admission, and version compatibility.

## Host trust / enrollment

A host connection is not trusted because it knows a server URL or presents a self-asserted `host_id`.

Future host enrollment must bind:

```text
HostTrustObservation {
  host_trust_observation_id
  server_id
  host_id
  authenticated_principal_identity
  machine_or_installation_identity
  transport_security_identity
  enrollment_or_registration_decision_ref
  key_or_credential_binding_identity?
  attestation_or_platform_evidence_refs[]
  observed_at
  expires_at_or_revalidate_at?
}
```

The exact authentication technology is deferred to the owning slice, but the semantics are not:

```text
HOST_ID_CLAIM != AUTHENTICATED_HOST
TLS_CONNECTION != HOST_EXECUTION_AUTHORITY
AUTHENTICATED_HOST != QUALIFIED_RUNNER
```

Host credential rotation/revocation must invalidate future eligibility without erasing historical evidence.

## Runner ownership lease and fencing

A runner which restarts or reconnects can create split-brain risk if an old process/session still acts on stale grants.

Use a lease/fencing model:

```text
RunnerOwnershipLease {
  lease_id
  host_id
  runner_id
  runner_runtime_identity
  owner_epoch
  fencing_token
  issued_at
  expires_at
  renewal_policy_ref
  revocation_state
  evidence_refs[]
}
```

Rules:

```text
NEW_OWNER_EPOCH > OLD_OWNER_EPOCH
STALE_FENCING_TOKEN -> EFFECT_REFUSED
LEASE_EXPIRED -> EFFECT_REFUSED_OR_REQUALIFICATION_REQUIRED
RUNNER_RECONNECT_WITH_NEW_RUNTIME -> NEW_OWNERSHIP_EPOCH
```

Acceptance-critical external/process effects must carry the current runner ownership/fencing identity when the execution topology uses distributed runners.

A stale runner must not be able to continue simply because it still possesses a historical Assignment, ContextPackage, or Nawat decision reference.

## Exact harness execution identity

`WorkerDescriptor.version_identity` is not sufficient evidence that the executable/runtime actually launched for one Attempt matched the qualified artifact.

Record:

```text
HarnessExecutionIdentity {
  harness_execution_identity_id
  adapter_id
  dialect_extension_id?
  resolved_executable_or_runtime_identity
  executable_or_artifact_digest?
  package_or_distribution_identity?
  protocol_identity
  configuration_identity
  observed_capability_handshake_identity
  launch_environment_policy_ref
  containment_posture_ref
  evidence_refs[]
}
```

```text
WORKER_DESCRIPTOR_VERSION != EXECUTED_HARNESS_IDENTITY
PATH_RESOLUTION != QUALIFIED_BINARY_IDENTITY
AUTO_UPDATED_HARNESS -> PRIOR_QUALIFICATION_STALE_WHEN_MATERIAL
```

Silent self-update or vendor CLI replacement cannot remain invisible to route/acceptance evidence.

## Runtime event envelope

Server/runner transports may duplicate, reorder, reconnect, or replay messages. Runtime facts therefore require stable event identity rather than arrival-order interpretation.

```text
RuntimeEventEnvelope {
  runtime_event_id
  producer_kind
  producer_identity
  producer_runtime_identity
  host_id?
  runner_id?
  attempt_id?
  event_kind
  producer_sequence?
  causal_parent_event_refs[]
  idempotency_or_dedupe_key?
  payload_identity
  policy_schema_version
  observed_at_source?
  received_at
  authenticity_evidence_ref?
}
```

Rules:

```text
MESSAGE_ARRIVAL_ORDER != CAUSAL_ORDER
DUPLICATE_DELIVERY != SECOND_EFFECT
REPLAYED_EVENT != NEW_AUTHORITY
MISSING_SEQUENCE != PERMISSION_TO_INFER_ORDER
```

Derived state must be deterministic under duplicate delivery and must detect impossible/conflicting event histories rather than silently choose one.

## Capacity admission and reservation

A route qualification that was true before execution can become invalid under host resource exhaustion.

Future resource admission should support a bounded reservation/slot identity when resource guarantees are required:

```text
RuntimeReservation {
  reservation_id
  host_id
  runner_id
  attempt_id
  resource_envelope
  admitted_at
  expires_at?
  release_state
}
```

No overcommit algorithm is selected here. The invariant is:

```text
RESOURCE_REQUIREMENT_NOT_ADMITTED -> ATTEMPT_NOT_STARTED
```

and resource exhaustion must be surfaced distinctly from provider/model failure.

## Version compatibility / handshake

Server, host, runner, protocol adapter, dialect extension, and native desktop bridge may evolve independently.

A connection must negotiate/observe compatible contract versions before using privileged capabilities.

```text
SOFTWARE_CONNECTED != CONTRACT_COMPATIBLE
UNKNOWN_REQUIRED_PROTOCOL_VERSION -> CAPABILITY_UNAVAILABLE
SILENT_SCHEMA_DOWNGRADE = PROHIBITED
```

Backward-compatible observation-only behavior may be permitted by the owning contract; effectful behavior requires exact semantics sufficient for qualification.

## Split-brain / recovery sequence

After reconnect/restart:

1. authenticate current host/runner identity;
2. establish a fresh ownership lease/epoch when runtime ownership changed;
3. reject stale fencing tokens;
4. reconstruct/dedupe runtime events;
5. reconcile any material `EFFECT_OUTCOME_UNKNOWN`;
6. re-observe containment/environment/credential state;
7. requalify stale route evidence;
8. revalidate Nawat grants;
9. only then resume or create a new Attempt according to policy.

## Required negative oracles

```text
SELF_ASSERTED_HOST_ID_CANNOT_AUTHENTICATE_HOST
REVOKED_HOST_CREDENTIAL_CANNOT_RECONNECT_AS_TRUSTED
OLD_RUNNER_EPOCH_CANNOT_EFFECT_AFTER_NEW_OWNER_ACTIVATES
EXPIRED_LEASE_CANNOT_EFFECT
DUPLICATE_RUNTIME_EVENT_CANNOT_DUPLICATE_DERIVED_EFFECT
OUT_OF_ORDER_EVENTS_CANNOT_SILENTLY_REWRITE_CAUSAL_HISTORY
AUTO_UPDATED_HARNESS_CANNOT_REUSE_STALE_QUALIFICATION
RESOURCE_EXHAUSTION_CANNOT_MASQUERADE_AS_PROVIDER_FAILURE
INCOMPATIBLE_PROTOCOL_VERSION_CANNOT_SILENTLY_DOWNGRADE_EFFECTFUL_CAPABILITY
RECONNECTED_TRANSPORT_CANNOT_SKIP_EFFECT_RECONCILIATION
```

## Omnigent relationship

Omnigent's explicit host/runner routing and recovery behavior motivated this deeper review, but the lease/fencing/event envelope above is a WePLD hardening requirement rather than a claim that Omnigent implements the exact same model.