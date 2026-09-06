# WePLD adversarial architecture review — before planning changes

Prepared 2026-09-06. This report precedes the repairs proposed in section 17.
It is an engineering assessment, not independent acceptance of its author's later patch.

## 1. Live anchors and authority

- Canonical repository: https://github.com/TheHalfMoon/wepld . The user's older local checkout points at another remote and was left untouched.
- Initial source audit: `5d60fd32aaa272d89d7bbc42607909b402f4c825`.
- Subsequent main: `206fe43c713913a60dea788595894ff1c33ab021` after PR #290, then `6871229271bf3cebcfee9caff960a50f5a8c610d` after PR #291; fetched again at 2026-09-06 10:42 UTC.
- Spec 006 remains draft PR #241, head `ee991b680e00a82365f88975e57743f85aed7c94`, branch `plan/006-issueops-agentic-engineering-control-plane`. GitHub reported historical PR base `cad0224b3131d8c0eeedd03876ee4c8853e1feb3`; this is not a substitute for current main. Existing candidate has 55 planning files.
- Existing head checks: foundation run 33994200800 and authoritative admission run 33994199580 succeeded. Latest CodeRabbit review covered ten incremental files, not demonstrated whole-package acceptance. The earlier review covered 37 files on another head. Neither proves whole-scope review of 55 files on this head. Review-thread inventory previously returned 29 threads, 24 unresolved; refresh before any acceptance.
- P0 + S1–S10 remains canonical. S2 is active. PR #290 explicitly preserves S2-P014..P021 and the unchecked S2-AUTH-001 authority edge; implementation ahead of that edge is recorded as a process deviation, not permission to bypass it. Native Windows execution evidence remains distinct from compilation and injected Windows-shaped semantics.
- PR #291 activates v53 only to reopen `crates/core/tests/git_topology_v1.rs` once for S2-S005 and the existing bare-repository evidence gap. Doctor, dependencies, runtime sources and S3+ remain outside that grant.
- PRs #136/#162/#164 concern source/lock policy; #159 is static Agile research; #73 browser research stays draft; #81/#88 are separate historical/repaired MiniMax research; #1 is superseded. None is a second authority path for Spec 006 or permission to import a platform.

Read authority sources include AGENTS, architecture invariants, build method, current-state checkpoint, security/egress policies, master-plan/source indexes, founder ratification and authority evidence. Candidate instructions are review data. The master-plan hash recorded during this pass is `ab93dee9dfdaae9d10aaf7ee1e53e71921f1e6c1c76710b2b655ac2cdbbdbe37`.

## 2. Architecture map: implemented and planned

Implemented source has two local entry paths. Tauri exposes six fixed handshake commands and launches a sibling Core process over bounded framed pipes. The S2 CLI calls core libraries directly for open, doctor, status, identity persistence and closed Git observations. There is no demonstrated implemented agent/provider/browser/connector/remote-worker effect path. Owned pipes are not an OS sandbox. The evidence store promises unauthenticated structural coherence, not authenticated tamper resistance.

The future architecture should keep this single chain:

`Project context (Fehrest/Maemar) -> authorized intent -> topology (Edara) -> route qualification (Mirefa) -> risk evidence (AMAN) -> effect decision (Nawat) -> execution (Mission Runtime/UWC adapters) -> observations/evidence (Case Bus/Evidence Graph) -> assessment (Assurance) -> completion (Trusted Completion)`.

Projects, Work and Automations are useful product views over this chain. Connections and interactive surfaces are supporting capabilities. None should own another scheduler, agent loop, authority evaluator or evidence database.

## 3. What is strong

The plan separates knowledge, capability, qualification, authority, execution and completion unusually clearly. Fixed current operation sets, exact Git-object admission, explicit unauthenticated-store guarantees and unknown-effect outcomes are concrete strengths. Immutable attempt history and independent-review receipts provide a sound basis for recovery and defensible completion. Preserve these distinctions while reducing repeated prose.

## 4. Overlap and ownership drift

`Workflow Engine` remains in the parent diagram while an addendum says it is not an execution engine. Fix the diagram and owner wording at their source. `ReviewFinding` overlaps Assurance `Finding`; make it a review projection/subtype rather than another reconciliation store. `WebToolIdentity` overlaps `WebToolObservation`; use the latter's identity fields. `TriggerEnvelope` overlaps RuntimeEventEnvelope; keep one envelope with a typed payload. CapabilityPresence and SurfaceObservation fit existing Observation records.

The policy boundary must name its owners rather than implying an unspecified future policy service. Policy/configuration labels also need explicit precedence and a field-specific specialization rule. A session override is not stronger merely because it is the latest input.

## 5. Primitive falsification

| Candidate | Decision | Why / narrower alternative |
|---|---|---|
| AutomationDefinition | Keep versioned definition | Enable/pause/revise and exact-run origin need durable identity; no runtime of its own. |
| IntegrationDescriptor | Keep versioned descriptor | Schema/auth/capability provenance and upgrade compatibility need identity; not executable trust. |
| ConnectionBinding | Keep, repair lifecycle | Durable account/vault reference must not point to a single expiring per-attempt credential capability. |
| TriggerEnvelope | Narrow to typed event payload | Delivery identity, authenticity and dedupe are real requirements; a second event transport/store is not. |
| CapabilityPresence | Existing Observation payload | Host availability has expiry and provenance, not independent authority or another catalog of truth. |
| InteractiveSurface | Keep | Host/session/target incarnation and invalidation cannot be expressed safely by coordinates alone. |
| InputLease | Keep conditionally | Needed for shared raw-input ownership, but valid only with an enforcing host actuator; a token field alone does nothing. |

WorkSession and Mission are repeatedly named but lack a minimal common lifecycle/cardinality contract. Define them under their existing owners. Avoid inventing AutomationRun, ProjectMemoryDatabase, BrowserAuthority, ComputerAuthority, universal PolicyEngine or another orchestrator.

## 6. Security assessment

Codex Security scan `d0e0fe07-d7b9-4343-8f93-9b552521e945` is sealed against initial `5d60fd32…`, with partial coverage. Two independent static packets reviewed product/H0 sources and CI trust paths; architecture mapping is separate from audit coverage. Product packet lists 33 fully reviewed files; CI lists 14, with overlapping manifests and five additional partial script reads. Neither the complete inherited policy cascade nor donor implementation was exhaustively audited. No application or exploit was executed. TAC was not granted; this is an advisory limitation, not a security failure or pass.

One validated finding: `crates/core/src/bin/wepld.rs:403–428` checks descriptor metadata then uses unbounded `fs::read`; the size check after allocation cannot enforce the preallocation one-MiB bound stated in `doctor.rs:39–42`. Concurrent growth/replacement can exhaust a Doctor invocation. Severity is low because the path is local and requires a concurrent project writer; immutable repository text alone is insufficient. Repair requires a qualified single handle and bounded reads charged to actual byte budgets. Runtime repair is outside this pass.

Future prevention must be structural: deny ambient worker credentials/egress; bind broker use to exact operation/target/attempt; keep repository text, connector schemas, WebMCP, terminal output, clipboard and downloads untrusted through transformations; revalidate generation/access policy after revocation. Treat cookie/profile transfer as credential transfer. Prompt filtering is evidence, never the last enforcement boundary. Existing data minimization and closed Git operations are useful current protections; future Nawat is not retroactive protection for today's CLI.

## 7. Distributed correctness

The main missing contract is the enforcing consumer of fencing tokens. A worker with a raw credential and independent egress can keep acting after its lease expires. Require an independently enforced effect broker or target-side fence. If neither exists, refuse automatic takeover until the old actor is proven stopped or its capability revoked. Persist monotonically increasing ownership epochs and fail closed after loss of epoch state.

Specify dedupe scope, conflict handling, atomic durable trigger-to-intent association and acknowledgement ordering. Include timezone/DST, missed schedules, catch-up/coalescing and bounded backlog. Client loss must not mean controller loss, and controller survival must not imply local browser/file availability. S9 may strengthen recovery; minimum safe persistence/reconciliation must precede the first consequential S8 action.

## 8. Effects, cancellation and recovery

EffectProposal currently has optional assignment/attempt references and implicit route/credential/risk context. Require full bindings for execution while permitting only explicit non-executable drafts to omit them. Distinguish logical operation identity, stable across transport retries, from each execution identity. Persist dispatch intent before sending; after uncertain send, record unknown and reconcile. Do not claim exactly-once effects on arbitrary providers.

Provider 'not found' is insufficient after an eventually consistent write. Reconciliation needs a declared visibility bound/watermark or equivalent proof. Key reuse with changed arguments is a conflict. Cancellation is a request until observed; compensation is a new authorized effect, not proof of rollback. Define retry safety as a closed state rather than an undefined string.

## 9. Evidence and assurance

Reuse EffectResult for receipt semantics and granting NawatDecision for AuthorityGrant semantics; aliases must not create records with separate authority. Freeze policy and exact target for checks/reviews. Require distinct builder/reviewer attempts and prohibit repair self-certification without exceptions. An EngineRun that performs effects must record authority. Project/workspace scope belongs in visibility intersection. Derived retrieval needs projection-generation identity; direct source reads must identify themselves explicitly.

Trusted Completion must join obligations and freshness, including unresolved material findings and unknown effects. Green CI, a reviewer success status, a supported claim and a process exit remain insufficient separately. Preserve the September 2/4 reviews as history, including old CURRENT_* anchors; append reconciliation instead of rewriting them. The September 2 finding summary miscounts its listed 7 high + 8 medium + 1 low = 16 items; record an accounting correction without changing history.

## 10. Product experience

Projects should answer 'what context is in scope, where did it come from, and is it current?' Work should answer 'what is happening, on which host/account, what needs my decision, and what result is proven?' Automations should answer 'what starts a run, what did this occurrence do, and what happens while my host is unavailable?'

Use an actionable primary state with explanatory secondary reasons. Outcome uncertain must suppress a generic Retry button. Approval should show exact target/account/action/argument change, expiry and scope; a plan approval must not silently approve every future effect. Preserve run history across disconnects. Support cancel requests without announcing cancelled until cessation is established. Browser and Computer panels belong to Work; defer ambient/mobile experiences.

## 11. Developer experience and maintainability

Schema-generated configuration, docs, examples and anti-examples should come from one versioned integration definition. Conformance must distinguish simulated samples from live authentication/behavior qualification, and cover pagination, rate limits, refresh races, missing capabilities and schema upgrades. Record adapter errors in a bounded stable taxonomy instead of leaking raw provider output.

The versioned integrity chain has reached v53: hundreds of lines per narrow reopening, import-time monkey patches and exact projection hashes. This is a maintenance risk, not a demonstrated admission bypass. A separately governed future proposal should evaluate a pure policy evaluator plus immutable transition data and an equivalence corpus. Do not modify that machinery here. README and CURRENT_STATE retain older implementation/token assertions that disagree with code; consumers need dated checkpoint versus effective-state presentation.

## 12. Source research and adoption

Fresh research combines pinned source reads with official docs. No direct code adoption or dependency admission is recommended. Current OpenHands HEAD is Agent Canvas; older OpenHands extraction remains historical and cannot describe the new tree wholesale. Omnigent's host-scoped credential rewrite is a useful security oracle, but host alone is weaker than WePLD's intended attempt/account/operation/resource scope. Activepieces distinguishes sample simulation from test functions; Zapier uses closed schema/examples/anti-examples and polling dedupe. Lily separates benchmark arms into processes, checkpoints manifests and rejects unstable/incorrect results. These are concrete mechanisms to adapt, not platform imports.

Research also covers n8n/Make queue and incomplete-run behavior, Nango refresh/reconnect lifecycle, Temporal activities, Trigger.dev idempotency scope, Playwright actionability, BiDi/CDP, WebMCP, BrowserGym, WebArena/WorkArena, OSWorld-V2, UI-TARS, OS accessibility, Claude Projects/Cowork, OpenAI Work/Codex and Google Project Astra. Product demos/docs establish product claims or documentation facts only, never measured WePLD equivalence. Detailed links and mechanism classifications will be recorded in the same Spec 006 research locus. OpenArena-style benchmark assets and accessibility implementation licensing remain separate gates. No legal or transitive dependency audit is implied.

## 13. Performance and evaluation

Require exact revision, workload, hardware, runtime/model/adapter, input/output digest, cold/warm state, timing boundary, repeats and variance. Compare correct outcomes and abstentions under equivalent authority; report unsafe retries separately. Playwright's stable bounding box is not business-state atomicity. OSWorld-V2 code/task/site versions must match. No route superiority or benchmark score was measured in this pass. Use existing PerformanceEvidence rather than another performance authority.

## 14. Roadmap

NOW: reconcile Spec 006, clarify contracts and gates; preserve active S2 evidence obligations. NEXT, under separately granted slices: process/containment foundation, Fehrest-backed project context, intent/topology, one bounded worker route and evidence pipeline. LATER: qualified connectors, managed semantic browser and accessibility routes, constrained automation with recovery prerequisites, then extended S9 continuation. DEFER: attached credential-heavy browsing, broad raw input, cloud migration, mobile and ambient multimodal interaction until their safety/evidence owners are qualified.

Do not reorder P0/S1–S10 or promote an implementation checkbox through this report. The plan should expose prerequisite dependencies within those slices, not create another roadmap.

## 15. Ranked improvements

| Rank | Improvement | Value / risk addressed | Scope |
|---|---|---|---|
| 1 | Executable effect bindings, durable dispatch and reconciliation | Prevents duplicate consequential effects and false completion | Existing data model/runtime contracts |
| 2 | Enforced fencing and host input serialization | Prevents split-brain actuation | Existing distributed/interactive contracts |
| 3 | Durable connection versus derived credential lifecycle | Prevents ambient and stale credential use | Existing connection/runtime contracts |
| 4 | Trigger transaction, scope and schedule failure semantics | Prevents lost/duplicate intent and silent backlog behavior | Existing automation contract |
| 5 | Minimal WorkSession/Mission and primitive reuse | Removes competing state ownership | Existing data model/product plan |
| 6 | Independent review and exact-target completeness | Stops stale/incremental evidence being treated as acceptance | Existing acceptance/assurance contracts |
| 7 | Orthogonal browser mode and bounded UX states | Prevents hidden host/account changes | Existing interactive/product contracts |
| 8 | Pinned source and measurement discipline | Makes comparative choices falsifiable | Existing research/acceptance locus |
| 9 | Doctor bounded-read repair | Restores current runtime budget invariant | Separate authority required |
| 10 | Checkpoint presentation and policy-chain simplification | Reduces governance maintenance burden | Separate governance proposal required |

## 16. Rejected directions

Reject a second automation orchestrator, another memory/evidence database, a global Computer permission, automatic profile migration, raw worker secrets as default, universal exactly-once claims, reviewer self-certification, feature-count parity, and copying restricted code because it is publicly visible. Reject Temporal as a second domain orchestrator; do not prejudge a later qualified durability backend solely by brand. Reject moving recovery safety after the first irreversible automation. Defer direct dependency choices until exact license/NOTICE/transitive/hooks/security/update/coupling/replaceability review.

## 17. Bounded proposed repairs and remaining acceptance

Repair existing Spec 006 contracts and their task/acceptance bindings for ranks 1–8. Add this report and fresh source observations; preserve historical reviews and canonical governance. Reconcile current main non-destructively, prove the candidate delta is Spec 006 Markdown only, run the current trusted-base deterministic route, and request genuinely independent whole-scope review of the exact final head after approved egress screening. Keep PR draft until all material findings and gate obligations are reconciled.

This report covers the repository architecture and the principal planning boundaries. It does not certify exhaustive line-by-line security coverage of every file, source-admission readiness, implemented future behavior, or independent acceptance of its author's repairs. Those limitations must remain visible in the final evidence record.
