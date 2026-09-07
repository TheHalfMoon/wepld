# Adversarial repair disposition — 2026-09-06

```text
STATUS = AUTHOR_REPAIR_RECORD_PENDING_INDEPENDENT_REVIEW
INPUT_HEAD = ee991b680e00a82365f88975e57743f85aed7c94
CANONICAL_MAIN_RECONCILED = 6871229271bf3cebcfee9caff960a50f5a8c610d
IMPLEMENTATION_AUTHORITY = NONE
INDEPENDENT_ACCEPTANCE = NOT_ESTABLISHED
```

The [pre-change report](adversarial-pre-change-review-2026-09-06.md) was delivered before these contract edits. The [source recheck](../research/adversarial-mechanism-recheck-2026-09-06.md) separates code observations, documentation, inference and recommendations. Exact post-commit head/check/reviewer state belongs in the live PR evidence record, avoiding a self-referential commit identity in this file.

## Repairs submitted for review

| Concern / prior thread location | Disposition and owning artifact |
|---|---|
| EffectProposal intent/bindings and retry safety (`data-model.md`, original lines 478/512) | Required executable intent/Mission/Assignment/Attempt/principal/route/credential/risk/envelope bindings; stable operation versus dispatch identity; closed retry states; durable dispatch and unknown-outcome reconciliation. |
| ContextPackage manifest and project/workspace visibility (original lines 298/304) | Existing untrusted-content contract delegates its schema to data-model; explicit project/workspace intersection added at construction and consumption. |
| Retrieval projection identity (original line 248) | Direct-source versus derived-projection discriminator with conditional mandatory generation and exact-source evidence. |
| WorkerRequirement (`plan.md`, original line 551) | Existing canonical definition in data-model section 12 remains controlling; no duplicate type introduced. |
| EngineRun authority and policy precedence (assurance-fabric original lines 236/746) | Authority mandatory for effectful runs; explicit highest-to-lowest ordering plus field specialization and separate controlling-authority path. |
| Credential transport (retrieval original line 235; historical Omnigent research line 184) | Validated HTTPS required before authenticated HTTP traffic, redirect revalidation before credential forwarding; current runtime/retrieval contracts govern. |
| Historical Omnigent optional credential scopes (original line 200) | Historical research schema remains an earlier sketch. The current runtime contract requires deny-default account/target/resource/method/attempt/operation/use limits and activation evidence; omitted fields in old research confer no rights. |
| Review independence (original lines 75/126) | Distinct reviewer worker/Attempt and no repair self-certification are mandatory; exception removed. |
| RuntimeReservation (original line 407) | Envelope reference required for resource-bound routes, with exact Attempt/Host/Runner and start-validity checks. |
| Browser binding (runtime spec original line 78) | Session/target/frame/origin/navigation/document/snapshot/element bindings made explicit; WebToolIdentity becomes existing observation projection. |
| DownloadObservation (web boundary original line 163) and quarantine task | Typed existing Observation payload, inert bounded staging, mandatory quarantine/classification and separately authorized release. |
| Parent acceptance live state/reviewer unavailability (original lines 165/182) | Live base/head/tree/check/review record required; unavailable/incomplete reviewer means REVIEW_BLOCKED. |
| Historical September 2 count and September 4 CURRENT_* labels | Preserved original files. Explicit accounting correction: 7 high + 8 medium + 1 low = 16. All old CURRENT_* values are historical reviewed anchors, not live acceptance evidence. |
| Product acceptance section J and plan/task PCT-P006 | All criteria need evidence or justified N/A; whole final package review scope declared; incremental/stale/author review excluded as acceptance. |

Newly identified gaps also repaired: enforcing fence consumers and refusal on unfenced takeover; host input serialization and residual GUI races; durable connection versus ephemeral capability with non-circular activation; atomic trigger capture/intent association, scoped dedupe and misfire/backlog semantics; WorkSession/Mission cardinality; existing Case Bus support for generic Work events; orthogonal browser ownership/location; minimum recovery safety before consequential S8 actuation.

These are author dispositions for verification, not unilateral resolution of GitHub review threads. A fresh reviewer must test the reasoning and detect cross-contract conflicts. None of the future implementation task boxes is completed by this drafting pass.

## Deliberately unresolved outside this patch

- Current Doctor's concurrent descriptor-read budget flaw is recorded in sealed partial security scan `d0e0fe07-d7b9-4343-8f93-9b552521e945` at `5d60fd32aaa272d89d7bbc42607909b402f4c825`, finding `csf_1be42b0fd47f31ef266a5451` (low severity, high static confidence). No runtime repair or exploit was performed; the fixed source is unchanged by the main deltas reviewed here.
- The full inherited policy chain, donor implementations, live branch protection, provider account settings and new v53 security delta are not covered by that partial source scan. It is not independent security acceptance of this patch.
- Canonical checkpoint drift and policy-chain maintainability need separate governance work. S2 acceptance/authority-edge questions are not decided by Spec 006.
- Source/dependency rights, install hooks, full operator implementations and benchmark runs remain future qualification; no import is recommended or admitted.
- Entire-package independent review and acceptance-criteria evidence disposition remain open. The PR must remain a draft until the applicable gates are satisfied.

## Validation boundary

Local structural checks cover Markdown UTF-8, fenced blocks, relative links, Spec 006-only path scope and credential token patterns. They do not prove architecture correctness or absence of every secret/private datum. The first trusted-base policy selftest attempt failed because Windows CRLF checkout bytes differed from frozen Git blobs; isolated checkout bytes were restored from Git without changing policy source, then qualification was rerun. Actual results and exact candidate identities are recorded in the PR preflight/check evidence, not inferred here.

## Completion repair — 2026-09-07, awaiting independent qualification

This section records author dispositions for CodeRabbit review 5125933000 on head 0e85b2f42e6aa38ee0d8ba3fa9fdb55107e207df. It does not resolve threads or claim the next candidate is reviewed. The prior source and review anchors above remain historical.

| Review concern | Repair and exact owner |
|---|---|
| Policy-sensitive assurance cache | assurance-fabric-plan §17 and AF contract §27 bind immutable PolicySnapshot, required claims/evidence and invalidation/reassessment. |
| RETRY_FAIL/TIMEOUT/CANCELLED false clean | AF-FR006, AF contract §§8/13/27, AF-S7-T003/T006 preserve every non-FIRST_PASS outcome. |
| Optional reservation | DM RouteQualification requires typed reservation determination/evidence; RF ExecutionEnvelope has closed Reserved/QualifiedNoReservation variants and exact live matching. |
| Web context and complete effect binding | WB WebToolObservation and InvocationProposal require browser_context_id; proposal requires canonical effect_proposal_ref and matching complete inputs/authority prerequisites. |
| Retrieval optional generation/location | DM RetrievalEvidence has closed DirectSource/DerivedProjection variants with mandatory content/location identities; RR delegates to those rules. |
| Nawat enum/grant mismatch | DM NawatDecision owns seven outcomes and ALLOW-only grant_id; WB consumes that exact record. |
| OM credential/recovery task gaps | OM tasks and professional hardening explicitly consume complete RF credential/HTTPS and RD enrollment/fence/event/capacity/version contracts. |
| Weak task/acceptance review and egress gates | OM/HARD/PCT tasks and product acceptance J require live exact scope, qualified independent whole-scope review and canonical screening/handling/authorization before sharing; unavailable/incomplete is REVIEW_BLOCKED. |
| Research authenticated transport ambiguity | Omnigent research recommendation now specifies authenticated HTTPS on every credential-bearing hop, including redirects. |
| S9 privacy task omission | RT-S6-PRIV001 makes privacy a prerequisite before capture; RT-S9-PRIV001 covers replay/export/restore negative fixtures. |
| WEB-S8-001 skips qualification | Explicit complete proposal and browser/profile/context/origin/document/tool identity -> Mirefa WebRouteQualification -> Nawat -> dispatch revalidation. |
| Historical OpenHands storage reference nit | Existing S2 generation/store ownership remains controlling; OH runtime lineage now references canonical RuntimeEventEnvelope. Historical sketches are not standalone contracts or new stores. |

Additional completion repairs define Project context/import projection, revision-checked Work controls, immutable automation templates/conditions/DST and revision-independent occurrence dedupe, complete connection lifecycle/SDK, Browser operation matrix and Computer identity/actuation constraints. Eight feature families now have a common ownership/evidence/task matrix, all 38 requested failure cases and 14 UX states. Supporting requirements/tasks/acceptance are mapped in analyze.md. Real source inspection receipts and limitations are integrated into the existing mechanism research file.

The feature matrix remains PARTIAL pending final coherence assessment and qualified whole-package review. All applicable acceptance checkboxes require concrete disposition before merge; no future runtime tasks were marked done. No runtime, canonical governance, workflow, dependency or source-registry edit belongs to this planning delta. Main's later S2 test/policy commits are incorporated only by non-destructive merge and trusted-base checks.

Build-learning candidate: optional schema fields plus mandatory prose permit incompatible implementations; use closed variants and one canonical vocabulary. Dedupe identity must survive definition edits; execution revision belongs in the first accepted record. Safety prerequisites cannot be deferred merely because durable-history tasks live in S9. These are local planning lessons, not edits to frozen canonical learning or authority.
