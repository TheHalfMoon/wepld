# Constitution — Spec 004 V2.3 Canonicalization Bootstrap

## Purpose

Govern the minimum non-destructive bootstrap required to make the already-merged V2.3 Agent Control Plane planning candidate eligible for canonical-plan adoption without allowing a candidate branch to rewrite its own acceptance policy.

## Invariants

```text
TRUSTED_BASE_GOVERNANCE = AUTHORITY
CANDIDATE_BOOTSTRAP_TEXT != AUTHORITY
V2_3_CANDIDATE != CANONICAL_V2_3
POLICY_BOOTSTRAP != PLAN_CANONICALIZATION
PLAN_CANONICALIZATION != SOURCE_ADMISSION
PLAN_CANONICALIZATION != DEPENDENCY_ADMISSION
PLAN_CANONICALIZATION != PRODUCT_RUNTIME_AUTHORITY
PLAN_CANONICALIZATION != MODEL_PROVIDER_EXECUTION
```

The work MUST preserve P0 + S1..S10 numbering, the frozen 402-entry source-registry evidence, current source/dependency/runtime/model boundaries, and the separation of Nawat authority, Fehrest evidence, AMAN security evidence, Assurance review, and Trusted Completion.

## Required execution shape

1. Plan and qualify this Spec 004 package under the current V2.2 trusted base.
2. Bootstrap a successor admission policy that authorizes only the exact future V2.3 canonicalization transition.
3. Qualify, independently review, merge, and prove **post-merge Foundation activation on canonical v5 main** for that bootstrap policy.
4. Create the separate V2.3 canonicalization PR.
5. Require exact-head deterministic checks, independent review, finding reconciliation, final live race, merge, and **post-merge V2.3 canonicalization activation**.
6. Only after V2.3 canonicalization activation may later roadmap work use V2.3 as canonical planning authority.

No source import, dependency install/admission, donor execution, provider/model access, inference, or product-runtime expansion is authorized by Spec 004.
