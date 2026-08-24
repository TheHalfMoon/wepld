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

## Reference-only boundary

`anthropics/claude-code` is reference-only under its current repository terms. Do not copy source unless a future exact rights review establishes a different permissible source surface.

## Additional mining queue

Tree-sitter, SCIP, ast-grep, Joern/CPG, OpenGrep, OPA, OpenHands, Goose, Cline, Aider, OpenSandbox, E2B, gVisor, Firecracker, in-toto, SLSA and OpenTelemetry.

Each must be pinned and rights/dependency/security reviewed at the capability-triggered mining gate before source reuse.

## Explicit no-admission statement

A pin in this file establishes only reproducible reconnaissance identity. It is not a dependency selection, source import authorization, runtime authorization or security qualification.
