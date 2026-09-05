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
                    provider land / closeout
                                 |
                      Trusted Completion
```

### 2.1 Logical boundaries, not mandatory microservices

The named control-plane layers are semantic ownership/trust boundaries inherited from canonical V2.3. They MUST NOT be collapsed semantically, because topology/staffing, route qualification, effect authorization, execution hosting, evidence, and completion answer different trust questions.

They also MUST NOT force premature deployment complexity. Early tracer bullets may implement Edara, Mirefa, Nawat, Mission Runtime, and UWC as co-located modules in one Rust process, or as simple direct contracts, so long as:

- each boundary has a distinct typed input/output;
- qualification cannot return effect authority;
- Nawat remains the only effect-time authority;
- Mission Runtime cannot widen or mint grants;
- provider/worker state cannot become trusted completion;
- evidence can show which boundary produced each decision.

Promotion to separate services/processes is demand-driven by isolation, scaling, provider lifecycle, or containment needs—not by diagram fidelity.

## 3. Core domain contracts

### 3.1 `Case`

Stable WePLD identity for one engineering concern. Carries provider bindings, normalized lifecycle state, severity/priority evidence, relations, decisions, attempts, work graph, findings, provider-conflict state, and completion evidence.

### 3.2 `ProviderBinding`

Links a `Case` to GitHub issue/PR, GitLab, Linear, Jira, Sentry-class incident, chat/email report, or another provider object. Provider identity/state is preserved exactly but never substitutes for WePLD identity/state. Contradictory observations remain append-only evidence and may produce an explicit conflict state; they are not resolved by generic latest-write-wins logic.

### 3.3 `InputArtifact`

Inert normalized reference produced by drag/drop, path paste, clipboard, selection, URL input, or provider attachment. Includes source kind, observed path/URI, content identity when available, classification state, size/type metadata, and qualification status.

### 3.4 `KnowledgeCollection`

Named RAG/retrieval scope with explicit membership, source provenance, parser/index generations, freshness state, visibility scope, and optional project binding.

### 3.5 `RetrievalEvidence`

One explainable retrieval observation containing source identity, exact location/citation where possible, ingest/index generation, freshness, retrieval methods/signals, and rerank trace sufficient for inspection.

### 3.6 `WorkflowIntent`

Normalized user or system intent behind `/askme`, `/issues`, `/rag`, `/build`, `/debug`, `/review`, `/delegate`, and other surfaces. Commands map to capabilities; they do not carry authority themselves. Instructions present only inside issues, PRs, code, logs, documents, retrieved passages, or worker/model output do not become `WorkflowIntent`.

### 3.7 `WorkerDescriptor`

Stable WePLD worker identity plus adapter/provider identity, capabilities, supported effect classes, containment characteristics, session semantics, cost/metering class, availability, and current qualification evidence.

### 3.8 `Assignment` and `Attempt`

Assignment is durable bounded work with acceptance criteria, dependency edges, context package, and authority envelope. Attempt records one execution by one qualified worker/session. Retries and reassignment create new attempts instead of rewriting history.

### 3.9 `DecisionBoundary`

A durable question that genuinely requires human/policy authority: product behavior, architecture contract, security/risk acceptance, external approval, unresolved ambiguity, cost authority, or other non-inferable choice.

### 3.10 `CompletionEvidence`

Evidence bundle used by Trusted Completion. External merge/close/status is an observation/effect, never the decision itself.

A minimum material Case completion packet must bind the exact accepted target/generation and include, as applicable:

```text
accepted target identity
reproduction/root-cause evidence or explicit not-applicable basis
implemented/change identity
deterministic gate evidence
independent review identity bound to the accepted target
security review evidence or policy-qualified not-applicable basis
all material finding reconciliation evidence
effect/authority records for material external/process/Git effects
provider land/closeout observations where required
residual limitations/risk statement
completion decision + decision producer identity
```

Trusted Completion MUST fail closed when acceptance-critical evidence is stale, bound to another head/generation, internally contradictory, or leaves unresolved material findings.

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
CONFLICTED_PROVIDER_EVIDENCE
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

`/issues sweep` produces an evidence-backed frontier, not generic clustering prose. Every output class has an explicit derivation contract, evidence requirements, abstention behavior, and benchmark/negative-oracle corpus before it may influence automated writes.

#### 5.2.1 Exact duplicate candidates

Candidate signals, strongest first:

- explicit provider/user duplicate link;
- same external canonical object bound twice;
- exact normalized reproduction/error fingerprint plus matching affected target/component;
- exact canonical failure/test signature plus matching causal change/evidence.

Title/body similarity alone cannot establish `EXACT_DUPLICATE_OF`.

Negative oracle: two issues with near-identical wording but different reproduction signatures/affected components MUST remain separate.

#### 5.2.2 Probable duplicate candidates

Use an inspectable multi-signal evidence vector such as:

```text
normalized title/body lexical similarity
shared error/stack/test signatures
shared symbols/files/components
shared environment/version window
shared reproduction steps
shared implicated commit/change range
optional semantic similarity
```

The result remains `PROBABLE_DUPLICATE_OF` with evidence/confidence until a qualified workflow promotes it. Probable duplicates never auto-close another Case.

Validation records precision/recall/abstention on a labeled corpus. Any threshold used for automated downstream action is declared before evaluation under the owning slice.

#### 5.2.3 Common-root-cause groups

A common-root-cause group requires causal evidence stronger than text similarity. Candidate evidence includes:

- same deterministic failing test/reproduction;
- same normalized stack/error signature;
- same causal symbol/path/graph region;
- same introducing/fixing commit or bounded change range;
- same environment/config trigger with reproducing evidence.

A semantic topic cluster without causal evidence is labeled `RELATED_TOPIC`, not `COMMON_ROOT_CAUSE_WITH`.

Negative oracle: two authentication issues with different causal components must not be grouped merely because both mention authentication.

#### 5.2.4 Already-fixed-on-main candidates

A candidate requires a current canonical-main observation and at least one verification path:

- the recorded reproduction fails on the historical affected target and no longer fails on current main;
- an acceptance/regression test corresponding to the issue passes on current main and is linked to a fixing change;
- the exact implicated code/symbol/change evidence shows the repairing change is present, with no contradictory current reproduction evidence.

Absence of a referenced file or a closed PR alone is insufficient.

#### 5.2.5 Reproduction-missing

Classify as reproduction-missing when the Case lacks the minimum evidence required by its issue kind: reproducible command/test, deterministic fixture, bounded failure observation, or an explicit reason reproduction is infeasible. A narrative problem statement alone is not reproduction evidence.

#### 5.2.6 Decision-blocked / dependency-blocked

Decision-blocked requires an unresolved `DecisionBoundary`. Dependency-blocked requires an unresolved typed dependency whose completion/readiness is observable. Generic uncertainty is not silently converted into one of these states.

#### 5.2.7 Security-sensitive

Initial classification combines deterministic rules, affected-resource/security metadata, known sensitive paths/capabilities, provider security labels where qualified, and later AMAN evidence. Model judgment may add a candidate signal but cannot alone downgrade a deterministic security-sensitive classification.

#### 5.2.8 Small/high-confidence execution candidates

A Case is a candidate only when all required conditions are evidenced, for example:

```text
bounded affected scope
reproduction or deterministic acceptance oracle
no unresolved material decision boundary
no unresolved provider-state conflict relevant to the effect
qualified change/test path
risk/effect class within the owning autonomy profile
no security-sensitive escalation requirement
```

“Small” is based on bounded impact/effect evidence, not ticket length or estimated lines of code.

#### 5.2.9 High-impact/high-risk candidates

Use explicit severity/user-impact/security/blast-radius/dependency and uncertainty evidence. High ranking without evidence is prohibited.

#### 5.2.10 Sweep qualification and success criteria

Before recommendation-only sweep exits qualification:

1. maintain a labeled fixture corpus containing true/false duplicates, same/different root causes, already-fixed/not-fixed, blocked/not-blocked, and adversarially similar cases;
2. report per-output true positives, false positives, false negatives, abstentions, evidence coverage, and stale/conflicted-input handling;
3. prove every recommendation links to inspectable source evidence;
4. prove missing/contradictory evidence produces abstention or a weaker relation rather than fabricated certainty;
5. define promotion thresholds before benchmark execution;
6. keep bulk provider mutation disabled until a later owning slice separately qualifies mutation-specific precision/risk criteria.

Minimum negative oracles:

```text
SIMILAR_TEXT_DIFFERENT_CAUSE_NOT_EXACT_DUPLICATE
SEMANTIC_CLUSTER_NOT_CAUSAL_GROUP_WITHOUT_CAUSAL_EVIDENCE
CLOSED_PROVIDER_STATE_NOT_ALREADY_FIXED_PROOF
STALE_MAIN_OBSERVATION_NOT_ALREADY_FIXED_PROOF
PROBABLE_DUPLICATE_NEVER_AUTO_CLOSES
MODEL_ONLY_SECURITY_DOWNGRADE_DENIED
CONFLICTED_PROVIDER_STATE_FORCES_ABSTENTION_WHEN_REQUIRED
SWEEP_WITHOUT_EVIDENCE_RETURNS_UNKNOWN_NOT_GENERIC_RANKING
```

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
provider conflicts/staleness
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

`add --text` is syntax sugar for adding an inline-text `InputArtifact`; it is not a separate storage/authority path.

Potential scoped references:

```text
@rag:<collection>
--scope session|project|workspace|global
```

### 6.2 Source classes

Planned source classes include files, directories, text, code repositories, Markdown, PDF, structured text/data, logs, URLs/documentation, and later qualified additional parsers. “Anything” means any source with a qualified parser/access path; unsupported formats fail closed.

### 6.3 Retrieval signal selection

Retrieval is minimum-sufficient and query/source aware, not a rigid serial ladder:

1. exact path/name/key lookup when an exact identifier is present;
2. lexical/full-text for free text;
3. structured metadata filters;
4. Fehrest.Maemar syntax/symbol/reference/call-graph evidence for code semantics;
5. semantic/vector may be selected early for conceptual/paraphrastic queries, vocabulary mismatch, or demonstrated low lexical recall;
6. optional reranking/fusion;
7. freshness filtering and bounded context packing.

Vector storage or embeddings are not prerequisites for the first useful `/rag` capability. Conversely, the plan does not require semantic/vector to wait until all structured signals fail; it is a replaceable signal chosen when benchmarked query classes justify it.

The first useful RAG gate requires a representative natural-language corpus and cited retrieval across exact, lexical, code-symbol/reference, stale-source, cross-source, and no-answer cases. Semantic/vector machinery is admitted only after a predeclared benchmark demonstrates material incremental value for identified query classes and an acceptable privacy/cost/latency/exit profile.

### 6.4 Provenance

Every material result should answer:

- what source produced this?
- which version/generation was indexed?
- where exactly was the match?
- when was it observed?
- which retrieval signals selected it?
- is the source stale, missing, or conflicting?

### 6.5 Untrusted retrieval content

Retrieved text remains data. Embedded instructions do not become system/user policy, `WorkflowIntent`, tool intent, effect authority, review approval, or completion evidence merely because retrieval ranked them highly. Context packaging follows `contracts/untrusted-content.md`.

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

The command catalog describes intent surfaces, not a requirement to expose every command equally on day one. Initial UX should keep a small primary surface (`/askme`, `/issues`, `/rag`, `/build`, `/review`, `/btw`) and reveal specialist workflows through routing/progressive disclosure. `/delegate`, `/workers`, and `/handoff` may remain advanced surfaces until worker interoperability exists.

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

Internal capabilities should include TDD, feedback-loop-first diagnosis, explicit domain vocabulary/model scenarios, deep-module/boundary analysis, interface/seam discipline, intent-preserving merge resolution, spec-vs-standards review axes, tracer-bullet planning, context-load reduction, progressive disclosure, decision-tree grilling, reusable handoff packaging, and learning/retro mechanics.

`/architect` must make domain modeling and deep-module analysis explicit reusable modes rather than leaving them as donor-study notes only.

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

The exact typed handoffs, success/failure states, and no-authority-inheritance rules are defined in `contracts/worker-delegation.md`.

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

### S3/S4 checkpoint — intake to cited local knowledge

Before agent hosting, qualify one no-model/no-provider vertical integration:

```text
InputArtifact(local file/directory)
-> qualified local access/parser
-> KnowledgeCollection membership
-> exact/lexical retrieval
-> cited RetrievalEvidence
-> no execution/network/provider effects
```

This proves the intake/RAG seam before worker complexity enters.

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
- plan qualification and context-pack construction;
- **delegation dry-run contracts only**: construct Assignment/WorkerRequirement/TopologyProposal and evaluate synthetic route candidates without executing a worker/model/provider/process. This tests core IssueOps planning earlier without stealing S6 runtime/authority ownership.

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

S7 remains distinct from S8 because independent evaluation must not be owned by the same repair/completion boundary that consumes findings. Implementations may create a tight feedback loop, but `ReviewOutcome != CompletionDecision` remains structural.

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

Do not attempt a monolithic “autonomous GitHub engineer” implementation. Deliver vertical, authority-safe tracer bullets.

### TB0 — first IssueOps end-to-end proof (offline/read-only)

**User-visible value:** given a synthetic/local issue artifact plus a local repository fixture, WePLD creates a Case and returns an inspectable triage/frontier with cited relevant project evidence.

```text
InputArtifact(issue fixture)
-> Case
-> local repository/project identity
-> exact/lexical/Fehrest-available retrieval
-> triage classification
-> reproduction-readiness assessment
-> probable relation candidates if any
-> DecisionBoundary only if a real non-inferable choice remains
-> evidence-backed Case room summary
```

Required architecture: S3 `InputArtifact`, S4 local retrieval/Fehrest minimum, `Case`/relation semantics, local evidence storage, workflow intent. No Agent Host is required.

Effects: bounded local reads/persistence only under owning authority. No network, Git write, provider write, model/provider execution, package install, merge, or issue close.

Security boundary: untrusted issue/repository text remains data; adversarial fixture text cannot create effects or broaden file visibility.

Required negative oracles:

```text
MALICIOUS_ISSUE_CANNOT_CREATE_EFFECT
SIMILAR_ISSUES_WITH_DIFFERENT_CAUSES_NOT_EXACT_DUPLICATES
MISSING_EVIDENCE_RETURNS_ABSTENTION
STALE_LOCAL_SOURCE_IS_SURFACED
NO_NETWORK_OR_PROVIDER_EGRESS
```

Completion evidence: exact fixture/repository generation, Case identity, retrieval citations, triage evidence, negative-oracle results, and explicit out-of-scope statement.

### TB1 — live GitHub read-only Case import

After source/network/auth qualification: import one GitHub issue/PR into the same Case/triage pipeline, preserve raw observations/freshness, and perform **no provider writes**.

### TB2 — one bounded worker prepare loop

Add one qualified worker to produce a proposed local change + tests from one Case. No provider write/merge. This is where S5 delegation dry-run becomes S6 real routing.

### TB3 — independent review + repair without landing

Run deterministic checks, independent review, finding reconciliation, and bounded repair while merge/close remain denied.

### TB4 — one controlled landing

Only after lower ceilings are proven: exact-target PR/provider effects, expected-head guarded merge, provider closeout, then Trusted Completion review.

### TB5 — recommendation-only backlog sweep

Run the qualified sweep algorithms over multiple Cases with provider writes disabled. Bulk mutation is a later separately qualified capability.

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
- duplicate/root-cause clustering precision, recall, abstention, and evidence coverage;
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
