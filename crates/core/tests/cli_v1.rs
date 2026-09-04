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
