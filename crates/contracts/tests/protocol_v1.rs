#![forbid(unsafe_code)]

use serde::{Deserialize, Serialize};
use std::io::{self, Cursor, Read};
use wepld_contracts::*;

fn health_request() -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::Health(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: 7,
        request_id: 11,
        payload: HealthRequestPayload {},
    }))
}

#[test]
fn protocol_v1_constants_are_frozen() {
    assert_eq!(ProtocolVersion::V1.get(), 1);
    assert_eq!(LENGTH_PREFIX_BYTES, 4);
    assert_eq!(MAX_PAYLOAD_BYTES, 65_536);
    assert_eq!(MAX_WIRE_FRAME_BYTES, 65_540);
}

#[test]
fn golden_health_request_round_trips() {
    let fixture = r#"{
        "protocol_version": 1,
        "kind": "request",
        "principal": "desktop_host",
        "launch_id": 7,
        "request_id": 11,
        "operation": "health",
        "payload": {}
    }"#;

    let decoded: ProtocolEnvelope =
        serde_json::from_str(fixture).expect("golden fixture must decode");
    assert_eq!(decoded, health_request());

    let expected: serde_json::Value = serde_json::from_str(fixture).expect("fixture must be JSON");
    let encoded = serde_json::to_value(&decoded).expect("typed envelope must encode");
    assert_eq!(encoded, expected);
}

#[test]
fn golden_cancel_and_protocol_error_fixtures_round_trip() {
    let fixtures = [
        r#"{"protocol_version":1,"kind":"cancel","principal":"desktop_host","launch_id":7,"request_id":15,"target_request_id":14}"#,
        r#"{"protocol_version":1,"kind":"protocol_error","principal":"desktop_host","launch_id":7,"request_id":16,"payload":{"code":"malformed_message","message":"bad frame"}}"#,
    ];

    for fixture in fixtures {
        let decoded: ProtocolEnvelope =
            serde_json::from_str(fixture).expect("golden fixture must decode");
        let expected: serde_json::Value =
            serde_json::from_str(fixture).expect("fixture must be JSON");
        let encoded = serde_json::to_value(&decoded).expect("typed envelope must encode");
        assert_eq!(encoded, expected);
    }
}

#[test]
fn all_envelope_families_round_trip() {
    let envelopes = vec![
        health_request(),
        ProtocolEnvelope::Response(ResponseEnvelope::Health(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 11,
            payload: HealthResponsePayload {
                status: HealthStatus::Healthy,
            },
        })),
        ProtocolEnvelope::Response(ResponseEnvelope::Version(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 12,
            payload: VersionResponsePayload {
                core_version: "0.1.0".to_owned(),
                build_id: "build-1".to_owned(),
            },
        })),
        ProtocolEnvelope::Response(ResponseEnvelope::Capabilities(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 13,
            payload: CapabilitiesResponsePayload {
                capabilities: vec![
                    Capability::Health,
                    Capability::Version,
                    Capability::Capabilities,
                    Capability::HealthObservation,
                    Capability::Cancellation,
                ],
            },
        })),
        ProtocolEnvelope::Response(ResponseEnvelope::ObserveHealth(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 14,
            payload: ObserveHealthResponsePayload {},
        })),
        ProtocolEnvelope::Event(EventEnvelope::ObserveHealth(EventFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 14,
            payload: HealthObservationEventPayload {
                sequence: 1,
                status: HealthStatus::Degraded,
            },
        })),
        ProtocolEnvelope::Cancel(CancelEnvelope {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 15,
            target_request_id: 14,
        }),
        ProtocolEnvelope::Response(ResponseEnvelope::Cancel(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: 15,
            payload: CancelResponsePayload {
                outcome: CancellationOutcome::Cancelled,
            },
        })),
        ProtocolEnvelope::ProtocolError(ProtocolErrorEnvelope {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: 7,
            request_id: Some(16),
            payload: ProtocolErrorPayload {
                code: ProtocolErrorCode::MalformedMessage,
                message: "malformed message".to_owned(),
            },
        }),
    ];

    for envelope in envelopes {
        let wire = encode_frame(&envelope).expect("envelope must encode");
        let mut cursor = Cursor::new(wire);
        let decoded: ProtocolEnvelope = read_frame(&mut cursor).expect("envelope must decode");
        assert_eq!(decoded, envelope);
    }
}

#[test]
fn unknown_and_malformed_protocol_fields_fail_closed() {
    let cases = [
        r#"{"protocol_version":2,"kind":"request","principal":"desktop_host","launch_id":7,"request_id":11,"operation":"health","payload":{}}"#,
        r#"{"protocol_version":1,"kind":"future_kind","principal":"desktop_host","launch_id":7,"request_id":11,"operation":"health","payload":{}}"#,
        r#"{"protocol_version":1,"kind":"request","principal":"webview","launch_id":7,"request_id":11,"operation":"health","payload":{}}"#,
        r#"{"protocol_version":1,"kind":"request","principal":"desktop_host","launch_id":7,"request_id":11,"operation":"future_operation","payload":{}}"#,
        r#"{"protocol_version":1,"kind":"request","principal":"desktop_host","launch_id":7,"operation":"health","payload":{}}"#,
        r#"{"protocol_version":1,"kind":"request","principal":"desktop_host","launch_id":7,"request_id":11,"operation":"health","payload":{"unexpected":true}}"#,
        r#"{"protocol_version":1,"kind":"cancel","principal":"desktop_host","launch_id":7,"request_id":15,"target_request_id":14,"unexpected":true}"#,
    ];

    for case in cases {
        assert!(serde_json::from_str::<ProtocolEnvelope>(case).is_err());
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct SizedPayload {
    data: String,
}

#[test]
fn frame_round_trips_property_style_size_corpus() {
    for size in [
        0_usize, 1, 2, 3, 7, 31, 255, 256, 1_023, 1_024, 4_095, 8_192, 32_768, 60_000,
    ] {
        let value = SizedPayload {
            data: "a".repeat(size),
        };
        let wire = encode_frame(&value).expect("bounded payload must encode");
        assert!(wire.len() <= MAX_WIRE_FRAME_BYTES);
        let mut cursor = Cursor::new(wire);
        let decoded: SizedPayload = read_frame(&mut cursor).expect("bounded payload must decode");
        assert_eq!(decoded, value);
    }
}

#[test]
fn exact_max_payload_is_accepted() {
    let empty = SizedPayload {
        data: String::new(),
    };
    let overhead = serde_json::to_vec(&empty)
        .expect("empty fixture must encode")
        .len();
    let value = SizedPayload {
        data: "a".repeat(MAX_PAYLOAD_BYTES - overhead),
    };
    let wire = encode_frame(&value).expect("exact max payload must encode");
    assert_eq!(wire.len(), MAX_WIRE_FRAME_BYTES);

    let mut cursor = Cursor::new(wire);
    let decoded: SizedPayload = read_frame(&mut cursor).expect("exact max payload must decode");
    assert_eq!(decoded, value);
}

#[test]
fn oversized_encoded_payload_is_rejected_at_bound() {
    let value = SizedPayload {
        data: "a".repeat(MAX_PAYLOAD_BYTES),
    };

    match encode_frame(&value) {
        Err(FrameError::PayloadTooLarge { length, max }) => {
            assert!(length > MAX_PAYLOAD_BYTES);
            assert_eq!(max, MAX_PAYLOAD_BYTES);
        }
        other => panic!("expected payload-too-large error, got {other:?}"),
    }
}

#[derive(Debug)]
struct FailingSerialize;

impl Serialize for FailingSerialize {
    fn serialize<S>(&self, _serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        Err(serde::ser::Error::custom("forced serialization failure"))
    }
}

struct ErrorReader {
    kind: io::ErrorKind,
}

impl Read for ErrorReader {
    fn read(&mut self, _buffer: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::from(self.kind))
    }
}

#[test]
fn frame_errors_retain_deterministic_classification() {
    let expected_serialization_category = serde_json::to_vec(&FailingSerialize)
        .expect_err("fixture must fail serialization")
        .classify();
    assert_eq!(
        encode_frame(&FailingSerialize),
        Err(FrameError::SerializationFailed {
            category: expected_serialization_category,
        })
    );

    let mut reader = ErrorReader {
        kind: io::ErrorKind::PermissionDenied,
    };
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut reader),
        Err(FrameError::Io {
            kind: io::ErrorKind::PermissionDenied,
        })
    );
}

struct PrefixProbe {
    prefix: [u8; LENGTH_PREFIX_BYTES],
    offset: usize,
    body_reads: usize,
}

impl PrefixProbe {
    fn oversized() -> Self {
        Self {
            prefix: ((MAX_PAYLOAD_BYTES + 1) as u32).to_be_bytes(),
            offset: 0,
            body_reads: 0,
        }
    }
}

impl Read for PrefixProbe {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        if self.offset < self.prefix.len() {
            let count = (self.prefix.len() - self.offset).min(buffer.len());
            buffer[..count].copy_from_slice(&self.prefix[self.offset..self.offset + count]);
            self.offset += count;
            return Ok(count);
        }

        self.body_reads += 1;
        Ok(0)
    }
}

#[test]
fn oversized_declared_length_rejects_before_body_read() {
    let mut probe = PrefixProbe::oversized();
    let result = read_frame::<_, serde_json::Value>(&mut probe);
    assert_eq!(
        result,
        Err(FrameError::PayloadTooLarge {
            length: MAX_PAYLOAD_BYTES + 1,
            max: MAX_PAYLOAD_BYTES,
        })
    );
    assert_eq!(probe.body_reads, 0);
}

#[test]
fn framing_failures_are_deterministic() {
    let mut truncated_prefix = Cursor::new(vec![0_u8, 0]);
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut truncated_prefix),
        Err(FrameError::TruncatedPrefix)
    );

    let mut empty_payload = Cursor::new(0_u32.to_be_bytes().to_vec());
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut empty_payload),
        Err(FrameError::EmptyPayload)
    );

    let mut truncated_body = Cursor::new([3_u32.to_be_bytes().as_slice(), b"{}"].concat());
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut truncated_body),
        Err(FrameError::TruncatedPayload { declared: 3 })
    );

    let malformed_payload = b"{";
    let malformed_category = serde_json::from_slice::<serde_json::Value>(malformed_payload)
        .expect_err("fixture must be malformed JSON")
        .classify();
    let mut malformed_json =
        Cursor::new([1_u32.to_be_bytes().as_slice(), malformed_payload.as_slice()].concat());
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut malformed_json),
        Err(FrameError::InvalidJson {
            category: malformed_category,
        })
    );

    let invalid_utf8_payload = [0xff];
    let invalid_utf8_category = serde_json::from_slice::<serde_json::Value>(&invalid_utf8_payload)
        .expect_err("fixture must reject invalid UTF-8")
        .classify();
    let mut invalid_utf8 = Cursor::new(
        [
            1_u32.to_be_bytes().as_slice(),
            invalid_utf8_payload.as_slice(),
        ]
        .concat(),
    );
    assert_eq!(
        read_frame::<_, serde_json::Value>(&mut invalid_utf8),
        Err(FrameError::InvalidJson {
            category: invalid_utf8_category,
        })
    );
}
