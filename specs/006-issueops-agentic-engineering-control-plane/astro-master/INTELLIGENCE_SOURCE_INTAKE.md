# Intelligence Source Intake

```text
STATUS = CANDIDATE_SOURCE_INTAKE
OBSERVATION_DATE = 2026-09-23
BASE_WEPLD_MAIN = 666e62d7d9e040505baca277a474d734afcc07a0
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
MODEL_EXECUTION_AUTHORITY = NONE
NETWORK_AUTHORITY = NONE
```

This intake supports `WEPLD_LOCAL_INTELLIGENCE_CAPABILITY_AMENDMENT.md`. It records candidate identities and dispositions only. It does not alter the frozen 402-entry registry count or silently create a new canonical registry revision.

The founder states permission to copy/use the requested source code and sources available in the founder's GitHub repositories.

```text
FOUNDER_PERMISSION_ASSERTED_2026_09_22 = YES
FOUNDER_PERMISSION_REAFFIRMED_2026_09_23 = mizorewww/laya-coreml, caio0452/jev_search, unreallabsai/unreal-agent, mrmps/classifier-dev
FOUNDER_PERMISSION_ASSERTION != SOURCE_ADMISSION
FOUNDER_PERMISSION_ASSERTION != PUBLIC_LICENSE_METADATA
FOUNDER_PERMISSION_ASSERTION != PATH_LEVEL_PROVENANCE
```

Any actual import still needs selected paths, digests, rights evidence, dependencies, build/import hooks, negative oracles, conformance and an exit route.

## 1. Fresh public candidate anchors

| Candidate | Observed revision / identity | Public rights observed | Proposed disposition | Owning tasks | Admission |
|---|---|---|---|---|---|
| `google/ax` | `d8ed0fe38bceb7842d3c47817d53d16ccdfcb601` | Apache-2.0 `LICENSE` | BEHAVIOR_REFERENCE + SALVAGE selected Task/Workspace/Gateway/Model/lifecycle mechanisms; reject Kubernetes/Redis as default dependencies | A05, F05, U01/U02, F06, O03 | NONE |
| `superdesigndev/treg` | `6e667a4c6f7c70c448ea6574c5a038ba8f14bc5f` | Apache-2.0 text plus Additional Terms restricting hosted/embedded third-party commercial service without explicit licensor authorization | SALVAGE/ADAPT capability catalog, MCP facade, CLI/skill bundle, credential-binding and audit mechanisms; preserve founder custom-permission evidence if relied upon beyond public terms | A09, H01, H02, F06 | NONE |
| `TheoLeeCJ/SemIf` | `1f2dea3e25379f9dfc98cb83c324f00ab5deda37` | MIT | ADAPT/BENCHMARK local typed-decision scoring, shared-state decisions, calibration patterns; never authority | A09, K03 | NONE |
| `Mapika/decider` | `e84e36c1d9fbc5d3ed588e3b916bf1b465cc6282` | Apache-2.0 | ADAPT/BENCHMARK typed decisions, probabilities, TypeSafe-compatible boundary and local model routes | A09, K03 | NONE |
| `mizorewww/laya-coreml` | `4619e0483f07adf39068532e85b42ec2347edb83` | Apache-2.0 + NOTICE; founder permission reaffirmed | ADAPT/BENCHMARK local typed-decision runtime for Apple Silicon/Core ML/ANE; mine calibration clamps, offline/cache controls, artifact checksums, conversion-fidelity fixtures and hardware/energy evidence. macOS/Apple-Silicon-specific route only; never general authority | A09, A05, K03, B03 | NONE |
| `caio0452/jev_search` | `ea073f6db48f5bff73ae4b9f2240d2d302fb9dc1` | No public license file found at observed revision; founder explicitly asserts permission to copy/use | SALVAGE/REFERENCE two-stage directory search, keyword-density prioritization, chunk scheduling, parallel decision filtering and progressive result emission. Reject its OpenRouter requirement as a default dependency; adapt behind local/qualified CalibratedDecision routes | A09, A04, F04, K03 | NONE |
| `unreallabsai/unreal-agent` | `df8b0ba560da17fd705d941cbeb75eff86c74a1e` | MIT; founder permission reaffirmed | SALVAGE/ADAPT async harness mechanics: stable input IDs, inbox deduplication, append-only/forkable sessions, versioned operations, pure synchronous tool translators, durable operation manager, cancellation/retry/recovery tests. Preserve WePLD Runtime/UWC/Nawat ownership | A09, A05, F05, U01/U02, F06, O03 | NONE |
| `mrmps/classifier-dev` | `8f2bb2b84a0d51ad1c9ed3436b64155908354f75` | MIT; founder permission reaffirmed | SALVAGE/BENCHMARK zero-shot/multi-label classification contracts, Jev packing, confidence/escalation logic, CLI/SDK/MCP/skill surfaces and eval harness. Hosted Cloudflare/provider chain is optional behavior reference, not a mandatory dependency; prefer local route where qualified | A09, A05, K03, H01, B03 | NONE |
| `tinyfish-io/agentql` | `418ba8ad1c69dfac134a6833369a01dfba5a24a7` | MIT | ADAPT/REFERENCE semantic browser querying/extraction behind WePLD browser contracts | A09, K01, P05 | NONE |
| `tinyfish-io/bigset-oss` | `73b5fd0289d17bf99f14e770eabc6b7ec7406bc5` | AGPL-3.0 | BEHAVIOR_REFERENCE first; study intent->schema->parallel acquisition->verification->dedupe->refresh workflow. Any code import needs explicit AGPL/custom-rights compatibility review | A09, K01 | NONE |
| `wonderwhy-er/DesktopCommanderMCP` | `75048278f4866f0d8bde26f6f9aa3b8d39dca870` | MIT | ADAPT/REFERENCE local filesystem/terminal/process UX and MCP mechanisms; real-machine access is not a containment boundary | A09, P05, O02/O03, UWC/F06 | NONE |
| `deepseek-ai/DeepSeek-OCR-2` | `2f3699ebbb96fa8af32212e8c170f2cc28730fad` | Apache-2.0 in `LICENSE.txt` | BENCHMARK + candidate local OCR/document engine after code/weights/tokenizer/runtime qualification. README Transformers example uses `trust_remote_code=True`; no such trust is inherited | A09, A04, P03, S01/S02 | NONE |
| `bespokelabs/Bespoke-Nimble-9B` | Hugging Face model ID observed 2026-09-22; updated 2026-09-18; exact immutable model revision/digests still required before admission | Hub metadata: Apache-2.0; Qwen3.5-9B adapter/PEFT tags | BENCHMARK + candidate calibrated typed-decision route; no model execution until exact weights/base/tokenizer route is pinned | A09, K03 | NONE |
| `https://laya.aay.sh` | behavior/source-permission reference; exact source artifact/revision not established by this intake | founder permission asserted; public source artifact/license not established here | BEHAVIOR_REFERENCE for normalized events, enrichment/triage and Action Cards. Do not infer source-tree identity from website behavior | A09, P04 | NONE |
| Cohere Parse | external product/behavior benchmark reference | hosted service terms, not source admission | BENCHMARK_REFERENCE for document parsing/layout/table/forms/Arabic behavior where measurable; never a required local dependency | P03/B02/B03 | NONE |
| TypeSafe/Jev | provider/interface/philosophy reference | no source admission asserted by this row | BEHAVIOR_REFERENCE for runtime-defined typed decisions, calibration and abstention. WePLD owns CalibratedDecision and Nawat remains authority | K03 | NONE |

## 2. DeepSeek-OCR-2 observed import-risk notes

At revision `2f3699ebbb96fa8af32212e8c170f2cc28730fad` the public README documents:
- CUDA 11.8 + Torch 2.6.0 environment;
- vLLM 0.8.5 route;
- image and PDF inference;
- benchmark batch evaluation;
- Transformers loading with `trust_remote_code=True`;
- document-to-Markdown grounding prompt.

Before any WePLD execution/import, freeze:
- repository tree and selected source paths;
- Hugging Face model/weights revision and file hashes;
- tokenizer/config hashes;
- all custom Python/modeling code executed by the loader;
- vLLM/Torch/FlashAttention dependency graph;
- CUDA/driver/platform matrix;
- build/install hooks and network access;
- memory/VRAM/page/image ceilings;
- cancellation/timeout behavior;
- output path/file behavior;
- license/NOTICE obligations for repo, model and transitive assets.

```text
README_WORKS != WEPLD_QUALIFIED
TRUST_REMOTE_CODE_TRUE != WEPLD_TRUST_DECISION
MODEL_REPO_LICENSE != TRANSITIVE_DEPENDENCY_QUALIFICATION
```

## 3. Decision/search/harness source notes — 2026-09-23 additions

### Laya-CoreML

Observed revision: `4619e0483f07adf39068532e85b42ec2347edb83`.

High-value mining targets:
- `laya_coreml/agent.py`, `ane.py`, `common.py`, `inputs.py`, `prompt.py`, `result.py`, `tokenizer.py`;
- artifact/package validation in `artifacts.py` and local/cache resolution in `hub.py`;
- conversion and portability evidence in `convert.py` and `torch_model.py`;
- committed `tests/`, `benchmarks/`, `BENCHMARKS.md` and ANE evidence.

Important upstream lesson already visible at this revision: calibration temperatures are clamped to `[0.5, 5.0]` because an upstream `choice:11+` bucket could otherwise over-sharpen confidence. WePLD must preserve raw calibration evidence, route identity and warnings rather than importing a confidence number as truth.

```text
COREML_ROUTE = APPLE_SILICON_SPECIFIC
LOCAL_FILES_ONLY = QUALIFICATION_TARGET
LayaProbability != NawatDecision
LayaCalibration != CompletionDecision
UPSTREAM_BENCHMARK != WEPLD_BENCHMARK_PASS
```

### Jev Search

Observed revision: `ea073f6db48f5bff73ae4b9f2240d2d302fb9dc1`.

The repository is intentionally small and its README warns it is fully AI-generated and not production-ready. No public `LICENSE*`/COPYING file was found during this intake. The founder explicitly states permission to copy/use its source; any import relying on that permission must preserve the custom grant evidence.

Mine the mechanism, not the hosted dependency:
- file discovery and ignore rules;
- keyword-density/top-file prioritization;
- bounded chunking;
- high-priority then low-priority scheduling;
- concurrent decision requests;
- progressive result emission;
- criteria parser behavior and negative tests to be constructed.

Its current OpenRouter Decisions requirement conflicts with WePLD's local-first/no-silent-fallback default and is therefore a donor implementation detail, not a required architecture choice.

### Unreal Agent

Observed revision: `df8b0ba560da17fd705d941cbeb75eff86c74a1e`.

High-value mechanism targets are under `harness/` and `benchmarks/`:
- caller-stable Input IDs and session-scoped deduplication;
- append-only persisted sessions and forks;
- context builder with explicit omitted/truncated/compacted accounting;
- schema-bound Tool -> pure ToolTranslator -> serializable Operation separation;
- operation state persisted separately from model-facing tool-call status;
- swappable durable operation manager;
- retry timing, cancellation, recovery and provider-adapter tests.

Do not import Unreal Agent as a second runtime authority. WePLD Mission Runtime owns Task/Attempt lifecycle, UWC owns normalized adapters and Nawat owns protected effects.

### classifier.dev

Observed source repository: `mrmps/classifier-dev@8f2bb2b84a0d51ad1c9ed3436b64155908354f75`.

High-value mining targets:
- `src/jev.ts`: typed-decision packing/probability handling;
- `src/index.ts`: request validation, multi-label/single-label routing, provider/escalation/fallback accounting;
- `src/privacy.ts`, `src/cost.ts`, limiter/receipt patterns;
- `eval/bench.py`, `eval/vs_jev.py`, `eval/fallback_bench.py`, `eval/cases.py`: evaluation/calibration/fallback corpus mechanics;
- `cli/`, `sdk/python/`, `sdk/go/`, MCP/skill descriptors for capability packaging and conformance.

The hosted Cloudflare Worker and its upstream API/provider fallback chain are not a core WePLD dependency. The valuable reusable shape is classification-as-a-typed decision surface plus evaluation/observability. Local qualified routes remain preferred when the user selects `LOCAL_ONLY`.

```text
CLASSIFICATION_RESULT != AUTHORITY
HOSTED_CLASSIFIER != REQUIRED_CORE_DEPENDENCY
FALLBACK_CHAIN != SILENT_SUBSTITUTION_PERMISSION
PROVIDER_ESCALATION_REQUIRES_ROUTE_IDENTITY
```

## 4. Treg rights and product-boundary note

The public Treg license observed at the pinned revision is not plain Apache-2.0. Its Additional Terms include a hosted/managed/embedded service restriction for third parties without explicit authorization.

The founder separately states permission to copy/use the source. If WePLD relies on that permission for an otherwise restricted use, the actual import record must include the custom authorization evidence and scope.

Technical disposition remains separate from rights:

```text
TECHNICAL_DISPOSITION = ADAPT_OR_SALVAGE_SELECTED_MECHANISMS
PUBLIC_RIGHTS = CONDITIONAL_ADDITIONAL_TERMS
CUSTOM_RIGHTS = FOUNDER_ASSERTED_PENDING_IMPORT_RECORD
SOURCE_ADMISSION = NONE
```

## 5. TinyFish family boundary

The founder requested the TinyFish source family. Do not bulk-admit an organization.

Current high-value candidates captured here:
- AgentQL for semantic browser/query/extraction mechanisms;
- BigSet OSS for live-dataset workflow behavior.

Future ASTRO-A09 source discovery may add other TinyFish repositories only when a concrete WePLD capability needs them.

```text
ORG_PERMISSION_OR_VISIBILITY != BULK_ADMISSION
ONE_REPO_LICENSE != ANOTHER_REPO_LICENSE
HOSTED_API_BEHAVIOR != PUBLIC_CORE_SOURCE
```

Do not make TinyFish cloud, OpenRouter or any paid provider a mandatory WePLD core dependency.

## 6. Founder-owned/source-family candidates

All relevant founder-owned public/private repositories are discovery candidates, not automatically imported source. Cross-project reuse must still pin the exact repository revision and selected paths so provenance remains reconstructable.

High-priority current anchors observed:

| Repository | Main observed | Candidate mechanisms | WePLD disposition |
|---|---|---|---|
| `TheHalfMoon/Morize` | `62fc04d01d398da93b4dacf0ab2f33e3f1440462` | memory lifecycle, retrieval provenance, local privacy, Graphify/code-graph-RAG source studies | SALVAGE/REFERENCE into Fehrest/K02/A04 only by selected mechanism |
| `TheHalfMoon/kernux` | `e9300caaee76ccede8e59316ed154b1bcbd9d71d` | local privacy, context/memory/search, tool/security/effect patterns, evidence discipline | SALVAGE/REFERENCE behind existing owners; no runtime replacement |
| `TheHalfMoon/Ascout` | `4e14d4f99ac00349757d0e728fff3702525d8e92` | Review/Test/Security, browser/mobile/OCR evidence, quality engineering | SALVAGE/REFERENCE into Assurance/P05/P03 with independent qualification |
| `TheHalfMoon/MESC` | `0645cd770062f2af0d10fd047f946d9201c8ba41` | model registry/evaluation, sandbox/evidence attestation, provenance and fail-closed qualification patterns | SALVAGE/REFERENCE; never transfer domain-specific medical authority into WePLD |

Other founder repositories remain searchable under Source Acquisition Check. A task must name the needed mechanism before mining/import.

```text
FOUNDER_OWNED_REPO != WEPLD_CANONICAL_OWNER
CROSS_REPO_REUSE != SHARED_AUTHORITY
```

## 7. Required per-import record

Every imported/adapted mechanism must record:

```text
capability/task
repository/model/source identity
exact commit/revision/tree/blob
exact path/file set
base model and weight identities when applicable
tests/fixtures/failure corpus mined
public license/NOTICE
custom grant evidence when relied upon
transitive dependencies
build/install/import hooks
network behavior
remote-code/custom-loader behavior
supported OS/toolchain/hardware
maintenance/advisory observation
data/secret boundary
authority boundary
adaptation/porting decision
conformance fixtures
negative oracles
benchmark evidence
rollback/removal/replacement route
residual limitations
decision owner
```

## 8. Source-to-task routing

| Source family | First owning task | Later consumers |
|---|---|---|
| Google AX | A09/A05 | F05, U01/U02, F06, O03 |
| Treg | A09 | H01/H02/F06 |
| SemIf | A09 | K03 |
| Decider | A09 | K03 |
| Laya-CoreML | A09/A05 | K03/B03; Apple-Silicon local route only |
| Jev Search | A09/A04 | F04/K03; reuse search scheduling/filtering, not mandatory OpenRouter |
| Unreal Agent | A09/A05 | F05/U01/U02/F06/O03 |
| classifier.dev | A09/A05 | K03/H01/B03; local adapter/eval patterns preferred |
| Bespoke Nimble 9B | A09 | K03 |
| DeepSeek-OCR-2 | A09/A04 | P03, S01/S02, B03 |
| TinyFish AgentQL | A09 | K01/P05 |
| TinyFish BigSet | A09 | K01 behavior profile |
| Desktop Commander | A09 | P05/O02/O03/UWC |
| Laya | A09 | P04 |
| Morize mechanisms | A04/A09 | F03/F04/K02/B03 |
| Kernux mechanisms | A09 by concrete need | F04/F06/H01/P05/S01 |
| Ascout mechanisms | A07/A09 by concrete need | Review/Test/Security/P05 |
| MESC mechanisms | A05/A09 by concrete need | model/sandbox/evidence qualification |

No row changes the existing 63-task dependency graph.

## 9. Admission stop conditions

Stop an import/admission when any of the following is unresolved for the selected mechanism:

- exact source/model identity cannot be pinned;
- rights for the selected paths/assets are not evidenced;
- hidden custom/remote code would execute without qualification;
- transitive build/install hooks are unknown;
- local/offline claim cannot be reproduced;
- capability would create a competing authority/truth owner;
- effect boundary cannot be expressed through Nawat/UWC;
- source or model update cannot be pinned/rolled back;
- negative tests are unavailable and cannot be constructed;
- benchmark shows no material value over simpler admitted machinery;
- exit/replacement path is not credible.

A rejected source candidate blocks only that candidate, not independent original implementation or other source candidates.