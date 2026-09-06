# Contract — Interactive Surfaces

```text
STATUS = FUTURE_PLANNING_CONTRACT
CANONICAL_OWNER_WITHIN_SPEC_006 = INTERACTIVE_SURFACE_INPUT_LEASE_BROWSER_MODE_TYPES_DEFINED_HERE
IMPLEMENTATION_AUTHORITY = NONE
BROWSER_AUTHORITY = NONE
COMPUTER_USE_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
```

This contract defines the future common interaction substrate for Browser and Computer Use. It does not authorize browser launch, browsing, page tools, screen capture, OS accessibility access, mouse/keyboard input, clipboard access, files, network, or remote hosts.

## 1. Core thesis

Browser and Computer Use should share surface identity/freshness/evidence mechanics without becoming one product feature or one ambient permission.

```text
INTERACTIVE_SURFACE != AUTHORITY
OBSERVATION != ACTUATION
SCREEN_CAPTURE != INPUT_AUTHORITY
INPUT_CONTROL != GLOBAL_MACHINE_AUTHORITY
```

## 2. InteractiveSurface

```text
InteractiveSurface {
  surface_id
  host_id
  surface_kind
  owner_process_or_context_identity?
  generation
  geometry?
  focus_state
  visibility_state
  observation_capabilities[]
  interaction_capabilities[]
  origin_or_application_identity?
  created_at
  last_observed_at
}
```

Candidate surface kinds:

```text
BROWSER_PAGE
BROWSER_TAB
DESKTOP_WINDOW
APPLICATION_SURFACE
REMOTE_DESKTOP_SURFACE
MOBILE_SURFACE_LATER
```

A surface generation changes when state relevant to target identity or safe actuation changes according to the owning adapter contract.

## 3. SurfaceObservation

Use the existing `Observation` evidence primitive with typed interactive payloads rather than creating a separate canonical evidence store.

Candidate payload:

```text
SurfaceObservation {
  observation_id
  surface_id
  surface_generation
  observed_at
  semantic_snapshot_ref?
  visual_snapshot_ref?
  navigation_or_application_state?
  focus_state
  target_fingerprints[]
  completeness
  freshness
}
```

Action proposals must identify the observation/preconditions on which target selection depends.

```text
SURFACE_OBSERVATION != CURRENT_SURFACE_STATE
VISUAL_TARGET != STABLE_TARGET
STALE_SURFACE != SAFE_TO_ACT
```

## 4. Action precondition/revalidation flow

```text
observe
-> propose target/action against observation N
-> refresh/revalidate relevant surface preconditions
-> Mirefa qualification evidence current
-> Nawat effect decision/revalidation
-> containment/input-lease preconditions
-> execute
-> post-effect observation
-> effect result/reconciliation
```

If focus, navigation/origin, modal state, document/tool declaration, window geometry, relevant semantic target identity, or another required precondition changed, the action must not blindly execute against stale coordinates or handles.

## 5. Browser modes

Lifecycle ownership and execution location are orthogonal axes. Record `lifecycle_mode = MANAGED | ATTACHED_USER` and `location_mode = LOCAL | REMOTE` with host/session/profile identities. `ManagedBrowser`, `AttachedUserBrowser`, and `RemoteBrowser` remain user-facing route labels; RemoteBrowser is not a mutually exclusive third lifecycle. A remote route may be managed or attached and must satisfy both dimensions' qualification. No combination inherits another combination's credential, containment or recovery evidence.

```text
ManagedBrowser
AttachedUserBrowser
RemoteBrowser
```

### 5.1 ManagedBrowser

A browser/browser-context lifecycle owned by WePLD or a qualified browser host with deliberately scoped profile/session state. This is the preferred default when a managed web environment is sufficient.

### 5.2 AttachedUserBrowser

A route into the user's existing browser/session. It has a larger credential/privacy blast radius and MUST be qualified separately from ManagedBrowser.

### 5.3 RemoteBrowser

A browser on a remote/cloud host. It has distinct host identity, storage/profile state, network origin, credential capabilities, and recovery semantics.

```text
MANAGED_BROWSER != ATTACHED_USER_BROWSER
ATTACHED_USER_BROWSER != AMBIENT_USER_AUTHORITY
REMOTE_BROWSER != LOCAL_BROWSER
REMOTE_BROWSER_STATE != LOCAL_BROWSER_STATE
```

## 6. Browser profile/session state

Cookies, authenticated sessions, local storage, and similar state may carry credential-equivalent authority.

```text
BROWSER_COOKIE_STATE = CREDENTIAL_BEARING_STATE
BROWSER_PROFILE != ORDINARY_CACHE
BROWSER_PROFILE_TRANSFER != ORDINARY_FILE_COPY
```

No default design may silently:

- copy the user's complete browser profile into WePLD;
- synchronize a browser profile to cloud/remote hosts;
- share authenticated state across Projects;
- hand profile state to arbitrary workers;
- retain authenticated state without explicit lifecycle/security policy.

Prefer selective authentication/credential brokering and isolated managed contexts where practical.

## 7. Browser route hierarchy

When semantics are equivalent and the route is currently qualified, prefer:

```text
1. Native Integration / API
2. WebMCP
3. Semantic Browser interaction
4. Browser protocol interaction
5. Visual grounding
6. Raw pointer / keyboard
```

This is a preference, not silent fallback permission. Route constraints and qualification remain explicit.

Playwright-class locators, WebDriver BiDi, CDP, accessibility trees, and similar mechanisms are implementation/source candidates or oracles only after their owning source/dependency gate.

## 8. WebMCP boundary

WebMCP is an untrusted page-declared Browser route.

A candidate WebMCP identity should bind enough state to detect page/tool drift:

```text
WebToolIdentity {
  web_tool_observation_ref
  origin
  browsing_context_id
  navigation_epoch
  document_identity
  tool_name
  schema_digest
  declaration_digest
}
```

This is an identity projection of `WebToolObservation` in `web-agent-boundary.md`, not another canonical observation. The observation records browser session, page/frame context, origin, navigation epoch, document identity, schema and declaration digests plus tool generation; the projection uses those exact values. Missing required context identity prevents invocation. A same-origin navigation or re-declaration may still invalidate the prior tool.

Rules:

```text
WEBMCP_TOOL_DECLARATION = UNTRUSTED_PAGE_INPUT
WEBMCP_TOOL_DESCRIPTION = UNTRUSTED_PAGE_INPUT
WEBMCP_TOOL_SCHEMA != SAFE_EFFECT
WEBMCP_TOOL != TRUSTED_TOOL
WEBMCP_HINT != NAWAT_GRANT
NAVIGATION_MAY_INVALIDATE_PAGE_SCOPED_TOOL_IDENTITY
SCHEMA_CHANGE_INVALIDATES_PRIOR_TOOL_QUALIFICATION_WHERE_RELEVANT
```

Tool output also remains untrusted input. Page-provided safety/consequential annotations may inform AMAN/Mirefa but never decide authority.

## 9. Browser uploads/downloads

```text
DOWNLOADED_FILE = UNTRUSTED_INPUT
FILE_READ_AUTHORITY != UPLOAD_AUTHORITY
DOWNLOAD_AUTHORITY != PARSE_OR_EXECUTE_AUTHORITY
```

Upload may require both bounded local file-read authority and remote/browser effect authority. Download creates an artifact/observation that remains subject to file/content qualification before parsing/execution where those operations are effectful or risky.

## 10. Computer Use route hierarchy

For arbitrary software interaction, prefer:

```text
1. App-native Integration / API
2. OS accessibility / automation API
3. Structured application surface
4. Visual grounding
5. Raw pointer / keyboard
```

Accessibility/automation APIs are semantic interaction routes, not automatic trust. Application-exposed accessibility properties can be stale, incomplete, malicious, or semantically misleading and require qualification appropriate to the effect.

## 11. Computer capability decomposition

Do not model Computer Use as `computer_access = true`.

Candidate capability classes include:

```text
screen_observation
application_observation
window_interaction
pointer_input
keyboard_input
clipboard_read
clipboard_write
file_picker_access
drag_drop
```

Each has separate qualification/security/authority implications.

```text
CLIPBOARD_CAPABILITY != KEYBOARD_CAPABILITY
WINDOW_INTERACTION != FILESYSTEM_AUTHORITY
SCREEN_OBSERVATION != NETWORK_AUTHORITY
```

## 12. InputLease

Raw or ownership-sensitive input actuation should require an expiring/fenced lease.

```text
InputLease {
  input_lease_id
  principal
  host_id
  allowed_surface_refs[]
  allowed_input_classes[]
  issued_at
  expires_at
  fencing_token
  authority_ref
  containment_or_session_ref
}
```

A stale/fenced/expired lease cannot actuate. Worker/host ownership transition fences prior leases before replacement actuation begins.

`InputLease` does not replace Nawat: it is an execution/ownership precondition created under valid authority.

A qualified host actuator owns a serialized input queue and validates the lease, current ownership epoch, surface/session incarnation, focus, target and Nawat decision immediately before emitting each input action. It must reject queued actions from fenced epochs, stop/release held buttons and keys where the platform permits, and report any uncertain residual input state. Worker-held raw OS input access that bypasses this actuator is incompatible with a fencing claim.

OS/GUI routes may lack an atomic compare-and-act operation. Fresh observation, a stable locator or a generation counter does not remove the race between validation and an external UI change. The route must declare its enforceable guarantees and residual race; consequential effects requiring stronger target guarantees must use a qualified semantic/API path, obtain the required human decision, or refuse. Merely asking for approval does not repair an unenforceable target binding. Focus theft/user intervention fences queued work and requires re-observation; an action already emitted may still have an unknown business outcome.

## 13. User intervention

User input during active Computer Use is a causal event, not noise.

A relevant `USER_INTERVENTION` may require:

```text
pause pending actuation
invalidate stale observation
suspend/release input lease
refresh focus/surface state
re-observe
replan/re-authorize when required
```

The agent must not fight the user for cursor/keyboard ownership.

## 14. Security-sensitive surfaces

Qualification/authority must treat security-sensitive surfaces more strictly, including as applicable:

- password managers;
- authentication/credential dialogs;
- OS security/privilege settings;
- secure desktop/UAC-class prompts;
- financial/purchase/payment surfaces;
- destructive administrative controls;
- surfaces exposing unrelated private accounts/data.

The initial architecture must not assume a global allow followed by a growing ad-hoc blocklist.

## 15. Remote/distributed ownership

Remote interaction requires explicit identities:

```text
Host
-> Desktop/Browser Session
-> InteractiveSurface
-> SurfaceObservation
-> InputLease (if actuation needs ownership)
-> Effect execution
```

Required future semantics include lease expiry, fencing, reconnect/recovery, event causality/deduplication, version negotiation, capability refresh, and no split-brain input ownership.

## 16. Effect outcome semantics

A click, keypress, accessibility invocation, WebMCP call, or DOM action finishing locally does not prove the intended business effect occurred.

```text
GUI_ACTION_COMPLETED != BUSINESS_EFFECT_CONFIRMED
BROWSER_ACTION_ACKNOWLEDGED != REMOTE_EFFECT_CONFIRMED
LOCAL_TIMEOUT != REMOTE_EFFECT_NOT_APPLIED
EFFECT_OUTCOME_UNKNOWN != SAFE_TO_RETRY
```

Use post-effect observations and the existing effect-reconciliation contract.

## 17. Future negative-oracle suite

Minimum tests should include:

```text
STALE_COORDINATE_NOT_EXECUTED_AFTER_SURFACE_CHANGE
FOCUS_THEFT_INVALIDATES_RELEVANT_TARGET_PRECONDITION
NAVIGATION_INVALIDATES_PAGE_SCOPED_WEBMCP_TOOL
WEBMCP_DESCRIPTION_CANNOT_MINT_AUTHORITY
WEBMCP_OUTPUT_PROMPT_INJECTION_REMAINS_DATA
ATTACHED_BROWSER_PROFILE_NOT_SILENTLY_COPIED_TO_REMOTE
USER_INTERVENTION_STOPS_STALE_AUTOMATION_INPUT
EXPIRED_INPUT_LEASE_CANNOT_ACTUATE
FENCED_WORKER_CANNOT_CONTINUE_INPUT
CLIPBOARD_PERMISSION_NOT_IMPLIED_BY_KEYBOARD_PERMISSION
DOWNLOAD_DOES_NOT_AUTO_EXECUTE
UPLOAD_REQUIRES_SEPARATE_FILE_READ_AND_EFFECT_AUTHORITY
UNKNOWN_POST_CLICK_EFFECT_RECONCILES_BEFORE_RETRY
```

## 18. Evidence model

Record only evidence needed for explanation, security, recovery, qualification, and completion. Do not require full-video capture as canonical truth.

Material interaction evidence may include:

```text
route qualification
surface identity/generation
relevant observation/snapshot refs
action proposal/preconditions
Nawat decision
InputLease ref where applicable
executed action identity
post-action observation
effect result/reconciliation
security/finding refs
```

Screenshots/visual traces are evidence artifacts where required, not automatically the canonical semantic state of every interaction.
