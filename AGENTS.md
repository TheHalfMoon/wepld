# WePLD Agent Bootstrap

## Mandatory read order

Before planning, reviewing, implementing, or mutating WePLD:

1. `docs/canonical/CURRENT_STATE.md`
2. `docs/canonical/ARCHITECTURE_INVARIANTS.md`
3. `docs/canonical/BUILD_METHOD.md`
4. `docs/canonical/MASTER_PLAN_INDEX.md`
5. `docs/acquisition/SOURCE_REGISTRY_INDEX.md`
6. the active Spec Kit feature directory under `specs/`

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

## Non-bypassable invariants

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

## Mandatory build method

```text
SPEC_KIT_BUILD_METHOD = REQUIRED
PONYTAIL_MODE = FULL
SOURCE_ACQUISITION_CHECK = REQUIRED
DETERMINISTIC_GATES = REQUIRED
INDEPENDENT_REVIEW = REQUIRED
BUILD_LEARNING_CAPTURE = REQUIRED
```

Independent review producers when available and policy permits:
- CodeRabbit
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue

No reviewer is completion authority.

## Repository authority

```text
CANONICAL_REPOSITORY = TheHalfMoon/wepld
```

The connected account is the repository owner/admin. Never mutate repository or GitHub state outside current founder authorization.

## Fresh reconstitution

```text
FORMER_REPOSITORY = wepld/wepld
FORMER_TREE = HISTORICAL_QUARRY
FORMER_CODE = REJECT_UNLESS_EXPLICITLY_SALVAGED
FORMER_DOCS = NON_CANONICAL_UNLESS_EXPLICITLY_SALVAGED
LEGACY_DIRECTORY_COPY = NO
```
