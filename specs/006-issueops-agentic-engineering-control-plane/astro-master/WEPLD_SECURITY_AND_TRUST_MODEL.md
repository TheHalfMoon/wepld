# Security and trust model

STATUS = PROPOSED_TARGET_THREAT_MODEL. This is planning evidence, not a completed security scan or new executable policy. Existing canonical security and external-review policies remain controlling.

## Overview

WePLD handles private repositories, credentials, personal/organizational knowledge, worker execution, browser/media access, package installation and external effects. A malicious repository, retrieved page, skill, tool response or worker can influence planning; none may manufacture authority. Nawat authorizes effects, the enforcing adapter checks the real target and containment, AMAN supplies risk signals, and Assurance produces independently scoped evidence. Trusted Completion alone evaluates completion under the applicable acceptance policy.

Current base `765f9d4ae0588ca06b0f65cd76de16eaa8a5c246` contains S1/S2, not this target runtime. Relevant present evidence: [`state.rs:205`](../../../crates/core/src/state.rs#L205) request admission and [`state.rs:375`](../../../crates/core/src/state.rs#L375) launch validation; [`state_v1.rs:150`](../../../crates/core/tests/state_v1.rs#L150) stale-launch tests; [`project_v1.rs:399`](../../../crates/contracts/tests/project_v1.rs#L399) secret-shaped contract fixtures; [`security_sensitive_config_v1.rs:208`](../../../crates/core/tests/security_sensitive_config_v1.rs#L208) include handling; [`wepld.rs:391`](../../../crates/core/src/bin/wepld.rs#L391) bounded descriptor scan. These are specific existing controls/tests, not proof of hostile-worker containment. No S3 implementation module exists at this base.

## Boundaries and assumptions

Assets: grants and membership epochs; repository/workspace content; credentials and connection handles; source/evidence generations; private memory and transcripts; accepted findings/passports; package trust metadata; host process identity and budgets. Attackers may control a cloned repo, webpage/document, MCP server, plugin, model response, remote worker, ordinary team account or stale external event. A fully compromised OS administrator is outside first-loop containment claims; restoration and tamper visibility remain required, and this limit must be disclosed.

Boundaries are (1) presentation to local core, (2) core to worker/host, (3) context to authority, (4) project/team/tenant scopes, (5) local to external provider, (6) untrusted source/package to admitted capability, (7) observations to durable evidence and (8) review evidence to acceptance. Filesystem ownership, transport authentication and application authorization are distinct. Worktree, PTY, process Job Object, container and browser profile each need their own qualified claims.

Every effect decision records the **acting and represented principals**, resource identity, operation, scope, purpose, policy/grant and membership epochs, route identity, expiry, budget, constraints, environment/containment evidence and evidence references. The effective resource includes resolved target, redirects/aliases, nested resources, credentials and transport endpoint. Opaque command strings must not bypass operation/resource classification. Recheck at use; refusal, cancellation and unknown dispatch outcomes are durable states.

S2's eight carried limitations remain restrictions until closed. Proposed controls below are requirements, not descriptions of installed protections. Model remote code, installer/build hooks and automatic updates are untrusted execution. Secrets are handles by default; redact both logs and exports, and test indirect leakage through errors, traces, screenshots, embeddings and filenames. External reviewer export requires the existing egress policy even if the repository is public.

## Threat scenarios

Each row names attacker/entry, vulnerable trust transition, impact, proposed mitigation, negative oracle and owning tasks. The rows are threat hypotheses for qualification, not reported vulnerabilities in donor projects.

| ID / attacker and entry | Trust transition and impact | Required mitigation | Negative oracle / task |
|---|---|---|---|
| TH-01 repository instruction injection | Context becomes a grant; unauthorized command/export | Typed effect proposal, immutable scope and at-use policy | README asks to upload keys; no grant/no send; ASTRO-F04/F06 |
| TH-02 worker requests shell escape | Tool authorization becomes arbitrary host authority | Qualified containment plus command/resource constraints | Descendant/breakaway, inherited handles, shell indirection; ASTRO-A02/F06 |
| TH-03 stale/PID-reused process | Cancel targets another process | Owned process-tree identity, launch epoch and handle-based evidence | PID reuse and child outliving parent; ASTRO-C01/A02 |
| TH-04 revoked member races dispatch | Cached membership authorizes new effect | Epoch check and bounded lease; offline ceiling explicit | Revoke after plan/before dispatch; ASTRO-T01/F06 |
| TH-05 deputy/delegation escalation | Worker borrows wider principal | Actor/represented chain, narrowing grants, separate connection scope | Delegate project A then target B; ASTRO-T01/F06 |
| TH-06 tenant/project identifier collision | One scope retrieves another's evidence | Scope-qualified keys, access filter at retrieval and export | Same IDs in two tenants, search/cache/export; ASTRO-T01/F04 |
| TH-07 poisoned memory or foreign OKF verification | Imported claim becomes trusted fact/policy | Provenance, confidence vs verification separation, correction lineage | Imported verified=true cannot grant/overwrite verified local fact; ASTRO-K02 |
| TH-08 malicious URL/DNS/redirect | Research reaches internal service/metadata/credential endpoint | Destination checks at resolution/redirect/connect; size/time/MIME limits | Rebinding, IPv6/local encodings, redirect to loopback; ASTRO-K01/P05 |
| TH-09 webpage or tool hidden instruction | Browser/connector output triggers unrelated effects | Source/role taint, scoped tool capability, explicit form/send target | Page tells worker to reveal clipboard; ASTRO-P05/F06 |
| TH-10 provider substitution | Local/private task silently exits host | Exact model/provider/harness route; explicit user reassignment | Local model unavailable must fail/degrade visibly; ASTRO-A05/F05 |
| TH-11 token exfiltration via logs/artifacts | Safe UI hides unsafe export | Handle-based secrets, minimization and export screening | Canary in exception/trace/screenshot; ASTRO-S01/T04 |
| TH-12 malicious package/update | Signed/listed package gains ambient permission | Quarantine, immutable dependency graph, conformance, scoped admission | Valid signature with new network permission; re-admission required; ASTRO-H01/H02 |
| TH-13 source/build/grammar remote code | Acquisition becomes unbounded execution | Inventory hooks/scanners/custom loaders; isolated qualification | Networked build hook and malformed grammar input; ASTRO-A04/A09 |
| TH-14 duplicate webhook/schedule | Replayed event creates repeated effects or charges | Authenticated trigger IDs, revision fence, budget and dispatch receipts | Duplicate/delayed event and daylight-saving boundary; ASTRO-P04 |
| TH-15 lost effect acknowledgement | Retry duplicates external send/payment/publication | Persist intent, idempotency where available, unknown-state reconciliation | Kill after send before receipt; no blind retry; ASTRO-F06/F08 |
| TH-16 stale review/check | Old green result accepts new target | Target/context/producer/environment digests and freshness | One-line post-review edit invalidates affected evidence; ASTRO-F02/F07 |
| TH-17 correlated or malicious reviewers | Repeated model agreement appears independent | Record producer/model/context independence; validate claims | Two wrappers same backend cannot become two independent votes; ASTRO-R01/S02 |
| TH-18 self-healing tests weaken assertions | Test silently adapts away real defect | Separate locator repair from oracle change; diff and approval | Broken checkout still fails despite locator repair; ASTRO-Q01/Q02 |
| TH-19 user enables Review then auto-fix/push | Read evaluation gains write authority | Separate repair/delivery proposals and grants | Review invocation cannot push even if donor can; ASTRO-R02/F06 |
| TH-20 cleanup/path traversal/symlink swap | Worktree/restore removes outside target | Resolve and fence paths, owned identities, staged recovery | Reparse/junction changes during cleanup; ASTRO-O01/F08 |
| TH-21 corrupt store or interrupted migration | Evidence rewritten/lost while UI claims current | Versioned generation/checkpoint, integrity and recovery evidence | Crash at commit/pointer swap; partial generation not current; ASTRO-F08 |
| TH-22 remote session replay/stale host | Old wire state authorizes new host action | Authenticated session, epoch/capability negotiation, fail-closed unknowns | Missing/null/unknown opcode and resumed stale cursor; ASTRO-O03 |
| TH-23 collaboration conflict | Last-writer silently loses accepted work | Revision checks, visible conflict, protected execution leases | Two editors publish against same revision; ASTRO-T02 |
| TH-24 recording without continuing consent | Meeting/media capture exceeds participant intent | Visible capture state, consent scope, stop and retention controls | Participant withdrawal/device loss; no hidden resumed recording; ASTRO-P07/P08 |
| TH-25 live tool call after interruption | Cancelled spoken intent still performs effect | Turn and dispatch epochs; interrupt acknowledgement | Barge-in at tool dispatch boundary; ASTRO-P08/F06 |
| TH-26 false high-confidence typed decision | Model score becomes security/acceptance decision | Calibration, abstention and deterministic policy ownership | Adversarial out-of-distribution high score cannot grant; ASTRO-K03 |
| TH-27 budget amplification | Subagents/tool loops exceed user limits | Parent budget reservation, depth/concurrency/time/token ceilings | Recursive spawn/retry and streaming overrun; ASTRO-F05/O01/B03 |
| TH-28 learning/analytics feedback | Accepted prior behavior becomes future permission | Proposal-only learning, held-out evaluation, human promotion | Learned policy widening never auto-admitted; ASTRO-K02/B03 |
| TH-29 selective security coverage | Clean subset reported as project secure | Coverage ledger, rejected/unknown/unsupported distinct | Excluded risky file forces partial outcome; ASTRO-S01/S02 |
| TH-30 enterprise deletion/hold conflict | Content persists invisibly or is erased against hold | Explicit precedence, payload/index/export lineage and policy-visible tombstone | Deletion during legal hold; exact retained copies disclosed; ASTRO-T04/K02 |

Priority first-loop risks are TH-01/02/03/04/05/10/15/16/19/21/27; Teams/Hub/meeting/remote profiles cannot ship before their additional rows are qualified. No count of threat rows is a claim of complete coverage.

## Severity calibration

Assess reachable actor privileges, actual data/effect scope, preconditions, likelihood, recoverability and demonstrated control bypass. Unauthorized cross-tenant secret access or arbitrary execution outside qualified containment is potentially critical; scoped sensitive data leakage or irreversible effect can be high; limited denial of service or recoverable local corruption depends on exposure and impact. A missing or untested control is a coverage gap until an attack path is established. Do not inflate severity from a scary API name, nor lower it because a model performed the action.

Security release evidence must bind scenario, exact target, environment, producer, scope, reproduction, mitigation, negative oracle and residual limitation. Confirmed findings, needs-validation candidates, rejected hypotheses, unsupported checks and accepted risk remain distinct. Independent security review complements deterministic tests; it never supplies write or acceptance authority. Builder-only review cannot close acceptance-critical gates.
