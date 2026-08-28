# S2 Ponytail FULL

## Verdict

```text
PONYTAIL_MODE = FULL
PONYTAIL_STATUS = COMPLETE_FOR_PLANNING_CANDIDATE
NEW_DEPENDENCY_REQUIRED_BY_PLAN = NO
SOURCE_IMPORT_REQUIRED_BY_PLAN = NO
DATABASE_REQUIRED_BY_PLAN = NO
MODEL_REQUIRED_BY_PLAN = NO
NETWORK_REQUIRED_BY_PLAN = NO
WHOLE_REPOSITORY_GRAPH_REQUIRED = NO
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

Ponytail asks whether each proposed mechanism needs to exist now, already exists in admitted/native machinery, can be smaller, or belongs to a later slice.

## 1. Project identity

### Candidate: canonical path as identity

**Reject.** Too weak and unstable across moves, symlinks, mounts, worktrees, Windows path forms, and copies.

### Candidate: remote URL as identity

**Reject.** Mutable, optional, duplicate, secret-bearing, and not local authority.

### Candidate: current Git HEAD as identity

**Reject.** Normal development changes it; different clones/worktrees can share it.

### Candidate: custom global repository fingerprint with broad tree hashing

**Reject for S2.** Expensive, whole-repository traversal, false certainty, and overlaps later Fehrest/content machinery.

### Selected minimum

WePLD local project identity + layered locator/repository topology evidence + conservative reassociation.

## 2. Git topology machinery

### Candidate: hand-reimplement Git repository/worktree semantics

**Reject as default.** Git worktrees, gitfiles, alternates/common-dir, submodules, and protected trust behavior are mature and subtle.

### Candidate: arbitrary Git invocation

**Reject.** Process effects and broad command surface are unnecessary.

### Selected candidate

A narrowly allowlisted official Git read-only topology adapter **only if** separately authorized; otherwise a smaller filesystem-only subset with explicit unavailable facts.

## 3. Local storage

### Candidate: SQLite immediately

**Reject initial.** S2 needs a small identity/evidence foundation, not a query engine. A database introduces dependency/native-binary/migration/recovery surface before evidence proves need.

### Candidate: embedded KV database

**Reject initial.** Same overbuild problem.

### Candidate: repository-local `.wepld` database

**Reject initial.** Mutates user projects, creates ignore/commit/privacy ambiguity, and entangles project ownership with local WePLD state.

### Selected minimum

Versioned file-backed per-user local store using admitted serialization contracts and qualified Rust standard-library filesystem/locking primitives. Reopen dependency admission only if cross-platform durability/concurrency evidence disproves sufficiency.

## 4. Serialization

### Candidate: new serialization framework

**Reject.** `wepld-contracts` already has admitted `serde=1.0.229` and `serde_json=1.0.151`.

### Candidate: duplicate handwritten JSON parser

**Reject.** Unnecessary security/compatibility surface.

### Selected minimum

WePLD-owned versioned contracts and bounded serialization helpers in the existing admitted contract crate.

## 5. File locking

Rust 1.97.1 standard library already includes file lock/try-lock primitives. Prefer them if deterministic cross-platform tests support the claim. Do not add a locking crate without evidence of a concrete missing requirement.

## 6. Hashing/content identity

### Candidate: add a new hashing crate now

**Defer.** First inspect whether an already-admitted digest implementation exists in the trusted graph or whether the implementation-authority slice needs a minimal standard/system strategy. The planning model requires an algorithm-labelled digest but does not self-admit a package.

If cryptographic content addressing becomes mandatory and no admitted implementation exists, run a focused source/dependency acquisition gate rather than weakening the requirement.

## 7. Data-directory helper crate

### Candidate: add `dirs`/`directories` immediately

**Reject initial assumption.** Platform data-directory rules are small enough to evaluate against standard/platform APIs first. If the qualified implementation becomes error-prone or incomplete, dependency acquisition can be reopened with concrete evidence.

## 8. Async runtime

**Reject.** Baseline S2 operations are bounded local request/response operations. No Tokio/general async runtime is needed merely to open a project, inspect descriptors, or update a small local store.

## 9. Watcher/file monitoring

**Reject for S2 minimum.** Freshness can be represented/invalidation-aware without continuous watchers. File watching can be added only when a later slice proves it is necessary for user-visible latency/accuracy.

## 10. Semantic parser/code graph

**Reject for S2.** Canonical roadmap places semantic Project Graph in S4.

## 11. Search/vector database/embeddings

**Reject.** No S2 requirement needs them.

## 12. LLM/model explanation

**Reject.** Doctor findings are deterministic and evidence-linked. A later model may explain facts but cannot invent them.

## 13. Agent framework/MCP/ACP/A2A

**Reject for S2.** Agent Host interoperability belongs later. S2 contracts should be machine-readable but do not need an agent protocol stack.

## 14. Terminal/process fabric

**Reject except the narrowly qualified Git adapter seam.** S3 owns general trusted process execution. The Git seam, if granted, must remain special-purpose and incapable of becoming a hidden general runner.

## 15. Project task runner abstraction

**Reject for S2.** WePLD should eventually orchestrate Cargo/npm/pnpm/uv/mise/just/Taskfile/Make/Gradle/Maven/Go/Nx, but S2 only detects descriptive indicators. Running tasks comes later.

## 16. Workspace parser depth

### Candidate: fully parse every ecosystem

**Reject.** Minimum Doctor discovery only.

### Selected minimum

Bounded descriptors and unambiguous metadata needed to identify workspace/tool candidates. Exact deeper parsers are capability-triggered later.

## 17. Whole-repository traversal

**Reject.** `open` and baseline Doctor must stay bounded and fast. S4 performs semantic graph work later.

## 18. Automatic remediation

**Reject.** Doctor recommendations are evidence/advice; execution needs later authority.

## 19. Git trust overrides

**Reject.** WePLD does not make an untrusted repository trusted by changing `safe.directory` or related protected settings.

## 20. Raw environment capture

**Reject.** High privacy/secret risk and not needed for S2. Use explicit allowlisted environment facts only if a later diagnostic requirement proves need.

## 21. Remote/cloud project identity

**Reject for S2.** Local-first identity is sufficient. Remote services may become adapters later but never replace local authority by default.

## 22. Telemetry

**Reject.** No hidden telemetry. S2 acceptance does not depend on remote analytics.

## 23. Project-local daemon

**Reject.** No need for a daemon/service to satisfy bounded S2 commands.

## 24. Global daemon

**Reject.** Same reason. Revisit only if later event/terminal/agent orchestration requires it.

## 25. Continuous background indexing

**Reject.** S4/later concern.

## 26. Identity UUID/random package

A local project ID needs opaque uniqueness, but a new random-ID dependency is not automatically necessary. Evaluate existing admitted/system capabilities under the implementation gate. If collision-safe opaque IDs cannot be produced within admitted machinery, run a focused dependency acquisition decision. Never derive store path directly from secret-bearing project input.

## 27. Human-only CLI

**Reject.** Stable JSON/no-input must exist from the first command-plane slice to avoid later compatibility debt.

## 28. JSONL streaming implementation now

**Reject initial.** Preserve schema/event seam; S2 commands are bounded. Implement streaming only when an S2 requirement actually streams progress/results.

## 29. AI fallback for unknown command

**Reject constitutionally.** Unknown commands remain errors.

## 30. Automatic package-manager selection

**Reject when ambiguous.** Doctor reports conflicts. A future task router may select based on explicit qualified project authority.

## 31. Git remote credential persistence

**Reject.** Sanitized remote metadata only when genuinely useful.

## 32. Evidence store as authority engine

**Reject.** Store facts/evidence only. Nawat later owns effect-time authority.

## 33. Evidence store as final Fehrest database

**Reject.** S2 supplies foundations, not the final Project Brain schema/index.

## 34. Strong durability claims without platform proof

**Reject.** File/dir flush and replace semantics differ. Implement the strongest proven portable contract and retain residual limitations explicitly.

## 35. Path equality using lowercasing

**Reject.** Case behavior differs by platform/filesystem and Unicode rules. Use qualified platform/filesystem identity observations; never generic lowercase normalization as identity truth.

## 36. Canonicalization as sandbox

**Reject.** It resolves links at observation time but is not containment/authority.

## 37. S2 dependency decision

Current preferred implementation dependency posture:

```text
NEW_RUNTIME_DEPENDENCIES = NONE_PREFERRED
EXISTING_ADMITTED_SERIALIZATION = wepld-contracts -> serde + serde_json
RUST_STDLIB = PRIMARY_FILESYSTEM_LOCKING_PRIMITIVES
GIT = SYSTEM_TOOL_ADAPTER_CANDIDATE_NOT_ADMITTED_FOR_EXECUTION
```

Any exception must be justified by a concrete failing requirement and separately admitted.

## 38. Ponytail residual questions converted to tasks

- opaque ID generation mechanism;
- digest algorithm/implementation;
- per-platform data directory;
- directory flush durability;
- Git executable qualification;
- non-UTF8 path JSON representation;
- exact CLI exit codes.

These are not reasons to overbuild now. They are explicit pre-implementation decisions in `tasks.md`.
