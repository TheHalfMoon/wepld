# Requirements Checklist — Harness H0 Screening Falsification

This checklist evaluates planning quality and pre-implementation readiness only. Checked items mean the planning artifact contains an explicit contract; they do not mean implementation, Source Acquisition, screening, or H0 promotion is complete.

## Authority and scope

- [x] H0-SCREEN is explicitly outside roadmap S1..S10.
- [x] `ROADMAP_MUTATION = NONE` is explicit.
- [x] `S1_013_PLUS = NOT_STARTED` is explicit.
- [x] Spec Kit artifacts are distinguished from implementation/effect/source/completion authority.
- [x] H0-SCREEN has `PROMOTION_AUTHORITY = NONE`.
- [x] H0-CONFIRM execution is excluded.
- [x] Product Harness integration is excluded.
- [x] Frozen 402-source registry mutation is excluded.
- [x] Seven canonical Harness research documents are consumed without editing.

## Experimental arms

- [x] Exactly four arms A/B/C/D are defined.
- [x] A remains a smaller minimal baseline.
- [x] B/C/D share one predeclared component library.
- [x] B is globally fixed and non-routing.
- [x] C routes only from task/environment/budget-risk information.
- [x] C explicitly ignores model identity/profile and benchmark task IDs.
- [x] D uses C inputs plus a frozen ModelCapabilityProfile.
- [x] D calibration is disjoint from screening and confirmatory tasks.
- [x] D is deterministic and non-LLM-routed for H0 v1.
- [x] Self-evolution, dynamic harness code generation, sibling portfolios, and harness search are excluded.

## Component vocabulary

- [x] `ContextPolicy` options are bounded.
- [x] `ToolSurfacePolicy` options are bounded.
- [x] `PlanningPolicy` options are bounded.
- [x] `VerifierCadencePolicy` options are bounded.
- [x] `RecoveryPolicy` options are bounded.
- [x] `StopPolicy` options are bounded.
- [x] General memory and multi-agent delegation are excluded from H0-SCREEN.
- [x] Recipe compilers cannot select unknown components.

## Screening design

- [x] `DISTINCT_TASKS = 40` is frozen.
- [x] `ATTEMPTS_PER_TASK_ARM_MODEL = 1` is frozen.
- [x] Screening tasks are required to be disjoint from future confirmatory tasks.
- [x] Screening may validate plumbing/variance/cost/failure taxonomy only.
- [x] Screening may not satisfy GO criteria.
- [x] Same task instruction bytes are required across arms.
- [x] Same maximum budget envelope is required across paired arms.
- [x] Same maximum effect envelope is required across paired arms.
- [x] Same final objective verifier is required for a task across arms.
- [x] No unfavorable task/trial may be silently removed.

## Recipe conformance

- [x] R01 identical C input -> identical recipe hash.
- [x] R02 C ignores model identity.
- [x] R03 D may differ only through frozen model-profile routing.
- [x] R04 unknown component selection fails closed.
- [x] R05 authority expansion fails closed.
- [x] R06 budget expansion fails closed.
- [x] R07 benchmark/task-ID special-casing is prohibited.
- [x] RecipeDecisionTrace records machine-readable decision facts without chain-of-thought.

## Runner qualification

- [x] F01 deterministic passing task is required.
- [x] F02 deterministic failing task is required.
- [x] F03 false completion is required.
- [x] F04 timeout is required.
- [x] F05 process crash is required.
- [x] F06 malformed runner output is required.
- [x] F07 missing artifact is required.
- [x] F08 oversized stdout/stderr is required.
- [x] F09 verifier crash is required.
- [x] F10 cleanup failure is required.
- [x] F11 denied network attempt is required where enforceable.
- [x] F12 unexpected egress canary is required where instrumentable.
- [x] F13 synthetic secret-redaction boundary is required.
- [x] F14 parallel workspace isolation is required.
- [x] F15 retry-policy symmetry is required.
- [x] F16 run-order identity is required.
- [x] All required synthetic fixtures must pass before real screening tasks.

## Identity and evidence

- [x] Canonical serialization is required before execution.
- [x] Decision-relevant manifests are content-addressed.
- [x] TrialIdentity binds the full comparison cell.
- [x] Schedule position cannot change TrialIdentity.
- [x] Runner execution completion does not imply verified success.
- [x] Only the WePLD evidence finalizer may emit finalized trial semantics.
- [x] Verifier failure cannot fall back to model/harness claims.
- [x] Missing evidence becomes explicit `EVIDENCE_INCOMPLETE` where applicable.
- [x] Raw observations and original failures remain retained.
- [x] Normalized paired-analysis export is runner-neutral.

## Effects, secrets, and egress

- [x] Task-environment network is deny-by-default.
- [x] Model-provider egress is separated from task egress.
- [x] Runner/verifier/observability egress are separately accounted.
- [x] Merge/deploy/publish authority is denied.
- [x] Real credential values are prohibited from Git/manifests/public evidence.
- [x] Synthetic canary secrets are used for redaction testing.
- [x] Container privileged mode is denied.
- [x] Host container-engine socket is not exposed inside task environments.
- [x] External reviewer egress remains subject to canonical preflight policy.

## Retry and failure semantics

- [x] Task/harness/model/budget failures are not retried.
- [x] Shared infrastructure/provider replacement is capped at one when independently proven.
- [x] Original failed trial is retained.
- [x] Harness-induced crashes/loops/context failures remain outcomes.
- [x] Failure taxonomy is frozen before screening execution.

## Runner adequacy

- [x] Runner-caused invalid/incomplete rate is measured.
- [x] Runner overhead is measured.
- [x] Manual recovery burden is measured.
- [x] Resource contention is measured.
- [x] Runner retention threshold is `<= 2%` invalid/incomplete rate.
- [x] Runner retention threshold is `<= 15%` median overhead fraction.
- [x] Runner retention threshold is `<= 2 operator-hours / 100 completed trials`.
- [x] Distributed scheduler/cloud-backend requirement triggers runner re-evaluation.
- [x] Harbor remains conditional and not automatically admitted.

## Build method and source acquisition

- [x] Canonical Spec Kit order is followed.
- [x] Ponytail FULL is required before implementation.
- [x] Source Acquisition Check is required before implementation.
- [x] Existing S1 dependency admission is not assumed to authorize H0.
- [x] Rust-first trusted control/evidence logic is the planning preference.
- [x] Stdlib-first process execution is preferred.
- [x] A local container/runtime CLI is treated as replaceable external machinery.
- [x] No provider SDK is assumed.
- [x] No Harbor dependency is admitted for screening.
- [ ] Exact H0 direct dependency/component pins are qualified.
- [ ] Exact container/runtime boundary is qualified for real screening tasks.
- [ ] Exact model-provider integration boundary is qualified.
- [ ] H0 Source Acquisition Check reaches PASS.

## Implementation authorization

- [x] A separate trusted-base implementation policy is required after planning/acquisition.
- [x] Candidate-head self-check is not treated as bootstrap authority.
- [x] Post-merge policy activation proof is required.
- [ ] H0 implementation policy exists and is canonical.
- [ ] H0 implementation policy activation is proven.
- [ ] H0 source/dependency surface is admitted.
- [ ] H0 implementation has started.

## Review and acceptance

- [x] Independent correctness/engineering review is required for material planning/policy work.
- [x] Security-specialist review is applicable to policy/workflow trust changes when available and egress-permitted.
- [x] Reviewer output is evidence, not completion authority.
- [x] Exact-head egress preflight precedes manual external review.
- [x] Material head mutation invalidates stale review conclusions.
- [ ] Spec Kit canonicalization review complete.
- [ ] Ponytail/Source Acquisition review complete.
- [ ] Implementation deterministic gates complete.
- [ ] H0-SCREEN execution complete.

## Checklist verdict

```text
SPEC_KIT_REQUIREMENTS = SUFFICIENT_TO_PROCEED_TO_ANALYSIS
PONYTAIL_FULL = REQUIRED_NEXT_WITHIN_PLANNING_PACKET
SOURCE_ACQUISITION_CHECK = OPEN
H0_SCREEN_IMPLEMENTATION = BLOCKED
HARNESS_IMPLEMENTATION_AUTHORIZED = NO
S1_013_PLUS = NOT_STARTED
```
