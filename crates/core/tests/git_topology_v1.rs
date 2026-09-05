#![forbid(unsafe_code)]

//! S2 Git-topology qualification suite for the v45-authorized product tranche.
//!
//! This suite exercises the actual current checkout through the closed adapter,
//! executable-spoof refusal, cancellation/reaping, machine-output parsing,
//! repository non-mutation, a real linked worktree (S2-I006), and a real
//! submodule/superproject (S2-I007). It does not pretend to prove unavailable
//! platform evidence: ownership-based `safe.directory` refusal,
//! bare-repository, and hard-timeout fixtures require separately available
//! platform fixtures and remain explicit qualification obligations rather
//! than fabricated PASS results.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::atomic::{AtomicUsize, Ordering};

use wepld_contracts::{
    LinkedWorktreeState, Observation, OptionalObservation, RepositoryTrustState, VcsKind,
};
use wepld_core::git_topology::{
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
    root.push(format!(
        "wepld-git-topology-{label}-{}-{counter}",
        std::process::id()
    ));
    fs::create_dir_all(&root).expect("temporary qualification root must be creatable");
    root
}

fn read_if_file(path: &Path) -> Option<Vec<u8>> {
    path.is_file()
        .then(|| fs::read(path).expect("qualification snapshot must be readable"))
}

fn git(repo: &Path, args: &[&str]) {
    let status = Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .status()
        .expect("spawn git");
    assert!(status.success(), "git {args:?} in {repo:?} must succeed");
}

/// Runs `git` in `repo` and returns trimmed stdout, used as an independent
/// oracle (a second, separate Git invocation) for exact-path assertions,
/// rather than trusting the adapter under test to grade its own output.
fn git_output(repo: &Path, args: &[&str]) -> String {
    let output = Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .output()
        .expect("spawn git");
    assert!(
        output.status.success(),
        "git {args:?} in {repo:?} must succeed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout)
        .expect("git output must be UTF-8 in this fixture")
        .trim()
        .to_owned()
}

fn init_committed_repo(label: &str) -> PathBuf {
    let repo = temp_root(label);
    git(&repo, &["init", "--quiet"]);
    git(
        &repo,
        &[
            "-c",
            "user.email=wepld-test@example.test",
            "-c",
            "user.name=wepld-test",
            "commit",
            "--allow-empty",
            "--quiet",
            "-m",
            "init",
        ],
    );
    repo
}

#[test]
fn current_checkout_is_observed_through_the_closed_read_only_adapter() {
    let root = repository_root();
    let evidence_root = temp_root("evidence");
    let cargo_lock_before = fs::read(root.join("Cargo.lock")).expect("Cargo.lock must be readable");
    let index_before = read_if_file(&root.join(".git").join("index"));

    let git = discover_system_git(&root, &evidence_root).expect("system Git must qualify on CI");
    assert!(git.lexical_path().is_absolute());
    assert!(git.resolved_path().is_absolute());
    assert!(git.file_len() > 0);
    assert_eq!(
        git.version_evidence(),
        GitVersionEvidence::NotObservedUnderCurrentAuthority
    );

    let topology =
        observe_git_topology(&git, &root).expect("current checkout topology must resolve");
    assert_eq!(topology.vcs_kind, VcsKind::Git);
    assert_eq!(topology.trust_state, RepositoryTrustState::Trusted);
    assert!(matches!(
        topology.worktree_root,
        Observation::Available { .. }
    ));
    assert!(matches!(
        topology.absolute_git_dir,
        Observation::Available { .. }
    ));
    assert!(matches!(
        topology.git_common_dir,
        Observation::Available { .. }
    ));
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
    fs::write(&executable, b"not a real git executable\n")
        .expect("fake executable must be writable");

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
fn a_relative_locator_is_rejected_before_any_git_process_starts() {
    let root = repository_root();
    let evidence_root = temp_root("relative-locator-evidence");
    let git = discover_system_git(&root, &evidence_root).expect("system Git must qualify on CI");

    // `.` would otherwise resolve from the Git executable directory, not the
    // caller working directory, because the child current directory is pinned.
    assert_eq!(
        observe_git_topology(&git, Path::new(".")),
        Err(GitTopologyError::NonAbsoluteLocator)
    );
    assert_eq!(
        observe_git_topology_with_cancel(&git, Path::new("relative/sub"), &|| false),
        Err(GitTopologyError::NonAbsoluteLocator)
    );
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
    assert!(
        validate_worktree_porcelain_z(b"HEAD 0123456789012345678901234567890123456789\0\0")
            .is_err()
    );
    assert!(validate_worktree_porcelain_z(b"worktree /repo\0HEAD bad\0\0").is_err());
    assert!(
        validate_worktree_porcelain_z(b"worktree /repo\0detached\0\0worktree /repo\0detached\0\0")
            .is_err(),
        "a worktree path repeated across records is malformed"
    );
}

/// S2-I006 adversarial fixture: a real linked worktree, not the current
/// checkout. Proves `worktree_root` (the linked worktree) is distinct from
/// `git_common_dir` (still the main repository's shared `.git`), and that
/// `absolute_git_dir` (this worktree's own private gitdir under
/// `.git/worktrees/<name>`) differs from `git_common_dir` too.
#[test]
fn linked_worktree_observes_distinct_root_and_shared_common_dir() {
    let evidence_root = temp_root("evidence");
    let main_repo = init_committed_repo("main-repo");

    let worktrees_parent = temp_root("linked-worktree-parent");
    let linked_worktree = worktrees_parent.join("linked");
    git(
        &main_repo,
        &[
            "worktree",
            "add",
            "--quiet",
            linked_worktree
                .to_str()
                .expect("temp worktree path must be valid UTF-8"),
            "-b",
            "feature",
        ],
    );

    let git_exe =
        discover_system_git(&linked_worktree, &evidence_root).expect("system Git must qualify");
    let topology = observe_git_topology(&git_exe, &linked_worktree)
        .expect("linked worktree topology must resolve");

    assert_eq!(topology.trust_state, RepositoryTrustState::Trusted);
    assert_eq!(topology.is_bare, Observation::Available { value: false });
    assert_eq!(topology.linked_worktree_state, LinkedWorktreeState::Known);

    let worktree_root = match &topology.worktree_root {
        Observation::Available { value } => value.safe_display().as_str().to_owned(),
        other => panic!("expected an available worktree_root, got {other:?}"),
    };
    let common_dir = match &topology.git_common_dir {
        Observation::Available { value } => value.safe_display().as_str().to_owned(),
        other => panic!("expected an available git_common_dir, got {other:?}"),
    };
    let own_git_dir = match &topology.absolute_git_dir {
        Observation::Available { value } => value.safe_display().as_str().to_owned(),
        other => panic!("expected an available absolute_git_dir, got {other:?}"),
    };

    // Independent ground truth: a second, separate `git` invocation from
    // inside the linked worktree, not the adapter under test grading its
    // own output. Exact canonicalized-path equality, not substring matching.
    let expected_own_git_dir = PathBuf::from(git_output(
        &linked_worktree,
        &["rev-parse", "--absolute-git-dir"],
    ));
    let expected_common_dir_raw = git_output(&linked_worktree, &["rev-parse", "--git-common-dir"]);
    let expected_common_dir = if Path::new(&expected_common_dir_raw).is_absolute() {
        PathBuf::from(expected_common_dir_raw)
    } else {
        PathBuf::from(&expected_own_git_dir)
            .parent()
            .expect("absolute-git-dir must have a parent")
            .join(&expected_common_dir_raw)
    };

    assert_eq!(
        PathBuf::from(&worktree_root)
            .canonicalize()
            .expect("observed worktree_root must canonicalize"),
        linked_worktree
            .canonicalize()
            .expect("the linked worktree path must canonicalize"),
        "worktree_root must be exactly the linked worktree, not the main checkout: {worktree_root}"
    );
    assert_eq!(
        PathBuf::from(&common_dir)
            .canonicalize()
            .expect("observed git_common_dir must canonicalize"),
        main_repo
            .join(".git")
            .canonicalize()
            .expect("the main repository .git directory must canonicalize"),
        "git_common_dir must be exactly the main repository's shared .git: {common_dir}"
    );
    assert_eq!(
        PathBuf::from(&common_dir)
            .canonicalize()
            .expect("observed git_common_dir must canonicalize"),
        expected_common_dir
            .canonicalize()
            .expect("git rev-parse --git-common-dir must canonicalize"),
        "git_common_dir must match git's own --git-common-dir for the linked worktree"
    );
    assert_eq!(
        PathBuf::from(&own_git_dir)
            .canonicalize()
            .expect("observed absolute_git_dir must canonicalize"),
        expected_own_git_dir
            .canonicalize()
            .expect("git rev-parse --absolute-git-dir must canonicalize"),
        "absolute_git_dir must match git's own --absolute-git-dir for the linked worktree"
    );
    assert_ne!(
        own_git_dir, common_dir,
        "a linked worktree's own gitdir must differ from the shared common dir"
    );
}

/// S2-I007 adversarial fixture: a real submodule, not a synthetic value.
/// Proves `superproject_worktree` is populated with the superproject's root
/// when the observation locator is the submodule's own worktree.
#[test]
fn submodule_worktree_observes_its_superproject() {
    let evidence_root = temp_root("evidence");
    let submodule_source = init_committed_repo("submodule-source");
    let superproject = init_committed_repo("superproject");

    git(
        &superproject,
        &[
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "--quiet",
            "add",
            submodule_source
                .to_str()
                .expect("temp submodule source path must be valid UTF-8"),
            "sub",
        ],
    );

    let submodule_worktree = superproject.join("sub");
    let git_exe =
        discover_system_git(&submodule_worktree, &evidence_root).expect("system Git must qualify");
    let topology = observe_git_topology(&git_exe, &submodule_worktree)
        .expect("submodule topology must resolve");

    // Independent ground truth: git's own dedicated command for exactly this
    // relationship, run separately from the adapter under test.
    let expected_superproject_root = PathBuf::from(git_output(
        &submodule_worktree,
        &["rev-parse", "--show-superproject-working-tree"],
    ));
    assert!(
        !expected_superproject_root.as_os_str().is_empty(),
        "git rev-parse --show-superproject-working-tree must report the superproject from inside the submodule"
    );

    match &topology.superproject_worktree {
        OptionalObservation::Value { value } => {
            let superproject_root = value.safe_display().as_str().to_owned();
            assert_eq!(
                PathBuf::from(&superproject_root)
                    .canonicalize()
                    .expect("observed superproject_worktree must canonicalize"),
                superproject
                    .canonicalize()
                    .expect("the superproject path must canonicalize"),
                "superproject_worktree must be exactly the superproject root: {superproject_root}"
            );
            assert_eq!(
                PathBuf::from(&superproject_root)
                    .canonicalize()
                    .expect("observed superproject_worktree must canonicalize"),
                expected_superproject_root
                    .canonicalize()
                    .expect("git rev-parse --show-superproject-working-tree must canonicalize"),
                "superproject_worktree must match git's own --show-superproject-working-tree"
            );
        }
        other => panic!(
            "expected superproject_worktree to be populated from inside a submodule, got {other:?}"
        ),
    }
}
