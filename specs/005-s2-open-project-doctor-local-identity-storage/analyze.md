# S2 Cross-Artifact Analysis

## Analysis result

```text
ANALYSIS_STATUS = REPAIRED_PLANNING_CANDIDATE_COMPLETE_PENDING_FRESH_EXACT_HEAD_REVIEW
INITIAL_REVIEWED_HEAD = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
INITIAL_ACTIONABLE_FINDINGS = 9
INITIAL_FINDINGS_RECONCILED_IN_CANDIDATE_TEXT = 9
FRESH_REREVIEW_ACCEPTANCE = REQUIRED
MATERIAL_INTERNAL_CONTRADICTIONS = 0
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

“Reconciled in candidate text” means the plan/spec/contracts now contain a coherent repair. It does **not** mean an independent reviewer has accepted the repaired head. Any tracked repair invalidates old exact-head qualification/review evidence.

## 1. Constitution ↔ specification

The constitution requires local-first behavior, layered identity, serialized first-open reservation, generation-consistent evidence, bounded inspection/locking, secret-safe output, evidence/authority separation, explicit CLI modes, and no later-slice pull-forward.

The specification maps those invariants to requirements:

- C2 → FR-002/FR-013 and SR-002;
- C3/C4 → FR-003/FR-005/FR-009/FR-010/FR-011/FR-032;
- C5 → FR-006 and SR-001;
- C6 → FR-003/FR-004 and SR-004;
- C7 → FR-014..FR-017/FR-023/FR-031 and SR-007;
- C8 → FR-018..FR-026 and SR-008;
- C9 → FR-025..FR-029 and SR-009;
- C10 → FR-020/FR-022 plus NFR-001/NFR-006;
- C11 → explicit out-of-scope and authority boundaries.

No specification requirement grants an effect forbidden by the constitution.

## 2. Specification ↔ clarifications

The clarifications now freeze all planning decisions needed to remove the initial review gaps:

- non-Git support is explicit;
- canonical path is not identity;
- no global Git ID is invented;
- worktrees remain distinct contexts;
- local store remains outside the repo;
- Git execution is a separately governed adapter decision;
- Doctor does not execute builds/tests/installers;
- remote URLs are advisory and sanitized;
- S4 graph and full `why` remain later;
- unknown CLI tokens never become prompts;
- first-open identity uses a store-wide `reserved|initialized` catalog protocol;
- project state uses immutable generations and one atomic `CURRENT` selection boundary;
- lock acquisition is non-blocking/bounded/cancellable with 2000ms/25ms planning defaults;
- baseline descriptor discovery uses a closed exact allowlist and 32 / 1 MiB / 4 MiB / depth-64 limits;
- Doctor TTY/JSON prose is template-based and cannot interpolate raw secret-bearing inputs;
- reviewer unavailability is `REVIEW_BLOCKED`, never PASS;
- contracts-only is the preferred first implementation-authority successor.

## 3. Specification ↔ plan

The plan uses the minimum existing architecture while now solving the reviewer-identified correctness gaps:

- serializable contract types remain in `wepld-contracts`, which already owns admitted serde/serde_json dependencies;
- Core project/evidence logic remains Rust-first;
- first-open allocation uses one small catalog coordination surface rather than introducing a database;
- project writes use immutable generations + a small `CURRENT` selector instead of independently mutable current files;
- `std::fs::File::try_lock`-style bounded coordination is preferred, with no PID-lock ownership invention;
- Git remains a bounded later external-process candidate, not an implicit first-tranche dependency;
- S2 Doctor remains deterministic/rule-based and now has one secret-safe projection model;
- CLI human/JSON output remains projection over shared contracts;
- descriptor discovery is closed, root-only, and bounded.

Potential implementation source paths remain intentionally unfrozen until the corresponding successor policy grants them.

## 4. Source acquisition consistency

The Source Acquisition Check is now bound to exact inputs:

```text
TRUSTED_BASE_OID = 46b1fc423f3fc5175d79acaf0f134747bf0d90f0
SOURCE_CHECK_INPUT_HEAD_OID = 4a9b3566c74818c6b53a4ac4026b3a4937678d2e
SOURCE_REGISTRY_INDEX_GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
```

It also records research issues #211–#214 as non-authoritative task-specific evidence. No donor code, package, service, binary, or model is admitted.

Existing `uuid 1.24.1` / `sha2 0.10.9` lock presence is explicitly not direct Core dependency admission. File-backed catalog/generation design remains the minimum until deterministic evidence disproves it.

## 5. Authority analysis

### Planning authority

Canonical v21 grants creation/review/canonicalization of exactly this eleven-file package.

### Implementation authority

None.

### Preferred next transition

After planning is actually canonical and post-merge activation is proven, S2-AUTH-C is a **contracts-only** successor. It grants no Core filesystem/process/network/model authority. Later successors separately bound locator/identity/evidence Core behavior, optional Git process effects, and Doctor/CLI projections.

### Process authority

None during planning. The Git adapter remains a later candidate only.

### Network/provider authority

None.

## 6. Initial review finding-by-finding reconciliation

### R1 — exact base/main evidence

**Finding:** acceptance text said base equals canonical main without requiring recorded SHAs.

**Repair:** `acceptance.md` now requires exact live PR base SHA and exact trusted canonical `main` SHA, recorded and equal immediately before qualification/acceptance.

### R2 — reviewer qualification / REVIEW_BLOCKED

**Finding:** independent-review requirement lacked explicit evidence/unavailability semantics.

**Repair:** acceptance defines reviewer identity/product, qualification, independence, exact base/head coverage, completion state, findings, and `REVIEW_BLOCKED`/stale states. Blocked/pending cannot satisfy acceptance.

### R3 — incomplete planning completion rule

**Finding:** constitution omitted trusted-base admission, egress, race checks, Ready-triggered admission, and complete pre/post merge verification.

**Repair:** constitution and acceptance now enumerate every gate and preserve candidate-policy non-authority before trusted activation.

### R4 — first-open identity race

**Finding:** per-project lock is selected after project ID and cannot serialize first allocation.

**Repair:** catalog lock/reservation precedes project lock. Reservation is durable `reserved|initialized`; recovery reuses the same ID. Lock order is fixed catalog → project.

### R5 — mixed multi-file state after crash

**Finding:** independent `identity/index/evidence` replacement could create mixed valid-looking state.

**Repair:** immutable project generations + manifest + atomic small `CURRENT` selector. Readers read one current generation only; orphan/incomplete generations never become current by inspection.

### R6 — indefinite file-lock wait

**Finding:** blocking lock could hang commands indefinitely.

**Repair:** plan freezes non-blocking polling with default 2000ms acquisition deadline, 25ms interval, cancellation checks, typed busy errors, OS lock ownership, no PID-lock takeover.

### R7 — unbounded descriptor examples

**Finding:** open-ended descriptor categories lacked allowlist/byte/count/depth bounds.

**Repair:** exact root descriptor and presence-only marker lists plus 32 candidates, 1 MiB/file, 4 MiB aggregate parsed bytes, depth 64, no recursive baseline discovery.

### R8 — source registry not revision-bound

**Finding:** registry state had no trusted-base/head/blob binding.

**Repair:** Source Acquisition records trusted-base OID, source-check input head OID, exact registry blob SHA, and requires live PR/check reread for final acceptance.

### R9 — secret leakage through Doctor output

**Finding:** privacy covered storage but not finding prose/TTY/JSON values.

**Repair:** spec/plan/threat model define WePLD-owned text templates, opaque evidence refs, closed safe parameters, shared TTY/JSON redaction, and adversarial secret/control-character tests.

## 7. Identity-model analysis

A single canonical path would fail on moves, linked worktrees, symlink/junction changes, Windows path representations, mount changes, and Git common-dir/worktree distinctions. Remote URL/current HEAD are also insufficient.

The layered identity model remains minimum sufficient, but concurrency requires one additional correctness mechanism: **first-open reservation must serialize before ID-specific storage exists**. This does not turn the catalog key into global repository identity; it is a versioned local coordination key over revalidated matching facts.

## 8. Evidence-store sufficiency analysis

A naïve mutable multi-file directory was insufficient after independent review. The minimum corrected file-backed design is:

```text
small versioned catalog + OS catalog lock
immutable project generations
manifest per generation
small atomic CURRENT selector
OS project lock
bounded parsing and recovery
```

This solves first-open and mixed-generation correctness without introducing a general database/query engine. Database acquisition remains deferred unless platform implementation evidence proves this design insufficient.

## 9. Locking/availability analysis

OS file locking coordinates participating WePLD writers but is not a filesystem security boundary. Blocking forever is inconsistent with a stable command plane. The plan therefore selects bounded `try_lock` polling and typed busy outcomes.

Lock-file existence, PID content, or arbitrary stale-file deletion is not ownership. Platform qualification must prove the actual lock release/interaction semantics claimed.

## 10. Doctor/output privacy analysis

Escaping terminal controls alone is insufficient: a perfectly escaped token is still a leaked token. Therefore output safety has two independent layers:

1. **semantic release policy:** only WePLD-owned templates + allowlisted safe parameters may enter findings;
2. **presentation escaping:** any allowed untrusted display value such as a path is escaped for its target surface.

TTY and JSON consume the same semantic release model so machine mode cannot bypass redaction.

## 11. Descriptor/performance analysis

A fixed root allowlist and fixed byte/count/depth limits make baseline Doctor work independent of repository file count and prevent recursive manifest expansion. Presence-only lock markers are sufficient for package-manager ambiguity at this slice; deeper workspace/member parsing is capability-triggered later.

## 12. Git-trust/process analysis

Git's `safe.directory` remains protected. Any future Git adapter preserves protected trust config, scrubs runtime/repository-redirection environment injection, invokes a resolved qualified executable, uses exact bounded argv with `--no-optional-locks`, and has no network/hooks/general shell authority.

This adapter is intentionally **not** part of the contracts-only first successor.

## 13. Residual planning risks converted to tasks

1. per-platform data-root acquisition mechanism must be frozen before Core implementation;
2. lossless machine path representation must be frozen/tested per platform;
3. direct UUID/SHA-256 edges need exact dependency admission if Core requires them;
4. Git executable/environment contract needs separate authority/security qualification;
5. directory-entry/power-loss durability differs by platform and must remain measured/explicit;
6. identity reassociation thresholds require adversarial fixtures;
7. exact CLI numeric exit-code compatibility must reconcile S1 conventions;
8. macOS qualification may remain an explicit blocker/limitation where required;
9. the 2000ms lock deadline may require evidence-backed later tuning but cannot degrade into unbounded wait.

These are explicit tasks/acceptance gates rather than hidden assumptions.

## 14. Plan-in-repository verification

The repository planning package now contains the execution path itself rather than relying on chat state:

- `plan.md`: architecture, store protocol, exact descriptor bounds, output policy, staged authority, delivery sequence;
- `tasks.md`: planning reconciliation, contracts-first successor, identity/store/Doctor/CLI/security/platform tasks;
- `acceptance.md`: immutable evidence gates and product acceptance;
- `clarify.md`: frozen design decisions;
- `source-acquisition.md`: revision-bound machinery/donor decisions;
- `threat-model.md`: adversarial rationale/tests;
- `ponytail.md`: why the selected mechanisms are minimum sufficient rather than overbuild.

Issues #211–#214 are supporting research evidence only; they are not required to reconstruct the canonical implementation plan after this package is merged.

## Conclusion

The repaired package is internally consistent and materially stronger than the initial reviewed head. It remains a **candidate** until the repaired exact head passes fresh deterministic qualification, trusted-base admission, fresh egress/rereview, reconciliation, Ready-triggered admission, guarded merge, and post-merge canonical verification. It grants no S2 product implementation authority.
