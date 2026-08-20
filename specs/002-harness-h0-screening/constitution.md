# Constitution — Harness H0 Screening Falsification

```text
FEATURE = 002-harness-h0-screening
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0-SCREEN
ROADMAP_SLICE = NONE
PLANNING_ORIGIN_MAIN = a377c75727456934ea6bde456e4a082bdaf710f5
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## Authority

1. Canonical `AGENTS.md`, architecture invariants, build method, security policy, egress policy, master-plan index, source-registry index, and the seven canonical Harness research documents remain controlling authority.
2. This Spec Kit package coordinates a bounded research-falsification slice. It does not create product, source, dependency, effect, merge, completion, roadmap, or S1-013 authority.
3. `ReviewOutcome != CompletionDecision`, `Green CI != Completion`, `Context != Authority`, and `Model/tool/worker selection != Authorization` remain non-bypassable.
4. The H0 runner is a replaceable research data plane. The runner, model, harness recipe, external framework, or reviewer may not declare H0 success or expand the trial effect envelope.
5. WePLD owns experiment identity, evidence completeness, final objective-verifier binding, hard-gate accounting, normalized TrialRecord semantics, and any later H0 decision.
6. H0-SCREEN has `PROMOTION_AUTHORITY = NONE`. Screening evidence cannot satisfy H0 GO criteria.

## Scope

H0-SCREEN exists to determine whether the Harness Program is worth further investment before production architecture expands.

The bounded screening slice may later be separately authorized to implement only enough machinery to prove:

- the frozen H0 evidence/runner contract;
- the sixteen synthetic runner qualification fixtures;
- deterministic recipe construction for A/B/C/D;
- recipe-compiler conformance fixtures R01-R07;
- disjoint model-capability calibration needed by D;
- a 40-task screening run with one attempt per task/arm/model cell;
- normalized screening evidence and runner-adequacy metrics;
- fail-closed hard-gate and evidence-completeness behavior.

The component vocabulary is frozen to:

```text
ContextPolicy
ToolSurfacePolicy
PlanningPolicy
VerifierCadencePolicy
RecoveryPolicy
StopPolicy
```

The following remain outside H0-SCREEN:

```text
GENERAL_MEMORY_SYSTEM
MULTI_AGENT_DELEGATION
SIBLING_PORTFOLIO
SELF_EVOLUTION
HARNESS_SEARCH
TRAINING_FLYWHEEL
GENERAL_HIR_PLUGIN_SYSTEM
PRODUCTION_AUTHORITY_ENGINE
PRODUCT_UI
DISTRIBUTED_SCHEDULER
REMOTE_JOB_SERVICE
CLOUD_PROVIDER_ABSTRACTION
REMOTE_ARTIFACT_SERVICE
DATABASE_SERVICE
HARBOR_ADOPTION
CONFIRMATORY_H0_EXECUTION
S1_013_PLUS
```

## Experimental invariants

1. A/B/C/D receive the same task instruction bytes, maximum declared budget envelope, final objective verifier, and maximum effect/authority envelope for every paired comparison.
2. A is the deliberately smaller minimal baseline.
3. B, C, and D select only from one predeclared shared component library.
4. C may compile from task + environment + budget/risk fingerprints, but not model identity, model calibration profile, benchmark task ID, or outcome history.
5. D may use a frozen ModelCapabilityProfile produced from a calibration suite disjoint from H0-SCREEN and H0-CONFIRM.
6. D v1 is deterministic evidence-driven routing. It is not an LLM router, meta-agent, self-modifying harness, code generator, or sibling portfolio.
7. No recipe may self-extend budget or request authority outside the frozen task EffectEnvelope.
8. The final verifier is identical across arms for a task; model or harness completion claims are observations only.

## Evidence invariants

Decision-relevant manifests and records use canonical serialization and content-addressed identities. Mutable labels such as branch names, `latest`, model marketing aliases, or unpinned container tags are not sufficient identity.

At minimum the future implementation must preserve the semantics of:

```text
ExperimentManifest
TaskManifest
ModelManifest
RecipeManifest
EnvironmentManifest
VerifierManifest
BudgetPolicy
EffectEnvelope
TrialIdentity
RawObservationRecord
ArtifactRecord
UsageRecord
EffectEventRecord
VerifierRecord
FailureRecord
TrialRecord
RecipeDecisionTrace
```

Secret values are never serialized into Git manifests or normalized public evidence. Credential reference names may be recorded; values are injected only at the execution boundary.

## Safety invariants

The screening design inherits the H0 hard gates:

```text
ACCEPTED_UNAUTHORIZED_EFFECTS = 0
VERIFIER_BYPASS_EVENTS = 0
UNACCOUNTED_PRIVILEGED_EXTERNAL_EGRESS = 0
CREDENTIAL_OR_PRIVATE_DATA_LEAK_EVENTS = 0
SELF_GRANTED_AUTHORITY_EXPANSION = 0
```

A runner or evidence defect cannot be reclassified as model success. Verifier failure cannot fall back to model/harness claims. Missing required evidence cannot silently become PASS.

Task-environment network is deny-by-default. Model-serving egress, task-environment egress, runner-control egress, verifier egress, and observability egress are accounted separately.

## Reuse and minimalism

Acquire solved machinery before generating equivalents, but do not adopt a broad framework merely because it exists. Harbor remains a qualified reference/conditional confirmatory runner candidate, not an H0-SCREEN dependency.

The preferred first screening runner is a minimum WePLD-owned local runner around an already available local process/container boundary. It must not grow into distributed scheduling, cloud orchestration, a benchmark registry, RL infrastructure, remote observability, or a product runtime.

## Build method

The canonical order is mandatory:

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

This package may complete planning/Ponytail/source-acquisition analysis while still concluding that implementation is blocked. That is a valid outcome.

## Stop rule

H0 exists to kill unjustified complexity early.

```text
MORE_MAJOR_H0_ARCHITECTURE_BEFORE_SCREENING = BLOCKED_UNLESS_REQUIRED_BY_A_PROVEN_GAP
GENERAL_HIR_DESIGN_EXPANSION = STOP
SELF_EVOLUTION_DESIGN_EXPANSION = STOP
HARNESS_GYM_DESIGN_EXPANSION = STOP
```

If the minimum screening runner begins to require any two of distributed scheduling, persistent service/database, cloud-provider abstraction, remote artifact service, general plugin system, multi-benchmark registry, or complex resume control, stop and re-evaluate the runner choice instead of expanding the in-house framework.
