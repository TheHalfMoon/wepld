# Task Map — WebMCP and Browser Agent Interoperability

```text
STATUS = FUTURE_TASK_MAP_ONLY
PARENT_SPEC = 006-issueops-agentic-engineering-control-plane
CURRENT_ACTIVE_SLICE = S2
ALL_TASKS_ACTIVE = NO
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
BROWSER_EXECUTION_AUTHORITY = NONE
```

These tasks are planning dependencies only. They require activation through the owning slice and canonical build method.

## Planning / acquisition preparation

- [ ] `006-WEB-P001` Reverify current WebMCP specification/status/editors/browser implementation before activation; planning-time support claims are not frozen truth.
- [ ] `006-WEB-P002` Run Ponytail FULL for the exact first WebMCP/browser tranche.
- [ ] `006-WEB-P003` Run Source Acquisition Check for the exact WebMCP specification/revision, browser implementation/test sources, and selected diagnostics adapter.
- [ ] `006-WEB-P004` Determine whether WebMCP is specification oracle, test oracle, protocol adapter input, bounded source donor, or reject; do not assume reuse mode.
- [ ] `006-WEB-P005` Qualify Chrome DevTools MCP/underlying browser-control machinery independently from WebMCP.
- [ ] `006-WEB-P006` Qualify Microsoft Edge/WebView2 compatibility independently from Chrome compatibility.
- [ ] `006-WEB-P007` Define browser profile/session/privacy policy covering cookies, SSO, password managers, autofill, downloads, uploads, clipboard, and private browsing.
- [ ] `006-WEB-P008` Define adversarial WebMCP/browser corpus covering tool poisoning, output injection, origin change, tool mutation, misleading annotations, cross-origin confusion, duplicate invocation, and authenticated-session ambient authority.

## S3 — browser/session identity and containment seam

- [ ] `006-WEB-S3-001` Specify stable WePLD `browser_session_id`, browser target identity, profile identity, page context identity, and origin/freshness observations.
- [ ] `006-WEB-S3-002` Specify browser process/session containment capability report without creating browser execution authority.
- [ ] `006-WEB-S3-003` Define browser effect envelopes for observe, navigate, interact, submit, upload, download, and target-connect classes.
- [ ] `006-WEB-S3-004` Prove authenticated-session/cookie presence creates no authority or WorkflowIntent.
- [ ] `006-WEB-S3-005` Add inert browser evidence intake for screenshot/page observation artifacts.
- [ ] `006-WEB-S3-006` Add Windows-first browser/WebView2 process identity and containment investigation when the owning S3 route permits it.

## S4 — browser evidence / Project Brain integration

- [ ] `006-WEB-S4-001` Define browser/page source identity and freshness semantics for Fehrest evidence.
- [ ] `006-WEB-S4-002` Define citations/locations for DOM/accessibility/console/network/browser evidence where meaningful.
- [ ] `006-WEB-S4-003` Ensure browser observations entering RAG retain origin/session/page-generation/trust provenance.
- [ ] `006-WEB-S4-004` Prove page/browser evidence cannot override stronger exact repository/source facts without surfacing conflict.
- [ ] `006-WEB-S4-005` Prove browser evidence remains advisory and cannot become effect authority or Trusted Completion.

## S5 — workflow and offline WebMCP dry-run

- [ ] `006-WEB-S5-001` Specify `/web` intent surface with at least `inspect`, `tools`, `reproduce`, and `verify` capabilities subject to progressive disclosure.
- [ ] `006-WEB-S5-002` Route eligible `/askme`, `/issues`, `/debug`, `/review`, and `/build` intents into web capabilities without bypassing authority.
- [ ] `006-WEB-S5-003` Implement WEB-TB0 against a local/static WebMCP fixture: discover tool definition -> classify untrusted metadata -> preview invocation -> produce evidence, with no live grant/effect.
- [ ] `006-WEB-S5-004` Normalize WebMCP tool name/title/description/schema/annotation claims into `WebToolObservation`.
- [ ] `006-WEB-S5-005` Treat WebMCP descriptions/schemas/annotations/output as untrusted data and preserve source/trust labels.
- [ ] `006-WEB-S5-006` Independently derive candidate effect class rather than trusting website `read-only` or other annotations.
- [ ] `006-WEB-S5-007` Add prompt-injection/tool-poisoning dry-run corpus proving metadata cannot create WorkflowIntent, select routes, or grant effects.
- [ ] `006-WEB-S5-008` Define WePLD publisher-mode safe surfaces as intent/read/proposal tools only; direct authority remains prohibited.

## S6 — UWC browser interoperability

- [ ] `006-WEB-S6-001` Qualify one browser diagnostics adapter behind UWC.
- [ ] `006-WEB-S6-002` Qualify one WebMCP consumer route against an exact protocol/browser version on a controlled local origin.
- [ ] `006-WEB-S6-003` Implement WEB-TB1: controlled local browser WebMCP discovery with tool-generation change detection and zero effectful invocation.
- [ ] `006-WEB-S6-004` Specify `WebRouteQualification` between browser capability observation and Nawat.
- [ ] `006-WEB-S6-005` Prove WebMCP tool discovery/availability cannot mint Nawat authority.
- [ ] `006-WEB-S6-006` Prove WebMCP `read-only`/untrusted-content annotations remain claims until independently classified/qualified.
- [ ] `006-WEB-S6-007` Implement exact browser/profile/page/origin/tool-generation snapshot passed to Nawat.
- [ ] `006-WEB-S6-008` Prove Mission Runtime/UWC cannot silently substitute WebMCP with DOM click/type or DevTools action.
- [ ] `006-WEB-S6-009` Prove no silent browser/profile/session/remote-provider fallback.
- [ ] `006-WEB-S6-010` Normalize DevTools-class observation capabilities separately from effectful browser controls.
- [ ] `006-WEB-S6-011` Qualify Edge/WebView2 target behavior separately if activated.

## S7 — browser/web assurance

- [ ] `006-WEB-S7-001` Implement WEB-TB2: one synthetic web Case -> controlled reproduction -> DOM/console/screenshot evidence -> diagnosis -> deterministic local verification.
- [ ] `006-WEB-S7-002` Bind browser reproduction/verification evidence to exact Case/change target and browser/page generation.
- [ ] `006-WEB-S7-003` Add independent web/UI regression review route where material.
- [ ] `006-WEB-S7-004` Add WebMCP tool-poisoning, output-injection, misrepresented-intent, and sensitive-parameter findings.
- [ ] `006-WEB-S7-005` Prove successful prompt-level manipulation cannot bypass Nawat or independent review boundaries.
- [ ] `006-WEB-S7-006` Invalidate acceptance-critical browser evidence when target/page/origin/tool generation changes materially.

## S8 — controlled browser/WebMCP actuation

- [ ] `006-WEB-S8-001` Implement WEB-TB3 on a controlled local test page: explicit intent -> exact tool -> preview -> exact Nawat grant -> invoke once -> verify postcondition -> evidence.
- [ ] `006-WEB-S8-002` Implement duplicate/retry/idempotency protection for WebMCP actions.
- [ ] `006-WEB-S8-003` Implement separate effect classes for navigation, interaction, submit, upload, and download.
- [ ] `006-WEB-S8-004` Revalidate after material navigation, origin, authentication, profile, target, tool-set, definition, containment, or grant-expiry changes.
- [ ] `006-WEB-S8-005` Fail closed when WebMCP becomes unavailable; do not silently downgrade to raw automation.
- [ ] `006-WEB-S8-006` Integrate controlled browser reproduce/repair/verify loop into one IssueOps Case.
- [ ] `006-WEB-S8-007` Prove browser success, WebMCP success, or page state cannot directly create Trusted Completion.
- [ ] `006-WEB-S8-008` Require applicable independent security review before any tranche uses production credentials, uploads/downloads, destructive web actions, or authenticated high-impact effects.

## S9/S10 — evidence, policy, and scale

- [ ] `006-WEB-S9-001` Link browser/session/tool observations, proposed effects, Nawat decisions, invocations, diagnostics, and verification into the Case evidence timeline.
- [ ] `006-WEB-S9-002` Add recovery/checkpoint behavior for interrupted browser sessions without silently changing profiles/targets.
- [ ] `006-WEB-S9-003` Add audit export that preserves browser/origin/tool generation and sensitive-data redaction/classification.
- [ ] `006-WEB-S10-001` Add organization policy for permitted origins, browser profiles, web effect classes, and remote browser providers only after lower-slice qualification.
- [ ] `006-WEB-S10-002` Add cross-browser/browser-version qualification matrix only from measured evidence.
- [ ] `006-WEB-S10-003` Add recurring browser/web regression intelligence only after controlled single-Case browser workflows are trustworthy.

## Required invariants

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
BROWSER_TEST_PASS != TRUSTED_COMPLETION
WEBMCP_SUCCESS != TRUSTED_COMPLETION
NO_SILENT_BROWSER_ROUTE_FALLBACK = REQUIRED
```
