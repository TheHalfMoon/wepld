#![forbid(unsafe_code)]

//! S2-AUTH-015 Project Doctor: a deterministic, inspection-only projection over
//! already-qualified S2 observations.
//!
//! Doctor never executes a repository task, installer, build, test, package
//! manager, remediation, shell, or network effect. It consumes typed
//! observations that the caller has already collected and returns an ordered
//! [`DoctorReport`] of [`DoctorFinding`]s whose prose is projected only from
//! WePLD-owned templates plus allowlisted, non-secret [`SafeParameter`] values.
//!
//! Invariants enforced here:
//!
//! * `CONSUME_TYPED_S2_OBSERVATIONS_ONLY` — inputs are typed, not raw bytes.
//! * `UNAVAILABLE_IS_NOT_HEALTHY` / `STALE_IS_NOT_FRESH` /
//!   `PARTIAL_IS_NOT_COMPLETE` — degraded evidence yields findings, never a
//!   silent pass.
//! * `TRUST_REFUSED_IS_NOT_TRUSTED` / `PRESERVE_NATIVE_GIT_TRUST_REFUSAL` — a
//!   Git trust refusal is reported as a manual, user-owned decision; Doctor
//!   never proposes editing `safe.directory`.
//! * `ALLOWLISTED_STRUCTURED_FIELDS_ONLY` / `WEPLD_OWNED_TEMPLATES_ONLY` —
//!   findings carry template ids + [`SafeParameter`] only.
//! * `DIGEST_EQUALITY_IS_NOT_AUTHENTICITY` — the store is reported as
//!   structurally coherent only, never cryptographically authenticated.

use std::cmp::Ordering;

use wepld_contracts::{
    ContractValueError, DoctorCategory, DoctorFinding, DoctorFindingList, DoctorReport,
    DoctorSeverity, EvidenceStatus, FindingCode, GenerationId, MachineActionHint, MachinePath,
    PackageManagerKind, ProjectContractVersion, ProjectId, RemediationKind, RepositoryTrustState,
    SafeParameter, SafeParameterList, StoreAuthenticity, TemplateId, ToolchainKind, UnixMillis,
};

/// Baseline root-descriptor discovery bounds (spec FR-020). Discovery is fixed
/// to the exact root-level allowlist and these hard limits; there is no
/// recursive or open-ended manifest search in baseline S2.
pub const MAX_ROOT_DESCRIPTOR_CANDIDATES: usize = 32;
/// Maximum bytes of any single parsed descriptor before allocation/parse.
pub const MAX_PARSED_DESCRIPTOR_BYTES: u64 = 1_048_576;
/// Maximum aggregate bytes across all parsed descriptors.
pub const MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES: u64 = 4_194_304;
/// Maximum structured nesting depth accepted while parsing a descriptor.
pub const MAX_STRUCTURED_NESTING_DEPTH: u32 = 64;

/// Contract identifier embedded in the machine projection.
pub const DOCTOR_CONTRACT: &str = "wepld.doctor_cli.v1";

/// Error raised when caller-supplied inputs violate a Doctor bound.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DoctorInputError {
    /// A descriptor discovery bound was exceeded before parsing.
    DescriptorBudgetExceeded {
        /// Which bound tripped.
        bound: DescriptorBound,
    },
    /// The assembled finding list exceeded the contract maximum.
    TooManyFindings {
        /// Observed finding count.
        count: usize,
    },
    /// A WePLD-owned identifier failed contract validation. This is a Doctor
    /// bug, never external data, but it is surfaced rather than panicked.
    Contract(ContractValueError),
}

impl core::fmt::Display for DoctorInputError {
    fn fmt(&self, formatter: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::DescriptorBudgetExceeded { bound } => {
                write!(
                    formatter,
                    "root descriptor discovery bound exceeded: {bound:?}"
                )
            }
            Self::TooManyFindings { count } => {
                write!(
                    formatter,
                    "doctor finding count {count} exceeds contract maximum"
                )
            }
            Self::Contract(error) => write!(formatter, "doctor identifier invalid: {error}"),
        }
    }
}

impl std::error::Error for DoctorInputError {}

impl From<ContractValueError> for DoctorInputError {
    fn from(value: ContractValueError) -> Self {
        Self::Contract(value)
    }
}

/// Which descriptor-discovery bound was exceeded.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DescriptorBound {
    /// More than [`MAX_ROOT_DESCRIPTOR_CANDIDATES`] candidate descriptors.
    CandidateCount,
    /// A single descriptor larger than [`MAX_PARSED_DESCRIPTOR_BYTES`].
    PerFileBytes,
    /// Aggregate descriptor bytes over [`MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES`].
    AggregateBytes,
    /// Structured nesting deeper than [`MAX_STRUCTURED_NESTING_DEPTH`].
    NestingDepth,
}

/// Verify descriptor-discovery inputs against the frozen baseline bounds before
/// any allocation or parse. Presence-only lock markers are never counted here
/// because baseline S2 does not parse them.
pub fn check_descriptor_budget(
    parsed_candidate_count: usize,
    max_single_descriptor_bytes: u64,
    aggregate_descriptor_bytes: u64,
    max_structured_nesting_depth: u32,
) -> Result<(), DoctorInputError> {
    if parsed_candidate_count > MAX_ROOT_DESCRIPTOR_CANDIDATES {
        return Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::CandidateCount,
        });
    }
    if max_single_descriptor_bytes > MAX_PARSED_DESCRIPTOR_BYTES {
        return Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::PerFileBytes,
        });
    }
    if aggregate_descriptor_bytes > MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES {
        return Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::AggregateBytes,
        });
    }
    if max_structured_nesting_depth > MAX_STRUCTURED_NESTING_DEPTH {
        return Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::NestingDepth,
        });
    }
    Ok(())
}

/// Identity/reservation state already resolved by the S2 identity algorithm.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentityObservation {
    /// A confident existing binding was matched.
    Bound,
    /// A durable first-open reservation is being reused/recovered.
    ReservedRecovered,
    /// Multiple candidate identities remain and require explicit reconciliation.
    Ambiguous {
        /// Number of candidate identities (bounded, safe count only).
        candidate_count: u64,
    },
    /// Contradictory required topology evidence for one candidate key.
    Conflict,
    /// Identity could not be resolved from the available evidence.
    Unavailable,
}

/// Repository topology facts already qualified by the S2 Git-topology adapter.
/// `None` means the project is non-Git; repository facts are then unavailable
/// rather than synthesized.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RepositoryObservation {
    /// `trusted` / `refused_by_git` / `unknown`.
    pub trust_state: RepositoryTrustState,
    /// Whether the supplied path resolved inside more than one repository
    /// candidate and the selected root should be surfaced as ambiguous.
    pub nested_candidate_ambiguity: bool,
    /// Whether a linked-worktree relationship is only partially known.
    pub linked_worktree_state_unknown: bool,
}

/// Evidence-store health already read from exactly one committed generation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EvidenceStoreObservation {
    /// Aggregate status of the selected generation's records.
    pub status: EvidenceStatus,
    /// A record digest or generation reference did not validate.
    pub integrity_defect: bool,
    /// The freshness rule for at least one required record is not satisfied.
    pub stale_required_record: bool,
    /// Structural coherence only; never authenticity.
    pub authenticity: StoreAuthenticity,
}

/// Root-descriptor / toolchain / package-manager facts, presence-only where the
/// baseline forbids parsing.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DescriptorObservation {
    /// Recognized toolchain descriptors, exact-allowlist only.
    pub toolchains: Vec<ToolchainKind>,
    /// Distinct package-manager indicators observed (presence-only).
    pub package_managers: Vec<PackageManagerKind>,
    /// Count of distinct lockfile markers present.
    pub lockfile_marker_count: u64,
    /// Conflicting lockfiles / multiple package-manager indicators seen.
    pub package_manager_ambiguous: bool,
    /// A candidate descriptor was rejected for exceeding a discovery bound.
    pub descriptor_budget_rejected: bool,
}

/// Whether a bounded security-sensitive Git-config observation actually ran
/// to completion. `Unavailable` covers a non-Git project, a Git trust
/// refusal, an unavailable Git capability, and a bounded/malformed
/// observation failure alike; in every `Unavailable` case the zero counts
/// below are an absence of evidence, never evidence of absence.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SecuritySensitiveConfigAvailability {
    Unavailable,
    Observed,
}

/// Security-sensitive configuration observed as safe classes/counts only. Raw
/// secret-bearing values never enter this struct.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SecuritySensitiveObservation {
    /// Whether the counts below reflect a completed observation.
    pub availability: SecuritySensitiveConfigAvailability,
    /// Count of config entries classified as credential-bearing (value never
    /// captured).
    pub credential_bearing_entry_count: u64,
    /// Count of remote URLs whose userinfo was redacted on observation.
    pub redacted_remote_url_count: u64,
}

impl Default for SecuritySensitiveObservation {
    fn default() -> Self {
        Self {
            availability: SecuritySensitiveConfigAvailability::Unavailable,
            credential_bearing_entry_count: 0,
            redacted_remote_url_count: 0,
        }
    }
}

/// The complete typed input set for one Doctor evaluation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DoctorInputs {
    /// Resolved project identity for the report header.
    pub project_id: ProjectId,
    /// Selected committed generation, if a store generation was read.
    pub selected_generation_id: Option<GenerationId>,
    /// Identity/reservation observation.
    pub identity: IdentityObservation,
    /// Repository topology observation, or `None` for a non-Git project.
    pub repository: Option<RepositoryObservation>,
    /// Evidence-store observation, or `None` when no store generation was read.
    pub evidence_store: Option<EvidenceStoreObservation>,
    /// Root-descriptor / toolchain / package-manager observation.
    pub descriptors: DescriptorObservation,
    /// Security-sensitive configuration classes/counts.
    pub security_sensitive: SecuritySensitiveObservation,
}

/// Stable finding-code strings. Every code has the contract `D-` prefix and a
/// fixed family segment (`ID` / `GIT` / `WS` / `TC` / `LOCK` / `PM` / `EV` /
/// `FRESH` / `SEC`).
mod codes {
    pub const IDENTITY_AMBIGUOUS: &str = "D-ID-AMBIGUOUS";
    pub const IDENTITY_CONFLICT: &str = "D-ID-CONFLICT";
    pub const IDENTITY_RESERVED_RECOVERED: &str = "D-ID-RESERVED-RECOVERED";
    pub const IDENTITY_UNAVAILABLE: &str = "D-ID-UNAVAILABLE";
    pub const REPO_TRUST_REFUSED: &str = "D-GIT-TRUST-REFUSED";
    pub const REPO_TRUST_UNKNOWN: &str = "D-GIT-TRUST-UNKNOWN";
    pub const REPO_NESTED_AMBIGUOUS: &str = "D-GIT-NESTED-AMBIGUOUS";
    pub const REPO_WORKTREE_STATE_UNKNOWN: &str = "D-GIT-WORKTREE-STATE-UNKNOWN";
    pub const REPO_ABSENT_NON_GIT: &str = "D-GIT-ABSENT-NON-GIT";
    pub const DESCRIPTOR_BUDGET_REJECTED: &str = "D-WS-DESCRIPTOR-BUDGET-REJECTED";
    pub const TOOLCHAIN_NONE_RECOGNIZED: &str = "D-TC-NONE-RECOGNIZED";
    pub const LOCKFILE_MULTIPLE_MARKERS: &str = "D-LOCK-MULTIPLE-MARKERS";
    pub const PACKAGE_MANAGER_AMBIGUOUS: &str = "D-PM-AMBIGUOUS";
    pub const EVIDENCE_STORE_UNAVAILABLE: &str = "D-EV-STORE-UNAVAILABLE";
    pub const EVIDENCE_STORE_CORRUPT: &str = "D-EV-STORE-CORRUPT";
    pub const EVIDENCE_STORE_PARTIAL: &str = "D-EV-STORE-PARTIAL";
    pub const EVIDENCE_STORE_AUTHENTICITY_LIMITATION: &str = "D-EV-AUTHENTICITY-LIMITATION";
    pub const FRESHNESS_STALE_REQUIRED_RECORD: &str = "D-FRESH-STALE-REQUIRED-RECORD";
    pub const SECURITY_CREDENTIAL_BEARING_CONFIG: &str = "D-SEC-CREDENTIAL-BEARING-CONFIG";
    pub const SECURITY_OBSERVATION_UNAVAILABLE: &str = "D-SEC-OBSERVATION-UNAVAILABLE";
}

/// Stable template-id strings. All are WePLD-owned; none interpolate external
/// data. `render_finding_text` maps each to English prose.
mod templates {
    pub const SUMMARY_IDENTITY_AMBIGUOUS: &str = "tpl.doctor.identity.ambiguous.summary";
    pub const EXPLAIN_IDENTITY_AMBIGUOUS: &str = "tpl.doctor.identity.ambiguous.explain";
    pub const REMEDY_IDENTITY_AMBIGUOUS: &str = "tpl.doctor.identity.ambiguous.remedy";
    pub const SUMMARY_IDENTITY_CONFLICT: &str = "tpl.doctor.identity.conflict.summary";
    pub const EXPLAIN_IDENTITY_CONFLICT: &str = "tpl.doctor.identity.conflict.explain";
    pub const REMEDY_IDENTITY_CONFLICT: &str = "tpl.doctor.identity.conflict.remedy";
    pub const SUMMARY_IDENTITY_RESERVED: &str = "tpl.doctor.identity.reserved.summary";
    pub const EXPLAIN_IDENTITY_RESERVED: &str = "tpl.doctor.identity.reserved.explain";
    pub const REMEDY_NONE: &str = "tpl.doctor.remedy.none";
    pub const SUMMARY_IDENTITY_UNAVAILABLE: &str = "tpl.doctor.identity.unavailable.summary";
    pub const EXPLAIN_IDENTITY_UNAVAILABLE: &str = "tpl.doctor.identity.unavailable.explain";
    pub const REMEDY_IDENTITY_UNAVAILABLE: &str = "tpl.doctor.identity.unavailable.remedy";
    pub const SUMMARY_REPO_TRUST_REFUSED: &str = "tpl.doctor.repo.trust_refused.summary";
    pub const EXPLAIN_REPO_TRUST_REFUSED: &str = "tpl.doctor.repo.trust_refused.explain";
    pub const REMEDY_REPO_TRUST_REFUSED: &str = "tpl.doctor.repo.trust_refused.remedy";
    pub const SUMMARY_REPO_TRUST_UNKNOWN: &str = "tpl.doctor.repo.trust_unknown.summary";
    pub const EXPLAIN_REPO_TRUST_UNKNOWN: &str = "tpl.doctor.repo.trust_unknown.explain";
    pub const SUMMARY_REPO_NESTED: &str = "tpl.doctor.repo.nested.summary";
    pub const EXPLAIN_REPO_NESTED: &str = "tpl.doctor.repo.nested.explain";
    pub const REMEDY_REPO_NESTED: &str = "tpl.doctor.repo.nested.remedy";
    pub const SUMMARY_REPO_WORKTREE_UNKNOWN: &str = "tpl.doctor.repo.worktree_unknown.summary";
    pub const EXPLAIN_REPO_WORKTREE_UNKNOWN: &str = "tpl.doctor.repo.worktree_unknown.explain";
    pub const SUMMARY_REPO_ABSENT: &str = "tpl.doctor.repo.absent.summary";
    pub const EXPLAIN_REPO_ABSENT: &str = "tpl.doctor.repo.absent.explain";
    pub const SUMMARY_DESCRIPTOR_BUDGET: &str = "tpl.doctor.descriptor.budget.summary";
    pub const EXPLAIN_DESCRIPTOR_BUDGET: &str = "tpl.doctor.descriptor.budget.explain";
    pub const REMEDY_DESCRIPTOR_BUDGET: &str = "tpl.doctor.descriptor.budget.remedy";
    pub const SUMMARY_TOOLCHAIN_NONE: &str = "tpl.doctor.toolchain.none.summary";
    pub const EXPLAIN_TOOLCHAIN_NONE: &str = "tpl.doctor.toolchain.none.explain";
    pub const SUMMARY_LOCKFILE_MULTIPLE: &str = "tpl.doctor.lockfile.multiple.summary";
    pub const EXPLAIN_LOCKFILE_MULTIPLE: &str = "tpl.doctor.lockfile.multiple.explain";
    pub const REMEDY_LOCKFILE_MULTIPLE: &str = "tpl.doctor.lockfile.multiple.remedy";
    pub const SUMMARY_PACKAGE_MANAGER_AMBIGUOUS: &str =
        "tpl.doctor.package_manager.ambiguous.summary";
    pub const EXPLAIN_PACKAGE_MANAGER_AMBIGUOUS: &str =
        "tpl.doctor.package_manager.ambiguous.explain";
    pub const REMEDY_PACKAGE_MANAGER_AMBIGUOUS: &str =
        "tpl.doctor.package_manager.ambiguous.remedy";
    pub const SUMMARY_EVIDENCE_UNAVAILABLE: &str = "tpl.doctor.evidence.unavailable.summary";
    pub const EXPLAIN_EVIDENCE_UNAVAILABLE: &str = "tpl.doctor.evidence.unavailable.explain";
    pub const REMEDY_EVIDENCE_UNAVAILABLE: &str = "tpl.doctor.evidence.unavailable.remedy";
    pub const SUMMARY_EVIDENCE_CORRUPT: &str = "tpl.doctor.evidence.corrupt.summary";
    pub const EXPLAIN_EVIDENCE_CORRUPT: &str = "tpl.doctor.evidence.corrupt.explain";
    pub const REMEDY_EVIDENCE_CORRUPT: &str = "tpl.doctor.evidence.corrupt.remedy";
    pub const SUMMARY_EVIDENCE_PARTIAL: &str = "tpl.doctor.evidence.partial.summary";
    pub const EXPLAIN_EVIDENCE_PARTIAL: &str = "tpl.doctor.evidence.partial.explain";
    pub const SUMMARY_EVIDENCE_AUTHENTICITY: &str = "tpl.doctor.evidence.authenticity.summary";
    pub const EXPLAIN_EVIDENCE_AUTHENTICITY: &str = "tpl.doctor.evidence.authenticity.explain";
    pub const SUMMARY_FRESHNESS_STALE: &str = "tpl.doctor.freshness.stale.summary";
    pub const EXPLAIN_FRESHNESS_STALE: &str = "tpl.doctor.freshness.stale.explain";
    pub const REMEDY_FRESHNESS_STALE: &str = "tpl.doctor.freshness.stale.remedy";
    pub const SUMMARY_SECURITY_CREDENTIAL: &str = "tpl.doctor.security.credential.summary";
    pub const EXPLAIN_SECURITY_CREDENTIAL: &str = "tpl.doctor.security.credential.explain";
    pub const REMEDY_SECURITY_CREDENTIAL: &str = "tpl.doctor.security.credential.remedy";
    pub const SUMMARY_SECURITY_OBSERVATION_UNAVAILABLE: &str =
        "tpl.doctor.security.observation_unavailable.summary";
    pub const EXPLAIN_SECURITY_OBSERVATION_UNAVAILABLE: &str =
        "tpl.doctor.security.observation_unavailable.explain";
}

/// Map a WePLD-owned template id to its English prose. Returns `None` for any id
/// not in the registry; callers treat that as a Doctor bug, never as a reason to
/// interpolate external text.
pub fn render_template(template_id: &TemplateId) -> Option<&'static str> {
    let text = match template_id.as_str() {
        templates::SUMMARY_IDENTITY_AMBIGUOUS => "Project identity is ambiguous.",
        templates::EXPLAIN_IDENTITY_AMBIGUOUS => {
            "Multiple local project identities match the observed evidence. WePLD will not guess \
             which one to use."
        }
        templates::REMEDY_IDENTITY_AMBIGUOUS => {
            "Run an explicit identity reconciliation once available; do not assume a match."
        }
        templates::SUMMARY_IDENTITY_CONFLICT => "Project identity is in conflict.",
        templates::EXPLAIN_IDENTITY_CONFLICT => {
            "Observed topology evidence contradicts the stored identity binding for this key."
        }
        templates::REMEDY_IDENTITY_CONFLICT => {
            "Inspect the conflicting evidence references; a stored identity is never overwritten \
             automatically."
        }
        templates::SUMMARY_IDENTITY_RESERVED => "A first-open reservation was recovered.",
        templates::EXPLAIN_IDENTITY_RESERVED => {
            "An earlier open left a durable reserved identity; it is being reused rather than \
             replaced."
        }
        templates::REMEDY_NONE => "No action is required.",
        templates::SUMMARY_IDENTITY_UNAVAILABLE => "Project identity could not be resolved.",
        templates::EXPLAIN_IDENTITY_UNAVAILABLE => {
            "The available evidence was insufficient to resolve or reserve a local project \
             identity."
        }
        templates::REMEDY_IDENTITY_UNAVAILABLE => {
            "Re-open the project path; if the failure persists, inspect the referenced evidence."
        }
        templates::SUMMARY_REPO_TRUST_REFUSED => "Git refused access to this repository.",
        templates::EXPLAIN_REPO_TRUST_REFUSED => {
            "Git's ownership/trust boundary refused to operate on this working tree. This is a \
             deliberate protection, not a WePLD failure."
        }
        templates::REMEDY_REPO_TRUST_REFUSED => {
            "Resolve the trust decision yourself with native Git if appropriate. WePLD does not \
             add or widen safe.directory."
        }
        templates::SUMMARY_REPO_TRUST_UNKNOWN => "Git repository trust state is unknown.",
        templates::EXPLAIN_REPO_TRUST_UNKNOWN => {
            "WePLD could not determine whether Git trusts this working tree from the available \
             evidence."
        }
        templates::SUMMARY_REPO_NESTED => "The path lies inside nested repository candidates.",
        templates::EXPLAIN_REPO_NESTED => {
            "More than one repository root could apply to the supplied path. The selected root is \
             reported; nesting remains ambiguous."
        }
        templates::REMEDY_REPO_NESTED => {
            "Open the intended repository root explicitly to remove the ambiguity."
        }
        templates::SUMMARY_REPO_WORKTREE_UNKNOWN => {
            "Linked-worktree relationship is only partly known."
        }
        templates::EXPLAIN_REPO_WORKTREE_UNKNOWN => {
            "This working tree shares a common Git directory, but its linked-worktree state could \
             not be fully qualified."
        }
        templates::SUMMARY_REPO_ABSENT => "No Git repository was observed.",
        templates::EXPLAIN_REPO_ABSENT => {
            "This is a valid local project without Git. Repository-specific facts are unavailable \
             rather than synthesized."
        }
        templates::SUMMARY_DESCRIPTOR_BUDGET => {
            "A root descriptor was rejected by a discovery bound."
        }
        templates::EXPLAIN_DESCRIPTOR_BUDGET => {
            "At least one candidate descriptor exceeded the per-file, aggregate, count, or nesting \
             limit and was not parsed."
        }
        templates::REMEDY_DESCRIPTOR_BUDGET => {
            "Reduce the oversized descriptor or open a narrower project root."
        }
        templates::SUMMARY_TOOLCHAIN_NONE => "No recognized toolchain descriptor was found.",
        templates::EXPLAIN_TOOLCHAIN_NONE => {
            "None of the exact root-level descriptor names in the S2 allowlist were present."
        }
        templates::SUMMARY_LOCKFILE_MULTIPLE => "Multiple lockfile markers are present.",
        templates::EXPLAIN_LOCKFILE_MULTIPLE => {
            "More than one lockfile marker was observed at the project root. Markers are reported \
             by presence only in baseline S2."
        }
        templates::REMEDY_LOCKFILE_MULTIPLE => {
            "Confirm which package manager owns this project; WePLD will not choose for you."
        }
        templates::SUMMARY_PACKAGE_MANAGER_AMBIGUOUS => "Package manager is ambiguous.",
        templates::EXPLAIN_PACKAGE_MANAGER_AMBIGUOUS => {
            "Conflicting lockfiles or multiple package-manager indicators were observed. WePLD \
             reports the ambiguity instead of picking one."
        }
        templates::REMEDY_PACKAGE_MANAGER_AMBIGUOUS => {
            "Remove or reconcile the conflicting indicators in the project."
        }
        templates::SUMMARY_EVIDENCE_UNAVAILABLE => "The local evidence store is unavailable.",
        templates::EXPLAIN_EVIDENCE_UNAVAILABLE => {
            "No committed evidence generation could be read. Unavailable evidence is not treated \
             as healthy."
        }
        templates::REMEDY_EVIDENCE_UNAVAILABLE => {
            "Re-open the project to initialize the store, then re-run doctor."
        }
        templates::SUMMARY_EVIDENCE_CORRUPT => "The local evidence store has an integrity defect.",
        templates::EXPLAIN_EVIDENCE_CORRUPT => {
            "A record digest or generation reference did not validate. Invalid records are \
             quarantined and never promoted to current evidence."
        }
        templates::REMEDY_EVIDENCE_CORRUPT => {
            "Inspect the referenced records; destructive repair requires separate authority."
        }
        templates::SUMMARY_EVIDENCE_PARTIAL => "The selected evidence generation is incomplete.",
        templates::EXPLAIN_EVIDENCE_PARTIAL => {
            "The committed generation does not contain every required record. Partial evidence is \
             not treated as complete."
        }
        templates::SUMMARY_EVIDENCE_AUTHENTICITY => {
            "The evidence store proves structural coherence only."
        }
        templates::EXPLAIN_EVIDENCE_AUTHENTICITY => {
            "Digest equality shows content equality, not authenticity or tamper-evidence. An \
             internally consistent forged store cannot be labeled cryptographically authenticated."
        }
        templates::SUMMARY_FRESHNESS_STALE => "A required evidence record is stale.",
        templates::EXPLAIN_FRESHNESS_STALE => {
            "At least one required record no longer satisfies its freshness rule. A timestamp \
             alone does not prove the underlying fact is still true."
        }
        templates::REMEDY_FRESHNESS_STALE => "Re-open the project to refresh the stale evidence.",
        templates::SUMMARY_SECURITY_CREDENTIAL => "Credential-bearing configuration was observed.",
        templates::EXPLAIN_SECURITY_CREDENTIAL => {
            "One or more configuration entries were classified as credential-bearing. Their raw \
             values are never captured, stored, or shown."
        }
        templates::REMEDY_SECURITY_CREDENTIAL => {
            "Review how those credentials are supplied; WePLD reports only safe counts and classes."
        }
        templates::SUMMARY_SECURITY_OBSERVATION_UNAVAILABLE => {
            "Security-sensitive configuration could not be observed."
        }
        templates::EXPLAIN_SECURITY_OBSERVATION_UNAVAILABLE => {
            "The bounded Git-config classification did not complete for this repository. The \
             absence of a credential-bearing-configuration finding here is not evidence that none \
             exists."
        }
        _ => return None,
    };
    Some(text)
}

fn code(value: &str) -> Result<FindingCode, DoctorInputError> {
    FindingCode::try_from(value).map_err(DoctorInputError::from)
}

fn template(value: &str) -> Result<TemplateId, DoctorInputError> {
    TemplateId::try_from(value).map_err(DoctorInputError::from)
}

fn safe_params(values: Vec<SafeParameter>) -> Result<SafeParameterList, DoctorInputError> {
    SafeParameterList::try_from(values).map_err(DoctorInputError::from)
}

struct FindingSpec {
    code: &'static str,
    severity: DoctorSeverity,
    category: DoctorCategory,
    summary: &'static str,
    explanation: &'static str,
    remediation_kind: RemediationKind,
    remediation: &'static str,
    hint: Option<MachineActionHint>,
    params: Vec<SafeParameter>,
}

fn build_finding(spec: FindingSpec) -> Result<DoctorFinding, DoctorInputError> {
    Ok(DoctorFinding {
        finding_code: code(spec.code)?,
        severity: spec.severity,
        category: spec.category,
        summary_template_id: template(spec.summary)?,
        explanation_template_id: template(spec.explanation)?,
        observed_evidence_refs: Vec::new().try_into().map_err(DoctorInputError::from)?,
        remediation_kind: spec.remediation_kind,
        remediation_template_id: template(spec.remediation)?,
        machine_action_hint: spec.hint,
        safe_parameters: safe_params(spec.params)?,
    })
}

fn category_rank(category: DoctorCategory) -> u8 {
    match category {
        DoctorCategory::Identity => 0,
        DoctorCategory::Repository => 1,
        DoctorCategory::Workspace => 2,
        DoctorCategory::ToolchainDescriptor => 3,
        DoctorCategory::Lockfile => 4,
        DoctorCategory::PackageManager => 5,
        DoctorCategory::EvidenceStore => 6,
        DoctorCategory::Freshness => 7,
        DoctorCategory::SecuritySensitiveConfig => 8,
    }
}

fn severity_rank(severity: DoctorSeverity) -> u8 {
    match severity {
        DoctorSeverity::Blocking => 0,
        DoctorSeverity::Warning => 1,
        DoctorSeverity::Info => 2,
    }
}

fn finding_order(left: &DoctorFinding, right: &DoctorFinding) -> Ordering {
    category_rank(left.category)
        .cmp(&category_rank(right.category))
        .then_with(|| severity_rank(left.severity).cmp(&severity_rank(right.severity)))
        .then_with(|| left.finding_code.as_str().cmp(right.finding_code.as_str()))
}

/// Evaluate all Doctor rules over the typed inputs and return a deterministically
/// ordered report. No filesystem, process, or network access occurs.
pub fn evaluate(
    inputs: &DoctorInputs,
    evaluated_at: UnixMillis,
) -> Result<DoctorReport, DoctorInputError> {
    let mut specs: Vec<FindingSpec> = Vec::new();

    match inputs.identity {
        IdentityObservation::Bound => {}
        IdentityObservation::ReservedRecovered => specs.push(FindingSpec {
            code: codes::IDENTITY_RESERVED_RECOVERED,
            severity: DoctorSeverity::Info,
            category: DoctorCategory::Identity,
            summary: templates::SUMMARY_IDENTITY_RESERVED,
            explanation: templates::EXPLAIN_IDENTITY_RESERVED,
            remediation_kind: RemediationKind::None,
            remediation: templates::REMEDY_NONE,
            hint: Some(MachineActionHint::InspectIdentity),
            params: Vec::new(),
        }),
        IdentityObservation::Ambiguous { candidate_count } => specs.push(FindingSpec {
            code: codes::IDENTITY_AMBIGUOUS,
            severity: DoctorSeverity::Blocking,
            category: DoctorCategory::Identity,
            summary: templates::SUMMARY_IDENTITY_AMBIGUOUS,
            explanation: templates::EXPLAIN_IDENTITY_AMBIGUOUS,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_IDENTITY_AMBIGUOUS,
            hint: Some(MachineActionHint::ResolveAmbiguity),
            params: vec![SafeParameter::Count {
                value: candidate_count,
            }],
        }),
        IdentityObservation::Conflict => specs.push(FindingSpec {
            code: codes::IDENTITY_CONFLICT,
            severity: DoctorSeverity::Blocking,
            category: DoctorCategory::Identity,
            summary: templates::SUMMARY_IDENTITY_CONFLICT,
            explanation: templates::EXPLAIN_IDENTITY_CONFLICT,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_IDENTITY_CONFLICT,
            hint: Some(MachineActionHint::InspectIdentity),
            params: Vec::new(),
        }),
        IdentityObservation::Unavailable => specs.push(FindingSpec {
            code: codes::IDENTITY_UNAVAILABLE,
            severity: DoctorSeverity::Blocking,
            category: DoctorCategory::Identity,
            summary: templates::SUMMARY_IDENTITY_UNAVAILABLE,
            explanation: templates::EXPLAIN_IDENTITY_UNAVAILABLE,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_IDENTITY_UNAVAILABLE,
            hint: Some(MachineActionHint::InspectIdentity),
            params: Vec::new(),
        }),
    }

    match inputs.repository {
        None => specs.push(FindingSpec {
            code: codes::REPO_ABSENT_NON_GIT,
            severity: DoctorSeverity::Info,
            category: DoctorCategory::Repository,
            summary: templates::SUMMARY_REPO_ABSENT,
            explanation: templates::EXPLAIN_REPO_ABSENT,
            remediation_kind: RemediationKind::Informational,
            remediation: templates::REMEDY_NONE,
            hint: None,
            params: Vec::new(),
        }),
        Some(repository) => {
            match repository.trust_state {
                RepositoryTrustState::Trusted => {}
                RepositoryTrustState::RefusedByGit => specs.push(FindingSpec {
                    code: codes::REPO_TRUST_REFUSED,
                    severity: DoctorSeverity::Blocking,
                    category: DoctorCategory::Repository,
                    summary: templates::SUMMARY_REPO_TRUST_REFUSED,
                    explanation: templates::EXPLAIN_REPO_TRUST_REFUSED,
                    remediation_kind: RemediationKind::ManualAction,
                    remediation: templates::REMEDY_REPO_TRUST_REFUSED,
                    hint: Some(MachineActionHint::InspectRepositoryTrust),
                    params: vec![SafeParameter::TrustState {
                        value: RepositoryTrustState::RefusedByGit,
                    }],
                }),
                RepositoryTrustState::Unknown => specs.push(FindingSpec {
                    code: codes::REPO_TRUST_UNKNOWN,
                    severity: DoctorSeverity::Warning,
                    category: DoctorCategory::Repository,
                    summary: templates::SUMMARY_REPO_TRUST_UNKNOWN,
                    explanation: templates::EXPLAIN_REPO_TRUST_UNKNOWN,
                    remediation_kind: RemediationKind::Informational,
                    remediation: templates::REMEDY_NONE,
                    hint: Some(MachineActionHint::InspectRepositoryTrust),
                    params: vec![SafeParameter::TrustState {
                        value: RepositoryTrustState::Unknown,
                    }],
                }),
            }
            if repository.nested_candidate_ambiguity {
                specs.push(FindingSpec {
                    code: codes::REPO_NESTED_AMBIGUOUS,
                    severity: DoctorSeverity::Warning,
                    category: DoctorCategory::Repository,
                    summary: templates::SUMMARY_REPO_NESTED,
                    explanation: templates::EXPLAIN_REPO_NESTED,
                    remediation_kind: RemediationKind::ManualAction,
                    remediation: templates::REMEDY_REPO_NESTED,
                    hint: None,
                    params: Vec::new(),
                });
            }
            if repository.linked_worktree_state_unknown {
                specs.push(FindingSpec {
                    code: codes::REPO_WORKTREE_STATE_UNKNOWN,
                    severity: DoctorSeverity::Info,
                    category: DoctorCategory::Repository,
                    summary: templates::SUMMARY_REPO_WORKTREE_UNKNOWN,
                    explanation: templates::EXPLAIN_REPO_WORKTREE_UNKNOWN,
                    remediation_kind: RemediationKind::Informational,
                    remediation: templates::REMEDY_NONE,
                    hint: None,
                    params: Vec::new(),
                });
            }
        }
    }

    if inputs.descriptors.descriptor_budget_rejected {
        specs.push(FindingSpec {
            code: codes::DESCRIPTOR_BUDGET_REJECTED,
            severity: DoctorSeverity::Warning,
            category: DoctorCategory::Workspace,
            summary: templates::SUMMARY_DESCRIPTOR_BUDGET,
            explanation: templates::EXPLAIN_DESCRIPTOR_BUDGET,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_DESCRIPTOR_BUDGET,
            hint: Some(MachineActionHint::InspectWorkspace),
            params: Vec::new(),
        });
    }
    if inputs.descriptors.toolchains.is_empty() {
        specs.push(FindingSpec {
            code: codes::TOOLCHAIN_NONE_RECOGNIZED,
            severity: DoctorSeverity::Info,
            category: DoctorCategory::ToolchainDescriptor,
            summary: templates::SUMMARY_TOOLCHAIN_NONE,
            explanation: templates::EXPLAIN_TOOLCHAIN_NONE,
            remediation_kind: RemediationKind::Informational,
            remediation: templates::REMEDY_NONE,
            hint: None,
            params: Vec::new(),
        });
    }
    if inputs.descriptors.lockfile_marker_count > 1 {
        specs.push(FindingSpec {
            code: codes::LOCKFILE_MULTIPLE_MARKERS,
            severity: DoctorSeverity::Warning,
            category: DoctorCategory::Lockfile,
            summary: templates::SUMMARY_LOCKFILE_MULTIPLE,
            explanation: templates::EXPLAIN_LOCKFILE_MULTIPLE,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_LOCKFILE_MULTIPLE,
            hint: None,
            params: vec![SafeParameter::Count {
                value: inputs.descriptors.lockfile_marker_count,
            }],
        });
    }
    if inputs.descriptors.package_manager_ambiguous {
        specs.push(FindingSpec {
            code: codes::PACKAGE_MANAGER_AMBIGUOUS,
            severity: DoctorSeverity::Warning,
            category: DoctorCategory::PackageManager,
            summary: templates::SUMMARY_PACKAGE_MANAGER_AMBIGUOUS,
            explanation: templates::EXPLAIN_PACKAGE_MANAGER_AMBIGUOUS,
            remediation_kind: RemediationKind::ManualAction,
            remediation: templates::REMEDY_PACKAGE_MANAGER_AMBIGUOUS,
            hint: None,
            params: vec![SafeParameter::Count {
                value: inputs.descriptors.package_managers.len() as u64,
            }],
        });
    }

    match inputs.evidence_store {
        None => specs.push(FindingSpec {
            code: codes::EVIDENCE_STORE_UNAVAILABLE,
            severity: DoctorSeverity::Blocking,
            category: DoctorCategory::EvidenceStore,
            summary: templates::SUMMARY_EVIDENCE_UNAVAILABLE,
            explanation: templates::EXPLAIN_EVIDENCE_UNAVAILABLE,
            remediation_kind: RemediationKind::CapabilityRequired,
            remediation: templates::REMEDY_EVIDENCE_UNAVAILABLE,
            hint: Some(MachineActionHint::InspectEvidenceStore),
            params: Vec::new(),
        }),
        Some(store) => {
            if store.integrity_defect || matches!(store.status, EvidenceStatus::Corrupt) {
                specs.push(FindingSpec {
                    code: codes::EVIDENCE_STORE_CORRUPT,
                    severity: DoctorSeverity::Blocking,
                    category: DoctorCategory::EvidenceStore,
                    summary: templates::SUMMARY_EVIDENCE_CORRUPT,
                    explanation: templates::EXPLAIN_EVIDENCE_CORRUPT,
                    remediation_kind: RemediationKind::ManualAction,
                    remediation: templates::REMEDY_EVIDENCE_CORRUPT,
                    hint: Some(MachineActionHint::InspectEvidenceStore),
                    params: vec![SafeParameter::EvidenceStatus {
                        value: store.status,
                    }],
                });
            } else if matches!(store.status, EvidenceStatus::Unavailable) {
                specs.push(FindingSpec {
                    code: codes::EVIDENCE_STORE_UNAVAILABLE,
                    severity: DoctorSeverity::Blocking,
                    category: DoctorCategory::EvidenceStore,
                    summary: templates::SUMMARY_EVIDENCE_UNAVAILABLE,
                    explanation: templates::EXPLAIN_EVIDENCE_UNAVAILABLE,
                    remediation_kind: RemediationKind::CapabilityRequired,
                    remediation: templates::REMEDY_EVIDENCE_UNAVAILABLE,
                    hint: Some(MachineActionHint::InspectEvidenceStore),
                    params: vec![SafeParameter::EvidenceStatus {
                        value: store.status,
                    }],
                });
            } else if matches!(store.status, EvidenceStatus::Partial) {
                specs.push(FindingSpec {
                    code: codes::EVIDENCE_STORE_PARTIAL,
                    severity: DoctorSeverity::Blocking,
                    category: DoctorCategory::EvidenceStore,
                    summary: templates::SUMMARY_EVIDENCE_PARTIAL,
                    explanation: templates::EXPLAIN_EVIDENCE_PARTIAL,
                    remediation_kind: RemediationKind::ManualAction,
                    remediation: templates::REMEDY_EVIDENCE_CORRUPT,
                    hint: Some(MachineActionHint::InspectEvidenceStore),
                    params: vec![SafeParameter::EvidenceStatus {
                        value: store.status,
                    }],
                });
            }
            specs.push(FindingSpec {
                code: codes::EVIDENCE_STORE_AUTHENTICITY_LIMITATION,
                severity: DoctorSeverity::Info,
                category: DoctorCategory::EvidenceStore,
                summary: templates::SUMMARY_EVIDENCE_AUTHENTICITY,
                explanation: templates::EXPLAIN_EVIDENCE_AUTHENTICITY,
                remediation_kind: RemediationKind::Informational,
                remediation: templates::REMEDY_NONE,
                hint: None,
                params: Vec::new(),
            });
            if store.stale_required_record || matches!(store.status, EvidenceStatus::Stale) {
                specs.push(FindingSpec {
                    code: codes::FRESHNESS_STALE_REQUIRED_RECORD,
                    severity: DoctorSeverity::Warning,
                    category: DoctorCategory::Freshness,
                    summary: templates::SUMMARY_FRESHNESS_STALE,
                    explanation: templates::EXPLAIN_FRESHNESS_STALE,
                    remediation_kind: RemediationKind::ManualAction,
                    remediation: templates::REMEDY_FRESHNESS_STALE,
                    hint: Some(MachineActionHint::RefreshEvidence),
                    params: vec![SafeParameter::EvidenceStatus {
                        value: EvidenceStatus::Stale,
                    }],
                });
            }
        }
    }

    if inputs.repository.is_some()
        && matches!(
            inputs.security_sensitive.availability,
            SecuritySensitiveConfigAvailability::Unavailable
        )
    {
        specs.push(FindingSpec {
            code: codes::SECURITY_OBSERVATION_UNAVAILABLE,
            severity: DoctorSeverity::Info,
            category: DoctorCategory::SecuritySensitiveConfig,
            summary: templates::SUMMARY_SECURITY_OBSERVATION_UNAVAILABLE,
            explanation: templates::EXPLAIN_SECURITY_OBSERVATION_UNAVAILABLE,
            remediation_kind: RemediationKind::None,
            remediation: templates::REMEDY_NONE,
            hint: None,
            params: Vec::new(),
        });
    }

    if inputs.security_sensitive.availability == SecuritySensitiveConfigAvailability::Observed
        && inputs.security_sensitive.credential_bearing_entry_count > 0
    {
        specs.push(FindingSpec {
            code: codes::SECURITY_CREDENTIAL_BEARING_CONFIG,
            severity: DoctorSeverity::Warning,
            category: DoctorCategory::SecuritySensitiveConfig,
            summary: templates::SUMMARY_SECURITY_CREDENTIAL,
            explanation: templates::EXPLAIN_SECURITY_CREDENTIAL,
            remediation_kind: RemediationKind::Informational,
            remediation: templates::REMEDY_SECURITY_CREDENTIAL,
            hint: None,
            params: vec![
                SafeParameter::Count {
                    value: inputs.security_sensitive.credential_bearing_entry_count,
                },
                SafeParameter::Count {
                    value: inputs.security_sensitive.redacted_remote_url_count,
                },
            ],
        });
    }

    let mut findings: Vec<DoctorFinding> = specs
        .into_iter()
        .map(build_finding)
        .collect::<Result<_, _>>()?;
    findings.sort_by(finding_order);

    let count = findings.len();
    let findings: DoctorFindingList = findings
        .try_into()
        .map_err(|_| DoctorInputError::TooManyFindings { count })?;

    Ok(DoctorReport {
        schema_version: ProjectContractVersion::V1,
        project_id: inputs.project_id.clone(),
        selected_generation_id: inputs.selected_generation_id.clone(),
        evaluated_at,
        findings,
    })
}

/// True when any finding is `Blocking`. Drives the CLI exit-class decision.
pub fn has_blocking_findings(report: &DoctorReport) -> bool {
    report
        .findings
        .as_slice()
        .iter()
        .any(|finding| matches!(finding.severity, DoctorSeverity::Blocking))
}

/// The only authenticity guarantee S2 makes about the local store.
pub fn store_authenticity() -> StoreAuthenticity {
    StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
}

/// Render an already-observed path as a terminal-safe, credential-redacted
/// display string. This is the only sanctioned way to move a path into output.
pub fn safe_display_path(path: &MachinePath) -> String {
    path.safe_display().as_str().to_owned()
}
