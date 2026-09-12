# S3 Source Acquisition Check

## Gate result

```text
CHECK_DATE = 2026-09-12
CHECK_SCOPE = S3_PLANNING_ONLY
TRUSTED_BASE_OID = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
SOURCE_REGISTRY_INDEX_GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
SOURCE_ACQUISITION_CHECK = COMPLETE_FOR_PLANNING_INPUT
SOURCE_IMPORT = NONE
SOURCE_ADMISSION = NONE
NEW_DEPENDENCY_ADMISSION = NONE
EXTERNAL_BINARY_EXECUTION_AUTHORITY = NONE
DONOR_EXECUTION_DURING_PLANNING = NONE
WINDOWS_API_BINDING = NONE
```

This check identifies behavior oracles and native/admitted machinery. It does not import donor code or grant implementation authority. Live GitHub base/head/check state must be re-read before canonical planning acceptance, exactly as `acceptance.md` requires.

## 1. Canonical registry — revision-bound

Registry input:

```text
PATH = docs/acquisition/SOURCE_REGISTRY_INDEX.md
TRUSTED_BASE_OID = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
BROAD_DISCOVERY = CLOSED
SOURCE_ADMISSION = NONE
```

The registry bytes are unchanged since S2's own acquisition check (same blob SHA). S3 uses capability-triggered source research only, targeted at the Windows process/containment boundary.

## 2. Native/admitted machinery

### Rust standard library

Official references:

- `https://doc.rust-lang.org/std/process/`
- `https://doc.rust-lang.org/std/process/struct.Command.html`

Relevant qualified behavior:

- `std::process::Command` can spawn a child process and control its stdio/environment/current directory, but the standard library alone does not expose Windows Job Objects, process-tree containment, or resource limits;
- `Child::kill` terminates the immediate child process only; it does not by itself terminate an entire process tree, which is exactly the gap `contracts/runtime-execution-fabric.md`'s containment/cancellation requirements exist to close;
- environment inheritance for a spawned child defaults to the parent's environment unless explicitly cleared, which is the opposite of the deny-by-default posture this package requires — any future implementation must explicitly clear/allowlist rather than rely on library defaults.

Role:

```text
RUST_STDLIB = NATIVE_BEHAVIOR_ORACLE + PARTIAL_IMPLEMENTATION_CANDIDATE
SOURCE_IMPORT = NONE
```

`std::process` alone is insufficient for the process-tree containment this package requires; a Windows-specific API surface (§3) is the actual qualification target.

### Existing WePLD serialization

Trusted-base manifests, unchanged from S2's acquisition check:

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

## 3. Windows Job Objects — primary containment oracle

Official references:

- `https://learn.microsoft.com/windows/win32/procthread/job-objects`
- `https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-createjobobjectw`
- `https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject`
- `https://learn.microsoft.com/windows/win32/api/winbase/nf-winbase-setinformationjobobject`
- `https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject`

Relevant qualified behavior:

- a Job Object groups one or more processes so operations (limits, termination) apply to the whole group;
- `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` terminates member processes when the *last* handle to the job closes — this guarantee applies only to processes that remain assigned to the job at that moment and only once every handle (not merely one) has closed; it is directly relevant to the "no orphaned process on ownership loss" property this package's ownership-epoch model needs, but only under those preconditions;
- a process can escape job membership ("breakaway") if the job and process were created with breakaway permitted, and `AssignProcessToJobObject` itself can fail (e.g., the target process is already in a job that disallows nested assignment); both a breakaway process and a failed assignment fall **outside** the kill-on-close guarantee — `ContainmentCapabilityReport`/`ContainmentPosture` must not report whole-tree containment without a native test proving assignment succeeded and breakaway was not permitted, and must fail closed to `NONE`/`UNKNOWN` on assignment failure;
- Job Objects natively bound process-tree membership (for processes that stay assigned) and can terminate the whole tree via `TerminateJobObject`, which is the qualification target for FR-013 (bounded cancellation covering the entire process tree) — but this too requires a native test proving termination reaches a child-of-child, not just the directly-assigned process;
- Job Objects do **not** by themselves provide filesystem or network isolation — this directly supports `constitution.md` C4/`spec.md` FR-006's rule that `PROCESS_TREE_ONLY != HARD_FILESYSTEM_ISOLATION`/`!= NETWORK_ISOLATION`;
- nested Job Objects and nested-job support vary by Windows version, which is exactly why `ContainmentCapabilityReport` must record `os_version_identity` and fail closed to `UNKNOWN` on an unrecognized version rather than assume nesting support.

`S3-AUTH-HOST` must not claim whole-tree containment (for `ContainmentPosture.process_tree_strength` or for FR-013's cancellation guarantee) without native Windows tests covering: last-handle closure (not merely the first), a breakaway-permitted child escaping the job, an `AssignProcessToJobObject` failure, and child-of-child cancellation. Any of these untested is an explicit `UNKNOWN`, not an assumed pass.

Acquisition decision:

```text
JOB_OBJECT_SOURCE_IMPORT = NONE
JOB_OBJECT_API_BINDING = NOT_GRANTED_BY_THIS_PLAN
JOB_OBJECT_ROLE = BEHAVIOR_ORACLE + PRIMARY_CONTAINMENT_QUALIFICATION_TARGET
FIRST_S3_SUCCESSOR_WINDOWS_API_AUTHORITY = NONE
```

If a later `S3-AUTH-HOST` successor selects an actual binding crate, it must separately qualify the exact crate/version (a candidate research question, not a decision this package makes): the official `windows` crate (Microsoft-maintained, MIT/Apache-2.0 dual-licensed) is the most likely qualified candidate over the older, less actively maintained `winapi` crate, but the exact choice, version, and feature set require their own admission gate — this package admits neither.

## 4. AppContainer / restricted tokens — recorded, not investigated

Official reference:

- `https://learn.microsoft.com/windows/win32/secauthz/appcontainer-isolation`

AppContainer offers stronger isolation than a Job Object alone but is a materially larger qualification surface (application-manifest requirements, capability SIDs, network isolation semantics). It is recorded here as a future investigation candidate only, per `clarify.md` Q7; this package does not claim it is evaluated or available.

```text
ROLE = FUTURE_INVESTIGATION_CANDIDATE
S3_CLAIM = NONE
```

## 5. Omnigent — research-only mechanism quarry

Per `contracts/runtime-execution-fabric.md`'s own source-acquisition note:

```text
DONOR = omnigent-ai/omnigent
ROLE = RESEARCH_ONLY_MECHANISM_QUARRY
SPECIFIC_VALUE = server/host/runner distinction; policy choke point; Bubblewrap/security
                 posture; environment allowlisting
SOURCE_ADMISSION = NONE
DONOR_EXECUTION = NONE
```

Bubblewrap-class sandboxing is a Linux-specific mechanism; it is noted here as a future oracle for Linux containment investigation (out of this package's Windows-first scope) rather than a current acquisition target.

## 6. OpenAI/Codex-style process safety architecture

Current process/sandbox/approval/network patterns from agent-execution products remain a useful process-boundary oracle for the PEP seam's eventual real policy engine (S6-N), not for anything this package implements.

```text
ROLE = FUTURE_S6_N_POLICY_ENGINE_ORACLE
S3_RUNTIME_USE = NONE
```

## 7. Database / distributed-coordination candidates

No database, distributed lock service, or message broker is required by this planning package. S3 is single-host; no cross-process/cross-host coordination problem exists yet that would justify one.

```text
STATUS = REJECT_INITIAL
RATIONALE = S3 needs a local ownership-epoch counter, not a distributed coordination system
```

## 8. Credential broker candidates

Not researched. `CredentialCapability` is entirely out of S3's scope per `clarify.md` Q9; no broker (Nango-class or otherwise) is relevant to this package.

## 9. License / provenance posture

No donor code is copied in this planning package. Behavior-oracle documentation is cited by public URL. Therefore:

```text
THIRD_PARTY_SOURCE_COPIED = NO
THIRD_PARTY_NOTICE_CHANGE = NONE
LICENSE_ADMISSION = NONE
SBOM_CHANGE = NONE
```

Any later source import (a Windows API binding crate, in particular) requires exact revision, license/NOTICE obligations, source review, tests/failure-mode review, security/maintenance/exit strategy, and canonical source admission before it is used.

## 10. Live verification boundary

Before this source check contributes to canonical planning acceptance, the acceptance workflow must re-read from GitHub:

```text
LIVE_CANONICAL_MAIN_SHA
LIVE_PR_BASE_SHA
LIVE_PR_HEAD_SHA
LIVE_DIFF_SCOPED_TO_THIS_PACKAGE
LIVE_FOUNDATION_STATE
LIVE_TRUSTED_BASE_ADMISSION_STATE
LIVE_REVIEW_THREADS_AND_REVIEW_STATE
```

This document cannot embed its own future commit SHA and must never pretend that this check's input head is the live repaired acceptance head.

## 11. Final acquisition decision

```text
USE_EXISTING_ADMITTED_CONTRACT_SERIALIZATION = YES_PREFERRED
WINDOWS_JOB_OBJECT_API = PRIMARY_QUALIFICATION_TARGET_FOR_S3_AUTH_HOST_NOT_ADMITTED_NOW
WINDOWS_API_BINDING_CRATE = LATER_S3_AUTH_HOST_ADMISSION_DECISION
APPCONTAINER = FUTURE_INVESTIGATION_CANDIDATE_NOT_ADMITTED
PROCESS_SPAWN_MECHANISM = LATER_S3_AUTH_SPAWN_ADMISSION_DECISION
NEW_DATABASE = NO
NEW_ASYNC_RUNTIME = NO
NEW_CREDENTIAL_BROKER = NO
NEW_SOURCE_IMPORT = NO
NEW_DEPENDENCY_ADMISSION = NO
```

Source Acquisition is complete for the planning/no-import boundary. Before any S3 implementation authority is granted, unresolved task-specific machinery (in particular, the exact Windows API binding crate) and current dependency/security state must be revalidated explicitly; this planning result never auto-admits them.
