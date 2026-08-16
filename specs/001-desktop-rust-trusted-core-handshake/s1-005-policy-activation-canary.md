# S1-005 component-policy activation canary

```text
PURPOSE = POST_MERGE_TRUSTED_BASE_ACTIVATION_PROOF
CANONICAL_POLICY_BASE = 048dc246aea6c17e2b9e0209be2c317a689f61cb
EXPECTED_STAGE = S1_PLANNING_ONLY
VENDOR_BYTES = NONE
CARGO_CHANGES = NONE
RUNTIME_DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
SOURCE_ACQUISITION_CHECK = OPEN
S1_006 = BLOCKED
```

This docs-only candidate exists solely to prove that the newly canonical S1-005 trusted-base integrity policy is active after PR #9 and can inspect an ordinary planning-only candidate as Git object data.

A successful canary proves policy activation only. It does not admit the frozen GLib component, close `RUSTSEC-2024-0429`, pass the Source Acquisition Check, authorize product implementation, or start S1-006.
