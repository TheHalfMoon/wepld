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
