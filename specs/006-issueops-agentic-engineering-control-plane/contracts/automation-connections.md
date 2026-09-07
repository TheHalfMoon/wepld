# Contract — Automations and Connections

```text
STATUS = FUTURE_PLANNING_CONTRACT
CANONICAL_OWNER_WITHIN_SPEC_006 = AUTOMATION_CONNECTION_TYPES_DEFINED_HERE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

This contract defines future semantics for event/schedule-triggered work and integration connections. It does not authorize triggers, network access, secrets, provider calls, or effects.

## 1. Core separation

```text
AUTOMATION != ORCHESTRATOR
AUTOMATION_DEFINITION != EXECUTION_AUTHORITY
TRIGGER_RECEIVED != WORKFLOW_INTENT
SCHEDULE_FIRED != EFFECT_AUTHORITY
INTEGRATION != CONNECTION
CONNECTION != CREDENTIAL
CREDENTIAL != SECRET
CREDENTIAL_CAPABILITY != NETWORK_AUTHORITY
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
```

An Automation may create a Mission through qualified intent compilation. Mission Runtime remains the execution host; Edara owns topology; Mirefa qualifies routes; Nawat owns effect-time authority.

## 2. AutomationDefinition

```text
AutomationDefinition {
  automation_id
  project_ref?
  revision
  trigger_definition_ref
  intent_template
  input_mapping
  required_capabilities[]
  preferred_routes[]
  required_routes[]
  forbidden_routes[]
  approval_profile_ref?
  completion_expectation
  created_at
}
```

Properties:

- declarative rather than executable code;
- contains no raw secret;
- contains no worker identity requirement unless expressed through ordinary capability/topology constraints;
- contains no implicit Nawat grant;
- enable/pause state is a separate revision-checked activation projection over runtime events; it never mutates the immutable definition revision or pre-authorizes downstream effects;
- revisions are durable so a run can identify the exact definition that produced its intent.

## 3. TriggerDefinition / TriggerEnvelope

```text
TriggerDefinition {
  trigger_definition_id
  trigger_kind
  source_or_schedule_identity
  schedule_timezone_and_rule_version?
  misfire_catchup_and_coalescing_policy
  backlog_and_concurrency_limits
  schema_version
  matching_constraints[]
  authenticity_requirements[]
  deduplication_contract
  freshness_or_replay_window?
}

TriggerEnvelope {
  runtime_event_ref
  trigger_definition_ref
  automation_definition_revision_ref
  tenant_and_project_scope
  source_identity
  subscription_identity
  logical_occurrence_identity
  source_event_identity?
  observed_at
  payload_identity
  schema_version
  authenticity_evidence_refs[]
  replay_or_dedup_evidence_refs[]
  raw_payload_evidence_ref?
}
```

Candidate trigger kinds:

```text
SCHEDULE
WEBHOOK
POLL_OBSERVATION
PROVIDER_EVENT
STREAM_EVENT
INTERNAL_CASE_EVENT
MANUAL
```

Receiving a valid trigger means only that a qualifying event was observed. It does not prove user/workflow intent or effect authority.

`TriggerEnvelope` is a typed payload of `RuntimeEventEnvelope` from the distributed runtime contract, carried by Case Bus. Its stable identity is the containing event identity; it does not create another ingress transport, event store or execution owner. Provider delivery identity and logical occurrence identity remain separate. CapabilityPresence likewise uses an ordinary typed Observation with host/runtime identity, observed/expiry times and evidence; it is not qualification or authority.

`subscription_identity` is a stable WePLD-owned value in the existing versioned trigger configuration, scoped to the verified source account/tenant and tenant/project/automation. Ingress resolves it from trusted configuration and verifies `source_identity` and any provider subscription identifier against that binding; producer-supplied identifiers cannot choose another subscription. Renewal or configuration revision retains the value. Replacement may retain it only with an explicit verified same-subscription mapping and retained dedupe history; otherwise a new identity is allocated and overlapping/ambiguous old occurrences are quarantined until reconciled. Separate subscriptions to the same provider never share this identity accidentally.

`logical_occurrence_identity` is the stable business occurrence within that subscription. For provider events it is the qualified provider event key; schedules use the declared timezone/tzdb/instant/fold occurrence rule; polling uses the qualified source item/version occurrence; a manual run receives a fresh accepted user-invocation identity. `source_event_identity` is optional upstream provenance, not an optional substitute for the mandatory occurrence identity. The containing `runtime_event_id` identifies the ingested delivery/event record and survives its own transport replay; separate duplicate deliveries may have different runtime event IDs but must resolve to the same durable logical occurrence key. No separate event store is added.

## 4. Trigger ingress rules

Effectful or remote triggers require, where applicable:

- source identity;
- signature/authentication evidence;
- timestamp/freshness validation;
- replay-window handling;
- deduplication identity;
- bounded payload size/schema validation;
- tenant/project binding;
- ambiguity/conflict handling;
- explicit failure when source authenticity cannot be established and the trigger contract requires it.

Duplicate trigger delivery must not silently create duplicate irreversible effects.

```text
DUPLICATE_EVENT != DUPLICATE_INTENT
DELIVERY_RETRY != EFFECT_RETRY
```

Ingress must durably capture the accepted event and its scoped dedupe identity before acknowledging durable acceptance to the source. The durable occurrence key comprises tenant/project scope, stable automation_id, `subscription_identity` and `logical_occurrence_identity`. It excludes mutable automation/trigger revisions: the first accepted occurrence atomically pins both revisions and its payload digest. A duplicate after an edit resolves that original record; it cannot select the new revision or create another intent. Subscription replacement must retain upstream occurrence identity or explicitly quarantine ambiguous cross-subscription replay. An identical key with a different payload digest is a conflict, not a duplicate success. A contract without a stable event/occurrence identity must explicitly qualify a bounded alternative or refuse consequential automatic compilation.

The transition from accepted trigger to qualified WorkflowIntent and Mission association must be atomic in the existing runtime persistence boundary, or use its durable transactional outbox and idempotent consumer. Crash/replay between those stages cannot create a second intent. Dedupe retention must cover the source replay window; after expiry, old deliveries are quarantined/reconciled rather than assumed new. An intentional manual rerun receives a new controlling intent and operation identity. These are minimum prerequisites before effectful automation, not deferred optional S9 work.

Schedule contracts record timezone, timezone-data/rule version, occurrence identity, DST skipped/repeated-time behavior, missed-run policy (`SKIP`, bounded `CATCH_UP`, or `COALESCE`), and backlog/concurrency limits. Disabled definitions stop new matching; already accepted occurrences retain their pinned revision and require explicit cancellation/requalification policy. Polling records cursor/checkpoint and source ordering assumptions. Stream/webhook acknowledgement and backpressure must never silently discard accepted work. Define overflow as visible refusal or a recorded policy-governed loss, never successful execution.

## 5. IntegrationDescriptor

```text
IntegrationDescriptor {
  integration_id
  integration_version
  source_identity
  authentication_modes[]
  capabilities[]
  trigger_types[]
  schemas
  risk_annotations[]
  network_requirements[]
  secret_requirements[]
  test_vectors[]
  examples[]
  anti_examples[]
}
```

Candidate semantic capability classes:

```text
READ
SEARCH
CREATE
UPDATE
DELETE
EXECUTE
UPLOAD
DOWNLOAD
SUBSCRIBE
POLL
WEBHOOK
STREAM
```

Capability class affects qualification/risk/effect semantics. A generic `action` label is not sufficient security classification.

## 6. IntegrationCapability

```text
IntegrationCapability {
  capability_id
  semantic_class
  input_schema
  output_schema
  effect_class
  idempotency_contract
  reconciliation_contract
  timeout_contract
  rate_limit_contract
  network_target_constraints[]
  required_credential_capabilities[]
}
```

Schema validation is necessary but not sufficient for safe execution. Functional constraints, security policy, runtime containment, and effect-time authority remain separate.

## 7. ConnectionBinding

```text
ConnectionBinding {
  connection_binding_id
  integration_id
  integration_version
  binding_revision
  binding_scope
  account_or_tenant_identity
  credential_broker_binding_ref
  credential_request_policy_ref
  revocation_generation
  allowed_capability_subset[]
  connection_state
  observed_at
  freshness_or_expiry?
}
```

Binding scopes may include Project, Automation, Work, or another qualified WePLD scope. Binding never copies a raw secret into the AutomationDefinition or Project context.

A ConnectionBinding is a durable account/broker association, not an expiring execution credential. At dispatch, the broker derives the per-attempt CredentialCapability defined in `runtime-execution-fabric.md` from the current binding revision, account/tenant, authorized operation, target and grants. Token refresh is serialized per credential binding to prevent refresh-token rotation races; failed refresh/revocation becomes a visible sign-in requirement. Rotation/revocation advances the binding generation and invalidates outstanding eligibility where required. Updating integration versions requires compatibility/schema qualification and cannot silently alter pending runs.

```text
PROJECT_CONNECTION_BINDING != PROJECT_AUTHORITY
CONNECTION_AVAILABLE != CONNECTION_QUALIFIED
```

## 8. Credential capability boundary

A future credential broker should prefer references/capabilities over exposing raw secrets to workers. A credential capability must state enough scope to prevent ambient credential reuse, such as service/account, operation class, target scope, validity/expiry, and broker/runtime identity where applicable.

Separate decisions remain required for:

```text
authentication capability
network destination authority
effect authority
```

OAuth success or an API token's provider scope never becomes a Nawat grant.

## 9. Route constraints

Automation/Work planning may express:

```text
preferred_routes[]
required_routes[]
forbidden_routes[]
```

Examples:

- API only; Browser prohibited;
- Browser required because user-visible rendering is part of the outcome;
- attached-user-browser prohibited; managed browser allowed;
- raw Computer Use prohibited.

Mirefa evaluates currently qualified routes against these constraints. No silent fallback is allowed when fallback changes semantics, trust, credentials, or evidence.

## 10. Run identity

The UI may present `AutomationRunId` as a view key if useful, but a new canonical execution primitive is not justified initially. The authoritative execution lineage remains:

```text
AutomationDefinition revision
-> TriggerEnvelope
-> WorkflowIntent / Mission
-> Assignment(s)
-> Attempt(s)
-> Effect/Observation/Evidence
```

If implementation later proves a durable automation-run entity is required for lifecycle or query performance, Ponytail must re-evaluate whether it is a true domain identity or only a projection.

## 11. Effect outcomes and retries

Integration actions reuse the existing Spec 006 effect model.

Important distinctions:

```text
REQUEST_SENT != EFFECT_APPLIED
LOCAL_TIMEOUT != REMOTE_EFFECT_NOT_APPLIED
TRANSPORT_RETRYABLE != EFFECT_RETRY_SAFE
EFFECT_OUTCOME_UNKNOWN != SAFE_TO_RETRY
RECONCILIATION != REEXECUTION
```

The capability contract should identify provider idempotency keys, read-after-write reconciliation, event lookup, or other mechanisms that can prove effect state. Missing reconciliation support is a qualification limitation, not permission to guess.

## 12. Long-lived waits

Scheduled, delayed, approval-gated, webhook-waiting, or provider-waiting Automations must use Mission Runtime persistence and recovery semantics before consequential execution. S9 extends continuation/audit capability; it cannot postpone the minimum safe dispatch and reconciliation required by S6/S8. An in-memory callback is never durable truth.

A resumed run must identify:

- original definition revision;
- trigger identity;
- mission/assignment identity;
- prior attempts/effects;
- current capability/connection state;
- stale authority/qualification requiring refresh.

## 13. Connector SDK design requirements

A future SDK should be schema-first enough to generate or validate:

```text
configuration UI
types
validation
documentation
test fixtures
examples
anti-examples
capability declaration
risk metadata
```

Code-first ergonomics are allowed behind these contracts. Community integration code remains an untrusted supply-chain boundary and must not gain filesystem/process/network/secret capabilities beyond the admitted runtime contract.

Conformance separates schema/sample simulation from live authentication and behavioral qualification. Fixtures cover pagination/cursor stability, duplicate delivery, rate-limit retry-after, refresh races, revoked accounts, incompatible schema upgrades and conflicting idempotency keys. Dry-run planning has no credential read, network or provider effects unless those effects are independently authorized and explicitly identified. Connector metadata never supplies its own authority policy.

## 14. Security/failure negative oracles

Minimum future negative tests:

```text
VALID_OAUTH_TOKEN_DOES_NOT_GRANT_DELETE
CONNECTION_BINDING_DOES_NOT_EXPOSE_RAW_SECRET
DUPLICATE_WEBHOOK_DOES_NOT_DUPLICATE_IRREVERSIBLE_EFFECT
STALE_WEBHOOK_IS_REJECTED_WHEN_FRESHNESS_REQUIRED
INVALID_SIGNATURE_DOES_NOT_CREATE_WORKFLOW_INTENT
RATE_LIMIT_DOES_NOT_BECOME_GENERIC_SUCCESS
TIMEOUT_AFTER_SEND_BECOMES_UNKNOWN_WHEN_EFFECT_CANNOT_BE_PROVEN
UNKNOWN_EFFECT_IS_RECONCILED_BEFORE_RETRY
REQUIRED_ROUTE_UNAVAILABLE_FAILS_VISIBLE
DISALLOWED_ROUTE_IS_NOT_SILENTLY_SUBSTITUTED
```

## 15. UX states

Connection/Automation UX should distinguish at least:

```text
Connected
Needs sign-in
Expired
Unsupported capability
Route unavailable
Needs permission
Waiting
Running
Outcome uncertain
Recovering
Blocked
Completed
```

Provider connectivity must not be presented as effect permission.

## 16. Definition revision, schedule and step semantics

Automation revisions are immutable and content addressed. Mutable enable/pause state uses a separate revision-checked activation projection on the stable automation identity, reconstructed from existing RuntimeEventEnvelope payloads containing `automation_id`, `activation_revision`, `selected_definition_revision_ref`, `enabled_state = ENABLED | PAUSED | DISABLED`, controlling principal and decision evidence. This is a view of existing runtime persistence, not an additional activation store. The ingress transaction compares the current activation revision before accepting a new occurrence; stale activation cannot admit new work. Accepted occurrences retain the exact definition, trigger, template, integration and input-schema revisions. An edit affects only new occurrences; explicit cancellation affects accepted runs through MissionRuntime. Changing or replacing a webhook subscription cannot silently replay past events as new work.

Schedule identity includes timezone name, tzdb version, local rule, resolved UTC instant and repeated-time fold. The default repeated-time policy is FIRST_ONLY; BOTH is explicit and produces two distinct fold identities. Skipped local times default to SKIP; SHIFT_FORWARD is explicit and records the resulting instant. Misfire policy defaults to SKIP; CATCH_UP requires finite lookback, count and backlog limits; COALESCE creates one intent with an explicit bounded missed-occurrence range. Updating timezone rules creates a new trigger revision; already accepted instants do not move. Runtime uses an authoritative persisted occurrence ledger and monotonic lease timing; wall-clock rollback cannot recreate an accepted occurrence. Cross-host clock skew outside the admitted bound blocks scheduling until reconciled.

Polling atomically persists the captured items and next cursor (or its existing runtime transactional outbox). Cursor advancement before durable capture is forbidden. Provider ordering, page consistency, replay and cursor expiry are declared; a rescan deduplicates stable source occurrences. Webhook/stream receipt first validates signature against exact bytes, timestamp/window, subscription and tenant binding, then performs bounded parsing and durable capture. Authentication failure, unsupported schema and overload are explicit non-acceptance responses. Sensitive raw payloads are excluded from ordinary logs. Acknowledged accepted work cannot be dropped on a full queue.

Reusable steps and templates are versioned declarative fragments compiled by Edara into existing Assignments, dependencies and DecisionBoundaries. The initial conditional language permits only typed field lookup, literal comparison, boolean composition and declared existence checks; no eval, script, recursion, dynamic import or unbounded loop. The compiler type-checks both branches, bounds expansion, detects dependency cycles and records branch selection with input identity. Only one selected branch dispatches. Human approval steps become durable waits with exact decision identity/expiry; timeout is an explicit blocked/cancel outcome, never approval. Compensation is a fresh proposal under current authority and may itself fail or become uncertain.

Templates contain capability requirements and connection-slot references, never embedded credentials or grants. A copied template creates a new definition identity and explicit bindings. Simulation is a non-effectful plan/fixture evaluation with a SIMULATED evidence label. Live connection testing declares each read/network/credential effect and obtains separate qualification/authority. A successful sample is never a live-qualified capability. Run history is the Mission/Attempt/effect timeline projected by automation_id and accepted revision.

## 17. Authentication and connection lifecycle

Connection states are DISCONNECTED, CONNECTING, CONNECTED, REFRESHING, EXPIRED, REVOKED, NEEDS_RECONNECT and UNSUPPORTED. OAuth qualification requires one-time state bound to the initiating principal/session/connection, exact registered redirect URI, PKCE for every public authorization-code client flow and bounded callback lifetime. Public clients require transaction-bound S256 PKCE and a provider that enforces the verifier; lack of that support is UNSUPPORTED, never a downgrade to plain/no PKCE. Confidential-client alternatives require explicit security qualification rather than inferring safety from provider support. The flow pins the authorization-server issuer and endpoint tuple and validates the response against it to prevent mix-up. Public-client refresh uses sender constraint or rotation with replay detection. These requirements follow [RFC 9700 §§2.1.1, 2.2.2 and 4.4](https://www.rfc-editor.org/rfc/rfc9700.html). A provider lacking required protections is UNSUPPORTED for that route; there is no silent downgrade. The broker verifies account/tenant identity from a qualified provider identity response before CONNECTED. UI displays that verified identity, granted scopes, project/workspace visibility and last verification.

Multiple accounts are separate ConnectionBindings with explicit selection. No first-account fallback is allowed. Refresh uses generation-checked single ownership per binding across processes/hosts, preserving account and scopes; rotation publishes a successor generation atomically, then invalidates superseded capabilities. Revocation/reconnect fences queued dispatch. Reconnecting the same verified account advances generation; a different account requires a new binding and explicit run requalification. A late refresh cannot revive a revoked generation. Provider tokens remain in the broker, outside context, prompts and ordinary evidence.

Every derived capability consumes the complete CredentialCapability contract in `runtime-execution-fabric.md`, including all resource/account/method/operation/Attempt/use/expiry/revocation and authenticated HTTPS redirect restrictions. Integration network requirements are untrusted declarations checked against canonical egress policy. A credential test is an effect; it cannot piggyback on schema validation.

## 18. Provider protocol and developer conformance

IntegrationDescriptor pins SDK/protocol/schema versions, package digest/provenance and admission evidence. Its capability declarations include operation-specific pagination/completeness, timeout/cancellation, idempotency retention, reconciliation visibility bounds, rate-limit scope, maximum input/output bytes and subscription lifecycle. A descriptor upgrade cannot mutate queued work; an explicit migration produces a successor definition and requalification, or rejects incompatibility. Webhook registration, renewal and deletion are separately authorized provider effects with stable logical operation identity and recovery receipts. Disabled ingress rejects new work while separately reconciling existing subscriptions/runs.

Normalized failures are AUTH_REQUIRED, SCOPE_DENIED, REVOKED, RATE_LIMITED, PROVIDER_UNAVAILABLE, SCHEMA_INCOMPATIBLE, PARTIAL_OBSERVATION, TARGET_CONFLICT, UNSUPPORTED and EFFECT_OUTCOME_UNKNOWN. Preserve bounded provider diagnostics and retry-after evidence. Backoff has finite attempt/time/cost limits and jitter; a retryable transport failure never proves effect retry safety. Pagination declares a stable snapshot/watermark or an explicit partial/mutable result. Repeated cursor, truncated page, missed event and expired cursor are visible; a partial list cannot prove absence for reconciliation.

The connector SDK supplies typed schema and capability validation, synthetic auth/refresh fixtures, deterministic event replay, action previews, redacted local diagnostics and operation-specific examples/anti-examples for READ, SEARCH, CREATE, UPDATE, DELETE, EXECUTE, UPLOAD, DOWNLOAD, SUBSCRIBE, POLL, WEBHOOK and STREAM. Code executes only inside the admitted adapter/runtime envelope: installing, importing or validating metadata must not run package hooks or acquire ambient process/network/filesystem access. Extension conformance includes account confusion, refresh races, key conflicts, schema changes, pagination gaps, rate limits, revoked credentials and unknown outcomes. Unsupported provider features are declared individually; a connected account is not a blanket qualification.
