#![forbid(unsafe_code)]

//! S2-D012: bounded, read-only classification of security-sensitive local
//! Git configuration through `git_topology::observe_security_sensitive_config`.
//!
//! Every fixture here is a fresh, disposable `git init` repository with fake
//! credentials only. This suite proves classification/counting behavior
//! against real Git config files; it does not attempt a `safe.directory`
//! ownership trust-refusal fixture, since that requires a separately
//! available platform fixture (a config observation reusing the already
//! S2-AUTH-014-qualified adapter and its `classify_git_failure` mapping,
//! covered there) rather than a fabricated PASS here.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::atomic::{AtomicUsize, Ordering};

use wepld_core::git_topology::{
    self, GitTopologyError, SecuritySensitiveConfigTopology, discover_system_git,
};

static TEMP_COUNTER: AtomicUsize = AtomicUsize::new(0);

fn temp_root(label: &str) -> PathBuf {
    let counter = TEMP_COUNTER.fetch_add(1, Ordering::Relaxed);
    let mut root = PathBuf::from(env!("CARGO_TARGET_TMPDIR"));
    root.push(format!(
        "wepld-sec-config-{label}-{}-{counter}",
        std::process::id()
    ));
    fs::create_dir_all(&root).expect("temporary root must be creatable");
    root
}

fn init_repo(label: &str) -> PathBuf {
    let repo = temp_root(label);
    let status = Command::new("git")
        .args(["init", "--quiet"])
        .current_dir(&repo)
        .status()
        .expect("spawn git init");
    assert!(status.success(), "git init must succeed");
    repo
}

fn set_config(repo: &Path, args: &[&str]) {
    let mut command = Command::new("git");
    command.arg("-C").arg(repo).arg("config");
    command.args(args);
    let status = command.status().expect("spawn git config");
    assert!(status.success(), "git config {args:?} must succeed");
}

fn observe(repo: &Path) -> Result<SecuritySensitiveConfigTopology, GitTopologyError> {
    let evidence = temp_root("evidence");
    let git = discover_system_git(repo, &evidence).expect("system Git must qualify on CI");
    git_topology::observe_security_sensitive_config(&git, repo)
}

#[test]
fn clean_local_git_config_yields_zero_counts() {
    let repo = init_repo("clean");
    let topology = observe(&repo).expect("clean repo observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 0);
    assert_eq!(topology.redacted_remote_url_count, 0);
}

#[test]
fn credential_bearing_remote_url_is_counted_and_never_echoed() {
    let repo = init_repo("cred-url");
    set_config(
        &repo,
        &[
            "remote.origin.url",
            "https://alice:supersecret@example.test/repo.git",
        ],
    );
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 1);
    assert_eq!(topology.redacted_remote_url_count, 1);
    let rendered = format!("{topology:?}");
    assert!(
        !rendered.contains("supersecret"),
        "raw secret leaked into Debug output"
    );
    assert!(
        !rendered.contains("alice"),
        "raw userinfo leaked into Debug output"
    );
}

#[test]
fn pushurl_credential_is_counted_independently_of_a_clean_fetch_url() {
    let repo = init_repo("pushurl");
    set_config(&repo, &["remote.origin.url", "git@example.test:repo.git"]);
    set_config(
        &repo,
        &[
            "remote.origin.pushurl",
            "https://ghp_deadbeefdeadbeefdeadbeef@example.test/repo.git",
        ],
    );
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 1);
    assert_eq!(topology.redacted_remote_url_count, 1);
}

#[test]
fn ssh_git_at_file_and_local_path_remote_urls_are_not_flagged_credential_bearing() {
    let repo = init_repo("non-http-forms");
    set_config(
        &repo,
        &["remote.origin.url", "ssh://user@example.test/repo.git"],
    );
    set_config(&repo, &["remote.upstream.url", "git@example.test:repo.git"]);
    set_config(&repo, &["remote.mirror.url", "file:///tmp/mirror.git"]);
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 0);
    assert_eq!(topology.redacted_remote_url_count, 0);
}

#[test]
fn presence_only_classes_are_each_counted_credential_bearing() {
    let repo = init_repo("presence-only");
    set_config(&repo, &["credential.helper", "store"]);
    set_config(
        &repo,
        &[
            "--add",
            "http.extraHeader",
            "Authorization: Basic Zm9vOmJhcg==",
        ],
    );
    set_config(
        &repo,
        &[
            "url.https://fake.example/.insteadOf",
            "https://example.test/",
        ],
    );
    set_config(
        &repo,
        &[
            "url.https://fake.example/.pushInsteadOf",
            "https://example.test/",
        ],
    );
    set_config(&repo, &["core.sshCommand", "ssh -i /tmp/id_rsa"]);
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 5);
    assert_eq!(
        topology.redacted_remote_url_count, 0,
        "none of these classes are the remote-url family"
    );
}

#[test]
fn http_proxy_is_credential_bearing_only_when_userinfo_is_present() {
    let repo = init_repo("proxy");
    set_config(
        &repo,
        &["http.proxy", "http://plainproxy.example.test:8080"],
    );
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 0);

    set_config(
        &repo,
        &[
            "http.proxy",
            "http://proxyuser:proxypass@proxy.example.test:8080",
        ],
    );
    let topology = observe(&repo).expect("observation must succeed");
    assert_eq!(topology.credential_bearing_entry_count, 1);
    assert_eq!(
        topology.redacted_remote_url_count, 0,
        "a credential-bearing proxy is not a remote URL"
    );
}

#[test]
fn multiple_sensitive_classes_produce_deterministic_aggregate_counts() {
    let repo = init_repo("aggregate");
    set_config(
        &repo,
        &["remote.origin.url", "https://token@example.test/a.git"],
    );
    set_config(
        &repo,
        &["remote.origin.pushurl", "https://token@example.test/b.git"],
    );
    set_config(&repo, &["credential.helper", "store"]);
    set_config(&repo, &["core.sshCommand", "ssh -F /tmp/config"]);

    let first = observe(&repo).expect("first observation must succeed");
    let second = observe(&repo).expect("second observation must succeed");
    assert_eq!(
        first, second,
        "observation over an unchanged repo is deterministic"
    );
    assert_eq!(first.credential_bearing_entry_count, 4);
    assert_eq!(first.redacted_remote_url_count, 2);
}

#[test]
fn a_repository_local_include_directive_is_not_followed() {
    // A malicious repository could try to smuggle a credential-bearing entry
    // through `[include]`/`includeIf`, or through a huge/irrelevant file, by
    // pointing the local config at another file. `--no-includes` must make
    // this observation blind to it entirely: the aggregate count must match
    // exactly what the repository's own `.git/config` states directly, never
    // what an included file adds.
    let repo = init_repo("include-defense");
    let outside_root = temp_root("include-defense-outside");
    let included = outside_root.join("outside.gitconfig");
    fs::write(
        &included,
        "[remote \"injected\"]\n\turl = https://attacker:pwned@example.test/repo.git\n",
    )
    .expect("outside include file must be writable");

    let config_path = repo.join(".git").join("config");
    let mut config = fs::read_to_string(&config_path).expect("git config file must be readable");
    config.push_str(&format!(
        "[include]\n\tpath = {}\n",
        included.to_string_lossy().replace('\\', "/")
    ));
    fs::write(&config_path, config).expect("git config file must be writable");

    // Sanity: with includes followed, Git itself would see the injected URL.
    let included_visible = Command::new("git")
        .arg("-C")
        .arg(&repo)
        .args(["config", "--get", "remote.injected.url"])
        .output()
        .expect("spawn git config --get");
    assert!(
        included_visible.status.success(),
        "fixture sanity check: Git itself must see the included remote"
    );

    let topology = observe(&repo).expect("observation must succeed despite the include directive");
    assert_eq!(
        topology.credential_bearing_entry_count, 0,
        "an included file's credential-bearing entry must not be observed"
    );
    assert_eq!(topology.redacted_remote_url_count, 0);
}

#[test]
fn observation_does_not_mutate_the_repository() {
    let repo = init_repo("no-mutation");
    set_config(
        &repo,
        &[
            "remote.origin.url",
            "https://alice:secret@example.test/repo.git",
        ],
    );
    let config_path = repo.join(".git").join("config");
    let before = fs::read(&config_path).expect("config must be readable");

    let _ = observe(&repo).expect("observation must succeed");

    let after = fs::read(&config_path).expect("config must remain readable");
    assert_eq!(before, after, "observation must never mutate .git/config");
}

#[test]
fn a_relative_locator_is_rejected_before_any_git_process_starts() {
    let repo = init_repo("relative-locator");
    let evidence = temp_root("relative-locator-evidence");
    let git = discover_system_git(&repo, &evidence).expect("system Git must qualify on CI");
    assert_eq!(
        git_topology::observe_security_sensitive_config(&git, Path::new(".")),
        Err(GitTopologyError::NonAbsoluteLocator)
    );
}

#[test]
fn cancellation_terminates_the_spawned_git_and_returns_a_stable_error() {
    let repo = init_repo("cancel");
    let evidence = temp_root("cancel-evidence");
    let git = discover_system_git(&repo, &evidence).expect("system Git must qualify on CI");
    let result = git_topology::observe_security_sensitive_config_with_cancel(&git, &repo, &|| true);
    assert_eq!(result, Err(GitTopologyError::GitCancelled));
}
