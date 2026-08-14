# Build Learning Protocol

## Objective

While WePLD uses external engineering tools, reviewers, agents, IDEs, CLIs, MCP servers, plugins, SDKs, and OSS donors, WePLD must learn from their actual behavior.

This is controlled product learning, not automatic architecture mutation.

## Observation classes

```text
POSITIVE_MECHANISM
NEGATIVE_ORACLE
TEST_QUARRY
UX_ORACLE
CONTEXT_ORACLE
ROUTING_ORACLE
RECOVERY_ORACLE
PERMISSION_ORACLE
PERFORMANCE_EVIDENCE
INTEROPERABILITY_EVIDENCE
NO_REUSABLE_LEARNING
```

## Required record

For every material observation:

```text
LEARNING_ID
DATE
TOOL_OR_SOURCE
EXACT_VERSION_OR_PIN
TASK_OR_REVIEW_CONTEXT
OBSERVED_BEHAVIOR
EVIDENCE_REFERENCE
OBSERVATION_CLASS
WHAT_WORKED_OR_FAILED
WEPLD_OWNER_CANDIDATE
REUSABLE_MECHANISM_CANDIDATE
NEGATIVE_TEST_CANDIDATE
SECURITY_OR_AUTHORITY_IMPACT
PONYTAIL_VALUE
CONFIDENCE
CONFLICTS
STATUS
```

## Status lifecycle

```text
OBSERVED
-> CORROBORATED
-> CANDIDATE
-> QUALIFIED / REJECTED
-> INCORPORATED
```

Only `QUALIFIED` material may be incorporated into canonical contracts/tests/skills, and incorporation still follows normal founder/architecture/source admission boundaries.

## Special rule for reviewers

A reviewer may teach WePLD about review quality, context selection, finding structure, false positives, repair loops, or UX.

Reviewer behavior **must never** teach WePLD that reviewer approval is completion authority.

## Special rule for builders/agents

Observe:
- planning/decomposition;
- context loading;
- tool routing;
- permission prompts;
- retries/fallbacks;
- sandbox/egress assumptions;
- session persistence;
- worktree behavior;
- parallelism;
- generated tests;
- failure representation.

Explicitly record silent fallback, fabricated success/quality, overbroad permissions, or context/authority conflation as negative oracles.

## Byan future mapping

When S10 exists, this ledger becomes one governed input family to Byan. Byan may propose SkillCandidate, RouteCandidate, ContextPolicyCandidate, ReviewerPolicyCandidate, or benchmark cases. Byan never authorizes adoption.
