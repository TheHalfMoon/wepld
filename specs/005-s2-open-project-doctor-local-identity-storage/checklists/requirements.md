# S2 Requirements Checklist

## Authority and scope

- [x] S2 planning authority is explicitly separated from implementation authority.
- [x] Source admission remains none.
- [x] Dependency admission remains none.
- [x] Product/runtime authority remains none during planning.
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
- [x] Repository mutation is prohibited for S2 inspection.
- [x] Local evidence storage is outside the project by default.
- [x] Evidence freshness/provenance/corruption states are specified.
- [x] Doctor findings include evidence references and remediation text.

## CLI contract

- [x] Human output is required.
- [x] Stable JSON is required.
- [x] Noninteractive behavior is required.
- [x] Exit-code semantic classes are defined for later freezing.
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
- [x] Raw remote credentials/environment capture is prohibited.
- [x] Store corruption fails closed for evidence claims.
- [x] Parser/file/output bounds are required before implementation.

## Portability and durability

- [x] Windows-first qualification is explicit.
- [x] Unix portability cases are explicit.
- [x] Concurrent writers are addressed.
- [x] Crash/torn-write behavior is addressed.
- [x] Durability claims must match platform evidence.
- [x] Whole-repository traversal is prohibited for baseline open/doctor.

## Build method

- [x] Constitution complete.
- [x] Specification complete.
- [x] Clarifications complete.
- [x] Plan complete.
- [x] Checklist complete.
- [x] Analyze complete.
- [x] Tasks ledger complete.
- [x] Ponytail FULL complete for the planning candidate.
- [x] Source Acquisition Check complete for the planning candidate.
- [x] Threat model complete.
- [ ] Exact-head deterministic planning qualification complete.
- [ ] Independent exact-head planning review complete.
- [ ] All material planning findings reconciled.
- [ ] Planning package merged/canonical.
- [ ] Post-merge planning activation evidence complete.

## Implementation gate

- [ ] Separate S2 implementation authority granted by canonical successor policy.
- [ ] Any external-process authority qualified and granted exactly.
- [ ] Any new dependency/source admission separately qualified.
- [ ] Implementation deterministic gates defined at exact authorized paths.

Unchecked live-evidence items must remain unchecked until the corresponding immutable evidence exists. Tracked checkbox mutation is not itself authority.
