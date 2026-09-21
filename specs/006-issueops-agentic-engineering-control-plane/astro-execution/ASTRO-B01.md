# ASTRO-B01 - Preregister controlled benchmark protocol

```text
TASK = ASTRO-B01
TASK_TYPE = D (bounded specification / qualification manifest)
SLICE = S3-D
HANDOFF_CARD = WEPLD_MUSE_EXECUTION_HANDOFF.md (ASTRO-B01)
PREREQUISITE = ASTRO-G01 accepted

BASE = 100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde
BASE_TREE = a0abd67acd610284d275fad87662a4ab7f64fcb2
CANONICAL_REPOSITORY = TheHalfMoon/wepld
CANONICAL_DEFAULT_BRANCH = main
```

This record is a preregistration, not a result. It fixes the dataset
construction rules, route identity, budget envelope, scoring rubric,
adjudication independence, contamination handling, stopping rules and pilot
sizing method that must be frozen before any benchmark score exists. It grants
nothing, admits no source, authorizes no donor execution and publishes no
performance claim.

```text
PROTOCOL_STATE = PREREGISTERED
SCORES_PRODUCED = NONE
RUNTIME_RESULT_IMPLIED = NONE
PERFORMANCE_CLAIM = NONE
```

## 1. Bounded output and non-goals

```text
BOUNDED_OUTPUT = this single record
PRODUCT_CODE_CHANGE = NONE
RUNTIME_DEPENDENCY_CHANGE = NONE
CI_POLICY_CHANGE = NONE
PROTECTED_GOVERNANCE_CHANGE = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
AUTHORITY_EFFECT = NONE
RIGHTS_EFFECT = NONE
```

Non-goals, per the B01 card and the common task contract:

- no benchmark run, pilot run, harness, scorer or reporting implementation;
- no model/provider/worker selection, routing, installation or authorization;
- no source acquisition, dependency admission, donor import or vendor pin;
- no mutation of `docs/canonical/*`, `specs/005-*`, `specs/007-*` or any other
  historical record - historical records are preserved byte-identically;
- no release, parity, capacity, latency, cost or "better than" claim;
- no repurposing of the benchmark protocol as an acceptance or authority
  mechanism for any other task.

The existing owners and conventions are reused: Assurance owns the evidence
model, Byan owns proposal-only learning, and the Runtime owns execution. This
record introduces no new owner, store, service, numbering system or dependency.

## 2. Verified inputs used to build this preregistration

Every identity below was resolved from the trusted base for this task - the
exact PR base of this candidate - and from live GitHub state re-read at the
time this record was written. Blob identities are Git blob hashes, not
narrative references.

| Input | Exact identity | Role here |
|---|---|---|
| Canonical `main` | `100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde`, tree `a0abd67acd610284d275fad87662a4ab7f64fcb2` | trusted base for this record |
| ASTRO-G01 accepted planning head | `4deee28f85153c357e5a51413cbef438297f67cc` | accepted predecessor head |
| ASTRO-G01 post-merge closure | PR #340 closure record; merge commit `100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde`; post-merge `foundation-integrity` run `35513354193` event `push` = PASS | prerequisite evidence |
| Benchmark and assurance plan | `specs/006-issueops-agentic-engineering-control-plane/astro-master/WEPLD_BENCHMARK_AND_ASSURANCE_PLAN.md`, blob `6a2466b77beca0105e619cebcee0edae6808dacd` | arm definitions A/B/C/D/D0 and the qualification matrix |
| Muse execution handoff | `specs/006-issueops-agentic-engineering-control-plane/astro-master/WEPLD_MUSE_EXECUTION_HANDOFF.md`, blob `0331210c08e2c2626668271b89efb10b31c618a0` | B01 card, common task contract, dependency graph |
| Master build plan | `specs/006-issueops-agentic-engineering-control-plane/astro-master/WEPLD_CANONICAL_MASTER_BUILD_PLAN.md`, blob `797aaabae74a0b65fa5575bbef0c76a8b8b64b95` | S3-D slice placement and the "no performance claim from a README" rule |
| Assessment evidence | `specs/006-issueops-agentic-engineering-control-plane/astro-master/EVIDENCE_AND_VALIDATION.md`, blob `d81e63a72d757ca94e4a93498ca35245f07c133d` | evidence-record conventions |
| Active integrity successor | `.github/scripts/wepld_s3_contracts_freeze_shortcut_v71_integrity.py`, blob `e2b3caf4ef7e0ed0e34c7415776cb29c92d752e0` | current authority/grant source |
| Inherited integrity base | `.github/scripts/wepld_integrity.py`, blob `1c6eee47822086d4c900bf6e9621b0d067320946` | path-allowlist and stage rules |
| Integrity workflow | `.github/workflows/foundation-integrity.yml`, blob `be8dd63cd222b326353dc72468bfb6e7d6f57585` | deterministic gate wiring for this candidate |
| Canonical state | `docs/canonical/CURRENT_STATE.md`, blob `86a52a910cb6d03f5ab63c71893040894913adfe` | frozen frontier vocabulary |
| Build method | `docs/canonical/BUILD_METHOD.md`, blob `807d6574e48b179414d6aa826b475619b3f452f1` | mandatory build/evidence sequence |
| Security review policy | `docs/canonical/SECURITY_REVIEW_POLICY.md`, blob `d6c0e85f7d4395ac19023d4c6e215cbe69821f9c` | security-scan applicability rules |
| External review egress policy | `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`, blob `63828b821775d2a3659e9b7478bd78d96c0cdb98` | manual-only external review boundary |
| Source registry index | `docs/acquisition/SOURCE_REGISTRY_INDEX.md`, blob `4a2fe363e0e66f7183e0221743258fcf558a3733` | source/rights record location; nothing acquired by this task |

## 3. Controlled difference arms

The arm set is fixed exactly as the benchmark plan defines it. Each arm is a
single controlled difference against arm A. No arm may add, remove or weaken a
safety constraint, and no arm may change more than its named difference.

| Arm | Controlled difference | Typed question | Executable at this preregistration |
|---|---|---|---|
| A | Raw qualified worker with the same base tools and safety constraints | What does the available intelligence achieve unaided? | NO |
| B | A + AGILLE intent / specification / plan qualification | What is the value of clearer work definition? | NO |
| C | A + Fehrest bounded source-grounded context | What is the value of the Project Brain? | NO |
| D | A + AGILLE + Fehrest + governed Runtime + independent assurance | What is the value, and what is the overhead, of the complete WePLD loop? | NO |
| D0 | Deterministic tooling only, on tasks with a deterministic route | Is an agent unnecessary for this task at all? | NO |

```text
ARM_EXECUTABLE_AT_THIS_BASE = NONE
REASON = the first closed WePLD loop does not exist yet at this base; the
         qualifying tasks (C01, A02, X01, X02, X03, U01..U05, F02..F08, R01/R03,
         Q01/Q03, S01/S03, W01, T01) are not accepted, and ASTRO-G02 has not
         qualified an executable first-loop fixture
CONSEQUENCE = B01 fixes the protocol; it does not and cannot run it
```

The raw baseline is "raw" only with respect to WePLD machinery. It keeps every
safety constraint, permission boundary and prohibited-effect rule that applies
to the qualified route. A faster unsafe baseline is not a baseline.

## 4. Dataset construction and task families

Task families are fixed to the benchmark plan set, each with its own required
outcome criteria frozen before any run:

| Family | Required preregistered outcome criteria |
|---|---|
| Defect repair | Named failing behavior becomes correct; no unrelated behavior change |
| Small feature | Named behavior exists and is reachable through the declared surface |
| Refactor | Declared structural property holds; observable behavior unchanged |
| Unfamiliar / legacy repository | Correct localization and change without regressions in the touched contract |
| Security-sensitive change | Threat-to-test obligation satisfied; no new unauthorized effect |
| Deliberate no-change / clarification case | Correct abstention or clarification request instead of an invented change |

Per task, the preregistration record fixes before execution:

```text
TASK_ID / FAMILY
STARTING_TREE_SHA
TASK_STATEMENT_SHA
DECLARED_OUTCOME_CRITERIA (frozen, no post-hoc relaxation)
TOOL_AVAILABILITY_SET
ENVIRONMENT_IDENTITY (OS build, hardware class, locale, network posture)
PREREGISTERED_SEED(S)
ROUTE_IDENTITY (section 5)
BUDGET_ENVELOPE (section 6)
HELD_OUT_STATUS (visible | held-out)
```

The visible feasibility set and the held-out set are disjoint and both are
frozen before the held-out run. A task statement that changes after the first
attempt is a new task identity, not an edit to the old one.

## 5. Route identity freeze and substitution control

Comparison validity depends on holding route identity constant. The
preregistration therefore requires, per arm and per comparison:

```text
MODEL_IDENTITY = exact model identifier and revision string as reported by the provider
PROVIDER_IDENTITY = exact provider/product identity
HARNESS_IDENTITY = exact worker/harness name, version and configuration digest
TOOL_SET_IDENTITY = exact tool/permission set and its configuration digest
CONTEXT_ROUTE_IDENTITY = retrieval/specification route and its configuration digest
```

Rules:

- a comparison whose arms differ in any identity above other than the named
  controlled difference is `NONCOMPARABLE` and is reported as such, never as a
  win or a loss;
- a qualified route change starts a separately reported stratum; results are
  never pooled across strata to manufacture significance;
- silent provider, model, worker or tool substitution is prohibited, and any
  substitution invalidates the affected runs rather than being smoothed over;
- where a provider publishes no immutable revision identity, that limitation is
  recorded at task level and the comparison carries a stated uncertainty floor.

## 6. Budget envelope and cost accounting

Total budget is equalized across compared arms for the same task: the same
wall-clock ceiling, the same token ceiling, the same tool-call ceiling and the
same monetary ceiling, expressed in the units the harness can actually meter.

```text
TRACKED_SEPARATELY = indexing / context setup cost, reported both unamortized
                     and amortized over repeated work on the same project
COUNTED_AS_COST    = input tokens, output tokens, retrieval bytes, tool calls,
                     wall time, compute/cloud spend, peak memory/CPU,
                     interactive p50/p95 latency, cancellation latency,
                     human review minutes, maintenance effort
```

Budget exhaustion is an outcome, not an excluded run. An arm that spends its
budget without producing an accepted outcome has failed that task, and its cost
still counts in the denominator.

## 7. Scoring rubric

```text
PRIMARY_MEASURE = proportion of tasks independently accepted against the
                  preregistered outcome criteria with zero unauthorized effects
```

Secondary measures, all preregistered: severity-weighted regressions, false
completion (claimed done while criteria are unmet), coverage omissions, human
review minutes, wall time, input/output tokens, retrieval bytes, tool/runtime/
cloud cost, peak memory/CPU, p50/p95 interactive latency, cancellation latency,
recovery success and maintenance burden.

Scoring rules:

- report denominators, exclusions and confidence intervals for every aggregate;
- report task-level evidence, not only an aggregate leaderboard position;
- green CI, merged pull request, generated tokens, agent count and turn count
  are never scored as success;
- a task abandoned by budget exhaustion scores as not accepted;
- the rubric is frozen before the first run of the compared pair, and no
  participant may relax the outcome criteria after seeing results;
- Byan may later propose optimizations, but it may not change scoring rules,
  thresholds or exclusions to improve an apparent score.

## 8. Independence and adjudication

```text
BUILDER != ACCEPTANCE_AUTHORITY
PRODUCER != ADJUDICATOR
SCORER != INTERESTED_PARTY
```

Preregistered rules:

- acceptance of each task outcome is a separate decision made by an adjudicator
  who did not produce the change;
- adjudicator identity, qualification basis and independence basis are recorded
  per task; an unqualified adjudicator is not a substitute for a qualified one;
- majority vote across correlated producers is not adjudication; disagreement
  is exposed rather than averaged away;
- the adjudicator may abstain, and an abstention is recorded as an unresolved
  outcome rather than a pass;
- where independent adjudication is unavailable for a task, the task is
  reported as `UNRESOLVED`; missing adjudication is never converted into PASS;
- author-generated tests are not the sole correctness oracle; the
  preregistered outcome criteria and, where applicable, an independent
  evaluator carry that role.

## 9. Contamination control

```text
HELD_OUT_SET = BLINDED_AND_DISJOINT_FROM_VISIBLE_SET
CANARY_OR_PRIVATE_WORKLOADS = NEVER_PUBLISHED
```

Preregistered controls:

- record whether each task, fixture or artifact is publicly available, and if so
  where it is available;
- record plausible training-data exposure of the task family and treat it as an
  explicit limitation rather than assuming a clean split;
- sequence the visible set before the held-out set and never re-run the held-out
  set after observing aggregate results without recording the extra look;
- record every discarded or aborted run, including runs discarded for harness
  or environment faults;
- keep internal canaries and private workloads out of any published evidence;
- publish only approved/redacted evidence, and publish no aggregate that would
  let a reader reconstruct a private workload.

## 10. Stopping rules and pilot sizing method

Stopping rules, frozen before the first run:

```text
PER_TASK_ATTEMPT_LIMIT      = preregistered fixed integer, identical across arms
PER_TASK_BUDGET_CEILING     = preregistered, identical across arms
GLOBAL_BUDGET_CEILING       = preregistered for the whole study
CANCELLATION_POLICY         = preregistered; cancellation latency measured
UNSAFE_EFFECT_STOP          = any unauthorized effect stops that run immediately
                              and is reported, never reclassified
SYSTEM_FAULT_POLICY         = harness/environment faults are recorded; the task
                              may be rerun only under the recorded fault rule
```

Pilot sizing method (a method, not a result):

1. run a feasibility pilot on the visible set with the arms the base actually
   permits, preserving paired structure by task;
2. from the pilot, estimate the per-task paired difference and its dispersion,
   and report the pilot separately from the held-out study;
3. size the held-out study from the paired-difference dispersion and the
   founder/product-set practical effect threshold, at a preregistered
   confidence level and precision target;
4. if the pilot dispersion estimate is unstable (for example, too few tasks or
   an outlying family), enlarge the pilot or the held-out set rather than
   reporting a narrow interval the data cannot support;
5. stop expanding an arm, topology level or context treatment when the measured
   gain falls below the preregistered practical threshold or when safety or cost
   worsens, even if the point estimate is favourable.

```text
PRACTICAL_EFFECT_THRESHOLD_SET_BY = founder / product acceptance, before the held-out run
PILOT_VARIANCE_ESTIMATE = NOT_COMPUTED (no pilot has run)
HELD_OUT_SIZE = NOT_COMPUTED (sized from a pilot that does not exist yet)
```

## 11. Required negative oracle

Card oracle, in the card's own words: missing baseline or changed model makes
the comparison noncomparable. This is treated as a rejection test that a later
scoring/reporting implementation must pass, not as a documentation statement.

```text
ORACLE_ID = B01-NEG-1
CANDIDATE_ORACLE = inject a comparison in which arm B's baseline records are
                   absent or incomplete, and a second comparison in which the
                   frozen route identity differs between compared arms
REQUIRED_RESULT = the scoring/reporting implementation refuses to emit a
                  comparative claim; it must report NONCOMPARABLE with the
                  reason recorded, and must not emit a win/loss or an aggregate
                  that silently drops the affected pair
ORACLE_STATUS = CANDIDATE_NOT_EXECUTED
BLOCKING_REASON = no scoring/reporting implementation exists at this base and
                  this task is not authorized to add one
ORACLE_OWNER = the implementation that first emits comparative benchmark
               evidence (expected ASTRO-B02 evidence pipeline, with the
               ASTRO-F02 deterministic assurance seed as its producer surface)
```

Recorded companion failure conditions that must also be rejected rather than
scored: a paired task whose starting tree, task statement, tool set or budget
differs between arms; a paired task whose outcome criteria changed after the
first attempt; and an aggregate computed over a denominator that omits
exhausted, aborted or unresolved runs.

## 12. Typed-decision and calibration interface

B01 exposes the preregistered typed questions that the later typed-decision work
(`ASTRO-K03`, which depends on this task and `ASTRO-A05`) consumes. This is a
decision-quality interface only.

```text
JEV_INFORMS = YES
JEV_AUTHORIZES = NO
```

Preregistered typed questions for evaluation, each with an explicit abstention
option and a held-out reliability requirement:

- "Is this candidate change plausibly sufficient for the declared outcome
  criteria?" (binary, with abstention);
- "Does this evidence package cover every applicable changed surface?"
  (binary, with abstention);
- "Which of the named unresolved causes explains this failure?" (choice over a
  frozen label set, with abstention);
- "How severe is this regression relative to the declared contract?" (ordered
  scale, with abstention).

Calibration is measured on held-out decisions with a proper scoring rule and an
explicit abstention rate. A calibrated confidence never becomes an acceptance
decision, a security pass, a merge authority or a benchmark score, and a
model's self-reported confidence is not evidence.

## 13. Verification performed and coverage limits

Verification performed while producing this record:

- live canonical `main` and the base tree were re-resolved from the canonical
  remote rather than copied from a summary (`main` = `100d5c3c...`, tree =
  `a0abd67...`);
- the ASTRO-G01 closure evidence on PR #340 was re-read live, including the
  merge identity and the post-merge `foundation-integrity` push run;
- every blob identity in section 2 was resolved with `git rev-parse` against
  the exact base commit;
- the arm set, task families, qualification-matrix obligations and the
  "no performance claim" rule were read from the benchmark plan at the base;
- the delta shape of this candidate is documentation-only: one new Markdown
  record, with no executable, workflow, configuration, dependency or protected
  governance change;
- the external-reviewer availability snapshot taken for this head was
  `CodeRabbit = rate limited on manual request` and
  `Qodo = billing blocked (trial ended)`; neither state is a review result.

Not executed here, and therefore not claimed:

- no benchmark, pilot, harness run or measurement of any kind;
- no scores, effect sizes, confidence intervals, thresholds or sized study;
- no arm was executed and no first loop exists at this base, as recorded in
  section 3;
- the section 11 negative oracle is a candidate and was not executed;
- no source acquisition, dependency admission, donor pin, rights decision or
  platform qualification was performed by this task;
- no native Windows qualification was performed by this task;
- Codex Security applicability is `NOT_APPLICABLE` on the ground that this
  change adds a planning/governance Markdown record only and alters no trust
  boundary, authority implementation, parser, containment or credential
  surface. This is an applicability classification, not a security pass.

## 14. Successors unlocked by acceptance

Acceptance of this record unlocks exactly the successors named by the B01 card:

```text
ASTRO-B02  (also requires ASTRO-G02)
ASTRO-K03  (also requires ASTRO-A05)
```

No other successor is unlocked. Acceptance of this protocol grants no runtime,
routing, provider, source or implementation authority, and no benchmark claim
becomes true by virtue of this record being accepted. B02 remains blocked until
an executable first loop is qualified by ASTRO-G02, and no arm may be run
before that point.

## 15. Resume record

```text
TASK = ASTRO-B01
BRANCH = codex/astro-b01-benchmark-prereg-20260921
BASE = 100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde
SCOPE_GRANT = documentation-only task record under
              specs/006-issueops-agentic-engineering-control-plane/astro-execution/
CHANGED_FILES = 1 (this record)
SOURCE_PINS = none acquired by this task
COMPLETED_TESTS = trusted-base resolution, blob-identity resolution, arm/card
                  traceability check, delta-shape check
PENDING_TESTS = foundation-integrity candidate verification and s1-admission
                verification on this exact head; independent review of this head
REVIEW_STATE = not yet requested at the time this record was written
UNKNOWN_EFFECTS = none identified; no effect was proposed
OPEN_FINDINGS = none recorded
OPEN_ORACLE_CANDIDATES = B01-NEG-1 (noncomparable-comparison rejection),
                         owner recorded, not executed
NEXT_SMALLEST_ACTION = resolve exact-head identities for this candidate, run the
                      canonical candidate gate on the exact head, record the
                      egress preflight, request the independent review, and
                      proceed to acceptance only if that review is clean
```

Resuming this task means re-reading live canonical `main`, re-resolving every
identity in section 2, and comparing them against this record. A remembered
narrative is not evidence, and a superseded base invalidates every identity
above. If the base has advanced, this preregistration must be revalidated
against the new base before acceptance rather than silently rebased.
