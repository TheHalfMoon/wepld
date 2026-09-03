#![forbid(unsafe_code)]

use std::env;
use std::ffi::{OsStr, OsString};
use std::fmt;
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use std::process::{Child, Command, ExitStatus, Stdio};
use std::sync::Arc;
use std::sync::atomic::{AtomicU8, Ordering};
use std::thread;
use std::time::{Duration, Instant, SystemTime};

use wepld_contracts::{
    LinkedWorktreeState, Observation, ObservationErrorClass, OptionalObservation,
    ProjectContractVersion, RepositoryTopology, RepositoryTrustState, VcsKind,
};

use crate::project::{ProjectObservationError, machine_path_from_path};

#[cfg(unix)]
use std::os::unix::ffi::OsStringExt as _;
#[cfg(unix)]
use std::os::unix::fs::PermissionsExt as _;

pub const GIT_TOPOLOGY_TIMEOUT_MS: u64 = 10_000;
pub const GIT_STDOUT_MAX_BYTES: usize = 1_048_576;
pub const GIT_STDERR_MAX_BYTES: usize = 262_144;
pub const GIT_PROCESS_POLL_INTERVAL_MS: u64 = 5;
pub const MAX_WORKTREE_RECORDS: usize = 4_096;

const STDOUT_OVERFLOW: u8 = 0b01;
const STDERR_OVERFLOW: u8 = 0b10;
const GIT_GLOBAL_FLAGS: [&str; 3] = ["--no-pager", "--no-optional-locks", "--no-lazy-fetch"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GitVersionEvidence {
    /// v45 does not authorize a semantic-version argv family such as
    /// `git --version`. Do not widen authority merely to obtain a version string.
    NotObservedUnderCurrentAuthority,
}

/// An opaque proof that one absolute system Git executable passed the closed
/// discovery contract (`discover_system_git` / `qualify_git_executable`): PATH
/// entries only, first qualified match with no silent fallback, symlink
/// resolution, regular-executable check, and refusal of a candidate resolving
/// inside the opened project or the WePLD evidence root.
///
/// The fields are private and there is no public constructor, so a caller
/// cannot forge one to hand `observe_git_topology` an unqualified path:
///
/// ```compile_fail
/// use std::path::PathBuf;
/// use wepld_core::git_topology::QualifiedGitExecutable;
/// let _forged = QualifiedGitExecutable {
///     resolved_path: PathBuf::from("/tmp/attacker/git"),
/// };
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QualifiedGitExecutable {
    lexical_path: PathBuf,
    resolved_path: PathBuf,
    file_len: u64,
    modified_at: Option<SystemTime>,
    version_evidence: GitVersionEvidence,
}

impl QualifiedGitExecutable {
    /// The PATH entry joined with the platform Git filename, before symlink
    /// resolution.
    pub fn lexical_path(&self) -> &Path {
        &self.lexical_path
    }

    /// The canonicalized (symlink-resolved) absolute executable path actually
    /// spawned.
    pub fn resolved_path(&self) -> &Path {
        &self.resolved_path
    }

    /// Byte length of the resolved executable at qualification time.
    pub fn file_len(&self) -> u64 {
        self.file_len
    }

    /// Modification time of the resolved executable at qualification time, when
    /// the platform reports one.
    pub fn modified_at(&self) -> Option<SystemTime> {
        self.modified_at
    }

    /// Always [`GitVersionEvidence::NotObservedUnderCurrentAuthority`]; v45 does
    /// not authorize a `git --version` argv family.
    pub fn version_evidence(&self) -> GitVersionEvidence {
        self.version_evidence
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GitOutputStream {
    Stdout,
    Stderr,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GitTopologyError {
    SearchPathUnavailable,
    UnsafeSearchPathEntry,
    ExecutableUnavailable,
    ExecutableCandidateInvalid,
    ExecutableInsideOpenedProject,
    ExecutableInsideEvidenceRoot,
    BoundaryPathUnavailable,
    NotGitRepository,
    UntrustedRepositoryRefusedByGit,
    UnsupportedGitCapability,
    GitTimeout,
    GitCancelled,
    GitOutputTooLarge {
        stream: GitOutputStream,
        max_bytes: usize,
    },
    GitOutputMalformed {
        field: &'static str,
    },
    GitProcessFailed {
        code: Option<i32>,
    },
    ChangedUnderObservation,
    Io {
        operation: &'static str,
        kind: io::ErrorKind,
    },
    Project(ProjectObservationError),
    ReaderThreadPanicked,
}

impl fmt::Display for GitTopologyError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::SearchPathUnavailable => {
                write!(formatter, "system executable search path is unavailable")
            }
            Self::UnsafeSearchPathEntry => write!(
                formatter,
                "system executable search path contains a relative entry"
            ),
            Self::ExecutableUnavailable => {
                write!(formatter, "qualified system Git executable is unavailable")
            }
            Self::ExecutableCandidateInvalid => write!(
                formatter,
                "first discovered Git executable candidate is not qualified"
            ),
            Self::ExecutableInsideOpenedProject => write!(
                formatter,
                "Git executable resolves inside the opened project"
            ),
            Self::ExecutableInsideEvidenceRoot => write!(
                formatter,
                "Git executable resolves inside the WePLD evidence root"
            ),
            Self::BoundaryPathUnavailable => write!(
                formatter,
                "project/evidence boundary cannot be resolved for executable qualification"
            ),
            Self::NotGitRepository => write!(formatter, "path is not inside a Git repository"),
            Self::UntrustedRepositoryRefusedByGit => write!(
                formatter,
                "Git refused repository access at its protected trust boundary"
            ),
            Self::UnsupportedGitCapability => write!(
                formatter,
                "installed Git lacks a required closed topology capability"
            ),
            Self::GitTimeout => write!(
                formatter,
                "Git topology observation exceeded the hard timeout"
            ),
            Self::GitCancelled => write!(formatter, "Git topology observation was cancelled"),
            Self::GitOutputTooLarge { stream, max_bytes } => write!(
                formatter,
                "Git {stream:?} exceeded the {max_bytes}-byte capture bound"
            ),
            Self::GitOutputMalformed { field } => {
                write!(formatter, "Git topology output is malformed: {field}")
            }
            Self::GitProcessFailed { code } => write!(
                formatter,
                "Git topology process failed with exit code {code:?}"
            ),
            Self::ChangedUnderObservation => write!(
                formatter,
                "Git topology changed during one bounded observation"
            ),
            Self::Io { operation, kind } => write!(
                formatter,
                "Git topology I/O failure during {operation}: {kind:?}"
            ),
            Self::Project(error) => write!(formatter, "project-path conversion failed: {error}"),
            Self::ReaderThreadPanicked => {
                write!(formatter, "bounded Git output reader thread panicked")
            }
        }
    }
}

impl std::error::Error for GitTopologyError {}

impl From<ProjectObservationError> for GitTopologyError {
    fn from(value: ProjectObservationError) -> Self {
        Self::Project(value)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum RevParseQuery {
    WorktreeRoot,
    AbsoluteGitDir,
    GitCommonDir,
    IsBare,
    IsInsideWorktree,
    SuperprojectWorktree,
}

impl RevParseQuery {
    fn argv(self) -> &'static [&'static str] {
        match self {
            Self::WorktreeRoot => &["--path-format=absolute", "--show-toplevel"],
            Self::AbsoluteGitDir => &["--path-format=absolute", "--absolute-git-dir"],
            Self::GitCommonDir => &["--path-format=absolute", "--git-common-dir"],
            Self::IsBare => &["--is-bare-repository"],
            Self::IsInsideWorktree => &["--is-inside-work-tree"],
            Self::SuperprojectWorktree => {
                &["--path-format=absolute", "--show-superproject-working-tree"]
            }
        }
    }
}

#[derive(Debug)]
struct GitRunOutput {
    stdout: Vec<u8>,
    stderr: Vec<u8>,
    status: ExitStatus,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ForcedTermination {
    Timeout,
    Cancelled,
    OutputOverflow(u8),
}

pub fn discover_system_git(
    opened_project: &Path,
    evidence_root: &Path,
) -> Result<QualifiedGitExecutable, GitTopologyError> {
    let path = env::var_os("PATH").ok_or(GitTopologyError::SearchPathUnavailable)?;
    let executable_name = if cfg!(windows) { "git.exe" } else { "git" };

    for directory in env::split_paths(&path) {
        if !directory.is_absolute() {
            return Err(GitTopologyError::UnsafeSearchPathEntry);
        }
        let candidate = directory.join(executable_name);
        match fs::symlink_metadata(&candidate) {
            Ok(_) => return qualify_git_executable(&candidate, opened_project, evidence_root),
            Err(error) if error.kind() == io::ErrorKind::NotFound => continue,
            Err(error) => {
                return Err(GitTopologyError::Io {
                    operation: "inspect executable candidate",
                    kind: error.kind(),
                });
            }
        }
    }

    Err(GitTopologyError::ExecutableUnavailable)
}

pub fn qualify_git_executable(
    lexical_path: &Path,
    opened_project: &Path,
    evidence_root: &Path,
) -> Result<QualifiedGitExecutable, GitTopologyError> {
    if !lexical_path.is_absolute() {
        return Err(GitTopologyError::ExecutableCandidateInvalid);
    }

    let resolved_path = fs::canonicalize(lexical_path).map_err(|error| GitTopologyError::Io {
        operation: "resolve Git executable",
        kind: error.kind(),
    })?;
    let metadata = fs::metadata(&resolved_path).map_err(|error| GitTopologyError::Io {
        operation: "inspect Git executable",
        kind: error.kind(),
    })?;
    if !metadata.is_file() || !is_executable_file(&metadata) {
        return Err(GitTopologyError::ExecutableCandidateInvalid);
    }

    let project_boundary =
        fs::canonicalize(opened_project).map_err(|_| GitTopologyError::BoundaryPathUnavailable)?;
    let evidence_boundary =
        fs::canonicalize(evidence_root).map_err(|_| GitTopologyError::BoundaryPathUnavailable)?;

    if resolved_path.starts_with(&project_boundary) {
        return Err(GitTopologyError::ExecutableInsideOpenedProject);
    }
    if resolved_path.starts_with(&evidence_boundary) {
        return Err(GitTopologyError::ExecutableInsideEvidenceRoot);
    }

    Ok(QualifiedGitExecutable {
        lexical_path: lexical_path.to_path_buf(),
        resolved_path,
        file_len: metadata.len(),
        modified_at: metadata.modified().ok(),
        version_evidence: GitVersionEvidence::NotObservedUnderCurrentAuthority,
    })
}

#[cfg(unix)]
fn is_executable_file(metadata: &fs::Metadata) -> bool {
    metadata.permissions().mode() & 0o111 != 0
}

#[cfg(not(unix))]
fn is_executable_file(_metadata: &fs::Metadata) -> bool {
    true
}

pub fn sanitized_git_environment_from<I>(environment: I) -> Vec<(OsString, OsString)>
where
    I: IntoIterator<Item = (OsString, OsString)>,
{
    let mut sanitized = Vec::new();
    for (key, value) in environment {
        if environment_key_is_removed(&key) {
            continue;
        }
        sanitized.push((key, value));
    }
    sanitized.push((OsString::from("GIT_TERMINAL_PROMPT"), OsString::from("0")));
    sanitized.push((OsString::from("LC_ALL"), OsString::from("C")));
    sanitized.push((OsString::from("LANG"), OsString::from("C")));
    sanitized
}

fn environment_key_is_removed(key: &OsStr) -> bool {
    let upper = key.to_string_lossy().to_ascii_uppercase();
    upper.starts_with("GIT_")
        || upper == "LC_ALL"
        || upper == "LANG"
        || upper == "SSH_ASKPASS"
        || upper == "PAGER"
        || upper == "LESS"
        || upper == "LV"
        || upper == "LD_PRELOAD"
        || upper == "LD_LIBRARY_PATH"
        || upper.starts_with("DYLD_")
}

pub fn observe_git_topology(
    git: &QualifiedGitExecutable,
    locator: &Path,
) -> Result<RepositoryTopology, GitTopologyError> {
    observe_git_topology_with_cancel(git, locator, &|| false)
}

pub fn observe_git_topology_with_cancel<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    cancelled: &F,
) -> Result<RepositoryTopology, GitTopologyError>
where
    F: Fn() -> bool,
{
    let is_bare = match rev_parse_bool(git, locator, RevParseQuery::IsBare, cancelled) {
        Ok(value) => value,
        Err(GitTopologyError::UntrustedRepositoryRefusedByGit) => return Ok(refused_topology()),
        Err(error) => return Err(error),
    };
    let is_inside_worktree =
        rev_parse_bool(git, locator, RevParseQuery::IsInsideWorktree, cancelled)?;
    let absolute_git_dir = rev_parse_path(git, locator, RevParseQuery::AbsoluteGitDir, cancelled)?;
    let git_common_dir = rev_parse_path(git, locator, RevParseQuery::GitCommonDir, cancelled)?;

    let worktree_root = if is_bare {
        Observation::Unavailable {
            error: ObservationErrorClass::NotApplicable,
        }
    } else {
        let path = rev_parse_path(git, locator, RevParseQuery::WorktreeRoot, cancelled)?;
        Observation::Available {
            value: machine_path_from_path(&path)?,
        }
    };

    let superproject_bytes =
        run_rev_parse(git, locator, RevParseQuery::SuperprojectWorktree, cancelled)?;
    let superproject_worktree = if superproject_bytes.is_empty() {
        OptionalObservation::None
    } else {
        let path = absolute_path_from_git_bytes(&superproject_bytes, "superproject_worktree")?;
        OptionalObservation::Value {
            value: machine_path_from_path(&path)?,
        }
    };

    let linked_worktree_state = match run_worktree_list(git, locator, cancelled) {
        Ok(output) => {
            validate_worktree_porcelain_z(&output)?;
            LinkedWorktreeState::Known
        }
        Err(GitTopologyError::UnsupportedGitCapability) => LinkedWorktreeState::Unknown,
        Err(error) => return Err(error),
    };

    let topology = RepositoryTopology {
        schema_version: ProjectContractVersion::V1,
        vcs_kind: VcsKind::Git,
        worktree_root,
        absolute_git_dir: Observation::Available {
            value: machine_path_from_path(&absolute_git_dir)?,
        },
        git_common_dir: Observation::Available {
            value: machine_path_from_path(&git_common_dir)?,
        },
        is_bare: Observation::Available { value: is_bare },
        is_inside_worktree: Observation::Available {
            value: is_inside_worktree,
        },
        superproject_worktree,
        linked_worktree_state,
        trust_state: RepositoryTrustState::Trusted,
    };

    verify_stable_topology(git, locator, &topology, cancelled)?;
    Ok(topology)
}

fn unavailable_trust<T>() -> Observation<T> {
    Observation::Unavailable {
        error: ObservationErrorClass::TrustRefused,
    }
}

fn refused_topology() -> RepositoryTopology {
    RepositoryTopology {
        schema_version: ProjectContractVersion::V1,
        vcs_kind: VcsKind::Git,
        worktree_root: unavailable_trust(),
        absolute_git_dir: unavailable_trust(),
        git_common_dir: unavailable_trust(),
        is_bare: unavailable_trust(),
        is_inside_worktree: unavailable_trust(),
        superproject_worktree: OptionalObservation::Unavailable {
            error: ObservationErrorClass::TrustRefused,
        },
        linked_worktree_state: LinkedWorktreeState::Unknown,
        trust_state: RepositoryTrustState::RefusedByGit,
    }
}

fn verify_stable_topology<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    first: &RepositoryTopology,
    cancelled: &F,
) -> Result<(), GitTopologyError>
where
    F: Fn() -> bool,
{
    let bare = rev_parse_bool(git, locator, RevParseQuery::IsBare, cancelled)?;
    let inside = rev_parse_bool(git, locator, RevParseQuery::IsInsideWorktree, cancelled)?;
    let git_dir = rev_parse_path(git, locator, RevParseQuery::AbsoluteGitDir, cancelled)?;
    let common_dir = rev_parse_path(git, locator, RevParseQuery::GitCommonDir, cancelled)?;

    if first.is_bare != (Observation::Available { value: bare })
        || first.is_inside_worktree != (Observation::Available { value: inside })
        || first.absolute_git_dir
            != (Observation::Available {
                value: machine_path_from_path(&git_dir)?,
            })
        || first.git_common_dir
            != (Observation::Available {
                value: machine_path_from_path(&common_dir)?,
            })
    {
        return Err(GitTopologyError::ChangedUnderObservation);
    }
    Ok(())
}

fn rev_parse_bool<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    query: RevParseQuery,
    cancelled: &F,
) -> Result<bool, GitTopologyError>
where
    F: Fn() -> bool,
{
    let bytes = run_rev_parse(git, locator, query, cancelled)?;
    match bytes.as_slice() {
        b"true" => Ok(true),
        b"false" => Ok(false),
        _ => Err(GitTopologyError::GitOutputMalformed {
            field: "boolean rev-parse result",
        }),
    }
}

fn rev_parse_path<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    query: RevParseQuery,
    cancelled: &F,
) -> Result<PathBuf, GitTopologyError>
where
    F: Fn() -> bool,
{
    let bytes = run_rev_parse(git, locator, query, cancelled)?;
    absolute_path_from_git_bytes(&bytes, "absolute rev-parse path")
}

fn run_rev_parse<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    query: RevParseQuery,
    cancelled: &F,
) -> Result<Vec<u8>, GitTopologyError>
where
    F: Fn() -> bool,
{
    let mut args = Vec::with_capacity(1 + query.argv().len());
    args.push(OsString::from("rev-parse"));
    args.extend(query.argv().iter().map(OsString::from));
    let output = ensure_success(run_git(git, locator, &args, cancelled)?)?;
    strip_terminal_line_ending(output)
}

fn run_worktree_list<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    cancelled: &F,
) -> Result<Vec<u8>, GitTopologyError>
where
    F: Fn() -> bool,
{
    let args = [
        OsString::from("worktree"),
        OsString::from("list"),
        OsString::from("--porcelain"),
        OsString::from("-z"),
    ];
    ensure_success(run_git(git, locator, &args, cancelled)?)
}

fn ensure_success(output: GitRunOutput) -> Result<Vec<u8>, GitTopologyError> {
    if output.status.success() {
        return Ok(output.stdout);
    }
    Err(classify_git_failure(&output.stderr, output.status.code()))
}

fn run_git<F>(
    git: &QualifiedGitExecutable,
    locator: &Path,
    args: &[OsString],
    cancelled: &F,
) -> Result<GitRunOutput, GitTopologyError>
where
    F: Fn() -> bool,
{
    if !git.resolved_path.is_absolute() {
        return Err(GitTopologyError::ExecutableCandidateInvalid);
    }

    let mut command = Command::new(&git.resolved_path);
    command.args(GIT_GLOBAL_FLAGS);
    command.arg("-C").arg(locator);
    command.args(args);
    command.stdin(Stdio::null());
    command.stdout(Stdio::piped());
    command.stderr(Stdio::piped());
    if let Some(parent) = git.resolved_path.parent() {
        command.current_dir(parent);
    }
    command.env_clear();
    for (key, value) in sanitized_git_environment_from(env::vars_os()) {
        command.env(key, value);
    }

    let mut child = command.spawn().map_err(|error| GitTopologyError::Io {
        operation: "spawn qualified Git",
        kind: error.kind(),
    })?;
    let stdout = child.stdout.take().ok_or(GitTopologyError::Io {
        operation: "capture Git stdout",
        kind: io::ErrorKind::BrokenPipe,
    })?;
    let stderr = child.stderr.take().ok_or(GitTopologyError::Io {
        operation: "capture Git stderr",
        kind: io::ErrorKind::BrokenPipe,
    })?;

    let overflow = Arc::new(AtomicU8::new(0));
    let stdout_reader = spawn_bounded_reader(
        stdout,
        GIT_STDOUT_MAX_BYTES,
        STDOUT_OVERFLOW,
        Arc::clone(&overflow),
    );
    let stderr_reader = spawn_bounded_reader(
        stderr,
        GIT_STDERR_MAX_BYTES,
        STDERR_OVERFLOW,
        Arc::clone(&overflow),
    );

    let started = Instant::now();
    let mut forced = None;
    let status = loop {
        let overflow_bits = overflow.load(Ordering::Acquire);
        if overflow_bits != 0 {
            forced = Some(ForcedTermination::OutputOverflow(overflow_bits));
            break kill_and_reap(&mut child)?;
        }
        if cancelled() {
            forced = Some(ForcedTermination::Cancelled);
            break kill_and_reap(&mut child)?;
        }
        if started.elapsed() >= Duration::from_millis(GIT_TOPOLOGY_TIMEOUT_MS) {
            forced = Some(ForcedTermination::Timeout);
            break kill_and_reap(&mut child)?;
        }
        match child.try_wait().map_err(|error| GitTopologyError::Io {
            operation: "poll qualified Git",
            kind: error.kind(),
        })? {
            Some(status) => break status,
            None => thread::sleep(Duration::from_millis(GIT_PROCESS_POLL_INTERVAL_MS)),
        }
    };

    let stdout = join_reader(stdout_reader)?;
    let stderr = join_reader(stderr_reader)?;
    let overflow_bits = overflow.load(Ordering::Acquire);
    if forced.is_none() && overflow_bits != 0 {
        forced = Some(ForcedTermination::OutputOverflow(overflow_bits));
    }

    match forced {
        Some(ForcedTermination::Timeout) => return Err(GitTopologyError::GitTimeout),
        Some(ForcedTermination::Cancelled) => return Err(GitTopologyError::GitCancelled),
        Some(ForcedTermination::OutputOverflow(bits)) => {
            if bits & STDOUT_OVERFLOW != 0 {
                return Err(GitTopologyError::GitOutputTooLarge {
                    stream: GitOutputStream::Stdout,
                    max_bytes: GIT_STDOUT_MAX_BYTES,
                });
            }
            return Err(GitTopologyError::GitOutputTooLarge {
                stream: GitOutputStream::Stderr,
                max_bytes: GIT_STDERR_MAX_BYTES,
            });
        }
        None => {}
    }

    Ok(GitRunOutput {
        stdout,
        stderr,
        status,
    })
}

fn spawn_bounded_reader<R>(
    mut reader: R,
    max_bytes: usize,
    overflow_bit: u8,
    overflow: Arc<AtomicU8>,
) -> thread::JoinHandle<io::Result<Vec<u8>>>
where
    R: Read + Send + 'static,
{
    thread::spawn(move || {
        let mut output = Vec::with_capacity(max_bytes.min(8_192));
        let mut buffer = [0_u8; 8_192];
        loop {
            let read = reader.read(&mut buffer)?;
            if read == 0 {
                break;
            }
            let remaining = max_bytes.saturating_sub(output.len());
            if read > remaining {
                output.extend_from_slice(&buffer[..remaining]);
                overflow.fetch_or(overflow_bit, Ordering::Release);
                break;
            }
            output.extend_from_slice(&buffer[..read]);
        }
        Ok(output)
    })
}

fn join_reader(
    handle: thread::JoinHandle<io::Result<Vec<u8>>>,
) -> Result<Vec<u8>, GitTopologyError> {
    handle
        .join()
        .map_err(|_| GitTopologyError::ReaderThreadPanicked)?
        .map_err(|error| GitTopologyError::Io {
            operation: "read bounded Git output",
            kind: error.kind(),
        })
}

fn kill_and_reap(child: &mut Child) -> Result<ExitStatus, GitTopologyError> {
    match child.kill() {
        Ok(()) => {}
        Err(error) if error.kind() == io::ErrorKind::InvalidInput => {}
        Err(error) => {
            return Err(GitTopologyError::Io {
                operation: "terminate qualified Git",
                kind: error.kind(),
            });
        }
    }
    child.wait().map_err(|error| GitTopologyError::Io {
        operation: "reap qualified Git",
        kind: error.kind(),
    })
}

fn strip_terminal_line_ending(mut bytes: Vec<u8>) -> Result<Vec<u8>, GitTopologyError> {
    if bytes.contains(&0) {
        return Err(GitTopologyError::GitOutputMalformed {
            field: "unexpected NUL in scalar result",
        });
    }
    if bytes.ends_with(b"\n") {
        bytes.pop();
        if bytes.ends_with(b"\r") {
            bytes.pop();
        }
    }
    Ok(bytes)
}

fn absolute_path_from_git_bytes(
    bytes: &[u8],
    field: &'static str,
) -> Result<PathBuf, GitTopologyError> {
    if bytes.is_empty() {
        return Err(GitTopologyError::GitOutputMalformed { field });
    }
    let path = path_from_git_bytes(bytes, field)?;
    if !path.is_absolute() {
        return Err(GitTopologyError::GitOutputMalformed { field });
    }
    Ok(path)
}

#[cfg(unix)]
fn path_from_git_bytes(bytes: &[u8], _field: &'static str) -> Result<PathBuf, GitTopologyError> {
    Ok(PathBuf::from(OsString::from_vec(bytes.to_vec())))
}

#[cfg(windows)]
fn path_from_git_bytes(bytes: &[u8], field: &'static str) -> Result<PathBuf, GitTopologyError> {
    let value = String::from_utf8(bytes.to_vec())
        .map_err(|_| GitTopologyError::GitOutputMalformed { field })?;
    Ok(PathBuf::from(value))
}

#[cfg(not(any(unix, windows)))]
fn path_from_git_bytes(_bytes: &[u8], field: &'static str) -> Result<PathBuf, GitTopologyError> {
    Err(GitTopologyError::GitOutputMalformed { field })
}

pub fn validate_worktree_porcelain_z(output: &[u8]) -> Result<usize, GitTopologyError> {
    if output.is_empty() || !output.ends_with(&[0]) {
        return Err(GitTopologyError::GitOutputMalformed {
            field: "worktree porcelain must be NUL terminated",
        });
    }

    let mut record_count = 0usize;
    let mut has_worktree_path = false;
    let mut saw_attribute = false;
    // Every validated worktree path for the whole parse. `git worktree list`
    // never repeats a path; a repeat - within one record or across records -
    // is malformed. Bounded: at most one insert per record, and the record
    // count is capped at MAX_WORKTREE_RECORDS.
    let mut seen_paths: std::collections::BTreeSet<Vec<u8>> = std::collections::BTreeSet::new();

    for field in output.split(|byte| *byte == 0) {
        if field.is_empty() {
            if saw_attribute {
                finish_worktree_record(has_worktree_path, &mut record_count)?;
                has_worktree_path = false;
                saw_attribute = false;
            }
            continue;
        }

        saw_attribute = true;
        if let Some(path_bytes) = field.strip_prefix(b"worktree ") {
            if has_worktree_path {
                return Err(GitTopologyError::GitOutputMalformed {
                    field: "duplicate worktree path",
                });
            }
            absolute_path_from_git_bytes(path_bytes, "worktree path")?;
            if !seen_paths.insert(path_bytes.to_vec()) {
                return Err(GitTopologyError::GitOutputMalformed {
                    field: "repeated worktree path across records",
                });
            }
            has_worktree_path = true;
            continue;
        }
        if let Some(head) = field.strip_prefix(b"HEAD ") {
            if !valid_object_id(head) {
                return Err(GitTopologyError::GitOutputMalformed {
                    field: "worktree HEAD object id",
                });
            }
            continue;
        }
        if field == b"bare"
            || field == b"detached"
            || field.starts_with(b"branch ")
            || field == b"locked"
            || field.starts_with(b"locked ")
            || field == b"prunable"
            || field.starts_with(b"prunable ")
        {
            continue;
        }
        // Unknown future porcelain attributes remain bounded and are ignored;
        // they are never reinterpreted as a known field or persisted as prose.
    }

    if saw_attribute {
        finish_worktree_record(has_worktree_path, &mut record_count)?;
    }
    if record_count == 0 {
        return Err(GitTopologyError::GitOutputMalformed {
            field: "empty worktree record set",
        });
    }
    Ok(record_count)
}

fn finish_worktree_record(
    has_worktree_path: bool,
    record_count: &mut usize,
) -> Result<(), GitTopologyError> {
    if !has_worktree_path {
        return Err(GitTopologyError::GitOutputMalformed {
            field: "worktree record without worktree path",
        });
    }
    *record_count += 1;
    if *record_count > MAX_WORKTREE_RECORDS {
        return Err(GitTopologyError::GitOutputMalformed {
            field: "too many worktree records",
        });
    }
    Ok(())
}

fn valid_object_id(value: &[u8]) -> bool {
    matches!(value.len(), 40 | 64) && value.iter().all(|byte| byte.is_ascii_hexdigit())
}

fn classify_git_failure(stderr: &[u8], code: Option<i32>) -> GitTopologyError {
    let stderr = String::from_utf8_lossy(stderr).to_ascii_lowercase();
    if stderr.contains("detected dubious ownership in repository")
        || stderr.contains("safe.directory")
        || stderr.contains("unsafe repository")
    {
        return GitTopologyError::UntrustedRepositoryRefusedByGit;
    }
    if stderr.contains("not a git repository") {
        return GitTopologyError::NotGitRepository;
    }
    if stderr.contains("unknown option")
        || stderr.contains("unknown switch")
        || stderr.contains("unrecognized option")
    {
        return GitTopologyError::UnsupportedGitCapability;
    }
    GitTopologyError::GitProcessFailed { code }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn environment_scrub_removes_git_and_loader_override_routes() {
        let input = vec![
            (OsString::from("HOME"), OsString::from("/home/user")),
            (OsString::from("GIT_DIR"), OsString::from("/attacker")),
            (OsString::from("GIT_CONFIG_COUNT"), OsString::from("1")),
            (
                OsString::from("GIT_TRACE2_EVENT"),
                OsString::from("/tmp/trace"),
            ),
            (
                OsString::from("LD_PRELOAD"),
                OsString::from("/tmp/inject.so"),
            ),
            (OsString::from("LC_ALL"), OsString::from("ar_SA.UTF-8")),
        ];
        let sanitized = sanitized_git_environment_from(input);
        assert!(
            sanitized
                .iter()
                .any(|(key, value)| key == "HOME" && value == "/home/user")
        );
        assert!(!sanitized.iter().any(|(key, _)| key == "GIT_DIR"));
        assert!(!sanitized.iter().any(|(key, _)| key == "GIT_CONFIG_COUNT"));
        assert!(!sanitized.iter().any(|(key, _)| key == "GIT_TRACE2_EVENT"));
        assert!(!sanitized.iter().any(|(key, _)| key == "LD_PRELOAD"));
        assert!(
            sanitized
                .iter()
                .any(|(key, value)| key == "GIT_TERMINAL_PROMPT" && value == "0")
        );
        assert!(
            sanitized
                .iter()
                .any(|(key, value)| key == "LC_ALL" && value == "C")
        );
    }

    #[test]
    fn bounded_reader_stops_at_limit_and_signals_overflow() {
        let overflow = Arc::new(AtomicU8::new(0));
        let reader = spawn_bounded_reader(
            Cursor::new(vec![b'x'; 33]),
            32,
            STDOUT_OVERFLOW,
            Arc::clone(&overflow),
        );
        let bytes = join_reader(reader).expect("reader must complete");
        assert_eq!(bytes.len(), 32);
        assert_eq!(overflow.load(Ordering::Acquire), STDOUT_OVERFLOW);
    }

    #[test]
    fn failure_classifier_maps_only_safe_closed_classes() {
        assert_eq!(
            classify_git_failure(b"fatal: not a git repository (or any parent)", Some(128)),
            GitTopologyError::NotGitRepository
        );
        assert_eq!(
            classify_git_failure(
                b"fatal: detected dubious ownership in repository at '/secret/path'; add safe.directory",
                Some(128),
            ),
            GitTopologyError::UntrustedRepositoryRefusedByGit
        );
        assert_eq!(
            classify_git_failure(b"error: unknown option `no-lazy-fetch'", Some(129)),
            GitTopologyError::UnsupportedGitCapability
        );
    }

    #[test]
    fn worktree_porcelain_parser_requires_absolute_paths_and_valid_head() {
        #[cfg(windows)]
        let output = b"worktree C:\\repo\0HEAD 0123456789012345678901234567890123456789\0branch refs/heads/main\0\0";
        #[cfg(not(windows))]
        let output = b"worktree /repo\0HEAD 0123456789012345678901234567890123456789\0branch refs/heads/main\0\0";
        assert_eq!(validate_worktree_porcelain_z(output), Ok(1));
        assert!(validate_worktree_porcelain_z(b"worktree relative\0\0").is_err());
        assert!(validate_worktree_porcelain_z(b"worktree /repo\0HEAD nope\0\0").is_err());
    }

    #[test]
    fn worktree_porcelain_parser_rejects_a_path_repeated_across_records() {
        #[cfg(windows)]
        let twice = b"worktree C:\\repo\0detached\0\0worktree C:\\repo\0detached\0\0".as_slice();
        #[cfg(not(windows))]
        let twice = b"worktree /repo\0detached\0\0worktree /repo\0detached\0\0".as_slice();
        assert_eq!(
            validate_worktree_porcelain_z(twice),
            Err(GitTopologyError::GitOutputMalformed {
                field: "repeated worktree path across records",
            })
        );

        #[cfg(windows)]
        let distinct = b"worktree C:\\a\0detached\0\0worktree C:\\b\0detached\0\0".as_slice();
        #[cfg(not(windows))]
        let distinct = b"worktree /a\0detached\0\0worktree /b\0detached\0\0".as_slice();
        assert_eq!(validate_worktree_porcelain_z(distinct), Ok(2));
    }
}
