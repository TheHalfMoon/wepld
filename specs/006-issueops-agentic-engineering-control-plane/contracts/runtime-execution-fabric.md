# Contract — Runtime Execution Fabric

```text
STATUS = FUTURE_PLANNING_CONTRACT
PRIMARY_OWNERS = S3_PROCESS_FOUNDATION + S6_MISSION_RUNTIME_UWC
EFFECT_AUTHORITY = NAWAT_ONLY
QUALIFICATION_OWNER = MIrefa
TOPOLOGY_OWNER = EDARA
SECURITY_EVIDENCE_OWNER = AMAN
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

## Purpose

Define the WePLD-owned boundary among control-plane server state, execution hosts, runners, worker/harness adapters, containment, environment exposure, credential capabilities, runtime ceilings, and effect execution.

This contract is the canonical owner of the following future planning types:

```text
ServerDescriptor
HostDescriptor
RunnerDescriptor
HarnessProtocolAdapter
HarnessDialectExtension
ContainmentPosture
RuntimeCeiling
EnvironmentExposurePolicy
CredentialCapability
ExecutionEnvelope
```

`WorkerDescriptor`, `WorkerRequirement`, `Assignment`, `Attempt`, route qualification, and Nawat/effect records remain owned by `../data-model.md` and `worker-delegation.md`.

## Core identity separation

```text
ServerIdentity != HostIdentity
HostIdentity != RunnerIdentity
RunnerIdentity != WorkerIdentity
WorkerIdentity != AttemptIdentity
HarnessIdentity != ModelIdentity
ProviderSessionIdentity != RunnerIdentity
```

A single process may implement more than one logical boundary in an early tracer bullet, but the durable identities/evidence MUST remain distinct wherever the trust question differs.

## `ServerDescriptor`

```text
ServerDescriptor {
  server_id
  deployment_identity
  software_identity
  policy_snapshot_ref
  execution_host_registration_mode
  native_bridge_policy_ref?
  observed_at
}
```

Connecting a client or host to a server creates no execution authority.

## `HostDescriptor`

A host is a machine/runtime capable of owning one or more runners.

```text
HostDescriptor {
  host_id
  server_binding_ref?
  machine_identity
  os_platform_identity
  runtime_identity
  host_registration_evidence_refs[]
  host_execution_opt_in_state
  available_containment_backends[]
  available_network_containment_backends[]
  process_tree_containment_capability
  filesystem_containment_capability
  credential_broker_capability?
  native_bridge_capabilities[]
  last_liveness_observation
  qualification_state
  qualification_evidence_refs[]
  qualification_expiry?
}
```

```text
HOST_REGISTERED != HOST_QUALIFIED
HOST_QUALIFIED != EFFECT_AUTHORITY
HOST_ONLINE != RUNNER_READY
```

Host execution must be explicit/opt-in. Merely loading WePLD Desktop or connecting to a server MUST NOT silently register the machine as an execution host.

## `RunnerDescriptor`

A runner is one execution runtime instance or durable runtime identity owned by a host.

```text
RunnerDescriptor {
  runner_id
  host_id
  runner_runtime_identity
  runner_software_identity
  process_or_service_identity?
  supported_protocol_adapters[]
  supported_worker_families[]
  containment_posture_ref
  runtime_ceiling_ref
  environment_exposure_policy_ref
  credential_broker_identity?
  current_liveness_state
  current_capacity
  current_resource_usage?
  current_network_state
  qualification_state
  qualification_evidence_refs[]
  qualification_expiry?
}
```

A stable `runner_id` is routing provenance, not proof that the same process/runtime still owns the session. Resume/recovery must bind current runtime identity and effect state.

## Runtime routing invariants

```text
REQUESTED_RUNNER != QUALIFIED_RUNNER
QUALIFIED_RUNNER != NAWAT_GRANT
RUNNER_OFFLINE != SAFE_FALLBACK_TO_ANOTHER_RUNNER
RUNNER_REPLACED -> ROUTE_REQUALIFICATION_WHEN_MATERIAL
NO_SILENT_RUNNER_FALLBACK
```

A change of host, runner, containment backend, credential broker, network route, or worker implementation that is material to qualification creates a new route qualification before effectful work continues.

## `HarnessProtocolAdapter`

```text
HarnessProtocolAdapter {
  adapter_id
  protocol_family
  protocol_version_or_identity
  adapter_software_identity
  capability_vocabulary_version
  normalized_event_contract_version
  supported_operation_classes[]
  supported_session_semantics[]
  supported_permission_surfaces[]
  supported_subagent_semantics[]
  supported_resume_semantics[]
  known_opaque_fields[]
  extension_ids[]
  qualification_evidence_refs[]
}
```

Examples of protocol families may include ACP, provider-native SDK, provider-native CLI/stdio, MCP-mediated tool worker, or a WePLD-native worker protocol.

The protocol adapter normalizes transport/protocol behavior. It does not decide authority.

## `HarnessDialectExtension`

Vendor- or implementation-specific behavior is composed through an explicit extension rather than scattered harness-name branches in the generic core.

```text
HarnessDialectExtension {
  extension_id
  adapter_id
  vendor_or_dialect_identity
  extension_software_identity
  additional_handshake_claims[]
  subagent_mapping_rules[]
  permission_option_mapping_rules[]
  event_metadata_mapping_rules[]
  known_unsupported_or_ambiguous_semantics[]
  qualification_evidence_refs[]
}
```

Rules:

```text
DIALECT_EXTENSION != AUTHORITY
DIALECT_PERMISSION_OPTION != NAWAT_DECISION
DIALECT_CAPABILITY_CLAIM != QUALIFIED_CAPABILITY
UNRECOGNIZED_EXTENSION_DATA -> OPAQUE_OR_UNSUPPORTED
EXTENSION_SELECTION = TRUSTED_CONFIGURATION_OR_QUALIFIED_ADAPTER_DECISION
```

Untrusted repository/page/provider content cannot dynamically select an extension with greater capability or permission semantics.

## `ContainmentPosture`

A boolean `sandboxed` field is prohibited for acceptance/security decisions.

```text
ContainmentPosture {
  containment_posture_id
  backend_identity
  platform_runtime_identity
  process_tree_strength
  filesystem_strength
  network_strength
  namespace_or_container_strength?
  seccomp_or_syscall_policy_identity?
  read_mount_policy_identity?
  write_mount_policy_identity?
  home_visibility_state
  temporary_storage_policy
  escape_or_downgrade_limitations[]
  evidence_refs[]
  observed_at
  expires_at?
}
```

Normalized strength candidates:

```text
HARD_ISOLATION
HARD_WITH_EXPLICIT_LIMITATION
PROCESS_TREE_ONLY
ADVISORY
NONE
UNKNOWN
```

Every dimension is independent. For example a Windows Job Object-like backend may qualify as process-tree containment while filesystem and network isolation remain `NONE`.

```text
PROCESS_TREE_ONLY != HARD_FILESYSTEM_ISOLATION
PROCESS_TREE_ONLY != NETWORK_ISOLATION
PROVIDER_SANDBOX_LABEL != CONTAINMENT_POSTURE
SANDBOX_REQUIRED + QUALIFIED_BACKEND_UNAVAILABLE -> EXECUTION_REFUSED
CONTAINMENT_DOWNGRADE -> EXPLICIT_REQUALIFICATION
NO_SILENT_UNSANDBOXED_FALLBACK
```

## `RuntimeCeiling`

Deployment/operator limits are a hard upper bound which lower-trust configuration cannot widen.

```text
RuntimeCeiling {
  runtime_ceiling_id
  max_effect_classes[]
  max_network_class
  max_credential_class
  max_write_scope
  max_process_scope
  max_parallel_attempts
  max_wall_clock
  max_cpu?
  max_memory?
  max_disk?
  max_output?
  max_cost?
  allowed_containment_postures[]
  policy_snapshot_ref
}
```

The effective execution envelope is an intersection, never a union:

```text
EffectiveExecutionEnvelope =
  DeploymentRuntimeCeiling
  INTERSECT WorkspaceOrProjectCeiling
  INTERSECT AssignmentConstraints
  INTERSECT WorkerRequirement
  INTERSECT RouteQualification
  INTERSECT NawatGrant
```

If the intersection is empty, the attempt is blocked.

## `EnvironmentExposurePolicy`

The worker process receives a deny-by-default environment.

```text
EnvironmentExposurePolicy {
  environment_policy_id
  baseline_allowlist[]
  adapter_family_allowlist[]
  explicit_assignment_passthrough[]
  forced_values[]
  scrub_patterns[]
  prohibited_secret_classes[]
  home_config_visibility_policy
  inherited_path_policy
  policy_snapshot_ref
}
```

Rules:

```text
AMBIENT_HOST_ENV != WORKER_ENV
AMBIENT_SECRET != WORKER_VISIBLE_SECRET
GENERIC_PROTOCOL_ADAPTER_GETS_NO_VENDOR_SECRET_FAMILY_BY_DEFAULT
WORKER_REQUEST_FOR_ENV != ENV_AUTHORITY
```

Environment evidence should record names/classes and policy identities, not raw secret values.

## `CredentialCapability`

The preferred credential model is capability/broker based: when technically feasible, a worker never receives the reusable underlying credential.

```text
CredentialCapability {
  credential_capability_id
  secret_owner_ref
  credential_class
  broker_identity
  target_host_set[]
  target_resource_or_path_scope[]
  method_or_protocol_scope[]
  assignment_ref
  attempt_ref?
  route_qualification_ref
  egress_grant_ref
  nawat_grant_ref
  placeholder_identity?
  credential_refresh_policy_ref?
  usage_receipt_policy
  created_at
  expires_at
}
```

Possible delivery modes:

```text
BROKER_INJECT_ON_AUTHORIZED_EGRESS
BOUND_NON_SECRET_PLACEHOLDER
SCOPED_EPHEMERAL_CREDENTIAL
DIRECT_SECRET_EXPOSURE_LAST_RESORT
NONE
```

Direct secret exposure is a materially weaker route and requires separate qualification/authority evidence when a stronger broker route was required.

Rules:

```text
CREDENTIAL_CAPABILITY != SECRET_VALUE
CREDENTIAL_CAPABILITY != GENERAL_NETWORK_AUTHORITY
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
PLACEHOLDER != SECRET
PLACEHOLDER_BOUND_TO_TARGET != VALID_FOR_OTHER_TARGET
EGRESS_ALLOWED != AUTHENTICATED_REQUEST_AUTHORIZED
```

The broker must bind credential use to current target/route/attempt authority. Credential injection after Nawat grant expiry or route staleness is prohibited.

## Credential broker security requirements

Any implementation must qualify:

- canonical target-host parsing;
- redirects and cross-host redirects;
- DNS rebinding/private-address changes;
- raw-socket/proxy bypass;
- TLS trust and MITM CA handling if applicable;
- path/resource scope versus host-only scope;
- multiple credentials for one host;
- placeholder replay and guessing;
- header/query/body credential placement;
- logging/tracing/redaction;
- refresh races and stale credentials;
- broker crash/restart;
- credential use after attempt cancellation;
- unknown remote effect outcome;
- separation between secret storage, network transport, and effect authority.

## `ExecutionEnvelope`

Mission Runtime receives a frozen per-attempt envelope rather than re-reading mutable ambient configuration at each effect.

```text
ExecutionEnvelope {
  execution_envelope_id
  assignment_ref
  attempt_id
  host_ref
  runner_ref
  worker_ref
  protocol_adapter_ref
  dialect_extension_ref?
  containment_posture_ref
  runtime_ceiling_ref
  environment_exposure_policy_ref
  credential_capability_refs[]
  route_qualification_ref
  nawat_grant_refs[]
  context_package_ref
  policy_snapshot_refs[]
  created_at
  revalidation_triggers[]
}
```

The envelope is evidence of the current allowed execution intersection. It cannot widen any constituent authority.

## Revalidation triggers

Material changes include:

```text
HOST_CHANGE
RUNNER_CHANGE
RUNNER_RUNTIME_RESTART
WORKER_CHANGE
MODEL_CHANGE_WHEN_QUALIFICATION_BOUND
ADAPTER_OR_EXTENSION_CHANGE
CONTAINMENT_CHANGE
NETWORK_ROUTE_CHANGE
ENV_POLICY_CHANGE
CREDENTIAL_BROKER_CHANGE
CREDENTIAL_CAPABILITY_CHANGE
CONTEXT_ACCESS_REVOCATION
NAWAT_GRANT_EXPIRY
TARGET_IDENTITY_CHANGE
```

A trigger does not always require total workflow restart, but the owning contract must state which qualification/authority evidence becomes stale.

## Effect ordering and irreversible dependencies

Composite operations declare an effect dependency graph.

```text
EffectDependency {
  prerequisite_effect_ref
  dependent_effect_ref
  required_prerequisite_postcondition
  failure_policy
  compensation_or_reconciliation_policy?
  irreversible_boundary?
}
```

Rules:

```text
PREREQUISITE_UNAVAILABLE -> DEPENDENT_EFFECT_NOT_STARTED
PREREQUISITE_EFFECT_OUTCOME_UNKNOWN -> IRREVERSIBLE_DEPENDENT_EFFECT_NOT_STARTED
ROLLBACK_REQUESTED != ROLLBACK_SUCCEEDED
COMPENSATION_AVAILABLE != ORIGINAL_EFFECT_NOT_APPLIED
```

This is required for session/worktree/provider closeout, multi-step Git/provider actions, browser submissions followed by cleanup, and any workflow where a later destructive effect assumes an earlier external effect succeeded.

## Native desktop bridge boundary

A desktop shell may consume a local or remote WePLD SPA, but privileged native capabilities require a narrow typed bridge.

```text
NativeBridgeCapability {
  native_bridge_capability_id
  capability_kind
  pinned_application_origin
  allowed_sender_context
  exact_argument_schema
  result_schema
  effect_class
  qualification_ref
}
```

Rules:

```text
REMOTE_PAGE != NATIVE_PROCESS_AUTHORITY
RAW_IPC_EXPOSURE = PROHIBITED
RAW_NODE_OR_SHELL_EXPOSURE = PROHIBITED
PINNED_ORIGIN != EFFECT_AUTHORITY
FOREIGN_ORIGIN -> PRIVILEGED_BRIDGE_INERT
NATIVE_PERMISSION_PROMPT != WEPLD_USER_APPROVAL
```

Navigation may be needed for authentication, but privileged bridge eligibility must be tied to the pinned/trusted application context and revalidated after origin transitions.

## Adapter conformance additions

Every S6 worker/harness adapter conformance suite should include:

```text
IDENTITY_SEPARATION
NO_SILENT_RUNNER_FALLBACK
CAPABILITY_NEGOTIATION
UNKNOWN_DIALECT_FAIL_CLOSED_OR_OPAQUE
ENVIRONMENT_DENY_BY_DEFAULT
CONTAINMENT_STRENGTH_REPORTING
REQUIRED_SANDBOX_UNAVAILABLE_REFUSAL
CREDENTIAL_ROUTE_SEPARATION
NO_RAW_SECRET_UNLESS_EXPLICITLY_QUALIFIED
CANCELLATION_AND_ORPHAN_SEMANTICS
RESTART_AND_RESUME_SEMANTICS
UNKNOWN_EFFECT_RECONCILIATION
```

## Required negative oracles

```text
SERVER_CONNECTED_CANNOT_AUTO_REGISTER_EXECUTION_HOST
HOST_REGISTERED_CANNOT_EXECUTE_WITHOUT_ROUTE_AND_AUTHORITY
RUNNER_ID_CANNOT_CREATE_WORKER_TRUST
RUNNER_OFFLINE_CANNOT_SILENTLY_SELECT_ANOTHER_RUNNER
DIALECT_EXTENSION_CANNOT_GRANT_EFFECT
VENDOR_PERMISSION_CANNOT_BECOME_NAWAT_GRANT
RUNTIME_CEILING_CANNOT_BE_WIDENED_BY_AGENT_CONFIG
PROCESS_TREE_ONLY_CANNOT_BE_LABELED_HARD_SANDBOX
REQUIRED_SANDBOX_MISSING_BLOCKS_EXECUTION
AMBIENT_SECRET_CANNOT_LEAK_BY_DEFAULT_ENV_INHERITANCE
CREDENTIAL_PLACEHOLDER_CANNOT_AUTHENTICATE_WRONG_TARGET
CREDENTIAL_BROKER_CANNOT_INJECT_AFTER_GRANT_EXPIRY
EGRESS_ALLOWLIST_CANNOT_AUTHORIZE_CREDENTIAL_USE
PREREQUISITE_UNKNOWN_BLOCKS_IRREVERSIBLE_DEPENDENT_EFFECT
REMOTE_SPA_CANNOT_CALL_RAW_NATIVE_IPC
FOREIGN_ORIGIN_CANNOT_USE_PRIVILEGED_NATIVE_BRIDGE
```

## Source-acquisition note

Omnigent is a high-value behavior/source quarry for this boundary, especially its server/host/runner distinction, ACP extension seam, policy choke point, Bubblewrap/security posture, credential proxy, environment allowlisting, browser snapshot model, and desktop bridge. No source is admitted by this contract. Later source acquisition must pin exact owning paths, licenses/notices, tests, and security evidence before reuse.