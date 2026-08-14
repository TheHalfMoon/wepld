
### 37.0 Current Founder Ratification Packages

```text
CURRENT_FOUNDER_RATIFICATION_PACKAGES = 6
```

The current founder ratification workflow groups the answerable decisions without deleting or renumbering their underlying IDs:

1. **`RAT-01 Architecture ownership`** — recommend `Fehrest.Maemar`; ratify reconciled vocabulary/aggregate boundaries. Maps `FD-P0-001` + `FD-P0-006`.
2. **`RAT-02 Repository/IP posture`** — proprietary/Private posture; owner/admin containment and historical-exposure review before code publication. Maps `FD-P0-012`.
3. **`RAT-03 Historical/PR governance`** — PR #11 replacement-first then close superseded; PR #1 donor ledger/archive if needed then close superseded; immutable history plus namespaced ADR/supersession manifest. Maps `FD-P0-004` + `FD-P0-005` + `FD-P0-016`.
4. **`RAT-04 Windows execution scope`** — authorize bounded Windows containment qualification; `NO_UNTRUSTED_LOCAL_WORKER` until an approved profile passes. Maps `FD-P0-011`.
5. **`RAT-05 Roadmap`** — ten primary S1–S10 slices plus non-primary S3-D Assurance Seed gate. Maps `FD-P0-017`.
6. **`RAT-06 Runtime Verifier Alpha scope`** — WePLD-owned desktop/Core/terminal/project/review surfaces only; generalized external production/browser/computer verification Post-Alpha. Maps `FD-P0-022`.

`FD-P0-013` is retained below for traceability but classified `FUTURE_EVIDENCE_GATED_APPROVAL`: it cannot be answered before the component-specific evidence exists and is therefore not a current founder ratification package.

### 37.1 `FD-P0-001` — Maemar ownership and name

**Decision:** choose top-level bounded context, named Fehrest domain, or explicit split. **Recommendation:** `Fehrest.Maemar` with a mandatory capability register, retaining declared/implemented/build/runtime/deployment/supply-chain/target architecture, semantic structure, ownership/trust, decisions, impact and drift. **Consequence:** resolves architecture-context ownership without service proliferation; required before S4/S7 contract exit.

### 37.2 `FD-P0-004` — PR #11 supersession and closure

**Decision:** authorize the §23 replacement-first/cross-link/archive/close-superseded path or choose another durable disposition. **Recommendation:** replacement first, then close as superseded; do not merge unchanged or leave a stale draft as the governance marker. No action in this task.

### 37.3 `FD-P0-005` — PR #1 donor, archive, and closure

**Decision:** authorize exact salvage ledger, immutable archival reference where needed, successor links and closure as superseded. **Recommendation:** do so after evidence extraction; never wholesale merge/rebase. No action in this task.

### 37.4 `FD-P0-006` — Final vocabulary and aggregate ownership

**Decision:** ratify or amend §5–§10 names, owners and no-duplicate-truth rules, including Work/AGILLE/Mission Runtime and Mirefa/Edara/Nawat/UWC. **Recommendation:** ratify the reconciled logical boundaries while leaving exact technical schemas to P0 evidence work.

### 37.5 `FD-P0-011` — Windows qualification or no-untrusted-worker Alpha

**Decision:** require a bounded profile to pass §21 before Alpha worker execution, or explicitly ship Alpha with no untrusted local worker. **Recommendation:** fail closed to no-untrusted-worker until the bounded profile has adversarial evidence; do not weaken the profile to preserve schedule.

### 37.6 `FD-P0-012` — Private/Public governance and IP posture

**Decision:** reconcile the currently public repository with adopted proprietary/Private posture, including visibility, access, fork/history/secret review, publication and future contribution policy. **Recommendation:** establish an owner/admin session and approved containment plan before any implementation/code publication; do not assume changing visibility retroactively removes public exposure.

### 37.7 `FD-P0-013` — Component-specific S1 and S3-D admissions

**Classification:** `FUTURE_EVIDENCE_GATED_APPROVAL`, not a current founder ratification package. Accept/reject each actual component only after the §27 record exists, including platform/IPC/storage/process and deterministic review candidates. **Recommendation:** grant no blanket donor approval; make a narrow record per component/path/version and preserve replacement/exit strategy.

### 37.8 `FD-P0-016` — ADR/history namespacing and supersession

**Decision:** approve a generation-aware namespace/manifest and treatment of colliding historical sequences. **Recommendation:** immutable historical trees plus current namespace and explicit successor links as in §34; never renumber/rewrite history silently.

### 37.9 `FD-P0-017` — Corrected roadmap and S3-D

**Decision:** ratify ten primary slices S1–S10, non-primary S3-D and the dependency/authorization gates in §§28–30. **Recommendation:** ratify; keep Byan at S10 and first full native Review/Assurance at S7.

### 37.10 `FD-P0-022` — Runtime Verifier Alpha scope

**Decision:** choose bounded WePLD-owned surfaces, no Alpha verifier, or a separately justified wider profile. **Recommendation:** bounded WePLD desktop/Core/terminal/project/review surfaces only; third-party production/general browser/computer-use verification Post-Alpha.

---

## 38. Current Scoped Blockers

```text
CURRENT_SCOPED_BLOCKERS_COUNT = 2
```

### 38.1 `B-GOV-001` — Public repository vs proprietary/Private posture

**Evidence:** `wepld/wepld` is live Public. **Blocks:** repository implementation/code publication and any action that assumes the proprietary/Private posture is already enforced. **Does not block:** this read-only reconciliation or preparation of P0 governance/evidence artifacts outside repositories. **Resolution authority:** founder/owner-admin governance decision, with historical-exposure and access review.

The currently connected read-only evidence session is `IamShehri` (ID `285091250`) with `admin=false`; owner object `wepld` is ID `304164736`. This did not block read-only verification, but future owner/admin-only mutation must establish and reverify the proper session.

### 38.2 `B-WIN-001` — Unqualified Windows containment for untrusted local workers

**Evidence:** useful primitives and source oracles exist, but no complete adversarial profile proves the §21 properties; known fail-open/gap cases remain. **Blocks:** untrusted local worker execution and any claim that trusted tooling is safe over untrusted project content without a profile qualified for that input class. **Does not block:** P0 planning, contracts, acquisition work, deterministic tooling over inputs covered by its disclosed qualified profile, or a no-untrusted-worker Alpha. **Resolution:** pass an approved bounded profile or ratify the no-untrusted-worker Alpha fallback.

Direct V1.5 inspection closed the former evidence blocker. V1.5 ChangeStack evidence closed the former lineage blocker. Contract refinement, corpus design and component admission are P0 tasks, not additional current scoped blockers.

---

## 39. Required Next Founder Action

The next action is a read-only/recorded founder ratification pass over the six current packages in §37.0, preserving all ten historical decision IDs for traceability. `FD-P0-013` remains a future evidence-gated approval. Priority remains `RAT-02` / `FD-P0-012` because repository posture blocks code publication and `RAT-04` / `FD-P0-011` because it controls untrusted-local-worker eligibility. The ratification should:

1. record answers/dissent/deferrals for `RAT-01` through `RAT-06` and exact authority while retaining their underlying decision IDs;
2. approve or amend P0-D1–D7, the ten slices and S3-D, without pre-answering `FD-P0-013`;
3. decide whether a subsequent task is authorized to create P0 governance/specification artifacts and where, under the repository privacy decision;
4. grant no implementation/import/dependency/PR/settings authority unless separately explicit;
5. require a fresh live identity/permission/ref check immediately before any later GitHub mutation.

Until that action, the reports are planning evidence. They do not begin P0 mutation, S1 implementation, PR disposition, repository containment or source acquisition.

---

## 40. Final Verdict and State

```text
MASTER_PLAN_V2_2_READY_FOR_FOUNDER_RATIFICATION
```
