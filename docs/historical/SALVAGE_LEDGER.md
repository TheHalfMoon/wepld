# Former-Repository Salvage Ledger

## Rule

```text
OLD_PATH_EXISTS != KEEP
KEEP_AS_IS | COPY_AND_REWRITE | CONCEPT_ONLY | TEST_ORACLE_ONLY | HISTORICAL_REFERENCE | REJECT
```

High-value former-repo candidates:

- governance dependency/provenance disciplines -> `COPY_AND_REWRITE`;
- governed specification workflow authority separation -> `CONCEPT_ONLY`;
- PR #11 human control/no-silent-routing/lifecycle/GitHub boundary concepts -> `CONCEPT_ONLY`;
- PR #1 validation/workspace/ledger/provider tests -> `TEST_ORACLE_ONLY` or `CONCEPT_ONLY`;
- PR #1 Hermes runtime and old architecture -> runtime `REJECT`, tests/failure corpus `TEST_ORACLE_ONLY`;
- PR #1 golden/adversarial/governance/integrity/lifecycle tests -> `TEST_ORACLE_ONLY`;
- old dependency set -> `REJECT_BY_DEFAULT`, re-admit only per capability gate.

Any later code salvage requires exact old path/blob/commit/test paths/rights/security/platform limits/new owner/rewrite delta/negative tests/admission decision.
