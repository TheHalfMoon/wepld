# S1-010 v11 deterministic-icon policy activation canary

This file is a docs-only activation canary for the canonical S1-010 v11 deterministic Windows-icon admission repair.

It carries no S1-010 product byte, no icon byte, no UI/branding byte, and grants no new product authority.

Canonical activation target:

```text
TRUSTED_BASE=069a2656127e4a16b24efeef5d55f7552f87698f
POLICY=.github/scripts/wepld_s1_shell_integrity_v11.py
PRIOR_POLICY_BLOB=c562744f9119fc83360343ee1a8297d74a0ac307
FUTURE_ICON_PATH=apps/desktop/src-tauri/icons/icon.ico
FUTURE_ICON_BYTES=4286
FUTURE_ICON_SHA256=8293595e42484de7f89ee953c0c4465731010ecb66bb8041097db97524ee47e8
FUTURE_ICON_GIT_BLOB_SHA1=d0840ec88b1a85bc485dac79f72869cd2ee6c44f
BRANDING_AUTHORITY=NONE
UI_AUTHORITY=NONE
```

Required proof before this canary may close:

1. Candidate-side `foundation-integrity` executes canonical v11 and passes on the exact canary HEAD.
2. Trusted-base `s1-admission-integrity` checks out exact canonical base `069a2656127e4a16b24efeef5d55f7552f87698f`, executes v11 self-tests from that trusted base, and inspects this candidate only as Git data.
3. Trusted-base remote verification returns PASS with `mode=REMOTE_CANDIDATE_DATA_ONLY`.
4. No candidate checkout or candidate-code execution occurs in the privileged path.
5. The v11 self-test chain proves the deterministic 4286-byte Windows icon recipe and its exact SHA-256 identity.
6. This PR is closed WITHOUT MERGE after the activation proof is durably recorded.

Because this canary is docs-only and contains no S1-010 product marker set, ordinary candidate product classification is expected to remain the already-canonical S1-009 stage. The v11 self-test chain separately proves the repaired future S1-010 icon boundary.

The icon covered here is a neutral technical Windows build fixture only. Final UI/branding design is outside this execution-admission gate.

Do not add the icon to PR #25, merge this canary, or start S1-011+ until the exact activation evidence above is complete.
