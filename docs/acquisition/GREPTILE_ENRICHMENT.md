# Greptile — Bounded Review / Context Enrichment

## Classification

```text
FAMILY = Greptile
CLASS = REVIEW_BEHAVIOR_ORACLE + FEHREST_CONTEXT_ORACLE + OPTIONAL_EXTERNAL_REVIEWER
HOSTED_CORE_SOURCE = NOT_ESTABLISHED
PUBLIC_EDGE = greptileai/greptile-vscode
PUBLIC_EDGE_PIN = 72fc0c5a68ff966e64c2b182a2e6bf5912410821
PUBLIC_EDGE_LICENSE = MIT
NAMED_SOURCE_REGISTRY_CHANGE = 0
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

Greptile already exists in the frozen WePLD discussion/source universe. This record enriches the existing source family and does not increment the 402-entry canonical source-registry V1 count.

The public VS Code repository establishes only an edge/integration surface. It does **not** establish that Greptile's hosted code-review engine or graph/indexing backend is available as public source.

## Current official behavior evidence

Official Greptile documentation currently describes:

- a codebase graph containing files, functions/classes, imports, dependencies, calls, usages, and related patterns;
- review-time retrieval of affected callers, dependencies, related code, and similar implementations rather than diff-only analysis;
- `.greptile/` directory-scoped configuration with cascading root-to-leaf inheritance;
- `config.json` structured rules, severity, scope, disable-by-ID, review settings, and cross-repository context;
- `rules.md` as plain-language reviewer context scoped to the containing directory tree;
- `files.json` for architecture documents, schemas, API contracts, and other explicit context files;
- cross-repository context through explicitly configured repositories;
- high-signal review, inline findings, suggested fixes, conversational follow-up, and learning from team feedback.

Hosted behavior is mutable service behavior. Reuse of old Greptile evaluation evidence therefore requires a use-time provider/product compatibility check; no immutable hosted-core revision is claimed here.

## WePLD mapping

```text
PRIMARY_OWNER_CANDIDATE = Assurance
CONTEXT_OWNER = Fehrest
ARCHITECTURE_CONTEXT = Fehrest.Maemar through stable Fehrest interfaces
SECURITY_FINDING_OWNER = AMAN when implemented
EFFECT_AUTHORITY = Nawat only
REPAIR_AUTHORITY = separate authorized Attempt only
COMPLETION_AUTHORITY = Trusted Completion / applicable founder boundary only
```

## Review Context Capsule candidate

Greptile's strongest reusable behavior is not "an LLM reads a PR." It is the context selection shape around a changed unit.

Candidate WePLD capsule:

```text
Changed symbol / file
-> callers / usages
-> dependencies / imported contracts
-> related and similar implementations
-> explicit architecture / API / schema context
-> repository-scoped review rules
-> relevant historical findings / accepted patterns
-> runtime / deterministic verification evidence when available
-> bounded reviewer context capsule
```

Fehrest should own the canonical context and provenance. Assurance consumes a bounded capsule; the reviewer does not become a context-authority service.

## Positive mechanics worth adopting or benchmarking

### 1. Graph-aware change impact

Review should reason over callers, dependencies, relationships, and similar local patterns instead of treating every changed file as an isolated text document.

### 2. Cascading repository rules

A directory can inherit repository-wide review rules while adding or disabling scoped rules for a component. This is useful for monorepos and subsystem-specific assurance policy.

WePLD should adapt the hierarchy while preserving canonical authority: a lower-level file may narrow or specialize applicable review guidance only where the governing policy permits it. A repository branch cannot silently redefine Nawat authority or Trusted Completion.

### 3. Explicit context-file references

Schemas, architecture records, API contracts, and other known files can be named as reviewer context instead of hoping retrieval finds them. This maps well to Fehrest context manifests and architecture contracts.

### 4. Cross-repository context

Related repositories can be declared as context for review. WePLD should preserve this as a useful capability but separate **relevance** from **authorization to read**.

### 5. Feedback-driven review quality

Greptile can learn from comments, replies, reactions, commits, and repeated patterns. This is a useful Byan/Assurance behavior oracle for candidate learning and reviewer calibration.

## Negative authority / safety oracles

```text
GREPTILE_FINDING != COMPLETION_DECISION
GREPTILE_CLEAN != COMPLETION_DECISION
GREPTILE_FIX_SUGGESTION != WRITE_AUTHORITY
GREPTILE_LEARNED_PATTERN != CANONICAL_RULE
GREPTILE_GRAPH_RELEVANCE != TRUTH
CROSS_REPO_CONTEXT_CONFIGURED != SOURCE_ACCESS_AUTHORIZED
REVIEW_CONFIG_PRESENT != AUTHORITY_GRANT
HOSTED_SERVICE_AVAILABLE != EGRESS_AUTHORIZED
```

### Source-branch configuration is untrusted review input

Greptile documents that repository configuration can be read from the source branch of a pull request. In WePLD, any reviewer configuration coming from a proposed change must be treated as untrusted data and cannot weaken canonical review/security/authority requirements for the change that contains it.

Candidate rule:

```text
PR_CONTROLLED_REVIEW_CONFIG may narrow or add advisory context
PR_CONTROLLED_REVIEW_CONFIG may not disable canonical acceptance/security/authority gates
```

### Learning cannot self-promote

Team feedback can identify candidate preferences or repeated patterns, but repeated acceptance, reactions, or historical prevalence do not establish desired architecture or canonical policy.

```text
REPEATED_PATTERN != DESIRED_ARCHITECTURE
TEAM_PREFERENCE != CANONICAL_RULE
LEARNED_REVIEW_SUPPRESSION != SECURITY_EXCEPTION
```

## Hosted review / egress

Any actual Greptile hosted review is governed by `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`.

Before a run:

- bind exact provider/product identity and review scope;
- screen every egressed repository file for prohibited content;
- record content classification and approval;
- apply retention/training/tenant-isolation requirements for non-public material;
- bind results to exact base/head or immutable diff identity;
- record coverage limitations.

Greptile being installed or responding to a mention is not evidence that these prerequisites were satisfied.

## Acquisition decision

```text
DISPOSITION = REFERENCE | BEHAVIOR_ORACLE | TEST_QUARRY | REVIEWER_CANDIDATE
PUBLIC_EDGE_REUSE = PATH_LEVEL_ONLY_IF_NEEDED
HOSTED_CORE_REUSE = NOT_AVAILABLE_AS_PUBLIC_SOURCE_FROM_CURRENT_EVIDENCE
```

Priority mining/benchmark targets:

1. graph-context quality and changed-symbol impact retrieval;
2. cascading rule/context semantics for monorepos;
3. explicit context-file manifests;
4. cross-repository context with strict access gating;
5. reviewer feedback/learning as non-authoritative candidate learning;
6. false-positive/false-negative and coverage behavior against WePLD Assurance benchmarks.

No source, dependency, hosted service, reviewer result, learned rule, or repair mechanism is admitted by this document.