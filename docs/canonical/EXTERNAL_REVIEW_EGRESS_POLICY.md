# External Review Egress Policy

## Purpose

This policy governs sending repository content to hosted/external review systems, including CodeRabbit, Qodo, Augment Code, Graphite-hosted review surfaces, Cubic cloud review, Continue-hosted services, Greptile-hosted review surfaces, and Codex Security when those products process content outside the trusted local boundary.

External review is evidence production, not authority.

## Fail-closed eligibility

Before any external review run, classify the exact content scope:

```text
PUBLIC_SOURCE_ONLY
APPROVED_NON_PUBLIC_SOURCE
PROHIBITED_EGRESS
```

`PROHIBITED_EGRESS` includes secrets, credentials, tokens, signing material, private keys, private customer data, PHI/PII not explicitly approved for the destination, private third-party source without egress rights, incident forensics restricted from the provider, or any content whose handling requirements are not satisfied.

Unknown classification is `PROHIBITED_EGRESS` until resolved.

## Automatic-trigger boundary

An automated external-review trigger that can transmit repository content before this policy's classification, screening, provider-handling decision, and egress approval is complete is prohibited.

Until WePLD has a machine-enforced pre-egress gate that runs before transmission, hosted external reviewers must remain manual/explicit opt-in. A provider integration may stay installed or connected, but repository configuration must not automatically start review on PR creation, Draft state, push, or incremental commit.

A manual review command may be issued only after the exact review scope has a recorded egress preflight satisfying this policy. Enabling or resuming automatic review requires a separately reviewed machine-enforced pre-egress design; reviewer convenience or quota pressure is not an exception.

```text
UNSCREENED_AUTOMATIC_EXTERNAL_REVIEW = PROHIBITED_EGRESS
CONNECTED_EXTERNAL_REVIEWER != EGRESS_AUTHORIZED
MANUAL_REVIEW_TRIGGER_REQUIRES_RECORDED_PREFLIGHT = YES
```

## Allowed file scope

The review request must use the minimum necessary scope:

1. exact changed files with applicable review effect;
2. deleted baseline files when required to understand the change;
3. only the smallest supporting files needed to validate behavior, findings, or attack paths.

Do not upload unrelated repository history, `.git` objects, environment files, credential stores, local caches, user home content, database dumps, build artifacts, or private workspaces merely for convenience.

Broad repository upload requires a separately recorded justification and egress approval.

## Secret and private-data screening

Before egress of any repository content:

- run an approved secret/private-data screening step appropriate to the repository;
- remove or redact detected credentials and prohibited private data before transfer;
- if the required screening capability is unavailable, record `EGRESS_BLOCKED` rather than assuming the content is clean;
- never rely on the external reviewer itself to discover secrets after transmission.

Redaction must preserve enough context for the requested review without reconstructing the protected value.

## Provider data-handling gate

For `PUBLIC_SOURCE_ONLY`, repository content may be sent only when the provider identity is known and the user/founder has authorized that external review surface.

For `APPROVED_NON_PUBLIC_SOURCE`, the evaluation record must additionally establish, from current official/provider terms or an applicable contract:

- retention period or no-retention commitment;
- whether content may be used for model training/product improvement;
- tenant isolation / access-control model;
- subprocessors or material onward-processing constraints when applicable;
- deletion/expiry behavior;
- region/residency requirements when applicable.

If required retention, isolation, training-use, or contractual facts are unknown or incompatible with project policy, external review is blocked for that content.

## Egress record

Every external review record must include:

```text
PROVIDER / PRODUCT
OFFICIAL_REFERENCE
EVALUATION_DATE
BASE_SHA / HEAD_SHA or immutable scope
FILE_SCOPE
CONTENT_CLASSIFICATION
SCREENING_EVIDENCE
REDACTIONS
RETENTION / TRAINING-USE DECISION
TENANT-ISOLATION DECISION
EGRESS_APPROVAL
RESULT / COVERAGE LIMITATIONS
```

## Authority invariants

```text
EGRESS_ALLOWED != EFFECT_AUTHORITY
EXTERNAL_REVIEW_AVAILABLE != EGRESS_AUTHORIZED
EXTERNAL_REVIEW_RESULT != CompletionDecision
PROVIDER_POLICY_UNKNOWN + NON_PUBLIC_CONTENT = EGRESS_BLOCKED
SECRET_SCREENING_UNAVAILABLE = EGRESS_BLOCKED for protected content
```

Nawat/AMAN ownership applies when those subsystems are implemented. Before then, egress requires the current explicit founder-authorized repository/review scope and must remain within this policy.
