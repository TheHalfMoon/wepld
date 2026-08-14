# WePLD Security Review Policy

## Purpose

Codex Security is an additional security-specialist review producer for WePLD. It is not completion authority and does not replace deterministic security gates, correctness review, Ponytail, AMAN/Nawat governance, or Trusted Completion.

## Applicability

Run a Codex Security diff scan when available and egress policy permits for material changes involving any of:

- source/runtime behavior;
- Nawat authority or effect grants;
- Mission Runtime execution;
- UWC tool/process boundaries;
- filesystem/process/network/IPC effects;
- sandbox/containment behavior;
- parsers or untrusted external input;
- credentials, secrets, tokens, signing, provenance, or identity;
- dependency execution or supply-chain surfaces;
- CI/workflow trust boundaries;
- serialization/deserialization or protocol boundaries;
- security-sensitive recovery or rollback.

Documentation-only changes with no executable/security-boundary effect may be `NOT_APPLICABLE`. Workflow/configuration changes are not automatically documentation-only; evaluate their actual effects.

## Exact scan identity

For PR review, bind the scan to the exact immutable range:

```text
BASE_SHA
HEAD_SHA
CHANGED_FILE_SET
```

Do not silently continue a security conclusion after the reviewed head changes. Material repair requires re-scan of the new range or explicit coverage accounting.

## Required security-scan method

When Codex Security is used:

1. resolve and freeze the exact diff;
2. apply repository security guidance;
3. produce/adopt one threat model;
4. review every changed source file, including deleted files at baseline;
5. perform candidate finding discovery;
6. validate candidates;
7. perform attack-path analysis for reportable/deferred candidates;
8. record findings and coverage gaps;
9. preserve the report/SARIF or equivalent durable evidence when the host supports it.

## Status vocabulary

```text
PASS = completed applicable scan with no validated reportable finding and accounted coverage
FAIL = validated reportable security finding blocks the applicable gate
DEFERRED = unresolved candidate or coverage limitation explicitly retained
NOT_APPLICABLE = no material security-review surface for this change
NOT_RUN_NON_BLOCKING = Codex Security unavailable or policy/egress prevents execution
```

`NOT_RUN_NON_BLOCKING` is never rewritten as `PASS`.

## Authority invariants

```text
Codex Security clean != CompletionDecision
Codex Security finding != Write Authority
Codex Security unavailable != Security PASS
Security reviewer consensus != Nawat Grant
Security scan result != Source Admission
```

Repairs require the normal authorized Attempt/repair boundary when applicable.

## Build-learning capture

Record useful security-review mechanics, false positives, missed classes, attack-path reasoning, coverage failures, and negative oracles in the Build Learning Ledger. Learning may inform later tests/skills/policies but never self-promotes into authority.
