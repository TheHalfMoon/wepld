# Greptile Official Behavior Evidence — 2026-08-15

## Purpose

This is a bounded provenance snapshot for claims used by `docs/acquisition/GREPTILE_ENRICHMENT.md`. It preserves only the minimum normalized evidence needed to make those claims auditable. It is not source admission, dependency admission, hosted-service approval, or a mirror of Greptile proprietary implementation.

```text
EVIDENCE_CLASS = OFFICIAL_PUBLIC_DOCUMENTATION_SNAPSHOT
RETRIEVAL_DATE = 2026-08-15 Asia/Riyadh
OFFICIAL_DOC_INDEX = https://www.greptile.com/docs/llms.txt
SNAPSHOT_FORM = normalized bounded evidence capsules
HASH_METHOD = SHA-256 over the exact UTF-8 three-line capsule shown for each evidence ID, with LF separators and no trailing newline
RAW_HOSTED_CORE_SOURCE = NOT_ESTABLISHED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
HOSTED_REVIEW_EGRESS_APPROVAL = NONE
```

The evidence capsules below are deliberately normalized rather than copied wholesale from vendor documentation. The official URL remains the authority for what Greptile currently documents; the capsule digest makes the exact claim used by WePLD stable and independently re-hashable.

## GREP-E1 — graph-based codebase context

Official page: `https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents a repository codebase graph spanning code elements and relationships and uses it for context-aware review beyond isolated diff text.
```

```text
CAPSULE_SHA256 = e1467d37d86e41a0a62db380d20b52638b362d2eb6737d8c71ee2e8c813eadde
```

## GREP-E2 — cascading `.greptile/` configuration and context files

Official page: `https://www.greptile.com/docs/code-review/greptile-config`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/code-review/greptile-config
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents directory-scoped .greptile configuration with root-to-leaf cascading inheritance, structured config, prose rules, and explicit context files.
```

```text
CAPSULE_SHA256 = 5d1d05f1b4cde8308f036f05800b5851b99cf2b721263d3155f32f158eac3830
```

## GREP-E3 — cross-repository context

Official page: `https://www.greptile.com/docs/code-review/greptile-config-reference`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/code-review/greptile-config-reference
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents cross-repository review context through context.repos entries naming related repositories accessible with the same credentials.
```

```text
CAPSULE_SHA256 = 073e2e59be95e48a7d91889bf517d7fd8f964e094f7f99753b610bad0c3269f9
```

## GREP-E4 — memory and learning from review feedback

Official page: `https://www.greptile.com/docs/how-greptile-works/memory-and-learning`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/how-greptile-works/memory-and-learning
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents learning from team review comments, replies, reactions, commit analysis, and repeated patterns to adapt review suggestions.
```

```text
CAPSULE_SHA256 = 1b18db7b32e1bd6b4656299d1a0da08e36934af9baa7dadc7ea0c3bff892c9f3
```

## GREP-E5 — review behavior surface

Official page: `https://www.greptile.com/docs/code-review/key-features`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/code-review/key-features
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents full-codebase-context review, high-signal findings, team learning, conversational follow-up, and agent-assisted fixes.
```

```text
CAPSULE_SHA256 = 4b27ff4f0f0dcf370b6fdc1ab427bc234dea3bd003b88f4e3b86ce73b67d6e02
```

## GREP-E6 — source-branch repository configuration

Official page: `https://www.greptile.com/docs/code-review/greptile-json-reference`

Canonical capsule:

```text
SOURCE_URL=https://www.greptile.com/docs/code-review/greptile-json-reference
RETRIEVED_AT=2026-08-15T02:21:00+03:00
CLAIM=Greptile documents that repository-level greptile.json settings are read from the pull request source branch and override dashboard settings.
```

```text
CAPSULE_SHA256 = 0030949045a956e1ee5f73cbbd5d21fa1bdf2df7215bb7224a09e63d99fcca33
```

## Evidence limits

- These capsules attest only to public behavior documented at retrieval time.
- They do not establish an immutable Greptile hosted-core revision.
- Hosted behavior remains mutable and requires use-time compatibility recheck.
- Cross-repository context being documented does not authorize WePLD to expose any repository.
- Learned behavior, reviewer output, graph relevance, or suggested fixes do not become canonical truth, authority, or completion evidence by themselves.
