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

Recent bounded enrichments include Kilo/Kiro, Goose, Zed, Greptile, Cubic, Graphite, Augment, Qodo, Devin, Eigent/CAMEL, Fern, Cohere, DeepSeek Harness/Cordis, CommandCode, and Continue.

## Post-registry-V1 candidates

DeepCode was identified after the 402-entry registry V1 restoration was frozen:

```text
HKUDS/DeepCode@287510fbf6820147a48adf79f7fd86b0ed1afe92
STATUS = POST_V1_CANDIDATE_PENDING_NEXT_REGISTRY_REVISION
SOURCE_ADMISSION = NONE
```

This does **not** change `CURRENT_ACCOUNTED_NAMED_ENTRIES = 402` for registry V1, the canonical archive, or its immutable foundation baseline. A future source-registry revision must reconcile the new candidate explicitly rather than silently rewriting restoration evidence.

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

The full registry remains a 402-entry acquisition artifact; this index is the canonical lightweight restoration point until a separately governed next registry revision is authorized.