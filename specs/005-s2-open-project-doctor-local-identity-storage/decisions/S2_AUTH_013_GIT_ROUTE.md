# S2-AUTH-013 — Git Topology Route Decision

```text
STATUS = CANDIDATE_UNTIL_GUARDED_MERGE
TASK = S2-AUTH-013
CANONICAL_PREDECESSOR_MAIN = a6edc3af9e0435ed6283b2bf42ab0aff240b10db
DECISION = SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER
DECISION_CLASS = ROUTE_SELECTION_AND_FUTURE_QUALIFICATION_CONTRACT_ONLY
GIT_PROCESS_ADMISSION = NONE
EXTERNAL_PROCESS_AUTHORITY = NONE
GIT_EXECUTION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = UNCHANGED
MODEL_PROVIDER_EXECUTION = NONE
DOCTOR_CLI_AUTHORITY = NONE
S3_PLUS_AUTHORITY = NONE
NEXT_AUTHORITY_GATE = S2-AUTH-014
```

## Decision

WePLD selects a narrow adapter around the user's qualified system Git executable for
S2 repository-topology observation. It does **not** reimplement broad Git repository
semantics inside Core, and this decision does not execute Git.

This is the minimum route consistent with canonical S2 acquisition evidence and
research issue #213: Git already owns gitfiles, linked worktrees, common-directory
semantics, bare repositories, submodule/superproject topology, and protected
`safe.directory` behavior. Rebuilding that behavior would create a second parser and
a larger compatibility/security surface.

```text
ROUTE_SELECTED != PROCESS_ADMISSION
ROUTE_SELECTED != GIT_EXECUTION_AUTHORITY
ROUTE_SELECTED != NAWAT_GRANT
SYSTEM_GIT_PRESENT != QUALIFIED_GIT
GIT_OUTPUT != TRUSTED_FACT_UNTIL_PARSED_AND_REVALIDATED
```

## Frozen future adapter boundary

`S2-AUTH-014` may authorize implementation only after it qualifies this closed
boundary.

```text
EXECUTABLE_DISCOVERY = deterministic documented local rule
EXECUTABLE_INVOCATION = resolved absolute executable path only
EXECUTABLE_INSIDE_OPENED_PROJECT = REJECT
EXECUTABLE_INSIDE_WEPLD_EVIDENCE_PAYLOAD = REJECT
SILENT_BINARY_FALLBACK = PROHIBITED

USER_GIT_SUBCOMMAND = NONE
USER_GIT_OPTIONS = NONE
ARGUMENT_VECTOR = closed enum -> exact allowlisted argv
SHELL = false
STDIN = closed
STDOUT = bounded capture
STDERR = bounded capture
TIMEOUT = hard bounded
PAGER = false
PROMPT = false
OPTIONAL_LOCKS = false
NETWORK_COMMANDS = none
HOOK_COMMANDS = none
CURRENT_DIRECTORY = explicit

AMBIENT_GIT_CONFIG_COUNT_KEY_VALUE = scrub
AMBIENT_REPOSITORY_REDIRECTION_GIT_ENV = scrub
RAW_ENVIRONMENT_CAPTURE = prohibited
SAFE_DIRECTORY_POLICY = preserve native protected system/global trust evaluation
SAFE_DIRECTORY_OVERRIDE = prohibited
PROJECT_LOCAL_GIT_SPOOF = reject

PROJECT_TREE_MUTATION = none
INDEX_MUTATION = none
WORKTREE_METADATA_MUTATION = none
TREE_INDEX_NON_MUTATION = must be demonstrated by qualification
```

The future adapter must preserve enough platform/user environment to launch the
selected executable and allow Git's native protected system/global trust policy to
operate. Scrubbing must not be used to bypass `safe.directory`.

## Candidate command family for S2-AUTH-014

The following strings are specification data only in this tranche.

```text
<qualified-git> --no-pager --no-optional-locks -C <observed-locator> rev-parse <one exact allowlisted topology query>
<qualified-git> --no-pager --no-optional-locks -C <observed-locator> worktree list --porcelain -z
```

Initial `rev-parse` query candidates are limited to the topology observations already
required by Spec 005:

```text
--show-toplevel
--absolute-git-dir
--git-common-dir
--is-bare-repository
--is-inside-work-tree
--show-superproject-working-tree
```

Path-returning queries must use an exact qualified absolute-path mode where supported.
The owning S2-AUTH-014 gate must freeze the final argv matrix against the exact
qualified Git version/capability evidence before any product implementation.

Dirty/status/conflict inspection is **not** implied by this decision and requires its
own exact later command qualification if needed.

## Required S2-AUTH-014 evidence

Before `S2-I005..S2-I007` may execute Git, the successor must demonstrate or
explicitly retain a limitation for:

- ordinary repository and subdirectory observation;
- gitfile and linked worktrees;
- bare repositories;
- submodule/superproject topology;
- native `safe.directory` refusal without override;
- malicious repository configuration;
- ambient `GIT_CONFIG_*` injection attempts;
- repository-redirection environment variables;
- malicious hooks remaining unexecuted;
- a project-local spoofed `git` executable being rejected;
- bounded malformed/huge stdout and stderr;
- hard timeout behavior;
- project tree/index unchanged;
- no required network effect;
- Windows, Linux, and macOS capability behavior or an explicit platform limitation.

Failure classes remain typed and fail closed:

```text
not_git_repository
untrusted_repository_refused_by_git
unsupported_git_capability
unqualified_git_executable
git_timeout
git_output_too_large
git_output_malformed
git_process_failed
changed_under_observation
```

An arbitrary non-zero exit must not silently become a healthy `not_git_repository`
result when stronger observations indicate a repository candidate.

## Sequencing

```text
S2-AUTH-013 = this route decision
S2-AUTH-014 = separate process/executable/environment/argv qualification + authority
S2-I005..S2-I007 = Git-backed topology implementation only after S2-AUTH-014 canonical activation
S2-AUTH-015 = Doctor + CLI authority only after underlying observations/contracts exist
S2-AUTH-016 = network/model/S3/S4 authority stays denied throughout S2
```

## Acquisition / provenance

This decision uses already-recorded S2 behavior-oracle research only:

- `specs/005-s2-open-project-doctor-local-identity-storage/source-acquisition.md`;
- GitHub issue #213, `research(s2): prequalify a bounded read-only Git topology adapter`;
- the official Git behavior references recorded in those artifacts.

```text
THIRD_PARTY_SOURCE_COPIED = NO
GIT_SOURCE_IMPORT = NONE
GIT_BINARY_BUNDLING = NONE
NEW_DEPENDENCY = NONE
SOURCE_ADMISSION = NONE
```

Permissive source availability or local executable presence is not admission.

## Acceptance

This file becomes canonical only through the normal trusted-bootstrap path:

1. exact policy-only candidate delta;
2. deterministic exact-head Foundation and trusted-base admission checks;
3. external-review egress preflight when a hosted reviewer is used;
4. at least one qualified independent exact-head engineering review;
5. applicable security accounting; if the specialized Codex Security product remains
   unavailable, record `NOT_RUN_NON_BLOCKING` and do not rewrite it as PASS;
6. reconciliation of every valid material finding;
7. zero unresolved material review threads;
8. final main/base/head/tree/diff/check/review race verification;
9. guarded merge with `expected_head_sha`;
10. post-merge canonical activation proof.

The merge of this decision still leaves `GIT_EXECUTION_AUTHORITY = NONE`.
