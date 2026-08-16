# S1-003 activation canary

```text
PURPOSE = prove base-controlled s1-admission-integrity activation
CANARY_CLASS = DOCS_ONLY
BASE_MAIN = af000ec9cd4a1ce71545cdc509f13af0e69429f9
SOURCE_ACQUISITION_CHECK = OPEN
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION = BLOCKED
S1_003_ACTIVATION_PROVEN = NO
S1_004_AUTHORIZED = NO
```

This file is intentionally inert Markdown. It exists only to trigger the post-merge activation canary required by S1-003 governance.

The canary must prove that canonical `main` supplies the trusted `pull_request_target` workflow and integrity policy, while the candidate branch is inspected only as Git tree/blob data through the GitHub API. The privileged path must not check out, build, import, or execute candidate code or candidate scripts.

A successful canary is activation evidence only. It does not admit dependencies, pass source acquisition, authorize product implementation, accept S1, or start S1-004.
