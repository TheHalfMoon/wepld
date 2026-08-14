- It is not “an external development tool becomes product authority.”
- It is not permission to ship every long-term capability in Alpha.

### 4.3 WePLD Development Method Contract

This contract governs any future slice only after that slice receives explicit founder authorization.

**Spec Kit — required external planning workflow.** Use, as appropriate:

```text
constitution → specify → clarify → plan → checklist → analyze → tasks → implement
```

Each artifact has source, digest, scope, supersession, and mapping to WePLD-owned decisions/acceptance obligations. `Spec Kit artifact != WePLD canonical authority`. Product-native mechanics arrive in S5; external use starts now.

**Ponytail — always on, `PONYTAIL_MODE = FULL`.** Every proposal asks:

- Does this need to exist?
- Is it already solved in WePLD?
- Can stdlib, the native platform, an already-admitted dependency, or a qualified reusable component solve it?
- Can a smaller architecture solve it?
- Why this abstraction, dependency, process, privilege, worker, or service?

Ponytail preserves security, validation, correctness, recovery, evidence, accessibility, and authority boundaries. For worker topology, one qualified worker is preferred unless an additional worker has positive marginal accepted-outcome value after coordination cost, latency, duplicated context, independence need, and synthesis overhead.

**Cubic — required independent build reviewer when egress permits.** For code-changing slices:

```text
builder
→ deterministic checks
→ Cubic local/preflight review
→ validate/fix findings
→ deterministic checks
→ Cubic re-review
→ push/open PR (only when separately authorized)
→ Cubic PR review
→ repair
→ Cubic re-review
→ additional independent/adversarial review when risk requires
→ ChatGPT architecture/evidence reconciliation
→ founder acceptance
```

If policy denies source/code egress:

```text
CUBIC_STATUS = NOT_RUN_DATA_EGRESS_DENIED
```

That state is never converted to PASS. If egress would otherwise be permitted but Cubic is unavailable, record `CUBIC_STATUS = NOT_RUN_UNAVAILABLE`; unavailability never becomes success. `Cubic clean != CompletionDecision`; `Cubic approval != founder acceptance`; `Cubic finding != write authority`; `Cubic unavailable != PASS`.

**Development-tool provenance qualification.** Before the first code-changing slice, and whenever a tool or materially relevant configuration changes, the development packet records supply-chain evidence for the external build method:

- **Spec Kit:** exact release/tag/commit where applicable; workflow/template version or digest; configuration; source/provenance.
- **Ponytail:** exact release/version/commit where applicable; ruleset/skill/configuration digest; `PONYTAIL_MODE = FULL`; source/provenance.
- **Cubic:** CLI/client version; review configuration/profile; observable service/policy snapshot where applicable; data-egress classification; retention/disclosure qualification; exact target/revision reviewed.

This evidence qualifies the development method; it grants none of these tools canonical WePLD authority. Any exceptional acceptance without the normally required Cubic review requires an explicit waiver by the same authorized acceptance authority that may decide G9, an independently qualified substitute review route, and a recorded residual limitation. A waiver is not a PASS for the missing Cubic route.

---

## 5. Reconciled Vocabulary and Domain Model

### 5.1 Canonical hierarchy

```text
Tenant / Organization
  └─ Team
      └─ Project
          ├─ Workspace
          └─ Work
              └─ Mission
                  └─ Task
                      └─ Attempt
```

The hierarchy is the working canonical model from V1.5; final aggregate ownership remains founder decision 4. Distinctions remain strict: Team is governance; Work is durable coordination; Mission is executable outcome; Task is execution unit; Attempt is one execution instance. Chat, room, canvas, branch, worktree, sandbox, VM, process, session, provider, model, worker, and harness do not become hidden canonical identity.

### 5.2 Change and review identities

`DIRECT_V1_5_EVIDENCE`: V1.5 §42.3 establishes `ChangeUnit`, `ChangeStack`, `ChangeDependency`, `ChangeStackRevision`, `RestackDecision`, `ChangeConflict`, `StackAssuranceResult`, `StackDeliveryDecision`, and `SpeculativeCheckReuseEvidence`. Exact fields, revisions, and transitions are P0 technical contract work; existence is no longer a founder question.

Review producer execution is named `ReviewProducerRun` by default. `ReviewPassRecord` may be retained only if compatibility evidence requires it and its schema mechanically states that it is not a verdict.

### 5.3 Consistency and persistence classes

| Class | Semantics |
|---|---|
| Authority, policy, approvals, grants, budgets, completion | Strong/causal, versioned, explicit lifecycle |
| Owned aggregates | Optimistic concurrency with revision checks where safe |
| Facts, receipts, findings, decisions, evidence | Append/idempotent, immutable identity/digest |
| `ReviewCoverage` | Immutable append-only execution evidence bound to `ReviewPlan` and producer runs |
| Search, graphs, dashboards, `ReviewSynthesis`, `ReviewTour`, forge comments | Rebuildable projections/content-addressed artifacts |
| Presence | Lease-derived/best effort |

Coverage cannot be regenerated later to make an incomplete old review appear complete. Projection schemas are not prematurely frozen as canonical domain truth.

---

## 6. Canonical Subsystem Ownership Matrix
