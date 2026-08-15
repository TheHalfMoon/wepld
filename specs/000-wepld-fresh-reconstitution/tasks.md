# Tasks — Fresh Reconstitution Foundation

Completed tasks require stable evidence references; a checked box without evidence is not sufficient.

- [x] Verify new canonical repo and owner/admin. Evidence: `docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md`; base `7813dea9c53863378a5ae2fefcaf66f6b5d43103`.
- [x] Recover V2.2 and source-acquisition integrity anchors. Evidence: `docs/canonical/artifacts/README.md`; `foundation-integrity` run `31840048136` on `026012c764f7331d10593dac8f65a689d8d9aefb`.
- [x] Create bootstrap/current-state/invariants/build-learning docs. Evidence: `AGENTS.md`, `docs/canonical/CURRENT_STATE.md`, `docs/canonical/ARCHITECTURE_INVARIANTS.md`, `docs/learning/BUILD_LEARNING_PROTOCOL.md`.
- [x] Preserve 402-entry source accounting. Evidence: canonical archive + `docs/acquisition/SOURCE_REGISTRY_INDEX.md`; integrity run `31840048136` reports `source_registry_entries=402` and `source_admission=0`.
- [x] Preserve full raw V2.2 plan + source registry/pin/mining artifacts. Evidence: archive SHA `35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0`; `docs/canonical/artifacts/README.md`.
- [x] Keep `src/` empty of implementation on reviewed head `552589e9e35d3977a4123d4aca69f23a6eef179c`. Evidence: `src/.gitkeep` is the empty blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`; `foundation-integrity` run `31891094949` (run #117) succeeded on that exact head. CodeRabbit Run `899e93d3-6829-4f8a-b594-ef912ddf2488` nevertheless found that the gate did not reject a future non-empty placeholder, so the resulting repair head still requires fresh validation.
- [x] Publish documentation-only branch and Draft PR #2. Evidence: `TheHalfMoon/wepld#2`.
- [x] Trigger and collect initial CodeRabbit review. Evidence: submitted review `2026-08-14T19:26:19Z`, CodeRabbit Run ID `9cb4838a-1a05-423e-8806-bb95874a2d23`.
- [x] Reconcile initial material CodeRabbit findings. Evidence: commit `5bbbc07436b5c26f47622b9ee5240bc8266f935a`; follow-up exact commits `c4fae554eb32eb8e917cc09c06be3d739c6fa4b0` and `d74b5baa2ad95eb1c7c344ca66c681586318a434`.
- [x] Collect historical CodeRabbit full review on `d74b5baa2ad95eb1c7c344ca66c681586318a434`. Evidence: Run ID `ee7f2c6e-c05a-4cd6-974b-40a7037c1c60`, submitted `2026-08-14T23:59:56Z`.
- [x] Reconcile the five valid findings from the later full review and produce repair head `552589e9e35d3977a4123d4aca69f23a6eef179c`. Evidence: commit `552589e9e35d3977a4123d4aca69f23a6eef179c`; `foundation-integrity` run `31891094949` (run #117) succeeded on that exact head.
- [x] Collect CodeRabbit exact-head full re-review on `552589e9e35d3977a4123d4aca69f23a6eef179c`. Evidence: Run ID `899e93d3-6829-4f8a-b594-ef912ddf2488`, submitted `2026-08-15T15:28:51Z`; outcome: two actionable findings, not PASS.
- [ ] Close the two findings from Run `899e93d3-6829-4f8a-b594-ef912ddf2488`, re-run deterministic gates on the resulting live repair head, and obtain an independent exact-head re-review. A changed `HEAD_SHA` must not inherit the review or gate result from `552589e9`.
- [ ] Run Greptile/Qodo/Augment/Graphite/Cubic/Continue reviews where actually connected/available; record `NOT_RUN` explicitly for unavailable or egress-blocked products rather than implying PASS. Greptile state: egress preflight recorded and manual trigger sent, but no completed Greptile review output has been observed.
- [ ] Record Codex Security status for this foundation change (`NOT_APPLICABLE`, actual scan evidence, or `NOT_RUN_NON_BLOCKING`) according to `docs/canonical/SECURITY_REVIEW_POLICY.md`.
- [ ] Reconcile all remaining material findings and re-run applicable gates/reviews.
- [ ] Founder acceptance.
- [ ] Separate S1 authorization.
