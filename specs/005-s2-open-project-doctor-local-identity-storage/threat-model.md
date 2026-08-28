# S2 Threat Model — Open Project + Project Doctor + Local Identity/Storage

## 1. Scope

S2 introduces a new trust boundary: WePLD begins reading local user-selected projects and persisting local identity/evidence about them. The target repository is untrusted input. The local evidence store is trusted only to the extent that its integrity can be verified.

This threat model is planning evidence. It grants no implementation/effect authority.

## 2. Assets

- correctness of selected project identity;
- separation of repository vs worktree identity;
- user filesystem privacy;
- integrity of local evidence records;
- freshness/provenance of observations;
- WePLD command-plane output integrity;
- Git/platform trust controls;
- local store availability and recoverability;
- absence of unintended project mutation;
- future authority separation between facts and effects.

## 3. Trust boundaries

### TB-1 — CLI/user locator → trusted core

Input path may be malformed, ambiguous, raceable, or point to hostile filesystem objects.

### TB-2 — target project filesystem → trusted core

All repository files/configuration/symlinks/gitfiles/workspace descriptors are untrusted data.

### TB-3 — system Git executable → trusted core

If later admitted, executable identity/path plus stdout/stderr/exit status are external-process inputs. Repository-controlled Git configuration may influence behavior.

### TB-4 — trusted core → local evidence store

Writes must survive concurrency/crash without creating valid-looking partial evidence.

### TB-5 — local evidence store → trusted core

Store contents can be stale, tampered, truncated, downgraded, partially deleted, or replaced.

### TB-6 — core contracts → human/machine/Desktop projections

A projection must not change semantic status, hide ambiguity, or manufacture PASS.

## 4. Threats and mitigations

### T-001 — Workspace escape through symlink/junction/reparse point

**Attack:** A repository path redirects outside the expected tree.

**Mitigation:** preserve lexical/resolved forms; inspect link/reparse facts; never infer containment from string prefix; no S2 arbitrary write inside project; future effects revalidate target at effect time.

**Residual:** observation can race after inspection.

### T-002 — TOCTOU replacement

**Attack:** path target changes between check and use.

**Mitigation:** treat S2 facts as snapshots; avoid effect-bearing trust decisions; future effect slices must use handle/identity-aware revalidation where required.

### T-003 — Windows case/canonicalization confusion

**Attack:** case-only paths, drive aliases, extended-length paths, junctions, or normalization differences cause identity collision.

**Mitigation:** never generic-lowercase paths; maintain platform-qualified representations; collision checks use multiple strong facts; adversarial Windows tests.

### T-004 — Symlink loop / broken link denial

**Attack:** recursive resolution loops or broken targets cause hangs/fallback guesses.

**Mitigation:** bounded standard APIs, no manual unbounded recursive following, explicit resolution errors, hard operation bounds.

### T-005 — Malicious `.git` assumptions

**Attack:** `.git` is a gitfile/linked worktree/hostile layout and a naïve parser escapes or misidentifies repository state.

**Mitigation:** never assume `.git` directory; prefer qualified official Git topology adapter if authorized; otherwise implement a deliberately limited parser with strict bounds and explicit unavailable states.

### T-006 — `safe.directory` bypass

**Attack:** hostile repository causes WePLD to add itself to trusted Git directories.

**Mitigation:** trust refusal becomes Doctor finding; S2 never changes protected Git config; no wildcard auto-remediation.

### T-007 — Repository hook/script execution

**Attack:** opening/Doctor inadvertently executes hooks, package lifecycle scripts, task files, build scripts, editor configs, or generated binaries.

**Mitigation:** descriptor reads are data-only; no task/package-manager/build execution; any Git adapter exact-command contract must prove it does not intentionally execute project hooks/scripts for S2 operations.

### T-008 — Spoofed Git executable

**Attack:** PATH resolves to a malicious `git` binary.

**Mitigation:** later adapter authority must define executable qualification/resolution. Unqualified executable => capability unavailable, not fallback execution.

### T-009 — Git output parser abuse

**Attack:** repository paths/reasons/output contain newlines/NULs/huge fields/invalid encoding to confuse parser.

**Mitigation:** prefer NUL-delimited porcelain where applicable; max output/field/record counts; closed parser state machine; fuzz/negative fixtures; invalid output fails closed.

### T-010 — Hidden network through discovery

**Attack:** S2 command contacts remotes or package registries.

**Mitigation:** S2 network authority none; no fetch/pull/package-manager commands; network-negative test/containment evidence when implementation exists.

### T-011 — Remote URL credential leakage

**Attack:** `https://user:token@host/...` or equivalent is persisted/logged.

**Mitigation:** remote URL is not required identity; sanitize/redact userinfo before evidence/logging; allowlisted evidence fields; secret-bearing raw value never persisted.

### T-012 — Identity false merge

**Attack:** two different projects/clones/copies are assigned one local project ID.

**Mitigation:** evidence-strength hierarchy; contradictions block reassociation; remote/HEAD alone insufficient; ambiguity is explicit.

### T-013 — Identity false split after move

**Attack:** same intended local project receives duplicate identities after benign rename/move.

**Mitigation:** deterministic conservative reassociation using strong stored/current topology evidence; user reconciliation seam later. Prefer false split over unsafe false merge when uncertain.

### T-014 — Linked worktree collapse

**Attack:** worktrees sharing common Git data overwrite one another's current project context.

**Mitigation:** model repository relationship separately from worktree context/root; identity-store keys include worktree-specific binding where required.

### T-015 — Store path traversal

**Attack:** project name/path/remote injects `../`, separators, reserved names, or device paths into local store.

**Mitigation:** store filenames derive only from WePLD-owned safe opaque IDs/encodings; raw project strings remain payload data.

### T-016 — Torn evidence write

**Attack:** crash/power loss leaves partial JSON accepted as complete.

**Mitigation:** full bytes built first; same-store temp; flush according to proven contract; atomic/replace step; schema/digest validation; partial/temp files never current.

### T-017 — Concurrent writer corruption

**Attack:** two WePLD processes interleave identity/evidence writes.

**Mitigation:** qualified exclusive lock or equivalent single-writer protocol; generation/conflict checks; failure returns contention, not silent last-writer corruption.

### T-018 — Stale lock denial

**Attack:** crash leaves lock artifact blocking forever.

**Mitigation:** prefer OS file-lock semantics whose ownership ends with handle/process rather than homegrown PID lockfiles; if lock files remain as names, their existence alone is not ownership proof.

### T-019 — Store tampering/downgrade

**Attack:** old/modified record is injected to make Doctor green.

**Mitigation:** schema/version/digest validation; explicit provenance and freshness; contradictions with live stronger facts surface; evidence does not authorize effects.

### T-020 — Oversized store record denial

**Attack:** huge local record exhausts memory.

**Mitigation:** hard per-file/per-record/aggregate size bounds before parse; bounded collection sizes.

### T-021 — Unsupported schema confusion

**Attack:** future/unknown fields/statuses are misread as PASS.

**Mitigation:** versioned envelope; closed authority/status semantics; unsupported versions explicit, never default to complete/current.

### T-022 — Raw environment secret capture

**Attack:** Doctor snapshots tokens/keys from environment.

**Mitigation:** no raw environment dump; explicit allowlisted non-secret facts only if required.

### T-023 — Malicious workspace descriptor

**Attack:** package manifest contains pathological size/encoding/structure or command strings intended for later execution.

**Mitigation:** bounded file size/parser; treat commands as opaque descriptive data; never execute during S2; no template/eval interpolation.

### T-024 — Package-manager ambiguity hidden

**Attack:** Doctor silently picks an attacker-controlled lockfile/tool configuration.

**Mitigation:** deterministic precedence only where ecosystem contract proves it; otherwise emit ambiguity finding.

### T-025 — Doctor finding injection into terminal

**Attack:** project-controlled strings inject ANSI/control sequences or misleading formatting.

**Mitigation:** escape/control-filter untrusted strings in human output; structured JSON preserves data safely without terminal interpretation.

### T-026 — JSON consumer authority confusion

**Attack:** downstream agent interprets `healthy=true` as permission to run commands.

**Mitigation:** schemas never include effect grants; documentation and types separate fact/health from authority; future Nawat grants use different contracts.

### T-027 — Unknown command becomes AI execution

**Attack:** typo or malicious token is routed to a model/tool automatically.

**Mitigation:** unknown command hard error + suggestions; explicit AI command family only later.

### T-028 — Evidence freshness overclaim

**Attack:** old observation remains shown as current after project change.

**Mitigation:** per-kind freshness basis/invalidation; current/unknown/stale states; refresh required before claims with freshness preconditions.

### T-029 — Clock manipulation

**Attack:** wall-clock change makes stale evidence look young.

**Mitigation:** freshness may use observation sequence/content markers plus wall time; never use timestamp alone for security authority.

### T-030 — Repository move while open

**Attack:** path changes midway, causing records to bind to wrong location.

**Mitigation:** compare before/after strong locator/topology facts during identity commit; mismatch retries/fails as changed-under-observation.

### T-031 — Store directory permission exposure

**Attack:** local project metadata reveals sensitive paths to other users.

**Mitigation:** create per-user data root with restrictive platform-appropriate permissions where controllable; avoid storing unnecessary secrets; test/document platform ACL limitations.

### T-032 — Store deletion/partial corruption mistaken as project deletion

**Attack:** local evidence loss causes WePLD to claim project is gone or create unsafe identity merge.

**Mitigation:** distinguish `store_unavailable/corrupt` from `project_missing`; rebuild/reassociate conservatively; missing local state is not proof about project identity.

### T-033 — Unicode/non-UTF8 path loss

**Attack:** lossy conversion causes collisions or wrong project selection.

**Mitigation:** freeze explicit OS-path encoding representation for machine schema; never use lossy display string as identity key.

### T-034 — Bare repository surprise

**Attack:** commands assume worktree exists and traverse wrong path.

**Mitigation:** explicit bare state; commands requiring worktree return capability unavailable/not applicable.

### T-035 — Worktree metadata repair side effect

**Attack:** inspection invokes `git worktree repair/prune` and mutates repository metadata.

**Mitigation:** prohibited in S2. Doctor may report prunable/broken state only.

## 5. Abuse-case acceptance tests

At minimum, implementation qualification must include negative tests proving:

1. project tree bytes are unchanged by open/doctor/status fixtures;
2. no `safe.directory` mutation occurs;
3. malicious gitfile cannot escape bounded parser/read scope;
4. symlink/junction cases do not become containment grants;
5. corrupt evidence cannot produce a healthy/current status;
6. concurrent writers cannot create a parseable mixed record;
7. secret-bearing remote data is redacted;
8. unknown command cannot invoke AI/tool fallback;
9. no S2 network call is required;
10. linked worktrees remain distinct contexts.

## 6. Security review applicability

S2 implementation will touch filesystem parsing, identity, local persistence, external process behavior if Git adapter is admitted, and untrusted repository input. Therefore:

```text
CODEX_SECURITY_APPLICABILITY = APPLICABLE_TO_IMPLEMENTATION_WHEN_AVAILABLE
MISSING_CODEX_SECURITY = NOT_PASS
```

For this planning-only documentation package, security review still examines whether the plan creates unsafe authority or omits required threat classes; no security PASS is asserted by planning text.

## 7. Residual risks

- filesystem races cannot be eliminated by path canonicalization;
- cross-platform rename/directory durability semantics differ;
- user can deliberately override Git trust outside WePLD;
- hostile network filesystems may provide weaker metadata/durability behavior;
- perfect move/copy identity inference is impossible without explicit durable identity stored with the project, which S2 intentionally avoids by default;
- macOS/Windows-specific runner limitations may leave explicit qualification gaps.

Residual risk must be reported; it must not be converted into PASS by optimistic prose.
