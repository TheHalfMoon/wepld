#![forbid(unsafe_code)]

//! S2 identity and evidence-store qualification suite.
//!
//! Covered tasks: S2-I013, S2-I014, S2-E013, S2-E014, S2-E016, plus direct
//! coverage of the identity ordering, reservation, bounded-read, generation,
//! publication, freshness, redaction, and authenticity behaviours implemented
//! for S2-I008..S2-I012 and S2-E003..S2-E012, S2-E017.
//!
//! S2-E015 is covered only in part, and the part is named rather than implied.
//! The half stating that lock-file existence never blocks ownership recovery is
//! demonstrated: the lock file is asserted to persist and the lock is
//! immediately reacquired. The half requiring process-crash release is not
//! demonstrated. Dropping the owning handle exercises the same operating-system
//! path a crashed process takes when its handles close, but that is reasoning
//! about the mechanism, not an observation of a crash. Spawning a process is
//! outside this tranche.
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
    MAX_EVIDENCE_REFS, MAX_RECORD_DIGESTS, MachinePath, Observation, ObservationErrorClass,
    ProjectContractVersion, ProjectCurrentRef, ProjectId, ProjectLocator, RecordDigest,
    StoreAuthenticity, StoreLockScope, UnixMillis, canonical_project_json,
};
use wepld_core::evidence_store::{EvidenceStore, ProjectLock, StoreDefect, StoreError};
use wepld_core::identity::{
    IdentityCandidate, IdentityError, ProjectMatchFacts, ReservationRecovery,
    allocate_generation_id, allocate_project_id, allocate_record_id, allocate_worktree_id,
    build_identity_record, build_reservation, compare_match_strength, complete_reservation,
    match_strength_rank, recover_reservation, resolve_identity,
};
use wepld_core::{
    LOCK_ACQUIRE_DEADLINE_MS, MAX_MANIFEST_BYTES, MAX_RECORD_BYTES, PRODUCER_CONTRACT_VERSION,
    build_manifest, busy_error_code, content_digest, redacted_summary, safe_path_segment,
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

/// Build a fixture root the running platform genuinely calls absolute.
///
/// `Path::is_absolute` is platform-specific and the difference matters here. On
/// Windows a leading separator alone is root-relative: `/state/wepld` resolves
/// against the current drive and is therefore not an absolute Windows path.
/// These fixtures are about lexical normalisation rather than about that
/// distinction, so they are anchored with a drive prefix on Windows and used
/// unchanged elsewhere.
fn absolute_fixture(path: &str) -> PathBuf {
    #[cfg(windows)]
    {
        PathBuf::from(format!("C:{path}"))
    }
    #[cfg(not(windows))]
    {
        PathBuf::from(path)
    }
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
fn facts_digest_does_not_canonicalise_the_resolved_path() -> TestResult {
    // A characterisation, not a regression: it passes against the current
    // implementation by design and exists so the precondition stays visible.
    //
    // The digest reconciles contract representations of a path, not spellings of
    // a location. Canonicalisation is the observer's job:
    // observe_project_locator fills resolved_path from std::fs::canonicalize.
    // This layer has no filesystem access and therefore cannot tell `/a/./b`
    // from `/a/b`, so two hand-built locators that differ only in that way carry
    // two identities.
    //
    // The neighbouring spelling test varies input_path and lexical_absolute_path
    // while holding resolved_path fixed; it proves caller spelling is excluded.
    // It does not speak to this, which is why this case is stated separately
    // instead of being read into that one.
    let canonical = MachinePath::utf8("/projects/canonical")?;
    let dotted = MachinePath::utf8("/projects/./canonical")?;

    let facts_of = |resolved: MachinePath| {
        ProjectMatchFacts::new(ProjectLocator {
            schema_version: ProjectContractVersion::V1,
            input_path: resolved.clone(),
            lexical_absolute_path: resolved.clone(),
            resolved_path: Observation::Available { value: resolved },
            observation_time: UnixMillis::new(1_000),
        })
    };

    assert_ne!(
        facts_of(canonical.clone()).facts_digest()?,
        facts_of(dotted).facts_digest()?,
        "an uncanonicalised resolved path is a different identity, and the \
         documentation must not promise otherwise"
    );

    // Representation, as opposed to spelling, is reconciled.
    let same_bytes = MachinePath::unix_bytes(b"/projects/canonical".to_vec())?;
    assert_eq!(
        facts_of(canonical).facts_digest()?,
        facts_of(same_bytes).facts_digest()?
    );
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
    let base = absolute_fixture("/state/wepld");
    let aliases = [
        absolute_fixture("/state/wepld"),
        absolute_fixture("/state/./wepld"),
        absolute_fixture("/state/other/../wepld"),
        absolute_fixture("/state/a/b/../../wepld"),
    ];
    assert!(
        base.is_absolute(),
        "the fixture root must be absolute on this platform"
    );
    for alias in aliases {
        assert_eq!(
            EvidenceStore::new(alias.clone())?.root(),
            EvidenceStore::new(base.clone())?.root(),
            "alias {alias:?} must normalise to the base root"
        );
    }

    // A parent component that would climb above an absolute root is discarded,
    // matching how both POSIX and Windows resolve it. Retaining it would leave
    // two spellings of one location as different keys and would name nothing.
    assert_eq!(
        EvidenceStore::new(absolute_fixture("/a/../../b"))?.root(),
        EvidenceStore::new(absolute_fixture("/b"))?.root()
    );
    assert_eq!(
        EvidenceStore::new(absolute_fixture("/.."))?.root(),
        EvidenceStore::new(absolute_fixture("/"))?.root()
    );

    // A relative root is refused outright. It would resolve against the process
    // working directory, so one handle would address different locations at
    // different times and initialize would create the skeleton wherever the
    // process happened to be.
    assert!(matches!(
        EvidenceStore::new(PathBuf::from("../x")),
        Err(StoreError::RelativeStoreRoot)
    ));
    assert!(matches!(
        EvidenceStore::new(PathBuf::from("relative/child")),
        Err(StoreError::RelativeStoreRoot)
    ));

    // Distinct locations must stay distinct.
    assert_ne!(
        EvidenceStore::new(absolute_fixture("/state/wepld"))?.root(),
        EvidenceStore::new(absolute_fixture("/state/wepld-other"))?.root()
    );
    Ok(())
}

#[test]
fn a_relative_store_root_is_refused_before_a_store_exists() -> TestResult {
    // The absolute-root requirement used to be documentation only. A relative
    // root was accepted, and every later path resolved against the process
    // working directory, so initialize would have created the store skeleton
    // wherever the process happened to be. The refusal has to happen at
    // construction: no handle, therefore no write path.
    for relative in ["relative", "./relative", "../relative", "a/b/c"] {
        assert!(
            matches!(
                EvidenceStore::new(PathBuf::from(relative)),
                Err(StoreError::RelativeStoreRoot)
            ),
            "relative root {relative:?} must be refused"
        );
    }

    // An absolute root is still accepted and still normalised.
    let root = temp_root("absoluteroot")?;
    let store = EvidenceStore::new(root.join("sibling").join(".."))?;
    assert_eq!(store.root(), root.as_path());
    store.initialize()?;
    Ok(())
}

#[test]
fn root_normalisation_preserves_components_and_prefixes() -> TestResult {
    // A path component may legitimately look like a Windows drive prefix. It
    // must stay a component: reassembling through PathBuf::push would let such a
    // component replace the accumulated path and silently re-root the store.
    let lookalike = absolute_fixture("/outer/C:/inner");
    let normalised = EvidenceStore::new(lookalike.clone())?;
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
    let once = EvidenceStore::new(lookalike)?;
    let twice = EvidenceStore::new(once.root().to_path_buf())?;
    assert_eq!(once.root(), twice.root());
    Ok(())
}

/// Assert a fixture genuinely carries a Windows `Component::Prefix`.
///
/// A single leading backslash does not produce a prefix: `\?\C:\a` parses as
/// `RootDir` plus ordinary components, so a fixture written that way exercises
/// none of the prefix handling while still passing. Two leading backslashes are
/// required. This guard makes that degradation a test failure instead of silent
/// vacuous coverage.
#[cfg(windows)]
fn assert_has_prefix(raw: &std::path::Path) -> TestResult {
    let has_prefix = raw
        .components()
        .any(|component| matches!(component, std::path::Component::Prefix(_)));
    if !has_prefix {
        return Err(format!(
            "fixture {raw:?} carries no Component::Prefix, so it does not exercise \
             Windows prefix handling"
        )
        .into());
    }
    Ok(())
}

#[cfg(windows)]
#[test]
fn windows_root_forms_normalise_without_loss() -> TestResult {
    // Verbatim and UNC prefixes must survive normalisation intact, and a parent
    // component must clamp at the drive root rather than escaping it.
    //
    // Scope of this test, stated precisely. It establishes the positive
    // property that genuine Windows prefix forms round-trip through
    // normalisation, and the `assert_has_prefix` guard proves the fixtures
    // actually reach `Component::Prefix` rather than parsing as ordinary
    // components. It does NOT catch the reassembly defect that motivated this
    // work: a syntactic prefix survives `PathBuf::push` intact, so this test
    // passes against that defective implementation too. The test with
    // fail-before proof for that defect is
    // `root_normalisation_preserves_components_and_prefixes`, which uses a
    // Normal component whose text merely resembles a prefix.
    let verbatim_input = PathBuf::from(r"\\?\C:\a\..\b");
    let verbatim_expected = PathBuf::from(r"\\?\C:\b");
    assert_has_prefix(&verbatim_input)?;
    assert_has_prefix(&verbatim_expected)?;
    let verbatim = EvidenceStore::new(verbatim_input)?;
    assert_eq!(verbatim.root(), &verbatim_expected);

    let unc_input = PathBuf::from(r"\\server\share\a\..\b");
    let unc_expected = PathBuf::from(r"\\server\share\b");
    assert_has_prefix(&unc_input)?;
    assert_has_prefix(&unc_expected)?;
    let unc = EvidenceStore::new(unc_input)?;
    assert_eq!(unc.root(), &unc_expected);

    // The verbatim UNC form carries a distinct prefix kind and must also survive.
    let verbatim_unc_input = PathBuf::from(r"\\?\UNC\server\share\a\..\b");
    let verbatim_unc_expected = PathBuf::from(r"\\?\UNC\server\share\b");
    assert_has_prefix(&verbatim_unc_input)?;
    let verbatim_unc = EvidenceStore::new(verbatim_unc_input)?;
    assert_eq!(verbatim_unc.root(), &verbatim_unc_expected);

    let clamped_input = PathBuf::from(r"C:\..");
    assert_has_prefix(&clamped_input)?;
    let clamped = EvidenceStore::new(clamped_input)?;
    assert_eq!(clamped.root(), &PathBuf::from(r"C:\"));

    // A drive-relative path carries a prefix but no root, so it resolves
    // against a per-drive current directory. It is as unanchored as any other
    // relative root and is refused for the same reason.
    let drive_relative_input = PathBuf::from(r"C:..");
    assert_has_prefix(&drive_relative_input)?;
    assert!(
        !drive_relative_input.is_absolute(),
        "the fixture must genuinely be drive-relative"
    );
    assert!(matches!(
        EvidenceStore::new(drive_relative_input),
        Err(StoreError::RelativeStoreRoot)
    ));
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
    let store = Arc::new(EvidenceStore::new(&root)?);
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
                // the project guard, or acquisition is contended and returns a
                // stable busy result. This exercises churn; it does not by
                // itself establish an ordering property.
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
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;

    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        // `unreachable!` unwinds exactly like any other panic while staying
        // inside the tokens this product test file is permitted to use.
        let _ = store.lock_project(&project, &|| unreachable!());
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
    let store = EvidenceStore::new(&root)?;
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
    let store = Arc::new(EvidenceStore::new(&root)?);
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store_a = EvidenceStore::new(&root_a)?;
    let store_b = EvidenceStore::new(&root_b)?;
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

/// Asserts only that `CatalogLock` is `Send`. Nothing here guards `ProjectLock`.
///
/// `ProjectLock` must remain non-`Send`, because ordering accounting is
/// thread-local: a guard moved to another thread would let the releasing thread
/// decrement a count it never incremented while the acquiring thread kept one
/// forever. That invariant currently rests on the `PhantomData<*const ()>` field
/// on `ProjectLock`.
///
/// This function does **not** enforce it. A negative auto-trait bound cannot be
/// written in stable Rust, and asserting it by compile failure needs a
/// compile-test harness that would require a dependency this tranche has no
/// authority to admit. Removing the marker field would therefore make
/// `ProjectLock` `Send` again and every test here would still pass.
///
/// The invariant is consequently classified `PROVEN_BY_CONSTRUCTION_AND_REVIEW`,
/// not proven by test. An earlier version of this comment claimed a
/// compile-failure probe asserted it; that probe was run interactively and never
/// committed, so the claim was false and has been removed.
///
/// `CatalogLock` carries no thread-local accounting, so its `Send` is asserted
/// positively and that assertion is real.
#[allow(dead_code)]
fn catalog_lock_is_send() {
    fn assert_send<T: Send>() {}
    assert_send::<wepld_core::evidence_store::CatalogLock>();
}

#[test]
fn a_leaked_project_guard_blocks_the_catalog_on_that_thread_for_good() -> TestResult {
    // The guard-leak limitation is usually described as leaking a handle. The
    // larger consequence is this one, and it was reasoned rather than shown:
    // ordering accounting is thread-local and released by Drop, so a forgotten
    // guard leaves the count raised for the life of the thread and that thread
    // can never acquire the catalog lock again.
    //
    // The leak is deliberate and confined. It runs on its own thread so it
    // cannot affect the rest of the suite, and on its own store root so the
    // leaked operating-system lock reaches nothing else.
    let root = temp_root("leakedguard")?;
    let outcome = thread::spawn(move || -> Result<(), String> {
        let store = EvidenceStore::new(&root).map_err(|error| format!("new: {error}"))?;
        store
            .initialize()
            .map_err(|error| format!("initialize: {error}"))?;
        let project = allocate_project_id().map_err(|error| format!("allocate: {error}"))?;

        let guard = store
            .lock_project(&project, &|| false)
            .map_err(|error| format!("project lock: {error}"))?;
        std::mem::forget(guard);

        match store.lock_catalog(&|| false) {
            Err(StoreError::LockOrderViolation) => {}
            other => return Err(format!("expected a permanent refusal, observed {other:?}")),
        }
        // Still refused on a second attempt: the state is not consumed by being
        // observed, which is what "for good" has to mean.
        match store.lock_catalog(&|| false) {
            Err(StoreError::LockOrderViolation) => Ok(()),
            other => Err(format!("expected a permanent refusal, observed {other:?}")),
        }
    })
    .join()
    .map_err(|_| "leak thread panicked")?;
    outcome?;
    Ok(())
}

#[test]
fn a_caller_holding_a_project_guard_cannot_acquire_the_catalog() -> TestResult {
    // Canonical Q26 fixes catalog-before-project when one operation needs both.
    // That is a per-caller rule, so the calling thread holding a project guard
    // must be refused the catalog. The check reads thread-local state, so no
    // other thread can change the answer between the check and the acquisition.
    let root = temp_root("reverseorder")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;

    let project_lock = store.lock_project(&project, &never_cancelled())?;
    assert!(
        matches!(
            store.lock_catalog(&never_cancelled()),
            Err(StoreError::LockOrderViolation)
        ),
        "the calling thread must not acquire the catalog while holding a project guard"
    );

    // A second handle to the same root is the same caller, so the guard cannot
    // be laundered through another handle.
    let other_handle = EvidenceStore::new(&root)?;
    assert!(matches!(
        other_handle.lock_catalog(&never_cancelled()),
        Err(StoreError::LockOrderViolation)
    ));

    // Nor through a different lexical spelling of the same root. A current
    // directory component would prove nothing because Rust path comparison
    // already collapses it, so a parent component is used.
    let aliased_spelling = root.join("sibling").join("..");
    assert_ne!(
        aliased_spelling, root,
        "the alias fixture must not already compare equal"
    );
    let aliased = EvidenceStore::new(aliased_spelling)?;
    assert_eq!(aliased.root(), store.root());
    assert!(matches!(
        aliased.lock_catalog(&never_cancelled()),
        Err(StoreError::LockOrderViolation)
    ));

    drop(project_lock);
    let recovered = store.lock_catalog(&never_cancelled())?;
    drop(recovered);
    Ok(())
}

#[test]
fn a_different_store_root_cannot_launder_a_held_project_guard() -> TestResult {
    // Q26 constrains a caller that ends up holding both lock kinds. Keying the
    // ordering check on one normalised root made that rule evadable: any second
    // root the same thread can name passes the check while its project guard is
    // still held, and the two roots may address one physical store through a
    // symbolic link. This suite holds no authority to create a link, so two
    // distinct roots reproduce the identical evasion without needing one. The
    // rule is therefore about the calling thread holding a project guard at
    // all, not about which root that guard names.
    let first = temp_root("launderfirst")?;
    let second = temp_root("laundersecond")?;
    let store_a = EvidenceStore::new(&first)?;
    let store_b = EvidenceStore::new(&second)?;
    store_a.initialize()?;
    store_b.initialize()?;
    assert_ne!(
        store_a.root(),
        store_b.root(),
        "the fixture must use two genuinely different roots"
    );
    let project = allocate_project_id()?;

    let held = store_a.lock_project(&project, &never_cancelled())?;
    assert!(
        matches!(
            store_b.lock_catalog(&never_cancelled()),
            Err(StoreError::LockOrderViolation)
        ),
        "a held project guard must refuse the catalog for every root, or an          aliased root evades the ordering rule entirely"
    );
    drop(held);

    // The refusal is scoped to the guard's lifetime, not permanent.
    let catalog = store_b.lock_catalog(&never_cancelled())?;
    drop(catalog);
    Ok(())
}

#[test]
fn another_thread_holding_a_project_guard_does_not_block_the_catalog() -> TestResult {
    // The rule is per caller, not per process. Refusing an unrelated thread's
    // catalog acquisition would be stricter than canonical authority requires,
    // and it was also the shape that made the previous check racy.
    let root = temp_root("crossthread")?;
    let store = Arc::new(EvidenceStore::new(&root)?);
    store.initialize()?;
    let project = Arc::new(allocate_project_id()?);

    let (ready_tx, ready_rx) = std::sync::mpsc::channel::<()>();
    let (release_tx, release_rx) = std::sync::mpsc::channel::<()>();
    let holder = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || -> Result<(), String> {
            let guard = store
                .lock_project(&project, &|| false)
                .map_err(|error| format!("project lock: {error}"))?;
            ready_tx.send(()).map_err(|_| "ready send")?;
            release_rx.recv().map_err(|_| "release recv")?;
            drop(guard);
            Ok(())
        })
    };

    ready_rx.recv().map_err(|_| "holder never signalled")?;
    // The holder thread is definitely inside its project guard here.
    let catalog = store.lock_catalog(&never_cancelled())?;
    drop(catalog);
    release_tx.send(()).map_err(|_| "release send")?;
    holder.join().map_err(|_| "holder panicked")??;
    Ok(())
}

#[test]
fn reverse_lock_acquisition_is_refused() -> TestResult {
    // Canonical Q26 fixes catalog-before-project whenever an operation needs
    // both locks, while permitting a project-only lock for ordinary updates.
    // Holding a project guard must therefore make catalog acquisition refuse
    // rather than invert the order.
    let root = temp_root("reverseorder")?;
    let store = EvidenceStore::new(&root)?;
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
    let other_handle = EvidenceStore::new(&root)?;
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
    let aliased = EvidenceStore::new(aliased_spelling)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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

#[test]
fn an_entry_this_store_could_never_have_written_is_not_an_orphan() -> TestResult {
    // Same wider-charset gap as the reservation binding, one directory over. The
    // contract identifier charset admits `.` and `:`; safe_path_segment refuses
    // them. A directory named `g_a.b` therefore parses as a valid GenerationId
    // while being one this store can never address, and reporting it as an
    // orphan would hand a caller an identifier every later store call refuses.
    let root = temp_root("unwritableorphan")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let published = write_generation(&store, &project)?;

    let unwritable = GenerationId::try_from("g_a.b")?;
    assert!(
        safe_path_segment(unwritable.as_str()).is_err(),
        "the fixture identifier must be one the path projection refuses"
    );
    let generations = root
        .join("projects")
        .join(project.as_str())
        .join("generations");
    fs::create_dir_all(generations.join(unwritable.as_str()))?;

    let orphans = store.orphan_generations(&project)?;
    assert!(
        !orphans.contains(&unwritable),
        "an entry this store could not have written must not be reported as an orphan"
    );
    assert!(
        !orphans.contains(&published),
        "the published generation is never an orphan"
    );

    // A genuine orphan is still reported, so the binding does not silence the
    // case the function exists for.
    let second = write_generation(&store, &project)?;
    assert_ne!(second, published);
    let orphans = store.orphan_generations(&project)?;
    assert!(orphans.contains(&published));
    Ok(())
}

#[test]
fn a_defective_current_pointer_does_not_turn_the_published_generation_into_residue() -> TestResult {
    // An undetermined current generation is not an absent one. Flattening every
    // defect into "nothing is published" reported a live, validly published
    // generation as residue, which is the one classification a caller may later
    // act on destructively.
    let root = temp_root("orphandefect")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let published = write_generation(&store, &project)?;

    let current_path = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current_path, b"{ not a pointer")?;

    let outcome = store.orphan_generations(&project);
    assert!(
        matches!(
            outcome,
            Err(StoreError::Defect(StoreDefect::CurrentCorrupt))
        ),
        "a corrupt pointer must surface as a defect, not as an orphan listing"
    );

    // The repair must not silence the ordinary case: with no pointer at all,
    // nothing is published and every generation genuinely is unpublished.
    let unpublished_root = temp_root("orphannocurrent")?;
    let unpublished_store = EvidenceStore::new(&unpublished_root)?;
    unpublished_store.initialize()?;
    let bare = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;
    let lock = unpublished_store.lock_project(&bare, &never_cancelled())?;
    unpublished_store.write_generation_record(
        &lock,
        &bare,
        &generation,
        &record,
        IDENTITY_PAYLOAD,
    )?;
    drop(lock);
    let orphans = unpublished_store.orphan_generations(&bare)?;
    assert!(
        orphans.contains(&generation),
        "with no pointer at all, an unpublished generation is still an orphan"
    );
    assert!(!orphans.contains(&published));
    Ok(())
}

// ---------------------------------------------------------------------------
// S2-E014 failure injection at every commit boundary
// ---------------------------------------------------------------------------

#[test]
fn interrupted_generation_never_becomes_current() -> TestResult {
    // Records written but manifest never written: publication must refuse.
    let root = temp_root("nomanifest")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;
    store.write_generation_record(&lock, &project, &generation, &record, b"{}")?;

    // The generation was never closed, and no pointer names it. Reporting a
    // dangling `CURRENT` here would describe a pointer that does not exist.
    let outcome = store.publish_generation(&lock, &project, &generation);
    assert!(matches!(
        outcome,
        Err(StoreError::Defect(StoreDefect::GenerationManifestMissing))
    ));
    assert!(store.read_published_generation(&project).is_err());
    Ok(())
}

#[cfg(unix)]
#[test]
fn an_unreadable_closure_state_is_refused_before_any_write_effect() -> TestResult {
    // Scope of this test, stated precisely. It proves that when the closure
    // state of a generation cannot be read at all, the store refuses and
    // performs no write effect, rather than reading the failure as "not closed"
    // and proceeding.
    //
    // It is Unix-only because the fixture depends on a POSIX metadata error:
    // resolving a path whose prefix component is a regular file fails with
    // ENOTDIR, while Windows reports that same shape as an ordinary
    // path-not-found and so cannot reach the error branch at all. The Windows
    // side of this behaviour is therefore not covered here.
    //
    // What separates the two implementations is the side effect. Both fail, but
    // the previous one turned the metadata error into `false`, decided the
    // generation was open, and went on to create its temporary directory before
    // the destination write failed for the same underlying reason.
    let root = temp_root("closurestate")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;

    let project_dir = root.join("projects").join(project.as_str());
    let generations = project_dir.join("generations");
    fs::create_dir_all(&generations)?;
    // The generation "directory" is a regular file, so every metadata call
    // through it fails instead of reporting absence.
    fs::write(generations.join(generation.as_str()), b"not a directory")?;

    let temp_dir = project_dir.join("tmp");
    assert!(
        !temp_dir.exists(),
        "the fixture must start with no temporary directory"
    );

    let outcome = store.write_generation_record(&lock, &project, &generation, &record, b"{}");
    assert!(
        matches!(outcome, Err(StoreError::Io(_))),
        "an unreadable closure state must fail rather than be read as open"
    );
    assert!(
        !temp_dir.exists(),
        "the store must perform no write effect when it cannot determine closure"
    );
    Ok(())
}

#[test]
fn manifest_referencing_a_missing_record_is_refused_at_publish() -> TestResult {
    let root = temp_root("missingrecord")?;
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
fn a_current_pointer_naming_an_unaddressable_generation_is_corrupt() -> TestResult {
    // The generation identifier came off disk, so an identifier this store could
    // never address is a property of the persisted pointer, not of the caller.
    // Before this was classified, the read returned StoreError::UnsafeIdentifier,
    // which reports an argument fault for bytes no caller chose.
    let root = temp_root("unaddressablecurrent")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;

    let unaddressable = GenerationId::try_from("g_a.b")?;
    assert!(
        safe_path_segment(unaddressable.as_str()).is_err(),
        "the fixture identifier must be one the path projection refuses"
    );
    let current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: unaddressable,
        manifest_digest: content_digest(b"{}")?,
    };
    fs::write(
        root.join("projects").join(project.as_str()).join("CURRENT"),
        canonical_project_json(&current)?,
    )?;

    assert!(
        matches!(
            store.read_published_generation(&project),
            Err(StoreError::Defect(StoreDefect::CurrentCorrupt))
        ),
        "a pointer naming an unaddressable generation is a defective pointer"
    );
    Ok(())
}

#[test]
fn current_pointing_at_a_missing_generation_is_detected() -> TestResult {
    let root = temp_root("danglingcurrent")?;
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
fn a_persisted_artifact_of_exactly_the_limit_is_accepted_and_one_byte_more_is_not() -> TestResult {
    // The read window is the untaken allowance plus a single probe byte, so the
    // boundary is where that arithmetic is load-bearing: at exactly the limit the
    // window is one byte, and whether that byte arrives decides the outcome.
    //
    // This does not fail against the previous implementation, and that is stated
    // rather than left to be assumed: the previous loop accepted and refused the
    // same two files. What changed is how much it read from the file before
    // deciding, which no portable assertion can observe. The byte figure is
    // established by the loop and documented there; this test pins the boundary
    // the arithmetic has to get right.
    let root = temp_root("readboundary")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let exact_record = allocate_record_id()?;
    let lock = store.lock_project(&project, &never_cancelled())?;

    // Exactly at the limit is valid, on the write side and on the read side.
    let exact = vec![b'x'; MAX_RECORD_BYTES];
    let digest =
        store.write_generation_record(&lock, &project, &generation, &exact_record, &exact)?;
    let record_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("records")
        .join(format!("{}.json", exact_record.as_str()));
    assert_eq!(fs::read(&record_path)?.len(), MAX_RECORD_BYTES);

    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        exact_record.clone(),
        exact_record.clone(),
        EvidenceRecordRefs::try_from(Vec::new())?,
        vec![digest],
        UnixMillis::new(1),
    )?;
    store.write_generation_manifest(&lock, &manifest)?;
    store.publish_generation(&lock, &project, &generation)?;
    let published = store.read_published_generation(&project)?;
    let bytes = store.read_generation_record(&published.manifest, &exact_record)?;
    assert_eq!(bytes.len(), MAX_RECORD_BYTES);

    // One byte more is refused, and as a store defect rather than a read error.
    fs::write(&record_path, vec![b'x'; MAX_RECORD_BYTES + 1])?;
    assert!(matches!(
        store.read_generation_record(&published.manifest, &exact_record),
        Err(StoreError::Defect(StoreDefect::RecordCorrupt))
    ));
    Ok(())
}

#[test]
fn an_oversized_persisted_manifest_is_classified_as_corrupt() -> TestResult {
    // The StoreDefect documentation says an over-limit manifest is corrupt. The
    // read paths returned the bounded-read refusal instead, so one corruption
    // carried two classes depending on how it was produced. A caller-supplied
    // oversized value is still an argument error; bytes already on disk are not.
    let root = temp_root("oversizemanifest")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = write_generation(&store, &project)?;

    let manifest_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    fs::write(&manifest_path, vec![b'x'; MAX_MANIFEST_BYTES + 1])?;

    assert!(
        matches!(
            store.read_published_generation(&project),
            Err(StoreError::Defect(StoreDefect::ManifestCorrupt))
        ),
        "an over-limit persisted manifest must be a store defect"
    );
    assert!(matches!(
        store.validate_generation(&project, &generation),
        Err(StoreError::Defect(StoreDefect::ManifestCorrupt))
    ));
    Ok(())
}

#[test]
fn an_oversized_persisted_record_is_classified_as_corrupt() -> TestResult {
    let root = temp_root("oversizerecord")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    write_generation(&store, &project)?;

    let published = store.read_published_generation(&project)?;
    let record_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(published.manifest.generation_id.as_str())
        .join("records")
        .join(format!(
            "{}.json",
            published.manifest.identity_record_ref.as_str()
        ));
    fs::write(&record_path, vec![b'x'; MAX_RECORD_BYTES + 1])?;

    assert!(
        matches!(
            store.read_generation_record(
                &published.manifest,
                &published.manifest.identity_record_ref
            ),
            Err(StoreError::Defect(StoreDefect::RecordCorrupt))
        ),
        "an over-limit persisted record must be a store defect"
    );
    assert!(matches!(
        store.read_published_generation(&project),
        Err(StoreError::Defect(StoreDefect::RecordCorrupt))
    ));
    Ok(())
}

#[test]
fn an_oversized_reservation_is_classified_the_same_way_by_both_apis() -> TestResult {
    // Same rule as the malformed-reservation case: one corruption, one class,
    // whichever API observes it. Enumeration must also keep reporting the other
    // entries rather than aborting on the oversized one.
    let root = temp_root("oversizereservation")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let facts = facts_at("/projects/oversize")?;
    let good = allocate_project_id()?;
    let bad = allocate_project_id()?;
    let catalog = store.lock_catalog(&never_cancelled())?;
    store.write_reservation(
        &catalog,
        &build_reservation(good, &facts, UnixMillis::new(1))?,
    )?;
    drop(catalog);

    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", bad.as_str()));
    fs::write(&path, vec![b'x'; MAX_RECORD_BYTES + 1])?;

    assert!(matches!(
        store.read_reservation(&bad),
        Err(StoreError::Defect(StoreDefect::RecordCorrupt))
    ));

    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 2, "the valid entry must still be enumerated");
    assert_eq!(
        listed
            .iter()
            .filter(|entry| matches!(entry, Err(StoreDefect::RecordCorrupt)))
            .count(),
        1
    );
    assert_eq!(listed.iter().filter(|entry| entry.is_ok()).count(), 1);
    Ok(())
}

#[test]
fn an_unsupported_producer_contract_version_is_refused_at_publish_and_read() -> TestResult {
    // The producer contract version records what the writer meant by the fields,
    // which the serialization schema version does not capture. A reader that
    // accepted any value would make the field decorative and would adopt a
    // generation whose semantics it does not implement.
    let root = temp_root("producerversion")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let identity_record = allocate_record_id()?;
    let index_record = allocate_record_id()?;

    let lock = store.lock_project(&project, &never_cancelled())?;
    let identity_digest = store.write_generation_record(
        &lock,
        &project,
        &generation,
        &identity_record,
        IDENTITY_PAYLOAD,
    )?;
    let index_digest = store.write_generation_record(
        &lock,
        &project,
        &generation,
        &index_record,
        INDEX_PAYLOAD,
    )?;
    let mut manifest = build_manifest(
        project.clone(),
        generation.clone(),
        identity_record,
        index_record,
        EvidenceRecordRefs::try_from(Vec::new())?,
        vec![identity_digest, index_digest],
        UnixMillis::new(1),
    )?;
    manifest.producer_contract_version = PRODUCER_CONTRACT_VERSION + 1;
    store.write_generation_manifest(&lock, &manifest)?;

    // Publication refuses it, so this generation can never become current
    // through the supported path.
    assert!(
        matches!(
            store.publish_generation(&lock, &project, &generation),
            Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion
            ))
        ),
        "an unsupported producer contract must not be publishable"
    );

    // A writer-capable actor can still point CURRENT at it directly, with a
    // matching manifest digest, so the read path must refuse it as well. The
    // digest agrees; only the producer contract does not.
    let manifest_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    let manifest_bytes = fs::read(&manifest_path)?;
    let current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: generation,
        manifest_digest: content_digest(&manifest_bytes)?,
    };
    let current_path = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current_path, canonical_project_json(&current)?)?;

    assert!(
        matches!(
            store.read_published_generation(&project),
            Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion
            ))
        ),
        "a coherent generation from an unsupported producer must not be read as current"
    );

    // read_generation_record takes an ordinary public manifest, so it is a
    // public entry point of its own. Refusing only in read_published_generation
    // would leave the boundary bypassable by anyone holding a manifest value.
    let identity_ref = manifest.identity_record_ref.clone();
    assert!(
        matches!(
            store.read_generation_record(&manifest, &identity_ref),
            Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion
            ))
        ),
        "a record must not be readable through a manifest from an unsupported producer"
    );
    Ok(())
}

#[test]
fn the_evidence_reference_cap_holds_on_both_the_constructor_and_the_disk_path() -> TestResult {
    // This is what makes the aggregate read ceiling real. The per-artifact bound
    // caps one read; the reference cap is what stops a generation from holding
    // an unbounded number of them, and it has to hold on the persisted path as
    // well as on the constructor, because a manifest read back from disk is
    // never one this process built.
    //
    // With both caps the worst case is arithmetic:
    //     (2 + MAX_EVIDENCE_REFS) * MAX_RECORD_BYTES
    // for records, plus one bounded manifest and one bounded pointer.
    //
    // This test passes against the previous implementation as well, and that is
    // deliberate rather than a weakness: the caps were already enforced, and
    // what was defective was the documentation claiming no aggregate ceiling
    // existed. The test pins the two properties that claim now rests on, so a
    // later change to either cap fails here instead of quietly invalidating the
    // stated worst case.
    let mut too_many = Vec::with_capacity(MAX_EVIDENCE_REFS + 1);
    for _ in 0..=MAX_EVIDENCE_REFS {
        too_many.push(allocate_record_id()?);
    }
    assert_eq!(too_many.len(), MAX_EVIDENCE_REFS + 1);
    assert!(
        EvidenceRecordRefs::try_from(too_many.clone()).is_err(),
        "the constructor must refuse more references than the contract admits"
    );

    // The persisted path. A manifest carrying an over-length reference list must
    // not decode, so no read can be driven past the derived ceiling by bytes on
    // disk.
    let root = temp_root("evidencecap")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let project = allocate_project_id()?;
    let generation = write_generation(&store, &project)?;

    let manifest_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    let text =
        String::from_utf8(fs::read(&manifest_path)?).map_err(|_| "canonical JSON must be UTF-8")?;
    let refs = too_many
        .iter()
        .map(|record| format!("\"{}\"", record.as_str()))
        .collect::<Vec<_>>()
        .join(",");
    let inflated = text.replace(
        "\"evidence_record_refs\":[]",
        &format!("\"evidence_record_refs\":[{refs}]"),
    );
    assert_ne!(
        inflated, text,
        "the fixture must actually inflate the reference list"
    );
    fs::write(&manifest_path, inflated.as_bytes())?;

    // Repoint CURRENT so the digest check cannot mask what is under test.
    let manifest_bytes = fs::read(&manifest_path)?;
    let current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: generation,
        manifest_digest: content_digest(&manifest_bytes)?,
    };
    fs::write(
        root.join("projects").join(project.as_str()).join("CURRENT"),
        canonical_project_json(&current)?,
    )?;

    assert!(
        matches!(
            store.read_published_generation(&project),
            Err(StoreError::Defect(StoreDefect::ManifestCorrupt))
        ),
        "an over-length reference list must not decode from disk"
    );

    // Control. The same fixture at exactly the cap must decode, and then fail
    // later for the ordinary reason that its referenced records do not exist.
    // Without this the assertion above would prove only that something went
    // wrong, not that the reference cap is what stopped it.
    let at_cap = too_many[..MAX_EVIDENCE_REFS]
        .iter()
        .map(|record| format!("\"{}\"", record.as_str()))
        .collect::<Vec<_>>()
        .join(",");
    let capped = text.replace(
        "\"evidence_record_refs\":[]",
        &format!("\"evidence_record_refs\":[{at_cap}]"),
    );
    fs::write(&manifest_path, capped.as_bytes())?;
    let capped_bytes = fs::read(&manifest_path)?;
    let capped_current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: current.generation_id.clone(),
        manifest_digest: content_digest(&capped_bytes)?,
    };
    fs::write(
        root.join("projects").join(project.as_str()).join("CURRENT"),
        canonical_project_json(&capped_current)?,
    )?;
    assert!(
        matches!(
            store.read_published_generation(&project),
            Err(StoreError::Defect(StoreDefect::RecordMissing))
        ),
        "exactly at the cap the manifest must decode and fail on its missing records"
    );
    Ok(())
}

#[test]
fn a_manifest_beyond_the_digest_bound_reports_the_bound_not_the_count() -> TestResult {
    // `limit` names the limit that was exceeded. Reporting the observed count
    // there tells a caller the bound is whatever they happened to send, which is
    // precisely backwards when the message reads "exceeds bounded limit N".
    let project = allocate_project_id()?;
    let generation = allocate_generation_id()?;
    let mut digests = Vec::with_capacity(MAX_RECORD_DIGESTS + 1);
    for _ in 0..=MAX_RECORD_DIGESTS {
        digests.push(RecordDigest {
            record_id: allocate_record_id()?,
            digest: content_digest(b"{}")?,
        });
    }
    assert_eq!(digests.len(), MAX_RECORD_DIGESTS + 1);

    let outcome = build_manifest(
        project,
        generation,
        allocate_record_id()?,
        allocate_record_id()?,
        EvidenceRecordRefs::try_from(Vec::new())?,
        digests,
        UnixMillis::new(1),
    );
    let Err(StoreError::TooLarge { limit }) = outcome else {
        return Err("a manifest beyond the digest bound must be refused".into());
    };
    assert_eq!(
        limit, MAX_RECORD_DIGESTS,
        "limit must name the bound, not the observed count"
    );
    Ok(())
}

#[test]
fn oversized_record_is_refused_before_it_is_written() -> TestResult {
    let root = temp_root("oversize")?;
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
fn both_reservation_apis_classify_one_corruption_the_same_way() -> TestResult {
    // FR-023 requires malformed persisted records to be treated as invalid.
    // One corrupt reservation must therefore carry one classification, not a
    // codec error through one API and a store defect through another.
    let root = temp_root("corruptclass")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let facts = facts_at("/projects/classify")?;
    let project = allocate_project_id()?;
    let reservation = build_reservation(project.clone(), &facts, UnixMillis::new(1))?;
    let catalog = store.lock_catalog(&never_cancelled())?;
    store.write_reservation(&catalog, &reservation)?;
    drop(catalog);

    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", project.as_str()));
    fs::write(&path, b"{ not valid json")?;

    // Single-record read.
    let single = store.read_reservation(&project);
    assert!(
        matches!(single, Err(StoreError::Defect(StoreDefect::RecordCorrupt))),
        "read_reservation must report a store defect, not a codec error"
    );

    // Enumeration of the same record.
    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1);
    assert!(matches!(
        listed.first(),
        Some(Err(StoreDefect::RecordCorrupt))
    ));
    Ok(())
}

#[test]
fn a_reservation_bound_to_another_project_is_a_typed_defect() -> TestResult {
    // A reservation names a project twice: once in the path it is stored under
    // and once in the bytes it carries. Nothing forced those to agree, so a
    // syntactically valid reservation for one project could sit at another
    // project's path and be returned as that project's reservation. Recovery
    // would then resume an identity this store never reserved under that name.
    let root = temp_root("misboundreservation")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let facts = facts_at("/projects/misbound")?;
    let owner = allocate_project_id()?;
    let intruder = allocate_project_id()?;
    assert_ne!(owner, intruder, "the fixture needs two distinct projects");

    // Both halves are individually well formed. Only their binding is wrong,
    // which is why a decode-only check cannot catch this.
    let foreign = build_reservation(intruder, &facts, UnixMillis::new(1))?;
    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", owner.as_str()));
    fs::create_dir_all(path.parent().ok_or("reservation path needs a parent")?)?;
    fs::write(&path, canonical_project_json(&foreign)?)?;

    assert!(
        matches!(
            store.read_reservation(&owner),
            Err(StoreError::Defect(StoreDefect::ProjectMismatch))
        ),
        "a reservation naming another project must not be returned as this one's"
    );

    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1, "the misbound file must still be observed");
    let entry = listed
        .into_iter()
        .next()
        .ok_or("one entry must be listed")?;
    assert!(
        matches!(entry, Err(StoreDefect::ProjectMismatch)),
        "enumeration must classify the same record the same way"
    );
    Ok(())
}

#[test]
fn an_unsupported_persisted_schema_version_is_reported_as_corruption() -> TestResult {
    // This pins what actually happens, not what the defect names suggest.
    //
    // `StoreDefect::UnsupportedSchemaVersion` exists and this module checks for
    // it, but the contract codec rejects an unknown `schema_version` while
    // decoding, so no persisted record can reach those checks: a future version
    // fails to decode and arrives as the corresponding corruption class instead.
    // Separating the two would mean reading the version before decoding the
    // record, which needs a version-tolerant decoder in the contract layer or a
    // JSON parser here, and this tranche has authority for neither.
    //
    // The behaviour is recorded rather than assumed, so a later codec change
    // makes this test fail instead of quietly turning dead guards live.
    let root = temp_root("schemaversion")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let facts = facts_at("/projects/schemaversion")?;
    let project = allocate_project_id()?;

    let bump = |bytes: Vec<u8>| -> Result<Vec<u8>, TestError> {
        let text = String::from_utf8(bytes).map_err(|_| "canonical JSON must be UTF-8")?;
        let bumped = text.replace("\"schema_version\":1", "\"schema_version\":2");
        if bumped == text {
            return Err("the fixture must actually change the schema version".into());
        }
        Ok(bumped.into_bytes())
    };

    // A reservation from a future contract version.
    let reservation = build_reservation(project.clone(), &facts, UnixMillis::new(1))?;
    let reservation_path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", project.as_str()));
    fs::create_dir_all(reservation_path.parent().ok_or("reservation parent")?)?;
    fs::write(
        &reservation_path,
        bump(canonical_project_json(&reservation)?)?,
    )?;

    assert!(
        matches!(
            store.read_reservation(&project),
            Err(StoreError::Defect(StoreDefect::RecordCorrupt))
        ),
        "a future reservation version currently arrives as corruption, not as an unsupported version"
    );
    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1);
    assert!(matches!(
        listed
            .into_iter()
            .next()
            .ok_or("one entry must be listed")?,
        Err(StoreDefect::RecordCorrupt)
    ));

    // A manifest from a future contract version, with `CURRENT` updated so the
    // digest check cannot mask the classification under test.
    let manifest_project = allocate_project_id()?;
    let generation = write_generation(&store, &manifest_project)?;
    let manifest_path = root
        .join("projects")
        .join(manifest_project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    let bumped_manifest = bump(fs::read(&manifest_path)?)?;
    fs::write(&manifest_path, &bumped_manifest)?;
    let current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: manifest_project.clone(),
        generation_id: generation,
        manifest_digest: content_digest(&bumped_manifest)?,
    };
    fs::write(
        root.join("projects")
            .join(manifest_project.as_str())
            .join("CURRENT"),
        canonical_project_json(&current)?,
    )?;

    assert!(
        matches!(
            store.read_published_generation(&manifest_project),
            Err(StoreError::Defect(StoreDefect::ManifestCorrupt))
        ),
        "a future manifest version currently arrives as corruption too"
    );
    Ok(())
}

#[test]
fn a_reservation_this_store_could_never_have_written_is_a_typed_defect() -> TestResult {
    // The contract identifier charset is wider than the path projection: it
    // admits `.` and `:`, which safe_path_segment refuses. So an identifier can
    // be perfectly valid as a contract value and still be one this store can
    // never write or address.
    //
    // Binding a reservation to its filename alone accepted exactly that case,
    // because the record and the name agreed with each other while agreeing on
    // something unwritable. Enumeration then handed a caller a reservation for a
    // project it could not open. The binding is a path comparison now, so the
    // record is valid only where this store itself would have filed it.
    let root = temp_root("unwritablereservation")?;
    let store = EvidenceStore::new(&root)?;
    store.initialize()?;
    let facts = facts_at("/projects/unwritable")?;

    let unwritable = ProjectId::try_from("p_a.b")?;
    assert!(
        safe_path_segment(unwritable.as_str()).is_err(),
        "the fixture identifier must be one the path projection refuses"
    );

    let reservation = build_reservation(unwritable.clone(), &facts, UnixMillis::new(1))?;
    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", unwritable.as_str()));
    fs::create_dir_all(path.parent().ok_or("reservation parent")?)?;
    fs::write(&path, canonical_project_json(&reservation)?)?;

    let listed = store.list_reservations()?;
    assert_eq!(listed.len(), 1, "the file must still be observed");
    assert!(
        matches!(
            listed
                .into_iter()
                .next()
                .ok_or("one entry must be listed")?,
            Err(StoreDefect::ProjectMismatch)
        ),
        "a reservation at a path this store could not have written must not enumerate as valid"
    );
    Ok(())
}

#[test]
fn corrupt_reservation_is_reported_rather_than_skipped() -> TestResult {
    // Silently skipping a corrupt reservation would let a second identity be
    // allocated for an already-reserved project.
    let root = temp_root("corruptreservation")?;
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
    let store = Arc::new(EvidenceStore::new(&root)?);
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
    let store = Arc::new(EvidenceStore::new(&root)?);
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
    let store = Arc::new(EvidenceStore::new(&root)?);
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
            let mut coherent_reads = 0_usize;
            for _ in 0..25 {
                match store.read_published_generation(&project) {
                    Ok(published) => {
                        // Asserting that the pointer and the manifest name the
                        // same generation would prove nothing here, because
                        // `read_published_generation` already refuses that case
                        // internally and can only return `Ok` when they agree.
                        // What the reader must establish is that the generation
                        // it just selected stays completely readable and
                        // digest-exact while a writer publishes over it.
                        let bytes = store
                            .read_generation_record(
                                &published.manifest,
                                &published.manifest.identity_record_ref,
                            )
                            .map_err(|error| {
                                format!("selected generation was not readable: {error}")
                            })?;
                        if bytes != IDENTITY_PAYLOAD {
                            return Err("selected generation returned foreign bytes".to_owned());
                        }
                        coherent_reads += 1;
                    }
                    // A structural defect during an ordinary concurrent publish
                    // is a real failure. Swallowing it would leave this test
                    // unable to fail for the property it is named after.
                    Err(StoreError::Defect(defect)) => {
                        return Err(format!("reader observed a store defect: {defect}"));
                    }
                    // A transient sharing or permission error while the pointer
                    // is being replaced is an operating-system condition rather
                    // than an incoherent store, so it is tolerated and not
                    // counted as a successful read.
                    Err(StoreError::Io(_)) => {}
                    Err(error) => return Err(format!("unexpected read error: {error}")),
                }
            }
            if coherent_reads == 0 {
                return Err("the reader completed no read at all".to_owned());
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
    let store = EvidenceStore::new(&root)?;
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
    let store = EvidenceStore::new(&root)?;
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
        let store = EvidenceStore::new(&root)?;
        store.initialize()?;
        write_generation(&store, &project)?;
    }

    let reopened = EvidenceStore::new(&root)?;
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
