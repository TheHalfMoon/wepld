# Clarifications — IssueOps Agentic Engineering Control Plane

```text
STATUS = RESOLVED_FOR_PLANNING
IMPLEMENTATION_AUTHORITY = NONE
```

## Founder intent captured

1. WePLD should become the best place to deal with GitHub issues and later other issue systems.
2. The experience should be highly automated and agentic, while remaining governed.
3. Users should have a universal `/rag` capability for arbitrary supported knowledge sources.
4. CLI/Desktop intake should support drag/drop or equivalent path-paste normalization.
5. The complete useful behavior set studied from `mattpocock/skills` should be adapted into WePLD-native workflows and internal primitives rather than copied with donor branding.
6. `amElnagdy/delegate-skills` should inform provider/agent switching and delegation, but WePLD should expose a provider-neutral `/delegate` and worker catalog rather than one command per provider.

## Resolved product decisions

### Q1 — Is GitHub the internal issue model?

No. GitHub is the first provider adapter. The canonical internal abstraction is a WePLD `Case`.

### Q2 — What does “automated” mean?

Automation means WePLD may progress a case through the maximum currently authorized lifecycle without routine human prompts. It does not mean unconditional write/merge/close authority.

### Q3 — What should reach the human?

Only genuine decision boundaries, approval requirements, unresolved ambiguity, externally blocked state, or residual risk that cannot be safely resolved by evidence and policy.

### Q4 — Does an autonomy profile grant effects?

No. `observe|triage|prepare|execute|land` constrains workflow behavior. Nawat still owns effect-time authorization and revalidation.

### Q5 — What is `/askme`?

The primary workflow router. It determines which qualified WePLD capability or workflow best matches the user's intent and current case/project state.

### Q6 — What is `/btw`?

A context-aware re-explanation capability: restate the current result, blocker, plan, or project state more clearly without altering authority or execution state.

### Q7 — Is every Matt skill a slash command?

No. High-value user intents become WePLD-native commands. Reusable engineering methods become internal primitives invoked by workflows.

### Q8 — Is `/delegate` the same as `/handoff`?

No. `/delegate` assigns bounded work. `/handoff` transfers durable context/session responsibility. Both use WePLD-owned identity/evidence contracts.

### Q9 — Can a user force a provider?

A user can request a worker/provider, but the request cannot bypass qualification, containment, cost policy, or Nawat authorization.

### Q10 — Does a drag/drop event perform an action?

No. A drop/paste is normalized into inert `InputArtifact` input. Follow-on actions such as inspect, attach, add-to-RAG, open-project, or execute remain explicit and separately governed.

### Q11 — How should terminal drag/drop work?

The portable CLI baseline should recognize quoted/escaped path paste and bracketed-paste behavior produced by common terminals. Native Desktop/embedded-terminal drop events should normalize to the same `InputArtifact` contract. No terminal-specific behavior becomes the core abstraction.

### Q12 — Can `/rag` ingest anything?

The product intent is “whatever the user wants,” subject to supported/qualified parsers, source access, size/resource policy, content classification, and effect authority. Unsupported or unsafe input must fail closed rather than be guessed.

### Q13 — Is RAG authoritative?

No. Retrieval is advisory evidence. Results must be provenance-first and freshness-aware; `RETRIEVAL_SCORE != TRUTH` remains controlling.

### Q14 — When should vector search be added?

Only after the owning Fehrest slice performs Ponytail FULL and Source Acquisition. Exact/lexical and structured project facts should not be displaced by an unnecessary vector dependency.

### Q15 — How should issue duplicates be represented?

As evidence-backed relationships between Cases (exact duplicate, probable duplicate, common-root-cause candidate, blocked-by, supersedes, regression-of), with confidence/evidence separate from provider labels.

### Q16 — Can WePLD close an issue because a PR merged?

No. Merge and provider closeout are effects and state transitions, not Trusted Completion. Completion requires the governing evidence and acceptance criteria.

### Q17 — How should external paid/quota agents behave?

Worker descriptors must expose cost/metering. If policy does not authorize paid/quota consumption, execution fails closed; no silent spend or fallback.

### Q18 — Does this planning candidate change S2?

No. It intentionally adds no S2 product scope and grants no implementation/source/network/model/provider/Git/issue-write authority.
