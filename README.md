# WePLD

**Universal Engineering Intelligence System**

This repository is the clean reconstitution of WePLD. It does not build on the predecessor implementation tree.

## Start here

Any human or agent continuing WePLD must read:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/canonical/CURRENT_STATE.md`](docs/canonical/CURRENT_STATE.md)
3. [`docs/canonical/ARCHITECTURE_INVARIANTS.md`](docs/canonical/ARCHITECTURE_INVARIANTS.md)
4. [`docs/canonical/BUILD_METHOD.md`](docs/canonical/BUILD_METHOD.md)
5. [`docs/canonical/MASTER_ARCHITECTURE_EXECUTION_PLAN_V2_2.md`](docs/canonical/MASTER_ARCHITECTURE_EXECUTION_PLAN_V2_2.md)
6. [`docs/acquisition/MASTER_SOURCE_REGISTRY_V1.md`](docs/acquisition/MASTER_SOURCE_REGISTRY_V1.md)
7. the active package under [`specs/`](specs/)

## Build discipline

```text
SPEC_KIT_BUILD_METHOD = REQUIRED
PONYTAIL_MODE = FULL
SOURCE_ACQUISITION_CHECK = REQUIRED
DETERMINISTIC_GATES = REQUIRED
BUILD_LEARNING_CAPTURE = REQUIRED
```

Independent review producers are used when available and permitted:

- CodeRabbit
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue

Their output is review evidence only:

```text
ReviewOutcome != CompletionDecision
Reviewer finding != write authority
Green CI != completion
```

## Current scope

This foundation contains architecture, governance, acquisition records, build method, historical salvage evidence, and specifications only.

```text
IMPLEMENTATION = NOT_STARTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
B-WIN-001 = OPEN
```

The predecessor repository `wepld/wepld` remains a historical quarry. No old implementation is inherited merely because it exists.
