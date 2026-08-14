# WePLD Mandatory Build Method

## Purpose

WePLD is built through a repeatable engineering protocol. Fast implementation is allowed; bypassing specification, source acquisition, deterministic validation, independent review, learning capture, or acceptance authority is not.

## Canonical loop

```text
Spec Kit
  -> Ponytail challenge
  -> source acquisition check
  -> implementation
  -> deterministic gates
  -> independent multi-review
  -> finding reconciliation
  -> bounded repair
  -> deterministic gates again
  -> re-review material changes
  -> authorized acceptance
  -> build-learning capture
```

## 1. Spec Kit — required

For every material change:

```text
constitution
-> specify
-> clarify
-> plan
-> checklist
-> analyze
-> tasks
-> implement
```

A Spec Kit artifact is planning/build-method material. It is not a Nawat grant, CompletionDecision, architecture ratification, or source admission.

## 2. Ponytail — always FULL

Before creating code, dependency, abstraction, service, worker, process, schema, package, or document, challenge it:

1. Does the requested thing need to exist?
2. Is it already solved by the standard library/native platform?
3. Is it already solved by an admitted dependency?
4. Is it solved by a qualified reusable source?
5. Can the design be smaller?
6. Can we remove a process/service/worker/dependency?
7. Does the marginal accepted-outcome value justify its complexity?

Ponytail never removes security, validation, evidence, recovery, correctness, accessibility, or authority controls.

## 3. Source acquisition check

Before building solved machinery, consult `docs/acquisition/MASTER_SOURCE_REGISTRY_V1.*`.

For the exact capability:
- identify 2-3 strongest implementation candidates;
- pin exact revisions;
- inspect exact source paths and tests;
- inspect rights, lineage, security, portability, maintenance state and exit path;
- mine failure cases;
- select minimum sufficient reuse strategy.

Allowed proposed dispositions:

```text
COPY_CANDIDATE
ADAPT_CANDIDATE
PORT_CANDIDATE
VENDOR_CANDIDATE
EMBED_CANDIDATE
PACKAGE_CANDIDATE
REIMPLEMENT
BENCHMARK
REFERENCE
REJECT_AS_INFERIOR
```

No disposition itself admits source.

## 4. Deterministic gates

Run all applicable:
- format/lint;
- static/type checks;
- unit tests;
- integration tests;
- contract/conformance tests;
- negative/adversarial tests;
- security checks;
- dependency/license/SBOM checks when dependencies exist;
- platform-specific checks;
- diff/whitespace/secret checks;
- benchmark or performance gates where material.

A missing applicable gate is explicit incomplete coverage, not PASS.

## 5. Independent reviewer mesh

Use the following as independent Review Producers when available and policy/egress permits:

### CodeRabbit
Use for independent PR/CLI/IDE review and broad bug/security/style review.

### Qodo
Use for multi-agent review, rule/standards enforcement, historical-review relevance, and governance-oriented findings.

### Augment Code
Use for whole-repository context, cross-system impact, correctness/security analysis, and context-heavy review.

### Graphite
Use for review plus ChangeStack/stack-aware PR and delivery context.

### Cubic
Use for independent local/deep/PR review as required by the ratified build method when egress policy permits.

### Continue
Use as an additional source-controlled AI-check/CLI/agent surface. Prefer version-controlled rules/checks where useful. Treat Plan mode/read-only exploration and Agent/tool permissions as behavior oracles, not WePLD authority.

## 6. Reviewer disagreement

Do not vote.

```text
Finding A
Finding B
Finding C
   -> normalize
   -> deduplicate
   -> compare against spec/code/tests/invariants/evidence
   -> resolve or retain explicit ReviewConflict
```

Three clean reviewers do not erase a valid finding from a fourth.

## 7. Repair

A repair is a new bounded Attempt when the change is acceptance-relevant. The reviewer finding does not itself authorize the repair.

After material repair:
- rerun deterministic gates;
- rerun affected reviewers;
- preserve before/after evidence.

## 8. Acceptance

```text
CodeRabbit clean != CompletionDecision
Qodo clean != CompletionDecision
Augment clean != CompletionDecision
Graphite clean != CompletionDecision
Cubic clean != CompletionDecision
Continue check green != CompletionDecision
Green CI != CompletionDecision
Merge != CompletionDecision
```

Completion requires the applicable authorized WePLD/founder acceptance boundary.

## 9. Build Learning — learning while building

Every tool used is also an observable engineering system.

Record evidence-backed mechanisms in `docs/learning/BUILD_LEARNING_LEDGER.md`.

The goal is not to copy product branding. The goal is to learn:
- how planning is structured;
- how context is selected;
- how tools are exposed;
- how permissions are requested;
- how workers are routed;
- how failures are represented;
- how review findings are normalized;
- how sessions recover;
- how cost/latency/quality trade-offs behave;
- which tests expose edge cases.

Learning never silently changes canonical architecture. It becomes a candidate for later qualification.
