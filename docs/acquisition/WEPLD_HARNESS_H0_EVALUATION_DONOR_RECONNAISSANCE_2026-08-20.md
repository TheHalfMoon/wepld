# WePLD Harness Program — H0 Evaluation Donor Reconnaissance

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / DONOR RECONNAISSANCE
CAPABILITY = EVALUATION / PAIRED HARNESS EFFECTS
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
RUNTIME_ADOPTION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## 1. Purpose

This document narrows the H0 evaluation capability to three research donors only and records exact inspected revisions, rights evidence, useful mechanics, risks, and WePLD acquisition boundaries.

This is not a source-admission record.

```text
DONOR_DISCOVERY != SOURCE_ADMISSION
LICENSE_FOUND != DEPENDENCY_ADMISSION
REFERENCE_VALUE != ARCHITECTURE_AUTHORITY
EXPERIMENT_TOOL_CANDIDATE != PRODUCT_DEPENDENCY
```

The governing H0 quantitative contract is:

`docs/acquisition/WEPLD_HARNESS_H0_THESIS_TOURNAMENT_CONTRACT_2026-08-20.md`

## 2. Capability objective

The exact capability under reconnaissance is:

> Run paired model×harness experiments over reproducible tasks and environments, retain exact run/artifact identities, separate objective completion from diagnostic process analysis, and compute auditable success/efficiency/failure evidence without allowing the evaluation substrate to become completion or effect authority.

The minimum falsification surface needs:

```text
TASK_IDENTITY
ENVIRONMENT_IDENTITY
MODEL_IDENTITY
HARNESS_RECIPE_IDENTITY
BUDGET_IDENTITY
TRIAL_IDENTITY
OBJECTIVE_VERIFIER_IDENTITY
RAW_ARTIFACT_RETENTION
TOKEN/COST/LATENCY ACCOUNTING
FAILURE_CLASSIFICATION
PAIRED_ANALYSIS
REPRODUCIBLE_MANIFESTS
```

## 3. Selected donors

Exactly three donors are retained for this capability round:

```text
D1 = harbor-framework/harbor
D2 = Qihoo360/harness-bench
D3 = namanvats/scaffold-effects
```

No fourth donor is admitted to this reconnaissance unless a concrete missing capability is identified.

## 4. D1 — Harbor

### 4.1 Exact inspected pin

```text
REPOSITORY = harbor-framework/harbor
DEFAULT_BRANCH = main
INSPECTED_COMMIT = 2fe1615503fed39ad82b7ce09b22497996b30f1f
INSPECTED_TREE = 9bea05fa72ea12d90910a1cacf790894c6102770
PIN_DATE = 2026-08-20
ARCHIVED = NO
```

This pin is an inspection identity, not a moving `main` dependency.

### 4.2 Rights

At the inspected pin:

```text
LICENSE = Apache-2.0
LICENSE_FILE = LICENSE
LICENSE_BLOB = 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64
PYPROJECT_LICENSE = Apache-2.0
```

Any future reuse must preserve the applicable Apache-2.0 license/notice obligations and provenance. This document does not perform a full NOTICE/transitive-license review.

### 4.3 Relevant behavior

Harbor exposes a clean evaluation vocabulary:

```text
Task
Dataset
Agent
Container Environment
Trial
Job
```

Relevant mechanics:

- a task binds instruction + environment + test script;
- datasets group tasks;
- agents integrate behind base interfaces;
- environments integrate behind a common environment interface;
- trials represent one task attempt;
- jobs expand into many trial configurations and support parallel evaluation;
- arbitrary agents and benchmarks can be integrated;
- containerized execution is a first-class assumption.

### 4.4 Strong donor value

Retain as an oracle for:

```text
TASK/DATASET/TRIAL/JOB IDENTITY SEPARATION
AGENT ADAPTER BOUNDARY
ENVIRONMENT ADAPTER BOUNDARY
CONTAINERIZED EVALUATION
RUN MANIFEST EXPANSION
PARALLEL TRIAL ORCHESTRATION
ARTIFACT/RESULT RETENTION PATTERNS
NETWORK-POLICY TEST IDEAS
```

### 4.5 Dependency / security surface

The inspected project declares a broad default dependency surface including model-routing, HTTP/API, web-server, auth/token, storage, and configuration packages, with many optional cloud/sandbox providers.

The project also contains explicit network-policy examples and cloud execution paths.

Therefore:

```text
H0_VENDOR_HARBOR_WHOLESALE = NO
H0_PRODUCT_DEPENDENCY = NO
H0_DEFAULT_CLOUD_EXTRAS = NO
H0_UNCONTROLLED_NETWORK = NO
```

### 4.6 Preferred WePLD use

Initial preference:

```text
ROLE = BEHAVIORAL_ORACLE + POSSIBLE_ISOLATED_EXTERNAL_RESEARCH_RUNNER
INTEGRATION = BEHIND_WEPLD_OWNED_EXPERIMENT_MANIFESTS
LOCAL_CONTAINER_MODE_FIRST = YES
CLOUD_PROVIDER_REQUIRED_FOR_H0 = NO
```

If direct Harbor execution is later needed, qualify a pinned research-tool use separately. Do not make Harbor's internal abstractions the WePLD HIR or product authority plane.

### 4.7 Exit path

WePLD must retain enough of its own experiment schema that Harbor can be replaced by another runner without changing H0 evidence semantics.

Required WePLD-owned boundary:

```text
ExperimentManifest
TaskManifest
ModelManifest
RecipeManifest
EnvironmentManifest
VerifierManifest
TrialRecord
ArtifactIndex
MetricRecord
FailureRecord
```

## 5. D2 — Harness-Bench

### 5.1 Identity verification

The official Harness-Bench project site for arXiv:2605.27922 links its `GitHub Repository` / `Evaluation Kit` to:

```text
REPOSITORY = Qihoo360/harness-bench
DEFAULT_BRANCH = main
INSPECTED_COMMIT = 1025086a446653702b80cfb48babbeec35db6b2c
INSPECTED_TREE = 49208501704f1d7e2ada03800ac14621f760e1b6
PIN_DATE = 2026-08-20
```

### 5.2 Rights status — blocked for code reuse

At the inspected commit, repository-root enumeration contains no `LICENSE` file, and the inspected `pyproject.toml` contains no project license declaration.

Therefore:

```text
CODE_REUSE_RIGHTS = NOT_ESTABLISHED_FROM_REPOSITORY
SOURCE_COPY = BLOCKED
VENDORING = BLOCKED
DEPENDENCY_ADOPTION = BLOCKED
BEHAVIORAL_REFERENCE = ALLOWED_AS_PUBLIC_RESEARCH_REFERENCE
```

Founder-reported broad permission does not replace per-source rights evidence required by WePLD governance.

Before any code reuse, obtain explicit repository/project rights evidence sufficient for the intended use and record attribution/redistribution requirements.

### 5.3 Relevant behavior

The repository demonstrates a useful task shape:

```text
tasks/<task_id>/
  task.yaml
  prompt.txt
  fixtures/
  oracle_grade.py
```

It also records adapter execution, token usage, workspace artifacts, oracle results, process diagnostics, and security rubric signals.

### 5.4 Strong donor value

Retain as a behavioral oracle for:

```text
OFFLINE REAL-WORKSPACE TASK FIXTURES
PROGRAMMATIC ORACLE PER TASK
ADAPTER-NEUTRAL TASK EXECUTION
USAGE/TOKEN ACCOUNTING
TRACE RETENTION
OUTCOME VS PROCESS DIAGNOSTIC SEPARATION
TASK-LOCAL GRADER STRUCTURE
```

### 5.5 Important negative oracle

The inspected README describes a composite score where process/security components may be LLM-rubric-derived and where fallback behavior can make outcome accounting non-obvious when no usable outcome/quality exists.

WePLD H0 must **not** copy this as completion semantics.

```text
WEPLD_FINAL_ACCEPTANCE = OBJECTIVE_VERIFIER_FIRST
LLM_PROCESS_RUBRIC = DIAGNOSTIC_ONLY
MISSING_OBJECTIVE_OUTCOME = NOT_AUTOMATIC_SUCCESS
SECURITY_RUBRIC_MODEL_OUTPUT = NOT_EFFECT_AUTHORITY
```

This negative oracle is as important as the task-format inspiration.

### 5.6 Preferred WePLD use

```text
ROLE = TASK/ORACLE/TRACE DESIGN REFERENCE ONLY
CODE_IMPORT = NO
DEPENDENCY = NO
```

Reimplement any needed pattern under a WePLD-owned schema rather than copying repository code until rights are proven.

## 6. D3 — Scaffold Effects

### 6.1 Exact inspected pin

```text
REPOSITORY = namanvats/scaffold-effects
DEFAULT_BRANCH = main
INSPECTED_COMMIT = ed8014f42a13483379d76ad2732a40132c1becf9
INSPECTED_TREE = b5bcef7c6e0bafcc2fd0ba3aea261f7b03b51946
PIN_DATE = 2026-08-20
ARCHIVED = NO
```

### 6.2 Rights

At the inspected pin:

```text
LICENSE = MIT
LICENSE_FILE = LICENSE
LICENSE_BLOB = 934f7d42d36bb45da4dbb20f276500d4364d0ba9
COPYRIGHT = Naman Vats, 2026
```

Any reused substantial code must preserve the copyright and permission notice.

### 6.3 Relevant behavior

The repository publishes:

- exact harness configuration files;
- system prompts;
- a selected evaluation task subset;
- raw trial result trees;
- frozen aggregate snapshots;
- per-trial records;
- Harbor-result readers;
- trajectory metrics;
- failure categories;
- analysis code and archived dataset citation.

Its README records a 50-task × 2-model × 3-harness study with common task images/turn budgets and metrics including solved status, turns, tokens, no-progress behavior, and failure categories.

### 6.4 Strong donor value

Retain as an oracle for:

```text
EXACT_HARNESS_CONFIG_AS_EXPERIMENT_VARIABLE
RAW_TRIAL_RETENTION
FROZEN_ANALYSIS_SNAPSHOT
PER_TRIAL_JSONL_STYLE RECORDS
NO_PROGRESS METRICS
FAILURE TAXONOMY
TOKENS_PER_SOLVED ACCOUNTING
PROVENANCE FROM RAW RUN TREE -> AGGREGATE
REPRODUCIBLE ANALYSIS PACKAGE
```

### 6.5 Dependency / egress caveat

The inspected `pyproject.toml` declares:

```text
harbor[daytona]>=0.4.0
```

The reproduction README instructs use of OpenRouter and Daytona credentials.

Therefore:

```text
H0_ADOPT_SCAFFOLD_EFFECTS_RUNTIME_STACK = NO
H0_REQUIRE_DAYTONA = NO
H0_REQUIRE_OPENROUTER = NO
H0_COPY_CREDENTIAL_FLOW = NO
```

The initial WePLD H0 experiment should prefer local/offline container execution where possible and independently govern any provider egress.

### 6.6 Preferred WePLD use

```text
ROLE = ANALYSIS/PROVENANCE/METRIC ORACLE
CODE_IMPORT_NOW = NO
DEPENDENCY_NOW = NO
POSSIBLE_LATER_REUSE = SMALL_ANALYSIS_MECHANICS_ONLY_IF_IT_REDUCES_RISK_OR_EFFORT
```

Prefer reimplementing the H0 paired bootstrap and evidence schema directly from the preregistered WePLD contract so the analysis is not coupled to one paper's runtime assumptions.

## 7. Cross-donor synthesis

The three donors suggest a minimal WePLD-owned evaluation boundary:

```text
                 WEPLD H0 CONTROL
                       |
             Frozen ExperimentManifest
                       |
        +--------------+--------------+
        |                             |
   Execution Runner              Evidence Plane
        |                             |
 task/env/agent adapter       raw trials + artifacts
        |                     verifier outcomes
 sandbox/container            usage/cost/latency
        |                     failure records
        +--------------+--------------+
                       |
              Paired Analysis
                       |
              H0 Decision Rules
```

The runner is replaceable. The evidence schema and promotion rules are WePLD-owned.

## 8. Minimum H0 evaluation interface hypothesis

Without authorizing implementation, the research contract should eventually be satisfiable by a small interface similar to:

```text
ExperimentRunner
- prepare(task, environment, recipe, model, budget)
- execute(trial_identity)
- collect_artifacts()
- collect_usage()
- finalize_trial_record()

ObjectiveVerifier
- verify(task_identity, artifact_identity)
- emit deterministic outcome/evidence

EvidenceStore
- append immutable trial record
- index artifacts by hash
- expose raw records for analysis

PairedAnalyzer
- validate manifest pairing
- compute frozen metrics
- perform paired task bootstrap
- derive H0 decision mechanically
```

This interface is a research hypothesis only. It is not HIR, runtime, or product authority.

## 9. Acquisition priority decision

```text
D1_HARBOR = RETAIN_HIGH_PRIORITY_REFERENCE
D1_CODE_IMPORT_NOW = NO
D1_RESEARCH_RUNNER_CANDIDATE = YES_SEPARATELY_QUALIFIED

D2_HARNESS_BENCH = RETAIN_HIGH_PRIORITY_BEHAVIORAL_REFERENCE
D2_CODE_IMPORT = BLOCKED_RIGHTS_NOT_ESTABLISHED

D3_SCAFFOLD_EFFECTS = RETAIN_HIGH_PRIORITY_ANALYSIS_REFERENCE
D3_CODE_IMPORT_NOW = NO
D3_SMALL_ANALYSIS_REUSE_CANDIDATE = YES_IF_LATER_JUSTIFIED
```

No donor becomes a dependency merely because it is retained.

## 10. What WePLD should build itself if H0 implementation is later authorized

Prefer WePLD-owned minimal code for:

```text
manifest hashing
run identity
arm/recipe identity
verifier identity binding
artifact hashing/index
failure classification contract
hard authority event accounting
paired bootstrap analysis
H0 decision derivation
```

These semantics are central to WePLD's falsification and trust model and should not be delegated to a donor framework.

## 11. What may be delegated to a replaceable runner

Potentially replaceable implementation details:

```text
container lifecycle
parallel trial scheduling
adapter process invocation
benchmark fixture materialization
basic stdout/stderr capture
resource metering plumbing
```

Even when delegated, WePLD must independently bind resulting evidence to exact identities.

## 12. Current decision

```text
CAPABILITY_RECONNAISSANCE = COMPLETE_FOR_INITIAL_H0_SET
DONORS_SELECTED = 3
EXACT_REPOSITORY_PINS = RECORDED
RIGHTS_STATUS = RECORDED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
RUNTIME_ADOPTION = NONE
H0_EXPERIMENT_EXECUTION = NOT_STARTED
S1_013_PLUS = NOT_STARTED
```

Next research gate:

> Specify the minimum WePLD-owned H0 evidence/runner contract and falsification implementation boundary before choosing whether Harbor is needed as an external research runner at all.
