| `R-15` | Generated/binary/unsupported file mishandled | Explicit exclusion and limitation; unsupported producer cannot claim coverage |
| `R-16` | ReviewRule glob/priority conflict | Deterministic versioned precedence or blocked rule set with record |
| `R-17` | Issue/comment/source contains injection or secrets | Treat as untrusted, redact/contain and report; cannot override instructions/scope |
| `R-18` | Repair exceeds finding/write/capability scope | Nawat denies and records; finding remains open |
| `R-19` | Reviewer/producer attempts mutation or policy change | Deny and record security event; no inferred repair authority |
| `R-20` | Verifier cannot reach exact environment | Verification blocked with limitations; never pass |
| `R-21` | Verifier exercises wrong revision/path/endpoint | Observation not counted toward target coverage |
| `R-22` | Static tests green but real selected path fails | Runtime divergence visible; completion/profile claim blocked as configured |
| `R-23` | Verification artifact missing/digest mismatch | Unsupported observation; run incomplete |
| `R-24` | “No findings” with incomplete coverage | Projection leads with gap; cannot present clean/pass |
| `R-25` | Upstack/restack mutation invalidates review | New evaluation identity; re-anchor/re-run/supersede explicitly |
| `R-26` | Check-reuse tuple differs in any relevant field | Re-run and preserve field-by-field mismatch evidence |
| `R-27` | Scan interrupted/resumed | Equivalent pinned result or disclosed divergence/partial state |
| `R-28` | AI egress denied | Local deterministic evidence continues; AI route blocked; no cloud fallback/pass |
| `R-29` | Secret reaches reviewer input | Deny route before transfer, redact and record security event |
| `R-30` | ReviewOutcome converted to CompletionDecision | Type/architecture test fails; no conversion path exists |
| `R-31` | Source contains instruction to reviewer/tool | Instruction ignored as untrusted content; injection finding where applicable |
| `R-32` | Unadmitted/malicious ReviewRule | Rule inert; admission/evidence event records rejection |
| `R-33` | One local model cannot meet independence profile | Outcome blocked/incomplete, not silently downgraded |
| `R-34` | Worker/repository asks to lower risk/profile | Reject; only authorized role can reduce with recorded rationale/residual risk |
| `R-35` | Required deterministic tool missing | Profile remains unmet/incomplete; no auto-reduction to available tools |
| `R-36` | Tool/config/environment digest differs | Block or create new declared run; never silently treat equivalent |
| `R-37` | Repair Attempts overlap write sets | Reject/serialize/replan before execution; no race by optimism |
| `R-38` | Repairer assigned acceptance-critical re-review | Reject topology where independence required |
| `R-39` | Completion attempted with open blocking finding | Block |
| `R-40` | Completion with acceptance-critical unverified coverage | Block unless authorized policy explicitly permits disclosed residual-risk decision |
| `R-41` | Sealed corpus item enters rule/context/tuning | Detect contamination; invalidate affected runs/admission |
| `R-42` | Metrics/Byan subsystem attempts unauthorized egress | Deny and record security event |
| `R-43` | Ported component imports rejected/unreviewed upstream path | Build/acquisition gate fails |
| `R-44` | Source/worktree rollback erases evidence/audit | Test fails; immutable evidence survives operational rollback |
| `R-45` | Worker/harness returns normally after tool error | Completion proposal records failure/uncertainty; no no-exception⇒complete rule |
| `R-46` | Quality parser retries exhausted | Never substitute threshold-passing default score; failure/manual review |
| `R-47` | Browser/local session already authenticated | No extra read/write/disclose/publish authority; effect still denied absent lease |
| `R-48` | Scheduled/automatic workflow skips confirmation | Effect-time authorization and freshness still required; expired/revoked lease fails |

### 32.2 Development method, acquisition, and benchmark

| ID | Adversarial case | Required result |
|---|---|---|
| `MTH-01` | Code has no Spec Kit trace | Slice gate fails; artifact gains no authority |
| `MTH-02` | Spec Kit Markdown treated as canon | Reject; typed/governed WePLD record remains authority |
| `MTH-03` | Ponytail mode absent/reduced | Gate fails; `PONYTAIL_MODE=FULL` is required |
| `MTH-04` | Sufficiency removes security/correctness/recovery/evidence/accessibility/authority | Reject regardless of apparent simplicity |
| `MTH-05` | Added worker/service lacks net accepted-outcome value | Reject topology expansion or require evidence-gated experiment |
| `MTH-06` | Cubic receives code/context without egress grant | Deny before transfer and record policy event |
| `MTH-07` | Egress denial/unavailability shown as Cubic pass | Gate fails; exact `NOT_RUN_*` state required |
| `MTH-08` | Cubic finding/approval used as mutation/completion authority | Type/authority gate fails |
| `MTH-09` | S7 silently retires Cubic | Fail until pre-registered non-inferiority/superiority evidence and founder decision |
| `MTH-10` | External build method conflated with native product capability | Reconciliation fails; producer/authority/stage must be explicit |
| `ACQ-01` | Repository license badge treated as component admission | Fail; exact path/blob/dependency/security/NOTICE record required |
| `ACQ-02` | OpenReview README “MIT” treated as operative grant | Fail; remain `RIGHTS_UNKNOWN / LEGAL_REVIEW_REQUIRED` |
| `ACQ-03` | reviewdog code/schema/fixture translated/copied without artifact review | Fail acquisition/legal gate |
| `ACQ-04` | MonkeyCode AGPL code enters proprietary tree | Fail unless separately approved compliant rights strategy; negatives remain reference |
| `ACQ-05` | OhMyAgent reviewer behavior assumed from unavailable gitlink | Fail; internals/rights/tests remain unaudited/unknown |
| `ACQ-06` | Empty webhook secret accepts event | Fail closed; secret required or endpoint disabled |
| `ACQ-07` | PR URL/time window suppresses legitimate new-head event | Fail; bind delivery/event and immutable head identity |
| `ACQ-08` | Magic text suppresses bot loop | Fail; use authenticated principal/producer provenance |
| `ACQ-09` | Raw webhook/secrets logged or token injected ambiently | Fail; minimize/redact and use short-lived least-authority lease |
| `B-01` | D0 includes AI/learned output | Arm invalid |
| `B-02` | Arms change target/budget/ground truth without disclosure | Comparison invalid or explicitly stratified |
| `B-03` | Universal monotonicity required/claimed | Analysis invalid; use floors/margins/budgets/Pareto evidence |
| `B-04` | One stochastic run decides gate | Invalid; paired repeats and uncertainty required |
| `B-05` | Aggregate/F1 hides M-03 or M-04 regression | Reject decision; safety guardrail dominates |
| `B-06` | Local/egress encoded as M-21 | Schema fails; it is a stratum, not metric family |
| `B-07` | CTX-C5 assumed superior | Invalid; compare empirically to CTX-C0–C4 |
| `B-08` | Corpus count arbitrary/underpowered | CORPUS-C2 gate fails pending power analysis |
| `B-09` | Item lacks rights/provenance/independent annotation/adjudication | Exclude from gate corpus |
| `B-10` | Sealed holdout enters operational context/rules/tuning | Contamination invalidates affected results |
| `B-11` | Cubic/native conditions differ invisibly | Record mismatch; prohibit unsupported causal/superiority claim |
| `B-12` | Benchmark/inspection treated as source admission | Acquisition gate fails |
| `B-13` | Missing/blocked route imputed as clean zero-findings | Analysis fails; preserve missingness and reason |
| `B-14` | Multiple testing/p-hacking/stopping after favorable run | Confirmatory claim rejected; apply preregistration/correction |

### 32.3 Windows containment families

The S2/S3 suite includes all §21 dimensions and, at minimum:

- token privilege/group/integrity/elevation/impersonation escape;
- Job Object breakaway, nested jobs, detached descendants, grandchildren and kill/cancel/restart races;
- symlink/junction/reparse/TOCTOU, `.git`/protected path, volume/device/UNC, ADS, long path, reserved name, case/Unicode collision;
- IPv4/IPv6, TCP/UDP, DNS, loopback, proxy/VPN/local-subnet and WFP-control-process failure/lifecycle;
- environment/browser/SSH/Git/cloud credential enumeration and unauthorized provider use;
- inherited/duplicated handles, pipes/RPC/COM/window messages, clipboard, shared memory and ConPTY escape;
- process/memory/handle/disk/file/output/decompression/time bombs and bounded logging/backpressure;
- atomic startup, partial enforcement failure, orphan/stale state, crash, reboot, idempotent teardown/reconciliation;
- direct executable, `cmd.exe`, PowerShell, scripts/interpreters/build tools/installers and unusual quoting/encoding;
- performance and evidence integrity under allow, deny, overload and degraded enforcement.

No successful trusted-path-only test can be represented as hostile-worker containment evidence.

### 32.4 False-success meta-test

For every UI/API/report state named “clean,” “pass,” “satisfied,” “complete,” or “accepted,” inject at least one missing producer, unavailable context surface, unknown independence relation, denied Cubic route, corrupted evidence artifact, expired capability, or evaluator failure. Presentation must become incomplete, blocked, failed, limited, or an explicitly authorized residual-risk state. If it remains clean, the architecture contains a false-success defect.

---

## 33. Decision Records Required Before Implementation

This V2 removes ADRs whose only purpose was to ask the founder to re-ratify already canonical technical concepts. ChangeStack and Design/Accessibility do not need new existence votes. Contract counts, corpus size and exact source imports are technical/evidence gates, not architecture plebiscites.

