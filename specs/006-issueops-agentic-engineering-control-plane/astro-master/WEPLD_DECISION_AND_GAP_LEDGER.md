# Decisions, conflicts and remaining gates

STATUS = DEPENDENCY_OWNED_DECISION_AND_GAP_LEDGER. These recommendations preserve the identifiers of the founder decision register. RAT-01 through RAT-06 remain inherited historical ratifications; this package neither repeats nor expands them. Accepted Astro execution state is determined by canonical merge/acceptance evidence and the live task graph, not by this status line alone. See the [master](WEPLD_CANONICAL_MASTER_BUILD_PLAN.md).

## FD-WORK register

| ID | Proposed resolution and reason | Acceptance / execution gate |
|---|---|---|
| FD-WORK-001 | One Nawat authority model across local and team work; team administration cannot override the executor host's ceiling | ASTRO-T01/F06; founder accepts topology before team execution |
| FD-WORK-002 | Tenant is isolation/accounting scope, Organization is administrative ownership, Team is membership/collaboration; do not collapse them | ASTRO-T01; membership and cross-tenant negative fixtures |
| FD-WORK-003 | Preserve WorkSession, Case, Mission, Task and Attempt with separate lifetimes; retry creates an Attempt | ASTRO-F05; existing Spec 006 field owners prevail |
| FD-WORK-004 | Cross-project/repository work uses the intersection of member, task, resource and executor scopes; explicit resource expansion | ASTRO-F06/T02; cross-project read and write tests |
| FD-WORK-005 | Work remains domain-neutral; first accepted outcome is software maintenance, then research/documents/meetings profiles | ASTRO-P01; founder chooses launch breadth, not a new generic runtime |
| FD-WORK-006 | Work owns collaboration, AGILLE owns intent/planning, Runtime owns durable attempts; Edara proposes staffing | ASTRO-F05; reject duplicate orchestration state |
| FD-WORK-007 | Distinguish actor, represented principal, service identity and delegated worker; delegation can only narrow authority | ASTRO-T01/F06; confused-deputy and delegation-chain tests |
| FD-WORK-008 | Offline local work remains available within explicit unexpired grants and a declared revocation lease; no promise of instant offline revocation | ASTRO-F06/T04; founder accepts high-risk offline policy before enterprise release |
| FD-WORK-009 | Inherited access is recomputed against current policy/membership at effect time; snapshots are evidence, not permanent grants | ASTRO-F06; revocation-between-plan-and-dispatch test |
| FD-WORK-010 | Personal, Team, Work and Mission memory have explicit provenance and access boundaries; retrieval cannot widen them | ASTRO-F04/K02/T02; deletion, membership loss and cache-leak tests |
| FD-WORK-011 | Conversation/room/meeting can exist without a Mission; a transcript or inferred action item proposes work, never commits it | ASTRO-P07/T02; consent and conversion receipts |
| FD-WORK-012 | External issues, PRs, chats and calendars are revisioned observations; preserve conflicts and last refresh | ASTRO-P04; stale event and duplicate webhook tests |
| FD-WORK-013 | Retention, residency, legal hold and deletion are scoped policies with explicit precedence and export effects | ASTRO-T04; founder/deployment owner chooses actual jurisdiction and retention settings before release |
| FD-WORK-014 | First vertical: one local project, one maintenance task, one worker route, one ChangeUnit, human acceptance; measure larger strata separately | ASTRO-B01/B02; founder approves release targets after baseline measurement |
| FD-WORK-015 | Reuse requires path-level rights, behavior, maintenance, conformance and exit evidence; popularity is insufficient | ASTRO-A01..A09; acquisition decision per mechanism |
| FD-WORK-016 | Record founder's asserted permission; preserve licenses/notices and obtain the specific grant record when an import relies on broader rights | ASTRO-A01..A09; does not block original implementation or independent planning |
| FD-WORK-017 | Preserve canonical history and branch evidence; old repository is a quarry, never a directory-copy seed | ASTRO-G01/F01; migration explicitly reviewed, no branch deletion implied |
| FD-WORK-018 | Logical modules first, one local authority core; deploy separate services only for a measured boundary or requirement | ASTRO-F05/T04; deployment ADR must justify extra operational cost |

## Conflicts resolved in this proposal

| Conflict | Resolution |
|---|---|
| Frozen CURRENT_STATE vs merged S2/S3 successor policy | Fresh main and merged v71 establish the narrow current frontier; leave frozen records intact |
| “Master” filename vs canonical authority | This is a proposed extension, navigated from one master entry; protected canonical index changes need their own transition |
| ContextCapsule vs ContextPackage; receipt/grant/finding synonyms | Use profiles of existing field-owning contracts; no parallel stores |
| Autonomous coding vs independent completion | Workers propose/execute only within grants; independent evidence and acceptance remain separate |
| All donor features vs one coherent runtime | Capture behavior in profiles; select mechanisms, avoid embedding competing runtimes |
| Teams vs air gap | Organization seams are early; network services optional and cannot own local authority |
| Continue API archived=false vs README final/no maintenance | Record both; require maintained fork/adapter strategy, never assume active upstream support |
| PR-Agent vs Qodo organization | Separate source identities and commercial products; qualify each public component independently |
| OpenReview auto-fix/push vs Review UX | Separate review, dependency execution, repair and push effects |
| AutoClaw local-first marketing vs cloud/privacy terms | Show actual processing/retention/provider path; local mode cannot silently egress |
| AnythingLLM all features vs edition/platform differences | Edition-aware parity and explicit unavailable states; single-user schedules are not team authorization |
| Orca workspace isolation vs security containment | Worktrees isolate changes, not host filesystem/network/process privileges |
| Matt “debate” request vs repository contents | No literal debate skill at inspected pin; design an attributed WePLD Debate flow using critique/research mechanics |
| Automatic learning, shared rules and Hub updates vs policy | Learning/update is a candidate; re-admission before any privilege expansion |
| TypeSafe confidence vs authority | Calibration and abstention inform a consumer; sharp probability does not authorize an effect |

## Planning completeness invariant

```text
NO_UNOWNED_PLANNING_GAPS = REQUIRED
EVERY_GAP_HAS_CLASS_OWNER_TASK_EVIDENCE_STOP_CONDITION = YES
FUTURE_GATE != CURRENT_BLOCKER
RESEARCH_UNKNOWN != PERMISSION_TO_GUESS
```

A gap may remain open when it is intentionally downstream and has an explicit owner, closure task, evidence requirement and fail-closed stop condition. That is an implementation gate, not a missing plan. If a newly discovered uncertainty can change architecture, authority, security/privacy, source rights, acceptance semantics, rollback/recovery or user-visible support claims and has no owner/closure task, affected implementation stops until this ledger is extended.

## Gap register

Gap classes: CLOSED_CANONICAL is satisfied by exact canonical evidence; BLOCKER_CURRENT prevents the next bounded action; GATE_FUTURE prevents only its named release/import; LIMITATION_CARRIED is an explicit accepted historical limitation, not fixed by this plan; RESEARCH_UNKNOWN requires new evidence. Open future gates are allowed only when they are owned and cannot be silently crossed.

| Gap | Class / why it matters | Owner, closure task and evidence |
|---|---|---|
| GAP-01 independent acceptance of the Astro base plan | CLOSED_CANONICAL; ASTRO-G01 accepted the exact base-plan revision | PR #340 accepted/merged at `100d5c3c0049fd97e3a1e5d54c5cc9fcc6ca9bde`; post-merge foundation-integrity PASS. Later amendments still require their own exact-head review/acceptance but do not reopen G01 |
| GAP-02 S3 host/observe/spawn authority absent | GATE_FUTURE; v71 permits pure contracts only | Runtime/governance, ASTRO-F01/A02; separate exact-path grants before host APIs or fixtures |
| GAP-03 eight S2 limitations | LIMITATION_CARRIED; do not infer hostile-store/native safety | Runtime/AMAN, ASTRO-F01; enumerate S2-S001/S003/S005/S007/Q001/Q004/Q008/Q009 from canonical records with exact closure or retained restrictions |
| GAP-04 Windows native qualification | GATE_FUTURE; Linux or pure Rust tests cannot prove Windows ownership/containment | Runtime, ASTRO-A01/A02/A03; native CI artifact and descendant/cancellation oracle |
| GAP-05 new donor admission | GATE_FUTURE; no donor installed or executed in this planning session | Mirefa/AMAN, ASTRO-A01..A09; path/dependency/rights/test/maintenance record |
| GAP-06 baseline 402 entries include ambiguous roots, obsolete names and unmined paths | RESEARCH_UNKNOWN; inventory is not individual source audit | Acquisition, ASTRO-A01..A09; resolve only capability-selected rows, preserve rejected/unknown identities |
| GAP-07 AutoClaw full 50+ skill and 140+ style catalogues | RESEARCH_UNKNOWN; public pages do not expose every entry | Product, ASTRO-P01; edition/version catalogue or document exact unsupported coverage; no literal all-feature claim yet |
| GAP-08 closed/hosted feature internals | RESEARCH_UNKNOWN; client source does not establish service source access | Acquisition, ASTRO-P01/A09; official API/entitlement and specific source grant if copying internals |
| GAP-09 team identity, revocation, retention and legal-hold policy | GATE_FUTURE; enterprise release cannot rely on solo-user assumptions | Nawat/Work, ASTRO-T01/T04; threat tests plus deployment owner decisions |
| GAP-10 Community publisher/update trust | GATE_FUTURE; signed malicious packages remain malicious | Mirefa/AMAN, ASTRO-H01/H02; quarantine, provenance, dependency and rollback/revocation drills |
| GAP-11 meeting capture/consent and cloud transcript handling | GATE_FUTURE; platform capture and consent are distinct | Work, ASTRO-P07; visible consent/capture/retention state and tested stop/deletion |
| GAP-12 benchmark budgets and release thresholds | GATE_FUTURE; “best” lacks evidence | Assurance/Byan, ASTRO-B01/B02/B03; preregistration and blind outcome adjudication |
| GAP-13 grammar/scanner rights and parser robustness | GATE_FUTURE for Brain ingestion | Maemar, ASTRO-A04/F03; exact grammar pins, timeout/memory/malformed fixtures |
| GAP-14 semantic precision and memory completeness | RESEARCH_UNKNOWN; extraction/recall cannot imply complete knowledge | Fehrest, ASTRO-F03/F04/K02; unknown/omission coverage and contradiction tests |
| GAP-15 adapter wire and model route compatibility | GATE_FUTURE; silent fallback changes behavior/egress | Mirefa/UWC, ASTRO-A05/O03; route identity/version negotiation and explicit unsupported results |
| GAP-16 capability parity beyond public pages | RESEARCH_UNKNOWN; UI/account-only features were not exercised | Product, ASTRO-P01; record advertised/documented/inspected/executed/qualified separately |
| GAP-17 disaster recovery across evidence, workspace and external effects | GATE_FUTURE; Git rollback cannot undo external sends | Runtime/Work, ASTRO-A08/F08; separate restore/compensation/unknown-outcome drills |
| GAP-18 assurance producer independence and egress | GATE_FUTURE; more reviewers do not imply independence | Assurance, ASTRO-A07/R01/S02; producer/context/model correlation and approved export proof |
| GAP-19 broader critical/formal, runtime and binary intelligence | GATE_FUTURE; specialized toolchains/fixtures required | Assurance/Maemar, ASTRO-A09/P01; separate profile manifests; do not place on first-loop critical path |

Founder input is deferred to consequential product/deployment choices: launch breadth and measured targets (FD-WORK-005/014), organization/offline policy (001/008), concrete retention/residency/legal-hold requirements (013), and any specific import relying on an undocumented custom grant (016). Routine technical decomposition and source inspection do not require another permission question.

## Complexity removed or deferred

Do not add a second team runtime, memory database, authority service or completion vote. Avoid a graph/vector server before measurement, universal CRDT synchronization, a universal rollback promise, arbitrary self-installing agents and model-generated policy updates. Full enterprise federation, every language/parser, binary reconstruction, formal proof profiles and marketplace commerce remain scoped future gates. These requirements survive in the capability map; they do not delay the first measurable local outcome.