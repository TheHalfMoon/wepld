#![forbid(unsafe_code)]

//! `wepld` — the S2-AUTH-015 command front-end for `open | doctor | status`.
//!
//! This binary is the only effectful part of the Doctor/CLI tranche. It collects
//! already-authorized S2 observations — the project locator, read-only Git
//! topology (S2-AUTH-014), the local identity/reservation catalog, and the local
//! evidence store — assembles them into one redacted [`cli::CommandOutcome`],
//! projects it through the requested mode, and exits with a frozen class.
//!
//! It never starts a project task, installer, build, test, package manager, or
//! remediation; it never mutates a repository or `safe.directory`; it makes no
//! network request. The pure decision layers live in [`wepld_core::doctor`] and
//! [`wepld_core::cli`]; this file only feeds and prints them.

use std::env;
use std::ffi::OsString;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use wepld_contracts::{
    EvidenceRecordRefs, EvidenceStatus, IdentityRecordState, IdentityResolution, MachinePath,
    Observation, ProjectId, ProjectLocator, RepositoryTopology, RepositoryTrustState,
    canonical_project_json,
};
use wepld_core::cli::{
    self, Command, CommandOutcome, EvidenceSummary, ExitClass, Invocation, OutputMode,
    RepositorySummary,
};
use wepld_core::doctor::{
    self, DescriptorObservation, DoctorInputs, EvidenceStoreObservation, IdentityObservation,
    RepositoryObservation, SecuritySensitiveObservation,
};
use wepld_core::evidence_store::{self, EvidenceStore, StoreError};
use wepld_core::git_topology::{self, GitTopologyError, QualifiedGitExecutable};
use wepld_core::identity::{self, ProjectMatchFacts, ReservationRecovery};
use wepld_core::project::{self, DataRootInputs};

/// Freshness horizon for a published generation. A generation older than this is
/// reported `stale`; it is a deterministic Doctor input, not a wall-clock SLA.
const EVIDENCE_MAX_AGE_MILLIS: u64 = 7 * 24 * 60 * 60 * 1000;

/// Leaf directory under the qualified platform data root that holds the S2
/// evidence/identity store. Kept separate so a future store revision can sit
/// beside it without colliding.
const STORE_LEAF: &str = "s2-store";

fn main() -> ExitCode {
    let args: Vec<OsString> = env::args_os().skip(1).collect();
    let string_args: Vec<String> = args
        .iter()
        .map(|a| a.to_string_lossy().into_owned())
        .collect();

    let invocation = match cli::parse(&string_args) {
        Ok(invocation) => invocation,
        Err(error) => {
            let command = failed_command(string_args.first().map(String::as_str));
            let outcome = CommandOutcome::Failure {
                command,
                class: ExitClass::UsageInput,
                reason: format!("usage: {error}"),
            };
            return emit(&outcome, OutputMode::Human);
        }
    };

    let outcome = run(&invocation);
    emit(&outcome, invocation.output)
}

fn failed_command(first: Option<&str>) -> Command {
    match first {
        Some("doctor") => Command::Doctor,
        Some("status") => Command::Status,
        _ => Command::Open,
    }
}

fn run(invocation: &Invocation) -> CommandOutcome {
    match invocation.command {
        Command::Open => run_open(invocation.open_path.as_deref().unwrap_or_default()),
        Command::Doctor => run_doctor(),
        Command::Status => run_status(),
    }
}

// --------------------------------------------------------------------------
// Shared observation collection
// --------------------------------------------------------------------------

/// Everything the three commands share: a resolved locator plus the store handle.
struct Context {
    locator: ProjectLocator,
    /// Absolute lexical project path, used as the Git `-C` target and the
    /// executable-boundary for Git discovery.
    project_path: PathBuf,
    store: EvidenceStore,
    /// Absolute store root, used as the Git executable evidence-root boundary.
    store_root: PathBuf,
}

#[derive(Debug)]
enum ContextError {
    /// The locator path could not be observed at all (empty, too deep, platform).
    Locator(String),
    /// The qualified platform data root is unavailable (no HOME / LOCALAPPDATA).
    StoreRootUnavailable(String),
    /// `EvidenceStore::new` refused the derived root.
    Store(String),
}

fn build_context(input: &str) -> Result<Context, ContextError> {
    let now = evidence_store::now_unix_millis();
    let cwd = env::current_dir().map_err(|error| {
        ContextError::Locator(format!("current_directory_unavailable: {error}"))
    })?;
    let input_path = Path::new(input);
    let locator = project::observe_project_locator(input_path, &cwd, now)
        .map_err(|error| ContextError::Locator(format!("locator_observation_failed: {error}")))?;

    let project_path = project::lexical_absolute_path(input_path, &cwd)
        .map_err(|error| ContextError::Locator(format!("locator_observation_failed: {error}")))?;

    let store_root = qualified_store_root().map_err(|error| {
        ContextError::StoreRootUnavailable(format!("data_root_unavailable: {error}"))
    })?;
    let store = EvidenceStore::new(store_root.clone()).map_err(|error| {
        ContextError::Store(format!("store_open_failed: {}", store_error_reason(&error)))
    })?;

    Ok(Context {
        locator,
        project_path,
        store,
        store_root,
    })
}

/// Derive the S2 store root from the qualified per-user platform data location.
fn qualified_store_root() -> Result<PathBuf, project::ProjectObservationError> {
    let xdg_state_home = env::var_os("XDG_STATE_HOME").map(PathBuf::from);
    let home = env::var_os("HOME").map(PathBuf::from);
    let macos_support = home
        .as_deref()
        .map(|home| home.join("Library").join("Application Support"));
    let windows_local_app_data = env::var_os("LOCALAPPDATA").map(PathBuf::from);

    let inputs = DataRootInputs {
        xdg_state_home: xdg_state_home.as_deref(),
        home: home.as_deref(),
        macos_application_support: macos_support.as_deref(),
        windows_local_app_data: windows_local_app_data.as_deref(),
    };
    let observation = project::platform_data_root(inputs)?;
    let base = machine_path_to_pathbuf(&observation.path)
        .ok_or(project::ProjectObservationError::UnsupportedPlatform)?;
    Ok(base.join(STORE_LEAF))
}

fn machine_path_to_pathbuf(path: &MachinePath) -> Option<PathBuf> {
    match path {
        MachinePath::Utf8(value) => Some(PathBuf::from(value)),
        #[cfg(unix)]
        MachinePath::UnixBytes(value) => {
            use std::os::unix::ffi::OsStrExt as _;
            Some(PathBuf::from(std::ffi::OsStr::from_bytes(value)))
        }
        #[cfg(not(unix))]
        MachinePath::UnixBytes(_) => None,
        #[cfg(windows)]
        MachinePath::WindowsWtf16(value) => {
            use std::os::windows::ffi::OsStringExt as _;
            Some(PathBuf::from(OsString::from_wide(value)))
        }
        #[cfg(not(windows))]
        MachinePath::WindowsWtf16(_) => None,
    }
}

/// Best-effort read-only Git topology. A non-Git directory, a Git trust refusal,
/// or an unavailable Git capability are all normal outcomes, distinguished for
/// the caller rather than collapsed.
enum RepositoryOutcome {
    /// Git topology was qualified.
    Git(RepositoryTopology),
    /// The path is a valid local project without Git.
    NonGit,
    /// Git is present but refused this working tree (ownership/trust boundary).
    RefusedByGit,
    /// The Git capability itself is unavailable (no executable, no PATH, timeout).
    CapabilityUnavailable,
}

fn observe_repository(project_path: &Path, store_root: &Path) -> RepositoryOutcome {
    if !project_path.is_absolute() {
        return RepositoryOutcome::CapabilityUnavailable;
    }
    // The Git executable-boundary check canonicalizes both boundary paths; the
    // store root may not exist yet on a first `doctor`, so fall back to its
    // nearest existing ancestor for the boundary only.
    let boundary_root =
        nearest_existing_ancestor(store_root).unwrap_or_else(|| store_root.to_path_buf());
    let git = match git_topology::discover_system_git(project_path, &boundary_root) {
        Ok(git) => git,
        Err(GitTopologyError::UntrustedRepositoryRefusedByGit) => {
            return RepositoryOutcome::RefusedByGit;
        }
        Err(_) => return RepositoryOutcome::CapabilityUnavailable,
    };
    classify_topology(&git, project_path)
}

fn classify_topology(git: &QualifiedGitExecutable, project_path: &Path) -> RepositoryOutcome {
    match git_topology::observe_git_topology(git, project_path) {
        Ok(topology) => match topology.trust_state {
            RepositoryTrustState::RefusedByGit => RepositoryOutcome::RefusedByGit,
            _ => RepositoryOutcome::Git(topology),
        },
        Err(GitTopologyError::NotGitRepository) => RepositoryOutcome::NonGit,
        Err(GitTopologyError::UntrustedRepositoryRefusedByGit) => RepositoryOutcome::RefusedByGit,
        Err(_) => RepositoryOutcome::CapabilityUnavailable,
    }
}

fn nearest_existing_ancestor(path: &Path) -> Option<PathBuf> {
    let mut candidate = path;
    loop {
        if candidate.try_exists().unwrap_or(false) {
            return Some(candidate.to_path_buf());
        }
        candidate = candidate.parent()?;
    }
}

/// Project the topology into the redacted [`RepositoryObservation`] Doctor consumes.
fn repository_observation(outcome: &RepositoryOutcome) -> Option<RepositoryObservation> {
    match outcome {
        RepositoryOutcome::NonGit => None,
        RepositoryOutcome::RefusedByGit => Some(RepositoryObservation {
            trust_state: RepositoryTrustState::RefusedByGit,
            nested_candidate_ambiguity: false,
            linked_worktree_state_unknown: false,
        }),
        RepositoryOutcome::CapabilityUnavailable => Some(RepositoryObservation {
            trust_state: RepositoryTrustState::Unknown,
            nested_candidate_ambiguity: false,
            linked_worktree_state_unknown: false,
        }),
        RepositoryOutcome::Git(topology) => Some(RepositoryObservation {
            trust_state: topology.trust_state,
            nested_candidate_ambiguity: matches!(
                &topology.superproject_worktree,
                wepld_contracts::OptionalObservation::Value { .. }
            ),
            linked_worktree_state_unknown: matches!(
                topology.linked_worktree_state,
                wepld_contracts::LinkedWorktreeState::Unknown
            ),
        }),
    }
}

fn repository_summary(outcome: &RepositoryOutcome) -> RepositorySummary {
    match outcome {
        RepositoryOutcome::NonGit => RepositorySummary::NonGit,
        RepositoryOutcome::RefusedByGit => RepositorySummary::Git {
            trust_state: RepositoryTrustState::RefusedByGit,
        },
        RepositoryOutcome::CapabilityUnavailable => RepositorySummary::Git {
            trust_state: RepositoryTrustState::Unknown,
        },
        RepositoryOutcome::Git(topology) => RepositorySummary::Git {
            trust_state: topology.trust_state,
        },
    }
}

// --------------------------------------------------------------------------
// Root-descriptor allowlist scan (S2-D004..D008, FR-020)
// --------------------------------------------------------------------------

/// Exact root-level descriptor names that baseline S2 recognizes, with the
/// toolchain and package-manager class each implies. Detection is by name and
/// bounded read only; the file structure is not parsed in baseline S2.
const PARSED_DESCRIPTORS: &[(
    &str,
    wepld_contracts::ToolchainKind,
    Option<wepld_contracts::PackageManagerKind>,
)] = {
    use wepld_contracts::PackageManagerKind as P;
    use wepld_contracts::ToolchainKind as T;
    &[
        ("Cargo.toml", T::Rust, Some(P::Cargo)),
        ("package.json", T::Node, Some(P::Npm)),
        ("pnpm-workspace.yaml", T::Node, Some(P::Pnpm)),
        ("pyproject.toml", T::Python, None),
        ("mise.toml", T::Mise, None),
        (".mise.toml", T::Mise, None),
        ("justfile", T::Just, None),
        ("Justfile", T::Just, None),
        ("Makefile", T::Make, None),
        ("settings.gradle", T::Gradle, None),
        ("settings.gradle.kts", T::Gradle, None),
        ("build.gradle", T::Gradle, None),
        ("build.gradle.kts", T::Gradle, None),
        ("pom.xml", T::Maven, Some(P::Yarn)),
        ("go.mod", T::Go, Some(P::Go)),
        ("go.work", T::Go, Some(P::Go)),
        ("nx.json", T::Nx, None),
        ("workspace.json", T::Nx, None),
    ]
};

/// Presence-only lock/package-manager markers. Never read or parsed in baseline
/// S2 (S2-D007); their presence and count is the only signal.
const PRESENCE_MARKERS: &[(&str, Option<wepld_contracts::PackageManagerKind>)] = {
    use wepld_contracts::PackageManagerKind as P;
    &[
        ("Cargo.lock", Some(P::Cargo)),
        ("package-lock.json", Some(P::Npm)),
        ("npm-shrinkwrap.json", Some(P::Npm)),
        ("pnpm-lock.yaml", Some(P::Pnpm)),
        ("yarn.lock", Some(P::Yarn)),
        ("bun.lock", Some(P::Bun)),
        ("bun.lockb", Some(P::Bun)),
        ("uv.lock", Some(P::Uv)),
        ("poetry.lock", Some(P::Poetry)),
        ("go.sum", Some(P::Go)),
    ]
};

fn scan_root_descriptors(project_path: &Path) -> DescriptorObservation {
    let mut toolchains: Vec<wepld_contracts::ToolchainKind> = Vec::new();
    let mut package_managers: Vec<wepld_contracts::PackageManagerKind> = Vec::new();
    let mut lockfile_marker_count: u64 = 0;
    let mut budget_rejected = false;

    let mut candidate_count: usize = 0;
    let mut aggregate_bytes: u64 = 0;
    let mut max_single_bytes: u64 = 0;

    for (name, toolchain, package_manager) in PARSED_DESCRIPTORS {
        let path = project_path.join(name);
        let metadata = match fs::symlink_metadata(&path) {
            Ok(metadata) => metadata,
            Err(_) => continue,
        };
        if !metadata.is_file() {
            continue;
        }
        candidate_count += 1;
        let len = metadata.len();
        max_single_bytes = max_single_bytes.max(len);

        if len > doctor::MAX_PARSED_DESCRIPTOR_BYTES {
            budget_rejected = true;
            continue;
        }
        aggregate_bytes = aggregate_bytes.saturating_add(len);
        if aggregate_bytes > doctor::MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES {
            budget_rejected = true;
            continue;
        }
        // Bounded read to exercise the per-file limit and to hold real
        // content-addressed evidence; the bytes are not parsed as structure in
        // baseline S2 (FR-022), so nesting depth stays zero.
        if fs::read(&path)
            .map(|bytes| bytes.len() as u64 > doctor::MAX_PARSED_DESCRIPTOR_BYTES)
            .unwrap_or(true)
        {
            budget_rejected = true;
            continue;
        }
        push_unique(&mut toolchains, *toolchain);
        if let Some(kind) = package_manager {
            push_unique(&mut package_managers, *kind);
        }
    }

    if candidate_count > doctor::MAX_ROOT_DESCRIPTOR_CANDIDATES {
        budget_rejected = true;
    }

    let mut distinct_marker_kinds: Vec<wepld_contracts::PackageManagerKind> = Vec::new();
    for (name, kind) in PRESENCE_MARKERS {
        let path = project_path.join(name);
        if fs::symlink_metadata(&path)
            .map(|m| m.is_file())
            .unwrap_or(false)
        {
            lockfile_marker_count += 1;
            if let Some(kind) = kind {
                push_unique(&mut distinct_marker_kinds, *kind);
            }
        }
    }

    // Ambiguity: more than one distinct package-manager family evidenced, from
    // parsed descriptors or presence-only lock markers combined.
    let mut all_manager_kinds = package_managers.clone();
    for kind in &distinct_marker_kinds {
        push_unique(&mut all_manager_kinds, *kind);
    }
    let package_manager_ambiguous = all_manager_kinds.len() > 1;

    if doctor::check_descriptor_budget(candidate_count, max_single_bytes, aggregate_bytes, 0)
        .is_err()
    {
        budget_rejected = true;
    }

    DescriptorObservation {
        toolchains,
        package_managers,
        lockfile_marker_count,
        package_manager_ambiguous,
        descriptor_budget_rejected: budget_rejected,
    }
}

fn push_unique<T: PartialEq>(list: &mut Vec<T>, value: T) {
    if !list.contains(&value) {
        list.push(value);
    }
}

// --------------------------------------------------------------------------
// Identity resolution (read-only and reserve-and-initialize)
// --------------------------------------------------------------------------

/// Never-blocking cancellation for store locks: S2 commands are bounded
/// request/response, so there is no interactive interrupt to observe.
fn never_cancelled() -> bool {
    false
}

/// Build the identity candidate list from the catalog's reservations.
fn candidates_from_catalog(
    store: &EvidenceStore,
) -> Result<Vec<identity::IdentityCandidate>, StoreError> {
    let mut candidates = Vec::new();
    for entry in store.list_reservations()? {
        let Ok(reservation) = entry else {
            // A defective catalog entry must not silently shrink the candidate
            // set; surface it as a store integrity error.
            return Err(StoreError::Defect(
                evidence_store::StoreDefect::RecordCorrupt,
            ));
        };
        candidates.push(identity::IdentityCandidate {
            project_id: reservation.project_id,
            facts_digest: reservation.revalidated_match_facts_digest,
            anchor_digest: None,
            state: IdentityRecordState::Active,
        });
    }
    Ok(candidates)
}

enum IdentityDecision {
    /// A confident existing binding (normal reopen).
    Bound(ProjectId),
    /// A crashed first-open reservation is being resumed with the same id.
    ReservedRecovered(ProjectId),
    /// This project has never been seen; `project_id` was freshly reserved.
    FirstOpen(ProjectId),
    /// Multiple candidate identities remain; needs explicit reconciliation.
    Ambiguous { candidate_count: u64 },
    /// Contradictory topology evidence for one key.
    Conflict,
    /// A store lock deadline elapsed.
    Busy(wepld_contracts::StoreLockScope),
}

/// Resolve identity read-only. Never allocates or reserves.
fn resolve_identity_readonly(
    store: &EvidenceStore,
    facts: &ProjectMatchFacts,
) -> Result<IdentityDecision, StoreError> {
    let catalog = store.lock_catalog(&never_cancelled)?;
    let _ = &catalog;
    let candidates = candidates_from_catalog(store)?;
    match identity::resolve_identity(facts, &candidates).map_err(StoreError::Identity)? {
        IdentityResolution::Existing { project_id, .. } => {
            match store.read_reservation(&project_id)? {
                Some(reservation) => match identity::recover_reservation(&reservation, facts)
                    .map_err(StoreError::Identity)?
                {
                    ReservationRecovery::ResumeSameProject { project_id } => {
                        Ok(IdentityDecision::ReservedRecovered(project_id))
                    }
                    ReservationRecovery::AlreadyInitialized { project_id } => {
                        Ok(IdentityDecision::Bound(project_id))
                    }
                    ReservationRecovery::Mismatch => Ok(IdentityDecision::Conflict),
                },
                None => Ok(IdentityDecision::Bound(project_id)),
            }
        }
        IdentityResolution::Reserved { reservation } => {
            Ok(IdentityDecision::ReservedRecovered(reservation.project_id))
        }
        IdentityResolution::Ambiguous { candidates } => {
            if candidates.as_slice().is_empty() {
                Ok(IdentityDecision::Ambiguous { candidate_count: 0 })
            } else {
                Ok(IdentityDecision::Ambiguous {
                    candidate_count: candidates.as_slice().len() as u64,
                })
            }
        }
        IdentityResolution::Conflict { candidates, .. } => {
            let _ = candidates;
            Ok(IdentityDecision::Conflict)
        }
        IdentityResolution::Busy { scope } => Ok(IdentityDecision::Busy(scope)),
    }
}

// --------------------------------------------------------------------------
// `wepld open`
// --------------------------------------------------------------------------

fn run_open(input: &str) -> CommandOutcome {
    let context = match build_context(input) {
        Ok(context) => context,
        Err(ContextError::Locator(reason)) => {
            return failure(Command::Open, ExitClass::ProjectResolutionIdentity, reason);
        }
        Err(ContextError::StoreRootUnavailable(reason)) => {
            return failure(
                Command::Open,
                ExitClass::RequiredCapabilityUnavailable,
                reason,
            );
        }
        Err(ContextError::Store(reason)) => {
            return failure(Command::Open, ExitClass::EvidenceStoreIntegrity, reason);
        }
    };

    let locator_display = doctor::safe_display_path(machine_path_of_lexical(&context.locator));
    let repository = observe_repository(&context.project_path, &context.store_root);
    let repository_summary = repository_summary(&repository);

    // Identity requires an available resolved path; a failed canonicalization is
    // transient and must never become identity input.
    if !matches!(context.locator.resolved_path, Observation::Available { .. }) {
        return failure(
            Command::Open,
            ExitClass::ProjectResolutionIdentity,
            "identity_unavailable: resolved path could not be observed".to_owned(),
        );
    }

    if let Err(error) = context.store.initialize() {
        return failure(
            Command::Open,
            ExitClass::EvidenceStoreIntegrity,
            format!("store_initialize_failed: {}", store_error_reason(&error)),
        );
    }

    let facts = ProjectMatchFacts::new(context.locator.clone());

    let decision = match reserve_identity(&context.store, &facts) {
        Ok(decision) => decision,
        Err(error) => return store_failure(Command::Open, &error),
    };

    let (project_id, identity_note) = match decision {
        IdentityDecision::Bound(id) => (id, "bound"),
        IdentityDecision::ReservedRecovered(id) => (id, "reservation_recovered"),
        IdentityDecision::FirstOpen(id) => (id, "first_open"),
        IdentityDecision::Ambiguous { candidate_count } => {
            return failure(
                Command::Open,
                ExitClass::ProjectResolutionIdentity,
                format!("identity_ambiguous: {candidate_count} candidate identities"),
            );
        }
        IdentityDecision::Conflict => {
            return failure(
                Command::Open,
                ExitClass::ProjectResolutionIdentity,
                "identity_conflict: contradictory topology evidence".to_owned(),
            );
        }
        IdentityDecision::Busy(scope) => {
            return failure(
                Command::Open,
                ExitClass::RequiredCapabilityUnavailable,
                format!("store_busy: {}", evidence_store::busy_error_code(scope)),
            );
        }
    };
    let _ = identity_note;

    let evidence =
        match write_and_publish_generation(&context.store, &project_id, &facts, &context.locator) {
            Ok(()) => EvidenceSummary::Present {
                status: EvidenceStatus::Complete,
                authenticity: EvidenceStore::authenticity(),
            },
            Err(error) => return store_failure(Command::Open, &error),
        };

    CommandOutcome::Open {
        project_id: Some(project_id.as_str().to_owned()),
        locator_display,
        repository: repository_summary,
        evidence,
    }
}

/// Resolve identity and, only for a genuine first open, reserve one under the
/// catalog lock. Concurrent first opens converge on one reserved id or a busy
/// result; a second identity is never allocated.
fn reserve_identity(
    store: &EvidenceStore,
    facts: &ProjectMatchFacts,
) -> Result<IdentityDecision, StoreError> {
    let catalog = store.lock_catalog(&never_cancelled)?;
    let candidates = candidates_from_catalog(store)?;
    match identity::resolve_identity(facts, &candidates).map_err(StoreError::Identity)? {
        IdentityResolution::Existing { project_id, .. } => {
            match store.read_reservation(&project_id)? {
                Some(reservation) => {
                    match identity::recover_reservation(&reservation, facts)
                        .map_err(StoreError::Identity)?
                    {
                        ReservationRecovery::ResumeSameProject { project_id } => {
                            Ok(IdentityDecision::ReservedRecovered(project_id))
                        }
                        ReservationRecovery::AlreadyInitialized { project_id } => {
                            Ok(IdentityDecision::Bound(project_id))
                        }
                        ReservationRecovery::Mismatch => Ok(IdentityDecision::Conflict),
                    }
                }
                None => Ok(IdentityDecision::Bound(project_id)),
            }
        }
        IdentityResolution::Reserved { reservation } => {
            Ok(IdentityDecision::ReservedRecovered(reservation.project_id))
        }
        IdentityResolution::Conflict { .. } => Ok(IdentityDecision::Conflict),
        IdentityResolution::Busy { scope } => Ok(IdentityDecision::Busy(scope)),
        IdentityResolution::Ambiguous { candidates } => {
            if !candidates.as_slice().is_empty() {
                return Ok(IdentityDecision::Ambiguous {
                    candidate_count: candidates.as_slice().len() as u64,
                });
            }
            // Genuine first open: reserve one id before releasing the catalog lock.
            let project_id = identity::allocate_project_id().map_err(StoreError::Identity)?;
            let now = evidence_store::now_unix_millis();
            let reservation = identity::build_reservation(project_id.clone(), facts, now)
                .map_err(StoreError::Identity)?;
            store.write_reservation(&catalog, &reservation)?;
            Ok(IdentityDecision::FirstOpen(project_id))
        }
    }
}

/// Build one immutable generation (identity + index records) and publish it,
/// then mark the catalog reservation initialized.
fn write_and_publish_generation(
    store: &EvidenceStore,
    project_id: &ProjectId,
    facts: &ProjectMatchFacts,
    locator: &ProjectLocator,
) -> Result<(), StoreError> {
    let now = evidence_store::now_unix_millis();
    let (catalog, project_lock) = store.lock_catalog_then_project(project_id, &never_cancelled)?;

    let worktree_id = identity::allocate_worktree_id().map_err(StoreError::Identity)?;
    let identity_record = identity::build_identity_record(
        project_id.clone(),
        worktree_id,
        facts,
        IdentityRecordState::Active,
    )
    .map_err(StoreError::Identity)?;
    let identity_bytes = canonical_project_json(&identity_record).map_err(StoreError::Codec)?;
    let index_bytes = canonical_project_json(locator).map_err(StoreError::Codec)?;

    let generation_id = identity::allocate_generation_id().map_err(StoreError::Identity)?;
    let identity_ref = identity::allocate_record_id().map_err(StoreError::Identity)?;
    let index_ref = identity::allocate_record_id().map_err(StoreError::Identity)?;

    let identity_digest = store.write_generation_record(
        &project_lock,
        project_id,
        &generation_id,
        &identity_ref,
        &identity_bytes,
    )?;
    let index_digest = store.write_generation_record(
        &project_lock,
        project_id,
        &generation_id,
        &index_ref,
        &index_bytes,
    )?;

    let manifest = evidence_store::build_manifest(
        project_id.clone(),
        generation_id.clone(),
        identity_ref,
        index_ref,
        EvidenceRecordRefs::try_from(Vec::new()).map_err(StoreError::Contract)?,
        vec![identity_digest, index_digest],
        now,
    )?;
    store.write_generation_manifest(&project_lock, &manifest)?;
    store.publish_generation(&project_lock, project_id, &generation_id)?;

    if let Some(reservation) = store.read_reservation(project_id)? {
        let completed = identity::complete_reservation(&reservation, project_id, now)
            .map_err(StoreError::Identity)?;
        store.write_reservation(&catalog, &completed)?;
    }
    Ok(())
}

// --------------------------------------------------------------------------
// `wepld doctor`
// --------------------------------------------------------------------------

fn run_doctor() -> CommandOutcome {
    let context = match build_context(".") {
        Ok(context) => context,
        Err(ContextError::Locator(reason)) => {
            return failure(
                Command::Doctor,
                ExitClass::ProjectResolutionIdentity,
                reason,
            );
        }
        Err(ContextError::StoreRootUnavailable(reason)) => {
            return failure(
                Command::Doctor,
                ExitClass::RequiredCapabilityUnavailable,
                reason,
            );
        }
        Err(ContextError::Store(reason)) => {
            return failure(Command::Doctor, ExitClass::EvidenceStoreIntegrity, reason);
        }
    };
    let now = evidence_store::now_unix_millis();

    let repository = observe_repository(&context.project_path, &context.store_root);
    let repository_obs = repository_observation(&repository);

    let (identity_obs, project_id, generation_id) = doctor_identity(
        &context,
        matches!(context.locator.resolved_path, Observation::Available { .. }),
    );

    let evidence_obs = match &project_id {
        Some(project_id) => doctor_evidence(&context.store, project_id, now),
        None => None,
    };

    let descriptors = scan_root_descriptors(&context.project_path);

    let inputs = DoctorInputs {
        project_id: project_id.unwrap_or_else(sentinel_project_id),
        selected_generation_id: generation_id,
        identity: identity_obs,
        repository: repository_obs,
        evidence_store: evidence_obs,
        descriptors,
        security_sensitive: SecuritySensitiveObservation::default(),
    };

    match doctor::evaluate(&inputs, now) {
        Ok(report) => CommandOutcome::Doctor { report },
        Err(error) => failure(
            Command::Doctor,
            ExitClass::UnexpectedInternal,
            format!("doctor_evaluation_failed: {error}"),
        ),
    }
}

fn doctor_identity(
    context: &Context,
    resolved_available: bool,
) -> (
    IdentityObservation,
    Option<ProjectId>,
    Option<wepld_contracts::GenerationId>,
) {
    if !resolved_available {
        return (IdentityObservation::Unavailable, None, None);
    }
    let facts = ProjectMatchFacts::new(context.locator.clone());
    match resolve_identity_readonly(&context.store, &facts) {
        Ok(IdentityDecision::Bound(id)) => (IdentityObservation::Bound, Some(id), None),
        Ok(IdentityDecision::ReservedRecovered(id)) => {
            (IdentityObservation::ReservedRecovered, Some(id), None)
        }
        Ok(IdentityDecision::FirstOpen(_)) => (IdentityObservation::Unavailable, None, None),
        Ok(IdentityDecision::Ambiguous { candidate_count: 0 }) => {
            (IdentityObservation::Unavailable, None, None)
        }
        Ok(IdentityDecision::Ambiguous { candidate_count }) => (
            IdentityObservation::Ambiguous { candidate_count },
            None,
            None,
        ),
        Ok(IdentityDecision::Conflict) => (IdentityObservation::Conflict, None, None),
        Ok(IdentityDecision::Busy(_)) | Err(_) => (IdentityObservation::Unavailable, None, None),
    }
}

fn doctor_evidence(
    store: &EvidenceStore,
    project_id: &ProjectId,
    now: wepld_contracts::UnixMillis,
) -> Option<EvidenceStoreObservation> {
    match store.read_published_generation(project_id) {
        Ok(published) => {
            let freshness =
                EvidenceStore::freshness(&published.manifest, now, EVIDENCE_MAX_AGE_MILLIS);
            Some(EvidenceStoreObservation {
                status: freshness.status,
                integrity_defect: false,
                stale_required_record: matches!(freshness.status, EvidenceStatus::Stale),
                authenticity: EvidenceStore::authenticity(),
            })
        }
        Err(StoreError::Defect(evidence_store::StoreDefect::CurrentMissing)) => None,
        Err(StoreError::Defect(_)) => Some(EvidenceStoreObservation {
            status: EvidenceStatus::Corrupt,
            integrity_defect: true,
            stale_required_record: false,
            authenticity: EvidenceStore::authenticity(),
        }),
        Err(_) => Some(EvidenceStoreObservation {
            status: EvidenceStatus::Unavailable,
            integrity_defect: false,
            stale_required_record: false,
            authenticity: EvidenceStore::authenticity(),
        }),
    }
}

// --------------------------------------------------------------------------
// `wepld status`
// --------------------------------------------------------------------------

fn run_status() -> CommandOutcome {
    let context = match build_context(".") {
        Ok(context) => context,
        Err(ContextError::Locator(reason)) => {
            return failure(
                Command::Status,
                ExitClass::ProjectResolutionIdentity,
                reason,
            );
        }
        Err(ContextError::StoreRootUnavailable(reason)) => {
            return failure(
                Command::Status,
                ExitClass::RequiredCapabilityUnavailable,
                reason,
            );
        }
        Err(ContextError::Store(reason)) => {
            return failure(Command::Status, ExitClass::EvidenceStoreIntegrity, reason);
        }
    };

    if !matches!(context.locator.resolved_path, Observation::Available { .. }) {
        return CommandOutcome::Status {
            project_id: None,
            associated: false,
            evidence: EvidenceSummary::Unavailable,
        };
    }

    let facts = ProjectMatchFacts::new(context.locator.clone());
    let project_id = match resolve_identity_readonly(&context.store, &facts) {
        Ok(IdentityDecision::Bound(id)) | Ok(IdentityDecision::ReservedRecovered(id)) => id,
        Ok(IdentityDecision::Conflict) => {
            return failure(
                Command::Status,
                ExitClass::ProjectResolutionIdentity,
                "identity_conflict: contradictory topology evidence".to_owned(),
            );
        }
        Ok(_) => {
            return CommandOutcome::Status {
                project_id: None,
                associated: false,
                evidence: EvidenceSummary::Unavailable,
            };
        }
        Err(error) => return store_failure(Command::Status, &error),
    };

    match context.store.read_published_generation(&project_id) {
        Ok(published) => {
            let now = evidence_store::now_unix_millis();
            let freshness =
                EvidenceStore::freshness(&published.manifest, now, EVIDENCE_MAX_AGE_MILLIS);
            CommandOutcome::Status {
                project_id: Some(project_id.as_str().to_owned()),
                associated: true,
                evidence: EvidenceSummary::Present {
                    status: freshness.status,
                    authenticity: EvidenceStore::authenticity(),
                },
            }
        }
        Err(StoreError::Defect(evidence_store::StoreDefect::CurrentMissing)) => {
            CommandOutcome::Status {
                project_id: Some(project_id.as_str().to_owned()),
                associated: false,
                evidence: EvidenceSummary::Unavailable,
            }
        }
        Err(StoreError::Defect(defect)) => failure(
            Command::Status,
            ExitClass::EvidenceStoreIntegrity,
            format!("store_defect: {defect}"),
        ),
        Err(error) => store_failure(Command::Status, &error),
    }
}

// --------------------------------------------------------------------------
// Helpers
// --------------------------------------------------------------------------

fn machine_path_of_lexical(locator: &ProjectLocator) -> &MachinePath {
    &locator.lexical_absolute_path
}

fn sentinel_project_id() -> ProjectId {
    ProjectId::try_from("p_unresolved").expect("static sentinel project id is contract-valid")
}

fn failure(command: Command, class: ExitClass, reason: String) -> CommandOutcome {
    CommandOutcome::Failure {
        command,
        class,
        reason,
    }
}

fn store_failure(command: Command, error: &StoreError) -> CommandOutcome {
    let class = match error {
        StoreError::Busy { .. } | StoreError::Cancelled { .. } => {
            ExitClass::RequiredCapabilityUnavailable
        }
        StoreError::Defect(_)
        | StoreError::TooLarge { .. }
        | StoreError::GenerationAlreadyClosed
        | StoreError::Codec(_)
        | StoreError::Contract(_) => ExitClass::EvidenceStoreIntegrity,
        StoreError::Identity(_) => ExitClass::ProjectResolutionIdentity,
        StoreError::UnsafeIdentifier
        | StoreError::RelativeStoreRoot
        | StoreError::WrongProjectLock
        | StoreError::ForeignLock
        | StoreError::LockOrderViolation
        | StoreError::Io(_) => ExitClass::UnexpectedInternal,
    };
    failure(
        command,
        class,
        format!("store_error: {}", store_error_reason(error)),
    )
}

fn store_error_reason(error: &StoreError) -> String {
    match error {
        StoreError::Busy { scope } => {
            format!("busy:{}", evidence_store::busy_error_code(*scope))
        }
        StoreError::Cancelled { .. } => "cancelled".to_owned(),
        StoreError::Defect(defect) => format!("defect:{defect}"),
        StoreError::TooLarge { limit } => format!("too_large:{limit}"),
        StoreError::UnsafeIdentifier => "unsafe_identifier".to_owned(),
        StoreError::RelativeStoreRoot => "relative_store_root".to_owned(),
        StoreError::WrongProjectLock => "wrong_project_lock".to_owned(),
        StoreError::ForeignLock => "foreign_lock".to_owned(),
        StoreError::GenerationAlreadyClosed => "generation_already_closed".to_owned(),
        StoreError::LockOrderViolation => "lock_order_violation".to_owned(),
        StoreError::Identity(_) => "identity_error".to_owned(),
        StoreError::Contract(_) => "contract_value_error".to_owned(),
        StoreError::Codec(_) => "contract_codec_error".to_owned(),
        StoreError::Io(_) => "io_error".to_owned(),
    }
}

fn emit(outcome: &CommandOutcome, mode: OutputMode) -> ExitCode {
    let rendered = cli::render(outcome, mode);
    let class = outcome.exit_class();
    // A completed command result — success, or a Doctor report whose findings
    // merely happen to be blocking — is primary output and goes to stdout so a
    // `--json` consumer reads it the same way regardless of exit code. Only a
    // genuine failure (usage, resolution, integrity, capability, internal) is
    // written to stderr.
    if matches!(
        class,
        ExitClass::Success | ExitClass::DoctorBlockingFindings
    ) {
        print!("{rendered}");
    } else {
        eprint!("{rendered}");
    }
    ExitCode::from(class.code() as u8)
}
