#![forbid(unsafe_code)]

//! S2 identity and evidence-store qualification suite.
//!
//! Covered tasks: S2-I013, S2-I014, S2-E013, S2-E014, S2-E015, S2-E016, plus
//! direct coverage of the identity ordering, reservation, bounded-read,
//! generation, publication, freshness, redaction, and authenticity behaviours
//! implemented for S2-I008..S2-I012 and S2-E003..S2-E012, S2-E017.
//!
//! Every test returns a result and propagates failures. The suite holds no
//! deletion authority, so temporary stores are left in the Cargo target
//! temporary directory rather than being removed, which mirrors the store's own
//! never-delete rule.

use std::fmt;
use std::fs;
use std::io::Write as _;
use std::path::PathBuf;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering as AtomicOrdering};
use std::thread;
use std::time::Instant;

use wepld_contracts::{
    EvidenceRecordRefs, EvidenceStatus, FreshnessBasis, GenerationId, IdentityConflictKind,
    IdentityMatchStrength, IdentityRecordState, IdentityReservationState, IdentityResolution,
    MachinePath, Observation, ObservationErrorClass, ProjectContractVersion, ProjectCurrentRef,
    ProjectId, ProjectLocator, RecordDigest, StoreAuthenticity, StoreLockScope, UnixMillis,
    canonical_project_json,
};
use wepld_core::evidence_store::{EvidenceStore, ProjectLock, StoreDefect, StoreError};
use wepld_core::identity::{
    IdentityCandidate, IdentityError, ProjectMatchFacts, ReservationRecovery,
    allocate_generation_id, allocate_project_id, allocate_record_id, allocate_worktree_id,
    build_identity_record, build_reservation, compare_match_strength, complete_reservation,
    match_strength_rank, recover_reservation, resolve_identity,
};
use wepld_core::{
    LOCK_ACQUIRE_DEADLINE_MS, MAX_RECORD_BYTES, build_manifest, busy_error_code, content_digest,
    redacted_summary, safe_path_segment,
};

/// Local test error.
///
/// Several contract error types do not implement `std::error::Error`, and the
/// contracts crate is outside this tranche's authorized path set, so the suite
/// carries its own conversion boundary rather than widening scope.
#[derive(Debug)]
struct TestError(String);

impl fmt::Display for TestError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

macro_rules! test_error_from {
    ($($source:ty),* $(,)?) => {
        $(
            impl From<$source> for TestError {
                fn from(error: $source) -> Self {
                    Self(error.to_string())
                }
            }
        )*
    };
}

test_error_from!(
    wepld_contracts::ContractValueError,
    wepld_contracts::ProjectContractCodecError,
    wepld_core::identity::IdentityError,
    StoreError,
    StoreDefect,
    std::io::Error,
    String,
);

impl From<&str> for TestError {
    fn from(message: &str) -> Self {
        Self(message.to_owned())
    }
}

type TestResult = Result<(), TestError>;

// ---------------------------------------------------------------------------
// fixtures
// ---------------------------------------------------------------------------

fn temp_root(name: &str) -> Result<PathBuf, TestError> {
    let mut root = PathBuf::from(env!("CARGO_TARGET_TMPDIR"));
    let unique = allocate_record_id()?;
    root.push(format!("wepld-s2-{name}-{}", unique.as_str()));
    fs::create_dir_all(&root)?;
    Ok(root)
}

fn locator_at(path: &str, observed_at: u64) -> Result<ProjectLocator, TestError> {
    let machine = MachinePath::utf8(path)?;
    Ok(ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: machine.clone(),
        lexical_absolute_path: machine.clone(),
        resolved_path: Observation::Available { value: machine },
        observation_time: UnixMillis::new(observed_at),
    })
}

fn facts_at(path: &str) -> Result<ProjectMatchFacts, TestError> {
    Ok(ProjectMatchFacts::new(locator_at(path, 1_000)?))
}

fn candidate(
    project_id: &ProjectId,
    facts: &ProjectMatchFacts,
    state: IdentityRecordState,
) -> Result<IdentityCandidate, TestError> {
    Ok(IdentityCandidate {
        project_id: project_id.clone(),
        facts_digest: facts.facts_digest()?,
        anchor_digest: facts.anchor_digest()?,
        state,
    })
}

const IDENTITY_PAYLOAD: &[u8] = b"{\"kind\":\"identity\"}";
const INDEX_PAYLOAD: &[u8] = b"{\"kind\":\"index\"}";

/// Write one complete generation and publish it. Returns the generation id.
fn write_generation(store: &EvidenceStore, project: &ProjectId) -> Result<GenerationId, TestError> {
    let lock = store.lock_project(project, &never_cancelled())?;
    write_generation_locked(store, &lock, project)
}

/// Write and publish one generation while already holding the project lock.
fn write_generation_locked(
    store: &EvidenceStore,
    lock: &ProjectLock,
    project: &ProjectId,
) -> Result<GenerationId, TestError> {
    let generation = allocate_generation_id()?;
    let identity_record = allocate_record_id()?;
    let index_record = allocate_record_id()?;

    let identity_digest = store.write_generation_record(
        lock,
        project,
        &generation,
        &identity_record,
        IDENTITY_PAYLOAD,
    )?;
    let index_digest =
        store.write_generation_record(lock, project, &generation, &index_record, INDEX_PAYLOAD)?;

    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        identity_record,
        index_record,
        EvidenceRecordRefs::try_from(Vec::new())?,
        vec![identity_digest, index_digest],
        UnixMillis::new(10_000),
    )?;
    store.write_generation_manifest(lock, &manifest)?;
    store.publish_generation(lock, project, &generation)?;
    Ok(generation)
}

fn never_cancelled() -> impl Fn() -> bool {
    || false
}

fn unexpected<T: std::fmt::Debug>(what: &str, value: &T) -> TestError {
    format!("expected {what}, got {value:?}").into()
}

// ---------------------------------------------------------------------------
// S2-I008 deterministic match strength ordering
// ---------------------------------------------------------------------------

#[test]
fn match_strength_order_is_total_and_stable() {
    assert_eq!(match_strength_rank(IdentityMatchStrength::ExactBinding), 0);
    assert_eq!(
        match_strength_rank(IdentityMatchStrength::StrongReassociation),
        1
    );
    assert_eq!(
        match_strength_rank(IdentityMatchStrength::ReservedBinding),
        2
    );
    assert!(
        compare_match_strength(
            IdentityMatchStrength::ExactBinding,
            IdentityMatchStrength::StrongReassociation
        )
        .is_lt()
    );
    assert!(
        compare_match_strength(
            IdentityMatchStrength::ReservedBinding,
            IdentityMatchStrength::ExactBinding
        )
        .is_gt()
    );
}

#[test]
fn exact_binding_outranks_reassociation_regardless_of_input_order() -> TestResult {
    let anchor = MachinePath::utf8("/anchor")?;
    let exact_facts = facts_at("/projects/alpha")?;
    let moved_facts =
        ProjectMatchFacts::with_anchor(locator_at("/projects/alpha", 1_000)?, anchor.clone());

    let exact_id = ProjectId::try_from("p_exact")?;
    let moved_id = ProjectId::try_from("p_moved")?;

    let exact_candidate = candidate(&exact_id, &exact_facts, IdentityRecordState::Active)?;
    let mut reassociation_candidate =
        candidate(&moved_id, &moved_facts, IdentityRecordState::Active)?;
    // Different facts, same anchor: a genuine move.
    reassociation_candidate.facts_digest = facts_at("/old/location")?.facts_digest()?;

    for ordering in [
        vec![exact_candidate.clone(), reassociation_candidate.clone()],
        vec![reassociation_candidate, exact_candidate],
    ] {
        let resolved = resolve_identity(&moved_facts, &ordering)?;
        let IdentityResolution::Existing {
            project_id,
            strength,
        } = &resolved
        else {
            return Err(unexpected("exact binding", &resolved));
        };
        assert_eq!(project_id, &exact_id);
        assert_eq!(*strength, IdentityMatchStrength::ExactBinding);
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-I009 / S2-I013 adversarial identity fixtures
// ---------------------------------------------------------------------------

#[test]
fn filesystem_copy_does_not_adopt_the_source_identity() -> TestResult {
    // A copy sits at a different path and carries no shared stable anchor.
    // It must not silently become the same local project.
    let source = facts_at("/projects/original")?;
    let copy = facts_at("/projects/original-copy")?;
    let source_id = ProjectId::try_from("p_source")?;

    let resolved = resolve_identity(
        &copy,
        &[candidate(&source_id, &source, IdentityRecordState::Active)?],
    )?;

    let IdentityResolution::Ambiguous { candidates } = &resolved else {
        return Err(unexpected("no existing identity for a copy", &resolved));
    };
    assert!(candidates.as_slice().is_empty());
    Ok(())
}

#[test]
fn independent_clone_does_not_adopt_the_source_identity() -> TestResult {
    // Overlapping content and remotes are not identity. Without a shared
    // explicit anchor an independent clone stays a separate project.
    let source = facts_at("/checkouts/repo-a")?;
    let clone = facts_at("/checkouts/repo-b")?;
    let source_id = ProjectId::try_from("p_clonesource")?;

    let resolved = resolve_identity(
        &clone,
        &[candidate(&source_id, &source, IdentityRecordState::Active)?],
    )?;
    assert!(matches!(resolved, IdentityResolution::Ambiguous { .. }));
    Ok(())
}

#[test]
fn linked_worktrees_do_not_collapse_into_one_project() -> TestResult {
    // Two worktrees of one repository have distinct roots. Each keeps its own
    // per-worktree identity rather than collapsing into a single object.
    let primary = facts_at("/repo/main-worktree")?;
    let linked = facts_at("/repo/feature-worktree")?;
    let primary_id = ProjectId::try_from("p_primary")?;

    let resolved = resolve_identity(
        &linked,
        &[candidate(
            &primary_id,
            &primary,
            IdentityRecordState::Active,
        )?],
    )?;
    assert!(matches!(resolved, IdentityResolution::Ambiguous { .. }));
    Ok(())
}

#[test]
fn move_with_shared_anchor_reassociates_conservatively() -> TestResult {
    let anchor = MachinePath::utf8("/stable/anchor")?;
    let before =
        ProjectMatchFacts::with_anchor(locator_at("/projects/before", 1_000)?, anchor.clone());
    let after = ProjectMatchFacts::with_anchor(locator_at("/projects/after", 2_000)?, anchor);
    let project_id = ProjectId::try_from("p_moved")?;

    let resolved = resolve_identity(
        &after,
        &[candidate(
            &project_id,
            &before,
            IdentityRecordState::Active,
        )?],
    )?;

    let IdentityResolution::Existing {
        project_id: resolved_id,
        strength,
    } = &resolved
    else {
        return Err(unexpected("strong reassociation", &resolved));
    };
    assert_eq!(resolved_id, &project_id);
    assert_eq!(*strength, IdentityMatchStrength::StrongReassociation);
    Ok(())
}

#[test]
fn two_equally_strong_candidates_are_a_conflict_not_a_guess() -> TestResult {
    let facts = facts_at("/projects/shared")?;
    let first = ProjectId::try_from("p_first")?;
    let second = ProjectId::try_from("p_second")?;

    let resolved = resolve_identity(
        &facts,
        &[
            candidate(&first, &facts, IdentityRecordState::Active)?,
            candidate(&second, &facts, IdentityRecordState::Active)?,
        ],
    )?;

    let IdentityResolution::Conflict { kind, candidates } = &resolved else {
        return Err(unexpected("conflict", &resolved));
    };
    assert_eq!(*kind, IdentityConflictKind::MultipleStrongCandidates);
    assert_eq!(candidates.as_slice().len(), 2);
    Ok(())
}

#[test]
fn recorded_conflict_is_sticky_and_not_overridden_by_a_fresh_match() -> TestResult {
    let facts = facts_at("/projects/conflicted")?;
    let project_id = ProjectId::try_from("p_conflicted")?;

    let resolved = resolve_identity(
        &facts,
        &[candidate(
            &project_id,
            &facts,
            IdentityRecordState::Conflict,
        )?],
    )?;

    let IdentityResolution::Conflict { kind, candidates } = &resolved else {
        return Err(unexpected("sticky conflict", &resolved));
    };
    assert_eq!(*kind, IdentityConflictKind::ContradictoryTopology);
    assert_eq!(candidates.as_slice().len(), 1);
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-I011 / S2-I012 reservation and crash recovery
// ---------------------------------------------------------------------------

#[test]
fn reservation_round_trips_and_completes() -> TestResult {
    let facts = facts_at("/projects/reserved")?;
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id.clone(), &facts, UnixMillis::new(5))?;

    assert_eq!(reservation.state, IdentityReservationState::Reserved);
    assert_eq!(
        reservation.revalidated_match_facts_digest,
        facts.facts_digest()?
    );

    let completed = complete_reservation(&reservation, &project_id, UnixMillis::new(9))?;
    assert_eq!(completed.state, IdentityReservationState::Initialized);
    assert_eq!(completed.project_id, project_id);
    assert_eq!(completed.created_at.get(), 5);
    assert_eq!(completed.updated_at.get(), 9);
    Ok(())
}

#[test]
fn completing_a_reservation_for_another_project_is_rejected() -> TestResult {
    let facts = facts_at("/projects/reserved")?;
    let owner = allocate_project_id()?;
    let other = allocate_project_id()?;
    let reservation = build_reservation(owner, &facts, UnixMillis::new(1))?;
    assert!(complete_reservation(&reservation, &other, UnixMillis::new(2)).is_err());
    Ok(())
}

#[test]
fn crashed_reservation_resumes_the_same_project_id() -> TestResult {
    // S2-I012. A crash between `reserved` and `initialized` must never allocate
    // a second identity for the same facts.
    let facts = facts_at("/projects/crashed")?;
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id.clone(), &facts, UnixMillis::new(1))?;

    let recovered = recover_reservation(&reservation, &facts)?;
    let ReservationRecovery::ResumeSameProject {
        project_id: resumed,
    } = &recovered
    else {
        return Err(unexpected("resume same project", &recovered));
    };
    assert_eq!(resumed, &project_id);
    Ok(())
}

#[test]
fn reservation_for_different_facts_is_not_adopted() -> TestResult {
    let facts = facts_at("/projects/a")?;
    let other_facts = facts_at("/projects/b")?;
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id, &facts, UnixMillis::new(1))?;

    assert_eq!(
        recover_reservation(&reservation, &other_facts)?,
        ReservationRecovery::Mismatch
    );
    Ok(())
}

#[test]
fn initialized_reservation_reports_already_initialized() -> TestResult {
    let facts = facts_at("/projects/done")?;
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id.clone(), &facts, UnixMillis::new(1))?;
    let completed = complete_reservation(&reservation, &project_id, UnixMillis::new(2))?;

    let recovered = recover_reservation(&completed, &facts)?;
    let ReservationRecovery::AlreadyInitialized {
        project_id: existing,
    } = &recovered
    else {
        return Err(unexpected("already initialized", &recovered));
    };
    assert_eq!(existing, &project_id);
    Ok(())
}

// ---------------------------------------------------------------------------
// observation-time independence (regression for the identity-facts digest)
// ---------------------------------------------------------------------------

#[test]
fn facts_digest_ignores_observation_time() -> TestResult {
    // The locator records when an observation was taken. That value changes on
    // every open, so including it in the identity digest would make the digest
    // volatile and break both exact rebinding and reservation recovery.
    let first = ProjectMatchFacts::new(locator_at("/projects/stable", 1_000)?);
    let later = ProjectMatchFacts::new(locator_at("/projects/stable", 9_999_999)?);
    assert_ne!(
        first.locator.observation_time.get(),
        later.locator.observation_time.get(),
        "fixture must actually differ in observation time"
    );
    assert_eq!(first.facts_digest()?, later.facts_digest()?);

    // A different path must still produce a different digest.
    let elsewhere = ProjectMatchFacts::new(locator_at("/projects/other", 1_000)?);
    assert_ne!(first.facts_digest()?, elsewhere.facts_digest()?);
    Ok(())
}

#[test]
fn reopening_later_rebinds_exactly() -> TestResult {
    // A normal later open of an unchanged project must resolve to the existing
    // identity as an exact binding, not fall through to ambiguous.
    let first = ProjectMatchFacts::new(locator_at("/projects/reopen", 1_000)?);
    let later = ProjectMatchFacts::new(locator_at("/projects/reopen", 5_000)?);
    let project_id = allocate_project_id()?;

    let resolved = resolve_identity(
        &later,
        &[candidate(&project_id, &first, IdentityRecordState::Active)?],
    )?;
    let IdentityResolution::Existing {
        project_id: resolved_id,
        strength,
    } = &resolved
    else {
        return Err(unexpected("exact binding on a later reopen", &resolved));
    };
    assert_eq!(resolved_id, &project_id);
    assert_eq!(*strength, IdentityMatchStrength::ExactBinding);
    Ok(())
}

#[test]
fn crashed_reservation_resumes_across_a_later_observation() -> TestResult {
    // S2-I012 under realistic timing: the resuming opener observes the project
    // at a later time than the interrupted one. It must still recognise its own
    // reservation and reuse the same identifier rather than allocating a second.
    let interrupted = ProjectMatchFacts::new(locator_at("/projects/resumed", 1_000)?);
    let resuming = ProjectMatchFacts::new(locator_at("/projects/resumed", 8_500)?);
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id.clone(), &interrupted, UnixMillis::new(1))?;

    let recovered = recover_reservation(&reservation, &resuming)?;
    let ReservationRecovery::ResumeSameProject {
        project_id: resumed,
    } = &recovered
    else {
        return Err(unexpected("resume across a later observation", &recovered));
    };
    assert_eq!(resumed, &project_id);
    Ok(())
}

#[test]
fn unavailable_resolved_path_is_rejected_not_digested() -> TestResult {
    // A failed resolution is transient. Digesting its error class would make the
    // same project take one identity when resolution succeeded and another when
    // it did not.
    let machine = MachinePath::utf8("/projects/transient")?;
    let unavailable = ProjectMatchFacts::new(ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: machine.clone(),
        lexical_absolute_path: machine,
        resolved_path: Observation::Unavailable {
            error: ObservationErrorClass::Io,
        },
        observation_time: UnixMillis::new(1_000),
    });
    assert!(matches!(
        unavailable.facts_digest(),
        Err(IdentityError::ResolvedPathUnavailable)
    ));
    Ok(())
}

#[test]
fn distinct_unavailable_error_classes_do_not_produce_identities() -> TestResult {
    // Two different failure classes must not become two different identities.
    for class in [
        ObservationErrorClass::Io,
        ObservationErrorClass::PermissionDenied,
        ObservationErrorClass::NotFound,
    ] {
        let machine = MachinePath::utf8("/projects/transient")?;
        let facts = ProjectMatchFacts::new(ProjectLocator {
            schema_version: ProjectContractVersion::V1,
            input_path: machine.clone(),
            lexical_absolute_path: machine,
            resolved_path: Observation::Unavailable { error: class },
            observation_time: UnixMillis::new(1_000),
        });
        assert!(facts.facts_digest().is_err());
    }
    Ok(())
}

#[test]
fn equivalent_path_representations_agree() -> TestResult {
    // The same bytes expressed as Utf8 or UnixBytes are the same path and must
    // not produce two identities.
    let text = "/projects/equivalent";
    let utf8 = MachinePath::utf8(text)?;
    let bytes = MachinePath::unix_bytes(text.as_bytes().to_vec())?;

    let as_utf8 = ProjectMatchFacts::new(ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: utf8.clone(),
        lexical_absolute_path: utf8.clone(),
        resolved_path: Observation::Available { value: utf8 },
        observation_time: UnixMillis::new(1_000),
    });
    let as_bytes = ProjectMatchFacts::new(ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: bytes.clone(),
        lexical_absolute_path: bytes.clone(),
        resolved_path: Observation::Available { value: bytes },
        observation_time: UnixMillis::new(2_000),
    });
    assert_eq!(as_utf8.facts_digest()?, as_bytes.facts_digest()?);

    // A genuinely different path must still differ.
    let other = ProjectMatchFacts::new(locator_at("/projects/different", 1_000)?);
    assert_ne!(as_utf8.facts_digest()?, other.facts_digest()?);
    Ok(())
}

#[test]
fn equivalent_input_spellings_resolve_to_one_identity() -> TestResult {
    // input_path is caller-supplied spelling. The same project named through a
    // dot component, or through a different input entirely, must not split into
    // several identities while the resolved path is the same.
    let resolved = MachinePath::utf8("/projects/spelling")?;
    let spellings = [
        "/projects/spelling",
        "/projects/./spelling",
        "/projects/other/../spelling",
        "spelling",
    ];
    let mut digests = Vec::new();
    for spelling in spellings {
        let input = MachinePath::utf8(spelling)?;
        let facts = ProjectMatchFacts::new(ProjectLocator {
            schema_version: ProjectContractVersion::V1,
            input_path: input.clone(),
            lexical_absolute_path: input,
            resolved_path: Observation::Available {
                value: resolved.clone(),
            },
            observation_time: UnixMillis::new(1_000),
        });
        digests.push(facts.facts_digest()?);
    }
    for digest in &digests {
        assert_eq!(
            digest, &digests[0],
            "input spelling must not change identity"
        );
    }

    // A genuinely different resolved path must still differ.
    let other = ProjectMatchFacts::new(locator_at("/projects/elsewhere", 1_000)?);
    assert_ne!(digests[0], other.facts_digest()?);
    Ok(())
}

#[test]
fn reservation_recovers_across_a_different_input_spelling() -> TestResult {
    // A reservation created under one spelling must be recoverable under
    // another, or an interrupted opener allocates a second identity.
    let resolved = MachinePath::utf8("/projects/spelled")?;
    let facts_for = |spelling: &str| -> Result<ProjectMatchFacts, TestError> {
        let input = MachinePath::utf8(spelling)?;
        Ok(ProjectMatchFacts::new(ProjectLocator {
            schema_version: ProjectContractVersion::V1,
            input_path: input.clone(),
            lexical_absolute_path: input,
            resolved_path: Observation::Available {
                value: resolved.clone(),
            },
            observation_time: UnixMillis::new(1_000),
        }))
    };
    let created = facts_for("/projects/spelled")?;
    let resumed = facts_for("/projects/./spelled")?;
    let project_id = allocate_project_id()?;
    let reservation = build_reservation(project_id.clone(), &created, UnixMillis::new(1))?;

    let recovered = recover_reservation(&reservation, &resumed)?;
    let ReservationRecovery::ResumeSameProject {
        project_id: resumed_id,
    } = &recovered
    else {
        return Err(unexpected("resume across a different spelling", &recovered));
    };
    assert_eq!(resumed_id, &project_id);
    Ok(())
}

// ---------------------------------------------------------------------------
// store-root normalisation
// ---------------------------------------------------------------------------

#[test]
fn root_normalisation_collapses_aliases_without_escaping() -> TestResult {
    // Aliases of one location must share an enforcement identity. A `.` form is
    // not sufficient evidence because Rust path comparison already collapses it,
    // so the `..` forms carry the weight here.
    let base = PathBuf::from("/state/wepld");
    let aliases = [
        PathBuf::from("/state/wepld"),
        PathBuf::from("/state/./wepld"),
        PathBuf::from("/state/other/../wepld"),
        PathBuf::from("/state/a/b/../../wepld"),
    ];
    for alias in aliases {
        assert_eq!(
            EvidenceStore::new(alias.clone()).root(),
            EvidenceStore::new(base.clone()).root(),
            "alias {alias:?} must normalise to the base root"
        );
    }

    // A parent component that would climb above an absolute root is discarded,
    // matching how both POSIX and Windows resolve it. Retaining it would leave
    // two spellings of one location as different keys and would name nothing.
    assert_eq!(
        EvidenceStore::new(PathBuf::from("/a/../../b")).root(),
        EvidenceStore::new(PathBuf::from("/b")).root()
    );
    assert_eq!(
        EvidenceStore::new(PathBuf::from("/..")).root(),
        EvidenceStore::new(PathBuf::from("/")).root()
    );

    // Normalisation must not invent a root for a relative path, and a leading
    // parent component stays meaningful because there is no known root above.
    assert_eq!(
        EvidenceStore::new(PathBuf::from("../x")).root(),
        PathBuf::from("../x")
    );

    // Distinct locations must stay distinct.
    assert_ne!(
        EvidenceStore::new(PathBuf::from("/state/wepld")).root(),
        EvidenceStore::new(PathBuf::from("/state/wepld-other")).root()
    );
    Ok(())
}

#[test]
fn root_normalisation_preserves_components_and_prefixes() -> TestResult {
    // A path component may legitimately look like a Windows drive prefix. It
    // must stay a component: reassembling through PathBuf::push would let such a
    // component replace the accumulated path and silently re-root the store.
    let lookalike = PathBuf::from("/outer/C:/inner");
    let normalised = EvidenceStore::new(lookalike.clone());
    let rendered = normalised.root().to_string_lossy().into_owned();
    assert!(
        rendered.contains("outer") && rendered.contains("inner"),
        "a prefix-looking component must not re-root the store: {rendered}"
    );
    assert_eq!(
        normalised.root().components().count(),
        lookalike.components().count(),
        "component count must be preserved when nothing is redundant"
    );

    // Normalisation must be idempotent: normalising an already-normal root
    // cannot drift.
    let once = EvidenceStore::new(lookalike);
    let twice = EvidenceStore::new(once.root().to_path_buf());
    assert_eq!(once.root(), twice.root());
    Ok(())
}

#[cfg(windows)]
#[test]
fn windows_root_forms_normalise_without_loss() -> TestResult {
    // Verbatim and UNC prefixes must survive normalisation intact, and a parent
    // component must clamp at the drive root rather than escaping it.
    let verbatim = EvidenceStore::new(PathBuf::from(r"\?\C:\a\..\b"));
    assert_eq!(verbatim.root(), &PathBuf::from(r"\?\C:\b"));

    let unc = EvidenceStore::new(PathBuf::from(r"\server\share\a\..\b"));
    assert_eq!(unc.root(), &PathBuf::from(r"\server\share\b"));

    let clamped = EvidenceStore::new(PathBuf::from(r"C:\.."));
    assert_eq!(clamped.root(), &PathBuf::from(r"C:\"));

    // A drive-relative path is not rooted, so its parent component is
    // meaningful and must be preserved rather than discarded.
    let drive_relative = EvidenceStore::new(PathBuf::from(r"C:.."));
    assert_eq!(drive_relative.root(), &PathBuf::from(r"C:.."));
    Ok(())
}

// ---------------------------------------------------------------------------
// concurrency around ordering and publication
// ---------------------------------------------------------------------------

#[test]
fn ordering_state_drains_under_concurrent_churn() -> TestResult {
    // What this proves: under heavy concurrent acquire/release churn the
    // ordering registry does not leak, underflow, or strand state, and the
    // catalog is reachable again once every guard is released.
    //
    // What this does NOT prove: that registration precedes operating-system
    // lock acquisition. That window cannot be driven deterministically through
    // the public API, so the ordering of those two steps is established by
    // construction and review rather than by this test. It is recorded that way
    // rather than implied.
    let root = temp_root("orderchurn")?;
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize()?;
    let project = Arc::new(allocate_project_id()?);

    let mut handles = Vec::new();
    for _ in 0..4 {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        handles.push(thread::spawn(move || -> Result<(), String> {
            for _ in 0..40 {
                if let Ok(guard) = store.lock_project(&project, &|| false) {
                    drop(guard);
                }
            }
            Ok(())
        }));
    }
    for _ in 0..4 {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        handles.push(thread::spawn(move || -> Result<(), String> {
            for _ in 0..40 {
                // Either the catalog is taken first and the ordered path yields
                // the project guard, or ordering refuses because a project guard
                // is live. Both are correct; an inverted pair is not reachable.
                match store.lock_catalog(&|| false) {
                    Ok(catalog) => {
                        if let Ok(project_guard) = catalog.lock_project(&store, &project, &|| false)
                        {
                            drop(project_guard);
                        }
                        drop(catalog);
                    }
                    Err(StoreError::LockOrderViolation) | Err(StoreError::Busy { .. }) => {}
                    Err(error) => return Err(format!("unexpected catalog error: {error}")),
                }
            }
            Ok(())
        }));
    }
    for handle in handles {
        handle.join().map_err(|_| "thread panicked")??;
    }

    // Every guard is gone, so no phantom ownership may remain.
    let catalog = store.lock_catalog(&never_cancelled())?;
    drop(catalog);
    Ok(())
}

#[test]
fn a_panicking_cancellation_callback_leaves_no_phantom_ownership() -> TestResult {
    // Registration happens before operating-system lock acquisition, so a panic
    // unwinding out of the caller-supplied cancellation callback must still
    // release the registry entry. Otherwise no ProjectLock exists to drop, no
    // operating-system lock is held, and every later catalog acquisition for
    // this root fails for the lifetime of the process.
    let root = temp_root("panicunwind")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let _ = store.lock_project(&project, &|| panic!("cancellation callback"));
    }));
    std::panic::set_hook(previous);
    assert!(outcome.is_err(), "the fixture must actually panic");

    // No guard survived, so the catalog must still be acquirable.
    let catalog = store.lock_catalog(&never_cancelled())?;
    drop(catalog);
    Ok(())
}

#[test]
fn a_refused_project_acquisition_leaves_no_phantom_ownership() -> TestResult {
    // What this proves: a refused or cancelled acquisition does not leave the
    // registry holding ownership that never existed, so the catalog is not
    // blocked forever.
    let root = temp_root("phantom")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let held = store.lock_project(&project, &never_cancelled())?;
    let polls = AtomicUsize::new(0);
    let cancel = || polls.fetch_add(1, AtomicOrdering::SeqCst) >= 2;
    assert!(store.lock_project(&project, &cancel).is_err());
    drop(held);

    let catalog = store.lock_catalog(&never_cancelled())?;
    drop(catalog);
    Ok(())
}

#[test]
fn readers_never_observe_bytes_rewritten_in_a_selected_generation() -> TestResult {
    // A reader that selected generation N must not have N change underneath it.
    // Closure makes that structural rather than a race the reader has to survive.
    let root = temp_root("closerace")?;
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize()?;
    let project = Arc::new(allocate_project_id()?);
    write_generation(&store, &project)?;

    let selected = store.read_published_generation(&project)?;
    let selected_generation = selected.manifest.generation_id.clone();
    let identity_ref = selected.manifest.identity_record_ref.clone();

    let writer = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || -> Result<(), String> {
            for _ in 0..10 {
                write_generation(&store, &project)
                    .map_err(|error| format!("write generation: {error}"))?;
            }
            Ok(())
        })
    };

    for _ in 0..40 {
        // Reading through the generation selected earlier must keep returning
        // exactly the bytes that generation was closed with.
        let bytes = store.read_generation_record(&selected.manifest, &identity_ref)?;
        assert_eq!(bytes, IDENTITY_PAYLOAD);
    }
    writer.join().map_err(|_| "writer thread panicked")??;

    // The selected generation is still intact after concurrent publication.
    let bytes = store.read_generation_record(&selected.manifest, &identity_ref)?;
    assert_eq!(bytes, IDENTITY_PAYLOAD);
    assert_eq!(selected.manifest.generation_id, selected_generation);
    Ok(())
}

// ---------------------------------------------------------------------------
// generation immutability
// ---------------------------------------------------------------------------

#[test]
fn a_closed_generation_cannot_be_rewritten() -> TestResult {
    // Writing the manifest closes a generation. A caller holding the correct
    // project guard must still not rewrite it, or a published generation could
    // change underneath a reader that already selected it.
    let root = temp_root("immutable")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let lock = store.lock_project(&project, &never_cancelled())?;
    let generation = write_generation_locked(&store, &lock, &project)?;

    let published = store.read_published_generation(&project)?;
    let existing_record = published.manifest.identity_record_ref.clone();

    // Rewriting an existing record in the closed generation is rejected.
    assert!(matches!(
        store.write_generation_record(&lock, &project, &generation, &existing_record, b"{}"),
        Err(StoreError::GenerationAlreadyClosed)
    ));

    // Adding a new record to the closed generation is rejected.
    let fresh_record = allocate_record_id()?;
    assert!(matches!(
        store.write_generation_record(&lock, &project, &generation, &fresh_record, b"{}"),
        Err(StoreError::GenerationAlreadyClosed)
    ));

    // Replacing the manifest of the closed generation is rejected.
    assert!(matches!(
        store.write_generation_manifest(&lock, &published.manifest),
        Err(StoreError::GenerationAlreadyClosed)
    ));

    // The published generation is unchanged and still validates.
    let after = store.read_published_generation(&project)?;
    assert_eq!(after.current.generation_id, generation);
    assert_eq!(
        after.manifest.record_digests.as_slice(),
        published.manifest.record_digests.as_slice()
    );
    Ok(())
}

#[test]
fn a_new_generation_is_still_writable_after_one_is_closed() -> TestResult {
    // Immutability must seal a generation without freezing the project.
    let root = temp_root("immutable-next")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let first = write_generation(&store, &project)?;
    let second = write_generation(&store, &project)?;
    assert_ne!(first, second);
    assert_eq!(
        store
            .read_published_generation(&project)?
            .current
            .generation_id,
        second
    );
    Ok(())
}

// ---------------------------------------------------------------------------
// lock protocol enforced by the API
// ---------------------------------------------------------------------------

#[test]
fn mutations_reject_a_lock_for_a_different_project() -> TestResult {
    let root = temp_root("wronglock")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let owned = allocate_project_id()?;
    let other = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;

    let lock = store.lock_project(&owned, &never_cancelled())?;
    let outcome = store.write_generation_record(&lock, &other, &generation, &record, b"{}");
    assert!(matches!(outcome, Err(StoreError::WrongProjectLock)));

    let publish = store.publish_generation(&lock, &other, &generation);
    assert!(matches!(publish, Err(StoreError::WrongProjectLock)));
    Ok(())
}

#[test]
fn a_guard_from_another_store_is_rejected() -> TestResult {
    // A guard proves protection only for the store it was taken from. A guard
    // from one root must never authorise a mutation applied to another root,
    // where no lock is actually held.
    let root_a = temp_root("foreign-a")?;
    let root_b = temp_root("foreign-b")?;
    let store_a = EvidenceStore::new(&root_a);
    let store_b = EvidenceStore::new(&root_b);
    store_a.initialize()?;
    store_b.initialize()?;

    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;
    let facts = facts_at("/projects/foreign")?;

    let project_lock_a = store_a.lock_project(&project, &never_cancelled())?;
    assert!(matches!(
        store_b.write_generation_record(&project_lock_a, &project, &generation, &record, b"{}"),
        Err(StoreError::ForeignLock)
    ));
    assert!(matches!(
        store_b.publish_generation(&project_lock_a, &project, &generation),
        Err(StoreError::ForeignLock)
    ));
    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        allocate_record_id()?,
        allocate_record_id()?,
        EvidenceRecordRefs::try_from(Vec::new())?,
        Vec::new(),
        UnixMillis::new(1),
    )?;
    assert!(matches!(
        store_b.write_generation_manifest(&project_lock_a, &manifest),
        Err(StoreError::ForeignLock)
    ));
    drop(project_lock_a);

    let catalog_a = store_a.lock_catalog(&never_cancelled())?;
    let reservation = build_reservation(project.clone(), &facts, UnixMillis::new(1))?;
    assert!(matches!(
        store_b.write_reservation(&catalog_a, &reservation),
        Err(StoreError::ForeignLock)
    ));
    assert!(matches!(
        catalog_a.lock_project(&store_b, &project, &never_cancelled()),
        Err(StoreError::ForeignLock)
    ));
    Ok(())
}

#[test]
fn reverse_lock_acquisition_is_refused() -> TestResult {
    // Canonical Q26 fixes catalog-before-project whenever an operation needs
    // both locks, while permitting a project-only lock for ordinary updates.
    // Holding a project guard must therefore make catalog acquisition refuse
    // rather than invert the order.
    let root = temp_root("reverseorder")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let project_lock = store.lock_project(&project, &never_cancelled())?;
    let reversed = store.lock_catalog(&never_cancelled());
    assert!(
        matches!(reversed, Err(StoreError::LockOrderViolation)),
        "catalog acquisition must be refused while a project lock is held"
    );

    // A second independently constructed handle to the same root shares the
    // constraint, so the guard cannot be laundered through another handle.
    let other_handle = EvidenceStore::new(&root);
    let laundered = other_handle.lock_catalog(&never_cancelled());
    assert!(matches!(laundered, Err(StoreError::LockOrderViolation)));

    // Nor through a different lexical spelling of the same root. A `.` component
    // would not prove anything, because Rust path comparison already skips it.
    // A `..` component is the spelling that genuinely aliases: path comparison
    // does not resolve it, so without root normalisation this would be a
    // distinct registry key and would bypass ordering enforcement entirely.
    let aliased_spelling = root.join("sibling").join("..");
    assert_ne!(
        aliased_spelling, root,
        "the alias fixture must not already compare equal"
    );
    let aliased = EvidenceStore::new(aliased_spelling);
    assert_eq!(aliased.root(), store.root());
    assert!(matches!(
        aliased.lock_catalog(&never_cancelled()),
        Err(StoreError::LockOrderViolation)
    ));

    // A guard taken from one spelling is not foreign to the other.
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;
    assert!(!matches!(
        aliased.write_generation_record(&project_lock, &project, &generation, &record, b"{}"),
        Err(StoreError::ForeignLock)
    ));

    // Releasing the project guard restores catalog availability.
    drop(project_lock);
    let recovered = store.lock_catalog(&never_cancelled())?;
    drop(recovered);

    // The canonical order still works.
    let (catalog, ordered_project) =
        store.lock_catalog_then_project(&project, &never_cancelled())?;
    drop(ordered_project);
    drop(catalog);
    Ok(())
}

#[test]
fn ordered_acquisition_yields_both_guards_in_canonical_order() -> TestResult {
    let root = temp_root("ordered")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let (catalog, project_lock) = store.lock_catalog_then_project(&project, &never_cancelled())?;
    assert_eq!(catalog.scope(), StoreLockScope::IdentityCatalog);
    assert_eq!(project_lock.scope(), StoreLockScope::ProjectStore);
    assert_eq!(project_lock.project(), &project);
    assert_eq!(catalog.root(), store.root());
    assert_eq!(project_lock.root(), store.root());
    Ok(())
}

// ---------------------------------------------------------------------------
// opaque identifiers and safe path derivation (S2-E003)
// ---------------------------------------------------------------------------

#[test]
fn allocated_identifiers_are_prefixed_and_unique() -> TestResult {
    let first = allocate_project_id()?;
    let second = allocate_project_id()?;
    assert!(first.as_str().starts_with("p_"));
    assert_ne!(first, second);
    assert!(allocate_worktree_id()?.as_str().starts_with("w_"));
    assert!(allocate_generation_id()?.as_str().starts_with("g_"));
    assert!(allocate_record_id()?.as_str().starts_with("r_"));
    Ok(())
}

#[test]
fn safe_path_segment_rejects_traversal_and_stream_selectors() {
    // The contract charset admits `.` and `:`; the path projection must not.
    assert!(safe_path_segment("p_abc123").is_ok());
    assert!(safe_path_segment(".").is_err());
    assert!(safe_path_segment("..").is_err());
    assert!(safe_path_segment(".hidden").is_err());
    assert!(safe_path_segment("p_a:stream").is_err());
    assert!(safe_path_segment("p_a/b").is_err());
    assert!(safe_path_segment("p_a\\b").is_err());
    assert!(safe_path_segment("p_a.b").is_err());
    assert!(safe_path_segment("").is_err());
    assert!(safe_path_segment("-leading").is_err());
}

// ---------------------------------------------------------------------------
// generation write / publish / read (S2-E007, S2-E008, S2-E009)
// ---------------------------------------------------------------------------

#[test]
fn published_generation_round_trips() -> TestResult {
    let root = temp_root("publish")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let generation = write_generation(&store, &project)?;
    let published = store.read_published_generation(&project)?;

    assert_eq!(published.current.generation_id, generation);
    assert_eq!(published.manifest.generation_id, generation);
    assert_eq!(published.manifest.project_id, project);
    assert_eq!(
        published.manifest.authenticity,
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    );
    Ok(())
}

#[test]
fn missing_current_is_a_typed_defect_not_an_invented_generation() -> TestResult {
    let root = temp_root("nocurrent")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let outcome = store.read_published_generation(&project);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::CurrentMissing))
    ));
    Ok(())
}

#[test]
fn publishing_a_second_generation_replaces_the_pointer_atomically() -> TestResult {
    let root = temp_root("republish")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    let first = write_generation(&store, &project)?;
    let second = write_generation(&store, &project)?;
    assert_ne!(first, second);

    let published = store.read_published_generation(&project)?;
    assert_eq!(published.current.generation_id, second);

    // The superseded generation remains on disk as an orphan and is never
    // promoted or deleted.
    let orphans = store.orphan_generations(&project)?;
    assert!(orphans.contains(&first));
    assert!(!orphans.contains(&second));
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-E014 failure injection at every commit boundary
// ---------------------------------------------------------------------------

#[test]
fn interrupted_generation_never_becomes_current() -> TestResult {
    // Records written but manifest never written: publication must refuse.
    let root = temp_root("nomanifest")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;
    store.write_generation_record(&lock, &project, &generation, &record, b"{}")?;

    let outcome = store.publish_generation(&lock, &project, &generation);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::CurrentDanglingGeneration))
    ));
    assert!(store.read_published_generation(&project).is_err());
    Ok(())
}

#[test]
fn manifest_referencing_a_missing_record_is_refused_at_publish() -> TestResult {
    let root = temp_root("missingrecord")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let identity_record = allocate_record_id()?;
    let index_record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;
    let identity_digest =
        store.write_generation_record(&lock, &project, &generation, &identity_record, b"{}")?;
    // The index record is referenced but never written.
    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        identity_record,
        index_record.clone(),
        EvidenceRecordRefs::try_from(Vec::new())?,
        vec![
            identity_digest,
            RecordDigest {
                record_id: index_record,
                digest: content_digest(b"{}")?,
            },
        ],
        UnixMillis::new(1),
    )?;
    store.write_generation_manifest(&lock, &manifest)?;

    let outcome = store.publish_generation(&lock, &project, &generation);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::RecordMissing))
    ));
    Ok(())
}

#[test]
fn torn_record_is_detected_by_digest_mismatch() -> TestResult {
    let root = temp_root("tornrecord")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = write_generation(&store, &project)?;

    // Simulate a torn write by truncating one published record in place.
    let records_dir = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("records");
    let victim = fs::read_dir(&records_dir)?
        .next()
        .ok_or("at least one record must exist")??
        .path();
    let mut file = fs::OpenOptions::new()
        .write(true)
        .truncate(true)
        .open(&victim)?;
    file.write_all(b"{")?;
    drop(file);

    let outcome = store.read_published_generation(&project);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::RecordDigestMismatch))
    ));
    Ok(())
}

#[test]
fn corrupt_current_pointer_is_detected() -> TestResult {
    let root = temp_root("corruptcurrent")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;

    let current = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current, b"not json at all")?;

    let outcome = store.read_published_generation(&project);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::CurrentCorrupt))
    ));
    Ok(())
}

#[test]
fn current_pointing_at_a_missing_generation_is_detected() -> TestResult {
    let root = temp_root("danglingcurrent")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;

    let absent = allocate_generation_id()?;
    let forged = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: absent,
        manifest_digest: content_digest(b"{}")?,
    };
    let bytes = canonical_project_json(&forged)?;
    let current = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current, &bytes)?;

    let outcome = store.read_published_generation(&project);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::CurrentDanglingGeneration))
    ));
    Ok(())
}

#[test]
fn manifest_digest_mismatch_is_detected() -> TestResult {
    let root = temp_root("manifestdigest")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = write_generation(&store, &project)?;

    let manifest_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    let mut bytes = fs::read(&manifest_path)?;
    bytes.push(b' ');
    fs::write(&manifest_path, &bytes)?;

    let outcome = store.read_published_generation(&project);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::ManifestDigestMismatch))
    ));
    Ok(())
}

#[test]
fn oversized_record_is_refused_before_it_is_written() -> TestResult {
    let root = temp_root("oversize")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;
    let oversized = vec![b'x'; MAX_RECORD_BYTES + 1];
    let outcome = store.write_generation_record(&lock, &project, &generation, &record, &oversized);
    assert!(matches!(outcome, Err(StoreError::TooLarge { .. })));
    Ok(())
}

#[test]
fn reservation_survives_temp_write_and_replace() -> TestResult {
    let root = temp_root("reservationio")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let facts = facts_at("/projects/persisted")?;
    let project = allocate_project_id()?;
    let reservation = build_reservation(project.clone(), &facts, UnixMillis::new(3))?;

    let catalog = store.lock_catalog(&never_cancelled())?;
    store.write_reservation(&catalog, &reservation)?;
    let read_back = store
        .read_reservation(&project)?
        .ok_or("reservation must be present")?;
    assert_eq!(read_back, reservation);

    let completed = complete_reservation(&reservation, &project, UnixMillis::new(4))?;
    store.write_reservation(&catalog, &completed)?;
    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1);
    let entry = listed
        .into_iter()
        .next()
        .ok_or("one reservation must be listed")?
        .map_err(|defect| format!("reservation decoded as defect: {defect}"))?;
    assert_eq!(entry.state, IdentityReservationState::Initialized);
    Ok(())
}

#[test]
fn corrupt_reservation_is_reported_rather_than_skipped() -> TestResult {
    // Silently skipping a corrupt reservation would let a second identity be
    // allocated for an already-reserved project.
    let root = temp_root("corruptreservation")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let facts = facts_at("/projects/corrupt")?;
    let project = allocate_project_id()?;
    let reservation = build_reservation(project.clone(), &facts, UnixMillis::new(1))?;
    let catalog = store.lock_catalog(&never_cancelled())?;
    store.write_reservation(&catalog, &reservation)?;
    drop(catalog);

    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", project.as_str()));
    fs::write(&path, b"{ broken")?;

    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1);
    assert!(matches!(
        listed.first(),
        Some(Err(StoreDefect::RecordCorrupt))
    ));
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-E005 / S2-E015 bounded locking and crash release
// ---------------------------------------------------------------------------

#[test]
fn contended_lock_returns_a_stable_busy_result_within_the_deadline() -> TestResult {
    let root = temp_root("lockbusy")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;

    let held = store.lock_catalog(&never_cancelled())?;

    let started = Instant::now();
    let result = store.lock_catalog(&never_cancelled());
    let elapsed = started.elapsed();

    let Err(StoreError::Busy { scope }) = &result else {
        return Err("expected a stable busy result".into());
    };
    assert_eq!(*scope, StoreLockScope::IdentityCatalog);
    assert_eq!(busy_error_code(*scope), "identity_catalog_busy");

    // Bounded completion: never an unbounded wait.
    assert!(elapsed.as_millis() >= u128::from(LOCK_ACQUIRE_DEADLINE_MS));
    assert!(elapsed.as_millis() < u128::from(LOCK_ACQUIRE_DEADLINE_MS) * 4);

    drop(held);
    Ok(())
}

#[test]
fn cancellation_stops_lock_acquisition_promptly() -> TestResult {
    let root = temp_root("lockcancel")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let held = store.lock_catalog(&never_cancelled())?;

    let polls = AtomicUsize::new(0);
    let cancel = || polls.fetch_add(1, AtomicOrdering::SeqCst) >= 2;
    let started = Instant::now();
    let result = store.lock_catalog(&cancel);
    let elapsed = started.elapsed();

    assert!(matches!(result, Err(StoreError::Cancelled { .. })));
    assert!(elapsed.as_millis() < u128::from(LOCK_ACQUIRE_DEADLINE_MS));
    drop(held);
    Ok(())
}

#[test]
fn releasing_a_lock_allows_immediate_reacquisition() -> TestResult {
    // Lock-file existence is never ownership. Once the owning handle is closed
    // the lock is available again, which is the same path a crashed process
    // takes when the operating system closes its handles.
    let root = temp_root("lockrelease")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;

    let held = store.lock_catalog(&never_cancelled())?;
    drop(held);

    let lock_path = root.join("catalog").join("catalog.lock");
    assert!(lock_path.exists(), "lock file intentionally persists");

    let started = Instant::now();
    let reacquired = store.lock_catalog(&never_cancelled())?;
    assert!(started.elapsed().as_millis() < u128::from(LOCK_ACQUIRE_DEADLINE_MS));
    drop(reacquired);
    Ok(())
}

#[test]
fn catalog_and_project_locks_are_independent_scopes() -> TestResult {
    let root = temp_root("lockscopes")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;

    // The only supported way to hold both is the ordered acquisition, which
    // takes the catalog lock before the project lock (S2-I011).
    let (catalog, project_lock) = store.lock_catalog_then_project(&project, &never_cancelled())?;
    assert_eq!(catalog.scope(), StoreLockScope::IdentityCatalog);
    assert_eq!(project_lock.scope(), StoreLockScope::ProjectStore);
    assert_eq!(project_lock.project(), &project);
    assert_eq!(busy_error_code(StoreLockScope::ProjectStore), "store_busy");
    drop(project_lock);
    drop(catalog);
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-I014 concurrent first open / S2-E013 concurrent writers
// ---------------------------------------------------------------------------

#[test]
fn concurrent_first_open_yields_one_identity_or_a_stable_busy() -> TestResult {
    // S2-I014. Never two identities for the same facts.
    let root = temp_root("firstopen")?;
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize()?;
    let facts = Arc::new(facts_at("/projects/race")?);

    let mut handles = Vec::new();
    for _ in 0..8 {
        let store = Arc::clone(&store);
        let facts = Arc::clone(&facts);
        handles.push(thread::spawn(
            move || -> Result<Option<ProjectId>, String> {
                let guard = match store.lock_catalog(&|| false) {
                    Ok(guard) => guard,
                    Err(StoreError::Busy { .. }) => return Ok(None),
                    Err(error) => return Err(format!("unexpected lock error: {error}")),
                };

                // Under the catalog lock: reuse an existing reservation for
                // these exact facts, otherwise commit exactly one new one.
                let existing = store
                    .list_reservations()
                    .map_err(|error| format!("list reservations: {error}"))?;
                for entry in existing {
                    let reservation =
                        entry.map_err(|defect| format!("reservation defect: {defect}"))?;
                    let recovered = recover_reservation(&reservation, &facts)
                        .map_err(|error| format!("recover: {error}"))?;
                    if let ReservationRecovery::ResumeSameProject { project_id }
                    | ReservationRecovery::AlreadyInitialized { project_id } = recovered
                    {
                        drop(guard);
                        return Ok(Some(project_id));
                    }
                }
                let project_id =
                    allocate_project_id().map_err(|error| format!("allocate: {error}"))?;
                let reservation = build_reservation(project_id.clone(), &facts, UnixMillis::new(1))
                    .map_err(|error| format!("reservation: {error}"))?;
                store
                    .write_reservation(&guard, &reservation)
                    .map_err(|error| format!("write reservation: {error}"))?;
                drop(guard);
                Ok(Some(project_id))
            },
        ));
    }

    let mut allocated: Vec<ProjectId> = Vec::new();
    for handle in handles {
        let outcome = handle.join().map_err(|_| "worker thread panicked")?;
        if let Some(project_id) = outcome? {
            allocated.push(project_id);
        }
    }

    assert!(!allocated.is_empty(), "at least one opener must succeed");
    allocated.sort();
    allocated.dedup();
    assert_eq!(
        allocated.len(),
        1,
        "concurrent first open must not create duplicate identities"
    );

    let reservations = store.list_reservations()?;
    assert_eq!(reservations.len(), 1, "exactly one reservation persists");
    Ok(())
}

#[test]
fn concurrent_ordinary_writers_never_publish_a_mixed_generation() -> TestResult {
    // S2-E013. Each writer publishes a complete generation under the project
    // lock. Readers always observe one coherent generation.
    let root = temp_root("concurrentwriters")?;
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize()?;
    let project = Arc::new(allocate_project_id()?);

    let mut handles = Vec::new();
    for _ in 0..4 {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        handles.push(thread::spawn(move || -> Result<(), String> {
            for _ in 0..3 {
                match store.lock_project(&project, &|| false) {
                    Ok(guard) => {
                        write_generation_locked(&store, &guard, &project)
                            .map_err(|error| format!("write generation: {error}"))?;
                        drop(guard);
                    }
                    Err(StoreError::Busy { .. }) => {}
                    Err(error) => return Err(format!("unexpected lock error: {error}")),
                }
            }
            Ok(())
        }));
    }
    for handle in handles {
        handle.join().map_err(|_| "writer thread panicked")??;
    }

    // Whatever interleaving occurred, the published generation validates fully.
    let published = store.read_published_generation(&project)?;
    assert_eq!(published.manifest.project_id, *project);
    Ok(())
}

#[test]
fn readers_observe_a_coherent_generation_while_a_writer_publishes() -> TestResult {
    let root = temp_root("readerwriter")?;
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize()?;
    let project = Arc::new(allocate_project_id()?);
    write_generation(&store, &project)?;

    let writer = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || -> Result<(), String> {
            for _ in 0..10 {
                write_generation(&store, &project)
                    .map_err(|error| format!("write generation: {error}"))?;
            }
            Ok(())
        })
    };

    let reader = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || -> Result<(), String> {
            for _ in 0..25 {
                // Every successful read must be internally coherent.
                if let Ok(published) = store.read_published_generation(&project)
                    && published.manifest.generation_id != published.current.generation_id
                {
                    return Err("mixed generation observed".to_owned());
                }
            }
            Ok(())
        })
    };

    writer.join().map_err(|_| "writer thread panicked")??;
    reader.join().map_err(|_| "reader thread panicked")??;
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-E011 freshness, S2-E012 redaction, S2-E016 durability, S2-E017 authenticity
// ---------------------------------------------------------------------------

#[test]
fn freshness_uses_generation_commit_time_not_filesystem_metadata() -> TestResult {
    let root = temp_root("freshness")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;
    let published = store.read_published_generation(&project)?;

    let fresh = EvidenceStore::freshness(&published.manifest, UnixMillis::new(10_500), 1_000);
    assert_eq!(fresh.basis, FreshnessBasis::GenerationCommit);
    assert_eq!(fresh.status, EvidenceStatus::Complete);
    assert_eq!(fresh.age_millis, 500);

    let stale = EvidenceStore::freshness(&published.manifest, UnixMillis::new(20_000), 1_000);
    assert_eq!(stale.status, EvidenceStatus::Stale);

    // A generation stamped in the future is stale, never negatively aged.
    let skewed = EvidenceStore::freshness(&published.manifest, UnixMillis::new(1), 1_000);
    assert_eq!(skewed.status, EvidenceStatus::Stale);
    assert_eq!(skewed.age_millis, 0);
    Ok(())
}

#[test]
fn redacted_summary_never_reveals_the_value() -> TestResult {
    let secret = b"https://user:tokenvalue@example.invalid/repo.git";
    let summary = redacted_summary(secret)?;
    assert!(summary.starts_with("redacted:"));
    assert!(!summary.contains("tokenvalue"));
    assert!(!summary.contains("example.invalid"));
    // The exact byte length is withheld; only a coarse class is emitted.
    //
    // This assertion proves exactly that and no more. A coarse class still
    // narrows a candidate search to one length range, so it reduces rather than
    // removes length disclosure. The module documentation states that boundary,
    // and this comment must not claim more than the body checks.
    assert!(!summary.contains(&secret.len().to_string()));
    // Identical values correlate; different values do not collide in practice.
    assert_eq!(summary, redacted_summary(secret)?);
    assert_ne!(summary, redacted_summary(b"different")?);
    Ok(())
}

#[test]
fn redaction_size_classes_are_coarse_and_stable() -> TestResult {
    // The bucket boundaries are part of the privacy contract: they decide how
    // much a summary narrows a candidate search. Pin them so a later change is
    // a deliberate contract change rather than a silent widening of disclosure.
    let class_of = |length: usize| -> Result<String, TestError> {
        let summary = redacted_summary(&vec![b'x'; length])?;
        let class = summary
            .split(':')
            .nth(1)
            .ok_or("summary must carry a size class")?
            .to_owned();
        Ok(class)
    };

    assert_eq!(class_of(0)?, "empty");
    assert_eq!(class_of(1)?, "xs");
    assert_eq!(class_of(32)?, "xs");
    assert_eq!(class_of(33)?, "s");
    assert_eq!(class_of(128)?, "s");
    assert_eq!(class_of(129)?, "m");
    assert_eq!(class_of(1024)?, "m");
    assert_eq!(class_of(1025)?, "l");

    // Different lengths inside one bucket are indistinguishable by class, which
    // is the whole point of bucketing.
    assert_eq!(class_of(40)?, class_of(120)?);
    Ok(())
}

#[test]
fn store_reports_only_structural_coherence_authenticity() {
    // S2-E017. A writer-capable actor can forge a self-consistent store, so the
    // store must never claim cryptographic authentication or tamper evidence.
    assert_eq!(
        EvidenceStore::authenticity(),
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    );
}

#[test]
fn a_forged_but_self_consistent_generation_is_not_reported_as_authenticated() -> TestResult {
    // S2-S015 in miniature: an actor with writer access can rebuild a complete
    // generation that validates. Validation success is coherence evidence only.
    let root = temp_root("forged")?;
    let store = EvidenceStore::new(&root);
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;

    // The forger simply writes another complete generation and publishes it.
    let forged = write_generation(&store, &project)?;
    let published = store.read_published_generation(&project)?;
    assert_eq!(published.current.generation_id, forged);
    assert_eq!(
        published.manifest.authenticity,
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
        "structural validity must not be presented as authenticity"
    );
    Ok(())
}

#[test]
fn published_records_are_durable_and_byte_exact_after_reopen() -> TestResult {
    // S2-E016. Durability evidence is limited to what this platform genuinely
    // guarantees: contents are synced before the rename that publishes them, so
    // a reopened store observes exactly the written bytes. No claim is made
    // about directory-entry or power-loss semantics.
    let root = temp_root("durability")?;
    let project = allocate_project_id()?;
    {
        let store = EvidenceStore::new(&root);
        store.initialize()?;
        write_generation(&store, &project)?;
    }

    let reopened = EvidenceStore::new(&root);
    let published = reopened.read_published_generation(&project)?;
    let identity_bytes = reopened
        .read_generation_record(&published.manifest, &published.manifest.identity_record_ref)?;
    assert_eq!(identity_bytes, IDENTITY_PAYLOAD);
    Ok(())
}

#[test]
fn identity_record_binds_the_revalidated_facts_digest() -> TestResult {
    let facts = facts_at("/projects/record")?;
    let project = allocate_project_id()?;
    let worktree = allocate_worktree_id()?;
    let record = build_identity_record(
        project.clone(),
        worktree.clone(),
        &facts,
        IdentityRecordState::Active,
    )?;

    assert_eq!(record.project_id, project);
    assert_eq!(record.worktree_id, worktree);
    assert_eq!(record.state, IdentityRecordState::Active);
    assert_eq!(record.revalidated_match_facts_digest, facts.facts_digest()?);
    Ok(())
}
