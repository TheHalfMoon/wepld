# Acceptance — Spec 004 V2.3 Canonicalization Bootstrap

Spec 004 planning is accepted only when the exact final planning head satisfies all of the following:

- the changed-file set contains only Markdown files under `specs/004-v2-3-canonicalization-bootstrap/`;
- canonical `MASTER_PLAN_INDEX.md` remains byte-identical V2.2 in this planning PR;
- the already-merged V2.3 Agent Control Plane document remains explicitly non-canonical in this planning PR;
- the package preserves `P0 + S1..S10` and does not mutate the frozen 402-entry registry;
- no Pictorial/Agile/MiniMax acquisition PR is mutated or coupled to this work;
- Source Acquisition Check concludes that no new external source/dependency/runtime/provider is required;
- Ponytail FULL selects the minimum two-event design: separate policy bootstrap, then separate exact canonicalization;
- Foundation and trusted-base `s1-admission-integrity` both pass for the same exact planning head;
- before any hosted external review trigger, an exact-head egress preflight is recorded under the canonical egress policy;
- at least one independently qualified engineering reviewer reviews the exact final head;
- every material finding is reconciled;
- every head-changing repair invalidates prior exact-head qualification and causes deterministic checks, egress preflight where applicable, and independent review to be repeated;
- the final live race re-reads PR base/head, exact changed files, both deterministic checks, review state/threads, and unresolved material findings before acceptance;
- merge uses the exact qualified head and post-merge canonical activation is verified.

Acceptance of Spec 004 authorizes only execution of the governed bootstrap/canonicalization sequence described by the package under standing founder authorization. It does not itself make V2.3 canonical and does not grant source, dependency, donor-execution, runtime, model-provider, model-weight, inference, or future-slice implementation authority.

```text
SPEC_004_ACCEPTED != V2_3_CANONICAL
POLICY_BOOTSTRAP_MERGED != V2_3_CANONICAL
V2_3_CANONICAL != SOURCE_ADMISSION
V2_3_CANONICAL != PRODUCT_RUNTIME_AUTHORITY
GREEN_CI != ACCEPTANCE
REVIEW_CLEAN != COMPLETION_DECISION
```
