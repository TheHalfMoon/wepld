# S1-010 shell-policy activation canary

```text
PURPOSE = POST_MERGE_TRUSTED_BASE_ACTIVATION_PROOF
CANONICAL_POLICY_BASE = 3211a66f75dd0cf7e5edd23f358cb7878ea12b68
CANONICAL_POLICY_TREE = b7aa4bdea1042f2cb4a30302e75e03c4c64b7f51
EXPECTED_CURRENT_STAGE = S1_DESKTOP_LIFECYCLE_CANDIDATE
EXPECTED_CURRENT_PRODUCT_AUTHORITY = S1_009_ONLY
FUTURE_S1_010_PRODUCT_BYTES = NONE
CARGO_CHANGES = NONE
DEPENDENCY_CHANGES = NONE
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
SOURCE_ACQUISITION_CHECK = PASS
S1_011_PLUS = NOT_STARTED
EVIDENCE_RETRIGGER = SYNCHRONIZE_CANARY_ONLY
```

This docs-only candidate exists solely to prove that the S1-010 shell admission policy merged by PR #23 is active from trusted canonical `main` and can inspect candidate Git objects as data without executing candidate code in the privileged `pull_request_target` path.

The candidate intentionally contains no S1-010 marker or product path, so ordinary tree classification must remain on the already-canonical S1-009 Desktop lifecycle stage. The newly canonical policy's self-tests must separately prove the bounded future `S1_TAURI_SHELL_CANDIDATE / S1_010_ONLY` surface.

A successful canary proves policy activation only. It does not itself implement or accept S1-010, authorize S1-011+, widen dependency authority, weaken the frozen S1-006 through S1-009 product sources, or grant any WebView/process/filesystem/network authority.
