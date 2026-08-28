#![forbid(unsafe_code)]

pub mod project;
pub mod state;

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
