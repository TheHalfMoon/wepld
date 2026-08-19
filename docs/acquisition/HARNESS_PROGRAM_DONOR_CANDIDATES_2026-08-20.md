# WePLD Harness Program — Donor Candidate Inventory

```text
DOCUMENT_DATE = 2026-08-20
DOCUMENT_CLASS = DISCOVERY / DONOR-CANDIDATE INVENTORY
CANONICAL_REGISTRY_REVISION = NONE
FROZEN_402_REGISTRY_MUTATION = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
S1_013_PLUS = NOT_STARTED
```

## Purpose

Record the high-signal source, behavior-oracle, benchmark, and research donors identified for the proposed WePLD Harness Program without silently rewriting the frozen 402-entry restoration registry or admitting any source/dependency into product execution.

The Harness Program research thesis is that WePLD should learn from multiple harness schools—minimal, composable, adaptive, self-evolving, verifier-grounded, and model↔harness co-evolution—while preserving WePLD-owned authority, evidence, and completion contracts.

## Rights / permission provenance

The founder reports that WePLD has permission to reuse source code from the sources represented in this donor program.

```text
FOUNDER_REPORTED_SOURCE_CODE_PERMISSION = YES
PERMISSION_EVIDENCE_STORED_IN_REPOSITORY = NO
PERMISSION_SCOPE_VERIFIED_PER_SOURCE = NO
ATTRIBUTION_OBLIGATIONS_VERIFIED_PER_SOURCE = NO
REDISTRIBUTION_OBLIGATIONS_VERIFIED_PER_SOURCE = NO
SOURCE_ADMISSION_IMPLIED_BY_PERMISSION = NO
```

Before any source code is imported, vendored, adapted, or used as a runtime dependency, the applicable Source Acquisition gate must still verify the exact source revision, permission/license scope, attribution/notice obligations, security, portability, maintenance, provenance, and exit strategy. Founder-reported permission is favorable acquisition evidence; it is not automatic source admission.

## Candidate source-code donors and behavior oracles

| Candidate | Repository | Primary Harness-Program value | Proposed role | Current status |
|---|---|---|---|---|
| DeepSeek Harness | `deepseek-ai/deepseek-harness` | plugin-tree composition, capability seams, durable session/event architecture, model-routed context/compaction | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Cordis | `cordiverse/cordis` | reversible plugin effects, contextual service/event composition | `SOURCE_DONOR + ARCHITECTURE_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| OpenHarness | `HKUDS/OpenHarness` | complete inspectable harness, tools, skills, memory, permissions, subagents, dry-run | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| HELIX | `HKUDS/HELIX` | ports/atoms/recipes, harness recomposition/search, sibling rollouts, data flywheel | `SOURCE_DONOR + BEHAVIOR_ORACLE + SEARCH_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Agentic Harness Engineering (AHE) | `china-qijizhifeng/agentic-harness-engineering` | observability-driven evaluate→analyze→improve loop, falsifiable harness evolution | `SOURCE_DONOR + EVOLUTION_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Harness-R1 | `DeepExperience/Harness-R1` | failure-trajectory→runtime-patch engineering, sandboxed lifecycle hooks, rerun-derived reward | `SOURCE_DONOR + EVOLUTION_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| mini-SWE-agent | `SWE-agent/mini-swe-agent` | minimal-harness baseline, bash-only execution, linear history, deployable sandbox abstraction | `SOURCE_DONOR + MINIMAL_BASELINE_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| SWE-agent | `SWE-agent/SWE-agent` | agent-computer interface design, configurable tools/history, software-engineering benchmark mechanics | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Pi Mono | `badlogic/pi-mono` | compact agent runtime, unified model API, coding-agent session mechanics, extensibility | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| OpenCode | `anomalyco/opencode` | provider-neutral coding-agent runtime, tools, plugins, sessions, production behavior | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| OpenHands Software Agent SDK | `OpenHands/software-agent-sdk` | composable software agents, workspaces, tools, skills/plugins, agent-server boundary | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| OpenHands Agent Canvas | `OpenHands/OpenHands` | multi-backend agent control center, automations, remote/local runtime topology | `SOURCE_DONOR + PRODUCT_BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| OpenAI Agents SDK | `openai/openai-agents-python` | sandbox agents, sessions, tracing, guardrails, HITL, handoffs/agents-as-tools | `SOURCE_DONOR + INTEROP_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Deep Agents | `langchain-ai/deepagents` | long-horizon context management, subagents, skills, persistent memory, pluggable backends | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| CheetahClaws | `SafeRL-Lab/cheetahclaws` | multi-model harness, configurable tool surface, permissions, context/memory, long-horizon operation | `SOURCE_DONOR + BEHAVIOR_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Scaffold Effects | `namanvats/scaffold-effects` | controlled model×harness trials, cost/pass-rate/failure fingerprints, reproducible analysis artifacts | `SOURCE_DONOR + BENCHMARK_ORACLE + FAILURE_CORPUS` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Harbor | `harbor-framework/harbor` | arbitrary-agent evaluation, sandboxed environments, parallel experiments, RL rollout generation | `SOURCE_DONOR + BENCHMARK_SUBSTRATE_CANDIDATE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| harness-bench | `LamaSu/harness-bench` | component-level harness ablations and Pareto capability×cost evaluation patterns | `SOURCE_DONOR + BENCHMARK_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Ouroboros | `razzant/ouroboros` | reviewed self-development, persistent agent runtime, guardrail-pressure behavior | `SOURCE_DONOR + NEGATIVE/POSITIVE_EVOLUTION_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| TimesFM | `google-research/timesfm` | executable model-specific skill/preflight pattern and capability-aware operating guidance | `SOURCE_DONOR + SKILL/PREFLIGHT_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Harness Open Source | `harness/harness` | development-platform/pipeline control-plane patterns; not an LLM harness baseline | `SOURCE_DONOR + PLATFORM_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |
| Harness AI | `harness/harness-ai` | one canonical skill/MCP/governance surface projected into multiple coding assistants | `SOURCE_DONOR + INTEROP/DISTRIBUTION_ORACLE` | `DISCOVERY_ONLY / NOT_ADMITTED` |

## Research-reference donors

These research references are first-class design/test/negative-oracle donors even where a canonical matching implementation repository has not yet been established in this inventory.

| Research source | Stable reference | Harness-Program value | Current status |
|---|---|---|---|
| Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows | `arXiv:2605.27922` | model-harness pair as evaluation unit; trace/usage/validator evidence | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents | `arXiv:2607.22688` | alternating harness/model optimization and trajectory distillation | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| SBCO: Self-Supervised, Verifier-Grounded Harness Optimization For Planning Agents | `arXiv:2608.10157` | low-compute verifier-grounded harness optimization | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| One Recipe, Many Harnesses: What Self-Evolution Encodes Across Languages and Models | `arXiv:2608.10178` | typed failure signals, falsifiable harness edits, compensation-layer interpretation | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Ouroboros: A Self-Developing Frontier Coding Agent with Reviewed Core Evolution | `arXiv:2608.08311` | reviewed self-evolution and authoritative-guardrail problem | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Code as Agent Harness | `arXiv:2605.18747` | harness taxonomy across reasoning/action/environment/verification and multi-agent scaling | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Proof-Carrying Agent Actions: Model-Agnostic Runtime Governance for Heterogeneous Agent Systems | `arXiv:2606.04104` | runtime-neutral action certificates and replayable governance evidence | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Agent Safety Should Be a Runtime Contract | `arXiv:2608.11274` | preventive + evidential runtime safety; trajectory-with-checkable-evidence | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| The Scaffold Effect in Coding Agents: Harness Choice as a Hidden Variable in Coding-Agent Evaluation | `arXiv:2607.22585` | controlled harness/model variance, efficiency, and failure fingerprints | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses | `arXiv:2604.25850` | harness evolution with component/experience/decision observability | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories | `arXiv:2608.02276` | learned executable harness repair from real rerun rewards | `RESEARCH_REFERENCE / NOT_ADMITTED` |
| Helix: Let Models and Harnesses Co-Evolve | `arXiv:2608.13951` | harness search, composition, sibling rollout labeling, model↔harness flywheel | `RESEARCH_REFERENCE / NOT_ADMITTED` |

## Proposed capability-triggered mining map

This document does not change S1–S10 or `docs/acquisition/MINING_PRIORITY.md`. It records the following proposed Harness-Program mapping for a future separately governed registry/mining revision:

```text
MODEL/CAPABILITY PROFILING
  -> TimesFM skill/preflight pattern
  -> Scaffold Effects
  -> Harness-Bench

HARNESS COMPOSITION / HIR
  -> DeepSeek Harness + Cordis
  -> HELIX
  -> OpenHarness
  -> Pi Mono
  -> OpenCode

CONTEXT / MEMORY / LONG-HORIZON EXECUTION
  -> DeepSeek Harness
  -> OpenHarness
  -> Deep Agents
  -> OpenHands SDK
  -> CheetahClaws

MINIMUM-SUFFICIENT HARNESS
  -> mini-SWE-agent
  -> Pi Mono

VERIFIER / BENCHMARK FABRIC
  -> Harbor
  -> Harness-Bench
  -> Scaffold Effects
  -> SBCO

FAILURE INTELLIGENCE / HARNESS EVOLUTION
  -> AHE
  -> Harness-R1
  -> One Recipe, Many Harnesses
  -> Ouroboros

MODEL <-> HARNESS DATA FLYWHEEL
  -> HELIX
  -> Co-Harness

AUTHORITY / PROOF-CARRYING EXECUTION
  -> Proof-Carrying Agent Actions
  -> Agent Safety Should Be a Runtime Contract
  -> Code as Agent Harness

CROSS-AGENT INTEROPERABILITY / DISTRIBUTION
  -> OpenAI Agents SDK
  -> Harness AI
  -> OpenHands
  -> Harness Open Source where platform-control patterns are relevant
```

## Ponytail / acquisition rule

For every concrete future Harness-Program capability:

1. mine only the strongest 2–3 donors for the exact capability;
2. pin exact revisions before code-level evaluation;
3. inspect tests, failure modes, security boundaries, rights, maintenance, and portability;
4. prefer behavior/test/failure-corpus reuse over machinery reuse when the machinery is not minimum-sufficient;
5. keep reused machinery behind WePLD-owned contracts;
6. retain a clear exit/replacement path;
7. require deterministic evidence that the donor mechanism improves the accepted objective before retention.

```text
DONOR_DISCOVERY != SOURCE_ADMISSION
FOUNDER_PERMISSION != SOURCE_ADMISSION
SOURCE_CODE_AVAILABLE != SOURCE_ADMISSION
BENCHMARK_GAIN != AUTHORITY
HARNESS_COMPLEXITY_MUST_EARN_ITS_PLACE = YES
```

## Canonicalization boundary

This inventory is intentionally prepared as a donor-candidate artifact only. It must not be merged into canonical `main` by bypassing the current S1 integrity/ledger-reconciliation sequence.

A future qualified acquisition/registry revision may:

- establish exact repository/paper pins;
- attach durable permission/license evidence;
- deduplicate donors already represented in the frozen registry;
- assign canonical source IDs where appropriate;
- update capability-triggered mining priority;
- keep the immutable 402-entry restoration artifact intact as historical evidence.
