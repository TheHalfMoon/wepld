V1.5 directly resolves the conceptual boundary; no duplicate founder vote is required. Final aggregate/vocabulary ratification remains decision 4.

### 9.2 State ownership

| State | Canonical owner | Notes |
|---|---|---|
| Team/Project/Work coordination | Work/governance domain | Links to missions; does not execute |
| Specification, acceptance criteria, rigor profile | AGILLE | Spec Kit artifacts are inputs/projections, not authority |
| Mission/Plan/Task/Attempt/Lease | Mission Runtime | Durable state, idempotency, checkpoints, cancellation |
| Staffing/topology decision | Edara inside Mission Runtime | Decision record, not an authority grant |
| Capability/effect decision | Nawat | Revalidated at effect time |
| Security/risk observation | AMAN | Signal only |
| Project facts/context | Fehrest | Governed knowledge; informs only |
| Review evidence/outcome | Assurance | Not completion |
| CompletionDecision | Trusted Completion under authorized policy | Produces receipt and Work projection |

### 9.3 Recovery domains

Recovery separates source/working copy, Mission state, terminal/process state, knowledge/indexes, evidence/artifacts, authority/grants, audit, and external effects. A Git reset cannot be represented as undoing an external API action, leaked credential, policy decision, or irreversible effect. Uncertainty remains first-class until reconciled.

Review attaches to an immutable target and Attempt lineage. It never mutates Work state directly. Accepted completion may update Work through an authorized projection after the CompletionDecision receipt exists.

---

## 10. Mirefa / Edara / Nawat / UWC Reconciliation

### 10.1 Four-question separation

```text
Mirefa  Which routes/components are qualified, compatible, healthy, and measured?
Edara   Who should do what, in which minimum-sufficient topology, and when?
Nawat   What may each principal do now, to which resource, for which purpose?
UWC     How is every worker invocation normalized, bounded, evidenced, and recovered?
```

Edara remains deterministic Rust-owned decision logic inside Mission Runtime for Alpha, not a separate service, second runtime, manager-model authority, or hidden subagent spawner. Model output may propose staffing; Rust validates eligibility, graph, dependency readiness, write-set conflicts, depth, budget, route compatibility, and authority preconditions before persisting a decision.

### 10.2 Universal Worker Contract minimum

Every worker assignment carries:

- worker/adapter/model/provider/harness/substrate identity and immutable version/digest;
- parent and represented principals, Assignment/Task/Attempt/Lease IDs, delegation lineage and depth;
- immutable objective, acceptance-policy digest, ReviewPlan/ContextCapsule digest where applicable;
- requested capability distinct from the Nawat-issued grant;
- data classification and egress policy;
- filesystem, writer, process, network, secret, provider, and tool profiles;
- token, monetary, time, context, request, CPU/memory, and child budgets;
- ordered/idempotent lifecycle events and durable checkpoints;
- effect receipts, output/evidence/artifact manifests, cost records, and cancellation/expiry;
- a non-authoritative completion claim: satisfied, partial, blocked, abstained, failed, or nonconverged;
- uncertain-effect, orphan, resume, reassignment, fallback, and cleanup semantics.

A child may request delegation but cannot create an authoritative child Attempt or enlarge authority. The request returns through Edara, Mission Runtime, and Nawat.

### 10.3 Role-relative measurable independence

Independence is a graph of relationships relative to the accountable builder/reviewer roles, not a count of D1–D8 labels.

| Relationship | Required evidence |
|---|---|
| Accountable principal / Attempt | Distinct principal and Attempt identities where policy requires separation |
| Model snapshot and lineage | Exact model/version plus known training/fine-tune/shared-lineage facts; `NOT_PUBLICLY_DETERMINABLE` stays unknown |
| Provider/operator/control plane | Provider, operator, tenancy/control-plane identity and shared-failure relation |
| Information set | Builder-history exposure, intermediate reasoning availability, memory/cache/retrieval overlap, context digest, and visibility timing |
| Instruction stack | System/policy/prompt/skill/rule digests and shared derivation |
| Execution harness | Adapter/harness/substrate/tool-profile identity and common-mode failure |
| Evidence-source diversity | Compiler/test/scanner/runtime/human/AI sources reported separately from reviewer identity |

Profiles state required relationships. The run records achieved relationships. `UNKNOWN` never satisfies a required relationship. Different names or providers do not prove effective independence if control plane, model lineage, context cache, prompt, harness, and evidence sources remain common.

### 10.4 Ponytail topology rule

One qualified worker is the default. Another worker is admitted only if its expected marginal accepted-outcome value remains positive after coordination time, critical-path latency, duplicated context, budget, write conflict, independence need, verification, and synthesis overhead. Dissent is preserved; it is not averaged into false certainty.

---

## 11. Fehrest / Project Brain Architecture

### 11.1 Composition

```text
Project Brain
= governed structural/semantic facts
+ human-readable knowledge and portable projections
+ source/claim/evidence/decision ledgers
+ branch- and time-aware provenance
+ runtime/operational observations
+ architecture/security/design/research knowledge
+ Memory Completeness Ledger
```

Canonical knowledge is distinct from exact/lexical indexes, symbol graphs, embeddings, vector stores, graph databases, analytics engines, and UI canvases. Those are rebuildable or advisory. Fehrest admits, supersedes, invalidates, and explains knowledge; it does not authorize effects.

### 11.2 Minimum before serious worker-quality claims

S4 must provide local deterministic ContextCapsules from files, Git, exact text search, available symbol/reference facts, requirements/ADRs/docs/evidence links, and freshness/provenance. No cloud embeddings or mandatory vector database are allowed. A claim that review is “WePLD-grade” is inadmissible until the relevant Fehrest and AGILLE context conditions are available and explicitly measured.

### 11.3 Coverage and the Memory Completeness Ledger

