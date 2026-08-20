# Plan — Harness H0 Screening Falsification

## Identity

```text
FEATURE = 002-harness-h0-screening
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0-SCREEN
PLANNING_ORIGIN_MAIN = a377c75727456934ea6bde456e4a082bdaf710f5
ROADMAP_SLICE = NONE
CANONICAL_HARNESS_RESEARCH = PR_42 / CLOSED_CANONICAL_PROVEN
IMPLEMENTATION = NOT_AUTHORIZED
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
S1_013_PLUS = NOT_STARTED
```

Exact final PR/head identity is GitHub evidence and MUST NOT be encoded as a purported final candidate head inside this tracked file.

## Build-method provenance

WePLD canonical order:

```text
constitution
-> specify
-> clarify
-> plan
-> checklist
-> analyze
-> tasks
-> Ponytail FULL
-> Source Acquisition Check
-> separate implementation authorization
-> minimum sufficient implementation
```

This plan follows `docs/canonical/BUILD_METHOD.md`. Spec Kit artifacts coordinate work; they do not create effect, source, dependency, completion, or roadmap authority.

## Upstream frozen research contracts

H0-SCREEN consumes, without editing, the canonical Harness research bundle:

```text
docs/acquisition/HARNESS_PROGRAM_DONOR_CANDIDATES_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_ARCHITECTURE_AND_FALSIFICATION_DOSSIER_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_H0_THESIS_TOURNAMENT_CONTRACT_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_H0_EVALUATION_DONOR_RECONNAISSANCE_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_H0_EVIDENCE_AND_RUNNER_CONTRACT_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_H0_RUNNER_DECISION_REVIEW_2026-08-20.md
docs/acquisition/WEPLD_HARNESS_H0_SCREENING_FIXTURE_AND_RECIPE_BOUNDARY_2026-08-20.md
```

The current Spec Kit package translates those research contracts into a bounded execution plan; it does not change their claims.

## Architecture

```text
Frozen H0 manifests / recipe definitions
                 |
          WePLD H0 control
                 |
      deterministic recipe compiler
          /       |        \
         A        B        C/D
                 |
         RunnerAdapter boundary
                 |
      replaceable local process/container
                 |
          harness/agent command
                 |
       raw logs/artifacts/usage/effects
                 |
       WePLD evidence collection
                 |
       frozen objective verifier
                 |
          evidence finalizer
                 |
        normalized TrialRecord
                 |
       screening metrics/report
```

The runner executes; it does not declare verified success or H0 promotion.

## Future implementation ownership boundaries

These paths are **planning candidates only**. They are not authorized by this document.

Preferred bounded shape:

```text
research/harness_h0/
  Cargo.toml
  src/
    lib.rs
    canonical.rs
    manifests.rs
    identity.rs
    recipe.rs
    calibration.rs
    runner.rs
    evidence.rs
    verifier.rs
    screening.rs
  fixtures/
    synthetic/
    calibration/
    recipe_conformance/
  tests/
    synthetic_runner.rs
    recipe_conformance.rs
    evidence_contract.rs
    isolation.rs
    hard_gates.rs
```

A later implementation-authorization policy may choose a smaller exact shape. Any broader architecture requires evidence of need and new authorization.

No product runtime path under `apps/` or existing S1 runtime crate is presumed part of H0-SCREEN.

## Phase H0-P0 — Spec Kit canonicalization

- canonicalize this exact planning packet under a dedicated trusted-base policy;
- run deterministic integrity qualification;
- apply exact-head egress preflight under `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`;
- obtain independent correctness/engineering review;
- reconcile findings;
- merge only on exact reviewed head;
- prove post-merge canonical activation/refreeze.

Exit:

```text
H0_SPEC_KIT = CLOSED_CANONICAL_PROVEN
IMPLEMENTATION = BLOCKED
```

## Phase H0-P1 — Ponytail FULL

Ponytail must test whether each proposed H0 mechanism is actually necessary.

Expected minimum conclusions:

- no generalized HIR/plugin framework;
- no LLM router;
- no memory subsystem;
- no multi-agent/sibling portfolio;
- no distributed scheduler;
- no database/service/UI;
- no cloud-provider SDK by default;
- no Harbor adoption for screening;
- no automatic harness mutation;
- no broad provider abstraction unless a concrete screening need proves it.

Non-reducible controls include immutable identity, verifier separation, effect/budget bounds, evidence completeness, cleanup/isolation, secret handling, and hard-gate accounting.

## Phase H0-P2 — Source Acquisition Check

Qualify only the minimum implementation substrate.

Planning preference:

```text
TRUSTED_CONTROL_EVIDENCE_LOGIC = RUST_FIRST
LOCAL_PROCESS_EXECUTION = STDLIB_FIRST
CONTAINER_BOUNDARY = EXISTING_LOCAL_RUNTIME_CLI / REPLACEABLE
SERIALIZATION = COMMODITY_TYPED_PACKAGE_CANDIDATE
SHA256 = COMMODITY_HASH_PACKAGE_CANDIDATE
MODEL_PROVIDER_INTEGRATION = REPLACEABLE / NO_SDK_ASSUMED
HARBOR = REFERENCE_ONLY_FOR_SCREENING
```

Existing S1 acquisition/admission evidence may be reused as prior evidence but does not automatically grant H0 direct-dependency authority.

Source Acquisition must finish with an exact, minimal component list and explicit `PASS` before any implementation policy can be proposed.

## Phase H0-P3 — Separate implementation authorization

Create a dedicated trusted-base H0 implementation policy that permits only the exact minimum source/config/fixture/dependency surface established by P1/P2.

The policy MUST preserve:

```text
PRODUCT_HARNESS_INTEGRATION = NO
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
HARBOR_ADMISSION = NONE
CONFIRMATORY_EXECUTION = NO
```

Candidate-head self-check is not trusted-base admission authority during the bootstrap transition. Merge requires exact-head deterministic/review evidence followed by post-merge activation proof.

## Phase H0-P4 — Evidence/control core

After authorization only:

- canonical serialization;
- content-addressed manifest identities;
- domain-separated TrialIdentity;
- frozen state machine;
- append-oriented raw observations;
- artifact/usage/effect/failure/verifier records;
- evidence completeness rules;
- mechanical `verified_success` derivation;
- normalized screening export.

No runner implementation is allowed to bypass or own finalization semantics.

## Phase H0-P5 — Recipe library and compilers

Implement only the frozen option vocabulary and A/B/C/D boundaries.

- A minimal constructor;
- B one fixed rich recipe;
- C deterministic task/environment/budget compiler;
- D deterministic C+ModelCapabilityProfile compiler;
- RecipeDecisionTrace;
- recipe validation against allowed components, budget, and authority.

Run R01-R07 before any real screening task.

## Phase H0-P6 — Calibration

Create a separate synthetic/micro-capability calibration suite for D.

Requirements:

```text
DISJOINT_FROM_H0_SCREEN = YES
DISJOINT_FROM_H0_CONFIRM = YES
BENCHMARK_SPECIFIC_IDENTIFIERS = NONE
PROMOTION_EVIDENCE = NO
PROFILE_DERIVATION = MECHANICAL
PROFILE_HASH = FROZEN
```

Recalibration is required when a provider/model revision materially changes.

## Phase H0-P7 — Synthetic runner qualification

Implement the minimum local RunnerAdapter and pass F01-F16.

Pass gate:

```text
ALL_REQUIRED_FIXTURES = PASS
UNEXPLAINED_EVIDENCE_MISMATCH = 0
ACCEPTED_UNAUTHORIZED_EFFECT = 0
SECRET_CANARY_LEAK_TO_PUBLIC_EVIDENCE = 0
CROSS_TRIAL_CONTAMINATION = 0
```

Any failure blocks H0-SCREEN tasks and is classified as runner/evidence defect rather than Harness evidence.

## Phase H0-P8 — Screening manifest freeze

Before real H0-SCREEN execution:

- freeze 40 task identities and archetypes;
- freeze eligible model identities/settings;
- freeze A/B/C/D recipes and routing rules;
- freeze task environments/verifiers/budgets/effect envelopes;
- freeze retry policy/failure taxonomy;
- generate balanced run-order rule;
- record expected run count.

Screening task identities must remain disjoint from future confirmatory tasks.

## Phase H0-P9 — H0-SCREEN execution

Execute one attempt per task/arm/model cell under common runner plumbing and paired authority/budget/verifier contracts.

Do not remove unfavorable trials. Preserve `EVIDENCE_INCOMPLETE`, verifier failures, runner defects, authority denials, and hard-gate incidents explicitly.

Screening may be restarted after a generic plumbing repair only by creating a new frozen screening batch/protocol identity; stale partial evidence is retained and not mixed silently.

## Phase H0-P10 — Screening analysis and runner decision

Produce descriptive/paired screening metrics and runner adequacy evidence. Screening analysis may estimate variance/cost ranges but MUST NOT issue confirmatory H0 GO decisions.

Evaluate the minimal runner against the frozen retention/switch criteria:

```text
INVALID_OR_INCOMPLETE_RATE <= 2_PERCENT
MEDIAN_RUNNER_OVERHEAD_FRACTION <= 15_PERCENT
OPERATOR_MINUTES_PER_100_STARTED_TRIALS <= 120
NO_DISTRIBUTED_SCHEDULER_REQUIRED
NO_NEW_CLOUD_PROVIDER_BACKEND_REQUIRED
EVIDENCE_CONTRACT_FULLY_SATISFIED
```

Possible screening closeout:

```text
SCREENING_EVIDENCE_READY_FOR_CONFIRMATORY_PLANNING
RUNNER_REPAIR_REQUIRED
RUNNER_REPLACEMENT_QUALIFICATION_REQUIRED
H0_DESIGN_REPAIR_REQUIRED
H0_RESEARCH_KILL_OR_NARROW_CANDIDATE
```

None is production implementation authority.

## Deterministic gates

Applicable future gates include:

- format/lint/static checks for the chosen implementation language;
- unit tests for canonical serialization and identity;
- R01-R07 recipe conformance;
- F01-F16 synthetic runner fixtures;
- evidence completeness/negative tests;
- budget/effect-envelope denial tests;
- secret-canary/redaction tests;
- workspace isolation/cleanup tests;
- retry symmetry tests;
- exact manifest/hash reproducibility;
- source/dependency/license/SBOM/advisory gates where dependencies exist;
- platform/runtime evidence for claimed local/container behavior;
- independent correctness review;
- Codex Security when available/egress-permitted for security-relevant implementation/policy changes.

## Evidence retention

The H0-SCREEN evidence packet must retain immutable identities for:

- planning/policy base and exact implementation head;
- toolchain and direct dependency graph;
- runner/runtime/container identity;
- all frozen experiment manifests;
- calibration profiles;
- recipe manifests/traces;
- synthetic qualification results;
- real screening TrialRecords;
- normalized export;
- runner adequacy metrics;
- hard-gate incidents;
- deterministic gate runs;
- security/reviewer evidence and finding reconciliation.

## Exit condition

This Spec Kit planning slice exits when planning, Ponytail, and Source Acquisition are canonical and independently qualified, with a bounded implementation surface defined. It does **not** exit into implementation automatically.

```text
NEXT_AFTER_PLANNING = SEPARATE_H0_SCREEN_IMPLEMENTATION_AUTHORIZATION
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
S1_013_PLUS = NOT_STARTED
```
