# Source Acquisition Addendum — Omnigent

```text
STATUS = RESEARCH_INPUT_ONLY
PARENT = source-acquisition.md
REPOSITORY = omnigent-ai/omnigent
PINNED_REVISION = f4e93c2b74158a2712d07f13e591abb90a999171
LICENSE_OBSERVED = Apache-2.0
NOTICE_PRESENT = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION_AUTHORITY = NONE
DONOR_EXECUTION = PROHIBITED
```

## Candidate role

Omnigent is a future source-acquisition candidate for **minimum-sufficient execution-fabric mechanisms**, not a donor root architecture.

Primary candidate roles:

```text
BEHAVIOR_ORACLE
SECURITY_DESIGN_QUARRY
PROTOCOL_ADAPTER_QUARRY
TEST_AND_NEGATIVE_ORACLE_QUARRY
BOUNDED_SOURCE_REUSE_CANDIDATE_ONLY_AFTER_OWNING_GATE
```

## Exact owning paths to requalify later

At the observed revision, the highest-value paths are:

```text
omnigent/runtime/policies/engine.py
omnigent/policies/types.py
omnigent/runtime/__init__.py
omnigent/runtime/caps.py
omnigent/inner/acp_extension.py
omnigent/inner/acp_executor.py
omnigent/inner/bwrap_sandbox.py
designs/SANDBOX_CREDENTIAL_PROXY.md
omnigent/inner/credential_proxy.py
omnigent/inner/egress/**
omnigent/tools/builtins/browser.py
omnigent/runner/tool_dispatch.py
examples/polly/**
web/electron/**
```

The exact path set must be reverified at the owning Source Acquisition Check. This planning record does not freeze future upstream layout as implementation truth.

## Candidate-by-candidate reuse posture

| Mechanism | Future reuse posture |
|---|---|
| Server / Host / Runner separation | clean-room contract/architecture adaptation |
| Generic ACP executor seam | clean-room adapter architecture; bounded source reuse only if justified |
| Vendor dialect extension seam | clean-room adaptation |
| Policy choke point / fail-closed phases | behavior oracle only; not Nawat |
| Runtime caps | clean-room execution-envelope/ceiling adaptation |
| Bubblewrap/seccomp sandbox | security/test quarry; implementation reuse requires dedicated qualification |
| Secretless credential proxy | P0 security/source qualification; clean-room preferred until proven otherwise |
| Environment allowlisting | clean-room adaptation |
| Browser snapshot/ref freshness | clean-room behavior adaptation |
| Tool advertisement vs execution | reinforcing behavior oracle |
| Polly cross-vendor review | behavior oracle for review-independence policy |
| Session/worktree effect ordering | behavior oracle for S8 effect dependency |
| Electron native bridge | architecture/security quarry |
| Recovery/reconnect behavior | behavior oracle |
| Hindsight integration | optional P2 adapter only |

## Apache-2.0 / NOTICE requirements

The repository license permits substantial reuse subject to its terms, but future copying/adaptation must still:

- preserve applicable copyright, patent, trademark, and attribution requirements;
- preserve/propagate NOTICE content as required for derivative distribution;
- mark modified copied files as required;
- separately inspect licenses of bundled/third-party code and dependencies;
- avoid treating repository-level Apache-2.0 as permission to copy trademarks, unrelated assets, or differently licensed third-party material.

```text
LICENSE_AVAILABLE != SOURCE_ADMITTED
NOTICE_PRESENT != ATTRIBUTION_COMPLETE_FOR_ANY_FUTURE_COPY
REPOSITORY_LICENSE != TRANSITIVE_DEPENDENCY_ADMISSION
```

## Security-specific admission gates

The following mechanism families require security-specialist qualification before source reuse or dependency activation:

```text
sandbox / seccomp / namespace code
TLS MITM / egress proxy
credential resolution / placeholder swapping
secret refresh/storage
host/runner transport and authentication
native desktop IPC/preload bridge
browser actuation
policy executable/plugin loading
```

Minimum questions include:

- what trusted computing base is imported?
- can a worker bypass the broker/sandbox/proxy?
- what credentials/config become visible?
- what filesystem/network/process effects occur during import/runtime?
- what platform limitations exist, especially Windows?
- what maintenance/update behavior can silently change semantics?
- what source/dependency chain becomes acceptance-critical?
- what is the exit strategy if the donor design or protocol changes?

## Donor execution prohibition

During reconnaissance/source qualification, do not run Omnigent's installer, development hooks, workflows, model/provider integrations, sandbox launchers, policy modules, cloud providers, package scripts, or examples merely to inspect source.

Any later execution must be separately admitted and authorized by the owning slice.

## Relationship to WePLD architecture

The following equations remain controlling:

```text
OMNIGENT_POLICY_ALLOW != NAWAT_GRANT
OMNIGENT_HOST_OR_RUNNER != WEPLD_AUTHORITY
OMNIGENT_SANDBOX_LABEL != WEPLD_CONTAINMENT_EVIDENCE
OMNIGENT_PROVIDER_SESSION != WEPLD_ATTEMPT_IDENTITY
OMNIGENT_CREDENTIAL_PROXY != GENERAL_NETWORK_OR_EFFECT_AUTHORITY
OMNIGENT_REVIEW_PATTERN != TRUSTED_COMPLETION
```

WePLD retains Fehrest, Edara, Mirefa, Nawat, Mission Runtime, UWC, AMAN, Assurance, S8 repair, and Trusted Completion ownership.

## Future admission procedure

For each mechanism actually needed by an activated slice:

1. reverify upstream revision, tree, license, NOTICE, and exact owning paths;
2. state the exact WePLD capability gap;
3. compare admitted/local alternatives and standard-library/native implementation cost;
4. choose one reuse mode: reject, oracle only, tests/fixtures, clean-room adaptation, bounded copied source, or dependency;
5. freeze provenance and required attribution;
6. run security/portability/maintenance/exit qualification;
7. admit only the minimum paths/dependencies required;
8. add adversarial negative tests proving no authority widening;
9. obtain exact-head independent review of any adaptation;
10. preserve source/review evidence in the owning Source Acquisition record.

No action in this addendum changes current S2 authority or admits Omnigent code.