The following compact set should be written only after the relevant founder decision and evidence exist:

| ID | Record | Scope |
|---|---|---|
| `ADR-P0-01` | Canonical vocabulary, aggregate ownership and Maemar placement | §5–§10 and founder decisions 1/4; includes logical-vs-deployable boundary |
| `ADR-P0-02` | Physical Trusted Core, authority/evidence/effect/completion chokepoints | Minimal TCB, untrusted producer/worker placement, fail-closed completion |
| `ADR-P0-03` | Assurance semantic contract and lifecycle boundary | Producer runs, immutable coverage/evidence, findings/conflicts, projections and `ReviewOutcome != CompletionDecision` |
| `ADR-P0-04` | Role-relative independence and context disclosure | §10 graph, evidence-source diversity, information-set/cache/memory and Nawat egress controls |
| `ADR-P0-05` | Windows execution profiles and qualification | §21 properties, atomic launch, fail-closed network and no-untrusted-worker fallback |
| `ADR-P0-06` | Bounded Runtime Verifier | Evidence-without-verdict, Alpha target/environment boundary, failure/replay semantics |
| `ADR-P0-07` | Benchmark/corpus decision protocol | D0/A/B/C/D, `M-01..M-20`, `CTX-C0..CTX-C5`, `CORPUS-C0..CORPUS-C4`, floors/budgets/statistics/Pareto and Cubic comparison |
| `ADR-P0-08` | Component acquisition and build-method controls | Per-component admission/exit, Spec Kit, Ponytail FULL, Cubic egress/non-authority and deprecation evidence |

Governance decisions are separate records, not ADRs:

| ID | Governance record |
|---|---|
| `GDR-P0-01` | Repository visibility, proprietary/IP/access and publication posture |
| `GDR-P0-02` | PR #11 replacement/supersession/cross-link/closure disposition |
| `GDR-P0-03` | PR #1 donor ledger/archive/supersession/cross-link/closure disposition |
| `GDR-P0-04` | ADR/history namespace and supersession manifest |
| `GDR-P0-05` | Corrected ten-slice roadmap, non-primary S3-D and authorization boundaries |

Each record states context, evidence, options, decision authority, decision, consequences, dissent/uncertainty, superseded records, migration/recovery, review date and falsifiers. Merely copying this report is not a decision record.

---

## 34. Repository, History, Migration, and Branch Strategy

### 34.1 Authority and preservation

The live `main` branch remains the source of current repository truth at SHA `993b2fb55af038091f365ad29d0740bdb1bd6c9e`. V1.5 and this report are planning artifacts outside the repository; neither silently mutates or replaces repository content. In a future authorized governance task, ratified successor artifacts must enter through the decided privacy/IP posture and ordinary protected review—not by rewriting history.

Historical documents/ADRs remain immutable evidence with explicit generation, source ref/blob, effective/superseded status and successor link. The recommended namespace is:

```text
docs/adr/current/<approved-id>.md
docs/adr/history/<generation>/<original-id>.md
docs/adr/history/MANIFEST.md
```

This is a recommendation subject to founder decision 8. It is not permission to move a file. IDs never imply chronological/canonical authority without the manifest.

### 34.2 PR and branch disposition

| Object | Live state | Future authorized disposition |
|---|---|---|
| `main` | Current public default branch at exact SHA above | Preserve history; no force-push or silent canonical substitution; successor enters after B-GOV-001 and governance approval |
| PR #11 / `docs/s0-b-product-architecture-foundation` | Open draft, unmerged, clean/mergeable; head `68cab399748c5c103b8f96380da69fdffca4d3fe` | Do not merge unchanged. Land/ratify replacement first, map every useful item to successor/rejection, preserve immutable ref/cross-links, then close superseded after founder approval |
| PR #1 / `feat/build-feature-engineering-memory` | Open draft, unmerged, dirty/non-mergeable; head `d5ef318468b6c35df3c14c1c5f72beb1191baf29` | Never wholesale merge. Complete path/concept donor ledger, preserve archival immutable ref if needed, cross-link destinations/rejections, then close superseded after founder approval |
| Other historical refs | Not dispositioned by this bounded Stage-3 task | Preserve until a separately authorized complete ref/citation audit; do not delete from partial evidence |

No branch, tag, PR, comment, review, commit, ruleset, visibility or repository setting is changed by this report.

### 34.3 Product/schema migration doctrine

- append versioned records; do not rewrite accepted evidence/history;
- distinguish reversible projections from authority-bearing records before migration;
- preflight compatibility, backup/checkpoint and rollback/recovery; crash-test partial migration;
- preserve source/provenance/decision/effect identities across replacements;
- make downgrade support explicit; never silently parse a newer envelope as older;
- external effects are reconciled/compensated separately from local source/state rollback;
- component replacement retains admission/version and evidence lineage and exercises the exit plan.

---

## 35. Alpha Non-Goals and Scope Guardrails

Unless separately founder-authorized with evidence, Alpha excludes:

- full ChangeStack authoring/restack/dependency/delivery UX beyond one S9 ChangeUnit evidence path;
- generalized Runtime Verifier, arbitrary production systems, broad browser/computer control and remote phone-initiated host effects;
- autonomous swarms, general dynamic Edara optimization, open-ended worker creation and cross-machine fleet orchestration;
- enterprise multi-tenant/team collaboration, SSO/admin controls, organization-wide knowledge and cross-tenant learning;
- broad nonsoftware object models and generalized workflow automation;
- self-training, feedback-to-policy auto-write, Byan operational authority and benchmark corpus as memory;
- unattended merge/release/publish/purchase/message, scheduled confirmation bypass, or credential-possession authority;
- hosted control plane or mandatory cloud index/reviewer as canonical truth;
- universal language/tool/provider/platform support or a containment claim broader than tested profiles;
- installer, auto-update, broad telemetry or public code publication before their specific governance/security gates;
- formal verification for every risk tier; CRITICAL formal/property controls remain evidence-gated and targeted;
- source acquisition by repository badge, wholesale harness adoption or dependency installation from this planning record.

These guardrails preserve a founder-usable vertical slice while keeping interfaces extensible and evidence honest.

---

## 36. Post-Alpha and Evidence-Gated Expansion

Post-Alpha candidates include full ChangeStack UX and multi-unit delivery; generalized/runtime-domain verifier profiles; broad browser/computer-use and external-system effects; enterprise collaboration/tenant administration; cross-project/organization Fehrest; nonsoftware Work objects; adaptive Edara/workforce optimization; richer ReviewTour and design/accessibility surfaces; formal CRITICAL profiles; remote execution; and cross-project Byan analytics.

Each candidate requires a new founder authorization, Ponytail FULL sufficiency record, component/rights/security evidence, threat/data/authority model, benchmark/operational evidence, migration/recovery/exit design, and explicit effect/acceptance ownership. “Deferred” means not authorized, not forgotten.

Cubic remains part of the development workflow until a pre-registered, independently reviewed comparison shows WePLD-native alone is non-inferior or superior for accepted safety/quality floors across relevant strata, stays within cost/latency/disclosure budgets, and retains adequate independent challenge. Deprecation is a founder/governance decision with an exit/fallback record; it is never inferred from reaching S7.

---

## 37. Founder / Governance Ratification Register

No former 24-question register is restored. The ten Stage-3 decision IDs remain immutable traceability records; they are not all current-answer questions. Spec Kit + Ponytail + Cubic is current direction, not an eleventh decision.
