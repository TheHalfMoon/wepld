# Acceptance — WebMCP and Browser Agent Interoperability

```text
STATUS = FUTURE_PLANNING_ACCEPTANCE
PARENT_SPEC = 006-issueops-agentic-engineering-control-plane
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
BROWSER_EXECUTION_AUTHORITY = NONE
```

This artifact supplements the parent Spec 006 acceptance criteria. It does not activate browser/WebMCP implementation.

## Planning acceptance

The WebMCP/browser feature is planning-complete only if:

- WebMCP is represented as a replaceable protocol candidate rather than core authority;
- the observed WebMCP artifact is correctly described as a Web Machine Learning Community Group Draft, not a W3C Standard/Standards-Track Recommendation;
- WebMCP application tools and DevTools-class browser diagnostics/control remain separate capability paths;
- browser/session/profile/page/origin/tool identity and freshness are explicit;
- website tool metadata, schemas, annotations, read-only hints, outputs, page content, cookies, login state, and DevTools connectivity are non-authoritative evidence;
- WebMCP invocation requires independently derived effect class, Mirefa qualification, exact-context Nawat authorization/revalidation, containment, execution evidence, and postcondition evidence;
- authenticated browser state cannot become implicit user intent or authority;
- no silent fallback exists among WebMCP, DOM automation, DevTools actions, local/remote/headless browsers, browser families, profiles, or sessions;
- WePLD publisher mode exposes safe read/intent/proposal surfaces by default and never turns a WebMCP call into a direct authority grant;
- protocol/browser support is reverified and pinned at owning Source Acquisition time;
- source/dependency/runtime/browser/network authority remains NONE in this planning candidate.

## Security acceptance

Before any live effectful browser/WebMCP tranche:

- tool poisoning and output injection adversarial cases pass;
- misleading `read-only`/annotation claims cannot weaken derived effect classification;
- cross-origin iframe/tool confusion fails closed;
- tool registration/definition changes invalidate stale qualification;
- navigation/origin/profile/session/authentication changes force revalidation where material;
- ambient cookies/SSO/password-manager/autofill state cannot authorize an action;
- sensitive browser observations use minimum necessary capture and explicit egress policy;
- duplicate/retry behavior is explicit for non-idempotent actions;
- failed WebMCP invocation cannot silently downgrade to click/type automation;
- production credentials, destructive actions, uploads/downloads, or authenticated high-impact effects receive applicable independent security review.

## Tracer-bullet acceptance

### WEB-TB0

Offline/local effect-free proof:

```text
local WebMCP fixture
-> WebToolObservation
-> untrusted metadata classification
-> effect classification preview
-> no live Nawat grant
-> evidence report
```

### WEB-TB1

Controlled local browser discovery:

```text
qualified local browser target
-> exact browser/profile/page/origin observation
-> discover WebMCP tools
-> detect tool-generation change
-> preserve provenance
-> zero effectful invocation
```

### WEB-TB2

Synthetic IssueOps browser reproduction:

```text
synthetic web Case
-> controlled browser reproduction
-> qualified DOM/console/screenshot/performance evidence as needed
-> diagnosis
-> deterministic verification
-> exact Case/change binding
```

No production credentials or provider writes.

### WEB-TB3

First bounded live tool effect, only after all owning gates:

```text
explicit user/workflow intent
-> exact controlled WebMCP tool
-> exact browser/page/origin/tool generation
-> preview
-> Mirefa qualification
-> exact Nawat grant
-> invoke once
-> verify postcondition
-> duplicate/retry proof
-> evidence
```

## Trusted Completion

```text
WEBMCP_SUCCESS != TRUSTED_COMPLETION
BROWSER_TEST_PASS != TRUSTED_COMPLETION
PAGE_STATE != TRUSTED_COMPLETION
DEVTOOLS_SUCCESS != TRUSTED_COMPLETION
```

Acceptance-critical browser/web evidence may contribute to Trusted Completion only when bound to the exact accepted Case/change target and current qualified browser/page/tool generation.

## Review gate

Any independent review bound to a predecessor PR #241 head is historical after the WebMCP/browser additions. The fresh final exact-head review must inspect:

- `web-agent.md`;
- `web-agent-tasks.md`;
- `contracts/web-agent-boundary.md`;
- WebMCP/browser changes in `spec.md`, `clarify.md`, `checklists/requirements.md`, and `source-acquisition.md`;
- interaction with the untrusted-content, worker-delegation, RAG, IssueOps, Nawat, Assurance, and Trusted Completion boundaries.

Planning acceptance requires zero unresolved material findings after that exact-head review.
