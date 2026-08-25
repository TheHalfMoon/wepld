# WePLD Agent Control Plane — Major Architecture & Source Reconnaissance

```text
DOCUMENT_CLASS = MAJOR_ARCHITECTURE_RECONNAISSANCE / PLAN_INPUT
DATE = 2026-08-24
CANONICAL_BASE = 08a06e9f2664735eb55db5b2f49f95d3d3f91c3f
CURRENT_CANONICAL_PLAN = V2.2
PLAN_ENRICHMENT_CANDIDATE = V2.3-AGENT-CONTROL-PLANE
FROZEN_402_REGISTRY_MUTATION = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
DONOR_EXECUTION = NONE
```

## Executive decision

The research supports a stronger product interpretation:

> **WePLD is a Universal Engineering Intelligence System whose execution surface is an Agent Development Control Plane.**

The control plane must keep agent hosting, project intelligence, security evidence, containment, review, and effect authority separate:

1. **Work / Evidence Timeline** — durable engineering sessions and evidence.
2. **Mission Runtime / Edara** — provider-neutral agent/session hosting and minimum-sufficient topology.
3. **UWC** — normalized worker/protocol edge.
4. **Mirefa** — capability and route qualification.
5. **Nawat** — effect-time authority, approval, transform, expiry and revalidation.
6. **Fehrest.Maemar** — semantic project/code/architecture intelligence.
7. **AMAN** — deterministic, graph and dynamic security/risk evidence.
8. **Assurance** — independent evaluation, never completion authority.
9. **Trusted Completion** — governed completion decision after evidence reconciliation.

Protocol compatibility, model confidence, reviewer consensus, retrieval scores, sandboxing and permission prompts are evidence/mechanisms; none mint Nawat authority.

## Major 2026 convergence

The research covered agent/session protocols, editor agent hosts, repository code graphs, authorization engines, coding-agent runtimes, sandbox/containment systems, provenance/attestation standards and security-review patterns. The central conclusion is that WePLD should acquire solved mechanics behind its own contracts instead of inventing a monolithic agent runtime.

## Agent/session interoperability

### VS Code Agent Host + AHP

VS Code Code-OSS now contains a provider-neutral Agent Host architecture with a durable session/chat catalog, separate provider harnesses, capability-driven differences, replay/E2E infrastructure, and adapters for multiple coding agents. The architectural lesson is **represent, don't orchestrate**: the host records and routes provider-native sessions without absorbing provider-specific semantics.

WePLD mapping:

```text
Agent Host orchestrator    -> Mission Runtime / Edara
host session/chat catalog  -> Work
provider harness           -> UWC worker adapter
capabilities               -> Mirefa evidence
side-effect request        -> Nawat proposal
session event/history      -> Work evidence
```

`microsoft/agent-host-protocol` is a high-priority protocol/source quarry for synchronized multi-client session state.

### ACP

Agent Client Protocol is the preferred first candidate for coding-agent client interoperability. It belongs at the UWC edge, not in the authority core.

```text
ACP permission request != Nawat grant
ACP capability != Mirefa qualification
ACP connection != trusted worker identity
```

### MCP

MCP remains useful for tools/resources and evolving client/server interoperability. Its authorization and elicitation mechanisms do not become effect authority.

```text
MCP OAuth success != Nawat grant
MCP tool schema != safe tool
MCP server identity != trusted server
```

### A2A

A2A is complementary to ACP/MCP for future external peer agents. It should remain non-primary until local UWC, Nawat and Work session ownership are proven.

## Fehrest.Maemar — semantic Project Brain

The Project Brain should not be a vector-only RAG store. The research favors a layered, provenance-first semantic model.

### F0 — repository identity
Git commit/tree/blob identity, file modes, generated/provenance labels, manifest and workspace facts.

### F1 — incremental structure
Tree-sitter/ast-grep-class machinery for syntax, scopes, definitions, exact spans, structural queries and incremental update after edits.

### F2 — precise semantic index
SCIP-class language-neutral facts from compiler/LSP/indexer frontends: symbols, definitions, references, documentation and implementation relationships.

### F3 — normalized code/property graph
Code-Graph-RAG, Graphify and Code Property Graph lessons provide a useful normalized vocabulary:

```text
DEFINES
CALLS
REFERENCES
INSTANTIATES
IMPORTS
DEPENDS_ON_EXTERNAL
READS_FROM
WRITES_TO
FLOWS_TO
HAS_VULNERABILITY
```

Resource nodes should model filesystem, environment, network, database, sockets and standard streams. Every node/edge needs provenance/freshness/coverage sufficient to explain why WePLD believes the fact.

### F4 — AMAN overlays
Taint, source/sink, reachability, blast radius, external-effect resources and security findings overlay the structural graph.

### F5 — dynamic evidence
Runtime traces may decorate or add runtime-only edges. They never silently replace structural truth.

**Decision:** embeddings/vector search remain optional retrieval indexes. Canonical Project Brain facts must be locally reconstructible from source/indexer evidence.

## AMAN — staged security evidence

```text
AMAN L0 = deterministic lexical/config/secret rules
AMAN L1 = structural AST rules
AMAN L2 = graph reachability + taint/data-flow
AMAN L3 = independent model/agent investigation
AMAN L4 = runtime/dynamic evidence
```

CodeQL, Joern/CPG and OpenGrep are high-value semantic/security oracles and failure-corpus sources. They should initially be adapters/reference tools rather than mandatory core dependencies. A clean reviewer or graph query never becomes completion authority.

## Nawat — effect-time authority

The Microsoft Agent Governance Toolkit / Agent Control Specification is the most important newly discovered policy-engine quarry. Useful mechanics include:

- deterministic/stateless evaluation;
- complete host-supplied snapshots;
- fail-closed errors;
- intervention points around model and tool calls;
- normalized allow/warn/deny/escalate/transform-style verdicts;
- host enforcement separate from policy evaluation;
- conformance tests and canonical serialization.

WePLD preserves the stronger invariant: **Nawat owns authority semantics.** ACS is a machinery/spec/test quarry, not the owner of WePLD authority.

Cedar is the preferred first policy-engine candidate because it is Rust-native and schema-validatable. OPA/Rego remains an interoperability/enterprise adapter candidate.

Candidate Nawat request:

```text
principal
action
resource
context
capability_evidence
containment_evidence
provenance_evidence
freshness
requested_effect
```

Candidate decision:

```text
ALLOW
DENY
REQUIRE_APPROVAL
TRANSFORM
DEFER_OR_REQUALIFY
```

Authority must be scoped and revalidated when relevant evidence, worker, resource, context or containment state changes.

## Mission Runtime / Edara

High-value runtime quarries:

- VS Code Agent Host — provider-neutral sessions and multi-chat ownership;
- DeepSeek Harness — replaceable plugin seams and append-only event/session mechanics;
- OpenAI Codex — Rust command/sandbox/approval boundary mechanics;
- OpenHands — event/workspace/runtime abstraction;
- Goose/Cline/Aider-class systems — provider-neutral harness ergonomics, recovery and context patterns.

Required WePLD rule:

> **Represent, route and record; do not make the orchestrator the authority.**

Edara selects minimum-sufficient topology. Mirefa qualifies. Nawat authorizes effects.

## Containment

Containment and authorization are independent.

### Windows-first
Microsoft Process Sandbox/AppContainer and related process-tree/mitigation mechanisms are strategically important for the desktop-first path. Stronger VM isolation remains available when necessary.

### Linux/remote
- gVisor/runsc — application-kernel isolation;
- Firecracker — microVM boundary;
- OpenSandbox — Apache-licensed sandbox lifecycle/execution API patterns;
- E2B — Firecracker-based agent sandbox infrastructure quarry.

Daytona's current production core moved closed-source in 2026; use current architecture as reference only and treat historical public code as a stale quarry requiring exact rights/status review.

```text
permission prompt != containment
container != sufficient containment
sandbox != authorization
Nawat grant != sandbox escape protection
```

## Evidence Timeline / Quality Passport

Ordinary prompt history is insufficient. Work should connect:

```text
intent
 -> spec/plan identity
 -> worker/session identity
 -> context/retrieval evidence
 -> proposed action
 -> Mirefa qualification
 -> Nawat decision
 -> containment state
 -> tool/process effect
 -> ChangeUnit
 -> AMAN/Assurance findings
 -> tests/benchmarks
 -> repair/retry
 -> finding reconciliation
 -> Trusted Completion decision
```

OpenTelemetry GenAI spans are an optional observational export. in-toto/SLSA-inspired attestations are useful for signed/material/product provenance. Canonical local evidence must not depend on a hosted telemetry backend.

## Tier-1 reproducible reconnaissance pins

| Candidate | Exact reconnaissance anchor | Rights/status at reconnaissance | Primary quarry | Proposed owner |
|---|---|---|---|---|
| `microsoft/vscode` | `7c54fda801c73e35072ac759b6d93f8c69c65d7b` | MIT | Agent Host contracts/state/adapters/replay corpus | Mission Runtime / Edara |
| `microsoft/agent-host-protocol` | `c058e213d8ed610cc011a8de2cfe20dd3f8dda84` | MIT | synchronized shared-session protocol | Work / UWC |
| `agentclientprotocol/agent-client-protocol` | `62c74ac119ec3296809496482440afca69926ce9` | Apache-2.0 | coding-agent edge protocol | UWC |
| `a2aproject/A2A` | `16ba52690519bf55b9388e34d4db356efa88aa51` | Apache-2.0 | future external agent-to-agent protocol/TCK | UWC future |
| `vitali87/code-graph-rag` | `79abdb5fdbcde6d138db071efbe61e9afc16f63d` | MIT | graph schema/parsers/calls/resources/data-flow/tests | Fehrest.Maemar / AMAN |
| `Graphify-Labs/graphify` | `91f4d120b630ee35c79bf3c75ccd186870a808f9` | MIT declared in `pyproject.toml`; standalone root license file not established; rights qualification pending | deterministic local graph/build hooks/failure corpus | Fehrest.Maemar |
| `microsoft/agent-governance-toolkit` | `b5705588883fac48b88cbe6fd0bd7d48c798453e` | MIT | ACS runtime/spec/conformance/intervention mechanics | Nawat |
| `cedar-policy/cedar` | `ba579ee7e9d63afa73a5b59be0d338a404c6108b` | Apache-2.0 | Rust fine-grained authorization | Nawat |
| `openai/codex` | `339751715c64496cb86246bfb3935f40e309dd3d` | Apache-2.0 | Rust sandbox/approval/command boundaries | Mission Runtime / Nawat |
| `deepseek-ai/deepseek-harness` | `b150a551b8d465e31e418e1b2eaf5e79bbb7d28e` | MIT repo metadata | event/plugin/context/recovery mechanics | Mission Runtime |

Pins establish reproducible reconnaissance identity only. They are not source admission, dependency selection or security qualification.

## Tier-2 path-mining queue

Pin and qualify only when the owning capability activates:

- Tree-sitter;
- ast-grep;
- SCIP and precise-code-navigation indexers;
- Joern / Code Property Graph;
- OpenGrep;
- OPA/Rego;
- OpenHands;
- Goose;
- Cline;
- Aider;
- OpenSandbox;
- gVisor;
- Firecracker;
- E2B infrastructure;
- in-toto;
- SLSA;
- OpenTelemetry.

Each future mining gate must inspect exact source/tests/failure modes/rights/notices/dependencies/security/portability/maintenance and exit strategy.

## Reference-only / negative oracles

- `anthropics/claude-code`: plugin, review, hook and security behavior is valuable, but the current repository license is All Rights Reserved / commercial terms. **No source admission from this reconnaissance.**
- Daytona current production implementation: current source is closed; architecture/reference only unless an exact separately licensed source surface is established.
- OpenCode-style permission UX: useful negative lesson because prompts/permissions are not containment.
- commercial cross-file analyzers: behavior/evaluation reference only unless separately licensed.

## Roadmap impact — no renumbering

Preserve P0 + S1..S10. Enrich existing slices:

- **S2:** immutable project/repository identity and evidence-store primitives.
- **S3:** effect envelope, process identity, containment report and Nawat PEP seam.
- **S4:** semantic graph foundation.
- **S5:** graph-informed Spec Kit scope and blast-radius evidence.
- **S6:** Agent Host/UWC adapters/Mirefa/Edara/Nawat.
- **S7:** AMAN graph-backed security and Assurance integration.
- **S8:** controlled repair with scoped grants, containment, replay and reassignment.
- **S9:** Evidence Timeline, attestation and recovery evidence.
- **S10:** dynamic graph/cross-project intelligence and Byan analytics.

Add bounded non-primary gates:

```text
S4-G  = SEMANTIC_PROJECT_GRAPH_FOUNDATION
S6-AH = AGENT_HOST_INTEROPERABILITY
S6-N  = NAWAT_EFFECT_TIME_AUTHORITY
S7-S  = AMAN_SECURITY_GRAPH
S9-P  = EXECUTION_PROVENANCE_AND_EVIDENCE_TIMELINE
```

## Rejected shortcuts

1. Forking VS Code as the WePLD product.
2. Making Memgraph/Neo4j mandatory canonical storage.
3. Treating vector RAG as Project Brain truth.
4. Letting ACP/AHP/MCP permission UX grant effects.
5. Treating a container as sufficient containment.
6. Sending all code/context to hosted models by default.
7. Making ACS/Cedar/OPA or any donor the authority owner.
8. Copying Claude Code source under its current license.
9. Building a custom universal agent protocol before ACP/AHP/A2A mining.
10. Introducing every candidate dependency in one slice.

## Next governed work

This dossier supports a V2.3 planning candidate only. Before implementation:

1. complete Spec Kit 003;
2. run Ponytail FULL against proposed abstractions;
3. perform capability-triggered path-level Source Acquisition;
4. select minimum reuse vs reimplementation;
5. produce exact dependency/SBOM/license/security evidence;
6. implement only the owning slice's minimum;
7. preserve Nawat/Fehrest/Assurance authority separation in negative tests.

No donor source, dependency, model/provider, sandbox or runtime execution is authorized by this reconnaissance.
