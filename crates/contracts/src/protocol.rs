use serde::de;
use serde::{Deserialize, Deserializer, Serialize};

pub const PROTOCOL_VERSION_V1: u8 = 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct ProtocolVersion(u8);

impl ProtocolVersion {
    pub const V1: Self = Self(PROTOCOL_VERSION_V1);

    pub const fn get(self) -> u8 {
        self.0
    }
}

impl<'de> Deserialize<'de> for ProtocolVersion {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = u8::deserialize(deserializer)?;
        if value == PROTOCOL_VERSION_V1 {
            Ok(Self(value))
        } else {
            Err(de::Error::custom("unsupported protocol version"))
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Principal {
    DesktopHost,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Capability {
    Health,
    Version,
    Capabilities,
    HealthObservation,
    Cancellation,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HealthStatus {
    Healthy,
    Degraded,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum CancellationOutcome {
    Cancelled,
    AlreadyTerminal,
    UnknownTarget,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RequestFields<P> {
    pub protocol_version: ProtocolVersion,
    pub principal: Principal,
    pub launch_id: u64,
    pub request_id: u64,
    pub payload: P,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ResponseFields<P> {
    pub protocol_version: ProtocolVersion,
    pub principal: Principal,
    pub launch_id: u64,
    pub request_id: u64,
    pub payload: P,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct EventFields<P> {
    pub protocol_version: ProtocolVersion,
    pub principal: Principal,
    pub launch_id: u64,
    pub request_id: u64,
    pub payload: P,
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HealthRequestPayload {}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct VersionRequestPayload {}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CapabilitiesRequestPayload {}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ObserveHealthRequestPayload {}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HealthResponsePayload {
    pub status: HealthStatus,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct VersionResponsePayload {
    pub core_version: String,
    pub build_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CapabilitiesResponsePayload {
    pub capabilities: Vec<Capability>,
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ObserveHealthResponsePayload {}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CancelResponsePayload {
    pub outcome: CancellationOutcome,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct HealthObservationEventPayload {
    pub sequence: u64,
    pub status: HealthStatus,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "operation", rename_all = "snake_case")]
pub enum RequestEnvelope {
    Health(RequestFields<HealthRequestPayload>),
    Version(RequestFields<VersionRequestPayload>),
    Capabilities(RequestFields<CapabilitiesRequestPayload>),
    ObserveHealth(RequestFields<ObserveHealthRequestPayload>),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "operation", rename_all = "snake_case")]
pub enum ResponseEnvelope {
    Health(ResponseFields<HealthResponsePayload>),
    Version(ResponseFields<VersionResponsePayload>),
    Capabilities(ResponseFields<CapabilitiesResponsePayload>),
    ObserveHealth(ResponseFields<ObserveHealthResponsePayload>),
    Cancel(ResponseFields<CancelResponsePayload>),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "operation", rename_all = "snake_case")]
pub enum EventEnvelope {
    ObserveHealth(EventFields<HealthObservationEventPayload>),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CancelEnvelope {
    pub protocol_version: ProtocolVersion,
    pub principal: Principal,
    pub launch_id: u64,
    pub request_id: u64,
    pub target_request_id: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProtocolErrorCode {
    UnsupportedProtocol,
    MalformedMessage,
    UnauthorizedPrincipal,
    UnsupportedOperation,
    InvalidCorrelation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProtocolErrorPayload {
    pub code: ProtocolErrorCode,
    pub message: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProtocolErrorEnvelope {
    pub protocol_version: ProtocolVersion,
    pub principal: Principal,
    pub launch_id: u64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub request_id: Option<u64>,
    pub payload: ProtocolErrorPayload,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum ProtocolEnvelope {
    Request(RequestEnvelope),
    Response(ResponseEnvelope),
    Event(EventEnvelope),
    Cancel(CancelEnvelope),
    ProtocolError(ProtocolErrorEnvelope),
}
