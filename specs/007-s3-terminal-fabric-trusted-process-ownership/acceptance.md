# S3 Acceptance Contract

## Authority

This file defines evidence required to accept S3 planning and, later, S3 implementation. It does not itself accept either.

```text
PLANNING_TRUSTED_BASE_EXPECTED_SHA = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
INITIAL_REVIEWED_PLANNING_HEAD_SHA = NOT_YET_ASSIGNED
PLANNING_ACCEPTED = NO
S3_IMPLEMENTATION_ACCEPTED = NO
S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

`INITIAL_REVIEWED_PLANNING_HEAD_SHA` must be filled in with the exact PR head SHA at first review submission, and re-verified live rather than trusted from this file on every subsequent read. Any tracked repair creates a new head and makes all prior head-bound qualification/review evidence stale.

## A. Planning-package acceptance

All of the following are required before this package can be described as canonical planning:

- [ ] Exact live PR head SHA is recorded from GitHub immediately before qualification/acceptance.
- [ ] Exact live PR base SHA and exact trusted canonical `main` SHA used for the decision are both recorded; they must match.
- [ ] The recorded trusted canonical `main` is `28e42da95e4d6304f24c1d2513ebd40f6f1c483a` or a separately authorized compatible trusted successor.
- [ ] Diff contains exactly this package's planning paths under `specs/007-s3-terminal-fabric-trusted-process-ownership/` and no others.
- [ ] Exact-head `foundation-integrity`/candidate policy qualification succeeds.
- [ ] Trusted-base `s1-admission-integrity` admission genuinely accepts the exact candidate as data; candidate policy is not allowed to self-authorize.
- [ ] External-review egress applies `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md` from the exact trusted canonical `main` and records content classification, approved secret/private-data screening evidence, provider-handling decision, egress approval, and the exact current base/head/file scope before any hosted review. If any required control is missing, fails, is unavailable, or yields prohibited/unknown egress, record `EGRESS_BLOCKED`, do not trigger hosted review, and keep `PLANNING_ACCEPTED = NO`.
- [ ] Independent review evidence records reviewer identity/product, qualification for the change class, independence, exact base/head coverage, completion state, and findings. If no qualified reviewer can complete, record `REVIEW_BLOCKED` and keep `PLANNING_ACCEPTED = NO`.
- [ ] Every valid material finding is reconciled; clean output from another reviewer never erases a valid finding.
- [ ] Any tracked repair invalidates stale head-bound evidence and is requalified/rereviewed as required.
- [ ] No unresolved material review threads remain.
- [ ] Security accounting is explicit; missing specialist review is never called PASS.
- [ ] Before each GitHub mutation in this acceptance flow, the current founder/canonical authorizing identity, explicit decision, authorized operation/scope, and the head/base facts the decision depends on are recorded as live evidence. Missing, withdrawn, stale, or scope-mismatched authorization prohibits that mutation.
- [ ] Final race check re-reads live canonical `main`, PR base/head, exact diff, review threads, and required check state immediately before Ready.
- [ ] Ready transition occurs only after the exact-head evidence above is complete.
- [ ] Ready-triggered trusted-base admission is reread and genuinely PASSes on the same exact head.
- [ ] Merge is separately guarded with `expected_head_sha` protection and uses an allowed non-destructive merge method; authorization evidence must still be current for the exact merge head.
- [ ] Post-merge canonical `main` is re-read and must contain the guarded merge result.
- [ ] Post-merge `foundation-integrity` succeeds on the exact canonical merge head before planning is called canonical.

Planning merge/activation grants no product implementation authority.

## A.1 Independent-review evidence states

```text
REVIEW_COMPLETE_CLEAN
REVIEW_COMPLETE_WITH_FINDINGS
REVIEW_BLOCKED
REVIEW_STALE_AFTER_HEAD_CHANGE
```

Only a completed, qualified, independent review bound to the exact current candidate can satisfy the planning review gate. `REVIEW_BLOCKED`, a trigger request, a pending status, a summary generated before completion, or a review on a superseded head cannot satisfy it. A rate-limit refusal (per this repository's own live experience on PRs #329/#335) is a provider message, never a review.

## B. Implementation-authority acceptance

Before any S3 source mutation:

- [ ] Canonical planning package is re-read from live `main`.
- [ ] Ponytail FULL result is revalidated against any changed implementation assumption.
- [ ] Source Acquisition Check is revalidated for task-specific machinery, in particular the exact Windows API binding crate.
- [ ] The first implementation-authority successor is minimum and append-only; the preferred initial tranche is `S3-AUTH-C` contracts-only unless canonical evidence proves a smaller/different tranche necessary.
- [ ] Successor policy grants exact implementation paths/effects and denies everything else.
- [ ] Exact dependency/source admissions are explicit; none are inferred from package availability or transitive lock presence.
- [ ] Process-spawn (`SPAWN_PROCESS_TREE`) authority remains explicitly `NONE` until a separately qualified `S3-AUTH-SPAWN` successor.
- [ ] Network authority remains none for S3, at every stage.
- [ ] Model/provider authority remains none.
- [ ] Distributed/multi-host runner fencing, credential brokering, harness/worker protocol adapters, and native desktop bridge capability remain denied at every S3 stage.
- [ ] S4/S5/S6/later-slice authority remains denied.
- [ ] Successor self-tests cover mixed/unknown path denial, frozen predecessor preservation, and authority drift.
- [ ] Successor is independently reviewed, guardedly merged, and proven active from canonical `main` before any Core runtime code begins.

## C. Host / runner / process-tree identity acceptance

Evidence must prove:

- [ ] `ServerDescriptor`/`HostDescriptor`/`RunnerDescriptor` remain distinct typed identities even where one process implements more than one role;
- [ ] `HostDescriptor.host_execution_opt_in_state` defaults false and is not set by any S1/S2 code path;
- [ ] `ProcessTreeIdentity` distinguishes a reused OS PID from the original process-tree identity via start-time (or equivalent) binding;
- [ ] `ownership_epoch` refuses an `EffectProposal` bound to a superseded epoch;
- [ ] no S3 evidence type or code path claims observation/ownership authority over a process WePLD did not itself spawn.

## D. Containment acceptance

- [ ] `ContainmentCapabilityReport` is produced only after explicit host qualification, never automatically at connect time;
- [ ] `ContainmentPosture` represents each dimension independently; no boolean `sandboxed` field satisfies any acceptance decision;
- [ ] a host with incomplete qualification cannot produce a stronger-than-`UNKNOWN` claim on any dimension;
- [ ] Windows Job-Object-class investigation is the primary, first-qualified backend;
- [ ] `PROCESS_TREE_ONLY` containment is never consumed as satisfying a filesystem- or network-isolation requirement;
- [ ] an expired `ContainmentCapabilityReport` cannot back a new `EffectProposal` without re-qualification;
- [ ] an unrecognized/unsupported OS or backend version fails closed to `NONE`/`UNKNOWN`.

## E. Effect envelope / PEP seam acceptance

- [ ] `EffectProposal.proposed_effect_kind` is a closed enum; an unrecognized kind is rejected, not passed through;
- [ ] `RuntimeCeiling`'s effective envelope is an intersection; an empty intersection blocks the proposal;
- [ ] `EnvironmentExposurePolicy` is deny-by-default; no ambient environment inheritance occurs by default for any spawned process;
- [ ] no `EffectResult` exists without a resolved `PEPDecision` for the same proposal;
- [ ] a missing/stale/malformed policy input yields `UNKNOWN_FAIL_CLOSED`, never `ALLOW`;
- [ ] any planning-only self-test PEP evaluator is documented as a test double and is not reachable from a real product surface;
- [ ] cancellation against a live effect is bounded and covers the entire process tree, not only a top-level process;
- [ ] `EffectDependency` blocks a dependent irreversible effect while its prerequisite outcome is unavailable or `UNKNOWN`;
- [ ] an `UNKNOWN` outcome is reconciled only via a new, separately evidenced record, never an in-place rewrite;
- [ ] the revalidation triggers in `spec.md` FR-015 each demonstrably stale a prior envelope/decision when exercised.

## F. Command-plane acceptance

Not applicable. S3 adds no `wepld` CLI subcommand (`plan.md` §6). This section is retained for structural parity with S2's acceptance contract and to make the absence of a CLI surface an explicit, checked fact rather than a silent omission.

- [x] No CLI subcommand is added, changed, or reserved by this package.

## G. Security acceptance

- [ ] threat-model abuse cases (`threat-model.md` §5) have deterministic tests;
- [ ] a vendor/provider self-reported `sandboxed` claim is never used directly as `ContainmentPosture` evidence;
- [ ] repository-controlled content cannot influence `PEPDecision.decision_source` or widen a `RuntimeCeiling`;
- [ ] `SPAWN_PROCESS_TREE`, if and when admitted, uses a closed allowlisted argv shape, never a shell string;
- [ ] no raw environment value or unredacted process output appears in any S3 durable evidence record;
- [ ] cancellation/timeout paths are bounded so an untrusted or hung process cannot force an indefinite wait;
- [ ] no S3 domain type or code path performs or requires network access;
- [ ] applicable Codex Security scan runs when available/egress-permitted, or exact `NOT_RUN_NON_BLOCKING`/`NOT_APPLICABLE` limitation is retained without implying PASS;
- [ ] security reviewer result is never treated as completion authority.

## H. Platform acceptance

- [ ] Windows gate passes all Windows-backed tests applicable to the current S3 execution surface.
- [ ] Linux/macOS gates record explicit `NONE`/`UNKNOWN` containment evidence rather than a silently absent row.
- [ ] Job-Object-class investigation is proven on at least one qualified Windows version; unqualified versions are explicit `UNKNOWN`, not assumed.

### H.1 `S2-S003` — adopted cross-slice obligation disposition

Per `constitution.md`'s "Adopted cross-slice obligation" section and `clarify.md` Q19, this package adopts responsibility for `S2-S003` (native Windows junction/reparse coverage), previously recorded as `OPEN_CROSS_SLICE_OBLIGATION` with `EXPECTED_NEXT_OWNER = S3_PLANNING` in `specs/005-s2-open-project-doctor-local-identity-storage/acceptance.md` §H.1 and `tasks.md`.

```text
S2_S003_ADOPTED = YES (this package)
S2_S003_DISCHARGE_REQUIRES = actual native Windows wepld-core CI execution, established by
  a future S3-AUTH-HOST implementation stage — not by this planning package alone
S2_S003_DISCHARGED_BY_THIS_PACKAGE = NO (planning cannot discharge an implementation-evidence obligation)
S2_S003_DISPOSITION_AT_THIS_PACKAGE_CLOSE = MUST_BE_RECORDED_EXPLICITLY_BELOW
```

At S3 planning acceptance, exactly one of the following must be true and recorded:

- [ ] `S2-S003` remains explicitly `OPEN_CROSS_SLICE_OBLIGATION`, now owned by S3 (not S2), pending the `S3-AUTH-HOST` implementation stage that has not yet occurred; **or**
- [ ] `S3-AUTH-HOST` has already landed by the time this package closes, native Windows `wepld-core` CI execution genuinely exists, and `S2-S003`'s original fixtures have been run for real on that surface with linked evidence, closing `S2-S003` with genuine proof.

This package must never close with `S2-S003` silently dropped or unaddressed. If S3 itself closes without reaching `S3-AUTH-HOST`, S3's own acceptance must carry `S2-S003` forward explicitly to the next slice, using the same disposition language S2 used here.

## I. Performance acceptance

- [ ] host/containment qualification completes in bounded time, independent of anything beyond the fixed API surface being probed;
- [ ] a measured cancellation deadline is published once Job-Object termination behavior is characterized (`plan.md` §4.4), not asserted without measurement;
- [ ] the planning-only self-test PEP evaluator's evaluation cost is O(1) against its fixed allowlist;
- [ ] performance optimization does not bypass correctness/security checks.

## J. Review/completion acceptance

Before S3 can become `CLOSED_CANONICAL`:

```text
EXACT_HEAD_DETERMINISTIC_GATES = REQUIRED
TRUSTED_BASE_ADMISSION = REQUIRED
EXACT_HEAD_EGRESS_PREFLIGHT = REQUIRED
INDEPENDENT_REVIEW = REQUIRED
REVIEW_BLOCKED = NOT_ACCEPTED
UNRESOLVED_MATERIAL_FINDINGS = 0
FINAL_RACE_CHECK = REQUIRED
READY_TRIGGERED_ADMISSION = REQUIRED
SECURITY_ACCOUNTING = REQUIRED
FOUNDER/CANONICAL_AUTHORITY = REQUIRED_FOR_EACH_GITHUB_MUTATION
GUARDED_MERGE = REQUIRED
POST_MERGE_CANONICAL_EVIDENCE = REQUIRED
BUILD_LEARNING_CAPTURE = REQUIRED
S2_S003_DISPOSITION_RECORDED = REQUIRED (see §H.1)
```

Forbidden equivalences:

```text
Green CI != Completion
Merge != Completion
Review clean != Completion
Review pending != Review complete
Containment reported != Containment guaranteed
PEP seam present != Policy engine complete
Evidence present != Fresh evidence
Envelope shape defined != Effect executed
Planning complete != Implementation authorized
```

## K. Current planning status

```text
PONYTAIL_FULL = COMPLETE_FOR_INITIAL_PLANNING_CANDIDATE
SOURCE_ACQUISITION_CHECK = COMPLETE_FOR_INITIAL_PLANNING_CANDIDATE
THREAT_MODEL = COMPLETE_FOR_INITIAL_PLANNING_CANDIDATE
ANALYZE = COMPLETE_FOR_INITIAL_PLANNING_CANDIDATE
INITIAL_HEAD_REVIEW = NOT_YET_SUBMITTED
PLANNING_CANONICAL = NO
NEXT_AUTHORITY = NOT_GRANTED
```
