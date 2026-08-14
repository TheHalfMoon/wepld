→ Mission Runtime records Attempt, effects, artifacts, lineage, cost, and uncertainty
→ Assurance evaluates criteria and persists evidence, coverage, findings, and ReviewOutcome
→ AGILLE determines lifecycle admissibility
→ Nawat revalidates apply/accept/release/publish authority
→ authorized CompletionDecision + append-only receipt
→ Work projection
```

The following never constitute completion by themselves: process exit, no exception, final message, task `DONE`, model self-score, clean Cubic review, no findings, green CI, merge, deploy, publish, `ReviewOutcome`, or verifier observation.

Valid outcomes include Accepted, Accepted with disclosed residual risk, Rejected, Blocked, Cancelled, NonConverged, and RecoveryRequired. Retry exhaustion cannot fabricate acceptance; it yields incomplete/failed/manual-review state according to policy.

Trusted Completion consumes exact target and policy revisions, acceptance criteria, immutable coverage, admitted findings and dispositions, deterministic and runtime evidence, effect receipts, route/independence lineage, repair/re-review evidence, cost/budget state, uncertainty, approvals, and residual risks. It does not trust a summary projection where underlying evidence is absent.

---

## 14. Adaptive Assurance Profiles

One AGILLE risk/rigor decision derives the AssuranceProfile; a lower label cannot be chosen merely to escape controls.

| Profile | Indicative requirements | Human/authority rule |
|---|---|---|
| LOW | Required deterministic checks; one qualified independent high-precision review where applicable; explicit coverage | Human acceptance remains required for canonical completion in Alpha |
| MEDIUM | Deterministic checks; correctness review; targeted architecture/context evaluation | Material findings/ambiguities resolved or disclosed |
| HIGH | Correctness, security, architecture, cross-boundary review; stronger independence; targeted runtime verification | Mandatory authorized judgment on residual risk |
| CRITICAL | Multiple effectively independent routes where justified; property/fuzz/model-checking/formal checks where tractable; runtime evidence; hardened provenance | Explicit authorized human/founder gate according to policy |

Admission criteria use change surface, affected authority/data/secrets, cross-repository and runtime blast radius, migration/irreversibility, dependency/supply-chain change, concurrency, provenance, novelty, rollback quality, and policy. Each profile states exact tools, required relationships, evidence, floors, budgets, and allowed exceptions.

Escalation occurs when evidence shows greater risk, missing context, disagreement, suspicious output, failed controls, or runtime divergence. De-escalation requires an authorized versioned rationale and cannot erase already observed risk. Ponytail controls reviewer count but never removes a safety-required independent relationship.

---

## 15. ReviewContextCapsule and Intent-Aware Review

The review begins from governed intent, not merely a diff or external ticket. A minimal capsule can include:

- Work/Mission objective and authorized scope;
- AGILLE specification, acceptance criteria, constraints, and non-goals;
- relevant ADRs, architecture ownership, and trust boundaries;
- changed symbols, inbound/outbound references, dependency/call graph, and cross-repository contracts;
- tests, invariants, schemas/APIs, prior findings, incidents, and runtime observations;
- exact base/head/stack/environment/toolchain/policy revisions;
- source provenance, freshness, disclosure class, omissions, and Memory Completeness gaps.

External Jira/Linear/etc. text remains untrusted evidence and possible prompt-injection/sensitive-data input. Canonical acceptance obligations must be represented in WePLD-owned contracts.

### 15.1 Mandatory context ablations

| Condition | Contents | Question |
|---|---|---|
| C0 | None beyond target/diff mechanics | Raw context floor |
| C1 | Minimal intent and acceptance criteria | Value of explicit outcome truth |
| C2 | Targeted local repository context | Value of local structure/history |
| C3 | Targeted cross-repository context | Value and disclosure cost of cross-repo reach |
| C4 | Relevant history/runtime evidence | Value of incidents, prior outcomes, traces, and temporal truth |
| C5 | Deliberately overstuffed context | Signal dilution, cost, latency, leakage, and failure threshold |

For each condition record target/task/model/harness/seed policy; capsule digest; source classes; freshness; retrieval misses; tokens; latency; monetary cost; disclosure risk; finding quality; false-success; architecture/security detection; acceptance coverage; and human burden. More context is never assumed better.

Missing acceptance criteria, stale/superseded ADRs, unavailable cross-repository dependencies, or incomplete capsule coverage remain explicit states. Reviewers may request bounded expansion; the request and resulting delta are recorded.

---

## 16. ChangeUnit, ChangeStack, and Delivery Evidence

V1.5 directly establishes the ChangeStack family in §42.3. This closes the former lineage/evidence uncertainty: `ChangeUnit`, `ChangeStack`, `ChangeDependency`, `ChangeStackRevision`, `RestackDecision`, `ChangeConflict`, `StackAssuranceResult`, `StackDeliveryDecision`, and `SpeculativeCheckReuseEvidence` are canonical future-domain concepts. Stage 3 does not reopen that decision.

The Alpha scope remains deliberately smaller than the eventual product surface:

- S9 proves one `ChangeUnit` and its delivery/quality evidence on a governed path.
- The full stacked-change authoring, restacking, dependency visualization, bottom-up review, and delivery UX remains Post-Alpha.
- A Git branch, pull request, Graphite stack, or tool-native object is an external representation, not canonical ChangeStack truth.
- ChangeStack must not duplicate Work, Mission, Attempt, ReviewTarget, or repository truth. It references their immutable identities.

### 16.1 Check-reuse invariant

Speculative reuse is permitted only when a recorded digest proves equality of every input that can affect the result: exact content/revision, base ancestry and stack dependencies, tool and configuration, environment, policy and acceptance criteria, relevant ContextCapsule, capability/network state, and declared nondeterminism. Any unknown or changed dimension invalidates reuse. A restack or conflict resolution creates a new evaluation identity even when the visible diff appears unchanged.

`StackAssuranceResult` is evidence about a stack revision. `StackDeliveryDecision` is a separately authorized delivery decision. Neither is a `CompletionDecision`.

---

## 17. Bounded Runtime Verifier

The Runtime Verifier is an evidence producer outside the physical Trusted Core. It may execute a controlled test, inspect a WePLD-owned runtime surface, or reproduce an otherwise unresolvable behavioral claim. It emits falsifiable `VerificationObservation` records, never an accept/reject/completion verdict and never ambient repair authority.

Each run records:

- immutable ReviewTarget, requested property, reason static evidence was insufficient, and authorizing policy;
- environment image/configuration digest, OS/runtime/toolchain, identity, capability leases, network policy, secret identities, and exact tested endpoints;
- replayable actions, inputs, timestamps, logs, screenshots/traces where relevant, artifacts and hashes, resource use, timeout/cancellation state, and cleanup result;
- observed behavior, tested and untested scope, uncertainty, limitations, and any divergence from the plan.

Wrong endpoint, stale target, unavailable environment, denied capability, timeout, malformed output, incomplete cleanup, or missing evidence yields `INCOMPLETE`, `BLOCKED`, or failure—never a pass.

The founder must still decide the Alpha scope. The recommended boundary is WePLD-owned desktop/core/terminal/project/review surfaces only, under explicit profiles. General browser/computer-use verification, arbitrary third-party systems, broad production access, and open-ended autonomous exploration remain Post-Alpha.

---

