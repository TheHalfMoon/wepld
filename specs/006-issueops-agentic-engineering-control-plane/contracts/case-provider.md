# Contract — Case / Provider Adapter Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
PROVIDER_NETWORK_AUTHORITY = NONE
PROVIDER_WRITE_AUTHORITY = NONE
```

## Boundary

External issue/ticket/error systems are adapters into a WePLD-owned `Case` model. Provider APIs never define internal completion, authority, or durable identity semantics.

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

A normalized provider observation must retain:

```text
provider_kind
provider_account_or_host
external_object_kind
external_object_id
canonical_locator
observed_version_or_etag_or_equivalent?
observed_state
observed_at
raw_or_hash-addressed_provider_evidence_ref
normalization_version
```

Normalization must not discard contradictory provider evidence.

## Write preconditions

Before any provider effect, the owning implementation must establish the exact required snapshot, including as applicable:

- provider/account identity;
- target object identity;
- target freshness/version;
- requested mutation identity;
- current Case/work identity;
- autonomy ceiling;
- route qualification;
- Nawat grant/revalidation;
- retry/idempotency identity;
- expected postcondition.

A stale or mismatched target fails closed.

## Idempotency / duplicate delivery

External events may be duplicated, reordered, or retried. The adapter contract must define deduplication/idempotency behavior per effect. Replaying one WePLD effect identity must not silently create repeated provider mutations.

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

## Provider closeout

Provider `closed`, `merged`, `resolved`, or equivalent states are observations/effects. They do not automatically produce `COMPLETED_TRUSTED`.

## Provider outage / permission loss

Loss of provider availability or permission becomes explicit Case/work evidence (`WAITING_EXTERNAL`, blocked capability, stale observation, etc.). WePLD must not pretend current provider state is known when it cannot be refreshed.
