# Benchmark and assurance plan

STATUS = PROPOSED_PROTOCOL; no benchmark scores or performance claims have been produced. Tasks ASTRO-B01/B02/B03 own preregistration, first-loop evaluation and topology/context experiments.

## Primary claim and experiment

Test whether WePLD improves **independently accepted engineering outcomes per unit of total cost** for the same available intelligence. Count useful accepted outcomes, regressions, unauthorized effects, review burden and recovery success; generated tokens, agent count and green CI are not success metrics.

Use task families covering defect repair, small feature, refactor, unfamiliar/legacy repository, security-sensitive change and a deliberate no-change/clarification case. Preserve a blinded held-out set. Pair identical starting trees, task statements, tool availability, model/provider/harness revision, execution budgets and environment. Randomize order, keep contamination records and include unsuccessful/aborted runs. Freeze scoring and stopping rules before results. Report task-level evidence and uncertainty, not only an aggregate leaderboard.

| Arm | Controlled difference | Question |
|---|---|---|
| A | Raw qualified worker with the same base tools and safety constraints | Baseline available intelligence |
| B | A + AGILLE intent/specification/plan qualification | Value of clearer work definition |
| C | A + Fehrest bounded source-grounded context | Value of Project Brain |
| D | A + AGILLE + Fehrest + governed Runtime + independent assurance | Value and overhead of complete WePLD loop |
| D0 | Deterministic tooling only on tasks with a deterministic route | Whether an agent is unnecessary |

“Raw” never removes safety constraints to obtain a faster unsafe baseline. Track setup/indexing cost separately and amortized over repeated work. Do not compare a stronger model in D with a weaker one in A. Qualified route changes start a separately reported stratum.

Primary measure: proportion of tasks independently accepted against preregistered outcome criteria with zero unauthorized effects. Secondary measures: severity-weighted regressions, false completion, coverage omissions, human review minutes, wall time, input/output tokens, retrieval bytes, tool/runtime/cloud cost, peak memory/CPU, p50/p95 interactive latency, cancellation latency, recovery success and maintenance burden. Report denominators, exclusions and confidence intervals. Budget exhaustion is an outcome, not an excluded run.

## Context and organization ablations

Context ablations compare no retrieval, lexical, syntax, precise semantics and hybrid retrieval; then relevant-only vs noisy/stale/conflicting evidence. Measure recall against a known relevant set, citation correctness, stale facts, access-filter leaks, token utility, omission transparency and downstream acceptance. “Memory completeness” means declared source/coverage/freshness bounds, not omniscient recall. Test branch/time switches and deleted or revoked content in caches and embeddings.

Edara topology ladder, enabled only when the preceding level has measured benefit under equal total budgets:

| Level | Topology | Required comparison |
|---|---|---|
| 0 | One worker, deterministic route where possible | Baseline |
| 1 | One worker with role-separated phases | Does structure help without concurrency? |
| 2 | Builder plus independent reviewer | Accepted gain vs review cost/correlation |
| 3 | Small bounded specialist team | Marginal gain vs duplicated work and coordination |
| 4 | Supervisor with bounded delegation | Failure recovery and narrow scope preservation |
| 5 | Multiple candidate solutions with independent comparison | Diverse outcomes, blind adjudication, no majority-vote authority |
| 6 | Adaptive topology selected from qualified previous levels | Held-out benefit, budget stability and no self-expanding permissions |

Freeze model identity, workload and budget per comparison. Stop expansion when gain is below preregistered practical significance or safety/cost worsens. Debate measures evidence quality, resolved uncertainty and downstream decisions; eloquence or number of turns does not score. Agents must expose unresolved disagreement and sources.

## Qualification matrix

| Suite | Positive evidence | Required failure / negative evidence | Gate |
|---|---|---|---|
| S3 pure contracts | Existing C001..C013 examples and round trips | Unknown fields/enums, bounds, secret-safe display and scope mismatch | ASTRO-C01 |
| Windows ownership | Owned parent/descendant identity, cancellation completion | Breakaway, PID reuse, restart, inherited handles, partial observation | ASTRO-A02 |
| Brain and context | Source/blob/branch lineage and bounded package | Stale index, parser failure, malicious document, missing coverage, revoked membership | ASTRO-F03/F04 |
| Durable effects | Fenced dispatch and reconciled receipts | Crash before/after send, duplicate callback, unknown outcome, revoked grant | ASTRO-F06 |
| Review | Exact target, evidence-backed finding and producer scope | No coverage, stale review, correlated producers, inability to review | ASTRO-R01/R02 |
| Test | Reproducible test intent, environment, oracle and trace | Flake, timeouts, target drift, tunnel loss, locator repair weakening assertion | ASTRO-Q01/Q02 |
| Security | Threat-to-test coverage with independently validated findings | Excluded files, missing evaluator, needs-validation, secret-tainted export | ASTRO-S01/S02 |
| Repair/completion | Separate repair grant and current evidence | Nonconvergence, new regression, changed outcome criterion, absent reviewer | ASTRO-F07 |
| Recovery | Workspace + evidence generation restore and external reconciliation | Interrupted migration, changed destination, irreversible send, divergent backup | ASTRO-F08 |
| Research | Snapshot-backed claims, contradictions, query/citation lineage | Fabricated citation, poisoned page, paywall/denied source, stale report | ASTRO-K01 |
| Memory/OKF | Round trip with declared semantic losses | Foreign verification, deleted source, conflict, unknown schema | ASTRO-K02 |
| Typed decisions | Held-out reliability curve/Brier or proper scoring measure, abstention | Distribution shift, overconfidence, malformed type, wrong model version | ASTRO-K03 |
| Teams | Simultaneous edits, scoped sharing, audit and accepted change | Tenant collisions, invite abuse, role downgrade, offline revocation, concurrent publish | ASTRO-T01/T02/T04 |
| Hub/packages | Reproducible pinned install and removal | Dependency substitution, permission expansion, revoked publisher, malicious signed content | ASTRO-H01/H02 |
| Meetings/live | Capture/stop state, transcript provenance, turn interruption | Withdrawn consent, cloud routing error, device loss, queued tool after interrupt | ASTRO-P07/P08 |
| Office/design | Editable deliverable, visual render and accessibility | Broken formula/link, missing citation, layout clipping, unsupported export | ASTRO-P03/P06 |
| Browser/computer | Qualified surface, input lease and target action | Stale screenshot, wrong window/account, injected content, unexpected navigation | ASTRO-P05 |
| Scheduling/connectors | Timezone-aware intent, history, deduplication | DST/clock jump, revoked connector, missed run and unknown external result | ASTRO-P04 |
| Remote/worktrees | Version negotiation, change isolation and explicit resume | Stale host, ambiguous cleanup, old cursor, network partition | ASTRO-O01/O03 |

Each feature ID in [feature parity](FEATURE_PARITY_AND_PRODUCT_FLOWS.md) must acquire a version/platform/edition-specific acceptance fixture under its named task. Marketing parity remains PARTIAL until the full visible catalogue has been mapped and executed; missing account-only catalogues remain explicit gaps. Test fixtures include keyboard-only navigation, accessible names/status, cancellation, unsupported state and data export/deletion for applicable UI flows.

## Release and evidence rules

ASTRO-B01 freezes dataset hashes, exact routes, environments, seeds, budgets, scoring rubric, reviewer independence and confidence method. Start with a feasibility pilot, use its variance to size the held-out study, and report the pilot separately. Founder/product acceptance sets practical effect thresholds before the held-out run. Zero observed unauthorized effects is a release gate, not a proof of impossible failure.

Current architecture remains Windows-first; qualification of Linux/macOS/web/mobile is separately named. An unexecuted Windows test is NOT_RUN, not PASS from cross-compilation. First-loop gates precede breadth claims. Tenant isolation, package revocation and recovery failures block their corresponding release even when feature demos work.

Benchmark artifacts record exact code/spec/target hashes, config, model/provider/harness identity, source package generations, hardware/OS, test data, logs, omissions, reviewer identities/qualification, findings and acceptance decision. Publish only approved/redacted evidence. Keep internal canaries and private workloads out of public leaderboards. Byan may propose optimizations after these experiments; it cannot change the scoring rules or authority to improve its apparent score.

## Local intelligence capability promotion matrix

The cross-cutting local intelligence amendment adds capability-specific measurements without creating a second benchmark authority. ASTRO-B01/B02/B03 remain the owners of comparative claims. Owning profile tasks may run bounded preregistered qualification experiments whose raw evidence later feeds B02/B03.

| Capability | Baseline / treatment | Primary measures | Required failure / negative cases | Promotion rule |
|---|---|---|---|---|
| OCR/document intelligence | native deterministic extraction first; qualified local OCR/document model second; external product only as benchmark reference | text accuracy, reading order, table/form structure where claimed, page/span/bbox traceability, Arabic/English/mixed-direction quality, hallucination/omission rate, latency/page, RAM/VRAM | degraded scan, malformed/oversize PDF/image, hidden instruction text, parser/model cancellation, unsupported hardware | promote a local route only after exact source/model/runtime qualification and preregistered quality/resource thresholds; OCR output remains derived projection |
| Retrieval/RAG | exact/lexical; structured/symbol/graph; + vector; + reranker | evidence recall, citation precision, no-answer abstention, stale/revoked exclusion, refresh-generation correctness, latency/index cost | poisoned source, access revocation, tombstone, stale index, conflicting exact fact, cross-scope collision | vector/rerank only if incremental value is material for named query classes over simpler qualified signals |
| Scoped memory | source-backed facts/no durable memory; governed durable memory | retrieval usefulness, provenance completeness, conflict/correction handling, deletion propagation, scope isolation | poisoned instruction, cross-project/tenant retrieval, deleted record in cache, foreign verified flag, unknown schema | promote only with correction/retraction, access and rebuild/recovery evidence; memory never becomes policy |
| Typed decisions / PLD | deterministic rule where available; general model baseline; each qualified decision route | accuracy, Brier/proper score, NLL when applicable, reliability/calibration, selective risk, abstention coverage, OOD confidence, latency/resources | malformed type, wrong model revision, route/quantization change, adversarial OOD high confidence | calibration is route-specific; no promotion without held-out reliability and abstention; result cannot grant |
| Tool/skill routing | manual/direct tool choice; Mirefa qualified routing | accepted task success, wrong-tool selection, invocation latency, requested permission breadth, human intervention | malicious metadata, broader secret/effect request, revoked package, version expands permissions | promote only through H01 admission and F06 effect enforcement; catalog success never implies authority |
| Browser/web acquisition | deterministic browser/API path; semantic AgentQL-style route where useful | extraction/task success, target identity, citation/source fidelity, latency, navigation/effect error rate | hidden prompt injection, redirect/DNS escape, stale DOM, credential forwarding, cancelled submit | semantic interaction must not weaken target/effect checks; network destination and action receipt remain explicit |
| Desktop/terminal interaction | direct user/manual operation; qualified UWC route | target correctness, stale-state rejection, cancel behavior, process ownership, effect receipts | focus/window swap, stale screenshot, secure field, shell indirection, descendant process | no promotion until current observation binding and Nawat-enforced effects are demonstrated; worktree/PTY are not containment |
| Event intelligence | raw event inbox/manual triage; normalized/triaged Action Cards | dedupe precision, stale-event detection, triage usefulness, action proposal correctness, latency | replay, connector revocation, conflicting provider revision, high-confidence wrong triage | ActionCard remains proposal; effect requires fresh authorization and idempotent/reconciled dispatch |
| Hardware/model routing | fixed route baseline; Mirefa hardware-aware route | success, latency, memory/VRAM, energy/resource pressure where measurable, fallback/reassignment visibility | unavailable accelerator, insufficient VRAM, runtime mismatch, LOCAL_ONLY route failure | prefer deterministic/no-model route when better; no silent hosted fallback; unsupported state is valid |

### Shared preregistration fields

Every capability experiment that supports a release/promotion claim records before the measured run:

```text
question / claim
task/corpus inclusion and exclusion
frozen source/model/tool revisions
hardware / OS / runtime
route identity and quantization
treatment arms
primary measure
secondary measures
thresholds
resource/time/token budget
retry policy
invalid-run policy
abstention/unsupported accounting
artifact digests
adjudication method
privacy/egress state
```

Post-result reruns are diagnostic evidence and must not silently replace the preregistered primary measurement.

### Donor-specific qualification obligations

The 2026-09-23 source additions contribute reusable mechanisms and upstream measurements, not WePLD PASS evidence.

| Donor | Upstream evidence to mine | WePLD qualification requirement |
|---|---|---|
| `mizorewww/laya-coreml@4619e0483f07adf39068532e85b42ec2347edb83` | Core ML/ANE latency and energy evidence, conversion fidelity, repeated-call stability, calibration-temperature clamp behavior | Re-run on WePLD-owned corpus and supported Apple hardware; verify raw-vs-clamped confidence, route identity, offline/cache behavior, token limits, memory/energy and OOD abstention. Upstream benchmark numbers remain historical evidence only |
| `caio0452/jev_search@ea073f6db48f5bff73ae4b9f2240d2d302fb9dc1` | two-phase file prioritization, chunking, concurrent decision filtering, progressive results | Compare against lexical/structured baseline and the same scheduler with qualified local decisions; measure evidence recall, false exclusions, latency, files/chunks evaluated, cancellation and no-network LOCAL_ONLY route. OpenRouter is never the control-plane default |
| `unreallabsai/unreal-agent@df8b0ba560da17fd705d941cbeb75eff86c74a1e` | input idempotency, session persistence/forks, pure tool translation, serializable operations, retry/cancellation tests | Fault-inject duplicate inputs, crash/restart, interrupted operation commit, cancellation, provider retry hints and stale session versions; prove WePLD Runtime/UWC/Nawat semantics remain authoritative |
| `mrmps/classifier-dev@8f2bb2b84a0d51ad1c9ed3436b64155908354f75` | classification/packing, confidence, multi-label, escalation/fallback, eval corpus and CLI/SDK/MCP surfaces | Reuse/adapt evaluation harness against local and controlled-egress routes; report accuracy/F1, Brier/NLL/reliability, selective risk, fallback frequency, route changes, batch limits, latency/resource cost and privacy/egress. Hosted service results cannot certify a local route |

```text
UPSTREAM_BENCHMARK != WEPLD_BENCHMARK_PASS
README_CLAIM != ACCEPTANCE_EVIDENCE
DONOR_TEST_PASS != WEPLD_CONFORMANCE_PASS
SAME_MODEL_DIFFERENT_RUNTIME != SAME_CALIBRATION_PROFILE
```

### Cross-capability whole-system comparison

B02/B03 should eventually compare identical or comparable work using a **separately namespaced capability-ablation vocabulary**. These labels are not aliases for the primary experiment's canonical `A/B/C/D/D0` arms:

```text
CAP-BASE = raw worker / minimal tools
CAP-SPEC = + specification and plan
CAP-CONTEXT = + source-backed Project Brain / ContextPackage
CAP-DECISION = + calibrated decisions and qualified routing where applicable
CAP-FULL = full governed WePLD outcome loop
```

The primary experiment retains exactly:
```text
A = raw qualified worker
B = A + AGILLE
C = A + Fehrest
D = A + AGILLE + Fehrest + governed Runtime + independent assurance
D0 = deterministic tooling only where applicable
```

Do not force a capability into an arm when it is irrelevant to the task. Report marginal contribution and resource/privacy cost separately so OCR, vector retrieval, PLD, extra workers or semantic browser machinery can be removed when they do not improve accepted outcomes.