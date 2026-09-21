# ASTRO-F01 — Freeze current frontier and limitation carry-forward

```text
TASK = ASTRO-F01
TASK_TYPE = D (bounded specification / qualification manifest)
SLICE = P0 / S3
HANDOFF_CARD = WEPLD_MUSE_EXECUTION_HANDOFF.md (ASTRO-F01)
PREREQUISITE = ASTRO-G01 accepted

BASE = 100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde
BASE_TREE = a0abd67acd610284d275fad87662a4ab7f64fcb2
CANONICAL_REPOSITORY = TheHalfMoon/wepld
CANONICAL_DEFAULT_BRANCH = main
```

This record is a bounded authority matrix. It grants nothing. It is the F01
deliverable named by the accepted Muse handoff: one matrix linking the eight
carried-forward S2 limitations and each S3 task group to the exact current
grant, the exact current paths, the current native evidence and the applicable
stop conditions.

## 1. Bounded output and non-goals

```text
BOUNDED_OUTPUT = this single record
PRODUCT_CODE_CHANGE = NONE
RUNTIME_DEPENDENCY_CHANGE = NONE
CI_POLICY_CHANGE = NONE
PROTECTED_GOVERNANCE_CHANGE = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
AUTHORITY_EFFECT = NONE
RIGHTS_EFFECT = NONE
```

Non-goals, per the F01 card and the common task contract:

- no host, filesystem, network, process, spawn or containment implementation;
- no Windows API binding selection or admission;
- no mutation of `docs/canonical/*`, `specs/005-*`, `specs/007-*` or any other
  historical record — historical records are preserved byte-identically;
- no re-opening of the accepted planning revision for edits;
- no claim that a planning artifact is a capability.

The existing owners and conventions are reused. No new owner, store, contract
module or numbering system is introduced by this record.

## 2. Verified inputs used to build this matrix

Every row below is traceable to a canonical artifact read from the trusted base
for this task. Live GitHub state was re-read before writing; the trusted base is
the exact PR base of this candidate.

| Input | Exact identity | Role here |
|---|---|---|
| Canonical `main` | `100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde`, tree `a0abd67acd610284d275fad87662a4ab7f64fcb2` | trusted base for this record |
| Accepted planning head | `4deee28f85153c357e5a51413cbef438297f67cc` | ASTRO-G01 exact accepted head |
| ASTRO-G01 acceptance | PR #340 acceptance record and post-merge closure (comment on PR #340); post-merge `foundation-integrity` run `35513354193` = PASS | prerequisite evidence |
| Active integrity successor | `.github/scripts/wepld_s3_contracts_freeze_shortcut_v71_integrity.py`, blob `e2b3caf4ef7e0ed0e34c7415776cb29c92d752e0` | current grant source |
| Integrity workflow | `.github/workflows/foundation-integrity.yml`, blob `be8dd63cd222b326353dc72468bfb6e7d6f57585` | current deterministic gate wiring |
| Base policy module | `.github/scripts/wepld_integrity.py` | stage/allowed-path mechanism |
| S2 task ledger | `specs/005-s2-open-project-doctor-local-identity-storage/tasks.md` | authority for S2 limitation rows |
| S2 acceptance record | `specs/005-s2-open-project-doctor-local-identity-storage/acceptance.md` | §H.1 and §J context |
| S3 task ledger | `specs/007-s3-terminal-fabric-trusted-process-ownership/tasks.md`, blob `43331b50a26f8920286e616fb2ef11e3f9f7b83c` | authority for S3 task groups |
| Decision and gap ledger | `specs/006-issueops-agentic-engineering-control-plane/astro-master/WEPLD_DECISION_AND_GAP_LEDGER.md` | GAP-02 and GAP-03 obligations this record discharges |
| Architecture invariants | `docs/canonical/ARCHITECTURE_INVARIANTS.md` | invariant set the matrix must not contradict |
| Governance checkpoint | `docs/canonical/CURRENT_STATE.md` | durable memory, explicitly not live-state authority |

`docs/canonical/CURRENT_STATE.md` is used as durable memory only. Where its
frozen text and later merged successor policy differ, the merged successor
policy and live GitHub state control, and this record follows them.

## 3. S2 carried-forward limitation matrix

S2 reached `CLOSED_CANONICAL` under `S2-A006` while carrying eight `[~]` rows
forward. The governing rule recorded with that decision is preserved verbatim:

```text
ACCEPTED_LIMITATION != PROVEN_REQUIREMENT
CARRIED_FORWARD != DISCHARGED
CLOSED_CANONICAL_S2 != ALL_FUTURE_PLATFORM_EVIDENCE_PROVEN
ABSENCE_OF_EVIDENCE != PASS
```

No row below is converted to a satisfied requirement by this record. No row is
closed by this record. Each row states what is actually proven today, what
remains unproven, which exact current grant and path is relevant, what native
evidence would be required, and the stop condition that keeps the limitation
visible.

| Row | Actually proven today | Not proven today | Relevant current grant / path | Native evidence required to close | Stop condition |
|---|---|---|---|---|---|
| `S2-S001` Path traversal / canonicalization / TOCTOU suite | A real on-disk retargeted-symlink TOCTOU mismatch (`crates/core/tests/project_v1.rs::symlink_retargeted_between_reservation_and_recovery_is_a_toctou_mismatch`, `#[cfg(unix)]`), plus lexical parent-escape clamping, interior-NUL `InvalidPath`, and no-fabricated-resolution behaviour in `project_v1.rs` | Windows reserved/device-name paths (`CON`, `NUL`, `COM1`, trailing dot/space, ADS `:` streams) under real Windows semantics | No S3 grant covers this row. `v71` grants `EXACT_CONTRACTS_S3_C001_C013_ONLY` inside `crates/contracts/` only. | A native Windows `wepld-core` execution surface able to exercise those names under real Windows path semantics | Do not report this row closed on Unix-only evidence; do not add Windows path fixtures to `crates/contracts/` to make it look closed |
| `S2-S003` Windows junction / reparse / extended-length path tests | Extended-length verbatim-prefix normalization (`\\?\`, `\\?\UNC\`) via injected inputs on Linux/macOS (`identity_store_v1.rs::windows_root_forms_normalise_without_loss`) | Real Windows junction/reparse behaviour; no native Windows `wepld-core` runtime exists | `S2_S003_ADOPTED = YES` into the S3 package; the S3 owners are `S3-H005`/`S3-H006`/`S3-H007` and `S3-Q001` | Native Windows `wepld-core` CI executing S2's existing junction/reparse fixtures unmodified | Stop S3 host work before `S3-AUTH-HOST` separately grants paths; do not edit S2 fixtures to reach green |
| `S2-S005` Git `safe.directory` refusal, no auto-bypass | Observation never writes or widens `global_safe_directory_entries()`; bare repositories observed explicitly; `RefusedByGit` classification mapping | The real end-to-end ownership-mismatch refusal — not exercisable on hosted CI, which sets `safe.directory = *` | No S3 grant covers this row; the Git adapter lives in `crates/core`, which `v71` does not authorize | A containerized or self-hosted CI surface with a genuinely dubious repository | Do not treat synthetic stderr classification as the end-to-end refusal proof |
| `S2-S007` External Git output / environment / parser / timeout / no-hook / no-network tests | Twelve planted hook names never fire with repo-local `core.hooksPath` pinned; output-ceiling mechanism, environment scrub and porcelain parser all unit-tested; argv is a closed enum; `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C` | Real over-ceiling output through `run_git` at `GIT_STDOUT_MAX_BYTES`/`GIT_STDERR_MAX_BYTES`; the real 10 s hard timeout firing | No S3 grant; `crates/core` is outside the current authorized delta | An admitted fault-injection or fake-Git seam, plus the containerized surface for `S2-S005` | Do not claim timeout/ceiling coverage from mechanism-level unit tests |
| `S2-Q001` Windows deterministic gate | `wepld-core` compiles on `windows-latest` (`desktop-windows`) | Any native Windows `wepld-core` suite execution; `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` | `S3-Q001` is the shared precondition with `S3-H005`; no grant exists yet | Native Windows `wepld-core` execution of the S2 suite | Compile coverage must never be reported as runtime coverage |
| `S2-Q004` Large-repository fixture (no non-allowlisted reads, no below-root classification) | 600 top-level files, a 40-level nested subtree, two 8 MiB non-allowlisted blobs and a buried conflicting lockfile pair, budget-clean and ambiguity-free, `< 30s` for that one fixture | Discrimination against a byte-free but still recursive `stat` enumeration; any scaling benchmark | No S3 grant; fixture and source live in `crates/core` | A direct traversal-syscall assertion and a tree-size scaling benchmark | Do not present the single `< 30s` ceiling as a scaling result |
| `S2-Q008` Git adapter timeout / output-ceiling evidence | `bounded_reader_stops_at_limit_and_signals_overflow` at a synthetic 32-byte limit; the shared forced-termination path proven through the `Cancelled` sibling arm | The real constants end-to-end: `GIT_STDOUT_MAX_BYTES` (1 MiB), `GIT_STDERR_MAX_BYTES` (256 KiB), and the real `GIT_TOPOLOGY_TIMEOUT_MS` (10 000) trigger | `BENCHMARK_HARNESS = NOT_ADMITTED`; no S3 grant covers this row | Admitted test seam plus the ceiling/timeout fixtures above | `STATED_BOUND != MEASURED_BOUND`; do not publish a latency distribution that does not exist |
| `S2-Q009` Performance ceiling evidence with fixture identity | Fail-closed ceiling oracles for descriptor discovery and lock-acquisition deadline; the enumerated fixture identity above | Git output/timeout ceilings at their real constants; any published timing distribution | Same as `S2-Q008` | Same as `S2-Q008` | Re-running enumerated oracle tests is not a benchmark publication |

Carry-forward obligation for the frontier: every row above remains an open,
owned obligation. `S2-S003` is the only one with an accepted adoption into S3
(`acceptance.md` §H.1); the remaining seven have no S3 owner and must be
re-recorded at the slice that owns them rather than silently dropped or
silently converted to `[x]`.

## 4. S3 task-group authority matrix

The S3 ledger is present on canonical `main`, and its own header still records
planning-package state:

```text
PLANNING_BASE = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
PLANNING_STATE = DRAFTED_PENDING_EXACT_HEAD_REVIEW
S3_IMPLEMENTATION_AUTHORITY = NOT_GRANTED
NEXT_AUTHORITY_GATE = S3_PLANNING_ACCEPTANCE
```

Separately, the merged successor policy `v71` grants a narrow, exact
implementation delta. Both statements are true at once and the difference
matters: the ledger is the task map, the policy is the effect grant. Neither
substitutes for the other.

| Group | Ledger tasks | Current grant | Exact current paths | Native evidence today | Stop condition |
|---|---|---|---|---|---|
| `S3-AUTH-C` pure contracts | `S3-C001`..`S3-C013` | `S3_IMPLEMENTATION_AUTHORITY = EXACT_CONTRACTS_S3_C001_C013_ONLY` under `S3_CONTRACTS_FREEZE_SHORTCUT_SUCCESSOR` | `crates/contracts/src/s3.rs` (new), `crates/contracts/tests/s3_contracts_v1.rs` (new), `crates/contracts/src/lib.rs` (export only) | None required — this group is pure contract/serialization surface | Stop on any host API use, spawn, network, dependency/manifest edit, or a mixed non-contract delta in the same candidate |
| `S3-AUTH-HOST` host/containment qualification | `S3-H001`..`S3-H007` | Not granted. `S3_AUTH_HOST_AUTHORITY = NOT_GRANTED`; `WINDOWS_API_AUTHORITY = NONE`; `JOB_OBJECT_AUTHORITY = NONE`; `CONTAINMENT_ACTUATION_AUTHORITY = NONE` | None | None | Stop before any Windows API binding selection, Job Object work, or containment claim; requires its own exact-path successor |
| `S3-AUTH-OBSERVE` effect/PEP seam | `S3-E001`..`S3-E006` | Not granted. `S3_AUTH_OBSERVE_AUTHORITY = NOT_GRANTED` | None | None | Stop before ownership-epoch, observation or cancellation implementation; requires its own exact-path successor |
| `S3-AUTH-SPAWN` process-spawn adapter | `S3-SP001`..`S3-SP007` | Not granted. `S3_AUTH_SPAWN_AUTHORITY = NOT_GRANTED`; `PROCESS_SPAWN_AUTHORITY = NONE` | None | None | Stop before argv allowlists, executable resolution or environment injection; separately reviewed source/security gate required |
| `S3` security / adversarial fixtures | `S3-S001`..`S3-S011`, `S3-S003a` | Only the `C013` secret-safety negative surface is reachable today, and only inside the authorized contract paths | `crates/contracts/tests/s3_contracts_v1.rs` | None | Stop: PID-reuse, epoch-race, job-object-unavailable, cancellation-hang and no-network fixtures require grants that do not exist |
| `S3` platform / qualification | `S3-Q001`..`S3-Q004` | Not granted beyond compile coverage; `PLATFORM_REQUIRED_CHECK_ENFORCEMENT = NOT_PROVEN` | None | `windows-latest` compile only; `S2_WINDOWS_CORE_RUNTIME = NOT_COVERED` | Stop: do not record `NONE`/`UNKNOWN` platform rows as qualified, and do not claim native containment |
| `S3` acceptance program | `S3-A001`..`S3-A010` | Not granted | None | None | Stop: acceptance follows implementation, never precedes it; `S3-A010` must confirm the final `S2-S003` disposition rather than drop it |

The groups that are *not* granted are not merely unimplemented. They are
unauthorized: the current successor explicitly records `FILESYSTEM_RUNTIME_AUTHORITY = NONE`,
`CREDENTIAL_AUTHORITY = NONE`, `NETWORK_AUTHORITY = NONE`,
`MODEL_PROVIDER_EXECUTION = NONE`, `SOURCE_ADMISSION = NONE` and
`S4_PLUS_AUTHORITY = NONE`.

## 5. Current effect grant, stated exactly

The only implementation authority in force at this base is the v71 successor.
Its own bound, quoted from the policy it enforces:

```text
AUTH = S3_CONTRACTS_FREEZE_SHORTCUT_SUCCESSOR
S3_PLANNING_AUTHORITY = CANONICAL_PRESERVED
S3_IMPLEMENTATION_AUTHORITY = EXACT_CONTRACTS_S3_C001_C013_ONLY
CONTRACT_CAPABILITY_SCAN_AUTHORITY = ENFORCED
S1_007_FREEZE_EXEMPTION_AUTHORITY = S3_CONTRACT_FILES_ONLY
FILESYSTEM_RUNTIME_AUTHORITY = NONE
WINDOWS_API_AUTHORITY = NONE
JOB_OBJECT_AUTHORITY = NONE
CONTAINMENT_ACTUATION_AUTHORITY = NONE
PROCESS_SPAWN_AUTHORITY = NONE
CREDENTIAL_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
SOURCE_ADMISSION = NONE
S3_AUTH_HOST_AUTHORITY = NOT_GRANTED
S3_AUTH_OBSERVE_AUTHORITY = NOT_GRANTED
S3_AUTH_SPAWN_AUTHORITY = NOT_GRANTED
S4_PLUS_AUTHORITY = NONE
```

`crates/contracts/Cargo.toml` and `Cargo.lock` are pinned identity constants in
the same successor. A candidate that changes either is rejected, which is the
mechanical form of "no dependency edit is authorized by the pure-contract
grant".

## 6. Required negative oracle

The F01 card requires one specific negative oracle:

```text
ORACLE = pure-contract grant must not allow host APIs, spawn, network or dependency edits
```

Recorded disposition of that oracle against this base, per enforcement mechanism
and per authorized path:

| Oracle leg | Enforcing mechanisms | Result |
|---|---|---|
| Host APIs | authority constants `WINDOWS_API_AUTHORITY`/`JOB_OBJECT_AUTHORITY`/`CONTAINMENT_ACTUATION_AUTHORITY = NONE`, the v70 substring capability scan, and the inherited S1-006 prohibited-effect identifier scan | ENFORCED_BY_POLICY |
| Spawn | `PROCESS_SPAWN_AUTHORITY = NONE` and `S3_AUTH_SPAWN_AUTHORITY = NOT_GRANTED`, plus the same two scans | ENFORCED_BY_POLICY |
| Network | `NETWORK_AUTHORITY = NONE`, plus the same two scans | ENFORCED_BY_POLICY |
| Dependency edits | `crates/contracts/Cargo.toml` and `Cargo.lock` are pinned identities in the successor; changing either fails candidate verification | ENFORCED_BY_POLICY |
| Mixed non-contract delta | a contract file combined with an unrelated change still delegates to the inherited frozen-S1-protocol check and fails | ENFORCED_BY_POLICY |

### Which mechanism covers which authorized contract path

| Authorized contract path | v70 substring capability scan | S1-006 prohibited-effect identifier scan | Other checks |
|---|---|---|---|
| `crates/contracts/src/s3.rs` | YES | no — not a member of `S1_006_ALLOWED_PATHS` | — |
| `crates/contracts/tests/s3_contracts_v1.rs` | YES | no — not a member of `S1_006_ALLOWED_PATHS` | — |
| `crates/contracts/src/lib.rs` | no — not a member of `SCANNED_CONTRACT_PATHS` | YES — explicit member of `S1_006_ALLOWED_PATHS` | v69 export checks (mode, non-empty, no NUL, UTF-8, exactly one `pub mod s3;`) and the v70 crate-scope `#![forbid(unsafe_code)]` marker |

The two scans differ in kind. The v70 scan matches literal substrings
(`std::fs`, `std::net`, `std::process`, `std::os::`, `std::env`, `windows::`,
`winapi::`, `libc::`, grouped `std::{...}` imports) and the `unsafe` token. The
inherited S1-006 scan extracts Rust identifiers and rejects a prohibited set
that includes `fs`, `net`, `process`, `env`, `thread`, `tokio`, `tauri`,
`Command`, `TcpStream`, `TcpListener`, `UdpSocket`, `UnixStream`, `UnixListener`,
`NamedPipe`, `File`, `OpenOptions`, `stdin`, `stdout`, `stderr`, `print`,
`println`, `eprint`, `eprintln`, `include`, `include_bytes` and `include_str`.

```text
ALL_THREE_AUTHORIZED_CONTRACT_PATHS_ARE_CAPABILITY_SCANNED = YES
MECHANISMS_DIFFER_PER_PATH = YES
ORACLE_STATUS = ENFORCED_BY_POLICY
```

### Executed negative-oracle candidate

The oracle was executed rather than inferred. A local-only probe branch — never
pushed — started from this same base and combined the C001..C013 contract shape
(the two new contract files plus the `s3` registration in the export path) with a
planted prohibited capability in the export path:

```text
PROBE_BRANCH = codex/astro-f01-neg-oracle-probe (local worktree only, never pushed)
PROBE_BASE = 100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde
PROBE_PLANTED = std::process::Command usage in crates/contracts/src/lib.rs
PROBE_RESULT = FAIL as required
PROBE_MESSAGE = "wepld integrity verification: FAIL: S1-006 prohibited effect
                 identifier(s) found in code: crates/contracts/src/lib.rs: Command, process"
```

The planted capability was rejected. The executed leg and the unexecuted legs are
now recorded separately, because one probe class is not the whole oracle:

```text
EXECUTED_ORACLE_LEG = a planted identifier-based process/spawn capability in
                      crates/contracts/src/lib.rs (`std::process::Command`) was rejected
                      by the inherited S1-006 identifier scan
STATIC_POLICY_COVERAGE_ONLY = the network leg (NETWORK_AUTHORITY = NONE plus the same
                      S1-006 identifier set, whose members include TcpStream, TcpListener,
                      UdpSocket, UnixStream, UnixListener and NamedPipe) and the
                      dependency-edit leg (the pinned crates/contracts/Cargo.toml and
                      Cargo.lock identities that make a manifest or lock edit fail
                      candidate verification) are enforced by policy and mechanism
                      reading at this base; no separate negative probe was executed for
                      either leg by this task
EXECUTED_PROBE_CLASSES = 1 (host-API / spawn); the remaining oracle classes are static
                      policy coverage only
```

### Independent-review finding reconciled in this section

An independent review of this pull request raised a `🟠 Major` `CWE-693` finding
stating that `SCANNED_CONTRACT_PATHS` excludes `crates/contracts/src/lib.rs` and
concluding that "a valid export can therefore contain safe `std::fs`, `std::net`,
or `std::process` APIs without rejection".

```text
FINDING_OBSERVATION = ACCURATE (the v70 substring scan does exclude the export path)
FINDING_CONCLUSION = REFUTED_BY_EXECUTED_ORACLE
FINDING_DISPOSITION = PARTIALLY_VALID / CONCLUSION_NOT_ACCEPTED
```

The observation is correct and is recorded above. The conclusion is not: the
export path is covered by the inherited S1-006 identifier scan, and the executed
probe shows that a planted `std::process::Command` in that exact file fails
verification. The reviewer's requested change — add the export path to the
substring scan and add a negative export-file candidate test — is therefore not
required by this oracle, and it would in any case be an enforcement-policy change
outside this task's bounded scope, since the active successor wrapper is frozen
after activation.

Residual nuance, recorded because it is true and not upgraded into a claim: the
two mechanisms do not overlap. `s3.rs` and the C01 test file are covered by the
substring scan and not by the identifier scan; the export path is covered by the
identifier scan and not by the substring scan. Converging them is a reasonable
future hygiene change for the enforcement owner, and this record does not assert
that either mechanism is complete on its own.

This section records enforcement as exercised. It is not a runtime security
result and not a substitute for running the policy verifier; the executed result
for this exact candidate is recorded in §8.

### Exact-head review findings reconciled after the correction

```text
REVIEW_PRODUCER = CodeRabbit (manual opt-in under the recorded egress preflight)
REVIEWED_HEAD = 32e76810b78d1e98dffca64c5adaf63c8217e72c
FINDINGS = 2, both Minor
F1 = the oracle conclusion claimed more executed coverage than the probe exercised:
     the network leg and the dependency-edit leg were static policy coverage only
F2 = the bullet describing the executed probe was filed under the
     "Not executed here, and therefore not claimed" heading
F1_DISPOSITION = ACCURATE_ACCEPTED; the executed leg is now labelled explicitly and the
     remaining legs are labelled static policy coverage in this section
F2_DISPOSITION = ACCURATE_ACCEPTED; the bullet was moved to "Recorded checks" with its
     local-only, never-pushed and not-part-of-this-candidate qualifiers intact
FINDINGS_GRANT_WRITE_AUTHORITY = NO; both repairs are documentation corrections inside
     this task's bounded output
```

## 7. Preserved historical records

This task freezes the frontier by reading it, not by editing it. The following
remain byte-identical to the trusted base and are deliberately not touched:

- `docs/canonical/CURRENT_STATE.md` — frozen durable memory, writable only
  through its own paired policy-successor transition;
- `docs/learning/BUILD_LEARNING_LEDGER.md` — same paired-transition discipline;
- `specs/005-s2-open-project-doctor-local-identity-storage/tasks.md` and
  `acceptance.md` — the S2 limitation record and the `S2-A006` decision;
- `specs/007-s3-terminal-fabric-trusted-process-ownership/*` — the S3 planning
  package, including its still-pending planning markers;
- `specs/006-.../astro-master/*` — the accepted planning revision
  (`4deee28f85153c357e5a51413cbef438297f67cc`), accepted as-is;
- `.github/scripts/*` and `.github/workflows/*` — no policy or gate change in
  this task.

Preserving these records is the point of the task. A freeze that rewrote the
thing it froze would destroy the evidence it exists to preserve.

## 8. Verification performed and coverage limits

Recorded checks:

- the trusted base, tree and accepted planning head in §2 were resolved from
  live canonical `main` and live GitHub state rather than copied from a chat
  summary;
- every S2 row above is traceable to the S2 task ledger rows that the `S2-A006`
  decision carries forward, and every S3 group is traceable to the S3 ledger
  sections;
- every quoted authority constant in §5 is taken from the active successor
  policy file at this base;
- the candidate delta of this task is documentation-only: one new Markdown
  record, with no executable, workflow, configuration, dependency or protected
  governance change.
- the export-path enforcement probe described in §6 was executed on a local-only
  probe branch started from this same base and failed as required
  (`S1-006 prohibited effect identifier(s) found in code:
  crates/contracts/src/lib.rs: Command, process`); that probe branch was never
  pushed and its sources are not part of this candidate. This is a recorded
  check on the enforcement mechanism, distinct from the exact-head CI check for
  this candidate, which has not been run by this record.

Not executed here, and therefore not claimed:

- the `foundation-integrity` candidate verification for this exact head is a CI
  result and is not asserted by this record before that run exists;
- no native Windows qualification was performed; §3 and §4 record that absence
  as a first-class status rather than as a pass;
- no source acquisition, dependency admission, donor execution or benchmark was
  performed by this task;
- Codex Security applicability for this task is `NOT_APPLICABLE` on the
  ground that the change adds planning/governance Markdown only and alters no
  trust boundary, authority implementation, parser, containment or credential
  surface. This is an applicability classification, not a security pass.

## 9. Successors unlocked by acceptance

Acceptance of this record unlocks exactly the successors named by the F01 card:

```text
ASTRO-C01
ASTRO-A01
ASTRO-A04
ASTRO-A05
ASTRO-A06
ASTRO-A07
ASTRO-A08
ASTRO-A09
```

No enforcement obligation is carried forward by this task. The required oracle is
already enforced on all three authorized contract paths (§6), so nothing here
gates `ASTRO-C01` on a new policy successor. One non-blocking improvement
candidate is recorded instead:

```text
RECORDED_IMPROVEMENT_CANDIDATE = converge the v70 substring capability scan and the
                                 inherited S1-006 identifier scan so that every
                                 authorized contract path is covered by both
                                 mechanisms
REQUIRED_FOR_THE_ORACLE = NO
OWNER = the S3-AUTH-C enforcement owner, at its own discretion
```

Correction recorded against the G01 acceptance text: PR #340's acceptance record
also listed `ASTRO-P01` as unlocked by G01, but the P01 card in the same handoff
declares dependencies `ASTRO-G01, ASTRO-A09`. The card's own dependency list is
the more specific statement, and `ASTRO-A09` is not accepted at this base
therefore `ASTRO-P01` remains blocked on `ASTRO-A09`, not on `ASTRO-G01` alone.
No other successor is unlocked, and acceptance here grants no implementation
authority beyond the successor policy already in force.

## 10. Resume record

```text
TASK = ASTRO-F01
BRANCH = codex/astro-f01-frontier-freeze-20260921
BASE = 100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde
SCOPE_GRANT = documentation-only task record under
              specs/006-issueops-agentic-engineering-control-plane/astro-execution/
CHANGED_FILES = 1 (this record)
SOURCE_PINS = none acquired by this task
COMPLETED_TESTS = trusted-base resolution, traceability checks, delta-shape check,
                  and the executed export-path negative-oracle probe (section 6),
                  plus the exact-head deterministic gates recorded on the pull request
PENDING_TESTS = exact-head re-review of the repaired head, then the guarded merge and
                its post-merge verification
REVIEW_STATE = reviewed on the first head (one Major finding, conclusion refuted by the
               executed oracle) and again on head 32e76810 (two Minor documentation
               findings, both accepted and repaired in this record). The repaired head
               is a new exact-head review target, so a fresh review of it is required
               rather than reuse of either earlier review.
UNKNOWN_EFFECTS = none identified; no effect was proposed
OPEN_FINDINGS = none unresolved; one non-blocking improvement candidate recorded
                in section 9
NEXT_SMALLEST_ACTION = record exact-head deterministic evidence for the repaired head,
                      request the fresh exact-head review, and proceed to acceptance
                      only if that review produces no unresolved material finding
```

Resuming this task means re-reading live canonical `main`, re-resolving the
identities in §2, and comparing them against this record. A remembered narrative
is not evidence, and a superseded base invalidates every identity above.
