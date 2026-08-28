# S2 Requirements Checklist

## Authority and scope

- [x] S2 planning authority is explicitly separated from implementation authority.
- [x] Candidate governance/planning text cannot self-authorize before trusted-base merge/activation.
- [x] Source admission remains none.
- [x] Dependency admission remains none.
- [x] Product/runtime authority remains none during planning.
- [x] First post-planning successor is contracts-only by default unless canonical evidence proves otherwise.
- [x] Git process authority is deferred to a later separate gate.
- [x] S3 Terminal Fabric is excluded.
- [x] S4 semantic graph is excluded.
- [x] Agents/models/providers are excluded.
- [x] Automatic remediation is excluded.

## Product requirements

- [x] `wepld open` outcome is specified.
- [x] `wepld doctor` outcome is specified.
- [x] `wepld status` outcome is specified.
- [x] Non-Git projects are specified.
- [x] Git worktree/submodule/nested-repository cases are specified.
- [x] Project identity is not reduced to one path.
- [x] Local identity reassociation is conservative.
- [x] Concurrent first-open identity creation is serialized by a store-wide catalog reservation before per-project locking.
- [x] Reserved first-open identity recovery after crash is specified.
- [x] Repository mutation is prohibited for S2 inspection.
- [x] Local identity/evidence storage is outside the project by default.
- [x] Project-store updates use immutable generations plus one committed `CURRENT` selector.
- [x] Mixed-generation reads are prohibited.
- [x] Evidence freshness/provenance/corruption states are specified.
- [x] Doctor findings include safe evidence references and non-executable remediation semantics.

## CLI and output contract

- [x] Human output is required.
- [x] Stable JSON is required.
- [x] TTY and JSON share one secret-redaction/allowlist semantic layer.
- [x] Finding prose comes from WePLD-owned templates plus closed safe parameters.
- [x] Raw secret-bearing environment/config/remote/command-output values are prohibited from trusted output.
- [x] Noninteractive behavior is required.
- [x] Exit-code semantic classes are defined for later numeric reconciliation.
- [x] Busy/contended conditions are machine distinguishable.
- [x] Unknown commands remain errors.
- [x] AI prompt interfaces remain explicit future commands.
- [x] Streaming JSONL/event mode is preserved as a forward seam, not overbuilt in S2.

## Security

- [x] Git `safe.directory` refusal must not be auto-bypassed.
- [x] Path canonicalization is explicitly not containment authority.
- [x] TOCTOU is represented in the threat model.
- [x] Symlink/junction/reparse risks are represented.
- [x] Repository-controlled hooks/scripts are prohibited during S2 inspection.
- [x] External Git process use is gated behind separate effect authority.
- [x] Git environment injection/executable spoofing are represented for later adapter qualification.
- [x] Raw remote credentials/environment capture is prohibited.
- [x] Store corruption/generation mismatch fails closed for evidence claims.
- [x] Catalog corruption/reservation conflict fails closed for identity creation.
- [x] Parser/file/output bounds are required before implementation.
- [x] Descriptor discovery exact root allowlists are frozen.
- [x] Descriptor candidate/per-file/aggregate/nesting limits are frozen.
- [x] Indefinite lock acquisition is prohibited.
- [x] Lock-file existence is not ownership proof.
- [x] Doctor TTY/JSON secret-exfiltration threat and tests are explicit.

## Portability and durability

- [x] Windows-first qualification is explicit.
- [x] Unix portability cases are explicit.
- [x] Concurrent first-open and ordinary writers are separately addressed.
- [x] Crash/torn-write behavior is addressed at catalog, generation, manifest, and `CURRENT` boundaries.
- [x] Durability claims must match measured platform evidence.
- [x] Whole-repository traversal is prohibited for baseline open/Doctor.
- [x] Lock acquisition planning defaults are bounded to 2000ms with 25ms polling and cancellation checks.

## Source Acquisition / Ponytail

- [x] Registry input is bound to trusted-base OID `46b1fc423f3fc5175d79acaf0f134747bf0d90f0`.
- [x] Registry file is bound to Git blob `4a2fe363e0e66f7183e0221743258fcf558a3733`.
- [x] Historical source-check input head is recorded without pretending it is the future repaired acceptance head.
- [x] Research issues #211–#214 are referenced as non-authoritative evidence only.
- [x] UUID/SHA-256 transitive presence is not treated as dependency admission.
- [x] Catalog reservation + immutable generations + `CURRENT` are justified as minimum correctness machinery, not database creep.
- [x] Database, async runtime, agent framework, vector store, crawler, model provider, and source import remain rejected for S2 minimum.

## Build method / planning content

- [x] Constitution complete and reconciled with initial review findings.
- [x] Specification complete and reconciled with initial review findings.
- [x] Clarifications complete and reconciled with initial review findings.
- [x] Plan complete and contains staged post-planning authority/delivery sequence.
- [x] Checklist complete.
- [x] Analyze complete for the repaired planning candidate.
- [x] Tasks ledger contains explicit implementation/review tasks for every initial material finding.
- [x] Ponytail FULL complete for the repaired planning candidate.
- [x] Source Acquisition Check complete for the planning/no-import boundary.
- [x] Threat model covers first-open split, mixed generation, lock DoS, descriptor amplification, and output secret leakage.
- [x] Acceptance contract includes exact base/main, reviewer qualification, `REVIEW_BLOCKED`, race, Ready-triggered admission, guarded merge, and post-merge evidence.

## Live evidence — must remain unchecked until fresh immutable evidence exists

- [ ] Exact repaired PR head SHA recorded from live GitHub.
- [ ] Live PR base SHA equals live trusted canonical `main` SHA.
- [ ] Repaired diff remains exactly the eleven v21 planning paths.
- [ ] Fresh exact-head deterministic Foundation qualification complete.
- [ ] Fresh trusted-base v21 admission genuinely PASSes on the repaired head.
- [ ] Fresh exact-head external-review egress preflight recorded.
- [ ] Fresh qualified independent exact-head rereview complete.
- [ ] All fresh material planning findings reconciled.
- [ ] No unresolved material review threads.
- [ ] Final race check complete.
- [ ] PR moved Ready only after the above evidence.
- [ ] Ready-triggered trusted-base admission genuinely PASSes on the same head.
- [ ] Guarded expected-head merge complete.
- [ ] Post-merge canonical `main`/Foundation activation evidence complete.

## Implementation gate — blocked until planning is canonical

- [ ] S2-AUTH-C contracts-only successor canonically grants exact contract/test paths.
- [ ] S2 contract implementation complete and canonical before Core filesystem authority.
- [ ] Separate locator/identity/evidence Core authority granted exactly.
- [ ] Per-platform data-root and lossless path contract frozen before corresponding Core behavior.
- [ ] Any direct UUID/SHA-256 dependency edge separately qualified/admitted if required.
- [ ] Any external Git process authority separately qualified and granted exactly.
- [ ] Doctor/CLI authority granted only after underlying contracts/evidence logic exists.

Unchecked live-evidence and authority items must remain unchecked until the corresponding immutable evidence/transition exists. Tracked checkbox mutation is not itself authority.
