| `AUTHORITY` | Worker proposes/requests; Edara assigns; Mission Runtime records; Nawat grants/revalidates; worker cannot delegate or expand itself unless explicitly authorized |
| `DATA` | Minimum ContextCapsule, exact write/read scope, classification, provenance, secrets by lease reference, checkpoint/output/evidence refs |
| `NETWORK` | `LOCAL_ONLY` or named `CONTROLLED_EGRESS` route; no silent provider/model/harness fallback |
| `PLATFORM` | Windows containment profile required for untrusted local workers; no worktree-as-security claim |
| `FAILURE` | Timeout, crash, revocation, orphan, fallback, invalid output, overlapping effects and uncertain external effect remain durable explicit states |
| `NEGATIVE_TESTS` | Child self-delegation, grant expansion, overlapping writes, hidden fallback, context leak, unknown independence, orphan, replayed effect, credential possession treated as authority |
| `ACCEPTANCE` | One adapter passes UWC conformance; one isolated Attempt has exact lineage, caps/budget/context, cancellation/revocation/recovery and no authority expansion |
| `BENCHMARKS` | Startup/handshake, task outcome, context duplication, token/model/tool/VM costs, intervention, retries, coordination and topology overhead |
| `NON_GOALS` | Swarms, generalized workforce, adaptive optimizer, broad parallelism, native review, trusted worker completion |
| `DEFERRED` | Dynamic Edara optimizer, rich team topology, remote/cross-machine execution and multiworker economics |
| `EXPECTED_PATHS` | `crates/uwc/**`, `crates/mirefa/**`, `crates/edara/**`, `crates/mission_runtime/**`, `crates/adapters/**` |
| `MIGRATION` | Introduces durable Attempt/assignment/route/checkpoint/effect lineage; adapter versions explicit and replaceable |
| `RECOVERY` | Resume exact safe checkpoint or start a new authorized Attempt; reconcile leases/orphans/effects; never mutate prior provenance |
| `EXIT` | Single-worker topology passes conformance, containment, least-authority, cancellation, replay, recovery and economics gates |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S6 authorization, component admissions, and B-WIN-001 resolution for untrusted local worker |

### 29.9 S7 — Native Review and Assurance

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Deliver the first full WePLD-native independent, evidence-grounded review pipeline |
| `USER_VALUE` | A change receives understandable findings, immutable coverage/gaps, preserved dissent and acceptance grounding rather than a generic clean score |
| `ARCHITECTURE_DELTA` | Adds ReviewTarget/Plan/ProducerRun/Finding/Coverage/Outcome pipeline, governed rules, deterministic and AI producers, Fehrest context, risk routing, role-relative independence, validation/fusion and projections |
| `OWNER` | Logical Assurance owns review lifecycle; Fehrest supplies governed context; AGILLE supplies criteria/risk; Edara routes; minimal TCB admits/records only |
| `DEPENDENCIES` | S3-D evidence foundation, S4 context, S5 acceptance/risk and S6 qualified worker route |
| `DONORS` | open-code-review, reviewdog, pr-agent, OpenReview, MonkeyCode, deterministic tools; Cubic is actual external build reviewer and benchmark comparator |
| `DISPOSITIONS` | Apply exact ledger: OpenReview rights unknown/legal review; reviewdog derivation legal review; MonkeyCode reference/benchmark/negative oracle with unaudited OhMyAgent; no project auto-admitted |
| `TRUST` | All producer/model/parser findings and summaries are untrusted evidence; validators can also fail; trusted path validates envelopes, immutable evidence and state transitions |
| `AUTHORITY` | `ReviewOutcome != CompletionDecision`; finding/coverage/score/Cubic result grants no write, merge, release, acceptance or completion authority |
| `DATA` | Minimum disclosure-safe ReviewContextCapsule; exact target/rules/criteria/context/producer lineage; corpus kept separate from operational memory |
| `NETWORK` | `LOCAL_ONLY` and `CONTROLLED_EGRESS` are separate operational/experimental strata; every fallback and disclosure recorded |
| `PLATFORM` | Windows runtime claim with producer/platform limitations in coverage; deterministic local route always available for its admitted scope |
| `FAILURE` | Timeout, malformed output, missing context/tool, disagreement, invalid location, incomplete coverage or insufficient independence yields incomplete/blocked, never clean |
| `NEGATIVE_TESTS` | Prompt injection, secrets, self-review, shared route falsely independent, silent fallback, partial/oversized change, duplicate/conflict, stale context, false no-findings, producer/evaluator fail-open |
| `ACCEPTANCE` | Five target classes use one semantic pipeline; criterion/surface coverage and gaps immutable; roles independently qualified; findings normalized/evidenced; zero verdict/completion conflation |
| `BENCHMARKS` | D0/A/B/C/D; Cubic, WePLD-native and combined; `M-01..M-20`; `CTX-C0..CTX-C5` context; `CORPUS-C0..CORPUS-C4`; local/egress strata and full statistics |
| `NON_GOALS` | Controlled repair, Trusted Completion, generalized Runtime Verifier, automatic Cubic retirement, universal languages/tools |
| `DEFERRED` | Rich ReviewTour UX/projections, adaptive reviewer topology and generalized runtime verification |
| `EXPECTED_PATHS` | `crates/assurance/**`, `crates/review/**`, `crates/review_rules/**`, `crates/review_context/**`, `tests/review/**` |
| `MIGRATION` | S3-D envelopes evolve versionedly; immutable earlier coverage/run evidence preserved; projection schemas rebuildable |
| `RECOVERY` | Re-run producers against pinned target/plan/context; preserve prior runs/conflicts; no missing run fabricated or overwritten |
| `EXIT` | Native pipeline meets pre-registered safety floors/non-inferiority/budgets, records every limitation and passes method/authority/adversarial/accessibility gates |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S7 implementation and external-route/data-egress authorizations |

### 29.10 S8 — Controlled Repair, Bounded Fallback/Reassignment, and Trusted Completion

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Repair validated findings under separate authority, re-review independently, and decide completion only from admissible evidence and authority |
| `USER_VALUE` | Fixes are bounded, visible, recoverable and cannot self-approve; unresolved risk stays visible |
| `ARCHITECTURE_DELTA` | Adds RepairProposal, separate repair Attempt/write set, fallback/reassignment controls, re-review convergence, bounded own-surface VerificationRun and authorized CompletionDecision/receipt |
| `OWNER` | Mission Runtime owns repair Attempts; Nawat owns effects; Edara owns bounded assignment; Assurance owns re-review; Trusted Completion path owns decisions/receipts |
| `DEPENDENCIES` | S7 full review, acceptance policy, capability/effect receipts, founder Runtime Verifier scope decision |
| `DONORS` | PR #1 repair/worktree evidence and proprietary/OSS repair systems as behavior/negative oracles only after exact assessment |
| `DISPOSITIONS` | Port only bounded audited mechanics; reject direct reviewer writes, auto-approval, environment-success-as-completion and silent fallback |
| `TRUST` | Repairer, fallback worker, model and verifier are untrusted; effect chokepoint, evidence admission and completion decision/receipt are trusted |
| `AUTHORITY` | Finding proposes; Nawat separately grants exact effects; repairer cannot re-review acceptance-critical work; authorized human/policy decides completion |
| `DATA` | Attempt/worktree/change scoped; exact findings/write set/context/effects/evidence; audit survives source/worktree rollback |
| `NETWORK` | Route and fallback profiles explicit; no silent provider/model/egress change; verifier network/secrets named and bounded |
| `PLATFORM` | Windows containment/worktree/filesystem/process and selected WePLD-owned runtime surfaces only for Alpha verifier scope |
| `FAILURE` | Scope overrun, conflict, fallback, verifier unavailable/wrong target, non-convergence, open blocker, uncertain effect and exhausted retry remain explicit |
| `NEGATIVE_TESTS` | Repair exceeds finding/scope, repairer re-reviews, overlapping writes, tests green but runtime fails, wrong endpoint, missing evidence, fallback changes independence, retry exhaustion self-accepts |
| `ACCEPTANCE` | Separate least-authority Attempt, independent re-review, exact effect receipts, no partial promotion, completion impossible from worker/ReviewOutcome/verifier alone |
| `BENCHMARKS` | Repair rounds/time, convergence/regressions, M03/M04, human burden, verifier yield/cost, fallback/reassignment overhead and residual-risk outcomes |
| `NON_GOALS` | Unattended merge/release, arbitrary autonomous repair, third-party production verification, broad computer control |
| `DEFERRED` | General Runtime Verifier, generalized browser/computer use and autonomous fleet repair |
| `EXPECTED_PATHS` | `crates/repair/**`, `crates/completion/**`, `crates/verification/**`, `crates/mission_runtime/**`, `tests/trusted_completion/**` |
| `MIGRATION` | Adds repair/verification/completion lineage without rewriting review/attempt/effect evidence; state transitions versioned |
| `RECOVERY` | Revert source/worktree state while retaining Attempts, findings, effects, observations and decisions; reconcile uncertain effects before retry |
| `EXIT` | Blocking findings resolved or explicitly accepted with authorized disclosed residual risk; fail-open/self-certification tests impossible; method gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S8 authorization and Runtime Verifier Alpha-scope decision |

### 29.11 S9 — Quality Passport, Recovery Time Machine, and ChangeUnit/Delivery Evidence

| Field | Reconciled plan |
|---|---|
| `PURPOSE` | Make accepted quality, delivery lineage and recovery independently auditable for one ChangeUnit |
| `USER_VALUE` | The user can prove what was reviewed/accepted/delivered and restore safely without erasing history |
| `ARCHITECTURE_DELTA` | Adds Quality Passport, recovery checkpoint/manifests, one ChangeUnit minimum, delivery evidence, stack-family references, epistemic supersession and exact check-reuse evidence |
| `OWNER` | Passport/Recovery/Delivery modules under Core contracts; ChangeStack canonical family; Work/Mission/Assurance remain their own owners |
| `DEPENDENCIES` | S8 accepted evidence/effect/completion chain; V1.5 ChangeStack invariants; admitted storage/graph/Git mechanics |
| `DONORS` | V1.5 canonical contracts; Git Town, spr, ghstack and archived gh-stack as behavior/source evidence |
| `DISPOSITIONS` | Preserve canonical concepts; external stack tools reference unless separately admitted; archived source historical only; no hosted stack state as truth |
| `TRUST` | Passport/manifest is digest/signature-verifiable evidence; forge comments/checks/tool objects are observations; recovery executor remains capability-bound |
| `AUTHORITY` | Passport/delivery evidence records decisions; it grants no merge/release/publish authority and cannot substitute for CompletionDecision |
| `DATA` | Local append-only/content-addressed evidence, artifact/checkpoint manifests, exact ChangeUnit/revision/dependency/reuse digests |
| `NETWORK` | Offline verification required; forge publication/read is separate controlled egress/effect with current authorization |
| `PLATFORM` | Windows recovery/crash/storage semantics; forge-independent portable core format |
| `FAILURE` | Missing artifact/receipt, digest mismatch, stale stack revision, invalid reuse, interrupted restore, partial checkpoint or incompatible schema blocks claim |
| `NEGATIVE_TESTS` | Upstack mutation, restack/conflict change, mismatched reuse field, source rollback, forged passport, missing receipt, interrupted recovery, stale grant, forge unavailable |
| `ACCEPTANCE` | Complete offline-verifiable passport; independent restoration; reuse invalidates on any relevant mismatch; one ChangeUnit evidence path without premature stack UX |
| `BENCHMARKS` | Recovery time/success, passport verification latency/evidence size, reuse correctness, avoided reruns, storage overhead and failure recovery |
| `NON_GOALS` | Full ChangeStack UX, multi-unit stack optimizer, release automation and hosted forge truth |
| `DEFERRED` | Stacked-change authoring/restacking/delivery UX and advanced recovery visualization Post-Alpha |
| `EXPECTED_PATHS` | `crates/passport/**`, `crates/recovery/**`, `crates/changeunit/**`, `crates/delivery_evidence/**`, `tests/recovery/**` |
| `MIGRATION` | Versioned passport/recovery schemas; explicit supersession; immutable evidence/history never deleted or rewritten |
| `RECOVERY` | Restore source and runtime state from verified checkpoint; preserve append-only audit/evidence and reconcile external effects separately |
| `EXIT` | Passport/recovery verify independently, reuse cannot cross mismatch, crash/corruption tests pass, and method/authority gates pass |
| `FOUNDER_AUTHORIZATION_REQUIRED` | `YES`—S9 implementation authorization and any external delivery/forge effects separately authorized |

