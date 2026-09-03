#![forbid(unsafe_code)]

//! S2 Git-topology qualification suite for the v45-authorized product tranche.
//!
//! This suite exercises the actual current checkout through the closed adapter,
//! executable-spoof refusal, cancellation/reaping, machine-output parsing, and
//! repository non-mutation. It does not pretend to prove unavailable platform
//! evidence: ownership-based `safe.directory` refusal, linked-worktree,
//! submodule/superproject, bare-repository, and hard-timeout fixtures require
//! separately available platform fixtures and remain explicit qualification
//! obligations rather than fabricated PASS results.

use std::fs;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicUsize, Ordering};

use wepld_contracts::{LinkedWorktreeState, Observation, RepositoryTrustState, VcsKind};
use wepld_core::{
    GitTopologyError, GitVersionEvidence, discover_system_git, observe_git_topology,
    observe_git_topology_with_cancel, qualify_git_executable, validate_worktree_porcelain_z,
};

static TEMP_COUNTER: AtomicUsize = AtomicUsize::new(0);

fn repository_root() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .ancestors()
        .find(|candidate| candidate.join("Cargo.lock").is_file() && candidate.join(".git").exists())
        .expect("integration test must run from the WePLD Git checkout")
        .to_path_buf()
}

fn temp_root(label: &str) -> PathBuf {
    let counter = TEMP_COUNTER.fetch_add(1, Ordering::Relaxed);
    let mut root = PathBuf::from(env!("CARGO_TARGET_TMPDIR"));
    root.push(format!("wepld-git-topology-{label}-{}-{counter}", std::process::id()));
    fs::create_dir_all(&root).expect("temporary qualification root must be creatable");
    root
}

fn read_if_file(path: &Path) -> Option<Vec<u8>> {
    path.is_file().then(|| fs::read(path).expect("qualification snapshot must be readable"))
}

#[test]
fn current_checkout_is_observed_through_the_closed_read_only_adapter() {
    let root = repository_root();
    let evidence_root = temp_root("evidence");
    let cargo_lock_before = fs::read(root.join("Cargo.lock")).expect("Cargo.lock must be readable");
    let index_before = read_if_file(&root.join(".git").join("index"));

    let git = discover_system_git(&root, &evidence_root).expect("system Git must qualify on CI");
    assert!(git.lexical_path.is_absolute());
    assert!(git.resolved_path.is_absolute());
    assert!(git.file_len > 0);
    assert_eq!(
        git.version_evidence,
        GitVersionEvidence::NotObservedUnderCurrentAuthority
    );

    let topology = observe_git_topology(&git, &root).expect("current checkout topology must resolve");
    assert_eq!(topology.vcs_kind, VcsKind::Git);
    assert_eq!(topology.trust_state, RepositoryTrustState::Trusted);
    assert!(matches!(topology.worktree_root, Observation::Available { .. }));
    assert!(matches!(topology.absolute_git_dir, Observation::Available { .. }));
    assert!(matches!(topology.git_common_dir, Observation::Available { .. }));
    assert_eq!(topology.is_bare, Observation::Available { value: false });
    assert_eq!(
        topology.is_inside_worktree,
        Observation::Available { value: true }
    );
    assert_eq!(topology.linked_worktree_state, LinkedWorktreeState::Known);

    assert_eq!(
        fs::read(root.join("Cargo.lock")).expect("Cargo.lock must remain readable"),
        cargo_lock_before,
        "topology observation must not mutate tracked project bytes"
    );
    assert_eq!(
        read_if_file(&root.join(".git").join("index")),
        index_before,
        "topology observation must not mutate the Git index"
    );
}

#[test]
fn project_local_git_candidate_is_rejected_without_fallback() {
    let project = temp_root("spoof-project");
    let evidence = temp_root("spoof-evidence");
    let executable = project.join(if cfg!(windows) { "git.exe" } else { "git" });
    fs::write(&executable, b"not a real git executable\n").expect("fake executable must be writable");

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt as _;
        let mut permissions = fs::metadata(&executable)
            .expect("fake executable metadata")
            .permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&executable, permissions).expect("fake executable mode");
    }

    assert_eq!(
        qualify_git_executable(&executable, &project, &evidence),
        Err(GitTopologyError::ExecutableInsideOpenedProject)
    );
}

#[test]
fn cancellation_terminates_the_spawned_git_and_returns_a_stable_error() {
    let root = repository_root();
    let evidence_root = temp_root("cancel-evidence");
    let git = discover_system_git(&root, &evidence_root).expect("system Git must qualify on CI");

    let result = observe_git_topology_with_cancel(&git, &root, &|| true);
    assert_eq!(result, Err(GitTopologyError::GitCancelled));
}

#[test]
fn worktree_porcelain_z_accepts_sha1_and_sha256_object_ids() {
    #[cfg(windows)]
    let root = b"C:\\repo".as_slice();
    #[cfg(not(windows))]
    let root = b"/repo".as_slice();

    let mut sha1 = Vec::new();
    sha1.extend_from_slice(b"worktree ");
    sha1.extend_from_slice(root);
    sha1.extend_from_slice(b"\0HEAD 0123456789012345678901234567890123456789\0detached\0\0");
    assert_eq!(validate_worktree_porcelain_z(&sha1), Ok(1));

    let mut sha256 = Vec::new();
    sha256.extend_from_slice(b"worktree ");
    sha256.extend_from_slice(root);
    sha256.extend_from_slice(
        b"\0HEAD 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\0branch refs/heads/main\0\0",
    );
    assert_eq!(validate_worktree_porcelain_z(&sha256), Ok(1));
}

#[test]
fn malformed_worktree_machine_output_fails_closed() {
    assert!(validate_worktree_porcelain_z(b"").is_err());
    assert!(validate_worktree_porcelain_z(b"worktree relative\0\0").is_err());
    assert!(validate_worktree_porcelain_z(b"HEAD 0123456789012345678901234567890123456789\0\0").is_err());
    assert!(validate_worktree_porcelain_z(b"worktree /repo\0HEAD bad\0\0").is_err());
}
