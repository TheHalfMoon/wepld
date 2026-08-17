#![forbid(unsafe_code)]

use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, mpsc};
use std::thread;

use wepld_contracts::CancelEnvelope;
use wepld_contracts::CapabilitiesRequestPayload;
use wepld_contracts::EventEnvelope;
use wepld_contracts::FrameError;
use wepld_contracts::HealthRequestPayload;
use wepld_contracts::ObserveHealthRequestPayload;
use wepld_contracts::Principal;
use wepld_contracts::ProtocolEnvelope;
use wepld_contracts::ProtocolErrorEnvelope;
use wepld_contracts::ProtocolVersion;
use wepld_contracts::RequestEnvelope;
use wepld_contracts::RequestFields;
use wepld_contracts::ResponseEnvelope;
use wepld_contracts::VersionRequestPayload;
use wepld_contracts::encode_frame;
use wepld_contracts::read_frame;

#[cfg(target_os = "windows")]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core.exe";
#[cfg(not(target_os = "windows"))]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core";

const DIAGNOSTIC_CHANNEL_CAPACITY: usize = 16;
const DIAGNOSTIC_READ_CHUNK_BYTES: usize = 4_096;
const MAX_RETAINED_DIAGNOSTIC_BYTES: usize =
    DIAGNOSTIC_CHANNEL_CAPACITY * DIAGNOSTIC_READ_CHUNK_BYTES;
const _: () = assert!(MAX_RETAINED_DIAGNOSTIC_BYTES == 65_536);

const INBOUND_CHANNEL_CAPACITY: usize = 32;
const OUTBOUND_CHANNEL_CAPACITY: usize = 32;
const PROTOCOL_RESPONSE_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(5);
const CHILD_TERMINATION_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(5);
const CHILD_TERMINATION_POLL_INTERVAL: std::time::Duration = std::time::Duration::from_millis(5);
const INITIAL_COMMAND_ID: u64 = 1;

static NEXT_LAUNCH_ID: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);

#[derive(Debug)]
pub enum CoreClientError {
    Io(std::io::Error),
    Frame(FrameError),
    MissingExecutableParent,
    MissingChildStdin,
    MissingChildStdout,
    MissingChildStderr,
    ChildExited,
    ProtocolTimeout,
    ChildTerminationTimeout,
    InboundChannelClosed,
    InboundOverflow,
    OutboundOverflow,
    WriterChannelClosed,
    WriterFailed,
    UnexpectedInboundKind,
    StaleLaunch { expected: u64, actual: u64 },
    CommandIdExhausted,
    LaunchIdExhausted,
}

impl From<std::io::Error> for CoreClientError {
    fn from(error: std::io::Error) -> Self {
        Self::Io(error)
    }
}

impl From<FrameError> for CoreClientError {
    fn from(error: FrameError) -> Self {
        Self::Frame(error)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InboundEnvelope {
    Response(ResponseEnvelope),
    Event(EventEnvelope),
    ProtocolError(ProtocolErrorEnvelope),
}

pub struct CoreClient {
    child: Child,
    writer_tx: Option<mpsc::SyncSender<Vec<u8>>>,
    writer_failed: Arc<AtomicBool>,
    writer_thread: Option<thread::JoinHandle<()>>,
    inbound_rx: mpsc::Receiver<Result<ProtocolEnvelope, FrameError>>,
    inbound_overflowed: Arc<AtomicBool>,
    protocol_thread: Option<thread::JoinHandle<()>>,
    diagnostic_rx: mpsc::Receiver<Vec<u8>>,
    diagnostics_truncated: Arc<AtomicBool>,
    diagnostic_thread: Option<thread::JoinHandle<()>>,
    launch_id: u64,
    next_command_id: u64,
    ready: Arc<AtomicBool>,
}

fn fresh_launch_id() -> Result<u64, CoreClientError> {
    NEXT_LAUNCH_ID
        .fetch_update(Ordering::AcqRel, Ordering::Acquire, |current| {
            current.checked_add(1)
        })
        .map_err(|_| CoreClientError::LaunchIdExhausted)
}

fn resolve_owned_core_sibling() -> Result<std::path::PathBuf, CoreClientError> {
    let current_exe = std::env::current_exe()?;
    let core_parent = current_exe
        .parent()
        .ok_or(CoreClientError::MissingExecutableParent)?;
    Ok(core_parent.join(CORE_EXECUTABLE_FILENAME))
}

fn spawn_stderr_drain(
    mut stderr: ChildStderr,
    diagnostic_tx: mpsc::SyncSender<Vec<u8>>,
    diagnostics_truncated: Arc<AtomicBool>,
) -> thread::JoinHandle<()> {
    thread::spawn(move || {
        let mut buffer = [0_u8; DIAGNOSTIC_READ_CHUNK_BYTES];
        loop {
            let read = match std::io::Read::read(&mut stderr, &mut buffer) {
                Ok(0) => break,
                Ok(read) => read,
                Err(_) => break,
            };
            if diagnostic_tx.try_send(buffer[..read].to_vec()).is_err() {
                diagnostics_truncated.store(true, Ordering::Release);
            }
        }
    })
}

#[allow(clippy::type_complexity)]
fn spawn_owned_core() -> Result<
    (
        Child,
        ChildStdin,
        ChildStdout,
        mpsc::Receiver<Vec<u8>>,
        Arc<AtomicBool>,
        thread::JoinHandle<()>,
    ),
    CoreClientError,
> {
    let core_executable = resolve_owned_core_sibling()?;
    let mut child = Command::new(core_executable.as_os_str())
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
    Ok((
        child,
        input,
        output,
        diagnostic_rx,
        diagnostics_truncated,
        diagnostic_thread,
    ))
}

fn spawn_protocol_writer(
    mut input: ChildStdin,
    ready: Arc<AtomicBool>,
) -> (
    mpsc::SyncSender<Vec<u8>>,
    Arc<AtomicBool>,
    thread::JoinHandle<()>,
) {
    let (writer_tx, writer_rx) = mpsc::sync_channel(OUTBOUND_CHANNEL_CAPACITY);
    let writer_failed = Arc::new(AtomicBool::new(false));
    let failure_flag = Arc::clone(&writer_failed);
    let writer_thread = thread::spawn(move || {
        while let Ok(wire) = writer_rx.recv() {
            let write_result = std::io::Write::write_all(&mut input, &wire)
                .and_then(|()| std::io::Write::flush(&mut input));
            if write_result.is_err() {
                failure_flag.store(true, Ordering::Release);
                ready.store(false, Ordering::Release);
                break;
            }
        }
    });
    (writer_tx, writer_failed, writer_thread)
}

fn spawn_protocol_reader(
    mut output: ChildStdout,
    ready: Arc<AtomicBool>,
) -> (
    mpsc::Receiver<Result<ProtocolEnvelope, FrameError>>,
    Arc<AtomicBool>,
    thread::JoinHandle<()>,
) {
    let (inbound_tx, inbound_rx) = mpsc::sync_channel(INBOUND_CHANNEL_CAPACITY);
    let inbound_overflowed = Arc::new(AtomicBool::new(false));
    let overflow_flag = Arc::clone(&inbound_overflowed);
    let protocol_thread = thread::spawn(move || {
        loop {
            let inbound = read_frame::<_, ProtocolEnvelope>(&mut output);
            let terminal = inbound.is_err();
            if terminal {
                ready.store(false, Ordering::Release);
            }
            if inbound_tx.try_send(inbound).is_err() {
                overflow_flag.store(true, Ordering::Release);
                ready.store(false, Ordering::Release);
            }
            if terminal {
                break;
            }
        }
    });
    (inbound_rx, inbound_overflowed, protocol_thread)
}

fn enqueue_wire(
    writer_tx: &mpsc::SyncSender<Vec<u8>>,
    wire: Vec<u8>,
) -> Result<(), mpsc::TrySendError<Vec<u8>>> {
    writer_tx.try_send(wire)
}

fn launch_id_of(envelope: &InboundEnvelope) -> u64 {
    match envelope {
        InboundEnvelope::Response(response) => match response {
            ResponseEnvelope::Health(fields) => fields.launch_id,
            ResponseEnvelope::Version(fields) => fields.launch_id,
            ResponseEnvelope::Capabilities(fields) => fields.launch_id,
            ResponseEnvelope::ObserveHealth(fields) => fields.launch_id,
            ResponseEnvelope::Cancel(fields) => fields.launch_id,
        },
        InboundEnvelope::Event(event) => match event {
            EventEnvelope::ObserveHealth(fields) => fields.launch_id,
        },
        InboundEnvelope::ProtocolError(error) => error.launch_id,
    }
}

impl CoreClient {
    pub fn start() -> Result<Self, CoreClientError> {
        let launch_id = fresh_launch_id()?;
        let (child, input, output, diagnostic_rx, diagnostics_truncated, diagnostic_thread) =
            spawn_owned_core()?;
        let ready = Arc::new(AtomicBool::new(false));
        let (writer_tx, writer_failed, writer_thread) =
            spawn_protocol_writer(input, Arc::clone(&ready));
        let (inbound_rx, inbound_overflowed, protocol_thread) =
            spawn_protocol_reader(output, Arc::clone(&ready));
        Ok(Self {
            child,
            writer_tx: Some(writer_tx),
            writer_failed,
            writer_thread: Some(writer_thread),
            inbound_rx,
            inbound_overflowed,
            protocol_thread: Some(protocol_thread),
            diagnostic_rx,
            diagnostics_truncated,
            diagnostic_thread: Some(diagnostic_thread),
            launch_id,
            next_command_id: INITIAL_COMMAND_ID,
            ready,
        })
    }

    pub fn launch_id(&self) -> u64 {
        self.launch_id
    }

    pub fn is_ready(&self) -> bool {
        self.ready.load(Ordering::Acquire)
    }

    pub fn diagnostics_truncated(&self) -> bool {
        self.diagnostics_truncated.load(Ordering::Acquire)
    }

    pub fn drain_diagnostics(&self) -> Vec<u8> {
        let mut retained = Vec::new();
        while retained.len() < MAX_RETAINED_DIAGNOSTIC_BYTES {
            match self.diagnostic_rx.try_recv() {
                Ok(chunk) => {
                    let remaining = MAX_RETAINED_DIAGNOSTIC_BYTES - retained.len();
                    let accepted = chunk.len().min(remaining);
                    retained.extend_from_slice(&chunk[..accepted]);
                    if accepted != chunk.len() {
                        self.diagnostics_truncated.store(true, Ordering::Release);
                        break;
                    }
                }
                Err(mpsc::TryRecvError::Empty) | Err(mpsc::TryRecvError::Disconnected) => break,
            }
        }
        retained
    }

    pub fn send_health(&mut self) -> Result<u64, CoreClientError> {
        let request_id = self.allocate_command_id()?;
        let envelope = ProtocolEnvelope::Request(RequestEnvelope::Health(RequestFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id,
            payload: HealthRequestPayload {},
        }));
        self.write_envelope(&envelope)?;
        Ok(request_id)
    }

    pub fn send_version(&mut self) -> Result<u64, CoreClientError> {
        let request_id = self.allocate_command_id()?;
        let envelope = ProtocolEnvelope::Request(RequestEnvelope::Version(RequestFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id,
            payload: VersionRequestPayload {},
        }));
        self.write_envelope(&envelope)?;
        Ok(request_id)
    }

    pub fn send_capabilities(&mut self) -> Result<u64, CoreClientError> {
        let request_id = self.allocate_command_id()?;
        let envelope = ProtocolEnvelope::Request(RequestEnvelope::Capabilities(RequestFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id,
            payload: CapabilitiesRequestPayload {},
        }));
        self.write_envelope(&envelope)?;
        Ok(request_id)
    }

    pub fn send_observe_health(&mut self) -> Result<u64, CoreClientError> {
        let request_id = self.allocate_command_id()?;
        let envelope = ProtocolEnvelope::Request(RequestEnvelope::ObserveHealth(RequestFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id,
            payload: ObserveHealthRequestPayload {},
        }));
        self.write_envelope(&envelope)?;
        Ok(request_id)
    }

    pub fn send_cancel(&mut self, target_request_id: u64) -> Result<u64, CoreClientError> {
        let request_id = self.allocate_command_id()?;
        let envelope = ProtocolEnvelope::Cancel(CancelEnvelope {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id,
            target_request_id,
        });
        self.write_envelope(&envelope)?;
        Ok(request_id)
    }

    pub fn receive(&mut self) -> Result<InboundEnvelope, CoreClientError> {
        self.ensure_child_running()?;
        if self.writer_failed.load(Ordering::Acquire) {
            let error = self.stop_with_error(CoreClientError::WriterFailed);
            Err(error)
        } else if self.inbound_overflowed.load(Ordering::Acquire) {
            let error = self.stop_with_error(CoreClientError::InboundOverflow);
            Err(error)
        } else {
            match self.inbound_rx.recv_timeout(PROTOCOL_RESPONSE_TIMEOUT) {
                Ok(Ok(envelope)) => self.accept_inbound(envelope),
                Ok(Err(error)) => {
                    let error = self.stop_with_error(CoreClientError::Frame(error));
                    Err(error)
                }
                Err(mpsc::RecvTimeoutError::Timeout) => {
                    let error = self.stop_with_error(CoreClientError::ProtocolTimeout);
                    Err(error)
                }
                Err(mpsc::RecvTimeoutError::Disconnected) => {
                    let error = self.stop_with_error(CoreClientError::InboundChannelClosed);
                    Err(error)
                }
            }
        }
    }

    pub fn restart(&mut self) -> Result<(), CoreClientError> {
        self.stop_child()?;
        let launch_id = fresh_launch_id()?;
        let (child, input, output, diagnostic_rx, diagnostics_truncated, diagnostic_thread) =
            spawn_owned_core()?;
        let ready = Arc::new(AtomicBool::new(false));
        let (writer_tx, writer_failed, writer_thread) =
            spawn_protocol_writer(input, Arc::clone(&ready));
        let (inbound_rx, inbound_overflowed, protocol_thread) =
            spawn_protocol_reader(output, Arc::clone(&ready));
        self.child = child;
        self.writer_tx = Some(writer_tx);
        self.writer_failed = writer_failed;
        self.writer_thread = Some(writer_thread);
        self.inbound_rx = inbound_rx;
        self.inbound_overflowed = inbound_overflowed;
        self.protocol_thread = Some(protocol_thread);
        self.diagnostic_rx = diagnostic_rx;
        self.diagnostics_truncated = diagnostics_truncated;
        self.diagnostic_thread = Some(diagnostic_thread);
        self.launch_id = launch_id;
        self.next_command_id = INITIAL_COMMAND_ID;
        self.ready = ready;
        Ok(())
    }

    fn allocate_command_id(&mut self) -> Result<u64, CoreClientError> {
        let request_id = self.next_command_id;
        self.next_command_id = self
            .next_command_id
            .checked_add(1)
            .ok_or(CoreClientError::CommandIdExhausted)?;
        Ok(request_id)
    }

    fn write_envelope(&mut self, envelope: &ProtocolEnvelope) -> Result<(), CoreClientError> {
        self.ensure_child_running()?;
        if self.writer_failed.load(Ordering::Acquire) {
            let error = self.stop_with_error(CoreClientError::WriterFailed);
            Err(error)
        } else {
            match encode_frame(envelope) {
                Ok(wire) => match self.writer_tx.as_ref() {
                    Some(writer_tx) => match enqueue_wire(writer_tx, wire) {
                        Ok(()) => Ok(()),
                        Err(mpsc::TrySendError::Full(_)) => {
                            let error = self.stop_with_error(CoreClientError::OutboundOverflow);
                            Err(error)
                        }
                        Err(mpsc::TrySendError::Disconnected(_)) => {
                            let error =
                                self.stop_with_error(CoreClientError::WriterChannelClosed);
                            Err(error)
                        }
                    },
                    None => {
                        let error = self.stop_with_error(CoreClientError::WriterChannelClosed);
                        Err(error)
                    }
                },
                Err(error) => {
                    let error = self.stop_with_error(CoreClientError::Frame(error));
                    Err(error)
                }
            }
        }
    }

    fn ensure_child_running(&mut self) -> Result<(), CoreClientError> {
        match self.child.try_wait() {
            Ok(Some(_)) => {
                let error = self.stop_with_error(CoreClientError::ChildExited);
                Err(error)
            }
            Ok(None) => Ok(()),
            Err(error) => {
                let error = self.stop_with_error(CoreClientError::Io(error));
                Err(error)
            }
        }
    }

    fn accept_inbound(
        &mut self,
        envelope: ProtocolEnvelope,
    ) -> Result<InboundEnvelope, CoreClientError> {
        let inbound = match envelope {
            ProtocolEnvelope::Response(response) => InboundEnvelope::Response(response),
            ProtocolEnvelope::Event(event) => InboundEnvelope::Event(event),
            ProtocolEnvelope::ProtocolError(error) => InboundEnvelope::ProtocolError(error),
            ProtocolEnvelope::Request(_) | ProtocolEnvelope::Cancel(_) => {
                let error = self.stop_with_error(CoreClientError::UnexpectedInboundKind);
                Err(error)?
            }
        };
        let actual = launch_id_of(&inbound);
        if actual != self.launch_id {
            let error = self.stop_with_error(CoreClientError::StaleLaunch {
                expected: self.launch_id,
                actual,
            });
            Err(error)
        } else {
            self.ready.store(true, Ordering::Release);
            Ok(inbound)
        }
    }

    fn stop_with_error(&mut self, original: CoreClientError) -> CoreClientError {
        match self.stop_child() {
            Ok(()) => original,
            Err(cleanup_error) => cleanup_error,
        }
    }

    fn stop_child(&mut self) -> Result<(), CoreClientError> {
        self.ready.store(false, Ordering::Release);
        let _ = self.writer_tx.take();
        let termination = match self.child.try_wait() {
            Ok(Some(_)) => Ok(()),
            Ok(None) => {
                let _ = self.child.kill();
                let deadline = std::time::Instant::now() + CHILD_TERMINATION_TIMEOUT;
                let mut outcome = Err(CoreClientError::ChildTerminationTimeout);
                while std::time::Instant::now() < deadline {
                    match self.child.try_wait() {
                        Ok(Some(_)) => {
                            outcome = Ok(());
                            break;
                        }
                        Ok(None) => thread::sleep(CHILD_TERMINATION_POLL_INTERVAL),
                        Err(error) => {
                            outcome = Err(CoreClientError::Io(error));
                            break;
                        }
                    }
                }
                outcome
            }
            Err(error) => Err(CoreClientError::Io(error)),
        };
        let _ = self.writer_thread.take();
        let _ = self.protocol_thread.take();
        let _ = self.diagnostic_thread.take();
        termination
    }
}

impl Drop for CoreClient {
    fn drop(&mut self) {
        let _ = self.stop_child();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use wepld_contracts::{HealthStatus, ResponseEnvelope};

    fn health_response(
        inbound: InboundEnvelope,
    ) -> wepld_contracts::ResponseFields<wepld_contracts::HealthResponsePayload> {
        match inbound {
            InboundEnvelope::Response(ResponseEnvelope::Health(fields)) => fields,
            other => panic!("expected health response, got {other:?}"),
        }
    }

    #[test]
    fn outbound_enqueue_is_bounded_and_nonblocking() {
        let (writer_tx, _writer_rx) = mpsc::sync_channel(1);
        enqueue_wire(&writer_tx, vec![1]).expect("first frame must fit bounded queue");
        let error = enqueue_wire(&writer_tx, vec![2]).expect_err("full queue must reject immediately");
        assert!(matches!(error, mpsc::TrySendError::Full(_)));
    }

    #[test]
    fn owned_core_health_round_trip_binds_internal_identity() {
        let mut client = CoreClient::start().expect("owned Core must start");
        assert!(!client.is_ready());

        let request_id = client.send_health().expect("health request must enqueue");
        assert_eq!(request_id, INITIAL_COMMAND_ID);

        let response = health_response(client.receive().expect("health response must arrive"));
        assert_eq!(response.protocol_version, ProtocolVersion::V1);
        assert_eq!(response.principal, Principal::DesktopHost);
        assert_eq!(response.launch_id, client.launch_id());
        assert_eq!(response.request_id, request_id);
        assert_eq!(response.payload.status, HealthStatus::Healthy);
        assert!(client.is_ready());
    }

    #[test]
    fn command_ids_follow_serialized_write_order() {
        let mut client = CoreClient::start().expect("owned Core must start");

        let first = client.send_health().expect("first command must enqueue");
        let _ = client.receive().expect("first response must arrive");
        let second = client.send_version().expect("second command must enqueue");
        let _ = client.receive().expect("second response must arrive");
        let third = client
            .send_capabilities()
            .expect("third command must enqueue");
        let _ = client.receive().expect("third response must arrive");

        assert_eq!((first, second, third), (1, 2, 3));
    }

    #[test]
    fn explicit_restart_changes_launch_and_invalidates_readiness() {
        let mut client = CoreClient::start().expect("owned Core must start");
        let _ = client.send_health().expect("health request must enqueue");
        let _ = client.receive().expect("health response must arrive");
        let prior_launch = client.launch_id();
        assert!(client.is_ready());

        client.restart().expect("explicit restart must succeed");

        assert_ne!(client.launch_id(), prior_launch);
        assert!(!client.is_ready());
        let first_after_restart = client
            .send_health()
            .expect("new launch health request must enqueue");
        assert_eq!(first_after_restart, INITIAL_COMMAND_ID);
        let response = health_response(
            client
                .receive()
                .expect("new launch health response must arrive"),
        );
        assert_eq!(response.launch_id, client.launch_id());
    }

    #[test]
    fn child_exit_invalidates_readiness_without_followup_protocol_call() {
        let mut client = CoreClient::start().expect("owned Core must start");
        let _ = client.send_health().expect("health request must enqueue");
        let _ = client.receive().expect("health response must arrive");
        assert!(client.is_ready());

        client
            .child
            .kill()
            .expect("owned Core must accept termination");
        let exit_deadline = std::time::Instant::now() + CHILD_TERMINATION_TIMEOUT;
        let mut exited = false;
        while !exited && std::time::Instant::now() < exit_deadline {
            match client
                .child
                .try_wait()
                .expect("owned Core status must remain readable")
            {
                Some(_) => exited = true,
                None => thread::sleep(CHILD_TERMINATION_POLL_INTERVAL),
            }
        }
        assert!(exited);

        let readiness_deadline = std::time::Instant::now() + CHILD_TERMINATION_TIMEOUT;
        while client.is_ready() && std::time::Instant::now() < readiness_deadline {
            thread::sleep(CHILD_TERMINATION_POLL_INTERVAL);
        }
        assert!(!client.is_ready());
    }

    #[test]
    fn idle_protocol_timeout_invalidates_readiness_without_infinite_wait() {
        let mut client = CoreClient::start().expect("owned Core must start");

        let error = client
            .receive()
            .expect_err("idle Core produces no unsolicited frame");

        assert!(matches!(error, CoreClientError::ProtocolTimeout));
        assert!(!client.is_ready());
    }

    #[test]
    fn observation_and_cancel_use_distinct_serialized_command_ids() {
        let mut client = CoreClient::start().expect("owned Core must start");
        let observation_id = client
            .send_observe_health()
            .expect("observation command must enqueue");
        let observation = client.receive().expect("observation response must arrive");
        assert!(matches!(
            observation,
            InboundEnvelope::Response(ResponseEnvelope::ObserveHealth(_))
        ));

        let cancel_id = client
            .send_cancel(observation_id)
            .expect("cancel command must enqueue");
        assert_eq!(cancel_id, observation_id + 1);
        let cancel = client.receive().expect("cancel response must arrive");
        assert!(matches!(
            cancel,
            InboundEnvelope::Response(ResponseEnvelope::Cancel(_))
        ));
    }
}
