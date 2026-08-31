# Web Agent Interoperability — WebMCP + Browser Diagnostics

```text
STATUS = FUTURE_PLANNING_CANDIDATE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
BROWSER_EXECUTION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
```

## 1. Objective

Make WePLD a first-class governed environment for engineering work on and through the web without making browser state, website-declared tools, MCP servers, cookies, logged-in sessions, browser automation frameworks, or model/provider permissions authoritative.

WePLD should support two distinct web-agent boundaries:

1. **WebMCP application tools** — structured tools exposed by a visited web application to a browser agent.
2. **Browser diagnostics/control adapters** — DevTools-class inspection, debugging, performance, DOM/accessibility, screenshot, network, console, and controlled browser actuation capabilities.

These are complementary and MUST NOT be collapsed into one trust model.

## 2. Current protocol observations

As observed during planning research on 2026-08-31:

- WebMCP is published by the W3C Web Machine Learning Community Group as a Community Group Draft Report, not a W3C Standard and not on the W3C Standards Track.
- The current editor set includes Microsoft and Google representatives.
- WebMCP allows web applications to expose JavaScript-backed or declaratively described tools to agents.
- Current Chrome documentation describes both imperative JavaScript tools and declarative HTML-form-based tools.
- Current Chrome documentation describes origin-isolation and `tools` Permissions Policy requirements.
- Current Microsoft Edge documentation documents use of `chrome-devtools-mcp` against Edge and WebView2 for agent-driven inspection/debugging/control.

These observations are research evidence only. They do not admit a protocol, browser dependency, MCP server, Puppeteer, Node.js package, or remote service.

## 3. Product capabilities

### 3.1 Web tool discovery

When a qualified browser/session route is active, WePLD should be able to discover WebMCP tools exposed by the current top-level application context and represent each tool as an untrusted capability claim.

Candidate normalized fields:

```text
WebToolObservation {
  web_tool_observation_id
  browser_session_id
  page_context_id
  origin_identity
  page_identity
  tool_name
  tool_title?
  description?
  input_schema_identity?
  declared_annotations[]
  discovery_generation
  observed_at
  raw_protocol_evidence_ref
  trust_class = UNTRUSTED_EXTERNAL_CAPABILITY_CLAIM
}
```

Tool names, descriptions, schemas, annotations, and outputs are external content. They are evidence for routing and UX, not authority.

### 3.2 Web tool invocation

Invoking a WebMCP tool is an effect proposal.

```text
user/workflow intent
-> discovered WebToolObservation
-> normalized capability/effect classification
-> required data/context calculation
-> Mirefa route/tool qualification
-> Nawat exact effect-time decision/revalidation
-> browser/session containment precondition
-> invocation through qualified browser adapter
-> structured result + browser/page state observation
-> postcondition evidence
```

A site declaring a tool MUST NOT grant permission to invoke it.

```text
WEBMCP_TOOL_DISCOVERY != AUTHORIZATION
WEBMCP_READ_ONLY_HINT != WEPLD_CONTAINMENT
WEBMCP_TOOL_DESCRIPTION != TRUSTED_INSTRUCTION
WEBMCP_TOOL_OUTPUT != TRUSTED_INSTRUCTION
BROWSER_LOGIN_STATE != NAWAT_GRANT
COOKIE_OR_SESSION_PRESENCE != USER_INTENT
```

### 3.3 Browser diagnostics

WePLD should support a separately qualified DevTools-class capability surface for engineering workflows such as:

- inspect live DOM/accessibility state;
- console and runtime diagnostics;
- network request/response inspection where authorized;
- screenshots and visual evidence;
- performance traces;
- page/application state inspection;
- WebView2 inspection on Windows where qualified;
- bounded browser navigation and actuation;
- reproduction evidence for web issues;
- automated UI/regression verification.

Diagnostics/control adapters are worker/tool edges behind UWC and are independently qualified from WebMCP application tools.

### 3.4 IssueOps integration

A web-related Case may use the web boundary for:

```text
GitHub/Sentry/provider issue
-> Case
-> launch/connect qualified browser context
-> reproduce reported behavior
-> inspect console/network/DOM/performance
-> discover WebMCP tools when present
-> invoke only explicitly authorized tools/effects
-> capture evidence
-> diagnose
-> implement/repair through ordinary governed repository workflow
-> rerun browser verification
-> independent review
-> Trusted Completion
```

This should enable high-value IssueOps workflows such as "reproduce this UI issue," "verify this form," "inspect this production-safe diagnostic page," and "prove this regression is fixed" without making browser automation a bypass around repository or provider authority.

## 4. Security boundary

### 4.1 Untrusted website content

All page text, DOM content, accessibility text, tool descriptions, tool schemas, tool outputs, console output, network content, screenshots, and browser-observed application data are untrusted external evidence unless independently classified otherwise.

They MUST NOT by themselves:

- create or alter WorkflowIntent;
- widen filesystem/network/provider/model access;
- reveal secrets or credentials;
- select a paid remote worker;
- weaken containment;
- authorize a tool invocation;
- authorize navigation to a new origin;
- approve a purchase/submission/delete/publish/merge/close effect;
- satisfy independent review;
- produce Trusted Completion.

### 4.2 Authentication and ambient authority

A logged-in browser can contain substantial ambient authority. WePLD MUST model this explicitly.

Candidate state:

```text
BrowserAuthorityContext {
  browser_session_id
  profile_identity
  origin_identity
  authentication_observed
  credential_material_access = DENIED_BY_DEFAULT
  session_capability_claims[]
  approved_effect_classes[]
  containment_evidence[]
  expiry/revalidation
}
```

The existence of cookies, authentication tokens, browser autofill, password managers, enterprise SSO, or an already authenticated page is not authorization for WePLD to use those capabilities.

### 4.3 Tool poisoning and output injection

WebMCP metadata and outputs must pass the same untrusted-content boundary planned for IssueOps/RAG. Tool descriptions and structured outputs may contain prompt injection or misleading intent descriptions.

Qualification MUST include negative oracles for:

- malicious tool descriptions;
- schema tricks and oversized fields;
- misleading `read-only`/annotation claims;
- output injection;
- tool name collisions;
- tool-set changes after qualification;
- navigation/origin changes between discovery and invocation;
- stale page/tool generation;
- hidden side effects behind apparently read-only tools;
- cross-origin frame/tool confusion;
- replay/duplicate invocation;
- accidental submission/finalization;
- sensitive form-field overcollection;
- browser-profile/session mix-ups.

### 4.4 Exact-context revalidation

Before an effectful web invocation, the implementation must revalidate at least:

```text
browser_session_id
page_context_id
current origin
current page/document identity or qualified freshness observation
current WebMCP tool generation/definition identity
exact tool name
input identity
classified effect class
user/workflow intent
Mirefa qualification freshness
Nawat grant
containment state
expected postcondition
idempotency/retry identity where applicable
```

Navigation, reload, origin changes, tool registration changes, authentication changes, or stale context invalidate acceptance-critical prior assumptions.

## 5. WebMCP consumer mode

WePLD should eventually consume website-exposed WebMCP tools through a replaceable browser adapter.

Desired behavior:

- list/discover current tools;
- inspect schemas and annotations;
- classify likely read/write/external/financial/destructive effects independently of website labels;
- preview proposed call and required arguments;
- require DecisionBoundary when user intent is materially ambiguous;
- invoke only after exact effect authorization;
- retain structured request/result evidence;
- surface tool-set changes and stale observations;
- fail closed when the browser/runtime does not support the qualified protocol version.

No automatic call should occur simply because a tool is available.

## 6. WePLD publisher mode

A later WePLD web/Desktop surface MAY expose selected WePLD capabilities through WebMCP so browser agents can collaborate with WePLD.

This is a separate capability and MUST expose only safe intent/proposal surfaces rather than direct authority.

Candidate examples:

```text
inspect_case
list_case_evidence
propose_triage
request_review
prepare_workflow
```

High-impact operations such as merge, close, delete, provider write, shell/process execution, filesystem mutation, credential use, or paid worker execution SHOULD NOT be exposed as direct browser-owned authority surfaces. If ever exposed, the tool creates a WePLD effect proposal and still passes the complete native authority pipeline.

```text
WEBMCP_CALL_TO_WEPLD != DIRECT_NAWAT_GRANT
```

## 7. Browser diagnostics adapter

A future DevTools-class adapter should normalize browser inspection/control into UWC capabilities rather than making `chrome-devtools-mcp`, Chrome, Edge, WebView2, Puppeteer, or another implementation the architecture.

Candidate normalized capability classes:

```text
BROWSER_OBSERVE_PAGE
BROWSER_OBSERVE_DOM
BROWSER_OBSERVE_ACCESSIBILITY
BROWSER_OBSERVE_CONSOLE
BROWSER_OBSERVE_NETWORK
BROWSER_CAPTURE_SCREENSHOT
BROWSER_CAPTURE_PERFORMANCE
BROWSER_NAVIGATE
BROWSER_INTERACT
BROWSER_SUBMIT
BROWSER_DOWNLOAD
BROWSER_UPLOAD
BROWSER_OPEN_DEVTOOLS_TARGET
```

Read/observe classes and effectful navigation/interaction/upload/download/submit classes MUST be independently classified.

## 8. UX

The user-facing product should not require protocol knowledge.

Candidate surfaces:

```text
/web inspect
/web tools
/web reproduce <Case>
/web verify <Case>
```

`/askme`, `/issues`, `/debug`, `/review`, and `/build` may route into these capabilities automatically when qualified and within the current autonomy ceiling.

The default UI should show intent and risk, for example:

```text
Web tools discovered: 4
Read-only candidates: 2
Effectful candidates: 2
Current origin: example.com
Authenticated session: observed
No web effect authorized yet
```

Protocol/provider detail belongs in expandable evidence.

## 9. Roadmap placement

### S3 — browser/process containment prerequisite

- browser process/session identity;
- local browser-target discovery seam;
- containment/effect envelopes;
- inert screenshot/page evidence intake;
- no WebMCP invocation authority.

### S4 — browser evidence into Project Brain

- page/source identity and freshness;
- cited browser observations where useful;
- web evidence provenance;
- no website tool authority.

### S5 — workflow integration / dry run

- `/web` intent surface and `/askme` routing;
- WebMCP tool observations against synthetic/local fixtures;
- tool classification and invocation preview only;
- prompt-injection/tool-poisoning adversarial corpus;
- no live effectful browser invocation required.

### S6 — browser/UWC interoperability

- qualify one browser diagnostics adapter;
- qualify WebMCP consumer protocol candidate;
- WebMCP discovery on a controlled local test page;
- Mirefa/Nawat/Mission Runtime contracts for browser effects;
- explicit browser session/profile/origin identity.

### S7 — assurance

- browser-based reproduction/verification evidence;
- independent UI/web regression review;
- tool poisoning/output injection findings;
- exact browser/page/tool generation binding.

### S8 — controlled actuation

- bounded authorized WebMCP invocation;
- controlled navigation/input/submit flows;
- duplicate/retry/idempotency protection;
- IssueOps repair-and-verify loop;
- no provider/browser state automatically establishes Trusted Completion.

### S9/S10 — evidence and scale

- browser evidence timeline/recovery;
- cross-browser qualification matrix;
- organization policy for browser profiles/origins/actions;
- recurring web regression and issue intelligence only after lower slices qualify.

## 10. First tracer bullets

### WEB-TB0 — offline tool semantics

```text
local static WebMCP fixture
-> tool discovery observation
-> classify untrusted metadata
-> preview proposed invocation
-> Nawat = no live grant
-> evidence report
```

No network and no browser effect required.

### WEB-TB1 — controlled local browser discovery

```text
controlled local origin
-> qualified browser target
-> discover WebMCP tools
-> detect tool-set generation change
-> preserve provenance
-> no effectful tool invocation
```

### WEB-TB2 — browser diagnostics for one synthetic IssueOps Case

```text
synthetic web Case
-> controlled browser reproduction
-> console/DOM/screenshot evidence
-> diagnosis evidence
-> deterministic local verification
-> no production credentials/provider writes
```

### WEB-TB3 — one bounded WebMCP effect

Only after Source Acquisition, protocol/runtime qualification, browser containment, Nawat integration, and applicable security review:

```text
explicit user intent
-> exact local test-page tool
-> effect preview
-> exact Nawat grant
-> invoke once
-> verify postcondition
-> prove duplicate/retry protection
-> evidence
```

## 11. Candidate qualification criteria

Before live browser/WebMCP activation:

- exact protocol/runtime version is pinned and qualified;
- current browser support is verified rather than assumed;
- secure-origin/origin-isolation/permissions behavior is tested where applicable;
- browser profile/session identity is explicit;
- cookies/login state never become implicit authority;
- tool metadata/output is treated as untrusted content;
- tool generation/origin changes invalidate stale qualification;
- effect classes are independently derived rather than copied from website hints;
- prompt injection/tool poisoning/output injection corpus passes structural negative oracles;
- browser diagnostics and WebMCP tool invocation remain distinct capability paths;
- offline/local failure behavior is defined;
- provider/browser fallback is explicit and never silent;
- unsupported protocol/browser states fail closed;
- final security review is independently qualified for any effectful tranche.

## 12. Source-acquisition candidates

Research candidates for later governed acquisition include:

```text
WebMCP Community Group specification / webmachinelearning/webmcp
Chrome WebMCP documentation and implementation/test fixtures
Chrome DevTools for agents / chrome-devtools-mcp
Microsoft Edge/WebView2 compatibility guidance for chrome-devtools-mcp
Web Platform Tests for WebMCP
browser security/tool-poisoning adversarial corpora
```

Reuse mode is intentionally undecided. Each source may become a specification oracle, behavior oracle, test/fixture source, protocol adapter candidate, bounded source donor, or rejection after the owning Source Acquisition Check.

No source is admitted by this document.
