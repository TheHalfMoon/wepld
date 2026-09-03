# Omnigent Qualified Mechanism Extraction — 2026-09-04

```text
STATUS = RESEARCH_INPUT_ONLY
UPSTREAM = omnigent-ai/omnigent
PINNED_REVISION = f4e93c2b74158a2712d07f13e591abb90a999171
OBSERVED_MAIN_DATE = 2026-09-03
LATEST_RELEASE_OBSERVED = v0.12.0
MAIN_PACKAGE_VERSION_OBSERVED = 0.13.0.dev0
LICENSE_OBSERVED = Apache-2.0
NOTICE_PRESENT = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = PROHIBITED
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S3_PLUS_IMPLEMENTATION_AUTHORITY = NONE_UNTIL_CANONICAL_OWNING_SLICE
```

## Purpose

Qualify Omnigent as a mechanism quarry for WePLD execution-fabric, worker-interoperability, sandbox, credential, browser, review-independence, recovery, and desktop trust-boundary design without importing Omnigent as WePLD's root architecture.

The repository describes itself as an open-source meta-harness over multiple coding agents and custom agents. The useful distinction for WePLD is not the product branding; it is the separation of server/control state, execution hosts/runners, harness adapters, policy gates, sandbox/credential machinery, and UI clients.

```text
OMNIGENT_ARCHITECTURE != WEPLD_ARCHITECTURE_AUTHORITY
APACHE_2_LICENSE_AVAILABLE != SOURCE_ADMISSION
SOURCE_AVAILABLE != DEPENDENCY_ADMITTED
BEHAVIOR_ORACLE != EFFECT_AUTHORITY
```

## Exact high-value owning paths inspected

Pinned under `f4e93c2b74158a2712d07f13e591abb90a999171`:

```text
omnigent/runtime/policies/engine.py
omnigent/policies/types.py
omnigent/runtime/__init__.py
omnigent/runtime/caps.py
omnigent/inner/acp_extension.py
omnigent/inner/acp_executor.py
omnigent/inner/bwrap_sandbox.py
designs/SANDBOX_CREDENTIAL_PROXY.md
omnigent/inner/credential_proxy.py
omnigent/inner/egress/**
omnigent/tools/builtins/browser.py
omnigent/runner/tool_dispatch.py
examples/polly/**
web/electron/**
README.md
LICENSE
NOTICE
```

These paths are candidates for later owning-slice source qualification. No donor command, install script, workflow, test suite, policy module, sandbox, model, or provider integration is authorized to run from this planning record.

## Mechanism OM-01 — Server / Host / Runner identity separation

Observed behavior:

- server coordinates durable/API/UI state;
- a host is a machine that may execute agent work;
- runner identity/affinity selects where a session executes;
- desktop hosting is explicit/opt-in rather than implied by connecting to a server;
- runner routing can fail explicitly rather than silently selecting a global fallback.

WePLD adaptation:

```text
ServerIdentity
!= HostIdentity
!= RunnerIdentity
!= WorkerIdentity
!= AttemptIdentity
```

Introduce explicit runtime/execution descriptors rather than overloading `WorkerDescriptor` with machine/process identity.

Candidate owning slices: S3 runtime/process foundation, S6 Mission Runtime/UWC.

Reuse mode: **P0 clean-room contract adaptation**.

## Mechanism OM-02 — Generic protocol executor + additive vendor extension seam

Omnigent's ACP path keeps the generic executor protocol-oriented while composing vendor-specific behavior at a harness boundary through an extension seam. Vendor sub-agent/permission dialects do not become branches scattered through the generic executor.

WePLD adaptation:

```text
HarnessProtocolAdapter
+ HarnessDialectExtension
-> normalized WePLD worker/event vocabulary
```

Required properties:

- protocol core has neutral defaults;
- extensions are explicitly selected, never discovered from untrusted content;
- capability claims from an extension remain claims until Mirefa qualification;
- extension-specific permission options never create Nawat authority;
- no harness-name conditional fan-out in the core execution path where a typed extension can own the behavior;
- unknown dialect fields remain opaque provenance or unsupported, not silently interpreted.

Candidate owning slice: S6 UWC.

Reuse mode: **P0 design/behavior adaptation**.

## Mechanism OM-03 — Policy choke point and fail-closed enforcement phases

Observed policy model uses composed `ALLOW`, `ASK`, `DENY` decisions and explicit evaluation contexts. Request/tool-call phases are treated as fail-closed when policy evaluation is unavailable because those are pre-effect enforcement points.

WePLD adaptation:

Use this as a behavior oracle for a separate `BehaviorPolicyEvaluation` boundary, not as Nawat.

```text
BEHAVIOR_POLICY_ALLOW != NAWAT_GRANT
BEHAVIOR_POLICY_ASK != NAWAT_APPROVAL_RECORD
BEHAVIOR_POLICY_DENY MAY_NARROW_OR_BLOCK
POLICY_ENGINE_UNAVAILABLE_AT_REQUIRED_PRE_EFFECT_GATE -> EFFECT_BLOCKED
```

Nawat remains the only effect-time authority. A policy layer may impose stricter local/server/user constraints but cannot mint authority.

Candidate owning slices: S6/S8.

Reuse mode: **P0 behavior oracle, not authority implementation**.

## Mechanism OM-04 — Runtime caps as an operator hard ceiling

Omnigent separates deployment/operator runtime ceilings from agent configuration. Agents cannot override the deployment ceiling.

WePLD adaptation:

Add a typed runtime ceiling/containment snapshot that is intersected with Assignment requirements and Nawat grants:

```text
EffectiveExecutionEnvelope =
  canonical deployment ceiling
  INTERSECT project/workspace ceiling
  INTERSECT Assignment constraints
  INTERSECT route qualification
  INTERSECT Nawat grant
```

No lower-trust configuration can widen a higher-precedence ceiling.

Candidate owning slices: S3/S6.

Reuse mode: **P0 contract adaptation**.

## Mechanism OM-05 — Fail-loud OS sandbox and explicit downgrade semantics

Observed Linux path uses Bubblewrap plus seccomp/no-new-privileges with a read-only-oriented mount model. Omnigent also documents that Windows Job Object containment does not provide the same filesystem/network isolation.

WePLD adaptation requires a normalized containment vocabulary instead of one boolean `sandboxed` flag:

```text
HARD_FS_AND_NETWORK_ISOLATION
HARD_FS_ISOLATION_NETWORK_SEPARATE
PROCESS_TREE_CONTAINMENT_ONLY
ADVISORY_PROVIDER_RESTRICTION
NONE
UNKNOWN
```

Rules:

```text
SANDBOX_REQUESTED + REQUIRED_BACKEND_UNAVAILABLE -> REFUSE_EXECUTION
PROCESS_TREE_CONTAINMENT_ONLY != HARD_SANDBOX
CONTAINMENT_DOWNGRADE_REQUIRES_EXPLICIT_REQUALIFICATION
NO_SILENT_UNSANDBOXED_FALLBACK
```

Candidate owning slices: S3 process fabric, S6 worker qualification.

Reuse mode: **P0 behavior/security oracle; bounded implementation quarry later**.

## Mechanism OM-06 — Secretless credential broker

The strongest Omnigent security mechanism observed is a parent-side credential proxy where the real credential remains outside the sandbox. For HTTP(S), a trusted egress proxy can inject a credential for a bound host. Clients that require a local credential can receive a non-secret placeholder which is swapped only for its bound destination; misuse against another host is refused.

WePLD adaptation:

```text
CredentialCapability {
  credential_capability_id
  secret_owner_ref
  broker_identity
  allowed_target_host_set
  allowed_path_or_resource_scope?
  allowed_method_or_protocol_scope?
  attempt_or_assignment_scope
  egress_grant_ref
  placeholder_identity?
  expiry
  usage_receipt_policy
}
```

The worker should normally possess a capability to cause one bounded authenticated request, not the reusable underlying secret.

```text
WORKER_HAS_CREDENTIAL = FALSE_BY_DEFAULT
WORKER_HAS_BOUNDED_CREDENTIAL_CAPABILITY = POSSIBLE_AFTER_AUTHORITY
PLACEHOLDER != SECRET
PLACEHOLDER != AUTHORITY_TO_OTHER_HOST
EGRESS_ALLOWLIST != CREDENTIAL_AUTHORITY
CREDENTIAL_CAPABILITY != EFFECT_AUTHORITY
```

Mandatory future threat-model cases:

- proxy bypass/raw socket path;
- DNS rebinding and target canonicalization;
- redirect to another host;
- wildcard/path-scope confusion;
- credential header clobbering;
- placeholder replay;
- proxy logs/traces leaking real secrets;
- TLS interception trust-store contamination;
- parent compromise;
- stale credential/refresh race;
- retries after unknown remote outcome;
- multiple credentials bound to the same host with different scopes.

Candidate owning slices: S3 egress/containment substrate, S6 worker runtime, S8 effect execution.

Reuse mode: **P0 source/security qualification candidate; clean-room design preferred until admitted**.

## Mechanism OM-07 — Environment deny-by-default

Omnigent's sandbox policy explicitly treats environment passthrough as an allowlisted escape hatch rather than inheriting all host variables.

WePLD adaptation:

```text
EnvironmentExposurePolicy {
  base_allowlist
  adapter_family_allowlist
  explicit_assignment_passthrough[]
  forbidden_secret_patterns[]
  provenance
  policy_snapshot_ref
}
```

Rules:

```text
AMBIENT_ENV_PRESENT != WORKER_VISIBLE
PROVIDER_KEY_FOR_A != PROVIDER_KEY_FOR_B_VISIBLE
GENERIC_PROTOCOL_ADAPTER_GETS_NO_VENDOR_SECRET_FAMILY_BY_DEFAULT
```

Candidate owning slices: S3/S6.

Reuse mode: **P0 contract/security adaptation**.

## Mechanism OM-08 — Browser snapshot identity + stale element rejection

Omnigent's embedded-browser tools expose an accessibility-oriented snapshot with a `snapshot_id` and stable element refs. Actions can bind both the snapshot identity and element ref so navigation/supersession produces a precise stale-ref failure rather than acting on a different page element.

WePLD adaptation extends the existing browser exact-context contract:

```text
BrowserSnapshotObservation {
  browser_snapshot_id
  browser_session_id
  browser_context_id
  document_identity
  origin_identity
  snapshot_generation
  accessibility_or_dom_projection_identity
  observed_at
}

BrowserElementRef {
  browser_snapshot_id
  element_ref
  semantic_projection_identity?
}
```

Any click/type/submit proposal that uses an element ref must bind the exact snapshot. Snapshot supersession/navigation/context change makes the proposal stale.

Candidate owning slice: future browser/WebMCP work, principally S6/S7/S8 depending on operation.

Reuse mode: **P0 behavior adaptation**.

## Mechanism OM-09 — Tool advertisement separated from execution

Omnigent's browser tool classes can be schema/advertisement-only while the runner dispatch layer owns execution. Misrouting fails loudly.

WePLD already has stronger conceptual separation; freeze it explicitly:

```text
CAPABILITY_ADVERTISEMENT
!= CAPABILITY_QUALIFICATION
!= EFFECT_PROPOSAL
!= EFFECT_AUTHORITY
!= EFFECT_EXECUTION
```

Candidate owning slices: S5/S6.

Reuse mode: **reinforcing behavior oracle**.

## Mechanism OM-10 — Cross-vendor review isolation

Polly's workflow routes implementation and review through different vendors and gives the reviewer the diff/contract rather than the implementer's full transcript/worktree.

WePLD adaptation should be stronger than `different vendor`:

```text
ReviewIndependenceReceipt {
  review_independence_receipt_id
  reviewed_target_identity
  builder_attempt_refs[]
  builder_worker_ids[]
  reviewer_attempt_ref
  reviewer_worker_id
  builder_provider_model_harness_identities[]
  reviewer_provider_model_harness_identity
  shared_context_refs[]
  excluded_context_classes[]
  authority_conflict_checks[]
  independence_policy_snapshot_ref
  result
  evidence_refs[]
}
```

Different vendor is one possible signal, not sufficient proof. Reviewer must not inherit mutable builder workspace/process authority when the required independence policy forbids it.

Candidate owning slice: S7.

Reuse mode: **P0 assurance design adaptation**.

## Mechanism OM-11 — Effect prerequisite ordering before irreversible dependent mutations

The inspected current Omnigent main includes a worktree/session-deletion fix that refuses destructive session-file deletion when an explicitly requested worktree cleanup cannot even reach the owning runner. The key reusable idea is not its exact API behavior; it is dependency-aware effect ordering.

WePLD adaptation:

```text
PREREQUISITE_EFFECT_UNKNOWN_OR_UNAVAILABLE
-> DO_NOT_EXECUTE_IRREVERSIBLE_DEPENDENT_EFFECT
```

A composite operation must declare effect dependencies, postconditions, compensation/reconciliation behavior, and the point after which rollback is impossible.

Candidate owning slice: S8.

Reuse mode: **P0 recovery/effect-ordering behavior oracle**.

## Mechanism OM-12 — Thin desktop shell with a narrow origin-pinned native bridge

Omnigent's desktop architecture uses the same server SPA under a thin Electron shell. Privileged native IPC is exposed through a narrow context-isolated preload bridge and validates the sender against the pinned server origin rather than exposing raw Node/IPC capability to the page.

WePLD adaptation:

- no duplicate desktop/web business logic merely to obtain native framing;
- native bridge capabilities are individually typed and allowlisted;
- page origin/session identity is an input to qualification, not authority;
- remote content never receives raw native IPC/process/filesystem access;
- native permission prompts remain effect proposals, not implicit user consent;
- browser navigation away from the pinned app origin revokes privileged bridge eligibility until revalidated.

Candidate owning slice: S3 desktop/native boundary and later browser integration.

Reuse mode: **P1 architecture/security adaptation**.

## Mechanism OM-13 — Session/recovery behavior and explicit runner unavailability

Observed releases emphasize reconnecting runner/session/MCP state after transient outages. WePLD should use this as a recovery quarry while retaining stronger Attempt/effect semantics.

```text
RUNNER_RECONNECTED != ATTEMPT_SAFE_TO_RESUME
SESSION_ID_RESTORED != EFFECT_STATE_RECONCILED
TRANSPORT_RECOVERED != AUTHORITY_REVALIDATED
```

Candidate owning slices: S6/S8/S9.

Reuse mode: **P1 behavior oracle**.

## Mechanism OM-14 — Optional long-term memory remains a replaceable tool

Omnigent integrates Hindsight as optional built-in memory tooling. This supports WePLD's decision not to make one vendor memory system canonical.

```text
MEMORY_TOOL_OUTPUT != SOURCE_OF_TRUTH
MEMORY_BACKEND != EVIDENCE_STORE
MEMORY_RECALL != CURRENT_ACCESS_AUTHORITY
```

Candidate owning slice: later S9/S10 or optional extension.

Reuse mode: **P2 optional adapter/oracle only**.

## Explicit negative-oracle register

```text
OMNI-N001 POLICY_ALLOW_NOT_NAWAT_GRANT
OMNI-N002 SESSION_OR_AGENT_POLICY_NOT_AUTHORITY
OMNI-N003 SERVER_CONNECTION_NOT_HOST_EXECUTION_AUTHORITY
OMNI-N004 RUNNER_ID_NOT_WORKER_TRUST
OMNI-N005 SANDBOX_REQUIRED_UNAVAILABLE_BLOCKS_EXECUTION
OMNI-N006 PROCESS_TREE_CONTAINMENT_NOT_FS_OR_NETWORK_SANDBOX
OMNI-N007 CONTAINMENT_DOWNGRADE_NO_SILENT_FALLBACK
OMNI-N008 PLACEHOLDER_CREDENTIAL_NOT_SECRET_OR_CROSS_HOST_AUTHORITY
OMNI-N009 EGRESS_ALLOWLIST_NOT_CREDENTIAL_OR_EFFECT_AUTHORITY
OMNI-N010 ACP_EXTENSION_NOT_CORE_AUTHORITY
OMNI-N011 VENDOR_CAPABILITY_CLAIM_NOT_QUALIFIED_CAPABILITY
OMNI-N012 STALE_BROWSER_SNAPSHOT_REF_BLOCKS_ACTION
OMNI-N013 DIFFERENT_VENDOR_ALONE_NOT_INDEPENDENCE_PROOF
OMNI-N014 RUNNER_DISCONNECT_NOT_REMOTE_EFFECT_NOT_APPLIED
OMNI-N015 IRREVERSIBLE_DEPENDENT_EFFECT_WAITS_FOR_REQUIRED_PREREQUISITE
OMNI-N016 DESKTOP_PINNED_ORIGIN_NOT_WEPLD_AUTHORITY
OMNI-N017 REMOTE_SPA_NEVER_GETS_RAW_NATIVE_BRIDGE
OMNI-N018 MEMORY_RECALL_NOT_TRUTH_OR_CURRENT_ACCESS_AUTHORITY
OMNI-N019 CUSTOM_POLICY_CODE_NOT_DEFAULT_TRUSTED_AUTHORITY_PATH
OMNI-N020 DONOR_INSTALL_OR_DEV_COMMAND_NOT_RECONNAISSANCE_STEP
```

## Source-admission procedure if an owning slice later needs code reuse

1. reverify the exact upstream revision and repository license;
2. inspect `NOTICE` and preserve required attribution/notices for any copied/adapted source;
3. identify the smallest owning path and tests rather than importing the meta-harness wholesale;
4. compare the mechanism against current WePLD contracts before reuse;
5. prefer clean-room Rust/native adaptation where the behavior is small and dependency-free;
6. independently security-review any sandbox, credential, TLS/MITM, egress, process, native bridge, or secret path;
7. prohibit donor installer/workflow execution during reconnaissance;
8. model every imported dependency separately; Apache-2.0 on the repository does not admit all transitive packages;
9. add negative oracles proving the adaptation cannot widen Nawat authority;
10. preserve provenance and exact source identity in the future source registry;
11. obtain exact-head independent review after adaptation;
12. retain an exit strategy so ACP/vendor/sandbox/provider-specific code remains replaceable.

## Planning decision

```text
OMNIGENT = HIGH_VALUE_EXECUTION_FABRIC_MECHANISM_QUARRY
ROOT_ARCHITECTURE = REJECT
P0 = HOST_RUNNER_IDENTITY + ACP_EXTENSION_SEAM + FAIL_LOUD_SANDBOX + SECRETLESS_CREDENTIAL_BROKER + POLICY_CHOKE_POINT_ORACLE + BROWSER_SNAPSHOT_FRESHNESS + REVIEW_INDEPENDENCE + EFFECT_ORDERING
P1 = DESKTOP_NATIVE_BRIDGE + SESSION_RECOVERY + ROUTING/COST_PATTERNS
P2 = OPTIONAL_MEMORY + CLOUD_SANDBOX_FLEET
```

Omnigent materially improves the future S3/S6/S7/S8 design but does not alter the current active slice, canonical source registry, implementation authority, or roadmap ordering.