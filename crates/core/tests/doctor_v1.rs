#![forbid(unsafe_code)]

//! S2-AUTH-015 Project Doctor behavior and negative oracles.

use std::path::PathBuf;

use wepld_contracts::{
    DoctorCategory, DoctorSeverity, EvidenceStatus, ProjectId, RemediationKind,
    RepositoryTrustState, SafeParameter, StoreAuthenticity, UnixMillis,
};
use wepld_core::doctor::{
    self, DescriptorBound, DescriptorObservation, DoctorInputError, DoctorInputs,
    EvidenceStoreObservation, IdentityObservation, MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES,
    MAX_PARSED_DESCRIPTOR_BYTES, MAX_ROOT_DESCRIPTOR_CANDIDATES, MAX_STRUCTURED_NESTING_DEPTH,
    RepositoryObservation, SecuritySensitiveObservation,
};

fn project_id() -> ProjectId {
    ProjectId::try_from("p_test").expect("static test id is valid")
}

fn at() -> UnixMillis {
    UnixMillis::new(1_700_000_000_000)
}

fn healthy_inputs() -> DoctorInputs {
    DoctorInputs {
        project_id: project_id(),
        selected_generation_id: None,
        identity: IdentityObservation::Bound,
        repository: Some(RepositoryObservation {
            trust_state: RepositoryTrustState::Trusted,
            nested_candidate_ambiguity: false,
            linked_worktree_state_unknown: false,
        }),
        evidence_store: Some(EvidenceStoreObservation {
            status: EvidenceStatus::Complete,
            integrity_defect: false,
            stale_required_record: false,
            authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
        }),
        descriptors: DescriptorObservation {
            toolchains: vec![wepld_contracts::ToolchainKind::Rust],
            package_managers: vec![wepld_contracts::PackageManagerKind::Cargo],
            lockfile_marker_count: 1,
            package_manager_ambiguous: false,
            descriptor_budget_rejected: false,
        },
        security_sensitive: SecuritySensitiveObservation::default(),
    }
}

fn codes(report: &wepld_contracts::DoctorReport) -> Vec<String> {
    report
        .findings
        .as_slice()
        .iter()
        .map(|finding| finding.finding_code.as_str().to_owned())
        .collect()
}

#[test]
fn healthy_project_yields_only_the_authenticity_limitation_and_no_blocking() {
    let report = doctor::evaluate(&healthy_inputs(), at()).expect("evaluate");
    assert_eq!(codes(&report), vec!["D-EV-AUTHENTICITY-LIMITATION"]);
    assert!(!doctor::has_blocking_findings(&report));
}

#[test]
fn unavailable_identity_is_not_healthy() {
    let mut inputs = healthy_inputs();
    inputs.identity = IdentityObservation::Unavailable;
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    assert!(codes(&report).contains(&"D-ID-UNAVAILABLE".to_owned()));
    assert!(doctor::has_blocking_findings(&report));
}

#[test]
fn ambiguous_identity_is_blocking_and_carries_only_a_safe_count() {
    let mut inputs = healthy_inputs();
    inputs.identity = IdentityObservation::Ambiguous { candidate_count: 3 };
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let finding = report
        .findings
        .as_slice()
        .iter()
        .find(|finding| finding.finding_code.as_str() == "D-ID-AMBIGUOUS")
        .expect("ambiguous finding present");
    assert_eq!(finding.severity, DoctorSeverity::Blocking);
    assert_eq!(finding.category, DoctorCategory::Identity);
    assert_eq!(
        finding.safe_parameters.as_slice(),
        &[SafeParameter::Count { value: 3 }]
    );
}

#[test]
fn git_trust_refusal_is_blocking_and_never_proposes_editing_safe_directory() {
    let mut inputs = healthy_inputs();
    inputs.repository = Some(RepositoryObservation {
        trust_state: RepositoryTrustState::RefusedByGit,
        nested_candidate_ambiguity: false,
        linked_worktree_state_unknown: false,
    });
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let finding = report
        .findings
        .as_slice()
        .iter()
        .find(|finding| finding.finding_code.as_str() == "D-GIT-TRUST-REFUSED")
        .expect("trust-refused finding present");
    assert_eq!(finding.severity, DoctorSeverity::Blocking);
    assert_eq!(finding.remediation_kind, RemediationKind::ManualAction);

    let remediation = doctor::render_template(&finding.remediation_template_id)
        .expect("remediation template resolves");
    // The remediation is a user-owned manual decision; WePLD never offers to add
    // or widen safe.directory itself.
    assert!(remediation.contains("does not add or widen safe.directory"));
    let lowered = remediation.to_lowercase();
    assert!(!lowered.contains("run `git config"));
    assert!(!lowered.contains("git config --global --add safe.directory"));
}

#[test]
fn non_git_project_is_valid_with_repository_facts_absent() {
    let mut inputs = healthy_inputs();
    inputs.repository = None;
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let finding = report
        .findings
        .as_slice()
        .iter()
        .find(|finding| finding.finding_code.as_str() == "D-GIT-ABSENT-NON-GIT")
        .expect("absent-repo finding present");
    assert_eq!(finding.severity, DoctorSeverity::Info);
    assert!(!doctor::has_blocking_findings(&report));
}

#[test]
fn unavailable_store_is_blocking() {
    let mut inputs = healthy_inputs();
    inputs.evidence_store = None;
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    assert!(codes(&report).contains(&"D-EV-STORE-UNAVAILABLE".to_owned()));
    assert!(doctor::has_blocking_findings(&report));
}

#[test]
fn partial_store_is_not_complete() {
    let mut inputs = healthy_inputs();
    inputs.evidence_store = Some(EvidenceStoreObservation {
        status: EvidenceStatus::Partial,
        integrity_defect: false,
        stale_required_record: false,
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    });
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    assert!(codes(&report).contains(&"D-EV-STORE-PARTIAL".to_owned()));
    assert!(doctor::has_blocking_findings(&report));
}

#[test]
fn unavailable_status_store_is_distinct_from_partial() {
    let mut inputs = healthy_inputs();
    inputs.evidence_store = Some(EvidenceStoreObservation {
        status: EvidenceStatus::Unavailable,
        integrity_defect: false,
        stale_required_record: false,
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    });
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let observed = codes(&report);
    assert!(
        observed.contains(&"D-EV-STORE-UNAVAILABLE".to_owned()),
        "unavailable evidence must carry the unavailable finding code: {observed:?}"
    );
    assert!(
        !observed.contains(&"D-EV-STORE-PARTIAL".to_owned()),
        "unavailable evidence must not be reported as partial: {observed:?}"
    );
    assert!(doctor::has_blocking_findings(&report));
}

#[test]
fn corrupt_store_is_blocking_integrity_defect() {
    let mut inputs = healthy_inputs();
    inputs.evidence_store = Some(EvidenceStoreObservation {
        status: EvidenceStatus::Corrupt,
        integrity_defect: true,
        stale_required_record: false,
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    });
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    assert!(codes(&report).contains(&"D-EV-STORE-CORRUPT".to_owned()));
    assert!(doctor::has_blocking_findings(&report));
}

#[test]
fn stale_required_record_is_not_fresh() {
    let mut inputs = healthy_inputs();
    inputs.evidence_store = Some(EvidenceStoreObservation {
        status: EvidenceStatus::Stale,
        integrity_defect: false,
        stale_required_record: true,
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    });
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let finding = report
        .findings
        .as_slice()
        .iter()
        .find(|finding| finding.finding_code.as_str() == "D-FRESH-STALE-REQUIRED-RECORD")
        .expect("stale finding present");
    assert_eq!(finding.category, DoctorCategory::Freshness);
}

#[test]
fn multiple_lockfiles_and_ambiguous_package_manager_are_reported_not_resolved() {
    let mut inputs = healthy_inputs();
    inputs.descriptors.lockfile_marker_count = 3;
    inputs.descriptors.package_manager_ambiguous = true;
    inputs.descriptors.package_managers = vec![
        wepld_contracts::PackageManagerKind::Npm,
        wepld_contracts::PackageManagerKind::Pnpm,
    ];
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let found = codes(&report);
    assert!(found.contains(&"D-LOCK-MULTIPLE-MARKERS".to_owned()));
    assert!(found.contains(&"D-PM-AMBIGUOUS".to_owned()));
}

#[test]
fn security_sensitive_config_reports_only_safe_counts_no_raw_values() {
    let mut inputs = healthy_inputs();
    inputs.security_sensitive = SecuritySensitiveObservation {
        credential_bearing_entry_count: 2,
        redacted_remote_url_count: 1,
    };
    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    let finding = report
        .findings
        .as_slice()
        .iter()
        .find(|finding| finding.finding_code.as_str() == "D-SEC-CREDENTIAL-BEARING-CONFIG")
        .expect("security finding present");
    for parameter in finding.safe_parameters.as_slice() {
        assert!(
            matches!(parameter, SafeParameter::Count { .. }),
            "security finding must expose counts only, got {parameter:?}"
        );
    }
}

#[test]
fn evaluation_is_deterministic_and_sorted_by_category_then_severity_then_code() {
    let mut inputs = healthy_inputs();
    inputs.identity = IdentityObservation::Conflict;
    inputs.repository = Some(RepositoryObservation {
        trust_state: RepositoryTrustState::Unknown,
        nested_candidate_ambiguity: true,
        linked_worktree_state_unknown: true,
    });
    inputs.evidence_store = None;
    inputs.descriptors.toolchains.clear();
    inputs.descriptors.lockfile_marker_count = 2;
    inputs.security_sensitive.credential_bearing_entry_count = 1;

    let first = doctor::evaluate(&inputs, at()).expect("evaluate");
    let second = doctor::evaluate(&inputs, at()).expect("evaluate");
    assert_eq!(codes(&first), codes(&second));

    let findings = first.findings.as_slice();
    for window in findings.windows(2) {
        let order = category_rank(window[0].category)
            .cmp(&category_rank(window[1].category))
            .then(severity_rank(window[0].severity).cmp(&severity_rank(window[1].severity)))
            .then(
                window[0]
                    .finding_code
                    .as_str()
                    .cmp(window[1].finding_code.as_str()),
            );
        assert_ne!(order, std::cmp::Ordering::Greater, "findings not sorted");
    }
}

fn category_rank(category: DoctorCategory) -> u8 {
    match category {
        DoctorCategory::Identity => 0,
        DoctorCategory::Repository => 1,
        DoctorCategory::Workspace => 2,
        DoctorCategory::ToolchainDescriptor => 3,
        DoctorCategory::Lockfile => 4,
        DoctorCategory::PackageManager => 5,
        DoctorCategory::EvidenceStore => 6,
        DoctorCategory::Freshness => 7,
        DoctorCategory::SecuritySensitiveConfig => 8,
    }
}

fn severity_rank(severity: DoctorSeverity) -> u8 {
    match severity {
        DoctorSeverity::Blocking => 0,
        DoctorSeverity::Warning => 1,
        DoctorSeverity::Info => 2,
    }
}

#[test]
fn every_finding_uses_wepld_owned_templates_and_d_prefixed_codes() {
    let mut inputs = healthy_inputs();
    inputs.identity = IdentityObservation::Ambiguous { candidate_count: 2 };
    inputs.repository = None;
    inputs.evidence_store = None;
    inputs.descriptors.toolchains.clear();
    inputs.descriptors.lockfile_marker_count = 2;
    inputs.descriptors.package_manager_ambiguous = true;
    inputs.descriptors.descriptor_budget_rejected = true;
    inputs.security_sensitive.credential_bearing_entry_count = 1;

    let report = doctor::evaluate(&inputs, at()).expect("evaluate");
    for finding in report.findings.as_slice() {
        assert!(finding.finding_code.as_str().starts_with("D-"));
        assert!(doctor::render_template(&finding.summary_template_id).is_some());
        assert!(doctor::render_template(&finding.explanation_template_id).is_some());
        assert!(doctor::render_template(&finding.remediation_template_id).is_some());
    }
}

#[test]
fn store_authenticity_is_structural_coherence_only_never_a_pass() {
    assert_eq!(
        doctor::store_authenticity(),
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    );
    let explanation = doctor::render_template(
        &wepld_contracts::TemplateId::try_from("tpl.doctor.evidence.authenticity.explain")
            .expect("template id"),
    )
    .expect("authenticity template resolves");
    assert!(explanation.to_lowercase().contains("not authenticity"));
}

#[test]
fn descriptor_budget_bounds_fail_closed_at_each_limit() {
    doctor::check_descriptor_budget(
        MAX_ROOT_DESCRIPTOR_CANDIDATES,
        MAX_PARSED_DESCRIPTOR_BYTES,
        MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES,
        MAX_STRUCTURED_NESTING_DEPTH,
    )
    .expect("exact limits accepted");

    assert_eq!(
        doctor::check_descriptor_budget(MAX_ROOT_DESCRIPTOR_CANDIDATES + 1, 0, 0, 0),
        Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::CandidateCount
        })
    );
    assert_eq!(
        doctor::check_descriptor_budget(0, MAX_PARSED_DESCRIPTOR_BYTES + 1, 0, 0),
        Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::PerFileBytes
        })
    );
    assert_eq!(
        doctor::check_descriptor_budget(0, 0, MAX_PARSED_DESCRIPTOR_AGGREGATE_BYTES + 1, 0),
        Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::AggregateBytes
        })
    );
    assert_eq!(
        doctor::check_descriptor_budget(0, 0, 0, MAX_STRUCTURED_NESTING_DEPTH + 1),
        Err(DoctorInputError::DescriptorBudgetExceeded {
            bound: DescriptorBound::NestingDepth
        })
    );
}

/// S2-D014 / S2-S014 negative oracle: the Doctor module performs no process
/// execution, installation, remediation, or network effect. Enforced statically
/// against the module source so a later edit that reaches for one is caught.
#[test]
fn doctor_module_source_contains_no_process_or_network_effect() {
    let source =
        std::fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/doctor.rs"))
            .expect("doctor.rs readable");
    for forbidden in [
        "std::process",
        "Command::new",
        "std::net",
        "TcpStream",
        "std::fs::",
        "std::env::",
    ] {
        assert!(
            !source.contains(forbidden),
            "doctor.rs must not reference `{forbidden}`"
        );
    }
}
