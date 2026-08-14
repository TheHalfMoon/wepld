
| Subsystem/domain | Owns | Must not own |
|---|---|---|
| Work | Durable human/team coordination and links | Execution, tool effects, completion authority |
| AGILLE | Rigor, specification/planning gates, acceptance obligations, admissibility | Runtime state or effect authorization |
| Mission Runtime | Mission/Plan/Task/Attempt/Lease, checkpoints, retries, waits, cancellation, effect orchestration, recovery | Membership, policy authorship, canonical knowledge |
| Mirefa | Qualification/catalog/route evidence for models, workers, providers, tools, skills, substrates, components | Authority |
| Edara | Staffing/delegation/topology decision structure and minimum-sufficient team | Grants, runtime truth, acceptance, a separate service in Alpha |
| Nawat | Principal identity, authority, capability grants, revocation, effect-time authorization | Staffing, security scanning, review verdicts |
| AMAN | Security/risk signals, scanner normalization, threats and defensive observations | Effect authorization |
| Fehrest | Project Brain, provenance, branch/temporal truth, context compilation, knowledge admission | Permission or effect authority |
| Byan | Derived metrics, benchmarks, analytical views, outcome learning candidates | Operational/canonical authority |
| Assurance | Logical evaluation ownership, findings, evidence adjudication, coverage, review outcomes | CompletionDecision, mutation authority by finding |
| Trusted Completion | Authorized decision about what counts as complete after evidence/admissibility/authority checks | Reviewer self-certification |

### 6.1 Minimal Assurance TCB

Logical ownership does not imply physical trust placement.

**Inside the Rust Trusted Core only where necessary to enforce truth/authority:**

- contract and schema validation;
- immutable `ReviewTarget` identity validation;
- `AssuranceProfile` and `ReviewPlan` policy validation;
- evidence/digest verification;
- finding admission and state-transition validation;
- immutable `ReviewCoverage` persistence;
- `ReviewOutcome` persistence;
- authority separation, including `ReviewOutcome != CompletionDecision`.

**Outside the TCB:**

- deterministic scanners, linters, compilers, and test tools;
- AI reviewers and their model/provider harnesses;
- runtime-verifier workloads;
- format-specific adapters where practical;
- finding generation and synthesis workers;
- `ReviewTour`, dashboards, and forge comments.

Untrusted producer output enters the Core only through bounded, versioned, hostile-input validation. The TCB may reject or admit evidence; it does not need to contain every producer.

---

## 7. Cross-Subsystem Invariants

1. **Human final authority:** protected acceptance/release remains authorized-human controlled.
2. **UI zero authority:** UI, chat, dashboard, forge, Spec Kit, and Cubic surfaces are projections/inputs, not policy boundaries.
3. **No ambient authority:** every effect uses typed scope, purpose, budget, expiry, revocation, and receipt.
4. **Builder cannot self-certify:** acceptance-critical completion requires independent evidence and authority.
5. **Review is not completion:** `ReviewProducerRun`, finding, coverage, synthesis, tour, verification observation, and `ReviewOutcome` are not `CompletionDecision`.
6. **Finding does not grant mutation:** repair is a separate Attempt and grant.
7. **Coverage is evidence:** no-findings without explicit coverage is incomplete, never clean.
8. **No fail-open evaluation:** unavailable/malformed/timeout/context/tool/evaluator states become incomplete, blocked, failed, or nonconverged.
9. **Worktrees are not containment:** source-control collision isolation is distinct from host security.
10. **Local is topology, not proof:** local data/processes still require identity, ACL, token, secret, process, network, and recovery controls.
11. **Minimum sufficient topology:** every additional worker must justify positive marginal accepted-outcome value.
12. **Unknown is not independence:** an unknown relationship cannot satisfy a required independence relation.
13. **No silent route changes:** model/provider/helper/harness/context/tool/permission changes remain explicit lineage.
14. **Canonical knowledge is not a derived index:** vector, graph, search, and analytics stores remain rebuildable/advisory.
15. **Acquisition is component-specific:** inspection, popularity, public visibility, or root license label is not import admission.
16. **External build tools remain non-authoritative:** Spec Kit, Ponytail implementation helpers, and Cubic do not write canonical truth.
17. **S3-D cannot fork Assurance:** it emits through P0-frozen minimal envelopes and creates no second finding or authority system.
18. **Accessibility and Arabic/RTL are architectural:** never minimized as polish.
19. **Self-improving, never self-authorizing:** feedback produces candidates, never direct policy/rule/routing mutation.
20. **One object, one identity, one truth, many authorized projections.**

---

## 8. Maemar Reconciliation Recommendation

`DIRECT_V1_5_EVIDENCE`: V1.5 §6.10 deliberately preserves Maemar as the architecture-intelligence domain and requires founder reconciliation. Its mandatory capabilities include declared, implemented, build, runtime, deployment, supply-chain, and target architecture; semantic structure; APIs/events/databases/schemas; ownership/trust boundaries; impact; decisions; and drift.

Three durable arrangements remain possible:

1. Maemar as a top-level logical bounded context.
2. Maemar as a named capability domain inside Fehrest/Project Brain.
3. A split in which Fehrest owns architectural facts/provenance, AGILLE owns admissibility/constraints, and Byan owns derived architecture analytics, with Maemar retained as the named cross-domain interface.

**V2 recommendation:** option 2, with an explicit Maemar Capability Register and stable interfaces to AGILLE and Byan. This avoids a new deployable service and duplicate truth while preserving the name, ownership visibility, and capability family. The founder must decide; V2 does not answer decision 1 on the founder's behalf.

Regardless of the choice:

- architecture facts retain provenance, revision, validity interval, and authority class;
- derived graphs/reports are not canonical truth;
- architecture drift is evidence, not automatic policy;
- Maemar does not authorize effects or accept completion;
- deployment separation requires later evidence, not naming alone.

---

## 9. Work / AGILLE / Mission Runtime Reconciliation

### 9.1 Boundary questions

```text
Work             What durable outcome/coordination record exists for people and teams?
AGILLE           What engineering method, rigor, obligations, and admissibility apply?
Mission Runtime  What execution state and effects are durably true, and how do they recover?
```
