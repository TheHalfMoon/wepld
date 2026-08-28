# S2 Implementation Plan — Planning Candidate Only

## Authority header

```text
CANONICAL_PLANNING_BASE = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
S2_PLANNING_AUTHORITY = EXACT_SPEC_KIT_PACKAGE_ONLY
S2_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S3_PLUS_AUTHORITY = NONE
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
- first-open reservation/result contracts;
- `EvidenceEnvelope`, generation-manifest, provenance, freshness, and status types;
- `DoctorReport`, `DoctorFinding`, `RemediationHint`;
- command response/error JSON contracts;
- canonical bounded serialization/deserialization helpers required by the evidence store.

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

The exact filenames must be fixed by later implementation-authority bootstraps; this planning package must not create them.

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

### Phase III — match or reserve local identity

Use ordered evidence strength:

1. exact existing identity-store binding to currently revalidated strong topology facts;
2. deterministic move/reassociation rule with no conflicting strong facts;
3. an existing compatible `reserved` first-open catalog binding;
4. otherwise reserve/create a new local identity under the store-wide catalog protocol or return ambiguity/conflict/busy.

Do not use remote URL, repository name, or current HEAD alone as identity authority.

#### First-open reservation protocol

A per-project lock cannot serialize identity selection before the project ID exists. New identity creation therefore follows this sequence:

1. acquire the **store-wide catalog lock** with the bounded lock protocol in §4.4;
2. re-observe/revalidate the strong locator/topology inputs used by the matching rule;
3. re-read the catalog under the lock;
4. if a compatible existing or `reserved` binding now exists, reuse it;
5. if conflicting strong evidence exists, return ambiguity/conflict without mutation;
6. otherwise generate one opaque project ID under separately qualified ID machinery and commit a versioned catalog reservation with `state=reserved` plus a digest/reference to the revalidated matching facts;
7. initialize the project's first complete generation under the project lock while preserving lock order `catalog -> project` if both are held;
8. commit the catalog entry to `state=initialized` only after the first project generation is current;
9. release locks in reverse order.

Crash recovery rule: a later opener that encounters `state=reserved` acquires the catalog lock, revalidates the stored matching facts, and either completes the same project ID or fails closed. It never allocates a second ID solely because initialization was interrupted.

Ordinary updates to an already-resolved project use the project lock only unless catalog state must change.

### Phase IV — persist evidence

Persist only allowlisted typed fields. Project state changes use the generation protocol below. Identity creation and evidence updates must be crash-aware, generation-consistent, bounded, and concurrency-safe.

## 4. Local evidence-store candidate

### 4.1 Per-user layout

Use a WePLD-owned per-user data root. Candidate conceptual layout:

```text
<wepld-data>/
  projects/
    catalog.lock
    catalog.json
    <safe-project-id>/
      lock
      CURRENT
      generations/
        <generation-id>/
          manifest.json
          identity.json
          index.json
          evidence/
            <record-id>.json
```

Names use WePLD-generated safe opaque identifiers, never raw project paths/remotes.

`catalog.json` is a small versioned first-open/reassociation coordination record. It is committed under the catalog lock using the same same-store temp/replace discipline appropriate to a single file. A catalog reservation is evidence/coordination, not repository authority.

Exact platform data-root paths are implementation decisions requiring qualification. No repository-local `.wepld` directory is created in S2.

### 4.2 Project generation commit boundary

A project update is never committed file-by-file into a mutable current directory. Instead:

1. acquire the bounded project lock;
2. read `CURRENT` once if present and validate the referenced current generation;
3. construct a new generation ID and all new identity/index/evidence/manifest bytes in memory or bounded staging;
4. create a new generation directory in the same project store;
5. write each immutable generation file completely, enforcing size/schema/digest/reference bounds;
6. synchronize files only to the durability level that the platform contract can honestly claim;
7. write/validate the generation manifest last within that generation;
8. ensure the complete generation is readable and self-consistent before it can be selected;
9. build a tiny versioned `CURRENT` record containing at least project ID, generation ID, and manifest digest/reference;
10. write `CURRENT` to a unique same-directory temporary file, validate it, synchronize as qualified, and atomically replace the live `CURRENT` within the same filesystem;
11. where directory-entry synchronization is qualified and available, perform it; otherwise record the residual limitation and do not overclaim power-loss durability;
12. release the lock.

**Commit point:** the successful qualified replacement of `CURRENT`. Before that point, the previous `CURRENT` generation remains current. After that point, readers select only the new generation.

Readers:

- read and parse bounded `CURRENT` once;
- open only the referenced generation;
- validate manifest/project/generation IDs and required digests/references;
- either complete against that immutable generation or retry explicitly if policy requires; they do not opportunistically reread `CURRENT` and mix old/new records.

Incomplete, malformed, or unreferenced generations are orphan/stale artifacts. Their existence does not make them current. Automatic destructive garbage collection is not part of S2 minimum.

### 4.3 Catalog commit/recovery

The catalog is protected by `catalog.lock`. Catalog writes use complete-new-bytes + same-directory temp + qualified synchronization + atomic replace. Catalog entries use explicit states such as `reserved|initialized`.

Recovery rules:

- malformed/unsupported catalog => explicit catalog-corrupt/capability failure; do not create a new identity as if the catalog were empty;
- `reserved` + matching revalidated facts => reuse and complete that project ID;
- `reserved` + conflicting facts => identity conflict/ambiguity;
- initialized binding + missing/corrupt project generation => store degradation, not automatic new identity;
- lock-file presence without an active OS lock => not ownership.

### 4.4 Bounded lock protocol

Planning freezes the initial command-operation lock contract:

```text
LOCK_ACQUIRE_DEADLINE_MS = 2000
LOCK_POLL_INTERVAL_MS = 25
CATALOG_BUSY_ERROR = identity_catalog_busy
PROJECT_STORE_BUSY_ERROR = store_busy
LOCK_ACQUISITION = nonblocking try_lock polling
CANCELLATION_CHECK = every poll iteration and before mutation
PID_LOCKFILE_TAKEOVER = PROHIBITED
LOCK_FILE_EXISTENCE_IS_OWNERSHIP = NO
```

Rules:

1. open the dedicated lock file/handle with the qualified platform mode;
2. call non-blocking `try_lock` rather than an unbounded blocking lock;
3. on `WouldBlock`, check cancellation/deadline, sleep/yield for the bounded poll interval, and retry;
4. deadline exhaustion returns the stable busy error and performs no partial mutation;
5. unexpected lock errors remain typed operation/platform failures;
6. OS/process/handle lock-release semantics are relied upon only where platform tests qualify them;
7. do not recursively reacquire the same logical store lock;
8. fixed lock order is catalog before project whenever both are needed.

The timing constants are part of the initial planning contract. A later change requires explicit contract/review evidence; implementation may not silently replace them with indefinite waits.

### 4.5 Corruption strategy

- never parse unbounded files;
- unsupported schema version => explicit unsupported state;
- malformed/truncated/digest/reference/generation mismatch => corrupt state;
- valid older records may remain readable only behind explicit versioned adapters;
- corrupted `CURRENT` never causes arbitrary generation selection;
- an orphan generation is not recovery authority merely because it parses;
- destructive cleanup is not automatic.

### 4.5.1 Authenticity boundary

S2's schema/version/digest/manifest/reference checks are **corruption and internal-coherence checks only**. The planned digests are unkeyed and the store has no authenticated trust anchor in S2. Therefore:

- the implementation must not label a structurally valid generation cryptographically authenticated, tamper-evident, or writer-authentic;
- an actor able to rewrite the complete local store, including records, manifests, references, `CURRENT`, catalog state, and corresponding unkeyed digests, can construct an internally self-consistent forged generation that passes structural validation;
- contradictions against stronger freshly observed live facts may still surface, but absence of contradiction is not authenticity proof;
- evidence remains non-authoritative for effects regardless of structural validity;
- adding a keyed MAC, signature, OS-protected trust anchor, or other authenticated store mechanism is a separate future security/design/authority decision, not an implicit S2 requirement.

This limitation is intentional for the minimum S2 file-backed foundation and must be surfaced in threat-model, contract, test, and acceptance evidence rather than hidden behind the word “integrity.”

### 4.6 Durability claim levels

The implementation reports the strongest measured guarantee, conceptually:

```text
FILE_CONTENT_SYNCED
RUNTIME_NAMESPACE_REPLACE_COMMITTED
DIRECTORY_ENTRY_SYNC = PROVEN | UNAVAILABLE | NOT_QUALIFIED
POWER_LOSS_DURABILITY = NOT_CLAIMED_UNLESS_PLATFORM_EVIDENCE_PROVES_IT
```

Exact enum names are frozen in the later contract implementation, but weaker platform semantics must remain visible rather than normalized into a false universal PASS.

## 5. Project Doctor plan

Doctor is rule-based and deterministic in S2.

Initial rule families:

```text
D-ID-*      identity/reservation/reassociation/conflict
D-GIT-*     repository/worktree/trust/dirty-conflict seam
D-WS-*      workspace/root/member descriptors
D-TC-*      toolchain descriptor/version-hint facts
D-LOCK-*    lockfile presence/consistency/ambiguity
D-PM-*      package-manager ambiguity
D-EV-*      evidence store/generation/catalog corruption
D-FRESH-*   stale/unavailable evidence
D-SEC-*     security-sensitive configuration observations
```

Every rule returns safe evidence references and non-executable remediation semantics.

### 5.1 Secret-safe finding projection

Doctor findings do not construct trusted prose by concatenating repository-controlled values. The contract uses:

- stable `finding_code`;
- stable severity/category enums;
- WePLD-owned summary/explanation/remediation template IDs;
- opaque evidence reference IDs;
- allowlisted safe parameters such as enums, booleans, bounded counts, sanitized tool names, and explicitly escaped path-display values when necessary;
- closed descriptive machine hints, never arbitrary shell text.

Prohibited as direct finding-text/JSON parameters:

- raw environment values;
- raw repository configuration values;
- remote URLs containing userinfo/query secrets;
- arbitrary command stdout/stderr;
- arbitrary manifest command strings;
- unsanitized terminal control sequences;
- secret/token values regardless of source.

TTY and JSON share one semantic redaction layer. JSON mode is not a raw-data escape hatch.

S2 explicitly does not prove that builds/tests pass. Later slices attach execution evidence.

## 6. Command-plane plan

### `wepld open <path>`

- resolve/observe project;
- establish, reserve, recover, or match local identity;
- persist S2 evidence only under later local-store authority;
- return human or JSON result;
- no project mutation;
- no network;
- no model.

### `wepld doctor [path|project]`

- evaluate bounded deterministic Doctor rules;
- return findings sorted by stable category/code;
- optionally refresh only those S2 observations explicitly allowed by the command contract;
- enforce secret-safe output projections;
- no remediation execution.

### `wepld status`

- show active/selected local project identity;
- show evidence-store catalog/current-generation health/freshness;
- report unavailable association explicitly.

### Machine interface

All three commands share versioned response envelopes. Human output is a projection; JSON is not generated by scraping terminal prose. Both projections consume the same redacted semantic fields.

## 7. External-process decision gate

S2 topology accuracy benefits from official Git behavior, but Git invocation is an effect and may parse repository configuration. Therefore implementation must split into one of two qualified routes:

### Route A — narrow Git adapter (deferred from the first contracts tranche; preferred later if authorized)

Exact command family candidate:

```text
<qualified-git> --no-pager --no-optional-locks -C <observed-locator> rev-parse <one allowlisted topology query>
<qualified-git> --no-pager --no-optional-locks -C <observed-locator> worktree list --porcelain -z
```

Allowlisted topology queries are limited to the official facts needed for:

```text
--show-toplevel
--absolute-git-dir
--git-common-dir
--is-bare-repository
--is-inside-work-tree
--show-superproject-working-tree
```

Before admission define and prove:

- executable resolution/trust rule;
- resolved absolute executable invocation rather than per-call PATH re-resolution;
- rejection of project-local spoofed executable candidates;
- explicit environment contract that scrubs repository-redirection/runtime-config `GIT_*` injection while preserving native protected trust evaluation;
- current directory/`-C` semantics;
- `--no-optional-locks`;
- stdin closed/null;
- shell false;
- pager/prompt disabled;
- hard timeout/cancellation;
- max stdout/stderr bytes;
- UTF-8/OS-string handling;
- exit-code mapping including `safe.directory` refusal;
- no network;
- no hooks/scripts;
- parser fuzz/negative tests.

Git process authority is **not** part of the preferred first S2 contracts-only successor.

### Route B — no-process filesystem discovery

If process authority is denied, implement only facts safely obtainable from filesystem/Gitfile structure and mark unavailable facts explicitly. Do not reimplement broad Git behavior merely to avoid a narrow, auditable adapter.

A later authority bootstrap chooses the permitted route; this plan does not self-authorize either implementation.

## 8. Workspace/tool discovery plan

Baseline Doctor inspects only **root-level exact names**. No recursive globbing or open-ended “such as” discovery is permitted.

### 8.1 Parsed descriptor allowlist

```text
Cargo.toml
package.json
pnpm-workspace.yaml
pyproject.toml
mise.toml
.mise.toml
justfile
Justfile
Makefile
settings.gradle
settings.gradle.kts
build.gradle
build.gradle.kts
pom.xml
go.mod
go.work
nx.json
workspace.json
```

### 8.2 Presence-only lock/package-manager marker allowlist

```text
Cargo.lock
package-lock.json
npm-shrinkwrap.json
pnpm-lock.yaml
yarn.lock
bun.lock
bun.lockb
uv.lock
poetry.lock
go.sum
```

Presence-only markers may be stat'ed and reported by name/size/safe metadata but are not parsed merely to identify package-manager ambiguity in baseline S2.

### 8.3 Hard discovery/parse limits

```text
MAX_ROOT_DESCRIPTOR_CANDIDATES = 32
MAX_PARSED_DESCRIPTOR_BYTES = 1_048_576
MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES = 4_194_304
MAX_STRUCTURED_NESTING_DEPTH = 64
ROOT_DISCOVERY_RECURSION = NONE
```

Rules:

1. candidate name matching is exact according to platform path semantics; no wildcard expansion;
2. enforce per-file size before reading full parsed content;
3. track aggregate parsed bytes before every allocation/read;
4. parsers enforce structured nesting depth where the format supports nesting;
5. invalid encoding/oversize/depth/candidate-count cases become bounded findings/unavailable states;
6. command strings inside descriptors remain opaque data and are never evaluated/executed;
7. workspace member expansion is not baseline S2 unless a later exact capability contract freezes separate bounds.

This is descriptive discovery. It does not execute tools or construct the semantic graph.

## 9. Deterministic qualification matrix

Required test classes before S2 implementation acceptance:

### Unit/contract

- identity evidence strength ordering;
- first-open reservation state transitions;
- ambiguity/conflict behavior;
- schema round trips;
- generation/current-pointer contracts;
- canonical JSON ordering/contract snapshots where required;
- finding ordering/codes;
- freshness state transitions;
- output redaction/template parameter validation;
- authenticity-status semantics prove unkeyed structural validation is never represented as writer authentication.

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

### Identity concurrency

- two concurrent first opens of the same unseen project;
- concurrent first opens with conflicting strong facts;
- crash after durable reservation before project initialization;
- retry completes/reuses the same reserved project ID;
- catalog corruption never becomes “empty catalog” identity creation;
- fixed catalog-before-project lock order.

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
- malicious `GIT_CONFIG_*`/repository-redirection environment;
- malicious hooks prove non-execution;
- malformed/bounded command output;
- timeout;
- spoofed/unqualified executable path negative case;
- project tree/index unchanged;
- no required network effect.

### Store durability and consistency

- concurrent writer contention;
- bounded catalog/project lock deadline;
- cancellation during lock polling;
- process crash releases qualified OS lock;
- simulated crash after every generation file write;
- crash before/after manifest completion;
- crash before/after `CURRENT` temp sync/replace;
- old generation remains current before commit point;
- complete new generation becomes current after commit point;
- no mixed-generation read;
- truncated record;
- unsupported version;
- digest mismatch;
- stale temp/orphan generation files;
- permission loss;
- store move/partial deletion;
- catalog `reserved` recovery;
- recovery never fabricates PASS;
- writer-level tampering fixture demonstrates that an internally self-consistent forged unkeyed store is not claimed authenticated/tamper-evident.

### Workspace/tool descriptors

- exact allowlisted names accepted;
- unknown lookalike names ignored/not treated as recognized descriptors;
- >32 candidates bounded;
- parsed file >1 MiB bounded before full parse;
- aggregate parsed bytes >4 MiB bounded;
- nesting depth >64 bounded;
- presence-only lockfiles are not parsed;
- no recursive member/repository scan occurs in baseline Doctor;
- descriptor command strings are never executed.

### Output privacy

- credential-bearing HTTPS remote;
- token-like config values;
- environment secret fixture;
- arbitrary manifest command text;
- ANSI/control characters;
- TTY projection contains no raw secret;
- JSON projection contains no raw secret;
- logs/diagnostics use typed redacted fields.

### CLI

- TTY vs non-TTY;
- JSON snapshots;
- `--no-input` never prompts;
- exit-code/error-class mapping;
- busy errors are machine distinguishable;
- unknown command errors/suggestions;
- no accidental AI-prompt interpretation.

### Platform

- Windows required;
- Linux required;
- macOS when available or limitation retained explicitly.

## 10. Performance budgets to qualify

Planning targets, not PASS claims:

- opening a project must not traverse the entire repository;
- baseline `status` reads a bounded number of local catalog/current-generation records;
- Doctor root discovery is fixed to the exact allowlist and hard candidate/byte/depth bounds in §8;
- evidence parser has explicit per-record/aggregate byte bounds frozen before code;
- lock acquisition has a 2-second planning deadline rather than indefinite blocking;
- external Git adapter, if later admitted, has hard timeout/output bounds.

Benchmarks must publish fixture size/topology and p50/p95 or deterministic ceiling evidence before acceptance.

## 11. Implementation-authority bootstrap strategy

After this planning package becomes canonical, use staged authority rather than one broad S2 grant.

### Stage S2-AUTH-C — contracts-only preferred first successor

Preferred first successor scope:

- only exact `crates/contracts` S2 contract modules/exports/tests needed for S2-C001..S2-C009, including the negative secret-safety contract test;
- existing admitted contract serialization graph only;
- no `crates/core` filesystem behavior;
- no external process;
- no network;
- no model/provider;
- no source import;
- no new dependency unless a separate focused acquisition/admission gate proves it necessary.

The exact paths are frozen by that successor after canonical planning is re-read. This plan intentionally does not self-create or self-authorize them.

### Stage S2-AUTH-I/E — locator/identity/evidence core

Only after contracts are canonical and separately authorized:

- bounded local filesystem observations;
- per-platform data-root contract;
- catalog reservation;
- project generation store;
- qualified locking/durability;
- task-specific opaque ID/digest dependency decisions if required.

### Stage S2-AUTH-GIT — optional Git adapter

Separate from contracts and basic local-store authority. Admit only the exact executable/environment/argv/time/output semantics in §7 after its own source/security review.

### Stage S2-AUTH-D/CLI — Doctor + command projections

After the underlying contracts/observations exist, authorize deterministic Doctor and CLI projection paths with no general process/network/model authority.

Every successor remains append-only, preserves frozen predecessors, and must state:

```text
S2_IMPLEMENTATION_AUTHORITY = <exact bounded paths/effects only>
DEPENDENCY_ADMISSION = <none unless separately qualified>
SOURCE_ADMISSION = <none unless separately qualified>
EXTERNAL_PROCESS_AUTHORITY = <none unless exact later Git adapter contract>
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S3_PLUS_AUTHORITY = NONE
```

The canonical plan cannot self-activate a successor.

## 12. Source/research decisions already captured

Non-authoritative GitHub research evidence created during planning review:

```text
#211 donor capability map: memory/agent/search/evaluation donors
#212 existing-graph UUID/SHA-256 prequalification research
#213 bounded read-only Git topology adapter research
#214 local data-root/lossless path/file-store durability research
```

These issues inform future task-specific acquisition only. They grant no source/dependency/process/runtime authority. Material decisions incorporated here are:

- donor frameworks do not justify S2 runtime dependencies;
- contracts-first remains the minimum successor;
- `uuid 1.24.1` and `sha2 0.10.9` existing transitively are candidates only, not admitted direct edges;
- Git adapter remains later and special-purpose;
- file-backed generations remain minimum sufficient until platform evidence disproves them;
- OS-path representation/data-root/durability must be frozen before corresponding Core code.

## 13. Delivery sequence

1. reconcile all planning-review findings in the eleven-file Spec Kit package;
2. rerun exact-head Foundation/trusted-base planning admission on the repaired head;
3. record fresh exact-head egress preflight and complete independent rereview;
4. reconcile any new valid material finding and repeat qualification if the head changes;
5. perform final main/base/head/diff/thread/check race verification;
6. mark the planning PR Ready only with exact-head evidence;
7. reread Ready-triggered trusted-base admission and require genuine PASS;
8. guarded merge with expected-head protection;
9. prove post-merge canonical planning activation/Foundation on exact `main`;
10. re-read canonical planning and design/qualify the contracts-only S2-AUTH-C successor;
11. implement/qualify S2 contracts first;
12. separately authorize and implement bounded locator/identity/generation-store foundations;
13. separately decide/admit the optional Git adapter;
14. implement Doctor rules and secret-safe outputs;
15. implement CLI projections;
16. adversarial/platform/performance qualification;
17. independent correctness/security review and bounded repair;
18. S2 acceptance + Build Learning only with exact evidence.