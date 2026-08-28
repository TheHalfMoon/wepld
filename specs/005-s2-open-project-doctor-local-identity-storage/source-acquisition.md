# S2 Source Acquisition Check

## Gate result

```text
CHECK_DATE = 2026-08-28
CHECK_SCOPE = S2_PLANNING_ONLY
SOURCE_ACQUISITION_CHECK = COMPLETE_FOR_PLANNING
SOURCE_IMPORT = NONE
SOURCE_ADMISSION = NONE
NEW_DEPENDENCY_ADMISSION = NONE
EXTERNAL_BINARY_EXECUTION_AUTHORITY = NONE
DONOR_EXECUTION_DURING_PLANNING = NONE
```

This check identifies behavior oracles and native/admitted machinery. It does not import donor code or grant implementation authority.

## 1. Canonical registry

Read first:

- `docs/acquisition/SOURCE_REGISTRY_INDEX.md`

Registry state at the trusted base remains:

```text
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
BROAD_DISCOVERY = CLOSED
SOURCE_ADMISSION = NONE
PATH_LEVEL_MINING = CAPABILITY_TRIGGERED
```

S2 uses capability-triggered source research only.

## 2. Native/admitted machinery

### Rust standard library

Official references observed 2026-08-28:

- `https://doc.rust-lang.org/std/path/`
- `https://doc.rust-lang.org/std/path/fn.absolute.html`
- `https://doc.rust-lang.org/std/fs/`
- `https://doc.rust-lang.org/std/fs/fn.canonicalize.html`
- `https://doc.rust-lang.org/std/fs/struct.File.html`
- `https://doc.rust-lang.org/std/fs/fn.rename.html`

Relevant qualified behavior:

- lexical path operations and filesystem canonicalization are different operations;
- `canonicalize` resolves symbolic links and on Windows can return extended-length path syntax;
- filesystem operations are subject to TOCTOU;
- Rust 1.97.1 includes file locking/try-lock primitives;
- `rename` has platform-dependent replacement behavior and cannot cross mount points.

Role:

```text
RUST_STDLIB = NATIVE_BEHAVIOR_ORACLE + PRIMARY_IMPLEMENTATION_CANDIDATE
SOURCE_IMPORT = NONE
```

### Existing WePLD serialization

Trusted base manifests:

```text
wepld-contracts
  serde = 1.0.229
  serde_json = 1.0.151

wepld-core
  wepld-contracts = path dependency
```

Role:

```text
EXISTING_ADMITTED_MACHINERY = PREFERRED
NEW_SERIALIZATION_DEPENDENCY = REJECT_INITIAL
```

A direct new dependency declaration in `wepld-core` is still dependency mutation and requires authority even if the package exists transitively.

## 3. Git — primary repository-topology oracle

Official references observed 2026-08-28:

- `https://git-scm.com/docs/git-rev-parse`
- `https://git-scm.com/docs/git-worktree`
- `https://git-scm.com/docs/git-config`

Relevant behavior:

- `rev-parse` exposes worktree top-level, Git directory, Git common directory, bare/worktree state, and superproject context;
- linked worktrees carry distinct worktree metadata while sharing repository data;
- `git worktree list --porcelain -z` is intended for stable script parsing;
- `safe.directory` is protected configuration intended to prevent an untrusted repository from declaring itself trusted.

Acquisition decision:

```text
GIT_SOURCE_IMPORT = NONE
GIT_BINARY_BUNDLING = NONE
GIT_EXECUTION_AUTHORITY = NOT_GRANTED
GIT_ROLE = BEHAVIOR_ORACLE + NARROW_SYSTEM_TOOL_ADAPTER_CANDIDATE
```

If implementation selects the Git adapter, qualify the installed executable, exact commands, environment, output bounds, timeout, parser, trust-refusal behavior, and no-network/no-hook guarantees before authority is granted.

## 4. Cargo

Official references:

- `https://doc.rust-lang.org/cargo/reference/workspaces.html`
- `https://doc.rust-lang.org/cargo/commands/cargo-metadata.html`

Useful behavior patterns:

- workspaces separate root/member concepts;
- `cargo metadata` provides versioned machine-readable workspace/package information.

Decision:

```text
ROLE = WORKSPACE_BEHAVIOR_ORACLE
CARGO_EXECUTION_IN_S2 = NOT_ADMITTED_BY_PLANNING
SOURCE_IMPORT = NONE
```

S2 may detect Cargo descriptors without running Cargo. Later execution/metadata use requires exact authority.

## 5. npm / pnpm / uv

Official references:

- `https://docs.npmjs.com/cli/using-npm/workspaces/`
- `https://pnpm.io/workspaces`
- `https://docs.astral.sh/uv/concepts/projects/workspaces/`

Useful behavior:

- workspace root/member semantics;
- explicit lock/workspace descriptors;
- ecosystem-native commands remain visible rather than hidden behind WePLD.

Decision:

```text
ROLE = WORKSPACE_AND_TOOLCHAIN_BEHAVIOR_ORACLE
EXECUTION = NOT_ADMITTED_IN_S2_PLANNING
SOURCE_IMPORT = NONE
```

## 6. mise / just

Official references:

- `https://mise.jdx.dev/tasks/`
- `https://just.systems/man/en/`

Useful behavior:

- discoverable task definitions;
- source/output freshness concepts;
- excellent command-runner UX and errors.

Decision:

```text
ROLE = DOCTOR/FUTURE_COMMAND_PLANE_BEHAVIOR_ORACLE
TASK_EXECUTION = LATER_SLICE
SOURCE_IMPORT = NONE
```

## 7. GitHub CLI

Official reference:

- `https://cli.github.com/manual/gh_help_formatting`

Useful behavior:

- explicit `--json` machine output;
- structured filtering/templates without scraping human prose.

Decision:

```text
ROLE = CLI_MACHINE_OUTPUT_BEHAVIOR_ORACLE
SOURCE_IMPORT = NONE
```

S2 adopts the pattern, not GitHub CLI code.

## 8. Dagger / Nx

References:

- `https://docs.dagger.io/`
- `https://nx.dev/ci/features/affected`

Useful later behavior:

- local/CI workflow parity;
- affected/task graph computation.

Decision:

```text
ROLE = FUTURE_S3/S4_ORACLE
S2_IMPLEMENTATION_USE = REJECT_PULL_FORWARD
SOURCE_IMPORT = NONE
```

Nx graph behavior belongs with S4 semantic/project graph work, not S2.

## 9. OpenAI Codex safety architecture

Current official product guidance is useful as a later process-boundary oracle for sandbox/approval/network policy, but S2 does not execute agents or general commands.

Decision:

```text
ROLE = FUTURE_PROCESS/AUTHORITY_ORACLE
S2_RUNTIME_USE = NONE
```

## 10. Database candidates

SQLite/embedded KV stores were considered as solved machinery for durability/querying.

Decision:

```text
STATUS = REJECT_INITIAL / TOO_EARLY
RATIONALE = S2 only requires a small identity/evidence foundation; a DB expands dependency, migration, native/supply-chain, and recovery surfaces before need is proven.
```

Reopen only if deterministic implementation evidence shows the file-backed design cannot satisfy required cross-platform durability/concurrency semantics.

## 11. Directory helper candidates

`dirs`/`directories`-class crates were considered for platform data roots.

Decision:

```text
STATUS = DEFER
RATIONALE = first qualify the small platform path contract against standard/platform APIs; admit a helper only if concrete complexity/coverage evidence justifies it.
```

## 12. Hash/ID candidates

A digest and opaque local ID may require implementation machinery not yet frozen.

Decision:

```text
STATUS = TASK_SPECIFIC_ACQUISITION_REQUIRED_BEFORE_USE
SILENT_DEPENDENCY_ADMISSION = PROHIBITED
```

The requirement is retained; the package is not selected prematurely.

## 13. License / provenance posture

No donor code is copied in this planning package. Behavior-oracle documentation is cited by public URL. Therefore:

```text
THIRD_PARTY_SOURCE_COPIED = NO
THIRD_PARTY_NOTICE_CHANGE = NONE
LICENSE_ADMISSION = NONE
SBOM_CHANGE = NONE
```

Any later source import requires exact revision, license/NOTICE obligations, source review, tests/failure-mode review, security/maintenance/exit strategy, and canonical source admission.

## 14. Final acquisition decision

```text
USE_EXISTING_ADMITTED_CONTRACT_SERIALIZATION = YES_PREFERRED
USE_RUST_STDLIB_FILESYSTEM_LOCKING = YES_PREFERRED_SUBJECT_TO_TESTS
NARROW_GIT_ADAPTER = CANDIDATE_REQUIRES_SEPARATE_EFFECT_AUTHORITY
NEW_DATABASE = NO
NEW_ASYNC_RUNTIME = NO
NEW_AGENT_FRAMEWORK = NO
NEW_GRAPH_ENGINE = NO
NEW_MODEL_PROVIDER = NO
NEW_SOURCE_IMPORT = NO
NEW_DEPENDENCY_ADMISSION = NO
```

Source Acquisition is complete for the planning/no-import boundary. Before any S2 implementation authority is granted, unresolved task-specific machinery (Git execution, digest, opaque ID generation, data root, durability claims) must be reconciled explicitly; this planning result never auto-admits them.
