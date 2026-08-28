use serde::de::{self, DeserializeOwned, IgnoredAny, SeqAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::error::Category as JsonErrorCategory;
use serde_json::{Map, Value};
use std::fmt;
use std::io::{Error, Write};
use std::marker::PhantomData;

pub const PROJECT_CONTRACT_VERSION_V1: u16 = 1;
pub const MAX_PROJECT_CONTRACT_JSON_BYTES: usize = 1_048_576;
pub const MAX_MACHINE_PATH_BYTES: usize = 32_768;
pub const MAX_MACHINE_PATH_WIDE_UNITS: usize = 32_768;
pub const MAX_SAFE_DISPLAY_PATH_BYTES: usize = 262_144;
pub const MAX_OPAQUE_ID_BYTES: usize = 96;
pub const MAX_TEMPLATE_ID_BYTES: usize = 96;
pub const MAX_FINDING_CODE_BYTES: usize = 64;
pub const MAX_IDENTITY_CANDIDATES: usize = 32;
pub const MAX_EVIDENCE_REFS: usize = 256;
pub const MAX_RECORD_DIGESTS: usize = 512;
pub const MAX_DOCTOR_FINDINGS: usize = 256;
pub const MAX_SAFE_PARAMETERS: usize = 16;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct ProjectContractVersion(u16);

impl ProjectContractVersion {
    pub const V1: Self = Self(PROJECT_CONTRACT_VERSION_V1);

    pub const fn get(self) -> u16 {
        self.0
    }
}

impl TryFrom<u16> for ProjectContractVersion {
    type Error = ContractValueError;

    fn try_from(value: u16) -> Result<Self, Self::Error> {
        if value == PROJECT_CONTRACT_VERSION_V1 {
            Ok(Self(value))
        } else {
            Err(ContractValueError::UnsupportedSchemaVersion { value })
        }
    }
}

impl<'de> Deserialize<'de> for ProjectContractVersion {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = u16::deserialize(deserializer)?;
        Self::try_from(value).map_err(de::Error::custom)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContractValueError {
    UnsupportedSchemaVersion {
        value: u16,
    },
    TokenEmpty {
        kind: &'static str,
    },
    TokenTooLong {
        kind: &'static str,
        bytes: usize,
        max: usize,
    },
    TokenPrefixInvalid {
        kind: &'static str,
        expected: &'static str,
    },
    TokenCharacterInvalid {
        kind: &'static str,
    },
    MachinePathTooLong {
        units: usize,
        max: usize,
    },
    SafeDisplayPathTooLong {
        bytes: usize,
        max: usize,
    },
    SafeDisplayPathContainsControl,
    DigestHexInvalid,
    ItemsTooMany {
        length: usize,
        max: usize,
    },
}

impl fmt::Display for ContractValueError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnsupportedSchemaVersion { value } => {
                write!(
                    formatter,
                    "unsupported project contract schema version: {value}"
                )
            }
            Self::TokenEmpty { kind } => write!(formatter, "{kind} must not be empty"),
            Self::TokenTooLong { kind, bytes, max } => {
                write!(
                    formatter,
                    "{kind} length {bytes} exceeds maximum {max} bytes"
                )
            }
            Self::TokenPrefixInvalid { kind, expected } => {
                write!(formatter, "{kind} must start with {expected}")
            }
            Self::TokenCharacterInvalid { kind } => {
                write!(formatter, "{kind} contains a prohibited character")
            }
            Self::MachinePathTooLong { units, max } => {
                write!(
                    formatter,
                    "machine path length {units} exceeds maximum {max}"
                )
            }
            Self::SafeDisplayPathTooLong { bytes, max } => {
                write!(
                    formatter,
                    "safe display path length {bytes} exceeds maximum {max} bytes"
                )
            }
            Self::SafeDisplayPathContainsControl => {
                write!(
                    formatter,
                    "safe display path contains an unescaped control character"
                )
            }
            Self::DigestHexInvalid => write!(
                formatter,
                "SHA-256 digest must be 64 lowercase hexadecimal characters"
            ),
            Self::ItemsTooMany { length, max } => {
                write!(formatter, "item count {length} exceeds maximum {max}")
            }
        }
    }
}

fn validate_prefixed_token(
    value: &str,
    kind: &'static str,
    prefix: &'static str,
    max: usize,
) -> Result<(), ContractValueError> {
    if value.is_empty() {
        return Err(ContractValueError::TokenEmpty { kind });
    }
    if value.len() > max {
        return Err(ContractValueError::TokenTooLong {
            kind,
            bytes: value.len(),
            max,
        });
    }
    if !value.starts_with(prefix) {
        return Err(ContractValueError::TokenPrefixInvalid {
            kind,
            expected: prefix,
        });
    }
    if !value
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'_' | b'-' | b'.' | b':'))
    {
        return Err(ContractValueError::TokenCharacterInvalid { kind });
    }
    Ok(())
}

macro_rules! bounded_token_type {
    ($name:ident, $kind:literal, $prefix:literal, $max:expr) => {
        #[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize)]
        #[serde(transparent)]
        pub struct $name(String);

        impl $name {
            pub fn as_str(&self) -> &str {
                &self.0
            }

            pub fn into_string(self) -> String {
                self.0
            }
        }

        impl TryFrom<String> for $name {
            type Error = ContractValueError;

            fn try_from(value: String) -> Result<Self, Self::Error> {
                validate_prefixed_token(&value, $kind, $prefix, $max)?;
                Ok(Self(value))
            }
        }

        impl TryFrom<&str> for $name {
            type Error = ContractValueError;

            fn try_from(value: &str) -> Result<Self, Self::Error> {
                Self::try_from(value.to_owned())
            }
        }

        impl<'de> Deserialize<'de> for $name {
            fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
            where
                D: Deserializer<'de>,
            {
                let value = String::deserialize(deserializer)?;
                Self::try_from(value).map_err(de::Error::custom)
            }
        }
    };
}

bounded_token_type!(ProjectId, "project id", "p_", MAX_OPAQUE_ID_BYTES);
bounded_token_type!(WorktreeId, "worktree id", "w_", MAX_OPAQUE_ID_BYTES);
bounded_token_type!(RecordId, "record id", "r_", MAX_OPAQUE_ID_BYTES);
bounded_token_type!(GenerationId, "generation id", "g_", MAX_OPAQUE_ID_BYTES);
bounded_token_type!(ProducerId, "producer id", "wepld.", MAX_OPAQUE_ID_BYTES);
bounded_token_type!(TemplateId, "template id", "tpl.", MAX_TEMPLATE_ID_BYTES);
bounded_token_type!(FindingCode, "finding code", "D-", MAX_FINDING_CODE_BYTES);

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(transparent)]
pub struct UnixMillis(u64);

impl UnixMillis {
    pub const fn new(value: u64) -> Self {
        Self(value)
    }

    pub const fn get(self) -> u64 {
        self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(tag = "encoding", content = "value", rename_all = "snake_case")]
pub enum MachinePath {
    Utf8(String),
    UnixBytes(Vec<u8>),
    WindowsWtf16(Vec<u16>),
}

impl MachinePath {
    pub fn utf8(value: impl Into<String>) -> Result<Self, ContractValueError> {
        let value = value.into();
        if value.len() > MAX_MACHINE_PATH_BYTES {
            return Err(ContractValueError::MachinePathTooLong {
                units: value.len(),
                max: MAX_MACHINE_PATH_BYTES,
            });
        }
        Ok(Self::Utf8(value))
    }

    pub fn unix_bytes(value: Vec<u8>) -> Result<Self, ContractValueError> {
        if value.len() > MAX_MACHINE_PATH_BYTES {
            return Err(ContractValueError::MachinePathTooLong {
                units: value.len(),
                max: MAX_MACHINE_PATH_BYTES,
            });
        }
        Ok(Self::UnixBytes(value))
    }

    pub fn windows_wtf16(value: Vec<u16>) -> Result<Self, ContractValueError> {
        if value.len() > MAX_MACHINE_PATH_WIDE_UNITS {
            return Err(ContractValueError::MachinePathTooLong {
                units: value.len(),
                max: MAX_MACHINE_PATH_WIDE_UNITS,
            });
        }
        Ok(Self::WindowsWtf16(value))
    }

    pub fn safe_display(&self) -> SafeDisplayPath {
        let mut output = String::new();
        match self {
            Self::Utf8(value) => push_escaped_text(&mut output, value),
            Self::UnixBytes(value) => {
                for byte in value {
                    if byte.is_ascii_graphic() || *byte == b' ' {
                        output.push(char::from(*byte));
                    } else {
                        use std::fmt::Write as _;
                        write!(&mut output, "\\x{byte:02x}")
                            .expect("writing to String cannot fail");
                    }
                }
            }
            Self::WindowsWtf16(value) => {
                for unit in value {
                    if let Some(character) = char::from_u32(u32::from(*unit)) {
                        if !character.is_control() {
                            output.push(character);
                            continue;
                        }
                    }
                    use std::fmt::Write as _;
                    write!(&mut output, "\\u{unit:04x}").expect("writing to String cannot fail");
                }
            }
        }
        debug_assert!(output.len() <= MAX_SAFE_DISPLAY_PATH_BYTES);
        SafeDisplayPath(output)
    }
}

impl<'de> Deserialize<'de> for MachinePath {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        #[derive(Deserialize)]
        #[serde(tag = "encoding", content = "value", rename_all = "snake_case")]
        enum Wire {
            Utf8(String),
            UnixBytes(Vec<u8>),
            WindowsWtf16(Vec<u16>),
        }

        match Wire::deserialize(deserializer)? {
            Wire::Utf8(value) => Self::utf8(value),
            Wire::UnixBytes(value) => Self::unix_bytes(value),
            Wire::WindowsWtf16(value) => Self::windows_wtf16(value),
        }
        .map_err(de::Error::custom)
    }
}

fn push_escaped_text(output: &mut String, value: &str) {
    for character in value.chars() {
        if character.is_control() {
            use std::fmt::Write as _;
            write!(output, "\\u{{{:x}}}", u32::from(character))
                .expect("writing to String cannot fail");
        } else {
            output.push(character);
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct SafeDisplayPath(String);

impl SafeDisplayPath {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl<'de> Deserialize<'de> for SafeDisplayPath {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = String::deserialize(deserializer)?;
        if value.len() > MAX_SAFE_DISPLAY_PATH_BYTES {
            return Err(de::Error::custom(
                ContractValueError::SafeDisplayPathTooLong {
                    bytes: value.len(),
                    max: MAX_SAFE_DISPLAY_PATH_BYTES,
                },
            ));
        }
        if value.chars().any(char::is_control) {
            return Err(de::Error::custom(
                ContractValueError::SafeDisplayPathContainsControl,
            ));
        }
        Ok(Self(value))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ObservationErrorClass {
    NotFound,
    PermissionDenied,
    InvalidPath,
    SymlinkLoop,
    Unsupported,
    TrustRefused,
    Io,
    RaceDetected,
    NotApplicable,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "state", rename_all = "snake_case")]
pub enum Observation<T> {
    Available { value: T },
    Unavailable { error: ObservationErrorClass },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "state", rename_all = "snake_case")]
pub enum OptionalObservation<T> {
    Value { value: T },
    None,
    Unavailable { error: ObservationErrorClass },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectLocator {
    pub schema_version: ProjectContractVersion,
    pub input_path: MachinePath,
    pub lexical_absolute_path: MachinePath,
    pub resolved_path: Observation<MachinePath>,
    pub observation_time: UnixMillis,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum VcsKind {
    Git,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum LinkedWorktreeState {
    Known,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RepositoryTrustState {
    Trusted,
    RefusedByGit,
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RepositoryTopology {
    pub schema_version: ProjectContractVersion,
    pub vcs_kind: VcsKind,
    pub worktree_root: Observation<MachinePath>,
    pub absolute_git_dir: Observation<MachinePath>,
    pub git_common_dir: Observation<MachinePath>,
    pub is_bare: Observation<bool>,
    pub is_inside_worktree: Observation<bool>,
    pub superproject_worktree: OptionalObservation<MachinePath>,
    pub linked_worktree_state: LinkedWorktreeState,
    pub trust_state: RepositoryTrustState,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DigestAlgorithm {
    Sha256,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct DigestHex(String);

impl DigestHex {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl TryFrom<String> for DigestHex {
    type Error = ContractValueError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.len() != 64
            || !value
                .bytes()
                .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
        {
            return Err(ContractValueError::DigestHexInvalid);
        }
        Ok(Self(value))
    }
}

impl TryFrom<&str> for DigestHex {
    type Error = ContractValueError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Self::try_from(value.to_owned())
    }
}

impl<'de> Deserialize<'de> for DigestHex {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = String::deserialize(deserializer)?;
        Self::try_from(value).map_err(de::Error::custom)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ContentDigest {
    pub algorithm: DigestAlgorithm,
    pub hex: DigestHex,
}

impl ContentDigest {
    pub fn sha256(hex: impl AsRef<str>) -> Result<Self, ContractValueError> {
        Ok(Self {
            algorithm: DigestAlgorithm::Sha256,
            hex: DigestHex::try_from(hex.as_ref())?,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundedList<T, const MAX: usize>(Vec<T>);

impl<T, const MAX: usize> BoundedList<T, MAX> {
    pub fn as_slice(&self) -> &[T] {
        &self.0
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn into_vec(self) -> Vec<T> {
        self.0
    }
}

impl<T, const MAX: usize> TryFrom<Vec<T>> for BoundedList<T, MAX> {
    type Error = ContractValueError;

    fn try_from(value: Vec<T>) -> Result<Self, Self::Error> {
        if value.len() > MAX {
            return Err(ContractValueError::ItemsTooMany {
                length: value.len(),
                max: MAX,
            });
        }
        Ok(Self(value))
    }
}

impl<T, const MAX: usize> Serialize for BoundedList<T, MAX>
where
    T: Serialize,
{
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.0.serialize(serializer)
    }
}

impl<'de, T, const MAX: usize> Deserialize<'de> for BoundedList<T, MAX>
where
    T: Deserialize<'de>,
{
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct BoundedListVisitor<T, const MAX: usize>(PhantomData<T>);

        impl<'de, T, const MAX: usize> Visitor<'de> for BoundedListVisitor<T, MAX>
        where
            T: Deserialize<'de>,
        {
            type Value = BoundedList<T, MAX>;

            fn expecting(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(formatter, "a list with at most {MAX} items")
            }

            fn visit_seq<A>(self, mut sequence: A) -> Result<Self::Value, A::Error>
            where
                A: SeqAccess<'de>,
            {
                let capacity = sequence.size_hint().unwrap_or(0).min(MAX);
                let mut values = Vec::with_capacity(capacity);
                while values.len() < MAX {
                    match sequence.next_element::<T>()? {
                        Some(value) => values.push(value),
                        None => return Ok(BoundedList(values)),
                    }
                }
                if sequence.next_element::<IgnoredAny>()?.is_some() {
                    return Err(de::Error::custom(ContractValueError::ItemsTooMany {
                        length: MAX + 1,
                        max: MAX,
                    }));
                }
                Ok(BoundedList(values))
            }
        }

        deserializer.deserialize_seq(BoundedListVisitor::<T, MAX>(PhantomData))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum IdentityRecordState {
    Active,
    Ambiguous,
    Conflict,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectIdentityRecord {
    pub schema_version: ProjectContractVersion,
    pub project_id: ProjectId,
    pub worktree_id: WorktreeId,
    pub revalidated_match_facts_digest: ContentDigest,
    pub state: IdentityRecordState,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum IdentityReservationState {
    Reserved,
    Initialized,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct IdentityCatalogReservation {
    pub schema_version: ProjectContractVersion,
    pub reservation_key_version: u16,
    pub revalidated_match_facts_digest: ContentDigest,
    pub project_id: ProjectId,
    pub state: IdentityReservationState,
    pub created_at: UnixMillis,
    pub updated_at: UnixMillis,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum IdentityMatchStrength {
    ExactBinding,
    StrongReassociation,
    ReservedBinding,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum IdentityConflictKind {
    ContradictoryTopology,
    MultipleStrongCandidates,
    ReservationMismatch,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum StoreLockScope {
    IdentityCatalog,
    ProjectStore,
}

pub type IdentityCandidateList = BoundedList<ProjectId, MAX_IDENTITY_CANDIDATES>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "result", rename_all = "snake_case")]
pub enum IdentityResolution {
    Existing {
        project_id: ProjectId,
        strength: IdentityMatchStrength,
    },
    Reserved {
        reservation: IdentityCatalogReservation,
    },
    Ambiguous {
        candidates: IdentityCandidateList,
    },
    Conflict {
        kind: IdentityConflictKind,
        candidates: IdentityCandidateList,
    },
    Busy {
        scope: StoreLockScope,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EvidenceRecordKind {
    ProjectLocator,
    RepositoryTopology,
    ProjectIdentity,
    ProjectIndex,
    DoctorReport,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum FreshnessBasis {
    ObservationTime,
    FilesystemMetadata,
    ContentDigest,
    RepositoryTopology,
    GenerationCommit,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EvidenceStatus {
    Complete,
    Partial,
    Stale,
    Corrupt,
    Unavailable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProvenanceSource {
    UserLocator,
    FilesystemObservation,
    GitMetadata,
    RootDescriptor,
    LocalStore,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct EvidenceProvenance {
    pub source: ProvenanceSource,
    pub parent_record_id: Option<RecordId>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct EvidenceEnvelope<T> {
    pub schema_version: ProjectContractVersion,
    pub record_id: RecordId,
    pub record_kind: EvidenceRecordKind,
    pub project_id: ProjectId,
    pub producer: ProducerId,
    pub producer_contract_version: u16,
    pub observed_at: UnixMillis,
    pub freshness_basis: FreshnessBasis,
    pub payload_digest: ContentDigest,
    pub provenance: EvidenceProvenance,
    pub status: EvidenceStatus,
    pub payload: T,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RecordDigest {
    pub record_id: RecordId,
    pub digest: ContentDigest,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum StoreAuthenticity {
    UnauthenticatedStructuralCoherenceOnly,
}

pub type EvidenceRecordRefs = BoundedList<RecordId, MAX_EVIDENCE_REFS>;
pub type RecordDigestList = BoundedList<RecordDigest, MAX_RECORD_DIGESTS>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectGenerationManifest {
    pub schema_version: ProjectContractVersion,
    pub generation_id: GenerationId,
    pub project_id: ProjectId,
    pub identity_record_ref: RecordId,
    pub index_record_ref: RecordId,
    pub evidence_record_refs: EvidenceRecordRefs,
    pub record_digests: RecordDigestList,
    pub producer_contract_version: u16,
    pub created_at: UnixMillis,
    pub authenticity: StoreAuthenticity,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectCurrentRef {
    pub schema_version: ProjectContractVersion,
    pub project_id: ProjectId,
    pub generation_id: GenerationId,
    pub manifest_digest: ContentDigest,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DoctorSeverity {
    Info,
    Warning,
    Blocking,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DoctorCategory {
    Identity,
    Repository,
    Workspace,
    ToolchainDescriptor,
    Lockfile,
    PackageManager,
    EvidenceStore,
    Freshness,
    SecuritySensitiveConfig,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RemediationKind {
    None,
    Informational,
    ManualAction,
    CapabilityRequired,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum MachineActionHint {
    InspectIdentity,
    InspectRepositoryTrust,
    InspectWorkspace,
    InspectEvidenceStore,
    RefreshEvidence,
    ResolveAmbiguity,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ToolchainKind {
    Rust,
    Node,
    Python,
    Mise,
    Just,
    Make,
    Gradle,
    Maven,
    Go,
    Nx,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PackageManagerKind {
    Cargo,
    Npm,
    Pnpm,
    Yarn,
    Bun,
    Uv,
    Poetry,
    Go,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum SafeParameter {
    Boolean { value: bool },
    Count { value: u64 },
    Path { value: SafeDisplayPath },
    Toolchain { value: ToolchainKind },
    PackageManager { value: PackageManagerKind },
    TrustState { value: RepositoryTrustState },
    EvidenceStatus { value: EvidenceStatus },
    LockScope { value: StoreLockScope },
}

pub type EvidenceReferenceList = BoundedList<RecordId, MAX_EVIDENCE_REFS>;
pub type SafeParameterList = BoundedList<SafeParameter, MAX_SAFE_PARAMETERS>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DoctorFinding {
    pub finding_code: FindingCode,
    pub severity: DoctorSeverity,
    pub category: DoctorCategory,
    pub summary_template_id: TemplateId,
    pub explanation_template_id: TemplateId,
    pub observed_evidence_refs: EvidenceReferenceList,
    pub remediation_kind: RemediationKind,
    pub remediation_template_id: TemplateId,
    pub machine_action_hint: Option<MachineActionHint>,
    pub safe_parameters: SafeParameterList,
}

pub type DoctorFindingList = BoundedList<DoctorFinding, MAX_DOCTOR_FINDINGS>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DoctorReport {
    pub schema_version: ProjectContractVersion,
    pub project_id: ProjectId,
    pub selected_generation_id: Option<GenerationId>,
    pub evaluated_at: UnixMillis,
    pub findings: DoctorFindingList,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProjectCommand {
    Open,
    Doctor,
    Status,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProjectErrorClass {
    UsageInput,
    ProjectResolutionIdentity,
    EvidenceStoreIntegrity,
    BlockingDoctorFindings,
    CapabilityUnavailable,
    UnexpectedInternal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProjectErrorCode {
    InvalidInput,
    ProjectResolutionFailed,
    IdentityConflict,
    IdentityAmbiguous,
    IdentityCatalogBusy,
    StoreBusy,
    EvidenceCorrupt,
    BlockingFindings,
    CapabilityUnavailable,
    InternalFailure,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectCommandError {
    pub class: ProjectErrorClass,
    pub code: ProjectErrorCode,
    pub safe_parameters: SafeParameterList,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "outcome", rename_all = "snake_case")]
pub enum ProjectCommandEnvelope<T> {
    Success {
        schema_version: ProjectContractVersion,
        command: ProjectCommand,
        project_id: Option<ProjectId>,
        data: T,
    },
    Error {
        schema_version: ProjectContractVersion,
        command: ProjectCommand,
        error: ProjectCommandError,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProjectContractCodecError {
    PayloadTooLarge { length: usize, max: usize },
    SerializationFailed { category: JsonErrorCategory },
    DeserializationFailed { category: JsonErrorCategory },
}

impl fmt::Display for ProjectContractCodecError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::PayloadTooLarge { length, max } => {
                write!(
                    formatter,
                    "project contract JSON length {length} exceeds maximum {max} bytes"
                )
            }
            Self::SerializationFailed { category } => {
                write!(
                    formatter,
                    "project contract serialization failed: {category:?}"
                )
            }
            Self::DeserializationFailed { category } => {
                write!(
                    formatter,
                    "project contract deserialization failed: {category:?}"
                )
            }
        }
    }
}

#[derive(Default)]
struct BoundedJsonWriter {
    bytes: Vec<u8>,
    overflow_length: Option<usize>,
}

impl Write for BoundedJsonWriter {
    fn write(&mut self, buffer: &[u8]) -> std::io::Result<usize> {
        let attempted = self.bytes.len().saturating_add(buffer.len());
        if attempted > MAX_PROJECT_CONTRACT_JSON_BYTES {
            self.overflow_length = Some(attempted);
            return Err(Error::other("project contract JSON exceeds bound"));
        }
        self.bytes.extend_from_slice(buffer);
        Ok(buffer.len())
    }

    fn flush(&mut self) -> std::io::Result<()> {
        Ok(())
    }
}

fn write_bounded_json<T>(value: &T) -> Result<Vec<u8>, ProjectContractCodecError>
where
    T: Serialize,
{
    let mut writer = BoundedJsonWriter::default();
    let serialization = serde_json::to_writer(&mut writer, value);
    if let Some(length) = writer.overflow_length {
        return Err(ProjectContractCodecError::PayloadTooLarge {
            length,
            max: MAX_PROJECT_CONTRACT_JSON_BYTES,
        });
    }
    serialization.map_err(|error| ProjectContractCodecError::SerializationFailed {
        category: error.classify(),
    })?;
    Ok(writer.bytes)
}

fn canonicalize_json(value: Value) -> Value {
    match value {
        Value::Array(values) => Value::Array(values.into_iter().map(canonicalize_json).collect()),
        Value::Object(values) => {
            let mut entries: Vec<_> = values.into_iter().collect();
            entries.sort_by(|left, right| left.0.cmp(&right.0));
            let mut canonical = Map::new();
            for (key, value) in entries {
                canonical.insert(key, canonicalize_json(value));
            }
            Value::Object(canonical)
        }
        other => other,
    }
}

pub fn canonical_project_json<T>(value: &T) -> Result<Vec<u8>, ProjectContractCodecError>
where
    T: Serialize,
{
    let initial = write_bounded_json(value)?;
    let parsed: Value = serde_json::from_slice(&initial).map_err(|error| {
        ProjectContractCodecError::SerializationFailed {
            category: error.classify(),
        }
    })?;
    write_bounded_json(&canonicalize_json(parsed))
}

pub fn decode_project_json<T>(bytes: &[u8]) -> Result<T, ProjectContractCodecError>
where
    T: DeserializeOwned,
{
    if bytes.len() > MAX_PROJECT_CONTRACT_JSON_BYTES {
        return Err(ProjectContractCodecError::PayloadTooLarge {
            length: bytes.len(),
            max: MAX_PROJECT_CONTRACT_JSON_BYTES,
        });
    }
    serde_json::from_slice(bytes).map_err(|error| {
        ProjectContractCodecError::DeserializationFailed {
            category: error.classify(),
        }
    })
}
