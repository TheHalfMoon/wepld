# Foundation Integrity Baseline

## Purpose

The fresh-foundation PR must not be able to change a canonical artifact and its expected digest in the same checked-out revision without crossing a separately governed evidence boundary.

## Immutable baseline identity

```text
BASELINE_BRANCH = governance/foundation-integrity-baseline-v1
BASELINE_COMMIT = 421c769b47fd8ad4f5bcba67ff8b00ba0adfc6c3
BASELINE_PATH = .wepld/foundation-integrity-baseline-v1.json
BASELINE_BLOB = a7c1423c95683f94479fb4a166ec73b3c35149ed
BASELINE_CLASS = BOOTSTRAP_INTEGRITY_EVIDENCE_NOT_ACCEPTANCE
```

The commit object is outside PR #2 and is addressed by exact SHA. The branch name is for discoverability; verification uses the immutable commit SHA, not the mutable branch tip.

Baseline contents establish:

```text
REPOSITORY_ID = 1334408699
BASE_MAIN_SHA = 7813dea9c53863378a5ae2fefcaf66f6b5d43103
CANONICAL_ARTIFACT_ARCHIVE_SHA256 = 35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0
MASTER_PLAN_V2_2_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
SOURCE_REGISTRY_ENTRIES = 402
SOURCE_ADMISSION = 0
```

## Bootstrap trust boundary

`foundation-integrity.yml` loads digest values from the exact baseline commit rather than from the PR revision being checked.

This removes the prior data-plane defect where changing the artifact and its hardcoded expected digest in the same PR was sufficient to satisfy the check.

The workflow definition itself is still reviewable code. A change to the pinned baseline commit/path, the baseline-fetch logic, or the comparison logic is security-sensitive and must be treated as a trust-boundary change by independent review. This bootstrap record does not claim that a workflow can cryptographically authenticate its own modified code.

After the foundation is accepted and a trusted required-check mechanism is established on canonical `main`, future PR integrity should be enforced from the trusted base/default-branch control plane rather than relying on a PR-authored bootstrap workflow.

## Authority invariants

```text
BASELINE_MATCH != FounderAcceptance
BASELINE_MATCH != SourceAdmission
BASELINE_MATCH != DependencyAdmission
BASELINE_MATCH != S1Authorization
BASELINE_MATCH != CompletionDecision
```
