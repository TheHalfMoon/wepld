# WePLD MiniMax Universal Agent / Automation Donor Reconnaissance

```text
DOCUMENT_DATE = 2026-08-21
DOCUMENT_CLASS = DISCOVERY / DONOR RECONNAISSANCE / FUTURE PRODUCT-ARCHITECTURE INPUT
RESEARCH_BASE_MAIN = 5d25112d506b0044f2e79756869c009c5b5ba358
CANONICAL_REGISTRY_REVISION = NONE
FROZEN_402_REGISTRY_MUTATION = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
ROADMAP_MUTATION = NONE
H0_014_PLUS = NOT_STARTED
H0_SCREEN_EXECUTION = NONE
MODEL_PROVIDER_EXECUTION = NONE
MODEL_WEIGHT_ACCESS = NONE
MODEL_INFERENCE = NONE
EXTERNAL_REVIEW_EGRESS = NONE
```

## Purpose

Record the strongest current MiniMax product behaviors and public source mechanisms relevant to a future WePLD universal agent system without importing source, adding dependencies, modifying the frozen source registry, granting product implementation authority, starting H0-014+, executing H0-SCREEN, or invoking any model/provider runtime.

The target is not to embed MiniMax as a privileged provider. The target is to learn from the strongest separable mechanisms and preserve WePLD-owned contracts so that hosted and local models remain replaceable.

```text
MINIMAX_LIKE_EXPERIENCE != MINIMAX_DEPENDENCY
MODEL_PROVIDER != AGENT_RUNTIME
MODEL_PROVIDER != AUTHORITY
MODEL_PROVIDER != MEMORY_OWNER
MODEL_PROVIDER != SCHEDULE_OWNER
MODEL_PROVIDER != SKILL_OWNER
MODEL_PROVIDER != COMPLETION_AUTHORITY
```

The architectural goal is a provider-neutral, local-first-capable work system in which WePLD owns tasks, teams, skills, schedules, memory, permissions, evidence, and completion decisions while models supply bounded reasoning or generation behind explicit adapters.

## Executive decision

MiniMax is a high-value donor family for future WePLD agent orchestration, especially for:

1. long-horizon goal execution;
2. Leader / Worker / Verifier collaboration;
3. persistent memory and evolving reusable skills;
4. scheduled recurring work;
5. custom agents with independent instructions and capability sets;
6. MCP-based tool integration;
7. remote progress / approval workflows;
8. model/provider indirection;
9. local OpenAI-compatible inference through `llama.cpp`-style endpoints;
10. structured application actions that separate tool contracts from the model.

The correct WePLD disposition is:

```text
ADOPT THE BEHAVIORAL REQUIREMENTS
STUDY THE OPEN SOURCE MECHANISMS
KEEP WEPLD-OWNED CONTRACTS
MAKE LOCAL MODELS FIRST-CLASS
KEEP CLOUD MODELS OPTIONAL
KEEP AUTHORITY OUTSIDE THE MODEL
DEFER SOURCE / DEPENDENCY ADMISSION
REJECT A PROVIDER-LOCKED AGENT CORE
```

## Current official product evidence

MiniMax's current documentation index exposes dedicated surfaces for custom models/BYOK, custom Agents, Memory, Skills, Agent Team, messaging integrations, Remote Control, Scheduled Tasks, Built-in Browser, Goal mode, permissions/safety, task history, and workspace/project context.

Primary current documentation index:

- https://agent.minimax.io/docs/llms.txt

Current MiniMax Code product surface:

- https://agent.minimax.io/download

Current Agent Team engineering description:

- https://agent.minimax.io/docs/techblog
- https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953

Current MiniMax M3 / Agent Team description:

- https://www.minimax.io/blog/minimax-m3

Current changelog:

- https://agent.minimax.io/docs/changelog

These product references are behavior / architecture evidence only. They do not establish open-source availability of every product subsystem.

## Agent Team findings

MiniMax describes a deterministic multi-Agent collaboration loop with three primary roles:

```text
Leader
  -> translates the user goal into task structure
  -> decomposes and coordinates work

Worker
  -> executes a bounded sub-task
  -> may have different tools, context, and output requirements

Verifier
  -> evaluates produced work
  -> can reject and return work for correction
```

The product engineering material also emphasizes context isolation, parallel sub-task execution, adversarial quality gates, asynchronous execution, and long-running work.

### WePLD lesson

The useful abstraction is not the role names themselves. It is the separation of orchestration, execution, and verification.

Future WePLD contract candidate:

```text
CoordinatorRole
WorkerRole
VerifierRole

CoordinatorRole != AuthorityIssuer
WorkerRole != CompletionAuthority
VerifierRole != MergeAuthority
```

A Coordinator may decompose work, assign tasks, adjust plans, and request verification. It must not mint permissions that were not already granted by the user/governance layer.

A Worker may execute only within its effective capability envelope.

A Verifier may produce evidence and a verdict under an explicit verification contract. It must not silently expand the candidate's authority or mutate the candidate while claiming to verify it.

Verifier rejection should produce an explicit state transition:

```text
CANDIDATE
  -> VERIFY
      -> PASS
      -> REPAIR_REQUIRED
      -> REASSIGN
      -> ESCALATE
      -> BLOCKED
```

Never:

```text
VERIFIER_REJECTED -> SILENTLY_ACCEPT_WORKER_SUCCESS
```

## Goal / long-horizon execution findings

MiniMax exposes a Goal mode in which the user specifies a verifiable outcome and the agent keeps working until the goal is achieved or progress is blocked.

### WePLD lesson

A goal should be a durable WePLD object, not prompt text owned by a model session.

Candidate contract:

```text
Goal {
  goal_id
  requested_outcome
  success_criteria
  constraints
  authority_snapshot_ref
  task_graph_ref
  evidence_requirements
  stop_conditions
  status
}
```

Required invariant:

```text
GOAL_PERSISTENCE != AUTHORITY_PERSISTENCE
```

A goal can survive restarts, provider changes, and model changes. Any privileged operation must still re-evaluate effective authority at execution time.

## Persistent memory findings

MiniMax currently presents persistent memory as retention of habits, preferences, project context, conventions, and long-term working patterns. `Mini-Agent` also exposes a concrete persistent Session Note mechanism.

### WePLD lesson

Memory should be layered and typed rather than injected as one opaque transcript.

Candidate layers:

```text
USER_PREFERENCE_MEMORY
PROJECT_MEMORY
WORKSPACE_MEMORY
AGENT_PROFILE_MEMORY
TASK_MEMORY
VERIFICATION_MEMORY
EPHEMERAL_SESSION_CONTEXT
```

Every durable memory item should carry provenance and scope:

```text
MemoryRecord {
  memory_id
  scope
  source
  created_at
  last_confirmed_at
  content_digest
  sensitivity_class
  retention_policy
  authority_effect = NONE
}
```

Required invariants:

```text
MEMORY_MAY_INFORM = YES
MEMORY_MAY_AUTHORIZE = NO
MEMORY_MAY_OVERRIDE_CURRENT_USER_CONSTRAINT = NO
STALE_MEMORY_MUST_NOT_BECOME_AUTHORITY = YES
```

## Scheduled work findings

MiniMax exposes Scheduled Tasks for recurring Agent work and its current product surfaces advertise schedules alongside skills, memories, and teams.

### WePLD lesson

Schedules persist intent and timing, not privileged authorization.

Candidate contract:

```text
Schedule {
  schedule_id
  task_template_ref
  cadence
  timezone
  enabled
  next_due_at
  authority_recheck_policy
  output_policy
}
```

Required invariant:

```text
SCHEDULE_PERSISTS_INTENT
SCHEDULE_DOES_NOT_PERSIST_AUTHORITY
```

At run time:

```text
SCHEDULE_DUE
  -> LOAD_TASK_TEMPLATE
  -> RECHECK_CURRENT_AUTHORITY
  -> RECHECK_CURRENT_CAPABILITIES
  -> RECHECK_CURRENT_POLICY
  -> EXECUTE_OR_BLOCK
```

A schedule created while a capability is allowed must not continue exercising that capability after it is revoked.

## Skills findings

MiniMax exposes reusable Skills in the product and maintains a public `MiniMax-AI/skills` repository. The repository documents installation into Claude Code, Cursor, Codex, OpenCode, and other agent environments, demonstrating that the skill concept is portable across model/tool hosts.

### WePLD lesson

A Skill should be a versioned capability package, not a hidden prompt fragment.

Candidate contract:

```text
SkillManifest {
  skill_id
  version
  content_digest
  provenance
  instructions
  declared_tools
  declared_filesystem_scope
  declared_network_scope
  declared_side_effects
  required_permissions
  output_contract
  verifier_contract
}
```

Required invariants:

```text
SKILL != MODEL
SKILL != PROVIDER
SKILL != AUTHORITY
SKILL_CANNOT_SELF_AUTHORIZE
SKILL_REQUESTED_CAPABILITY > EFFECTIVE_AUTHORITY => BLOCK
```

The skill loader should expose the minimum relevant skill to the model and avoid loading unrelated skill libraries into persistent context.

## Custom Agents findings

MiniMax's current documentation index exposes Custom Agents with their own role, instructions, skills, workspace, and channels.

### WePLD lesson

An Agent profile should be configuration over a shared governed runtime.

Candidate contract:

```text
AgentProfile {
  agent_id
  role
  instructions_ref
  allowed_skills
  preferred_model_selector
  workspace_scope
  channel_scope
  capability_request_profile
  memory_scope
}
```

Required invariant:

```text
AGENT_PROFILE_REQUESTS_CAPABILITY
GOVERNANCE_GRANTS_CAPABILITY
```

A profile must not contain an irrevocable or hidden privilege grant.

## Model / provider indirection findings

MiniMax Code currently documents Custom Models / BYOK with a provider base URL, API key, API format, and model names.

The stronger open-source evidence is `MiniMax-AI/OpenRoom`, which has a typed provider abstraction supporting both OpenAI-compatible and Anthropic-compatible request formats. Its current provider configuration explicitly includes `llama.cpp` with a default local endpoint:

```text
provider = llama.cpp
baseUrl = http://localhost:8080
model = local-model
```

The corresponding OpenAI-compatible client only sends an Authorization header when the configured API key is non-empty.

### WePLD lesson

Local models must be first-class rather than a degraded fallback.

Candidate provider boundary:

```text
ModelAdapter {
  adapter_id
  protocol_family
  endpoint
  model_identifier
  auth_mode
  tool_call_capabilities
  structured_output_capabilities
  context_limit_metadata
  locality
  health_state
}
```

Target protocol families:

```text
OPENAI_COMPATIBLE
ANTHROPIC_COMPATIBLE
LOCAL_OPENAI_COMPATIBLE
FUTURE_EXPLICIT_ADAPTER
```

Target locality classes:

```text
LOCAL_PROCESS
LOCAL_NETWORK
REMOTE_PROVIDER
```

Required invariants:

```text
LOCAL_MODEL = FIRST_CLASS
LOCAL_ENDPOINT_MAY_REQUIRE_NO_API_KEY = YES
MODEL_SWITCH_MUST_NOT_DESTROY_TASK_STATE = YES
MODEL_SWITCH_MUST_NOT_DESTROY_MEMORY = YES
MODEL_SWITCH_MUST_NOT_CHANGE_AUTHORITY = YES
MODEL_OUTPUT_MUST_BE_NORMALIZED_BEFORE_TOOL_EXECUTION = YES
```

WePLD should not encode provider-specific tool-call or reasoning markup directly into task state. Provider responses should be normalized into WePLD-owned message/tool-call structures.

## Structured application-action findings

`MiniMax-AI/OpenRoom` exposes a browser desktop in which apps publish structured Actions and the Agent operates applications through those action contracts rather than directly owning each app's internal state.

### WePLD lesson

The future tool layer should expose stable typed actions at subsystem boundaries:

```text
MODEL
  -> PROPOSED_TOOL_CALL
  -> WEPLD_NORMALIZATION
  -> CAPABILITY_CHECK
  -> POLICY_CHECK
  -> TOOL_ADAPTER
  -> RESULT
  -> EVIDENCE
```

Not:

```text
MODEL -> DIRECT_UNGOVERNED_SIDE_EFFECT
```

This same pattern should apply to browser operations, filesystem changes, terminal commands, project actions, remote integrations, and future application automation.

## MCP findings

MiniMax maintains public MCP repositories and `Mini-Agent` includes an MCP loader. The current MiniMax documentation also treats MCP as an extensibility layer.

### WePLD lesson

MCP is a useful tool-edge protocol but must not become the internal authority model.

```text
MCP_SERVER_AVAILABLE != MCP_TOOL_AUTHORIZED
MCP_TOOL_DISCOVERED != MCP_TOOL_ENABLED
MCP_TOOL_ENABLED != SIDE_EFFECT_AUTHORIZED
```

A future WePLD MCP bridge should map every discovered tool to a local capability descriptor and require policy evaluation before invocation.

Tool schemas should be loaded on demand where possible to avoid permanently spending model context on rarely used tools.

## Browser and remote-control findings

MiniMax currently exposes a built-in browser and Remote Control surfaces. The current product documentation distinguishes browser functionality from broader task collaboration and permission flows.

### WePLD lesson

Browser automation and remote control are separate capability families.

Candidate capability boundaries:

```text
BROWSER_READ
BROWSER_NAVIGATE
BROWSER_INTERACT
BROWSER_DOWNLOAD
BROWSER_UPLOAD
REMOTE_VIEW_TASK
REMOTE_SEND_INSTRUCTION
REMOTE_APPROVE_PERMISSION
```

Each should have explicit scope and audit evidence.

Remote Control is a control plane, not a reason to bypass local authority checks.

## Permissions findings

MiniMax's current documentation index exposes a dedicated Permissions and Safety surface, and the changelog records permission-review explanations.

### WePLD lesson

Permissions should be deterministic policy inputs, not merely UI prompts generated by the active model.

Candidate policy result:

```text
ALLOW
CONFIRM
BLOCK
```

With mandatory provenance:

```text
PermissionDecision {
  requested_capability
  requested_scope
  decision
  governing_rule
  user_confirmation_ref
  task_id
  candidate_ref
  expires_at
}
```

The model may explain why it wants a capability. The model does not decide whether the capability exists.

## Public source anchors inspected

These exact pins are research anchors only. They are not canonical source-registry entries and are not admitted dependencies.

### MiniMax-AI/Mini-Agent

```text
REPOSITORY = MiniMax-AI/Mini-Agent
PIN = d76a4f6389688cabda39c224a6cdfa274215d47c
ROOT_LICENSE = MIT
ROOT_LICENSE_BLOB = 9f742bcceb684ea85a3aa9d1acde3243ff213c04

mini_agent/agent.py
BLOB = b7d7feab2cd1a6d65199a637965e366db2c47161

mini_agent/tools/note_tool.py
BLOB = 4ca6092172e918d98ab6e5a2fa10486062cdd1be

mini_agent/tools/mcp_loader.py
BLOB = c89b07906813d333416024110fac1962a082730c

mini_agent/tools/skill_loader.py
BLOB = 7128f79a7ba6552bd9e4d60ee88b6c78b2631a9a
```

Research disposition:

```text
AGENT_LOOP_ORACLE = STRONG
PERSISTENT_NOTE_MEMORY_ORACLE = STRONG
MCP_LOADER_ORACLE = STRONG
SKILL_LOADER_ORACLE = STRONG
SOURCE_ADMISSION = NONE
```

### MiniMax-AI/OpenRoom

```text
REPOSITORY = MiniMax-AI/OpenRoom
PIN = 02468154c4d99f8925916425bf444d672454fb3d
ROOT_LICENSE = MIT
ROOT_LICENSE_BLOB = 7c6829e76a214ff4d45de9fc5dd0d7b0b5db1b41

apps/webuiapps/src/lib/llmClient.ts
BLOB = 5c30e126f112030ba2f0b2329b4394ce7eac2a72

apps/webuiapps/src/lib/llmModels.ts
BLOB = 346907efa52ddf017be6087ca422628884377d25

MERGED_LOCAL_LLAMACPP_PR = #29
MERGE_COMMIT = 02468154c4d99f8925916425bf444d672454fb3d
```

Research disposition:

```text
PROVIDER_ABSTRACTION_ORACLE = STRONG
LOCAL_MODEL_ENDPOINT_ORACLE = STRONG
STRUCTURED_TOOL_CALL_ORACLE = STRONG
BROWSER_APP_ACTION_ORACLE = STRONG
SOURCE_ADMISSION = NONE
```

Important: the repository contains multiple provider presets. Their presence is implementation evidence for provider indirection, not a WePLD recommendation or provider admission.

### MiniMax-AI/skills

```text
REPOSITORY = MiniMax-AI/skills
PIN = 60aaae52bb2af8162732751a4332f62a5fef518b
ROOT_LICENSE = MIT
ROOT_LICENSE_BLOB = 132dd20ee3294d09a1c613a6bd4c8094c496fbf9
```

The repository itself records that some content is inspired by or derived from third-party work and includes separate attribution/license handling. Therefore root MIT licensing does not eliminate future per-skill provenance review.

Research disposition:

```text
PORTABLE_SKILL_FORMAT_ORACLE = STRONG
PER_SKILL_RIGHTS_REVIEW_BEFORE_REUSE = REQUIRED
SOURCE_ADMISSION = NONE
```

### MiniMax-AI/MiniMax-MCP

```text
REPOSITORY = MiniMax-AI/MiniMax-MCP
PIN = 0856b9aef8a9d676bb63bdd6b6426d7b640a3b7a
ROOT_LICENSE = MIT
ROOT_LICENSE_BLOB = b3d379e6706e52edcf591c846ad356b92e983994
```

Research disposition:

```text
MCP_TOOL_EDGE_ORACLE = STRONG
SOURCE_ADMISSION = NONE
```

### MiniMax-AI/MiniMax-Coding-Plan-MCP

```text
REPOSITORY = MiniMax-AI/MiniMax-Coding-Plan-MCP
PIN = 5dbf3494d7dac35d154958e0c1dab03910b89bbd
ROOT_LICENSE = MIT
ROOT_LICENSE_BLOB = b3d379e6706e52edcf591c846ad356b92e983994
```

Research disposition:

```text
CODING_MCP_ORACLE = USEFUL
SOURCE_ADMISSION = NONE
```

### MiniMax-AI/minimax-code

```text
REPOSITORY = MiniMax-AI/minimax-code
PIN = cd025375799a1360d499d5c06cfb2e1111a960fc
PUBLIC_PRODUCT_SOURCE_IMPLEMENTATION = NOT_ESTABLISHED
CURRENT_REPOSITORY_ROLE = ISSUE / PRODUCT SUPPORT SURFACE
```

Do not infer that the complete MiniMax Code desktop implementation or Agent Team engine is open source from this repository.

## Team-engine source availability finding

Current research did not establish an official public MiniMax repository containing the complete production Leader / Worker / Verifier Team Engine implementation used by MiniMax Code.

Therefore:

```text
MINIMAX_AGENT_TEAM_BEHAVIOR_ORACLE = YES
MINIMAX_AGENT_TEAM_ARCHITECTURE_ORACLE = YES
MINIMAX_AGENT_TEAM_TEST_ORACLE = YES
FULL_PRODUCTION_TEAM_ENGINE_SOURCE_DONOR = NOT_ESTABLISHED
```

This distinction is load-bearing. Product documentation can define behavior requirements; source reuse requires separately inspectable public source and rights evidence.

## Proposed WePLD universal work model

The strongest synthesis from MiniMax is a WePLD-owned work graph with replaceable reasoning workers.

```text
User Intent
  -> Goal
  -> Task Graph
  -> Coordinator
      -> Worker A
      -> Worker B
      -> Worker C
  -> Candidate Outputs
  -> Independent Verifier(s)
  -> Evidence Reconciliation
  -> Completion Decision
```

The system should allow Workers to use different model adapters:

```text
Worker A -> LOCAL_OPENAI_COMPATIBLE
Worker B -> REMOTE_PROVIDER_A
Worker C -> REMOTE_PROVIDER_B
Verifier -> LOCAL_OR_REMOTE_INDEPENDENT_ADAPTER
```

No role identity should be hard-bound to a vendor.

## Proposed model selection semantics

Future model selection should be a policy function over task requirements rather than a hardcoded provider preference.

Inputs may include:

```text
LOCALITY_REQUIREMENT
DATA_EGRESS_CLASS
TOOL_CALL_REQUIREMENT
CONTEXT_REQUIREMENT
LATENCY_BUDGET
COST_BUDGET
MODEL_CAPABILITY_PROFILE
USER_SELECTION
AVAILABILITY
```

Example decisions:

```text
PROHIBITED_EGRESS -> LOCAL_ONLY
USER_PINNED_LOCAL -> LOCAL_ONLY
PUBLIC_SOURCE_ONLY + USER_ALLOWS_REMOTE -> LOCAL_OR_REMOTE
REMOTE_PROVIDER_UNAVAILABLE -> QUALIFIED_LOCAL_FALLBACK
```

Required invariant:

```text
FALLBACK_MAY_CHANGE_MODEL
FALLBACK_MUST_NOT_CHANGE_AUTHORITY
```

## Proposed task object

```text
TaskRecord {
  task_id
  parent_goal_id
  requested_by
  task_type
  inputs
  expected_outputs
  candidate_scope
  assigned_agent_profile
  selected_model_adapter
  requested_capabilities
  effective_authority_ref
  status
  attempt
  evidence_refs
  verifier_refs
}
```

Suggested lifecycle:

```text
PLANNED
READY
RUNNING
AWAITING_PERMISSION
AWAITING_VERIFICATION
REPAIR_REQUIRED
BLOCKED
CANCELLED
COMPLETED_PROVISIONAL
COMPLETED_TRUSTED
```

Only governance-defined evidence can advance `COMPLETED_PROVISIONAL` to `COMPLETED_TRUSTED`.

## Proposed evidence model

Every meaningful action should be attributable to an immutable task/candidate identity.

```text
EvidenceRecord {
  evidence_id
  task_id
  candidate_id
  producer
  evidence_type
  subject_digest
  result
  timestamp
  environment_identity
  authority_snapshot_ref
}
```

A model statement such as "done" is not evidence of completion.

## Proposed local-first architecture

```text
WePLD Core
  |
  +-- Task / Goal Store
  +-- Memory Store
  +-- Schedule Store
  +-- Skill Registry
  +-- Permission Engine
  +-- Evidence Ledger
  +-- Team Orchestrator
  +-- Tool / MCP Capability Router
  +-- Model Adapter Registry
        |
        +-- Local OpenAI-Compatible Adapter
        |     +-- llama.cpp-style endpoint
        |     +-- other future qualified local servers
        |
        +-- Remote OpenAI-Compatible Adapter
        +-- Anthropic-Compatible Adapter
        +-- Future Explicit Adapters
```

Air-gapped operation is a target when every selected tool and model adapter is local and the task does not require external network access.

```text
AIR_GAP_CAPABLE = TARGET
AIR_GAP_AUTOMATICALLY_PROVEN = NO
```

Air-gap claims require separate test evidence for the concrete runtime configuration.

## Security and governance requirements

### Tool capability isolation

```text
MODEL_SEES_TOOL != MODEL_MAY_USE_TOOL
TOOL_DISCOVERED != TOOL_ENABLED
TOOL_ENABLED != SIDE_EFFECT_AUTHORIZED
```

### Memory poisoning resistance

Durable memory must not accept arbitrary model-generated claims as trusted policy facts.

Candidate controls:

```text
PROVENANCE_REQUIRED
SCOPE_REQUIRED
SENSITIVITY_CLASS_REQUIRED
USER_CORRECTION_PRECEDENCE
POLICY_FACTS_NOT_WRITABLE_BY_MODEL
AUTHORITY_FACTS_NOT_WRITABLE_BY_MODEL
```

### Schedule safety

Recurring tasks must fail closed when their required capability is no longer authorized.

### Team safety

A Coordinator cannot expand a Worker's permissions by assignment. A Worker cannot delegate capabilities it does not possess. A Verifier cannot modify the candidate under review unless the workflow explicitly transitions into repair mode and creates a new candidate identity.

### Local model safety

Local inference reduces data egress but does not imply trustworthy behavior.

```text
LOCAL_MODEL != TRUSTED_MODEL
LOCAL_MODEL != SAFE_TOOL_CALLER
LOCAL_MODEL != COMPLETION_AUTHORITY
```

Local models remain subject to the same capability, candidate, evidence, and verification boundaries.

## Donor priority matrix

| Mechanism | Evidence strength | WePLD value | Current disposition |
|---|---|---:|---|
| Agent Team Leader/Worker/Verifier behavior | Strong official product/engineering evidence | Very high | Behavior + architecture oracle |
| Goal / long-horizon loop | Strong official docs evidence | Very high | Behavior oracle |
| Persistent memory | Strong official docs + Mini-Agent source | Very high | Behavior + source oracle |
| Scheduled tasks | Strong official docs evidence | Very high | Behavior oracle |
| Skills | Strong docs + public skills source | Very high | Behavior + source oracle; per-skill rights required |
| Custom agents | Strong official docs evidence | High | Behavior oracle |
| BYOK/custom models | Strong official docs evidence | Very high | Behavior oracle |
| Local `llama.cpp` OpenAI-compatible backend | Strong merged official OpenRoom source | Very high | Source + architecture oracle |
| Provider-normalized tool calls | Strong OpenRoom source | Very high | Source + architecture oracle |
| MCP integration | Strong source/docs evidence | High | Tool-edge oracle |
| Built-in browser | Strong official docs evidence | High | Behavior oracle |
| Remote control | Strong official docs evidence | Medium/high | Control-plane behavior oracle |
| Complete production Team Engine source | Not established | Potentially very high | Not a current source donor |

## What WePLD should not copy

1. Do not hardwire the product to MiniMax models.
2. Do not make a cloud provider the owner of task state.
3. Do not let model memory become policy authority.
4. Do not let schedules preserve stale permissions.
5. Do not treat an MCP server as trusted merely because it is configured.
6. Do not let a Leader/Coordinator grant capabilities to Workers.
7. Do not let a Worker self-certify trusted completion.
8. Do not let a Verifier mutate and verify the same candidate invisibly.
9. Do not equate local inference with safe inference.
10. Do not infer source availability from product behavior.

## Future acquisition questions

Before any MiniMax-related source is copied, adapted, vendored, linked, or admitted, a separately governed Source Acquisition step must answer at minimum:

```text
EXACT_SOURCE_REVISION
EXACT_FILES
APPLICABLE_LICENSE_PER_FILE
THIRD_PARTY_NOTICES
TRANSITIVE_DEPENDENCIES
SECURITY_REVIEW
PORTABILITY
MAINTENANCE_COST
REPLACEMENT_PATH
MINIMUM_SUFFICIENT_API_SURFACE
TEST_ORACLE
EXIT_STRATEGY
```

For skills, per-skill provenance and license review is mandatory even when the repository root is MIT.

## Research conclusion

MiniMax provides unusually strong evidence for the product direction WePLD should pursue, but the key lesson is architectural separation rather than provider adoption.

```text
WEPLD_OWNS_GOALS = YES
WEPLD_OWNS_TASKS = YES
WEPLD_OWNS_TEAMS = YES
WEPLD_OWNS_MEMORY = YES
WEPLD_OWNS_SKILLS = YES
WEPLD_OWNS_SCHEDULES = YES
WEPLD_OWNS_PERMISSIONS = YES
WEPLD_OWNS_EVIDENCE = YES
WEPLD_OWNS_COMPLETION = YES

MODEL_PROVIDER_IS_REPLACEABLE = YES
LOCAL_MODEL_IS_FIRST_CLASS = TARGET
CLOUD_MODEL_IS_OPTIONAL = TARGET
```

The strongest future WePLD experience is therefore not "support MiniMax." It is:

```text
ANY QUALIFIED MODEL
+ ANY QUALIFIED AGENT PROFILE
+ ANY QUALIFIED SKILL
+ ANY QUALIFIED TOOL EDGE
+ WEPLD-OWNED MEMORY / TASK / SCHEDULE / TEAM STATE
+ LOCAL AUTHORITY GATES
+ EXACT-CANDIDATE VERIFICATION
= UNIVERSAL GOVERNED AGENT WORK SYSTEM
```

## Authority boundary

This reconnaissance authorizes nothing beyond recording research evidence.

```text
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
MODEL_WEIGHT_ACCESS = NONE
MODEL_INFERENCE = NONE
H0_SCREEN_EXECUTION = NONE
H0_014_PLUS = NOT_STARTED
ROADMAP_MUTATION = NONE
READY = NO
MERGE_AUTHORITY = NONE
```
