# S1-010 v10 icon-policy activation canary

This file is a docs-only activation canary for the S1-010 v10 Tauri icon-admission repair.

It carries no S1-010 product byte and grants no new product authority.

Canonical activation target:

```text
TRUSTED_BASE=7a4a373e9bc676e4d7765ba8d69662cc78fb8d66
POLICY=.github/scripts/wepld_s1_shell_integrity_v10.py
FUTURE_ICON_PATH=apps/desktop/src-tauri/icons/icon.ico
FUTURE_ICON_BYTES=4286
FUTURE_ICON_SHA256=e598c151776122e15f426798fddb4ed9c400085ce83623718b58841e25bac38b
```

Required proof before this canary may close:

1. Candidate-side `foundation-integrity` executes canonical v10 and passes on the exact canary HEAD.
2. Trusted-base `s1-admission-integrity` checks out exact canonical base `7a4a373e9bc676e4d7765ba8d69662cc78fb8d66`, executes v10 self-tests from that trusted base, and inspects this candidate only as Git data.
3. Trusted-base remote verification returns PASS with `mode=REMOTE_CANDIDATE_DATA_ONLY`.
4. No candidate checkout or candidate-code execution occurs in the privileged path.
5. This PR is closed WITHOUT MERGE after the proof is recorded.

Because this canary is docs-only and contains no S1-010 marker set, ordinary candidate product classification is expected to remain the already-canonical S1-009 stage. The v10 self-test chain separately proves the repaired future S1-010 icon boundary.

Do not add the icon to PR #25, merge this canary, or start S1-011+ until the exact activation evidence above is complete.