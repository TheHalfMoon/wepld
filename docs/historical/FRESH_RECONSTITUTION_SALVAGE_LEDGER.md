# WePLD Fresh Reconstitution Salvage Ledger

**Historical canonical-main anchor inspected:** `993b2fb55af038091f365ad29d0740bdb1bd6c9e`  
**Historical PR #1 head:** `d5ef318468b6c35df3c14c1c5f72beb1191baf29`  
**Historical PR #11 head:** `68cab399748c5c103b8f96380da69fdffca4d3fe`

## Salvage rule

```text
OLD_PATH_EXISTS != KEEP

KEEP_AS_IS
COPY_AND_REWRITE
CONCEPT_ONLY
TEST_ORACLE_ONLY
HISTORICAL_REFERENCE
REJECT
```

Nothing below is imported automatically. This ledger identifies what deserves exact follow-up before fresh foundation publication or later slices.

## Canonical-main candidates

| Old path/family | Disposition | What is worth preserving | Fresh destination / treatment |
|---|---|---|---|
| `LICENSE` | KEEP_AS_IS_CANDIDATE | Proprietary/closed-source outbound posture, subject to governance containment confirmation. | Root legal files after admin/private containment verification. |
| `COPYRIGHT` | KEEP_AS_IS_CANDIDATE | Ownership notice. | Root legal files after exact review. |
| `docs/governance/DEPENDENCY_REGISTER.md` | COPY_AND_REWRITE | Exact separation between main dependencies and PR-only dependencies; immutable action pins; provenance discipline. | `docs/governance/DEPENDENCY_REGISTER.md`, reset to fresh-tree truth. |
| `docs/governance/THIRD_PARTY_DEPENDENCIES.md` | COPY_AND_REWRITE | Third-party intake/approval concepts. | Fresh governance policy aligned to UCAP/FD-P0-013. |
| `docs/governance/INTELLECTUAL_PROPERTY.md` | COPY_AND_REWRITE | IP/provenance discipline. | Fresh governance policy after B-GOV-001. |
| `docs/governance/REPOSITORY_ACCESS_CONTROL.md` | CONCEPT_ONLY | Access-control intent. | Rebuild from verified live owner/admin/ruleset state. |
| `docs/governance/AI_ASSISTED_DEVELOPMENT.md` | CONCEPT_ONLY | AI development disclosure/governance ideas. | Replace with mandatory BUILD_METHOD + AGENTS. |
| `docs/31_Governed_Specification_Workflow.md` | CONCEPT_ONLY | Strict authority hierarchy; proposal != approval; durable immutable artifacts; Core effect boundary. | Re-express using AGILLE/Nawat/Mission/Assurance/Trusted Completion vocabulary. |
| `docs/01_...docs/30_...` legacy architecture set | HISTORICAL_REFERENCE | Design history and potentially useful concepts only. | Do not copy wholesale. Mine only when a ratified capability needs evidence. |
| existing docs validator workflow | TEST_ORACLE_ONLY | Documentation validation mechanics and immutable Action pin discipline. | Rebuild minimal fresh validator if still needed. |

## PR #11 candidates

PR #11 is documentation-only, ten paths under `docs/product/architecture/`.

| Family | Disposition | Salvage |
|---|---|---|
| `HUMAN-CENTRED-CONTROL-MODEL.md` | CONCEPT_ONLY | Human final authority, pause/cancel/freeze/takeover, explicit capability/approval, progressive disclosure, accessibility/RTL. |
| `AI-CREW-AND-ASSIGNMENT-MODEL.md` | CONCEPT_ONLY | Keep model/provider/role/agent/assignment distinct; no silent routing. |
| `MISSION-AND-RUN-LIFECYCLE.md` | CONCEPT_ONLY | Mission lifecycle UX/state concepts; reconcile to native Mission/Task/Attempt contracts. |
| `GITHUB-AND-DELIVERY-BOUNDARIES.md` | CONCEPT_ONLY | GitHub first-class but never hidden authority. |
| `PERSONAL-AND-COWORK-BOUNDARY.md` | HISTORICAL_REFERENCE | Local/server product boundary ideas; not Alpha architecture. |
| Studio/product IA documents | HISTORICAL_REFERENCE | UI visual design deferred; do not import into foundation. |
| PR #11 as a whole | REJECT_WHOLESALE | Replacement-first, then close as superseded under RAT-03. |

## PR #1 candidates

PR #1 contains 142 changed paths and 20k+ additions. Whole-PR merge is prohibited.

### Highest-value source/test quarries

| Path/family | Disposition | Why |
|---|---|---|
| `crates/contracts/src/validation.rs` | TEST_ORACLE_ONLY / CONCEPT_ONLY | Boundary validation, bounded payloads, identifiers-as-data. Reconcile with new contracts; do not inherit old vocabulary blindly. |
| `crates/workspace/` | TEST_ORACLE_ONLY | No-follow/path confinement, worktree containment mechanics, atomic replacement behaviors. Windows claims remain unqualified. |
| `crates/ledger/` | CONCEPT_ONLY / TEST_ORACLE_ONLY | Durable fact/ledger mechanics and failure handling. Compare with new Mission/authority model before reuse. |
| `crates/runtime/` | HISTORICAL_REFERENCE / TEST_QUARRY | Old runtime ownership/vocabulary conflicts with ratified Mission Runtime/Nawat/Edara boundaries; mine tests/failures only. |
| `crates/wwp/` | HISTORICAL_REFERENCE | Old worker protocol may contain useful framing/transport tests but UWC is the new owner/contract. |
| `crates/providers/` | TEST_ORACLE_ONLY | Local-loopback provider parsing, credential non-leakage, boundary tests. |
| `crates/specification/` | CONCEPT_ONLY / TEST_QUARRY | Spec parsing/validation tests may inform AGILLE, but GitHub Spec Kit is the mandatory build method and new typed AGILLE begins later. |
| `crates/artifacts/` | CONCEPT_ONLY | Content-addressed artifact ideas may remain useful; revalidate against new Fehrest/Mission evidence contracts. |
| `crates/hermes/` | REJECT_AS_RUNTIME / TEST_QUARRY | Hermes no longer owns orchestration/runtime architecture. Keep adversarial/golden/governance/lifecycle tests as quarry. |
| `crates/hermes/tests/adversarial_tests.rs` | TEST_ORACLE_ONLY | High-value negative/adversarial corpus. |
| `crates/hermes/tests/governance_tests.rs` | TEST_ORACLE_ONLY | Authority/governance failure corpus. |
| `crates/hermes/tests/integrity_tests.rs` | TEST_ORACLE_ONLY | Integrity/fail-closed corpus. |
| `crates/hermes/tests/lifecycle_tests.rs` | TEST_ORACLE_ONLY | Failed-attempt/non-promotion/recovery lifecycle corpus. |
| `fixtures/golden/*.trace` | TEST_ORACLE_ONLY | Golden trace/replay evidence; map to new event contracts only after reconciliation. |
| `docs/adr/*` and `docs/v2/*` | HISTORICAL_REFERENCE | Superseded architecture record, never new authority. |
| PR #1 dependency set | REJECT_BY_DEFAULT | Fresh tree starts with zero implementation dependencies; re-admit only per exact capability gate. |

## Required exact follow-up before any code salvage

For any path selected later:

```text
OLD_PATH
OLD_BLOB_SHA
OLD_COMMIT
EXACT_TEST_PATHS
LICENSE / LINEAGE
SECURITY / PLATFORM LIMITATIONS
NEW_CONTRACT_OWNER
WHAT_IS_REUSED
WHAT_IS_REWRITTEN
NEGATIVE_TESTS
ADMISSION_DECISION
```
