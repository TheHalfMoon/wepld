# S2 Specification — Open Project + Project Doctor + Local Identity/Storage

## 1. Problem statement

WePLD cannot become the developer command plane until it can answer a basic question deterministically: **what project is the user asking WePLD to reason about, what facts are currently known about it, and how fresh/trustworthy are those facts?**

Today S1 provides the Desktop ↔ Rust trusted-core foundation. S2 must add project identity, diagnostics, and local evidence foundations without pulling Terminal Fabric or Fehrest's semantic graph forward.

## 2. User outcomes

### UO-1 — Open an unfamiliar repository

A developer can conceptually run:

```text
wepld open .
```

and receive a deterministic project identity/status record that explains what WePLD resolved, what repository/worktree topology was observed, what evidence was stored, and which observations are uncertain or unavailable.

### UO-2 — Diagnose readiness

A developer can conceptually run:

```text
wepld doctor
```

and receive structured findings about project identity, repository state, project/toolchain descriptors, lockfile/package-manager ambiguity, evidence freshness, and security-sensitive configuration—without S2 installing, fixing, building, testing, or executing project tasks.

### UO-3 — Inspect current WePLD project state

A developer can conceptually run:

```text
wepld status
```

and receive the currently associated project identity plus evidence-store health/freshness without requiring a model or network service.

## 3. Scope

### In scope

- local path/project opening semantics;
- Git-aware repository/worktree topology as an observed fact source;
- non-Git local project support with explicitly weaker repository facts;
- local identity records and conservative reassociation;
- deterministic Project Doctor findings;
- content/freshness/provenance primitives;
- local evidence-store durability foundation;
- human + JSON command contract design;
- negative/adversarial/path-platform qualification;
- Windows-first behavior plus Linux/macOS portability contracts.

### Out of scope

- code/symbol/reference/call graph;
- project-native command execution;
- arbitrary shell/process execution;
- package installation or environment mutation;
- CI orchestration;
- agents/models/providers;
- network/remote repository fetching;
- cloud sync/telemetry;
- automatic remediation;
- Nawat grants or Mission Runtime;
- final Fehrest storage/index architecture.

## 4. Domain model

### 4.1 ProjectLocator

Represents where the user pointed WePLD, not what the project permanently *is*.

Required facts:

```text
input_path
lexical_absolute_path
resolved_path = value | unavailable(error_class)
observation_time
```

`lexical_absolute_path` and `resolved_path` remain separate. A failed filesystem canonicalization must not destroy the original locator or fabricate a resolved value.

### 4.2 RepositoryTopology

When Git topology can be qualified, capture separate facts:

```text
vcs_kind = git
worktree_root
absolute_git_dir
git_common_dir
is_bare
is_inside_worktree
superproject_worktree = value | none | unavailable
linked_worktree_state = known | unknown
trust_state = trusted | refused_by_git | unknown
```

Remote URLs are optional sanitized observations only. Credentials/userinfo must never be persisted in plaintext evidence. Remote identity is mutable and is not repository authority.

### 4.3 LocalProjectIdentity

A WePLD-owned local identifier stored outside the repository and bound to a versioned evidence set.

Required behavior:

- opening a never-seen project may create a new local identity record;
- opening the same confidently matched project may reuse that identity;
- moves/renames may reassociate only under deterministic evidence rules;
- copies/clones/worktrees with ambiguous evidence must not silently collapse into one identity;
- an ambiguity result must expose candidate identities and require a later explicit reconciliation mechanism rather than guessing.

The spec does not claim a universal immutable Git repository ID exists.

### 4.4 EvidenceEnvelope

Minimum durable envelope:

```text
schema_version
record_id
record_kind
project_id
producer
producer_contract_version
observed_at
freshness_basis
payload_digest
provenance
status
payload
```

`status` is a closed enum including at least:

```text
complete
partial
stale
corrupt
unavailable
```

An evidence record is information, never effect authority.

### 4.5 DoctorFinding

Minimum structure:

```text
finding_code
severity
category
summary
explanation
observed_evidence_refs[]
remediation_kind
remediation_text
machine_action_hint = optional descriptive value only
```

S2 remediation hints are non-executable descriptions.

## 5. Functional requirements

### FR-001 — Explicit project locator

`open` accepts an explicit local path. `.` is permitted. Empty/invalid paths fail with a stable usage or project-resolution error.

### FR-002 — No implicit network

Project opening, doctor, and status perform no network access as part of S2.

### FR-003 — Path observation layers

WePLD preserves input, lexical absolute, and filesystem-resolved forms separately. It never treats string prefix comparison alone as proof of filesystem containment.

### FR-004 — Symlink/reparse awareness

The project-resolution contract must detect/report relevant symbolic-link and Windows reparse/junction facts when they affect root resolution or safety. Symlink loops, broken targets, denied metadata, and races produce explicit diagnostic states.

### FR-005 — Git topology without `.git` assumptions

Git repositories may use `.git` directories, gitfiles, linked worktrees, bare repositories, submodules, or alternate/common directories. S2 must not derive repository topology by assuming `<root>/.git` is a directory.

### FR-006 — Git trust refusal preservation

If the Git trust boundary refuses repository access, WePLD records `refused_by_git` (or equivalent) and explains it. WePLD does not automatically add or wildcard `safe.directory`.

### FR-007 — Non-Git project support

A directory can still be a WePLD local project without Git. Repository-specific facts then remain unavailable rather than synthesized.

### FR-008 — Nested repository clarity

If the supplied path lies inside nested repository candidates, WePLD identifies the selected root and reports relevant nesting ambiguity. Selection rules must be deterministic and documented.

### FR-009 — Worktree distinction

Linked worktrees sharing a common Git repository remain distinguishable as worktrees. The local project model must support both repository relationship and worktree-specific identity/context.

### FR-010 — Conservative local identity

Identity matching uses a versioned deterministic rule set. Weak observations cannot silently override stronger contradictory evidence.

### FR-011 — Identity collision guard

If two observed projects map to the same candidate identity key but contradict required topology evidence, the operation fails into an identity-conflict state rather than overwriting the existing record.

### FR-012 — External local store

The default S2 evidence/identity store lives under a WePLD-owned per-user local data location, not in the opened repository. The exact platform path must be defined and qualified during implementation planning/authority.

### FR-013 — Repository read-only opening

Opening/doctor/status must not create or modify files inside the target project in S2.

### FR-014 — Durable writes

Local-store updates use a crash-aware transaction pattern: construct a complete new record, validate it, write to a same-store temporary location, flush at the required durability level, then commit/replace according to qualified platform semantics. Partial writes must not be accepted as complete records.

### FR-015 — Concurrent writers

Two WePLD processes must not silently corrupt the same project identity/evidence state. The implementation plan must use an admitted standard-library or otherwise qualified locking/serialization strategy and define stale-lock/crash behavior.

### FR-016 — Content addressing

Evidence payloads that claim content identity use a deterministic digest with explicit algorithm/version label. Digest equality is content equality evidence only; it is not authority.

### FR-017 — Freshness

Each freshness-sensitive observation defines what invalidates or ages it. Wall-clock timestamps alone are not sufficient proof that a fact remains current.

### FR-018 — Doctor categories

Minimum doctor categories:

- `identity`;
- `repository`;
- `workspace`;
- `toolchain_descriptor`;
- `lockfile`;
- `package_manager`;
- `evidence_store`;
- `freshness`;
- `security_sensitive_config`.

### FR-019 — Dirty/conflicted state seam

The contract supports dirty/untracked/conflicted repository diagnostics, but actual Git process invocation or repository-parser machinery requires separately granted implementation/effect authority. Planning must not self-authorize it.

### FR-020 — Toolchain discovery is descriptive

Detecting manifests/configuration (for example Cargo/npm/pnpm/uv/mise/just/Make/Gradle/Maven/Go/Nx) identifies project-native ecosystems and candidate commands. Detection does not execute or install them.

### FR-021 — Package-manager ambiguity

If multiple package-manager indicators or conflicting lockfiles exist, Doctor reports ambiguity rather than choosing silently.

### FR-022 — Workspace awareness seam

S2 may identify workspace roots/members from deterministic descriptors or qualified read-only metadata sources, but does not construct the S4 semantic code graph.

### FR-023 — Evidence corruption handling

Malformed, truncated, digest-mismatched, unsupported-version, or partially committed records are quarantined/ignored as invalid and surfaced by Doctor. They are never silently promoted to current evidence.

### FR-024 — Privacy

The store must not persist secrets merely because they appear in repository configuration, remote URLs, environment variables, or command output. Stored evidence schemas use allowlisted fields; raw environment capture is prohibited.

### FR-025 — Human output

TTY output prioritizes the selected project, health summary, important findings, evidence age, and next safe actions.

### FR-026 — JSON output

`--json` returns a versioned deterministic schema with no ANSI formatting and no prose-only fields required for machine interpretation.

### FR-027 — Noninteractive behavior

`--no-input` prohibits prompts. Any operation requiring unresolved user choice exits with a stable non-success code and a machine-readable ambiguity/error payload.

### FR-028 — Exit codes

S2 planning reserves stable classes at minimum for:

```text
0 success
2 usage/input error
3 project resolution/identity error
4 evidence-store integrity error
5 doctor completed with blocking findings
6 required capability unavailable
1 unexpected/internal failure
```

Exact numeric compatibility must be reconciled against existing CLI conventions before implementation; this list is a planning candidate, not yet runtime contract.

### FR-029 — Unknown commands

Unknown CLI tokens are errors with suggestions. They are never treated as model prompts.

### FR-030 — Evidence for `wepld why`

S2 evidence must retain enough provenance to support a later `wepld why this project is unhealthy` explanation without requiring an LLM to invent project facts. S2 does not implement the full `why` command.

## 6. Security requirements

### SR-001

Never use repository-controlled configuration to weaken the trust boundary that judges that repository.

### SR-002

Never execute repository hooks, scripts, build files, package lifecycle scripts, task runners, shell snippets, or binaries merely to open/doctor a project under S2.

### SR-003

Any future use of the Git executable is an external-process effect. It requires an exact allowlisted command/environment/output contract and separate implementation authority. Git output is untrusted input to be parsed boundedly.

### SR-004

Path canonicalization is an observation, not a containment proof. Effect-bearing path access later must revalidate at effect time.

### SR-005

Store paths and filenames must be derived from WePLD-owned safe encodings/identifiers, not raw repository names or remotes.

### SR-006

Evidence parsing is bounded by file count/record size/field size/version limits defined before implementation.

### SR-007

Store corruption or permission anomalies fail closed for claims that depend on durable evidence.

## 7. Non-functional requirements

### NFR-001 — Fast open

S2 opening must avoid whole-repository traversal. Identity and baseline Doctor should be proportional to a bounded set of root/topology descriptors, not repository file count.

### NFR-002 — Determinism

Given the same qualified local observations, output ordering, finding codes, JSON field semantics, and identity matching decisions are deterministic.

### NFR-003 — Cross-platform

Windows is first-class. Tests must cover Windows path forms, drive roots, case behavior, extended-length paths, symlinks/junctions/reparse points where the test environment permits, plus Unix symlinks and permission failures.

### NFR-004 — Explainability

Every blocking Doctor finding references the evidence that caused it and a safe remediation explanation.

### NFR-005 — Backward-compatible schemas

Machine-facing schemas are versioned from first release; unknown future fields must not be confused with authority.

## 8. Acceptance scenarios

1. Normal Git repository opens to one local project identity with separate locator/worktree/git/common-dir facts.
2. Same project reopened from a subdirectory deterministically resolves to the same project/worktree association.
3. Linked worktree is recognized as related to the same Git common repository while remaining a distinct worktree context.
4. Git ownership refusal is reported; WePLD does not alter `safe.directory`.
5. Non-Git directory opens with repository facts unavailable but valid local project identity.
6. Broken symlink/reparse target yields explicit resolution failure/diagnostic, not fallback to a guessed root.
7. Multiple lockfiles/package-manager indicators produce Doctor ambiguity.
8. Truncated/corrupt local evidence is not consumed as current and is reported.
9. Two concurrent writers cannot silently produce a valid-looking torn record.
10. `--json --no-input` produces deterministic machine output and never prompts.
11. Opening does not mutate the target repository.
12. No S2 operation requires network/model/provider access.

## 9. Planning status

```text
SPEC_STATUS = PROPOSED_FOR_REVIEW
IMPLEMENTATION = BLOCKED_BY_AUTHORITY
SOURCE_IMPORT = NONE
DEPENDENCY_ADMISSION = NONE
```
