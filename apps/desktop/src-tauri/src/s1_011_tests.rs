use super::*;

use std::io::{Read, Write};
use std::path::Path;
use std::time::{Duration, Instant};

use wepld_contracts::{
    CancelResponsePayload, CancellationOutcome, EventFields, HealthObservationEventPayload,
    HealthResponsePayload, HealthStatus, ObserveHealthResponsePayload, ResponseFields,
};

const FAKE_CORE_HELPER_ENV: &str = "WEPLD_S1_011_FAKE_CORE_HELPER";
const FAKE_CORE_READY_MARKER: &[u8] = b"WEPLD_S1_011_FAKE_CORE_READY\n";
const FAKE_CORE_HELPER_TEST: &str = "core_client::s1_011_tests::fake_core_stderr_flood_helper";
const TEST_POLL_INTERVAL: Duration = Duration::from_millis(5);
const TEST_TIMEOUT: Duration = Duration::from_secs(5);

fn build_test_client(
    child: Child,
    input: ChildStdin,
    output: ChildStdout,
    diagnostic_rx: mpsc::Receiver<Vec<u8>>,
    diagnostics_truncated: Arc<AtomicBool>,
    diagnostic_thread: thread::JoinHandle<()>,
) -> Result<CoreClient, CoreClientError> {
    let ready = Arc::new(AtomicBool::new(false));
    let io_state = Arc::new(Mutex::new(LaunchIoState::default()));
    let (writer_tx, writer_thread) =
        spawn_protocol_writer(input, Arc::clone(&ready), Arc::clone(&io_state));
    let (inbound_rx, protocol_thread) =
        spawn_protocol_reader(output, Arc::clone(&ready), Arc::clone(&io_state));

    Ok(CoreClient {
        child,
        writer_tx: Some(writer_tx),
        writer_thread: Some(writer_thread),
        inbound_rx,
        io_state,
        protocol_thread: Some(protocol_thread),
        diagnostic_rx,
        diagnostics_truncated,
        diagnostic_thread: Some(diagnostic_thread),
        launch_id: fresh_launch_id()?,
        next_command_id: INITIAL_COMMAND_ID,
        ready,
    })
}

fn spawn_test_client(path: &Path, args: &[&str]) -> Result<CoreClient, CoreClientError> {
    let mut child = Command::new(path)
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    let input = child
        .stdin
        .take()
        .ok_or(CoreClientError::MissingChildStdin)?;
    let output = child
        .stdout
        .take()
        .ok_or(CoreClientError::MissingChildStdout)?;
    let stderr = child
        .stderr
        .take()
        .ok_or(CoreClientError::MissingChildStderr)?;
    let (diagnostic_tx, diagnostic_rx) = mpsc::sync_channel(DIAGNOSTIC_CHANNEL_CAPACITY);
    let diagnostics_truncated = Arc::new(AtomicBool::new(false));
    let diagnostic_thread =
        spawn_stderr_drain(stderr, diagnostic_tx, Arc::clone(&diagnostics_truncated));

    build_test_client(
        child,
        input,
        output,
        diagnostic_rx,
        diagnostics_truncated,
        diagnostic_thread,
    )
}

fn read_until_marker(output: &mut ChildStdout) -> Result<(), CoreClientError> {
    let mut observed = Vec::new();
    let mut byte = [0_u8; 1];
    while !observed.ends_with(FAKE_CORE_READY_MARKER) {
        output.read_exact(&mut byte)?;
        observed.push(byte[0]);
        if observed.len() > 16_384 {
            return Err(CoreClientError::UnexpectedInboundKind);
        }
    }
    Ok(())
}

fn spawn_stderr_flood_client() -> Result<CoreClient, CoreClientError> {
    let current = std::env::current_exe()?;
    let mut child = Command::new(current)
        .arg("--exact")
        .arg(FAKE_CORE_HELPER_TEST)
        .arg("--nocapture")
        .env(FAKE_CORE_HELPER_ENV, "1")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    let input = child
        .stdin
        .take()
        .ok_or(CoreClientError::MissingChildStdin)?;
    let mut output = child
        .stdout
        .take()
        .ok_or(CoreClientError::MissingChildStdout)?;
    let stderr = child
        .stderr
        .take()
        .ok_or(CoreClientError::MissingChildStderr)?;
    let (diagnostic_tx, diagnostic_rx) = mpsc::sync_channel(DIAGNOSTIC_CHANNEL_CAPACITY);
    let diagnostics_truncated = Arc::new(AtomicBool::new(false));
    let diagnostic_thread =
        spawn_stderr_drain(stderr, diagnostic_tx, Arc::clone(&diagnostics_truncated));

    read_until_marker(&mut output)?;

    build_test_client(
        child,
        input,
        output,
        diagnostic_rx,
        diagnostics_truncated,
        diagnostic_thread,
    )
}

fn wait_until_child_exits(client: &mut CoreClient) {
    let deadline = Instant::now() + TEST_TIMEOUT;
    loop {
        if client
            .child
            .try_wait()
            .expect("owned child status must remain readable")
            .is_some()
        {
            return;
        }
        if Instant::now() >= deadline {
            panic!("owned child did not exit within the bounded test window");
        }
        thread::sleep(TEST_POLL_INTERVAL);
    }
}

fn health_response(launch_id: u64, request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Response(ResponseEnvelope::Health(ResponseFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: HealthResponsePayload {
            status: HealthStatus::Healthy,
        },
    }))
}

fn observation_event(launch_id: u64, request_id: u64) -> ProtocolEnvelope {
    ProtocolEnvelope::Event(EventEnvelope::ObserveHealth(EventFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: HealthObservationEventPayload {
            sequence: 1,
            status: HealthStatus::Degraded,
        },
    }))
}

#[test]
fn fake_core_stderr_flood_helper() {
    if std::env::var_os(FAKE_CORE_HELPER_ENV).is_none() {
        return;
    }

    let mut stdout = std::io::stdout().lock();
    stdout
        .write_all(FAKE_CORE_READY_MARKER)
        .expect("fake Core ready marker must write");
    stdout.flush().expect("fake Core ready marker must flush");

    let mut stderr = std::io::stderr().lock();
    let diagnostic_chunk = [b'd'; DIAGNOSTIC_READ_CHUNK_BYTES];
    for _ in 0..512 {
        stderr
            .write_all(&diagnostic_chunk)
            .expect("fake Core diagnostic flood must write");
    }
    stderr
        .flush()
        .expect("fake Core diagnostic flood must flush");

    let mut stdin = std::io::stdin().lock();
    let request: ProtocolEnvelope =
        read_frame(&mut stdin).expect("fake Core must receive health request");
    let fields = match request {
        ProtocolEnvelope::Request(RequestEnvelope::Health(fields)) => fields,
        other => panic!("fake Core expected health request, got {other:?}"),
    };
    let response = ProtocolEnvelope::Response(ResponseEnvelope::Health(ResponseFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id: fields.launch_id,
        request_id: fields.request_id,
        payload: HealthResponsePayload {
            status: HealthStatus::Healthy,
        },
    }));
    let wire = encode_frame(&response).expect("fake Core health response must encode");
    stdout
        .write_all(&wire)
        .expect("fake Core health response must write");
    stdout
        .flush()
        .expect("fake Core health response must flush");

    let mut sink = [0_u8; 1];
    while stdin.read(&mut sink).unwrap_or(0) != 0 {}
}

#[test]
fn missing_and_mismatched_core_binaries_fail_closed() {
    let current = std::env::current_exe().expect("test executable path must resolve");
    let missing = current.with_file_name(format!(
        "__wepld_s1_011_missing_core_{}__",
        std::process::id()
    ));

    match spawn_test_client(&missing, &[]) {
        Err(CoreClientError::Io(error)) => {
            assert_eq!(error.kind(), std::io::ErrorKind::NotFound);
        }
        Err(other) => panic!("missing Core must fail as IO not-found, got {other:?}"),
        Ok(mut client) => {
            let _ = client.stop_child();
            panic!("missing Core path unexpectedly spawned");
        }
    }

    let mut mismatched = spawn_test_client(&current, &["--list"])
        .expect("current test executable must spawn as a mismatched fixture");
    let result = mismatched
        .send_health()
        .and_then(|_| mismatched.receive().map(|_| ()));
    assert!(result.is_err());
    assert!(!mismatched.is_ready());
}

#[test]
fn core_crash_invalidates_then_restart_uses_fresh_launch() {
    let mut client = CoreClient::start().expect("owned Core must start");
    let request_id = client.send_health().expect("health request must enqueue");
    let _ = client.receive().expect("health response must arrive");
    assert_eq!(request_id, INITIAL_COMMAND_ID);
    assert!(client.is_ready());
    let prior_launch = client.launch_id();

    client
        .child
        .kill()
        .expect("owned Core must accept termination");
    wait_until_child_exits(&mut client);

    let error = client
        .send_health()
        .expect_err("exited Core must reject new command");
    assert!(matches!(error, CoreClientError::ChildExited));
    assert!(!client.is_ready());

    client.restart().expect("explicit restart must succeed");
    assert_ne!(client.launch_id(), prior_launch);
    assert!(!client.is_ready());
    let next = client
        .send_health()
        .expect("fresh launch health request must enqueue");
    assert_eq!(next, INITIAL_COMMAND_ID);
    let _ = client.receive().expect("fresh launch response must arrive");
    assert!(client.is_ready());
}

#[test]
fn writer_and_reader_loss_are_terminal_and_non_recovering() {
    {
        let mut client = CoreClient::start().expect("owned Core must start");
        let _ = client.writer_tx.take();
        let error = client
            .send_health()
            .expect_err("missing writer channel must fail closed");
        assert!(matches!(error, CoreClientError::WriterChannelClosed));
        assert!(!client.is_ready());
    }

    {
        let mut client = CoreClient::start().expect("owned Core must start");
        {
            let mut state = lock_io_state(&client.io_state);
            state.reader_terminated = true;
            client.ready.store(false, Ordering::Release);
        }
        let error = client
            .send_health()
            .expect_err("terminal reader state must reject outbound command");
        assert!(matches!(error, CoreClientError::ReaderTerminated));
        assert!(!client.is_ready());
    }
}

#[test]
fn stale_response_and_event_after_restart_fail_closed() {
    {
        let mut client = CoreClient::start().expect("owned Core must start");
        let prior_launch = client.launch_id();
        client.restart().expect("restart must succeed");
        let current_launch = client.launch_id();
        assert_ne!(current_launch, prior_launch);

        let error = client
            .accept_inbound(health_response(prior_launch, INITIAL_COMMAND_ID))
            .expect_err("stale response must fail closed");
        assert!(matches!(
            error,
            CoreClientError::StaleLaunch {
                expected,
                actual
            } if expected == current_launch && actual == prior_launch
        ));
        assert!(!client.is_ready());
    }

    {
        let mut client = CoreClient::start().expect("owned Core must start");
        let prior_launch = client.launch_id();
        client.restart().expect("restart must succeed");
        let current_launch = client.launch_id();

        let error = client
            .accept_inbound(observation_event(prior_launch, INITIAL_COMMAND_ID))
            .expect_err("stale event must fail closed");
        assert!(matches!(
            error,
            CoreClientError::StaleLaunch {
                expected,
                actual
            } if expected == current_launch && actual == prior_launch
        ));
        assert!(!client.is_ready());
    }
}

#[test]
fn event_delivery_and_cancellation_preserve_request_identity() {
    let mut client = CoreClient::start().expect("owned Core must start");
    let observation_id = client
        .send_observe_health()
        .expect("observation request must enqueue");
    let acknowledgement = client.receive().expect("observation ack must arrive");
    assert!(matches!(
        acknowledgement,
        InboundEnvelope::Response(ResponseEnvelope::ObserveHealth(ResponseFields {
            payload: ObserveHealthResponsePayload {},
            ..
        }))
    ));

    let event = client
        .accept_inbound(observation_event(client.launch_id(), observation_id))
        .expect("current-launch observation event must be accepted");
    assert!(matches!(
        event,
        InboundEnvelope::Event(EventEnvelope::ObserveHealth(EventFields {
            request_id,
            ..
        })) if request_id == observation_id
    ));

    let cancel_id = client
        .send_cancel(observation_id)
        .expect("cancel request must enqueue");
    assert_eq!(cancel_id, observation_id + 1);
    let cancellation = client.receive().expect("cancel response must arrive");
    assert!(matches!(
        cancellation,
        InboundEnvelope::Response(ResponseEnvelope::Cancel(ResponseFields {
            request_id,
            payload: CancelResponsePayload {
                outcome: CancellationOutcome::Cancelled
            },
            ..
        })) if request_id == cancel_id
    ));
}

#[test]
fn desktop_owned_child_cleanup_is_bounded_and_observable() {
    let mut client = CoreClient::start().expect("owned Core must start");
    let _ = client.send_health().expect("health request must enqueue");
    let _ = client.receive().expect("health response must arrive");
    assert!(client.is_ready());

    client
        .stop_child()
        .expect("owned child cleanup must succeed");
    assert!(!client.is_ready());
    assert!(
        client
            .child
            .try_wait()
            .expect("cleaned child status must remain readable")
            .is_some()
    );
}

#[test]
fn stderr_pressure_beyond_retained_capacity_does_not_block_protocol_round_trip() {
    let mut client = spawn_stderr_flood_client().expect("frozen stderr-flood helper must start");

    let request_id = client.send_health().expect("health request must enqueue");
    let response = client
        .receive()
        .expect("protocol response must survive diagnostic pressure");
    assert!(matches!(
        response,
        InboundEnvelope::Response(ResponseEnvelope::Health(ResponseFields {
            request_id: observed,
            ..
        })) if observed == request_id
    ));

    let deadline = Instant::now() + TEST_TIMEOUT;
    while !client.diagnostics_truncated() && Instant::now() < deadline {
        thread::sleep(TEST_POLL_INTERVAL);
    }
    assert!(client.diagnostics_truncated());

    let retained = client.drain_diagnostics();
    assert!(retained.len() <= MAX_RETAINED_DIAGNOSTIC_BYTES);

    client
        .stop_child()
        .expect("frozen stderr-flood helper cleanup must succeed");
}
