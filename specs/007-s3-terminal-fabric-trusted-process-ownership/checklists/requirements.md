# S3 Requirements Checklist

## Authority and scope

- [x] S3 planning authority is explicitly separated from implementation authority.
- [x] Candidate governance/planning text cannot self-authorize before trusted-base merge/activation.
- [x] Source admission remains none.
- [x] Dependency admission remains none.
- [x] Product/runtime authority remains none during planning.
- [x] First post-planning successor is contracts-only by default.
- [x] Process-spawn authority is deferred to a later separate gate.
- [x] Distributed/multi-host runner fencing is excluded.
- [x] Credential brokering is excluded.
- [x] Harness/worker protocol adapters are excluded.
- [x] Native desktop bridge capability is excluded.
- [x] S3-D (deterministic assurance seed) is excluded as a separate gate.
- [x] `S2-S003` (Windows junction/reparse native-runtime coverage, `EXPECTED_NEXT_OWNER = S3_PLANNING`) is explicitly adopted, not left unowned (`clarify.md` Q19).
- [x] S4 Fehrest/semantic graph is excluded.
- [x] S6 Mission Runtime/UWC/full Nawat policy engine is excluded.
- [x] Agents/models/providers are excluded.
- [x] Network access is excluded.

## Domain/contract requirements

- [x] `ServerDescriptor`/`HostDescriptor`/`RunnerDescriptor` identity separation is specified.
- [x] Explicit, default-off host execution opt-in is specified.
- [x] `ProcessTreeIdentity` distinguishes OS PID from durable ownership (PID-reuse detection).
- [x] Ownership-epoch / stale-owner refusal is specified for a single local host.
- [x] `ContainmentCapabilityReport` is a discovery-time, multidimensional artifact, never a boolean.
- [x] Windows Job-Object-class investigation is the primary containment target.
- [x] `RuntimeCeiling` intersection rule (never union) is specified.
- [x] `EnvironmentExposurePolicy` deny-by-default shape is specified.
- [x] `EffectProposal`/`PEPDecision`/`EffectResult` closed-enum envelope shapes are specified.
- [x] The PEP seam fails closed (`UNKNOWN_FAIL_CLOSED`) on missing/stale/malformed policy input.
- [x] The PEP seam is explicitly not the effect-time policy engine.
- [x] Bounded cancellation covering the entire process tree is specified.
- [x] `EffectDependency` prerequisite/dependent ordering and unknown-outcome blocking are specified.
- [x] Revalidation triggers that stale a frozen envelope/decision are enumerated.
- [x] Reconciliation of an `UNKNOWN` outcome is a separate evidenced effect, never an in-place rewrite.

## Security

- [x] Repository-controlled content cannot influence `PEPDecision.decision_source` or widen a `RuntimeCeiling`.
- [x] `SPAWN_PROCESS_TREE`, if ever admitted, requires a closed allowlisted argv shape, never a shell string.
- [x] `ContainmentPosture` cannot be populated from a vendor/provider self-reported `sandboxed` boolean.
- [x] PID-reuse misattribution is represented and requires a fixture.
- [x] Cancellation/timeout paths are bounded so an untrusted/hung process cannot force an indefinite wait.
- [x] No raw environment value or unredacted process output may appear in durable evidence.
- [x] Unrecognized/unsupported OS or containment-backend versions fail closed to `NONE`/`UNKNOWN`.

## Portability

- [x] Windows-first qualification is explicit.
- [x] Linux/macOS containment claims are explicit evidence, never inferred from the Windows result.
- [x] Cross-platform gaps are recorded as explicit limitations, not silently absent from the matrix.

## Source Acquisition / Ponytail

- [x] No Rust crate for Windows Job-Object binding, process spawning, or any Windows API is admitted by this plan.
- [x] `contracts/runtime-execution-fabric.md`'s Omnigent source-acquisition note is treated as research-only, not an admission.
- [x] Contracts-first is justified as minimum correctness machinery, not scope creep.
- [x] Database, async runtime, agent framework, distributed-fencing, credential broker, and model-provider execution remain rejected for S3 minimum.

## Build method / planning content

- [x] Constitution complete.
- [x] Specification complete.
- [x] Clarifications complete.
- [x] Plan complete and contains a staged post-planning authority/delivery sequence.
- [x] Checklist complete.
- [x] Analyze complete for the initial planning candidate (pending exact-head review).
- [ ] Tasks ledger contains explicit implementation/review tasks for every material finding.
- [x] Ponytail FULL complete for the initial planning candidate.
- [x] Source Acquisition Check complete for the planning/no-import boundary.
- [x] Threat model covers host-opt-in bypass, containment-badge misrepresentation, PID reuse, stale-epoch effect injection, PEP fail-open regressions, and cancellation DoS.
- [x] Acceptance contract includes exact base/main, reviewer qualification, `REVIEW_BLOCKED`, race, Ready-triggered admission, guarded merge, post-merge evidence, and the `S2-S003` disposition (§H.1).

## Live evidence — must remain unchecked until fresh immutable evidence exists

- [ ] Exact PR head SHA recorded from live GitHub.
- [ ] Live PR base SHA equals live trusted canonical `main` SHA.
- [ ] Diff remains exactly this package's planning paths under `specs/007-s3-terminal-fabric-trusted-process-ownership/`.
- [ ] Fresh exact-head deterministic `foundation-integrity` qualification complete.
- [ ] Fresh trusted-base `s1-admission-integrity` genuinely PASSes on the exact head.
- [ ] Fresh exact-head external-review egress preflight recorded.
- [ ] Fresh qualified independent exact-head review complete.
- [ ] All material planning findings reconciled.
- [ ] No unresolved material review threads.
- [ ] Final race check complete.
- [ ] PR moved Ready only after the above evidence.
- [ ] Ready-triggered trusted-base admission genuinely PASSes on the same head.
- [ ] Guarded expected-head merge complete.
- [ ] Post-merge canonical `main`/`foundation-integrity` activation evidence complete.

## Implementation gate — blocked until planning is canonical

- [ ] S3-AUTH-C contracts-only successor canonically grants exact contract/test paths.
- [ ] S3 contract implementation complete and canonical before any Core runtime authority.
- [ ] S3-AUTH-HOST (read-only host/containment qualification) separately authorized and granted exactly.
- [ ] S3-AUTH-OBSERVE (bounded observation-only effects) separately authorized and granted exactly.
- [ ] Any process-spawn (`S3-AUTH-SPAWN`) authority separately qualified and granted exactly.
- [ ] Any direct Windows-API dependency edge separately qualified/admitted.

Unchecked live-evidence and authority items must remain unchecked until the corresponding immutable evidence/transition exists. Tracked checkbox mutation is not itself authority.
