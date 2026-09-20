# Feature parity and product flows

STATUS = PLANNED_NOT_IMPLEMENTED. All task references resolve in the [handoff](WEPLD_MUSE_EXECUTION_HANDOFF.md). Sources and pins are in the [acquisition plan](WEPLD_CAPABILITY_AND_SOURCE_ACQUISITION_PLAN.md). This inventory covers publicly documented capabilities; it does not claim that inaccessible account-only features, every unpublished skill, or vendor performance claims have been verified in operation.

The founder requests capability completeness, enterprise Teams and a Community Hub. Features below stay in the backlog even when their prerequisite slice is later. WePLD will implement equivalent useful behavior through its own contracts and qualified donors. Product names, marketing assets, promotional token amounts and unsupported security guarantees are not parity requirements.

## Review, Test and Security: where users activate them

The Project navigation contains **Review**, **Test**, and **Security**. The same actions are available from a selected change/PR, the command palette and the CLI. A project's overview shows the latest exact-target result and its age, including “not run” and “coverage incomplete”. These are three views of Assurance with distinct run profiles, not three competing engines.

| Action | User chooses | Run and results | Explicit next action |
|---|---|---|---|
| Review | Working changes, commit range, PR, files or repository snapshot; standards/spec/correctness focus; eligible local/remote producers | Freeze base/head and dirty snapshot; reveal included/excluded files and estimated spend; inspect findings with exact locations, rationale, reproduction, coverage and disagreements | Dismiss with reason, request validation, assign owner, or propose repair. A suggestion never writes by itself |
| Test | Existing suite, selected cases, generated plan, changed-code tests, API, browser, accessibility, visual or performance profile | Discover runner; inspect prerequisites/environment/network; approve generation separately from execution; show steps, logs, traces, screenshots, assertions and failed/blocked/skipped/flaky counts | Rerun same target/environment, investigate, export JUnit/SARIF-compatible evidence where meaningful, propose test/code repair |
| Security | Diff or snapshot; dependency/secrets/static/architecture/agent-boundary profile; depth and allowed validation methods | Show threat coverage and safe validation limits; keep confirmed, unresolved and rejected findings distinct; redacted evidence and exact source trace | Triage, assign, authorize bounded fix or accept a named residual risk through policy. No automatic exploitation or public disclosure |

All three offer **Run now**, saved profiles, run history, compare runs, cancellation and export. Team administrators may define required profiles and later schedules; defaults are local and manual. A hosted producer shows destination, content scope, retention/training decision and secret screening before transmission. A disconnected/unsupported producer yields UNAVAILABLE, not a green result. A changed target makes previous results historical. Cancel requested, stopped, and unknown remote outcome are separate states.

Accessibility includes keyboard-only target selection, focus restoration, readable inline findings, non-color status indicators and screen-reader summaries. Friendly labels lead; detailed technical evidence is expandable. The UI must never say “secure”, “all tests pass” or “ready to ship” when the relevant coverage is missing.

Core acceptance journey: make a known faulty local change → Review finds or misses it with declared coverage → Test reproduces it → Security handles a separate seeded boundary flaw → choose one repair → fresh Attempt → all applicable evidence refreshed → independent acceptance. ASTRO-R01/R02, Q01/Q02, S01/S02 and B02 own this journey.

## AutoClaw: documented feature inventory

Official source keys: [AC-home](https://autoclaw.z.ai/), [AC-download](https://autoclaw.z.ai/download/), [AC-changes](https://autoclaw.z.ai/changelog/), [AC-overview](https://autoclaw.z.ai/blog/product/what-is-autoclaw/), [AC-cluster](https://autoclaw.z.ai/blog/product/autoclaw-cluster-mode-professional-team/), [AC-use-cases](https://autoclaw.z.ai/blog/product/autoclaw-cluster-mode/), [AC-personas](https://autoclaw.z.ai/blog/product/multi-agent-work-life-isolation/), [AC-learning](https://autoclaw.z.ai/blog/product/hermes-self-evolution/), [AC-design](https://autoclaw.z.ai/blog/product/auto-design-ai-designer/), [AC-design-release](https://autoclaw.z.ai/blog/product/autoclaw-v1-9-0-glm-5-2-auto-design/), [AC-models](https://autoclaw.z.ai/models/), [AC-visual](https://autoclaw.z.ai/blog/model/glm-5.3-flash/).

Evidence is DOCUMENTED_VENDOR_BEHAVIOR, not hands-on validation. Prior research read the linked product articles, download/models and visible changelog; September 20 homepage refresh succeeded, changelog refresh intermittently failed. Latest previously observed entry was v1.17.8 dated August 27. Article/model date inconsistencies remain unresolved; no current binary was installed. The “50+ skills” and “140+ styles” claims lack a complete public item catalogue. ASTRO-P01 must close that catalogue gap before claiming literal full parity.

| ID | Documented capability / source key | WePLD requirement and acceptance | Owner / task |
|---|---|---|---|
| ACF-01 | Packaged desktop setup; AC-download | Open a project without requiring a developer shell; verify signed installer/update identity and recover failed upgrade | Presentation / ASTRO-P02 |
| ACF-02 | Windows and Intel/Apple Silicon macOS; AC-download | Publish per-platform qualification; unsupported platforms say unavailable | Runtime / ASTRO-P02 |
| ACF-03 | Account onboarding and credits; AC-home | Optional managed account/entitlement profile coexists with local use; show quotas before paid work | Work / ASTRO-P02 |
| ACF-04 | Goal-driven tasks; AC-overview | Compile natural-language objective into inspectable plan and measurable outcome | AGILLE / ASTRO-F05 |
| ACF-05 | Files, scripts and APIs; AC-overview | Read/write/execute/network are separate effect classes with bounded results | Runtime / ASTRO-F06 |
| ACF-06 | Word/report authoring; AC-home | Export editable document with checked headings, citations and no hidden overflow | Work / ASTRO-P03 |
| ACF-07 | Spreadsheets and charts; AC-home | Preserve formulas, units and source cells; recompute and verify chart totals | Work / ASTRO-P03 |
| ACF-08 | Presentations; AC-home | Export editable deck with readable layout, notes and reproducible source assets | Work / ASTRO-P03 |
| ACF-09 | Meeting synthesis; AC-use-cases | Deduplicate decisions/actions from mixed inputs and retain source attribution | Fehrest / ASTRO-P07 |
| ACF-10 | Research reports; AC-cluster | Trace substantive claims to retrievable evidence and contradictions | Fehrest / ASTRO-K01 |
| ACF-11 | Market/filing/backtest research; AC-home | Domain research pack records dates, assumptions and reproducible calculations; no transaction execution implied | Work / ASTRO-P03 |
| ACF-12 | Content production; AC-home | Topic, headline, draft, cover brief and platform variants share one content artifact lineage | Work / ASTRO-P03 |
| ACF-13 | Content calendar/monitoring; AC-use-cases | Schedule approved drafts and measure outcomes without silently publishing | Work / ASTRO-P04 |
| ACF-14 | Pages/dashboards/internal tools; AC-home | Produce runnable artifact plus preview; qualify before publication | Work / ASTRO-P06 |
| ACF-15 | Browser collection/forms/screenshots; AC-home | Bind actions to fresh owned surface and explicit account scope | UWC / ASTRO-P05 |
| ACF-16 | Scheduled tasks and daily briefs; AC-home | Durable trigger identity, missed-run policy, budgets, pause and run evidence | Runtime / ASTRO-P04 |
| ACF-17 | Slack/Telegram/WhatsApp/Lark/Discord; AC-home | Individual connector qualification; DM/group mention routing and reply/file delivery scoped to destination | UWC / ASTRO-P04 |
| ACF-18 | WeCom and Feishu inputs; AC-use-cases | Retain regional connector candidates; no claimed support before API/rights tests | UWC / ASTRO-P04 |
| ACF-19 | Channel progress/results; AC-overview | Resume the same Work from another permitted channel without context leakage | Work / ASTRO-T02 |
| ACF-20 | Model switching; AC-models | Explicit route identity, compatibility and egress revalidation on switch | Mirefa / ASTRO-F05 |
| ACF-21 | Long-context work; AC-models | Budgeted ContextPackage with omissions and retrieval fallback, not reliance on advertised window size | Fehrest / ASTRO-F04 |
| ACF-22 | Image/video/file understanding; AC-visual | Qualified modality adapters with source-frame/page references | Mirefa / ASTRO-P03 |
| ACF-23 | Standard/cluster modes; AC-cluster | One worker then budgeted specialised topology; compare quality-adjusted cost | Edara / ASTRO-B03 |
| ACF-24 | Plan/research/review/delivery gates; AC-cluster | Stage evidence binds exact output and independent review remains separate | AGILLE/Assurance / ASTRO-F07 |
| ACF-25 | Parallel specialist roles; AC-cluster | Disjoint writable scopes and dependency-aware merge/reconciliation | Edara / ASTRO-O01 |
| ACF-26 | Progress panel; AC-cluster | Show actual task state, blockers, spend and cancellation rather than guessed progress | Work / ASTRO-O01 |
| ACF-27 | Citation/numeric/output audit; AC-cluster | Independent source, calculation and file-manifest checks | Assurance / ASTRO-P03 |
| ACF-28 | Data cleaning and event planning; AC-use-cases | Reversible transformations and linked budget/agenda/materials/contingency outputs | Work / ASTRO-P03 |
| ACF-29 | Separate personas/workspaces; AC-personas | Distinct scope, memory and sessions; prove cross-scope denial beyond UI hiding | Nawat/Work / ASTRO-T01 |
| ACF-30 | New session/clone; AC-personas | Explicit blank or selected-context fork; no ambient secrets or authority inheritance | Work / ASTRO-O02 |
| ACF-31 | Multi-channel agent memory; AC-personas | Same-agent memory only within authorized scope intersection | Fehrest / ASTRO-T02 |
| ACF-32 | Persistent preferences/corrections; AC-learning | Candidate learning has evidence, owner, approval, rollback and expiry | Fehrest / ASTRO-K02 |
| ACF-33 | Learned workflows; AC-learning | Propose versioned SkillPackage after observed success; evaluate before promotion | Mirefa / ASTRO-H01 |
| ACF-34 | Learning review cards/history; AC-learning | Accept/reject/edit/revoke; configurable rejection cooldown; show what changed | Work / ASTRO-K02 |
| ACF-35 | Behavior/fact/tool memory files; AC-learning | Map to typed scoped records; never auto-edit protected governance | Fehrest/Nawat / ASTRO-K02 |
| ACF-36 | Chat plus design canvas; AC-design | Versioned authored design with selected-object context and undo | Presentation / ASTRO-P06 |
| ACF-37 | Screenshot/asset/code/design-system input; AC-design | Track asset rights, source version and binding to generated components | Fehrest / ASTRO-P06 |
| ACF-38 | Style catalogue; AC-design | Curated original/licensed styles, searchable by use case with accessibility checks | Work / ASTRO-P06 |
| ACF-39 | Chat edits/local annotations/direct manipulation; AC-design | Concurrent edits detect version conflict; accepted change updates one artifact model | Presentation / ASTRO-P06 |
| ACF-40 | Tone/fonts/motion controls; AC-design | Global tokens propagate with contrast and reduced-motion validation | Presentation / ASTRO-P06 |
| ACF-41 | Responsive preview and zoom; AC-design | Desktop/tablet/mobile and deck views retain artifact identity | Presentation / ASTRO-P06 |
| ACF-42 | Slide/speaker presentation tools; AC-design | Notes and presentation state export without leaking private comments | Work / ASTRO-P06 |
| ACF-43 | ZIP/HTML/Markdown/PDF/PNG/PPTX export; AC-design | Format-specific round-trip/visual checks and export manifest | Work / ASTRO-P03 |
| ACF-44 | Figma layered export; AC-design-release | Optional connector preserves supported layers; disclose losses, no false editable export | UWC / ASTRO-P06 |
| ACF-45 | Multi-screen design consistency; AC-design-release | Shared components/tokens plus flow coverage across screens | Assurance / ASTRO-P06 |
| ACF-46 | Visual office-output revision; AC-visual | Render, detect clipping/overlap and verify amended artifact | Assurance / ASTRO-P03 |
| ACF-47 | Cloudflare/Vercel connectors; AC-changes | Preview and deployment are distinct grants with rollback/receipt evidence | UWC / ASTRO-P04 |
| ACF-48 | Consumption detail; AC-changes | Attribute token/cost estimates and billed usage by route, task and Team | Work/Byan / ASTRO-T03 |
| ACF-49 | Pin/rename/delete conversations; AC-changes | Stable IDs, reversible presentation changes and explicit retention semantics | Work / ASTRO-O02 |
| ACF-50 | Inbox/notifications; AC-changes | Meaningful completion/blocker alerts, read/unread and mute preferences | Work / ASTRO-O02 |
| ACF-51 | Multilingual operation; AC-changes | Localized UI and mixed-language artifacts; this planning package remains English | Presentation / ASTRO-P02 |
| ACF-52 | Keep-awake while running; AC-changes | Scoped user-visible power request released on finish/crash; battery policy honored | Runtime / ASTRO-P02 |
| ACF-53 | Streaming/reconnect reliability; AC-changes | Bounded event replay, gap markers and no duplicate effects after reconnect | Runtime / ASTRO-O02 |
| ACF-54 | Check-in/rewards/events; AC-changes | Optional entitlement/promotion module, transparent accounting, no effect-authority benefit | Work / ASTRO-T03 |
| ACF-55 | Third-party API configuration; terms | Credential references and provider-specific cost/privacy displayed; never infer key ownership from login | Mirefa/Nawat / ASTRO-F06 |
| ACF-56 | Stop and high-risk confirmation; terms | Cancellation result and proposal-bound confirmation; neither blanket future approval nor rollback claim | Runtime/Nawat / ASTRO-F06 |
| ACF-57 | Account/history deletion; privacy | Deletion, legal hold, export and retention verified across payload/index/backups | Nawat/Fehrest / ASTRO-T04 |

[AutoClaw privacy](https://autoclaw.z.ai/privacy/md2html/?favicon=autoglm&md=autoclaw_privacy) describes service-side processing, retention and possible international transfers; its overview's broad local-privacy wording therefore is not evidence of zero egress. [Terms](https://autoclaw.z.ai/privacy/md2html/?favicon=autoglm&md=autoclaw_agreement) describe third-party keys and restrictions on software/content use. No AutoClaw core-source license or complete public binary-to-source mapping was established. Treat it as a product reference; any source reuse needs a specific accessible artifact and rights basis. Its OpenClaw lineage does not establish rights to AutoClaw-specific additions.

## Orca: priority agent-workspace profile

The [pinned Orca README](https://github.com/stablyai/orca/blob/b5b727bddbdd34c31801fb125d43eb818cf84a76/README.md) documents parallel worktrees, terminals, visual design targeting, provider integrations, SSH, diff annotation, rich previews, CLI control, account usage and mobile steering. These are documented features; WePLD qualification is separate.

| ID | Planned parity | WePLD acceptance / task |
|---|---|---|
| ORC-01 | Multiple CLI workers and subscriptions | Qualified per-route adapters; no sharing credentials across principals; ASTRO-O01 |
| ORC-02 | Prompt fan-out and isolated worktrees | Fixed comparison budget, independent branches, explicit selection and conflict review; worktrees do not sandbox processes; ASTRO-O01 |
| ORC-03 | Terminal splits, rendering and persisted scrollback | Bounded retention, replay gaps, secret redaction, resize/cancel/exit tests; ASTRO-O02 |
| ORC-04 | Chromium element selection with DOM/CSS/crop | Fresh surface/version and minimal captured scope; ASTRO-P05/P06 |
| ORC-05 | GitHub/Linear tasks and project boards | Versioned external observations, issue-to-worktree flow and conflict handling; ASTRO-O01 |
| ORC-06 | Inline diff comments, edit and commit | Comments bind base/head/side/line; edit/commit are new authorized effects; ASTRO-R02 |
| ORC-07 | Editor, file/image context and previews | Autosave conflict handling, safe rendering and content provenance; ASTRO-O02 |
| ORC-08 | Quick-open across projects/files/tasks | Access-filtered search with source freshness; ASTRO-O02 |
| ORC-09 | SSH workspaces, reconnect, port forwarding | Explicit host key, destination and port grants; no scope fallback after reconnect; ASTRO-O03 |
| ORC-10 | Mobile monitoring, notifications, follow-ups | Device enrollment/revocation and delegated scope; lost phone cannot mint host authority; ASTRO-O03 |
| ORC-11 | CLI automation and computer interaction | Same contracts as UI; command availability does not expand effects; ASTRO-P05 |
| ORC-12 | Account switching, rate limits, unread state | Route/approval invalidation and attributed usage; ASTRO-O02/T03 |

Source mechanisms worth mining include negotiated remote capabilities and explicit missing/null states, plugin worker/log lifetime tests, stale worktree registration handling and bounded fingerprint reconciliation. None establishes that an upstream isolation boundary meets WePLD's threat model.

## Other requested sources: capability traceability

Each row defines a proposed WePLD capability, not a promise that upstream supplies all of its acceptance controls.

| ID / source | Capabilities carried into WePLD | Owner / task / decisive acceptance |
|---|---|---|
| EXT-01 [Vane](https://github.com/ItzCrazyKns/Vane) | Research depth modes, web/discussion/academic search, domain filters, citations, file questions, visual search, suggestions, history, discovery and lookup cards | Fehrest / ASTRO-K01; answer citation coverage and bounded crawl; local models do not make internet queries private by default |
| EXT-02 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | Plugin/service composition, provider adapters, durable session and streaming UI, context/tool loading | Runtime/UWC / ASTRO-A05/F05; unload/restart safety and no donor-owned authority |
| EXT-03 [Dreambeans](https://labs.google/dreambeans) | Opt-in connected-source daily briefs, tuning feedback/history, notifications, illustrations, actionable cards and deletion | Work/Fehrest / ASTRO-P04/K02; team briefs exclude private sources; feedback changes future recommendations, not historical evidence |
| EXT-04 [Cline Desktop](https://cline.bot/desktop) | Standalone workspace, BYO provider, editable/reorderable queued prompts, session forks/checkpoints, cross-client history/favorites | Work / ASTRO-O02; fork preserves predecessor and never silently rewinds shared/external state |
| EXT-05 [TrueForge](https://github.com/truefoundry/trueforge) | Model/tool/skill catalogues, MCP OAuth, approvals, deferred loading/compaction, sandbox adapters, SDK/UI and schedules | UWC/Runtime / ASTRO-A05/F05/H01; tenant-aware session deletion and cancellation conformance |
| EXT-06 [Alibaba Open Code Review](https://github.com/alibaba/open-code-review) | Diff and whole-file review, contextual tools, structured line findings, coverage/budget signals | Assurance / ASTRO-R01; no unseen file declared reviewed; precise location and false-positive tests |
| EXT-07 [Vercel OpenReview](https://github.com/vercel-labs/openreview) | On-demand PR entry, inline suggestions, resumable review and skill loading | Assurance / ASTRO-R02; WePLD separates review from writable fix/push; rights artifact still needed for direct copying |
| EXT-08 [Continue](https://github.com/continuedev/continue) | CLI/IDE adapter patterns and configurable model/tool context | UWC/Assurance / ASTRO-R01; maintained alternative or owned fork budget required; not a current managed-review guarantee |
| EXT-09 [PR-Agent](https://github.com/The-PR-Agent/pr-agent) | Review/describe/improve/ask profiles, diff compression and provider adapters | Assurance / ASTRO-R01; missing compressed context remains declared; disabled upstream functions not silently enabled |
| EXT-10 [Qodo organization](https://github.com/qodo-ai) | Review/context/test-generation candidates, separately selected per repository or hosted product | Assurance / ASTRO-A07; an organization URL is not one codebase/license; PR-Agent and Qodo commercial service remain distinct |
| EXT-11 [Review-tools directory](https://github.com/kodustech/awesome-code-review-tools) | Capability comparison and acquisition cross-check | Acquisition / ASTRO-A07; directory entries are discovery evidence, not imported engines |
| EXT-12 [TestSprite CLI](https://github.com/TestSprite/testsprite-cli) | Test plan generation/acceptance, run/rerun/cancel, environment sets, failure bundle, flaky testing, run comparison, schedules and reports | Assurance / ASTRO-Q01/Q02; hosted/tunnel egress disclosed; “detached” is not “cancelled” |
| EXT-13 [Momentic](https://momentic.ai/blog/how-agentic-testing-works) | Intent-based browser testing, cached locators, re-resolution, traces and agent-driven test management | Assurance / ASTRO-Q02; healed locator cannot change assertion or hide a real regression; hosted core source unestablished |
| EXT-14 [Playwright](https://github.com/microsoft/playwright) | Browser contexts, web/API tests, retries, trace/debug artifacts and cross-browser qualification | Assurance / ASTRO-Q02; pin engine/browser/tool versions; no production target by default |
| EXT-15 [TeamAI](https://github.com/Tencent/teamai-cli) | Team skills/rules/agents/MCP distribution, shared learning/wiki, session/digest/dashboard practices | Work/Mirefa / ASTRO-T02/H02; updates versioned and screened, no automatic privilege expansion |
| EXT-16 [Archify](https://github.com/tt-a1i/archify) | Typed diagram IR, deterministic render, before/delta/after, source links, tracing and portable exports | Fehrest.Maemar / ASTRO-P06; source-verified edges distinguished from authored hypotheses |
| EXT-17 [Cloudflare security audit skill](https://github.com/cloudflare/security-audit-skill) | Coverage ledger, hunting/validation separation, structured findings and independent record checks | AMAN/Assurance / ASTRO-S01; unmet validation stays unresolved; no arbitrary target execution |
| EXT-18 [GitHub testing collection](https://github.com/collections/opensource-testing) | Runner category coverage cross-check | Acquisition / ASTRO-A07; select concrete libraries per need, no bulk installation |
| EXT-19 [ADK live agents](https://adk.dev/live/) | Two-way voice/video/text, interruption, session resumption, live tools, voice/turn configuration and live evaluation | UWC / ASTRO-P08; interruption fences pending effects; media capture/retention and tools scoped separately |
| EXT-20 [TypeSafe](https://docs.typesafe.ai/introduction) | Typed choice, rubric score and truth-likelihood questions, distributions/confidence, independent batched questions, composable threshold routing | Mirefa/Assurance / ASTRO-K03; calibrated on held-out WePLD data, abstain on uncertainty; confidence never authorizes effects |
| EXT-21 [Memanto](https://memanto.ai) | Namespace memory, remember/recall/answer, provenance/freshness/conflict handling, categories, temporal queries, local/cloud backends, CLI/dashboard/MCP and Markdown export | Fehrest / ASTRO-K02; deletion and cross-scope negatives, portability and measured retrieval quality; no unverified latency/compression promises |
| EXT-22 [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) | Markdown/frontmatter bundles, links/index/log, source/verification/freshness fields, portable visualization and attested-computation descriptions | Fehrest / ASTRO-K02; loss report and scope-preserving round trip; imported verification is an external claim, executable descriptions are inert |

Dreambeans is documented as a personal Google-account experiment, not an enterprise collaboration engine. ADK live is documented as experimental and currently backed by Gemini Live. TypeSafe's advertised speed/cost comparisons and Memanto's benchmark/zero-egress claims require independent profile-specific validation. These limitations constrain acquisition, not the founder's requested capability backlog.

TypeSafe's [quickstart](https://docs.typesafe.ai/introduction/quickstart) also supplies a playground, authenticated API, Python SDK and an agent-skill entry point. Preserve response model identity and token usage. Its [confidence documentation](https://docs.typesafe.ai/confidence) distinguishes Choice/Score distributions from Noul, which has no confidence property. The [pattern index](https://docs.typesafe.ai/patterns) covers speculative fan-out, confidence routing, composite scoring and intent routing. ASTRO-K03 maps each to typed, budgeted consumers with calibrated abstention; a concentrated distribution is not proof of accuracy. SDK/skill source rights and pins are separate from access to model weights or the service internals.

Qodo's selected public components are pinned in the inventory. Qodo Cover supplies test-generation/coverage ideas but its README says maintenance ended; Open Aware exposes public-repository context/research interfaces, while private enterprise indexing is a distinct product. The agents repository provides workflow examples; qodo-skills provides local review, PR-review resolution, codebase guidance and optional standards packages. ASTRO-A07/R01/Q01/H01 preserve these distinctions and require a maintenance plan before adopting abandoned code.

## AnythingLLM completeness profile

Sources: [repository](https://github.com/Mintplex-Labs/anything-llm/blob/da6685510ce691b2e1be417f739c7dffee3cfc49/README.md), [feature index](https://docs.anythingllm.com/features/all-features), [meeting](https://docs.anythingllm.com/meeting-assistant/introduction), [scheduling](https://docs.anythingllm.com/scheduled-jobs/overview), [desktop assistant](https://docs.anythingllm.com/desktop-assistant/features), [dictation](https://docs.anythingllm.com/pro/magic-echo), [selection assistant](https://docs.anythingllm.com/pro/magic-beacon), [completion assistant](https://docs.anythingllm.com/pro/magic-tab). Feature labels below summarize documentation; controls are proposed WePLD requirements.

| ID | Capability inventory | WePLD acceptance / owner / task |
|---|---|---|
| ALL-01 | Document chat, attachment/RAG modes, uploads, citations, collections | Distinguish attached context from indexed generations; access-filter retrieval / Fehrest / ASTRO-K01 |
| ALL-02 | Local/cloud language, embedding, speech and vector providers; multimodal input; model routing | Pin route and capability; explicit data destination, no silent fallback / Mirefa / ASTRO-F05/K03 |
| ALL-03 | Chat/event logs, workspace history, appearance, shortcuts, prompt variables | Safe variable expansion, retention and keyboard access / Work / ASTRO-O02 |
| ALL-04 | Agents, surveys, custom skills, MCP, intelligent tool selection | Deferred discovery within admitted capabilities; missing tool cannot become invented success / UWC / ASTRO-H01 |
| ALL-05 | No-code agent flows: scrape, API, model, file read/write | Compile to same qualified task/effect graph; step preview and bounded failure / AGILLE / ASTRO-P04 |
| ALL-06 | Web search, scraping, browser extension and private browser | Source snapshots, domain budgets, SSRF/DNS/redirect checks, credential-scope isolation / Runtime / ASTRO-K01/P05 |
| ALL-07 | Document listing/summarizing/generation, charts, SQL and filesystem tools | Read-only SQL first; per-effect approval for mutations; factual and artifact checks / Work / ASTRO-P03 |
| ALL-08 | Gmail/Calendar/Outlook, Telegram | Per-account access and explicit destination; calendar event/message is a separate effect / UWC / ASTRO-P04 |
| ALL-09 | Recurring jobs, cron builder, limits, run history and continuation | Timezone/DST/missed-run/overlap semantics, replay-safe trigger and revocation / Runtime / ASTRO-P04 |
| ALL-10 | Auto/manual memory and personalization | Evidence-backed proposed memory, edits/deletion/export and scoped use / Fehrest / ASTRO-K02 |
| ALL-11 | Multi-user permissioning, API keys, embedded chat, self-host/cloud/mobile profiles | Scoped APIs/widgets and authenticated tenant boundary; separate deployment qualification / Nawat / ASTRO-T01/T04 |
| ALL-12 | Community import/upload of skills, flows, prompts and commands | Versioned manifest, publisher provenance, quarantine and workspace admission / Mirefa / ASTRO-H02 |
| ALL-13 | Meeting capture/import, transcription, speakers, summaries, search/chat and follow-ups | Recording consent, correction lineage, local/cloud disclosure, action proposals / Work / ASTRO-P07 |
| ALL-14 | Meeting detection/reminders and custom summary prompts | No ambient recording; notification alone cannot start capture / Work / ASTRO-P07 |
| ALL-15 | App/window/area capture assistant | User-selected fresh scope; sensitive app exclusion; capture does not grant input / UWC / ASTRO-P05 |
| ALL-16 | Dictation, quick/extended modes, vocabulary, transcript history and voice commands | Preview destination; clear listening indicator, focus-change refusal and retention / UWC / ASTRO-P08 |
| ALL-17 | Selected-text revise/research/translate/ask actions | Preserve original text, undo, app exclusion and explicit insert action / Work / ASTRO-P05 |
| ALL-18 | Inline completion, on-focus suggestions, chaining, personalization and delay controls | User acceptance binds fresh field state; no password/secure-desktop capture / UWC / ASTRO-P05 |
| ALL-19 | Image generation, speech output, transcription and custom model import | Qualified model artifact/license/format, no remote-code trust by default / Mirefa / ASTRO-P03/P08 |
| ALL-20 | Live document sync and computer-use previews; Open Computer direction | Treat preview as preview; reconcile deletions/access revocation and sandbox actual effects / Runtime / ASTRO-P05/K02 |
| ALL-21 | Pro/free entitlement and subscription management | Optional transparent entitlement accounting; core local authority unaffected / Work / ASTRO-T03 |

Some AnythingLLM features are desktop-only or Docker-only. Its meeting documentation says cloud summarization sends the transcript; local recording does not imply zero egress. Scheduling's documented single-user restriction is a donor limitation: WePLD's team schedules require explicit membership/ownership/revocation tests. Public source availability for a server or collector does not prove every desktop/Pro feature has matching reusable source. ASTRO-P01 records the edition/source matrix before parity acceptance.

## Teams and enterprise collaboration

**Teams** appears at workspace level. Users create/join a Team, choose a project, collaborate on Work/rooms, assign bounded tasks, review changes, run assurance and share qualified capabilities. Organization administration is a separate view for identity, policy, billing/quotas, data handling and audit. Team membership does not confer access to every project or personal memory.

| ID | Requirement | Concrete acceptance / task |
|---|---|---|
| TEAM-01 | Organizations, Teams, projects and guests | Resource-scoped membership, explicit owner/admin/member/reviewer/guest/custom roles; deny cross-tenant IDs / ASTRO-T01 |
| TEAM-02 | Shared Work/rooms, comments, mentions and files | Permission check on subscription, replay, export and search; no notification metadata leak / ASTRO-T02 |
| TEAM-03 | Collaborative build/edit | Presence and draft co-editing separated from execution ownership; CAS conflicts and per-file/worktree ownership; no lost updates / ASTRO-T02 |
| TEAM-04 | Shared agents and reusable policies | Versioned profile with scoped secrets, quotas and individual acting principal; no shared human credentials / ASTRO-T01/T03 |
| TEAM-05 | Team Review/Test/Security | Required profiles, independent assignments, routing/escalation and finding ownership; reviewer cannot accept own critical work / ASTRO-R02/T02 |
| TEAM-06 | Team knowledge, wiki and approved learning | Personal/team/project namespaces, promotion review, lineage and revocation of derived access / ASTRO-K02/T02 |
| TEAM-07 | SSO/OIDC/SAML and provisioning/SCIM | Group mapping, deprovisioning, break-glass audit and short-lived host leases; qualified identity adapter / ASTRO-T04 |
| TEAM-08 | Budgets, chargeback, usage and limits | Atomic reservations across concurrent tasks; caps refuse or request new allocation; estimate vs billed distinction / ASTRO-T03 |
| TEAM-09 | Private registry and trusted rollout | Admin allowlist, staged versions, signed mirror, air-gap bundle, revocation and rollback / ASTRO-H02/T04 |
| TEAM-10 | Residency, retention, hold, deletion and export | Profile-specific policy and restore drill; legal hold visibly blocks incompatible deletion / ASTRO-T04 |
| TEAM-11 | Enterprise operations | Audit export, health metrics, backup/restore, upgrade compatibility, key rotation and incident runbook / ASTRO-T04 |
| TEAM-12 | Disconnected and remote work | Declared offline ceiling; reconnection fences stale owner and reconciles unsent/unknown effects / ASTRO-O03/T04 |

## Community Hub

**Hub** provides Plugins, Tools, MCP servers, Skills, Agent Profiles, Workflow Templates and Evaluation Packs. Browse/search/filter by capability, platform, license, version, cost, provider, maintenance and trust evidence. Each detail page shows publisher, immutable source digest, permission diff, dependencies, network destinations, data handling, compatibility, tests, known limitations and changelog. Ratings describe usefulness; they do not replace qualification.

ASTRO-H01/H02 implement this lifecycle: draft → publisher checks → package validation → isolated conformance → moderation → signed catalogue entry → user/org selection → workspace admission → invocation grant → versioned update → revoke/uninstall. Install preview states exactly what files/configuration will change. Updates are pinned and require new admission for expanded permissions. Uninstall stops owned processes, revokes credentials, removes only owned files and explains retained user data. Reinstallation uses a new generation so stale callbacks cannot act on it.

Public/private/unlisted distribution, organization mirrors, vulnerability reporting, quarantine/takedown, provenance attestations, publisher-key rotation, offline export/import and dependency conflicts are first-class. Malware scanning is evidence with limits. No hub package may edit core policy, inherit ambient secrets or auto-execute its own installer during discovery. Preserve license/NOTICE and custom permission records. A reviewed package can still be refused by a workspace's scope or platform policy.

## Skills as product features, including debate

The exact pinned Matt Pocock inventory is enumerated in [source inventory](SOURCE_INVENTORY.md#matt-pocock-feature-adaptation-catalogue). All 38 SKILL.md paths receive a disposition, including in-progress content. They become small selectable Work/AGILLE/Mirefa feature packs, not mandatory prompts copied into every session. ASTRO-SK01 handles source adaptation; ASTRO-SK02 adds conformance and user-facing flows.

**Debate / Challenge a plan** is an explicit founder-requested WePLD feature. No literal `debate` skill was found among the 38 pinned paths. The design draws on grilling, domain modeling, research, architecture critique and standards/spec review without attributing an invented upstream feature. A user selects a proposal, constraints and budget; independent advocate/critic roles produce sourced claims and counterexamples; a synthesizer preserves disagreement, falsifiable experiments and decision options. The user may accept a decision or request an experiment. Voting and debate consensus never create grants or acceptance. Stop at the budget or when no new supported counterexample appears; measure decision quality and cost against a single reviewer.

Improve donor workflows with bounded questions, reusable glossaries/ADRs, source citations, structured outputs, accessibility, interruption/resume, explicit publication permission and exact-target tests. A skill's instructions cannot override the project constitution or silently publish issues, reset a workspace, install hooks or run arbitrary commands.
