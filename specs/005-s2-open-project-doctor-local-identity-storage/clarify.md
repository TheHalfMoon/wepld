# S2 Clarifications

## Status

```text
CLARIFICATION_STATUS = COMPLETE_FOR_PLANNING_CANDIDATE
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

## Q1 — Is S2 only for Git repositories?

**Decision:** No. S2 supports local non-Git projects. Git adds repository/worktree topology evidence; its absence does not make a local directory invalid as a WePLD project.

Reason: the WePLD command plane must not require a specific VCS, while Git-aware facts are still essential for the dominant workflow.

## Q2 — Is canonical filesystem path the project identity?

**Decision:** No.

We preserve input path, lexical absolute path, resolved path, worktree root, Git directory, Git common directory, and WePLD local identity as separate concepts. Filesystem canonicalization can change after moves/mounts and resolves links at one point in time; linked Git worktrees also prove that repository and worktree identity differ.

## Q3 — Do we invent a global immutable Git repository ID?

**Decision:** No.

Git does not provide a universal immutable repository identifier suitable for this claim. S2 owns a **local** project identity and binds it to versioned observed evidence. Reassociation after moves is conservative; ambiguous matches remain ambiguous.

## Q4 — How are project copies/clones handled?

**Decision:** A filesystem copy or independent clone is not silently treated as the same local project merely because content/remotes overlap. Strong explicit matching/reassociation evidence is required. Conflicting strong facts produce an identity conflict.

## Q5 — How are linked worktrees handled?

**Decision:** Repository relationship and worktree context are modeled separately. Worktrees sharing a common Git directory can be related without collapsing their per-worktree roots/status into one object.

## Q6 — How are submodules/superprojects handled?

**Decision:** S2 records available superproject/submodule context and makes root selection explicit. It does not silently jump from a submodule to its superproject or vice versa.

## Q7 — What happens with nested repositories?

**Decision:** The explicit input locator is resolved to the nearest applicable project/repository root according to deterministic discovery rules, and nesting is reported. Ambiguous root candidates fail into a diagnostic state when the rule cannot choose safely.

## Q8 — Does `wepld open` write `.wepld/` into the project?

**Decision:** No for S2. Default identity/evidence state is outside the repository in a WePLD-owned per-user data location. Project-local metadata may be considered later only through separate planning/authority.

## Q9 — Does S2 call `git`?

**Decision:** Planning permits an **adapter seam**, not execution authority.

Official Git porcelain commands are attractive behavior oracles for complex topology (`rev-parse`, `worktree list --porcelain -z`) and correctly respect Git's trust model. However, starting a process is an effect. A later implementation-authority policy must explicitly decide whether S2 may execute a tightly allowlisted system Git command set, with environment sanitization, no network, no hooks/tasks, bounded output, timeout/cancellation, and deterministic parsing. If that authority is not granted, implementation must use a smaller no-process discovery strategy and expose its limitations.

## Q10 — Should WePLD automatically fix `safe.directory`?

**Decision:** No. A trust refusal is diagnostic evidence. Doctor may explain the native Git remediation, but S2 does not weaken protected Git configuration.

## Q11 — Does Doctor run builds/tests/package managers to determine health?

**Decision:** No. S2 Doctor is inspection-only. It can detect descriptors/lockfiles/configuration and report likely readiness/ambiguity. Running `cargo`, `pnpm`, `uv`, `mise`, `just`, `make`, Gradle, Maven, Go tooling, Nx, or project scripts belongs to later execution-authorized slices.

## Q12 — Can Doctor install missing tools?

**Decision:** No. It reports missing/ambiguous toolchain facts and safe next actions only.

## Q13 — Are remote URLs part of identity?

**Decision:** Remote URLs are mutable advisory observations, never authority. If inspected, credentials/userinfo are redacted and raw secret-bearing URLs are not stored.

## Q14 — What local-store format is chosen now?

**Decision:** The planning preference is a WePLD-owned, versioned, file-backed evidence foundation using already-admitted serialization machinery in `wepld-contracts` and Rust standard-library filesystem/locking primitives where sufficient.

No SQLite/database/network dependency is admitted by this plan. If deterministic implementation proves the standard-library design insufficient for required atomicity/concurrency/recovery, that becomes an explicit dependency-acquisition decision rather than an invisible expansion.

## Q15 — Can `crates/core` directly add `serde_json` because it is already transitive?

**Decision:** Not automatically. Direct dependency declaration is dependency mutation/admission. Prefer WePLD-owned serialization helpers/contracts in the already-serde-enabled `wepld-contracts` crate unless a separately governed dependency step proves a direct core dependency is necessary.

## Q16 — What does freshness mean?

**Decision:** Freshness is per evidence kind. Each record names its observation basis and invalidation/age rule. A timestamp is metadata, not proof that the underlying filesystem/repository fact is still true.

## Q17 — Can S2 rely on mtime alone?

**Decision:** No as a universal truth primitive. Timestamps may be one input, but coarse clocks, clock changes, restored files, network filesystems, and metadata-preserving operations require conservative handling. Content claims use explicit digests when justified.

## Q18 — Does S2 build the Fehrest graph?

**Decision:** No. S2 supplies identity, provenance, freshness, and durable evidence primitives required by later Fehrest work. Semantic project graph/indexing stays S4.

## Q19 — Does S2 implement `wepld why`?

**Decision:** No. S2 ensures future `why` can cite deterministic project/doctor evidence. Full explanation/routing arrives later.

## Q20 — Are unknown CLI tokens AI prompts?

**Decision:** Never. Unknown commands remain errors with suggestions. Future model interaction is explicit (`wepld ask`, `wepld agent run`).

## Q21 — What machine modes are required?

**Decision:** S2 requires a stable JSON contract and noninteractive behavior. JSONL/event streaming is specified as a forward-compatible command-plane seam; S2 need not stream if the three S2 operations complete as bounded request/response commands.

## Q22 — How are exit codes finalized?

**Decision:** The spec defines semantic classes. Implementation must reconcile exact numeric values against existing CLI behavior/tests before freezing them. It may not silently reuse a code for a different semantic class.

## Q23 — What about TOCTOU?

**Decision:** S2 treats path/metadata observations as snapshots. It does not claim containment from them. Future effect-bearing operations must revalidate targets at effect time under Nawat/Terminal Fabric authority.

## Q24 — What if local evidence is corrupt?

**Decision:** Corrupt/partial/unsupported records are not loaded as current truth. Doctor reports store degradation and preserves recoverable valid records. Destructive repair requires separate authority; S2 planning does not authorize it.

## Q25 — Does canonical planning grant implementation?

**Decision:** No. Even after this package is reviewed and merged, implementation remains blocked until a separately governed successor policy grants exact implementation paths/effects/dependencies.
