# Source Acquisition Addendum — Product Capability Tracks

```text
STATUS = FUTURE_PLANNING_SOURCE_ACQUISITION_ADDENDUM
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
IMPORT_AUTHORITY = NONE
DONOR_EXECUTION = NONE
```

This addendum applies the parent Spec 006 Source Acquisition boundary to Projects / Work / Automations / Connections / Browser / WebMCP / Computer Use research.

Primary evidence record:

`research/product-capability-source-study-2026-09-06.md`

## 1. Current classification summary

```text
Activepieces              BOUNDED_SOURCE_CANDIDATE + BEHAVIOR_ORACLE
Zapier Platform            SPEC_ORACLE + BEHAVIOR_ORACLE + CLEAN_ROOM_REIMPLEMENT
n8n                        BEHAVIOR_ORACLE + SECURITY_ORACLE + FAILURE_ORACLE
Make                       SPEC_ORACLE + UX_ORACLE + FAILURE_ORACLE
Nango                      DEPENDENCY_CANDIDATE + BEHAVIOR_ORACLE
Trigger.dev                BEHAVIOR_ORACLE + TEST_ORACLE
Temporal                   SPEC_ORACLE + BEHAVIOR_ORACLE + TEST_ORACLE
Playwright                 DEPENDENCY_CANDIDATE + BEHAVIOR_ORACLE
WebMCP                     SPEC_ORACLE + TEST_ORACLE + ADAPTER_TARGET
WebDriver BiDi / CDP       SPEC_ORACLE + BOUNDED_ADAPTER_CANDIDATE
BrowserGym family          TEST_ORACLE
OSWorld-V2                 TEST_ORACLE
UI-TARS Desktop            BEHAVIOR_ORACLE + ARCHITECTURE_QUARRY + BOUNDED_SOURCE_CANDIDATE
Platform accessibility     SPEC_ORACLE + PLATFORM_ADAPTER_CANDIDATE
Claude/OpenAI products     UX_ORACLE + BEHAVIOR_ORACLE
Project Astra              LATER_UX_ORACLE
pplx-garden/Lily           MEASUREMENT_DISCIPLINE_ORACLE + TEST_ORACLE
```

These classifications are research routing only.

## 2. Rejected automatic admissions

```text
OPEN_SOURCE_LICENSE != SOURCE_ADMISSION
PUBLIC_GITHUB_REPOSITORY != SOURCE_ADMISSION
COMMERCIAL_PRODUCT_SIMILARITY != IMPLEMENTATION_RIGHT
MCP_OR_WEB_STANDARD_COMPATIBILITY != RUNTIME_ADMISSION
BENCHMARK_AVAILABILITY != ACCEPTANCE_EVIDENCE
DEPENDENCY_CANDIDATE != DEPENDENCY_ADMITTED
```

## 3. Initial source recommendations

### Adaptation/source candidates requiring a future exact gate

- Activepieces: only narrowly selected community framework/integration paths if needed;
- Playwright: dependency candidate behind WePLD-owned Browser contract;
- UI-TARS Desktop: only bounded mechanism paths if source adaptation is justified;
- platform accessibility APIs/libraries: adapter candidate by platform;
- Nango: dependency candidate only after license/deployment/exit-strategy review.

### Oracle-only default

- Zapier Platform;
- n8n;
- Make product/docs;
- Trigger.dev and Temporal until buy-vs-build evidence changes the decision;
- WebMCP/WebDriver BiDi/CDP specification semantics;
- BrowserGym/OSWorld benchmark corpora;
- commercial Claude/OpenAI/Astra product UX;
- Lily measurement discipline.

## 4. Required future gate inputs

Before any candidate crosses from research to source/dependency use, record:

```text
exact upstream repository / distribution identity
exact revision/version
candidate paths/packages only
license and notice obligations
third-party provenance
transitive dependency graph
build/install scripts and hooks
network behavior
auth/secret behavior
filesystem/process behavior
telemetry/update behavior
platform support
security/adversarial review
maintenance health
exit/replacement strategy
benchmark/test oracle value
why acquisition is minimum sufficient
```

## 5. Runtime quarantine

Research checkout/read access must not be confused with runtime use. Do not execute donor build/install hooks, browser automation, providers, connectors, remote workers, model runtimes, or benchmarks merely to complete this planning addendum.

```text
RESEARCH_READ != DONOR_EXECUTION
SOURCE_CLASSIFIED != SOURCE_ADMITTED
SOURCE_ADMITTED != RUNTIME_AUTHORITY
```

## 6. Default decisions until owning gates

```text
FULL_N8N_IMPORT = REJECT
ZAPIER_SOURCE_REUSE = REJECT_UNLESS_SEPARATELY_PROVEN
ACTIVEPIECES_FULL_PLATFORM_IMPORT = REJECT
TEMPORAL_DEFAULT_RUNTIME_DEPENDENCY = REJECT
PLAYWRIGHT = CANDIDATE_NOT_ADMITTED
NANGO = CANDIDATE_NOT_ADMITTED
UI_TARS_MODEL_RUNTIME = REJECT_AS_ARCHITECTURE_FOUNDATION
WEBMCP = ADAPTER_TARGET_NOT_AUTHORITY
ASTRA_LIKE_AMBIENT_RUNTIME = LATER_RESEARCH
```

The owning future slice may supersede these default recommendations only through its normal Spec Kit / Ponytail / Source Acquisition process with fresh evidence.
