# Acceptance — Spec 003 Planning Candidate

Spec 003 is accepted as a **planning candidate** only when:

- all planning artifacts are present and mutually consistent;
- V2.2 is still explicitly canonical in candidate text;
- no implementation/dependency/source/runtime authorization is introduced;
- active Pictorial/Agile PRs remain outside the change;
- frozen registry count remains untouched;
- Tier-1 source pins are research anchors only;
- the planning PR does not mutate base-controlled canonical authority files; `docs/canonical/MASTER_PLAN_INDEX.md` remains byte-identical to the trusted base in this planning change;
- both the Foundation exact-head check and trusted-base `s1-admission-integrity` exact-head check pass for the same candidate head and are recorded in immutable PR/check evidence;
- when an external reviewer is used, a recorded exact-head `EGRESS_PREFLIGHT` exists **before** the review trigger and covers scope classification, secret/private-data screening, provider handling/retention/training/tenant-isolation decisions, `EGRESS_APPROVAL`, and result limitations under `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`;
- at least one independently qualified engineering reviewer reviews the exact head; if a required qualified review is unavailable, record `REVIEW_BLOCKED` and stop qualification/canonicalization rather than treating absence as PASS;
- all material findings are reconciled on the exact reviewed head or a repaired successor head that is fully requalified;
- a final live-evidence race re-reads current GitHub PR, base, head, changed-file, both deterministic check results, and review state and records the exact values compared.

Merging this planning package, if separately qualified, may only persist a **non-canonical V2.3 candidate**. Canonicalization of V2.3 requires a separately governed bootstrap/override event for the base-controlled canonical index. Source admission and implementation remain separate effects.

```text
GREEN_CI != ACCEPTANCE
FOUNDATION_PASS_ALONE != ACCEPTANCE
PLANNING_ACCEPTANCE != IMPLEMENTATION_AUTHORITY
PLANNING_PR_MERGE != V2_3_CANONICALIZATION
V2_3_CANDIDATE != CANONICAL_V2_3
REVIEW_UNAVAILABLE = REVIEW_BLOCKED
```
