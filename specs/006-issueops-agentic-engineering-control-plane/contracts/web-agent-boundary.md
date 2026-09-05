# Contract — Web Agent Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
BROWSER_EXECUTION_AUTHORITY = NONE
```

## Purpose

Define a WePLD-owned boundary for browser-native web tools and browser diagnostics/control so that WebMCP, MCP servers, browser sessions, DevTools protocols, page content, and provider-native permissions remain replaceable external edges rather than authority.

This file is the canonical owner of `BrowserSessionObservation`, `BrowserContextObservation`, `WebToolObservation`, `WebToolInvocationProposal`, and `WebRouteQualification` semantic shapes. Other planning files reference these shapes rather than redeclare incompatible variants.

## Boundary types

```text
WEB_APPLICATION_TOOL
BROWSER_DIAGNOSTIC_TOOL
BROWSER_ACTUATION_TOOL
BROWSER_ARTIFACT_TRANSFER
BROWSER_CONTEXT_CONTROL
```

`WEB_APPLICATION_TOOL` covers WebMCP-class tools exposed by the current web application.

`BROWSER_DIAGNOSTIC_TOOL` covers DevTools-class observations such as DOM/accessibility/console/network/performance/screenshot evidence.

`BROWSER_ACTUATION_TOOL` covers navigation, input, submit, or other state-changing browser actions.

`BROWSER_ARTIFACT_TRANSFER` covers upload/download/file-chooser operations and must integrate with the canonical `InputArtifact`/artifact-transfer boundary.

`BROWSER_CONTEXT_CONTROL` covers popup/new-tab/frame/target creation or selection, clipboard access, browser permission prompts, and other ambient browser context changes.

These classes MUST NOT be conflated merely because one adapter exposes all of them.

## Core invariants

```text
WEBMCP_TOOL != NAWAT_GRANT
WEBMCP_ANNOTATION != VERIFIED_EFFECT_CLASS
WEBMCP_READ_ONLY_HINT != WEPLD_CONTAINMENT
WEBMCP_OUTPUT != TRUSTED_INSTRUCTION
PAGE_CONTENT != TRUSTED_INSTRUCTION
BROWSER_SESSION != WEPLD_AUTHORITY
AUTHENTICATED_BROWSER != AUTHORIZED_ACTION
COOKIE_PRESENCE != USER_INTENT
DEVTOOLS_CONNECTION != EXECUTION_AUTHORITY
BROWSER_AUTOMATION_PERMISSION != TRUSTED_COMPLETION
DOWNLOAD_COMPLETE != SAFE_ARTIFACT
UPLOAD_PATH_VISIBLE != UPLOAD_AUTHORITY
CLIPBOARD_AVAILABLE != CLIPBOARD_AUTHORITY
POPUP_CREATED != POPUP_TARGET_AUTHORIZED
```

## BrowserSessionObservation

```text
BrowserSessionObservation {
  browser_session_id
  browser_family
  browser_version
  profile_identity
  process_or_runtime_identity?
  containment_evidence_refs[]
  authentication_observed
  private_browsing_state?
  observed_at
  freshness_generation
}
```

Authentication state is an observation only. Credential material SHOULD remain inaccessible by default and MUST NOT be copied into agent context merely because the browser can use it.

## BrowserContextObservation

A browser session may contain multiple targets/tabs/windows/frames. Every effect/observation binds one exact context.

```text
BrowserContextObservation {
  browser_context_id
  browser_session_id
  target_identity
  parent_or_opener_context_id?
  frame_identity?
  page_context_id
  origin_identity
  current_locator?
  context_kind
  lifecycle_state
  observed_at
  freshness_generation
}
```

Candidate context kinds:

```text
TOP_LEVEL_PAGE
POPUP_OR_NEW_TAB
FRAME
WORKER_OR_BACKGROUND_CONTEXT
OTHER_QUALIFIED_TARGET
```

Ambiguous target selection fails closed. A new popup/frame/tab is a new context identity rather than implicit continuation of the old effect target.

## WebToolObservation

```text
WebToolObservation {
  web_tool_observation_id
  browser_session_id
  page_context_id
  origin_identity
  tool_name
  tool_title?
  description?
  input_schema_identity?
  annotation_claims[]
  raw_definition_identity
  tool_generation
  observed_at
  trust_class = UNTRUSTED_EXTERNAL_CAPABILITY_CLAIM
}
```

A changed tool definition creates a new observation/generation. Acceptance-critical invocation MUST NOT reuse qualification bound to a superseded definition.

## WebToolInvocationProposal

```text
WebToolInvocationProposal {
  proposal_id
  workflow_intent_ref
  web_tool_observation_ref
  exact_browser_session_id
  exact_page_context_id
  exact_origin
  exact_tool_generation
  input_identity
  derived_effect_class
  required_context_refs[]
  expected_postcondition
  idempotency_identity?
}
```

Website annotations MAY inform classification but cannot decide the final effect class.

## Browser artifact transfer

Downloads and uploads use explicit artifact identities.

### Download

```text
browser context
-> authorized download effect
-> bounded destination/staging policy
-> DownloadObservation
-> inert InputArtifact
-> classification/quarantine
-> optional separately qualified parser/use action
```

A downloaded file does not execute, parse, enter RAG, or become worker-visible merely because the browser created it.

### Upload

```text
explicit InputArtifact
-> current access-policy check
-> explicit upload proposal
-> exact browser context/origin/control identity
-> Nawat grant
-> transfer
-> postcondition evidence
```

The browser adapter MUST NOT browse arbitrary filesystem paths or substitute another file when the authorized artifact becomes unavailable.

## Clipboard, file chooser, permission prompt, and native dialog effects

These are separate effect classes when supported:

```text
CLIPBOARD_READ
CLIPBOARD_WRITE
FILE_CHOOSER_SELECT_ARTIFACT
BROWSER_PERMISSION_PROMPT_ACCEPT
BROWSER_PERMISSION_PROMPT_DENY
NATIVE_DIALOG_INTERACTION
POPUP_OR_CONTEXT_CREATE
POPUP_OR_CONTEXT_CLOSE
```

OS/browser availability does not authorize these effects. A permission prompt is evidence of a browser request, not a user approval recorded by WePLD.

## Qualification boundary

Mirefa candidate output:

```text
WebRouteQualification {
  qualification_id
  proposal_id
  browser_adapter_identity
  protocol_identity
  target_browser_version
  supported_operation
  derived_effect_class
  origin_constraints
  context_constraints
  containment_requirements
  trust/input constraints
  qualification_evidence_refs[]
  expires_at_or_generation
  outcome = QUALIFIED | REFUSED | STALE | UNKNOWN
}
```

Qualification does not grant execution.

## Authority boundary

Nawat receives the complete exact-context snapshot and may return:

```text
ALLOW
DENY
REQUIRE_APPROVAL
TRANSFORM
REQUALIFY
```

A valid allow/grant is scoped to the exact classified web/browser effect. It cannot be widened by Mission Runtime or the browser adapter.

Navigation, reload, origin change, target/context/frame change, profile change, authentication change, WebMCP tool-set change, tool-definition change, containment change, access-policy change, or grant expiry MUST trigger revalidation when material to the effect.

## Execution boundary

Mission Runtime / UWC may execute only the authorized proposal against the exact qualified browser/session/context/tool state.

Execution must record:

```text
execution_identity
adapter_identity
browser_session_id
browser_context_id/page_context_id
pre_effect_origin
pre_effect_tool_generation?
exact input/artifact identity
Nawat decision ref
observed result identity
post_effect_origin
post_effect_context_identity
postcondition evidence refs[]
error/cancel/unknown-outcome state?
```

The runtime MUST NOT silently:

- select another browser/profile/session/context/frame;
- navigate to another origin to make the action succeed;
- substitute a different WebMCP tool;
- downgrade to raw click/type automation;
- use a remote browser/provider;
- consume paid browser infrastructure;
- select a different upload artifact/path;
- accept a download as trusted input;
- retry a non-idempotent action whose outcome is unknown without reconciliation.

A crash/disconnect after a browser submission may create the canonical `EFFECT_OUTCOME_UNKNOWN` state and must be reconciled before unsafe retry.

## Discovery-only path

Read-only discovery still treats tool metadata as untrusted data.

```text
browser observation
-> tool discovery
-> untrusted WebToolObservation
-> evidence/UI
```

Discovery alone creates no invocation proposal or authority.

## DevTools diagnostics path

Browser diagnostics are separately classified:

```text
observe DOM/accessibility
observe console
observe network metadata/content
capture screenshot
capture performance trace
```

Observation may still expose sensitive information. Each class requires explicit content/access/handling/egress policy and should minimize captured data.

A diagnostic MCP server or DevTools connection is a transport/tool edge only.

## Fallback policy

No silent fallback between:

```text
WebMCP structured tool
DOM click/type automation
DevTools protocol action
remote browser service
headless browser
local browser
Chrome
Edge
WebView2
another browser profile/session/context/frame
```

If the selected path becomes unavailable or stale, fail closed or surface an explicitly qualified alternative.

## Prompt injection / tool poisoning

The untrusted-content contract applies to:

```text
page text
DOM/accessibility content
tool names/descriptions
schemas
annotations
tool outputs
console output
network content
screenshots-derived text
downloaded artifact metadata/content
clipboard content
```

These inputs cannot alter authority or control-plane instructions merely through content.

Required negative oracles include:

- tool description asks the agent to ignore policy;
- tool output asks for secrets or broader access;
- `read-only` annotation hides a state-changing implementation;
- page mutates tool definitions after discovery;
- same tool name is re-registered with different semantics;
- origin changes after the proposal is formed;
- cross-origin iframe exposes unexpected tools;
- user is logged in but has not authorized the requested action;
- popup/new tab appears and adapter silently switches target;
- downloaded file attempts active execution or parser exploitation;
- upload selector exposes unauthorized local paths;
- clipboard contains instructions/credentials outside authorized scope;
- duplicate invocation would produce a repeated side effect;
- a failed WebMCP call tempts the adapter to silently click UI instead.

## Evidence / Trusted Completion

Browser/WebMCP evidence may contribute to reproduction, verification, review, and completion, but:

```text
BROWSER_TEST_PASS != TRUSTED_COMPLETION
WEBMCP_SUCCESS != TRUSTED_COMPLETION
PAGE_STATE != TRUSTED_COMPLETION
DOWNLOAD_SUCCESS != TRUSTED_COMPLETION
```

Trusted Completion remains owned by the existing WePLD completion boundary and must bind browser evidence to the exact accepted Case/change/browser context and current handling/access policy where material.
