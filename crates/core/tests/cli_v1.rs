#![forbid(unsafe_code)]

//! S2-AUTH-015 command-plane parsing, projection, and negative oracles.

use std::path::PathBuf;

use wepld_contracts::{
    EvidenceStatus, MachinePath, ProjectId, RepositoryTrustState, StoreAuthenticity, UnixMillis,
};
use wepld_core::cli::{
    self, Command, CommandOutcome, EvidenceSummary, ExitClass, OutputMode, ParseError,
    RepositorySummary,
};
use wepld_core::doctor::{
    self, DescriptorObservation, DoctorInputs, IdentityObservation, SecuritySensitiveObservation,
};

fn parse(args: &[&str]) -> Result<cli::Invocation, ParseError> {
    cli::parse(args)
}

#[test]
fn parses_each_command_and_flag_combination() {
    let open = parse(&["open", "."]).expect("open parses");
    assert_eq!(open.command, Command::Open);
    assert_eq!(open.open_path.as_deref(), Some("."));
    assert_eq!(open.output, OutputMode::Human);
    assert!(!open.no_input);

    let doctor = parse(&["doctor", "--json"]).expect("doctor parses");
    assert_eq!(doctor.command, Command::Doctor);
    assert_eq!(doctor.output, OutputMode::Json);

    let status = parse(&["status", "--json", "--no-input"]).expect("status parses");
    assert_eq!(status.command, Command::Status);
    assert!(status.no_input);
    assert_eq!(status.output, OutputMode::Json);
}

#[test]
fn missing_command_is_a_usage_error() {
    assert_eq!(parse(&[]), Err(ParseError::MissingCommand));
}

#[test]
fn unknown_command_is_an_error_with_a_suggestion_never_a_prompt() {
    match parse(&["opne"]) {
        Err(ParseError::UnknownCommand { token, suggestion }) => {
            assert_eq!(token, "opne");
            assert_eq!(suggestion, Some("open"));
        }
        other => panic!("expected unknown-command error, got {other:?}"),
    }
    match parse(&["doctro"]) {
        Err(ParseError::UnknownCommand { suggestion, .. }) => {
            assert_eq!(suggestion, Some("doctor"));
        }
        other => panic!("expected unknown-command error, got {other:?}"),
    }
    // A free-form phrase is still an error, not a model prompt.
    assert!(matches!(
        parse(&["please", "fix", "my", "build"]),
        Err(ParseError::UnknownCommand { .. })
    ));
}

#[test]
fn open_requires_exactly_one_nonempty_path() {
    assert_eq!(parse(&["open"]), Err(ParseError::OpenPathMissing));
    assert_eq!(parse(&["open", ""]), Err(ParseError::OpenPathEmpty));
    match parse(&["open", "a", "b"]) {
        Err(ParseError::UnexpectedArgument { argument }) => assert_eq!(argument, "b"),
        other => panic!("expected unexpected-argument error, got {other:?}"),
    }
}

#[test]
fn unknown_flag_and_stray_positional_are_usage_errors() {
    match parse(&["doctor", "--wat"]) {
        Err(ParseError::UnknownFlag { flag }) => assert_eq!(flag, "--wat"),
        other => panic!("expected unknown-flag error, got {other:?}"),
    }
    match parse(&["status", "extra"]) {
        Err(ParseError::UnexpectedArgument { argument }) => assert_eq!(argument, "extra"),
        other => panic!("expected unexpected-argument error, got {other:?}"),
    }
}

#[test]
fn exit_class_codes_are_frozen() {
    assert_eq!(ExitClass::Success.code(), 0);
    assert_eq!(ExitClass::UnexpectedInternal.code(), 1);
    assert_eq!(ExitClass::UsageInput.code(), 2);
    assert_eq!(ExitClass::ProjectResolutionIdentity.code(), 3);
    assert_eq!(ExitClass::EvidenceStoreIntegrity.code(), 4);
    assert_eq!(ExitClass::DoctorBlockingFindings.code(), 5);
    assert_eq!(ExitClass::RequiredCapabilityUnavailable.code(), 6);
}

fn open_outcome(evidence: EvidenceSummary) -> CommandOutcome {
    CommandOutcome::Open {
        project_id: Some("p_demo".to_owned()),
        locator_display: "/home/dev/project".to_owned(),
        repository: RepositorySummary::Git {
            trust_state: RepositoryTrustState::Trusted,
        },
        evidence,
    }
}

#[test]
fn open_exit_class_reflects_evidence_state() {
    assert_eq!(
        open_outcome(EvidenceSummary::Present {
            status: EvidenceStatus::Complete,
            authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
        })
        .exit_class(),
        ExitClass::Success
    );
    assert_eq!(
        open_outcome(EvidenceSummary::Present {
            status: EvidenceStatus::Corrupt,
            authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
        })
        .exit_class(),
        ExitClass::EvidenceStoreIntegrity
    );
    assert_eq!(
        open_outcome(EvidenceSummary::Unavailable).exit_class(),
        ExitClass::RequiredCapabilityUnavailable
    );
}

fn at() -> UnixMillis {
    UnixMillis::new(1_700_000_000_000)
}

fn doctor_inputs(identity: IdentityObservation) -> DoctorInputs {
    DoctorInputs {
        project_id: ProjectId::try_from("p_demo").expect("id"),
        selected_generation_id: None,
        identity,
        repository: None,
        evidence_store: None,
        descriptors: DescriptorObservation {
            toolchains: Vec::new(),
            package_managers: Vec::new(),
            lockfile_marker_count: 0,
            package_manager_ambiguous: false,
            descriptor_budget_rejected: false,
        },
        security_sensitive: SecuritySensitiveObservation::default(),
    }
}

#[test]
fn doctor_outcome_exit_class_tracks_blocking_findings() {
    let blocking =
        doctor::evaluate(&doctor_inputs(IdentityObservation::Unavailable), at()).expect("evaluate");
    assert_eq!(
        CommandOutcome::Doctor { report: blocking }.exit_class(),
        ExitClass::DoctorBlockingFindings
    );
}

#[test]
fn human_and_json_come_from_one_model_and_are_deterministic() {
    let outcome = open_outcome(EvidenceSummary::Present {
        status: EvidenceStatus::Complete,
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    });

    let human_a = cli::render(&outcome, OutputMode::Human);
    let human_b = cli::render(&outcome, OutputMode::Human);
    assert_eq!(human_a, human_b);

    let json_a = cli::render(&outcome, OutputMode::Json);
    let json_b = cli::render(&outcome, OutputMode::Json);
    assert_eq!(json_a, json_b);

    assert!(json_a.starts_with('{'));
    assert!(json_a.ends_with("}\n"));
    assert!(json_a.contains("\"schema_version\":1"));
    assert!(json_a.contains("\"contract\":\"wepld.doctor_cli.v1\""));
    assert!(json_a.contains("\"exit_class\":\"success\""));
    // JSON carries no ANSI/prose-only formatting.
    assert!(!json_a.contains('\u{1b}'));
}

#[test]
fn terminal_control_sequences_never_reach_human_or_json_output() {
    let hostile = "proj\u{1b}[31mHACK\u{1b}[0m\u{0}name";
    let outcome = CommandOutcome::Open {
        project_id: None,
        locator_display: hostile.to_owned(),
        repository: RepositorySummary::NonGit,
        evidence: EvidenceSummary::Unavailable,
    };

    let human = cli::render(&outcome, OutputMode::Human);
    let json = cli::render(&outcome, OutputMode::Json);

    for rendered in [&human, &json] {
        assert!(!rendered.contains('\u{1b}'), "raw ESC leaked into output");
        assert!(!rendered.contains('\u{0}'), "raw NUL leaked into output");
    }
    assert!(human.contains("\\u{1b}"));
}

#[test]
fn safe_display_path_redacts_credential_bearing_remote_urls() {
    let machine_path =
        MachinePath::utf8("https://alice:s3cr3t@example.com/repo.git?token=abc").expect("path");
    let display = doctor::safe_display_path(&machine_path);
    assert!(!display.contains("s3cr3t"));
    assert!(!display.contains("alice:s3cr3t"));
    assert!(display.contains("<redacted>"));
}

#[test]
fn failure_outcome_preserves_its_declared_exit_class() {
    let outcome = CommandOutcome::Failure {
        command: Command::Open,
        class: ExitClass::ProjectResolutionIdentity,
        reason: "project_resolution_failed".to_owned(),
    };
    assert_eq!(outcome.exit_class(), ExitClass::ProjectResolutionIdentity);
    let json = cli::render(&outcome, OutputMode::Json);
    assert!(json.contains("\"outcome\":\"error\""));
    assert!(json.contains("\"exit_class\":\"project_resolution_or_identity_error\""));
}

/// S2-S013 / S2-S014 negative oracle: the command-plane module is pure — no
/// filesystem, process, or network effect lives here.
#[test]
fn cli_module_source_contains_no_effect_surface() {
    let source =
        std::fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/cli.rs"))
            .expect("cli.rs readable");
    for forbidden in [
        "std::process",
        "Command::new",
        "std::net",
        "TcpStream",
        "std::fs",
        "std::env",
    ] {
        assert!(
            !source.contains(forbidden),
            "cli.rs must not reference `{forbidden}`"
        );
    }
}

// ==========================================================================
// Orchestration integration tests — spawn the built `wepld` binary against
// hermetic fixture directories. The store is redirected to a per-test temp
// dir via XDG_STATE_HOME / HOME / LOCALAPPDATA so nothing touches the real
// user profile and no test depends on another.
// ==========================================================================

mod orchestration {
    use std::collections::BTreeMap;
    use std::fs;
    use std::path::{Path, PathBuf};
    use std::process::Command;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn scratch(tag: &str) -> PathBuf {
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("clock")
            .as_nanos();
        let dir = std::env::temp_dir().join(format!("wepld-cli-it-{tag}-{nanos}"));
        fs::create_dir_all(&dir).expect("scratch dir");
        dir
    }

    struct Run {
        code: i32,
        stdout: String,
        stderr: String,
    }

    fn run_wepld(args: &[&str], cwd: &Path, store_home: &Path) -> Run {
        let output = Command::new(env!("CARGO_BIN_EXE_wepld"))
            .args(args)
            .current_dir(cwd)
            .env("XDG_STATE_HOME", store_home)
            .env("HOME", store_home)
            .env("LOCALAPPDATA", store_home)
            .env_remove("XDG_CONFIG_HOME")
            .output()
            .expect("spawn wepld");
        Run {
            code: output.status.code().unwrap_or(-1),
            stdout: String::from_utf8_lossy(&output.stdout).into_owned(),
            stderr: String::from_utf8_lossy(&output.stderr).into_owned(),
        }
    }

    /// Recursive content snapshot: relative path -> bytes, for every regular file.
    fn snapshot(root: &Path) -> BTreeMap<String, Vec<u8>> {
        fn walk(base: &Path, dir: &Path, out: &mut BTreeMap<String, Vec<u8>>) {
            let Ok(entries) = fs::read_dir(dir) else {
                return;
            };
            for entry in entries.flatten() {
                let path = entry.path();
                let meta = match entry.metadata() {
                    Ok(m) => m,
                    Err(_) => continue,
                };
                if meta.is_dir() {
                    walk(base, &path, out);
                } else if meta.is_file() {
                    let rel = path
                        .strip_prefix(base)
                        .unwrap_or(&path)
                        .to_string_lossy()
                        .replace('\\', "/");
                    out.insert(rel, fs::read(&path).unwrap_or_default());
                }
            }
        }
        let mut out = BTreeMap::new();
        walk(root, root, &mut out);
        out
    }

    fn project_id_field(json: &str) -> Option<String> {
        let key = "\"project_id\":\"";
        let start = json.find(key)? + key.len();
        let rest = &json[start..];
        let end = rest.find('"')?;
        Some(rest[..end].to_owned())
    }

    #[test]
    fn open_on_a_plain_directory_succeeds_and_reuses_one_identity() {
        let store = scratch("open-idem-store");
        let project = scratch("open-idem-proj");
        fs::write(project.join("README.md"), b"hi").unwrap();

        let first = run_wepld(&["open", ".", "--json"], &project, &store);
        assert_eq!(first.code, 0, "first open stderr: {}", first.stderr);
        let id1 = project_id_field(&first.stdout).expect("first open reports a project id");

        let second = run_wepld(&["open", ".", "--json"], &project, &store);
        assert_eq!(second.code, 0, "second open stderr: {}", second.stderr);
        let id2 = project_id_field(&second.stdout).expect("second open reports a project id");

        assert_eq!(
            id1, id2,
            "reopening the same project must reuse its identity"
        );
    }

    #[test]
    fn empty_open_path_is_a_usage_error() {
        let store = scratch("empty-path-store");
        let project = scratch("empty-path-proj");
        let run = run_wepld(&["open", ""], &project, &store);
        assert_eq!(run.code, 2, "empty path must map to the usage/input class");
    }

    #[test]
    fn unknown_command_exits_two_with_a_suggestion_and_never_prompts() {
        let store = scratch("unknown-store");
        let project = scratch("unknown-proj");
        let run = run_wepld(&["opne"], &project, &store);
        assert_eq!(run.code, 2);
        let combined = format!("{}{}", run.stdout, run.stderr).to_lowercase();
        assert!(combined.contains("open"), "expected an `open` suggestion");
        assert!(
            !combined.contains("did you mean to ask")
                && !combined.contains("prompt")
                && !combined.contains("assistant"),
            "an unknown token must never be treated as a model prompt"
        );
    }

    #[test]
    fn status_reports_no_association_before_open_then_the_identity_after() {
        let store = scratch("status-store");
        let project = scratch("status-proj");

        let before = run_wepld(&["status", "--json"], &project, &store);
        assert!(
            before.code == 0 || before.code == 3,
            "status before open: code {} stderr {}",
            before.code,
            before.stderr
        );
        assert!(
            before.stdout.contains("\"associated\":false") || before.code == 3,
            "status before open must not claim an association: {}",
            before.stdout
        );

        let opened = run_wepld(&["open", ".", "--json"], &project, &store);
        assert_eq!(opened.code, 0, "open stderr: {}", opened.stderr);
        let opened_id = project_id_field(&opened.stdout).expect("open reports an id");

        let after = run_wepld(&["status", "--json"], &project, &store);
        assert_eq!(after.code, 0, "status after open stderr: {}", after.stderr);
        assert_eq!(
            project_id_field(&after.stdout).as_deref(),
            Some(opened_id.as_str()),
            "status must report the same identity `open` established"
        );
    }

    #[test]
    fn doctor_completes_and_flags_package_manager_ambiguity() {
        let store = scratch("doctor-amb-store");
        let project = scratch("doctor-amb-proj");
        fs::write(project.join("package.json"), b"{}").unwrap();
        fs::write(project.join("pnpm-lock.yaml"), b"lockfileVersion: 9\n").unwrap();
        fs::write(project.join("yarn.lock"), b"# yarn\n").unwrap();

        let run = run_wepld(&["doctor", "--json"], &project, &store);
        assert!(
            run.code == 0 || run.code == 5,
            "doctor exit: code {} stderr {}",
            run.code,
            run.stderr
        );
        assert!(run.stdout.starts_with('{') && run.stdout.ends_with("}\n"));
        assert!(
            run.stdout.contains("D-PM-AMBIGUOUS"),
            "the filesystem->CLI path must surface package-manager ambiguity, not only \
             the lockfile marker finding: {}",
            run.stdout
        );
        assert!(
            run.stdout.contains("D-LOCK-MULTIPLE-MARKERS"),
            "doctor should also surface the multiple-lockfile-marker finding: {}",
            run.stdout
        );
    }

    #[test]
    fn json_output_is_byte_deterministic_and_control_free() {
        let store = scratch("json-det-store");
        let project = scratch("json-det-proj");

        let a = run_wepld(&["open", ".", "--json", "--no-input"], &project, &store);
        let b = run_wepld(&["open", ".", "--json", "--no-input"], &project, &store);
        assert_eq!(a.code, 0);
        assert_eq!(
            a.stdout, b.stdout,
            "repeated --json open must be byte-identical"
        );
        assert!(!a.stdout.contains('\u{1b}'), "ESC leaked into --json");
        assert!(!a.stdout.contains('\u{0}'), "NUL leaked into --json");
        assert!(a.stdout.starts_with('{') && a.stdout.ends_with("}\n"));
        assert!(a.stdout.contains("\"schema_version\":1"));
    }

    #[test]
    fn open_doctor_status_do_not_mutate_the_project_tree() {
        // S2-S013: the project tree is byte-identical before and after every command.
        let store = scratch("s013-store");
        let project = scratch("s013-proj");
        fs::create_dir_all(project.join("src")).unwrap();
        fs::write(project.join("src/lib.rs"), b"pub fn a() {}\n").unwrap();
        fs::write(project.join("Cargo.toml"), b"[package]\nname=\"x\"\n").unwrap();
        fs::write(project.join("Cargo.lock"), b"# lock\n").unwrap();

        let before = snapshot(&project);
        for args in [
            vec!["open", ".", "--json"],
            vec!["doctor", "--json"],
            vec!["status", "--json"],
        ] {
            let run = run_wepld(&args, &project, &store);
            assert!(
                run.code == 0 || run.code == 5,
                "{args:?} unexpected exit {}: {}",
                run.code,
                run.stderr
            );
        }
        let after = snapshot(&project);
        assert_eq!(
            before, after,
            "open/doctor/status must leave the project tree unchanged"
        );
        assert!(
            !project.join(".wepld").exists(),
            "S2 must not write .wepld/ into the project (clarify Q8)"
        );
    }

    #[test]
    fn no_secret_or_ansi_pattern_appears_in_any_surface() {
        // S2-D015 / S2-S008: neither human nor JSON output carries a raw
        // credential pattern or a terminal control sequence.
        let store = scratch("s008-store");
        let project = scratch("s008-proj");
        fs::write(
            project.join("config.txt"),
            b"url=https://alice:supersecret@host/repo.git\ntoken=ghp_deadbeefdeadbeefdeadbeefdeadbeef0000\n",
        )
        .unwrap();

        for mode in [
            vec!["open", "."],
            vec!["open", ".", "--json"],
            vec!["doctor"],
            vec!["doctor", "--json"],
            vec!["status"],
        ] {
            let run = run_wepld(&mode, &project, &store);
            let all = format!("{}{}", run.stdout, run.stderr);
            assert!(!all.contains("supersecret"), "{mode:?} leaked a credential");
            assert!(!all.contains("ghp_deadbeef"), "{mode:?} leaked a token");
            assert!(
                !all.contains("alice:supersecret"),
                "{mode:?} leaked userinfo"
            );
            assert!(!all.contains('\u{1b}'), "{mode:?} leaked an ANSI escape");
            assert!(!all.contains('\u{0}'), "{mode:?} leaked a NUL");
        }
    }

    #[test]
    fn bin_source_starts_no_project_task_and_opens_no_socket() {
        // S2-D014 / S2-S014: bin/wepld.rs itself never spawns a process (Git
        // topology observation lives behind the qualified S2-AUTH-014 adapter in
        // git_topology.rs, not here) and never touches the network.
        let source =
            fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/bin/wepld.rs"))
                .expect("bin/wepld.rs readable");
        // Strip the module doc comment first: it legitimately *names* the
        // effects it forbids ("never mutates ... `safe.directory`").
        let code: String = source
            .lines()
            .filter(|line| !line.trim_start().starts_with("//!"))
            .collect::<Vec<_>>()
            .join("\n");
        for forbidden in [
            "process::Command",
            "std::net",
            "TcpStream",
            "UdpSocket",
            "reqwest",
            "safe.directory",
            "config --add",
        ] {
            assert!(
                !code.contains(forbidden),
                "bin/wepld.rs must not reference `{forbidden}`"
            );
        }
    }

    #[test]
    fn open_reports_the_documented_authenticity_limitation_not_a_false_pass() {
        // S2-S015 / DIGEST_EQUALITY != AUTHENTICITY.
        let store = scratch("s015-store");
        let project = scratch("s015-proj");
        let run = run_wepld(&["open", ".", "--json"], &project, &store);
        assert_eq!(run.code, 0, "stderr: {}", run.stderr);
        let lower = run.stdout.to_lowercase();
        assert!(
            lower.contains("unauthenticated")
                || lower.contains("not_authenticated")
                || lower.contains("writer")
                || lower.contains("limitation")
                || lower.contains("unkeyed"),
            "open must surface the store authenticity limitation, not a bare success: {}",
            run.stdout
        );
    }
}
