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

## Repository-content / egress controls

Any hosted Codex Security evaluation is governed by `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` before repository content leaves the trusted local/repository boundary.

The evaluation is available only after that policy establishes:

- exact allowed file scope;
- content classification and explicit egress authorization;
- required secret/private-data screening and redaction;
- applicable provider retention and training-use decision;
- tenant-isolation/access-control decision for non-public content;
- any required deletion, residency, contractual, or subprocessor constraints.

Unknown required data-handling facts block non-public egress. Service availability alone never authorizes repository upload.

## Admission, service identity, and evaluation validity

Codex Security is a hosted/research-preview product surface rather than an admitted WePLD runtime dependency in this foundation.

```text
CURRENT_RUNTIME_ADMISSION = NONE
IMMUTABLE_SERVICE_PIN = NOT_ESTABLISHED
USE_TIME_OFFICIAL_REFERENCE_RECHECK = REQUIRED
```

Because an immutable service pin is not established, every actual evaluation record must capture:

```text
PROVIDER = OpenAI
PRODUCT / SURFACE = exact official Codex Security product surface used
OFFICIAL_REFERENCE = exact current official OpenAI reference used to identify the service
VERSION / BUILD = exact value when exposed; otherwise UNVERSIONED_HOSTED_SERVICE
EVALUATION_DATE
BASE_SHA / HEAD_SHA or immutable patch identity
FILE_SCOPE
EGRESS_CLASSIFICATION / APPROVAL
COMPATIBILITY_DECISION = CURRENT | STALE | INCOMPATIBLE
MATERIAL_SERVICE_DIFFERENCES
RESULT / COVERAGE_LIMITATIONS
```

Prior evaluation evidence may be reused only after a new use-time official-reference check confirms the same provider/product identity and records a `CURRENT` compatibility decision for the intended scope. A material provider/product/model/worker behavior change makes the old evidence `STALE` until re-evaluated.

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

See:
- `docs/canonical/SECURITY_REVIEW_POLICY.md`
- `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`
