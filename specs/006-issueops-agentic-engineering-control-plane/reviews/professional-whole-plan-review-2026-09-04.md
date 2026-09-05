# Professional Whole-Plan Review — 2026-09-04

```text
REVIEW_CLASS = INTERNAL_ARCHITECTURE_PRODUCT_EXECUTION_SECURITY_PLANNING_REVIEW
REVIEWED_PR = 241
REVIEWED_CONTENT_FRONTIER = a67ff5261bd0c9c9c5387ab2feb9ff8b714be8d1
CANONICAL_MAIN_OBSERVED = 24791b11196106f0440ca01aa5344a5168e650f8
CANONICAL_MAIN_MERGE = PR_274_GIT_TOPOLOGY_TRANCHE
CURRENT_ACTIVE_SLICE = S2
INDEPENDENT_REVIEW_GATE_SATISFIED_BY_THIS_REVIEW = NO
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
```

## Objective

Review the complete Spec 006 planning package after the Omnigent execution-fabric study and prior OpenHands/Assurance hardening. The review asks whether the future plan is professional, implementable in dependency order, authority-safe, recoverable, secure by construction, and sufficiently explicit that independent teams would not make incompatible reasonable interpretations.

The review covers:

- product architecture and roadmap placement;
- provider-neutral IssueOps and Case semantics;
- RAG/source/access/freshness;
- untrusted-content boundaries;
- Server/Host/Runner/Worker/Attempt identity;
- process/runtime containment;
- harness/protocol interoperability;
- behavior policy versus Nawat authority;
- credential handling and egress;
- distributed runner ownership/recovery;
- runtime event identity/replay;
- browser/WebMCP freshness/effects;
- multi-agent coordination / Case Bus;
- independent review evidence;
- Assurance `/review`, `/security`, `/fulltest`;
- effect ordering, reconciliation, repair, and completion;
- evidence/privacy/durability;
- source acquisition/licensing/exit strategy;
- planning-package discoverability and implementation sequencing.

This review was produced as part of the plan repair and is therefore **not** a qualified independent acceptance review.

## Overall verdict at the reviewed content frontier

```text
ARCHITECTURE_DIRECTION = STRONG
PRODUCT_DIFFERENTIATION = STRONG
AUTHORITY_MODEL = STRONG
EXECUTION_FABRIC_MODEL = STRONG_AFTER_REPAIR
ASSURANCE_MODEL = STRONG_AFTER_PRIOR_REPAIR
RECOVERY_MODEL = STRONG_AFTER_REPAIR
SECURITY_POSTURE = STRONG_AS_FUTURE_PLAN
SOURCE_ACQUISITION_POSTURE = STRONG
ROADMAP_ORDERING = COHERENT
KNOWN_MATERIAL_CONTENT_GAPS_AT_REVIEWED_FRONTIER = 0
FINAL_PLANNING_ACCEPTANCE = NO
MERGE_READY = NO
```

`KNOWN_MATERIAL_CONTENT_GAPS_AT_REVIEWED_FRONTIER = 0` means this internal review found no remaining **known material planning-content gap** after the repairs enumerated below. It does **not** mean the branch is canonically reconciled, qualified, independently reviewed, or merge-authorized.

The branch remains materially diverged from current canonical `main`, so final acceptance still requires non-destructive canonical reconciliation, fresh exact-head deterministic qualification, and a genuinely independent whole-scope exact-head review.

## Findings and repair status

### EXEC-FABRIC-001 — HIGH — execution identities were overloaded around Worker

**Gap:** `WorkerDescriptor` could otherwise become an accidental container for server machine, execution host, runner, harness, provider, model, and Attempt identity.

**Repair:** `contracts/runtime-execution-fabric.md` now defines distinct `ServerDescriptor`, `HostDescriptor`, `RunnerDescriptor`, protocol/dialect adapters, and `ExecutionEnvelope` while preserving canonical Worker/Assignment/Attempt ownership.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### CONTAIN-001 — HIGH — one-dimensional sandbox semantics were insufficient

**Gap:** provider/runtime labels such as sandbox/read-only or process-tree containment could be misrepresented as full filesystem/network isolation, especially across Windows/Linux/macOS.

**Repair:** multidimensional `ContainmentPosture`, explicit platform limitations, required-sandbox fail-loud behavior, and no silent downgrade are now normative in runtime contracts/spec/acceptance/tasks.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_NEGATIVE_ORACLES`.

---

### CRED-001 — HIGH — credential transport lacked a first-class least-authority model

**Gap:** worker credential exposure, egress permission, effect authority, and secret possession could otherwise collapse into one provider-specific mechanism.

**Repair:** `CredentialCapability` separates secret ownership, broker identity, exact target/resource/protocol scope, Assignment/Attempt, egress, Nawat grant, expiry, placeholder identity, and usage receipts. Direct reusable-secret exposure is explicitly weaker/last-resort. Security qualification includes redirect, DNS rebinding, proxy bypass, TLS trust, replay, refresh, logging, and same-host multi-scope risks.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_SOURCE_ACQUISITION_GATE`.

---

### HOST-AUTH-001 — HIGH — host identity was not sufficient host trust

**Gap:** once Server and Host are distinct, a self-asserted `host_id` or server connection could be mistakenly treated as trusted execution-host enrollment.

**Repair:** `contracts/runtime-distributed-safety-addendum.md` defines `HostTrustObservation`, authenticated principal/installation identity, transport-security identity, enrollment decision, revocation/expiry, and explicit `HOST_ID_CLAIM != AUTHENTICATED_HOST` semantics.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### RUNNER-FENCE-001 — HIGH — distributed runner split-brain was not prevented

**Gap:** a restarted/reconnected runner could leave an old process able to act on stale Assignment/grant state.

**Repair:** `RunnerOwnershipLease` adds owner epoch, lease, fencing token, expiry, revocation, stale-token refusal, and new-runtime/new-epoch semantics. Future effect evidence can bind current ownership identity.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### RUNTIME-EVENT-001 — HIGH — transport delivery was not a durable causal event model

**Gap:** duplicated/replayed/out-of-order Server/Runner messages could otherwise be interpreted by arrival order or duplicate a derived effect/state transition.

**Repair:** `RuntimeEventEnvelope` adds stable event identity, producer/runtime/Attempt identity, causal parents, optional producer sequence, dedupe/idempotency identity, payload identity, schema version, and authenticity evidence. Duplicate/replay/causal negative oracles are explicit.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### POLICY-TRUST-001 — HIGH — behavior policy could become a second authority or executable-code backdoor

**Gap:** Omnigent-style ALLOW/ASK/DENY is useful, but copying that model directly could let custom executable policies or agent/session policy changes become de facto authority.

**Repair:** `contracts/behavior-policy-boundary.md` defines behavior policies as monotonic constraints only, canonical `NO_OBJECTION != NAWAT_GRANT`, fail-closed mandatory pre-effect evaluation, policy precedence, executable-policy source/runtime/security gates, and agent-policy proposal rather than self-activation.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### REVIEW-INDEP-001 — HIGH — `builder != reviewer` needed typed proof

**Gap:** different agent/vendor alone is not always sufficient independence; mutable workspace, process/session, shared hidden context, or inherited write authority can compromise review independence.

**Repair:** `contracts/review-independence.md` defines `ReviewIndependenceReceipt` and policy dimensions including worker/Attempt/provider/model/harness separation, workspace/context separation, effect-authority conflicts, exact-target freshness, and no self-certification after reviewer-authored repair.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### EFFECT-ORDER-001 — HIGH — unknown prerequisite outcomes could precede irreversible dependent effects

**Gap:** general `EFFECT_OUTCOME_UNKNOWN` existed, but composite operations also need dependency-aware ordering so a destructive cleanup/closeout does not proceed while an earlier required external effect is unavailable/unknown.

**Repair:** `EffectDependency` semantics in the runtime contract require prerequisite postconditions, block irreversible dependents on unknown prerequisite outcomes, and model compensation as a separate effect rather than historical rewrite.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TRACER_BULLET`.

---

### PROTO-DIALECT-001 — MEDIUM — generic protocol and vendor-specific semantics needed an explicit seam

**Gap:** ACP/provider adapters could devolve into scattered harness-name branching and provider permission semantics leaking into core worker contracts.

**Repair:** `HarnessProtocolAdapter` + `HarnessDialectExtension`; extension selection is trusted/qualified, unknown fields remain opaque/unsupported, vendor capability/permission claims cannot create effect authority.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### HARNESS-ID-001 — MEDIUM — descriptor version did not prove actual executed harness identity

**Gap:** a worker may be qualified at one CLI/runtime artifact and then execute another due to PATH replacement, package update, or vendor auto-update.

**Repair:** `HarnessExecutionIdentity` records resolved runtime/executable/artifact/config/protocol/capability-handshake identity; material auto-update/replacement stales qualification.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### BROWSER-SNAPSHOT-001 — MEDIUM — browser exact-context semantics needed document/snapshot-bound refs

**Gap:** browser context/origin freshness was already strong, but element refs/selectors could still be interpreted against a changed document without a first-class snapshot identity.

**Repair:** Omnigent-derived `BrowserSnapshotObservation` / `BrowserElementRef` planning binds ref actions to exact document/snapshot generation and blocks stale superseded references. The existing broader browser session/context/origin/tool-generation contract remains controlling.

**Status:** `CLOSED_BY_PLANNING_ADDENDUM_AND_TASKS`.

---

### DESKTOP-BRIDGE-001 — MEDIUM — native Desktop trust boundary needed explicit least-authority bridge semantics

**Gap:** a server-served/remote SPA under a native shell could become a raw IPC/Node/process/filesystem privilege bridge.

**Repair:** `NativeBridgeCapability` plus origin/sender validation, context isolation, serialization-safe schemas, foreign-origin inert behavior, and explicit prohibition on raw IPC/Node/shell exposure.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### RESOURCE-ADMIT-001 — MEDIUM — route qualification did not equal resource admission

**Gap:** a worker/runner can be qualified but lack CPU/memory/disk/process/concurrency capacity at actual Attempt start.

**Repair:** distributed runtime contract introduces optional `RuntimeReservation` / resource-admission semantics; `RESOURCE_REQUIREMENT_NOT_ADMITTED -> ATTEMPT_NOT_STARTED` and resource exhaustion remains distinct from provider failure.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### VERSION-COMPAT-001 — MEDIUM — independently evolving runtime components needed compatibility semantics

**Gap:** Server, Host, Runner, protocol adapter/dialect, and native bridge can change independently; connection alone cannot prove effectful contract compatibility.

**Repair:** explicit version/handshake compatibility with unknown required version fail-closed and no silent effectful schema downgrade.

**Status:** `CLOSED_BY_PLANNING_CONTRACT_AND_TASKS`.

---

### CASE-BUS-001 — MEDIUM — Case Bus was referenced without a canonical coordination contract

**Gap:** the PR described a durable Case-scoped coordination bus but had no dedicated contract preventing arbitrary worker messages from becoming Assignment, WorkflowIntent, review acceptance, or authority.

**Repair:** `contracts/case-bus.md` defines typed message acts, bounded/reference-first payloads, duplicate-safe delivery, causal rather than arrival ordering, access/egress semantics, cancellation distinctions, and no-authority-inheritance invariants.

**Status:** `CLOSED_BY_PLANNING_CONTRACT`.

---

### DISCOVERABILITY-001 — MEDIUM — package complexity itself became an implementation risk

**Gap:** the planning package grew beyond forty files. A future implementer reading only parent `spec.md`/`plan.md` could miss normative contracts/addenda/tasks and make an internally reasonable but incompatible implementation.

**Repair:** `PLANNING_INDEX.md` defines the start-here sequence, canonical ownership map, normative contracts/addenda, task maps, research/reviews, roadmap placement, and acceptance sequence. `ASSURANCE_FABRIC_INDEX.md` was expanded accordingly.

**Status:** `CLOSED_BY_PLANNING_INDEX`.

---

### HIST-ACCOUNT-001 — LOW — historical internal review footer under-counted its own findings

**Gap:** `reviews/professional-whole-plan-review-2026-09-02.md` enumerates sixteen finding sections but its historical footer reports fifteen (`HIGH=7`, `MEDIUM=7`, `LOW=1`). The actual enumerated severity count is 7 HIGH + 8 MEDIUM + 1 LOW = 16.

**Repair:** preserve the historical artifact rather than silently rewriting evidence; `PLANNING_INDEX.md` and this review explicitly record the mismatch. Final acceptance requires fresh exact-head review/accounting anyway.

**Status:** `CLOSED_AS_HISTORICAL_METADATA_CLARIFICATION`.

## Finding accounting

```text
TOTAL_FINDINGS = 18
HIGH = 9
MEDIUM = 8
LOW = 1
OPEN_MATERIAL_FINDINGS_AT_REVIEWED_CONTENT_FRONTIER = 0
```

The count above matches the eighteen enumerated finding IDs in this document.

## Prior 2026-09-02 hardening revalidation

The earlier material categories remain represented after the new runtime work:

```text
cross-artifact schema ownership                 -> data-model / dedicated contracts
Assurance ClaimAssessment                       -> contracts/assurance-fabric.md
AssurancePolicySnapshot                         -> contracts/assurance-fabric.md
EFFECT_OUTCOME_UNKNOWN                          -> data-model / worker runtime
RAG access revocation                           -> data-model / retrieval contract
EvidenceHandlingPolicy                          -> assurance contract
REQUIRED / CONDITIONAL / OPTIONAL FullTest      -> assurance contract
provider completeness/authenticity              -> provider/spec/acceptance
atomic source generations                       -> data-model / retrieval
remote RAG SSRF/redirect/DNS controls           -> spec/tasks/acceptance
exact engine identity/resource envelope         -> assurance contract
finding fingerprint/disposition                 -> assurance contract
performance evidence statistics                 -> assurance contract
browser artifact/context effects                -> web boundary
command catalog consistency                     -> command-surface/spec/acceptance
```

The Omnigent integration does not reopen or weaken these repairs.

## Source-acquisition assessment

Omnigent is appropriately classified as a high-value mechanism quarry, not architecture authority.

Exact observed research pin:

```text
omnigent-ai/omnigent@f4e93c2b74158a2712d07f13e591abb90a999171
LICENSE_OBSERVED = Apache-2.0
NOTICE_PRESENT = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
```

The plan correctly prefers clean-room/native WePLD adaptation for small mechanisms and reserves direct source reuse/dependency import for exact future Source Acquisition gates. Credential proxy, sandbox/seccomp, TLS/egress, executable policy, browser actuation, host transport, and native IPC source reuse have explicit security-specific gates.

## Professional architecture assessment

The resulting future architecture is coherent:

```text
Case / WorkflowIntent
        |
      Edara
        |
     Mirefa
        |
      Nawat
        |
ExecutionEnvelope
        |
Mission Runtime
        |
Host -> Runner -> ProtocolAdapter(+Dialect) -> Worker
        |
Effects / RuntimeEvents / Evidence
        |
Assurance + ReviewIndependence
        |
S8 repair / effect dependency / reconciliation
        |
Trusted Completion
        |
S9 Quality Passport / replay
```

Control and evidence boundaries remain distinct:

```text
Fehrest = graph/context owner
Edara = work-topology owner
Mirefa = qualification owner
Nawat = effect authority owner
Mission Runtime = Attempt execution owner
UWC = worker/protocol normalization boundary
AMAN = security evidence owner
Assurance = claim/evidence/finding evaluation owner
S8 = separately authorized repair/effect consumer
Trusted Completion = completion decision boundary
```

The plan is stronger than directly copying Omnigent/OpenHands because it adopts their useful runtime mechanisms while adding explicit authority intersection, exact identities, review-independence receipts, split-brain fencing, causal runtime evidence, and Trusted Completion separation.

## Remaining deferred decisions that are not current planning gaps

The following remain intentionally deferred to owning canonical slices/Source Acquisition:

- exact host-authentication technology and trust root;
- exact lease/fencing storage/transport implementation;
- exact runner transport protocol;
- exact sandbox implementation(s) admitted per platform;
- exact credential broker/proxy technology or whether clean-room native implementation is preferable;
- exact first ACP/native/SDK worker adapters;
- exact policy expression/plugin technology;
- exact database/event-store representation;
- exact resource scheduler/admission algorithm;
- exact GitHub authentication/webhook architecture;
- exact browser automation/protocol implementation;
- exact semantic/vector retrieval engine, if benchmark evidence justifies one;
- S10 multi-case scheduling/fairness algorithms.

Each has an owning boundary and fail-closed interface; therefore choosing the technology now would be premature rather than gap-filling.

## Current acceptance blockers

At the reviewed content frontier:

```text
BRANCH = plan/006-issueops-agentic-engineering-control-plane
PR = 241
PR_STATE = DRAFT
CURRENT_CANONICAL_MAIN_OBSERVED = 24791b11196106f0440ca01aa5344a5168e650f8
BRANCH_RELATION_TO_MAIN = DIVERGED_AND_MATERIALLY_BEHIND
CURRENT_HEAD_DETERMINISTIC_QUALIFICATION = NOT_ESTABLISHED_AFTER_LATEST_REPAIRS
INDEPENDENT_WHOLE_SCOPE_EXACT_HEAD_REVIEW = PENDING
MERGE = NOT_AUTHORIZED
```

Required next acceptance sequence:

1. re-read then-current canonical governance;
2. non-destructively reconcile branch with canonical `main`;
3. confirm final diff remains planning/spec/research-only;
4. run fresh exact-head deterministic qualification;
5. obtain a genuinely independent whole-scope exact-head engineering/correctness review;
6. reconcile every material finding on any new head and rerun freshness-dependent gates;
7. prove zero unresolved material review threads and internally consistent review coverage/accounting;
8. perform final base/head/tree/diff/check/review race verification before merge.

## Final review statement

```text
INTERNAL_CONTENT_REVIEW_COMPLETE = YES
INTERNAL_FINDINGS = 18
INTERNAL_FINDINGS_REPAIRED_OR_HISTORICALLY_CLARIFIED = 18
KNOWN_OPEN_MATERIAL_CONTENT_FINDINGS = 0
INDEPENDENT_ACCEPTANCE_REVIEW = STILL_REQUIRED
CANONICAL_RECONCILIATION = STILL_REQUIRED
FRESH_EXACT_HEAD_QUALIFICATION = STILL_REQUIRED
PLANNING_MERGE_AUTHORIZED = NO
```

No implementation, source, dependency, process, network, browser, model/provider, Git-write, issue-provider-write, or S3+ authority is created by this review.