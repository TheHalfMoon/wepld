# Codex Security — Bounded Source / Behavior Enrichment

## Classification

```text
FAMILY = OpenAI Codex
CAPABILITY = Codex Security
CLASS = SECURITY_REVIEW_BEHAVIOR_ORACLE + OPTIONAL_EXTERNAL_REVIEWER
NAMED_SOURCE_REGISTRY_CHANGE = 0
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

Codex Security enriches the existing OpenAI Codex family; it is not a new top-level WePLD source-registry entry.

## WePLD mapping

```text
PRIMARY_OWNER_CANDIDATE = AMAN
INDEPENDENT_EVALUATION_INTERFACE = Assurance
EFFECT_AUTHORITY = Nawat only
REPAIR_AUTHORITY = separate authorized Attempt only
COMPLETION_AUTHORITY = Trusted Completion / applicable founder boundary only
```

Useful behavior to evaluate when the service is available and repository-egress policy permits:

- repository-specific security/threat-model review;
- vulnerability-candidate generation;
- exploitability/validation evidence;
- security-context selection across code/history;
- targeted patch suggestions for human/governed review;
- false-positive and false-negative behavior;
- security test / reproduction quality.

## Admission and versioning

Codex Security is a hosted/research-preview product surface rather than an admitted WePLD runtime dependency in this foundation.

At each actual use, record the then-current official OpenAI product/version/reference and review any material changes before treating prior evaluation evidence as current.

```text
CURRENT_RUNTIME_ADMISSION = NONE
IMMUTABLE_SERVICE_PIN = NOT_ESTABLISHED
USE_TIME_OFFICIAL_REFERENCE_RECHECK = REQUIRED
```

## Negative authority oracles

```text
SECURITY_REVIEW_RESULT != COMPLETION_DECISION
THREAT_MODEL != AUTHORITY_GRANT
VULNERABILITY_FINDING != WRITE_AUTHORITY
PATCH_SUGGESTION != AUTHORIZED_REPAIR
SERVICE_AVAILABLE != EGRESS_AUTHORIZED
SERVICE_UNAVAILABLE = NOT_RUN_NON_BLOCKING
NOT_RUN != SECURITY_COVERAGE_PASS
```

## Related canonical policy

See `docs/canonical/CODEX_SECURITY_REVIEW_POLICY.md`.
