# Ponytail FULL — Harness H0 Screening Falsification

```text
MODE = FULL
FEATURE = 002-harness-h0-screening
PROGRAM = WEPLD HARNESS PROGRAM
PHASE = H0-SCREEN
PONYTAIL_FULL = COMPLETE_FOR_PLANNING_REVIEW
IMPLEMENTATION_AUTHORITY = NO
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

Ponytail is applied here to the full H0-SCREEN flow, not to isolated implementation ideas. It may remove machinery, abstractions, services, dependencies, and convenience features; it may not remove identity, verifier independence, authority/effect limits, evidence completeness, isolation, cleanup, recovery, secret handling, deterministic testing, or review evidence.

## 1 — Does H0-SCREEN need to exist?

**YES, as a bounded falsification slice.**

The Harness research contracts already define a falsifiable thesis, A/B/C/D arms, hard gates, screening/confirmatory separation, evidence semantics, and a runner decision. Without H0-SCREEN, the project either stops before evidence or jumps directly into a large production Harness architecture.

The minimum useful next step is therefore not product integration. It is a controlled screening experiment that can kill or narrow the thesis cheaply.

## 2 — Does existing canonical WePLD machinery already solve H0-SCREEN?

**PARTLY, but not enough to run H0.**

Canonical WePLD already provides governance, exact-head integrity, trusted-bootstrap rules, build/review/egress policy, S1 Rust/runtime evidence, and a frozen Harness research contract. These should be reused as governance/evidence inputs.

It does not currently provide the H0-specific content-addressed experiment manifests, recipe compilers, runner/evidence finalizer, calibration suite, synthetic qualification fixtures, or normalized screening export.

Therefore H0 may add only the missing research machinery after separate authorization.

## 3 — Can the runner be only a thin local adapter?

**YES, initially.**

The preferred H0-SCREEN runner needs only to:

```text
load/validate frozen manifests
prepare isolated local task environment
launch one selected command
bound/observe execution
capture stdout/stderr/artifacts/usage/effects
invoke frozen objective verifier separately
finalize normalized evidence through WePLD-owned logic
clean up
support one fixed bounded local concurrency policy
```

It does not need a scheduler service, database, remote queue, cloud abstraction, plugin marketplace, benchmark registry, RL infrastructure, or hosted viewer.

## 4 — Does H0 need Harbor for screening?

**NO by default.**

Harbor is a strong qualified reference and conditional future runner candidate, but its broader evaluation/cloud/provider machinery is not required to falsify the first H0 thesis. H0-SCREEN should first measure whether a small local runner is adequate.

Harbor may be reconsidered only after the frozen runner switch criteria fire and a separate exact-pin qualification passes.

```text
HARBOR_SCREENING_DEPENDENCY = REJECT_DEFAULT
HARBOR_BEHAVIORAL_REFERENCE = KEEP
HARBOR_CONFIRMATORY_CANDIDATE = CONDITIONAL
```

## 5 — Does H0 need a generalized Harness Intermediate Representation?

**NO.**

H0 v1 requires only one small frozen vocabulary:

```text
ContextPolicy
ToolSurfacePolicy
PlanningPolicy
VerifierCadencePolicy
RecoveryPolicy
StopPolicy
```

Typed enums/config records are sufficient. A plugin graph, dynamic registry, general HIR, dependency-injection framework, or runtime extension marketplace would make the falsification slice harder to attribute and more expensive to kill.

```text
GENERAL_HIR = REJECT
PLUGIN_SYSTEM = REJECT
DYNAMIC_COMPONENT_LOADING = REJECT
```

## 6 — Does H0 need an LLM/meta-agent router?

**NO.**

D v1 exists specifically to test whether deterministic evidence-driven model-aware routing has value. Adding an LLM router introduces another stochastic model, cost, context leakage risk, and attribution problem.

```text
LLM_ROUTER = REJECT_H0_V1
META_AGENT_ROUTER = REJECT_H0_V1
MODEL_WRITES_RECIPE = REJECT
```

## 7 — Does H0 need memory or multi-agent delegation?

**NO.**

General memory and delegation are intentionally excluded from the canonical H0 component boundary. Their effects can be tested later only if the simpler static/adaptive recipe thesis earns continuation.

```text
GENERAL_MEMORY_SYSTEM = REJECT
MULTI_AGENT_DELEGATION = REJECT
SIBLING_PORTFOLIO = REJECT
```

## 8 — Does H0 need self-evolution, harness search, or training flywheel machinery?

**NO.**

Those mechanisms would change the experimental object during or between runs and make the first causal question harder to falsify.

```text
SELF_EVOLUTION = REJECT
HARNESS_SEARCH = REJECT
DYNAMIC_CODE_GENERATION = REJECT
TRAINING_FLYWHEEL = REJECT
AUTOMATIC_RECIPE_MUTATION = REJECT
```

## 9 — Does H0 need a database or persistent service?

**NO.**

Content-addressed manifests, append-oriented trial records, artifacts, and normalized exports can be retained as files/artifact bundles for screening. A database adds schema/service/recovery/locking/operational surface without being required by the 40-task screening design.

```text
DATABASE = REJECT
REMOTE_JOB_SERVICE = REJECT
REMOTE_ARTIFACT_SERVICE = REJECT
HOSTED_OBSERVABILITY = REJECT
```

If file/artifact retention later proves inadequate at confirmatory scale, that is a separate measured problem.

## 10 — Does H0 need a cloud-provider abstraction?

**NO.**

Screening is local-first. A narrow replaceable adapter to one qualified local process/container boundary is sufficient. Cloud execution is a future runner-selection concern, not a default H0-SCREEN feature.

```text
CLOUD_PROVIDER_ABSTRACTION = REJECT
CLOUD_PROVIDER_SDK = REJECT_DEFAULT
DISTRIBUTED_SCHEDULER = REJECT
```

## 11 — Does H0 need provider-specific model SDKs?

**NOT BY DEFAULT.**

The model boundary must be replaceable and record exact provider/model/settings/usage evidence. A provider SDK is justified only if it is the minimum qualified mechanism for an explicitly selected screening model set.

Prefer existing admitted or simple separately qualified interfaces before adding multiple provider SDKs.

```text
MULTI_PROVIDER_SDK_LAYER = REJECT_DEFAULT
SILENT_PROVIDER_FALLBACK = PROHIBITED
```

## 12 — Can cryptographic/content hashing be handwritten?

**NO.**

H0 relies on SHA-256 identities for decision-relevant evidence. Hand-writing a cryptographic hash implementation is unjustified and dangerous. Source Acquisition must select a mature commodity implementation or an already-qualified mechanism.

```text
CUSTOM_SHA256 = REJECT
COMMODITY_HASH_IMPLEMENTATION = QUALIFY
```

## 13 — Can manifest serialization/canonicalization be handwritten casually?

**NO.**

H0 needs deterministic canonical bytes, not merely “JSON that usually looks stable.” Typed serialization machinery may be reused, but WePLD must own and test canonicalization rules, map/key ordering, unsupported values, normalization, and domain separation.

```text
AD_HOC_DYNAMIC_JSON_MAPS = REJECT
TYPED_SERIALIZATION = PREFERRED_CANDIDATE
WEPLD_CANONICALIZATION_RULES = REQUIRED
```

## 14 — Can synthetic qualification fixtures be tiny scripts?

**YES, when they are frozen untrusted inputs.**

F01-F16 are test stimuli, not authority. A minimal script/executable is preferable when it produces the intended deterministic crash/timeout/output/secret/network behavior more simply than product-like code.

Fixture bytes and expected behavior must be frozen and content-addressed. Fixture language does not become an H0 runtime dependency by implication.

## 15 — What custom WePLD-owned code remains justified?

Minimum justified H0 custom logic, after Source Acquisition and implementation authorization:

```text
canonical serialization rules
manifest validation
content-addressed identities / TrialIdentity
trial state machine
A/B recipe construction
C deterministic compiler
D deterministic model-profile compiler
RecipeDecisionTrace
calibration-profile derivation
runner adapter boundary
append-oriented evidence collection
objective-verifier binding
evidence completeness / hard-gate finalization
normalized screening export
runner-adequacy computation
```

These are H0 experiment semantics and should remain WePLD-owned even when execution machinery is replaced.

## 16 — Anti-complexity threshold

If the proposed “minimal” runner begins to require any two of:

```text
distributed scheduler
persistent service/database
cloud-provider abstraction
remote artifact server
general plugin system
multi-benchmark registry
complex resume controller
```

stop implementation expansion and reopen the runner decision rather than continuing to build infrastructure.

## 17 — Non-reducible controls

Ponytail MUST NOT remove:

- canonical content-addressed manifest identity;
- domain-separated TrialIdentity;
- exact recipe identity and decision trace;
- disjoint D calibration;
- shared B/C/D component library;
- same paired effect/budget/final-verifier boundaries;
- objective verifier independence;
- evidence completeness state;
- original failed/incomplete trial retention;
- hard-gate accounting;
- task/model/provider/runner identities;
- secret-value exclusion from Git/public evidence;
- task-network deny-by-default where claimed;
- workspace/process cleanup/isolation;
- F01-F16 and R01-R07 gates;
- runner adequacy thresholds;
- deterministic and independent review evidence.

## 18 — Current dependency dispositions

| Candidate class | Ponytail disposition | Current authority |
|---|---|---|
| Rust toolchain for trusted H0 control/evidence | REUSE/QUALIFY | NOT YET H0-ADMITTED |
| typed serialization | QUALIFY MINIMUM COMMODITY SET | NOT ADMITTED |
| SHA-256 implementation | QUALIFY COMMODITY IMPLEMENTATION | NOT ADMITTED |
| local process primitives | STDLIB-FIRST | IMPLEMENTATION NOT AUTHORIZED |
| local container/runtime boundary | REUSE EXISTING EXTERNAL MACHINERY VIA NARROW ADAPTER | EXACT IDENTITY NOT YET QUALIFIED |
| provider SDKs | REJECT DEFAULT | NONE |
| Harbor | REFERENCE / CONDITIONAL FUTURE RUNNER | NO SCREENING ADMISSION |
| database/service/UI | REJECT | NONE |
| HIR/plugin framework | REJECT | NONE |
| self-evolution/search/training machinery | REJECT | NONE |

## Gate conclusion

```text
PONYTAIL_FULL = COMPLETE_FOR_PLANNING_REVIEW
MINIMUM_H0_SCREEN_ARCHITECTURE = BOUNDED
SOURCE_ACQUISITION_CHECK = OPEN
H0_SCREEN_IMPLEMENTATION = BLOCKED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
S1_013_PLUS = NOT_STARTED
```

Ponytail must be revalidated against exact acquisition results before the future implementation boundary is authorized. A dependency/runtime constraint discovered during acquisition may justify further reduction or a narrowly evidenced reopening; it does not silently authorize more machinery.
