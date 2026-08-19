#![forbid(unsafe_code)]

use std::io::Write;
use std::process::{Child, Command, Stdio};
use std::thread;
use std::time::{Duration, Instant};

use wepld_contracts::{
    CancelEnvelope, CancellationOutcome, Capability, CapabilityList, HealthRequestPayload,
    HealthStatus, MAX_PAYLOAD_BYTES, ObserveHealthRequestPayload, Principal, ProtocolEnvelope,
    ProtocolVersion, RequestEnvelope, RequestFields, ResponseEnvelope, encode_frame, read_frame,
};
use wepld_core::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS, MAX_TERMINAL_RESULTS,
    StateError,
};

const LAUNCH_ID: u64 = 711;
const PROCESS_EXIT_TIMEOUT: Duration = Duration::from_secs(5);
const PROCESS_POLL_INTERVAL: Duration = Duration::from_millis(5);

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

fn observe_request(request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Request(RequestEnvelope::ObserveHealth(request_fields(
        request_id,
        ObserveHealthRequestPayload {},
    )))
}

fn cancel_request(request_id: u64, target_request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Cancel(CancelEnvelope {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: LAUNCH_ID,
        request_id,
        target_request_id,
    })
}

fn send_wire(child: &mut Child, wire: &[u8]) {
    let stdin = child.stdin.as_mut().expect("child stdin must be piped");
    stdin.write_all(wire).expect("wire write must succeed");
    stdin.flush().expect("wire flush must succeed");
}

fn send(child: &mut Child, envelope: &ProtocolEnvelope) {
    let wire = encode_frame(envelope).expect("test envelope must fit frame budget");
    send_wire(child, &wire);
}

fn send_raw_json(child: &mut Child, payload: &[u8]) {
    let declared = u32::try_from(payload.len())
        .expect("bounded raw JSON fixture length must fit u32")
        .to_be_bytes();
    let mut wire = Vec::with_capacity(4 + payload.len());
    wire.extend_from_slice(&declared);
    wire.extend_from_slice(payload);
    send_wire(child, &wire);
}

fn receive(child: &mut Child) -> ProtocolEnvelope {
    read_frame(child.stdout.as_mut().expect("child stdout must be piped"))
        .expect("Core must emit one canonical frame")
}

fn wait_for_exit(child: &mut Child) -> bool {
    let deadline = Instant::now() + PROCESS_EXIT_TIMEOUT;
    loop {
        if let Some(status) = child.try_wait().expect("child status must be readable") {
            return status.success();
        }
        if Instant::now() >= deadline {
            child.kill().expect("timed-out child must be killable");
            let _ = child.wait();
            panic!("Core did not terminate within the bounded test window");
        }
        thread::sleep(PROCESS_POLL_INTERVAL);
    }
}

fn close_input_and_wait(child: &mut Child) -> bool {
    drop(child.stdin.take());
    wait_for_exit(child)
}

fn assert_health_response(envelope: ProtocolEnvelope, request_id: u64) {
    match envelope {
        ProtocolEnvelope::Response(ResponseEnvelope::Health(fields)) => {
            assert_eq!(fields.protocol_version, ProtocolVersion::V1);
            assert_eq!(fields.principal, Principal::DesktopHost);
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, request_id);
            assert_eq!(fields.payload.status, HealthStatus::Healthy);
        }
        other => panic!("unexpected health response: {other:?}"),
    }
}

fn assert_cancel_response(envelope: ProtocolEnvelope, expected: CancellationOutcome) {
    match envelope {
        ProtocolEnvelope::Response(ResponseEnvelope::Cancel(fields)) => {
            assert_eq!(fields.protocol_version, ProtocolVersion::V1);
            assert_eq!(fields.principal, Principal::DesktopHost);
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.payload.outcome, expected);
        }
        other => panic!("unexpected cancel response: {other:?}"),
    }
}

fn canonical_profile() -> CoreProfile {
    CoreProfile::new(
        "0.0.0",
        "s1-011-adversarial",
        CapabilityList::try_from(vec![
            Capability::Health,
            Capability::Version,
            Capability::Capabilities,
            Capability::HealthObservation,
            Capability::Cancellation,
        ])
        .expect("canonical test capabilities must fit budget"),
    )
}

#[test]
fn exact_max_frame_and_normal_round_trip_survive_process_boundary() {
    let mut child = spawn_core();

    send(&mut child, &health_request(1));
    assert_health_response(receive(&mut child), 1);

    let encoded = encode_frame(&health_request(2)).expect("health request must encode");
    let mut payload = encoded[4..].to_vec();
    assert!(payload.len() < MAX_PAYLOAD_BYTES);
    payload.resize(MAX_PAYLOAD_BYTES, b' ');
    let mut exact = Vec::with_capacity(4 + MAX_PAYLOAD_BYTES);
    exact.extend_from_slice(&(MAX_PAYLOAD_BYTES as u32).to_be_bytes());
    exact.extend_from_slice(&payload);
    assert_eq!(exact.len(), MAX_PAYLOAD_BYTES + 4);

    send_wire(&mut child, &exact);
    assert_health_response(receive(&mut child), 2);
    assert!(!close_input_and_wait(&mut child));
}

#[test]
fn zero_oversized_truncated_malformed_and_invalid_utf8_frames_fail_closed() {
    {
        let mut child = spawn_core();
        send_wire(&mut child, &0_u32.to_be_bytes());
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        send_wire(&mut child, &((MAX_PAYLOAD_BYTES as u32) + 1).to_be_bytes());
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        let stdin = child.stdin.as_mut().expect("child stdin must be piped");
        stdin
            .write_all(&8_u32.to_be_bytes())
            .expect("truncated prefix must write");
        stdin
            .write_all(b"{}")
            .expect("truncated body prefix must write");
        stdin.flush().expect("truncated frame must flush");
        drop(child.stdin.take());
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        send_raw_json(&mut child, b"{");
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        send_raw_json(&mut child, &[0xff]);
        assert!(!wait_for_exit(&mut child));
    }
}

#[test]
fn unknown_kind_version_principal_operation_and_downgrade_fail_closed() {
    let cases: [&[u8]; 5] = [
        br#"{"protocol_version":1,"kind":"future_kind","principal":"desktop_host","launch_id":711,"request_id":1,"operation":"health","payload":{}}"#,
        br#"{"protocol_version":2,"kind":"request","principal":"desktop_host","launch_id":711,"request_id":1,"operation":"health","payload":{}}"#,
        br#"{"protocol_version":0,"kind":"request","principal":"desktop_host","launch_id":711,"request_id":1,"operation":"health","payload":{}}"#,
        br#"{"protocol_version":1,"kind":"request","principal":"webview","launch_id":711,"request_id":1,"operation":"health","payload":{}}"#,
        br#"{"protocol_version":1,"kind":"request","principal":"desktop_host","launch_id":711,"request_id":1,"operation":"future_operation","payload":{}}"#,
    ];

    for payload in cases {
        let mut child = spawn_core();
        send_raw_json(&mut child, payload);
        assert!(!wait_for_exit(&mut child));
    }
}

#[test]
fn replay_non_monotonic_and_stale_launch_fail_closed() {
    {
        let mut child = spawn_core();
        send(&mut child, &health_request(2));
        assert_health_response(receive(&mut child), 2);
        send(&mut child, &health_request(1));
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        send(&mut child, &health_request(1));
        assert_health_response(receive(&mut child), 1);
        send(&mut child, &health_request(1));
        assert!(!wait_for_exit(&mut child));
    }

    {
        let mut child = spawn_core();
        send(&mut child, &health_request(1));
        assert_health_response(receive(&mut child), 1);
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
}

#[test]
fn terminal_cache_eviction_never_reopens_old_command_ids() {
    let mut child = spawn_core();

    for request_id in 1..=(MAX_TERMINAL_RESULTS as u64 + 2) {
        send(&mut child, &health_request(request_id));
        assert_health_response(receive(&mut child), request_id);
    }

    send(&mut child, &health_request(1));
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn duplicate_observation_cannot_allocate_a_second_watch() {
    let mut child = spawn_core();

    send(&mut child, &observe_request(1));
    assert!(matches!(
        receive(&mut child),
        ProtocolEnvelope::Response(ResponseEnvelope::ObserveHealth(_))
    ));

    send(&mut child, &observe_request(1));
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn cancellation_unknown_terminal_replay_and_pre_target_race_are_deterministic() {
    let mut child = spawn_core();

    send(&mut child, &cancel_request(1, 2));
    assert_cancel_response(receive(&mut child), CancellationOutcome::UnknownTarget);

    send(&mut child, &observe_request(2));
    assert!(matches!(
        receive(&mut child),
        ProtocolEnvelope::Response(ResponseEnvelope::ObserveHealth(_))
    ));

    send(&mut child, &cancel_request(3, 2));
    assert_cancel_response(receive(&mut child), CancellationOutcome::Cancelled);

    send(&mut child, &cancel_request(4, 2));
    assert_cancel_response(receive(&mut child), CancellationOutcome::AlreadyTerminal);

    send(&mut child, &health_request(5));
    assert_health_response(receive(&mut child), 5);

    send(&mut child, &cancel_request(6, 5));
    assert_cancel_response(receive(&mut child), CancellationOutcome::AlreadyTerminal);

    send(&mut child, &cancel_request(6, 5));
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn health_watch_budget_exhaustion_is_fail_closed() {
    let mut child = spawn_core();

    for request_id in 1..=(MAX_HEALTH_WATCHES as u64) {
        send(&mut child, &observe_request(request_id));
        assert!(matches!(
            receive(&mut child),
            ProtocolEnvelope::Response(ResponseEnvelope::ObserveHealth(_))
        ));
    }

    send(&mut child, &observe_request(MAX_HEALTH_WATCHES as u64 + 1));
    assert!(!wait_for_exit(&mut child));
}

#[test]
fn in_flight_budget_exhaustion_remains_bounded_before_dispatch() {
    let mut state = HandshakeState::new(LAUNCH_ID, canonical_profile(), HealthStatus::Healthy);

    for request_id in 1..=(MAX_IN_FLIGHT_REQUESTS as u64) {
        let _ = state
            .accept_request(match health_request(request_id) {
                ProtocolEnvelope::Request(request) => request,
                _ => unreachable!("health helper always returns a request"),
            })
            .expect("in-flight reservation within budget must succeed");
    }

    let error = state
        .accept_request(match health_request(MAX_IN_FLIGHT_REQUESTS as u64 + 1) {
            ProtocolEnvelope::Request(request) => request,
            _ => unreachable!("health helper always returns a request"),
        })
        .expect_err("first request over the in-flight budget must fail");

    assert_eq!(
        error,
        StateError::InFlightBudgetExhausted {
            max: MAX_IN_FLIGHT_REQUESTS,
        }
    );
}
