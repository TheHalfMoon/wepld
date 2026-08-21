# H0-012 implementation-policy activation canary

```text
PURPOSE = prove base-controlled H0-012 implementation-policy activation
CANARY_CLASS = DOCS_ONLY
BASE_MAIN = dca804f239bb54605a94076e364c231fdbb06bbb
SOURCE_ACQUISITION_CHECK = PASS
H0_DIRECT_COMPONENT_SET = EXACT_AND_MINIMUM
H0_SCREEN_IMPLEMENTATION_AUTHORIZED = NO_PENDING_THIS_ACTIVATION_PROOF
H0_013_PLUS = NOT_STARTED
PRODUCT_HARNESS_INTEGRATION = NO
H0_CONFIRMATORY_EXECUTION = NO
HARBOR_ADMISSION = NONE
ROADMAP_MUTATION = NONE
```

This file is intentionally inert Markdown. It exists only to trigger the post-merge activation canary required by H0-012 governance.

The canary must prove that canonical `main` supplies the trusted `pull_request_target` workflow and the canonical H0 implementation-retention policy, while the candidate branch is inspected only as Git tree/blob data through the GitHub API. The privileged path must not check out, build, import, or execute candidate code or candidate scripts.

A successful canary is activation evidence only. It does not execute H0-SCREEN, execute Docker screening, make provider/model requests, access credentials, admit Harbor, start H0-013+, integrate the product harness, perform confirmatory execution, or mutate the roadmap. The canary PR is evidence-only and must close without merge after the required exact-head proofs are recorded.
