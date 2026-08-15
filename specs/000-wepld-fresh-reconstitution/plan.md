# Plan — Fresh Reconstitution Foundation

Every completed verification step requires a stable evidence reference. Missing required evidence is `INCOMPLETE`, not PASS.

1. Verify `TheHalfMoon/wepld` identity, owner/admin session, and clean base main.  
   Evidence: `docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md`; base `7813dea9c53863378a5ae2fefcaf66f6b5d43103`.
2. Add canonical-memory files only; do not introduce product implementation.  
   Evidence: latest independently reviewed pre-repair head `552589e9e35d3977a4123d4aca69f23a6eef179c`; `foundation-integrity` run `31891094949` (run #117) succeeded on that exact head. CodeRabbit exact-head re-review Run ID `899e93d3-6829-4f8a-b594-ef912ddf2488`, submitted `2026-08-15T15:28:51Z`, found two actionable follow-up findings, so that review is historical evidence only and cannot certify any later repair head.
3. Preserve source-universe counts and immutable V2.2 integrity anchors.  
   Evidence: `docs/canonical/artifacts/README.md`; `foundation-integrity` GitHub Actions run `31840048136` on head `026012c764f7331d10593dac8f65a689d8d9aefb` proved archive SHA `35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0`, plan SHA `e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44`, 402 unique entries, and zero source admission.
4. Record mandatory Spec Kit, Ponytail, independent-review, security-review, and learning method.  
   Evidence: `docs/canonical/BUILD_METHOD.md`, `docs/canonical/SECURITY_REVIEW_POLICY.md`, `docs/learning/BUILD_LEARNING_PROTOCOL.md`.
5. Keep the former repository as quarry only.  
   Evidence: `docs/historical/HISTORICAL_SOURCE_INDEX.md` and `docs/historical/SALVAGE_LEDGER.md`.
6. Validate no implementation source or admitted implementation dependencies.  
   Evidence: on reviewed head `552589e9e35d3977a4123d4aca69f23a6eef179c`, `src/.gitkeep` is the empty blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` and `foundation-integrity` run `31891094949` (run #117) succeeded; CodeRabbit Run ID `899e93d3-6829-4f8a-b594-ef912ddf2488` identified that the gate itself did not reject a future non-empty placeholder. The resulting repair head must add that fail-closed check and pass a fresh exact-head gate before this evidence can support acceptance.
7. Keep the foundation change in Draft PR #2 until review reconciliation and founder acceptance.  
   Evidence: GitHub PR `TheHalfMoon/wepld#2`.
8. Run independent review and reconcile findings before acceptance.  
   Evidence: historical full-review Run ID `ee7f2c6e-c05a-4cd6-974b-40a7037c1c60` reviewed through `d74b5baa2ad95eb1c7c344ca66c681586318a434`; later exact-head re-review Run ID `899e93d3-6829-4f8a-b594-ef912ddf2488` reviewed base `7813dea9c53863378a5ae2fefcaf66f6b5d43103` through `552589e9e35d3977a4123d4aca69f23a6eef179c` and produced two actionable findings. Repairing either finding changes `HEAD_SHA`; the resulting live repair head must receive a fresh deterministic gate and independent re-review and must not inherit PASS from `552589e9`.
9. Record founder acceptance separately before any S1 authorization.  
   Evidence: future explicit founder acceptance record; absence blocks this step.
