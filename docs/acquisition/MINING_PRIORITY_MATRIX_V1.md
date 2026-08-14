# WePLD Source Capability & Mining Priority Matrix V1
## 2026-08-14

This matrix does not change the ratified S1–S10 roadmap. It determines **which source families to mine when a ratified capability reaches its acquisition gate**.

| Capability / WePLD destination | Highest-value direct source quarries | Highest-value behavior / benchmark oracles | Current rule |
|---|---|---|---|
| S1 Desktop ↔ Rust Core | Tauri, Zed selected workspace mechanics | Devin/Kiro/Kilo workspace UX | UI/desktop transport has zero authority |
| S2 Project Doctor / Git intelligence | gix, Git/JJ references, ripgrep, Tree-sitter | Graphite/CommandCode change UX | Git remains canonical effect mechanism initially |
| S3 Terminal / Process / Windows | windows-rs, portable-pty, Codex Windows mechanics, hcsshim reference | OpenShell/LiteBox/E2B/Daytona | B-WIN-001 remains open until WePLD profile evidence |
| S4 Fehrest Minimum | Glean, Codebase Memory MCP, Tree-sitter, SCIP/Zoekt, Tantivy, gix | Augment, Greptile, Cohere Agentic RAG, Kiro | retrieval/context never grants authority |
| S5 AGILLE / Spec | GitHub Spec Kit, deterministic schema/spec tooling, Fern | Kiro Specs, Devin interactive planning, CommandCode Plan | Spec artifact != canonical authority |
| S6 UWC / Mirefa / Edara | DeepSeek Harness+Cordis, Goose, Kilo, Eigent+CAMEL, OpenHands/Continue/Codex adapters | Devin managed agents, Kiro Powers/Skills | minimum-sufficient worker topology; no silent route substitution |
| S7 Native Assurance | OpenCodeReview, reviewdog, deterministic scanners, Qodo Open Aware, public review edges | Cubic, Greptile, Augment, Qodo, Graphite, Devin Review | ReviewOutcome != CompletionDecision |
| S8 Repair / Trusted Completion | Mission/Nawat native contracts + donor failure corpora | Codex/Goose/DeepSeek Harness/Eigent negative oracles | retry/repair requires separate authorized Attempt |
| S9 Recovery / ChangeStack | JJ operation log, Git/gh-stack/Git Town, source/test corpora | Replit, CommandCode rewind, Graphite stacks | rollback claim must match reversible effect class |
| S10 Byan learning | outcome/event data + deterministic benchmark machinery | CommandCode Taste, Devin session analysis, Kiro skills, routing/Edara research | learning proposes; never authorizes |
| External SDK/adapters | Fern, provider SDKs, WIT/Wasmtime when justified | Cohere/OpenAI/etc provider contracts | generated artifacts are derived, replaceable |
| Design surfaces | OpenPencil, Penpot, Figma Code Connect, Onlook, Impeccable | Figma/v0/Magic Patterns | product surface only; owner resolved through canonical subsystems |

## Highest-priority source pairs

```text
DeepSeek Harness + Cordis
Eigent + exact CAMEL 0.2.91a5 lineage
Codex + windows-rs + portable-pty
Fehrest stack: Tree-sitter/SCIP/Zoekt/Glean/Tantivy + Augment/Greptile/Cohere behavior
Assurance stack: deterministic scanners + OpenCodeReview + Qodo + Cubic/Greptile/Augment/Graphite behavior
Byan stack: CommandCode Taste + Devin session learning + historical accepted-outcome evidence
```

## Ponytail rule

No capability receives every donor listed above.

For each acquisition gate:
1. define exact required outcome;
2. choose 2–3 best candidate mechanisms;
3. inspect exact source/tests/failure model;
4. reject redundant dependency/runtime/service layers;
5. retain only the minimum implementation that improves accepted outcomes;
6. keep exit/replacement path.
