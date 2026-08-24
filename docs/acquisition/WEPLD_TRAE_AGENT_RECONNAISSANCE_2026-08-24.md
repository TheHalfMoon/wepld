# WePLD — TRAE / Trae-Agent Architecture & Source Reconnaissance Addendum

```text
DOCUMENT_CLASS = ARCHITECTURE_RECONNAISSANCE_ADDENDUM / PLAN_INPUT
DATE = 2026-08-24
BOUND_WEPLD_PLAN_PR = 167
BOUND_WEPLD_PREDECESSOR_HEAD = 83cb7f4ffc809146dff86e5fe064ffd37c800034
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
```

## Executive decision

TRAE contributes two distinct evidence surfaces that MUST NOT be conflated:

1. **TRAE product / trae.ai** — current product and UX reference only.
2. **`bytedance/trae-agent`** — separately licensed open-source software-engineering agent and research platform that is eligible for future bounded path mining.

```text
TRAE_PRODUCT != TRAE_AGENT_SOURCE
PRODUCT_BEHAVIOR != SOURCE_PROVENANCE
OPEN_SOURCE_AGENT != COMMERCIAL_IDE_IMPLEMENTATION
```

The open-source repository is valuable primarily as a quarry for agent-loop mechanics, trajectory/evidence schemas, Docker tool routing, provider/tool abstraction, lightweight code-knowledge indexing, evaluation harnesses and test-time scaling. It is NOT selected as a WePLD runtime or dependency.

## Reproducible source anchor

```text
REPOSITORY = bytedance/trae-agent
EXACT_COMMIT = e839e559ac61bdd0e057c375dd1dee391fee797d
EXACT_TREE = fceea1cae3ddf5fcc29649db47449c54e011844e
MAIN_COMMIT_DATE = 2026-02-05
LICENSE = MIT
LICENSE_BLOB = 3b8890f7c67d2e5342e96c343b1aa3ae8bf6b78c
PYPROJECT_BLOB = 3599350958181100d08f7e4efb0e62dba2542d42
README_BLOB = 0e47f0593b085e2e7c75f7d58d0e645f4dc92472
```

Important inspected paths:

```text
trae_agent/agent/base_agent.py
  blob=01d4fde4c178ae8112292373d9f47cf4a9d03efe

trae_agent/utils/trajectory_recorder.py
  blob=e24909e89ea6daeac109a752fff8b274c81a2391

trae_agent/tools/ckg/ckg_database.py
  blob=e077585feaa086f579d0b64ebf8b697f50c44558

server/Readme.md
  blob=b2e1effcc78189007c5b4adbfad24ac1606f8f92

evaluation/patch_selection/README.md
  blob=10d28acbc161e783e1b5f4c3fe791da2c51c9d59
```

The product website continued evolving after this open-source main pin. Therefore product claims and open-source implementation claims remain separately sourced.

## Product / UX reference

Current TRAE product materials present several useful product patterns:

- traditional IDE mode and a more autonomous SOLO mode;
- integrated editor/browser/terminal/document visibility during autonomous work;
- custom agents with selectable tools, skills and logic;
- agents callable as sub-agents;
- user-facing agent-team composition;
- expansion from coding-only work into broader product/research/data workflows under TRAE Work.

WePLD product lessons:

```text
IDE_MODE <-> MISSION_MODE should be a visible user choice
SUBAGENT_TOPOLOGY should be inspectable, not hidden
AGENT_TEAM should map to Edara staffing/topology evidence
EDITOR_BROWSER_TERMINAL_DOCS should converge into one Work evidence timeline
AUTONOMY_LEVEL should never bypass Nawat
```

No TRAE product source rights are inferred from the public website. Product behavior is REFERENCE-ONLY unless an exact separately licensed source surface is established.

## Mission Runtime / Edara quarry

`BaseAgent` exposes a compact software-engineering agent loop:

```text
messages
 -> model response
 -> completion decision OR tool calls
 -> sequential/parallel tool execution
 -> tool results
 -> optional reflection
 -> recorded step
 -> next step
```

It also exposes replaceable model clients, configurable tools, cleanup, max-step control and optional Docker routing.

Useful WePLD mechanics to mine later:

- explicit step state machine;
- provider/model adapter seams;
- tool registry and tool-result normalization;
- sequential versus parallel tool-call handling;
- bounded max-step execution;
- resource cleanup and cancellation concerns;
- CLI/headless separation direction;
- Docker workspace/path translation mechanics.

Critical divergence:

Trae Agent's model-to-tool path reaches `ToolExecutor`/`DockerToolExecutor` directly. WePLD must interpose a host-owned effect proposal and Nawat decision before any effectful tool execution.

```text
MODEL_TOOL_CALL != EFFECT_AUTHORITY
DOCKER_TOOL_EXECUTOR != NAWAT
TOOL_REGISTRY_ENTRY != SAFE_CAPABILITY
```

## Work / Evidence Timeline quarry

The trajectory recorder captures useful fields:

- task;
- provider/model;
- max steps;
- LLM input/output;
- token usage;
- available tools;
- agent step state;
- tool calls/results;
- reflection;
- errors;
- execution time;
- final success/result;
- Lakeview summary.

This is valuable as an evidence-schema quarry, especially for Work and Quality Passport design.

However, the implementation repeatedly rewrites a mutable JSON file. WePLD MUST NOT adopt that as canonical evidence semantics.

```text
TRAE_TRAJECTORY_JSON = OBSERVABILITY_QUARRY
WEPLD_EVIDENCE_TIMELINE = APPEND_ONLY + CONTENT_ADDRESSED + AUTHORITY_LINKED
```

Every WePLD effect record should additionally bind proposal identity, Mirefa qualification, Nawat decision, containment state, ChangeUnit identity and post-effect evidence.

## Fehrest.Maemar CKG quarry and negative oracle

Trae Agent contains a local CKG implementation using Tree-sitter and SQLite with function/class extraction and reusable local databases. This supports the decision that useful structural code intelligence can remain local and lightweight before adopting a graph server.

Useful ideas:

- local reconstructible index;
- repository snapshot identity;
- parsed function/class spans;
- SQLite as a simple replaceable persistence layer;
- cache expiry and rebuild behavior.

Important negative lessons:

1. Dirty Git identity hashes `git status --porcelain` output rather than the bytes of modified files. Two different dirty contents can preserve the same status representation and therefore collide at the freshness layer.
2. The file-metadata fallback relies on names, modification times and sizes rather than content-addressed bytes.
3. The source documents incomplete JavaScript/TypeScript AST coverage and inefficient rebuild behavior.

Therefore WePLD's Fehrest freshness floor remains stronger:

```text
PROJECT_FACT_IDENTITY = CONTENT/OBJECT ADDRESSED
DIRTY_CONTENT_CHANGE MUST CHANGE FACT_PROVENANCE
UNKNOWN_LANGUAGE_COVERAGE = UNKNOWN, NOT COMPLETE
CACHE_REUSE REQUIRES PROVEN FRESHNESS
```

Trae CKG is a quarry and failure corpus, not the canonical Project Brain design.

## Containment quarry

The open-source agent can route selected tools through a Docker manager/executor. This is useful for studying:

- host/container workspace mapping;
- tool-specific containment routing;
- lifecycle/start/stop behavior;
- Docker execution ergonomics.

But Docker mode is not authorization and is not sufficient as a universal security boundary.

```text
DOCKER_ROUTE != EFFECT_GRANT
CONTAINER != COMPLETE_CONTAINMENT
CONTAINMENT != QUALIFICATION
```

The stronger WePLD Windows-first and risk-tiered containment plan remains unchanged.

## Provider / dependency surface

The exact `pyproject.toml` directly depends on multiple model/provider and agent ecosystem packages including OpenAI, Anthropic, Google GenAI, Ollama and MCP, plus Tree-sitter and UI/build tooling. Evaluation extras add Docker and benchmark-related dependencies.

This makes whole-project adoption inappropriate for WePLD's minimum-sufficient Rust-first trusted core.

Future mining MUST prefer bounded mechanics/tests over package/runtime adoption and must inventory:

- provider/network surfaces;
- credential handling;
- MCP process/network behavior;
- Docker effects;
- Python package dependency graph;
- portability/Windows behavior;
- tool execution and shell boundaries.

## MCP / protocol lesson

Trae Agent's MCP support is useful as interoperability evidence, but does not alter the V2.3 protocol layering decision:

```text
MCP = UWC tool/resource edge candidate
MCP_TOOL = UNTRUSTED UNTIL QUALIFIED
MCP_PERMISSION != NAWAT_GRANT
```

## Headless / service direction

The repository's HTTP server area is explicitly under construction. Its stated direction includes stateless operations, concurrent requests, JSON/streaming output and trajectory-based reproduction/replay.

This is useful as a Mission Runtime research signal, but MUST NOT be treated as production-ready source or architecture proof.

WePLD should retain durable Work state outside provider/HTTP request identity and make replay depend on immutable evidence, not an arbitrary mutable trajectory file.

## Assurance and test-time scaling

Trae Agent's research/evaluation surface includes generation, pruning and patch-selection/test-time-scaling mechanics for software issue resolution.

This is a high-value Assurance quarry:

```text
GENERATE_N_CANDIDATES
QUALIFY_EACH_CANDIDATE
PRUNE_DOMINATED_OR_INVALID
INDEPENDENTLY_SCORE/REVIEW
SELECT_FOR_FURTHER_QUALIFICATION
```

But WePLD preserves stronger boundaries:

```text
SELECTOR_SCORE != TRUTH
ENSEMBLE_VOTE != AUTHORITY
PATCH_SELECTION != TRUSTED_COMPLETION
TEST_TIME_SCALING != NAWAT_GRANT
```

Candidate generation can improve search quality while every proposed effect and final completion decision remains governed by Mirefa/Nawat/Assurance/Trusted Completion.

## Acquisition disposition

```text
TRAE_AI_PRODUCT:
  DISPOSITION = REFERENCE_ONLY
  OWNER = Work / Edara product UX

BYTEDANCE_TRAE_AGENT:
  DISPOSITION = TIER_1_PATH_MINING_CANDIDATE
  OWNERS = Mission Runtime / Work / Fehrest.Maemar / Assurance
  WHOLE_PROJECT_ADOPTION = NO
  DEPENDENCY_ADMISSION = NONE
  SOURCE_ADMISSION = NONE
  EXECUTION_AUTHORITY = NONE
```

Priority future mining paths:

1. `trae_agent/agent/*` — step/runtime abstractions and negative authority oracle;
2. `trae_agent/utils/trajectory_recorder.py` — evidence schema quarry;
3. `trae_agent/tools/ckg/*` — local-index ideas and freshness failure corpus;
4. `trae_agent/tools/*` plus Docker executor/manager — tool/containment seams;
5. `evaluation/patch_selection/*` — Assurance/test-time-scaling mechanics;
6. model/MCP configuration and clients — provider/network/dependency surface inventory;
7. server direction — replay/headless negative and future reference.

## Plan impact

This addendum strengthens but does not renumber V2.3:

- **S4-G:** include Trae CKG as a negative/failure oracle for content freshness and lightweight local indexing.
- **S6-AH:** include Trae agent-loop, tool-registry, trajectory and Docker seams in Tier-1 path mining.
- **S7-S / Assurance:** evaluate Trae patch-selection/test-time-scaling mechanics as advisory candidate-selection evidence.
- **S9-P:** use trajectory fields as schema input while retaining append-only/content-addressed canonical evidence.

No implementation, source import, dependency installation, donor execution, provider access or model execution is authorized by this addendum.
