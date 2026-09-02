# Contract — Retrieval / RAG Boundary

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
VECTOR_DEPENDENCY_ADMISSION = NONE
```

## Purpose

Define a universal, provenance-first retrieval boundary for user-selected knowledge without making any retrieval engine, vector database, embedding model, parser, or remote service the Project Brain.

The canonical `KnowledgeCollection`, `KnowledgeSource`, `RetrievalEvidence`, and `ContextPackage` field vocabulary is defined in `../data-model.md`.

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

The product intent is broad user choice; the implementation must fail closed on unsupported, unsafe, over-limit, unauthorized, or unqualified source classes.

## Source access and visibility propagation

Every source and derived projection carries a current access-policy reference. Collection scope is not sufficient by itself.

Access propagation is monotonic toward narrower visibility:

```text
SOURCE_ACCESS
  -> SOURCE_GENERATION
  -> CHUNK/LEXICAL/VECTOR/GRAPH_PROJECTION
  -> RetrievalEvidence
  -> ContextPackage
  -> WORKER/PROVIDER/REVIEWER EGRESS ELIGIBILITY
```

A derived projection may narrow visibility but MUST NOT broaden it.

```text
COLLECTION_MEMBERSHIP != VISIBILITY_AUTHORITY
INDEX_ENTRY_PRESENT != CURRENT_ACCESS_PERMISSION
CONTENT_HASH_STABLE != ACCESS_STILL_ALLOWED
```

If source permission is revoked, collection visibility narrows, provider authorization is lost, or content is redacted/tombstoned, affected derived projections become ineligible for new retrieval/context/egress until the current access state is reconciled.

Old historical evidence may retain non-sensitive identity/provenance where policy permits, but protected content cannot remain exposed through stale caches.

## Generation and publication model

Source refresh uses immutable complete generations and atomic publication of the selected current generation.

```text
SOURCE_GENERATION = IMMUTABLE_COMPLETE_VIEW
PROJECTION_GENERATION = BOUND_TO_ONE_SOURCE_GENERATION
ACTIVE_GENERATION_SWITCH = ATOMIC_AFTER_VALIDATION
```

A query must not silently combine old and new chunks/index rows as if they were one current source generation.

Each derived chunk/projection must retain at least:

```text
source_id
source_generation
projection_kind
projection_generation
source_location_or_range?
content_identity
parser_or_index_identity
access_policy_ref
trust_classification
```

Removal/redaction produces explicit tombstone/revocation state and must propagate to derived indexes. Deletion of an index row is not sufficient audit evidence by itself.

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
7. freshness/access filters may exclude or downgrade stale or no-longer-visible evidence before context packing.

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
access-revoked-source exclusion
atomic-refresh generation transition
no-answer / abstention case
```

For every query the benchmark records whether the system retrieved a source containing the required evidence, whether the citation/location is inspectable, whether stale/conflicting/inaccessible evidence was surfaced, and whether it abstained when qualified evidence was absent.

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

Every material result must include or reference the canonical `RetrievalEvidence` fields, including:

```text
source_id
source_generation
projection_generation?
source_kind/source identity via source ref
exact_location_or_citation?
freshness_state
retrieval_signals[]
rank_or_score_observations[]
parser_or_index identity
access_policy_ref
trust_classification
retrieved_at/created_at
```

Scores are evidence only:

```text
RETRIEVAL_SCORE != TRUTH
RERANK_SCORE != TRUTH
EMBEDDING_DISTANCE != TRUTH
CITATION != AUTHORITY
```

## Freshness

A source/index generation must make freshness inspectable. Missing, stale, inaccessible, revoked, tombstoned, or conflicting source state must be surfaced explicitly. A retrieval path that requires current evidence cannot silently substitute a stale generation.

## Context packaging and untrusted content

Downstream workflows/workers receive bounded `RetrievalEvidence` references or a derived minimum-sufficient canonical `ContextPackage`. The package must preserve citations/provenance/access/trust labels and should avoid dumping entire collections when smaller evidence is sufficient.

Retrieved content remains untrusted data unless its origin is a controlling WePLD/user policy channel. Embedded instructions, tool requests, fake policy text, or workflow commands inside sources do not become `WorkflowIntent` and cannot expand worker access/effects.

Context eligibility is rechecked at package use/egress time. A package built before access revocation is stale for future transmission.

## Remote URL/documentation source boundary

`url` and `documentation_site` are source kinds, not implicit network grants. Before live remote ingestion is authorized, the owning network/source gate must define and test at least:

```text
exact requested URL/origin scope
scheme allowlist
redirect count and redirect-origin policy
DNS resolution and rebinding handling
loopback/link-local/private/metadata-service address policy
proxy policy
credential/header forwarding policy
cookie/auth isolation
response size/time/content-type bounds
archive/decompression/parser bounds
TLS/certificate policy where applicable
robots/legal/product policy where applicable
cache/freshness identity
```

The fetcher must fail closed on redirects or resolution changes that leave the authorized target scope.

```text
URL_TEXT_PRESENT != NETWORK_AUTHORITY
REDIRECT_TARGET != AUTHORIZED_TARGET
PUBLIC_HOSTNAME != PUBLIC_IP_PROVEN
AUTH_HEADER_FOR_SOURCE_A != AUTHORIZED_FOR_REDIRECT_B
```

## Privacy / egress

Adding content to a local collection does not authorize sending it to a remote embedding/model/retrieval provider. External egress remains independently classified, screened, qualified, and authorized under canonical policy.

Derived embeddings/index rows are also governed content and inherit current access/handling policy; they are not automatically safe to export merely because they are not plain text.

## Vector/embedding seam

Semantic/vector retrieval is optional. Before activation the owning slice must prove incremental value, perform Source Acquisition, define model/index privacy and determinism limits, qualify local/offline behavior where required, preserve source/access/generation provenance, and preserve an exit path back to non-vector retrieval.

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
SOURCE_ACCESS_REVOCATION_EXCLUDES_DERIVED_RETRIEVAL
OLD_CONTEXT_PACKAGE_CANNOT_BYPASS_CURRENT_ACCESS_POLICY
MIXED_REFRESH_GENERATIONS_CANNOT_MASQUERADE_AS_CURRENT
TOMBSTONED_SOURCE_CONTENT_CANNOT_SURVIVE_IN_SEARCHABLE_CACHE
REMOTE_URL_CANNOT_REACH_UNAUTHORIZED_PRIVATE_TARGET
REDIRECT_CANNOT_ESCAPE_AUTHORIZED_ORIGIN_SCOPE
DNS_REBINDING_CANNOT_EXPAND_TARGET_SCOPE
SOURCE_CREDENTIALS_CANNOT_LEAK_TO_REDIRECTED_OR_UNRELATED_TARGET
```
