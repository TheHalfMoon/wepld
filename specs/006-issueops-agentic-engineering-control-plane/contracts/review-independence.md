# Contract — Review Independence

```text
STATUS = FUTURE_PLANNING_CONTRACT
PRIMARY_OWNER = S7_NATIVE_REVIEW_AND_ASSURANCE
COMPLETION_AUTHORITY = TRUSTED_COMPLETION_ONLY
REPAIR_AUTHORITY = S8_ONLY_WHEN_SEPARATELY_AUTHORIZED
CURRENT_IMPLEMENTATION_AUTHORITY = NONE
```

## Purpose

Make reviewer independence a typed, auditable property rather than a prose claim such as "different agent" or "different vendor".

This contract is consumed by `contracts/assurance-fabric.md` whenever an `AssurancePolicySnapshot` requires independent review evidence.

## Core invariant

```text
BUILDER != REVIEWER
```

is necessary but not always sufficient.

A qualified independence policy may also require separation of worker identity, model/provider family, mutable workspace, process/session, context, write authority, or organizational conflict-of-interest depending on the claim/risk class.

## `ReviewIndependenceReceipt`

```text
ReviewIndependenceReceipt {
  review_independence_receipt_id
  reviewed_target_identity
  assurance_policy_snapshot_ref
  independence_policy_id
  independence_policy_version
  builder_attempt_refs[]
  builder_worker_ids[]
  builder_provider_model_harness_identities[]
  builder_workspace_or_execution_context_refs[]
  reviewer_attempt_ref
  reviewer_worker_id
  reviewer_provider_model_harness_identity
  reviewer_workspace_or_execution_context_ref
  reviewer_effect_authority_state
  shared_context_refs[]
  excluded_context_classes[]
  mutable_state_overlap_observations[]
  identity_conflict_observations[]
  authority_conflict_observations[]
  independence_checks[]
  result
  evidence_refs[]
  created_at
}
```

Candidate results:

```text
SATISFIES_POLICY
DOES_NOT_SATISFY_POLICY
INCONCLUSIVE
STALE
```

## Policy dimensions

An `IndependencePolicy` may require any combination of:

```text
DISTINCT_WORKER_IDENTITY
DISTINCT_ATTEMPT_IDENTITY
DISTINCT_PROVIDER
DISTINCT_MODEL_FAMILY
DISTINCT_HARNESS_IMPLEMENTATION
NO_MUTABLE_BUILDER_WORKTREE_ACCESS
NO_BUILDER_PROCESS_OR_SESSION_INHERITANCE
NO_BUILDER_PRIVATE_CHAIN_OF_ACTIONS_UNLESS_EXPLICITLY_ALLOWED
DIFF_PLUS_CONTRACT_ONLY_CONTEXT
READ_ONLY_REVIEW_EFFECT_PROFILE
NO_ACCEPTANCE_CRITICAL_WRITE_AUTHORITY
NO_SELF_REVIEW_OF_REPAIR
NO_SHARED_UNREVIEWED_TOOL_OUTPUT_AS_SOLE_EVIDENCE
```

Different-vendor review, as demonstrated by Omnigent Polly, is a valuable default signal but cannot alone establish every policy dimension.

## Context separation

The reviewer should receive the minimum context needed to judge the claim. Depending on policy this can include:

```text
exact diff/target
specification/acceptance contract
relevant architecture/code context
required test/security evidence
known findings requiring reconciliation
```

It may intentionally exclude:

```text
builder persuasive narrative
builder hidden scratch reasoning
mutable builder worktree
unreviewed builder-generated verdict summaries
credentials/effect grants unnecessary for review
```

Exclusion is not universal: some reviews need broader architectural history. The policy snapshot defines the required context, and the receipt records what was actually shared.

## Authority separation

A reviewer may need read/analysis/tool execution authority, but an independent review worker should not automatically inherit the builder's effect grants.

```text
BUILDER_GRANT != REVIEWER_GRANT
REVIEWER_FINDING != REPAIR_AUTHORITY
REVIEWER_APPROVAL != TRUSTED_COMPLETION
```

If a reviewer also performs a repair, the repaired target requires a new independent review according to the owning policy unless a narrowly defined policy explicitly permits otherwise.

## Exact-target freshness

The receipt binds one exact target. Any material target change creates stale independence evidence for acceptance of the new target.

```text
NEW_EXACT_HEAD -> PRIOR_REVIEW_INDEPENDENCE_RECEIPT_STALE_FOR_ACCEPTANCE
```

Historical receipts remain audit evidence.

## Required negative oracles

```text
SAME_ATTEMPT_CANNOT_REVIEW_OWN_ACCEPTANCE_CRITICAL_CHANGE
DIFFERENT_VENDOR_WITH_SHARED_MUTABLE_BUILDER_WORKSPACE_MAY_FAIL_POLICY
REVIEWER_WITH_BUILDER_WRITE_GRANT_MAY_FAIL_STRICT_POLICY
STALE_HEAD_REVIEW_CANNOT_SATISFY_CURRENT_HEAD
BUILDER_SUMMARY_ONLY_WITHOUT_REQUIRED_TARGET_CONTEXT_CANNOT_SATISFY_REVIEW_COVERAGE
REVIEWER_REPAIR_CANNOT_SELF_CERTIFY_THE_REPAIRED_HEAD
MULTIPLE_CLEAN_REVIEWERS_CANNOT_ERASE_ONE_VALIDATED_FINDING
```

## Omnigent source note

Omnigent's Polly workflow is a high-value behavior oracle because it routes review to a different vendor and deliberately isolates the reviewer to diff + contract rather than the implementer's worktree/transcript. WePLD adopts the stronger typed receipt model above; Omnigent does not define WePLD's independence authority.