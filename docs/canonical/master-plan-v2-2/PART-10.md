
## 29. Corrected Ten-Slice Roadmap and Non-Primary S3-D Gate

`PRIMARY_SLICES_COUNT = 10`. S3-D is a non-primary Assurance Seed gate between S3 and S4; it is not an eleventh slice and creates no new authority domain.

### 29.1 Shared build protocol for every code-changing slice

Before any code-changing slice begins, an authorized development packet must run the external build methodology:

1. **Spec Kit:** constitution → specify → clarify → plan → checklist → analyze → tasks → implement. These are controlled development artifacts, not canonical product truth by themselves. Record the exact release/tag/commit where applicable, workflow/template version or digest, configuration, and provenance.
2. **Ponytail FULL:** challenge every proposed dependency, abstraction, privilege, worker/service, data copy, deployment boundary, recovery mechanism, evidence path, accessibility impact, and authority-bearing type. “Minimum sufficient” cannot remove a protected safety, recovery, accessibility, evidence, or authority concern. Record the exact release/version/commit where applicable and the ruleset/skill/configuration digest with `PONYTAIL_MODE = FULL`.
3. **Cubic independent review:** run on the exact change when the approved egress envelope permits. Record CLI/client version, review configuration/profile, observable service/policy snapshot where applicable, data-egress classification, retention/disclosure qualification, exact target/revision and all findings. If denied or unavailable, record the exact `NOT_RUN_*` state; never infer pass. Cubic is non-authoritative. Exceptional acceptance without the normally required Cubic route requires an explicit waiver by the same authorized acceptance authority that may decide G9, an independently qualified substitute review route, and a recorded residual limitation.
4. **WePLD-owned controls:** deterministic checks, applicable security and negative tests, independent human/Assurance review, evidence admission, and authorized slice exit remain mandatory. An external tool cannot grant acceptance.

**Bootstrap rule for pre-native development evidence.** Before a corresponding WePLD-native subsystem exists and has been accepted, its obligation is represented by immutable external development evidence with stable identifiers, hashes/digests, exact scope, authority, provenance, acceptance obligations, budgets where applicable, recovery/rollback obligations, and evidence references. Such evidence MUST NOT be described as an already-native `Work`, `Mission`, `Attempt`, `ContextCapsule`, or Nawat grant/record when that product capability does not yet exist. From the first accepted slice that implements the relevant native capability, subsequent slices MUST use the WePLD-native representation where applicable. This creates no new canonical aggregate: it preserves no ambient authority, no fabricated canonical identity, no false self-hosting claim, and full traceability from S1 onward.

Every slice must additionally have an approved component ledger, an acceptance policy or its immutable pre-native equivalent, budget, rollback/recovery plan, evidence retention, accessibility/RTL review where user-facing, and no unresolved scope expansion. Native Work/Mission/Attempt, ContextCapsule, and Nawat records are required only from the first accepted slice that makes each corresponding native representation available and applicable.

The `EXPECTED_PATHS` below are provisional physical-placement hypotheses for planning. P0 vocabulary/ownership and repository inventory may refine them before implementation; listing a path does not authorize creating it.

### 29.2 S1 — Desktop ↔ Rust Trusted Core Handshake

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Establish one typed, versioned, observable request/response/event channel between the Tauri desktop and a separate Rust Core process |
| `USER_VALUE` | A desktop shell can connect, report health/version/capabilities, cancel a request, and fail clearly without hidden authority |
| `ARCHITECTURE_DELTA` | Core owns authority-bearing validation/state; shell renders projections; correlation, idempotency, schema negotiation, bounded payloads, cancellation, liveness, and restart semantics are introduced |
| `OWNER` | Trusted Core owns protocol validation and state; Desktop owns presentation/transport only |
| `DEPENDENCIES` | P0-D2/D3/D5/D7, resolved repository-governance authority, Rust/Tauri toolchain and qualified local IPC selection |
| `DONORS` | Tauri shell/typed-IPC mechanics; Rust ecosystem components only after exact S1 acquisition records; prior handshake evidence as test oracle |
| `DISPOSITIONS` | `PACKAGE` or narrow `ADAPT` only after admission; reject Tauri ACL/IPC as Nawat authority; no broad source import |
| `TRUST` | Desktop/UI/webview and all incoming payloads are untrusted; minimal Core validation/state/receipts are trusted |
| `AUTHORITY` | Handshake conveys a principal-bound request; it grants no file/process/network/repository authority by connection alone |
| `DATA` | Health, version, capability descriptors, bounded request/event payloads; no secrets or project content required for the base handshake |
| `NETWORK` | `LOCAL_ONLY`; no hosted control plane; local transport endpoint authenticated/bound and origin constrained |
| `PLATFORM` | Windows-first with cross-platform compile/contract plan; IPC/path/encoding/restart behavior tested per OS |
| `FAILURE` | Version mismatch, spoofed/stale peer, duplicate/replayed request, oversized/malformed payload, partial response, crash/restart, cancellation race, backpressure, event loss |
| `NEGATIVE_TESTS` | Unknown command, schema downgrade, forged principal/correlation, duplicate effect, invalid origin, flood/oversize, Core unavailable, desktop crash, Core crash, stale socket/endpoint |
| `ACCEPTANCE` | Typed round-trip and cancellation succeed; malformed/unauthorized inputs fail closed; restart/reconnect preserves no false authority; evidence identifies exact binaries/protocol |
| `BENCHMARKS` | Startup/handshake latency, steady request latency/throughput, memory, backpressure, crash recovery, schema-validation and denial cost |
| `NON_GOALS` | Project open, terminal, AI worker, Fehrest, review, repair, completion, cloud sync |
| `DEFERRED` | Rich streaming UI, remote clients, collaboration, auto-update, generalized plugin transport |
| `EXPECTED_PATHS` | `apps/desktop/**`, `crates/core/**`, `crates/contracts/**`, `crates/ipc/**`, `tests/desktop_core/**` |
| `MIGRATION` | Versioned protocol envelopes; no silent downgrade; compatibility window explicitly bounded |
| `RECOVERY` | Restart/reconnect with correlation and idempotency reconciliation; stale endpoints removed safely; no in-flight request fabricated complete |
| `EXIT` | S1 evidence packet passes Spec Kit/Ponytail/Cubic policy, contract/security/negative/performance tests, accessibility baseline, and authorized review |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—P0 ratification, governance resolution, and specific S1 implementation authorization |

### 29.3 S2 — Open Project, Project Doctor, Local Identity and Storage

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Open an explicitly selected local project, identify it durably, diagnose readiness, and persist minimal local state without granting execution authority |
| `USER_VALUE` | The founder sees what project is open, why it is healthy/degraded/blocked, and how to recover without hidden mutation |
| `ARCHITECTURE_DELTA` | Adds Project identity, source/root observations, versioned local store, Doctor findings, storage migration/backup, and read-only discovery contracts |
| `OWNER` | Core Project/identity/storage modules own canonical local records; Doctor emits evidence; UI projects it |
| `DEPENDENCIES` | S1, P0 vocabulary/aggregate ownership, data-classification/retention rules, storage and filesystem component admission |
| `DONORS` | Git/filesystem/storage libraries and prior Project Doctor behavior only after exact admission; no external project object becomes truth |
| `DISPOSITIONS` | Prefer qualified packages for commodity parsing/storage; custom logic only for WePLD identity/authority invariants |
| `TRUST` | User-selected path is intent evidence, not proof; filesystem, repository metadata, config, symlinks/reparse points, and external files are untrusted observations |
| `AUTHORITY` | Open exposes bounded read discovery for the selected scope; write, install, execute, network, credential, and repository effect capabilities are structurally absent at S2. This is not a pre-Nawat authorization engine or policy grant and must not become a second authority point when Nawat appears |
| `DATA` | Local path identity, repository/worktree/ref observations, Doctor results, storage schema/version, classification and provenance; secrets excluded/redacted |
| `NETWORK` | `LOCAL_ONLY`; remotes recorded as strings/evidence without contact unless later separately authorized |
| `PLATFORM` | Windows path/reparse/ACL/UNC semantics plus cross-platform normalization; long paths, Unicode and case behavior tested |
| `FAILURE` | Missing/inaccessible/moved root, identity collision, repository corruption, reparse escape, stale observation, locked/corrupt store, migration interruption, disk full |
| `NEGATIVE_TESTS` | Root swap/TOCTOU, junction outside scope, malicious config, huge tree, binary/permission traps, stale ref, corrupt DB, interrupted migration, backup restore mismatch |
| `ACCEPTANCE` | Exact project identity and scope are stable/explainable; Doctor separates observation from decision; store migration is atomic/recoverable; no unauthorized write/exec/network occurs |
| `BENCHMARKS` | Open/scan latency by tree size, memory/I/O, cache correctness, change detection, Doctor precision/noise, migration/recovery time |
| `NON_GOALS` | Full Fehrest indexing, terminal execution, dependency installation, remote fetch, auto-fix, multi-project aggregation |
| `DEFERRED` | Cross-repository graph, shared/team storage, cloud sync, advanced watch/index services |
| `EXPECTED_PATHS` | `crates/project/**`, `crates/doctor/**`, `crates/storage/**`, `crates/identity/**`, `tests/project_doctor/**`, storage migrations |
| `MIGRATION` | Versioned schema with preflight, backup, forward migration and explicit unsupported downgrade |
| `RECOVERY` | Restore last valid store or rebuild projections from source-authoritative local state; quarantine corrupt records; preserve audit evidence |
| `EXIT` | Open/Doctor/store property, adversarial path, migration, recovery, performance and UI accessibility tests pass under approved method packet |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—separate S2 implementation authorization after S1 exit |

### 29.4 S3 — Terminal Fabric, Trusted Process Ownership, and Windows Qualification Foundation

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Provide a structured, principal-bound executor and PTY terminal with truthful process lifecycle, while building the evidence needed for bounded Windows confinement |
| `USER_VALUE` | Commands run visibly and cancellably; ownership, environment, limits, exit, and failure are explicit; no orphan is called complete |
| `ARCHITECTURE_DELTA` | Adds principal-bound `CommandRun` / `ProcessTreeRecord` execution records, launcher, structured argv/env/cwd, PTY adapter, output limits, cancellation, reconciliation, effect receipts, and Windows profile harness; no native `Attempt` is created in S3 |
| `OWNER` | Mission Runtime owns command/process lifecycle; Nawat owns capabilities/effect-time authorization; Terminal owns presentation; Core persists receipts; canonical `Mission`/`Task`/`Attempt` semantics remain for their later native slice |
| `DEPENDENCIES` | S2 identity/storage, P0-D4/D5, §21 protocol, Windows profile choice, accepted PTY/process components |
| `DONORS` | WezTerm `portable-pty` for PTY mechanics only; Codex Windows code as selective-port/test oracle; Windows APIs/windows-rs/HCS candidates after path-level audit |
| `DISPOSITIONS` | PTY behind WePLD launcher; port only admitted containment primitives; reject worktree/PTY/Tauri ACL as sandbox and reject WFP continue-on-failure |
| `TRUST` | Worker/command/shell/output/project files are untrusted; launcher, policy verification, minimal state and receipts are trusted; containment claim is profile-specific |
| `AUTHORITY` | Every spawn/effect requires principal, `CommandRun` identity, executable/argv/cwd/env digest, capability lease and budget; possession of terminal or credential is not authority |
| `DATA` | Commands, bounded environment, transcripts, exit/resource/containment evidence; secrets referenced by lease identity and redacted from logs |
| `NETWORK` | Denied by default; per-profile WFP/stronger substrate qualification required; enforcement failure aborts spawn |
| `PLATFORM` | Windows qualification foundation is mandatory; cross-platform adapters cannot dilute Windows properties; `cmd`, PowerShell, direct and ConPTY paths covered |
| `FAILURE` | Pre-launch partial setup, breakaway/orphan, token/ACL/WFP failure, handle/IPC leak, shell quoting, output/resource bomb, cancellation race, crash/reboot/stale state, teardown failure |
| `NEGATIVE_TESTS` | Full §21 matrix including elevation, reparse/TOCTOU/device/UNC, IPv4/IPv6/DNS/UDP/TCP/loopback/proxy, credentials, pipes/shared memory/ConPTY, bombs and reboot reconciliation |
| `ACCEPTANCE` | Structured execution and PTY lifecycle are truthful/idempotent; unqualified profiles make no sandbox claim; either a bounded Windows profile passes or Alpha remains no-untrusted-worker |
| `BENCHMARKS` | Spawn/interactive latency, throughput, output/backpressure, resource overhead, denial cost, cleanup/recovery time, containment false-allow/false-deny by profile |
| `NON_GOALS` | General autonomous worker, broad browser/computer control, arbitrary container orchestration, completion, review/repair |
| `DEFERRED` | Stronger VM/HCS/Hyper-V profiles, remote execution, multiplexer collaboration, generalized scheduler |
| `EXPECTED_PATHS` | `crates/execution/**`, `crates/terminal/**`, `crates/runtime/**`, `crates/nawat/**`, `crates/windows_containment/**`, `tests/windows_qualification/**` |
| `MIGRATION` | Profile/version IDs and launcher contracts; PTY provider replaceable; no persisted claim upgraded without requalification |
