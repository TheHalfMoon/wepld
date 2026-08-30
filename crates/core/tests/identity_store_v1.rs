//! S2 identity and evidence-store qualification suite.
//!
//! Covered tasks: S2-I013, S2-I014, S2-E013, S2-E014, S2-E015, S2-E016, plus
//! direct coverage of the identity ordering, reservation, bounded-read,
//! generation, publication, freshness, redaction, and authenticity behaviours
//! implemented for S2-I008..S2-I012 and S2-E003..S2-E012, S2-E017.

use std::fs;
use std::io::Write as _;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering as AtomicOrdering};
use std::thread;
use std::time::Instant;

use wepld_contracts::{
    EvidenceRecordRefs, EvidenceStatus, FreshnessBasis, GenerationId, IdentityConflictKind,
    IdentityMatchStrength, IdentityRecordState, IdentityReservationState, IdentityResolution,
    MachinePath, Observation, ProjectContractVersion, ProjectCurrentRef, ProjectId, ProjectLocator,
    RecordDigest, StoreAuthenticity, StoreLockScope, UnixMillis, canonical_project_json,
};
use wepld_core::evidence_store::{EvidenceStore, StoreDefect, StoreError};
use wepld_core::identity::{
    IdentityCandidate, ProjectMatchFacts, ReservationRecovery, allocate_generation_id,
    allocate_project_id, allocate_record_id, allocate_worktree_id, build_identity_record,
    build_reservation, compare_match_strength, complete_reservation, match_strength_rank,
    recover_reservation, resolve_identity,
};
use wepld_core::{
    build_manifest, busy_error_code, content_digest, redacted_summary, safe_path_segment,
};

// ---------------------------------------------------------------------------
// fixtures
// ---------------------------------------------------------------------------

fn temp_root(name: &str) -> PathBuf {
    let mut root = PathBuf::from(env!("CARGO_TARGET_TMPDIR"));
    let mut token = [0_u8; 8];
    getrandom_fill(&mut token);
    let mut suffix = String::new();
    for byte in token {
        suffix.push_str(&format!("{byte:02x}"));
    }
    root.push(format!("wepld-s2-{name}-{suffix}"));
    let _ = fs::create_dir_all(&root);
    root
}

fn getrandom_fill(buffer: &mut [u8]) {
    // Tests derive uniqueness from the same OS randomness the store uses.
    let id = allocate_record_id().expect("record id allocation");
    let bytes = id.as_str().as_bytes();
    for (slot, byte) in buffer.iter_mut().zip(bytes.iter().rev()) {
        *slot = *byte;
    }
}

fn cleanup(root: &Path) {
    let _ = fs::remove_dir_all(root);
}

fn locator_at(path: &str, observed_at: u64) -> ProjectLocator {
    let machine = MachinePath::utf8(path).expect("machine path");
    ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: machine.clone(),
        lexical_absolute_path: machine.clone(),
        resolved_path: Observation::Available { value: machine },
        observation_time: UnixMillis::new(observed_at),
    }
}

fn facts_at(path: &str) -> ProjectMatchFacts {
    ProjectMatchFacts::new(locator_at(path, 1_000))
}

fn candidate(
    project_id: &ProjectId,
    facts: &ProjectMatchFacts,
    state: IdentityRecordState,
) -> IdentityCandidate {
    IdentityCandidate {
        project_id: project_id.clone(),
        facts_digest: facts.facts_digest().expect("facts digest"),
        anchor_digest: facts.anchor_digest().expect("anchor digest"),
        state,
    }
}

/// Write one complete generation and publish it. Returns the generation id.
fn write_generation(store: &EvidenceStore, project: &ProjectId) -> GenerationId {
    let generation = allocate_generation_id().expect("generation id");
    let identity_record = allocate_record_id().expect("identity record id");
    let index_record = allocate_record_id().expect("index record id");

    let identity_bytes = b"{\"kind\":\"identity\"}".to_vec();
    let index_bytes = b"{\"kind\":\"index\"}".to_vec();

    let identity_digest = store
        .write_generation_record(project, &generation, &identity_record, &identity_bytes)
        .expect("write identity record");
    let index_digest = store
        .write_generation_record(project, &generation, &index_record, &index_bytes)
        .expect("write index record");

    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        identity_record,
        index_record,
        EvidenceRecordRefs::try_from(Vec::new()).expect("empty refs"),
        vec![identity_digest, index_digest],
        UnixMillis::new(10_000),
    )
    .expect("build manifest");
    store
        .write_generation_manifest(&manifest)
        .expect("write manifest");
    store
        .publish_generation(project, &generation)
        .expect("publish generation");
    generation
}

fn never_cancelled() -> impl Fn() -> bool {
    || false
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
fn exact_binding_outranks_reassociation_regardless_of_input_order() {
    let anchor = MachinePath::utf8("/anchor").expect("anchor");
    let exact_facts = facts_at("/projects/alpha");
    let moved_facts =
        ProjectMatchFacts::with_anchor(locator_at("/projects/alpha", 1_000), anchor.clone());

    let exact_id = ProjectId::try_from("p_exact").expect("exact id");
    let moved_id = ProjectId::try_from("p_moved").expect("moved id");

    let exact_candidate = candidate(&exact_id, &exact_facts, IdentityRecordState::Active);
    let mut reassociation_candidate =
        candidate(&moved_id, &moved_facts, IdentityRecordState::Active);
    // Different facts, same anchor: a genuine move.
    reassociation_candidate.facts_digest = facts_at("/old/location")
        .facts_digest()
        .expect("old facts digest");

    for ordering in [
        vec![exact_candidate.clone(), reassociation_candidate.clone()],
        vec![reassociation_candidate, exact_candidate],
    ] {
        let resolved = resolve_identity(&moved_facts, &ordering).expect("resolve");
        match resolved {
            IdentityResolution::Existing {
                project_id,
                strength,
            } => {
                assert_eq!(project_id, exact_id);
                assert_eq!(strength, IdentityMatchStrength::ExactBinding);
            }
            other => panic!("expected exact binding, got {other:?}"),
        }
    }
}

// ---------------------------------------------------------------------------
// S2-I009 / S2-I013 adversarial identity fixtures
// ---------------------------------------------------------------------------

#[test]
fn filesystem_copy_does_not_adopt_the_source_identity() {
    // A copy sits at a different path and carries no shared stable anchor.
    // It must not silently become the same local project.
    let source = facts_at("/projects/original");
    let copy = facts_at("/projects/original-copy");
    let source_id = ProjectId::try_from("p_source").expect("source id");

    let resolved = resolve_identity(
        &copy,
        &[candidate(&source_id, &source, IdentityRecordState::Active)],
    )
    .expect("resolve");

    match resolved {
        IdentityResolution::Ambiguous { candidates } => {
            assert!(candidates.as_slice().is_empty());
        }
        other => panic!("copy must not resolve to an existing identity, got {other:?}"),
    }
}

#[test]
fn independent_clone_does_not_adopt_the_source_identity() {
    // Overlapping content and remotes are not identity. Without a shared
    // explicit anchor an independent clone stays a separate project.
    let source = facts_at("/checkouts/repo-a");
    let clone = facts_at("/checkouts/repo-b");
    let source_id = ProjectId::try_from("p_clonesource").expect("id");

    let resolved = resolve_identity(
        &clone,
        &[candidate(&source_id, &source, IdentityRecordState::Active)],
    )
    .expect("resolve");
    assert!(matches!(resolved, IdentityResolution::Ambiguous { .. }));
}

#[test]
fn linked_worktrees_do_not_collapse_into_one_project() {
    // Two worktrees of one repository have distinct roots. Each keeps its own
    // per-worktree identity rather than collapsing into a single object.
    let primary = facts_at("/repo/main-worktree");
    let linked = facts_at("/repo/feature-worktree");
    let primary_id = ProjectId::try_from("p_primary").expect("id");

    let resolved = resolve_identity(
        &linked,
        &[candidate(
            &primary_id,
            &primary,
            IdentityRecordState::Active,
        )],
    )
    .expect("resolve");
    assert!(matches!(resolved, IdentityResolution::Ambiguous { .. }));
}

#[test]
fn move_with_shared_anchor_reassociates_conservatively() {
    let anchor = MachinePath::utf8("/stable/anchor").expect("anchor");
    let before =
        ProjectMatchFacts::with_anchor(locator_at("/projects/before", 1_000), anchor.clone());
    let after = ProjectMatchFacts::with_anchor(locator_at("/projects/after", 2_000), anchor);
    let project_id = ProjectId::try_from("p_moved").expect("id");

    let resolved = resolve_identity(
        &after,
        &[candidate(&project_id, &before, IdentityRecordState::Active)],
    )
    .expect("resolve");

    match resolved {
        IdentityResolution::Existing {
            project_id: resolved_id,
            strength,
        } => {
            assert_eq!(resolved_id, project_id);
            assert_eq!(strength, IdentityMatchStrength::StrongReassociation);
        }
        other => panic!("expected strong reassociation, got {other:?}"),
    }
}

#[test]
fn two_equally_strong_candidates_are_a_conflict_not_a_guess() {
    let facts = facts_at("/projects/shared");
    let first = ProjectId::try_from("p_first").expect("id");
    let second = ProjectId::try_from("p_second").expect("id");

    let resolved = resolve_identity(
        &facts,
        &[
            candidate(&first, &facts, IdentityRecordState::Active),
            candidate(&second, &facts, IdentityRecordState::Active),
        ],
    )
    .expect("resolve");

    match resolved {
        IdentityResolution::Conflict { kind, candidates } => {
            assert_eq!(kind, IdentityConflictKind::MultipleStrongCandidates);
            assert_eq!(candidates.as_slice().len(), 2);
        }
        other => panic!("expected conflict, got {other:?}"),
    }
}

#[test]
fn recorded_conflict_is_sticky_and_not_overridden_by_a_fresh_match() {
    let facts = facts_at("/projects/conflicted");
    let project_id = ProjectId::try_from("p_conflicted").expect("id");

    let resolved = resolve_identity(
        &facts,
        &[candidate(
            &project_id,
            &facts,
            IdentityRecordState::Conflict,
        )],
    )
    .expect("resolve");

    match resolved {
        IdentityResolution::Conflict { kind, candidates } => {
            assert_eq!(kind, IdentityConflictKind::ContradictoryTopology);
            assert_eq!(candidates.as_slice().len(), 1);
        }
        other => panic!("expected sticky conflict, got {other:?}"),
    }
}

// ---------------------------------------------------------------------------
// S2-I011 / S2-I012 reservation and crash recovery
// ---------------------------------------------------------------------------

#[test]
fn reservation_round_trips_and_completes() {
    let facts = facts_at("/projects/reserved");
    let project_id = allocate_project_id().expect("project id");
    let reservation =
        build_reservation(project_id.clone(), &facts, UnixMillis::new(5)).expect("reservation");

    assert_eq!(reservation.state, IdentityReservationState::Reserved);
    assert_eq!(
        reservation.revalidated_match_facts_digest,
        facts.facts_digest().expect("digest")
    );

    let completed = complete_reservation(&reservation, &project_id, UnixMillis::new(9))
        .expect("complete reservation");
    assert_eq!(completed.state, IdentityReservationState::Initialized);
    assert_eq!(completed.project_id, project_id);
    assert_eq!(completed.created_at.get(), 5);
    assert_eq!(completed.updated_at.get(), 9);
}

#[test]
fn completing_a_reservation_for_another_project_is_rejected() {
    let facts = facts_at("/projects/reserved");
    let owner = allocate_project_id().expect("owner id");
    let other = allocate_project_id().expect("other id");
    let reservation = build_reservation(owner, &facts, UnixMillis::new(1)).expect("reservation");
    assert!(complete_reservation(&reservation, &other, UnixMillis::new(2)).is_err());
}

#[test]
fn crashed_reservation_resumes_the_same_project_id() {
    // S2-I012. A crash between `reserved` and `initialized` must never allocate
    // a second identity for the same facts.
    let facts = facts_at("/projects/crashed");
    let project_id = allocate_project_id().expect("project id");
    let reservation =
        build_reservation(project_id.clone(), &facts, UnixMillis::new(1)).expect("reservation");

    match recover_reservation(&reservation, &facts).expect("recover") {
        ReservationRecovery::ResumeSameProject {
            project_id: resumed,
        } => assert_eq!(resumed, project_id),
        other => panic!("expected resume, got {other:?}"),
    }
}

#[test]
fn reservation_for_different_facts_is_not_adopted() {
    let facts = facts_at("/projects/a");
    let other_facts = facts_at("/projects/b");
    let project_id = allocate_project_id().expect("project id");
    let reservation =
        build_reservation(project_id, &facts, UnixMillis::new(1)).expect("reservation");

    assert_eq!(
        recover_reservation(&reservation, &other_facts).expect("recover"),
        ReservationRecovery::Mismatch
    );
}

#[test]
fn initialized_reservation_reports_already_initialized() {
    let facts = facts_at("/projects/done");
    let project_id = allocate_project_id().expect("project id");
    let reservation =
        build_reservation(project_id.clone(), &facts, UnixMillis::new(1)).expect("reservation");
    let completed =
        complete_reservation(&reservation, &project_id, UnixMillis::new(2)).expect("complete");

    match recover_reservation(&completed, &facts).expect("recover") {
        ReservationRecovery::AlreadyInitialized {
            project_id: existing,
        } => assert_eq!(existing, project_id),
        other => panic!("expected already initialized, got {other:?}"),
    }
}

// ---------------------------------------------------------------------------
// opaque identifiers and safe path derivation (S2-E003)
// ---------------------------------------------------------------------------

#[test]
fn allocated_identifiers_are_prefixed_and_unique() {
    let first = allocate_project_id().expect("first");
    let second = allocate_project_id().expect("second");
    assert!(first.as_str().starts_with("p_"));
    assert_ne!(first, second);
    assert!(
        allocate_worktree_id()
            .expect("w")
            .as_str()
            .starts_with("w_")
    );
    assert!(
        allocate_generation_id()
            .expect("g")
            .as_str()
            .starts_with("g_")
    );
    assert!(allocate_record_id().expect("r").as_str().starts_with("r_"));
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
fn published_generation_round_trips() {
    let root = temp_root("publish");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");

    let generation = write_generation(&store, &project);
    let published = store
        .read_published_generation(&project)
        .expect("read published");

    assert_eq!(published.current.generation_id, generation);
    assert_eq!(published.manifest.generation_id, generation);
    assert_eq!(published.manifest.project_id, project);
    assert_eq!(
        published.manifest.authenticity,
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    );
    cleanup(&root);
}

#[test]
fn missing_current_is_a_typed_defect_not_an_invented_generation() {
    let root = temp_root("nocurrent");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");

    match store.read_published_generation(&project) {
        Err(StoreError::Defect(StoreDefect::CurrentMissing)) => {}
        other => panic!("expected CurrentMissing, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn publishing_a_second_generation_replaces_the_pointer_atomically() {
    let root = temp_root("republish");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");

    let first = write_generation(&store, &project);
    let second = write_generation(&store, &project);
    assert_ne!(first, second);

    let published = store
        .read_published_generation(&project)
        .expect("read published");
    assert_eq!(published.current.generation_id, second);

    // The superseded generation remains on disk as an orphan and is never
    // promoted or deleted.
    let orphans = store.orphan_generations(&project).expect("orphans");
    assert!(orphans.contains(&first));
    assert!(!orphans.contains(&second));
    cleanup(&root);
}

// ---------------------------------------------------------------------------
// S2-E014 failure injection at every commit boundary
// ---------------------------------------------------------------------------

#[test]
fn interrupted_generation_never_becomes_current() {
    // Records written but manifest never written: publication must refuse.
    let root = temp_root("nomanifest");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    let generation = allocate_generation_id().expect("generation");
    let record = allocate_record_id().expect("record");

    store
        .write_generation_record(&project, &generation, &record, b"{}")
        .expect("write record");

    match store.publish_generation(&project, &generation) {
        Err(StoreError::Defect(StoreDefect::CurrentDanglingGeneration)) => {}
        other => panic!("expected dangling generation refusal, got {other:?}"),
    }
    assert!(store.read_published_generation(&project).is_err());
    cleanup(&root);
}

#[test]
fn manifest_referencing_a_missing_record_is_refused_at_publish() {
    let root = temp_root("missingrecord");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    let generation = allocate_generation_id().expect("generation");
    let identity_record = allocate_record_id().expect("identity record");
    let index_record = allocate_record_id().expect("index record");

    let identity_digest = store
        .write_generation_record(&project, &generation, &identity_record, b"{}")
        .expect("write identity record");
    // The index record is referenced but never written.
    let manifest = build_manifest(
        project.clone(),
        generation.clone(),
        identity_record,
        index_record.clone(),
        EvidenceRecordRefs::try_from(Vec::new()).expect("refs"),
        vec![
            identity_digest,
            RecordDigest {
                record_id: index_record,
                digest: content_digest(b"{}").expect("digest"),
            },
        ],
        UnixMillis::new(1),
    )
    .expect("manifest");
    store
        .write_generation_manifest(&manifest)
        .expect("write manifest");

    match store.publish_generation(&project, &generation) {
        Err(StoreError::Defect(StoreDefect::RecordMissing)) => {}
        other => panic!("expected RecordMissing, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn torn_record_is_detected_by_digest_mismatch() {
    let root = temp_root("tornrecord");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    let generation = write_generation(&store, &project);

    // Simulate a torn write by truncating one published record in place.
    let records_dir = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("records");
    let victim = fs::read_dir(&records_dir)
        .expect("read records")
        .next()
        .expect("at least one record")
        .expect("record entry")
        .path();
    let mut file = fs::OpenOptions::new()
        .write(true)
        .truncate(true)
        .open(&victim)
        .expect("open victim");
    file.write_all(b"{").expect("write truncated");
    drop(file);

    match store.read_published_generation(&project) {
        Err(StoreError::Defect(StoreDefect::RecordDigestMismatch)) => {}
        other => panic!("expected RecordDigestMismatch, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn corrupt_current_pointer_is_detected() {
    let root = temp_root("corruptcurrent");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    write_generation(&store, &project);

    let current = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current, b"not json at all").expect("corrupt current");

    match store.read_published_generation(&project) {
        Err(StoreError::Defect(StoreDefect::CurrentCorrupt)) => {}
        other => panic!("expected CurrentCorrupt, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn current_pointing_at_a_missing_generation_is_detected() {
    let root = temp_root("danglingcurrent");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    write_generation(&store, &project);

    let absent = allocate_generation_id().expect("absent generation");
    let forged = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project.clone(),
        generation_id: absent,
        manifest_digest: content_digest(b"{}").expect("digest"),
    };
    let bytes = canonical_project_json(&forged).expect("encode");
    let current = root.join("projects").join(project.as_str()).join("CURRENT");
    fs::write(&current, &bytes).expect("write forged current");

    match store.read_published_generation(&project) {
        Err(StoreError::Defect(StoreDefect::CurrentDanglingGeneration)) => {}
        other => panic!("expected CurrentDanglingGeneration, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn manifest_digest_mismatch_is_detected() {
    let root = temp_root("manifestdigest");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    let generation = write_generation(&store, &project);

    let manifest_path = root
        .join("projects")
        .join(project.as_str())
        .join("generations")
        .join(generation.as_str())
        .join("manifest.json");
    let mut bytes = fs::read(&manifest_path).expect("read manifest");
    bytes.push(b' ');
    fs::write(&manifest_path, &bytes).expect("rewrite manifest");

    match store.read_published_generation(&project) {
        Err(StoreError::Defect(StoreDefect::ManifestDigestMismatch)) => {}
        other => panic!("expected ManifestDigestMismatch, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn oversized_record_is_refused_before_it_is_written() {
    let root = temp_root("oversize");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    let generation = allocate_generation_id().expect("generation");
    let record = allocate_record_id().expect("record");

    let oversized = vec![b'x'; wepld_core::MAX_RECORD_BYTES + 1];
    match store.write_generation_record(&project, &generation, &record, &oversized) {
        Err(StoreError::TooLarge { .. }) => {}
        other => panic!("expected TooLarge, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn reservation_survives_temp_write_and_replace() {
    let root = temp_root("reservationio");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let facts = facts_at("/projects/persisted");
    let project = allocate_project_id().expect("project");
    let reservation =
        build_reservation(project.clone(), &facts, UnixMillis::new(3)).expect("reservation");

    store.write_reservation(&reservation).expect("write");
    let read_back = store
        .read_reservation(&project)
        .expect("read")
        .expect("present");
    assert_eq!(read_back, reservation);

    let completed =
        complete_reservation(&reservation, &project, UnixMillis::new(4)).expect("complete");
    store.write_reservation(&completed).expect("rewrite");
    let listed = store.list_reservations().expect("list");
    assert_eq!(listed.len(), 1);
    match listed.first() {
        Some(Ok(entry)) => assert_eq!(entry.state, IdentityReservationState::Initialized),
        other => panic!("expected one initialized reservation, got {other:?}"),
    }
    cleanup(&root);
}

#[test]
fn corrupt_reservation_is_reported_rather_than_skipped() {
    // Silently skipping a corrupt reservation would let a second identity be
    // allocated for an already-reserved project.
    let root = temp_root("corruptreservation");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let facts = facts_at("/projects/corrupt");
    let project = allocate_project_id().expect("project");
    let reservation =
        build_reservation(project.clone(), &facts, UnixMillis::new(1)).expect("reservation");
    store.write_reservation(&reservation).expect("write");

    let path = root
        .join("catalog")
        .join("reservations")
        .join(format!("{}.json", project.as_str()));
    fs::write(&path, b"{ broken").expect("corrupt");

    let listed = store.list_reservations().expect("list");
    assert_eq!(listed.len(), 1);
    assert!(matches!(
        listed.first(),
        Some(Err(StoreDefect::RecordCorrupt))
    ));
    cleanup(&root);
}

// ---------------------------------------------------------------------------
// S2-E005 / S2-E015 bounded locking and crash release
// ---------------------------------------------------------------------------

#[test]
fn contended_lock_returns_a_stable_busy_result_within_the_deadline() {
    let root = temp_root("lockbusy");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");

    let held = store
        .acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled())
        .expect("first acquisition");

    let started = Instant::now();
    let result = store.acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled());
    let elapsed = started.elapsed();

    match result {
        Err(StoreError::Busy { scope }) => {
            assert_eq!(scope, StoreLockScope::IdentityCatalog);
            assert_eq!(busy_error_code(scope), "identity_catalog_busy");
        }
        other => panic!("expected busy, got {other:?}"),
    }
    // Bounded completion: never an unbounded wait.
    assert!(elapsed.as_millis() >= u128::from(wepld_core::LOCK_ACQUIRE_DEADLINE_MS));
    assert!(elapsed.as_millis() < u128::from(wepld_core::LOCK_ACQUIRE_DEADLINE_MS) * 4);

    drop(held);
    cleanup(&root);
}

#[test]
fn cancellation_stops_lock_acquisition_promptly() {
    let root = temp_root("lockcancel");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let held = store
        .acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled())
        .expect("first acquisition");

    let polls = AtomicUsize::new(0);
    let cancel = || polls.fetch_add(1, AtomicOrdering::SeqCst) >= 2;
    let started = Instant::now();
    let result = store.acquire_lock(StoreLockScope::IdentityCatalog, None, &cancel);
    let elapsed = started.elapsed();

    assert!(matches!(result, Err(StoreError::Cancelled { .. })));
    assert!(elapsed.as_millis() < u128::from(wepld_core::LOCK_ACQUIRE_DEADLINE_MS));
    drop(held);
    cleanup(&root);
}

#[test]
fn releasing_a_lock_allows_immediate_reacquisition() {
    // Lock-file existence is never ownership. Once the owning handle is closed
    // the lock is available again, which is the same path a crashed process
    // takes when the operating system closes its handles.
    let root = temp_root("lockrelease");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");

    let held = store
        .acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled())
        .expect("acquire");
    drop(held);

    let lock_path = root.join("catalog").join("catalog.lock");
    assert!(lock_path.exists(), "lock file intentionally persists");

    let started = Instant::now();
    let reacquired = store
        .acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled())
        .expect("reacquire after release");
    assert!(started.elapsed().as_millis() < u128::from(wepld_core::LOCK_ACQUIRE_DEADLINE_MS));
    drop(reacquired);
    cleanup(&root);
}

#[test]
fn catalog_and_project_locks_are_independent_scopes() {
    let root = temp_root("lockscopes");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");

    let catalog = store
        .acquire_lock(StoreLockScope::IdentityCatalog, None, &never_cancelled())
        .expect("catalog lock");
    // Canonical order: catalog first, then project.
    let project_lock = store
        .acquire_lock(
            StoreLockScope::ProjectStore,
            Some(&project),
            &never_cancelled(),
        )
        .expect("project lock");
    assert_eq!(project_lock.scope(), StoreLockScope::ProjectStore);
    assert_eq!(busy_error_code(StoreLockScope::ProjectStore), "store_busy");
    drop(project_lock);
    drop(catalog);
    cleanup(&root);
}

// ---------------------------------------------------------------------------
// S2-I014 concurrent first open / S2-E013 concurrent writers
// ---------------------------------------------------------------------------

#[test]
fn concurrent_first_open_yields_one_identity_or_a_stable_busy() {
    // S2-I014. Never two identities for the same facts.
    let root = temp_root("firstopen");
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize().expect("initialize");
    let facts = Arc::new(facts_at("/projects/race"));

    let mut handles = Vec::new();
    for _ in 0..8 {
        let store = Arc::clone(&store);
        let facts = Arc::clone(&facts);
        handles.push(thread::spawn(move || -> Option<ProjectId> {
            let guard = match store.acquire_lock(StoreLockScope::IdentityCatalog, None, &|| false) {
                Ok(guard) => guard,
                Err(StoreError::Busy { .. }) => return None,
                Err(error) => panic!("unexpected lock error: {error:?}"),
            };

            // Under the catalog lock: reuse an existing reservation for these
            // exact facts, otherwise commit exactly one new reservation.
            let existing = store.list_reservations().expect("list reservations");
            for entry in existing {
                let reservation = entry.expect("reservation decodes");
                if let ReservationRecovery::ResumeSameProject { project_id }
                | ReservationRecovery::AlreadyInitialized { project_id } =
                    recover_reservation(&reservation, &facts).expect("recover")
                {
                    drop(guard);
                    return Some(project_id);
                }
            }
            let project_id = allocate_project_id().expect("allocate");
            let reservation = build_reservation(project_id.clone(), &facts, UnixMillis::new(1))
                .expect("reservation");
            store.write_reservation(&reservation).expect("write");
            drop(guard);
            Some(project_id)
        }));
    }

    let mut allocated: Vec<ProjectId> = Vec::new();
    for handle in handles {
        if let Some(project_id) = handle.join().expect("thread joins") {
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

    let reservations = store.list_reservations().expect("list");
    assert_eq!(reservations.len(), 1, "exactly one reservation persists");
    cleanup(&root);
}

#[test]
fn concurrent_ordinary_writers_never_publish_a_mixed_generation() {
    // S2-E013. Each writer publishes a complete generation under the project
    // lock. Readers always observe one coherent generation.
    let root = temp_root("concurrentwriters");
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize().expect("initialize");
    let project = Arc::new(allocate_project_id().expect("project"));

    let mut handles = Vec::new();
    for _ in 0..4 {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        handles.push(thread::spawn(move || {
            for _ in 0..3 {
                match store.acquire_lock(StoreLockScope::ProjectStore, Some(&project), &|| false) {
                    Ok(guard) => {
                        write_generation(&store, &project);
                        drop(guard);
                    }
                    Err(StoreError::Busy { .. }) => {}
                    Err(error) => panic!("unexpected lock error: {error:?}"),
                }
            }
        }));
    }
    for handle in handles {
        handle.join().expect("thread joins");
    }

    // Whatever interleaving occurred, the published generation validates fully.
    let published = store
        .read_published_generation(&project)
        .expect("published generation is coherent");
    assert_eq!(published.manifest.project_id, *project);
    cleanup(&root);
}

#[test]
fn readers_observe_a_coherent_generation_while_a_writer_publishes() {
    let root = temp_root("readerwriter");
    let store = Arc::new(EvidenceStore::new(&root));
    store.initialize().expect("initialize");
    let project = Arc::new(allocate_project_id().expect("project"));
    write_generation(&store, &project);

    let writer = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || {
            for _ in 0..10 {
                write_generation(&store, &project);
            }
        })
    };

    let reader = {
        let store = Arc::clone(&store);
        let project = Arc::clone(&project);
        thread::spawn(move || {
            for _ in 0..25 {
                // Every successful read must be internally coherent.
                if let Ok(published) = store.read_published_generation(&project) {
                    assert_eq!(
                        published.manifest.generation_id,
                        published.current.generation_id
                    );
                }
            }
        })
    };

    writer.join().expect("writer joins");
    reader.join().expect("reader joins");
    cleanup(&root);
}

// ---------------------------------------------------------------------------
// S2-E011 freshness, S2-E012 redaction, S2-E016 durability, S2-E017 authenticity
// ---------------------------------------------------------------------------

#[test]
fn freshness_uses_generation_commit_time_not_filesystem_metadata() {
    let root = temp_root("freshness");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    write_generation(&store, &project);
    let published = store
        .read_published_generation(&project)
        .expect("published");

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
    cleanup(&root);
}

#[test]
fn redacted_summary_never_reveals_the_value() {
    let secret = b"https://user:tokenvalue@example.invalid/repo.git";
    let summary = redacted_summary(secret).expect("summary");
    assert!(summary.starts_with("redacted:"));
    assert!(!summary.contains("tokenvalue"));
    assert!(!summary.contains("example.invalid"));
    // Identical values correlate; different values do not collide in practice.
    assert_eq!(summary, redacted_summary(secret).expect("summary again"));
    assert_ne!(summary, redacted_summary(b"different").expect("other"));
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
fn a_forged_but_self_consistent_generation_is_not_reported_as_authenticated() {
    // S2-S015 in miniature: an actor with writer access can rebuild a complete
    // generation that validates. Validation success is coherence evidence only.
    let root = temp_root("forged");
    let store = EvidenceStore::new(&root);
    store.initialize().expect("initialize");
    let project = allocate_project_id().expect("project");
    write_generation(&store, &project);

    // The forger simply writes another complete generation and publishes it.
    let forged = write_generation(&store, &project);
    let published = store
        .read_published_generation(&project)
        .expect("forged generation validates structurally");
    assert_eq!(published.current.generation_id, forged);
    assert_eq!(
        published.manifest.authenticity,
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
        "structural validity must not be presented as authenticity"
    );
    cleanup(&root);
}

#[test]
fn published_records_are_durable_and_byte_exact_after_reopen() {
    // S2-E016. Durability evidence is limited to what this platform genuinely
    // guarantees: contents are synced before the rename that publishes them, so
    // a reopened store observes exactly the written bytes. No claim is made
    // about directory-entry or power-loss semantics.
    let root = temp_root("durability");
    let project = allocate_project_id().expect("project");
    {
        let store = EvidenceStore::new(&root);
        store.initialize().expect("initialize");
        write_generation(&store, &project);
    }

    let reopened = EvidenceStore::new(&root);
    let published = reopened
        .read_published_generation(&project)
        .expect("published survives reopen");
    let identity_bytes = reopened
        .read_generation_record(&published.manifest, &published.manifest.identity_record_ref)
        .expect("identity record survives reopen");
    assert_eq!(identity_bytes, b"{\"kind\":\"identity\"}");
    cleanup(&root);
}

#[test]
fn identity_record_binds_the_revalidated_facts_digest() {
    let facts = facts_at("/projects/record");
    let project = allocate_project_id().expect("project");
    let worktree = allocate_worktree_id().expect("worktree");
    let record = build_identity_record(
        project.clone(),
        worktree.clone(),
        &facts,
        IdentityRecordState::Active,
    )
    .expect("identity record");

    assert_eq!(record.project_id, project);
    assert_eq!(record.worktree_id, worktree);
    assert_eq!(record.state, IdentityRecordState::Active);
    assert_eq!(
        record.revalidated_match_facts_digest,
        facts.facts_digest().expect("digest")
    );
}
