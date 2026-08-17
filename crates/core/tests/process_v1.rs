#![forbid(unsafe_code)]

use std::io::Write;
use std::process::{Child, Command, Stdio};
use std::thread;
use std::time::Duration;
use wepld_contracts::{
    CancelEnvelope, CancellationOutcome, CapabilitiesRequestPayload, Capability,
    HealthRequestPayload, HealthStatus, MAX_PAYLOAD_BYTES, ObserveHealthRequestPayload, Principal,
    ProtocolEnvelope, ProtocolErrorCode, ProtocolErrorEnvelope, ProtocolErrorPayload,
    ProtocolErrorText, ProtocolVersion, RequestEnvelope, RequestFields, ResponseEnvelope,
    VersionRequestPayload, encode_frame, read_frame,
};

const LAUNCH_ID: u64 = 71;

fn spawn_core() -> Child {
    Command::new(env!("CARGO_BIN_EXE_wepld-core"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("owned Core binary must spawn")
}

fn request_fields<P>(request_id: u64, payload: P) -> RequestFields<P> {
    RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: LAUNCH_ID,
        request_id,
        payload,
    }
}

fn health_request(request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::Health(request_fields(
        request_id,
        HealthRequestPayload {},
    )))
}

fn version_request(request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::Version(request_fields(
        request_id,
        VersionRequestPayload {},
    )))
}

fn capabilities_request(request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::Capabilities(request_fields(
        request_id,
        CapabilitiesRequestPayload {},
    )))
}

fn observe_request(request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::ObserveHealth(request_fields(
        request_id,
        ObserveHealthRequestPayload {},
    )))
}

fn send(child: &mut Child, envelope: &ProtocolEnvelope) {
    let wire = encode_frame(envelope).expect("test envelope must fit frame budget");
    let stdin = child.stdin.as_mut().expect("child stdin must be piped");
    stdin.write_all(&wire).expect("frame write must succeed");
    stdin.flush().expect("frame flush must succeed");
}

fn receive(child: &mut Child) -> ProtocolEnvelope {
    read_frame(child.stdout.as_mut().expect("child stdout must be piped"))
        .expect("Core must emit one canonical frame")
}

fn wait_for_exit(child: &mut Child) -> bool {
    for _ in 0..200 {
        if let Some(status) = child.try_wait().expect("child status must be readable") {
            return status.success();
        }
        thread::sleep(Duration::from_millis(5));
    }
    child.kill().expect("timed-out child must be killable");
    let _ = child.wait();
    panic!("Core did not terminate within the bounded test window");
}

fn close_input_and_wait(child: &mut Child) -> bool {
    drop(child.stdin.take());
    wait_for_exit(child)
}

#[test]
fn health_version_and_capabilities_round_trip_over_owned_process() {
    let mut child = spawn_core();

    send(&mut child, &health_request(1));
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::Health(fields)) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 1);
            assert_eq!(fields.payload.status, HealthStatus::Healthy);
        }
        other => panic!("unexpected health response: {other:?}"),
    }

    send(&mut child, &version_request(2));
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::Version(fields)) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 2);
            assert_eq!(fields.payload.core_version, "0.0.0");
            assert_eq!(fields.payload.build_id, "s1-008-core-process");
        }
        other => panic!("unexpected version response: {other:?}"),
    }

    send(&mut child, &capabilities_request(3));
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::Capabilities(fields)) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 3);
            assert_eq!(
                fields.payload.capabilities.as_slice(),
                &[
                    Capability::Health,
                    Capability::Version,
                    Capability::Capabilities,
                    Capability::HealthObservation,
                    Capability::Cancellation,
                ]
            );
        }
        other => panic!("unexpected capabilities response: {other:?}"),
    }

    assert!(!close_input_and_wait(&mut child));
}

#[test]
fn observe_health_can_be_cancelled_and_recancel_is_terminal_noop() {
    let mut child = spawn_core();

    send(&mut child, &observe_request(1));
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::ObserveHealth(fields)) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 1);
        }
        other => panic!("unexpected observe response: {other:?}"),
    }

    send(
        &mut child,
        &ProtocolEnvelope::Cancel(CancelEnvelope {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: LAUNCH_ID,
            request_id: 2,
            target_request_id: 1,
        }),
    );
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::Cancel(fields)) => {
            assert_eq!(fields.payload.outcome, CancellationOutcome::Cancelled);
        }
        other => panic!("unexpected cancel response: {other:?}"),
    }

    send(
        &mut child,
        &ProtocolEnvelope::Cancel(CancelEnvelope {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: LAUNCH_ID,
            request_id: 3,
            target_request_id: 1,
        }),
    );
    match receive(&mut child) {
        ProtocolEnvelope::Response(ResponseEnvelope::Cancel(fields)) => {
            assert_eq!(fields.payload.outcome, CancellationOutcome::AlreadyTerminal);
        }
        other => panic!("unexpected terminal cancel response: {other:?}"),
    }

    assert!(!close_input_and_wait(&mut child));
}

#[test]
fn replayed_command_exits_fail_closed_without_second_success() {
    let mut child = spawn_core();

    send(&mut child, &health_request(1));
    assert!(matches!(
        receive(&mut child),
        ProtocolEnvelope::Response(ResponseEnvelope::Health(_))
    ));

    send(&mut child, &health_request(1));
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn stale_launch_exits_fail_closed() {
    let mut child = spawn_core();

    send(&mut child, &health_request(1));
    assert!(matches!(
        receive(&mut child),
        ProtocolEnvelope::Response(ResponseEnvelope::Health(_))
    ));

    let stale = ProtocolEnvelope::Request(RequestEnvelope::Health(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: LAUNCH_ID + 1,
        request_id: 2,
        payload: HealthRequestPayload {},
    }));
    send(&mut child, &stale);
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn oversized_declared_payload_exits_before_body_is_required() {
    let mut child = spawn_core();
    let declared = (MAX_PAYLOAD_BYTES as u32 + 1).to_be_bytes();
    let stdin = child.stdin.as_mut().expect("child stdin must be piped");
    stdin
        .write_all(&declared)
        .expect("oversized prefix write must succeed");
    stdin.flush().expect("oversized prefix flush must succeed");
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn malformed_json_exits_fail_closed() {
    let mut child = spawn_core();
    let stdin = child.stdin.as_mut().expect("child stdin must be piped");
    stdin
        .write_all(&1_u32.to_be_bytes())
        .expect("malformed prefix write must succeed");
    stdin
        .write_all(b"{")
        .expect("malformed payload write must succeed");
    stdin.flush().expect("malformed frame flush must succeed");
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn desktop_inbound_protocol_error_kind_is_rejected() {
    let mut child = spawn_core();
    let inbound = ProtocolEnvelope::ProtocolError(ProtocolErrorEnvelope {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: Some(LAUNCH_ID),
        request_id: Some(1),
        payload: ProtocolErrorPayload {
            code: ProtocolErrorCode::MalformedMessage,
            message: ProtocolErrorText::try_from("desktop must not send protocol_error")
                .expect("fixture error text must fit budget"),
        },
    });
    send(&mut child, &inbound);
    assert!(!wait_for_exit(&mut child));
}
