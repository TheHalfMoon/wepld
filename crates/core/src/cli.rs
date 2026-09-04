#![forbid(unsafe_code)]

//! S2-AUTH-015 command plane for `wepld open | doctor | status`.
//!
//! This module is pure: it parses an argument vector, and it renders one
//! already-computed [`CommandOutcome`] into either a terminal-safe human string
//! or a versioned deterministic JSON string. It performs no filesystem, process,
//! or network effect — the binary front-end collects observations and this
//! module only projects them.
//!
//! The human and JSON projections are produced from the **same** redacted
//! [`CommandOutcome`]; `--json` is never a bypass for secret suppression or
//! terminal-control-sequence defense.

use std::fmt::Write as _;

use wepld_contracts::{
    DoctorCategory, DoctorFinding, DoctorReport, DoctorSeverity, EvidenceStatus, MachineActionHint,
    RemediationKind, RepositoryTrustState, SafeParameter, StoreAuthenticity,
};

use crate::doctor::{self, DOCTOR_CONTRACT};

/// Schema version of the machine (`--json`) projection. Bumped only on a
/// breaking change to the JSON shape.
pub const JSON_SCHEMA_VERSION: u32 = 1;

/// The exact command surface authorized by v49.
pub const COMMAND_SURFACE: [&str; 3] = ["open", "doctor", "status"];

/// Stable process exit classes. Numeric values are frozen: a value is never
/// reused for a different semantic class.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExitClass {
    /// Command completed and reported a healthy or informational result.
    Success,
    /// Unexpected or internal failure.
    UnexpectedInternal,
    /// Usage or input error (bad flags, unknown command, missing path).
    UsageInput,
    /// Project could not be resolved, or its identity is ambiguous/conflicting.
    ProjectResolutionIdentity,
    /// The local evidence store failed an integrity check.
    EvidenceStoreIntegrity,
    /// Doctor completed but produced at least one blocking finding.
    DoctorBlockingFindings,
    /// A capability required to answer the request is unavailable.
    RequiredCapabilityUnavailable,
}

impl ExitClass {
    /// The frozen numeric process exit code.
    pub fn code(self) -> i32 {
        match self {
            Self::Success => 0,
            Self::UnexpectedInternal => 1,
            Self::UsageInput => 2,
            Self::ProjectResolutionIdentity => 3,
            Self::EvidenceStoreIntegrity => 4,
            Self::DoctorBlockingFindings => 5,
            Self::RequiredCapabilityUnavailable => 6,
        }
    }

    /// Stable machine token for the class, used in JSON and diagnostics.
    pub fn token(self) -> &'static str {
        match self {
            Self::Success => "success",
            Self::UnexpectedInternal => "unexpected_internal",
            Self::UsageInput => "usage_or_input_error",
            Self::ProjectResolutionIdentity => "project_resolution_or_identity_error",
            Self::EvidenceStoreIntegrity => "evidence_store_integrity_error",
            Self::DoctorBlockingFindings => "doctor_completed_with_blocking_findings",
            Self::RequiredCapabilityUnavailable => "required_capability_unavailable",
        }
    }
}

/// Which of the three commands was requested.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Command {
    /// `wepld open <path>`
    Open,
    /// `wepld doctor`
    Doctor,
    /// `wepld status`
    Status,
}

impl Command {
    fn token(self) -> &'static str {
        match self {
            Self::Open => "open",
            Self::Doctor => "doctor",
            Self::Status => "status",
        }
    }
}

/// Human vs machine projection selector.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutputMode {
    /// Terminal-oriented text.
    Human,
    /// Versioned deterministic JSON.
    Json,
}

/// A fully parsed, validated invocation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Invocation {
    /// Selected command.
    pub command: Command,
    /// Explicit local path for `open`. `None` for `doctor` / `status`.
    pub open_path: Option<String>,
    /// Output projection.
    pub output: OutputMode,
    /// `--no-input`: never prompt; any unresolved choice is a non-success exit.
    pub no_input: bool,
}

/// Argument-vector parse failures. Every variant maps to [`ExitClass::UsageInput`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    /// No command token supplied.
    MissingCommand,
    /// First token is not one of `open` / `doctor` / `status`.
    UnknownCommand {
        /// The offending token, already terminal-sanitized.
        token: String,
        /// Closest known command, when one is within edit distance 2.
        suggestion: Option<&'static str>,
    },
    /// `open` requires exactly one non-empty path argument.
    OpenPathMissing,
    /// `open` path argument was empty.
    OpenPathEmpty,
    /// A flag token was not recognized.
    UnknownFlag {
        /// The offending flag, already terminal-sanitized.
        flag: String,
    },
    /// A positional argument was supplied where none is accepted.
    UnexpectedArgument {
        /// The offending argument, already terminal-sanitized.
        argument: String,
    },
}

impl std::fmt::Display for ParseError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::MissingCommand => write!(
                formatter,
                "no command given; expected one of: open, doctor, status"
            ),
            Self::UnknownCommand { token, suggestion } => match suggestion {
                Some(candidate) => write!(
                    formatter,
                    "unknown command '{token}'; did you mean '{candidate}'?"
                ),
                None => write!(
                    formatter,
                    "unknown command '{token}'; expected one of: open, doctor, status"
                ),
            },
            Self::OpenPathMissing => write!(formatter, "'open' requires a project path argument"),
            Self::OpenPathEmpty => write!(formatter, "'open' path argument must not be empty"),
            Self::UnknownFlag { flag } => write!(formatter, "unknown flag '{flag}'"),
            Self::UnexpectedArgument { argument } => {
                write!(formatter, "unexpected argument '{argument}'")
            }
        }
    }
}

impl std::error::Error for ParseError {}

/// Replace every ASCII/Unicode control character with a visible `\u{..}` escape
/// so a hostile argument, path, or descriptor value can never emit a raw
/// terminal control sequence. Applied to every externally-influenced string
/// before it reaches a rendered projection.
pub fn sanitize_terminal(value: &str) -> String {
    let mut output = String::with_capacity(value.len());
    for character in value.chars() {
        if character.is_control() {
            let _ = write!(output, "\\u{{{:x}}}", u32::from(character));
        } else {
            output.push(character);
        }
    }
    output
}

fn edit_distance(left: &str, right: &str) -> usize {
    let left: Vec<char> = left.chars().collect();
    let right: Vec<char> = right.chars().collect();
    let mut previous: Vec<usize> = (0..=right.len()).collect();
    let mut current = vec![0usize; right.len() + 1];
    for (index_left, character_left) in left.iter().enumerate() {
        current[0] = index_left + 1;
        for (index_right, character_right) in right.iter().enumerate() {
            let substitution_cost = usize::from(character_left != character_right);
            current[index_right + 1] = (previous[index_right + 1] + 1)
                .min(current[index_right] + 1)
                .min(previous[index_right] + substitution_cost);
        }
        std::mem::swap(&mut previous, &mut current);
    }
    previous[right.len()]
}

fn nearest_command(token: &str) -> Option<&'static str> {
    COMMAND_SURFACE
        .iter()
        .map(|candidate| (*candidate, edit_distance(token, candidate)))
        .filter(|(_, distance)| *distance <= 2)
        .min_by_key(|(_, distance)| *distance)
        .map(|(candidate, _)| candidate)
}

/// Parse an argument vector (excluding argv[0]). Unknown commands are always
/// errors with a suggestion where possible; they are never treated as prompts.
pub fn parse<S: AsRef<str>>(args: &[S]) -> Result<Invocation, ParseError> {
    let mut tokens = args.iter().map(AsRef::as_ref);

    let Some(command_token) = tokens.next() else {
        return Err(ParseError::MissingCommand);
    };

    let command = match command_token {
        "open" => Command::Open,
        "doctor" => Command::Doctor,
        "status" => Command::Status,
        other => {
            return Err(ParseError::UnknownCommand {
                token: sanitize_terminal(other),
                suggestion: nearest_command(other),
            });
        }
    };

    let mut output = OutputMode::Human;
    let mut no_input = false;
    let mut positionals: Vec<&str> = Vec::new();

    for token in tokens {
        match token {
            "--json" => output = OutputMode::Json,
            "--no-input" => no_input = true,
            flag if flag.starts_with("--") => {
                return Err(ParseError::UnknownFlag {
                    flag: sanitize_terminal(flag),
                });
            }
            positional => positionals.push(positional),
        }
    }

    let open_path = match command {
        Command::Open => match positionals.split_first() {
            None => return Err(ParseError::OpenPathMissing),
            Some((first, rest)) => {
                if let Some(extra) = rest.first() {
                    return Err(ParseError::UnexpectedArgument {
                        argument: sanitize_terminal(extra),
                    });
                }
                if first.is_empty() {
                    return Err(ParseError::OpenPathEmpty);
                }
                Some((*first).to_owned())
            }
        },
        Command::Doctor | Command::Status => {
            if let Some(extra) = positionals.first() {
                return Err(ParseError::UnexpectedArgument {
                    argument: sanitize_terminal(extra),
                });
            }
            None
        }
    };

    Ok(Invocation {
        command,
        open_path,
        output,
        no_input,
    })
}

/// Redacted repository summary for `open` / `status`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RepositorySummary {
    /// Git topology was qualified; carries only the closed trust enum.
    Git {
        /// `trusted` / `refused_by_git` / `unknown`.
        trust_state: RepositoryTrustState,
    },
    /// No Git repository observed; a valid non-Git local project.
    NonGit,
}

/// Redacted evidence-store summary for `open` / `status`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceSummary {
    /// A committed generation was read.
    Present {
        /// Aggregate record status.
        status: EvidenceStatus,
        /// The only authenticity guarantee S2 makes.
        authenticity: StoreAuthenticity,
    },
    /// No committed generation could be read.
    Unavailable,
}

/// One fully-computed command result, already redacted, ready to project.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CommandOutcome {
    /// `open` succeeded far enough to report a locator + summaries.
    Open {
        /// Resolved local project id, if one was resolved/reserved.
        project_id: Option<String>,
        /// Terminal-safe, credential-redacted display of the resolved locator.
        locator_display: String,
        /// Redacted repository summary.
        repository: RepositorySummary,
        /// Redacted evidence summary.
        evidence: EvidenceSummary,
    },
    /// `status` result.
    Status {
        /// Currently associated local project id, if any.
        project_id: Option<String>,
        /// Whether a project is currently associated at all.
        associated: bool,
        /// Redacted evidence summary.
        evidence: EvidenceSummary,
    },
    /// `doctor` completed and produced a report (possibly with findings).
    Doctor {
        /// The deterministically ordered report.
        report: DoctorReport,
    },
    /// The command failed before producing a result.
    Failure {
        /// Which command was attempted.
        command: Command,
        /// Frozen exit class.
        class: ExitClass,
        /// Stable machine reason token (already sanitized / closed vocabulary).
        reason: String,
    },
}

impl CommandOutcome {
    /// The frozen exit class this outcome maps to.
    pub fn exit_class(&self) -> ExitClass {
        match self {
            Self::Open { evidence, .. } => match evidence {
                EvidenceSummary::Present {
                    status: EvidenceStatus::Corrupt | EvidenceStatus::Partial,
                    ..
                } => ExitClass::EvidenceStoreIntegrity,
                EvidenceSummary::Unavailable => ExitClass::RequiredCapabilityUnavailable,
                EvidenceSummary::Present { .. } => ExitClass::Success,
            },
            Self::Status { .. } => ExitClass::Success,
            Self::Doctor { report } => {
                if doctor::has_blocking_findings(report) {
                    ExitClass::DoctorBlockingFindings
                } else {
                    ExitClass::Success
                }
            }
            Self::Failure { class, .. } => *class,
        }
    }
}

fn trust_token(trust_state: RepositoryTrustState) -> &'static str {
    match trust_state {
        RepositoryTrustState::Trusted => "trusted",
        RepositoryTrustState::RefusedByGit => "refused_by_git",
        RepositoryTrustState::Unknown => "unknown",
    }
}

fn evidence_status_token(status: EvidenceStatus) -> &'static str {
    match status {
        EvidenceStatus::Complete => "complete",
        EvidenceStatus::Partial => "partial",
        EvidenceStatus::Stale => "stale",
        EvidenceStatus::Corrupt => "corrupt",
        EvidenceStatus::Unavailable => "unavailable",
    }
}

fn authenticity_token(authenticity: StoreAuthenticity) -> &'static str {
    match authenticity {
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly => {
            "unauthenticated_structural_coherence_only"
        }
    }
}

fn severity_token(severity: DoctorSeverity) -> &'static str {
    match severity {
        DoctorSeverity::Info => "info",
        DoctorSeverity::Warning => "warning",
        DoctorSeverity::Blocking => "blocking",
    }
}

fn category_token(category: DoctorCategory) -> &'static str {
    match category {
        DoctorCategory::Identity => "identity",
        DoctorCategory::Repository => "repository",
        DoctorCategory::Workspace => "workspace",
        DoctorCategory::ToolchainDescriptor => "toolchain_descriptor",
        DoctorCategory::Lockfile => "lockfile",
        DoctorCategory::PackageManager => "package_manager",
        DoctorCategory::EvidenceStore => "evidence_store",
        DoctorCategory::Freshness => "freshness",
        DoctorCategory::SecuritySensitiveConfig => "security_sensitive_config",
    }
}

fn remediation_token(kind: RemediationKind) -> &'static str {
    match kind {
        RemediationKind::None => "none",
        RemediationKind::Informational => "informational",
        RemediationKind::ManualAction => "manual_action",
        RemediationKind::CapabilityRequired => "capability_required",
    }
}

fn hint_token(hint: MachineActionHint) -> &'static str {
    match hint {
        MachineActionHint::InspectIdentity => "inspect_identity",
        MachineActionHint::InspectRepositoryTrust => "inspect_repository_trust",
        MachineActionHint::InspectWorkspace => "inspect_workspace",
        MachineActionHint::InspectEvidenceStore => "inspect_evidence_store",
        MachineActionHint::RefreshEvidence => "refresh_evidence",
        MachineActionHint::ResolveAmbiguity => "resolve_ambiguity",
    }
}

fn json_escape(value: &str, output: &mut String) {
    output.push('"');
    for character in value.chars() {
        match character {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            control if control.is_control() => {
                let _ = write!(output, "\\u{:04x}", u32::from(control));
            }
            other => output.push(other),
        }
    }
    output.push('"');
}

fn json_field_string(output: &mut String, key: &str, value: &str, trailing_comma: bool) {
    json_escape(key, output);
    output.push(':');
    json_escape(&sanitize_terminal(value), output);
    if trailing_comma {
        output.push(',');
    }
}

fn safe_parameter_json(parameter: &SafeParameter, output: &mut String) {
    output.push('{');
    match parameter {
        SafeParameter::Boolean { value } => {
            json_field_string(output, "kind", "boolean", true);
            let _ = write!(output, "\"value\":{value}");
        }
        SafeParameter::Count { value } => {
            json_field_string(output, "kind", "count", true);
            let _ = write!(output, "\"value\":{value}");
        }
        SafeParameter::Path { value } => {
            json_field_string(output, "kind", "path", true);
            json_field_string(output, "value", value.as_str(), false);
        }
        SafeParameter::Toolchain { value } => {
            json_field_string(output, "kind", "toolchain", true);
            json_field_string(output, "value", &format!("{value:?}").to_lowercase(), false);
        }
        SafeParameter::PackageManager { value } => {
            json_field_string(output, "kind", "package_manager", true);
            json_field_string(output, "value", &format!("{value:?}").to_lowercase(), false);
        }
        SafeParameter::TrustState { value } => {
            json_field_string(output, "kind", "trust_state", true);
            json_field_string(output, "value", trust_token(*value), false);
        }
        SafeParameter::EvidenceStatus { value } => {
            json_field_string(output, "kind", "evidence_status", true);
            json_field_string(output, "value", evidence_status_token(*value), false);
        }
        SafeParameter::LockScope { value } => {
            json_field_string(output, "kind", "lock_scope", true);
            let token = match value {
                wepld_contracts::StoreLockScope::IdentityCatalog => "identity_catalog",
                wepld_contracts::StoreLockScope::ProjectStore => "project_store",
            };
            json_field_string(output, "value", token, false);
        }
    }
    output.push('}');
}

fn finding_json(finding: &DoctorFinding, output: &mut String) {
    output.push('{');
    json_field_string(output, "finding_code", finding.finding_code.as_str(), true);
    json_field_string(output, "severity", severity_token(finding.severity), true);
    json_field_string(output, "category", category_token(finding.category), true);
    json_field_string(
        output,
        "summary_template_id",
        finding.summary_template_id.as_str(),
        true,
    );
    json_field_string(
        output,
        "explanation_template_id",
        finding.explanation_template_id.as_str(),
        true,
    );
    json_field_string(
        output,
        "remediation_kind",
        remediation_token(finding.remediation_kind),
        true,
    );
    json_field_string(
        output,
        "remediation_template_id",
        finding.remediation_template_id.as_str(),
        true,
    );
    output.push_str("\"machine_action_hint\":");
    match finding.machine_action_hint {
        Some(hint) => json_escape(hint_token(hint), output),
        None => output.push_str("null"),
    }
    output.push(',');
    output.push_str("\"safe_parameters\":[");
    for (index, parameter) in finding.safe_parameters.as_slice().iter().enumerate() {
        if index > 0 {
            output.push(',');
        }
        safe_parameter_json(parameter, output);
    }
    output.push_str("]}");
}

fn evidence_json(evidence: &EvidenceSummary, output: &mut String) {
    match evidence {
        EvidenceSummary::Present {
            status,
            authenticity,
        } => {
            output.push_str("{\"state\":\"present\",");
            json_field_string(output, "status", evidence_status_token(*status), true);
            json_field_string(
                output,
                "authenticity",
                authenticity_token(*authenticity),
                false,
            );
            output.push('}');
        }
        EvidenceSummary::Unavailable => output.push_str("{\"state\":\"unavailable\"}"),
    }
}

/// Render the machine (`--json`) projection. Deterministic key order, no ANSI,
/// same redaction policy as the human projection.
pub fn render_json(outcome: &CommandOutcome) -> String {
    let mut output = String::new();
    output.push('{');
    let _ = write!(output, "\"schema_version\":{JSON_SCHEMA_VERSION},");
    json_field_string(&mut output, "contract", DOCTOR_CONTRACT, true);

    match outcome {
        CommandOutcome::Open {
            project_id,
            locator_display,
            repository,
            evidence,
        } => {
            json_field_string(&mut output, "command", "open", true);
            json_field_string(&mut output, "outcome", "success", true);
            json_optional_string(&mut output, "project_id", project_id.as_deref(), true);
            json_field_string(&mut output, "locator_display", locator_display, true);
            output.push_str("\"repository\":");
            match repository {
                RepositorySummary::Git { trust_state } => {
                    output.push_str("{\"kind\":\"git\",");
                    json_field_string(&mut output, "trust_state", trust_token(*trust_state), false);
                    output.push('}');
                }
                RepositorySummary::NonGit => output.push_str("{\"kind\":\"non_git\"}"),
            }
            output.push(',');
            output.push_str("\"evidence\":");
            evidence_json(evidence, &mut output);
            output.push(',');
            json_field_string(
                &mut output,
                "exit_class",
                outcome.exit_class().token(),
                false,
            );
        }
        CommandOutcome::Status {
            project_id,
            associated,
            evidence,
        } => {
            json_field_string(&mut output, "command", "status", true);
            json_field_string(&mut output, "outcome", "success", true);
            let _ = write!(output, "\"associated\":{associated},");
            json_optional_string(&mut output, "project_id", project_id.as_deref(), true);
            output.push_str("\"evidence\":");
            evidence_json(evidence, &mut output);
            output.push(',');
            json_field_string(
                &mut output,
                "exit_class",
                outcome.exit_class().token(),
                false,
            );
        }
        CommandOutcome::Doctor { report } => {
            json_field_string(&mut output, "command", "doctor", true);
            json_field_string(&mut output, "outcome", "success", true);
            json_field_string(&mut output, "project_id", report.project_id.as_str(), true);
            json_optional_string(
                &mut output,
                "selected_generation_id",
                report.selected_generation_id.as_ref().map(|id| id.as_str()),
                true,
            );
            let _ = write!(output, "\"evaluated_at\":{},", report.evaluated_at.get());
            let _ = write!(
                output,
                "\"blocking\":{},",
                doctor::has_blocking_findings(report)
            );
            output.push_str("\"findings\":[");
            for (index, finding) in report.findings.as_slice().iter().enumerate() {
                if index > 0 {
                    output.push(',');
                }
                finding_json(finding, &mut output);
            }
            output.push_str("],");
            json_field_string(
                &mut output,
                "exit_class",
                outcome.exit_class().token(),
                false,
            );
        }
        CommandOutcome::Failure {
            command,
            class,
            reason,
        } => {
            json_field_string(&mut output, "command", command.token(), true);
            json_field_string(&mut output, "outcome", "error", true);
            json_field_string(&mut output, "reason", reason, true);
            json_field_string(&mut output, "exit_class", class.token(), false);
        }
    }

    output.push('}');
    output.push('\n');
    output
}

fn json_optional_string(output: &mut String, key: &str, value: Option<&str>, trailing_comma: bool) {
    json_escape(key, output);
    output.push(':');
    match value {
        Some(value) => json_escape(&sanitize_terminal(value), output),
        None => output.push_str("null"),
    }
    if trailing_comma {
        output.push(',');
    }
}

fn push_line(output: &mut String, line: &str) {
    output.push_str(&sanitize_terminal(line));
    output.push('\n');
}

/// Render the human (terminal) projection from the same redacted outcome. All
/// externally-influenced text passes through [`sanitize_terminal`].
pub fn render_human(outcome: &CommandOutcome) -> String {
    let mut output = String::new();
    match outcome {
        CommandOutcome::Open {
            project_id,
            locator_display,
            repository,
            evidence,
        } => {
            push_line(&mut output, "wepld open");
            push_line(
                &mut output,
                &format!(
                    "  project: {}",
                    project_id.as_deref().unwrap_or("(unresolved)")
                ),
            );
            push_line(&mut output, &format!("  locator: {locator_display}"));
            match repository {
                RepositorySummary::Git { trust_state } => push_line(
                    &mut output,
                    &format!("  repository: git (trust: {})", trust_token(*trust_state)),
                ),
                RepositorySummary::NonGit => {
                    push_line(&mut output, "  repository: none (non-git local project)");
                }
            }
            render_evidence_human(&mut output, evidence);
            push_line(
                &mut output,
                &format!("  exit: {}", outcome.exit_class().token()),
            );
        }
        CommandOutcome::Status {
            project_id,
            associated,
            evidence,
        } => {
            push_line(&mut output, "wepld status");
            if *associated {
                push_line(
                    &mut output,
                    &format!(
                        "  project: {}",
                        project_id.as_deref().unwrap_or("(unresolved)")
                    ),
                );
            } else {
                push_line(&mut output, "  project: (none associated)");
            }
            render_evidence_human(&mut output, evidence);
            push_line(
                &mut output,
                &format!("  exit: {}", outcome.exit_class().token()),
            );
        }
        CommandOutcome::Doctor { report } => {
            push_line(&mut output, "wepld doctor");
            push_line(
                &mut output,
                &format!("  project: {}", report.project_id.as_str()),
            );
            let blocking = doctor::has_blocking_findings(report);
            push_line(
                &mut output,
                &format!(
                    "  findings: {} ({})",
                    report.findings.len(),
                    if blocking {
                        "blocking present"
                    } else {
                        "no blocking"
                    }
                ),
            );
            for finding in report.findings.as_slice() {
                render_finding_human(&mut output, finding);
            }
            push_line(
                &mut output,
                &format!("  exit: {}", outcome.exit_class().token()),
            );
        }
        CommandOutcome::Failure {
            command,
            class,
            reason,
        } => {
            push_line(&mut output, &format!("wepld {}: error", command.token()));
            push_line(&mut output, &format!("  reason: {reason}"));
            push_line(&mut output, &format!("  exit: {}", class.token()));
        }
    }
    output
}

fn render_evidence_human(output: &mut String, evidence: &EvidenceSummary) {
    match evidence {
        EvidenceSummary::Present {
            status,
            authenticity,
        } => {
            push_line(
                output,
                &format!(
                    "  evidence: {} (authenticity: {})",
                    evidence_status_token(*status),
                    authenticity_token(*authenticity)
                ),
            );
        }
        EvidenceSummary::Unavailable => push_line(output, "  evidence: unavailable"),
    }
}

fn render_finding_human(output: &mut String, finding: &DoctorFinding) {
    let summary =
        doctor::render_template(&finding.summary_template_id).unwrap_or("(unknown finding)");
    push_line(
        output,
        &format!(
            "  - [{}] {} {}",
            severity_token(finding.severity),
            finding.finding_code.as_str(),
            summary
        ),
    );
    if let Some(explanation) = doctor::render_template(&finding.explanation_template_id) {
        push_line(output, &format!("      {explanation}"));
    }
    if !matches!(finding.remediation_kind, RemediationKind::None)
        && let Some(remediation) = doctor::render_template(&finding.remediation_template_id)
    {
        push_line(output, &format!("      remediation: {remediation}"));
    }
}

/// Project one outcome according to the requested mode.
pub fn render(outcome: &CommandOutcome, mode: OutputMode) -> String {
    match mode {
        OutputMode::Human => render_human(outcome),
        OutputMode::Json => render_json(outcome),
    }
}
