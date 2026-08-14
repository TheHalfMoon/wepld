# Tasks — Fresh Reconstitution Foundation

Completed tasks require stable evidence references; a checked box without evidence is not sufficient.

- [x] Verify new canonical repo and owner/admin. Evidence: `docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md`; base `7813dea9c53863378a5ae2fefcaf66f6b5d43103`.
- [x] Recover V2.2 and source-acquisition integrity anchors. Evidence: `docs/canonical/artifacts/README.md`; `foundation-integrity` run `31840048136` on `026012c764f7331d10593dac8f65a689d8d9aefb`.
- [x] Create bootstrap/current-state/invariants/build-learning docs. Evidence: `AGENTS.md`, `docs/canonical/CURRENT_STATE.md`, `docs/canonical/ARCHITECTURE_INVARIANTS.md`, `docs/learning/BUILD_LEARNING_PROTOCOL.md`.
- [x] Preserve 402-entry source accounting. Evidence: canonical archive + `docs/acquisition/SOURCE_REGISTRY_INDEX.md`; integrity run `31840048136` reports `source_registry_entries=402` and `source_admission=0`.
- [x] Preserve full raw V2.2 plan + source registry/pin/mining artifacts. Evidence: archive SHA `35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0`; `docs/canonical/artifacts/README.md`.
- [x] Keep `src/` empty of implementation. Evidence: `src/.gitkeep`; PR #2 current changed-file set contains no product source implementation.
- [x] Publish documentation-only branch and Draft PR #2. Evidence: `TheHalfMoon/wepld#2`.
- [x] Trigger and collect initial CodeRabbit review. Evidence: submitted review `2026-08-14T19:26:19Z`, CodeRabbit Run ID `9cb4838a-1a05-423e-8806-bb95874a2d23`.
- [x] Reconcile initial material CodeRabbit findings. Evidence: commit `5bbbc07436b5c26f47622b9ee5240bc8266f935a` plus the follow-up evidence corrections in the current branch.
- [ ] Collect CodeRabbit re-review on the corrected head and reconcile any new material findings.
- [ ] Run Qodo/Augment/Graphite/Cubic/Continue reviews where actually connected/available; record `NOT_RUN` explicitly for unavailable products rather than implying PASS.
- [ ] Record Codex Security status for this foundation change (`NOT_APPLICABLE`, actual scan evidence, or `NOT_RUN_NON_BLOCKING`) according to `docs/canonical/SECURITY_REVIEW_POLICY.md`.
- [ ] Reconcile all remaining material findings and re-run applicable gates/reviews.
- [ ] Founder acceptance.
- [ ] Separate S1 authorization.
