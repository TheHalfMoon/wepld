# Source Acquisition — IssueOps / Workflow Skills / Delegation / Web Agents

```text
STATUS = RESEARCH_INPUT_ONLY
CANONICAL_REGISTRY_COUNT = 402
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION_AUTHORITY = NONE
```

The canonical source registry does not currently admit the newly studied donor/protocol candidates below. This document records them as future source-acquisition candidates only. A separately governed registry revision is required before any admission/import.

## Candidate A — mattpocock/skills

```text
REPOSITORY = mattpocock/skills
PINNED_REVISION = 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76
LICENSE_OBSERVED = MIT
ROLE_CANDIDATE = BEHAVIOR_ORACLE + WORKFLOW_DESIGN_QUARRY + TEST/NEGATIVE_ORACLE_CANDIDATE
SOURCE_ADMISSION = NONE
```

### Studied skill inventory

Stable engineering:

1. `ask-matt`
2. `code-review`
3. `codebase-design`
4. `diagnosing-bugs`
5. `domain-modeling`
6. `grill-with-docs`
7. `implement`
8. `improve-codebase-architecture`
9. `prototype`
10. `research`
11. `resolving-merge-conflicts`
12. `setup-matt-pocock-skills`
13. `tdd`
14. `to-spec`
15. `to-tickets`
16. `triage`
17. `wayfinder`
18. `wizard`

Stable productivity:

19. `grill-me`
20. `grilling`
21. `handoff`
22. `teach`
23. `to-questionnaire`
24. `wait-what`
25. `writing-for-agents`

In-progress:

26. `claude-handoff`
27. `implement-spec`
28. `loop-me`
29. `retro`
30. `setup-ts-deep-modules`
31. `writing-beats`
32. `writing-fragments`
33. `writing-shape`

Miscellaneous:

34. `git-guardrails-claude-code`
35. `migrate-to-shoehorn`
36. `scaffold-exercises`
37. `setup-pre-commit`

### WePLD adaptation plan

| Donor behavior | WePLD-native destination |
|---|---|
| ask-matt | `/askme` workflow router |
| wait-what | `/btw` context-aware re-explanation |
| triage | `/triage` + `/issues` Case triage |
| grilling / grill-me / grill-with-docs | `/grill` + internal decision-tree primitive |
| codebase-design / domain-modeling / improve-codebase-architecture | `/architect` + internal architecture/domain primitives |
| to-spec | `/spec` |
| to-tickets | `/tickets` tracer-bullet/dependency planner |
| implement / tdd | `/build` + internal TDD primitive |
| diagnosing-bugs | `/debug` feedback-loop-first diagnosis |
| code-review | `/review` with standards/spec axes |
| prototype | `/prototype` |
| research | `/research` |
| wayfinder | `/wayfinder` |
| handoff / claude-handoff | provider-neutral `/handoff`; never Claude-owned architecture |
| teach / scaffold-exercises | `/teach` + learning assets |
| to-questionnaire | `/questionnaire` |
| wizard | `/wizard` |
| loop-me | `/workflow` recurring/checkpointed workflow |
| retro | `/retro` |
| implement-spec | Edara/Mission Runtime task-graph orchestration, not a second build command |
| writing-for-agents | internal bounded-context packaging primitive |
| writing-beats/fragments/shape | future writing capability; not three mandatory commands |
| setup-ts-deep-modules | language-neutral `/architect` boundary qualification |
| resolving-merge-conflicts | intent-preserving reconciliation primitive subject to WePLD Git policy |
| git-guardrails-claude-code | Nawat effect policy/guardrails, provider-neutral |
| setup-pre-commit | optional repository qualification pattern, not mandatory dependency |
| migrate-to-shoehorn | generic migration workflow pattern only |
| setup-matt-pocock-skills | inspiration for WePLD workflow setup/triage conventions; no donor branding |

### Important incompatibilities/rejections

- Donor instructions that imply rebase/history rewriting MUST NOT override WePLD repository policy.
- Provider-specific background execution MUST become governed Mission Runtime work.
- Donor branding MUST NOT define user-facing WePLD product language.
- Skill prose is not authority and is not copied wholesale merely because the license permits reuse.

## Candidate B — amElnagdy/delegate-skills

```text
REPOSITORY = amElnagdy/delegate-skills
PINNED_REVISION = b781ee2e23089630e2fbee1cfd6174afe4edeb76
LICENSE_OBSERVED = MIT
ROLE_CANDIDATE = WORKER_ADAPTER_BEHAVIOR_ORACLE + DELEGATION_PROTOCOL_QUARRY + FAILURE_MODE_QUARRY
SOURCE_ADMISSION = NONE
```

### Studied skill inventory

1. `delegate-setup`
2. `agy`
3. `aider`
4. `claude`
5. `cline`
6. `codex`
7. `commandcode`
8. `copilot`
9. `cursor`
10. `grok`
11. `kimi`
12. `omp`
13. `opencode`
14. `pi`
15. `qoder`
16. `vibe`
17. `warp`
18. `zcode`

Shared behavior studied includes fleet schema, dispatch pattern, brief construction, CLI delegate protocol, queue/poll behavior, and review/land flow.

### WePLD adaptation plan

Do not expose one `/delegate-*` command per provider. Normalize all qualified providers behind:

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
```

Required adapter facts:

- stable WePLD `worker_id`;
- opaque provider identity/session identifiers;
- capability descriptor;
- effect classes;
- enforceable vs advisory read-only/containment semantics;
- process/session lifecycle;
- structured event/result normalization;
- cancellation/recovery behavior;
- cost/quota/metering classification;
- provider/model identity;
- version/provenance;
- known unsafe/full-trust modes;
- qualification evidence and expiry.

### Security finding from cross-provider study

Provider flags are not semantically equivalent. Some workers offer enforceable sandbox modes; others expose advisory “read-only” behavior or full-trust/yolo modes. Therefore:

```text
PROVIDER_READONLY_FLAG != WEPLD_CONTAINMENT
PROVIDER_PERMISSION != NAWAT_GRANT
PROVIDER_SESSION_ID != TRUST
```

WePLD must qualify containment and effect behavior independently.

## Candidate C — WebMCP / webmachinelearning/webmcp

```text
UPSTREAM = W3C Web Machine Learning Community Group WebMCP draft
OFFICIAL_SPEC = https://webmachinelearning.github.io/webmcp/
UPSTREAM_REPOSITORY = webmachinelearning/webmcp
OBSERVED_ON = 2026-08-31
STATUS_OBSERVED = COMMUNITY_GROUP_DRAFT / NOT_W3C_STANDARD / NOT_STANDARDS_TRACK
EDITORS_OBSERVED = MICROSOFT + GOOGLE
ROLE_CANDIDATE = PROTOCOL_SPECIFICATION_ORACLE + TEST_ORACLE + BROWSER_TOOL_INTEROP_CANDIDATE
SOURCE_ADMISSION = NONE
```

Observed capability themes:

- JavaScript-based web-application tools exposed to agents;
- imperative tool registration;
- declarative HTML-form-oriented tool exposure;
- structured input schemas;
- tool annotations including advisory read-only/untrusted-content signals;
- origin/exposure semantics;
- Permissions Policy integration;
- security/privacy sections covering prompt injection, tool poisoning, output injection, intent misrepresentation, privacy leakage, and same-origin risks;
- Web Platform Tests as a future conformance/test oracle candidate.

WePLD adaptation:

```text
website WebMCP tool
-> untrusted WebToolObservation
-> independent effect classification
-> Mirefa qualification
-> Nawat exact-context grant/revalidation
-> qualified browser/UWC adapter
-> evidence
```

WebMCP metadata, annotations, tool availability, and tool output MUST NOT become WePLD authority.

## Candidate D — Chrome WebMCP implementation/docs

```text
UPSTREAM = Chrome for Developers / Chromium WebMCP implementation surface
OFFICIAL_DOCS = https://developer.chrome.com/docs/ai/webmcp
OBSERVED_ON = 2026-08-31
ROLE_CANDIDATE = IMPLEMENTATION_BEHAVIOR_ORACLE + COMPATIBILITY_ORACLE + FIXTURE/TEST_QUARRY
SOURCE_ADMISSION = NONE
```

Observed implementation themes include imperative/declarative APIs, origin-isolation requirements, `tools` Permissions Policy, current experimental/origin-trial behavior, local testing flags, tool inspector behavior, and browser-context requirements.

Current browser support MUST be reverified at the owning acquisition gate; no planning-time browser/version statement is frozen as implementation truth.

## Candidate E — Chrome DevTools MCP / Microsoft Edge + WebView2 compatibility

```text
UPSTREAM = Chrome DevTools for agents / chrome-devtools-mcp
MICROSOFT_REFERENCE = Microsoft Edge DevTools MCP guidance
MICROSOFT_DOCS = https://learn.microsoft.com/en-us/microsoft-edge/web-platform/devtools-mcp-server
OBSERVED_ON = 2026-08-31
ROLE_CANDIDATE = BROWSER_DIAGNOSTICS_ADAPTER + DEVTOOLS_BEHAVIOR_ORACLE + EDGE_WEBVIEW2_COMPATIBILITY_ORACLE
SOURCE_ADMISSION = NONE
```

Observed capability themes:

- agent-driven inspection/control of Chromium-based browsers;
- Edge compatibility;
- WebView2 compatibility;
- DOM/page inspection;
- debugging and performance analysis;
- browser target/session connection semantics;
- browser-profile/user-data-directory implications;
- underlying DevTools/Puppeteer implementation behavior.

This candidate is distinct from WebMCP. WebMCP exposes application-defined structured tools; DevTools MCP exposes browser inspection/control. WePLD should support both behind different capability/effect classifications.

## Web-agent security acquisition requirements

Any future browser/WebMCP source acquisition MUST explicitly qualify:

- browser session/profile identity;
- origin and page/tool generation freshness;
- authenticated-session ambient authority;
- cookies/password-manager/autofill/SSO handling;
- WebMCP tool poisoning and output injection;
- advisory annotations vs independently verified effect classes;
- cross-origin iframe/tool exposure;
- tool-definition mutation after discovery;
- duplicate/non-idempotent invocation;
- browser navigation and origin changes;
- download/upload semantics;
- local vs remote browser boundaries;
- headless vs visible-session behavior;
- fallback behavior among WebMCP, DOM automation, DevTools, local browser, remote browser, Chrome, Edge, and WebView2;
- data capture/egress from console/network/DOM/screenshots;
- Windows-first portability and containment.

## Future acquisition sequence

1. Create a separately governed next source-registry revision candidate.
2. Add only the candidates needed by the owning tranche with exact revisions/versions/source hashes where applicable.
3. Mine only the paths needed by the owning slice.
4. Extract tests, fixtures, behavior contracts, negative oracles, and security/containment differences.
5. Compare against already-admitted sources to avoid duplicate machinery.
6. Decide reuse mode independently per capability:
   - reject;
   - specification oracle;
   - behavior oracle only;
   - test/fixture acquisition;
   - documentation/process pattern;
   - bounded source reuse;
   - protocol/adapter candidate.
7. Run applicable license/security/dependency/portability/maintenance/exit qualification.
8. Admit only through the owning future slice; never through this planning candidate.

## Additional source classes to qualify later

IssueOps, RAG, and web-agent interoperability will require capability-triggered acquisition rather than broad discovery. Candidate categories include:

- GitHub API/App/webhook/reference implementations and fixtures;
- GitLab/Linear/Jira/Azure DevOps/Sentry API contracts when their adapter is actually activated;
- terminal bracketed-paste/path escaping behavior or reusable libraries;
- PDF/document/structured-data parsers and adversarial corpora;
- lexical/full-text retrieval engines;
- optional vector/embedding/index engines only if S4 evidence proves the need;
- code semantic-index/graph sources already contemplated by Fehrest;
- browser/WebMCP/DevTools protocol fixtures and adversarial corpora;
- retry/idempotency/checkpoint libraries or patterns only when stdlib/admitted machinery is insufficient.

No category listing is source admission.
