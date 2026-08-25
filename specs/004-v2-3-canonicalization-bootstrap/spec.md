# Spec — 004 V2.3 Canonicalization Bootstrap

## Problem

Spec 003 is merged and qualified as a non-canonical V2.3 Agent Control Plane planning candidate. Canonical `docs/canonical/MASTER_PLAN_INDEX.md` remains V2.2 and is a base-controlled governance file. Ordinary candidate PRs are intentionally unable to mutate it.

## Goal

Create and qualify the smallest bootstrap mechanism that can authorize one later, exact V2.3 canonicalization transition while preserving all existing source/dependency/runtime/model boundaries.

## User stories

### US1 — Fail-closed canonicalization bootstrap
As the founder, I can adopt a previously qualified architecture candidate without weakening the general rule that candidate branches cannot rewrite the governance used to judge them.

Acceptance:
- the bootstrap is a separate PR from the canonicalization PR;
- the bootstrap policy is successor-only and binds its predecessor by immutable identity;
- its bootstrap delta is exact and does not contain the canonical-plan mutation itself;
- post-bootstrap steady state authorizes exactly one canonicalization path-set/content transformation;
- unrelated base-controlled changes remain rejected.

### US2 — Exact canonical V2.3 adoption
As the project, I can make V2.3 canonical only when the exact new canonical plan bytes and index bytes are derived from the already-merged V2.3 candidate and independently qualified.

Acceptance:
- canonical plan content derives from the exact merged candidate blob;
- `MASTER_PLAN_INDEX.md` becomes V2.3 and points to the exact canonical plan document;
- P0 + S1..S10 numbering is unchanged;
- no source registry, acquisition PR, runtime, dependency, model, or provider authority changes;
- exact-head checks and independent review bind the same final head;
- **post-merge V2.3 canonicalization activation** passes.

## Out of scope

```text
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = NONE
PRODUCT_RUNTIME_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
MODEL_WEIGHT_ACCESS = NONE
MODEL_INFERENCE = NONE
PICTORIAL_AGILE_PR_MUTATION = NONE
FROZEN_402_REGISTRY_MUTATION = NONE
ROADMAP_RENUMBERING = NONE
```

## Security classification

The bootstrap changes CI/admission-policy trust behavior and is security-relevant. Deterministic self-tests, trusted-base qualification, exact-head correctness review, and Codex Security when available/egress-permitted apply. Codex Security unavailability is `NOT_RUN_NON_BLOCKING`, never PASS.
