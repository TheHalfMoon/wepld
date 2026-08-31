#![forbid(unsafe_code)]

//! S2 local project identity semantics.
//!
//! This module owns deterministic identity match ordering, conservative
//! reassociation, collision/conflict/ambiguity handling, and the store-wide
//! catalog reservation model that serializes first-open identity allocation.
//!
//! Covered tasks: S2-I008, S2-I009, S2-I010, S2-I011, S2-I012.
//!
//! The module performs no filesystem, process, Git, network, or model effect.
//! Persistence and locking live in [`crate::evidence_store`]; this module is a
//! pure decision layer over already-revalidated facts so that identity rules can
//! be exercised deterministically without a store.

use std::cmp::Ordering;
use std::error::Error;
use std::fmt;

use sha2::{Digest as _, Sha256};
use wepld_contracts::{
    ContentDigest, ContractValueError, GenerationId, IdentityCandidateList,
    IdentityCatalogReservation, IdentityConflictKind, IdentityMatchStrength, IdentityRecordState,
    IdentityReservationState, IdentityResolution, MAX_IDENTITY_CANDIDATES, MachinePath,
    Observation, ProjectContractCodecError, ProjectContractVersion, ProjectId,
    ProjectIdentityRecord, ProjectLocator, RecordId, StoreLockScope, UnixMillis, WorktreeId,
};

/// Random bytes drawn per opaque identifier.
///
/// Sixteen bytes render as thirty-two lowercase hexadecimal characters, which
/// stays far inside `MAX_OPAQUE_ID_BYTES` once a contract prefix is applied.
pub const OPAQUE_ID_RANDOM_BYTES: usize = 16;

/// Version of the reservation key derivation recorded in catalog reservations.
pub const RESERVATION_KEY_VERSION: u16 = 1;

/// Domain separation tag for the project match-facts digest.
const MATCH_FACTS_DOMAIN: &[u8] = b"wepld.s2.match_facts.v1\n";

/// Domain separation tag for the reassociation anchor digest.
const ANCHOR_DOMAIN: &[u8] = b"wepld.s2.reassociation_anchor.v1\n";

/// Field separator used between digested contract components.
const FIELD_SEPARATOR: &[u8] = b"\x1f";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum IdentityError {
    /// The operating system randomness source did not produce an identifier.
    ///
    /// This is a typed failure on purpose. There is deliberately no timestamp,
    /// process-id, or path-derived fallback identifier.
    RandomnessUnavailable,
    /// More distinct candidates were observed than the contract admits.
    CandidateLimitExceeded {
        count: usize,
        max: usize,
    },
    /// A reservation was presented for a different project than requested.
    ReservationProjectMismatch,
    /// Identity was requested while the resolved path observation is
    /// unavailable.
    ///
    /// A failed resolution is a transient condition, not a stable identity fact.
    /// Deriving identity from it would make the digest depend on whether a
    /// filesystem call happened to succeed.
    ResolvedPathUnavailable,
    Contract(ContractValueError),
    Codec(ProjectContractCodecError),
}

impl fmt::Display for IdentityError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::RandomnessUnavailable => write!(
                formatter,
                "operating system randomness is unavailable for opaque identifier allocation"
            ),
            Self::CandidateLimitExceeded { count, max } => write!(
                formatter,
                "identity candidate count {count} exceeds maximum {max}"
            ),
            Self::ReservationProjectMismatch => write!(
                formatter,
                "catalog reservation does not describe the requested project"
            ),
            Self::ResolvedPathUnavailable => write!(
                formatter,
                "identity requires an available resolved path observation"
            ),
            Self::Contract(error) => write!(formatter, "contract value error: {error}"),
            Self::Codec(error) => write!(formatter, "contract codec error: {error}"),
        }
    }
}

impl Error for IdentityError {}

impl From<ContractValueError> for IdentityError {
    fn from(error: ContractValueError) -> Self {
        Self::Contract(error)
    }
}

impl From<ProjectContractCodecError> for IdentityError {
    fn from(error: ProjectContractCodecError) -> Self {
        Self::Codec(error)
    }
}

const HEX_DIGITS: &[u8; 16] = b"0123456789abcdef";

fn hex_lower(bytes: &[u8]) -> String {
    let mut rendered = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        let high = HEX_DIGITS[usize::from(byte >> 4)];
        let low = HEX_DIGITS[usize::from(byte & 0x0f)];
        rendered.push(char::from(high));
        rendered.push(char::from(low));
    }
    rendered
}

fn random_token(prefix: &str) -> Result<String, IdentityError> {
    let mut bytes = [0_u8; OPAQUE_ID_RANDOM_BYTES];
    getrandom::fill(&mut bytes).map_err(|_| IdentityError::RandomnessUnavailable)?;
    let mut token = String::with_capacity(prefix.len() + bytes.len() * 2);
    token.push_str(prefix);
    token.push_str(&hex_lower(&bytes));
    Ok(token)
}

/// Allocate a fresh opaque project identifier from operating-system randomness.
///
/// WePLD owns project identity. The randomness source supplies unpredictable
/// bytes only; it carries no identity authority of its own.
pub fn allocate_project_id() -> Result<ProjectId, IdentityError> {
    Ok(ProjectId::try_from(random_token("p_")?)?)
}

/// Allocate a fresh opaque worktree identifier.
pub fn allocate_worktree_id() -> Result<WorktreeId, IdentityError> {
    Ok(WorktreeId::try_from(random_token("w_")?)?)
}

/// Allocate a fresh opaque generation identifier.
pub fn allocate_generation_id() -> Result<GenerationId, IdentityError> {
    Ok(GenerationId::try_from(random_token("g_")?)?)
}

/// Allocate a fresh opaque evidence record identifier.
pub fn allocate_record_id() -> Result<RecordId, IdentityError> {
    Ok(RecordId::try_from(random_token("r_")?)?)
}

/// Narrow byte-oriented path domain tag.
const PATH_DOMAIN_NARROW: u8 = 0x01;

/// Wide unit-oriented path domain tag.
const PATH_DOMAIN_WIDE: u8 = 0x02;

/// Encode a machine path so that equivalent paths compare equal.
///
/// `MachinePath::Utf8` and `MachinePath::UnixBytes` can carry the exact same
/// bytes while being distinct contract variants. Digesting the contract encoding
/// would make identity depend on which constructor a caller happened to use, so
/// both narrow forms normalise to the same tagged byte string. The wide Windows
/// form stays a separate domain because it is a genuinely different encoding
/// rather than a different spelling of the same bytes.
fn stable_path_bytes(path: &MachinePath) -> Vec<u8> {
    match path {
        MachinePath::Utf8(value) => {
            let mut encoded = vec![PATH_DOMAIN_NARROW];
            encoded.extend_from_slice(value.as_bytes());
            encoded
        }
        MachinePath::UnixBytes(value) => {
            let mut encoded = vec![PATH_DOMAIN_NARROW];
            encoded.extend_from_slice(value);
            encoded
        }
        MachinePath::WindowsWtf16(value) => {
            let mut encoded = vec![PATH_DOMAIN_WIDE];
            for unit in value {
                encoded.extend_from_slice(&unit.to_le_bytes());
            }
            encoded
        }
    }
}

fn digest_parts(parts: &[&[u8]]) -> Result<ContentDigest, IdentityError> {
    let mut hasher = Sha256::new();
    for part in parts {
        hasher.update(part);
    }
    let digest = hasher.finalize();
    Ok(ContentDigest::sha256(hex_lower(&digest))?)
}

/// Facts that identity matching is allowed to depend on.
///
/// Only revalidated observations belong here. Filesystem canonicalization is a
/// point-in-time fact, so the locator is digested as a whole rather than any
/// single path being treated as identity.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectMatchFacts {
    pub locator: ProjectLocator,
    /// A stable anchor that survives a move, when one is genuinely available.
    ///
    /// S2 does not execute Git, so no anchor is available from repository
    /// metadata in this tranche. The seam exists so that a later, separately
    /// authorized topology route can supply one without changing this contract.
    pub reassociation_anchor: Option<MachinePath>,
}

impl ProjectMatchFacts {
    pub fn new(locator: ProjectLocator) -> Self {
        Self {
            locator,
            reassociation_anchor: None,
        }
    }

    pub fn with_anchor(locator: ProjectLocator, anchor: MachinePath) -> Self {
        Self {
            locator,
            reassociation_anchor: Some(anchor),
        }
    }

    /// Digest of the stable revalidated matching facts.
    ///
    /// Only facts that are stable for an unchanged project participate.
    ///
    /// `ProjectLocator::observation_time` is excluded: it changes on every open,
    /// so including it would make the digest volatile, prevent exact rebinding,
    /// and make a resumed first open fail to recognise its own reservation.
    ///
    /// An unavailable resolved-path observation is rejected rather than
    /// digested. A failed resolution is a transient condition, and its error
    /// class would otherwise become identity input: the same project would take
    /// one identity when resolution succeeded and another when it did not.
    ///
    /// Paths are normalised so that equivalent representations agree. The
    /// components are digested in a fixed order under a domain separation tag
    /// with explicit length prefixes, so no component boundary can be forged by
    /// concatenation.
    ///
    /// The digest is unkeyed. It detects drift and supports coherent matching;
    /// it authenticates nothing.
    pub fn facts_digest(&self) -> Result<ContentDigest, IdentityError> {
        let Observation::Available { value: resolved } = &self.locator.resolved_path else {
            return Err(IdentityError::ResolvedPathUnavailable);
        };
        let input = stable_path_bytes(&self.locator.input_path);
        let lexical = stable_path_bytes(&self.locator.lexical_absolute_path);
        let resolved = stable_path_bytes(resolved);
        let mut buffer = Vec::with_capacity(input.len() + lexical.len() + resolved.len() + 24);
        for component in [&input, &lexical, &resolved] {
            let length = u64::try_from(component.len()).unwrap_or(u64::MAX);
            buffer.extend_from_slice(&length.to_be_bytes());
            buffer.extend_from_slice(component);
        }
        digest_parts(&[MATCH_FACTS_DOMAIN, &buffer, FIELD_SEPARATOR])
    }

    /// Digest of the stable reassociation anchor when one is available.
    pub fn anchor_digest(&self) -> Result<Option<ContentDigest>, IdentityError> {
        match self.reassociation_anchor.as_ref() {
            None => Ok(None),
            Some(anchor) => {
                let encoded = stable_path_bytes(anchor);
                let digest = digest_parts(&[ANCHOR_DOMAIN, &encoded, FIELD_SEPARATOR])?;
                Ok(Some(digest))
            }
        }
    }
}

/// An existing catalog binding considered during identity resolution.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IdentityCandidate {
    pub project_id: ProjectId,
    pub facts_digest: ContentDigest,
    pub anchor_digest: Option<ContentDigest>,
    pub state: IdentityRecordState,
}

/// Deterministic strength ordering used when several candidates match.
///
/// S2-I008. A lower rank is a stronger match. The ordering is total and does not
/// depend on catalog iteration order.
pub fn match_strength_rank(strength: IdentityMatchStrength) -> u8 {
    match strength {
        IdentityMatchStrength::ExactBinding => 0,
        IdentityMatchStrength::StrongReassociation => 1,
        IdentityMatchStrength::ReservedBinding => 2,
    }
}

/// Compare two match strengths, strongest first.
pub fn compare_match_strength(
    left: IdentityMatchStrength,
    right: IdentityMatchStrength,
) -> Ordering {
    match_strength_rank(left).cmp(&match_strength_rank(right))
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct RankedCandidate {
    strength: IdentityMatchStrength,
    project_id: ProjectId,
}

fn candidate_list(mut ids: Vec<ProjectId>) -> Result<IdentityCandidateList, IdentityError> {
    ids.sort();
    ids.dedup();
    let count = ids.len();
    IdentityCandidateList::try_from(ids).map_err(|_| IdentityError::CandidateLimitExceeded {
        count,
        max: MAX_IDENTITY_CANDIDATES,
    })
}

/// Classify one candidate against the revalidated facts.
///
/// S2-I009. Reassociation is conservative: a differing facts digest only yields
/// [`IdentityMatchStrength::StrongReassociation`] when both sides carry the same
/// explicit stable anchor. Overlapping content alone never reassociates, so a
/// filesystem copy or an independent clone does not silently adopt an existing
/// identity.
fn classify_candidate(
    candidate: &IdentityCandidate,
    facts_digest: &ContentDigest,
    anchor_digest: Option<&ContentDigest>,
) -> Option<IdentityMatchStrength> {
    if &candidate.facts_digest == facts_digest {
        return Some(IdentityMatchStrength::ExactBinding);
    }
    match (candidate.anchor_digest.as_ref(), anchor_digest) {
        (Some(existing), Some(observed)) if existing == observed => {
            Some(IdentityMatchStrength::StrongReassociation)
        }
        _ => None,
    }
}

/// Resolve local project identity against existing catalog candidates.
///
/// S2-I008, S2-I009, S2-I010. The result is one of: a single existing binding, an
/// ambiguous set, or a conflict. Nothing here mutates state; the caller commits
/// the decision under the catalog lock.
pub fn resolve_identity(
    facts: &ProjectMatchFacts,
    candidates: &[IdentityCandidate],
) -> Result<IdentityResolution, IdentityError> {
    let facts_digest = facts.facts_digest()?;
    let anchor_digest = facts.anchor_digest()?;

    let mut ranked: Vec<RankedCandidate> = Vec::new();
    let mut conflicted: Vec<ProjectId> = Vec::new();
    for candidate in candidates {
        let Some(strength) = classify_candidate(candidate, &facts_digest, anchor_digest.as_ref())
        else {
            continue;
        };
        match candidate.state {
            IdentityRecordState::Conflict => conflicted.push(candidate.project_id.clone()),
            IdentityRecordState::Ambiguous | IdentityRecordState::Active => {
                ranked.push(RankedCandidate {
                    strength,
                    project_id: candidate.project_id.clone(),
                });
            }
        }
    }

    // A recorded conflict is sticky. It must be resolved explicitly rather than
    // being overridden by a fresh match on the same facts.
    if !conflicted.is_empty() {
        let mut all = conflicted;
        all.extend(ranked.into_iter().map(|entry| entry.project_id));
        return Ok(IdentityResolution::Conflict {
            kind: IdentityConflictKind::ContradictoryTopology,
            candidates: candidate_list(all)?,
        });
    }

    if ranked.is_empty() {
        return Ok(IdentityResolution::Ambiguous {
            candidates: candidate_list(Vec::new())?,
        });
    }

    ranked.sort_by(|left, right| {
        compare_match_strength(left.strength, right.strength)
            .then_with(|| left.project_id.cmp(&right.project_id))
    });

    let Some(best) = ranked.first() else {
        return Ok(IdentityResolution::Ambiguous {
            candidates: candidate_list(Vec::new())?,
        });
    };
    let strongest = best.strength;
    let strongest_ids: Vec<ProjectId> = ranked
        .iter()
        .filter(|entry| entry.strength == strongest)
        .map(|entry| entry.project_id.clone())
        .collect();

    if strongest_ids.len() > 1 {
        return Ok(IdentityResolution::Conflict {
            kind: IdentityConflictKind::MultipleStrongCandidates,
            candidates: candidate_list(strongest_ids)?,
        });
    }

    Ok(IdentityResolution::Existing {
        project_id: best.project_id.clone(),
        strength: strongest,
    })
}

/// Build the durable `reserved` binding committed before project initialization.
///
/// S2-I011. The reservation is written under the catalog lock so that concurrent
/// first-open attempts cannot each allocate an identity for the same facts.
pub fn build_reservation(
    project_id: ProjectId,
    facts: &ProjectMatchFacts,
    now: UnixMillis,
) -> Result<IdentityCatalogReservation, IdentityError> {
    Ok(IdentityCatalogReservation {
        schema_version: ProjectContractVersion::V1,
        reservation_key_version: RESERVATION_KEY_VERSION,
        revalidated_match_facts_digest: facts.facts_digest()?,
        project_id,
        state: IdentityReservationState::Reserved,
        created_at: now,
        updated_at: now,
    })
}

/// Outcome of inspecting an existing reservation during crash recovery.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReservationRecovery {
    /// The reservation matches the revalidated facts and must be completed
    /// using the same project identifier. A second identity is never allocated.
    ResumeSameProject { project_id: ProjectId },
    /// Initialization already completed for these facts.
    AlreadyInitialized { project_id: ProjectId },
    /// The reservation describes different facts; the caller must not adopt it.
    Mismatch,
}

/// Decide how to recover a reservation left behind by an interrupted opener.
///
/// S2-I012. A crash between `reserved` and `initialized` must resume the same
/// project identifier rather than allocating a second one.
pub fn recover_reservation(
    reservation: &IdentityCatalogReservation,
    facts: &ProjectMatchFacts,
) -> Result<ReservationRecovery, IdentityError> {
    if reservation.revalidated_match_facts_digest != facts.facts_digest()? {
        return Ok(ReservationRecovery::Mismatch);
    }
    if reservation.reservation_key_version != RESERVATION_KEY_VERSION {
        return Ok(ReservationRecovery::Mismatch);
    }
    Ok(match reservation.state {
        IdentityReservationState::Reserved => ReservationRecovery::ResumeSameProject {
            project_id: reservation.project_id.clone(),
        },
        IdentityReservationState::Initialized => ReservationRecovery::AlreadyInitialized {
            project_id: reservation.project_id.clone(),
        },
    })
}

/// Mark a reservation initialized after the project store is durably created.
pub fn complete_reservation(
    reservation: &IdentityCatalogReservation,
    project_id: &ProjectId,
    now: UnixMillis,
) -> Result<IdentityCatalogReservation, IdentityError> {
    if &reservation.project_id != project_id {
        return Err(IdentityError::ReservationProjectMismatch);
    }
    let mut completed = reservation.clone();
    completed.state = IdentityReservationState::Initialized;
    completed.updated_at = now;
    Ok(completed)
}

/// Build the durable identity record stored inside a project generation.
pub fn build_identity_record(
    project_id: ProjectId,
    worktree_id: WorktreeId,
    facts: &ProjectMatchFacts,
    state: IdentityRecordState,
) -> Result<ProjectIdentityRecord, IdentityError> {
    Ok(ProjectIdentityRecord {
        schema_version: ProjectContractVersion::V1,
        project_id,
        worktree_id,
        revalidated_match_facts_digest: facts.facts_digest()?,
        state,
    })
}

/// A stable busy result for the given lock scope.
///
/// Bounded lock acquisition never escalates into an unbounded wait; it reports a
/// stable busy result instead.
pub fn busy(scope: StoreLockScope) -> IdentityResolution {
    IdentityResolution::Busy { scope }
}
