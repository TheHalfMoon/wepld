# Contract — Case / Provider Adapter Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
PROVIDER_NETWORK_AUTHORITY = NONE
PROVIDER_WRITE_AUTHORITY = NONE
```

## Boundary

External issue/ticket/error systems are adapters into a WePLD-owned `Case` model. Provider APIs never define internal completion, authority, or durable identity semantics.

Shared durable entity shapes in this contract MUST use the canonical field vocabulary in `../data-model.md`. Provider-specific extensions may add namespaced fields but may not redefine shared identities.

## Required adapter operations

Every provider adapter declares which operations it actually supports and which are read-only vs effectful.

### Observation candidates

```text
observe_object
observe_timeline
observe_relationships
observe_checks_or_status
observe_review_state
observe_attachments
observe_version_or_freshness
```

### Effect candidates

```text
create_object
update_body_or_metadata
comment
label_or_tag
assign
link
create_or_update_change_request
merge_or_land
close
reopen
```

Unsupported operations remain explicitly unsupported.

## Observation envelope

The canonical normalized provider observation is the `ProviderObservation` record in `../data-model.md` and must retain at least:

```text
provider_observation_id
binding_id
provider_version_or_etag?
observed_state
observed_relationships[]
observed_at
raw_or_hash_addressed_evidence_ref
adapter_identity
normalization_contract_version
observation_completeness
observation_authenticity
```

Provider/account/object identity is resolved through the referenced `ProviderBinding`; it MUST NOT be copied into a second mutable identity vocabulary inside the observation.

`normalization_contract_version` is the single canonical normalizer-version field. A second ambiguous `normalization_version` field is prohibited.

Normalization must not discard contradictory provider evidence or provider-native fields needed to reconstruct/inspect the source observation.

### Observation completeness

Provider reads may be paginated, permission-filtered, rate-limited, truncated, or interrupted. Every acceptance-relevant observation must classify completeness:

```text
COMPLETE
PARTIAL_PAGINATION
PARTIAL_PERMISSION
PARTIAL_RATE_LIMIT
PARTIAL_TIMEOUT
UNKNOWN_COMPLETENESS
```

```text
PARTIAL_OBSERVATION != COMPLETE_CURRENT_PROVIDER_STATE
UNKNOWN_COMPLETENESS != COMPLETE_CURRENT_PROVIDER_STATE
```

A dependent effect or completion claim that requires complete current state fails closed when the required observation is partial or unknown.

### Observation authenticity

Inbound provider events and webhooks must retain authenticity evidence appropriate to the provider transport, for example verified signature/delivery identity, authenticated API observation, or an explicit `AUTHENTICITY_NOT_ESTABLISHED` state.

```text
EVENT_RECEIVED != EVENT_AUTHENTICATED
WEBHOOK_PAYLOAD != TRUSTED_PROVIDER_OBSERVATION_UNTIL_AUTHENTICATED
```

Authenticity evidence does not create effect authority.

## Conflicting provider observations

Provider observations are append-only evidence, not last-write-wins mutable truth. A Case may have contradictory observations across time or providers.

The canonical derived conflict record is `ProviderConflict` from `../data-model.md`:

```text
provider_conflict_id
case_id
subject_semantic
observation_refs[]
conflict_kind
resolution_state
resolution_rule_or_decision_ref?
first_detected_at
latest_evaluated_at
```

Candidate conflict kinds include:

```text
TEMPORAL_STALENESS
CROSS_PROVIDER_STATE_DISAGREEMENT
RELATIONSHIP_DISAGREEMENT
IDENTITY_BINDING_AMBIGUITY
NORMALIZATION_SEMANTIC_CONFLICT
PERMISSION_OR_VISIBILITY_GAP
OBSERVATION_COMPLETENESS_GAP
OBSERVATION_AUTHENTICITY_GAP
```

Rules:

- latest timestamp alone is not a universal conflict resolver;
- one provider's `closed`, `resolved`, `merged`, severity, assignee, or status cannot overwrite another provider observation;
- derived Case state must surface conflict when a controlling workflow requires a single current semantic and evidence is contradictory;
- automated effects that depend on disputed state fail closed, abstain, or open a `DecisionBoundary` according to the owning contract;
- a conflict resolution preserves the losing/older observations and the evidence for the chosen resolution;
- provider outage or permission loss may make an observation stale but does not erase it.

## Case-binding rules

Multiple external provider objects may bind to one Case only through evidence-backed binding logic. Similar titles, embeddings, labels, or issue numbers are candidate evidence only and MUST NOT silently merge two durable Cases.

Binding classes should distinguish at least:

```text
EXPLICIT_USER_OR_PROVIDER_LINK
EXACT_EXTERNAL_REFERENCE
QUALIFIED_DUPLICATE_RELATION
PROBABLE_RELATION_ONLY
UNRESOLVED_BINDING_CANDIDATE
```

A probable relation does not collapse Case identity.

## Read backpressure / provider health

Provider adapters must surface rate limiting and availability rather than hide them behind infinite retry.

Candidate route states:

```text
AVAILABLE
RATE_LIMITED
RETRY_AFTER
AUTH_BLOCKED
PERMISSION_BLOCKED
PROVIDER_UNAVAILABLE
PARTIAL_READ
```

Backoff policy is bounded and inspectable. A stale cached observation may be shown as historical evidence but cannot masquerade as a fresh provider read.

## Write preconditions

Before any provider effect, the owning implementation must establish the exact required snapshot, including as applicable:

- provider/account identity;
- target object identity;
- target freshness/version;
- requested mutation identity;
- current Case/work identity;
- relevant provider-conflict state;
- observation completeness/authenticity required by the effect;
- autonomy ceiling;
- route qualification;
- Nawat grant/revalidation;
- retry/idempotency identity;
- expected postcondition.

A stale, incomplete where completeness is required, unauthenticated where authenticity is required, conflicted where single-state certainty is required, or mismatched target fails closed.

## Idempotency / duplicate delivery

External events may be duplicated, reordered, or retried. The adapter contract must define deduplication/idempotency behavior per effect and observation source. Replaying one WePLD effect identity must not silently create repeated provider mutations. Duplicate observation delivery must preserve one logical observation identity or an explicit duplicate relation rather than manufacture contradictory Case state.

## Unknown effect outcome / crash recovery

A process/network interruption can occur after an external provider accepted an effect but before WePLD durably recorded the response. This state is first-class:

```text
EFFECT_OUTCOME_UNKNOWN
```

Recovery must not blindly retry. The owning adapter must reconcile using the exact effect identity, idempotency key where supported, target/version observation, and expected postcondition:

```text
EFFECT_OUTCOME_UNKNOWN
  -> CONFIRMED_APPLIED
   | CONFIRMED_NOT_APPLIED
   | STILL_UNKNOWN
```

Retry is allowed only after `CONFIRMED_NOT_APPLIED` or when provider-native idempotency semantics prove replay safe under the exact effect identity.

```text
LOCAL_TIMEOUT != REMOTE_EFFECT_NOT_APPLIED
CONNECTION_LOSS != SAFE_TO_RETRY
UNKNOWN_EFFECT_OUTCOME != FAILURE_WITH_NO_SIDE_EFFECT
```

## Provider edits, deletion, and redaction

Append-only evidence does not mean retaining prohibited content forever. If provider content is edited, deleted, legally removed, or access is revoked:

- preserve the observation/event identity and minimum non-sensitive provenance needed for audit;
- apply the governing evidence-handling/redaction policy to protected content;
- use tombstone/redaction metadata rather than silently rewriting history;
- derived Case state and retrieval projections must stop exposing content that is no longer authorized for visibility.

## GitHub reference adapter

GitHub is the first planned adapter and should cover Issues + PRs in incremental authority classes:

1. issue/PR metadata read;
2. timeline/comments/reviews/checks read;
3. comment write;
4. label/assignee/milestone write;
5. PR create/update;
6. review-thread operations where qualified;
7. expected-head guarded merge;
8. issue close/reopen.

Later providers must fit the same Case/provider contract rather than expand the core model with provider-specific state.

## Provider / Case schema evolution

The core Case model should evolve only for provider-independent engineering semantics that are demonstrated by more than one provider/workflow need or are required by a canonical invariant. Provider-specific features remain typed adapter observations/extensions until such promotion is justified.

Each adapter revision must declare:

```text
adapter_contract_version
normalization_contract_version
supported_external_object_kinds[]
observation_capabilities[]
effect_capabilities[]
provider_extension_schema_version?
migration_or_compatibility_policy
pagination_and_completeness_policy
rate_limit_and_backoff_policy
webhook_or_event_authenticity_policy?
```

Evolution rules:

1. unknown provider-native fields remain available through raw/hash-addressed evidence when handling policy permits, even when the current normalizer does not model them;
2. a new provider cannot redefine existing Case lifecycle or completion semantics;
3. incompatible normalization changes require explicit versioning and replay/migration behavior;
4. derived Case state records which normalization contract produced it;
5. old evidence remains inspectable subject to redaction/retention/access policy after adapter upgrades;
6. migration must not silently convert probable relations/conflicts into exact identity.

## Provider closeout

Provider `closed`, `merged`, `resolved`, or equivalent states are observations/effects. They do not automatically produce `COMPLETED_TRUSTED`.

## Provider outage / permission loss

Loss of provider availability or permission becomes explicit Case/work evidence (`WAITING_EXTERNAL`, blocked capability, stale observation, partial observation, etc.). WePLD must not pretend current provider state is known when it cannot be refreshed.

## Required negative oracles

```text
CROSS_PROVIDER_DISAGREEMENT_IS_PRESERVED
LATEST_WRITE_DOES_NOT_SILENTLY_RESOLVE_SEMANTIC_CONFLICT
PROBABLE_DUPLICATE_DOES_NOT_MERGE_CASE_IDENTITY
STALE_OR_CONFLICTED_TARGET_BLOCKS_DEPENDENT_WRITE
PARTIAL_PROVIDER_OBSERVATION_NOT_COMPLETE_STATE
UNAUTHENTICATED_WEBHOOK_NOT_TRUSTED_OBSERVATION
ADAPTER_UPGRADE_PRESERVES_OLD_OBSERVATION_PROVENANCE
DUPLICATE_WEBHOOK_DOES_NOT_DUPLICATE_PROVIDER_EFFECT
RATE_LIMIT_DOES_NOT_SILENTLY_RETURN_STALE_AS_FRESH
UNKNOWN_EFFECT_OUTCOME_IS_RECONCILED_BEFORE_RETRY
PROVIDER_REDACTION_PROPAGATES_TO_DERIVED_VISIBILITY
```
