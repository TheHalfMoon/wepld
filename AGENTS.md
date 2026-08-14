# WePLD Agent Bootstrap

This repository is the canonical project-memory surface for WePLD after fresh reconstitution.

## Mandatory read order

Before planning, reviewing, implementing, or mutating WePLD:

1. `docs/canonical/CURRENT_STATE.md`
2. `docs/canonical/ARCHITECTURE_INVARIANTS.md`
3. `docs/canonical/BUILD_METHOD.md`
4. `docs/canonical/MASTER_ARCHITECTURE_EXECUTION_PLAN_V2_2.md`
5. `docs/acquisition/MASTER_SOURCE_REGISTRY_V1.md`
6. the active Spec Kit feature directory under `specs/`

Historical files or Git history are evidence quarries only unless a canonical file explicitly incorporates them.

## Product thesis

```text
WePLD = Universal Engineering Intelligence System
Desktop-first / Windows-first initial execution
Rust-first trusted logic
Local-authoritative / cloud-independent / air-gap-capable
Any model / worker / tool / skill behind one governed engineering truth
Project Brain is durable; models are replaceable
Acquire solved software before generating equivalents
```

## Non-bypassable architecture invariants

```text
ReviewOutcome != CompletionDecision
Context != Authority
Provenance != Authority
Model/tool/worker selection != Authorization
Green CI != Completion
Merge/Deploy/Publish != Completion
Reviewer finding != Write Authority
Builder != Acceptance Authority for acceptance-critical work
Missing evaluator/context/coverage/containment evidence != PASS
No silent provider/model/worker substitution
```

## Build method

```text
SPEC_KIT_BUILD_METHOD = REQUIRED
PONYTAIL_MODE = FULL
SOURCE_ACQUISITION_CHECK = REQUIRED_BEFORE_BUILDING_SOLVED_MACHINERY
DETERMINISTIC_GATES = REQUIRED
INDEPENDENT_REVIEW = REQUIRED
BUILD_LEARNING_CAPTURE = REQUIRED
```

Default independent review producers when available and permitted:

- CodeRabbit
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue AI checks / CLI as an additional independent check surface

No reviewer is completion authority.

## Build-learning rule

When using a builder, reviewer, CLI, IDE agent, MCP, plugin, or source donor:

1. use it for the current engineering task;
2. observe what mechanism actually helped or failed;
3. record only evidence-backed lessons in `docs/learning/BUILD_LEARNING_LEDGER.md`;
4. classify the lesson as `POSITIVE_MECHANISM`, `NEGATIVE_ORACLE`, `TEST_QUARRY`, `UX_ORACLE`, `PERFORMANCE_EVIDENCE`, or `NO_REUSABLE_LEARNING`;
5. never promote a lesson directly into architecture, policy, skill, dependency, or authority;
6. later qualification may turn a lesson into a source-acquisition record, test, SkillCandidate, RouteCandidate, or Byan learning candidate.

## Mutation safety

This repository is the founder-selected fresh WePLD target and the connected GitHub account is verified as owner/admin.

Never mutate GitHub or repository state unless the current founder authorization explicitly permits the exact mutation.

## Fresh-reconstitution rule

```text
OLD_TREE = HISTORICAL_QUARRY
OLD_CODE = REJECT_UNLESS_EXPLICITLY_SALVAGED
OLD_DOC = NON_CANONICAL_UNLESS_EXPLICITLY_SALVAGED
GIT_HISTORY = PRESERVE
NEW_FOUNDATION = RATIFIED_V2_2_ONLY
```
