# Requirements Checklist — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CHECKLIST
IMPLEMENTATION_AUTHORITY = NONE
```

## Scope / authority

- [ ] Planning-only status is explicit.
- [ ] No S2 implementation authority is created.
- [ ] No source/dependency/network/model/provider/Git/issue-write authority is created.
- [ ] P0 + S1..S10 numbering remains unchanged.
- [ ] Future activation still requires Spec Kit, Ponytail FULL, Source Acquisition, deterministic gates, independent review, applicable security review, and finding reconciliation.

## IssueOps

- [ ] GitHub is first provider, not internal Case identity.
- [ ] Provider observations remain append-only and conflicting observations remain inspectable.
- [ ] Generic latest-write-wins is prohibited for acceptance-critical cross-provider semantics.
- [ ] Case/provider schema evolution is versioned and provider-specific semantics remain extensions until promotion is justified.
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
- [ ] Retrieval preserves provenance, freshness, location/citation, and trust classification.
- [ ] `RETRIEVAL_SCORE != TRUTH` remains structural.
- [ ] S3/S4 includes a no-agent local InputArtifact -> collection -> cited evidence checkpoint.

## Untrusted content / prompt injection

- [ ] External issue/PR/RAG/repository/document/browser/model/worker content is data by default.
- [ ] Untrusted content cannot mint WorkflowIntent or effect authority.
- [ ] Context packages preserve source/trust labels.
- [ ] Sanitization/model refusal/injection classifiers are defense-in-depth only.
- [ ] Effect-time Nawat checks are structurally independent of prompt content.
- [ ] Adversarial corpora cover prompt injection, malicious tool output, malicious patches, secret requests, and policy-bypass text.

## Delegation

- [ ] Edara topology, Mirefa qualification, Nawat authority, Mission Runtime execution, and UWC transport remain semantically separate.
- [ ] Early implementation may co-locate those boundaries without collapsing semantics.
- [ ] Mirefa outputs typed qualification evidence and cannot mint authority.
- [ ] Nawat denial/approval/requalification states are visible and exact-target bound.
- [ ] Mission Runtime cannot widen/reuse expired grants or silently substitute routes.
- [ ] S5 delegation testing is dry-run/synthetic only; real worker execution remains S6-owned.
- [ ] `/delegate` is primary worker UX; `/workers` and `/handoff` can be progressively disclosed.
- [ ] No silent provider/model/worker/paid fallback.

## Assurance / completion

- [ ] S7 Assurance remains semantically independent from S8 repair/completion.
- [ ] Review outcome cannot become completion decision.
- [ ] CompletionEvidence binds exact target/generation, gates, independent review, security disposition, finding reconciliation, authority/effect evidence, provider closeout, residual limitations, and producer.
- [ ] Stale/mismatched evidence and unresolved material findings fail closed.
- [ ] Merge/provider close/browser success do not automatically establish Trusted Completion.

## Web agent / WebMCP

- [ ] WebMCP is treated as a replaceable protocol candidate, not core authority.
- [ ] Planning records that the observed WebMCP specification is a Community Group Draft, not a W3C Standard/Standards-Track Recommendation.
- [ ] WebMCP application tools and DevTools-class browser diagnostics are separate capability paths.
- [ ] Website tool metadata, schemas, annotations, and outputs are untrusted external capability claims/evidence.
- [ ] `WEBMCP_TOOL != NAWAT_GRANT` is structural.
- [ ] `WEBMCP_READ_ONLY_HINT != WEPLD_CONTAINMENT` is structural.
- [ ] Authenticated browser state/cookies/session presence cannot become implicit authority.
- [ ] Browser session/profile/page/origin/tool-generation identity is explicit and freshness-aware.
- [ ] Tool definition or origin/navigation changes invalidate stale acceptance-critical qualification.
- [ ] WebMCP invocation is represented as an exact effect proposal with independently derived effect class.
- [ ] No silent fallback from WebMCP to raw DOM click/type, DevTools, remote browser, or another browser/profile.
- [ ] Browser diagnostics capture only the minimum authorized DOM/console/network/screenshot/performance evidence.
- [ ] WebMCP/tool poisoning/output injection/cross-origin/session-confusion/duplicate-invocation negative oracles are explicit.
- [ ] WePLD publisher mode, if activated later, exposes intent/proposal surfaces rather than direct authority.
- [ ] WEB-TB0/1/2/3 provide incremental protocol/browser qualification before production actuation.
- [ ] Chrome/Edge/WebView2 support claims are reverified at owning acquisition time rather than frozen from planning research.

## Review-derived repairs

- [ ] ARCH-001 concern is addressed without collapsing qualification and authority.
- [ ] ISSUEOPS-001 concrete sweep mechanisms are specified.
- [ ] RAG-001 semantic retrieval trigger/qualification is clarified.
- [ ] DELEGATE-001 interfaces are explicit.
- [ ] SECURITY-001 structural prompt-injection protections are specified.
- [ ] Provider conflict handling is explicit.
- [ ] First IssueOps tracer bullet is explicit.
- [ ] Case-model evolution is explicit.
- [ ] Trusted Completion evidence minimum is explicit.
- [ ] Fresh independent rereview is required after all review-derived and later planning changes.
