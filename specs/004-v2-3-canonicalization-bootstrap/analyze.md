# Analyze — Spec 004

## Consistency analysis

### Governance

The current trusted base says ordinary future candidates may not mutate base-controlled governance and that legitimate policy migration requires an explicitly governed bootstrap/override event. Spec 003 acceptance separately requires that event before V2.3 canonicalization. Spec 004 satisfies both by splitting policy bootstrap from plan adoption.

The immediate predecessor PR #169 establishes the applicable bootstrap precedent: an old canonical policy cannot authorize an unseen successor policy. Its old-base `s1-admission-integrity` result was preserved as `EXPECTED_BOOTSTRAP_FAILURE` with `OLD_BASE_S1_PASS=NO`; the failure was not renamed PASS. Spec 004 applies the same truth-preserving rule to v4 -> v5.

### Authority

No contradiction with standing founder authorization exists. Standing authorization allows governed execution; it does not mint PASS or permit a candidate to redefine its own trusted-base controls. For a policy-successor bootstrap, it permits the separately governed bootstrap event after candidate deterministic evidence, security accounting, independent review, finding reconciliation, and final live-race evidence are complete while the expected old-base rejection remains explicitly recorded.

### Roadmap

V2.3 keeps `P0 + S1..S10` and adds named non-primary gates inside existing slices. Therefore canonicalization is a bounded architecture enrichment, not a roadmap reset.

### Source registry

The frozen 402-entry registry is untouched. Post-V1 candidates remain pending a later separately governed registry revision.

### Active acquisition work

PRs #136/#159/#162/#164/#166 and PR #88 remain outside Spec 004. No branch relationship, source import, lock repair, dependency admission, or donor execution is required for V2.3 canonicalization.

## Failure modes and controls

| Failure mode | Required control |
|---|---|
| Candidate policy appears to self-authorize a governance edit | Separate bootstrap event; preserve trusted v4 rejection as `EXPECTED_BOOTSTRAP_FAILURE`; require candidate exact-head evidence and independent review before founder-authorized merge |
| Old-base bootstrap failure is mislabeled PASS | Record `OLD_BASE_S1_PASS=NO`; never use the old-base result as acceptance evidence |
| Bootstrap accidentally canonicalizes V2.3 | Exact three-file bootstrap delta; no index/plan path allowed |
| v5 grants broad governance mutation | Exact post-activation two-file V2.3 route only |
| Candidate plan changed after Spec 003 review | Bind exact trusted-base candidate Git blob |
| Canonical plan differs materially from reviewed candidate | Deterministic metadata-only transformation |
| Index points to wrong/unstable bytes | Bind index to derived canonical-plan digest/path |
| Extra file piggybacks canonicalization | Exact changed-path set |
| v5 is merged but not actually active as trusted base | Require post-merge Foundation activation and trusted-base v5 PASS on the first successor canonicalization PR before that PR can merge |
| Head changes after review/check | Re-run every invalidated exact-head gate |
| Reviewer unavailable | `REVIEW_BLOCKED`, not PASS |
| Security scan unavailable | `NOT_RUN_NON_BLOCKING`, never PASS |
| Canonicalization reused for later mutation | One-time precondition: trusted base must still be V2.2 with no canonical V2.3 file |

## Conclusion

The two-event design is internally consistent, minimum-sufficient, and preserves authority separation once the old-base bootstrap limitation is modeled explicitly. Implementation may begin only after this Spec 004 planning package itself is exactly qualified and accepted.
