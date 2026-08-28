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

and receive structured findings about project identity, repository state, project/toolchain descriptors, lockfile/package-manager ambiguity, evidence freshness, and security-sensitive configuration—without S2 installing, fixing, building, testing, executing project tasks, or leaking secret-bearing configuration through output.

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
- local identity records, serialized first-open reservation, and conservative reassociation;
- deterministic Project Doctor findings;
- content/freshness/provenance primitives;
- local evidence-store durability foundation with committed-generation consistency;
- human + JSON command contract design with one redaction policy;
- bounded root descriptor discovery;
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

Remote URLs are optional sanitized observations only. Credentials/userinfo must never be persisted or emitted in plaintext. Remote identity is mutable and is not repository authority.

### 4.3 LocalProjectIdentity

A WePLD-owned local identifier stored outside the repository and bound to a versioned evidence set.

Required behavior:

- opening a never-seen project may create a new local identity record only through the serialized first-open reservation protocol;
- opening the same confidently matched project may reuse that identity;
- an existing durable `reserved` first-open binding is reused/recovered after crash rather than replaced with another ID;
- moves/renames may reassociate only under deterministic evidence rules;
- copies/clones/worktrees with ambiguous evidence must not silently collapse into one identity;
- an ambiguity result must expose candidate identities through safe identifiers and require a later explicit reconciliation mechanism rather than guessing.

The spec does not claim a universal immutable Git repository ID exists.

### 4.4 IdentityCatalogReservation

First-open selection requires a store-wide coordination record because a per-project lock cannot protect an ID before that ID exists.

Minimum semantics:

```text
schema_version
reservation_key_version
revalidated_match_facts_digest
project_id
state = reserved | initialized
created_at
updated_at
```

The reservation key is derived only from the versioned, revalidated matching inputs defined by the identity algorithm; it is not a raw path/remote store filename and is not global repository authority.

A process that finds `reserved` under the catalog lock revalidates the match facts and completes/rejects the reservation deterministically. It does not invent a second ID.

### 4.5 EvidenceEnvelope

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

### 4.6 ProjectGenerationManifest

A project-store update is current only through one committed generation.

Minimum conceptual facts:

```text
generation_schema_version
generation_id
project_id
identity_record_ref
index_record_ref
evidence_record_refs[]
record_digests[]
producer_contract_version
created_at
```

The implementation may choose the exact serialized shape under later authority, but it must preserve this semantic rule: one `CURRENT` pointer/record selects exactly one complete generation, and readers never combine identity/index/evidence from different generations.

### 4.7 DoctorFinding

Minimum structure:

```text
finding_code
severity
category
summary_template_id
explanation_template_id
observed_evidence_refs[]
remediation_kind
remediation_template_id
machine_action_hint = optional closed descriptive value only
safe_parameters = allowlisted non-secret structured values only
```

Human `summary`, `explanation`, and `remediation_text` are projections from WePLD-owned templates plus allowlisted safe parameters. Arbitrary repository-controlled strings, raw config/environment values, remote URLs, or command output are not trusted prose inputs.

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

### FR-011 — Identity collision and first-open serialization guard

If two observed projects map to the same candidate identity key but contradict required topology evidence, the operation fails into an identity-conflict state rather than overwriting the existing record.

When no binding exists, selection/creation occurs under the bounded store-wide catalog reservation protocol **before** per-project locking can be relied upon. Concurrent opens of the same previously unseen project must converge on one reserved project ID or fail explicitly; they must not silently create two local identities.

### FR-012 — External local store

The default S2 evidence/identity store lives under a WePLD-owned per-user local data location, not in the opened repository. The exact platform path must be defined and qualified during implementation planning/authority.

### FR-013 — Repository read-only opening

Opening/doctor/status must not create or modify files inside the target project in S2.

### FR-014 — Generation-atomic durable writes

Local-store project updates use a crash-aware generation transaction:

1. hold the required bounded project lock;
2. construct a complete immutable generation containing identity/index/evidence records plus a manifest;
3. validate schema, references, and digests before commit;
4. write generation files to same-store temporary/final immutable locations and synchronize only to the durability level actually claimed;
5. atomically replace a small same-filesystem `CURRENT` pointer/record selecting that generation;
6. readers load `CURRENT` once and validate exactly that generation;
7. incomplete/orphan generations and temp files remain non-current.

A crash between individual file writes/replacements must not create a current mixed generation. The implementation must not claim stronger power-loss or directory-entry durability than platform evidence proves.

### FR-015 — Concurrent writers and bounded lock acquisition

Two WePLD processes must not silently corrupt the same identity/evidence state. The implementation uses qualified OS file-lock semantics or an explicitly admitted equivalent.

Command operations must not block indefinitely waiting for catalog/project locks. The initial contract candidate is:

```text
LOCK_ACQUIRE_DEADLINE_MS = 2000
LOCK_POLL_INTERVAL_MS = 25
CATALOG_BUSY_ERROR = identity_catalog_busy
PROJECT_STORE_BUSY_ERROR = store_busy
```

Polling uses non-blocking acquisition with cancellation checks. Lock-file existence alone is not ownership proof. A process crash/handle close must rely on qualified OS lock release semantics rather than homegrown stale-PID takeover.

### FR-016 — Content addressing

Evidence payloads that claim content identity use a deterministic digest with explicit algorithm/version label. Digest equality is content equality evidence only; it is not authenticity, freshness, or authority.

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

### FR-020 — Toolchain discovery is descriptive, closed, and bounded

Baseline S2 examines only the exact root-level descriptor/marker allowlist frozen in `clarify.md` and `plan.md`. Detection identifies project-native ecosystems and candidate commands; it does not execute or install them.

Parsed descriptor inputs are bounded before allocation/parse by:

```text
MAX_ROOT_DESCRIPTOR_CANDIDATES = 32
MAX_PARSED_DESCRIPTOR_BYTES = 1_048_576
MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES = 4_194_304
MAX_STRUCTURED_NESTING_DEPTH = 64
```

Lock/package-manager markers designated presence-only are not parsed merely for baseline ecosystem detection. Recursive arbitrary manifest discovery is not part of baseline S2.

### FR-021 — Package-manager ambiguity

If multiple package-manager indicators or conflicting lockfiles exist, Doctor reports ambiguity rather than choosing silently.

### FR-022 — Workspace awareness seam

S2 may identify root/workspace facts from the exact bounded descriptors or qualified read-only metadata sources, but does not construct the S4 semantic code graph. Deeper/member traversal requires a separately frozen capability-triggered contract.

### FR-023 — Evidence corruption handling

Malformed, truncated, digest-mismatched, unsupported-version, generation-mismatched, or partially committed records are quarantined/ignored as invalid and surfaced by Doctor. They are never silently promoted to current evidence.

### FR-024 — Privacy across storage and outputs

The store must not persist secrets merely because they appear in repository configuration, remote URLs, environment variables, or command output. Stored evidence schemas use allowlisted fields; raw environment capture is prohibited.

The same protection applies to Doctor findings, TTY/JSON projections, logs, and diagnostics. Raw secret-bearing values are not interpolated into summary/explanation/remediation text or machine hints.

### FR-025 — Human output

TTY output prioritizes the selected project, health summary, important findings, evidence age, and next safe actions. Project-controlled strings are escaped for terminal safety. Finding prose uses WePLD-owned templates plus allowlisted/redacted safe values only.

### FR-026 — JSON output

`--json` returns a versioned deterministic schema with no ANSI formatting and no prose-only fields required for machine interpretation. It is subject to the same field allowlist/redaction policy as human output; JSON mode is not a bypass for secret suppression.

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

Busy/contended conditions must be machine-distinguishable within the documented command error contract even if final numeric mapping reuses an existing compatible non-success class.

Exact numeric compatibility must be reconciled against existing CLI conventions before implementation; this list is a planning candidate, not yet runtime contract.

### FR-029 — Unknown commands

Unknown CLI tokens are errors with suggestions. They are never treated as model prompts.

### FR-030 — Evidence for `wepld why`

S2 evidence must retain enough provenance to support a later `wepld why this project is unhealthy` explanation without requiring an LLM to invent project facts. S2 does not implement the full `why` command.

### FR-031 — One generation per read decision

Any read operation that consumes durable project state records the selected generation ID and validates all referenced records against that generation manifest. If the pointer changes concurrently, the read either completes against the already-selected immutable generation or retries explicitly; it never opportunistically mixes the old and new generation.

### FR-032 — Reservation recovery

A durable catalog reservation has explicit `reserved|initialized` state. Under the catalog lock, a later opener may complete an abandoned `reserved` initialization only after revalidating the stored matching facts. Conflicting facts fail closed into ambiguity/conflict; the reservation is not silently rebound.

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

Evidence and descriptor parsing is bounded by file count/record size/aggregate size/field size/version and parser-depth limits defined before implementation.

### SR-007

Store corruption, generation mismatch, reservation conflict, permission anomalies, and unsupported schemas fail closed for claims that depend on durable evidence.

### SR-008

No raw secret-bearing repository/config/environment/remote/command-output value may cross into Doctor finding prose, TTY/JSON output, logs, or diagnostics. Safe output parameters are explicitly allowlisted and tested.

### SR-009

Lock contention is an availability boundary: acquisition is bounded/cancellable and returns stable typed errors. An untrusted or crashed peer must not cause an ordinary S2 command to wait forever.

## 7. Non-functional requirements

### NFR-001 — Fast open

S2 opening must avoid whole-repository traversal. Identity and baseline Doctor are proportional to a bounded set of root/topology descriptors, not repository file count.

### NFR-002 — Determinism

Given the same qualified local observations, output ordering, finding codes, JSON field semantics, identity matching decisions, reservation decisions, and generation selection are deterministic.

### NFR-003 — Cross-platform

Windows is first-class. Tests must cover Windows path forms, drive roots, case behavior, extended-length paths, symlinks/junctions/reparse points where the test environment permits, plus Unix symlinks and permission failures.

### NFR-004 — Explainability

Every blocking Doctor finding references the safe evidence identifiers that caused it and a safe remediation explanation.

### NFR-005 — Backward-compatible schemas

Machine-facing schemas are versioned from first release; unknown future fields must not be confused with authority.

### NFR-006 — Bounded waiting

Baseline command behavior has no unbounded lock wait, unbounded descriptor parse, unbounded evidence parse, or unbounded external-process wait if a Git adapter is later admitted.

## 8. Acceptance scenarios

1. Normal Git repository opens to one local project identity with separate locator/worktree/git/common-dir facts.
2. Same project reopened from a subdirectory deterministically resolves to the same project/worktree association.
3. Linked worktree is recognized as related to the same Git common repository while remaining a distinct worktree context.
4. Git ownership refusal is reported; WePLD does not alter `safe.directory`.
5. Non-Git directory opens with repository facts unavailable but valid local project identity.
6. Broken symlink/reparse target yields explicit resolution failure/diagnostic, not fallback to a guessed root.
7. Multiple lockfiles/package-manager indicators produce Doctor ambiguity.
8. Truncated/corrupt local evidence is not consumed as current and is reported.
9. Two concurrent ordinary writers cannot silently produce a valid-looking torn/mixed state.
10. Two concurrent first opens of one unseen project converge on one reserved project ID or one gets a stable busy outcome; they never commit two identities.
11. Crash after reservation but before initialization reuses/reconciles the reservation on retry.
12. Crash at every generation-file/manifest/`CURRENT` transition leaves either the prior generation current or the complete new generation current, never a mixed generation.
13. Held catalog/project locks reach the bounded deadline/cancellation path and return the documented busy error without hanging.
14. Descriptor candidates above per-file, aggregate, count, or nesting limits fail boundedly; presence-only lock markers are not parsed.
15. Credential-bearing remote URLs/config values/tokens/control characters do not appear in Doctor TTY or JSON output.
16. `--json --no-input` produces deterministic machine output and never prompts.
17. Opening does not mutate the target repository.
18. No S2 operation requires network/model/provider access.

## 9. Planning status

```text
SPEC_STATUS = REPAIRED_PLANNING_CANDIDATE_PENDING_FRESH_EXACT_HEAD_REVIEW
IMPLEMENTATION = BLOCKED_BY_AUTHORITY
SOURCE_IMPORT = NONE
DEPENDENCY_ADMISSION = NONE
```
