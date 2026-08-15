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

## Lifecycle

```text
UNVERIFIED -> OBSERVED -> CORROBORATED -> CANDIDATE
CANDIDATE -> QUALIFIED -> INCORPORATED
CANDIDATE -> REJECTED
```

`REJECTED` is terminal unless a new, separately evidenced candidate is created.

## Deterministic transition gates

### `UNVERIFIED -> OBSERVED`

Requires:
- at least one stable evidence reference;
- a bounded factual observation that the evidence directly supports;
- tool/source identity sufficient to distinguish the observed system or revision;
- unresolved uncertainty recorded rather than omitted.

### `OBSERVED -> CORROBORATED`

Requires at least one of:
- a second independent evidence source supporting the same mechanism/failure; or
- deterministic reproduction against the same pinned source/tool identity.

Contradictory evidence blocks promotion while the conflict remains unresolved. Recording or retaining the conflict for audit does not satisfy this gate; promotion requires resolution with supporting evidence.

### `CORROBORATED -> CANDIDATE`

Requires:
- a named WePLD owner/capability destination candidate;
- an explicit proposed use such as test, negative oracle, behavior, skill, route, context policy, or acquisition decision;
- no unresolved conflict with a canonical architecture/authority invariant;
- known material limitations recorded.

### `CANDIDATE -> QUALIFIED`

Requires the evidence appropriate to the candidate class, including as applicable:
- exact scope/version/pin and provenance;
- source rights/admission evidence when reuse is proposed;
- deterministic tests, benchmark, or reproduction evidence;
- security/egress review where applicable;
- independent review of the qualification claim;
- explicit authorized acceptance of the qualification decision.

Missing applicable evidence blocks qualification.

### `CANDIDATE -> REJECTED`

Requires:
- explicit rejection reason;
- evidence supporting the rejection or incompatibility;
- decision record identifying the rejected scope/version/candidate;
- explicit authorized acceptance of the rejection decision when the record is canonical.

### `QUALIFIED -> INCORPORATED`

Requires a separate reviewed and authorized repository/product change naming the destination owner, retained evidence, tests/policy updates, and any required source/dependency admission. `QUALIFIED` alone never self-incorporates.

## Authorized status writer

Tools, models, reviewers, workers, and Byan may **propose** status transitions but may not mutate canonical learning status merely because they produced the evidence.

Before native Nawat/Byan authority exists, a canonical `Status` change requires:

```text
CURRENT_FOUNDER_AUTHORIZED_REPOSITORY_WRITE
+ TRANSITION_GATE_EVIDENCE
+ APPLICABLE_INDEPENDENT_REVIEW
```

For `QUALIFIED`, `REJECTED`, or `INCORPORATED`, the applicable explicit acceptance/authority boundary must also be recorded.

After Nawat exists, an exact Nawat grant is additive to, and never a replacement for, every applicable transition gate, recorded acceptance requirement, and `CURRENT_FOUNDER_AUTHORIZED_REPOSITORY_WRITE`. The grant authorizes the status mutation only after those prerequisites are satisfied. Byan remains a learning/proposal producer and does not mint that grant.

Only qualified material may enter canonical contracts/tests/skills, and normal authority/source-admission rules still apply.