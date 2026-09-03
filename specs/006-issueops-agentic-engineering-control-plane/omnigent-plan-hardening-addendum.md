# Plan Hardening Addendum — Omnigent Execution Fabric

```text
STATUS = FUTURE_PLANNING_ADDENDUM
PARENT_PLAN = plan.md
UPSTREAM_RESEARCH = research/omnigent-qualified-mechanism-extraction-2026-09-04.md
CURRENT_ACTIVE_SLICE = S2
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
ROADMAP_REMAP = NONE
```

This addendum is normative planning input for Spec 006. It strengthens the parent plan without changing roadmap ordering or pulling S3+ implementation into S2.

## 1. Execution-fabric architecture refinement

The parent architecture is refined as follows:

```text
WePLD control plane / server state
            |
            v
      explicit Host registry
            |
            v
      qualified Runner runtime
            |
            v
   HarnessProtocolAdapter
      + optional qualified
    HarnessDialectExtension
            |
            v
       WorkerDescriptor
            |
            v
        Assignment
            |
      Edara topology
            |
    Mirefa route qualification
            |
      Nawat authority
            |
            v
   frozen ExecutionEnvelope
            |
            v
     Mission Runtime Attempt
            |
   effects / evidence / recovery
```

The following identities are never aliases:

```text
Server != Host != Runner != Worker != Attempt
Harness != Model != ProviderSession
```

Early implementations may co-locate components but may not collapse their semantic/trust identities when those identities are material to qualification, authority, recovery, or evidence.

## 2. Runtime hard-ceiling rule

Introduce the `RuntimeCeiling` and `ExecutionEnvelope` concepts from `contracts/runtime-execution-fabric.md`.

Effective execution capability is the intersection of all applicable constraints:

```text
Deployment ceiling
∩ project/workspace ceiling
∩ Assignment
∩ WorkerRequirement
∩ RouteQualification
∩ Nawat grant
= ExecutionEnvelope
```

No user/agent/provider/repository configuration can widen a stronger higher-precedence ceiling.

## 3. Containment semantics

Replace any future single boolean concept of `sandboxed` with multidimensional `ContainmentPosture` evidence.

At minimum distinguish:

```text
process-tree containment
filesystem isolation
network isolation
namespace/container isolation
syscall policy
write/read mount policy
home/config visibility
known platform limitations
```

Planning rule:

```text
REQUIRED_CONTAINMENT_UNAVAILABLE -> EXECUTION_REFUSED
```

There is no silent unsandboxed fallback. A weaker backend may be offered only as an explicitly requalified alternative that still satisfies the Assignment/authority requirements.

## 4. Credential architecture

WePLD should prefer secretless/scoped credential capabilities over passing reusable secrets into workers.

Target architecture:

```text
Secret store / credential owner
        |
        v
trusted credential broker
        |
 exact target + route + Attempt + grant
        |
        v
authenticated outbound operation
```

The worker should ideally receive neither the reusable secret nor a general-purpose credential. When a client requires local credential-shaped material, a non-secret target-bound placeholder or scoped ephemeral credential may be used only after separate qualification.

```text
CredentialCapability != EffectAuthority
CredentialCapability != GeneralNetworkAuthority
EgressAllowlist != CredentialAuthority
```

Direct secret passthrough remains a weaker last-resort route whose limitation must be visible in route/containment/security evidence.

## 5. Harness/protocol architecture

Provider interoperability should prefer:

```text
one generic protocol adapter
+ explicit additive dialect extension
```

over one bespoke executor or scattered provider-name branches for every agent.

Extension selection must be trusted/qualified configuration. An extension may normalize vendor capabilities, permission options, sub-agent events, or metadata, but cannot create effect authority.

This is a key UWC design rule for S6.

## 6. Policy versus authority

A future user/server/agent behavior-policy system may use concepts such as:

```text
ALLOW
ASK
DENY
```

for cost, safety, workflow, model-selection, or organization constraints.

However:

```text
POLICY_ALLOW != NAWAT_GRANT
POLICY_ASK != NAWAT_APPROVAL_RECORD
```

Behavior policies may narrow, block, transform, or require a separate approval path. Only Nawat owns effect-time authorization.

A required pre-effect policy evaluation that cannot run fails closed; advisory post-effect analysis must not pretend it prevented an effect already incurred.

## 7. Environment exposure

Worker processes receive a deny-by-default environment.

The future environment contract must separate:

```text
baseline runtime variables
adapter-family variables
explicit Assignment passthrough
forced safety values
scrubbed variables
prohibited secret classes
```

Ambient host credentials never become worker-visible merely because they exist in the launching shell.

## 8. Browser exact-observation refinement

The browser boundary gains snapshot-bound element references:

```text
BrowserSnapshotObservation
BrowserElementRef
```

A ref-based browser action binds:

```text
browser session
browser context
origin
document/snapshot identity
element ref
input identity
route qualification
Nawat decision
```

Navigation, reload, document replacement, snapshot supersession, context/frame change, or origin change can stale the proposal before execution.

```text
STALE_BROWSER_SNAPSHOT != VALID_ACTION_TARGET
```

This extends, not replaces, `contracts/web-agent-boundary.md`.

## 9. Review independence refinement

Independent review is a typed evidence requirement, not merely a provider choice.

Use `contracts/review-independence.md` and a `ReviewIndependenceReceipt` to prove the active policy's required separation dimensions.

Different-vendor review is a useful signal but not sufficient by itself.

Possible requirements include:

```text
different worker/Attempt
different provider/model/harness when required
no mutable builder worktree inheritance
no builder effect-grant inheritance
reviewer read-only effect profile
minimum-sufficient exact target + contract context
no self-certification after reviewer-authored repair
```

## 10. Effect dependency ordering

S8 planning must model composite effects as a dependency graph.

A later irreversible effect cannot start when a required prerequisite effect is unavailable or its outcome is unknown.

```text
PREREQUISITE_EFFECT_OUTCOME_UNKNOWN
-> RECONCILE
-> only then dependent irreversible effect if postcondition permits
```

Compensation/rollback is a new effect with its own authority/evidence; it never rewrites history to claim the original effect did not occur.

## 11. Native desktop boundary

A desktop shell must expose only narrow typed native capabilities. Remote or server-served UI content never receives raw native process, shell, filesystem, IPC, or credential APIs.

Required principles:

```text
context isolation
serialization-safe native bridge
sender/application-origin validation
foreign-origin privileged bridge disabled
native permission prompts separately classified
no duplicate desktop/web decision engine
```

The same typed product decisions should drive web and desktop UX; the native shell adds platform capabilities rather than a second authority model.

## 12. Recovery semantics

Transport/session recovery and effect recovery are separate.

```text
RUNNER_RECONNECTED != ATTEMPT_SAFE_TO_RESUME
SESSION_FOUND != RUNTIME_IDENTITY_SAME
TRANSPORT_RECOVERED != AUTHORITY_REVALIDATED
```

Before an interrupted Attempt resumes, Mission Runtime must reconcile any material unknown effects and revalidate every runtime/route/grant element declared stale by the owning contract.

## 13. Roadmap placement refinement

### S3

Add:

- Server/Host/Runner identity foundation;
- multidimensional containment posture;
- required-sandbox fail-loud semantics;
- environment exposure policy;
- native desktop bridge boundary;
- credential-broker feasibility/security design only, without pulling future network authority forward.

### S5

Add dry-run-only:

- protocol/dialect capability fixtures;
- synthetic ExecutionEnvelope intersection tests;
- no real provider/model/process execution.

### S6

Add:

- explicit host/runner lifecycle;
- generic protocol adapter + dialect extension seam;
- capability negotiation/conformance;
- no silent runner/worker/model fallback;
- runtime-ceiling enforcement;
- credential capability broker only if separately source/security/network-authorized;
- hierarchical budget evidence;
- runner restart/recovery semantics.

### S7

Add:

- typed `ReviewIndependenceReceipt`;
- independence-policy dimensions stronger than different-vendor alone;
- ClaimAssessment must reject stale/insufficient independence evidence when required.

### S8

Add:

- effect dependency graph;
- prerequisite postcondition gating;
- unknown-effect reconciliation before dependent irreversible effects;
- separately authorized compensation semantics.

### S9

Add:

- Server/Host/Runner/Worker/Attempt execution lineage;
- containment/environment/credential-use evidence;
- recovery replay distinguishing transport, runtime, authority, and external-effect states.

## 14. New tracer bullets

### RT-TB0 — runtime identity dry-run

Synthetic Server/Host/Runner/Worker route creates one `ExecutionEnvelope` without executing any process.

Proves:

```text
identity separation
ceiling intersection
no authority inheritance
```

### RT-TB1 — containment refusal

A synthetic route requires hard filesystem/network isolation but only process-tree containment is available.

Expected result:

```text
ROUTE_NOT_QUALIFIED / EXECUTION_REFUSED
```

No downgrade.

### RT-TB2 — generic adapter dialect fixture

One generic ACP-like adapter plus two dialect fixtures prove vendor-specific fields do not contaminate core authority semantics.

### RT-TB3 — credential capability simulation

No live secret/network required. Simulate a credential capability bound to one target and prove wrong-target placeholder replay is refused and no raw secret enters worker context/evidence.

### RT-TB4 — browser snapshot freshness

Synthetic snapshot/ref proposal becomes stale after document/snapshot generation change; action is blocked.

### RT-TB5 — independent review receipt

Synthetic builder/reviewer identities demonstrate:

- same worker -> fail;
- different vendor but shared mutable builder workspace under strict policy -> fail;
- policy-satisfying separated reviewer -> pass.

### RT-TB6 — effect ordering

Synthetic external prerequisite has `EFFECT_OUTCOME_UNKNOWN`; dependent irreversible cleanup/closeout is not started until reconciliation establishes the required postcondition.

## 15. Success measures added

When the owning slices exist, measure:

- silent-fallback prevention rate across runner/worker/model/containment routes;
- percentage of effectful Attempts with complete Server/Host/Runner/Worker/Attempt lineage;
- containment evidence coverage by dimension, not one boolean;
- percentage of credentialed effects using brokered/scoped capability versus direct reusable secret exposure;
- wrong-target credential-use prevention rate;
- stale browser snapshot action prevention rate;
- independent review receipts satisfying the selected policy;
- unsafe retry/dependent-effect prevention when external outcome is unknown;
- runtime recovery events correctly requiring revalidation/reconciliation.

These metrics are guardrails/evidence quality measures, not incentives to maximize autonomy volume.

## 16. Source boundary

Omnigent is used as a mechanism quarry. The default adaptation strategy is clean-room WePLD-native contracts/implementation where practical. Direct source reuse, Python dependency import, sandbox implementation reuse, TLS proxy reuse, ACP executor reuse, or Electron source reuse requires a future exact owning-slice Source Acquisition Check and applicable license/NOTICE/security qualification.

```text
OMNIGENT_RESEARCHED = YES
OMNIGENT_SOURCE_ADMITTED = NO
OMNIGENT_DEPENDENCY_ADMITTED = NO
OMNIGENT_RUNTIME_AUTHORITY = NONE
```
