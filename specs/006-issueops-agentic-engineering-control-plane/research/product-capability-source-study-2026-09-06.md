# Product Capability Tracks — Source and Mechanism Study — 2026-09-06

```text
STATUS = FUTURE_PLANNING_RESEARCH
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = NONE
NETWORK_AUTHORITY = NONE
```

Purpose: classify mechanisms that may make Projects, Work, Automations/Connections, Browser/WebMCP, and Computer Use faster or stronger to build later. This study extracts mechanisms, not brands.

```text
PRODUCT CLAIM != SOURCE-CODE FACT
DOCUMENTATION FACT != SOURCE ADMISSION
LICENSE_AVAILABLE != SOURCE_ADMISSION
PUBLIC_REPOSITORY != ADMITTED_DEPENDENCY
```

## 1. Activepieces

```text
UPSTREAM = activepieces/activepieces
RESEARCH_REVISION_OBSERVED = e281f65f5f2cfa7a37d98ed4f572e9769f8f6f68
LICENSE_OBSERVED = MIT for community code outside separately licensed enterprise paths
CLASSIFICATION = BOUNDED_SOURCE_CANDIDATE + BEHAVIOR_ORACLE
SOURCE_ADMISSION = NONE
```

High-value mechanisms:

- typed integration/piece model;
- explicit auth/action/trigger construction;
- polling/webhook trigger patterns;
- versioned integration packages;
- examples suitable for schema/SDK negative-oracle mining;
- community integration ecosystem useful for connector-contract coverage.

Recommended use: inspect narrowly selected framework and representative integration paths at the owning source-acquisition gate. Do not import the full platform.

## 2. Zapier Platform

```text
UPSTREAM = zapier/zapier-platform
RESEARCH_REVISION_OBSERVED = 1cdff93f03711b4dc21c1424d8bc530c6afed888
LICENSE_OBSERVED = repository use subject to Zapier Platform Agreement
CLASSIFICATION = SPEC_ORACLE + BEHAVIOR_ORACLE + CLEAN_ROOM_REIMPLEMENT
SOURCE_ADMISSION = NONE
```

High-value mechanisms:

- schema/core/CLI separation;
- JSON-Schema-driven integration structure;
- functional constraints beyond JSON Schema;
- examples and anti-examples as first-class validation inputs;
- generated docs/types from schema truth;
- mediated request/runtime behavior and auth/request hooks.

Recommended use: specification/behavior oracle. Do not assume source reuse rights from public visibility.

## 3. n8n

```text
UPSTREAM = n8n-io/n8n
RESEARCH_REVISION_OBSERVED = 33eb5c196e0ce3a2c71525929a4ef861cb94b168
LICENSE_OBSERVED = Sustainable Use License with separately licensed enterprise paths
CLASSIFICATION = BEHAVIOR_ORACLE + SECURITY_ORACLE + FAILURE_ORACLE + CLEAN_ROOM_REIMPLEMENT
SOURCE_ADMISSION = NONE
```

High-value mechanisms:

- main/worker/queue execution behavior;
- webhook lifecycle;
- execution lifecycle and pub/sub behavior;
- credential handling across workers;
- concurrency/scaling failure cases;
- MCP/integration surfaces;
- recovery and operational edge cases from a mature automation system.

Recommended use: mine behavior/failure/security semantics, not architecture authority and not broad code import.

## 4. Make

```text
SOURCE_CLASS = PRODUCT_DOCUMENTATION
CLASSIFICATION = SPEC_ORACLE + UX_ORACLE + FAILURE_ORACLE
SOURCE_ADMISSION = NOT_APPLICABLE_TO_PRODUCT_DOCS
```

High-value mechanisms:

- Action/Search/Trigger/instant-webhook module taxonomy;
- dynamic input/output interface UX;
- connection setup patterns;
- incomplete execution/error semantics;
- rate-limit handling as a distinct condition rather than generic failure.

Recommended use: product/spec behavior oracle only.

## 5. Nango

```text
SOURCE_CLASS = INTEGRATION_AUTH_INFRASTRUCTURE_CANDIDATE
LICENSE_OBSERVED_IN_RESEARCH = Elastic License family at the observed product/repository state
CLASSIFICATION = DEPENDENCY_CANDIDATE + BEHAVIOR_ORACLE
DEPENDENCY_ADMISSION = NONE
```

High-value mechanisms:

- OAuth/token refresh;
- multi-tenant connection management;
- integration actions/sync/webhooks;
- reducing bespoke auth-refresh code.

Recommended use: evaluate buy-vs-build at the Connection/Credential broker gate. License/deployment/exit strategy require fresh verification before any dependency decision.

## 6. Trigger.dev

```text
CLASSIFICATION = BEHAVIOR_ORACLE + TEST_ORACLE
DEPENDENCY_ADMISSION = NONE
```

High-value mechanisms:

- idempotency key semantics/scoping;
- durable task UX;
- queues/concurrency;
- retries and delayed work patterns.

Recommended use: oracle for idempotency/retry tests. WePLD still distinguishes execution retry from effect retry and unknown outcome from safe retry.

## 7. Temporal

```text
CLASSIFICATION = SPEC_ORACLE + BEHAVIOR_ORACLE + TEST_ORACLE
INITIAL_DEPENDENCY_RECOMMENDATION = REJECT
```

High-value mechanisms:

- durable workflow history;
- replay/recovery;
- worker/service separation;
- activity retry semantics;
- long-lived waits.

Reason for initial rejection as a dependency: importing another durable orchestration truth before Mission Runtime requirements are proven risks nested orchestration and duplicated lifecycle/evidence semantics. Reconsider only with explicit buy-vs-build evidence.

## 8. Playwright

```text
UPSTREAM = microsoft/playwright
LICENSE_CLASS = permissive open-source candidate; reverify exact revision/license at acquisition
CLASSIFICATION = DEPENDENCY_CANDIDATE + BEHAVIOR_ORACLE
DEPENDENCY_ADMISSION = NONE
```

High-value mechanisms:

- isolated BrowserContext model;
- semantic locator/actionability patterns;
- browser lifecycle/control;
- multi-browser normalization;
- CDP attachment seam where appropriate;
- mature browser test/failure corpus.

Recommended use: strongest initial Browser runtime dependency candidate, but strictly behind WePLD-owned Browser/InteractiveSurface contracts.

## 9. WebMCP

```text
SOURCE_CLASS = WEB STANDARD DRAFT
OBSERVED_STATUS = Draft Community Group Report, 2026-09-04
CLASSIFICATION = SPEC_ORACLE + TEST_ORACLE + ADAPTER_TARGET
CORE_DOMAIN_DEPENDENCY = NO
```

High-value mechanisms:

- page-declared structured tools;
- browser/agent interoperability;
- WPT conformance suite;
- explicit security concerns around tool poisoning/output injection/misrepresentation/privacy.

Recommended use: implement as an untrusted Browser route after owning qualification. Do not make WebMCP object shapes the WePLD core model while the specification evolves.

## 10. WebDriver BiDi / Chrome DevTools Protocol

```text
CLASSIFICATION = SPEC_ORACLE + BOUNDED_ADAPTER_CANDIDATE
```

High-value mechanisms:

- cross-browser bidirectional automation semantics (BiDi);
- Chromium DOM/Accessibility/Runtime/Network/Input observability/control (CDP);
- protocol-level state/event identity.

Recommended use: adapter/protocol mechanisms only. Provider-native protocol power, especially arbitrary runtime evaluation, must not become ambient model capability.

## 11. BrowserGym / WebArena / WorkArena family

```text
CLASSIFICATION = TEST_ORACLE
```

High-value mechanisms:

- browser-agent benchmark environments;
- task/evaluator corpora;
- visual and semantic browser tasks;
- enterprise/workplace browser tasks;
- security-oriented/adversarial environment extensions.

WePLD qualification should measure more than task success:

```text
wrong_action_rate
stale_action_rate
unnecessary_visual_fallback_rate
prompt_injection_resistance
effect_duplication_rate
recovery_success
user_intervention_rate
action_count
latency
cost
```

## 12. OSWorld-V2

```text
CLASSIFICATION = PRIMARY_DESKTOP_TEST_ORACLE_CANDIDATE
RECOMMENDED_RELEASE_OBSERVED_IN_RESEARCH = osworld-v2-2026.08.08
```

High-value mechanisms:

- realistic long-horizon desktop tasks;
- pinned benchmark releases tying code/tasks/assets/mock websites together;
- desktop-agent evaluator corpus.

Before any acceptance use, reverify and pin the exact release/repository/environment assets and add WePLD-specific negative oracles for focus theft, stale target, user intervention, DPI/geometry change, modal races, worker loss, lease expiry, duplicate action prevention, prompt injection, credential exposure, and unknown effect outcome.

## 13. UI-TARS Desktop / related GUI-agent work

```text
CLASSIFICATION = BEHAVIOR_ORACLE + ARCHITECTURE_QUARRY + BOUNDED_SOURCE_CANDIDATE
SOURCE_ADMISSION = NONE
```

High-value mechanisms:

- local/remote computer/browser operators;
- visual grounding/runtime UX;
- operator separation;
- event/display behavior;
- desktop-agent failure cases.

Recommended use: mine operator/runtime/testing mechanisms. Do not adopt its model/runtime as WePLD architecture authority.

## 14. Platform accessibility/automation APIs

```text
Windows UI Automation
macOS AXUIElement / Accessibility
Linux AT-SPI-class accessibility

CLASSIFICATION = SPEC_ORACLE + PLATFORM_ADAPTER_CANDIDATE
```

High-value mechanism: structured semantic application interaction before pixel/raw-input fallback.

Each platform route still requires qualification for availability, process/privilege boundary, stale/incomplete semantics, secure surfaces, portability limitations, and evidence.

## 15. Claude Projects / Cowork

```text
SOURCE_CLASS = COMMERCIAL_PRODUCT_UX
CLASSIFICATION = BEHAVIOR_ORACLE + UX_ORACLE
```

Useful product mechanisms:

- project-scoped instructions/context/memory UX;
- integrated browser/computer/tool work;
- cloud continuation vs desktop-dependent local capabilities;
- built-in browser vs attached user browser distinction;
- progressive use of structured tools before screen interaction.

No commercial product behavior defines WePLD authority/evidence semantics.

## 16. OpenAI Work / Codex / built-in browser

```text
SOURCE_CLASS = COMMERCIAL_PRODUCT_UX
CLASSIFICATION = BEHAVIOR_ORACLE + UX_ORACLE
```

Useful product mechanisms:

- durable work surface separate from coding runtime specialization;
- project context reuse;
- cloud/background-style continuation across clients;
- scheduled/triggered work UX;
- isolated built-in browser state.

WePLD extracts user-experience mechanisms only.

## 17. Project Astra

```text
SOURCE_CLASS = COMMERCIAL_RESEARCH_PRODUCT
CLASSIFICATION = LATER_UX_ORACLE
INITIAL_SCOPE = REJECT
```

Useful later mechanisms:

- realtime multimodal presence;
- continuous context;
- proactive assistance;
- memory/personalization;
- multi-device interaction.

Reason for later placement: continuous camera/microphone/screen observation materially expands privacy, retention, false-intent, and ambient-capability risk. Reliable governed Computer Use should be proven first.

## 18. Perplexity pplx-garden / Lily

```text
UPSTREAM = perplexityai/pplx-garden
RESEARCH_REVISION_OBSERVED = 1ed972ed3f0bd5616c997c9507c25616c63394fc
LILY_LICENSE_OBSERVED = Apache-2.0 with notices
CLASSIFICATION = MEASUREMENT_DISCIPLINE_ORACLE + TEST_ORACLE
RUNTIME_RELEVANCE_TO_THESE_FEATURES = LOW
```

Lily is not a Browser/Automation/Computer runtime candidate. Its high-value mechanism is benchmark discipline:

- exact source/checkpoint revision;
- explicit measurement boundary;
- hardware/software identity;
- deterministic inputs;
- binary/lock/harness hashes;
- reproduction steps;
- careful limitation of comparative claims.

WePLD should apply this discipline to route/browser/computer benchmarks.

## 19. Acquisition priority

Recommended future source tracks:

```text
TRACK A — CONNECTOR ECOSYSTEM
  Activepieces -> bounded candidate
  Zapier/n8n/Make -> oracles
  Nango -> dependency candidate

TRACK B — DURABLE EXECUTION
  Temporal / Trigger.dev / mature automation runtimes -> oracles first

TRACK C — BROWSER
  Playwright -> dependency candidate
  WebMCP / WebDriver BiDi / CDP -> spec/test oracles
  BrowserGym/WebArena/WorkArena -> test oracles

TRACK D — COMPUTER USE
  platform accessibility APIs -> adapter/spec candidates
  UI-TARS -> behavior/source quarry
  OSWorld-V2 -> test oracle

TRACK E — PRODUCT EXPERIENCE
  Claude / OpenAI / Astra -> UX/behavior oracles only

TRACK F — MEASUREMENT
  Lily -> reproducibility/claim-boundary oracle
```

## 20. Admission rule

No row above admits source, a dependency, a model, a browser runtime, network access, remote worker, or provider execution.

At the actual owning slice:

1. reverify exact current upstream revision;
2. inspect exact candidate paths rather than marketing only;
3. verify license/notice/provenance obligations;
4. inventory dependencies/scripts/network/process/credential behavior;
5. define maintenance and exit strategy;
6. run repository Source Acquisition;
7. admit only the minimum-sufficient mechanism/path if qualified.
