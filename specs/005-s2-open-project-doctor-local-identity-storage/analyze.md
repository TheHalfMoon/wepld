# S2 Cross-Artifact Analysis

## Analysis result

```text
ANALYSIS_STATUS = COMPLETE_FOR_PLANNING_CANDIDATE
MATERIAL_INTERNAL_CONTRADICTIONS = 0
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

## 1. Constitution ↔ specification

The constitution requires local-first behavior, layered identity, no hidden repository mutation, evidence/authority separation, explicit CLI modes, and no later-slice pull-forward.

The specification maps those invariants to requirements:

- C2 → FR-002/FR-013 and SR-002;
- C3/C4 → FR-003/FR-005/FR-009/FR-010/FR-011;
- C5 → FR-006 and SR-001;
- C6 → FR-003/FR-004 and SR-004;
- C7 → FR-014..FR-017/FR-023;
- C8 → FR-018..FR-021;
- C9 → FR-025..FR-029;
- C10 → explicit out-of-scope and plan boundaries.

No specification requirement grants an effect forbidden by the constitution.

## 2. Specification ↔ clarifications

Resolved ambiguities are reflected consistently:

- non-Git support is explicit;
- canonical path is not identity;
- no global Git ID is invented;
- worktrees remain distinct contexts;
- local store remains outside the repo;
- Git execution is a separately governed adapter decision;
- Doctor does not execute builds/tests/installers;
- remote URLs are advisory and sanitized;
- S4 graph and full `why` remain later;
- unknown CLI tokens never become prompts.

## 3. Specification ↔ plan

The plan uses the minimum existing architecture:

- serializable contract types live in `wepld-contracts`, which already owns admitted serde/serde_json dependencies;
- core project/evidence logic remains Rust-first;
- no new database/runtime framework is assumed;
- Git is treated as a bounded external-process candidate, not an implicit implementation detail;
- S2 Doctor is deterministic/rule-based;
- CLI human output is a projection over stable contracts.

Potential implementation paths are intentionally provisional until a successor policy freezes their exact allowlist.

## 4. Source acquisition consistency

The Source Acquisition Check classifies current research sources as behavior oracles/reference inputs only. It admits no code, package, binary, or service. This is consistent with v21's `SOURCE_ADMISSION=NONE` and `DEPENDENCY_ADMISSION=NONE`.

The plan prefers existing admitted serde/serde_json through `wepld-contracts` plus Rust standard-library primitives. A future direct dependency addition remains a separate admission decision even if that package already exists transitively elsewhere.

## 5. Authority analysis

### Planning authority

Canonical v21 grants creation/review/canonicalization of exactly this eleven-file package.

### Implementation authority

None.

The package identifies a provisional v22 successor as the next expected authority transition after planning canonicalization. That statement is a required future gate, not self-authorization.

### Process authority

None during planning. The Git adapter is a candidate only.

### Network/provider authority

None.

## 6. Identity-model analysis

A single canonical path would fail on:

- project moves/renames;
- linked worktrees;
- symlink/junction resolution changes;
- Windows path representation/case behavior;
- mount changes;
- Git common-dir vs worktree-dir separation.

A remote URL would fail because remotes can change, duplicate, contain credentials, or be absent.

A current HEAD would fail because it changes with normal development and can be shared across clones.

Therefore the layered local identity + observed topology model is minimum sufficient.

## 7. Filesystem-security analysis

Rust filesystem APIs explicitly expose canonicalization and metadata as filesystem observations, and filesystem operations remain subject to TOCTOU. Windows canonicalization can produce extended-length path syntax. Consequently:

- preserve lexical and resolved forms;
- do not use string-prefix checks as containment proof;
- treat link/reparse facts explicitly;
- revalidate future effect targets at effect time;
- make all S2 path-based findings evidence, not grants.

## 8. Git-trust analysis

Git's `safe.directory` is protected configuration intended to prevent an untrusted repository from declaring itself trusted. Automatically modifying it from Doctor would invert the trust boundary. The plan therefore reports refusal and leaves remediation explicit/manual.

Git linked-worktree support also establishes that `worktree root`, `git dir`, and `git common dir` are distinct facts that must not be collapsed.

## 9. Doctor-scope analysis

A Doctor that executes builds/tests would require S3-style process ownership and authority too early. A Doctor that only checks whether binaries exist would be too weak. S2 therefore chooses a middle layer:

- inspect deterministic descriptors/topology/evidence;
- identify conflicts/ambiguity/readiness gaps;
- expose remediation hints;
- defer actual execution evidence to later slices.

This preserves product value without pulling runtime authority backward.

## 10. Evidence-store sufficiency analysis

S2 needs durability/freshness/provenance before Fehrest, but not a general database. A small versioned file-backed store is sufficient to prove:

- project local identity persistence;
- typed evidence envelopes;
- corruption detection;
- concurrency protocol;
- freshness/status semantics.

If implementation evidence disproves the standard-library approach on required platforms, dependency admission can be reopened explicitly. Premature SQLite/database adoption is rejected by Ponytail.

## 11. CLI product analysis

S2 preserves the long-term command-plane direction without implementing later commands. The essential architectural choice is that human, agent/CI, and Desktop surfaces consume the same project/core contracts.

Stable JSON and `--no-input` matter now because retrofitting machine semantics after a human-only CLI would create compatibility debt. JSONL streaming is only a seam because S2 operations are bounded request/response commands.

## 12. Residual planning risks

1. exact platform data-directory rules must be frozen before implementation;
2. Git adapter executable qualification/environment contract needs dedicated threat review;
3. local-store directory flush/replace guarantees differ by platform and must not be overstated;
4. identity reassociation thresholds require adversarial fixtures to avoid false merges;
5. non-UTF8 Windows/Unix path representation in JSON needs a deterministic encoding decision;
6. exact CLI exit-code values must reconcile existing S1 CLI behavior before freeze;
7. macOS-specific qualification may be unavailable and must remain an explicit coverage limitation if so.

These are converted into tasks/acceptance gates rather than hidden assumptions.

## Conclusion

The package is internally consistent, bounded to S2, and does not leak S3/S4/agent/runtime authority. It is ready for deterministic planning qualification and independent review, not implementation.
