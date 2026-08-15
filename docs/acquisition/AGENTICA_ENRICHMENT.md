# Agentica — Bounded Source / Behavior Enrichment

## Classification

```text
SOURCE = wrtnlabs/agentica
PIN = dc91f4307a3f2ee25e1ee07cf48777fcd13b6b0d
RELEASE_AT_PIN = v0.45.1
ROOT_LICENSE = MIT
CLASS = UWC_SCHEMA_NORMALIZATION + FUNCTION_CALL_VALIDATION + MIREFA_TOOL_SELECTION + CONTRACT_ORACLE + BENCHMARK_QUARRY
TIER = S
DISPOSITION = ADAPT_CANDIDATE | PORT_CANDIDATE | TEST_QUARRY | BENCHMARK | NEGATIVE_ORACLE | REFERENCE
CANONICAL_SOURCE_REGISTRY_V1_CHANGE = 0
PENDING_NEXT_REGISTRY_REVISION = YES
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
ROADMAP_CHANGE = NONE
```

Agentica is not present in the frozen 402-entry source-registry V1. This document records it as a post-V1 candidate pending a separately governed registry revision; it does not rewrite the frozen restoration artifact.

## Rights / provenance state

The pinned repository root license is MIT. Root licensing does not by itself establish transitive dependency rights, generated controller/schema rights, remote OpenAPI-document rights, benchmark-service rights, or the suitability of every optional plugin.

```text
ROOT_LICENSE_ESTABLISHED = MIT
TRANSITIVE_RIGHTS_AUDIT = INCOMPLETE
PATH_LEVEL_RIGHTS_AUDIT = REQUIRED_BEFORE_REUSE
WHOLE_REPOSITORY_COPY = NOT_AUTHORIZED
```

## Pinned evidence anchors

```text
README.md
blob = 6515cfc1bf9924cfc2bbd8be0e1f50698942caf2

LICENSE
blob = 886b7e88682164a5a22e609120c9f96c9ea57216

packages/core/prompts/validate.md
blob = 9c930df0a0576de4e19954f7044cd5ce809ac8f4

packages/core/src/events/AgenticaValidateEvent.ts
blob = 9d193ad86d603a8c2998439f6a61024d730e3a76

website/content/docs/plugins/vector-selector.mdx
blob = 14e006bec18e0bb589ec4460455c9b0128c42c40
```

## WePLD capability mapping

```text
UWC      <- normalize callable capabilities from TypeScript classes, OpenAPI/Swagger, and MCP
Mirefa   <- select the minimum relevant tool/function subset before model exposure
AGILLE   <- typed function contracts + schema compilation + validation feedback loops
Assurance<- deterministic validation events + failure corpus + benchmark cases
Fehrest  <- bounded context/tool-selection evidence, not truth or authority
Byan     <- later outcome/selector benchmark learning candidates only
```

## Positive mechanics worth mining

### 1. Multi-protocol function ingestion behind one calling model

Agentica presents a common agent surface over three major capability sources: TypeScript classes, Swagger/OpenAPI documents, and MCP servers. This is directly relevant to UWC adapter normalization.

The useful principle is:

```text
MANY_UPSTREAM_CAPABILITY_FORMATS
-> ONE_WEPLD_OWNED_NORMALIZED_CONTRACT
```

Do not inherit Agentica-specific vendor/schema assumptions as WePLD authority.

### 2. Compiler-driven schema construction

Agentica uses compiler/type information to construct function-calling schemas rather than relying entirely on handwritten JSON. This is a strong AGILLE/UWC donor for reducing schema drift and creating testable contract generation.

### 3. Vendor schema conversion

Agentica explicitly normalizes schema differences between model vendors. WePLD can mine the converter/test corpus to harden UWC provider adapters, while keeping semantic equivalence and unsupported-feature handling fail-loud.

### 4. Validation feedback loop

The runtime emits a typed validation event containing the exact tool-call id, target operation, validation failure, and lifecycle count. Its correction prompt requires every validation error to be addressed and uses exact paths/expected values to guide repair.

This is valuable for bounded tool-call repair:

```text
TOOL_ARGUMENTS
-> DETERMINISTIC_VALIDATION
-> STRUCTURED_FAILURE
-> BOUNDED_CORRECTION_ATTEMPT
-> REVALIDATION
```

Each correction in WePLD would still require the applicable Attempt/write authority and cannot silently become an unbounded retry loop.

### 5. Selector-agent / vector-selection benchmark quarry

Agentica's Vector Selector uses semantic search to reduce the function set exposed to the model. Its published benchmark documentation reports a substantial token reduction and higher task success in its benchmark, with a latency tradeoff and PostgreSQL/SQLite strategies.

Treat these numbers as source-specific benchmark evidence, not universal performance claims. The benchmark harness and strategy interface are more valuable than the headline numbers.

### 6. Pluggable selector strategy

The vector selector supports a strategy interface separating `searchTool` from context embedding. That is useful for Mirefa experiments comparing lexical, graph, vector, hybrid, deterministic, and model-assisted capability selection behind one WePLD contract.

## Negative oracles / required WePLD divergence

```text
AGENTICA_FUNCTION_SELECTED != TOOL_EXECUTION_AUTHORIZED
AGENTICA_VECTOR_SIMILARITY != CAPABILITY_AUTHORITY
AGENTICA_SCHEMA_CONVERSION != SEMANTIC_EQUIVALENCE_PROVEN
AGENTICA_VALIDATION_SUCCESS != BUSINESS_CORRECTNESS
AGENTICA_VALIDATION_SUCCESS != COMPLETION_DECISION
AGENTICA_VENDOR_ADAPTER != ROUTE_AUTHORIZATION
```

### Runtime validation feedback cannot be universal authority

The pinned correction prompt states that validation feedback overrides the general JSON schema because feedback reflects current runtime constraints. That can be correct inside Agentica's trusted validator contract, but WePLD must scope this rule much more tightly:

```text
QUALIFIED_DETERMINISTIC_RUNTIME_CONSTRAINT
may narrow
GENERAL_TOOL_SCHEMA

UNTRUSTED_TEXTUAL_FEEDBACK
must not override
CANONICAL_CONTRACT / NAWAT / SECURITY POLICY
```

Validation descriptions and `expected` values are data from a specific validator for a specific call. They cannot grant capabilities, weaken authority, or redefine canonical engineering requirements.

### Argument compliance is not action safety

A tool call can be perfectly schema-valid and still be unauthorized, unsafe, stale, or semantically wrong. UWC validation therefore precedes, but never replaces, Nawat effect-time authorization and application-specific preconditions.

### Selector relevance is not permission

The selector's purpose is context/token efficiency. A function ranking highly enough to expose to a model does not mean it is permitted to execute. Mirefa may qualify relevance/capability; Nawat owns authority.

### Vector benchmark dependency cost must face Ponytail

The documented vector strategies can introduce embedding providers, vector stores, databases, network services, and operational complexity. WePLD must benchmark simpler lexical/metadata/graph filters first and add vector machinery only when accepted-outcome value justifies it.

## Acquisition decision

Mine Agentica selectively as a UWC/Mirefa/AGILLE validation and benchmark quarry.

Priority path-mining order:

1. `packages/core/` controller/function normalization and vendor-schema conversion paths;
2. validation event, validation execution, bounded retry/correction, and tests;
3. `packages/vector-selector/` strategy contracts and selector tests;
4. `benchmark/vector-selector-benchmark/` methodology, fixtures, metrics, and reproducibility gaps;
5. WebSocket/RPC contracts only if S6 UWC requires a directly comparable transport mechanism.

Do not adopt its entire application stack or vector infrastructure merely to obtain function-calling mechanics.

No source, package, dependency, vector database, embedding provider, controller, MCP server, model provider, or remote service is admitted by this document.
