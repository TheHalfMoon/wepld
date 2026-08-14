| `SUPERSEDE` | A later canonical artifact fully replaces it with cross-link |
| `REJECT` | Do not reuse; record reason and negative oracle if valuable |

For every kept item record source commit/path/blob digest, authoring/license provenance, affected contracts, security/privacy implications, dependencies, current relevance, validation evidence, destination, and replacement/exit plan. Preserve an archival immutable ref if required for provenance, establish durable cross-links, and then close the draft as superseded only after founder approval in a separately authorized task. No rebase, merge, branch, comment, or closure occurs here.

---

## 25. Reconciliation of Former Decisions and Blockers

Direct V1.5 inspection and the Stage-2 correction close several false or stale governance questions:

| Former item | Stage-3 status | Basis |
|---|---|---|
| Evidence access / V1.5 inspection | `CLOSED` | Full direct inspection; exact path/hash recorded in §0 |
| ChangeStack existence and lineage | `CLOSED` | Direct V1.5 §42.3 and final discovery sweep |
| Design/Accessibility Review existence | `CLOSED` | Direct V1.5 constitutional/native-review requirements |
| Core state hierarchy, Spec/AGILLE split, terminal structure, evidence-not-verdict | `TECHNICALLY_SETTLED` | Canonical architecture plus Stage-3 corrections; implement through contracts/tests |
| Assurance contract count and benchmark corpus size | `P0_TECHNICAL_WORK` | Must be designed/validated; not founder votes or external blockers |
| Independence topology and benchmark statistics | `P0_TECHNICAL_WORK` | Corrected requirements are testable design obligations |
| Source universe blanket admission | `RETRACTED` | Acquisition is component/path/version specific and incomplete |

Only the ten questions in §37 remain founder/governance decisions. Only the two scoped blockers in §38 remain current blockers.

---

## 26. Reconciled Conflict Ledger

| Conflict | Controlling resolution |
|---|---|
| Stage 1 treated V1.5 as unavailable | V1.5 is directly inspected and controls as the latest canonical reference, subject to newer explicit founder direction |
| Stage 1 treated ChangeStack lineage as unverified | Direct V1.5 §42.3 establishes it; exact implementation remains later technical work |
| Stage 1 questioned Design/Accessibility Review | Direct V1.5 retains accessibility/RTL/design assurance; close the decision |
| V1.5 has an earlier §26.1 roadmap and later §42.21 roadmap | The later final-discovery sweep controls: S1–S10, Fehrest S4, Spec Kit/AGILLE S5, first full Review/Assurance S7; Stage 3 adds non-primary S3-D |
| V1.5 benchmark arms differ from Stage-3 arms | Newer founder direction controls: D0, A raw, B governed rules, C Fehrest+AGILLE, D full topology; record the change rather than misquoting V1.5 |
| V1.5 independence list is incomplete for adversarial assurance | Preserve it as a floor and apply the role-relative Stage-3 relation graph in §10 |
| V1.5 names only part of the proposed review vocabulary | Use proposed envelopes conservatively; do not attribute new names to V1.5 or create duplicate canonical truth |
| V1.5 treats Spec Kit/Ponytail mainly as future native capability and Cubic as behavior oracle | Current founder direction additionally mandates their bounded development-workflow use now; product internalization remains later |
| Public live repository conflicts with proprietary/Private posture | `B-GOV-001`; founder-controlled containment/governance decision required before implementation publication |
| Stage 1 called OpenReview definitively license-blocked | Correct to `RIGHTS_UNKNOWN / LEGAL_REVIEW_REQUIRED`; a README assertion is not an operative grant |

---

## 27. Component Acquisition and Build-vs-Reuse Gate

`SOURCE_ACQUISITION_COMPLETENESS = PARTIAL / PREVIOUSLY_OVERCLAIMED`.

`NO_COMPONENT_IMPORT_ADMITTED` by this planning report. Repository-level licenses and reference-level study are not path-level admission. P0 must create a record for every actual S1 or S3-D component and its transitive/runtime surface before code reuse.

### 27.1 Mandatory acquisition record

Each record includes exact repository, immutable revision, selected paths and blob hashes, upstream lineage, tests/fixtures, dependencies and build scripts, license/NOTICE/attribution, advisories and security posture, platform/maintenance evidence, data/network/effect surface, intended `COPY | VENDOR | EMBED | PORT | PACKAGE | REFERENCE | REJECT` disposition, contract boundary, delta from upstream, admission/negative/performance/security tests, SBOM provenance, update/replacement/exit plan, reviewer and decision authority.

Custom machinery is permitted only for `NO_SUITABLE_COMPONENT`, `LICENSE_BLOCKED`, `SECURITY_BLOCKED`, `ARCHITECTURE_INCOMPATIBLE`, `PERFORMANCE_BLOCKED`, `PORTABILITY_BLOCKED`, or a documented `WEPLD_DIFFERENTIATOR`. “Easy to generate” is invalid.

### 27.2 Current exact-source ledger

| Source @ inspected revision | Rights/evidence state | Stage-3 disposition |
|---|---|---|
| `alibaba/open-code-review@4068a4bd25a48df12d3ec89f70adfea63151593c` | Apache-2.0 at repository level; exact candidate paths/dependencies still need admission | Path-level audit candidate; deterministic/agent orchestration reference only now |
| `reviewdog/reviewdog@d8462283c7315f1a47e8edd140aeffd0f0ca28ea` | MIT; copying/translating schema, code, or fixtures is fact-specific | RDFormat/diff-filter behavior reference; any derivation/copy is `LEGAL_REVIEW_REQUIRED` with exact blobs |
| `The-PR-Agent/pr-agent@20bc0fe8ae7c1494c0be580f7ceb35a1c45e5741` | MIT repository evidence; provider/VCS/dependency surface separate | Reference/test oracle for compression and workflow; no runtime dependency admitted |
| `vercel-labs/openreview@672deb21e70e471e0536d5ad7a67c14b8359e97e` | No operative grant established; README says MIT | `RIGHTS_UNKNOWN / LEGAL_REVIEW_REQUIRED`; behavior reference only; reject code reuse now |
| `augmentcode/context-connectors@f7d6472ae626c98fd768f64cdfd6160145eefa77` | MIT repository evidence; service dependency exists | Connector/index/ignore reference; reject Augment service dependency as Fehrest truth |
| `chaitin/MonkeyCode@12107c7bfc3bb0ef97e2fd0709411a3a6afda9cb` | AGPL-3.0; linked `OhMyAgent@a455e6f346c42cdb78c8943bbeacf935d02c5a5a` unavailable and rights unknown | `REFERENCE + BENCHMARK + NEGATIVE_ORACLE`; reject proprietary copy/vendor/embed/port absent separate approved rights strategy |
| `astral-sh/ruff@8f11b10b926b1625cf35a5babb44854e2bbd423d` | MIT repository evidence | Qualified local deterministic producer candidate; package/path admission still required |
| `biomejs/biome@40dad299ae90e045b55a219a3c0f9e6cca0e153f` | Apache-2.0 repository evidence | Qualified local deterministic producer candidate; package/path admission still required |
| `ast-grep/ast-grep@5aa00e1dd5e0077589a6c0c23c640e39947403ec` | MIT repository evidence | Semantic-query producer candidate outside minimal TCB; do not auto-embed |
| `Wilfred/difftastic@e23b7d4ff8fa1eabe8236d3b7c20ac5507c888ee` | MIT repository evidence | Structured-diff behavior/reference candidate |
| `git-town/git-town@8c5aa8834c22db5beb0ddb16fe5aa224bdd1bccf` | MIT repository evidence | ChangeStack behavior/mechanism reference only |
| `ejoffe/spr@0767a458e50fa1f7ae203b73e50298ab201c80bb` | MIT repository evidence | ChangeStack behavior/mechanism reference only |
| `ezyang/ghstack@f4e9df551eda204bc95b4329870ea304bd20fbb0` | MIT repository evidence | ChangeStack behavior/mechanism reference only |
| `timothyandrew/gh-stack@d6aa8192ed4cf905826abb2ab97c51b8aaaafa4c` | Archived; repository rights evidence must be carried in its record | Historical reference only; no dependency |
| `amElnagdy/delegate-skills@f9f2528525b820e7fd24724f87d6821c0e272947` | MIT repository evidence | UWC/schema/test donor only; never authority or runtime admission by implication |
| `petgraph/petgraph@ed714652ab4576104e506c096b6ed9f5128613a7` | MIT/Apache-2.0 repository evidence | Strong direct graph-library candidate with minimal features; transitive/admission gate remains |

Supplemental exact-revision source inspection also narrows platform reuse: Tauri remains the shell dependency and typed IPC defense in depth, not the authority kernel; Codex Windows source is a selective-port/test oracle with known fail-open/gap cases; WezTerm `portable-pty` is usable only behind a WePLD-owned launcher and containment boundary. Their actual S1/S3 admission records must capture the full inspected SHAs and exact paths before reuse; this report deliberately does not convert abbreviated audit notes into false exact pins.

### 27.3 Proprietary products

Graphite, Augment, and Cubic are product-behavior evidence and may also have separately identified source artifacts. Observation alone creates no source-acquisition right; the founder-provided authorization is a distinct rights basis and must be recorded where invoked. Every actual artifact remains individually pinned with upstream-license, third-party-rights, NOTICE/attribution, advisory and provenance lineage. No hosted object may become canonical WePLD authority.

---

## 28. P0 Founder Package and Exit Deliverables

P0 is documentation, specification, evidence, governance, and experiment design only. It authorizes no product implementation, dependency installation, source import, repository mutation, or external effect.

| ID | Deliverable | Exit condition |
|---|---|---|
| `P0-D1` | Direct V1.5 reconciliation record | Exact artifact path/hash, authority precedence, contradictions, ChangeStack, Design/Accessibility, roadmap, decisions, and blockers are traceably reconciled |
| `P0-D2` | Canonical architecture/ownership record | Final vocabulary and aggregate ownership, Maemar disposition, logical/deployable boundaries, authority graph, anti-fork invariants, UCAP owner-label resolution, and pre-Mission executor-record semantics are founder-approved; S3 uses `CommandRun`/`ProcessTreeRecord`, not a native `Attempt` |
| `P0-D3` | Minimal Assurance/Trusted Completion boundary | Semantic envelopes and transitions are specified; `ReviewCoverage` is immutable evidence; projections are distinguished; `ReviewOutcome != CompletionDecision` is mechanically testable; physical TCB is minimal |
| `P0-D4` | TCB and Windows security plan | Trusted/untrusted placement, input-trust classes, the §21 qualification matrix, fail-closed profiles, atomic lifecycle, evidence requirements, and no-untrusted-worker fallback are explicit and falsifiable; trusted tools processing untrusted project content require a profile qualified for that threat class |
| `P0-D5` | Component-specific acquisition ledger | Actual S1 and S3-D dependencies/oracles have exact revision/path/blob/rights/security/test/SBOM/exit records; MonkeyCode negatives included; no blanket donor admission |
| `P0-D6` | Benchmark laboratory and corpus protocol | D0/A/B/C/D, exactly twenty metric families `M-01..M-20`, strata, floors/budgets/non-inferiority/Pareto/statistics, `CTX-C0..CTX-C5` context ablations, `CORPUS-C0..CORPUS-C4` lifecycle, and Cubic/native/combined comparison are approved |
| `P0-D7` | Governance, roadmap, and development-method contract | Visibility/IP disposition, PR #11/#1 successor posture, ADR/history namespacing, ten slices plus S3-D, and the always-on Spec Kit/Ponytail FULL/Cubic workflow are approved with narrow authorizations |

P0 exit requires approved falsifiable protocols, not completion of the Windows experiment or final corpus. Unavailable evidence is disclosed with a bounded acquisition plan; it is never marked passed.

---
