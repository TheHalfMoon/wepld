# WePLD Mandatory Build Method

```text
Spec Kit
-> Ponytail FULL
-> Source Acquisition Check
-> Implement minimum sufficient solution
-> Deterministic gates
-> Correctness / engineering reviewer mesh
-> Security-specialist review when applicable/available
-> Finding reconciliation
-> Bounded repair
-> Re-run gates
-> Re-review material changes
-> Authorized acceptance
-> Build Learning Capture
```

## Spec Kit

Required sequence for material work:

```text
constitution -> specify -> clarify -> plan -> checklist -> analyze -> tasks -> implement
```

Spec Kit artifacts guide engineering; they do not grant effects or completion.

## Ponytail FULL

Before creating code/dependency/service/worker/abstraction, ask whether it needs to exist, already exists in native/stdlib/admitted machinery, can be acquired from a qualified source, or can be smaller. Ponytail never removes security, correctness, validation, evidence, recovery, accessibility, or authority.

## Source acquisition

Consult the canonical source registry. Pin exact candidate revisions, inspect source/tests/failure modes/rights/security/portability/maintenance/exit strategy, then choose the minimum reuse strategy.

## Deterministic gates

Run all applicable formatting, lint/static/type, unit, integration, contract, negative/adversarial, security, dependency/license/SBOM, platform, secret/diff, and benchmark gates. Missing applicable coverage is incomplete, not PASS.

## Correctness / engineering reviewer mesh

Use when available and policy permits:
- CodeRabbit
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue

Normalize findings. Do not vote. A valid finding from one reviewer is not erased by clean outputs from others.

## Security-specialist review — Codex Security

For material changes to source code, runtime behavior, authority/security boundaries, parsers, filesystem/process/network effects, dependency execution, sandboxing, credentials/secrets handling, CI trust, or external-input handling, run a Codex Security diff scan when available and egress policy permits.

The scan must be anchored to the exact reviewed base/head or local patch. Review every changed source file and follow changed behavior only as far as needed to validate candidate vulnerabilities. Use a threat model, validate candidates, and perform attack-path analysis for reportable/deferred candidates. Preserve coverage gaps explicitly.

For documentation-only changes with no executable/security-boundary effect, Codex Security may be recorded as `NOT_APPLICABLE`; workflow/config changes remain security-relevant and require deterministic/security review appropriate to their effects.

```text
Codex Security clean != CompletionDecision
Codex Security finding != Write Authority
Codex Security unavailable = NOT_RUN_NON_BLOCKING
Codex Security not run != Deterministic Security Coverage Passed
```

Codex Security supplements deterministic security gates and the correctness reviewer mesh. It never replaces Ponytail, AMAN/Nawat governance, evidence requirements, or Trusted Completion.

## Reviewer outcomes

```text
CodeRabbit clean != CompletionDecision
Qodo clean != CompletionDecision
Augment clean != CompletionDecision
Graphite clean != CompletionDecision
Cubic clean != CompletionDecision
Continue green != CompletionDecision
Codex Security clean != CompletionDecision
Green CI != CompletionDecision
```

## Build Learning

While using builders/reviewers/tools, observe how they plan, retrieve context, expose tools, request permissions, route workers, recover sessions, retry/fallback, generate tests, detect defects, and represent failures. Record evidence-backed positive mechanisms and negative oracles. Learning proposes; it never authorizes.
