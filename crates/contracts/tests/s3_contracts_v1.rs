//! S3-AUTH-C contract tests (C001..C013).
//!
//! These tests exercise the public contract surface only. They construct no
//! host behavior: every assertion is about construction rules, closed enums,
//! fail-closed defaults and schema round trips.

use serde::de::DeserializeOwned;
use wepld_contracts::s3::{
    AllowlistedEvidenceField, CapabilityDimension, CapabilityState, CeilingIntersection,
    ContainmentCapabilityReport, ContainmentPosture, DependencyState, DimensionReport,
    EffectDependency, EffectKind, EffectOutcome, EffectProposal, EffectResult,
    EnvironmentExposurePolicy, EnvironmentKey, EnvironmentValueCarrier, EvidenceKey,
    FilesystemIsolation, HostDescriptor, HostExecutionOptInState, Identifier, NetworkIsolation,
    NetworkState, PepDecision, PepOutcome, PlatformClass, ProcessTreeIdentity, ProcessTreeScope,
    RunnerDescriptor, RuntimeCeiling, S3_SCHEMA_VERSION, ServerDescriptor,
};

fn id(value: &str) -> Identifier {
    Identifier::new(value).expect("test identifier is valid")
}

fn evidence(key: EvidenceKey, value: &str) -> AllowlistedEvidenceField {
    AllowlistedEvidenceField::new(key, value).expect("test evidence value is valid")
}

fn proposal() -> EffectProposal {
    EffectProposal::new(
        id("effect-1"),
        EffectKind::FilesystemRead,
        id("target-1"),
        RuntimeCeiling::unbounded().with_wall_ms(1_000),
        EnvironmentExposurePolicy::new(Vec::new()),
    )
}

/// Insert one extra field into a JSON object literal.
fn with_extra_field(base: &str, extra: &str) -> String {
    let trimmed = base.trim_end();
    let without_close = trimmed
        .strip_suffix('}')
        .expect("test fixture is a JSON object");
    let separator = if without_close.trim_end().ends_with('{') {
        ""
    } else {
        ","
    };
    format!("{without_close}{separator}{extra}}}")
}

fn rejects<T: DeserializeOwned>(payload: &str) -> bool {
    serde_json::from_str::<T>(payload).is_err()
}

#[test]
fn c001_server_descriptor_round_trips_and_rejects_unknown_fields() {
    let descriptor = ServerDescriptor::new(
        id("server-1"),
        3,
        vec![id("cap.a"), id("cap.b")],
        1_772_000_000_000,
    )
    .expect("descriptor constructs");

    let encoded = serde_json::to_string(&descriptor).expect("serializes");
    let decoded: ServerDescriptor = serde_json::from_str(&encoded).expect("round trips");
    assert_eq!(decoded, descriptor);
    assert_eq!(decoded.schema_version, S3_SCHEMA_VERSION);

    assert!(rejects::<ServerDescriptor>(&with_extra_field(
        &encoded,
        "\"unexpected_capability\":\"cap.c\""
    )));
}

#[test]
fn c001_duplicate_capabilities_are_rejected() {
    let result = ServerDescriptor::new(id("server-1"), 3, vec![id("cap.a"), id("cap.a")], 0);
    assert!(result.is_err());
}

#[test]
fn c002_host_opt_in_defaults_false_and_is_never_implicit() {
    let descriptor = HostDescriptor::new(id("host-1"), PlatformClass::WindowsX64);
    assert_eq!(
        descriptor.host_execution_opt_in_state(),
        HostExecutionOptInState::NotOptedIn
    );
    assert!(descriptor.host_execution_opt_in_evidence().is_none());

    let without_field = r#"{"schema_version":1,"host_id":"host-1","platform":"WINDOWS_X64"}"#;
    let decoded: HostDescriptor = serde_json::from_str(without_field).expect("defaults apply");
    assert_eq!(
        decoded.host_execution_opt_in_state(),
        HostExecutionOptInState::NotOptedIn
    );

    let opt_in_without_evidence = r#"{"schema_version":1,"host_id":"host-1","platform":"WINDOWS_X64","host_execution_opt_in_state":"OPTED_IN"}"#;
    assert!(rejects::<HostDescriptor>(opt_in_without_evidence));

    let wrong_key = HostDescriptor::new(id("host-1"), PlatformClass::WindowsX64)
        .opt_in(evidence(EvidenceKey::EffectAuthorization, "record-1"));
    assert!(wrong_key.is_err());

    let explicit = HostDescriptor::new(id("host-1"), PlatformClass::WindowsX64)
        .opt_in(evidence(EvidenceKey::HostExecutionOptIn, "record-1"))
        .expect("explicit opt-in with evidence");
    assert_eq!(
        explicit.host_execution_opt_in_state(),
        HostExecutionOptInState::OptedInExplicitly
    );
}

#[test]
fn c003_runner_network_state_is_fixed_none() {
    let runner = RunnerDescriptor::new(
        id("runner-1"),
        PlatformClass::WindowsX64,
        ContainmentCapabilityReport::new(id("runner-1")),
        RuntimeCeiling::unbounded(),
    );
    assert_eq!(runner.current_network_state, NetworkState::None);

    let encoded = serde_json::to_string(&runner).expect("serializes");
    assert!(encoded.contains("\"current_network_state\":\"NONE\""));
    assert!(rejects::<RunnerDescriptor>(&encoded.replace(
        "\"current_network_state\":\"NONE\"",
        "\"current_network_state\":\"ALLOW\""
    )));
    assert!(rejects::<NetworkState>("\"ALLOW\""));
}

#[test]
fn c004_process_tree_identity_requires_both_fields() {
    let first = ProcessTreeIdentity::new(4_242, 100);
    let same = ProcessTreeIdentity::new(4_242, 100);
    let recycled = ProcessTreeIdentity::new(4_242, 101);

    assert_eq!(first, same);
    assert!(first.matches(&same));
    assert_ne!(first, recycled);
    assert!(!first.matches(&recycled));

    assert!(rejects::<ProcessTreeIdentity>(r#"{"os_process_id":4242}"#));
    assert!(rejects::<ProcessTreeIdentity>(
        r#"{"os_process_id":4242,"os_process_start_time":100,"os_process_name":"cmd"}"#
    ));
}

#[test]
fn c005_capability_report_proves_nothing_by_default() {
    let report = ContainmentCapabilityReport::new(id("runner-1"))
        .with_unsupported(CapabilityDimension::NetworkIsolation);
    assert!(!report.proves_any_dimension());
    assert_eq!(
        report.state_of(CapabilityDimension::NetworkIsolation),
        CapabilityState::NotProven
    );
    assert_eq!(
        report.state_of(CapabilityDimension::ProcessTreeOwnership),
        CapabilityState::NotProven
    );
    assert_eq!(
        report.unsupported(),
        &[CapabilityDimension::NetworkIsolation]
    );

    let proven_without_evidence = DimensionReport::new(
        CapabilityDimension::FilesystemIsolation,
        CapabilityState::Proven,
        None,
    );
    assert!(proven_without_evidence.is_err());

    let proven = DimensionReport::new(
        CapabilityDimension::FilesystemIsolation,
        CapabilityState::Proven,
        Some(evidence(EvidenceKey::ContainmentQualification, "run-1")),
    )
    .expect("proven with evidence");

    let report = report.with_dimension(proven).expect("dimension added");
    assert!(report.proves_any_dimension());
    assert_eq!(
        report.state_of(CapabilityDimension::ProcessTreeOwnership),
        CapabilityState::NotProven
    );
}

#[test]
fn c006_containment_dimensions_are_independent() {
    let posture = ContainmentPosture::new().with_process_tree(ProcessTreeScope::OwnedTreeOnly);
    assert_eq!(posture.process_tree, ProcessTreeScope::OwnedTreeOnly);
    assert_eq!(posture.filesystem, FilesystemIsolation::NotEstablished);
    assert_eq!(posture.network, NetworkIsolation::NotEstablished);
    assert!(!posture.is_entirely_unestablished());

    let posture = posture.with_filesystem(FilesystemIsolation::ScopedRoot);
    assert_eq!(posture.network, NetworkIsolation::NotEstablished);

    let posture = posture.with_network(NetworkIsolation::NoNetwork);
    assert_eq!(posture.process_tree, ProcessTreeScope::OwnedTreeOnly);

    assert!(ContainmentPosture::new().is_entirely_unestablished());
    assert!(rejects::<ContainmentPosture>(
        r#"{"process_tree":"OWNED_TREE_ONLY","filesystem":"NOT_ESTABLISHED","network":"NOT_ESTABLISHED","isolation":"STRONG"}"#
    ));
}

#[test]
fn c007_ceiling_intersection_is_tightest_and_blocks_on_empty() {
    let left = RuntimeCeiling::unbounded()
        .with_wall_ms(1_000)
        .with_output_bytes(4_096);
    let right = RuntimeCeiling::unbounded()
        .with_wall_ms(500)
        .with_effect_count(3);

    match left.intersect(&right) {
        CeilingIntersection::Ceiling(ceiling) => {
            assert_eq!(ceiling.max_wall_ms, Some(500));
            assert_eq!(ceiling.max_output_bytes, Some(4_096));
            assert_eq!(ceiling.max_effect_count, Some(3));
        }
        CeilingIntersection::Blocked => panic!("tightest intersection is not blocked"),
    }

    let unbounded = RuntimeCeiling::unbounded();
    match left.intersect(&unbounded) {
        CeilingIntersection::Ceiling(ceiling) => assert_eq!(ceiling, left),
        CeilingIntersection::Blocked => panic!("unbounded intersection is not blocked"),
    }

    assert_eq!(
        left.intersect(&RuntimeCeiling::blocked()),
        CeilingIntersection::Blocked
    );
    assert_eq!(
        unbounded.intersect(&RuntimeCeiling::unbounded().with_wall_ms(0)),
        CeilingIntersection::Blocked
    );
}

#[test]
fn c008_environment_policy_names_keys_and_never_carries_raw_values() {
    let key = EnvironmentKey::new("PATH").expect("upper-case key name is accepted");
    assert_eq!(key.as_str(), "PATH");
    assert!(EnvironmentKey::new("PATH=/usr/bin").is_err());
    assert!(EnvironmentKey::new("lower").is_err());
    assert!(EnvironmentKey::new("").is_err());

    let policy = EnvironmentExposurePolicy::new(vec![key]);
    assert_eq!(policy.value_carrier(), EnvironmentValueCarrier::NoValues);
    assert!(policy.evidence().is_none());

    let with_wrong_key = EnvironmentExposurePolicy::new(Vec::new())
        .with_allowlisted_evidence(evidence(EvidenceKey::OutputDigest, "digest"));
    assert!(with_wrong_key.is_err());

    let with_evidence = EnvironmentExposurePolicy::new(Vec::new())
        .with_allowlisted_evidence(evidence(EvidenceKey::EnvironmentDeclaration, "declared"))
        .expect("declared evidence is accepted");
    assert_eq!(
        with_evidence.value_carrier(),
        EnvironmentValueCarrier::AllowlistedEvidence
    );

    assert!(rejects::<EnvironmentExposurePolicy>(
        r#"{"schema_version":1,"exposed_keys":["PATH"],"value_carrier":"NO_VALUES","evidence":{"key":"ENVIRONMENT_DECLARATION","value":"declared"}}"#
    ));
    assert!(rejects::<EnvironmentExposurePolicy>(
        r#"{"schema_version":1,"exposed_keys":["PATH=/usr/bin"],"value_carrier":"NO_VALUES"}"#
    ));
}

#[test]
fn c009_effect_kind_is_closed_and_unknown_values_are_construction_errors() {
    let encoded = serde_json::to_string(&proposal()).expect("serializes");
    let decoded: EffectProposal = serde_json::from_str(&encoded).expect("round trips");
    assert_eq!(decoded.proposed_effect_kind(), EffectKind::FilesystemRead);

    let unknown_kind = encoded.replace("\"FILESYSTEM_READ\"", "\"TELEPORT\"");
    assert!(rejects::<EffectProposal>(&unknown_kind));
    assert!(rejects::<EffectKind>("\"TELEPORT\""));
    assert!(rejects::<EffectProposal>(&with_extra_field(
        &encoded,
        "\"effect_class\":\"EXTRA\""
    )));
}

#[test]
fn c010_default_and_missing_input_are_unknown_fail_closed() {
    let default = PepDecision::missing_input();
    assert_eq!(default.decision(), PepOutcome::UnknownFailClosed);
    assert_ne!(default.decision(), PepOutcome::Allow);

    let decoded: PepDecision = serde_json::from_str("{}").expect("empty input deserializes");
    assert_eq!(decoded.decision(), PepOutcome::UnknownFailClosed);

    let no_proposal = PepDecision::evaluate(
        None,
        Some(evidence(EvidenceKey::EffectAuthorization, "grant-1")),
    );
    assert_eq!(no_proposal.decision(), PepOutcome::UnknownFailClosed);

    let no_evidence = PepDecision::evaluate(Some(&proposal()), None);
    assert_eq!(no_evidence.decision(), PepOutcome::UnknownFailClosed);

    let wrong_key = PepDecision::evaluate(
        Some(&proposal()),
        Some(evidence(EvidenceKey::OutputDigest, "grant-1")),
    );
    assert_eq!(wrong_key.decision(), PepOutcome::UnknownFailClosed);

    let allowed = PepDecision::evaluate(
        Some(&proposal()),
        Some(evidence(EvidenceKey::EffectAuthorization, "grant-1")),
    );
    assert_eq!(allowed.decision(), PepOutcome::Allow);

    assert!(rejects::<PepDecision>(r#"{"decision":"ALLOW"}"#));
}

#[test]
fn c011_executed_requires_a_referenced_allow_decision() {
    let decision_allowed = PepDecision::evaluate(
        Some(&proposal()),
        Some(evidence(EvidenceKey::EffectAuthorization, "grant-1")),
    );
    let executed = EffectResult::new(id("effect-1"), EffectOutcome::Executed, decision_allowed)
        .expect("executed with allow");
    assert_eq!(executed.outcome(), EffectOutcome::Executed);

    let denied = EffectResult::new(
        id("effect-1"),
        EffectOutcome::Executed,
        PepDecision::missing_input(),
    );
    assert!(denied.is_err());

    let refused = EffectResult::new(
        id("effect-1"),
        EffectOutcome::Refused,
        PepDecision::missing_input(),
    )
    .expect("a refusal is constructible without allow");
    assert_eq!(refused.outcome(), EffectOutcome::Refused);

    let executed_json = serde_json::to_string(&executed).expect("serializes");
    let decoded: EffectResult = serde_json::from_str(&executed_json).expect("round trips");
    assert_eq!(decoded.outcome(), EffectOutcome::Executed);

    let without_decision = r#"{"schema_version":1,"effect_id":"effect-1","outcome":"EXECUTED","decision":{"decision":"UNKNOWN_FAIL_CLOSED"}}"#;
    assert!(rejects::<EffectResult>(without_decision));

    let with_unknown_allow = r#"{"schema_version":1,"effect_id":"effect-1","outcome":"EXECUTED","decision":{"decision":"ALLOW"}}"#;
    assert!(rejects::<EffectResult>(with_unknown_allow));

    assert!(rejects::<EffectOutcome>("\"PARTIAL\""));
}

#[test]
fn c012_dependency_blocking_rules_and_self_dependency() {
    let dependency =
        EffectDependency::new(id("effect-1"), id("effect-2")).expect("valid dependency");
    assert_eq!(dependency.prerequisite().as_str(), "effect-1");
    assert_eq!(dependency.dependent().as_str(), "effect-2");

    assert_eq!(
        dependency.evaluate(None),
        DependencyState::UnknownFailClosed
    );
    assert_eq!(
        dependency.evaluate(Some(EffectOutcome::Executed)),
        DependencyState::Ready
    );
    assert_eq!(
        dependency.evaluate(Some(EffectOutcome::Refused)),
        DependencyState::BlockedOnFailedPrerequisite
    );
    assert_eq!(
        dependency.evaluate(Some(EffectOutcome::Failed)),
        DependencyState::BlockedOnFailedPrerequisite
    );
    assert_eq!(
        dependency.evaluate(Some(EffectOutcome::Unknown)),
        DependencyState::BlockedOnPrerequisite
    );

    assert!(EffectDependency::new(id("effect-1"), id("effect-1")).is_err());
    assert!(rejects::<EffectDependency>(
        r#"{"prerequisite":"effect-1","dependent":"effect-1"}"#
    ));
}

#[test]
fn c013_no_contract_accepts_raw_environment_or_output_content() {
    // Every contract type denies unknown fields, so a raw content payload is a
    // reconstruction error rather than a silent pass-through.
    let server = serde_json::to_string(
        &ServerDescriptor::new(id("server-1"), 3, vec![id("cap.a")], 0).expect("descriptor"),
    )
    .expect("serializes");
    let host = serde_json::to_string(&HostDescriptor::new(
        id("host-1"),
        PlatformClass::WindowsX64,
    ))
    .expect("serializes");
    let env_policy =
        serde_json::to_string(&EnvironmentExposurePolicy::new(Vec::new())).expect("serializes");
    let effect = serde_json::to_string(&proposal()).expect("serializes");
    let decision = serde_json::to_string(&PepDecision::missing_input()).expect("serializes");
    let result = serde_json::to_string(
        &EffectResult::new(
            id("effect-1"),
            EffectOutcome::Refused,
            PepDecision::missing_input(),
        )
        .expect("refusal result"),
    )
    .expect("serializes");
    let dependency = serde_json::to_string(
        &EffectDependency::new(id("effect-1"), id("effect-2")).expect("dependency"),
    )
    .expect("serializes");

    let raw_fields = [
        "\"environment_value\":\"RAW\"",
        "\"process_output\":\"RAW\"",
        "\"raw_output\":\"RAW\"",
        "\"secret\":\"RAW\"",
    ];

    for extra in raw_fields {
        assert!(
            rejects::<ServerDescriptor>(&with_extra_field(&server, extra)),
            "ServerDescriptor accepted {extra}"
        );
        assert!(
            rejects::<HostDescriptor>(&with_extra_field(&host, extra)),
            "HostDescriptor accepted {extra}"
        );
        assert!(
            rejects::<EnvironmentExposurePolicy>(&with_extra_field(&env_policy, extra)),
            "EnvironmentExposurePolicy accepted {extra}"
        );
        assert!(
            rejects::<EffectProposal>(&with_extra_field(&effect, extra)),
            "EffectProposal accepted {extra}"
        );
        assert!(
            rejects::<PepDecision>(&with_extra_field(&decision, extra)),
            "PepDecision accepted {extra}"
        );
        assert!(
            rejects::<EffectResult>(&with_extra_field(&result, extra)),
            "EffectResult accepted {extra}"
        );
        assert!(
            rejects::<EffectDependency>(&with_extra_field(&dependency, extra)),
            "EffectDependency accepted {extra}"
        );
    }

    // The single allowlisted carrier itself rejects secret-shaped, unbounded
    // and control-bearing values.
    assert!(AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "ghp_0123456789").is_err());
    assert!(
        AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "-----BEGIN PRIVATE KEY-----")
            .is_err()
    );
    assert!(AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "").is_err());
    assert!(AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "a".repeat(129)).is_err());
    assert!(AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "with\u{0}nul").is_err());
    assert!(AllowlistedEvidenceField::new(EvidenceKey::OutputDigest, "sha256:abc").is_ok());

    // Evidence keys are a closed allowlist, so an unlisted carrier key is a
    // construction error.
    assert!(rejects::<AllowlistedEvidenceField>(
        r#"{"key":"RAW_CONTENT","value":"anything"}"#
    ));
}

#[test]
fn contract_errors_are_reachable_only_as_rejections() {
    assert!(Identifier::new("").is_err());
    assert!(Identifier::new("a".repeat(129)).is_err());
    assert!(Identifier::new("has space").is_err());
    assert!(Identifier::new("ok.identifier:1").is_ok());
}
