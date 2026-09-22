# Capability and source acquisition plan

STATUS = PLANNING_QUALIFIED_FOR_FIRST_TASKS; SOURCE_ADMISSION = NONE.

Read [source inventory](SOURCE_INVENTORY.md) for all 402 historical entries, all requested source identities, exact inspected Git revisions and skill paths. Read [feature parity](FEATURE_PARITY_AND_PRODUCT_FLOWS.md) for behavior requirements. No donor was installed or executed. Metadata/README/tree inspection is not a security audit, test pass or deployment qualification.

## Rights and provenance

The founder states permission to copy and use all listed sources and sources in the repository. Record that as FOUNDER_PERMISSION_ASSERTED_2026_09_20, not as a fabricated upstream license, blanket commercial-hosted entitlement or proof that a public client contains the hosted core. Work on planning and permissively licensed candidate qualification proceeds without another generic permission question.

For each actual import, record the selected paths and artifact hash, rights holder, applicable license/NOTICE and dependencies, plus the custom grant document if relying on permission beyond published terms. Scope includes redistribution, modification and embedded third-party assets. Keep this evidence with the import; preserve required notices. Unknown rights block that import, not independent original implementation, interface design or the remainder of the plan. Repository visibility and GitHub license metadata alone settle neither rights nor security.

Technical disposition and rights are separate columns: EMBED, ADAPTER, SALVAGE, BEHAVIOR_REFERENCE, BENCHMARK_REFERENCE, DEFER or REJECT; independently, rights may be qualified, conditional, asserted or unresolved. No marketing promise is a technical test. No source count is a success metric.

## Minimum acquisition record and pipeline

Need → existing registry/stdlib search → two or three mechanism candidates → exact source and test paths → rights/dependency/build-script inventory → safety/portability/maintenance analysis → wrapper and exit strategy → negative-oracle mining → isolated conformance → admission decision → bounded integration → benchmark. Source tests are evidence to inspect and adapt; executing their build scripts requires a qualified sandbox and separate authorization.

Every record has: capability/task, repository and exact revision/tree/blob, package/release mapping, path set, code/test evidence, license/NOTICE/custom grant, transitive graph, build hooks/network/remote-code behavior, supported OS/toolchain, advisory/maintenance observation date, performance budget, authority boundary, adaptation/porting cost, alternate/exit route, conformance fixtures, residual gaps and decision owner. Preserve provenance when translating TypeScript/Python mechanisms to Rust; language preference never justifies careless reimplementation.

## Near-term machinery and continuity

| Mechanism | Existing evidence / proposed disposition | Required gate |
|---|---|---|
| S3 contracts | Existing serde/serde_json and Spec 007 C001..C013; no new serializer needed | ASTRO-F01/C01; exact three paths only |
| Windows APIs | Microsoft Job Objects are the process-tree oracle; windows-rs candidate pin 5f8e1504dea507f1d86af7bf5a824eb49ff8b5a5 from prior research, not fresh admission | ASTRO-A01/A02; resolve exact package/features/MSRV and run native assignment, breakaway, last-handle and descendant cancellation tests |
| PTY | wezterm/wezterm portable-pty historical pin fe3006aefcdc4c22924e7bce966b2c430dade4f1; presentation candidate | ASTRO-A03; immediate-child kill cannot establish whole-tree containment; no PTY required for pure contracts |
| Parsing | Tree-sitter historical research pin 1b8407d1e718f2a26e2886c03cc55622d8d1d7bd; bounded syntax machinery candidate | ASTRO-A04; grammar/query/external-scanner rights, cancellation, malformed input, rebuild and language matrix |
| Precise semantics / retrieval | SCIP/rust-analyzer/ctags, ripgrep/Tantivy/SQLite families already in registry | ASTRO-A04; one bounded language/profile first; lexical/syntax baseline before vectors |
| Runtime / workers | DeepSeek, TrueForge, Codex/Pi/OpenHands/Continue and existing Spec 006 research | ASTRO-A05; one host and UWC contract, reject importing multiple full runtimes |
| Policy | Cedar first candidate; OPA adapter later; OS containment remains separate | ASTRO-A06; Nawat owns grants, not donor PDP or plugin approval |
| Assurance | Alibaba OCR, PR-Agent, Continue, Qodo public edges, Cloudflare skill, Playwright/TestSprite/Momentic | ASTRO-A07; producer coverage/independence/egress and local-vs-hosted truth |
| Change / recovery | Git qualified route, Jujutsu/Mergiraf/GitButler, in-toto/TUF/Cosign/SLSA patterns | ASTRO-A08; no replacement of canonical evidence with Git state |
| Later capabilities | Research/docs/design/voice/Teams/Hub/memory sources listed below | ASTRO-A09/P01; select per profile, not blanket package installation |

Official containment references: [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), [AppContainer](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation). Job Objects alone do not isolate filesystem/network. No hostile-worker qualification exists at the base. S3 fixture execution, host API use and spawn each require the relevant separate authority.

## Fresh mechanism findings that change the plan

| Source / exact file at pinned revision | Inspected result | WePLD acquisition decision |
|---|---|---|
| Vane, `src/lib/agents/search/researcher/index.ts` | Iteration ceilings differ by search mode; action tools depend on classification/source/file inputs | ADAPTER/SALVAGE candidate for research loop and source selection; add wall-clock, byte and monetary ceilings, cancellation and citation validation. README lists authentication as upcoming, so do not expose its service as a team boundary |
| DeepSeek, `docs/architecture.md`, `SAFETY.md` | Plugin architecture; explicit unaudited developer-preview warning and broad execution powers | SALVAGE composition/event mechanisms; reject wholesale trust-boundary adoption |
| TrueForge, `agent-session/schemas/events.ts`, `tests/agent-session/store/storeContractSuite.ts` | Terminal/paused event shapes; tests for tenant identity, deletion races and pagination | SALVAGE lifecycle/test ideas behind WePLD records; test titles inspected, suite not executed |
| Alibaba OCR, `ASSURANCE_CASE.md`, `cmd/opencodereview/output_manifest_test.go` | Coverage/waiver/failure/budget output cases; assurance prose also names user-configured shell/MCP exceptions | ADAPTER first; require independent audit of actual reachable tools rather than repeating the broad “Git only” summary |
| OpenReview, README and package manifest | Review workflow includes dependency installation and automatic commit/push; root license not established by inventory | BEHAVIOR_REFERENCE, conditional source salvage after specific rights evidence; split review, test execution, repair and push grants |
| Continue, README | Final 2.0.0 and no-active-maintenance statement despite API archived=false | SALVAGE or explicitly maintained adapter; preserve discrepancy, budget fork maintenance; no assumed hosted service |
| PR-Agent, README and reviewer module | Legacy community project distinct from Qodo; help_docs documented disabled pending credential issue | ADAPTER candidate with narrow commands and egress; no automatic enabling of disabled functions |
| TestSprite, README and selected CLI tests | Hosted runs, local tunnel, run receipt, detached-vs-cancelled behavior, failure artifacts | ADAPTER candidate; local target can still transmit data. Record transport/owner/billing semantics and do not infer hosted engine source rights from CLI license |
| TeamAI, LICENSE and usage guide | MIT text although metadata NOASSERTION; team resource synchronization and learning | SALVAGE versioned team distribution; do not auto-pull executable rules into authority |
| Orca, `docs/reference/remote-wire-compatibility.md` | Capability negotiation, absent/null distinction, epoch/cursor compatibility | Priority SALVAGE/CONFORMANCE oracle for ASTRO-O03; upstream degradation rules must still fail closed for WePLD authority |
| Orca, plugin retention audit docs | Generation/lifetime and bounded log retention claims with reproduction scope | Mine tests before adaptation; treat audit claims as upstream evidence, not independent WePLD proof |
| AnythingLLM, `collector/utils/url/index.js` and corresponding tests | Loopback is deliberately allowed; broad override exists | Require WePLD destination policy at resolution/redirect/use, not direct adoption as SSRF boundary |
| OKF, `SPEC.md` | Portable provenance/verification/lifecycle and attested-computation descriptions | INTERCHANGE adapter; foreign human/machine verification never becomes a local grant or unquestioned truth |
| Matt Pocock, 38 SKILL.md paths | Small engineering/productivity packs plus in-progress items; no literal debate skill | SALVAGE/adapt feature-by-feature; preserve attribution and mark experimental packs. Add founder debate flow explicitly |

These are bounded inspections, not vulnerability reports about the donors. The source inventory records every downloaded evidence path/hash and the depth distinction. Tests not executed are never reported as passed.

## Source composition by capability

| Capability family | Candidate composition / outcome | Gate and exit |
|---|---|---|
| Project Brain | lexical search + incremental syntax + precise semantic seam + provenance; optional vectors | ASTRO-A04/F03/F04; known stale/unknown facts and deletion respected |
| Research | Vane orchestration + existing SearXNG/retrieval/docling families; independent citation checks | ASTRO-K01; licensed content, SSRF protection, evidence-backed report |
| Knowledge memory | Existing Fehrest contracts + Memanto behavior + OKF interoperability | ASTRO-K02; deterministic scope/provenance and loss-aware export; no new memory authority |
| Worker orchestration | DeepSeek/TrueForge/Orca mechanisms + existing UWC and durable Runtime | ASTRO-A05/F05; qualification and restart/cancel tests |
| Review | Alibaba structured coverage; PR-Agent provider edges; maintained alternative to Continue; Qodo components separately | ASTRO-A07/R01/R02; no reviewer outcome treated as completion |
| Test | Playwright local runner first; TestSprite/Momentic optional adapters; collection as comparison only | ASTRO-Q01/Q02; deterministic oracle unchanged by locator repair |
| Security | Existing Codex Security policy; Cloudflare coverage/validation mechanics; static/scanner registry | ASTRO-S01/S02; threat-led coverage and independent validation |
| Design | Existing design donors + Archify typed graph + AutoClaw product reference | ASTRO-P06; editable artifact, provenance and accessible render |
| Office/content | Existing document/image/table/export tools, AutoClaw/AnythingLLM behavior references | ASTRO-P03; artifact and formula/citation checks |
| Meetings/live | Local STT candidates + AnythingLLM UX + ADK streaming adapter patterns | ASTRO-P07/P08; explicit recording/media/retention and interruption tests |
| Teams | Nawat/Work native semantics + TeamAI sharing + TrueForge tenant test ideas | ASTRO-T01..T04; isolation, revocation, concurrent edits and restore |
| Community | Mirefa packages + DeepSeek/TrueForge/AnythingLLM catalogue patterns + skills | ASTRO-H01/H02; signed immutable packages, quarantine, rights and update/exit safety |
| Typed decisions | TypeSafe optional provider adapter; schema-valid output and calibration harness | ASTRO-K03; held-out confidence calibration, abstention, no autonomous grant |

The 402-entry universe remains accounted, not freshly admitted. Post-V1 candidates do not change frozen counts. Duplicate Alibaba/Orca links in the request are one source each; Qodo organization is separate from PR-Agent's current repository. Source families sharing a repository are aliases only when identity is established. Vane's potential Perplexica history must not be silently assigned a registry identity without evidence.

## Local intelligence source-family amendment

The founder-requested OCR/document intelligence, retrieval/RAG, memory, typed decisions/PLD, tool/skill registry, browser/web, desktop and event-intelligence sources are reconciled in [WEPLD_LOCAL_INTELLIGENCE_CAPABILITY_AMENDMENT.md](WEPLD_LOCAL_INTELLIGENCE_CAPABILITY_AMENDMENT.md) with candidate identities and fresh pins in [INTELLIGENCE_SOURCE_INTAKE.md](INTELLIGENCE_SOURCE_INTAKE.md).

This is a bounded source-family expansion, not bulk admission.

```text
NEW_ROADMAP = NO
NEW_AUTHORITY_OWNER = NO
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
MODEL_EXECUTION_AUTHORITY = NONE
```

Near-term source routing:

| Capability | Candidate sources | Existing gate |
|---|---|---|
| OCR / document intelligence | DeepSeek-OCR-2; Cohere Parse as behavior/benchmark reference; existing Docling/parser family | ASTRO-A09/A04 -> ASTRO-P03 |
| Typed decisions / PLD | SemIf, Mapika Decider, Bespoke Nimble 9B, future TypeSafe/Jev adapter | ASTRO-A09/A05/B01 -> ASTRO-K03 |
| Tool / skill / MCP discovery | Treg selected mechanisms | ASTRO-A09/F06 -> ASTRO-H01/H02 |
| Runtime lifecycle | Google AX selected concepts; no Kubernetes/Redis default dependency | ASTRO-A09/A05 -> F05/U01/U02/O03 |
| Browser / web acquisition | TinyFish AgentQL; BigSet workflow behavior | ASTRO-A09/F04/F06 -> K01/P05 |
| Desktop / terminal interaction | Desktop Commander mechanisms behind UWC/Nawat | ASTRO-A09/U02/F06 -> P05/O02/O03 |
| Event intelligence | Laya behavior/source-permission reference until exact source artifact is pinned | ASTRO-A09 -> P04 |
| Memory / local privacy / context | founder-owned Morize/Kernux selected mechanisms plus existing registry candidates | ASTRO-A04/A09/F04 -> K02/B03 |
| Assurance/sandbox evidence | founder-owned Ascout/MESC selected mechanisms where the owning task needs them | ASTRO-A07/A09 -> owning Assurance/runtime profile |

Each actual import remains capability-triggered and path-level. Founder permission is recorded as rights evidence where applicable but never replaces exact source identity, selected paths, license/NOTICE/custom-grant scope, dependency/build-hook review, conformance, security and exit strategy.

## Build-from-scratch exceptions and exit costs

WePLD must own Nawat effect semantics, exact-target evidence binding, completion, context provenance, package admission and recovery composition. These are differentiators, not reasons to reimplement browser engines, parsers, terminals or authentication protocols. Any native rewrite needs a comparison of embedding, wrapping, porting and original implementation, test corpus transfer, ongoing maintenance and a removal route. Expensive services enter only after a bounded alternative fails measured requirements.

Every admitted adapter exports neutral records and has a kill switch, version pin, migration/rollback plan and a replacement test suite. Model weights with custom remote code are rejected by default; qualify code, weights, tokenizer, formats, dependencies, rights and isolated execution separately. A license-compatible package remains unqualified until its behavior and operational boundary pass.