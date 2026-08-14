Fehrest surfaces known gaps: unindexed sources, unavailable cross-repository dependencies, stale ADRs, missing revisions, degraded parsers, unverified runtime evidence, unknown ownership, and unsupported claims. Assurance persists the resulting `ReviewCoverage` as immutable evidence for the exact plan/run; later index repair cannot rewrite that historical coverage.

### 11.4 Context economics

Context selection optimizes accepted outcome, not volume:

```text
ContextValue =
  Relevance × EvidenceStrength × Freshness × StructuralReachability
  × TaskSpecificity × AuthorityEligibility
  / (TokenCost + RetrievalLatency + DisclosureRisk + StalenessRisk)
```

Each selected item records source, revision, selection reason, freshness, classification, compression, disclosure decision, and omissions. Retrieval misses and expansion requests remain evidence.

---

## 12. Native Review & Assurance Architecture

### 12.1 Core position

Native Review & Assurance is a logical WePLD capability whose first full product slice is S7. Its minimal envelopes are settled in P0 and seeded deterministically in S3-D. WePLD does not require Graphite, Augment, Cubic, Qodo, CodeRabbit, Greptile, or any other SaaS to provide product review. Separately, Cubic is a required conditional **development reviewer while building WePLD**, as defined in §4.3.

### 12.2 Native surfaces

- Local working-copy/preflight review.
- Diff review.
- Commit review.
- Branch/ChangeUnit review.
- PR review.
- ChangeStack review (future UX; canonical concept now).
- Repository scan/assurance campaign.
- Mission verification.
- Security review.
- Architecture review.
- Continuous assurance.
- **Design/Accessibility Review.**
- Runtime/incident review.

Accessibility and Arabic/RTL are architecture requirements and part of assurance, never optional polish.

### 12.3 Reconciled pipeline

```text
1  Resolve immutable ReviewTarget and exact base/head/stack/environment/policy revisions.
2  Derive and validate AssuranceProfile.
3  Pin ReviewPlan, rule set, budgets, required relationships, and expected coverage.
4  Compile Fehrest ReviewContextCapsule from governed truth.
5  Run selected deterministic evidence producers outside the TCB.
6  Edara selects the minimum-sufficient Mirefa-qualified reviewer topology.
7  Reviewers run through UWC with explicit Nawat grants and isolated information sets.
8  Produce FindingCandidates and ReviewProducerRun records.
9  Validate location, evidence, reproducibility, rule binding, and context sufficiency.
10 Admit/reject/deduplicate findings while preserving conflicts and dissent.
11 Persist immutable ReviewCoverage and accepted ReviewFindings.
12 Render high-signal ReviewSynthesis/ReviewTour projections where useful.
13 Run bounded runtime verification when static evidence is insufficient.
14 Convert a repair need into a separately authorized RepairProposal/Attempt.
15 Re-run deterministic checks and independent re-review on the repaired target.
16 Persist ReviewOutcome; send evidence to Trusted Completion without collapsing authority.
```

### 12.4 Two-channel review

The machine channel may optimize recall across deterministic and specialized reviewers. Candidate validation, location checking, evidence sufficiency, rule mapping, deduplication, and conflict preservation reduce noise. The human channel receives prioritized validated findings, coverage gaps, unresolved disagreement, uncertainty, residual risk, and explicit judgment questions. A runtime-verification channel supplies falsifiable observations and limits, not a verdict.

### 12.5 Review rule governance

`ReviewRule` contains identity/version, objective, scope/path/language, provenance/rationale, examples/counterexamples, deterministic checks where possible, AI instructions, severity/evidence requirements, exceptions, owner, and admission state. Feedback produces a Byan candidate after S10; it never silently rewrites a rule or policy.

### 12.6 Minimal contract disposition

| Contract/object | V2 disposition |
|---|---|
| V1.5 `ReviewRule`, `ReviewFinding`, `EvaluationRecord`, `SecurityFinding`, `ArchitectureFinding`, `DesignFinding`, `TestResult`, `EvidenceAssessment`, `QualityPassport`, `StackAssuranceResult` | Preserve; refine fields/versioning through P0 technical work |
| `ReviewTarget` | Minimal immutable identity envelope frozen in P0 |
| `AssuranceProfile` | Versioned requirements derived from AGILLE/risk; validated in Core |
| `ReviewPlan` | Versioned reference to target, rules, producers, context, budgets, coverage and required independence |
| `ReviewContextCapsule` | Fehrest `ContextCapsule` subtype, not a duplicate context system |
| `ReviewProducerRun` | One producer execution; non-verdict; replaces ambiguous `ReviewPass` by default |
| `FindingCandidate` / `FindingDisposition` / `ReviewConflict` | Technical records behind finding admission; no duplicate finding truth |
| `ReviewCoverage` | Immutable append-only evidence bound to plan and producer-run identities |
| `VerificationRun` / `VerificationObservation` | Controlled execution/evidence records, never acceptance |
| `RepairProposal` | Proposal only; creates no mutation authority |
| `ReviewOutcome` | Assurance lifecycle outcome; mechanically distinct from `CompletionDecision` |
| `ReviewLearningCandidate` | Byan candidate at S10; governed admission required |
| `ReviewSynthesis`, `ReviewTour` | Rebuildable/content-addressed projections; do not freeze as canonical P0 domain truth |

P0 freezes semantic invariants and versioned envelopes, not an arbitrary count of fifteen schemas.

### 12.7 Finding location integrity

Every finding anchors to immutable target/base/head identity and, where possible, path plus symbol/AST identity and a contextual line window. Renames, rebases, generated files, binary files, stack restacks, and changed-line filters must produce explicit relocation or stale states. A plausible comment on the wrong revision/location is invalid evidence.

---

## 13. Review / Trusted Completion Boundary

```text
WorkerCompletionClaim
