# S2 Threat Model — Open Project + Project Doctor + Local Identity/Storage

## 1. Scope

S2 introduces a new trust boundary: WePLD begins reading local user-selected projects and persisting local identity/evidence about them. The target repository is untrusted input. The local evidence store is trusted only to the extent that its catalog, current-generation reference, generation manifest, records, freshness, and provenance can be structurally verified. S2 does not authenticate the store against an actor with writer-level access to the complete store.

This threat model is planning evidence. It grants no implementation/effect authority.

## 2. Assets

- correctness of selected project identity;
- one-identity convergence for concurrent first opens;
- separation of repository vs worktree identity;
- user filesystem privacy;
- integrity and generation consistency of local evidence records;
- freshness/provenance of observations;
- WePLD command-plane output integrity and secret safety;
- Git/platform trust controls;
- local store availability and recoverability;
- bounded command latency under contention/hostile descriptors;
- absence of unintended project mutation;
- future authority separation between facts and effects.

## 3. Trust boundaries

### TB-1 — CLI/user locator → trusted core

Input path may be malformed, ambiguous, raceable, or point to hostile filesystem objects.

### TB-2 — target project filesystem → trusted core

All repository files/configuration/symlinks/gitfiles/workspace descriptors are untrusted data.

### TB-3 — system Git executable → trusted core

If later admitted, executable identity/path plus stdout/stderr/exit status are external-process inputs. Repository-controlled Git configuration and ambient `GIT_*` state may influence behavior.

### TB-4 — trusted core → identity catalog

First-open reservation and reassociation coordination must remain single-writer, bounded, crash-recoverable, and conflict-aware.

### TB-5 — trusted core → project generation store

Writes must survive concurrency/crash without creating valid-looking mixed generations.

### TB-6 — local catalog/store → trusted core

Store contents can be stale, tampered, truncated, downgraded, partially deleted, generation-mismatched, or replaced. Schema/version/digest/manifest/reference validation can prove bounded structural consistency and detect many corruption classes, but because S2 has no authenticated trust anchor it cannot prove writer authenticity when an attacker can replace the complete store and recompute unkeyed digests consistently.

### TB-7 — core contracts → human/machine/Desktop projections

A projection must not change semantic status, hide ambiguity, manufacture PASS, execute hints, or leak secret-bearing untrusted values.

## 4. Threats and mitigations

### T-001 — Workspace escape through symlink/junction/reparse point

**Attack:** A repository path redirects outside the expected tree.

**Mitigation:** preserve lexical/resolved forms; inspect link/reparse facts; never infer containment from string prefix; no S2 arbitrary write inside project; future effects revalidate target at effect time.

**Residual:** observation can race after inspection.

### T-002 — TOCTOU replacement

**Attack:** path target changes between check and use.

**Mitigation:** treat S2 facts as snapshots; revalidate strong locator/topology facts before identity catalog mutation; future effect slices use stronger effect-time revalidation.

### T-003 — Windows case/canonicalization confusion

**Attack:** case-only paths, drive aliases, extended-length paths, junctions, or normalization differences cause identity collision.

**Mitigation:** never generic-lowercase paths; maintain platform-qualified/lossless representations; collision checks use multiple strong facts; adversarial Windows tests.

### T-004 — Symlink loop / broken link denial

**Attack:** recursive resolution loops or broken targets cause hangs/fallback guesses.

**Mitigation:** bounded standard APIs, no manual unbounded recursive following, explicit resolution errors, hard operation bounds.

### T-005 — Malicious `.git` assumptions

**Attack:** `.git` is a gitfile/linked worktree/hostile layout and a naïve parser escapes or misidentifies repository state.

**Mitigation:** never assume `.git` directory; prefer qualified official Git topology adapter if authorized; otherwise deliberately limited parser with strict bounds and unavailable states.

### T-006 — `safe.directory` bypass

**Attack:** hostile repository causes WePLD to add itself to trusted Git directories.

**Mitigation:** trust refusal becomes Doctor finding; S2 never changes protected Git config; no wildcard auto-remediation.

### T-007 — Repository hook/script execution

**Attack:** opening/Doctor inadvertently executes hooks, package lifecycle scripts, task files, build scripts, editor configs, or generated binaries.

**Mitigation:** descriptor reads are data-only; no task/package-manager/build execution; any Git adapter exact-command contract must prove no project hooks/scripts are executed for S2 operations.

### T-008 — Spoofed Git executable

**Attack:** PATH resolves to a malicious `git` binary.

**Mitigation:** later adapter authority defines deterministic executable qualification/resolution, rejects project-local candidates, invokes resolved absolute path, and returns capability unavailable rather than arbitrary fallback execution.

### T-009 — Git environment/config/output abuse

**Attack:** ambient `GIT_CONFIG_*`, `GIT_DIR`, `GIT_WORK_TREE`, related variables, hostile output, NUL/newlines, huge fields, or invalid encoding alter topology or parser decisions.

**Mitigation:** scrub behavior-control `GIT_*` variables while preserving native protected trust evaluation; exact argv; NUL-delimited porcelain where applicable; max output/field/record counts; closed parser; timeout/fuzz/negative fixtures.

### T-010 — Hidden network through discovery

**Attack:** S2 command contacts remotes or package registries.

**Mitigation:** S2 network authority none; no fetch/pull/package-manager commands; network-negative evidence.

### T-011 — Remote URL credential leakage

**Attack:** `https://user:token@host/...` or equivalent is persisted, logged, or rendered.

**Mitigation:** remote URL is not required identity; raw secret-bearing URL never enters durable evidence or trusted Doctor prose; sanitize/allowlist before any safe projection.

### T-012 — Identity false merge

**Attack:** two different projects/clones/copies are assigned one local project ID.

**Mitigation:** evidence-strength hierarchy; contradictions block reassociation; remote/HEAD alone insufficient; ambiguity explicit.

### T-013 — Identity false split after move

**Attack:** same intended local project receives duplicate identities after benign rename/move.

**Mitigation:** deterministic conservative reassociation using strong stored/current evidence; later explicit user reconciliation seam. Prefer false split over unsafe false merge when uncertain.

### T-014 — Linked worktree collapse

**Attack:** worktrees sharing common Git data overwrite one another's current context.

**Mitigation:** model repository relationship separately from worktree context/root; worktree-specific binding where required.

### T-015 — Store path traversal

**Attack:** project name/path/remote injects traversal, separators, reserved names, or device paths into local store.

**Mitigation:** filenames derive only from WePLD-owned safe opaque IDs/encodings; raw project strings remain bounded payload/display observations.

### T-016 — Torn individual record write

**Attack:** crash leaves partial JSON accepted as complete.

**Mitigation:** build full bytes; same-store temp; qualified synchronization; schema/digest validation; temp/partial files never current.

### T-017 — Concurrent ordinary writer corruption

**Attack:** two WePLD processes interleave project updates.

**Mitigation:** bounded project OS lock, immutable generation construction, single `CURRENT` commit point; failure returns stable contention/error rather than silent last-writer mixing.

### T-018 — Stale lock denial

**Attack:** crash leaves lock artifact blocking forever.

**Mitigation:** active ownership comes from qualified OS file locks, not file existence or PID text. `try_lock` polling is bounded/cancellable; no homegrown stale-PID takeover.

### T-019 — Store tampering/downgrade

**Attack:** an old/modified record is injected to make Doctor green, or an actor with writer-level access rewrites records, manifests, references, `CURRENT`, catalog state, and corresponding unkeyed digests into one internally self-consistent forged store.

**Mitigation:** schema/version/digest/manifest/reference validation detects corruption, truncation, version/reference mismatch, and internal incoherence; explicit provenance/freshness and contradictions with stronger live facts can surface additional problems; evidence never authorizes effects. These checks are **not an authenticity mechanism**. S2 has no keyed MAC, signature, OS-protected trust anchor, or equivalent writer-authentication primitive, so a complete self-consistent rewrite by a store writer is outside the protection claim. The implementation must surface this limitation and must never report structural validation as cryptographic authentication or tamper evidence. Any authenticated store trust anchor is a separate future planning/security/authority decision.

**Residual:** a writer-level attacker can forge an internally coherent S2 store that passes the unkeyed structural checks when no stronger live contradiction is observed.

### T-020 — Oversized store record denial

**Attack:** huge local record exhausts memory.

**Mitigation:** hard per-file/per-record/aggregate size bounds before parse; bounded collection sizes.

### T-021 — Unsupported schema confusion

**Attack:** future/unknown fields/statuses are misread as PASS.

**Mitigation:** versioned envelope; closed authority/status semantics; unsupported versions explicit, never default complete/current.

### T-022 — Raw environment secret capture

**Attack:** Doctor snapshots tokens/keys from environment.

**Mitigation:** no raw environment dump; explicit allowlisted non-secret facts only where required; raw values forbidden from findings/output/logs.

### T-023 — Malicious workspace descriptor

**Attack:** package manifest contains pathological size/encoding/nesting or command strings intended for later execution.

**Mitigation:** exact root allowlist; no recursive baseline discovery; candidate count <=32; parsed file <=1 MiB; aggregate parsed bytes <=4 MiB; structured nesting <=64; command strings opaque/non-executable.

### T-024 — Package-manager ambiguity hidden

**Attack:** Doctor silently picks an attacker-controlled lockfile/tool configuration.

**Mitigation:** exact presence marker allowlist; deterministic precedence only where contract proves it; otherwise ambiguity finding.

### T-025 — Doctor terminal injection

**Attack:** project-controlled strings inject ANSI/control sequences or misleading formatting.

**Mitigation:** escape untrusted path/display strings; trusted finding prose is WePLD-owned template output, not arbitrary repository text.

### T-026 — JSON consumer authority confusion

**Attack:** downstream agent interprets health as permission to run commands.

**Mitigation:** schemas never include effect grants; fact/health and authority use distinct types/contracts.

### T-027 — Unknown command becomes AI execution

**Attack:** typo/malicious token routed to a model/tool automatically.

**Mitigation:** unknown command hard error + suggestions; explicit AI command family only later.

### T-028 — Evidence freshness overclaim

**Attack:** old observation remains current after project change.

**Mitigation:** per-kind freshness basis/invalidation; current/unknown/stale states; refresh before claims with freshness preconditions.

### T-029 — Clock manipulation

**Attack:** wall-clock change makes stale evidence look young.

**Mitigation:** freshness may use sequence/content markers plus wall time; timestamp never security authority.

### T-030 — Repository move while open

**Attack:** path changes midway, causing records to bind to wrong location.

**Mitigation:** compare before/after strong locator/topology facts during catalog/project commit; mismatch retries/fails changed-under-observation.

### T-031 — Store directory permission exposure

**Attack:** local project metadata reveals sensitive paths to other users.

**Mitigation:** restrictive platform-appropriate per-user root where controllable; minimize stored sensitive data; document ACL limitations.

### T-032 — Store deletion/partial corruption mistaken as project deletion

**Attack:** local evidence loss causes claim project is gone or unsafe identity merge.

**Mitigation:** distinguish store unavailable/corrupt from project missing; conservative rebuild/reassociation; missing state is not project identity proof.

### T-033 — Unicode/non-UTF8 path loss

**Attack:** lossy conversion causes collision or wrong project selection.

**Mitigation:** explicit lossless OS-path machine representation; lossy display never identity key.

### T-034 — Bare repository surprise

**Attack:** commands assume worktree exists and traverse wrong path.

**Mitigation:** explicit bare state; worktree-dependent operations return not-applicable/capability unavailable.

### T-035 — Worktree metadata repair side effect

**Attack:** inspection invokes `git worktree repair/prune` and mutates metadata.

**Mitigation:** prohibited in S2. Doctor may report prunable/broken state only.

### T-036 — Concurrent first-open identity split

**Attack:** two processes see no binding, independently generate IDs, then each locks a different new project directory; the same project acquires two valid local identities.

**Mitigation:** first-open selection occurs under one bounded store-wide catalog lock before per-project lock; revalidate matching facts under lock; durable `reserved` entry is reused/recovered; fixed catalog-before-project lock order; duplicate allocation is a test failure.

### T-037 — Crash leaves abandoned reservation and duplicate retry identity

**Attack:** process commits project ID reservation then crashes before first generation is initialized; retry treats reservation as missing/broken and allocates another ID.

**Mitigation:** explicit `reserved|initialized` catalog states; retry under catalog lock revalidates and completes the same reservation; conflicting facts fail closed.

### T-038 — Cross-file mixed generation

**Attack:** identity/index/evidence files are replaced independently; crash or concurrent read combines records from different updates into a valid-looking state.

**Mitigation:** immutable complete generations plus manifest; tiny atomic `CURRENT` selector is the sole project commit point; reader reads `CURRENT` once and validates only that generation; orphan/incomplete generations never current.

### T-039 — Corrupt `CURRENT` or orphan generation recovery confusion

**Attack:** attacker/crash corrupts current pointer; implementation scans for newest parseable generation and silently promotes an uncommitted one.

**Mitigation:** corrupt/unsupported `CURRENT` is explicit store degradation; no arbitrary “newest valid” promotion. Recovery/cleanup is conservative and separately authorized where destructive.

### T-040 — Lock-holder denial of service

**Attack:** another WePLD process holds catalog/project lock indefinitely, causing `open/doctor/status` to hang.

**Mitigation:** non-blocking `try_lock` polling; default 2000ms acquisition deadline, 25ms polling, cancellation checks; stable `identity_catalog_busy` / `store_busy` outcomes; no indefinite fallback.

### T-041 — Descriptor amplification / parser DoS

**Attack:** hostile repository adds many recognized-looking files, oversized descriptors, deep nesting, or recursive workspace references to force large reads/CPU/memory.

**Mitigation:** exact root names only; <=32 candidates; <=1 MiB per parsed descriptor; <=4 MiB aggregate parsed bytes; nesting <=64; no root recursion; presence-only markers not parsed; deeper member traversal requires later contract.

### T-042 — Doctor secret exfiltration through finding prose/JSON

**Attack:** secret-bearing config, environment value, remote URL, manifest command, or command output is interpolated into `summary`, `explanation`, `remediation`, JSON, logs, or diagnostics.

**Mitigation:** finding prose chosen from WePLD-owned templates; parameters closed/allowlisted safe values only; evidence refs opaque; raw secret-bearing inputs prohibited; shared TTY/JSON redaction layer; credential/token/control-character fixtures.

### T-043 — Candidate governance self-authorizes planning

**Attack:** candidate text/checks are treated as trusted completion authority before trusted-base admission/Ready/post-merge activation.

**Mitigation:** record exact live base/main/head; trusted-base admission required; candidate policy cannot self-authorize; Ready-triggered admission reread; guarded merge; post-merge Foundation on canonical main.

### T-044 — Reviewer unavailability silently becomes approval

**Attack:** a requested/pending/rate-limited reviewer is treated as clean.

**Mitigation:** explicit `REVIEW_BLOCKED`; require reviewer qualification, independence, exact-head coverage, and completed state; any tracked repair invalidates prior review evidence.

## 5. Abuse-case acceptance tests

At minimum, implementation qualification must include negative tests proving:

1. project tree bytes are unchanged by open/doctor/status fixtures;
2. no `safe.directory` mutation occurs;
3. malicious gitfile cannot escape bounded parser/read scope;
4. symlink/junction cases do not become containment grants;
5. corrupt evidence cannot produce a healthy/current status;
6. concurrent ordinary writers cannot create a parseable mixed generation;
7. concurrent first opens cannot create two project IDs for one unseen project;
8. crash after first-open reservation reuses/revalidates the same reserved ID;
9. crash at every generation/manifest/`CURRENT` boundary yields old-or-new complete generation only;
10. lock contention completes within the bounded contract or explicit platform limitation;
11. descriptor count/size/aggregate/depth limits are enforced without recursion/execution;
12. secret-bearing remote/config/environment/manifest fixtures are absent from TTY/JSON/log/diagnostic outputs;
13. a self-consistent writer-level rewrite with recomputed unkeyed digests is never reported as authenticated/tamper-evident merely because structural validation passes;
14. unknown command cannot invoke AI/tool fallback;
15. no S2 network call is required;
16. linked worktrees remain distinct contexts.

## 6. Security review applicability

S2 implementation will touch filesystem parsing, identity, local persistence, external process behavior if Git adapter is admitted, and untrusted repository input. Therefore:

```text
CODEX_SECURITY_APPLICABILITY = APPLICABLE_TO_IMPLEMENTATION_WHEN_AVAILABLE
MISSING_CODEX_SECURITY = NOT_PASS
```

For this planning-only documentation package, security review examines whether the plan creates unsafe authority or omits required threat classes. No security PASS is asserted merely by planning text.

## 7. Residual risks

- filesystem races cannot be eliminated by path canonicalization;
- cross-platform rename/directory-entry/power-loss durability semantics differ;
- OS file-lock interactions vary by platform/filesystem and must be qualified per claimed environment;
- S2 has no authenticated local-store trust anchor; a writer-level attacker can forge an internally coherent store and recompute unkeyed digests, so structural validation must not be presented as writer authenticity/tamper evidence;
- user can deliberately override Git trust outside WePLD;
- hostile/network filesystems may provide weaker metadata/durability behavior;
- perfect move/copy identity inference is impossible without explicit durable identity stored with the project, which S2 intentionally avoids by default;
- bounded 2-second lock deadline may yield transient busy errors under legitimate long operations; later tuning requires explicit evidence/contract change, not unbounded fallback;
- macOS/Windows-specific runner limitations may leave explicit qualification gaps.

Residual risk must be reported; it must not be converted into PASS by optimistic prose.
