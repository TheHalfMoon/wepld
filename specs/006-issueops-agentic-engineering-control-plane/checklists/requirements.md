# Requirements Checklist — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CHECKLIST
IMPLEMENTATION_AUTHORITY = NONE
```

## Scope / authority

- [ ] Planning-only status is explicit.
- [ ] No S2 implementation authority is created.
- [ ] No source/dependency/network/model/provider/Git/browser/issue-write authority is created.
- [ ] P0 + S1..S10 numbering remains unchanged.
- [ ] Future activation still requires Spec Kit, Ponytail FULL, Source Acquisition, deterministic gates, independent review, applicable security review, and finding reconciliation.
- [ ] Shared contract ownership is explicit: `data-model.md` owns shared domain vocabulary; `contracts/web-agent-boundary.md` owns canonical browser/WebMCP semantic records; `contracts/assurance-fabric.md` owns Assurance semantic records.

## IssueOps

- [ ] GitHub is first provider, not internal Case identity.
- [ ] Provider observations remain append-only and conflicting observations remain inspectable.
- [ ] Provider observation completeness/authenticity, pagination/permission/rate-limit limitations, and stale states are explicit.
- [ ] Unauthenticated or partial provider data cannot masquerade as complete current truth.
- [ ] Generic latest-write-wins is prohibited for acceptance-critical cross-provider semantics.
- [ ] Case/provider schema evolution is versioned and provider-specific semantics remain extensions until promotion is justified.
- [ ] Provider effect idempotency and `EFFECT_OUTCOME_UNKNOWN` reconciliation are explicit before unsafe retry.
- [ ] `/issues sweep` outputs have explicit evidence requirements and abstention behavior.
- [ ] Duplicate/root-cause/already-fixed/security/blocker candidates have negative oracles.
- [ ] Sweep qualification uses a labeled corpus and predeclared promotion criteria.
- [ ] Probable duplicate or semantic similarity cannot auto-close or establish causal equivalence.
- [ ] TB0 proves offline/read-only end-to-end Case value before Agent Host complexity.

## RAG / Project Brain

- [ ] Retrieval signals are query/source aware rather than a rigid ladder.
- [ ] Exact/lexical/metadata/Fehrest.Maemar facts remain useful without vector infrastructure.
- [ ] Semantic/vector can be selected for conceptual/paraphrastic queries only under explicit qualification.
- [ ] Semantic/vector admission requires predeclared incremental-value benchmark evidence.
- [ ] Retrieval preserves source/projection generation, provenance, freshness, location/citation, access policy, and trust classification.
- [ ] Source access/visibility propagates through chunks/indexes/embeddings/graph projections/RetrievalEvidence/ContextPackage/worker egress.
- [ ] Access revocation/redaction/tombstone invalidates affected derived-context eligibility.
- [ ] Source refresh publishes immutable complete generations atomically and prohibits mixed-generation current views.
- [ ] Remote URL/documentation ingestion has deferred but explicit SSRF/redirect/DNS-rebinding/private-address/credential-forwarding/content-bound requirements before network activation.
- [ ] `RETRIEVAL_SCORE != TRUTH` remains structural.
- [ ] S3/S4 includes a no-agent local InputArtifact -> collection -> cited evidence checkpoint.

## Untrusted content / prompt injection

- [ ] External issue/PR/RAG/repository/document/browser/model/worker content is data by default.
- [ ] Untrusted content cannot mint WorkflowIntent or effect authority.
- [ ] Context packages use one canonical vocabulary and preserve source/trust/visibility/access/freshness/policy labels.
- [ ] Context visibility is revalidated at use/egress time; old packages cannot bypass access revocation.
- [ ] EffectProposal carries typed controlling-origin kind/ref.
- [ ] Sanitization/model refusal/injection classifiers are defense-in-depth only.
- [ ] Effect-time Nawat checks are structurally independent of prompt content.
- [ ] Adversarial corpora cover prompt injection, malicious tool output, malicious patches, secret requests, policy-bypass text, and revoked-content cache reuse.

## Command surface / UX

- [ ] `contracts/command-surface.md` is the canonical planned stable command catalog.
- [ ] `/web`, `/review`, `/security`, and `/fulltest` appear consistently in parent spec/acceptance/command-surface planning.
- [ ] `/review`, `/security`, and `/fulltest` are profiles over one Assurance Fabric, not three authority paths.
- [ ] `/web` is an intent surface over browser/WebMCP capabilities, not implicit browser authority.
- [ ] Optional aliases such as `/fix` are not presented as stable commands until separately promoted.

## Delegation

- [ ] Canonical `WorkerRequirement` exists and is distinct from selection/qualification/authority.
- [ ] Worker capabilities use a versioned WePLD vocabulary.
- [ ] WorkerDescriptor includes provider permission claims, containment evidence, session/cancellation/recovery semantics, availability, and qualification evidence.
- [ ] Edara topology, Mirefa qualification, Nawat authority, Mission Runtime execution, and UWC transport remain semantically separate.
- [ ] Early implementation may co-locate those boundaries without collapsing semantics.
- [ ] Mirefa outputs typed qualification evidence and cannot mint authority.
- [ ] Nawat denial/approval/requalification states are visible and exact-target bound.
- [ ] Mission Runtime cannot widen/reuse expired grants, silently substitute routes, or retry unknown-outcome effects unsafely.
- [ ] Cancel-request, remote termination proof, safe resume, new Attempt, and orphan/unknown runtime state are distinct.
- [ ] S5 delegation testing is dry-run/synthetic only; real worker execution remains S6-owned.
- [ ] `/delegate` is primary worker UX; `/workers` and `/handoff` can be progressively disclosed.
- [ ] No silent provider/model/worker/paid fallback.

## Native Assurance

- [ ] S7 Assurance remains semantically independent from S8 repair/completion.
- [ ] Exact `AssuranceTarget` accounts for material dirty-workspace state when relevant.
- [ ] Immutable/versioned `AssurancePolicySnapshot` defines profile/claim semantics.
- [ ] Every check has required/conditional/optional semantics under the exact policy snapshot.
- [ ] Budget/availability/authority/unsupported gaps cannot silently weaken required claim evidence.
- [ ] Typed `ClaimAssessment` outcomes include supported/not-supported/partial/inconclusive/blocked/stale.
- [ ] Missing/stale required evidence, unresolved blocking findings, or material conflicts prevent `SUPPORTED`.
- [ ] Acceptance-critical EngineRun binds actual executable/runtime/artifact identity and material rule/database/template/config snapshots plus resource/cleanup envelope.
- [ ] Engine crash/timeout/resource failure/unsupported scope/cleanup gap cannot normalize clean.
- [ ] Finding fingerprints/correlation preserve producer-specific evidence.
- [ ] Finding disposition for false positive/accepted risk/suppression/rule exception/fixed/superseded requires scope, authority, policy/target, evidence, and expiry/review where applicable.
- [ ] Untrusted/source-branch config cannot forge or extend suppressions/accepted risk.
- [ ] Evidence handling covers classification, access, storage/encryption requirement where applicable, redaction, retention/tombstone, safe rendering, and export/egress.
- [ ] Review scope/context coverage is typed evidence.
- [ ] Retry-pass remains flaky; quarantine requires owner/evidence/scope/expiry/review and cannot erase failure.
- [ ] Performance evidence binds baseline/environment/fixture/warmup/repetitions/noise/threshold/decision rule and supports inconclusive states.
- [ ] Review outcome and supported claim cannot become completion decision.

## Browser agent / WebMCP

- [ ] WebMCP is treated as a replaceable protocol candidate, not core authority.
- [ ] Planning records that the observed WebMCP specification is a Community Group Draft, not a W3C Standard/Standards-Track Recommendation.
- [ ] `contracts/web-agent-boundary.md` is canonical owner of WebTool/browser semantic record shapes; `web-agent.md` does not redeclare an incompatible WebToolObservation.
- [ ] WebMCP application tools and DevTools-class browser diagnostics are separate capability paths.
- [ ] Browser actuation, artifact transfer, clipboard/native-dialog/permission, and context-control effects are separable.
- [ ] Website tool metadata, schemas, annotations, outputs, downloaded artifacts, and clipboard content are untrusted external evidence.
- [ ] `WEBMCP_TOOL != NAWAT_GRANT` is structural.
- [ ] `WEBMCP_READ_ONLY_HINT != WEPLD_CONTAINMENT` is structural.
- [ ] Authenticated browser state/cookies/SSO/password-manager/autofill/session presence cannot become implicit authority.
- [ ] Browser session/profile/context/frame/page/origin/tool-generation identity is explicit and freshness-aware.
- [ ] Tool definition, context, access-policy, or origin/navigation changes invalidate stale acceptance-critical qualification.
- [ ] WebMCP invocation is represented as an exact effect proposal with independently derived effect class.
- [ ] No silent fallback from WebMCP to raw DOM click/type, DevTools, remote browser, another browser/profile/context, or substitute artifact route.
- [ ] Browser download produces inert/quarantined InputArtifact before parser/RAG/execution follow-on.
- [ ] Upload uses one exact authorized artifact and cannot browse/substitute arbitrary local paths.
- [ ] Popups/new tabs/frames cannot silently inherit another context's effect authorization.
- [ ] Browser diagnostics capture only the minimum authorized evidence and follow evidence handling policy.
- [ ] WebMCP/tool poisoning/output injection/cross-origin/session-confusion/artifact/duplicate-invocation negative oracles are explicit.
- [ ] WePLD publisher mode, if activated later, exposes intent/proposal surfaces rather than direct authority.
- [ ] WEB-TB0/1/2/3 provide incremental protocol/browser qualification before production actuation.
- [ ] Chrome/Edge/WebView2 support claims are reverified at owning acquisition time rather than frozen from planning research.

## Recovery / completion / durable evidence

- [ ] CompletionEvidence binds exact target/generation/policy as applicable, gates, independent review, security disposition, finding reconciliation, authority/effect/effect-reconciliation evidence, provider closeout, residual limitations, and producer.
- [ ] No acceptance-critical material effect remains `EFFECT_OUTCOME_UNKNOWN` at Trusted Completion.
- [ ] Stale/mismatched evidence and unresolved material findings fail closed.
- [ ] Merge/provider close/browser success/Assurance supported claim do not automatically establish Trusted Completion.
- [ ] S9 plans schema migration, backup/restore, redaction/tombstone propagation, and bounded evidence retention sufficient to reconstruct historical decisions.

## Source acquisition

- [ ] Donor/reference listing never equals source/dependency admission.
- [ ] OpenHands exact mechanism extraction remains research/source-acquisition input with no donor execution.
- [ ] Clean-room WePLD-native adaptation is preferred for small mechanisms unless direct source reuse is separately justified/admitted.
- [ ] Source-registry canonical rules are re-read before future reuse/import.

## Review-derived repairs

- [ ] Historical Fable findings remain recorded as historical evidence, not current-head qualification.
- [ ] Historical fields do not use misleading `CURRENT_*` labels.
- [ ] `reviews/professional-whole-plan-review-2026-09-02.md` records the later whole-plan gaps and is not counted as independent acceptance review.
- [ ] `professional-plan-hardening-tasks.md` maps every material hardening finding into the existing roadmap without creating a new authority path.
- [ ] Fresh independent exact-head whole-scope rereview is required after all repairs.
