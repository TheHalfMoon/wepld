#![forbid(unsafe_code)]

pub mod evidence_store;
pub mod git_topology;
pub mod identity;
pub mod project;
pub mod state;

pub use evidence_store::{
    EvidenceStore, Freshness, LOCK_ACQUIRE_DEADLINE_MS, LOCK_POLL_INTERVAL_MS, MAX_CURRENT_BYTES,
    MAX_MANIFEST_BYTES, MAX_RECORD_BYTES, PRODUCER_CONTRACT_VERSION, PublishedGeneration,
    StoreDefect, StoreError, StoreLock, build_manifest, busy_error_code, content_digest,
    now_unix_millis, redacted_summary, safe_path_segment,
};
pub use identity::{
    IdentityCandidate, IdentityError, OPAQUE_ID_RANDOM_BYTES, ProjectMatchFacts,
    RESERVATION_KEY_VERSION, ReservationRecovery, allocate_generation_id, allocate_project_id,
    allocate_record_id, allocate_worktree_id, build_identity_record, build_reservation, busy,
    compare_match_strength, complete_reservation, match_strength_rank, recover_reservation,
    resolve_identity,
};
pub use project::{
    DataRootInputs, DataRootObservation, DataRootSource, MAX_PATH_COMPONENT_OBSERVATIONS,
    NonGitProjectRoot, PathEntryKind, PathMetadataObservation, PathMetadataTrail,
    ProjectObservationError, ProjectRootBasis, classify_path_io_error, lexical_absolute_path,
    machine_path_from_path, observe_non_git_project_root, observe_path_metadata,
    observe_project_locator, platform_data_root,
};
pub use state::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS, MAX_TERMINAL_RESULTS,
    PendingRequest, StateError,
};
