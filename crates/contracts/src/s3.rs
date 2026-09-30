//! WePLD S3-AUTH-C pure contracts (C001..C013).
//!
//! Every type in this module is a plain data contract with fail-closed
//! construction rules. The module declares no host, filesystem, network,
//! process, credential or containment behavior, and it adds no dependency:
//! it uses only `serde` and the language prelude.
//!
//! Fail-closed rules enforced here rather than by convention:
//!
//! - identifiers are bounded and charset-checked, so a contract cannot carry
//!   unbounded free text through an identifier field;
//! - environment and output-shaped content is reachable only through
//!   [`AllowlistedEvidenceField`], whose value is bounded, NUL-free and
//!   screened against secret-shaped values;
//! - every contract type denies unknown fields, so a raw payload dressed as a
//!   new field is a deserialization error rather than a silent pass-through;
//! - closed enums reject unrecognized values at construction time;
//! - the default decision path is `UNKNOWN_FAIL_CLOSED` and never `ALLOW`;
//! - `EXECUTED` cannot be constructed without a referenced `ALLOW` decision;
//! - a `PROVEN` capability requires evidence, and a blocked ceiling
//!   intersection blocks instead of widening.

use core::fmt;

use serde::{Deserialize, Serialize};

/// Schema version shared by every contract type in this module.
pub const S3_SCHEMA_VERSION: u16 = 1;

/// Maximum accepted byte length of any identifier field.
pub const MAX_IDENTIFIER_BYTES: usize = 128;

/// Maximum accepted byte length of an allowlisted evidence value.
pub const MAX_EVIDENCE_VALUE_BYTES: usize = 128;

/// Construction failures for S3 contract types.
///
/// Every variant is a rejection. There is no variant that means "accept with a
/// caveat", because a caveat that is not represented as data cannot be checked.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ContractError {
    EmptyIdentifier,
    IdentifierTooLong,
    IdentifierCharset,
    UnsupportedSchemaVersion,
    DuplicateIdentifier,
    EvidenceValueEmpty,
    EvidenceValueTooLong,
    EvidenceValueControlCharacter,
    EvidenceValueSecretShaped,
    ProvenRequiresEvidence,
    EvidenceWithoutCarrier,
    CarrierWithoutEvidence,
    EnvironmentKeyMalformed,
    EnvironmentKeyCarriesValue,
    OptInRequiresEvidence,
    ExecutedWithoutAllow,
    AllowRequiresEvidence,
    SelfDependency,
    LimitNotDeclared,
}

impl fmt::Display for ContractError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::EmptyIdentifier => "identifier must not be empty",
            Self::IdentifierTooLong => "identifier exceeds the accepted byte length",
            Self::IdentifierCharset => "identifier contains a character outside the accepted set",
            Self::UnsupportedSchemaVersion => "schema version is not the supported version",
            Self::DuplicateIdentifier => "identifier is repeated where uniqueness is required",
            Self::EvidenceValueEmpty => "evidence value must not be empty",
            Self::EvidenceValueTooLong => "evidence value exceeds the accepted byte length",
            Self::EvidenceValueControlCharacter => {
                "evidence value contains a control character or NUL"
            }
            Self::EvidenceValueSecretShaped => "evidence value is shaped like secret material",
            Self::ProvenRequiresEvidence => "a proven capability requires referenced evidence",
            Self::EvidenceWithoutCarrier => {
                "evidence was supplied by a carrier that does not accept evidence"
            }
            Self::CarrierWithoutEvidence => {
                "the declared carrier requires an evidence field that is missing"
            }
            Self::EnvironmentKeyMalformed => "environment key is not a bounded upper-case name",
            Self::EnvironmentKeyCarriesValue => {
                "environment key carries an inline value instead of naming a key"
            }
            Self::OptInRequiresEvidence => "host execution opt-in requires explicit evidence",
            Self::ExecutedWithoutAllow => "EXECUTED requires a referenced ALLOW decision",
            Self::AllowRequiresEvidence => "ALLOW requires referenced evidence",
            Self::SelfDependency => "an effect cannot depend on itself",
            Self::LimitNotDeclared => "a declared ceiling is required for this operation",
        };
        formatter.write_str(text)
    }
}

/// A bounded, charset-checked identifier.
///
/// The accepted set is ASCII alphanumerics plus `.`, `_`, `-`, `:` and `/`.
/// Anything else, an empty value or an over-long value is rejected, so no
/// identifier field can become an unbounded free-text channel.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(try_from = "String")]
pub struct Identifier(String);

impl Identifier {
    pub fn new(value: impl Into<String>) -> Result<Self, ContractError> {
        let value = value.into();
        if value.is_empty() {
            return Err(ContractError::EmptyIdentifier);
        }
        if value.len() > MAX_IDENTIFIER_BYTES {
            return Err(ContractError::IdentifierTooLong);
        }
        if !value.bytes().all(|byte| {
            byte.is_ascii_alphanumeric() || matches!(byte, b'.' | b'_' | b'-' | b':' | b'/')
        }) {
            return Err(ContractError::IdentifierCharset);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl TryFrom<String> for Identifier {
    type Error = ContractError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

/// Server identity (S3-C001).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ServerDescriptor {
    pub schema_version: u16,
    pub server_id: Identifier,
    pub protocol_version: u32,
    pub declared_capabilities: Vec<Identifier>,
    pub issued_at_unix_ms: u64,
}

impl ServerDescriptor {
    pub fn new(
        server_id: Identifier,
        protocol_version: u32,
        declared_capabilities: Vec<Identifier>,
        issued_at_unix_ms: u64,
    ) -> Result<Self, ContractError> {
        let mut seen: Vec<&Identifier> = Vec::new();
        for capability in &declared_capabilities {
            if seen.contains(&capability) {
                return Err(ContractError::DuplicateIdentifier);
            }
            seen.push(capability);
        }
        Ok(Self {
            schema_version: S3_SCHEMA_VERSION,
            server_id,
            protocol_version,
            declared_capabilities,
            issued_at_unix_ms,
        })
    }
}

/// Host platform class. `Unsupported` is an explicit value, not a silent absence.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum PlatformClass {
    WindowsX64,
    WindowsArm64,
    LinuxX64,
    MacosArm64,
    Unsupported,
}

/// Host execution opt-in state (S3-C002).
///
/// The default is `NOT_OPTED_IN`. Selecting `OPTED_IN` requires referenced
/// evidence, so no constructor path can set it implicitly.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum HostExecutionOptInState {
    #[default]
    NotOptedIn,
    OptedInExplicitly,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct HostDescriptorWire {
    schema_version: u16,
    host_id: Identifier,
    platform: PlatformClass,
    #[serde(default)]
    host_execution_opt_in_state: HostExecutionOptInState,
    #[serde(default)]
    host_execution_opt_in_evidence: Option<AllowlistedEvidenceField>,
}

/// Host descriptor (S3-C002). Fields are private; construction goes through
/// [`HostDescriptor::new`] or through validated deserialization.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "HostDescriptorWire", into = "HostDescriptorWire")]
pub struct HostDescriptor {
    schema_version: u16,
    host_id: Identifier,
    platform: PlatformClass,
    host_execution_opt_in_state: HostExecutionOptInState,
    host_execution_opt_in_evidence: Option<AllowlistedEvidenceField>,
}

impl HostDescriptor {
    /// The only constructor. It always produces `NOT_OPTED_IN`.
    pub fn new(host_id: Identifier, platform: PlatformClass) -> Self {
        Self {
            schema_version: S3_SCHEMA_VERSION,
            host_id,
            platform,
            host_execution_opt_in_state: HostExecutionOptInState::NotOptedIn,
            host_execution_opt_in_evidence: None,
        }
    }

    /// Explicit opt-in. Requires referenced evidence, so it cannot be implied.
    pub fn opt_in(mut self, evidence: AllowlistedEvidenceField) -> Result<Self, ContractError> {
        if evidence.key() != EvidenceKey::HostExecutionOptIn {
            return Err(ContractError::OptInRequiresEvidence);
        }
        self.host_execution_opt_in_state = HostExecutionOptInState::OptedInExplicitly;
        self.host_execution_opt_in_evidence = Some(evidence);
        Ok(self)
    }

    pub fn schema_version(&self) -> u16 {
        self.schema_version
    }

    pub fn host_id(&self) -> &Identifier {
        &self.host_id
    }

    pub fn platform(&self) -> PlatformClass {
        self.platform
    }

    pub fn host_execution_opt_in_state(&self) -> HostExecutionOptInState {
        self.host_execution_opt_in_state
    }

    pub fn host_execution_opt_in_evidence(&self) -> Option<&AllowlistedEvidenceField> {
        self.host_execution_opt_in_evidence.as_ref()
    }
}

impl TryFrom<HostDescriptorWire> for HostDescriptor {
    type Error = ContractError;

    fn try_from(wire: HostDescriptorWire) -> Result<Self, Self::Error> {
        if wire.schema_version != S3_SCHEMA_VERSION {
            return Err(ContractError::UnsupportedSchemaVersion);
        }
        match (
            wire.host_execution_opt_in_state,
            wire.host_execution_opt_in_evidence.as_ref(),
        ) {
            (HostExecutionOptInState::NotOptedIn, Some(_)) => {
                return Err(ContractError::EvidenceWithoutCarrier);
            }
            (HostExecutionOptInState::OptedInExplicitly, None) => {
                return Err(ContractError::OptInRequiresEvidence);
            }
            _ => {}
        }
        Ok(Self {
            schema_version: wire.schema_version,
            host_id: wire.host_id,
            platform: wire.platform,
            host_execution_opt_in_state: wire.host_execution_opt_in_state,
            host_execution_opt_in_evidence: wire.host_execution_opt_in_evidence,
        })
    }
}

impl From<HostDescriptor> for HostDescriptorWire {
    fn from(descriptor: HostDescriptor) -> Self {
        Self {
            schema_version: descriptor.schema_version,
            host_id: descriptor.host_id,
            platform: descriptor.platform,
            host_execution_opt_in_state: descriptor.host_execution_opt_in_state,
            host_execution_opt_in_evidence: descriptor.host_execution_opt_in_evidence,
        }
    }
}

/// Network state. The only representable value is `NONE`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum NetworkState {
    #[default]
    None,
}

/// Runner descriptor (S3-C003). `current_network_state` is fixed at `NONE` and
/// has no setter, so no construction path can represent another value.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunnerDescriptor {
    pub schema_version: u16,
    pub runner_id: Identifier,
    pub platform: PlatformClass,
    pub current_network_state: NetworkState,
    pub containment: ContainmentCapabilityReport,
    pub ceiling: RuntimeCeiling,
}

impl RunnerDescriptor {
    pub fn new(
        runner_id: Identifier,
        platform: PlatformClass,
        containment: ContainmentCapabilityReport,
        ceiling: RuntimeCeiling,
    ) -> Self {
        Self {
            schema_version: S3_SCHEMA_VERSION,
            runner_id,
            platform,
            current_network_state: NetworkState::None,
            containment,
            ceiling,
        }
    }
}

/// Process-tree identity (S3-C004).
///
/// Identity is the pair `(os_process_id, os_process_start_time)`. Matching uses
/// both fields, so a recycled process id does not match a previous identity.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProcessTreeIdentity {
    pub os_process_id: u32,
    pub os_process_start_time: u64,
}

impl ProcessTreeIdentity {
    pub fn new(os_process_id: u32, os_process_start_time: u64) -> Self {
        Self {
            os_process_id,
            os_process_start_time,
        }
    }

    /// True only when both fields match. A partial match is not a match.
    pub fn matches(&self, other: &Self) -> bool {
        self == other
    }
}

/// Capability state for one containment dimension.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum CapabilityState {
    #[default]
    NotProven,
    Proven,
    NotApplicable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum CapabilityDimension {
    ProcessTreeOwnership,
    FilesystemIsolation,
    NetworkIsolation,
    CredentialIsolation,
    DisplayCapture,
}

/// One dimension of a containment capability report. `PROVEN` requires evidence.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "DimensionReportWire")]
pub struct DimensionReport {
    dimension: CapabilityDimension,
    state: CapabilityState,
    evidence: Option<AllowlistedEvidenceField>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct DimensionReportWire {
    dimension: CapabilityDimension,
    #[serde(default)]
    state: CapabilityState,
    #[serde(default)]
    evidence: Option<AllowlistedEvidenceField>,
}

impl DimensionReport {
    pub fn new(
        dimension: CapabilityDimension,
        state: CapabilityState,
        evidence: Option<AllowlistedEvidenceField>,
    ) -> Result<Self, ContractError> {
        match (state, evidence.as_ref()) {
            (CapabilityState::Proven, None) => Err(ContractError::ProvenRequiresEvidence),
            (CapabilityState::NotProven, Some(_)) => Err(ContractError::EvidenceWithoutCarrier),
            (CapabilityState::NotApplicable, Some(_)) => Err(ContractError::EvidenceWithoutCarrier),
            _ => Ok(Self {
                dimension,
                state,
                evidence,
            }),
        }
    }

    pub fn dimension(&self) -> CapabilityDimension {
        self.dimension
    }

    pub fn state(&self) -> CapabilityState {
        self.state
    }

    pub fn evidence(&self) -> Option<&AllowlistedEvidenceField> {
        self.evidence.as_ref()
    }
}

impl TryFrom<DimensionReportWire> for DimensionReport {
    type Error = ContractError;

    fn try_from(wire: DimensionReportWire) -> Result<Self, Self::Error> {
        Self::new(wire.dimension, wire.state, wire.evidence)
    }
}

/// Containment capability report (S3-C005).
///
/// An absent dimension is absent from `dimensions` and named in `unsupported`;
/// it is never reported as proven. The default report proves nothing.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "ContainmentCapabilityReportWire")]
pub struct ContainmentCapabilityReport {
    schema_version: u16,
    runner_id: Identifier,
    dimensions: Vec<DimensionReport>,
    unsupported: Vec<CapabilityDimension>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct ContainmentCapabilityReportWire {
    #[serde(default = "default_schema_version")]
    schema_version: u16,
    runner_id: Identifier,
    #[serde(default)]
    dimensions: Vec<DimensionReport>,
    #[serde(default)]
    unsupported: Vec<CapabilityDimension>,
}

fn default_schema_version() -> u16 {
    S3_SCHEMA_VERSION
}

impl ContainmentCapabilityReport {
    pub fn new(runner_id: Identifier) -> Self {
        Self {
            schema_version: S3_SCHEMA_VERSION,
            runner_id,
            dimensions: Vec::new(),
            unsupported: Vec::new(),
        }
    }

    pub fn with_dimension(mut self, report: DimensionReport) -> Result<Self, ContractError> {
        if self
            .dimensions
            .iter()
            .any(|existing| existing.dimension() == report.dimension())
        {
            return Err(ContractError::DuplicateIdentifier);
        }
        self.dimensions.push(report);
        Ok(self)
    }

    pub fn with_unsupported(mut self, dimension: CapabilityDimension) -> Self {
        if !self.unsupported.contains(&dimension) {
            self.unsupported.push(dimension);
        }
        self
    }

    pub fn runner_id(&self) -> &Identifier {
        &self.runner_id
    }

    pub fn dimensions(&self) -> &[DimensionReport] {
        &self.dimensions
    }

    pub fn unsupported(&self) -> &[CapabilityDimension] {
        &self.unsupported
    }

    /// A dimension that has no report is not proven.
    pub fn state_of(&self, dimension: CapabilityDimension) -> CapabilityState {
        self.dimensions
            .iter()
            .find(|report| report.dimension() == dimension)
            .map_or(CapabilityState::NotProven, DimensionReport::state)
    }

    /// A report proves nothing until a dimension is explicitly `PROVEN`.
    pub fn proves_any_dimension(&self) -> bool {
        self.dimensions
            .iter()
            .any(|report| report.state() == CapabilityState::Proven)
    }
}

impl TryFrom<ContainmentCapabilityReportWire> for ContainmentCapabilityReport {
    type Error = ContractError;

    fn try_from(wire: ContainmentCapabilityReportWire) -> Result<Self, Self::Error> {
        if wire.schema_version != S3_SCHEMA_VERSION {
            return Err(ContractError::UnsupportedSchemaVersion);
        }
        let mut report = Self {
            schema_version: wire.schema_version,
            runner_id: wire.runner_id,
            dimensions: Vec::new(),
            unsupported: Vec::new(),
        };
        for dimension_report in wire.dimensions {
            report = report.with_dimension(dimension_report)?;
        }
        for dimension in wire.unsupported {
            report = report.with_unsupported(dimension);
        }
        Ok(report)
    }
}

/// Process-tree scope dimension (S3-C006). Independent of every other dimension.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum ProcessTreeScope {
    #[default]
    NotEstablished,
    OwnedTreeOnly,
}

/// Filesystem dimension (S3-C006). Independent of every other dimension.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum FilesystemIsolation {
    #[default]
    NotEstablished,
    ScopedRoot,
}

/// Network dimension (S3-C006). Independent of every other dimension.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum NetworkIsolation {
    #[default]
    NotEstablished,
    NoNetwork,
}

/// Containment posture (S3-C006).
///
/// Each strength dimension is set independently: establishing one dimension
/// never establishes another, so a process-tree-only fixture implies nothing
/// about filesystem or network posture.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ContainmentPosture {
    pub process_tree: ProcessTreeScope,
    pub filesystem: FilesystemIsolation,
    pub network: NetworkIsolation,
}

impl ContainmentPosture {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_process_tree(mut self, scope: ProcessTreeScope) -> Self {
        self.process_tree = scope;
        self
    }

    pub fn with_filesystem(mut self, isolation: FilesystemIsolation) -> Self {
        self.filesystem = isolation;
        self
    }

    pub fn with_network(mut self, isolation: NetworkIsolation) -> Self {
        self.network = isolation;
        self
    }

    /// True only when every dimension is still unestablished.
    pub fn is_entirely_unestablished(&self) -> bool {
        self.process_tree == ProcessTreeScope::NotEstablished
            && self.filesystem == FilesystemIsolation::NotEstablished
            && self.network == NetworkIsolation::NotEstablished
    }
}

/// A runtime ceiling (S3-C007).
///
/// `None` means "no ceiling declared for this dimension" and `Some(0)` means
/// "this dimension is blocked". Intersecting two ceilings takes the tighter
/// bound per dimension; if any dimension ends blocked, the intersection as a
/// whole is [`CeilingIntersection::Blocked`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RuntimeCeiling {
    pub max_wall_ms: Option<u64>,
    pub max_output_bytes: Option<u64>,
    pub max_effect_count: Option<u32>,
}

/// Result of intersecting two ceilings.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum CeilingIntersection {
    Blocked,
    Ceiling(RuntimeCeiling),
}

impl RuntimeCeiling {
    pub fn unbounded() -> Self {
        Self::default()
    }

    pub fn blocked() -> Self {
        Self {
            max_wall_ms: Some(0),
            max_output_bytes: Some(0),
            max_effect_count: Some(0),
        }
    }

    pub fn with_wall_ms(mut self, limit: u64) -> Self {
        self.max_wall_ms = Some(limit);
        self
    }

    pub fn with_output_bytes(mut self, limit: u64) -> Self {
        self.max_output_bytes = Some(limit);
        self
    }

    pub fn with_effect_count(mut self, limit: u32) -> Self {
        self.max_effect_count = Some(limit);
        self
    }

    /// Per-dimension tightening. A blocked dimension blocks the whole result.
    pub fn intersect(&self, other: &Self) -> CeilingIntersection {
        let wall = tightest_u64(self.max_wall_ms, other.max_wall_ms);
        let output = tightest_u64(self.max_output_bytes, other.max_output_bytes);
        let effects = tightest_u32(self.max_effect_count, other.max_effect_count);
        if wall == Some(0) || output == Some(0) || effects == Some(0) {
            return CeilingIntersection::Blocked;
        }
        CeilingIntersection::Ceiling(Self {
            max_wall_ms: wall,
            max_output_bytes: output,
            max_effect_count: effects,
        })
    }

    pub fn is_blocked(&self) -> bool {
        self.max_wall_ms == Some(0)
            || self.max_output_bytes == Some(0)
            || self.max_effect_count == Some(0)
    }
}

fn tightest_u64(left: Option<u64>, right: Option<u64>) -> Option<u64> {
    match (left, right) {
        (Some(a), Some(b)) => Some(a.min(b)),
        (Some(a), None) => Some(a),
        (None, Some(b)) => Some(b),
        (None, None) => None,
    }
}

fn tightest_u32(left: Option<u32>, right: Option<u32>) -> Option<u32> {
    match (left, right) {
        (Some(a), Some(b)) => Some(a.min(b)),
        (Some(a), None) => Some(a),
        (None, Some(b)) => Some(b),
        (None, None) => None,
    }
}

/// An environment key name (S3-C008).
///
/// This type names a key. It cannot carry a value: an inline `KEY=VALUE` pair,
/// a NUL, or a character outside the upper-case name set is rejected.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(try_from = "String")]
pub struct EnvironmentKey(String);

impl EnvironmentKey {
    pub fn new(value: impl Into<String>) -> Result<Self, ContractError> {
        let value = value.into();
        if value.is_empty() || value.len() > MAX_IDENTIFIER_BYTES {
            return Err(ContractError::EnvironmentKeyMalformed);
        }
        if value.bytes().any(|byte| matches!(byte, b'=' | b':' | 0)) {
            return Err(ContractError::EnvironmentKeyCarriesValue);
        }
        let mut characters = value.chars();
        let Some(first) = characters.next() else {
            return Err(ContractError::EnvironmentKeyMalformed);
        };
        if !first.is_ascii_uppercase() {
            return Err(ContractError::EnvironmentKeyMalformed);
        }
        if !characters.all(|character| {
            character.is_ascii_uppercase() || character == '_' || character.is_ascii_digit()
        }) {
            return Err(ContractError::EnvironmentKeyMalformed);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl TryFrom<String> for EnvironmentKey {
    type Error = ContractError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

/// How a policy carries environment content.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EnvironmentValueCarrier {
    /// No environment values are carried at all.
    #[default]
    NoValues,
    /// Only an allowlisted evidence field may carry a declared value.
    AllowlistedEvidence,
}

/// Environment exposure policy (S3-C008).
///
/// Exposed keys are names, never values. When the carrier is
/// `ALLOWLISTED_EVIDENCE`, exactly one allowlisted evidence field is required;
/// when the carrier is `NO_VALUES`, supplying evidence is an error.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "EnvironmentExposurePolicyWire")]
pub struct EnvironmentExposurePolicy {
    schema_version: u16,
    exposed_keys: Vec<EnvironmentKey>,
    value_carrier: EnvironmentValueCarrier,
    evidence: Option<AllowlistedEvidenceField>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct EnvironmentExposurePolicyWire {
    #[serde(default = "default_schema_version")]
    schema_version: u16,
    #[serde(default)]
    exposed_keys: Vec<EnvironmentKey>,
    #[serde(default)]
    value_carrier: EnvironmentValueCarrier,
    #[serde(default)]
    evidence: Option<AllowlistedEvidenceField>,
}

impl EnvironmentExposurePolicy {
    pub fn new(exposed_keys: Vec<EnvironmentKey>) -> Self {
        Self {
            schema_version: S3_SCHEMA_VERSION,
            exposed_keys,
            value_carrier: EnvironmentValueCarrier::NoValues,
            evidence: None,
        }
    }

    pub fn with_allowlisted_evidence(
        mut self,
        evidence: AllowlistedEvidenceField,
    ) -> Result<Self, ContractError> {
        if evidence.key() != EvidenceKey::EnvironmentDeclaration {
            return Err(ContractError::CarrierWithoutEvidence);
        }
        self.value_carrier = EnvironmentValueCarrier::AllowlistedEvidence;
        self.evidence = Some(evidence);
        Ok(self)
    }

    pub fn schema_version(&self) -> u16 {
        self.schema_version
    }

    pub fn exposed_keys(&self) -> &[EnvironmentKey] {
        &self.exposed_keys
    }

    pub fn value_carrier(&self) -> EnvironmentValueCarrier {
        self.value_carrier
    }

    pub fn evidence(&self) -> Option<&AllowlistedEvidenceField> {
        self.evidence.as_ref()
    }
}

impl TryFrom<EnvironmentExposurePolicyWire> for EnvironmentExposurePolicy {
    type Error = ContractError;

    fn try_from(wire: EnvironmentExposurePolicyWire) -> Result<Self, Self::Error> {
        if wire.schema_version != S3_SCHEMA_VERSION {
            return Err(ContractError::UnsupportedSchemaVersion);
        }
        match (wire.value_carrier, wire.evidence.as_ref()) {
            (EnvironmentValueCarrier::NoValues, Some(_)) => {
                Err(ContractError::EvidenceWithoutCarrier)
            }
            (EnvironmentValueCarrier::AllowlistedEvidence, None) => {
                Err(ContractError::CarrierWithoutEvidence)
            }
            (EnvironmentValueCarrier::AllowlistedEvidence, Some(evidence))
                if evidence.key() != EvidenceKey::EnvironmentDeclaration =>
            {
                Err(ContractError::CarrierWithoutEvidence)
            }
            _ => Ok(Self {
                schema_version: wire.schema_version,
                exposed_keys: wire.exposed_keys,
                value_carrier: wire.value_carrier,
                evidence: wire.evidence,
            }),
        }
    }
}

/// Closed effect-kind set (S3-C009).
///
/// An unrecognized value is a construction error, because this enum has no
/// catch-all variant and no `serde(other)` fallback.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EffectKind {
    FilesystemRead,
    FilesystemWrite,
    NetworkEgress,
    ProcessSpawn,
    CredentialAccess,
    DisplayOutput,
    ArtifactWrite,
}

/// Effect proposal (S3-C009).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "EffectProposalWire")]
pub struct EffectProposal {
    schema_version: u16,
    effect_id: Identifier,
    proposed_effect_kind: EffectKind,
    target: Identifier,
    ceiling: RuntimeCeiling,
    environment_exposure: EnvironmentExposurePolicy,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct EffectProposalWire {
    #[serde(default = "default_schema_version")]
    schema_version: u16,
    effect_id: Identifier,
    proposed_effect_kind: EffectKind,
    target: Identifier,
    #[serde(default)]
    ceiling: RuntimeCeiling,
    #[serde(default = "default_environment_policy")]
    environment_exposure: EnvironmentExposurePolicy,
}

fn default_environment_policy() -> EnvironmentExposurePolicy {
    EnvironmentExposurePolicy::new(Vec::new())
}

impl EffectProposal {
    pub fn new(
        effect_id: Identifier,
        proposed_effect_kind: EffectKind,
        target: Identifier,
        ceiling: RuntimeCeiling,
        environment_exposure: EnvironmentExposurePolicy,
    ) -> Self {
        Self {
            schema_version: S3_SCHEMA_VERSION,
            effect_id,
            proposed_effect_kind,
            target,
            ceiling,
            environment_exposure,
        }
    }

    pub fn effect_id(&self) -> &Identifier {
        &self.effect_id
    }

    pub fn proposed_effect_kind(&self) -> EffectKind {
        self.proposed_effect_kind
    }

    pub fn target(&self) -> &Identifier {
        &self.target
    }

    pub fn ceiling(&self) -> RuntimeCeiling {
        self.ceiling
    }

    pub fn environment_exposure(&self) -> &EnvironmentExposurePolicy {
        &self.environment_exposure
    }
}

impl TryFrom<EffectProposalWire> for EffectProposal {
    type Error = ContractError;

    fn try_from(wire: EffectProposalWire) -> Result<Self, Self::Error> {
        if wire.schema_version != S3_SCHEMA_VERSION {
            return Err(ContractError::UnsupportedSchemaVersion);
        }
        Ok(Self {
            schema_version: wire.schema_version,
            effect_id: wire.effect_id,
            proposed_effect_kind: wire.proposed_effect_kind,
            target: wire.target,
            ceiling: wire.ceiling,
            environment_exposure: wire.environment_exposure,
        })
    }
}

/// Policy-enforcement-point outcome (S3-C010).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum PepOutcome {
    Allow,
    Deny,
    #[default]
    UnknownFailClosed,
}

/// Policy-enforcement-point decision (S3-C010).
///
/// The default and every missing-input path is `UNKNOWN_FAIL_CLOSED`. `ALLOW`
/// requires referenced evidence and cannot be reached by omission.
#[derive(Debug, Clone, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "PepDecisionWire")]
pub struct PepDecision {
    decision: PepOutcome,
    effect_id: Option<Identifier>,
    evidence: Option<AllowlistedEvidenceField>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct PepDecisionWire {
    #[serde(default)]
    decision: PepOutcome,
    #[serde(default)]
    effect_id: Option<Identifier>,
    #[serde(default)]
    evidence: Option<AllowlistedEvidenceField>,
}

impl PepDecision {
    /// The default decision for absent input.
    pub fn missing_input() -> Self {
        Self::default()
    }

    /// Evaluate a proposal. Absent proposal or absent evidence is fail-closed.
    pub fn evaluate(
        proposal: Option<&EffectProposal>,
        evidence: Option<AllowlistedEvidenceField>,
    ) -> Self {
        let Some(proposal) = proposal else {
            return Self::default();
        };
        let Some(evidence) = evidence else {
            return Self::default();
        };
        if evidence.key() != EvidenceKey::EffectAuthorization {
            return Self::default();
        }
        Self {
            decision: PepOutcome::Allow,
            effect_id: Some(proposal.effect_id().clone()),
            evidence: Some(evidence),
        }
    }

    /// Explicit denial.
    pub fn deny(proposal: &EffectProposal) -> Self {
        Self {
            decision: PepOutcome::Deny,
            effect_id: Some(proposal.effect_id().clone()),
            evidence: None,
        }
    }

    pub fn decision(&self) -> PepOutcome {
        self.decision
    }

    pub fn effect_id(&self) -> Option<&Identifier> {
        self.effect_id.as_ref()
    }

    pub fn evidence(&self) -> Option<&AllowlistedEvidenceField> {
        self.evidence.as_ref()
    }
}

impl TryFrom<PepDecisionWire> for PepDecision {
    type Error = ContractError;

    fn try_from(wire: PepDecisionWire) -> Result<Self, Self::Error> {
        if wire.decision == PepOutcome::Allow {
            let Some(evidence) = wire.evidence.as_ref() else {
                return Err(ContractError::AllowRequiresEvidence);
            };
            if evidence.key() != EvidenceKey::EffectAuthorization || wire.effect_id.is_none() {
                return Err(ContractError::AllowRequiresEvidence);
            }
        }
        Ok(Self {
            decision: wire.decision,
            effect_id: wire.effect_id,
            evidence: wire.evidence,
        })
    }
}

/// Effect outcome (S3-C011).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EffectOutcome {
    Executed,
    Refused,
    Failed,
    Unknown,
}

/// Effect result (S3-C011).
///
/// `EXECUTED` is unconstructible without a referenced `ALLOW` decision, on
/// both the constructor path and the deserialization path.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "EffectResultWire")]
pub struct EffectResult {
    schema_version: u16,
    effect_id: Identifier,
    outcome: EffectOutcome,
    decision: PepDecision,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct EffectResultWire {
    #[serde(default = "default_schema_version")]
    schema_version: u16,
    effect_id: Identifier,
    outcome: EffectOutcome,
    decision: PepDecision,
}

impl EffectResult {
    pub fn new(
        effect_id: Identifier,
        outcome: EffectOutcome,
        decision: PepDecision,
    ) -> Result<Self, ContractError> {
        if outcome == EffectOutcome::Executed && decision.decision() != PepOutcome::Allow {
            return Err(ContractError::ExecutedWithoutAllow);
        }
        if decision.decision() == PepOutcome::Allow && decision.evidence().is_none() {
            return Err(ContractError::AllowRequiresEvidence);
        }
        Ok(Self {
            schema_version: S3_SCHEMA_VERSION,
            effect_id,
            outcome,
            decision,
        })
    }

    pub fn effect_id(&self) -> &Identifier {
        &self.effect_id
    }

    pub fn outcome(&self) -> EffectOutcome {
        self.outcome
    }

    pub fn decision(&self) -> &PepDecision {
        &self.decision
    }
}

impl TryFrom<EffectResultWire> for EffectResult {
    type Error = ContractError;

    fn try_from(wire: EffectResultWire) -> Result<Self, Self::Error> {
        if wire.schema_version != S3_SCHEMA_VERSION {
            return Err(ContractError::UnsupportedSchemaVersion);
        }
        Self::new(wire.effect_id, wire.outcome, wire.decision)
    }
}

/// Dependency between two effects (S3-C012). A self-dependency is rejected.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "EffectDependencyWire")]
pub struct EffectDependency {
    prerequisite: Identifier,
    dependent: Identifier,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct EffectDependencyWire {
    prerequisite: Identifier,
    dependent: Identifier,
}

/// Blocking state of a dependent effect.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum DependencyState {
    Ready,
    BlockedOnPrerequisite,
    BlockedOnFailedPrerequisite,
    UnknownFailClosed,
}

impl EffectDependency {
    pub fn new(prerequisite: Identifier, dependent: Identifier) -> Result<Self, ContractError> {
        if prerequisite == dependent {
            return Err(ContractError::SelfDependency);
        }
        Ok(Self {
            prerequisite,
            dependent,
        })
    }

    pub fn prerequisite(&self) -> &Identifier {
        &self.prerequisite
    }

    pub fn dependent(&self) -> &Identifier {
        &self.dependent
    }

    /// Prerequisite/dependent blocking rules.
    ///
    /// A missing prerequisite outcome, or an outcome that is itself unknown, is
    /// fail-closed: the dependent is not released.
    pub fn evaluate(&self, prerequisite_outcome: Option<EffectOutcome>) -> DependencyState {
        match prerequisite_outcome {
            None => DependencyState::UnknownFailClosed,
            Some(EffectOutcome::Executed) => DependencyState::Ready,
            Some(EffectOutcome::Refused) | Some(EffectOutcome::Failed) => {
                DependencyState::BlockedOnFailedPrerequisite
            }
            Some(EffectOutcome::Unknown) => DependencyState::BlockedOnPrerequisite,
        }
    }
}

impl TryFrom<EffectDependencyWire> for EffectDependency {
    type Error = ContractError;

    fn try_from(wire: EffectDependencyWire) -> Result<Self, Self::Error> {
        Self::new(wire.prerequisite, wire.dependent)
    }
}

/// Allowlisted evidence keys for S3 contracts (S3-C013).
///
/// This enum is the complete allowlist. A value that is not one of these keys
/// cannot be carried into an S3 contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EvidenceKey {
    HostExecutionOptIn,
    EffectAuthorization,
    EnvironmentDeclaration,
    ContainmentQualification,
    OutputByteCount,
    OutputDigest,
}

/// The only carrier for environment- or output-shaped content (S3-C013).
///
/// The value is bounded, NUL-free, control-character-free and screened against
/// secret-shaped strings. There is deliberately no raw string field on any S3
/// contract type that accepts this kind of content.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields, try_from = "AllowlistedEvidenceFieldWire")]
pub struct AllowlistedEvidenceField {
    key: EvidenceKey,
    value: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct AllowlistedEvidenceFieldWire {
    key: EvidenceKey,
    value: String,
}

/// Secret-shaped markers that make an evidence value unacceptable, whatever the
/// key. The list is deliberately short and literal: this is a rejection screen,
/// not a claim of secret detection.
pub const SECRET_SHAPED_MARKERS: [&str; 9] = [
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN EC PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "ghp_",
    "gho_",
    "ghs_",
    "ghr_",
    "sk-",
];

impl AllowlistedEvidenceField {
    pub fn new(key: EvidenceKey, value: impl Into<String>) -> Result<Self, ContractError> {
        let value = value.into();
        if value.is_empty() {
            return Err(ContractError::EvidenceValueEmpty);
        }
        if value.len() > MAX_EVIDENCE_VALUE_BYTES {
            return Err(ContractError::EvidenceValueTooLong);
        }
        if value
            .chars()
            .any(|character| character.is_control() || character == '\u{0}')
        {
            return Err(ContractError::EvidenceValueControlCharacter);
        }
        if SECRET_SHAPED_MARKERS
            .iter()
            .any(|marker| value.contains(marker))
        {
            return Err(ContractError::EvidenceValueSecretShaped);
        }
        Ok(Self { key, value })
    }

    pub fn key(&self) -> EvidenceKey {
        self.key
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl TryFrom<AllowlistedEvidenceFieldWire> for AllowlistedEvidenceField {
    type Error = ContractError;

    fn try_from(wire: AllowlistedEvidenceFieldWire) -> Result<Self, Self::Error> {
        Self::new(wire.key, wire.value)
    }
}
