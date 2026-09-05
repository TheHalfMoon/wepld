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

Make WePLD a first-class governed environment for engineering work on and through the web without making browser state, website-declared tools, MCP servers, cookies, logged-in sessions, browser automation frameworks, downloaded files, or model/provider permissions authoritative.

WePLD should support two primary web-agent families:

1. **WebMCP application tools** — structured tools exposed by a visited web application to a browser agent.
2. **Browser diagnostics/control adapters** — DevTools-class inspection/debugging/performance/DOM/accessibility/network/console plus explicitly classified actuation/artifact/context capabilities.

These are complementary and MUST NOT be collapsed into one trust model.

All normative browser/session/context/tool/proposal/qualification record shapes are owned by `contracts/web-agent-boundary.md`. This product plan intentionally does **not** redeclare `WebToolObservation` or other canonical browser contract shapes.

## 2. Current protocol observations

As observed during planning research on 2026-08-31:

- WebMCP is published by the W3C Web Machine Learning Community Group as a Community Group Draft Report, not a W3C Standard and not on the W3C Standards Track.
- The observed editor set includes Microsoft and Google representatives.
- WebMCP allows web applications to expose JavaScript-backed or declaratively described tools to agents.
- Observed Chrome documentation describes imperative JavaScript and declarative HTML-form-oriented tools plus origin/permissions behavior.
- Observed Microsoft Edge documentation describes `chrome-devtools-mcp` use with Edge/WebView2.

These observations are research evidence only. Exact protocol/browser/editor/support facts must be reverified during owning Source Acquisition. No protocol, browser dependency, MCP server, Puppeteer/Node package, or remote service is admitted here.

## 3. Product capabilities

### 3.1 Web tool discovery

When a qualified browser/session/context route is active, WePLD should discover current WebMCP tools and normalize them into the canonical `WebToolObservation` record.

Tool names, descriptions, schemas, annotations, raw definitions, and outputs are external content. They are evidence for routing/UX and possible effect classification, not authority.

```text
WEBMCP_TOOL_DISCOVERY != AUTHORIZATION
WEBMCP_READ_ONLY_HINT != WEPLD_CONTAINMENT
WEBMCP_TOOL_DESCRIPTION != TRUSTED_INSTRUCTION
WEBMCP_TOOL_OUTPUT != TRUSTED_INSTRUCTION
BROWSER_LOGIN_STATE != NAWAT_GRANT
COOKIE_OR_SESSION_PRESENCE != USER_INTENT
```

### 3.2 Web tool invocation

Invoking a WebMCP tool is an effect proposal:

```text
explicit user/workflow intent
-> canonical WebToolObservation
-> normalized capability/effect classification
-> minimum required context calculation
-> Mirefa route/tool qualification
-> Nawat exact effect-time decision/revalidation
-> browser/session/context containment precondition
-> invocation through qualified browser adapter
-> structured result + browser/page state observation
-> postcondition evidence
```

A site declaring a tool MUST NOT grant permission to invoke it.

### 3.3 Browser diagnostics

A separately qualified DevTools-class surface may support:

- DOM/accessibility inspection;
- console/runtime diagnostics;
- network metadata/content where authorized;
- screenshots and visual evidence;
- performance traces;
- page/application state inspection;
- WebView2/Edge inspection where separately qualified;
- bounded navigation/actuation;
- reproduction evidence;
- automated UI/regression verification.

Diagnostics/control adapters are UWC/tool edges independently qualified from WebMCP application tools.

### 3.4 Browser artifact transfer

Downloads/uploads are explicit governed artifact flows, not incidental browser convenience.

```text
DOWNLOAD
  -> authorized browser effect
  -> bounded staging destination
  -> DownloadObservation
  -> inert InputArtifact
  -> classification/quarantine
  -> separately qualified follow-on use

UPLOAD
  -> explicit authorized InputArtifact
  -> current access-policy check
  -> exact browser context/origin
  -> Nawat grant
  -> transfer
  -> postcondition evidence
```

A browser-created file never automatically executes, parses, enters RAG, or becomes worker-visible.

### 3.5 Multi-context browser behavior

Popups, new tabs, frames, target switches, service/background contexts, clipboard use, file chooser interaction, native dialogs, and permission prompts are separately represented/classified when material.

A new context identity cannot silently inherit the exact target authorization of the previous page merely because one browser session owns both.

## 4. IssueOps integration

A web-related Case may use the web boundary for:

```text
provider issue / synthetic report
-> Case
-> qualified browser context
-> reproduce
-> inspect console/network/DOM/performance
-> discover WebMCP tools when present
-> invoke only explicitly authorized effects
-> capture governed evidence/artifacts
-> diagnose
-> implement/repair through ordinary repository workflow
-> rerun browser verification
-> independent review
-> Trusted Completion decision
```

This enables workflows such as “reproduce this UI issue”, “verify this form”, “inspect this diagnostic page”, and “prove this regression is fixed” without making browser automation a bypass around repository/provider authority.

## 5. Security boundary

### 5.1 Untrusted website content

All page text, DOM/accessibility text, tool descriptions/schemas/outputs, console/network content, screenshots-derived text, clipboard content, downloaded artifacts, and browser-observed data remain untrusted external evidence unless independently classified otherwise.

They MUST NOT by themselves:

- create or alter WorkflowIntent;
- widen filesystem/network/provider/model/artifact access;
- reveal secrets/credentials;
- select paid/remote workers;
- weaken containment;
- authorize tool invocation/navigation/submission/upload/download;
- approve purchase/delete/publish/merge/close effects;
- satisfy independent review;
- produce Trusted Completion.

### 5.2 Authentication and ambient authority

A logged-in browser may hold significant ambient authority. WePLD models browser/profile/authentication state as observation only.

Credential material access is denied by default. Cookies, tokens, autofill, password managers, SSO, clipboard, browser permissions, or an authenticated page do not become WePLD user intent or Nawat authority.

### 5.3 Tool poisoning and output injection

Qualification includes negative oracles for:

- malicious tool descriptions/output;
- schema tricks/oversized fields;
- misleading `read-only` claims;
- tool name collision/re-registration;
- tool-set mutation after qualification;
- origin/navigation/authentication/context changes;
- hidden side effects;
- cross-origin frame/tool confusion;
- replay/duplicate invocation;
- accidental submission/finalization;
- sensitive form-field overcollection;
- browser-profile/session/context mix-ups;
- popup/new-tab target confusion;
- downloaded artifact active-content/parser attack;
- upload path overreach;
- clipboard credential/instruction leakage.

### 5.4 Exact-context revalidation

Before an effectful web/browser action, revalidate all exact fields required by `contracts/web-agent-boundary.md`, including browser session/context/page/origin/tool generation, input/artifact identity, effect class, controlling intent, Mirefa qualification, Nawat grant, containment/access state, expected postcondition, and retry/idempotency identity.

Material navigation, origin, target/frame/context, tool, authentication, profile, containment, access-policy, or grant changes invalidate prior assumptions.

## 6. WebMCP consumer mode

Desired behavior:

- discover/list current tools;
- inspect schemas/annotation claims;
- independently classify likely effects;
- preview exact proposed call/arguments;
- require DecisionBoundary when intent is materially ambiguous;
- invoke only after exact qualification/authority;
- retain structured request/result evidence;
- surface stale tool/origin/context state;
- fail closed on unsupported protocol/browser state.

No automatic invocation occurs merely because a tool is available.

## 7. WePLD publisher mode

A later WePLD surface MAY expose selected WebMCP tools to external browser agents.

Default publisher-mode tools should be safe read/intent/proposal surfaces, for example:

```text
inspect_case
list_case_evidence
propose_triage
request_review
prepare_workflow
```

High-impact operations still create native WePLD effect proposals and traverse normal qualification/Nawat/execution/evidence boundaries.

```text
WEBMCP_CALL_TO_WEPLD != DIRECT_NAWAT_GRANT
```

## 8. Browser diagnostics adapter capability classes

A future UWC adapter may normalize capability classes such as:

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
BROWSER_CLIPBOARD_READ
BROWSER_CLIPBOARD_WRITE
BROWSER_FILE_CHOOSER
BROWSER_PERMISSION_PROMPT
BROWSER_CONTEXT_CREATE_OR_SELECT
BROWSER_OPEN_DEVTOOLS_TARGET
```

Observation, actuation, artifact transfer, and context-control classes remain independently qualified.

## 9. UX

Users should not need protocol knowledge.

Canonical planned web surfaces:

```text
/web inspect
/web tools
/web reproduce <Case>
/web verify <Case>
```

`/askme`, `/issues`, `/debug`, `/review`, `/security`, `/fulltest`, and `/build` may route into web capabilities only when qualified and within the governing autonomy/effect policy.

The UI should show intent/risk/context, for example:

```text
Web tools discovered: 4
Effect classification pending/known
Current origin/context: exact
Authenticated session: observed
No web effect authorized yet
```

Protocol/provider detail belongs in expandable evidence.

## 10. Roadmap placement

### S3

- browser process/session/context identity;
- containment/effect envelopes;
- inert screenshot/page/download evidence intake;
- artifact transfer boundary;
- no WebMCP invocation authority.

### S4

- browser/page/source identity/freshness;
- cited browser observations;
- governed browser artifact/RAG provenance;
- no website-tool authority.

### S5

- `/web` intent surface and routing;
- synthetic/local WebMCP observation/classification/preview;
- prompt-injection/tool-poisoning corpus;
- no live effect required.

### S6

- qualify one browser diagnostics adapter;
- qualify one WebMCP consumer path;
- controlled local discovery;
- Mirefa/Nawat/Mission Runtime contracts;
- exact browser/profile/context/origin identity.

### S7

- browser reproduction/verification evidence;
- web/UI review/security/test evidence;
- tool poisoning/output-injection findings;
- exact target/context/tool-generation binding.

### S8

- bounded authorized WebMCP/navigation/input/submit/artifact/context effects;
- duplicate/retry/unknown-outcome reconciliation;
- IssueOps repair/verify loop;
- browser/provider success still not Trusted Completion.

### S9/S10

- browser evidence timeline/recovery;
- cross-browser qualification matrix;
- organization policies for profiles/origins/effect/artifact classes;
- recurring web intelligence only after lower-slice qualification.

## 11. First tracer bullets

### WEB-TB0 — offline tool semantics

```text
local static fixture
-> canonical WebToolObservation
-> untrusted metadata classification
-> invocation preview
-> no live grant/effect
-> evidence report
```

### WEB-TB1 — controlled local browser discovery

```text
controlled local origin
-> qualified exact browser context
-> discover tools
-> detect tool/context generation changes
-> preserve provenance
-> zero effectful invocation
```

### WEB-TB2 — synthetic IssueOps browser reproduction

```text
synthetic web Case
-> controlled reproduction
-> DOM/console/screenshot/performance evidence as needed
-> diagnosis
-> deterministic verification
-> no production credentials/provider writes
```

### WEB-TB3 — one bounded WebMCP effect

Only after owning gates:

```text
explicit intent
-> exact controlled tool/context
-> effect preview
-> Mirefa qualification
-> exact Nawat grant
-> invoke once
-> verify postcondition
-> prove retry/unknown-outcome semantics
-> evidence
```

A later artifact-transfer tracer bullet should separately prove download -> inert InputArtifact -> quarantine and upload from one exact authorized InputArtifact.

## 12. Qualification criteria

Before live browser/WebMCP activation:

- exact protocol/runtime/browser identities are pinned and qualified;
- browser support is verified rather than assumed;
- browser/profile/session/context/origin identity is explicit;
- cookies/login/password-manager/autofill/clipboard state never become implicit authority;
- tool/page/output/download content remains untrusted;
- tool/context/origin/access changes invalidate stale qualification;
- effect classes are independently derived;
- prompt-injection/tool-poisoning/artifact/multi-context corpus passes structural oracles;
- diagnostics/WebMCP/artifact/context capability paths remain distinct;
- offline/local failure behavior is defined;
- no silent browser/provider/profile/context fallback;
- unsupported states fail closed;
- effectful tranches receive applicable independent security review.

## 13. Source-acquisition candidates

Research candidates include:

```text
WebMCP Community Group specification / webmachinelearning/webmcp
Chrome WebMCP documentation/implementation/test fixtures
Chrome DevTools for agents / chrome-devtools-mcp
Microsoft Edge/WebView2 compatibility guidance
Web Platform Tests for WebMCP
browser security/tool-poisoning/adversarial corpora
```

Reuse mode remains undecided until owning Source Acquisition. No source is admitted by this document.
