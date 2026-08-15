# Source Registry Index

```text
FROZEN_V1_5_NAMED_ENTRIES = 397
POST_V1_5_NEW_TOP_LEVEL_ENTRIES = 5
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
BROAD_DISCOVERY = CLOSED
SOURCE_ADMISSION = NONE
PATH_LEVEL_MINING = CAPABILITY_TRIGGERED
```

Post-V1.5 top-level additions represented in frozen registry V1: Devin, Fern, DeepSeek Harness, Cordis, CommandCode.

Recent bounded enrichments include Kilo/Kiro, Goose, Zed, Greptile, Cubic, Graphite, Augment, Qodo, Devin, Eigent/CAMEL, Fern, Cohere, DeepSeek Harness/Cordis, CommandCode, Continue, and DeerFlow.

## Existing registry V1 source enriched after restoration

DeerFlow is already represented in frozen registry V1:

```text
SRC-0364 = DeerFlow
bytedance/deer-flow@1dd6ba1acb03700589994b0366c5d1c7d05e2eff
STATUS = BOUNDED_ENRICHMENT / PATH_MINING EVIDENCE
SOURCE_ADMISSION = NONE
```

This enrichment does **not** add a named registry entry.

## Post-registry-V1 candidates

The following sources were identified after the 402-entry registry V1 restoration was frozen:

```text
HKUDS/DeepCode@287510fbf6820147a48adf79f7fd86b0ed1afe92
STATUS = POST_V1_CANDIDATE_PENDING_NEXT_REGISTRY_REVISION
SOURCE_ADMISSION = NONE

wrtnlabs/agentica@dc91f4307a3f2ee25e1ee07cf48777fcd13b6b0d
STATUS = POST_V1_CANDIDATE_PENDING_NEXT_REGISTRY_REVISION
SOURCE_ADMISSION = NONE

deer-flow/llm-space@be629ddd58c6a9f5f011687580a1858652f12925
STATUS = POST_V1_CANDIDATE_PENDING_NEXT_REGISTRY_REVISION
SOURCE_ADMISSION = NONE
```

These candidates do **not** change `CURRENT_ACCOUNTED_NAMED_ENTRIES = 402` for registry V1, the canonical archive, or its immutable foundation baseline. A future source-registry revision must reconcile post-V1 candidates explicitly rather than silently rewriting restoration evidence.

Current Continue anchor:

```text
continuedev/continue@5522c6f44ca0ac3528b37244818fbfa39b5af470
LICENSE = Apache-2.0
ROLE = SOURCE_DONOR + BEHAVIOR_ORACLE + BUILD_TOOL_CANDIDATE
```

Current Greptile public-edge anchor:

```text
greptileai/greptile-vscode@72fc0c5a68ff966e64c2b182a2e6bf5912410821
LICENSE = MIT
ROLE = PUBLIC_EDGE + REVIEW_BEHAVIOR_ORACLE
HOSTED_CORE_SOURCE = NOT_ESTABLISHED
```

See:
- `docs/acquisition/GREPTILE_ENRICHMENT.md`
- `docs/acquisition/DEEPCODE_ENRICHMENT.md`
- `docs/acquisition/DEERFLOW_ENRICHMENT.md`
- `docs/acquisition/AGENTICA_ENRICHMENT.md`
- `docs/acquisition/LLM_SPACE_ENRICHMENT.md`

The full registry remains a 402-entry acquisition artifact; this index is the canonical lightweight restoration point until a separately governed next registry revision is authorized.
