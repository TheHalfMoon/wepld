# Distributed Runtime Safety Task Map

```text
STATUS = FUTURE_PLANNING_TASK_MAP
PARENT_CONTRACT = contracts/runtime-distributed-safety-addendum.md
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
```

## S3 — trust, identity, and transport foundation

- [ ] `006-RT-S3-001` Define authenticated Host enrollment semantics and revocation/rotation evidence.
- [ ] `006-RT-S3-002` Define Host/Runner transport-security identity and replay-resistant connection binding without assuming the transport itself grants execution authority.
- [ ] `006-RT-S3-003` Define `RuntimeEventEnvelope` identity, producer/runtime provenance, dedupe key, causal-parent semantics, and deterministic duplicate/out-of-order handling.
- [ ] `006-RT-S3-004` Add negative fixtures for replayed events, duplicate delivery, out-of-order terminal events, and conflicting runtime histories.
- [ ] `006-RT-S3-005` Define server/host/runner protocol-version compatibility negotiation and fail-closed behavior for unknown required effectful semantics.

## S6 — runner ownership and exact execution identity

- [ ] `006-RT-S6-001` Implement runner ownership epoch/lease/fencing semantics once distributed/restartable runners are authorized.
- [ ] `006-RT-S6-002` Prove stale runner epoch/fencing tokens cannot execute after a new owner becomes active.
- [ ] `006-RT-S6-003` Bind each acceptance-critical Attempt to exact `HarnessExecutionIdentity`, including resolved executable/runtime/artifact/config/protocol/capability-handshake identity where material.
- [ ] `006-RT-S6-004` Detect material harness auto-update/replacement and stale affected route qualification before further effectful execution.
- [ ] `006-RT-S6-005` Distinguish route qualification from resource admission/reservation; resource exhaustion produces a typed runtime frontier.
- [ ] `006-RT-S6-006` Ensure reconnect/restart establishes current authenticated Host/Runner runtime identity before any resume decision.

## S7/S9 — evidence integration

- [ ] `006-RT-S7-001` Allow Assurance policies to require exact Host/Runner/Harness execution identities and containment posture for acceptance-critical claims.
- [ ] `006-RT-S9-001` Preserve ownership epochs/fencing, runtime events, harness execution identity, and protocol compatibility evidence in the Quality Passport/timeline.
- [ ] `006-RT-S9-002` Replay duplicated/reordered transport histories deterministically and surface impossible histories as explicit conflicts.

## Cross-cutting behavior-policy tasks

- [ ] `006-POL-S5-001` Define behavior-policy precedence and monotonic narrowing with no executable policy loading.
- [ ] `006-POL-S6-001` Implement mandatory pre-effect policy gate integration only after the owning policy/runtime authority exists; policy `NO_OBJECTION` never becomes a Nawat grant.
- [ ] `006-POL-S6-002` Add agent/session policy proposal flow where activation follows user/controlling authority rather than agent self-activation.
- [ ] `006-POL-S6-003` Qualify any executable/sandboxed policy-plugin mechanism separately for source/dependency/process/security risks.
- [ ] `006-POL-S7-001` Record policy snapshot/evaluation evidence sufficient to explain why an effect was narrowed/blocked/required-decision without treating policy as completion authority.

## Negative oracles

```text
HOST_ID_CLAIM_CANNOT_AUTHENTICATE_HOST
REVOKED_HOST_CANNOT_REJOIN_AS_TRUSTED
STALE_RUNNER_EPOCH_CANNOT_EFFECT
EXPIRED_RUNNER_LEASE_CANNOT_EFFECT
DUPLICATE_RUNTIME_EVENT_CANNOT_DUPLICATE_EFFECT
OUT_OF_ORDER_EVENT_CANNOT_REWRITE_CAUSAL_HISTORY_SILENTLY
HARNESS_AUTO_UPDATE_STALES_MATERIAL_QUALIFICATION
RESOURCE_EXHAUSTION_NOT_PROVIDER_FAILURE
UNKNOWN_EFFECTFUL_PROTOCOL_VERSION_FAILS_CLOSED
POLICY_NO_OBJECTION_CANNOT_EXECUTE_WITHOUT_NAWAT
UNTRUSTED_POLICY_MODULE_CANNOT_AUTO_LOAD
LOWER_TRUST_POLICY_CANNOT_WEAKEN_STRONGER_RESTRICTION
```

## Privacy and retention prerequisites

- [ ] `006-RT-S6-PRIV001` Before any S6 event persistence/egress, implement bounded payloads, access checks, classification and secret exclusion under Assurance EvidenceHandlingPolicy. Raw environment values, reusable secrets, bearer placeholders and private browser/session payloads must not enter ordinary runtime events, logs or replay records. Only safe names/classes and protected references are eligible.
- [ ] `006-RT-S9-PRIV001` Depends on 006-RT-S6-PRIV001 and 006-RT-S9-001/002: qualify export, backup/restore, migration and tombstone propagation with seeded raw-environment/reusable-secret fixtures; prove exclusion at capture and after replay/export. A later redaction pass cannot excuse an earlier plaintext leak. Minimum privacy precedes S6 execution; S9 adds durable-history verification.

## Requirement and acceptance lookup

Every task in this file maps bidirectionally through `analyze.md` section Supporting-package bidirectional traceability to its requirements, canonical owner, acceptance family, evidence expectation and roadmap gate. Product refinements also consume `product-capability-tracks-plan.md` sections 14–17. The complete owning contract governs; local summaries never weaken it. Future task completion requires implementation qualification under then-current authority, not merely this planning text.
