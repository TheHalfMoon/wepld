# DeepCode — Bounded Source / Behavior Enrichment

## Classification

```text
SOURCE = HKUDS/DeepCode
PIN = 287510fbf6820147a48adf79f7fd86b0ed1afe92
ROOT_LICENSE = MIT
CLASS = AGENT_HARNESS + MISSION_RUNTIME + UWC + EDARA + FEHREST + WINDOWS_EXECUTION + RECOVERY + ASSURANCE_ORACLE
TIER = S+
DISPOSITION = PORT_CANDIDATE | ADAPT_CANDIDATE | TEST_QUARRY | NEGATIVE_ORACLE | REFERENCE
CANONICAL_SOURCE_REGISTRY_V1_CHANGE = 0
PENDING_NEXT_REGISTRY_REVISION = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

DeepCode was identified after the frozen 402-entry source-registry V1 restoration. This record does not rewrite that immutable restoration count. It is a post-V1 acquisition candidate for the next explicitly governed registry revision.

## Rights / provenance state

The repository root is MIT at the pinned revision. Whole-repository reuse is **not** implied by that root license.

Pinned rights anchors at `287510fbf6820147a48adf79f7fd86b0ed1afe92`:

```text
LICENSE
blob = b3ba37ce442298d5bdec96e2e52a8a812a25f123

THIRD_PARTY_NOTICES.md
blob = 5f3c1d1070080dfb65acccd3c8b1007166e2ff1e
```

`THIRD_PARTY_NOTICES.md` records resolved Python, JavaScript, Rust, and platform components with multiple license families and additional attributed presentation assets. DeepCode also bundles pinned upstream Agent Skills from OpenAI Codex, OpenAI Skills, and Anthropic Skills, with exact upstream repository/revision/path records in `core/skills/builtin/UPSTREAM_SOURCES.json`.

Therefore:

```text
ROOT_LICENSE_ESTABLISHED = MIT
TRANSITIVE_RIGHTS_AUDIT = INCOMPLETE
PATH_LEVEL_RIGHTS_AUDIT = REQUIRED_BEFORE_REUSE
WHOLE_REPOSITORY_COPY = NOT_AUTHORIZED
```

## High-value observed paths

Pinned path observations:

```text
core/harness/tools/spawn_agent.py
blob = 816db9e2deff8b85e309b94fbf934c2a48a92762

core/harness/agents/control.py
blob = c17907a4278170633387da4458a0e72f0811a3cc

core/harness/permissions.py
blob = 4ef371ec8bb5d91edab889c22a5656b1af340c4f

core/harness/windows_sandbox.py
blob = 5c2aa2ac4a09268c374794563e6bafd386174308

core/skills/builtin/UPSTREAM_SOURCES.json
blob = 5be15ce2db2b8f081a024250769c48fa89ac4923
```

## WePLD capability mapping

```text
Mission Runtime <- durable Session/Turn/Goal/execution/evidence mechanics
UWC             <- external backend adapters + capability checking + MCP/runtime seams
Edara           <- bounded fan-out + stable task dedup + non-recursive delegation
Fehrest         <- durable local history + context/Skill provenance + late-result persistence
Nawat candidate <- three-valued permission mechanics and read-only upper bounds only
S3              <- process ownership / interruption / Windows Job Object evidence
Assurance       <- reviewer composition + structured result + verification evidence mechanics
S8              <- stop/resume/crash-settlement/no-side-effect-replay behavior
Byan candidate  <- outcome/session/review evidence for later learning, never authority
```

## Positive mechanics worth mining

### 1. One durable execution model across surfaces

DeepCode exposes one Agent runtime through CLI and a Tauri Desktop workbench while sharing local Projects, Sessions, models, Skills, permissions, Goals, Automations, approvals, and verification evidence. This is a strong UI/runtime separation oracle for WePLD desktop-first architecture.

### 2. Capability-aware bounded delegation

`spawn_agent` is non-blocking and defaults to isolated worktrees. Native children can receive a persona, narrowing tool allowlist, and structured output schema. External backends include Codex and Claude Code but receive only the self-contained task plus workspace; unsupported context/composition capabilities fail loudly before start rather than being silently ignored.

A stable task-name/dedup key blocks wasteful duplicate successful work, the default fan-out is bounded, and delegation depth is capped so subagents cannot recursively create more agents.

### 3. Structured delegated results

A native child with an output schema must submit a conforming structured result. A prose response does not silently stand in for the required structure. This is a useful UWC/Assurance negative-contract pattern.

### 4. Durable result delivery and continuation

Subagent results are delivered through the active Turn input boundary. When a result loses the active-Turn race, DeepCode attempts to append it to canonical Session context for the next Turn rather than leaving it only in ephemeral agent state. Native child conversations can be interrupted, parked, redirected, and resumed.

### 5. Three-valued permission engine

DeepCode exposes `ALLOW | ASK | DENY`, sensitive-path protection, explicit read-only upper bounds, rule-based narrowing, and a plan mode that denies mutating tools. MCP policy can narrow the shared permission boundary rather than silently widening it.

These are useful implementation/mechanics candidates, but they are not WePLD authorization semantics.

### 6. Skill capability discipline

Skills can declare dependencies; missing requirements and cycles fail before the first model request. Skills can narrow tools already available to the Session but cannot grant new permissions. Revision/provenance data is retained, and upstream bundled Skills have explicit source pins.

### 7. Windows process-tree ownership

`core/harness/windows_sandbox.py` uses a Windows Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, suspended process creation, assignment to the Job, resume, and exit-code forwarding. This is useful S3 process-tree/lifetime evidence and a direct Windows test quarry.

### 8. Evidence-oriented execution

DeepCode keeps tests, builds, diagnostics, diffs, artifacts, permission decisions, Goals, model configuration, and verification records with durable Sessions. Failed verification becomes repair input instead of being presented as success.

## Negative oracles / required WePLD divergence

```text
DEEPCODE_SESSION_MODE != NAWAT_GRANT
DEEPCODE_FULL_ACCESS != UNIVERSAL_EFFECT_AUTHORITY
DEEPCODE_COMPLETED != WEPLD_COMPLETION_DECISION
DEEPCODE_WORKTREE_ISOLATION != SECURITY_BOUNDARY
DEEPCODE_EXTERNAL_BACKEND_POLICY != WEPLD_AUTHORITY
DEEPCODE_SKILL_SELECTED != CAPABILITY_GRANTED
DEEPCODE_MODEL_ROUTE != AUTHORITY
```

### Windows fallback must not be copied

The pinned Windows Job Object launcher explicitly degrades to plain subprocess execution when Win32 Job Object setup fails. That is an acceptable product choice for its stated boundary, but it is a **negative oracle** for WePLD untrusted-worker execution:

```text
REQUIRED_CONTAINMENT_UNAVAILABLE != FALLBACK_TO_UNCONTAINED_EXECUTION
```

For a WePLD execution class that requires containment, failure to establish the required boundary must fail closed or be routed to a separately qualified lower-trust profile. This directly preserves `B-WIN-001` and `NO_UNTRUSTED_LOCAL_WORKER` until qualified evidence exists.

### Semantic task completion is not trusted completion

DeepCode documents that the working Agent may request `complete` or `blocked`, while tests/builds/diagnostics/diffs/review remain evidence. WePLD must retain its stronger separation:

```text
MODEL_REQUESTED_COMPLETE != COMPLETION_DECISION
VERIFICATION_EVIDENCE != COMPLETION_AUTHORITY
GREEN_TESTS != COMPLETION_DECISION
```

### Observability persistence cannot silently become optional evidence

DeepCode deliberately avoids letting transcript-observability failure kill the underlying run. WePLD may adopt that behavior for non-critical telemetry, but acceptance-critical evidence persistence must instead produce an explicit incomplete/degraded result and cannot silently count as complete.

## Acquisition decision

DeepCode should be mined capability-by-capability rather than imported as a runtime dependency.

Priority path-mining order:

1. `core/harness/permissions.py` — permission mechanics / negative authority comparison;
2. `core/harness/agents/control.py` + `core/harness/tools/spawn_agent.py` — UWC/Edara delegation and result delivery;
3. `core/harness/windows_sandbox.py` + related sandbox tests — S3 Windows process ownership and negative fallback oracle;
4. durable Session/Turn/Goal/evidence domain paths — Mission Runtime / Fehrest / recovery;
5. Skill provider/runtime paths and upstream pin ledger — governed Skill mechanics;
6. Paper2Code reference-mining/indexing/verification paths when S4/S5 research reproduction reaches its acquisition gate.

No source, package, dependency, Skill, runtime, provider, or model is admitted by this document.