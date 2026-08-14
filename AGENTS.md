# WePLD Agent Bootstrap

## Mandatory read order

Before planning, reviewing, implementing, or mutating WePLD:

1. `docs/canonical/CURRENT_STATE.md`
2. `docs/canonical/ARCHITECTURE_INVARIANTS.md`
3. `docs/canonical/BUILD_METHOD.md`
4. `docs/canonical/SECURITY_REVIEW_POLICY.md`
5. `docs/canonical/MASTER_PLAN_INDEX.md`
6. `docs/acquisition/SOURCE_REGISTRY_INDEX.md`
7. the active Spec Kit feature directory under `specs/`

On every new chat or agent session, treat this repository read order as the durable bootstrap. Repository canonical memory outranks chat memory. Verify live PR/check/review state before any mutation.

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

Correctness / engineering review producers, when connected and policy/egress permits:
- CodeRabbit
- Greptile
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue

Security-specific reviewer:
- Codex Security for security-sensitive changes when available and policy/egress permits.

At least one independently qualified correctness/engineering review is required before acceptance of material work. If no qualified independent reviewer can run, record `REVIEW_BLOCKED`; do not convert unavailability into PASS. Any exception requires explicit authorization, a named qualified substitute, and a residual-limitation record.

No reviewer is completion authority. Codex Security supplements deterministic security gates and never replaces them.

While building, learn from the reviewers/builders/tools: record evidence-backed mechanics, tests, failure modes, context strategies, permission patterns, routing, recovery, and negative oracles through the canonical Build Learning protocol. Learned behavior is a candidate, never authority.

## Repository authority

```text
CANONICAL_REPOSITORY = TheHalfMoon/wepld
AUTHORITY_EVIDENCE = docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md
```

Treat repository/session authority as point-in-time evidence. Reverify live permissions before privileged mutation. Never mutate repository or GitHub state outside current founder authorization.

## Fresh reconstitution

```text
FORMER_REPOSITORY = wepld/wepld
FORMER_TREE = HISTORICAL_QUARRY
FORMER_CODE = REJECT_UNLESS_EXPLICITLY_SALVAGED
FORMER_DOCS = NON_CANONICAL_UNLESS_EXPLICITLY_SALVAGED
LEGACY_DIRECTORY_COPY = NO
```

## Communication

```text
DISCUSSION_LANGUAGE = Arabic
READY_TO_USE_TECHNICAL_PROMPTS = English
```
