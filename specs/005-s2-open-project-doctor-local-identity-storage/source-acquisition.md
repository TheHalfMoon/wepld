# S2 Source Acquisition Check

## Gate result

```text
CHECK_DATE = 2026-08-28
CHECK_SCOPE = S2_PLANNING_ONLY
TRUSTED_BASE_OID = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
SOURCE_CHECK_INPUT_HEAD_OID = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
SOURCE_REGISTRY_INDEX_GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
SOURCE_ACQUISITION_CHECK = COMPLETE_FOR_PLANNING_INPUT
SOURCE_IMPORT = NONE
SOURCE_ADMISSION = NONE
NEW_DEPENDENCY_ADMISSION = NONE
EXTERNAL_BINARY_EXECUTION_AUTHORITY = NONE
DONOR_EXECUTION_DURING_PLANNING = NONE
```

`SOURCE_CHECK_INPUT_HEAD_OID` identifies the exact planning candidate whose assumptions were used for this acquisition pass. It is **not** a self-declared current acceptance head. Any tracked planning repair creates a new PR head; live GitHub base/head/check state must then be re-read and all head-bound qualification/review evidence refreshed before canonical planning acceptance.

This check identifies behavior oracles and native/admitted machinery. It does not import donor code or grant implementation authority.

## 1. Canonical registry — revision-bound

Registry input:

```text
PATH = docs/acquisition/SOURCE_REGISTRY_INDEX.md
TRUSTED_BASE_OID = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
BROAD_DISCOVERY = CLOSED
SOURCE_ADMISSION = NONE
PATH_LEVEL_MINING = CAPABILITY_TRIGGERED
```

The registry bytes above were read from the trusted base rather than inferred from candidate text. Canonical acceptance additionally requires live PR/check-state verification under `acceptance.md`; this file does not turn registry observations into completion authority.

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
- blocking file locks can wait indefinitely, so S2 planning selects bounded non-blocking `try_lock` polling rather than unbounded `lock` for command operations;
- OS file locks are a writer-coordination primitive, not a security boundary;
- lock-file existence alone is not ownership proof;
- `rename` has platform-dependent replacement/durability behavior and cannot cross mount points;
- file close errors can require explicit synchronization handling; directory-entry/power-loss semantics must not be overclaimed cross-platform.

Role:

```text
RUST_STDLIB = NATIVE_BEHAVIOR_ORACLE + PRIMARY_IMPLEMENTATION_CANDIDATE
SOURCE_IMPORT = NONE
```

### Existing WePLD serialization

Trusted-base manifests:

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
- `safe.directory` is protected configuration intended to prevent an untrusted repository from declaring itself trusted;
- `--no-optional-locks` disables optional locking side effects;
- runtime `GIT_CONFIG_*` and repository-redirection `GIT_*` variables can alter behavior and therefore must be scrubbed by any future adapter.

Acquisition decision:

```text
GIT_SOURCE_IMPORT = NONE
GIT_BINARY_BUNDLING = NONE
GIT_EXECUTION_AUTHORITY = NOT_GRANTED
GIT_ROLE = BEHAVIOR_ORACLE + NARROW_SYSTEM_TOOL_ADAPTER_CANDIDATE
FIRST_S2_SUCCESSOR_GIT_AUTHORITY = NONE
```

If implementation later selects the Git adapter, qualify the installed executable, exact commands, environment, output bounds, timeout, parser, trust-refusal behavior, no-network/no-hook guarantees, and project-tree/index non-mutation before authority is granted.

## 4. Cargo / npm / pnpm / uv / mise / just / Gradle / Maven / Go / Nx

These ecosystems are behavior oracles for workspace/toolchain descriptors only in baseline S2. Their commands are not executed.

The planning package now freezes a closed root-level descriptor/marker list in `clarify.md` and `plan.md`, plus explicit candidate-count, per-file, aggregate-byte, and nesting-depth ceilings.

Decision:

```text
ROLE = DESCRIPTOR_AND_WORKSPACE_BEHAVIOR_ORACLE
EXECUTION = NOT_ADMITTED
RECURSIVE_DISCOVERY = NOT_ADMITTED_IN_BASELINE_S2
SOURCE_IMPORT = NONE
```

Presence-only lock/package-manager markers are not parsed merely to identify ambiguity.

## 5. GitHub CLI

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

## 6. Dagger / Nx graph behavior

Useful later behavior includes local/CI workflow parity and affected/task graph computation.

Decision:

```text
ROLE = FUTURE_S3_S4_ORACLE
S2_GRAPH_OR_TASK_EXECUTION_USE = REJECT_PULL_FORWARD
SOURCE_IMPORT = NONE
```

## 7. OpenAI/Codex-style process safety architecture

Current process/sandbox/approval/network patterns are useful as later process-boundary oracles. S2 does not execute agents or general commands.

Decision:

```text
ROLE = FUTURE_PROCESS_AUTHORITY_ORACLE
S2_RUNTIME_USE = NONE
```

## 8. Database candidates

SQLite/embedded KV stores were considered as solved machinery for durability/querying.

Initial decision remains:

```text
STATUS = REJECT_INITIAL_TOO_EARLY
RATIONALE = S2 needs identity/evidence durability, not a general query engine
```

The CodeRabbit planning review exposed two real requirements that a naïve multi-file store had not solved: serialized first-open identity creation and a whole-project commit boundary. The minimum repair is **not** automatic database adoption. The plan now requires:

```text
STORE_WIDE_IDENTITY_RESERVATION = YES
IMMUTABLE_PROJECT_GENERATIONS = YES
ATOMIC_CURRENT_GENERATION_POINTER = YES
DATABASE = STILL_NOT_REQUIRED_BY_PLANNING
```

Reopen database/dependency acquisition only if deterministic cross-platform implementation evidence shows this bounded file-backed design cannot satisfy the required correctness/recovery contract.

## 9. Directory helper candidates

`dirs`/`directories`-class crates remain deferred. Platform data-root semantics are recorded separately in research issue #214; exact implementation machinery is qualified only when Core authority exists.

```text
STATUS = DEFER
SILENT_DEPENDENCY_ADMISSION = PROHIBITED
```

## 10. Hash / opaque-ID candidates — focused research completed, admission still none

Planning research issue #212 inspected the canonical Rust graph and upstream behavior.

Observed canonical lock candidates:

```text
uuid = 1.24.1
sha2 = 0.10.9
```

Provisional behavior choices:

```text
PROJECT_ID_CONTRACT = WEPLD_OWNED_OPAQUE_ID
CORE_GENERATION_CANDIDATE = UUID_V4
EVIDENCE_DIGEST_ALGORITHM_CANDIDATE = SHA_256
```

Important boundary:

```text
TRANSITIVE_PRESENCE != DIRECT_DEPENDENCY_ADMISSION
CONTRACTS_TRANCHE_DIRECT_UUID_EDGE = NONE
CONTRACTS_TRANCHE_DIRECT_SHA2_EDGE = NONE
CORE_DIRECT_EDGE = REQUIRES_SEPARATE_EXACT_ADMISSION_IF_USED
```

Never fall back to timestamp/PID/path hashing for opaque IDs if qualified randomness is unavailable.

## 11. Donor capability research — issues #211–#214

Non-authoritative research was durably recorded in GitHub without mutating the reviewed planning head:

```text
#211 memory/agent/search/evaluation donor capability map
#212 opaque ID and SHA-256 existing-graph research
#213 bounded read-only Git topology adapter research
#214 local data-root, lossless path, locking, and durability research
```

Representative donor dispositions:

- Mem0: history/lineage concept donor for future memory, not S2 evidence runtime;
- LangGraph: durable checkpoint/reconstruction concept donor for later mission state;
- Braintrust AgentBehavior: high-value evaluation/governance concept donor;
- Hermes: resilient state/migration/quarantine concept donor, rebuild contracts in Rust rather than porting trusted core;
- DeepSeek Harness: capability/plugin/event concept donor only; its own safety notice prevents treating it as a trust boundary;
- Qdrant: Project Brain/S4+ vector/search donor, not S2;
- Firecrawl: later acquisition adapter/oracle, not Rust trusted core; licensing/security isolation must be reviewed;
- LlamaIndex/LangChain: later retrieval/interoperability surfaces;
- AutoResearch: experiment-loop behavior oracle; source import blocked unless licensing is resolved.

Current S2 impact:

```text
MATERIAL_S2_RUNTIME_DEPENDENCY_DISCOVERED = NO
SOURCE_IMPORT_REQUIRED = NO
AGENT_FRAMEWORK_REQUIRED = NO
VECTOR_DATABASE_REQUIRED = NO
WEB_CRAWLER_REQUIRED = NO
MODEL_PROVIDER_REQUIRED = NO
```

## 12. Secret-safe Doctor output

The independent review identified that storage-only redaction is insufficient. No external package is required to fix this planning gap.

Selected minimum:

```text
FINDING_PROSE = WEPLD_OWNED_TEMPLATES
PARAMETERS = CLOSED_ALLOWLIST_SAFE_VALUES
RAW_ENV_CONFIG_REMOTE_COMMAND_OUTPUT_INTERPOLATION = PROHIBITED
TTY_JSON_REDACTION_POLICY = SHARED
```

This is contract/design work using admitted string/serialization machinery. A dedicated secret-scanner/redaction dependency is not admitted by planning.

## 13. License / provenance posture

No donor code is copied in this planning package. Behavior-oracle documentation is cited by public URL or recorded research issue. Therefore:

```text
THIRD_PARTY_SOURCE_COPIED = NO
THIRD_PARTY_NOTICE_CHANGE = NONE
LICENSE_ADMISSION = NONE
SBOM_CHANGE = NONE
```

Any later source import requires exact revision, license/NOTICE obligations, source review, tests/failure-mode review, security/maintenance/exit strategy, and canonical source admission.

## 14. Live verification boundary

Before this source check contributes to canonical planning acceptance, the acceptance workflow must re-read from GitHub:

```text
LIVE_CANONICAL_MAIN_SHA
LIVE_PR_BASE_SHA
LIVE_PR_HEAD_SHA
LIVE_11_FILE_DIFF
LIVE_FOUNDATION_STATE
LIVE_TRUSTED_BASE_ADMISSION_STATE
LIVE_REVIEW_THREADS_AND_REVIEW_STATE
```

The values must satisfy `acceptance.md`. This document cannot embed its own future commit SHA and must never pretend that a historical source-check input head is the live repaired acceptance head.

## 15. Final acquisition decision

```text
USE_EXISTING_ADMITTED_CONTRACT_SERIALIZATION = YES_PREFERRED
USE_RUST_STDLIB_FILESYSTEM_LOCKING = YES_PREFERRED_WITH_BOUNDED_TRY_LOCK_AND_PLATFORM_TESTS
FILE_BACKED_GENERATION_STORE = MINIMUM_PREFERRED
STORE_WIDE_CATALOG_RESERVATION = REQUIRED_BY_CORRECTNESS
NARROW_GIT_ADAPTER = LATER_CANDIDATE_REQUIRES_SEPARATE_EFFECT_AUTHORITY
FIRST_IMPLEMENTATION_SUCCESSOR = CONTRACTS_ONLY_PREFERRED
NEW_DATABASE = NO
NEW_ASYNC_RUNTIME = NO
NEW_AGENT_FRAMEWORK = NO
NEW_GRAPH_ENGINE = NO
NEW_MODEL_PROVIDER = NO
NEW_SOURCE_IMPORT = NO
NEW_DEPENDENCY_ADMISSION = NO
```

Source Acquisition is complete for the planning/no-import boundary. Before any S2 implementation authority is granted, unresolved task-specific machinery and current dependency/security state must be revalidated explicitly; this planning result never auto-admits them.
