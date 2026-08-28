# S2 Acceptance Contract

## Authority

This file defines evidence required to accept S2 planning and, later, S2 implementation. It does not itself accept either.

```text
PLANNING_TRUSTED_BASE_EXPECTED_SHA = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
INITIAL_REVIEWED_PLANNING_HEAD_SHA = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
PLANNING_ACCEPTED = NO
S2_IMPLEMENTATION_ACCEPTED = NO
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

`INITIAL_REVIEWED_PLANNING_HEAD_SHA` is historical review input only. Any tracked repair creates a new head and makes all prior head-bound qualification/review evidence stale.

## A. Planning-package acceptance

All of the following are required before the eleven-file package can be described as canonical planning:

- [ ] Exact live PR head SHA is recorded from GitHub immediately before qualification/acceptance.
- [ ] Exact live PR base SHA and exact trusted canonical `main` SHA used for the decision are both recorded; they must match.
- [ ] The recorded trusted canonical `main` is the expected v21 planning base or a separately authorized compatible trusted successor.
- [ ] Diff contains exactly the eleven v21-authorized S2 planning paths and no others.
- [ ] Exact-head Foundation/candidate policy qualification succeeds.
- [ ] Trusted-base v21 admission genuinely accepts the exact candidate as data; candidate policy is not allowed to self-authorize.
- [ ] v21 exact-package enforcement is exercised successfully.
- [ ] External-review egress preflight is recorded for the exact current base/head/file scope before hosted review.
- [ ] Independent review evidence records reviewer identity/product, qualification for the change class, independence, exact base/head coverage, completion state, and findings. If no qualified reviewer can complete, record `REVIEW_BLOCKED` and keep `PLANNING_ACCEPTED = NO`.
- [ ] Every valid material finding is reconciled; clean output from another reviewer never erases a valid finding.
- [ ] Any tracked repair invalidates stale head-bound evidence and is requalified/rereviewed as required.
- [ ] No unresolved material review threads remain.
- [ ] Security accounting is explicit; missing specialist review is never called PASS.
- [ ] Final race check re-reads live canonical `main`, PR base/head, exact diff, review threads, and required check state immediately before Ready.
- [ ] Ready transition occurs only after the exact-head evidence above is complete.
- [ ] Ready-triggered trusted-base admission is reread and genuinely PASSes on the same exact head.
- [ ] Merge is guarded with `expected_head_sha` protection and uses an allowed non-destructive merge method.
- [ ] Post-merge canonical `main` is re-read and must contain the guarded merge result.
- [ ] Post-merge Foundation succeeds on the exact canonical merge head before planning is called canonical.

Planning merge/activation grants no product implementation authority.

## A.1 Independent-review evidence states

```text
REVIEW_COMPLETE_CLEAN
REVIEW_COMPLETE_WITH_FINDINGS
REVIEW_BLOCKED
REVIEW_STALE_AFTER_HEAD_CHANGE
```

Only a completed, qualified, independent review bound to the exact current candidate can satisfy the planning review gate. `REVIEW_BLOCKED`, a trigger request, a pending status, a summary generated before completion, or a review on a superseded head cannot satisfy it.

## B. Implementation-authority acceptance

Before any S2 source mutation:

- [ ] Canonical planning package is re-read from live `main`.
- [ ] Ponytail FULL result is revalidated against any changed implementation assumption.
- [ ] Source Acquisition Check is revalidated for task-specific machinery.
- [ ] The first implementation-authority successor is minimum and append-only; the preferred initial tranche is contracts-only unless canonical evidence proves a smaller/different tranche necessary.
- [ ] Successor policy grants exact implementation paths/effects and denies everything else.
- [ ] Exact dependency/source admissions are explicit; none are inferred from package availability or transitive lock presence.
- [ ] External Git process route is explicitly `NONE` or separately, exactly bounded and authorized.
- [ ] Network authority remains none for S2.
- [ ] Model/provider authority remains none.
- [ ] S3/S4/later slices remain denied.
- [ ] Successor self-tests cover mixed/unknown path denial, frozen predecessor preservation, and authority drift.
- [ ] Successor is independently reviewed, guardedly merged, and proven active from canonical `main` before product code begins.

## C. Product behavior acceptance — Open Project

Evidence must prove:

- [ ] normal Git repository opens deterministically;
- [ ] subdirectory resolves to documented root semantics;
- [ ] non-Git directory opens with repository facts unavailable rather than invented;
- [ ] linked worktree relationship is represented without collapsing contexts;
- [ ] submodule/superproject semantics are deterministic;
- [ ] bare repository is explicit;
- [ ] move/rename reassociation is conservative;
- [ ] clone/copy ambiguity cannot silently false-merge identities;
- [ ] symlink/junction/reparse facts are handled according to threat model;
- [ ] concurrent first-open operations for one previously unseen project cannot allocate different local project IDs;
- [ ] a crash after first-open reservation but before initialization causes the reservation to be reused/recovered, not replaced by a second identity;
- [ ] project tree is not mutated by opening;
- [ ] no network/model/provider is required;
- [ ] Git trust refusal is preserved and not auto-bypassed.

## D. Local evidence-store acceptance

- [ ] data root is documented and qualified per platform;
- [ ] store filenames use WePLD-safe IDs, not raw project paths/remotes;
- [ ] records are versioned and bounded;
- [ ] first-open identity creation is serialized by a bounded store-wide catalog reservation protocol before any per-project lock can be relied upon;
- [ ] project updates use a single committed-generation boundary: readers select one committed generation and never combine `identity`, `index`, or evidence records from different generations;
- [ ] a small atomic current-generation pointer/manifest commit, or an equivalently proven algorithm, is the only transition that makes a generation current;
- [ ] orphan/incomplete generations and stale temporary artifacts are never promoted merely because individual files parse;
- [ ] malformed/truncated records cannot become current evidence;
- [ ] unsupported schema is explicit;
- [ ] payload/digest mismatch is detected where digest applies;
- [ ] lock acquisition is bounded and cancellable; exhaustion maps to a stable busy error rather than an indefinite wait;
- [ ] lock-file existence alone is never ownership proof; OS-owned locks release on handle/process termination under the qualified platform semantics;
- [ ] concurrent writer tests prove no silent mixed/torn state;
- [ ] crash/failure-injection tests cover every generation construction, manifest/current-pointer, and catalog-reservation boundary;
- [ ] permission failures are explicit;
- [ ] durability wording matches measured platform semantics and never overclaims power-loss/directory-entry guarantees;
- [ ] persisted fields pass privacy/secret-redaction tests.

## E. Project Doctor acceptance

- [ ] stable finding-code registry exists;
- [ ] identity conflict/ambiguity findings are covered;
- [ ] repository/worktree/trust findings are covered;
- [ ] workspace/toolchain descriptor findings are covered;
- [ ] lockfile/package-manager ambiguity is covered;
- [ ] evidence corruption/freshness findings are covered;
- [ ] security-sensitive configuration observations are evidence-linked;
- [ ] every blocking finding cites safe evidence references and non-executable remediation text;
- [ ] finding summaries/explanations/remediation templates do not interpolate raw secret-bearing config, environment, remote URL, command output, or arbitrary repository-controlled text;
- [ ] TTY and JSON output use the same allowlisted/redacted semantic fields and are proven secret-free with adversarial fixtures;
- [ ] Doctor executes no build/test/install/task remediation in S2;
- [ ] Doctor does not claim build/test health without execution evidence.

## F. CLI acceptance

- [ ] `open`, `doctor`, `status` share versioned core contracts;
- [ ] human output is readable and escapes project-controlled terminal control data;
- [ ] `--json` is stable, deterministic, ANSI-free, schema-versioned, and subject to the same secret-redaction policy as human output;
- [ ] `--no-input` never prompts;
- [ ] exact exit-code mapping is documented/tested;
- [ ] stable busy/capability-unavailable/identity-conflict classes are machine distinguishable;
- [ ] unknown command remains an error with suggestions;
- [ ] unknown command never becomes an AI prompt;
- [ ] Desktop/agent/CI surfaces can consume the same logical contracts without duplicating project logic.

## G. Security acceptance

- [ ] threat-model abuse cases have deterministic tests;
- [ ] path prefix/canonicalization is never used as authority proof;
- [ ] TOCTOU limitation remains explicit;
- [ ] Git executable qualification is proven if adapter admitted;
- [ ] Git stdout/stderr/parser bounds are proven if adapter admitted;
- [ ] `safe.directory` negative oracle passes;
- [ ] secret-bearing remote/config/environment values cannot escape through persisted evidence, Doctor finding text, TTY output, JSON, logs, or diagnostics;
- [ ] evidence parser size/version limits pass;
- [ ] descriptor discovery uses the exact root allowlist and explicit parse/file/aggregate/depth bounds frozen by the plan;
- [ ] no hidden project script/hook/task execution path exists;
- [ ] no hidden network path exists;
- [ ] applicable Codex Security scan runs when available/egress-permitted, or exact `NOT_RUN_NON_BLOCKING`/`NOT_APPLICABLE` limitation is retained without implying PASS;
- [ ] security reviewer result is never treated as completion authority.

## H. Platform acceptance

- [ ] Windows gate passes applicable path/worktree/store tests.
- [ ] Linux gate passes applicable path/worktree/store tests.
- [ ] macOS gate passes or an explicit unsatisfied coverage limitation blocks any claim requiring macOS qualification.
- [ ] non-UTF8/Unicode path representation contract is proven on applicable platforms.
- [ ] case/path separator/extended-length path behavior has targeted fixtures.
- [ ] lock deadline/crash-release semantics are tested on each claimed platform/filesystem class or retained as an explicit limitation.

## I. Performance and bounded-discovery acceptance

- [ ] baseline open proves no whole-repository traversal.
- [ ] descriptor discovery examines only the exact root-level allowlist frozen by `plan.md`.
- [ ] parsed descriptor per-file bytes, aggregate bytes, candidate count, and structured nesting depth are hard-bounded before allocation/parse.
- [ ] lockfiles/manager markers designated presence-only are not parsed merely for baseline Doctor.
- [ ] over-limit descriptor fixtures fail/return bounded findings without unbounded reads or recursion.
- [ ] evidence read has explicit record/aggregate byte bounds.
- [ ] selected performance fixture is content/topology identified.
- [ ] published latency/ceiling evidence is reproducible.
- [ ] performance optimization does not bypass correctness/security checks.

## J. Review/completion acceptance

Before S2 can become `CLOSED_CANONICAL`:

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
FOUNDER/CANONICAL_AUTHORITY = REQUIRED
GUARDED_MERGE = REQUIRED
POST_MERGE_CANONICAL_EVIDENCE = REQUIRED
BUILD_LEARNING_CAPTURE = REQUIRED
```

Forbidden equivalences:

```text
Green CI != Completion
Merge != Completion
Review clean != Completion
Review pending != Review complete
Doctor healthy != Effect authority
Evidence present != Fresh evidence
Canonical path != Project authority
Source available != Source admitted
Planning complete != Implementation authorized
```

## K. Current planning status

```text
PONYTAIL_FULL = COMPLETE_FOR_PLANNING_CANDIDATE
SOURCE_ACQUISITION_CHECK = COMPLETE_FOR_PLANNING_CANDIDATE
THREAT_MODEL = COMPLETE_FOR_PLANNING_CANDIDATE
INITIAL_HEAD_REVIEW = COMPLETE_WITH_MATERIAL_FINDINGS
TRACKED_REPAIR = REQUIRED
EXACT_HEAD_FOUNDATION_AFTER_REPAIR = REQUIRED
INDEPENDENT_REVIEW_AFTER_REPAIR = REQUIRED
PLANNING_CANONICAL = NO
NEXT_AUTHORITY = NOT_GRANTED
```
