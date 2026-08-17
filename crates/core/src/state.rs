use std::collections::{BTreeMap, VecDeque};
use std::fmt;
use wepld_contracts::{
    CancelEnvelope, CancelResponsePayload, CancellationOutcome, CapabilitiesResponsePayload,
    CapabilityList, EventEnvelope, EventFields, HealthObservationEventPayload,
    HealthResponsePayload, HealthStatus, ObserveHealthResponsePayload, Principal, ProtocolVersion,
    RequestEnvelope, ResponseEnvelope, ResponseFields, VersionResponsePayload,
};

pub const MAX_IN_FLIGHT_REQUESTS: usize = 32;
pub const MAX_HEALTH_WATCHES: usize = 8;
pub const MAX_TERMINAL_RESULTS: usize = MAX_IN_FLIGHT_REQUESTS;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CoreProfile {
    core_version: String,
    build_id: String,
    capabilities: CapabilityList,
}

impl CoreProfile {
    pub fn new(
        core_version: impl Into<String>,
        build_id: impl Into<String>,
        capabilities: CapabilityList,
    ) -> Self {
        Self {
            core_version: core_version.into(),
            build_id: build_id.into(),
            capabilities,
        }
    }

    pub fn core_version(&self) -> &str {
        &self.core_version
    }

    pub fn build_id(&self) -> &str {
        &self.build_id
    }

    pub fn capabilities(&self) -> &CapabilityList {
        &self.capabilities
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum OperationKind {
    Health,
    Version,
    Capabilities,
    ObserveHealth,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum InFlightStatus {
    Pending,
    ActiveWatch,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct InFlightEntry {
    operation: OperationKind,
    status: InFlightStatus,
    event_sequence: u64,
}

#[derive(Debug, PartialEq, Eq)]
#[must_use]
pub struct PendingRequest {
    launch_id: u64,
    request_id: u64,
    operation: OperationKind,
}

impl PendingRequest {
    pub fn launch_id(&self) -> u64 {
        self.launch_id
    }

    pub fn request_id(&self) -> u64 {
        self.request_id
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StateError {
    StaleLaunch {
        expected: u64,
        received: u64,
    },
    ReplayOrNonMonotonic {
        highest_accepted_command_id: u64,
        received: u64,
    },
    InFlightBudgetExhausted {
        max: usize,
    },
    HealthWatchBudgetExhausted {
        max: usize,
    },
    PendingRequestNoLongerInFlight {
        request_id: u64,
    },
    PendingRequestMismatch {
        request_id: u64,
    },
    HealthSequenceExhausted {
        request_id: u64,
    },
}

impl fmt::Display for StateError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::StaleLaunch { expected, received } => {
                write!(formatter, "stale launch {received}; expected {expected}")
            }
            Self::ReplayOrNonMonotonic {
                highest_accepted_command_id,
                received,
            } => write!(
                formatter,
                "command id {received} is not greater than high-water {highest_accepted_command_id}"
            ),
            Self::InFlightBudgetExhausted { max } => {
                write!(formatter, "in-flight request budget exhausted at {max}")
            }
            Self::HealthWatchBudgetExhausted { max } => {
                write!(formatter, "health-watch budget exhausted at {max}")
            }
            Self::PendingRequestNoLongerInFlight { request_id } => {
                write!(
                    formatter,
                    "pending request {request_id} is no longer in flight"
                )
            }
            Self::PendingRequestMismatch { request_id } => {
                write!(
                    formatter,
                    "pending request {request_id} does not match reserved state"
                )
            }
            Self::HealthSequenceExhausted { request_id } => {
                write!(
                    formatter,
                    "health sequence exhausted for request {request_id}"
                )
            }
        }
    }
}

impl std::error::Error for StateError {}

#[derive(Debug, PartialEq, Eq)]
pub struct HandshakeState {
    launch_id: u64,
    highest_accepted_command_id: Option<u64>,
    health_status: HealthStatus,
    profile: CoreProfile,
    in_flight: BTreeMap<u64, InFlightEntry>,
    terminal_results: VecDeque<u64>,
}

impl HandshakeState {
    pub fn new(launch_id: u64, profile: CoreProfile, health_status: HealthStatus) -> Self {
        Self {
            launch_id,
            highest_accepted_command_id: None,
            health_status,
            profile,
            in_flight: BTreeMap::new(),
            terminal_results: VecDeque::new(),
        }
    }

    pub fn launch_id(&self) -> u64 {
        self.launch_id
    }

    pub fn highest_accepted_command_id(&self) -> Option<u64> {
        self.highest_accepted_command_id
    }

    pub fn health_status(&self) -> HealthStatus {
        self.health_status
    }

    pub fn in_flight_count(&self) -> usize {
        self.in_flight.len()
    }

    pub fn health_watch_count(&self) -> usize {
        self.in_flight
            .values()
            .filter(|entry| entry.operation == OperationKind::ObserveHealth)
            .count()
    }

    pub fn terminal_result_count(&self) -> usize {
        self.terminal_results.len()
    }

    pub fn accept_request(
        &mut self,
        request: RequestEnvelope,
    ) -> Result<PendingRequest, StateError> {
        let (launch_id, request_id, operation) = request_identity(&request);
        self.validate_launch(launch_id)?;
        self.validate_command_id(request_id)?;

        if self.in_flight.len() >= MAX_IN_FLIGHT_REQUESTS {
            return Err(StateError::InFlightBudgetExhausted {
                max: MAX_IN_FLIGHT_REQUESTS,
            });
        }
        if operation == OperationKind::ObserveHealth
            && self.health_watch_count() >= MAX_HEALTH_WATCHES
        {
            return Err(StateError::HealthWatchBudgetExhausted {
                max: MAX_HEALTH_WATCHES,
            });
        }

        self.highest_accepted_command_id = Some(request_id);
        self.in_flight.insert(
            request_id,
            InFlightEntry {
                operation,
                status: InFlightStatus::Pending,
                event_sequence: 0,
            },
        );

        Ok(PendingRequest {
            launch_id,
            request_id,
            operation,
        })
    }

    pub fn dispatch_request(
        &mut self,
        pending: PendingRequest,
    ) -> Result<ResponseEnvelope, StateError> {
        self.validate_launch(pending.launch_id)?;
        let entry = *self.in_flight.get(&pending.request_id).ok_or(
            StateError::PendingRequestNoLongerInFlight {
                request_id: pending.request_id,
            },
        )?;

        if entry.operation != pending.operation || entry.status != InFlightStatus::Pending {
            return Err(StateError::PendingRequestMismatch {
                request_id: pending.request_id,
            });
        }

        match pending.operation {
            OperationKind::Health => {
                self.finish_request(pending.request_id);
                Ok(ResponseEnvelope::Health(ResponseFields {
                    protocol_version: ProtocolVersion::V1,
                    principal: Principal::DesktopHost,
                    launch_id: self.launch_id,
                    request_id: pending.request_id,
                    payload: HealthResponsePayload {
                        status: self.health_status,
                    },
                }))
            }
            OperationKind::Version => {
                self.finish_request(pending.request_id);
                Ok(ResponseEnvelope::Version(ResponseFields {
                    protocol_version: ProtocolVersion::V1,
                    principal: Principal::DesktopHost,
                    launch_id: self.launch_id,
                    request_id: pending.request_id,
                    payload: VersionResponsePayload {
                        core_version: self.profile.core_version.clone(),
                        build_id: self.profile.build_id.clone(),
                    },
                }))
            }
            OperationKind::Capabilities => {
                self.finish_request(pending.request_id);
                Ok(ResponseEnvelope::Capabilities(ResponseFields {
                    protocol_version: ProtocolVersion::V1,
                    principal: Principal::DesktopHost,
                    launch_id: self.launch_id,
                    request_id: pending.request_id,
                    payload: CapabilitiesResponsePayload {
                        capabilities: self.profile.capabilities.clone(),
                    },
                }))
            }
            OperationKind::ObserveHealth => {
                let reserved = self.in_flight.get_mut(&pending.request_id).ok_or(
                    StateError::PendingRequestNoLongerInFlight {
                        request_id: pending.request_id,
                    },
                )?;
                reserved.status = InFlightStatus::ActiveWatch;
                Ok(ResponseEnvelope::ObserveHealth(ResponseFields {
                    protocol_version: ProtocolVersion::V1,
                    principal: Principal::DesktopHost,
                    launch_id: self.launch_id,
                    request_id: pending.request_id,
                    payload: ObserveHealthResponsePayload {},
                }))
            }
        }
    }

    pub fn cancel(&mut self, cancel: CancelEnvelope) -> Result<ResponseEnvelope, StateError> {
        self.validate_launch(cancel.launch_id)?;
        self.validate_command_id(cancel.request_id)?;

        self.highest_accepted_command_id = Some(cancel.request_id);

        let outcome = if self.in_flight.remove(&cancel.target_request_id).is_some() {
            self.remember_terminal(cancel.target_request_id);
            CancellationOutcome::Cancelled
        } else if self.terminal_results.contains(&cancel.target_request_id) {
            CancellationOutcome::AlreadyTerminal
        } else {
            CancellationOutcome::UnknownTarget
        };

        Ok(ResponseEnvelope::Cancel(ResponseFields {
            protocol_version: ProtocolVersion::V1,
            principal: Principal::DesktopHost,
            launch_id: self.launch_id,
            request_id: cancel.request_id,
            payload: CancelResponsePayload { outcome },
        }))
    }

    pub fn update_health(
        &mut self,
        status: HealthStatus,
    ) -> Result<Vec<EventEnvelope>, StateError> {
        if status == self.health_status {
            return Ok(Vec::new());
        }

        for (&request_id, entry) in &self.in_flight {
            if entry.status == InFlightStatus::ActiveWatch && entry.event_sequence == u64::MAX {
                return Err(StateError::HealthSequenceExhausted { request_id });
            }
        }

        self.health_status = status;
        let mut events = Vec::with_capacity(self.health_watch_count());
        for (&request_id, entry) in &mut self.in_flight {
            if entry.status != InFlightStatus::ActiveWatch {
                continue;
            }
            entry.event_sequence += 1;
            events.push(EventEnvelope::ObserveHealth(EventFields {
                protocol_version: ProtocolVersion::V1,
                principal: Principal::DesktopHost,
                launch_id: self.launch_id,
                request_id,
                payload: HealthObservationEventPayload {
                    sequence: entry.event_sequence,
                    status,
                },
            }));
        }
        Ok(events)
    }

    fn validate_launch(&self, received: u64) -> Result<(), StateError> {
        if received != self.launch_id {
            return Err(StateError::StaleLaunch {
                expected: self.launch_id,
                received,
            });
        }
        Ok(())
    }

    fn validate_command_id(&self, received: u64) -> Result<(), StateError> {
        if let Some(highest_accepted_command_id) = self.highest_accepted_command_id
            && received <= highest_accepted_command_id
        {
            return Err(StateError::ReplayOrNonMonotonic {
                highest_accepted_command_id,
                received,
            });
        }
        Ok(())
    }

    fn finish_request(&mut self, request_id: u64) {
        self.in_flight.remove(&request_id);
        self.remember_terminal(request_id);
    }

    fn remember_terminal(&mut self, request_id: u64) {
        if self.terminal_results.len() == MAX_TERMINAL_RESULTS {
            self.terminal_results.pop_front();
        }
        self.terminal_results.push_back(request_id);
    }
}

fn request_identity(request: &RequestEnvelope) -> (u64, u64, OperationKind) {
    match request {
        RequestEnvelope::Health(fields) => {
            (fields.launch_id, fields.request_id, OperationKind::Health)
        }
        RequestEnvelope::Version(fields) => {
            (fields.launch_id, fields.request_id, OperationKind::Version)
        }
        RequestEnvelope::Capabilities(fields) => (
            fields.launch_id,
            fields.request_id,
            OperationKind::Capabilities,
        ),
        RequestEnvelope::ObserveHealth(fields) => (
            fields.launch_id,
            fields.request_id,
            OperationKind::ObserveHealth,
        ),
    }
}
