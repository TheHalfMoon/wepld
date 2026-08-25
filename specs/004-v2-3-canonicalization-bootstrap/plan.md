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
- exact-head egress preflight under `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` before any hosted reviewer trigger;
- at least one independently qualified engineering review; if unavailable, record `REVIEW_BLOCKED` and stop rather than inferring PASS;
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

The canonical v4 trusted-base admission policy cannot authorize an unseen v5 successor. This is the same structural bootstrap limitation recorded for PR #169 (v3 -> v4). Therefore the v5 bootstrap qualification MUST preserve the old-base result truthfully:

```text
TRUSTED_BASE_V4_CLASS = EXPECTED_BOOTSTRAP_FAILURE
OLD_BASE_S1_PASS = NO
EXPECTED_BOOTSTRAP_FAILURE != PASS
```

The expected old-base failure is not a waiver and is never relabeled PASS. The separate bootstrap event instead requires exact-head candidate Foundation/self-tests, every other applicable deterministic gate, applicable security accounting, independent exact-head engineering review, finding reconciliation, and a final live race. Candidate-side Foundation verification remains non-authoritative evidence; standing founder authorization permits the governed bootstrap event but does not convert any failed gate to PASS.

Because this phase changes CI/admission trust behavior, security review is applicable.

## Phase 3 — Prove v5 policy activation

Merge the v5 bootstrap only after the bounded bootstrap qualification above is complete and the expected old-base failure is explicitly preserved. Then require **post-merge Foundation activation on canonical v5 main** to PASS on the v5 merge commit.

The first successor PR that relies on v5 authority is the V2.3 canonicalization PR in Phase 4. Its trusted-base `s1-admission-integrity` run MUST execute v5 from canonical v5 main and PASS before that PR can merge. That exact successor PASS is the authoritative proof that the new trusted-base route is active.

## Phase 4 — V2.3 canonicalization PR

Create a separate branch from activated v5 `main`.

Exact intended transition:
1. add `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`, deterministically derived from the exact merged candidate `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md` by changing only canonical-status/title metadata required to remove candidate semantics;
2. update `docs/canonical/MASTER_PLAN_INDEX.md` to `CANONICAL_PLAN_VERSION = V2.3`, point to the canonical V2.3 document, retain `ROADMAP = P0 + S1..S10`, and state bounded enrichment rather than architecture restart.

The v5 policy must verify the trusted-base candidate blob identity and exact canonicalization transformation rather than accepting arbitrary plan text.

## Phase 5 — V2.3 canonicalization qualification and activation

Require:
- Foundation exact-head PASS;
- trusted-base v5 admission exact-head PASS;
- changed-file set exactly the two canonicalization files;
- exact-head egress preflight under `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` before any hosted external review trigger;
- independent exact-head engineering review; if unavailable, record `REVIEW_BLOCKED` and stop rather than inferring PASS;
- all material findings reconciled;
- requalification after any repair;
- final live race;
- merge with expected-head binding;
- **post-merge V2.3 canonicalization activation** PASS;
- direct re-read of `MASTER_PLAN_INDEX.md` on canonical main proving V2.3.

## Phase 6 — Continue roadmap

After V2.3 is canonically activated, re-read the canonical plan and identify the next eligible roadmap unit from repository truth. Canonicalization does not itself authorize any future source/runtime/dependency/model gate.
