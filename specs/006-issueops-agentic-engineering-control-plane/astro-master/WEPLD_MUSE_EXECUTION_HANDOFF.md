# Muse execution handoff

STATUS = PROPOSED_DEPENDENCY_ORDERED_HANDOFF. Implementation authorized by Astro: **NO**. First task: **ASTRO-G01**. Read the [master](WEPLD_CANONICAL_MASTER_BUILD_PLAN.md), trusted canonical governance and live GitHub state before using this file.

## How to execute without guessing

The graph contains 63 bounded tasks. A task is not an authority grant. C01 points to the existing 13 canonical S3 contract tasks; it does not duplicate or expand their authority. HOST/OBSERVE/SPAWN and every later code path require separately accepted exact grants. All D tasks deliver one concrete specification/qualification manifest; they do not ask Muse to implement an entire product family. Future manifests split product breadth into one adapter, contract, migration or UI state machine per leaf before any product code. This is deliberate staged implementation, not a claim that all later dependencies have already been admitted.

Default base is canonical main `765f9d4ae0588ca06b0f65cd76de16eaa8a5c246`, advanced only through accepted predecessors and a fresh trusted bootstrap. Never build future tasks from a stale planning SHA without reconciling intervening changes. Stop on an altered authority frontier, changed field owner or unresolved conflicting requirement.

## Common task contract (applies to every card)

- **Entry / prerequisite:** dependencies accepted with exact evidence, current trusted base and live branch/check state verified, Spec Kit and Ponytail FULL, current authority and source-acquisition record sufficient for the task. A dependent task is not unlocked merely because its predecessor produced a file.
- **Purpose / scope:** the named title and single bounded output in its card. All unrelated features, broad rewrites, new runtimes, donor installation and protected governance edits are out of scope unless the exact task grant explicitly includes them.
- **Files:** G/D/A/E write one task record under proposed `specs/006-issueops-agentic-engineering-control-plane/astro-execution/<TASK_ID>.md`, plus referenced approved evidence artifacts. D includes exact proposed leaf paths/API/fixtures; A includes source paths/hashes. I uses the proposed modules in its card only after path authority; add one test module and minimal exports, never an implicit dependency/policy change. X tasks use the canonical successor grant paths. C01 uses only `crates/contracts/src/s3.rs`, `crates/contracts/src/lib.rs`, `crates/contracts/tests/s3_contracts_v1.rs`. Proposed paths are not current files or grants.
- **Implementation requirements:** reuse existing field owners and state conventions; version serialized boundaries; explicit bounds, identity, scope, failure/cancellation and unsupported states. G/D/A/E must produce actionable evidence/manifests, not product code. D manifests bind each applicable feature ID to an owner, exact leaf, source record, tests, release claim and rollback.
- **Security invariants:** context/provenance/route choice is not authority; reviewer is not write authority; builder is not acceptance authority; Nawat at use; no silent route substitution or egress; tenant/project isolation; missing coverage is not PASS. Apply relevant TH rows in the security model.
- **Failure / recovery:** preserve predecessor evidence, durable reason and exact target; partial output remains noncurrent. Unknown external outcome requires reconciliation before retry. Changes are staged with a reversible migration or explicit compensation/irreversible limitation. A failed source candidate leaves the adapter unqualified rather than enabling a fallback.
- **Tests:** positive fixture for the single promised behavior; the card negative oracle; applicable target freshness, cancel/restart, bounds, secret-safe output, scope and schema compatibility cases. G/D/A use record/link/traceability/consistency checks, not invented runtime passes. E uses preregistered protocol and raw artifact checks.
- **Benchmarks:** B01/B02/B03 own comparative claims; other tasks capture overhead against their declared budget when runtime behavior changes. No performance claim from a README.
- **Acceptance / required evidence:** exact base/head/tree and scope, source/rights record if relevant, Spec Kit/Ponytail sufficiency, tests with environment/result/coverage, independent engineering review, security review when required by canonical policy, finding reconciliation, recovery/migration evidence and Build Learning. G records accepted or blocked; no builder-only acceptance.
- **Stop:** unauthorized paths/dependencies/egress, source rights unresolved for selected import, missing qualified platform/evaluator, unexpected secrets, route substitution, failing oracle, unknown effect, stale review, unmet prerequisite or ambiguity that changes surrounding architecture. Record the smallest missing gate and continue unrelated authorized tasks.

Types: G acceptance; A acquisition; D bounded manifest; C current pure contracts; I future-granted implementation; E experiment. Late profile manifests are implementation preparation, not shipped feature work. Release parity requires their later leaf tasks and tests, not just finishing this graph.

## Dependency graph

| Task | Title | Slice | Type | Dependencies |
|---|---|---|---|---|
| ASTRO-G01 | Accept the exact plan revision | P0 | G | NONE |
| ASTRO-F01 | Freeze current frontier and limitation carry-forward | P0/S3 | D | ASTRO-G01 |
| ASTRO-C01 | Implement the existing 13 pure S3 contract tasks | S3 | C | ASTRO-F01 |
| ASTRO-A01 | Qualify Windows binding source | S3 | A | ASTRO-F01 |
| ASTRO-A02 | Freeze native host qualification harness | S3 | A | ASTRO-A01, ASTRO-C01 |
| ASTRO-A03 | Qualify PTY display adapter | S3 | A | ASTRO-A01 |
| ASTRO-A04 | Qualify one Brain parser/retrieval profile | S4-G | A | ASTRO-F01 |
| ASTRO-A05 | Qualify one worker/harness route | S6-AH | A | ASTRO-F01 |
| ASTRO-A06 | Qualify policy evaluation machinery | S6-N | A | ASTRO-F01 |
| ASTRO-A07 | Qualify first assurance producers | S3-D/S7 | A | ASTRO-F01 |
| ASTRO-A08 | Qualify change and recovery mechanisms | S9-P | A | ASTRO-F01 |
| ASTRO-A09 | Freeze acquisition records for later profiles | S5-S10 profiles | A | ASTRO-F01 |
| ASTRO-F02 | Implement deterministic assurance evidence seed | S3-D | I | ASTRO-C01, ASTRO-A07 |
| ASTRO-F03 | Implement versioned source facts for one language | S4-G | I | ASTRO-A04, ASTRO-F02 |
| ASTRO-F04 | Implement access-checked ContextPackage assembly | S4 | I | ASTRO-F03, ASTRO-T01 |
| ASTRO-F05 | Freeze first-loop runtime contract manifest | S5/S6 | D | ASTRO-C01, ASTRO-A05, ASTRO-T01 |
| ASTRO-F06 | Implement effect-time authority seam | S6-N | I | ASTRO-C01, ASTRO-A06, ASTRO-T01, ASTRO-F05 |
| ASTRO-F07 | Implement exact-outcome completion evaluator | S8 | I | ASTRO-F02, ASTRO-R01, ASTRO-Q01, ASTRO-S01, ASTRO-U04 |
| ASTRO-F08 | Implement first-loop recovery checkpoint | S9-P | I | ASTRO-A08, ASTRO-F06, ASTRO-F07 |
| ASTRO-X01 | Qualify native owned-process host | S3 | I | ASTRO-A02 |
| ASTRO-X02 | Implement bounded observation and PEP adapter | S3 | I | ASTRO-X01, ASTRO-C01 |
| ASTRO-X03 | Implement one owned spawn/cancel route | S3 | I | ASTRO-X02, ASTRO-A03 |
| ASTRO-U01 | Persist task attempts and resume state | S6 | I | ASTRO-F05, ASTRO-F06 |
| ASTRO-U02 | Adapt one qualified worker through UWC | S6-AH | I | ASTRO-U01, ASTRO-X03, ASTRO-A05, ASTRO-F04 |
| ASTRO-U03 | Assign one builder and independent reviewer | S6 | I | ASTRO-U02, ASTRO-F05, ASTRO-W01 |
| ASTRO-U04 | Implement one bounded repair cycle | S8 | I | ASTRO-U03, ASTRO-R01, ASTRO-Q01, ASTRO-S01, ASTRO-F06, ASTRO-R03, ASTRO-Q03, ASTRO-S03 |
| ASTRO-U05 | Connect the first desktop outcome loop | S9 | I | ASTRO-F08, ASTRO-R03, ASTRO-Q03, ASTRO-S03, ASTRO-U04, ASTRO-W01 |
| ASTRO-R01 | Normalize one review producer result | S7 | I | ASTRO-A07, ASTRO-F02, ASTRO-F04 |
| ASTRO-R02 | Freeze Review activation and repair handoff UI | S7 | D | ASTRO-R01, ASTRO-F06 |
| ASTRO-Q01 | Implement test plan/run/oracle contracts | S7 | I | ASTRO-A07, ASTRO-F02 |
| ASTRO-Q02 | Qualify local browser test route and Test UX | S7 | D | ASTRO-Q01, ASTRO-X03, ASTRO-F06 |
| ASTRO-S01 | Implement security coverage and finding contracts | S7-S | I | ASTRO-A07, ASTRO-F02 |
| ASTRO-S02 | Freeze Security activation and validation flow | S7-S | D | ASTRO-S01, ASTRO-F06, ASTRO-R01 |
| ASTRO-B01 | Preregister controlled benchmark protocol | S3-D | D | ASTRO-G01 |
| ASTRO-B02 | Run first-loop benchmark and recovery drill | S9 | E | ASTRO-B01, ASTRO-G02 |
| ASTRO-B03 | Qualify context and Edara improvements | S10 | E | ASTRO-B02, ASTRO-SK02 |
| ASTRO-P01 | Freeze edition-aware feature completeness | S5-S10 profiles | D | ASTRO-G01, ASTRO-A09 |
| ASTRO-P02 | Freeze onboarding and local operation profile | S1/S9 profile | D | ASTRO-P01, ASTRO-T03 |
| ASTRO-P03 | Freeze one office/artifact output profile | S5/S9 profile | D | ASTRO-P01, ASTRO-F04, ASTRO-F06 |
| ASTRO-P04 | Freeze schedule/connector/brief profile | S6/S9 profile | D | ASTRO-P01, ASTRO-U01, ASTRO-F06, ASTRO-T01 |
| ASTRO-P05 | Freeze browser/computer/text-assist profile | S6/S9 profile | D | ASTRO-P01, ASTRO-U02, ASTRO-F06 |
| ASTRO-P06 | Freeze typed architecture/design artifact profile | S4-G/S9 profile | D | ASTRO-P01, ASTRO-F03, ASTRO-F06 |
| ASTRO-P07 | Freeze meeting capture and memory profile | S5/S9 profile | D | ASTRO-P01, ASTRO-K02, ASTRO-F06, ASTRO-T01 |
| ASTRO-P08 | Freeze live voice/video tool session profile | S6/S9 profile | D | ASTRO-P01, ASTRO-U02, ASTRO-F06 |
| ASTRO-O01 | Freeze Orca worktree and parallel comparison profile | S6/S9 profile | D | ASTRO-P01, ASTRO-U03, ASTRO-F08 |
| ASTRO-O02 | Freeze session/editor/terminal productivity profile | S5/S9 profile | D | ASTRO-P01, ASTRO-U01 |
| ASTRO-O03 | Freeze remote/mobile compatibility profile | S6/S9 profile | D | ASTRO-P01, ASTRO-X03, ASTRO-T01, ASTRO-F06 |
| ASTRO-K01 | Freeze bounded deep research profile | S4/S6 profile | D | ASTRO-P01, ASTRO-F04, ASTRO-F06 |
| ASTRO-K02 | Freeze scoped memory and OKF interchange profile | S4/S10 profile | D | ASTRO-P01, ASTRO-F04, ASTRO-T01 |
| ASTRO-K03 | Freeze typed-decision adapter and calibration profile | S6/S7 profile | D | ASTRO-P01, ASTRO-A05, ASTRO-B01 |
| ASTRO-T01 | Implement local principal and team scope seam | S5/S6-N | I | ASTRO-C01 |
| ASTRO-T02 | Freeze shared Work collaboration profile | S5/S9 profile | D | ASTRO-P01, ASTRO-T01, ASTRO-F05, ASTRO-F04 |
| ASTRO-T03 | Freeze usage/budget/entitlement profile | S6/S9 profile | D | ASTRO-P01, ASTRO-T01, ASTRO-F06 |
| ASTRO-T04 | Freeze enterprise deployment and lifecycle profile | S9 profile | D | ASTRO-T02, ASTRO-T03, ASTRO-F08, ASTRO-H01 |
| ASTRO-H01 | Implement immutable capability admission manifest | S6 | I | ASTRO-A09, ASTRO-F06 |
| ASTRO-H02 | Freeze Community Hub lifecycle profile | S9/S10 profile | D | ASTRO-P01, ASTRO-H01, ASTRO-T01 |
| ASTRO-SK01 | Adapt first Matt skill with full provenance | S5 | D | ASTRO-P01, ASTRO-H01 |
| ASTRO-SK02 | Freeze Debate and skill-driven product flows | S5/S10 profile | D | ASTRO-SK01, ASTRO-F05, ASTRO-F04 |
| ASTRO-W01 | Implement one Work-to-qualified-plan transition | S5 | I | ASTRO-F05, ASTRO-F04 |
| ASTRO-R03 | Implement one qualified Review route and panel | S7 | I | ASTRO-R02, ASTRO-U02, ASTRO-A07 |
| ASTRO-Q03 | Implement local Playwright Test route and panel | S7 | I | ASTRO-Q02, ASTRO-X03 |
| ASTRO-S03 | Implement one scoped Security route and panel | S7-S | I | ASTRO-S02, ASTRO-X03, ASTRO-A07 |
| ASTRO-G02 | Qualify the executable first-loop fixture | S9 | G | ASTRO-U05, ASTRO-R03, ASTRO-Q03, ASTRO-S03, ASTRO-W01 |

Critical first-loop chain (parallel branches converge at consumers): G01 → F01 → C01 → A02 → X01 → X02 → X03 → U02 → R03/Q03/S03 → U04 → F07 → F08 → U05 → G02 → B02. U02 also needs the separately qualified S6 F06 authority seam, durable U01 and F04 context; U03 needs W01 qualified intent. S3 X02 uses its canonical test-double PEP and does not depend on full Nawat. UI/producer manifests alone cannot satisfy G02 or unlock B02. Native or authority gaps block only the dependent branch.

Verified topological order: ASTRO-G01, ASTRO-B01, ASTRO-F01, ASTRO-A01, ASTRO-A04, ASTRO-A05, ASTRO-A06, ASTRO-A07, ASTRO-A08, ASTRO-A09, ASTRO-C01, ASTRO-A02, ASTRO-A03, ASTRO-F02, ASTRO-P01, ASTRO-T01, ASTRO-F03, ASTRO-F05, ASTRO-K03, ASTRO-Q01, ASTRO-S01, ASTRO-X01, ASTRO-F04, ASTRO-F06, ASTRO-X02, ASTRO-H01, ASTRO-K01, ASTRO-K02, ASTRO-P03, ASTRO-P06, ASTRO-R01, ASTRO-T02, ASTRO-T03, ASTRO-U01, ASTRO-W01, ASTRO-X03, ASTRO-H02, ASTRO-O02, ASTRO-O03, ASTRO-P02, ASTRO-P04, ASTRO-P07, ASTRO-Q02, ASTRO-R02, ASTRO-S02, ASTRO-SK01, ASTRO-U02, ASTRO-P05, ASTRO-P08, ASTRO-Q03, ASTRO-R03, ASTRO-S03, ASTRO-SK02, ASTRO-U03, ASTRO-U04, ASTRO-F07, ASTRO-F08, ASTRO-O01, ASTRO-T04, ASTRO-U05, ASTRO-G02, ASTRO-B02, ASTRO-B03.

## Task cards

### ASTRO-G01 — Accept the exact plan revision

**Owner / slice / type:** Founder / independent reviewer; P0; acceptance gate.

**Dependencies:** NONE; fresh bootstrap.

**Purpose, in-scope output and implementation requirements:** One review record: trusted base/head/tree, scope, findings, decisions, residual gaps and acceptance or REVIEW_BLOCKED. Do not implement product code in this task.

**Contracts, donors and expected modules:** Trusted AGENTS, protected governance, this package and live GitHub; no donor. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Candidate governance tries to expand its own authority; reject it.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F01, ASTRO-B01, ASTRO-P01.

### ASTRO-F01 — Freeze current frontier and limitation carry-forward

**Owner / slice / type:** Runtime / governance; P0/S3; bounded specification / qualification manifest.

**Dependencies:** ASTRO-G01.

**Purpose, in-scope output and implementation requirements:** One authority matrix linking S2 eight limitations and each S3 task group to exact current grants, paths, native evidence and stop conditions. Preserve historical records.

**Contracts, donors and expected modules:** Spec 007 tasks and merged v71; existing project/process/effect contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Pure-contract grant must not allow host APIs, spawn, network or dependency edits.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-C01, ASTRO-A01, ASTRO-A04, ASTRO-A05, ASTRO-A06, ASTRO-A07, ASTRO-A08, ASTRO-A09.

### ASTRO-C01 — Implement the existing 13 pure S3 contract tasks

**Owner / slice / type:** Rust contracts; S3; existing authorized pure-contract implementation.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** Implement C001..C013 in canonical order, with tests and exports, only in the three already authorized paths. No host behavior or new dependencies.

**Contracts, donors and expected modules:** Spec 007 contracts/tasks; serde/serde_json already present. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Unknown input fails closed; EXECUTED without ALLOW is unconstructible; raw secret-bearing fields rejected.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-A02, ASTRO-F02, ASTRO-F05, ASTRO-F06, ASTRO-X02, ASTRO-T01.

### ASTRO-A01 — Qualify Windows binding source

**Owner / slice / type:** Runtime acquisition; S3; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One exact windows-rs package/features/version-to-commit record and minimal binding surface with mined upstream or official API oracles. No dependency addition.

**Contracts, donors and expected modules:** Historical windows-rs pin in acquisition plan; Job Objects/Windows API contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Package/features cannot be selected without MSRV, transitive/build-hook and rights evidence.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-A02, ASTRO-A03.

### ASTRO-A02 — Freeze native host qualification harness

**Owner / slice / type:** Runtime / AMAN; S3; source acquisition record.

**Dependencies:** ASTRO-A01, ASTRO-C01.

**Purpose, in-scope output and implementation requirements:** One Windows qualification fixture manifest covering owned process identity, assignment, breakaway, last-handle behavior and descendant cancellation; identify exact separately authorized execution path.

**Contracts, donors and expected modules:** Spec 007 S3-AUTH-HOST tasks and Windows source record. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Do not label process-tree containment as filesystem/network isolation; non-Windows run cannot pass.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-X01.

### ASTRO-A03 — Qualify PTY display adapter

**Owner / slice / type:** Runtime acquisition; S3; source acquisition record.

**Dependencies:** ASTRO-A01.

**Purpose, in-scope output and implementation requirements:** One portable-pty embed/wrap/alternative comparison with resize, encoding, bounded output and cancellation fixture plan. PTY remains optional.

**Contracts, donors and expected modules:** wezterm historical pin and exact selected portable-pty paths. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Immediate child kill is not descendant-tree termination.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-X03.

### ASTRO-A04 — Qualify one Brain parser/retrieval profile

**Owner / slice / type:** Fehrest.Maemar; S4-G; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** Choose Rust-first source ingestion: lexical search plus one exact syntax grammar/query set; compare precise semantic seam separately. Record external scanners and malformed-input budgets.

**Contracts, donors and expected modules:** Tree-sitter, rust-analyzer/SCIP, ripgrep/Tantivy/SQLite families in source inventory. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** No parser/scanner execution or import before rights and isolated conformance.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F03.

### ASTRO-A05 — Qualify one worker/harness route

**Owner / slice / type:** Mirefa / UWC; S6-AH; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One route dossier: exact model/provider/harness/host IDs, supported events/tools, cancel/resume behavior, gaps and exit route. Mine DeepSeek/TrueForge/Orca mechanisms without importing whole runtimes.

**Contracts, donors and expected modules:** Fresh source inventory paths; existing worker/runtime contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Missing advertised tool, changed model or unavailable local provider yields explicit unsupported/reassignment.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F05, ASTRO-U02, ASTRO-K03.

### ASTRO-A06 — Qualify policy evaluation machinery

**Owner / slice / type:** Nawat; S6-N; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One Cedar-first policy evaluation comparison, typed operation/resource schema and test oracle set; alternate OPA remains an adapter option.

**Contracts, donors and expected modules:** Cedar/OPA historical registry, existing authority/effect contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** A donor permit cannot bypass WePLD principal, scope, expiry, budget or containment checks.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F06.

### ASTRO-A07 — Qualify first assurance producers

**Owner / slice / type:** Assurance / AMAN; S3-D/S7; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One producer matrix selecting deterministic local checks first and one review/security candidate per profile; identify exact source paths, context independence and optional hosted egress.

**Contracts, donors and expected modules:** Alibaba OCR, PR-Agent, Continue, Qodo components, Cloudflare, Playwright/TestSprite/Momentic evidence. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Tool unavailable, partial scan and hosted engine source unknown remain explicit; no implied PASS.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F02, ASTRO-R01, ASTRO-Q01, ASTRO-S01, ASTRO-R03, ASTRO-S03.

### ASTRO-A08 — Qualify change and recovery mechanisms

**Owner / slice / type:** Work / Runtime; S9-P; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One Git-first workspace/evidence/external-effect recovery matrix and isolated restore fixture manifest; compare optional Jujutsu/Mergiraf mechanisms.

**Contracts, donors and expected modules:** Existing change/recovery contracts; Git/Jujutsu/in-toto/TUF source families. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Git reset must not be reported as undoing external effects or restoring evidence store.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F08.

### ASTRO-A09 — Freeze acquisition records for later profiles

**Owner / slice / type:** Capability owners; S5-S10 profiles; source acquisition record.

**Dependencies:** ASTRO-F01.

**Purpose, in-scope output and implementation requirements:** One queue of capability-selected source-mining records, each with exact need, candidate paths, rights state, test oracle and owner; unresolved baseline rows stay deferred.

**Contracts, donors and expected modules:** All baseline/new sources in SOURCE_INVENTORY; choose at profile entry. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Website/org/directory listing cannot become admitted code or proof of hosted source access.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-P01, ASTRO-H01.

### ASTRO-F02 — Implement deterministic assurance evidence seed

**Owner / slice / type:** Assurance; S3-D; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-C01, ASTRO-A07.

**Purpose, in-scope output and implementation requirements:** One deterministic-check producer envelope and exact-target coverage result with local fixtures; no model reviewer or acceptance decision.

**Contracts, donors and expected modules:** ReviewTarget/ReviewOutcome/Finding existing contracts; proposed crates/contracts/src/assurance.rs and tests/assurance_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Stale target, skipped check, missing executable and truncated output remain non-PASS.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F03, ASTRO-F07, ASTRO-R01, ASTRO-Q01, ASTRO-S01.

### ASTRO-F03 — Implement versioned source facts for one language

**Owner / slice / type:** Fehrest.Maemar; S4-G; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A04, ASTRO-F02.

**Purpose, in-scope output and implementation requirements:** One bounded Rust file ingestion adapter storing source/blob/branch identities and syntax facts; incremental rebuild and explicit unsupported files.

**Contracts, donors and expected modules:** Acquired parser record; proposed crates/core/src/brain/source_facts.rs and tests/source_facts_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Malformed file, cancelled parse and stale generation do not replace current valid facts.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F04, ASTRO-P06.

### ASTRO-F04 — Implement access-checked ContextPackage assembly

**Owner / slice / type:** Fehrest; S4; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-F03, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One package builder with lexical/syntax retrieval, provenance, scope filter, byte/token budget and omission reasons; vectors excluded.

**Contracts, donors and expected modules:** Existing ContextPackage owner; proposed crates/core/src/brain/context_package.rs and tests/context_package_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Cross-project hit, revoked source, conflicting generations, budget truncation and deleted payload.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U02, ASTRO-R01, ASTRO-P03, ASTRO-K01, ASTRO-K02, ASTRO-T02, ASTRO-SK02, ASTRO-W01.

### ASTRO-F05 — Freeze first-loop runtime contract manifest

**Owner / slice / type:** AGILLE / Runtime / Edara / Mirefa; S5/S6; bounded specification / qualification manifest.

**Dependencies:** ASTRO-C01, ASTRO-A05, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One field-ownership and transition matrix for a single Mission with bounded tasks/attempts, one route and one reviewer. Emit exact leaf module interfaces for U01/U02/U03; no universal workflow framework.

**Contracts, donors and expected modules:** Existing Spec 006 Work/intent/runtime/UWC contracts; DeepSeek/TrueForge/Orca selected evidence. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Provider session ID cannot become Mission identity; WorkSession without Mission remains valid.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F06, ASTRO-U01, ASTRO-U03, ASTRO-T02, ASTRO-SK02, ASTRO-W01.

### ASTRO-F06 — Implement effect-time authority seam

**Owner / slice / type:** Nawat / Runtime; S6-N; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-C01, ASTRO-A06, ASTRO-T01, ASTRO-F05.

**Purpose, in-scope output and implementation requirements:** One typed policy-to-enforcing-adapter seam with principal/scope/epoch/expiry/containment/budget checks and possibly-sent intent. Begin with fixture effects; actual host routes require X02/X03.

**Contracts, donors and expected modules:** Existing NawatDecision/EffectProposal/EffectResult contracts; proposed crates/core/src/authority/effect_gate.rs and tests/effect_gate_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Revocation race, unknown effective resource, stale grant and duplicate dispatch fail closed.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F08, ASTRO-U01, ASTRO-U04, ASTRO-R02, ASTRO-Q02, ASTRO-S02, ASTRO-P03, ASTRO-P04, ASTRO-P05, ASTRO-P06, ASTRO-P07, ASTRO-P08, ASTRO-O03, ASTRO-K01, ASTRO-T03, ASTRO-H01.

### ASTRO-F07 — Implement exact-outcome completion evaluator

**Owner / slice / type:** Trusted Completion; S8; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-F02, ASTRO-R01, ASTRO-Q01, ASTRO-S01, ASTRO-U04.

**Purpose, in-scope output and implementation requirements:** One deterministic acceptance evaluator joining immutable target, outcome criteria, coverage, independent evidence, findings and residual limitations. Human decision remains explicit.

**Contracts, donors and expected modules:** Existing CompletionDecision/QualityPassport contracts; proposed crates/core/src/assurance/completion.rs and tests/completion_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Green CI, reviewer agreement, merge or missing evaluator cannot complete work.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F08.

### ASTRO-F08 — Implement first-loop recovery checkpoint

**Owner / slice / type:** Work / Runtime; S9-P; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A08, ASTRO-F06, ASTRO-F07.

**Purpose, in-scope output and implementation requirements:** One versioned checkpoint/restore flow for workspace plus evidence generation; external effect ledger supports unknown/reconciled/compensated/irreversible states. No universal undo.

**Contracts, donors and expected modules:** Existing recovery/change contracts; proposed crates/core/src/recovery/checkpoint.rs and tests/recovery_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Crash during restore, target changed, secret-bearing backup and irreversible external effect.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U05, ASTRO-O01, ASTRO-T04.

### ASTRO-X01 — Qualify native owned-process host

**Owner / slice / type:** Runtime; S3; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A02.

**Purpose, in-scope output and implementation requirements:** Execute only separately granted S3-HOST tasks and capture native Windows ownership/containment results. Contract test success does not unlock this automatically.

**Contracts, donors and expected modules:** Exact Spec 007 host task paths after S3-AUTH-HOST grant; no invented path authority. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Assignment failure, reused PID, lost owning handle and detached descendant.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-X02.

### ASTRO-X02 — Implement bounded observation and PEP adapter

**Owner / slice / type:** Runtime / Nawat; S3; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-X01, ASTRO-C01.

**Purpose, in-scope output and implementation requirements:** Execute separately granted S3-OBSERVE tasks with the canonical S3 test-double PEP, observation freshness, explicit unknown and no general command execution. Full Nawat is excluded from this S3 seam; S6 integration occurs through F06/U02.

**Contracts, donors and expected modules:** Spec 007 S3-AUTH-OBSERVE; paths fixed by successor grant. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Observation changes between policy decision and use; deny or re-evaluate.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-X03.

### ASTRO-X03 — Implement one owned spawn/cancel route

**Owner / slice / type:** Runtime; S3; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-X02, ASTRO-A03.

**Purpose, in-scope output and implementation requirements:** Execute separately granted S3-SPAWN route: bounded environment/output, owned descendant cancellation and terminal receipt; PTY optional.

**Contracts, donors and expected modules:** Spec 007 S3-AUTH-SPAWN; exact grant paths, qualified bindings. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Cancel race, output flood, descendant survives parent and environment secret leak.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U02, ASTRO-Q02, ASTRO-O03, ASTRO-Q03, ASTRO-S03.

### ASTRO-U01 — Persist task attempts and resume state

**Owner / slice / type:** Mission Runtime; S6; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-F05, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One durable Attempt state machine with idempotent events, lease epoch, terminal state and restart reconciliation; one local store.

**Contracts, donors and expected modules:** Existing Runtime contracts; proposed crates/core/src/runtime/attempt.rs and tests/attempt_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Restart after dispatch with no receipt produces unknown outcome, not success or automatic retry.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U02, ASTRO-P04, ASTRO-O02.

### ASTRO-U02 — Adapt one qualified worker through UWC

**Owner / slice / type:** UWC / Mirefa; S6-AH; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-U01, ASTRO-X03, ASTRO-A05, ASTRO-F04.

**Purpose, in-scope output and implementation requirements:** One worker route exposing capability negotiation, bounded context, typed events, cancellation and explicit limitations. No fallback route.

**Contracts, donors and expected modules:** Qualified A05 record; proposed crates/core/src/workers/qualified_route.rs and tests/worker_route_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Unknown event/capability, route replacement, disconnect and rejected cancellation.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U03, ASTRO-P05, ASTRO-P08, ASTRO-R03.

### ASTRO-U03 — Assign one builder and independent reviewer

**Owner / slice / type:** Edara; S6; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-U02, ASTRO-F05, ASTRO-W01.

**Purpose, in-scope output and implementation requirements:** One assignment policy selecting minimum roles from qualified descriptors with parent budget/delegation bounds; no adaptive spawning yet.

**Contracts, donors and expected modules:** Existing topology/assignment contracts; proposed crates/core/src/runtime/assignment.rs and tests/assignment_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Same producer masquerades as independent reviewer; recursive assignment exceeds parent limits.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U04, ASTRO-O01.

### ASTRO-U04 — Implement one bounded repair cycle

**Owner / slice / type:** Mission Runtime; S8; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-U03, ASTRO-R01, ASTRO-Q01, ASTRO-S01, ASTRO-F06, ASTRO-R03, ASTRO-Q03, ASTRO-S03.

**Purpose, in-scope output and implementation requirements:** One finding-to-repair proposal, separate write grant, new Attempt, rerun affected evidence, stop on budget or nonconvergence.

**Contracts, donors and expected modules:** Existing repair/assignment contracts; proposed crates/core/src/runtime/repair.rs and tests/repair_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Reviewer suggestion alone cannot write; unrelated new changes invalidate target evidence.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F07, ASTRO-U05.

### ASTRO-U05 — Connect the first desktop outcome loop

**Owner / slice / type:** Presentation / Work; S9; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-F08, ASTRO-R03, ASTRO-Q03, ASTRO-S03, ASTRO-U04, ASTRO-W01.

**Purpose, in-scope output and implementation requirements:** Implement the minimal first-loop desktop/core bindings for open/Doctor/qualified plan/authorize/run/Review/Test/Security/repair/accept/recover, using accepted R02/Q02/S02 path manifests. Include keyboard access, cancellation and explicit unavailable states; no desktop-shell replacement. Exact UI/export paths require their own grant.

**Contracts, donors and expected modules:** Existing S1 desktop/core boundary and product flows. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Unavailable producer, revoked grant and unknown effect remain visible; accessibility and cancel path required.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-G02.

### ASTRO-R01 — Normalize one review producer result

**Owner / slice / type:** Assurance; S7; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A07, ASTRO-F02, ASTRO-F04.

**Purpose, in-scope output and implementation requirements:** One producer adapter contract and fixture corpus for file/diff evidence, severity, confidence, coverage, waived/unknown items and target identity.

**Contracts, donors and expected modules:** Alibaba structured manifests first candidate; proposed crates/contracts/src/review.rs and tests/review_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Invalid line/blob, budget-limited review and mismatched target cannot become clean outcome.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F07, ASTRO-U04, ASTRO-R02, ASTRO-S02.

### ASTRO-R02 — Freeze Review activation and repair handoff UI

**Owner / slice / type:** Presentation / Work; S7; bounded specification / qualification manifest.

**Dependencies:** ASTRO-R01, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One state/action/accessibility specification for Project > Review: target/profile/producer/egress preview, run, cancel, findings, assign, export and separately authorize repair.

**Contracts, donors and expected modules:** Feature parity Review flow; existing desktop paths selected in manifest. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Review may not install dependencies, edit, push or publish merely because enabled.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-R03.

### ASTRO-Q01 — Implement test plan/run/oracle contracts

**Owner / slice / type:** Assurance; S7; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A07, ASTRO-F02.

**Purpose, in-scope output and implementation requirements:** One TestPlan/TestRun schema and result normalizer for deterministic local runs, trace artifacts, failure classification, retry and retained oracle revision.

**Contracts, donors and expected modules:** Existing assurance owner; proposed crates/contracts/src/test_run.rs and tests/test_run_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Flaky retry, skipped test and assertion modification cannot silently produce pass.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F07, ASTRO-U04, ASTRO-Q02.

### ASTRO-Q02 — Qualify local browser test route and Test UX

**Owner / slice / type:** Assurance / Presentation; S7; bounded specification / qualification manifest.

**Dependencies:** ASTRO-Q01, ASTRO-X03, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One Playwright adapter qualification and Project > Test UI manifest; optional hosted TestSprite/Momentic remain separately qualified routes.

**Contracts, donors and expected modules:** Pinned Playwright; TestSprite/Momentic behavior evidence and exact future adapter path record. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Tunnel loss, wrong environment, browser secret trace and locator healing that weakens assertion.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-Q03.

### ASTRO-S01 — Implement security coverage and finding contracts

**Owner / slice / type:** AMAN / Assurance; S7-S; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A07, ASTRO-F02.

**Purpose, in-scope output and implementation requirements:** One coverage ledger/result schema separating confirmed, needs-validation, rejected, unsupported and omitted scope; resource/taint links remain evidence.

**Contracts, donors and expected modules:** Cloudflare report/coverage patterns plus existing security contracts; proposed crates/contracts/src/security_review.rs and tests/security_review_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Skipped risky path, missing validator and unconfirmed hypothesis do not become secure or confirmed.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F07, ASTRO-U04, ASTRO-S02.

### ASTRO-S02 — Freeze Security activation and validation flow

**Owner / slice / type:** AMAN / Presentation; S7-S; bounded specification / qualification manifest.

**Dependencies:** ASTRO-S01, ASTRO-F06, ASTRO-R01.

**Purpose, in-scope output and implementation requirements:** One Project > Security flow and isolated validation manifest: scope, data handling, threat coverage, producer, finding reproduction, separate fix proposal and explicit limitations.

**Contracts, donors and expected modules:** Existing security review policy; feature parity Security flow. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** No whole-project security claim from partial scan; candidate cannot validate itself as independent.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-S03.

### ASTRO-B01 — Preregister controlled benchmark protocol

**Owner / slice / type:** Assurance / Byan; S3-D; bounded specification / qualification manifest.

**Dependencies:** ASTRO-G01.

**Purpose, in-scope output and implementation requirements:** One dataset/route/budget/scoring/independence/contamination/stopping plan and pilot sizing method before scores.

**Contracts, donors and expected modules:** Benchmark plan arms A/B/C/D/D0; no runtime result implied. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Missing baseline or changed model makes comparison noncomparable.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-B02, ASTRO-K03.

### ASTRO-B02 — Run first-loop benchmark and recovery drill

**Owner / slice / type:** Assurance; S9; qualified experiment.

**Dependencies:** ASTRO-B01, ASTRO-G02.

**Purpose, in-scope output and implementation requirements:** One reproducible paired pilot plus held-out study sized from pilot variance, exact artifacts and independent adjudication. Report failures and uncertainty.

**Contracts, donors and expected modules:** Benchmark plan and qualified first loop. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Do not discard exhausted/failed runs or score author-generated tests as sole correctness oracle.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-B03.

### ASTRO-B03 — Qualify context and Edara improvements

**Owner / slice / type:** Byan / Edara / Fehrest; S10; qualified experiment.

**Dependencies:** ASTRO-B02, ASTRO-SK02.

**Purpose, in-scope output and implementation requirements:** One preregistered ablation at a time across retrieval and topology ladder, equal total budgets, held-out results and maintenance cost. Entry additionally requires independently accepted executable leaves and exact builds for every measured variant, including any Debate/skill variant from SK02; a manifest is not an executable treatment. Record those leaf acceptance IDs before running.

**Contracts, donors and expected modules:** Benchmark context/topology tables; Byan proposal-only learning. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** More agents or larger context without accepted gain cannot be promoted.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P01 — Freeze edition-aware feature completeness

**Owner / slice / type:** Product / capability owners; S5-S10 profiles; bounded specification / qualification manifest.

**Dependencies:** ASTRO-G01, ASTRO-A09.

**Purpose, in-scope output and implementation requirements:** One catalogue reconciliation for all ACF/ORC/EXT/ALL/TEAM rows plus unavailable public catalogues. Each feature gets edition/platform/source depth, acceptance fixture and bounded implementation leaf manifest.

**Contracts, donors and expected modules:** Feature parity and inventory; public AutoClaw catalogue gaps remain explicit. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Do not claim literal full parity from unseen skills/styles or account-only behavior.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-P02, ASTRO-P03, ASTRO-P04, ASTRO-P05, ASTRO-P06, ASTRO-P07, ASTRO-P08, ASTRO-O01, ASTRO-O02, ASTRO-O03, ASTRO-K01, ASTRO-K02, ASTRO-K03, ASTRO-T02, ASTRO-T03, ASTRO-H02, ASTRO-SK01.

### ASTRO-P02 — Freeze onboarding and local operation profile

**Owner / slice / type:** Presentation / Work; S1/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-T03.

**Purpose, in-scope output and implementation requirements:** One onboarding/recovery UX manifest covering Doctor, local/cloud route choice, workspace import, entitlements, accessibility, localization, power/background state and unsupported platforms.

**Contracts, donors and expected modules:** AutoClaw/Cline/AnythingLLM product references. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Offline mode silently calls cloud, invalid entitlement blocks local evidence access, or sleep causes duplicate run.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P03 — Freeze one office/artifact output profile

**Owner / slice / type:** Work / Presentation; S5/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-F04, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One document/report profile first with editable source, citations, export, visual validation and errors; separate spreadsheet/slides/image/audio leaves with qualified libraries and tests.

**Contracts, donors and expected modules:** AutoClaw/AnythingLLM and baseline document/media families. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Broken formula/citation/layout cannot be accepted from a successful export command alone.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P04 — Freeze schedule/connector/brief profile

**Owner / slice / type:** Work / Runtime; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-U01, ASTRO-F06, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One recurring read-only daily brief with scoped sources, timezone, deduplication, run history and missed-run policy; external writes require separate leaves.

**Contracts, donors and expected modules:** Existing automation-connections contract; Dreambeans/TrueForge/AnythingLLM behavior. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** DST duplicate, stale webhook, revoked connector and inferred commitment cannot send twice.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P05 — Freeze browser/computer/text-assist profile

**Owner / slice / type:** UWC / Runtime; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-U02, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One browser read/observe surface first, then separately granted input/actions, screenshots, text selection and form assist leaves; explicit leases and destination policy.

**Contracts, donors and expected modules:** Existing interactive-surfaces contract; AutoClaw/AnythingLLM/Playwright references. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Wrong window/account, stale screenshot, prompt injection, private network redirect and hidden capture.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P06 — Freeze typed architecture/design artifact profile

**Owner / slice / type:** Maemar / Work; S4-G/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-F03, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One Archify-style typed architecture diagram with source references, diff and editable/exported view; broader design canvas leaves follow with version/conflict semantics.

**Contracts, donors and expected modules:** Archify source anchor; existing design/diagram families. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Diagram invents source relation, inaccessible export or conflicting edit silently overwrites.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P07 — Freeze meeting capture and memory profile

**Owner / slice / type:** Work / Fehrest; S5/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-K02, ASTRO-F06, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One capture/import/transcription/search/action-proposal manifest including consent, speaker correction, retention, local/cloud routing and device-loss behavior.

**Contracts, donors and expected modules:** AnythingLLM meeting docs; exact STT/diarization candidates selected at acquisition. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Withdrawal stops capture; inferred action item cannot create authorized send/task.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-P08 — Freeze live voice/video tool session profile

**Owner / slice / type:** Runtime / UWC; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-U02, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One ADK-inspired bidi session adapter manifest with interruption, media scope, transcript policy, resumption and tool-dispatch epoch; no provider-neutral claim until tested.

**Contracts, donors and expected modules:** ADK Live experimental API reference; exact SDK pin required by A09. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Barge-in followed by stale tool call, disconnected media and automatic cloud fallback.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-O01 — Freeze Orca worktree and parallel comparison profile

**Owner / slice / type:** Work / Edara; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-U03, ASTRO-F08.

**Purpose, in-scope output and implementation requirements:** One two-worker isolated-change comparison manifest with owned worktrees, shared budget, independent review, conflict and cleanup receipts.

**Contracts, donors and expected modules:** Priority Orca source/audit anchors; existing ChangeUnit. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Worktree isolation must not imply host sandbox; cleanup outside owned paths blocked.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-O02 — Freeze session/editor/terminal productivity profile

**Owner / slice / type:** Presentation / Work; S5/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-U01.

**Purpose, in-scope output and implementation requirements:** One session queue/history/fork/edit manifest with preview of workspace rewind effects, terminal limits, diff and review navigation; no shared-work silent rewind.

**Contracts, donors and expected modules:** Orca and Cline Desktop behavior. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Editing an old message cannot silently discard another member change or active external effect.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-O03 — Freeze remote/mobile compatibility profile

**Owner / slice / type:** UWC / Runtime; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-X03, ASTRO-T01, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One authenticated remote attachment manifest with capability negotiation, epoch/cursor resume, explicit host identity, read-only fallback and disconnect policy.

**Contracts, donors and expected modules:** Priority Orca remote-wire compatibility and retained-output documents. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Absent vs null, unknown enum, stale epoch and revoked device cannot retain write access.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-K01 — Freeze bounded deep research profile

**Owner / slice / type:** Fehrest / Runtime; S4/S6 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-F04, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One Vane-inspired research loop manifest with mode budgets, source/domain filters, file/web evidence, citation snapshots, contradiction handling and cancellation.

**Contracts, donors and expected modules:** Vane exact researcher path and baseline search/doc extraction sources. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Iteration bound alone does not cap money/time; poisoned source and fabricated citation rejected.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-K02 — Freeze scoped memory and OKF interchange profile

**Owner / slice / type:** Fehrest; S4/S10 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-F04, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One namespace/claim/conflict/freshness/deletion model and loss-aware OKF round-trip manifest; learned candidates never become policy automatically.

**Contracts, donors and expected modules:** Memanto pinned README/API surface; OKF SPEC v0.2; existing Fehrest contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Foreign verified label, stale claim, deleted source and cross-team namespace cannot widen trust.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-P07.

### ASTRO-K03 — Freeze typed-decision adapter and calibration profile

**Owner / slice / type:** Mirefa / Assurance; S6/S7 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-A05, ASTRO-B01.

**Purpose, in-scope output and implementation requirements:** One Choice/Score/Noul provider schema, batch/usage receipt, playground/API/SDK integration manifest and held-out calibration/abstention fixture plan.

**Contracts, donors and expected modules:** TypeSafe official introduction/quickstart/confidence/patterns; source/SDK pin still required. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Noul has no confidence field; high confidence or malformed output cannot grant authority.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-T01 — Implement local principal and team scope seam

**Owner / slice / type:** Nawat / Work; S5/S6-N; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-C01.

**Purpose, in-scope output and implementation requirements:** One local principal/organization/team/membership/scope model with explicit epoch and role binding; no federation or multi-tenant server yet.

**Contracts, donors and expected modules:** Existing Work/Nawat contracts; proposed crates/contracts/src/principals.rs and tests/principals_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Tenant/team ID collision, role downgrade, represented principal confusion and membership revocation.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-F04, ASTRO-F05, ASTRO-F06, ASTRO-P04, ASTRO-P07, ASTRO-O03, ASTRO-K02, ASTRO-T02, ASTRO-T03, ASTRO-H02.

### ASTRO-T02 — Freeze shared Work collaboration profile

**Owner / slice / type:** Work; S5/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-T01, ASTRO-F05, ASTRO-F04.

**Purpose, in-scope output and implementation requirements:** One two-member shared project manifest for rooms, tasks, comments, review assignment, shared context, concurrent revisions and audit; no CRDT-everything architecture.

**Contracts, donors and expected modules:** TeamAI versioned resources; TrueForge tenant test ideas; existing Work contracts. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Concurrent publish conflict and private memory leak must remain visible/blocking.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-T04.

### ASTRO-T03 — Freeze usage/budget/entitlement profile

**Owner / slice / type:** Work / Nawat; S6/S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-T01, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One usage ledger and budget reservation manifest with per-person/team/project caps and transparent local/BYOK/hosted costs; commerce/pricing stays a founder launch decision.

**Contracts, donors and expected modules:** AutoClaw/TrueForge/team requirements; existing budget contract. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Child runs cannot exceed parent reservation; billing failure cannot erase user-owned local evidence.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-P02, ASTRO-T04.

### ASTRO-T04 — Freeze enterprise deployment and lifecycle profile

**Owner / slice / type:** Nawat / Work / AMAN; S9 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-T02, ASTRO-T03, ASTRO-F08, ASTRO-H01.

**Purpose, in-scope output and implementation requirements:** One deployment decision record for SSO/SCIM, private/offline registries, audit export, retention/hold/residency, backups and disaster recovery; exact deployment owner choices required before implementation leaves.

**Contracts, donors and expected modules:** Enterprise requirements; baseline identity/observability families. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Cross-tenant restore, expired federation, deletion/hold conflict and unapproved region.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-H01 — Implement immutable capability admission manifest

**Owner / slice / type:** Mirefa / Nawat; S6; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-A09, ASTRO-F06.

**Purpose, in-scope output and implementation requirements:** One versioned manifest/lock graph with tool/MCP/skill/plugin identity, rights/provenance, permissions, conformance, update delta and revocation; no arbitrary installers.

**Contracts, donors and expected modules:** Existing capability package contract; source catalogue mechanisms; proposed crates/contracts/src/capability_package.rs and tests/capability_package_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Signed malicious package, dependency substitution and permission-widening update not auto-admitted.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-T04, ASTRO-H02, ASTRO-SK01.

### ASTRO-H02 — Freeze Community Hub lifecycle profile

**Owner / slice / type:** Mirefa / Work; S9/S10 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-H01, ASTRO-T01.

**Purpose, in-scope output and implementation requirements:** One public/private catalogue lifecycle manifest: discover, compare, inspect permissions, quarantine, admit, install, update, rollback, revoke, remove, report abuse and export; publisher/reputation evidence cannot replace admission.

**Contracts, donors and expected modules:** Hub product flow; baseline MCP/skill/package registries. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Revoked publisher/version, malicious review, hidden dependency and data retention after uninstall.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** profile leaf manifests or release gate; no automatic authority.

### ASTRO-SK01 — Adapt first Matt skill with full provenance

**Owner / slice / type:** AGILLE / Mirefa; S5; bounded specification / qualification manifest.

**Dependencies:** ASTRO-P01, ASTRO-H01.

**Purpose, in-scope output and implementation requirements:** One attributed requirements-challenge skill package first; retain all 38 dispositions and create one bounded leaf per selected workflow, preserving experimental labels.

**Contracts, donors and expected modules:** All 38 pinned SKILL.md hashes; no literal debate source. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Skill text cannot override Spec Kit, authorize commands or impersonate source author.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-SK02.

### ASTRO-SK02 — Freeze Debate and skill-driven product flows

**Owner / slice / type:** AGILLE / Assurance; S5/S10 profile; bounded specification / qualification manifest.

**Dependencies:** ASTRO-SK01, ASTRO-F05, ASTRO-F04.

**Purpose, in-scope output and implementation requirements:** One Debate session manifest with proposition, evidence/counterevidence, bounded critiques, unresolved disagreements, decision and export; other skill flows use the same package/authority seam.

**Contracts, donors and expected modules:** Founder debate request; Matt research/grill/domain/review patterns. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Agent voting, eloquence or repeated identical-model opinions cannot become factual proof or acceptance.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-B03.

### ASTRO-W01 — Implement one Work-to-qualified-plan transition

**Owner / slice / type:** Work / AGILLE / Mission Runtime; S5; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-F05, ASTRO-F04.

**Purpose, in-scope output and implementation requirements:** One maintenance intent, versioned outcome criteria and qualified bounded task plan associated with a local WorkSession. Mission Runtime retains WorkSession durable identity/continuation; Work is the collaboration projection. Require clarification or reject when insufficient. No general workflow designer.

**Contracts, donors and expected modules:** Existing Work/AGILLE/Runtime field owners; proposed crates/core/src/work/qualified_plan.rs and tests/qualified_plan_v1.rs. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Ambiguous outcome criteria, stale source or missing resource scope cannot create an executable Mission.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U03, ASTRO-U05, ASTRO-G02.

### ASTRO-R03 — Implement one qualified Review route and panel

**Owner / slice / type:** Assurance / Presentation; S7; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-R02, ASTRO-U02, ASTRO-A07.

**Purpose, in-scope output and implementation requirements:** Implement one acquired producer adapter and the R02 state/action panel, including run/cancel/coverage/findings/export. Exact adapter and desktop paths must be granted from the R02 manifest first.

**Contracts, donors and expected modules:** R01 contracts and R02 exact leaf paths; A07 selected producer and egress record. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Review-only invocation cannot edit/push; unavailable or partial producer is visible.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U04, ASTRO-U05, ASTRO-G02.

### ASTRO-Q03 — Implement local Playwright Test route and panel

**Owner / slice / type:** Assurance / Presentation; S7; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-Q02, ASTRO-X03.

**Purpose, in-scope output and implementation requirements:** Implement the qualified local Playwright adapter and Q02 Test panel on a fixture web target; preserve oracle/target/environment and bounded artifacts. No hosted fallback.

**Contracts, donors and expected modules:** Q01 contracts and Q02 exact adapter/UI grant; pinned qualified Playwright acquisition. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Browser failure, timeout, flaky retry and assertion-changing repair cannot become clean success.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U04, ASTRO-U05, ASTRO-G02.

### ASTRO-S03 — Implement one scoped Security route and panel

**Owner / slice / type:** AMAN / Presentation; S7-S; bounded implementation under a future exact grant.

**Dependencies:** ASTRO-S02, ASTRO-X03, ASTRO-A07.

**Purpose, in-scope output and implementation requirements:** Implement one qualified local security producer selected by A07 with S02 UI, coverage ledger and validation state. This bounded profile does not certify whole-project security.

**Contracts, donors and expected modules:** S01 contracts and S02 exact leaf grant; selected source paths required before code. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** Unsupported language/path or missing validator stays uncovered/needs-validation, never confirmed clean.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-U04, ASTRO-U05, ASTRO-G02.

### ASTRO-G02 — Qualify the executable first-loop fixture

**Owner / slice / type:** Independent engineering reviewer; S9; acceptance gate.

**Dependencies:** ASTRO-U05, ASTRO-R03, ASTRO-Q03, ASTRO-S03, ASTRO-W01.

**Purpose, in-scope output and implementation requirements:** Demonstrate the installed Windows desktop fixture end to end with actual owned host/worker and real review/test/security producers, explicit missing coverage, repair, acceptance and recovery. Verify every implementation leaf from the first-loop manifests is accepted; a manifest cannot satisfy this gate.

**Contracts, donors and expected modules:** Exact native build, route/producer/UI leaf acceptance and U05 walkthrough evidence. Exact fresh donor commits/path hashes are in [SOURCE_INVENTORY](SOURCE_INVENTORY.md); historical anchors require repinning/qualification before actual reuse.

**Required negative test / stop condition:** No benchmark admission from documentation, mocked host effects, absent producer or unimplemented UI.

**Acceptance:** the bounded output plus every applicable common-contract obligation above. Record unexecuted/unsupported checks explicitly. **Next tasks unlocked after acceptance:** ASTRO-B02.

## C01 exact subtask sequence

The authoritative descriptions remain in [Spec 007 tasks](../../007-s3-terminal-fabric-trusted-process-ownership/tasks.md). Execute C001 ServerDescriptor; C002 HostDescriptor opt-in default false; C003 RunnerDescriptor network NONE; C004 ProcessTreeIdentity PID plus start time; C005 ContainmentCapabilityReport; C006 independent posture dimensions; C007 RuntimeCeiling intersection; C008 EnvironmentExposurePolicy; C009 closed EffectProposal; C010 unknown-fail-closed PEPDecision; C011 EffectResult bound to ALLOW; C012 EffectDependency blocking; C013 secret-safety negative surface. Preserve exact existing schema requirements and v71 checks. No host implementation, filesystem/network probing, spawn, dependency addition or Windows API use belongs to C01.

## Resume record

At every interruption persist task ID, exact branch/head/base, scope grant, source pins, changed files, completed/pending tests, review state, unknown effects, open findings and the next smallest action. Resume by refreshing live truth and comparing the record; never infer completion from a prior narrative. A provider session or chat summary is a convenience pointer, not canonical state.
