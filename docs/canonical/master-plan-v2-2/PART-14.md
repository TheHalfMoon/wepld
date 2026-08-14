CUBIC
WEPLD_NATIVE
CUBIC + WEPLD_NATIVE
```

Hold target, ground truth, acceptance obligations and applicable budgets/model conditions constant where scientifically possible. If a proprietary service prevents exact control, record the mismatch and restrict the claim; do not manufacture equivalence.

Universal monotonic improvement from D0→A→B→C→D is neither required nor assumed. Added context or topology may dilute signal, raise leakage/cost, or harm quality.

### 31.2 Exactly twenty metric families

| ID | Metric family | Required expression |
|---|---|---|
| `M-01` | Severity-weighted precision | Weighted true findings / weighted reported findings |
| `M-02` | Severity-weighted recall | Weighted found defects / weighted ground-truth defects |
| `M-03` | Escaped defects | Missed ground-truth defects by severity, with HIGH/CRITICAL separate |
| `M-04` | False-success rate | Satisfied/clean outcomes while a ground-truth HIGH/CRITICAL defect exists; headline safety guardrail |
| `M-05` | False-positive / human-noise burden | Human-rejected findings per accepted finding and review |
| `M-06` | Acceptance-criteria coverage | Criteria evaluated with admissible evidence / criteria defined |
| `M-07` | Architecture-issue detection | Ground-truth architecture violations found |
| `M-08` | Security-issue detection | Ground-truth security defects found |
| `M-09` | Review-coverage completeness | In-scope files, surfaces, rules, requirements and risks evaluated, with explicit gaps |
| `M-10` | Location accuracy | Findings anchored to correct revision/file/symbol/context window |
| `M-11` | Finding reproducibility and evidence quality | Stability over pinned repeated runs plus sufficient provenance/evidence fraction |
| `M-12` | Reviewer independence | Required role-relative relationships actually satisfied; `UNKNOWN` fails |
| `M-13` | Repair rounds | Attempts, regressions and elapsed convergence by severity |
| `M-14` | Runtime-verification yield | Valid defects found by bounded runtime evidence that static review missed |
| `M-15` | Post-merge reverts / incidents | Longitudinal escaped-defect outcome and severity |
| `M-16` | Human intervention time | Active human attention per review and accepted outcome |
| `M-17` | Latency | Wall time to evidence, outcome, repair and acceptance, reported separately |
| `M-18` | Token / context use | Input/output tokens, capsule size, expansions, cache/retrieval use and omissions |
| `M-19` | Monetary cost | Model/provider/service/VM/tool cost per review and accepted finding |
| `M-20` | Deterministic-tool cost | CPU, memory, I/O and elapsed cost of deterministic evidence production |

The full vector is reported. No weighted scalar may hide an `M-03` or `M-04` regression.

### 31.3 Pre-registered decision and statistical rules

Before a gate run, record primary accepted-outcome measures, safety guardrails, quality floors, cost/latency/disclosure budgets, non-inferiority margins, allowed trade-offs, hypotheses, strata/context, sample/power and stopping rules.

1. A safety-guardrail breach cannot be offset by mean F1, latency or cost.
2. An added layer is accepted only if its pre-registered superiority or non-inferiority condition holds while all safety floors/budgets hold.
3. Report the M-01–M-20 vector and Pareto frontier; do not optimize one scalar.
4. Use paired repeated runs on the same targets, pinned prompts/tools/configuration, seed/stochasticity controls, confidence intervals and effect sizes.
5. Correct multiplicity when testing many arms, contexts or defect classes; distinguish confirmatory from exploratory analysis.
6. Separate sealed/frozen regression results from longitudinal live results.
7. Missing, blocked, timed-out, malformed, denied-egress and unavailable-route runs are missing/blocked evidence, never success.
8. Preserve raw manifests/results so reproduction is possible and limitations are inspectable.
9. Report heterogeneous effects by severity, defect type, language, repository, change size, risk profile and local/egress stratum; no universal aggregate claim.
10. Record planning/decomposition, producer/model/tool/VM, duplicated work, merge/synthesis/evaluation/retry/waste and human coordination cost for workforce comparisons.

### 31.4 Context-economics ablations

| Regime | Contents |
|---|---|
| `CTX-C0` | No context beyond target/diff mechanics |
| `CTX-C1` | Minimal intent and acceptance criteria |
| `CTX-C2` | Targeted local project context |
| `CTX-C3` | Targeted cross-repository context |
| `CTX-C4` | Relevant history and bounded runtime evidence |
| `CTX-C5` | Deliberately overstuffed context |

Each regime records capsule/source digests, provenance/freshness/classification, retrieval misses, omissions, tokens, latency, cost, disclosure risk, quality, false success, architecture/security detection, coverage and human burden. CTX-C5 is a harm/dilution probe, not an assumed optimum.

### 31.5 Staged corpus protocol

| Stage | Purpose and gate |
|---|---|
| `CORPUS-C0` | Tiny mechanism fixtures proving manifests, labels, replay, coverage and failure semantics |
| `CORPUS-C1` | Annotation pilot validating taxonomy, independent annotation, adjudication, severity calibration, rights workflow and cost |
| `CORPUS-C2` | Power-sized stratified gate corpus; size follows primary measures/non-inferiority margins, stratified by severity/class/language/repository/change size and including no-defect controls |
| `CORPUS-C3` | Sealed adversarial/rare-event holdout: prompt injection, architecture/security defects, runtime divergence, huge/generated/binary changes and rare HIGH/CRITICAL cases |
| `CORPUS-C4` | Longitudinal live set of accepted outcomes, escaped defects, reverts, incidents and drift |

Every item records rights, provenance, repository/revision, exact defect/fix or no-defect basis, real/synthetic status, independent annotations, adjudication, severity calibration, contamination and disclosure class. The sealed set must not enter Fehrest, ReviewRules, prompts, memory or tuning. Before S10, corpus/runner/metrics are evaluation infrastructure and evidence—not Byan knowledge.

---

## 32. Adversarial, Failure, and Negative-Test Matrix

These are architecture acceptance cases, not an implementation authorization or a claim that they have run.

### 32.1 Review, repair, completion, and evidence

| ID | Adversarial case | Required result |
|---|---|---|
| `R-01` | Producer timeout/unavailable | Run records timeout/unavailable; immutable coverage gap; outcome incomplete |
| `R-02` | Malformed structured output | No finding/pass synthesized from unparseable output; failure explicit |
| `R-03` | Evaluator/parser failure or exhausted retry | Never default to acceptable quality; incomplete/failed/manual review |
| `R-04` | Large change exceeds budget | Every unreviewed file/surface enumerated; no silent truncation |
| `R-05` | Finding location drifts after rebase/rename | Re-anchor with evidence or mark stale/superseded/unresolvable |
| `R-06` | Duplicate or conflicting findings | Fuse duplicates with provenance; preserve genuine disagreement and routes |
| `R-07` | False-positive feedback | Learning candidate only; no silent rule/threshold/route/exclusion change |
| `R-08` | Builder/reviewer same principal/Attempt where independence required | Requirement fails; self-review remains labelled advisory only |
| `R-09` | Required relationship shared or `UNKNOWN` | Independence fails; unknown never counts as independent |
| `R-10` | Silent provider/model/harness fallback | Reject; persist fallback, disclosure and recompute independence/profile |
| `R-11` | Acceptance criteria missing/contradictory | Record gap; acceptance-critical outcome cannot be satisfied |
| `R-12` | ADR/context stale or superseded | Mark lineage; invalidate/re-evaluate dependent context/findings |
| `R-13` | Cross-repository source unavailable/stale/ACL-changed | Coverage names surface and freshness; never assume clean |
| `R-14` | Capsule digest/source/omission mismatch | Review invalid/incomplete until reconciled; no hidden expansion |
