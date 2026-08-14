## 18. Byan Learning Boundary

Byan is non-authoritative analytics and learning. It cannot write operational truth, alter a `ReviewRule`, change an AssuranceProfile, admit memory, weaken an acceptance floor, or authorize an effect.

Before S10, benchmark corpora, annotations, outcomes, calibration data, and experiment records are ordinary governed infrastructure/evidence artifacts. They are not a deployed Byan runtime and do not justify a pre-S10 operational dependency.

At S10, Byan may consume validated, disclosure-safe snapshots of outcomes and produce `ReviewLearningCandidate` or optimization candidates with source lineage, confidence, affected populations, bias/contamination risks, expiry, and reproducibility evidence. Fehrest governs knowledge admission, AGILLE governs policy relevance, Assurance evaluates claims, and an authorized principal accepts or rejects any operational change. Feedback cannot directly retrain policy or silently mutate reviewer behavior.

---

## 19. AMAN and the Deterministic Evidence Mesh

AMAN observes and scans; Nawat authorizes. AMAN normalizes qualified deterministic producers—compiler/linter/test output, dependency and secret scans, structured and semantic diff evidence, architecture/security checks, and artifact provenance—into versioned evidence envelopes. It does not become a second policy store or a completion authority.

The mesh must preserve producer identity, exact revision/configuration, invocation, environment, raw-artifact digest, parser/normalizer version, location mapping, coverage, exit state, truncation, and limitations. A producer crash or parser failure cannot become “no findings.” Duplicate findings are fused only after retaining their independent source records and disagreements.

MonkeyCode is admitted only as `REFERENCE + BENCHMARK + NEGATIVE_ORACLE` at its inspected revision. Its observed empty-secret webhook acceptance, PR-URL/time-window deduplication, magic-message loop suppression, raw event logging, long-lived token exposure, and unavailable reviewer submodule become explicit negative tests. They are not patterns to port.

---

## 20. Desktop, Terminal, Browser, and Structured Execution

The Tauri desktop is an untrusted presentation/transport shell relative to authority-bearing Core state. Typed IPC, command allowlists, origin checks, schema validation, request identity, cancellation, and output limits are defense in depth; they do not grant authority. All effectful requests resolve to a principal, Work/Mission/Attempt, capability lease, target digest, and policy decision in the Core path.

Terminal execution is a structured executor plus PTY presentation:

- the structured path owns executable identity, arguments, working directory, environment allowlist, standard streams, exit/termination, resource limits, capability and network policy, and effect receipts;
- the PTY path provides interactive terminal semantics, resize, signals, encoding, and transcript evidence;
- shell text is untrusted input; quoting is platform-specific; terminal output is neither a protocol nor trusted evidence without normalization;
- a pane, process, worktree, PTY, or container ID never substitutes for an Attempt/principal/capability identity.

Browser or authenticated-session operations require a separate substrate class and per-effect authorization. Visible browser control, connector possession, or an existing login does not imply permission to read, disclose, mutate, publish, purchase, message, or accept. Session changes, navigation, downloads, uploads, clipboard, credentials, and remote-origin content are recorded and revalidated at effect time.

---

## 21. Windows Containment Qualification

V1.5 elevates Windows containment to P0 and explicitly names Job Objects, restricted tokens/ACL/AppContainer, HCS/hcsshim, Hyper-V/Windows Sandbox/LiteBox, and Windows APIs. Stage 3 strengthens this into an adversarial qualification, not a paper checklist. A trusted Rust path check, worktree, PTY, Tauri ACL, or process boundary is not containment of a hostile worker.

### 21.1 Required property matrix

Every proposed Windows execution profile must state and test:

1. **Principal and token confinement:** restricted token construction, integrity level, privileges, groups/SIDs, elevation/UAC behavior, service-account boundary, impersonation, child inheritance, and credential isolation.
2. **Process-tree control:** Job Object assignment before untrusted execution, nested jobs, breakaway flags, grandchildren, detached processes, shell/script hosts, GUI processes, debugger/injection surfaces, handle inheritance, termination, accounting, and race-free startup.
3. **Filesystem confinement:** canonical path and ACL behavior, junctions/symlinks/reparse points, mount/volume changes, hard links, alternate data streams, device paths, 8.3/case/Unicode normalization, UNC/network paths, TOCTOU swaps, temp locations, locks, quotas, and project-boundary escape.
4. **Network confinement:** IPv4/IPv6, TCP/UDP, DNS, loopback, local subnets, proxies, VPN interfaces, raw sockets where applicable, process identity binding, dynamic child processes, WFP lifecycle, policy-update races, telemetry, and fail-closed behavior when enforcement setup fails.
5. **Credentials and providers:** no ambient user tokens, browser/session stores, SSH/Git/cloud credentials, DPAPI material, named-provider secrets, or inherited environment secrets; only short-lived scoped leases with use receipts and revocation.
6. **IPC and kernel-object confinement:** named pipes, mailslots, RPC/COM, window messages, clipboard, shared memory, mutex/events, inherited and duplicated handles, ConPTY handles, local ports, and cross-session interaction.
7. **Resource resistance:** CPU, memory, process, thread, handle, disk, output/log, file-count, recursion, decompression/archive, fork/process, and time bombs; backpressure and bounded evidence capture.
8. **Atomic lifecycle:** enforcement is established before executable-controlled code; partial setup aborts cleanly; cancellation, crash, host restart, stale state, orphan discovery, reboot, replay, idempotent cleanup, and reconciliation are tested.
9. **Command diversity:** direct executables, `cmd.exe`, PowerShell, batch/scripts, interpreters, build tools, installers, child shells, ConPTY and non-PTY paths, unusual quoting/encoding, and executable resolution are covered.
10. **Evidence and performance:** each denial/allow decision and teardown is attributable without leaking secrets; startup, interactive latency, throughput, memory, cleanup, and degraded/failure modes are measured on supported Windows versions.

The current Codex Windows mechanisms are useful source/test oracles, not a qualified WePLD sandbox: WFP configuration may continue after failure and known URL/ConPTY smoke-test gaps must remain negative cases. WezTerm `portable-pty` is terminal plumbing, not token/job/network confinement. Tauri IPC is transport defense in depth.

`B-WIN-001` remains scoped: it blocks execution of an untrusted local Alpha worker. It does not block P0 planning, contract work, or an Alpha explicitly limited to no untrusted worker. Deterministic tooling in the trusted developer workflow is permitted only under a disclosed profile whose input-trust class is explicit; processing untrusted project content is an execution-risk class and requires evidence for that class. Founder authorization must choose bounded qualification or the no-untrusted-worker limitation before S3 exits.

---

## 22. Data, Network, Egress, and External Reviewer Policy

The Core path must function `LOCAL_ONLY`. Network access is an explicit capability, not an ambient assumption. Nawat policy binds destination/service class, data classes, purpose, payload digest or bounded derivation, identity, time, budget, retention expectation, approval, and revocation. AMAN records observations; it does not decide.

Cubic is now an actual independent reviewer in the WePLD development workflow when the governing data-egress policy permits the exact code/context disclosure. It remains non-authoritative and is not a runtime dependency. When egress is denied, unavailable, or outside the approved disclosure envelope, record `NOT_RUN_DATA_EGRESS_DENIED`, `NOT_RUN_UNAVAILABLE`, or the precise non-run reason—never `PASS` and never silent fallback.

Every external model/reviewer route records provider, operator/control plane, model/version lineage, harness and instruction stack, information sources, memory/cache/retrieval state, region where relevant, retention/training posture, tool access, fallback behavior, and exact disclosed artifact digests. Provider assertions are vendor-reported until independently verified. Secrets, customer data, private repositories, security findings, and cross-repository context default to non-egress unless explicitly authorized.

External tickets, webhook payloads, PR comments, repository content, generated output, and connector data are untrusted and possibly prompt-injecting. They cannot expand scope, capabilities, context disclosure, or acceptance criteria.

---

## 23. PR #11 — Replacement-First Supersession

Live evidence at the review window shows PR #11 open, draft, unmerged, cleanly mergeable, and one commit ahead of current `main`; its head is `68cab399748c5c103b8f96380da69fdffca4d3fe`. Its successful documentation check is evidence about that workflow, not architectural ratification. It has no independent submitted review or review thread.

The canonical direction remains **do not merge unchanged**. The corrected disposition is replacement-first:

1. produce and ratify the replacement canonical plan/records outside the PR;
2. create a durable provenance map from each useful PR #11 artifact/decision to its successor or explicit rejection;
3. preserve immutable head/base identities and any required archival reference;
4. add cross-links in the authorized governance channel; then
5. close PR #11 as superseded, only after founder authorization and only in a later mutation-authorized task.

Leaving an obsolete draft open indefinitely is not a governance mechanism. This report performs none of those GitHub mutations.

---

## 24. PR #1 — Donor Ledger, Archive, and Supersession

Live evidence shows PR #1 open, draft, unmerged, non-mergeable/dirty, with head `d5ef318468b6c35df3c14c1c5f72beb1191baf29`, 46 commits and 142 changed files. Its recorded base is stale relative to live `main`. The successful Rust check and four author remediation comments are useful evidence, not independent acceptance or authority to merge.

PR #1 remains an implementation-evidence donor, never a wholesale merge candidate. Before disposition, create a path- and concept-level salvage ledger:

| Disposition | Meaning |
|---|---|
| `KEEP_EVIDENCE` | Preserve tests, failure cases, decisions, or measurements without importing implementation |
| `PORT` | Reimplement a bounded mechanism with exact provenance/rights/tests |
| `ADAPT` | Rework a suitable component behind current contracts and controls |
| `REWRITE` | Preserve requirement/evidence but replace implementation |
