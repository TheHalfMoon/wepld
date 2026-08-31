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

## Boundary types

```text
WEB_APPLICATION_TOOL
BROWSER_DIAGNOSTIC_TOOL
BROWSER_ACTUATION_TOOL
```

`WEB_APPLICATION_TOOL` covers WebMCP-class tools exposed by the current web application.

`BROWSER_DIAGNOSTIC_TOOL` covers DevTools-class observations such as DOM/accessibility/console/network/performance/screenshot evidence.

`BROWSER_ACTUATION_TOOL` covers navigation, input, submit, upload/download, or other state-changing browser actions.

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
```

## BrowserSessionObservation

```text
BrowserSessionObservation {
  browser_session_id
  browser_family
  browser_version
  profile_identity
  target_identity
  page_context_id
  current_origin
  current_locator?
  authentication_observed
  private_browsing_state?
  containment_evidence_refs[]
  observed_at
  freshness_generation
}
```

Authentication state is an observation only. Credential material SHOULD remain inaccessible by default and MUST NOT be copied into agent context merely because the browser can use it.

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

Navigation, reload, origin change, target change, profile change, authentication change, WebMCP tool-set change, tool-definition change, containment change, or grant expiry MUST trigger revalidation when material to the effect.

## Execution boundary

Mission Runtime / UWC may execute only the authorized proposal against the exact qualified browser/session/tool context.

Execution must record:

```text
execution_identity
adapter_identity
browser_session_id
page_context_id
pre_effect_origin
pre_effect_tool_generation?
exact input identity
Nawat decision ref
observed result identity
post_effect_origin
postcondition evidence refs[]
error/cancel state?
```

The runtime MUST NOT silently:

- select another browser/profile/session;
- navigate to another origin to make the action succeed;
- substitute a different WebMCP tool;
- downgrade to raw click/type automation;
- use a remote browser/provider;
- consume paid browser infrastructure;
- retry a non-idempotent action without an explicit retry policy.

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

Observation may still expose sensitive information. Each class requires explicit content/egress policy and should minimize captured data.

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
- duplicate invocation would produce a repeated side effect;
- a failed WebMCP call tempts the adapter to silently click UI instead.

## Evidence / Trusted Completion

Browser/WebMCP evidence may contribute to reproduction, verification, review, and completion, but:

```text
BROWSER_TEST_PASS != TRUSTED_COMPLETION
WEBMCP_SUCCESS != TRUSTED_COMPLETION
PAGE_STATE != TRUSTED_COMPLETION
```

Trusted Completion remains owned by the existing WePLD completion boundary and must bind browser evidence to the exact accepted Case/change target where material.
