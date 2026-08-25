# Plan — Spec 004 V2.3 Canonicalization Bootstrap

## Phase 0 — Trusted baseline

Bind all work to live canonical `main` and its trusted governance. Confirm:

```text
CANONICAL_PLAN_VERSION = V2.2
V2_3_PLANNING_CANDIDATE = PERSISTED_ON_MAIN
SPEC_003 = COMPLETE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_RUNTIME_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

Do not mutate active Pictorial/Agile acquisition PRs in this work.

## Phase 1 — Spec 004 planning qualification

This planning package is documentation-only and must remain within the current bounded planning route. Require on the exact final planning head:
- Foundation PASS;
- trusted-base `s1-admission-integrity` PASS;
- exact changed-file set = Spec 004 Markdown only;
- exact-head egress preflight before any hosted reviewer trigger;
- at least one independently qualified engineering review;
- reconciliation of every material finding;
- fresh requalification after every head change;
- final live base/head/check/review race.

## Phase 2 — Bootstrap policy v5

Create a separate policy-migration branch from then-current canonical main.

Minimum bootstrap delta:

```text
.github/scripts/wepld_s1_admission_steady_state_routing_v5_integrity.py
.github/workflows/foundation-integrity.yml
.github/workflows/s1-admission-integrity.yml
```

The v5 wrapper must:
- bind exact v4 predecessor identity before import;
- bind exact predecessor workflow identities;
- allow only the exact three-file v5 bootstrap delta when v5 is absent from the trusted base;
- preserve v4 token-isolation and local trusted-base worktree behavior;
- after activation, preserve all ordinary v4 routes unchanged;
- add exactly one canonicalization route for the V2.3 transition;
- fail closed for every other base-controlled path mutation;
- include deterministic positive and negative self-tests;
- report no source/dependency/donor/runtime/model authority expansion.

Because this phase changes CI/admission trust behavior, security review is applicable.

## Phase 3 — Prove v5 activation

Qualify the exact bootstrap head with every applicable deterministic and independent-review gate. Merge only after final live race. Then require post-merge Foundation/canonical activation PASS on the merge commit before Phase 4.

## Phase 4 — V2.3 canonicalization PR

Create a separate branch from activated v5 `main`.

Exact intended transition:
1. add `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`, deterministically derived from the exact merged candidate `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md` by changing only canonical-status/title metadata required to remove candidate semantics;
2. update `docs/canonical/MASTER_PLAN_INDEX.md` to `CANONICAL_PLAN_VERSION = V2.3`, point to the canonical V2.3 document, retain `ROADMAP = P0 + S1..S10`, and state bounded enrichment rather than architecture restart.

The v5 policy must verify the trusted-base candidate blob identity and exact canonicalization transformation rather than accepting arbitrary plan text.

## Phase 5 — Canonicalization qualification and activation

Require:
- Foundation exact-head PASS;
- trusted-base admission exact-head PASS;
- changed-file set exactly the two canonicalization files;
- independent exact-head engineering review;
- all material findings reconciled;
- requalification after any repair;
- final live race;
- merge with expected-head binding;
- post-merge canonical activation PASS;
- direct re-read of `MASTER_PLAN_INDEX.md` on canonical main proving V2.3.

## Phase 6 — Continue roadmap

After V2.3 is canonically activated, re-read the canonical plan and identify the next eligible roadmap unit from repository truth. Canonicalization does not itself authorize any future source/runtime/dependency/model gate.
