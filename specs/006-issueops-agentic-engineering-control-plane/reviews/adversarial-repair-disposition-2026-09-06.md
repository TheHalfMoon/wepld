# Adversarial repair disposition — 2026-09-06

```text
STATUS = AUTHOR_REPAIR_RECORD_PENDING_INDEPENDENT_REVIEW
INPUT_HEAD = ee991b680e00a82365f88975e57743f85aed7c94
CANONICAL_MAIN_RECONCILED = 6871229271bf3cebcfee9caff960a50f5a8c610d
IMPLEMENTATION_AUTHORITY = NONE
INDEPENDENT_ACCEPTANCE = NOT_ESTABLISHED
```

The [pre-change report](adversarial-pre-change-review-2026-09-06.md) was delivered before these contract edits. The [source recheck](../research/adversarial-mechanism-recheck-2026-09-06.md) separates code observations, documentation, inference and recommendations. Exact post-commit head/check/reviewer state belongs in the live PR evidence record, avoiding a self-referential commit identity in this file.

## Owner-level reconciliation — 2026-09-07

Rechecking the nine remaining review threads against the actual owners found that several earlier dispositions overstated closure: a canonical name or general reference did not always supply the requested field mapping or enforcement rule. The later repairs below supersede those closure descriptions. They remain author evidence pending independent verification.

| Review comment | Exact owner repair / verification required |
|---|---|
| 3896901494 | DM §11 and UC Context package manifest now share `*_by_item` and `created_at`; the manifest owner is singular. |
| 3896901502 | WD Nawat decision contract now explicitly resolves and matches the typed origin to the complete proposal before granting; syntactically present references cannot suffice. |
| 3896901508 | DM §12 explicitly defines the transient Assignment/topology capability mapping; plan S5 and clarify both reference it. |
| 3929875333 | RI Exact-target freshness now requires completed qualified whole-final-scope review and records missing/partial/unavailable coverage as REVIEW_BLOCKED. |
| 3929875341 | WB owner list and Download section define one typed Observation payload with exact context, bounded staging, sealed artifact identity, media/classification/quarantine and handling-policy invariants; DM §6 references this owner. |
| 3929875380 | Historical Omnigent OM-06 now locally distinguishes upstream HTTP(S) observation from mandatory WePLD HTTPS credential hops and superseded optional-field sketches. |
| 3929875393 | September 2 review now contains its own linked dated accounting correction, preserving original findings/footer: 7 HIGH + 8 MEDIUM + 1 LOW = 16. |
| 3929875407 | September 4 review now locally identifies every CURRENT_* field as its historical reviewed frontier and points to live acceptance procedure. |
| 3944560972 | Omnigent plan §4 explicitly consumes the complete canonical credential contract, including scope/activation/revocation/use/HTTPS/redirect constraints; §12 also consumes the full fenced recovery sequence. |

Runtime acceptance H now matches the unconditional acceptance-critical worker/Attempt separation and repair independence rules. Parent acceptance describes planned Assurance profiles without implying implemented runtime. No historical review is promoted to current acceptance, and no thread is closed by this author record.

Build learning candidate: cross-document review findings must be verified at every named owning site. A reference to a type does not prove its mapping is defined, and a field's presence does not prove its consumer validates it. Preserve dated research facts while placing supersession/accounting annotations at the original point of use. Structural trace coverage remains necessary but does not establish semantic closure.

## Repairs submitted for review

| Concern / prior thread location | Disposition and owning artifact |
|---|---|
| EffectProposal intent/bindings and retry safety (`data-model.md`, original lines 478/512) | Required executable intent/Mission/Assignment/Attempt/principal/route/credential/risk/envelope bindings; stable operation versus dispatch identity; closed retry states; durable dispatch and unknown-outcome reconciliation. |
| ContextPackage manifest and project/workspace visibility (original lines 298/304) | Existing untrusted-content contract delegates its schema to data-model; explicit project/workspace intersection added at construction and consumption. |
| Retrieval projection identity (original line 248) | Direct-source versus derived-projection discriminator with conditional mandatory generation and exact-source evidence. |
| WorkerRequirement (`plan.md`, original line 551) | Existing canonical definition in data-model section 12 remains controlling; no duplicate type introduced. |
| EngineRun authority and policy precedence (assurance-fabric original lines 236/746) | Authority mandatory for effectful runs; explicit highest-to-lowest ordering plus field specialization and separate controlling-authority path. |
| Credential transport (retrieval original line 235; historical Omnigent research line 184) | Authenticated HTTPS-only credential-bearing transport required on every hop, redirect revalidation before credential forwarding; current runtime/retrieval contracts govern. |
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

### Post-draft lifecycle consistency repairs

Mission now declares control_revision/control_state in its canonical schema, with pause/cancel/handoff state independent of coarse runtime phase and EffectResult. Automation enable/pause is a revision-checked runtime-event projection; immutable definition revisions no longer contain mutable enabled_state/updated_at fields. The first accepted occurrence checks activation revision and keeps its original definition pin. Product acceptance A–I has criterion-range author evidence; this is design inspection, not independent acceptance. K and the merge gate remain open for the final review.

## Completed cf229 review reconciliation — 2026-09-07

CodeRabbit review [5132611076](https://github.com/TheHalfMoon/wepld/pull/241#pullrequestreview-5132611076), run `21697c34-0b5c-4b9b-bd15-315bf45d1f41`, completed against base `00acb57887af4a3073374c3bfa76c506deda6f92` and head `cf22921257435fbb79ea6c0171ee2aba21ddf9ca`, reporting 12 actionable comments, one duplicate group and 42 additional comments. The selected set was all 58 files, with file-specific positive assessments as well as findings. One additional credential finding explicitly said verification did not complete. This is useful independent repair input, not acceptance of its successor or proof that every requested context/qualification condition was satisfied.

| Comment / issue | Author disposition submitted for fresh review |
|---|---|
| 3950260360 Reproduction authority | AF §15 adds effect_mode and conditional mandatory Nawat authority before process/provider/network/protected-resource execution; AF-S7-A006 owns missing-authority negative fixtures. |
| 3950260367 trigger identity | AC §3 adds required subscription_identity/logical_occurrence_identity, trusted configuration binding, replacement/replay rules and separation from runtime delivery identity; §4 uses those exact key fields. |
| 3950260381 public OAuth PKCE | AC §17 requires S256 PKCE for public authorization-code flows, no downgrade, issuer binding and public refresh protections; official RFC 9700 is linked. |
| 3950260397 CaseMessage schema | Case Bus owns payload_schema_version distinct from envelope version; exact payload digest, compatibility negotiation and original-version replay refuse unknown semantics. RD references that payload boundary. |
| 3950260409 CaseMessage trust | Case Bus derives/validates trust from authenticated provenance and trusted state; a producer label cannot promote worker/provider text. |
| 3950260418 CaseMessage addressing/access | Case Bus resolves exact policy and typed recipient from trusted Case/Assignment/item/enrollment state and checks scope, eligibility and revocation before route/replay. |
| 3950260428 context spelling | IS WebToolIdentity uses the canonical browser_context_id. WB names the precise observation/proposal fields and EffectProposal target binding. |
| 3950260434 owner spelling | RF QUALIFICATION_OWNER is Mirefa. |
| 3950260442 proposal variants | DM §19 makes execution bindings syntactically optional only under explicit DRAFT rules and conditionally mandatory for EXECUTABLE; typed WorkflowIntent/Assignment/Policy origin cases define exact reference equality/provenance. |
| 3950260446 OH-M008 coverage | Existing OH-S7-007/008/009 and OH-TB3/4 own risk/confirmation semantics, negative cases and evidence. A source-to-task table reconciles all nine mechanisms without new task/store ownership. |
| 3950260453 final review gate | No weakening or false closure. PCT acceptance J already requires qualified exact-final-base/head whole-scope evidence, exclusions, reconciliation and final race checks. PR remains Draft and REVIEW_BLOCKED until those conditions are actually met. This status finding needs final live evidence, not a self-approval prose edit. |
| 3950260460 browser review freshness | Web acceptance resolves actual live PR/base/head/check/review targets and records immutable predecessors; it no longer relies on a hard-coded PR identifier to classify freshness. |

Additional/duplicate concerns were also reconciled: typed DownloadObservation and local historical accounting annotations were prepared after the reviewed head; historical CURRENT_* identifiers now use REVIEWED_* while preserving original values. Credential transport wording is explicitly HTTPS-only with credential withholding on unsafe redirects in RF, Omnigent and hardening tasks; the older upstream observation remains labeled historical and rejected where unsafe. FR-051, runtime acceptance G and OM-WEB-002 now share the full browser/profile/context/frame/document/snapshot/tool/input/qualification/grant tuple. The reviewer must verify the complete final files, including these supplemental concerns, rather than count the 12 inline comments as exhaustive coverage.

Learning candidate: parse completed review bodies as well as inline threads. Additional comments can contain unverified or material cross-file concerns, while a green provider status only signals run completion. Follow the named owner through schema, consumer validation, acceptance and task fixtures before recording closure. All repairs above remain author dispositions pending exact-head independent assessment.


## Completed 820f322 review and successor repairs — 2026-09-08

CodeRabbit full run `3619ffef-09c2-48ac-a9ad-a865dd5c4034` completed on 2026-09-07 at 19:14 UTC against base `00acb57887af4a3073374c3bfa76c506deda6f92` and head `820f322518fbad9dd77a91d779595a7daed11c7b`. It selected all 58 package files and posted nine actionable findings plus one research clarification. Selection alone is not completed coverage proof; a separate scope/limitation response remains required. The provider's successful status does not override its findings. This section records author repairs, not independent acceptance of the successor.

| Review comment | Verified gap and successor disposition |
|---|---|
| 3952155108 | Assurance task shorthand already named its source ledger but did not explicitly define every alias/range. `analyze.md` now defines the 006-AF namespace and expansion examples, preserving distinct HARD aliases. |
| 3952155115 | Executable-policy load prerequisites used optional language. BP now requires fixed trusted admission identities, exact artifact/dependency/configuration qualification, containment and applicable effect authority before load; failures remain inert. Existing 006-POL-S6-003 covers zero-load negative fixtures. |
| 3952155119 | Event authenticity was globally optional. RD now classifies inert observations versus consequential/authority-adjacent uses with mandatory validated producer/principal/incarnation/payload/scope proof. Trigger ingress and DM Work/Mission consumers explicitly enforce it; RT-S3-003/004 cover forged/missing/stale proof and zero-transition negatives. Authentication never proves a worker result or grants authority. |
| 3952155122 | Upload flow omitted the enforcing input lease. WB now validates expiring fenced InputLease and current ownership epoch immediately before file selection, alongside Nawat and exact artifact/transfer checks, with takeover/staleness refusal. |
| 3952155125 | OM recovery dependency incorrectly required reservation for every route. It now consumes the closed Reserved/QualifiedNoReservation contract with the matching reservation requirement, exact qualification and nonempty determination evidence. |
| 3952155129 | Parent command subset lacked an explicit canonical catalog reference. Plan section 8.1 now points to command-surface, including /web, /security and /fulltest, and identifies the scoped UX subset. |
| 3952155130 | Checked A–I criteria could be mistaken for independent acceptance despite author-only prose. All 49 checkboxes are now open; the retained evidence table has distinct AUTHOR_ASSESSMENT and INDEPENDENT_QUALIFICATION states. J/K remain open. |
| 3952155134 | Historical OpenHands research still proposed a reduced AttemptEvent. It now maps source semantics losslessly into canonical RuntimeEventEnvelope/payload/provenance and refuses to fabricate missing canonical evidence or create a second store. |
| 3952155137 | FR-056 privacy exclusion used SHOULD. It now uses MUST and preserves separately qualified handling for protected secret-derived identity evidence. |
| Research clarification | Munder Difflin's CaseEventLedger is explicitly a Case-scoped materialized view of RuntimeEventEnvelope history, with canonical event identity/causality and no separate durable log. |

The two older schema/WorkerRequirement threads received rate-limit responses rather than substantive independent verification. Their author repairs remain recorded above; an unavailable chat response is neither rejection nor acceptance. Current head, checks, scope, review and thread state must be obtained live from the PR, not inferred from this historical section.

Build learning: a correct canonical owner does not excuse weaker consumer summaries, historical adaptation schemas or ambiguous checklist state. Review every projection/consumer against the owner's mandatory conditions, distinguish inert data from actionable facts, and make author assessment structurally distinct from qualified acceptance. Preserve these as planning refinements within existing task IDs and owners; no runtime implementation or source admission is authorized here.
