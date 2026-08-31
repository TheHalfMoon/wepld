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

## Retrieval ladder

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

No signal is mandatory unless required by the owning slice/task. Exact/lexical/structured retrieval should remain usable without semantic/vector machinery.

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

## Context packaging

Downstream workflows/workers receive bounded `RetrievalEvidence` references or a derived minimum-sufficient context package. The package must preserve citations/provenance and should avoid dumping entire collections when smaller evidence is sufficient.

## Privacy / egress

Adding content to a local collection does not authorize sending it to a remote embedding/model/retrieval provider. External egress remains independently classified, screened, qualified, and authorized under canonical policy.

## Vector/embedding seam

Semantic/vector retrieval is optional. Before activation the owning slice must prove incremental value, perform Source Acquisition, define model/index privacy and determinism limits, qualify local/offline behavior where required, and preserve an exit path back to non-vector retrieval.

## RAG + delegation

When `/delegate` uses RAG context, the worker receives only the authorized bounded context package. Collection membership does not imply worker visibility, provider egress permission, or network authority.
