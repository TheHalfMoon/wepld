# WePLD Harness Program — Architecture and Falsification Dossier

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = RESEARCH / ARCHITECTURE / FALSIFICATION
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_MUTATION = NONE
S1_013_PLUS = NOT_STARTED
```

## Executive thesis

WePLD should not compete by building another feature-rich coding-agent loop.

The target position is:

> **WePLD is the trusted execution system that finds the best way for a model to work, measures whether the harness actually improved that model, and promotes harness changes only through independently checkable evidence.**

The Harness Program therefore treats effective agent capability as a function of more than model weights:

```text
EffectiveCapability = f(
  model,
  task,
  environment,
  context policy,
  tool surface,
  loop policy,
  memory,
  delegation,
  recovery,
  verification,
  authority,
  budget
)
```

No claim is made that harness engineering can remove the intrinsic capability ceiling of a weak checkpoint. The research question is narrower and falsifiable: can WePLD systematically extract more **verified useful work** from the same model under controlled task, cost, latency, and risk budgets?

## Product-level differentiation

Existing harness work spans several strong schools:

- **Minimal harnesses**: aggressively small loops and tool surfaces that avoid scaffold overhead.
- **Composable harnesses**: replaceable services/plugins/ports/atoms/recipes.
- **Adaptive harnesses**: route context, tools, loops, memory, or workers according to model/task/environment state.
- **Self-evolving harnesses**: learn harness edits from failures and rerun evidence.
- **Model↔harness co-evolution**: use harness search to generate verified training data, then improve the model and recalibrate the harness.

WePLD's intended novelty is not merely another atom catalog or another meta-agent. It is the combination of adaptive harness intelligence with a non-self-authorizing trusted authority plane.

```text
                    WePLD HARNESS
                         │
          ┌──────────────┴──────────────┐
          │                             │
 ADAPTIVE INTELLIGENCE PLANE      TRUSTED AUTHORITY PLANE
          │                             │
 model routing                   effect authority
 context compilation             process ownership
 tool selection                  filesystem boundaries
 planning                        network boundaries
 memory                          identity
 subagents                       approvals
 recovery                        evidence capture
 harness optimization            verifier enforcement
          │                             │
          └──────────────┬──────────────┘
                         ↓
                VERIFIED EXECUTION
```

Adaptive components may propose behavior and harness mutations. They may not grant themselves new filesystem/process/network/credential/merge/deploy/publish/acceptance authority.

## Core design principles

```text
WEPLD_HARNESS_PRINCIPLE_1
No model, task, environment, or budget is assumed to have one universally optimal harness.

WEPLD_HARNESS_PRINCIPLE_2
Harness complexity must earn its place through measured verified lift.

WEPLD_HARNESS_PRINCIPLE_3
Adaptive components may propose behavior; they may not expand their own authority.

WEPLD_HARNESS_PRINCIPLE_4
A harness mutation is not an improvement until paired evidence demonstrates benefit without violating its regression and authority envelope.

WEPLD_HARNESS_PRINCIPLE_5
Deterministic/verifiable evidence is preferred to model confidence whenever an objective verifier exists.

WEPLD_HARNESS_PRINCIPLE_6
The model does not own DONE. Completion belongs to WePLD acceptance/verification semantics.

WEPLD_HARNESS_PRINCIPLE_7
A donor mechanism is retained only if it improves an accepted objective and remains replaceable behind WePLD-owned contracts.
```

## Competitive synthesis

The current Harness Program donor inventory is maintained separately in:

`docs/acquisition/HARNESS_PROGRAM_DONOR_CANDIDATES_2026-08-20.md`

Research conclusions to preserve:

- DeepSeek Harness is a primary oracle for plugin-tree composition, capability seams, durable session/event behavior, and route-aware context/compaction.
- HELIX is the strongest overlap risk for generic `ports + atoms + recipes + harness search`; therefore those concepts alone are not sufficient differentiation for WePLD.
- Agentic Harness Engineering (AHE) is a primary oracle for observable and falsifiable evaluate→analyze→improve loops.
- Harness-R1 is a primary oracle for learning executable runtime patches from failure trajectories and rewarding them with actual reruns of a frozen target.
- mini-SWE-agent is a critical negative oracle against unnecessary harness complexity.
- OpenHands, OpenAI Agents SDK, OpenCode, Pi Mono, Deep Agents, and CheetahClaws are valuable behavior/interoperability/runtime references, not automatic architectural authorities.
- Harbor, Harness-Bench, Scaffold Effects, and verifier-grounded research are candidates for evaluation methodology and controlled paired experiments.
- HELIX/Co-Harness-style model↔harness data loops are later-stage opportunities, not a prerequisite for proving the core Harness thesis.

Exact repository/paper revisions must be pinned before code-level acquisition or publication-grade claims.

## Primary abstraction — Proof-Carrying Harness Recipe

A WePLD harness configuration should not be treated as trusted merely because a human or meta-agent wrote it.

The intended compiled unit is a **Proof-Carrying Harness Recipe**.

Conceptual schema:

```text
HarnessRecipe
├── recipe_identity
├── recipe_version
├── provenance
├── model_fingerprint
├── task_fingerprint
├── environment_fingerprint
├── objective
├── context_policy
├── tool_surface
├── loop_policy
├── memory_policy
├── delegation_policy
├── recovery_policy
├── verifier_plan
├── effect_authorities
├── resource_budget
│   ├── token_budget
│   ├── money_budget
│   ├── latency_budget
│   ├── process_budget
│   └── external-egress_budget
├── stop_conditions
├── expected_lift
├── expected_task_flips
├── known_regressions
├── regression_envelope
├── evidence_requirements
└── promotion_evidence
```

A proposed recipe is not canonical merely because it parses or achieves one benchmark success.

Intended promotion flow:

```text
Recipe proposal
   ↓
schema validation
   ↓
authority/effect validation
   ↓
paired evaluation
   ↓
regression evaluation
   ↓
security / egress accounting
   ↓
independent verification/review
   ↓
promotion evidence
   ↓
canonical harness profile
```

## Harness Intermediate Representation (HIR)

The Harness Program should eventually define a WePLD-owned HIR rather than adopting a donor's internal plugin model wholesale.

Candidate atom classes:

```text
ContextAtom
ToolAtom
MemoryAtom
PlannerAtom
VerifierAtom
RouterAtom
RecoveryAtom
DelegationAtom
CompactionAtom
AcceptanceAtom
SandboxAtom
PermissionAtom
ObservationAtom
```

Every HIR unit should expose more than input/output type compatibility.

Conceptual contract:

```text
HarnessComponentContract
- stable identity/version
- inputs
- outputs
- required capabilities
- produced capabilities
- requested effects
- required authority
- failure modes
- fallback semantics
- cost model
- latency model
- compatibility constraints
- deterministic conformance tests
- provenance
- evidence requirements
- replacement/exit path
```

The purpose is to prevent an untyped plugin soup where composition success is confused with safe or useful execution.

## Model Capability Profiler

WePLD should empirically characterize how a model behaves inside an agent loop instead of relying only on provider metadata.

Candidate profile:

```text
ModelCapabilityProfile
- tool_call_reliability
- parallel_tool_reliability
- structured_output_reliability
- shell_fluency
- patch_accuracy
- effective_context_window
- long_context_degradation_curve
- instruction_retention
- planning_gain
- verifier_gain
- reflection_gain
- subagent_gain
- compaction_sensitivity
- tool_schema_sensitivity
- retry_signature
- no_progress_signature
- latency_distribution
- token_cost_curve
- preferred_tool_granularity
- preferred_context_density
- preferred_turn_budget
- preferred_verification_cadence
```

This profile is measured evidence, not a static reputation score.

A model may empirically prefer typed tools, bash-only execution, smaller tool schemas, more aggressive verification, less reflection, more context retention, or a different delegation policy. The harness router should be allowed to choose differently per model when evidence supports it.

## Task and environment fingerprinting

Harness selection also depends on the work itself.

Candidate task/environment features:

```text
TaskFingerprint
- task_class
- expected mutation surface
- language/toolchain
- repository scale
- test availability
- verifier availability
- uncertainty
- expected horizon
- security sensitivity
- external-service requirements
- reversibility
- concurrency suitability

EnvironmentFingerprint
- OS/platform
- shell/runtime availability
- sandbox/containment availability
- filesystem semantics
- network policy
- credential availability
- CPU/RAM/GPU budget
- package/build tools
- deterministic verifier availability
```

A small local bug should not automatically receive the same topology as a repository-scale migration, security investigation, or long-horizon refactor.

## Adaptive Harness Router

Intended selection model:

```text
TaskFingerprint
      +
ModelFingerprint
      +
EnvironmentFingerprint
      +
Budget/Risk Envelope
      ↓
Harness Router
      ↓
Proof-Carrying Harness Recipe
```

Examples:

```text
small local bug
→ minimal shell/file loop
→ focused tests
→ completion verifier

large migration
→ exploration
→ plan
→ selective parallel evidence workers
→ implementation
→ deterministic verifier fabric
→ bounded repair
→ acceptance

security-sensitive change
→ read-only discovery
→ threat model / source→sink reasoning
→ sandboxed validation where applicable
→ deterministic security gates
→ independent review
→ no autonomous authority expansion
```

The router must be able to choose **less machinery**, not merely more machinery.

## Adaptive Context Compiler

Context handling should be treated as compilation, not just truncation or summarization.

Candidate per-turn plan:

```text
ContextPlan
- immutable invariants
- active task/goal
- current exact evidence
- changed artifacts
- unresolved failures
- relevant durable memory
- tool outputs needed now
- historical decisions
- compacted trajectory
- omitted-but-recallable references
- token budget allocation
```

Each context item should support policies such as:

```text
KEEP_EXACT
SUMMARIZE
REFERENCE
REHYDRATE_ON_DEMAND
OFFLOAD_TO_ARTIFACT
MOVE_TO_SUBAGENT
DROP_IF_PROVEN_IRRELEVANT
```

A useful research metric is `context_value_per_token`, estimated through controlled ablations rather than guessed from recency alone.

## Tool Surface Compiler

The harness should not send the entire global tool registry to every model turn.

Target flow:

```text
current task state
   ↓
tool relevance selection
   ↓
capability + authority + risk filter
   ↓
model-specific tool representation
   ↓
minimum useful turn tool surface
```

Possible outputs range from `bash + read + edit` to richer typed tools, depending on model/task evidence.

Research questions:

- Does shrinking the tool surface improve success or reduce tokens for this model?
- Does the model perform better with high-level typed tools or shell primitives?
- Does parallel tool use improve completion or induce ordering/tool-call errors?
- When should a tool be deferred until a capability becomes relevant?

## Verifier Fabric

A central Harness Program thesis is that output quality should be anchored to objective evidence whenever possible.

Candidate verifier resolver:

```text
Claim / intended completion
   ↓
Verifier Resolver
   ├── compiler
   ├── formatter/linter/type checker
   ├── unit tests
   ├── integration tests
   ├── contract tests
   ├── schema validation
   ├── Git diff/path invariants
   ├── runtime probes
   ├── benchmark-specific verifier
   ├── dependency/license/SBOM checks
   ├── security gates
   └── model-based evaluator only when objective evidence is unavailable
```

This enables **Proof-Carrying Completion**:

```text
COMPLETION_CLAIM
- exact artifact identity
- verifier identities
- verifier outcomes
- unresolved claims
- residual limitations
- authority/effect accounting
```

A model's statement `done` is never itself completion evidence.

## Failure Intelligence Engine

Every failure trajectory should produce structured diagnostic evidence rather than being discarded as a failed run.

Candidate taxonomy:

```text
CONTEXT_LOSS
CONTEXT_OVERLOAD
TOOL_SCHEMA_CONFUSION
TOOL_SELECTION_FAILURE
TOOL_EXECUTION_FAILURE
NO_PROGRESS_LOOP
BAD_PLAN
BAD_DECOMPOSITION
REPEATED_PATCH_REGRESSION
VERIFIER_MISUSE
VERIFICATION_GAP
AUTHORITY_DENIED
ENVIRONMENT_FAILURE
DEPENDENCY_FAILURE
MODEL_PROVIDER_FAILURE
RECOVERY_FAILURE
BUDGET_EXHAUSTION
```

Candidate output:

```text
FailureRecord
- failure_class
- evidence
- last_good_state
- first_bad_transition
- model_contribution
- harness_contribution
- environment_contribution
- recoverability
- recommended bounded intervention class
- whether retry-with-same-recipe is justified
```

The key question is not just `why did the model fail?` but `which failure belongs to model capability, harness design, verifier design, or environment?`

## Harness Portfolio

One globally best recipe may not exist.

The system should support two modes:

```text
ROUTED_SINGLE_RECIPE
TaskFingerprint → learned best recipe

BOUNDED_SIBLING_PORTFOLIO
low router confidence / high-value task
→ execute N diverse admissible recipes
→ verify each
→ select verified winner
```

Portfolio execution must be explicit about cost, latency, authority, and duplicated effects. Unsafe or irreversible effectful siblings must not race without a separately safe execution design.

## Harness Gym

The Harness Gym is the proposed controlled optimization laboratory.

Conceptual CLI:

```bash
wepld harness optimize \
  --model <model> \
  --suite <task-suite> \
  --budget <budget> \
  --objective verified-success-per-dollar
```

Conceptual loop:

```text
calibrate model
→ establish baseline
→ classify failure fingerprints
→ generate bounded candidate recipes
→ run paired trials
→ reject regressions
→ discover Pareto frontier
→ freeze evidence-backed profile
```

Explanatory output should be first-class:

```text
For this model/task family:
- planner: beneficial / neutral / harmful
- verifier cadence: measured gain
- tool surface: selected size and rationale
- context retention: selected policy
- subagents: enabled only for defined classes
- reflection: enabled/disabled based on evidence
- cost and latency effects
- known regression classes
```

## Governed Harness Evolution

Self-evolution is deliberately not v1.

When introduced, the Harness Engineer must propose **candidate mutations only**.

```text
Canonical Harness
      │
      ├── trajectories
      ├── failures
      └── metrics
            ↓
      Harness Engineer
            ↓
      candidate mutation
            ↓
      shadow / paired evaluation
            ↓
      regression matrix
            ↓
      independent verification
            ↓
      governance gate
            ↓
      PROMOTE or REJECT
```

Each proposed mutation should state before evaluation:

```text
WHY_CHANGE
FAILURE_EVIDENCE
ROOT_CAUSE_HYPOTHESIS
TARGETED_FIX
EXPECTED_GAIN
EXPECTED_TASK_FLIPS
REGRESSION_RISK
EXPECTED_MODEL_FAMILIES
AUTHORITY_DELTA = NONE unless separately authorized
```

The prediction must be falsifiable by the next evaluation round.

### Non-self-authorization invariant

```text
HARNESS_ENGINEER_CAN_PROPOSE = YES
HARNESS_ENGINEER_CAN_SELF_PROMOTE = NO
HARNESS_ENGINEER_CAN_EXPAND_AUTHORITY = NO
HARNESS_ENGINEER_CAN_OVERRIDE_VERIFIERS = NO
HARNESS_ENGINEER_CAN_DECLARE_COMPLETION = NO
```

## Model ↔ Harness flywheel

Later-stage opportunity:

```text
Harness optimization
→ sibling rollouts
→ deterministic/verifier labels
→ trace and patch audit
→ training examples
→ stronger model/router/critic
→ model recalibration
→ harness optimization
```

Potential datasets:

```text
SFT positives
near misses
regression-aware negatives
preference pairs
failure classifier examples
tool-router examples
context-selection examples
verifier-selection examples
recovery-policy examples
```

This stage must not be started before the static/adaptive harness thesis has demonstrated reproducible lift.

## Product modes

Possible user-facing modes:

```text
wepld fast
- low overhead
- minimal recipe
- bounded verification
- optimized for latency/cost

wepld adaptive
- dynamic context/tools
- selective planning/delegation
- recovery and verification
- default intelligent mode

wepld max
- bounded sibling recipe portfolio
- stronger search/verification
- higher compute budget
- intended for high-value tasks
```

These names are research placeholders, not approved product naming.

## WePLD Lift

`WEPLD_LIFT` should be a product/research primitive, not a single leaderboard score.

Candidate vector:

```text
verified_success_delta
cost_per_verified_success_delta
tokens_per_verified_success_delta
latency_delta
human_intervention_delta
no_progress_turn_delta
regression_delta
unsafe_action_delta
verification_coverage_delta
context_loss_delta
recovery_success_delta
```

Example report shape only:

```text
Model X / Task Family Y

Baseline Harness
Verified success      <measured>
Tokens / solved       <measured>
Median latency        <measured>

WePLD Adaptive
Verified success      <measured>
Tokens / solved       <measured>
Median latency        <measured>

WEPLD LIFT
<computed deltas>
```

No illustrative number is evidence. All published lift must come from reproducible paired runs with exact model, harness, task, environment, verifier, and budget identities.

## Roadmap mapping hypothesis

This dossier does **not** change canonical S1–S10.

The Harness Program can potentially unify existing slices rather than create a parallel product:

```text
S4  Fehrest / Project Brain
    → durable context and memory substrate

S5  Spec Kit + AGILLE + Plan Qualification + Ponytail
    → task/goal compilation + minimum-sufficient harness principle

S6  UWC + Mirefa + Edara
    → normalized worker edge + route qualification + minimum-sufficient topology

S7  Native Review & Assurance
    → Verifier Fabric

S8  Controlled Repair + bounded fallback/reassignment + Trusted Completion
    → Failure Intelligence + governed recovery

S9  Quality Passport + Recovery Time Machine + ChangeUnit/Delivery evidence
    → proof-carrying execution/completion evidence

S10 Fehrest expansion + Byan analytics
    → lift analytics, failure fingerprints, learning candidates
```

A future roadmap revision may make this relationship explicit only after the canonical ledger sequence is complete and the Harness thesis passes falsification gates.

## Donor mining strategy

For each concrete Harness capability, apply Ponytail FULL:

1. define the exact capability and measurable objective;
2. select only the strongest 2–3 donors for that capability;
3. pin exact revisions;
4. inspect implementation, tests, failure cases, rights, security, portability, maintenance, and exit path;
5. prefer tests/fixtures/failure corpora/behavioral mechanics over dependency adoption when possible;
6. keep reused machinery behind WePLD-owned contracts;
7. require evidence that the donor mechanism improves the accepted objective;
8. reject unnecessary machinery even when permission to reuse it exists.

Founder-reported permission to use donor source/code is favorable acquisition evidence, but it does not replace per-source permission/license/attribution/redistribution/provenance verification at admission time.

## Initial Harness Thesis Tournament

The Harness Program must be falsifiable before building a large framework.

### Candidate experiment

Use multiple model families and multiple task archetypes. Exact models/tasks must be selected later based on availability, reproducibility, licensing/terms, budget, and verifier quality.

Compare at least:

```text
A = minimal baseline
B = representative fixed composable baseline
C = WePLD static compiled recipe
D = WePLD adaptive recipe
```

Optional reference baselines may include donor harnesses where their evaluation protocol can be reproduced fairly.

### Pairing requirements

For a valid paired comparison:

```text
SAME_MODEL_IDENTITY
SAME_PROVIDER_OR_EXACT_SERVING_STACK
SAME_MODEL_SETTINGS
SAME_TASK_IDENTITIES
SAME_ENVIRONMENT_IDENTITIES
SAME_VERIFIER_IDENTITIES
SAME_EFFECT/AUTHORITY ENVELOPE where comparison claims require it
RECORDED_TOKEN/COST/LATENCY BUDGETS
REPRODUCIBLE SEEDS / RUN IDENTITIES where supported
INFRA_FAILURES REPORTED SEPARATELY FROM TASK FAILURES
```

### Primary objective

```text
maximize verified_success_probability
subject to token, money, latency, and risk budgets
```

### Secondary objectives

```text
reduce tokens per verified success
reduce cost per verified success
reduce no-progress turns
reduce human intervention
reduce context-loss failures
reduce unsafe/unauthorized attempted effects
preserve or improve latency
```

### Proposed go criteria

The exact numeric threshold must be ratified before experiment execution. The qualitative requirement is:

- repeatable lift on more than one model family; **or**
- equivalent verified success with a material efficiency improvement; and
- no unacceptable regression in authority/safety/verification coverage.

### Proposed kill / narrow criteria

Stop or narrow the architecture if controlled evaluation shows one or more of:

- adaptive composition does not outperform a simpler fixed/minimal harness across diverse models/tasks;
- gains disappear under paired exact-task reruns;
- improvements are primarily benchmark-search/portfolio effects with no useful routed single-recipe lift;
- complexity cost exceeds improvement in verified success/cost/latency;
- model-specific profiles do not generalize enough to justify a reusable router;
- verification overhead dominates practical value;
- safe authority separation makes adaptive features impractical for real workflows.

If killed, retain useful isolated mechanics behind the existing roadmap rather than preserving the Harness Program as a large standalone abstraction.

## Phased research program

```text
H0 — Harness thesis and falsification contract
H1 — Model Capability Profile
H2 — Task/Environment Fingerprint
H3 — Harness Intermediate Representation / Proof-Carrying Recipe
H4 — Context Compiler
H5 — Tool Surface Compiler
H6 — Verifier Fabric
H7 — Failure Intelligence
H8 — Adaptive Harness Router
H9 — Harness Gym / controlled tournament
H10 — Governed Evolution (only if H0–H9 prove value)
H11 — Model↔Harness Data Flywheel (later, separately authorized)
```

This numbering is Harness Program research notation only. It does not create canonical implementation tasks and must not be confused with S1 task authority.

## Current decision

```text
HARNESS_PROGRAM = GO_FOR_RESEARCH
IMPLEMENTATION_NOW = NO
S1_013_START = NO
ROADMAP_REWRITE_NOW = NO
SOURCE_ADMISSION_NOW = NO
DEPENDENCY_ADMISSION_NOW = NO
SELF_EVOLUTION_NOW = NO

NEXT_AFTER_CURRENT_S1_LEDGER_SEQUENCE =
  qualify a Harness architecture/falsification planning slice before implementation
```

## Current repository sequencing boundary

At the time this dossier was captured, canonical `main` remained at the S1-012 merge baseline while the separately governed v24 ledger-reconciliation bootstrap and the docs-only ledger reconciliation remained active work.

The Harness Program must not bypass that sequence.

```text
PR_39 = v24 exact ledger-reconciliation policy bootstrap
PR_38 = docs-only S1 ledger reconciliation
HARNESS_PROGRAM_BRANCH = research/docs only
HARNESS_PROGRAM_PR = NOT_OPENED
S1_013_PLUS = NOT_STARTED
```

Before any future Harness Program mutation, read live GitHub truth; this point-in-time note is not live authority.

## Research-output acceptance rule

This dossier records a design hypothesis, not product acceptance.

```text
RESEARCH_DOSSIER != ROADMAP_AUTHORITY
DONOR_INVENTORY != SOURCE_ADMISSION
FOUNDER_PERMISSION != AUTOMATIC_IMPORT
BENCHMARK_RESULT != EFFECT_AUTHORITY
HARNESS_RECIPE != COMPLETION_AUTHORITY
META_AGENT_OUTPUT != PROMOTION_AUTHORITY
```
