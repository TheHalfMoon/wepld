# Codex Security Review Policy

## Status

```text
CODEX_SECURITY = OPTIONAL_SECURITY_REVIEWER
AVAILABILITY_GATE = NON_BLOCKING
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
AUTHORITY_GRANT = NONE
```

Codex Security is an additional security-specialist review producer for WePLD. It does not replace the normal correctness reviewer mesh, deterministic security gates, source-acquisition review, Ponytail, AMAN evidence, Nawat authorization, or Trusted Completion.

## Intended use

When available and repository-egress policy permits, Codex Security may provide security-focused evidence such as repository-specific threat-model observations, vulnerability candidates, exploitability/validation evidence, and targeted patch suggestions.

Its output enters the same governed reconciliation path as any other reviewer output:

```text
Codex Security output
-> SecurityFindingCandidate
-> evidence / reproduction / scope validation
-> Finding Reconciliation
-> accepted finding or rejected finding
-> separately authorized repair Attempt when required
-> deterministic gates again
-> security re-review when material
-> normal acceptance boundary
```

## Non-bypassable rules

```text
Codex Security clean != CompletionDecision
Codex Security finding != Write Authority
Codex Security patch suggestion != Authorized Repair
Codex Security unavailable = NOT_RUN_NON_BLOCKING
Codex Security not run != Deterministic Security Coverage Passed
Codex Security threat model != AMAN Risk Decision
Codex Security validation != Nawat Authorization
```

A valid finding from Codex Security is not erased by clean output from CodeRabbit, Qodo, Augment Code, Graphite, Cubic, Continue, or another reviewer. Likewise, a clean Codex Security result does not erase a valid correctness, architecture, provenance, or safety finding from another producer.

## Egress and trust

Codex Security is an external review surface. Before use on material that is not approved for external processing, AMAN/Nawat policy must determine whether repository content, diff content, history, logs, artifacts, or secrets may leave the local boundary.

Never send credentials, secrets, private customer data, PHI, or unauthorized third-party source merely because the reviewer is available.

## Build-method position

Codex Security is **additional**, not a replacement step:

```text
Spec Kit
-> Ponytail FULL
-> Source Acquisition Check
-> Implementation
-> Deterministic Gates
   -> deterministic security gates where applicable
-> Correctness / engineering reviewer mesh
   -> CodeRabbit / Qodo / Augment Code / Graphite / Cubic / Continue
-> Optional security-specialist review
   -> Codex Security when available and policy permits
-> Finding Reconciliation
-> Bounded Repair
-> Re-run Gates
-> Re-review Material Changes
-> Authorized Acceptance
-> Build Learning Capture
```

## Build Learning

When Codex Security is used, record evidence-backed lessons about threat-model quality, repository-context selection, false positives, validation quality, security test generation, patch quality, and failure modes in the Build Learning Ledger.

Learned behavior is a candidate only. It does not silently become architecture, policy, a security rule, a source admission, a skill, or authority.

## Acquisition classification

```text
FAMILY = OpenAI Codex
ENRICHMENT = Codex Security
ROLE = SECURITY_REVIEW_BEHAVIOR_ORACLE + OPTIONAL_EXTERNAL_REVIEWER
WEPLD_OWNER_CANDIDATES = AMAN + Assurance
NAMED_SOURCE_COUNT_CHANGE = 0
ROADMAP_CHANGE = NONE
```
