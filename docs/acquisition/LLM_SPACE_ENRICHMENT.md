# LLM Space — Bounded Source / Behavior Enrichment

## Classification

```text
SOURCE = deer-flow/llm-space
PIN = be629ddd58c6a9f5f011687580a1858652f12925
CURRENT_RELEASE_REFERENCED_AT_PIN = v4.12.1
ROOT_LICENSE = MIT
CLASS = DESKTOP_AGENT_LAB + FEHREST + ASSURANCE + TRACE_DEBUG + RECOVERY + PLUGIN_SYSTEM + BUILD_LEARNING_ORACLE
TIER = S+
DISPOSITION = ADAPT_CANDIDATE | PORT_CANDIDATE | TEST_QUARRY | UX_ORACLE | NEGATIVE_ORACLE | REFERENCE
CANONICAL_SOURCE_REGISTRY_V1_CHANGE = 0
PENDING_NEXT_REGISTRY_REVISION = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

LLM Space is not present in the frozen 402-entry source-registry V1. This document records it as a post-V1 candidate pending a separately governed registry revision; it does not rewrite the frozen restoration artifact.

## Rights / provenance state

The pinned repository root license is MIT. Root licensing does not establish the rights or suitability of every transitive package, plugin, model/provider integration, generated project, downloaded extension, or bundled asset.

```text
ROOT_LICENSE_ESTABLISHED = MIT
TRANSITIVE_RIGHTS_AUDIT = INCOMPLETE
PATH_LEVEL_RIGHTS_AUDIT = REQUIRED_BEFORE_REUSE
WHOLE_REPOSITORY_COPY = NOT_AUTHORIZED
```

## Pinned evidence anchors

```text
README.md
blob = 784642c70d4d5a84947463bea2f53daad92ddbd1

LICENSE
blob = 3f609fa5b91d241f0889a3af43f5f33033b8c652

docs/core-concepts.md
blob = 6c54140615e31283c184f5ab9c8eaedcf7325e36

docs/plugins.md
blob = 31c2c2952ddbc603019b7d6bfe01e83210ea08c0

.agents/kaizen-loop/CAPABILITY_MAP.md
pinned by repository commit; path-level blob identity should be captured before direct reuse
```

## WePLD capability mapping

```text
Desktop / Work   <- local agent workbench, file/tree/tab experiment UX, model/tool/prompt controls
Fehrest          <- local durable Thread files, run snapshots, variables, tool results, provenance-friendly storage
Assurance        <- trace inspection, replay/debug, durable run comparison, rubric snapshots and human verdicts
Mission Runtime  <- thread/run/tool-call event shapes and abort/persist behavior
S9 Recovery      <- source-preserving compaction, run history, replay/debug mechanics
UWC              <- tool/provider/MCP/plugin extension surfaces
Byan             <- kaizen capability/evidence mapping and benchmark observations as non-authoritative learning candidates
```

## Positive mechanics worth mining

### 1. Local-first experiment file as the unit of work

LLM Space models a Thread as a saved experiment file containing model selection, system prompt, variables, tools, messages, tool-call results, run history, and evaluations. Workspace management is ordinary local file management.

This is a strong Fehrest/Desktop behavior oracle:

```text
DURABLE_LOCAL_EXPERIMENT
> EPHEMERAL_CHAT_SESSION
```

WePLD should preserve typed canonical ownership rather than adopting Thread JSON as the Project Brain contract wholesale.

### 2. Run history as durable evidence for comparison and debugging

Historical run snapshots are preserved for replay, comparison, and debugging. Tool-call requests, raw/partial arguments, results, error flags, provider usage, and model configuration remain inspectable.

This is directly useful for Assurance and Mission Runtime evidence design.

### 3. Evaluation rubric snapshotting with human verdict separation

LLM Space can compare two durable runs using a reusable rubric with ordered criteria and scores. Saved evaluations contain an immutable snapshot of the rubric and scores keyed by stable run ID, so later rubric edits do not rewrite historical evaluations. It derives score averages/deltas while keeping the overall verdict as a separate human decision.

This maps very well to:

```text
MEASURED_SCORE != ACCEPTANCE_VERDICT
HISTORICAL_EVALUATION_SNAPSHOT = IMMUTABLE_EVIDENCE
```

WePLD should retain its stronger `ReviewOutcome != CompletionDecision` boundary.

### 4. Compaction that preserves the source conversation

Conversation compaction is previewed and applied to a new Thread file, leaving the source conversation available. This is a useful recovery/non-destructive-transformation oracle for Fehrest and S9.

### 5. Explicit distinction between template and rendered prompt

Stored prompt templates retain variables while runtime resolution produces concrete text for execution; run snapshots can preserve the relevant execution evidence without destroying the reusable template. Missing or empty variables produce actionable errors.

This can inform AGILLE/Fehrest context-materialization contracts.

### 6. Plugin distribution separated from Extension capability types

LLM Space defines Plugin as the unit of distribution/version/config/reload and Extension as the contributed capability. One plugin may contribute Skills, MCP servers, model providers, commands, executable tools, and Thread Storages.

Useful mechanics include:
- stable package identity from `package.json.name`;
- conventional non-recursive extension discovery;
- symlink rejection and path-root confinement;
- ZIP bounds for compressed size, extracted size, and entry count;
- traversal/absolute/backslash-path rejection;
- plugin runtime data stored outside the replaceable installation directory;
- corrupt plugin settings disabling third-party plugins for that startup rather than preventing the application from starting.

These are strong plugin-loader/test-quarry mechanics.

### 7. Evidence-driven capability map / kaizen loop

The repository maintains a capability map that labels observations by freshness and evidence state (`confirmed`, `stale`, `unknown`), records explicit non-goals, visible gaps, and concrete code/product evidence. That is a useful Build Learning / Byan process oracle.

WePLD can adopt the evidence discipline without allowing such a map to become architecture authority automatically.

### 8. Shared core across desktop and headless evaluation

The monorepo separates shared domain/storage/generators, local runtime/models/tools/skills/MCP/plugins, shared UI, and desktop shell. This is useful for separating trusted contracts from presentation while keeping desktop and headless evaluation aligned.

## Negative oracles / required WePLD divergence

```text
LLM_SPACE_RUN_REPLAY != SAFE_EXTERNAL_EFFECT_REPLAY
LLM_SPACE_MANUAL_EVALUATION != COMPLETION_DECISION
LLM_SPACE_THREAD_JSON != WEPLD_CANONICAL_PROJECT_BRAIN
LLM_SPACE_PLUGIN_ENABLED != NAWAT_GRANT
LLM_SPACE_LOCAL_PLUGIN_TRUST != SECURITY_SANDBOX
LLM_SPACE_MODEL_FALLBACK != SILENT_ROUTE_SUBSTITUTION_ALLOWED
LLM_SPACE_TOOL_VISIBLE != TOOL_EXECUTION_AUTHORIZED
```

### Plugin trust must be stronger in WePLD

LLM Space explicitly states that local Plugins are fully trusted and that runtime process isolation is not a security sandbox. WePLD may reuse discovery, ZIP hardening, identity, reload, and data-separation mechanics, but executable extensions must remain behind WePLD trust/authority/containment policy.

```text
PLUGIN_DISCOVERED_OR_ENABLED != EFFECT_AUTHORITY
PROCESS_ISOLATION != SECURITY_BOUNDARY
```

### Default-enabled third-party plugins are not a WePLD default

LLM Space treats a newly discovered Plugin as enabled by default. For WePLD, newly discovered executable or external-effect capabilities should not silently become active authority-bearing surfaces.

### Model fallback cannot become silent execution substitution

LLM Space documents a UI/runtime fallback to an available model when a Thread has no saved model. That is reasonable for an interactive lab, but WePLD's execution contracts require no silent model/provider route substitution for governed work.

```text
MISSING_EXACT_ROUTE != SILENTLY_PICK_ANY_AVAILABLE_MODEL
```

### Replay/debug must not replay side effects by default

Historical replay is excellent for model/tool trace inspection, but WePLD must distinguish deterministic evidence replay from re-executing external effects. Recovery/diagnostic replay should use recorded effects or explicit new Attempts unless effect re-execution is separately authorized.

### Generated agent code is not automatically qualified code

LLM Space can generate runnable agent projects from Threads. In WePLD, generation output remains builder output and must enter normal Spec Kit/Ponytail/testing/review/acceptance gates.

## Acquisition decision

Mine LLM Space as a Desktop/Fehrest/Assurance/Recovery/plugin-system donor rather than adopting it as the WePLD application shell or canonical runtime.

Priority path-mining order:

1. `packages/core/src/types/threads/` + tests — durable run/evaluation/thread schemas;
2. thread history/storage/client paths — run snapshots, replay, comparison, persistence and migration behavior;
3. trace/debug workbench paths — event inspection, failure replay, provider/tool evidence;
4. `docs/plugins.md` plus plugin runtime/scanner/installer tests — identity, path confinement, ZIP bounds, data separation, corruption behavior;
5. `.agents/kaizen-loop/` — evidence-state/capability-map mechanics for Build Learning;
6. desktop/runtime boundary and headless execution/evaluation paths — shared contracts without UI authority leakage.

No source, package, plugin, extension, model provider, MCP server, executable tool, generated project, telemetry service, or runtime dependency is admitted by this document.
