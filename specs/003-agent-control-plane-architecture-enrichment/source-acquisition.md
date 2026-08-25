# Source Acquisition — Spec 003 Planning Gate

```text
STATUS = RECONNAISSANCE_COMPLETE / PATH_MINING_PENDING
FROZEN_402_REGISTRY_MUTATION = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = NONE
```

## Tier-1 reconnaissance pins

- `microsoft/vscode@7c54fda801c73e35072ac759b6d93f8c69c65d7b` — MIT — Agent Host source/contracts/tests.
- `microsoft/agent-host-protocol@c058e213d8ed610cc011a8de2cfe20dd3f8dda84` — MIT — shared session/state protocol.
- `agentclientprotocol/agent-client-protocol@62c74ac119ec3296809496482440afca69926ce9` — Apache-2.0 — agent/client edge protocol.
- `a2aproject/A2A@16ba52690519bf55b9388e34d4db356efa88aa51` — Apache-2.0 — future agent-to-agent protocol/TCK.
- `vitali87/code-graph-rag@79abdb5fdbcde6d138db071efbe61e9afc16f63d` — MIT — code graph/data-flow/parser quarry.
- `Graphify-Labs/graphify@91f4d120b630ee35c79bf3c75ccd186870a808f9` — MIT declared in `pyproject.toml`; standalone root license file not established; exact rights/notice qualification required at path-mining gate.
- `microsoft/agent-governance-toolkit@b5705588883fac48b88cbe6fd0bd7d48c798453e` — MIT — ACS policy runtime/spec/conformance quarry.
- `cedar-policy/cedar@ba579ee7e9d63afa73a5b59be0d338a404c6108b` — Apache-2.0 — Rust authorization candidate.
- `openai/codex@339751715c64496cb86246bfb3935f40e309dd3d` — Apache-2.0 — Rust sandbox/approval/runtime boundary quarry.
- `deepseek-ai/deepseek-harness@b150a551b8d465e31e418e1b2eaf5e79bbb7d28e` — MIT — session/event/plugin/recovery quarry.
- `bytedance/trae-agent@e839e559ac61bdd0e057c375dd1dee391fee797d` — MIT; exact tree `fceea1cae3ddf5fcc29649db47449c54e011844e` — bounded agent-loop/trajectory/Docker-tool/CKG/evaluation/test-time-scaling quarry for Mission Runtime, Work, Fehrest.Maemar and Assurance. Whole-project adoption is not selected.

## TRAE source/product separation

The open-source `bytedance/trae-agent` repository and current TRAE product must be treated as separate evidence surfaces.

```text
TRAE_PRODUCT != TRAE_AGENT_SOURCE
PRODUCT_REFERENCE != SOURCE_ADMISSION
```

Current `trae.ai` IDE/SOLO/Work behavior, custom-agent/sub-agent/team UX, and integrated editor/browser/terminal/document experience are **reference-only product evidence**. No commercial product source rights or implementation equivalence are inferred from the MIT-licensed `trae-agent` repository.

Future Trae Agent path mining should prioritize:
- `trae_agent/agent/*` — step/runtime/tool-call seams and negative authority oracle;
- `trae_agent/utils/trajectory_recorder.py` — trajectory/evidence schema quarry;
- `trae_agent/tools/ckg/*` — lightweight local code-index ideas plus freshness/coverage failure corpus;
- Docker manager/executor and effectful tools — containment/tool-boundary quarry;
- `evaluation/patch_selection/*` — candidate-generation/selection/test-time-scaling mechanics;
- model clients/config/MCP surfaces — provider/network/credential/dependency inventory;
- `server/*` — headless/replay direction, explicitly not production-ready at the inspected pin.

Trae Agent's current Python dependency graph includes multiple direct model-provider SDKs, MCP, Tree-sitter and related runtime/build packages. These dependencies are NOT admitted by this pin.

## Reference-only boundary

`anthropics/claude-code` is reference-only under its current repository terms. Do not copy source unless a future exact rights review establishes a different permissible source surface.

CodeQL is a **reference-only security oracle/evaluation surface in Spec 003**. This planning package does not classify CodeQL as an admitted donor or dependency candidate. Any future source/dependency use would require a separate capability-triggered exact pin, rights/license/notice, dependency, security, portability, maintenance, and exit-strategy qualification.

TRAE/trae.ai product behavior is reference-only as described above. The separately pinned MIT `bytedance/trae-agent` repository is the only Trae-related source-mining candidate established by this planning package.

## Additional mining queue

Tree-sitter, SCIP, ast-grep, Joern/CPG, OpenGrep, OPA, OpenHands, Goose, Cline, Aider, OpenSandbox, E2B, gVisor, Firecracker, in-toto, SLSA and OpenTelemetry.

Each must be pinned and rights/dependency/security reviewed at the capability-triggered mining gate before source reuse.

## Exact qualification requirements for harness candidates

Before any source reuse from Trae Agent or another harness candidate, require:

1. exact path/blob inventory and retained copyright/license/notice obligations;
2. dependency/SBOM and supply-chain qualification;
3. model-provider, network, credential and telemetry surface inventory;
4. MCP/tool/process-effect inventory;
5. Docker/sandbox/host containment analysis;
6. Windows portability and process-cleanup behavior;
7. trajectory/replay integrity and secret-content handling review;
8. provider/session identity mapping to WePLD-owned Work identity;
9. proof that effectful execution can be placed behind Nawat without donor authority leakage;
10. minimum-reuse and exit-strategy decision.

For Trae CKG specifically, treat its current freshness logic and documented language/rebuild limitations as negative-test inputs. WePLD must use content/object-addressed provenance and fail closed on unknown or stale graph coverage.

## Explicit no-admission statement

A pin in this file establishes only reproducible reconnaissance identity. It is not a dependency selection, source import authorization, runtime authorization, provider authorization or security qualification.
