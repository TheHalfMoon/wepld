# S3 Cross-Artifact Analysis

## Analysis result

```text
ANALYSIS_STATUS = INITIAL_PLANNING_CANDIDATE_COMPLETE_PENDING_EXACT_HEAD_REVIEW
INITIAL_REVIEWED_HEAD = NOT_YET_REVIEWED
MATERIAL_INTERNAL_CONTRADICTIONS = 0
IMPLEMENTATION_AUTHORITY = NOT_GRANTED
```

This is the first drafted candidate for the S3 planning package; it has not yet been through an independent exact-head review. "Complete" here means internally self-consistent and ready to submit for that review, not that a reviewer has accepted it. Any tracked repair after review creates a new head and invalidates prior head-bound qualification/review evidence, exactly as S2's own process required.

## 1. Constitution ↔ specification

The constitution's invariants map onto the specification's requirements:

- C1 (no network authority) → FR-016, and the fixed `NONE` values on `RunnerDescriptor.current_network_state`/`RuntimeCeiling.max_network_class`;
- C2 (explicit host opt-in) → FR-001, §4.2 `HostDescriptor`;
- C3 (identity separation) → FR-002, §4.1–4.3;
- C4 (multidimensional containment) → FR-004/FR-006, §4.5–4.6;
- C5 (Windows-native containment target) → FR-005, `plan.md` §4.1;
- C6 (runtime ceiling as hard upper bound) → FR-007, §4.7;
- C7 (deny-by-default environment) → FR-008, §4.8;
- C8 (PEP seam, not the engine) → FR-010/FR-011/FR-012, §4.10;
- C9 (bounded cancellation, local ownership/fencing prerequisite) → FR-013/FR-014, §4.4/§4.9–4.11;
- C10 (envelope shape, no effect authority) → §4.9–4.12, and the explicit exclusion of a Terminal/PTY feature;
- C11 (later slices, and S2-S003, stay in their proper place) → out-of-scope list, and §10's explicit adoption-not-implementation of `S2-S003`.

No specification requirement grants an effect forbidden by the constitution: every domain type that could plausibly be misread as effect authority (`PEPDecision.ALLOW`, `ContainmentPosture`) has an explicit `!=` invariant attached in both files.

## 2. Specification ↔ clarifications

The clarifications resolve every scope ambiguity the specification's domain model would otherwise leave open:

- Q1/Q2 confirm no working Terminal and no spawn authority is granted by this package;
- Q4 explicitly bounds `ProcessTreeIdentity` to WePLD-spawned process trees only, preventing scope creep into general process monitoring;
- Q5/Q11 bound the PEP seam to a narrow, policy-language-agnostic interface, never a real evaluator;
- Q6/Q7 defer all Windows API binding and stronger-than-Job-Object investigation;
- Q8/Q9/Q10 exclude distributed fencing, credentials, and harness adapters entirely, even though they share a contract file with S3's actual scope;
- Q12 prevents silent pre-consent containment profiling;
- Q13 defers numeric ceiling/timeout defaults to measurement rather than guessing;
- Q14/Q15 fix the reconciliation-is-a-new-record rule and the cancellation-scope requirement;
- Q16/Q17 restate the S2-established `REVIEW_BLOCKED` and planning-does-not-grant-implementation rules;
- Q18 fixes the staged-authority order;
- Q19 adopts `S2-S003` explicitly rather than leaving it unowned.

## 3. Specification ↔ plan

The plan uses the minimum existing architecture:

- new contract types live in `crates/contracts`, which already owns admitted serde/serde_json, exactly as S2's contracts did;
- no `crates/core` runtime behavior, Windows API binding, or process spawn is authorized by this package;
- the host/effect algorithm (plan §3) implements every FR in `spec.md` §5 in dependency order: opt-in before qualification, qualification before runner establishment, runner establishment before any proposal, proposal before PEP decision, decision before result;
- the process-spawn admission gate (plan §7) mirrors S2's Git-adapter Route A/B split precisely, including the explicit "not part of the first successor" boundary;
- the staged implementation-authority strategy (plan §10) mirrors S1's and S2's proven staged-admission pattern instead of one broad grant.

Potential implementation source paths remain intentionally unfrozen until the corresponding successor policy grants them, exactly as S2's plan required.

## 4. Source acquisition consistency

The Source Acquisition Check is bound to exact inputs:

```text
TRUSTED_BASE_OID = 28e42da95e4d6304f24c1d2513ebd40f6f1c483a
SOURCE_REGISTRY_INDEX_GIT_BLOB_SHA1 = 4a2fe363e0e66f7183e0221743258fcf558a3733
CURRENT_ACCOUNTED_NAMED_ENTRIES = 402
```

It records Windows Job Objects and Omnigent as research-only oracles, records the `std::process` gaps (single-process `kill`, ambient environment inheritance by default) the implementation must explicitly overcome rather than rely on, and admits no dependency, source, or Windows API binding. This is consistent with `ponytail.md` §9's rejection of admitting any binding crate during planning.

## 5. Authority analysis

### Planning authority

Canonical policy v68 grants creation/review/canonicalization of exactly this planning package under `specs/007-s3-terminal-fabric-trusted-process-ownership/`.

### Implementation authority

None.

### Preferred next transition

After planning is canonical and post-merge activation is proven, `S3-AUTH-C` is a **contracts-only** successor granting no Core runtime/Windows-API/process/network authority. Later successors separately bound read-only host/containment qualification (`S3-AUTH-HOST`), bounded observation (`S3-AUTH-OBSERVE`), and an optional process-spawn adapter (`S3-AUTH-SPAWN`).

### Process/network/provider authority

None during planning, and `NETWORK_AUTHORITY = NONE` for every stage this package specifies, including every future stage through `S3-AUTH-SPAWN`.

## 6. Cross-slice obligation analysis — `S2-S003`

S2's own acceptance gate (`acceptance.md` §H.1) could not be closed without native Windows `wepld-core` runtime execution, which did not exist anywhere in the canonical repository at S2's close. It explicitly named S3 planning as the expected next owner rather than leaving the obligation to drift unowned.

This package's own domain (Windows Job-Object investigation) independently requires exactly the precondition `S2-S003` was waiting on: real native Windows execution of `wepld-core`. This is not a coincidence this package manufactured to look tidy — the master plan named "Windows-native containment investigation" as S3's own deliverable before this analysis considered `S2-S003` at all (`plan.md` §11 cites the master plan and `contracts/runtime-execution-fabric.md` as the source of that requirement, independent of S2's carried obligation). The adoption in `spec.md` §10/`clarify.md` Q19 is therefore a genuine alignment, not a forced one: if `S3-AUTH-HOST` is implemented, native Windows CI execution becomes available as a side effect of S3's own goal, and S2's already-written fixtures become executable for real at that point without S3 rewriting them.

The honesty obligation this analysis flags for `tasks.md`/`acceptance.md`: if `S3-AUTH-HOST` is not reached during this slice, or is reached in a way that does not actually stand up native Windows CI execution (for example, if the qualified implementation approach turns out not to require full native execution), `S2-S003` must be explicitly re-recorded as still open for the next slice, exactly as S2 did. Silence would be a defect of the same shape `wepld-ledger-annotation-discipline` and BL-0022 (self-referential/moving-target staleness) already caught elsewhere in this repository's history — this package must not let that recur here.

## 7. Residual planning risks converted to tasks

1. exact contract source path allowlist for `S3-AUTH-C` must be frozen before that successor;
2. exact Windows Job-Object API surface and candidate binding crate must be researched at `S3-AUTH-HOST` time, not assumed now;
3. measured cancellation deadline/poll-interval defaults require actual Job-Object termination benchmarking;
4. exact `ownership_epoch` representation is an implementation decision within the semantic guarantee this package fixes;
5. `S2-S003` closure evidence (or its explicit re-carry) must be recorded no later than this package's own acceptance;
6. the concrete narrow self-test PEP evaluator rule set, if specified at all, must be reviewed for accidental over-permissiveness before any contract test relies on it.

These are explicit tasks/acceptance gates in `tasks.md`/`acceptance.md`, not hidden assumptions.

## 8. Plan-in-repository verification

The repository planning package contains the execution path itself rather than relying on chat state:

- `plan.md`: architecture, host/effect algorithm, containment-qualification approach, PEP-seam plan, process-spawn admission gate, staged authority, delivery sequence;
- `tasks.md`: planning-package tasks plus the staged post-planning implementation task map;
- `acceptance.md`: immutable evidence gates, domain acceptance, and the `S2-S003` disposition;
- `clarify.md`: frozen design decisions, including the `S2-S003` adoption;
- `source-acquisition.md`: revision-bound machinery/oracle decisions;
- `threat-model.md`: adversarial rationale/tests;
- `ponytail.md`: why the selected mechanisms are minimum sufficient rather than overbuild.

## Conclusion

This initial candidate is internally consistent: every constitutional invariant is reflected in a functional requirement, every functional requirement is reflected in the domain model or an explicit deferral, and the one cross-slice obligation this package is required to address (`S2-S003`) is genuinely adopted rather than merely mentioned. It remains a **candidate** until it passes fresh exact-head deterministic qualification, trusted-base admission, egress preflight, independent review, finding reconciliation, Ready-triggered admission, guarded merge, and post-merge canonical verification. It grants no S3 implementation authority.
