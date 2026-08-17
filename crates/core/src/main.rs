#![forbid(unsafe_code)]

#[derive(Debug)]
enum CoreProcessError {
    Frame,
    State,
    UnexpectedInboundKind,
}

impl From<::wepld_contracts::FrameError> for CoreProcessError {
    fn from(_: ::wepld_contracts::FrameError) -> Self {
        Self::Frame
    }
}

impl From<::wepld_core::StateError> for CoreProcessError {
    fn from(_: ::wepld_core::StateError) -> Self {
        Self::State
    }
}

fn write_protocol_frame(
    stdout: &mut ::std::io::StdoutLock<'_>,
    envelope: &::wepld_contracts::ProtocolEnvelope,
) -> Result<(), ::wepld_contracts::FrameError> {
    let wire = ::wepld_contracts::encode_frame(envelope)?;
    ::std::io::Write::write_all(stdout, &wire).map_err(|error| {
        ::wepld_contracts::FrameError::Io {
            kind: error.kind(),
        }
    })?;
    ::std::io::Write::flush(stdout).map_err(|error| ::wepld_contracts::FrameError::Io {
        kind: error.kind(),
    })
}

fn core_state(launch_id: u64) -> ::wepld_core::HandshakeState {
    let capabilities = ::wepld_contracts::CapabilityList::try_from(vec![
        ::wepld_contracts::Capability::Health,
        ::wepld_contracts::Capability::Version,
        ::wepld_contracts::Capability::Capabilities,
        ::wepld_contracts::Capability::HealthObservation,
        ::wepld_contracts::Capability::Cancellation,
    ])
    .expect("S1 capability set must remain within the frozen protocol budget");
    let profile =
        ::wepld_core::CoreProfile::new("0.0.0", "s1-008-core-process", capabilities);
    ::wepld_core::HandshakeState::new(
        launch_id,
        profile,
        ::wepld_contracts::HealthStatus::Healthy,
    )
}

fn request_launch_id(request: &::wepld_contracts::RequestEnvelope) -> u64 {
    match request {
        ::wepld_contracts::RequestEnvelope::Health(fields) => fields.launch_id,
        ::wepld_contracts::RequestEnvelope::Version(fields) => fields.launch_id,
        ::wepld_contracts::RequestEnvelope::Capabilities(fields) => fields.launch_id,
        ::wepld_contracts::RequestEnvelope::ObserveHealth(fields) => fields.launch_id,
    }
}

fn state_for_launch(
    state: &mut Option<::wepld_core::HandshakeState>,
    launch_id: u64,
) -> &mut ::wepld_core::HandshakeState {
    if state.is_none() {
        *state = Some(core_state(launch_id));
    }
    state
        .as_mut()
        .expect("state must exist after launch initialization")
}

fn handle_inbound(
    state: &mut Option<::wepld_core::HandshakeState>,
    envelope: ::wepld_contracts::ProtocolEnvelope,
) -> Result<::wepld_contracts::ProtocolEnvelope, CoreProcessError> {
    match envelope {
        ::wepld_contracts::ProtocolEnvelope::Request(request) => {
            let launch_id = request_launch_id(&request);
            let state = state_for_launch(state, launch_id);
            let pending = state.accept_request(request)?;
            let response = state.dispatch_request(pending)?;
            Ok(::wepld_contracts::ProtocolEnvelope::Response(response))
        }
        ::wepld_contracts::ProtocolEnvelope::Cancel(cancel) => {
            let state = state_for_launch(state, cancel.launch_id);
            let response = state.cancel(cancel)?;
            Ok(::wepld_contracts::ProtocolEnvelope::Response(response))
        }
        ::wepld_contracts::ProtocolEnvelope::Response(_)
        | ::wepld_contracts::ProtocolEnvelope::Event(_)
        | ::wepld_contracts::ProtocolEnvelope::ProtocolError(_) => {
            Err(CoreProcessError::UnexpectedInboundKind)
        }
    }
}

fn run() -> Result<(), CoreProcessError> {
    let stdin = ::std::io::stdin();
    let mut input = stdin.lock();
    let stdout = ::std::io::stdout();
    let mut output = stdout.lock();
    let mut state = None;

    loop {
        let inbound =
            ::wepld_contracts::read_frame::<_, ::wepld_contracts::ProtocolEnvelope>(&mut input)?;
        let outbound = handle_inbound(&mut state, inbound)?;
        write_protocol_frame(&mut output, &outbound)?;
    }
}

fn main() -> Result<(), CoreProcessError> {
    run()
}
