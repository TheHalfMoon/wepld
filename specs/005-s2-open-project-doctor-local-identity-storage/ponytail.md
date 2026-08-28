# S2 Ponytail FULL

## Verdict

```text
PONYTAIL_MODE = FULL
PONYTAIL_STATUS = COMPLETE_FOR_REPAIRED_PLANNING_CANDIDATE_PENDING_FRESH_EXACT_HEAD_REVIEW
NEW_DEPENDENCY_REQUIRED_BY_PLAN = NO
SOURCE_IMPORT_REQUIRED_BY_PLAN = NO
DATABASE_REQUIRED_BY_PLAN = NO
MODEL_REQUIRED_BY_PLAN = NO
NETWORK_REQUIRED_BY_PLAN = NO
WHOLE_REPOSITORY_GRAPH_REQUIRED = NO
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

Ponytail asks whether each proposed mechanism needs to exist now, already exists in admitted/native machinery, can be smaller, or belongs to a later slice. The independent planning review invalidated a few mechanisms as **too small to be correct**; the repair adds only the minimum machinery needed to close those concrete races/crash/privacy/bounds gaps.

## 1. Project identity

### Canonical path as identity

**Reject.** Too weak and unstable across moves, symlinks, mounts, worktrees, Windows path forms, and copies.

### Remote URL as identity

**Reject.** Mutable, optional, duplicate, secret-bearing, and not local authority.

### Current Git HEAD as identity

**Reject.** Normal development changes it; different clones/worktrees can share it.

### Broad tree fingerprint

**Reject for S2.** Whole-repository traversal, false certainty, and overlap with later Fehrest/content machinery.

### Selected minimum

WePLD local project identity + layered locator/repository topology evidence + conservative reassociation.

## 2. First-open concurrency — per-project lock alone

### Candidate: choose ID, then lock `<project-id>/lock`

**Reject after independent review.** This cannot serialize first-open identity selection because competing processes can choose different project IDs before either project-specific lock exists.

### Candidate: global database/transaction engine

**Reject initial.** Solves more than S2 needs and adds dependency/schema/query/recovery surface.

### Selected minimum

A small versioned **store-wide catalog reservation** under one OS catalog lock:

- revalidate matching facts while locked;
- reuse existing/reserved binding;
- otherwise commit one opaque project ID with `reserved` state;
- complete first project generation and transition to `initialized`;
- retry after crash reuses/revalidates the reservation;
- fixed lock order catalog → project.

This is necessary coordination, not a global authority database.

## 3. Project-store atomicity — mutable current files

### Candidate: independently replace `identity.json`, `index.json`, and evidence files

**Reject after independent review.** A crash or concurrent reader can observe a valid-looking mixture of generations.

### Candidate: SQLite/KV immediately

**Reject initial.** Still overbuild unless platform evidence proves the corrected file protocol insufficient.

### Selected minimum

Immutable project generations + manifest + one small atomic `CURRENT` selector:

- build/validate a complete new generation off to the side;
- commit only by replacing `CURRENT`;
- readers select one immutable generation once;
- orphan/incomplete generations are never current;
- cleanup is not automatic authority.

This is the smallest explicit whole-state commit boundary that preserves the file-backed design.

## 4. Git topology machinery

### Hand-reimplement broad Git semantics

**Reject as default.** Worktrees, gitfiles, common-dir, submodules, and protected trust are subtle.

### Arbitrary Git invocation

**Reject.** Broad process authority is unnecessary.

### Selected candidate

A narrowly allowlisted official Git read-only topology adapter only if separately authorized later; otherwise a smaller filesystem-only subset with explicit unavailable facts.

The preferred first S2 successor grants **no Git process authority**.

## 5. Serialization

### New serialization framework

**Reject.** `wepld-contracts` already has admitted serde/serde_json.

### Duplicate handwritten JSON parser

**Reject.** Unnecessary security/compatibility surface.

### Selected minimum

WePLD-owned versioned contracts and bounded serialization helpers in the existing admitted contract crate.

## 6. File locking

Rust 1.97.1 standard library already provides file lock/try-lock primitives.

### Candidate: blocking `File::lock`

**Reject for ordinary S2 command acquisition.** It may wait indefinitely and convert another process into an unbounded availability failure.

### Candidate: PID/stale-lock file protocol

**Reject.** File existence/PID text is not reliable ownership and creates takeover races.

### Selected minimum

Qualified OS lock handles with non-blocking `try_lock` polling, cancellation, and frozen planning defaults:

```text
deadline = 2000 ms
poll = 25 ms
catalog busy = identity_catalog_busy
project busy = store_busy
```

Tune only through later evidence-backed contract change; never silently fall back to indefinite waiting.

## 7. Hashing/content identity

### Add a new hashing crate now

**Reject for contracts tranche.** Planning research #212 found `sha2 0.10.9` already in the canonical lock graph, but transitive presence is not direct dependency admission.

### Selected planning choice

Algorithm-labelled SHA-256 evidence contract. If Core later needs direct `sha2`, admit the exact existing candidate/version/features under a focused dependency gate.

## 8. Opaque project IDs

### Timestamp/PID/path-derived IDs

**Reject.** Leak structure, may collide, and are unsafe fallbacks when randomness is unavailable.

### Add random-ID dependency to contracts now

**Reject.** Contract should own representation, not generator package.

### Selected planning choice

WePLD-owned opaque project-ID contract. Research #212 identifies UUID v4 via existing `uuid 1.24.1` as a later Core generation candidate; direct edge requires explicit admission.

## 9. Data-directory helper crate

**Reject initial assumption.** Platform semantics are small enough to qualify first. Research #214 records XDG/Windows/macOS targets and lossless path issues. Admit a helper only with concrete evidence.

## 10. Async runtime

**Reject.** Baseline S2 operations are bounded local request/response operations. Lock polling does not justify a general async runtime by itself.

## 11. Watcher/file monitoring

**Reject for S2 minimum.** Freshness can be explicit without continuous background workers.

## 12. Semantic parser/code graph

**Reject for S2.** Canonical roadmap places semantic Project Graph in S4.

## 13. Search/vector database/embeddings

**Reject.** Qdrant and related donors are useful S4+ oracles; no S2 requirement needs them.

## 14. LLM/model explanation

**Reject.** Doctor findings are deterministic and evidence-linked. A later model may explain facts but cannot invent them.

## 15. Agent framework/MCP/ACP/A2A

**Reject for S2.** Donor research #211 informs later Agent Host/memory/evaluation design only.

## 16. Terminal/process fabric

**Reject except separately governed narrow Git seam.** S3 owns general process execution.

## 17. Project task runner abstraction

**Reject for S2.** Detect descriptive indicators only. Running Cargo/npm/pnpm/uv/mise/just/Make/Gradle/Maven/Go/Nx comes later.

## 18. Workspace descriptor discovery

### Candidate: “such as” examples / broad ecosystem globs

**Reject after independent review.** Open-ended discovery cannot prove bounded work and is easy to amplify.

### Candidate: recursively discover every workspace/member manifest

**Reject.** Pulls graph/task discovery forward and makes cost repository-size dependent.

### Selected minimum

Exact root descriptor + presence-marker allowlists frozen in `clarify.md`/`plan.md`, with:

```text
MAX_ROOT_DESCRIPTOR_CANDIDATES = 32
MAX_PARSED_DESCRIPTOR_BYTES = 1_048_576
MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES = 4_194_304
MAX_STRUCTURED_NESTING_DEPTH = 64
ROOT_DISCOVERY_RECURSION = NONE
```

Presence-only lock markers are not parsed just for ecosystem ambiguity. Deeper member parsing is capability-triggered later.

## 19. Doctor output construction

### Candidate: interpolate raw observed values into finding text

**Reject after independent review.** Escaping makes terminal rendering safer but does not stop token/credential disclosure.

### Candidate: add a generic secret-scanner dependency now

**Reject initial.** The S2 output contract can be safer and smaller by preventing unsafe values from entering trusted prose at all.

### Selected minimum

WePLD-owned finding templates + closed safe parameter types + opaque evidence references + shared TTY/JSON semantic redaction. Presentation escaping is an additional layer, not the secret policy.

## 20. Whole-repository traversal

**Reject.** `open` and baseline Doctor remain root/topology bounded. S4 performs semantic graph work later.

## 21. Automatic remediation

**Reject.** Doctor recommendations are evidence/advice; execution needs later authority.

## 22. Git trust overrides

**Reject.** WePLD does not make an untrusted repository trusted by changing `safe.directory` or related protected settings.

## 23. Raw environment capture

**Reject.** High privacy/secret risk and unnecessary for S2. Any later environment fact is individually allowlisted.

## 24. Remote/cloud project identity

**Reject for S2.** Local-first identity is sufficient.

## 25. Telemetry

**Reject.** No hidden telemetry. S2 acceptance does not depend on remote analytics.

## 26. Daemons/background services

**Reject.** Neither project-local nor global daemon is required for bounded S2 commands.

## 27. Continuous background indexing

**Reject.** S4/later concern.

## 28. Human-only CLI

**Reject.** Stable JSON/no-input must exist from the first command-plane slice.

## 29. JSONL streaming implementation now

**Reject initial.** Preserve schema/event seam; S2 commands are bounded.

## 30. AI fallback for unknown command

**Reject constitutionally.** Unknown commands remain errors.

## 31. Automatic package-manager selection

**Reject when ambiguous.** Doctor reports conflicts.

## 32. Git remote credential persistence/output

**Reject.** Sanitized safe metadata only when genuinely useful; raw userinfo/tokens never enter store or Doctor output.

## 33. Evidence store as authority engine

**Reject.** Store facts/evidence only. Nawat later owns effect-time authority.

## 34. Evidence store as final Fehrest database

**Reject.** S2 supplies foundations, not Project Brain index architecture.

## 35. Strong durability claims without platform proof

**Reject.** File/dir flush and replace semantics differ. Report the strongest measured level and explicit residual limitation.

## 36. Path equality using lowercasing

**Reject.** Case behavior differs by platform/filesystem and Unicode rules.

## 37. Canonicalization as sandbox

**Reject.** It resolves links at observation time but is not containment/authority.

## 38. Reviewer unavailability as exception

**Reject.** A requested, pending, rate-limited, or unavailable independent reviewer is `REVIEW_BLOCKED`, not a clean review.

## 39. One broad S2 implementation authorization

**Reject.** Too much authority at once and inconsistent with proven S1 staged admission.

### Selected staged strategy

1. **S2-AUTH-C:** contracts-only paths/tests, no Core effects/process/network/model/new dependencies by default.
2. **S2-AUTH-I/E:** bounded locator/identity/catalog/generation-store Core behavior after contracts are canonical.
3. **S2-AUTH-GIT:** optional exact Git adapter separately qualified.
4. **S2-AUTH-D/CLI:** Doctor + output projections after underlying facts exist.

## 40. Current dependency posture

```text
NEW_RUNTIME_DEPENDENCIES = NONE_PREFERRED
EXISTING_ADMITTED_SERIALIZATION = wepld-contracts -> serde + serde_json
RUST_STDLIB = PRIMARY_FILESYSTEM_LOCKING_PRIMITIVES
UUID_1_24_1 = LATER_CORE_CANDIDATE_NOT_ADMITTED_DIRECTLY
SHA2_0_10_9 = LATER_CORE_CANDIDATE_NOT_ADMITTED_DIRECTLY
GIT = SYSTEM_TOOL_ADAPTER_CANDIDATE_NOT_ADMITTED_FOR_EXECUTION
DATABASE = REJECT_INITIAL
```

Any exception must be justified by a concrete failing requirement and separately admitted.

## 41. Ponytail residual questions converted to tasks

- exact contract source path allowlist in S2-AUTH-C;
- per-platform data-root acquisition mechanism;
- lossless Unix/Windows path representation details;
- exact direct UUID/SHA-256 dependency/features if Core requires them;
- directory-entry/power-loss durability evidence;
- Git executable/environment qualification;
- identity reassociation thresholds;
- exact CLI numeric exit codes;
- platform evidence for lock semantics;
- evidence-backed tuning if 2000ms lock deadline proves inadequate.

These are explicit tasks in `tasks.md`; they are not permission to overbuild.

## 42. Final minimum-sufficient result

The repaired plan deliberately adds **only** the mechanisms whose absence created concrete correctness/security/availability defects:

```text
catalog reservation for first-open race
immutable generations + CURRENT for cross-file crash consistency
bounded try_lock for lock DoS
closed descriptor allowlist + limits for discovery amplification
safe output templates for secret leakage
complete acceptance/review gates for governance correctness
```

No database, async runtime, agent framework, vector engine, crawler, model, source import, or general process fabric is required to close those findings. That is the Ponytail justification for the repaired plan.
