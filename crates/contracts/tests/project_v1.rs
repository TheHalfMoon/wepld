#![forbid(unsafe_code)]

use serde_json::json;
use wepld_contracts::*;

fn project_id() -> ProjectId {
    ProjectId::try_from("p_project_001").expect("fixture project id must be valid")
}

fn worktree_id() -> WorktreeId {
    WorktreeId::try_from("w_worktree_001").expect("fixture worktree id must be valid")
}

fn record_id(value: &str) -> RecordId {
    RecordId::try_from(value).expect("fixture record id must be valid")
}

fn generation_id() -> GenerationId {
    GenerationId::try_from("g_generation_001").expect("fixture generation id must be valid")
}

fn digest(byte: char) -> ContentDigest {
    ContentDigest::sha256(byte.to_string().repeat(64)).expect("fixture digest must be valid")
}

fn locator() -> ProjectLocator {
    ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: MachinePath::utf8("./workspace").expect("fixture input path must fit"),
        lexical_absolute_path: MachinePath::utf8("/tmp/workspace")
            .expect("fixture absolute path must fit"),
        resolved_path: Observation::Available {
            value: MachinePath::utf8("/tmp/workspace").expect("fixture resolved path must fit"),
        },
        observation_time: UnixMillis::new(1_787_912_000_000),
    }
}

fn topology() -> RepositoryTopology {
    RepositoryTopology {
        schema_version: ProjectContractVersion::V1,
        vcs_kind: VcsKind::Git,
        worktree_root: Observation::Available {
            value: MachinePath::utf8("/tmp/workspace").expect("fixture path must fit"),
        },
        absolute_git_dir: Observation::Available {
            value: MachinePath::utf8("/tmp/workspace/.git").expect("fixture path must fit"),
        },
        git_common_dir: Observation::Available {
            value: MachinePath::utf8("/tmp/workspace/.git").expect("fixture path must fit"),
        },
        is_bare: Observation::Available { value: false },
        is_inside_worktree: Observation::Available { value: true },
        superproject_worktree: OptionalObservation::None,
        linked_worktree_state: LinkedWorktreeState::Known,
        trust_state: RepositoryTrustState::Trusted,
    }
}

fn safe_finding() -> DoctorFinding {
    DoctorFinding {
        finding_code: FindingCode::try_from("D-GIT-001")
            .expect("fixture finding code must be valid"),
        severity: DoctorSeverity::Warning,
        category: DoctorCategory::Repository,
        summary_template_id: TemplateId::try_from("tpl.doctor.repository.summary")
            .expect("fixture template id must be valid"),
        explanation_template_id: TemplateId::try_from("tpl.doctor.repository.explanation")
            .expect("fixture template id must be valid"),
        observed_evidence_refs: EvidenceReferenceList::try_from(vec![record_id("r_topology")])
            .expect("fixture evidence list must fit"),
        remediation_kind: RemediationKind::ManualAction,
        remediation_template_id: TemplateId::try_from("tpl.doctor.repository.remediation")
            .expect("fixture template id must be valid"),
        machine_action_hint: Some(MachineActionHint::InspectRepositoryTrust),
        safe_parameters: SafeParameterList::try_from(vec![
            SafeParameter::TrustState {
                value: RepositoryTrustState::Trusted,
            },
            SafeParameter::Path {
                value: MachinePath::utf8("/tmp/workspace\nunsafe")
                    .expect("fixture path must fit")
                    .safe_display(),
            },
        ])
        .expect("fixture safe parameters must fit"),
    }
}

#[test]
fn project_contract_v1_constants_are_frozen() {
    assert_eq!(
        ProjectContractVersion::V1.get(),
        PROJECT_CONTRACT_VERSION_V1
    );
    assert_eq!(PROJECT_CONTRACT_VERSION_V1, 1);
    assert_eq!(MAX_PROJECT_CONTRACT_JSON_BYTES, 1_048_576);
    assert_eq!(MAX_MACHINE_PATH_BYTES, 32_768);
    assert_eq!(MAX_MACHINE_PATH_WIDE_UNITS, 32_768);
    assert_eq!(MAX_IDENTITY_CANDIDATES, 32);
    assert_eq!(MAX_SAFE_PARAMETERS, 16);
}

#[test]
fn project_locator_preserves_machine_path_layers_and_safe_display() {
    let unix = MachinePath::unix_bytes(vec![b'a', 0, b'b']).expect("unix path must fit");
    assert_eq!(unix.safe_display().as_str(), "a\\x00b");

    let windows = MachinePath::windows_wtf16(vec![u16::from(b'C'), u16::from(b':'), 0xd800])
        .expect("Windows path must fit");
    assert_eq!(windows.safe_display().as_str(), "C:\\ud800");

    let value = locator();
    let bytes = canonical_project_json(&value).expect("locator must serialize");
    let decoded: ProjectLocator = decode_project_json(&bytes).expect("locator must deserialize");
    assert_eq!(decoded, value);
}

#[test]
fn repository_topology_round_trips_and_future_contract_values_fail_closed() {
    let value = topology();
    let bytes = canonical_project_json(&value).expect("topology must serialize");
    let decoded: RepositoryTopology =
        decode_project_json(&bytes).expect("topology must deserialize");
    assert_eq!(decoded, value);

    let mut future_version = serde_json::to_value(locator()).expect("locator must convert to JSON");
    future_version["schema_version"] = json!(2);
    assert!(serde_json::from_value::<ProjectLocator>(future_version).is_err());

    let mut future_enum = serde_json::to_value(topology()).expect("topology must convert to JSON");
    future_enum["trust_state"] = json!("future_trust_state");
    assert!(serde_json::from_value::<RepositoryTopology>(future_enum).is_err());

    let mut unknown_field = serde_json::to_value(locator()).expect("locator must convert to JSON");
    unknown_field["unexpected"] = json!(true);
    assert!(serde_json::from_value::<ProjectLocator>(unknown_field).is_err());
}

#[test]
fn tagged_project_contract_enums_reject_unknown_fields() {
    assert!(
        serde_json::from_value::<MachinePath>(json!({
            "encoding": "utf8",
            "value": "/tmp/workspace",
            "unexpected": true
        }))
        .is_err()
    );
    assert!(
        serde_json::from_value::<Observation<MachinePath>>(json!({
            "state": "available",
            "value": {"encoding": "utf8", "value": "/tmp/workspace"},
            "unexpected": true
        }))
        .is_err()
    );
    assert!(
        serde_json::from_value::<OptionalObservation<MachinePath>>(json!({
            "state": "none",
            "unexpected": true
        }))
        .is_err()
    );
    assert!(
        serde_json::from_value::<IdentityResolution>(json!({
            "result": "busy",
            "scope": "identity_catalog",
            "unexpected": true
        }))
        .is_err()
    );
    assert!(
        serde_json::from_value::<SafeParameter>(json!({
            "kind": "count",
            "value": 1,
            "unexpected": true
        }))
        .is_err()
    );
    assert!(
        serde_json::from_value::<ProjectCommandEnvelope<()>>(json!({
            "outcome": "success",
            "schema_version": 1,
            "command": "status",
            "project_id": null,
            "data": null,
            "unexpected": true
        }))
        .is_err()
    );
}

#[test]
fn identity_reservation_resolution_and_busy_states_are_versioned_and_bounded() {
    let reservation = IdentityCatalogReservation {
        schema_version: ProjectContractVersion::V1,
        reservation_key_version: 1,
        revalidated_match_facts_digest: digest('a'),
        project_id: project_id(),
        state: IdentityReservationState::Reserved,
        created_at: UnixMillis::new(10),
        updated_at: UnixMillis::new(11),
    };
    let reserved = IdentityResolution::Reserved {
        reservation: reservation.clone(),
    };
    let bytes = canonical_project_json(&reserved).expect("reservation result must serialize");
    let decoded: IdentityResolution =
        decode_project_json(&bytes).expect("reservation result must deserialize");
    assert_eq!(decoded, reserved);

    let identity = ProjectIdentityRecord {
        schema_version: ProjectContractVersion::V1,
        project_id: project_id(),
        worktree_id: worktree_id(),
        revalidated_match_facts_digest: digest('b'),
        state: IdentityRecordState::Active,
    };
    assert_eq!(
        decode_project_json::<ProjectIdentityRecord>(
            &canonical_project_json(&identity).expect("identity must serialize")
        )
        .expect("identity must deserialize"),
        identity
    );

    let candidates = vec![project_id(); MAX_IDENTITY_CANDIDATES + 1];
    assert!(matches!(
        IdentityCandidateList::try_from(candidates),
        Err(ContractValueError::ItemsTooMany { .. })
    ));

    let busy = IdentityResolution::Busy {
        scope: StoreLockScope::IdentityCatalog,
    };
    assert_eq!(
        decode_project_json::<IdentityResolution>(
            &canonical_project_json(&busy).expect("busy result must serialize")
        )
        .expect("busy result must deserialize"),
        busy
    );
}

#[test]
fn evidence_generation_and_current_reference_preserve_authenticity_limitation() {
    let evidence = EvidenceEnvelope {
        schema_version: ProjectContractVersion::V1,
        record_id: record_id("r_locator"),
        record_kind: EvidenceRecordKind::ProjectLocator,
        project_id: project_id(),
        producer: ProducerId::try_from("wepld.project_locator")
            .expect("fixture producer id must be valid"),
        producer_contract_version: 1,
        observed_at: UnixMillis::new(20),
        freshness_basis: FreshnessBasis::FilesystemMetadata,
        payload_digest: digest('c'),
        provenance: EvidenceProvenance {
            source: ProvenanceSource::FilesystemObservation,
            parent_record_id: None,
        },
        status: EvidenceStatus::Complete,
        payload: locator(),
    };
    let evidence_bytes = canonical_project_json(&evidence).expect("evidence must serialize");
    let decoded: EvidenceEnvelope<ProjectLocator> =
        decode_project_json(&evidence_bytes).expect("evidence must deserialize");
    assert_eq!(decoded, evidence);

    let manifest = ProjectGenerationManifest {
        schema_version: ProjectContractVersion::V1,
        generation_id: generation_id(),
        project_id: project_id(),
        identity_record_ref: record_id("r_identity"),
        index_record_ref: record_id("r_index"),
        evidence_record_refs: EvidenceRecordRefs::try_from(vec![record_id("r_locator")])
            .expect("fixture evidence refs must fit"),
        record_digests: RecordDigestList::try_from(vec![RecordDigest {
            record_id: record_id("r_locator"),
            digest: digest('d'),
        }])
        .expect("fixture digest list must fit"),
        producer_contract_version: 1,
        created_at: UnixMillis::new(21),
        authenticity: StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly,
    };
    let manifest_bytes = canonical_project_json(&manifest).expect("manifest must serialize");
    let manifest_decoded: ProjectGenerationManifest =
        decode_project_json(&manifest_bytes).expect("manifest must deserialize");
    assert_eq!(manifest_decoded, manifest);
    assert_eq!(
        manifest_decoded.authenticity,
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    );

    let current = ProjectCurrentRef {
        schema_version: ProjectContractVersion::V1,
        project_id: project_id(),
        generation_id: generation_id(),
        manifest_digest: digest('e'),
    };
    assert_eq!(
        decode_project_json::<ProjectCurrentRef>(
            &canonical_project_json(&current).expect("CURRENT reference must serialize")
        )
        .expect("CURRENT reference must deserialize"),
        current
    );
}

#[test]
fn doctor_report_uses_only_closed_safe_parameters() {
    let report = DoctorReport {
        schema_version: ProjectContractVersion::V1,
        project_id: project_id(),
        selected_generation_id: Some(generation_id()),
        evaluated_at: UnixMillis::new(30),
        findings: DoctorFindingList::try_from(vec![safe_finding()])
            .expect("fixture finding list must fit"),
    };
    let bytes = canonical_project_json(&report).expect("doctor report must serialize");
    let decoded: DoctorReport =
        decode_project_json(&bytes).expect("doctor report must deserialize");
    assert_eq!(decoded, report);
    let text = String::from_utf8(bytes).expect("canonical JSON is UTF-8");
    assert!(text.contains("\\u{a}"));
    assert!(!text.contains('\n'));
}

#[test]
fn command_envelopes_cover_required_machine_error_classes() {
    let required = [
        ProjectErrorCode::IdentityAmbiguous,
        ProjectErrorCode::IdentityCatalogBusy,
        ProjectErrorCode::StoreBusy,
        ProjectErrorCode::CapabilityUnavailable,
        ProjectErrorCode::EvidenceCorrupt,
    ];

    for code in required {
        let class = match code {
            ProjectErrorCode::EvidenceCorrupt => ProjectErrorClass::EvidenceStoreIntegrity,
            ProjectErrorCode::CapabilityUnavailable => ProjectErrorClass::CapabilityUnavailable,
            _ => ProjectErrorClass::ProjectResolutionIdentity,
        };
        let envelope: ProjectCommandEnvelope<()> = ProjectCommandEnvelope::Error {
            schema_version: ProjectContractVersion::V1,
            command: ProjectCommand::Doctor,
            error: ProjectCommandError {
                class,
                code,
                safe_parameters: SafeParameterList::try_from(Vec::new())
                    .expect("empty safe parameter list must fit"),
            },
        };
        let bytes = canonical_project_json(&envelope).expect("command error must serialize");
        let decoded: ProjectCommandEnvelope<()> =
            decode_project_json(&bytes).expect("command error must deserialize");
        assert_eq!(decoded, envelope);
    }
}

#[test]
fn canonical_json_is_deterministic_and_bounded() {
    let value = json!({
        "z": 1,
        "a": {"z": 2, "a": 3},
        "m": [
            {"z": 4, "a": 5}
        ]
    });
    let first = canonical_project_json(&value).expect("value must serialize");
    let second = canonical_project_json(&value).expect("value must serialize deterministically");
    assert_eq!(first, second);
    assert_eq!(
        String::from_utf8(first).expect("canonical JSON is UTF-8"),
        r#"{"a":{"a":3,"z":2},"m":[{"a":5,"z":4}],"z":1}"#
    );

    let oversized = "x".repeat(MAX_PROJECT_CONTRACT_JSON_BYTES + 1);
    assert!(matches!(
        canonical_project_json(&oversized),
        Err(ProjectContractCodecError::PayloadTooLarge { .. })
    ));
    let oversized_wire = vec![b'x'; MAX_PROJECT_CONTRACT_JSON_BYTES + 1];
    assert!(matches!(
        decode_project_json::<String>(&oversized_wire),
        Err(ProjectContractCodecError::PayloadTooLarge { .. })
    ));

    assert!(matches!(
        MachinePath::unix_bytes(vec![0; MAX_MACHINE_PATH_BYTES + 1]),
        Err(ContractValueError::MachinePathTooLong { .. })
    ));
}

#[test]
fn c009_raw_secret_bearing_text_cannot_enter_safe_parameter_contract() {
    let secret = "https://user:supersecret@example.invalid/repo?token=supersecret";
    let finding = json!({
        "finding_code": "D-SEC-001",
        "severity": "blocking",
        "category": "security_sensitive_config",
        "summary_template_id": "tpl.doctor.security.summary",
        "explanation_template_id": "tpl.doctor.security.explanation",
        "observed_evidence_refs": [],
        "remediation_kind": "manual_action",
        "remediation_template_id": "tpl.doctor.security.remediation",
        "machine_action_hint": null,
        "safe_parameters": [
            {"kind": "raw_text", "value": secret}
        ]
    });
    assert!(serde_json::from_value::<DoctorFinding>(finding).is_err());

    let unsafe_path_parameter = json!({"kind": "path", "value": secret});
    assert!(serde_json::from_value::<SafeParameter>(unsafe_path_parameter).is_err());

    let redacted = MachinePath::utf8(secret)
        .expect("secret-shaped fixture must fit machine path contract")
        .safe_display();
    assert_eq!(
        redacted.as_str(),
        "https://<redacted>@example.invalid/repo?<redacted>"
    );
    assert!(!redacted.as_str().contains("supersecret"));

    let safe_path_parameter = SafeParameter::Path { value: redacted };
    let safe_path_json = String::from_utf8(
        canonical_project_json(&safe_path_parameter).expect("safe path parameter must serialize"),
    )
    .expect("canonical JSON is UTF-8");
    assert!(!safe_path_json.contains("supersecret"));

    let safe = safe_finding();
    let encoded =
        String::from_utf8(canonical_project_json(&safe).expect("safe finding must serialize"))
            .expect("canonical JSON is UTF-8");
    assert!(!encoded.contains("supersecret"));
    assert!(!encoded.contains("raw_text"));
}
