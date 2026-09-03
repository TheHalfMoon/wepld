# Acceptance Addendum — Runtime Execution Fabric

```text
STATUS = PLANNING_ACCEPTANCE_ADDENDUM
PARENT_ACCEPTANCE = acceptance.md
IMPLEMENTATION_AUTHORITY = NONE
```

The planning candidate is not internally complete unless the execution-fabric hardening below is represented by explicit contracts/tasks and remains consistent with the parent Spec 006 package.

## A. Identity and routing

- [ ] `ServerIdentity`, `HostIdentity`, `RunnerIdentity`, `WorkerIdentity`, and `AttemptIdentity` are explicitly distinct.
- [ ] Connecting Desktop/web/CLI to a server cannot implicitly opt a machine into execution hosting.
- [ ] Host registration, host qualification, runner liveness, worker qualification, and effect authority remain separate states.
- [ ] Runner/host changes that matter to route qualification stale/requalify the route.
- [ ] No silent host/runner/worker/model fallback is permitted.

## B. Protocol / dialect

- [ ] A generic harness protocol adapter can represent protocol-standard behavior without provider-name branching.
- [ ] Vendor-specific behavior is modeled as an explicit dialect extension with neutral defaults.
- [ ] Extension selection is trusted/qualified configuration, not untrusted content.
- [ ] Unknown dialect fields remain opaque/unsupported.
- [ ] Vendor permission/capability claims cannot become Nawat authority.

## C. Runtime ceiling

- [ ] A typed `RuntimeCeiling` exists as a hard upper bound.
- [ ] Effective execution capability is an intersection of all controlling ceilings/constraints/grants.
- [ ] Lower-trust configuration cannot widen a higher-precedence ceiling.
- [ ] Empty intersection produces a blocked Attempt rather than implicit downgrade.

## D. Containment

- [ ] Containment is multidimensional, not one `sandboxed` boolean.
- [ ] Process-tree-only containment cannot satisfy hard filesystem/network isolation requirements.
- [ ] Required sandbox/containment backend unavailability fails loudly.
- [ ] Containment downgrade requires explicit alternative routing/requalification.
- [ ] Platform limitations such as Windows process containment without filesystem/network isolation are explicit evidence, not hidden behind a generic sandbox badge.

## E. Environment and secrets

- [ ] Worker environment is deny-by-default.
- [ ] Baseline, adapter-family, explicit passthrough, forced values, and scrub rules are distinguishable.
- [ ] Ambient provider secrets do not reach unrelated workers.
- [ ] Generic protocol adapters receive no vendor secret family by default.
- [ ] Raw environment/secret values are not persisted as normal evidence.

## F. Credential capability

- [ ] Credential use is separated from effect authority and general network authority.
- [ ] Preferred route keeps reusable secrets outside the worker where technically feasible.
- [ ] Target-bound placeholders are explicitly non-secret and cannot authenticate another target.
- [ ] Credential use binds exact target/route/Attempt/egress/grant/expiry.
- [ ] Direct reusable-secret exposure is explicit and classified as a weaker route.
- [ ] Future broker qualification covers redirect, DNS rebinding, proxy bypass, TLS trust, logs/traces, refresh races, multi-credential same-host scope, replay, and grant expiry.

## G. Browser freshness

- [ ] Browser action by element ref binds an exact snapshot/document identity.
- [ ] Snapshot supersession/navigation/context/frame/origin change can stale the proposal.
- [ ] A stale element ref cannot be silently re-resolved against the latest page.
- [ ] Capability advertisement/schema presence is separate from browser execution authority.

## H. Review independence

- [ ] Independent review is represented by a typed `ReviewIndependenceReceipt` when required.
- [ ] Different-vendor alone is not sufficient proof under a stricter policy.
- [ ] Policy can require worker/Attempt/provider/model/harness/workspace/context/authority separation.
- [ ] Reviewer repair cannot self-certify the repaired exact target when policy requires independent re-review.
- [ ] New exact head stales prior acceptance-critical review-independence receipt.

## I. Effect ordering and recovery

- [ ] Composite operations can declare prerequisite/dependent effects.
- [ ] Unknown/unavailable required prerequisite blocks irreversible dependent effect.
- [ ] Compensation is a separately authorized/evidenced effect.
- [ ] Transport reconnect does not automatically resume an Attempt.
- [ ] Runtime identity, route/containment/context/credential/grant state and unknown external effects are revalidated/reconciled before effectful resume as required.

## J. Native desktop bridge

- [ ] Remote/server SPA gets only narrow serialization-safe native APIs.
- [ ] Raw Node/process/shell/filesystem/IPC exposure is prohibited.
- [ ] Privileged bridge eligibility validates the sender/application origin.
- [ ] Foreign-origin navigation makes privileged bridge operations inert until trusted app context is restored.
- [ ] Native OS/browser permission prompt is not treated as a WePLD approval/Nawat grant.

## K. Omnigent source boundary

- [ ] Records `omnigent-ai/omnigent@f4e93c2b74158a2712d07f13e591abb90a999171` as research-only mechanism quarry.
- [ ] Records Apache-2.0 and NOTICE presence without treating license as source/dependency admission.
- [ ] Donor install/dev/workflow/policy/model/sandbox machinery is not executed during reconnaissance.
- [ ] Default adaptation strategy is minimum-sufficient clean-room WePLD-native implementation unless owning Source Acquisition later admits exact source.
- [ ] Credential/sandbox/TLS/native-bridge source reuse requires security-specific qualification.

## L. Planning package discoverability

- [ ] `ASSURANCE_FABRIC_INDEX.md` links the Omnigent research, runtime contract, review-independence contract, and integration task map.
- [ ] `omnigent-plan-hardening-addendum.md` maps the changes into S3/S5/S6/S7/S8/S9 without roadmap renumbering.
- [ ] `runtime-execution-fabric-spec-addendum.md` turns the design into functional requirements.
- [ ] `omnigent-execution-fabric-integration-tasks.md` supplies dependency-ordered tasks and negative oracles.
- [ ] Whole-plan review records all material remaining gaps and closure/defer status accurately.
