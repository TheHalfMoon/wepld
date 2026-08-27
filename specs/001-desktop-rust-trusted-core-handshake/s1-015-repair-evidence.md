# S1-015 — Bounded repair and rerun evidence

```text
STATUS = S1_015_CLOSEOUT_EVIDENCE
DATE = 2026-08-27
FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE

S1_014_ACCEPTANCE_CANDIDATE = 58ad0d166b6177ae69d04ff59da17aa8cc0e3c28
REPAIR_BASE = fd5afdbd6cc034a1623feb2e2c94b34468cab06c
REPAIR_PR = #197
REPAIR_HEAD = 1229bdd9a411c70cce5494185c1f6c7814fa2085
REPAIR_HEAD_TREE = 063a5bef4d053636efd486cb5f5d50ac886b984b
REPAIR_CHANGED_FILES = 1_EXACT
REPAIR_PATH = .github/workflows/s1-performance.yml
REPAIR_MERGE = 9ae784106f36c2234e3cdf6befdb03449a224c34
REPAIR_MERGE_TREE = 063a5bef4d053636efd486cb5f5d50ac886b984b

PRE_REPAIR_WORKFLOW_SHA256 = 7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784
PRE_REPAIR_WORKFLOW_GIT_BLOB = b16d57b42e617808d4b5d2547c1677e9ef7c3535
REPAIRED_WORKFLOW_SHA256 = 6c0b8cb346730a6865a6a2e5b9af2dbccb788c572fa6d36d36860814cabd008e
REPAIRED_WORKFLOW_GIT_BLOB = 3ccd118aea80fd31866973371babc329913aafb8

EXACT_HEAD_FOUNDATION = 33068200273 / #737 / SUCCESS
EXACT_HEAD_TRUSTED_ADMISSION_INITIAL = 33068200340 / #575 / SUCCESS
EXACT_HEAD_TRUSTED_ADMISSION_FINAL = 33069378037 / #576 / SUCCESS
EXACT_HEAD_PERFORMANCE = 33068200332 / #7 / SUCCESS
EXACT_HEAD_QODO_REVIEW = issuecomment-5438445407 / 0_BUGS / 0_RULE_VIOLATIONS / 0_REQUIREMENT_GAPS
CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
SECURITY_PASS = NO
CODERABBIT = NOT_COUNTED_AS_REVIEW

POST_MERGE_FOUNDATION = 33069506354 / #738 / SUCCESS
POST_MERGE_PERFORMANCE = 33069506387 / #8 / SUCCESS
POST_MERGE_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34

UNRESOLVED_MATERIAL_FINDINGS = 0
STALE_EVIDENCE_INHERITANCE = 0
S1_015_CLOSEOUT_AUTHORITY = REQUIRES_CANONICAL_V17_SUCCESSOR_POLICY
S1_016_AUTHORITY = NOT_GRANTED_BY_THIS_EVIDENCE
S1_ACCEPTED = NO
```

## Finding reconciliation

S1-014 normalized one valid material finding: the `s1-performance` workflow
path filters did not cover every measured build input. PR #197 changed only
`.github/workflows/s1-performance.yml`, adding the missing measured build-input
paths to both pull-request and push trigger filters. No product source,
dependency, runtime, model/provider, or later-slice authority was added.

## Exact-head qualification

The exact repair head `1229bdd9a411c70cce5494185c1f6c7814fa2085`
passed Foundation, trusted-base admission, and the S1 performance workflow. The
final trusted-base admission rerun also passed on the same exact head. Qodo
reviewed that exact head and reported zero bugs, zero rule violations, and zero
requirement gaps. CodeRabbit did not provide counted review evidence. Codex
Security remained unavailable for this bounded repair and is recorded as
`NOT_RUN_NON_BLOCKING`, never PASS.

## Canonical activation

PR #197 merged as `9ae784106f36c2234e3cdf6befdb03449a224c34`.
On that exact canonical merge commit, post-merge Foundation #738 and
`s1-performance` #8 both succeeded. The post-merge performance run is the
activation proof that the repaired path filters trigger and execute on the
canonical measured build-input tree.

## Closeout boundary

This evidence counts as S1-015 closeout evidence only after the exact
two-file ledger/evidence transition is admitted and merged under the separately
qualified v17 successor policy. It does not authorize S1-016, S1 acceptance,
Build Learning mutation, S2, roadmap mutation, provider/model execution, source
admission, dependency expansion, or product-runtime expansion.
