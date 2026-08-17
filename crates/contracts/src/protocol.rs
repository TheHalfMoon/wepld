use serde::de::{self, SeqAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize};
use std::fmt;

pub const PROTOCOL_VERSION_V1: u8 = 1;
pub const MAX_CAPABILITY_ITEMS: usize = 64;
pub const MAX_PROTOCOL_ERROR_TEXT_BYTES: usize = 1_024;

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

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProtocolBudgetError {
    CapabilityItemsTooMany { length: usize, max: usize },
    ProtocolErrorTextTooLong { bytes: usize, max: usize },
}

impl fmt::Display for ProtocolBudgetError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::CapabilityItemsTooMany { length, max } => {
                write!(
                    formatter,
                    "capability item count {length} exceeds maximum {max}"
                )
            }
            Self::ProtocolErrorTextTooLong { bytes, max } => {
                write!(
                    formatter,
                    "protocol error text length {bytes} exceeds maximum {max} bytes"
                )
            }
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

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct CapabilityList(Vec<Capability>);

impl CapabilityList {
    pub fn as_slice(&self) -> &[Capability] {
        &self.0
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn into_vec(self) -> Vec<Capability> {
        self.0
    }
}

impl TryFrom<Vec<Capability>> for CapabilityList {
    type Error = ProtocolBudgetError;

    fn try_from(capabilities: Vec<Capability>) -> Result<Self, Self::Error> {
        if capabilities.len() > MAX_CAPABILITY_ITEMS {
            return Err(ProtocolBudgetError::CapabilityItemsTooMany {
                length: capabilities.len(),
                max: MAX_CAPABILITY_ITEMS,
            });
        }
        Ok(Self(capabilities))
    }
}

impl<'de> Deserialize<'de> for CapabilityList {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct CapabilityListVisitor;

        impl<'de> Visitor<'de> for CapabilityListVisitor {
            type Value = CapabilityList;

            fn expecting(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(
                    formatter,
                    "a capability list with at most {MAX_CAPABILITY_ITEMS} items"
                )
            }

            fn visit_seq<A>(self, mut sequence: A) -> Result<Self::Value, A::Error>
            where
                A: SeqAccess<'de>,
            {
                let capacity = sequence.size_hint().unwrap_or(0).min(MAX_CAPABILITY_ITEMS);
                let mut capabilities = Vec::with_capacity(capacity);

                while capabilities.len() < MAX_CAPABILITY_ITEMS {
                    match sequence.next_element::<Capability>()? {
                        Some(capability) => capabilities.push(capability),
                        None => return Ok(CapabilityList(capabilities)),
                    }
                }

                if sequence.next_element::<de::IgnoredAny>()?.is_some() {
                    return Err(de::Error::custom(
                        ProtocolBudgetError::CapabilityItemsTooMany {
                            length: MAX_CAPABILITY_ITEMS + 1,
                            max: MAX_CAPABILITY_ITEMS,
                        },
                    ));
                }

                Ok(CapabilityList(capabilities))
            }
        }

        deserializer.deserialize_seq(CapabilityListVisitor)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct ProtocolErrorText(String);

impl ProtocolErrorText {
    pub fn as_str(&self) -> &str {
        &self.0
    }

    pub fn bytes_len(&self) -> usize {
        self.0.len()
    }

    pub fn into_string(self) -> String {
        self.0
    }
}

impl TryFrom<String> for ProtocolErrorText {
    type Error = ProtocolBudgetError;

    fn try_from(message: String) -> Result<Self, Self::Error> {
        let bytes = message.len();
        if bytes > MAX_PROTOCOL_ERROR_TEXT_BYTES {
            return Err(ProtocolBudgetError::ProtocolErrorTextTooLong {
                bytes,
                max: MAX_PROTOCOL_ERROR_TEXT_BYTES,
            });
        }
        Ok(Self(message))
    }
}

impl TryFrom<&str> for ProtocolErrorText {
    type Error = ProtocolBudgetError;

    fn try_from(message: &str) -> Result<Self, Self::Error> {
        let bytes = message.len();
        if bytes > MAX_PROTOCOL_ERROR_TEXT_BYTES {
            return Err(ProtocolBudgetError::ProtocolErrorTextTooLong {
                bytes,
                max: MAX_PROTOCOL_ERROR_TEXT_BYTES,
            });
        }
        Ok(Self(message.to_owned()))
    }
}

impl<'de> Deserialize<'de> for ProtocolErrorText {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct ProtocolErrorTextVisitor;

        impl<'de> Visitor<'de> for ProtocolErrorTextVisitor {
            type Value = ProtocolErrorText;

            fn expecting(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(
                    formatter,
                    "a protocol error string of at most {MAX_PROTOCOL_ERROR_TEXT_BYTES} UTF-8 bytes"
                )
            }

            fn visit_borrowed_str<E>(self, message: &'de str) -> Result<Self::Value, E>
            where
                E: de::Error,
            {
                ProtocolErrorText::try_from(message).map_err(E::custom)
            }

            fn visit_str<E>(self, message: &str) -> Result<Self::Value, E>
            where
                E: de::Error,
            {
                ProtocolErrorText::try_from(message).map_err(E::custom)
            }

            fn visit_string<E>(self, message: String) -> Result<Self::Value, E>
            where
                E: de::Error,
            {
                ProtocolErrorText::try_from(message).map_err(E::custom)
            }
        }

        deserializer.deserialize_str(ProtocolErrorTextVisitor)
    }
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
    pub capabilities: CapabilityList,
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
    pub message: ProtocolErrorText,
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

#[cfg(test)]
mod tests {
    use super::*;
    use serde::de::value::{BorrowedStrDeserializer, Error as ValueError, SeqDeserializer};
    use std::cell::Cell;
    use std::rc::Rc;

    struct CountingCapabilityNames {
        remaining: usize,
        consumed: Rc<Cell<usize>>,
    }

    impl Iterator for CountingCapabilityNames {
        type Item = &'static str;

        fn next(&mut self) -> Option<Self::Item> {
            if self.remaining == 0 {
                return None;
            }

            self.remaining -= 1;
            self.consumed.set(self.consumed.get() + 1);
            Some("health")
        }
    }

    #[test]
    fn capability_deserialization_stops_at_first_over_budget_item() {
        let consumed = Rc::new(Cell::new(0));
        let input = CountingCapabilityNames {
            remaining: MAX_CAPABILITY_ITEMS + 1_000,
            consumed: Rc::clone(&consumed),
        };
        let deserializer = SeqDeserializer::<_, ValueError>::new(input);

        let error = CapabilityList::deserialize(deserializer)
            .expect_err("over-budget capability sequence must be rejected");

        assert_eq!(consumed.get(), MAX_CAPABILITY_ITEMS + 1);
        assert!(error.to_string().contains("exceeds maximum 64"));
    }

    #[test]
    fn protocol_error_text_borrowed_deserialization_checks_bytes_before_ownership() {
        let exact = "é".repeat(MAX_PROTOCOL_ERROR_TEXT_BYTES / "é".len());
        let decoded = ProtocolErrorText::deserialize(BorrowedStrDeserializer::<ValueError>::new(
            exact.as_str(),
        ))
        .expect("exact borrowed UTF-8 byte budget must deserialize");
        assert_eq!(decoded.bytes_len(), MAX_PROTOCOL_ERROR_TEXT_BYTES);

        let first_over = format!("{exact}a");
        assert!(
            ProtocolErrorText::deserialize(BorrowedStrDeserializer::<ValueError>::new(
                first_over.as_str(),
            ))
            .is_err()
        );
    }
}
