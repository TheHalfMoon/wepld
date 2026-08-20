# Analyze — Harness H0 Screening Falsification

## Purpose

This analysis reconciles the H0-SCREEN constitution, specification, clarifications, plan, requirements checklist, canonical build method, architecture invariants, and the seven frozen Harness research documents before producing execution-authoritative `tasks.md`.

```text
ANALYSIS_SCOPE = PLANNING CONSISTENCY / GAP RECONCILIATION
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## A-001 — Research contract versus roadmap authority

**Potential conflict:** the Harness Program proposes substantial future capability while canonical V2.2 currently defines roadmap P0+S1..S10.

**Reconciliation:** H0-SCREEN is not inserted into or substituted for any roadmap slice. It is an off-roadmap falsification program with `ROADMAP_SLICE = NONE`. Its evidence may later support a separately governed architecture/roadmap proposal, but H0 itself cannot mutate V2.2 or start S1-013.

**Disposition:** RESOLVED.

## A-002 — H0 GO thresholds versus screening authority

**Potential conflict:** the tournament contract defines static/adaptive GO/KILL thresholds, while H0-SCREEN executes A/B/C/D.

**Reconciliation:** screening has exactly 40 distinct tasks and one attempt per task/arm/model, with `PROMOTION_AUTHORITY = NONE`. Confirmatory GO thresholds are frozen upstream but are not evaluated as promotion decisions by the screening slice. Screening may estimate variance, cost, failure patterns, and effect directions only.

**Disposition:** RESOLVED. `GO_STATIC`, `GO_ADAPTIVE`, and `NARROW_TO_STATIC` remain confirmatory-only.

## A-003 — Current integrity policy versus a new Spec Kit directory

**Conflict:** canonical Harness research policy permits the frozen seven research docs and otherwise delegates to v24/v23/v19 exact-delta semantics. A new `specs/002-harness-h0-screening/` tree is not an inherited authorized delta and would fail closed.

**Reconciliation:** do not PR the planning package directly. First create a dedicated Harness H0 Spec-Kit trusted-bootstrap wrapper that:

1. binds the exact canonical Harness research wrapper and controlled workflows;
2. permits only its own bounded bootstrap surface;
3. after canonical activation, permits one exact content-addressed H0 Spec Kit package;
4. freezes that package after canonicalization;
5. continues to delegate all unrelated candidate semantics to the prior canonical policy;
6. preserves `HARNESS_IMPLEMENTATION_AUTHORIZED = NO`, source/dependency admission `NONE`, roadmap mutation `NONE`, and `S1_013_PLUS = NOT_STARTED`.

**Disposition:** RESOLVED / POLICY BOOTSTRAP REQUIRED BEFORE SPEC PR.

## A-004 — Rust-first trusted logic versus replaceable research runner

**Potential conflict:** canonical product thesis says `Rust-first trusted logic`, while the H0 runner is intentionally replaceable experiment plumbing.

**Reconciliation:** runner transport may be replaceable, but H0 control/evidence semantics are trusted research logic because they bind identities, verifier results, hard gates, and TrialRecord finalization. Rust-first is therefore the planning preference for authoritative control/evidence code. Synthetic fixture helpers may be minimal scripts/executables because they are frozen untrusted test inputs, not authority.

**Disposition:** RESOLVED. Exact implementation language/toolchain still requires Source Acquisition and implementation authorization.

## A-005 — Existing S1 dependencies versus H0 source admission

**Conflict:** canonical S1 has an admitted exact graph, but H0 is not an S1 runtime feature.

**Reconciliation:** H0 may reuse S1 acquisition records as prior evidence only. Direct H0 use of Rust crates, model SDKs, container engines, CLIs, or donor code requires H0-specific qualification/disposition. Transitive presence in S1 does not become H0 direct-dependency authority.

**Disposition:** RESOLVED / SOURCE ACQUISITION REMAINS OPEN.

## A-006 — SHA-256 identity requirement versus minimal dependency surface

**Gap:** H0 evidence contract prefers SHA-256 canonical identities. Rust stdlib does not provide SHA-256.

**Reconciliation:** do not hand-write cryptographic hashing. Source Acquisition must identify a minimum commodity SHA-256 implementation candidate or another already-admitted mechanism that preserves the frozen SHA-256 contract. Until qualified, implementation remains blocked.

**Disposition:** OPEN ACQUISITION ITEM.

## A-007 — Typed serialization versus zero-dependency aspiration

**Gap:** content-addressed manifests require canonical serialization. Hand-written JSON/canonicalization code can become fragile, but adding serialization packages adds dependency surface.

**Reconciliation:** prefer an already proven typed serialization package set when separately admitted, but define WePLD-owned canonicalization rules above the library. Library defaults are not automatically canonical bytes. Source Acquisition must verify exact versions/features and deterministic behavior.

**Disposition:** OPEN ACQUISITION ITEM.

## A-008 — Local process runner versus container isolation

**Potential conflict:** runner minimalism prefers stdlib/local execution, while H0 effect/network/isolation evidence benefits from containers.

**Reconciliation:** synthetic F01-F16 may use controlled local processes when they can test the intended runner/evidence behavior safely. Real H0-SCREEN tasks requiring task-network denial or filesystem/process isolation must use a qualified controlled local environment. Prefer a narrow adapter to an existing container/runtime CLI rather than embedding a container platform or SDK.

**Disposition:** RESOLVED CONCEPTUALLY / EXACT RUNTIME QUALIFICATION OPEN.

## A-009 — Model-provider access versus task network denial

**Potential conflict:** remote models may require network access while task environments are deny-by-default.

**Reconciliation:** separate model-serving egress from task-environment network authority. Model provider access, when required, occurs through an explicitly qualified channel outside the task environment's general network envelope. All egress classes are recorded separately.

**Disposition:** RESOLVED CONCEPTUALLY / PROVIDER BOUNDARY QUALIFICATION OPEN.

## A-010 — Model profile calibration versus screening leakage

**Risk:** D could overfit to screening outcomes or task identities.

**Reconciliation:** calibration tasks are synthetic/micro-capability fixtures disjoint from H0-SCREEN and H0-CONFIRM. Profiles are derived mechanically, frozen by hash, and contain no benchmark-specific solutions/IDs. D routing rules use profile fields, not screening outcome labels.

**Disposition:** RESOLVED.

## A-011 — B/C/D shared components versus A minimality

**Potential conflict:** equal component libraries could force A to carry complexity, while unequal libraries can create unfair wins.

**Reconciliation:** equality applies only to B/C/D. A is intentionally a separate smaller minimal baseline. Fairness is preserved through common task instructions, final verifier, maximum budgets, and maximum effect authority.

**Disposition:** RESOLVED.

## A-012 — Internal verifier cadence versus final verifier equivalence

**Potential conflict:** recipe policy may vary verifier cadence.

**Reconciliation:** internal test/verifier scheduling may vary as an experimental component, but every task's final acceptance uses the same frozen VerifierManifest across A/B/C/D. Internal calls cannot redefine final pass semantics.

**Disposition:** RESOLVED.

## A-013 — One attempt versus infrastructure readiness failures

**Risk:** a retry/replacement path could preferentially rescue failing arms and silently violate `ATTEMPTS_PER_TASK_ARM_MODEL = 1`.

**Reconciliation:** no started task/arm/model cell is retried for task, harness, model, budget, verifier, infrastructure, or provider failure. Independently evidenced shared infrastructure/provider failure may be rescheduled at most once only before the cell enters task/model/harness execution. That event is a `PRE_ATTEMPT_INFRASTRUCTURE_OBSERVATION`, not a TrialRecord or attempt, and cannot alter any frozen cell identity or protocol parameter. A second pre-attempt readiness failure blocks the affected batch. Once attempt start occurs, every terminal state is retained as the cell's sole screening outcome.

**Disposition:** RESOLVED.

## A-014 — Screening repair versus experiment identity

**Risk:** generic runner/recipe plumbing may need repair during screening, creating mixed protocol generations.

**Reconciliation:** a tracked material runner/recipe/evidence repair creates a new screening batch/protocol identity. Old partial evidence is retained and cannot be silently pooled with a new stable rerun. Recipe revisions must be globally frozen before the next batch.

**Disposition:** RESOLVED.

## A-015 — Runner adequacy versus Harness performance

**Risk:** runner failures or ambiguous runner-overhead accounting could distort arm comparisons or be mistaken for Harness weakness.

**Reconciliation:** runner adequacy metrics are first-class separate evidence. For every started trial, runner overhead is measured from non-overlapping monotonic runner-controlled orchestration intervals divided by total trial wall time from attempt start through finalization. Task/model/provider/verifier execution waits are excluded from the numerator; all started trials, including runner-caused invalid/incomplete outcomes, remain in the batch aggregation. Pre-attempt infrastructure observations are separate readiness evidence. Missing or nonpositive timing fails runner-evidence completeness rather than disappearing from the metric. The minimum runner remains a confirmatory candidate only if the final stable screening batch meets all frozen operational criteria.

**Disposition:** RESOLVED.

## A-016 — Harbor maturity versus anti-complexity rule

**Potential conflict:** Harbor already solves broad evaluation machinery, but immediate adoption introduces a large dependency/provider surface.

**Reconciliation:** Harbor stays reference-only for H0-SCREEN. If stable screening proves local runner inadequacy under frozen triggers, Harbor may enter a separate exact-pin confirmatory runner qualification. No Harbor code import/product dependency is authorized now.

**Disposition:** RESOLVED.

## A-017 — Source acquisition timing

**Question:** can Ponytail and Source Acquisition be canonicalized in the same planning package?

**Reconciliation:** yes, provided `source-acquisition.md` truthfully records current evidence and remains `OPEN` where exact pins/runtime/provider qualification are incomplete. The build method requires the gate before implementation; it does not require a false PASS to finish planning documentation.

**Disposition:** RESOLVED. Implementation remains blocked until a later exact-head Source Acquisition closeout reaches PASS.

## A-018 — Tasks authority

**Question:** may `tasks.md` include implementation tasks even while implementation is unauthorized?

**Reconciliation:** yes as a decomposition, but every implementation-class task must carry an explicit prerequisite on separate canonical implementation authorization. Planning/source-qualification/policy tasks may be executed under their own governed authorization. `tasks.md` cannot grant effects by its own presence.

**Disposition:** RESOLVED.

## A-019 — Acceptance semantics

**Risk:** “planning complete” could be confused with H0 screening complete or H0 thesis accepted.

**Reconciliation:** use distinct states:

```text
H0_SPEC_KIT = CLOSED_CANONICAL_PROVEN
PONYTAIL_COMPLETE_FOR_PLANNING
SOURCE_ACQUISITION_OPEN|PASS
IMPLEMENTATION_AUTHORIZATION_NOT_STARTED|PROVEN
H0_SCREEN_NOT_STARTED|ACTIVE|COMPLETE
H0_PROMOTION_AUTHORITY = NONE
```

**Disposition:** RESOLVED.

## A-020 — Unresolved items that block implementation

The following are intentionally not invented in planning:

```text
EXACT_H0_TOOLCHAIN/CRATE_PINS
EXACT_SHA256_COMPONENT
EXACT_CANONICAL_SERIALIZATION_PACKAGE_SET
EXACT_LOCAL_CONTAINER_RUNTIME_IDENTITY
EXACT_MODEL_PROVIDER_INTEGRATION_BOUNDARY
EXACT_40_TASK_SCREENING_MANIFEST
EXACT_ELIGIBLE_SCREENING_MODEL_SET
EXACT_PER_TASK_BUDGET_VALUES
EXACT_SCREENING_RUN_ORDER_SEED/ALGORITHM
```

These must be resolved by Source Acquisition and pre-execution manifest-freeze tasks under separately governed authority.

## Analysis verdict

No contradiction requires reopening the seven canonical Harness research documents or the V2.2 roadmap.

The minimum next path is:

```text
1. canonicalize dedicated H0 Spec-Kit bootstrap policy
2. prove policy activation
3. canonicalize exact H0 Spec Kit package
4. prove package refreeze
5. execute Ponytail/source-acquisition closeout tasks until Source Acquisition PASS
6. create separate exact H0-SCREEN implementation authorization
7. only then implement runner/evidence/recipe/calibration/fixture machinery
```

```text
ANALYSIS = COMPLETE_FOR_TASK_DECOMPOSITION
SPEC_KIT_SCOPE = COHERENT
SOURCE_ACQUISITION_CHECK = OPEN
H0_SCREEN_IMPLEMENTATION = BLOCKED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
S1_013_PLUS = NOT_STARTED
```
