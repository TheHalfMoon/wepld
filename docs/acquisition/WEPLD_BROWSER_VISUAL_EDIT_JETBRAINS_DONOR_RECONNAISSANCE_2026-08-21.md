# WePLD Browser Studio / Visual Edit Mode — JetBrains Donor Reconnaissance

```text
DOCUMENT_DATE = 2026-08-21
DOCUMENT_CLASS = DISCOVERY / DONOR RECONNAISSANCE / FUTURE PRODUCT-ARCHITECTURE INPUT
RESEARCH_BASE_MAIN = c5779d4589d13285f69d2f090731ef60a3fd69f5
CANONICAL_REGISTRY_REVISION = NONE
FROZEN_402_REGISTRY_MUTATION = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
ROADMAP_MUTATION = NONE
H0_014_PLUS = NOT_STARTED
H0_SCREEN_EXECUTION = NONE
MODEL_PROVIDER_EXECUTION = NONE
EXTERNAL_REVIEW_EGRESS = NONE
```

## Purpose

Record the strongest JetBrains source-code donors, behavior oracles, and engineering mechanisms relevant to a future WePLD Browser Studio / Visual Edit Mode without importing source, adding dependencies, changing the frozen source registry, mutating P0+S1..S10 roadmap authority, or starting H0-014+.

The target product behavior is not merely an embedded browser. The target is a governed visual-development loop in which a user can point at rendered UI, select one or more concrete elements, describe the desired change, let a replaceable coding agent produce a candidate patch, see the result hot-reloaded in the real application, and then verify the exact candidate before acceptance.

```text
POINT AT RENDERED UI
  -> RESOLVE LIVE DOM / ACCESSIBILITY / SPATIAL IDENTITY
  -> MAP TO TRUE SOURCE / FRAMEWORK COMPONENT / SYMBOL
  -> ATTACH MINIMUM SUFFICIENT RUNTIME + DESIGN CONTEXT
  -> ASK A SELECTED REPLACEABLE AGENT
  -> PRODUCE AN ISOLATED CANDIDATE PATCH
  -> HOT RELOAD THE REAL APPLICATION
  -> COMPARE BEFORE / AFTER
  -> RUN FUNCTIONAL + ACCESSIBILITY + DESIGN + REGRESSION CHECKS
  -> INDEPENDENTLY REVIEW THE EXACT CANDIDATE
  -> ACCEPT / REJECT WITH EVIDENCE
```

This document is a capability-triggered donor study. It is not a new canonical roadmap slice and does not imply that the future browser substrate, semantic engine, ACP, Qodana, Koog, JCEF, or any other donor is admitted.

## Rights / permission provenance

The founder reports permission to reuse source code that JetBrains and related identified projects make available on GitHub or the open internet.

```text
FOUNDER_REPORTED_SOURCE_CODE_PERMISSION = YES
PERMISSION_EVIDENCE_STORED_IN_REPOSITORY = NO
PERMISSION_SCOPE_VERIFIED_PER_SOURCE = NO
PER_FILE_LICENSE_NOTICE_AUDIT = INCOMPLETE
TRANSITIVE_LICENSE_AUDIT = INCOMPLETE
ATTRIBUTION_OBLIGATIONS_VERIFIED_PER_SOURCE = PARTIAL
REDISTRIBUTION_OBLIGATIONS_VERIFIED_PER_SOURCE = PARTIAL
SOURCE_ADMISSION_IMPLIED_BY_PERMISSION = NO
```

Where this reconnaissance inspected an exact license or source header, that evidence is recorded below. Before any source is copied, adapted, vendored, linked, packaged, or admitted as a runtime dependency, a separately governed Source Acquisition step must verify the exact revision, applicable license/permission scope, attribution and notice obligations, third-party/transitive obligations, security, portability, maintenance, replacement path, and minimum-sufficient API surface.

```text
FOUNDER_PERMISSION != SOURCE_ADMISSION
PUBLIC_SOURCE != SOURCE_ADMISSION
PERMISSIVE_LICENSE != SOURCE_ADMISSION
BEHAVIOR_ORACLE != RUNTIME_DEPENDENCY
```

## Executive decision

JetBrains is a high-value donor family for the future Browser Studio, but a wholesale IntelliJ-platform transplant is not justified by this research.

The highest-value mechanisms are separable:

1. **JCEF/JBCef browser lifecycle and JavaScript bridge patterns** — strong architecture oracle for embedded Chromium ownership, lifecycle, DevTools, browser↔host callbacks, and optional out-of-process execution.
2. **Remote Driver `JCefUI` DOM automation** — exceptionally direct source oracle for host-driven DOM selection, XPath lookup, injected browser helpers, element bounds, scrolling, visibility checks, and physical click dispatch.
3. **WebStorm Live Edit + Actual DOM + Web Inspector** — strong behavior oracle for live browser synchronization, browser↔editor highlighting, element picking, locator generation, and code/browser round trips.
4. **IntelliJ semantic project analysis / Find Usages / refactoring / structural search** — essential model for converting a visual selection into a real source symbol and a bounded impact set rather than relying on text grep.
5. **Local History (`lvcs`)** — strong source and behavior donor for reversible agent edits before Git commit.
6. **JetBrains Air** — strong workflow oracle for plan-before-edit, agent-neutral selection, permission modes, Git worktree/Docker isolation, parallel agents, diff review, and agent-on-agent review; no full Air source-code admission is inferred here.
7. **ACP** — high-priority interoperability candidate for keeping coding agents replaceable rather than building one bespoke integration per agent.
8. **JetBrains MCP Server tool exposure/router model** — strong behavior oracle for per-tool enablement and keeping rarely needed tool schemas out of persistent model context.
9. **Qodana baseline + SARIF + quality-gate model** — strong verification oracle for distinguishing new regressions from unchanged debt and failing closed on configured thresholds.
10. **Koog** — secondary source/architecture candidate for agent persistence, retry/fault-tolerance, structured workflows, and history management; exact license/notice disposition remains pending before any source-level reuse.

The proposed WePLD position is therefore:

```text
ADOPT THE BEHAVIORAL REQUIREMENTS
STUDY THE STRONGEST SOURCE MECHANISMS
KEEP WEPLD-OWNED CONTRACTS
DEFER SUBSTRATE / LANGUAGE / DEPENDENCY CHOICE
REJECT WHOLESALE PLATFORM TRANSPLANT
```

## Exact public-source anchors inspected in this reconnaissance

These pins are research anchors only. They are not canonical source-registry entries or admitted dependencies.

| Source | Exact research pin | Exact surface inspected | Rights evidence observed | Research disposition |
|---|---|---|---|---|
| `JetBrains/intellij-community` | `6ffe34ff385a21836520b3effc4b9315b4831364` | `platform/ui.jcef/jcef/JBCefApp.java`; `platform/remote-driver/.../JCefUI.kt`; `platform/lvcs-impl/` | `JBCefApp.java` carries an Apache-2.0 source header; repository-wide/per-file third-party audit not completed here | `S+ SOURCE + ARCHITECTURE ORACLE / NOT_ADMITTED` |
| `JetBrains/jcef` | `aaec9cdf5f2e80f9a5e9659a636ac9de8fd25f02` (`dev`) | JCEF repository and `LICENSE.txt` | BSD-style CEF redistribution terms observed at exact pin; bundled/upstream obligations still require full acquisition review | `S+ BROWSER-SUBSTRATE ORACLE / NOT_ADMITTED` |
| `JetBrains/qodana-cli` | `8efeb409ce704bcae711b8b9c2b62b016073ab68` | CLI repository + exact `LICENSE` | Apache-2.0 license observed | `S VERIFICATION ORACLE / NOT_ADMITTED` |
| `agentclientprotocol/agent-client-protocol` | `bb2ef8f713c347523862a0fa351913ea4c10639b` | protocol/schema repository + exact `LICENSE` | Apache-2.0 license observed | `S+ INTEROP CANDIDATE / NOT_ADMITTED` |
| `agentclientprotocol/rust-sdk` | `0541b81fb08e3a633ff1ae8d08eeb8419d7ba0a8` | Rust client/agent/proxy/conductor SDK | repository identifies Apache-2.0; exact transitive review not performed here | `S+ INTEROP SOURCE CANDIDATE / NOT_ADMITTED` |
| `JetBrains/koog` | `a6335272fd7481b3e0daefcacbad3e0c6e4cb4e2` (`develop`) | current framework tree / agent architecture | exact license file was not resolved in this bounded reconnaissance; do not infer admission | `A ARCHITECTURE CANDIDATE / RIGHTS_REVIEW_PENDING` |

Important exact inspected blobs under `intellij-community@6ffe34ff385a21836520b3effc4b9315b4831364`:

```text
platform/ui.jcef/jcef/JBCefApp.java
BLOB = ca9a03d77500dcfa7516513aa99ce719b3a92f6b

platform/remote-driver/test-sdk/src/com/intellij/driver/sdk/ui/components/common/JCefUI.kt
BLOB = 5175d7a3277ca6ce05e7d0051aaff19c414298da
```

`JBCefApp` exposes concrete evidence of a mature browser-owner abstraction: CEF startup/lifecycle ownership, client creation, disposal, version compatibility checks, debugging-port state, and an explicit `ide.browser.jcef.out-of-process.enabled` control. `JCefUI` is particularly relevant to Visual Edit Mode because it injects an element-finder into the real page, evaluates XPath against the live DOM, serializes element metadata, reads `outerHTML`, obtains `getBoundingClientRect()`, checks visibility, scrolls, and dispatches clicks through the host UI.

These are implementation oracles, not instructions to use Java/JVM/JCEF in the final WePLD product.

## JetBrains capability findings

### 1. Embedded browser ownership — JCEF / JBCef

Official IntelliJ Platform documentation describes JCEF as the Java port of Chromium Embedded Framework and exposes `JBCefApp`, `JBCefBrowser`, JavaScript execution, `JBCefJSQuery` for browser→plugin callbacks, and Chrome DevTools access.

Primary references:

- https://plugins.jetbrains.com/docs/intellij/embedded-browser-jcef.html
- https://github.com/JetBrains/intellij-community/tree/6ffe34ff385a21836520b3effc4b9315b4831364/platform/ui.jcef
- https://github.com/JetBrains/jcef/tree/aaec9cdf5f2e80f9a5e9659a636ac9de8fd25f02

**WePLD lesson:** browser ownership is a subsystem, not merely a WebView widget. The future contract should explicitly own browser process/lifecycle state, navigation, page readiness, DevTools/debug transport, browser↔host messaging, crash/restart semantics, cleanup, and evidence capture.

**Do not infer:** JCEF is automatically the correct WePLD implementation substrate. A later Ponytail/Source Acquisition comparison must evaluate native WebView2, CEF-family options, an existing Tauri/webview path, external Chromium/CDP, Playwright-style controlled browser processes, or another minimum-sufficient solution against Windows-first packaging, binary size, security patching, accessibility, cross-platform needs, testability, and exit strategy.

### 2. Deterministic DOM control — Remote Driver `JCefUI`

Exact source at the research pin demonstrates a simple but valuable pattern:

```text
HOST DRIVER
  -> INJECT SMALL PAGE-SIDE ELEMENT FINDER
  -> QUERY LIVE DOM
  -> RETURN STABLE SERIALIZED ELEMENT DATA
  -> READ GEOMETRY / VISIBILITY
  -> SCROLL / CLICK THROUGH CONTROLLED HOST PATH
```

The current implementation supports XPath-based lookup, text lookup, `outerHTML`, page URL/load state, element geometry, scroll, and click.

**WePLD lesson:** the visual-edit picker and the automated browser test interface should share one canonical live-element representation rather than creating separate selector systems for humans, agents, tests, and evidence.

The WePLD representation should be richer than `JCefUI` and must avoid treating XPath as durable source identity.

### 3. Live browser feedback — WebStorm Live Edit

WebStorm 2026.2 documentation confirms immediate browser updates for HTML/CSS/JavaScript during debugging, support for files compiled into those forms (for example TypeScript, Pug, and SCSS), configurable update delay, restart/reload when hot swap fails, and browser highlighting associated with the current editor element.

Reference:

- https://www.jetbrains.com/help/webstorm/live-editing.html

**WePLD lesson:** the preferred visual-edit loop should update the real application through its native dev-server/HMR path where possible. A reload fallback must be explicit and observable rather than silently changing verification semantics.

### 4. Actual DOM synchronization

WebStorm's current Actual HTML DOM tooling reflects the live browser DOM, updates it when the page changes, and synchronizes DOM selection with highlighting in the browser.

Reference:

- https://www.jetbrains.com/help/webstorm/viewing-actual-html-dom.html

**WePLD lesson:** source HTML, framework source, generated browser DOM, and screenshot pixels are distinct identities. Visual Edit Mode must preserve those distinctions and bind them deliberately.

```text
SOURCE_COMPONENT != GENERATED_DOM_NODE
GENERATED_DOM_NODE != DURABLE_SOURCE_IDENTITY
SCREENSHOT_REGION != DOM_IDENTITY
DOM_SELECTION != WRITE_AUTHORITY
```

### 5. Web Inspector / locator round trip

Current JetBrains Web UI Test Automation tooling can select an element on the live page, generate CSS/XPath and role-based Playwright locators, insert locator code, and navigate in the opposite direction from code locator to highlighted browser element.

References:

- https://www.jetbrains.com/help/webstorm/ui-test-automation.html
- https://www.jetbrains.com/help/idea/playwright.html

**WePLD lesson:** Visual Edit should be bidirectional:

```text
BROWSER ELEMENT -> SOURCE / TEST / COMPONENT CONTEXT
SOURCE SYMBOL / LOCATOR -> BROWSER HIGHLIGHT
```

Role/accessibility identity should be first-class alongside DOM selectors because it is often more semantically meaningful and more useful for testing.

### 6. Semantic project intelligence

IntelliJ IDEA's Project Analysis creates a virtual map of classes, methods, objects, code elements, and dependencies that powers completion, inspections, refactoring, navigation, and Find Usages. Find Usages provides impact-oriented symbol search, while Structural Search and Replace operates on source structure rather than treating code as unstructured text.

References:

- https://www.jetbrains.com/help/idea/project-analysis.html
- https://www.jetbrains.com/help/idea/find-highlight-usages.html
- https://www.jetbrains.com/help/idea/structural-search-and-replace.html

**WePLD lesson:** a selected browser element should not be translated into an agent prompt containing only `outerHTML` and a screenshot. The system should resolve, when evidence supports it, the true component/symbol/source range and relevant usages before an edit is proposed.

Target reasoning surface:

```text
LIVE_ELEMENT
  -> FRAMEWORK / SOURCE MAP EVIDENCE
  -> COMPONENT IDENTITY
  -> SOURCE DEFINITION
  -> DESIGN-TOKEN DEPENDENCIES
  -> RELEVANT USAGES
  -> BOUNDED EDIT SCOPE
```

If source mapping is ambiguous, the UI must expose ambiguity rather than pretending the first text match is authoritative.

### 7. Reversible work — Local History

IntelliJ IDEA Local History automatically records project states independently of Git, can recover deleted files, restore individual fragments, roll back larger states, label meaningful checkpoints, and create patches from historical revisions.

Reference:

- https://www.jetbrains.com/help/idea/local-history.html
- https://github.com/JetBrains/intellij-community/tree/6ffe34ff385a21836520b3effc4b9315b4831364/platform/lvcs-impl

**WePLD lesson:** agent-native development needs a local reversible journal beneath Git. Git commits are too coarse to be the only recovery mechanism for rapid visual iteration.

Future behavior candidate:

```text
PRE_AGENT_CHECKPOINT
SELECTION_CONTEXT_CAPTURED
AGENT_PATCH_1
HMR_RENDER_1
DESIGN_FINDINGS_1
AGENT_PATCH_2
FUNCTIONAL_VERIFY_2
USER_ACCEPTED
```

Recovery should support restoring an exact task, file, fragment, or pre-agent state without silently rewriting unrelated work.

### 8. Agent-first execution — JetBrains Air

JetBrains Air is valuable primarily as a behavior/workflow oracle. Current official documentation exposes:

- Plan mode before implementation;
- agent/model selection;
- permission modes such as Plan, Ask, Edit, and Full Access depending on the agent;
- Local Workspace, Git Worktree, and Docker task environments;
- multiple agent tasks in parallel worktrees;
- review of agent diffs before integration;
- a workflow in which one agent implements and a different agent reviews and comments on the result;
- ACP-compatible external agents.

References:

- https://www.jetbrains.com/help/air/plan-mode.html
- https://www.jetbrains.com/help/air/permission-modes.html
- https://www.jetbrains.com/help/air/execution-environments.html
- https://www.jetbrains.com/help/air/review-and-integrate.html
- https://blog.jetbrains.com/air/2026/06/jetbrains-air-lands-on-windows/
- https://blog.jetbrains.com/air/2026/07/what-s-new-air-gets-more-agents-local-models-and-java-kotlin-code-intelligence/

**WePLD lesson:** visual editing should operate inside isolated candidate workspaces by default for material edits and should keep agent choice independent from authority. The user selecting an agent, model, or permission mode is context/configuration; final effect authority and acceptance remain governed by WePLD.

### 9. Agent interoperability — ACP

The Agent Client Protocol standardizes communication between code editors and coding agents. Current public protocol materials use negotiated protocol versions/capabilities rather than asking clients to infer wire compatibility from package versions. The official Rust SDK provides client, agent, proxy, and conductor abstractions; the conductor can compose proxy behavior between editor and agent.

Research pins:

```text
agentclientprotocol/agent-client-protocol
  bb2ef8f713c347523862a0fa351913ea4c10639b

agentclientprotocol/rust-sdk
  0541b81fb08e3a633ff1ae8d08eeb8419d7ba0a8
```

References:

- https://github.com/agentclientprotocol/agent-client-protocol
- https://github.com/agentclientprotocol/rust-sdk
- https://agentclientprotocol.com/

**WePLD lesson:** ACP is a high-priority interoperability candidate because WePLD's product thesis requires replaceable models/workers/tools. A proxy/conductor seam is especially interesting for placing WePLD-owned context, authority, audit, evidence, and redaction mediators between editor/browser surfaces and heterogeneous agents without patching every agent.

Conceptual only:

```text
WEPLD CLIENT
  -> CONTEXT / REDACTION PROXY
  -> AUTHORITY / EFFECT PROXY
  -> AUDIT / EVIDENCE PROXY
  -> ACP-COMPATIBLE AGENT
```

This does not admit ACP or imply that every agent must use ACP.

### 10. Tool exposure and router-only semantics — JetBrains MCP Server

Current JetBrains MCP Server documentation exposes project/IDE tools to external clients, allows tools to be enabled/disabled individually, and supports `Router-only` tools that are removed from the direct MCP tool list and reached through a router when needed. JetBrains explicitly describes this as a way to keep unnecessary tool descriptions out of agent context.

Reference:

- https://www.jetbrains.com/help/rider/mcp-server.html

**WePLD lesson:** tool discovery should be minimum-sufficient and authority-aware rather than shipping a giant permanent tool schema to every agent session.

Conceptual policy surface:

```text
read_file        = ENABLED
search_symbol    = ENABLED
find_usages      = ENABLED
inspect_element  = ENABLED
browser_click    = EFFECT_GATED
terminal_exec    = EFFECT_GATED
write_file       = EFFECT_GATED
commit           = EFFECT_GATED
push             = EFFECT_GATED
merge            = NEVER_DIRECT_AGENT_AUTHORITY
```

Router selection itself must not mint authority.

### 11. Regression-oriented quality gates — Qodana

Qodana's current baseline mechanism stores analysis state in SARIF and classifies later findings as new, unchanged, or absent/resolved. Quality gates can fail CI when thresholds are exceeded. This is a strong model for visual-development verification because it separates pre-existing debt from candidate regressions.

References:

- https://www.jetbrains.com/help/qodana/baseline.html
- https://www.jetbrains.com/help/qodana/quality-gate.html
- https://github.com/JetBrains/qodana-cli/tree/8efeb409ce704bcae711b8b9c2b62b016073ab68

**WePLD lesson:** Browser Studio verification should compare exact before/after evidence, not merely report an absolute design or accessibility score.

Example conceptual gate:

```text
BASELINE
  accessibility_findings = 0
  runtime_errors = 0
  design_findings = 3

CANDIDATE
  accessibility_findings = 1 NEW
  runtime_errors = 0
  design_findings = 1

VERDICT
  REJECT: NEW ACCESSIBILITY REGRESSION
```

A prettier candidate does not erase a new correctness/accessibility regression.

### 12. Structured agent runtime — Koog

Koog is a useful secondary architecture candidate for structured agent workflows, persistence, retry/fault handling, and history/context mechanics. This research intentionally does not make it a primary Browser Studio dependency and did not complete exact rights/transitive evaluation.

Research pin:

```text
JetBrains/koog@a6335272fd7481b3e0daefcacbad3e0c6e4cb4e2
DEFAULT_BRANCH_AT_RESEARCH_TIME = develop
```

Reference:

- https://github.com/JetBrains/koog

**WePLD lesson:** mine mechanisms only if a future Browser Studio or agent-runtime requirement cannot be satisfied more simply by existing WePLD machinery, ACP, stdlib/native platform support, or an already admitted dependency.

## Impeccable integration target

Impeccable is not a JetBrains donor, but it is directly relevant to the founder-requested Browser Studio behavior and should remain a separable design-intelligence layer rather than acceptance authority.

Current Live Mode behavior includes picking a real element in a running dev server, adding comments or strokes, generating multiple variants, hot-swapping them through the framework's HMR path, and writing an accepted variant back to source.

References:

- https://impeccable.style/docs/live/
- https://impeccable.style/live-mode/
- https://impeccable.style/docs/audit/

Proposed composition:

```text
WEPLD LIVE ELEMENT SELECTION
  + TRUE SOURCE / SYMBOL CONTEXT
  + DESIGN SYSTEM CONTEXT
  + OPTIONAL IMPECCABLE CRITIQUE / AUDIT / VARIANTS
  + SELECTED CODING AGENT
  -> ISOLATED CANDIDATE PATCH
  -> LIVE RENDER
  -> WEPLD VERIFICATION + EVIDENCE
```

```text
IMPECCABLE_FINDING != CORRECTNESS
IMPECCABLE_SCORE != ACCEPTANCE_AUTHORITY
VISUAL_PREFERENCE != WRITE_AUTHORITY
```

## Proposed canonical selection-context contract — research candidate only

A future implementation should evaluate a WePLD-owned context object approximately covering the following semantic fields. Field names/types remain unfrozen.

```text
BrowserSelectionContext
  browser_session_identity
  candidate_workspace_identity
  candidate_git_identity
  page_url
  navigation_identity
  viewport
  device_scale
  selected_dom_identity
  selector_candidates
  accessibility_role / name / state
  text_content_summary
  bounding_box
  computed_style_subset
  parent / sibling structural context
  framework_component_candidate
  source_file_candidate
  source_range_candidate
  source_map_evidence
  symbol_identity_candidate
  relevant_usages
  design_token_dependencies
  screenshot_region_identity
  console_evidence_ref
  network_evidence_ref
  selection_ambiguities
```

The actual prompt should receive only the minimum sufficient subset for the requested action. Large DOM dumps, full browser logs, full source trees, or full screenshots should not be sent by default merely because they are available.

## Multi-select and relationship edits

The future UX should support selecting more than one rendered element and expressing relationships rather than forcing the user to verbalize file paths.

Examples:

```text
Select Card A + Card B
"Make B use the same visual language as A without changing B's content."
```

```text
Select Header + Sidebar + Command Palette
"Reduce the visual weight of these three without changing their dimensions."
```

Multi-selection must preserve identity per selected element and must not collapse ambiguity into one broad write scope.

## Direct manipulation and point-to-prompt

Two interaction paths should converge on the same candidate/evidence system:

1. **Point-to-prompt** — select an element and tell a coding/design agent what outcome is wanted.
2. **Direct manipulation** — adjust supported typography/layout/token controls and generate an explicit source patch from the bounded change.

Neither path should mutate canonical source invisibly. Both should produce reviewable candidate changes and preserve before/after evidence.

## Browser Studio architecture candidate

```text
+------------------------------------------------------------------+
|                       WePLD Browser Studio                       |
+------------------------------------------------------------------+
| Browser substrate                                                |
|  - lifecycle / tabs / navigation / viewport / DevTools           |
|  - browser<->host bridge                                         |
+-------------------------------+----------------------------------+
| Live Element Plane            | Runtime Evidence Plane           |
|  - DOM                         |  - console                       |
|  - accessibility              |  - network                       |
|  - geometry                   |  - screenshots                   |
|  - multi-select               |  - page/load state               |
+-------------------------------+----------------------------------+
| Source Resolution Plane                                          |
|  DOM -> framework component -> source map -> symbol -> usages     |
+------------------------------------------------------------------+
| Agent / Design Plane                                              |
|  ACP or adapter -> selected agent -> optional Impeccable          |
+------------------------------------------------------------------+
| Candidate Workspace                                               |
|  isolated edit -> local history checkpoint -> HMR/reload          |
+------------------------------------------------------------------+
| Verification Plane                                                |
|  functional + a11y + runtime + design delta + exact diff          |
+------------------------------------------------------------------+
| Review / Evidence / Acceptance                                    |
|  independent review -> reconciled candidate -> accept/reject      |
+------------------------------------------------------------------+
```

## WePLD differentiator

The differentiator should not be "we also embedded Chromium" or "we also let an agent click buttons." Those are increasingly commodity behaviors.

The stronger product thesis is:

> **Point at anything in the live product, resolve it to trustworthy engineering context, ask any qualified agent for the desired outcome, optionally apply professional design intelligence, then verify and preserve the exact result before acceptance.**

That combines visual directness with WePLD's core authority/evidence philosophy.

```text
POINTING = CONTEXT
AGENT = REPLACEABLE WORKER
DESIGN INTELLIGENCE = ADVISORY
CANDIDATE PATCH = PROPOSED EFFECT
VERIFICATION = EVIDENCE
ACCEPTANCE = SEPARATE AUTHORITY
```

## Adopt / study / reject-now matrix

### Adopt as future behavioral requirement candidates

```text
ADOPT_BEHAVIOR_CANDIDATE:
- point at a real rendered element
- browser <-> source bidirectional highlighting
- multi-select and relational instructions
- accessibility identity beside DOM identity
- exact viewport / geometry / screenshot context
- hot reload with explicit reload fallback
- source/component/symbol/usages resolution
- isolated candidate workspaces for material edits
- reversible pre-Git local history checkpoints
- review-before-apply
- heterogeneous agent support
- tool exposure minimization / router pattern
- before/after regression classification
- deterministic evidence for accepted visual edits
```

### Study exact source before implementation choice

```text
STUDY_SOURCE:
- IntelliJ JBCef lifecycle / JS bridge / DevTools patterns
- IntelliJ Remote Driver JCefUI DOM adapter
- IntelliJ lvcs local-history storage / recovery mechanics
- IntelliJ diff / VCS granular patch-review mechanics
- ACP protocol + Rust SDK proxy/conductor mechanics
- Qodana CLI baseline / SARIF / gate mechanics
- Koog persistence/history/retry only if a concrete gap remains
```

### Reject for the current architecture boundary

```text
REJECT_NOW:
- wholesale IntelliJ Platform transplant
- JVM dependency solely to obtain an embedded browser
- treating XPath/CSS locator as durable source identity
- direct source mutation immediately on element selection
- agent/model selection as effect authority
- design score as acceptance verdict
- visual improvement as permission to regress accessibility/functionality
- automatic external-review egress
- broad permanent tool exposure to every agent
- importing donor code before exact Source Acquisition
- mutating P0+S1..S10 roadmap through this research document
- starting H0-014+ through this research document
```

## Security / trust questions a future implementation must answer

A browser-integrated coding surface materially expands the attack and authority surface. Before implementation, the design must explicitly address at least:

1. navigation to untrusted origins and origin isolation;
2. browser→host message validation and serialization limits;
3. host→page script injection boundaries;
4. DevTools/debug-port exposure;
5. local-file and custom-scheme handling;
6. page content attempting to spoof selection/agent context;
7. cross-origin iframe and shadow-DOM semantics;
8. CSP handling without permanent production weakening;
9. browser downloads/uploads and filesystem effects;
10. clipboard, credentials, cookies, auth sessions, and secrets;
11. console/network evidence redaction;
12. screenshot privacy/redaction;
13. agent browser actions vs human browser actions;
14. write/terminal/process effects initiated after visual selection;
15. crash recovery and orphan browser processes;
16. browser binary/update provenance and security patch cadence;
17. sandbox / out-of-process containment claims;
18. exact candidate binding so browser evidence cannot be reused for a moved head.

```text
UNTRUSTED_PAGE_CONTENT != TRUSTED_INSTRUCTION
DOM_ATTRIBUTE != AUTHORITY
BROWSER_SESSION != REPOSITORY_WRITE_GRANT
BROWSER_AUTOMATION != ACCEPTANCE
```

## Failure oracles to preserve from donor study

Future tests should deliberately include at least:

```text
- selected DOM node has no unique source mapping
- one source component renders many indistinguishable nodes
- one DOM node is composed from multiple source components
- stale source map after HMR
- generated file selected instead of true source
- shadow DOM element
- cross-origin iframe element
- element disappears between selection and action
- layout moves between screenshot and geometry capture
- hot swap fails and reload occurs
- browser crashes during candidate verification
- agent changes a shared component used outside selected page
- design token edit expands blast radius unexpectedly
- accepted-looking visual change introduces keyboard/a11y regression
- console error introduced while visual result improves
- network request introduced unexpectedly
- local-history restore only partially reverts a multi-file patch
- candidate head/workspace changes after evidence capture
```

These negative oracles are more valuable than cloning donor UI chrome.

## Proposed future evaluation sequence — proposal only, not roadmap

If a later canonical task authorizes Browser Studio planning, use a staged evaluation rather than building the full system at once.

### R0 — Browser substrate qualification

Compare the minimum viable browser-control substrates against Windows-first packaging, process isolation, patch/update ownership, accessibility, DevTools/control access, testability, cross-platform exit path, binary size, and license/notice burden.

### R1 — Live element identity

Prove deterministic selection, geometry, accessibility metadata, screenshot-region binding, multi-select, and explicit ambiguity behavior without source writes.

### R2 — Source resolution

Prove browser element -> true source/component/symbol mapping on representative React/Vite and other deliberately selected framework fixtures. Measure ambiguity and false mapping, not just happy-path demos.

### R3 — Isolated edit + reversible history

Apply bounded candidate edits only inside an isolated workspace with exact local-history checkpoints and granular diff review.

### R4 — Design intelligence

Integrate Impeccable or another qualified design-intelligence adapter behind a WePLD-owned advisory contract. Compare useful findings/variants and failure modes without granting it acceptance authority.

### R5 — Verification and evidence

Bind runtime, accessibility, visual, functional, source-diff, and candidate identity evidence. Adopt Qodana-style new/unchanged/resolved classification where useful.

### R6 — Heterogeneous agent interop

Evaluate ACP and non-ACP adapter paths against at least two materially different coding agents. Prove no silent provider/agent substitution and no agent-specific authority assumptions.

```text
R0_R6 = RESEARCH_SEQUENCE_CANDIDATE_ONLY
R0_R6 != ROADMAP_AUTHORITY
```

## Source references

### JetBrains official product / platform documentation

- JCEF embedded browser: https://plugins.jetbrains.com/docs/intellij/embedded-browser-jcef.html
- WebStorm Live Edit: https://www.jetbrains.com/help/webstorm/live-editing.html
- WebStorm Actual HTML DOM: https://www.jetbrains.com/help/webstorm/viewing-actual-html-dom.html
- WebStorm Web UI Test Automation / Web Inspector: https://www.jetbrains.com/help/webstorm/ui-test-automation.html
- IntelliJ Playwright / Web Inspector: https://www.jetbrains.com/help/idea/playwright.html
- IntelliJ Project Analysis: https://www.jetbrains.com/help/idea/project-analysis.html
- IntelliJ Find Usages: https://www.jetbrains.com/help/idea/find-highlight-usages.html
- IntelliJ Structural Search and Replace: https://www.jetbrains.com/help/idea/structural-search-and-replace.html
- IntelliJ Local History: https://www.jetbrains.com/help/idea/local-history.html
- JetBrains Air Plan mode: https://www.jetbrains.com/help/air/plan-mode.html
- JetBrains Air permission modes: https://www.jetbrains.com/help/air/permission-modes.html
- JetBrains Air execution environments: https://www.jetbrains.com/help/air/execution-environments.html
- JetBrains Air review/integration: https://www.jetbrains.com/help/air/review-and-integrate.html
- JetBrains Air Windows / multi-agent review: https://blog.jetbrains.com/air/2026/06/jetbrains-air-lands-on-windows/
- JetBrains Air ACP/agent update: https://blog.jetbrains.com/air/2026/07/what-s-new-air-gets-more-agents-local-models-and-java-kotlin-code-intelligence/
- JetBrains MCP Server: https://www.jetbrains.com/help/rider/mcp-server.html
- Qodana baseline: https://www.jetbrains.com/help/qodana/baseline.html
- Qodana quality gates: https://www.jetbrains.com/help/qodana/quality-gate.html

### Exact public source anchors

- IntelliJ Community: https://github.com/JetBrains/intellij-community/tree/6ffe34ff385a21836520b3effc4b9315b4831364
- `JBCefApp.java`: https://github.com/JetBrains/intellij-community/blob/6ffe34ff385a21836520b3effc4b9315b4831364/platform/ui.jcef/jcef/JBCefApp.java
- Remote Driver `JCefUI.kt`: https://github.com/JetBrains/intellij-community/blob/6ffe34ff385a21836520b3effc4b9315b4831364/platform/remote-driver/test-sdk/src/com/intellij/driver/sdk/ui/components/common/JCefUI.kt
- IntelliJ Local History implementation: https://github.com/JetBrains/intellij-community/tree/6ffe34ff385a21836520b3effc4b9315b4831364/platform/lvcs-impl
- JetBrains JCEF: https://github.com/JetBrains/jcef/tree/aaec9cdf5f2e80f9a5e9659a636ac9de8fd25f02
- Qodana CLI: https://github.com/JetBrains/qodana-cli/tree/8efeb409ce704bcae711b8b9c2b62b016073ab68
- ACP protocol/schema: https://github.com/agentclientprotocol/agent-client-protocol/tree/bb2ef8f713c347523862a0fa351913ea4c10639b
- ACP Rust SDK: https://github.com/agentclientprotocol/rust-sdk/tree/0541b81fb08e3a633ff1ae8d08eeb8419d7ba0a8
- Koog: https://github.com/JetBrains/koog/tree/a6335272fd7481b3e0daefcacbad3e0c6e4cb4e2

### Complementary design-intelligence reference

- Impeccable Live Mode: https://impeccable.style/docs/live/
- Impeccable audit: https://impeccable.style/docs/audit/

## Canonicalization boundary

This reconnaissance is intentionally a discovery artifact only.

It does **not**:

- revise the frozen 402-source registry;
- create source IDs;
- admit JetBrains, ACP, Qodana, Koog, Impeccable, or any browser substrate;
- create a runtime dependency;
- authorize copying donor source into WePLD;
- create Browser Studio product implementation authority;
- change P0+S1..S10 roadmap authority;
- start H0-014 or any later H0 task;
- execute H0-SCREEN;
- authorize model/provider execution;
- authorize external-review egress.

A future canonical task may use this document as bounded evidence for Ponytail and Source Acquisition, but must reverify moving upstream source heads and current official product behavior before making an implementation or admission decision.

```text
JETBRAINS_RECONNAISSANCE = COMPLETE_FOR_DISCOVERY_ARTIFACT
SOURCE_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
ROADMAP_MUTATION = NONE
H0_014_PLUS = NOT_STARTED
```
