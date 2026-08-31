# Plan — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CANDIDATE
CANONICAL_BASE = 573670eca575a5972e52b623b01b3143d036d281
CURRENT_ACTIVE_SLICE = S2
ROADMAP_REMAP = NONE
IMPLEMENTATION_AUTHORITY = NONE
```

## 1. Objective

Build WePLD into the governed operating environment where humans and agents can take an engineering issue from discovery to verified completion with the least necessary human intervention. The system must unify issue operations, arbitrary knowledge retrieval, artifact intake, workflow skills, worker delegation, assurance, and evidence without collapsing qualification, authorization, provider state, and completion into one concept.

## 2. Product architecture

```text
External issue/ticket/error sources     Drag/drop / paste / URL / repo / files
              |                                      |
              v                                      v
      Provider Adapters                         Input Intake
              |                                      |
              +------------------+-------------------+
                                 v
                         Universal Case / Work
                                 |
                  +--------------+---------------+
                  |                              |
                  v                              v
             Fehrest / RAG                 Workflow Engine
                  |                              |
                  +--------------+---------------+
                                 v
                         Edara task topology
                                 |
                         Mirefa qualification
                                 |
                          Nawat decision
                                 |
                         Mission Runtime
                                 |
                      UWC worker adapters
                                 |
                   qualified agent/tool workers
                                 |
                                 v
                         Evidence Timeline
                                 |
                        Assurance / Review
                                 |
                       bounded repair loop
                                 |
                      Trusted Completion
                                 |
                    provider land / closeout
```

## 3. Core domain contracts

### 3.1 `Case`

Stable WePLD identity for one engineering concern. Carries provider bindings, normalized lifecycle state, severity/priority evidence, relations, decisions, attempts, work graph, findings, and completion evidence.

### 3.2 `ProviderBinding`

Links a `Case` to GitHub issue/PR, GitLab, Linear, Jira, Sentry-class incident, chat/email report, or another provider object. Provider identity/state is preserved exactly but never substitutes for WePLD identity/state.

### 3.3 `InputArtifact`

Inert normalized reference produced by drag/drop, path paste, clipboard, selection, URL input, or provider attachment. Includes source kind, observed path/URI, content identity when available, classification state, size/type metadata, and qualification status.

### 3.4 `KnowledgeCollection`

Named RAG/retrieval scope with explicit membership, source provenance, parser/index generations, freshness state, visibility scope, and optional project binding.

### 3.5 `RetrievalEvidence`

One explainable retrieval observation containing source identity, exact location/citation where possible, ingest/index generation, freshness, retrieval methods/signals, and rerank trace sufficient for inspection.

### 3.6 `WorkflowIntent`

Normalized user or system intent behind `/askme`, `/issues`, `/rag`, `/build`, `/debug`, `/review`, `/delegate`, and other surfaces. Commands map to capabilities; they do not carry authority themselves.

### 3.7 `WorkerDescriptor`

Stable WePLD worker identity plus adapter/provider identity, capabilities, supported effect classes, containment characteristics, session semantics, cost/metering class, availability, and current qualification evidence.

### 3.8 `Assignment` and `Attempt`

Assignment is durable bounded work with acceptance criteria, dependency edges, context package, and authority envelope. Attempt records one execution by one qualified worker/session. Retries and reassignment create new attempts instead of rewriting history.

### 3.9 `DecisionBoundary`

A durable question that genuinely requires human/policy authority: product behavior, architecture contract, security/risk acceptance, external approval, unresolved ambiguity, cost authority, or other non-inferable choice.

### 3.10 `CompletionEvidence`

Evidence bundle used by Trusted Completion. External merge/close/status is an observation/effect, never the decision itself.

## 4. Case lifecycle

The internal lifecycle should be explicit and replayable:

```text
DISCOVERED
-> NORMALIZED
-> TRIAGED
-> REPRODUCTION_READY
-> DIAGNOSED
-> PLANNED
-> EXECUTION_READY
-> IN_PROGRESS
-> VERIFYING
-> REVIEWING
-> REPAIRING (optional loop)
-> LAND_READY
-> LANDED
-> CLOSEOUT_READY
-> CLOSED_EXTERNAL
-> COMPLETION_REVIEW
-> COMPLETED_TRUSTED
```

Orthogonal states:

```text
BLOCKED
NEEDS_DECISION
WAITING_EXTERNAL
STALE_EVIDENCE
CANCELLED
SUPERSEDED
```

A provider issue may be closed while the WePLD Case is not `COMPLETED_TRUSTED`, and vice versa until provider closeout is authorized.

## 5. IssueOps design

### 5.1 GitHub-first adapter

Start with GitHub Issues + PRs as the reference provider adapter. Separate capabilities:

- read issue/PR metadata and timeline;
- read linked commits/checks/reviews;
- post comments;
- labels/assignees/milestones;
- create/update PRs;
- merge;
- close/reopen issue;
- reactions and review-thread operations.

Each write capability must have a separate effect class and exact target/precondition. Read access must not imply write access.

### 5.2 Backlog sweep

`/issues sweep` should produce an evidence-backed frontier rather than merely rank tickets. Planned outputs:

- exact/probable duplicate clusters;
- common-root-cause groups;
- already-fixed-on-main candidates;
- reproduction-missing cases;
- decision-blocked cases;
- dependency-blocked cases;
- security-sensitive cases;
- small/high-confidence execution candidates;
- high-impact/high-risk cases needing deeper planning.

### 5.3 Case room

A case room should show:

```text
Case identity + provider links
current lifecycle state
autonomy profile
work graph / frontier
active workers and attempts
retrieved evidence
reproduction/root-cause evidence
decision boundaries
CI/test/security/review state
findings and reconciliation
landing/closeout state
completion evidence
```

## 6. RAG / Project Brain plan

### 6.1 Command surface

```text
/rag create <name>
/rag use <name>
/rag add <source>
/rag add --text <text>
/rag list
/rag inspect
/rag refresh
/rag remove <source>
/rag clear
/rag ask <question>
```

Potential scoped references:

```text
@rag:<collection>
--scope session|project|workspace|global
```

### 6.2 Source classes

Planned source classes include files, directories, text, code repositories, Markdown, PDF, structured text/data, logs, URLs/documentation, and later qualified additional parsers. “Anything” means any source with a qualified parser/access path; unsupported formats fail closed.

### 6.3 Retrieval ladder

Prefer the minimum sufficient mechanism:

1. exact path/name/key lookup;
2. lexical/full-text search;
3. structured metadata filters;
4. Fehrest syntax/symbol/reference/call-graph evidence;
5. optional semantic/vector retrieval;
6. optional reranking;
7. context packing.

Vector storage or embeddings are not prerequisites for the first useful `/rag` capability.

### 6.4 Provenance

Every material result should answer:

- what source produced this?
- which version/generation was indexed?
- where exactly was the match?
- when was it observed?
- which retrieval signals selected it?
- is the source stale, missing, or conflicting?

## 7. Drag/drop and artifact intake

### 7.1 Portable CLI baseline

Many terminals express a file drop as quoted/escaped path text. The CLI should have a path-paste resolver that safely recognizes candidate paths without executing them. Bracketed paste should be used when available to distinguish paste from typed input.

### 7.2 Native Desktop

Native file/directory/URL drop events should map directly to the same `InputArtifact` contract.

### 7.3 Intake actions

After normalization, the UI may offer:

```text
Inspect
Ask about it
Add to RAG
Attach to Case
Attach to Spec/Task
Compare
Open as Project
```

No action is implied by the drop itself.

## 8. WePLD-native workflow layer

### 8.1 Primary commands

```text
/askme       workflow/capability router
/btw         context-aware re-explanation
/issues      Case/IssueOps entrypoint
/rag         knowledge/retrieval workspace
/triage      issue/PR/problem classification and frontier
/grill       decision-boundary interrogation
/architect   codebase/domain/boundary design
/spec        specification synthesis
/tickets     tracer-bullet work/dependency decomposition
/build       governed implementation
/debug       reproduce/diagnose/regression workflow
/review      independent correctness/engineering review
/prototype   bounded throwaway experiment
/research    source-backed investigation
/wayfinder   decision map for foggy large work
/handoff     context/session responsibility transfer
/teach       durable learning workflow
/questionnaire structured external decision capture
/wizard      human-only setup/migration flow
/retro       environment/workflow improvement
/workflow    recurring/checkpointed workflow definition
/delegate    bounded work assignment
/workers     worker catalog/qualification view
```

### 8.2 Internal primitives adapted from the Matt skills study

Internal capabilities should include TDD, feedback-loop-first diagnosis, domain vocabulary, deep-module analysis, interface/seam discipline, intent-preserving merge resolution, spec-vs-standards review axes, tracer-bullet planning, context-load reduction, progressive disclosure, decision-tree grilling, reusable handoff packaging, and learning/retro mechanics.

The user-facing product should not expose donor branding as architecture.

## 9. Delegation and worker interoperability

### 9.1 Unified delegation

Avoid one product command per provider. Use:

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
```

### 9.2 Routing flow

```text
intent/task
-> capability/effect requirements
-> Edara candidate topology
-> Mirefa qualification
-> Nawat grant/revalidation
-> Mission Runtime attempt
-> UWC adapter
-> provider/agent execution
-> normalized events/results
-> evidence
-> Assurance
-> Trusted Completion
```

### 9.3 Worker safety

Adapters must declare whether “read-only” is enforceable or advisory. Provider flags such as sandbox/read-only/yolo/full-trust cannot be treated as equivalent security boundaries. WePLD containment evidence and Nawat effect policy remain controlling.

### 9.4 Cost and availability

Worker routing must include availability and cost/metering. No automatic paid/quota fallback. If the requested route cannot run under policy, the assignment becomes blocked or requires an explicit alternative.

## 10. Autonomy model

Repository/workspace profile:

```text
observe  = ingest/read/analyze only
triage   = observe + classify/dedupe/reproduce-plan recommendations
prepare  = triage + build proposed changes/artifacts/PR drafts where authorized
execute  = prepare + execute qualified effects/tests/repairs
land     = execute + authorized merge/provider closeout workflow
```

Each individual effect remains Nawat-gated. A profile is a ceiling, not a grant.

## 11. Roadmap placement

This plan preserves P0 + S1..S10 and maps capabilities to existing owning slices.

### S2 — prerequisites only

Use local project identity and durable evidence-store foundations. Do not pull IssueOps/RAG/agent-host scope backward.

### S3 — trusted intake and terminal fabric

- `InputArtifact` envelope;
- terminal path-paste/drop normalization;
- Desktop/CLI intake convergence;
- effect proposal/result envelopes needed by later IssueOps execution;
- process/containment foundations.

### S4 — Fehrest/RAG minimum

- content/source identity and freshness;
- lexical/exact retrieval;
- syntax/symbol/reference graph foundations;
- provenance-first retrieval evidence;
- named knowledge collections;
- optional semantic/vector seam without mandatory vector dependency.

### S5 — workflow/skill layer

- `/askme` router;
- `/btw` explanation state;
- `/rag` workflow UX over S4 contracts;
- `/triage`, `/grill`, `/architect`, `/spec`, `/tickets`, `/debug`, `/prototype`, `/research`, `/wayfinder`;
- internal Matt-derived primitives behind WePLD contracts;
- plan qualification and context-pack construction.

### S6 — agent host, delegation, and provider adapters

- Worker catalog;
- Mission Runtime;
- UWC normalized worker protocol;
- Mirefa route/capability qualification;
- Edara minimum-sufficient task topology;
- `/delegate`, `/workers`, `/handoff` worker targets;
- GitHub IssueOps read/write adapter candidate only after source/network/auth qualification;
- later issue-provider adapter seam.

### S7 — native IssueOps assurance

- independent review orchestration;
- security-sensitive issue classification;
- review finding normalization/reconciliation;
- evidence-backed triage and root-cause confidence;
- Case room assurance state;
- provider closeout preconditions.

### S8 — autonomous repair and landing

- bounded repair/retry/reassignment;
- dynamic teams;
- autonomous case progression under `execute|land` ceilings;
- exact-head PR landing safeguards;
- issue closeout effect;
- Trusted Completion gate.

### S9 — evidence/quality passport

- complete Case timeline;
- attempt/review/repair provenance;
- issue-to-change-to-test-to-review-to-closeout trace;
- replay/recovery and audit export.

### S10 — organization-scale Issue Intelligence

- multi-repository backlog sweeps;
- recurring root-cause analytics;
- duplicate/regression intelligence;
- cross-provider federation;
- outcome/throughput/quality analytics;
- optional advanced retrieval/reranking expansion.

## 12. Delivery strategy

Do not attempt a monolithic “autonomous GitHub engineer” implementation. Deliver vertical, authority-safe tracer bullets:

1. inert input artifact -> inspect;
2. Case import -> read-only triage;
3. local knowledge collection -> cited retrieval;
4. workflow router -> deterministic local capability selection;
5. one qualified local worker -> one bounded assignment;
6. GitHub read adapter -> normalized Case evidence;
7. GitHub prepare path -> draft/comment without landing;
8. implement/test/review loop -> no merge;
9. exact-authority landing on a controlled case;
10. autonomous sweep -> bounded multi-case frontier.

Each tracer bullet must preserve replayable evidence and negative tests for forbidden effects.

## 13. Source-acquisition strategy

The donor studies are research inputs only. Before reuse/import/adapter activation:

- register candidates in a separately governed future registry revision;
- pin exact revisions;
- verify licenses and relevant source paths;
- mine tests/failure modes/behavior rather than copying product branding;
- qualify security, portability, maintenance, containment, cost, and exit strategy;
- select the minimum reuse mode: behavior oracle, test/fixture acquisition, adapter idea, bounded source reuse, or reject.

## 14. Success measures

When the owning slices exist, evaluate:

- percentage of issues auto-triaged with inspectable evidence;
- duplicate/root-cause clustering precision;
- reproduction success rate;
- median human decision boundaries per completed Case;
- autonomous prepare/execute/land completion rate by autonomy profile;
- repair-loop convergence rate;
- stale-evidence and unsafe-effect prevention rate;
- retrieval citation/provenance coverage;
- worker route qualification/fallback-block rate;
- issue-to-Trusted-Completion lead time;
- regression/reopen rate after autonomous closeout.

Optimization MUST NOT reward unsafe closure volume over correctness, evidence quality, or authority compliance.

## 15. Activation rule

This planning candidate is not executable authority. Future work must activate each capability only in its owning slice through the mandatory Spec Kit, Ponytail FULL, Source Acquisition Check, deterministic gates, independent review, applicable security review, finding reconciliation, and authorized acceptance sequence.
