# Acceptance — Spec 004 V2.3 Canonicalization Bootstrap

Spec 004 planning is accepted only when the exact final planning head satisfies all of the following:

- the changed-file set contains only Markdown files under `specs/004-v2-3-canonicalization-bootstrap/`;
- canonical `MASTER_PLAN_INDEX.md` remains byte-identical V2.2 in this planning PR;
- the already-merged V2.3 Agent Control Plane document remains explicitly non-canonical in this planning PR;
- the package preserves `P0 + S1..S10` and does not mutate the frozen 402-entry registry;
- no Pictorial/Agile/MiniMax acquisition PR is mutated or coupled to this work;
- Source Acquisition Check concludes that no new external source/dependency/runtime/provider is required;
- Ponytail FULL selects the minimum two-event design: separate policy bootstrap, then separate exact canonicalization;
- Foundation and trusted-base `s1-admission-integrity` both pass for the same exact **Spec 004 planning head**;
- before any hosted external review trigger, an exact-head egress preflight is recorded under `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`, covering scope classification, secret/private-data screening, provider-handling decisions, `EGRESS_APPROVAL`, and advisory-result limitations;
- at least one independently qualified engineering reviewer reviews the exact final head; if no independently qualified reviewer is available, record `REVIEW_BLOCKED` and stop rather than inferring PASS;
- every material finding is reconciled;
- every head-changing repair invalidates prior exact-head qualification and causes deterministic checks, egress preflight where applicable, and independent review to be repeated;
- the final live race re-reads PR base/head, exact changed files, both deterministic checks, review state/threads, and unresolved material findings before acceptance;
- merge uses the exact qualified head and **post-merge Foundation activation on canonical main** is verified.

The planning-head trusted-base PASS above does **not** impose an impossible old-base PASS on the later policy-successor bootstrap. The v5 bootstrap is a separately governed event. Canonical PR #169 records the controlling precedent: an old canonical policy cannot authorize an unseen successor policy. Therefore v4 -> v5 must preserve the old-base result as:

```text
TRUSTED_BASE_V4_CLASS=EXPECTED_BOOTSTRAP_FAILURE
OLD_BASE_S1_PASS=NO
EXPECTED_BOOTSTRAP_FAILURE!=PASS
```

That expected failure is never waived, hidden, or renamed. The v5 bootstrap may merge only after its candidate exact-head Foundation/self-tests, every other applicable deterministic gate, applicable security accounting, independent exact-head review, finding reconciliation, final live race, and standing-founder bootstrap authority are all satisfied. After merge, **post-merge Foundation activation on canonical v5 main** must pass. The subsequent V2.3 canonicalization PR must then obtain a genuine trusted-base **v5** `s1-admission-integrity` PASS before it may merge, followed after merge by separate **post-merge V2.3 canonicalization activation** proof.

Acceptance of Spec 004 authorizes only execution of the governed bootstrap/canonicalization sequence described by the package under standing founder authorization. It does not itself make V2.3 canonical and does not grant source, dependency, donor-execution, runtime, model-provider, model-weight, inference, or future-slice implementation authority.

```text
SPEC_004_ACCEPTED != V2_3_CANONICAL
POLICY_BOOTSTRAP_MERGED != V2_3_CANONICAL
V2_3_CANONICAL != SOURCE_ADMISSION
V2_3_CANONICAL != PRODUCT_RUNTIME_AUTHORITY
GREEN_CI != ACCEPTANCE
REVIEW_CLEAN != COMPLETION_DECISION
```
