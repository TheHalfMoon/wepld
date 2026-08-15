# WePLD Current State

**Checkpoint date:** 2026-08-15 Asia/Riyadh  
**Canonical repository:** `TheHalfMoon/wepld`

This file is durable continuation memory, not live-state authority. Before any write, review, admission, acceptance, or merge, re-read the live GitHub PR head/check/review state. Repository canonical memory outranks chat memory.

## Repository identity

```text
REPOSITORY_ID = 1334408699
OWNER = TheHalfMoon
DEFAULT_BRANCH = main
VISIBILITY = public
```

## P0 — accepted and merged

```text
P0 = Fresh Foundation
PR = #2
FOUNDER_ACCEPTED_HEAD = b67fc1be0e505b7cbd1adf286c6a26db9da9c95c
FOUNDER_ACCEPTANCE_COMMENT = 5303860663
FOUNDATION_INTEGRITY = PASS
FOUNDATION_INTEGRITY_RUN = 31901805621
FOUNDATION_INTEGRITY_RUN_NUMBER = 121
INDEPENDENT_EXACT_HEAD_REVIEW = SATISFIED
UNRESOLVED_MATERIAL_FINDINGS_AT_ACCEPTANCE = 0
MERGE_COMMIT = 6eff72319cad99c878a80f0d5bce9f107d213679
P0_STATE = MERGED / CANONICAL
```

P0 acceptance was exact-head bound. The merge does not waive later-slice qualification requirements.

## Standing founder authority

PR #2 comment `5303875093` records standing founder authorization to continue WePLD without repeated per-gate approval requests.

```text
FOUNDER_STANDING_AUTHORIZATION = GRANTED
```

It authorizes governed execution, branches, commits, PRs, reviews, bounded repair, qualified source/dependency admission, Ready transitions, merges, and roadmap continuation when canonical conditions are satisfied.

It is **not** a bypass for Spec Kit, Ponytail FULL, Source Acquisition Check, deterministic gates, applicable security review, independent engineering review, finding reconciliation, exact-head evidence, AMAN/Nawat/containment/egress invariants, or Trusted Completion.

```text
Authority != Qualification
Permission != PASS
```

## Active slice — S1

```text
SLICE = S1
NAME = Desktop ↔ Rust Trusted Core Handshake
BRANCH = feat/s1-desktop-rust-core-handshake
PR = #3
PR_STATE_AT_CHECKPOINT = OPEN / DRAFT
BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
INITIAL_PLANNING_HEAD = b114fc503c5fba17072b2870612815fd07cc8c8c
INITIAL_PLANNING_TREE = e33e28d694deb0c48f778cc445b12df7a8698573
INITIAL_PLANNING_INTEGRITY_RUN = 31905016507
INITIAL_PLANNING_INTEGRITY_RUN_NUMBER = 122
INITIAL_PLANNING_INTEGRITY = PASS
```

The live PR #3 head after this checkpoint commit must be read from GitHub; do not copy `INITIAL_PLANNING_HEAD` forward as live authority.

### S1 canonical target

Establish one typed, versioned, observable local channel between a Tauri Desktop process and a **separate Rust Trusted Core process**.

Required properties include health/version/capability negotiation, bounded framing, correlation, duplicate/replay handling, events, cancellation, fail-closed malformed/unauthorized input, restart/reconnect without false authority or fabricated completion, exact build/protocol evidence, and Windows-first runtime qualification.

S1 non-goals include project opening, terminal execution, AI workers, Fehrest, native review/repair systems, cloud control, generalized plugin transport, and S3 hostile-worker containment.

## S1 planning / method state

Active Spec Kit directory:

`specs/001-desktop-rust-trusted-core-handshake/`

It contains constitution, spec, clarifications, plan, requirements checklist, provisional task decomposition, analysis, final tasks, threat model, Ponytail FULL record, Source Acquisition preflight, and acceptance contract.

```text
SPEC_KIT_PLANNING = COMPLETE_FOR_CURRENT_SCOPE
PONYTAIL_FULL = COMPLETE_FOR_PLANNING
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
SOURCE_IMPORT = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
```

Spec Kit upstream is pinned as a development-method reference at `github/spec-kit@bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`. Its current command order differs from WePLD's canonical order, so S1 explicitly uses a compatibility sequence with provisional tasks before analysis and corrected/final `tasks.md` after analysis. Upstream tool behavior does not override repository authority.

Ponytail source is pinned at `DietrichGebert/ponytail@2ed6c52c9d7e5e56942508591085fd45dea277d3`, `skills/ponytail/SKILL.md` blob `02c0712c86277d49d18a77da3a2b825657bf02d1`.

## S1 current architecture decisions

```text
TRANSPORT_PREFERENCE = inherited child stdin/stdout anonymous pipes
HANDSHAKE_RUNTIME_NETWORK = NONE
PROTOCOL_V1_FRAMING = 4-byte big-endian payload length + UTF-8 JSON payload
LENGTH_PREFIX_BYTES = 4
MAX_PAYLOAD_BYTES = 65536
MAX_WIRE_FRAME_BYTES = 65540
PROTOCOL_PRINCIPAL = desktop_host
CONNECTION_GRANTS_AUTHORITY = NO
TAURI_ACL_IS_NAWAT_AUTHORITY = NO
```

`HANDSHAKE_RUNTIME_NETWORK = NONE` applies only to the S1 Desktop ↔ Core handshake runtime boundary. It is not a repository-wide prohibition on network capabilities that later slices may separately specify, qualify, and authorize.

For protocol v1, the 4-byte prefix encodes **payload length**. A declared payload length greater than `65_536` is rejected before payload allocation/read/deserialization. The largest complete wire frame is therefore `65_540` bytes (`4 + 65_536`).

Ponytail currently rejects unnecessary base-S1 machinery:

```text
TCP/localhost service = REJECT
General RPC framework = REJECT
Direct Tokio dependency in Core = REJECT
UUID/random-ID package = REJECT
React/Vite/Tailwind/frontend package manager = REJECT
Database/network/telemetry package = REJECT
Tauri shell plugin = REJECT_INITIAL / REFERENCE_ONLY
```

`tauri-plugin-shell` may be reconsidered only through a new explicit acquisition decision if direct stdlib launch of the packaged Core is proven insufficient. No silent fallback is allowed.

## S1 component candidates — not yet admitted

Current acquisition pins include:

```text
Rust = 1.97.1 / release commit 8bab26f4f68e0e26f0bb7960be334d5b520ea452
Tauri = 2.11.5 / 7cd71369c00978a3783b6ae3e9972358abbe4ae6
Tauri-build = 2.6.3 at the same Tauri source commit
Serde = 1.0.229 / 7fc3b4c30c94f73a96ebd1553f2b090d928fc3a8
serde_json = 1.0.151 / de8500740cdcabffb9734f503e4889def823cf10
```

These are **candidate identities**, not admitted runtime dependencies. Final admission requires the resolved lockfile, feature inventory, SBOM, advisory reconciliation, exact dependency-register state, minimum capability surface, and replacement/exit strategy.

## Foundation CI transition

The current P0 `foundation-integrity` workflow intentionally rejects implementation-language files and dependency manifests. That is correct for P0 but incompatible with S1 implementation.

S1 must first migrate it to a stage-aware integrity gate that preserves:

- immutable P0 canonical archive / V2.2 identity;
- frozen 402-source restoration evidence unchanged;
- zero unauthorized source/dependency admission;
- symlink/gitlink/repair-payload protections;
- explicit S1-only phase/path/admission rules;
- rejection of later-slice implementation;
- hosted reviewer manual pre-egress control.

The workflow change is security-relevant and requires applicable exact-head security coverage. Broadly deleting or weakening P0 protections is prohibited.

## Hosted reviewer egress controls

Repository configuration paths:

- `.coderabbit.yaml`
- `cubic.yaml`
- `.github/workflows/foundation-integrity.yml`
- `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`

The current S1 planning contract is fail-closed and explicit:

```text
CODERABBIT_AUTO_REVIEW = false
CODERABBIT_AUTO_INCREMENTAL_REVIEW = false
CODERABBIT_REVIEW_WHEN_USED = MANUAL_EXACT_SCOPE_AFTER_RECORDED_PREFLIGHT

CUBIC_REVIEWS_ENABLED = false
CUBIC_INCREMENTAL_COMMITS = false
CUBIC_CHECK_DRAFTS = false
CUBIC_PR_DESCRIPTION_GENERATION = false
CUBIC_AUTO_APPROVE = disabled
CUBIC_ULTRAREVIEW = disabled
CUBIC_AUTO_ULTRAREVIEW = disabled
CUBIC_THREAD_AUTO_RESOLUTION = false
CUBIC_FIX_WITH_CUBIC_BUTTONS = false
CUBIC_PR_COMMENT_FIXES = false
CUBIC_FIX_COMMITS_TO_PR = false
CUBIC_PROVIDER_EFFECTIVE_STATE = NOT_PROVEN
```

`foundation-integrity` verifies the checked-out repository-configuration bytes against the approved profile. That proves repository-file state only. It does **not** prove Cubic accepted the YAML or that provider/dashboard-effective settings match it. Cubic must remain `BLOCKED/NOT_RUN` as a reviewer until separate provider-effective evidence exists; no Cubic output may be counted as PASS merely from the repository file.

PR #3 comment `5303961793` records the historical automatic Cubic PR-description egress-order incident. Hosted review after that incident is manual and exact-scope only after the canonical pre-egress classification/screening/approval record. CodeRabbit review evidence is always bound to the exact reviewed head; a changed head invalidates the prior review for acceptance purposes.

## Architecture state

```text
MASTER_PLAN = V2.2
MASTER_PLAN_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
RAT-01..RAT-06 = APPROVED
ROADMAP = P0 + S1..S10
NON_PRIMARY_GATE = S3-D
BROAD_DISCOVERY = CLOSED
PATH_LEVEL_ACQUISITION = CAPABILITY_TRIGGERED
```

Canonical artifact archive:

```text
docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz
ARCHIVE_SHA256 = 35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0
MASTER_PLAN_MEMBER_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
FROZEN_REGISTRY_V1_ACCOUNTED_ENTRIES = 402
```

The frozen 402 registry remains restoration evidence. New donor discoveries/enrichments do not silently rewrite it.

## Canonical owners

```text
Work = durable coordination
AGILLE = engineering rigor
Mission Runtime = execution truth
Mirefa = capability / route qualification
Edara = staffing + minimum-sufficient topology
Nawat = authority grants + revalidation
Fehrest = governed Project Brain / context
Fehrest.Maemar = architecture-intelligence domain
AMAN = security / risk evidence
UWC = normalized worker edge
Assurance = independent evaluation
Trusted Completion = what may count complete
Byan = learns from outcomes without authorizing
```

## Mandatory build method

```text
Spec Kit
-> Ponytail FULL
-> Source Acquisition Check
-> minimum sufficient implementation
-> deterministic gates
-> independent correctness / engineering review
-> security-specialist review when applicable
-> finding reconciliation
-> bounded repair
-> rerun affected gates
-> rereview material changes
-> authorized exact-head acceptance
-> Build Learning capture
```

At least one independently qualified correctness/engineering review is required before acceptance of material work. Reviewer-product unavailability is not PASS. Codex Security supplements deterministic security coverage and does not replace correctness review or Trusted Completion.

## Security / claim boundaries

```text
CHILD_PROCESS_RELATIONSHIP != CONTAINMENT
ANONYMOUS_PIPE != CRYPTOGRAPHIC_AUTHENTICATION
PRINCIPAL_LABEL != NAWAT_GRANT
TAURI_ACL != CORE_AUTHORITY
PROTOCOL_VALIDATION != WINDOWS_SANDBOX
LOCAL_REVIEWER_CONFIG_VALIDATION != PROVIDER_EFFECTIVE_STATE
COMPILE_SUCCESS != RUNTIME_QUALIFICATION
SECURITY_REVIEW_CLEAN != COMPLETION
```

Windows hostile-worker containment remains future evidence-gated work. S1 may measure child lifecycle and orphan behavior but must not claim S3 process ownership/containment without matching evidence.

## Historical repository

`wepld/wepld` remains a historical quarry only. Concepts/tests/failure corpora may be salvaged only through bounded acquisition/salvage review. Do not inherit the former architecture wholesale.

## New-chat bootstrap

```text
Continue WePLD.
Repository: TheHalfMoon/wepld

Read AGENTS.md first, then docs/canonical/CURRENT_STATE.md, then the remaining mandatory canonical documents and active Spec Kit directory.
Verify live PR #3 head/check/review state before any mutation.
Treat repository canonical documents as authority over chat memory.
Standing founder authorization permits governed continuation without repeated approval requests; it does not waive gates.
Speak Arabic to the founder. Write repository artifacts and ready-to-use technical prompts in English.
```

## Next gate

1. finish PR #3 exact-head finding reconciliation and rerun `foundation-integrity` plus independent exact-head review;
2. close/merge the S1 planning baseline only when the exact head is clean and repository merge conditions are satisfied;
3. execute S1-003: stage-aware foundation-integrity migration while tree is still planning-only;
4. security-review/reconcile that workflow-trust change;
5. execute S1-004 bounded dependency-resolution bootstrap only after S1-003 is validated;
6. generate/reconcile lockfile, feature tree, SBOM and advisory evidence;
7. complete S1-005 component admission / `SOURCE_ACQUISITION_CHECK = PASS`;
8. only then begin S1 product implementation.
