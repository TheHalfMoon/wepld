# S2 Implementation Plan — Planning Candidate Only

## Authority header

```text
CANONICAL_PLANNING_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
S2_PLANNING_AUTHORITY = EXACT_SPEC_KIT_PACKAGE_ONLY
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

This document defines the minimum implementation shape to qualify later. It does not authorize source mutation.

## 1. Architectural target

```text
Human CLI        Agent / CI interfaces        Desktop
     \                  |                       /
      \                 |                      /
             WePLD Command Plane
                     |
          Project Context Boundary
             /        |        \
      Identity      Doctor     Evidence
         |             |          |
       Trusted Rust Core / WePLD contracts
```

S2 makes project context a first-class core concept. Desktop remains a projection over the same contracts rather than owning separate project logic.

## 2. Minimal module ownership candidate

### `crates/contracts`

Own versioned serializable contract types:

- `ProjectLocator`;
- `RepositoryTopology`;
- `LocalProjectIdentity` / `ProjectIdentityRecord`;
- `EvidenceEnvelope` and status/provenance/freshness types;
- `DoctorReport`, `DoctorFinding`, `RemediationHint`;
- command response/error JSON contracts;
- canonical serialization helpers required by the evidence store.

Existing admitted `serde`/`serde_json` remain the preferred serialization substrate. No new package is granted by this plan.

### `crates/core`

Candidate modules, subject to later exact-path authority:

```text
project/
  locator.rs
  identity.rs
  repository.rs
  doctor.rs
  discovery.rs

evidence/
  store.rs
  record.rs
  freshness.rs

cli or command boundary
  open
  doctor
  status
```

The exact filenames must be fixed by the later implementation-authority bootstrap; this planning package must not create them.

## 3. Project identity algorithm candidate

### Phase I — observe locator

1. preserve exact user locator;
2. derive lexical absolute path without filesystem resolution;
3. attempt filesystem canonicalization;
4. record failures explicitly;
5. inspect bounded root metadata without whole-repository traversal.

### Phase II — observe repository topology

If Git qualification is available under later authority:

- resolve worktree root;
- resolve absolute Git directory;
- resolve common Git directory;
- detect bare/worktree state;
- detect superproject context;
- optionally enumerate linked worktrees using stable porcelain output;
- preserve Git ownership/trust refusal as a finding.

No Git command may be invoked until external-process authority is granted. No command may trigger network access or project hooks/scripts as part of S2.

### Phase III — match local identity

Use ordered evidence strength:

1. exact existing identity-store binding to currently revalidated strong topology facts;
2. deterministic move/reassociation rule with no conflicting strong facts;
3. otherwise create a new local identity or return ambiguity/conflict.

Do not use remote URL, repository name, or current HEAD alone as identity authority.

### Phase IV — persist evidence

Persist only allowlisted typed fields. Identity creation and evidence updates must be crash-aware and concurrency-safe.

## 4. Local evidence-store candidate

### 4.1 Layout

Use a WePLD-owned per-user data root. Candidate conceptual layout:

```text
<wepld-data>/
  projects/
    <safe-project-id>/
      identity.json
      evidence/
        <record-id>.json
      index.json
      lock
```

Names use WePLD-generated safe identifiers, never raw project paths/remotes.

Exact platform paths are implementation decisions requiring tests. No repository-local `.wepld` directory is created in S2.

### 4.2 Write protocol

Candidate protocol:

1. acquire project/store lock using qualified standard-library file locking where sufficient;
2. validate existing index/record versions and digests;
3. build complete new bytes in memory;
4. write to a unique same-directory temporary file;
5. flush file contents as required by the durability claim;
6. replace/rename within the same filesystem;
7. flush containing directory where supported/required or document residual platform limitation;
8. reread/validate committed record when required by acceptance tests;
9. release lock.

The implementation must not claim stronger crash durability than the platform evidence supports.

### 4.3 Corruption strategy

- never parse unbounded files;
- unsupported schema version => explicit unsupported state;
- malformed/truncated/digest mismatch => corrupt state;
- valid older records may remain readable behind versioned adapters;
- destructive cleanup is not automatic.

## 5. Project Doctor plan

Doctor is rule-based and deterministic in S2.

Initial rule families:

```text
D-ID-*      identity/reassociation/conflict
D-GIT-*     repository/worktree/trust/dirty-conflict seam
D-WS-*      workspace/root/member descriptors
D-TC-*      toolchain descriptor/version-hint facts
D-LOCK-*    lockfile presence/consistency/ambiguity
D-PM-*      package-manager ambiguity
D-EV-*      evidence store/corruption
D-FRESH-*   stale/unavailable evidence
D-SEC-*     security-sensitive configuration observations
```

Every rule returns evidence references and non-executable remediation text.

S2 explicitly does not prove that builds/tests pass. Later slices attach execution evidence.

## 6. Command-plane plan

### `wepld open <path>`

- resolve/observe project;
- establish or match local identity;
- persist S2 evidence if permitted by local-store authority;
- return human or JSON result;
- no project mutation;
- no network;
- no model.

### `wepld doctor [path|project]`

- evaluate bounded deterministic doctor rules;
- return findings sorted by stable category/code;
- optionally refresh only those S2 observations explicitly allowed by the command contract;
- no remediation execution.

### `wepld status`

- show active/selected local project identity;
- show evidence-store health/freshness;
- report unavailable association explicitly.

### Machine interface

All three commands share versioned response envelopes. Human output is a projection; JSON is not generated by scraping terminal prose.

## 7. External-process decision gate

S2 topology accuracy benefits from official Git behavior, but Git invocation is an effect and may parse repository configuration. Therefore implementation must split into one of two qualified routes:

### Route A — narrow Git adapter (preferred if authorized)

Exact command set candidate:

```text
git rev-parse --show-toplevel
git rev-parse --absolute-git-dir
git rev-parse --git-common-dir
git rev-parse --is-bare-repository
git rev-parse --is-inside-work-tree
git rev-parse --show-superproject-working-tree
git worktree list --porcelain -z
```

Before admission define:

- executable resolution/trust rule;
- environment allowlist;
- current directory semantics;
- `--no-optional-locks`/other safe invocation details if justified;
- timeout/cancellation;
- max stdout/stderr bytes;
- UTF-8/OS-string handling;
- exit-code mapping including `safe.directory` refusal;
- no network;
- no hooks/scripts;
- parser fuzz/negative tests.

### Route B — no-process filesystem discovery

If process authority is denied, implement only facts safely obtainable from filesystem/Gitfile structure and mark unavailable facts explicitly. Do not reimplement broad Git behavior merely to avoid a narrow, auditable adapter.

The authority bootstrap chooses the permitted route; this plan does not.

## 8. Workspace/tool discovery plan

S2 scans only a bounded root descriptor set such as:

- `Cargo.toml`, `Cargo.lock`;
- `package.json`, package-manager lockfiles/workspace descriptors;
- `pyproject.toml`, `uv.lock`;
- `mise.toml`, `.mise.toml`;
- `justfile`/`Justfile`;
- `Makefile`;
- Gradle/Maven descriptors;
- `go.mod`/`go.work`;
- Nx workspace descriptors.

This is descriptive discovery. Parsing depth is minimum sufficient for Doctor and future routing; it does not execute tools or construct the semantic graph.

## 9. Deterministic qualification matrix

Required test classes before S2 implementation acceptance:

### Unit/contract

- identity evidence strength ordering;
- ambiguity/conflict behavior;
- schema round trips;
- canonical JSON ordering/contract snapshots where required;
- finding ordering/codes;
- freshness state transitions;
- redaction.

### Filesystem adversarial

- missing path;
- permission denied;
- non-UTF8/Unicode paths where platform supports;
- `.`/`..` and long paths;
- symlink loops/broken links;
- Windows junction/reparse scenarios;
- case-only path differences;
- rename/move during observation;
- target replacement between checks.

### Git topology

If Route A is authorized:

- ordinary repo;
- subdirectory;
- bare repo;
- linked worktree;
- detached HEAD;
- unborn repository;
- submodule/superproject;
- gitfile;
- moved/prunable worktree;
- safe-directory refusal;
- malformed/bounded command output;
- spoofed/unqualified executable path negative case.

### Store durability

- concurrent writer contention;
- simulated crash before/after replace;
- truncated record;
- unsupported version;
- digest mismatch;
- stale temp files;
- permission loss;
- store move/partial deletion;
- recovery never fabricates PASS.

### CLI

- TTY vs non-TTY;
- JSON snapshots;
- `--no-input` never prompts;
- exit-code mapping;
- unknown command errors/suggestions;
- no accidental AI-prompt interpretation.

### Platform

- Windows required;
- Linux required;
- macOS when available or limitation retained explicitly.

## 10. Performance budgets to qualify

Planning targets, not PASS claims:

- opening a project must not traverse the entire repository;
- baseline `status` reads a bounded number of local evidence records;
- Doctor root discovery has explicit descriptor/file-count bounds;
- evidence parser has explicit per-record/aggregate byte bounds;
- external Git adapter, if admitted, has hard timeout/output bounds.

Benchmarks must publish fixture size/topology and p50/p95 or deterministic ceiling evidence before acceptance.

## 11. Implementation authority bootstrap

After this planning package becomes canonical, the next safe unit is expected to be a new append-only successor policy (provisionally `v22`) that grants **only** exact S2 implementation paths and the minimum qualified effects selected by this plan.

That successor must separately state:

```text
S2_IMPLEMENTATION_AUTHORITY = <exact bounded paths only>
DEPENDENCY_ADMISSION = <none unless separately qualified>
SOURCE_ADMISSION = <none unless separately qualified>
EXTERNAL_PROCESS_AUTHORITY = <none or exact Git adapter contract>
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S3_PLUS_AUTHORITY = NONE
```

The canonical plan cannot self-activate v22.

## 12. Delivery sequence

1. canonicalize this Spec Kit package;
2. independent exact-head planning review and reconciliation;
3. post-merge planning activation evidence;
4. design/qualify minimal v22 implementation-authority successor;
5. implement contracts first;
6. implement bounded locator/identity/store;
7. implement Doctor rules;
8. implement CLI projection;
9. adversarial/platform qualification;
10. independent correctness/security review;
11. bounded repair;
12. S2 acceptance + Build Learning only with exact evidence.
