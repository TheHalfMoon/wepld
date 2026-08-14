| `RECOVERY` | Durable command/process ledger (`CommandRun` + `ProcessTreeRecord`), orphan discovery, lease revocation, kill/reconcile, idempotent cleanup, crash/reboot recovery evidence; later `Attempt` records reference these immutable execution records rather than reinterpret them |
| `EXIT` | Trusted-process foundation passes; §21 evidence supports the authorized profile or records no-untrusted-worker Alpha; all method/security/performance gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S3 implementation authorization and founder choice on Windows qualification vs no-untrusted-worker Alpha |

### 29.5 S3-D — Assurance Seed Gate (Non-Primary)

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Seed deterministic, fail-clean Assurance evidence and benchmark mechanics without creating the full Assurance product or a new authority domain |
| `USER_VALUE` | Early changes receive reproducible producer and coverage evidence before native AI review exists |
| `ARCHITECTURE_DELTA` | Adds versioned producer/evidence envelopes, ReviewTarget minimum, ReviewPlan reference, `ReviewProducerRun`, immutable `ReviewCoverage`, deterministic adapters, diff/location fixtures, fail-clean tests, and benchmark manifest/runner seed |
| `OWNER` | Assurance contracts and test infrastructure; explicitly not Byan and not the entire logical Assurance subsystem inside the TCB |
| `DEPENDENCIES` | P0-D3/D5/D6/D7, S2 artifact storage, S3 trusted deterministic execution foundation; untrusted producer execution **or trusted producers over untrusted project content** requires a profile explicitly qualified for that input/execution threat class |
| `DONORS` | Ruff, Biome, ast-grep, Difftastic, open-code-review, reviewdog, pr-agent, OpenReview, MonkeyCode and useful PR #1 fixtures, each under its exact record |
| `DISPOSITIONS` | Deterministic tools are candidates only; open-code-review/pr-agent reference; reviewdog derivation/copy requires exact-artifact legal review; OpenReview rights unknown/legal review; MonkeyCode reference/benchmark/negative oracle; inspection admits nothing |
| `TRUST` | Producers, parsers and their findings are untrusted evidence sources; only minimal envelope validation/admission/state/receipts are trusted |
| `AUTHORITY` | Producers and findings have zero mutation, verdict, completion, grant, rule or policy authority |
| `DATA` | Fixtures/corpus are evaluation data; runner is test infrastructure; coverage/run records are immutable evidence; no Byan operational knowledge |
| `NETWORK` | Deterministic route `LOCAL_ONLY`; external Cubic is governed separately by the build-workflow egress gate |
| `PLATFORM` | Windows 11 deterministic path first; exact tool/platform limitations appear in coverage; no untested cross-platform claim |
| `FAILURE` | Timeout, crash, malformed/partial output, missing tool, digest mismatch, unscanned file, parser error or denied capability yields incomplete/blocked evidence, never clean |
| `NEGATIVE_TESTS` | Interrupt/resume, unpinned tool, glob/rule conflict, binary/generated content, location drift, missing coverage, malformed producer output, false zero-findings, rejected/unlicensed import |
| `ACCEPTANCE` | Pinned replay produces equivalent evidence; every target has immutable coverage and explicit gaps; fail-clean/admission suites pass; prohibited AI/Byan/completion/repair capability absent |
| `BENCHMARKS` | D0 mechanism baseline, CORPUS-C0 fixtures, runner reproducibility, evidence size, CPU/memory/I/O/latency and failure-state truthfulness |
| `NON_GOALS` | AI review, Byan, Trusted Completion, repair, ReviewSynthesis/Tour as canonical truth, independent reviewer topology, broad Assurance TCB |
| `DEFERRED` | Full native review to S7, repair/completion to S8, Byan to S10, rich ReviewTour projection |
| `EXPECTED_PATHS` | `crates/assurance/contracts/**`, `crates/assurance/producers/**`, `tests/assurance/fixtures/**`, `benchmarks/review/**`; explicitly no `crates/byan/**` ownership |
| `MIGRATION` | Evidence/coverage envelopes version from first emission; immutable records are superseded, never rewritten; producers remain replaceable |
| `RECOVERY` | Resume only from exact target/manifest/checkpoint digests; discard or quarantine unverifiable partial output; retain failure evidence |
| `EXIT` | Only the permitted seed exists; all method, component, deterministic, fail-clean, reproducibility, data and authority-negative gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—specific non-primary gate authorization plus component-specific S3-D admissions |

### 29.6 S4 — Fehrest Minimum / Project Brain Bootstrap

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Build deterministic, provenance-bearing local project context sufficient for later planning, work and review |
| `USER_VALUE` | Files, symbols, requirements, ADRs, tests and evidence can be found with freshness and source links rather than guessed |
| `ARCHITECTURE_DELTA` | Adds files/Git/exact-text index, qualified symbol/reference adapters, requirement/ADR/evidence links, retrieval manifests and deterministic ContextCapsule inputs |
| `OWNER` | Fehrest owns admission/retrieval/provenance/freshness; source systems remain authoritative; consumers own their decisions |
| `DEPENDENCIES` | S2 identity/storage; S3/S3-D evidence and deterministic execution where applicable; final Maemar relationship decision |
| `DONORS` | gix, language-server/Tree-sitter and local-index patterns, plus useful PR #1 indexing evidence after exact audit |
| `DISPOSITIONS` | `REFERENCE`, `PACKAGE`, or bounded `PORT` only after component/path/version/rights/security admission; reject mandatory cloud index/vector service |
| `TRUST` | Indexed source, comments, history and external objects are untrusted data; provenance/freshness/disclosure/admission policy is trusted |
| `AUTHORITY` | Fehrest retrieves and compiles; it cannot authorize, accept, mutate source, lower rigor or turn memory into truth |
| `DATA` | Local project and explicitly authorized cross-repository scopes; classification, source lineage, freshness, omission and deletion propagation retained |
| `NETWORK` | `LOCAL_ONLY`; no mandatory embeddings, hosted search, or connector contact; future egress requires explicit capability |
| `PLATFORM` | Windows filesystem and Git facts with explicit language-adapter support/limits; generated/binary/large repositories handled honestly |
| `FAILURE` | Stale, partial, unsupported, ambiguous, deleted or unavailable context is explicit and propagates to consumers |
| `NEGATIVE_TESTS` | Stale/superseded ADR, renamed symbol, unavailable dependency, generated/binary file, huge repo, injection in indexed text, provenance mismatch, source deletion/ACL change |
| `ACCEPTANCE` | Deterministic capsule digest, source links, freshness and coverage/omission ledger; rebuildable index; no context claim without provenance |
| `BENCHMARKS` | Index/full and incremental latency, query latency, memory/disk, retrieval recall/precision, freshness and C0–C5 context preparation cost |
| `NON_GOALS` | Semantic/acceptance authority, autonomous memory, universal languages, organization brain, Byan learning |
| `DEFERRED` | Broad cross-project/organization knowledge, optional semantic retrieval, connector fleet and advanced temporal reasoning |
| `EXPECTED_PATHS` | `crates/fehrest/**`, `crates/context/**`, `crates/index/**`, `crates/git/**`, `tests/fehrest/**` |
| `MIGRATION` | Versioned rebuildable index/provenance schemas; immutable source/evidence identities remain referenced; no silent re-admission |
| `RECOVERY` | Rebuild projections from sources and ledger; quarantine corrupt state; preserve immutable evidence and admission history |
| `EXIT` | Required local surfaces resolve with provenance/freshness/coverage, missing context remains explicit, and method/security/performance gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S4 authorization and ratified Maemar/Fehrest ownership relationship |

### 29.7 S5 — Spec Kit Mechanics, AGILLE, Plan Qualification, and Ponytail Sufficiency Gate

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Internalize typed specification, acceptance, risk, plan qualification and sufficiency mechanics as product capability |
| `USER_VALUE` | Work begins from clarified intent, testable acceptance, qualified plans and the smallest safe sufficient solution |
| `ARCHITECTURE_DELTA` | Adds Mission/spec/clarification/plan/task/checklist records, acceptance criteria/policy, risk profile, plan qualification and Ponytail sufficiency evidence |
| `OWNER` | AGILLE owns specification/acceptance/risk/qualification; Work owns human-governed goal aggregation; Mission Runtime owns execution lifecycle |
| `DEPENDENCIES` | S4 governed context; P0 vocabulary/ownership; external Spec Kit and Ponytail already govern the build method before S1 |
| `DONORS` | Exact pinned Spec Kit and Ponytail sources after component admission; Kiro/product planning behavior only as reference oracle |
| `DISPOSITIONS` | Port mechanics into typed AGILLE contracts; Markdown is evidence/input, never authority; port Ponytail questions/protected concerns; proprietary products reference only |
| `TRUST` | External text/artifacts and worker plans are untrusted inputs; admitted typed AGILLE records and authorized decisions carry product authority |
| `AUTHORITY` | Authorized human/role owns acceptance and any rigor reduction; model/worker/tool cannot accept, lower risk or waive protected concern |
| `DATA` | Local specification/planning artifacts with provenance, version/supersession and classification |
| `NETWORK` | `LOCAL_ONLY` by default; controlled egress only under explicit Nawat policy and disclosure record |
| `PLATFORM` | Platform-neutral contracts; Windows implementation/runtime evidence for Alpha; accessible/RTL UI for product surfaces |
| `FAILURE` | Ambiguous/contradictory intent, missing acceptance, stale plan, unqualified task or failed sufficiency remains blocked/incomplete |
| `NEGATIVE_TESTS` | Missing criterion, contradictory spec, untraceable task, worker lowers risk, Ponytail removes security/recovery/accessibility/evidence/authority, stale Markdown overrides canonical record |
| `ACCEPTANCE` | End-to-end objective→criterion→plan→task→test/evidence traceability; gaps explicit; FULL sufficiency answers; protected concerns retained |
| `BENCHMARKS` | Clarification/human burden, criterion coverage/quality, plan-defect/rework rate, task traceability, false qualification and cycle time |
| `NON_GOALS` | External Spec Kit as authority, automatic founder acceptance, dynamic workforce optimizer, generalized product-design suite |
| `DEFERRED` | Rich collaborative specification and adaptive risk/staffing beyond Alpha |
| `EXPECTED_PATHS` | `crates/agille/**`, `crates/specification/**`, `crates/qualification/**`, `crates/ponytail/**`, `tests/agille/**` |
| `MIGRATION` | External artifact mechanics map into versioned typed objects with provenance; earlier artifacts preserved and explicitly superseded |
| `RECOVERY` | Supersede plan/spec epistemically; never rewrite accepted history; requalify dependent tasks after material change |
| `EXIT` | A qualified Mission yields authorized tasks with traceable acceptance/risk/sufficiency and all method/negative/accessibility gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S5 authorization and final vocabulary/ownership ratification |

### 29.8 S6 — UWC, Mirefa Minimum, and Edara Minimum

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Execute one qualified worker route in one isolated, durable Attempt with a minimal governed ContextCapsule and bounded authority |
| `USER_VALUE` | Delegated work is visible, attributable, cancellable, reproducible and unable to expand its own scope |
| `ARCHITECTURE_DELTA` | Adds Universal Worker Contract, adapter conformance, native `Attempt`/worktree binding, Mirefa qualification/context transfer, deterministic Edara assignment and route/fallback lineage; an `Attempt` references immutable S3 `CommandRun`/`ProcessTreeRecord` execution records rather than reinterpreting or backfilling them |
| `OWNER` | Mission Runtime owns Attempts/checkpoints; UWC owns adapter contract; Mirefa qualifies routes/context; Edara assigns; Nawat grants effects |
| `DEPENDENCIES` | Qualified S3 containment for untrusted local worker, S4 context, S5 qualified plan, component admission, founder admissions decision |
| `DONORS` | delegate-skills schema/tests, Beads and agent/workforce systems as references, petgraph candidate for graph mechanics |
| `DISPOSITIONS` | delegate-skills schema/test donor only; petgraph package candidate after exact qualification; other frameworks reference/benchmark; no external workflow-server authority |
| `TRUST` | Every worker/model/adapter/harness/output is untrusted; outer launcher, policy/effect chokepoint and minimal state/evidence are trusted |
