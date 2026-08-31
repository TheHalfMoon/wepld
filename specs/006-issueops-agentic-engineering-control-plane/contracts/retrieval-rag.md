# Contract — Retrieval / RAG Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
VECTOR_DEPENDENCY_ADMISSION = NONE
```

## Purpose

Define a universal, provenance-first retrieval boundary for user-selected knowledge without making any retrieval engine, vector database, embedding model, parser, or remote service the Project Brain.

## Collection operations

Planned logical operations:

```text
create_collection
select_collection
add_source
remove_source
refresh_source
list_sources
inspect_source
retrieve
clear_collection
```

Each operation declares whether it is pure/local or requires filesystem/network/parser/model effects under the owning implementation.

## Supported source model

A source is admitted to a collection only through a qualified source-access/parser path. Candidate kinds include:

```text
file
directory
pasted_text
clipboard_text
repository
markdown
pdf
structured_text_or_data
log
url
documentation_site
provider_attachment
```

The product intent is broad user choice; the implementation must fail closed on unsupported, unsafe, over-limit, or unqualified source classes.

## Retrieval signals and minimum-sufficient selection

The retrieval contract allows multiple replaceable signals:

```text
EXACT
PATH_OR_KEY
LEXICAL
METADATA
SYNTAX
SYMBOL
REFERENCE
CALL_GRAPH
SEMANTIC_VECTOR
RERANK
FRESHNESS
```

These are **not a rigid serial pipeline**. The retrieval planner selects the minimum sufficient signal set for the query/source class and may evaluate compatible signals in parallel.

Baseline rules:

1. exact/path/key lookup is preferred when the query names a known identifier or locator;
2. lexical retrieval is a baseline for free text and remains available without embeddings;
3. Fehrest.Maemar syntax/symbol/reference/call-graph facts are first-class retrieval signals for code questions and should be preferred over semantic similarity when they answer the query precisely;
4. semantic/vector retrieval may be selected early for conceptual/paraphrastic natural-language queries, low lexical recall, vocabulary mismatch, or qualified cross-document similarity tasks;
5. semantic/vector retrieval is not mandatory merely because the query is natural language;
6. reranking is optional and must not hide source-level signals/provenance;
7. freshness filters may exclude or downgrade stale evidence before context packing.

No signal is mandatory unless required by the owning slice/task. Exact/lexical/structured retrieval must remain usable without semantic/vector machinery.

## First useful RAG qualification

The first useful `/rag` capability is not defined by possession of a vector database. Before semantic/vector admission, the non-vector baseline should be tested on a representative corpus that includes:

```text
exact file/path lookup
error/log lookup
natural-language question answered by lexical evidence
symbol/reference question answered by Fehrest.Maemar facts
cross-source citation lookup
stale-source detection
no-answer / abstention case
```

For every query the benchmark records whether the system retrieved a source containing the required evidence, whether the citation/location is inspectable, whether stale/conflicting evidence was surfaced, and whether it abstained when qualified evidence was absent.

Semantic/vector machinery is justified only if an owning-slice benchmark shows a material retrieval-quality improvement for identified query classes that cannot be met by query decomposition, lexical, metadata, or Fehrest.Maemar structured signals at acceptable cost/latency/privacy. Exact promotion thresholds are declared **before** the benchmark run under the owning slice; post-hoc threshold selection is not qualification.

If semantic/vector retrieval is admitted, quality evaluation must report its incremental contribution separately from lexical/structured signals so removal/replacement remains possible.

## Fehrest.Maemar integration

Fehrest.Maemar facts are source-backed semantic code facts, not RAG-generated truth. Retrieval may reference:

```text
repository/blob identity
syntax node identity
symbol identity
reference/call edge
architecture/module relation
fact provenance
fact freshness/generation
```

A natural-language retrieval result that cites a symbol/call relation must retain the underlying Maemar fact identity and source generation. Semantic/vector similarity may help locate a candidate symbol or document, but the exact graph/source fact remains the stronger evidence when available.

## Retrieval response

Every material result must include or reference:

```text
source_id
source_generation
source_kind
source_identity
exact_location_or_citation?
freshness_state
retrieval_signals[]
rank_or_score_observations[]
parser_or_index_identity
retrieved_at
```

Scores are evidence only:

```text
RETRIEVAL_SCORE != TRUTH
RERANK_SCORE != TRUTH
EMBEDDING_DISTANCE != TRUTH
CITATION != AUTHORITY
```

## Freshness

A source/index generation must make freshness inspectable. Missing, stale, inaccessible, or conflicting source state must be surfaced explicitly. A retrieval path that requires current evidence cannot silently substitute a stale generation.

## Context packaging and untrusted content

Downstream workflows/workers receive bounded `RetrievalEvidence` references or a derived minimum-sufficient context package. The package must preserve citations/provenance and should avoid dumping entire collections when smaller evidence is sufficient.

Retrieved content remains untrusted data unless its origin is a controlling WePLD/user policy channel. Embedded instructions, tool requests, fake policy text, or workflow commands inside sources do not become `WorkflowIntent` and cannot expand worker access/effects. Context-package manifests must preserve source/trust labels so the effect boundary can distinguish evidence from instruction authority.

## Privacy / egress

Adding content to a local collection does not authorize sending it to a remote embedding/model/retrieval provider. External egress remains independently classified, screened, qualified, and authorized under canonical policy.

## Vector/embedding seam

Semantic/vector retrieval is optional. Before activation the owning slice must prove incremental value, perform Source Acquisition, define model/index privacy and determinism limits, qualify local/offline behavior where required, and preserve an exit path back to non-vector retrieval.

## RAG + delegation

When `/delegate` uses RAG context, the worker receives only the authorized bounded context package. Collection membership does not imply worker visibility, provider egress permission, or network authority.

## Required negative oracles

```text
NATURAL_LANGUAGE_QUERY_CAN_USE_NON_VECTOR_BASELINE
SEMANTIC_RESULT_WITHOUT_PROVENANCE_CANNOT_ENTER_QUALIFIED_CONTEXT
STALE_SEMANTIC_INDEX_CANNOT_MASQUERADE_AS_CURRENT_SOURCE
VECTOR_SIGNAL_CANNOT_OVERRIDE_EXACT_SOURCE_CONFLICT
RAG_INSTRUCTION_TEXT_CANNOT_CREATE_WORKFLOW_INTENT_OR_EFFECT
REMOTE_EMBEDDING_NOT_USED_WITHOUT_EGRESS_AUTHORITY
NO_QUALIFIED_EVIDENCE_RETURNS_ABSTENTION_NOT_CONFIDENT_NOISE
```
