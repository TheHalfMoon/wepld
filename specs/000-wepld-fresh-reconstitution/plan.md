# Plan — Fresh Reconstitution Foundation

Every completed verification step requires a stable evidence reference. Missing required evidence is `INCOMPLETE`, not PASS.

1. Verify `TheHalfMoon/wepld` identity, owner/admin session, and clean base main.  
   Evidence: `docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md`; base `7813dea9c53863378a5ae2fefcaf66f6b5d43103`.
2. Add canonical-memory files only; do not introduce product implementation.  
   Evidence: `AGENTS.md`, `docs/canonical/`, `docs/governance/`, `docs/learning/`, `specs/000-wepld-fresh-reconstitution/`, and `src/.gitkeep` in PR #2.
3. Preserve source-universe counts and immutable V2.2 integrity anchors.  
   Evidence: `docs/canonical/artifacts/README.md`; `foundation-integrity` GitHub Actions run `31840048136` on head `026012c764f7331d10593dac8f65a689d8d9aefb` proved archive SHA `35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0`, plan SHA `e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44`, 402 unique entries, and zero source admission.
4. Record mandatory Spec Kit, Ponytail, independent-review, security-review, and learning method.  
   Evidence: `docs/canonical/BUILD_METHOD.md`, `docs/canonical/SECURITY_REVIEW_POLICY.md`, `docs/learning/BUILD_LEARNING_PROTOCOL.md`.
5. Keep the former repository as quarry only.  
   Evidence: `docs/historical/HISTORICAL_SOURCE_INDEX.md` and `docs/historical/SALVAGE_LEDGER.md`.
6. Validate no implementation source or admitted implementation dependencies.  
   Evidence: `src/.gitkeep`, `docs/governance/DEPENDENCY_REGISTER.md`, and the current PR #2 changed-file set; future foundation-integrity runs must remain fail-closed on canonical artifact semantics.
7. Keep the foundation change in Draft PR #2 until review reconciliation and founder acceptance.  
   Evidence: GitHub PR `TheHalfMoon/wepld#2`.
8. Run independent review and reconcile findings before acceptance.  
   Evidence: CodeRabbit submitted review at `2026-08-14T19:26:19Z`, CodeRabbit Run ID `9cb4838a-1a05-423e-8806-bb95874a2d23`; reconciliation commit `5bbbc07436b5c26f47622b9ee5240bc8266f935a`; subsequent review evidence must be recorded before closure.
9. Record founder acceptance separately before any S1 authorization.  
   Evidence: future explicit founder acceptance record; absence blocks this step.
