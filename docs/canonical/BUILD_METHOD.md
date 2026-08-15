# WePLD Mandatory Build Method

```text
Spec Kit planning
-> Ponytail FULL
-> Source Acquisition Check
-> Implement minimum sufficient solution
-> Deterministic gates
-> Independent correctness / engineering review
-> Security-specialist review when applicable
-> Finding reconciliation
-> Bounded repair
-> Re-run gates
-> Re-review material changes
-> Authorized acceptance
-> Build Learning Capture
```

## Spec Kit

Required planning sequence for material work:

```text
constitution -> specify -> clarify -> plan -> checklist -> analyze -> tasks
```

Implementation begins only after the top-level mandatory Ponytail FULL and Source Acquisition Check gates have completed for the task. Spec Kit artifacts guide engineering; they do not grant effects, source admission, or completion.

## Ponytail FULL

Before creating code/dependency/service/worker/abstraction, ask whether it needs to exist, already exists in native/stdlib/admitted machinery, can be acquired from a qualified source, or can be smaller. Ponytail never removes security, correctness, validation, evidence, recovery, accessibility, or authority.

## Source acquisition

Consult the canonical source registry. Pin exact candidate revisions, inspect source/tests/failure modes/rights/security/portability/maintenance/exit strategy, then choose the minimum reuse strategy.

## Deterministic gates

Run all applicable formatting, lint/static/type, unit, integration, contract, negative/adversarial, security, dependency/license/SBOM, platform, secret/diff, and benchmark gates. Missing applicable coverage is incomplete, not PASS.

## Independent correctness / engineering review

`INDEPENDENT_REVIEW = REQUIRED` before acceptance of material work.

Named review producers are used when connected and policy/egress permits:
- CodeRabbit
- Greptile
- Qodo
- Augment Code
- Graphite
- Cubic
- Continue

The minimum gate is evidence from at least one independently qualified reviewer appropriate to the change class, in addition to deterministic gates. If no qualified independent reviewer can run, the work is `REVIEW_BLOCKED`, not PASS, unless an explicitly authorized exception names a qualified substitute and records the residual limitation. A missing named product is never silently treated as approval.

Normalize findings. Do not vote. A valid finding from one reviewer is not erased by clean outputs from others.

External reviewer egress follows `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`.

## Security-specialist review — Codex Security

For material changes with security effect—including source/runtime behavior, authority/security boundaries, parsers, filesystem/process/network effects, dependency execution, sandboxing, credentials/secrets handling, CI/workflow logic, configuration, infrastructure, or external-input handling—run a Codex Security diff scan when available and egress policy permits.

The scan must be anchored to the exact reviewed base/head or local patch. Review every changed file with an applicable security effect, including workflow/configuration/infrastructure changes and deleted baseline files when the deletion affects security behavior. Follow changed behavior only as far as needed to validate candidate vulnerabilities. Use a threat model, validate candidates, perform attack-path analysis for reportable/deferred candidates, and preserve coverage gaps explicitly.

For documentation-only changes with no executable/security-boundary effect, Codex Security may be recorded as `NOT_APPLICABLE`; workflow/configuration/infrastructure changes remain security-relevant when they alter trust or effects.

```text
Codex Security clean != CompletionDecision
Codex Security finding != Write Authority
Codex Security unavailable = NOT_RUN_NON_BLOCKING
Codex Security not run != Deterministic Security Coverage Passed
```

Codex Security supplements deterministic security gates and the correctness reviewer gate. It never replaces Ponytail, AMAN/Nawat governance, evidence requirements, or Trusted Completion.

## Reviewer outcomes

```text
CodeRabbit clean != CompletionDecision
Greptile clean != CompletionDecision
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