# Clarify — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CLARIFICATIONS
IMPLEMENTATION_AUTHORITY = NONE
```

## Resolved planning clarifications

### Q1 — Is GitHub the internal issue model?

No. GitHub is the first reference provider. WePLD owns a provider-neutral `Case` identity/lifecycle/evidence model.

### Q2 — Can provider state set Case completion?

No. Provider open/closed/merged/resolved state is evidence only. Trusted Completion is a separate governed decision.

### Q3 — How are conflicting provider observations handled?

Observations remain append-only. Generic latest-write-wins is prohibited for cross-provider semantics. Acceptance/effect paths that require one current semantic must re-observe, abstain/fail closed, resolve through an explicit rule, or open a DecisionBoundary. The losing/older evidence remains inspectable.

### Q4 — Does adding a new provider require expanding the Case schema?

Not by default. Provider-specific fields remain adapter observations/extensions. Core Case semantics evolve only when provider-independent engineering meaning is justified and the adapter/normalization migration is explicitly versioned.

### Q5 — Is `/issues sweep` allowed to produce opaque AI clusters?

No. Every output class must have inspectable evidence requirements and negative oracles. Probable duplicates cannot auto-close or merge Case identity. Common-root-cause requires causal evidence stronger than topic/semantic similarity. Recommendation thresholds are predeclared and measured against a labeled corpus.

### Q6 — Is semantic/vector retrieval a mandatory later step after lexical retrieval?

No. Retrieval signals are query/source aware, not a rigid sequence. Semantic/vector may be selected early for conceptual/paraphrastic queries or measured lexical recall gaps, but remains optional and requires predeclared incremental-value qualification before admission.

### Q7 — What is the minimum useful RAG capability?

A user can ingest qualified local sources into a named collection, ask natural-language/exact/code-reference questions, receive inspectable cited evidence, see stale/conflicting/no-answer states, and do so without requiring embeddings/vector infrastructure.

### Q8 — Can retrieved or provider content instruct agents?

Not merely by containing imperative text. External/retrieved/repository/browser/worker/model content is data by default. It cannot mint WorkflowIntent, authority, paid/remote routes, broader context access, review approval, or Trusted Completion. Prompt filtering is defense-in-depth; effect-time structural enforcement remains required.

### Q9 — Must Edara, Mirefa, Nawat, Mission Runtime, and UWC be separate services from the beginning?

No. They are semantic trust/ownership boundaries, not mandatory deployment units. Early implementations may co-locate them as direct modules/contracts. Their authority distinctions must remain enforceable and evidenced.

### Q10 — Can Mirefa qualification authorize execution?

No. Mirefa says whether a route is qualified for consideration. Nawat alone owns effect-time authority/revalidation. Mission Runtime may execute only within the exact current grant/containment constraints and cannot widen or silently substitute them.

### Q11 — Should delegation move into S5 to prove value sooner?

Only as a dry-run planning contract. S5 may construct Assignment/WorkerRequirement/TopologyProposal against synthetic workers. Real worker/model/provider/process execution and the full Edara/Mirefa/Nawat/Mission Runtime path remain S6-owned.

### Q12 — Should S7 and S8 be merged to tighten review/repair feedback?

No semantic merge. A tight feedback loop is desirable, but Assurance must remain independent from the repair/completion boundary consuming findings so `ReviewOutcome != CompletionDecision` remains structural.

### Q13 — What is the first IssueOps end-to-end tracer bullet?

TB0 is offline/read-only: synthetic/local issue artifact -> Case -> local repository identity -> cited local retrieval -> triage/reproduction-readiness/relations/decision frontier -> evidence-backed Case summary. No network, provider write, model/provider execution, Git write, merge, or issue close is required.

### Q14 — What must Trusted Completion prove?

It must bind exact accepted target/generation, deterministic gates, genuine independent review, security review or qualified not-applicable basis, all material finding reconciliations, material effect/authority evidence, provider closeout where required, residual limitations, and the completion decision producer. Stale/mismatched evidence or unresolved findings fail closed.

### Q15 — Are all proposed slash commands day-one primary UX?

No. The catalog describes native intent surfaces. Initial UX should expose a smaller primary set through `/askme` and progressive disclosure. Specialist worker controls such as `/workers` and `/handoff` may remain advanced until their owning capabilities exist.

### Q16 — Is WebMCP the same thing as ordinary MCP?

No. WePLD treats WebMCP as a browser/web-application interoperability protocol in which the current page exposes structured tools to agents. Ordinary MCP remains a broader tool/resource protocol edge. Neither protocol owns WePLD authority.

### Q17 — Is WebMCP already a stable W3C Standard?

No. The version observed during 2026-08-31 planning research is a Web Machine Learning Community Group Draft Report and explicitly states that it is not a W3C Standard and not on the W3C Standards Track. Its exact status and API surface must be reverified at Source Acquisition time.

### Q18 — Should WePLD support WebMCP?

Yes, as a replaceable qualified web-agent feature. WePLD should support both consuming website-exposed WebMCP tools and, later, exposing selected safe WePLD intent/read/proposal capabilities through WebMCP. Neither direction grants direct authority.

### Q19 — Are WebMCP and Chrome/Edge DevTools MCP one feature?

They belong to one web-agent product area but are separate capability paths. WebMCP exposes application-defined structured tools. DevTools-class MCP/browser adapters expose browser inspection/debugging/control. The same browser may support both, but WePLD must classify and authorize them separately.

### Q20 — Does a website declaring a WebMCP tool authorize WePLD to call it?

No. Tool discovery produces an untrusted `WebToolObservation`. Tool metadata, schemas, annotations, `read-only` hints, and outputs are evidence/claims only. Invocation requires independent effect classification, Mirefa qualification, Nawat exact-context authorization, containment, and explicit governing intent.

### Q21 — Does an already logged-in browser authorize actions?

No. Cookies, login state, SSO, autofill, password managers, and ambient browser sessions can embody powerful authority, but their presence is only an observation. `AUTHENTICATED_BROWSER != AUTHORIZED_ACTION` and `COOKIE_PRESENCE != USER_INTENT` are controlling invariants.

### Q22 — Can WePLD silently fall back if WebMCP fails?

No. It must not silently replace WebMCP with raw DOM click/type automation, DevTools actions, another browser/profile, headless/remote browser infrastructure, or a different provider. Any alternative route requires explicit qualification and governing authorization.

### Q23 — What is the first WebMCP/browser proof?

WEB-TB0 is offline/local and effect-free: local WebMCP fixture -> tool discovery observation -> untrusted metadata classification -> invocation preview -> evidence. WEB-TB1 then proves controlled local-browser discovery and tool-generation freshness without effectful invocation. Browser actuation is deferred until later qualified tranches.

## Deferred owning-slice decisions

The following remain intentionally deferred because this planning candidate does not have implementation/source/dependency authority:

- exact GitHub app/token/authentication model;
- webhook vs polling implementation and replay storage;
- exact parser implementations and archive/document policies;
- lexical index engine;
- vector database/embedding model, if benchmark-justified;
- first concrete worker/provider adapters;
- exact policy-engine/sandbox implementation;
- exact persistent event-store representation and retention thresholds;
- organization-scale scheduling/resource policy;
- numeric autonomy-promotion and sweep-action thresholds, which must be declared before their owning benchmark run;
- exact WebMCP revision/browser versions and client API shape;
- first browser diagnostics/control adapter;
- Chrome vs Edge vs WebView2 qualification details;
- local vs remote browser execution model;
- browser-profile isolation and credential integration details;
- whether WePLD publisher mode is enabled beyond safe read/intent/proposal tools.
