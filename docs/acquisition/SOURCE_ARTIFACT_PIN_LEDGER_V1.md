# WePLD Source Artifact Pin Ledger V1
## Exact repositories / child artifacts discovered during P0-A and bounded post-V1.5 enrichment — 2026-08-14

This is the child-artifact companion to the 402-entry Master Source Registry. Child repositories do **not** create new top-level named-entry counts.

```text
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
PINS = RESEARCH / ACQUISITION ANCHORS ONLY
REPINS_REQUIRED_AT_FD-P0-013
```

| Family | Artifact / repository | Pin | Rights state | Evidence status | Notes |
|---|---|---|---|---|---|

| Kilo Code | `Kilo-Org/kilocode` | `f7115470740c51fd4200fedd9ad3edfad60589ce` | MIT at current root; opencode lineage present | `BOUNDED_ENRICHED` | Current root licensing must override stale website-level Apache statements; path-level third-party lineage still required. |
| Kiro | `kirodotdev/Kiro` | `e8daa058590dd58efb14f6d41ddb3ba1a26cfba3` | NOT_FULLY_AUDITED | `PINNED_PUBLIC_EDGE` | Public repo does not establish full Kiro IDE/CLI core source. Product remains S+ behavior/spec/skills/powers/hooks oracle. |
| Goose | `aaif-goose/goose` | `5751715df0b4a5e81abe6533e608baec669bf131` | Apache-2.0 | `BOUNDED_ENRICHED` | Permission inspector, execution manager, sessions, ACP/MCP, subagent mechanics identified. |
| Zed | `zed-industries/zed` | `c05e34637b4f7f100a688bf6ac71cb70877fc8ad` | Mixed/path-specific; root Apache plus GPL-marked crates observed | `BOUNDED_ENRICHED_RIGHTS_COMPLEX` | ACP/editor/agent mechanics strong; whole-repo copy rejected; path-level rights mandatory. |
| Greptile | `greptileai/greptile-vscode` | `72fc0c5a68ff966e64c2b182a2e6bf5912410821` | MIT | `PINNED_PUBLIC_EDGE` | Public integration source pinned; Greptile core review/context engine public source not established. |
| Augment Code | `augmentcode/context-connectors` | `f7d6472ae626c98fd768f64cdfd6160145eefa77` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_SOURCE` | Context connector source candidate. |
| Augment Code | `augmentcode/augment-swebench-agent` | `17d813385f50ec59d58fdfe1576f758ed3daaa4e` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_SOURCE` | Agent harness/evaluation quarry. |
| Qodo Open Aware | `qodo-ai/open-aware` | `68976a9dd957f493a602b1063eaca553718c9254` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_SOURCE` | Code-context/research source candidate. |
| Qodo PR-Agent | `The-PR-Agent/pr-agent` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `LINEAGE_NAME_UPDATED` | Current repository ownership resolves to The-PR-Agent organization; provenance must not assume historical qodo-ai path. |
| Devin | `CognitionAI/devin-cli` | `bd4163ed29e934b898f185752182c91aacac20f7` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_EDGE` | CLI edge source; not public core-agent proof. |
| Devin | `CognitionAI/devin-extension` | `36437282f7f131d066022369ece7fd24c721c079` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_EDGE` | IDE/browser integration edge source. |
| Devin | `CognitionAI/devin-outpost-k8s` | `992f807dac0d33d578ff46eb7aa10ffbc93699b4` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PINNED_PUBLIC_INFRA` | Kubernetes/operator reference; not Alpha foundation. |
| Devin | `CognitionAI/devin-swebench-results` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_EVIDENCE_REPO` | Benchmark/evaluation evidence quarry. |
| Devin | `CognitionAI/qa-devin` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_TEST_REPO` | QA/test evidence quarry. |
| Devin | `CognitionAI/deepwiki` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_CONTEXT_REPO` | Project/code understanding behavior/source edge. |
| Devin | `CognitionAI/terraform-provider-devin` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_INFRA_REPO` | External integration/infrastructure edge. |
| Eigent | `eigent-ai/eigent` | `88d837f75ad95a21eebaa638072adad2019644be` | Apache-2.0 | `BOUNDED_ENRICHED` | Workforce/task decomposition/worker pool/context isolation/snapshots. Negative oracle: evaluator failure must not fabricate quality_score=80. |
| CAMEL | `camel-ai/camel package line used by Eigent` | `PACKAGE_VERSION camel-ai[eigent]==0.2.91a5; COMMIT_PIN_PENDING` | REQUIRES_EXACT_VERSION_RIGHTS_AUDIT | `UPSTREAM_LINEAGE_PIN_PARTIAL` | Eigent mining is incomplete without exact CAMEL version-to-commit mapping. |
| Fern | `fern-api/fern` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_SOURCE_CONFIRMED` | Contract-driven SDK/CLI/docs generation source candidate. |
| Cohere / Command / Aya / Rerank concepts | `cohere-ai/cohere-python` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_SDK_SOURCE` | Provider/conformance source; Cohere product/model not canonical dependency. |
| Cohere / Command / Aya / Rerank concepts | `cohere-ai/cohere-typescript` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_SDK_SOURCE` | Provider/conformance source. |
| Cohere / Command / Aya / Rerank concepts | `cohere-ai/cohere-developer-experience` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_PATH_LEVEL_CONFIRMATION | `PUBLIC_DOCS_SOURCE` | Agentic RAG/routing/parallel-query/reranking/citation behavior and docs source. |
| DeepSeek Harness | `deepseek-ai/deepseek-harness` | `47f943859bef60e4160492346772ded9b24f765a` | MIT | `BOUNDED_ENRICHED_DEVELOPER_PREVIEW` | Plugin-first harness; tool pipeline, durable session events, subagent provider seam, monotonic guards. No model admission implied. |
| Cordis | `cordiverse/cordis` | `8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4` | MIT | `PINNED_UPSTREAM_LINEAGE` | DeepSeek Harness underlying service/event/plugin/reversible-effects framework. |
| CommandCode | `CommandCodeAI/command-code` | `5c8f1b48c9d6704210cb3f9a476fdcffe5093e9a` | REQUIRES_EXACT_RIGHTS_AUDIT | `PUBLIC_DOCS_ISSUE_SURFACE` | Current public repository does not establish product core source. |
| CommandCode | `CommandCodeAI/cmd-old-public` | `48cacf798aa213f88cd5d2be12187a91c793bddf` | REQUIRES_EXACT_RIGHTS_AUDIT | `ARCHIVED_HISTORICAL_QUARRY` | Historical source/docs quarry only; archived. |
| CommandCode | `CommandCodeAI/desktop` | `PIN_PENDING_EXACT_FETCH` | REQUIRES_EXACT_RIGHTS_AUDIT | `PUBLIC_EDGE_REPO` | Small desktop edge repository; no product-core inference. |
| openai/codex | `openai/codex` | `91d6f48992ad8db636b3ca52a3a36c2fb6d75537` | Apache-2.0 | `PATH_MINED_PASS1` | P0A-01; PORT_CANDIDATE + NEGATIVE_ORACLE + REFERENCE |
| tauri-apps/tauri | `tauri-apps/tauri` | `d727d631659f07a597cc86cf808f505858dee878` | Apache-2.0 OR MIT (workspace package declaration) | `PATH_MINED_PASS1` | P0A-02; PACKAGE_CANDIDATE + ADAPT_CANDIDATE + REFERENCE |
| microsoft/windows-rs | `microsoft/windows-rs` | `5f8e1504dea507f1d86af7bf5a824eb49ff8b5a5` | MIT file verified; exact package metadata to remain path-registered | `PATH_MINED_PASS1` | P0A-03; PACKAGE_CANDIDATE + REFERENCE |
| Windows native execution/containment primitives | `Windows native execution/containment primitives` | `Documentation/API contracts; no Git revision is canonical for the OS APIs` | Platform/API documentation terms; no source import proposed | `PATH_MINED_PASS1` | P0A-04; REFERENCE + PORT_CANDIDATE |
| wezterm/wezterm — portable-pty | `wezterm/wezterm — portable-pty` | `fe3006aefcdc4c22924e7bce966b2c430dade4f1` | MIT; bundled fonts have OFL 1.1 obligations | `PATH_MINED_PASS1` | P0A-05; PACKAGE_CANDIDATE + REFERENCE |
| jj-vcs/jj | `jj-vcs/jj` | `3a81f836030b00bea85e66c4070d054c555af8b2` | Apache-2.0 | `PATH_MINED_PASS1` | P0A-06; REFERENCE + PORT_CANDIDATE |
| GitoxideLabs/gitoxide / gix | `GitoxideLabs/gitoxide / gix` | `dc370d9cacb4b06a132d2ffaaf224cc770173742` | MIT OR Apache-2.0 files verified | `PATH_MINED_PASS1` | P0A-07; PACKAGE_CANDIDATE + BENCHMARK |
| bytecodealliance/wasmtime | `bytecodealliance/wasmtime` | `0b9b72dc2bc7a3fd427c31c9e50ccb704c040a97` | Apache-2.0 WITH LLVM exception | `PATH_MINED_PASS1` | P0A-08; REFERENCE + PACKAGE_CANDIDATE (DEFERRED) |
| WebAssembly/component-model | `WebAssembly/component-model` | `6be2295c9c7c2add4f1d21a74e6493afff8e5120` | Apache-2.0 unless a subdirectory LICENSE says otherwise | `PATH_MINED_PASS1` | P0A-09; REFERENCE |
| NVIDIA/OpenShell | `NVIDIA/OpenShell` | `d22859c22d1de9ac83013b8947655e372709eb7a` | Apache-2.0 | `PATH_MINED_PASS1` | P0A-10; REFERENCE + PORT_CANDIDATE |
| microsoft/litebox | `microsoft/litebox` | `7af6242f0729c1f0224161c7cec0afc114994cf6` | MIT | `PATH_MINED_PASS1` | P0A-11; BENCHMARK + REFERENCE |
| microsoft/hcsshim | `microsoft/hcsshim` | `2bbdac6fec23e5ad2f9b8abb9520e1dbf11a8973` | MIT | `PATH_MINED_PASS1` | P0A-12; REFERENCE + PORT_CANDIDATE |
| e2b-dev/E2B | `e2b-dev/E2B` | `034c503f1fd51fd166db76dfae037673714d633b` | Apache-2.0 | `PATH_MINED_PASS1` | P0A-13; BENCHMARK + REFERENCE |
| daytonaio/daytona (historical public source) | `daytonaio/daytona (historical public source)` | `ec4c21b2d597091ac09ecc278f3bcc172575a987` | README points to v0.190.0 LICENSE; that pinned license is AGPL-3.0 | `PATH_MINED_PASS1` | P0A-14; REFERENCE + BENCHMARK + NEGATIVE_ORACLE + REJECT_FOUNDATION |

## Required treatment of `PIN_PENDING_EXACT_FETCH`

`PIN_PENDING_EXACT_FETCH` does not mean the source is unknown. It means:
- the source family/repository is accounted for;
- its exact immutable current acquisition revision was not frozen in the bounded pass represented here;
- no reuse/admission may occur until that pin and its exact paths/hashes/rights are recorded.

## High-value lineage pairs that must be mined together

```text
Eigent -> exact CAMEL lineage
DeepSeek Harness -> Cordis
Augment Code -> context-connectors + SWE-bench agent + product behavior
Devin -> product behavior + public edge/infra repos
Cohere Agentic RAG -> developer-experience docs + SDK contracts
Kiro -> product behavior/specs/powers/skills/hooks + public repo edge
Greptile -> product graph/review behavior + public VS Code/skills edges
CommandCode -> product Taste/skills/session behavior + public/archived repository edges
```


## Continue — bounded enrichment

| Family | Artifact / repository | Pin | Rights state | Evidence status | Notes |
|---|---|---|---|---|---|
| Continue | `continuedev/continue` | `5522c6f44ca0ac3528b37244818fbfa39b5af470` | Apache-2.0 | `BOUNDED_ENRICHED_MAINTENANCE_ENDED` | Current README states upstream is no longer actively maintained/read-only and final 2.0.0 was released. Mine CLI, agent modes, rules, MCP, source-controlled AI checks, config/context, tests and failure corpus. Do not make an unmaintained upstream a non-replaceable foundation. |
