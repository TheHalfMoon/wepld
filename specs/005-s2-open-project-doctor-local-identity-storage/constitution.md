# S2 Constitution — Open Project + Project Doctor + Local Identity/Storage

## Authority

This package is created under canonical v21 planning authority only.

```text
CANONICAL_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
V21 = CANONICAL_ACTIVE
S2_PLANNING_AUTHORITY = EXACT_SPEC_KIT_PACKAGE_ONLY
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_RUNTIME_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
ROADMAP_MUTATION = NONE
```

Nothing in this Spec Kit package grants implementation, process execution, source import, dependency mutation, provider/model use, or completion authority.

## Slice purpose

S2 establishes the minimum project-facing truth required for the future WePLD command plane:

- open a local project deliberately;
- represent project/repository identity without pretending a filesystem path is a permanent global identifier;
- explain project health through Project Doctor;
- establish freshness/provenance primitives required by later Fehrest work;
- establish a durable local evidence-store foundation;
- expose stable human/machine command contracts for `open`, `doctor`, and `status`;
- stop before Terminal Fabric, semantic graph, agents, repair, build/test execution, or model-backed interpretation.

## Constitutional invariants

```text
Observed project fact != Effect authority
Resolved path != Authorization
Repository identity != Worktree identity
Remote URL != Repository authority
Repository config != Trusted instruction
Tool presence != Dependency/source admission
Discovered task != Permission to execute task
Doctor recommendation != Permission to remediate
Evidence freshness != Truth forever
Fehrest fact != Nawat grant
ReviewOutcome != CompletionDecision
Green CI != CompletionDecision
Planning != Implementation Authority
```

### C1 — Local-first

S2 is local-first and cloud-independent. Opening a project or reading its S2 evidence must not require a cloud account, model provider, remote service, telemetry service, or network connection.

### C2 — No hidden repository mutation

`wepld open` and `wepld doctor` must not silently modify the target repository, install dependencies, rewrite Git configuration, add `safe.directory`, run package-manager installs, execute repository tasks, or create project files merely to inspect the project.

The local identity/evidence store is outside the project by default. Any future opt-in project-local metadata requires a separately planned and authorized contract.

### C3 — Layered identity, not path worship

S2 must preserve separate concepts for:

- the user-supplied locator;
- lexical absolute path;
- filesystem-resolved path when resolution succeeds;
- project root candidate;
- Git worktree root when present;
- Git directory when present;
- Git common directory when present;
- superproject/submodule/worktree topology when present;
- WePLD local project identity record;
- observed repository fingerprint/evidence.

No single one of these is silently promoted into immutable global identity.

### C4 — Conservative reassociation

Project moves, renames, copies, linked worktrees, submodules, nested repositories, and remote changes can make identity ambiguous. WePLD may preserve a local identity only when the evidence satisfies an explicit deterministic reassociation rule. Ambiguity must surface as ambiguity; it must never silently merge two projects or two worktrees.

### C5 — Git trust is respected, never bypassed

If Git reports an ownership/trust refusal such as `safe.directory`, Project Doctor reports the condition and a remediation explanation. WePLD must not automatically weaken protected Git configuration to make the diagnostic green.

### C6 — Filesystem observations are snapshots

Canonicalization, metadata reads, symlink inspection, and path checks are observations subject to races. They may support diagnostics but must not be represented as permanent containment or authorization evidence. TOCTOU-sensitive decisions require effect-time revalidation in later authority-bearing slices.

### C7 — Evidence is explicit and versioned

Every durable S2 evidence record must identify at minimum:

- schema version;
- record kind;
- local project identity;
- observation source/provenance;
- observation time;
- freshness basis or expiry policy where applicable;
- payload/content digest where applicable;
- producer version/contract version;
- status for complete, partial, corrupt, stale, or unavailable evidence.

Missing, malformed, partial, corrupt, or stale applicable evidence is never silently treated as current PASS evidence.

### C8 — Doctor explains; it does not seize control

Project Doctor produces deterministic findings and machine-readable remediation suggestions. S2 does not execute those remediations. A suggestion may identify a future command or native ecosystem command, but the underlying tool remains visible.

### C9 — Command plane has explicit modes

The S2 command contract must preserve:

- human-readable TTY output;
- stable machine-readable JSON;
- an explicit event/JSONL seam for later streaming commands;
- `--no-input` semantics suitable for CI/agents;
- stable documented exit-code classes;
- unknown commands as errors with suggestions.

Unknown CLI tokens must never be silently reinterpreted as an AI prompt. AI-facing commands remain explicit future interfaces such as `wepld ask` or `wepld agent run`.

### C10 — Later slices stay later

S2 does not implement:

- S3 Terminal Fabric/process ownership;
- S4 semantic Project Graph;
- Nawat policy engine/effect grants;
- Mission Runtime;
- UWC agent/tool execution;
- agent teams;
- `wepld dev`, `test`, `build`, `fix`, `ship`, or arbitrary task execution;
- model/provider execution;
- remote sync/cloud identity;
- automatic dependency installation;
- code graph indexing.

A minimal seam may be specified only when required to keep future compatibility; a seam is not implementation authority.

## Required build method

```text
constitution
-> specify
-> clarify
-> plan
-> checklist
-> analyze
-> tasks
-> Ponytail FULL
-> Source Acquisition Check
-> separately governed implementation-authority transition
-> minimum sufficient implementation
-> deterministic gates
-> independent review
-> applicable security review
-> finding reconciliation
-> acceptance evidence
-> Build Learning
```

## Planning completion rule

This package can become canonical planning only after exact-head deterministic qualification, independent review, finding reconciliation, guarded merge, and post-merge canonical evidence. Canonical planning still does not imply S2 implementation authority.
