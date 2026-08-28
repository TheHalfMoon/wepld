# S2 Acceptance Contract

## Authority

This file defines evidence required to accept S2 planning and, later, S2 implementation. It does not itself accept either.

```text
PLANNING_ACCEPTED = NO
S2_IMPLEMENTATION_ACCEPTED = NO
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

## A. Planning-package acceptance

All of the following are required before the eleven-file package can be described as canonical planning:

- [ ] Exact live PR head SHA recorded.
- [ ] PR base equals the then-current trusted canonical `main` expected by v21.
- [ ] Diff contains exactly the eleven v21-authorized S2 planning paths and no others.
- [ ] Foundation/candidate policy qualification succeeds on the exact head.
- [ ] v21 exact-package enforcement is exercised successfully.
- [ ] External-review egress preflight recorded before hosted review.
- [ ] At least one qualified independent correctness/engineering review covers the exact head.
- [ ] Every valid material finding reconciled.
- [ ] Any tracked repair is requalified and rereviewed as required.
- [ ] No unresolved material review threads.
- [ ] Security accounting is explicit; missing specialist review is never called PASS.
- [ ] Ready transition occurs only after exact-head evidence.
- [ ] Merge is guarded with expected-head protection.
- [ ] Post-merge Foundation succeeds on the exact canonical merge head.

Planning merge/activation grants no product implementation authority.

## B. Implementation-authority acceptance

Before any S2 source mutation:

- [ ] Canonical planning package re-read from live `main`.
- [ ] Ponytail FULL result revalidated against any changed implementation assumption.
- [ ] Source Acquisition Check revalidated for task-specific machinery.
- [ ] Append-only successor policy grants exact S2 implementation paths.
- [ ] Exact dependency/source admissions are explicit; none inferred from availability/transitivity.
- [ ] External Git process route is explicitly `NONE` or exactly bounded/authorized.
- [ ] Network authority remains none for S2.
- [ ] Model/provider authority remains none.
- [ ] S3/S4/later slices remain denied.
- [ ] Successor self-tests cover mixed/unknown path denial and authority drift.
- [ ] Successor independently reviewed and canonically activated.

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
- [ ] project tree is not mutated by opening;
- [ ] no network/model/provider is required;
- [ ] Git trust refusal is preserved and not auto-bypassed.

## D. Local evidence-store acceptance

- [ ] data root is documented and qualified per platform;
- [ ] store filenames use WePLD-safe IDs, not raw project paths/remotes;
- [ ] records are versioned and bounded;
- [ ] malformed/truncated records cannot become current evidence;
- [ ] unsupported schema is explicit;
- [ ] payload/digest mismatch is detected where digest applies;
- [ ] concurrent writer test proves no silent mixed/torn state;
- [ ] crash/failure-injection tests cover pre-write/pre-replace/post-replace points;
- [ ] permission failures are explicit;
- [ ] stale temp artifacts are handled without fabricating a committed record;
- [ ] durability wording matches measured platform semantics;
- [ ] persisted fields pass privacy/secret-redaction tests.

## E. Project Doctor acceptance

- [ ] stable finding-code registry exists;
- [ ] identity conflict/ambiguity findings are covered;
- [ ] repository/worktree/trust findings are covered;
- [ ] workspace/toolchain descriptor findings are covered;
- [ ] lockfile/package-manager ambiguity is covered;
- [ ] evidence corruption/freshness findings are covered;
- [ ] security-sensitive configuration observations are evidence-linked;
- [ ] every blocking finding cites evidence and remediation text;
- [ ] Doctor executes no build/test/install/task remediation in S2;
- [ ] Doctor does not claim build/test health without execution evidence.

## F. CLI acceptance

- [ ] `open`, `doctor`, `status` share versioned core contracts;
- [ ] human output is readable and escapes project-controlled terminal control data;
- [ ] `--json` is stable, deterministic, ANSI-free, and schema-versioned;
- [ ] `--no-input` never prompts;
- [ ] exact exit-code mapping is documented/tested;
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
- [ ] secret-bearing remote/config data redaction passes;
- [ ] evidence parser size/version limits pass;
- [ ] no hidden project script/hook/task execution path exists;
- [ ] no hidden network path exists;
- [ ] applicable Codex Security scan runs when available/egress-permitted, or exact `NOT_RUN_NON_BLOCKING` limitation is retained;
- [ ] security reviewer result is never treated as completion authority.

## H. Platform acceptance

- [ ] Windows gate passes applicable path/worktree/store tests.
- [ ] Linux gate passes applicable path/worktree/store tests.
- [ ] macOS gate passes or an explicit unsatisfied coverage limitation blocks any claim requiring macOS qualification.
- [ ] non-UTF8/Unicode path representation contract is proven on applicable platforms.
- [ ] case/path separator/extended-length path behavior has targeted fixtures.

## I. Performance acceptance

- [ ] baseline open proves no whole-repository traversal.
- [ ] descriptor scan has explicit file-count/byte bounds.
- [ ] evidence read has explicit record/aggregate byte bounds.
- [ ] selected performance fixture is content/topology identified.
- [ ] published latency/ceiling evidence is reproducible.
- [ ] performance optimization does not bypass correctness/security checks.

## J. Review/completion acceptance

Before S2 can become `CLOSED_CANONICAL`:

```text
EXACT_HEAD_DETERMINISTIC_GATES = REQUIRED
INDEPENDENT_REVIEW = REQUIRED
UNRESOLVED_MATERIAL_FINDINGS = 0
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
EXACT_HEAD_FOUNDATION = NOT_YET_RECORDED
INDEPENDENT_REVIEW = NOT_YET_RECORDED
PLANNING_CANONICAL = NO
NEXT_AUTHORITY = NOT_GRANTED
```
