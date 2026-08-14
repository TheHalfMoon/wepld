# Build Learning Protocol

While building WePLD, external builders, reviewers, CLIs, IDE agents, MCPs, plugins, SDKs, and OSS donors are also observable engineering systems.

Observation classes:

```text
POSITIVE_MECHANISM
NEGATIVE_ORACLE
TEST_QUARRY
UX_ORACLE
CONTEXT_ORACLE
ROUTING_ORACLE
RECOVERY_ORACLE
PERMISSION_ORACLE
MAINTENANCE_EVIDENCE
PERFORMANCE_EVIDENCE
INTEROPERABILITY_EVIDENCE
NO_REUSABLE_LEARNING
```

Every learning record must carry a stable evidence reference such as an exact repository revision/path, canonical artifact, source-registry record, review/run identifier, or other durable evidence anchor.

Lifecycle:

```text
UNVERIFIED -> OBSERVED -> CORROBORATED -> CANDIDATE
CANDIDATE -> QUALIFIED -> INCORPORATED
CANDIDATE -> REJECTED
```

`UNVERIFIED` means a potentially useful lesson has been noted but lacks sufficient stable evidence to count as an observation. `REJECTED` is terminal unless a new, separately evidenced candidate is created.

Only qualified material may enter canonical contracts/tests/skills, and normal authority/source-admission rules still apply. Byan may later consume this ledger but never authorizes adoption.
